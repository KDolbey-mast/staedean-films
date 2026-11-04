"""The Bigger Picture: a customer decision, helped by Customer Success.

Native 4:5 staging. The original customer and CS puppets carry all expressions;
new equipment icons, paper panels and tablet props stay local to this film.
"""
import math,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/staedean-cast/src'))
os.environ['MS_STYLE']='wash'
import cast,film,film2 as f,rb,props,sets,rig
from logo_path import LOGO_D,LOGO_W,LOGO_H
rb.STYLE='wash';FPS=12;WIDTH=1080;HEIGHT=1350
BROWSER=os.environ.get('ANIMATION_BROWSER',str(Path.home()/'Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell'))
k=film.ramp;FULL=(0,0,1080,1350)
MOUNTAIN=sets.big_mountain(show_sign=False).removeprefix(sets.sky())
INK='#2e2520';YELLOW='#d9b35c';TEAL='#5f8f7c'


def group(art,x,y,s=1):return f'<g transform="translate({x},{y}) scale({s})">{art}</g>'
def finish(art,n,view=FULL):
    # Keep the shared wash renderer, replacing only its landscape output dimensions.
    return rb.wrap_rb(art,view,film.boil(n)).replace('width="1920" height="1080"','width="1080" height="1350"',1)


def warning(x,y,s=1):
    art=f.washed('M 0,-40 L 36,22 L -36,22 Z','#e5b65c',sw=3,off=(1,1))+f.path('M 0,-22 L 0,0',sw=5)+f'<circle cx="0" cy="11" r="3" fill="{INK}"/>'
    return group(art,x,y,s)


def machine(x,y,s=1,unit='E-17',moving=0,show_id=True):
    """One shared silhouette links the physical machines and all picture cards."""
    colour=YELLOW if unit=='E-17' else '#79a9aa'
    art=f.washed('M -115,-36 L 73,-36 Q 98,-36 98,-9 Q 98,16 70,16 L -115,16 Q -143,13 -143,-10 Q -142,-36 -115,-36 Z','#56605f',sw=3,off=(1,1))
    for xx in (-105,-60,-15,30,70):
        art+=f'<circle cx="{xx}" cy="-10" r="15" fill="#a1adab" stroke="{INK}" stroke-width="2"/>'
        a=moving*8
        art+=f.path(f'M {xx-9*math.cos(a)},{-10-9*math.sin(a)} L {xx+9*math.cos(a)},{-10+9*math.sin(a)}',sw=2)
    art+=f.washed('M -115,-89 L 62,-89 L 82,-39 L -125,-39 Z',colour,sw=3,off=(2,1))
    art+=f.washed('M -92,-194 L -15,-194 L 0,-90 L -99,-90 Z',colour,sw=3,off=(1,1))
    art+=f.washed('M -81,-182 L -27,-182 L -15,-109 L -85,-109 Z','#b9d3e6',sw=2,off=(1,1))
    art+=f.tube([(45,-95),(100,-219),(175,-122)],17,colour)
    art+=f.washed('M 160,-131 L 203,-130 L 220,-78 L 167,-72 L 150,-96 Z','#9da9a3',sw=3,off=(1,1))
    if show_id:art+=f.text(-35,-53,unit,size=22)
    return group(art,x,y,s)


def request_card(x,y,s=1):
    art=f.washed('M -73,-100 L 73,-100 L 73,100 L -73,100 Z','#fffaf0',sw=3,off=(2,1))
    art+=machine(-12,4,.33,show_id=False)
    art+=f.text(0,67,'NOW',size=37)
    return group(art,x,y,s)


def yard(prepared=0):
    art=f.washed('M 60,120 L 710,120 L 710,590 L 60,590 Z','#fffefa',sw=4,off=(3,2))
    scenery=group(MOUNTAIN,210,150,.24)
    scenery+=f.washed('M 30,465 Q 410,415 760,465 L 760,610 L 30,610 Z','#bac5a3',sw=2,off=(3,2))
    # The chosen machine advances to a preparation pad, while service remains flagged.
    scenery+=f.washed('M 445,365 L 675,365 L 675,570 L 445,570 Z','#eee8db',sw=2,off=(2,1))
    scenery+=f.text(560,395,'SERVICE',size=27)+warning(645,435,.5)
    scenery+=f.path('M 115,558 L 395,558',sw=5,stroke='#f5efda')
    scenery+=f.text(250,585,'PREPARATION',size=20,fill='#667a6c')
    scenery+=machine(220+70*prepared,535,.5,moving=prepared*3)
    scenery+=machine(535,535,.46,'E-24')
    if prepared>.3:
        scenery+=f.path('M 128,500 l 12,14 l 27,-39',sw=6,stroke='#4e8166')
        scenery+=f.washed('M 180,545 L 175,523 L 169,545 Z','#c98c55',sw=2,off=(1,1))
    art+='<defs><clipPath id="yard-window"><rect x="65" y="125" width="640" height="460"/></clipPath></defs><g clip-path="url(#yard-window)">'+scenery+'</g>'
    art+=f.path('M 53,597 L 720,597',sw=10,stroke='#b5aa94')
    return art


