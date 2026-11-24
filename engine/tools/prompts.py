"""SCENES.json → IMAGE_PROMPTS.md + STORYBOARD.md (+ SCENES.json içine est_dur).
Kullanım: python3 engine/tools/prompts.py videos/001 [--lang tr]"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import (load_scenes, save_json, load_script_lines, line_timings,
                    scene_durations, image_filename)

STYLE = ("STYLE: hand-drawn editorial cartoon illustration, warm ink line art with variable line weight "
         "(thin tapered ends, slightly wobbly, not vector-perfect), flat colours with light diagonal ink hatching "
         "on shadow sides, subtle warm paper-grain texture over the whole image, muted warm palette (paper #F7F1E5, "
         "ink #1D1A17, terracotta #E4572E, teal #2A7F7A, sand #D9B27C, stone #B9AFA2), no gradients, no 3D render, "
         "no anime, no chibi, no photorealism.")
FORMAT = ("FORMAT: 16:9 landscape (1792x1024 or 1536x864). Keep the top ~12% and bottom ~15% calm and free of "
          "important details (text is added later on a separate layer).")
NEG = ("DO NOT: no text, no letters, no numbers, no captions, no signage writing, no watermark, no signature, "
       "no logos, no religious buildings or symbols, no gore or visible weapons in use, no realistic human faces, "
       "no noses on bean people (except where explicitly asked), do not change Fasulye's design.")

def build_prompt(s, data, prev):
    cast = data["cast"]
    parts = [STYLE, FORMAT, ""]
    who = [c for c in s["cast"] if c in cast]
    if who:
        parts.append("CHARACTERS (keep exactly this identity and anatomy):")
        if "fasulye" in who:
            parts.append("- " + cast["fasulye"])
            if s.get("fasulye_costume"):
                parts.append("  COSTUME: " + data["fasulye_costumes"][s["fasulye_costume"]])
        if any(c != "fasulye" for c in who):
            parts.append("- " + cast["bean_people"])
        for c in who:
            if c not in ("fasulye", "bean_people"):
                parts.append("- " + cast[c])
        parts.append("")
    parts += [
        f"SCENE: {s['action']}",
        f"POSE / EXPRESSION: {s['expression']}" if s.get("expression") else "",
        f"COMPOSITION: {s['composition']}",
        f"CAMERA: {s['camera']}",
        f"BACKGROUND: {s['background']}",
        f"COLOURS: {s['palette']}",
        f"STORY FUNCTION: {s['function']}",
        "CONTINUITY: " + s["continuity"] + (f" Previous scene was {prev['id']} ({prev['location']})." if prev else ""),
        "",
        NEG,
    ]
    return "\n".join(p for p in parts if p is not None).replace("\n\n\n", "\n\n").strip()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    a = ap.parse_args(); vdir = a.vdir.rstrip("/")
    data = load_scenes(vdir); scenes = data["scenes"]; vid = data["video"]
    script = load_script_lines(vdir, a.lang)
    timings, src = line_timings(vdir, a.lang)
    durs = scene_durations(scenes, timings)
    for s in scenes:
        s["est_dur"] = durs[s["id"]]
    data["timing_source"] = src
    data["total_est_sec"] = round(sum(durs.values()), 2)
    save_json(os.path.join(vdir, "SCENES.json"), data)

    # ---------- IMAGE_PROMPTS.md ----------
    img = [s for s in scenes if s["kind"] == "imagegen"]
    L = [f"# {vid} · IMAGE_PROMPTS · {data['title']['tr']}", "",
         "ChatGPT için: önce `IMAGE_GENERATION_GUIDE.md` oku. Her blok kendi başına eksiksiz bir prompttur; **kod bloğunun tamamını** kopyala.",
         f"Toplam ImageGen sahnesi: **{len(img)}** (+ thumbnail T01). Türev ve kart sahneleri motor tarafından üretilir (en altta).",
         "Dosya adı kuralı: `{video}_{Sxxx}_v{K}.png` → `videos/" + vid + "/images/`", ""]
    prev = None
    for s in scenes:
        if s["kind"] != "imagegen":
            continue
        narr = " ".join(script.get(l, "") for l in s["lines"])
        import re as _re
        linked = sorted(set(_re.findall(r"S\d{3}", s["continuity"] + " " + s["background"] + " " + s["action"])) - {s["id"]})
        linked = [x for x in linked if x < s["id"]]
        cont_refs = [f"images/{image_filename(vid, x).replace('_v1', '_vK')} (süreklilik)" for x in linked]
        L += [f"## {s['id']} — {s['title']}",
              f"- **Dosya:** `{image_filename(vid, s['id'])}`",
              f"- **Anlatım ({', '.join(s['lines'])}):** {narr}",
              f"- **Tahmini süre:** {s['est_dur']:.1f} sn ({src})",
              f"- **Referanslar:** " + (", ".join(f"`{r}`" for r in s["references"] + cont_refs) or "—"),
              f"- **Metin katmanı (motor):** {s['overlay'].get(a.lang, '—') if isinstance(s['overlay'].get(a.lang), str) else '—'}",
              "", "```", build_prompt(s, data, prev), "```", ""]
        prev = s
    t = data.get("thumbnail")
    if t:
        L += [f"## {t['id']} — Thumbnail", f"- **Dosya:** `{vid}_T01_v1.png`",
              "- **Metin katmanı (motor):** " + t["overlay"].get(a.lang, ""), "",
              "```", build_prompt(t, data, None), "```", ""]
    L += ["## Motorun ürettiği sahneler (ImageGen gerekmez)", "", "| Sahne | Tür | Kaynak | Efekt | Anlatım |", "|---|---|---|---|---|"]
    for s in scenes:
        if s["kind"] != "imagegen":
            eff = ", ".join(e["type"] for e in s.get("effects", []))
            L.append(f"| {s['id']} | {s['kind']} | {s.get('source','—')} | {eff} | {', '.join(s['lines'])} |")
    open(os.path.join(vdir, "IMAGE_PROMPTS.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    # ---------- STORYBOARD.md ----------
    B = [f"# {vid} · STORYBOARD · {data['title']['tr']}", "",
         f"Zamanlama kaynağı: **{src}** · toplam ≈ **{data['total_est_sec']/60:.1f} dk** ({data['total_est_sec']:.0f} sn) · hedef çekim ≈ {data['target_shot_sec']} sn",
         "Uzun sahneler montajda otomatik olarak ~2 sn'lik çekimlere bölünür (geniş → yakın → daha yakın).", "",
         "| # | Sahne | Başlangıç | Süre | Tür | Görsel | Metin katmanı | Anlatım |", "|---|---|---|---|---|---|---|---|"]
    t0 = 0.0
    for i, s in enumerate(scenes, 1):
        ov = s["overlay"].get(a.lang) or (s["overlay"].get("stamp", {}) or {}).get(a.lang, "")
        narr = " ".join(script.get(l, "") for l in s["lines"]).replace("|", "/")
        vis = s["title"] if s["kind"] == "imagegen" else f"{s['kind']} ← {s.get('source','motor')}"
        B.append(f"| {i} | {s['id']} | {int(t0//60)}:{t0%60:04.1f} | {s['est_dur']:.1f} | {s['kind']} | {vis} | {ov or '—'} | {narr} |")
        t0 += s["est_dur"]
    open(os.path.join(vdir, "STORYBOARD.md"), "w", encoding="utf-8").write("\n".join(B) + "\n")
    print(f"{len(img)} ImageGen promptu, {len(scenes)} sahne, toplam {data['total_est_sec']:.0f} sn ({src})")

if __name__ == "__main__":
    main()
