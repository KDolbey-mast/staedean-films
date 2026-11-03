"""MOUNT STAEDEAN - every frame of the film.

Continuity rules (fixed for the whole film):
  * Bulb: once chosen it stays bright until the mountain, then only ever gets dimmer.
  * Bulb hand: whenever he holds it in one hand it is his LEFT hand (screen-right when he faces right).
  * Paperwork: always on the other side (screen-left), growing from folder -> stack -> backpack.
  * Beard: clean-shaven until the first bench; then it only grows, greying from the climb onwards.
"""
import sys
from office import *
from sets import *
from render import wrap, render

FRAMES = {}


def frame(name):
    def deco(fn):
        FRAMES[name] = fn
        return fn
    return deco


# progression tables -------------------------------------------------------
BULB = {"S3": [1.0, 1.0, 1.0, 1.0, 1.0, 0.92, 0.86, 0.84, 0.8],
        "S4": [0.74, 0.7, 0.67, 0.62, 0.58, 0.55, 0.5, 0.45, 0.42],
        "S5": [0.36, 0.35, 0.34, 0.32],
        "S6": [0.24, 0.2, 0.18, 0.13],
        "S7": [0.09, 0.07, 0.05, 0.03, 0.0]}
BEARD = {"S3": [0, 0, 0, 0, 0, 0, 0.05, 0.07, 0.09],
         "S4": [0.11, 0.12, 0.13, 0.18, 0.21, 0.24, 0.3, 0.36, 0.38],
         "S5": [0.5, 0.5, 0.5, 0.5],
         "S6": [1.05, 1.05, 1.05, 1.1],
         "S7": [1.1] * 5}
GREY = {"S3": [0] * 9, "S4": [0, 0, 0, 0.08, 0.12, 0.14, 0.22, 0.28, 0.28],
        "S5": [0.45] * 4, "S6": [0.8] * 4, "S7": [0.88] * 5}


def mirror(svg, x):
    return f'<g transform="translate({x},0) scale(-1,1) translate({-x},0)">{svg}</g>'


# ========================= SCENE 1: THE OFFICE =========================
def office_frame(*, head_rot, look, brows, mouth, eyes="open", arms, pad, bin_contents,
                 air_bulb=None, held_bulb=None, pencil_on_pad=False, extra="", view=None):
    body, hd, _ = pm(*NECK, head_rot=head_rot, look=look, brows=brows, mouth=mouth, eyes=eyes)
    arm_svg = "".join(arm(*a) for a in arms)
    floating = bulb(*THOUGHT_BULB, s=0.95, **air_bulb) if air_bulb else ""
    held = ""
    light = ""
    if held_bulb:
        xy = held_bulb.pop("xy")
        held = bulb(*xy, s=0.95, **held_bulb)
        light = (f'<circle cx="{xy[0]}" cy="{xy[1]}" r="300" fill="{C["glow"]}" opacity="0.10" '
                 f'filter="url(#bloom)" style="mix-blend-mode:screen"/>')
    art = (back_wall() + window() + calendar() + poster() + wastebin(bin_contents)
           + chair_back() + body + hd + desk_top() + mug() + tray()
           + notepad(pad, pencil_on_pad) + arm_svg + held + floating + light + extra)
    return wrap(art, view)


A_WRITE = [(SH_L, (752, 640), (868, 670), "rest"), (SH_R, (1150, 640), (1090, 664), "pencil")]
A_CUP = [(SH_L, (800, 640), (936, 622), "cup"), (SH_R, (1104, 640), (1000, 622), "cup", True)]
BIN0 = ("paper",)
BIN1 = ("dead_bulb", "paper")


@frame("S1_01_working")
def _():
    return office_frame(head_rot=6, look=(0.5, 0.9), brows="neutral", mouth="neutral", arms=A_WRITE, pad="blank", bin_contents=BIN0)


@frame("S1_02_an_idea")
def _():
    return office_frame(head_rot=-7, look=(0.35, -1.0), brows="raised", mouth="o", arms=A_WRITE, pad="idea1", bin_contents=BIN0,
                        air_bulb=dict(b=0.2, pop=True))


@frame("S1_03_hmm_no")
def _():
    return office_frame(head_rot=6, look=(0.5, 0.9), brows="furrow", mouth="frown", arms=A_WRITE, pad="idea1_x", bin_contents=BIN0,
                        air_bulb=dict(b=0.0))


