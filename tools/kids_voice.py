"""Kids test 01: the "spoken-sung" vocal.

1. TTS every unique lyric line with OpenAI gpt-4o-mini-tts (style `instructions`), cached per (voice, text).
2. Word timestamps for each clip from OpenAI whisper-1 (verbose_json, word granularity), cached.
3. Quantise: cut each clip at its word onsets and place every word on its beat in the song grid
   (kids_song.py), time-stretching each word gently with rubberband (ratio clamped), short crossfades.
4. Write vocal.wav (44.1 kHz mono) + timeline.json (actual word times for karaoke + visual cues).

    python tools/kids_voice.py audition            # a few voices on two lines -> output/kids/test01/audition/
    python tools/kids_voice.py build [voice]       # full vocal + timeline

The API key is read from the environment / .env through hiddeneco.config (never printed).
Every paid call is appended to kids/test-01/costs.json.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import requests
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import kids_song as S  # noqa: E402
from hiddeneco.config import env, settings  # noqa: E402

WORK = ROOT / "output" / "kids" / "test01"
CACHE = WORK / "tts_cache"
COSTS = ROOT / "kids" / "test-01" / "costs.json"
SR = 44100
BUDGET_USD = 1.00

TTS_MODEL = "gpt-4o-mini-tts"
INSTRUCTIONS = (
    "Você é uma cantora de músicas infantis brasileira, animada e carinhosa, cantando para crianças de 2 a 6 anos. "
    "Sotaque brasileiro natural, pronúncia bem clara. Fale de forma cantada e melódica, como uma canção de roda: "
    "voz sorridente, alegre e brilhante, com sobe-e-desce na entonação, marcando bem o ritmo de cada sílaba, "
    "como se batesse palmas no tempo. Alongue um pouco as vogais no fim das frases. "
    "Imite os sons dos bichos de um jeito fofo e divertido. Energia alta, mas doce, nunca gritando."
)
# rough public prices: gpt-4o-mini-tts ~ $0.015 per minute of audio (+ $0.60/M input text tokens);
# whisper-1 $0.006 per minute
TTS_PER_MIN, TTS_TEXT_PER_TOKEN, WHISPER_PER_MIN = 0.015, 0.60e-6, 0.006


# ------------------------------------------------------------------ cost log
def _costs() -> dict:
    if COSTS.exists():
        return json.loads(COSTS.read_text())
    return {"budget_usd": BUDGET_USD, "calls": [], "total_usd": 0.0}


def log_cost(kind: str, detail: str, seconds: float, usd: float) -> None:
    c = _costs()
    c["calls"].append({"kind": kind, "detail": detail, "audio_seconds": round(seconds, 2), "usd": round(usd, 5),
                       "at": time.strftime("%Y-%m-%dT%H:%M:%S")})
    c["total_usd"] = round(sum(x["usd"] for x in c["calls"]), 4)
    COSTS.parent.mkdir(parents=True, exist_ok=True)
    COSTS.write_text(json.dumps(c, indent=1, ensure_ascii=False))


def check_budget() -> None:
    if _costs()["total_usd"] >= BUDGET_USD * 0.95:
        raise SystemExit("TTS budget reached; refusing further paid calls")


def _key() -> str:
    settings()  # loads .env
    k = env("OPENAI_API_KEY")
    if not k:
        raise SystemExit("OPENAI_API_KEY not set")
    return k


# ------------------------------------------------------------------ TTS + whisper (cached)
def tts(text: str, voice: str, instructions: str = INSTRUCTIONS) -> Path:
    h = hashlib.sha1(f"{TTS_MODEL}|{voice}|{instructions}|{text}".encode()).hexdigest()[:16]
    out = CACHE / f"{voice}_{h}.wav"
    if out.exists():
        return out
    check_budget()
    CACHE.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            r = requests.post("https://api.openai.com/v1/audio/speech",
                              headers={"Authorization": f"Bearer {_key()}"},
                              json={"model": TTS_MODEL, "voice": voice, "input": text, "response_format": "wav",
                                    "instructions": instructions}, timeout=120)
            r.raise_for_status()
            break
        except requests.RequestException as e:  # noqa: PERF203
            if attempt == 3:
                raise SystemExit(f"TTS failed: {type(e).__name__} {getattr(e.response, 'status_code', '')}")
            time.sleep(2 + 3 * attempt)
    out.write_bytes(r.content)
    x, sr = sf.read(out)
    secs = len(x) / sr
    log_cost("tts", f"{voice}: {text}", secs, secs / 60 * TTS_PER_MIN + (len(instructions) + len(text)) / 4 * TTS_TEXT_PER_TOKEN)
    return out


def words_of(clip: Path, prompt: str) -> list[dict]:
    out = clip.with_suffix(".words.json")
    if out.exists():
        return json.loads(out.read_text())
    check_budget()
    with clip.open("rb") as fh:
        for attempt in range(4):
            try:
                fh.seek(0)
                r = requests.post("https://api.openai.com/v1/audio/transcriptions",
                                  headers={"Authorization": f"Bearer {_key()}"},
                                  files={"file": (clip.name, fh, "audio/wav")},
                                  data={"model": "whisper-1", "language": "pt", "response_format": "verbose_json",
                                        "timestamp_granularities[]": "word", "prompt": prompt}, timeout=120)
                r.raise_for_status()
                break
            except requests.RequestException as e:  # noqa: PERF203
                if attempt == 3:
                    raise SystemExit(f"whisper failed: {type(e).__name__} {getattr(e.response, 'status_code', '')}")
                time.sleep(2 + 3 * attempt)
    data = r.json()
    words = [{"w": w["word"], "s": float(w["start"]), "e": float(w["end"])} for w in data.get("words", [])]
    secs = float(data.get("duration", 0) or 0)
    log_cost("whisper", clip.name, secs, secs / 60 * WHISPER_PER_MIN)
    out.write_text(json.dumps({"text": data.get("text", ""), "words": words}, ensure_ascii=False))
    return json.loads(out.read_text())


# ------------------------------------------------------------------ audio helpers
def load_mono(path: Path) -> np.ndarray:
    x, sr = sf.read(path, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    if sr != SR:
        n = int(round(len(x) * SR / sr))
        x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
    return x


def speech_bounds(x: np.ndarray, thr_db: float = -38) -> tuple[float, float]:
    w = int(0.01 * SR)
    frames = len(x) // w
    rms = np.sqrt((x[: frames * w].reshape(frames, w) ** 2).mean(axis=1) + 1e-12)
    db = 20 * np.log10(rms / (rms.max() + 1e-12))
    on = np.where(db > thr_db)[0]
    if not len(on):
        return 0.0, len(x) / SR
    return on[0] * w / SR, (on[-1] + 1) * w / SR


def stretch(seg: np.ndarray, ratio: float) -> np.ndarray:
    """Time-stretch by `ratio` (>1 = longer) with rubberband, pitch preserved."""
    if abs(ratio - 1) < 0.02 or len(seg) < SR * 0.04:
        return seg
    with tempfile.TemporaryDirectory() as td:
        a, b = Path(td) / "a.wav", Path(td) / "b.wav"
        sf.write(a, seg, SR)
        subprocess.run(["rubberband", "-q", "-3", "-t", f"{ratio:.4f}", str(a), str(b)], check=True,
                       capture_output=True)
        y, _ = sf.read(b, dtype="float32")
    return y if y.ndim == 1 else y.mean(axis=1)


def norm_word(w: str) -> str:
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)


def align(lyric_words: list[str], found: list[dict], clip_len: float) -> list[tuple[float, float]]:
    """Map each lyric word to (start, end) in the clip using whisper words; interpolate the rest."""
    a = [norm_word(w) for w in lyric_words]
    b = [norm_word(w["w"]) for w in found]
    res: list[tuple[float, float] | None] = [None] * len(a)
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            f = found[blk.b + k]
            res[blk.a + k] = (f["s"], f["e"])
    # fuzzy pass for unmatched words (onomatopoeia often transcribed differently): take positional neighbours
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                f = found[j1 + k]
                res[i1 + k] = (f["s"], f["e"])
        elif op == "replace" and j2 > j1:  # spread the found span over the lyric words
            s0, e0 = found[j1]["s"], found[j2 - 1]["e"]
            n = i2 - i1
            for k in range(n):
                res[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
    # interpolate remaining gaps
    for i in range(len(res)):
        if res[i] is None:
            prev_e = next((res[j][1] for j in range(i - 1, -1, -1) if res[j]), 0.0)
            nxt = next(((j, res[j][0]) for j in range(i + 1, len(res)) if res[j]), (len(res), clip_len))
            span = (nxt[1] - prev_e) / max(1, nxt[0] - i)
            res[i] = (prev_e, prev_e + span)
    # monotonic clean-up
    out = []
    t = 0.0
    for s, e in res:
        s = max(s, t)
        e = max(e, s + 0.08)
        out.append((s, e))
        t = s + 0.02
    return out


# ------------------------------------------------------------------ build
def envelope_db(x: np.ndarray) -> np.ndarray:
    """10 ms RMS in dB relative to the clip's loudest frame, lightly smoothed."""
    w = int(0.01 * SR)
    n = len(x) // w
    rms = np.sqrt((x[: n * w].reshape(n, w) ** 2).mean(axis=1) + 1e-12)
    rms = np.convolve(rms, np.ones(3) / 3, mode="same")
    return 20 * np.log10(rms / (rms.max() + 1e-12) + 1e-9)


