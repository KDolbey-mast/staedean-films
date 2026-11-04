# The Lost Fleet — 25-second storyboard

The existing illustrated world: pale watercolour washes, broken ink contours, the blond customer, red-beanie Maker, Mount Staedean, the corrected binoculars from The Perfect Bridge, and warm bulb glows. New equipment and the sheep use those same drawing primitives and palette.

| Time | Shot and camera | Performance | Audio |
|---|---|---|---|
| 00–04 | Rental yard. Customer foreground left, three empty numbered equipment bays right, Mount Staedean beyond. Gentle widening. | Reads clipboard, looks at empty bays, scratches head. A lonely tumbleweed crosses the yard. | Sparse plucked notes, breeze, dry tumbleweed rustle. |
| 04–06 | Hard cut: excavator in a field. Small pullback reveals large cobwebs. | Spider descends slightly; a weed flutters beside motionless tracks. | First melodramatic orchestral stab. |
| 06–08 | Hard cut: mobile crane halfway up a tree. Tilt from trunk to stranded vehicle. | Branch sags and rebounds; crane hook swings helplessly. | Bigger orchestral stab and a wooden creak. |
| 08–11 | Moving dumper. Start on its load bed, pan to the cab and push closer. | Wheels turn; a hard-hat sheep appears at the wheel, looks toward us, opens its mouth and bleats. | Engine putter and building music. Music stops at 09.8 for BAAAA. |
| 11–16 | Back to exactly the same yard. Maker joins customer; medium two-shot. | Enormous familiar binoculars scan left, right, then lower into his pocket. He calmly brings out a tablet. | Footsteps, exaggerated scan swishes, little pocket plop. |
| 16–21 | Tablet tap, then cut close on the illustrated fleet map. Return to faces for the response. | Bulb markers light sequentially. A sheep icon hops between dated recorded locations and settles. Customer's eyes widen. | Tap and rising bell notes; triumphant flourish as the full picture appears. |
| 21–25 | Familiar free-standing STAEDEAN logo and festoon bulbs, Rental IQ and the exact message. Mount Staedean stays pale in the background. | Tiny sheep-driven dumper crosses the distant hillside. | Warm concluding chord and a quiet final engine putter. |

End-card copy: **Rental IQ** / **Know where every unit is. Every day.**

## Product capability check — 2026-11-04

Primary source: https://staedean.com/rental/feature/equipment-rental-intelligence

STAEDEAN describes a unified rental data model including equipment and locations, alongside connected ERP and other sources. Telematics can be connected and configured. This supports showing recorded fleet whereabouts; it does not establish universal built-in live GPS tracking or a standard animated map interface.

Accordingly, the cartoon tablet is labelled **Recorded fleet locations** and **Location history · illustrative**. The sheep marker moves once between labelled recorded stops and then stays put. This is a visual metaphor, not a reproduction of an actual Rental IQ screen. No LIVE, GPS, real-time, constant refresh, or guaranteed coverage claim is added. The requested end-card slogan is retained as campaign copy; the factual visual is explicitly tied to recorded information.

## How the pieces connect

`director.py` contains the seven shots, camera keyframes, equipment drawings and sheep puppet. Shared cast, scenery, logo and watercolour rendering are imported from `../staedean-cast/src`. The binocular drawing is reused from `../bridge-test/director.py`. Existing films and shared character files remain unchanged.

`build.py` renders the drawings at 12 fps, mixes sound on the same 25-second timeline, encodes a 1080p H.264/AAC movie at 24 fps, and decodes the complete export to verify it. The bleat and music use the existing synthesised sound system, with no downloaded recordings.

Use `../animation-env/bin/python build.py --proof` for keyframes and `--render` for the complete film from this folder. For edits, remove the changed shot's `frames/<shot>` cache and the assembled `sequence` folder before rendering. `SHOTS` holds durations; camera and pose keyframes live in each shot function; timed sound cues are in `soundtrack()`.
