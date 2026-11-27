#!/usr/bin/env python3
"""Can language B's vocals sit on language A's instrumental? Per 10 s window: beat-grid lag (onset cross-correlation, +-150 ms)
and harmony similarity (12-bin chroma cosine) between the two Demucs instrumentals.
Usage: align_check.py A_no_vocals.wav B_no_vocals.wav"""
import subprocess, sys, numpy as np
SR = 22050
def load(p): return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
a, b = load(sys.argv[1]), load(sys.argv[2]); n = min(len(a), len(b))
H, N = 256, 1024
def onset(x):
    fr = np.lib.stride_tricks.sliding_window_view(x, N)[::H] * np.hanning(N); S = np.log1p(np.abs(np.fft.rfft(fr, axis=1)))
    o = np.maximum(np.diff(S, axis=0), 0).sum(1); return (o - o.mean()) / (o.std() + 1e-9)
def chroma(x):
    fr = np.lib.stride_tricks.sliding_window_view(x, 4096)[::2048] * np.hanning(4096); P = np.abs(np.fft.rfft(fr, axis=1)).mean(0)
    F = np.fft.rfftfreq(4096, 1 / SR); c = np.zeros(12); ok = (F > 60) & (F < 2000)
    np.add.at(c, (np.round(69 + 12 * np.log2(F[ok] / 440)).astype(int)) % 12, P[ok]); return c / np.linalg.norm(c)
fps = SR / H; maxlag = int(0.15 * fps); res = []
for t in range(0, int(n / SR) - 5, 10):
    sa, sb = a[t * SR:(t + 10) * SR], b[t * SR:(t + 10) * SR]
    oa, ob = onset(sa), onset(sb); L = min(len(oa), len(ob)); oa, ob = oa[:L], ob[:L]
    cc = [np.dot(oa[max(0, k):L + min(0, k)], ob[max(0, -k):L - max(0, k)]) / L for k in range(-maxlag, maxlag + 1)]
    lag = (np.argmax(cc) - maxlag) / fps * 1000; peak = max(cc)
    sim = float(np.dot(chroma(sa), chroma(sb)))
    res.append((t, lag, peak, sim)); print(f'{t:4d}-{t+10:4d}s  lag {lag:+6.0f} ms  onset corr {peak:.2f}  chroma cos {sim:.3f}')
lags = np.array([r[1] for r in res]); sims = np.array([r[3] for r in res])
print(f'median |lag| {np.median(np.abs(lags)):.0f} ms, max |lag| {np.abs(lags).max():.0f} ms, median chroma cos {np.median(sims):.3f}, min {sims.min():.3f}')
