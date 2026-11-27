#!/usr/bin/env python3
"""Generate the sung song with the ElevenLabs Eleven Music API (POST /v1/music) from a composition plan.

SAFETY: costs credits. Refuses to run without --confirm.
The API key is NEVER read, printed or stored by this script: in this cloud environment the network proxy
injects it for api.elevenlabs.io; a dummy value is sent in `xi-api-key`. Outside this environment, set
ELEVENLABS_API_KEY (the script will use it but never print it).

Usage:
  python3 music/scripts/eleven_generate.py --plan music/compositions/eleven_music_plan.json --confirm [--tag v1]

Output: music/masters/<name>_<tag>.wav (if PCM was accepted) or .mp3, plus a .response.json with
non-sensitive response headers (song id, etc.). Appends a cost line to reports/CUSTOS.md.
Docs: https://elevenlabs.io/docs/api-reference/music/compose
"""
import argparse, datetime, json, os, sys, wave
import requests

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
API = 'https://api.elevenlabs.io/v1/music'
# best first; fall back only if the server rejects the format (4xx => nothing generated)
FORMATS = ['pcm_48000', 'pcm_44100', 'mp3_48000_320', 'mp3_48000_192']
PRICE_PER_MIN_USD = 0.15   # https://elevenlabs.io/pricing/api ("$0.15 per minute")
CREDITS_PER_MIN = 900      # https://elevenlabs.io/pricing ("uses about 900 per minute")
SAFE_HEADERS = ('song-id', 'x-song-id', 'request-id', 'x-request-id', 'content-type', 'content-length',
                'character-cost', 'x-character-count', 'history-item-id', 'x-credits-used', 'date')


def strip_meta(o):
    if isinstance(o, dict):
        return {k: strip_meta(v) for k, v in o.items() if not k.startswith('_')}
    if isinstance(o, list):
        return [strip_meta(v) for v in o]
    return o


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', default=f'{ROOT}/music/compositions/eleven_music_plan.json')
    ap.add_argument('--out-dir', default=f'{ROOT}/music/masters')
    ap.add_argument('--name', default='danca_das_patinhas')
    ap.add_argument('--tag', default='v1')
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--confirm', action='store_true', help='required: acknowledges this spends ElevenLabs credits')
    a = ap.parse_args()

    raw = json.load(open(a.plan, encoding='utf-8'))
    body = strip_meta(raw)
    total_ms = sum(c['duration_ms'] for c in body['composition_plan']['chunks'])
    est_min = total_ms / 60000
    print(f'Plan: {len(body["composition_plan"]["chunks"])} chunks, {total_ms/1000:.1f} s, model {body.get("model_id")}')
    print(f'Estimated cost: ~{est_min*CREDITS_PER_MIN:.0f} credits (~US$ {est_min*PRICE_PER_MIN_USD:.2f} at API list price)')
    if not a.confirm:
        print('Refusing to call the paid API without --confirm.'); sys.exit(2)
    if a.seed is not None:
        body['seed'] = a.seed
    for k in ('prompt', 'music_length_ms', 'force_instrumental'):
        assert k not in body, f'{k} is not allowed together with composition_plan'

    os.makedirs(a.out_dir, exist_ok=True)
    key = os.environ.get('ELEVENLABS_API_KEY') or 'proxy-injected'
    headers = {'xi-api-key': key, 'Content-Type': 'application/json'}
    resp, fmt = None, None
    for fmt in FORMATS:
        r = requests.post(API, params={'output_format': fmt}, headers=headers, json=body, timeout=900)
        if r.status_code == 200:
            resp = r; break
        msg = r.text[:400]
        print(f'format {fmt}: HTTP {r.status_code}: {msg}')
        if r.status_code in (400, 403, 422) and ('format' in msg.lower() or 'tier' in msg.lower() or 'subscription' in msg.lower()):
            continue  # rejected before generation -> try next format
        sys.exit(1)
    if resp is None:
        sys.exit(1)

    base = f'{a.out_dir}/{a.name}_{a.tag}'
    data = resp.content
    if fmt.startswith('pcm'):
        sr = int(fmt.split('_')[1])
        mono_s = len(data) / (sr * 2)
        ch = 2 if abs(mono_s / 2 - total_ms / 1000) < abs(mono_s - total_ms / 1000) else 1
        path = base + '.wav'
        with wave.open(path, 'wb') as w:
            w.setnchannels(ch); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data)
    else:
        path = base + '.mp3'
        open(path, 'wb').write(data)
    meta = {'format': fmt, 'file': os.path.relpath(path, ROOT), 'bytes': len(data),
            'generated_at': datetime.datetime.utcnow().isoformat() + 'Z',
            'headers': {k: v for k, v in resp.headers.items() if k.lower() in SAFE_HEADERS},
            'plan': os.path.relpath(a.plan, ROOT), 'planned_ms': total_ms}
    json.dump(meta, open(base + '.response.json', 'w'), indent=1)
    print('saved', path, len(data), 'bytes; format', fmt)
    print('response headers (safe subset):', meta['headers'])
    line = (f"| {datetime.date.today()} | ElevenLabs Eleven Music (music_v2_5) | 1 geração {a.tag}, {total_ms/1000:.0f} s | "
            f"~{est_min*CREDITS_PER_MIN:.0f} créditos (estimado) | ~US$ {est_min*PRICE_PER_MIN_USD:.2f} (preço de lista API; "
            f"débito real no plano do proprietário) |\n")
    with open(f'{ROOT}/reports/CUSTOS.md', 'a', encoding='utf-8') as f:
        f.write(line)


if __name__ == '__main__':
    main()
