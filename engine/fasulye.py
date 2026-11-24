"""fasulye.py - ana karakter 'Fasulye' üretim sürümü.
Görünümler: front | tq (üç çeyrek, sağa bakar) | side (profil, sağa) | back.  flip=True -> sola bakar.
Daha olgun çizgi: az allık, gövdede mürekkep taraması, küçük göz bebeği seçeneği."""
import math
from ink import Pen
from chars import Character, EXPR, POSE, INK

EXPR2 = dict(EXPR)
EXPR2.update({
  "dehşet":   dict(brow=(-0.35, 0.35, 16), eye="wide", pupil=(0, 0), mouth="shout", pr=0.55),
  "gururlu":  dict(brow=(-0.25, 0.25, 8),  eye="happy", pupil=(0, 0), mouth="smile0"),
  "sıkılmış": dict(brow=(0.05, -0.05, -4), eye="half", pupil=(0, 3), mouth="flat"),
  "şüpheli":  dict(brow=(0.35, -0.2, 2),   eye="half", pupil=(6, 0), mouth="flat_side"),
  "kahkaha":  dict(brow=(-0.3, 0.3, 10),   eye="happy", pupil=(0, 0), mouth="grin"),
  "ağlamaklı":dict(brow=(0.45, -0.45, 8),  eye="open", pupil=(0, 4), mouth="wavy", pr=0.8),
  "yorgun":   dict(brow=(0.15, -0.15, -6), eye="half", pupil=(0, 4), mouth="frown"),
})
POSE2 = dict(POSE)
POSE2.update({
  "yüz_kapat":  dict(L=[(-0.18, 0.5), (-0.25, 1.0)], R=[(0.25, -0.05), (-0.5, -0.72)], legs="stand"),
  "eller_belde":dict(L=[(-0.5, 0.35), (0.25, 0.75)], R=[(0.5, 0.35), (-0.25, 0.75)], legs="stand"),
  "yukarı":     dict(L=[(-0.18, 0.5), (-0.25, 1.0)], R=[(0.12, -0.5), (0.18, -1.0)], legs="stand"),
  "it":         dict(L=[(0.35, 0.2), (0.85, 0.05)], R=[(0.45, 0.25), (0.95, 0.12)], legs="run"),
  "kaz":        dict(L=[(0.2, 0.45), (0.55, 0.85)], R=[(0.35, 0.4), (0.7, 0.8)], legs="stand"),
  "kaldır":     dict(L=[(-0.35, -0.3), (-0.1, -0.95)], R=[(0.35, -0.3), (0.1, -0.95)], legs="stand"),
  "pes":        dict(L=[(-0.1, 0.55), (-0.08, 1.05)], R=[(0.1, 0.55), (0.08, 1.05)], legs="stand"),
  "anlat":      dict(L=[(-0.4, 0.3), (-0.65, 0.05)], R=[(0.45, 0.3), (0.8, 0.1)], legs="stand"),
})
COSTUMES = ("modern", "tarih_öncesi", "arkeolog", "bilim", "1900")

VIEW = {   # yüz merkez kayması, uzak göz ölçeği, gövde genişliği
  "front": dict(fx=0,  far=1.0,  rx=122, sh=((-92, -205), (92, -205)), hips=(-42, 42)),
  "tq":    dict(fx=30, far=0.78, rx=116, sh=((-70, -208), (98, -205)), hips=(-30, 46)),
  "side":  dict(fx=40, far=0.0,  rx=108, sh=((-8, -210), (20, -205)),  hips=(-12, 18)),
  "back":  dict(fx=0,  far=None, rx=122, sh=((-92, -205), (92, -205)), hips=(-42, 42)),
}

