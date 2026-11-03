# The Priority — blinding desk revision

The desk full of bulbs now builds into an exaggerated white-hot glow, almost obscuring the entire team. The glow rises continuously as the priorities accumulate, reaching its full strength around 7.7 seconds. The PM remains faintly visible at the edge for the sunglasses beat.

The same glare follows the smaller background group in the ninja cutaway. The ninja, customer and single useful bulb remain clear in front. Runtime remains 15 seconds; action, cuts and sound timing are unchanged from the ninja revision. Earlier exports are preserved.

## How to adjust it

`work/the-priority-glare/director.py` contains `glare(t)`: its timing points control the build, its gradient stops control the white core and yellow edge, and the ellipse dimensions control how much of the group is obscured. `bright_opening()` adds it over the original gag. `background_team()` applies the same effect inside the group's scaled background placement.

`work/the-priority-glare/build.py` exports the separate revised movie. It imports the established cast and original Priority staging, preserving the previous film sources.

Rebuild using:

    work/animation-env/bin/python work/the-priority-glare/build.py --render

Clear the generated `frames` and `sequence` folders in this revision before rerendering changed drawings. Sample frames were checked at the bright wide shot, sunglasses hold and ninja handoff. The renderer decodes the complete exported video and audio to check encoding.
