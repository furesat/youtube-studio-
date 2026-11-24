"""pilot.py - 60 sn pilot: 'Tarladan Önce Tapınak? — Göbeklitepe'
Her çekim (shot) = görsel katman (dilden bağımsız) + metin katmanı (dil başına ayrı PNG).
Çekimler cümlelere bağlı; çekim süresi = cümle süresi × ağırlık / toplam ağırlık (geçici zamanlama)."""
import sys, os
_T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _T if os.path.exists(os.path.join(_T, "fasulye.py")) else os.path.join(_T, "identity"))
from fasulye import Fasulye, fx
from library import Lib
from palettes import A as P

F = Fasulye(P)
def L(seed=101): return Lib(P, seed)
RED = P["red"]; INK = P["ink"]; TEAL = P["accent2"]

# ---- metin katmanı içerikleri (anahtar -> dil) ----
TXT = {
 "t_title":   {"tr": "DÜNYANIN EN ESKİ ANITLARINDAN BİRİ", "de": "EINES DER ÄLTESTEN MONUMENTE", "en": "ONE OF THE OLDEST MONUMENTS"},
 "t_nofarm":  {"tr": "HENÜZ ÇİFTÇİ YOK", "de": "NOCH KEINE BAUERN", "en": "NO FARMERS YET"},
 "t_bce":     {"tr": "MÖ ~9500", "de": "~9500 v. Chr.", "en": "~9500 BCE"},
 "t_today":   {"tr": "BUGÜN", "de": "HEUTE", "en": "TODAY"},
 "t_place":   {"tr": "GÖBEKLİTEPE · ŞANLIURFA", "de": "GÖBEKLI TEPE · ŞANLIURFA", "en": "GÖBEKLI TEPE · ŞANLIURFA"},
 "t_5m":      {"tr": "> 5 m", "de": "> 5 m", "en": "> 5 m"},
 "t_wheel":   {"tr": "TEKERLEK", "de": "RAD", "en": "WHEEL"},
 "t_metal":   {"tr": "METAL", "de": "METALL", "en": "METAL"},
 "t_write":   {"tr": "YAZI", "de": "SCHRIFT", "en": "WRITING"},
 "t_safety":  {"tr": "İŞ GÜVENLİĞİ?", "de": "ARBEITSSCHUTZ?", "en": "HEALTH & SAFETY?"},
 "t_fox":     {"tr": "TİLKİ", "de": "FUCHS", "en": "FOX"},
 "t_vulture": {"tr": "AKBABA", "de": "GEIER", "en": "VULTURE"},
 "t_snake":   {"tr": "YILAN", "de": "SCHLANGE", "en": "SNAKE"},
 "t_7m":      {"tr": "~7 m · YARIM", "de": "~7 m · UNFERTIG", "en": "~7 m · UNFINISHED"},
 "t_tomorrow":{"tr": "“YARIN BİTİRİRİZ.”", "de": "„MORGEN MACHEN WIR'S FERTIG.“", "en": "“WE'LL FINISH IT TOMORROW.”"},
 "t_stone":   {"tr": "STONEHENGE", "de": "STONEHENGE", "en": "STONEHENGE"},
 "t_stone_d": {"tr": "MÖ ~3000", "de": "~3000 v. Chr.", "en": "~3000 BCE"},
 "t_6000":    {"tr": "≈ 6.000 YIL", "de": "≈ 6.000 JAHRE", "en": "≈ 6,000 YEARS"},
 "t_gt":      {"tr": "GÖBEKLİTEPE", "de": "GÖBEKLI TEPE", "en": "GÖBEKLI TEPE"},
 "t_1963":    {"tr": "1963", "de": "1963", "en": "1963"},
 "t_1994":    {"tr": "1994", "de": "1994", "en": "1994"},
 "t_grave":   {"tr": "MEZAR TAŞI?", "de": "GRABSTEIN?", "en": "GRAVESTONE?"},
 "t_pillar":  {"tr": "SÜTUN!", "de": "PFEILER!", "en": "PILLAR!"},
 "t_temple":  {"tr": "“DÜNYANIN İLK TAPINAĞI”", "de": "„DER ERSTE TEMPEL DER WELT“", "en": "“THE WORLD'S FIRST TEMPLE”"},
 "t_schmidt": {"tr": "Klaus Schmidt'in yorumu", "de": "Deutung von Klaus Schmidt", "en": "Klaus Schmidt's interpretation"},
 "t_houses":  {"tr": "EVLER · SU TESİSATI", "de": "HÄUSER · WASSERANLAGEN", "en": "HOUSES · WATER SYSTEMS"},
 "t_q_temple":{"tr": "TAPINAK?", "de": "TEMPEL?", "en": "TEMPLE?"},
 "t_q_settle":{"tr": "YERLEŞİM?", "de": "SIEDLUNG?", "en": "SETTLEMENT?"},
 "t_ambitious":{"tr": "ÇOK İDDİALI BİR YERLEŞİM", "de": "SEHR AMBITIONIERTE SIEDLUNG", "en": "A VERY AMBITIOUS SETTLEMENT"},
 "t_5pct":    {"tr": "%5'TEN AZI KAZILDI", "de": "< 5 % AUSGEGRABEN", "en": "< 5% EXCAVATED"},
 "t_hurry":   {"tr": "ACELESİ YOK.", "de": "KEINE EILE.", "en": "NO HURRY."},
}

