#!/usr/bin/env python3
"""Transcribe the final master with OpenAI whisper-1 (word + segment timestamps). Key read from env, never printed.
Usage: whisper_words.py AUDIO OUT.json [--prompt-lyrics]"""
import json, os, sys, requests
audio, out = sys.argv[1], sys.argv[2]
data = {'model': 'whisper-1', 'language': 'pt', 'response_format': 'verbose_json', 'temperature': '0'}
files = [('file', (os.path.basename(audio), open(audio, 'rb'), 'audio/mpeg')),
         ('timestamp_granularities[]', (None, 'word')), ('timestamp_granularities[]', (None, 'segment'))]
if '--prompt-lyrics' in sys.argv:
    data['prompt'] = 'Clara e as Patinhas. Ayra, Pandora e Tifa. Patinha pra frente, patinha pra trás, dá uma voltinha. Au, au, au. Bate palma, bate o pé.'
r = requests.post('https://api.openai.com/v1/audio/transcriptions', headers={'Authorization': f"Bearer {os.environ['OPENAI_API_KEY']}"},
                  data=data, files=files, timeout=600)
r.raise_for_status()
j = r.json(); json.dump(j, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('duration', j.get('duration'), 'words', len(j.get('words', [])), 'segments', len(j.get('segments', [])))
