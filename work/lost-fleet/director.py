"""The Lost Fleet: one world, one sheep, one 25-second joke.

Equipment IDs persist through the montage, clipboard and map. The map is
explicitly recorded history, not a promise of universal live GPS tracking.
"""
import math,os,sys,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'work/staedean-cast/src'))
os.environ['MS_STYLE']='wash'
import cast,film,film2 as f,rb,props,sets
from logo_path import LOGO_D,LOGO_W,LOGO_H
spec=importlib.util.spec_from_file_location('bridge_props',ROOT/'work/bridge-test/director.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
rb.STYLE='wash';FPS=12;BROWSER=bridge.BROWSER
k=film.ramp;FULL=(0,0,1920,1080)
MOUNTAIN=sets.big_mountain(show_sign=False).removeprefix(sets.sky())
INK='#2e2520';YELLOW='#d9b35c';TEAL='#17c8be'


def finish(art,n,view=FULL):return rb.wrap_rb(art,view,film.boil(n))
def group(art,x,y,s=1,angle=0):return f'<g transform="translate({x},{y}) scale({s}) rotate({angle})">{art}</g>'


def landscape(t=0):
    art=f.sky()+group(MOUNTAIN,640,200,.47)
    art+=f.cloud(200,230,.65)+f.cloud(1710,250,.85)
    art+=f.washed('M -300,760 Q 550,650 1100,720 Q 1550,640 2200,710 L 2200,1200 L -300,1200 Z','#b5bf99',sw=2,off=(5,3))
    for x,y in ((150,920),(550,810),(1540,950),(1760,810)):
        art+=f.path(f'M {x},{y} l -9,-28 M {x},{y} l 12,-21 M {x+14},{y+2} l 8,-20',sw=2,stroke='#6b8b55')
    return art


def yard(t=0):
    art=landscape(t)
    art+=f.washed('M -100,800 Q 1000,740 2050,790 L 2050,1200 L -100,1200 Z','#d6c8ae',sw=2,off=(4,3))
    for i in range(3):
        x=870+i*310
        art+=f.path(f'M {x},805 L {x-110},1040 L {x+170},1040 L {x+190},805',sw=5,stroke='#fffaf0')
        art+=f.text(x+50,855,f'0{i+1}',size=27,fill='#8e826f')
    # Fence and yard sign locate the story without building an elaborate set.
    for x in range(50,1850,140):art+=f.path(f'M {x},770 L {x},690',sw=4,stroke='#9b927f')
    art+=f.path('M 30,710 L 1840,710 M 30,747 L 1840,747',sw=3,stroke='#9b927f')
    art+=f.washed('M 80,590 L 350,590 L 350,695 L 80,695 Z','#fff9e9',sw=3,off=(2,1))+f.text(215,633,'RENTAL YARD',size=26)+f.text(215,668,'3 UNITS',size=23,fill='#5b6c64')
    return art


def clipboard(x,y):
    art=f.washed('M -60,-165 L 60,-165 L 60,0 L -60,0 Z','#b98a5e',sw=3,off=(2,1))
    art+=f.washed('M -51,-153 L 51,-153 L 51,-10 L -51,-10 Z','#fffaf0',sw=2,off=(1,1))
    art+=f.washed('M -21,-174 L 21,-174 L 21,-149 L -21,-149 Z','#9caeac',sw=2,off=(1,1))
    for i,label in enumerate(('E-017','C-008','D-023')):
        art+=f.text(-38,-115+i*37,label,size=18,anchor='start')
        art+=f.path(f'M 28,{-132+i*37} h 15 v 15 h -15 Z',sw=1.6)
    return group(art,x,y)


def customer(t,scratch=False,surprised=False):
    tilt=k(t,[(0,9),(.9,9),(1.5,-6)]) if not surprised else -3
    hand=(-120+8*math.sin(t*19),-890+9*math.sin(t*19)) if scratch else (-145,-410)
    art=props.customer(480,980,.57,pose='down',coffee=False,receive_at=hand,look=(.8,1) if t<1 else (1,-.15),brows='raised' if surprised else 'puzzled',mouth='talk' if surprised else 'frown',head_tilt=tilt)
    art+=clipboard(555,765)
    art+=group(f.hand_extra((0,0),'fist',0),548,716,.57)
    if surprised:
        eyes=''
        for ex in (-32,32):
            eyes+=f'<ellipse cx="{ex}" cy="-800" rx="20" ry="29" fill="#fffdf6" stroke="{INK}" stroke-width="2.6"/><circle cx="{ex+6}" cy="-795" r="7" fill="{INK}"/>'
        art+=group('<g transform="rotate(-3,0,-690)">'+eyes+'</g>',480,980,.57)
    return art


def tumbleweed(x,y,t):
    art=''
    for i in range(8):
        a=i*math.pi/4;xx=math.cos(a)*32;yy=math.sin(a)*32
        art+=f.path(f'M {-xx},{-yy} Q {yy+22},{xx-15} {xx},{yy} Q {-yy-22},{-xx+15} {-xx},{-yy}',sw=2,stroke='#9a8058')
    art+=f.path('M -47,4 Q 0,-45 46,8 M -30,-33 Q 40,0 -25,39',sw=2,stroke='#9a8058')
    return group(art,x,y,1,t*180)


def missing(t,n):
    art=yard(t)+customer(t,scratch=1.65<t<3.5)
    xx=k(t,[(.8,1880),(3.9,750)],smooth=False)
    art+=tumbleweed(xx,1000-15*abs(math.sin(t*7)),t)
    view=k(t,[(0,(200,290,1250,703.125)),(1.8,FULL)])
    return finish(art,n,view)


def wheel(x,y,r,t=0):
    art=f'<circle r="{r}" fill="#3c4244" stroke="{INK}" stroke-width="4"/><circle r="{r*.56}" fill="#8a9a9a" stroke="{INK}" stroke-width="3"/>'
    for i in range(6):
        a=i*math.pi/3+t*5
        art+=f.path(f'M {math.cos(a)*r*.21},{math.sin(a)*r*.21} L {math.cos(a)*r*.45},{math.sin(a)*r*.45}',sw=4,stroke='#e1ddd0')
    return group(art,x,y)


def excavator(x,y,s=1):
    art=f.washed('M -280,-105 L 135,-105 Q 215,-100 215,-42 Q 210,15 145,18 L -270,18 Q -330,10 -330,-40 Q -330,-95 -280,-105 Z','#535d5d',sw=5,off=(3,2))
    for xx in range(-260,160,75):art+=wheel(xx,-45,39)
    art+=f.washed('M -240,-180 L 135,-180 L 170,-100 L -275,-100 Z',YELLOW,sw=4,off=(3,2))
    art+=f.washed('M -155,-398 L 25,-398 L 65,-195 L -170,-195 Z',YELLOW,sw=4,off=(2,1))
    art+=f.washed('M -130,-373 L 4,-373 L 32,-225 L -139,-225 Z','#b9d3e6',sw=3,off=(2,1))
    art+=f.path('M -105,-360 L -42,-235 M -80,-365 L -18,-240',sw=3,stroke='#fffaf0')
    art+=f.tube([(100,-210),(250,-490),(440,-260)],39,YELLOW)
    art+=f.tube([(110,-220),(232,-440)],10,'#a8b9ba')
    art+=f.tube([(250,-465),(420,-272)],9,'#a8b9ba')
    art+=f.washed('M 406,-277 L 490,-282 L 530,-168 L 420,-155 L 378,-205 Z','#9caaa5',sw=4,off=(2,1))
    for xx in (430,455,480):art+=f.path(f'M {xx},-164 l 4,23',sw=7)
    for xx,yy in ((100,-210),(250,-490),(440,-260)):
        art+=f'<circle cx="{xx}" cy="{yy}" r="12" fill="#eee4c6" stroke="{INK}" stroke-width="3"/>'
    art+=f.text(-60,-130,'E-017',size=29)
    return group(art,x,y,s)


def cobweb(x,y,t):
    # Visible triangular web connects the cab and boom; the spider moves separately.
    art='';ends=[(-135,-110),(117,-219),(260,45),(40,135),(-120,90)]
    for xx,yy in ends:art+=f.path(f'M 0,0 L {xx},{yy}',sw=2,stroke='#8a958c')
    for q in (.3,.55,.8,1):
        pts=[(xx*q,yy*q) for xx,yy in ends]
        art+=f.path('M '+' L '.join(f'{xx},{yy}' for xx,yy in pts)+' Z',sw=2,stroke='#8a958c')
    yy=70+25*math.sin(t*2)
    art+=f.path(f'M -65,40 L -65,{yy}',sw=1.5,stroke='#77827c')
    art+=f'<ellipse cx="-65" cy="{yy+6}" rx="7" ry="10" fill="#4e5652"/>'
    for sign in (-1,1):
        for dy in (-4,3,9):art+=f.path(f'M -65,{yy+dy} l {sign*13},-5 l {sign*5},9',sw=1.5)
    return group(art,x,y)


def abandoned(t,n):
    art=landscape(t)+excavator(830,925,1.15)+cobweb(1000,580,t)
    for xx in (520,580,1100):art+=f.path(f'M {xx},930 q -10,-80 {10*math.sin(t*2)},-140 M {xx},890 l -26,-30 M {xx},880 l 24,-28',sw=3,stroke='#7c8c59')
    view=k(t,[(0,(400,250,1400,787.5)),(1.1,(260,100,1620,911.25))])
    return finish(art,n,view)


def tree():
    art=f.washed('M 920,1000 Q 945,740 905,540 L 760,425 L 785,395 L 960,480 L 1000,320 L 1040,330 L 1000,590 L 1160,435 L 1195,470 L 1040,680 L 1060,1000 Z','#a18460',sw=4,off=(4,2))
    art+=f.path('M 965,970 Q 985,750 951,565 M 1008,600 L 1168,460',sw=3,stroke='#7d654d')
    for x,y,s in ((720,380,1.2),(1000,250,1.6),(1250,380,1.3)):
        leaves=f.washed('M -160,30 Q -210,-30 -140,-75 Q -130,-145 -55,-115 Q 0,-175 62,-110 Q 160,-140 170,-50 Q 230,15 150,65 Q 50,105 -15,70 Q -110,115 -160,30 Z','#a9b394',sw=3,off=(4,2))
        art+=group(leaves,x,y,s)
    return art


def crane(x,y,t,s=1):
    art=f.washed('M -230,-100 L 210,-100 L 230,-30 L -240,-30 Z',YELLOW,sw=4,off=(2,1))
    art+=wheel(-145,-15,55)+wheel(145,-15,55)
    art+=f.washed('M -210,-230 L -70,-230 L -50,-105 L -220,-105 Z',YELLOW,sw=3,off=(2,1))
    art+=f.washed('M -190,-212 L -90,-212 L -76,-135 L -196,-135 Z','#b9d3e6',sw=3,off=(1,1))
    art+=f.tube([(30,-120),(310,-510)],35,YELLOW)
    art+=f.path('M 47,-120 L 315,-500',sw=7,stroke='#f5df98')
    swing=15*math.sin(t*3)
    art+=f.path(f'M 310,-510 L {310+swing},-180 Q {335+swing},-160 {312+swing},-145 Q {292+swing},-139 {291+swing},-158',sw=5)
    art+=f.text(30,-60,'C-008',size=27)
    return group(art,x,y,s,-9+2*math.sin(t*3))


def treed(t,n):
    art=landscape(t)+tree()
    art+=f.path(f'M 890,620 Q 1070,{660+8*math.sin(t*3)} 1350,560',sw=34,stroke='#9d805c')
    art+=crane(1080,590,t,.8)
    view=k(t,[(0,(470,350,1280,720)),(.65,(360,-40,1500,843.75))])
    return finish(art,n,view)


def sheep(x,y,t=0,s=1,bleat=False,hat=True):
    art=f.washed('M -60,40 Q -98,15 -72,-25 Q -80,-70 -40,-72 Q -10,-110 20,-80 Q 70,-93 80,-55 Q 110,-15 75,18 Q 83,65 32,64 Q -20,86 -60,40 Z','#fff9e9',sw=3,off=(2,1))
    art+=f.washed('M -38,-32 Q -65,-61 -85,-38 Q -88,-20 -45,-10 M 38,-32 Q 67,-62 88,-36 Q 86,-18 42,-10','#af9d85',sw=3,off=(2,1))
    art+=f.washed('M -40,-37 Q 0,-64 41,-34 L 34,31 Q 0,66 -33,30 Z','#d1bda1',sw=3,off=(2,1))
    for ex in (-17,17):
        art+=f'<ellipse cx="{ex}" cy="-14" rx="11" ry="15" fill="#fffdf6" stroke="{INK}" stroke-width="2"/><circle cx="{ex+(0 if bleat else 4)}" cy="-13" r="5" fill="{INK}"/>'
    art+=f.path('M -5,10 Q 0,16 5,10',sw=3)
    if bleat:art+=f'<ellipse cx="0" cy="31" rx="17" ry="{12+8*abs(math.sin(t*20))}" fill="#713b31" stroke="{INK}" stroke-width="2.5"/>'
    else:art+=f.path('M -12,25 Q 0,35 13,24',sw=2.5)
    if hat:
        art+=f.washed('M -52,-50 Q -47,-111 0,-113 Q 48,-110 52,-50 Z',YELLOW,sw=3,off=(2,1))
        art+=f.washed('M -63,-53 Q 0,-63 64,-53 L 66,-40 L -65,-40 Z','#e9c46a',sw=3,off=(1,1))
        art+=f.path('M -8,-108 L -9,-60 M 8,-108 L 9,-60',sw=3,stroke='#b38a43')
    return group(art,x,y,s)


def dumper(x,y,t,s=1,bleat=False):
    """Open cab keeps the driver reveal readable; all wheel motion shares one clock."""
    art=f.washed('M -310,-215 L -100,-215 L -60,-60 L -270,-60 Z',YELLOW,sw=4,off=(3,2))
    art+=f.washed('M -325,-245 L -90,-245 L -105,-205 L -305,-205 Z','#eed082',sw=4,off=(2,1))
    art+=f.path('M -280,-202 L -246,-90 M -218,-202 L -190,-90 M -156,-202 L -134,-90',sw=3,stroke='#ae8a46')
    # Roll cage behind the sheep, steering wheel and bonnet in front.
    art+=f.path('M -20,-85 L -20,-325 Q -20,-345 0,-345 L 175,-345 L 185,-105',sw=12,stroke='#5b6868')
    art+=f.washed('M 16,-170 Q -6,-158 10,-140 Q -2,-118 22,-100 Q 67,-75 132,-103 Q 154,-129 132,-151 Q 140,-176 111,-181 Z','#fff9e9',sw=3,off=(2,1))
    art+=sheep(70,-214,t,.73,bleat)
    art+=f.tube([(45,-154),(70,-136),(100,-134)],15,'#fff9e9')
    art+=f.tube([(120,-154),(135,-130)],15,'#fff9e9')
    art+=f.path('M 96,-136 l 10,4 M 132,-132 l 9,3',sw=12,stroke='#655d52')
    art+=f'<ellipse cx="125" cy="-135" rx="40" ry="15" fill="none" stroke="{INK}" stroke-width="6"/>'
    art+=f.path('M 125,-135 L 141,-83',sw=6)
    art+=f.washed('M -285,-80 L -40,-80 L -20,-120 L 165,-120 L 215,-70 L 215,-25 L -285,-25 Z',YELLOW,sw=4,off=(2,1))
    art+=f.washed('M 150,-170 L 210,-168 L 235,-75 L 166,-75 Z',YELLOW,sw=3,off=(2,1))
    art+=f.text(-160,-40,'D-023',size=23)
    art+=wheel(-210,0,63,t)+wheel(155,0,63,t)
    return group(art,x,y,s)


def sheep_driver(t,n):
    # Tracking camera follows the dumper; drifting scenery establishes travel even
    # once the wheels are outside the close driver composition.
    art=group(landscape(t),-100*t,0)
    # Passing tufts and rolling wheels sell motion while the camera pans to the cab.
    for i in range(8):
        xx=((i*300-t*180+2400)%2400)-200
        art+=f.path(f'M {xx},955 l 60,-3 M {xx+100},925 l 35,1',sw=3,stroke='#a99d7b')
    art+=dumper(1050,920+3*math.sin(t*15),t,1.65,bleat=1.8<t<2.65)
    view=k(t,[(0,(420,430,700,393.75)),(.45,(420,430,700,393.75)),(1.6,(820,390,680,382.5)),(3,(820,390,680,382.5))])
    return finish(art,n,view)


def tablet_shape():
    art=f.washed('M -160,-110 Q -175,-110 -175,-90 L -175,90 Q -175,110 -155,110 L 155,110 Q 175,110 175,90 L 175,-90 Q 175,-110 155,-110 Z','#53696b',sw=4,off=(2,1))
    art+=f.washed('M -150,-87 L 150,-87 L 150,87 L -150,87 Z','#f3f0de',sw=2,off=(1,1))
    art+=f.text(0,-28,'Rental IQ',size=27,fill='#315d5c')
    art+=f.path('M -115,45 Q -40,5 5,40 T 115,0',sw=4,stroke='#b5bf99')
    for xx,yy in ((-75,23),(5,35),(96,5)):art+=f'<circle cx="{xx}" cy="{yy}" r="9" fill="#17c8be"/>'
    return art


def maker_with_tablet(t,tap=False):
    arms=[(f.SHL,(-200,230),(-160,285),'cup'),(f.SHR,(220,150),(30 if tap else 160,240 if tap else 285),'point' if tap else 'cup',True)]
    front=group(tablet_shape(),0,270)
    if tap:
        # The tapping hand must render in front of the tablet glass, not behind it.
        front+=f.tube([(190,220),(65,250)],26,'#f0c9a6')+f.hand_extra((60,250),'point',180)
    return f.maker(870,980,.55,arms=arms,front=front,face=dict(look=(-1,.3),brows='happy',mouth='smile'))


def hero_arrives(t,n):
    art=yard(t)+customer(t+4)
    xx=k(t,[(0,1900),(.7,870)])
    if t<3.3:
        yy=k(t,[(0,-140),(2.3,-140),(2.8,260),(3.3,330)])
        scale=k(t,[(0,1.8),(2.8,1.8),(3.3,.05)])
        angle=k(t,[(.8,-10),(1.25,-10),(1.7,12),(2.2,12),(2.8,0)])
        bx=k(t,[(.7,-25),(1.25,-25),(1.7,30),(2.2,30),(2.8,0)])
        # The same paired lenses as The Perfect Bridge, enlarged for this gag.
        front=group(bridge.binoculars(0,0),bx,yy,scale,angle)
        r=math.radians(angle)
        hands=[]
        for side,shoulder in ((-1,f.SHL),(1,f.SHR)):
            hand=(bx+side*58*scale*math.cos(r),yy+side*58*scale*math.sin(r)+8*scale)
            hands.append((shoulder,(side*235,80),hand,'fist',side==1))
        art+=f.maker(xx,980,.55,arms=hands,front=front,phase=(t*8 if t<.7 else None),face=dict(look=(1,-.2),brows='happy',mouth='smile'))
    else:
        lift=k(t,[(3.3,0),(3.85,1)])
        arms=[(f.SHL,(-200,230),(-160,330-45*lift),'cup'),(f.SHR,(220,180),(160,330-45*lift),'cup',True)]
        art+=f.maker(870,980,.55,arms=arms,front=group(tablet_shape(),0,400-130*lift,lift),face=dict(look=(-1,.3),brows='happy',mouth='smile'))
    view=k(t,[(0,FULL),(.9,(250,340,1200,675)),(4.9,(250,340,1200,675))])
    return finish(art,n,view)


def fleet_map(t):
    art=f.washed('M 150,110 Q 150,75 190,75 L 1730,75 Q 1770,75 1770,115 L 1770,975 Q 1770,1010 1730,1010 L 190,1010 Q 150,1010 150,975 Z','#53696b',sw=5,off=(3,2))
    art+=f.washed('M 205,130 L 1715,130 L 1715,955 L 205,955 Z','#f4f0df',sw=3,off=(2,1))
    art+='<defs><clipPath id="map-screen"><rect x="205" y="130" width="1510" height="825"/></clipPath></defs><g clip-path="url(#map-screen)">'
    art+=f.text(960,205,'Recorded fleet locations',size=48,fill='#315d5c')
    art+=f.text(960,253,'Location history · illustrative',size=26,weight='normal',fill='#697971')
    art+=group(MOUNTAIN,920,285,.42)
    art+=f.path('M 310,760 Q 650,870 870,640 T 1580,520',sw=32,stroke='#ded3b8')
    art+=f.path('M 420,350 Q 600,620 900,480 T 1520,820',sw=22,stroke='#b9d3e6')
    art+=f.path('M 320,755 Q 700,840 870,635 T 1580,520',sw=3,stroke='#fffaf0',extra='stroke-dasharray="14 18"')
    # A hand-drawn connecting wire makes the location markers echo the festoon bulbs.
    art+=f.path('M 460,520 Q 730,360 1080,450 Q 1290,500 1490,735',sw=3,stroke='#8c927a')
    for i,(xx,yy,label) in enumerate(((460,520,'E-017'),(1080,450,'C-008'),(1490,735,'D-023'))):
        on=t>.35+i*.35
        art+=f.bulb(xx,yy,s=.65,b=.8 if on else 0,rot=0,rays=0)
        art+=f.text(xx,yy+95,label,size=31)
    art+=f.text(610,890,'Recorded 08:00',size=25,fill='#64786f')+f.text(1230,890,'Recorded 10:00',size=25,fill='#64786f')
    progress=k(t,[(1.7,0),(2.35,1)])
    if t>1.5:
        # One history transition, then a fixed endpoint: deliberately not a live tracker.
        xx=610+620*progress;yy=770-55*math.sin(progress*math.pi)
        art+=group(sheep(0,0,t,.5,False),xx,yy)
        art+=f.path('M 610,810 L 1230,810',sw=2,stroke='#9caa93',extra='stroke-dasharray="7 12"')
    return art+'</g>'


def revelation(t,n):
    if .75<=t<4.05:
        return finish(fleet_map(t-.75),n)
    surprised=t>=4.05
    art=yard(t)+customer(t+5,surprised=surprised)+maker_with_tablet(t,tap=(.3<t<.65))
    if .3<t<.65:art+=f'<circle cx="874" cy="732" r="{12+(t-.3)*60}" fill="none" stroke="#17c8be" stroke-width="3"/>'
    return finish(art,n,(250,340,1200,675))


def ending(t,n):
    # Match the established logo/light finish; scenery remains a distant callback.
    art=f.sky()+'<g opacity=".4">'+group(MOUNTAIN,-240,210,.36)+'</g>'
    art+=f.washed('M -100,900 Q 700,760 1100,870 Q 1580,790 2050,860 L 2050,1200 L -100,1200 Z','#bdc6a6',sw=2,off=(4,2))
    art+=dumper(1370+t*100,855+5*math.sin(t*4),t,.32)
    xs=[600+i*90 for i in range(9)]
    wire='M 530,240 '+' '.join(f'Q {x-45},282 {x},258' for x in xs)+' Q 1390,282 1420,240'
    art+=f.path(wire,sw=3)
    for x in xs:art+=f.path(f'M {x},258 L {x},270',sw=3)+f.bulb(x,306,s=.32,b=.75,rot=180,rays=0)
    scale=1100/LOGO_W*k(t,[(0,.96),(.3,1)])
    art+=f'<g transform="translate({960-LOGO_W*scale/2},{470-LOGO_H*scale/2}) scale({scale})"><path d="{LOGO_D}" fill="#17c8be" fill-rule="evenodd" transform="translate(10,8)" filter="url(#wc)"/><path d="{LOGO_D}" fill="none" stroke="{INK}" stroke-width="9" stroke-linejoin="round" stroke-dasharray="420 16 260 12 340 14"/></g>'
    art+=f.text(960,650,'Rental IQ',size=62,fill='#315d5c',family='Georgia, serif',weight='normal')
    art+=f.text(960,749,'Know where every unit is. Every day.',size=48,family='Georgia, serif',weight='normal')
    return finish(art,n)


SHOTS=[dict(name='01-missing',dur=4,draw=missing),dict(name='02-excavator',dur=2,draw=abandoned),dict(name='03-crane',dur=2,draw=treed),dict(name='04-sheep-driver',dur=3,draw=sheep_driver),dict(name='05-binoculars',dur=5,draw=hero_arrives),dict(name='06-map',dur=5,draw=revelation),dict(name='07-ending',dur=4,draw=ending)]
DURATION=sum(s['dur'] for s in SHOTS)
def timeline():
    result=[];start=0
    for shot in SHOTS:result.append((start,shot));start+=shot['dur']
    return result,start
