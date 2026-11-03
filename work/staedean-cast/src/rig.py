"""MOUNT STAEDEAN - reusable drawing rig.

Every frame is built from the same parts. The PM is one puppet with dials
(pose, expression, beard, bulb brightness). Each location is a fixed set.
Nothing is redrawn from scratch per frame, so continuity holds by construction.
"""
import math

W, H = 1920, 1080

# ---------- palette (muted watercolour) ----------
C = dict(
    paper="#f2e8d5", ink="#2e2520", wall="#e4d5bb", wall_dark="#d3c09f",
    floor="#c4ab88", skin="#f0c9a6", skin_shade="#e2ae8a", nose="#eeb796",
    blush="#e79b86", hair="#7b4b2b", hair_dark="#5e3820", shirt="#b9d3e6",
    shirt_shade="#9dbcd4", tie="#c0623a", tie_dark="#9c4a2b", trousers="#3a3a40",
    shoes="#6b4426", desk="#b98a5e", desk_dark="#9a6f47", chair="#5d5753",
    sky="#d3e3ec", mountain="#9ea6aa", mountain_dark="#858d92", snow="#f4f1ea",
    bulb_off="#efece2", bulb_on="#ffe07a", glow="#ffd659", metal="#a9a49b",
    mug="#6fa39c", paper_sheet="#fbf7ee", bin="#7f8a8c", beard="#6b4228",
    beard_grey="#b9b3aa", cal_red="#b8483a",
)

INK = C["ink"]


def f(x):
    return f"{x:.1f}"


