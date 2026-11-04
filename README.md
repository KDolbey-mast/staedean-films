# STAEDEAN films and gag reel

The shared cast, current animation source and editing handoff for Ken's STAEDEAN films.

**Claude or another collaborator: read the [canonical character profiles and casting rules](work/staedean-cast/docs/CAST.md), then [the current handoff](docs/CURRENT_HANDOFF.md).** The cast guide defines who belongs in each story: the ninja is the silent enemy, and the sheep is an occasional gag, not a universal mascot. The handoff identifies approved cuts, current previews, source entry points and decisions that should not be undone. [AGENTS.md](AGENTS.md) gives a short checklist for future agents.

## Current films

Download the movies from the [2026-11-03 animation handoff release](https://github.com/KDolbey-mast/staedean-films/releases/tag/animation-handoff-2026-11-03). The two rental shorts below are committed as source and previews; their MP4s are not in that older release.

| Film | Duration | Current status | Movie filename |
|---|---:|---|---|
| Mount Staedean | 98.83 s | Approved shorter continuity/sound cut | `Mount-Staedean-continuity-and-sound-v3.mp4` |
| The Door | 57 s | Approved; stocked hut, whole cast with bulbs, crossed-out sign | `The-Door-everyone-has-an-idea.mp4` |
| The Perfect Bridge | 12 s | Approved short gag, corrected binoculars and mountain backdrop | `The-Perfect-Bridge-mountain-v3.mp4` |
| The Priority | 19.5 s | Approved; ninja delivery and awkward final desk glances | `The-Priority-awkward-glances-v6.mp4` |
| The Bigger Picture | 28 s, 4:5 | Current cut; committed at Ken's request | `The-Bigger-Picture-v1.mp4` |
| The Lost Fleet | 25 s, 16:9 | Current cut; driving-sheep gag committed at Ken's request | `The-Lost-Fleet-v1.mp4` |
| The Handoff | 18 s | First preview, awaiting Ken's creative feedback | `The-Handoff-gag-v1.mp4` |

**The 41-second Perfect Bridge expansion is shelved.** The short version above is the selected film.

![The Priority's final desk reaction](outputs/The-Priority-awkward-glances-v6.png)

## Setup and rendering

Use Python 3.9–3.11. The pinned packages match the working Python 3.9 environment; newer Python versions have not been validated.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m playwright install chromium
python scripts/render_film.py bridge
```

Other film keys: `priority`, `handoff`, `door`, `mount`, `bigger-picture`, `lost-fleet`. The launcher selects the installed Playwright Chromium automatically unless `ANIMATION_BROWSER` is already set. Renders are written into `outputs/`. Mount's fresh build runs several historical editing stages and takes longer.

Frame caches are intentionally reused. After editing drawing code, remove the affected generated shot cache and sequence directory as described in that film's notes. Do not delete source or earlier exported movies.

## Source layout

- `work/staedean-cast/src/`: shared character rigs, props, mountain, colouring and synthesized sound.
- `work/staedean-cast/docs/`: canonical character profiles plus original story documentation. The current handoff supersedes older marker-style and duration descriptions.
- `work/staedean-cast/assets/`: cast model sheets, original stills and logo assets.
- `work/full-mount/`, `work/full-door/`: approved long-film edits and continuity/sound work.
- `work/bridge-test/`: approved short Bridge gag.
- `work/the-priority-reaction/`: latest Priority entry point; it imports the earlier Priority stages.
- `work/the-handoff/`: Customer Success-led handoff preview.
- `work/bigger-picture/`: 28-second mobile Equipment Rental IQ short with customer and Customer Success.
- `work/lost-fleet/`: 25-second rental-yard gag with the driving sheep.
- `docs/RENTAL_SHORTS.md`: rental-short review notes, exact export filenames and delivery manifest.
- `outputs/*-notes.md`: editing notes, history and implementation breadcrumbs.

The numbered edit directories are dependencies as well as history; do not remove them without following the imports. Videos and source bundles are release assets, not Git history. A few small WAV reference mixes are tracked because later edits preserve their approved sound exactly.

The repository's original README is retained at [docs/ORIGINAL_README.md](docs/ORIGINAL_README.md).
