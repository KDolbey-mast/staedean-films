"""Animated proof: Scene 1 + the reveal, 12 drawings per second, puppet animation with boiling lines."""
import math, os, sys, subprocess, copy
import numpy as np
import story
from story import office_frame, A_WRITE, A_CUP, BIN0, BIN1, SH_L, SH_R, THOUGHT_BULB
from sets import big_mountain
from rig import bulb, path
from rb import wrap_rb
from render import render

story.wrap = lambda art, view=None, *a, **k: (art, view)
FPS = 12
FULL = (0, 0, 1920, 1080)
MED = (300, 130, 1280, 720)


def ease(u):
    u = min(1, max(0, u)); return u * u * (3 - 2 * u)


def mix(a, b, u):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + (b - a) * u
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)) and len(a) == len(b):
        out = [mix(x, y, u) for x, y in zip(a, b)]
        return tuple(out) if isinstance(a, tuple) else out
    return b if u >= 0.5 else a


# ---------------- key poses ----------------
KEYS = []
state = dict(head_rot=6, look=(0.5, 0.9), brows="neutral", mouth="neutral", eyes="open", arms=A_WRITE, writing=1.0,
             pad="blank", pencil_on_pad=False, bin=BIN0, air_b=None, air_s=0.0, air_dead=False, grab=None, held=None,
             fly=None, view=MED, scene="office", flicker=False)


def K(t, **ch):
    global state
    state = {**state, **ch}
    KEYS.append((t, copy.deepcopy(state)))


REACH_L = [(SH_L, (820, 380), (975, 200), "open"), A_WRITE[1]]
WIND_L = [(SH_L, (760, 420), (790, 260), "open"), A_WRITE[1]]
TOSS_L = [(SH_L, (720, 470), (700, 350), "open"), A_WRITE[1]]
CHIN = [(SH_L, (868, 648), (972, 488), "chin"), (SH_R, (1150, 640), (1100, 664), "pencil")]
PLUCK = [(SH_L, (850, 430), (975, 205), "cup"), (SH_R, (1110, 430), (1048, 205), "cup", True)]

K(0.0)
K(1.45)
K(1.5, air_b=0.25, air_s=0.0)
K(1.62, air_s=1.15, head_rot=-7, look=(0.35, -1.0), brows="raised", mouth="o", writing=0.0)
K(1.75, air_s=0.95)
K(2.6)
K(2.9, head_rot=6, look=(0.5, 0.9), brows="furrow", mouth="frown", writing=1.0, pad="idea1")
K(3.45, pad="idea1_x")
K(3.5, flicker=True, writing=0.0)
K(3.95, flicker=False, air_b=0.0, air_dead=True, mouth="flat")
K(4.1, head_rot=-4, look=(0.4, -1.0))
K(4.4, arms=REACH_L, grab="air")
K(4.45, grab="hand", air_b=None)
K(4.75, arms=WIND_L)
K(4.9, arms=TOSS_L, grab=None, fly=0.0, eyes="closed_happy", brows="happy", mouth="smile", head_rot=0, look=(0, 0))
K(5.45, fly=1.0)
K(5.5, fly=None, bin=BIN1)
K(6.2)
K(6.6, arms=A_WRITE, writing=1.0, eyes="open", head_rot=6, look=(0.5, 0.9))
K(7.0, air_b=0.25, air_s=0.0, air_dead=False, pad="sketch1")
K(7.12, air_s=1.15, head_rot=-7, look=(0.35, -1.0), brows="raised", mouth="o", writing=0.0)
K(7.25, air_s=0.95)
K(7.7)
K(8.15, arms=CHIN, head_rot=4, look=(0.55, 0.85), brows="quizzical", mouth="hmm", writing=0.0, pad="sketch2", air_b=0.4)
K(9.0, air_b=0.72, look=(0.3, -0.8))
K(9.15, mouth="grin", brows="happy", head_rot=-4, pad="sketch3", pencil_on_pad=True)
K(9.55, arms=PLUCK, grab="pluck")
K(9.6, air_b=None, held=True, )
K(10.25, arms=A_CUP, head_rot=9, look=(0.05, 1.0))
K(11.4)
K(11.8, head_rot=-5, look=(1.0, -0.3), brows="raised", mouth="smile")
K(12.0, view=MED)
K(12.7, mouth="o")
K(13.2, view=(820, 70, 1100, 618.75))
K(13.75, view=(1560, 270, 220, 123.75))
K(13.83, scene="mountain", view=(0, 216, 1536, 864))
K(17.2, view=FULL)
K(18.6)
END = 18.6

