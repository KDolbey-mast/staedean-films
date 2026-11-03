"""Full first cut. Reuse the approved opening, then bring the cast to the customer.

Each shot uses local seconds. SHOTS is the single source for the edit and audio.
The shared puppets are untouched; all new staging lives in this file.
"""
import sys, math, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('bridge_opening',ROOT/'work/bridge-test/director.py')
opening=importlib.util.module_from_spec(spec);spec.loader.exec_module(opening)
f,film,cast,props,rb=opening.f,opening.film,opening.cast,opening.props,opening.rb
FPS=12; BROWSER=opening.BROWSER
k=opening.k
VIEW=(100,170,1720,967.5)
ROLES=('qa','customer success','product owner','planning')


def finish(art,n):return rb.wrap_rb(art,VIEW,film.boil(n))

def plank(x,y,angle=0):
    # The same 386-world-unit board from the opening, with its grain intact.
    art=f.washed('M -193,-12 L 193,-12 L 193,12 L -193,12 Z','#b98a5e',off=(2,1))
    art+=f.path('M -177,-3 Q -30,-9 177,-3 M -165,5 Q 30,-1 150,5',sw=1.5,stroke='#765338')
    return f'<g transform="translate({x},{y}) rotate({angle})">{art}</g>'


def official(role,x,y,t,index=0,travel=0,gesture='rest',look=(.6,.2)):
    scale=.48; hip=y-370*scale
    phase=travel/(30+index*3)+index*1.3
    moving=abs(travel)>0
    lower=f.legs(film.walk_legs(phase,.65+index*.04,lift=22) if moving else 'stand')
    art=f'<g transform="translate({x},{hip}) scale({scale}) translate(0,-330)">{lower}</g>'
    art+=props.official(x,hip,scale,cast.OFFICIALS[role],arm='walk' if moving else gesture,
        mouth='smile',look=look,walk_phase=phase,swing=.5+index*.13,
        head_tilt=1.8*math.sin(t*1.3+index))
    return art


def hero(role,x,y,t,look=(1,.2),hands=None,travel=0,lean=0,mouth='smile',front='',crouch=0):
    phase=travel/35
    swing=math.sin(phase)*50 if travel else 0
    arms=hands or [(f.SHL,(-170-swing*.3,200),(-140-swing,320),'rest'),
                   (f.SHR,(170+swing*.3,200),(140+swing,320),'rest',True)]
    options=dict(arms=arms,front=front,lean=lean)
    face=dict(look=look,brows='happy',mouth=mouth,head_rot=2*math.sin(t*1.5))
    legs=film.walk_legs(phase,.8,lift=22) if travel else 'stand'
    if crouch:
        # Lower the torso while shortening/bending the legs, keeping shoes planted.
        foot=700-crouch/.46
        legs=[((-80,340),(-145,410),(-90,foot)),((80,340),(155,410),(90,foot))]
    if role=='maker':return f.maker(x,y+crouch,.46,legs=legs,face=face,**options)
    return cast.pm_full(x,y+crouch,.46,legs_mode=legs,**face,**options)


def grand_bridge(progress=1):
    # Impressive engineering, carefully placed over dry land beside the stream.
    art=''
    if progress>.05:
        art+=f.washed('M 220,735 L 900,735 L 900,765 L 220,765 Z','#b9c4cc',off=(3,2))
        for x in (290,835):
            art+=f.washed(f'M {x-22},765 L {x-22},370 L {x+22},370 L {x+22},765 Z','#b9c4cc',off=(3,2))
    if progress>.4:
        art+=f.path('M 220,725 L 290,385 Q 560,730 835,385 L 900,725',sw=7,stroke='#697b87')
        for x in range(320,820,38):
            top=385+170*math.sin((x-290)/545*math.pi)
            art+=f.path(f'M {x},{top} L {x},735',sw=3,stroke='#697b87')
    if progress>.75:
        art+=f.path('M 220,695 L 900,695',sw=5,stroke='#697b87')
        for x in range(230,900,35):art+=f.path(f'M {x},695 L {x},735',sw=3)
        art+=f.text(565,335,'THE PERFECT BRIDGE',size=30)
    return art


def board_hands():
    # Match the held board at world y=780 and -8 degrees in the two middle shots.
    return [(f.SHL,(-180,180),(-140,240),'cup'),
            (f.SHR,(180,180),(140,201),'cup',True)]


def planning(t,n):
    art=opening.setting(t)
    art+=cast.customer(1350,860,.52,pose='down',mood='puzzled',look=(-1,.2),blink=n%43==0)
    # A cut to the working huddle makes room for the four familiar specialists.
    for i,role in enumerate(ROLES):
        arrival=k(t,[(i*.3,0),(2+i*.3,1)])
        x=190+i*190-(1-arrival)*450
        art+=official(role,x,710,t,i,travel=(arrival*450 if arrival<1 else 0),
            gesture='finger_up' if int(t*1.1)%4==i else 'rest')
    art+=hero('maker',350,1000,t,look=(1,-.4),mouth='flat',hands=board_hands())
    art+=plank(350,780,-8)
    art+=hero('pm',825,1000,t,look=(-1,-.3))
    # The plan balloons through three revisions while the customer stays visible.
    scale=k(t,[(0,.55),(2,.55),(2.4,.72),(4.2,.72),(4.6,.9)])
    art+=f'<g transform="translate({520-320*scale},730) scale({scale},.5)">'+opening.blueprint(640)+'</g>'
    if t>2:art+=f.text(520,1030,'REVISED. REVISED AGAIN.',size=26)
    return finish(art,n)


