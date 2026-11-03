"""Props and supporting cast. Same drawing every time they appear."""
import math, random
from rig import *
from rig import _mix

SERIF = "Georgia, 'DejaVu Serif', serif"
HAND = "'Comic Neue', 'Patrick Hand', 'DejaVu Sans', sans-serif"


def text(x, y, s, size=28, fill=None, anchor="middle", weight="bold", family=SERIF, rot=0, spacing=0):
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill or INK}" letter-spacing="{spacing}" transform="rotate({rot},{f(x)},{f(y)})">{s}</text>')


# ---------- speech bubbles ----------
def bubble(x, y, w, h, tail, lines=None, words=None, size=40, seed=1):
    """Rounded bubble centred at (x, y). tail = (tx, ty) point. lines = number of scribble lines."""
    tx, ty = tail
    rx, ry = w / 2, h / 2
    # tail base on the bubble edge nearest the tail
    ang = math.atan2(ty - y, tx - x)
    bx, by = x + rx * 0.8 * math.cos(ang), y + ry * 0.8 * math.sin(ang)
    px, py = -math.sin(ang) * 26, math.cos(ang) * 26
    tail_d = f"M {f(bx + px)},{f(by + py)} L {f(tx)},{f(ty)} L {f(bx - px)},{f(by - py)} Z"
    body = (f"M {f(x - rx)},{f(y)} C {f(x - rx)},{f(y - ry * 1.1)} {f(x + rx)},{f(y - ry * 1.1)} {f(x + rx)},{f(y)} "
            f"C {f(x + rx)},{f(y + ry * 1.1)} {f(x - rx)},{f(y + ry * 1.1)} {f(x - rx)},{f(y)} Z")
    g = [f'<path d="{tail_d}" fill="#fffdf6"/>', f'<path d="{body}" fill="#fffdf6"/>',
         path(f"M {f(bx + px)},{f(by + py)} L {f(tx)},{f(ty)} L {f(bx - px)},{f(by - py)}", sw=3.4), path(body, sw=3.4),
         f'<path d="{tail_d}" fill="#fffdf6" transform="translate(0,0) scale(1)" opacity="1" stroke="none" />']
    # cover the seam
    g.append(f'<path d="M {f(bx + px * 0.8)},{f(by + py * 0.8)} L {f(bx - px * 0.8)},{f(by - py * 0.8)}" stroke="#fffdf6" stroke-width="10"/>')
    if lines:
        rnd = random.Random(seed)
        n = lines
        lh = min((h * 0.72) / n, 30)
        for i in range(n):
            yy = y - h * 0.36 + lh * (i + 0.5)
            half = rx * 0.8 * math.sqrt(max(0.05, 1 - ((yy - y) / (ry * 0.95)) ** 2))
            x0, x1 = x - half, x + half
            if i == n - 1:
                x1 = x0 + (x1 - x0) * rnd.uniform(0.3, 0.6)
            segs, cx = [], x0
            while cx < x1 - 10:
                wl = min(rnd.uniform(14, 60), x1 - cx)
                segs.append(f"M {f(cx)},{f(yy)} L {f(cx + wl)},{f(yy)}")
                cx += wl + rnd.uniform(8, 13)
            g.append(path(" ".join(segs), sw=min(7.0, max(2.0, lh * 0.32))))
    if words:
        g.append(text(x, y + size * 0.35, words, size=size, family=HAND))
    return "".join(g)


# ---------- calendar pages flying ----------
def flying_pages(region, n=14, seed=3, months=None):
    x0, y0, x1, y1 = region
    rnd = random.Random(seed)
    names = months or ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    g = []
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(-40, 40)
        sc = rnd.uniform(0.55, 0.9)
        m = names[(i + seed) % len(names)]
        inner = (washed("M 0,0 L 90,0 L 92,110 L 2,112 Z", C["paper_sheet"], sw=2.6, off=(2, 2))
                 + washed("M 0,0 L 90,0 L 90,26 L 0,26 Z", C["cal_red"], sw=2.4, off=(1, 1))
                 + f'<text x="45" y="20" text-anchor="middle" font-family="{SERIF}" font-weight="bold" font-size="17" fill="#fbf3e6">{m}</text>'
                 + path("M 14,46 L 30,46 M 40,46 L 56,46 M 66,46 L 78,46 M 14,70 L 30,70 M 40,70 L 56,70 M 66,70 L 78,70 M 14,94 L 30,94 M 40,94 L 56,94", sw=2))
        g.append(f'<g transform="translate({f(x)},{f(y)}) rotate({f(r)}) scale({f(sc)})">{inner}</g>')
        # motion streak
        g.append(path(f"M {f(x - 30)},{f(y + 40)} C {f(x - 80)},{f(y + 50)} {f(x - 120)},{f(y + 30)} {f(x - 160)},{f(y + 44)}", sw=2, stroke="#9a8a74"))
    return "".join(g)


def page_pile(x, y, n=8, seed=9):
    rnd = random.Random(seed)
    g = []
    for i in range(n):
        dx, r = rnd.uniform(-120, 120), rnd.uniform(-30, 30)
        inner = washed("M 0,0 L 70,0 L 70,40 L 0,40 Z", C["paper_sheet"], sw=2.2, off=(1, 1)) + \
            washed("M 0,0 L 70,0 L 70,10 L 0,10 Z", C["cal_red"], sw=2, off=(1, 1))
        g.append(f'<g transform="translate({f(x + dx)},{f(y - rnd.uniform(0, 14))}) rotate({f(r)}) scale(0.8,0.55)">{inner}</g>')
    return "".join(g)