def path(d, fill="none", stroke=INK, sw=3.5, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def washed(d, fill, sw=3.5, off=(4, 3), stroke=INK):
    """Watercolour fill printed slightly off-register, then the ink line on top."""
    return (f'<path d="{d}" fill="{fill}" transform="translate({off[0]},{off[1]})" filter="url(#wc)"/>'
            + path(d, sw=sw, stroke=stroke))


def tube(pts, width, fill, sw=3.5):
    """Outlined limb: thick ink stroke underneath, colour stroke on top."""
    d = "M " + " L ".join(f"{f(x)},{f(y)}" for x, y in pts)
    return (path(d, stroke=INK, sw=width + sw * 2)
            + path(d, stroke=fill, sw=width))


def lerp(a, b, t):
    return a + (b - a) * t


def lerp2(p, q, t):
    return (lerp(p[0], q[0], t), lerp(p[1], q[1], t))


# ---------- defs: paper, ink wobble, watercolour ----------
def defs(seed=7, z=1.0):
    return f'''
<defs>
  <filter id="wobble" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="{0.032 * z:.4f}" numOctaves="2" seed="{seed}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="{5 / z:.3f}" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="2"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.55 0"/>
  </filter>
  <filter id="blotch" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.006 0.009" numOctaves="4" seed="11"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.45  0 0 0 0 0.35  0 0 0 0.9 -0.25"/>
  </filter>
  <filter id="wc" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="{0.018 * z:.4f}" numOctaves="3" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0.9 0.9 0 0 -0.55" result="na"/>
    <feFlood flood-color="#5a3f28" flood-opacity="0.32"/>
    <feComposite in2="na" operator="in" result="blot"/>
    <feComposite in="blot" in2="SourceAlpha" operator="in" result="blotc"/>
    <feMorphology in="SourceAlpha" operator="erode" radius="{4 / z:.3f}" result="er"/>
    <feComposite in="SourceAlpha" in2="er" operator="out" result="ring"/>
    <feGaussianBlur in="ring" stdDeviation="{1.5 / z:.3f}" result="ringb"/>
    <feFlood flood-color="#3a2614" flood-opacity="0.22"/>
    <feComposite in2="ringb" operator="in" result="edge"/>
    <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="blotc"/><feMergeNode in="edge"/></feMerge>
  </filter>
  <filter id="bloom" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="{18 / z:.3f}"/>
  </filter>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="{6 / z:.3f}"/>
  </filter>
  <radialGradient id="glowG">
    <stop offset="0" stop-color="{C['glow']}" stop-opacity="0.95"/>
    <stop offset="0.35" stop-color="{C['glow']}" stop-opacity="0.45"/>
    <stop offset="1" stop-color="{C['glow']}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="vig" cx="50%" cy="48%" r="70%">
    <stop offset="0.6" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#3a2a18" stop-opacity="0.28"/>
  </radialGradient>
</defs>'''


def paper_overlay():
    return (f'<rect width="{W}" height="{H}" filter="url(#blotch)" style="mix-blend-mode:multiply" opacity="0.35"/>'
            f'<rect width="{W}" height="{H}" filter="url(#grain)" style="mix-blend-mode:multiply" opacity="0.35"/>'
            f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')


# ---------- the idea bulb ----------
def bulb(x, y, s=1.0, b=1.0, rot=0, rays=None, pop=False, dead=False):
    """Light bulb centred on its glass. b = brightness 0..1. At 1.0 it blazes; it only ever fades from there."""
    glass = C["bulb_off"] if b < 0.05 else _mix(C["bulb_off"], C["bulb_on"], min(1, b * 1.25))
    if b > 0.7:
        glass = _mix(glass, "#fffbe6", (b - 0.7) / 0.3 * 0.75)
    if dead:
        glass = "#cfcac0"
    fil = "#8a7f72" if b < 0.2 else _mix("#c7863a", "#ff5a10", b)
    out = []
    if b > 0.05 and not dead:
        if b > 0.3:  # light spilling onto everything around it
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(760 * b * s)}" fill="url(#glowG)" opacity="{f(0.42 * b)}" '
                       f'style="mix-blend-mode:screen"/>')
        r = 80 + 340 * b
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * s)}" fill="url(#glowG)" opacity="{f(min(1, 0.12 + 0.95 * b))}"/>')
    g = []
    gd = ("M -22,26 C -24,12 -36,4 -36,-14 C -36,-36 -20,-48 0,-48 "
          "C 20,-48 36,-36 36,-14 C 36,4 24,12 22,26 Z")
    g.append(washed(gd, glass, sw=3.2, off=(2, 2)))
    if b > 0.45 and not dead:  # white-hot core
        g.append(f'<ellipse cx="0" cy="-10" rx="{f(12 + 18 * b)}" ry="{f(14 + 20 * b)}" fill="#ffffff" opacity="{f((b - 0.45) * 1.6)}" filter="url(#soft)"/>')
    # filament
    g.append(path("M -10,24 L -8,4 C -6,-6 -2,-6 0,2 C 2,-6 6,-6 8,4 L 10,24", stroke=fil, sw=2.6))
    # highlight
    g.append(path("M -22,-26 C -18,-36 -10,-40 -4,-41", stroke="#ffffff", sw=4))
    # screw base
    g.append(washed("M -22,26 L 22,26 L 20,48 L -20,48 Z", C["metal"], sw=3, off=(2, 1)))
    g.append(path("M -21,33 L 21,33 M -20,41 L 20,41", sw=2.2))
    g.append(washed("M -12,48 L 12,48 L 7,56 L -7,56 Z", "#6e6a63", sw=2.6, off=(1, 1)))
    if dead:
        g.append(path("M -12,-20 L -4,-12 M -4,-20 L -12,-12 M 4,-20 L 12,-12 M 12,-20 L 4,-12", sw=2.4))
    out.append(f'<g transform="translate({f(x)},{f(y)}) rotate({rot}) scale({s})">{"".join(g)}</g>')
    # rays scale with brightness: a blazing starburst at 1.0, gone by about 0.35
    if rays is None or rays > 0:
        nr = 0 if b < 0.35 else int(3 + 10 * b)
    else:
        nr = 0
    for i in range(nr):
        a = math.radians(-90 + (i - (nr - 1) / 2) * (330 / max(nr, 1)))
        r1, r2 = 64 * s, (72 + 70 * b * (1.0 if i % 2 else 0.7)) * s
        out.append(path(f"M {f(x + r1 * math.cos(a))},{f(y + r1 * math.sin(a))} "
                        f"L {f(x + r2 * math.cos(a))},{f(y + r2 * math.sin(a))}", sw=2.5 + 3 * b, stroke=_mix("#c98a1e", "#ffb21a", b)))
    if pop:
        for a in (-150, -30, -110, -70):
            ar = math.radians(a)
            out.append(path(f"M {f(x + 58 * math.cos(ar))},{f(y + 58 * math.sin(ar))} "
                            f"L {f(x + 72 * math.cos(ar))},{f(y + 72 * math.sin(ar))}", sw=2.4))
    return "".join(out)


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(lerp(p, q, t)):02x}" for p, q in zip(a, b))


# ---------- the PM ----------
# Fixed design: tousled brown hair, big nose, pale-blue shirt with rolled sleeves,
# rust-orange tie, charcoal trousers, brown shoes. Beard is a dial (0 = clean-shaven).

BROWS = {
    "neutral": [("M -22,-46 C -10,-52 6,-52 18,-46", "M 40,-52 C 50,-56 60,-55 68,-50")],
    "raised":  [("M -22,-60 C -10,-70 6,-70 18,-62", "M 40,-66 C 50,-72 60,-71 68,-64")],
    "furrow":  [("M -22,-50 C -8,-52 6,-48 18,-42", "M 40,-44 C 50,-50 60,-54 68,-54")],
    "quizzical": [("M -22,-48 C -10,-52 6,-50 18,-45", "M 40,-64 C 50,-72 60,-71 68,-64")],
    "happy":   [("M -22,-54 C -10,-62 6,-62 18,-55", "M 40,-58 C 50,-64 60,-63 68,-57")],
    "sad":     [("M -22,-44 C -10,-48 4,-56 16,-62", "M 40,-62 C 48,-58 58,-50 68,-46")],
    "weary":   [("M -24,-42 C -12,-46 4,-48 18,-50", "M 40,-50 C 50,-48 60,-44 68,-40")],
}

