# The Door — accepted colour edition

This edition applies the accepted clean ink-and-wash colour study to the complete latest catapult cut. It uses richer clothing colours, white skies/backgrounds, soft colour variation and fine continuous outlines. The rejected patchy brush treatment is not selected.

## Deliverable

`The-Door-colour-edition.mp4`: 1920 × 1080, 24 fps, approximately 57.58 seconds. The underlying animation remains 12 drawings per second, held twice. Movement, shot timing, the corrected thumbs-down, the close-to-wide catapult reveal and the catch are unchanged. The saved catapult soundtrack is reused rather than regenerated.

## How to reproduce it

The source package contains the drawing and sound code, current edit, accepted colour renderer, original project documentation and the saved soundtrack. It excludes installed libraries, generated frames and old full-film videos.

1. Create a Python environment and install `work/full-door/requirements-lock.txt`.
2. Set `ANIMATION_BROWSER` to your Chromium executable path.
3. Run `python work/full-door/build-colour.py --proof` for review frames, or `python work/full-door/build-colour.py` for the full export.

`build-colour.py` selects `rb.STYLE='wash'` after the legacy scene imports and uses a dedicated `clean-wash-1080` cache. Every scene's renderer reads that same style setting. This keeps older marker frames out of the colour export. `wash_style.py` controls the accepted palette and shading; `brush_style.py` is the earlier rejected experiment and is not active. `director.py` remains the owner of acting and shot timing, while `launch_shot.py` supplies the revised catapult.

To change a colour, start with `PALETTE` in `wash_style.py`. The fill gradients and pigment filter are in its `wrap()` function. To change the edit, use the shot functions and `SHOTS` list in `director.py`, then regenerate the soundtrack and confirm its duration before using the colour build. The colour build intentionally refuses a soundtrack with a different duration.

After changing the renderer or a scene, remove the generated `work/full-door/clean-wash-1080` cache before rebuilding. Do not remove source files or the saved soundtrack.

## Verification

All 691 drawings were generated and parsed as SVG in the accepted style. Representative frames from every scene were rendered and visually inspected before the full export, including the hands, clothing, mountain reveal, shop and ending. The completed export was fully decoded and checked for duration, resolution, frame rate and audio. The soundtrack file was reused unchanged.

The visual review is based on rendered frames and complete decoding, not a claim of human playback review. The original source archives and earlier finished cuts remain intact. No GitHub push was made.
