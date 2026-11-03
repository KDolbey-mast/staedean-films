"""The Door performance edition: shot staging and one shared picture/sound clock.

Existing cast/props remain in staedean-cast/src. The approved Week 1 lives in
performance-test/scene.py. This file supplies the remaining acting and edit.
Each shot carries its duration and sound cues; build.py renders and mixes it.
"""
import os, sys, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'work/staedean-cast/src'),str(ROOT/'work/performance-test')]
os.environ['MS_STYLE']='marker'
import cast, film, film2 as f, scene as week1
from rb import wrap_rb
FPS=12
BASE={s['name']:s for s in f.SHOTS}

def k(t, points): return film.ramp(t,points)
def finish(art,n,view=None): return wrap_rb(art,view,film.boil(n))
def rest(): return [(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(200,190),(190,300),'rest',True)]
def pm(x,y,*,mood='hopeful',lean=0,tilt=0,arms=None,front='',look=None,scale=.42):
    face=dict(cast.PM_MOODS[mood]); face['eyes']='open'
    if look is not None: face['look']=look
    return cast.pm_full(x,y,scale,legs_mode='stand',lean=lean,head_rot=tilt,arms=arms or rest(),front=front,**face)
def gesture(y): return [(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(210,130),(265,y),'open',True)]

def office(t,n):
    # Replace abrupt head snaps with a glance, a worried hold, then recognition.
    view=k(t,[(0,film.AO.MED),(1.25,film.AO.MED),(2.15,(700,70,1300,731.25)),(3.15,f.DOOR_VIEW)])
    look=k(t,[(0,(.5,.9)),(.6,(.5,.9)),(.85,(.35,-1)),(1.4,(1,-.3))])
    tilt=k(t,[(0,6),(.6,6),(.8,-10),(1,-6),(1.7,3),(2.5,3),(3,-8),(3.4,-4)])
    brows='neutral' if t<.7 else 'raised' if t<1.6 else 'sad' if t<2.9 else 'raised' if t<3.4 else 'happy'
    mouth='neutral' if t<.7 else 'o' if t<1.6 else 'wobbly' if t<2.9 else 'o' if t<3.4 else 'grin'
    arms=[list(a) for a in f.A_WRITE]
    if t<.6:
        x,y=arms[1][2]; arms[1][2]=(x+9*math.sin(t*20),y+3*math.sin(t*40))
    extra=f.door(k(t,[(3.7,0),(4.2,1.06),(4.45,1)]))
    if t>=.6: extra+=f.bulb(*f.THOUGHT_BULB,s=k(t,[(.6,0),(.75,1.12),(.95,.95)]),b=.65,pop=t<1)
    art,_=f.story.office_frame(head_rot=tilt,look=look,brows=brows,mouth=mouth,arms=[tuple(a) for a in arms],pad='sketch1',bin_contents=('dead_bulb','paper'),extra=extra,view=view)
    return finish(art,n,view)

def arrival(t,n):
    # Distance drives leg phase, so easing into a stop does not cause foot skating.
    progress=k(t,[(0,0),(2.1,1)])
    x=230+430*progress; mx=120+400*k(t,[(.2,0),(2.25,1)])
    art=f.path_set()+f.parasol()+f.table()
    art+=cast.customer(f.CUST2_X,f.GROUND-16,pose='phone' if t<.75 else 'wave' if t<1.55 else 'down',mood='happy',look=(-1,0),blink=n==22)
    art+=f.maker(mx,f.GROUND+6,.42,phase=(mx-120)/34 if t<2.25 else None,
        arms=[(f.SHL,(-170,230),(-60,250),'cup'),(f.SHR,(180,230),(60,250),'cup',True)],front=f.proto(0,220,1),face=dict(look=(1,-.2),brows='happy',mouth='smile'))
    if t<2.1: art+=film.walker(x,f.GROUND+6,.42,(x-230)/34,b=.65,face=dict(look=(1,-.3),brows='happy',mouth='smile'))
    else: art+=cast.pm(x,f.GROUND+6,mood='hopeful',bulb=.65)
    return finish(art,n)

def visit_base(): return f.path_set()+f.parasol()+f.learned_bin(440,1)

