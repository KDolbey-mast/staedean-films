"""THE CAST line-up banner. MS_STYLE=marker python3 lineup.py out_dir"""
import os, sys
os.environ.setdefault("MS_STYLE", "marker")
import cast, film2
from story import *
from render import render
OUT = sys.argv[1] if len(sys.argv) > 1 else "lineup"
CT = 640  # counter top
art = text(80, 110, "THE CAST", size=72, anchor="start", family="Georgia, serif")
art += path("M 80,134 C 260,126 420,128 520,134", sw=6, stroke="#17c8be")
art += text(82, 178, "Mount Staedean  ·  The Door", size=28, anchor="start", weight="normal", family="Georgia, serif")
# the counter with the four officials and their plaques
for x, dept in [(760, "planning"), (960, "qa"), (1160, "customer success"), (1360, "product owner")]:
    art += cast.official(dept, x, CT, s=0.55, gesture="rest")
art += washed(f"M 640,{CT} L 1480,{CT} L 1480,1010 L 640,1010 Z", "#c4a77c", off=(3, 2))
art += path(f"M 640,{CT + 130} L 1480,{CT + 130} M 640,{CT + 250} L 1480,{CT + 250}", sw=2)
# awning
art += path("M 660,330 L 660,{0} M 1460,330 L 1460,{0}".format(CT), sw=3)
sc = "M 620,300 L 1500,300 L 1500,350 " + " ".join(f"Q {1500 - 55 - 110 * k},400 {1500 - 110 * (k + 1)},350" for k in range(8)) + " Z"
art += washed(sc, "#17c8be", off=(3, 2))
for x, lines in [(760, ("PLANNING",)), (960, ("QA",)), (1160, ("CUSTOMER", "SUCCESS")), (1360, ("PRODUCT", "OWNER"))]:
    art += washed(f"M {x - 86},{CT + 30} L {x + 86},{CT + 30} L {x + 86},{CT + 92} L {x - 86},{CT + 92} Z", "#fbf7ee", sw=2.6, off=(2, 1))
    art += (text(x, CT + 70, lines[0], size=20) if len(lines) == 1 else text(x, CT + 58, lines[0], size=16) + text(x, CT + 82, lines[1], size=16))
art += path("M 40,1010 L 1880,1010", sw=2.4)
# front row
art += cast.pm(300, 1016, s=0.46, pose="stand", mood="delighted", bulb=1.0)
art += cast.maker(560, 1016, s=0.42, mood="hopeful")
art += cast.customer(1610, 1010, s=0.5, pose="wave", mood="happy")
for i, pal in enumerate(film2.QUEUE[:3]):
    art += cast.customer(1740 + i * 62, 1010, s=0.36 - i * 0.02, pose="phone", mood="happy", palette=pal, coffee=False)
for x, t in [(300, "the PM"), (560, "the Maker"), (1610, "the customer")]:
    art += text(x, 1050, t, size=24, weight="normal", family="Georgia, serif")
art += text(1060, 1050, "the officials", size=24, weight="normal", family="Georgia, serif")
render([("the_cast", cast.frame(art))], OUT)
