"""Re-render only the doorway acting; reuse the accepted edit and soundtrack."""
import asyncio,os,argparse,subprocess
from pathlib import Path
import build,rb,imageio_ffmpeg
parser=argparse.ArgumentParser();parser.add_argument('--proof',action='store_true');args=parser.parse_args()
rb.STYLE='wash'
source=Path(__file__).resolve().parent
previous=source/'whole-cast-1080'
build.WORK=source/'natural-walk-1080';build.WORK.mkdir(exist_ok=True)
build.WIDTH,build.HEIGHT=1920,1080
for shot in build.d.SHOTS:
    folder=build.WORK/'frames'/shot['name'];folder.mkdir(parents=True,exist_ok=True)
    if shot['name']=='N1_how_we_work':continue
    for n in range(round(shot['dur']*12)):
        old=previous/'frames'/shot['name']/f'{n:04d}.png';dest=folder/f'{n:04d}.png'
        if old.exists() and not dest.exists():os.link(old,dest)
asyncio.run(build.render(proof=args.proof))
if not args.proof:
    audio=previous/'soundtrack.wav'
    if not audio.exists():audio=build.soundtrack()
    name='The-Door-natural-walk-edition.mp4'
    build.encode(audio,name,'sequence')
    start=next(start for start,s in build.d.timeline()[0] if s['name']=='N1_how_we_work')
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-y','-loglevel','error','-ss',str(start),'-i',str(build.OUT/name),'-t','6.25','-c:v','libx264','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart',str(build.OUT/'The-Door-natural-walk-preview.mp4')],check=True)
