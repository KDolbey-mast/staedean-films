"""Continuity/sound pass; retain the approved 57-second edit and seven walkers."""
import asyncio,os,sys
from pathlib import Path
import build,rb
import reviewed_sound
BASE=Path(__file__).parent
build.WORK=BASE/'reviewed-1080';build.WORK.mkdir(exist_ok=True)
build.WIDTH,build.HEIGHT=1920,1080
rb.STYLE='wash'
for shot in build.d.SHOTS:
    if shot['name'] in ('L2_got_it','S1_now_open'):continue
    folder=build.WORK/'frames'/shot['name'];folder.mkdir(parents=True,exist_ok=True)
    for frame in (BASE/'natural-walk-1080/frames'/shot['name']).glob('*.png'):
        if not (folder/frame.name).exists():os.link(frame,folder/frame.name)
if __name__=='__main__':
    proof='--proof' in sys.argv
    asyncio.run(build.render(proof=proof))
    if not proof:
        previous=BASE/'whole-cast-1080/soundtrack.wav'
        # Source-only bundles can regenerate the old mix for the protected beat.
        if not previous.exists(): previous=build.soundtrack()
        audio=reviewed_sound.mix(build.d,build.WORK,previous)
        build.encode(audio,'The-Door-continuity-and-sound-edition.mp4')
