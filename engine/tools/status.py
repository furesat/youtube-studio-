"""images/ ve audio/ klasörlerini tarar, STATUS.json'u günceller.
Kullanım: python3 engine/tools/status.py videos/001"""
import os, sys, glob, datetime
sys.path.insert(0, os.path.dirname(__file__))
from common import load_scenes, load_json, save_json, scan_images, line_timings

def main():
    vdir = sys.argv[1].rstrip("/")
    data = load_scenes(vdir); vid = data["video"]
    sp = os.path.join(vdir, "STATUS.json")
    st = load_json(sp) if os.path.exists(sp) else {}
    found = scan_images(vdir)
    need = [s["id"] for s in data["scenes"] if s["kind"] == "imagegen"]
    have = [i for i in need if i in found]
    missing = [i for i in need if i not in found]
    # türev sahneler kaynakları gelince tamam sayılır
    done = []
    for s in data["scenes"]:
        k = s["kind"]
        if (k == "imagegen" and s["id"] in found) or (k == "derived" and s["source"] in found) or k == "engine_card":
            done.append(s["id"])
    timings, src = line_timings(vdir, "tr")
    audio_files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(vdir, "audio", "*")) if not p.endswith(".gitkeep"))
    st.update({
        "video": vid,
        "title": data["title"]["tr"],
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "images": {"needed": len(need), "found": len(have), "missing": missing,
                   "files": {k: os.path.relpath(v, vdir) for k, v in sorted(found.items())},
                   "thumbnail": "T01" in found},
        "scenes": {"total": len(data["scenes"]), "complete": len(done),
                   "incomplete": [s["id"] for s in data["scenes"] if s["id"] not in done]},
        "voice": {**st.get("voice", {}), "timing_source": src, "audio_files": len(audio_files),
                  "total_sec": round(sum(timings.values()), 1)},
    })
    st.setdefault("stages", {})
    st["stages"]["images"] = "done" if not missing else ("in_progress" if have else "waiting")
    save_json(sp, st)
    print(f"Görseller {len(have)}/{len(need)} · eksik: {', '.join(missing[:12])}{' …' if len(missing) > 12 else ''}")
    print(f"Sahneler {len(done)}/{len(data['scenes'])} hazır · zamanlama: {src} ({st['voice']['total_sec']} sn)")

if __name__ == "__main__":
    main()
