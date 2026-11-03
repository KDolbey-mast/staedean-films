"""The Priority: preserve the approved fifteen seconds, add an awkward desk hold."""
import importlib.util,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('foreground_cut',ROOT/'work/the-priority-foreground/director.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
original=previous.original
f,film,cast,props,rb=previous.f,previous.film,previous.cast,previous.props,previous.rb
FPS=12;BROWSER=previous.BROWSER;DURATION=19.5;CUT=15
k=film.ramp


def glance(t,index):
    """Stagger eye movements, then hold, so this reads as exchanged looks."""
    start=.55+index*.29
    direction=1 if index%2==0 else -1
    gx=k(t,[(0,0),(start,0),(start+.18,direction*1.5),
            (start+.7,direction*1.5),(start+.9,-direction*1.5),
            (3.55,-direction*1.5),(3.8,0)])
    gy=k(t,[(0,.2),(3.5,.2),(3.85,.9)])
    return gx,gy


def reaction(t,n):
    film.NOW=15+t
    art=original.setting()
    art+='<defs><radialGradient id="priority-glow"><stop stop-color="#ffe998" stop-opacity=".5"/><stop offset="1" stop-color="#fff5c0" stop-opacity="0"/></radialGradient></defs>'
    # Same positions as the original desk shot: the cut changes attention only.
    for i,item in enumerate(original.ARRIVALS):
        x=item['x'];look=glance(t,i+1)
        tilt=look[0]*2
        embarrassed=t>.25+i*.23
        if item['role']=='maker':
            art+=f.maker(x,930,.52,face=dict(look=look,brows='quizzical' if embarrassed else 'happy',
                mouth='flat' if embarrassed else 'smile',head_rot=tilt,
                eyes='closed' if 2.7<t<2.85 else 'open'))
        else:
            scale=.60;hip=930-370*scale
            art+=f'<g transform="translate({x},{hip}) scale({scale}) translate(0,-330)">'+f.legs('stand')+'</g>'
            art+=props.official(x,hip,scale,cast.OFFICIALS[item['role']],
                look=look,head_tilt=tilt,brows='puzzled' if embarrassed else 'neutral',
                mouth='flat' if embarrassed else 'smile')
    # PM lowers the glasses enough to show his eyes. The prop remains in hand.
    hand_up=k(t,[(0,0),(.3,1)])
    lowered=k(t,[(.3,0),(.85,1)])
    gy=-134+62*lowered
    grip=(150+(100-150)*hand_up,320+(gy+2-320)*hand_up)
    arms=[(f.SHL,(-170,210),(-140,320),'rest'),(f.SHR,(215,100),grip,'fist',True)]
    art+=cast.pm_full(520,930,.62,arms=arms,front=original.sunglasses(34,gy),
        look=glance(t,0),brows='raised',mouth='flat',eyes='open')
    art+=original.pedestal()
    art+=original.idea(800,original.BULB_Y,11.8)
    for item in original.ARRIVALS:
        y=original.BULB_Y+(8 if item['habit']=='nudge' else 0)
        art+=original.idea(item['bulb'],y,11.8)
    # Expose for their faces in this reaction shot; keep the hot bulbs visible.
    art+=previous.glare(11.8,strength_scale=.18)
    return rb.wrap_rb(art,(340,300,1280,720),film.boil(n))

SHOTS=previous.SHOTS+[dict(name='reaction',dur=4.5,draw=reaction,cues=[])]
def timeline():return [(0,SHOTS[0]),(11,SHOTS[1]),(15,SHOTS[2])],DURATION
