"""Lote 1 chorus proposals (PT). Voice lock = VOICE_PROFILE.md (house singer of 'Cadê? Achou!' / pilot).
Never names artists or existing songs. Usage: build_chorus.py SLUG [A B C]"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SONGS = json.load(open(f'{ROOT}/music/lyrics/lote1/songs.json', encoding='utf-8'))
VOICE = ("the same warm young adult female lead singer throughout the whole song, identical voice, timbre and vocal register in every "
         "section, sweet and clear, natural Brazilian Portuguese")
NEG = ["electric guitar", "synthesizer", "EDM", "heavy drums", "aggressive vocals", "rap", "autotune", "sad", "dark", "minor key", "scary",
       "male lead vocal", "European Portuguese accent", "Spanish accent", "different singer", "voice change between sections", "child lead voice",
       "high-pitched chipmunk vocal", "pitched-up vocal", "falsetto", "shrill", "reverb wash", "muddy mix", "explicit content"]
ARR = {
 'au-au-ayra': ["gentle Brazilian forro pe-de-serra in a soft xote groove", "sanfona accordion is the lead instrument and carries the hook",
                "triangle keeps a light steady pulse", "soft zabumba", "a soft hand drum answers the barks", "light acoustic bass"],
 'miau-miau-milo': ["playful light children's song", "pizzicato strings are the lead instrument and carry the hook", "soft glockenspiel accents",
                    "light finger snaps", "light acoustic bass", "tiptoeing cat-like feel"],
 'pula-pula-pandora': ["bright cheerful Brazilian marchinha rhythm, light and bouncy", "xylophone is the lead instrument and carries the hook",
                       "hand claps", "light snare brushes", "small brass section, very soft", "acoustic bass"],
 'toby-gira-girou': ["playful Brazilian baiao groove, light and bouncy", "triangle and soft zabumba", "soft muted trumpet plays little funny fills",
                     "sanfona accordion chords", "light acoustic bass", "gentle humour"],
 'nana-patinhas': ["very calm gentle lullaby", "soft felt piano and fingerpicked ukulele", "no drums, no percussion", "soft sustained strings pad, very quiet",
                   "very soft tender singing, close and calm, almost whispered but clear", "sleepy and peaceful"],
}
VAR = {
 'A': ["chorus melody uses only three neighbouring notes, moving step by step, very easy to sing", "simple call and answer with soft backing vocals echoing the hook"],
 'B': ["chorus melody uses four notes of the major scale with one small happy upward leap on the hook word, then gently falling back",
       "the lead instrument answers each sung line with a short echo"],
 'C': ["bouncy repeated-note melody on the hook, the last line resolves down to the home note", "soft backing vocals sing the answers in brackets"],
}
VAR_LULL = {
 'A': ["melody moves only by small steps, rocking like a cradle, three notes", "long held notes at the end of each line"],
 'B': ["gentle four-note melody that rises softly and falls back home, like a sigh", "piano answers each line softly"],
 'C': ["very simple two-bar phrase repeated, descending to the home note", "ukulele arpeggios answer each line"],
}
slug = sys.argv[1]; s = SONGS[slug]; bpm = s['bpm']; bar = round(4 * 60000 / bpm)
lull = slug == 'nana-patinhas'
bars = 8 if lull else 9
neg = NEG + (["drums", "percussion", "loud", "bright", "fast tempo"] if lull else ["fast tempo"])
ch = '\n'.join(s['pt']['chorus'])
for k in (sys.argv[2:] or ['A', 'B']):
    pos = ARR[slug] + (VAR_LULL if lull else VAR)[k] + [f"{bpm} BPM", "C major", "4/4", "happy major key" if not lull else "warm major key",
          "music for babies and toddlers", "vocal upfront and clear, clear diction, clean modern children's music production, studio quality",
          "very short instrumental intro, the vocal starts within two seconds", "simple catchy sing-along chorus", VOICE]
    plan = {'_meta': {'song': s['title'], 'what': f'chorus proposal {k}', 'bpm': bpm, 'key': 'C major'}, 'model_id': 'music_v2_5',
            'composition_plan': {'chunks': [{'text': '[Intro: short pickup]\n[Chorus]\n' + ch + '\n' + ch, 'duration_ms': bars * bar,
                                             'positive_styles': pos, 'negative_styles': neg, 'context_adherence': 'high'}]}}
    os.makedirs(f'{ROOT}/music/compositions/lote1/{slug}', exist_ok=True)
    json.dump(plan, open(f'{ROOT}/music/compositions/lote1/{slug}/chorus_{k}.json', 'w'), ensure_ascii=False, indent=1)
    print(slug, k, bars * bar, 'ms')
