"""Lote 1 full songs (PT original + EN/ES on the same timing map), pilot pipeline.

  build_full.py SLUG pt                       -> plan full_pt.json   (chorus = chosen PT proposal, reused by reference)
  build_full.py SLUG chorus_en|chorus_es      -> plan chorus_<lg>.json (PT intro by reference + <lg> chorus x2, 2*CH)
  build_full.py SLUG full_en|full_es SONGID   -> plan full_<lg>.json (same chunk durations as PT)
Section map is written to music/compositions/lote1/<slug>/sections.json (shared by all languages).
Never names artists or existing songs."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_chorus import SONGS, ARR, NEG, VAR, VAR_LULL, ROOT

CFG = {  # chosen chorus proposal (PT), its song_id, requested BPM
    'au-au-ayra': dict(k='B', sid='XGydOA6eLQkXnIUtnbOx', bpm=95, brk=True,
                       outro={'pt': 'Au, au, au... Ayra!', 'en': 'Woof, woof, woof... Ayra!', 'es': '¡Guau, guau, guau... Ayra!'},
                       brk_txt='the accordion plays the hook, two small happy dog barks, light hand drum'),
    'miau-miau-milo': dict(k='A', sid='AtggjgKBrpqm1ja9drXt', bpm=100, brk=True,
                           outro={'pt': 'Miau, miau... Milo!', 'en': 'Meow, meow... Milo!', 'es': '¡Miau, miau... Milo!'},
                           brk_txt='the pizzicato strings play the hook, two soft kitten meows, glockenspiel sparkle'),
    'nana-patinhas': dict(k='A', sid='C78sYznHoPvevnzXFLno', bpm=70, brk=False,
                          outro={'pt': 'Nana, naná... (hum, hum)', 'en': 'Nana, nana... (hmm, hmm)', 'es': 'Nana, naná... (mm, mm)'},
                          brk_txt=''),
}
VOICE = {'pt': "natural Brazilian Portuguese", 'en': "natural American English", 'es': "natural neutral Latin American Spanish"}
ACC_NEG = {'pt': ["European Portuguese accent", "Spanish accent"], 'en': ["British accent", "Brazilian accent", "Spanish accent"],
           'es': ["Castilian Spain accent", "Brazilian Portuguese", "English"]}


def voice(lg):
    return ("the same warm young adult female lead singer throughout the whole song, identical voice, timbre and vocal register in every "
            f"section, sweet and clear, {VOICE[lg]}")


def chunk(slug, lg, text, ms, extra, instrumental=False):
    s = SONGS[slug]; lull = slug == 'nana-patinhas'
    pos = ARR[slug] + extra + [f"{CFG[slug]['bpm']} BPM", "C major", "4/4", "music for babies and toddlers",
                               "same tempo and key as the surrounding song", "clean modern children's music production, studio quality"]
    if not instrumental:
        pos += ["warm young adult female lead singer, same voice, timbre and register as the rest of the song", voice(lg)]
    neg = [n for n in NEG if 'accent' not in n] + ACC_NEG[lg] + (["drums", "percussion", "loud", "fast tempo"] if lull else ["fast tempo"])
    if instrumental:
        neg += ["vocals", "lyrics", "singing"]
    return {'text': text, 'duration_ms': ms, 'positive_styles': pos, 'negative_styles': neg, 'context_adherence': 'high'}


def plan_sections(slug):
    bar = round(4 * 60000 / CFG[slug]['bpm']); CH = 4 * bar
    sec = [('intro', 3000), ('chorus_1', CH), ('verse_1', 8 * bar), ('chorus_2', CH), ('verse_2', 8 * bar), ('chorus_3', CH), ('verse_3', 8 * bar)]
    if CFG[slug]['brk']:
        sec.append(('break', 4 * bar))
    sec += [('chorus_final_x2', 2 * CH), ('outro', 2 * bar)]
    return bar, CH, sec


def ref(sid, a, b):
    return {'song_id': sid, 'range': {'start_ms': a, 'end_ms': b}}


def full(slug, lg, chorus_sid, intro_sid=None):
    s = SONGS[slug]; c = CFG[slug]; bar, CH, sec = plan_sections(slug)
    verses = s[lg]['verses']; chunks = []; t = 0; smap = []
    for name, ms in sec:
        if name == 'intro':
            ch = ref(intro_sid, 0, 3000) if intro_sid else chunk(slug, lg, '[Intro]', 3000, ['very short instrumental pickup into the chorus, three seconds'], True)
        elif name.startswith('chorus_final') and intro_sid:  # EN/ES: one sung chorus (CH) reused twice
            chunks += [ref(chorus_sid, 3000, 3000 + CH)]; ch = ref(chorus_sid, 3000, 3000 + CH)
        elif name.startswith('chorus') and intro_sid:
            ch = ref(chorus_sid, 3000, 3000 + CH)
        elif name.startswith('chorus_final'):
            ch = ref(chorus_sid, 0, 2 * CH)
        elif name.startswith('chorus'):
            ch = ref(chorus_sid, 0, CH) if name in ('chorus_1', 'chorus_3') else ref(chorus_sid, CH, 2 * CH)
        elif name.startswith('verse'):
            vt, vl = verses[int(name[-1]) - 1]
            ch = chunk(slug, lg, f'[Verse: {vt}]\n' + '\n'.join(vl) + '\n' + '\n'.join(vl), ms,
                       ['verse sung on the same few notes and the same melody family as the chorus', 'the four lines are sung twice',
                        'the lead instrument answers between lines'])
        elif name == 'break':
            ch = chunk(slug, lg, '[Instrumental break]', ms, [c['brk_txt'], 'playful instrumental dance break'], True)
        else:
            ch = chunk(slug, lg, '[Outro]\n' + c['outro'][lg], ms, ['gentle natural ending', 'final soft chord'])
        chunks.append(ch); smap.append({'name': name, 'start_ms': t, 'end_ms': t + ms}); t += ms
    return chunks, smap, t


if __name__ == '__main__':
    slug, what = sys.argv[1], sys.argv[2]; c = CFG[slug]; out = f'{ROOT}/music/compositions/lote1/{slug}'
    bar, CH, _ = plan_sections(slug)
    if what == 'pt':
        chunks, smap, tot = full(slug, 'pt', c['sid'])
        json.dump({'song': SONGS[slug]['title'], 'bpm': c['bpm'], 'bar_ms': bar, 'chorus_ms': CH, 'duration_ms': tot, 'sections': smap},
                  open(f'{out}/sections.json', 'w'), indent=1)
        plan = {'_meta': {'what': f'full PT, chorus = proposal {c["k"]} by reference', 'total_ms': tot}, 'model_id': 'music_v2_5',
                'composition_plan': {'chunks': chunks}}
        json.dump(plan, open(f'{out}/full_pt.json', 'w'), ensure_ascii=False, indent=1); print('full_pt', tot)
    elif what.startswith('chorus_'):
        lg = what[7:]; pt_sid = sys.argv[3]
        ch = '\n'.join(SONGS[slug][lg]['chorus'])
        plan = {'_meta': {'what': f'{lg} chorus (once, CH) on the PT intro'}, 'model_id': 'music_v2_5', 'composition_plan': {'chunks': [
            ref(pt_sid, 0, 3000),
            chunk(slug, lg, '[Chorus]\n' + ch, CH, ['simple catchy sing-along chorus', 'very simple chorus melody on few notes',
                                                                   'soft backing vocals sing the answers in brackets'])]}}
        json.dump(plan, open(f'{out}/chorus_{lg}.json', 'w'), ensure_ascii=False, indent=1); print('chorus', lg)
    elif what.startswith('full_'):
        lg = what[5:]; csid, pt_sid = sys.argv[3], sys.argv[4]
        chunks, smap, tot = full(slug, lg, csid, intro_sid=pt_sid)
        plan = {'_meta': {'what': f'full {lg}, same timing map as PT', 'total_ms': tot}, 'model_id': 'music_v2_5', 'composition_plan': {'chunks': chunks}}
        json.dump(plan, open(f'{out}/full_{lg}.json', 'w'), ensure_ascii=False, indent=1); print('full', lg, tot)
