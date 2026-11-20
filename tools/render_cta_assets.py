"""Renders the channel's call-to-action assets (docs/CTA_STANDARD.md) from the Remotion compositions in
remotion/src/brand/SubscribeCTA.tsx:

  assets/brand/cta/subscribe_cta_1080.webm   SUBSCRIBE / LIKE widget, 760x260, VP9 with alpha, 4 s (for 1920x1080 films)
  assets/brand/cta/subscribe_cta_720.webm    the same scaled for 1280x720 films (506x174)
  assets/brand/cta/subscribe_cta_preview.png one frame of the widget on a mid-grey background (for review)
  assets/brand/cta/cta_card_subscribe.mp4    full-frame silent card (1920x1080, 5.5 s) used by tools/cta_retrofit.py

Overlay with FFmpeg (decode the alpha with libvpx-vp9):
    ffmpeg -i film.mp4 -c:v libvpx-vp9 -itsoffset 60 -i assets/brand/cta/subscribe_cta_720.webm \
           -filter_complex "[0:v][1:v]overlay=24:H-h-24:eof_action=pass" ...

Run: python tools/render_cta_assets.py [--card-seconds 5.5]
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable  # noqa: E402

OUT = ROOT / "assets" / "brand" / "cta"


def remotion(args: list[str]) -> None:
    cmd = ["npx", "remotion", *args, "--log=error"]
    b = browser_executable()
    if b:
        cmd.append(f"--browser-executable={b}")
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--card-seconds", type=float, default=5.5)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    big = OUT / "subscribe_cta_1080.webm"
    remotion(["render", "src/index.ts", "SubscribeCTA", str(big), "--codec=vp9", "--pixel-format=yuva420p",
              "--image-format=png", "--crf=30"])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-c:v", "libvpx-vp9", "-i", str(big), "-vf", "scale=506:174:flags=lanczos",
                    "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "0", "-crf", "32", "-auto-alt-ref", "0",
                    str(OUT / "subscribe_cta_720.webm")], check=True)
    remotion(["still", "src/index.ts", "SubscribeCTA", str(OUT / "_w.png"), "--frame=80"])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x6B7280:s=760x260", "-i", str(OUT / "_w.png"),
                    "-filter_complex", "[0:v][1:v]overlay=0:0", "-frames:v", "1", str(OUT / "subscribe_cta_preview.png")], check=True)
    (OUT / "_w.png").unlink()
    frames = int(round(a.card_seconds * 30))
    remotion(["render", "src/index.ts", "CTACard", str(OUT / "cta_card_subscribe.mp4"), "--codec=h264", "--crf=20", "--muted",
              f"--props={{\"kind\":\"subscribe\",\"seconds\":{a.card_seconds}}}", f"--frames=0-{frames - 1}"])
    for f in sorted(OUT.iterdir()):
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
