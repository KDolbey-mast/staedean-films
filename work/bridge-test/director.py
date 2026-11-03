"""The Perfect Bridge: a 12-second timing test using the established SVG cast.

One shared clock drives poses, hard camera cut and the sound cue list.
Adjust BEATS first when reviewing comic timing; the film is deliberately short.
"""
import os,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/staedean-cast/src'))
os.environ['MS_STYLE']='wash'
import cast,film,film2 as f,rb,props
rb.STYLE='wash'
FPS=12
BROWSER=os.environ.get('ANIMATION_BROWSER',str(Path.home()/'Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell'))
BEATS=dict(wide=2.5,plank=4.15,offer=5.15,plan=7.4,unrolled=8.35,deadpan=9.4,end=12)
GROUND=860

def k(t,points):return film.ramp(t,points)

def setting(t,background=""):
    # Optional distant scenery sits behind the grass, stream and performers.
    art=f.sky()+background+f.cloud(240,220,.7)+f.cloud(1640,270,.9)
    art+=f.washed('M -50,660 C 500,580 1100,625 1980,620 L 1980,1130 L -50,1130 Z','#a9b394',off=(4,3))
    art+=f.washed('M 1050,600 C 1055,750 1020,940 1000,1120 L 1110,1120 C 1120,940 1145,750 1130,600 Z','#b9d3e6',sw=3,off=(2,2))
    for i in range(7):
        y=640+i*70+6*math.sin(t*1.6+i)
        x=1086-20*(y-640)/420
        art+=f.path(f'M {x-18},{y} q 16,6 31,-1',sw=2,stroke='#6e9da5')
    for x,y in [(930,900),(1200,935),(970,745),(1195,710)]:
        art+=f.path(f'M {x},{y} l -6,-17 M {x},{y} l 9,-13',sw=2.2,stroke='#6b8b55')
    return art

def binoculars(x,y,angle=0):
    """Paired forward-facing lenses, with short barrels and a focus bridge."""
    inner=f.path('M -26,-5 L 26,-5',sw=14,stroke='#434951')
    inner+=f.washed('M -8,-20 L 8,-20 L 8,-2 L -8,-2 Z','#62696c',sw=2,off=(1,1))
    # Eyepieces sit against the face; larger objective rims project forward.
    for bx in (-28,28):
        inner+=f.washed(f'M {bx-17},-19 Q {bx},-26 {bx+17},-19 L {bx+29},3 L {bx+27},27 L {bx-24},27 L {bx-25},3 Z','#434951',sw=3,off=(1,1))
        inner+=f'<ellipse cx="{bx+4}" cy="10" rx="27" ry="25" fill="#62696c" stroke="#2e2520" stroke-width="3"/>'
        inner+=f'<ellipse cx="{bx+4}" cy="10" rx="20" ry="19" fill="#93bdce" stroke="#2e2520" stroke-width="2.5"/>'
        inner+=f.path(f'M {bx-7},9 Q {bx-6},-1 {bx+4},-2',sw=3,stroke='#fffaf0')
    return f'<g transform="translate({x},{y}) rotate({angle})">{inner}</g>'

def binocular_grip(x,y,angle,side):
    # Both wrists follow the prop transform, keeping contact while it lowers.
    r=math.radians(angle)
    return (x+side*58*math.cos(r),y+side*58*math.sin(r)+8)

def blueprint(width):
    # Reveal the drawing by clipping a fixed plan, so its bridge never stretches.
    drawing=f.washed('M 0,0 L 640,0 L 640,365 L 0,365 Z','#b9d3e6',off=(3,2))
    drawing+=f.text(320,54,'THE PERFECT BRIDGE',size=29)
    drawing+=f.path('M 35,280 L 600,280 M 55,285 L 55,310 M 580,285 L 580,310 M 55,305 L 580,305',sw=2.6,stroke='#486b80')
    for x in (150,485):
        drawing+=f.path(f'M {x-10},275 L {x-10},100 L {x+10},100 L {x+10},275',sw=5,stroke='#486b80')
    drawing+=f.path('M 40,260 Q 150,110 150,110 Q 320,285 485,110 Q 550,210 610,260',sw=4,stroke='#486b80')
    for x in range(65,600,35):
        yy=150+85*math.sin((x-150)/335*math.pi)
        drawing+=f.path(f'M {x},{max(140,yy)} L {x},276',sw=2,stroke='#486b80')
    drawing+=f.text(320,345,'CONCEPT 01',size=20)
    return (f'<defs><clipPath id="plan-unroll"><rect x="0" y="-15" width="{width}" height="395"/></clipPath></defs>'
            +f'<g clip-path="url(#plan-unroll)">{drawing}</g>'
            +f.washed(f'M {width-9},-8 Q {width+14},-16 {width+18},0 L {width+18},365 Q {width+2},383 {width-9},370 Z','#dce8ec',sw=3,off=(1,1)))

