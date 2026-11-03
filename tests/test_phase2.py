import pytest

from hiddeneco.research.dossier import DossierError, _series_claim
from hiddeneco.speech_text import int_words, spoken, year_words


@pytest.mark.parametrize("year,words", [(1815, "eighteen fifteen"), (1848, "eighteen forty-eight"),
                                        (1900, "nineteen hundred"), (2005, "two thousand five"),
                                        (2023, "twenty twenty-three"), (1908, "nineteen oh eight")])
def test_years_read_like_a_narrator(year, words):
    assert year_words(year) == words


def test_numbers_currency_percent():
    assert int_words(139) == "one hundred thirty-nine"
    assert int_words(99557) == "ninety-nine thousand five hundred fifty-seven"
    assert spoken("$99,557") == "ninety-nine thousand five hundred fifty-seven dollars"
    assert spoken("52.7 percent") == "fifty-two point seven percent"
    assert spoken("52.7%") == "fifty-two point seven percent"
    assert spoken("In 1815, the") == "In eighteen fifteen, the"
    assert spoken("#1 of 139") == "number one of one hundred thirty-nine"
    assert spoken("about 8.9 million") == "about eight point nine million"


def test_series_and_always_above(dossier):
    series = dossier.claim("gdppc_series_2000_2023").value
    assert {s["code"] for s in series} == {"CHE", "USA", "DEU", "EUU"}
    assert all(len(s["points"]) == 24 for s in series)
    assert dossier.claim("che_above_deu_euu_2000_2023").value is True


def test_always_above_refuses_false_statement():
    spec = {"id": "x", "metric": "series_always_above", "country": "EUU", "others": ["CHE"],
            "start_year": 2000, "end_year": 2023, "source_ids": ["wb_gdp_mirror"]}
    with pytest.raises(DossierError, match="must not claim"):
        _series_claim(spec)


def test_silent_scene_duration(paths, dossier):
    from hiddeneco.config import settings
    from hiddeneco.models import Script, Segment, Scene, Storyboard
    from hiddeneco.render.assemble import synthesize_narration
    from hiddeneco.tts.providers import get_provider
    sc = Script(title="t", segments=[Segment(id="card", narration="")])
    sb = Storyboard(scenes=[Scene(id="c", segment="card", type="act_title", params={"min_seconds": 3.0})])
    fmt = settings()["formats"]["long_16x9"]
    timed, chars = synthesize_narration(sc, dossier, sb, get_provider("silent", settings()), paths.out_sub("a"),
                                        fmt, 48000, 30, 0.2)
    assert chars == 0 and timed[0].audio_seconds == 0 and abs(timed[0].duration - 3.0) < 0.04


def test_budget_refuses_before_overspending(tmp_path):
    from hiddeneco.budget import Budget, BudgetExceeded
    b = Budget(tmp_path / "spend.json", 0.50, 0.030, "openai")
    b.check(9000)                      # $0.27 fits
    b.charge(9000, "topic")
    assert abs(b.spent - 0.27) < 1e-9
    with pytest.raises(BudgetExceeded):
        b.check(8000)                  # +$0.24 would exceed $0.50
    b2 = Budget(tmp_path / "spend.json", 0.50, 0.030, "openai")   # persists across runs
    assert abs(b2.remaining() - 0.23) < 1e-9
    with pytest.raises(BudgetExceeded):
        Budget(tmp_path / "x.json", 0.50, None, "elevenlabs")   # unknown price -> refuse


def test_paid_provider_without_budget_never_calls_api(tmp_path, dossier):
    from hiddeneco.render.assemble import _sentence_audio
    from hiddeneco.tts.base import TTSProvider

    class FakePaid(TTSProvider):
        name, paid, calls = "fake", True, 0

        def available(self):
            return True, ""

        def _synthesize(self, text, out_path):
            FakePaid.calls += 1
            raise AssertionError("must not be called")
    with pytest.raises(RuntimeError, match="without a budget"):
        _sentence_audio(FakePaid(), "Hello there.", tmp_path, 48000)
    assert FakePaid.calls == 0
