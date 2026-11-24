"""Yerel model adaptörleri — İSKELET. Kütüphane yalnızca seçilince (lazy) içe aktarılır,
yüklü değilse available() False döner; üretim hattı bu durumda 'estimate'e düşer.
Bu oturumda HİÇBİRİ çalıştırılıp test edilmedi."""
from ..base import VoiceProvider, LineResult

class _Lazy(VoiceProvider):
    module = ""
    def available(self):
        try: __import__(self.module); return True
        except Exception: return False

class ChatterboxProvider(_Lazy):
    """Chatterbox Multilingual (MIT) — tr/de/en destekli. Ses klonlama için izinli referans ses gerekir."""
    name = "chatterbox"; module = "chatterbox"
    def synthesize(self, line, out_dir, voice):
        raise NotImplementedError("Ses testi aşamasında doldurulacak (chatterbox.mtl_tts).")

class PiperProvider(_Lazy):
    """Piper (ONNX). DİKKAT: tr_TR-dfki sesi CC BY-NC-SA verili -> ticari kullanma."""
    name = "piper"; module = "piper"
    def synthesize(self, line, out_dir, voice):
        raise NotImplementedError("Ses testi aşamasında doldurulacak.")

class KokoroProvider(_Lazy):
    """Kokoro-82M (Apache-2.0) — Türkçe ve Almanca YOK; yalnızca EN sürüm için aday."""
    name = "kokoro"; module = "kokoro"; languages = ("en",)
    def synthesize(self, line, out_dir, voice):
        raise NotImplementedError("Ses testi aşamasında doldurulacak.")
