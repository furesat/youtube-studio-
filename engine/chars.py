"""chars.py - üç özgün karakter ailesi (A: Fasulye, B: Gözlük, C: Topak).
Ortak poz + ifade + kostüm sistemi. Çıktı: SVG <g> metni."""
import math
from ink import Pen

INK = "#1d1a17"

# ---------------- ifade tanımları ----------------
EXPR = {
  "nötr":     dict(brow=(0, 0, 0),     eye="open", pupil=(0, 0),    mouth="smile0"),
  "mutlu":    dict(brow=(-0.15, 0.15, 4), eye="happy", pupil=(0, 0), mouth="grin"),
  "şaşkın":   dict(brow=(-0.25, 0.25, 14), eye="wide", pupil=(0, 0), mouth="o"),
  "endişeli": dict(brow=(0.35, -0.35, 6), eye="open", pupil=(0, 2),  mouth="wavy"),
  "kurnaz":   dict(brow=(0.3, 0.05, -2),  eye="half", pupil=(5, 0),  mouth="smirk"),
  "öfkeli":   dict(brow=(0.5, -0.5, -6),  eye="open", pupil=(0, 0),  mouth="frown"),
  "uykulu":   dict(brow=(0, 0, -3),       eye="closed", pupil=(0, 0), mouth="flat"),
  "düşünceli":dict(brow=(-0.2, 0.35, 6),  eye="open", pupil=(-5, -6), mouth="flat_side"),
}

# ---------------- pozlar (omuza göre dirsek, el) ----------------
# değerler kol uzunluğu birimi (1.0 = tam kol)
POSE = {
  "duruş":   dict(L=[(-0.18, 0.5), (-0.25, 1.0)],  R=[(0.18, 0.5), (0.25, 1.0)],  legs="stand"),
  "el_salla":dict(L=[(-0.18, 0.5), (-0.25, 1.0)],  R=[(0.45, -0.25), (0.55, -0.85)], legs="stand"),
  "göster":  dict(L=[(-0.18, 0.5), (-0.22, 1.0)],  R=[(0.5, 0.05), (1.0, -0.05)], legs="stand"),
  "omuz":    dict(L=[(-0.5, 0.25), (-0.75, -0.2)], R=[(0.5, 0.25), (0.75, -0.2)], legs="stand"),
  "taşı":    dict(L=[(-0.15, 0.45), (0.25, 0.6)],  R=[(0.15, 0.45), (-0.25, 0.6)], legs="stand"),
  "düşün":   dict(L=[(-0.18, 0.5), (-0.25, 1.0)],  R=[(0.35, 0.35), (0.05, -0.15)], legs="stand"),
  "koş":     dict(L=[(-0.45, 0.2), (-0.3, -0.35)], R=[(0.45, 0.35), (0.75, 0.6)],  legs="run"),
  "otur":    dict(L=[(-0.18, 0.5), (0.05, 0.75)],  R=[(0.18, 0.5), (-0.05, 0.75)], legs="sit"),
}


