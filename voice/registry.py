from .providers.estimate import EstimateProvider
from .providers.external import ExternalFileProvider
from .providers.local_models import ChatterboxProvider, PiperProvider, KokoroProvider
PROVIDERS = {p.name: p for p in (EstimateProvider, ExternalFileProvider, ChatterboxProvider, PiperProvider, KokoroProvider)}

def get_provider(name, lang="tr", fallback="estimate"):
    """İstenen sağlayıcı yoksa / dili desteklemiyorsa üretimi durdurmadan fallback'e düşer."""
    cls = PROVIDERS.get(name)
    if cls:
        p = cls()
        if lang in p.languages and p.available(): return p, None
        why = f"{name}: dil '{lang}' desteklenmiyor" if lang not in p.languages else f"{name}: kurulu değil"
    else:
        why = f"{name}: bilinmeyen sağlayıcı"
    return PROVIDERS[fallback](), why
