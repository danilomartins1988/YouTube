import numpy as np
import pytest

from hiddeneco import audio, timing
from hiddeneco.retry import retry


def test_sentence_split_and_word_timings():
    sents = timing.sentences("Stability. Specialisation. Skills. It built it.")
    assert sents == ["Stability.", "Specialisation.", "Skills.", "It built it."]
    words = timing.word_timings("In 2023, it produced almost 100,000 dollars.", 1.0, 4.0)
    assert words[0]["start"] == 1.0
    assert abs(words[-1]["end"] - 5.0) < 1e-6          # trailing pause excluded -> ends exactly
    assert all(a["end"] <= b["start"] for a, b in zip(words, words[1:]))
    long_num = next(w for w in words if w["word"].startswith("100,000"))
    short = next(w for w in words if w["word"] == "it")
    assert long_num["end"] - long_num["start"] > short["end"] - short["start"]


def test_cue_time_is_punctuation_blind():
    words = timing.word_timings("Part of the answer is stability. In 1815, Europe's powers", 0.0, 5.0)
    assert timing.cue_time(words, "in 1815") == next(w["start"] for w in words if w["word"] == "In")
    assert timing.cue_time(words, "not there") is None


def test_caption_chunks_break_on_punctuation_and_length():
    words = timing.word_timings("It isn't chocolate. And it isn't watches.", 0.0, 3.0)
    chunks = timing.caption_chunks(words, max_words=3, max_chars=18)
    assert [c["text"] for c in chunks] == ["It isn't", "chocolate.", "And it isn't", "watches."]
    assert all(len(c["text"]) <= 18 for c in chunks)
    assert all(c["start"] < c["end"] for c in chunks)


@pytest.mark.parametrize("kind", ["whoosh", "pop", "tick", "hit"])
def test_sfx_are_normalised(kind):
    x = audio.sfx(kind)
    assert 0 < len(x) < audio.RATE and abs(np.max(np.abs(x)) - 1.0) < 1e-3


def test_music_ducks_under_voice():
    rate = audio.RATE
    voice = np.zeros(rate * 8, np.float32)
    voice[rate * 4:rate * 6] = 0.5 * np.sin(np.linspace(0, 2000, rate * 2)).astype(np.float32)
    bed = audio.mix(np.zeros_like(voice), [], music=True)
    ducked = audio.mix(voice, [], music=True) - voice
    loud = slice(rate * 4 + rate // 2, rate * 6 - rate // 2)
    assert np.abs(ducked[loud]).mean() < 0.6 * np.abs(bed[loud]).mean()


def test_retry_backoff():
    calls, sleeps = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise ConnectionError("boom")
        return "ok"
    assert retry(flaky, attempts=4, base_delay=2, sleep=sleeps.append) == "ok"
    assert sleeps == [2, 4]
    with pytest.raises(ConnectionError):
        retry(lambda: (_ for _ in ()).throw(ConnectionError("x")), attempts=2, sleep=lambda s: None)