def cobweb(x, y, s=1.0):
    g = []
    for a in range(0, 91, 18):
        ar = math.radians(a)
        g.append(f"M {x},{y} L {f(x + 120 * s * math.cos(ar))},{f(y + 120 * s * math.sin(ar))}")
    for r in (36, 70, 104):
        pts = [(x + r * s * math.cos(math.radians(a)), y + r * s * math.sin(math.radians(a))) for a in range(0, 91, 18)]
        d = f"M {f(pts[0][0])},{f(pts[0][1])}" + "".join(
            f" Q {f((p[0] + q[0]) / 2 - 4)},{f((p[1] + q[1]) / 2 - 4)} {f(q[0])},{f(q[1])}" for p, q in zip(pts, pts[1:]))
        g.append(d)
    return path(" ".join(g), sw=1.4, stroke="#7d7568")


def snowfall(region, n=80, seed=4, wind=0.3):
    x0, y0, x1, y1 = region
    rnd = random.Random(seed)
    g = []
    for _ in range(n):
        x, y, r = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(3, 7)
        g.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="#ffffff" opacity="0.9"/>')
        if wind > 0.5 and rnd.random() < 0.3:
            g.append(path(f"M {f(x + 20)},{f(y - 4)} L {f(x + 20 + 60 * wind)},{f(y - 14)}", sw=1.6, stroke="#ffffff"))
    return "".join(g)


def wind_lines(region, n=6, seed=8):
    x0, y0, x1, y1 = region
    rnd = random.Random(seed)
    g = []
    for _ in range(n):
        x, y, L = rnd.uniform(x0, x1), rnd.uniform(y0, y1), rnd.uniform(120, 260)
        g.append(f"M {f(x)},{f(y)} C {f(x - L * 0.3)},{f(y - 14)} {f(x - L * 0.6)},{f(y + 12)} {f(x - L)},{f(y)} "
                 f"C {f(x - L - 26)},{f(y - 4)} {f(x - L - 22)},{f(y - 26)} {f(x - L - 6)},{f(y - 22)}")
    return path(" ".join(g), sw=2.4, stroke="#8a98a0")


# ---------- the officials (friendly, busy people, never villains) ----------
OFFICIALS = {
    # hair colour, cardigan, glasses, hair style
    "desk":     dict(hair="#3b3633", top="#8a6f9c", glasses=True,  style="bun",   skin="#e8bf9c"),
    "cs":       dict(hair="#b5642f", top="#5f8f7c", glasses=False, style="bob",   skin="#f2cfae", headset=True),
    "po":       dict(hair="#2f2a28", top="#c99a3e", glasses=True,  style="short", skin="#c99272"),
    "planning": dict(hair="#9c9a94", top="#6d7f9c", glasses=True,  style="bald",  skin="#efc7a4"),
}


