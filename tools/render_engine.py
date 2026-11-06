"""Render the animation-engine demo and component previews (Remotion), with the world geometry as props.

    python tools/render_engine.py demo                 -> output/engine/engine_demo_30s.mp4
    python tools/render_engine.py previews             -> output/engine/previews/<Comp>.mp4
    python tools/render_engine.py stills <Comp> <frames,...> <out.jpg> [scale]   contact sheet of single frames
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable, ensure_installed  # noqa: E402

OUT = ROOT / "output" / "engine"
PREVIEWS = ["EnginePresenter", "EngineDraw", "EngineMap", "EngineFlow", "EngineCharts", "EngineChartsLine", "EngineExploded"]


def props_file() -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "props.json"
    geo = json.loads((ROOT / "assets" / "geo" / "remotion_world.json").read_text())
    p.write_text(json.dumps({"geo": geo}))
    return p


def remotion(args: list[str]) -> None:
    cmd = ["npx", "remotion", *args, f"--props={props_file()}", "--log=error", "--gl=angle"]
    b = browser_executable()
    if b:
        cmd.append(f"--browser-executable={b}")
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)


def render(comp: str, out: Path, concurrency: int = min(4, os.cpu_count() or 2)) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    remotion(["render", "src/index.ts", comp, str(out.resolve()), "--codec=h264", "--crf=17", "--pixel-format=yuv420p",
              "--muted", f"--concurrency={concurrency}"])
    return out


def stills(comp: str, frames: list[int], out: Path, scale: float = 0.33) -> Path:
    from PIL import Image
    tmp = OUT / "stills"
    tmp.mkdir(parents=True, exist_ok=True)
    ims = []
    for f in frames:
        png = tmp / f"{comp}_{f:04d}.jpeg"
        remotion(["still", "src/index.ts", comp, str(png.resolve()), f"--frame={f}", f"--scale={scale}", "--image-format=jpeg"])
        ims.append(Image.open(png))
    w, h = ims[0].size
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h))
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(out, quality=85)
    return out


if __name__ == "__main__":
    ensure_installed()
    mode = sys.argv[1]
    if mode == "demo":
        print(render("EngineDemo", OUT / "engine_demo_30s.mp4", 4))
    elif mode == "previews":
        for c in (sys.argv[2].split(",") if len(sys.argv) > 2 else PREVIEWS):
            print(render(c, OUT / "previews" / f"{c}.mp4", 4))
    elif mode == "stills":
        print(stills(sys.argv[2], [int(x) for x in sys.argv[3].split(",")], Path(sys.argv[4]), float(sys.argv[5]) if len(sys.argv) > 5 else 0.33))
