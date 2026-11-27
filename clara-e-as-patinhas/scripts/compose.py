#!/usr/bin/env python3
"""Clara e as Patinhas - "A Danca das Patinhas" - original composition generator.

Writes:
  music/compositions/estrutura.json   (structure, timestamps, lyrics, melody notes)
  music/instrumentals/guia_instrumental.mid        (guide arrangement + melody line)
  music/instrumentals/guia_sem_melodia.mid         (same, without the melody guide)
All music here is original (melody, harmony and arrangement written for this project).
Key D major, 4/4, 115 BPM.
"""
import json, os
import mido

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BPM = 115
BEAT = 60.0 / BPM
BAR = 4 * BEAT
TPB = 480

# ---------- pitch helpers ----------
N = {}
for name, pc in [('C', 0), ('C#', 1), ('D', 2), ('D#', 3), ('E', 4), ('F', 5), ('F#', 6), ('G', 7),
                 ('G#', 8), ('A', 9), ('A#', 10), ('B', 11)]:
    for o in range(1, 7):
        N[f'{name}{o}'] = 12 * (o + 1) + pc
SCALE_PC = {2, 4, 6, 7, 9, 11, 1}  # D major
CHORDS = {  # pitch classes
    'D': [2, 6, 9], 'G': [7, 11, 2], 'A': [9, 1, 4], 'Bm': [11, 2, 6], 'Em': [4, 7, 11],
    'A7': [9, 1, 4, 7], 'Gmaj': [7, 11, 2],
}
ROOTS = {'D': N['D2'], 'G': N['G2'], 'A': N['A2'], 'A7': N['A2'], 'Bm': N['B2'], 'Em': N['E2'], 'Gmaj': N['G2']}


def snap(p, pcs):
    best = None
    for d in [0, 1, -1, 2, -2, 3, -3]:
        if (p + d) % 12 in pcs:
            return p + d
    return p


# ---------- lyric / melody data ----------
# Syllables: UPPERCASE = stressed. "_" = vowel elision sung as one syllable.
# Hand-written lines are given as explicit (syllable, pitch, beats) lists.
def H(*items):
    out = []
    for it in items:
        syl, p, d = it
        out.append((syl, None if p is None else N[p], d))
    return out

STING = H(('Cla', 'A4', .5), ('ra_e_as', 'F#4', .5), ('Pa', 'A4', .5), ('ti', 'B4', .5), ('nhas', 'D5', 1), (None, None, 1),
          (None, None, .5), ('(au!)', None, .5), ('(au!)', None, 1), (None, None, 2))
STING_NOTES = [(N['A4'], 0, .5), (N['F#4'], .5, .5), (N['A4'], 1, .5), (N['B4'], 1.5, .5), (N['D5'], 2, 1), (N['A4'], 3, .5),
               (N['B4'], 4, .5), (N['C#5'], 4.5, .5), (N['D5'], 5, 1.5), (N['A5'], 6.5, 1.5)]

