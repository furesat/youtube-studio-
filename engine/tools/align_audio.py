"""Bölüm sesleri (part_A/B/C.mp3) → satır zamanları (audio/timing_<lang>.json).
Yöntem: sessizlik tespiti → her konuşma parçasını Whisper (sherpa-onnx) ile yaz → kelimeleri
senaryo kelimeleriyle difflib ile eşle → satır başlangıç/bitişini bul. Ses içeriği değiştirilmez.
Kullanım: python3 engine/tools/align_audio.py videos/001 --parts A:L001-L019 B:L020-L041 C:L042-L075
Gerekli: ffmpeg, sherpa-onnx, Whisper modeli (WHISPER_DIR ortam değişkeni)."""
import os, sys, re, json, wave, argparse, subprocess, difflib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import load_narration, save_json

WD = os.environ.get("WHISPER_DIR", "/home/claude/w/models/sherpa-onnx-whisper-small/")

def norm(t):
    t = t.lower().replace("â", "a").replace("î", "i").replace("û", "u")
    return re.findall(r"[a-zçğıöşü0-9]+", t)

def silences(wav, db=-38, d=0.25):
    out = subprocess.run(["ffmpeg", "-i", wav, "-af", f"silencedetect=noise={db}dB:d={d}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(st, en))

def transcribe(wav, rec):
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    total = len(a) / sr; sil = silences(wav); segs = []; prev = 0.0
    for s, e in sil:
        if s - prev > 0.2: segs.append((prev, s))
        prev = e
    if total - prev > 0.2: segs.append((prev, total))
    # Whisper 30 sn'den uzun parçayı keser: uzun parçaları en sessiz noktadan böl
    def split(s, e):
        if e - s <= 24: return [(s, e)]
        lo, hi = int((s + 10) * sr), int((s + 22) * sr); w = int(0.05 * sr)
        best = min(range(lo, hi, w), key=lambda i: float(np.abs(a[i:i + w]).mean()))
        c = best / sr
        return [(s, c)] + split(c, e)
    segs = [x for s0, e0 in segs for x in split(s0, e0)]
    words = []
    for s, e in segs:
        st = rec.create_stream(); st.accept_waveform(sr, a[int(s * sr):int(e * sr)]); rec.decode_stream(st)
        ws = norm(st.result.text)
        for i, wd in enumerate(ws):   # parça içinde harf sayısına göre zaman dağıt
            words.append((wd, s, e, i, len(ws)))
    return words, segs, total, sil

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--parts", nargs="+", required=True)
    a = ap.parse_args(); vdir = a.vdir.rstrip("/")
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(encoder=WD + "small-encoder.int8.onnx", decoder=WD + "small-decoder.int8.onnx",
                                                     tokens=WD + "small-tokens.txt", language=a.lang, task="transcribe", num_threads=4)
    narr = load_narration(vdir, a.lang)
    timing = {"lines": {}, "parts": {}, "provider": "elevenlabs", "method": "whisper+difflib"}
    offset = 0.0
    for spec in a.parts:
        name, rng = spec.split(":"); l0, l1 = rng.split("-")
        mp3 = os.path.join(vdir, "audio", a.lang, f"part_{name}.mp3")
        wav = f"/tmp/align_{name}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", "16000", wav], check=True)
        words, segs, total, sil = transcribe(wav, rec)
        ids = [k for k in narr if l0 <= k <= l1]
        sw = []  # (word, line)
        for lid in ids:
            sw += [(w, lid) for w in norm(narr[lid])]
        sm = difflib.SequenceMatcher(a=[w for w, _ in sw], b=[w[0] for w in words], autojunk=False)
        first, last = {}, {}
        for blk in sm.get_matching_blocks():
            for k in range(blk.size):
                lid = sw[blk.a + k][1]; w = words[blk.b + k]
                t0 = w[1] + (w[2] - w[1]) * w[3] / w[4]; t1 = w[1] + (w[2] - w[1]) * (w[3] + 1) / w[4]
                first.setdefault(lid, t0); last[lid] = t1
        # satır sınırı: bir sonraki satırın ilk kelimesi (yoksa son kelime + boşluk)
        bounds = []
        for i, lid in enumerate(ids):
            st = first.get(lid, bounds[-1][1] if bounds else 0.0)
            bounds.append([lid, st])
        out = []
        for i, (lid, st) in enumerate(bounds):
            en = bounds[i + 1][1] if i + 1 < len(bounds) else total
            out.append((lid, st if i else 0.0, en))
        matched = sum(1 for lid in ids if lid in first)
        for lid, st, en in out:
            timing["lines"][lid] = {"part": name, "start": round(st, 3), "end": round(en, 3), "dur": round(en - st, 3),
                                    "speech_end": round(last.get(lid, en), 3), "abs_start": round(offset + st, 3)}
        timing["parts"][name] = {"file": os.path.relpath(mp3, vdir), "duration": round(total, 3), "lines": f"{l0}-{l1}",
                                 "matched_lines": f"{matched}/{len(ids)}", "match_ratio": round(sm.ratio(), 3)}
        offset += total
        print(name, round(total, 2), "sn", f"eşleşen satır {matched}/{len(ids)}", "oran", round(sm.ratio(), 3))
    timing["total_raw_sec"] = round(offset, 3)
    save_json(os.path.join(vdir, "audio", f"timing_{a.lang}.json"), timing)

if __name__ == "__main__":
    main()
