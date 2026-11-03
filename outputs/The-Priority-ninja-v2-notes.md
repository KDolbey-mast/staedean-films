# The Priority — ninja cutaway

A 15-second revision of the short gag. The original first eleven seconds, including the sunglasses action, are retained. The long final sunglasses hold is replaced by a four-second customer handoff.

## New ending

At 11 seconds, cut to a wider view nearby. The original team is still gathered around its six equally labelled priorities in the left background. A single charcoal-clad ninja approaches the customer with one bulb. The customer's picture bubble shows the matching bulb shape. The customer reaches out, accepts it, and nods with a delighted smile. A green tick confirms the match; the ninja's eyes smile. No explanatory dialogue or end card.

The new sound is restrained: a short entrance swish, a small handoff sound, and a warm bell on acceptance. The existing audio before the cut is preserved.

## How the drawing and animation connect

`work/the-priority-ninja/director.py` imports the approved scene from `work/the-priority/director.py`. `SHOTS` keeps eleven seconds of that scene, then four seconds of `cutaway()`.

`ninja()` defines the new character using the existing ink-and-wash drawing helpers: charcoal hood, visible friendly eyes, dark fabric clothing, belt and headband tails. The character has no weapons. Its hand follows the bulb's world position until release.

`cutaway()` controls entrance, transfer, receiving hand, customer nod and matching-bulb bubble. The background ensemble reuses the established cast and their final poses. `background_team()` sets the size and placement of that group.

`work/staedean-cast/src/props.py` adds an optional `receive_at` position for the customer's free hand. Existing calls retain their original poses. The coffee hand stays steady throughout the handoff.

`work/the-priority-ninja/build.py` reuses the original audio before eleven seconds and adds the cutaway cues. It exports a separate H.264/AAC MP4 at 1920 × 1080, with 12 drawings per second displayed at 24 fps. The prior 13-second movie is preserved.

## Rebuild and review

    work/animation-env/bin/python work/the-priority-ninja/build.py --render

The existing environment supplies the dependencies; the source bundle also contains the pinned requirements. Set `ANIMATION_BROWSER` if Chromium is installed elsewhere. After editing drawings, clear the affected generated shot folder under `frames` and the generated `sequence` folder before rendering again.

Review the hand-to-hand transfer, the customer's pleased nod, and the contrast with the distracted group. Handoff and ending sample frames were inspected before the full export. The renderer decodes the complete output to check for video/audio encoding errors.