CHORUS = [  # one bar per line
    ("Patinha pra frente,", H(('Pa', 'A4', .5), ('ti', 'A4', .5), ('nha', 'B4', .5), ('pra', 'A4', .5), ('FREN', 'D5', 1), ('te', 'A4', 1)), ['D']),
    ("Patinha pra trás,", H(('Pa', 'G4', .5), ('ti', 'G4', .5), ('nha', 'A4', .5), ('pra', 'G4', .5), ('TRÁS', 'E4', 2)), ['A']),
    ("Dá uma voltinha,", H(('DÁ', 'F#4', 1), ('u', 'G4', .5), ('ma', 'A4', .5), ('vol', 'B4', .5), ('TI', 'C#5', .5), ('nha', 'D5', 1)), ['G']),
    ("E dança muito mais!", H(('E', 'A4', .5), ('DAN', 'B4', .5), ('ça', 'A4', .5), ('MUI', 'F#4', .5), ('to', 'E4', 1), ('MAIS', 'D4', 1)), ['A', 'D']),
    ("Au, au, au, vamos brincar,", H(('AU', 'D5', .5), ('AU', 'D5', .5), ('AU', 'D5', .5), (None, None, .5), ('VA', 'A4', .5), ('mos', 'B4', .5), ('brin', 'C#5', .5), ('CAR', 'D5', .5)), ['D']),
    ("Au, au, au, vamos cantar!", H(('AU', 'B4', .5), ('AU', 'B4', .5), ('AU', 'B4', .5), (None, None, .5), ('VA', 'A4', .5), ('mos', 'G4', .5), ('can', 'F#4', .5), ('TAR', 'E4', .5)), ['G', 'A']),
    ("Bate palma, bate o pé,", H(('BA', 'F#4', .5), ('te', 'F#4', .5), ('PAL', 'A4', .5), ('ma', 'F#4', .5), ('BA', 'G4', .5), ('te_o', 'G4', .5), ('PÉ', 'B4', 1)), ['D', 'G']),
    ("Dança junto como quiser!", H(('DAN', 'A4', .5), ('ça', 'A4', .5), ('JUN', 'B4', .5), ('to', 'A4', .5), ('CO', 'G4', .5), ('mo', 'F#4', .5), ('qui', 'E4', .5), ('SER', 'D4', .5)), ['A', 'D']),
]
FINAL_TAIL = [  # final chorus lines 7-8, two bars each
    ("Com os amigos é tão bom viver,", H(('com_os', 'F#4', .5), ('a', 'G4', .5), ('MI', 'A4', 1), ('gos', 'F#4', .5), ('É', 'A4', .5), ('tão', 'B4', .5), ('BOM', 'D5', 1.5),
                                         ('vi', 'C#5', .5), ('VER', 'B4', 2.5)), ['D', 'D', 'G', 'G']),
    ("Dançando juntos, eu e você!", H(('dan', 'A4', .5), ('ÇAN', 'B4', 1), ('do', 'A4', .5), ('JUN', 'D5', 1), ('tos', 'B4', 1), ('EU_e', 'A4', .5), ('vo', 'E4', .5), ('CÊ', 'D4', 3)), ['A', 'A', 'D', 'D']),
]
ENDING = [  # one bar each, re-uses the sting motif
    ("Clara e as Patinhas,", H(('CLA', 'A4', .5), ('ra_e_as', 'F#4', .5), ('pa', 'A4', .5), ('TI', 'B4', .5), ('nhas', 'D5', 2)), ['D']),
    ("Que alegria!", H((None, None, .5), ('que_a', 'B4', .5), ('le', 'C#5', .5), ('GRI', 'D5', 1), ('a', 'B4', 1.5)), ['G', 'A']),
    ("Juntos brincando,", H(('JUN', 'B4', 1), ('tos', 'A4', .5), ('brin', 'G4', .5), ('CAN', 'F#4', 1), ('do', 'E4', 1)), ['Bm', 'G']),
    ("Todo dia!", H((None, None, .5), ('TO', 'E4', .5), ('do', 'F#4', .5), ('DI', 'A4', .5), ('a', 'D5', 2)), ['A', 'D']),
]

