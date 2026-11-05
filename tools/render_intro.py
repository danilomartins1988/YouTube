"""Render the standalone channel intro: Remotion composition "Intro" (5 s, 1920x1080) + the synthesised sonic
signature, muxed to H.264/AAC.

    python tools/render_intro.py [out.mp4]        (default output/brand/the_hidden_economics_intro.mp4)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.intro import ensure_signature  # noqa: E402
from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable, ensure_installed  # noqa: E402


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "output" / "brand" / "the_hidden_economics_intro.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    ensure_installed()
    silent = out.with_name(out.stem + "_silent.mp4")
    cmd = ["npx", "remotion", "render", "src/index.ts", "Intro", str(silent.resolve()), "--codec=h264", "--crf=16",
           "--muted", "--pixel-format=yuv420p", "--log=error", "--gl=angle"]
    b = browser_executable()
    if b:
        cmd.append(f"--browser-executable={b}")
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)
    wav = ensure_signature()
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=7", "-t", "5", "-movflags", "+faststart", str(out)], check=True)
    silent.unlink(missing_ok=True)
    print(out)


if __name__ == "__main__":
    main()
