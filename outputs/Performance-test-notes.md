# The Door: Week 1 performance test

This nine-second standalone scene explores character acting and comic timing using the existing cast and felt-tip renderer. The full films and original source archives were not changed.

## Watch for

- An enthusiastic pitch, followed by a held smile while the customer considers it.
- A customer reaction insert with an eye-line change and blink before the thumbs-down.
- The PM reacting first, then the Maker. Their reactions do not happen in unison.
- The bulb flickering out after the rejection, followed by a brief recovery beat.
- A wind-up, curved bulb toss, follow-through, and settling bin wobble.
- A new idea and a bright musical ending. The joke remains about learning quickly.

The original scene is approximately 4.6 seconds. This test deliberately expands it to 9 seconds to evaluate the acting; it is not yet a proposed final film edit. The comparison clip is silent. The new clip has synthesized sound effects from the existing sound library, with silence under the customer assessment.

## How it connects

`scene.py` controls staging and timing. It imports the existing `cast.py` character definitions and articulated PM puppet, plus `film2.py` scenery and props. `rb.py` supplies the existing marker finish. Playwright renders the SVG drawings in Chromium. The sound library generates timed effects, and FFmpeg combines the drawings and sound into an MP4.

The source package contains the original project, the standalone experiment, and its installed Python dependency versions. It excludes generated frame sequences, installed libraries, and original finished films.

## Modify and run

Place `performance-test` and `staedean-cast` inside a `work` directory beneath your project root. Create a Python virtual environment and install `performance-test/requirements-lock.txt`. Set `ANIMATION_BROWSER` to your Chromium executable path. Run `python work/performance-test/scene.py` from the project root. Output clips are written into `outputs`.

The timing constants at the top of `scene.py` control rejection, fizzle, wind-up, release, landing and the new idea. `frame()` handles the poses and camera; `soundtrack()` uses those same constants for effects. `render_clip()` holds the visual cadence at 12 drawings per second; `encode()` exports at 24 fps.

## Validation and limits

Both clips were rendered from source. Representative frames were visually inspected for character consistency, composition and event timing. Video duration, frame rate, dimensions and audio presence were checked after encoding. This is a performance experiment, not a full-film regression check or a claim that every animation issue is resolved. Integrating it into the full film will require updating the overall timing and rebuilding the full soundtrack.

## Revision 2: readable thumbs-down

The customer hand previously sat close to the jacket, and the close-up cut away after only three drawings of the verdict. The revised shared puppet in `work/staedean-cast/src/props.py` places the fist outside the torso, uses a broader curled fist with a distinct downward thumb, and lifts the forearm to present the gesture. The reaction framing in `scene.py` includes the full hand and holds the verdict for approximately two-thirds of a second. The total clip remains nine seconds and sound timing is unchanged.

This edits the extracted working copy's shared customer pose, so future renders using that copy will inherit the clearer hand. Previously delivered clips, the original archive, and the full film files remain unchanged. The revised clip is `the-door-performance-test-v2.mp4`.

## Revision 3: natural hand proportions

The enlarged thumb in revision 2 looked wrong. The shared customer pose now uses one connected silhouette for the wrist, curled fingers and a short bent thumb. The fist is smaller, the thumb extension is roughly half its previous length, and the finger contours establish a sideways fist. The arm position and longer reaction hold remain unchanged. A close-up still was inspected before rendering the affected frames (39 through 58). The clip keeps the same nine-second duration and soundtrack.

The current deliverable is `the-door-performance-test-v3.mp4`. To adjust the drawing, find the `thumbs_down` branch in `props.py`; the outline controls the shape and the short inner paths define the curled fingers and thumb crease. Camera framing and timing remain in `scene.py`.
