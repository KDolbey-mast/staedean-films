"""MOUNT STAEDEAN, chapter 2: THE DOOR. About 45 seconds, same PM, same felt-tip look.

Idea -> a small door next to the mountain window ("CUSTOMER 20 m") -> quick customer visits (MON fail, TUE fix,
THU yes) -> handshake ("When can I have it?") -> product catapulted over Mount Staedean to the customer ->
shop window where everyone from the climb now serves the queue -> the door's sign becomes "HOW WE WORK".
"""
import math, os, sys, random
import film                                    # helpers, and story.wrap patched to return (art, view)
from film import (ease, lerp, ramp, step, flap, oflap, walk_legs, boil, W_, walker, stand, mirror, page_svg, anim_pages,
                  FPS, FULL)
import story
from story import *
from office import back_wall, window, calendar, poster, wastebin, chair_back, desk_top, mug, tray, notepad, NECK, THOUGHT_BULB
from rb import wrap_rb
from render import render

TEALC = "#17c8be"
DOOR_X, DOOR_W, DOOR_TOP = 1890, 190, 330
DOOR_VIEW = (1000, 70, 1300, 731.25)
VISIT_VIEW = (300, 290, 1320, 742.5)
TABLE_X, TABLE_TOP = 1040, GROUND - 200
PM_X, MAKER_X, CUST2_X = 760, 950, 1300


# ---------------- new props ----------------
def door(open_=0.0, sign="INNOVATION", sub="CUSTOMER  20 m", flip=1.0):
    x0, x1, y0, y1 = DOOR_X, DOOR_X + DOOR_W, DOOR_TOP, 812
    g = []
    if open_ > 0:
        g.append(f'<rect x="{x0}" y="{y0}" width="{DOOR_W}" height="{y1 - y0}" fill="#fff6d0"/>')
        g.append(f'<circle cx="{x0 + DOOR_W / 2}" cy="{(y0 + y1) / 2}" r="{260 * open_:.0f}" fill="url(#glowG)" opacity="{0.6 * open_:.2f}"/>')
        g.append(path(f"M {x0 + 20},{y1} L {x0 + 60},{y0 + 200} M {x1 - 20},{y1} L {x1 - 60},{y0 + 200}", sw=2, stroke="#e8c96a"))
    # the door leaf swings inward (gets narrower)
    w = DOOR_W * (1 - 0.82 * open_)
    g.append(washed(f"M {x0},{y0} L {x0 + w:.0f},{y0 + 18 * open_:.0f} L {x0 + w:.0f},{y1 - 10 * open_:.0f} L {x0},{y1} Z", "#ead7b0", off=(3, 2)))
    if open_ < 0.5:
        g.append(f'<circle cx="{x0 + w - 26:.0f}" cy="{(y0 + y1) / 2 + 20:.0f}" r="9" fill="#c9a24a" stroke="#2e2520" stroke-width="2.4"/>')
        g.append(path(f"M {x0 + 30},{y0 + 40} L {x0 + w - 30:.0f},{y0 + 40} L {x0 + w - 30:.0f},{y0 + 190} L {x0 + 30},{y0 + 190} Z", sw=2.2))
    # teal frame
    g.append(washed(f"M {x0 - 22},{y1} L {x0 - 22},{y0 - 22} L {x1 + 22},{y0 - 22} L {x1 + 22},{y1} L {x1},{y1} L {x1},{y0} L {x0},{y0} L {x0},{y1} Z", TEALC, off=(3, 2)))
    # the sign above (flips over at the end)
    sy = DOOR_TOP - 120
    inner = (washed(f"M -150,-46 L 150,-46 L 150,46 L -150,46 Z", "#fbf7ee", off=(3, 2))
             + text(0, -2 if sub else 12, sign, size=38 if len(sign) < 11 else 31, spacing=1)
             + (text(0, 32, sub, size=22, weight="normal") if sub else ""))
    g.append(path(f"M {x0 + 30},{y0 - 22} L {x0 + 50},{sy + 46} M {x1 - 30},{y0 - 22} L {x1 - 50},{sy + 46}", sw=2.4))
    g.append(f'<g transform="translate({x0 + DOOR_W / 2},{sy}) scale(1,{max(0.04, abs(flip)):.2f})">{inner}</g>')
    return "".join(g)


def recolour(svg, mapping):
    for a, b in mapping.items():
        svg = svg.replace(f'"{a}"', f'"{b}"')
    return svg


MAKER = {"#7b4b2b": "#2c2a2e", "#5e3820": "#1c1a1d", "#b9d3e6": "#e9c46a", "#9dbcd4": "#d4ad52", "#e3eef6": "#f4e3b0",
         "#c0623a": "#3d6a52", "#9c4a2b": "#2f5240", "#3a3a40": "#5a4a3c"}
COLLEAGUES = [
    {"#7b4b2b": "#c9a043", "#5e3820": "#9a7a2a", "#b9d3e6": "#e8b4b8", "#9dbcd4": "#d39ca1", "#c0623a": "#5b5fa8", "#9c4a2b": "#44488a"},
    {"#7b4b2b": "#a0522d", "#5e3820": "#7a3a1d", "#b9d3e6": "#cfe8c8", "#9dbcd4": "#b4d4ac", "#c0623a": "#9b4d6f", "#9c4a2b": "#7a3a56"},
    {"#7b4b2b": "#3b2f2f", "#5e3820": "#241c1c", "#b9d3e6": "#f6e3b4", "#9dbcd4": "#e4cc92", "#c0623a": "#8e2f45", "#9c4a2b": "#6e2335"},
]


