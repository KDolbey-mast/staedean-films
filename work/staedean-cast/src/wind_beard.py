"""A chin-attached beard with a travelling wind wave, in head coordinates.

The root stays attached to the jaw. Displacement grows toward the tip and the
wave travels outward, rather than rotating the entire beard like a rigid flag.
"""
import math
from rig import C, INK, washed, path, _mix


def draw(grey, time, length=720, strength=1.0):
    colour = _mix(C['beard'], C['beard_grey'], grey)
    phase = time * 2 * math.pi * .85

    def point(u, side=0):
        wave = (math.sin(phase - 5 * u) + .3 * math.sin(phase * 1.7 - 8 * u))
        centre = 115 + 32 * u + 55 * strength * u * wave
        width = 48 * (1 - u) ** .8
        return (-125 - length * u, centre + side * width)

    def curve(points):
        # Catmull-Rom tangents give a smooth outline through the sampled wave.
        result = ''
        for i in range(len(points) - 1):
            a = points[max(0, i - 1)]; b = points[i]
            c = points[i + 1]; d = points[min(len(points) - 1, i + 2)]
            result += ' C %.2f,%.2f %.2f,%.2f %.2f,%.2f' % (
                b[0] + (c[0]-a[0])/6, b[1] + (c[1]-a[1])/6,
                c[0] - (d[0]-b[0])/6, c[1] - (d[1]-b[1])/6, *c)
        return result

    samples = [i/16 for i in range(17)]
    lower = [point(u, 1) for u in samples]
    upper = [point(u, -1) for u in reversed(samples)]
    outline = 'M 90,40 C 100,112 -50,170 %.2f,%.2f' % lower[0]
    outline += curve(lower) + curve(upper)
    outline += ' C -112,62 -95,45 -82,30 C -60,36 -30,60 34,64 C 50,70 70,66 90,40 Z'
    art = washed(outline, colour, off=(3, 2))
    for side in (-.5, 0, .5):
        points = [point(u, side) for u in samples[:-1]]
        art += path('M %.2f,%.2f' % points[0] + curve(points), sw=1.8,
                    stroke=_mix(colour, INK, .35))
    return art