def week2(t,n):
    # Three deliberate hammer strokes replace the perpetual two-pose flicker.
    hits=(1.75,2.25,2.75)
    wrist=-220
    for hit in hits:
        if hit-.3 <= t <= hit+.18:
            wrist=k(t,[(hit-.3,-220),(hit-.12,-300),(hit,-110),(hit+.18,-220)])
    hammer=f.path('M 0,0 L 0,-120',sw=9)+f.path('M 0,0 L 0,-120',sw=5,stroke='#b98a5e')+f.washed('M -40,-150 L 40,-150 L 40,-110 L -40,-110 Z','#8a8f90',sw=3,off=(1,1))
    working=1.35<t<3.1
    arms=[(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(230,120),(260,wrist),'fist',True)] if working else None
    # The tool and wrist share the same local coordinates in the Maker's rig.
    tool=f'<g transform="translate(260,{wrist}) rotate(180)">{hammer}</g>' if working else ''
    art=visit_base()
    art+=f.maker(f.MAKER_X,f.GROUND-40,.42,arms=arms,front=tool,lean=3 if working else 0,face=dict(look=(1,.6),brows='furrow' if working else 'happy',mouth='flat' if working else 'smile'))
    art+=f.table()+f.proto(f.TABLE_X,f.TABLE_TOP-6,2)
    art+=cast.customer(f.CUST2_X,f.GROUND-16,pose='point' if .5<t<1.45 else 'down',mood='puzzled' if t<3.2 else 'happy',look=(-1,.6),blink=n in (39,40))
    art+=pm(f.PM_X,f.GROUND+6,mood='thinking' if t<3.15 else 'hopeful',tilt=k(t,[(0,-5),(.7,5),(1,0),(3.15,0),(3.4,6),(3.65,0)]),look=(1,.2))
    if .5<t<1.3: art+=f.bubble(1130,380,240,100,(1280,490),lines=2,seed=4)
    art+=f.day_card(f.VISIT_VIEW,'WEEK 2',max(.2,t))
    return finish(art,n,f.VISIT_VIEW)

def week3(t,n):
    glow=k(t,[(0,.1),(.85,.15),(1.05,.9),(1.2,.65),(1.4,.95)])
    verdict=t>=1.75
    art=visit_base()
    # The Maker sees the device light up first; the PM waits for the buyer.
    maker_arms=gesture(k(t,[(2.1,280),(2.35,-35),(2.55,0),(2.85,20)])) if t>2.1 else None
    art+=f.maker(f.MAKER_X,f.GROUND-40,.42,arms=maker_arms,face=dict(look=(1,.2),brows='happy' if t>1.2 else 'raised',mouth='grin' if t>2.1 else 'smile'))
    art+=f.table()+f.proto(f.TABLE_X,f.TABLE_TOP-6,3,glow)
    art+=cast.customer(f.CUST2_X,f.GROUND-16,pose='thumbs_up' if verdict else 'down',mood='delighted' if verdict else 'puzzled',look=(-1,.4),blink=n in (15,16))
    art+=pm(f.PM_X,f.GROUND+6,mood='delighted' if t>2 else 'hopeful',tilt=k(t,[(0,-5),(1.7,-5),(2.05,6),(2.3,-3),(2.7,0)]),lean=k(t,[(0,3),(1.75,3),(2.1,-5),(2.5,0)]),arms=gesture(k(t,[(2,300),(2.3,30),(2.6,70)])) if t>2 else None)
    art+=f.day_card(f.VISIT_VIEW,'WEEK 3',max(.2,t))
    return finish(art,n,f.VISIT_VIEW)

def handshake(t,n):
    # Both hands share an exact contact point; the pumps decay into a firm hold.
    contact=.5
    bob=0 if t<contact else 10*math.exp(-1.8*(t-contact))*math.sin((t-contact)*math.pi*6)
    art=f.path_set()+f.parasol()
    # Existing customer hand is at (customer x - .52*290, feet - .52*490).
    customer_x=1300; customer_y=f.GROUND-16+bob
    art+=cast.customer(customer_x,customer_y,pose='shake' if t>=contact else 'down',mood='talking' if 1.8<t<2.8 else 'happy',look=(-1,0))
    px=1000; py=f.GROUND+6
    hx=(customer_x-.52*290-px)/.42
    hy=(customer_y-.52*490-py)/.42+700
    reach=k(t,[(0,0),(.5,1)])
    arms=[(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(230,140),(film.lerp(190,hx,reach),film.lerp(300,hy,reach)),'fist',True)]
    art+=pm(px,py,mood='delighted' if t>2.8 else 'hopeful',arms=arms,tilt=k(t,[(0,0),(1.8,0),(2.2,-5),(2.9,-5),(3.1,5),(3.4,0)]))
    if t>1.8: art+=f.bubble(940,420,420,130,(1250,390),words='When can I have it?',size=40)
    return finish(art,n,f.HAND_VIEW)