def beanie():
    return (washed("M -96,-150 C -100,-250 110,-250 104,-150 C 60,-170 -50,-170 -96,-150 Z", "#b5523b", off=(2, 2))
            + washed("M -102,-160 L 108,-160 L 108,-130 L -102,-130 Z", "#9a4330", sw=2.6, off=(1, 1)))


def maker(x, y, s, *, arms=None, front="", face=None, legs="stand", phase=None, lean=0):
    face = face or dict(look=(1, -0.2), brows="happy", mouth="smile")
    arms = arms or [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (180, 230), (120, 330), "rest", True)]
    legs_mode = walk_legs(phase) if phase is not None else legs
    hat = f'<g transform="translate(6,-50)">{beanie()}</g>'
    svg = pm_full(x, y - (6 * abs(math.sin(phase)) * s if phase is not None else 0), s, legs_mode=legs_mode, lean=lean,
                  arms=arms, front=hat + front, **face)
    return recolour(svg, MAKER)


def colleague(i, x, y, s, phase, b=0.8):
    face = dict(look=(-1, -0.2), brows="happy", mouth="smile")
    svg = walker(x, y, s, phase, b=b, face=face, mirror_it=True)
    return recolour(svg, COLLEAGUES[i % len(COLLEAGUES)])


def proto(x, y, v, glow=0.0):
    """Prototype standing on the table; (x, y) = bottom centre."""
    if v == 1:  # crude cardboard
        return (washed(f"M {x - 70},{y} L {x - 64},{y - 110} L {x + 72},{y - 104} L {x + 66},{y} Z", "#c8a26b", off=(3, 2))
                + path(f"M {x - 60},{y - 100} L {x + 60},{y - 10} M {x + 60},{y - 100} L {x - 60},{y - 10}", sw=6, stroke="#e6d7b0")
                + path(f"M {x - 20},{y - 60} C {x - 20},{y - 90} {x + 20},{y - 90} {x + 20},{y - 60} L {x + 10},{y - 44} L {x - 10},{y - 44} Z", sw=2.4))
    if v == 2:  # better, with a dial and antenna
        return (washed(f"M {x - 74},{y} L {x - 74},{y - 104} C {x - 74},{y - 116} {x + 74},{y - 116} {x + 74},{y - 104} L {x + 74},{y} Z", "#b9c4cc", off=(3, 2))
                + f'<circle cx="{x - 30}" cy="{y - 56}" r="22" fill="#fbf7ee" stroke="#2e2520" stroke-width="3"/>'
                + path(f"M {x - 30},{y - 56} L {x - 18},{y - 70}", sw=3)
                + path(f"M {x + 30},{y - 112} L {x + 46},{y - 170}", sw=3) + f'<circle cx="{x + 46}" cy="{y - 172}" r="7" fill="#e05a4f"/>'
                + path(f"M {x + 14},{y - 40} L {x + 56},{y - 40} M {x + 14},{y - 60} L {x + 56},{y - 60}", sw=2.4))
    # v3: sleek device with the idea glowing inside
    return (washed(f"M {x - 80},{y} C {x - 86},{y - 60} {x - 80},{y - 126} {x},{y - 130} C {x + 80},{y - 126} {x + 86},{y - 60} {x + 80},{y} Z", "#f5f2ea", off=(3, 2))
            + washed(f"M {x - 80},{y - 22} L {x + 80},{y - 22} L {x + 80},{y - 10} L {x - 80},{y - 10} Z", TEALC, sw=2, off=(1, 1))
            + bulb(x, y - 70, s=0.6, b=glow, rays=0 if glow < 0.6 else 6))


def product_box(x, y, s=1.0, rot=0, glow=0.9):
    inner = (washed("M -80,-70 L 80,-70 L 80,70 L -80,70 Z", "#d2ad74", off=(3, 2))
             + washed("M -80,-10 L 80,-10 L 80,10 L -80,10 Z", TEALC, sw=2.2, off=(1, 1))
             + washed("M -10,-70 L 10,-70 L 10,70 L -10,70 Z", TEALC, sw=2.2, off=(1, 1))
             + washed("M 0,-70 C -40,-110 -60,-80 0,-70 C 60,-80 40,-110 0,-70 Z", TEALC, sw=2.4, off=(1, 1))
             + bulb(-44, -36, s=0.32, b=glow, rays=0))
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot:.1f}) scale({s})">{inner}</g>'


def table(x=TABLE_X, top=TABLE_TOP, cup=False):
    g = [path(f"M {x},{top + 20} L {x},{GROUND - 6}", sw=12), path(f"M {x},{top + 20} L {x},{GROUND - 6}", sw=6, stroke="#9a9a9a"),
         washed(f"M {x - 70},{GROUND} C {x - 70},{GROUND - 18} {x + 70},{GROUND - 18} {x + 70},{GROUND} Z", "#9a9a9a", sw=2.6, off=(1, 1)),
         washed(f"M {x - 160},{top} C {x - 160},{top - 26} {x + 160},{top - 26} {x + 160},{top} C {x + 160},{top + 26} {x - 160},{top + 26} {x - 160},{top} Z", "#f0ece2", off=(3, 2))]
    if cup:
        g.append(washed(f"M {x + 90},{top - 4} L {x + 120},{top - 4} L {x + 116},{top - 54} L {x + 94},{top - 54} Z", "#fbf7ee", sw=2.4, off=(1, 1))
                 + washed(f"M {x + 92},{top - 20} L {x + 118},{top - 20} L {x + 117},{top - 36} L {x + 93},{top - 36} Z", "#b08a5a", sw=2, off=(1, 1)))
    return "".join(g)