def official(x, y, s=0.5, who="desk", arm="rest", mouth="smile", look=(0, 0), brows="neutral", phone=False, walk_phase=0, swing=1.0, head_tilt=0, carry_idea=False, hand_targets=None, mic_angle=0):
    """Front-facing upper body behind a counter. (x, y) = counter top centre."""
    o = OFFICIALS[who]
    g = []
    # body
    g.append(washed("M -150,0 C -150,-120 -110,-180 -60,-190 L 60,-190 C 110,-180 150,-120 150,0 Z", o["top"], off=(4, 3)))
    g.append(washed("M -30,-190 L 0,-130 L 30,-190 Z", "#f6efe2", sw=2.6, off=(1, 1)))
    g.append(washed("M -26,-216 L 26,-216 L 28,-186 L -28,-186 Z", o["skin"], sw=3, off=(2, 1)))
    # Head motion is independent of the torso; default zero preserves existing shots.
    g.append(f'<g transform="rotate({head_tilt},0,-205)">')
    # head
    hy = -300
    if o["style"] == "bob":
        g.append(washed(f"M -96,{hy + 40} C -110,{hy - 70} 110,{hy - 70} 96,{hy + 40} L 70,{hy + 60} L -70,{hy + 60} Z", o["hair"], off=(3, 2)))
    g.append(washed(f"M -80,{hy} C -80,{hy - 100} 80,{hy - 100} 80,{hy} C 80,{hy + 90} -80,{hy + 90} -80,{hy} Z", o["skin"], off=(4, 3)))
    if o["style"] == "bun":
        g.append(washed(f"M -82,{hy - 10} C -86,{hy - 96} 86,{hy - 96} 82,{hy - 10} C 60,{hy - 50} -60,{hy - 50} -82,{hy - 10} Z", o["hair"], off=(3, 2)))
        g.append(washed(f"M -30,{hy - 92} C -30,{hy - 140} 30,{hy - 140} 30,{hy - 92} Z", o["hair"], off=(2, 2)))
    elif o["style"] == "short":
        g.append(washed(f"M -82,{hy - 6} C -90,{hy - 100} 90,{hy - 100} 82,{hy - 6} C 70,{hy - 40} 30,{hy - 56} 0,{hy - 50} C -30,{hy - 56} -70,{hy - 40} -82,{hy - 6} Z", o["hair"], off=(3, 2)))
    elif o["style"] == "bald":
        g.append(washed(f"M -82,{hy + 10} C -96,{hy - 30} -80,{hy - 50} -70,{hy - 30} L -66,{hy + 20} Z", o["hair"], off=(2, 2)))
        g.append(washed(f"M 82,{hy + 10} C 96,{hy - 30} 80,{hy - 50} 70,{hy - 30} L 66,{hy + 20} Z", o["hair"], off=(2, 2)))
    elif o["style"] == "bob":
        g.append(washed(f"M -84,{hy - 4} C -90,{hy - 96} 90,{hy - 96} 84,{hy - 4} C 50,{hy - 50} -40,{hy - 60} -84,{hy - 4} Z", o["hair"], off=(3, 2)))
    # face
    lx, ly = look
    for ex in (-30, 30):
        g.append(f'<circle cx="{ex + lx * 5}" cy="{hy - 4 + ly * 5}" r="7" fill="{INK}"/>')
        if o["glasses"]:
            g.append(f'<circle cx="{ex}" cy="{hy - 4}" r="22" fill="none" stroke="{INK}" stroke-width="3.2"/>')
    if o["glasses"]:
        g.append(path(f"M -8,{hy - 6} L 8,{hy - 6}", sw=3))
    bmap = {"neutral": (0, 0), "raised": (-10, 0), "puzzled": (-8, 8)}
    by1, by2 = bmap.get(brows, (0, 0))
    g.append(path(f"M -46,{hy - 36 + by1} L -16,{hy - 40 + by1} M 16,{hy - 40 + by2} L 46,{hy - 36 + by2}", sw=4.5, stroke=o["hair"] if o["style"] != "bald" else "#7a756e"))
    g.append(path(f"M -2,{hy + 4} C 4,{hy + 18} 8,{hy + 22} -2,{hy + 26}", sw=2.6))
    mouths = {"smile": f"M -24,{hy + 44} C -10,{hy + 58} 10,{hy + 58} 24,{hy + 44}",
              "flat": f"M -16,{hy + 50} L 16,{hy + 50}",
              "o": None, "talk": None}
    if mouth in ("o", "talk"):
        g.append(washed(f"M -14,{hy + 44} C -14,{hy + 66} 14,{hy + 66} 14,{hy + 44} C 6,{hy + 40} -6,{hy + 40} -14,{hy + 44} Z", "#7a2f25", sw=2.6, off=(1, 1)))
    else:
        g.append(path(mouths[mouth], sw=3.2))
    g.append(f'<ellipse cx="-50" cy="{hy + 26}" rx="14" ry="8" fill="{C["blush"]}" opacity="0.35"/><ellipse cx="50" cy="{hy + 26}" rx="14" ry="8" fill="{C["blush"]}" opacity="0.35"/>')
    if o.get("headset"):
        g.append(path(f"M -84,{hy - 10} C -84,{hy - 110} 84,{hy - 110} 84,{hy - 10}", sw=5))
        g.append(washed(f"M -96,{hy - 24} L -76,{hy - 24} L -76,{hy + 12} L -96,{hy + 12} Z", "#555", sw=2.6, off=(1, 1)))
        # Optional microphone rotation is used by the Handoff reaction; zero preserves prior films.
        g.append(f'<g transform="rotate({mic_angle},-86,{hy + 12})">'+path(f"M -86,{hy + 12} C -80,{hy + 50} -50,{hy + 56} -26,{hy + 52}", sw=3)+'</g>')
    g.append('</g>')  # close the independently posed head
    # Counter poses remain unchanged. The walking adapter supplies phase/swing.
    # Arms counter-swing against the corresponding leg, with relaxed elbows.
    if hand_targets is not None:
        # Optional prop-contact pose. Existing films keep their original arms.
        for side, (hx, hy2) in zip((-1, 1), hand_targets):
            elbow=(side*160, (hy2-150)*.5)
            g.append(tube([(side*120,-150),elbow,(hx,hy2)],38,o["top"]))
            g.append(washed(f"M {hx-17},{hy2-5} C {hx-24},{hy2+13} {hx+19},{hy2+19} {hx+21},{hy2-5} Z",o["skin"],sw=2.6,off=(1,1)))
    elif arm == "walk":
        for side in (-1, 1):
            if carry_idea and side == 1:
                # Hold the idea steady while the other arm keeps its walk swing.
                g.append(tube([(120,-150),(185,-140),(190,-90)],38,o["top"]))
                g.append(bulb(190,-142,s=.9,b=.7,rays=6))
                g.append(washed("M 162,-96 C 158,-72 208,-66 218,-96 C 200,-86 180,-86 162,-96 Z",o["skin"],sw=2.6,off=(1,1)))
                continue
            motion=math.sin(walk_phase + (math.pi if side < 0 else 0))*swing
            elbow=(side*155 + 30*motion,-68)
            hand=(side*135 + 65*motion,45 - 12*abs(motion))
            g.append(tube([(side*120,-150),elbow,hand],38,o["top"]))
            hx,hy2=hand
            g.append(washed(f"M {hx-14},{hy2-5} C {hx-21},{hy2+16} {hx+18},{hy2+24} {hx+17},{hy2+1} Z",o["skin"],sw=2.6,off=(1,1)))
    elif arm == "point_left":
        g.append(tube([(-120, -150), (-200, -170), (-270, -200)], 40, o["top"]))
        g.append(hand_extra((-290, -204), "point", 180))
        g.append(tube([(120, -150), (150, -40), (90, -6)], 40, o["top"]))
    elif arm == "point_right":
        g.append(tube([(120, -150), (220, -170), (330, -190)], 40, o["top"]))
        g.append(hand_extra((350, -190), "point", 0))
        g.append(tube([(-120, -150), (-150, -40), (-90, -6)], 40, o["top"]))
    elif arm == "finger_up":
        g.append(tube([(120, -150), (170, -60), (150, -230)], 40, o["top"]))
        g.append(washed("M 136,-230 C 130,-250 170,-252 166,-230 L 160,-216 L 140,-216 Z", o["skin"], sw=2.6, off=(1, 1)) +
                 washed("M 144,-246 L 144,-290 C 144,-300 158,-300 158,-290 L 158,-244 Z", o["skin"], sw=2.6, off=(1, 1)))
        g.append(tube([(-120, -150), (-150, -40), (-90, -6)], 40, o["top"]))
    else:
        g.append(tube([(-120, -150), (-150, -40), (-90, -6)], 40, o["top"]))
        g.append(tube([(120, -150), (150, -40), (90, -6)], 40, o["top"]))
    if phone:
        g.append(washed(f"M 70,{hy - 10} L 96,{hy - 20} L 112,{hy + 50} L 86,{hy + 60} Z", "#3d3d3d", sw=2.6, off=(1, 1)))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


