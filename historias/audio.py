"""Cama sonora sintetizada para las historias: drone ambiental + whooshes de transición + SFX sincronizados."""
import wave
import numpy as np

SR = 48000
rng = np.random.default_rng(4)

def env(n, a, r):
    e = np.ones(n); a = int(a * SR); r = int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.exp(-np.linspace(0, 6, r))
    return e

def onepole(x, fc):
    """Paso bajo de un polo con corte variable (fc escalar o array)."""
    fc = np.broadcast_to(fc, x.shape); a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a[i]) * x[i] + a[i] * s; y[i] = s
    return y

def bandsweep(dur, f0, f1):
    n = int(dur * SR); x = rng.standard_normal(n); fc = np.geomspace(f0, f1, n)
    y = onepole(x, np.minimum(fc * 1.8, 3200)) - onepole(x, fc * 0.55)
    return y / (np.abs(y).max() + 1e-9)

def whoosh(dur=0.55):
    n = int(dur * SR); y = bandsweep(dur, 260, 1400) * np.sin(np.linspace(0, np.pi, n)) ** 2
    pan = np.linspace(0, 1, n)
    return np.stack([y * np.cos(pan * np.pi / 2), y * np.sin(pan * np.pi / 2)], 1) * 0.30

def thud():
    d = 0.9; n = int(d * SR); t = np.arange(n) / SR
    f = 45 + 80 * np.exp(-t * 14); ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) * np.exp(-t * 5.5) + 0.35 * onepole(rng.standard_normal(n), 900) * np.exp(-t * 30)
    return np.stack([y, y], 1) * 0.75

def tick():
    n = int(0.03 * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * (1700 + rng.uniform(-200, 200)) * t) * np.exp(-t * 260)
    p = rng.uniform(0.3, 0.7)
    return np.stack([y * (1 - p), y * p], 1) * 0.10

def ding():
    d = 1.6; n = int(d * SR); t = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 880 * t) + 0.35 * np.sin(2 * np.pi * 1318.5 * t) + 0.2 * np.sin(2 * np.pi * 440 * t)) * np.exp(-t * 3.2) * env(n, 0.004, 0)
    return np.stack([y, y], 1) * 0.12

def swell(dur):
    n = int(dur * SR); y = bandsweep(dur, 200, 1200) * np.linspace(0, 1, n) ** 2.5
    return np.stack([y, y], 1) * 0.22

def fall(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.geomspace(500, 70, n); y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.5) * 0.5
    y += bandsweep(dur, 900, 200) * np.exp(-t * 2.5) * 0.5
    return np.stack([y, y], 1) * 0.25

def drone(total):
    n = int(total * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for f, a, lf in [(55, .55, .07), (82.41, .35, .05), (110, .30, .09), (164.81, .16, .06), (220, .08, .11)]:
        y += a * np.sin(2 * np.pi * f * t + 3 * np.sin(2 * np.pi * 0.13 * t)) * (0.65 + 0.35 * np.sin(2 * np.pi * lf * t))
    air = onepole(rng.standard_normal(n), 500) * 0.6
    y = y * 0.16 + air * 0.08
    fade = np.minimum(1, np.minimum(t / 1.5, (total - t) / 1.2))
    return np.stack([y, y], 1) * fade[:, None]

def read_wav(path):
    with wave.open(path) as w:
        ch, sr, raw = w.getnchannels(), w.getframerate(), w.readframes(w.getnframes())
    x = np.frombuffer(raw, np.int16).astype(np.float64) / 32768
    x = x.reshape(-1, ch).mean(1)
    if sr != SR: x = np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)
    return x


def build(tl, out, voz=None):
    total = tl["total"]; n = int(total * SR)
    mix = drone(total)
    def put(sig, at):
        i = int(at * SR); j = min(n, i + len(sig))
        if i < n: mix[i:j] += sig[:j - i]
    for s in tl["starts"][1:]: put(whoosh(), s - 0.3)
    for e in tl["events"]:
        k = e["type"]
        if k == "ticks":
            for tt in np.arange(e["t"], e["t"] + e["dur"], 1 / e["rate"]): put(tick(), tt + rng.uniform(0, 0.02))
        elif k == "thud": put(thud(), e["t"])
        elif k == "ding": put(ding(), e["t"])
        elif k == "swell": put(swell(e["dur"]), e["t"] - e["dur"] + 0.15)
        elif k == "fall": put(fall(e["dur"]), e["t"])
    mix *= 10 ** (-3 / 20) / np.abs(mix).max()
    if voz:
        # con voz: la cama y los efectos quedan por debajo (~-15 dB) y la voz manda
        v = read_wav(voz)[:n]; mix *= 0.18
        mix[:len(v)] += np.stack([v, v], 1) * 0.9
        mix *= 10 ** (-1.5 / 20) / np.abs(mix).max()
    pcm = (mix * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
