"""Fasulye tekil şeffaf PNG varlıkları: görünüm×kostüm ve ifade seti."""
import os
from fasulye import Fasulye, EXPR2, COSTUMES
from palettes import A
from render import render
F = Fasulye(A); jobs = []
os.makedirs("boards/fasulye/objects", exist_ok=True)
for v in ("front", "tq", "side", "back"):
    for c in COSTUMES:
        jobs.append((F.g(256, 600, 1.0, costume=c, view=v, seed=7), f"boards/fasulye/objects/fasulye_{v}_{c}.png", 512, 640))
for e in EXPR2:
    jobs.append((F.g(256, 600, 1.0, expr=e, view="front", seed=7), f"boards/fasulye/objects/fasulye_ifade_{e}.png", 512, 640))
render(jobs, transparent=True); print(len(jobs))
