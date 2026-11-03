"""Catapult performance shot: one geometry definition drives cup and flight.

Positive SVG rotation is clockwise. The arm starts behind the pivot and swings
upwards; release occurs while its tangent still points up and to the right.
"""
import math
import film,film2 as f,cast
from rb import wrap_rb
FPS=12
DURATION=44/12  # Cut just after the parcel passes the summit horizontally.
CUT=1.5
RELEASE=2.0833333333333335
FLIGHT_END=DURATION
BASE_X,BASE_Y,SCALE=400,1000,.65
PIVOT=(-40,-200)
CUP=(280,-40)
RELEASE_ANGLE=-150
CLOSE=(0,590,800,450)
WIDE=(-350,-480,2720,1530)

def key(t,points):return film.ramp(t,points)

def cup_position(angle):
    r=math.radians(angle);x,y=CUP
    return (BASE_X+SCALE*(PIVOT[0]+x*math.cos(r)-y*math.sin(r)),
            BASE_Y+SCALE*(PIVOT[1]+x*math.sin(r)+y*math.cos(r)))

def flight(elapsed):
    x,y=cup_position(RELEASE_ANGLE)
    # Match the arm's release tangent; gravity then bends the path over the peak.
    r=math.radians(RELEASE_ANGLE)
    tx=-CUP[0]*math.sin(r)-CUP[1]*math.cos(r)
    ty=CUP[0]*math.cos(r)-CUP[1]*math.sin(r)
    vx=510;vy=vx*ty/tx;gravity=700
    return x+vx*elapsed,y+vy*elapsed+.5*gravity*elapsed**2

def machine(angle,loaded,recoil=0):
    g=[]
    g.append(f.washed('M -180,0 L 180,0 L 155,-35 L -155,-35 Z','#a87a4e',off=(3,2)))
    for x in (-120,120):
        g.append(f'<circle cx="{x}" cy="0" r="32" fill="#c9a77a" stroke="#2e2520" stroke-width="4"/>')
        g.append(f.path(f'M {x-22},0 L {x+22},0 M {x},-22 L {x},22',sw=3))
    # Triangular support and a visible axle make the rotation easy to read.
    for width,colour in ((17,'#2e2520'),(10,'#b98a5e')):
        g.append(f.path('M -135,-30 L -40,-200 L 95,-30 M -135,-30 L 95,-30',sw=width,stroke=colour))
    beam=f.path('M -75,0 L 280,0',sw=19)+f.path('M -75,0 L 280,0',sw=11,stroke='#b98a5e')
    # A pivoting cradle stays upright while the arm rotates beneath it.
    cradle=f.washed('M -40,16 L -32,38 L 32,38 L 40,16 L 32,16 L 26,29 L -26,29 L -32,16 Z','#a87a4e',off=(2,1))
    if loaded: cradle=f.product_box(0,0,.43,rot=0,glow=.35)+cradle
    beam+=f'<g transform="translate({CUP[0]},{CUP[1]}) rotate({-angle})">{cradle}</g>'
    g.append(f'<g transform="translate({PIVOT[0]},{PIVOT[1]}) rotate({angle})">{beam}</g>')
    g.append('<circle cx="-40" cy="-200" r="18" fill="#6d543e" stroke="#2e2520" stroke-width="4"/><circle cx="-40" cy="-200" r="6" fill="#c8a26b"/>')
    return f'<g transform="translate({BASE_X+recoil},{BASE_Y}) scale({SCALE})">{"".join(g)}</g>'

def draw(t,n):
    film.NOW=t
    # Wind down a little, hold the tension, then snap through release and settle.
    angle=key(t,[(0,-185),(.85,-195),(1.9,-195),(RELEASE,-150),(2.25,-80),(2.42,-94),(2.65,-87),(3,-90)])
    flying=t>=RELEASE
    recoil=3*math.exp(-6*(t-RELEASE))*math.sin(30*(t-RELEASE)) if flying else 0
    art=f.big_mountain(show_sign=True)
    # Extend the backdrop for this wider camera, avoiding visible sky edges.
    art=art.replace('x="-200" y="-200" width="2400" height="1500"', 'x="-600" y="-650" width="3400" height="2000"')
    # Both operators stand clear of the moving arm. The Maker pulls the latch;
    # the PM watches the load, then follows its flight with a delayed celebration.
    anticipation=key(t,[(0,0),(.7,7),(1.8,7),(2.1,-5),(2.4,0)])
    maker_arms=[(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(210,220),(270,300),'fist',True)]
    art+=f.maker(100,1012,.3,arms=maker_arms,lean=-anticipation,
        face=dict(look=(1,-.25 if t<RELEASE else -1),brows='furrow' if t<RELEASE else 'happy',mouth='flat' if t<RELEASE else 'grin'))
    if t<RELEASE:
        # A latch cord gives the preparatory pull a visible purpose.
        art+=f.path('M 181,892 Q 250,930 330,949',sw=2.5,stroke='#6d543e')
    raised=key(t,[(0,300),(2.45,300),(2.7,-40),(2.9,0),(3.15,30)])
    arms=[(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(210,140),(250,raised),'open',True)]
    art+=cast.pm_full(650,1012,.3,legs_mode='stand',arms=arms,lean=key(t,[(0,0),(.8,-3),(1.8,-3),(2.2,-7),(2.6,0)]),
        head_rot=key(t,[(0,4),(1,0),(RELEASE,-10),(3,-12)]),look=(-.8,-.2) if t<RELEASE else (.8,-1),brows='raised' if t<2.45 else 'happy',mouth='o' if RELEASE<t<2.45 else 'smile' if t<RELEASE else 'grin')
    art+=machine(angle,not flying,recoil)
    if flying:
        elapsed=t-RELEASE;x,y=flight(elapsed)
        if elapsed>.08:
            tx,ty=flight(max(0,elapsed-.11))
            art+=f.path(f'M {tx:.1f},{ty:.1f} L {x:.1f},{y:.1f}',sw=2.5,extra='stroke-dasharray="8 9"')
        # The parcel retains its release rotation and size before a gentle tumble.
        art+=f.product_box(x,y,SCALE*.43,rot=elapsed*95,glow=.35)
    view=CLOSE if t<CUT else WIDE
    # The title is placed in the current view so the cut doesn't crop it away.
    card=f.day_card(view,'WEEK 4',.3)
    if t<CUT: card=f'<g transform="translate({view[0]},{view[1]}) scale(.5) translate({-view[0]},{-view[1]})">{card}</g>'
    art+=card
    return wrap_rb(art,view,film.boil(n))

CUES=[(0,'wind',{'d':DURATION,'intensity':.2},.04,'amb'),(.2,'creak',{},.3,'sfx'),
      (RELEASE,'twang',{},.45,'sfx'),(RELEASE,'whoosh',{'d':DURATION-RELEASE,'lo':300,'hi':3000},.3,'sfx'),
      (RELEASE+1.2,'triumph',{},.65,'music')]
