"""timing_<lang>.json + PAUSES_<lang>.json + SCENES.json → timeline_<lang>.json
Montaj zaman haritası: her satırın (parça, kaynak başlangıç/bitiş, timeline başlangıcı) ve her sahnenin süresi.
Kullanım: python3 engine/tools/timeline_map.py videos/001 [--lang tr]"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import load_scenes, save_json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    T = json.load(open(f"{v}/audio/timing_{a.lang}.json"))["lines"]
    P = json.load(open(f"{v}/PAUSES_{a.lang}.json"))
    ids = sorted(T)
    t = 0.0; lines = {}
    for lid in ids:
        L = T[lid]
        lines[lid] = {"part": L["part"], "src_start": L["start"], "src_end": L["end"], "tl_start": round(t, 3)}
        t += L["dur"]
        t += P["after"].get(lid, P["default"])
        lines[lid]["tl_end"] = round(t, 3)
    data = load_scenes(v); out = []
    sc = data["scenes"]
    for i, s in enumerate(sc):
        st = lines[s["lines"][0]]["tl_start"]
        en = lines[sc[i + 1]["lines"][0]]["tl_start"] if i + 1 < len(sc) else round(t, 3)
        out.append({"id": s["id"], "title": s["title"], "kind": s["kind"], "start": st, "dur": round(en - st, 3)})
    save_json(f"{v}/timeline_{a.lang}.json", {"total_sec": round(t, 3), "lines": lines, "scenes": out})
    print("toplam", round(t, 2), "sn", f"({int(t//60)} dk {t%60:.0f} sn)", "sahne", len(out))
    print("en kısa/uzun sahne:", min(o['dur'] for o in out), max(o['dur'] for o in out))

if __name__ == "__main__":
    main()