# ---------- the checkpoint kiosk ----------
def booth_back(x, y, s=1.0, sign="CHECKPOINT 1", sign_size=46, calendar_state=0):
    """Back part of the kiosk (drawn BEFORE the official). (x, y) = ground centre."""
    g = []
    g.append(washed("M -300,0 L -300,-560 L 300,-560 L 300,0 Z", "#cdb58e", off=(5, 3)))
    for i in range(1, 12):
        g.append(path(f"M -300,{-i * 48} L 300,{-i * 48}", sw=1.4, stroke="#a88f68"))
    # inside of the window (darker)
    g.append(washed("M -230,-250 L 230,-250 L 230,-500 L -230,-500 Z", "#8e7a5e", off=(3, 2)))
    # roof
    g.append(washed("M -350,-560 L 0,-700 L 350,-560 Z", "#9c5b3c", off=(5, 3)))
    # sign board
    g.append(washed("M -260,-690 L 260,-690 L 260,-610 L -260,-610 Z", "#f4ecd9", off=(4, 3)))
    g.append(text(0, -634, sign, size=sign_size, spacing=1))
    # a wall calendar inside the kiosk (sheds pages when time passes)
    g.append(washed("M 150,-480 L 220,-480 L 220,-390 L 150,-390 Z", C["paper_sheet"], sw=2.4, off=(2, 2)))
    g.append(washed("M 150,-480 L 220,-480 L 220,-462 L 150,-462 Z", C["cal_red"], sw=2.2, off=(1, 1)))
    # paperwork piles behind the official (they are busy too)
    g.append(paper_stack(-170, -262, n=7, w=80))
    g.append(paper_stack(-110, -262, n=11, w=70))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def booth_front(x, y, s=1.0):
    """Counter and window frame (drawn AFTER the official)."""
    g = [washed("M -300,0 L -300,-250 L 300,-250 L 300,0 Z", "#c4a77c", off=(5, 3))]
    g.append(washed("M -330,-270 L 330,-270 L 330,-240 L -330,-240 Z", "#9a6f47", off=(3, 2)))
    for i in range(1, 5):
        g.append(path(f"M -300,{-i * 50} L 300,{-i * 50}", sw=1.4, stroke="#a08560"))
    g.append(path("M -300,-560 L -300,0 M 300,-560 L 300,0 M -230,-500 L 230,-500 M -230,-500 L -230,-270 M 230,-500 L 230,-270", sw=3.5))
    g.append(f'<ellipse cx="0" cy="8" rx="340" ry="18" fill="#6d5a44" opacity="0.3" filter="url(#soft)"/>')
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def dispenser(x, y, s=1.0, strip=0, ticket="087"):
    """Ticket dispenser on a post. strip = how much paper has unspooled (0..1)."""
    g = [washed("M -8,0 L 8,0 L 8,-330 L -8,-330 Z", "#8a8f90", off=(2, 1))]
    g.append(washed("M -60,-330 L 60,-330 L 60,-450 L -60,-450 Z", "#c0623a", off=(3, 2)))
    g.append(washed("M -40,-360 L 40,-360 L 40,-374 L -40,-374 Z", "#2e2520", sw=2, off=(0, 0)))
    g.append(text(0, -400, "TAKE A", size=20, fill="#fbf3e6"))
    g.append(text(0, -422, "", size=18))
    g.append(text(0, -380 - 46, "PLEASE", size=18, fill="#fbf3e6"))
    g.append(text(0, -382 + 4, "", size=10))
    g.append(text(0, -384 + 2, "TICKET", size=20, fill="#fbf3e6"))
    g.append(washed("M -70,0 C -70,-14 70,-14 70,0 Z", "#8a8f90", sw=3, off=(2, 1)))
    if strip > 0:
        # ribbon of paper pouring from the slot and pooling in loops on the ground
        n = int(3 + strip * 9)
        d = "M 0,-366 C -20,-300 40,-240 -10,-180 "
        yy = -180
        for i in range(n):
            xx = -60 - i * 44
            d += f"C {f(xx - 50)},{f(-120 + (i % 2) * 40)} {f(xx + 60)},{f(-40 + (i % 3) * 10)} {f(xx - 10)},{f(-10 - (i % 2) * 14)} "
        g.append(path(d, stroke=INK, sw=26) + path(d, stroke=C["paper_sheet"], sw=20))
        g.append(path(d, stroke="#bdb3a0", sw=1.2, extra='stroke-dasharray="3 14"'))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def ticket_end(x, y, s=1.0, num="087", rot=0):
    inner = washed("M -60,-30 L 60,-30 L 60,30 L -60,30 Z", C["paper_sheet"], sw=3, off=(2, 2)) + \
        text(0, 16, num, size=40, family=SERIF)
    return f'<g transform="translate({f(x)},{f(y)}) rotate({rot}) scale({s})">{inner}</g>'