MOUTHS = {
    "neutral": "M 30,72 C 42,74 54,73 62,70",
    "hmm":     "M 30,74 C 38,70 46,76 54,72 C 58,70 61,71 63,72",
    "smile":   "M 26,66 C 36,80 54,80 64,66",
    "flat":    "M 32,72 L 60,72",
    "frown":   "M 28,78 C 38,66 52,66 62,76",
    "wobbly":  "M 28,74 C 34,70 38,78 44,72 C 50,68 54,78 62,72",
    "tiny":    "M 40,73 L 52,73",
}


def head(look=(0, 0), brows="neutral", mouth="neutral", eyes="open", beard=0.0, grey=0.0, mask=False, beard_wind=None):
    """Head in local coords (origin ~ centre of skull). Faces 3/4 to screen-right."""
    g = []
    skull = ("M -10,-112 C 60,-116 96,-62 92,-6 C 90,48 70,96 26,106 "
             "C -28,114 -82,82 -94,22 C -102,-40 -76,-108 -10,-112 Z")
    g.append(washed(skull, C["skin"], off=(4, 3)))
    # soft shading on the back of the head
    g.append('<path d="M -94,22 C -100,-30 -80,-90 -40,-106 C -70,-70 -76,-10 -60,60 Z" '
             f'fill="{C["skin_shade"]}" opacity="0.55"/>')
    # ear
    g.append(washed("M -86,-16 C -118,-26 -124,24 -104,42 C -96,50 -86,44 -84,36", C["skin"], off=(3, 2)))
    g.append(path("M -100,0 C -108,6 -106,22 -98,26", sw=2.4))
    # cheek blush
    g.append(f'<ellipse cx="6" cy="34" rx="20" ry="12" fill="{C["blush"]}" opacity="0.35" filter="url(#soft)"/>')
    # beard (grows from the jaw)
    if beard > 0:
        if beard_wind is None:
            g.append(_beard(beard, grey))
        else:
            from wind_beard import draw
            g.append(draw(grey, **beard_wind))
    # mouth
    if mouth == "grin":
        g.append(washed("M 22,62 C 34,92 60,92 70,60 C 54,68 36,68 22,62 Z", "#7a2f25", sw=3, off=(1, 1)))
        g.append('<path d="M 25,64 C 38,70 56,70 68,62 L 66,70 C 54,76 38,76 28,71 Z" fill="#fffaf0"/>')
    elif mouth == "talk":
        g.append(washed("M 24,62 C 30,96 62,96 68,62 C 54,66 38,66 24,62 Z", "#7a2f25", sw=3, off=(1, 1)))
        g.append('<path d="M 34,86 C 42,80 52,80 58,86 C 52,92 40,92 34,86 Z" fill="#c25a4a"/>')
    elif mouth == "o":
        g.append(washed("M 40,66 C 34,66 34,82 42,82 C 50,82 50,66 40,66 Z", "#7a2f25", sw=3, off=(1, 1)))
    else:
        g.append(path(MOUTHS[mouth], sw=3.2))
    # eyes
    lx, ly = look
    for ex, ey, rx, ry in ((2, -22, 13, 16), (54, -26, 10, 15)):
        if eyes == "closed":
            g.append(path(f"M {ex - rx},{ey} C {ex - rx / 2},{ey + 6} {ex + rx / 2},{ey + 6} {ex + rx},{ey}", sw=3.2))
            continue
        if eyes == "closed_happy":
            g.append(path(f"M {ex - rx},{ey + 2} C {ex - rx / 2},{ey - 10} {ex + rx / 2},{ey - 10} {ex + rx},{ey + 2}", sw=3.2))
            continue
        g.append(washed(f"M {ex - rx},{ey} C {ex - rx},{ey - ry * 1.3} {ex + rx},{ey - ry * 1.3} {ex + rx},{ey} "
                        f"C {ex + rx},{ey + ry * 1.3} {ex - rx},{ey + ry * 1.3} {ex - rx},{ey} Z", "#fffdf6", sw=2.6, off=(0, 0)))
        ly_ = max(ly, -0.1) if eyes in ("half", "tired") else ly   # keep pupils below heavy lids
        g.append(f'<circle cx="{f(ex + lx * rx * 0.4)}" cy="{f(ey + ly_ * ry * 0.42 + (ry * 0.25 if eyes in ("half", "tired") else 0))}" r="{f(rx * 0.58)}" fill="{INK}"/>')
        if eyes in ("tired", "half"):
            g.append(path(f"M {ex - rx + 2},{ey + ry + 4} C {ex - rx / 2},{ey + ry + 10} {ex + rx / 2},{ey + ry + 10} {ex + rx - 2},{ey + ry + 4}", sw=2, stroke="#8a6a5a"))
        if eyes == "wide":
            g.append(f'<circle cx="{f(ex + lx * rx * 0.45)}" cy="{f(ey + ly * ry * 0.45)}" r="{f(rx * 0.22)}" fill="#fffdf6"/>')
        if eyes in ("half", "tired"):
            g.append(f'<path d="M {ex - rx - 1},{ey - ry * 0.3:.1f} C {ex - rx},{ey - ry * 1.4} {ex + rx},{ey - ry * 1.4} {ex + rx + 1},{ey - ry * 0.3:.1f} Z" fill="{C["skin_shade"]}" stroke="{INK}" stroke-width="2.6"/>')
    # brows
    for d in BROWS[brows][0]:
        g.append(path(d, sw=5, stroke=C["hair_dark"]))
    # the nose (normal size)
    if not mask:
        nose = "M 66,-24 C 72,-4 86,14 92,28 C 96,38 88,44 78,42 C 74,46 68,44 66,40"
        g.append(washed(nose + " C 70,20 70,0 66,-24 Z", C["nose"], off=(2, 2)))
        g.append(path(nose))
        g.append(path("M 76,36 C 79,40 84,40 86,37", sw=2.2))
    # hair (tousled)
    hair = ("M -96,8 C -112,-30 -100,-70 -78,-92 C -84,-110 -60,-128 -40,-118 "
            "C -32,-140 0,-142 10,-124 C 22,-144 56,-136 58,-114 C 78,-122 100,-100 88,-80 "
            "C 104,-72 98,-52 84,-50 C 76,-62 62,-70 48,-70 C 52,-82 40,-90 30,-84 "
            "C 20,-96 0,-92 -6,-80 C -22,-90 -44,-80 -44,-62 C -62,-60 -70,-40 -66,-22 "
            "C -76,-30 -88,-20 -82,-6 Z")
    g.append(washed(hair, C["hair"], off=(4, 3)))
    g.append(path("M -60,-96 C -50,-104 -36,-104 -26,-98 M 4,-112 C 14,-118 30,-118 38,-110 "
                  "M -84,-60 C -78,-70 -70,-74 -60,-74", sw=2.4, stroke=C["hair_dark"]))
    if mask:
        g.append(washed("M 40,-6 C 70,-14 104,6 104,34 C 104,66 76,84 50,80 C 30,76 24,40 40,-6 Z", "#cfe3e0", off=(2, 2)))
        g.append(path("M 30,10 L -70,0 M 34,64 L -66,40", sw=2.4))
        g.append(washed("M 92,40 C 106,34 120,42 118,56 C 116,68 100,70 92,62 Z", "#9fbcb8", sw=2.6, off=(1, 1)))
    return "".join(g)


