# THE CAST

The recurring characters, props and places from the STAEDEAN films. Every one of them is drawn by code, so they look the same every time they appear. Change a drawing once and it changes everywhere.

The model sheets are in `assets/sheets/`. Regenerate them with `make sheets`.

All drawing calls go through `src/cast.py`. Coordinates are in a 1920 x 1080 frame. `(x, y)` is where the character's feet touch the ground unless noted.

```python
import os; os.environ["MS_STYLE"] = "marker"   # house look, set before importing
import cast
from render import render

art  = cast.pm(700, 900, pose="stand", mood="hopeful", bulb=1.0)
art += cast.customer(1250, 890, pose="thumbs_up", mood="delighted")
render([("my_frame", cast.frame(art))], "out")
```

Names: the characters are known by their roles for now. If they get names, add them here and as aliases in `cast.py`.

---

## The PM

![PM expressions](../assets/sheets/01_pm_expressions.png)

**Role:** the hero. A product manager who has an idea and tries to get it to the customer. In film 1 he climbs Mount Staedean and fails. In film 2 he walks through the door and succeeds.

**Design**

| Part | Look | Base colour in code | Final colour (marker look) |
|---|---|---|---|
| Hair | tousled, brown | `#7b4b2b` | `#8c5630` |
| Face | normal nose, pink cheeks, big round eyes | skin `#f0c9a6` | warm peach |
| Shirt | pale blue, sleeves rolled up | `#b9d3e6` | `#c3e2f4` |
| Tie | | `#c0623a` | **Tangerine Orange `#FF9C46`** |
| Trousers | | `#3a3a40` | **Galaxy Black `#1F2342`** |
| Shoes | brown | | |

**Calls**

```python
cast.pm(x, y, s=0.42, pose="stand", mood="hopeful", bulb=1.0, age="fresh",
        phase=0.0, mirror_it=False, stack=0, pack=0, tank=False)
cast.pm_head(x, y, s=1.0, mood="neutral", age="fresh")   # close-ups
```

- `pose`: `stand`, `walk`, `trudge`, `sit`, `crawl`
- `mood`: `neutral`, `hopeful`, `delighted`, `surprised`, `talking`, `thinking`, `annoyed`, `weary`, `sad`, `dismayed`, `content`, `exhausted`
- `age`: `fresh`, `stubble`, `first bench`, `mid climb`, `the fork`, `summit`, or your own `(beard, grey)` pair from 0 to about 1
- `phase`: walk cycle position in radians. Add about 0.75 per drawing for a steady walk.
- `stack`: number of sheets in his paperwork pile. `pack`: height of the paperwork backpack. `tank`: oxygen tank.

![PM poses](../assets/sheets/02_pm_poses.png)
![PM climb](../assets/sheets/03_pm_climb.png)

**Rules**

1. His pupils are always visible. Heavy lids never cover them.
2. He holds the idea in his **left hand**, which is screen-right when he faces right.
3. Paperwork is always on the other side.
4. The beard only grows within a story. Grey arrives from mid-climb.
5. Normal nose. The first big-nosed version was rejected.

---

## The idea

![The idea](../assets/sheets/04_the_idea.png)

**Role:** the real main character. A light bulb.

```python
cast.idea(x, y, s=1.0, brightness=1.0, dead=False)
```

| Brightness | Meaning |
|---|---|
| 1.0 | just chosen. Rays, big glow. The brightest thing on screen. |
| 0.8 to 0.4 | the climb. Glow shrinks, rays thin out then vanish. |
| 0.2 to 0.06 | thin air. An ember. |
| 0.0 | off |
| `dead=True` | burnt out, filament broken, little crosses |

**Rules**

1. Nothing on screen is ever brighter than a live idea.
2. In a "death" story it only dims, never recovers.
3. In film 2 ideas can fail fast (fizzle into the LEARNED bin) and a new one lights straight away. Failing is fine, dying slowly is not.
4. The "together" ending is a string of bulbs, all lit.

---

## The customer

![The customer](../assets/sheets/05_customer.png)

**Role:** the person all of this is for. In film 1 he is at the top of the mountain and has never heard of us ("Who are you?"). In film 2 he is 20 m away, gives honest feedback every week and ends up asking "When can I have it?".

**Design**

| Part | Look | Colour |
|---|---|---|
| Hair | blond quiff | `#d9b25a` |
| Jacket | smart, lapels | **Sapphire Blue `#00316C`** (base `#4f7a5c` remapped) |
| Tie | | burgundy `#8e2f45` |
| Coffee | takeaway cup, kraft-brown sleeve `#b08a5a` | |
| Trousers | | slate `#323a48` |

```python
cast.customer(x, y, s=0.52, pose="phone", mood="neutral", look=(0, 0),
              blink=False, palette=None, coffee=True, box=False)
```

- `pose`: `phone`, `down`, `wave`, `thumbs_up`, `thumbs_down`, `point`, `shake`, `hold_box`
- `mood`: `neutral`, `happy`, `delighted`, `puzzled`, `unimpressed`, `talking`
- `palette`: override any of `JK` (jacket), `HR` (hair), `TIE`, `SK` (skin), `TR` (trousers). This is how the queue customers are made.

**Rules**

1. **He never wears STAEDEAN colours on his tie or cup.** Only the jacket is brand Sapphire. He is the customer, not one of us.
2. Thumbs are drawn wide and chunky so a thumbs-up never reads as a rude gesture. Keep it that way if you redraw hands.
3. He is front-facing. He only speaks one line per film.