def room(prepared=0):
    return yard(prepared)+f.path('M 0,1100 L 1080,1100',sw=2,stroke='#c9bfa9')


def desk():
    return f.washed('M 25,945 L 1050,945 L 1070,1040 L 10,1040 Z','#c6a982',sw=3,off=(3,2))+f.washed('M 35,1040 L 1045,1040 L 1045,1380 L 35,1380 Z','#d4bd9a',sw=3,off=(3,2))+f.path('M 70,1055 L 1010,1055',sw=2,stroke='#9d8260')


def customer(x=350,t=0,mood='flat',look=(1,.2),tilt=0,hand=None,active_right=False):
    # Preserve the original blond quiff, jacket mapping and burgundy tie.
    hand_local=((hand[0]-x)/.65,(hand[1]-1200)/.65) if hand else (-145,-410)
    art=props.customer(x,1200,.65,pose='down',coffee=False,receive_at=hand_local,mouth=mood,look=look,brows='raised' if mood=='talk' else ('puzzled' if mood=='flat' else 'neutral'),head_tilt=tilt)
    if active_right:
        # Replace the resting arm when a foreground prop-contact arm is animated.
        # This local adapter leaves the shared rig and earlier movies untouched.
        resting=f.tube([(116,-650),(146,-520),(130,-410)],44,'#4f7a5c')+f.washed('M 120,-424 C 112,-400 150,-390 150,-418 Z','#f0cdb0',sw=2.4,off=(1,1))
        assert resting in art,'Shared customer resting-arm shape changed; update adapter.'
        art=art.replace(resting,'',1)
    return art


def cs(x=855,t=0,point=False,nod=0,hand=None):
    # The exact shared CS head includes her ginger bob and headset microphone.
    targets=None
    if hand:targets=[((hand[0]-x)/.85,(hand[1]-945)/.85),(90,-6)]
    return props.official(x,945,.85,'cs',arm='point_left' if point else 'rest',mouth='smile',look=(-1,.5),head_tilt=nod,hand_targets=targets)


def laptop(opening=1):
    art=f.washed('M 670,925 L 955,925 L 997,973 L 630,973 Z','#9aa9aa',sw=3,off=(2,1))
    screen=f.washed('M -140,-205 L 140,-205 L 140,0 L -140,0 Z','#53696b',sw=3,off=(2,1))+f.washed('M -125,-187 L 125,-187 L 125,-17 L -125,-17 Z','#f7f5e8',sw=2,off=(1,1))
    screen+=f.text(0,-120,'ERP:',size=36)+f.text(0,-65,'AVAILABLE',size=30,fill='#3a795b')
    art+=f'<g transform="translate(815,925) scale(1,{max(.03,opening)})">{screen}</g>'
    return art


def setup(t,n):
    rx=k(t,[(0,-130),(.7,220)]);look=(0,1) if t<1 else (1,-.8) if t<1.7 else (1,.6)
    nod=5*math.sin((t-2.7)*7) if 2.7<t<3.4 else 0
    art=room()+customer(t=t,mood='smile',look=look,tilt=nod,hand=(220,870))+desk()+laptop(k(t,[(1.4,0),(2.1,1)]))+request_card(rx,860,.76)
    return finish(art,n)


REPORTS=('SERVICE','DEMAND','UTILIZATION')
def paper_panel(x,bottom,w,h,index,shade=False):
    top=bottom-h;slant=12 if index%2 else -12
    art=f.washed(f'M {x},{top} L {x+w},{top+slant} L {x+w},{bottom} L {x},{bottom} Z','#eee5d1' if shade else '#fffaf0',sw=3,off=(2,1))
    if w>35 and h>100:
        scale=min(1,w/110)
        art+=f.text(x+w/2,top+43,REPORTS[index%3],size=15*scale)
        for j in range(4):
            yy=top+80+j*max(25,(h-130)/5)
            art+=f.path(f'M {x+15},{yy} L {x+w-15},{yy}',sw=2,stroke='#a8a79b')
            if j%2==0:art+=f.path(f'M {x+15},{yy+12} L {x+15+(w-30)*(.4+.15*(index%3))},{yy+12}',sw=6,stroke=('#93ad9c','#c6b079','#9cabb9')[index%3])
    return art


