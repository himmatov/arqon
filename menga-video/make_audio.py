"""Generates background music + cartoon sound effects synced to animation.html.
Output: audio-sfx-music.wav (60 s, 44.1 kHz stereo). Pure numpy, no samples needed.
"""
import wave
import numpy as np

SR = 44100
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
music = np.zeros(N)
sfx = np.zeros(N)


def t_arr(d):
    return np.arange(int(SR * d)) / SR


def env(n, a=0.005, r=None):
    e = np.ones(n)
    na = max(1, int(SR * a))
    e[:na] = np.linspace(0, 1, na)
    if r is None:
        e *= np.exp(-np.linspace(0, 6, n))
    else:
        nr = max(1, int(SR * r))
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    buf[i : i + len(sig)] += sig * gain


def lowpass(x, k=8):
    return np.convolve(x, np.ones(k) / k, mode="same")


# ---------- sound effects ----------
def pop(f=900):
    t = t_arr(0.12)
    fr = f * (1 + 1.5 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 35)


def whoosh(d=0.45, up=True):
    n = int(SR * d)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    # sweeping crude band filter: moving average with changing width
    for j, k in enumerate(np.linspace(40, 4, 6) if up else np.linspace(4, 40, 6)):
        a, b = j * n // 6, (j + 1) * n // 6
        out[a:b] = lowpass(x, int(k))[a:b]
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    return out * e * 2.2


def boing():
    t = t_arr(0.5)
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 5) + 200 * t
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6)


def ding(f=1320):
    t = t_arr(0.6)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 2.01 * t) + 0.25 * np.sin(2 * np.pi * f * 3.02 * t)
    return s * np.exp(-t * 7) * 0.5


def paper():
    n = int(SR * 0.12)
    x = rng.standard_normal(n) - lowpass(rng.standard_normal(n), 3)
    return x * np.exp(-np.linspace(0, 5, n)) * 0.6


def beep(f=1000, d=0.08):
    t = t_arr(d)
    return np.sign(np.sin(2 * np.pi * f * t)) * 0.25 * env(len(t), 0.002, 0.01)


def meow():
    t = t_arr(0.7)
    f = 500 + 450 * np.sin(np.pi * t / 0.7) ** 1.5
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)
    return s * np.sin(np.pi * t / 0.7) * 0.35


def thud():
    t = t_arr(0.35)
    return np.sin(2 * np.pi * (60 + 80 * np.exp(-t * 20)) * t) * np.exp(-t * 10) * 1.2


def fanfare(start):
    for k, (f, d) in enumerate([(523, 0.12), (659, 0.12), (784, 0.12), (1047, 0.6)]):
        t = t_arr(d + 0.2)
        s = sum(np.sign(np.sin(2 * np.pi * f * h * t)) / h for h in (1, 2))
        add(sfx, start + k * 0.12, lowpass(s, 6) * env(len(t), 0.01, 0.15) * 0.22)


def sad_trombone(start):
    for k, f in enumerate([392, 370, 349, 330]):
        d = 0.35 if k < 3 else 0.9
        t = t_arr(d)
        vib = 1 + (0.012 * np.sin(2 * np.pi * 6 * t) if k == 3 else 0)
        ph = 2 * np.pi * np.cumsum(f * vib) / SR
        s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph)
        add(sfx, start + k * 0.35, s * env(len(t), 0.02, 0.08) * 0.18)


def engine(d):
    n = int(SR * d)
    x = lowpass(rng.standard_normal(n), 60) * 4
    t = np.arange(n) / SR
    s = x + 0.3 * np.sin(2 * np.pi * 110 * t) * (1 + 0.2 * np.sin(2 * np.pi * 3 * t))
    e = np.minimum(1, np.minimum(t / 0.4, (d - t) / 0.4))
    return s * e * 0.35


def typing(start, nchars, speed=38):
    for k in range(0, nchars, 2):
        add(sfx, start + k / speed, pop(1800 + rng.integers(0, 600)) * 0.07)


# transitions
for b in [4, 11, 19, 26, 32, 41, 47, 50, 55.5]:
    add(sfx, b - 0.3, whoosh(0.6), 0.35)

# 1. Title
add(sfx, 0.1, pop(500), 0.5)
for s in (0.5, 0.8, 1.5, 1.8, 2.2):
    add(sfx, s, pop(800 + s * 200), 0.35)
add(sfx, 2.4, whoosh(1.2), 0.3)

# 2. Room
for s in np.arange(4.2, 5.7, 0.35):
    add(sfx, s, ding(1600), 0.12)  # sparkly hearts
add(sfx, 5.7, boing(), 0.45)
add(sfx, 6.0, pop(), 0.4); typing(6.0, 40)
add(sfx, 8.2, whoosh(0.4, False), 0.35)
add(sfx, 8.6, pop(700), 0.4); typing(8.6, 45)
for s in np.arange(8.4, 11, 0.45):
    add(sfx, s, whoosh(0.15), 0.25)  # slipper swish

# 3. Documents
for i in range(42):
    add(sfx, 11 + 0.2 + i * 0.16 + 0.9, paper(), 0.35)
