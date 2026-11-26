"""v2 render: SHOTS_v2.json sırasıyla (ana sahne kareleri + ara çekimler) yavaş yakınlaşmalı MP4.
Ana sahneler için assemble.py'nin ürettiği kareler (renders/<lang>/shots, yazı katmanları işlenmiş) kullanılır.
Kullanım: python3 engine/tools/render_v2.py videos/001 --audio audio/mix_tr_muziksiz.wav --out renders/tr/001_tr_v2_muziksiz.mp4"""
import os, sys, glob, json, argparse, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image
from assemble import cover, render_frame

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--audio"); ap.add_argument("--out", required=True); ap.add_argument("--fps", type=int, default=30)
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    shots = json.load(open(f"{v}/SHOTS_v2.json"))["shots"]
    scenes = {s["id"]: s for s in json.load(open(f"{v}/SCENES.json"))["scenes"]}
    main_frames = {os.path.basename(p)[5:9]: p for p in glob.glob(f"{v}/renders/{a.lang}/shots/*.jpg")}
    tmp = f"{v}/renders/{a.lang}/shots_v2"; os.makedirs(tmp, exist_ok=True)
    total = shots[-1]["start"] + shots[-1]["dur"]
    tasks = []
    for i, s in enumerate(shots):
        if s["new"]:
            src = sorted(glob.glob(f"{v}/images/001_{s['shot']}_v*.png"))[-1]
            fp = f"{tmp}/{s['shot']}.jpg"
            if not os.path.exists(fp): cover(Image.open(src)).save(fp, quality=93)
            focus = [0.5, 0.5]
        else:
            fp = main_frames[s["scene"]]; focus = scenes[s["scene"]].get("focus", [0.5, 0.5])
        t1 = shots[i + 1]["start"] if i + 1 < len(shots) else total
        f0, f1 = round(s["start"] * a.fps), round(t1 * a.fps); d = (f1 - f0) / a.fps
        is_map = s["scene"] == "S003" and not s["new"]
        z = 0.04 if is_map else max(0.025, min(0.06, 0.011 * d))   # kısa çekimler: daha az yakınlaşma
        tasks.append((fp, f1 - f0, focus, z, i % 2 == 0))
    out = f"{v}/{a.out}"
    ff = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1920x1080", "-r", str(a.fps), "-i", "-"]
    if a.audio: ff += ["-i", f"{v}/{a.audio}"]
    ff += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p"]
    if a.audio: ff += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    proc = subprocess.Popen(ff + [out], stdin=subprocess.PIPE)
    from multiprocessing import Pool
    with Pool(2) as pool:
        for t in tasks:
            for buf in pool.imap(render_frame, [t + (k,) for k in range(t[1])], chunksize=8):
                proc.stdin.write(buf)
    proc.stdin.close(); proc.wait()
    print(json.dumps({"out": out, "shots": len(tasks), "frames": sum(t[1] for t in tasks), "sec": round(total, 2)}))

if __name__ == "__main__":
    main()
