"""DE v3 render: timeline_de_v3.json + Sprecher-Audio -> MP4 (yatay pan, çizgi titremesi, parşömen renk, müziksiz).
python3 engine/tools/render_de_v3.py videos/001 --audio audio/de_v3/voice_de_v3.wav --out renders/de/Kahve_001_DE_v3.mp4 [--sec 40]"""
import os, sys, json, glob, zlib, argparse, subprocess
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from assemble import cover
W, H, FPS = 1920, 1080, 30
_C = {}; _N = {}
def load(fp):
    im = _C.get(fp)
    if im is None:
        _C.clear(); im = np.asarray(Image.open(fp).convert("RGB"))
        if "_D" in os.path.basename(fp):  # ChatGPT-Bilder haben oben/unten Papierrand -> abschneiden
            a = im.astype(int); bg = np.median(np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3)]), axis=0)
            rows = np.where((abs(a - bg).sum(2) > 60).mean(1) > 0.3)[0]
            if len(rows) and (rows.min() > 12 or rows.max() < a.shape[0] - 13):
                im = np.ascontiguousarray(im[rows.min() + 4: rows.max() - 3])
        if im.shape[:2] != (H, W): im = np.asarray(cover(Image.fromarray(im)))
        _C[fp] = im
    return im
def grade(im, grey):
    f = im.astype(np.float32)
    g = f.mean(axis=2, keepdims=True); s = 0.92 - (0.30 if grey else 0)
    f = g + (f - g) * s
    f *= np.array([0.985, 1.0, 1.02], np.float32)
    return np.clip(f, 0, 255)
def noise(k, fp):
    key = (k, fp)
    if key not in _N:
        if len(_N) > 8: _N.clear()
        rng = np.random.default_rng(k * 7919 + zlib.crc32(fp.encode()) % 1000)
        _N[key] = tuple(cv2.resize(rng.standard_normal((6, 10)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) * 1.4 for _ in range(2))
    return _N[key]
XS, YS = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
def frame(task):
    fp, nfr, move, grey, i = task
    im = load(fp); u = i / max(1, nfr - 1); t = i / FPS
    if move in ("pan_l", "pan_r"):
        z = 1.10; ox = (W - W / z) * (u if move == "pan_r" else 1 - u)
    elif move == "push": z = 1.0 + 0.07 * u; ox = (W - W / z) / 2
    else: z = 1.025; ox = (W - W / z) / 2
    oy = (H - H / z) / 2
    M = np.float32([[z, 0, -ox * z], [0, z, -oy * z]])  # titreşim/nefes yok: yalnız pan + yakınlaşma
    out = cv2.warpAffine(im, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return grade(out, grey).astype(np.uint8).tobytes()
def resolve(v, s, sh):
    n = s["shot"]
    if n.startswith("D"): return f"{v}/images/001_{n}_v1.png"
    p = f"{v}/renders/de/shots_v2/{n}.jpg"
    if os.path.exists(p): return p
    sc = sh[n]["scene"]; return glob.glob(f"{v}/renders/de/shots/*_{sc}.jpg")[0]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--audio"); ap.add_argument("--out", required=True); ap.add_argument("--sec", type=float, default=0); ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float, default=0)
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    tl = json.load(open(f"{v}/timeline_de_v3.json"))["shots"]
    sh = {s["shot"]: s for s in json.load(open(f"{v}/SHOTS_v2.json"))["shots"]}
    tasks = []
    for i, s in enumerate(tl):
        if a.sec and s["start"] >= a.sec: break
        if s["start"] < a.t0 - 1e-6 or (a.t1 and s["start"] >= a.t1 - 1e-6): continue
        t1 = tl[i + 1]["start"] if i + 1 < len(tl) else s["start"] + s["dur"]
        if a.sec: t1 = min(t1, a.sec)
        n = round(t1 * FPS) - round(s["start"] * FPS)
        tasks.append((resolve(v, s, sh), n, s["move"], s["akt"].startswith("H2")))
    out = f"{v}/{a.out}"; os.makedirs(os.path.dirname(out), exist_ok=True)
    ff = ["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-"]
    if a.audio: ff += ["-i", f"{v}/{a.audio}"]
    ff += ["-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p"]
    if a.audio: ff += ["-c:a","aac","-b:a","192k","-shortest"]
    proc = subprocess.Popen(ff + [out], stdin=subprocess.PIPE)
    from multiprocessing import Pool
    with Pool(os.cpu_count() or 2) as pool:
        for fp, n, mv, gr in tasks:
            for buf in pool.imap(frame, [(fp, n, mv, gr, k) for k in range(n)], chunksize=10): proc.stdin.write(buf)
    proc.stdin.close(); proc.wait(); print(out)
if __name__ == "__main__": main()
