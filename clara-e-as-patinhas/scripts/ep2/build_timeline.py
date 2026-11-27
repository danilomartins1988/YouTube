#!/usr/bin/env python3
"""Ep. 002 timeline from the REAL master: Whisper words (+ manual fixes from clip re-checks), beat grid,
sections, ACHOU cues, bark cues, and per-frame (24 fps) mouth opening + viseme class for Clara.
Writes music/compositions/cade_achou_timeline.json"""
import json, re, subprocess
import numpy as np
ROOT = __file__.rsplit('/scripts/', 1)[0]
FPS = 24
W = json.load(open(f'{ROOT}/music/analysis/ep2/whisper_v1.json', encoding='utf-8'))['words']
B = json.load(open(f'{ROOT}/music/analysis/ep2/beats.json'))
words = []
for w in W:
    a, b, txt = w['start'], w['end'], w['word']
    if txt == 'Achou' and 98 < a < 99: a, b = 98.28, 98.84          # clip re-check (whole bridge clip)
    if txt == 'Tapou' and a > 100: txt = 'Tapa'                      # clip re-check of the final verse
    if b - a < 0.14: b = a + 0.14
    words.append({'w': txt, 'a': round(a, 3), 'b': round(b, 3)})
BAR = 2.4
SECS = [('intro', 0, 2), ('refrao', 2, 10), ('estrofe1', 10, 16), ('refrao_curto1', 16, 20), ('estrofe2', 20, 26),
        ('refrao_curto2', 26, 30), ('estrofe3', 30, 36), ('ponte', 36, 42), ('final', 42, 48), ('encerramento', 48, 52)]
sections = {n: (a * BAR, b * BAR) for n, a, b in SECS}
achou = [33.84, 58.66, 82.20, 98.28, 111.92]
barks = {'ayra': [34.82, 35.4, 36.42, 37.0], 'pandora': [59.9, 60.5, 61.3, 61.9], 'tifa': [83.8, 84.4, 85.2, 85.8]}
def wt(word, after=0.0):
    return next(x['a'] for x in words if x['w'].lower().startswith(word) and x['a'] >= after)
cues = {'orelhinha': wt('orelhinha'), 'bandana_azul': wt('bandana', 24), 'rabinho': wt('rabinho'), 'laco': wt('laço'),
        'narizinho': wt('narizinho'), 'bandana_verde': wt('bandana', 72), 'menina': wt('menina'), 'tapou': wt('tapou'),
        'voce': wt('você', 100), 'tapa': wt('tapa'), 'cade_words': [x['a'] for x in words if x['w'].lower() == 'cadê'],
        'vem': wt('vem')}
# vocal-band envelope
SR = 16000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f'{ROOT}/music/masters/cade_achou_final.wav', '-ac', '1', '-ar', str(SR),
                      '-af', 'highpass=f=300,lowpass=f=3400', '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32)
hop = SR // FPS; n = len(x) // hop
env = np.sqrt(np.convolve((x[:n * hop] ** 2).reshape(n, hop).mean(1), np.ones(2) / 2, 'same'))
ref = np.percentile(env, 95)
t = np.arange(n) / FPS
gate = np.zeros(n)
for w in words:
    gate[(t >= w['a'] - 0.06) & (t <= w['b'] + 0.08)] = 1.0
gate = np.convolve(gate, np.ones(3) / 3, 'same')
mouth = np.clip(gate * np.clip(env / ref, 0, 1) ** 1.2 * 1.25, 0, 1)
# visemes: syllable nuclei spread across each word; class per frame: A (open wide), E (wide/narrow), O (round), M (closed)
VOW = re.compile(r'[aáâãà]|[eéê]|[ií]|[oóôõ]|[uú]', re.I)
vis = ['M'] * n
def vclass(ch):
    ch = ch.lower()
    return 'A' if ch in 'aáâãà' else 'E' if ch in 'eéêií' else 'O'
for w in words:
    txt = w['w'].lower(); vs = [m for m in VOW.finditer(txt)]
    if not vs: continue
    # collapse diphthongs (ou, ei, ai...) into the first vowel
    nuc = [vs[0]] + [m for p, m in zip(vs, vs[1:]) if m.start() != p.end()]
    dur = w['b'] - w['a']
    for k, m in enumerate(nuc):
        s0 = w['a'] + dur * k / len(nuc); s1 = w['a'] + dur * (k + 1) / len(nuc)
        pre = txt[max(0, m.start() - 1):m.start()]
        for f in range(int(s0 * FPS), min(n, int(np.ceil(s1 * FPS)))):
            u = (f / FPS - s0) / max(1e-3, s1 - s0)
            vis[f] = 'M' if (pre and pre in 'mbp' and u < 0.22) else vclass(m.group())
out = {'bpm': B['bpm'], 'beats_s': B['beats_s'], 'downbeat_beat_index': B['downbeat_beat_index'], 'bar_s': BAR,
       'duration_s': round(len(x) / SR, 3), 'sections': sections, 'achou': achou, 'barks': barks, 'cues': cues,
       'words': words, 'fps': FPS, 'mouth': [round(float(v), 3) for v in mouth], 'viseme': ''.join(vis)}
json.dump(out, open(f'{ROOT}/music/compositions/cade_achou_timeline.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('frames', n, 'cues', {k: v for k, v in cues.items() if k != 'cade_words'}, 'mouth>0.2', float((mouth > 0.2).mean()))
