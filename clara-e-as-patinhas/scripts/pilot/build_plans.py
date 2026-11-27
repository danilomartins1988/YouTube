"""Composition plans for the pilot "Pata Pata Patatá" (xote). Voice lock = VOICE_PROFILE.md.
Never names real artists or existing songs in prompts."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = f'{ROOT}/music/compositions/pilot'
BPM, KEY = 95, 'C major'
BAR = round(4 * 60000 / BPM)  # 2526 ms (API: every generated chunk >= 3000 ms)
VOICE = ("the same warm young adult female lead singer throughout the whole song, identical voice, timbre and vocal "
         "register in every section, sweet and clear, natural Brazilian Portuguese")
STYLE = ["gentle Brazilian forró pé-de-serra in a slow, soft xote groove", "sanfona accordion is the lead instrument and carries the hook",
         "triangle keeps a light steady pulse", "soft zabumba", "light acoustic bass", f"{BPM} BPM", KEY, "4/4",
         "happy major key", "gentle dynamics, warm and cheerful, music for babies and toddlers",
         "vocal upfront and bright, clear diction, clean modern children's music production, studio quality"]
NEG = ["electric guitar", "synthesizer", "EDM", "heavy drums", "loud zabumba", "fast tempo", "aggressive vocals", "rap", "autotune",
       "sad", "dark", "minor key", "scary", "male lead vocal", "European Portuguese accent", "Spanish accent", "different singer",
       "voice change between sections", "child lead voice", "high-pitched chipmunk vocal", "pitched-up vocal", "falsetto",
       "shrill", "reverb wash", "muddy mix", "explicit content"]
CHORUS = "Pata, pata, patatá!\nPata, pata, patatá!\nBate palma, bate o pé!\nPata, pata, patatá!"
PROPOSALS = {
 'A': ["chorus melody uses only three neighbouring notes, moving step by step, very easy to sing",
       "'pata, pata' on a repeated note, 'patatá' steps up and comes back home", "the accordion answers each sung line with a short echo"],
 'B': ["chorus melody with one happy upward leap on 'patatá', then gently falling back",
       "soft backing vocals echo 'patatá'", "hand claps on 'bate palma'"],
 'D': ["chorus melody uses only four notes of the major scale, bouncy and joyful",
       "'bate palma, bate o pé' sung on a descending line", "the accordion answers each sung line"],
 'E': ["very simple chorus melody, 'pata, pata' on a repeated note and 'patatá' lifting up with joy",
       "soft backing vocals echo 'patatá'", "hand claps on 'bate palma'"],
 'C': ["bouncy playful phrasing that sits on the xote swing", "'bate palma, bate o pé' sung on a descending line",
       "the accordion doubles the vocal melody an octave below"],
}
def chunk(text, bars, extra, instrumental=False):
    pos = STYLE + extra + ([] if instrumental else [VOICE])
    neg = NEG + (['vocals', 'lyrics', 'singing'] if instrumental else [])
    return {'text': text, 'duration_ms': bars * BAR, 'positive_styles': pos, 'negative_styles': neg, 'context_adherence': 'high'}
os.makedirs(OUT, exist_ok=True)
import sys
for k, extra in PROPOSALS.items():
    if len(sys.argv) > 1 and k not in sys.argv[1:]: continue
    plan = {'_meta': {'song': 'Pata Pata Patatá', 'what': f'chorus proposal {k}', 'bpm': BPM, 'key': KEY},
            'model_id': 'music_v2_5',
            'composition_plan': {'chunks': [chunk('[Intro: accordion hook, one bar]\n[Chorus]\n' + CHORUS + '\n' + CHORUS, 9,
                                                  ['very short one-bar accordion intro, then the vocal starts', 'simple catchy sing-along chorus'] + extra)]}}
    json.dump(plan, open(f'{OUT}/chorus_{k}.json', 'w'), ensure_ascii=False, indent=1)
print('bar ms', BAR)

# ---------------- full PT song: chorus E reused by reference (identical melody + voice every time) ----------------
E_ID = 'AJ9DqGXvKvVlWJKmwH19'
CH = round(4 * 60000 / 94.85 * 4)  # 4 bars at the measured 94.85 BPM = 10120 ms
def ref(a, b): return {'song_id': E_ID, 'range': {'start_ms': a, 'end_ms': b}}
VERSE_EXTRA = ['verse sung on the same few notes and the same melody family as the chorus', 'same tempo and key as the surrounding song',
               'warm young adult female lead singer, same voice, timbre and register as the rest of the song']
def verse(tag, lines, instr, bars=6):
    return chunk(f'[{tag}]\n' + '\n'.join(lines), bars, VERSE_EXTRA + instr)
if 'full_pt' in sys.argv[1:]:
    G = 2 * 6 * 0  # placeholder
    chunks = [
        chunk('[Intro]', 0, ['very short accordion pickup into the chorus, three seconds', 'same tempo and key as the following song'], True) | {'duration_ms': 3000},
        ref(0, CH),
        verse('Verse: Ayra', ['Ayra faz au, au, au!', 'Au, au, au!', 'Au, au, au!', 'Ayra faz au, au, au!', 'Balança o rabinho!'],
              ['a soft hand drum joins for this verse', 'one bar of accordion at the end of the verse']),
        ref(CH, 2 * CH),
        verse('Verse: Pandora', ['Pandora pula, pula, pula!', 'Pula, pula, pula!', 'Pula, pula, pula!', 'Pandora pula, pula, pula!', 'Balança o rabinho!'],
              ['a gentle xylophone plays little fills in this verse', 'one bar of accordion at the end of the verse']),
        ref(0, CH),
        verse('Verse: Toby', ['Toby gira, gira, gira!', 'Gira, gira, gira!', 'Gira, gira, gira!', 'Toby gira, gira, gira!', 'Balança o rabinho!'],
              ['a soft muted trumpet plays little fills in this verse', 'one bar of accordion at the end of the verse']),
        ref(CH, 2 * CH),
        verse('Verse: Milo', ['Milo faz miau, miau, miau!', 'Miau, miau, miau!', 'Miau, miau, miau!', 'Milo faz miau, miau, miau!', 'E mexe o rabinho!'],
              ['pizzicato violin plays little fills in this verse', 'one bar of accordion at the end of the verse']),
        verse('Verse: Clara', ['Clara bate palma, palma!', 'Palma, palma, palma!', 'Clara bate palma, palma!', 'Vamos todos dançar!'],
              ['ukulele strums join the accordion', 'hand claps', 'ends with two bars of instrumental dance groove, accordion and claps']),
        ref(0, 2 * CH),
        chunk('[Outro]\nPata, pata... patatá!', 2, ['gentle ending', 'final accordion chord', 'a small happy dog bark and a soft kitten meow at the very end'] + VERSE_EXTRA),
    ]
    plan = {'_meta': {'song': 'Pata Pata Patatá', 'what': 'full PT song, chorus = proposal E reused by reference', 'chorus_song_id': E_ID,
                      'bpm': 94.85, 'key': 'C major (target)'}, 'model_id': 'music_v2_5', 'composition_plan': {'chunks': chunks}}
    json.dump(plan, open(f'{OUT}/full_pt.json', 'w'), ensure_ascii=False, indent=1)
    tot = sum(c.get('duration_ms') or (c['range']['end_ms'] - c['range']['start_ms']) for c in chunks)
    print('full_pt total ms', tot, 'chunks', len(chunks))
