"""Soundtrack for the animated film, built from the cue lists in film.py."""
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
from sfx import *
import film


def reverb(x, secs=2.5, wet=0.45, bright=3000):
    t = tt(secs)
    ir = lp(noise(secs), bright) * np.exp(-t * 6.9 / secs)
    ir /= np.sqrt(np.sum(ir ** 2))
    y = fftconvolve(x, ir)[: len(x) + len(ir)]
    out = np.zeros(len(y)); out[: len(x)] += x * (1 - wet)
    return out + y * wet


def choir_voice(f, d, vowel=(800, 1150, 2900)):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.012 * np.sin(2 * np.pi * 5.3 * t + rng.uniform(0, 6)))) / SR
    src = ss.sawtooth(ph)
    v = bp(src, vowel[0] * 0.85, vowel[0] * 1.15) + 0.7 * bp(src, vowel[1] * 0.88, vowel[1] * 1.12) + 0.2 * bp(src, vowel[2] * 0.9, vowel[2] * 1.1)
    return v


def chord_voices(notes, d, attack=0.2, release=1.5, kind="choir"):
    t = tt(d)
    s = sum((choir_voice(midi(m), d) if kind == "choir" else saw_voice(midi(m), d, 14, 1100)) for m in notes)
    env = np.minimum(1, t / attack) * np.clip((d - t) / release, 0, 1)
    return norm(s * env, 1)


def sub_boom(d=2.0, f0=58, f1=28):
    t = tt(d)
    f = f0 * (f1 / f0) ** (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)


def crack(d=0.6):
    t = tt(d)
    return lp(noise(d), 4000) * np.exp(-t * 14)


def mountain_hit():
    """Riser lands on three huge hits; the last one opens into brass and choir with a long tail."""
    total = 7.5
    out = np.zeros(int(total * SR))
    hits = [(0.0, 43, 0.5), (0.6, 43, 0.5), (1.2, 39, 5.5)]
    for at_, m, d in hits:
        i = int(at_ * SR)
        h = np.zeros(int(2.4 * SR))
        for part in (norm(brass_hit(m, min(d, 2.4)), 0.8), norm(timpani(midi(m - 12), 2.0), 0.9), norm(sub_boom(2.2), 1.0), crack() * 0.5):
            h[: len(part)] += part
        out[i:i + len(h)] += h[: len(out) - i]
    i = int(1.2 * SR)
    brass = chord_voices([39, 46, 51, 55, 58], 5.5, 0.05, 3.0, kind="brass") * 0.7
    choir = chord_voices([63, 67, 70, 75], 5.5, 0.35, 3.2) * 0.6
    for s in (brass, choir):
        out[i:i + len(s)] += s[: len(out) - i]
    # cymbal swell into the last hit
    t = tt(1.2)
    cym = hp(noise(1.2), 5000) * (t / 1.2) ** 3
    out[: len(cym)] += cym * 0.4
    return norm(reverb(out, 3.2, 0.5), 1.0)


def riser(d=1.0):
    t = tt(d)
    f = np.linspace(180, 1400, len(t))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    n = hp(noise(d), 1500) * 0.6
    return fade((tone + n) * (t / d) ** 2.5, 0.01, 0.01)


def eagle():
    t = tt(0.9)
    f = 2700 - 900 * (t / 0.9) + 120 * np.sin(2 * np.pi * 14 * t)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.9) ** 0.5
    return reverb(fade(s + bp(noise(0.9), 2000, 4000) * 0.2, 0.02, 0.2), 2.0, 0.5)


def theme_player(d, bpm, transpose=0, start=0.0, minor=False, inst="pluck"):
    beat = 60 / bpm; out = np.zeros(int(d * SR))
    k0 = int(np.ceil(start / beat))
    k = k0
    while (k * beat - start) < d:
        m, b = THEME[k % 16], BASS[k % 16]
        tpos = k * beat - start
        i = int(tpos * SR)
        if i >= 0:
            for note, gain, dur in ((m, 0.5, 0.42), (b, 0.45, 0.5)):
                if note is None: continue
                nn = note + transpose
                if minor and nn % 12 in (4, 9, 11):
                    nn -= 1
                s = pluck(midi(nn), dur) if inst == "pluck" else bassoon(midi(nn), dur * 1.4)
                out[i:i + len(s)] += s[: len(out) - i] * gain
        k += 1
    return out


def bassoon(f, d):
    t = tt(d)
    s = lp(ss.square(2 * np.pi * f * t, 0.3), 900) * np.minimum(1, t / 0.03) * np.exp(-t * 2.5)
    return s


def plod(d, start=0.0):
    beat = 60 / 76
    notes = [36, 43, 39, 43, 36, 43, 38, 43]
    out = np.zeros(int(d * SR)); k = int(np.ceil(start / beat))
    while k * beat - start < d:
        i = int((k * beat - start) * SR)
        s = bassoon(midi(notes[k % 8]), 0.55) * 0.8
        out[i:i + len(s)] += s[: len(out) - i]
        if k % 2 == 1:
            p = pluck(midi(notes[k % 8] + 24), 0.3) * 0.25
            out[i:i + len(p)] += p[: len(out) - i]
        k += 1
    return out


