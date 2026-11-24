"""build.py - pilotu üretir.  Kullanım: python3 build.py [tr|de|en|all]
1) geçici zamanlama (voice 'estimate')  2) görsel katmanlar  3) metin katmanları (dil başına)
4) kompozit kareler  5) MP4 (temiz + inceleme)  6) SRT  7) storyboard  8) scene_plan.json"""
import sys, os, json, subprocess, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TOP = os.path.dirname(HERE)
ROOT = TOP if os.path.exists(os.path.join(TOP, "fasulye.py")) else os.path.join(TOP, "identity")   # kimlik kodu + fontlar
sys.path.insert(0, TOP); sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from PIL import Image, ImageDraw, ImageFont
from render import render
from pilot import SHOTS, TXT, END_HOLD
from voice.registry import get_provider
from voice.base import Line

LANGS = ["tr", "de", "en"] if (len(sys.argv) < 2 or sys.argv[1] == "all") else [sys.argv[1]]
OUT = os.path.join(HERE, "out"); LAY = os.path.join(HERE, "layers")
S = json.load(open(os.path.join(HERE, "script.json"), encoding="utf-8"))
CFG = json.load(open(os.path.join(TOP, "voice_config.json"), encoding="utf-8"))
FONT_UI = os.path.join(ROOT, "fonts", "Nunito[wght].ttf")
MIN_SHOT = 0.9

def timing(lang):
    vc = CFG["languages"].get(lang, {}); prov, warn = get_provider(vc.get("provider", "estimate"), lang)
    if warn: print("UYARI:", warn)
    res, t = [], 0.0
    for L in S["lines"]:
        r = prov.synthesize(Line(L["id"], L[lang], lang, L["style"]), os.path.join(OUT, lang, "audio"), {**vc.get("voice", {}), "write_silence": False})
        d = r.to_dict(); d["t0"] = round(t, 3); d["t1"] = round(t + r.duration, 3); d["text"] = L[lang]; t += r.duration; res.append(d)
    return {"lang": lang, "provider": prov.name, "timing_source": "estimated", "FINAL_SYNC": False, "total_s": round(t, 3), "lines": res}

def shot_times(T):
    by = {l["id"]: l for l in T["lines"]}; out = []
    for line_id in [l["id"] for l in S["lines"]]:
        group = [s for s in SHOTS if s[1] == line_id]; tot = sum(g[2] for g in group); L = by[line_id]
        t = L["t0"]; dur = L["t1"] - L["t0"]
        for g in group:
            d = max(MIN_SHOT, dur*g[2]/tot); out.append((g[0], round(t, 3), round(d, 3))); t += d
    # MIN_SHOT taşmalarını sona doğru düzelt: başlangıçları ardışık yap
    fixed, t = [], 0.0
    for sid, _, d in out: fixed.append((sid, round(t, 3), d)); t += d
    sid, t0, d = fixed[-1]; fixed[-1] = (sid, t0, round(d + END_HOLD, 3))
    return fixed

_FT = {}
def fit(item, s):
    """Gerçek ölçüm: Shantell (wght 800) ile genişliği PIL ölç, 1720 px'e sığdır."""
    size = item["size"]
    if size not in _FT:
        f = ImageFont.truetype(os.path.join(ROOT, "fonts", "ShantellSans[BNCE,INFM,SPAC,wght].ttf"), int(size))
        try:
            axes = f.get_variation_axes(); f.set_variation_by_axes([800 if a.get("name", b"") in (b"Weight", "Weight") else a["default"] for a in axes])
        except Exception: pass
        _FT[size] = f
    w = _FT[size].getlength(s) + 2*len(s)   # + letter-spacing
    limit = 1720 if item["anchor"] == "middle" else 1720 - item["x"]
    return size * min(1.0, limit / w)

def text_svg(items, lang):
    o = ""
    for it in items:
        s = TXT[it["key"]][lang]; size = fit(it, s)
        o += (f'<text x="{it["x"]}" y="{it["y"]}" font-family="Shantell" font-weight="{it["wt"]}" font-size="{size:.0f}" '
              f'fill="{it["col"]}" text-anchor="{it["anchor"]}" letter-spacing="2" lang="{lang}">{s}</text>')
    return o

def srt(T, path):
    def ts(x): h = int(x//3600); m = int(x % 3600//60); s = x % 60; return f"{h:02d}:{m:02d}:{int(s):02d},{int((s-int(s))*1000):03d}"
    with open(path, "w", encoding="utf-8") as f:
        for i, l in enumerate(T["lines"], 1): f.write(f"{i}\n{ts(l['t0'])} --> {ts(l['t1'])}\n{l['text']}\n\n")

def ffconcat(frames, times, mp4):
    lst = mp4 + ".txt"
    with open(lst, "w") as f:
        for (sid, t0, d), fr in zip(times, frames): f.write(f"file '{fr}'\nduration {d:.3f}\n")
        f.write(f"file '{frames[-1]}'\n")
    total = sum(d for _, _, d in times)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-t", f"{total:.3f}", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                    "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", mp4], check=True)
    os.remove(lst)

def review_frame(src, dst, caption, sid, d):
    """İnceleme karesi: görüntü %87'ye küçültülür, altyazı ayrı şeritte (ekrandaki metni örtmez)."""
    src_im = Image.open(src).convert("RGB").resize((1670, 940))
    im = Image.new("RGB", (1920, 1080), (24, 22, 20)); im.paste(src_im, (125, 0)); dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_UI, 32); f2 = ImageFont.truetype(FONT_UI, 22)
    words = caption.split(); lines, cur = [], ""
    for w in words:
        if dr.textlength(cur + " " + w, font=f) > 1700: lines.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    lines.append(cur)
    for i, ln in enumerate(lines[:2]): dr.text((960, 985 + i*42 - (20 if len(lines) > 1 else 0)), ln, font=f, fill="white", anchor="mm")
    dr.rectangle([125, 0, 700, 36], fill=(183, 58, 43))
    dr.text((136, 6), f"GEÇİCİ ZAMANLAMA · SES YOK · {sid} · {d:.2f} sn", font=f2, fill="white")
    im.save(dst)

