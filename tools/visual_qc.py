"""Visual and audio QC for a finished episode (mandatory from Episode 06).

Produces, next to <out_dir>/:
  sheet_sampled.jpg      a frame every N seconds across the whole film
  sheet_opening.jpg      the first 30 s, one frame every 2 s
  sheet_<scene>.jpg      four frames (20/45/70/95 %) of each listed scene (e.g. signature animations)
  visual_qc.json         safe-margin check, near-duplicate frame check, audio peak / silence / clipping

    python tools/visual_qc.py <video.mp4> <timeline.json> <out_dir> [--scenes id1,id2] [--every 20]

Technical checks cannot prove an animation is meaningful: the sheets exist so a person (or a model with
vision) can look at every part of the film.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageStat


def frame(video: Path, t: float, w: int = 640) -> Image.Image:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={w}:-1",
                          "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True, check=True).stdout
    from io import BytesIO
    return Image.open(BytesIO(raw)).convert("RGB")


def sheet(frames: list[tuple[str, Image.Image]], cols: int, out: Path) -> None:
    w, h = frames[0][1].size
    rows = (len(frames) + cols - 1) // cols
    s = Image.new("RGB", (cols * w, rows * (h + 22)), "#000")
    d = ImageDraw.Draw(s)
    for i, (label, im) in enumerate(frames):
        x, y = (i % cols) * w, (i // cols) * (h + 22)
        s.paste(im, (x, y + 22))
        d.text((x + 6, y + 4), label, fill="#fff")
    s.save(out, quality=85)


def margin_ink(im: Image.Image, frac: float = 0.025) -> float:
    """Share of bright 'ink' pixels in the outer safe-margin band (text bleeding off-frame shows up here)."""
    g = im.convert("L")
    w, h = g.size
    m = int(min(w, h) * frac)
    bands = [g.crop((0, 0, w, m)), g.crop((0, h - m, w, h)), g.crop((0, 0, m, h)), g.crop((w - m, 0, w, h))]
    bright = sum(sum(1 for p in b.getdata() if p > 200) for b in bands)
    total = sum(b.size[0] * b.size[1] for b in bands)
    return bright / total


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("timeline"); ap.add_argument("out_dir")
    ap.add_argument("--scenes", default=""); ap.add_argument("--every", type=float, default=20.0)
    a = ap.parse_args()
    video, out = Path(a.video), Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tl = json.loads(Path(a.timeline).read_text())
    scenes = tl["scenes"] if isinstance(tl, dict) else tl
    total = scenes[-1]["start"] + scenes[-1]["duration"]
    report: dict = {"video": str(video), "duration_s": round(total, 2)}

    # 1. sampled frames across the film + margin and duplicate checks
    sampled, prev, dup, margins = [], None, [], []
    t = 2.0
    while t < total - 1:
        im = frame(video, t)
        sampled.append((f"{int(t // 60)}:{int(t % 60):02d}", im))
        margins.append((round(t, 1), round(margin_ink(im), 4)))
        if prev is not None:
            diff = ImageStat.Stat(ImageChops.difference(im, prev).convert("L")).mean[0]
            if diff < 1.0:
                dup.append(round(t, 1))
        prev = im
        t += a.every
    sheet(sampled, 6, out / "sheet_sampled.jpg")
    report["sampled_frames"] = len(sampled)
    report["near_identical_consecutive_samples"] = dup
    report["safe_margin_ink_max"] = max(m for _, m in margins) if margins else 0
    report["safe_margin_flags"] = [t for t, m in margins if m > 0.01]

    # 2. opening sequence
    sheet([(f"{t:.0f}s", frame(video, t)) for t in range(0, 30, 2)], 5, out / "sheet_opening.jpg")

    # 3. chosen scenes (signature animations)
    for sid in [s for s in a.scenes.split(",") if s]:
        ts = next(x for x in scenes if x["scene"]["id"] == sid)
        fr = [(f"{sid} {int(f * 100)}%", frame(video, ts["start"] + ts["duration"] * f, 960)) for f in (0.2, 0.45, 0.7, 0.95)]
        sheet(fr, 2, out / f"sheet_{sid}.jpg")

    # 4. audio: peak, clipping, long silences
    vd = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-af", "volumedetect,silencedetect=n=-45dB:d=2.5", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    mx = re.search(r"max_volume: (-?[\d.]+) dB", vd)
    report["audio_max_volume_db"] = float(mx.group(1)) if mx else None
    report["audio_clipping"] = bool(mx and float(mx.group(1)) >= -0.1)
    report["audio_silences_over_2_5s"] = [round(float(x), 1) for x in re.findall(r"silence_start: ([\d.]+)", vd)]
    (out / "visual_qc.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
