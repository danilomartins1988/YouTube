"""Retrofit the channel call to action (docs/CTA_STANDARD.md) into finished, not-yet-published LIGHT videos
(output/<name>_light.mp4, 1280x720) whose masters are gone, without re-rendering the film.

For each film:
  1. a narrated CTA clip (full-frame animated SUBSCRIBE / LIKE card + one generic line, gpt-4o-mini-tts, voice "ash" for
     documentaries, "alloy" for the Before You Buy series, -16 LUFS) is SPLICED in right before the channel intro
     (the "vinheta"; start time from output/<slug>/<deliverable>/timeline.json), with 0.25 s audio fades at both joins;
  2. the corner SUBSCRIBE / LIKE overlay (assets/brand/cta/subscribe_cta_720.webm, 4 s) is laid over the picture
     25 s before the end, in the lower corner with less on-screen detail;
  3. the episode's docs are shifted by the inserted length after the insertion point: subtitles_en.srt (plus a cue for
     the CTA line), youtube-package/chapters.txt and description.txt, and the chapter lines of youtube_package.md
     (the first chapter stays at 0:00); description.txt / youtube_package.md also get the subscribe line.

Encode: same settings as the lights (scale=1280:720, libx264 -preset slow -crf 32 -tune animation, +faststart); the
audio is re-encoded (AAC 80k, as tools' post step) because the splice changes it. Writes to the scratch dir first,
checks the duration (old + clip), then replaces in place. Resumable: files logged as `done` are skipped, and a film
whose duration already equals old + clip is treated as spliced.

Run (foreground, a few files per call):
    python tools/cta_retrofit.py clip                 # build the two narrated clips (cents of TTS, cached)
    python tools/cta_retrofit.py run aimfg europeai    # or: run --next 3 (next three not yet done from UNPOSTED)
    python tools/cta_retrofit.py status
Env: CTA_SCRATCH (temp dir), CTA_LOG (log file).
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.cta import DESCRIPTION_LINE, SUBSCRIBE_LINE  # noqa: E402

CTA = ROOT / "assets" / "brand" / "cta"
OVERLAY = CTA / "subscribe_cta_720.webm"
SCRATCH = Path(os.environ.get("CTA_SCRATCH", "/tmp/cta_retrofit"))
LOG = Path(os.environ.get("CTA_LOG", str(SCRATCH / "cta_retrofit.log")))
LEAD, TAIL, FADE, END_OFFSET = 0.45, 0.6, 0.25, 25.0

# Long films with a light copy that were NOT public on 2026-11-20 (public channel pages read that day: the 30 newest
# long videos, which reach back past every candidate below, plus docs/UPLOAD_KIT/published.json of 2026-11-10).
# Left out: films already public, and superseded cuts that will not be published (costco = Ep 32 -> Ep 57,
# housing = Ep 31 -> Ep 58, taiwan = Ep 07 -> 07-taiwan-v2, nvidia_* = Ep 06 variants).
UNPOSTED = ["bybnvda", "bybant", "bybamzn", "costco_v2", "usdebt", "aimfg", "europeai", "robotsrich", "aipowerbill",
            "japanai", "powernewoil", "shovels", "aitaxes", "canadaai", "brazilai",
            "memory", "chip_chemicals", "healthcare", "oil", "quibi", "debeers", "prime", "bigtech", "creditcard",
            "visamc", "nickel", "autoins", "dealers", "mcdonalds", "studentdebt", "power", "airports", "grocery",
            "penny", "gold", "predmkt", "overdraft", "college", "mfglobal"]


def sh(cmd: list[str], **kw) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        raise SystemExit(f"failed: {' '.join(cmd[:8])} ...\n{r.stderr[-2000:]}")
    return r.stdout


def duration(p: Path) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def log(name: str, status: str, **kw) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "name": name, "status": status, **kw}) + "\n")


def done_names() -> set[str]:
    if not LOG.exists():
        return set()
    return {j["name"] for j in map(json.loads, LOG.read_text().splitlines()) if j.get("status") == "done"}


# ------------------------------------------------------------------------------------------------ mapping
def film_info(name: str) -> dict:
    """light name -> slug, deliverable, timeline, docs dir."""
    import yaml
    for d in glob.glob(str(ROOT / "projects" / "*" / "deliverables" / "*" / "deliverable.yaml")):
        alias = (yaml.safe_load(Path(d).read_text()) or {}).get("output_alias", "")
        if alias and Path(alias).stem == f"{name}_documentary":
            slug, dv = Path(d).parts[-4], Path(d).parts[-2]
            docs = None
            for f in glob.glob(str(ROOT / "docs" / "episodes" / "*" / "youtube-package" / "PACKAGE_STATUS.json")):
                if json.loads(Path(f).read_text()).get("slug") == slug:
                    docs = Path(f).parents[1]
            tl = json.loads((ROOT / "output" / slug / dv / "timeline.json").read_text())
            tl = tl["scenes"] if isinstance(tl, dict) else tl
            intro = next((s["start"] for s in tl if s["scene"]["type"] == "channel_intro"), None)
            return {"name": name, "slug": slug, "deliverable": dv, "docs": docs, "intro": intro,
                    "total": tl[-1]["start"] + tl[-1]["duration"], "voice": "alloy" if name.startswith("byb") else "ash",
                    "light": ROOT / "output" / f"{name}_documentary_light.mp4"}
    raise SystemExit(f"no project with output_alias output/{name}_documentary.mp4")


# ------------------------------------------------------------------------------------------------ clip
def voice_options(voice: str) -> dict:
    import yaml
    from hiddeneco.config import settings
    o = dict(settings()["tts"]["providers"]["openai"])
    o["voice"] = voice
    if voice == "alloy":   # the Before You Buy voice direction (series standard)
        p = yaml.safe_load((ROOT / "projects" / "before-you-buy-anthropic-2026-11" / "project.yaml").read_text())
        o["instructions"] = p["tts_overrides"]["openai"]["instructions"]
    return o


def build_clip(voice: str, force: bool = False) -> Path:
    out = CTA / f"cta_clip_{voice}_720.mp4"
    if out.exists() and not force:
        return out
    from hiddeneco.audio import RATE, music_bed, write_wav
    from hiddeneco.tts.providers import OpenAIProvider
    SCRATCH.mkdir(parents=True, exist_ok=True)
    wav = CTA / f"cta_voice_{voice}.wav"
    if not wav.exists() or force:
        tts = OpenAIProvider(voice_options(voice))
        secs = tts.synthesize(SUBSCRIBE_LINE, wav)
        print(f"tts {voice}: {secs:.2f} s, {len(SUBSCRIBE_LINE)} chars (~${len(SUBSCRIBE_LINE) / 1000 * 0.03:.4f})")
    import wave
    with wave.open(str(wav)) as w:
        speech = w.getnframes() / w.getframerate()
        v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    dur = round((LEAD + speech + TAIL) * 30) / 30
    card = SCRATCH / f"cta_card_{voice}.mp4"
    from hiddeneco.render.remotion_bridge import REMOTION_DIR, browser_executable
    cmd = ["npx", "remotion", "render", "src/index.ts", "CTACard", str(card), "--codec=h264", "--crf=16", "--muted", "--log=error",
           f"--props={json.dumps({'kind': 'subscribe', 'seconds': dur})}"]
    if browser_executable():
        cmd.append(f"--browser-executable={browser_executable()}")
    subprocess.run(cmd, cwd=REMOTION_DIR, check=True)
    n = int(dur * RATE)
    mixv = np.zeros(n, dtype=np.float32)
    s = int(LEAD * RATE)
    mixv[s:s + len(v)] += v[: n - s]
    bed = music_bed(dur, RATE) * 0.05
    mixv += bed[:n]
    raw = SCRATCH / f"cta_mix_{voice}.wav"
    write_wav(raw, mixv, RATE)
    # two-pass loudnorm to -16 LUFS integrated (the films measure about -16.3)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(raw), "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
          f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(card), "-i", str(raw), "-map", "0:v", "-map", "1:a",
        "-vf", "scale=1280:720:flags=lanczos,fps=30,format=yuv420p", "-af", f"{ln},aresample=48000", "-ac", "2",
        "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-tune", "animation", "-c:a", "aac", "-b:a", "192k",
        "-t", f"{dur:.3f}", "-movflags", "+faststart", str(out)])
    print(f"clip {out.relative_to(ROOT)}: {duration(out):.3f} s")
    return out


# ------------------------------------------------------------------------------------------------ corner choice
def busy(light: Path, at: float, corner: str, lift: int = 24) -> float:
    """Clutter score of the 506x174 lower-corner box over the 4 s window: edge density, plus a heavy penalty for
    caption pills (the older films' yellow lower-third captions) so the overlay never sits on a caption."""
    x = 24 if corner == "left" else 1280 - 506 - 24
    vals = []
    for k in (0.2, 1.3, 2.4, 3.5, 4.1):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{at + k:.2f}", "-i", str(light), "-frames:v", "1",
                              "-vf", f"crop=546:194:{max(0, x - 20)}:{720 - 174 - lift - 10},format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
        if len(raw) < 546 * 194 * 3:
            continue
        a = np.frombuffer(raw, dtype=np.uint8).reshape(194, 546, 3).astype(np.float32)
        g = a.mean(axis=2)
        edge = float(np.abs(np.diff(g, axis=1)).mean() + np.abs(np.diff(g, axis=0)).mean())
        r, gg, b = a[..., 0], a[..., 1], a[..., 2]
        lum = g
        pill = float(((r > 190) & (gg > 150) & (b < 120)).mean()          # yellow caption pills
                     + ((lum > 215)).mean()                               # white caption pills / bright text
                     + ((r > 190) & (gg < 120) & (b < 120)).mean())       # red caption pills
        vals.append(edge + 300 * pill)
    return float(np.mean(vals)) if vals else 1e9


def place_end_overlay(light: Path, old: float) -> tuple[float, str, int, float]:
    """(seconds before the end in the ORIGINAL film, corner, lift in px from the bottom, score): the cleanest lower
    corner and moment around 25 s before the end (tries 22-41 s); lifted above the caption band (lift 110) only when
    a caption pill fills both bottom corners."""
    best = None
    for off in (25.0, 22.0, 29.0, 33.0, 37.0, 41.0):
        for corner in ("right", "left"):
            for lift, pen in ((24, 0.0), (110, 1.5)):
                sc = busy(light, old - off, corner, lift) + 0.1 * abs(off - 25.0) + pen   # prefer ~25 s before the end
                if best is None or sc < best[3] - 0.5:
                    best = (off, corner, lift, sc)
    return best


# ------------------------------------------------------------------------------------------------ docs
def _ts(s: str) -> float:
    p = [int(x) for x in s.split(":")]
    return p[0] * 60 + p[1] if len(p) == 2 else p[0] * 3600 + p[1] * 60 + p[2]


def _fmt(t: float, like: str) -> str:
    t = int(round(t))
    if like.count(":") == 2 or t >= 3600:
        return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"
    return f"{t // 60}:{t % 60:02d}"


def shift_chapter_lines(text: str, at: float, d: float) -> str:
    def rep(m):
        t = _ts(m.group(1))
        return (_fmt(t + d, m.group(1)) if t > 0 and t >= at - 0.5 else m.group(1)) + m.group(2)
    return re.sub(r"(?m)^(\d{1,2}:\d{2}(?::\d{2})?)(\s)", rep, text)


def srt_time(s: str) -> float:
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def srt_fmt(t: float) -> str:
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms % 3600000 // 60000:02d}:{ms % 60000 // 1000:02d},{ms % 1000:03d}"


def shift_srt(path: Path, at: float, d: float, line: str, line_start: float, line_end: float) -> None:
    blocks = [b for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()) if b.strip()]
    cues = []
    for b in blocks:
        ls = b.strip().splitlines()
        a, b2 = [x.strip() for x in ls[1].split("-->")]
        s, e = srt_time(a), srt_time(b2)
        if s >= at - 0.01:
            s, e = s + d, e + d
        elif e > at:
            e = at
        cues.append((s, e, "\n".join(ls[2:])))
    cues.append((line_start, line_end, line))
    cues.sort(key=lambda c: c[0])
    path.write_text("\n\n".join(f"{i}\n{srt_fmt(s)} --> {srt_fmt(e)}\n{t}" for i, (s, e, t) in enumerate(cues, 1)) + "\n", encoding="utf-8")


