"""Remotion (React + SVG) renderer backend.

The Python pipeline still owns research, script, narration, timing, audio, QC and packaging. For a project
with `renderer: remotion` in project.yaml, scenes are drawn by the Remotion project in `remotion/`:
Python writes a props JSON (scenes with params, narration word timings and durations, palette, map layers),
Remotion renders the silent H.264 picture, and FFmpeg muxes the narration/music mix as AAC.
"""
from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
from pathlib import Path

from hiddeneco.config import REPO_ROOT
from hiddeneco.logging_setup import log
from hiddeneco.models import TimedScene

REMOTION_DIR = REPO_ROOT / "remotion"
GEO_DIR = REPO_ROOT / "assets" / "geo"


def browser_executable() -> str | None:
    """A local Chrome Headless Shell if one is installed (avoids a download); else Remotion fetches its own."""
    env = os.environ.get("REMOTION_BROWSER")
    if env:
        return env
    hits = sorted(glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"))
    return hits[-1] if hits else None


def build_props(timed: list[TimedScene], style: dict, credits: dict[str, list[str]], fmt: dict, fps: int,
                geo_layers: list[str]) -> dict:
    fonts = style.get("web_fonts") or {"display": "Inter Display, Inter, sans-serif", "body": "Inter, sans-serif"}
    scenes = []
    for ts in timed:
        scenes.append({
            "id": ts.scene.id, "type": ts.scene.type, "params": ts.scene.params, "narration": ts.narration,
            "duration": ts.duration, "lead": fmt["scene_lead_in"] if ts.audio_seconds else 0.0,
            "speech": max(0.1, ts.audio_seconds or ts.duration), "words": ts.words,
            "credits": credits.get(ts.scene.id, []), "chapter": ts.scene.params.get("chapter", ""),
        })
    geo = {name: json.loads((GEO_DIR / f"remotion_{name}.json").read_text()) for name in geo_layers}
    return {"fps": fps, "width": fmt["width"], "height": fmt["height"], "palette": style["palette"], "fonts": fonts,
            "brand": "The Hidden Economics", "scenes": scenes, "geo": geo,
            "transition": style.get("transition", "fade"), "background": style.get("background", "grid")}


def ensure_installed() -> None:
    if not shutil.which("npx"):
        raise RuntimeError("Node.js/npx not found: install Node 18+ to use the Remotion renderer")
    if not (REMOTION_DIR / "node_modules" / "remotion").exists():
        log("remotion.install", dir=str(REMOTION_DIR))
        subprocess.run(["npm", "ci" if (REMOTION_DIR / "package-lock.json").exists() else "install", "--no-audit",
                        "--no-fund", "--loglevel=error"], cwd=REMOTION_DIR, check=True)


def render_video(props: dict, work: Path, out_mp4: Path, concurrency: int = 4, crf: int = 18,
                 frames: str | None = None) -> Path:
    """Render the silent picture with Remotion. `frames` e.g. '0-299' renders a range (previews)."""
    ensure_installed()
    work.mkdir(parents=True, exist_ok=True)
    props_path = work / "remotion_props.json"
    props_path.write_text(json.dumps(props), encoding="utf-8")
    cmd = ["npx", "remotion", "render", "src/index.ts", "Documentary", str(out_mp4.resolve()),
           f"--props={props_path.resolve()}", "--codec=h264", f"--crf={crf}", "--muted", "--pixel-format=yuv420p",
           f"--concurrency={concurrency}", "--log=error", "--timeout=120000", "--gl=angle"]
    if frames:
        cmd.append(f"--frames={frames}")
    b = browser_executable()
    if b:
        cmd.append(f"--browser-executable={b}")
    log("remotion.render", scenes=len(props["scenes"]), out=str(out_mp4))
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)
    return out_mp4


def mux(video: Path, audio: Path, out_mp4: Path, crf: int = 18) -> Path:
    """Final encode: Remotion's JPEG frames come out as full-range yuvj420p; convert to standard limited-range
    yuv420p BT.709 H.264 (what YouTube and most players expect) and add the AAC mix."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-i", str(audio),
                    "-map", "0:v:0", "-map", "1:a:0",
                    "-vf", "scale=in_range=full:out_range=tv,format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-profile:v", "high",
                    "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-ar", "48000", "-shortest", "-movflags", "+faststart",
                    str(out_mp4)], check=True)
    return out_mp4
