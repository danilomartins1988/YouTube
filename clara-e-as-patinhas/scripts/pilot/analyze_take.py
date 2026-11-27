#!/usr/bin/env python3
"""Objective analysis of a take: tempo, key, melody simplicity (notes / range of the lead vocal), stereo, loudness.
Uses Demucs vocals (via voice_match.separate). Melody: harmonic-sum f0 per voiced frame -> MIDI notes.
Usage: analyze_take.py AUDIO [--json OUT]"""
import json, os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import voice_match as vm
SR = vm.SR
path = sys.argv[1]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
mix = np.frombuffer(raw, np.float32)
voc = vm.separate(path)
N, HOP = 2048, 512
# --- melody
fr = np.lib.stride_tricks.sliding_window_view(voc, N)[::HOP] * np.hanning(N)
rms = np.sqrt((fr ** 2).mean(1)) + 1e-9; v = fr[20 * np.log10(rms / rms.max()) > -25]
S = np.abs(np.fft.rfft(v, axis=1)); f0 = []
for s in S:
    s = s / (s.max() + 1e-9)
    sc = sum(np.interp(vm.CAND * h, vm.FREQ, s) * (0.85 ** (h - 1)) for h in range(1, 6))
    f0.append(vm.CAND[np.argmax(sc)])
midi = np.round(69 + 12 * np.log2(np.array(f0) / 440)).astype(int)
# fold octave errors toward the median register
med = int(np.median(midi)); midi = np.where(midi > med + 9, midi - 12, midi); midi = np.where(midi < med - 9, midi + 12, midi)
vals, cnt = np.unique(midi, return_counts=True); order = np.argsort(-cnt); cum = np.cumsum(cnt[order]) / cnt.sum()
notes90 = int(np.searchsorted(cum, 0.9) + 1)
names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
top = [f"{names[m % 12]}{m // 12 - 1}:{c / cnt.sum():.0%}" for m, c in zip(vals[order][:6], cnt[order][:6])]
# --- key (Krumhansl) on the mix
fm = np.lib.stride_tricks.sliding_window_view(mix, 4096)[::2048] * np.hanning(4096)
P = np.abs(np.fft.rfft(fm, axis=1)).mean(0); F = np.fft.rfftfreq(4096, 1 / SR)
chroma = np.zeros(12); ok = (F > 60) & (F < 2000)
for f, p in zip(F[ok], P[ok]): chroma[int(round(69 + 12 * np.log2(f / 440))) % 12] += p
maj = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); mnr = np.array([6.33, 2.68, 3.52, 5.38, 2.6, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
sc = [(np.corrcoef(np.roll(maj, k), chroma)[0, 1], f'{names[k]} major') for k in range(12)] + [(np.corrcoef(np.roll(mnr, k), chroma)[0, 1], f'{names[k]} minor') for k in range(12)]
key = max(sc)[1]
# --- tempo (onset autocorrelation 70-130 BPM)
H = 256; fo = np.lib.stride_tricks.sliding_window_view(mix, 1024)[::H] * np.hanning(1024)
Sp = np.abs(np.fft.rfft(fo, axis=1)); flux = np.maximum(np.diff(np.log1p(Sp), axis=0), 0).sum(1); flux -= flux.mean()
ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]; fps = SR / H
lags = np.arange(int(fps * 60 / 130), int(fps * 60 / 70)); bpm = 60 * fps / lags[np.argmax(ac[lags])]
res = {'audio': path, 'tempo_bpm': round(float(bpm), 1), 'key': key, 'lead_notes_covering_90pct': notes90,
       'lead_range_semitones_p5_p95': int(np.percentile(midi, 95) - np.percentile(midi, 5)), 'lead_top_notes': top,
       'lead_f0_median_hz': round(float(np.median(f0)))}
print(json.dumps(res, ensure_ascii=False))
if '--json' in sys.argv: json.dump(res, open(sys.argv[sys.argv.index('--json') + 1], 'w'), ensure_ascii=False, indent=1)
