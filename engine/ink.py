"""ink.py - el çizimi hissi veren SVG ilkel öğeleri (değişken kalınlıklı fırça, dalgalı formlar).
Bağımlılık yok (yalnızca standart kütüphane). Tüm rastgelelik tohumlu -> tekrar üretilebilir."""
import math, random

class Pen:
    def __init__(self, seed=1, wobble=1.0):
        self.r = random.Random(seed); self.wobble = wobble

    # ---------- yardımcılar ----------
    @staticmethod
    def catmull(pts, n=12, closed=False):
        P = list(pts)
        if closed: P = [P[-1]] + P + [P[0], P[1]]
        else: P = [P[0]] + P + [P[-1]]
        out = []
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i-1], P[i], P[i+1], P[i+2]
            for k in range(n):
                t = k / n; t2 = t*t; t3 = t2*t
                x = 0.5*((2*p1[0]) + (-p0[0]+p2[0])*t + (2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2 + (-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3)
                y = 0.5*((2*p1[1]) + (-p0[1]+p2[1])*t + (2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2 + (-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3)
                out.append((x, y))
        if not closed: out.append(P[-2])
        return out

    @staticmethod
    def fmt(pts):
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"

    def jit(self, a):
        return (self.r.random()*2 - 1) * a * self.wobble

    # ---------- fırça darbesi ----------
    def stroke(self, pts, w=6, color="#1d1a17", taper=0.22, smooth=True, press=0.18, n=10, opacity=1, rough=0.6):
        pts = [(x + self.jit(rough), y + self.jit(rough)) for x, y in pts]
        S = self.catmull(pts, n) if smooth and len(pts) > 2 else pts
        if len(S) < 2: return ""
        if len(S) == 2:
            (x0, y0), (x1, y1) = S; S = [(x0+(x1-x0)*t/8, y0+(y1-y0)*t/8) for t in range(9)]
        L = [0.0]
        for i in range(1, len(S)): L.append(L[-1] + math.dist(S[i-1], S[i]))
        tot = L[-1] or 1
        ph = self.r.random()*6.28; f = 1.5 + self.r.random()*2
        left, right = [], []
        for i, (x, y) in enumerate(S):
            a = S[max(0, i-1)]; b = S[min(len(S)-1, i+1)]
            dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
            nx, ny = -dy/d, dx/d
            t = L[i]/tot
            tp = 1.0
            if taper > 0: tp = min(1.0, (t/taper)**0.55 if t < taper else 1, ((1-t)/taper)**0.55 if t > 1-taper else 1)
            ww = w * max(0.18, tp) * (1 + press*math.sin(ph + t*f*math.pi*2))
            left.append((x + nx*ww/2, y + ny*ww/2)); right.append((x - nx*ww/2, y - ny*ww/2))
        poly = left + right[::-1]
        op = f' opacity="{opacity}"' if opacity != 1 else ""
        return f'<path d="{self.fmt(poly)}" fill="{color}"{op}/>'

    # ---------- dalgalı kapalı form ----------
    def blob_pts(self, cx, cy, rx, ry, n=48, amp=0.012, squash=None, rot=0, power=2.0):
        ph = [self.r.random()*6.28 for _ in range(3)]
        pts = []
        for i in range(n):
            a = 2*math.pi*i/n
            c, s = math.cos(a), math.sin(a)
            # süperelips (power>2 -> köşeli)
            ex = math.copysign(abs(c)**(2/power), c); ey = math.copysign(abs(s)**(2/power), s)
            k = 1 + amp*self.wobble*(math.sin(2*a+ph[0]) + 0.6*math.sin(3*a+ph[1]) + 0.3*math.sin(5*a+ph[2]))
            x, y = ex*rx*k, ey*ry*k
            if squash: x *= 1 + squash*(-s)  # üst dar / alt geniş (yumurta)
            xr = x*math.cos(rot) - y*math.sin(rot); yr = x*math.sin(rot) + y*math.cos(rot)
            pts.append((cx+xr, cy+yr))
        return pts

    def shape(self, pts, fill, line="#1d1a17", w=6, closed=True, smooth=True, extra=""):
        S = self.catmull(pts, 6, closed=True) if smooth else pts
        out = f'<path d="{self.fmt(S)}" fill="{fill}" {extra}/>'
        if line and w > 0:
            ring = pts + pts[:3]
            out += self.stroke(ring, w=w, color=line, taper=0.03, press=0.22, n=6, rough=0.3, smooth=smooth)
        return out

    def blob(self, cx, cy, rx, ry, fill, line="#1d1a17", w=6, **kw):
        return self.shape(self.blob_pts(cx, cy, rx, ry, **kw), fill, line, w)

    def hatch(self, x0, y0, x1, y1, step=14, ang=-0.9, w=2, color="#1d1a17", opacity=0.35, clip=None, length=None):
        out = []
        dx, dy = math.cos(ang), math.sin(ang)
        L = length or math.hypot(x1-x0, y1-y0)
        x = x0
        while x < x1:
            y = y0 + self.r.random()*(y1-y0)
            l = L*(0.25+self.r.random()*0.35)
            out.append(self.stroke([(x, y), (x+dx*l, y+dy*l)], w=w, color=color, taper=0.4, press=0.1, opacity=opacity, rough=1.2))
            x += step*(0.6+self.r.random()*0.8)
        g = "".join(out)
        return f'<g clip-path="url(#{clip})">{g}</g>' if clip else g


def paper_defs(fid="paper", base_freq=0.9, strength=0.08, warm=True):
    """Kâğıt grenini SVG filtresi olarak tanımlar (Chrome render eder)."""
    tint = "0.12 0.10 0.06" if warm else "0.08 0.09 0.11"
    return f'''<filter id="{fid}" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="{base_freq}" numOctaves="3" seed="7" result="n"/>
      <feColorMatrix type="matrix" values="0 0 0 0 {tint.split()[0]}  0 0 0 0 {tint.split()[1]}  0 0 0 0 {tint.split()[2]}  0 0 0 {strength*2.2} -{strength*0.9}" in="n" result="g"/>
      <feComposite in="g" in2="SourceGraphic" operator="in"/>
    </filter>'''
