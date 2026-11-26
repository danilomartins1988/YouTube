"""Kids test 01, v2: instrumental song + natural narration (owner decision after v1's "spoken-sung" vocal).

The song (melody, chords, chorus lyrics) comes from tools/kids_song.py. The chorus is INSTRUMENTAL (xylophone
melody) with karaoke text on screen for parents to sing along. A warm Brazilian kids-TV narrator talks in the
gaps; speech keeps its natural timing and the arrangement is laid out around the measured clip lengths
(whole bars), with a light "verse bed" and ducking under the voice. Nothing is time-stretched.

Per number:  [question over the bed: "Olha quem chegou: um patinho! Como ele faz?"]  ->  [1 bar: music answers]
             ->  [animal sound, imitated playfully by the narrator, music thinned]  ->  [number reveal "Um!" + ding]

    python tools/kids_v2.py audio     -> output/kids/test01/{music_v2.wav, narration_v2.wav, mix_v2.wav, timeline.json}
                                         + scratchpad MP3 preview
"""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import mido
import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy import signal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import kids_song as S  # noqa: E402
import kids_voice as V  # noqa: E402
from kids_music import CHH, CLAP, KICK, PROGRAMS, SF2, SHAKER, SNARE, SPLASH, TAMB, TPB, TRI  # noqa: E402

WORK = ROOT / "output" / "kids" / "test01"
PREVIEW = Path("/tmp/claude-0/-home-user-YouTube/d850b732-f9ee-5afb-a405-beaa03bb820f/scratchpad/musica_infantil_v2.mp3")
VOICE = "coral"
SR = 44100
BEAT, BAR = S.BEAT, S.BAR
LEAD, UKE, BASS, GLOCK, PAD, DRUM = 0, 1, 2, 3, 4, 9

NARRATOR = (
    "Você é uma apresentadora de programa infantil brasileiro, conversando com crianças pequenas (2 a 6 anos). "
    "Fale de forma natural, calorosa e entusiasmada, com um sorriso na voz. Ritmo de fala normal e expressivo, "
    "dicção bem clara, sotaque brasileiro natural. NÃO cante e NÃO fale cantando: é uma fala natural de quem "
    "conversa com as crianças, com curiosidade e alegria nas perguntas.")
ANIMAL = (
    "Você é uma apresentadora de programa infantil brasileiro, imitando o som de um bicho para crianças pequenas. "
    "Faça a imitação de forma brincalhona, fofa e expressiva, como numa brincadeira, com sorriso na voz. "
    "Curto e divertido, sotaque brasileiro. Não cante.")
NUMBER = (
    "Você é uma apresentadora de programa infantil brasileiro. Diga o número com alegria e orgulho, "
    "como quem comemora junto com as crianças que acertaram a contagem. Natural, claro, sorrindo. Não cante.")

INTRO = "Oi, criançada! Hoje a gente vai contar os bichinhos. Vamos cantar juntos? Bate palma!"
OUTRO = "Tchau, tchau, bichinhos! Até a próxima!"
# (n, animal key, question, sound imitation, spoken number)
NUMBERS = [
    (1, "duck", "Olha quem chegou: um patinho! Como ele faz?", "Quá, quá, quá!", "Um!"),
    (2, "cat", "Dois gatinhos! E o gatinho, como faz?", "Miau! Miau!", "Dois!"),
    (3, "dog", "Três cachorrinhos! Como eles fazem?", "Au, au, au!", "Três!"),
    (4, "cow", "Olha só: quatro vaquinhas! Como a vaca faz?", "Muuuuu!", "Quatro!"),
    (5, "sheep", "Cinco ovelhinhas! Como elas fazem?", "Mééé! Mééé!", "Cinco!"),
    (6, "chick", "Quem vem lá? Seis pintinhos! Como eles fazem?", "Piu, piu, piu!", "Seis!"),
    (7, "pig", "Sete porquinhos! Como o porquinho faz?", "Oinc, oinc!", "Sete!"),
    (8, "frog", "Oito sapinhos no lago! Como o sapo faz?", "Croac, croac!", "Oito!"),
    (9, "bee", "Nove abelhinhas! Como a abelha faz?", "Zum, zum, zum!", "Nove!"),
    (10, "monkey", "E agora... dez macaquinhos! Como eles fazem?", "Uh, uh, ah, ah!", "Dez!"),
]
TAGS = {5: "Cinco amigos! Que legal!", 10: "Dez amigos no quintal! Muito bem!"}
NUMBER_WORDS = S.NUMBER_WORDS


