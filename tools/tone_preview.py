"""Representative still frames of an episode WITH its visual direction plan (and optionally without, for comparison).

  python tools/tone_preview.py <slug> <out.jpg> <scene_id,scene_id,...> [--at 0.6] [--plain] [--deliverable documentary]

No narration is generated: scene lengths are estimated from the text (14.5 chars/s), cues are timed accordingly, and
one frame per scene is rendered at fraction --at of its length. --plain ignores visual_direction.yaml (the "before").
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from hiddeneco import timing  # noqa: E402
from hiddeneco import visual_direction as vdir  # noqa: E402
from hiddeneco.config import project_paths  # noqa: E402
from hiddeneco.models import TimedScene  # noqa: E402
from hiddeneco.pipeline import format_cfg, load_deliverable, load_project, prepare, research  # noqa: E402
from hiddeneco.render import remotion_bridge as rb  # noqa: E402
from hiddeneco.script import render_text  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("out"); ap.add_argument("scenes")
    ap.add_argument("--at", type=float, default=0.6); ap.add_argument("--plain", action="store_true")
    ap.add_argument("--deliverable", default="documentary"); ap.add_argument("--scale", type=float, default=0.4)
    a = ap.parse_args()
    only = a.scenes.split(",")
    if a.plain:                                   # pretend there is no plan
        vdir.load = lambda *x, **k: None          # type: ignore
    p = project_paths(a.slug, deliverable=a.deliverable)
    d = research(p)
    sc, sb = prepare(p, d)
    deliv, _ = load_deliverable(p)
    fmt = format_cfg(deliv)
    proj = load_project(p)
    by = {s.id: s for s in sc.segments}
    timed, start = [], 0.0
    order = {sid: i for i, sid in enumerate(only)}
    for scn in sorted([s for s in sb.scenes if s.id in order], key=lambda s: order[s.id]):
        text = render_text(by[scn.segment].narration, d)
        speech = len(text) / 14.5 if text else 0.0
        dur = max(fmt["scene_lead_in"] + speech + fmt["scene_tail"], float(scn.params.get("min_seconds", 0)))
        words, t = [], fmt["scene_lead_in"]
        for s in timing.sentences(text):
            ds = len(s) / 14.5
            words += timing.word_timings(s, t, ds)
            t += ds
        timed.append(TimedScene(scene=scn, narration=text, audio_path="", audio_seconds=speech, start=start, duration=dur, words=words))
        start += dur
    credits = {ts.scene.id: [] for ts in timed}
    props = rb.build_props(timed, proj["style"], credits, fmt, 30, proj.get("remotion_geo", []))
    for s, ts in zip(props["scenes"], timed):
        s["preview_t"] = ts.duration * a.at
        s["frames"] = 1
    work = p.out_sub("work") / ("tone_preview_plain" if a.plain else "tone_preview")
    work.mkdir(parents=True, exist_ok=True)
    for f in glob.glob(str(work / "frames" / "*")):
        os.remove(f)
    (work / "props.json").write_text(json.dumps(props))
    cmd = ["npx", "remotion", "render", "src/index.ts", "Documentary", str(work / "frames"), f"--props={work / 'props.json'}",
           "--sequence", "--image-format=jpeg", f"--scale={a.scale}", "--concurrency=3", "--log=error",
           f"--browser-executable={rb.browser_executable()}"]
    subprocess.run(cmd, cwd=rb.REMOTION_DIR, check=True)
    frames = sorted(glob.glob(str(work / "frames" / "*.jpeg")))
    ims = [Image.open(f).convert("RGB") for f in frames]
    w, h = ims[0].size
    cols = 3
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 28)), "#111111")
    dr = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    for i, (im, ts) in enumerate(zip(ims, timed)):
        x, y = (i % cols) * w, (i // cols) * (h + 28)
        sheet.paste(im, (x, y + 28))
        tone = ts.scene.params.get("tone", "default")
        sh = ts.scene.params.get("toneShift")
        dr.text((x + 8, y + 4), f"{ts.scene.id} · {tone}" + (f" → {sh['to']}" if isinstance(sh, dict) else ""), fill="#FFFFFF", font=font)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=88)
    print(len(ims), "frames ->", a.out)


if __name__ == "__main__":
    main()
