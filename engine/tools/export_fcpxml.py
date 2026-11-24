"""timing_<lang>_final.json + SCENES.json + images → FCPXML 1.9 (DaVinci Resolve: File > Import > Timeline).
Her sahne bir görsel klip (+ sahne işaretçisi), her satır bir ses klibi (duraklamalar boşluk).
Kullanım: python3 engine/tools/export_fcpxml.py videos/001 --audio-dir DIR --image-dir DIR --out x.fcpxml"""
import os, sys, json, argparse, urllib.parse
from xml.sax.saxutils import quoteattr
sys.path.insert(0, os.path.dirname(__file__))
from common import load_scenes
FPS = 30
def fr(sec): return f"{round(sec*FPS)}/{FPS}s"
def url(p): return "file://" + urllib.parse.quote(p)
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("vdir"); ap.add_argument("--lang", default="tr")
    ap.add_argument("--audio-dir", required=True); ap.add_argument("--image-dir", required=True)
    ap.add_argument("--files", default="A=New tts node-7.mp3,B=New tts node-8.mp3,C=New tts node-9.mp3")
    ap.add_argument("--out", default="timeline.fcpxml"); a = ap.parse_args(); v = a.vdir.rstrip("/")
    F = json.load(open(f"{v}/audio/timing_{a.lang}_final.json")); raw = json.load(open(f"{v}/audio/timing_{a.lang}.json"))
    files = dict(x.split("=", 1) for x in a.files.split(",")); scenes = load_scenes(v)["scenes"]
    pos = {}; t = 0.0
    for lid in sorted(F["lines"]): pos[lid] = t; t += F["lines"][lid]["dur"]
    total = t
    imgs = {}
    for s in scenes:
        sid = s.get("source") or s["id"]; fn = f"001_{sid}_v1.jpg"
        if os.path.exists(f"{v}/images/{fn}"): imgs[s["id"]] = fn
    o = ['<?xml version="1.0" encoding="UTF-8"?>', '<!DOCTYPE fcpxml>', '<fcpxml version="1.9">', '<resources>',
         '<format id="r1" name="FFVideoFormat1080p30" frameDuration="1/30s" width="1920" height="1080" colorSpace="1-1-1 (Rec. 709)"/>']
    for k, fn in files.items():
        o.append(f'<asset id="a{k}" name={quoteattr(fn)} start="0s" duration="{fr(raw["parts"][k]["duration"])}" hasAudio="1" audioSources="1" audioChannels="2" audioRate="44100">'
                 f'<media-rep kind="original-media" src={quoteattr(url(os.path.join(a.audio_dir, fn)))}/></asset>')
    for sid, fn in sorted(set((fn, fn) for fn in imgs.values())):
        o.append(f'<asset id="i_{fn[:-4]}" name={quoteattr(fn)} start="0s" duration="0s" hasVideo="1" format="r1">'
                 f'<media-rep kind="original-media" src={quoteattr(url(os.path.join(a.image_dir, fn)))}/></asset>')
    o += ['</resources>', '<library>', '<event name="Kahve 001">', f'<project name="Kahve 001 {a.lang.upper()} görselli">',
          f'<sequence format="r1" duration="{fr(total)}" tcStart="0s" tcFormat="NDF" audioLayout="stereo" audioRate="48k">', '<spine>']
    for i, s in enumerate(scenes):
        st = pos[s["lines"][0]]; en = pos[scenes[i + 1]["lines"][0]] if i + 1 < len(scenes) else total
        name = quoteattr(f'{s["id"]} {s["title"]}')
        if s["id"] in imgs:
            o.append(f'<video ref="i_{imgs[s["id"]][:-4]}" name={name} offset="{fr(st)}" start="0s" duration="{fr(en-st)}">')
        else:
            o.append(f'<gap name={name} offset="{fr(st)}" start="0s" duration="{fr(en-st)}">')
        o.append(f'<marker start="0s" duration="1/30s" value={name}/>')
        for lid in s["lines"]:
            L = F["lines"][lid]
            o.append(f'<asset-clip ref="a{L["part"]}" lane="-1" offset="{fr(pos[lid]-st)}" name={quoteattr(lid)} start="{fr(L["start"])}" duration="{fr(L["speech"])}" audioRole="dialogue"/>')
        o.append('</video>' if s["id"] in imgs else '</gap>')
    o += ['</spine>', '</sequence>', '</project>', '</event>', '</library>', '</fcpxml>']
    open(a.out, "w", encoding="utf-8").write("\n".join(o)); print("yazıldı", a.out, round(total, 1), "sn;", len(imgs), "görsel klip")
if __name__ == "__main__": main()
