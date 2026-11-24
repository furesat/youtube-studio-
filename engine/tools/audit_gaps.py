"""Seste cümle ORTASINDAKİ bekleme boşluklarını bulur (yazıda nokta/?/!/… ile bitmeyen yerlerde).
Kullanım: python3 engine/tools/audit_gaps.py videos/001 [--min 0.3]"""
import os, sys, re, json, wave, argparse, subprocess, difflib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import load_narration
from align_audio import norm, silences, transcribe, WD

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr"); ap.add_argument("--min", type=float, default=0.3)
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=WD + "small-encoder.int8.onnx", decoder=WD + "small-decoder.int8.onnx", tokens=WD + "small-tokens.txt", language=a.lang, task="transcribe", num_threads=4)
    T = json.load(open(f"{v}/audio/timing_{a.lang}.json")); narr = load_narration(v, a.lang); out = []
    for k, info in T["parts"].items():
        wav = f"/tmp/ag_{k}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{v}/audio/{a.lang}/part_{k}.mp3", "-ac", "1", "-ar", "16000", wav], check=True)
        words, segs, total, sil = transcribe(wav, rec)
        ids = [l for l, x in T["lines"].items() if x["part"] == k]
        # satır sınırları (başlangıç saniyeleri)
        starts = sorted((T["lines"][l]["start"], l) for l in ids)
        for (s, e) in sil:
            if e - s < a.min or s < 0.05 or e > total - 0.05: continue
            line = [l for st, l in starts if st <= s + 0.01][-1]
            at_boundary = any(abs(st - ((s + e) / 2)) < 0.6 for st, _ in starts)
            # önce/sonra kelimeler
            prev = [w[0] for w in words if w[2] <= s + 0.05][-3:]; nxt = [w[0] for w in words if w[1] >= e - 0.05][:3]
            txt = narr.get(line, "")
            out.append({"part": k, "at": round(s, 2), "dur": round(e - s, 2), "line": line, "boundary": at_boundary, "prev": " ".join(prev), "next": " ".join(nxt), "line_text": txt})
    json.dump(out, open(f"{v}/audio/gaps_{a.lang}.json", "w"), ensure_ascii=False, indent=1)
    for o in out:
        if not o["boundary"]:
            print(f'{o["part"]} {o["at"]:7.2f}s {o["dur"]:.2f}s {o["line"]}  …{o["prev"]} | {o["next"]}…')
if __name__ == "__main__": main()
