# The Door — shorter flight, whole-cast entrance and revised card

This 57-second, 1080p cut retains the accepted clean wash colouring and current performance improvements, with three requested edits.

1. **Shorter parcel flight.** The launch shot ends after 44 drawings (3.667 seconds), just after the package passes horizontally beyond the mountain summit, then cuts to the existing catch. Preparation and the close-to-wide reveal remain. The last visible flight position is approximately x=968, just beyond the summit at x=960. The rest of the arc is omitted.
2. **Whole recurring cast through the door.** The PM, QA, Maker, Customer Success, Product Owner, Planning and the customer enter in a staggered procession. Department characters retain their established heads, clothing, glasses and headset. Their existing counter-height upper bodies are extended with walking legs. The shot is 6.25 seconds, framed to show the feet; the sign becomes HOW WE WORK as the procession finishes.
3. **End-card wording.** The card reads “Some ideas still die.” followed by “Faster..”, using the user's requested wording and punctuation.

The soundtrack is rebuilt against the new shot timeline. Earlier exported films remain available; this edit is saved separately as `The-Door-whole-cast-edition.mp4`.

## Source flow

- `work/full-door/launch_shot.py`: launch duration, geometry and flight cues. `DURATION` sets the earlier cut; the whoosh duration follows the shortened flight.
- `work/full-door/procession.py`: explicit cast order, spacing, walking adapters, doorway masking and sign timing. This reuses the existing cast rather than substituting PM heads.
- `work/full-door/director.py`: revised shot list and durations; imports the procession.
- `work/staedean-cast/src/film2.py`: end-card text.
- `work/full-door/build-final-edits.py`: selects the accepted wash style, reuses unchanged 1080p frames when available, redraws changed scenes, rebuilds the sound and exports.

## Reproduce

Create a Python environment, install `work/full-door/requirements-lock.txt`, and set `ANIMATION_BROWSER` to the local Chromium executable. Run `python work/full-door/build-final-edits.py --proof` to review frames, then run it without `--proof` for the complete film. On a fresh extraction, all required frames are rendered; an existing accepted-colour cache can accelerate unchanged scenes.

Generated files live under `work/full-door/whole-cast-1080`. Remove that cache before rebuilding after a source change. Keep the code and source archives. To change who enters, edit `CAST_ORDER` in `procession.py`; when changing count or spacing, allow enough scene duration for the last character to leave the frame and update sound cue durations in `director.py`.

## Checks

The changed scenes' drawings were parsed as SVG; the summit cut position and cast list were checked. Rendered procession and end-card frames were visually inspected. The full encoded video and audio were decoded, and duration, resolution and frame rate checked. The render remains 12 drawings per second presented at 24 fps.

No original Desktop source archives or earlier finished films were overwritten, and no GitHub push was made.
