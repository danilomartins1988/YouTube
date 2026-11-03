"""Narration timing: sentence splitting, per-word timing estimates, cue lookup, caption chunks.

When each sentence is synthesised separately, sentence boundaries are exact. When a whole
paragraph is synthesised at once, boundaries are snapped to the pauses detected in the audio
(`paragraph_word_timings`). Inside a sentence,
word times are distributed by estimated syllables plus punctuation pauses, which is typically
within ~0.2 s of the real speech. A forced aligner can replace `word_timings` later without
changing anything downstream.
"""
from __future__ import annotations

import re

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
VOWEL_GROUPS = re.compile(r"[aeiouy]+", re.IGNORECASE)
PAUSE_WEIGHT = {",": 0.9, ";": 1.2, ":": 1.2, ".": 1.4, "!": 1.4, "?": 1.4}


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENTENCE_SPLIT.split(text.strip()) if s.strip()]


def syllables(word: str) -> float:
    core = re.sub(r"[^\w.,%$]", "", word)
    digits = re.sub(r"\D", "", core)
    if digits:
        # "100,000" -> "one hundred thousand" etc. Rough but monotone in length.
        return 1.6 * len(digits) + (1.5 if "." in core.strip(".,") else 0) + (2 if "%" in core else 0)
    letters = re.sub(r"[^A-Za-z']", "", word).lower()
    if not letters:
        return 0.5
    n = len(VOWEL_GROUPS.findall(letters))
    if letters.endswith("e") and not letters.endswith(("le", "ee")) and n > 1:
        n -= 1
    return float(max(1, n))


def word_timings(sentence: str, start: float, duration: float) -> list[dict]:
    words = sentence.split()
    weights, pauses = [], []
    for w in words:
        weights.append(syllables(w))
        pauses.append(PAUSE_WEIGHT.get(w[-1], 0.0) if w else 0.0)
    pauses[-1] = 0.0                      # trailing silence was trimmed from the audio
    total = sum(weights) + sum(pauses) or 1.0
    unit = duration / total
    out, t = [], start
    for w, wt, p in zip(words, weights, pauses):
        d = wt * unit
        out.append({"word": w, "start": round(t, 3), "end": round(t + d, 3)})
        t += d + p * unit
    return out


def _weight(sentence: str) -> float:
    words = sentence.split()
    return sum(syllables(w) for w in words) + sum(PAUSE_WEIGHT.get(w[-1], 0.0) for w in words[:-1])


def pauses(samples, rate: int, min_gap: float = 0.12, floor_db: float = -35.0) -> list[tuple[float, float]]:
    """(start, end) seconds of quiet stretches at least `min_gap` long, relative to the peak level."""
    import numpy as np
    hop = max(1, int(0.01 * rate))
    n = len(samples) // hop
    if n == 0:
        return []
    frames = np.asarray(samples[: n * hop], dtype=np.float64).reshape(n, hop)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    quiet = rms < (rms.max() or 1.0) * 10 ** (floor_db / 20)
    out, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * hop / rate >= min_gap and i > 0 and j < n:   # interior pauses only
                out.append((i * hop / rate, j * hop / rate))
            i = j
        else:
            i += 1
    return out


def paragraph_word_timings(sents: list[str], samples, rate: int, start: float) -> list[dict]:
    """Word timings for several sentences spoken in ONE audio clip.

    Sentence ends are estimated by syllable weight. When the audio has at least as many interior
    pauses as needed, the boundaries are the in-order set of pauses that maximises
    sum(pause length - 0.5 * distance from its estimated position): sentence breaks are usually the
    longest pauses. Otherwise the estimates are used."""
    total = len(samples) / rate
    weights = [_weight(s) for s in sents]
    gap_w = PAUSE_WEIGHT["."]
    unit = total / ((sum(weights) + gap_w * (len(sents) - 1)) or 1.0)
    expected, t = [], 0.0
    for w in weights[:-1]:
        t += w * unit
        expected.append(t + gap_w * unit / 2)            # middle of the estimated pause
        t += gap_w * unit
    need, found = len(expected), pauses(samples, rate)
    if need and len(found) >= need:
        score = lambda k, j: (found[j][1] - found[j][0]) - 0.5 * abs(sum(found[j]) / 2 - expected[k])
        n = len(found)
        best = [[float("-inf")] * n for _ in range(need)]
        back = [[-1] * n for _ in range(need)]
        for j in range(n):
            best[0][j] = score(0, j)
        for k in range(1, need):
            run, arg = float("-inf"), -1
            for j in range(n):
                if j and best[k - 1][j - 1] > run:
                    run, arg = best[k - 1][j - 1], j - 1
                if arg >= 0:
                    best[k][j], back[k][j] = run + score(k, j), arg
        j = max(range(n), key=lambda x: best[need - 1][x])
        picks = []
        for k in range(need - 1, -1, -1):
            picks.append(found[j])
            j = back[k][j]
        cuts = list(reversed(picks))
    else:
        cuts = [(e - gap_w * unit / 2, e + gap_w * unit / 2) for e in expected]
    spans, t = [], 0.0
    for a, b in cuts:
        spans.append((t, a))
        t = b
    spans.append((t, total))
    out = []
    for sent, (a, b) in zip(sents, spans):
        out += word_timings(sent, start + a, max(0.05, b - a))
    return out


def _norm(w: str) -> str:
    return re.sub(r"[^\w%]", "", w.lower())


def cue_time(words: list[dict], phrase: str) -> float | None:
    """Start time of the first occurrence of `phrase` in the word list (case/punctuation-blind)."""
    target = [_norm(x) for x in phrase.split() if _norm(x)]
    if not target:
        return None
    seq = [_norm(w["word"]) for w in words]
    for i in range(len(seq) - len(target) + 1):
        if seq[i:i + len(target)] == target:
            return words[i]["start"]
    return None


def caption_chunks(words: list[dict], max_words: int = 3, max_chars: int = 18) -> list[dict]:
    """Group words into short on-screen captions, breaking after punctuation."""
    chunks, cur = [], []
    for w in words:
        trial = " ".join(x["word"] for x in cur + [w])
        if cur and (len(cur) >= max_words or len(trial) > max_chars):
            chunks.append(cur)
            cur = []
        cur.append(w)
        if w["word"][-1] in ".,;:!?":
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    return [{"text": " ".join(x["word"] for x in c), "start": c[0]["start"], "end": c[-1]["end"],
             "words": c} for c in chunks]