# ---------------------------------------------------------------------------------------------- narration clips
def clip(text: str, style: str) -> tuple[np.ndarray, float]:
    """Trimmed mono clip + its speech length in seconds (natural timing, untouched)."""
    path = V.tts(text, VOICE, style)
    x = V.load_mono(path)
    s0, s1 = V.speech_bounds(x, -42)
    a, b = max(0, int((s0 - 0.03) * SR)), min(len(x), int((s1 + 0.12) * SR))
    y = x[a:b].copy()
    f = int(0.01 * SR)
    y[:f] *= np.linspace(0, 1, f)
    y[-f * 4:] *= np.linspace(1, 0, f * 4)
    return y, len(y) / SR


def bars_for(seconds: float, pad: float = 0.45, minimum: int = 1) -> int:
    return max(minimum, math.ceil((seconds + pad) / BAR))


def words_timed(text: str, start: float, dur: float) -> list[dict]:
    """Subtitle word timing for natural speech: syllable-proportional with pauses at punctuation."""
    ws = text.split()
    wt = [S._syllables(w) + (1.2 if w[-1] in ",.!?:" else 0) + (1.5 if w.endswith("...") else 0) for w in ws]
    tot = sum(wt)
    out, acc = [], 0.0
    for w, k in zip(ws, wt):
        s = start + dur * acc / tot
        acc += k
        out.append({"w": w, "s": round(s, 3), "e": round(start + dur * (acc - (1.0 if w[-1] in ",.!?:" else 0)) / tot, 3)})
    return out


# ---------------------------------------------------------------------------------------------- layout
def layout() -> dict:
    """Decide every segment's bars from the measured narration, and where each clip sits."""
    segs: list[dict] = []
    bar = 0
    voice: list[tuple[float, np.ndarray]] = []
    lines: list[dict] = []

    def speak(text, style, at, kind, **extra):
        y, d = clip(text, style)
        voice.append((at, y))
        ln = {"text": text, "kind": kind, "start": round(at, 3), "end": round(at + d, 3),
              "words": words_timed(text, at + 0.03, d - 0.15), "claps": [], "speaker": "narrator", **extra}
        lines.append(ln)
        return d

    # intro: 1 bar of xylophone hook, then the narrator over the bed, ending into the chorus
    _, d = clip(INTRO, NARRATOR)
    nb = 1 + bars_for(d, 0.35)
    segs.append({"name": "intro", "kind": "intro", "bar": bar, "bars": nb})
    speak(INTRO, NARRATOR, (bar + 1) * BAR + 0.1, "intro", section="intro")
    bar += nb

    def chorus(name, which):
        nonlocal bar
        nb = 2 * len(which)
        segs.append({"name": name, "kind": "chorus", "bar": bar, "bars": nb, "lines": which})
        for k, ci in enumerate(which):
            c = S.CHORUS[ci]
            t0 = (bar + 2 * k) * BAR
            beats = [b for _, b in c["words"]] + [7.5]
            words = [{"w": w, "s": round(t0 + b * BEAT, 3), "e": round(t0 + min(beats[i + 1], b + 2) * BEAT - 0.04, 3)}
                     for i, (w, b) in enumerate(c["words"])]
            lines.append({"text": c["text"], "kind": "chorus", "chorus_line": ci, "start": round(t0, 3),
                          "end": round(t0 + 8 * BEAT, 3), "words": words, "speaker": "karaoke", "section": name,
                          "claps": [round(t0 + x * BEAT, 3) for x in c.get("claps", [])]})
        bar += nb

    def verse(name, nums):
        nonlocal bar
        start = bar
        for n, animal, q, snd, num in nums:
            _, dq = clip(q, NARRATOR)
            _, ds = clip(snd, ANIMAL)
            _, dn = clip(num, NUMBER)
            qb = bars_for(dq, 0.3, 2)
            sb = bars_for(ds, 0.5)
            u0 = bar
            q_at = u0 * BAR + 0.12
            ans = (u0 + qb) * BAR                      # 1 bar: the music "answers" the question
            s_at = (u0 + qb + 1) * BAR + 0.05          # animal sound (music thinned)
            r_bar = u0 + qb + 1 + sb                   # number reveal bar
            r_at = r_bar * BAR + 0.08
            unit = {"name": f"n{n}", "kind": "number", "bar": u0, "bars": qb + 1 + sb + 1, "q_bars": qb, "s_bars": sb,
                    "number": n}
            segs.append(unit)
            common = {"section": name, "number": n, "animal": animal, "number_word": NUMBER_WORDS[n]}
            speak(q, NARRATOR, q_at, "number", **common, phase="question", answer_at=round(ans, 3),
                  sound_at=round(s_at, 3), reveal_at=round(r_at, 3), unit_end=round((r_bar + 1) * BAR, 3),
                  sound=snd)
            speak(snd, ANIMAL, s_at, "sound", **common, phase="sound")
            speak(num, NUMBER, r_at, "reveal", **common, phase="reveal")
            bar = r_bar + 1
            if n in TAGS:
                _, dt = clip(TAGS[n], NARRATOR)
                tb = bars_for(dt, 0.3, 2)
                segs.append({"name": f"tag{n}", "kind": "tag", "bar": bar, "bars": tb})
                speak(TAGS[n], NARRATOR, bar * BAR + 0.1, "tag", section=name, total=n)
                bar += tb
        segs.append({"name": name, "kind": "verse_section", "bar": start, "bars": bar - start})

    chorus("chorus1", [0, 1, 2, 3])
    verse("verse1", NUMBERS[:5])
    chorus("chorus2", [0, 3])
    verse("verse2", NUMBERS[5:])
    chorus("chorus3", [0, 1, 2, 3])
    _, d = clip(OUTRO, NARRATOR)
    nb = bars_for(d, 0.4, 2) + 1
    segs.append({"name": "outro", "kind": "outro", "bar": bar, "bars": nb})
    speak(OUTRO, NARRATOR, bar * BAR + 0.1, "outro", section="outro")
    bar += nb
    return {"segs": segs, "total_bars": bar, "voice": voice, "lines": sorted(lines, key=lambda l: l["start"])}


