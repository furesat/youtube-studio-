"""boards.py - karşılaştırma panoları."""
import os
from chars import Fasulye, Gozluk, Topak, EXPR, POSE
from palettes import ALL
from scenes import Scene, FONTS
from render import render
R = os.path.abspath("boards/scenes")
CH = {"A": Fasulye, "B": Gozluk, "C": Topak}
INFO = {
 "A": ("Mürekkep & Kiremit", "Fasulye", "Baş+gövde tek yumurta; kâğıt beyazı; kiremit atkı imzası. Konturlu, taramalı, sıcak kâğıt."),
 "B": ("Kobalt Defter", "Gözlük", "Uzun boylu; yumuşak kare kafa, mercan gözlük imzası. Arka planlar konturuz düz vektör."),
 "C": ("Toprak Gouache", "Topak", "İri kafa, kalın kontur, bulut saç; gouache katmanlı dokular, sıcak toprak paleti."),
}
SCALE = {"A": 0.55, "B": 0.54, "C": 0.5}
def T(x, y, s, size, fam="Nunito", wt=700, col="#1d1a17", anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{wt}" font-size="{size}" fill="{col}" text-anchor="{anchor}" lang="tr">{s}</text>'
def img(path, x, y, w, h, border=True):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#1d1a17" stroke-opacity="0.25" stroke-width="2"/>' if border else ""
    return f'<image href="file://{path}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice"/>' + b

def lum(h):
    h = h.lstrip("#"); c = [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]
    c = [v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4 for v in c]
    return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la+0.05)/(lb+0.05)

def overview():
    w, h = 1920, 1560; o = f'<rect width="{w}" height="{h}" fill="#fbfaf7"/>'
    o += T(60, 80, "ÖZGÜN GÖRSEL KİMLİK — 3 YÖN KARŞILAŞTIRMASI", 44, "Nunito", 900)
    o += T(60, 122, "Aynı test senaryosu, üç farklı karakter ailesi + palet + tipografi. Tüm çizimler bu projede koddan üretildi (SVG); referanstan hiçbir görsel kullanılmadı.", 22, "Nunito", 500, "#555")
    for i, d in enumerate("ABC"):
        P = ALL[d]; x = 60 + i*610; c = CH[d](P); hf, hw, lf, lw = FONTS[d]
        o += f'<rect x="{x}" y="160" width="580" height="1360" rx="18" fill="{P["paper"]}" stroke="#1d1a17" stroke-opacity="0.15"/>'
        o += T(x+30, 220, f"YÖN {d}", 26, "Nunito", 900, P["accent"]) + T(x+30, 270, INFO[d][0], 40, hf, hw)
        o += T(x+30, 308, f'Anlatıcı: “{INFO[d][1]}”', 22, "Nunito", 700, "#444")
        words = INFO[d][2].split(); line = ""; yy = 342
        for wd in words:
            if len(line + wd) > 52: o += T(x+30, yy, line, 19, "Nunito", 500, "#555"); yy += 26; line = ""
            line += wd + " "
        o += T(x+30, yy, line, 19, "Nunito", 500, "#555")
        sc = SCALE[d]
        o += c.g(x+120, 760, sc, "duruş", "mutlu", "modern", seed=2)
        o += c.g(x+290, 760, sc, "el_salla", "şaşkın", "tarih_öncesi", seed=3)
        o += c.g(x+460, 760, sc, "omuz", "kurnaz", "1900", seed=4)
        sw = ["paper", "ink", "accent", "accent2", "hide", "sky", "ground", "fire"]
        for k, r in enumerate(sw):
            o += f'<rect x="{x+30+k*65}" y="800" width="58" height="58" rx="8" fill="{P[r]}" stroke="#000" stroke-opacity="0.15"/>'
        o += T(x+30, 940, "BAŞKAYDI · ÇOĞU", 54, hf, hw) + T(x+30, 980, "Etiket: Größe · Değişim · Ağız", 24, lf, lw, "#333")
        o += img(f"{R}/{d}_01_dis_mekan.png", x+30, 1010, 520, 292)
        o += img(f"{R}/{d}_04_karsilastirma.png", x+30, 1318, 255, 143) + img(f"{R}/{d}_02_modern_oda.png", x+295, 1318, 255, 143)
    return o, w, h

