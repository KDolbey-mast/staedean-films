# The Priority — GOOD IDEAS and ending corrections

The desk front now says GOOD IDEAS in both the main gag and the ninja cutaway.

The main gag retains the exaggerated brightness approved in revision 3. In the final cutaway, only the glare strength is reduced to 58%, leaving the team and desk recognisable behind the ninja and customer. The group itself is now fully opaque: the previous group-level transparency allowed scenery to show through the characters and light. The low mountain cloud directly behind that group is also removed from the cutaway.

Runtime, action, camera cuts and soundtrack remain the same: 15 seconds, including the four-second ninja handoff. Earlier movies are preserved.

## Modification points

`work/the-priority-polish/director.py` imports the original Priority staging. `labelled_pedestal()` adds the shared desk text. `glare(t, strength_scale=1)` keeps full intensity in the opening; `background_team()` uses 0.58 in the cutaway without fading the entire group. `cutaway()` removes the one low background cloud from its scenery.

`work/the-priority-polish/build.py` exports the new movie. Run:

    work/animation-env/bin/python work/the-priority-polish/build.py --render

After changing drawings, clear this revision's generated `frames` and `sequence` directories before rebuilding. The shared cast and earlier source files are unchanged by this revision.

The desk label and corrected ending were inspected in rendered samples. The complete MP4 is decoded after export to verify its video and audio encoding.
