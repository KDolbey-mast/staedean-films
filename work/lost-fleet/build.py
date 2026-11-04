"""Render, mix, and verify The Lost Fleet. Run from any directory.

--proof renders a contact sheet before the expensive full render.
--render builds cached shot frames and the finished MP4. Delete a shot's frame
folder after changing its drawing; cached frames deliberately are not overwritten.
"""
import asyncio, argparse, pathlib, json, subprocess, sys
import director as d
import numpy as np
from PIL import Image,ImageDraw
from scipy.io import wavfile
from scipy.ndimage import uniform_filter1d
from playwright.async_api import async_playwright
import imageio_ffmpeg
import film_sound as sound
ROOT=d.ROOT; WORK=pathlib.Path(__file__).parent; OUT=ROOT/'outputs'
WIDTH,HEIGHT=1920,1080

async def render(proof=False):
    jobs=[]
    for start,shot in d.timeline()[0]:
        folder=WORK/'frames'/shot['name'];folder.mkdir(parents=True,exist_ok=True)
        count=round(shot['dur']*d.FPS)
        indices=sorted(set([0,count//3,2*count//3,count-1])) if proof else range(count)
        for n in indices:
            target=folder/f'{n:04d}.png'
            if not target.exists(): jobs.append((shot,n,target))
    print('Render jobs:',len(jobs),flush=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.BROWSER)
        queue=asyncio.Queue()
        for item in jobs:queue.put_nowait(item)
        done=0
        async def worker():
            nonlocal done
            page=await browser.new_page(viewport={'width':WIDTH,'height':HEIGHT})
            while not queue.empty():
                shot,n,target=queue.get_nowait()
                # Drawing is synchronous; global legacy rig time cannot interleave.
                d.film.NOW=n/d.FPS
                svg=shot['draw'](n/d.FPS,n)
                await page.set_content(f'<style>body{{margin:0}}svg{{width:{WIDTH}px;height:{HEIGHT}px}}</style>'+svg)
                await page.screenshot(path=str(target));done+=1
                if done%36==0:print('Rendered',done,'/',len(jobs),shot['name'],flush=True)
            await page.close()
        await asyncio.gather(*[worker() for _ in range(3)])
        await browser.close()
    if proof:
        shots=d.SHOTS
        sheet=Image.new('RGB',(960,len(shots)*155),'#f5f0e7');draw=ImageDraw.Draw(sheet)
        for row,s in enumerate(shots):
            count=round(s['dur']*d.FPS)
            for col,n in enumerate([count//3,2*count//3,count-1]):
                im=Image.open(WORK/'frames'/s['name']/f'{n:04d}.png');im.thumbnail((320,135))
                sheet.paste(im,(col*320,row*155));draw.text((col*320+5,row*155+136),f"{s['name']} {n/d.FPS:.2f}s",fill='black')
        sheet.save(WORK/'proof.jpg')

def sheep_bleat(duration=.95):
    """A cartoon BAAAA made from a quavering voiced source and vowel resonances."""
    t=sound.tt(duration)
    pitch=205-40*t/duration+18*np.sin(2*np.pi*10*t)*np.minimum(1,t/.13)
    phase=2*np.pi*np.cumsum(pitch)/sound.SR
    voice=sum(np.sin(phase*i)/i for i in range(1,17))
    vowel=sound.bp(voice,550,950)+.75*sound.bp(voice,1100,1800)+.2*sound.bp(voice,2400,3300)
    pulse=.72+.28*np.sin(2*np.pi*10*t)
    return sound.norm(sound.fade(vowel*pulse,.055,.14),.85)


def engine(duration):
    t=sound.tt(duration)
    return sound.fade((np.sin(2*np.pi*58*t)+.4*np.sin(2*np.pi*116*t))*(.5+.5*np.sin(2*np.pi*8*t)**6),.1,.15)


def soundtrack():
    sr=sound.SR;audio=np.zeros(round(d.DURATION*sr))
    sound.rng.bit_generator.state=np.random.default_rng(87).bit_generator.state
    def add(at,signal,gain):
        start=round(at*sr);count=min(len(signal),len(audio)-start)
        audio[start:start+count]+=np.asarray(signal[:count])*gain
    add(0,sound.theme_player(3.7,78),.04)
    add(1,sound.whoosh(2.7,350,1700),.025)
    add(2,sound.flutter(.6),.035)
    for at,note in ((4,43),(6,46),(8,50)):
        add(at,sound.brass_hit(note,1.55),.14);add(at,sound.timpani(65,1.1),.08)
    add(6.15,sound.creak(1.2),.13)
    add(8,engine(1.8),.045)
    add(8,sound.swell([50,57,62,65],1.8),.12)
    # All dramatic music ends at the visual sheep reveal. Leave the bleat exposed.
    add(9.8,sheep_bleat(),.32)
    for at in (11.05,11.25,11.45):add(at,sound.flop(),.055)
    add(12.2,sound.whoosh(.35),.055);add(12.7,sound.whoosh(.35),.055)
    add(14.15,sound.flop(),.075)
    add(14.8,sound.pop(),.045)
    add(16.4,sound.bell(1100,.3),.1)
    for at,note in ((17.1,60),(17.45,64),(17.8,67)):
        add(at,sound.bell(sound.midi(note),1.0),.11)
    add(18.45,sound.pop(),.035)
    add(19,sound.swell([48,55,60,64,67],3),.13)
    add(20.1,sound.bell(784,1),.08)
    add(21,sound.theme_player(3.9,106),.085)
    add(21,sound.chord_voices([48,55,60,64],3.8,attack=.08,release=1.2,kind='brass'),.075)
    add(21.8,engine(2.6),.018)
    add(23.2,sound.bell(1046,1.5),.06)
    audio=np.tanh(audio*1.5);audio[-17640:]*=np.linspace(1,0,17640)
    path=WORK/'soundtrack.wav';wavfile.write(path,sr,np.rint(audio*32767).astype(np.int16))
    print('Soundtrack peak:',round(float(np.max(np.abs(audio))),3),flush=True)
    return path

def encode(audio, output_name="The-Lost-Fleet-v1.mp4", sequence_name="sequence"):
    # Concatenate frame sequences numerically on disk, preserving shot boundaries.
    import os
    folder=WORK/sequence_name;folder.mkdir(exist_ok=True);index=0
    manifest=[]
    for start,s in d.timeline()[0]:
        count=round(s['dur']*d.FPS)
        manifest.append({'shot':s['name'],'start':start,'duration':count/d.FPS,'frames':count})
        for n in range(count):
            source=WORK/'frames'/s['name']/f'{n:04d}.png';assert source.exists(),source
            target=folder/f'{index:05d}.png'
            if not target.exists():os.link(source,target)
            index+=1
    target=OUT/output_name
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-framerate','12','-i',str(folder/'%05d.png'),'-i',str(audio),'-vf','fps=24,format=yuv420p','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(target)],check=True)
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(target),'-f','null','-'],check=True)
    (WORK/'timeline.json').write_text(json.dumps(manifest,indent=2))
    print('Verified output:',target,flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--proof',action='store_true');parser.add_argument('--render',action='store_true');args=parser.parse_args()
    if not (args.proof or args.render):parser.error('Choose --proof or --render')
    OUT.mkdir(exist_ok=True)
    asyncio.run(render(proof=args.proof))
    if args.render:encode(soundtrack())
