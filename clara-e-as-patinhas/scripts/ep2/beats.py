#!/usr/bin/env python3
"""Beat/tempo analysis (ep. 002 copy: 85-115 BPM search range, writes music/analysis/ep2/beats.json) with numpy only (spectral-flux onset envelope,
autocorrelation tempo, comb-filter phase, local drift check). Writes music/analysis/ep2/beats.json."""
import json, subprocess, sys
import numpy as np
SR = 22050; HOP = 256
audio = sys.argv[1]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32)
N = 2048; win = np.hanning(N)
frames = np.lib.stride_tricks.sliding_window_view(np.pad(x, (N // 2, N // 2)), N)[::HOP] * win
S = np.abs(np.fft.rfft(frames, axis=1))
S = np.log1p(100 * S)
flux = np.maximum(0, np.diff(S, axis=0)).sum(1); flux = np.concatenate([[0], flux])
flux = flux - np.convolve(flux, np.ones(16) / 16, 'same'); flux = np.maximum(flux, 0)
fps = SR / HOP
env = (flux - flux.mean()) / (flux.std() + 1e-9)
ac = np.correlate(env, env, 'full')[len(env) - 1:]
lags = np.arange(len(ac)) / fps
cand = []
for bpm in np.arange(85, 115.01, 0.05):
    lag = 60 / bpm * fps
    s = sum(np.interp(lag * k, np.arange(len(ac)), ac) for k in (1, 2, 4))
    cand.append((s, bpm))
bpm = max(cand)[1]
period = 60 / bpm
# phase: comb sum of env at beat positions
t_env = np.arange(len(env)) / fps
best = None
for ph in np.arange(0, period, 0.005):
    bt = np.arange(ph, t_env[-1], period)
    sc = np.interp(bt, t_env, env).sum()
    if best is None or sc > best[0]:
        best = (sc, ph)
phase = best[1]
beats = np.arange(phase, t_env[-1] - 0.05, period)
# local drift: best local offset per 8-bar window
drift = []
for w0 in np.arange(0, t_env[-1] - 16, 16.0):
    bt0 = beats[(beats >= w0) & (beats < w0 + 16)]
    offs = np.arange(-0.08, 0.081, 0.005)
    sc = [np.interp(bt0 + o, t_env, env).sum() for o in offs]
    drift.append((round(float(w0), 1), round(float(offs[int(np.argmax(sc))]), 3)))
# downbeat: which beat index mod 4 has the strongest low-frequency energy (kick on 1)
low = S[:, 1:12].sum(1); low = (low - low.mean()) / low.std()
acc = [np.interp(beats[k::4], t_env, low).sum() for k in range(4)]
d0 = int(np.argmax(acc))
out = {'bpm': round(float(bpm), 3), 'period_s': round(float(period), 5), 'phase_s': round(float(phase), 4), 'downbeat_beat_index': d0,
       'n_beats': len(beats), 'beats_s': [round(float(b), 4) for b in beats], 'local_offset_by_16s_window': drift,
       'downbeat_scores': [round(float(a), 2) for a in acc]}
json.dump(out, open('music/analysis/ep2/beats.json', 'w'), indent=1)
print('BPM', out['bpm'], 'phase', out['phase_s'], 'downbeat idx', d0, acc, 'drift', drift)
