"""MOUNT STAEDEAN - clean wash performance edition.

Isolated staging copy: shared cast/props stay in staedean-cast/src, while
this film owns its acting keys. The Door and original film remain unchanged.

Each shot: (name, duration, draw(t, n) -> svg, cues). Cues are read by film_sound.py.
"""
import math, os, sys, random
import numpy as np
import anim_office as AO                     # also patches story.wrap to hand back (art, view)
import story
from story import *
from rb import wrap_rb
from render import render

FPS = 12
NOW = 0.0          # global film time, set per drawing (used for idle breathing)


def breath(amp=1.2):
    return amp * math.sin(2 * math.pi * 0.45 * NOW)
FULL = (0, 0, 1920, 1080)
SUMMIT_VIEW = (560, 345, 1100, 618.75)


# ---------------- animation helpers ----------------
def ease(u):
    u = min(1.0, max(0.0, u)); return u * u * (3 - 2 * u)


def lerp(a, b, u):
    if isinstance(a, (tuple, list)):
        return tuple(lerp(x, y, u) for x, y in zip(a, b))
    return a + (b - a) * u


def ramp(t, pts, smooth=True):
    """Value at time t along keyed points [(t, v), ...]."""
    if t <= pts[0][0]: return pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            u = (t - t0) / (t1 - t0) if t1 > t0 else 1
            return lerp(v0, v1, ease(u) if smooth else u)
    return pts[-1][1]


def step(t, pts):
    v = pts[0][1]
    for t0, v1 in pts:
        if t >= t0: v = v1
    return v


