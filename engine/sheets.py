"""Fasulye karakter sayfaları (model sheet)."""
from fasulye import Fasulye, EXPR2, POSE2, COSTUMES, fx, FX
from palettes import A
from render import render
F = Fasulye(A); P = A
def T(x, y, s, size=24, wt=700, col="#1D1A17", fam="Shantell", anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{wt}" font-size="{size}" fill="{col}" text-anchor="{anchor}" lang="tr">{s}</text>'
def head(t, sub):
    return T(60, 80, t, 44, 800, anchor="start") + T(60, 120, sub, 22, 500, "#555", "Nunito", "start")
jobs = []
# 1 turnaround
o = f'<rect width="1920" height="1080" fill="{P["paper"]}"/>' + head("FASULYE — dönüş sayfası (turnaround)", "Ön · üç çeyrek · yan · arka. Ölçü çizgileri: baş-gövde yüksekliği 1,0 birim; bacak 0,27 birim. Yönler flip ile aynalanır.")
for y in (330, 520, 700, 900):
    o += f'<line x1="80" x2="1840" y1="{y}" y2="{y}" stroke="#2A7F7A" stroke-opacity="0.35" stroke-dasharray="10 10" stroke-width="2"/>'
for i, (v, lab) in enumerate((("front", "ÖN"), ("tq", "ÜÇ ÇEYREK"), ("side", "YAN"), ("back", "ARKA"))):
    o += F.g(300 + i*440, 900, 1.25, view=v, seed=7) + T(300 + i*440, 1000, lab, 30, 800)
jobs.append((o, "boards/fasulye/01_donus_sayfasi.png", 1920, 1080))
# 2 ifadeler
o = f'<rect width="1920" height="1440" fill="{P["paper"]}"/>' + head("FASULYE — ifade seti (15)", "Kaş açısı + göz tipi + göz bebeği yönü + ağız. Allık bilinçli olarak az: çocuksu değil, kuru-ironik.")
for k, e in enumerate(EXPR2):
    r, c = divmod(k, 5); x = 200 + c*380; y = 560 + r*420
    o += F.g(x, y, 0.78, expr=e, view="front" if k % 3 else "tq", seed=20+k) + T(x, y+50, e, 26)
jobs.append((o, "boards/fasulye/02_ifadeler.png", 1920, 1440))
# 3 pozlar
o = f'<rect width="1920" height="1440" fill="{P["paper"]}"/>' + head("FASULYE — poz seti (16)", "Kol = omuz→dirsek→el; poz kütüphanesi JSON parametresi. Her poz her görünüm ve kostümle birleşir.")
for k, po in enumerate(POSE2):
    r, c = divmod(k, 8); x = 140 + c*235; y = 640 + r*620
    o += F.g(x, y, 0.68, pose=po, expr="nötr" if po not in ("koş", "it") else "kurnaz", view="tq" if po in ("it", "kaz") else "front", seed=40+k) + T(x, y+50, po, 24)
jobs.append((o, "boards/fasulye/03_pozlar.png", 1920, 1440))
# 4 kostümler + efektler
o = f'<rect width="1920" height="1300" fill="{P["paper"]}"/>' + head("FASULYE — kostümler (5) ve komik efektler (9)", "Kostüm = katman. Yüz ve siluet sabit kalır: 'aynı kişi, başka çağ' şakası buradan doğar.")
labs = {"modern": "modern (anlatıcı)", "tarih_öncesi": "tarih öncesi", "arkeolog": "arkeolog", "bilim": "bilim insanı", "1900": "1900 işçi"}
for k, cs in enumerate(COSTUMES):
    x = 220 + k*370
    o += F.g(x, 650, 0.92, costume=cs, view="tq", expr="nötr", seed=60+k) + T(x, 700, labs[cs], 26)
for k, f in enumerate(FX):
    x = 140 + k*205; y = 1000
    o += f'<rect x="{x-90}" y="{y-120}" width="180" height="200" rx="14" fill="#fff" stroke="#1D1A17" stroke-opacity="0.12"/>'
    o += fx(f, x + (60 if f == "hız" else 0), y - (10 if f in ("soru", "ünlem") else 30) + (40 if f in ("soru", "ünlem") else 0), 0.8, P) + T(x, y + 60, f, 22)
jobs.append((o, "boards/fasulye/04_kostum_efekt.png", 1920, 1300))
# 5 komik tepki örnekleri
o = f'<rect width="1920" height="1080" fill="{P["paper"]}"/>' + head("FASULYE — komik tepki kombinasyonları", "İfade + poz + efekt üçlüsü; kuru mizahta tepki küçük ve gecikmeli tutulur.")
combos = [("dehşet", "yukarı", "şok", "Fark etmek"), ("şüpheli", "eller_belde", "soru", "İkna olmamak"), ("yorgun", "pes", "ter", "Taş taşımak"),
          ("uykulu", "pes", "zzz", "Yarın bitiririz"), ("kahkaha", "anlat", "parıltı", "Eureka"), ("öfkeli", "eller_belde", "buhar", "Yanlış tarih")]
for k, (e, po, f, lab) in enumerate(combos):
    x = 170 + k*318
    o += F.g(x, 900, 0.8, pose=po, expr=e, view="tq" if k % 2 else "front", seed=80+k)
    o += fx(f, x + 70, 450 if f in ("soru",) else 470, 0.8, P) + T(x, 960, lab, 26)
jobs.append((o, "boards/fasulye/05_komik_tepkiler.png", 1920, 1080))
import os; os.makedirs("boards/fasulye", exist_ok=True); render(jobs); print("ok")
