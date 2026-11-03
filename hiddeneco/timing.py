"""Narration timing: sentence splitting, per-word timing estimates, cue lookup, caption chunks.

Each sentence is synthesised separately, so sentence boundaries are exact. Inside a sentence,
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
