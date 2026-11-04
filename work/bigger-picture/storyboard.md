# Equipment Rental IQ — The Bigger Picture

28 seconds. Native 4:5 mobile composition, 1080 × 1350. No dialogue.

## Casting and intent

Checked the updated canonical CAST.md and AGENTS.md at shared repository revision 4faa3ab, the current handoff and the supporting-cast model sheet on 2026-11-04.

- Customer: rental-business decision maker. Wants to fulfil an immediate excavator request. Preserve the original blond quiff, Sapphire jacket, burgundy tie and expressive face. His decision resolves the story.
- Customer Success: helps the customer compare useful information. Reuse the original ginger bob, headset, microphone and dark-teal top. She brings the tablet, points and acknowledges his choice. She does not allocate equipment for him.
- Only these two characters are required. The gag is the effort of comparing disconnected reports, not incompetence or bad data.

## Shots

| Time | Composition and movement | Performance and sound |
|---|---|---|
| 00–04 | Shallow rental-yard view behind a desk. Incoming request card with excavator pictogram and NOW. Laptop opens to ERP: AVAILABLE. | Customer looks at the yard and opens the laptop; satisfied nod. Optimistic phrase and reassuring ding. |
| 04–10 | Service, demand and utilization reports slide in, then unfold into an enormous vertical concertina across the window. | Each useful report adds panels. Flaps accelerate; final unfold stops the music. A hand emerges above the wall still holding the tiny NOW request. |
| 10–16 | Customer Success enters on the right, places RENTAL IQ tablet on the clear corner and points. Customer peeks around the paper wall. Cut to three simple picture cards. | UTILIZATION: idle yellow E-17; DEMAND: waiting excavator requests; RISK: teal E-24 with service warning. Three restrained notes. Back to his eyes moving between cards and an idea bulb. |
| 16–22 | Close on the customer's Sapphire sleeve placing the NOW request beside E-17. Pull back as he folds the concertina. Yard becomes visible again. | Decisive click, synchronized paper folds. E-17 moves to the preparation pad; E-24 stays in its marked service bay. Customer Success nods. |
| 22–24 | Close reaction. One report panel springs upright beside him. | Looking towards the yard, he calmly presses it down with one finger. Tiny fwip, hold on his expression. |
| 24–28 | Clean STAEDEAN logo and glowing festoon bulbs. EQUIPMENT RENTAL IQ. BEYOND ERP. / COMPETE ON INTELLIGENCE. | All final copy is fully visible from the first end-card frame to the last. Warm four-second closing phrase. |

## Product and continuity boundaries

ERP availability remains correct. The reports remain useful. Rental IQ's view is symbolic: comparative utilization, demand and service-risk information. The customer places the request himself. No automated allocation, forecasting, predictive maintenance, live location tracking or fictional product interface is implied.

The yellow excavator E-17 and teal excavator E-24 retain their colours and IDs in the yard, picture cards and decision shot. E-24 keeps its service warning throughout. Mount Staedean is seen through the shallow yard window. The small idea bulb belongs to the customer's understanding; it does not make the decision.

## Implementation and review

`director.py` imports the established shared customer and Customer Success rigs. New props and camera keyframes are local to this short. The mobile SVG viewBox and renderer dimensions are both 4:5; this is composed for portrait rather than cropped from a landscape movie.

`build.py` renders at 12 drawings per second, encodes 24-fps H.264/AAC, mixes cues on the same 28-second timeline, and decodes the complete output. Run `../animation-env/bin/python build.py --proof` or `--render` from this folder. Remove a changed shot's frame cache and the assembled sequence before rerendering. The four-second end card has no text fade or obstruction.

Review without sound first: request -> useful but overwhelming reports -> three cards -> customer's own choice -> safe machine prepared -> dry last-panel gag. Then review with sound for the unfolding stop, idea chime and tiny fwip.

## Final continuity pass

The tablet uses the same portrait hardware and vertically stacked cards in wide and close views. The chosen request remains beside the idle-machine card after the customer places it. The ERP laptop stays present; its lid lowers slightly to make room while retaining the AVAILABLE display. Foreground folding gestures replace the resting arm, and the last-panel gag comes from the collapsed stack. A snapshot of the checked canonical cast guide is included in `reference/CAST.md`.
