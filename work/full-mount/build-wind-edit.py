"""Render only the changed beard shots, then make a separate editorial cut.

Cuts select frame ranges at normal speed; sound is cut from the same ranges.
The original performance edition and its frame cache are never overwritten.
"""
import asyncio
import json
import os
from pathlib import Path
import sys
import numpy as np
from scipy.io import wavfile
import build
import mount_wind_film as film

BASE = Path(__file__).parent
build.d.film = film
build.d.SHOTS = film.SHOTS
build.d.timeline = film.timeline
build.WORK = BASE / 'wind-edit'
build.WORK.mkdir(exist_ok=True)
CHANGED = {s['name'] for s in film.SHOTS if s['name'].startswith(('F','G'))}
# Frame ranges are [first, end), at 12 drawings/second. Omitted shots stay whole.
# Preserve the setup, ticket gag, customer question and final bulb extinction.
TRIMS = {
 'B1_oh': (0,34), 'B2_off_he_goes': (0,36), 'C1_arrival': (6,31),
 'C2_the_pitch': (0,42), 'C5_take_a_seat': (0,10), 'C7_087': (0,18),
 'C8_jolt': (0,12), 'C9_onwards': (0,34), 'D1_upwards': (0,22),
 'D2_customer_success': (0,28), 'D4_sit': (0,13), 'D5_product_owner': (0,34),
 'D6_sit_again': (0,12), 'D7_planning': (0,20), 'D8_sit_in_the_snow': (0,17),
 'D9_how_far': (0,42), 'E1_the_fork': (6,34), 'E2_here_be_dragons': (0,22),
 'E3_or_the_sea_monster': (0,22), 'E4_either_way': (0,36),
 'F1_thin_air': (0,29), 'F2_dot_dot_dot': (0,0), 'F3_oxygen': (0,24),
 'F4_on_all_fours': (0,24), 'G1_the_summit': (17,41), 'G4_silence': (0,44),
}


def seed_cache():
    for shot in film.SHOTS:
        if shot['name'] in CHANGED:
            continue
        folder = build.WORK/'frames'/shot['name']
        folder.mkdir(parents=True, exist_ok=True)
        for frame in (BASE/'frames'/shot['name']).glob('*.png'):
            target = folder/frame.name
            if not target.exists(): os.link(frame,target)


def shorter_cut(audio, output_name="Mount-Staedean-tighter-cut.mp4"):
    sample_rate, original_audio = wavfile.read(audio)
    pieces = []; shots = []; manifest = []; position = 0
    for start, shot in film.timeline()[0]:
        count = round(shot['dur']*film.FPS)
        first, end = TRIMS.get(shot['name'], (0,count))
        assert 0 <= first <= end <= count
        if first == end: continue
        name = shot['name'] + '_cut'
        folder = build.WORK/'frames'/name
        folder.mkdir(exist_ok=True)
        for i, n in enumerate(range(first,end)):
            target = folder/f'{i:04d}.png'
            if not target.exists(): os.link(build.WORK/'frames'/shot['name']/f'{n:04d}.png',target)
        duration = (end-first)/film.FPS
        shots.append(dict(name=name, dur=duration))
        first_sample = round((start+first/film.FPS)*sample_rate)
        samples = round(duration*sample_rate)
        piece = original_audio[first_sample:first_sample+samples].astype(float)
        # Tiny fades prevent clicks at edit boundaries without changing cue pitch.
        fade = min(round(.005*sample_rate),len(piece)//2)
        piece[:fade] *= np.linspace(0,1,fade)
        piece[-fade:] *= np.linspace(1,0,fade)
        pieces.append(piece)
        manifest.append(dict(shot=shot['name'],source_frames=[first,end],start=position,duration=duration))
        position += duration
    target = build.WORK/'short-soundtrack.wav'
    wavfile.write(target,sample_rate,np.concatenate(pieces).astype(np.int16))
    timeline = []; elapsed = 0
    for shot in shots:
        timeline.append((elapsed,shot)); elapsed += shot['dur']
    build.d.timeline = lambda: (timeline,elapsed)
    build.encode(target,output_name,'short-sequence')
    (build.WORK/'edit-decisions.json').write_text(json.dumps(manifest,indent=2))
    print('Short cut duration:',elapsed,flush=True)


if __name__ == '__main__':
    seed_cache()
    proof = '--proof' in sys.argv
    asyncio.run(build.render(proof=proof))
    if not proof:
        audio = build.soundtrack()
        build.encode(audio,'Mount-Staedean-wind-beard-edition.mp4')
        shorter_cut(audio)
