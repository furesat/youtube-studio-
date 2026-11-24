"""Görseller + metin katmanı + (varsa) ses → MP4 + SRT.
Kullanım:
  python3 engine/tools/assemble.py videos/001 --lang tr                 # eksik görsel varsa durur
  python3 engine/tools/assemble.py videos/001 --lang tr --placeholders  # eksikler storyboard kartı olur (animatik)
Çıktı: videos/NNN/renders/<lang>/ (git dışı)
Ses: audio/full_<lang>.(mp3|wav) + audio/timing_<lang>.json  VEYA  audio/<lang>/L001.(mp3|wav) …
"""
import os, sys, glob, math, argparse, subprocess, textwrap, json
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from common import (load_scenes, scan_images, line_timings, load_script_lines, FONT_TITLE, FONT_UI, MIN_SHOT, save_json)

W, H = 1920, 1080
PAPER = (247, 241, 229); INK = (29, 26, 23); RED = (184, 58, 43); TEAL = (42, 127, 122)

def font(size, weight="ExtraBold", path=FONT_TITLE):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f

def cover(img):
    img = img.convert("RGB"); r = max(W / img.width, H / img.height)
    img = img.resize((math.ceil(img.width * r), math.ceil(img.height * r)), Image.LANCZOS)
    x = (img.width - W) // 2; y = (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))

def punch(img, scale, focus):
    if scale <= 1.001: return img
    cw, ch = W / scale, H / scale
    cx = min(max(focus[0] * W, cw / 2), W - cw / 2); cy = min(max(focus[1] * H, ch / 2), H - ch / 2)
    return img.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.LANCZOS)

def placeholder(s, narr):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rectangle((60, 60, W - 60, H - 60), outline=INK, width=6)
    d.text((110, 100), s["id"], font=font(150), fill=RED)
    d.text((110, 290), s["title"], font=font(64, "Bold"), fill=INK)
    d.text((110, 380), "GÖRSEL BEKLENİYOR · " + s["kind"], font=font(36, "Medium", FONT_UI), fill=TEAL)
    y = 470
    for ln in textwrap.wrap(narr, 62)[:8]:
        d.text((110, y), ln, font=font(40, "Regular", FONT_UI), fill=INK); y += 56
    return im

def wobble_line(d, p0, p1, w, col):
    d.line([p0, p1], fill=col, width=w); r = w // 2
    for p in (p0, p1): d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=col)

def fx_red_x(im, focus):
    d = ImageDraw.Draw(im); cx, cy = focus[0] * W, focus[1] * H; r = 230
    wobble_line(d, (cx - r, cy - r * .8), (cx + r, cy + r * .8), 34, RED)
    wobble_line(d, (cx + r, cy - r * .8), (cx - r, cy + r * .8), 34, RED)

