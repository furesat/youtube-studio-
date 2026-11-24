"""Düzenleme yazılımları için zaman çizelgesi: OTIO (+ FCP7 XML; DaVinci Resolve / Premiere içe aktarır).
Üç video izi: V1 görsel katman, V2 metin katmanı (dil), V3 yok. Ses izi boş (ses sağlayıcısı sonra)."""
import json, os, sys
import opentimelineio as otio
HERE = os.path.dirname(os.path.abspath(__file__)); FPS = 30
# Medya kökü: varsayılan teslim klasörü (Mac). Başka yere taşıdıysan: python3 export_timeline.py /yeni/yol/pilot
BASE = sys.argv[1] if len(sys.argv) > 1 else "/Users/furkanyonat/Downloads/youtube video/pilot"
from urllib.parse import quote
plan = json.load(open(os.path.join(HERE, "scene_plan.json"), encoding="utf-8"))
for lang, L in plan["languages"].items():
    tl = otio.schema.Timeline(name=f"pilot_{lang}"); tl.global_start_time = otio.opentime.RationalTime(0, FPS)
    v1 = otio.schema.Track(name="V1_gorsel", kind=otio.schema.TrackKind.Video)
    v2 = otio.schema.Track(name=f"V2_metin_{lang}", kind=otio.schema.TrackKind.Video)
    frames_total = 0
    for s in L["shots"]:
        n = round((s["t0"] + s["dur"]) * FPS) - frames_total; frames_total += n
        rng = otio.opentime.TimeRange(otio.opentime.RationalTime(0, FPS), otio.opentime.RationalTime(n, FPS))
        for tr, rel in ((v1, f"layers/art/{s['id']}.png"), (v2, f"layers/text_{lang}/{s['id']}_txt.png")):
            ref = otio.schema.ExternalReference(target_url="file://" + quote(os.path.join(BASE, rel)), available_range=rng)
            tr.append(otio.schema.Clip(name=s["id"], media_reference=ref, source_range=rng))
    tl.tracks.extend([v1, v2])
    tl.tracks.append(otio.schema.Track(name="A1_ses_bos", kind=otio.schema.TrackKind.Audio))
    os.makedirs(os.path.join(HERE, "timeline"), exist_ok=True)
    otio.adapters.write_to_file(tl, os.path.join(HERE, "timeline", f"pilot_{lang}.otio"))
    try:
        otio.adapters.write_to_file(tl, os.path.join(HERE, "timeline", f"pilot_{lang}_fcp7.xml"), adapter_name="fcp_xml")
        print(lang, "otio + fcp7 xml ok,", frames_total, "kare")
    except Exception as e:
        print(lang, "fcp xml yazılamadı:", e)
