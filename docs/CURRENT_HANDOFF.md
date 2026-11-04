# Start here: current animation handoff

Prepared 2026-11-03 for Ken and Claude; character direction clarified 2026-11-04. Read the [canonical cast and casting rules](../work/staedean-cast/docs/CAST.md) before drafting a story, then use this handoff for current cuts and source entry points.

## The collaboration

Ken likes quick, concrete animation previews, followed by small visual corrections. Keep the established cast and colouring. Make the requested edit and show a playable movie. Explain changes in plain language. He is an inexperienced programmer; keep implementation clear and add useful purpose/connection comments.

The earlier gag format was generally 12–15 seconds: setup, payoff, short reaction. Ken's current new-short direction is 15–30 seconds; follow the individual brief. Ken explicitly allowed The Priority to extend to 20 seconds; its approved cut is 19.5 seconds. The Handoff is an 18-second first preview, not yet approved. Do not assume every new gag should expand into a longer film.

## Creative decisions to preserve

- Use `rb.STYLE='wash'`: clean ink-and-wash colour. The heavier uneven/brush experiment was rejected as looking like running ink.
- Mount Staedean should loom in the gag reel's outdoor backgrounds.
- Individual walking rhythms, arm swings, readable gestures, expressions and comic pauses matter.
- The PM need not lead every gag. Customer Success (ginger bob, headset, teal top) leads The Handoff.
- The system and helpful overcomplication are the joke; the team are not villains.
- The ninja is the **silent enemy**, not a helpful STAEDEAN hero or automatic rescuer. Reuse the charcoal-clad design, but follow the [ninja profile](../work/staedean-cast/docs/CAST.md#the-ninja) for casting. Existing deliveries do not establish a team allegiance; future stories must make his opposing role clear.
- The sheep is an occasional humorous character/Easter egg, not a universal mascot. Include it only when the gag and setting earn the appearance; follow the [sheep profile](../work/staedean-cast/docs/CAST.md#the-sheep).
- Ken's current direction for new shorts is 15–30 seconds. This does not change the selected cuts below; agree the story's length from its brief rather than copying historical runtimes.

## Current entry points and review state

| Film | Run from repository root | Status |
|---|---|---|
| Perfect Bridge | `python scripts/render_film.py bridge` | Approved 12 seconds; fixed binoculars, Mount Staedean backdrop. |
| The Priority | `python scripts/render_film.py priority` | Approved 19.5 seconds. |
| The Handoff | `python scripts/render_film.py handoff` | First preview. Ken's last request was to publish everything so Claude can continue. |
| The Door | `python scripts/render_film.py door` | Approved 57-second cut. |
| Mount Staedean | `python scripts/render_film.py mount` | Approved 98.83-second cut; fresh build is multi-stage. |

### Perfect Bridge

Source: `work/bridge-test/build-mountain.py` and `director.py`. It is the binoculars/tiny-stream/plank/huge-blueprint opening gag. The 41-second version in `work/perfect-bridge` is explicitly shelved. Do not restore it as the main film or automatically pursue its plank ending.

### The Priority

Latest source: `work/the-priority-reaction/director.py`. It imports `work/the-priority-foreground/director.py`, which imports `work/the-priority/director.py`. Preserve this chain.

- Six bulbs, each tagged PRIORITY 1; desk says GOOD IDEAS.
- Glow grows so bright it almost obscures the team.
- PM puts on sunglasses.
- Cutaway: ninja gives the customer the exact bulb. This recorded delivery is consistent with the team being outmanoeuvred; it is not permission to cast him as their helper. Ninja/customer are larger and nearer the bottom of the frame, separated in depth from the desk team.
- The team must remain recognisable through the glow in that cutaway. The stray low cloud was removed and group opacity corrected.
- Final 4.5 seconds: return to the desk, PM lowers sunglasses, staggered awkward sideways glances, then everyone looks down. Faces must stay readable here.

### The Handoff

Source: `work/the-handoff/director.py`. Five shots: receive (3 s), chain (6 s), empty (3 s), ninja delivery (3 s), Customer Success reaction (3 s).

The customer passes her a tiny parcel with a teal ribbon and red seal. It gathers forms and packaging through CS, QA, PM, Maker and Planning. The grand box is empty. Ninja delivers the original tiny parcel; she looks across/back and lowers her headset mic. This is a first draft for creative review. Do not describe it as final approval. The ninja's delivery must not be read as membership of the STAEDEAN team; the current character guide governs any next treatment.

### Long films

Mount's final notes: `outputs/Mount-Staedean-continuity-and-sound-v3-notes.md`. Preserve progressive beard growth, increasing paperwork, dimming bulb, windblown beard and the special mountain-reveal reaction sound. The protected audio reference is included.

Door's final notes: `outputs/The-Door-everyone-has-an-idea-notes.md`. Preserve stocked hut, feet clipped inside, individually animated whole cast, each walker with a bulb, INNOVATION crossed out with a large X and HOW WE WORK on a second plaque. Parcel flight cuts just over the mountain; end wording is Faster, not But faster.

## Technical conventions and boundaries

- 1920 × 1080, 12 drawings per second displayed at 24 fps, H.264/AAC MP4.
- SVG generated by Python and rendered with Chromium; generic SVG converters do not reproduce the wash filters reliably.
- Python modules use repository-relative `ROOT` values; keep the current work-directory structure.
- `ANIMATION_BROWSER` can override Chromium; the launcher otherwise finds Playwright's installed browser.
- `props.official` optional arguments include hand targets and microphone rotation; `props.customer` includes optional receiving-hand position. Defaults preserve earlier callers.
- Current source and reference assets are in Git. Generated frame caches, local Python environments, earlier videos and temporary tooling are excluded.
- This handoff's small renderer launcher is new; source imports and representative SVG frames were checked. The movies were rendered and decode-verified in the original workspace. Full long-film rerenders were not repeated just for publication.
