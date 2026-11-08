"""Render an episode's thumbnail from the `thumbnail` block of its visual_direction.yaml (designed separately from the film).

  python tools/tone_thumbnail.py <slug> <out.png> [--doc docs/episodes/NN-name]

thumbnail:
  tone: thriller                      # same grade as the film's dominant tone
  headline: ["$2 BILLION", "NEVER EXISTED"]   # 2-4 words, 1-2 lines
  accent_line: 1
  side: left                          # headline side; the dominant object sits on the other side
  at: 3.0                             # frozen time in the scene
  scene: {zones: [...], items: [...], cam: [...]}   # a purpose-built CartoonStage (or {ocean: true, ...})
Rules: one dominant visual idea, strong contrast, readable at phone size, no screenshots of the film.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.render import remotion_bridge as rb  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("out")
    a = ap.parse_args()
    vd = yaml.safe_load((ROOT / "projects" / a.slug / "visual_direction.yaml").read_text(encoding="utf-8"))
    th = vd.get("thumbnail") or {}
    if not th.get("scene") or not th.get("headline"):
        raise SystemExit("visual_direction.yaml: thumbnail needs `scene` and `headline`")
    words = sum(len(l.split()) for l in th["headline"])
    if words > 5:
        print(f"warning: {words} words in the headline; keep it to 2-4 for mobile")
    props = {"tone": th.get("tone", vd.get("primary_tone", "bright")), "scene": th["scene"], "at": th.get("at", 3.0),
             "headline": th["headline"], "accent_line": th.get("accent_line", 1), "side": th.get("side", "left")}
    work = ROOT / "output" / a.slug / "thumbnail_work"
    work.mkdir(parents=True, exist_ok=True)
    (work / "props.json").write_text(json.dumps(props))
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["npx", "remotion", "still", "src/index.ts", "ToneThumbnail", str(out), f"--props={work / 'props.json'}",
           "--scale=0.6667", "--log=error", f"--browser-executable={rb.browser_executable()}"]
    subprocess.run(cmd, cwd=rb.REMOTION_DIR, check=True)
    print("thumbnail ->", out)


if __name__ == "__main__":
    main()
