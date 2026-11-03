"""Render the accepted clean wash palette at 1080p without changing the edit.

The separate cache prevents marker/brush frames entering this export. The saved
catapult soundtrack is reused verbatim; no cue generation or retiming occurs.
"""
import argparse,asyncio
from pathlib import Path
import build,rb
from scipy.io import wavfile

parser=argparse.ArgumentParser()
parser.add_argument('--proof',action='store_true',help='Render review frames only')
args=parser.parse_args()
# Legacy scene imports select marker. Set the accepted style after those imports;
# every imported wrap_rb function reads this same module variable when called.
rb.STYLE='wash'
source_dir=Path(__file__).resolve().parent
audio=source_dir/'soundtrack.wav'
sr,samples=wavfile.read(audio)
assert abs(len(samples)/sr-build.d.timeline()[1])<1/sr, 'Soundtrack does not match current edit'
build.WORK=source_dir/'clean-wash-1080'
build.WORK.mkdir(exist_ok=True)
build.WIDTH,build.HEIGHT=1920,1080
asyncio.run(build.render(proof=args.proof))
if not args.proof:
    build.encode(audio,'The-Door-colour-edition.mp4','sequence')
