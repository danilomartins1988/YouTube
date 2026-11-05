"""Render the presenter demonstration scene (no narration): the character walks in, draws a flowchart,
writes labels, points at a bottleneck, reacts, then builds a bar chart and points at the result.

    python tools/render_presenter_demo.py [out.mp4] [--stills N]   (stills: N evenly spaced frames to a sheet)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable, ensure_installed  # noqa: E402

PALETTE = {"bg": "#0A1120", "bg2": "#121B2D", "ink": "#F2F5F9", "muted": "#8C98AD", "land": "#18233A", "border": "#2A3854",
           "accent": "#D9B25F", "accent2": "#2FB4FF", "accent3": "#E8B64C", "risk": "#FF5A5F"}

DEMO_ITEMS = [
    {"text": "HOW A PRODUCT REACHES CUSTOMERS", "x": 560, "y": 230, "size": 34, "colour": "accent3"},
    {"box": [560, 300, 250, 110], "label": "DESIGN", "colour": "accent2"},
    {"arrow": [[820, 355], [960, 355]], "bend": 0.0, "colour": "ink"},
    {"box": [970, 300, 250, 110], "label": "FACTORY", "colour": "accent2"},
    {"arrow": [[1230, 355], [1370, 355]], "bend": 0.0, "colour": "ink"},
    {"box": [1380, 300, 300, 110], "label": "PACKAGING", "colour": "risk", "size": 30},
    {"point": [1530, 420], "label": "Bottleneck", "colour": "risk", "hold": 1.6},
    {"react": True},
    {"bars": [{"label": "Y1", "value": 2}, {"label": "Y2", "value": 3}, {"label": "Y3", "value": 5}, {"label": "Y4", "value": 9}],
     "x": 600, "base": 860, "width": 900, "max_h": 330, "colour": "accent"},
    {"point": [1390, 520], "label": "Fastest growth", "colour": "accent3", "hold": 1.4},
]


def props(seconds: float = 18.0) -> dict:
    scene = {"id": "presenter_demo", "type": "presenter", "params": {"items": DEMO_ITEMS, "exit": {"at": 0.97}},
             "narration": "", "duration": seconds, "lead": 0.4, "speech": seconds - 1.0, "words": [], "credits": [], "chapter": ""}
    return {"fps": 30, "width": 1920, "height": 1080, "palette": PALETTE,
            "fonts": {"display": "Inter Display, Inter, sans-serif", "body": "Inter, sans-serif"},
            "brand": "The Hidden Economics", "scenes": [scene], "geo": {}, "transition": "fade", "background": "grid"}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = Path(args[0]) if args else ROOT / "output" / "brand" / "presenter_demo.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    ensure_installed()
    pj = out.with_suffix(".props.json")
    pj.write_text(json.dumps(props()))
    b = browser_executable()
    extra = [f"--browser-executable={b}"] if b else []
    if "--stills" in sys.argv:
        n = int(sys.argv[sys.argv.index("--stills") + 1])
        from PIL import Image
        ims = []
        for k in range(n):
            f = int((k + 0.5) / n * 18 * 30)
            png = out.with_name(f"{out.stem}_f{f}.jpg")
            subprocess.run(["npx", "remotion", "still", "src/index.ts", "Documentary", str(png.resolve()), f"--props={pj.resolve()}",
                            f"--frame={f}", "--scale=0.5", "--log=error", "--gl=angle", *extra], cwd=REMOTION_DIR, check=True)
            ims.append(Image.open(png))
        w, h = ims[0].size
        cols = 4
        sheet = Image.new("RGB", (cols * w, ((n + cols - 1) // cols) * h))
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % cols) * w, (i // cols) * h))
        sheet.save(out.with_name(out.stem + "_sheet.jpg"), quality=85)
        print(out.with_name(out.stem + "_sheet.jpg"))
        return
    subprocess.run(["npx", "remotion", "render", "src/index.ts", "Documentary", str(out.resolve()), f"--props={pj.resolve()}",
                    "--codec=h264", "--crf=18", "--muted", "--pixel-format=yuv420p", "--log=error", "--gl=angle", *extra],
                   cwd=REMOTION_DIR, check=True)
    print(out)


if __name__ == "__main__":
    main()
