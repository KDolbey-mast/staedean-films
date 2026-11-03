"""The Priority: one setup, five helpful additions, one dry reaction.

BEATS and ARRIVALS drive both the performances and sound cues. Bulbs and hands
share world coordinates until release, so the props never float into position.
"""
import os,sys,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/staedean-cast/src'))
os.environ['MS_STYLE']='wash'
import cast,film,film2 as f,rb,props,sets
rb.STYLE='wash'
FPS=12
BROWSER=os.environ.get('ANIMATION_BROWSER',str(Path.home()/'Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell'))
DURATION=13
BEATS=dict(first=1.15,wide=2.2,look=8.4,pocket=9.05,glasses=10.35,close=9.0)
# Each newcomer keeps an individual gait and a small placement habit.
ARRIVALS=[dict(role='maker',start=2.15,place=3.35,x=850,bulb=920,habit='straighten'),
          dict(role='qa',start=3.05,place=4.25,x=990,bulb=1040,habit='straighten'),
          dict(role='customer success',start=3.95,place=5.15,x=1130,bulb=1160,habit='squeeze'),
          dict(role='product owner',start=4.85,place=6.05,x=1270,bulb=1280,habit='nudge'),
          dict(role='planning',start=5.75,place=6.95,x=1410,bulb=1400,habit='nudge')]
GROUND=930; TABLE_Y=765; BULB_SCALE=.75
BULB_Y=TABLE_Y-56*BULB_SCALE
k=film.ramp
MOUNTAIN=sets.big_mountain(show_sign=False).removeprefix(sets.sky())


def setting():
    return (f.sky()+'<g transform="translate(350,180) scale(.75)" opacity=".45">'+MOUNTAIN+'</g>'
        +f.cloud(210,220,.7)+f.cloud(1660,270,.9)
        +f.washed('M -100,700 C 500,640 1300,690 2030,650 L 2030,1200 L -100,1200 Z','#a9b394',off=(4,3)))


def pedestal():
    # A single display surface: identical labels accumulate without ranking.
    art=f.washed('M 780,765 L 1470,765 L 1445,950 L 805,950 Z','#e9e5dc',off=(3,2))
    art+=f.washed('M 755,749 L 1485,749 L 1495,770 L 745,770 Z','#d0c6b1',off=(3,2))
    art+=f.path('M 810,930 L 1435,930',sw=2,stroke='#b3ada1')
    return art


def idea(x,y,t,placed=False,angle=0):
    # A clipped local halo keeps increasing brightness readable, not a whiteout.
    brightness=k(t,[(0,.65),(3,.65),(7.2,1),(13,1)])
    bulb=f.bulb(x,y,s=BULB_SCALE,b=brightness,rot=angle,rays=0)
    # The shared bulb includes a room-sized light spill. Keep its actual glass,
    # filament and base, but use a smaller halo for this crowded outdoor display.
    body=(f'<ellipse cx="{x}" cy="{y-8}" rx="100" ry="95" fill="url(#priority-glow)" opacity="{brightness}"/>'
          +bulb[bulb.index('<g transform='):])
    for dx,dy in [(-48,-35),(-30,-62),(0,-72),(30,-62),(48,-35)]:
        body+=f.path(f'M {x+dx},{y+dy} l {dx*.18},{dy*.18}',sw=2,stroke='#e4b848')
    # The tag travels with its bulb. Its two-line wording stays legible in wide.
    tag=f.washed('M -45,48 L 45,48 L 45,101 L -45,101 Z','#fff9e9',sw=2,off=(1,1))
    tag+=f.text(0,69,'PRIORITY',size=15)+f.text(0,94,'1',size=25)
    tag=f'<g transform="translate({x},{y})">{tag}</g>'
    return body+tag


def sunglasses(x,y,angle=0):
    art=f.path('M -54,-5 L -35,0 M 62,-5 L 78,-12',sw=5)
    art+=f.path('M -6,-4 Q 8,-12 20,-4',sw=6)
    for xx in (-33,38):
        art+=f.washed(f'M {xx-27},-15 L {xx+27},-15 L {xx+24},15 Q {xx},32 {xx-24},15 Z','#30343e',sw=4,off=(1,1))
        art+=f.path(f'M {xx-13},-6 L {xx+1},6',sw=3,stroke='#a3b8c4')
    return f'<g transform="translate({x},{y}) rotate({angle})">{art}</g>'


