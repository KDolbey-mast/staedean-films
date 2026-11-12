# The Assembly — local Mac render review

Rendered 12 November 2026 from `film/the-assembly-storyboard` (PR #1).
Status: rendered first preview, awaiting Ken's creative review. Not an approved cut.

## Delivered movie

- The-Assembly-v1.mp4: 1920 × 1080, 16:9, exactly 20.00 seconds.
- 240 source drawings at 12 fps, encoded as 480 frames at 24 fps.
- H.264, yuv420p, AAC mono at 44.1 kHz, fast-start MP4.
- Size: 3,883,626 bytes.
- SHA-256: `19e06f0cf117273ba1bed50de4313e21f2235e23b817ce2b6a11fa2b0288c267`.

## Current bulbs and props revision (v4)

Ken requested a bulb for everyone assembling, and clearer cellphone and hammer designs. All five lineup figures now hold a lit bulb: Maker, Customer Success, PM, QA and ninja. Bulbs remain attached to the carrying hands in approach and tableau shots, with restrained additional glow so faces remain readable. The ninja copies the ensemble as part of the approved impostor gag.

The phone is now a wider rounded smartphone with a lit call screen, contact icon, red hang-up button, earpiece and home button. The hammer now has a flat striking face, split claw, metal head and wooden handle. Both props use local character coordinates to retain hand contact. Changes are confined to the Assembly director and documentation; shared rigs and older films are untouched.

The current download is **The-Assembly-v4.mp4**. Inspected proof frames for the phone, hammer, approach and heroic tableau. Rerendered the four changed shots and decoded the complete movie successfully: 480 frames, 1920 × 1080, 24 fps, 20.00 seconds, H.264/AAC. Sound, gobbledygook, shot timing, budget ending and globe outro remain unchanged. For future edits, `team()` controls the five bulbs, `phone_call()` draws the smartphone, and `maker()` draws the claw hammer. `official_full(carry_idea=True)` selects the established carrying pose only for this film.

## Phone-call revision (v3)

Ken requested a close-up of the product guy saying “I'm putting together a team” in the house gobbledygook language. The PM now holds a phone at his ear in a three-second close-up (1–4 seconds), with the exact caption and animated mouth shapes. The existing `sfx.mumble(..., phone=True)` synthesizer supplies four nonsense phrases. `PHONE_PHRASES` in `director.py` is shared with `build.py`, aligning phrase windows and mouth motion. No external voice service or new dependency is involved.

The phone call replaces the button shot. The approval stamp is now one second, and Maker/Customer Success introductions are 1.5 seconds each. QA and every later shot keep their previous times, so the ninja, budget reaction and globe outro are preserved. The riser is quieter under the call; the recruitment hits move to match the revised cuts.

The v3 download was **The-Assembly-v3.mp4**. All changed shots were rerendered, the phone close-up was visually inspected, and the full MP4 decoded at 480 frames / 20.00 seconds. Speech windows measure approximately -19 to -21 dBFS RMS in the source mix; the encoded mix remains below clipping. This is technical audio verification; Ken should review the gobbledygook's performance by listening. The unchanged renderer output basename remains The-Assembly-v1.mp4 inside the repo.

## Globe outro correction

Ken requested the familiar globe outro. The final second now reuses `film2.py`’s `E3_logo` drawing directly: nine illuminated globes above the traced teal STAEDEAN logo, with INNOVATION · ASSEMBLING NOW. below. No shot durations or audio changed. The revised user download is The-Assembly-v2.mp4; the repository render command still writes its established The-Assembly-v1.mp4 filename. The final outro frame was visually inspected and the revised MP4 fully decode-checked at 20.00 seconds / 480 frames.

## What changed and why

The Maker close-up originally cut off the beanie and face; the camera now includes them. His hammer now follows his hand instead of floating independently. The earlier button-contact fix is superseded by the requested phone close-up. Customer Success raises her hand for the budget line. Maker and Customer Success look right toward the PM, while QA looks left. The budget caption remains through the reaction, and its tail stops above Customer Success's face.

The same PM, Maker, Customer Success, QA and charcoal ninja rigs are reused. The ninja enters the approach and remains in the hero tableau, with a question mark reinforcing the impostor joke. He is absent from the office team. Ken explicitly approved this one-film cameo; it does not make him a canonical teammate. No sheep is inserted.

Only Assembly drawing code and documentation were changed. Shared rigs, older films, sound mixes and main were not edited. The soundtrack remains synthesized, with the new gobbledygook phone speech and no intelligible spoken dialogue.

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
