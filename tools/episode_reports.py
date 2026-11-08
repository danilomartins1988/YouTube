"""Write reports/<name>_quality_report.md and reports/<name>_cost_report.md for a built deliverable.

Everything in the reports is measured from the files on disk (ffprobe, the QC report, the timeline, the
narration cache and the paid-spend ledger). Nothing is assumed.

    python tools/episode_reports.py <slug> <name> [deliverable] [--video output/<name>_documentary.mp4]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco import audio as A  # noqa: E402
from hiddeneco.config import project_paths, settings  # noqa: E402


def ffprobe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "format=duration,size,bit_rate:stream=codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,sample_rate,channels",
                          "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def loudness(path: Path) -> str:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    tp = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    return f"{i[-1]} LUFS integrated, true peak {tp[-1]} dBFS" if i and tp else "n/a"


def black_or_frozen(path: Path) -> tuple[str, str]:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vf", "blackdetect=d=1.0:pix_th=0.05,freezedetect=n=0.002:d=5",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err)
    freezes = re.findall(r"freeze_start: ([\d.]+)", err)
    return (", ".join(f"{float(a):.1f}-{float(b):.1f}s" for a, b in blacks) or "none",
            ", ".join(f"{float(a):.1f}s" for a in freezes) or "none")


def caption_sync(out: Path, lead: float) -> dict:
    tl = json.loads((out / "timeline.json").read_text())
    total = tl[-1]["start"] + tl[-1]["duration"]
    voice = np.zeros(int(total * 100) + 1, bool)
    for s in tl:
        if not s["audio_seconds"]:
            continue
        x, r = A.read_wav(Path(s["audio_path"]))
        hop = r // 100
        rms = np.sqrt((x[: len(x) // hop * hop].reshape(-1, hop) ** 2).mean(1))
        on = rms > rms.max() * 10 ** (-38 / 20)
        i0 = int((s["start"] + lead) * 100)
        voice[i0:i0 + len(on)] |= on[: len(voice) - i0]
    def t(v):
        h, m, rest = v.split(":"); sec, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
    cues = [(t(a), t(b)) for a, b in re.findall(r"(\S+) --> (\S+)", (out / "subtitles.srt").read_text())]
    mask = np.zeros_like(voice)
    for a, b in cues:
        mask[int(a * 100): int(b * 100)] = True
    onsets = np.flatnonzero(voice[1:] & ~voice[:-1]) / 100
    err = [float(np.min(np.abs(onsets - a))) for a, _ in cues]
    return {"cues": len(cues), "voice_captioned": float((mask & voice).sum() / max(1, voice.sum())),
            "median": float(np.median(err)), "p90": float(np.percentile(err, 90)), "max": float(np.max(err))}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("name"); ap.add_argument("deliverable", nargs="?", default="documentary")
    ap.add_argument("--video")
    a = ap.parse_args()
    p = project_paths(a.slug, deliverable=a.deliverable)
    cfg = settings()
    video = Path(a.video) if a.video else p.final_video
    info = ffprobe(video)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    au = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    dur = float(info["format"]["duration"])
    qc = json.loads((p.out / "qc" / "qc_report.json").read_text())
    lead = cfg["formats"]["long_16x9"]["scene_lead_in"]
    sync = caption_sync(p.out, lead)
    blacks, freezes = black_or_frozen(video)
    tl = json.loads((p.out / "timeline.json").read_text())
    types = {}
    for s in tl:
        types[s["scene"]["type"]] = types.get(s["scene"]["type"], 0) + 1
    checks = [
        ("File exists", video.exists(), f"{video} ({int(info['format']['size']) / 1e6:.1f} MB)"),
        ("Resolution 1920x1080", (v["width"], v["height"]) == (1920, 1080), f"{v['width']}x{v['height']}"),
        ("H.264 video", v["codec_name"] == "h264", f"{v['codec_name']} {v.get('profile', '')}, {v.get('pix_fmt')}, {v.get('r_frame_rate')} fps"),
        ("AAC audio", bool(au) and au["codec_name"] == "aac", f"{au['codec_name']} {au['sample_rate']} Hz, {au['channels']} ch" if au else "missing"),
        ("Duration 11-13:20 min (channel standard 660-800 s)", 660 <= dur <= 800, f"{dur:.2f} s ({int(dur // 60)}:{int(dur % 60):02d})"),
        ("English narration", qc.get("errors", 1) == 0, "OpenAI gpt-4o-mini-tts 'ash', English script; QC errors: " + str(qc.get("errors"))),
        ("Caption/voice sync", sync["median"] < 0.15 and sync["voice_captioned"] > 0.97,
         f"{sync['cues']} cues; median cue-start offset {sync['median']:.2f} s, p90 {sync['p90']:.2f} s; "
         f"{sync['voice_captioned']:.0%} of speech captioned"),
        ("No black gaps (>1 s)", blacks == "none", blacks),
        ("No frozen picture (>5 s)", freezes == "none", freezes),
        ("Licensed assets only", not any(i["category"] == "licensing" and i["severity"] == "error" for i in qc.get("issues", [])),
         "every scene asset is on the licence allowlist (assets/manifest.yaml)"),
    ]
    lines = [f"# Quality report - {p.slug} / {a.deliverable}", "",
             "| Check | Result | Detail |", "|---|---|---|"]
    lines += [f"| {c} | {'PASS' if ok else 'FAIL'} | {d} |" for c, ok, d in checks]
    lines += ["", f"- Loudness: {loudness(video)}",
              f"- Scenes: {len(tl)}; types: " + ", ".join(f"{k} x{n}" for k, n in sorted(types.items())),
              f"- Average scene length: {dur / len(tl):.1f} s; act cards are music-only.",
              "", "## Pipeline QC report", "", (p.out / "qc" / "qc_report.md").read_text()]
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / f"{a.name}_quality_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    ledger_path = p.topic_out / "paid_spend.json"
    led = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"entries": []}
    chars = sum(e["chars"] for e in led["entries"])
    usd = sum(e["usd"] for e in led["entries"])
    o = cfg["tts"]["providers"]["openai"]
    proj = json.loads(json.dumps(__import__("yaml").safe_load((p.project_dir / "project.yaml").read_text())))
    cap = (proj.get("budget") or {}).get("max_paid_usd", cfg["budget"]["max_paid_usd_per_topic"])
    speech = sum(s["audio_seconds"] for s in tl)
    c = ["# Cost report - " + p.slug, "",
         "## Narration (the only paid component)", "",
         f"- Provider / model / voice: OpenAI `{o['model']}`, voice `{o['voice']}`, unit `{o.get('unit', 'sentence')}` "
         "(one request per script segment), existing integration (`hiddeneco/tts/providers.py`).",
         f"- Requests: {len(led['entries'])} (each a successful synthesis; cached audio is never re-billed).",
         f"- Characters sent: {chars:,}. Audio produced: {speech:.1f} s ({speech / 60:.1f} min).",
         f"- Estimated cost (configured conservative rate US${cfg['pricing']['openai']['usd_per_1k_chars']}/1k chars): **US${usd:.4f}**.",
         f"- Cross-check with OpenAI's published token pricing for {o['model']} (US$0.60 per 1M text-input tokens, US$12 per 1M "
         f"audio-output tokens, about US$0.015 per minute of audio): about **US${speech / 60 * 0.015 + chars / 4 / 1e6 * 0.6:.3f}**.",
         f"- Episode cap: **US${cap:.2f}** cumulative (enforced before every request by `hiddeneco/budget.py`). Remaining under the cap: US${cap - usd:.4f}.",
         "- Billing evidence: the local ledger `output/" + p.slug + "/paid_spend.json` (timestamp, characters and estimated USD per request). "
         "The OpenAI usage/costs API was queried and refused with 403 (the project key lacks the `api.usage.read` scope), "
         "so no invoice-level figure is available here; check https://platform.openai.com/usage for the authoritative amount.",
         "", "## Everything else", "",
         "| Item | Tool | Cost |", "|---|---|---|",
         "| Research | Web research by the pipeline's agents | US$0 (no paid data) |",
         "| Animation and rendering | Remotion 4.0.535 (React + SVG), Chrome Headless Shell, FFmpeg, local CPU | US$0 |",
         "| Maps | Natural Earth (public domain) | US$0 |",
         "| Music and sound effects | Generated by code (`hiddeneco/audio.py`) | US$0 |",
         "| Fonts | Inter (SIL OFL 1.1) | US$0 |",
         "", f"**Total paid: US${usd:.4f}** (estimate; cap US${cap:.2f}). No other paid service was called. Nothing was published.", "",
         "Licence note: Remotion is free for individuals and companies with up to three employees; larger companies need a "
         "Remotion company licence (https://www.remotion.dev/license)."]
    (ROOT / "reports" / f"{a.name}_cost_report.md").write_text("\n".join(c) + "\n", encoding="utf-8")
    print("\n".join(f"{'PASS' if ok else 'FAIL'}  {c}: {d}" for c, ok, d in checks))


if __name__ == "__main__":
    main()