def _beard(L, grey):
    col = _mix(C["beard"], C["beard_grey"], grey)
    if L < 0.08:  # stubble
        dots = []
        import random
        rnd = random.Random(5)
        for _ in range(int(140 * L / 0.08)):
            x = rnd.uniform(-60, 80); y = rnd.uniform(30, 104)
            if (x + 10) ** 2 / 90 ** 2 + (y - 40) ** 2 / 75 ** 2 < 1 and not (20 < x < 70 and 55 < y < 85):
                dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="1.6" fill="{INK}" opacity="0.55"/>')
        return "".join(dots)
    drop = L * 660
    sway = L * 30
    wid = 1 + L * 0.25
    bot = 110 + drop
    if L <= 0.4:
        d = (f"M -82,30 C {f(-96 * wid)},{f(70 + drop * 0.35)} {f(-60 * wid)},{f(80 + drop * 0.8)} {f(10 - sway)},{f(bot)} "
             f"C {f(80 * wid - sway)},{f(80 + drop * 0.8)} {f(104 * wid)},{f(60 + drop * 0.35)} 90,40 "
             f"C 80,62 70,66 62,66 C 50,70 40,68 34,64 C 16,64 -30,60 -60,36 Z")
    else:  # long beard: tapers like a wizard's
        d = (f"M -82,30 C -104,{f(90 + drop * 0.12)} -60,{f(60 + drop * 0.55)} {f(10 - sway)},{f(bot)} "
             f"C {f(70 - sway)},{f(60 + drop * 0.55)} 116,{f(90 + drop * 0.12)} 90,40 "
             f"C 80,62 70,66 62,66 C 50,70 40,68 34,64 C 16,64 -30,60 -60,36 Z")
    out = washed(d, col, off=(4, 3))
    strands = []
    for i, x0 in enumerate((-50, -20, 10, 40, 66)):
        y1 = 110 + drop * (0.5 + 0.12 * (i % 3))
        tx = x0 * 0.45 + 10 - sway
        strands.append(f"M {x0},{90 + i * 3} C {x0},{f(100 + drop * 0.3)} {f(tx)},{f(100 + drop * 0.4)} {f(tx)},{f(y1)}")
    out += path(" ".join(strands), sw=1.8, stroke=_mix(col, INK, 0.45))
    if L > 0.2:  # moustache
        out += washed("M 40,52 C 52,46 70,46 82,52 C 86,60 76,64 70,58 C 64,64 54,64 50,58 C 44,64 34,62 40,52 Z", col, sw=2.6, off=(2, 1))
    return out