# ---------------------------------------------------------------------------------------------- arrangement
def chords_for(seg: dict) -> list[str]:
    k = seg["kind"]
    if k == "intro":
        return (["C", "F", "C", "F", "G"] * 3)[: seg["bars"] - 1] + ["G"]
    if k == "chorus":
        prog = {0: ["C", "C"], 1: ["F", "G"], 2: ["C", "F"], 3: ["G", "C"]}
        return sum((prog[i] for i in seg["lines"]), [])
    if k == "number":
        q = (["C", "F"] * 4)[: seg["q_bars"]]
        return q + ["G"] + ["Am", "G", "F"][: seg["s_bars"] - 1][::-1] + (["G"] if seg["s_bars"] > 1 else []) + ["C"] \
            if seg["s_bars"] > 1 else q + ["G", "G", "C"]
    if k == "tag":
        return (["F"] * (seg["bars"] - 1)) + ["G"]
    if k == "outro":
        return (["C", "F", "G", "C"] * 3)[: seg["bars"] - 1] + ["C"]
    return []


def build_events(L: dict) -> list[tuple]:
    ev: list[tuple] = []

    def note(beat, length, ch, pitch, vel):
        ev.append((beat, "on", ch, pitch, vel))
        ev.append((beat + max(0.05, length), "off", ch, pitch, 0))

    total = L["total_bars"]
    for seg in L["segs"]:
        if seg["kind"] == "verse_section":
            continue
        chords = chords_for(seg)
        assert len(chords) == seg["bars"], (seg, chords)
        for k, ch in enumerate(chords):
            bar = seg["bar"] + k
            b0 = bar * 4
            root, triad = S.CHORDS[ch]
            last = bar == total - 1
            voicing = sorted([p + 7 if i == 0 else p for i, p in enumerate(sorted(triad))]) + [sorted(triad)[0] + 12]
            kind = seg["kind"]
            role = kind
            if kind == "number":
                qb, sb = seg["q_bars"], seg["s_bars"]
                role = "bed" if k < qb else "answer" if k == qb else "sound" if k < qb + 1 + sb else "reveal"
            if kind in ("intro", "tag", "outro") and not (kind == "intro" and k == 0) and not last:
                role = "bed"
            if kind == "intro" and k == 0:
                role = "hook"
            if last:
                role = "end"
            strum = lambda pat, scale=1.0: [  # noqa: E731
                [note(b0 + pos + i * 0.025, 0.45, UKE, p, int((v - 4 * i) * scale))
                 for i, p in enumerate(voicing if d == "D" else voicing[::-1])] for pos, d, v in pat]
            if role in ("chorus", "hook", "answer", "reveal"):
                note(b0, 0.9, BASS, root, 92)
                note(b0 + 1.5, 0.4, BASS, root + 12, 60)
                note(b0 + 2, 0.9, BASS, root + 7, 84)
                strum([(0, "D", 84), (1, "D", 70), (1.5, "U", 58), (2.5, "U", 60), (3, "D", 72), (3.5, "U", 56)])
                for beat in (0, 2):
                    note(b0 + beat, 0.2, DRUM, KICK, 86)
                for beat in (1, 3):
                    note(b0 + beat, 0.2, DRUM, SNARE, 60)
                for e in range(8):
                    note(b0 + e * 0.5, 0.1, DRUM, CHH, 46 if e % 2 else 58)
                    note(b0 + e * 0.5 + 0.25, 0.1, DRUM, SHAKER, 32)
                if role == "chorus":
                    for beat in (1, 3):
                        note(b0 + beat, 0.2, DRUM, TAMB, 50)
                    for p in triad:
                        note(b0, 3.9, PAD, p - 12, 34)
            elif role == "bed":
                # light verse bed under speech: soft bass on 1 and 3, gentle strums, shaker; no snare/hats
                note(b0, 1.8, BASS, root, 70)
                note(b0 + 2, 1.8, BASS, root + 7, 60)
                strum([(0, "D", 62), (2, "D", 54), (3, "U", 44)])
                for p in triad:
                    note(b0, 3.9, PAD, p - 12, 30)
                for e in range(4):
                    note(b0 + e, 0.1, DRUM, SHAKER, 30)
                note(b0, 0.2, DRUM, KICK, 50)
            elif role == "sound":
                # music steps back for the animal sound: a held chord and a tiny tiptoe on the glockenspiel
                note(b0, 3.8, BASS, root, 56)
                for p in triad:
                    note(b0, 3.9, PAD, p - 12, 32)
                note(b0 + 3, 0.3, DRUM, TRI, 34)
            elif role == "end":
                note(b0, 6, BASS, root, 90)
                for i, p in enumerate(voicing):
                    note(b0 + i * 0.03, 6, UKE, p, 80)
                note(b0, 1, DRUM, KICK, 80)
                note(b0, 2, DRUM, SPLASH, 50)
            # melodic material
            if role == "answer":
                # the xylophone "answers" the question with a playful rising call ending on the dominant
                for j, (bt, ln, p) in enumerate([(0, .5, 67), (.5, .5, 69), (1, .5, 71), (1.5, .5, 74), (2, 1, 79), (3, .5, 74), (3.5, .5, 71)]):
                    note(b0 + bt, ln, LEAD, p + 12 - 12, 88)
            if role == "reveal":
                n = seg["number"]
                scale = [84, 86, 88, 89, 91, 93, 95, 96, 98, 100]
                note(b0, 2, GLOCK, scale[n - 1], 90)
                for j, p in enumerate([72, 76, 79, 84]):
                    note(b0 + 2 + j * 0.25, 0.4, LEAD, p, 84)
                note(b0, 1.5, DRUM, SPLASH, 40)
        if seg["kind"] == "chorus":
            for k, ci in enumerate(seg["lines"]):
                lb = (seg["bar"] + 2 * k) * 4
                c = S.CHORUS[ci]
                for bt, ln, p in c["melody"]:
                    note(lb + bt, ln, LEAD, p + 12, 100)
                    note(lb + bt, ln * 0.9, GLOCK, p + 24, 40)  # sparkle doubling
                for x in c.get("claps", []):
                    note(lb + x, 0.2, DRUM, CLAP, 96)
            note(seg["bar"] * 4, 1.5, DRUM, SPLASH, 46)
        if seg["kind"] == "intro":
            for bt, ln, p in S.CHORUS[0]["melody"]:
                if bt < 4:
                    note(bt, ln, LEAD, p + 12, 96)
            note(0.0 + 4 - 0.0, 0.0, LEAD, 0, 0) if False else None
        if seg["kind"] == "tag":
            b0 = (seg["bar"] + seg["bars"] - 1) * 4
            for j, p in enumerate([67, 69, 71, 74]):
                note(b0 + 2 + j * 0.5, 0.45, LEAD, p + 12, 84)
        if seg["kind"] == "outro":
            b0 = (seg["bar"] + seg["bars"] - 2) * 4
            for bt, ln, p in S.CHORUS[3]["melody"]:
                if b0 + bt < (seg["bar"] + seg["bars"]) * 4 - 4:
                    note(b0 - 4 + bt, ln, LEAD, p + 12, 80) if seg["bars"] > 2 else None
    return [e for e in ev if e[3] > 0]


