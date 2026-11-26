"""Kids channel test 01: "Vamos Contar os Bichinhos!" -- song definition (single source of truth).

Original lyrics and melody (pt-BR), counting 1-10 with animal sounds. Everything downstream (MIDI arrangement,
voice placement, karaoke timing, animation cues) is derived from the data in this file.

Times are in bars/beats on a fixed grid: 4/4, BPM below. A "line" occupies 2 bars (8 beats); each lyric word has
a target onset in beats from the start of its line, and each melody note is (beat, length_beats, midi_pitch)
written in the vocal octave (C4 = 60). The xylophone lead plays it an octave up.
"""
from __future__ import annotations

TITLE = "Vamos Contar os Bichinhos!"
SLUG = "kids_test01"
BPM = 112
KEY = "C major (Dó maior)"
BEAT = 60.0 / BPM
BAR = 4 * BEAT
TOTAL_BARS = 56
TAIL_SECONDS = 2.5  # final chord ring-out after the last bar

# chord symbols -> (root midi for bass, triad pitches in the vocal octave)
CHORDS = {
    "C": (36, [60, 64, 67]),
    "F": (41, [60, 65, 69]),
    "G": (43, [59, 62, 67]),
    "Am": (45, [60, 64, 69]),
}

# (name, kind, start_bar, n_bars)
SECTIONS = [
    ("intro", "intro", 0, 4),
    ("chorus1", "chorus", 4, 8),
    ("verse1", "verse", 12, 12),
    ("chorus2", "chorus", 24, 8),
    ("verse2", "verse", 32, 12),
    ("chorus3", "chorus", 44, 8),
    ("outro", "outro", 52, 4),
]

CHORD_BARS: list[str] = (
    ["C", "F", "G", "G"]                                     # intro
    + ["C", "C", "F", "G", "C", "F", "G", "C"]               # chorus 1
    + ["C", "G", "F", "C"] * 2 + ["C", "G", "F", "G"]        # verse 1 (5 numbers + tag)
    + ["C", "C", "F", "G", "C", "F", "G", "C"]               # chorus 2
    + ["C", "G", "F", "C"] * 2 + ["C", "G", "F", "G"]        # verse 2
    + ["C", "C", "F", "G", "C", "F", "G", "C"]               # chorus 3
    + ["C", "F", "G", "C"]                                   # outro
)
assert len(CHORD_BARS) == TOTAL_BARS

# ---------------------------------------------------------------- chorus (4 lines x 2 bars)
CHORUS = [
    {"text": "Um, dois, três, vamos contar!",
     "words": [("Um,", 0), ("dois,", 1), ("três,", 2), ("vamos", 3), ("contar!", 4)],
     "melody": [(0, 1, 60), (1, 1, 64), (2, 1, 67), (3, .5, 69), (3.5, .5, 67), (4, 1, 64), (5, 2.5, 67)]},
    {"text": "Os bichinhos vêm brincar!",
     "words": [("Os", 0), ("bichinhos", 0.5), ("vêm", 2), ("brincar!", 4)],
     "melody": [(0, .5, 65), (.5, .5, 65), (1, .5, 69), (1.5, .5, 69), (2, 2, 72), (4, 1, 71), (5, 2.5, 67)]},
    {"text": "Bate palma, bate o pé,",
     "words": [("Bate", 0), ("palma,", 1), ("bate", 4), ("o", 5), ("pé,", 6)],
     "melody": [(0, .5, 64), (.5, .5, 64), (1, .5, 67), (1.5, .5, 67), (4, .5, 69), (4.5, .5, 69), (5, 1, 67),
                (6, 1.5, 69)],
     "claps": [2, 3, 7, 7.5]},
    {"text": "Conta junto: oba, olé!",
     "words": [("Conta", 0), ("junto:", 1), ("oba,", 2), ("olé!", 4)],
     "melody": [(0, .5, 62), (.5, .5, 62), (1, .5, 67), (1.5, .5, 67), (2, .5, 71), (2.5, 1, 71), (4, 1, 67),
                (5, 2.5, 72)]},
]

# ---------------------------------------------------------------- verses: (number, numeral word, animal, sounds)
# pattern "A" melody resolves upward (C|G), "B" comes home (F|C)
VERSE1 = [
    (1, "Um", "patinho", "patinho", ["quá,", "quá!"], "faz"),
    (2, "Dois", "gatinhos,", "gatinho", ["miau,", "miau!"], None),
    (3, "Três", "cachorros,", "cachorro", ["au,", "au,", "au!"], None),
    (4, "Quatro", "vaquinhas,", "vaca", ["muuu,", "muuu!"], None),
    (5, "Cinco", "ovelhas,", "ovelha", ["béé,", "béé!"], None),
]
VERSE2 = [
    (6, "Seis", "pintinhos,", "pintinho", ["piu,", "piu,", "piu!"], None),
    (7, "Sete", "porquinhos,", "porquinho", ["oinc,", "oinc!"], None),
    (8, "Oito", "sapinhos,", "sapo", ["croac,", "croac!"], None),
    (9, "Nove", "abelhas,", "abelha", ["zum,", "zum,", "zum!"], None),
    (10, "Dez", "macaquinhos,", "macaco", ["uh,", "uh,", "ah!"], None),
]
TAGS = {
    1: {"text": "Cinco amigos, que legal!", "words": [("Cinco", 0), ("amigos,", 1), ("que", 3.5), ("legal!", 4)]},
    2: {"text": "Dez amigos no quintal!", "words": [("Dez", 0), ("amigos", 1), ("no", 3.5), ("quintal!", 4)]},
}
TAG_MELODY = [(0, .5, 69), (.5, .5, 69), (1, .5, 72), (1.5, .5, 72), (2, 1.5, 69), (3.5, .5, 67), (4, 1, 71),
              (5, 2.5, 74)]

