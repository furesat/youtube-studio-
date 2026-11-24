"""Ses üretmeden süre ve kelime zamanı tahmini. Hiçbir dış bağımlılık yok.
Amaç: ses sağlayıcısı seçilmeden storyboard/animatik zamanlamasını yapabilmek.
Dil başına hece hızı (hece/sn) ayarlanabilir; gerçek ses gelince ölçüp kalibre edilir."""
import re, wave, os, struct
from ..base import VoiceProvider, LineResult, Word

VOWELS = {"tr": "aeıioöuüâîû", "de": "aeiouäöüy", "en": "aeiouy"}
DEFAULT_RATE = {"tr": 5.6, "de": 5.0, "en": 4.6}   # hece/sn — başlangıç varsayımı, ölçülmedi
STYLE_K = {"neutral": 1.0, "emphasis": 0.92, "tension": 0.95, "warm": 0.9, "joke": 1.05}

def syllables(word, lang):
    v = VOWELS.get(lang, VOWELS["en"]); w = word.lower()
    if lang == "tr":   # Türkçede hece sayısı = ünlü sayısı
        n = sum(1 for ch in w if ch in v)
    else:              # DE/EN: ardışık ünlü grupları
        n = len(re.findall(f"[{v}]+", w))
        if lang == "en" and w.endswith("e") and n > 1: n -= 1
    digits = re.findall(r"\d", w)
    if digits: n = max(n, len(digits) * 2)        # sayılar okunurken uzar
    return max(1, n)

class EstimateProvider(VoiceProvider):
    name = "estimate"
    def synthesize(self, line, out_dir, voice):
        rate = voice.get("rate_sps", {}).get(line.lang, DEFAULT_RATE.get(line.lang, 5.0))
        rate *= STYLE_K.get(line.style, 1.0)
        toks = re.findall(r"\S+", line.text)
        t = 0.0; words = []
        for tok in toks:
            d = syllables(re.sub(r"[^\wçğıöşüâîûäß]", "", tok, flags=re.I) or tok, line.lang) / rate
            if re.search(r"[,;:]$", tok): d += 0.12          # virgül duraksaması
            words.append(Word(tok, round(t, 3), round(t + d, 3))); t += d
        dur = round(t + line.pause_after, 3)
        path = None
        if voice.get("write_silence", False):
            os.makedirs(out_dir, exist_ok=True); path = os.path.join(out_dir, f"{line.id}.wav")
            sr = 24000; n = int(dur * sr)
            with wave.open(path, "wb") as f:
                f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(b"\x00\x00" * n)
        return LineResult(line.id, path, dur, words, "estimated", self.name)