def pm(t):
    scale=.62
    x=k(t,[(0,630),(1.35,630),(2.1,520)])
    first=k(t,[(0,0),(.4,0),(BEATS['first'],1)])
    bx=770+30*first; by=625+(BULB_Y-625)*first
    release=k(t,[(1.15,0),(1.55,1)])
    handx=(bx-x)/scale; handy=(by+40-GROUND)/scale+700
    hand=(handx*(1-release)+170*release,handy*(1-release)+300*release)
    arms=[(f.SHL,(-170,210),(-140,320),'rest'),(f.SHR,(210,190),hand,'cup',True)]
    front=''
    if t>=BEATS['pocket']:
        rise=k(t,[(9.05,0),(9.45,0),(10.35,1)])
        gx=115+(34-115)*rise; gy=270+(-134-270)*rise
        # The same prop travels from the shirt pocket to the eyes.
        grip=(gx+66,gy+2)
        withdraw=k(t,[(10.35,0),(10.75,1)])
        grip=(grip[0]*(1-withdraw)+150*withdraw,grip[1]*(1-withdraw)+320*withdraw)
        arms[1]=(f.SHR,(215,110),grip,'fist',True)
        front=sunglasses(gx,gy,12*(1-rise))
    motion=(630-x)/35
    legs=film.walk_legs(-motion,.6,lift=18) if 1.35<t<2.1 else 'stand'
    face=dict(look=(1,.2) if t<8.4 else (0,0),brows='happy' if t<6.7 else 'weary',
              mouth='smile' if t<6.7 else 'flat',eyes='closed' if 8.65<t<8.85 else 'open')
    art=cast.pm_full(x,GROUND,scale,legs_mode=legs,arms=arms,front=front,**face)
    return art,(bx,by)


def teammate(data,t,index):
    start,place=data['start'],data['place']
    if t<start:return '',None
    u=k(t,[(start,0),(place-.35,1)])
    x=2000+(data['x']-2000)*u
    travelled=2000-x
    phase=travelled/(31+index*3)+index*.8
    moving=u<1
    put=k(t,[(place-.35,0),(place,1)])
    # Carry in front of the torso, then set it down with a modest reach.
    bx=x+65+(data['bulb']-(data['x']+65))*put
    by=650+(BULB_Y-650)*put
    angle=0
    if data['habit']=='straighten':angle=k(t,[(place-.3,-10),(place+.18,-10),(place+.45,0)])
    if data['habit']=='squeeze':bx+=12*math.sin(math.pi*k(t,[(place-.4,0),(place+.35,1)]))
    if data['habit']=='nudge':by+=k(t,[(place,0),(place+.25,0),(place+.55,8)])
    release=k(t,[(place+.4,0),(place+.7,1)])
    if data['role']=='maker':
        scale=.52; hip=GROUND-700*scale
        hx=(bx-x)/scale;hy=(by+40-hip)/scale
        hx=hx*(1-release)+130*release;hy=hy*(1-release)+320*release
        swing=35*math.sin(phase) if moving else 0
        arms=[(f.SHL,(-170,200),(-140+swing,320),'rest'),(f.SHR,(190,170),(hx,hy),'cup',True)]
        art=f.maker(x,GROUND,scale,arms=arms,phase=phase if moving else None,
                    face=dict(look=(-.5,.4),brows='happy',mouth='smile',head_rot=2*math.sin(t*2)))
    else:
        scale=.60;hip=GROUND-370*scale
        legs=f.legs(film.walk_legs(phase,.6+index*.05,lift=20) if moving else 'stand')
        art=f'<g transform="translate({x},{hip}) scale({scale}) translate(0,-330)">{legs}</g>'
        hx=(bx-x)/scale;hy=(by+40-hip)/scale
        targets=[(-130+(25*math.sin(phase) if moving else 0),30),
                 (hx*(1-release)+100*release,hy*(1-release)+20*release)]
        art+=props.official(x,hip,scale,cast.OFFICIALS[data['role']],look=(-.3,.5),
                           head_tilt=1.5*math.sin(t*1.7+index),hand_targets=targets)
    return art,(bx,by,angle)


def frame(t,n):
    film.NOW=t
    art=setting()+'<defs><radialGradient id="priority-glow"><stop offset="0" stop-color="#ffed85" stop-opacity=".8"/><stop offset=".45" stop-color="#fff0a0" stop-opacity=".3"/><stop offset="1" stop-color="#fff5ba" stop-opacity="0"/></radialGradient></defs>'
    # Draw performers behind the surface, then bulbs/tags in front of their hands.
    ideas=[]
    for i,data in enumerate(ARRIVALS):
        actor,bulb=teammate(data,t,i)
        art+=actor
        if bulb:ideas.append(bulb)
    actor,first=pm(t)
    art+=actor+pedestal()
    art+=idea(*first,t)
    for bx,by,angle in ideas:art+=idea(bx,by,t,angle=angle)
    # Increasing light is local to the display; no flashes or whole-frame fade.
    if t>7:
        amount=k(t,[(7,0),(8,.06)])
        art+=f'<ellipse cx="1100" cy="700" rx="420" ry="140" fill="#fff8bb" opacity="{amount}" filter="url(#soft)"/>'
    view=(300,300,1120,630) if t<BEATS['wide'] else (150,190,1700,956.25)
    if t>=BEATS['close']:view=(345,285,590,331.875)
    return rb.wrap_rb(art,view,film.boil(n))

SHOTS=[dict(name='priority',dur=DURATION,draw=frame,cues=[])]
def timeline():return [(0,SHOTS[0])],DURATION