def flap(n, rate=2):
    return ["talk", "o", "talk", "neutral", "talk", "o"][(n // rate) % 6]


def oflap(n, rate=2):
    return ["talk", "smile", "talk", "flat"][(n // rate) % 4]


def walk_legs(phase, stride=1.0, lift=30):
    out = []
    for k, hx in enumerate((-70, 75)):
        ph = phase + k * math.pi
        fx = hx + 85 * stride * math.sin(ph)
        up = max(0.0, math.cos(ph)) * lift * stride
        kx = (hx + fx) / 2 + 34 * stride
        out.append(((hx, 330), (kx, 515 - up * 0.6), (fx, 700 - up)))
    return out


def boil(n):
    return 7 + (n // 2) % 3


def W_(art_view, n):
    art, view = art_view
    return wrap_rb(art, view, boil(n))


MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def page_svg(x, y, r, sc, m):
    inner = (washed("M 0,0 L 90,0 L 92,110 L 2,112 Z", C["paper_sheet"], sw=2.6, off=(2, 2))
             + washed("M 0,0 L 90,0 L 90,26 L 0,26 Z", C["cal_red"], sw=2.4, off=(1, 1))
             + f'<text x="45" y="20" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="17" fill="#fbf3e6">{m}</text>'
             + path("M 14,46 L 30,46 M 40,46 L 56,46 M 66,46 L 78,46 M 14,70 L 30,70 M 40,70 L 56,70 M 66,70 L 78,70 M 14,94 L 30,94 M 40,94 L 56,94", sw=2))
    return f'<g transform="translate({x:.1f},{y:.1f}) rotate({r:.1f}) scale({sc:.2f})">{inner}</g>'


def anim_pages(t, region, n=10, seed=1, speed=1.0):
    x0, y0, x1, y1 = region
    rnd = random.Random(seed)
    g = []
    span = (x1 - x0) + 400
    for i in range(n):
        v = rnd.uniform(260, 520) * speed
        off = rnd.uniform(0, span)
        x = x1 + 200 - ((t * v + off) % span)
        y = rnd.uniform(y0, y1) + 30 * math.sin(t * 3 + i)
        r = rnd.uniform(-40, 40) + t * rnd.choice((-1, 1)) * rnd.uniform(60, 200)
        g.append(page_svg(x, y, r, rnd.uniform(0.5, 0.85), MONTHS[(i + seed + int(t * 2)) % 12]))
        g.append(path(f"M {x + 70:.0f},{y + 40:.0f} C {x + 120:.0f},{y + 50:.0f} {x + 160:.0f},{y + 30:.0f} {x + 200:.0f},{y + 44:.0f}", sw=2, stroke="#9a8a74"))
    return "".join(g)


def anim_snow(t, n=90, seed=4, wind=0.3, region=(-50, -50, 1970, 1130), size=1.0):
    x0, y0, x1, y1 = region
    rnd = random.Random(seed)
    g = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        vy, r = rnd.uniform(70, 170) * (1 + wind), rnd.uniform(3, 7) * size
        y = y0 + ((y - y0 + vy * t) % (y1 - y0))
        x = x0 + ((x - x0 - wind * 500 * t) % (x1 - x0))
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#ffffff" stroke="#1f1a17" stroke-width="1.2"/>')
    return "".join(g)


def anim_wind(t, seed=8, region=(300, 100, 1900, 900), n=6):
    return wind_lines(region, n, seed=seed + int(t * 4))


def seat(x, *, beard=0.0, grey=0.0, b=1.0, lean=0, legs="sit", face=None, ticket=False, cob=0.0, snow_on=False, pack=0, drop=0.0):
    face = face or dict(look=(0.6, -0.2), brows="happy", mouth="smile")
    slump = legs == "sit_slump"
    front = bulb(90, 252 if not slump else 272, s=0.9, b=b, rays=0 if b < 0.6 else 6)
    if ticket:
        front += ticket_end(-90, 300, 0.7, "087", rot=-8)
    if snow_on:
        front += ('<path d="M -110,-230 C -80,-260 60,-270 100,-230 C 60,-220 -60,-214 -110,-230 Z" fill="#ffffff" stroke="#2e2520" stroke-width="2.4"/>'
                  '<path d="M -150,50 C -130,30 -90,30 -70,46 Z M 90,48 C 110,28 150,30 160,52 Z" fill="#ffffff" stroke="#2e2520" stroke-width="2.4"/>')
    svg = pm_full(x, GROUND + 2 - drop, 0.42, legs_mode=legs, lean=lean + breath(1.0), beard=beard, grey=grey,
                  behind=backpack(pack) if pack else "",
                  arms=[(SHL, (-170, 250), (-80, 320), "rest"), (SHR, (180, 250), (90, 310), "cup", True)],
                  front=front, **face)
    if cob > 0.02:
        svg += f'<g transform="translate({BENCH_X - 150},{GROUND - 180}) scale({cob:.2f})">' + cobweb(0, 0, 0.9) + '</g>'
    return svg


def walker(x, y, s, phase, *, b, beard=0.0, grey=0.0, lean=0, face=None, stack=0, pack=0, raised=True, mirror_it=False,
           stride=1.0, tank=False, beard_trail=0):
    face = face or dict(look=(1, -0.3), brows="happy", mouth="smile")
    # Energy fades with the idea: buoyant early steps become burdened shuffles.
    energy = max(0.18, min(1.0, b))
    phase += 0.12 * math.sin(phase)  # planted beat, quicker passing foot
    bob = (4 + 7 * energy) * abs(math.sin(phase)) * stride
    sw_ = math.sin(phase) * stride if not stack else 0.0
    free = (SHL, (-190 + 38 * sw_, 215 + 12 * sw_), (-145 + (65 + 45 * energy) * sw_, 310 - 22 * abs(sw_)), "rest")
    if raised:
        arms = [free, (SHR, (200, 190), (190, 110), "cup", True)]
        front = bulb(190, 58, s=1, b=b, rays=0 if b < 0.6 else 7)
    else:
        arms = [free, (SHR, (200, 210), (190, 202), "cup", True)]
        front = bulb(190, 150, s=1, b=b, rays=0 if b < 0.6 else 6)
    svg = pm_full(x, y - bob * s, s, legs_mode=walk_legs(phase, stride), lean=lean + 1.8 * math.sin(phase) * stride * energy, beard=beard, grey=grey,
                  behind=backpack(pack) if pack else "", before_arms=paper_stack(-190, 300, n=stack, w=140, tilt=-6) if stack else "",
                  arms=arms, front=front, tank=tank, beard_trail=beard_trail, head_rot=(1.3 * math.sin(phase - 0.4) + 1.4 * math.sin(2 * phase)) * stride, **face)
    return mirror(svg, x) if mirror_it else svg


def stand(x, y, s, *, b, arms=None, front_extra="", legs="stand", beard=0.0, grey=0.0, stack=0, lean=0, **face):
    arms = arms or [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)]
    return pm_full(x, y, s, legs_mode=legs, lean=lean + breath(1.2), beard=beard, grey=grey,
                   before_arms=paper_stack(-180, 300, n=stack, w=140, tilt=-6) if stack else "",
                   arms=arms, front=bulb(190, 58, s=1, b=b, rays=0 if b < 0.6 else 7) + front_extra, **face)


SHOTS = []


def shot(name, dur, cues=()):
    def deco(fn):
        SHOTS.append(dict(name=name, dur=dur, draw=fn, cues=list(cues)))
        return fn
    return deco


# ======================= A. OFFICE + REVEAL (from the approved test) =======================
@shot("A_office_and_reveal", AO.END, cues=[
    (0, "room_tone_office", {}), (0, "office_theme", {"d": 13.83}),
    (0.2, "scribble", {"d": 1.25}, 0.5), (1.5, "pop", {}, 0.45), (2.95, "scribble", {"d": 0.5}, 0.5),
    (3.5, "fizzle", {"d": 0.5}, 0.4), (4.4, "grab", {}, 0.3), (4.85, "whoosh", {"d": 0.6}, 0.45), (5.47, "clang", {}, 0.35),
    (6.7, "scribble", {"d": 0.3}, 0.45), (7.0, "pop", {}, 0.45), (8.15, "swell_soft", {}, 0.12, "music"),
    (9.55, "pop", {}, 0.2), (9.6, "swell_big", {}, 0.3, "music"),
    (12.83, "riser", {"d": 1.0}, 0.5), (13.2, "whoosh", {"d": 0.6, "lo": 300, "hi": 4000}, 0.45),
    (13.83, "mountain_hit", {}, 0.9, "music"), (13.83, "wind", {"d": 4.8, "intensity": 0.25}, 0.06, "amb"),
    (15.9, "eagle", {}, 0.12),
])
def _(t, n):
    return AO.draw(t, n)


# ======================= B. FOOT OF THE MOUNTAIN =======================
@shot("B1_oh", 3.4, cues=[(0, "wind", {"d": 3.4, "intensity": 0.25}, 0.06, "amb"), (2.25, "gulp", {}, 0.4)])
def _(t, n):
    look = ramp(t, [(0, (0.4, 0.0)), (1.0, (0.35, -1.0))])
    eyes = "closed" if 1.6 < t < 1.75 else "wide"
    mouth = "o" if 2.2 < t < 2.45 else "tiny"
    art = sky() + mountain_wall(200)
    art += pm_full(470, 1500, 1.15, legs_mode="stand", look=look, brows="sad", mouth=mouth, eyes=eyes,
                   head_rot=ramp(t, [(0, 3), (1.15, -7), (2.2, -7), (2.42, -2), (2.75, -4)]),
                   arms=[(SHL, (-170, 230), (-40, 270), "cup"), (SHR, (190, 240), (60, 270), "cup", True)],
                   front=bulb(10, 214, s=1, b=1.0, rays=7))
    view = ramp(t, [(0, FULL), (3.4, (60, 40, 1760, 990))])
    return W_((art, view), n)


@shot("B2_off_he_goes", 4.0, cues=[(0, "wind", {"d": 4.0, "intensity": 0.25}, 0.06, "amb"), (0.1, "march", {"d": 3.9}, 0.3, "music"),
                                    (0.2, "steps", {"d": 3.6, "rate": 2.4}, 0.3)])
def _(t, n):
    x = ramp(t, [(0, 470), (3.8, 1080)], smooth=False)
    ph = t * 2 * math.pi * 1.2
    art = trailhead() + walker(x, GROUND + 6, 0.36, ph, b=1.0, face=dict(look=(1, -0.4), brows="furrow", mouth="smile"))
    return W_((art, None), n)


# ======================= C. THE FIRST CHECKPOINT =======================
def cp(t, n, view, *, pm="", bench_pm="", off=None, serving="086", ding=False, strip=0.0, pages="", extra="", sign="CHECKPOINT",
       who="desk", snow=0.0, marker="100 m"):
    return W_(checkpoint(sign=sign, who=who, off=off or dict(look=(0, 1), mouth="flat"), serving=serving, ding=ding, strip=strip,
                         snow=snow, marker=marker, pm_layer=pm, bench_pm=bench_pm, pages=pages, extra=extra, view=view), n)


@shot("C1_arrival", 2.6, cues=[(0, "wind", {"d": 2.6, "intensity": 0.3}, 0.07, "amb"), (0, "march", {"d": 2.4, "start": 3.9}, 0.3, "music"),
                                (0, "steps", {"d": 2.5, "rate": 2.4}, 0.3)])
def _(t, n):
    x = ramp(t, [(0, 120), (2.4, 960)], smooth=False)
    ph = t * 2 * math.pi * 1.2
    pm = walker(x, GROUND + 6, 0.42, ph, b=1.0, face=dict(look=(1, -0.2), brows="happy", mouth="smile")) if t < 2.4 else \
        stand(960, GROUND + 6, 0.42, b=1.0, look=(1, -0.3), brows="happy", mouth="smile")
    return cp(t, n, None, pm=pm)


@shot("C2_the_pitch", 3.8, cues=[(0, "wind", {"d": 3.8, "intensity": 0.3}, 0.07, "amb"), (0.1, "mumble", {"d": 3.6, "f0": 165, "rate": 8.0}, 0.45)])
def _(t, n):
    g = ramp(t, [(0, 0.2), (0.35, 1.0), (2.6, 1.0), (3.8, 1.25)])
    lines = int(ramp(t, [(0, 1), (2.6, 9), (3.8, 14)], smooth=False))
    # Three deliberate beats: introduce, explain, then over-explain.
    wave = ramp(t, [(0, 0), (.28, .9), (.55, .5), (1.2, .5),
                    (1.48, -.5), (1.9, -.2), (2.65, -.2), (2.95, 1), (3.3, .6)])
    pm = stand(1000, GROUND + 6, 0.42, b=1.0, look=(1, -0.3), brows="raised", mouth=flap(n) if t < 3.35 else "smile",
               head_rot=ramp(t, [(0, -4), (.5, 2), (1.5, -3), (2.8, 4), (3.35, -2)]),
               arms=[(SHL, (-200, 160 + 20 * wave), (-230, 40 - 60 * wave), "open"), (SHR, (200, 190), (190, 110), "cup", True)])
    bub = bubble(860, 335 + 40 * (1 - g), 560 * g, 320 * g, (975, 560), lines=lines, seed=2)
    nod = "smile"
    return cp(t, n, COUNTER_VIEW, pm=pm, off=dict(look=(-1, 0), mouth=nod, head_tilt=ramp(t, [(0, 0), (.8, 0), (1.05, 5), (1.3, 0), (3.1, 0), (3.5, -3)])), extra=bub)


@shot("C3_take_a_ticket", 2.2, cues=[(0, "wind", {"d": 2.2, "intensity": 0.3}, 0.07, "amb"), (0.35, "mumble", {"d": 0.8, "f0": 260, "rate": 4.5}, 0.4)])
def _(t, n):
    arm_ = "point_left" if t > 0.3 else "rest"
    om = oflap(n) if 0.35 < t < 1.15 else "smile"
    look = ramp(t, [(0, (1, -.3)), (1.05, (1, -.3)), (1.35, (-.4, .6))])
    pm = pm_full(960, GROUND + 6, 0.42, legs_mode="stand", look=look, brows="raised" if t < 1.0 else "quizzical", mouth="o",
                 arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                 front=bulb(190, 58, s=1, b=1.0, rays=7))
    return cp(t, n, COUNTER_VIEW, pm=pm, off=dict(arm=arm_, mouth=om, look=(-1, 0)))


@shot("C4_ticket_087", 3.4, cues=[(0, "wind", {"d": 3.4, "intensity": 0.3}, 0.07, "amb"), (0.3, "printer", {"d": 2.4}, 0.25),
                                   (2.75, "pop", {}, 0.15)])
def _(t, n):
    strip = ramp(t, [(0.3, 0.0), (2.7, 1.0)], smooth=False)
    hy = ramp(t, [(0.3, 120), (2.7, 30), (2.83, 16), (3.05, 30)])
    eyes = "wide" if t > 1.4 else "open"
    tk = ticket_end(-190, hy - 60, 1.3 if t > 2.7 else 1.0, "087", rot=-6)
    pm = pm_full(640, GROUND + 6, 0.42, legs_mode="stand", look=(-0.6, -0.4), brows="raised", mouth="o" if t > 1.4 else "neutral", eyes=eyes,
                 arms=[(SHL, (-210, 170), (-180, hy), "fist"), (SHR, (200, 190), (190, 110), "cup", True)],
                 front=bulb(190, 58, s=1, b=1.0, rays=7) + tk)
    return cp(t, n, DISP_VIEW, pm=pm, strip=strip, off=dict(look=(-1, 0.3), mouth="smile"))


@shot("C5_take_a_seat", 2.4, cues=[(0, "wind", {"d": 2.4, "intensity": 0.3}, 0.07, "amb"), (0.0, "creak", {}, 0.5), (0.3, "ticking", {"d": 2.1}, 0.35)])
def _(t, n):
    drop = ramp(t, [(0, 35), (.2, -8), (.38, 4), (.58, 0)])
    sw = 0.0
    return cp(t, n, None, strip=1.0, bench_pm=seat(BENCH_X, b=1.0, ticket=True, drop=drop))


@shot("C6_waiting", 3.8, cues=[(0, "wind", {"d": 3.8, "intensity": 0.3}, 0.07, "amb"), (0, "ticking", {"d": 3.8}, 0.35),
                                (0.2, "flutter", {}, 0.4), (0.9, "flutter", {}, 0.35), (1.6, "flutter", {}, 0.35), (2.3, "flutter", {}, 0.3),
                                (2.6, "cricket", {"d": 1.2}, 0.08)])
def _(t, n):
    lean = ramp(t, [(0, 0), (3.0, 6)])
    legs = "sit" if t < 1.6 else "sit_slump"
    face = step(t, [(0, dict(look=(0.6, -0.2), brows="happy", mouth="smile")),
                    (1.0, dict(look=(0.4, 0.3), brows="weary", mouth="flat", eyes="half")),
                    (2.4, dict(look=(0.3, 0.6), brows="sad", mouth="frown", eyes="tired"))])
    beard = ramp(t, [(1.0, 0.0), (3.6, 0.06)])
    b = ramp(t, [(0, 1.0), (3.8, 0.9)])
    pages = anim_pages(t, (60, 330, 1080, 640), 9, seed=3)
    pm = seat(BENCH_X, beard=beard, b=b, lean=lean, legs=legs, face=face, ticket=True, cob=ramp(t, [(2.2, 0.0), (3.4, 1.0)]))
    pile = page_pile(BENCH_X, GROUND + 20, int(ramp(t, [(0, 0), (3.8, 14)], smooth=False)), seed=4) if t > 0.5 else ""
    return cp(t, n, BENCH_VIEW, strip=1.0, bench_pm=pm, pages=pile + pages)


@shot("C7_087", 2.0, cues=[(0, "wind", {"d": 2.0, "intensity": 0.3}, 0.07, "amb"), (0, "ticking", {"d": 1.0}, 0.3), (1.0, "dingdong", {}, 0.32)])
def _(t, n):
    ding = t >= 1.0
    pm = seat(BENCH_X, beard=0.06, b=0.9, lean=6, legs="sit_slump", face=dict(look=(0.3, 0.6), brows="sad", mouth="frown", eyes="tired"),
              ticket=True, cob=1.0)
    return cp(t, n, (1045, 205, 410, 230.6), strip=1.0, bench_pm=pm, serving="087" if ding else "086", ding=ding and (n % 4 < 3))


@shot("C8_jolt", 1.4, cues=[(0, "wind", {"d": 1.4, "intensity": 0.3}, 0.07, "amb"), (0.05, "boing", {}, 0.3)])
def _(t, n):
    drop = ramp(t, [(0, 0), (.08, -8), (.25, 38), (.43, -6), (.65, 0)])
    pm = seat(BENCH_X, beard=0.07, b=0.88, lean=-4, legs="sit", face=dict(look=(1.0, -0.6), brows="raised", mouth="o", eyes="wide"),
              ticket=True, drop=drop)
    return cp(t, n, BENCH_VIEW, strip=1.0, bench_pm=pm, serving="087", pages=page_pile(BENCH_X, GROUND + 20, 14, seed=4))


@shot("C9_onwards", 3.6, cues=[(0, "wind", {"d": 3.6, "intensity": 0.3}, 0.07, "amb"), (0.25, "stamp", {}, 0.6), (0.55, "stamp", {}, 0.6),
                                (1.1, "steps", {"d": 2.4, "rate": 2.0}, 0.3)])
def _(t, n):
    arm_ = "finger_up" if (0.15 < t < 0.3 or 0.45 < t < 0.6) else ("point_right" if t > 1.0 else "rest")
    if t < 1.1:
        pm = stand(1000, GROUND + 6, 0.42, b=0.85, beard=0.09, stack=5 if t > 0.7 else 0, look=(1, -0.6), brows="weary", mouth="flat", eyes="half",
                   arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 190), (190, 110), "cup", True)])
    else:
        x = ramp(t, [(1.1, 1000), (3.6, 1760)], smooth=False)
        pm = walker(x, GROUND + 6, 0.42, (t - 1.1) * 2 * math.pi * 1.0, b=0.85, beard=0.09, stack=5,
                    face=dict(look=(1, -0.6), brows="weary", mouth="flat", eyes="half"))
    return cp(t, n, None, pm=pm, strip=1.0, serving="088", off=dict(arm=arm_, mouth="smile", look=(1, 0)),
              pages=page_pile(BENCH_X, GROUND + 20, 14, seed=4))


# ======================= D. THE CLIMB =======================
@shot("D1_upwards", 2.8, cues=[(0, "wind", {"d": 2.8, "intensity": 0.45}, 0.09, "amb"), (0, "plod", {"d": 2.8}, 0.2, "music"),
                                (0, "steps", {"d": 2.7, "rate": 1.7, "heavy": 0.4}, 0.32)])
def _(t, n):
    x = ramp(t, [(0, 480), (2.8, 900)], smooth=False)
    art = slope(snow=0.1, steep=1.0)
    art += booth_back(1820, slope_y(1820) + 6, 0.12, sign="") + booth_front(1820, slope_y(1820) + 6, 0.12)
    art += walker(x, slope_y(x) + 8, 0.42, t * 2 * math.pi * 0.85, b=0.76, beard=0.11, lean=10, stack=8, raised=False,
                  face=dict(look=(1, -0.3), brows="weary", mouth="flat", eyes="half"))
    return W_((art, None), n)


def counter_pm(n, *, b, beard, grey, stack, talking=True, look=(1, -0.3), brows="raised", doc=False, mouth=None):
    front_extra = ""
    arms = [(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 190), (190, 110), "cup", True)]
    if doc:
        d = washed("M -40,-70 L 60,-70 L 60,60 L -40,60 Z", "#fbf7ee", sw=3, off=(2, 2)) + text(10, -30, "WRITE-UP", size=16) + \
            text(10, -6, "v7", size=22) + path("M -20,16 L 40,16 M -20,30 L 40,30 M -20,44 L 30,44", sw=2)
        wob = ramp(NOW, [(0, 15), (.25, -8), (.5, 0), (1.1, 0), (1.35, -16), (1.6, 0), (2.2, 0), (2.55, 32)])
        arms = [(SHL, (-200, 160), (-170, 30 + wob), "open"), arms[1]]
        front_extra = f'<g transform="translate(-170,{-60 + wob:.0f}) scale(1.3)">{d}</g>'
    return stand(1000, GROUND + 6, 0.42, b=b, beard=beard, grey=grey, stack=stack, arms=arms, front_extra=front_extra,
                 look=look, brows=brows, mouth=mouth or (flap(n) if talking else "flat"))


