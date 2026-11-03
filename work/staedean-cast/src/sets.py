"""Fixed locations. Each set is drawn the same way every time; frames only reframe or add weather."""
import math, random
from props import *
from rig import _mix, _old_hand

GROUND = 900


def sky(top="#cfe0ea", bottom="#eef1ea", snow=0.0):
    top = _mix(top, "#c7ccd0", snow * 0.8)
    bottom = _mix(bottom, "#e4e6e6", snow * 0.8)
    return (f'<defs><linearGradient id="skyG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/>'
            f'<stop offset="1" stop-color="{bottom}"/></linearGradient></defs>'
            f'<rect x="-200" y="-200" width="2400" height="1500" fill="url(#skyG)"/>')


def cloud(x, y, s=1.0, col="#fbfaf6"):
    d = ("M -120,0 C -150,0 -150,-40 -110,-44 C -110,-90 -40,-96 -20,-60 C 0,-110 90,-100 90,-50 "
         "C 140,-60 160,0 120,0 Z")
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{washed(d, col, sw=3, off=(3, 2))}</g>'


# ---------------- the giant mountain (reveal + wide shots) ----------------
SWITCHBACKS = None


def _route():
    """Points of the winding route from base to summit (in big-mountain coordinates)."""
    pts = []
    y = 1010
    amp = 520
    x = 470
    i = 0
    while y > 150:
        pts.append((x, y))
        x = 960 + (amp if i % 2 == 0 else -amp) * 0.9
        y -= 70 * (0.6 + y / 1400)
        amp *= 0.86
        i += 1
    pts.append((960, 96))
    return pts


def big_mountain(pm_dot=None, dot_b=1.0, show_sign=True, snow=0.0, pm_pos=0, pm_beard=0.0, pm_grey=0.0, pm_papers=0):
    g = [sky()]
    # distant small hills for scale
    g.append(f'<path d="M -200,1000 C 100,880 300,900 500,960 C 700,900 900,920 1100,980 L 1100,1100 L -200,1100 Z" fill="#b9c6b0"/>')
    # the mountain
    m = "M -260,1100 C 200,900 600,500 820,240 C 880,160 920,80 960,60 C 1010,80 1060,170 1120,250 C 1340,520 1700,860 2180,1100 Z"
    g.append(washed(m, C["mountain"], off=(6, 4)))
    g.append('<path d="M 960,60 C 920,80 880,160 820,240 C 700,400 600,520 520,620 C 700,520 820,380 900,240 C 930,180 950,120 960,60 Z" fill="#b4bbbe" opacity="0.7"/>')
    g.append('<path d="M 960,60 C 1010,80 1060,170 1120,250 C 1340,520 1700,860 2180,1100 L 1700,1100 C 1400,800 1150,500 1060,240 Z" fill="#7f878c" opacity="0.45"/>')
    # snow cap
    cap = "M 960,60 C 1010,80 1050,150 1090,210 C 1060,230 1040,200 1010,230 C 990,200 960,240 930,210 C 900,240 880,210 850,220 C 890,160 920,80 960,60 Z"
    g.append(washed(cap, C["snow"], off=(3, 2)))
    # cloud belt
    for cx, cy, cs in ((420, 640, 1.2), (1500, 560, 1.4), (1180, 420, 0.9), (700, 380, 0.8), (1660, 760, 1.1)):
        g.append(cloud(cx, cy, cs))
    # the route
    pts = _route()
    d = f"M {pts[0][0]},{pts[0][1]}" + "".join(f" L {x},{y}" for x, y in pts[1:])
    g.append(f'<path d="{d}" fill="none" stroke="#e8e0cc" stroke-width="7" stroke-linejoin="round"/>')
    g.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="7 6" stroke-linejoin="round"/>')
    # checkpoints, gates and benches along the route
    for i, (x, y) in enumerate(pts[1:-1]):
        sc = 0.13 * (0.45 + y / 1500)
        if i % 3 == 0:
            g.append(booth_back(x, y, sc, sign="") + booth_front(x, y, sc))
        elif i % 3 == 1:
            g.append(bench(x, y, sc * 0.8, sign=False) + bench_front(x, y, sc * 0.8))
        else:
            # gate
            g.append(f'<g transform="translate({x},{y}) scale({sc})">' + path("M -120,0 L -120,-260 M 120,0 L 120,-260", sw=14)
                     + washed("M -140,-280 L 140,-280 L 140,-230 L -140,-230 Z", "#c0623a", off=(3, 2))
                     + path("M -110,-150 L 110,-150", sw=10, stroke="#c0623a") + '</g>')
    # base: the office building
    g.append(washed("M 120,1010 L 120,900 L 300,900 L 300,1010 Z", "#d9cdb5", off=(3, 2)))
    for wx in (140, 190, 240):
        g.append(f'<rect x="{wx}" y="920" width="34" height="26" fill="#cfe0ea" stroke="{INK}" stroke-width="2"/>')
        g.append(f'<rect x="{wx}" y="960" width="34" height="26" fill="#cfe0ea" stroke="{INK}" stroke-width="2"/>')
    g.append(path("M 110,1010 L 2000,1010", sw=3))
    g.append(f'<path d="M -10,1010 L 1930,1010 L 1930,1090 L -10,1090 Z" fill="#a9b394"/>')
    if show_sign:
        g.append(washed("M 380,980 L 392,980 L 392,860 L 380,860 Z", "#8a6a48", sw=2.6, off=(1, 1)))
        g.append(washed("M 300,800 L 720,800 L 720,880 L 300,880 Z", "#f1e6cf", off=(3, 2)))
        g.append(text(510, 836, "MOUNT STAEDEAN", size=34, spacing=2))
        g.append(text(510, 868, "20,000 m", size=24, weight="normal"))
    # the PM: a tiny figure with a glowing dot
    if pm_dot:
        x, y = pm_dot
        g.append(f'<circle cx="{x}" cy="{y - 24}" r="{30 * dot_b + 6}" fill="url(#glowG)"/>')
        g.append(f'<g transform="translate({x},{y}) scale(0.045)">' +
                 pm_full(0, 0, 1.0, legs_mode="stand", look=(0.3, -1),
                         beard=pm_beard, grey=pm_grey,
                         before_arms=paper_stack(-180, 300, n=pm_papers, w=140, tilt=-6) if pm_papers else "",
                         arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 90), "cup", True)],
                         front=bulb(190, 38, s=1, b=dot_b, rays=0)) + '</g>')
    return "".join(g)


