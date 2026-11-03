"""'90s TV-cartoon look: thin scratchy black line on off-white paper, almost no colour.
The idea bulb is the only thing that glows; a couple of small red-orange accents stay (tie, calendar).
Works on any frame the rig draws, so continuity carries over unchanged."""
import re, colorsys
from rig import W, H, defs

PAPER = "#fbf8f0"
INK = "#1f1a17"


def _keep(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h *= 360
    if (h < 22 or h > 345) and s > 0.45 and v > 0.5:      # red-orange accents
        return True
    if 38 < h < 65 and s > 0.35 and v > 0.93:              # bulb yellows
        return True
    return False


def _fill(m):
    col = m.group(1)
    if _keep(col):
        return f'fill="{col}"'
    r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return f'fill="{INK}"' if lum < 0.28 else f'fill="{PAPER}"'


def _stroke(m):
    col = m.group(1)
    if col.lower() in ("#ffffff", "#fffdf6", PAPER) or _keep(col):
        return f'stroke="{col}"'
    r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return f'stroke="{INK}"' if lum < 0.75 else f'stroke="{PAPER}"'


def stylize(art):
    art = art.replace('filter="url(#wc)"', "")
    art = art.replace('fill="url(#skyG)"', f'fill="{PAPER}"')
    art = re.sub(r'fill="(#[0-9a-fA-F]{6})"', _fill, art)
    # thick strokes are limbs (filled tubes): colour them like fills; thin strokes are lines
    def _pair(m):
        col, w = m.group(1), float(m.group(2))
        if w > 14:
            fm = _fill(re.match(r'(#[0-9a-fA-F]{6})', col)) if False else None
            r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
            lum = 0.299 * r + 0.587 * g + 0.114 * b
            new = col if _keep(col) else (INK if lum < 0.28 else PAPER)
            return f'stroke="{new}" stroke-width="{m.group(2)}"'
        return _stroke(m) + f' stroke-width="{m.group(2)}"'
    art = re.sub(r'stroke="(#[0-9a-fA-F]{6})" stroke-width="([0-9.]+)"', _pair, art)
    art = re.sub(r'stroke="(#[0-9a-fA-F]{6})"(?! stroke-width)', _stroke, art)
    art = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) * 0.72:.2f}"', art)
    # soft shading shapes become invisible paper-on-paper; drop them to keep the page clean
    art = re.sub(r'<path d="[^"]*" fill="#fbf8f0" opacity="0\.[0-9]+"/>', "", art)
    return art


def overlay():
    return (f'<rect width="{W}" height="{H}" filter="url(#grain)" style="mix-blend-mode:multiply" opacity="0.18"/>'
            f'<rect width="{W}" height="{H}" fill="url(#vig)" opacity="0.45"/>')


def wrap_rb(art, view=None, seed=7):
    vb = view or (0, 0, W, H)
    z = W / vb[2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">'
            + defs(seed, z) + f'<rect x="-500" y="-500" width="4000" height="3000" fill="{PAPER}"/>'
            + f'<g filter="url(#wobble)">{stylize(art)}</g>'
            + f'<g transform="translate({vb[0]},{vb[1]}) scale({vb[2] / W},{vb[3] / H})">{overlay()}</g></svg>')


# ======================= colour pass =======================
# Basic flat colours under the same black line, with STAEDEAN brand colours tucked into smart places:
#   tie = Tangerine Orange, trousers & chair = Galaxy Black, mug & checkpoint roofs & summit flag = Miami Teal,
#   customer = Sapphire Blue, floor = brand beige, officials in the supporting colours,
#   and an orange-and-teal sky at the summit (the brand's photo grading).
import os
STYLE = os.environ.get("MS_STYLE", "line")
TEAL, SAPPHIRE, TANGERINE, GALAXY = "#17C8BE", "#00316C", "#FF9C46", "#1F2342"
PINK, BEIGE, PURPLE, DTEAL, SIGNAL = "#FF95D2", "#D7BA94", "#6749C9", "#008C94", "#FA5A4F"
CMAP = {
    # the PM
    "#b9d3e6": "#c3e2f4", "#9dbcd4": "#a3cbe6", "#c0623a": TANGERINE, "#9c4a2b": "#e27c25",
    "#f0c9a6": "#f7d3b4", "#eeb796": "#f4c3a3", "#7b4b2b": "#8c5630", "#3a3a40": GALAXY,
    # office
    "#e4d5bb": "#f5e9d2", "#d3c09f": "#ead8b6", "#c4ab88": BEIGE, "#5d5753": GALAXY, "#6fa39c": TEAL,
    "#b8483a": SIGNAL, "#7f8a8c": DTEAL, "#d3e3ec": "#cdeeed",
    "#9ea6aa": "#aebccb", "#858d92": "#8e9fb2", "#b4bbbe": "#c4d0dc",
    # outdoors
    "#cfe0ea": "#c4ece8", "#eef1ea": "#fdf1e2", "#b9c6b0": "#b3d9a8", "#a9b394": "#97c486",
    "#b7c0c4": "#bfd0db", "#b8a888": "#d3bb93", "#a99c80": "#cdb790",
    "#b9d6ea": "#9fe0da", "#f3efe4": "#ffcf9e",
    # checkpoints
    "#cdb58e": "#e8cfa3", "#9c5b3c": TEAL, "#3a3a3c": GALAXY, "#ff6a3a": TANGERINE,
    "#8a6f9c": PINK, "#5f8f7c": DTEAL, "#c99a3e": PURPLE, "#6d7f9c": "#3d6fb0",
    # customer, flag, fork, ascent
    "#4f7a5c": SAPPHIRE, "#c0623b": TEAL,
    "#5d7f8e": DTEAL, "#4f6f80": "#007780", "#86a6b4": "#5fd6cf", "#56788a": "#2d86a8",
    "#7c9a74": TEAL, "#2e2520": "#1f1a17",
}