def render_music(L: dict) -> Path:
    mid = mido.MidiFile(ticks_per_beat=TPB)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(S.BPM), time=0))
    for ch, prog in PROGRAMS.items():
        tr.append(mido.Message("program_change", channel=ch, program=prog, time=0))
    mixcc = {LEAD: (98, 70, 40, 0), UKE: (86, 50, 30, 20), BASS: (102, 64, 10, 0), GLOCK: (80, 84, 60, 0),
             PAD: (56, 64, 70, 30), DRUM: (90, 64, 25, 0)}
    for ch, (vol, pan, rev, cho) in mixcc.items():
        for cc, val in ((7, vol), (10, pan), (91, rev), (93, cho)):
            tr.append(mido.Message("control_change", channel=ch, control=cc, value=val, time=0))
    last = 0
    for beat, kind, ch, pitch, vel in sorted(build_events(L), key=lambda e: (e[0], 0 if e[1] == "off" else 1)):
        tick = int(round(beat * TPB))
        tr.append(mido.Message("note_on" if kind == "on" else "note_off", channel=ch, note=pitch, velocity=vel,
                               time=tick - last))
        last = tick
    tr.append(mido.MetaMessage("end_of_track", time=TPB * 4))
    midi = WORK / "song_v2.mid"
    mid.save(midi)
    raw = WORK / "music_v2_raw.wav"
    subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.5", "-r", str(SR), "-F", str(raw), SF2, str(midi)],
                   check=True, capture_output=True)
    x, _ = sf.read(raw)
    raw.unlink()
    n = int(duration(L) * SR)
    x = x[:n] if len(x) >= n else np.pad(x, ((0, n - len(x)), (0, 0)))
    fade = int(1.2 * SR)
    x[-fade:] *= (np.linspace(1, 0, fade) ** 2)[:, None]
    out = WORK / "music_v2.wav"
    sf.write(out, x.astype(np.float32), SR)
    return out