class Fasulye(Character):
    arm_len = 125; leg_len = 92; limb_w = 7
    skin = "#fffaf0"
    def __init__(self, P, seed=3):
        super().__init__(seed); self.c = P

    def g(self, x, y, s=1.0, pose="duruş", expr="nötr", costume="modern", flip=False, seed=None, view="front"):
        self.p = Pen(seed or self.seed); self.view = view; self.V = VIEW[view]
        P = POSE2[pose]; E = EXPR2[expr]
        parts = []
        parts += self.back_layer(costume)
        parts += self.legs(P["legs"], costume)
        parts += self.arm("L", P["L"], costume)
        parts += self.body(costume)
        parts += self.head(E, costume)
        parts += self.front_layer(costume)
        parts += self.arm("R", P["R"], costume)
        tr = f'translate({x},{y}) scale({-s if flip else s},{s})'
        return f'<g transform="{tr}">' + "".join(parts) + "</g>"

    def shoulder(self, side): return self.V["sh"][0 if side == "L" else 1]
    def hip(self, sgn): return (self.V["hips"][0 if sgn < 0 else 1], -92)
    def hand(self, H, ang): return self.p.blob(H[0], H[1], 12.5, 11.5, self.skin, w=5, amp=0.05)
    def foot(self, F, sgn):
        d = 1 if self.view in ("side", "tq") else sgn
        if self.view == "back": d = sgn
        return self.p.blob(F[0] + d*11, F[1] + 4, 24, 10.5, INK, line=None, w=0, amp=0.04)

    def egg(self):
        return self.p.blob_pts(0, -262, self.V["rx"], 172, n=60, amp=0.01, squash=0.12)

    def back_layer(self, costume):
        p = self.p; c = self.c; out = []
        if costume == "tarih_öncesi":
            pts = []
            for i in range(26):
                a = math.pi*(1.05 + 0.9*i/25)
                r = 146 + (16 if i % 2 else -4) + p.jit(5)
                pts.append((r*math.cos(a)*self.V["rx"]/122, -300 + r*0.95*math.sin(a)))
            pts += [(112, -215), (-112, -215)]
            out.append(p.shape(pts, c["hair"], w=5.5))
        if costume == "modern" and self.view in ("side", "tq"):   # atkı ucu arkada uçuşur
            out.append(p.shape([(-60, -198), (-150, -178), (-168, -150), (-120, -160), (-70, -172)], c["accent"], w=5))
        return out

    def body(self, costume):
        p = self.p; c = self.c; out = []
        egg = self.egg(); E = p.fmt(p.catmull(egg, 6, True)); cid = f"eg{id(self)%9999}{p.r.randint(0,9999)}"
        out.append(f'<clipPath id="{cid}"><path d="{E}"/></clipPath>')
        out.append(f'<path d="{E}" fill="{self.skin}"/>')
        shx = -1 if self.view == "back" else 1
        out.append(f'<g clip-path="url(#{cid})"><ellipse cx="{shx*95}" cy="-230" rx="80" ry="190" fill="{c["shade"]}"/>')
        # mürekkep taraması (gölge tarafı) -> daha "editoryal" his
        out.append(p.hatch(shx*40 if shx > 0 else -130, -330, shx*130 if shx > 0 else -40, -110, step=10, ang=-1.15, w=1.8, color=INK, opacity=0.22, length=40))
        out.append("</g>")
        out.append(p.shape(egg, "none", w=7.5))
        if costume == "modern":
            if self.view == "back":
                out.append(p.shape([(-108, -205), (108, -205), (102, -175), (-102, -175)], c["accent"], w=5))
                out.append(p.shape([(-15, -185), (18, -185), (28, -105), (-6, -110)], c["accent"], w=5))
            else:
                k = {"front": 50, "tq": 72, "side": 78}[self.view]
                out.append(p.shape([(-self.V["rx"]+12, -205), (-40, -190), (40, -190), (self.V["rx"]-12, -205), (self.V["rx"]-18, -175), (40, -160), (-40, -160), (-self.V["rx"]+18, -175)], c["accent"], w=5))
                if self.view != "side":
                    out.append(p.shape([(k-20, -170), (k+12, -170), (k+26, -100), (k-4, -108)], c["accent"], w=5))
                out.append(p.stroke([(-60, -180), (-20, -175)], w=2.2, opacity=0.35) + p.stroke([(5, -177), (45, -180)], w=2.2, opacity=0.35))
        elif costume == "tarih_öncesi":
            rx = self.V["rx"]
            out.append(p.shape([(-rx+4, -170), (rx-4, -170), (rx-10, -110), (60, -92), (0, -100), (-60, -90), (-rx+8, -110)], c["hide"], w=5))
            out.append(p.hatch(-rx+20, -165, rx-20, -100, step=11, ang=1.2, w=1.8, opacity=0.35, length=30))
            for i in range(5):
                x = -95 + i*45
                if abs(x) < rx - 20: out.append(p.stroke([(x, -172), (x+25, -160), (x+45, -172)], w=3.5, color=c["accent2"]))
        elif costume == "arkeolog":
            rx = self.V["rx"]
            out.append(p.shape([(-rx+14, -212), (-30, -198), (-24, -92), (-rx+26, -104)], c["hide"], w=5, smooth=False))
            out.append(p.shape([(rx-14, -212), (30, -198), (24, -92), (rx-26, -104)], c["hide"], w=5, smooth=False))
            for sx in (-1, 1): out.append(p.shape([(sx*88, -168), (sx*50, -166), (sx*52, -136), (sx*86, -138)], c["hide"], w=3.5, smooth=False))
        elif costume == "bilim":
            rx = self.V["rx"]
            for sx in (-1, 1):
                out.append(p.shape([(sx*(rx-34), -214), (sx*(rx+4), -168), (sx*(rx+16), -62), (sx*16, -64), (sx*12, -150), (sx*30, -200)], "#ffffff", w=5, smooth=False))
                out.append(p.hatch(min(sx*(rx-10), sx*30), -190, max(sx*(rx-10), sx*30), -80, step=13, ang=1.3, w=1.5, opacity=0.18, length=30))
            out.append(p.stroke([(sx*0+62, -150), (66, -125)], w=4, color=c["accent2"]))
            out.append(p.shape([(46, -128), (78, -130), (80, -104), (48, -102)], "none", w=3))
        elif costume == "1900":
            out.append(p.stroke([(-55, -200), (-40, -100)], w=9, color=c["accent2"]))
            out.append(p.stroke([(55, -200), (40, -100)], w=9, color=c["accent2"]))
        return out

    def front_layer(self, costume): return []

    def head(self, E, costume):
        p = self.p; c = self.c; out = []; fx = self.V["fx"]; v = self.view
        # saç / şapka
        if costume in ("modern", "bilim"):
            tx = fx*0.4
            out.append(p.stroke([(tx-6, -432), (tx+4, -462), (tx+28, -470), (tx+40, -452), (tx+22, -440)], w=7.5, taper=0.3))
        if costume == "tarih_öncesi":
            for i in range(9):
                x = (-100 + i*25)*self.V["rx"]/122
                out.append(p.shape([(x-16, -380), (x+2, -448 - (i % 3)*8), (x+18, -380)], c["hair"], w=4.5))
            out.append(p.stroke([(-self.V["rx"], -392), (0, -405), (self.V["rx"], -392)], w=9, color=c["accent2"], taper=0.05))
        if costume == "arkeolog":
            o = fx*0.3
            out.append(p.shape([(-150+o, -402), (-100, -414), (-92, -470), (0, -490), (92, -470), (100, -414), (150+o, -402), (150+o, -390), (-150+o, -390)], c["hide"], w=6))
            out.append(p.stroke([(-96, -420), (96, -420)], w=8, color=c["hair"], taper=0.02))
        if costume == "1900":
            out.append(p.shape([(-108, -380), (-95, -440), (0, -462), (95, -440), (112, -392), (150, -385), (150, -372), (-108, -368)], c["cap"], w=6))
        if v == "back":
            return out
        # yüz
        out += self._face(E, fx)
        if costume == "bilim":   # alında koruyucu gözlük
            out.append(p.stroke([(-self.V["rx"]+6, -392), (self.V["rx"]-6, -392)], w=6, color=c["cap"]))
            for gx in (fx-34, fx+40):
                if v != "side" or gx > 0: out.append(p.blob(gx, -394, 26, 16, "#cfe6ea", w=5))
        return out

    def _face(self, E, fx):
        p = self.p; c = self.c; out = []; v = self.view
        size = 28; pr = E.get("pr", 1.0)
        near = fx + 40; far = fx - 40*(0.9 if v == "tq" else 1)
        eyes = [(near, 1.0)]
        if v != "side": eyes.insert(0, (far, self.V["far"]))
        for ex, sc in eyes:
            if sc <= 0: continue
            out += self._eye(E, ex, -318, size*sc, pr, squeeze=sc)
        # kaşlar
        al, ar, lift = E["brow"]
        for (ex, sc), a in zip(eyes, (al, ar) if len(eyes) == 2 else (ar,)):
            span = 17*sc
            out.append(p.stroke([(ex-span*math.cos(a), -364 - lift - span*math.sin(a)), (ex, -364 - lift - 3), (ex+span*math.cos(a), -364 - lift + span*math.sin(a))], w=5.5, taper=0.35))
        # allık (azaltıldı)
        for bx in ([near + 34] if v != "front" else [-78, 78]):
            out.append(f'<ellipse cx="{bx}" cy="-272" rx="14" ry="7" fill="{c["blush"]}" opacity="0.28"/>')
        mx = fx + (6 if v == "tq" else (30 if v == "side" else 0))
        out += self.mouth(E, mx, -262, 24*(0.85 if v == "side" else 1), 5.5)
        return out

    def _eye(self, E, cx, ey, size, pr, squeeze=1.0):
        p = self.p; kind = E["eye"]; out = []
        if kind in ("happy", "closed"):
            if kind == "happy":
                out.append(p.stroke([(cx-size*0.8, ey+size*0.2), (cx, ey-size*0.5), (cx+size*0.8, ey+size*0.2)], w=size*0.24, taper=0.25))
            else:
                out.append(p.stroke([(cx-size*0.8, ey), (cx, ey+size*0.3), (cx+size*0.8, ey)], w=size*0.22, taper=0.25))
            return out
        scw = 1.2 if kind == "wide" else 1.0
        out.append(p.blob(cx, ey, size*0.82*scw, size*0.98*scw, "#fffdf8", w=max(3, size*0.15), amp=0.02))
        dx, dy = E["pupil"]
        r = size*0.38*pr*(0.75 if kind == "wide" else 1)
        if self.view == "side": dx += 5
        if self.view == "tq": dx += 2
        px, py = cx + dx*size/12, ey + dy*size/12 + 2
        out.append(p.blob(px, py, r, r*1.08, INK, line=None, w=0, amp=0.03))
        out.append(f'<circle cx="{px - r*0.35:.1f}" cy="{py - r*0.35:.1f}" r="{r*0.26:.1f}" fill="#fff"/>')
        if kind == "half":
            out.append(p.shape([(cx-size*1.05, ey-size*1.2), (cx+size*1.05, ey-size*1.2), (cx+size*1.0, ey-size*0.05), (cx-size*1.0, ey-size*0.05)], self.skin, w=0, smooth=False))
            out.append(p.stroke([(cx-size*0.92, ey-size*0.05), (cx, ey-size*0.12), (cx+size*0.92, ey-size*0.05)], w=size*0.18, taper=0.15))
        return out

    def mouth(self, E, mx, my, s, w):
        if E["mouth"] == "shout":
            p = self.p
            pts = [(mx-s*0.7, my-s*0.2), (mx+s*0.7, my-s*0.2), (mx+s*0.55, my+s*0.9), (mx, my+s*1.15), (mx-s*0.55, my+s*0.9)]
            return [p.shape(pts, "#5a2a22", w=w*0.8), p.blob(mx, my+s*0.85, s*0.38, s*0.18, "#e98a7c", line=None, w=0)]
        return super().mouth(E, mx, my, s, w)

