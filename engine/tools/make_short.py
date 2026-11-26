"""Ana videonun bir bölümünden dikey YouTube Shorts (1080x1920) üretir.
Düzen: üstte soru başlığı · ortada çekimler (yazısız görseller, yavaş yakınlaşma, 9:16'ya kırpılmış) · altında gömülü altyazı · sonda kısa kapanış kartı.
Kullanım:
  python3 engine/tools/make_short.py videos/001 --start-shot S043 --end-scene S048 \
     --title "Kahveyi koklayarak|yakalayan polis" --out renders/shorts/001_short_prusya.mp4"""
import os, sys, json, glob, argparse, subprocess, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
W, H, FPS = 1080, 1920, 30
PAPER, INK, RED = (243, 233, 214), (29, 26, 23), (184, 58, 43)
FONT = os.path.join(os.path.dirname(__file__), "..", "fonts", "ShantellSans[BNCE,INFM,SPAC,wght].ttf")
IMG_Y, IMG_H = 470, 900          # görüntü alanı
CAP_Y = 1415                     # altyazı merkezi (Shorts arayüzü altta ~350 px kaplar)
END = 1.6                        # kapanış kartı süresi

def font(sz, w=800):
    f = ImageFont.truetype(FONT, sz); f.set_variation_by_axes([w, 60, 0, 0]); return f