# Verse lines (2 bars each) generated from syllables + a melodic contour template.
VERSES = {
    'intro': [
        ("Clara chamou as amiguinhas,", "CLA ra cha MOU as a mi GUI nhas"),
        ("Vieram correndo três cachorrinhas!", "VIE ram cor REN do TRÊS ca chor RI nhas"),
        ("Ayra, Pandora e Tifa também,", "AI ra pan DO ra_e TI fa tam BÉM"),
        ("Vamos dançar, vem, vem, vem!", "VA mos dan ÇAR VEM VEM VEM"),
    ],
    'ayra': [
        ("Ayra corre pelo jardim,", "AI ra COR re pe lo jar DIM"),
        ("Mexe o rabinho e olha pra mim!", "ME xe_o ra BI nho_e O lha pra MIM"),
        ("Pula pra cá, pula pra lá,", "PU la pra CÁ PU la pra LÁ"),
        ("Que cachorrinha gosta de brincar!", "que ca chor RI nha GOS ta de brin CAR"),
    ],
    'pandora': [
        ("Pandora branquinha, fofinha demais,", "pan DO ra bran QUI nha fo FI nha de MAIS"),
        ("Dá uma voltinha e pede mais!", "DÁ u ma vol TI nha_e PE de MAIS"),
        ("Mexe as patinhas, começa a girar,", "ME xe_as pa TI nhas co ME ça_a gi RAR"),
        ("Com a Clara ela vai dançar!", "com_a CLA ra E la vai dan ÇAR"),
    ],
    'tifa': [
        ("Tifa pequena, cheia de energia,", "TI fa pe QUE na CHEI a de_e ner GI a"),
        ("Faz todo mundo sorrir de alegria!", "FAZ to do MUN do sor RIR de_a le GRI a"),
        ("Dá um pulinho: um, dois, três,", "DÁ um pu LI nho UM DOIS TRÊS"),
        ("Vamos dançar mais uma vez!", "VA mos dan ÇAR mais U ma VEZ"),
    ],
    'ponte': [
        ("Uma patinha, duas patinhas,", "U ma pa TI nha DU as pa TI nhas"),
        ("Três cachorrinhas fazendo festinha!", "TRÊS ca chor RI nhas fa ZEN do fes TI nha"),
        ("Uma voltinha, um salto no ar,", "U ma vol TI nha um SAL to no AR"),
        ("Todo mundo pronto pra dançar!", "TO do MUN do PRON to pra dan ÇAR"),
    ],
}
VERSE_CHORDS = ['D', 'G', 'A', 'D', 'G', 'D', 'Em', 'A']
BRIDGE_CHORDS = ['Bm', 'G', 'Em', 'A', 'Bm', 'G', 'Em', 'A']
# contour templates: (pre-stress start pitch, pre-stress end pitch, final stressed pitch, trailing pitch)
VERSE_TPL = [('D4', 'A4', 'B4', 'G4'), ('A4', 'F#4', 'A4', 'F#4'), ('G4', 'B4', 'D5', 'A4'), ('B4', 'F#4', 'E4', 'C#4')]
BRIDGE_TPL = [('F#4', 'A4', 'B4', 'G4'), ('G4', 'B4', 'C#5', 'A4'), ('A4', 'C#5', 'D5', 'B4'), ('B4', 'D5', 'E5', 'C#5')]


def is_stressed(s):
    core = s.replace('_', '')
    return core.upper() == core and any(c.isalpha() for c in core)


SCALE_LIST = sorted(p for p in range(40, 100) if p % 12 in SCALE_PC)


def step(p, k):
    i = min(range(len(SCALE_LIST)), key=lambda j: abs(SCALE_LIST[j] - p))
    return SCALE_LIST[max(0, min(len(SCALE_LIST) - 1, i + k))]