def paper_wall(progress=1,fold=0):
    extent=k(progress,[(0,0),(.18,1),(.36,2),(.55,3),(.72,4),(.85,5),(1,6)])
    height=k(progress,[(0,120),(.35,220),(.6,360),(1,670)])*(1-fold)+23*fold
    width=100*(1-fold)+12*fold;art=''
    for i in range(6):
        visible=min(1,max(0,extent-i))
        if visible:art+=paper_panel(85+430*fold+i*width,950,width*visible,height*visible,i,i%2==1)
    return art


def reports(t,n):
    p=k(t,[(0,0),(.9,.18),(1.7,.36),(2.5,.55),(3.2,.72),(3.8,.85),(4.35,1)])
    art=room()+customer(t=t,mood='flat',look=(1,.6))+desk()+laptop()+paper_wall(p)
    if t>4.5:
        raised=k(t,[(4.5,0),(5.15,1)])
        yy=530-310*raised
        # Sleeve and fingers emerge above the paper; the tiny request stays the point.
        art+='<defs><clipPath id="above-paper"><rect x="0" y="0" width="1080" height="300"/></clipPath></defs><g clip-path="url(#above-paper)">'
        art+=f.tube([(445,460),(455,yy+100)],28,'#4f7a5c')
        art+=request_card(455,yy,.7)+f.hand_extra((455,yy+65),'fist')+'</g>'
    return finish(art,n)


def tablet(x,y,s=1,selected=False):
    # Same portrait screen and vertically stacked cards in wide and insert shots.
    art=f.washed('M -130,-165 L 130,-165 L 130,165 L -130,165 Z','#53696b',sw=4,off=(2,1))+f.washed('M -112,-147 L 112,-147 L 112,147 L -112,147 Z','#fbf6e9',sw=2,off=(1,1))
    art+=f.text(0,-115,'RENTAL IQ',size=24,fill='#315d5c')
    for i,label in enumerate(('UTILIZATION','DEMAND','RISK')):
        yy=-57+i*76
        art+=f.washed(f'M -100,{yy-31} L 100,{yy-31} L 100,{yy+31} L -100,{yy+31} Z','#fffaf0',sw=1.5,off=(1,1))
        art+=f.text(-88,yy-16,label,size=10,anchor='start')
        if i==0:art+=machine(-45,yy+22,.13,'E-17')+f.text(40,yy+12,'IDLE',size=12)
        elif i==1:
            for xx in (-30,0,30):art+=request_card(xx,yy+4,.17)
        else:art+=machine(-45,yy+22,.13,'E-24')+warning(45,yy+8,.25)
    if selected:art+=request_card(65,-53,.16)+f.path('M 80,-36 l 5,6 l 10,-15',sw=2,stroke='#52785d')
    return group(art,x,y,s)


def picture_card(x,y,kind):
    art=f.washed('M -395,-125 L 395,-125 L 395,125 L -395,125 Z','#fffaf0',sw=4,off=(2,1))
    art+=f.text(-350,-75,kind,size=33,anchor='start',fill='#315d5c')
    if kind=='UTILIZATION':
        art+=machine(-205,90,.58,'E-17')+f.text(90,0,'IDLE',size=38,fill='#52785d')+f.text(90,53,'E-17',size=27)
    elif kind=='DEMAND':
        for i in range(3):art+=request_card(-225+i*95,35,.5)
        art+=f.text(190,28,'WAITING',size=33)
    else:
        art+=machine(-205,90,.58,'E-24')+warning(95,0,1)+f.text(245,22,'SERVICE',size=29)+f.text(95,75,'E-24',size=27)
    return group(art,x,y)


def cards_view(t,selection=0,show_hand=False):
    art=f.washed('M 65,75 L 1015,75 L 1015,1280 L 65,1280 Z','#53696b',sw=5,off=(3,2))+f.washed('M 90,100 L 990,100 L 990,1255 L 90,1255 Z','#f1efdf',sw=2,off=(1,1))
    art+=f.text(540,170,'RENTAL IQ',size=48,fill='#315d5c')
    for i,(kind,yy) in enumerate((('UTILIZATION',360),('DEMAND',690),('RISK',1020))):
        alpha=k(t,[(i*.28,0),(i*.28+.24,1)])
        art+=f'<g opacity="{alpha}">'+picture_card(540,yy,kind)+'</g>'
    if selection>0:
        xx=k(selection,[(0,335),(1,765)]);yy=k(selection,[(0,725),(1,390)])
        art+=request_card(xx,yy,.58)
        if show_hand:
            # Sapphire sleeve identifies the customer as the actor making the choice.
            art+=f.tube([(1110,yy+180),(xx+80,yy+75)],60,'#4f7a5c')+group(f.hand_extra((0,0),'fist'),xx+54,yy+55,1.2)
    if selection>=.98:art+=f.path('M 875,430 l 14,16 l 30,-42',sw=7,stroke='#52785d')
    return art