def tx(key, x, y, size, col=INK, anchor="middle", wt=800):
    return dict(key=key, x=x, y=y, size=size, col=col, anchor=anchor, wt=wt)

def red_x(cx, cy, s, seed=3):
    return L(seed).red_x(cx, cy, s)

def paper(): return L().loc("beyaz_kart")

# ============ ÇEKİMLER ============
# her çekim: (id, cümle, ağırlık, görsel_fn, [metin öğeleri], not)
def s01():
    l = L(); return l.loc("beyaz_kart") + l.obj("t_sutun", 1760, 300, 0.45)
def s02():
    l = L(5); return l.loc("tepe") + F.g(330, 1040, 0.95, "göster", "kurnaz", "modern", view="tq", seed=11)
def s03a():
    l = L(); return l.loc("beyaz_kart") + l.obj("bugday", 960, 760, 1.6)
def s03b():
    return s03a() + red_x(960, 560, 210)
def s04():
    l = L(); o = l.loc("beyaz_kart")
    o += l.p.stroke([(220, 620), (1700, 620)], w=9, taper=0.02)
    o += l.p.stroke([(1700, 600), (1730, 620), (1700, 640)], w=8)
    o += l.pin(380, 590, RED) + l.p.stroke([(380, 600), (380, 640)], w=6) + l.p.stroke([(1640, 600), (1640, 640)], w=6)
    o += F.g(1640, 560, 0.42, "duruş", "nötr", "modern", seed=4)
    return o
def s05():
    l = L(9); return l.loc("tepe") + F.g(1600, 1050, 0.8, "el_salla", "mutlu", "tarih_öncesi", view="tq", flip=True, seed=12)
def s06():
    l = L(6); o = l.loc("tepe", pillars=False)
    for x in (1000, 1220, 1440): o += l.p.blob(x, 948, 34, 34, P["hide"], w=5) + l.p.blob(x, 948, 10, 10, P["hair"], w=3)
    o += l.obj("t_sutun", 0, 0, 1).replace('translate(0,0) scale(1)', 'translate(1560,846) rotate(-90) scale(2.0)')
    for k, x in enumerate((640, 770)):
        o += F.g(x, 1040, 0.72, "it", ("yorgun", "dehşet")[k], "tarih_öncesi", view="side", seed=20+k)
    o += F.g(1780, 1050, 0.6, "eller_belde", "şüpheli", "tarih_öncesi", view="tq", flip=True, seed=22)
    o += fx("ter", 640, 610, 1.0, P) + fx("ter", 780, 600, 1.0, P) + fx("hız", 550, 820, 1.0)
    return o
def s07():
    l = L(7); o = l.loc("beyaz_kart") + l.obj("t_sutun", 1040, 990, 2.6)
    o += l.p.stroke([(1400, 990), (1400, 150)], w=6) + l.p.stroke([(1380, 150), (1420, 150)], w=6) + l.p.stroke([(1380, 990), (1420, 990)], w=6)
    o += F.g(640, 990, 0.62, "yukarı", "şaşkın", "modern", view="tq", seed=13) + fx("şok", 670, 640, 0.8)
    return o
def s08(n):
    l = L(8); o = l.loc("beyaz_kart")
    items = (("tekerlek", 420), ("balta", 960), ("parsomen", 1500))
    for i, (nm, x) in enumerate(items):
        o += l.obj(nm, x, 720, 1.25)
        if i < n: o += red_x(x, 580, 150, seed=10+i)
    return o
def s09():
    l = L(9); o = l.loc("tepe", pillars=False)
    o += l.obj("t_sutun", 0, 0, 1).replace('translate(0,0) scale(1)', 'translate(900,1000) rotate(14) scale(1.25)')
    o += F.g(1180, 1050, 0.85, "pes", "endişeli", "tarih_öncesi", view="tq", flip=True, seed=24) + fx("ter", 1130, 590, 1.2, P)
    o += l.obj("baret", 1560, 400, 1.0)
    return o
