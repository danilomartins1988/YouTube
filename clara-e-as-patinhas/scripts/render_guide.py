#!/usr/bin/env python3
"""Render guide instrumental: MIDI -> FluidSynth (FluidR3_GM) -> mix synthetic barks -> MP3.
Barks are synthesized here (pitched glide + noise burst), no samples used."""
import json, os, subprocess, wave
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f'{ROOT}/output'; os.makedirs(OUT, exist_ok=True)
SF = '/usr/share/sounds/sf2/FluidR3_GM.sf2'
SR = 44100
st = json.load(open(f'{ROOT}/music/compositions/estrutura.json'))

def bark(seed):
    rng = np.random.default_rng(seed)
    dur = 0.16; n = int(SR * dur); t = np.arange(n) / SR
    f = np.linspace(780, 430, n) * (1 + 0.02 * rng.standard_normal())
    ph = 2 * np.pi * np.cumsum(f) / SR
    tone = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.25 * np.sin(3 * ph)
    noise = rng.standard_normal(n) * 0.25
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.05)
    s = (tone + noise) * env
    return s / np.abs(s).max()

def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, w.getnchannels())
    return a.astype(np.float32) / 32768

def write_wav(p, a):
    a = np.clip(a, -1, 1)
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((a * 32767).astype(np.int16).tobytes())

for name in ['guia_instrumental', 'guia_sem_melodia']:
    mid = f'{ROOT}/music/instrumentals/{name}.mid'
    raw = f'{OUT}/{name}_raw.wav'
    subprocess.run(['fluidsynth', '-ni', '-g', '0.6', '-r', str(SR), '-F', raw, SF, mid], check=True, capture_output=True)
    a = read_wav(raw)
    for i, ts in enumerate(st['latidos_s']):
        b = bark(i) * 0.35
        k = int(ts * SR)
        if k + len(b) < len(a):
            a[k:k + len(b), 0] += b * 0.9; a[k:k + len(b), 1] += b * 1.0
    a = a[: int((st['duracao_com_cauda_s'] + 1.0) * SR)]
    peak = np.abs(a).max(); a = a * (0.89 / peak)
    fade = int(1.0 * SR); a[-fade:] *= np.linspace(1, 0, fade)[:, None]
    wav = f'{OUT}/{name}.wav'; write_wav(wav, a); os.remove(raw)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                    '-ar', '44100', '-b:a', '192k', f'{OUT}/{name}.mp3'], check=True)
    print(name, len(a) / SR, 's')
