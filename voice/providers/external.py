"""Hazır ses dosyası sağlayıcısı: insan kaydı veya herhangi bir araçta üretilmiş wav/mp3.
Dosya adı = line.id. Süreyi dosyadan okur (wav: standart kütüphane; diğer biçimler: ffprobe varsa)."""
import os, wave, subprocess, json
from ..base import VoiceProvider, LineResult

class ExternalFileProvider(VoiceProvider):
    name = "external"
    def synthesize(self, line, out_dir, voice):
        src = voice.get("dir", "recordings")
        for ext in (".wav", ".mp3", ".m4a", ".flac"):
            p = os.path.join(src, line.id + ext)
            if os.path.exists(p):
                if ext == ".wav":
                    with wave.open(p) as f: d = f.getnframes() / f.getframerate()
                else:
                    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", p], capture_output=True, text=True)
                    d = float(json.loads(r.stdout)["format"]["duration"])
                return LineResult(line.id, p, round(d, 3), [], "provider", self.name)
        raise FileNotFoundError(f"{line.id}: kayıt bulunamadı ({src})")
