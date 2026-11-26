"""Başka dildeki anlatımı ana dilin (TR) sahne zamanlamasına oturtur -> YouTube çok dilli ses (dublaj) izi.
Her sahne: TR'deki başlangıcında (ya da önceki sahne taşarsa hemen ardından) başlar; sığmazsa en çok %15 hızlandırılır,
kısa kalırsa sonuna sessizlik eklenir. Kullanım: python3 engine/tools/fit_dub.py videos/001 --lang de"""
import json, argparse, subprocess, numpy as np
SR = 48000; CAP = 1.15; EARLY = 0.6; LAG = 0.8   # sahne sesi görüntüden en çok 0,6 sn önce başlayabilir, 0,8 sn taşabilir
def load(p):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
def squeeze(x, need, floor=0.30, thr_db=-40):
    """Uzun sessizlikleri (en uzundan başlayarak) en çok `floor` sn'ye kadar kısaltır; `need` sn kazanmaya çalışır."""
    w = int(0.02 * SR); n = len(x) // w
    if need <= 0 or n == 0: return x
    e = 20 * np.log10(np.sqrt((x[:n * w].mean(1).reshape(n, w) ** 2).mean(1)) + 1e-9); sil = e < thr_db
    runs, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            if (j - i) * 0.02 > floor and i > 0 and j < n: runs.append((i, j))
            i = j
        else: i += 1
    cut = {}; left = need
    for a0, a1 in sorted(runs, key=lambda r: r[0] - r[1]):
        if left <= 0: break
        c = min((a1 - a0) * 0.02 - floor, left); cut[a0] = (a1, c); left -= c
    out, pos = [], 0
    for a0 in sorted(cut):
        a1, c = cut[a0]; mid = (a0 + a1) // 2 * w; k = int(c * SR)
        out.append(x[pos:mid - k // 2]); pos = mid - k // 2 + k
    out.append(x[pos:]); return np.concatenate(out)
def tempo(x, f):
    if abs(f - 1) < 1e-3: return x
    p = subprocess.run(["ffmpeg", "-loglevel", "error", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-i", "-", "-af", f"atempo={f:.4f}",
                        "-f", "f32le", "-"], input=x.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(p, dtype=np.float32).reshape(-1, 2)
ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="de"); ap.add_argument("--base", default="tr")
a = ap.parse_args(); v = a.vdir.rstrip("/")
sc = json.load(open(f"{v}/SCENES.json"))["scenes"]
TB = json.load(open(f"{v}/audio/timing_{a.base}_final.json"))["lines"]; TL = json.load(open(f"{v}/audio/timing_{a.lang}_final.json"))["lines"]
voice = load(f"{v}/audio/full_{a.lang}.mp3")
total = sum(TB[l]["dur"] for s in sc for l in s["lines"]); out = np.zeros((int((total + 0.5) * SR), 2), np.float32)
tb = 0.0; end = 0.0; rep = []
for s in sc:
    t = sum(TB[l]["dur"] for l in s["lines"])
    a0 = TL[s["lines"][0]]["start"]; a1 = TL[s["lines"][-1]]["start"] + TL[s["lines"][-1]]["dur"]
    seg = voice[int(a0 * SR):int(a1 * SR)]; d = len(seg) / SR; d0 = d
    st = max(tb - EARLY if s is not sc[0] else 0.0, end); avail = min(tb + t + LAG, total) - st
    if avail > 0 and d > avail: seg = squeeze(seg, d - avail); d = len(seg) / SR
    f = min(CAP, max(1.0, d / avail)) if avail > 0 else CAP
    seg = tempo(seg, f); i = int(st * SR); seg = seg[:max(0, len(out) - i)]
    out[i:i + len(seg)] += seg; end = st + len(seg) / SR
    rep.append({"scene": s["id"], "lag": round(st - tb, 2), "speed": round(f, 3), "src_start": a0, "src_dur": d0, "dst_start": st, "dst_dur": len(seg) / SR}); tb += t
out = out[:int(total * SR)]
o = f"{v}/audio/dub_{a.lang}_on_{a.base}.wav"
import wave; w = wave.open(o, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
json.dump(rep, open(f"{v}/audio/dub_{a.lang}_on_{a.base}.json", "w"), indent=0)
print(o, round(len(out) / SR, 2), "sn; max gecikme", max(r["lag"] for r in rep), "sn; >%10 hızlanan sahne:", [r["scene"] for r in rep if r["speed"] > 1.1])
