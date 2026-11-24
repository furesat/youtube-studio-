"""timeline_<lang>.json → FCPXML 1.9 (DaVinci Resolve: File > Import > Timeline).
Ses: 75 satır klipi (3 parça dosyasından, duraklamalar boşluk olarak). Sahneler: işaretçi (marker) + boşluk klibi.
Görseller varsa (images/NNN_Sxxx_*.png) sahne klibi olarak yerleştirilir.
Kullanım: python3 engine/tools/export_fcpxml.py videos/001 --audio-dir "/Users/.../youtube video" --out kahve_001.fcpxml"""
import os, sys, json, argparse, urllib.parse
from xml.sax.saxutils import escape, quoteattr
FPS = 30
def fr(sec): return f"{round(sec*FPS)}/{FPS}s"
def url(p): return "file://" + urllib.parse.quote(p)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--audio-dir", required=True)
    ap.add_argument("--files", default="A=New tts node-7.mp3,B=New tts node-8.mp3,C=New tts node-9.mp3")
    ap.add_argument("--out", default="timeline.fcpxml")
    a = ap.parse_args(); v = a.vdir.rstrip("/")
    T = json.load(open(f"{v}/timeline_{a.lang}.json")); tim = json.load(open(f"{v}/audio/timing_{a.lang}.json"))
    files = dict(x.split("=", 1) for x in a.files.split(","))
    total = T["total_sec"]; tot_f = fr(total)
    o = ['<?xml version="1.0" encoding="UTF-8"?>', '<!DOCTYPE fcpxml>', '<fcpxml version="1.9">', '<resources>',
         '<format id="r1" name="FFVideoFormat1080p30" frameDuration="1/30s" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>']
    for k, fn in files.items():
        d = tim["parts"][k]["duration"]
        o.append(f'<asset id="a{k}" name={quoteattr(fn)} start="0s" duration="{fr(d)}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="44100">'
                 f'<media-rep kind="original-media" src={quoteattr(url(os.path.join(a.audio_dir, fn)))}/></asset>')
    o += ['</resources>', '<library>', '<event name="Kahve 001">', f'<project name="Kahve 001 {a.lang.upper()}">',
          f'<sequence format="r1" duration="{tot_f}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">', '<spine>']
    sc = T["scenes"]
    for i, s in enumerate(sc):
        o.append(f'<gap name={quoteattr(s["id"] + " " + s["title"])} offset="{fr(s["start"])}" start="3600s" duration="{fr(s["dur"])}">')
        o.append(f'<marker start="3600s" duration="1/30s" value={quoteattr(s["id"] + " " + s["title"])}/>')
        if i == 0:   # ses klipleri ilk gap'e bağlı, offset = gap içi zaman (start=3600s tabanı)
            for lid, L in sorted(T["lines"].items()):
                d = L["src_end"] - L["src_start"]
                o.append(f'<asset-clip ref="a{L["part"]}" lane="-1" offset="{fr(3600 + L["tl_start"])}" name={quoteattr(lid)} '
                         f'start="{fr(L["src_start"])}" duration="{fr(d)}" audioRole="dialogue"/>')
        o.append('</gap>')
    o += ['</spine>', '</sequence>', '</project>', '</event>', '</library>', '</fcpxml>']
    open(a.out, "w", encoding="utf-8").write("\n".join(o)); print("yazıldı", a.out, round(total, 1), "sn")
if __name__ == "__main__": main()