def parasol(x=TABLE_X):
    g = [path(f"M {x},{TABLE_TOP - 10} L {x},{TABLE_TOP - 430}", sw=6)]
    cols = ["#e05a4f", "#fbf7ee"] * 4
    for i in range(8):
        a0, a1 = -260 + i * 65, -260 + (i + 1) * 65
        g.append(washed(f"M {x},{TABLE_TOP - 470} L {x + a0},{TABLE_TOP - 380} C {x + (a0 + a1) / 2},{TABLE_TOP - 400} {x + (a0 + a1) / 2},{TABLE_TOP - 400} {x + a1},{TABLE_TOP - 380} Z", cols[i], sw=2.4, off=(2, 1)))
    return "".join(g)


def learned_bin(x=440, contents=0):
    g = []
    for k in range(contents):
        g.append(bulb(x + 20 - 25 * k, GROUND - 150, s=0.45, b=0, dead=True, rot=-30 + 25 * k))
    g.append(washed(f"M {x - 70},{GROUND - 140} L {x + 70},{GROUND - 140} L {x + 58},{GROUND} L {x - 58},{GROUND} Z", "#8fa6b0", off=(3, 2)))
    g.append(f'<ellipse cx="{x}" cy="{GROUND - 140}" rx="70" ry="10" fill="none" stroke="#2e2520" stroke-width="3"/>')
    g.append(washed(f"M {x - 54},{GROUND - 100} L {x + 54},{GROUND - 100} L {x + 50},{GROUND - 64} L {x - 50},{GROUND - 64} Z", "#fbf7ee", sw=2.2, off=(1, 1)))
    g.append(text(x, GROUND - 74, "LEARNED", size=22))
    return "".join(g)


def day_card(view, label, t):
    s = ramp(t, [(0, 1.5), (0.15, 1.0)])
    x, y = view[0] + 60, view[1] + 40
    inner = (washed("M 0,0 L 220,0 L 222,170 L 2,172 Z", "#fbf7ee", sw=3, off=(3, 2))
             + washed("M 0,0 L 220,0 L 220,44 L 0,44 Z", "#b8483a", sw=2.6, off=(1, 1))
             + text(111, 124, label, size=46))
    return f'<g transform="translate({x},{y}) rotate(-6) scale({s:.2f})">{inner}</g>'


