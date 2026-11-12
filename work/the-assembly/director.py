"""The Assembly: a 20-second parody of an absurdly epic team recruitment.

New short. Does not alter or import approved film edit chains.
Keep the canonical PM, Maker, Customer Success and QA; no ninja or sheep.
"""
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "work/staedean-cast/src"))
os.environ["MS_STYLE"] = "wash"
import cast
import film
import film2 as f
import props
import rb
import sets

rb.STYLE = "wash"
FPS = 12
DURATION = 20
BROWSER = os.environ.get("ANIMATION_BROWSER", "")
k = film.ramp
FULL = (0, 0, 1920, 1080)
INK = "#2e2520"
MOUNTAIN = sets.big_mountain(show_sign=False).removeprefix(sets.sky())


def finish(art, n, view=FULL):
    return rb.wrap_rb(art, view, film.boil(n))


def group(art, x, y, scale=1, rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({scale})">{art}</g>'


def official_full(role, x, y, scale=.6, look=(0, .1), mouth="smile", tilt=0, mic=0):
    """Existing canonical official upper-body rig plus matching standing legs."""
    hip = y - 370 * scale
    art = f'<g transform="translate({x},{hip}) scale({scale}) translate(0,-330)">{f.legs("stand")}</g>'
    art += props.official(
        x, hip, scale, cast.OFFICIALS[role], mouth=mouth, look=look,
        brows="puzzled" if mouth == "flat" else "neutral",
        head_tilt=tilt, mic_angle=mic
    )
    return art


def landscape():
    art = f.sky() + group(MOUNTAIN, 920, 250, .47)
    art += f.washed(
        "M -100,850 Q 550,795 1100,835 Q 1550,775 2020,820 L 2020,1200 L -100,1200 Z",
        "#a9b394", off=(4, 3)
    )
    return art


def office():
    art = f.washed(
        "M 0,0 L 1920,0 L 1920,1080 L 0,1080 Z", "#e9e4d9", off=(2, 1)
    )
    art += f.path("M 0,860 L 1920,860 M 320,0 L 320,860 M 1620,0 L 1620,860",
                  sw=3, stroke="#c8c1b6")
    art += f.washed("M 1350,90 L 1660,90 L 1660,320 L 1350,320 Z", "#fffaf0", off=(2, 2))
    art += f.text(1505,176,"MEETING", size=37)
    art += f.text(1505,235,"ROOM", size=37)
    return art


def small_table():
    art = f.washed("M 630,725 L 1300,725 L 1250,840 L 685,840 Z", "#c9ae88", off=(4, 3))
    art += f.washed("M 720,840 L 765,840 L 765,1020 L 720,1020 Z", "#9d7e5d", off=(2, 1))
    art += f.washed("M 1180,840 L 1225,840 L 1225,1020 L 1180,1020 Z", "#9d7e5d", off=(2, 1))
    for cx in (755, 1220):
        art += f.washed(f"M {cx-18},735 L {cx+18},735 L {cx+13},670 L {cx-13},670 Z", "#fbf7ee", off=(1, 1))
    return art


def cramped_team(t, reaction=False):
    """Four original cast members; deliberately inadequate space, no invented identities."""
    look = (-1, .2) if reaction else (0, .1)
    mood = "weary" if reaction else "hopeful"
    mouths = "flat" if reaction else "smile"
    art = f.maker(715, 930, .47, face=dict(look=look, brows="quizzical" if reaction else "happy",
                                         mouth=mouths, head_rot=-2 if reaction else 0))
    art += official_full("customer success", 870, 930, .51,
                         look=look, mouth=mouths, tilt=-6 if reaction else 0)
    art += cast.pm(1035, 930, s=.48, mood=mood, bulb=None)
    art += official_full("qa", 1185, 930, .51,
                         look=look, mouth=mouths, tilt=5 if reaction else 0)
    return art + small_table()


def approved(t, n):
    art = f.washed("M 0,0 L 1920,0 L 1920,1080 L 0,1080 Z", "#e8dfcb", off=(5, 3))
    art += f.washed("M 400,140 L 1530,140 L 1530,930 L 400,930 Z", "#fffaf0", off=(4, 3))
    art += f.text(960,330,"INNOVATION TEAM", size=74)
    art += f.text(960,425,"PROPOSAL", size=59, fill="#6a6e68")
    for y in (540,590,640,690):
        art += f.path(f"M 540,{y} L 1380,{y}", sw=3, stroke="#bcb9af")
    if t >= .33:
        drop = k(t,[(.33,-55),(.52,0),(.62,3),(.72,0)])
        stamp = (f.washed("M -395,-92 L 395,-92 L 395,92 L -395,92 Z", "#fff8ed",
                          sw=11, off=(2, 1))
                 + f.text(0,53,"APPROVED", size=123, fill="#b44639"))
        art += group(stamp, 980, 635+drop, 1, -11)
    return finish(art,n)


def button(t,n):
    art = office()
    art += cast.pm(610,970,s=.67,mood="surprised" if t < .7 else "delighted",
                   bulb=1.0)
    art += f.washed("M 1070,640 L 1580,640 L 1580,930 L 1070,930 Z", "#888f94", off=(4,3))
    art += f.washed("M 1160,676 L 1490,676 L 1490,805 L 1160,805 Z", "#e8e3d6", off=(2,1))
    art += f.text(1325,760,"ASSEMBLE",size=51)
    push=k(t,[(0,0),(.7,0),(.9,1),(1.08,0)])
    art += f.washed(f"M 1200,{833+push*15} Q 1325,{800+push*15} 1450,{833+push*15} "
                    f"L 1450,{870+push*13} Q 1325,{902+push*13} 1200,{870+push*13} Z",
                    "#b44639", off=(4,2))
    return finish(art,n)


def maker(t,n):
    art = landscape()
    art += f.maker(960,985,.88,face=dict(
        look=(.6,-.1),brows="happy",mouth="flat",head_rot=k(t,[(0,-7),(1,3)])
    ))
    # A hammer can be holstered without changing the Maker rig.
    hy=k(t,[(0,570),(.9,760),(1.4,770)])
    art += f.path(f"M 1275,{hy-150} L 1235,{hy+95}",sw=21,stroke="#9c6b46")
    art += f.washed(f"M 1190,{hy-205} L 1360,{hy-205} L 1360,{hy-155} L 1190,{hy-155} Z",
                    "#68757a",off=(3,2))
    return finish(art,n,(370,260,1180,663.75))


def customer_success(t,n):
    art=landscape()
    angle=k(t,[(0,45),(.55,45),(1.25,0)])
    art+=official_full("customer success",960,1040,.97,
                       look=(.2,-.2),mouth="smile",
                       tilt=k(t,[(0,6),(1.3,-4)]),mic=angle)
    return finish(art,n,(450,220,1020,573.75))


def qa(t,n):
    art=landscape()
    art+=official_full("qa",960,1050,1.05,
                       look=(0,-.1),mouth="smile",tilt=k(t,[(0,8),(.8,0)]))
    if .55<t<1.0:
        flash=k(t,[(.55,-100),(.72,0),(1.0,140)])
        art+=f.path(f"M {850+flash},385 L {1060+flash},530",sw=9,stroke="#fffdf5")
    return finish(art,n,(450,210,1020,573.75))


def team(t,n,heroic=False):
    art=landscape()
    march=min(1,k(t,[(0,0),(2.7,1)])) if not heroic else 1
    # The same four performers from their close-ups.
    y=950
    drift=100*(1-march)
    art+=f.maker(415-drift,y,.56,
                 face=dict(look=(1,-.2),brows="happy",mouth="smile"),
                 phase=None if heroic else t*5)
    art+=official_full("customer success",780-drift/2,y,.60,look=(.2,-.1),tilt=3)
    art+=cast.pm(1120+drift/3,y,s=.64,pose="stand" if heroic else "walk",
                 phase=t*5,mood="delighted",bulb=1.0)
    art+=official_full("qa",1520+drift,y,.60,look=(-.3,-.1))
    # Suspiciously elaborate theatrical wind lines; no imported Marvel motifs.
    for i in range(4):
        xx=100+i*495+(45*math.sin(t*2+i))
        art+=f.path(f"M {xx},520 q 110,-25 210,0",sw=3,stroke="#e8e2d1")
    return finish(art,n)


def office_cut(t,n):
    art=office()+cramped_team(t)
    return finish(art,n)


def question(t,n):
    art=office()+cramped_team(t)
    if t>=.20:
        art+=f.bubble(930,260,1000,180,(870,630),
                      words="So... do we have a budget?",size=48)
    return finish(art,n)


def reaction(t,n):
    art=office()+cramped_team(t,reaction=t>.28)
    return finish(art,n)


def card(t,n):
    art=f.washed("M 0,0 L 1920,0 L 1920,1080 L 0,1080 Z","#fbf8f1",off=(2,1))
    art+=f.text(960,505,"STAEDEAN INNOVATION",size=83)
    art+=f.text(960,605,"ASSEMBLING NOW.",size=75,fill="#008c94")
    return finish(art,n)


SHOTS=[
    dict(name="approved",dur=1.5,draw=approved,cues=[]),
    dict(name="call",dur=1.5,draw=button,cues=[]),
    dict(name="maker",dur=2,draw=maker,cues=[]),
    dict(name="customer_success",dur=2,draw=customer_success,cues=[]),
    dict(name="qa",dur=2,draw=qa,cues=[]),
    dict(name="approach",dur=3,draw=team,cues=[]),
    dict(name="heroic",dur=3,draw=lambda t,n:team(t,n,heroic=True),cues=[]),
    dict(name="office_cut",dur=1,draw=office_cut,cues=[]),
    dict(name="question",dur=1.5,draw=question,cues=[]),
    dict(name="reaction",dur=1.5,draw=reaction,cues=[]),
    dict(name="card",dur=1,draw=card,cues=[]),
]


def timeline():
    at=0
    out=[]
    for shot in SHOTS:
        out.append((at,shot))
        at+=shot["dur"]
    assert at==DURATION, (at,DURATION)
    return out,at