@frame("S1_04_toss_it")
def _():
    arms = [(SH_L, (720, 470), (700, 350), "open"), (SH_R, (1150, 640), (1090, 664), "pencil")]
    flight = path("M 760,250 C 640,180 520,280 470,560", sw=2.4, extra='stroke-dasharray="10 10"') + \
        bulb(470, 600, s=0.62, b=0, rot=-160, dead=True)
    return office_frame(head_rot=0, look=(0, 0), brows="happy", mouth="smile", eyes="closed_happy", arms=arms, pad="idea1_x",
                        bin_contents=BIN0, extra=flight)


@frame("S1_05_back_to_work")
def _():
    return office_frame(head_rot=6, look=(0.5, 0.9), brows="happy", mouth="smile", arms=A_WRITE, pad="blank", bin_contents=BIN1)


@frame("S1_06_another_idea")
def _():
    return office_frame(head_rot=-7, look=(0.35, -1.0), brows="raised", mouth="o", arms=A_WRITE, pad="sketch1", bin_contents=BIN1,
                        air_bulb=dict(b=0.2, pop=True))


@frame("S1_07_weighing_it")
def _():
    arms = [(SH_L, (868, 648), (972, 488), "chin"), (SH_R, (1150, 640), (1100, 664), "pencil")]
    return office_frame(head_rot=4, look=(0.55, 0.85), brows="quizzical", mouth="hmm", arms=arms, pad="sketch2", bin_contents=BIN1,
                        air_bulb=dict(b=0.62))


@frame("S1_08_this_one")
def _():
    return office_frame(head_rot=9, look=(0.05, 1.0), brows="happy", mouth="grin", arms=A_CUP, pad="sketch3", bin_contents=BIN1,
                        held_bulb=dict(xy=(968, 566), b=1.0, rays=7), pencil_on_pad=True)


@frame("S1_09_to_the_window")
def _():
    return office_frame(head_rot=-5, look=(1.0, -0.3), brows="raised", mouth="smile", arms=A_CUP, pad="sketch3", bin_contents=BIN1,
                        held_bulb=dict(xy=(968, 566), b=1.0, rays=7), pencil_on_pad=True)


# ========================= SCENE 2: THE REVEAL =========================
@frame("S2_01_window_push")
def _():
    return office_frame(head_rot=-5, look=(1.0, -0.3), brows="raised", mouth="o", arms=A_CUP, pad="sketch3", bin_contents=BIN1,
                        held_bulb=dict(xy=(968, 566), b=1.0, rays=7), pencil_on_pad=True,
                        view=(820, 70, 1100, 618.75))


@frame("S2_02_mount_staedean")
def _():
    return wrap(big_mountain(pm_dot=(420, 1008), dot_b=1.0))


def pm_with_bulb_up(x, y, s, b, legs_mode="stand", **kw):
    return pm_full(x, y, s, legs_mode=legs_mode,
                   arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                   front=bulb(190, 58, s=1, b=b, rays=0 if b < 0.6 else 7), **kw)


@frame("S2_03_oh")
def _():
    art = sky() + mountain_wall(200)
    art += pm_full(470, 1500, 1.15, legs_mode="stand", look=(0.35, -1.0), brows="sad", mouth="tiny", eyes="wide",
                   arms=[(SHL, (-170, 230), (-40, 270), "cup"), (SHR, (190, 240), (60, 270), "cup", True)],
                   front=bulb(10, 214, s=1, b=1.0, rays=7))
    return wrap(art)


@frame("S2_04_off_he_goes")
def _():
    art = trailhead()
    art += pm_with_bulb_up(705, GROUND + 6, 0.36, 1.0, legs_mode="walk", look=(1, -0.4), brows="furrow", mouth="smile")
    return wrap(art)


# ========================= SCENE 3: THE FIRST CHECKPOINT =========================
BOOTH_X, BENCH_X, DISP_X = 1250, 380, 860
COUNTER_VIEW = (520, 150, 1160, 652.5)
DISP_VIEW = (330, 330, 1000, 562.5)
BENCH_VIEW = (0, 300, 1100, 618.75)
OFF_Y = GROUND - 0.75 * 250


