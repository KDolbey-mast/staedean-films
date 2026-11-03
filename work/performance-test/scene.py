"""A standalone Week 1 acting test. Reuses the existing puppets and scenery.

Flow: frame() stages the shot -> render_clip() makes 12 drawings/second ->
soundtrack() places cues on the same clock -> FFmpeg exports at 24 fps.
The original film scripts remain unchanged. Timing constants below are seconds.
"""
import os, sys, math, asyncio, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'work/staedean-cast/src'))
os.environ['MS_STYLE'] = 'marker'
import cast, film, film2 as f
from rb import wrap_rb
FPS = 12
DURATION = 9.0
REJECT, FIZZLE, WINDUP, RELEASE, LAND, NEW = 3.25, 4.0, 5.25, 5.75, 6.5, 7.25
VIEW = (300, 280, 1320, 742.5)
BROWSER = os.environ.get('ANIMATION_BROWSER', '/Users/ken/Library/Caches/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-mac-arm64/chrome-headless-shell')
OUT = ROOT / 'outputs'
WORK = pathlib.Path(__file__).parent

def key(t, points):
    return film.ramp(t, points)

def rotate(art, angle, x, y):
    return f'<g transform="rotate({angle:.3f},{x},{y})">{art}</g>'

def frame(t, n):
    film.NOW = t
    # The PM leads; the Maker reacts several drawings later, avoiding unison.
    pitch = .5 < t < 1.65
    mood = 'talking' if pitch else 'delighted' if t < REJECT+.25 else 'surprised' if t < 4.25 else 'sad' if t < 5 else 'thinking' if t < NEW else 'delighted'
    face = dict(cast.PM_MOODS[mood])
    if pitch: face['mouth'] = film.flap(n)
    if 4.25 < t < 5.0: face['look'] = (.8, .9)
    if 6.5 < t < 7.15: face['look'] = (-1, .5)
    # Only brief blinks: the reaction itself stays legible.
    if n in (24, 25, 61): face['eyes'] = 'closed_happy'
    lean = key(t, [(0,0),(.5,-3),(1,7),(1.65,2),(3.5,2),(3.75,-7),(4.5,6),(5,0),(WINDUP,0),(5.58,8),(RELEASE,-12),(6.1,-3),(7.25,0),(7.5,-4),(8,0)])
    tilt = key(t, [(0,-3),(1,4),(1.7,-5),(3.5,-5),(3.75,7),(4.5,12),(5.1,0),(7.2,-5),(7.5,-9),(8,0)])
    # Animate the existing bulb-holding arm in rig-local coordinates. The bulb
    # shares its wrist motion until release, then follows a continuous arc.
    wrist_y = key(t, [(0,110),(.6,70),(1.1,90),(3.5,90),(4.5,160),(WINDUP,160),(5.58,210),(RELEASE,20),(6.1,100),(NEW,110)])
    wrist_x = key(t, [(0,190),(WINDUP,190),(5.58,260),(RELEASE,-70),(6.1,100),(NEW,190)])
    bright = .85 if t < FIZZLE else ([.45,.05,.3,0][n%4] if t < 4.5 else 0)
    if t >= NEW: bright = key(t, [(NEW,.1),(NEW+.25,1),(8,.8)])
    held = t < RELEASE or t >= NEW
    arms = [(f.SHL,(-170,230),(-110,330),'rest'),(f.SHR,(190,190),(wrist_x,wrist_y),'cup',True)]
    front = f.bulb(wrist_x,wrist_y-52,s=1,b=bright,dead=bright==0,rays=7 if bright>.6 else 0) if held else ''
    art = f.path_set() + f.parasol()
    maker_mood = 'hopeful' if t < 3.8 else 'surprised' if t < 4.4 else 'thinking' if t < 7.6 else 'delighted'
    maker = cast.maker(f.MAKER_X, f.GROUND-40, mood=maker_mood)
    art += rotate(maker, key(t,[(0,0),(1.2,-2),(2,0),(3.8,0),(4.1,3),(4.5,0),(7.6,0),(7.85,-3),(8.2,0)]),f.MAKER_X,f.GROUND-40)
    art += f.table() + f.proto(f.TABLE_X, f.TABLE_TOP-6, 1)
    # The customer looks at the box, then the seller, then gives one clear verdict.
    pose = 'phone' if t < 1.75 else 'down' if t < REJECT else 'thumbs_down' if t < 4.9 else 'down'
    customer = cast.customer(f.CUST2_X, f.GROUND-16, pose=pose,
        mood='puzzled' if 2.25 < t < 4.9 else 'happy' if t > 7.8 else 'neutral',
        look=(-1,.8 if t < 2.7 else -.1), blink=n in (29,30,58))
    customer = rotate(customer,key(t,[(0,0),(2,0),(2.5,-3),(3,-3),(REJECT,0),(7.8,0),(8,1),(8.3,0)]),f.CUST2_X,f.GROUND-16)
    art += customer
    # Access the original articulated puppet through cast; no new character artwork.
    art += cast.pm_full(f.PM_X,f.GROUND+6,.42,legs_mode='stand',arms=arms,front=front,lean=lean,head_rot=tilt,**face)
    if pitch:
        art += f.bubble(780,390,255,105,(760,550),lines=2,seed=3)
    if RELEASE <= t < LAND:
        p=(t-RELEASE)/(LAND-RELEASE)
        x0=f.PM_X+.42*(-70); y0=f.GROUND+6-.42*(700+32)
        x1,y1=440,f.GROUND-150
        x=(1-p)**2*x0+2*(1-p)*p*520+p*p*x1
        y=(1-p)**2*y0+2*(1-p)*p*(y0-210)+p*p*y1
        art += rotate(cast.idea(x,y,.45,brightness=0,dead=True),-240*p,x,y)
    # Draw bin last to occlude the falling bulb at its rim. Its small impact
    # wobble settles rather than vibrating indefinitely.
    wobble = 5*math.exp(-8*(t-LAND))*math.sin(26*(t-LAND)) if t >= LAND else 0
    art += rotate(f.learned_bin(440,1 if t>=LAND else 0),wobble,440,f.GROUND)
    art += f.day_card(VIEW,'WEEK 1',max(.2,t))
    # A brief reaction insert gives the customer a readable silent assessment.
    # Include the entire downward thumb, and hold the verdict for eight drawings.
    view = (1020,350,600,337.5) if 2.25 <= t < 3.92 else VIEW
    return wrap_rb(art, view, film.boil(n))

