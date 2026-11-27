#!/usr/bin/env python3
"""Ep. 002 "Cadê? Achou!" - build the Eleven Music composition plan (music_v2_5 chunk format).
100 BPM, 4/4, D major (same key/voice style as ep. 001 for channel consistency), bar = 2.4 s.
NO character names anywhere in the request (owner rule from ep. 002 on).
Writes music/compositions/cade_achou_plan.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BPM = 100; BAR_MS = 4 * 60000 // BPM  # 2400
VOICE = ("the same warm young adult female lead singer throughout the whole song, identical voice, timbre and vocal register "
         "in every section, sweet and clear, natural Brazilian Portuguese")
GLOBAL = ["gentle Brazilian children's song for babies and toddlers, peekaboo hide-and-seek game song",
          VOICE, "small soft group of backing voices answering 'Achou!' and 'au, au!'",
          "ukulele fingerpicking and soft strumming", "xylophone and marimba melodies", "soft glockenspiel bells",
          "light percussion: shaker, soft hand claps, soft kick", "acoustic upright bass",
          f"{BPM} BPM", "D major", "4/4", "bright, warm, tender, playful, preschool-friendly",
          "clean modern production, studio quality, clear intelligible lyrics, lead vocal upfront in the mix"]
NEG = ["electric guitar distortion", "heavy drums", "EDM drops", "autotune", "aggressive vocals", "rap", "sad", "dark",
       "minor key", "scary", "explicit content", "male lead vocal", "European Portuguese accent", "Spanish accent",
       "different singer", "voice change between sections", "child lead voice", "high-pitched chipmunk vocal",
       "pitched-up vocal", "falsetto", "reverb wash", "muddy mix"]
INSTR = ["vocals", "lyrics", "singing"]
SUSP = "{short suspense pause: music drops to a soft shaker and a tiny rising glockenspiel}"
S = [  # (tag, bars, text-or-direction, local styles, instrumental?)
 ('Intro', 2, "{gentle xylophone and ukulele intro}\n{two small soft cute dog barks}",
  ["instrumental intro", "xylophone plays the 'cadê, cadê' melody", "two small soft dog barks at the end"], True),
 ('Chorus', 8, "Cadê, cadê, cadê você?\nCadê, cadê, quem vai aparecer?\nTem alguém escondidinho no jardim,\nVem procurar bem juntinho de mim!",
  ["simple catchy sing-along chorus", "call and answer feel", "tender and curious"], False),
 ('Verse 1', 6, f"Atrás da flor, quem será?\nUma orelhinha, olha lá!\nBandana azul...\n{SUSP}\nACHOU!\n(Au, au!)",
  ["curious whispery verse building to a joyful reveal", "backing voices shout a happy 'Achou!' with the lead", "backing voices answer 'au, au!'"], False),
 ('Short Chorus', 4, "Cadê, cadê, cadê você?\nCadê, cadê, quem vai aparecer?",
  ["short sing-along chorus", "soft claps"], False),
 ('Verse 2', 6, f"Dentro do balde, quem será?\nUm rabinho branco, olha lá!\nLaço cor-de-rosa...\n{SUSP}\nACHOU!\n(Au, au!)",
  ["curious whispery verse building to a joyful reveal", "sparkly bells", "backing voices shout a happy 'Achou!' with the lead", "backing voices answer 'au, au!'"], False),
 ('Short Chorus', 4, "Cadê, cadê, cadê você?\nCadê, cadê, quem vai aparecer?",
  ["short sing-along chorus", "soft claps"], False),
 ('Verse 3', 6, f"Embaixo do chapéu, quem será?\nUm narizinho, olha lá!\nBandana verde...\n{SUSP}\nACHOU!\n(Au, au!)",
  ["curious whispery verse building to a joyful reveal", "playful staccato marimba", "backing voices shout a happy 'Achou!' with the lead", "backing voices answer 'au, au!'"], False),
 ('Bridge', 6, f"E a menina? Cadê? Cadê?\nTapou o rostinho, quem vai ver?\n{SUSP}\nACHOU!",
  ["tender bridge", "softer arrangement", "anticipation", "big happy 'Achou!' with backing voices"], False),
 ('Final Verse', 6, f"E você? Cadê você?\nTapa o rostinho, deixa eu ver...\n{SUSP}\nACHOU!",
  ["intimate, singing directly to the little listener", "softest suspense", "biggest joyful 'Achou!' with backing voices"], False),
 ('Outro', 4, "Achou, achou, que alegria!\nBrincar de esconder todo dia!\n{soft final D major chord, two small soft dog barks}",
  ["happy ending tag", "slower final line", "warm", "final chord rings out"], False),
]
chunks = []
for i, (tag, bars, txt, loc, instr) in enumerate(S):
    pos = (GLOBAL + loc) if i == 0 else loc + [f"{BPM} BPM", "D major"] + ([] if instr else [VOICE])
    chunks.append({'text': f"[{tag}]\n{txt}", 'duration_ms': bars * BAR_MS, 'positive_styles': pos,
                   'negative_styles': NEG + (INSTR if instr else []), 'context_adherence': 'high'})
total = sum(c['duration_ms'] for c in chunks)
assert len(chunks) <= 30 and all(3000 <= c['duration_ms'] <= 120000 for c in chunks)
blob = json.dumps(chunks, ensure_ascii=False).lower()
for n in ('clara', 'ayra', 'aira', 'pandora', 'tifa', 'patinhas'):
    assert n not in blob, n
plan = {'_meta': {'projeto': 'ep. 002 - Cadê? Achou!', 'modelo': 'music_v2_5', 'endpoint': 'POST https://api.elevenlabs.io/v1/music',
                  'duracao_total_ms': total, 'bpm': BPM, 'compasso_ms': BAR_MS, 'tonalidade': 'D major',
                  'secoes': [{'tag': t, 'compassos': b, 'inicio_s': round(sum(x[1] for x in S[:k]) * BAR_MS / 1000, 2)} for k, (t, b, *_ ) in enumerate(S)],
                  'nota': 'Sem nomes de personagens (regra do proprietário). Campos com _ não são enviados.'},
        'model_id': 'music_v2_5', 'composition_plan': {'chunks': chunks}}
json.dump(plan, open(f'{ROOT}/music/compositions/cade_achou_plan.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(chunks), 'chunks', total, 'ms')
