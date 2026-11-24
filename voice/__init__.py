"""voice - sağlayıcıdan bağımsız seslendirme katmanı.
Üretim hattı yalnızca VoiceProvider arayüzünü bilir; sağlayıcı config ile seçilir."""
from .base import VoiceProvider, Line, LineResult, Word
from .registry import get_provider, PROVIDERS