def gen_line(sylstr, tpl, chords2):
    """Place syllables on an 8th grid so stressed syllables land on beats when there is room;
    final stressed syllable lands on the downbeat of bar 2 and is held. Pitch follows the line's
    contour template with a small neighbour-note zig-zag; stressed notes snap to chord tones."""
    syl = sylstr.split()
    last = max(i for i, s in enumerate(syl) if is_stressed(s))
    pre, fin, trail = syl[:last], syl[last], syl[last + 1:]
    n = len(pre)
    slots = 8  # eighths available in bar 1
    pickup = max(0, n - slots)
    pos = -pickup
    starts = []
    for i, s in enumerate(pre):
        remaining = n - i  # syllables still to place including this
        slack = (slots - pos) - remaining
        if is_stressed(s) and pos % 2 == 1 and slack >= 1 and pos >= 0:
            pos += 1  # delay stressed syllable onto the beat (previous note lengthened)
        starts.append(pos)
        pos += 1
    # if there's leftover room at the start, shift everything later only up to the first beat structure
    # durations: until next start (last pre-syllable until 8)
    durs = [(starts[i + 1] if i + 1 < n else slots) - starts[i] for i in range(n)]
    # if line starts late (lots of slack), stretch: double durations of stressed notes from the front
    p0, p1, pf, pt = (N[x] for x in tpl)
    out = []
    for i, s in enumerate(pre):
        t = starts[i] / 2.0
        frac = i / max(1, n - 1)
        base = round(p0 + (p1 - p0) * frac)
        chord = chords2[0] if t < 4.0 else chords2[1]
        if is_stressed(s) or starts[i] % 2 == 0 and durs[i] > 1:
            p = snap(base, set(CHORDS[chord]))
        else:
            p = snap(base, SCALE_PC)
            if i % 2 == 1 and i < n - 1:
                p = step(p, -1 if (p1 >= p0) else 1)
        out.append((s, p, durs[i] / 2.0, t))
    if trail:
        out.append((fin, pf, 1.5, 4.0))
        tt = 5.5
        for j, s in enumerate(trail):
            d = 1.5 if j == len(trail) - 1 else .5
            out.append((s, pt if j == len(trail) - 1 else step(pf, -1), d, tt))
            tt += d
    else:
        out.append((fin, pf, 3.0, 4.0))
    return out


# ---------- song form ----------
FORM = [
    ('assinatura', 'sting', 2), ('intro_instrumental', 'hook', 2), ('intro', 'verse:intro', 8),
    ('refrao_1', 'chorus:8', 8), ('pausa_danca_1', 'break', 2), ('verso_ayra', 'verse:ayra', 8),
    ('refrao_2_curto', 'chorus:6', 6), ('pausa_danca_2', 'break', 2), ('verso_pandora', 'verse:pandora', 8),
    ('verso_tifa', 'verse:tifa', 8), ('ponte', 'verse:ponte', 8), ('refrao_final', 'final', 10),
    ('final', 'ending', 4), ('assinatura_final', 'sting', 2), ('ressonancia', 'ringout', 1),
]


