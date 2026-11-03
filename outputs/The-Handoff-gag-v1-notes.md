# The Handoff — first 18-second cut

Customer Success leads this gag. A tiny parcel gathers paperwork and increasingly grand packaging as colleagues helpfully pass it along. The enormous box is empty. The ninja quietly delivers the original small parcel to the customer, and Customer Success lowers her headset microphone.

## Edit

| Time | Action |
|---|---|
| 0–3 seconds | Customer gives Customer Success the little parcel; customer releases it. |
| 3–9 seconds | Customer Success, QA, PM, Maker and Planning pass an increasingly large package along the line. Forms accumulate. |
| 9–12 seconds | Customer Success opens the impressive package. The empty interior is revealed; she and Planning look inside. |
| 12–15 seconds | Ninja hands the original little parcel to a delighted customer. |
| 15–18 seconds | Customer Success looks across, back at the box, then lowers the microphone. Hold. |

The tiny parcel has a teal ribbon and red seal in both handoffs. Mount Staedean and the settled ink-and-wash colouring continue the reel's visual world. Music gives the passing sequence momentum, then clears for the empty-box pause and final expression. There is no spoken dialogue or explanatory end card.

## How the pieces connect

`work/the-handoff/director.py` contains the five shots and their durations. `parcel()` draws the identifiable small package; `big_box()` draws both closed and open packaging; `paperwork()` draws the added forms. `chain()` uses one travelling package position to coordinate the people reaching for it. `reaction()` coordinates the microphone rotation and the hand touching its tip.

The existing ninja is imported from `work/the-priority-ninja/director.py`; the existing cast and setting are reused. `work/staedean-cast/src/props.py` adds an optional `mic_angle` parameter to officials. Its default is zero, preserving every earlier headset pose.

`work/the-handoff/build.py` renders the pictures, creates the soundtrack and exports a 1920 × 1080 H.264/AAC MP4 at 24 fps, using 12 drawings per second. Sound cue positions follow the five-shot edit.

Run:

    work/animation-env/bin/python work/the-handoff/build.py --render

Use `--proof` to inspect sample frames. When changing drawings, clear the affected generated shot directory under `frames` plus the generated `sequence` directory before rebuilding; these are caches, not source. All previous films are preserved.

Review the handover, speed of the growing-package sequence, clarity of the empty box, and whether her final pause lands. Proof frames were visually inspected before the full render. The exporter checks the complete movie by decoding its video and audio.
