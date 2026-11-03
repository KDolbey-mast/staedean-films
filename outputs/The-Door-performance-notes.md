# The Door — performance edition

A complete 56.58-second cut built from the existing STAEDEAN cast and scenery. The approved nine-second Week 1 scene, including the corrected compact thumbs-down, is retained. The drawings remain at 12 per second, held twice in a 24 fps, 1280 × 720 MP4 with synthesized sound.

## What changed

| Scene | Performance treatment |
|---|---|
| Discovering the door | Continuous head turns, a worried beat at the mountain, then recognition and a small door-opening overshoot. |
| Walking to the customer | Walking phase follows distance travelled; both characters ease into their stop, and the customer gives one greeting. |
| Week 1 | Approved pitch, silent customer assessment, delayed reactions, corrected thumbs-down, bulb toss, and renewed idea. |
| Week 2 | Customer points out the issue. The Maker makes three visible, timed hammer strokes; the PM observes and acknowledges. |
| Week 3 | Device illumination precedes the verdict. The Maker and PM celebrate at different moments, and the raised arms settle. |
| Handshake | Both hands meet at a shared contact point, with diminishing pumps and time to read the customer's line. |
| Catapult | More anticipation before release; a single held celebration replaces repeated flashing poses. |
| Catch | Accelerating descent, a small dip under the parcel's weight, recovery, a look at the product and a pleased reaction. |
| Shop | Staggered service gestures, a visible parcel transfer, and queue reactions that settle rather than bounce continuously. |
| How we work | Staggered walkers, clipping at the doorway, a wave that settles, and a readable sign change. |
| Ending | Slightly more room for the extinguished-bulb gag and a gentler logo settle; original wording and branding retained. |

The drawing style and narrative remain the existing project's. This is a performance edit, with some shots rebuilt and others retimed using their original drawings. It is not a new animation engine or a redesign of the characters.

## How the files connect

`work/full-door/director.py` is the edit and acting plan. Each entry in `SHOTS` contains a duration, drawing function and sound cues. `timeline()` rounds durations to whole drawings so picture and sound use the same clock. New acting is expressed through existing puppet controls: gaze, mouth, brows, lean, head angle and arm joints. Original shot functions are reused where a timing adjustment is sufficient.

`work/performance-test/scene.py` supplies the approved Week 1 performance. Its timing constants also drive that scene's sound effects.

`work/staedean-cast/src/cast.py`, `props.py` and `rig.py` supply the existing cast. The corrected thumbs-down is in the `thumbs_down` branch of `props.py`. `film2.py` provides locations, objects and retained shot functions; its shop and launch gestures have small working-copy edits.

`work/full-door/build.py` renders SVG drawings in Chromium, builds the music/effects mix using the established sound library, then encodes the MP4. It can first make a contact sheet with `--proof`, or build the film with `--render`. The soundtrack modules now run their original full-film exports only when invoked directly, so importing their sound functions does not unexpectedly render other films.

## Reproduce or modify

Extract the source package into a project folder. Create an isolated Python environment and install `work/full-door/requirements-lock.txt`. Set the `ANIMATION_BROWSER` environment variable to the path of your local Chromium executable. From the project root, run:

```sh
python work/full-door/build.py --proof
python work/full-door/build.py --render
```

The renderer caches frames by shot in `work/full-door/frames`. After changing a shot, remove its cached frame folder **and** `work/full-door/sequence` before rebuilding. These are generated files only. The default Chromium path in the original experiment is specific to Ken's current Mac; use the environment variable on another machine.

To tune acting, start with the named scene function in `director.py`. The keyframe lists use `(time in seconds, value)` pairs. To change editing pace, adjust the shot duration and cues together. Retimed original shots have a time map and automatically remap their cue start times; any long sound effect may still require a duration adjustment by ear.

The source archive includes the Python drawing/sound code, project documentation, the approved test and the new build scripts. It excludes installed dependencies, generated frame caches, reference image collections and the original large films. The code-generated logo is included.

## Validation and scope

Every drawing in the revised timeline was generated and parsed as SVG. Representative frames from all thirteen shots were visually inspected, with additional inspection of the corrected prototype-tool contact. The complete encoded MP4 was decoded to check for video/audio errors; timing, frame count, resolution, audio duration and signal peak were checked.

Visual checks are based on rendered frames and the complete decode, not a claim of human playback review. Please watch the whole cut with sound to judge performance and musical pacing. This is a review cut at 720p, not a final 1080p master.

Work took place in this chat's extracted working copy. The Desktop source archives and original finished films were not overwritten, and nothing was pushed to GitHub.

## Catapult revision

The new catapult cut starts close on the PM, Maker and loaded machine. At 1.5 seconds it cuts directly to a wide mountain reveal. The arm winds back, accelerates upward, releases at 2.083 seconds, then overshoots and settles. The parcel stays upright in a pivoting cradle before release. Its free-flight position begins at the cup's computed position, with a velocity aligned to the arm's tangent; gravity carries it over the mountain. The sky is extended to cover the wider view. The existing catch follows the launch.

`work/full-door/launch_shot.py` owns the geometry, camera views, timing constants and cues. `cup_position()` is shared by the loaded mechanism and the flight calculation, avoiding a jump at release. `director.py` imports this shot into the full timeline. `build-catapult.py` rebuilds the film and exports an eight-second launch/catch excerpt. The full cut is now 57.58 seconds; the earlier performance edition is preserved separately.

Deliverables: `The-Door-catapult-preview.mp4` and `The-Door-catapult-edition.mp4`. Key preparation, cut, release and flight frames were visually inspected. Release-position continuity was checked numerically, and both encoded files were fully decoded for errors. This is stylized cartoon mechanics rather than an engineering simulation.
