"""MOUNT STAEDEAN - synthesised soundtrack. Everything is generated from scratch (no samples)."""
import glob, os
import numpy as np
import scipy.signal as ss
from scipy.io import wavfile
from timing import T

SR = 44100
rng = np.random.default_rng(7)


# ---------------- building blocks ----------------
def tt(d):
    return np.arange(int(d * SR)) / SR


def noise(d):
    return rng.standard_normal(int(d * SR))


def _filt(x, kind, f, order=2):
    nyq = SR / 2
    if kind == "bp":
        b, a = ss.butter(order, [f[0] / nyq, f[1] / nyq], btype="band")
    else:
        b, a = ss.butter(order, f / nyq, btype=kind)
    return ss.lfilter(b, a, x)


lp = lambda x, f, o=2: _filt(x, "low", f, o)
hp = lambda x, f, o=2: _filt(x, "high", f, o)
bp = lambda x, lo, hi, o=2: _filt(x, "bp", (lo, hi), o)


def fade(x, a=0.01, r=0.05):
    n = len(x); e = np.ones(n)
    na, nr = min(int(a * SR), n), min(int(r * SR), n)
    if na: e[:na] = np.linspace(0, 1, na)
    if nr: e[-nr:] *= np.linspace(1, 0, nr)
    return x * e


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def smooth_rand(d, rate, lo=0.0, hi=1.0):
    n = int(d * rate) + 3
    pts = rng.uniform(lo, hi, n)
    x = np.linspace(0, n - 1, int(d * SR))
    return np.interp(x, np.arange(n), pts)


# ---------------- instruments & effects ----------------
def bell(f, d=1.4):
    t = tt(d)
    parts = [(1, 1, 2.5), (2.0, .45, 3.5), (2.76, .3, 5), (5.4, .12, 8)]
    return fade(sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t * k / d * 1.5) for r, a, k in parts), 0.002, 0.05)


def pluck(f, d=0.5):
    """Karplus-Strong plucked string."""
    n = int(d * SR); p = max(2, int(SR / f))
    buf = rng.uniform(-1, 1, p); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return fade(out, 0.001, 0.03)


def pop():
    a = bell(1568, 0.9) * 0.6
    b = bell(2093, 0.5) * 0.3
    a[: len(b)] += b
    return a


def fizzle(d=0.7):
    t = tt(d)
    n = bp(noise(d), 1500, 5000)
    crackle = (rng.random(len(t)) > 0.985) * rng.uniform(-1, 1, len(t))
    tone = np.sin(2 * np.pi * np.cumsum(np.linspace(900, 160, len(t))) / SR) * 0.3
    return fade((n * 0.25 + crackle * 0.8 + tone) * np.exp(-t * 3), 0.005, 0.1)


def scribble(d):
    t = tt(d)
    strokes = np.abs(np.sin(2 * np.pi * smooth_rand(d, 8, 4, 9).cumsum() / SR)) ** 2
    return fade(bp(noise(d), 2000, 6000) * strokes * 0.35, 0.02, 0.08)


def whoosh(d=0.6, lo=500, hi=2500):
    t = tt(d)
    return fade(bp(noise(d), lo, hi) * np.sin(np.pi * t / d) ** 2, 0.01, 0.05)


def clang():
    t = tt(1.2)
    parts = [(420, 1, 6), (1130, .6, 9), (1810, .4, 12), (2650, .3, 16), (3900, .2, 22)]
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in parts)
    return fade(s + hp(noise(1.2), 2000) * np.exp(-t * 40) * 0.6, 0.001, 0.1)


def saw_voice(f, d, harm=10, cutoff=1800):
    t = tt(d)
    s = sum(np.sin(2 * np.pi * f * k * t * (1 + 0.002 * np.sin(2 * np.pi * 5 * t))) / k for k in range(1, harm + 1))
    return lp(s, cutoff)


def swell(notes, d=2.8):
    t = tt(d)
    s = sum(saw_voice(midi(m), d, 8, 2200) for m in notes)
    env = np.minimum(1, t / 0.5) * np.minimum(1, (d - t) / 0.8)
    return norm(s * env, 0.8)


def brass_hit(m, d):
    t = tt(d)
    s = saw_voice(midi(m), d, 14, 900) + saw_voice(midi(m - 12), d, 14, 600)
    env = np.minimum(1, t / 0.03) * np.exp(-t * (1.2 / d))
    return norm(s * env, 1)


def timpani(f=60, d=1.2):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 3) + lp(noise(d), 300) * np.exp(-t * 18) * 0.4)


