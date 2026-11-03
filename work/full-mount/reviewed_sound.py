"""Mix against the actual edit: cue-locked effects, continuous wind and music.

The first office/reveal/reaction block is copied sample-for-sample from the
approved cut. This protects the mountain reaction, not just its cue name.
"""
import json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d
import film_sound as sound

SR = sound.SR


def release(signal, fade=.08):
    signal = np.array(signal, dtype=float, copy=True)
    n = min(len(signal)//2, round(fade*SR))
    if n:
        signal[:min(n,220)] *= np.linspace(0,1,min(n,220))
        signal[-n:] *= np.linspace(1,0,n)
    return signal


def mix(timeline, total, work, previous_audio):
    buses = {k:np.zeros(round((total+5)*SR)) for k in ('music','sfx','amb')}
    events=[]
    def add(at, signal, gain, bus, label):
        data=np.asarray(signal)*gain
        offset=round(at*SR)
        if offset<0: data=data[-offset:];offset=0
        count=min(len(data),len(buses[bus])-offset)
        if count>0: buses[bus][offset:offset+count]+=data[:count]
        events.append(dict(name=label,start=at,duration=len(data)/SR,bus=bus))
    starts={shot['source_name']:at for at,shot in timeline}
    protected_end=starts['B2_off_he_goes']
    sound.rng.bit_generator.state=np.random.default_rng(7).bit_generator.state
    for start,shot in timeline:
        if start < protected_end: continue
        trim=shot['source_first']/12
        duration=shot['dur']
        for cue_at,name,kwargs,*options in shot['cues']:
            fn,gain,bus=sound.FUN[name]
            gain=options[0] if options else gain
            bus=options[1] if len(options)>1 else bus
            # These beds are generated once over the edited sequence below.
            if bus=='amb' or name in ('march','plod'): continue
            at=cue_at-trim
            if at>=duration:continue
            signal=np.asarray(fn(**kwargs))
            if at<0:
                signal=signal[round(-at*SR):];at=0
            if not len(signal):continue
            # Visible speech/movement stops with its shot. Musical and impact
            # tails may cross a cut, preventing chopped notes and resonances.
            if name in ('mumble','steps','shuffle','taps','ticking','printer','hiss'):
                signal=signal[:max(0,round((duration-at)*SR))]
                signal=release(signal,.06)
            else:
                signal=release(signal,.12 if bus=='music' else .035)
            # Keep the emotional question/silence clear of the hopeful phrase.
            if name=='musicbox_hope':
                signal=release(signal[:round((starts['G3_who_are_you']-start-at)*SR)],.25)
            add(start+at,signal,gain,bus,name)
    # A single wind bed avoids random-noise restarts at each camera cut.
    wind_start=protected_end; summit=starts['G1_the_summit']
    length=summit-wind_start+.35
    wind=np.asarray(sound.wind(length,1.0))[:round(length*SR)]
    time=np.arange(len(wind))/SR+wind_start
    knots=[wind_start,starts['D1_upwards'],starts['E1_the_fork'],starts['F1_thin_air'],summit-.18,summit+.35]
    levels=[.055,.075,.10,.27,.27,0]
    wind*=np.interp(time,knots,levels)
    add(wind_start,release(wind,.35),1,'amb','continuous_mountain_wind')
    calm=release(sound.FUN['calm'][0](d=total-summit),.6)
    add(summit,calm,.04,'amb','summit_calm')
    march_end=starts['C2_the_pitch']
    add(wind_start,release(sound.FUN['march'][0](d=march_end-wind_start,start=0),.35),.3,'music','continuous_departure_march')
    # Keep the plodding motif in travelling shots, with its decay over the cut.
    for name in ('D1_upwards','E1_the_fork'):
        entry=next(s for at,s in timeline if s['source_name']==name)
        add(starts[name],release(sound.plod(entry['dur']+.3,start=0),.4),.18,'music','plod_'+name)
    fx=buses['sfx'];env=uniform_filter1d(np.abs(fx),size=4410)
    music=buses['music']*(1-.3*np.clip(env/(env.max() or 1)*4,0,1))
    mixed=np.tanh((music+fx+buses['amb'])*1.1)[:round(total*SR)]
    mixed*=.9/max(.9,float(np.max(np.abs(mixed))))
    rate,original=wavfile.read(previous_audio);assert rate==SR
    protected_samples=round(protected_end*SR)
    original=original.astype(float)/32767
    mixed[:protected_samples]=original[:protected_samples]
    # Continue the outgoing original ambience briefly into the new bed.
    overlap=round(.25*SR);weight=np.linspace(0,1,overlap)
    mixed[protected_samples:protected_samples+overlap]=(original[protected_samples:protected_samples+overlap]*(1-weight)+mixed[protected_samples:protected_samples+overlap]*weight)
    tail=round(1.3*SR);mixed[-tail:]*=np.linspace(1,0,tail)**1.5
    pcm=np.rint(mixed*32767).astype(np.int16)
    _,old_pcm=wavfile.read(previous_audio)
    assert np.array_equal(pcm[:protected_samples],old_pcm[:protected_samples]),'Protected mountain reaction changed'
    target=work/'reviewed-soundtrack.wav';wavfile.write(target,SR,pcm)
    (work/'sound-cues.json').write_text(json.dumps(dict(protected_through=protected_end,protected_samples_equal=True,peak=float(np.max(np.abs(mixed))),events=events),indent=2))
    return target