def add_subscribe_line(desc: str) -> str:
    if "Subscribe to The Hidden Economics" in desc:
        return desc
    lines = desc.rstrip("\n").split("\n")
    k = len(lines) - 1 if lines and lines[-1].lstrip().startswith("#") else len(lines)
    new = lines[:k] + ([""] if k and lines[k - 1].strip() else []) + [DESCRIPTION_LINE, ""] + lines[k:]
    out = "\n".join(new).replace("\n\n\n", "\n\n") + "\n"
    return out if len(out) <= 5000 else desc


def retrofit_docs(info: dict, at: float, d: float, speech_start: float, speech_end: float) -> list[str]:
    docs, changed = info["docs"], []
    if docs is None:
        return changed
    srt = docs / "subtitles_en.srt"
    if srt.exists():
        shift_srt(srt, at, d, SUBSCRIBE_LINE, speech_start, speech_end)
        changed.append(str(srt.relative_to(ROOT)))
    pkg = docs / "youtube-package"
    for f in (pkg / "chapters.txt", pkg / "description.txt", docs / "youtube_package.md"):
        if not f.exists():
            continue
        t0 = f.read_text(encoding="utf-8")
        t = shift_chapter_lines(t0, at, d)
        if f.name == "description.txt":
            t = add_subscribe_line(t)
        if f.name == "youtube_package.md":
            desc = (pkg / "description.txt").read_text(encoding="utf-8") if (pkg / "description.txt").exists() else ""
            tagline = desc.rstrip().split("\n")[-1] if desc.strip() else ""
            if DESCRIPTION_LINE in desc and DESCRIPTION_LINE not in t and tagline.startswith("#") and t.count(tagline) == 1:
                t = t.replace(tagline, DESCRIPTION_LINE + "\n\n" + tagline)
        if t != t0:
            f.write_text(t, encoding="utf-8")
            changed.append(str(f.relative_to(ROOT)))
    return changed