async def render_clip(name, draw, duration):
    from playwright.async_api import async_playwright
    folder=WORK/name; folder.mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=BROWSER)
        queue=asyncio.Queue()
        for n in range(round(duration*FPS)): queue.put_nowait(n)
        async def worker():
            page=await browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
            while not queue.empty():
                n=queue.get_nowait(); svg=draw(n/FPS,n)
                await page.set_content('<html><style>body{margin:0}svg{width:1280px;height:720px}</style><body>'+svg+'</body></html>')
                await page.screenshot(path=str(folder/f'{n:04d}.png'))
                if n%24==0: print(name,n,flush=True)
            await page.close()
        await asyncio.gather(*[worker() for _ in range(3)])
        await browser.close()
    return folder

def soundtrack():
    import numpy as np
    import sfx
    from scipy.io import wavfile
    audio=np.zeros(round(DURATION*sfx.SR))
    def cue(at, samples, gain):
        start=round(at*sfx.SR); count=min(len(samples),len(audio)-start)
        audio[start:start+count] += samples[:count]*gain
    cue(.1,sfx.flutter(.18),.15)
    cue(.5,sfx.mumble(.95,165,7),.23)
    # Silence under the customer close-up is intentional: let the look work.
    cue(REJECT,sfx.mumble(.28,125,2),.17)
    cue(FIZZLE,sfx.fizzle(.5),.28)
    cue(RELEASE,sfx.whoosh(.65),.18)
    cue(LAND,sfx.clang(),.23)
    cue(NEW,sfx.bell(sfx.midi(84),1.3),.23)
    cue(7.55,sfx.pluck(sfx.midi(72),.6),.13)
    cue(7.85,sfx.pluck(sfx.midi(76),.6),.13)
    cue(8.15,sfx.pluck(sfx.midi(79),.7),.13)
    audio=np.clip(audio,-.95,.95)
    path=WORK/'performance.wav'; wavfile.write(str(path),sfx.SR,(audio*32767).astype(np.int16))
    return path

def encode(folder, target, sound=None):
    import imageio_ffmpeg
    args=[imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.png')]
    if sound: args += ['-i',str(sound),'-c:a','aac','-b:a','160k']
    args += ['-vf','fps=24,format=yuv420p','-c:v','libx264','-crf','18','-movflags','+faststart',str(target)]
    subprocess.run(args,check=True)

if __name__=='__main__':
    OUT.mkdir(exist_ok=True)
    folder=asyncio.run(render_clip('polished',frame,DURATION))
    encode(folder,OUT/'the-door-performance-test.mp4',soundtrack())
    original=next(s for s in f.SHOTS if s['name']=='V1_week1')
    def baseline(t,n):
        film.NOW=t
        return original['draw'](t,n)
    folder=asyncio.run(render_clip('original',baseline,original['dur']))
    encode(folder,OUT/'the-door-original-scene.mp4')
    print('Finished both clips',flush=True)
