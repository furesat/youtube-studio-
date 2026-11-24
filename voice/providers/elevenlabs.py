"""ElevenLabs sağlayıcısı (ücretli; henüz test edilmedi).
Anahtar YALNIZCA ortam değişkeninden okunur: ELEVENLABS_API_KEY (repoya asla yazılmaz).
voice_config.json örneği:
  "tr": {"provider": "elevenlabs", "voice": {"voice_id": "<id>", "model_id": "eleven_multilingual_v2",
         "stability": 0.45, "similarity_boost": 0.8, "style": 0.15}}
Kelime zamanları /with-timestamps uç noktasının karakter hizalamasından türetilir."""
import os, json, base64, urllib.request
from ..base import VoiceProvider, LineResult, Word

API = "https://api.elevenlabs.io/v1/text-to-speech/{vid}/with-timestamps?output_format=mp3_44100_128"

class ElevenLabsProvider(VoiceProvider):
    name = "elevenlabs"
    languages = ("tr", "de", "en")

    def available(self):
        return bool(os.environ.get("ELEVENLABS_API_KEY"))

    def synthesize(self, line, out_dir, voice):
        body = {"text": line.text, "model_id": voice.get("model_id", "eleven_multilingual_v2"),
                "language_code": line.lang,
                "voice_settings": {k: voice[k] for k in ("stability", "similarity_boost", "style") if k in voice}}
        req = urllib.request.Request(API.format(vid=voice["voice_id"]), data=json.dumps(body).encode(),
                                     headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"],
                                              "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            res = json.load(r)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"{line.id}.mp3")
        open(path, "wb").write(base64.b64decode(res["audio_base64"]))
        al = res.get("alignment") or {}
        chars, st, en = al.get("characters", []), al.get("character_start_times_seconds", []), al.get("character_end_times_seconds", [])
        words, cur, ws = [], "", None
        for c, a, b in zip(chars, st, en):
            if c.isspace():
                if cur: words.append(Word(cur, round(ws, 3), round(prev_end, 3))); cur = ""
                continue
            if not cur: ws = a
            cur += c; prev_end = b
        if cur: words.append(Word(cur, round(ws, 3), round(prev_end, 3)))
        dur = (en[-1] if en else 0.0) + line.pause_after
        return LineResult(line.id, path, round(dur, 3), words, "provider", self.name)