def pm(x, y, *, head_rot=0, look=(0, 0), brows="neutral", mouth="neutral", eyes="open",
       arms="writing", beard=0.0, grey=0.0, slump=0.0, bulb_b=0.0, extras=None, mask=False, beard_wind=None):
    """Seated PM, upper body, behind a desk. (x, y) = base of neck."""
    g = []
    sy = slump * 30
    # torso
    torso = (f"M {x - 140},{y + 40 + sy} C {x - 150},{y + 120} {x - 160},{y + 220} {x - 160},{y + 320} "
             f"L {x + 165},{y + 320} C {x + 160},{y + 220} {x + 152},{y + 120} {x + 140},{y + 38 + sy} "
             f"C {x + 90},{y + 6 + sy} {x - 90},{y + 6 + sy} {x - 140},{y + 40 + sy} Z")
    g.append(washed(torso, C["shirt"], off=(5, 3)))
    g.append(f'<path d="M {x + 60},{y + 30} C {x + 130},{y + 60} {x + 150},{y + 200} {x + 160},{y + 320} L {x + 110},{y + 320} C {x + 110},{y + 200} {x + 90},{y + 90} {x + 60},{y + 30} Z" fill="{C["shirt_shade"]}" opacity="0.6"/>')
    # neck
    g.append(washed(f"M {x - 30},{y - 40} L {x - 34},{y + 20} L {x + 36},{y + 20} L {x + 34},{y - 40} Z", C["skin"], off=(2, 2)))
    g.append(f'<path d="M {x - 30},{y - 10} L {x + 34},{y - 10} L {x + 36},{y + 20} L {x - 34},{y + 20} Z" fill="{C["skin_shade"]}" opacity="0.6"/>')
    # placket + tie
    g.append(path(f"M {x + 8},{y + 30} L {x + 4},{y + 320}", sw=2.4))
    tie = (f"M {x - 8},{y + 36} L {x + 24},{y + 36} L {x + 32},{y + 200} L {x + 10},{y + 236} L {x - 14},{y + 200} Z")
    g.append(washed(tie, C["tie"], off=(3, 2)))
    g.append(f'<path d="M {x + 12},{y + 60} L {x + 30},{y + 200} L {x + 10},{y + 236} Z" fill="{C["tie_dark"]}" opacity="0.4"/>')
    g.append(washed(f"M {x - 12},{y + 14} L {x + 28},{y + 14} L {x + 24},{y + 40} L {x - 8},{y + 40} Z", C["tie"], off=(2, 2)))
    # collar
    g.append(washed(f"M {x - 40},{y + 4} L {x - 6},{y + 22} L {x - 20},{y + 60} L {x - 56},{y + 20} Z", "#e3eef6", off=(2, 2)))
    g.append(washed(f"M {x + 44},{y + 4} L {x + 22},{y + 22} L {x + 40},{y + 60} L {x + 62},{y + 20} Z", "#e3eef6", off=(2, 2)))
    body = "".join(g)

    hx, hy = x + 6, y - 110
    hd = f'<g transform="translate({hx},{hy + sy}) rotate({head_rot},0,110)">' + \
         head(look, brows, mouth, eyes, beard, grey, mask, beard_wind) + '</g>'
    return body, hd, (x, y + sy)


def arm(shoulder, elbow, hand, hand_shape="rest", flip=False):
    """Rolled-sleeve arm. Sleeve covers shoulder->elbow and a bit past; forearm is bare."""
    cuff = lerp2(elbow, hand, 0.18)
    cuff2 = lerp2(elbow, hand, 0.30)
    g = [tube([shoulder, elbow, cuff2], 50, C["shirt"])]
    # rolled cuff band
    dx, dy = hand[0] - elbow[0], hand[1] - elbow[1]
    n = math.hypot(dx, dy) or 1
    px, py = -dy / n * 30, dx / n * 30
    band = (f"M {f(cuff[0] + px)},{f(cuff[1] + py)} L {f(cuff[0] - px)},{f(cuff[1] - py)} "
            f"L {f(cuff2[0] - px)},{f(cuff2[1] - py)} L {f(cuff2[0] + px)},{f(cuff2[1] + py)} Z")
    g.append(washed(band, "#dbe8f2", sw=3, off=(1, 1)))
    g.append(tube([cuff2, hand], 32, C["skin"]))
    g.append(_hand(hand, hand_shape, math.degrees(math.atan2(dy, dx)), flip))
    return "".join(g)


