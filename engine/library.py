"""library.py - yeniden kullanılabilir nesne ve mekân kütüphanesi (Yön A dili: konturlu, taramalı, sıcak kâğıt).
Nesne:  Lib(P).obj(ad, x, y, s)  -> SVG; orijin = nesnenin alt-orta noktası, doğal boy ~200 birim.
Mekân:  Lib(P).loc(ad)            -> 1920x1080 arka plan SVG."""
import math
from scenes import Scene, W, H
from ink import Pen

INK = "#1D1A17"

class Lib(Scene):
    def __init__(self, P, seed=101):
        super().__init__(P, "A", seed)

    # =============== NESNELER ===============
    def obj(self, name, x, y, s=1.0, **kw):
        fn = getattr(self, "o_" + name)
        return f'<g transform="translate({x},{y}) scale({s})">' + fn(**kw) + "</g>"

    def _poly(self, pts, col, smooth=False, w=5):
        return self.p.shape(pts, col, w=w, smooth=smooth)

    # --- tarih / arkeoloji ---
    def o_t_sutun(self, relief=None, h=1.0):
        P = self.P; p = self.p; o = ""
        o += self._poly([(-34, 0), (-30, -260*h), (30, -260*h), (34, 0)], P["stone"])
        o += self._poly([(-95, -250*h), (-92, -320*h), (92, -322*h), (95, -252*h)], P["stone"])
        o += f'<path d="M8,0 L6,{-255*h} L29,{-257*h} L33,0Z" fill="{P["stone2"]}" opacity="0.5"/>'
        o += p.hatch(-28, -240*h, 28, -20, step=12, ang=-1.3, w=1.6, opacity=0.18, length=30)
        if relief: o += f'<g transform="translate(0,{-150*h}) scale(0.32)">' + getattr(self, "o_kabartma_" + relief)() + "</g>"
        return o
    def _relief(self, pts_list):
        P = self.P; p = self.p; o = ""
        for pts in pts_list:
            o += p.shape([(x+4, y+4) for x, y in pts], P["stone2"], w=0)
            o += p.shape(pts, "#d8cfc3", w=4, extra='')
        return o
    def o_kabartma_tilki(self):
        body = [(-110, 20), (-60, -30), (40, -35), (95, -10), (110, -60), (140, -70), (150, -40), (130, 0), (80, 40), (-60, 45)]
        tail = [(-110, 20), (-170, -10), (-200, 30), (-150, 40)]
        return self._relief([tail, body]) + self.p.stroke([(110, -60), (118, -95), (128, -64)], w=6)
    def o_kabartma_domuz(self):
        body = [(-130, 10), (-100, -50), (20, -70), (110, -40), (150, -10), (130, 30), (-110, 45)]
        o = self._relief([body])
        o += self.p.stroke([(140, 0), (165, -20), (160, -35)], w=7)
        for lx in (-90, -40, 40, 90): o += self.p.stroke([(lx, 40), (lx, 85)], w=8)
        return o
    def o_kabartma_akbaba(self):
        wingL = [(0, -10), (-60, -80), (-180, -100), (-120, -20), (-60, 20)]
        wingR = [(0, -10), (60, -80), (180, -100), (120, -20), (60, 20)]
        body = [(-30, -20), (30, -20), (25, 80), (-25, 80)]
        return self._relief([wingL, wingR, body]) + self.p.blob(0, -45, 26, 24, "#d8cfc3", w=4)
    def o_kabartma_yilan(self):
        pts = [(-180, 40), (-120, -30), (-60, 40), (0, -30), (60, 40), (120, -30), (170, 10)]
        o = self.p.stroke([(x+4, y+4) for x, y in pts], w=30, color=self.P["stone2"], taper=0.15)
        o += self.p.stroke(pts, w=24, color="#d8cfc3", taper=0.15) + self.p.blob(175, 8, 22, 15, "#d8cfc3", w=4)
        return o
    def o_cakmaktasi(self):
        P = self.P
        o = self._poly([(-25, 0), (-38, -60), (-10, -190), (6, -195), (30, -70), (24, 0)], "#8f8a86")
        for y in (-40, -80, -120, -160): o += self.p.stroke([(-20, y), (18, y-8)], w=2.5, opacity=0.4)
        return o
    def o_tas_kase(self):
        o = self.p.shape([(-120, -80), (120, -80), (95, -10), (60, 0), (-60, 0), (-95, -10)], self.P["stone"], w=5)
        o += self.p.blob(0, -80, 120, 20, self.P["stone2"], w=5)
        return o
    def o_mala(self):
        P = self.P
        o = self._poly([(-70, -10), (0, -150), (70, -10), (0, 10)], "#c9ced3")
        o += self.p.stroke([(0, -150), (0, -200)], w=8) + self._poly([(-14, -200), (14, -200), (12, -270), (-12, -270)], P["accent2"])
        return o
    def o_firca(self):
        P = self.P
        o = self._poly([(-12, -60), (12, -60), (10, -240), (-10, -240)], P["hide"])
        o += self._poly([(-40, 0), (40, 0), (22, -60), (-22, -60)], "#e9d8a6")
        for x in range(-30, 35, 10): o += self.p.stroke([(x, -2), (x*0.6, -55)], w=2, opacity=0.5)
        return o
    def o_kurek(self):
        P = self.P
        o = self.p.stroke([(0, -60), (0, -300)], w=12, color=P["hide"]) + self.p.stroke([(-30, -300), (30, -300)], w=12, color=P["hide"])
        o += self._poly([(-50, 0), (-55, -70), (55, -70), (50, 0), (0, 25)], "#aab1b7", smooth=True)
        return o
    def o_olcek(self):  # arkeolojik ölçek çubuğu
        o = ""
        for i in range(6):
            o += f'<rect x="{-150+i*50}" y="-24" width="50" height="24" fill="{INK if i % 2 == 0 else "#fff"}"/>'
        return o + self.p.shape([(-150, -24), (150, -24), (150, 0), (-150, 0)], "none", w=4, smooth=False)
    def o_parsomen(self):
        P = self.P
        o = self._poly([(-90, -20), (90, -20), (90, -200), (-90, -200)], "#f1e2bf")
        for y in (-170, -140, -110, -80, -50): o += self.p.stroke([(-65, y), (60, y)], w=3, opacity=0.45, rough=2)
        o += self.p.blob(0, -205, 105, 14, "#e3cf9f", w=5) + self.p.blob(0, -16, 105, 14, "#e3cf9f", w=5)
        return o
    def o_mezar_tasi(self):
        P = self.P
        o = self.p.shape([(-60, 0), (-60, -150), (-40, -190), (40, -190), (60, -150), (60, 0)], P["stone"], w=5)
        o += self.p.stroke([(0, -160), (0, -60)], w=7) + self.p.stroke([(-30, -125), (30, -125)], w=7)
        return o
    def o_tekerlek(self):
        P = self.P; o = self.p.blob(0, -110, 110, 110, P["hide"], w=7)
        o += self.p.blob(0, -110, 80, 80, "none", w=4) + self.p.blob(0, -110, 18, 18, P["hair"], w=4)
        for a in range(0, 360, 45):
            r = math.radians(a); o += self.p.stroke([(0, -110), (math.cos(r)*80, -110 + math.sin(r)*80)], w=6)
        return o
    def o_balta(self):
        P = self.P
        o = self.p.stroke([(0, 0), (0, -240)], w=12, color=P["hide"])
        o += self._poly([(-8, -262), (70, -292), (92, -190), (-8, -212)], "#c27a43")
        o += self.p.stroke([(60, -280), (78, -200)], w=3, color="#fff", opacity=0.5)
        return o
    def o_bugday(self):
        P = self.P; o = ""
        for dx, a in ((-30, -0.25), (0, 0), (30, 0.25)):
            tip = (dx + math.sin(a)*60, -230)
            o += self.p.stroke([(0, 0), (dx*0.5, -120), tip], w=5, color="#a07a2c")
            for k in range(5):
                yy = -150 - k*18; xx = dx*0.7 + math.sin(a)*(k*10)
                o += self.p.blob(xx-9, yy, 9, 15, "#e0b552", w=3, rot=-0.4) + self.p.blob(xx+9, yy, 9, 15, "#e0b552", w=3, rot=0.4)
        return o
    def o_ev_plani(self):  # kazıda dikdörtgen ev temeli (kuşbakışı)
        P = self.P; o = ""
        for (a, b) in (((-160, -120), (160, -120)), ((160, -120), (160, 0)), ((160, 0), (40, 0)), ((-40, 0), (-160, 0)), ((-160, 0), (-160, -120)), ((0, -120), (0, -40))):
            n = int(math.dist(a, b)//28)
            for i in range(n+1):
                t = i/max(n, 1); o += self.p.blob(a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t, 15, 11, P["stone"], w=3)
        return o
    # --- bilim ---
    def o_buyutec(self):
        P = self.P
        o = self.p.stroke([(50, -60), (120, 10)], w=22, color=P["hair"]) + self.p.blob(0, -120, 80, 80, "#d9eef2", w=8)
        o += self.p.stroke([(-40, -150), (-15, -170)], w=6, color="#fff")
        return o
    def o_erlen(self):
        P = self.P
        o = self._poly([(-20, -200), (20, -200), (20, -140), (80, 0), (-80, 0), (-20, -140)], "#e8f3f4")
        o += self.p.shape([(-55, -60), (55, -60), (80, 0), (-80, 0)], P["accent2"], w=0, smooth=False)
        o += self.p.blob(-20, -35, 8, 8, "#fff", line=None, w=0) + self.p.blob(15, -80, 5, 5, P["accent2"], line=None, w=0)
        return o + self._poly([(-20, -200), (20, -200), (20, -140), (80, 0), (-80, 0), (-20, -140)], "none")
    def o_mikroskop(self):
        P = self.P
        o = self._poly([(-90, 0), (90, 0), (80, -30), (-80, -30)], P["hair"])
        o += self.p.stroke([(40, -30), (50, -170), (0, -230)], w=26, color=P["cap"])
        o += self._poly([(-40, -190), (-5, -250), (25, -230), (-10, -170)], "#c9ced3")
        o += self._poly([(-60, -100), (40, -100), (40, -85), (-60, -85)], "#c9ced3")
        return o
    def o_ampul(self):
        P = self.P
        o = f'<circle cx="0" cy="-150" r="120" fill="{P["fire2"]}" opacity="0.25"/>'
        o += self.p.blob(0, -150, 75, 80, P["fire2"], w=6) + self._poly([(-35, -70), (35, -70), (30, 0), (-30, 0)], "#b9b4aa")
        o += self.p.stroke([(-20, -110), (0, -150), (20, -110)], w=4)
        return o
    def o_kum_saati(self):
        P = self.P
        o = self._poly([(-80, -230), (80, -230), (80, -210), (-80, -210)], P["hide"]) + self._poly([(-80, 0), (80, 0), (80, -20), (-80, -20)], P["hide"])
        o += self.p.shape([(-60, -210), (60, -210), (8, -115), (60, -20), (-60, -20), (-8, -115)], "#e8f3f4", w=5, smooth=False)
        o += self.p.shape([(-40, -20), (40, -20), (0, -60)], "#e0b552", w=0, smooth=False) + self.p.shape([(-30, -185), (30, -185), (0, -130)], "#e0b552", w=0, smooth=False)
        return o
    def o_kitap(self):
        P = self.P
        o = self._poly([(-110, 0), (110, 0), (110, -40), (-110, -40)], P["accent"]) + self._poly([(-100, -40), (100, -40), (100, -60), (-100, -60)], "#fffaf0")
        o += self._poly([(-110, -60), (110, -60), (110, -100), (-110, -100)], P["accent2"])
        return o + self.p.stroke([(-80, -80), (40, -80)], w=4, color="#fff", opacity=0.7)
    def o_takvim(self, text="9500"):
        P = self.P
        o = self._poly([(-100, 0), (100, 0), (100, -200), (-100, -200)], "#fffaf0") + self._poly([(-100, -200), (100, -200), (100, -150), (-100, -150)], P["red"])
        for x in (-50, 50): o += self.p.stroke([(x, -215), (x, -185)], w=8)
        return o + f'<text x="0" y="-45" font-family="Shantell" font-weight="800" font-size="74" text-anchor="middle" fill="{INK}">{text}</text>'
    # --- gündelik ---
    def o_telefon(self):
        P = self.P
        return self._poly([(-50, 0), (50, 0), (50, -190), (-50, -190)], INK) + f'<rect x="-40" y="-178" width="80" height="150" rx="6" fill="{P["accent2"]}"/>' + self.p.blob(0, -14, 7, 7, "#555", line=None, w=0)
    def o_kahve(self):
        P = self.P
        o = self._poly([(-60, 0), (60, 0), (72, -130), (-72, -130)], "#fffaf0") + self.p.blob(0, -130, 72, 14, "#6b4423", w=5)
        o += self.p.stroke([(70, -105), (110, -95), (105, -45), (62, -40)], w=9)
        o += self.p.stroke([(-15, -160), (0, -190), (-10, -220)], w=4, opacity=0.5) + self.p.stroke([(20, -160), (35, -190), (25, -220)], w=4, opacity=0.5)
        return o
    def o_laptop(self):
        P = self.P
        o = self._poly([(-130, -40), (130, -40), (120, -210), (-120, -210)], "#c9ced3") + f'<rect x="-108" y="-198" width="216" height="145" fill="{P["sky"]}"/>'
        return o + self._poly([(-160, 0), (160, 0), (130, -40), (-130, -40)], "#b4bbc2")
    def o_baret(self):
        P = self.P
        o = self.p.shape([(-110, -10), (-100, -80), (-60, -130), (0, -145), (60, -130), (100, -80), (110, -10)], "#F2C14E", w=6)
        return o + self._poly([(-140, 0), (140, 0), (130, -20), (-130, -20)], "#F2C14E") + self.p.stroke([(0, -140), (0, -30)], w=6, opacity=0.5)
    def o_kalem(self):
        P = self.P
        return self._poly([(-12, 0), (12, 0), (12, -200), (-12, -200)], "#F2C14E") + self._poly([(-12, 0), (12, 0), (0, 40)], "#e9d8a6") + self._poly([(-12, -200), (12, -200), (12, -225), (-12, -225)], P["accent"])
    def o_saat(self):
        P = self.P
        o = self.p.blob(0, -110, 110, 110, "#fffaf0", w=8)
        for a in range(0, 360, 30):
            r = math.radians(a); o += self.p.stroke([(math.cos(r)*85, -110+math.sin(r)*85), (math.cos(r)*98, -110+math.sin(r)*98)], w=5)
        return o + self.p.stroke([(0, -110), (0, -175)], w=8) + self.p.stroke([(0, -110), (45, -90)], w=8)

    # =============== MEKÂNLAR ===============
    def loc(self, name, **kw):
        return self.defs() + getattr(self, "l_" + name)(**kw) + self.grain()

    def l_beyaz_kart(self):
        return f'<rect width="{W}" height="{H}" fill="{self.P["paper"]}"/>'

    def _hill(self, base=720, top=470, col=None):
        P = self.P; p = self.p
        pts = [(-40, base+40)] + [(x, base - (base-top)*math.exp(-((x-960)/620)**2) + p.jit(6)) for x in range(-40, W+80, 80)] + [(W+40, base+40), (W+40, H+40), (-40, H+40)]
        return self.fill(pts, col or P["ground"])

    def l_tepe(self, pillars=True, people=False):
        P = self.P; p = self.p
        o = self.sky(P["sky"], P["sky2"], 700) + self.sun(1640, 170, 55)
        o += self.hills(560, P["hill"], 50, 0.2) + self._hill(760, 430, P["ground"])
        o += p.hatch(200, 560, 1720, 1000, step=30, ang=-0.25, w=2, opacity=0.15, length=70)
        if pillars:  # yuvarlak taş duvarlı alan (yamuk perspektif)
            o += f'<ellipse cx="960" cy="560" rx="330" ry="70" fill="{P["ground2"]}" opacity="0.6"/>'
            o += p.stroke([(640, 560), (700, 520), (960, 492), (1220, 520), (1280, 560)], w=16, color=P["stone2"], taper=0.05)
            for k, x in enumerate((700, 800, 1120, 1220)):
                o += self.obj("t_sutun", x, 560 + (10 if k in (0, 3) else -10), 0.42)
            o += self.obj("t_sutun", 905, 590, 0.62) + self.obj("t_sutun", 1015, 590, 0.62)
            o += p.stroke([(640, 560), (720, 600), (960, 630), (1200, 600), (1280, 560)], w=16, color=P["stone"], taper=0.05)
        o += self.ground_grass(560)
        return o

    def ground_grass(self, y):
        p = self.p; o = ""
        for i in range(26):
            x = p.r.random()*W; yy = y + 60 + p.r.random()*(H-y-80)
            for k in (-1, 0, 1):
                o += p.stroke([(x+k*6, yy), (x+k*12+p.jit(3), yy-16-p.r.random()*10)], w=3, color=self.P["ink"], taper=0.6, opacity=0.5)
        return o

    def l_tas_ocagi(self):
        P = self.P; p = self.p
        o = self.sky(P["sky"], P["sky2"], 420) + self.hills(380, P["hill"], 40, 1.0)
        o += self.fill([(-40, 420), (W+40, 410), (W+40, H+40), (-40, H+40)], "#d9cbb5", smooth=False)
        o += p.hatch(0, 440, W, H, step=24, ang=-0.15, w=2, opacity=0.18, length=90)
        # yerde yatan, yarım kalmış T sütun (kaya içinde oyulmuş)
        o += self.fill([(330, 760), (1430, 735), (1440, 840), (340, 870)], "#c7b9a2", smooth=False)
        o += self.fill([(1430, 650), (1640, 640), (1650, 940), (1440, 950)], "#c7b9a2", smooth=False)
        o += p.stroke([(320, 755), (1435, 728), (1445, 645), (1650, 635), (1660, 948), (1438, 958), (1448, 848), (335, 878), (320, 755)], w=8, taper=0.01, smooth=False)
        for x in range(360, 1420, 70): o += p.stroke([(x, 770), (x+20, 860)], w=3, opacity=0.35)
        o += p.stroke([(300, 740), (300, 900)], w=0)
        return o

    def l_kazi_alani(self, house=False, channel=False):
        P = self.P; p = self.p
        o = self.sky(P["sky"], P["sky2"], 420) + self.hills(400, P["hill"], 40, 2.2)
        o += self.fill([(-40, 430), (W+40, 420), (W+40, H+40), (-40, H+40)], P["ground"], smooth=False)
        # koruma çatısı
        o += self.fill([(150, 140), (1770, 140), (1830, 220), (90, 220)], "#e9ecee", smooth=False)
        for x in (180, 640, 1100, 1560, 1740): o += p.stroke([(x, 220), (x, 520)], w=10, color="#8d969e")
        # açma (hendek) + ip ızgarası
        o += self.fill([(300, 560), (1620, 560), (1700, 980), (220, 980)], P["ground2"], smooth=False)
        for x in range(300, 1700, 230): o += p.stroke([(x, 560), (x - 40 + (x-960)*0.06, 980)], w=2.5, color="#fff", opacity=0.8)
        o += p.stroke([(260, 770), (1660, 770)], w=2.5, color="#fff", opacity=0.8)
        if house: o += self.obj("ev_plani", 760, 900, 1.6)
        if channel:
            o += p.stroke([(1150, 620), (1250, 760), (1400, 900)], w=34, color="#7fb7c9", taper=0.05) + p.stroke([(1150, 620), (1250, 760), (1400, 900)], w=6, taper=0.05)
        return o

    def l_modern_oda(self):
        P = self.P
        o = f'<rect width="{W}" height="{H}" fill="{P["wall"]}"/>'
        o += self.fill([(-20, 800), (W+20, 790), (W+20, H+20), (-20, H+20)], P["floor"], smooth=False)
        for i in range(1, 9): o += self.p.stroke([(-20, 800+i*36), (W+20, 795+i*36)], w=2.5, opacity=0.25)
        o += self.window_city(1250, 170, 460, 400) + self.lamp(380, 800) + self.plant(1600, 860) + self.armchair(900, 900, P["sofa"])
        return o

    def l_laboratuvar(self):
        P = self.P; p = self.p
        o = f'<rect width="{W}" height="{H}" fill="#e7ece9"/>'
        for x in range(0, W, 120): o += p.stroke([(x, 0), (x, 640)], w=2, opacity=0.08)
        o += self.fill([(-20, 640), (W+20, 640), (W+20, 700), (-20, 700)], "#c9ced3", smooth=False)
        o += self.fill([(-20, 700), (W+20, 700), (W+20, H+20), (-20, H+20)], "#8d969e", smooth=False)
        o += self.obj("mikroskop", 1450, 640, 0.9) + self.obj("erlen", 1150, 640, 0.6) + self.obj("erlen", 1260, 640, 0.45)
        o += self.fill([(200, 120), (700, 120), (700, 420), (200, 420)], "#fffaf0", smooth=False)
        o += p.stroke([(240, 380), (330, 300), (430, 330), (530, 220), (660, 170)], w=6, color=P["red"])
        return o

    def l_kutuphane(self):
        P = self.P; p = self.p
        o = f'<rect width="{W}" height="{H}" fill="#efe0c8"/>'
        for sx in (120, 1320):
            o += self.fill([(sx, 120), (sx+480, 120), (sx+480, 900), (sx, 900)], "#8a5a3a", smooth=False)
            for row in range(4):
                y = 200 + row*180; x = sx + 20
                while x < sx + 450:
                    w = 24 + p.r.randint(0, 22); hgt = 110 + p.r.randint(0, 40)
                    col = (P["accent"], P["accent2"], P["cap"], P["hide"], "#d9b27c")[p.r.randint(0, 4)]
                    o += self.fill([(x, y+140-hgt), (x+w, y+140-hgt), (x+w, y+140), (x, y+140)], col, smooth=False); x += w + 4
                o += p.stroke([(sx, y+142), (sx+480, y+142)], w=8)
        o += self.fill([(-20, 900), (W+20, 900), (W+20, H+20), (-20, H+20)], P["floor"], smooth=False)
        o += self.fill([(700, 760), (1220, 760), (1220, 790), (700, 790)], "#6b4423", smooth=False) + self.lamp(780, 760)
        return o

    def l_gece_tepe(self):
        P = self.P; p = self.p
        o = f'<rect width="{W}" height="{H}" fill="{P["night"]}"/>'
        for i in range(90):
            x = p.r.random()*W; y = p.r.random()*600; r = 1 + p.r.random()*2.5
            o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity="{0.4+p.r.random()*0.6:.2f}"/>'
        o += f'<circle cx="1550" cy="180" r="60" fill="#f3ecd2"/><circle cx="1575" cy="165" r="56" fill="{P["night"]}"/>'
        o += self._hill(820, 520, P["night2"])
        for x in (800, 905, 1015, 1120): o += f'<g opacity="0.85">' + self.obj("t_sutun", x, 600, 0.45).replace(P["stone"], "#4a5670").replace(P["stone2"], "#2f3a52") + "</g>"
        return o

    def l_kesit(self, pct=5):
        """Tepenin enine kesiti: kazılmış kısım vs. gömülü kısım."""
        P = self.P; p = self.p
        o = self.sky(P["sky"], P["sky2"], 1000)
        top = [(x, 760 - 330*math.exp(-((x-960)/560)**2)) for x in range(-40, W+80, 60)]
        o += self.fill([(-40, H+40)] + top + [(W+40, H+40)], P["ground"])
        for k in range(1, 5):
            o += p.stroke([(x, y + k*70) for x, y in top], w=3, opacity=0.25)
        # gömülü sütunlar (silik)
        for x, yy in ((520, 860), (760, 800), (1180, 820), (1420, 880), (980, 940)):
            o += f'<g opacity="0.35">' + self.obj("t_sutun", x, yy, 0.42) + "</g>"
        # kazılmış dilim (~%5)
        o += self.fill([(900, 440), (1010, 440), (1010, 640), (900, 640)], P["paper"], smooth=False)
        o += self.obj("t_sutun", 955, 640, 0.5)
        return o

OBJECTS = ["t_sutun", "kabartma_tilki", "kabartma_domuz", "kabartma_akbaba", "kabartma_yilan", "cakmaktasi", "tas_kase", "mala", "firca", "kurek", "olcek",
           "parsomen", "mezar_tasi", "tekerlek", "balta", "bugday", "ev_plani", "buyutec", "erlen", "mikroskop", "ampul", "kum_saati", "kitap", "takvim",
           "telefon", "kahve", "laptop", "baret", "kalem", "saat"]
LOCATIONS = ["tepe", "tas_ocagi", "kazi_alani", "modern_oda", "laboratuvar", "kutuphane", "gece_tepe", "kesit", "beyaz_kart"]
