from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional, List

@dataclass
class Line:
    """Senaryonun tek cümlesi. id sahne planına bağlanır."""
    id: str
    text: str
    lang: str = "tr"            # "tr" | "de" | "en"
    style: str = "neutral"      # neutral | emphasis | tension | warm | joke
    pause_after: float = 0.18   # sn, cümle sonrası nefes

@dataclass
class Word:
    w: str
    start: float
    end: float

@dataclass
class LineResult:
    id: str
    audio_path: Optional[str]   # None = ses yok (yalnızca zamanlama)
    duration: float
    words: List[Word] = field(default_factory=list)
    timing_source: str = "estimated"   # estimated | provider | forced_alignment
    provider: str = ""
    def to_dict(self): return asdict(self)

class VoiceProvider:
    """Tüm sağlayıcıların uyduğu sözleşme.
    synthesize() bir LineResult döndürmek zorunda; kelime zamanları yoksa boş liste döner,
    sonradan hizalama (align) adımı doldurur."""
    name = "base"
    languages = ("tr", "de", "en")
    def available(self) -> bool: return True
    def synthesize(self, line: Line, out_dir: str, voice: dict) -> LineResult:
        raise NotImplementedError