@shot("D2_customer_success", 3.0, cues=[(0, "wind", {"d": 3.0, "intensity": 0.45}, 0.09, "amb"),
                                         (0.0, "mumble", {"d": 2.8, "f0": 230, "rate": 6.0, "phone": True}, 0.2),
                                         (0.15, "mumble", {"d": 2.6, "f0": 160, "rate": 8.5}, 0.42)])
def _(t, n):
    g = ramp(t, [(0, 0.3), (0.3, 1.0)])
    bub = bubble(860, 335, 560 * g, 300 * g, (975, 560), lines=int(ramp(t, [(0, 1), (2.6, 8)], smooth=False)), seed=5)
    pm = counter_pm(n, b=0.72, beard=0.12, grey=0, stack=10)
    return cp(t, n, COUNTER_VIEW, pm=pm, sign="CUSTOMER SUCCESS", who="cs", serving="412", snow=0.15, marker=None,
              off=dict(arm="finger_up", mouth=oflap(n + 1), look=(1, 0)), extra=bub)


@shot("D3_please_wait", 1.2, cues=[(0, "wind", {"d": 1.2, "intensity": 0.45}, 0.09, "amb"), (0.1, "mumble", {"d": 0.6, "f0": 230, "rate": 5.0, "phone": True}, 0.25)])
def _(t, n):
    pm = counter_pm(n, b=0.7, beard=0.13, grey=0, stack=10, talking=False, look=ramp(t, [(0, (1, -.3)), (.4, (1, -.3)), (.65, (-1, .4))]), brows="raised" if t < .5 else "sad")
    return cp(t, n, COUNTER_VIEW, pm=pm, sign="CUSTOMER SUCCESS", who="cs", serving="412", snow=0.15, marker=None,
              off=dict(arm="point_left", mouth=oflap(n) if t < 0.7 else "smile", look=(1, 0)))


