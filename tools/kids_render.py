"""Kids test 01: render the music video, the vertical Short and the thumbnail with Remotion (src/kids/index.ts).

    python tools/kids_render.py stills [t1,t2,...] [KidsSong|KidsShort]   QC contact sheet -> output/kids/test01/qc/
    python tools/kids_render.py video [start_frame end_frame]             silent picture (chunks allowed)
    python tools/kids_render.py light                                      concat chunks + mix -> output/kids_test01_light.mp4
    python tools/kids_render.py short                                      1080x1920 chorus Short (+ audio)
    python tools/kids_render.py thumb                                      1280x720 thumbnail

Large masters (silent chunks, full-quality video) are deleted after the light encode.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
import kids_song as S  # noqa: E402
from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable  # noqa: E402

WORK = ROOT / "output" / "kids" / "test01"
FPS = 30
ENTRY = "src/kids/index.ts"
LIGHT = ROOT / "output" / "kids_test01_light.mp4"
SHORT = ROOT / "output" / "kids_test01_short.mp4"
THUMB = ROOT / "output" / "kids_test01_thumb.png"
# Short: last two numbers of verse 2, the tag, the final chorus and the goodbye (bars 38..56 + tail)
SHORT_FROM_BAR = 38


def props(offset: float = 0.0, seconds: float | None = None) -> Path:
    tl = json.loads((WORK / "timeline.json").read_text())
    p = {"timeline": tl, "offset": offset, **({"seconds": seconds} if seconds else {})}
    out = WORK / f"props_{offset:.0f}.json"
    out.write_text(json.dumps(p, ensure_ascii=False))
    return out


def remotion(args: list[str], props_file: Path) -> None:
    cmd = ["npx", "remotion", *args, f"--props={props_file}", "--log=error", "--gl=angle", "--timeout=120000"]
    b = browser_executable()
    if b:
        cmd.append(f"--browser-executable={b}")
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)


def ff(*args: str) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def stills(times: list[float], comp: str = "KidsSong") -> Path:
    qc = WORK / "qc"
    qc.mkdir(parents=True, exist_ok=True)
    off = SHORT_FROM_BAR * S.BAR if comp == "KidsShort" else 0.0
    pf = props(off)
    pngs = []
    for t in times:
        png = qc / f"{comp}_{t:06.2f}.jpg"
        remotion(["still", ENTRY, comp, str(png), f"--frame={int(round((t - off) * FPS))}", "--image-format=jpeg",
                  "--scale=0.5"], pf)
        pngs.append(png)
    sheet = qc / f"{comp}_sheet.jpg"
    cols = 3 if comp == "KidsSong" else 4
    inputs = sum([["-i", str(p)] for p in pngs], [])
    n = len(pngs)
    while n % cols:
        inputs += ["-i", str(pngs[-1])]
        n += 1
    ff(*inputs, "-filter_complex", f"xstack=inputs={n}:grid={cols}x{n // cols}", "-frames:v", "1", str(sheet))
    print(sheet)
    return sheet


def video(a: int | None = None, b: int | None = None) -> Path:
    pf = props(0.0)
    total = int(round(S.duration_seconds() * FPS))
    a, b = (0, total - 1) if a is None else (a, min(b, total - 1))
    out = WORK / f"chunk_{a:05d}.mp4"
    remotion(["render", ENTRY, "KidsSong", str(out), "--codec=h264", "--crf=16", "--pixel-format=yuv420p", "--muted",
              "--concurrency=4", f"--frames={a}-{b}"], pf)
    print(out)
    return out


def light() -> Path:
    chunks = sorted(WORK.glob("chunk_*.mp4"))
    lst = WORK / "chunks.txt"
    lst.write_text("".join(f"file '{c}'\n" for c in chunks))
    ff("-f", "concat", "-safe", "0", "-i", str(lst), "-i", str(WORK / "mix.wav"), "-map", "0:v:0", "-map", "1:a:0",
       "-vf", "scale=1280:720:in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "30",
       "-tune", "animation", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", str(LIGHT))
    for c in chunks:
        c.unlink()
    lst.unlink()
    print(LIGHT, f"{LIGHT.stat().st_size / 1e6:.1f} MB")
    return LIGHT


def short() -> Path:
    off = SHORT_FROM_BAR * S.BAR
    secs = S.duration_seconds() - off
    pf = props(off, secs)
    master = WORK / "short_master.mp4"
    remotion(["render", ENTRY, "KidsShort", str(master), "--codec=h264", "--crf=16", "--pixel-format=yuv420p", "--muted",
              "--concurrency=4"], pf)
    ff("-i", str(master), "-ss", f"{off:.3f}", "-t", f"{secs:.3f}", "-i", str(WORK / "mix.wav"), "-map", "0:v:0", "-map", "1:a:0",
       "-af", "afade=t=in:d=0.25", "-vf", "scale=in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264",
       "-preset", "slow", "-crf", "26", "-tune", "animation", "-c:a", "aac", "-b:a", "128k", "-shortest",
       "-movflags", "+faststart", str(SHORT))
    master.unlink()
    print(SHORT, f"{secs:.1f}s", f"{SHORT.stat().st_size / 1e6:.1f} MB")
    return SHORT


def thumb() -> Path:
    pf = props(0.0)
    remotion(["still", ENTRY, "KidsThumb", str(THUMB), "--frame=0", "--image-format=png"], pf)
    print(THUMB)
    return THUMB


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        ts = [float(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 6, 10, 19, 27, 36, 44, 49, 62, 88, 106, 119]
        stills(ts, sys.argv[3] if len(sys.argv) > 3 else "KidsSong")
    elif cmd == "video":
        video(*(int(x) for x in sys.argv[2:4])) if len(sys.argv) > 3 else video()
    elif cmd == "light":
        light()
    elif cmd == "short":
        short()
    elif cmd == "thumb":
        thumb()