def checkpoint(*, sign="CHECKPOINT", who="desk", off=None, serving="086", ding=False, strip=0, snow=0.0, marker="100 m",
               pm_layer="", pm_front="", pages=None, extra="", bench_pm="", calendar_pages=0, booth_stacks=0, view=None):
    off = off or {}
    a = ledge(snow=snow, marker=marker)
    a += bench(BENCH_X, GROUND, 0.6)
    a += booth_back(BOOTH_X, GROUND, 0.75, sign=sign, sign_size=46 if len(sign) < 12 else 36)
    a += official(BOOTH_X, OFF_Y, 0.55, who, **off)
    a += booth_front(BOOTH_X, GROUND, 0.75)
    a += now_serving(BOOTH_X, GROUND - 0.75 * 720 - 40, 0.7, serving, ding)
    a += dispenser(DISP_X, GROUND, 0.75, strip=strip)
    a += bench_front(BENCH_X, GROUND, 0.6)
    a += bench_pm
    a += pm_layer
    if pages:
        a += pages
    a += pm_front + extra
    return wrap(a, view)


def S(scene, i):
    return dict(b=BULB[scene][i], beard=BEARD[scene][i], grey=GREY[scene][i])


def seated(x, s, i, scene="S3", slump=False, mood="hopeful", ticket=True, pack=None, snow_on=False, cobweb_on=False, ding=False):
    st = S(scene, i)
    face = {"hopeful": dict(look=(0.6, -0.2), brows="happy", mouth="smile"),
            "flat": dict(look=(0.4, 0.3), brows="weary", mouth="flat", eyes="half"),
            "tired": dict(look=(0.3, 0.6), brows="sad", mouth="frown", eyes="tired"),
            "alert": dict(look=(1.0, -0.6), brows="raised", mouth="o", eyes="wide"),
            "numb": dict(look=(0.2, 0.2), brows="weary", mouth="wobbly", eyes="half")}[mood]
    front = bulb(90, 252 if not slump else 272, s=0.9, b=st["b"], rays=0 if st["b"] < 0.6 else 6)
    if ticket:
        front += ticket_end(-90, 300, 0.7, "087", rot=-8)
    if snow_on:
        front += ('<path d="M -110,-230 C -80,-260 60,-270 100,-230 C 60,-220 -60,-214 -110,-230 Z" fill="#ffffff" stroke="#2e2520" stroke-width="2.4"/>'
                  '<path d="M -150,50 C -130,30 -90,30 -70,46 Z M 90,48 C 110,28 150,30 160,52 Z" fill="#ffffff" stroke="#2e2520" stroke-width="2.4"/>')
    lean = 6 if slump else (-4 if mood == "alert" else 0)
    svg = pm_full(x, GROUND - 0.6 * 150 + 0.6 * 0 + 92, s, legs_mode="sit_slump" if slump else "sit", lean=lean,
                  beard=st["beard"], grey=st["grey"], behind=pack or "",
                  arms=[(SHL, (-170, 250), (-80, 320), "rest"), (SHR, (180, 250), (90, 310), "cup", True)],
                  front=front, **face)
    if cobweb_on:
        svg += cobweb(BENCH_X - 150, GROUND - 0.6 * 300, 0.9)
    return svg


@frame("S3_01_hopeful_arrival")
def _():
    st = S("S3", 0)
    pmv = pm_with_bulb_up(220, GROUND + 6, 0.42, st["b"], legs_mode="walk", look=(1, -0.2), brows="happy", mouth="smile")
    return checkpoint(off=dict(look=(0, 1), mouth="flat"), pm_layer=pmv)


