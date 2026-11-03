# The Door — individual walking performances

The doorway procession now uses a separate walking profile for each of the seven recurring characters. The 6.25-second scene, 57-second edit, accepted colours, shortened catapult shot, end-card wording and existing soundtrack are retained.

## Movement changes

- Different entry times, travel times, step lengths and cycle offsets break the shared marching rhythm.
- Small changes in travel speed are reflected in leg phase, which follows distance travelled.
- The department characters now have relaxed walking arms with bent elbows, counter-swing and visible hands, rather than their old counter poses.
- The Maker has a longer stride and more generous two-arm movement. Planning's stride and arm swing are smaller.
- The PM steadies the bulb while swinging the free arm. The customer swings the free arm while retaining the original coffee-holding arm.
- Small independent head inclinations and glances add variation without changing character design.

## Where to modify it

`work/full-door/procession.py` owns `PROFILES`: entry time, travel duration, step length, leg reach, arm swing, cycle offset and head inclination. The three adapters draw officials, the customer and the PM/Maker through their existing rigs.

`work/staedean-cast/src/props.py` adds optional walking-arm and head-tilt parameters to the original official and customer puppets. Their defaults preserve the earlier poses used in the other scenes.

`work/full-door/build-natural-walk.py` uses a dedicated frame cache, reuses unchanged frames when available, and exports the full film plus a short doorway excerpt. It reuses the previous soundtrack if present; on a fresh extraction it can rebuild one from the same edit.

## Run

Install `work/full-door/requirements-lock.txt` in a Python environment and set `ANIMATION_BROWSER` to the Chromium executable. Run `python work/full-door/build-natural-walk.py --proof` for review frames, then run it without `--proof` for the video exports. Remove its generated `natural-walk-1080` cache before rebuilding changed source.

## Checks

All 75 doorway drawings were generated and parsed as SVG, and every character's entry plus travel time was checked to finish before the cut. Representative poses were visually inspected. The completed preview and full film were decoded to check video and audio integrity. The previous films remain intact; no GitHub push was made.
