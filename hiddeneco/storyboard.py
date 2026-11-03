"""Storyboard loading, placeholder rendering and markdown export."""
from __future__ import annotations

from pathlib import Path

import yaml

from hiddeneco.models import Dossier, Scene, Script, Storyboard
from hiddeneco.script import render_value


def load_storyboard(project_dir: Path) -> Storyboard:
    return Storyboard(**yaml.safe_load((project_dir / "storyboard.yaml").read_text(encoding="utf-8")))


def rendered(storyboard: Storyboard, dossier: Dossier) -> Storyboard:
    scenes = [Scene(**{**s.model_dump(), "params": render_value(s.params, dossier)})
              for s in storyboard.scenes]
    return Storyboard(scenes=scenes)


def check_alignment(storyboard: Storyboard, script: Script) -> list[str]:
    seg_ids = [s.id for s in script.segments]
    scene_segs = [s.segment for s in storyboard.scenes]
    errors = [f"Scene {s.id} references unknown segment '{s.segment}'"
              for s in storyboard.scenes if s.segment not in seg_ids]
    errors += [f"Segment '{sid}' has no scene" for sid in seg_ids if sid not in scene_segs]
    return errors


def to_markdown(sb: Storyboard, dossier: Dossier) -> str:
    lines = ["# Storyboard", "", "| Scene | Segment | Visual | Key on-screen content | Sources | Assets |",
             "|---|---|---|---|---|---|"]
    for s in sb.scenes:
        p = s.params
        content = p.get("title") or p.get("headline") or p.get("display") or \
            ", ".join(str(x.get("text")) for x in p.get("lines", [])) or ", ".join(p.get("words", []))
        lines.append(f"| {s.id} | {s.segment} | {s.type} | {content} | {', '.join(s.sources) or '-'} "
                     f"| {', '.join(s.assets)} |")
    lines += ["", "All visuals are generated programmatically (licence: original-programmatic) from "
              "the listed datasets; no third-party footage is used."]
    return "\n".join(lines) + "\n"