def catapult(x, y, s=1.0, arm=-30, load=""):
    g = [washed("M -160,0 L 160,0 L 140,-30 L -140,-30 Z", "#a87a4e", off=(3, 2)),
         path("M -120,-30 L -40,-200 L 40,-30 M -40,-200 L 120,-30", sw=12) + path("M -120,-30 L -40,-200 L 40,-30 M -40,-200 L 120,-30", sw=7, stroke="#b98a5e")]
    for wx in (-110, 110):
        g.append(f'<circle cx="{wx}" cy="0" r="34" fill="#c9a77a" stroke="#2e2520" stroke-width="3.4"/>')
    arm_svg = (path("M 0,0 L 260,0", sw=16) + path("M 0,0 L 260,0", sw=10, stroke="#b98a5e")
               + washed("M 240,-10 C 240,-60 320,-60 320,-10 Z", "#a87a4e", sw=3, off=(2, 1))
               + f'<g transform="translate(280,-40)">{load}</g>')
    g.append(f'<g transform="translate(-40,-200) rotate({arm:.1f})">{arm_svg}</g>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def path_set(door_open=1.0):
    g = [sky()]
    g.append(f'<path d="M -100,700 C 300,640 600,690 900,650 C 1200,610 1500,660 2020,620 L 2020,1100 L -100,1100 Z" fill="#b9c6b0"/>')
    # Mount Staedean, far away and irrelevant
    g.append(washed("M 1500,700 C 1620,560 1700,420 1760,330 C 1820,420 1900,560 2020,700 Z", C["mountain"], off=(3, 2)))
    g.append(washed("M 1760,330 C 1780,360 1800,390 1812,410 C 1790,400 1770,420 1755,400 C 1740,420 1724,405 1710,412 C 1730,380 1745,350 1760,330 Z", C["snow"], sw=2.4, off=(2, 1)))
    g.append(washed(f"M -60,{GROUND - 6} C 600,{GROUND - 20} 1300,{GROUND - 6} 1980,{GROUND - 20} L 1980,1100 L -60,1100 Z", "#a9b394", off=(4, 3)))
    # office outside wall with the teal door
    g.append(washed("M -60,860 L -60,260 L 300,260 L 300,860 Z", "#d9cdb5", off=(4, 3)))
    g.append(f'<rect x="120" y="440" width="150" height="420" fill="#fff6d0" stroke="#2e2520" stroke-width="3"/>')
    g.append(washed("M 98,862 L 98,418 L 292,418 L 292,862 L 270,862 L 270,440 L 120,440 L 120,862 Z", TEALC, off=(3, 2)))
    g.append(washed("M 270,440 L 300,452 L 300,850 L 270,862 Z", "#ead7b0", sw=2.6, off=(1, 1)))
    # stepping stones and the "20 m" post
    for i, sx in enumerate((360, 470, 590, 710, 830)):
        g.append(washed(f"M {sx - 46},{GROUND + 26 + (i % 2) * 6} C {sx - 46},{GROUND + 6} {sx + 46},{GROUND + 6} {sx + 46},{GROUND + 26} C {sx + 46},{GROUND + 44} {sx - 46},{GROUND + 44} {sx - 46},{GROUND + 26} Z", "#cfc8bb", sw=2.4, off=(1, 1)))
    g.append(marker_post(560, GROUND - 10, 0.7, "20 m"))
    return "".join(g)


def office_no_pm(door_open=0.0, sign="INNOVATION", sub="CUSTOMER  20 m", flip=1.0):
    return (back_wall() + window() + calendar() + poster() + wastebin(("dead_bulb", "paper")) + chair_back() + desk_top()
            + mug() + tray() + notepad("sketch3") + door(door_open, sign, sub, flip))


# ---------------- shots ----------------
SHOTS = []


def shot(name, dur, cues=()):
    def deco(fn):
        SHOTS.append(dict(name=name, dur=dur, draw=fn, cues=list(cues)))
        return fn
    return deco


A_WRITE = story.A_WRITE


@shot("O1_the_door", 4.2, cues=[(0, "room_tone", {"d": 4.2}, 0.07, "amb"), (0, "office_theme", {"d": 1.4}, 0.3, "music"),
                                 (0.2, "scribble", {"d": 0.5}, 0.45), (0.6, "pop", {}, 0.45), (1.5, "tiny_dun", {}, 0.4, "music"),
                                 (1.6, "brr", {}, 0.25), (2.9, "ding", {}, 0.35), (3.6, "door_creak", {}, 0.35), (3.7, "swell_soft", {}, 0.2, "music")])
def _(t, n):
    view = ramp(t, [(0, film.AO.MED), (1.3, film.AO.MED), (2.0, (700, 70, 1300, 731.25)), (2.9, DOOR_VIEW)])
    look = step(t, [(0, (0.5, 0.9)), (0.7, (0.35, -1.0)), (1.3, (1.0, -0.3))])
    head_rot = step(t, [(0, 6), (0.7, -7), (1.3, -5)])
    brows = step(t, [(0, "neutral"), (0.7, "raised"), (1.6, "sad"), (2.9, "raised"), (3.4, "happy")])
    mouth = step(t, [(0, "neutral"), (0.7, "o"), (1.6, "wobbly"), (2.9, "o"), (3.4, "grin")])
    writing = t < 0.7
    arms = [list(a) for a in A_WRITE]
    if writing:
        hx, hy = arms[1][2]
        arms[1][2] = (hx + 9 * math.sin(2 * math.pi * 3.2 * t), hy + 3 * math.sin(2 * math.pi * 6.4 * t))
    arms = [tuple(a) for a in arms]
    extra = door(ramp(t, [(3.6, 0.0), (4.2, 1.0)]))
    if t >= 0.6:
        sc = ramp(t, [(0.6, 0.0), (0.72, 1.15), (0.85, 0.95)])
        extra += bulb(*THOUGHT_BULB, s=sc, b=ramp(t, [(0.6, 0.3), (3.6, 0.6)]), pop=0.6 < t < 1.0)
    art, _ = story.office_frame(head_rot=head_rot, look=look, brows=brows, mouth=mouth, arms=arms, pad="sketch1",
                                bin_contents=("dead_bulb", "paper"), extra=extra, view=view)
    return W_((art, view), n)


@shot("P1_twenty_metres", 2.2, cues=[(0, "wind", {"d": 2.2, "intensity": 0.15}, 0.04, "amb"), (0.0, "theme2", {"d": 17.7}, 0.26, "music"),
                                      (0.1, "steps", {"d": 2.0, "rate": 2.6}, 0.3), (1.2, "mumble", {"d": 0.4, "f0": 150, "rate": 4}, 0.35)])
def _(t, n):
    px = ramp(t, [(0, 230), (2.4, 660)], smooth=False)
    mx = ramp(t, [(0.3, 120), (2.4, 440)], smooth=False)
    ph = t * 2 * math.pi * 1.3
    art = path_set() + parasol() + table()
    art += customer(CUST2_X, GROUND - 16, 0.52, "wave" if (n // 4) % 2 else "phone", "smile", (-1, 0), coffee=True)
    if t > 0.3:
        art += maker(mx, GROUND + 6, 0.42, phase=(t - 0.3) * 2 * math.pi * 1.3,
                     arms=[(SHL, (-170, 230), (-60, 250), "cup"), (SHR, (180, 230), (60, 250), "cup", True)],
                     front=proto(0, 220, 1).replace("translate", "translate"))
    art += walker(px, GROUND + 6, 0.42, ph, b=0.6, face=dict(look=(1, -0.3), brows="happy", mouth="grin"))
    return W_((art, None), n)


def visit(t, n, *, day, v, b, pm_face, cust_pose, cust_mouth="flat", cust_look=(-1, 0.3), cust_brows="neutral", bubble_=None,
          maker_arms=None, maker_face=None, bulb_held=True, bin_n=0, extra="", glow=0.0, view=VISIT_VIEW, cust_blink=False):
    art = path_set() + parasol() + learned_bin(440, bin_n)
    art += maker(MAKER_X, GROUND - 40, 0.42, arms=maker_arms, face=maker_face or dict(look=(1, 0.2), brows="happy", mouth="smile"))
    art += table() + proto(TABLE_X, TABLE_TOP - 6, v, glow)
    art += customer(CUST2_X, GROUND - 16, 0.52, cust_pose, cust_mouth, cust_look, cust_brows, blink=cust_blink)
    pm_arms = [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)]
    front = bulb(190, 58, s=1, b=b, rays=0 if b < 0.6 else 7, dead=(b <= 0.0)) if bulb_held else ""
    art += pm_full(PM_X, GROUND + 6, 0.42, legs_mode="stand", lean=film.breath(1.2), arms=pm_arms, front=front, **pm_face)
    if bubble_:
        art += bubble_
    art += day_card(view, day, t) + extra
    return W_((art, view), n)


@shot("V1_week1", 4.6, cues=[(0, "flip", {}, 0.4), (0.3, "mumble", {"d": 0.8, "f0": 165, "rate": 7}, 0.4),
                               (1.6, "mumble", {"d": 0.7, "f0": 130, "rate": 3}, 0.4), (2.2, "fizzle", {"d": 0.6}, 0.35),
                               (3.0, "whoosh", {"d": 0.6}, 0.4), (3.7, "clang", {}, 0.3)])
def _(t, n):
    talking = 0.3 < t < 1.1
    b = 0.6 if t < 2.2 else ([0.3, 0.0, 0.2, 0.0][n % 4] if t < 2.8 else 0.0)
    shake = t > 1.6 and t < 2.6
    cl = (-1 if (n // 2) % 2 else 1, 0.2) if shake else (-1, 0.3)
    face = dict(look=(1, -0.2), brows="raised", mouth=flap(n) if talking else ("o" if t < 2.8 else "smile"),
                eyes="closed_happy" if 3.0 < t < 4.2 else "open")
    if t > 2.8:
        face["brows"] = "happy"
    bub = bubble(800, 470, 260, 110, (760, 560), lines=2, seed=3) if talking else ""
    extra = ""
    held = t < 3.0
    if 3.0 <= t < 3.7:
        p = (t - 3.0) / 0.7
        x0, y0 = PM_X + 0.42 * 190, GROUND + 6 - 0.42 * (700 - 58)
        x1, y1 = 440, GROUND - 150
        cx, cy = (x0 + x1) / 2, y0 - 260
        bx = (1 - p) ** 2 * x0 + 2 * (1 - p) * p * cx + p ** 2 * x1
        by = (1 - p) ** 2 * y0 + 2 * (1 - p) * p * cy + p ** 2 * y1
        extra = bulb(bx, by, s=0.45, b=0, dead=True, rot=-200 * p)
    return visit(t, n, day="WEEK 1", v=1, b=b, bulb_held=held, bin_n=1 if t >= 3.7 else 0, extra=extra,
                 pm_face=face, cust_pose="thumbs_down" if t > 1.6 else "phone", cust_mouth="frown" if t > 1.6 else "flat",
                 cust_look=cl, cust_brows="puzzled" if t > 1.4 else "neutral", bubble_=bub)


@shot("V2_week2", 3.8, cues=[(0, "flip", {}, 0.4), (0.4, "mumble", {"d": 0.6, "f0": 140, "rate": 3, "question": True}, 0.4),
                                (1.4, "hammer", {"d": 1.4}, 0.45), (2.9, "mumble", {"d": 0.4, "f0": 150, "rate": 3}, 0.35)])
def _(t, n):
    hammering = 1.4 < t < 2.8
    up = (n // 2) % 2 == 0
    hammer = (path("M 0,0 L 0,-120", sw=10) + path("M 0,0 L 0,-120", sw=6, stroke="#b98a5e")
              + washed("M -40,-150 L 40,-150 L 40,-110 L -40,-110 Z", "#8a8f90", sw=3, off=(1, 1)))
    if hammering:
        hy = 150 if up else 230
        m_arms = [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (230, 120), (260, hy), "fist", True)]
        m_front = f'<g transform="translate(260,{hy}) rotate({-60 if up else 10})">{hammer}</g>'
    else:
        m_arms = None
        m_front = ""
    b = ramp(t, [(0, 0.62), (2.9, 0.62), (3.6, 0.85)])
    pose = "point" if 0.4 < t < 2.9 else "thumbs_up" if t > 3.4 else "phone"
    hx = f'<g transform="translate({MAKER_X},{GROUND - 40}) scale(0.42) translate(0,-700)">{m_front}</g>' if m_front else ""
    return visit(t, n, day="WEEK 2", v=2, b=b, bin_n=1,
                 pm_face=dict(look=(1, -0.1), brows="quizzical" if t < 2.9 else "happy", mouth="hmm" if t < 2.9 else "smile"),
                 cust_pose=pose, cust_mouth="flat" if t < 2.9 else "smile", cust_brows="puzzled" if t < 2.9 else "neutral",
                 maker_arms=m_arms, maker_face=dict(look=(1, 0.6), brows="furrow", mouth="flat") if hammering else None, extra=hx)


@shot("V3_week3", 3.5, cues=[(0, "flip", {}, 0.4), (0.9, "chord_up", {}, 0.35, "music"), (1.0, "mumble", {"d": 0.5, "f0": 170, "rate": 4}, 0.4)])
def _(t, n):
    yes = t > 0.9
    m_arms = [(SHL, (-200, 100), (-230, -40), "open"), (SHR, (200, 100), (230, -40), "open", True)] if yes and (n // 3) % 2 else None
    return visit(t, n, day="WEEK 3", v=3, b=0.0, bulb_held=False, glow=ramp(t, [(0, 0.45), (1.0, 0.75)]), bin_n=1,
                 pm_face=dict(look=(1, -0.2), brows="happy" if yes else "raised", mouth="grin" if yes else "o"),
                 cust_pose="thumbs_up" if yes else "phone", cust_mouth="grin" if yes else "flat", cust_look=(-1, 0.2),
                 cust_brows="raised" if yes else "neutral", maker_arms=m_arms,
                 maker_face=dict(look=(1, -0.4), brows="happy", mouth="grin") if yes else None)


HAND_VIEW = (620, 300, 1000, 562.5)


@shot("H1_handshake", 3.6, cues=[(0.2, "pat", {}, 0.4), (0.5, "pat", {}, 0.4), (0.8, "pat", {}, 0.4),
                                  (1.6, "mumble", {"d": 1.1, "f0": 150, "rate": 4.5, "question": True}, 0.5), (2.9, "swell_soft", {}, 0.18, "music")])
def _(t, n):
    bob = 10 * math.sin(t * 2 * math.pi * 3) if 0.2 < t < 1.2 else 0
    art = path_set() + parasol()
    art += customer(CUST2_X, GROUND - 16, 0.52, "shake", oflap(n) if 1.6 < t < 2.6 else "grin", (-1, 0.2), "raised" if t > 1.6 else "neutral")
    art += pm_full(1000, GROUND + 6, 0.42, legs_mode="stand", lean=film.breath(1.0),
                   arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (230, 140), (330, 40 + bob), "fist", True)],
                   look=(1, -0.4), brows="happy", mouth="grin")
    if t > 1.6:
        art += bubble(940, 420, 420, 130, (1250, 390), words="When can I have it?", size=40)
    return W_((art, HAND_VIEW), n)


@shot("L1_over_the_mountain", 4.2, cues=[(0, "wind", {"d": 4.2, "intensity": 0.25}, 0.05, "amb"), (0.1, "creak", {}, 0.4),
                                          (1.0, "twang", {}, 0.5), (1.0, "whoosh", {"d": 1.6, "lo": 300, "hi": 3000}, 0.45),
                                          (2.0, "triumph", {}, 0.8, "music")])
def _(t, n):
    art = big_mountain(show_sign=True)
    art += day_card(FULL, "WEEK 4", t)
    arm = ramp(t, [(0, -20), (0.9, -32), (1.08, 70)], smooth=False)
    flying = t >= 1.05
    load = "" if flying else product_box(0, 0, 0.45)
    art += catapult(330, 1000, 0.55, arm=arm, load=load)
    cheer = t > 1.2 and (n // 3) % 2
    pm_arms = [(SHL, (-200, 100), (-230, -40), "open"), (SHR, (200, 100), (230, -40), "open", True)] if cheer else None
    art += pm_full(560, 1012, 0.2, legs_mode="stand", arms=pm_arms or [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (150, 320), "rest", True)],
                   look=(0.6, -1), brows="happy", mouth="grin" if t > 1.2 else "smile")
    art += maker(130, 1012, 0.2, arms=pm_arms, face=dict(look=(1, -1), brows="happy", mouth="grin"))
    if flying:
        p = min(1.0, (t - 1.05) / 1.9)
        x0, y0, cx, cy, x1, y1 = 420, 820, 940, -1150, 1800, 1150
        bx = (1 - p) ** 2 * x0 + 2 * (1 - p) * p * cx + p ** 2 * x1
        by = (1 - p) ** 2 * y0 + 2 * (1 - p) * p * cy + p ** 2 * y1
        q = max(0, p - 0.12)
        tx = (1 - q) ** 2 * x0 + 2 * (1 - q) * q * cx + q ** 2 * x1
        ty = (1 - q) ** 2 * y0 + 2 * (1 - q) * q * cy + q ** 2 * y1
        art += path(f"M {tx:.0f},{ty:.0f} L {bx:.0f},{by:.0f}", sw=3, extra='stroke-dasharray="10 12"')
        if p < 1:
            art += product_box(bx, by, 0.5, rot=360 * p)
    return W_((art, None), n)


@shot("L2_got_it", 2.0, cues=[(0.45, "thump", {}, 0.5), (0.5, "mumble", {"d": 0.4, "f0": 190, "rate": 3}, 0.4), (0.6, "ding", {}, 0.3)])
def _(t, n):
    caught = t >= 0.5
    by = ramp(t, [(0, 120), (0.5, GROUND - 16 - 0.52 * 480)], smooth=False)
    art = path_set() + parasol() + table(cup=True) + learned_bin(440, 1)
    if caught:
        box = product_box(0, -470, 1.0, glow=1.0)
        art += customer(CUST2_X, GROUND - 16 + (6 if t < 0.65 else 0), 0.52, "hold_box", "grin", (0, 0.4), "raised", box=box)
    else:
        art += customer(CUST2_X, GROUND - 16, 0.52, "wave", "o", (0, -1), "raised", coffee=False)
        art += product_box(CUST2_X, by, 0.52, rot=20 * t)
    return W_((art, (700, 300, 1100, 618.75)), n)


SHOP_COUNTER = GROUND - 190


def shop_set(shutter):
    g = [sky()]
    g.append(washed(f"M -60,{GROUND - 6} C 600,{GROUND - 20} 1300,{GROUND - 6} 1980,{GROUND - 20} L 1980,1100 L -60,1100 Z", "#cdb790", off=(4, 3)))
    g.append(washed("M 220,900 L 220,190 L 1470,190 L 1470,900 Z", "#e8dcc2", off=(5, 3)))
    g.append(f'<rect x="300" y="330" width="1090" height="380" fill="#f6f1e4" stroke="#2e2520" stroke-width="3.4"/>')
    return "".join(g)


def shop_front(shutter, num):
    g = []
    # shutter (rolls up)
    sh_y = 330 + 380 * (1 - shutter)
    if shutter > 0.01:
        g.append(f'<rect x="300" y="330" width="1090" height="{max(0, 380 * shutter):.0f}" fill="#b8c0c6" stroke="#2e2520" stroke-width="3"/>')
        for k in range(int(380 * shutter / 30)):
            g.append(path(f"M 300,{330 + 30 * (k + 1)} L 1390,{330 + 30 * (k + 1)}", sw=2, stroke="#8a9298"))
    # counter
    g.append(washed(f"M 260,{SHOP_COUNTER} L 1430,{SHOP_COUNTER} L 1430,900 L 260,900 Z", "#c4a77c", off=(4, 3)))
    g.append(washed(f"M 240,{SHOP_COUNTER - 22} L 1450,{SHOP_COUNTER - 22} L 1450,{SHOP_COUNTER + 6} L 240,{SHOP_COUNTER + 6} Z", "#9a6f47", off=(3, 2)))
    # teal awning + sign
    for i in range(10):
        x0 = 200 + i * 129
        g.append(washed(f"M {x0},190 L {x0 + 129},190 L {x0 + 129},270 C {x0 + 100},300 {x0 + 30},300 {x0},270 Z", TEALC if i % 2 == 0 else "#fbf7ee", sw=2.6, off=(2, 1)))
    g.append(washed("M 560,70 L 1130,70 L 1130,170 L 560,170 Z", "#fbf7ee", off=(3, 2)))
    g.append(text(845, 140, "NOW OPEN", size=58, spacing=3))
    g.append(now_serving(1600, 300, 0.85, num, False))
    return "".join(g)


QUEUE = [dict(JK="#7a4f8c", HR="#3b2f2f", TIE="#d4a017"), dict(JK="#8c6a3f", HR="#a0522d", TIE="#2f5240"),
         dict(JK="#5c6b7a", HR="#c9a043", TIE="#8e2f45"), dict(JK="#9c3f4a", HR="#2c2a2e", TIE="#e9c46a"),
         dict(JK="#3f6f5a", HR="#d9b25a", TIE="#7a4f8c")]


@shot("S1_now_open", 5.8, cues=[(0.0, "theme2_out", {"d": 11.4, "fade": 3.2}, 0.26, "music"), (0.0, "shutter", {"d": 1.0}, 0.4), (1.0, "crowd", {"d": 4.6}, 0.3), (1.2, "ding_run", {"d": 4.4}, 0.25),
                                 (3.0, "ching", {}, 0.4), (4.6, "ching", {}, 0.35)])
def _(t, n):
    shutter = ramp(t, [(0.0, 1.0), (1.0, 0.0)])
    num = f"{101 + max(0, int((t - 1.2) / 0.3)):03d}" if t > 1.2 else "100"
    art = shop_set(shutter)
    # everyone from the climb, now serving
    people = [(430, "planning"), (650, "desk"), (1085, "cs"), (1290, "po")]
    for i, (x, who) in enumerate(people):
        arm_ = "point_right" if (t > 1.3 and (n // 4 + i) % 3 == 0) else "rest"
        art += official(x, SHOP_COUNTER, 0.6, who, arm=arm_, mouth="smile" if (n // 5 + i) % 2 else "talk", look=(0.6, 0.2))
    hand_over = t > 2.6
    pm_front = product_box(190, 80, 0.9, glow=1.0) if hand_over and t < 3.4 else ""
    art += pm_full(865, GROUND + 6, 0.58, legs_mode="stand", lean=film.breath(1.0),
                   arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (230, 160), (250, 80), "cup", True)] if pm_front else None or
                   [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 300), "rest", True)],
                   front=pm_front, look=(1, -0.2), brows="happy", mouth="grin")
    art += shop_front(shutter, num)
    plaques = [(430, ("PLANNING",)), (650, ("QA",)), (865, ("PRODUCT", "MANAGEMENT")), (1085, ("CUSTOMER", "SUCCESS")), (1290, ("PRODUCT", "OWNER"))]
    for x, lines in plaques:
        art += washed(f"M {x - 92},{SHOP_COUNTER + 34} L {x + 92},{SHOP_COUNTER + 34} L {x + 92},{SHOP_COUNTER + 100} L {x - 92},{SHOP_COUNTER + 100} Z", "#fbf7ee", sw=2.6, off=(2, 1))
        if len(lines) == 1:
            art += text(x, SHOP_COUNTER + 74, lines[0], size=20)
        else:
            art += text(x, SHOP_COUNTER + 62, lines[0], size=17) + text(x, SHOP_COUNTER + 86, lines[1], size=17)
    # the empty bench: nobody waits any more
    art += bench(100, GROUND, 0.6) + bench_front(100, GROUND, 0.6) + cobweb(-20, GROUND - 170, 0.8)
    # the queue
    for i, pal in enumerate(QUEUE):
        x = 1530 + i * 95
        hop = 10 * max(0, math.sin(t * 6 + i)) if t > 1.0 else 0
        pose = "hold_box" if (i == 0 and t > 3.4) else ("wave" if (n // 4 + i) % 3 == 0 and t > 1.0 else "phone")
        box = product_box(0, -470, 1.0, glow=1.0) if pose == "hold_box" else ""
        art += customer(x, GROUND - 6 - hop, 0.42 - i * 0.015, pose, "grin" if t > 1.0 else "smile", (-1, 0), "raised",
                        pal=pal, box=box, coffee=False)
    return W_((art, None), n)


@shot("N1_how_we_work", 4.6, cues=[(0, "room_tone", {"d": 4.6}, 0.06, "amb"), (2.2, "bridge_pad", {"d": 12.4}, 0.22, "music"), (0.1, "steps", {"d": 4.3, "rate": 3.0}, 0.3),
                                    (2.4, "clack", {}, 0.5), (2.5, "ding", {}, 0.3)])
def _(t, n):
    flip = ramp(t, [(2.2, 1.0), (2.4, 0.0), (2.6, -1.0)], smooth=False)
    sign, sub = ("INNOVATION", "CUSTOMER  20 m") if t < 2.4 else ("HOW WE WORK", "")
    art = office_no_pm(door_open=1.0, sign=sign, sub=sub, flip=flip)
    for i in range(3):
        st = 0.1 + i * 0.85
        x = ramp(t, [(st, 1330), (st + 3.3, 1985)], smooth=False)
        if t > st and x < 1980:
            svg = walker(x, GROUND + 6, 0.42, (t - st) * 2 * math.pi * 1.4, b=0.7, face=dict(look=(1, -0.2), brows="happy", mouth="smile"))
            art += recolour(svg, COLLEAGUES[i % len(COLLEAGUES)])
    wave = (n // 4) % 2
    art += mirror(pm_full(2190, GROUND + 6, 0.42, legs_mode="stand", lean=film.breath(1.0),
                          arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 100), (230, -30 if wave else 20), "open", True)],
                          look=(1, 0), brows="happy", mouth="grin"), 2190)
    return W_((art, DOOR_VIEW), n)


@shot("E1_still_die", 3.0, cues=[(1.7, "fizzle", {"d": 0.8}, 0.4), (2.3, "two_notes_down", {}, 0.3, "music")])
def _(t, n):
    a1 = min(1, max(0, (t - 0.1) / 0.4)); a2 = min(1, max(0, (t - 0.8) / 0.4))
    if t < 1.7:
        bb = 1.0
    elif t < 2.2:
        bb = [0.6, 0.0, 0.4, 0.0, 0.2, 0.0][n % 6] or 0.001
    else:
        bb = 0.0
    smoke = path(f"M 960,{730 - (t - 2.2) * 40:.0f} C 940,{700 - (t - 2.2) * 50:.0f} 980,{680 - (t - 2.2) * 60:.0f} 960,{650 - (t - 2.2) * 70:.0f}", sw=3, stroke="#9a948c") if t > 2.2 else ""
    art = (f'<g opacity="{a1:.2f}">' + text(960, 470, "Some ideas still die.", size=64, family="Georgia, serif", weight="normal") + '</g>'
           + f'<g opacity="{a2:.2f}">' + text(960, 570, "But faster.", size=64, family="Georgia, serif", weight="normal") + '</g>'
           + bulb(960, 800, s=0.7, b=bb, rays=8 if bb > 0.6 else 0, dead=(bb <= 0.0)) + smoke)
    return wrap_rb(art, None, boil(n))


@shot("E2_live_forever", 4.0, cues=[(0.1, "festoon", {}, 0.4, "music"), (1.3, "final_chord", {"d": 7.0}, 0.6, "music")])
def _(t, n):
    a1 = min(1, max(0, (t - 1.0) / 0.4)); a2 = min(1, max(0, (t - 1.7) / 0.4))
    # a string of bulbs, lighting up one after another
    xs = [520 + i * 110 for i in range(9)]
    wire = "M 440,640 " + " ".join(f"Q {x - 55},{690} {x},{660}" for x in xs) + " Q 1480,690 1520,640"
    art = path(wire, sw=3)
    for i, x in enumerate(xs):
        on = t > 0.1 + i * 0.1
        art += path(f"M {x},660 L {x},676", sw=3)
        art += bulb(x, 718, s=0.42, b=0.9 if on else 0.0, rot=180, rays=0)
    art += (f'<g opacity="{a1:.2f}">' + text(960, 420, "Some ideas live forever,", size=64, family="Georgia, serif", weight="normal") + '</g>'
            + f'<g opacity="{a2:.2f}">' + text(960, 520, "together.", size=64, family="Georgia, serif", weight="normal") + '</g>'
            + f'<g opacity="{a2:.2f}"><path d="M 860,560 C 920,550 1000,548 1060,556" fill="none" stroke="{TEALC}" stroke-width="9" stroke-linecap="round"/></g>')
    return wrap_rb(art, None, boil(n))


from logo_path import LOGO_D, LOGO_W, LOGO_H


@shot("E3_logo", 3.4, cues=[(0.05, "logo_sparkle", {}, 0.35, "music")])
def _(t, n):
    sc = ramp(t, [(0, 0.9), (0.25, 1.03), (0.45, 1.0)])
    k = 1150 / LOGO_W * sc
    x0, y0 = 960 - LOGO_W * k / 2, 560 - LOGO_H * k / 2
    logo = (f'<g transform="translate({x0:.1f},{y0:.1f}) scale({k:.4f})">'
            f'<path d="{LOGO_D}" fill="{TEALC}" fill-rule="evenodd" transform="translate(10,8)" filter="url(#wc)"/>'
            f'<path d="{LOGO_D}" fill="none" stroke="#2e2520" stroke-width="9" stroke-linejoin="round" stroke-dasharray="420 16 260 12 340 14"/></g>')
    # the string of lights stays on above it
    xs = [600 + i * 90 for i in range(9)]
    wire = "M 530,330 " + " ".join(f"Q {x - 45},{372} {x},{348}" for x in xs) + " Q 1390,372 1420,330"
    lights = path(wire, sw=3) + "".join(path(f"M {x},348 L {x},360", sw=3) + bulb(x, 396, s=0.32, b=0.75, rot=180, rays=0) for x in xs)
    return wrap_rb(lights + logo, None, boil(n))


def timeline():
    t0 = 0.0; out = []
    for s in SHOTS:
        out.append((t0, s)); t0 += round(s["dur"] * FPS) / FPS
    return out, t0


if __name__ == "__main__":
    tl, total = timeline()
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    mode = sys.argv[2] if len(sys.argv) > 2 else "all"
    OUT = os.environ.get("MS_OUT", "film2_frames"); os.makedirs(OUT, exist_ok=True)
    items = []
    for start, s in tl:
        if want and not s["name"].startswith(want):
            continue
        nf = int(round(s["dur"] * FPS)); g0 = int(round(start * FPS))
        idx = range(nf) if mode == "all" else [int(nf * float(mode))] if mode.replace(".", "").isdigit() else [nf // 2]
        for k in idx:
            film.NOW = (g0 + k) / FPS
            items.append((f"{g0 + k:05d}", s["draw"](k / FPS, g0 + k)))
    print("drawings", len(items), "total", round(total, 1))
    render(items, OUT)
