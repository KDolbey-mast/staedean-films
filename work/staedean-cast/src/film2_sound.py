"""Soundtrack for chapter 2 (THE DOOR). Same synth palette as film 1, but bright and quick."""
import numpy as np
from scipy.io import wavfile
from sfx import *
from film_sound import reverb, chord_voices, theme_player, sub_boom, crack, riser, FUN as FUN1
import film2


def tiny_dun():
    s = brass_hit(39, 0.5) * 0.6
    t = timpani(midi(27), 0.8)
    out = np.zeros(int(0.9 * SR)); out[: len(s)] += s; out[: len(t)] += norm(t, 0.6)
    return reverb(out, 1.2, 0.3)


def brr():
    t = tt(0.5)
    return np.sin(2 * np.pi * 220 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * t)) * np.exp(-t * 4) * 0.6


def ding():
    return bell(midi(84), 1.2) * 0.8


def door_creak():
    t = tt(0.7)
    f = np.interp(t, [0, 0.35, 0.7], [300, 520, 380])
    return fade(bp(ss.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 40 * t))), 500, 2500), 0.03, 0.1) * 0.6


def flip():
    t = tt(0.2)
    return bp(noise(0.2), 1500, 6000) * np.exp(-t * 25)


def hammer(d=1.4):
    out = np.zeros(int(d * SR)); k = 0
    while k / 6 < d - 0.05:
        t = tt(0.12)
        h = np.sin(2 * np.pi * 900 * t) * np.exp(-t * 60) + bp(noise(0.12), 800, 3000) * np.exp(-t * 50) * 0.6
        i = int(k / 6 * SR); out[i:i + len(h)] += h[: len(out) - i]
        k += 1
    return out


def chord_up():
    out = np.zeros(int(1.8 * SR))
    for k, m in enumerate((72, 76, 79, 84)):
        b = bell(midi(m), 1.4) * 0.5; i = int(k * 0.07 * SR); out[i:i + len(b)] += b
    return out


def pat():
    t = tt(0.08)
    return lp(noise(0.08), 1500) * np.exp(-t * 60)


def twang():
    t = tt(0.9)
    f = 110 * (1 + 0.3 * np.exp(-t * 12))
    out = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 4)
    p = pluck(midi(40), 0.8)
    out[: len(p)] += p * 0.5
    return out


def triumph():
    """The mirror of the mountain hit: one big MAJOR chord as the product sails over the peak."""
    total = 5.0
    out = np.zeros(int(total * SR))
    h = np.zeros(int(2.4 * SR))
    for part in (norm(brass_hit(48, 2.4), 0.8), norm(timpani(midi(36), 2.0), 0.8), norm(sub_boom(2.0, 70, 40), 0.7)):
        h[: len(part)] += part
    out[: len(h)] += h
    brass = chord_voices([48, 55, 60, 64, 67], 4.0, 0.05, 2.2, kind="brass") * 0.7
    choir = chord_voices([72, 76, 79, 84], 4.0, 0.3, 2.4) * 0.6
    out[: len(brass)] += brass; out[: len(choir)] += choir
    for k, m in enumerate((84, 88, 91, 96)):
        b = bell(midi(m), 1.2) * 0.3; i = int((0.1 + k * 0.08) * SR); out[i:i + len(b)] += b
    return norm(reverb(out, 2.5, 0.45), 1.0)


def thump():
    t = tt(0.3)
    return np.sin(2 * np.pi * 90 * t) * np.exp(-t * 20) + lp(noise(0.3), 1200) * np.exp(-t * 40) * 0.5


def shutter(d=1.0):
    t = tt(d)
    return bp(noise(d), 600, 3000) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 22 * t))) * np.minimum(1, (d - t) / 0.1) * 0.7


def crowd(d=5.0):
    out = np.zeros(int(d * SR))
    for k in range(7):
        m = mumble(d * rng.uniform(0.5, 0.9), rng.uniform(130, 260), rng.uniform(3, 6))
        i = int(rng.uniform(0, d * 0.3) * SR); out[i:i + len(m)] += m[: len(out) - i] * 0.35
    out += lp(noise(d), 1200) * 0.15
    return fade(out, 0.3, 0.6)


def ding_run(d=5.0):
    out = np.zeros(int(d * SR)); k = 0
    while k * 0.3 < d - 0.2:
        b = bell(midi(88 if k % 2 else 84), 0.5) * 0.4
        i = int(k * 0.3 * SR); out[i:i + len(b)] += b[: len(out) - i]
        k += 1
    return out


def ching():
    t = tt(0.8)
    return bell(midi(96), 0.8) * 0.5 + hp(noise(0.8), 4000) * np.exp(-t * 20) * 0.3


def clack():
    t = tt(0.15)
    return bp(noise(0.15), 400, 2500) * np.exp(-t * 40) + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 50)


def final_chord(d=3.2):
    c = chord_voices([60, 64, 67, 72, 76], d, 0.25, min(3.5, d * 0.5)) * 0.6
    b = chord_voices([48, 55, 64], d, 0.3, min(3.5, d * 0.5), kind="brass") * 0.4
    s = np.zeros(len(c)); s += c; s[: len(b)] += b
    return norm(reverb(s, 2.5, 0.45), 0.9)