@frame("S3_02_the_pitch")
def _():
    st = S("S3", 1)
    pmv = pm_full(1000, GROUND + 6, 0.42, legs_mode="stand", look=(1, -0.3), brows="raised", mouth="talk",
                  arms=[(SHL, (-200, 160), (-230, 40), "open"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=7))
    bub = bubble(860, 250, 560, 320, (975, 560), lines=9, seed=2)
    return checkpoint(off=dict(look=(-1, 0), mouth="smile"), pm_layer=pmv, extra=bub, view=COUNTER_VIEW)


@frame("S3_03_take_a_ticket")
def _():
    st = S("S3", 2)
    pmv = pm_full(960, GROUND + 6, 0.42, legs_mode="stand", look=(-0.4, 0.6), brows="quizzical", mouth="o",
                  arms=[(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=7))
    return checkpoint(off=dict(arm="point_left", mouth="smile", look=(-1, 0)), pm_layer=pmv, view=COUNTER_VIEW)


@frame("S3_04_ticket_087")
def _():
    st = S("S3", 3)
    pmv = pm_full(640, GROUND + 6, 0.42, legs_mode="stand", look=(-0.6, -0.4), brows="raised", mouth="o", eyes="wide",
                  arms=[(SHL, (-210, 170), (-180, 30), "fist"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=7) + ticket_end(-190, -30, 1.3, "087", rot=-6))
    return checkpoint(off=dict(look=(-1, 0.3), mouth="smile"), strip=1, pm_layer=pmv, view=DISP_VIEW)


@frame("S3_05_take_a_seat")
def _():
    return checkpoint(off=dict(look=(0, 1), mouth="flat"), strip=1, bench_pm=seated(BENCH_X, 0.42, 4, mood="hopeful"), view=BENCH_VIEW)


@frame("S3_06_pages_fly")
def _():
    return checkpoint(off=dict(look=(0, 1), mouth="flat"), strip=1, bench_pm=seated(BENCH_X, 0.42, 5, slump=True, mood="flat"),
                      pages=flying_pages((380, 330, 1060, 640), 11, seed=3), view=BENCH_VIEW)


@frame("S3_07_still_waiting")
def _():
    return checkpoint(off=dict(look=(0, 1), mouth="flat"), strip=1,
                      bench_pm=seated(BENCH_X, 0.42, 6, slump=True, mood="tired", cobweb_on=True),
                      pages=page_pile(BENCH_X, GROUND + 20, 14, seed=4) + flying_pages((560, 340, 1060, 600), 6, seed=7), view=BENCH_VIEW)


@frame("S3_08_number_087")
def _():
    return checkpoint(off=dict(look=(-1, 0), mouth="smile"), strip=1, serving="087", ding=True,
                      bench_pm=seated(BENCH_X, 0.42, 7, mood="alert"),
                      pages=page_pile(BENCH_X, GROUND + 20, 14, seed=4))


@frame("S3_09_onwards_with_paperwork")
def _():
    st = S("S3", 8)
    pmv = pm_full(1640, GROUND + 6, 0.42, legs_mode="walk", look=(1, -0.6), brows="weary", mouth="flat", eyes="half",
                  beard=st["beard"], grey=st["grey"],
                  before_arms=paper_stack(-180, 300, n=5, w=130, tilt=-8),
                  arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=6))
    return checkpoint(off=dict(look=(1, 0), mouth="smile"), strip=1, serving="088", pm_layer=pmv,
                      pages=page_pile(BENCH_X, GROUND + 20, 14, seed=4))


# ========================= SCENE 4: THE CLIMB =========================
def climber(x, y, s, st, *, legs_mode="trudge", lean=8, face=None, stack=8, pack=0, bulb_y=150, mask=False, tank=False,
            beard_trail=0, mirror_x=None):
    face = face or dict(look=(1, -0.3), brows="weary", mouth="flat", eyes="half")
    before = paper_stack(-190, 300, n=stack, w=140, tilt=-6) if stack else ""
    behind = backpack(pack) if pack else ""
    by = bulb_y
    svg = pm_full(x, y, s, legs_mode=legs_mode, lean=lean, beard=st["beard"], grey=st["grey"], behind=behind, before_arms=before,
                  arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 210), (190, by + 52), "cup", True)],
                  front=bulb(190, by, s=1, b=st["b"], rays=0 if st["b"] < 0.6 else 6), mask=mask, tank=tank,
                  beard_trail=beard_trail, **face)
    return mirror(svg, x) if mirror_x else svg


@frame("S4_01_upwards")
def _():
    st = S("S4", 0)
    x = 760
    art = slope(snow=0.1, steep=1.0)
    art += booth_back(1820, slope_y(1820) + 6, 0.12, sign="") + booth_front(1820, slope_y(1820) + 6, 0.12)
    art += climber(x, slope_y(x) + 8, 0.42, st, stack=8, lean=10)
    return wrap(art)


def booth_scene(sign, who, i, *, off, pm_layer="", extra="", snow=0.15, bench_pm="", pages=None):
    return checkpoint(sign=sign, who=who, off=off, serving="412", snow=snow, marker=None, pm_layer=pm_layer, extra=extra,
                      bench_pm=bench_pm, pages=pages)