class Character:
    """Alt sınıflar: body(), head_features(), hand(), foot(), costume katmanları."""
    arm_len = 150; leg_len = 100; limb_w = 7
    def __init__(self, seed=3):
        self.seed = seed

    def g(self, x, y, s=1.0, pose="duruş", expr="nötr", costume="modern", flip=False, seed=None):
        self.p = Pen(seed or self.seed)
        P = POSE[pose]; E = EXPR[expr]
        parts = []
        parts += self.back_layer(costume)
        parts += self.legs(P["legs"], costume)
        # arkadaki kol (sol) gövdenin arkasında
        parts += self.arm("L", P["L"], costume)
        parts += self.body(costume)
        parts += self.head(E, costume)
        parts += self.arm("R", P["R"], costume)
        tr = f'translate({x},{y}) scale({-s if flip else s},{s})'
        return f'<g transform="{tr}">' + "".join(parts) + "</g>"

    # ----- ortak uzuvlar -----
    def arm(self, side, spec, costume):
        sx, sy = self.shoulder(side)
        sgn = -1 if side == "L" else 1
        (ex, ey), (hx, hy) = spec
        A = self.arm_len
        E = (sx + ex*A, sy + ey*A); H = (sx + hx*A, sy + hy*A)
        out = [self.p.stroke([(sx, sy), ((sx+E[0])/2, (sy+E[1])/2 + 4), E, ((E[0]+H[0])/2, (E[1]+H[1])/2), H],
                             w=self.limb_w, color=self.limb_color(costume), taper=0.06, press=0.12)]
        out += self.sleeve(side, (sx, sy), E, costume)
        out.append(self.hand(H, math.atan2(H[1]-E[1], H[0]-E[0])))
        return out

    def sleeve(self, side, S, E, costume): return []
    def limb_color(self, costume): return INK
    def back_layer(self, costume): return []

    def legs(self, kind, costume):
        out = []
        for sgn in (-1, 1):
            hx, hy = self.hip(sgn)
            if kind == "stand":
                pts = [(hx, hy), (hx + sgn*4, hy + self.leg_len*0.5), (hx + sgn*8, hy + self.leg_len)]
            elif kind == "run":
                if sgn < 0: pts = [(hx, hy), (hx - 40, hy + self.leg_len*0.45), (hx - 70, hy + self.leg_len*0.8)]
                else: pts = [(hx, hy), (hx + 35, hy + self.leg_len*0.35), (hx + 30, hy + self.leg_len*0.95)]
            else:  # sit
                pts = [(hx, hy), (hx + sgn*10 + 50, hy + 6), (hx + sgn*10 + 55, hy + self.leg_len*0.75)]
            out.append(self.p.stroke(pts, w=self.limb_w, color=self.limb_color(costume), taper=0.05))
            out.append(self.foot(pts[-1], sgn))
        return out

    # ----- yüz -----
    def eyes(self, E, lx, rx, ey, size, sclera=True, pupil_r=None, lid_color=None):
        p = self.p; out = []
        pr = pupil_r or size*0.42
        for k, cx in enumerate((lx, rx)):
            kind = E["eye"]
            if kind in ("happy", "closed"):
                if kind == "happy":
                    out.append(p.stroke([(cx-size*0.8, ey+size*0.2), (cx, ey-size*0.55), (cx+size*0.8, ey+size*0.2)], w=size*0.28, taper=0.25))
                else:
                    out.append(p.stroke([(cx-size*0.8, ey), (cx, ey+size*0.35), (cx+size*0.8, ey)], w=size*0.24, taper=0.25))
                continue
            sc = 1.25 if kind == "wide" else 1.0
            if sclera:
                out.append(p.blob(cx, ey, size*0.85*sc, size*1.0*sc, "#fffdf8", w=size*0.16, amp=0.02))
            dx, dy = E["pupil"]
            r = pr*(0.8 if kind == "wide" else 1)
            out.append(p.blob(cx + dx*size/12, ey + dy*size/12 + (2 if sclera else 0), r, r*1.08, INK, line=None, w=0, amp=0.03))
            out.append(f'<circle cx="{cx + dx*size/12 - r*0.35:.1f}" cy="{ey + dy*size/12 - r*0.35:.1f}" r="{r*0.28:.1f}" fill="#fff"/>')
            if kind == "half":
                c = lid_color or self.skin
                out.append(p.shape([(cx-size*1.05, ey-size*1.2), (cx+size*1.05, ey-size*1.2), (cx+size*1.0, ey-size*0.05), (cx-size*1.0, ey-size*0.05)], c, w=0, smooth=False))
                out.append(p.stroke([(cx-size*0.95, ey-size*0.05), (cx, ey-size*0.12), (cx+size*0.95, ey-size*0.05)], w=size*0.2, taper=0.15))
        return out

    def brows(self, E, lx, rx, by, span, w):
        al, ar, lift = E["brow"]; out = []
        for cx, a in ((lx, al), (rx, ar)):
            dx = span*math.cos(a); dy = span*math.sin(a)
            out.append(self.p.stroke([(cx-dx, by - lift - dy), (cx, by - lift - 3), (cx+dx, by - lift + dy)], w=w, taper=0.35))
        return out

    def mouth(self, E, mx, my, s, w):
        p = self.p; t = E["mouth"]
        if t == "smile0": return [p.stroke([(mx-s, my), (mx, my+s*0.35), (mx+s, my-s*0.05)], w=w, taper=0.3)]
        if t == "flat": return [p.stroke([(mx-s*0.7, my+2), (mx+s*0.7, my)], w=w, taper=0.3)]
        if t == "flat_side": return [p.stroke([(mx-s*0.2, my+3), (mx+s*0.8, my-2)], w=w, taper=0.3)]
        if t == "frown": return [p.stroke([(mx-s*0.8, my+s*0.3), (mx, my-s*0.1), (mx+s*0.8, my+s*0.3)], w=w, taper=0.3)]
        if t == "smirk": return [p.stroke([(mx-s*0.7, my+s*0.1), (mx+s*0.3, my+s*0.15), (mx+s*0.9, my-s*0.35)], w=w, taper=0.3)]
        if t == "wavy": return [p.stroke([(mx-s*0.9, my+4), (mx-s*0.45, my-4), (mx, my+4), (mx+s*0.45, my-4), (mx+s*0.9, my+4)], w=w*0.85, taper=0.2)]
        if t == "o": return [p.blob(mx, my+s*0.2, s*0.38, s*0.5, "#5a2a22", w=w*0.8, amp=0.04)]
        if t == "grin":
            pts = [(mx-s, my-s*0.1), (mx+s, my-s*0.1), (mx+s*0.6, my+s*0.65), (mx, my+s*0.8), (mx-s*0.6, my+s*0.65)]
            return [p.shape(pts, "#5a2a22", w=w*0.8), p.blob(mx, my+s*0.55, s*0.45, s*0.2, "#e98a7c", line=None, w=0)]
        return []


