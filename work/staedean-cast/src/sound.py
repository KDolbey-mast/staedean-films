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


# ---------------- the cue sheet ----------------
keys = [os.path.basename(p)[:5] for p in sorted(glob.glob("frames/*.png"))]
start, tpos = {}, 0.0
for k in keys:
    start[k] = tpos; tpos += T[k]
TOTAL = tpos
mix = {"music": np.zeros(int((TOTAL + 2) * SR)), "sfx": np.zeros(int((TOTAL + 2) * SR)), "amb": np.zeros(int((TOTAL + 2) * SR))}


def at(key, off, sig, gain=1.0, bus="sfx"):
    i = int((start[key] + off) * SR)
    buf = mix[bus]
    buf[i:i + len(sig)] += sig[: len(buf) - i] * gain


def span(k1, k2):
    return start[k2] + T[k2] - start[k1]


def bench_signature(key):
    """The same little sound every time he sits down: creak, then the clock."""
    at(key, 0.0, creak(0.45), 0.5)
    at(key, 0.35, ticking(T[key] - 0.35), 0.35)


# SCENE 1: office. Music and room tone, hard stop when the mountain appears.
at("S1_01", 0, room_tone(span("S1_01", "S2_01")), 0.08, "amb")
m = office_music(span("S1_01", "S2_01"))
m[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
at("S1_01", 0, m, 0.32, "music")
at("S1_01", 0.3, scribble(T["S1_01"] - 0.6), 0.5)
at("S1_02", 0.0, pop(), 0.45)
at("S1_03", 0.0, scribble(0.7), 0.5); at("S1_03", 0.8, fizzle(0.6), 0.35)
at("S1_04", 0.0, whoosh(0.7), 0.35); at("S1_04", 0.75, clang(), 0.35)
at("S1_05", 0.2, scribble(0.9), 0.5)
at("S1_06", 0.0, pop(), 0.45)
at("S1_07", 0.2, scribble(0.8), 0.4)
at("S1_08", 0.0, swell([60, 64, 67, 72, 76], 3.0), 0.28, "music")

# SCENE 2: the reveal
at("S2_02", 0.05, dun_dun_dun(), 0.45, "music")
at("S2_02", 0, wind(span("S2_02", "S2_04"), 0.25), 0.07, "amb")
at("S2_03", 1.3, gulp(), 0.35)
at("S2_04", 0.1, music_box([67, 72, 76], 0.22), 0.5, "music")
at("S2_04", 0.3, footsteps(T["S2_04"] - 0.5, 2.4), 0.3)

# SCENE 3: the first checkpoint
at("S3_01", 0, wind(span("S3_01", "S3_09"), 0.3), 0.07, "amb")
at("S3_01", 0.0, footsteps(T["S3_01"] - 0.3, 2.4), 0.3)
at("S3_02", 0.1, mumble(T["S3_02"] - 0.5, 165, 8.0), 0.45)
at("S3_03", 0.2, mumble(0.9, 260, 4.5), 0.4)
at("S3_04", 0.0, printer(T["S3_04"] - 0.3), 0.3)
bench_signature("S3_05")
at("S3_06", 0, ticking(T["S3_06"]), 0.35)
for o in (0.05, 0.5, 0.95): at("S3_06", o, flutter(), 0.4)
at("S3_07", 0, ticking(T["S3_07"]), 0.35); at("S3_07", 0.2, cricket(T["S3_07"] - 0.4), 0.08); at("S3_07", 0.5, flutter(), 0.3)
at("S3_08", 0.0, dingdong(), 0.3)
at("S3_09", 0.0, stamp(), 0.6); at("S3_09", 0.3, stamp(), 0.6); at("S3_09", 0.8, footsteps(T["S3_09"] - 1.0, 2.0), 0.3)

# SCENE 4: the climb (the bench signature is the running gag)
at("S4_01", 0, wind(span("S4_01", "S4_09"), 0.45), 0.09, "amb")
at("S4_01", 0.0, footsteps(T["S4_01"] - 0.2, 1.7, heavy=0.4), 0.32)
at("S4_02", 0.0, mumble(T["S4_02"] - 0.3, 230, 6.0, phone=True), 0.18)
at("S4_02", 0.15, mumble(T["S4_02"] - 0.7, 160, 8.5), 0.42)
at("S4_03", 0.0, mumble(0.7, 230, 5.0, phone=True), 0.25); at("S4_03", 0.9, gulp(), 0.25)
bench_signature("S4_04"); at("S4_04", 0.4, flutter(), 0.35)
at("S4_05", 0.0, flutter(0.3), 0.3); at("S4_05", 0.1, mumble(T["S4_05"] - 0.5, 175, 10.0), 0.42)
bench_signature("S4_06"); at("S4_06", 0.3, cricket(1.0), 0.07); at("S4_06", 0.5, flutter(), 0.3)
at("S4_07", 0.05, mumble(0.5, 120, 5.0), 0.4); at("S4_07", 0.6, sigh(1.0), 0.35)
bench_signature("S4_08"); at("S4_08", 0, wind(T["S4_08"], 0.8), 0.08, "amb")
at("S4_09", 0.2, flutter(0.6), 0.2)

# SCENE 5: the fork
at("S5_01", 0, wind(span("S5_01", "S5_04"), 0.6), 0.12, "amb")
at("S5_02", 0.3, roar(1.3), 0.35)
at("S5_03", 0.4, bloops(), 0.3)
at("S5_04", 0.2, sigh(1.5), 0.45); at("S5_04", 1.6, footsteps(1.0, 1.5, heavy=0.5, snow=0.4), 0.3)

# SCENE 6: final ascent, a blizzard that cuts out at the summit
bliz = wind(span("S6_01", "S6_04"), 1.0)
bliz[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
at("S6_01", 0, bliz, 0.3, "amb")
at("S6_01", 0.0, footsteps(T["S6_01"] - 0.2, 1.0, heavy=0.8, snow=1.0), 0.35); at("S6_01", 0.0, shuffle(T["S6_01"] - 0.2), 0.15)
at("S6_02", 0.5, wheeze(1.0), 0.4)
at("S6_03", 0.3, hiss(2.2), 0.28)
at("S6_04", 0.0, shuffle(T["S6_04"]), 0.3)

# SCENE 7: the summit. Calm, a hopeful little tune, then nothing.
at("S7_01", 0, lp(noise(span("S7_01", "S7_05")), 500), 0.02, "amb")
at("S7_01", 0.2, taps(T["S7_01"] - 0.4), 0.25); at("S7_01", 0.4, shuffle(T["S7_01"] - 0.8), 0.25)
mb = music_box([76, 79, 84, 79, 81, 79, 76, 72], 0.4)
cut = int(T["S7_02"] * SR); mb = mb[:cut]; mb[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
at("S7_02", 0.0, mb, 0.35, "music"); at("S7_02", 0.1, taps(T["S7_02"] - 0.6), 0.2)
at("S7_03", 0.25, mumble(1.0, 140, 3.2, question=True), 0.5)
at("S7_04", 2.9, cricket(0.3, 1), 0.09)
at("S7_05", 0.4, fizzle(0.8), 0.4)
at("S7_05", 1.8, music_box([72, None, 67], 0.6), 0.35, "music")

# ---------------- mixdown ----------------
music = mix["music"] * 0.9
sfx = mix["sfx"]
amb = mix["amb"]
# duck music a little under speech/sfx
env = np.convolve(np.abs(sfx), np.ones(4410) / 4410, mode="same")
music = music * (1 - 0.4 * np.clip(env / (env.max() or 1) * 4, 0, 1))
out = music + sfx + amb
out = out[: int(TOTAL * SR)]
out = np.tanh(out * 1.2) / np.tanh(1.2)
out = norm(out, 0.89)
stereo = np.stack([out, out], 1)
wavfile.write("vid/soundtrack.wav", SR, (stereo * 32767).astype(np.int16))
print("soundtrack", round(TOTAL, 2), "s")
