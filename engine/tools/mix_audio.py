"""Anlatım (ham, dokunulmaz) + müzik + efektleri tek parçada karıştırır -> audio/mix_<lang>.wav
Kullanım: python3 mix_audio.py videos/001 --lang tr
Müzik/efekt planı: videos/001/SOUND_PLAN.json (sahne bazlı, her iki dilde aynı)"""
import os, sys, json, argparse, subprocess
import numpy as np
SR = 48000
def load(path, gain_db=0.0):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2) * 10 ** (gain_db / 20)
def lufs_gain(x, target):
    mono = x.mean(1); w = int(0.4 * SR); n = len(mono) // w
    ms = (mono[:n * w].reshape(n, w) ** 2).mean(1); ms = ms[ms > 1e-7]
    cur = 10 * np.log10(ms.mean() + 1e-12) - 0.691
    return 10 ** ((target - cur) / 20)
def put(buf, clip, t, fade_in=0.0, fade_out=0.0):
    a = int(t * SR); b = min(len(buf), a + len(clip)); clip = clip[:b - a].copy()
    if a < 0 or len(clip) == 0: return
    fi, fo = int(fade_in * SR), int(fade_out * SR)
    if fi: k = min(fi, len(clip)); clip[:k] *= np.linspace(0, 1, k)[:, None]
    if fo: k = min(fo, len(clip)); clip[-k:] *= np.linspace(1, 0, k)[:, None]
    buf[a:b] += clip
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr"); ap.add_argument("--no-music", action="store_true"); ap.add_argument("--voice", help="TR zamanlamasına oturtulmuş başka bir anlatım (dublaj) dosyası"); ap.add_argument("--out"); a = ap.parse_args(); v = a.vdir.rstrip("/")
    plan = json.load(open(f"{v}/SOUND_PLAN.json")); scenes = json.load(open(f"{v}/SCENES.json"))["scenes"]
    T = json.load(open(f"{v}/audio/timing_{a.lang}_final.json"))["lines"]
    start, dur, t = {}, {}, 0.0
    for s in scenes:
        d = sum(T[l]["dur"] for l in s["lines"]); start[s["id"]] = t; dur[s["id"]] = d; t += d
    total = t
    voice = load(a.voice if a.voice else f"{v}/audio/full_{a.lang}.mp3"); N = max(len(voice), int((total + 1) * SR))
    voice_buf = np.zeros((N, 2), np.float32); voice_buf[:len(voice)] = voice
    # --- müzik ---
    music = np.zeros((N, 2), np.float32); X = 1.5
    for m in ([] if a.no_music else plan["music"]):
        t0 = start[m["from"]]; t1 = start[m["to"]] + dur[m["to"]]
        clip = load(f"{v}/audio/music/{m['file']}.mp3"); clip *= lufs_gain(clip, plan["music_lufs"])
        last = m is plan["music"][-1]
        length = (t1 - t0) + (0 if last else X)
        put(music, clip[:int(length * SR)], t0, fade_in=0.6 if m is plan["music"][0] else X, fade_out=3.0 if last else X)
    # --- ducking: anlatım varken müzik biraz daha kısılır ---
    env = np.abs(voice_buf.mean(1)); w = int(0.05 * SR); env = np.convolve(env, np.ones(w) / w, "same")
    speaking = (env > 0.01).astype(np.float32); k = int(0.35 * SR); sm = np.convolve(speaking, np.ones(k) / k, "same")
    music *= (1 - plan["duck"] * np.clip(sm * 1.5, 0, 1))[:, None]
    # --- efektler ---
    sfx = np.zeros((N, 2), np.float32)
    for e in plan["sfx"]:
        for sid in (e["scenes"] if "scenes" in e else [e["scene"]]):
            base = start[sid] + (dur[sid] + e["at"] if e["at"] < 0 else e["at"])
            clip = load(f"{v}/audio/sfx/{e['file']}.mp3", e.get("gain", 0))
            reps = e.get("times", 1); gap = e.get("gap", 1.0)
            if e.get("loop_to_scene"):
                L = dur[sid]; out = np.zeros((int(L * SR), 2), np.float32); p = 0
                while p < len(out): seg = clip[:len(out) - p]; out[p:p + len(seg)] += seg; p += len(clip) - int(0.5 * SR)
                put(sfx, out, base, fade_in=0.8, fade_out=1.0)
            else:
                for r in range(reps): put(sfx, clip, base + r * gap, 0.01, 0.05)
    sfx *= 10 ** (plan.get("sfx_master_db", 0) / 20)
    mix = voice_buf + music + sfx
    peak = np.abs(mix).max(); 
    if peak > 0.97: mix *= 0.97 / peak
    out = a.out or (f"{v}/audio/mix_{a.lang}" + ("_muziksiz" if a.no_music else "") + ".wav")
    pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
    import wave; w = wave.open(out, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
    print("mix", round(len(mix) / SR, 1), "sn, tepe", round(float(peak), 2), "->", out)
if __name__ == "__main__": main()