@frame("S4_02_customer_success")
def _():
    st = S("S4", 1)
    pmv = pm_full(1000, GROUND + 6, 0.42, legs_mode="stand", look=(1, -0.3), brows="raised", mouth="talk",
                  beard=st["beard"], grey=st["grey"], before_arms=paper_stack(-180, 300, n=10, w=140, tilt=-6),
                  arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=6))
    bub = bubble(760, 250, 600, 300, (960, 560), lines=8, seed=5)
    return booth_scene("CUSTOMER SUCCESS", "cs", 1, off=dict(arm="finger_up", mouth="talk", look=(1, 0)), pm_layer=pmv, extra=bub)


@frame("S4_03_please_wait")
def _():
    st = S("S4", 2)
    pmv = pm_full(1000, GROUND + 6, 0.42, legs_mode="stand", look=(-1, 0.4), brows="sad", mouth="flat",
                  beard=st["beard"], grey=st["grey"], before_arms=paper_stack(-180, 300, n=10, w=140, tilt=-6),
                  arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=6))
    return booth_scene("CUSTOMER SUCCESS", "cs", 2, off=dict(arm="point_left", mouth="talk", look=(1, 0)), pm_layer=pmv)




def bench_cut(sign, who, i, mood, *, slump=True, cob=False, snow=0.15, snow_on=False, pack=0, pages_seed=11, pile=10):
    pages = flying_pages((40, 320, 230, 620), 3, seed=pages_seed) + flying_pages((560, 320, 1060, 640), 6, seed=pages_seed + 1) + page_pile(BENCH_X, GROUND + 20, pile, seed=pages_seed)
    stk = paper_stack(BENCH_X + 250, GROUND, n=12 + i * 3, w=150)
    return checkpoint(sign=sign, who=who, off=dict(look=(0, 1), mouth="flat"), serving="412", snow=snow, marker=None,
                      bench_pm=seated(BENCH_X, 0.42, i, "S4", slump=slump, mood=mood, ticket=False, cobweb_on=cob,
                                      snow_on=snow_on, pack=backpack(pack) if pack else None) + stk,
                      pages=pages, view=BENCH_VIEW)


@frame("S4_04_sit")
def _():
    return bench_cut("CUSTOMER SUCCESS", "cs", 3, "flat")


@frame("S4_05_product_owner")
def _():
    st = S("S4", 4)
    doc = washed("M -40,-70 L 60,-70 L 60,60 L -40,60 Z", "#fbf7ee", sw=3, off=(2, 2)) + text(10, -30, "WRITE-UP", size=16) + \
        text(10, -6, "v7", size=22) + path("M -20,16 L 40,16 M -20,30 L 40,30 M -20,44 L 30,44", sw=2)
    pmv = pm_full(1000, GROUND + 6, 0.42, legs_mode="stand", look=(1, -0.3), brows="raised", mouth="talk",
                  beard=st["beard"], grey=st["grey"], before_arms=paper_stack(-180, 300, n=13, w=140, tilt=-6),
                  arms=[(SHL, (-200, 160), (-170, 30), "open"), (SHR, (200, 190), (190, 110), "cup", True)],
                  front=bulb(190, 58, s=1, b=st["b"], rays=6) + f'<g transform="translate(-170,-60) scale(1.3)">{doc}</g>')
    bub = bubble(740, 240, 760, 360, (960, 560), lines=11, seed=8)
    return booth_scene("PRODUCT OWNER", "po", 4, off=dict(arm="point_left", mouth="smile", look=(-1, 0)), pm_layer=pmv, extra=bub, snow=0.25)


@frame("S4_06_sit_again")
def _():
    return bench_cut("PRODUCT OWNER", "po", 5, "tired", cob=True, snow=0.25, pages_seed=12, pile=16)


@frame("S4_07_planning")
def _():
    st = S("S4", 6)
    pmv = mirror(pm_full(900, GROUND + 6, 0.42, legs_mode="trudge", lean=6, look=(1, 0.4), brows="weary", mouth="flat", eyes="half",
                         beard=st["beard"], grey=st["grey"], before_arms=paper_stack(-180, 300, n=15, w=140, tilt=-6),
                         arms=[(SHL, (-200, 220), (-150, 310), "rest"), (SHR, (200, 210), (190, 202), "cup", True)],
                         front=bulb(190, 150, s=1, b=st["b"], rays=6)), 900)
    return booth_scene("PLANNING", "planning", 6, off=dict(arm="point_left", mouth="smile", look=(-1, 0)), pm_layer=pmv, snow=0.45)


