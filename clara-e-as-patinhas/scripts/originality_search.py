"""Originality search on public catalogues reachable without login:
 - Apple Music / iTunes Search API (itunes.apple.com/search, country BR, music only)
 - YouTube public search results page (first page, titles + channels, parsed from ytInitialData)
Writes raw JSON to intellectual-property/originality-reports/raw/<date>_search.json.
No result != legal clearance."""
import json, os, re, sys, time, urllib.parse, datetime, requests
ROOT = __file__.rsplit('/scripts/', 1)[0]
TERMS = [l.strip() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
COUNTRY = sys.argv[2] if len(sys.argv) > 2 else 'BR'
H = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'pt-BR,pt;q=0.9'}

def itunes(t):
    for attempt in range(4):
        r = requests.get('https://itunes.apple.com/search', params={'term': t, 'country': COUNTRY, 'media': 'music', 'limit': 15}, timeout=30)
        if r.status_code == 200 and r.text.strip().startswith('{'):
            return [{'track': x.get('trackName') or x.get('collectionName'), 'artist': x.get('artistName'), 'kind': x.get('kind'), 'year': (x.get('releaseDate') or '')[:4]} for x in r.json()['results']]
        time.sleep(8 * (attempt + 1))
    return 'ERROR: no valid response (rate limited?)'

def youtube(t):
    try:
        r = requests.get('https://www.youtube.com/results', params={'search_query': t, 'hl': 'pt', 'gl': 'BR'}, headers=H, timeout=30)
        m = re.search(r'var ytInitialData = (\{.*?\});</script>', r.text)
        if not m: return f'ERROR: HTTP {r.status_code}, results not parseable'
        d = json.loads(m.group(1)); out = []
        def walk(o):
            if isinstance(o, dict):
                if 'videoRenderer' in o:
                    v = o['videoRenderer']
                    out.append({'title': ''.join(x.get('text', '') for x in v.get('title', {}).get('runs', [])),
                                'channel': ''.join(x.get('text', '') for x in v.get('ownerText', {}).get('runs', [])),
                                'views': v.get('viewCountText', {}).get('simpleText', '')})
                for x in o.values(): walk(x)
            elif isinstance(o, list):
                for x in o: walk(x)
        walk(d); return out[:12]
    except Exception as e:
        return f'ERROR: {e}'

day = datetime.date.today().isoformat()
OUT = f'{ROOT}/intellectual-property/originality-reports/raw/{day}_search_{COUNTRY}{os.environ.get("TAG","")}.json'
res = {}
def save():
    json.dump({'date': day, 'note': 'raw first-page results; not legal clearance', 'results': res},
              open(OUT, 'w'), ensure_ascii=False, indent=1)
for t in TERMS:
    res[t] = {'apple_music_br': itunes(t), 'youtube_br_first_page': youtube(t)}
    print(t, '| apple:', len(res[t]['apple_music_br']) if isinstance(res[t]['apple_music_br'], list) else res[t]['apple_music_br'],
          '| yt:', len(res[t]['youtube_br_first_page']) if isinstance(res[t]['youtube_br_first_page'], list) else res[t]['youtube_br_first_page'], flush=True)
    save(); time.sleep(3)