# ---------------- mountain ledge: the checkpoint location ----------------
def ledge(snow=0.0, marker="100 m", far=True):
    g = [sky(snow=snow)]
    # distant ridge
    g.append(f'<path d="M -100,560 C 200,420 360,470 520,380 C 700,280 820,420 1000,360 C 1200,300 1400,400 2020,330 L 2020,1100 L -100,1100 Z" fill="{_mix("#b7c0c4", "#dfe3e4", snow)}"/>')
    # the mountainside rising behind the booth (huge, goes off frame)
    side = "M 700,1100 C 900,700 1200,300 1500,-40 L 2100,-40 L 2100,1100 Z"
    g.append(washed(side, _mix(C["mountain"], "#d8dcde", snow * 0.7), off=(6, 4)))
    g.append(f'<path d="M 1500,-40 C 1300,200 1100,500 960,780 C 1160,560 1360,280 1600,-40 Z" fill="#b4bbbe" opacity="0.6"/>')
    # switchback path continuing up the slope (the next checkpoint is tiny, far above)
    g.append(f'<path d="M 1780,900 C 1900,820 1500,760 1420,700 C 1700,620 1800,560 1600,480 C 1500,430 1700,360 1760,300" fill="none" stroke="#e8e0cc" stroke-width="10"/>')
    g.append(f'<path d="M 1780,900 C 1900,820 1500,760 1420,700 C 1700,620 1800,560 1600,480 C 1500,430 1700,360 1760,300" fill="none" stroke="{INK}" stroke-width="1.8" stroke-dasharray="8 7"/>')
    g.append(booth_back(1765, 296, 0.08, sign="") + booth_front(1765, 296, 0.08))
    # ground ledge
    g.append(washed(f"M -60,{GROUND - 10} C 500,{GROUND - 30} 1200,{GROUND - 10} 1980,{GROUND - 30} L 1980,1100 L -60,1100 Z",
                    _mix("#b8a888", "#e9ecec", snow), off=(4, 3)))
    g.append(f'<path d="M -60,{GROUND + 40} C 600,{GROUND + 30} 1200,{GROUND + 50} 1980,{GROUND + 30} L 1980,1100 L -60,1100 Z" fill="{_mix("#a39274", "#d9dddd", snow)}" opacity="0.7"/>')
    # rocks
    for rx, ry, rs in ((120, 960, 1), (1840, 990, 1.3), (760, 1010, 0.7)):
        g.append(f'<g transform="translate({rx},{ry}) scale({rs})">' + washed("M -50,10 C -60,-20 -20,-50 10,-40 C 40,-40 60,-10 50,10 Z", "#9a978f", off=(2, 2)) + '</g>')
    if marker:
        g.append(marker_post(1800, GROUND + 4, 0.8, marker))
    return "".join(g)


