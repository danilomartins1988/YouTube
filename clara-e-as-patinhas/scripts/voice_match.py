#!/usr/bin/env python3
"""Voice-match check: is the lead singer of a new take the same "voice" as the brand references?

Eleven Music has no fixed voice ID, so consistency = locked prompt + this check + inpainting of drifting
sections. Policy and thresholds: intellectual-property/music-rights/VOICE_PROFILE.md.

Method (numpy + Demucs, open source MIT):
  1. Demucs (htdemucs, two stems) isolates the vocal stem.
  2. On voiced frames (vocal RMS within 30 dB of the loudest frame) compute:
     - f0 median (harmonic-sum pitch, 120-900 Hz)  -> tessitura
     - spectral centroid 300-5000 Hz               -> brightness
     - MFCC 1-12 mean (40 mel bands, c0 dropped)   -> timbre fingerprint
  3. Compare against reference JSONs (voice_reference/*.json) and between sections of the same song.

Usage:
  voice_match.py ref  NAME AUDIO START END              # build a reference from a clip of an approved song
  voice_match.py check AUDIO [--win 10] [--json OUT]    # check a take, section by section (windows of N s)
"""
import json, os, subprocess, sys, tempfile, glob
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFDIR = f'{ROOT}/intellectual-property/music-rights/voice_reference'
SR = 22050; N = 2048; HOP = 512
# Thresholds (calibrated 2026-11-27 on the two owner-approved songs, see VOICE_PROFILE.md)
MAX_F0_SEMITONES = 5.0      # HARD: section f0 median vs reference (catches octave jumps, chipmunk, male/child voice)
MAX_CENTROID_RATIO = 1.25   # HARD: much brighter/darker = different vocal colour or pitched-up voice
MFCC_FACTOR = 1.6           # HARD: MFCC distance <= 1.6x the spread between the approved references
WARN_CENTROID_DEV = 0.08    # WARN: section brightness differs >8% from the song's own median -> listen to it
MIN_VOICED = 150            # windows with fewer voiced frames are 'n/a' (instrument leakage, too little singing)


def separate(path, start=None, end=None):
    tmp = tempfile.mkdtemp(prefix='vm_', dir=os.environ.get('VM_TMP'))
    clip = f'{tmp}/in.wav'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', path]
    if start is not None:
        cmd += ['-ss', str(start), '-to', str(end)]
    subprocess.run(cmd + ['-ac', '2', '-ar', '44100', clip], check=True)
    subprocess.run([sys.executable, '-m', 'demucs', '--two-stems=vocals', '-n', 'htdemucs', '-o', tmp, clip],
                   check=True, capture_output=True)
    voc = glob.glob(f'{tmp}/htdemucs/*/vocals.wav')[0]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', voc, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    subprocess.run(['rm', '-rf', tmp])
    return np.frombuffer(raw, np.float32).copy()


def mel_fb(n_mels=40, fmin=80, fmax=8000):
    m = lambda f: 2595 * np.log10(1 + f / 700); im = lambda x: 700 * (10 ** (x / 2595) - 1)
    pts = im(np.linspace(m(fmin), m(fmax), n_mels + 2)); f = np.fft.rfftfreq(N, 1 / SR)
    fb = np.zeros((n_mels, len(f)))
    for i in range(n_mels):
        l, c, r = pts[i], pts[i + 1], pts[i + 2]
        fb[i] = np.clip(np.minimum((f - l) / (c - l), (r - f) / (r - c)), 0, None)
    return fb
FB = mel_fb()
DCT = np.cos(np.pi / 40 * (np.arange(40) + 0.5)[None, :] * np.arange(13)[:, None])
FREQ = np.fft.rfftfreq(N, 1 / SR); CAND = np.arange(120, 900, 1.0)


