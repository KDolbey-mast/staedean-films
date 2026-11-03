# The Perfect Bridge: shelved full-cut experiment

Status: shelved at Ken’s request. The selected version is `The-Perfect-Bridge-binoculars-v2.mp4`, the approved 12-second opening. This longer cut is retained only for reference. Future cast films should generally be standalone 12–15-second gags.

A 41-second ensemble comedy, using the approved binoculars opening and clean ink-and-wash colouring. All seven recurring characters appear: the PM, Maker, QA, Customer Success, Product Owner, Planning and the customer.

## Story and timing

| Time | Beat |
|---|---|
| 0–12 seconds | Approved opening: binoculars, tiny stream, sensible plank, oversized blueprint hiding the customer. |
| 12–19 seconds | The specialists join the discussion; the plan grows through revisions. The customer waits. |
| 19–25 seconds | An impressive bridge appears over the dry ground. The customer points at the actual gap: “Just here.” |
| 25–32 seconds | The cast gathers around the crossing. PM and Maker lower the original plank, then release it. |
| 32–37 seconds | The customer crosses, coffee intact, and gives a thumbs-up. |
| 37–41 seconds | Hold the whole cast around the customer and the useful little bridge: “Start with the customer. Then build what helps.” |

This is a first full editorial cut for review. The grand bridge is intentionally assembled in three comic jumps, rather than a detailed construction sequence. There is no spoken dialogue; the customer's single line is a speech bubble.

## Picture and sound

The original twelve-second opening soundtrack is retained. Subsequent sounds and music use one continuous timeline. The customer's interruption has a deliberate quiet beat; the final music fades. The plank landing has its own impact cue at 29.8 seconds.

The final scene uses one board position to calculate both carriers' hand positions. Their bodies crouch as the board approaches the ground; the feet stay planted. Officials have different walking phases and arm swings. The Maker takes a small step aside after releasing the board so the customer does not obscure his face. The closing tableau retains the positions from the preceding shot.

## Files and modification points

`work/perfect-bridge/director.py` owns the new shots, cast staging, bridge and plank. Its `SHOTS` list sets shot order and duration. `together()` controls gathering, lowering and crossing. `hero()` supplies the crouch while keeping the shared character designs unchanged.

The approved opening is imported from `work/bridge-test/director.py`. Shared characters and colouring are loaded from `work/staedean-cast/src`. The earlier finished films and previews are preserved.

`work/perfect-bridge/build.py` renders each shot, mixes the soundtrack and exports the movie. Its `soundtrack()` contains the audio cue positions; update these when editing shot lengths. The render cache is under `work/perfect-bridge/frames`; clear affected shot folders and the generated `sequence` folder before rerendering changed drawings.

Run with the existing environment:

    work/animation-env/bin/python work/perfect-bridge/build.py --render

The output is 1920 × 1080 H.264/AAC MP4, with 12 drawings per second displayed at 24 fps. Full-file decoding checks for encoding errors. Review the reveal pause, the plank placement and whether the final ensemble feels centred on the customer.

## Verification

All 144 opening drawings match the approved binoculars preview exactly. The first twelve seconds of uncompressed audio also match exactly. Sample frames were inspected for the reveal, group staging, hand contact, crouch and crossing. The full exported MP4 is decoded after encoding.