def duration(L: dict) -> float:
    return L["total_bars"] * BAR + S.TAIL_SECONDS


# ---------------------------------------------------------------------------------------------- mix
def narration_track(L: dict) -> np.ndarray:
    v = np.zeros(int(duration(L) * SR), dtype=np.float64)
    for at, y in L["voice"]:
        a = int(at * SR)
        b = min(len(v), a + len(y))
        v[a:b] += y[: b - a]
    return v


def voice_fx(v: np.ndarray) -> np.ndarray:
    b, a = signal.butter(2, 90 / (SR / 2), "highpass")
    v = signal.lfilter(b, a, v)
    env = np.sqrt(signal.lfilter([0.002], [1, -0.998], v ** 2) + 1e-10)
    ref = np.percentile(env[env > 1e-4], 95)
    over = np.maximum(0, 20 * np.log10(env / ref + 1e-9) + 10)
    v = v * 10 ** (-(over * (1 - 1 / 2.5)) / 20)
    # small, dry-ish room so it sits with the music (narration, not a vocal effect)
    rng = np.random.default_rng(3)
    n = int(0.5 * SR)
    ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 11)
    ir[: int(0.008 * SR)] = 0
    ir /= np.sqrt((ir ** 2).sum())
    wet = signal.fftconvolve(v, ir)[: len(v)]
    v = v + 0.05 * wet / (np.abs(wet).max() + 1e-9) * np.abs(v).max()
    return np.stack([v, v], axis=1)


