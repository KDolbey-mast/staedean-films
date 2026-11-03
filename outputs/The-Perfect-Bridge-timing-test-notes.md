# The Perfect Bridge — opening timing test

A 12-second test, not the full film. Uses the existing PM, Maker and customer, with the approved clean ink-and-wash palette. The wider ensemble can enter in the next sequence after the timing is approved.

## Beats

- 0.0–2.5 seconds: tight view of the PM inspecting the crossing through binoculars; a short dramatic sound builds expectation.
- 2.5 seconds: hard cut wide to the tiny stream. The music stops so the scale joke can land.
- 4.15–5.15 seconds: the Maker turns the plank into a straightforward offer.
- 6.1 seconds: the PM has a rolled plan ready while retaining the binoculars in the other hand.
- 7.4–8.35 seconds: the grand bridge design unrolls, obscuring the customer.
- 9.2 seconds onward: the hidden customer's ellipsis and the Maker's deadpan look leave room for the second joke.

## What to judge

Does the wide cut get a laugh? Is there enough time to register the plank before the plan appears? Does the final hold feel dry and funny or too long? This test is intended to settle those beats before expanding the story.

## How it works

work/bridge-test/director.py owns the setting, new props, posing and timing. It imports the existing cast and wash style without editing the two finished films. The BEATS dictionary contains the main comic-timing anchors. The scene uses the established 12 drawings per second.

work/bridge-test/build.py uses the existing browser-based SVG rendering approach, places sounds on the same timeline, and exports a 1920×1080, 24 fps MP4. Sound cue times are in soundtrack(); update those when changing a beat. Some pose keys are explicit local seconds for fine acting adjustments.

From the extracted source root, install the packages in work/bridge-test/requirements-lock.txt and configure ANIMATION_BROWSER if needed, then run:

```sh
python work/bridge-test/build.py --proof
python work/bridge-test/build.py --render
```

After changing animation, remove the generated work/bridge-test/frames and work/bridge-test/sequence folders before rebuilding so cached frames are not reused. Keep exported videos for comparison.

Verified all 144 drawings rendered and the complete 12-second MP4 decoded without errors. Inspected opening, wide reveal, plan-unrolling and ending frames.