def char_sheet(d):
    P = ALL[d]; c = CH[d](P); w, h = 1920, 1800; hf, hw, lf, lw = FONTS[d]
    o = f'<rect width="{w}" height="{h}" fill="{P["paper"]}"/>'
    o += T(60, 80, f"YÖN {d} · {INFO[d][0]} — karakter sayfası “{INFO[d][1]}”", 40, hf, hw)
    o += T(60, 118, "Tek temel gövde; kostüm, ifade ve poz ayrı katmanlar (parametrik). Aynı kişinin çağlar arası tanınabilirliği = 'iki dünya' mizahının taşıyıcısı.", 21, "Nunito", 500, "#555")
    sc = SCALE[d]*1.05
    o += T(60, 180, "KOSTÜM / DÖNEM", 24, "Nunito", 900, P["accent"])
    for k, (cos, lab) in enumerate((("modern", "Modern (anlatıcı)"), ("tarih_öncesi", "Tarih öncesi"), ("1900", "1900 işçi"))):
        o += c.g(200+k*300, 640, sc*1.15, "duruş", "nötr", cos, seed=5) + T(200+k*300, 690, lab, 22, lf, lw, anchor="middle")
    o += T(1000, 180, "ÖLÇEK: anlatıcı / çocuk / kalabalık", 24, "Nunito", 900, P["accent"])
    o += c.g(1150, 640, sc*1.15, "duruş", "mutlu", "modern", seed=6) + c.g(1380, 640, sc*0.7, "el_salla", "mutlu", "modern", seed=7)
    for k in range(5): o += c.g(1530+k*70, 640, sc*0.42, "duruş", "nötr", "tarih_öncesi", seed=20+k)
    o += T(60, 770, "İFADE SETİ (8)", 24, "Nunito", 900, P["accent"])
    for k, e in enumerate(EXPR):
        x = 140 + k*230
        o += c.g(x, 1190, sc*0.95, "duruş", e, "modern", seed=9) + T(x, 1235, e, 22, lf, lw, anchor="middle")
    o += T(60, 1310, "POZ SETİ (8)", 24, "Nunito", 900, P["accent"])
    for k, po in enumerate(POSE):
        x = 140 + k*230
        o += c.g(x, 1720, sc*0.8, po, "nötr" if po != "koş" else "mutlu", "modern", seed=11) + T(x, 1765, po, 22, lf, lw, anchor="middle")
    return o, w, h

def palette_board():
    w, h = 1920, 1500; o = f'<rect width="{w}" height="{h}" fill="#fbfaf7"/>'
    o += T(60, 80, "PALETLER — roller ortak, değerler yöne özgü", 44, "Nunito", 900)
    o += T(60, 120, "Kontrast = WCAG oranı (metin/vurgu rengi ↔ kâğıt). Başlık metni için ≥4.5, büyük vurgu için ≥3 hedef.", 22, "Nunito", 500, "#555")
    groups = [("Kâğıt & mürekkep", ["paper", "ink", "shade"]), ("Vurgu", ["accent", "accent2", "red", "green"]),
              ("Dış mekân gündüz", ["sky", "sky2", "hill", "ground", "ground2", "stone"]), ("Gece / ateş", ["night", "night2", "fire", "fire2"]),
              ("Karakter", ["hide", "hair", "blush", "cap"]), ("İç mekân", ["wall", "floor", "sofa"])]
    for i, d in enumerate("ABC"):
        P = ALL[d]; y0 = 170 + i*440
        o += f'<rect x="40" y="{y0}" width="1840" height="410" rx="16" fill="{P["paper"]}" stroke="#000" stroke-opacity="0.12"/>'
        o += T(70, y0+50, f"YÖN {d} · {INFO[d][0]}", 32, FONTS[d][0], FONTS[d][1])
        x = 70
        for gname, roles in groups:
            o += T(x, y0+95, gname, 18, "Nunito", 800, "#555")
            for k, r in enumerate(roles):
                yy = y0 + 110 + k*72
                if k >= 4: continue
                o += f'<rect x="{x}" y="{yy}" width="64" height="60" rx="8" fill="{P[r]}" stroke="#000" stroke-opacity="0.18"/>'
                o += T(x+76, yy+24, r, 17, "Nunito", 800) + T(x+76, yy+48, P[r].upper(), 17, "Nunito", 500, "#444")
                if r in ("ink", "accent", "accent2", "red", "green"):
                    cr = contrast(P[r], P["paper"]); ok = "#2f8f4e" if cr >= 4.5 else ("#c27c0e" if cr >= 3 else "#c0392b")
                    o += T(x+180, yy+48, f"{cr:.1f}:1", 17, "Nunito", 800, ok)
            if len(roles) > 4:  # 5. ve 6. renk yan sütun
                for k, r in enumerate(roles[4:]):
                    yy = y0 + 110 + k*72; xx = x + 170
                    o += f'<rect x="{xx}" y="{yy}" width="64" height="60" rx="8" fill="{P[r]}" stroke="#000" stroke-opacity="0.18"/>'
                    o += T(xx+76, yy+24, r, 17, "Nunito", 800) + T(xx+76, yy+48, P[r].upper(), 17, "Nunito", 500, "#444")
            x += 330 if len(roles) > 4 else 280
    return o, w, h