def sad_trombone():
    out = np.zeros(int(3.0 * SR)); pos = 0
    for m, d in ((55, 0.38), (54, 0.38), (53, 0.38), (52, 1.5)):
        t = tt(d)
        vib = 1 + (0.03 * np.sin(2 * np.pi * 5.5 * t) if d > 1 else 0)
        s = lp(ss.sawtooth(2 * np.pi * np.cumsum(midi(m) * vib) / SR), 1300) * np.minimum(1, t / 0.04) * np.clip((d - t) / 0.12, 0, 1)
        i = int(pos * SR); out[i:i + len(s)] += s; pos += d
    return norm(out, 0.9)


def boing():
    t = tt(0.5)
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)


def flop():
    t = tt(0.4)
    return np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) + lp(noise(0.4), 900) * np.exp(-t * 18) * 0.6


def grab():
    return bp(noise(0.06), 1500, 5000) * np.exp(-tt(0.06) * 60)


FUN = {
    "room_tone_office": (lambda: room_tone(13.83), 0.08, "amb"),
    "office_theme": (lambda d: (lambda m: (m.__setitem__(slice(-441, None), m[-441:] * np.linspace(1, 0, 441)) or m))(office_music(d)), 0.3, "music"),
    "scribble": (scribble, 1, "sfx"), "pop": (pop, 1, "sfx"), "fizzle": (fizzle, 1, "sfx"), "grab": (grab, 1, "sfx"),
    "whoosh": (whoosh, 1, "sfx"), "clang": (clang, 1, "sfx"),
    "swell_soft": (lambda: swell([60, 64, 67], 1.0) * np.linspace(0.2, 1, int(1.0 * SR)), 1, "music"),
    "swell_big": (lambda: swell([60, 64, 67, 72, 76], 2.6), 1, "music"),
    "riser": (riser, 1, "sfx"), "mountain_hit": (mountain_hit, 1, "music"), "wind": (wind, 1, "amb"), "eagle": (eagle, 1, "sfx"),
    "gulp": (gulp, 1, "sfx"), "march": (lambda d, start=0.0: theme_player(d, 128, 0, start), 1, "music"),
    "steps": (lambda d, rate=2.2, heavy=0.0, snow=0.0: footsteps(d, rate, heavy, snow), 1, "sfx"),
    "mumble": (mumble, 1, "sfx"), "printer": (printer, 1, "sfx"), "creak": (lambda: creak(0.45), 1, "sfx"),
    "ticking": (ticking, 1, "sfx"), "flutter": (flutter, 1, "sfx"), "cricket": (cricket, 1, "sfx"), "dingdong": (dingdong, 1, "sfx"),
    "boing": (boing, 1, "sfx"), "stamp": (stamp, 1, "sfx"), "plod": (plod, 1, "music"), "sad_trombone": (sad_trombone, 1, "music"),
    "sigh": (sigh, 1, "sfx"), "roar": (roar, 1, "sfx"), "bloops": (bloops, 1, "sfx"),
    "blizzard": (lambda d, cut=False: (lambda w: (w.__setitem__(slice(-882, None), w[-882:] * np.linspace(1, 0, 882)) or w) if cut else w)(wind(d, 1.0)), 1, "amb"),
    "wheeze": (wheeze, 1, "sfx"), "hiss": (hiss, 1, "sfx"), "flop": (flop, 1, "sfx"),
    "shuffle": (lambda d: lp(noise(d), 1100) * (np.abs(np.sin(2 * np.pi * 1.1 * tt(d))) ** 3) * 0.7, 1, "sfx"),
    "calm": (lambda d: lp(noise(d), 500), 1, "amb"),
    "choir": (lambda: reverb(chord_voices([60, 64, 67, 72], 3.0, 0.8, 1.5), 2.5, 0.5), 1, "music"),
    "taps": (taps, 1, "sfx"),
    "musicbox_hope": (lambda d: (lambda mb: (mb.__setitem__(slice(-441, None), mb[-441:] * np.linspace(1, 0, 441)) or mb))(music_box([76, 79, 84, 79, 81, 79, 76, 72], 0.4)[: int(d * SR)]), 1, "music"),
    "musicbox_end": (lambda: music_box([72, None, 67], 0.6), 1, "music"),
}

def main():
    """Build the original soundtrack only when this file is run directly."""
    tl, TOTAL = film.timeline()
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

    music, sfx_, amb = bus["music"] * 0.9, bus["sfx"], bus["amb"]
    env = np.convolve(np.abs(sfx_), np.ones(4410) / 4410, mode="same")
    music = music * (1 - 0.35 * np.clip(env / (env.max() or 1) * 4, 0, 1))
    out = (music + sfx_ + amb)[: int(TOTAL * SR)]
    out = np.tanh(out * 1.1) / np.tanh(1.1)
    out = norm(out, 0.9)
    fo = int(1.5 * SR); out[-fo:] *= np.linspace(1, 0, fo)
    wavfile.write("vid/film.wav", SR, (np.stack([out, out], 1) * 32767).astype(np.int16))
    print("film soundtrack", round(TOTAL, 2), "s")


if __name__ == "__main__":
    main()
