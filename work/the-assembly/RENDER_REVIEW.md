# The Assembly — local Mac render review

Rendered 12 November 2026 from `film/the-assembly-storyboard` (PR #1).
Status: rendered first preview, awaiting Ken's creative review. Not an approved cut.

## Delivered movie

- The-Assembly-v1.mp4: 1920 × 1080, 16:9, exactly 20.00 seconds.
- 240 source drawings at 12 fps, encoded as 480 frames at 24 fps.
- H.264, yuv420p, AAC mono at 44.1 kHz, fast-start MP4.
- Size: 3,649,965 bytes.
- SHA-256: `b875b9c68ef217232843901b021ec81f2d8bbb4528c235623ca907cbdc2eeb87`.

## What changed and why

The Maker close-up originally cut off the beanie and face; the camera now includes them. His hammer now follows his hand instead of floating independently. The PM visibly reaches for the ASSEMBLE button. Customer Success raises her hand for the budget line. Maker and Customer Success look right toward the PM, while QA looks left. The budget caption remains through the reaction, and its tail stops above Customer Success's face.

The same PM, Maker, Customer Success, QA and charcoal ninja rigs are reused. The ninja enters the approach and remains in the hero tableau, with a question mark reinforcing the impostor joke. He is absent from the office team. Ken explicitly approved this one-film cameo; it does not make him a canonical teammate. No sheep is inserted.

Only Assembly drawing code and documentation were changed. Shared rigs, older films, sound mixes and main were not edited. The existing Assembly synthesized soundtrack is retained; there is no spoken dialogue.

## Verification performed

All 240 drawings rendered with Playwright Chromium on this Mac. Inspected the 11-row contact sheet and full-resolution Maker, button, lineup and budget frames. FFmpeg decoded both streams to completion without errors: 480 frames / 20.00 seconds. Audio was checked technically, not by a subjective listening review: it is present, peaks at approximately -5.70 dBFS (below clipping), and the dramatic score cuts at 15 seconds. The 16–17.5-second budget window is silent; chair and clock effects remain in the surrounding beats. AAC decoding includes about 16 ms of codec padding; the MP4 presentation duration is 20.00 seconds.

This remains the existing first-pass staging, not a full recreation of every storyboard embellishment. Customer Success and QA's recruitment shots use the existing mic/head movements; the tableau is lightly animated. Judge pacing and musical impact by playing the MP4 with sound, then once muted for the story.

## How the files connect

1. `scripts/render_film.py assembly` selects Chromium and launches `work/the-assembly/build.py`.
2. `director.py` defines the eleven shots, camera crops, gestures and exactly 20-second timeline. It calls the established cast helpers; its ninja is imported from the existing ninja director.
3. `build.py` renders SVG drawings to cached PNGs, synthesizes the soundtrack, encodes the MP4 and runs a decode check.
4. `proof.jpg` shows three samples per shot. `timeline.json` records shot timing.

## Reproduce or modify

Use Python 3.9–3.11, install `requirements.txt`, then run `python -m playwright install chromium`. On this Mac, Chromium needed permission to launch outside the restricted command environment; no renderer workaround was required.

Run `python work/the-assembly/build.py --proof` for the contact sheet, and `python scripts/render_film.py assembly` for the film. When changing a shot, remove only its matching `work/the-assembly/frames/<shot>` cache and the Assembly `sequence` directory before rerendering. Cached drawings otherwise hide source changes. Camera and gesture changes belong in `director.py`; music cues belong in `build.py`. Keep the eleven durations summing to 20 seconds.