def insight(t,n):
    if 2<=t<4.5:return finish(cards_view(t-2),n)
    entry=k(t,[(0,1200),(.7,855)])
    peek=k(t,[(.8,350),(1.5,720)])
    ty=k(t,[(.1,780),(.95,1000)])
    art=room()+customer(x=peek,t=t,mood='smile' if t>4.5 else 'flat',look=(-.7 if int(t*5)%3==0 else .7,.7))
    art+=cs(entry,t,point=1.1<t<1.9,hand=(855,ty-55) if t<1 else None)+desk()+laptop(k(t,[(0,1),(.8,.55)]))+paper_wall()+tablet(855,ty,.83)
    if t>=4.5:art+=f.bulb(740,510,s=.45,b=k(t,[(4.5,0),(4.85,.8)]),rays=5)
    return finish(art,n)


def decision(t,n):
    if t<1.8:
        choice=k(t,[(.15,0),(.95,1)])
        return finish(cards_view(5,choice,show_hand=t<1.3),n)
    fold=k(t,[(1.8,0),(3.5,1)])
    prep=k(t,[(3.6,0),(5.5,1)])
    xpos=k(t,[(1.8,720),(3.5,350)])
    nod=4*math.sin((t-4.5)*8) if 4.5<t<5.3 else 0
    art=room(prep)+customer(x=xpos,t=t,mood='smile',look=(1,-.8),active_right=t<3.6)+cs(t=t,nod=nod)+desk()+laptop(.55)+paper_wall(1,fold)+tablet(855,1000,.83,selected=True)
    if t<3.6:
        hx=685-90*fold;hy=280+650*fold
        art+=f.tube([(xpos+75,850),(hx,hy)],30,'#4f7a5c')+f.hand_extra((hx,hy),'fist')
    return finish(art,n)


def reaction(t,n):
    height=k(t,[(0,23),(.25,210),(.65,210),(1.05,23)])
    art=room(1)+customer(t=t,mood='smile',look=(1,-.8),active_right=t>.5)+cs()+desk()+laptop(.55)+paper_wall(1,1)+tablet(855,1000,.83,selected=True)
    art+=paper_panel(515,950,140,height,2)
    if t>.5:
        hy=950-height
        art+=f.tube([(425,788),(470,hy-65),(525,hy-56)],28,'#4f7a5c')
        art+=f.hand_extra((545,hy-52),'point',90)
    return finish(art,n,(110,500,760,950))


def end_card(t,n):
    # Every word is fully visible on every frame of the four-second closing hold.
    art='';xs=[220+i*80 for i in range(9)]
    wire='M 150,300 '+' '.join(f'Q {x-40},340 {x},318' for x in xs)+' Q 890,340 930,300'
    art+=f.path(wire,sw=3)
    for x in xs:art+=f.path(f'M {x},318 L {x},334',sw=3)+f.bulb(x,370,s=.32,b=.75,rot=180,rays=0)
    scale=880/LOGO_W
    art+=f'<g transform="translate(100,485) scale({scale})"><path d="{LOGO_D}" fill="#17c8be" fill-rule="evenodd" transform="translate(10,8)" filter="url(#wc)"/><path d="{LOGO_D}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round" stroke-dasharray="420 16 260 12 340 14"/></g>'
    art+=f.text(540,760,'EQUIPMENT RENTAL IQ',size=45,fill='#315d5c',family='Georgia, serif',weight='normal')
    art+=f.text(540,960,'BEYOND ERP.',size=63,family='Georgia, serif')
    art+=f.text(540,1050,'COMPETE ON INTELLIGENCE.',size=43,family='Georgia, serif')
    return finish(art,n)


SHOTS=[dict(name='01-request',dur=4,draw=setup),dict(name='02-reports',dur=6,draw=reports),dict(name='03-insight',dur=6,draw=insight),dict(name='04-decision',dur=6,draw=decision),dict(name='05-reaction',dur=2,draw=reaction),dict(name='06-end-card',dur=4,draw=end_card)]
DURATION=sum(s['dur'] for s in SHOTS)
def timeline():
    result=[];start=0
    for shot in SHOTS:result.append((start,shot));start+=shot['dur']
    return result,start