def build():
    bar = 0
    sections, melody, chords, events = [], [], [], []  # melody: (pitch, start_beat_abs, dur, syl)
    for name, kind, nbars in FORM:
        sb = bar * 4
        sec = {'nome': name, 'tipo': kind.split(':')[0], 'compasso_inicio': bar + 1, 'compassos': nbars,
               'inicio_s': round(bar * BAR, 3), 'fim_s': round((bar + nbars) * BAR, 3), 'linhas': [], 'acentos': []}
        if kind == 'sting':
            chords += [(sb, 4, 'D'), (sb + 4, 4, 'D')]
            for p, t, d in STING_NOTES:
                events.append(('sting', p, sb + t, d))
            events += [('bark', 0, sb + 5.5, .25), ('bark', 0, sb + 6, .25)]
            sec['linhas'].append({'texto': '(instrumental: assinatura da marca, xilofone + sinos, 2 latidinhos)', 'notas': [
                {'nota': p, 'inicio_beat': t, 'dur': d} for p, t, d in STING_NOTES]})
            sec['acentos'] = [sb + 2, sb + 5, sb + 5.5, sb + 6]
        elif kind == 'hook':
            chords += [(sb, 4, 'D'), (sb + 4, 4, 'A')]
            t = sb
            for li in range(2):
                for syl, p, d in CHORUS[li][1]:
                    if p:
                        events.append(('hook', p, t, d))
                    t += d
            sec['linhas'].append({'texto': '(instrumental: gancho do refrao "Patinha pra frente / pra tras" no xilofone)'})
        elif kind.startswith('verse'):
            key = kind.split(':')[1]
            lines = VERSES[key]
            tpl = BRIDGE_TPL if key == 'ponte' else VERSE_TPL
            ch = BRIDGE_CHORDS if key == 'ponte' else VERSE_CHORDS
            chords += [(sb + 4 * i, 4, c) for i, c in enumerate(ch)]
            for li, (txt, sylstr) in enumerate(lines):
                notes = gen_line(sylstr, tpl[li], ch[2 * li:2 * li + 2])
                lb = sb + 8 * li
                ln = []
                for s, p, d, t in notes:
                    melody.append((p, lb + t, d, s))
                    ln.append({'silaba': s, 'nota': p, 'inicio_beat': lb + t, 'dur': d})
                sec['linhas'].append({'texto': txt, 'inicio_s': round((lb + notes[0][3]) * BEAT, 3), 'notas': ln})
                sec['acentos'].append(lb + 4)
        elif kind.startswith('chorus') or kind == 'final':
            n = 6 if kind == 'chorus:6' else (6 if kind == 'final' else 8)
            t = sb
            src = CHORUS[:n] + (FINAL_TAIL if kind == 'final' else [])
            for txt, notes, chs in src:
                lb = t
                nb = sum(d for _, _, d in notes)
                per = nb / len(chs)
                for i, c in enumerate(chs):
                    chords.append((lb + i * per, per, c))
                ln = []
                for s, p, d in notes:
                    if p:
                        melody.append((p, t, d, s))
                        ln.append({'silaba': s, 'nota': p, 'inicio_beat': t, 'dur': d})
                    t += d
                sec['linhas'].append({'texto': txt, 'inicio_s': round(lb * BEAT, 3), 'notas': ln})
            sec['acentos'] = [sb + 4 * i for i in range(nbars)]
            sec['coreografia'] = {'Patinha pra frente': 'Clara pe a frente / cachorrinhas levantam pata dianteira',
                                  'Patinha pra tras': 'passinho para tras', 'Da uma voltinha': 'giro pequeno',
                                  'Bate palma, bate o pe': 'palmas nos tempos 2 e 4 / pisada no "pe"'}
        elif kind == 'ending':
            t = sb
            for txt, notes, chs in ENDING:
                lb = t
                for i, c in enumerate(chs):
                    chords.append((lb + i * 4 / len(chs), 4 / len(chs), c))
                ln = []
                for s, p, d in notes:
                    if p:
                        melody.append((p, t, d, s))
                        ln.append({'silaba': s, 'nota': p, 'inicio_beat': t, 'dur': d})
                    t += d
                sec['linhas'].append({'texto': txt, 'inicio_s': round(lb * BEAT, 3), 'notas': ln})
        elif kind == 'break':
            chords += [(sb, 4, 'D'), (sb + 4, 4, 'A')]
            events += [('bark', 0, sb + 1, .25), ('bark', 0, sb + 1.5, .25), ('bark', 0, sb + 5, .25)]
            sec['linhas'].append({'texto': '(instrumental: palmas + latidinhos ritmicos, danca livre)'})
            for b in range(nbars * 4):
                events.append(('xylo_fill', [N['D5'], N['F#5'], N['A5'], N['F#5']][b % 4] if b < 4 else [N['E5'], N['C#5'], N['A4'], N['C#5']][b % 4], sb + b, .5))
        elif kind == 'ringout':
            chords.append((sb, 4, 'D'))
            sec['linhas'].append({'texto': '(acorde final em Re maior)'})
        sec['beats'] = list(range(sb, sb + nbars * 4))
        sections.append(sec)
        bar += nbars
    return sections, melody, chords, events, bar


def section_of(beat, sections):
    for s in sections:
        if s['beats'] and s['beats'][0] <= beat <= s['beats'][-1] + 0.999:
            return s
    return sections[-1]