def bench_shot(t, n, *, sign, who, beard, grey, b, face, cob=0.0, snow=0.15, snow_on=False, pile=10, seed=11, stackn=12, falling=False):
    # Each return to the bench lands heavier; the head catches up after the body.
    drop = ramp(t, [(0, 30), (.18, -10), (.35, 3), (.55, 0)])
    face = dict(face)
    face['head_rot'] = ramp(t, [(0, -3), (.3, 7), (.6, 3), (1.4, 6)])
    pm = seat(BENCH_X, beard=beard, grey=grey, b=b, lean=6, legs="sit_slump", face=face, cob=cob, snow_on=snow_on, drop=drop)
    pm += paper_stack(BENCH_X + 250, GROUND, n=stackn, w=150)
    pages = anim_pages(t, (60, 330, 1080, 640), 7, seed=seed) + page_pile(BENCH_X, GROUND + 20, pile, seed=seed)
    if falling:
        pages += anim_snow(t, 70, seed=seed, wind=0.5, region=(0, 300, 1100, 920), size=1.2)
    return cp(t, n, BENCH_VIEW, sign=sign, who=who, serving="412", snow=snow, marker=None, bench_pm=pm, pages=pages)


SIT = [(0.0, "creak", {}, 0.5), (0.3, "ticking", {"d": 1.6}, 0.35), (0.4, "flutter", {}, 0.35)]


