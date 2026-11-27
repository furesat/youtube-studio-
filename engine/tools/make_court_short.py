"""Fasulye Mahkemesi Short'u (1080x1920) hazır dikey görsellerden + tek parça sesten üretir.
Kullanım: python3 engine/tools/make_court_short.py shorts/fasulye-mahkemesi/01_tokalasma/episode.json
episode.json: {"audio":..., "images_dir":..., "out":..., "verdict":"ŞÜPHELİ", "series":"Fasulye Mahkemesi #01",
               "lines":[{"text":"...", "shots":[["FM_ORTAK_01_v1.png",0.3],["FM01_E1_v1.png",0.7]], "stamp":false}]}
Zamanlama: ses süresi karakter oranıyla cümlelere bölünür; kesimler en yakın sessizliğe (±0.45 sn) oturtulur.
"""
import os, sys, json, subprocess, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 30
PAPER, INK, RED = (243, 233, 214), (29, 26, 23), (184, 58, 43)
FONT = os.path.join(os.path.dirname(__file__), "..", "fonts", "ShantellSans[BNCE,INFM,SPAC,wght].ttf")
CAP_Y = 1560   # altyazı merkezi (Shorts arayüzü alt ~350 px kaplar → mümkün olduğunca yukarıda)
ZOOM = 0.05

def font(sz, w=800):
    f = ImageFont.truetype(FONT, sz); f.set_variation_by_axes([w, 60, 0, 0]); return f

def chunks(text, maxc=24):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if len(t) > maxc and cur: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out

def silences(audio):
    r = subprocess.run(["ffmpeg", "-i", audio, "-af", "silencedetect=noise=-35dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return [((a + b) / 2) for a, b in zip(st, en)]

def snap(t, sil, tol=0.8):
    c = [s for s in sil if abs(s - t) <= tol]
    return min(c, key=lambda s: abs(s - t)) if c else t

def cover(img, z, fx=0.5, fy=0.5):
    r = max(W / img.width, H / img.height) * z; iw, ih = img.width * r, img.height * r
    cx = min(max(fx * iw, W / 2), iw - W / 2); cy = min(max(fy * ih, H / 2), ih - H / 2)
    c = (1 / r, 0, (cx - W / 2) / r, 0, 1 / r, (cy - H / 2) / r)
    return img.transform((W, H), Image.AFFINE, c, resample=Image.BICUBIC)

def stamp(f, word, u):
    # damga: büyük kırmızı, hafif döndürülmüş, içe doğru 'çarpma' animasyonu
    s = 1.0 + 0.9 * max(0, 1 - u / 0.18) ** 2
    ft = font(int(135 * s)); tmp = Image.new("RGBA", (W + 400, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    d.text((tmp.width // 2, 200), word, font=ft, fill=RED + (235,), anchor="mm", stroke_width=6, stroke_fill=(243, 233, 214, 255))
    bb = d.textbbox((tmp.width // 2, 200), word, font=ft, anchor="mm")
    d.rectangle((bb[0] - 28, bb[1] - 22, bb[2] + 28, bb[3] + 22), outline=RED + (235,), width=12)
    tmp = tmp.rotate(8, resample=Image.BICUBIC, expand=True)
    f.paste(tmp, ((W - tmp.width) // 2, 1330 - tmp.height // 2), tmp)

def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8")); base = os.path.dirname(os.path.abspath(sys.argv[1]))
    P = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    audio = P(cfg["audio"]); imgdir = P(cfg["images_dir"]); out = P(cfg["out"])
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).decode())
    lead, tail = cfg.get("lead", 0.15), cfg.get("tail", 0.7)
    total_speech = dur
    lines = cfg["lines"]; chars = [len(l["text"]) for l in lines]; T = sum(chars); sil = silences(audio)
    # cümle sınırları
    b = [0.0]; acc = 0
    for c in chars[:-1]:
        acc += c; b.append(snap(total_speech * acc / T, sil))
    b.append(total_speech)
    # çekimler ve altyazılar
    shots, caps, stamps = [], [], []
    for i, l in enumerate(lines):
        t0, t1 = b[i], b[i + 1]; ws = sum(w for _, w in l["shots"]); cur = t0
        for k, (im, w) in enumerate(l["shots"]):
            e = t1 if k == len(l["shots"]) - 1 else snap(cur + (t1 - t0) * w / ws, sil, 0.3); shots.append((cur, e, im)); cur = e
        cs = chunks(l["text"]); tot = sum(len(c) for c in cs); a = t0
        for c in cs:
            e = a + (t1 - t0) * len(c) / tot; caps.append((a, e, c)); a = e
        if l.get("stamp"): stamps.append((t0 + (t1 - t0) * 0.55, t1 + 1.0))
    total = lead + total_speech + tail
    shots[0] = (0.0, shots[0][1], shots[0][2]); shots[-1] = (shots[-1][0], total_speech + tail, shots[-1][2])
    imgs = {n: Image.open(os.path.join(imgdir, n)).convert("RGB") for n in {s[2] for s in shots}}
    capf = font(68)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    ff = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
          "-i", audio, "-filter_complex", f"[1:a]adelay={int(lead*1000)}|{int(lead*1000)},afade=t=in:d=0.08,apad=pad_dur={tail}[a]",
          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
          "-t", f"{total:.3f}", "-movflags", "+faststart", out]
    p = subprocess.Popen(ff, stdin=subprocess.PIPE); nfr = round(total * FPS)
    for fi in range(nfr):
        t = fi / FPS - lead
        k = next((j for j, s in enumerate(shots) if s[0] <= t < s[1]), len(shots) - 1); s0, s1, im = shots[k]
        u = min(1, max(0, (t - s0) / max(0.01, s1 - s0))); z = 1 + ZOOM * (u if k % 2 == 0 else 1 - u)
        f = cover(imgs[im], z)
        d = ImageDraw.Draw(f)
        cap = next((c for a0, a1, c in caps if a0 <= t < a1), None)
        if cap:
            d.text((W // 2, CAP_Y), cap, font=capf, fill=PAPER, anchor="mm", stroke_width=9, stroke_fill=INK)
        for a0, a1 in stamps:
            if a0 <= t < a1: stamp(f, cfg.get("verdict", "ŞÜPHELİ"), (t - a0) / max(0.01, a1 - a0) * 3)
        p.stdin.write(f.tobytes())
    p.stdin.close(); p.wait()
    # SRT
    def ts(x):
        ms = int(round(max(0, x + lead) * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s_, ms = divmod(ms, 1000); return f"{h:02d}:{m:02d}:{s_:02d},{ms:03d}"
    srt = [f"{i+1}\n{ts(b[i])} --> {ts(b[i+1])}\n{l['text']}\n" for i, l in enumerate(lines)]
    open(os.path.splitext(out)[0] + ".srt", "w", encoding="utf-8").write("\n".join(srt))
    print(json.dumps({"out": out, "sec": round(total, 2), "shots": len(shots), "captions": len(caps)}))

if __name__ == "__main__":
    main()
