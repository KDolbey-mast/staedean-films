"""The Priority, with a quiet customer-focused ninja payoff.

Keep the original first eleven seconds. The four-second cutaway shows one
continuous handoff: both hands follow the same bulb until the giver releases it.
"""
import importlib.util,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('priority_original',ROOT/'work/the-priority/director.py')
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
f,film,cast,props,rb=original.f,original.film,original.cast,original.props,original.rb
FPS=12; BROWSER=original.BROWSER; DURATION=15; CUT=11
k=film.ramp


base_pedestal=original.pedestal
def labelled_pedestal():
    """The same front-panel label appears in both the main gag and cutaway."""
    return base_pedestal()+f.text(1125,900,'GOOD IDEAS',size=54)
original.pedestal=labelled_pedestal


def glare(t,strength_scale=1):
    """Continuous overexposure grows with the pile, nearly hiding the ensemble.

    Draw after the team, in their coordinate system. The cutaway scales this
    same light with the background huddle, leaving the actual handoff untouched.
    """
    strength=k(t,[(0,0),(2.8,0),(3.35,.12),(4.25,.28),(5.15,.48),
                  (6.05,.7),(6.95,.95),(7.7,1)])
    return (f'<g opacity="{strength*strength_scale}"><defs>'
        '<radialGradient id="desk-glare"><stop offset="0" stop-color="#ffffff"/>'
        '<stop offset=".48" stop-color="#ffffff" stop-opacity=".995"/>'
        '<stop offset=".68" stop-color="#fffef0" stop-opacity=".97"/>'
        '<stop offset=".85" stop-color="#fff7bd" stop-opacity=".65"/>'
        '<stop offset="1" stop-color="#fff0a0" stop-opacity="0"/></radialGradient>'
        '</defs><ellipse cx="1080" cy="625" rx="790" ry="525" fill="url(#desk-glare)"/></g>')


def bright_opening(t,n):
    # Overlay in scene coordinates after the original wash rendering.
    return original.frame(t,n).replace('</svg>',glare(t)+'</svg>')


def light(x,y,scale=.75,brightness=.8):
    bulb=f.bulb(x,y,s=scale,b=brightness,rays=0)
    return (f'<ellipse cx="{x}" cy="{y}" rx="85" ry="80" fill="url(#ninja-glow)"/>'
            +bulb[bulb.index('<g transform='):])


def ninja(x,y,t,grip):
    """A friendly charcoal-clad courier, drawn with the existing wash primitives."""
    scale=.67;ink='#343944';shade='#252b35'
    lean=0  # Keep the carrying hand registered to the bulb during the entrance.
    art=''
    for side in (-1,1):
        art+=f.tube([(side*42,-300),(side*62,-150),(side*70,0)],53,ink)
        art+=f.washed(f'M {side*70-28},-15 Q {side*70},-35 {side*70+48},-8 L {side*70+48},10 L {side*70-28},10 Z',shade,sw=3,off=(2,1))
    art+=f.washed('M -105,-490 Q 0,-525 100,-490 L 112,-290 Q 0,-265 -112,-290 Z',ink,off=(3,2))
    art+=f.washed('M -110,-325 L 110,-325 L 110,-292 L -110,-292 Z',shade,sw=3,off=(1,1))
    art+=f.path('M -20,-320 L 20,-300 L -12,-270 M 15,-307 L 45,-265',sw=9,stroke=shade)
    # Hood and eye opening establish the ninja without weapons or extra props.
    art+=f.washed('M -86,-587 C -100,-725 100,-735 100,-590 Q 90,-500 10,-505 Q -75,-505 -86,-587 Z',ink,off=(3,2))
    art+=f.washed('M -65,-628 Q 15,-650 78,-625 L 72,-578 Q 10,-564 -63,-584 Z','#f0cdb0',sw=3,off=(2,1))
    for ex in (-28,39):
        if t>2.55:
            art+=f.path(f'M {ex-12},-600 Q {ex},-615 {ex+12},-600',sw=3)
        else:
            art+=f'<ellipse cx="{ex}" cy="-604" rx="12" ry="16" fill="#fffaf0" stroke="#2e2520" stroke-width="2.5"/>'
            art+=f'<circle cx="{ex+4}" cy="-603" r="6" fill="#2e2520"/>'
    art+=f.washed('M -78,-635 L -142,-652 L -132,-633 L -170,-620 L -80,-615 Z',shade,sw=3,off=(2,1))
    # Giver's hand follows the bulb, then retreats once the customer has it.
    hx=(grip[0]-x)/scale;hy=(grip[1]-y)/scale
    release=k(t,[(2.05,0),(2.55,1)])
    hx=hx*(1-release)+140*release;hy=hy*(1-release)-330*release
    art+=f.tube([(-96,-470),(-135,-375),(-110,-310)],43,ink)
    art+=f.tube([(96,-470),(160,-390),(hx,hy)],43,ink)
    art+=f.washed(f'M {hx-22},{hy-6} Q {hx},{hy-22} {hx+22},{hy-6} Q {hx+25},{hy+17} {hx-20},{hy+13} Z',shade,sw=3,off=(1,1))
    return f'<g transform="translate({x},{y}) scale({scale}) rotate({lean},0,0)">{art}</g>'