def pauses(x: np.ndarray, floor_db: float = -30, min_len: float = 0.05) -> list[tuple[float, float]]:
    """Silent runs strictly inside the speech (start, end) in seconds."""
    db = envelope_db(x)
    s0, s1 = speech_bounds(x)
    quiet = db < floor_db
    out, k = [], int(s0 * 100) + 1
    end = int(s1 * 100) - 1
    while k < end:
        if quiet[k]:
            j = k
            while j < end and quiet[j]:
                j += 1
            if (j - k) / 100 >= min_len:
                out.append((k / 100, j / 100))
            k = j
        else:
            k += 1
    return out


def chunks_of(line: dict, x: np.ndarray) -> list[dict]:
    """Split a line into rhythmic chunks at its punctuation. Word-level timestamps from ASR are too loose
    for beat placement (±0.2-0.4 s on this material), but the pause the TTS makes at every comma is
    reliable, so each chunk is cut at a detected pause and placed on the beat of its first word."""
    words = line["words"]
    groups, cur = [], []
    for i, (w, beat) in enumerate(words):
        cur.append(i)
        if re.search(r"[,!?:.;]$", w) and i < len(words) - 1:
            groups.append(cur)
            cur = []
    groups.append(cur)
    s0, s1 = speech_bounds(x)
    ps = pauses(x)
    need = len(groups) - 1
    if len(ps) < need:  # the voice ran some commas together: merge from the end until it fits
        while len(groups) - 1 > len(ps):
            last = groups.pop()
            groups[-1] += last
        need = len(groups) - 1
    chosen = sorted(sorted(ps, key=lambda p: p[1] - p[0], reverse=True)[:need])
    bounds = [max(0.0, s0 - 0.03)] + [p[1] - 0.025 for p in chosen] + [min(len(x) / SR, s1 + 0.08)]
    ends = [p[0] + 0.06 for p in chosen] + [min(len(x) / SR, s1 + 0.08)]
    return [{"idx": g, "a": bounds[k], "b": ends[k]} for k, g in enumerate(groups)]


