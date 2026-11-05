"""Render the `remotion_thumbnails` of a deliverable as 1280x720 PNGs with the Remotion engine.

    python tools/render_remotion_thumbnails.py <slug> <deliverable> [--copy-to output/norway_thumbnail_{id}.png]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hiddeneco.config import project_paths  # noqa: E402
from hiddeneco.pipeline import prepare, research  # noqa: E402
from hiddeneco.render import remotion_bridge as rb  # noqa: E402
from hiddeneco.script import render_value  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("deliverable"); ap.add_argument("--copy-to")
    a = ap.parse_args()
    p = project_paths(a.slug, deliverable=a.deliverable)
    d = research(p)
    sc, sb = prepare(p, d)
    proj = yaml.safe_load((p.project_dir / "project.yaml").read_text())
    raw = yaml.safe_load((p.deliverable_dir / "deliverable.yaml").read_text())
    thumbs = render_value(raw.get("remotion_thumbnails", []), d)
    scenes = {s.id: s for s in sb.scenes}
    style = proj["style"]
    geo = {n: json.loads((rb.GEO_DIR / f"remotion_{n}.json").read_text()) for n in proj.get("remotion_geo", [])}
    out_dir = p.out_sub("thumbnails")
    rb.ensure_installed()
    md = ["# Thumbnail candidates (Remotion)", ""]
    for th in thumbs:
        s = scenes[th["scene"]]
        # keep the picture, drop the scene's own text overlays (the thumbnail has its own headline)
        params = {k: v for k, v in s.params.items()
                  if k not in ("title", "kicker", "subtitle", "value", "callouts", "labels", "chapter")}
        params["markers"] = [{k: v for k, v in m.items() if k != "sublabel"} for m in params.get("markers", [])]
        params["arcs"] = [{k: v for k, v in a.items() if k not in ("label", "value")} for a in params.get("arcs", [])]
        params.update(th.get("params", {}))
        spec = {"id": s.id, "type": s.type, "params": {**params, "no_chrome": True}, "narration": "", "duration": 30.0,
                "lead": 0.0, "speech": 1.0, "words": [], "credits": [], "chapter": ""}
        props = {"fps": 30, "width": 1920, "height": 1080, "palette": style["palette"],
                 "fonts": style.get("web_fonts", {"display": "Inter Display, Inter, sans-serif", "body": "Inter, sans-serif"}),
                 "brand": "The Hidden Economics", "scenes": [spec], "geo": geo,
                 "thumb": {"scene": spec, "at": float(th.get("at", 3)), "headline": th["headline"], "kicker": th.get("kicker"),
                           "footer": th.get("footer"), "side": th.get("side", "left"), "accent_line": th.get("accent_line", -1)}}
        props_path = p.out_sub("work") / f"thumb_{th['id']}.json"
        props_path.write_text(json.dumps(props))
        out = out_dir / f"thumb_{th['id']}.png"
        cmd = ["npx", "remotion", "still", "src/index.ts", "Thumbnail", str(out.resolve()), f"--props={props_path.resolve()}",
               "--scale=0.6666667", "--image-format=png", "--log=error"]
        b = rb.browser_executable()
        if b:
            cmd.append(f"--browser-executable={b}")
        subprocess.run(cmd, cwd=rb.REMOTION_DIR, check=True)
        md.append(f"- **{out.name}** (1280x720) - {th.get('why', '')}")
        if a.copy_to:
            dst = Path(a.copy_to.format(id=th["id"]))
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(out.read_bytes())
        print(out)
    (out_dir / "thumbnails_remotion.md").write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