def wrap(d, text, f, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def chunks(text, maxc=24):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if len(t) > maxc and cur: out.append(cur); cur = w
        else: cur = t
    if cur: out.append(cur)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--start-shot", required=True); ap.add_argument("--end-scene", required=True)
    ap.add_argument("--title", required=True, help="iki satır için | kullan; 2. satır kırmızı")
    ap.add_argument("--audio", default="audio/mix_tr_muziksiz.wav"); ap.add_argument("--out", required=True)
    ap.add_argument("--endtext", default="Tam hikâye kanalda")
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    shots = json.load(open(f"{v}/SHOTS_v2.json"))["shots"]
    scenes = {s["id"]: s for s in json.load(open(f"{v}/SCENES.json"))["scenes"]}
    i0 = next(i for i, s in enumerate(shots) if s["shot"] == a.start_shot)
    i1 = max(i for i, s in enumerate(shots) if s["scene"] == a.end_scene)
    sel = shots[i0:i1 + 1]; t0 = sel[0]["start"]; t1 = sel[-1]["start"] + sel[-1]["dur"]
    # altyazı parçaları (cümle süresi içinde karakter oranına göre)
    T = json.load(open(f"{v}/audio/timing_{a.lang}_final.json"))["lines"]
    acc0 = 0.0; ABS = {}
    for l in sorted(T): ABS[l] = acc0; acc0 += T[l]["dur"]   # 'start' parça içinde; mutlak başlangıç = önceki cümlelerin toplamı
    nar = {l.split("|")[0]: l.split("|", 1)[1].strip() for l in open(f"{v}/NARRATION.txt", encoding="utf-8") if l.startswith("L")}
    lines = [l for s in sel for l in scenes[s["scene"]]["lines"]]; lines = list(dict.fromkeys(lines))
    caps = []
    for l in lines:
        st, sp = ABS[l], T[l]["speech"]
        if st + sp <= t0 or st >= t1: continue
        cs = chunks(nar[l]); tot = sum(len(c) for c in cs); acc = 0
        for c in cs:
            a0 = st + sp * acc / tot; acc += len(c); a1 = st + sp * acc / tot
            if a1 > t0: caps.append((max(a0, t0) - t0, a1 - t0, c))
    # sabit katman: kâğıt + başlık
    base = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(base)
    tf = font(92); y = 170
    for k, part in enumerate(a.title.split("|")):
        for ln in wrap(d, part, tf, 960):
            d.text((W // 2, y), ln, font=tf, fill=RED if k else INK, anchor="mm"); y += 108
    bf = font(40, 700); d.text((W // 2, 1880 - 40), "", font=bf)  # (marka yazısı yok: Shorts arayüzü kanal adını gösterir)
    capf = font(66)
    def frame(img, z, fx, fy, cap):
        # görüntüyü IMG_H yüksekliğe ölçekle, odak noktasından W genişliğinde kırp, yavaş yakınlaş
        r = IMG_H * z / img.height; iw = img.width * r
        cx = min(max(fx * iw, W / 2), iw - W / 2); cy = fy * IMG_H * z
        cy = min(max(cy, IMG_H / 2), IMG_H * z - IMG_H / 2)
        c = (1 / r, 0, (cx - W / 2) / r, 0, 1 / r, (cy - IMG_H / 2) / r)
        tile = img.transform((W, IMG_H), Image.AFFINE, c, resample=Image.BICUBIC)
        f = base.copy(); f.paste(tile, (0, IMG_Y))
        dd = ImageDraw.Draw(f)
        dd.line((0, IMG_Y - 2, W, IMG_Y - 2), fill=INK, width=4); dd.line((0, IMG_Y + IMG_H + 1, W, IMG_Y + IMG_H + 1), fill=INK, width=4)
        if cap:
            ls = wrap(dd, cap, capf, 980); yy = CAP_Y - (len(ls) - 1) * 40
            for ln in ls:
                dd.text((W // 2, yy), ln, font=capf, fill=INK, anchor="mm", stroke_width=0); yy += 80
        return f
    tmp = f"{v}/renders/{a.lang}/shots_v2"; os.makedirs(os.path.dirname(f"{v}/{a.out}"), exist_ok=True)
    total = (t1 - t0) + END
    ff = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
          "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", f"{v}/{a.audio}",
          "-filter_complex", f"[1:a]afade=t=in:d=0.12,afade=t=out:st={t1 - t0 - 0.25:.3f}:d=0.25,apad=pad_dur={END}[a]",
          "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
          "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", f"{v}/{a.out}"]
    p = subprocess.Popen(ff, stdin=subprocess.PIPE)
    nfr_total = round(total * FPS); fi = 0; last = None
    for k, s in enumerate(sel):
        if s["new"]: src = sorted(glob.glob(f"{v}/images/001_{s['shot']}_v*.png"))[-1]; foc = [0.5, 0.5]
        else:
            g = sorted(glob.glob(f"{v}/images/001_{s['scene']}_v*.*"))
            src = g[-1] if g and scenes[s["scene"]]["kind"] == "imagegen" else sorted(glob.glob(f"{v}/renders/{a.lang}/shots/*_{s['scene']}.jpg"))[0]
            foc = scenes[s["scene"]].get("focus", [0.5, 0.5])
        img = Image.open(src).convert("RGB")
        e = (sel[k + 1]["start"] if k + 1 < len(sel) else t1) - t0
        n = round(e * FPS) - fi
        zin = k % 2 == 0
        for j in range(n):
            u = j / max(1, n - 1); z = 1 + 0.06 * (u if zin else 1 - u)
            t = (fi + j) / FPS; cap = next((c for a0, a1, c in caps if a0 <= t < a1), None)
            last = frame(img, z, foc[0], foc[1], cap); p.stdin.write(last.tobytes())
        fi += n
    # kapanış kartı
    endf = last.copy(); dd = ImageDraw.Draw(endf)
    dd.rectangle((0, CAP_Y - 90, W, CAP_Y + 90), fill=PAPER)
    dd.text((W // 2, CAP_Y), a.endtext, font=font(70), fill=RED, anchor="mm")
    for _ in range(nfr_total - fi): p.stdin.write(endf.tobytes())
    p.stdin.close(); p.wait()
    print(json.dumps({"out": f"{v}/{a.out}", "sec": round(total, 2), "shots": len(sel), "captions": len(caps)}))

if __name__ == "__main__":
    main()