@frame("S4_08_sit_in_the_snow")
def _():
    return bench_cut("PLANNING", "planning", 7, "numb", cob=True, snow=0.55, snow_on=True, pages_seed=13, pile=22) \



@frame("S4_09_how_far")
def _():
    arrow = path("M 860,860 C 820,880 790,900 772,930", sw=4, stroke="#c0623a") + path("M 760,914 L 772,932 L 790,920", sw=4, stroke="#c0623a")
    return wrap(big_mountain(pm_dot=(760, 958), dot_b=0.42, show_sign=True) + arrow)


# ========================= SCENE 5: THE FORK =========================
SIGNS = (signpost(700, 860, 0.8, "left", "ERP ROADMAP", ("Analysis · Design · Architecture", "Development · QA", "Next quarterly release"), "dragon")
         + signpost(1220, 860, 0.8, "right", "AI ROUTE", ("Intake form · Is it really AI?", "Routing · Prioritisation", "Delivery · QA"), "sea"))


def fork_frame(pm_svg, view=None):
    return wrap(fork_set() + SIGNS + snowfall((0, 0, 1920, 1080), 40, seed=6) + pm_svg, view)


@frame("S5_01_the_fork")
def _():
    st = S("S5", 0)
    return fork_frame(climber(960, 1046, 0.36, st, legs_mode="stand", lean=4, stack=0, pack=180,
                              face=dict(look=(0, -0.6), brows="weary", mouth="flat", eyes="half")))


@frame("S5_02_here_be_dragons")
def _():
    st = S("S5", 1)
    return fork_frame(climber(960, 1046, 0.36, st, legs_mode="stand", lean=0, stack=0, pack=180, mirror_x=True,
                              face=dict(look=(0.6, -1.0), brows="sad", mouth="tiny", eyes="wide")),
                      view=(300, 380, 1000, 562.5))


@frame("S5_03_or_the_sea_monster")
def _():
    st = S("S5", 2)
    return fork_frame(climber(960, 1046, 0.36, st, legs_mode="stand", lean=0, stack=0, pack=180,
                              face=dict(look=(0.6, -1.0), brows="sad", mouth="tiny", eyes="wide")),
                      view=(620, 380, 1000, 562.5))


@frame("S5_04_sigh")
def _():
    st = S("S5", 3)
    sigh = bubble(1120, 700, 150, 100, (1010, 800), words="…", size=56)
    return fork_frame(climber(960, 1046, 0.36, st, legs_mode="trudge", lean=10, stack=0, pack=180, mirror_x=True,
                              face=dict(look=(0.4, 0.4), brows="weary", mouth="wobbly", eyes="half")) + sigh)


# ========================= SCENE 6: THE FINAL ASCENT =========================
def blizzard(art):
    return art + snowfall((-50, -50, 1970, 1130), 160, seed=9, wind=0.9) + wind_lines((300, 100, 1900, 900), 7, seed=3)


@frame("S6_01_thin_air")
def _():
    st = S("S6", 0)
    x = 900
    art = slope(snow=1.0, steep=1.3, seed=5)
    art += climber(x, slope_y(x, 1.3) + 10, 0.42, st, lean=18, stack=0, pack=260, tank=True, bulb_y=220, beard_trail=700,
                   face=dict(look=(1, 0.2), brows="sad", mouth="wobbly", eyes="tired"))
    return wrap(blizzard(art))


def closeup(st, *, mask=False, eyes="half", mouth="wobbly", extra=""):
    art = slope(snow=1.0, steep=1.3, seed=5)
    art += pm_full(820, 1560, 1.35, legs_mode="stand", lean=4, beard=st["beard"], grey=st["grey"], tank=True, mask=mask,
                   behind=backpack(260), look=(0.6, 0.2), brows="sad", mouth=mouth, eyes=eyes,
                   arms=[(SHL, (-170, 230), (-40, 270), "cup"), (SHR, (190, 240), (60, 270), "cup", True)],
                   front=bulb(10, 214, s=1, b=st["b"], rays=0))
    return wrap(blizzard(art) + extra)


