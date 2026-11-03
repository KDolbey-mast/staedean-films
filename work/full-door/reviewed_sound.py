"""The Door sound pass: preserve Week 1, map repeating cues to visible frames,
and give transitions release tails without moving picture cuts.
"""
import math,json
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d
import film2_sound as sound
import procession
SR=sound.SR
SHOP_MAP=[(0,0),(1.2,1),(2,1.6),(3.6,3.4),(5.8,5.8)]


def soften(signal, fade=.12, attack=.008):
    signal=np.asarray(signal,dtype=float).copy()
    a=min(len(signal)//2,round(attack*SR));b=min(len(signal)//2,round(fade*SR))
    if a:signal[:a]*=np.linspace(0,1,a)
    if b:signal[-b:]*=np.linspace(1,0,b)
    return signal


def mix(d,work,previous):
    timeline,total=d.timeline();starts={s['name']:at for at,s in timeline}
    buses={key:np.zeros(round((total+8)*SR)) for key in ('music','sfx','amb')};events=[]
    def add(at,signal,gain=.3,bus='sfx',name=''):
        data=np.asarray(signal)*gain;first=round(at*SR);count=min(len(data),len(buses[bus])-first)
        if count>0:buses[bus][first:first+count]+=data[:count]
        events.append(dict(name=name,time=at,duration=len(data)/SR,bus=bus))
    sound.rng.bit_generator.state=np.random.default_rng(7).bit_generator.state
    for start,shot in timeline:
        for at,name,kwargs,*options in shot['cues']:
            if name in ('theme2','theme2_out','bridge_pad','wind','ding_run','shutter'):continue
            if shot['name']=='S1_now_open' and name=='ching':continue
            if shot['name']=='N1_how_we_work' and name=='steps':continue
            fn,gain,bus=sound.FUN[name];kwargs=dict(kwargs)
            gain=options[0] if options else gain;bus=options[1] if len(options)>1 else bus
            if shot['name']=='L1_over_the_mountain' and name=='whoosh':
                kwargs['d']=shot['dur']-at+.75 # carry the parcel sound to the catch
            signal=fn(**kwargs)
            if name=='crowd':signal=soften(signal,.35,.08)
            elif name=='whoosh':signal=soften(signal,.12)
            elif bus=='music':signal=soften(signal,.18)
            add(start+at,signal,gain,bus,name)
    # Opening music resolves into the outside shot instead of cutting mid-note.
    add(0,soften(sound.office_music(4.5),.3),.14,'music','office_theme')
    add(starts['P1_twenty_metres'],sound.fade(sound.theme2(2.5),.1,.4),.17,'music','arrival_theme')
    start=starts['V2_week2'];end=starts['L1_over_the_mountain']
    add(start,sound.fade(sound.theme2(end-start),.15,.7),.16,'music','development_theme')
    start=starts['S1_now_open'];end=starts['E1_still_die']
    add(start,sound.theme2_out(end-start,fade=2.5),.17,'music','shop_to_door_theme')
    start=starts['N1_how_we_work']+2.7
    add(start,sound.bridge_pad(total-start),.13,'music','ending_bridge')
    # Low continuous exterior ambience across launch and catch; fade before shop.
    start=starts['V2_week2'];end=starts['S1_now_open']
    add(start,soften(sound.wind(end-start,.2),.4,.4),.025,'amb','continuous_exterior')
    add(starts['N1_how_we_work'],soften(sound.room_tone(6.25),.3,.3),.025,'amb','door_room')
    # The shop was retimed nonlinearly. Schedule its counter sounds from the
    # actual displayed number on each drawing, rather than a fixed-rate loop.
    shop=next(s for s in d.SHOTS if s['name']=='S1_now_open')
    previous_number=100;delivery=None;open_at=None
    for n in range(round(shop['dur']*12)):
        t=n/12;source=float(np.interp(t,[p[0] for p in SHOP_MAP],[p[1] for p in SHOP_MAP]))
        if source>=1 and open_at is None:open_at=t
        if source>=3.4 and delivery is None:delivery=t
        number=101+max(0,int((source-1.2)/.3)) if source>1.2 else 100
        if number!=previous_number:
            add(starts['S1_now_open']+t,sound.bell(sound.midi(84 if number%2 else 88),.5),.1,name='serving_'+str(number))
        previous_number=number
    add(starts['S1_now_open'],soften(sound.shutter(open_at),.08),.4,name='shutter')
    add(starts['S1_now_open']+delivery,sound.ching(),.4,name='parcel_handover')
    # Each walker gets quieter individual contacts, tied to the leg phase.
    # A foot plants when its cosine crosses into the grounded half-cycle.
    for role,profile in procession.PROFILES.items():
        start,travel,step_length,stride,swing,offset,tilt=profile
        last=None
        for n in range(round(procession.DURATION*12)):
            t=n/12;u=(t-start)/travel
            if not 0<u<1:continue
            distance=840*(u-.025*math.sin(2*math.pi*u))
            phase=distance/step_length+offset
            contact=math.floor((phase-math.pi/2)/math.pi)
            if last is not None and contact>last:
                add(starts['N1_how_we_work']+t,sound.footsteps(.2,rate=1),.045,name='foot_'+role)
            last=contact
    fx=buses['sfx'];env=uniform_filter1d(np.abs(fx),size=4410)
    music=buses['music']*(1-.3*np.clip(env/(env.max() or 1)*4,0,1))
    audio=np.tanh((music+fx+buses['amb'])*1.1)[:round(total*SR)]
    audio*=.9/max(.9,float(np.max(np.abs(audio))))
    # The accepted Week 1 silent assessment, thumb verdict and comic sounds
    # are preserved from the final previous mix, not regenerated approximations.
    rate,original=wavfile.read(previous);assert rate==SR
    first=round(starts['V1_week1']*SR);end=round(starts['V2_week2']*SR)
    audio[first:end]=original[first:end].astype(float)/32767
    blend=round(.08*SR);weight=np.linspace(0,1,blend)
    audio[first-blend:first]=audio[first-blend:first]*(1-weight)+original[first-blend:first]/32767*weight
    tail=round(1.3*SR);audio[-tail:]*=np.linspace(1,0,tail)**1.5
    pcm=np.rint(audio*32767).astype(np.int16)
    assert np.array_equal(pcm[first:end],original[first:end])
    path=work/'soundtrack.wav';wavfile.write(path,SR,pcm)
    (work/'sound-review.json').write_text(json.dumps(dict(week1_samples_identical=True,peak=float(np.max(np.abs(audio))),events=events),indent=2))
    return path
