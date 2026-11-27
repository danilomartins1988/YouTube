#!/usr/bin/env python3
"""Lead-voice consistency check (numpy only). For every Whisper word, estimate the sung f0 with a
harmonic-sum spectrum on the center (mid) channel (lead vocal sits in the middle), 150-800 Hz, and
the spectral centroid of the 300-4000 Hz band (timbre/brightness proxy). Reports per-segment medians.
Usage: voice_check.py AUDIO WHISPER.json [--label X]"""
import json, subprocess, sys
import numpy as np
SR = 22050
audio, wj = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', audio, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
st = np.frombuffer(raw, np.float32).reshape(-1, 2)
mid, side = st.mean(1), (st[:, 0] - st[:, 1]) / 2
j = json.load(open(wj, encoding='utf-8'))
N = 4096; f = np.fft.rfftfreq(N, 1 / SR)
cand = np.arange(150, 800, 1.0)
def f0_of(seg):
    if len(seg) < N: seg = np.pad(seg, (0, N - len(seg)))
    fr = np.lib.stride_tricks.sliding_window_view(seg, N)[::1024] * np.hanning(N)
    S = np.abs(np.fft.rfft(fr, axis=1)).mean(0)
    S = S / (S.max() + 1e-9)
    score = sum(np.interp(cand * h, f, S) * (0.85 ** (h - 1)) for h in range(1, 6))
    band = (f > 300) & (f < 4000)
    cen = float((S[band] * f[band]).sum() / (S[band].sum() + 1e-9))
    return float(cand[np.argmax(score)]), cen
rows = []
for s in j['segments']:
    ws = [w for w in j.get('words', []) if w['start'] >= s['start'] - 0.05 and w['end'] <= s['end'] + 0.05]
    f0s, cens = [], []
    for w in ws:
        a, b = int(w['start'] * SR), int(max(w['end'], w['start'] + 0.12) * SR)
        if b - a < 0.08 * SR: continue
        f0, c = f0_of(mid[a:b]); f0s.append(f0); cens.append(c)
    if not f0s: continue
    a, b = int(s['start'] * SR), int(s['end'] * SR)
    ms = float(np.sqrt((side[a:b] ** 2).mean() / ((mid[a:b] ** 2).mean() + 1e-12)))
    rows.append((s['start'], s['end'], float(np.median(f0s)), float(np.median(cens)), ms, s['text'].strip()[:50]))
    print(f"{s['start']:6.1f}-{s['end']:6.1f}  f0 med {np.median(f0s):5.0f} Hz  centroid {np.median(cens):5.0f} Hz  side/mid {ms:.2f}  {s['text'].strip()[:50]}")
f0 = np.array([r[2] for r in rows]); ce = np.array([r[3] for r in rows])
print(f'ALL: f0 median {np.median(f0):.0f} Hz (IQR {np.percentile(f0,25):.0f}-{np.percentile(f0,75):.0f}), centroid median {np.median(ce):.0f} Hz, centroid spread (max/min) {ce.max()/ce.min():.2f}')