INTRO_LINE = {"text": "Oi, criançada! Vamos contar?",
              "words": [("Oi,", 0), ("criançada!", 1), ("Vamos", 4), ("contar?", 5)], "melody": []}
OUTRO_LINE = {"text": "Tchau, tchau, bichinhos! Até a próxima!",
              "words": [("Tchau,", 0), ("tchau,", 1), ("bichinhos!", 2), ("Até", 4), ("a", 5), ("próxima!", 5.5)],
              "melody": [(0, 1, 72), (1, 1, 69), (2, 2, 67), (4, .5, 65), (4.5, .5, 64), (5, .5, 62),
                         (5.5, 2.5, 60)]}


def _syllables(word: str) -> int:
    import re
    w = re.sub(r"[^a-záàâãéêíóôõúüç]", "", word.lower())
    groups = re.findall(r"[aeiouáàâãéêíóôõúü]+", w)
    n = 0
    for g in groups:  # Portuguese: most vowel pairs are diphthongs except a few hiatus pairs
        n += 1 + sum(1 for a, b in zip(g, g[1:]) if a + b in ("ea", "eo", "oa", "ia", "ua", "ée", "uu", "úu"))
    return max(1, n)


def verse_line(n, numeral, animal, sounds, faz, pattern):
    words = [(numeral, 0), (animal, 1)]
    if faz:
        words.append((faz, 3))
    for i, s in enumerate(sounds):
        words.append((s, 4 + i))
    syl = _syllables(numeral)
    melody = []
    # numeral: one beat (two eighths if two syllables)
    num_pitch = 67 if pattern == "A" else 69
    if syl >= 2:
        melody += [(0, .5, num_pitch), (.5, .5, num_pitch)]
    else:
        melody += [(0, 1, num_pitch)]
    seq = [64, 64, 67, 67, 65, 64] if pattern == "A" else [65, 65, 69, 69, 67, 65]
    k = _syllables(animal) + (1 if faz else 0)
    for i in range(min(k, 5)):
        melody.append((1 + .5 * i, .5 if i < k - 1 else 1, seq[i]))
    if pattern == "A":
        snd = [(4, 1, 71), (5, 2.5, 67)] if len(sounds) == 2 else [(4, 1, 71), (5, 1, 71), (6, 1.5, 67)]
    else:
        snd = [(4, 1, 67), (5, 2.5, 60)] if len(sounds) == 2 else [(4, 1, 67), (5, 1, 64), (6, 1.5, 60)]
    melody += snd
    text = f"{numeral} {animal} " + (f"{faz} " if faz else "") + " ".join(sounds)
    return {"text": text, "words": words, "melody": melody}


ANIMAL_ICON = {  # animal key used by the Remotion character renderer
    "patinho": "duck", "gatinho": "cat", "cachorro": "dog", "vaca": "cow", "ovelha": "sheep",
    "pintinho": "chick", "porquinho": "pig", "sapo": "frog", "abelha": "bee", "macaco": "monkey",
}
NUMBER_WORDS = {1: "UM", 2: "DOIS", 3: "TRÊS", 4: "QUATRO", 5: "CINCO", 6: "SEIS", 7: "SETE", 8: "OITO",
                9: "NOVE", 10: "DEZ"}


def lines() -> list[dict]:
    """Every sung line with its absolute start bar, section and visual cue."""
    out: list[dict] = []

    def add(line, bar, section, kind, **extra):
        out.append({**line, "bar": bar, "section": section, "kind": kind, **extra})

    add(INTRO_LINE, 2, "intro", "intro")
    for sec, verse_no in (("chorus1", None), ("verse1", 1), ("chorus2", None), ("verse2", 2), ("chorus3", None)):
        start = next(s for s in SECTIONS if s[0] == sec)[2]
        if verse_no is None:
            for i, c in enumerate(CHORUS):
                add(c, start + 2 * i, sec, "chorus", chorus_line=i)
        else:
            verse = VERSE1 if verse_no == 1 else VERSE2
            for i, (n, numeral, animal, akey, sounds, faz) in enumerate(verse):
                vl = verse_line(n, numeral, animal, sounds, faz, "A" if i % 2 == 0 else "B")
                add(vl, start + 2 * i, sec, "number", number=n, animal=ANIMAL_ICON[akey],
                    number_word=NUMBER_WORDS[n], sound=sounds[0].strip(",!").upper())
            tag = {**TAGS[verse_no], "melody": TAG_MELODY}
            add(tag, start + 10, sec, "tag", total=5 * verse_no)
    add(OUTRO_LINE, 52, "outro", "outro")
    return out


def duration_seconds() -> float:
    return TOTAL_BARS * BAR + TAIL_SECONDS


if __name__ == "__main__":
    for ln in lines():
        print(f"bar {ln['bar']:>2}  {ln['section']:<8} {ln['text']}")
    print(f"{len(lines())} lines, {duration_seconds():.1f} s at {BPM} BPM")