def frame(t,n):
    film.NOW=t
    art=setting(t)
    art+=cast.customer(1350,GROUND,.52,pose='down',mood='puzzled' if t>8.2 else 'happy',look=(-1,.35),blink=n in (42,43,83))
    # Maker's hands and plank share a single rotating frame of reference.
    plank_angle=k(t,[(0,-65),(BEATS['plank'],-65),(BEATS['offer'],0),(9.8,0),(10.1,-6),(10.45,0)])
    def plank_hand(local_x):
        r=math.radians(plank_angle)
        return (local_x*math.cos(r),200+local_x*math.sin(r))
    arms=[(f.SHL,(-180,150),plank_hand(-140),'cup'),(f.SHR,(190,150),plank_hand(140),'cup',True)]
    plank=f.washed('M -420,-28 L 420,-28 L 420,24 L -420,24 Z','#b98a5e',off=(3,2))
    plank+=f.path('M -390,-7 C -180,-18 100,10 385,-7 M -365,10 Q -100,-2 175,10',sw=2,stroke='#765338')
    plank=f'<g transform="translate(0,200) rotate({plank_angle})">{plank}</g>'
    art+=f.maker(495,GROUND,.46,arms=arms,front=plank,
        face=dict(look=(1,-.1) if t<BEATS['deadpan'] else (0,0),brows='happy' if t<7.7 else 'neutral',mouth='smile' if t<7.7 else 'flat',eyes='closed' if 10.6<t<10.75 else 'open',head_rot=k(t,[(0,-2),(4.2,-2),(5.2,4),(7.4,4),(8.7,-4),(9.4,0)])))
    # The PM lowers the binoculars before the wide reveal, leaving a reaction hold.
    hand_y=k(t,[(0,-135),(1.3,-135),(1.85,220)])
    binocular_angle=k(t,[(0,-5),(1.3,-5),(1.85,8)])
    binocular_x=k(t,[(0,22),(1.3,22),(1.85,5)])
    hands=[(f.SHL,(-190,70),binocular_grip(binocular_x,hand_y,binocular_angle,-1),'fist'),
           (f.SHR,(195,80),binocular_grip(binocular_x,hand_y,binocular_angle,1),'fist',True)]
    front=binoculars(binocular_x,hand_y,binocular_angle)
    if t>=6.1:
        hands=[(f.SHL,(-160,210),(-100,300),'fist'),(f.SHR,(210,130),(235,110),'cup',True)]
        front=binoculars(-46,300,12)
    art+=cast.pm_full(805,GROUND,.5,arms=hands,front=front,
        head_rot=k(t,[(0,-5),(1.3,-5),(1.85,3),(3.5,3),(4.5,8),(5.6,3),(6.8,-6),(8.4,-2)]),
        look=(1,-.15) if t<4.4 else (-1,.5) if t<6.1 else (1,-.2),brows='raised' if t<3 else 'happy',mouth='o' if 1.6<t<2.05 else 'smile',eyes='closed' if 6.5<t<6.65 else 'open')
    if t>=6.1:
        width=k(t,[(BEATS['plan'],12),(7.75,80),(8.1,610),(BEATS['unrolled'],640)])
        sag=k(t,[(7.4,0),(8.15,0),(8.35,15),(8.6,0)])
        art+=f'<g transform="translate(920,{370+sag})">'+blueprint(width)+'</g>'
    # The customer is physically occluded by the oversized plan, then a small
    # speech bubble gives the forgotten customer one final dry reaction.
    if t>=9.2:art+=f.bubble(1630,320,110,65,(1535,455),words='…',size=38)
    view=(650,285,460,258.75) if t<BEATS['wide'] else (100,170,1720,967.5)
    return rb.wrap_rb(art,view,film.boil(n))

SHOTS=[dict(name='bridge_opening',dur=12,draw=frame,cues=[])]
def timeline():return [(0,SHOTS[0])],12