def type_board():
    w, h = 1920, 1720; o = f'<rect width="{w}" height="{h}" fill="#fbfaf7"/>'
    o += T(60, 80, "TİPOGRAFİ — TR / DE / EN, el yazısı başlık + okunur etiket", 44, "Nunito", 900)
    o += T(60, 120, "Tüm fontlar SIL Open Font License 1.1 (Google Fonts deposundan). Kapsam testi: ğĞ şŞ ıİ öÖ üÜ çÇ äÄ ß — fontTools ile doğrulandı.", 22, "Nunito", 500, "#555")
    rows = [("A", "Shantell Sans 700", "Shantell Sans 500"), ("B", "Kalam Bold", "Mali SemiBold"), ("C", "Playpen Sans 800", "Baloo 2 700")]
    for i, (d, hn, ln) in enumerate(rows):
        P = ALL[d]; hf, hw, lf, lw = FONTS[d]; y0 = 160 + i*420
        o += f'<rect x="40" y="{y0}" width="1840" height="390" rx="16" fill="{P["paper"]}" stroke="#000" stroke-opacity="0.12"/>'
        o += T(70, y0+44, f"YÖN {d} · başlık: {hn} · etiket: {ln}", 22, "Nunito", 800, "#555")
        o += T(70, y0+130, "11.600 YIL ÖNCE · ÇOĞU ŞAŞIRDI", 78, hf, hw)
        o += T(70, y0+215, "VOR 11.600 JAHREN · GRÖSSER", 60, hf, hw, P["accent"])
        o += T(70, y0+285, "11,600 YEARS AGO · SAME CURIOSITY", 52, hf, hw, P["accent2"])
        o += T(70, y0+350, "Etiket: Ağaç, değişim, ölçüm · Größe, Mädchen, Übung · ğüşıöç İ ÄÖÜß", 30, lf, lw, "#333")
    y0 = 160 + 3*420
    o += f'<rect x="40" y="{y0}" width="1840" height="250" rx="16" fill="#fff2f0" stroke="#c0392b" stroke-opacity="0.4"/>'
    o += T(70, y0+44, "ELENENLER — Türkçe ğ/ş eksik; tarayıcı başka fonttan yamıyor (karışık harf görünümü):", 22, "Nunito", 800, "#c0392b")
    for k, (fam, nm) in enumerate((("Fredoka", "Fredoka"), ("Gochi", "Gochi Hand"), ("Delius", "Delius"))):
        o += T(70 + k*610, y0+140, "BAŞKAYDI ĞÜŞ", 66, fam, 600) + T(70 + k*610, y0+200, nm + " — eksik: ğ Ğ ş Ş", 22, "Nunito", 700, "#c0392b")
    return o, w, h

def scene_grid():
    names = [("01_dis_mekan", "Dış mekân"), ("02_modern_oda", "Modern oda"), ("03_metin_karti", "Metin kartı"), ("04_karsilastirma", "Karşılaştırma"), ("05_grafik", "Grafik")]
    tw, th = 600, 338; w, h = 60 + 3*(tw+20) + 140, 140 + 5*(th+20)
    o = f'<rect width="{w}" height="{h}" fill="#fbfaf7"/>' + T(60, 70, "AYNI 5 SAHNE × 3 YÖN", 40, "Nunito", 900)
    for i, d in enumerate("ABC"): o += T(200 + i*(tw+20) + tw/2, 120, f"YÖN {d} · {INFO[d][0]}", 24, "Nunito", 900, ALL[d]["accent"], "middle")
    for r, (n, lab) in enumerate(names):
        o += T(60, 140 + r*(th+20) + th/2, lab, 22, "Nunito", 800)
        for i, d in enumerate("ABC"): o += img(f"{R}/{d}_{n}.png", 200 + i*(tw+20), 140 + r*(th+20), tw, th)
    return o, w, h

def lang_grid():
    tw, th = 600, 338; w, h = 200 + 3*(tw+20), 140 + 6*(th+20)
    o = f'<rect width="{w}" height="{h}" fill="#fbfaf7"/>' + T(60, 70, "ÇOK DİLLİ METİN KATMANI — aynı sahne, TR / DE / EN", 40, "Nunito", 900)
    rows = [("04_karsilastirma", "tr"), ("04_karsilastirma", "de"), ("04_karsilastirma", "en"), ("03_metin_karti", "tr"), ("03_metin_karti", "de"), ("03_metin_karti", "en")]
    for i, d in enumerate("ABC"): o += T(200 + i*(tw+20) + tw/2, 120, f"YÖN {d}", 24, "Nunito", 900, ALL[d]["accent"], "middle")
    for r, (n, lg) in enumerate(rows):
        o += T(60, 140 + r*(th+20) + th/2, lg.upper(), 30, "Nunito", 900)
        for i, d in enumerate("ABC"):
            f = f"{R}/{d}_{n}.png" if lg == "tr" else f"{R}/{d}_{n}_{lg}.png"
            o += img(f, 200 + i*(tw+20), 140 + r*(th+20), tw, th)
    return o, w, h

if __name__ == "__main__":
    jobs = []
    for name, fn in (("01_genel_bakis", overview), ("03_paletler", palette_board), ("04_tipografi", type_board), ("05_sahne_karsilastirma", scene_grid), ("06_cok_dilli", lang_grid)):
        o, w, h = fn(); jobs.append((o, f"boards/{name}.png", w, h))
    for d in "ABC":
        o, w, h = char_sheet(d); jobs.append((o, f"boards/02_karakter_{d}.png", w, h))
    render(jobs); print("ok")
