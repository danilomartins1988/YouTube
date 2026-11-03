import pytest

from hiddeneco.config import settings
from hiddeneco.costs import CostLedger, tts_cost
from hiddeneco.tts.providers import get_provider

from .conftest import requires_ffmpeg


def test_unknown_price_stays_unknown():
    assert tts_cost("elevenlabs", 1000).usd is None
    assert tts_cost("espeak", 1000).usd == 0


def test_ledger_flags_unknown(tmp_path):
    ledger = CostLedger(tmp_path / "c.json")
    ledger.replace_step("tts", tts_cost("elevenlabs", 1000))
    total, unknown = ledger.total()
    assert total == 0 and unknown
    assert "unknown" in ledger.markdown()


def test_paid_provider_needs_explicit_permission():
    with pytest.raises(PermissionError):
        get_provider("elevenlabs", settings())
    with pytest.raises(PermissionError):
        get_provider("openai", settings())


@requires_ffmpeg
def test_silent_provider_writes_audio(tmp_path):
    tts = get_provider("silent", settings())
    seconds = tts.synthesize("one two three four five six seven eight nine ten", tmp_path / "a.wav")
    assert 2 < seconds < 6
