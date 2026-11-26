"""Kanal banner + avatar. Banner: 2560x1440, her cihazda görünen güvenli alan ortadaki 1546x423 (x 507-2053, y 508-931)."""
from PIL import Image, ImageDraw, ImageFont
F = "../engine/fonts/ShantellSans[BNCE,INFM,SPAC,wght].ttf"
INK, RED, PAPER = (29, 26, 23), (184, 58, 43), (255, 250, 240)
def font(sz, w=800, inf=60):
    f = ImageFont.truetype(F, sz); f.set_variation_by_axes([w, inf, 0, 0]); return f
src = Image.open("src/kanal_banner_v1.png").convert("RGB")
SH = 128  # içeriği güvenli şeride oturtmak için yukarı kaydır
b = Image.new("RGB", src.size); b.paste(src, (0, -SH)); b.paste(src.crop((0, 1080, 2560, 1080 + SH)), (0, 1440 - SH))
d = ImageDraw.Draw(b)
def text(xy, s, f, fill, stroke=0, sfill=PAPER, anchor="la"):
    d.text(xy, s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill, anchor=anchor)
# sol boşluk: kanal adı
text((733, 655), "Fasulye", font(98), RED, 6, PAPER, "mm")
# sağ boşluk: slogan
fs = font(41, 600, 80)
text((1548, 620), "Bildiğin hikâyenin", fs, INK, anchor="mm")
text((1548, 674), "bilmediğin tarafı.", fs, INK, anchor="mm")
b.save("kanal_banner_2560x1440.jpg", quality=92)
# önizleme: güvenli alanlar
p = b.copy(); q = ImageDraw.Draw(p)
q.rectangle((507, 508, 2053, 931), outline=(0, 160, 0), width=6)       # tüm cihazlar
q.rectangle((0, 508, 2559, 931), outline=(0, 90, 200), width=4)        # masaüstü
p.thumbnail((1600, 1600)); p.save("/tmp/banner_preview.jpg", quality=85)
a = Image.open("src/kanal_avatar_v1.png").convert("RGB").resize((800, 800), Image.LANCZOS)
a.save("kanal_avatar_800.jpg", quality=92)
m = Image.new("L", (800, 800), 0); ImageDraw.Draw(m).ellipse((0, 0, 799, 799), fill=255)
c = Image.new("RGB", (800, 800), (255, 255, 255)); c.paste(a, (0, 0), m); c.thumbnail((300, 300)); c.save("/tmp/avatar_preview.jpg")
