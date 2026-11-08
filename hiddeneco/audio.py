"""Original sound design, generated from code (no third-party audio, no licence risk).

* sound effects: whoosh (scene transitions), pop (reveals), tick (counters), hit (title beats)
* music bed: a slow, soft chord pad, ducked automatically under narration
* mixing: narration + bed + effects, then EBU R128 loudness normalisation with FFmpeg
"""
from __future__ import annotations

import subprocess
import wave
from pathlib import Path

import numpy as np

RATE = 48000


def _env(n: int, attack: float, release: float, rate: int = RATE) -> np.ndarray:
    a = max(1, int(attack * rate))
    r = max(1, int(release * rate))
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a) if a < n else np.linspace(0, 1, n)
    if r < n:
        e[-r:] *= np.linspace(1, 0, r) ** 2
    return e


def _lowpass(x: np.ndarray, cutoff: np.ndarray | float, rate: int = RATE) -> np.ndarray:
    """One-pole low-pass with optionally time-varying cutoff (Hz)."""
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    alpha = 1 - np.exp(-2 * np.pi * cutoff / rate)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def sfx(kind: str, rate: int = RATE, seed: int = 0) -> np.ndarray:
    rng = np.random.default_rng(seed)
    if kind == "whoosh":
        n = int(0.55 * rate)
        t = np.linspace(0, 1, n)
        noise = rng.normal(0, 1, n)
        sweep = 300 + 5200 * np.sin(np.pi * t) ** 2          # filter opens then closes
        y = _lowpass(noise, sweep, rate) - _lowpass(noise, sweep * 0.25, rate)
        y *= np.sin(np.pi * t) ** 1.5
    elif kind == "pop":
        n = int(0.12 * rate)
        t = np.arange(n) / rate
        f = 880 * np.exp(-t * 18) + 420
        y = np.sin(2 * np.pi * np.cumsum(f) / rate) * np.exp(-t * 38)
    elif kind == "tick":
        n = int(0.035 * rate)
        t = np.arange(n) / rate
        y = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 160)
    elif kind == "intro":                                    # the channel's 5-second sonic signature
        from hiddeneco.intro import signature
        y = signature(rate)
    elif kind == "hit":
        n = int(0.9 * rate)
        t = np.arange(n) / rate
        body = np.sin(2 * np.pi * (48 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5)
        trans = _lowpass(rng.normal(0, 1, n), 2500, rate) * np.exp(-t * 60) * 0.5
        y = body + trans
    else:
        raise KeyError(f"Unknown sfx '{kind}'")
    return (y / (np.max(np.abs(y)) + 1e-9)).astype(np.float32)


CHORDS = {  # A-minor family, voiced low and close; frequencies in Hz
    "Am": [110.00, 130.81, 164.81, 220.00],
    "F": [87.31, 130.81, 174.61, 220.00],
    "C": [130.81, 164.81, 196.00, 261.63],
    "G": [98.00, 123.47, 146.83, 196.00],
    "E": [82.41, 103.83, 123.47, 164.81],
    "Em": [82.41, 123.47, 164.81, 196.00],
    "Dm": [73.42, 110.00, 146.83, 174.61],
    "D": [73.42, 110.00, 146.83, 185.00],
    "Bb": [116.54, 146.83, 174.61, 233.08],
    "Gm": [98.00, 116.54, 146.83, 196.00],
    "A": [110.00, 138.59, 164.81, 220.00],
}

# music direction per visual tone (adaptive visual storytelling): progression, chord length, pulse (Hz, depth),
# low drone (Hz or 0), octave shift, airy shimmer
MOODS = {
    "bright": {"progression": ("Am", "F", "C", "G"), "chord_seconds": 6.0},
    "trade": {"progression": ("C", "G", "Am", "F"), "chord_seconds": 5.0},
    "strategy": {"progression": ("C", "G", "Am", "F"), "chord_seconds": 6.0, "pulse": (0.5, 0.12)},
    "tech": {"progression": ("Em", "C", "G", "D"), "chord_seconds": 6.0, "shimmer": 0.18},
    "history": {"progression": ("Dm", "Am", "C", "G"), "chord_seconds": 8.0, "octave": 0.5},
    "thriller": {"progression": ("Am", "Am", "F", "E"), "chord_seconds": 8.0, "pulse": (0.9, 0.3), "drone": 55.0, "octave": 0.5},
    "crisis": {"progression": ("Dm", "Bb", "Gm", "A"), "chord_seconds": 5.0, "pulse": (1.6, 0.35), "drone": 73.42},
    "reflective": {"progression": ("Am", "F", "C", "G"), "chord_seconds": 9.0, "octave": 0.5},
    "spectacle": {"progression": ("Em", "C", "G", "D"), "chord_seconds": 4.0, "pulse": (2.0, 0.25), "shimmer": 0.12},
}


def music_bed(seconds: float, rate: int = RATE, progression=("Am", "F", "C", "G"),
              chord_seconds: float = 6.0, mood: str | None = None) -> np.ndarray:
    """Original ambient pad: detuned sines with slow swells, crossfaded chord changes. `mood` (a visual tone name)
    picks the progression, tempo, pulse and drone of MOODS."""
    m = MOODS.get(mood or "", {})
    progression = m.get("progression", progression)
    chord_seconds = m.get("chord_seconds", chord_seconds)
    octave, shimmer = m.get("octave", 1.0), m.get("shimmer", 0.0)
    n = int(seconds * rate)
    out = np.zeros(n, dtype=np.float64)
    seg = int(chord_seconds * rate)
    fade = int(1.5 * rate)
    t_all = np.arange(seg + fade) / rate
    k = 0
    for start in range(0, n, seg):
        chord = [f * octave for f in CHORDS[progression[k % len(progression)]]]
        k += 1
        length = min(seg + fade, n - start)
        t = t_all[:length]
        tone = np.zeros(length)
        for i, f in enumerate(chord):
            for detune, amp in ((1.0, 1.0), (1.003, 0.6), (0.997, 0.6), (2.0, 0.18)):
                phase = (i * 1.7 + detune * 3.1) % (2 * np.pi)
                tone += amp * np.sin(2 * np.pi * f * detune * t + phase)
            if shimmer:
                tone += shimmer * np.sin(2 * np.pi * f * 4 * t + i) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 1.5 + i))
        tone *= 0.75 + 0.25 * np.sin(2 * np.pi * t / chord_seconds - np.pi / 2)  # slow swell
        tone *= _env(length, min(fade, length) / rate, min(fade, length) / rate, rate)
        out[start:start + length] += tone
    if m.get("drone"):
        ta = np.arange(n) / rate
        out += 0.9 * np.sin(2 * np.pi * m["drone"] * ta) * (0.7 + 0.3 * np.sin(2 * np.pi * ta / 11))
    if m.get("pulse"):
        hz, depth = m["pulse"]
        ta = np.arange(n) / rate
        out *= (1 - depth) + depth * (0.5 + 0.5 * np.sin(2 * np.pi * hz * ta)) ** 4
    out /= np.max(np.abs(out)) + 1e-9
    out *= _env(n, 2.0, 3.0, rate)
    return out.astype(np.float32)