def _syl(w: str) -> float:
    return float(S._syllables(w)) + (0.6 if re.search(r"[,!?:.;]$", w) else 0)


def quantise_line(line: dict, clip: Path) -> tuple[np.ndarray, list[dict]]:
    """Return the vocal for one line (starting at the line's downbeat) and the word timings relative to it."""
    x = load_mono(clip)
    heard = norm_word(words_of(clip, line["text"])["text"])
    if SequenceMatcher(a=heard, b=norm_word(line["text"])).ratio() < 0.8:
        print(f"  ! ASR check: '{line['text']}' heard differently: {heard}")
    words = line["words"]
    targets = [b * S.BEAT for _, b in words]
    line_len = 8 * S.BEAT
    out = np.zeros(int((line_len + 2.0) * SR), dtype=np.float32)
    timings: list[dict] = []
    chunks = chunks_of(line, x)
    lead = 0.03  # the cut sits just before the consonant; land it a hair ahead of the beat
    for k, ch in enumerate(chunks):
        first, lastw = ch["idx"][0], ch["idx"][-1]
        seg = x[int(ch["a"] * SR): int(ch["b"] * SR)]
        natural = len(seg) / SR
        t_next = targets[chunks[k + 1]["idx"][0]] if k + 1 < len(chunks) else line_len * 0.82
        avail = t_next - targets[first]
        # natural speech pace inside the chunk; gentle stretch (max 30% longer / 25% shorter) to sit on the grid
        # and, for multi-word chunks, to reach the beat of its last word
        want_end = (targets[lastw] - targets[first]) + 0.45 if len(ch["idx"]) > 1 else natural
        want = min(avail * 0.95, max(natural, want_end))
        ratio = max(0.75, min(1.3, want / max(natural, 1e-3)))
        y = stretch(seg, ratio).copy()
        y = y[: int(max(avail - 0.01, 0.12) * SR)]  # never overlap the next chunk
        fi, fo = int(0.004 * SR), int(0.025 * SR)
        if len(y) > fi + fo:
            y[:fi] *= np.linspace(0, 1, fi)
            y[-fo:] *= np.linspace(1, 0, fo)
        start = max(0.0, targets[first] - lead)
        i0 = int(start * SR)
        i1 = min(len(out), i0 + len(y))
        out[i0:i1] += y[: i1 - i0]
        # karaoke times inside the chunk: syllable-proportional over the voiced length
        dur = len(y) / SR - 0.05
        sy = [_syl(words[i][0]) for i in ch["idx"]]
        acc = 0.0
        for i, n in zip(ch["idx"], sy):
            s = start + lead + dur * acc / sum(sy)
            acc += n
            e = start + lead + dur * acc / sum(sy)
            timings.append({"w": words[i][0], "s": round(s, 3), "e": round(max(e, s + 0.18), 3)})
    return out, timings