# ---------------- a steep slope for climbing shots ----------------
def slope(snow=0.0, steep=1.0, seed=2):
    g = [sky(snow=snow)]
    g.append(f'<path d="M -100,700 C 300,640 500,700 800,620 C 1100,560 1400,640 2020,560 L 2020,1100 L -100,1100 Z" fill="{_mix("#c3cbcf", "#e4e7e8", snow)}"/>')
    hill = f"M -100,{1100} L -100,{980} C 600,{940 - 200 * steep} 1300,{700 - 200 * steep} 2020,{460 - 250 * steep} L 2020,1100 Z"
    g.append(washed(hill, _mix("#a99c80", "#eef0f0", snow), off=(5, 3)))
    # path line along the slope
    g.append(path(f"M -100,{1000} C 600,{960 - 200 * steep} 1300,{720 - 200 * steep} 2020,{480 - 250 * steep}", sw=2, stroke="#7f7461"))
    rnd = random.Random(seed)
    for _ in range(8):
        x = rnd.uniform(0, 1900)
        t = x / 2020
        y = 1000 + (480 - 250 * steep - 1000) * t + rnd.uniform(30, 120)
        g.append(f'<g transform="translate({f(x)},{f(y)}) scale({f(rnd.uniform(0.4, 0.9))})">' + washed("M -50,10 C -60,-20 -20,-50 10,-40 C 40,-40 60,-10 50,10 Z", _mix("#9a978f", "#dfe3e3", snow * 0.6), off=(2, 2)) + '</g>')
    return "".join(g)


