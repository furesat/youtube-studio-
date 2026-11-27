"""v3: v2 + 'canlı çizim' hareketi. Yavaş yakınlaşmaya ek olarak:
 - çizgi titremesi (boil): 8 kare/sn'de değişen, düşük frekanslı çok küçük kaydırma dalgası
 - hafif nefes alma (kuyruk-sallanma değil, tüm kareye ~%0.4 salınım)
Kullanım: python3 engine/tools/render_v3_alive.py videos/001 --lang de --audio audio/dublaj_de_muziksiz.wav --out renders/de/x.mp4 [--sec 40]"""
import zlib, os, sys, glob, json, argparse, subprocess
import numpy as np, cv2
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from assemble import cover
_C = {}
def frame(task):
    fp, nfr, focus, zmax, zin, i, fps = task
    im = _C.get(fp)
    if im is None:
        _C.clear(); im = _C[fp] = np.asarray(Image.open(fp).convert("RGB"))
    H, W = im.shape[:2]; u = i / max(1, nfr - 1)
    z = 1 + zmax * (u if zin else 1 - u)
    t = i / fps
    z *= 1 + 0.004 * np.sin(2 * np.pi * t / 4.0)             # nefes
    fx, fy = focus
    M = np.float32([[z, 0, W * fx * (1 - z)], [0, z, H * fy * (1 - z)]])
    # boil: 8 fps'te değişen yumuşak dalga haritası (±1.6 px)
    k = int(t * 8); rng = np.random.default_rng(k * 7919 + zlib.crc32(fp.encode()) % 1000)
    gx = cv2.resize(rng.standard_normal((6, 10)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) * 1.6
    gy = cv2.resize(rng.standard_normal((6, 10)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC) * 1.6
    xs, ys = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    sx = ((xs - M[0, 2]) / z + gx).astype(np.float32); sy = ((ys - M[1, 2]) / z + gy).astype(np.float32)
    return cv2.remap(im, sx, sy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).tobytes()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--audio"); ap.add_argument("--out", required=True); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--sec", type=float, default=0)
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    shots = json.load(open(f"{v}/SHOTS_v2.json"))["shots"]
    scenes = {s["id"]: s for s in json.load(open(f"{v}/SCENES.json"))["scenes"]}
    main_frames = {os.path.basename(p)[5:9]: p for p in glob.glob(f"{v}/renders/{a.lang}/shots/*.jpg")}
    tmp = f"{v}/renders/{a.lang}/shots_v2"
    total = shots[-1]["start"] + shots[-1]["dur"]; tasks = []
    for i, s in enumerate(shots):
        if a.sec and s["start"] >= a.sec: break
        if s["new"]: fp = f"{tmp}/{s['shot']}.jpg"; focus = [0.5, 0.5]
        else: fp = main_frames[s["scene"]]; focus = scenes[s["scene"]].get("focus", [0.5, 0.5])
        t1 = shots[i + 1]["start"] if i + 1 < len(shots) else total
        if a.sec: t1 = min(t1, a.sec)
        f0, f1 = round(s["start"] * a.fps), round(t1 * a.fps); d = (f1 - f0) / a.fps
        z = 0.04 if (s["scene"] == "S003" and not s["new"]) else max(0.025, min(0.06, 0.011 * d))
        tasks.append((fp, f1 - f0, focus, z, i % 2 == 0))
    out = f"{v}/{a.out}"; os.makedirs(os.path.dirname(out), exist_ok=True)
    ff = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(a.fps), "-i", "-"]
    if a.audio: ff += ["-i", f"{v}/{a.audio}"]
    ff += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
    if a.audio: ff += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    proc = subprocess.Popen(ff + [out], stdin=subprocess.PIPE)
    from multiprocessing import Pool
    with Pool(os.cpu_count() or 2) as pool:
        for t in tasks:
            for buf in pool.imap(frame, [t + (k, a.fps) for k in range(t[1])], chunksize=8):
                proc.stdin.write(buf)
    proc.stdin.close(); proc.wait(); print(out)
if __name__ == "__main__": main()