def catch(t,n):
    impact=.75
    bob=k(t,[(0,0),(impact,0),(impact+.12,20),(impact+.3,-5),(impact+.55,0)])
    art=f.path_set()+f.parasol()+f.table(cup=True)+f.learned_bin(440,1)
    if t<impact:
        art+=cast.customer(f.CUST2_X,f.GROUND-16,pose='wave',mood='puzzled',look=(0,-1),coffee=False)
        p=t/impact; target=f.GROUND-16-.52*470
        art+=f.product_box(f.CUST2_X,film.lerp(90,target,p*p),.52,rot=18*(1-p),glow=.35)
    else:
        art+=cast.customer(f.CUST2_X,f.GROUND-16+bob,pose='hold_box',mood='puzzled' if t<1.35 else 'delighted',look=(0,.8) if t<1.55 else (-1,0),box=True,box_glow=.35,coffee=False,blink=n in (13,14))
    return finish(art,n,(700,300,1100,618.75))

# The full-cast entrance is kept separate because it adapts the officials'
# counter-height puppets into full-body walkers.
import procession
how_we_work=procession.draw

# Piecewise-linear time maps create holds without changing the underlying art.
# The same inverse map retimes each sound cue, avoiding picture/sound drift.
def retimed(name, points):
    import numpy as np
    def draw(t,n):
        source=float(np.interp(t,[p[0] for p in points],[p[1] for p in points]))
        film.NOW=t
        return BASE[name]['draw'](source,round(source*FPS))
    cues=[]
    for cue in BASE[name]['cues']:
        at=float(np.interp(cue[0],[p[1] for p in points],[p[0] for p in points]))
        cues.append((at,*cue[1:]))
    return draw,cues

def cue(t,name,kwargs=None,gain=.3,bus='sfx'): return (t,name,kwargs or {},gain,bus)
def shot(name,duration,draw,cues): return dict(name=name,dur=round(duration*FPS)/FPS,draw=draw,cues=cues)
import launch_shot
launch,launch_cues=launch_shot.draw,launch_shot.CUES
shop,shop_cues=retimed('S1_now_open',[(0,0),(1.2,1),(2,1.6),(3.6,3.4),(5.8,5.8)])
end1,end1_cues=retimed('E1_still_die',[(0,0),(1.7,1.7),(2.3,2.2),(3.25,3)])
end2,end2_cues=retimed('E2_live_forever',[(0,0),(4,4)])
logo,logo_cues=retimed('E3_logo',[(0,0),(.6,.45),(3.5,3.4)])
SHOTS=[
 shot('O1_the_door',4.5,office,[cue(.2,'scribble',{'d':.4}),cue(.6,'pop'),cue(1.6,'tiny_dun',gain=.3,bus='music'),cue(2.9,'ding'),cue(3.7,'door_creak')]),
 shot('P1_twenty_metres',2.5,arrival,[cue(.1,'steps',{'d':2,'rate':2.5},.2)]),
 shot('V1_week1',9,week1.frame,[]),
 shot('V2_week2',4.25,week2,[cue(0,'flip'),cue(.5,'mumble',{'d':.7,'rate':3,'question':True},.25)]+[cue(t,'hammer',{'d':.15},.3) for t in (1.75,2.25,2.75)]),
 shot('V3_week3',3.75,week3,[cue(0,'flip'),cue(1,'chord_up',gain=.25,bus='music'),cue(1.75,'mumble',{'d':.4,'f0':170,'rate':4},.22)]),
 shot('H1_handshake',4,handshake,[cue(t,'pat',gain=.2) for t in (.5,.83,1.16)]+[cue(1.8,'mumble',{'d':1,'f0':150,'rate':4.5,'question':True},.3)]),
 shot('L1_over_the_mountain',launch_shot.DURATION,launch,launch_cues),
 shot('L2_got_it',2.5,catch,[cue(.75,'thump',gain=.35),cue(1.4,'ding',gain=.22)]),
 shot('S1_now_open',5.8,shop,shop_cues),
 shot('N1_how_we_work',procession.DURATION,how_we_work,[cue(.1,'steps',{'d':5.7,'rate':2.7},.15),cue(procession.SIGN_FLIP,'clack'),cue(procession.SIGN_FLIP+.2,'ding',gain=.2)]),
 shot('E1_still_die',3.25,end1,end1_cues),shot('E2_live_forever',4,end2,end2_cues),shot('E3_logo',3.5,logo,logo_cues)]

def timeline():
    result=[]; frame=0
    for s in SHOTS:
        result.append((frame/FPS,s)); frame+=round(s['dur']*FPS)
    return result,frame/FPS
