"""Preview a CartoonStage world without a full build (new sets, items, characters).

  python tools/stage_preview.py sheet <scene.json> <out.jpg> <t1,t2,...> [--scale 0.5] [--cols 3]
      renders the world at the given times (seconds) into a contact sheet
  python tools/stage_preview.py clip <scene.json> <out.mp4> <start> <seconds> [--scale 0.5]
      renders a short motion test

scene.json holds CartoonStage params (zones, items, cam, tone...) with plain numbers (no narration cues).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from hiddeneco.render import remotion_bridge as rb  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["sheet", "clip"])
    ap.add_argument("scene"); ap.add_argument("out"); ap.add_argument("a"); ap.add_argument("b", nargs="?")
    ap.add_argument("--scale", default="0.5"); ap.add_argument("--cols", type=int, default=3)
    o = ap.parse_args()
    scene = json.loads(Path(o.scene).read_text())
    work = Path(tempfile.mkdtemp(prefix="stageprev_", dir=os.environ.get("STAGEPREV_DIR") or None))
    common = [f"--browser-executable={rb.browser_executable()}", "--log=error", f"--scale={o.scale}"]
    if o.mode == "sheet":
        times = [float(x) for x in o.a.split(",")]
        (work / "props.json").write_text(json.dumps({"scene": scene, "times": times}))
        subprocess.run(["npx", "remotion", "render", "src/index.ts", "StagePreview", str(work / "f"), f"--props={work/'props.json'}",
                        "--sequence", "--image-format=jpeg", "--concurrency=4", *common], cwd=rb.REMOTION_DIR, check=True)
        from PIL import Image, ImageDraw
        frames = sorted(glob.glob(str(work / "f" / "*.jpeg")))
        ims = [Image.open(f) for f in frames]
        w, h = ims[0].size; cols = min(o.cols, len(ims)); rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * w, rows * h), "black")
        for k, (im, tt) in enumerate(zip(ims, times)):
            sheet.paste(im, ((k % cols) * w, (k // cols) * h))
            ImageDraw.Draw(sheet).text(((k % cols) * w + 8, (k // cols) * h + 6), f"t={tt:.2f}", fill="white")
        sheet.save(o.out, quality=88); print(len(ims), "->", o.out)
    else:
        start, secs = float(o.a), float(o.b or 4)
        (work / "props.json").write_text(json.dumps({"scene": scene, "start": start, "seconds": secs}))
        subprocess.run(["npx", "remotion", "render", "src/index.ts", "StagePreview", str(Path(o.out).resolve()), f"--props={work/'props.json'}",
                        "--codec=h264", "--crf=26", "--concurrency=4", *common], cwd=rb.REMOTION_DIR, check=True)
        print("->", o.out)


if __name__ == "__main__":
    main()