def s10(n):
    l = L(10); o = f'<rect width="1920" height="1080" fill="#b3a693"/>' + l.defs()
    o += l.p.hatch(0, 0, 1920, 1080, step=40, ang=-0.2, w=2.5, color=P["stone2"], opacity=0.35, length=160)
    for i, (nm, x, y) in enumerate((("tilki", 520, 560), ("akbaba", 1380, 430), ("yilan", 1000, 860))):
        if i < n: o += l.obj("kabartma_" + nm, x, y, 1.6)
    return o + l.grain()
def s11():
    l = L(11); return l.loc("tas_ocagi")
def s12():
    l = L(11); return l.loc("tas_ocagi") + F.g(190, 1050, 0.78, "pes", "uykulu", "tarih_öncesi", view="side", seed=25) + fx("zzz", 260, 580, 1.3) + l.obj("cakmaktasi", 330, 1040, 0.4)
def s13():
    l = L(); o = l.loc("beyaz_kart")
    o += l.p.stroke([(160, 640), (1760, 640)], w=9, taper=0.02)
    for x in (300, 1060, 1720): o += l.p.stroke([(x, 615), (x, 665)], w=7)
    o += l.obj("t_sutun", 300, 600, 0.75)
    for k, x in enumerate((990, 1060, 1130)): o += l.obj("t_sutun", x, 600, 0.32)
    o += F.g(1720, 600, 0.42, "duruş", "nötr", "modern", seed=4)
    o += l.p.stroke([(300, 760), (300, 790), (1060, 790), (1060, 760)], w=7, color=RED, taper=0.02)
    return o
def s14():
    l = L(14); o = l.loc("tepe")
    o += F.g(420, 1050, 0.82, "kaz", "sıkılmış", "1900", view="tq", seed=30) + F.g(1560, 1050, 0.82, "eller_belde", "şüpheli", "1900", view="tq", flip=True, seed=31)
    o += l.p.blob(1300, 300, 150, 100, "#fff", w=6) + l.p.blob(1400, 440, 22, 18, "#fff", w=5) + l.p.blob(1440, 500, 12, 10, "#fff", w=4)
    o += l.obj("mezar_tasi", 1300, 380, 0.75)
    return o
def s14b():
    l = L(14); o = l.loc("tepe")
    o += F.g(300, 1050, 0.82, "duruş", "sıkılmış", "1900", view="back", seed=30) + F.g(520, 1050, 0.82, "duruş", "nötr", "1900", view="back", seed=31)
    o += fx("hız", 760, 820, 1.0)
    return o
def s15():
    l = L(15); o = l.loc("tepe")
    o += F.g(560, 1050, 0.95, "yukarı", "kahkaha", "arkeolog", view="tq", seed=32) + fx("parıltı", 680, 420, 1.3)
    o += l.obj("ampul", 820, 380, 0.75)
    return o
def s16(n):
    l = L(16); o = l.loc("beyaz_kart") + l.obj("mezar_tasi", 560, 760, 1.6)
    if n > 0:
        o += l.p.stroke([(820, 560), (1100, 560)], w=12, taper=0.05) + l.p.stroke([(1060, 520), (1110, 560), (1060, 600)], w=12)
        o += l.obj("t_sutun", 1420, 820, 1.55)
    return o
def s17():
    l = L(17); return l.loc("beyaz_kart") + l.obj("t_sutun", 960, 470, 0.7)
def s18a():
    l = L(18); return l.loc("kazi_alani") + F.g(1650, 1040, 0.62, "kaz", "sıkılmış", "arkeolog", view="tq", flip=True, seed=33)
def s18():
    l = L(18); return l.loc("kazi_alani", house=True, channel=True) + F.g(1650, 1040, 0.62, "göster", "şaşkın", "arkeolog", view="tq", flip=True, seed=33) + fx("şok", 1640, 520, 0.7)
def s19():
    l = L(19); o = l.loc("beyaz_kart")
    for y in range(60, 1000, 70): o += l.p.stroke([(960, y), (960, y+36)], w=6)
    o += l.obj("t_sutun", 480, 820, 1.2) + l.obj("ev_plani", 1440, 760, 1.4)
    return o
def s20():
    l = L(20); return l.loc("tepe") + F.g(960, 1050, 1.0, "eller_belde", "gururlu", "tarih_öncesi", seed=34) + fx("parıltı", 1080, 470, 1.0)
def s21():
    l = L(21); return l.loc("kesit")
def s22():
    l = L(22); return l.loc("gece_tepe") + F.g(1500, 1060, 0.85, "duruş", "nötr", "modern", view="back", seed=35)

