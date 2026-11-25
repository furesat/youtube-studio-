"""Video klasörleri için ortak yardımcılar: SCENES.json, anlatım, süre, görsel eşleştirme."""
import json, os, re, glob, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from voice.providers.estimate import syllables, DEFAULT_RATE  # tek tahmin formülü

FONT_TITLE = os.path.join(ROOT, "engine", "fonts", "ShantellSans[BNCE,INFM,SPAC,wght].ttf")
FONT_UI = os.path.join(ROOT, "engine", "fonts", "Nunito[wght].ttf")
LINE_PAUSE = 0.28          # satırlar arası nefes (sn), tahmin modunda
MIN_SHOT = 1.0

def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def save_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")

def load_scenes(vdir):
    return load_json(os.path.join(vdir, "SCENES.json"))

def load_narration(vdir, lang="tr"):
    name = "NARRATION.txt" if lang == "tr" else f"NARRATION_{lang}.txt"
    out = {}
    p = os.path.join(vdir, name)
    if not os.path.exists(p):
        return out
    for ln in open(p, encoding="utf-8"):
        ln = ln.rstrip("\n")
        if not ln or ln.startswith("#") or "|" not in ln:
            continue
        lid, txt = ln.split("|", 1)
        out[lid.strip()] = txt.strip()
    return out

def load_script_lines(vdir, lang="tr"):
    """Ekranda/altyazıda gösterilecek yazılı hâl (rakamlı) SCRIPT.md'den."""
    name = "SCRIPT.md" if lang == "tr" else f"SCRIPT_{lang}.md"
    p = os.path.join(vdir, name)
    if not os.path.exists(p):
        return load_narration(vdir, lang)   # SCRIPT_<lang>.md yoksa NARRATION_<lang>.txt kullan
    return dict(re.findall(r"\*\*(L\d{3})\*\* (.+)", open(p, encoding="utf-8").read()))

def estimate_line(text, lang="tr"):
    rate = DEFAULT_RATE.get(lang, 5.0)
    t = 0.0
    for tok in re.findall(r"\S+", text):
        w = re.sub(r"[^\wçğıöşüâîûäß]", "", tok, flags=re.I) or tok
        t += syllables(w, lang) / rate
        if re.search(r"[,;:]$", tok): t += 0.12
        if re.search(r"[.!?…]$", tok): t += 0.18
    return round(t + LINE_PAUSE, 3)

def line_timings(vdir, lang="tr"):
    """{Lxxx: süre} + kaynak. Gerçek ses varsa audio/timing_<lang>.json kazanır."""
    tp = os.path.join(vdir, "audio", f"timing_{lang}_final.json")
    if not os.path.exists(tp):
        tp = os.path.join(vdir, "audio", f"timing_{lang}.json")
    if os.path.exists(tp):
        t = load_json(tp)
        return {k: float(v["dur"] if isinstance(v, dict) else v) for k, v in t["lines"].items()}, "audio"
    narr = load_narration(vdir, lang)
    return {k: estimate_line(v, lang) for k, v in narr.items()}, "estimate"

def scene_durations(scenes, timings):
    return {s["id"]: round(sum(timings.get(l, 0) for l in s["lines"]), 3) for s in scenes}

# ---------- görsel eşleştirme ----------
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
PAT = re.compile(r"(?:^|[_\-\s])(?:s|scene|sahne)[_\-\s]?0*(\d{1,3})(?:[_\-\s]?v(\d+)|[_\-\s]?(final))?", re.I)
PAT_T = re.compile(r"(?:^|[_\-\s])t0*(\d{1,2})(?:[_\-\s]?v(\d+)|[_\-\s]?(final))?", re.I)

def scan_images(vdir):
    """images/ altını tarar → {'S014': path, 'T01': path}. final > en yüksek vK > sürümsüz."""
    best = {}
    for p in glob.glob(os.path.join(vdir, "images", "**", "*"), recursive=True):
        if not p.lower().endswith(IMG_EXT):
            continue
        stem = os.path.splitext(os.path.basename(p))[0]
        m = PAT.search(stem); prefix = "S"
        if not m:
            m = PAT_T.search(stem); prefix = "T"
        if not m:
            continue
        sid = f"S{int(m.group(1)):03d}" if prefix == "S" else f"T{int(m.group(1)):02d}"
        rank = 10**6 if m.group(3) else int(m.group(2) or 0)
        if sid not in best or rank >= best[sid][0]:
            best[sid] = (rank, p)
    return {k: v[1] for k, v in best.items()}

def image_filename(video, sid, v=1):
    return f"{video}_{sid}_v{v}.png"
