"""Location 1: the PM's office. Camera A (fixed). Layout never changes."""
from rig import *

NECK = (940, 470)            # PM neck base, fixed
SH_L = (815, 535)            # screen-left shoulder
SH_R = (1068, 535)           # screen-right shoulder
CHIN = (978, 474)
THOUGHT_BULB = (1012, 132)   # where ideas appear above his head
PAD = (1085, 668)            # notepad centre on desk


def back_wall():
    g = [f'<rect width="{W}" height="{H}" fill="{C["paper"]}"/>',
         f'<path d="M -10,-10 L 2300,-10 L 2300,812 L -10,812 Z" fill="{C["wall"]}"/>',
         f'<path d="M -10,-10 L 260,-10 L 180,812 L -10,812 Z" fill="{C["wall_dark"]}" opacity="0.5"/>',
         f'<path d="M -10,812 L 2300,812 L 2300,1090 L -10,1090 Z" fill="{C["floor"]}"/>',
         path("M -10,812 L 1930,812", sw=3.5),
         path("M -10,840 L 1930,836", sw=1.6, stroke="#8f7a5c")]
    # skirting board
    g.append(f'<path d="M -10,790 L 1930,790 L 1930,812 L -10,812 Z" fill="#d9c6a4"/>' + path("M -10,790 L 1930,790", sw=2.4))
    return "".join(g)


