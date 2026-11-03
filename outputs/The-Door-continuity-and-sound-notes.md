# The Door — continuity and sound pass

The approved 57-second picture edit, clean wash palette, compact thumbs-down, shortened launch and seven individual walk cycles are retained.

## Continuity review

Reviewed scene definitions and preview samples across all 13 shots, with additional checks on the parcel release/catch and shop transfer.

Fixed:

- The launched parcel's bulb emblem changed brightness at the delivery cut and again when caught. It now stays at the launch's 0.35 setting throughout the delivery shot.
- The shop parcel was offset from the PM's hand and changed size as it entered the transfer. It now starts at the actual hand position and held scale, then interpolates to the recipient's position and scale.
- The travelling shop parcel was being hidden behind the customer queue just before arrival. It now stays in front until the customer holds it.
- The shop transfer had a boundary where neither flying nor held parcel was drawn. The recipient now holds it from the exact end of the transfer.
- The shop parcel's glow stays constant during that hand-off.

Checked and retained:

- Fresh PM and consistent recurring cast appearances; Mount's ageing/paperwork progression does not belong to this story.
- Cardboard prototype, improved prototype and working device progress across the labelled weeks. Changes between weeks are intentional development, not disappearing-prop errors.
- The rejected idea remains in the learned bin during the later visits.
- Coffee is on the table when both customer hands catch the parcel.
- The catapult's projectile starts at the cup's release coordinates. The wide cut and early flight exit remain as approved.
- Seven distinct cast entries in the approved order, with their individual gaits.
- “Some ideas still die. Faster..” and the following lit-bulb ending remain intact. These symbolic closing bulbs and new ideas intentionally do not follow Mount's single-bulb dimming rule.

## Sound pass

- Preserve the previous final mix for the entire Week 1 scene, including the silent customer assessment and rejection/toss beats. A sample equality assertion protects this before encoding.
- Fade the office music into the arrival rather than cutting the phrase abruptly.
- Carry low exterior ambience across development, launch and catch, fading before the shop.
- Continue the launch whoosh to the catch impact, with a short release.
- Match shutter sound length to the retimed shutter animation.
- Schedule serving-number dings from each actual number-change drawing, rather than an unretimed repeating loop.
- Put the sale ching on completion of the parcel hand-off.
- Schedule quiet individual doorway footsteps from each character's leg phase; retain sign-flip cues.
- Soften crowd and musical tails while retaining the shop-to-door theme and closing music bridge.

## Files and modification points

- work/full-door/director.py: approved staging; catch now supplies constant parcel glow.
- work/staedean-cast/src/cast.py: optional box_glow preserves existing caller defaults.
- work/staedean-cast/src/film2.py: shop transfer coordinates, scale and boundary condition.
- work/full-door/reviewed_sound.py: cue timing, fades, continuous ambience and protected Week 1 comparison. SHOP_MAP mirrors the approved shop retiming; update both if that edit changes.
- work/full-door/build-reviewed.py: separate cache and new export, preserving prior movies.
- work/full-door/reviewed-1080/continuity-checks.json and sound-review.json: geometry, cast and audio-check evidence.

For a source-only rebuild, install the packages in work/full-door/requirements-lock.txt, set ANIMATION_BROWSER if the local Playwright Chromium path differs, and run `python work/full-door/build-reviewed.py` from the extracted root. Missing picture caches are rendered automatically; the previous mix can be regenerated to protect Week 1. `--proof` creates a contact sheet. After changing pictures, remove the generated work/full-door/reviewed-1080 folder before rebuilding to avoid stale cached drawings.

Watch the delivery and shop hand-off; listen for the launch-to-catch join, shutter/counter sounds, and footsteps through the door. Technical verification covers cue placement and file integrity; comic rhythm and the final mix remain listening judgements.

## Verification

The complete 57-second export decoded without errors. Week 1's final-mix samples are identical before encoding. The waveform peak is 0.624, below clipping. Verified seven unique cast entries and exact cup/projectile release coordinates, and inspected the hand-off at consecutive boundary drawings.
