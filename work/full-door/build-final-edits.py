"""Build the shorter launch, whole-cast entrance and revised end card at 1080p."""
import asyncio,argparse,os,shutil
from pathlib import Path
import build,rb
parser=argparse.ArgumentParser();parser.add_argument('--proof',action='store_true');args=parser.parse_args()
rb.STYLE='wash'
source=Path(__file__).resolve().parent
build.WORK=source/'whole-cast-1080';build.WORK.mkdir(exist_ok=True)
build.WIDTH,build.HEIGHT=1920,1080
# Reuse identical accepted-colour drawings. The launch only needs trimming;
# the entrance and end card must be redrawn from their changed source functions.
changed={'N1_how_we_work','E1_still_die'}
for shot in build.d.SHOTS:
    dest=build.WORK/'frames'/shot['name'];dest.mkdir(parents=True,exist_ok=True)
    if shot['name'] in changed:continue
    for n in range(round(shot['dur']*build.d.FPS)):
        old=source/'clean-wash-1080/frames'/shot['name']/f'{n:04d}.png'
        target=dest/f'{n:04d}.png'
        if old.exists() and not target.exists():os.link(old,target)
asyncio.run(build.render(proof=args.proof))
if not args.proof:
    audio=build.soundtrack()
    build.encode(audio,'The-Door-whole-cast-edition.mp4','sequence')