def mins(x): return x
SHOTS = [
 ("S01", "L01", 1.0, s01, [tx("t_title", 960, 580, 92)], "Beyaz kart: kanca başlığı"),
 ("S02", "L01", 1.0, s02, [], "Tepe; anlatıcı gösteriyor"),
 ("S03a","L02", 0.5, s03a, [tx("t_nofarm", 960, 960, 76)], "Buğday"),
 ("S03b","L02", 0.6, s03b, [tx("t_nofarm", 960, 960, 76, RED)], "Buğday + kırmızı X (durum değişimi)"),
 ("S04", "L03", 1.0, s04, [tx("t_bce", 380, 430, 70, RED), tx("t_today", 1640, 720, 48)], "Zaman çizgisi"),
 ("S05", "L03", 1.2, s05, [tx("t_place", 960, 150, 70)], "Mekân etiketi"),
 ("S06", "L04", 1.2, s06, [], "Sütunu itiyorlar (komik zorlanma)"),
 ("S07", "L04", 1.0, s07, [tx("t_5m", 1530, 590, 90, RED, "middle")], "Ölçek karşılaştırması"),
 ("S08a","L05", 1.0, lambda: s08(1), [tx("t_wheel", 420, 820, 54)], "X 1"),
 ("S08b","L05", 1.0, lambda: s08(2), [tx("t_wheel", 420, 820, 54), tx("t_metal", 960, 820, 54)], "X 2"),
 ("S08c","L05", 1.1, lambda: s08(3), [tx("t_wheel", 420, 820, 54), tx("t_metal", 960, 820, 54), tx("t_write", 1500, 820, 54)], "X 3"),
 ("S09", "L06", 1.0, s09, [tx("t_safety", 960, 140, 72, RED)], "Sallanan sütun + baret"),
 ("S10a","L07", 0.9, lambda: s10(1), [tx("t_fox", 520, 760, 60)], "Kabartma 1"),
 ("S10b","L07", 0.9, lambda: s10(2), [tx("t_fox", 520, 760, 60), tx("t_vulture", 1380, 640, 60)], "Kabartma 2"),
 ("S10c","L07", 1.0, lambda: s10(3), [tx("t_fox", 520, 760, 60), tx("t_vulture", 1380, 640, 60), tx("t_snake", 1000, 1010, 60)], "Kabartma 3"),
 ("S11", "L08", 1.0, s11, [tx("t_7m", 990, 640, 70)], "Ocakta yarım sütun"),
 ("S12", "L08", 1.4, s12, [tx("t_tomorrow", 960, 1010, 66, RED)], "Uyuyan işçi: 'yarın'"),
 ("S13", "L09", 1.0, s13, [tx("t_gt", 300, 220, 48), tx("t_bce", 300, 720, 42, RED), tx("t_stone", 1060, 410, 42), tx("t_stone_d", 1060, 720, 42), tx("t_today", 1720, 720, 42), tx("t_6000", 680, 870, 64, RED)], "Zaman çizgisi: 6.000 yıl"),
 ("S14a","L10", 1.4, s14, [tx("t_1963", 160, 150, 80, RED, "start"), tx("t_grave", 1300, 170, 44)], "1963: mezar taşı sandılar"),
 ("S14b","L10", 1.0, s14b, [tx("t_1963", 160, 150, 80, RED, "start")], "…ve geçip gittiler (arkadan)"),
 ("S15", "L11", 1.0, s15, [tx("t_1994", 160, 150, 80, RED, "start")], "1994: fark ediş"),
 ("S16a","L11", 0.6, lambda: s16(0), [tx("t_grave", 560, 920, 60)], "Mezar taşı"),
 ("S16b","L11", 0.8, lambda: s16(1), [tx("t_grave", 560, 920, 60), tx("t_pillar", 1420, 920, 70, RED)], "→ sütun"),
 ("S17", "L12", 1.0, s17, [tx("t_temple", 960, 640, 80), tx("t_schmidt", 960, 730, 38, "#555", wt=500)], "Alıntı kartı"),
 ("S18a","L13", 0.8, s18a, [], "Kazı alanı: yeni açma"),
 ("S18b","L13", 1.0, s18, [tx("t_houses", 960, 110, 64)], "Ev temeli + su kanalı belirir (durum değişimi)"),
 ("S19", "L14", 0.9, s19, [tx("t_q_temple", 480, 160, 76), tx("t_q_settle", 1440, 160, 76)], "Karşılaştırma"),
 ("S20", "L14", 1.1, s20, [tx("t_ambitious", 960, 140, 76, RED)], "Gururlu 'yerleşimci'"),
 ("S21", "L15", 1.0, s21, [tx("t_5pct", 960, 140, 80, RED)], "Kesit: %5"),
 ("S22", "L16", 1.0, s22, [tx("t_hurry", 960, 990, 70, "#f3ecd2")], "Gece; bekleyen tepe"),
]
END_HOLD = 1.2   # son çekime eklenen sessiz kapanış (sn)
