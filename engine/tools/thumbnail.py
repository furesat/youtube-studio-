"""Kapak görseline başlık yazısı ekler. Kullanım: python3 engine/tools/thumbnail.py videos/001 "YASAK!" """
import sys
from PIL import Image, ImageDraw, ImageFont
v, txt = sys.argv[1].rstrip("/"), sys.argv[2]
im = Image.open(f"{v}/images/001_T01_v1.png").convert("RGBA").resize((1280, 720), Image.LANCZOS)
f = ImageFont.truetype("engine/fonts/ShantellSans[BNCE,INFM,SPAC,wght].ttf", 220)
f.set_variation_by_axes([800, 60, 0, 0])  # ağırlık, gayriresmîlik, zıplama, aralık
L = Image.new("RGBA", (1400, 500), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
bb = d.textbbox((0, 0), txt, font=f, stroke_width=16); w, h = bb[2] - bb[0], bb[3] - bb[1]
d.text((40 - bb[0] + 9, 40 - bb[1] + 11), txt, font=f, fill=(29, 26, 23, 140), stroke_width=16, stroke_fill=(29, 26, 23, 140))
d.text((40 - bb[0], 40 - bb[1]), txt, font=f, fill=(184, 58, 43, 255), stroke_width=16, stroke_fill=(255, 250, 240, 255))
L = L.crop((0, 0, w + 100, h + 100)).rotate(6, expand=True, resample=Image.BICUBIC)
s = 520 / L.width; L = L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
im.alpha_composite(L, (1262 - L.width, 70))
im = im.convert("RGB"); im.save(f"{v}/renders/thumbnail_tr.png"); im.save(f"{v}/renders/thumbnail_tr.jpg", quality=92)
print(L.size)