add(sfx, 11.5, pop(), 0.35)
add(sfx, 15.0, pop(), 0.4); typing(15.0, 40)
add(sfx, 14.2, boing(), 0.3)

# 4. Study
add(sfx, 19.6, pop(), 0.4); typing(19.6, 40)
n = int(SR * 1.1)
add(sfx, 21.8, lowpass(rng.standard_normal(n), 2) * np.sin(np.linspace(0, np.pi, n)) * 0.3)  # brain steam
add(sfx, 22.9, pop(), 0.4); typing(22.9, 28)
add(sfx, 23.8, meow())
add(sfx, 24.3, pop(600), 0.4)

# 5. Yard
for s, ln in ((26.4, 36), (27.9, 34), (29.4, 28)):
    add(sfx, s, pop(), 0.4); typing(s, ln)
for k in range(3):
    add(sfx, 29.6 + k * 0.25, pop(1200 + k * 200), 0.25)

# 6. Hero
add(sfx, 32.0, thud(), 0.8)
fanfare(32.1)
add(sfx, 32.2, whoosh(1.0), 0.45)
add(sfx, 33.2, thud(), 0.7)
add(sfx, 33.4, pop(), 0.4); typing(33.4, 40)
add(sfx, 35.4, pop(500), 0.45)
for i in range(5):
    add(sfx, 35.8 + i * 0.55, ding(1046 * 2 ** (i / 12 * 2)), 0.6)
for s in np.arange(38.5, 41, 0.39):
    add(sfx, s, boing(), 0.18)
add(sfx, 38.8, pop(), 0.4); typing(38.8, 30)

# 7. Airport
for s in np.arange(41.3, 42.6, 0.06):
    add(sfx, s, beep(1400, 0.02), 0.5)
for s in np.arange(42.6, 45.5, 0.45):
    add(sfx, s, beep(900, 0.18), 0.6)
    add(sfx, s + 0.2, beep(700, 0.18), 0.6)
add(sfx, 41.8, pop(), 0.4); typing(41.8, 45)
add(sfx, 44.2, pop(), 0.4); typing(44.2, 40)

# 8. Flight
add(sfx, 47.0, engine(3.2))

# 9. Seoul
for s, ln in ((50.4, 14), (51.1, 45)):
    add(sfx, s, pop(), 0.4); typing(s, ln)
add(sfx, 52.7, pop(500), 0.45)
for i in range(3):
    add(sfx, 52.8 + i * 0.15, ding(1568), 0.35)
sad_trombone(53.5)

# 10. Outro
add(sfx, 55.55, pop(500), 0.5)
for s in (55.85, 56.1, 56.5):
    add(sfx, s, pop(900), 0.35)
for f in (523, 659, 784, 1047):
    add(sfx, 57.0, ding(f), 0.45)

# ---------- background music (upbeat 120 bpm, C–G–Am–F) ----------
BPM = 120
beat = 60 / BPM
chords = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [60, 64, 69]), (41, [60, 65, 69])]
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
melody = [72, 74, 76, 79, 76, 74, 72, 74, 71, 74, 79, 74, 72, 76, 81, 76, 77, 76, 74, 72, 69, 72, 74, 76]


def pluck(f, d, bright=1.0):
    t = t_arr(d)
    s = np.sin(2 * np.pi * f * t) + 0.4 * bright * np.sin(4 * np.pi * f * t) + 0.15 * bright * np.sin(6 * np.pi * f * t)
    return s * np.exp(-t * 6) * env(len(t), 0.004, 0.02)


bar = 0
t0 = 0.0
while t0 < DUR:
    root, notes = chords[bar % 4]
    for b in range(4):
        tb = t0 + b * beat
        add(music, tb, pluck(mtof(root), beat * 0.9, 0.3), 0.35)          # bass
        add(music, tb + beat / 2, pluck(mtof(root + 12), beat * 0.45, 0.3), 0.18)
        for m in notes:                                                     # off-beat chords
            add(music, tb + beat / 2, pluck(mtof(m), beat * 0.4), 0.07)
        k = int(SR * 0.04)                                                  # hi-hat
        add(music, tb + beat / 2, (rng.standard_normal(k) - lowpass(rng.standard_normal(k), 2)) * np.exp(-np.linspace(0, 8, k)), 0.05)
        if b % 2 == 0:                                                      # kick
            add(music, tb, thud(), 0.25)
    for j in range(6):                                                      # light melody
        if (bar // 4) % 2 == 1:
            m = melody[(bar * 6 + j) % len(melody)]
            add(music, t0 + j * (4 * beat / 6), pluck(mtof(m), 0.3, 0.6), 0.09)
    bar += 1
    t0 += 4 * beat

# fade music in/out, keep it low under voice
tt = np.arange(N) / SR
music *= np.clip(tt / 0.8, 0, 1) * np.clip((DUR - tt) / 1.5, 0, 1)
music *= 0.55
mix = music + sfx * 0.9
mix = np.tanh(mix * 1.1) * 0.85
peak = np.max(np.abs(mix))
mix = mix / peak * 0.89

stereo = np.stack([mix, mix], axis=1)
pcm = (stereo * 32767).astype("<i2")
with wave.open("audio-sfx-music.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("ok")