@shot("D4_sit", 2.0, cues=[(0, "wind", {"d": 2.0, "intensity": 0.45}, 0.09, "amb")] + SIT)
def _(t, n):
    return bench_shot(t, n, sign="CUSTOMER SUCCESS", who="cs", beard=0.18, grey=0.05, b=0.67,
                      face=dict(look=(0.4, 0.3), brows="weary", mouth="flat", eyes="half"), stackn=12)


@shot("D5_product_owner", 3.0, cues=[(0, "wind", {"d": 3.0, "intensity": 0.45}, 0.09, "amb"), (0.0, "flutter", {"d": 0.3}, 0.3),
                                      (0.1, "mumble", {"d": 2.3, "f0": 175, "rate": 10.0}, 0.42), (2.35, "mumble", {"d": 0.5, "f0": 120, "rate": 5.0}, 0.35)])
def _(t, n):
    g = ramp(t, [(0, 0.3), (0.3, 1.0), (2.2, 1.15)])
    bub = bubble(900, 345, 600 * g, 330 * g, (975, 560), lines=int(ramp(t, [(0, 2), (2.2, 13)], smooth=False)), seed=8) if t < 2.3 else ""
    pm = counter_pm(n, b=0.62, beard=0.21, grey=0.1, stack=13, doc=True, talking=t < 2.3, mouth=None if t < 2.3 else "o")
    return cp(t, n, COUNTER_VIEW, pm=pm, sign="PRODUCT OWNER", who="po", serving="412", snow=0.25, marker=None,
              off=dict(head_tilt=ramp(t, [(0, 0), (.8, 4), (1.1, 0), (2.3, 0), (2.6, -4)]), arm="point_left" if t > 2.3 else "rest", mouth=oflap(n) if t > 2.35 else "smile", look=(-1, 0)), extra=bub)


@shot("D6_sit_again", 2.0, cues=[(0, "wind", {"d": 2.0, "intensity": 0.5}, 0.09, "amb")] + SIT + [(0.5, "cricket", {"d": 1.2}, 0.07)])
def _(t, n):
    return bench_shot(t, n, sign="PRODUCT OWNER", who="po", beard=0.26, grey=0.12, b=0.57, cob=1.0, snow=0.25, pile=16, seed=12, stackn=16,
                      face=dict(look=(0.3, 0.6), brows="sad", mouth="frown", eyes="tired"))


@shot("D7_planning", 2.0, cues=[(0, "wind", {"d": 2.0, "intensity": 0.5}, 0.09, "amb"), (0.05, "mumble", {"d": 0.5, "f0": 120, "rate": 5.0}, 0.4),
                                 (0.5, "sigh", {"d": 1.0}, 0.35), (0.7, "steps", {"d": 1.3, "rate": 1.5, "heavy": 0.5}, 0.3)])
def _(t, n):
    x = ramp(t, [(0.6, 960), (2.0, 700)], smooth=False)
    pm = walker(x, GROUND + 6, 0.42, max(0, t - 0.6) * 2 * math.pi * 0.8, b=0.52, beard=0.3, grey=0.2, lean=6, stack=15, raised=False,
                mirror_it=True, stride=0.8 if t > 0.6 else 0.0, face=dict(look=(1, 0.4), brows="weary", mouth="flat", eyes="half"))
    return cp(t, n, None, pm=pm, sign="PLANNING", who="planning", serving="412", snow=0.45, marker=None,
              off=dict(arm="point_left", mouth=oflap(n) if t < 0.5 else "smile", look=(-1, 0)))


