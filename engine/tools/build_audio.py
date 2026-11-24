"""Part sesleri + timing_<lang>.json + PAUSES_<lang>.json → audio/full_<lang>.mp3 ve audio/timing_<lang>_final.json
Satır sınırları en yakın sessizlik ortasına oturtulur (±0.5 sn); duraklamalar sessizliğe eklenir, ses içeriği değiştirilmez.
Kullanım: python3 engine/tools/build_audio.py videos/001 [--lang tr]"""
import os, sys, re, json, wave, subprocess, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import save_json
SR = 44100

def load(mp3, wav):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
    w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).copy(); return a

def silences(wav, db=-38, d=0.2):
    out = subprocess.run(["ffmpeg", "-i", wav, "-af", f"silencedetect=noise={db}dB:d={d}", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return [((s + e) / 2) for s, e in zip(st, en)]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr"); a = ap.parse_args(); v = a.vdir.rstrip("/")
    T = json.load(open(f"{v}/audio/timing_{a.lang}.json")); P = json.load(open(f"{v}/PAUSES_{a.lang}.json"))
    L = T["lines"]; ids = sorted(L); pcm = {}; mids = {}
    for k, info in T["parts"].items():
        wav = f"/tmp/ba_{k}.wav"; pcm[k] = load(os.path.join(v, "audio", a.lang, f"part_{k}.mp3"), wav); mids[k] = silences(wav)
    out = []; final = {}; snapped = 0
    for i, lid in enumerate(ids):
        part = L[lid]["part"]; tot = len(pcm[part]) / SR
        def snap(t):
            global_snapped = 0
            c = [m for m in mids[part] if abs(m - t) <= 0.5]
            return min(c, key=lambda m: abs(m - t)) if c else t
        s = 0.0 if i == 0 or L[ids[i - 1]]["part"] != part else snap(L[lid]["start"])
        nxt = ids[i + 1] if i + 1 < len(ids) else None
        e = tot if (nxt is None or L[nxt]["part"] != part) else snap(L[nxt]["start"])
        seg = pcm[part][int(s * SR):int(e * SR)]
        pause = P["after"].get(lid, P["default"])
        # her parçanın son satırından sonra doğal bitiş sessizliği zaten var; yine de duraklama ekle
        out.append(seg); out.append(np.zeros(int(pause * SR), dtype=np.int16))
        final[lid] = {"part": part, "start": round(s, 3), "end": round(e, 3), "speech": round(e - s, 3), "pause": pause, "dur": round(e - s + pause, 3)}
    audio = np.concatenate(out); wavp = f"{v}/audio/full_{a.lang}.wav"
    w = wave.open(wavp, "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(audio.tobytes()); w.close()
    mp3 = f"{v}/audio/full_{a.lang}.mp3"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wavp, "-b:a", "192k", mp3], check=True); os.remove(wavp)
    save_json(f"{v}/audio/timing_{a.lang}_final.json", {"lines": final, "total_sec": round(len(audio) / SR, 3), "note": "dur = konuşma + duraklama"})
    print("toplam", round(len(audio) / SR, 2), "sn ->", mp3)
if __name__ == "__main__": main()