---

## Supporting cast

![Supporting cast](../assets/sheets/06_supporting_cast.png)

### The four officials

Behind every counter. In film 1 they each stop the PM with a checkpoint. In film 2 they all stand together in the shop window, serving the customers, with their department plaques underneath.

| Department | Look | Top colour (marker look) | Call |
|---|---|---|---|
| QA | dark bun, glasses | Pink `#FF95D2` | `cast.official("qa", x, y)` |
| Customer Success | ginger bob, headset | dark teal `#008C94` | `cast.official("customer success", x, y)` |
| Product Owner | short dark hair, glasses | purple `#6749C9` | `cast.official("product owner", x, y)` |
| Planning | bald, grey sides, glasses | blue `#3d6fb0` | `cast.official("planning", x, y)` |

`gesture`: `rest`, `point_left`, `point_right`, `finger_up`. `mood`: `smile`, `flat`, `talk`, `o`. `(x, y)` is the counter top, not the feet: they are drawn from the chest up.

**Rule:** the officials are never villains. They are nice people doing their jobs inside a slow system. In film 2 the same people are the ones who make the product fly.

### The Maker

The PM's teammate in film 2. One person who builds the prototypes while the PM goes to see the customer.

```python
cast.maker(x, y, s=0.42, mood="hopeful", phase=None)   # phase=None stands, a number walks
```

Dark hair, rust beanie, mustard shirt, green tie. Same body as the PM so they read as equals.

### Colleagues

Three recoloured versions of the PM body, each with their own idea. They walk through the door at the end of film 2 to show this is how everyone works now.

```python
cast.colleague(i, x, y, s=0.42, phase=0.0, bulb=0.8)   # i = 0, 1, 2
```

### The queue

The market. Customer bodies with different jackets, hair and ties (`film2.QUEUE`). Use `cast.customer(..., palette=film2.QUEUE[i])`.

---

## Props

![Props](../assets/sheets/07_props.png)

| Prop | Where it lives | Notes |
|---|---|---|
| Checkpoint booth | `props.booth_back` / `booth_front` | Teal roof. Sign text is a parameter. Wall calendar inside. |
| Ticket dispenser | `props.dispenser` | "PLEASE TAKE A TICKET". The strip loops on the floor when it whirrs too long. |
| Now serving | `props.now_serving` | 086, then 087, then 088. Later booths show 412. |
| The bench | `props.bench` / `bench_front` | "PLEASE TAKE A SEAT". Creak and a ticking clock every time someone sits. |
| Speech bubble | `props.bubble` | Lines, not words. Nobody speaks real words except the customer. |
| Signposts | `props.signpost` | The fork: ERP ROADMAP (dragon) and AI ROUTE (sea monster). |
| The door | `film2.door` | Small, teal frame. "INNOVATION / CUSTOMER 20 m". Flips to "HOW WE WORK". |
| Prototypes | `film2.proto(x, y, v)` | v1 cardboard box, v2 box with a dial and aerial, v3 lit dome. |
| The product | `film2.product_box` | Kraft box with teal ribbon and a glow. |
| LEARNED bin | `film2.learned_bin` | Where failed week-one ideas go. Fast failure is good. |
| Catapult | `film2.catapult` | Week 4. Throws the product over Mount Staedean. |
| Week cards | `film2.day_card` | WEEK 1 to WEEK 4. |
| Paperwork | `rig.paper_stack`, `rig.backpack` | Grows with every checkpoint. |
| Oxygen tank | `rig.oxygen_tank` | Teal. Summit only. |

## Places

| Place | Code | Seen in |
|---|---|---|
| The office | `office.py` (`back_wall`, `window`, `desk_top`, `calendar`, "MOVE FAST" snail poster) | Both films |
| Mount Staedean | `sets.big_mountain` | Through the office window. 20,000 m. Both films. |
| Checkpoint ledge | `sets.ledge` | Film 1 |
| The slope | `sets.slope` | Film 1 |
| The fork | `sets.fork_set` | Film 1 |
| The summit | `sets.summit_set` | Film 1 |
| The path to the customer | `film2.path_set` | Film 2. 20 m long, sunny, a parasol and a table. |
| The shop | `film2` shot `S1_now_open` | Film 2 |

---

## Brand colours

![Brand](../assets/sheets/08_brand.png)

STAEDEAN colours are used sparingly and only in these places, so they feel like a wink rather than an advert.

| Colour | Hex | Used for |
|---|---|---|
| Tangerine Orange | `#FF9C46` | PM tie |
| Miami Teal | `#17C8BE` | Checkpoint roofs, summit flag, PM mug, oxygen tank, the door, shop awning, the logo |
| Sapphire Blue | `#00316C` | Customer jacket |
| Galaxy Black | `#1F2342` | PM trousers, office chair, displays |
| Beige | `#D7BA94` | Office floor |
| Pink | `#FF95D2` | QA official |
| Purple | `#6749C9` | Product Owner |
| Dark teal | `#008C94` | Customer Success |

The rig draws in a neutral base palette. `src/rb.py` maps base colours to the final ones (`CMAP`), and the colours that must stay strong under the marker texture are listed in `BRAND_STRONG`. To recolour something for every film at once, change the map, not the drawing.

## The logo

`assets/logo/staedean_logo_clean.svg` is the vector, traced from the brand logo. `src/logo_path.py` holds the same path for code. In the films it is drawn in the house style: teal fill slightly offset, broken pen outline, a string of lit bulbs above.
