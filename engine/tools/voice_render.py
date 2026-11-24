"""NARRATION → ses dosyaları + audio/timing_<lang>.json (sahne süreleri buradan güncellenir).
Kullanım: python3 engine/tools/voice_render.py videos/001 --lang tr
Sağlayıcı voice_config.json'dan gelir; yoksa/kurulu değilse 'estimate'e düşer (yalnızca zamanlama).
Hazır kayıt kullanmak için: dosyaları audio/tr/L001.mp3 … diye koy ve provider'ı 'external' yap."""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT, load_json, save_json, load_narration
from voice.base import Line
from voice.registry import PROVIDERS, get_provider
try:
    from voice.providers.elevenlabs import ElevenLabsProvider
    PROVIDERS.setdefault("elevenlabs", ElevenLabsProvider)
except Exception:
    pass

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--only", nargs="*", help="L001 L002 … (yalnızca bu satırlar)")
    a = ap.parse_args(); vdir = a.vdir.rstrip("/")
    cfg = load_json(os.path.join(ROOT, "voice_config.json"))["languages"][a.lang]
    prov, why = get_provider(cfg["provider"], a.lang)
    if why: print("UYARI:", why, "→", prov.name)
    out_dir = os.path.join(vdir, "audio", a.lang)
    tp = os.path.join(vdir, "audio", f"timing_{a.lang}.json")
    timing = load_json(tp) if os.path.exists(tp) else {"lines": {}}
    for lid, txt in load_narration(vdir, a.lang).items():
        if a.only and lid not in a.only: continue
        r = prov.synthesize(Line(lid, txt, a.lang), out_dir, cfg.get("voice", {}))
        timing["lines"][lid] = {"dur": r.duration, "file": os.path.relpath(r.audio_path, vdir) if r.audio_path else None,
                                "words": [w.__dict__ for w in r.words]}
        print(lid, r.duration)
    timing["provider"] = prov.name
    if prov.name == "estimate":
        print("Tahmin modu: timing dosyası yazılmadı (gerçek ses değil).")
        return
    save_json(tp, timing)
    print("Yazıldı:", tp, "→ şimdi: prompts.py (süreler) + assemble.py")

if __name__ == "__main__":
    main()
