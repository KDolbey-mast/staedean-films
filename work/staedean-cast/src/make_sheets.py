"""Render the cast model sheets in the house style. Usage: MS_STYLE=marker python3 make_sheets.py [out_dir]"""
import os, sys
os.environ.setdefault("MS_STYLE", "marker")
import cast
import film2
from story import *
from render import render

OUT = sys.argv[1] if len(sys.argv) > 1 else "sheets"
INKC = "#2e2520"


def title(t, sub=""):
    return (text(70, 92, t, size=54, anchor="start", family="Georgia, serif")
            + (text(72, 136, sub, size=26, anchor="start", weight="normal", family="Georgia, serif") if sub else "")
            + path("M 70,112 C 400,104 800,106 1100,112", sw=3))


def label(x, y, t, size=24):
    return text(x, y, t, size=size, weight="normal", family="Georgia, serif")


def floor(y, x0=60, x1=1860):
    return path(f"M {x0},{y} L {x1},{y}", sw=2.4)


sheets = {}

# 1. the PM: expressions
art = title("THE PM: expressions", "Tousled brown hair, pale-blue shirt, rolled sleeves, Tangerine Orange tie. Pupils always visible.")
moods = list(cast.PM_MOODS)
for i, m in enumerate(moods):
    x, y = 220 + (i % 6) * 300, 380 + (i // 6) * 380
    art += cast.pm_head(x, y, 1.05, m) + label(x + 10, y + 190, m)
sheets["01_pm_expressions"] = art

# 2. the PM: poses
art = title("THE PM: poses", "Bulb in his left hand (screen-right). Free arm swings when he walks.")
art += floor(900)
art += cast.pm(220, 906, pose="stand", mood="hopeful", bulb=1.0) + label(220, 960, "stand, idea up")
art += cast.pm(560, 906, pose="walk", mood="delighted", bulb=1.0, phase=0.9) + label(560, 960, "walk")
art += cast.pm(900, 906, pose="trudge", mood="weary", bulb=0.5, phase=0.4, stack=8, age="mid climb") + label(900, 960, "trudge, paperwork")
art += bench(1240, 900, 0.6) + bench_front(1240, 900, 0.6) + cast.pm(1240, 906, pose="sit", mood="weary", bulb=0.7) + label(1240, 960, "sit (bench gag)")
art += cast.pm(1640, 896, s=0.3, pose="crawl", mood="exhausted", bulb=0.1, age=(0.12, 0.85), phase=0.8) + label(1640, 960, "leopard crawl")
sheets["02_pm_poses"] = art

# 3. the PM: the climb (ageing)
art = title("THE PM: the climb", "The beard only grows. Grey from mid-climb. Oxygen tank and paperwork backpack at the top.")
art += floor(940)
stops = [("fresh", 1.0, 0, False), ("stubble", 0.92, 0, False), ("first bench", 0.8, 0, False), ("mid climb", 0.55, 0, False),
         ("the fork", 0.4, 180, False), ("summit", 0.2, 260, True)]
for i, (age, b, pack, tank) in enumerate(stops):
    x = 200 + i * 300
    art += cast.pm(x, 946, s=0.4, pose="stand", mood="hopeful" if i < 2 else "weary" if i < 5 else "exhausted", bulb=b,
                   age=age, pack=pack, tank=tank) + label(x, 1000, age)
sheets["03_pm_climb"] = art

# 4. the idea bulb
art = title("THE IDEA", "The brightest thing on screen. Once chosen it blazes, and on the mountain it only ever dims.")
levels = [(1.0, "1.0  chosen"), (0.8, "0.8  first bench"), (0.6, "0.6  the climb"), (0.4, "0.4  the fork"),
          (0.2, "0.2  thin air"), (0.06, "0.06  summit"), (0.0, "out")]
for i, (b, t) in enumerate(levels):
    x = 190 + i * 255
    art += cast.idea(x, 560, 1.4, b, dead=(b == 0.0)) + label(x, 760, t)
art += label(960, 900, "Chapter 2 ending: a string of them, lit together.", 30)
xs = [600 + i * 90 for i in range(9)]
art += path("M 530,950 " + " ".join(f"Q {x - 45},992 {x},968" for x in xs) + " Q 1390,992 1420,950", sw=3)
art += "".join(path(f"M {x},968 L {x},980", sw=3) + cast.idea(x, 1016, 0.32, 0.8) for x in xs)
sheets["04_the_idea"] = art

# 5. the customer
art = title("THE CUSTOMER", "Blond quiff, Sapphire Blue jacket, burgundy tie, kraft-brown coffee sleeve. Never in STAEDEAN tie or cup colours.")
art += floor(930)
poses = [("phone", "neutral", "on his phone"), ("down", "puzzled", "“Who are you?”"), ("wave", "happy", "wave"),
         ("thumbs_down", "unimpressed", "week 1"), ("point", "puzzled", "week 2"), ("thumbs_up", "delighted", "week 3"),
         ("shake", "delighted", "handshake"), ("hold_box", "delighted", "got it")]
for i, (p, m, t) in enumerate(poses):
    x = 170 + i * 225
    art += cast.customer(x + (40 if p in ("shake", "point") else 0), 926, s=0.42, pose=p, mood=m, box=(p == "hold_box"),
                         coffee=p not in ("hold_box",), look=(-1, 0.4) if p == "down" else (0, 0)) + label(x, 985, t, 22)
sheets["05_customer"] = art

# 6. supporting cast
art = title("SUPPORTING CAST", "Everyone from the climb ends up behind the counter, serving the queue.")
art += floor(1000)
for i, (dept, x) in enumerate([("qa", 230), ("customer success", 560), ("product owner", 890), ("planning", 1220)]):
    art += washed(f"M {x - 150},470 L {x + 150},470 L {x + 150},550 L {x - 150},550 Z", "#c4a77c", off=(3, 2))
    art += cast.official(dept, x, 470, s=0.6, gesture="rest") + label(x, 600, "QA" if dept == "qa" else dept.title())
art += cast.maker(1660, 600, s=0.38, mood="delighted") + label(1660, 645, "the Maker")
art += label(1660, 675, "(chapter 2 teammate)", 20)
for i in range(3):
    art += cast.colleague(i, 250 + i * 250, 1006, s=0.36, phase=0.6 * i, bulb=0.7)
art += label(500, 1050, "colleagues, heading through the door", 22)
for i, pal in enumerate(film2.QUEUE[:4]):
    art += cast.customer(1250 + i * 160, 1000, s=0.33, pose="wave" if i % 2 else "phone", mood="happy", palette=pal, coffee=False)
art += label(1490, 1050, "the queue", 22)
sheets["06_supporting_cast"] = art

# 7. props
art = title("PROPS", "Same drawing every time they appear.")
art += booth_back(200, 640, 0.5, sign="CHECKPOINT") + booth_front(200, 640, 0.5) + label(200, 690, "checkpoint booth")
art += now_serving(240, 860, 0.8, "086") + label(240, 960, "now serving")
art += dispenser(460, 640, 0.6, strip=0.6) + label(460, 690, "ticket dispenser")
art += bench(710, 640, 0.5) + bench_front(710, 640, 0.5) + label(710, 690, "the bench")
art += f'<g transform="translate(-221,137) scale(0.62)">' + film2.door(0.0) + '</g>' + label(1010, 690, "the door")
art += film2.proto(1240, 630, 1) + film2.proto(1410, 630, 2) + film2.proto(1580, 630, 3, 0.7) + label(1410, 690, "prototypes, weeks 1 to 3")
art += film2.product_box(1790, 580, 0.8) + label(1790, 690, "the product")
art += film2.catapult(620, 960, 0.45, arm=-25) + label(620, 1010, "catapult")

art += signpost(1050, 1040, 0.42, "left", "ERP ROADMAP", ("Next quarterly release",), "dragon")
art += signpost(1400, 1040, 0.42, "right", "AI ROUTE", ("Intake form first",), "sea")
art += bubble(1720, 860, 260, 110, (1660, 940), lines=3, seed=3) + label(1720, 1010, "speech bubble")
sheets["07_props"] = art

# 8. brand + logo
from logo_path import LOGO_D, LOGO_W, LOGO_H
art = title("BRAND IN THE FILMS", "STAEDEAN colours appear only in these places.")
swatches = [("#FF9C46", "Tangerine Orange", "PM tie"), ("#17C8BE", "Miami Teal", "roofs, flag, door, awning, mug, tank, logo"),
            ("#00316C", "Sapphire Blue", "customer jacket"), ("#1F2342", "Galaxy Black", "PM trousers, chair, display"),
            ("#D7BA94", "Beige", "office floor"), ("#FF95D2", "Pink", "QA official")]
for i, (c, n, use) in enumerate(swatches):
    y = 230 + i * 85
    art += f'<rect x="80" y="{y}" width="120" height="60" fill="{c}" stroke="{INKC}" stroke-width="3"/>'
    art += text(230, y + 28, n, size=28, anchor="start", family="Georgia, serif") + text(230, y + 56, f"{c}   {use}", size=20, anchor="start", weight="normal", family="Georgia, serif")
k = 900 / LOGO_W
art += (f'<g transform="translate(960,{760 - LOGO_H * k / 2:.0f}) scale({k:.4f})">'
        f'<path d="{LOGO_D}" fill="#17c8be" fill-rule="evenodd" transform="translate(10,8)" filter="url(#wc)"/>'
        f'<path d="{LOGO_D}" fill="none" stroke="{INKC}" stroke-width="9" stroke-dasharray="420 16 260 12 340 14"/></g>')
art += label(1410, 940, "the logo, redrawn in the house style", 24)
sheets["08_brand"] = art

render([(k_, cast.frame(v)) for k_, v in sheets.items()], OUT)

# true-colour swatches painted on top (the marker filter softens flat fills)
from PIL import Image, ImageDraw
im = Image.open(f"{OUT}/08_brand.png").convert("RGB"); d = ImageDraw.Draw(im)
for i, (c, n, use) in enumerate(swatches):
    y = 230 + i * 85
    d.rectangle([84, y + 4, 196, y + 56], fill=c)
im.save(f"{OUT}/08_brand.png")