def write_midi(path, melody, chords, events, sections, total_bars, with_melody=True):
    mid = mido.MidiFile(ticks_per_beat=TPB)
    meta = mido.MidiTrack(); mid.tracks.append(meta)
    meta.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(BPM)))
    meta.append(mido.MetaMessage('time_signature', numerator=4, denominator=4))
    meta.append(mido.MetaMessage('key_signature', key='D'))
    tracks = {}
    # channel: (program, name, volume)
    CH = {0: (73, 'Melodia guia (flauta)', 92), 1: (24, 'Violao nylon / ukulele', 80), 2: (0, 'Piano', 64),
          3: (13, 'Xilofone', 92), 4: (12, 'Marimba', 66), 5: (32, 'Baixo acustico', 98), 6: (9, 'Glockenspiel / sinos', 70),
          9: (0, 'Percussao', 92)}
    notes = {c: [] for c in CH}  # (start_beat, dur, pitch, vel)

    def add(c, t, d, p, v):
        notes[c].append((t, d, p, v))

    if with_melody:
        for p, t, d, s in melody:
            add(0, t, d * 0.92, p, 92 if s and is_stressed(s) else 78)
    for kind, p, t, d in events:
        if kind == 'sting':
            add(3, t, d, p, 110); add(6, t, d, p + 12, 72)
        elif kind == 'hook':
            add(3, t, d, p, 105)
        elif kind == 'xylo_fill':
            add(3, t, d, p, 82)
    for (t, d, c) in chords:
        sec = section_of(t, sections)
        typ = sec['tipo']
        pcs = CHORDS[c]
        root = ROOTS[c]
        energetic = typ in ('chorus', 'final', 'break', 'hook')
        # guitar/ukulele strum: 8ths with accents (D . D U . U D U)
        gv = [snap(N['D4'] + 0, set(pcs))]
        voicing = sorted({snap(x, set(pcs)) for x in [N['F#3'], N['A3'], N['D4'], N['F#4']]})
        pat = [(0, 95), (1, 70), (1.5, 80), (2.5, 72), (3, 88), (3.5, 70)]
        for off, vel in pat:
            if off < d:
                for k, p in enumerate(voicing):
                    add(1, t + off + k * 0.015, 0.45, p, vel - (0 if energetic else 12))
        # bass: root on 1, fifth on 3, approach on 4&
        add(5, t, min(d, 1.5) * 0.9, root, 100)
        if d >= 4:
            add(5, t + 2, 1.4, root + 7, 88)
            add(5, t + 3.5, 0.45, root + 12 if energetic else root + 7, 80)
        elif d >= 2:
            add(5, t + 1, 0.9, root + 7, 85)
        # piano: offbeat block chords (beats 2 and 4)
        pv = sorted({snap(x, set(pcs)) for x in [N['A4'], N['D5'], N['F#5']]})
        for off in (1, 3):
            if off < d and typ != 'sting':
                for p in pv:
                    add(2, t + off, 0.8, p - 12, 56 if energetic else 48)
        # marimba arpeggio in verses/bridge
        if typ in ('verse',):
            arp = [root + 24, root + 24 + (pcs[1] - pcs[0]) % 12, root + 24 + (pcs[2] - pcs[0]) % 12, root + 36]
            for k in range(int(d * 2)):
                add(4, t + k * 0.5, 0.45, arp[[0, 1, 2, 3, 2, 1, 0, 1][k % 8]], 62 if k % 2 == 0 else 50)
    # percussion
    end_beat = total_bars * 4
    for sec in sections:
        typ = sec['tipo']
        for b in sec['beats']:
            beat_in_bar = b % 4
            if typ in ('ringout',):
                continue
            if typ == 'sting':
                if beat_in_bar in (0,):
                    add(9, b, .2, 81, 80)  # open triangle
                continue
            add(9, b, .2, 36, 78 if beat_in_bar in (0, 2) else 0) if beat_in_bar in (0, 2) else None
            for half in (0, .5):
                add(9, b + half, .1, 70, 58 if half == 0 else 44)  # maracas / shaker
            if typ in ('chorus', 'final', 'break', 'hook', 'ending'):
                if beat_in_bar in (1, 3):
                    add(9, b, .2, 39, 96)  # hand clap
                    add(9, b, .2, 54, 60)  # tambourine
            else:
                if beat_in_bar in (1, 3):
                    add(9, b, .2, 37, 55)  # side stick
    # bells / sparkle on every "voltinha" (spin) and at section starts
    for p, t, d, s in melody:
        if s and s.upper() == 'TI' and section_of(t, sections)['tipo'] in ('chorus', 'final'):
            for k, q in enumerate([N['D6'], N['F#6'], N['A6'], N['D6'] + 12]):
                add(6, t + k * 0.125, 0.3, min(q, 108), 60)
    for sec in sections:
        add(6, sec['beats'][0], 2, N['A5'], 45)
    # final chord
    last = sections[-1]['beats'][0]
    for p in [N['D3'], N['A3'], N['D4'], N['F#4'], N['A4']]:
        add(1, last, 3.5, p, 80)
    add(5, last, 3.5, N['D2'], 95)
    add(6, last, 3.5, N['D6'], 70)
    add(3, last, 1, N['D5'], 100)

    for c, (prog, name, vol) in CH.items():
        tr = mido.MidiTrack(); mid.tracks.append(tr)
        tr.append(mido.MetaMessage('track_name', name=name))
        if c != 9:
            tr.append(mido.Message('program_change', channel=c, program=prog, time=0))
        tr.append(mido.Message('control_change', channel=c, control=7, value=vol, time=0))
        tr.append(mido.Message('control_change', channel=c, control=91, value=40, time=0))  # reverb
        evs = []
        for t, d, p, v in notes[c]:
            if v <= 0 or t < 0:
                continue
            evs.append((int(t * TPB), 1, p, v))
            evs.append((int((t + d) * TPB), 0, p, 0))
        evs.sort(key=lambda e: (e[0], e[1]))
        now = 0
        for tick, on, p, v in evs:
            tr.append(mido.Message('note_on' if on else 'note_off', channel=c, note=int(p), velocity=int(v), time=tick - now))
            now = tick
    mid.save(path)


