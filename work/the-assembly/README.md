# The Assembly — work-in-progress

A **proposed** 20-second Avengers-style parody celebrating approval to assemble the STAEDEAN innovation team. Existing approved films are untouched. This short follows the existing cast guide and reuses the clean wash animation pipeline.

## Review

- Story and timing: [storyboard.md](storyboard.md)
- Animation shots and keyframes: [director.py](director.py)
- Audio and encoding: [build.py](build.py)
- Existing cast/canon: [../staedean-cast/docs/CAST.md](../staedean-cast/docs/CAST.md)
- Export name when rendered: `outputs/The-Assembly-v1.mp4`

## Render

From the repository root, use the established Python 3.9–3.11 environment and Playwright Chromium.

```sh
python work/the-assembly/build.py --proof
python scripts/render_film.py assembly
```

The first command creates an 11-row contact sheet at `work/the-assembly/proof.jpg`. The second renders 240 distinct drawings at 12fps, encodes 24fps H.264/AAC with the original synthesized soundtrack, and runs an FFmpeg decode check. **Rendered and visually inspected on Ken's Mac on 2026-11-12; see [render review](RENDER_REVIEW.md) for checks, fixes and remaining preview limitations.** Treat this as a reviewable production draft, not a completed delivery.

To rerender a corrected shot, delete only its `work/the-assembly/frames/<shot>` folder and `work/the-assembly/sequence` before running the full build; otherwise cached PNGs will remain unchanged. Do not remove original film output or edits.

## Creative notes

The approved decision should feel genuinely exciting. The dramatic music and hero poses are knowingly ridiculous. The team are nice people; the budget joke is about the practical gap between approval and mobilisation, not about incompetence. No Marvel audio, costumes or visual trademarks are reproduced.

The current end line is **"So... do we have a budget?"**, followed by the established **STAEDEAN logo and nine glowing globes**, with **INNOVATION · ASSEMBLING NOW.** below. Both are editable on review. Do not change canonical character profiles or declare this cut approved without Ken's review.

## Phone-call revision

The approval stamp now runs 0–1 seconds, followed by a 1–4-second PM phone close-up captioned “I’m putting together a team.” The existing `sfx.mumble` voice supplies the gobbledygook. `PHONE_PHRASES` in `director.py` supplies the phrase timing to both mouth animation and `build.py` audio, so changes remain aligned. Maker and Customer Success introductions are 1.5 seconds each; all shots from QA onward retain their previous times, including the globe outro at 19–20 seconds.