# =====================================================================
# A — "FASULYE": baş+gövde tek yumurta, kâğıt beyazı; tek kıvrık perçem; atkı = imza
# =====================================================================
class Fasulye(Character):
    arm_len = 125; leg_len = 92; limb_w = 7.5
    skin = "#fffaf0"
    def __init__(self, palette, seed=3):
        super().__init__(seed); self.c = palette
    def shoulder(self, side): return (-92 if side == "L" else 92, -205)
    def hip(self, sgn): return (sgn*42, -92)
    def hand(self, H, ang):
        return self.p.blob(H[0], H[1], 13, 12, self.skin, w=5.5, amp=0.04)
    def foot(self, F, sgn):
        return self.p.blob(F[0] + sgn*10, F[1] + 4, 24, 11, INK, line=None, w=0, amp=0.04)
    def back_layer(self, costume):
        p = self.p; out = []
        if costume == "tarih_öncesi":   # dağınık saç kütlesi (arka)
            pts = []
            for i in range(26):
                a = math.pi*(1.05 + 0.9*i/25)
                r = 150 + (16 if i % 2 else -4) + p.jit(5)
                pts.append((r*math.cos(a), -300 + r*0.95*math.sin(a)))
            pts += [(118, -215), (-118, -215)]
            out.append(p.shape(pts, self.c["hair"], w=6))
        return out
    def body(self, costume):
        p = self.p; c = self.c; out = []
        egg = p.blob_pts(0, -262, 122, 172, n=60, amp=0.01, squash=0.12)
        out.append(p.shape(egg, self.skin, w=0, smooth=True))
        # sağ-alt gölge hilali
        sh = p.blob_pts(18, -246, 108, 158, n=60, amp=0.01, squash=0.12)
        out.append(f'<clipPath id="eg{self.seed}"><path d="{p.fmt(p.catmull(egg,6,True))}"/></clipPath>')
        out.append(f'<g clip-path="url(#eg{self.seed})"><path d="{p.fmt(p.catmull(egg,6,True))}" fill="{c["shade"]}"/>'
                   f'<path d="{p.fmt(p.catmull([(x-34,y-20) for x,y in sh],6,True))}" fill="{self.skin}"/></g>')
        out.append(p.shape(egg, "none", w=8))
        if costume == "modern":   # imza: düğümlü atkı
            out.append(p.shape([(-105, -205), (-40, -190), (40, -190), (105, -205), (100, -175), (40, -160), (-40, -160), (-100, -175)], c["accent"], w=5.5))
            out.append(p.shape([(30, -170), (62, -170), (78, -100), (48, -108)], c["accent"], w=5.5))
            out += [p.stroke([(-60, -180), (-20, -175)], w=2.5, color=INK, opacity=0.35), p.stroke([(5, -177), (45, -180)], w=2.5, color=INK, opacity=0.35)]
        elif costume == "tarih_öncesi":
            out.append(p.shape([(-118, -170), (118, -170), (112, -110), (60, -92), (0, -100), (-60, -90), (-114, -110)], c["hide"], w=5.5))
            out.append(p.hatch(-100, -165, 100, -100, step=11, ang=1.2, w=2, opacity=0.35, length=30))
            for i in range(5):   # örgü kemer
                x = -95 + i*45
                out.append(p.stroke([(x, -172), (x+25, -160), (x+45, -172)], w=4, color=c["accent2"]))
        elif costume == "1900":
            out.append(p.stroke([(-55, -200), (-40, -100)], w=9, color=c["accent2"]))
            out.append(p.stroke([(55, -200), (40, -100)], w=9, color=c["accent2"]))
            for bx in (-40, 40): out.append(p.blob(bx, -110, 6, 6, "#f2c14e", w=3))
        return out
    def head(self, E, costume):
        p = self.p; c = self.c; out = []
        # perçem / saç
        if costume == "modern":
            out.append(p.stroke([(-6, -432), (4, -462), (28, -470), (40, -452), (22, -440)], w=8, taper=0.3))
        elif costume == "tarih_öncesi":
            for i in range(9):
                x = -100 + i*25
                out.append(p.shape([(x-16, -380), (x+2, -448 - (i % 3)*8), (x+18, -380)], c["hair"], w=4.5))
            out.append(p.stroke([(-118, -392), (0, -405), (118, -392)], w=10, color=c["accent2"], taper=0.05))
        elif costume == "1900":
            out.append(p.shape([(-108, -380), (-95, -440), (0, -462), (95, -440), (112, -392), (150, -385), (150, -372), (-108, -368)], c["cap"], w=6))
            out.append(p.hatch(-90, -450, 100, -390, step=12, ang=0.6, w=2, opacity=0.3, length=24))
        out += self.brows(E, -42, 42, -366, 18, 6)
        out += self.eyes(E, -42, 42, -318, 30)
        out.append(p.blob(-78, -272, 15, 9, c["blush"], line=None, w=0, extra='opacity="0.55"') if False else "")
        out.append(f'<ellipse cx="-80" cy="-270" rx="16" ry="9" fill="{c["blush"]}" opacity="0.45"/><ellipse cx="80" cy="-270" rx="16" ry="9" fill="{c["blush"]}" opacity="0.45"/>')
        out += self.mouth(E, 0, -262, 26, 6)
        return out