def main():
    sections, melody, chords, events, total_bars = build()
    os.makedirs(f'{ROOT}/music/instrumentals', exist_ok=True)
    write_midi(f'{ROOT}/music/instrumentals/guia_instrumental.mid', melody, chords, events, sections, total_bars, True)
    write_midi(f'{ROOT}/music/instrumentals/guia_sem_melodia.mid', melody, chords, events, sections, total_bars, False)
    barks = [round(t * BEAT, 3) for k, p, t, d in events if k == 'bark']
    for s in sections:
        del s['beats']
    struct = {
        'titulo': 'A Dança das Patinhas', 'serie': 'Clara e as Patinhas', 'episodio': '001',
        'bpm': BPM, 'compasso': '4/4', 'tonalidade': 'Ré maior (D)', 'segundos_por_beat': round(BEAT, 5),
        'segundos_por_compasso': round(BAR, 5), 'total_compassos': total_bars,
        'duracao_musical_s': round(total_bars * BAR, 2), 'duracao_com_cauda_s': round(total_bars * BAR + 1.5, 2),
        'gancho_principal': 'Assinatura (0:00-0:04) usa o mesmo contorno do refrão "Pa-ti-nha pra fren-te" (Lá-Fá#-Lá-Si-Ré); o gancho completo toca no xilofone em 0:04-0:08.',
        'assinatura_marca': {'compassos': 2, 'notas_midi': [n[0] for n in STING_NOTES],
                             'descricao': 'Lá4 Fá#4 Lá4 Si4 | Ré5 — Lá4 | Si4 Dó#5 Ré5 — Lá5 (xilofone + glockenspiel) + 2 latidinhos; reutilizável como vinheta de abertura/fechamento.'},
        'latidos_s': barks,
        'notas_formato': 'nota = número MIDI (60 = Dó4); inicio_beat = beat absoluto desde o início (0-based); dur em beats.',
        'secoes': sections,
    }
    with open(f'{ROOT}/music/compositions/estrutura.json', 'w', encoding='utf-8') as f:
        json.dump(struct, f, ensure_ascii=False, indent=1)
    print('bars', total_bars, 'duration', round(total_bars * BAR, 2))
    for s in sections:
        print(f"{s['nome']:22s} {s['inicio_s']:7.2f}-{s['fim_s']:7.2f}")


if __name__ == '__main__':
    main()
