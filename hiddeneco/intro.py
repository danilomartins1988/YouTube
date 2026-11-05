"""The channel's permanent 5-second intro: sonic signature + automatic placement after the opening hook.

Structure of every episode (default from 2026-11-05): opening hook -> channel intro -> documentary -> conclusion.

* `signature()` synthesises the original 5-second sonic identity (no samples, no paid APIs): a cinematic rise,
  soft electronic plucks, an impact on the title reveal (3.0 s), a three-note gold-bell motif and a resolving pad.
* `insert_intro()` adds one `channel_intro` scene (Remotion: remotion/src/brand/TheHiddenEconomicsIntro.tsx) at the
  first segment boundary after ~10 s of narration (the natural end of the hook), never before the hook, never inside
  a sentence (scenes always end on segment boundaries) and never twice.

Per-project configuration (project.yaml):

    intro:
      enabled: true          # default; set false to leave the intro out
      after_segment: open_x  # optional: place it after this segment instead of the automatic choice
      min_seconds: 10        # automatic choice: first boundary at or after this much opening
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

from hiddeneco.audio import RATE, _env, _lowpass
from hiddeneco.models import Scene, Script, Segment, Storyboard

INTRO_SECONDS = 5.0
INTRO_SEGMENT = "channel_intro"
SIGNATURE_WAV = Path(__file__).resolve().parents[1] / "assets" / "brand" / "intro_signature.wav"


def _bell(freq: float, n: int, rate: int, decay: float = 2.6) -> np.ndarray:
    """Inharmonic additive bell (warm 'gold' timbre)."""
    t = np.arange(n) / rate
    y = np.zeros(n)
    for ratio, amp, dk in ((1.0, 1.0, 1.0), (2.0, 0.42, 1.6), (2.76, 0.26, 2.2), (4.07, 0.14, 3.0), (0.5, 0.22, 0.7)):
        y += amp * np.sin(2 * np.pi * freq * ratio * t) * np.exp(-t * decay * dk)
    att = np.clip(t / 0.004, 0, 1)
    return y * att


def signature(rate: int = RATE) -> np.ndarray:
    """Original 5-second sonic identity, mono float32 peaking at -1 dBFS."""
    n = int(INTRO_SECONDS * rate)
    t = np.arange(n) / rate
    rng = np.random.default_rng(1505)
    out = np.zeros(n)
    # 1. cinematic rise (0 -> 2.95 s): filtered noise swell + gliding sub/octave tones
    rise_n = int(2.95 * rate)
    tr = t[:rise_n] / 2.95
    noise = rng.normal(0, 1, rise_n)
    cut = 160 + 3800 * tr ** 2.2
    swell = _lowpass(_lowpass(noise, cut, rate), cut, rate) * (tr ** 2.4) * 0.9
    f = 55 * 2 ** (tr * 1.0)
    tone = (np.sin(2 * np.pi * np.cumsum(f) / rate) * 0.5 + np.sin(2 * np.pi * np.cumsum(f * 2.003) / rate) * 0.22) * tr ** 1.6
    out[:rise_n] += swell + tone * 0.6
    # 2. soft electronic texture: accelerating plucks (A minor arpeggio) 0.5 -> 2.9 s, with a short echo
    notes = [220.0, 261.63, 329.63, 440.0, 329.63, 261.63]
    tt, k = 0.5, 0
    while tt < 2.88:
        m = int(0.22 * rate)
        s = int(tt * rate)
        q = np.arange(m) / rate
        pl = np.sin(2 * np.pi * notes[k % len(notes)] * 2 * q) * np.exp(-q * 22) + 0.3 * np.sin(2 * np.pi * notes[k % len(notes)] * 4 * q) * np.exp(-q * 30)
        amp = 0.12 + 0.12 * (tt - 0.5) / 2.4
        e = min(n, s + m)
        out[s:e] += pl[: e - s] * amp
        d = s + int(0.11 * rate)
        e2 = min(n, d + m)
        out[d:e2] += pl[: e2 - d] * amp * 0.35
        tt += 0.24 - 0.13 * (tt - 0.5) / 2.4          # gaps shrink: the texture accelerates into the hit
        k += 1
    # 3. impact on the title reveal (3.0 s): pitched sub boom + soft transient + air
    s = int(3.0 * rate)
    m = n - s
    q = np.arange(m) / rate
    boom = np.sin(2 * np.pi * (42 + 70 * np.exp(-q * 14)) * q) * np.exp(-q * 2.6)
    trans = _lowpass(rng.normal(0, 1, m), 3200, rate) * np.exp(-q * 40) * 0.5
    out[s:] += (boom * 0.95 + trans)
    # reverse-swell lead-in (2.75 -> 3.0 s)
    a0, a1 = int(2.75 * rate), s
    r = np.linspace(0, 1, a1 - a0)
    out[a0:a1] += _lowpass(_lowpass(rng.normal(0, 1, a1 - a0), 4200, rate), 4200, rate) * r ** 3 * 0.45
    # 4. musical signature: three gold-bell notes (A5, E6, D6) and a resolving A-major pad
    for at, fr, g in ((3.04, 880.0, 0.42), (3.32, 1318.5, 0.36), (3.6, 1174.7, 0.40)):
        s2 = int(at * rate)
        b = _bell(fr, n - s2, rate)
        out[s2:] += b * g
    pad_s = int(3.0 * rate)
    pq = np.arange(n - pad_s) / rate
    pad = np.zeros(n - pad_s)
    for fr in (220.0, 277.18, 329.63, 440.0):
        for det in (1.0, 1.004, 0.996):
            pad += np.sin(2 * np.pi * fr * det * pq)
    pad *= _env(n - pad_s, 0.35, 1.3, rate) * 0.045
    out[pad_s:] += pad
    # gentle fade so it hands off cleanly
    out *= _env(n, 0.02, 0.45, rate)
    out /= np.max(np.abs(out)) + 1e-9
    out *= 10 ** (-1 / 20)
    return out.astype(np.float32)


def ensure_signature(path: Path = SIGNATURE_WAV) -> Path:
    if not path.exists():
        from hiddeneco.audio import write_wav
        path.parent.mkdir(parents=True, exist_ok=True)
        write_wav(path, signature(), RATE)
    return path


def _estimated_seconds(seg: Segment, render, lead: float, tail: float) -> float:
    text = render(seg.narration)
    return (lead + len(text) / 14.5 + tail) if text else 3.0


def insert_intro(project: dict, sc: Script, sb: Storyboard, render, lead: float = 0.6, tail: float = 0.6) -> tuple[Script, Storyboard, str | None]:
    """Return (script, storyboard, segment the intro follows) with the intro inserted, or unchanged if disabled/present."""
    cfg = project.get("intro", {}) or {}
    if cfg is False or cfg.get("enabled", True) is False:
        return sc, sb, None
    if project.get("renderer") != "remotion":     # the intro is a Remotion component; the FFmpeg renderer cannot draw it
        return sc, sb, None
    if any(s.type == "channel_intro" for s in sb.scenes) or any(s.id == INTRO_SEGMENT for s in sc.segments):
        return sc, sb, None                       # never duplicate
    order = [s.segment for s in sb.scenes]
    by_id = {s.id: s for s in sc.segments}
    after = cfg.get("after_segment")
    if not after:
        acc = 0.0
        for seg_id in order:
            acc += _estimated_seconds(by_id[seg_id], render, lead, tail)
            if acc >= float(cfg.get("min_seconds", 10)) and by_id[seg_id].narration.strip():
                after = seg_id
                break
        after = after or order[0]
    if after not in order:
        raise ValueError(f"intro.after_segment '{after}' is not a storyboard segment")
    seg = Segment(id=INTRO_SEGMENT, chapter=by_id[after].chapter, narration="", claims=[])
    scene = Scene(id="intro", segment=INTRO_SEGMENT, type="channel_intro",
                  params={"min_seconds": INTRO_SECONDS, "no_chrome": True}, sfx=[{"kind": "intro", "at": 0.0, "gain": 0.85}],
                  sources=[], assets=["audio:intro_signature", "font:inter"], note="Channel intro (5 s)")
    segs = list(sc.segments)
    segs.insert([s.id for s in segs].index(after) + 1, seg)
    scenes = list(sb.scenes)
    last = max(i for i, s in enumerate(scenes) if s.segment == after)
    scenes.insert(last + 1, scene)
    return sc.model_copy(update={"segments": segs}), sb.model_copy(update={"scenes": scenes}), after
