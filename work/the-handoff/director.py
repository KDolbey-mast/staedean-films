"""The Handoff: Customer Success leads an eighteen-second visual gag.

The parcel has one distinctive teal ribbon and red seal in both handoffs.
A continuous travelling package anchors the middle montage; the accumulating
outer packaging becomes the empty box. Each shot takes local seconds.
"""
import importlib.util,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ninja_cast',ROOT/'work/the-priority-ninja/director.py')
lib=importlib.util.module_from_spec(spec);spec.loader.exec_module(lib)
f,film,cast,props,rb=lib.f,lib.film,lib.cast,lib.props,lib.rb
FPS=12;BROWSER=lib.BROWSER;DURATION=18
k=film.ramp
VIEW=(100,180,1720,967.5)


def setting():return lib.original.setting()
def finish(art,n,view=VIEW):return rb.wrap_rb(art,view,film.boil(n))


def parcel(x,y,scale=1):
    """Small identifiable parcel; x,y is its bottom centre."""
    art=f.washed('M -40,-62 L 40,-62 L 40,0 L -40,0 Z','#c8a26b',sw=3,off=(2,1))
    art+=f.path('M -40,-47 L 40,-47 M 0,-62 L 0,0',sw=9,stroke='#17C8BE')
    art+=f'<circle cx="0" cy="-30" r="9" fill="#b5523b" stroke="#2e2520" stroke-width="2"/>'
    return f'<g transform="translate({x},{y}) scale({scale})">{art}</g>'


def paperwork(x,y,index):
    art=f.washed('M -35,-55 L 35,-55 L 35,12 L -35,12 Z','#fff9e9',sw=2,off=(1,1))
    for yy in (-36,-23,-10):art+=f.path(f'M -23,{yy} L 8,{yy}',sw=2,stroke='#7c817d')
    art+=f.path('M 10,-5 l 6,6 l 12,-18',sw=3,stroke='#43875b')
    return f'<g transform="translate({x},{y}) rotate({(-1 if index%2 else 1)*9})">{art}</g>'


def big_box(x,y,w,h,opened=0,forms=4):
    top=y-h;left=x-w/2;right=x+w/2
    art=f.washed(f'M {left},{top} L {right},{top} L {right},{y} L {left},{y} Z','#c8a26b',off=(3,2))
    if opened:
        # Visible empty floor and inside walls, rather than a black featureless hole.
        art+=f.washed(f'M {left+8},{top} L {right-8},{top} L {right-48},{top+115} L {left+48},{top+115} Z','#876448',sw=3,off=(2,1))
        art+=f.washed(f'M {left+48},{top+115} L {right-48},{top+115} L {right-75},{top+75} L {left+75},{top+75} Z','#b98a5e',sw=2,off=(1,1))
        art+=f.washed(f'M {left},{top} L {x},{top+50-135*opened} L {left-100*opened},{top-75*opened} Z','#dfbf91',sw=3,off=(2,1))
        art+=f.washed(f'M {right},{top} L {x},{top+50-135*opened} L {right+100*opened},{top-75*opened} Z','#dfbf91',sw=3,off=(2,1))
        # Front rim below the empty cavity gives an unmistakable open-box silhouette.
        art+=f.washed(f'M {left},{top+125} L {right},{top+125} L {right},{y} L {left},{y} Z','#c8a26b',sw=3,off=(3,2))
    else:
        art+=f.path(f'M {x},{top} L {x},{y}',sw=18,stroke='#17C8BE')
        art+=f.path(f'M {left},{top+35} L {right},{top+35}',sw=12,stroke='#17C8BE')
    for i in range(forms):
        xx=left+55+(w-110)*(i/max(1,forms-1))
        art+=paperwork(xx,y-35-(i%2)*30,i)
    return art


def official(role,x,y,t,scale=.6,hand=None,look=(0,.2),mouth='smile',tilt=0,mic=0):
    hip=y-370*scale
    art=f'<g transform="translate({x},{hip}) scale({scale}) translate(0,-330)">'+f.legs('stand')+'</g>'
    targets=None
    if hand:
        hx=(hand[0]-x)/scale;hy=(hand[1]-hip)/scale
        targets=[(-115,25),(hx,hy)] if hx>0 else [(hx,hy),(115,25)]
    art+=props.official(x,hip,scale,cast.OFFICIALS[role],look=look,mouth=mouth,
                       brows='puzzled' if mouth=='flat' else 'neutral',head_tilt=tilt,hand_targets=targets,mic_angle=mic)
    return art


def hero(role,x,y,t,hand=None,look=(0,.2)):
    scale=.52;arms=None
    if hand:
        hx=(hand[0]-x)/scale;hy=(hand[1]-y)/scale+700
        arms=[(f.SHL,(-170,200),(-120,320),'rest'),(f.SHR,(180,200),(hx,hy),'cup',True)]
    face=dict(look=look,brows='happy',mouth='smile')
    if role=='maker':return f.maker(x,y,scale,arms=arms,face=face)
    return cast.pm_full(x,y,scale,arms=arms or [(f.SHL,(-170,200),(-120,320),'rest'),(f.SHR,(170,200),(120,320),'rest',True)],**face)


