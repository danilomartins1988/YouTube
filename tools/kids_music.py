"""Kids test 01: build the instrumental from tools/kids_song.py.

MIDI (mido) -> FluidSynth + FluidR3 GM soundfont -> output/kids/test01/music.wav (44.1 kHz stereo).
Arrangement: xylophone lead (melody, octave up), nylon guitar strummed like a ukulele (high voicing),
acoustic bass (root/fifth bounce), light kit (kick, snare, closed hat, shaker, tambourine), claps,
glockenspiel "ding" on every number reveal.

    python tools/kids_music.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import mido

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kids_song as S  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "output" / "kids" / "test01"
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
TPB = 480  # ticks per beat

# channels / GM programs
LEAD, UKE, BASS, GLOCK, PAD = 0, 1, 2, 3, 4
DRUM = 9
PROGRAMS = {LEAD: 13, UKE: 24, BASS: 32, GLOCK: 9, PAD: 89}  # xylophone, nylon gtr, acoustic bass, glock, warm pad
KICK, SNARE, CHH, SHAKER, TAMB, CLAP, SPLASH, TRI = 36, 38, 42, 70, 54, 39, 55, 81


def build_events() -> list[tuple[float, str, int, int, int]]:
    """(beat_time, 'on'/'off', channel, note, velocity)."""
    ev: list[tuple[float, str, int, int, int]] = []

    def note(beat, length, ch, pitch, vel):
        ev.append((beat, "on", ch, pitch, vel))
        ev.append((beat + max(0.05, length), "off", ch, pitch, 0))

    def section_kind(bar):
        for name, kind, start, n in S.SECTIONS:
            if start <= bar < start + n:
                return kind
        return "outro"

    total = S.TOTAL_BARS
    for bar in range(total):
        b0 = bar * 4
        chord = S.CHORD_BARS[bar]
        root, triad = S.CHORDS[chord]
        kind = section_kind(bar)
        last = bar == total - 1
        # ---------------- bass: root on 1, fifth on 3, pickup eighth before next bar
        if last:
            note(b0, 6, BASS, root, 90)
        else:
            note(b0, 0.9, BASS, root, 92)
            note(b0 + 1.5, 0.4, BASS, root + 12, 62)
            note(b0 + 2, 0.9, BASS, root + 7, 84)
            nxt = S.CHORDS[S.CHORD_BARS[bar + 1]][0]
            note(b0 + 3.5, 0.4, BASS, nxt + (2 if nxt < root else -1) if nxt != root else root + 7, 66)
        # ---------------- "ukulele" strum: D . D U . U D U on eighths, high voicing
        voicing = [p + 7 if i == 0 else p for i, p in enumerate(sorted(triad))]  # tighter, brighter
        voicing = sorted(voicing) + [sorted(triad)[0] + 12]
        if last:
            for i, p in enumerate(voicing):
                note(b0 + i * 0.03, 6, UKE, p, 80)
        else:
            pattern = [(0, "D", 84), (1, "D", 70), (1.5, "U", 58), (2.5, "U", 60), (3, "D", 72), (3.5, "U", 56)]
            if kind == "intro" and bar < 2:
                pattern = [(0, "D", 70), (2, "D", 62)]
            for pos, d, v in pattern:
                order = voicing if d == "D" else list(reversed(voicing))
                for i, p in enumerate(order):
                    note(b0 + pos + i * 0.025, 0.45, UKE, p, v - 4 * i)
        # ---------------- soft pad under choruses for warmth
        if kind == "chorus":
            for p in triad:
                note(b0, 3.9, PAD, p - 12, 34)
        # ---------------- drums
        full = not (kind == "intro" and bar < 2) and not last
        if full:
            for beat in (0, 2):
                note(b0 + beat, 0.2, DRUM, KICK, 88)
            if kind == "chorus":
                note(b0 + 2.5, 0.2, DRUM, KICK, 60)
            for beat in (1, 3):
                note(b0 + beat, 0.2, DRUM, SNARE, 62)
            for e in range(8):
                note(b0 + e * 0.5, 0.1, DRUM, CHH, 46 if e % 2 else 58)
            for e in range(8):
                note(b0 + e * 0.5 + 0.25, 0.1, DRUM, SHAKER, 34)
            if kind == "chorus":
                for beat in (1, 3):
                    note(b0 + beat, 0.2, DRUM, TAMB, 50)
        elif not last:
            for e in range(8):
                note(b0 + e * 0.5, 0.1, DRUM, SHAKER, 40 if e % 2 else 52)
        if last:
            note(b0, 1, DRUM, KICK, 80)
            note(b0, 2, DRUM, SPLASH, 54)
        # gentle splash to mark each new section (not on the very first bar)
        for name, k, start, n in S.SECTIONS:
            if start == bar and bar > 0 and not last:
                note(b0, 1.5, DRUM, SPLASH, 46)

    # ---------------- lead melody (xylophone, octave up) + claps + number dings
    for ln in S.lines():
        lb = ln["bar"] * 4
        vel = 78 if ln["kind"] in ("chorus", "tag", "outro") else 70
        for beat, length, pitch in ln.get("melody", []):
            note(lb + beat, length, LEAD, pitch + 12, vel)
        for c in ln.get("claps", []):
            note(lb + c, 0.2, DRUM, CLAP, 96)
        if ln["kind"] == "number":
            # ascending glockenspiel "ding" as the number pops in (C major scale from C6)
            scale = [84, 86, 88, 89, 91, 93, 95, 96, 98, 100]
            note(lb - 0.0, 1.5, GLOCK, scale[ln["number"] - 1], 74)
            note(lb + 6.5, 0.3, DRUM, TRI, 40)
    # intro hook: the chorus melody played on the xylophone over bars 0-1
    for beat, length, pitch in S.CHORUS[0]["melody"]:
        note(beat, length, LEAD, pitch + 12, 92)
    # instrumental fill on outro bar 54-55: hook again, then home
    for beat, length, pitch in S.CHORUS[3]["melody"]:
        note(54 * 4 + beat, length, LEAD, pitch + 12, 84)
    return ev


def write_midi(path: Path) -> Path:
    mid = mido.MidiFile(ticks_per_beat=TPB)
    tr = mido.MidiTrack()
    mid.tracks.append(tr)
    tr.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(S.BPM), time=0))
    tr.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    for ch, prog in PROGRAMS.items():
        tr.append(mido.Message("program_change", channel=ch, program=prog, time=0))
    # mix: volume (CC7), pan (CC10), reverb send (CC91), chorus (CC93)
    mixcc = {LEAD: (96, 70, 40, 0), UKE: (88, 50, 30, 20), BASS: (104, 64, 10, 0), GLOCK: (78, 84, 60, 0),
             PAD: (52, 64, 70, 30), DRUM: (92, 64, 25, 0)}
    for ch, (vol, pan, rev, cho) in mixcc.items():
        for cc, val in ((7, vol), (10, pan), (91, rev), (93, cho)):
            tr.append(mido.Message("control_change", channel=ch, control=cc, value=val, time=0))
    ev = sorted(build_events(), key=lambda e: (e[0], 0 if e[1] == "off" else 1))
    last_tick = 0
    for beat, kind, ch, pitch, vel in ev:
        tick = int(round(beat * TPB))
        msg = "note_on" if kind == "on" else "note_off"
        tr.append(mido.Message(msg, channel=ch, note=pitch, velocity=vel, time=tick - last_tick))
        last_tick = tick
    tr.append(mido.MetaMessage("end_of_track", time=int(TPB * 4)))
    mid.save(path)
    return path


def render(midi: Path, wav: Path) -> Path:
    subprocess.run(["fluidsynth", "-ni", "-q", "-g", "0.5", "-r", "44100", "-F", str(wav), SF2, str(midi)],
                   check=True, capture_output=True)
    return wav


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    midi = write_midi(WORK / "song.mid")
    wav = render(midi, WORK / "music_raw.wav")
    import numpy as np
    import soundfile as sf
    x, sr = sf.read(wav)
    n = int(S.duration_seconds() * sr)
    x = x[:n] if len(x) >= n else np.pad(x, ((0, n - len(x)), (0, 0)))
    fade = int(1.2 * sr)
    x[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
    sf.write(WORK / "music.wav", x.astype(np.float32), sr)
    wav.unlink()
    peak = 20 * np.log10(np.abs(x).max() + 1e-9)
    print(f"music.wav {len(x) / sr:.1f}s peak {peak:.1f} dBFS")


if __name__ == "__main__":
    main()