def window():
    x0, y0, x1, y1 = 1420, 110, 1830, 600
    g = [f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{C["sky"]}"/>']
    # foreshadowing: a slope far too big for the window
    g.append(f'<path d="M {x0},{y1} L {x0},430 C 1500,360 1560,250 1640,{y0 - 5} L {x1},{y0 - 5} L {x1},{y1} Z" fill="{C["mountain"]}"/>')
    g.append(f'<path d="M 1640,{y0 - 5} C 1600,200 1560,240 1600,290 C 1640,250 1700,200 1760,{y0 - 5} Z" fill="{C["snow"]}" opacity="0.85"/>')
    g.append(f'<path d="M 1700,600 C 1660,560 1760,520 1700,480 C 1650,450 1740,420 1690,380 C 1660,350 1720,320 1690,290" fill="none" stroke="#6f777b" stroke-width="2" stroke-dasharray="6 6"/>')
    g.append(f'<rect x="1695" y="468" width="10" height="8" fill="#6f777b"/><rect x="1684" y="372" width="8" height="6" fill="#6f777b"/>')
    g.append(path(f"M {x0},430 C 1500,360 1560,250 1640,{y0}", sw=2.6))
    # frame
    g.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="{C["paper_sheet"]}" stroke-width="22"/>')
    g.append(path(f"M {x0 - 11},{y0 - 11} L {x1 + 11},{y0 - 11} L {x1 + 11},{y1 + 11} L {x0 - 11},{y1 + 11} Z", sw=3.5))
    g.append(path(f"M {x0 + 11},{y0 + 11} L {x1 - 11},{y0 + 11} L {x1 - 11},{y1 - 11} L {x0 + 11},{y1 - 11} Z", sw=2.4))
    g.append(f'<path d="M {(x0 + x1) / 2},{y0} L {(x0 + x1) / 2},{y1}" stroke="{C["paper_sheet"]}" stroke-width="14"/>')
    g.append(path(f"M {(x0 + x1) / 2 - 7},{y0 + 11} L {(x0 + x1) / 2 - 7},{y1 - 11} M {(x0 + x1) / 2 + 7},{y0 + 11} L {(x0 + x1) / 2 + 7},{y1 - 11}", sw=2.2))
    # sill
    g.append(washed(f"M {x0 - 30},{y1 + 11} L {x1 + 30},{y1 + 11} L {x1 + 20},{y1 + 34} L {x0 - 20},{y1 + 34} Z", "#efe6d4", off=(3, 2)))
    return "".join(g)


def calendar(month="NOV"):
    x, y = 210, 190
    g = [washed(f"M {x},{y} L {x + 160},{y} L {x + 162},{y + 220} L {x + 2},{y + 222} Z", C["paper_sheet"], off=(4, 3))]
    g.append(washed(f"M {x},{y} L {x + 160},{y} L {x + 160},{y + 46} L {x},{y + 46} Z", C["cal_red"], off=(2, 2)))
    g.append(f'<text x="{x + 80}" y="{y + 34}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="28" fill="#fbf3e6">{month}</text>')
    for r in range(5):
        for c in range(5):
            cx, cy = x + 22 + c * 29, y + 72 + r * 32
            g.append(path(f"M {cx - 6},{cy} L {cx + 6},{cy}", sw=2.2))
    g.append(f'<circle cx="{x + 80}" cy="{y - 8}" r="5" fill="{INK}"/>' + path(f"M {x + 80},{y - 8} L {x + 60},{y} M {x + 80},{y - 8} L {x + 100},{y}", sw=2))
    return "".join(g)


def poster():
    x, y = 520, 170
    g = [washed(f"M {x},{y} L {x + 190},{y + 4} L {x + 186},{y + 250} L {x - 4},{y + 246} Z", "#efe1c3", off=(4, 3))]
    g.append(f'<text x="{x + 94}" y="{y + 52}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="34" fill="{INK}" letter-spacing="2">MOVE</text>')
    g.append(f'<text x="{x + 94}" y="{y + 90}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="34" fill="{INK}" letter-spacing="2">FAST</text>')
    # a snail
    g.append(washed(f"M {x + 60},{y + 200} C {x + 60},{y + 150} {x + 130},{y + 150} {x + 128},{y + 196} Z", "#c99a5a", off=(2, 2)))
    g.append(path(f"M {x + 94},{y + 196} C {x + 84},{y + 186} {x + 92},{y + 170} {x + 104},{y + 178} C {x + 112},{y + 186} {x + 104},{y + 194} {x + 98},{y + 188}", sw=2.2))
    g.append(washed(f"M {x + 40},{y + 210} L {x + 150},{y + 210} C {x + 156},{y + 196} {x + 146},{y + 186} {x + 134},{y + 192} L {x + 128},{y + 198} L {x + 40},{y + 200} Z", "#d9c08a", sw=2.6, off=(2, 1)))
    g.append(path(f"M {x + 146},{y + 190} L {x + 152},{y + 172} M {x + 140},{y + 190} L {x + 140},{y + 174}", sw=2))
    return "".join(g)


def chair_back():
    return washed("M 808,470 C 806,420 830,400 880,398 L 1010,398 C 1060,400 1076,420 1074,470 L 1080,700 L 800,700 Z",
                  C["chair"], off=(4, 3))


def desk_top():
    g = [washed("M 560,640 L 1340,640 L 1372,690 L 528,690 Z", C["desk"], off=(5, 3))]
    g.append(washed("M 528,690 L 1372,690 L 1372,720 L 528,720 Z", C["desk_dark"], off=(3, 2)))
    g.append(washed("M 560,720 L 1340,720 L 1336,880 L 564,880 Z", C["desk"], off=(5, 3)))
    g.append(f'<path d="M 560,720 L 1340,720 L 1340,760 L 560,760 Z" fill="{C["desk_dark"]}" opacity="0.5"/>')
    g.append(path("M 950,730 L 950,870", sw=2.4))
    g.append(path("M 900,790 L 920,790 M 980,790 L 1000,790", sw=3))
    g.append(path("M 640,668 C 760,664 900,670 1000,666", sw=1.6, stroke="#8a6440"))
    # floor shadow
    g.append(f'<ellipse cx="950" cy="884" rx="440" ry="18" fill="#7d6648" opacity="0.35" filter="url(#soft)"/>')
    return "".join(g)


def mug():
    x, y = 650, 600
    return (washed(f"M {x},{y} L {x + 56},{y} L {x + 52},{y + 58} L {x + 4},{y + 58} Z", C["mug"], off=(3, 2))
            + path(f"M {x + 54},{y + 12} C {x + 80},{y + 10} {x + 80},{y + 44} {x + 52},{y + 42}", sw=3.2)
            + f'<ellipse cx="{x + 28}" cy="{y}" rx="28" ry="6" fill="#5a3a26" stroke="{INK}" stroke-width="2.6"/>'
            + path(f"M {x + 20},{y - 14} C {x + 14},{y - 26} {x + 28},{y - 32} {x + 22},{y - 46} M {x + 36},{y - 12} C {x + 30},{y - 24} {x + 44},{y - 30} {x + 38},{y - 42}", sw=1.8, stroke="#8c8580"))


def tray():
    x, y = 1210, 600
    g = [washed(f"M {x},{y + 30} L {x + 110},{y + 30} L {x + 116},{y + 56} L {x - 6},{y + 56} Z", "#8c8f8e", off=(2, 2))]
    for i in range(5):
        g.append(washed(f"M {x + 4 + i},{y + 26 - i * 7} L {x + 104 + i},{y + 24 - i * 7} L {x + 108 + i},{y + 32 - i * 7} L {x + 2 + i},{y + 33 - i * 7} Z", C["paper_sheet"], sw=2.2, off=(1, 1)))
    return "".join(g)


def notepad(state="sketch1", pencil_on_pad=False):
    cx, cy = PAD
    pad = f"M {cx - 92},{cy - 20} L {cx + 78},{cy - 20} L {cx + 96},{cy + 18} L {cx - 104},{cy + 18} Z"
    g = [washed(pad, "#fbf3c8", sw=3, off=(3, 2))]
    g.append(path(f"M {cx - 88},{cy - 20} L {cx + 74},{cy - 20}", stroke="#c0623a", sw=5))
    if state in ("idea1", "idea1_x"):
        g.append(path(f"M {cx - 70},{cy + 4} C {cx - 50},{cy - 14} {cx - 30},{cy + 14} {cx - 10},{cy - 6} C {cx + 6},{cy - 16} {cx + 20},{cy + 10} {cx + 40},{cy - 4} "
                      f"M {cx - 60},{cy + 12} L {cx + 30},{cy + 10}", sw=2))
    if state == "idea1_x":
        g.append(path(f"M {cx - 80},{cy - 14} L {cx + 60},{cy + 14} M {cx - 80},{cy + 14} L {cx + 60},{cy - 14}", sw=3.4, stroke="#c0623a"))
    if state in ("sketch1", "sketch2", "sketch3"):
        g.append(path(f"M {cx - 70},{cy - 6} L {cx - 40},{cy - 6} L {cx - 42},{cy + 8} L {cx - 72},{cy + 8} Z", sw=2))
        g.append(path(f"M {cx - 34},{cy + 1} L {cx - 8},{cy + 1} M {cx - 14},{cy - 4} L {cx - 8},{cy + 1} L {cx - 14},{cy + 6}", sw=2))
    if state in ("sketch2", "sketch3"):
        g.append(path(f"M {cx + 6},{cy + 1} C {cx + 6},{cy - 12} {cx + 34},{cy - 12} {cx + 34},{cy + 1} C {cx + 34},{cy + 12} {cx + 6},{cy + 12} {cx + 6},{cy + 1}", sw=2))
        g.append(path(f"M {cx + 44},{cy - 4} L {cx + 70},{cy - 4} M {cx + 44},{cy + 6} L {cx + 64},{cy + 6}", sw=1.8))
    if state == "sketch3":
        g.append(path(f"M {cx + 2},{cy - 14} C {cx - 4},{cy - 2} {cx + 40},{cy + 22} {cx + 42},{cy - 2} C {cx + 46},{cy - 22} {cx + 2},{cy - 22} {cx + 2},{cy - 14}", sw=2.6, stroke="#c0623a"))
    if pencil_on_pad:
        g.append(path(f"M {cx + 20},{cy + 14} L {cx + 110},{cy - 6}", sw=10) + path(f"M {cx + 20},{cy + 14} L {cx + 110},{cy - 6}", sw=6, stroke="#e8b84a")
                 + path(f"M {cx + 20},{cy + 14} L {cx + 10},{cy + 17}", sw=3))
    return "".join(g)


def wastebin(contents=("dead_bulb",)):
    x, y = 360, 742
    g = []
    inside = ""
    if "dead_bulb" in contents:
        inside += bulb(x + 52, y - 6, s=0.62, b=0, rot=-28, dead=True)
    if "paper" in contents:
        inside += washed(f"M {x + 86},{y + 2} C {x + 80},{y - 18} {x + 108},{y - 22} {x + 112},{y - 4} Z", C["paper_sheet"], sw=2.4, off=(1, 1))
    g.append(inside)
    g.append(washed(f"M {x},{y} L {x + 130},{y} L {x + 116},{y + 138} L {x + 14},{y + 138} Z", C["bin"], off=(4, 3)))
    for i in range(1, 6):
        g.append(path(f"M {x + i * 22},{y + 8} L {x + 4 + i * 20},{y + 130}", sw=1.6, stroke="#5f6869"))
    g.append(f'<ellipse cx="{x + 65}" cy="{y}" rx="65" ry="10" fill="none" stroke="{INK}" stroke-width="3.2"/>')
    g.append(f'<ellipse cx="{x + 65}" cy="{y + 142}" rx="70" ry="10" fill="#7d6648" opacity="0.35" filter="url(#soft)"/>')
    return "".join(g)