def theme2(d):
    """Bright, quicker take on the office theme with a glockenspiel on the downbeats."""
    m = theme_player(d, 150, 0, 0.0)
    beat = 60 / 150; k = 0
    while k * 4 * beat < d:
        b = bell(midi([84, 88, 86, 91][k % 4]), 0.6) * 0.25
        i = int(k * 4 * beat * SR); m[i:i + len(b)] += b[: len(m) - i]
        k += 1
    return m


def two_notes_down():
    out = np.zeros(int(1.6 * SR))
    for k, m in enumerate((72, 67)):
        b = bell(midi(m), 1.0) * 0.5; i = int(k * 0.45 * SR); out[i:i + len(b)] += b
    return out


def festoon():
    out = np.zeros(int(1.6 * SR))
    for k, m in enumerate((60, 64, 67, 72, 76, 79, 84, 88, 91)):
        b = bell(midi(m), 0.8) * 0.35; i = int(k * 0.1 * SR); out[i:i + len(b)] += b[: len(out) - i]
    return out


def theme2_out(d, fade=3.0):
    """The bright theme, easing out over its last few seconds with a little room on it, instead of stopping dead."""
    m = theme2(d)
    n = int(fade * SR)
    m[-n:] *= np.linspace(1, 0, n) ** 1.6
    return reverb(m, 1.6, 0.25)[: int((d + 1.2) * SR)]


def bridge_pad(d):
    """A soft warm chord that slides in under the door scene and carries through both end cards."""
    t = tt(d)
    s = chord_voices([48, 55, 60, 64], d, 1.8, 3.0) * 0.8
    s += lp(chord_voices([67, 72], d, 2.4, 3.0, kind="brass"), 1200) * 0.3
    return reverb(s * np.minimum(1, t / 1.8), 2.5, 0.4)[: int((d + 1.0) * SR)]


def logo_sparkle():
    out = np.zeros(int(2.2 * SR))
    for k, m in enumerate((84, 91, 96)):
        b = bell(midi(m), 1.6) * 0.4; i = int(k * 0.09 * SR); out[i:i + len(b)] += b[: len(out) - i]
    return reverb(out, 2.0, 0.4)[: len(out)]


FUN = dict(FUN1)
FUN.update({
    "room_tone": (room_tone, 1, "amb"), "office_theme": (lambda d: office_music(d), 1, "music"),
    "tiny_dun": (tiny_dun, 1, "music"), "brr": (brr, 1, "sfx"), "ding": (ding, 1, "sfx"), "door_creak": (door_creak, 1, "sfx"),
    "theme2": (theme2, 1, "music"), "flip": (flip, 1, "sfx"), "hammer": (hammer, 1, "sfx"), "chord_up": (chord_up, 1, "music"),
    "pat": (pat, 1, "sfx"), "twang": (twang, 1, "sfx"), "triumph": (triumph, 1, "music"), "thump": (thump, 1, "sfx"),
    "shutter": (shutter, 1, "sfx"), "crowd": (crowd, 1, "sfx"), "ding_run": (ding_run, 1, "sfx"), "ching": (ching, 1, "sfx"),
    "clack": (clack, 1, "sfx"), "final_chord": (final_chord, 1, "music"),
    "creak": (lambda: creak(0.45), 1, "sfx"), "two_notes_down": (two_notes_down, 1, "music"), "theme2_out": (theme2_out, 1, "music"), "bridge_pad": (bridge_pad, 1, "music"), "festoon": (festoon, 1, "music"), "logo_sparkle": (logo_sparkle, 1, "music"),
})

def main():
    """Build the original soundtrack only when this file is run directly."""
    tl, TOTAL = film2.timeline()
    bus = {k: np.zeros(int((TOTAL + 8) * SR)) for k in ("music", "sfx", "amb")}
    for start, s in tl:
        for cue in s["cues"]:
            t_, name, kw = cue[0], cue[1], cue[2]
            fn, g0, b0 = FUN[name]
            g = cue[3] if len(cue) > 3 else g0
            b = cue[4] if len(cue) > 4 else b0
            sig = np.asarray(fn(**kw), dtype=float)
            i = int((start + t_) * SR)
            buf = bus[b]
            buf[i:i + len(sig)] += sig[: len(buf) - i] * g

    # the bright theme runs from the door to the new normal; let the end chord stand alone
    music = bus["music"]
    end_start = [st for st, s in tl if s["name"] == "E1_still_die"][0]
    fade_n = int(0.6 * SR); i0 = int((end_start - 0.6) * SR)
    theme_part = np.zeros_like(music)
    sfx_, amb = bus["sfx"], bus["amb"]
    env = np.convolve(np.abs(sfx_), np.ones(4410) / 4410, mode="same")
    music = music * (1 - 0.3 * np.clip(env / (env.max() or 1) * 4, 0, 1))
    out = (music * 0.9 + sfx_ + amb)[: int(TOTAL * SR)]
    out = np.tanh(out * 1.1) / np.tanh(1.1)
    out = norm(out, 0.9)
    fo = int(1.6 * SR); out[-fo:] *= np.linspace(1, 0, fo) ** 1.5
    wavfile.write("vid/film2.wav", SR, (np.stack([out, out], 1) * 32767).astype(np.int16))
    print("film2 soundtrack", round(TOTAL, 2), "s")


if __name__ == "__main__":
    main()
