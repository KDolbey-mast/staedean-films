# The Assembly — 20-second innovation-team reveal (storyboard v1)

**Status:** First-pass animation source now implemented (2026-11-12). Not yet rendered or approved.
**Format:** 1920×1080, 16:9, 20 seconds, 12 distinct drawings/s played at 24fps.
**Visual continuity:** Existing clean ink-and-wash ('wash') look, established rigs, Mount STAEDEAN backdrop. New film; do not alter approved cuts.

## One-sentence premise
Our innovation team gets the green light, assembles like an absurdly important superhero squad, then discovers that assembling a team and running one are two different things.

## Story without sound
A huge APPROVED stamp lands. The PM presses an ASSEMBLE button. Maker, Customer Success and QA respond in rapid theatrical shots. They stand together in an iconic windswept mountain tableau under a glowing idea. Hard cut to a cramped meeting table and a hand raised to ask about budget. The group looks at the PM, who loses his triumphant expression.

## Beat sheet (20 seconds exactly)

| Time | Visual / action | Audio / timing |
|---|---|---|
| 0.0–1.5 | Extreme close-up: APPROVED stamped across a document. | Exaggerated rubber-stamp THUNK; dramatic low chord |
| 1.5–3.0 | PM, usual blue shirt/orange tie, looks up, bright idea bulb; presses red ASSEMBLE button. | Rising brass, mechanical click |
| 3.0–5.0 | Maker lowers a hammer as if holstering a legendary weapon; determined stare. | One absurdly heroic percussion hit |
| 5.0–7.0 | Customer Success flips headset mic down like fighter-pilot visor. | Radio chirp, heroic sting |
| 7.0–9.0 | QA adjusts glasses, glare flashes across lenses. | Tiny metallic 'shing' |
| 9.0–12.0 | Silhouettes approach through theatrical *smoke* (not dense wash filter), Mount STAEDEAN in distance; PM and Maker join the others. | Ridiculously epic original orchestral swell |
| 12.0–15.0 | Freeze-like heroic tableau: PM front, bright idea bulb; the group strikes earnest poses, holding a beat too long. | Music reaches ridiculous peak |
| 15.0–16.0 | Smash cut to painfully ordinary, too-small office table, all three teammates plus PM squeezed into frame. | Music cuts dead; chair squeak |
| 16.0–17.5 | Hand goes up. Caption/speech balloon: 'So... do we have a budget?' | One mundane voice, optional; readable silently |
| 17.5–19.0 | Everyone very slowly turns to look at PM. PM's expression collapses. | Clock tick, awkward silence |
| 19.0–20.0 | Black or clean title card: 'STAEDEAN INNOVATION' / 'ASSEMBLING NOW.' | Tiny button click, no superhero soundtrack imitation |

## Casting and canon
- **PM:** Heroic-but-fallible lead; still blue shirt/orange tie; holds the idea. No summit beard.
- **Maker:** Equal teammate, rust beanie/mustard shirt, hammer prop; don't imply he works for PM.
- **Customer Success:** Existing ginger bob/teal top/headset; believable recruitment gesture.
- **QA:** Existing dark bun/glasses/pink top; well-intentioned team member, not an obstacle.
- **Ninja cameo (Ken-approved exception):** The existing ninja sneaks into the heroic team lineup, looking conspicuously out of place; this is a one-film joke and does not redefine his long-term antagonist role.
- **No sheep:** No setting-driven reason for it in this gag.
- **No invented job titles or claims about the actual innovation staffing.** This is a theatrical ensemble using established cast, not an official org chart.

## Implementation approach
- Add a **new** work/the-assembly/ storyboard/director/build; use established `cast.py` and shared drawing/audio helpers. Do not modify approved film sources or their sound mixes.
- Register `assembly` in `scripts/render_film.py` once implemented.
- Reuse established PM/Maker/supporting character references; existing `cast.official` is chest-up behind counters, so full-body hero-silhouette shots may require shot-specific body compositions while retaining canonical head/clothing features.
- Aim for 240 SVG drawings at 12fps, played at 24fps; render H.264/AAC MP4, confirm exact 20.0 s and readable text on a silent review.
- Use **original** superhero-style orchestral punctuation; do not reuse Marvel recordings or identifiable Avengers themes.
- Keep the joke precise: approval is real, enthusiasm is real, and operational practicalities are funny. The team are not incompetents.

## Review questions
- Is the budget line the strongest possible end gag, or would 'Has anyone booked a room?' land better?
- Should the final card read 'ASSEMBLING NOW.' or just 'WE'RE PUTTING TOGETHER A TEAM.'?

No existing approved sequence is changed by this storyboard.

## First-pass source and render

- `work/the-assembly/director.py` contains the 20-second timeline and established rigs, including the one-film ninja impostor.
- `work/the-assembly/build.py` renders the 12-fps drawings via Playwright Chromium, synthesizes original audio, then produces a 24-fps H.264/AAC MP4.
- Install requirements and Chromium as in the repository README.
- Render from the repository root: `python scripts/render_film.py assembly`.
- For a contact sheet first: `python work/the-assembly/build.py --proof`.
- Expected output: `outputs/The-Assembly-v1.mp4` (not yet produced/verified in this workspace).
- If adjusting a shot, clear only that shot's `work/the-assembly/frames/<shot-name>/` and the `work/the-assembly/sequence/` cache before rendering again.
