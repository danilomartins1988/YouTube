"""Typed data models shared by every pipeline stage."""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

# Claim status ladder. Only VERIFIED_STATUSES may be published.
#   data_derived     - computed by this pipeline from a cited, licensed dataset
#   human_verified   - a named person read the primary source and confirmed the claim
#   source_located   - a plausible source was found but nobody has read it in full yet
#   needs_verification - no adequate source yet
ClaimStatus = Literal["data_derived", "human_verified", "source_located", "needs_verification"]
VERIFIED_STATUSES = {"data_derived", "human_verified"}


class Source(BaseModel):
    id: str
    title: str
    publisher: str
    url: str
    published: str | None = None        # as stated by the publisher; None if unknown
    accessed: str                       # ISO date the URL was located/retrieved
    kind: Literal["primary", "secondary", "dataset"] = "primary"
    license: str | None = None
    credit: str | None = None           # short on-screen credit
    notes: str = ""


class Claim(BaseModel):
    id: str
    text: str                           # the factual statement in plain English
    spoken: str | None = None           # how narration says it, e.g. "about two thirds"
    display: str | None = None          # how it appears on screen, e.g. "52.7%"
    value: Any = None                   # machine-readable value for charts
    fields: dict[str, Any] = Field(default_factory=dict)  # extra values, e.g. {"year": 2024}
    source_ids: list[str]
    status: ClaimStatus = "needs_verification"
    verified_by: str | None = None
    verification_note: str = ""
    derived_from: dict[str, Any] | None = None


class Dossier(BaseModel):
    slug: str
    title: str
    generated_at: str
    sources: list[Source]
    claims: list[Claim]
    datasets: dict[str, Any] = Field(default_factory=dict)
    open_questions: list[str] = Field(default_factory=list)

    def claim(self, claim_id: str) -> Claim:
        for c in self.claims:
            if c.id == claim_id:
                return c
        raise KeyError(f"Unknown claim '{claim_id}'")

    def source(self, source_id: str) -> Source:
        for s in self.sources:
            if s.id == source_id:
                return s
        raise KeyError(f"Unknown source '{source_id}'")


class Segment(BaseModel):
    id: str
    chapter: str = ""
    narration: str                      # template; may contain {{claim_id}} placeholders
    claims: list[str] = Field(default_factory=list)
    source_note: str = ""
    analysis: bool = False              # True when the segment contains editorial interpretation


class Script(BaseModel):
    title: str
    logline: str = ""
    segments: list[Segment]


class Scene(BaseModel):
    id: str
    segment: str
    type: Literal["title_card", "map", "bar_chart", "kinetic_text", "ring_stat",
                  "pictogram", "ranking", "end_card", "big_number", "timeline"]
    params: dict[str, Any] = Field(default_factory=dict)
    sfx: list[dict[str, Any]] = Field(default_factory=list)   # e.g. {kind: pop, cue: "In 1815"}
    sources: list[str] = Field(default_factory=list)
    assets: list[str] = Field(default_factory=list)
    note: str = ""


class Storyboard(BaseModel):
    scenes: list[Scene]


class TimedScene(BaseModel):
    scene: Scene
    narration: str
    audio_path: str
    audio_seconds: float
    start: float
    duration: float
    words: list[dict[str, Any]] = Field(default_factory=list)  # times relative to scene start


class Deliverable(BaseModel):
    id: str
    format: Literal["long_16x9", "short_9x16", "extended_9x16"]
    title: str
    target_seconds: dict[str, float]
    captions: dict[str, bool] = Field(default_factory=lambda: {"burn_in": False, "sidecar": True})
    audio: dict[str, bool] = Field(default_factory=lambda: {"music": True, "sfx": True})
    platforms: list[str] = Field(default_factory=list)

    @property
    def vertical(self) -> bool:
        return self.format.endswith("9x16")


class CostLine(BaseModel):
    step: str
    provider: str
    units: float
    unit: str
    usd_per_unit: float | None
    usd: float | None
    estimated: bool = True
    note: str = ""