def dun_dun_dun():
    out = np.zeros(int(3.6 * SR))
    for at, m, d in ((0.0, 43, 0.35), (0.45, 43, 0.35), (0.9, 39, 2.6)):
        s = brass_hit(m, d) * 0.8 + norm(timpani(midi(m - 12), d), 0.7)
        i = int(at * SR); out[i:i + len(s)] += s
    return out


def gulp():
    t = tt(0.18)
    f = np.linspace(420, 120, len(t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.18)


def footsteps(d, rate=2.2, heavy=0.0, snow=0.0):
    out = np.zeros(int(d * SR)); step = 1 / rate
    k = 0
    while k * step < d - 0.1:
        n = noise(0.12); tt_ = tt(0.12)
        cr = lp(n, 1800 + 1500 * snow) * np.exp(-tt_ * (35 - 15 * snow)) + np.sin(2 * np.pi * (90 - 30 * heavy) * tt_) * np.exp(-tt_ * 30) * (0.6 + heavy)
        i = int((k * step + rng.uniform(0, 0.02)) * SR)
        out[i:i + len(cr)] += cr[: len(out) - i] * (0.8 + 0.2 * (k % 2))
        k += 1
    return out


VOWELS = [(730, 1090), (530, 1840), (570, 840), (440, 1020), (660, 1700)]


def mumble(d, f0=150, rate=6.0, question=False, phone=False):
    """Muted-trombone style speech (the 'wah-wah' adult voice)."""
    out = np.zeros(int(d * SR)); pos = 0.0; n = 0
    while pos < d - 0.08:
        sd = min(rng.uniform(0.7, 1.1) / rate, d - pos)
        last = pos + sd + 0.1 > d
        t = tt(sd)
        pitch = f0 * rng.uniform(0.88, 1.18)
        glide = np.linspace(1.0, 0.9, len(t))
        if question and last:
            glide = np.linspace(0.95, 1.45, len(t))
        ph = 2 * np.pi * np.cumsum(pitch * glide * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))) / SR
        src = ss.sawtooth(ph) * 0.6 + np.sin(ph) * 0.4
        f1, f2 = VOWELS[rng.integers(len(VOWELS))]
        v = bp(src, f1 * 0.8, f1 * 1.2) + 0.6 * bp(src, f2 * 0.85, f2 * 1.15) + 0.25 * lp(src, 500)
        env = np.minimum(1, t / 0.04) * np.minimum(1, (sd - t) / 0.06)
        i = int(pos * SR); out[i:i + len(v)] += (v * env)[: len(out) - i]
        pos += sd + (rng.uniform(0.0, 0.05) if rng.random() > 0.2 else rng.uniform(0.08, 0.16)); n += 1
    if phone:
        out = np.tanh(bp(out, 400, 2800) * 3) * 0.6
    return norm(out, 0.9)


def printer(d):
    t = tt(d)
    f = 110 * (1 + 0.03 * np.sin(2 * np.pi * 3 * t))
    buzz = lp(ss.square(2 * np.pi * np.cumsum(f) / SR), 1400) * (0.7 + 0.3 * np.sin(2 * np.pi * 24 * t))
    paper = hp(noise(d), 3000) * 0.25 * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t)))
    return fade(buzz * 0.5 + paper, 0.05, 0.15)


def ticking(d, rate=2.0):
    out = np.zeros(int(d * SR)); k = 0
    while k / rate < d - 0.02:
        c = bp(noise(0.012), 2500 if k % 2 else 1800, 6000 if k % 2 else 4000) * np.exp(-tt(0.012) * 300)
        i = int(k / rate * SR); out[i:i + len(c)] += c[: len(out) - i]
        k += 1
    return out


def cricket(d, every=0.7):
    out = np.zeros(int(d * SR)); t0 = 0.1
    while t0 < d - 0.15:
        for p in range(3):
            tp = tt(0.016)
            s = np.sin(2 * np.pi * 4600 * tp) * np.sin(np.pi * tp / 0.016)
            i = int((t0 + p * 0.032) * SR); out[i:i + len(s)] += s[: len(out) - i]
        t0 += every
    return out


def creak(d=0.5):
    t = tt(d)
    f = np.interp(t, [0, d * 0.4, d], [140, 260, 170]) * (1 + 0.05 * rng.standard_normal(len(t)).cumsum() / 400)
    s = ss.sawtooth(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 31 * t)))
    return fade(bp(s, 300, 1600), 0.03, 0.08)


def dingdong():
    out = np.zeros(int(2.4 * SR))
    for at, m in ((0, 76), (0.4, 72)):
        s = bell(midi(m), 1.8); i = int(at * SR); out[i:i + len(s)] += s
    return out


