import pytest

from hiddeneco.models import Claim, Dossier, Source
from hiddeneco.research.dossier import DossierError, to_markdown, unverified, validate
from hiddeneco.research.topics import TopicScore, composite, load_candidates


def test_dossier_built_from_snapshot(dossier):
    gd = dossier.claim("gdppc_che_2023")
    assert gd.status == "data_derived"
    assert 90_000 < gd.value < 110_000
    assert "snapshot" in gd.derived_from["method"][0] or "worldbank_api" in gd.derived_from["method"][0]
    assert gd.fields["year"] == 2023


def test_every_claim_cites_known_sources(dossier):
    ids = {s.id for s in dossier.sources}
    for c in dossier.claims:
        assert c.source_ids and set(c.source_ids) <= ids


def test_unverified_claims_are_surfaced(dossier):
    pending = {c.id for c in unverified(dossier)}
    assert "pharma_share_2024" in pending
    assert "gdppc_che_2023" not in pending
    assert "require verification" in to_markdown(dossier)


def _mini(**claim):
    return Dossier(slug="x", title="x", generated_at="now",
                   sources=[Source(id="s", title="t", publisher="p", url="https://e.org", accessed="2026-01-01")],
                   claims=[Claim(**{"id": "c", "text": "t", "source_ids": ["s"], **claim})])


def test_validate_rejects_unknown_source():
    with pytest.raises(DossierError):
        validate(_mini(source_ids=["nope"]))


def test_validate_requires_verifier_name():
    with pytest.raises(DossierError):
        validate(_mini(status="human_verified"))
    validate(_mini(status="human_verified", verified_by="A. Editor"))


def test_topics_ten_ranked():
    topics = load_candidates()
    assert len(topics) == 10
    scores = [t.composite for t in topics]
    assert scores == sorted(scores, reverse=True)
    assert all(0 <= s <= 100 for s in scores)


def test_difficulty_lowers_score():
    base = dict(title="t", angle="a", audience_interest=4, evergreen=4, evidence_quality=4, rationale={})
    easy = TopicScore(**base, production_difficulty=1)
    hard = TopicScore(**base, production_difficulty=5)
    assert composite(easy) > composite(hard)


def test_api_failing_midway_never_mixes_data_vintages(paths, monkeypatch):
    """If the live API answers some requests and then fails, every data claim must come from the
    snapshot; otherwise one statistic can show two different values in the same video."""
    from hiddeneco.research import data_sources
    from hiddeneco.research.dossier import build_dossier

    calls = {"n": 0}

    def flaky_api(codes, year, timeout=15):
        calls["n"] += 1
        if calls["n"] > 1:
            raise TimeoutError("simulated read timeout")
        snap = data_sources._from_snapshot(codes, year)
        for v in snap.values():   # a different "live" vintage
            v.gdp_per_capita_usd *= 1.05
            v.method = "worldbank_api:NY.GDP.PCAP.CD"
        return snap

    monkeypatch.setattr(data_sources, "offline", lambda: False)
    monkeypatch.setattr(data_sources, "_from_worldbank_api", flaky_api)
    monkeypatch.setattr(data_sources.requests, "get",
                        lambda *a, **k: (_ for _ in ()).throw(TimeoutError("simulated")))
    d = build_dossier(paths)
    methods = {c.get("method") for raw in d.datasets.values() for c in (raw.values() if isinstance(raw, dict) else [])
               if isinstance(c, dict) and "method" in c}
    assert calls["n"] >= 2
    assert data_sources.sources_used() == {"snapshot"}
    assert not any(str(m).startswith("worldbank_api") for m in methods)
    data_sources.reset_run()