@shot("D8_sit_in_the_snow", 2.6, cues=[(0, "wind", {"d": 2.6, "intensity": 0.8}, 0.12, "amb")] + SIT)
def _(t, n):
    return bench_shot(t, n, sign="PLANNING", who="planning", beard=0.36, grey=0.27, b=0.46, cob=1.0, snow=0.55, snow_on=True, pile=22,
                      seed=13, stackn=20, falling=True, face=dict(look=(0.2, 0.2), brows="weary", mouth="wobbly", eyes="half"))


@shot("D9_how_far", 4.2, cues=[(0, "wind", {"d": 4.2, "intensity": 0.4}, 0.08, "amb"), (2.4, "sad_trombone", {}, 0.35, "music")])
def _(t, n):
    # Hold the struggle, then cut wide: the tiny distance travelled is the joke.
    view = (600, 820, 400, 225) if t < 2.4 else FULL
    arrow = ""
    if t > 2.8:
        arrow = path("M 860,860 C 820,880 790,900 772,930", sw=4, stroke="#c0623a") + path("M 760,914 L 772,932 L 790,920", sw=4, stroke="#c0623a")
    return W_((big_mountain(pm_dot=(760, 958), dot_b=0.42, show_sign=True) + arrow, view), n)


# ======================= E. THE FORK =======================
def fork_art(t, extra_pm, cave_eyes=True, monster_dy=0.0):
    art = fork_set()
    # both roads lead to the same place
    art += path("M 600,872 C 700,760 820,600 930,500", sw=2.4) + path("M 1320,872 C 1220,760 1100,600 990,500", sw=2.4)
    art += booth_back(960, 500, 0.13, sign="QA", sign_size=150) + booth_front(960, 500, 0.13)
    if not cave_eyes:
        art += '<rect x="250" y="505" width="90" height="30" fill="#2f2b2a"/>'
    art += f'<g transform="translate(0,{monster_dy:.1f})">' + sea_monster(1720, 800, 0.9) + '</g>'
    art += SIGNS + anim_snow(t, 50, seed=6, wind=0.3) + extra_pm
    return art


@shot("E1_the_fork", 2.8, cues=[(0, "wind", {"d": 2.8, "intensity": 0.6}, 0.12, "amb"), (0, "plod", {"d": 2.2, "start": 2.8}, 0.2, "music"),
                                 (0, "steps", {"d": 1.9, "rate": 1.5, "heavy": 0.5, "snow": 0.4}, 0.3)])
def _(t, n):
    x = ramp(t, [(0, 760), (1.9, 960)], smooth=False)
    moving = t < 1.9
    pm = walker(x, 1046, 0.36, t * 2 * math.pi * 0.75, b=0.38, beard=0.5, grey=0.45, lean=4, pack=180, raised=False,
                stride=1.0 if moving else 0.0, face=dict(look=(0, -0.6), brows="weary", mouth="flat", eyes="half"))
    return W_((fork_art(t, pm), None), n)


@shot("E2_here_be_dragons", 2.2, cues=[(0, "wind", {"d": 2.2, "intensity": 0.6}, 0.12, "amb"), (0.8, "roar", {"d": 1.3}, 0.35)])
def _(t, n):
    view = ramp(t, [(0, FULL), (0.6, (300, 380, 1000, 562.5))])
    pm = climber(960, 1046, 0.36, dict(b=0.37, beard=0.5, grey=0.45), legs_mode="stand", lean=0, stack=0, pack=180, mirror_x=True,
                 face=dict(look=(0.6, -1.0), brows="sad", mouth="tiny", eyes="wide"))
    smoke = path(f"M 300,{420 - t * 60:.0f} C 280,{380 - t * 60:.0f} 330,{360 - t * 60:.0f} 310,{320 - t * 60:.0f}", sw=6, stroke="#9a948c")
    return W_((fork_art(t, pm + smoke, cave_eyes=not (1.2 < t < 1.35)), view), n)


@shot("E3_or_the_sea_monster", 2.2, cues=[(0, "wind", {"d": 2.2, "intensity": 0.6}, 0.12, "amb"), (0.0, "whoosh", {"d": 0.3, "lo": 600, "hi": 3000}, 0.35),
                                           (0.6, "bloops", {}, 0.32)])
def _(t, n):
    view = ramp(t, [(0, (300, 380, 1000, 562.5)), (0.25, (620, 380, 1000, 562.5))], smooth=False)
    pm = climber(960, 1046, 0.36, dict(b=0.36, beard=0.5, grey=0.45), legs_mode="stand", lean=0, stack=0, pack=180,
                 face=dict(look=(0.6, -1.0), brows="sad", mouth="tiny", eyes="wide"))
    return W_((fork_art(t, pm, monster_dy=-30 * max(0, math.sin(t * 4))), view), n)


@shot("E4_either_way", 3.8, cues=[(0, "wind", {"d": 3.8, "intensity": 0.6}, 0.12, "amb"), (0.0, "whoosh", {"d": 0.4, "lo": 400, "hi": 2500}, 0.3),
                                   (0.7, "sigh", {"d": 1.5}, 0.45), (2.1, "steps", {"d": 1.6, "rate": 1.4, "heavy": 0.5, "snow": 0.4}, 0.3)])
def _(t, n):
    view = ramp(t, [(0, (620, 380, 1000, 562.5)), (0.5, FULL), (2.2, FULL), (3.8, (560, 300, 800, 450))])
    walking = t > 2.0
    x = ramp(t, [(2.0, 960), (3.8, 800)], smooth=False)
    pm = walker(x, 1046 - (960 - x) * 0.6, 0.36, (t - 2.0) * 2 * math.pi * 0.75, b=0.34, beard=0.5, grey=0.45, lean=10, pack=180, raised=False,
                mirror_it=True, stride=0.9 if walking else 0.0, face=dict(look=(0.4, 0.4), brows="weary", mouth="wobbly", eyes="half"))
    sigh_b = bubble(1120, 700, 150, 100, (1010, 800), words="…", size=56) if 0.6 < t < 2.0 else ""
    return W_((fork_art(t, pm + sigh_b), view), n)


