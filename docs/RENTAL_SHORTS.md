# Rental shorts — 2026-11-04 handoff

Ken requested committing both current cuts and ensuring the character guides are in place. These are separate shorts. No change to the selected long films or the life-sciences film is included in this commit.

| Film | Export | Format | Render command |
|---|---|---|---|
| The Bigger Picture | `The-Bigger-Picture-v1.mp4` | 28 s, 1080 × 1350, 4:5 | `python scripts/render_film.py bigger-picture` |
| The Lost Fleet | `The-Lost-Fleet-v1.mp4` | 25 s, 1920 × 1080, 16:9 | `python scripts/render_film.py lost-fleet` |

## Review and editing

- [The Bigger Picture storyboard](../work/bigger-picture/storyboard.md), [visual storyboard](../outputs/The-Bigger-Picture-storyboard-v1.jpg), [verification](../work/bigger-picture/verification.json).
- [The Lost Fleet storyboard and product check](../work/lost-fleet/storyboard.md), [visual storyboard](../outputs/The-Lost-Fleet-storyboard-v1.jpg), [verification](../work/lost-fleet/verification.json).
- [Canonical character guide](../work/staedean-cast/docs/CAST.md) and [driving sheep reference](../outputs/The-Lost-Fleet-sheep-v1.png).

Each film's `director.py` controls shot timing, artwork and camera; `build.py` controls rendering, synchronized audio and encoding. Both use the existing shared cast library. Lost Fleet also imports the established binocular drawing from `work/bridge-test/director.py`. Shared drawing source has no new behavioural changes.

Both complete exports were rendered and decoded in the production workspace. Their metadata confirms runtime, dimensions and 24-fps H.264/AAC output. Frame checks cover character identity, prop continuity, text, and the key gag/decision poses. The Bigger Picture's final message is present on all 48 drawings of its four-second hold.

## Character guide reconciliation

The latest cast-guide commit was fast-forwarded before adding these films. The guide now links the actual Lost Fleet sheep rig and still instead of claiming no reference exists. The sheep remains occasional; its hard hat is story-specific. The ninja remains the silent enemy. The customer and Customer Success profiles remain distinct and unchanged.

## Video delivery

Repository convention keeps MP4s, audio renders, source ZIPs and frame caches out of Git. This commit includes source, notes, verification records and preview stills. [Export manifest](rental-short-exports.json) records the exact local movie filenames, byte counts and SHA-256 hashes. These new MP4s have not been uploaded to the older November 3 release. The source ZIPs are convenience copies of this source and are also local exports.
