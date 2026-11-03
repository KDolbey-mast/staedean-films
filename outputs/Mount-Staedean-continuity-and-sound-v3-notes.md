# Mount Staedean — continuity and sound review

Working edit: the approved 98.83-second shorter cut. Earlier exports are preserved.

## Continuity findings and fixes

Reviewed the first and last retained frames' drawing parameters for all 34 shots in the shorter cut, plus the shot definitions and corrected visual previews.

- **Beard:** the corrected progress shot matches the preceding snowy bench (length 0.36, greying 0.27). Growth then advances to the longer fork beard and the grey, windblown final-ascent beard. No further backward age reset was found in the retained shots. The initial office is intentionally clean-shaven.
- **Paperwork:** fixed Planning carrying 15 sheets after the preceding 16-sheet bench pile. It now carries 16. Restored the 20-sheet load in the progress reveal. Fixed crawling and summit poses resetting to a 12-sheet bundle after the final ascent's 28-sheet load; all now retain 28. Paperwork transfers from hand to beside the bench and later to a strapped bundle; its location changes but its amount should not shrink.
- **Bulb:** checked the chosen idea from the office exit to extinction. Brightness decreases through the checkpoints and climb. No additional upward reset was found at the retained shot boundaries. The low final flickers are intentional, with a falling brightness ceiling, and the bulb stays dead after extinction. The first rejected idea and the new idea forming in the office are separate setup actions, not part of this dimming progression.

The detailed drawing-parameter capture is in work/full-mount/reviewed-edit/continuity-audit.json in the source archive. This records the actual helper arguments for boundary drawings, not a claim of automated visual understanding.

## Sound changes

Previously the shorter version sliced an already-mixed soundtrack. This could cut notes, restart wind noise and truncate effect tails even when an effect's onset was correctly placed.

The new soundtrack uses the edited timeline directly:

- The opening, mountain reveal and reaction are copied sample-for-sample from the previous approved cut through the start of his departure. This protects the little mountain reaction, its volume and timing. An equality check guards this before MP4 encoding.
- One continuous wind bed spans the mountain sequence, growing toward the blizzard and fading into the quieter summit.
- The departure march plays as one phrase across the walk/arrival cut.
- Visible speech, footsteps, taps and movement effects follow their source shot timing and stop with short release fades where the edit cuts them.
- Musical and impact tails can continue across a picture cut. The hopeful music resolves before the customer question, keeping the final silence clear.
- Brief plodding phrases retain their release across travelling-shot cuts.

The audio is rebuilt at its original pitch and the picture is not sped up. A short blend into the new mix occurs after the protected opening block, not across the mountain reaction itself.

## Code breadcrumbs and rebuild

- work/full-mount/mount_reviewed_film.py: this edition's shot staging and continuity corrections.
- work/staedean-cast/src/sets.py: optional paperwork on the distant mountain character.
- work/staedean-cast/src/rig.py: optional paper_count for crawling, leaving earlier callers' defaults unchanged.
- work/full-mount/reviewed_sound.py: sound cue placement, continuous beds, fade lengths and protected-opening assertion.
- work/full-mount/build-reviewed.py: applies the approved frame ranges, reuses unchanged pictures and exports the new mix.
- work/full-mount/check-continuity.py: captures boundary drawing parameters for inspection; run from the project root.

For a fresh source-only rebuild, install the dependencies and configure the browser as in earlier editing guides, then run these scripts in order from the project root: work/full-mount/build.py --render; work/full-mount/build-wind-edit.py; work/full-mount/build-continuity.py; work/full-mount/build-reviewed.py. To rerender this edition after changing its pictures, remove its generated work/full-mount/reviewed-edit folder before rebuilding. This does not remove the exported videos.

## What to watch and listen for

Check the mountain reaction first, then the walk-to-checkpoint music join, the quick bench montage, the mountain-wide sting and the blizzard-to-summit transition. Compare the paperwork around Planning and the crawl. The technical checks establish timing, continuity parameters, sample preservation and a decodable export; the final judgement of comic rhythm and mix remains a listening judgement.

## Export verification

The complete 98.83-second MP4 decoded without errors. The original opening audio is sample-identical through 21.417 seconds before encoding. The mixed waveform peak is 0.765, below clipping.