def slope_y(x, steep=1.0):
    """Ground height on the slope path at screen x (approximate the bezier)."""
    t = (x + 100) / 2120
    y0, y1 = 1000, 480 - 250 * steep
    c1, c2 = 960 - 200 * steep, 720 - 200 * steep
    return (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * y1


# ---------------- the fork ----------------
def fork_set(snow=0.4):
    g = [sky(snow=snow)]
    g.append(f'<path d="M -100,600 C 200,500 500,560 760,480 C 960,420 1200,520 1400,460 C 1600,400 1800,480 2020,440 L 2020,1100 L -100,1100 Z" fill="#c9cfd2"/>')
    # left: dragon's lair, a craggy peak with smoke
    g.append(washed("M -100,900 L -100,300 C 60,220 160,140 260,180 C 340,120 420,200 520,260 C 600,320 640,500 700,900 Z", "#8d8f8a", off=(5, 3)))
    g.append(washed("M 220,520 C 220,420 380,420 380,520 L 380,600 L 220,600 Z", "#2f2b2a", off=(3, 2)))
    g.append(f'<circle cx="270" cy="520" r="7" fill="#ffd659"/><circle cx="320" cy="520" r="7" fill="#ffd659"/>')
    g.append(path("M 300,420 C 280,380 330,360 310,320 C 290,280 340,260 320,220", sw=6, stroke="#9a948c"))
    # right: a dark lake with a sea monster
    g.append(washed("M 1260,880 C 1320,820 1500,780 1700,780 C 1880,780 2000,800 2040,820 L 2040,880 Z", "#56788a", off=(5, 3)))
    g.append(sea_monster(1720, 800, 0.9))
    # ground and the two paths
    g.append(washed(f"M -60,{GROUND - 30} C 600,{GROUND - 40} 1300,{GROUND - 30} 1980,{GROUND - 40} L 1980,1100 L -60,1100 Z", _mix("#b8a888", "#e9ecec", snow), off=(4, 3)))
    g.append(path("M 900,1100 C 880,1010 760,960 560,900", sw=3))
    g.append(path("M 1020,1100 C 1040,1010 1160,960 1360,900", sw=3))
    g.append(path("M 960,1100 C 950,1010 900,980 700,910 M 960,1100 C 970,1010 1020,980 1220,910", sw=2, stroke="#9a8c70"))
    return "".join(g)


# ---------------- the summit ----------------
def summit_set():
    g = [sky(top="#b9d6ea", bottom="#f3efe4")]
    # sea of clouds below
    g.append(f'<path d="M -100,760 C 200,700 400,760 700,720 C 1000,680 1300,760 1600,710 C 1800,690 1900,720 2020,700 L 2020,1100 L -100,1100 Z" fill="#fbfaf6"/>')
    for cx, cy, cs in ((200, 760, 1.3), (900, 740, 1.0), (1700, 760, 1.4)):
        g.append(cloud(cx, cy, cs))
    # the summit plateau
    g.append(washed(f"M -60,1100 L -60,{GROUND + 20} C 300,{GROUND - 20} 700,{GROUND - 40} 1100,{GROUND - 40} C 1500,{GROUND - 30} 1800,{GROUND + 10} 1980,{GROUND + 60} L 1980,1100 Z", C["snow"], off=(4, 3)))
    g.append(f'<path d="M -60,1100 L -60,{GROUND + 90} C 400,{GROUND + 60} 1200,{GROUND + 80} 1980,{GROUND + 120} L 1980,1100 Z" fill="#dfe4e6" opacity="0.8"/>')
    return "".join(g)


# ---------------- the trailhead (foot of the mountain) ----------------
def mountain_wall(x0=560, with_route=True):
    g = [washed(f"M {x0},1100 C {x0 + 200},700 {x0 + 420},300 {x0 + 600},-60 L 2100,-60 L 2100,1100 Z", C["mountain"], off=(6, 4))]
    g.append(f'<path d="M {x0 + 600},-60 C {x0 + 450},250 {x0 + 300},600 {x0 + 150},1000 C {x0 + 380},620 {x0 + 560},300 {x0 + 700},-60 Z" fill="#b4bbbe" opacity="0.6"/>')
    if with_route:
        d = (f"M {x0 + 260},880 C {x0 + 700},850 {x0 + 1200},800 {x0 + 1250},740 C {x0 + 900},700 {x0 + 600},660 {x0 + 470},600 "
             f"C {x0 + 800},560 {x0 + 1100},520 {x0 + 1150},470 C {x0 + 900},430 {x0 + 700},400 {x0 + 640},350 "
             f"C {x0 + 900},320 {x0 + 1000},290 {x0 + 1040},250 C {x0 + 900},220 {x0 + 800},190 {x0 + 780},150 L {x0 + 900},40")
        g.append(f'<path d="{d}" fill="none" stroke="#e8e0cc" stroke-width="10"/>')
        g.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-dasharray="8 7"/>')
        for bx, by, bs in ((x0 + 1250, 740, 0.16), (x0 + 470, 600, 0.13), (x0 + 1150, 470, 0.11), (x0 + 640, 350, 0.09), (x0 + 1040, 250, 0.07), (x0 + 780, 150, 0.06)):
            g.append(booth_back(bx, by, bs, sign="") + booth_front(bx, by, bs))
    return "".join(g)


def trailhead():
    g = [sky()]
    g.append(f'<path d="M -100,700 C 200,640 400,680 600,640 L 600,1100 L -100,1100 Z" fill="#b9c6b0"/>')
    g.append(mountain_wall(560))
    # office building edge (where he came from)
    g.append(washed("M -60,900 L -60,560 L 200,560 L 200,900 Z", "#d9cdb5", off=(4, 3)))
    for wy in (600, 700, 800):
        for wx in (-30, 90):
            g.append(f'<rect x="{wx}" y="{wy}" width="70" height="56" fill="#cfe0ea" stroke="{INK}" stroke-width="2.4"/>')
    # ground
    g.append(washed(f"M -60,{GROUND - 6} C 600,{GROUND - 20} 1300,{GROUND - 6} 1980,{GROUND - 20} L 1980,1100 L -60,1100 Z", "#a9b394", off=(4, 3)))
    # big sign
    g.append(washed("M 330,900 L 346,900 L 346,690 L 330,690 Z", "#8a6a48", off=(2, 1)))
    g.append(washed("M 540,900 L 556,900 L 556,690 L 540,690 Z", "#8a6a48", off=(2, 1)))
    g.append(washed("M 220,560 L 660,560 L 660,700 L 220,700 Z", "#f1e6cf", off=(4, 3)))
    g.append(text(440, 618, "MOUNT STAEDEAN", size=36, spacing=2))
    g.append(text(440, 670, "20,000 m", size=30, weight="normal"))
    # little arrow sign at the start of the path
    g.append(washed("M 916,900 L 928,900 L 928,760 L 916,760 Z", "#8a6a48", sw=2.6, off=(1, 1)))
    g.append(washed("M 780,700 L 1040,700 L 1080,736 L 1040,772 L 780,772 Z", "#f6efe2", off=(3, 2)))
    g.append(text(920, 746, "TO THE CUSTOMER", size=24))
    return "".join(g)
