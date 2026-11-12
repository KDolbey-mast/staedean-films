"""Render and verify The Assembly at 1920x1080 / 20 seconds.

From repository root:
  python scripts/render_film.py assembly
Or for a cheap contact sheet:
  python work/the-assembly/build.py --proof

Cached shot frames are intentionally reused. To revise a drawing, delete only
work/the-assembly/frames/<shot> and work/the-assembly/sequence.
"""
import argparse
import asyncio
import json
import os
from pathlib import Path
import subprocess
import numpy as np
from PIL import Image,ImageDraw
from scipy.io import wavfile
from playwright.async_api import async_playwright
import imageio_ffmpeg
import director as d
import film_sound as sound

ROOT=d.ROOT
WORK=Path(__file__).resolve().parent
OUT=ROOT/"outputs"
WIDTH,HEIGHT=1920,1080


async def render(proof=False):
    jobs=[]
    for start,shot in d.timeline()[0]:
        folder=WORK/"frames"/shot["name"]
        folder.mkdir(parents=True,exist_ok=True)
        count=round(shot["dur"]*d.FPS)
        indices=sorted({0,count//3,2*count//3,count-1}) if proof else range(count)
        for n in indices:
            target=folder/f"{n:04d}.png"
            if not target.exists():
                jobs.append((shot,n,target))
    print("The Assembly render jobs:",len(jobs),flush=True)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=d.BROWSER or p.chromium.executable_path)
        queue=asyncio.Queue()
        for job in jobs:
            queue.put_nowait(job)
        async def worker():
            page=await browser.new_page(viewport={"width":WIDTH,"height":HEIGHT})
            while not queue.empty():
                shot,n,target=queue.get_nowait()
                # Older rig helpers use one shared time. Drawing finishes before await.
                d.film.NOW=n/d.FPS
                svg=shot["draw"](n/d.FPS,n)
                await page.set_content(
                    f'<style>body{{margin:0}}svg{{width:{WIDTH}px;height:{HEIGHT}px}}</style>'+svg
                )
                await page.screenshot(path=str(target))
            await page.close()
        await asyncio.gather(*(worker() for _ in range(3)))
        await browser.close()
    if proof:
        sheet=Image.new("RGB",(960,len(d.SHOTS)*155),"#f5f0e7")
        draw=ImageDraw.Draw(sheet)
        for row,shot in enumerate(d.SHOTS):
            count=round(shot["dur"]*d.FPS)
            for col,n in enumerate((count//3,2*count//3,count-1)):
                src=WORK/"frames"/shot["name"]/f"{n:04d}.png"
                im=Image.open(src)
                im.thumbnail((320,135))
                sheet.paste(im,(col*320,row*155))
                draw.text((col*320+5,row*155+136),f'{shot["name"]} {n/d.FPS:.2f}s',fill="black")
        target=WORK/"proof.jpg"
        sheet.save(target)
        print("Proof:",target,flush=True)


def soundtrack():
    """An original theatrical pastiche, not an Avengers theme or recording."""
    sr=sound.SR
    total=round(d.DURATION*sr)
    audio=np.zeros(total,dtype=np.float64)
    sound.rng.bit_generator.state=np.random.default_rng(116).bit_generator.state

    def add(at,signal,gain=1):
        start=round(at*sr)
        if start>=total:
            return
        sig=np.asarray(signal,dtype=np.float64)
        length=min(len(sig),total-start)
        audio[start:start+length]+=sig[:length]*gain

    # The absurd overconfident recruiting score grows then stops DEAD at 15s.
    add(.35,sound.stamp(),.45)
    add(1.1,sound.riser(2.8),.055)
    for at in (4,5.5,7,9.5,12):
        add(at,sound.chord_voices([45,52,57,60],1.7,attack=.07,release=1.15,kind="brass"),.13)
        add(at,sound.sub_boom(1.0),.075)
    add(9.2,sound.mountain_hit(),.16)
    add(12.5,sound.riser(2.3),.11)
    # The score disappears on the hard office cut.
    audio[round(15*sr):]=0
    # Add dialogue after the score cut logic. The existing house voice is
    # intentional nonsense; only the on-screen caption carries actual words.
    call_start = next(start for start,shot in d.timeline()[0] if shot["name"] == "call")
    for start,duration,pitch in d.PHONE_PHRASES:
        add(call_start+start,sound.mumble(duration,f0=pitch,rate=6,phone=True),.45)
    add(15.12,sound.creak(.6),.18)
    add(17.55,sound.ticking(1.2,rate=1.4),.08)
    add(19.05,sound.pop(),.06)
    audio=np.tanh(audio)
    audio[-2205:]*=np.linspace(1,0,2205)
    target=WORK/"soundtrack.wav"
    wavfile.write(target,sr,np.rint(np.clip(audio,-1,1)*32767).astype(np.int16))
    return target


def encode(audio):
    sequence=WORK/"sequence"
    sequence.mkdir(exist_ok=True)
    manifest=[]
    index=0
    for start,shot in d.timeline()[0]:
        frames=round(shot["dur"]*d.FPS)
        manifest.append({"shot":shot["name"],"start":start,"duration":shot["dur"],"frames":frames})
        for n in range(frames):
            src=WORK/"frames"/shot["name"]/f"{n:04d}.png"
            assert src.exists(),src
            dest=sequence/f"{index:05d}.png"
            if dest.exists():
                dest.unlink()
            os.link(src,dest)
            index+=1
    assert index==d.DURATION*d.FPS,index
    output=OUT/"The-Assembly-v1.mp4"
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg,"-y","-loglevel","error","-framerate",str(d.FPS),
                    "-i",str(sequence/"%05d.png"),"-i",str(audio),
                    "-vf","fps=24,format=yuv420p",
                    "-c:v","libx264","-crf","18","-c:a","aac","-b:a","192k",
                    "-t",str(d.DURATION),"-movflags","+faststart",str(output)],check=True)
    subprocess.run([ffmpeg,"-v","error","-i",str(output),"-f","null","-"],check=True)
    (WORK/"timeline.json").write_text(json.dumps(manifest,indent=2))
    print("Decoded/verified:",output,flush=True)


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--proof",action="store_true")
    parser.add_argument("--render",action="store_true")
    args=parser.parse_args()
    if not (args.proof or args.render):
        parser.error("Choose --proof or --render")
    OUT.mkdir(exist_ok=True)
    asyncio.run(render(proof=args.proof))
    if args.render:
        encode(soundtrack())
