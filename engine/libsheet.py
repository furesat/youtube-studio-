from library import Lib, OBJECTS, LOCATIONS
from palettes import A
from render import render
L = Lib(A)
def T(x, y, s, size=22):
    return f'<text x="{x}" y="{y}" font-family="Shantell" font-weight="700" font-size="{size}" fill="#1D1A17" text-anchor="middle">{s}</text>'
o = f'<rect width="1920" height="1500" fill="{A["paper"]}"/>' + f'<text x="60" y="80" font-family="Shantell" font-weight="800" font-size="44" fill="#1D1A17">NESNE KÜTÜPHANESİ (30) — tarih · bilim · gündelik</text>'
for k, n in enumerate(OBJECTS):
    r, c = divmod(k, 8); x = 140 + c*235; y = 380 + r*330
    sc = 0.62 if n.startswith("kabartma") else (0.42 if n in ("t_sutun",) else 0.85)
    if n.startswith("kabartma"): o += L.obj(n, x, y - 90, 0.5)
    elif n == "ev_plani": o += L.obj(n, x, y, 0.6)
    elif n == "olcek": o += L.obj(n, x, y - 40, 0.65)
    else: o += L.obj(n, x, y, sc)
    o += T(x, y + 50, n)
jobs = [(o, "boards/library/01_nesneler.png", 1920, 1500)]
for n in OBJECTS:   # tekil şeffaf nesneler
    s = 1.6 if n not in ("t_sutun",) else 1.0
    y = 420 if not n.startswith("kabartma") else 260
    jobs.append((L.obj(n, 256, y, s if not n.startswith("kabartma") else 1.0) if n != "ev_plani" else L.obj(n, 256, 330, 1.3), f"boards/library/objects/{n}.png", 512, 512))
for n in LOCATIONS:
    jobs.append((L.loc(n), f"boards/library/locations/{n}.png", 1920, 1080))
render(jobs, transparent=True)