def _hand(p, shape, ang, flip):
    x, y = p
    sc = -1 if flip else 1
    if shape == "pencil":
        inner = (washed("M -18,-14 C 8,-24 26,-8 24,8 C 22,22 -4,26 -18,14 Z", C["skin"], off=(2, 1))
                 + path("M 8,-30 L -14,26", stroke=INK, sw=9) + path("M 8,-30 L -14,26", stroke="#e8b84a", sw=5)
                 + path("M -14,26 L -17,34", sw=3))
        return f'<g transform="translate({x},{y}) scale({sc},1)">{inner}</g>'
    if shape == "chin":
        inner = washed("M -16,-20 C 4,-30 26,-18 26,0 C 26,16 6,24 -14,18 C -24,8 -24,-12 -16,-20 Z", C["skin"], off=(2, 1)) + \
                path("M 4,-22 C 12,-30 22,-26 22,-18", sw=2.6)
        return f'<g transform="translate({x},{y}) rotate({ang - 90})">{inner}</g>'
    if shape == "cup":
        inner = washed("M -34,-12 C -38,16 -10,26 12,22 C 28,18 36,4 34,-12 C 20,-2 -20,-2 -34,-12 Z", C["skin"], off=(2, 1)) + \
                washed("M 26,-10 C 30,-26 44,-26 42,-10 Z", C["skin"], sw=2.6, off=(1, 1)) + \
                path("M -18,8 L -16,16 M -2,10 L -2,18 M 14,8 L 12,16", sw=2.2)
        return f'<g transform="translate({x},{y}) scale({sc},1)">{inner}</g>'
    # rest: flat hand on desk
    inner = washed("M -24,-10 C -6,-20 22,-16 30,-4 C 34,6 20,12 -6,12 C -20,12 -28,4 -24,-10 Z", C["skin"], off=(2, 1)) + \
            path("M 6,-6 L 26,-2 M 4,2 L 24,6", sw=2)
    return f'<g transform="translate({x},{y}) scale({sc},1)">{inner}</g>'


# ---------- more hands ----------
_HANDS_EXTRA = {
    "open": lambda: washed("M -18,10 C -24,-6 -20,-22 -12,-34 L -6,-36 L -4,-20 L 0,-40 L 8,-40 L 8,-22 L 14,-38 L 22,-36 L 18,-16 "
                           "L 28,-28 L 34,-22 L 22,4 C 18,18 -6,22 -18,10 Z", C["skin"], sw=3, off=(2, 1)),
    "point": lambda: washed("M -16,-14 C 0,-22 14,-18 18,-14 L 52,-16 C 60,-16 60,-6 52,-6 L 22,-4 C 24,8 14,18 -2,18 C -16,18 -24,4 -16,-14 Z",
                            C["skin"], sw=3, off=(2, 1)),
    "fist": lambda: washed("M -20,-16 C -4,-26 20,-20 24,-4 C 26,12 10,22 -6,20 C -20,18 -28,0 -20,-16 Z", C["skin"], sw=3, off=(2, 1))
                    + path("M -2,-14 L -2,0 M 10,-12 L 10,2", sw=2),
}


def hand_extra(p, shape, ang=0, flip=False):
    sc = -1 if flip else 1
    return f'<g transform="translate({f(p[0])},{f(p[1])}) rotate({f(ang)}) scale({sc},1)">{_HANDS_EXTRA[shape]()}</g>'


_old_hand = _hand


def _hand(p, shape, ang, flip):  # noqa: F811
    if shape in _HANDS_EXTRA:
        if shape == "point":
            return hand_extra(p, shape, ang, False) if not flip else hand_extra(p, shape, ang + 180, False).replace("scale(1,1)", "scale(1,-1)")
        return hand_extra(p, shape, 0, flip)
    return _old_hand(p, shape, ang, flip)


# ---------- full-body PM ----------
SHL, SHR = (-125, 65), (128, 65)        # shoulders, local to neck base
LEGS = {
    "stand":  [((-70, 330), (-78, 520), (-82, 700)), ((75, 330), (82, 520), (88, 700))],
    "walk":   [((-70, 330), (-112, 510), (-176, 690)), ((75, 330), (140, 500), (158, 700))],
    "trudge": [((-70, 330), (-128, 520), (-170, 700)), ((75, 330), (160, 486), (138, 696))],
    "sit":    [((-70, 330), (-92, 410), (-100, 600)), ((75, 330), (98, 410), (110, 600))],
    "sit_slump": [((-70, 330), (-120, 404), (-150, 600)), ((75, 330), (130, 404), (170, 600))],
}


