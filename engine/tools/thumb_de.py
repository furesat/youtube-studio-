"""DE kapak: python3 engine/tools/thumb_de.py <görsel> <çıktı> <stil>  (stil: bar | plain | two)"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F = "engine/fonts/ShantellSans[BNCE,INFM,SPAC,wght].ttf"
RED, CREAM, INK, GOLD = (214, 52, 38, 255), (255, 246, 226, 255), (18, 14, 12, 255), (247, 196, 72, 255)
def word(s, size, fill, stroke, sw, rot=0, shadow=True):
    f = ImageFont.truetype(F, size); f.set_variation_by_axes([800, 70, 0, 0])
    L = Image.new("RGBA", (2400, 700), (0, 0, 0, 0)); d = ImageDraw.Draw(L); bb = d.textbbox((0, 0), s, font=f, stroke_width=sw)
    if shadow: d.text((80 - bb[0] + 12, 80 - bb[1] + 14), s, font=f, fill=(0, 0, 0, 210), stroke_width=sw, stroke_fill=(0, 0, 0, 210))
    d.text((80 - bb[0], 80 - bb[1]), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    L = L.crop(L.getbbox()); return L.rotate(rot, expand=True, resample=Image.BICUBIC)
def fit(L, w): s = w / L.width; return L.resize((int(L.width * s), int(L.height * s)), Image.LANCZOS)
def bar(txt, w, col, tcol, rot):
    t = fit(word(txt, 230, tcol, INK, 14, 0, False), w)
    b = Image.new("RGBA", (t.width + 60, t.height + 44), (0, 0, 0, 0)); ImageDraw.Draw(b).rounded_rectangle((0, 0, b.width - 1, b.height - 1), 18, fill=col, outline=INK, width=8)
    b.alpha_composite(t, (30, 22)); b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", b.size, (0, 0, 0, 0)); sh.putalpha(b.getchannel("A").point(lambda p: int(p * .75))); return b, sh.filter(ImageFilter.GaussianBlur(7))
src, out, style = sys.argv[1:4]
im = Image.open(src).convert("RGBA").resize((1280, 720), Image.LANCZOS)
if style == "bar":
    b, sh = bar("VERBOTEN!", 560, RED, CREAM, 6); im.alpha_composite(sh, (34, 262)); im.alpha_composite(b, (22, 246))
    y = fit(word("1781", 140, GOLD, INK, 12, 6), 230); im.alpha_composite(y, (60, 110))
elif style == "plain":
    t = fit(word("VERBOTEN!", 230, CREAM, INK, 16, 6), 590); im.alpha_composite(t, (14, 250))
    y = fit(word("1781", 140, GOLD, INK, 12, 6), 220); im.alpha_composite(y, (60, 110))
elif style == "two":
    a = fit(word("KAFFEE", 230, CREAM, INK, 16, 5), 450); im.alpha_composite(a, (40, 140))
    b, sh = bar("VERBOTEN!", 520, RED, CREAM, 5); im.alpha_composite(sh, (34, 352)); im.alpha_composite(b, (22, 336))
im = im.convert("RGB"); im.save(out, quality=93)