# ======================= F. THE FINAL ASCENT =======================
@shot("F1_thin_air", 3.4, cues=[(0, "blizzard", {"d": 3.4}, 0.3, "amb"), (0, "steps", {"d": 3.3, "rate": 1.0, "heavy": 0.8, "snow": 1.0}, 0.35),
                                 (0, "shuffle", {"d": 3.3}, 0.15)])
def _(t, n):
    x = ramp(t, [(0, 780), (3.4, 960)], smooth=False)
    art = slope(snow=1.0, steep=1.3, seed=5)
    art += walker(x, slope_y(x, 1.3) + 10, 0.42, t * 2 * math.pi * 0.55, b=0.25, beard=1.05, grey=0.8, lean=18, pack=260, raised=False,
                  tank=True, beard_trail=700, stride=0.7, face=dict(look=(1, 0.2), brows="sad", mouth="wobbly", eyes="tired"))
    art += anim_snow(t, 150, seed=9, wind=1.2) + anim_wind(t, 3)
    return W_((art, None), n)


def close(t, n, *, b, mask=False, eyes="half", mouth="wobbly", lean=4, extra=""):
    art = slope(snow=1.0, steep=1.3, seed=5)
    art += pm_full(820, 1560, 1.35, legs_mode="stand", lean=lean, beard=1.05, grey=0.8, tank=True, mask=mask,
                   behind=backpack(260), look=(0.6, 0.2), brows="sad", mouth=mouth, eyes=eyes,
                   arms=[(SHL, (-170, 230), (-40, 270), "cup"), (SHR, (190, 240), (60, 270), "cup", True)],
                   front=bulb(10, 214, s=1, b=b, rays=0))
    art += anim_snow(t, 150, seed=9, wind=1.2) + anim_wind(t, 3) + extra
    return W_((art, None), n)


@shot("F2_dot_dot_dot", 3.0, cues=[(0, "blizzard", {"d": 3.0}, 0.3, "amb"), (0.5, "wheeze", {"d": 1.0}, 0.4)])
def _(t, n):
    bub = bubble(1300, 260, 260, 170, (1060, 420), words="…", size=90) if t > 0.9 else ""
    eyes = "closed" if 2.1 < t < 2.4 else "half"
    b = 0.22 if (n % 7) else 0.12
    return close(t, n, b=b, eyes=eyes, extra=bub)


