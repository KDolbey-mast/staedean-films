# The Priority — 13-second gag

The PM proudly places one idea on a display. Five teammates arrive with equally important ideas, each carrying the same “PRIORITY 1” label. The PM takes out sunglasses, puts them on, and holds a deadpan look. Mount Staedean remains in the background. No explanatory end card or spoken dialogue.

## Timing

- 0–2.2 seconds: place the first bulb, step back, enjoy the apparent clarity.
- 2.2–7.5 seconds: Maker, QA, Customer Success, Product Owner and Planning arrive in sequence. Some straighten their bulbs; others squeeze in or nudge theirs forward.
- 7.5–9 seconds: hold on six equal priorities; PM blinks and looks towards us.
- 9–10.75 seconds: closer shot, sunglasses from shirt level to eyes, hand lowers.
- 10.75–13 seconds: quiet reaction hold, with one small cricket cue.

## Visual and audio choices

Same established cast and clean wash colouring as the approved Perfect Bridge short. The original mountain drawing provides the background. Bulbs use the established glass, filament and base with smaller local halos so faces and labels stay legible. A light music phrase ends before the reaction; each placement has a small sound on the same scene clock.

## How it connects

`work/the-priority/director.py` controls the entire short. `BEATS` and `ARRIVALS` define its timing, team order, placement positions and individual habits. `teammate()` calculates a shared position for each bulb and the hand carrying it. `pm()` handles the first placement, step back and sunglasses. `sunglasses()` draws the new prop. `setting()` reuses Mount Staedean.

`work/the-priority/build.py` renders the drawings and builds the audio from those same timing constants. It exports 1920 × 1080 H.264/AAC MP4 at 24 fps, displaying each of the 12 drawings per second twice.

The only shared puppet change is an optional `hand_targets` argument in `work/staedean-cast/src/props.py`, allowing officials to place objects. When omitted, the existing arm poses are retained. Earlier films and renders are preserved.

## Rebuild and review

Run:

    work/animation-env/bin/python work/the-priority/build.py --render

Use `--proof` for sample frames. After changing drawings, remove the affected generated `work/the-priority/frames/priority` and `work/the-priority/sequence` folders before rebuilding; otherwise cached frames are reused. These folders contain generated images, not source.

Review the pace of arrivals, readability of the repeated labels, and the sunglasses pause. Sample frames were inspected before rendering. The renderer checks the complete exported movie by decoding its video and audio.