def features(x):
    if len(x) < N * 4:
        return None
    fr = np.lib.stride_tricks.sliding_window_view(x, N)[::HOP] * np.hanning(N)
    rms = np.sqrt((fr ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(rms / rms.max())
    v = fr[db > -30]
    if len(v) < 20:
        return None
    S = np.abs(np.fft.rfft(v, axis=1))
    P = S ** 2
    mf = (DCT @ np.log(P @ FB.T + 1e-10).T).T[:, 1:]  # frames x 12
    band = (FREQ > 300) & (FREQ < 5000)
    cen = (S[:, band] * FREQ[band]).sum(1) / (S[:, band].sum(1) + 1e-9)
    f0s = []
    for s in S[::4]:
        s = s / (s.max() + 1e-9)
        score = sum(np.interp(CAND * h, FREQ, s) * (0.85 ** (h - 1)) for h in range(1, 6))
        f0s.append(CAND[np.argmax(score)])
    return {'f0_median_hz': float(np.median(f0s)), 'f0_p10_hz': float(np.percentile(f0s, 10)),
            'f0_p90_hz': float(np.percentile(f0s, 90)), 'centroid_hz': float(np.median(cen)),
            'mfcc_mean': mf.mean(0).round(3).tolist(), 'voiced_frames': int(len(v))}


def mfcc_dist(a, b):
    return float(np.linalg.norm(np.array(a['mfcc_mean']) - np.array(b['mfcc_mean'])))


def load_refs():
    return {os.path.basename(p)[:-5]: json.load(open(p)) for p in sorted(glob.glob(f'{REFDIR}/*.json'))}


def main():
    a = sys.argv[1:]
    if a[0] == 'ref':
        name, path, s, e = a[1], a[2], float(a[3]), float(a[4])
        f = features(separate(path, s, e)); assert f, 'no voiced frames'
        f.update({'source': os.path.relpath(path, ROOT), 'start_s': s, 'end_s': e})
        os.makedirs(REFDIR, exist_ok=True); json.dump(f, open(f'{REFDIR}/{name}.json', 'w'), indent=1)
        print(json.dumps({k: v for k, v in f.items() if k != 'mfcc_mean'}))
        return
    path = a[1]; win = float(a[a.index('--win') + 1]) if '--win' in a else 10.0
    out = a[a.index('--json') + 1] if '--json' in a else None
    refs = load_refs(); assert refs, 'no references: run "ref" first'
    names = list(refs)
    ref_spread = max((mfcc_dist(refs[i], refs[j]) for i in names for j in names if i < j), default=8.0)
    mf_thr = MFCC_FACTOR * max(ref_spread, 4.0)
    ref_f0 = float(np.median([r['f0_median_hz'] for r in refs.values()]))
    ref_cen = float(np.median([r['centroid_hz'] for r in refs.values()]))
    voc = separate(path)
    total = len(voc) / SR; rows = []; fails = 0
    t = 0.0
    while t < total - 2:
        f = features(voc[int(t * SR):int(min(total, t + win) * SR)])
        if f and f['voiced_frames'] >= MIN_VOICED:
            st = 12 * np.log2(f['f0_median_hz'] / ref_f0)
            cr = f['centroid_hz'] / ref_cen
            md = min(mfcc_dist(f, r) for r in refs.values())
            ok = abs(st) <= MAX_F0_SEMITONES and 1 / MAX_CENTROID_RATIO <= cr <= MAX_CENTROID_RATIO and md <= mf_thr
            fails += not ok
            rows.append({'start': t, 'end': min(total, t + win), 'f0': round(f['f0_median_hz']), 'semitones_vs_ref': round(st, 1),
                         'centroid_ratio': round(cr, 2), 'mfcc_dist': round(md, 2), 'pass': bool(ok)})
            print(f"{t:6.1f}-{min(total, t + win):6.1f}s  f0 {f['f0_median_hz']:4.0f} Hz ({st:+.1f} st)  centroid x{cr:.2f}  "
                  f"MFCC d={md:.2f} (thr {mf_thr:.2f})  {'PASS' if ok else 'FAIL'}")
        t += win
    if rows:
        med = float(np.median([r['centroid_ratio'] for r in rows]))
        for r in rows:
            r['warn'] = bool(abs(r['centroid_ratio'] / med - 1) > WARN_CENTROID_DEV)
            if r['warn']:
                print(f"WARN {r['start']:.0f}-{r['end']:.0f}s: brightness {100*(r['centroid_ratio']/med-1):+.0f}% vs rest of song -> listen (possible timbre drift)")
    whole = features(voc)
    warns = sum(r.get('warn', False) for r in rows)
    verdict = ('PASS' if fails == 0 else f'FAIL ({fails} section(s) drift: fix by inpainting those ranges)') + (f', {warns} WARN' if warns else '')
    print(f'References: {", ".join(names)} | ref f0 {ref_f0:.0f} Hz, ref centroid {ref_cen:.0f} Hz, ref MFCC spread {ref_spread:.2f}')
    print(f"Whole song: f0 {whole['f0_median_hz']:.0f} Hz (p10-p90 {whole['f0_p10_hz']:.0f}-{whole['f0_p90_hz']:.0f}), "
          f"min MFCC d {min(mfcc_dist(whole, r) for r in refs.values()):.2f}  => {verdict}")
    if out:
        json.dump({'audio': os.path.relpath(path, ROOT), 'references': names, 'mfcc_threshold': mf_thr,
                   'sections': rows, 'verdict': verdict}, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main()