def now_serving(x, y, s=1.0, num="086", ding=False):
    g = [washed("M -110,-70 L 110,-70 L 110,70 L -110,70 Z", "#3a3a3c", off=(3, 2))]
    g.append(text(0, -34, "NOW SERVING", size=22, fill="#e9e0cf", family="DejaVu Sans, sans-serif"))
    g.append(f'<rect x="-80" y="-20" width="160" height="72" fill="#1f1f1f"/>')
    g.append(text(0, 38, num, size=60, fill="#ff6a3a" if not ding else "#ffd659", family="DejaVu Sans Mono, monospace"))
    if ding:
        for a in range(-160, -10, 25):
            ar = math.radians(a)
            g.append(path(f"M {f(140 * math.cos(ar))},{f(100 * math.sin(ar) - 10)} L {f(185 * math.cos(ar))},{f(135 * math.sin(ar) - 10)}", sw=4, stroke="#c98a1e"))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def bench(x, y, s=1.0, sign=True):
    """Wooden bench. (x, y) = ground centre. Seat top at local y=-150."""
    g = []
    if sign:
        g.append(washed("M 250,0 L 262,0 L 262,-380 L 250,-380 Z", "#8a8f90", sw=2.6, off=(1, 1)))
        g.append(washed("M 130,-470 L 380,-470 L 380,-370 L 130,-370 Z", "#f4ecd9", off=(3, 2)))
        g.append(text(255, -430, "PLEASE TAKE", size=26))
        g.append(text(255, -392, "A SEAT", size=26))
    # back rest
    g.append(washed("M -230,-300 L 230,-300 L 230,-260 L -230,-260 Z", "#a87a4e", off=(3, 2)))
    g.append(washed("M -230,-240 L 230,-240 L 230,-200 L -230,-200 Z", "#a87a4e", off=(3, 2)))
    g.append(path("M -200,-300 L -200,-150 M 200,-300 L 200,-150", sw=8))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def bench_front(x, y, s=1.0):
    g = [washed("M -250,-160 L 250,-160 L 262,-130 L -262,-130 Z", "#b98a5e", off=(3, 2))]
    g.append(path("M -220,-130 L -230,0 M 220,-130 L 230,0", sw=9))
    g.append(f'<ellipse cx="0" cy="6" rx="270" ry="14" fill="#6d5a44" opacity="0.3" filter="url(#soft)"/>')
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def marker_post(x, y, s=1.0, label="100 m"):
    g = [washed("M -40,0 L -36,-150 C -30,-176 30,-176 36,-150 L 40,0 Z", "#b9b4a8", off=(3, 2))]
    g.append(text(0, -110, label, size=26))
    g.append(path("M -24,-80 L 24,-80", sw=2))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def flag(x, y, s=1.0, label="CUSTOMER"):
    g = [path("M 0,0 L 0,-420", sw=8)]
    g.append(washed("M 0,-420 C 80,-440 160,-400 240,-420 L 240,-300 C 160,-280 80,-320 0,-300 Z", "#c0623b", off=(3, 2)))
    g.append(text(120, -350, label, size=34, fill="#fbf3e6"))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def customer(x, y, s=0.5, pose="phone", mouth="flat", look=(0, 0), brows="neutral", blink=False, pal=None, box="", coffee=True, walk_phase=0, swing=1.0, head_tilt=0, carry_idea=False, receive_at=None):
    """The customer: smart jacket, quiff, coffee in one hand, phone in the other. Front-facing. (x, y) = feet."""
    P_ = dict(JK="#4f7a5c", TR="#323a48", SK="#f0cdb0", HR="#d9b25a", TIE="#8e2f45")
    P_.update(pal or {})
    JK, TR, SK, HR, TIE = P_["JK"], P_["TR"], P_["SK"], P_["HR"], P_["TIE"]
    g = []
    # legs + shoes
    g.append(tube([(-38, -380), (-44, -16)], 58, TR))
    g.append(tube([(38, -380), (44, -16)], 58, TR))
    for fx, d in ((-50, -1), (50, 1)):
        g.append(washed(f"M {fx - 34},-18 C {fx - 34},-44 {fx + 30},-44 {fx + 40 * d + 6},-20 L {fx + 44 * d},2 L {fx - 36},2 Z", "#3a2a22", off=(2, 1)))
    # jacket (tapered, with lapels) over a white shirt and a teal tie
    g.append(washed("M -122,-668 C -138,-600 -118,-470 -110,-350 L 110,-350 C 118,-470 138,-600 122,-668 C 70,-700 -70,-700 -122,-668 Z", JK, off=(4, 3)))
    g.append(washed("M -36,-690 L 36,-690 L 20,-520 L -20,-520 Z", "#fbf7ee", sw=2.6, off=(1, 1)))
    g.append(washed("M -8,-676 L 8,-676 L 14,-560 L 0,-536 L -14,-560 Z", TIE, sw=2.4, off=(1, 1)))
    g.append(washed("M -40,-690 L -2,-540 L -60,-600 L -46,-640 Z", JK, sw=2.6, off=(2, 1)))
    g.append(washed("M 40,-690 L 2,-540 L 60,-600 L 46,-640 Z", JK, sw=2.6, off=(2, 1)))
    g.append(f'<circle cx="0" cy="-470" r="6" fill="#2e2520"/><circle cx="0" cy="-420" r="6" fill="#2e2520"/>')
    g.append(path("M -90,-470 L -40,-466 M 40,-466 L 90,-470", sw=2.4))
    # Walking can add a small head inclination without tilting the coffee cup.
    g.append(f'<g transform="rotate({head_tilt},0,-690)">')
    # neck + head
    hy = -800
    g.append(washed(f"M -24,{hy + 80} L 24,{hy + 80} L 26,{hy + 116} L -26,{hy + 116} Z", SK, sw=3, off=(2, 1)))
    for ex in (-92, 92):
        g.append(washed(f"M {ex - 12},{hy - 14} C {ex - 12},{hy - 34} {ex + 12},{hy - 34} {ex + 12},{hy - 14} L {ex + 12},{hy + 20} C {ex + 12},{hy + 40} {ex - 12},{hy + 40} {ex - 12},{hy + 20} Z", SK, sw=2.6, off=(1, 1)))
    g.append(washed(f"M -88,{hy} C -88,{hy - 112} 88,{hy - 112} 88,{hy} C 88,{hy + 100} -88,{hy + 100} -88,{hy} Z", SK, off=(4, 3)))
    # hair with a quiff
    g.append(washed(f"M -92,{hy - 6} C -100,{hy - 96} -40,{hy - 128} 20,{hy - 120} C 70,{hy - 140} 118,{hy - 110} 96,{hy - 60} "
                    f"C 92,{hy - 30} 90,{hy - 14} 88,{hy - 4} C 70,{hy - 60} 20,{hy - 74} -20,{hy - 64} C -50,{hy - 60} -80,{hy - 40} -92,{hy - 6} Z", HR, off=(3, 2)))
    g.append(path(f"M -30,{hy - 100} C 0,{hy - 116} 40,{hy - 118} 70,{hy - 104} M -60,{hy - 70} C -30,{hy - 90} 10,{hy - 96} 40,{hy - 88}", sw=2.2, stroke="#9a7a3a"))
    # face
    lx, ly = look
    for ex in (-32, 32):
        if blink:
            g.append(path(f"M {ex - 14},{hy - 2} C {ex - 6},{hy + 6} {ex + 6},{hy + 6} {ex + 14},{hy - 2}", sw=3.2))
        else:
            g.append(washed(f"M {ex - 14},{hy} C {ex - 14},{hy - 22} {ex + 14},{hy - 22} {ex + 14},{hy} C {ex + 14},{hy + 22} {ex - 14},{hy + 22} {ex - 14},{hy} Z", "#fffdf6", sw=2.6, off=(0, 0)))
            g.append(f'<circle cx="{ex + lx * 5:.1f}" cy="{hy + ly * 6:.1f}" r="8" fill="#2e2520"/>')
    bro = {"neutral": (0, 0), "puzzled": (-14, 6), "raised": (-12, -12)}[brows]
    g.append(path(f"M -50,{hy - 34 + bro[0]} C -40,{hy - 42 + bro[0]} -24,{hy - 42 + bro[0]} -16,{hy - 36 + bro[0] * 0.6} "
                  f"M 16,{hy - 36 + bro[1] * 0.6} C 24,{hy - 42 + bro[1]} 40,{hy - 42 + bro[1]} 50,{hy - 34 + bro[1]}", sw=5, stroke="#9a7a3a"))
    g.append(path(f"M 4,{hy + 6} C 14,{hy + 22} 16,{hy + 30} 2,{hy + 34}", sw=2.8))
    g.append(f'<ellipse cx="-56" cy="{hy + 32}" rx="16" ry="9" fill="{C["blush"]}" opacity="0.35" filter="url(#soft)"/><ellipse cx="56" cy="{hy + 32}" rx="16" ry="9" fill="{C["blush"]}" opacity="0.35" filter="url(#soft)"/>')
    if mouth == "talk":
        g.append(washed(f"M -16,{hy + 50} C -16,{hy + 74} 16,{hy + 74} 16,{hy + 50} C 8,{hy + 46} -8,{hy + 46} -16,{hy + 50} Z", "#7a2f25", sw=2.6, off=(1, 1)))
    elif mouth == "grin":
        g.append(washed(f"M -30,{hy + 46} C -20,{hy + 80} 20,{hy + 80} 30,{hy + 46} C 10,{hy + 52} -10,{hy + 52} -30,{hy + 46} Z", "#7a2f25", sw=2.6, off=(1, 1)))
        g.append(f'<path d="M -26,{hy + 48} C -10,{hy + 54} 10,{hy + 54} 26,{hy + 48} L 24,{hy + 56} C 10,{hy + 60} -10,{hy + 60} -24,{hy + 56} Z" fill="#fffaf0"/>')
    elif mouth == "frown":
        g.append(path(f"M -18,{hy + 60} C -8,{hy + 50} 8,{hy + 50} 18,{hy + 60}", sw=3.2))
    elif mouth == "smile":
        g.append(path(f"M -24,{hy + 50} C -10,{hy + 64} 10,{hy + 64} 24,{hy + 50}", sw=3.2))
    else:
        g.append(path(f"M -16,{hy + 56} C -6,{hy + 54} 6,{hy + 58} 16,{hy + 55}", sw=3.2))
    g.append('</g>')
    # coffee hand (screen-right)
    if coffee and pose != "hold_box":
        g.append(tube([(116, -650), (150, -510), (132, -440)], 44, JK))
        g.append(washed("M 104,-500 L 164,-500 L 156,-400 L 112,-400 Z", "#fbf7ee", sw=2.8, off=(2, 1)))
        g.append(washed("M 108,-470 L 160,-470 L 157,-436 L 111,-436 Z", "#b08a5a", sw=2.4, off=(1, 1)))
        g.append(washed("M 100,-512 L 168,-512 L 166,-498 L 102,-498 Z", "#fbf7ee", sw=2.4, off=(1, 1)))
        g.append(washed("M 112,-450 C 106,-430 150,-424 156,-446 Z", SK, sw=2.4, off=(1, 1)))
    if not coffee and pose != "hold_box":
        g.append(tube([(116, -650), (146, -520), (130, -410)], 44, JK))
        g.append(washed("M 120,-424 C 112,-400 150,-390 150,-418 Z", SK, sw=2.4, off=(1, 1)))
    if pose == "phone" and coffee:
        g.append(path("M 124,-520 C 118,-545 136,-555 130,-580 M 146,-522 C 140,-546 158,-556 152,-580", sw=1.8, stroke="#8c8580"))
    if receive_at is not None:
        # Optional left-hand contact for a handoff; the coffee hand stays steady.
        hx, hy2 = receive_at
        g.append(tube([(-116,-650),(-180,-535),(hx,hy2)],44,JK))
        g.append(washed(f"M {hx-19},{hy2-6} C {hx-25},{hy2+15} {hx+20},{hy2+20} {hx+22},{hy2-6} Z",SK,sw=2.6,off=(1,1)))
    elif pose == "walk":
        motion=math.sin(walk_phase)*swing
        hx,hy2=(-180,-540) if carry_idea else (-142+55*motion,-380-12*abs(motion))
        g.append(tube([(-116,-650),(-160+25*motion,-510),(hx,hy2)],44,JK))
        if carry_idea:
            g.append(bulb(hx,hy2-52,s=1,b=.7,rays=6))
        g.append(washed(f"M {hx-14},{hy2-10} C {hx-23},{hy2+17} {hx+18},{hy2+22} {hx+18},{hy2-4} Z",SK,sw=2.6,off=(1,1)))
    elif pose == "phone":
        g.append(tube([(-116, -650), (-150, -510), (-50, -560)], 44, JK))
        g.append(washed("M -64,-610 L -14,-610 L -14,-524 L -64,-524 Z", "#3d3d3d", sw=2.6, off=(1, 1)))
        g.append(washed("M -60,-546 C -64,-524 -32,-520 -26,-540 Z", SK, sw=2.4, off=(1, 1)))
    elif pose in ("wave", "thumbs_up", "thumbs_down", "point", "shake"):
        tips = {"wave": ((-200, -770), (-180, -900)), "thumbs_up": ((-180, -540), (-120, -640)),
                "thumbs_down": ((-205, -520), (-265, -575)), "point": ((-190, -560), (-290, -560)),
                "shake": ((-180, -520), (-290, -490))}
        el, hd = tips[pose]
        g.append(tube([(-116, -650), el, hd], 44, JK))
        hx, hy2 = hd
        if pose == "wave":
            g.append(hand_extra((hx, hy2 - 10), "open", 0, True))
        elif pose == "point":
            g.append(hand_extra((hx - 10, hy2), "point", 180))
        elif pose == "shake":
            g.append(washed(f"M {hx - 30},{hy2 - 16} C {hx - 34},{hy2 + 14} {hx + 10},{hy2 + 22} {hx + 20},{hy2 + 6} C {hx + 24},{hy2 - 12} {hx}, {hy2 - 26} {hx - 30},{hy2 - 16} Z", SK, sw=2.6, off=(1, 1)))
        elif pose == "thumbs_down":
            # One silhouette connects wrist, curled fingers and a short bent
            # thumb. Readability comes from staging, not an oversized digit.
            fist = (washed("M 36,-20 L 8,-25 C 2,-32 -10,-33 -16,-28 C -24,-32 -34,-28 -35,-21 C -44,-20 -46,-11 -40,-5 C -46,2 -41,12 -33,14 L -28,17 L -35,34 L -34,48 L -25,55 C -20,58 -14,53 -15,47 L -17,36 L -5,19 C 4,23 15,20 21,14 L 36,14 Z", SK, sw=3, off=(1, 1))
                    + path("M -33,-19 L -7,-15 M -38,-6 L -10,-2 M -33,7 L -9,10", sw=2.2)
                    + path("M -28,17 Q -17,13 -8,18 M -32,35 L -23,38", sw=2))
            g.append(f'<g transform="translate({hx},{hy2})">{fist}</g>')
        else:
            # a proper thumb: wide curled fist with finger lines, short chunky thumb leaning off its side
            up = pose == "thumbs_up"
            fist = (washed("M -30,-20 C -32,-30 24,-32 30,-20 L 32,18 C 30,30 -28,30 -30,18 Z", SK, sw=2.6, off=(1, 1))
                    + path("M -26,-7 C -10,-4 10,-4 28,-7 M -26,6 C -10,9 10,9 28,6", sw=2)
                    + path("M 30,-20 C 40,-14 40,14 32,18", sw=2)
                    + washed("M -30,-14 C -40,-36 -34,-70 -16,-74 C -2,-76 6,-64 2,-44 L -2,-18 Z", SK, sw=2.6, off=(1, 1))
                    + path("M -24,-66 C -18,-72 -8,-70 -6,-62", sw=1.8))
            flipy = 1 if up else -1
            g.append(f'<g transform="translate({hx},{hy2}) scale(1,{flipy})">{fist}</g>')
    elif pose == "hold_box":
        g.append(box)
        g.append(tube([(-116, -650), (-170, -520), (-80, -470)], 44, JK))
        g.append(tube([(116, -650), (170, -520), (80, -470)], 44, JK))
        g.append(washed("M -100,-490 C -104,-460 -66,-452 -60,-478 Z", SK, sw=2.4, off=(1, 1)))
        g.append(washed("M 100,-490 C 104,-460 66,-452 60,-478 Z", SK, sw=2.4, off=(1, 1)))
    else:  # phone lowered to the hip
        g.append(tube([(-116, -650), (-150, -520), (-132, -410)], 44, JK))
        g.append(washed("M -152,-430 L -112,-430 L -112,-366 L -152,-366 Z", "#3d3d3d", sw=2.6, off=(1, 1)))
        g.append(washed("M -152,-414 C -160,-390 -116,-384 -114,-408 Z", SK, sw=2.4, off=(1, 1)))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


