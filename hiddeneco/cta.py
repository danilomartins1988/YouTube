"""The channel's call to action (docs/CTA_STANDARD.md): subscribe + like, narrated and animated, in every long film.

Structure of every episode (from 2026-11-20): opening hook -> narrated SUBSCRIBE ask (cta_card, ~5-7 s) -> channel intro
-> documentary -> narrated LIKE + COMMENT ask (cta_card) -> teaser / end card.

* `insert_cta()` adds, at build time, two narrated segments with a full-frame `cta_card` scene each (Remotion:
  remotion/src/brand/SubscribeCTA.tsx): `cta_subscribe` right BEFORE the `channel_intro` segment, and `cta_like`
  right before the film's last segment (the teaser / end card). The scriptwriter only has to set the wording in
  project.yaml when the generic line does not fit; nothing has to be added to the script or storyboard generators.
  Neither is inserted twice, and a script that already says "subscribe" / "tap like" keeps its own lines.
* Constants below are the single source for the wording used by the pipeline, the description / pinned-comment
  templates, the Shorts package text and tools/cta_retrofit.py.

Per-project configuration (project.yaml):

    cta:
      enabled: true                 # default; false leaves both asks out
      subscribe_line: "..."         # narrated line before the channel intro (one sentence, <= ~8 s)
      like_question: "..."          # the episode question in the end ask, e.g. "would you pay the toll?"
      like_line: "..."              # or the whole end line
      like: true                    # false: no end ask
"""
from __future__ import annotations

import re

from hiddeneco.models import Scene, Script, Segment, Storyboard

SUBSCRIBE_SEGMENT, LIKE_SEGMENT = "cta_subscribe", "cta_like"
SUBSCRIBE_LINE = "If you like finding the hidden money behind the headlines, hit subscribe and like. It really helps the channel."
LIKE_QUESTION = "what hidden business should we open up next?"
LIKE_LINE = "If this changed how you see the story, tap like, and tell us in the comments: {question}"
# text templates (descriptions, pinned comment, Shorts)
DESCRIPTION_LINE = ("Subscribe to The Hidden Economics for a new animated documentary about the money behind the headlines. "
                    "It's free, and it really helps the channel.")
PINNED_LINE = "If this one surprised you, tap like and subscribe: it helps more people find the channel."
SHORT_FOLLOW_LINE = "Follow The Hidden Economics for more of the hidden money behind the headlines."

_SUB_RE = re.compile(r"\bsubscribe\b", re.I)
_LIKE_RE = re.compile(r"\b(tap|hit|leave|smash|give (it|us|this)( a)?)\s+(a\s+)?like\b", re.I)


def _cfg(project: dict) -> dict:
    c = project.get("cta", {})
    if c is False:
        return {"enabled": False}
    return c or {}


def like_line(project: dict) -> str:
    c = _cfg(project)
    return c.get("like_line") or LIKE_LINE.format(question=c.get("like_question") or LIKE_QUESTION)


def insert_cta(project: dict, sc: Script, sb: Storyboard) -> tuple[Script, Storyboard, list[str]]:
    """Return (script, storyboard, inserted segment ids)."""
    c = _cfg(project)
    if c.get("enabled", True) is False or project.get("renderer") != "remotion":   # cta_card is a Remotion scene
        return sc, sb, []
    segs, scenes, done = list(sc.segments), list(sb.scenes), []
    text = " ".join(s.narration for s in segs)
    ids = [s.id for s in segs]

    def add(seg_id: str, before_seg: str, narration: str, kind: str, chapter: str) -> None:
        segs.insert([s.id for s in segs].index(before_seg), Segment(id=seg_id, chapter=chapter, narration=narration, claims=[]))
        first = min(i for i, s in enumerate(scenes) if s.segment == before_seg)
        scenes.insert(first, Scene(id=seg_id, segment=seg_id, type="cta_card", params={"kind": kind, "no_chrome": True},
                                   sources=[], assets=["font:inter"], note=f"Channel call to action ({kind})"))
        done.append(seg_id)

    if SUBSCRIBE_SEGMENT not in ids and not _SUB_RE.search(text):
        order = [s.segment for s in scenes]
        if "channel_intro" in order:
            before = "channel_intro"
        else:   # no intro: before the first act card, else after ~30 s worth of segments
            before = next((s.segment for s in scenes if s.type == "act_title" or s.segment.endswith("_card")), order[min(3, len(order) - 1)])
        prev = segs[max(0, [s.id for s in segs].index(before) - 1)]
        add(SUBSCRIBE_SEGMENT, before, c.get("subscribe_line") or SUBSCRIBE_LINE, "subscribe", prev.chapter)
    if c.get("like", True) and LIKE_SEGMENT not in ids and not _LIKE_RE.search(text) and len(scenes) > 2:
        ends = [s.segment for s in scenes[-4:] if s.type == "end_card" or s.segment == "teaser"]
        last = ends[0] if ends else scenes[-1].segment     # before the teaser / end card (a "button" joke stays after)
        prev = next(s for s in segs if s.id == last)
        add(LIKE_SEGMENT, last, like_line(project), "like", prev.chapter)
    if not done:
        return sc, sb, []
    return sc.model_copy(update={"segments": segs}), sb.model_copy(update={"scenes": scenes}), done