# =====================================================================
# B — "GÖZLÜK": uzun boylu, yumuşak kare kafa, büyük yuvarlak gözlük; kazak = imza
# =====================================================================
class Gozluk(Character):
    arm_len = 150; leg_len = 150; limb_w = 7
    skin = "#f3d6b8"
    def __init__(self, palette, seed=5):
        super().__init__(seed); self.c = palette
    def shoulder(self, side): return (-62 if side == "L" else 62, -330)
    def hip(self, sgn): return (sgn*26, -152)
    def limb_color(self, costume): return INK
    def hand(self, H, ang): return self.p.blob(H[0], H[1], 13, 13, self.skin, w=5, amp=0.05)
    def foot(self, F, sgn): return self.p.shape([(F[0]-8, F[1]-8), (F[0]+sgn*30, F[1]-6), (F[0]+sgn*34, F[1]+6), (F[0]-10, F[1]+6)], INK, w=0)
    def sleeve(self, side, S, E, costume):
        col = {"modern": self.c["accent"], "tarih_öncesi": self.c["hide"], "1900": self.c["cap"]}[costume]
        m = (S[0]*0.25 + E[0]*0.75, S[1]*0.25 + E[1]*0.75)
        s0 = (S[0]*1.0 + (0 if side=="L" else 0), S[1] + 8)
        return [self.p.stroke([s0, m], w=38, color=INK, taper=0.06, press=0.04, rough=0.2),
                self.p.stroke([s0, m], w=27, color=col, taper=0.06, press=0.04, rough=0.2)]
    def body(self, costume):
        p = self.p; c = self.c; out = []
        col = {"modern": c["accent"], "tarih_öncesi": c["hide"], "1900": c["cap"]}[costume]
        torso = [(-58, -340), (58, -340), (66, -250), (64, -150), (-64, -150), (-66, -250)]
        out.append(p.shape(torso, col, w=6))
        if costume == "modern":
            out.append(p.stroke([(-30, -338), (0, -312), (30, -338)], w=5))
            for y in (-200, -185): out.append(p.stroke([(-60, y), (60, y)], w=3, color="#fff", opacity=0.55))
        elif costume == "tarih_öncesi":
            out.append(p.hatch(-55, -330, 55, -160, step=12, ang=1.25, w=2, opacity=0.35, length=34))
            out.append(p.shape([(-64, -155), (64, -155), (50, -122), (-50, -120)], c["hide"], w=5))
        elif costume == "1900":
            out.append(p.stroke([(0, -335), (0, -155)], w=3, opacity=0.6))
            for y in (-300, -260, -220, -180): out.append(f'<circle cx="0" cy="{y}" r="4" fill="{INK}"/>')
        return out
    def head(self, E, costume):
        p = self.p; c = self.c; out = []
        hd = p.blob_pts(0, -440, 100, 92, n=56, amp=0.012, power=3.2)
        if costume == "tarih_öncesi":
            pts = []
            for i in range(30):
                a = math.pi*(0.85 + 1.3*i/29)
                r = (128 if i % 2 else 108) + p.jit(6)
                pts.append((r*math.cos(a), -455 + r*0.9*math.sin(a)))
            pts += [(112, -360), (60, -400), (-60, -400), (-112, -360)]
            out.append(p.shape(pts, c["hair"], w=6))
        out.append(p.shape(hd, self.skin, w=7))
        if costume == "modern":
            out.append(p.shape([(-100, -470), (-92, -520), (-40, -540), (40, -540), (95, -515), (102, -468), (60, -490), (10, -478), (-40, -496)], c["hair"], w=6))
        elif costume == "tarih_öncesi":
            out.append(p.shape([(-102, -462), (-80, -520), (-20, -548), (50, -540), (100, -505), (104, -455), (70, -488), (30, -470), (-10, -492), (-50, -472)], c["hair"], w=6))
        elif costume == "1900":
            out.append(p.shape([(-104, -478), (-96, -532), (96, -532), (104, -478), (150, -470), (150, -458), (-104, -462)], c["cap"], w=6))
        out += self.brows(E, -40, 40, -485, 16, 6)
        out += self.eyes(E, -40, 40, -446, 20, sclera=False, pupil_r=8, lid_color=self.skin)
        # gözlük = imza (tarih öncesinde yok -> görsel şaka)
        if costume != "tarih_öncesi":
            for cx in (-40, 40): out.append(p.blob(cx, -446, 32, 30, "none", line=c["accent2"], w=6, amp=0.01))
            out.append(p.stroke([(-9, -448), (9, -448)], w=5, color=c["accent2"]))
        out.append(p.shape([(-2, -432), (-14, -400), (12, -398)], c["nose"], w=4.5))
        out += self.mouth(E, 0, -380, 22, 5.5)
        return out