def fx_stamp(im, text, focus=(0.5, 0.5), angle=-8):
    f = font(150); tw = int(f.getlength(text)) + 120; th = 230
    st = Image.new("RGBA", (tw, th), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
    d.rounded_rectangle((8, 8, tw - 8, th - 8), radius=26, outline=RED + (235,), width=16)
    d.text((tw // 2, th // 2 + 6), text, font=f, fill=RED + (235,), anchor="mm")
    st = st.rotate(angle, expand=True, resample=Image.BICUBIC)
    x = int(W * 0.5 - st.width / 2); y = int(H * 0.45 - st.height / 2)
    im.paste(st, (x, y), st)

def fx_check_cross(im):
    d = ImageDraw.Draw(im)
    wobble_line(d, (360, 250), (440, 340), 30, TEAL); wobble_line(d, (440, 340), (600, 160), 30, TEAL)
    wobble_line(d, (1340, 160), (1540, 340), 30, RED); wobble_line(d, (1540, 160), (1340, 340), 30, RED)

def fx_pins(im, pins):
    d = ImageDraw.Draw(im); f = font(52, "Bold")
    for name, x, y in pins:
        px, py = int(x * W), int(y * H)
        d.ellipse((px - 26, py - 26, px + 26, py + 26), fill=RED, outline=INK, width=5)
        tw = f.getlength(name)
        d.rounded_rectangle((px + 34, py - 34, px + 58 + tw, py + 34), radius=14, fill=PAPER)
        d.text((px + 46, py), name, font=f, fill=INK, anchor="lm")

def map_card(s):
    im = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(im)
    d.rounded_rectangle((120, 90, W - 120, H - 90), radius=40, fill=(238, 243, 236), outline=INK, width=6)
    return im

def overlay_title(im, text):
    if not text: return
    f = font(96); d = ImageDraw.Draw(im)
    tw = f.getlength(text); x = (W - tw) / 2; y = 46
    pad = 28
    box = Image.new("RGBA", (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((x - pad * 2, y - 8, x + tw + pad * 2, y + 132), radius=24, fill=PAPER + (230,))
    im.paste(box, (0, 0), box)
    d.text((W / 2, y + 62), text, font=f, fill=INK, anchor="mm")

def base_image(s, found, scenes_by_id, args, narr):
    if s["kind"] == "engine_card":
        return map_card(s)
    sid = s["source"] if s["kind"] == "derived" else s["id"]
    if sid in found:
        return cover(Image.open(found[sid]))
    if not args.placeholders:
        raise SystemExit(f"Eksik görsel: {sid} (--placeholders ile animatik alınabilir)")
    return placeholder(scenes_by_id[sid], narr)

MAX_ZOOMS = 2  # bir sahnede en çok 2 yakınlaşma (kullanıcı kararı)

def shots_for(s, img, dur, lang, target):
    ov = s["overlay"]; title = ov.get(lang) if isinstance(ov.get(lang), str) else None
    stamp = (ov.get("stamp") or {}).get(lang)
    effects = {e["type"]: e for e in s.get("effects", [])}
    focus = s.get("focus", [0.5, 0.5])
    if "map_pins" in effects:
        im = img.copy(); overlay_title(im, title); fx_pins(im, effects["map_pins"]["pins"])
        return [(im, dur)]
    if s["kind"] == "derived" or effects.keys() & {"red_x", "stamp", "check_cross"}:
        im = punch(img.copy(), effects.get("punch_in", {}).get("scale", 1.0), focus)
        if "red_x" in effects: fx_red_x(im, (0.5, 0.5))
        if "check_cross" in effects: fx_check_cross(im)
        if stamp: fx_stamp(im, stamp)
        overlay_title(im, title)
        return [(im, dur)]
    n = min(MAX_ZOOMS + 1, max(1, round(dur / target))) if s["kind"] == "imagegen" else 1
    while n > 1 and dur / n < MIN_SHOT: n -= 1
    cycle = [1.0, 1.14, 1.28]  # en çok 2 yakınlaşma: geniş → yakın → daha yakın
    out = []
    for i in range(n):
        im = punch(img.copy(), cycle[i % len(cycle)], focus)
        if i == 0: overlay_title(im, title)
        out.append((im, dur / n))
    return out

def find_audio(vdir, lang):
    for ext in ("wav", "mp3", "m4a"):
        p = os.path.join(vdir, "audio", f"full_{lang}.{ext}")
        if os.path.exists(p): return p
    parts = sorted(glob.glob(os.path.join(vdir, "audio", lang, "L*.*")))
    return parts or None

def srt_time(t):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--placeholders", action="store_true"); ap.add_argument("--only", help="S001-S016 gibi aralık")
    args = ap.parse_args(); vdir = args.vdir.rstrip("/")
    data = load_scenes(vdir); scenes = data["scenes"]; by = {s["id"]: s for s in scenes}
    if args.only:
        a, b = args.only.split("-"); scenes = [s for s in scenes if a <= s["id"] <= b]
    found = scan_images(vdir); timings, src = line_timings(vdir, args.lang)
    script = load_script_lines(vdir, args.lang)
    out = os.path.join(vdir, "renders", args.lang); shots_dir = os.path.join(out, "shots")
    os.makedirs(shots_dir, exist_ok=True)
    for p in glob.glob(os.path.join(shots_dir, "*.jpg")): os.remove(p)
    concat, t, srt, n = [], 0.0, [], 0
    for s in scenes:
        dur = sum(timings.get(l, 0) for l in s["lines"])
        narr = " ".join(script.get(l, "") for l in s["lines"])
        img = base_image(s, found, by, args, narr)
        for im, d in shots_for(s, img, dur, args.lang, data.get("target_shot_sec", 2.2)):
            n += 1; fp = os.path.join(shots_dir, f"{n:04d}_{s['id']}.jpg")
            im.save(fp, quality=92); concat.append((fp, d))
        for l in s["lines"]:
            srt.append((t, t + timings.get(l, 0), script.get(l, ""))); t += timings.get(l, 0)
    with open(os.path.join(out, "concat.txt"), "w") as f:
        for fp, d in concat: f.write(f"file '{os.path.abspath(fp)}'\nduration {d:.3f}\n")
        f.write(f"file '{os.path.abspath(concat[-1][0])}'\n")
    with open(os.path.join(out, f"{data['video']}_{args.lang}.srt"), "w", encoding="utf-8") as f:
        for i, (a, b, txt) in enumerate(srt, 1): f.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n\n")
    mp4 = os.path.join(out, f"{data['video']}_{args.lang}.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(out, "concat.txt")]
    audio = find_audio(vdir, args.lang)
    if isinstance(audio, list):
        lst = os.path.join(out, "audio_concat.txt")
        with open(lst, "w") as f:
            for p in audio: f.write(f"file '{os.path.abspath(p)}'\n")
        cmd += ["-f", "concat", "-safe", "0", "-i", lst]
    elif audio:
        cmd += ["-i", audio]
    cmd += ["-vf", f"fps={data.get('fps',30)},format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]
    cmd += (["-c:a", "aac", "-b:a", "192k", "-shortest"] if audio else [])
    subprocess.run(cmd + [mp4], check=True)
    rep = {"mp4": os.path.relpath(mp4, vdir), "shots": n, "duration_sec": round(t, 2), "timing_source": src,
           "audio": bool(audio), "placeholders": sum(1 for s in scenes if (s.get("source") or s["id"]) not in found and s["kind"] != "engine_card")}
    save_json(os.path.join(out, "render_report.json"), rep)
    print(json.dumps(rep, ensure_ascii=False))

if __name__ == "__main__":
    main()