def legs(mode):
    g = []
    for hip, knee, foot in (LEGS[mode] if isinstance(mode, str) else mode):
        g.append(tube([hip, knee, foot], 66, C["trousers"]))
        fx, fy = foot
        g.append(washed(f"M {fx - 34},{fy - 10} C {fx - 30},{fy - 30} {fx + 10},{fy - 30} {fx + 30},{fy - 18} "
                        f"C {fx + 56},{fy - 12} {fx + 64},{fy + 8} {fx + 50},{fy + 14} L {fx - 34},{fy + 14} Z", C["shoes"], off=(2, 2)))
    # pelvis + belt
    g.append(washed("M -152,292 L 158,292 L 156,372 C 100,392 -100,392 -150,372 Z", C["trousers"], off=(3, 2)))
    g.append(washed("M -154,288 L 160,288 L 160,312 L -154,312 Z", "#5b3a22", sw=3, off=(1, 1)))
    g.append(washed("M -6,286 L 26,286 L 26,314 L -6,314 Z", "#c9a24a", sw=2.6, off=(1, 1)))
    return "".join(g)


def paper_stack(x, y, n=6, w=110, tilt=0, tied=False):
    g = []
    for i in range(n):
        dx = ((i * 37) % 9) - 4
        yy = y - i * 9
        g.append(washed(f"M {x - w / 2 + dx},{yy} L {x + w / 2 + dx},{yy - 2} L {x + w / 2 + dx + 2},{yy + 9} L {x - w / 2 + dx - 2},{yy + 9} Z",
                        C["paper_sheet"] if i % 3 else "#efe4c6", sw=2.2, off=(1, 1)))
    if tied:
        g.append(path(f"M {x - 10},{y + 9} L {x - 10},{y - n * 9} M {x + 14},{y + 9} L {x + 14},{y - n * 9}", stroke="#8a5a2a", sw=3))
    return f'<g transform="rotate({tilt},{x},{y})">{"".join(g)}</g>'


def backpack(h):
    """Paperwork strapped to his back: drawn BEFORE the torso so it sits behind him."""
    g = [paper_stack(-20, 300, n=int(h / 9), w=250, tied=True)]
    g.append(path("M -110,70 C -120,150 -110,230 -100,290 M 90,70 C 100,150 96,230 90,290", stroke="#6b4426", sw=8))
    return "".join(g)


def oxygen_tank():
    return (washed("M 110,20 C 110,0 190,0 190,20 L 190,300 C 190,316 110,316 110,300 Z", "#7c9a74", off=(3, 2))
            + washed("M 135,-4 L 165,-4 L 162,-26 L 138,-26 Z", C["metal"], sw=2.6, off=(1, 1))
            + path("M 150,-26 C 150,-60 120,-80 100,-90", sw=6) + path("M 150,-26 C 150,-60 120,-80 100,-90", stroke="#9fbcb8", sw=3))


def pm_full(x, y, s=0.5, *, legs_mode="stand", lean=0, head_rot=0, look=(0, 0), brows="neutral",
            mouth="neutral", eyes="open", beard=0.0, grey=0.0, arms=(), behind="", front="", mask=False,
            before_arms="", tank=False, beard_trail=0, beard_wind=None):
    """Standing/sitting PM. (x, y) = feet line (floor). Local origin = neck base, floor at local 700."""
    body, hd, _ = pm(0, 0, head_rot=head_rot, look=look, brows=brows, mouth=mouth, eyes=eyes,
                     beard=beard, grey=grey, mask=mask, beard_wind=beard_wind)
    floor = 600 if isinstance(legs_mode, str) and legs_mode.startswith("sit") else 700
    arm_svg = "".join(arm(*a) for a in arms)
    tank_svg = f'<g transform="translate(-280,40)">{oxygen_tank()}</g>' if tank else ""
    upper = f'<g transform="rotate({lean},0,330)">{behind}{tank_svg}{body}{hd}{before_arms}{arm_svg}{front}</g>'
    trail = ""
    if beard_trail and beard_wind is None:
        col = _mix(C["beard"], C["beard_grey"], grey)
        trail = washed(f"M 120,{floor - 40} C 60,{floor - 10} 0,{floor - 4} {-beard_trail},{floor - 6} C {-beard_trail - 30},{floor + 4} {-beard_trail},{floor + 14} {-beard_trail + 30},{floor + 12} L 140,{floor + 10} Z", col, off=(3, 2))
    return f'<g transform="translate({f(x)},{f(y)}) scale({s}) translate(0,{-floor})">{trail}{legs(legs_mode)}{upper}</g>'


