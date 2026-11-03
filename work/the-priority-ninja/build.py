"""Render, mix, and verify the performance edition. Run from any directory.

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

def soundtrack():
    # Preserve every approved cue before the cut, then land a very small payoff.
    sr,previous=wavfile.read(ROOT/'work/the-priority/soundtrack.wav')
    audio=np.zeros(round(d.DURATION*sr))
    audio[:round(d.CUT*sr)]=previous[:round(d.CUT*sr)]/32767
    sound.rng.bit_generator.state=np.random.default_rng(33).bit_generator.state
    def add(at,signal,gain):
        start=round(at*sr);count=min(len(signal),len(audio)-start)
        audio[start:start+count]+=np.asarray(signal[:count])*gain
    add(11.03,sound.whoosh(.45),.07)
    add(12.9,sound.pop(),.07)
    add(13.08,sound.bell(880,1.15),.10)
    audio=np.clip(audio,-.98,.98);audio[-4410:]*=np.linspace(1,0,4410)
    path=WORK/'soundtrack.wav';wavfile.write(path,sr,np.rint(audio*32767).astype(np.int16))
    return path

def encode(audio, output_name="The-Priority-ninja-v2.mp4", sequence_name="sequence"):
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
