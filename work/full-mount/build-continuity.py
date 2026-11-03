"""Refresh the progress reveal, reusing the approved shorter cut and beard frames."""
import asyncio
import importlib.util
import os
from pathlib import Path
import sys
BASE = Path(__file__).parent
spec = importlib.util.spec_from_file_location('wind_edit', BASE/'build-wind-edit.py')
edit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(edit)
build = edit.build
build.WORK = BASE/'continuity-edit'
build.WORK.mkdir(exist_ok=True)
for shot in edit.film.SHOTS:
    if shot['name'] == 'D9_how_far': continue
    target = build.WORK/'frames'/shot['name']
    target.mkdir(parents=True,exist_ok=True)
    for frame in (BASE/'wind-edit/frames'/shot['name']).glob('*.png'):
        if not (target/frame.name).exists(): os.link(frame,target/frame.name)
if __name__ == '__main__':
    proof = '--proof' in sys.argv
    asyncio.run(build.render(proof=proof))
    if not proof:
        edit.shorter_cut(BASE/'wind-edit/soundtrack.wav', 'Mount-Staedean-tighter-cut-v2.mp4')
