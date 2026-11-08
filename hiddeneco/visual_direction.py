"""Adaptive visual storytelling: the story sets the visual atmosphere, not the cartoon style.

Each project may carry `visual_direction.yaml` (written by `tools/visual_direction.py plan <slug>` and then edited by
a human). It is APPLIED to the render, not just documented:

- `palette`: merged over `project.yaml` style.palette (cards, kinetic text, studio, chrome and charts follow it).
- `primary_tone` / `chapters` / `segments`: each engine_cartoon / engine_draw scene gets `tone` (unless the storyboard
  already sets one). Tones: bright, thriller, crisis, strategy, trade, tech, history, reflective
  (remotion/src/animation-engine/tone.tsx).
- `turning_points`: [{segment, cue, to, dur}] add a `toneShift` inside that scene at the narration cue.
- `presenter`: {demeanor: serious|neutral|warm, min_sequences: N}: demeanour for every engine_draw scene; the
  minimum number of presenter sequences QC expects (overrides project.yaml presenter_min).

Projects without the file render exactly as before.
"""
from __future__ import annotations

from pathlib import Path

import yaml

TONES = ("bright", "thriller", "crisis", "strategy", "trade", "tech", "history", "reflective")
SERIOUS = {"thriller", "crisis", "reflective"}
TONED_TYPES = {"engine_cartoon", "engine_draw"}


def load(project_dir: Path, deliverable_dir: Path | None = None) -> dict | None:
    """The visual direction for a deliverable (deliverable-level file wins over the project-level one)."""
    for d in ([deliverable_dir] if deliverable_dir else []) + [project_dir]:
        f = d / "visual_direction.yaml"
        if f.exists():
            vd = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
            bad = [t for t in tone_names(vd) if t not in TONES]
            if bad:
                raise ValueError(f"{f}: unknown tone(s) {bad}; use one of {TONES}")
            return vd
    return None


def tone_names(vd: dict) -> list[str]:
    out = [vd.get("primary_tone", "bright")] + list(vd.get("secondary_tones") or [])
    out += [c.get("tone") for c in vd.get("chapters") or [] if c.get("tone")]
    out += list((vd.get("segments") or {}).values())
    out += [tp.get("to") for tp in vd.get("turning_points") or [] if tp.get("to")]
    return [t for t in out if t]


def merge_palette(project: dict, vd: dict | None) -> dict:
    if not vd or not vd.get("palette"):
        return project
    style = dict(project.get("style") or {})
    style["palette"] = {**(style.get("palette") or {}), **vd["palette"]}
    return {**project, "style": style}


def tone_for(vd: dict, segment_id: str, chapter: str) -> str:
    seg = vd.get("segments") or {}
    if segment_id in seg:
        return seg[segment_id]
    for c in vd.get("chapters") or []:
        if c.get("chapter", "").strip().lower() == (chapter or "").strip().lower():
            return c["tone"]
    return vd.get("primary_tone", "bright")


def apply(vd: dict | None, script, storyboard) -> list[str]:
    """Set tone / toneShift / demeanor on the storyboard scenes in place. Returns a log of what changed."""
    if not vd:
        return []
    chap = {s.id: s.chapter for s in script.segments}
    shifts = {}
    for tp in vd.get("turning_points") or []:
        shifts.setdefault(tp["segment"], tp)
    demeanor = (vd.get("presenter") or {}).get("demeanor")
    changed = []
    for sc in storyboard.scenes:
        if sc.type not in TONED_TYPES:
            continue
        p = sc.params
        if "tone" not in p:
            p["tone"] = tone_for(vd, sc.segment, chap.get(sc.segment, ""))
        tp = shifts.get(sc.segment)
        if tp and "toneShift" not in p:
            p["toneShift"] = {"at": {"cue": tp["cue"], **({"offset": tp["offset"]} if "offset" in tp else {})}, "to": tp["to"], "dur": tp.get("dur", 2.5)}
        if sc.type == "engine_draw" and "demeanor" not in p:
            tone_now = p["toneShift"]["to"] if "toneShift" in p else p["tone"]
            p["demeanor"] = "serious" if (p["tone"] in SERIOUS or tone_now in SERIOUS) else demeanor
            if p["demeanor"] is None:
                del p["demeanor"]
        changed.append(f"{sc.id}:{p['tone']}" + (f"->{p['toneShift']['to']}" if "toneShift" in p else ""))
    return changed


def presenter_min(project: dict, vd: dict | None, default: int = 4) -> int:
    if vd and (vd.get("presenter") or {}).get("min_sequences") is not None:
        return int(vd["presenter"]["min_sequences"])
    return int(project.get("presenter_min", default))
