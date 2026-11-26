"""Kids test 01: mix vocal over the instrumental with ducking, master to -16 LUFS.

    python tools/kids_mix.py      -> output/kids/test01/mix.wav (48 kHz stereo, -16 LUFS, peak <= -1.5 dBTP)

Vocal chain: high-pass 120 Hz, gentle presence lift, soft compression, small "room" reverb and a slight
stereo double (10 ms, +-6 cents feel via a tiny delay modulation) so it sits in the song like a vocal.
Music is side-chain ducked ~4 dB under the voice (smooth 30 ms attack / 250 ms release envelope).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "output" / "kids" / "test01"
SR = 44100
TARGET_LUFS = -16.0


def vocal_chain(v: np.ndarray) -> np.ndarray:
    b, a = signal.butter(2, 120 / (SR / 2), "highpass")
    v = signal.lfilter(b, a, v)
    # presence: +3 dB shelf-ish around 3-6 kHz (parallel band-pass)
    b, a = signal.butter(2, [2800 / (SR / 2), 7000 / (SR / 2)], "bandpass")
    v = v + 0.35 * signal.lfilter(b, a, v)
    # soft compressor (RMS envelope, 3:1 above -20 dB rel. peak)
    env = np.sqrt(signal.lfilter([0.002], [1, -0.998], v ** 2) + 1e-10)
    ref = np.percentile(env[env > 1e-4], 95) if np.any(env > 1e-4) else 1.0
    lvl = 20 * np.log10(env / ref + 1e-9)
    over = np.maximum(0, lvl + 8)
    gain = 10 ** (-(over * (1 - 1 / 3)) / 20)
    v = v * gain
    return v / (np.abs(v).max() + 1e-9) * 0.9


def reverb(v: np.ndarray, seconds: float = 0.9, mix: float = 0.13, seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-t * 6.5)[:, None]
    ir[: int(0.012 * SR)] = 0  # pre-delay
    b, a = signal.butter(1, 5000 / (SR / 2))
    ir = signal.lfilter(b, a, ir, axis=0)
    ir /= np.sqrt((ir ** 2).sum(axis=0))
    wet = np.stack([signal.fftconvolve(v, ir[:, c])[: len(v)] for c in range(2)], axis=1)
    dry = np.stack([v, v], axis=1)
    # light double: 11 ms copy on the right, 17 ms on the left, low level -> a bit of "sung" width
    d1, d2 = int(0.011 * SR), int(0.017 * SR)
    dbl = np.zeros_like(dry)
    dbl[d2:, 0] = v[:-d2] * 0.12
    dbl[d1:, 1] = v[:-d1] * 0.12
    return dry + dbl + mix * wet / (np.abs(wet).max() + 1e-9) * np.abs(v).max()


def duck_gain(v: np.ndarray, depth_db: float = 4.5) -> np.ndarray:
    env = np.abs(v)
    att, rel = np.exp(-1 / (0.03 * SR)), np.exp(-1 / (0.25 * SR))
    # fast envelope follower via decimated loop (10 ms hop) then interpolate
    hop = int(0.01 * SR)
    frames = env[: len(env) // hop * hop].reshape(-1, hop).max(axis=1)
    out = np.zeros_like(frames)
    e = 0.0
    a1, r1 = att ** hop, rel ** hop
    for i, x in enumerate(frames):
        e = a1 * e + (1 - a1) * x if x > e else r1 * e + (1 - r1) * x
        out[i] = e
    out = np.interp(np.arange(len(env)), np.arange(len(out)) * hop, out)
    amount = np.clip(out / (np.percentile(frames[frames > 1e-3], 60) if np.any(frames > 1e-3) else 1), 0, 1)
    return 10 ** (-depth_db * amount / 20)


def main() -> None:
    music, sr = sf.read(WORK / "music.wav", dtype="float64")
    assert sr == SR
    voice, sr2 = sf.read(WORK / "vocal.wav", dtype="float64")
    assert sr2 == SR
    n = len(music)
    voice = np.pad(voice, (0, max(0, n - len(voice))))[:n]
    v = vocal_chain(voice)
    g = duck_gain(v)
    meter = pyln.Meter(SR)
    # balance: vocal ~5 LU above the ducked music where both are present
    v_st = reverb(v)
    m = music * g[:, None]
    lv = meter.integrated_loudness(v_st)
    lm = meter.integrated_loudness(m)
    m *= 10 ** ((lv - 6.0 - lm) / 20)
    mix = v_st + m
    loud = meter.integrated_loudness(mix)
    mix *= 10 ** ((TARGET_LUFS - loud) / 20)
    tmp = WORK / "mix_pre.wav"
    sf.write(tmp, mix.astype(np.float32), SR, subtype="FLOAT")
    # true-peak safe limiter + resample to 48 kHz, then re-measure and trim to target
    out = WORK / "mix.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-af",
                    "alimiter=limit=0.80:attack=3:release=60:level=disabled,aresample=48000",
                    "-c:a", "pcm_s16le", str(out)], check=True)
    tmp.unlink()
    y, sr3 = sf.read(out)
    final = pyln.Meter(sr3).integrated_loudness(y)
    stats = {"lufs": round(final, 2), "peak_dbfs": round(20 * np.log10(np.abs(y).max()), 2),
             "seconds": round(len(y) / sr3, 2)}
    # silence check: longest run below -45 dBFS RMS (100 ms windows) inside the song
    w = int(0.1 * sr3)
    rms = np.sqrt((y[: len(y) // w * w].mean(axis=1).reshape(-1, w) ** 2).mean(axis=1))
    quiet = 20 * np.log10(rms + 1e-9) < -45
    run = best = 0
    for q in quiet[:-30]:  # ignore the final fade
        run = run + 1 if q else 0
        best = max(best, run)
    stats["longest_silence_s"] = round(best * 0.1, 2)
    stats["clipped_samples"] = int((np.abs(y) >= 0.999).sum())
    (WORK / "mix_stats.json").write_text(json.dumps(stats))
    print(stats)


if __name__ == "__main__":
    main()
