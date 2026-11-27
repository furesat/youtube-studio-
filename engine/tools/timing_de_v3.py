"""DE v3: EDL satırlarını gerçek ses zamanına oturtur (sessizlik + karakter oranı). Çıktı: videos/001/timeline_de_v3.json"""
import json, re, subprocess, sys
V = "videos/001"
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
def silences(f):
    o = subprocess.run(["ffmpeg","-hide_banner","-i",f,"-af","silencedetect=noise=-38dB:d=0.22","-f","null","-"],capture_output=True,text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", o)]; e = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", o)]
    return [((a+b)/2) for a,b in zip(s,e)]
edl = json.load(open(f"{V}/EDL_de_v3.json"))["edl"]
k = next(i for i,e in enumerate(edl) if e["text"].startswith("Und damit zurück nach Preußen"))
import os
TEMPO = 0.94  # Sprecher etwas ruhiger (Tonhöhe bleibt)
for n in (1, 2):
    o = f"{V}/audio/de_v3/teil{n}_t.wav"
    if not os.path.exists(o): subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{V}/audio/de_v3/teil{n}.mp3","-af",f"atempo={TEMPO}","-ar","44100","-ac","1",o],check=True)
parts = [(edl[:k], f"{V}/audio/de_v3/teil1_t.wav"), (edl[k:], f"{V}/audio/de_v3/teil2_t.wav")]
GAP = 1.2; off = 0.0; out = []
for items, f in parts:
    D = dur(f); sil = silences(f); tot = sum(len(e["text"]) for e in items)
    # sessizlik başı/sonu kırp: konuşma ~0.1..D-0.2
    a0, a1 = 0.1, D - 0.15
    cum = 0; bounds = [0.0]
    for e in items[:-1]:
        cum += len(e["text"]); t = a0 + (a1 - a0) * cum / tot
        near = min(sil, key=lambda s: abs(s - t)) if sil else t
        bounds.append(near if abs(near - t) < 2.2 else t)
    bounds.append(D)
    for i in range(1, len(bounds)):  # monoton
        bounds[i] = max(bounds[i], bounds[i-1] + 1.2) if i < len(bounds)-1 else bounds[i]
    for e, s, t in zip(items, bounds[:-1], bounds[1:]):
        out.append(dict(e, start=round(off + s, 3), dur=round(t - s, 3)))
    off += D + GAP
    if out: out[-1]["dur"] = round(out[-1]["dur"] + GAP, 3)
json.dump({"parts": [p[1] for p in parts], "gap": GAP, "total": round(off - GAP, 2), "shots": out}, open(f"{V}/timeline_de_v3.json","w"), ensure_ascii=False, indent=1)
print("toplam", round(off - GAP, 1), "sn;", len(out), "çekim; min/max", min(x["dur"] for x in out), max(x["dur"] for x in out))
