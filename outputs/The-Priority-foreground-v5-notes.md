# The Priority — foreground staging

The ninja and customer are now 16% larger and stand nearer the bottom edge in the final cutaway. Their shared floor position moves from 930 to 1080 scene units. The desk team, GOOD IDEAS label, glare and Mount Staedean remain in their previous positions, creating more depth between the two groups.

Both actors, their receiving/giving hands, the bulb and the request bubble move together under one transform. This preserves the handoff alignment and nod timing. Feet and the complete bubble remain inside the picture.

The first eleven seconds are reused unchanged. Total duration remains fifteen seconds; the soundtrack is unchanged. Earlier versions are preserved.

## Modification point

In `work/the-priority-foreground/director.py`, `cutaway()` wraps the foreground action in:

    translate(1250,1080) scale(1.16) translate(-1250,-930)

Adjust the scale for apparent distance and the first translation's vertical position for the ground line. Keep the entire handoff inside that group to retain contact between the hands and bulb.

Render with:

    work/animation-env/bin/python work/the-priority-foreground/build.py --render

Clear affected generated frames and the sequence folder before rerendering an edit. Preview frames were inspected for spacing, handoff contact and frame edges. The exported movie is fully decoded to verify video/audio encoding.
