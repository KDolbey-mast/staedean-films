# Mount Staedean — clean wash performance edition

This edition carries The Door's approved clean ink-and-wash colour and performance approach into the original mountain story. It uses the softer wash treatment, not the rejected patchy brush experiment.

## What changed

- The shared wash palette colours the whole film, including the office, checkpoints, mountain and summit.
- Walking has a stronger free-arm swing, a planted-foot rhythm, small body shifts and offset head movement. The bulb's fading brightness also controls the performance energy, so the early walk is livelier than the burdened ascent. Paper-carrying hands remain occupied.
- The first pitch has three deliberate gesture beats and a listening nod. The ticket instruction gets an eye movement before the reaction; the ticket lift overshoots and settles.
- Sitting has a small landing bounce. Later bench scenes add a delayed head slump. The ticket-call jolt now rises from the seat and settles instead of starting below it.
- The write-up is presented in deliberate beats, and the Product Owner has a small listening reaction.
- The mountain-distance reveal holds close, then cuts wide with the existing musical sting.
- The oxygen close-up keeps tired eyes visible between short blinks.
- The customer has small head movements. The PM's smile fades after the question, and the final bulb flicker stays below the preceding shot's brightness.

The original story, cast, dialogue and ending remain: “Some ideas should die. This one didn’t have to.” The Door's launch, doorway procession and “Faster..” ending belong to that film and are not inserted here.

## How the files connect

The source archive preserves a small project layout:

1. `work/full-mount/director.py` chooses the approved `wash` colour and connects the renderer to Mount's staging.
2. `work/full-mount/mount_film.py` contains this edition's shot list, gestures, expressions and timing. It is an isolated copy of the original film staging so edits do not change The Door or the original.
3. `work/staedean-cast/src/` supplies the shared characters, scenery, wash styling and sound generators.
4. `work/full-mount/build.py` draws each shot, mixes its sound cues, joins the shots and checks that the finished movie decodes.

The staging copy deliberately trades a little duplication for keeping the two approved films independent. Future shared character changes belong in the cast source; changes to Mount's performance belong in `mount_film.py`.

## Rebuilding and modifying

Use Python with the packages in `work/full-mount/requirements-lock.txt`, plus a Playwright Chromium browser. Set `ANIMATION_BROWSER` to its executable if it is not at the default Mac location in `director.py`.

From the extracted archive's root:

```sh
python work/full-mount/build.py --proof
python work/full-mount/build.py --render
```

The output is 1920×1080, with 12 drawings per second presented in a 24 fps MP4. The frame cache is intentionally reusable. After editing a shot, delete that shot's folder under `work/full-mount/frames/` and the `work/full-mount/sequence/` folder before rebuilding; otherwise old cached images or sequence links may be reused. The archive contains source rather than generated frame caches.

To adjust a gesture, find the named shot and change its `ramp()` time/value pairs: each pair means “reach this value at this many seconds into the shot.” Sound cues are stored alongside each shot. If you change a duration, review its sound cues too.

## Review

Watch the first pitch and ticket reaction, compare the early walk with the final climb, then watch the close-to-wide mountain reveal and the summit exchange. These are the clearest places to judge the changes. Preview contact sheets sample every shot; they are useful for composition and colour, while the MP4 is the reference for motion and comic timing.

The desktop originals and previous Door exports are untouched. No GitHub changes were published.

## Export verification

Completed all 35 shots (1,449 drawings), mixed the soundtrack to the same 120.75-second timeline, and decoded the entire exported MP4 without errors. Inspected preview samples from every shot and a closer sequence of the ticket-call jolt. The soundtrack peak before encoding is about 0.765, below clipping.
