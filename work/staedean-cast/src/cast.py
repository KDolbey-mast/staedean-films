"""THE CAST. One front door to every character, prop and set from the Mount Staedean films.

Every function returns an SVG fragment in 1920x1080 film space. Wrap fragments with `frame(...)` to get a finished
SVG in the house style, then render it with `render.render([(name, svg)], out_dir)`.

    import os; os.environ["MS_STYLE"] = "marker"     # the house look (set before importing cast)
    import cast
    art = cast.pm(700, 900, pose="stand", mood="hopeful", bulb=1.0)
    art += cast.customer(1200, 890, pose="thumbs_up", mood="happy")
    svg = cast.frame(art)

Continuity rules live in docs/CAST.md. The short version: the bulb only dims on the way up, the beard only grows,
the bulb is in the PM's left hand (screen-right), pupils always visible.
"""
import math
import film                                   # loads the rig and patches story.wrap
import film2
import story
from story import *                           # rig, props, sets
from rb import wrap_rb

# ------------------------------------------------------------------ moods
PM_MOODS = {
    "neutral":  dict(look=(1, 0), brows="neutral", mouth="neutral"),
    "hopeful":  dict(look=(1, -0.3), brows="happy", mouth="smile"),
    "delighted": dict(look=(1, -0.3), brows="happy", mouth="grin"),
    "surprised": dict(look=(0.4, -1.0), brows="raised", mouth="o", eyes="wide"),
    "talking":  dict(look=(1, -0.3), brows="raised", mouth="talk"),
    "thinking": dict(look=(0.55, 0.85), brows="quizzical", mouth="hmm"),
    "annoyed":  dict(look=(0.5, 0.9), brows="furrow", mouth="frown"),
    "weary":    dict(look=(1, 0.3), brows="weary", mouth="flat", eyes="half"),
    "sad":      dict(look=(0.3, 0.6), brows="sad", mouth="frown", eyes="tired"),
    "dismayed": dict(look=(0.35, -1.0), brows="sad", mouth="tiny", eyes="wide"),
    "content":  dict(look=(0, 0), brows="happy", mouth="smile", eyes="closed_happy"),
    "exhausted": dict(look=(0.6, 0.2), brows="sad", mouth="wobbly", eyes="half"),
}

CUSTOMER_MOODS = {
    "neutral": dict(mouth="flat", brows="neutral"), "happy": dict(mouth="smile", brows="neutral"),
    "delighted": dict(mouth="grin", brows="raised"), "puzzled": dict(mouth="flat", brows="puzzled"),
    "unimpressed": dict(mouth="frown", brows="puzzled"), "talking": dict(mouth="talk", brows="raised"),
}

AGES = {  # beard length, grey: the climb in five stops
    "fresh": (0.0, 0.0), "stubble": (0.06, 0.0), "first bench": (0.15, 0.0), "mid climb": (0.36, 0.27),
    "the fork": (0.5, 0.45), "summit": (1.05, 0.85),
}


# ------------------------------------------------------------------ the PM
def pm(x, y, s=0.42, *, pose="stand", mood="hopeful", bulb=1.0, age="fresh", phase=0.0, mirror_it=False, stack=0,
       pack=0, tank=False, mask=False):
    """The product manager. pose: stand | walk | trudge | sit | crawl | desk_head (head only)."""
    beard, grey = AGES.get(age, age) if isinstance(age, str) else age
    face = dict(PM_MOODS[mood])
    arms = [(SHL, (-170, 230), (-110, 330), "rest"), (SHR, (200, 190), (190, 110), "cup", True)]
    front = rig_bulb(190, 58, s=1, b=bulb, rays=0 if bulb < 0.6 else 7) if bulb is not None else ""
    if pose == "crawl":
        svg = pm_crawl(x, y, s, beard_tail=400 + 2200 * beard, grey=grey, bulb_b=bulb or 0.0, phase=phase,
                       look=face["look"], brows=face["brows"], mouth=face["mouth"], eyes=face.get("eyes", "tired"))
    elif pose in ("walk", "trudge"):
        svg = film.walker(x, y, s, phase, b=bulb or 0.0, beard=beard, grey=grey, lean=12 if pose == "trudge" else 0,
                          face=face, stack=stack, pack=pack, raised=pose == "walk", tank=tank)
    elif pose == "sit":
        svg = film.seat(x, beard=beard, grey=grey, b=bulb or 0.0, face=face)
    else:
        svg = pm_full(x, y, s, legs_mode="stand", beard=beard, grey=grey, arms=arms, front=front, mask=mask,
                      behind=backpack(pack) if pack else "", tank=tank,
                      before_arms=paper_stack(-180, 300, n=stack, w=140, tilt=-6) if stack else "", **face)
    return mirror(svg, x) if mirror_it else svg


def pm_head(x, y, s=1.0, mood="neutral", age="fresh", mask=False):
    beard, grey = AGES.get(age, age) if isinstance(age, str) else age
    f = dict(PM_MOODS[mood]); f.setdefault("eyes", "open")
    return f'<g transform="translate({x},{y}) scale({s})">' + head(f["look"], f["brows"], f["mouth"], f["eyes"], beard, grey, mask) + '</g>'


rig_bulb = bulb


def idea(x, y, s=1.0, brightness=1.0, dead=False):
    """The idea bulb. 1.0 blazing, ~0.5 glowing, ~0.2 ember, 0 off; dead=True for the burnt-out bulb."""
    return rig_bulb(x, y, s=s, b=brightness, dead=dead)


# ------------------------------------------------------------------ the customer
def customer(x, y, s=0.52, *, pose="phone", mood="neutral", look=(0, 0), blink=False, palette=None, coffee=True, box=False, box_glow=1.0):
    """The customer. pose: phone | down | wave | thumbs_up | thumbs_down | point | shake | hold_box."""
    m = CUSTOMER_MOODS[mood]
    return props_customer(x, y, s, pose, m["mouth"], look, m["brows"], blink=blink, pal=palette,
                          box=film2.product_box(0, -470, 1.0, glow=box_glow) if box else "", coffee=coffee)


import props as _props
props_customer = _props.customer


# ------------------------------------------------------------------ supporting cast
def maker(x, y, s=0.42, mood="hopeful", phase=None):
    return film2.maker(x, y, s, face=dict(PM_MOODS[mood]), phase=phase)


OFFICIALS = {"qa": "desk", "customer success": "cs", "product owner": "po", "planning": "planning"}


def official(department, x, y, s=0.6, gesture="rest", mood="smile"):
    """Behind-the-counter staff. department: qa | customer success | product owner | planning.
    gesture: rest | point_left | point_right | finger_up. mood: smile | flat | talk | o."""
    return _props.official(x, y, s, OFFICIALS[department], arm=gesture, mouth=mood)


def colleague(i, x, y, s=0.42, phase=0.0, bulb=0.8):
    svg = film.walker(x, y, s, phase, b=bulb, face=dict(look=(1, -0.2), brows="happy", mouth="smile"))
    return film2.recolour(svg, film2.COLLEAGUES[i % len(film2.COLLEAGUES)])


def frame(art, view=None, seed=7):
    """Finish a picture in the current house style (MS_STYLE env var: marker | colour | line)."""
    return wrap_rb(art, view, seed)
