"""Continuity audit edition: preserve the approved edit, replace affected shots,
and rebuild sound from the cue list on that edit's clock.
"""
import asyncio
import importlib.util
import json
import os
from pathlib import Path
import sys
import build
import mount_reviewed_film as film
import reviewed_sound
BASE=Path(__file__).parent
spec=importlib.util.spec_from_file_location('wind_edit',BASE/'build-wind-edit.py')
edit=importlib.util.module_from_spec(spec);spec.loader.exec_module(edit)
build.d.film=film
build.WORK=BASE/'reviewed-edit';build.WORK.mkdir(exist_ok=True)
CHANGED={'D7_planning','D9_how_far','F4_on_all_fours'}|{s['name'] for s in film.SHOTS if s['name'].startswith('G')}
shots=[]
for source_start,source in film.timeline()[0]:
    first,end=edit.TRIMS.get(source['name'],(0,round(source['dur']*12)))
    if first==end:continue
    shot=dict(source,source_name=source['name'],source_first=first,dur=(end-first)/12)
    def draw(t,n,source=source,first=first):
        film.NOW=(first+n)/12
        return source['draw']((first+n)/12,first+n)
    shot['draw']=draw;shots.append(shot)
    if source['name'] not in CHANGED:
        folder=build.WORK/'frames'/source['name'];folder.mkdir(parents=True,exist_ok=True)
        for i,n in enumerate(range(first,end)):
            previous=BASE/'continuity-edit/frames'/source['name']/f'{n:04d}.png'
            if not (folder/f'{i:04d}.png').exists():os.link(previous,folder/f'{i:04d}.png')
timeline=[];total=0
for shot in shots:timeline.append((total,shot));total+=shot['dur']
build.d.SHOTS=shots;build.d.timeline=lambda:(timeline,total)
if __name__=='__main__':
    proof='--proof' in sys.argv
    asyncio.run(build.render(proof=proof))
    if not proof:
        audio=reviewed_sound.mix(timeline,total,build.WORK,BASE/'continuity-edit/short-soundtrack.wav')
        build.encode(audio,'Mount-Staedean-continuity-and-sound-v3.mp4')