def background_team():
    # The first gag is still happening nearby: nobody in this huddle has noticed.
    art='';bulbs=[]
    for i,data in enumerate(original.ARRIVALS):
        actor,bulb=original.teammate(data,11.8,i);art+=actor;bulbs.append(bulb)
    actor,first=original.pm(11.8)
    art+=actor+original.pedestal()+original.idea(*first,11.8)
    for bx,by,angle in bulbs:art+=original.idea(bx,by,11.8,angle=angle)
    # Keep the team opaque; fading the whole group let scenery show through it.
    # Lower only the cutaway's glare so the faces and desk remain identifiable.
    return '<g transform="translate(-100,240) scale(.52)">'+art+glare(11.8,strength_scale=.58)+'</g>'


def cutaway(t,n):
    film.NOW=CUT+t
    # Remove the low mountain cloud directly behind the small background huddle.
    art=original.setting().replace(original.sets.cloud(420,640,1.2), "")
    art+='<defs><radialGradient id="ninja-glow"><stop stop-color="#ffe998" stop-opacity=".5"/><stop offset="1" stop-color="#fff5c0" stop-opacity="0"/></radialGradient><radialGradient id="priority-glow"><stop stop-color="#ffe998" stop-opacity=".6"/><stop offset="1" stop-color="#fff5c0" stop-opacity="0"/></radialGradient></defs>'
    art+=background_team()
    nx=k(t,[(0,930),(.55,1060)])
    transfer=k(t,[(.7,0),(1.9,1)])
    bx=(nx+125)*(1-transfer)+1278*transfer
    by=605-5*transfer
    # Keep wrist contact exact: scale .75 gives a 42-pixel bulb base.
    grip=(bx,by+42)
    art+=ninja(nx,930,t,grip)
    reach=k(t,[(.55,0),(1.55,1)])
    receive=(-132+(-200+132)*reach,-410+(-514+410)*reach)
    nod=7*math.sin(math.pi*k(t,[(2.1,0),(2.65,1)]))
    art+=props.customer(1390,930,.56,pose='down',mouth='grin' if t>2 else 'smile',
                        look=(-.8,.3),coffee=True,receive_at=receive,head_tilt=nod)
    art+=light(bx,by)
    # Matching silhouette makes the need explicit without a line of explanation.
    art+=f.bubble(1550,330,180,130,(1430,465),lines=0)
    icon=f.bulb(1528,325,s=.65,b=.05,rays=0)
    art+=icon
    if t>=2.05:
        art+=f.path('M 1570,330 l 15,17 l 32,-42',sw=7,stroke='#43875b')
    return rb.wrap_rb(art,(50,160,1740,978.75),film.boil(n))

SHOTS=[dict(name='priority',dur=CUT,draw=bright_opening,cues=[]),
       dict(name='ninja',dur=4,draw=cutaway,cues=[])]
def timeline():return [(0,SHOTS[0]),(CUT,SHOTS[1])],DURATION
