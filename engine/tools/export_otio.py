"""timing_<lang>_final.json + SCENES.json + images → .otio (Kdenlive: File > OpenTimelineIO Import).
V1: sahne görselleri, A1: 75 satır ses klibi (duraklamalar boşluk), sahne işaretçileri.
Kullanım: python3 engine/tools/export_otio.py videos/001 --audio-dir DIR --image-dir DIR --out x.otio"""
import os, sys, json, argparse
import opentimelineio as otio
sys.path.insert(0, os.path.dirname(__file__))
from common import load_scenes
FPS = 30
def rt(sec): return otio.opentime.RationalTime(round(sec * FPS), FPS)
def rng(a, d): return otio.opentime.TimeRange(rt(a), rt(d))
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--audio-dir", required=True); ap.add_argument("--image-dir", required=True)
    ap.add_argument("--files", default="A=New tts node-7.mp3,B=New tts node-8.mp3,C=New tts node-9.mp3")
    ap.add_argument("--out", default="timeline.otio"); a = ap.parse_args(); v = a.vdir.rstrip("/")
    F = json.load(open(f"{v}/audio/timing_{a.lang}_final.json"))["lines"]; raw = json.load(open(f"{v}/audio/timing_{a.lang}.json"))
    files = dict(x.split("=", 1) for x in a.files.split(",")); scenes = load_scenes(v)["scenes"]
    pos = {}; t = 0.0
    for lid in sorted(F): pos[lid] = t; t += F[lid]["dur"]
    total = t
    tl = otio.schema.Timeline(name="Kahve 001 TR"); tl.global_start_time = rt(0)
    vt = otio.schema.Track(name="Görseller", kind=otio.schema.TrackKind.Video)
    at = otio.schema.Track(name="Ses", kind=otio.schema.TrackKind.Audio)
    for i, s in enumerate(scenes):
        st = pos[s["lines"][0]]; en = pos[scenes[i + 1]["lines"][0]] if i + 1 < len(scenes) else total
        sid = s.get("source") or s["id"]; fn = f"001_{sid}_v1.jpg"
        ref = otio.schema.ExternalReference(target_url="file://" + os.path.join(a.image_dir, fn), available_range=rng(0, en - st))
        c = otio.schema.Clip(name=f'{s["id"]} {s["title"]}', media_reference=ref, source_range=rng(0, en - st))
        c.markers.append(otio.schema.Marker(name=s["id"], marked_range=rng(0, 1 / FPS), color=otio.schema.MarkerColor.RED))
        vt.append(c)
    cur = 0.0
    for lid in sorted(F):
        L = F[lid]; start = pos[lid]
        if start - cur > 1e-3: at.append(otio.schema.Gap(source_range=rng(0, start - cur)))
        ref = otio.schema.ExternalReference(target_url="file://" + os.path.join(a.audio_dir, files[L["part"]]),
                                            available_range=rng(0, raw["parts"][L["part"]]["duration"]))
        at.append(otio.schema.Clip(name=lid, media_reference=ref, source_range=rng(L["start"], L["speech"])))
        cur = start + L["speech"]
    tl.tracks.append(vt); tl.tracks.append(at)
    otio.adapters.write_to_file(tl, a.out); print("yazıldı", a.out, round(total, 1), "sn")
if __name__ == "__main__": main()
