#!/usr/bin/env python3
"""Build music/compositions/eleven_music_plan.json (Eleven Music composition plan, music_v2_5 chunk format)
from estrutura.json. Section durations match the guide instrumental exactly (115 BPM)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
st = json.load(open(f'{ROOT}/music/compositions/estrutura.json', encoding='utf-8'))
GLOBAL = ["cheerful Brazilian children's song", "warm young female lead vocal, sweet and clear, natural Brazilian Portuguese pronunciation",
          "light playful backing vocals", "ukulele and warm acoustic guitar strumming", "xylophone and marimba melodies",
          "hand claps on beats 2 and 4", "light percussion: shaker, tambourine, soft kick", "acoustic upright bass", "soft glockenspiel bells",
          "115 BPM", "D major", "4/4", "bright, warm, gentle, preschool-friendly", "clean modern production, studio quality"]
NEG = ["electric guitar distortion", "heavy drums", "EDM drops", "autotune", "aggressive vocals", "rap", "sad", "dark", "minor key",
       "explicit content", "male lead vocal", "European Portuguese accent", "Spanish accent"]
LOCAL = {
 'assinatura': (["short brand jingle", "xylophone and glockenspiel motif", "two small cute dog barks at the end"], ["vocals", "lyrics"], "{cheerful xylophone jingle}\n{two small cute dog barks}"),
 'intro_instrumental': (["instrumental", "xylophone plays the chorus hook", "ukulele groove starts"], ["vocals", "lyrics"], "{instrumental, xylophone plays the chorus melody}"),
 'intro': (["storytelling verse", "friendly and inviting", "light groove"], [], None),
 'refrao_1': (["big catchy sing-along chorus", "claps on 2 and 4", "backing vocals echo 'au, au, au'"], [], None),
 'pausa_danca_1': (["instrumental dance break", "claps", "small rhythmic dog barks in the groove"], ["vocals", "lyrics"], "{instrumental dance break with claps and small rhythmic dog barks}"),
 'verso_ayra': (["playful verse", "bouncy marimba"], [], None),
 'refrao_2_curto': (["catchy sing-along chorus", "claps on 2 and 4", "backing vocals"], [], None),
 'pausa_danca_2': (["instrumental dance break", "claps", "small rhythmic dog barks in the groove"], ["vocals", "lyrics"], "{instrumental dance break with claps and small rhythmic dog barks}"),
 'verso_pandora': (["soft, tender and fluffy feel", "gentle marimba", "sparkly bells"], [], None),
 'verso_tifa': (["energetic, funny and bouncy", "playful staccato", "counting 'um, dois, três' clearly"], [], None),
 'ponte': (["building bridge", "rising energy", "counting song feel", "anticipation before final chorus"], [], None),
 'refrao_final': (["final big chorus", "fullest arrangement", "joyful backing vocals", "claps"], [], None),
 'final': (["happy ending tag", "slower final line", "warm"], [], None),
 'assinatura_final': (["brand jingle repeats", "xylophone and glockenspiel motif", "final D major chord ringing out", "two small cute dog barks"], ["vocals", "lyrics"], "{cheerful xylophone jingle, final chord}\n{two small cute dog barks}"),
}
TAGS = {'intro': 'Intro', 'refrao_1': 'Chorus', 'verso_ayra': 'Verse 1 - Ayra', 'refrao_2_curto': 'Chorus', 'verso_pandora': 'Verse 2 - Pandora',
        'verso_tifa': 'Verse 3 - Tifa', 'ponte': 'Bridge', 'refrao_final': 'Final Chorus', 'final': 'Outro',
        'assinatura': 'Brand Jingle', 'intro_instrumental': 'Instrumental Hook', 'pausa_danca_1': 'Dance Break', 'pausa_danca_2': 'Dance Break',
        'assinatura_final': 'Brand Jingle'}
chunks = []
secs = st['secoes']
for i, s in enumerate(secs):
    if s['nome'] == 'ressonancia':
        chunks[-1]['duration_ms'] += int(round((s['fim_s'] - s['inicio_s']) * 1000))
        continue
    pos, neg, direction = LOCAL[s['nome']]
    if direction:
        text = f"[{TAGS[s['nome']]}]\n{direction}"
    else:
        text = f"[{TAGS[s['nome']]}]\n" + "\n".join(l['texto'] for l in s['linhas'])
    styles = (GLOBAL + pos) if i == 0 else pos + ["115 BPM", "D major", "warm young female lead vocal, Brazilian Portuguese"] if not direction else pos + ["115 BPM", "D major"]
    chunks.append({'text': text, 'duration_ms': int(round((s['fim_s'] - s['inicio_s']) * 1000)),
                   'positive_styles': styles, 'negative_styles': NEG + neg, 'context_adherence': 'high'})
total = sum(c['duration_ms'] for c in chunks)
plan = {
  '_meta': {
    'projeto': 'Clara e as Patinhas - ep. 001 - A Dança das Patinhas',
    'modelo': 'music_v2_5', 'endpoint': 'POST https://api.elevenlabs.io/v1/music',
    'formato': 'composition_plan.chunks (music_v2 / music_v2_5) - docs: https://elevenlabs.io/docs/api-reference/music/compose , https://elevenlabs.io/docs/eleven-api/guides/how-to/music/composition-plans',
    'duracao_total_ms': total, 'bpm': 115, 'tonalidade': 'D major',
    'estilo_global_prompt': "Cheerful Brazilian children's song for ages 1-5, warm young female lead vocal with natural Brazilian Portuguese pronunciation, light backing vocals, ukulele and acoustic guitar, xylophone and marimba, hand claps, light percussion, acoustic bass, soft bells, 115 BPM, D major, small rhythmic dog barks.",
    'pronuncia': 'Ayra = AI-ra, Tifa = TI-fa, Pandora = pan-DO-ra',
    'nota': 'Campos com prefixo _ não são enviados à API (o script remove).'
  },
  'model_id': 'music_v2_5',
  'composition_plan': {'chunks': chunks},
}
assert len(chunks) <= 30 and all(3000 <= c['duration_ms'] <= 120000 for c in chunks)
json.dump(plan, open(f'{ROOT}/music/compositions/eleven_music_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(chunks), 'chunks', total, 'ms')