@shot("F3_oxygen", 3.0, cues=[(0, "blizzard", {"d": 3.0}, 0.3, "amb"), (0.3, "hiss", {"d": 2.2}, 0.22)])
def _(t, n):
    lean = 4 + 3 * math.sin(t * 2 * math.pi * 0.6)
    hiss = path("M 1110,520 C 1150,500 1170,520 1210,500 M 1120,560 C 1170,550 1190,570 1240,556", sw=3) if (n // 2) % 2 else ""
    return close(t, n, b=0.2, mask=True, eyes="closed" if .7 < t < .9 or 2.1 < t < 2.3 else "tired", mouth="flat", lean=lean, extra=hiss)


@shot("F4_on_all_fours", 3.2, cues=[(0, "blizzard", {"d": 3.2, "cut": True}, 0.3, "amb"), (0.0, "flop", {}, 0.4), (0.3, "shuffle", {"d": 2.9}, 0.3)])
def _(t, n):
    art = slope(snow=1.0, steep=1.3, seed=5)
    fx = 1660
    art += flag(fx, slope_y(fx, 1.3) + 4, 0.6)
    x = ramp(t, [(0, 820), (3.2, 980)], smooth=False)
    y = slope_y(x, 1.3) + 14
    ang = math.degrees(math.atan2(slope_y(x + 50, 1.3) - slope_y(x - 50, 1.3), 100))
    reach = 1.0 + 0.25 * math.sin(t * 2 * math.pi * 1.1)
    art += f'<g transform="rotate({ang:.1f},{x:.1f},{y:.1f})">' + pm_crawl(x, y, 0.42, beard_tail=1400, grey=0.8, bulb_b=0.14, arm_reach=reach, phase=t * 2 * math.pi * 1.1,
                                                                         look=(0.8, -0.8), brows="sad", mouth="wobbly") + '</g>'
    art += anim_snow(t, 150, seed=9, wind=1.2) + anim_wind(t, 3)
    return W_((art, None), n)


# ======================= G. THE CUSTOMER =======================
def summit_frame(t, n, *, crawl_x, b, reach=1.0, cust_pose="phone", cust_mouth="flat", cust_look=(0, 0), cust_brows="neutral",
                 face=None, extra="", view=None, smoke_t=None, phase=None, cust_blink=False):
    face = face or dict(look=(1, -0.8), brows="raised", mouth="smile", eyes="tired")
    art = summit_set() + flag(1640, GROUND - 30, 0.9)
    art += customer(CUST_X, GROUND - 16, 0.52, cust_pose, cust_mouth, cust_look, cust_brows, blink=cust_blink, head_tilt=(3 * math.sin(t * 1.1) if cust_pose == "phone" else ramp(t, [(0, 0), (.4, -5), (.75, -3)])))
    if cust_pose == "phone" and (n // 3) % 2:
        art += path(f"M {CUST_X - 20},{GROUND - 16 - 0.55 * 560:.0f} l 6,-6", sw=2)
    bf = None
    if b <= 0.0:
        st_ = smoke_t or 0.0
        bf = (lambda bx, by: bulb(bx, by, s=0.9, b=0, rays=0, dead=True) +
              path(f"M {bx},{by - 70 - st_ * 30:.0f} C {bx - 20},{by - 100 - st_ * 40:.0f} {bx + 20},{by - 120 - st_ * 50:.0f} {bx},{by - 160 - st_ * 60:.0f}",
                   sw=3, stroke="#9a948c"))
    art += pm_crawl(crawl_x, GROUND + 50, 0.45, beard_tail=2600, grey=0.88, bulb_b=b, arm_reach=reach, bulb_fn=bf, phase=phase, **face)
    return W_((art + extra, view), n)


@shot("G1_the_summit", 3.4, cues=[(0, "calm", {"d": 3.4}, 0.05, "amb"), (0.0, "choir", {}, 0.25, "music"), (0.3, "taps", {"d": 3.0}, 0.25),
                                   (0.2, "shuffle", {"d": 3.0}, 0.25)])
def _(t, n):
    x = ramp(t, [(0, 180), (3.4, 520)], smooth=False)
    return summit_frame(t, n, crawl_x=x, b=0.1, reach=1.0 + 0.25 * math.sin(t * 2 * math.pi * 1.1), phase=t * 2 * math.pi * 1.1,
                        cust_blink=1.2 < t < 1.33,
                        face=dict(look=(1, -0.6), brows="raised", mouth="wobbly", eyes="tired"))


@shot("G2_for_you", 3.2, cues=[(0, "calm", {"d": 3.2}, 0.05, "amb"), (0.7, "musicbox_hope", {"d": 2.5}, 0.35, "music"), (0.0, "shuffle", {"d": 1.4}, 0.25),
                                (0.0, "taps", {"d": 3.2}, 0.2)])
def _(t, n):
    x = ramp(t, [(0, 920), (1.4, 1040)])
    reach = ramp(t, [(1.4, 1.0), (2.2, 1.3)])
    return summit_frame(t, n, crawl_x=x, b=0.08, reach=reach, view=SUMMIT_VIEW, phase=t * 2 * math.pi * 1.1 if t < 1.4 else None,
                        cust_blink=2.4 < t < 2.53,
                        face=dict(look=(1, -1), brows="raised", mouth="smile", eyes="tired"))


@shot("G3_who_are_you", 3.2, cues=[(0, "calm", {"d": 3.2}, 0.05, "amb"), (0.8, "mumble", {"d": 1.0, "f0": 140, "rate": 3.2, "question": True}, 0.5)])
def _(t, n):
    pose = "phone" if t < 0.3 else "down"
    bub = bubble(1000, 470, 380, 130, (1290, 440), words="Who are you?", size=44) if t > 0.8 else ""
    cm = oflap(n) if 0.8 < t < 1.8 else "flat"
    cm = {"smile": "flat", "talk": "talk", "flat": "flat"}.get(cm, "flat")
    return summit_frame(t, n, crawl_x=1040, b=0.06, reach=1.3, view=SUMMIT_VIEW, cust_pose=pose, cust_mouth=cm,
                        cust_look=(-1, 1) if t > 0.3 else (0, 0), cust_brows="puzzled" if t > 0.3 else "neutral",
                        face=dict(look=(1, -1), brows="raised" if t < 2.1 else "sad", mouth="smile" if t < 2.1 else "tiny" if t < 2.5 else "flat", eyes="closed" if 2.15 < t < 2.3 else "tired"), extra=bub)


@shot("G4_silence", 4.4, cues=[(0, "calm", {"d": 4.4}, 0.04, "amb"), (3.2, "cricket", {"d": 0.3, "every": 1}, 0.09)])
def _(t, n):
    eyes = "closed" if 2.6 < t < 2.9 else "half"
    b = ramp(t, [(0, .04), (4.4, .025)]) if n % 9 else .001
    return summit_frame(t, n, crawl_x=1040, b=b if b > 0 else 0.001, reach=1.3, view=(800, 560, 680, 382.5), cust_pose="down", cust_blink=1.5 < t < 1.63,
                        cust_look=(-1, 1), cust_brows="puzzled", face=dict(look=(1, -1), brows="neutral", mouth="flat", eyes=eyes))


@shot("G5_out", 4.6, cues=[(0, "calm", {"d": 4.6}, 0.04, "amb"), (0.4, "fizzle", {"d": 0.8}, 0.4), (2.4, "musicbox_end", {}, 0.35, "music")])
def _(t, n):
    if t < 1.1:
        b = [0.025, 0.0, 0.02, 0.0, 0.015, 0.0][n % 6] if t > 0.4 else 0.025
        b = b if b > 0 else 0.001
    else:
        b = 0.0
    pose = "down" if t < 2.8 else "phone"
    return summit_frame(t, n, crawl_x=1040, b=b, reach=ramp(t, [(1.4, 1.3), (2.6, 1.0)]), view=SUMMIT_VIEW, cust_pose=pose,
                        cust_look=(-1, 1) if t < 2.8 else (0, 0), cust_brows="puzzled" if t < 2.8 else "neutral",
                        face=dict(look=(1, -1) if t < 1.6 else (0.6, 0.4), brows="weary", mouth="flat", eyes="half"),
                        smoke_t=max(0, t - 1.1))


# ======================= H. END CARD =======================
@shot("H_end", 4.4, cues=[])
def _(t, n):
    a1 = min(1, max(0, (t - 0.3) / 0.4)); a2 = min(1, max(0, (t - 1.7) / 0.4))
    art = (f'<g opacity="{a1:.2f}">' + text(960, 500, "Some ideas should die.", size=64, family="Georgia, serif", weight="normal") + '</g>'
           + f'<g opacity="{a2:.2f}">' + text(960, 600, "This one didn&#8217;t have to.", size=64, family="Georgia, serif", weight="normal") + '</g>'
           + bulb(960, 800, s=0.7, b=0, dead=True)
           + f'<g opacity="{a2:.2f}"><path d="M 760,640 C 880,628 1040,626 1160,636" fill="none" stroke="#17C8BE" stroke-width="9" stroke-linecap="round"/></g>')
    return wrap_rb(art, None, boil(n))


# ---------------- timeline ----------------
def timeline():
    t0 = 0.0; out = []
    for s in SHOTS:
        out.append((t0, s)); t0 += round(s["dur"] * FPS) / FPS
    return out, t0


if __name__ == "__main__":
    tl, total = timeline()
    want = sys.argv[1] if len(sys.argv) > 1 else ""
    mode = sys.argv[2] if len(sys.argv) > 2 else "all"
    OUTDIR = os.environ.get("MS_OUT", "film_seq"); os.makedirs(OUTDIR, exist_ok=True)
    items = []
    for start, s in tl:
        if want and not s["name"].startswith(want):
            continue
        nf = int(round(s["dur"] * FPS))
        g0 = int(round(start * FPS))
        idx = range(nf) if mode == "all" else [nf // 2]
        for k in idx:
            globals()["NOW"] = (g0 + k) / FPS
            items.append((f"{g0 + k:05d}", s["draw"](k / FPS, g0 + k)))
    print("drawings", len(items), "total", round(total, 1))
    render(items, OUTDIR)