def reveal(t,n):
    art=opening.setting(t)+grand_bridge(k(t,[(0,.1),(.7,.45),(1.4,1)]))
    art+=hero('maker',340,1000,t,mouth='flat',hands=board_hands())+plank(340,780,-8)
    art+=hero('pm',780,1000,t,look=(1,0),mouth='smile' if t<3 else 'o')
    for i,role in enumerate(ROLES):art+=official(role,260+i*180,905,t,i,look=(1,0))
    art+=cast.customer(1350,860,.52,pose='point' if t>2.5 else 'down',mood='puzzled',look=(-1,.8))
    if t>3.2:art+=f.bubble(1470,290,270,85,(1340,470),words='Just here.',size=31)
    return finish(art,n)


def customer_walk(x,y,t,travel):
    # Reuse the customer's jacket, coffee and face with the established leg rig.
    phase=travel/32
    upper=props.customer(0,0,1,pose='walk',mouth='smile',look=(-.7,.2),coffee=True,
                         walk_phase=phase,swing=.7,head_tilt=1.5*math.sin(phase))
    lower=f.legs(film.walk_legs(phase,.7,lift=20)).replace('#3a3a40','#323a48')
    return (f'<g transform="translate({x},{y}) scale(.48)"><defs><clipPath id="walking-customer">'
            '<rect x="-400" y="-1200" width="800" height="850"/></clipPath></defs>'
            +f'<g transform="translate(0,-700) scale(.65,1)">{lower}</g>'
            +f'<g clip-path="url(#walking-customer)">{upper}</g></g>')


def together(t,n):
    art=opening.setting(t)
    # The grand construction remains behind them: attention, rather than cast,
    # changes. Everyone forms a loose semicircle around the customer's crossing.
    art+='<g opacity=".4">'+grand_bridge()+'</g>'
    targets=[(685,825),(885,720),(1465,735),(1650,845)]
    for i,(role,(tx,ty)) in enumerate(zip(ROLES,targets)):
        u=k(t,[(i*.22,0),(2.8+i*.22,1)])
        startx=260+i*180
        x=startx+(tx-startx)*u
        y=905+(ty-905)*u
        art+=official(role,x,y,t,i,travel=((x-startx) if u<1 else 0),look=((1070-x)/600,.4))
    # Board and wrists share world-space anchors during the placement.
    settle=k(t,[(0,0),(3.5,0),(4.8,1)])
    board_y=650+(895-650)*settle
    board_x=k(t,[(0,520),(3,1070)])
    maker_x=k(t,[(0,350),(3,900),(5.8,900),(6.6,800)])
    pm_x=k(t,[(0,690),(3,1240)])
    crouch=110*k(t,[(3.5,0),(4.8,1),(5.15,1),(5.8,0)])
    for role,x,gripx in [('maker',maker_x,board_x-140),('pm',pm_x,board_x+140)]:
        release=k(t,[(4.8,0),(5.3,1)])
        local_x=(gripx-x)/.46
        local_y=(board_y-900-crouch)/.46+700
        near=(local_x*(1-release)+(-120 if role=='maker' else 120)*release,
              local_y*(1-release)+320*release)
        hands=[(f.SHL,(-165,230),(near[0]-22,near[1]),'cup'),(f.SHR,(165,230),(near[0]+22,near[1]),'cup',True)]
        # Lean is avoided here so the hands stay registered to the shared plank.
        travel=x-(350 if role=='maker' else 690) if t<3 else (x-900 if role=='maker' and 5.8<t<6.6 else 0)
        gaze=(0,.8) if t<5.3 else ((1,.1) if role=='maker' else (-1,.1))
        art+=hero(role,x,900,t,look=gaze,hands=hands if t<5.3 else None,crouch=crouch,travel=travel)
    art+=plank(board_x,board_y)
    if t<7:
        art+=cast.customer(1350,895,.48,pose='point' if t<2 else 'down',mood='happy',look=(-1,.6),blink=n%47==0)
    else:
        distance=k(t,[(7,0),(10,400)])
        if t<10:art+=customer_walk(1350-distance,895,t,distance)
        else:art+=cast.customer(950,895,.48,pose='thumbs_up',mood='happy',look=(1,0))
    return finish(art,n)


def ending(t,n):
    # Freeze positions, not drawing boil: this keeps the final tableau continuous.
    frame=together(11.9,n)
    caption=f.text(1060,1010,'Start with the customer.',size=43)
    caption+=f.text(1060,1060,'Then build what helps.',size=30)
    return frame.replace('</svg>',caption+'</svg>')

SHOTS=[dict(name='opening',dur=12,draw=opening.frame,cues=[]),
       dict(name='planning',dur=7,draw=planning,cues=[]),
       dict(name='reveal',dur=6,draw=reveal,cues=[]),
       dict(name='together',dur=12,draw=together,cues=[]),
       dict(name='ending',dur=4,draw=ending,cues=[])]
def timeline():
    result=[];start=0
    for shot in SHOTS:result.append((start,shot));start+=shot['dur']
    return result,start
