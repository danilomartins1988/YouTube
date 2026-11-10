"""Storyboard lint for the diversity / hook rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md).

Checks every CartoonStage scene (engine_cartoon) of a project's storyboard:
- EMPTY_OPEN: no item and no callout appears in the first 1.0 s (all wait for narration cues) -> the scene opens on an
  empty backdrop for a moment. Fix: give at least one item `at` <= 1.0.
- CALLOUT_HEAVY: more than one callout at the bottom centre (y >= 900) in a scene.
- BOTTOM_SHARE: share of scenes with a bottom-centre callout above 1/2 for the episode.
- SAME_ZONE_RUN: three or more consecutive cartoon scenes on the same set (visual monotony).

Run: python tools/lint_storyboard.py <slug> [deliverable]   (exit code 0; prints findings)
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def early(v) -> bool:
    return isinstance(v, (int, float)) and v <= 1.0


def lint(slug: str, dv: str = "documentary") -> list[str]:
    sb = yaml.safe_load((ROOT / "projects" / slug / "deliverables" / dv / "storyboard.yaml").read_text())
    scenes = sb["scenes"] if isinstance(sb, dict) else sb
    out, bottom, carts, prev_sets, run = [], 0, 0, None, 0
    for s in scenes:
        if s.get("type") != "engine_cartoon":
            prev_sets, run = None, 0
            continue
        carts += 1
        p = s.get("params", {})
        items, cos = p.get("items") or [], p.get("callouts") or []
        firsts = [i.get("at", 0) for i in items] + [c.get("at") for c in cos]
        # items in a pinboard carry their own card times
        for i in items:
            for c in i.get("cards") or []:
                firsts.append(c.get("at", 0))
        if not any(early(v) for v in firsts):
            out.append(f"EMPTY_OPEN  {s['id']}: nothing visible in the first second")
        bc = [c for c in cos if c.get("y", 0) >= 900 and abs(c.get("x", 960) - 960) < 200]
        if len(bc) > 1:
            out.append(f"CALLOUT_HEAVY {s['id']}: {len(bc)} bottom-centre callouts")
        bottom += 1 if bc else 0
        sets = tuple(z.get("set") for z in p.get("zones") or [])
        run = run + 1 if sets == prev_sets else 1
        prev_sets = sets
        if run == 3:
            out.append(f"SAME_ZONE_RUN {s['id']}: 3+ consecutive scenes on {sets}")
    if carts and bottom / carts > 0.5:
        out.append(f"BOTTOM_SHARE: {bottom}/{carts} cartoon scenes use a bottom-centre callout (> 1/2)")
    return out


if __name__ == "__main__":
    slug = sys.argv[1]
    res = lint(slug, sys.argv[2] if len(sys.argv) > 2 else "documentary")
    print(f"{slug}: {len(res)} finding(s)")
    for r in res:
        print("  " + r)