# =====================================================================
# C — "TOPAK": iri kafa, kalın kontur, gouache doku; dalgalı saç bulutu = imza
# =====================================================================
class Topak(Character):
    arm_len = 92; leg_len = 62; limb_w = 9
    skin = "#fbe0c8"
    def __init__(self, palette, seed=9):
        super().__init__(seed); self.c = palette
    def shoulder(self, side): return (-78 if side == "L" else 78, -168)
    def hip(self, sgn): return (sgn*34, -62)
    def limb_color(self, costume): return INK
    def hand(self, H, ang): return self.p.blob(H[0], H[1], 15, 15, self.skin, w=6, amp=0.05)
    def foot(self, F, sgn): return self.p.blob(F[0] + sgn*8, F[1] + 2, 22, 13, INK, line=None, w=0)
    def body(self, costume):
        p = self.p; c = self.c; out = []
        col = {"modern": c["accent2"], "tarih_öncesi": c["hide"], "1900": c["cap"]}[costume]
        bell = [(-58, -205), (58, -205), (82, -120), (98, -58), (-98, -58), (-82, -120)]
        out.append(p.shape(bell, col, w=9))
        out.append(p.shape([(30, -195), (58, -200), (92, -62), (50, -60)], "#000", w=0, extra='opacity="0.12"'))
        if costume == "modern":
            out.append(p.blob(-28, -140, 14, 14, c["accent"], w=5))
        elif costume == "tarih_öncesi":
            out.append(p.hatch(-80, -195, 80, -65, step=13, ang=1.2, w=2.5, opacity=0.35, length=28))
            out.append(p.stroke([(-92, -105), (0, -94), (92, -105)], w=9, color=c["accent"]))
        elif costume == "1900":
            out.append(p.shape([(-20, -205), (20, -205), (8, -140), (-8, -140)], "#fff", w=4))
        return out
    def head(self, E, costume):
        p = self.p; c = self.c; out = []
        # saç bulutu (arka)
        if costume != "1900":
            hc = c["hair"] if costume == "modern" else c["hair2"]
            bumps = 9
            puffs = []
            for i in range(bumps):
                a = math.pi*(1.0 + i/(bumps-1))
                puffs.append((172*math.cos(a), -318 + 150*math.sin(a)))
            for (bx, by) in puffs: out.append(p.blob(bx, by, 48, 44, hc, w=9, amp=0.03))
            out.append(p.blob(0, -330, 160, 128, hc, line=None, w=0))
        hd = p.blob_pts(0, -305, 150, 128, n=60, amp=0.01)
        out.append(p.shape(hd, self.skin, w=0))
        out.append(f'<clipPath id="th{self.seed}"><path d="{p.fmt(p.catmull(hd,6,True))}"/></clipPath>')
        out.append(f'<g clip-path="url(#th{self.seed})"><ellipse cx="70" cy="-250" rx="150" ry="120" fill="#c9694a" opacity="0.13"/></g>')
        out.append(p.shape(hd, "none", w=10))
        if costume == "modern":
            out.append(p.shape([(-140, -350), (-90, -425), (0, -440), (90, -425), (140, -350), (80, -380), (20, -362), (-40, -385)], c["hair"], w=8))
        elif costume == "tarih_öncesi":
            out.append(p.shape([(-145, -345), (-100, -430), (0, -448), (100, -430), (145, -345), (70, -395), (0, -372), (-70, -398)], c["hair2"], w=8))
            out.append(p.blob(-96, -395, 22, 16, c["accent"], w=5))   # tüy/çiçek tokası
        elif costume == "1900":
            out.append(p.shape([(-150, -350), (-120, -430), (0, -448), (120, -430), (150, -350), (200, -340), (200, -326), (-150, -334)], c["cap"], w=9))
        out += self.brows(E, -48, 48, -345, 18, 9)
        out += self.eyes(E, -48, 48, -305, 16, sclera=False, pupil_r=14, lid_color=self.skin)
        out.append(f'<ellipse cx="-92" cy="-262" rx="26" ry="15" fill="{c["blush"]}" opacity="0.6"/><ellipse cx="92" cy="-262" rx="26" ry="15" fill="{c["blush"]}" opacity="0.6"/>')
        out += self.mouth(E, 0, -258, 22, 7)
        return out