def receive(t,n):
    art=setting()
    u=k(t,[(0,0),(.6,0),(1.65,1)])
    bx=1000-90*u;by=730
    # Customer offers with the free hand; CS receives from screen-right.
    release=k(t,[(1.65,0),(2.1,1)])
    hx=(bx-1130)/.58;hy=(by-930)/.58
    customer_hand=(hx*(1-release)-132*release,hy*(1-release)-410*release)
    art+=props.customer(1130,930,.58,pose='down',mouth='smile',look=(-1,.3),coffee=True,receive_at=customer_hand)
    art+=official('customer success',800,930,t,.68,hand=(bx,by),look=(1,.3),tilt=2*math.sin(t*2))
    art+=parcel(bx,by)
    return finish(art,n,(560,300,950,534.375))


CHAIN=('customer success','qa','pm','maker','planning')
POSITIONS=(340,620,900,1180,1500)
def chain(t,n):
    art=setting()
    stage=k(t,[(0,0),(.5,0),(1.35,1),(1.7,1),(2.55,2),(2.9,2),(3.75,3),(4.1,3),(5.2,4)])
    index=min(3,int(stage));fraction=stage-index
    bx=POSITIONS[index]+(POSITIONS[index+1]-POSITIONS[index])*fraction
    size=1+stage*1.0
    width=80+stage*84;height=62+stage*56
    bottom=755+stage*30
    for i,(role,x) in enumerate(zip(CHAIN,POSITIONS)):
        contact=abs(stage-i)<.85
        hand=(bx+(-width*.35 if x<bx else width*.35),bottom-8) if contact else None
        look=((bx-x)/max(150,abs(bx-x)),.4)
        if role in ('pm','maker'):art+=hero(role,x,950,t,hand,look)
        else:art+=official(role,x,950,t,hand=hand,look=look,tilt=2*math.sin(t*2+i))
    if stage<.25:art+=parcel(bx,bottom)
    else:art+=big_box(bx,bottom,width,height,forms=math.ceil(stage))
    # The helpful additions have their own brief downward motion on each arrival.
    for j,at in enumerate((1.35,2.55,3.75,5.2)):
        if at-.3<t<at+.2:
            drop=k(t,[(at-.3,0),(at,1)])
            art+=paperwork(bx+30,bottom-height-90+90*drop,j)
    return finish(art,n,(100,180,1800,1012.5))


def empty(t,n):
    art=setting();opened=k(t,[(0,0),(.4,0),(1.1,1)])
    art+=official('planning',1570,950,t,hand=(1430,780),look=(-1,.5),mouth='flat' if t>1.2 else 'smile',tilt=-4*opened)
    art+=official('customer success',650,950,t,.7,hand=(850,650-75*opened),look=(1,.8),
                  mouth='flat' if t>1.1 else 'smile',tilt=6*opened)
    art+=big_box(1120,950,560,350,opened,forms=4)
    if t>1.65:
        # A silent pause on a clearly empty cavity is the joke.
        art+=f.path('M 1095,665 q 14,-7 28,0',sw=1.5,stroke='#a48c6b')
    return finish(art,n,(400,300,1300,731.25))


def delivery(t,n):
    art=setting()
    nx=k(t,[(0,930),(.4,1060)])
    u=k(t,[(.4,0),(1.4,1)])
    bx=(nx+125)*(1-u)+1278*u;by=642
    # Reuse the established ninja rig; one shared contact point owns the parcel.
    art+=lib.ninja(nx,930,min(3,t+.55),(bx,by))
    reach=k(t,[(0,0),(.9,1)])
    hand=(-132-68*reach,-410-104*reach)
    art+=props.customer(1390,930,.56,pose='down',mouth='grin' if t>1.5 else 'smile',look=(-.8,.3),coffee=True,
                        receive_at=hand,head_tilt=6*math.sin(math.pi*k(t,[(1.6,0),(2.1,1)])))
    art+=parcel(bx,by)
    # Same distinct ribbon and seal as the first parcel, no new labels.
    return finish(art,n,(800,280,850,478.125))


def reaction(t,n):
    art=setting()
    angle=k(t,[(0,0),(1.2,0),(2,48)])
    rad=math.radians(angle)
    # Match the mic tip's rotation around the headset ear; hand follows it down.
    tip=(-86+60*math.cos(rad)-40*math.sin(rad),-288+60*math.sin(rad)+40*math.cos(rad))
    rise=k(t,[(.7,0),(1.2,1)])
    hand=(-130+(tip[0]+130)*rise,30+(tip[1]-30)*rise)
    art+=props.official(800,820,1.1,'cs',mouth='flat',look=(k(t,[(0,-1),(.7,-1),(1,1),(1.5,1)]),.4),
                        brows='puzzled',head_tilt=3,hand_targets=[hand,(110,20)],mic_angle=angle)
    art+=big_box(1400,1050,560,350,1,forms=4)
    return finish(art,n,(460,280,1050,590.625))

SHOTS=[dict(name='receive',dur=3,draw=receive,cues=[]),
       dict(name='chain',dur=6,draw=chain,cues=[]),
       dict(name='empty',dur=3,draw=empty,cues=[]),
       dict(name='delivery',dur=3,draw=delivery,cues=[]),
       dict(name='reaction',dur=3,draw=reaction,cues=[])]
def timeline():
    shots=[];start=0
    for shot in SHOTS:
        shots.append((start,shot));start+=shot['dur']
    return shots,start