def to_world(x, y, s, lx, ly, sitting=False):
    floor = 600 if sitting else 700
    return (x + lx * s, y + (ly - floor) * s)


# ---------- crawling PM (leopard crawl, profile to screen-right) ----------
def pm_crawl(x, y, s=0.5, *, beard_tail=900, grey=0.9, bulb_b=0.1, look=(0.6, -0.6), brows="sad",
             mouth="wobbly", eyes="tired", arm_reach=1.0, tank=True, pack=True, bulb_fn=None, phase=None, beard_wind=None, paper_count=12):
    """(x, y) = ground point under his chest. Facing right. phase drives an alternating leopard-crawl cycle."""
    g = []
    col = _mix(C["beard"], C["beard_grey"], grey)
    ph = 0.0 if phase is None else phase
    moving = phase is not None
    kA = (1 + math.sin(ph)) / 2 if moving else 1.0
    kB = (1 + math.sin(ph + math.pi)) / 2 if moving else 0.0
    bob = -7 * abs(math.sin(ph)) if moving else 0.0
    if beard_wind is None:
        # beard: from chin, down to the ground, trailing far behind him
        bd = (f"M 40,-90 C 30,-40 30,-34 0,-34 C {-beard_tail * 0.3},-40 {-beard_tail * 0.6},-20 {-beard_tail},-26 C {-beard_tail - 40},-10 {-beard_tail - 10},12 {-beard_tail + 20},10 "
              f"L 0,10 C 60,8 80,-40 92,-92 Z")
        g.append(washed(bd, col, off=(4, 3)))
        g.append(path(f"M 20,-40 C 10,-4 -200,2 {-beard_tail + 40},2 M 60,-40 C 50,0 -100,6 {-beard_tail + 120},6", sw=1.8, stroke=_mix(col, INK, 0.45)))
    # legs: knees draw up in turn, frog-style
    for k, hipy in ((kA, -60), (kB, -40)):
        knee = (-440 + 40 * k, -8 - 78 * k)
        foot = (-585 + 45 * k, -14 - 14 * k)
        g.append(tube([(-300, hipy), knee, foot], 62, C["trousers"]))
        fx, fy = foot
        g.append(washed(f"M {fx - 10:.1f},{fy - 40:.1f} C {fx - 30:.1f},{fy - 40:.1f} {fx - 40:.1f},{fy - 10:.1f} {fx - 30:.1f},{fy + 8:.1f} L {fx + 10:.1f},{fy + 8:.1f} L {fx + 10:.1f},{fy - 30:.1f} Z", C["shoes"], off=(2, 1)))
    up = []
    if pack:
        up.append(f'<g transform="translate(-170,-120) rotate(-90)">{paper_stack(0, 0, n=paper_count, w=200, tied=True)}</g>')
    if tank:
        up.append(f'<g transform="translate(-110,-200) rotate(80)">{washed("M 0,0 C 0,-14 60,-14 60,0 L 60,200 C 60,214 0,214 0,200 Z", "#7c9a74", off=(3, 2))}</g>')
    up.append(washed("M -320,-110 C -200,-130 -40,-140 10,-110 C 40,-90 40,-20 10,-4 C -80,6 -240,6 -320,-6 C -350,-30 -350,-90 -320,-110 Z", C["shirt"], off=(4, 3)))
    up.append(washed("M -330,-104 L -300,-104 L -300,-6 L -330,-6 Z", "#5b3a22", sw=3, off=(1, 1)))
    # back arm: elbow digs in and pulls
    ex_ = 60 + (34 * math.cos(ph) if moving else 0)
    hx_ = 140 + (46 * math.cos(ph) if moving else 0)
    up.append(tube([(-20, -60), (ex_, -10), (hx_, -12)], 46, C["shirt"]))
    up.append(_old_hand((hx_ + 10, -14), "rest", 0, False))
    tilt = 8 + (3 * math.sin(ph * 2) if moving else 0)
    up.append(f'<g transform="translate(70,-190) rotate({tilt:.1f}) scale(0.95)">' + head(look, brows, mouth, eyes, 0.2, grey, beard_wind=beard_wind) + '</g>')
    hx = 190 + 120 * arm_reach
    hy = -60 - 30 * arm_reach
    up.append(tube([(0, -90), (110, -40), (hx, hy)], 46, C["shirt"]))
    up.append(_old_hand((hx, hy), "cup", 0, False))
    up.append(bulb(hx, hy - 52, s=0.9, b=bulb_b, rays=0) if bulb_fn is None else bulb_fn(hx, hy - 52))
    g.append(f'<g transform="translate(0,{bob:.1f})">' + "".join(up) + '</g>')
    return f'<g transform="translate({f(x)},{f(y)}) scale({s})">{"".join(g)}</g>'
