"""Per-section check of a full take: Whisper text per section (clips) + voice match per section.
Usage: check_full.py SLUG FILE_TAG LANG   (file music/masters/lote1/SLUG/full_FILE_TAG.wav) -> music/analysis/SLUG/check_FILE_TAG.json"""
import json, os, subprocess, sys, requests
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import voice_match as vm
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
slug, tag, lg = sys.argv[1:4]
A = f'{ROOT}/music/masters/lote1/{slug}/full_{tag}.wav'
S = json.load(open(f'{ROOT}/music/compositions/lote1/{slug}/sections.json'))
TMP = os.environ.get('VM_TMP', '/tmp')
refs = vm.load_refs(); ref_f0 = sorted(r['f0_median_hz'] for r in refs.values())[1]
voc = vm.separate(A); out = []
for sec in S['sections']:
    a, b = sec['start_ms'] / 1000, sec['end_ms'] / 1000
    clip = f'{TMP}/chk.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b), '-i', A, '-b:a', '128k', clip], check=True)
    txt = ''
    if sec['name'] not in ('intro', 'break'):
        r = requests.post('https://api.openai.com/v1/audio/transcriptions', headers={'Authorization': f"Bearer {os.environ['OPENAI_API_KEY']}"},
                          data={'model': 'whisper-1', 'language': lg, 'temperature': '0'}, files={'file': open(clip, 'rb')}, timeout=120)
        txt = r.json().get('text', '')[:200]
    f = vm.features(voc[int(a * vm.SR):int(b * vm.SR)])
    row = {'section': sec['name'], 'start': a, 'end': b, 'text': txt}
    if f and f['voiced_frames'] >= vm.MIN_VOICED:
        import numpy as np
        row.update({'f0': round(f['f0_median_hz']), 'st_vs_ref': round(float(12 * np.log2(f['f0_median_hz'] / ref_f0)), 1),
                    'mfcc': round(min(vm.mfcc_dist(f, r) for r in refs.values()), 1)})
    out.append(row); print(json.dumps(row, ensure_ascii=False), flush=True)
json.dump(out, open(f'{ROOT}/music/analysis/{slug}/check_{tag}.json', 'w'), ensure_ascii=False, indent=1)