def colourize(art):
    art = art.replace('filter="url(#wc)"', "")

    def rep(m):
        return f'{m.group(1)}="{CMAP.get(m.group(2).lower(), m.group(2))}"'
    art = re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6})"', rep, art)
    art = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) * 0.72:.2f}"', art)
    return art


_stylize_line = stylize


def stylize(art):  # noqa: F811
    return colourize(art) if STYLE == "colour" else _stylize_line(art)


# ======================= marker pass (felt-tip colouring, broken pen line) =======================
WHITE = "#fdfcf8"


def _lighten(col, k):
    r, g, b = (int(col[i:i + 2], 16) for i in (1, 3, 5))
    return "#" + "".join(f"{int(v + (255 - v) * k):02x}" for v in (r, g, b))


def _lum(col):
    r, g, b = (int(col[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.299 * r + 0.587 * g + 0.114 * b


def marker_defs(z):
    return f'''<defs>
  <filter id="mk" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB">
    <feComponentTransfer in="SourceGraphic" result="pastel">
      <feFuncR type="linear" slope="0.25" intercept="0.75"/><feFuncG type="linear" slope="0.25" intercept="0.75"/><feFuncB type="linear" slope="0.25" intercept="0.75"/>
    </feComponentTransfer>
    <feMorphology in="SourceAlpha" operator="erode" radius="{9 / z:.2f}" result="er"/>
    <feOffset in="er" dx="{-7 / z:.2f}" dy="{-6 / z:.2f}" result="ero"/>
    <feGaussianBlur in="ero" stdDeviation="{7 / z:.2f}" result="erob"/>
    <feComposite in="SourceAlpha" in2="erob" operator="out" result="ring"/>
    <feComposite in="SourceGraphic" in2="ring" operator="in" result="shade"/>
    <feTurbulence type="fractalNoise" baseFrequency="{0.006 * z:.4f} {0.11 * z:.4f}" numOctaves="2" seed="5" result="st"/>
    <feColorMatrix in="st" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1.8 -0.55" result="sta"/>
    <feComposite in="SourceGraphic" in2="sta" operator="in" result="streak"/>
    <feComposite in="streak" in2="SourceAlpha" operator="in" result="streakc"/>
    <feColorMatrix in="shade" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.9 0" result="shadeA"/>
    <feColorMatrix in="streakc" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.12 0" result="streakA"/>
    <feMerge><feMergeNode in="pastel"/><feMergeNode in="streakA"/><feMergeNode in="shadeA"/></feMerge>
  </filter>
  <filter id="mk2" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB">
    <feComponentTransfer in="SourceGraphic" result="pastel">
      <feFuncR type="linear" slope="0.62" intercept="0.38"/><feFuncG type="linear" slope="0.62" intercept="0.38"/><feFuncB type="linear" slope="0.62" intercept="0.38"/>
    </feComponentTransfer>
    <feMorphology in="SourceAlpha" operator="erode" radius="{9 / z:.2f}" result="er"/>
    <feOffset in="er" dx="{-7 / z:.2f}" dy="{-6 / z:.2f}" result="ero"/>
    <feGaussianBlur in="ero" stdDeviation="{7 / z:.2f}" result="erob"/>
    <feComposite in="SourceAlpha" in2="erob" operator="out" result="ring"/>
    <feComposite in="SourceGraphic" in2="ring" operator="in" result="shade"/>
    <feMerge><feMergeNode in="pastel"/><feMergeNode in="shade"/></feMerge>
  </filter>
</defs>'''


DASH = 'stroke-dasharray="150 7 70 5 110 6"'
BRAND_STRONG = {TANGERINE.lower(), TEAL.lower(), SAPPHIRE.lower(), "#e27c25"}


def markerize(art):
    # brand colour choices first
    art = re.sub(r'(fill|stroke|stop-color)="(#[0-9a-fA-F]{6})"', lambda m: f'{m.group(1)}="{CMAP.get(m.group(2).lower(), m.group(2))}"', art)
    # coloured shapes the rig drew with a watercolour wash -> felt-tip marker fill
    art = art.replace('filter="url(#wc)"', 'filter="url(#mk)"')
    MK = "\x00MK\x00"
    art = art.replace('filter="url(#mk)"', MK)

    def fill_rep(m):
        tag = m.group(0)
        col = m.group(1)
        return tag
    # flat (non-marker) fills: lighten for the airy white-paper look, but keep ink, white and the bulb
    def flat_fill(m):
        col = m.group(1)
        if _lum(col) < 0.2 or _keep(col) and 38 < colorsys.rgb_to_hsv(*[int(col[i:i + 2], 16) / 255 for i in (1, 3, 5)])[0] * 360 < 65:
            return m.group(0)
        return f'fill="{_lighten(col, 0.6)}"'
    parts = re.split(r'(<[^>]+>)', art)
    out = []
    for p in parts:
        if p.startswith("<") and MK not in p and ("<path" in p or "<rect" in p or "<ellipse" in p or "<circle" in p):
            p = re.sub(r'fill="(#[0-9a-fA-F]{6})"', flat_fill, p)
        if p.startswith("<text"):
            p = re.sub(r'fill="(#[0-9a-fA-F]{6})"', lambda m: 'fill="#1f1a17"' if _lum(m.group(1)) > 0.8 else m.group(0), p)
        if p.startswith("<stop"):
            p = re.sub(r'stop-color="(#[0-9a-fA-F]{6})"', lambda m: f'stop-color="{_lighten(m.group(1), 0.45)}"', p)
        if p.startswith("<path"):
            m = re.search(r'stroke="(#[0-9a-fA-F]{6})" stroke-width="([0-9.]+)"', p)
            if m:
                col, w = m.group(1).lower(), float(m.group(2))
                if col == "#1f1a17":
                    p = p.replace("/>", f" {DASH}/>", 1) if "dasharray" not in p else p
                elif w > 14:          # limb colour: same pale marker tone as the body
                    k = 0.35 if col in BRAND_STRONG else 0.75
                    p = p.replace(m.group(0), f'stroke="{_lighten(col, k)}" stroke-width="{m.group(2)}"', 1)
        out.append(p)
    art = "".join(out)
    # brand colours get a stronger marker so they read on screen
    art = re.sub(r'fill="(#[0-9a-fA-F]{6})"([^>]*?)\x00MK\x00', lambda m: f'fill="{m.group(1)}"{m.group(2)}' + ('filter="url(#mk2)"' if m.group(1).lower() in BRAND_STRONG else MK), art)
    art = art.replace(MK, 'filter="url(#mk)"')
    # rosier cheeks, like the old ads
    art = art.replace('opacity="0.35" filter="url(#soft)"', 'opacity="0.7" filter="url(#soft)"')
    art = re.sub(r'stroke-width="([0-9.]+)"', lambda m: f'stroke-width="{float(m.group(1)) * 0.68:.2f}"', art)
    return art


def stylize(art):  # noqa: F811
    if STYLE == "marker":
        return markerize(art)
    return colourize(art) if STYLE == "colour" else _stylize_line(art)


_wrap_rb_base = wrap_rb


def wrap_rb(art, view=None, seed=7):  # noqa: F811
    if STYLE == "brush":
        from brush_style import wrap
        return wrap(art, view, seed, CMAP)
    if STYLE == "wash":
        # Optional colour study; keeps the established marker film unchanged.
        from wash_style import wrap
        return wrap(art, view, seed, CMAP)
    if STYLE != "marker":
        return _wrap_rb_base(art, view, seed)
    vb = view or (0, 0, W, H)
    z = W / vb[2]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}">'
            + defs(seed, z) + marker_defs(z) + f'<rect x="-500" y="-500" width="4000" height="3000" fill="{WHITE}"/>'
            + f'<g filter="url(#wobble)">{stylize(art)}</g>'
            + f'<g transform="translate({vb[0]},{vb[1]}) scale({vb[2] / W},{vb[3] / H})">'
            + f'<rect width="{W}" height="{H}" filter="url(#grain)" style="mix-blend-mode:multiply" opacity="0.10"/></g></svg>')