# ------------------------------------------------------------------------------------------------ splice
def retrofit(name: str) -> dict:
    info = film_info(name)
    light, clip = info["light"], build_clip(info["voice"])
    D = round(duration(clip) * 30) / 30
    old = duration(light)
    T = round((info["intro"] if info["intro"] is not None else 35.0) * 30) / 30
    if abs(old - (info["total"] + D)) < 0.15:   # spliced by an interrupted run: finish the docs once, then log
        srt = info["docs"] / "subtitles_en.srt" if info["docs"] else None
        changed = [] if (srt and srt.exists() and SUBSCRIBE_LINE in srt.read_text()) else retrofit_docs(info, T, D, T + LEAD, T + D - TAIL + 0.1)
        log(name, "done", slug=info["slug"], cta_at=round(T, 3), clip_s=D, new_s=round(old, 3), docs=changed, note="resumed")
        return {"name": name, "skipped": "already spliced (duration = timeline + clip)", "docs": changed}
    if abs(old - info["total"]) > 0.15:
        raise SystemExit(f"{name}: light {old:.2f}s does not match its timeline {info['total']:.2f}s")
    off, corner, lift, score = place_end_overlay(light, old)
    E = old + D - off
    x = "24" if corner == "left" else "W-w-24"
    SCRATCH.mkdir(parents=True, exist_ok=True)
    tmp = SCRATCH / f"{name}_cta_tmp.mp4"
    fc = (f"[0:v]split[v0][v1];[v0]trim=end={T:.4f},setpts=PTS-STARTPTS[va];[v1]trim=start={T:.4f},setpts=PTS-STARTPTS[vb];"
          f"[0:a]asplit[a0][a1];[a0]atrim=end={T:.4f},asetpts=PTS-STARTPTS,afade=t=out:st={T - FADE:.4f}:d={FADE}[aa];"
          f"[a1]atrim=start={T:.4f},asetpts=PTS-STARTPTS,afade=t=in:d={FADE}[ab];"
          f"[1:v]fps=30,format=yuv420p,setsar=1[vc];[1:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,"
          f"afade=t=in:d=0.08,afade=t=out:st={D - FADE:.4f}:d={FADE}[ac];"
          f"[va][aa][vc][ac][vb][ab]concat=n=3:v=1:a=1[cv][ca];"
          f"[2:v]setpts=PTS+{E:.4f}/TB[ov];[cv][ov]overlay={x}:H-h-{lift}:eof_action=pass,scale=1280:720[outv]")
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(light), "-i", str(clip), "-c:v", "libvpx-vp9", "-i", str(OVERLAY),
        "-filter_complex", fc, "-map", "[outv]", "-map", "[ca]", "-c:v", "libx264", "-preset", "slow", "-crf", "32", "-tune", "animation",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "80k", "-movflags", "+faststart", str(tmp)])
    new = duration(tmp)
    if abs(new - (old + D)) > 0.12:
        tmp.unlink(missing_ok=True)
        raise SystemExit(f"{name}: duration {new:.3f} != {old:.3f} + {D:.3f}")
    os.replace(tmp, light)
    changed = retrofit_docs(info, T, D, T + LEAD, T + D - TAIL + 0.1)
    rec = {"slug": info["slug"], "voice": info["voice"], "cta_at": round(T, 3), "clip_s": D, "old_s": round(old, 3), "new_s": round(new, 3),
           "end_overlay_at": round(E, 2), "end_offset_s": off, "corner": corner, "lift": lift, "clutter": round(score, 1), "size_mb": round(light.stat().st_size / 1e6, 1), "docs": changed}
    log(name, "done", **rec)
    return rec