def build(voice: str) -> None:
    total = int(S.duration_seconds() * SR)
    vocal = np.zeros(total + SR * 3, dtype=np.float32)
    timeline = []
    cache: dict[str, tuple[np.ndarray, list[dict]]] = {}
    for ln in S.lines():
        if ln["text"] not in cache:
            clip = tts(ln["text"], voice)
            cache[ln["text"]] = quantise_line(ln, clip)
        y, words = cache[ln["text"]]
        t0 = ln["bar"] * S.BAR
        a = int(t0 * SR)
        vocal[a: a + len(y)] += y[: len(vocal) - a]
        timeline.append({k: v for k, v in ln.items() if k not in ("melody", "words", "claps")} |
                        {"start": round(t0, 3), "end": round(t0 + 8 * S.BEAT, 3),
                         "words": [{**w, "s": round(w["s"] + t0, 3), "e": round(w["e"] + t0, 3)} for w in words],
                         "claps": [round(t0 + c * S.BEAT, 3) for c in ln.get("claps", [])]})
    vocal = vocal[:total]
    sf.write(WORK / "vocal.wav", vocal, SR)
    meta = {"title": S.TITLE, "bpm": S.BPM, "beat": S.BEAT, "bar": S.BAR, "duration": round(S.duration_seconds(), 3),
            "voice": voice, "sections": [{"name": n, "kind": k, "start": round(b * S.BAR, 3),
                                          "end": round((b + c) * S.BAR, 3)} for n, k, b, c in S.SECTIONS],
            "lines": timeline}
    (WORK / "timeline.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(f"vocal.wav + timeline.json ({len(timeline)} lines) voice={voice}; spend so far ${_costs()['total_usd']:.4f}")


def f0_stats(x: np.ndarray) -> tuple[float, float]:
    """Crude autocorrelation pitch track -> (median Hz, spread in semitones (p90-p10)) over voiced frames."""
    w, hop = 2048, 512
    f0 = []
    for i in range(0, len(x) - w, hop):
        fr = x[i:i + w] * np.hanning(w)
        if np.sqrt((fr ** 2).mean()) < 0.02:
            continue
        ac = np.fft.irfft(np.abs(np.fft.rfft(fr, 2 * w)) ** 2)[:w]
        lo, hi = int(SR / 600), int(SR / 120)
        k = lo + int(np.argmax(ac[lo:hi]))
        if ac[k] > 0.4 * ac[0]:
            f0.append(SR / k)
    if len(f0) < 5:
        return 0.0, 0.0
    st = 12 * np.log2(np.array(f0) / 100)
    return float(np.median(f0)), float(np.percentile(st, 90) - np.percentile(st, 10))


def audition(voices: list[str]) -> None:
    probe = [S.CHORUS[0], S.lines()[8]]  # chorus line 1 + "Um patinho faz quá, quá!"
    d = WORK / "audition"
    d.mkdir(parents=True, exist_ok=True)
    for v in voices:
        for ln in probe:
            clip = tts(ln["text"], v)
            x = load_mono(clip)
            heard = words_of(clip, ln["text"])["text"]
            hz, spread = f0_stats(x)
            s0, s1 = speech_bounds(x)
            print(f"{v:<8} {s1 - s0:4.2f}s f0~{hz:5.0f}Hz spread {spread:4.1f}st | heard: {heard.strip()}")
            sf.write(d / f"{v}_{norm_word(ln['text'])[:20]}.wav", x, SR)
    print(f"spend so far ${_costs()['total_usd']:.4f}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "audition":
        audition(sys.argv[2:] or ["coral", "nova", "shimmer", "sage"])
    else:
        build(sys.argv[2] if len(sys.argv) > 2 else "coral")
