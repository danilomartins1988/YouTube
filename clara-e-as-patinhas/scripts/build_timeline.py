#!/usr/bin/env python3
"""Build music/compositions/timeline_final.json from the REAL sung master.
- sections: cumulative chunk durations of eleven_music_plan.json (the generation honours them; vocal entrances
  confirm them within ~0.3 s); the ring-out is split off the last chunk; the end is clipped to the audio length.
- beats: per-section local beat grid (tempo search 110-120 BPM + phase) on a spectral-flux onset envelope;
  bars start at the first beat at/after the section start (-half a beat).
- lyrics: Whisper (whisper-1, word timestamps) aligned to the written lyrics with difflib; missing words interpolated.
- mouth: per-frame (24 fps) opening = vocal-band (300-3400 Hz) envelope, gated by Whisper word intervals.
- cues: chorus words (frente/trás/voltinha/palma/pé), names, counting, "au".
Output keeps the schema episode.py reads (secoes/linhas/notas with inicio_beat in units of the nominal beat)."""
import json, os, re, subprocess, difflib, unicodedata
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = f'{ROOT}/music/masters/danca_das_patinhas_final.wav'
PLAN = json.load(open(f'{ROOT}/music/compositions/eleven_music_plan.json', encoding='utf-8'))
GUIDE = json.load(open(f'{ROOT}/music/compositions/estrutura.json', encoding='utf-8'))
W1 = json.load(open(f'{ROOT}/music/analysis/whisper_prompt.json', encoding='utf-8'))
W0 = json.load(open(f'{ROOT}/music/analysis/whisper_noprompt.json', encoding='utf-8'))
FPS = 24; BPM_NOM = 115.0; BEAT = 60 / BPM_NOM
SR = 22050; HOP = 256

raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', AUDIO, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32); DUR = len(x) / SR
N = 2048; win = np.hanning(N)
fr = np.lib.stride_tricks.sliding_window_view(np.pad(x, (N // 2, N // 2)), N)[::HOP] * win
SP = np.abs(np.fft.rfft(fr, axis=1)); f = np.fft.rfftfreq(N, 1 / SR); efps = SR / HOP
S = np.log1p(100 * SP)
flux = np.maximum(0, np.diff(S, axis=0, prepend=S[:1])).sum(1)
flux = np.maximum(flux - np.convolve(flux, np.ones(16) / 16, 'same'), 0)
env = (flux - flux.mean()) / flux.std(); te = np.arange(len(env)) / efps

# ---------------- sections
names = [s['nome'] for s in GUIDE['secoes']]
chunks = PLAN['composition_plan']['chunks']
bounds = [0.0]
for c in chunks:
    bounds.append(bounds[-1] + c['duration_ms'] / 1000)
sections = []
for i, c in enumerate(chunks):
    sections.append([names[i], bounds[i], bounds[i + 1]])
last = sections[-1]  # split ring-out (1 bar) off the final sting chunk, as in the guide structure
ring0 = last[1] + 2 * 4 * BEAT
sections[-1] = [last[0], last[1], ring0]
sections.append(['ressonancia', ring0, DUR])

# ---------------- beats (per section)
beats = []; downbeats = []; sec_tempo = {}
for nm, a, b in sections:
    m = (te >= a - 0.05) & (te < b)
    if b - a < 2.5:
        best = (0, BPM_NOM, beats[-1] + 60 / BPM_NOM if beats else a)
    else:
        best = None
        for bpm in np.arange(110, 120.01, 0.1):
            P = 60 / bpm
            for ph in np.arange(0, P, 0.01):
                bt = np.arange(a + ph, b, P)
                sc = np.interp(bt, te, env).mean()
                if best is None or sc > best[0]:
                    best = (sc, bpm, a + ph)
    _, bpm, b0 = best
    P = 60 / bpm
    if b0 - a > P / 2:  # make first beat the one nearest the section start
        b0 -= P
    bt = list(np.arange(b0, b - 0.25 * P, P))
    sec_tempo[nm] = round(float(bpm), 2)
    beats += [round(float(v), 4) for v in bt]
    downbeats += [round(float(v), 4) for v in bt[::4]]
beats = sorted(set(beats)); all_bpm = 60 / np.median(np.diff(beats))

# ---------------- lyrics alignment
def norm(w):
    w = unicodedata.normalize('NFD', w.lower()); w = ''.join(c for c in w if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', w).replace('aira', 'ayra').replace('clare', 'clara')

LY = {  # sung version, section -> lines (from music/lyrics, plus the extra "au" line heard in break 2)
    'intro': ["Clara chamou as amiguinhas,", "Vieram correndo três cachorrinhas!", "Ayra, Pandora e Tifa também,", "Vamos dançar, vem, vem, vem!"],
    'refrao_1': ["Patinha pra frente,", "Patinha pra trás,", "Dá uma voltinha,", "E dança muito mais!", "Au, au, au, vamos brincar,",
                 "Au, au, au, vamos cantar!", "Bate palma, bate o pé,", "Dança junto como quiser!"],
    'verso_ayra': ["Ayra corre pelo jardim,", "Mexe o rabinho e olha pra mim!", "Pula pra cá, pula pra lá,", "Que cachorrinha gosta de brincar!"],
    'refrao_2_curto': ["Patinha pra frente,", "Patinha pra trás,", "Dá uma voltinha,", "E dança muito mais!", "Au, au, au, vamos brincar,", "Au, au, au, vamos cantar!"],
    'pausa_danca_2': ["Au, au, au, vamos brincar!"],
    'verso_pandora': ["Pandora branquinha, fofinha demais,", "Dá uma voltinha e pede mais!", "Mexe as patinhas, começa a girar,", "Com a Clara ela vai dançar!"],
    'verso_tifa': ["Tifa pequena, cheia de energia,", "Faz todo mundo sorrir de alegria!", "Dá um pulinho: um, dois, três,", "Vamos dançar mais uma vez!"],
    'ponte': ["Uma patinha, duas patinhas,", "Três cachorrinhas fazendo festinha!", "Uma voltinha, um salto no ar,", "Todo mundo pronto pra dançar!"],
    'refrao_final': ["Patinha pra frente,", "Patinha pra trás,", "Dá uma voltinha,", "E dança muito mais!", "Au, au, au, vamos brincar,",
                     "Au, au, au, vamos cantar!", "Com os amigos é tão bom viver,", "Dançando juntos, eu e você!"],
    'final': ["Clara e as Patinhas,", "Que alegria!", "Juntos brincando,", "Todo dia!"],
}
lyr = []  # (section, line_idx, word_idx, display_word, token)
for nm, a, b in sections:
    for li, ln in enumerate(LY.get(nm, [])):
        for wi, w in enumerate(re.findall(r"[\wÀ-ÿ]+", ln)):
            lyr.append((nm, li, wi, w, norm(w)))
times = [None] * len(lyr)
for WJ in (W0, W1):  # unprompted run first (its timings were closer to the bar grid), prompted run fills gaps
    ww = [w for w in WJ['words'] if 0 <= w['start'] <= DUR]
    wtok = [norm(w['word']) for w in ww]
    sm = difflib.SequenceMatcher(a=[t[4] for t in lyr], b=wtok, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            if times[blk.a + k] is None:
                w = ww[blk.b + k]; times[blk.a + k] = (w['start'], max(w['end'], w['start'] + 0.12))
matched = sum(t is not None for t in times)
# interpolate unmatched words inside their section
sec_rng = {nm: (a, b) for nm, a, b in sections}
for i in range(len(lyr)):
    if times[i] is None:
        prev = next((times[j] for j in range(i - 1, -1, -1) if times[j] and lyr[j][0] == lyr[i][0]), None)
        nxt = next((times[j] for j in range(i + 1, len(lyr)) if times[j] and lyr[j][0] == lyr[i][0]), None)
        a, b = sec_rng[lyr[i][0]]
        s0 = prev[1] if prev else a + 0.2; s1 = nxt[0] if nxt else b - 0.2
        times[i] = (s0, min(s1, s0 + 0.35))
# 'Au, au, au' is sung as three short notes: spread them on eighths from the first one
i = 0
while i < len(lyr):
    if lyr[i][4] == 'au' and i + 2 < len(lyr) and lyr[i + 1][4] == 'au' and lyr[i + 2][4] == 'au':
        s0 = times[i][0]
        for k in range(3):
            times[i + k] = (s0 + k * BEAT / 2, s0 + k * BEAT / 2 + BEAT * 0.45)
        i += 3
    else:
        i += 1
# whisper often gives zero-length words for sung syllables: give each word at least 0.18 s, not past the next word
for i in range(len(times) - 1):
    s, e = times[i]; ns = times[i + 1][0]
    times[i] = (s, min(max(e, s + 0.18), max(ns, s + 0.1)))

# ---------------- mouth envelope (vocal band, gated by words)
band = SP[:, (f >= 300) & (f <= 3400)].sum(1)
band = np.convolve(band, np.ones(3) / 3, 'same')
tf = np.arange(int(np.ceil((DUR + 1) * FPS))) / FPS
bf = np.interp(tf, te, band)
gate = np.zeros_like(tf)
for s, e in times:
    gate = np.maximum(gate, ((tf >= s - 0.04) & (tf <= e + 0.04)).astype(float))
# local normalisation (2 s window percentile) so loud instrumental parts don't saturate
mouth = np.zeros_like(tf)
for i in range(len(tf)):
    lo = max(0, i - FPS); hi = min(len(tf), i + FPS)
    ref = np.percentile(bf[lo:hi], 90) + 1e-9
    mouth[i] = gate[i] * np.clip((bf[i] / ref) ** 1.5, 0, 1)
# syllabic modulation: dip between consecutive words
mouth = np.round(np.clip(mouth, 0, 1), 3)

# ---------------- assemble
secoes = []
for nm, a, b in sections:
    lines = []
    for li, ln in enumerate(LY.get(nm, [])):
        idx = [i for i, t in enumerate(lyr) if t[0] == nm and t[1] == li]
        words = [{'w': lyr[i][3], 'start': round(times[i][0], 3), 'end': round(times[i][1], 3)} for i in idx]
        notas = [{'silaba': lyr[i][3].upper() if lyr[i][4] == 'au' else lyr[i][3], 'inicio_beat': round(times[i][0] / BEAT, 4),
                  'dur': round((times[i][1] - times[i][0]) / BEAT, 4)} for i in idx]
        lines.append({'texto': ln, 'inicio_s': words[0]['start'], 'fim_s': words[-1]['end'], 'palavras': words, 'notas': notas})
    secoes.append({'nome': nm, 'inicio_s': round(a, 3), 'fim_s': round(b, 3), 'bpm_local': sec_tempo[nm], 'linhas': lines})

def wt(sec, token, nth=0):
    hits = [times[i][0] for i, t in enumerate(lyr) if t[0] == sec and t[4] == token]
    return round(hits[nth], 3) if len(hits) > nth else None

cues = {}
for sec in ('refrao_1', 'refrao_2_curto', 'refrao_final'):
    cues[sec] = {k: wt(sec, k) for k in ('frente', 'tras', 'voltinha', 'danca', 'palma', 'pe')}
    cues[sec]['au'] = [round(times[i][0], 3) for i, t in enumerate(lyr) if t[0] == sec and t[4] == 'au']
cues['nomes_intro'] = {'ayra': wt('intro', 'ayra'), 'pandora': wt('intro', 'pandora'), 'tifa': wt('intro', 'tifa')}
cues['tifa_contagem'] = {'um': wt('verso_tifa', 'um', 1), 'dois': wt('verso_tifa', 'dois'), 'tres': wt('verso_tifa', 'tres')}
claps = []
for nm, a, b in sections:
    if nm.startswith(('refrao', 'pausa', 'final', 'intro_instrumental')):
        for db in downbeats:
            if a - 0.1 <= db < b:
                i = beats.index(db)
                claps += [beats[i + k] for k in (1, 3) if i + k < len(beats) and beats[i + k] < b]
out = {
    'fonte': 'music/masters/danca_das_patinhas_final.wav (Eleven Music v1 + intro inpaint, loudness -14 LUFS)',
    'bpm': round(float(all_bpm), 3), 'bpm_nominal_plano': BPM_NOM, 'bpm_por_secao': sec_tempo,
    'duracao_musical_s': round(DUR, 3), 'duracao_com_cauda_s': round(DUR, 3),
    'beats_s': beats, 'downbeats_s': downbeats, 'palmas_s': [round(c, 4) for c in claps],
    'cues': cues, 'mouth_fps': FPS, 'mouth': [float(v) for v in mouth],
    'whisper': {'modelo': 'whisper-1', 'palavras_letra': len(lyr), 'palavras_casadas': matched},
    'notas_formato': 'inicio_beat = start_s / (60/115) (beat nominal, só para compatibilidade); use palavras[].start/end em segundos.',
    'secoes': secoes,
}
json.dump(out, open(f'{ROOT}/music/compositions/timeline_final.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('DUR', round(DUR, 2), 'BPM', round(float(all_bpm), 2), 'per-section', sec_tempo)
print('words matched', matched, '/', len(lyr))
print('cues', json.dumps(cues, ensure_ascii=False))
print('claps', len(claps), 'beats', len(beats))
