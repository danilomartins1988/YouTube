"""Topic proposals with transparent, editable scoring.

Candidate topics and their 1-5 criterion scores live in config/topic_candidates.yaml. Scores are
editorial judgements written by a person (with a rationale for each), not measured audience data;
the report says so. Swap in measured signals (e.g. YouTube search volume) later by adding a field
and a weight - the ranking code does not change.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml
from pydantic import BaseModel

from hiddeneco.config import REPO_ROOT

WEIGHTS = {"audience_interest": 0.35, "evergreen": 0.25, "evidence_quality": 0.25,
           "production_difficulty": -0.15}   # harder production lowers the score


class TopicScore(BaseModel):
    title: str
    angle: str
    audience_interest: int
    evergreen: int
    evidence_quality: int
    production_difficulty: int
    rationale: dict[str, str]
    key_sources_to_find: list[str] = []
    composite: float = 0.0


def composite(t: TopicScore, weights: dict[str, float] = WEIGHTS) -> float:
    """Scale to 0-100. Positive criteria map 1..5 -> 0..1; difficulty is subtracted the same way."""
    pos = sum(w for w in weights.values() if w > 0)
    score = 0.0
    for key, w in weights.items():
        norm = (getattr(t, key) - 1) / 4
        score += w * norm
    neg = -sum(w for w in weights.values() if w < 0)
    return round(100 * (score + neg) / (pos + neg), 1)


def load_candidates(path: Path | None = None) -> list[TopicScore]:
    path = path or REPO_ROOT / "config" / "topic_candidates.yaml"
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))["topics"]
    topics = [TopicScore(**t) for t in raw]
    for t in topics:
        for k in ("audience_interest", "evergreen", "evidence_quality", "production_difficulty"):
            if not 1 <= getattr(t, k) <= 5:
                raise ValueError(f"{t.title}: {k} must be 1-5")
        t.composite = composite(t)
    return sorted(topics, key=lambda t: t.composite, reverse=True)


def report(topics: list[TopicScore], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "topics.json").write_text(json.dumps([t.model_dump() for t in topics], indent=2))
    lines = ["# Topic proposals", "",
             "Scores are 1-5 editorial judgements (see rationale), not measured audience data. "
             f"Weights: {WEIGHTS}. Production difficulty counts against a topic.", "",
             "| # | Topic | Interest | Evergreen | Evidence | Difficulty | Score |",
             "|---|---|---|---|---|---|---|"]
    for i, t in enumerate(topics, 1):
        lines.append(f"| {i} | **{t.title}** - {t.angle} | {t.audience_interest} | {t.evergreen} | "
                     f"{t.evidence_quality} | {t.production_difficulty} | {t.composite} |")
    lines += ["", "## Rationale", ""]
    for t in topics:
        lines.append(f"### {t.title} ({t.composite})")
        lines += [f"- **{k}**: {v}" for k, v in t.rationale.items()]
        if t.key_sources_to_find:
            lines.append("- **Sources to locate:** " + "; ".join(t.key_sources_to_find))
        lines.append("")
    path = out_dir / "topics.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