# ------------------------------------------------------------------------------------------------ Shorts
def retrofit_short(path: Path) -> dict:
    """Replace the Short's 2.5 s end card (its own GOP at the end, see tools/make_shorts.py) with the new one:
    the same box plus FOLLOW FOR MORE and the animated SUBSCRIBE / LIKE widget. The body is stream-copied."""
    sys.path.insert(0, str(ROOT / "tools"))
    import make_shorts as ms
    from PIL import Image, ImageDraw
    SCRATCH.mkdir(parents=True, exist_ok=True)
    patch = SCRATCH / "short_end_patch.png"
    if not patch.exists():
        im = Image.new("RGBA", (ms.W, ms.H), (0, 0, 0, 0))
        ms.end_box(ImageDraw.Draw(im))
        im.save(patch)
    old = duration(path)
    keys = [float(x.strip(",")) for x in sh(["ffprobe", "-v", "error", "-select_streams", "v", "-skip_frame", "nokey", "-show_entries",
                                               "frame=pts_time", "-of", "csv=p=0", str(path)]).split() if x.strip(",")]
    k = max(keys)
    if not 2.3 < old - k < 2.7:
        raise SystemExit(f"{path.name}: last keyframe {k:.2f} is not the end card start (duration {old:.2f})")
    body, end, lst, tmp = (SCRATCH / f"_sb.mp4", SCRATCH / f"_se.mp4", SCRATCH / "_sl.txt", SCRATCH / f"_{path.name}")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-t", f"{k - 0.001:.3f}", "-c", "copy", str(body)])
    sh(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{k:.3f}", "-i", str(path), "-loop", "1", "-i", str(patch),
        "-ss", "0.9", "-c:v", "libvpx-vp9", "-i", str(ROOT / "assets" / "brand" / "cta" / "subscribe_cta_1080.webm"),
        "-filter_complex", f"[1:v]format=rgba,fade=t=in:d=0.15:alpha=1[p];[0:v][p]overlay=0:0:shortest=1[e];[2:v]scale=720:246[w];"
                           f"[e][w]overlay={ms.CTA_XY[0]}:{ms.CTA_XY[1]}:eof_action=pass[v]",
        "-map", "[v]", "-map", "0:a", "-t", f"{old - k:.3f}", "-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-c:a", "copy", str(end)])
    lst.write_text(f"file '{body}'\nfile '{end}'\n")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(tmp)])
    new = duration(tmp)
    if abs(new - old) > 0.1:
        raise SystemExit(f"{path.name}: duration {new:.3f} != {old:.3f}")
    os.replace(tmp, path)
    log(path.name, "short_done", end_card_at=round(k, 3), old_s=round(old, 3), new_s=round(new, 3))
    return {"short": path.name, "end_card_at": round(k, 2), "dur": round(new, 2)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["clip", "run", "status", "list", "shorts"])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--next", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.cmd == "clip":
        for v in ("ash", "alloy"):
            build_clip(v, a.force)
        return
    if a.cmd == "list":
        for n in UNPOSTED:
            print(n, film_info(n)["slug"])
        return
    if a.cmd == "shorts":   # names = Short files (output/shorts/<ep>_short.mp4); skips ones already logged
        seen = {json.loads(x)["name"] for x in LOG.read_text().splitlines() if '"short_done"' in x} if LOG.exists() else set()
        for n in a.names:
            p = ROOT / "output" / "shorts" / (n if n.endswith(".mp4") else f"{n}_short.mp4")
            print(f"{p.name}: already done (log)" if p.name in seen and not a.force else json.dumps(retrofit_short(p)))
        return
    done = done_names()
    if a.cmd == "status":
        print(f"done {len([n for n in UNPOSTED if n in done])}/{len(UNPOSTED)}; todo: {[n for n in UNPOSTED if n not in done]}")
        return
    names = a.names or [n for n in UNPOSTED if n not in done][: a.next or 1]
    for n in names:
        if n in done:
            print(f"{n}: already done (log)")
            continue
        r = retrofit(n)
        print(json.dumps(r))


if __name__ == "__main__":
    main()
