# The Door: ink-and-wash colour study

The reference suggests white paper, richer local colour, broad translucent-looking highlights and fine ink contours. This study applies those qualities to three existing frames while retaining their exact staging and character geometry.

The new treatment is optional. The existing MP4 films have not been recoloured. `rb.py` dispatches the new `wash` style to `wash_style.py`; the existing `marker` branch remains unchanged. `wash_style.py` holds the palette, colour gradients, stable pigment texture and line treatment. Opaque base colour prevents background objects showing through characters. Stroke-only limbs use solid midtones because their zero-width path bounds can make SVG filters clip the artwork.

To reproduce the comparison, run `work/colour-study/render.py` using the established animation environment. It renders identical frames with `rb.STYLE` set to `marker` and `wash`. To change the proposed palette, edit `PALETTE` in `wash_style.py`; gradient highlight strengths control how much white shows within coloured shapes.

The three comparisons were rendered and visually checked, including hands and limb boundaries. Motion has not yet been checked in this treatment. The current film renderer explicitly selects marker style, so a full-film wash render requires deliberately selecting the new style and using a fresh frame cache.

This is a colouring study. The reference's more irregular hand-drawn shapes and individually placed brushwork are not reproduced by changing colour alone.

## Second study: overlapping brush washes

The optional `brush` style routes from `rb.py` to `brush_style.py`. It replaces smooth radial fills with overlapping, asymmetric brush footprints, darker overlaps and selective white reserves. A seeded edge filter softens and roughens the paint independently of the ink. Skin receives a quieter treatment. Each shape has opaque paper underneath so a white gap does not reveal objects behind the character. Stroke-only limbs use explicit bounds that include their rounded ends.

`work/colour-study/brush-frame.py` renders the same customer drawing in the previous wash and new brush styles. The new still and comparison were visually inspected; no full-film render or motion approval is implied. This remains a procedural approximation of painted washes, with more regular character geometry than the supplied reference. The existing marker film exports are unchanged.
