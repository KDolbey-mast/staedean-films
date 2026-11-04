# THE HOUSE STYLE

The look, the timing and the sound that make these films feel like one series. Read this before making anything new with the cast.

**Current authority:** follow [CAST.md](CAST.md) for character roles and casting, and [the current handoff](../../../docs/CURRENT_HANDOFF.md) for the accepted clean ink-and-wash look (`rb.STYLE='wash'`), selected cuts and durations. The marker description below records the original look, not a direction to revert it.

## Look

Inspired by '90s and 2000s European TV cartoons: simple drawings, deadpan jokes, felt-tip colour.

- **Paper:** warm off-white with a faint grain.
- **Line:** thin, scratchy black pen line with small breaks in it (a dash pattern), never perfectly smooth.
- **Colour:** felt-tip marker. Pastel in the middle of a shape, stronger at the edges, with a faint streaky texture. Light comes from the top left, so shading sits bottom-right.
- **Faces:** big round eyes, small pupils that are always visible, pink cheeks.
- **Line boil:** every drawing shimmers slightly because the wobble changes every other drawing.
- **Glow:** the only soft light in the world is the idea bulb (and the product, once it is good).

The style is picked with the `MS_STYLE` environment variable. `marker` is the house style. `line` (black and white) and `colour` (flat) are kept for sketches and drafts.

## Brand

STAEDEAN colours appear in a few small places so they feel like a wink. See `CAST.md` for the full list. Rules:

1. Never more than one or two brand colours in focus at once.
2. The customer is never in brand colours apart from his Sapphire jacket.
3. The logo only appears on an end card.

## Timing

- **12 drawings per second**, shown at 24 fps (each drawing held for two frames). This is what gives the cartoon feel. Do not animate on ones.
- Shot lengths are rounded to whole drawings so picture and sound stay on the same clock.
- Hold on a joke. Let a beat sit for a second before the cut. Film 1 is slow and heavy on purpose. Film 2 is quick and light on purpose.
- Moves ease in and out. Camera moves are slow pushes and pulls, plus one whip zoom in film 1.

## Words

- No dialogue. People talk in speech bubbles full of lines, and their voices are "wah-wah" mumbles.
- The customer gets one real line per film: "Who are you?" and "When can I have it?".
- On-screen text is short, plain and a bit dry: signs, numbers, week cards, end cards.
- End cards are plain paper with one or two short lines in a serif font.
- No em-dashes in on-screen text or docs.

## Sound

All sound is made by code (`src/sfx.py`), no samples.

- **Music:** a plucked office theme. Film 2 has a faster, brighter version with a glockenspiel.
- **Big moments:** brass, choir, timpani and a sub boom with a long reverb. The mountain reveal is minor, the catapult is the major-key mirror of it.
- **Voices:** muffled trombone-like "wah-wah" speech. The customer's line rises like a question.
- **Running gags:** the ticket printer that whirrs too long, the bench creak plus ticking clock, crickets while waiting, a ding-dong when the number changes.
- **Endings:** music eases out under the last scene and a warm pad carries into the end cards. Nothing stops dead unless the stop is the joke.

## Humour

- The system is the joke, never the people. The officials are kind and helpful.
- Exaggerate scale (20,000 m, ticket 087 to 412) and keep faces deadpan.
- Every story should be readable with the sound off.

## Continuity checklist for any new shot

- [ ] Each character has a story reason and follows the canonical profile
- [ ] Ninja retains his silent-enemy role, with no automatic hero/solution substitution
- [ ] Sheep omitted unless a specific gag and setting justify it
- [ ] Team remain well-intentioned, customer remains a customer

- [ ] Pupils visible
- [ ] Bulb in the PM's left hand, paperwork on the other side
- [ ] Bulb is the brightest thing on screen
- [ ] Beard and bulb brightness match where we are in the story
- [ ] Customer tie burgundy, cup sleeve kraft brown
- [ ] Display numbers in sequence
- [ ] Drawn with the cast functions, not redrawn by hand
