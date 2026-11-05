"""Insert the channel intro into an ALREADY RENDERED episode, without re-rendering it or touching the original.

The cut is made at a scene boundary (never inside a sentence): the end of the first scene whose cumulative
duration reaches --min-seconds (default 10), or the end of --after-segment. Audio: a 0.25 s fade on each side
of the cut, so the music bed does not jump. Subtitles after the cut are shifted by the intro length.

    python tools/splice_intro.py <episode.mp4> <timeline.json> <out.mp4> [--after-segment ID] [--min-seconds 10]
                                [--intro output/brand/the_hidden_economics_intro.mp4] [--srt in.srt]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def boundary(timeline: dict | list, after: str | None, min_s: float) -> tuple[float, str]:
    scenes = timeline["scenes"] if isinstance(timeline, dict) else timeline
    if any(s["scene"]["type"] == "channel_intro" for s in scenes):
        raise SystemExit("This episode already contains the channel intro: nothing to do (no duplicates).")
    for s in scenes:
        end = s["start"] + s["duration"]
        if (after and s["scene"]["segment"] == after) or (not after and end >= min_s and s.get("narration")):
            return end, s["scene"]["segment"]
    raise SystemExit("No suitable boundary found")


def shift_srt(src: Path, dst: Path, cut: float, by: float) -> None:
    def ts(x: float) -> str:
        h, r = divmod(x, 3600); m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}".replace(",1000", ",999")
    def parse(v: str) -> float:
        h, m, s = v.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    out = []
    for line in src.read_text(encoding="utf-8").splitlines():
        m = re.match(r"(\S+) --> (\S+)", line)
        if m:
            a, b = parse(m.group(1)), parse(m.group(2))
            if a >= cut - 0.01:
                a, b = a + by, b + by
            line = f"{ts(a)} --> {ts(b)}"
        out.append(line)
    dst.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("timeline"); ap.add_argument("out")
    ap.add_argument("--after-segment"); ap.add_argument("--min-seconds", type=float, default=10.0)
    ap.add_argument("--intro", default=str(ROOT / "output" / "brand" / "the_hidden_economics_intro.mp4"))
    ap.add_argument("--srt")
    a = ap.parse_args()
    src, out, intro = Path(a.video), Path(a.out), Path(a.intro)
    if out.resolve() == src.resolve():
        raise SystemExit("Refusing to overwrite the original render")
    cut, seg = boundary(json.loads(Path(a.timeline).read_text()), a.after_segment, a.min_seconds)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(intro)],
                               capture_output=True, text=True, check=True).stdout)
    f = 0.25
    fc = (
        f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS,format=yuv420p[v0];"
        f"[1:v]setpts=PTS-STARTPTS,format=yuv420p,fps=30[v1];"
        f"[0:v]trim=start={cut},setpts=PTS-STARTPTS,format=yuv420p[v2];"
        f"[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS,afade=t=out:st={cut - f}:d={f}[a0];"
        f"[1:a]aresample=48000,asetpts=PTS-STARTPTS[a1];"
        f"[0:a]atrim=start={cut},asetpts=PTS-STARTPTS,afade=t=in:st=0:d={f}[a2];"
        f"[v0][a0][v1][a1][v2][a2]concat=n=3:v=1:a=1[v][a]"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-i", str(intro), "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-color_range", "tv",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)], check=True)
    if a.srt:
        shift_srt(Path(a.srt), out.with_suffix(".srt"), cut, dur)
    print(json.dumps({"out": str(out), "intro_after_segment": seg, "cut_s": round(cut, 2), "intro_s": dur}))


if __name__ == "__main__":
    main()