def storyboard(times, T, lang, path_png):
    by = {l["id"]: l for l in T["lines"]}; f = ImageFont.truetype(FONT_UI, 20); fb = ImageFont.truetype(FONT_UI, 22)
    cols, tw, th, pad = 4, 440, 248, 24; pages = []
    per = 12
    for p0 in range(0, len(times), per):
        chunk = times[p0:p0+per]; rows = (len(chunk)+cols-1)//cols
        pg = Image.new("RGB", (cols*(tw+pad)+pad, 90 + rows*(th+150)), "#F7F1E5"); dr = ImageDraw.Draw(pg)
        dr.text((pad, 24), f"STORYBOARD — {S['title'][lang]}  ·  sayfa {p0//per+1}  ·  zamanlama geçicidir (tahmin)", font=fb, fill="#1D1A17")
        for i, (sid, t0, d) in enumerate(chunk):
            r, c = divmod(i, cols); x = pad + c*(tw+pad); y = 80 + r*(th+150)
            im = Image.open(os.path.join(OUT, lang, "frames", f"{sid}.png")).convert("RGB").resize((tw, th)); pg.paste(im, (x, y))
            dr.rectangle([x, y, x+tw, y+th], outline="#1D1A17", width=2)
            shot = [s for s in SHOTS if s[0] == sid][0]
            dr.text((x, y+th+8), f"{sid}  ·  {t0:5.2f}s  ·  {d:.2f}s  ·  {shot[1]}", font=fb, fill="#B83A2B")
            txt = by[shot[1]]["text"]; lines, cur = [], ""
            for w in txt.split():
                if dr.textlength(cur + " " + w, font=f) > tw: lines.append(cur); cur = w
                else: cur = (cur + " " + w).strip()
            lines.append(cur)
            for k, ln in enumerate(lines[:3]): dr.text((x, y+th+38+k*24), ln, font=f, fill="#1D1A17")
            dr.text((x, y+th+112), "Not: " + shot[5], font=f, fill="#555")
        pages.append(pg)
    for i, pg in enumerate(pages): pg.save(path_png.replace(".png", f"_{i+1}.png"))
    pages[0].save(path_png.replace(".png", ".pdf"), save_all=True, append_images=pages[1:])

def main():
    os.makedirs(os.path.join(LAY, "art"), exist_ok=True)
    jobs = [(fn(), os.path.join(LAY, "art", f"{sid}.png"), 1920, 1080) for sid, _, _, fn, _, _ in SHOTS]
    for lang in LANGS:
        os.makedirs(os.path.join(LAY, f"text_{lang}"), exist_ok=True)
        jobs += [(text_svg(items, lang), os.path.join(LAY, f"text_{lang}", f"{sid}_txt.png"), 1920, 1080) for sid, _, _, _, items, _ in SHOTS]
    render(jobs, transparent=True)
    plan = {"title": S["title"], "fps": 30, "resolution": [1920, 1080], "timing_note": "GEÇİCİ: voice 'estimate' sağlayıcısı; nihai ses senkronu değildir.", "shots": [], "languages": {}}
    for sid, line, w, _, items, note in SHOTS:
        plan["shots"].append({"id": sid, "line": line, "weight": w, "note": note, "art": f"layers/art/{sid}.png",
                              "text": {lg: f"layers/text_{lg}/{sid}_txt.png" for lg in ["tr", "de", "en"]}, "text_items": items})
    for lang in LANGS:
        T = timing(lang); times = shot_times(T); d = os.path.join(OUT, lang); os.makedirs(os.path.join(d, "frames"), exist_ok=True); os.makedirs(os.path.join(d, "review"), exist_ok=True)
        json.dump(T, open(os.path.join(d, f"timing_{lang}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        frames, rframes = [], []
        cap = {l["id"]: l["text"] for l in T["lines"]}
        for sid, t0, dur in times:
            a = Image.open(os.path.join(LAY, "art", f"{sid}.png")).convert("RGBA"); t = Image.open(os.path.join(LAY, f"text_{lang}", f"{sid}_txt.png")).convert("RGBA")
            fp = os.path.join(d, "frames", f"{sid}.png"); Image.alpha_composite(a, t).convert("RGB").save(fp); frames.append(fp)
            rp = os.path.join(d, "review", f"{sid}.png"); review_frame(fp, rp, cap[[s for s in SHOTS if s[0] == sid][0][1]], sid, dur); rframes.append(rp)
        ffconcat(frames, times, os.path.join(d, f"pilot_{lang}_1080p.mp4"))
        ffconcat(rframes, times, os.path.join(d, f"pilot_{lang}_inceleme_altyazili.mp4"))
        srt(T, os.path.join(d, f"pilot_{lang}.srt"))
        storyboard(times, T, lang, os.path.join(d, f"storyboard_{lang}.png"))
        plan["languages"][lang] = {"total_s": round(sum(x[2] for x in times), 2), "shots": [{"id": s, "t0": t0, "dur": dd} for s, t0, dd in times]}
        print(lang, "toplam", plan["languages"][lang]["total_s"], "sn,", len(times), "çekim, ort.", round(plan["languages"][lang]["total_s"]/len(times), 2))
    json.dump(plan, open(os.path.join(HERE, "scene_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__": main()