def mood_bed(seconds: float, moods: list[tuple[float, float, str]], rate: int = RATE, xfade: float = 2.0) -> np.ndarray:
    """A music bed that follows the story: one pad per (start, end, mood) run, cross-faded at the turning points."""
    n = int(seconds * rate)
    out = np.zeros(n, dtype=np.float32)
    for s0, s1, mood in moods:
        a, b = max(0.0, s0 - xfade / 2), min(seconds, s1 + xfade / 2)
        if b <= a:
            continue
        chunk = music_bed(b - a, rate, mood=mood)
        i = int(a * rate)
        out[i:i + len(chunk)] += chunk[: max(0, n - i)]
    return out


def envelope(x: np.ndarray, rate: int = RATE, window: float = 0.25) -> np.ndarray:
    w = max(1, int(window * rate))
    kernel = np.ones(w) / w
    return np.convolve(np.abs(x), kernel, mode="same")


def mix(voice: np.ndarray, events: list[tuple[float, str, float]], music: bool, rate: int = RATE,
        music_level: float = 0.11, duck_to: float = 0.035, moods: list[tuple[float, float, str]] | None = None) -> np.ndarray:
    """voice: float32 mono in [-1, 1]. events: (seconds, kind, gain). moods: optional (start, end, tone) runs from the
    visual direction plan (the music follows the story). Returns float32 mix."""
    out = voice.astype(np.float32).copy()
    if music:
        bed = (mood_bed(len(voice) / rate, moods, rate) if moods else music_bed(len(voice) / rate, rate))[: len(voice)]
        env = envelope(voice, rate)
        speaking = np.clip(env / (np.percentile(env, 90) * 0.35 + 1e-9), 0, 1)
        gain = music_level - (music_level - duck_to) * speaking
        for sec, kind, _g in events:                       # the intro carries its own music: bed out underneath
            if kind == "intro":
                s0, s1 = int(max(0.0, sec - 0.3) * rate), int((sec + 5.3) * rate)
                ramp = np.ones(len(gain))
                ramp[s0:s1] = 0.0
                gain = gain * np.convolve(ramp, np.ones(int(0.3 * rate)) / int(0.3 * rate), mode="same")
        out[: len(bed)] += bed * gain[: len(bed)]
    for i, (sec, kind, g) in enumerate(events):
        clip = sfx(kind, rate, seed=i) * g
        s = int(max(0.0, sec) * rate)
        e = min(len(out), s + len(clip))
        if e > s:
            out[s:e] += clip[: e - s]
    peak = np.max(np.abs(out))
    if peak > 0.98:
        out *= 0.98 / peak
    return out


def read_wav(path: Path) -> tuple[np.ndarray, int]:
    with wave.open(str(path), "rb") as w:
        rate = w.getframerate()
        pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return (pcm.astype(np.float32) / 32768.0), rate


def write_wav(path: Path, x: np.ndarray, rate: int = RATE) -> Path:
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(pcm.tobytes())
    return path


def loudnorm(src: Path, dst: Path, lufs: float, rate: int = RATE) -> Path:
    """Two-pass EBU R128 normalisation: measure, then apply linear gain to hit the target."""
    import json
    target = f"I={lufs}:TP=-1.5:LRA=11"
    probe = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
                            f"loudnorm={target}:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True, check=True).stderr
    m = json.loads(probe[probe.rindex("{"):probe.rindex("}") + 1])
    second = (f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
              f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
              f":offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af", second, "-ar", str(rate),
                    str(dst)], check=True)
    return dst
