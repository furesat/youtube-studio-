"""Kullanım: python -m voice script.json voice_config.json çıktı_klasörü
script.json: {"lang":"tr","lines":[{"id":"L001","text":"...","style":"neutral"}]}"""
import sys, json, os
from .base import Line
from .registry import get_provider

def main(script, cfg, out):
    S = json.load(open(script, encoding="utf-8")); C = json.load(open(cfg, encoding="utf-8"))
    lang = S.get("lang", "tr"); vc = C["languages"].get(lang, {})
    prov, warn = get_provider(vc.get("provider", "estimate"), lang)
    if warn: print("UYARI:", warn, "-> 'estimate' kullanılıyor", file=sys.stderr)
    t = 0.0; res = []
    for L in S["lines"]:
        r = prov.synthesize(Line(lang=lang, **L), os.path.join(out, "audio"), vc.get("voice", {}))
        d = r.to_dict(); d["t0"] = round(t, 3); d["t1"] = round(t + r.duration, 3); t += r.duration
        res.append(d)
    os.makedirs(out, exist_ok=True)
    json.dump({"lang": lang, "provider": prov.name, "total_s": round(t, 3), "lines": res}, open(os.path.join(out, "timing.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{prov.name}: {len(res)} cümle, {t:.1f} sn -> {out}/timing.json")

if __name__ == "__main__": main(*sys.argv[1:4])