@frame("S6_02_dot_dot_dot")
def _():
    return closeup(S("S6", 1), extra=bubble(1300, 260, 260, 170, (1060, 420), words="…", size=90))


@frame("S6_03_oxygen")
def _():
    hiss = path("M 1110,520 C 1150,500 1170,520 1210,500 M 1120,560 C 1170,550 1190,570 1240,556", sw=3, stroke="#7f9aa0")
    return closeup(S("S6", 2), mask=True, eyes="closed", mouth="flat", extra=hiss)


@frame("S6_04_on_all_fours")
def _():
    st = S("S6", 3)
    art = slope(snow=1.0, steep=1.3, seed=5)
    fx = 1660
    art += flag(fx, slope_y(fx, 1.3) + 4, 0.6)
    x = 900
    y = slope_y(x, 1.3) + 14
    ang = math.degrees(math.atan2(slope_y(x + 50, 1.3) - slope_y(x - 50, 1.3), 100))
    art += f'<g transform="rotate({ang:.1f},{x},{y})">' + pm_crawl(x, y, 0.42, beard_tail=1400, grey=st["grey"], bulb_b=st["b"],
                                                                     look=(0.8, -0.8), brows="sad", mouth="wobbly") + '</g>'
    return wrap(blizzard(art))


# ========================= SCENE 7: THE CUSTOMER =========================
CUST_X = 1340


def summit(*, crawl_x, cust_pose="phone", cust_mouth="flat", cust_look=(0, 0), cust_brows="neutral", st, face=None, extra="",
           view=None, reach=1.0, smoke=False):
    face = face or dict(look=(1, -0.8), brows="raised", mouth="smile", eyes="tired")
    art = summit_set() + flag(1640, GROUND - 30, 0.9)
    art += customer(CUST_X, GROUND - 16, 0.55, cust_pose, cust_mouth, cust_look, cust_brows)
    dead = st["b"] <= 0.0
    bf = (lambda bx, by: bulb(bx, by, s=0.9, b=0, rays=0, dead=True) +
          path(f"M {bx},{by - 70} C {bx - 20},{by - 100} {bx + 20},{by - 120} {bx},{by - 160}", sw=3, stroke="#9a948c")) if dead else None
    art += pm_crawl(crawl_x, GROUND + 50, 0.45, beard_tail=2600, grey=st["grey"], bulb_b=st["b"], arm_reach=reach, bulb_fn=bf, **face)
    return wrap(art + extra, view)


@frame("S7_01_the_summit")
def _():
    return summit(crawl_x=380, st=S("S7", 0), face=dict(look=(1, -0.6), brows="raised", mouth="wobbly", eyes="tired"))


SUMMIT_VIEW = (560, 340, 1100, 618.75)


@frame("S7_02_for_you")
def _():
    return summit(crawl_x=1040, st=S("S7", 1), reach=1.2, face=dict(look=(1, -1), brows="raised", mouth="smile", eyes="tired"),
                  view=SUMMIT_VIEW)


@frame("S7_03_who_are_you")
def _():
    bub = bubble(1000, 470, 380, 130, (1290, 440), words="Who are you?", size=44)
    return summit(crawl_x=1040, st=S("S7", 2), reach=1.2, cust_pose="down", cust_mouth="talk", cust_look=(-1, 1), cust_brows="puzzled",
                  face=dict(look=(1, -1), brows="raised", mouth="smile", eyes="tired"), extra=bub, view=SUMMIT_VIEW)


@frame("S7_04_silence")
def _():
    return summit(crawl_x=1040, st=S("S7", 3), reach=1.2, cust_pose="down", cust_look=(-1, 1), cust_brows="puzzled",
                  face=dict(look=(1, -1), brows="neutral", mouth="flat", eyes="half"), view=(800, 560, 680, 382.5))


@frame("S7_05_out")
def _():
    return summit(crawl_x=1040, st=S("S7", 4), reach=1.2, cust_pose="down", cust_look=(-1, 1), cust_brows="puzzled",
                  face=dict(look=(1, -1), brows="weary", mouth="flat", eyes="half"), view=SUMMIT_VIEW)


if __name__ == "__main__":
    pat = sys.argv[1] if len(sys.argv) > 1 else ""
    items = [(n, fn()) for n, fn in FRAMES.items() if n.startswith(pat)]
    render(items, "frames")