HELD_B = {9.6: 0.72, 10.0: 1.0}
BLINKS = [0.9, 6.3, 11.0, 12.4]


def at(t):
    for (t0, s0), (t1, s1) in zip(KEYS, KEYS[1:]):
        if t0 <= t < t1:
            u = ease((t - t0) / (t1 - t0))
            return {k: mix(s0[k], s1[k], u) for k in s0}, s0, s1, u
    return KEYS[-1][1], KEYS[-1][1], KEYS[-1][1], 1.0


def hand_of(arms, i):
    return arms[i][2]


def draw(t, n):
    st, s0, s1, u = at(t)
    seed = 7 + (n // 2) % 3                              # line boil: redraw every other drawing
    if st["scene"] == "mountain":
        return wrap_rb(big_mountain(pm_dot=(420, 1008), dot_b=1.0), st["view"], seed)
    arms = [list(a) for a in st["arms"]]
    # pencil wiggle while writing
    if st["writing"] > 0.01 and arms[1][3] == "pencil":
        hx, hy = arms[1][2]
        arms[1][2] = (hx + 9 * st["writing"] * math.sin(2 * math.pi * 3.2 * t), hy + 3 * st["writing"] * math.sin(2 * math.pi * 6.4 * t))
    arms = [tuple(a) for a in arms]
    eyes = st["eyes"]
    if any(abs(t - b) < 0.09 for b in BLINKS) and eyes == "open":
        eyes = "closed"
    extra = ""
    # the idea bulb
    if st["held"]:
        hb = max(v for k, v in HELD_B.items() if t >= k) if t >= 9.6 else 0.72
        if 9.6 <= t < 10.0:
            hb = 0.72 + (t - 9.6) / 0.4 * 0.28
        lx, ly = hand_of(arms, 0); rx, ry = hand_of(arms, 1)
        extra += bulb((lx + rx) / 2, min(ly, ry) - 56, s=0.95, b=hb, rays=7)
    elif s0["grab"] == "hand" or (st["grab"] == "hand"):
        hx, hy = hand_of(arms, 0)
        extra += bulb(hx + 10, hy - 30, s=0.95, b=0, dead=True, rot=-20)
    elif st["fly"] is not None and s0["fly"] is not None:
        p = st["fly"]
        p0, c, p1 = np.array((760, 250)), np.array((520, 120)), np.array((425, 735))
        pos = (1 - p) ** 2 * p0 + 2 * (1 - p) * p * c + p ** 2 * p1
        extra += bulb(pos[0], pos[1], s=0.62 + 0.0 * p, b=0, dead=True, rot=-160 * p - 40)
        tail = p0 if p < 0.4 else (1 - (p - 0.35)) ** 2 * p0 + 2 * (1 - (p - 0.35)) * (p - 0.35) * c + (p - 0.35) ** 2 * p1
        extra += path(f"M {tail[0]:.0f},{tail[1]:.0f} Q {c[0]},{c[1]} {pos[0]:.0f},{pos[1]:.0f}", sw=2, extra='stroke-dasharray="8 10"') if p > 0.1 else ""
    elif st["air_b"] is not None or s0["air_b"] is not None:
        b = st["air_b"] if st["air_b"] is not None else s0["air_b"]
        if st["flicker"]:
            b = [0.35, 0.05, 0.25, 0.0, 0.3, 0.02][n % 6]
        sc = st["air_s"] * 0.95
        if sc > 0.05:
            extra += bulb(*THOUGHT_BULB, s=sc, b=b, dead=st["air_dead"] and not st["flicker"], pop=1.4 < t < 1.9 or 6.95 < t < 7.4)
    # clang lines when the bulb lands
    if 5.45 <= t < 5.85:
        extra += path("M 360,720 L 330,700 M 352,690 L 335,664 M 500,718 L 530,698 M 506,690 L 524,664", sw=3)
    art, view = office_frame(head_rot=st["head_rot"], look=st["look"], brows=st["brows"], mouth=st["mouth"], eyes=eyes,
                             arms=arms, pad=st["pad"], bin_contents=st["bin"], pencil_on_pad=st["pencil_on_pad"],
                             extra=extra, view=st["view"])
    return wrap_rb(art, view, seed)


if __name__ == "__main__":
    n_frames = int(END * FPS)
    only = sys.argv[1:] and [int(x) for x in sys.argv[1:]]
    items = [(f"{n:04d}", draw(n / FPS, n)) for n in range(n_frames) if not only or n in only]
    os.makedirs("anim1", exist_ok=True)
    render(items, "anim1")