def duck(v: np.ndarray, depth_db: float = 9.0) -> np.ndarray:
    hop = int(0.01 * SR)
    fr = np.abs(v[: len(v) // hop * hop]).reshape(-1, hop).max(axis=1)
    on = (fr > 0.02 * fr.max()).astype(float)
    # hold through short gaps between words, smooth attack 60 ms / release 400 ms
    held = np.convolve(on, np.ones(35), mode="same") > 0
    g = np.zeros(len(held))
    e = 0.0
    for i, h in enumerate(held):
        tgt = 1.0 if h else 0.0
        e += (tgt - e) * (0.17 if tgt > e else 0.025)
        g[i] = e
    g = np.interp(np.arange(len(v)), np.arange(len(g)) * hop, g)
    return 10 ** (-depth_db * g / 20)


def mix(L: dict) -> dict:
    music, _ = sf.read(WORK / "music_v2.wav", dtype="float64")
    v = narration_track(L)
    sf.write(WORK / "narration_v2.wav", v.astype(np.float32), SR)
    v2 = voice_fx(v)
    g = duck(v)
    meter = pyln.Meter(SR)
    m = music * g[:, None]
    # voice level: ~ +6 LU over the (ducked) music while speaking
    speech_mask = g < 0.6
    lv = meter.integrated_loudness(v2[speech_mask]) if speech_mask.sum() > SR else meter.integrated_loudness(v2)
    lm = meter.integrated_loudness(m[speech_mask])
    v2 *= 10 ** ((lm + 7.0 - lv) / 20)
    out = v2 + m
    out *= 10 ** ((-16.0 - meter.integrated_loudness(out)) / 20)
    tmp = WORK / "mix_v2_pre.wav"
    sf.write(tmp, out.astype(np.float32), SR, subtype="FLOAT")
    final = WORK / "mix_v2.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-af",
                    "alimiter=limit=0.80:attack=3:release=60:level=disabled,aresample=48000", "-c:a", "pcm_s16le",
                    str(final)], check=True)
    tmp.unlink()
    y, sr = sf.read(final)
    w = int(0.1 * sr)
    rms = np.sqrt((y[: len(y) // w * w].mean(axis=1).reshape(-1, w) ** 2).mean(axis=1))
    quiet = 20 * np.log10(rms + 1e-9) < -45
    best = run = 0
    for q in quiet[:-30]:
        run = run + 1 if q else 0
        best = max(best, run)
    stats = {"lufs": round(float(pyln.Meter(sr).integrated_loudness(y)), 2),
             "peak_dbfs": round(float(20 * np.log10(np.abs(y).max())), 2), "seconds": round(len(y) / sr, 2),
             "clipped_samples": int((np.abs(y) >= 0.999).sum()), "longest_silence_s": round(best * 0.1, 2)}
    PREVIEW.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(final), "-c:a", "libmp3lame", "-b:a", "160k",
                    str(PREVIEW)], check=True)
    return stats


def write_timeline(L: dict) -> None:
    secs = []
    for s in L["segs"]:
        if s["kind"] in ("intro", "chorus", "outro", "verse_section"):
            secs.append({"name": s["name"], "kind": "verse" if s["kind"] == "verse_section" else s["kind"],
                         "start": round(s["bar"] * BAR, 3), "end": round((s["bar"] + s["bars"]) * BAR, 3)})
    secs.sort(key=lambda s: s["start"])
    tl = {"title": S.TITLE, "version": 2, "format": "instrumental song + natural narration", "bpm": S.BPM,
          "beat": BEAT, "bar": BAR, "duration": round(duration(L), 3), "voice": VOICE, "sections": secs,
          "segments": [{k: v for k, v in s.items()} for s in L["segs"] if s["kind"] != "verse_section"],
          "lines": L["lines"]}
    (WORK / "timeline.json").write_text(json.dumps(tl, ensure_ascii=False, indent=1))


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    L = layout()
    render_music(L)
    stats = mix(L)
    write_timeline(L)
    (WORK / "mix_v2_stats.json").write_text(json.dumps(stats))
    print("structure:")
    for s in L["segs"]:
        if s["kind"] != "verse_section":
            print(f"  bar {s['bar']:>3} {s['name']:<8} {s['bars']} bars")
    print(stats, f"total TTS/ASR spend ${V._costs()['total_usd']:.4f}")
    print(PREVIEW)


if __name__ == "__main__":
    main()
