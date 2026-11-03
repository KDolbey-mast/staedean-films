# The Door — stocked hut, everyone's idea, new sign

This version keeps the 57-second edit and the previous continuity/sound corrections.

## Changes

- Clip the Product Manager's drawing to the hut interior so his shoes cannot protrude below the front wall.
- Place two six-box stacks behind the team, inside the shop window and behind the shutter. They use the established product packaging.
- Give all seven doorway characters a glowing bulb: PM, QA, Maker, Customer Success, Product Owner, Planning and customer. Their different leg cycles and head movements remain. The officials keep one arm free to swing, the Maker holds the bulb with one hand, and the customer keeps the coffee in the other hand.
- Retain INNOVATION on the original sign. Two animated red strokes draw a big X across it; HOW WE WORK appears on a separate plaque immediately below. Both signs remain visible at the end of the shot.
- Add a short scribble sound to the crossing-out gesture, retaining the plaque/reveal cues and protected Week 1 soundtrack.

## Where to edit

- work/staedean-cast/src/film2.py, S1_now_open: stock positions, box count and hut clipping.
- work/staedean-cast/src/props.py: optional carry_idea setting for walking officials and customer; other callers keep their previous behavior.
- work/full-door/procession.py: all seven walkers request bulbs; the Maker's bulb and two-sign reveal are staged here. SIGN_FLIP remains the existing 4.6-second timing anchor despite no longer flipping the sign.
- work/full-door/build-details.py: reuse unaffected frames, add the sign scratch and export a separate film.

Rebuild from the extracted project root with `python work/full-door/build-details.py`, using the Python dependencies in work/full-door/requirements-lock.txt and ANIMATION_BROWSER for a different Chromium path. Missing picture caches render automatically. Use --proof for a contact sheet. After changing these scenes, remove the generated work/full-door/details-1080 folder before rebuilding so old cached frames are not reused. Earlier exported movies remain intact.

## Review

Look at the bottom of the hut and stock behind the team, then follow each walker’s bulb. At the end of the doorway shot, both the crossed-out old sign and the new sign should be readable together.