def stamp():
    t = tt(0.3)
    return np.sin(2 * np.pi * 85 * t) * np.exp(-t * 22) + lp(noise(0.3), 1500) * np.exp(-t * 60) * 0.7


def flutter(d=0.45):
    t = tt(d)
    return fade(bp(noise(d), 900, 4500) * (0.5 + 0.5 * np.sin(2 * np.pi * 28 * t)) * np.sin(np.pi * t / d), 0.01, 0.05) * 0.6


def wind(d, intensity=0.5):
    n = noise(d)
    base = lp(n, 350 + 500 * intensity) * smooth_rand(d, 0.6, 0.4, 1.0)
    howl = sum(bp(noise(d), f * 0.96, f * 1.04) * smooth_rand(d, 0.5, 0, 1) for f in (380, 520, 690))
    return norm(base * 0.8 + howl * 1.6 * intensity, 1.0)


def sigh(d=1.4):
    t = tt(d)
    env = np.minimum(1, t / 0.25) * np.clip((d - t) / (d - 0.25), 0, 1) ** 1.5
    tone = mumble(d * 0.6, 110, 1.5) * 0.15
    s = bp(noise(d), 300, 1400) * env
    s[: len(tone)] += tone
    return s


def roar(d=1.3):
    t = tt(d)
    s = lp(noise(d), 450) * (0.6 + 0.4 * np.sin(2 * np.pi * 17 * t)) + lp(ss.sawtooth(2 * np.pi * 52 * t), 300) * 0.6
    return fade(s * np.sin(np.pi * t / d), 0.05, 0.1)


def bloops(n=3):
    out = np.zeros(int(0.9 * SR))
    for k in range(n):
        t = tt(0.13); f = np.linspace(180, 900, len(t))
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.13)
        i = int((k * 0.22 + rng.uniform(0, 0.05)) * SR); out[i:i + len(s)] += s
    return out


def hiss(d=1.5):
    t = tt(d)
    return fade(hp(noise(d), 3000) * np.minimum(1, t / 0.1) * (0.8 + 0.2 * np.sin(2 * np.pi * 9 * t)), 0.02, 0.3) * 0.5


def wheeze(d=0.9):
    t = tt(d)
    s = bp(noise(d), 1400, 3600) + 0.2 * np.sin(2 * np.pi * 880 * t * (1 + 0.04 * np.sin(2 * np.pi * 7 * t)))
    return fade(s * np.sin(np.pi * t / d), 0.02, 0.05) * 0.6


def shuffle(d):
    t = tt(d)
    return lp(noise(d), 1100) * (np.abs(np.sin(2 * np.pi * 0.9 * t)) ** 3) * 0.7


def taps(d, rate=4):
    out = np.zeros(int(d * SR)); tpos = 0.1
    while tpos < d - 0.05:
        c = bp(noise(0.008), 2500, 7000) * np.exp(-tt(0.008) * 400)
        i = int(tpos * SR); out[i:i + len(c)] += c[: len(out) - i]
        tpos += rng.uniform(0.6, 1.6) / rate
    return out


def room_tone(d):
    t = tt(d)
    return lp(noise(d), 180) * 0.6 + np.sin(2 * np.pi * 50 * t) * 0.04 + np.sin(2 * np.pi * 100 * t) * 0.02


# ---------------- music ----------------
THEME = [76, 79, 84, 79, 81, 79, 76, 72, 74, 76, 77, 74, 79, None, 67, None]   # jaunty office theme
BASS = [48, 43, 48, 43, 53, 48, 53, 48, 43, 50, 43, 50, 48, 43, 48, 43]


def office_music(d, bpm=136):
    beat = 60 / bpm; out = np.zeros(int(d * SR)); k = 0
    while k * beat < d:
        m, b = THEME[k % 16], BASS[k % 16]
        i = int(k * beat * SR)
        if m:
            s = pluck(midi(m), 0.45) * 0.55
            out[i:i + len(s)] += s[: len(out) - i]
        if k % 2 == 0 or True:
            s = pluck(midi(b), 0.5) * 0.45
            out[i:i + len(s)] += s[: len(out) - i]
        k += 1
    return out


def music_box(notes, beat=0.42):
    out = np.zeros(int((len(notes) * beat + 1.5) * SR))
    for k, m in enumerate(notes):
        if m is None: continue
        s = bell(midi(m), 1.2) * 0.5
        i = int(k * beat * SR); out[i:i + len(s)] += s
    return out