# ---------------- komik efektler (karakter başına göre) ----------------
def fx(kind, x, y, s=1.0, P=None, seed=5):
    """x,y = efektin merkezi (sahne koordinatı). s = ölçek."""
    p = Pen(seed); red = (P or {}).get("red", "#B83A2B"); out = []
    if kind == "ter":
        out.append(p.shape([(x, y-26*s), (x-13*s, y+4*s), (x, y+16*s), (x+13*s, y+4*s)], "#bfe3ee", w=4*s))
    elif kind == "şok":
        for a in (-2.6, -2.1, -1.57, -1.05, -0.5):
            out.append(p.stroke([(x+math.cos(a)*60*s, y+math.sin(a)*60*s), (x+math.cos(a)*100*s, y+math.sin(a)*100*s)], w=6*s, taper=0.3))
    elif kind == "soru":
        out.append(f'<text x="{x}" y="{y}" font-family="Shantell" font-weight="800" font-size="{110*s}" fill="{red}" text-anchor="middle">?</text>')
    elif kind == "ünlem":
        out.append(f'<text x="{x}" y="{y}" font-family="Shantell" font-weight="800" font-size="{120*s}" fill="{red}" text-anchor="middle">!</text>')
    elif kind == "parıltı":
        for dx, dy, r in ((0, 0, 1), (60, -40, 0.6), (-55, -30, 0.5)):
            cx, cy, R = x+dx*s, y+dy*s, 26*s*r
            out.append(p.shape([(cx, cy-R), (cx+R*0.25, cy-R*0.25), (cx+R, cy), (cx+R*0.25, cy+R*0.25), (cx, cy+R), (cx-R*0.25, cy+R*0.25), (cx-R, cy), (cx-R*0.25, cy-R*0.25)], "#FFD166", w=3*s, smooth=False))
    elif kind == "zzz":
        for i, z in enumerate(("z", "z", "Z")):
            out.append(f'<text x="{x+i*34*s}" y="{y-i*36*s}" font-family="Shantell" font-weight="800" font-size="{(40+i*14)*s}" fill="#1D1A17">{z}</text>')
    elif kind == "buhar":
        for dx in (-40, 40):
            out.append(p.blob(x+dx*s, y, 22*s, 16*s, "#ffffff", w=4*s) + p.blob(x+dx*1.4*s, y-28*s, 16*s, 12*s, "#ffffff", w=4*s))
    elif kind == "hız":
        for i in range(4):
            out.append(p.stroke([(x-140*s, y+i*26*s), (x-40*s - i*12*s, y+i*26*s)], w=5*s, taper=0.5, opacity=0.7))
    elif kind == "gözyaşı":
        out.append(p.shape([(x, y-14*s), (x-9*s, y+6*s), (x, y+14*s), (x+9*s, y+6*s)], "#9fd3e6", w=3*s))
    return "".join(out)
FX = ("ter", "şok", "soru", "ünlem", "parıltı", "zzz", "buhar", "hız", "gözyaşı")
