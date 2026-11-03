# The Priority — awkward final glances

The approved fifteen-second sequence is followed by a new 4.5-second reaction shot at the GOOD IDEAS desk. Total runtime is 19.5 seconds.

The PM lowers his sunglasses so we can see his eyes. Sideways glances pass around the group at staggered times, smiles drop into straight faces, then everyone looks down at the bulbs. A tight ensemble view keeps all six team members and the desk label visible. The light is exposed more gently for this reaction so the eyes remain readable. The ninja handoff and foreground staging are unchanged.

The new shot is mostly silent, with a small glasses movement sound and one cricket near the end. There is no explanatory caption or dialogue.

## How to change the timing

`work/the-priority-reaction/director.py` imports the approved version from `work/the-priority-foreground/director.py`. `SHOTS` appends the reaction after fifteen seconds. `glance(t, index)` controls the stagger, direction and final downward look. `reaction()` draws the team, moves the PM's sunglasses and chooses the closer framing and glare level.

`work/the-priority-reaction/build.py` preserves the previous fifteen seconds of audio and adds only the final cues. The first two shots reuse their existing rendered frames.

Run:

    work/animation-env/bin/python work/the-priority-reaction/build.py --render

Clear the generated reaction frames and sequence folder before rebuilding changes to that shot. Earlier movies and their source are preserved. The reaction sample frames were inspected for eye direction, glasses contact, labels and framing. The complete exported movie is decoded to verify video/audio encoding.
