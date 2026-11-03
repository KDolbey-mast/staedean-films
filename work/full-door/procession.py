"""Individual walking performances for the established cast.

Profiles vary pace, step length, arm swing and head movement. Leg phase follows
travelled distance, so changing speed does not leave feet cycling in place.
"""
import math
import film,film2 as f,cast,props
from rb import wrap_rb
CAST_ORDER=('pm','qa','maker','customer success','product owner','planning','customer')
DURATION=6.25
SIGN_FLIP=4.6
# start, travel seconds, distance per phase-radian, leg reach, arm swing,
# phase offset, head tilt amplitude. Small differences preserve queue order.
PROFILES={
 'pm':(.05,2.70,37,.85,.65,.2,2.0),
 'qa':(.60,2.85,31,.62,.60,1.5,1.5),
 'maker':(1.15,2.70,40,.92,1.05,2.8,2.5),
 'customer success':(1.70,2.80,34,.76,.85,.8,2.0),
 'product owner':(2.25,2.80,36,.80,.70,2.1,1.8),
 'planning':(2.80,2.90,32,.65,.45,3.7,1.2),
 'customer':(3.35,2.65,39,.82,.55,1.1,1.3),
}

def official_walking(role,x,y,phase,stride,swing,tilt,look):
    scale=.48
    # A light upper-body rise, with feet retaining their world-space ground line.
    hip_y=y-370*scale
    legs=f.legs(film.walk_legs(phase,stride,lift=22))
    lower=f'<g transform="translate({x},{hip_y}) scale({scale}) translate(0,-330)">{legs}</g>'
    bob=1.5*math.cos(2*phase)
    upper=props.official(x,hip_y+bob,scale,cast.OFFICIALS[role],arm='walk',mouth='smile',look=look,
        walk_phase=phase,swing=swing,head_tilt=tilt,carry_idea=True)
    return lower+upper

def customer_walking(x,y,phase,stride,swing,tilt,look):
    scale=.44
    upper=props.customer(0,0,1,pose='walk',mouth='smile',look=look,coffee=True,
        walk_phase=phase,swing=swing,head_tilt=tilt,carry_idea=True)
    lower=f.legs(film.walk_legs(phase,stride,lift=20)).replace('#3a3a40','#323a48')
    return (f'<g transform="translate({x},{y}) scale({scale})">'
        +'<defs><clipPath id="customer-upper-only"><rect x="-400" y="-1200" width="800" height="850"/></clipPath></defs>'
        +f'<g transform="translate(0,-700) scale(.65,1)">{lower}</g>'
        +f'<g clip-path="url(#customer-upper-only)">{upper}</g></g>')

def hero_walking(role,x,y,phase,stride,swing,tilt,look):
    motion=math.sin(phase)*swing
    free=(f.SHL,(-185-28*motion,200),(-150-75*motion,310-18*abs(motion)),'rest')
    if role=='pm':
        # Keep the live idea steady; only the free arm swings broadly.
        arms=[free,(f.SHR,(200,190),(190,110),'cup',True)]
        front=f.bulb(190,58,s=1,b=.7,rays=7)
        return cast.pm_full(x,y,.42,legs_mode=film.walk_legs(phase,stride,lift=24),
            arms=arms,front=front,lean=1.5*math.sin(phase),head_rot=tilt,look=look,brows='happy',mouth='smile')
    arms=[free,(f.SHR,(200,190),(190,110),'cup',True)]
    # Maker uses the same established hat and palette, with a looser two-arm gait.
    return f.maker(x,y,.42,arms=arms,front=f.bulb(190,58,s=1,b=.7,rays=7),legs=film.walk_legs(phase,stride,lift=28),lean=2.5*math.sin(phase),
        face=dict(look=look,brows='happy',mouth='smile',head_rot=tilt))

def draw(t,n):
    # Keep the original sign visible. Cross it out, then add the new plaque.
    # The old flip clock remains the sound/edit anchor, but neither sign flips.
    art=f.office_no_pm(door_open=1,sign='INNOVATION',sub='',flip=1)
    centre=f.DOOR_X+f.DOOR_W/2
    if t >= SIGN_FLIP-.2:
        first=film.ramp(t,[(SIGN_FLIP-.2,0),(SIGN_FLIP,1)])
        second=film.ramp(t,[(SIGN_FLIP,0),(SIGN_FLIP+.2,1)])
        for x0,y0,x1,y1,u in [(-140,177,140,240,first),(-140,240,140,177,second)]:
            if u>0:
                art+=f.path(f'M {centre+x0},{y0} L {centre+x0+(x1-x0)*u},{y0+(y1-y0)*u}',sw=12,stroke='#c43f37')
    reveal=film.ramp(t,[(SIGN_FLIP,0),(SIGN_FLIP+.2,1)])
    if reveal>0:
        plaque=(f.washed('M -170,-30 L 170,-30 L 170,30 L -170,30 Z','#fbf7ee',off=(2,2))
                +f.text(0,12,'HOW WE WORK',size=34,spacing=1))
        art+=f'<g opacity="{reveal:.3f}" transform="translate({centre},285)">{plaque}</g>'
    art+='<defs><clipPath id="whole-cast-door"><rect x="900" y="0" width="1090" height="1200"/></clipPath></defs>'
    for role in CAST_ORDER:
        start,travel,step_length,stride,swing,offset,tilt_amount=PROFILES[role]
        u=(t-start)/travel
        if not 0<u<1:continue
        # Mild acceleration/deceleration avoids a mechanical conveyor-belt pace.
        progress=u-.025*math.sin(2*math.pi*u)
        distance=840*progress;x=1250+distance;phase=distance/step_length+offset
        tilt=tilt_amount*math.sin(phase*.5)+1.2*math.sin(u*math.pi)
        # Brief glances toward the person ahead, then toward the open doorway.
        look=(.85 if u>.6 else .45+.25*math.sin(u*math.pi*2+offset),-.1)
        if role in ('pm','maker'):person=hero_walking(role,x,f.GROUND+6,phase,stride,swing,tilt,look)
        elif role=='customer':person=customer_walking(x,f.GROUND+6,phase,stride,swing,tilt,look)
        else:person=official_walking(role,x,f.GROUND+6,phase,stride,swing,tilt,look)
        art+='<g clip-path="url(#whole-cast-door)">'+person+'</g>'
    return wrap_rb(art,(950,100,1500,843.75),film.boil(n))