# ---------- the fork signs ----------
def dragon(x, y, s=1.0):
    g = []
    g.append(path("M -80,4 C -130,14 -150,-6 -176,-34", sw=16) + path("M -80,4 C -130,14 -150,-6 -176,-34", sw=10, stroke="#6f8f4a"))
    g.append(washed("M -186,-30 L -200,-58 L -170,-46 Z", "#6f8f4a", sw=2.6, off=(1, 1)))
    g.append(washed("M -10,-34 L -70,-150 C -50,-128 -30,-126 -16,-140 C -4,-118 16,-118 28,-134 C 30,-96 30,-62 22,-36 Z", "#86a35a", off=(2, 2)))
    g.append(washed("M -90,0 C -70,-40 0,-50 40,-30 C 60,-50 70,-80 90,-100 C 100,-112 130,-112 142,-98 "
                    "C 156,-92 158,-80 144,-76 C 124,-74 110,-70 102,-56 C 92,-30 82,0 62,16 C 20,30 -60,30 -90,0 Z", "#6f8f4a", off=(3, 2)))
    g.append(path("M -50,20 L -54,44 M 30,20 L 34,44", sw=10) + path("M -50,20 L -54,44 M 30,20 L 34,44", sw=5, stroke="#6f8f4a"))
    g.append(path("M 96,-104 L 90,-126 L 108,-110 M 114,-110 L 116,-132 L 126,-110", sw=3))
    g.append(f'<circle cx="122" cy="-94" r="6" fill="{INK}"/>')
    g.append(washed("M 154,-84 C 190,-110 220,-80 250,-100 C 236,-70 260,-60 240,-44 C 220,-54 190,-50 154,-76 Z", "#e8823a", sw=2.6, off=(2, 1)))
    g.append(washed("M 160,-82 C 190,-96 206,-80 226,-88 C 216,-70 226,-64 214,-58 C 196,-64 180,-64 160,-78 Z", "#ffd659", sw=0.1, off=(0, 0)))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def sea_monster(x, y, s=1.0):
    g = []
    g.append(washed("M -190,14 C -214,-40 -170,-100 -130,-86 C -150,-74 -176,-40 -160,14 Z", "#5d7f8e", off=(2, 1)))
    for a in (-110, -10):
        g.append(washed(f"M {a},14 C {a + 10},-56 {a + 70},-56 {a + 80},14 Z", "#4f6f80", off=(3, 2)))
        g.append(washed(f"M {a + 26},-38 L {a + 40},-74 L {a + 54},-38 Z", "#86a6b4", sw=2.6, off=(1, 1)))
    g.append(washed("M 90,14 C 80,-60 96,-126 146,-126 C 186,-126 198,-96 178,-80 C 158,-72 138,-72 128,-52 C 124,-22 128,0 132,14 Z", "#4f6f80", off=(3, 2)))
    g.append(f'<circle cx="150" cy="-104" r="12" fill="#fffdf6" stroke="{INK}" stroke-width="3"/><circle cx="154" cy="-102" r="5" fill="{INK}"/>')
    g.append(path("M 140,-84 C 156,-76 172,-78 184,-86", sw=3))
    g.append(path("M 150,-80 L 152,-72 M 162,-80 L 163,-72 M 172,-82 L 172,-74", sw=2, stroke="#fffdf6"))
    g.append(path("M -220,20 C -180,8 -140,32 -100,20 C -60,8 -20,32 20,20 C 60,8 100,32 140,20 C 170,10 200,26 220,20", stroke="#3f6a8a", sw=5))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'


def signpost(x, y, s=1.0, side="left", title="", sub=(), creature="dragon"):
    g = [washed("M -10,0 L 10,0 L 10,-520 L -10,-520 Z", "#8a6a48", off=(2, 1))]
    if side == "left":
        board = "M 160,-520 L -260,-520 L -320,-420 L -260,-320 L 160,-320 Z"
        cx = -60
    else:
        board = "M -160,-520 L 260,-520 L 320,-420 L 260,-320 L -160,-320 Z"
        cx = 60
    g.append(washed(board, "#f1e6cf", off=(4, 3)))
    g.append(dragon(cx, -420, 0.62) if creature == "dragon" else sea_monster(cx, -400, 0.62))
    g.append(washed(f"M {cx - 210},-310 L {cx + 210},-310 L {cx + 210},{-300 + 34 * (len(sub) + 1) + 10} L {cx - 210},{-300 + 34 * (len(sub) + 1) + 10} Z", "#f6efe2", sw=3, off=(3, 2)))
    g.append(text(cx, -274, title, size=30))
    for i, t in enumerate(sub):
        g.append(text(cx, -240 + i * 34, t, size=22, weight="normal"))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'
