"""Shared timing map for "Pata Pata Patatá" (all languages): sections from the composition plan (identical chunk
durations in PT/EN/ES), sung-word cues per language from Whisper, choreography cues (Aditivo 01 §25), 30 fps frames."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
plan = json.load(open(f'{ROOT}/music/compositions/pilot/full_pt.json'))['composition_plan']['chunks']
names = ['intro', 'chorus_1', 'ayra', 'chorus_2', 'pandora', 'chorus_3', 'toby', 'chorus_4', 'milo', 'clara', 'chorus_final_x2', 'outro']
t = 0; sections = []
for n, c in zip(names, plan):
    d = c.get('duration_ms') or c['range']['end_ms'] - c['range']['start_ms']
    sections.append({'name': n, 'start_ms': t, 'end_ms': t + d, 'start_frame_30fps': round(t * 30 / 1000)}); t += d
CUE = {'pt': {'au': 'ayra_bark', 'pula': 'pandora_hop', 'gira': 'toby_spin', 'miau': 'milo_meow', 'palma': 'clara_clap', 'rabinho': 'tails_wag'},
       'en': {'woof': 'ayra_bark', 'jump': 'pandora_hop', 'spin': 'toby_spin', 'spins': 'toby_spin', 'meow': 'milo_meow', 'clap': 'clara_clap', 'tail': 'tails_wag'},
       'es': {'guau': 'ayra_bark', 'salta': 'pandora_hop', 'gira': 'toby_spin', 'miau': 'milo_meow', 'palmas': 'clara_clap', 'colita': 'tails_wag'}}
W = {'pt': 'whisper_pt_v3.json', 'en': 'whisper_en_v1.json', 'es': 'whisper_es_v1.json'}
lang = {}
for lg, f in W.items():
    j = json.load(open(f'{ROOT}/music/analysis/pata/{f}'))
    words = [{'w': w['word'], 's': round(w['start'], 2), 'e': round(w['end'], 2)} for w in j.get('words', [])]
    cues = [{'cue': CUE[lg][re.sub(r'\W', '', w['w'].lower())], 't': w['s']} for w in words if re.sub(r'\W', '', w['w'].lower()) in CUE[lg]]
    lang[lg] = {'words_source': f, 'n_words': len(words), 'choreo_cues': cues}
out = {'song': 'Pata Pata Patatá', 'duration_ms': t, 'fps': 30, 'bpm': 94.85, 'bar_ms': 2526,
       'note': 'Section boundaries are identical in all languages (same chunk durations; EN/ES vocals verified within ~12 ms of the PT beat grid). '
               'Word cues come from Whisper and can be off by ~0.1-0.3 s; ES words for the Ayra/Toby/Clara verses are from v1 (re-sung in v4 at the same positions).',
       'sections': sections, 'languages': lang}
json.dump(out, open(f'{ROOT}/music/compositions/pilot/timing_map.json', 'w'), ensure_ascii=False, indent=1)
print(t, [(s['name'], s['start_ms']) for s in sections]); print({k: len(v['choreo_cues']) for k, v in lang.items()})
