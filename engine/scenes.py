"""scenes.py - sahne şablonları. Her şablon (palet, yön) alır; arka plan işleme yöne göre değişir.
A: konturlu + tarama   B: konturuz düz vektör + yumuşak gölge   C: kalın kontur + gouache katmanları"""
import math
from ink import Pen, paper_defs

FONTS = {  # yön -> (başlık fontu, ağırlık, etiket fontu)
  "A": ("Shantell", 700, "Shantell", 500),
  "B": ("KalamB", 700, "Mali", 600),
  "C": ("Playpen", 800, "Baloo", 700),
}
W, H = 1920, 1080

class Scene:
    def __init__(self, P, style, seed=21):
        self.P = P; self.s = style; self.p = Pen(seed, wobble=1.0 if style != "B" else 0.5)
        self.lw = {"A": 5, "B": 0, "C": 8}[style]
    # --- stil uyarlamalı dolgu ---
    def fill(self, pts, col, line=True, smooth=True):
        p = self.p
        if self.s == "C":
            out = p.shape(pts, col, w=0, smooth=smooth)
            # gouache: iki yarı saydam kayık katman
            for dx, dy, op in ((6, -4, 0.10), (-5, 6, 0.08)):
                out += p.shape([(x+dx, y+dy) for x, y in pts], "#ffffff" if op > 0.09 else "#000000", w=0, smooth=smooth).replace("/>", f' opacity="{op}"/>', 1)
            if line: out += p.shape(pts, "none", w=self.lw, smooth=smooth)
            return out
        if self.s == "B":
            return p.shape(pts, col, w=0, smooth=smooth)
        return p.shape(pts, col, w=self.lw if line else 0, smooth=smooth)

    def defs(self):
        warm = self.s != "B"
        strength = {"A": 0.10, "B": 0.05, "C": 0.16}[self.s]
        return f"<defs>{paper_defs('paper', 0.85, strength, warm)}</defs>"
    def grain(self):
        return f'<rect width="{W}" height="{H}" fill="#888" filter="url(#paper)" opacity="1"/>'

    def font(self, kind="head"):
        f = FONTS[self.s]
        return (f[0], f[1]) if kind == "head" else (f[2], f[3])

    def text(self, x, y, s, size, col=None, kind="head", anchor="middle", ls=None):
        fam, wt = self.font(kind)
        col = col or self.P["ink"]
        ls = ls if ls is not None else (2 if kind == "head" else 0)
        return (f'<text x="{x}" y="{y}" font-family="{fam}" font-weight="{wt}" font-size="{size}" fill="{col}" '
                f'text-anchor="{anchor}" letter-spacing="{ls}" lang="tr">{s}</text>')

    # ===================== öğeler =====================
    def sky(self, top, bot, y1=650):
        return (f'<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
                f'<stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="{W}" height="{y1+40}" fill="url(#sk)"/>')

    def hills(self, y, col, amp=60, seed_shift=0, line=True):
        p = self.p; pts = [(-40, H)]
        for i in range(0, 21):
            x = -40 + i*100
            pts.append((x, y - amp*(0.5+0.5*math.sin(i*0.9+seed_shift)) + p.jit(10)))
        pts += [(W+40, H)]
        return self.fill(pts, col, line=line)

    def ground(self, y, col, col2):
        p = self.p; P = self.P
        pts = [(-40, y+10)] + [(x, y + p.jit(6) + 8*math.sin(x/260)) for x in range(0, W+80, 120)] + [(W+40, H+40), (-40, H+40)]
        out = self.fill(pts, col)
        if self.s == "A":
            out += p.hatch(0, y+40, W, H-20, step=26, ang=-0.25, w=2.2, color=P["ink"], opacity=0.18, length=70)
        elif self.s == "C":
            for i in range(28):
                x = p.r.random()*W; yy = y + 60 + p.r.random()*(H-y-80)
                out += p.blob(x, yy, 60+p.r.random()*90, 10+p.r.random()*10, col2, line=None, w=0).replace("/>", ' opacity="0.35"/>', 1)
        else:
            out += f'<rect x="0" y="{y+150}" width="{W}" height="{H-y}" fill="{col2}" opacity="0.35"/>'
        # çim tutamları
        for i in range(34):
            x = p.r.random()*W; yy = y + 20 + p.r.random()*(H-y-40)
            for k in (-1, 0, 1):
                out += p.stroke([(x+k*6, yy), (x+k*12+p.jit(3), yy-18-p.r.random()*12)], w=3 if self.s != "C" else 4,
                                color=P["ink"] if self.s != "B" else col2, taper=0.6, opacity=0.6 if self.s != "B" else 0.9)
        return out

    def pillar(self, x, y, s=1.0, carve=True):
        """T biçimli taş sütun (Anadolu Neolitik esinli, kendi çizimimiz)."""
        P = self.P; p = self.p
        stem = [(x-34*s, y), (x-30*s, y-260*s), (x+30*s, y-260*s), (x+34*s, y)]
        top = [(x-95*s, y-250*s), (x-92*s, y-320*s), (x+92*s, y-322*s), (x+95*s, y-252*s)]
        out = self.fill(stem, P["stone"], smooth=False) + self.fill(top, P["stone"], smooth=False)
        out += f'<path d="M{x+8*s},{y} L{x+6*s},{y-255*s} L{x+29*s},{y-257*s} L{x+33*s},{y}Z" fill="{P["stone2"]}" opacity="0.5"/>'
        out += f'<path d="M{x-92*s},{y-262*s} L{x+94*s},{y-264*s} L{x+95*s},{y-252*s} L{x-95*s},{y-250*s}Z" fill="{P["stone2"]}" opacity="0.5"/>'
        if carve:  # kabartma: kendi tasarımımız tilki silueti (basit)
            out += p.stroke([(x-18*s, y-200*s), (x+4*s, y-190*s), (x+16*s, y-170*s), (x-2*s, y-150*s), (x-20*s, y-160*s)], w=4*s, color=P["stone2"], taper=0.2)
            out += p.stroke([(x-60*s, y-292*s), (x+60*s, y-290*s)], w=3*s, color=P["stone2"], taper=0.2)
        return out

    def hut(self, x, y, s=1.0):
        P = self.P; p = self.p
        wall = p.blob_pts(x, y-60*s, 120*s, 70*s, n=30, amp=0.02, power=2.8)
        wall = [pt for pt in wall if pt[1] >= y-110*s] + [(x+120*s, y), (x-120*s, y)]
        out = self.fill([(x-118*s, y), (x-110*s, y-110*s), (x+110*s, y-112*s), (x+118*s, y)], P["hide"], smooth=False)
        out += self.fill([(x-150*s, y-100*s), (x, y-250*s), (x+150*s, y-100*s)], P["ground2"])
        out += self.fill([(x-26*s, y), (x-24*s, y-70*s), (x+24*s, y-72*s), (x+26*s, y)], P["hair"], smooth=False)
        if self.s != "B":
            out += p.hatch(x-130*s, y-235*s, x+130*s, y-110*s, step=13*s, ang=-1.9, w=2, color=P["ink"], opacity=0.3, length=60*s)
        else:
            out += f'<path d="M{x},{y-250*s} L{x+150*s},{y-100*s} L{x+40*s},{y-100*s}Z" fill="#000" opacity="0.10"/>'
        return out

    def fire(self, x, y, s=1.0):
        P = self.P; p = self.p
        out = ""
        for i in range(9):
            a = math.pi*(i/8)
            out += p.blob(x + math.cos(a)*85*s - 0, y + 8 + math.sin(a)*0, 26*s, 16*s, P["stone2"], w=self.lw*0.7 if self.lw else 0)
        outer = [(x-64*s, y), (x-70*s, y-45*s), (x-52*s, y-95*s), (x-38*s, y-60*s), (x-20*s, y-130*s), (x-2*s, y-185*s),
                 (x+14*s, y-120*s), (x+30*s, y-80*s), (x+48*s, y-140*s), (x+66*s, y-60*s), (x+64*s, y)]
        out += self.fill(outer, P["fire"])
        inner = [(x-38*s, y-2), (x-34*s, y-50*s), (x-14*s, y-70*s), (x+0*s, y-115*s), (x+14*s, y-62*s), (x+30*s, y-75*s), (x+40*s, y-2)]
        out += p.shape(inner, P["fire2"], w=0)
        for k, (ex, ey) in enumerate(((-30, -230), (40, -250), (8, -280))):
            out += p.blob(x+ex*s, y+ey*s, 6*s, 9*s, P["fire"], line=None, w=0)
        for k in (-1, 1):
            out += p.stroke([(x+k*55*s, y+6), (x-k*45*s, y-18*s)], w=12*s, color=P["hair"], taper=0.1)
        return out

    def sun(self, x, y, r=70):
        P = self.P
        return f'<circle cx="{x}" cy="{y}" r="{r*1.7}" fill="{P["fire2"]}" opacity="0.22"/>' + self.p.blob(x, y, r, r, P["fire2"], line=P["ink"] if self.s != "B" else None, w=self.lw*0.8)

    def window_city(self, x, y, w, h):
        P = self.P; p = self.p
        out = self.fill([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], P["sky"], smooth=False)
        for i in range(6):
            bw = w/6; bh = 60 + (i*37 % 110)
            out += f'<rect x="{x+i*bw+6}" y="{y+h-bh}" width="{bw-12}" height="{bh}" fill="{P["accent2"] if i%2 else P["cap"]}" opacity="0.55"/>'
        out += p.stroke([(x+w/2, y), (x+w/2, y+h)], w=6) + p.stroke([(x, y+h/2), (x+w, y+h/2)], w=6)
        for a, b in (((x, y), (x+w, y)), ((x+w, y), (x+w, y+h)), ((x+w, y+h), (x, y+h)), ((x, y+h), (x, y))):
            out += p.stroke([a, b], w=10, taper=0.02)
        out += f'<rect x="{x-14}" y="{y+h}" width="{w+28}" height="18" fill="{P["paper"]}"/>' + p.stroke([(x-14, y+h+18), (x+w+14, y+h+18)], w=6, taper=0.02)
        return out

    def armchair(self, x, y, col):
        P = self.P
        out = self.fill([(x-170, y-240), (x+170, y-240), (x+180, y-60), (x-180, y-60)], col)
        out += self.fill([(x-230, y-150), (x-160, y-160), (x-150, y), (x-225, y)], col)
        out += self.fill([(x+160, y-160), (x+230, y-150), (x+225, y), (x+150, y)], col)
        out += self.fill([(x-160, y-90), (x+160, y-90), (x+165, y), (x-165, y)], col)
        out += f'<rect x="{x-170}" y="{y-90}" width="340" height="90" fill="#000" opacity="0.10"/>'
        for k in (-1, 1): out += self.p.stroke([(x+k*190, y), (x+k*195, y+40)], w=10)
        return out

    def lamp(self, x, y):
        P = self.P
        out = self.p.stroke([(x, y), (x, y-300)], w=7)
        out += self.fill([(x-70, y-300), (x-45, y-400), (x+45, y-400), (x+70, y-300)], P["fire2"], smooth=False)
        out += f'<ellipse cx="{x}" cy="{y-260}" rx="160" ry="120" fill="{P["fire2"]}" opacity="0.18"/>'
        out += self.p.blob(x, y+4, 50, 10, P["ink"], line=None, w=0)
        return out

    def plant(self, x, y):
        P = self.P; p = self.p
        out = ""
        for a in (-0.9, -0.5, -0.15, 0.2, 0.55, 0.95):
            tip = (x + math.sin(a)*130, y - 120 - math.cos(a)*90)
            leaf = [(x, y-60), ((x+tip[0])/2 - 22, (y-60+tip[1])/2), tip, ((x+tip[0])/2 + 22, (y-60+tip[1])/2)]
            out += self.fill(leaf, P["green"])
        out += self.fill([(x-55, y-70), (x+55, y-70), (x+42, y), (x-42, y)], P["accent"], smooth=False)
        return out

    def phone(self, x, y, s=1):
        P = self.P
        return self.p.shape([(x-22*s, y-38*s), (x+22*s, y-38*s), (x+22*s, y+38*s), (x-22*s, y+38*s)], P["ink"], w=0, smooth=False) + \
               f'<rect x="{x-16*s}" y="{y-30*s}" width="{32*s}" height="{58*s}" rx="4" fill="{P["accent2"]}" opacity="0.9"/>'

    def pin(self, x, y, col):
        p = self.p
        return p.shape([(x, y), (x-30, y-50), (x-30, y-82), (x, y-104), (x+30, y-82), (x+30, y-50)], col, w=6) + \
               p.blob(x, y-72, 12, 12, "#fff", w=4)

    def red_circle(self, x, y, rx, ry):
        p = self.p; pts = []
        for i in range(30):
            a = -0.4 + 2*math.pi*1.08*i/29
            pts.append((x + rx*math.cos(a)*(1+0.02*i/29), y + ry*math.sin(a)*(1+0.03*i/29)))
        return p.stroke(pts, w=9, color=self.P["red"], taper=0.15, press=0.25)

    def red_x(self, cx, cy, s):
        p = self.p; c = self.P["red"]
        return p.stroke([(cx-s, cy-s*0.8), (cx+s, cy+s*0.85)], w=16, color=c, taper=0.15) + \
               p.stroke([(cx+s*0.95, cy-s*0.85), (cx-s*1.02, cy+s*0.8)], w=16, color=c, taper=0.15)
