"""compose.py - her yön için aynı 5 test sahnesini üretir (adil karşılaştırma)."""
import os, json
from scenes import Scene, W, H
from chars import Fasulye, Gozluk, Topak
from palettes import ALL
from render import render

CH = {"A": Fasulye, "B": Gozluk, "C": Topak}
SC = {"A": 1.25, "B": 1.08, "C": 1.32}       # sahne içi karakter ölçeği (boyları eşitlemek için)
HIP = {"A": 92, "B": 152, "C": 62}            # oturma yerleşimi için kalça yüksekliği
HAND_R_SIT = {"A": (86, -111), "B": (54, -217), "C": (73, -99)}
TXT = {
 "tr": dict(card="AMA ASIL SORUN BAŞKAYDI", now="BUGÜN", then="11.600 YIL ÖNCE", same="AYNI MERAK", avg="ORTALAMA?", yrs="YAŞ"),
 "de": dict(card="ABER DAS EIGENTLICHE PROBLEM", now="HEUTE", then="VOR 11.600 JAHREN", same="GLEICHE NEUGIER", avg="DURCHSCHNITT?", yrs="JAHRE"),
 "en": dict(card="BUT THE REAL PROBLEM", now="TODAY", then="11,600 YEARS AGO", same="SAME CURIOSITY", avg="AVERAGE?", yrs="YEARS"),
}

def ch(d): return CH[d](ALL[d])

def outdoor(d):
    P = ALL[d]; S = Scene(P, d, 31); c = ch(d); s = SC[d]
    o = S.defs() + S.sky(P["sky"], P["sky2"], 560) + S.sun(1600, 150, 60)
    o += S.hills(430, P["hill"], 70, 0.3) + S.hills(510, P["ground2"], 40, 2.0)
    o += S.ground(560, P["ground"], P["ground2"])
    o += S.pillar(1480, 690, 1.0) + S.pillar(1760, 650, 0.78) + S.pillar(140, 640, 0.7, carve=False)
    o += S.hut(420, 680, 1.15)
    o += S.fire(1010, 975, 1.1)
    o += c.g(620, 1040, s, pose="göster", expr="mutlu", costume="tarih_öncesi", seed=4)
    o += c.g(1400, 1050, s*0.97, pose="omuz", expr="şaşkın", costume="tarih_öncesi", flip=True, seed=8)
    o += c.g(1720, 1055, s*0.6, pose="koş", expr="mutlu", costume="tarih_öncesi", flip=True, seed=12)
    return o + S.grain()

def room(d):
    P = ALL[d]; S = Scene(P, d, 41); c = ch(d); s = SC[d]
    o = S.defs() + f'<rect width="{W}" height="{H}" fill="{P["wall"]}"/>'
    o += S.fill([(-20, 800), (W+20, 790), (W+20, H+20), (-20, H+20)], P["floor"], smooth=False)
    for i in range(1, 9): o += S.p.stroke([(-20, 800+i*36), (W+20, 795+i*36)], w=2.5, opacity=0.25)
    o += S.window_city(1250, 170, 460, 400)
    o += S.lamp(380, 800) + S.plant(1600, 860)
    o += S.armchair(900, 900, P["sofa"])
    seat = 900 - 90
    o += c.g(900, seat + HIP[d]*s, s, pose="otur", expr="kurnaz", costume="modern", seed=6)
    hx, hy = HAND_R_SIT[d]; o += S.phone(900 + hx*s, seat + HIP[d]*s + hy*s - 10, 1.2)
    return o + S.grain()

def card(d, lang="tr"):
    P = ALL[d]; S = Scene(P, d, 51)
    o = S.defs() + f'<rect width="{W}" height="{H}" fill="{P["paper"]}"/>'
    o += S.text(W/2, 585, TXT[lang]["card"], {"A": 96, "B": 118, "C": 104}[d] * (0.86 if lang == "de" else 1))
    o += f'<g transform="translate(1745,215) scale(0.42)">' + S.pillar(0, 0, 1.0) + '</g>'
    return o + S.grain()

def compare(d, lang="tr"):
    P = ALL[d]; S = Scene(P, d, 61); c = ch(d); s = SC[d]; T = TXT[lang]
    o = S.defs() + f'<rect width="{W}" height="{H}" fill="{P["paper"]}"/>'
    for y in range(60, 900, 70):
        if not 440 < y < 620: o += S.p.stroke([(960, y), (960, y+36)], w=6)
    hs = 76 if lang == "tr" else 66
    o += S.text(480, 140, T["now"], hs) + S.text(1440, 140, T["then"], hs)
    o += c.g(480, 925, s*1.02, pose="düşün", expr="düşünceli", costume="modern", seed=3)
    o += c.g(1440, 925, s*1.02, pose="düşün", expr="düşünceli", costume="tarih_öncesi", seed=3)
    for y in (510, 560): o += S.p.stroke([(905, y), (1015, y)], w=14)
    o += S.text(960, 1045, T["same"], 64, col=P["red"])
    return o + S.grain()

def chart(d, lang="tr"):
    P = ALL[d]; S = Scene(P, d, 71); c = ch(d); s = SC[d]; T = TXT[lang]
    o = S.defs() + f'<rect width="{W}" height="{H}" fill="{P["paper"]}"/>'
    x0, x1, y = 360, 1720, 640
    o += S.p.stroke([(x0, y), (x1, y)], w=9, taper=0.02)
    for k in range(0, 81, 10):
        x = x0 + (x1-x0)*k/80
        o += S.p.stroke([(x, y-18), (x, y+18)], w=5)
        o += S.text(x, y+75, str(k), 44, kind="label")
    px = x0 + (x1-x0)*35/80
    o += S.pin(px, y-30, P["red"]) + S.text(px, y-250, T["avg"], 76, col=P["red"])
    o += S.red_circle(px, y-80, 95, 88)
    o += S.text(x1, y+150, T["yrs"], 40, kind="label", anchor="end")
    o += c.g(190, 1060, s*0.62, pose="göster", expr="kurnaz", costume="modern", seed=5)
    return o + S.grain()

SCENES = [("01_dis_mekan", outdoor), ("02_modern_oda", room), ("03_metin_karti", card), ("04_karsilastirma", compare), ("05_grafik", chart)]

if __name__ == "__main__":
    os.makedirs("boards/scenes", exist_ok=True)
    jobs = []
    for d in "ABC":
        for n, f in SCENES: jobs.append((f(d), f"boards/scenes/{d}_{n}.png", W, H))
        for lang in ("de", "en"):
            jobs.append((compare(d, lang), f"boards/scenes/{d}_04_karsilastirma_{lang}.png", W, H))
            jobs.append((card(d, lang), f"boards/scenes/{d}_03_metin_karti_{lang}.png", W, H))
    render(jobs); print(len(jobs))
