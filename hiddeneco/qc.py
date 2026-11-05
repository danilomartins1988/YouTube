"""Quality control for one deliverable.

Errors block approval; warnings need a human look; unverified claims are publish blockers.
Checks: duration, resolution, streams, black/frozen frames, silence, loudness, caption timing,
caption safe zone, missing media, source attribution, licensing, distinctiveness.
"""
from __future__ import annotations

import difflib
import json
import re
import subprocess
from pathlib import Path

import yaml

from hiddeneco.config import REPO_ROOT, ProjectPaths, settings
from hiddeneco.models import VERIFIED_STATUSES, Deliverable, Dossier, Script, Storyboard, TimedScene
from hiddeneco.script import sourcing_issues, word_count


def _issue(cat, sev, msg, **kw):
    return {"category": cat, "severity": sev, "message": msg, **kw}


def check_timing(timed: list[TimedScene], deliverable: Deliverable) -> list[dict]:
    cfg = settings()["qc"]
    out = []
    total = sum(t.duration for t in timed)
    lo, hi = deliverable.target_seconds["min"], deliverable.target_seconds["max"]
    if not lo <= total <= hi:
        out.append(_issue("timing", "error", f"Runtime {total:.1f}s outside target {lo:g}-{hi:g}s"))
    for t in timed:
        if t.audio_seconds <= 0:
            if not t.narration.strip():
                continue   # intentional silent scene (act card), carried by music
            out.append(_issue("timing", "error", f"Segment {t.scene.segment} has no audio"))
            continue
        wpm = word_count(t.narration) / t.audio_seconds * 60
        if not cfg["narration_wpm_min"] <= wpm <= cfg["narration_wpm_max"]:
            out.append(_issue("timing", "warning", f"Segment {t.scene.segment} pace {wpm:.0f} wpm "
                                                   "(numerals count as one word)"))
        if t.duration < t.audio_seconds:
            out.append(_issue("timing", "error", f"Scene {t.scene.id} shorter than its narration"))
    return out


def check_captions(timed: list[TimedScene], total: float, deliverable: Deliverable, fmt: dict) -> list[dict]:
    from hiddeneco.render.assemble import caption_cues
    out = []
    words = [(ts.start + w["start"], ts.start + w["end"], w["word"]) for ts in timed for w in ts.words]
    narration_words = sum(word_count(ts.narration) for ts in timed)
    if not words:
        return [_issue("captions", "error", "No word timings - captions cannot be generated")]
    if sum(1 for _, _, w in words if re.search(r"[A-Za-z0-9]", w)) < 0.95 * narration_words:
        out.append(_issue("captions", "error", "Captions do not cover all narration words"))
    for (s0, e0, w0), (s1, _, _) in zip(words, words[1:]):
        if e0 < s0 or s1 < s0:
            out.append(_issue("captions", "error", f"Non-monotonic caption timing at '{w0}'"))
            break
    if words[-1][1] > total + 0.05:
        out.append(_issue("captions", "error", "Captions run past the end of the video"))
    for c in caption_cues(timed):
        dur = c["end"] - c["start"]
        if dur < 0.25:
            out.append(_issue("captions", "warning", f"Caption shorter than 0.25 s: '{c['text']}'"))
        elif len(c["text"]) / dur > 25:
            out.append(_issue("captions", "warning", f"Caption reading speed >25 chars/s: '{c['text']}'"))
    if deliverable.captions.get("burn_in") and fmt.get("safe_zone"):
        # caption baseline is placed by the renderer; verify it sits clear of the bottom UI zone
        y = fmt["height"] - fmt["safe_zone"]["bottom"] - 150
        if y + 60 > fmt["height"] - fmt["safe_zone"]["bottom"]:
            out.append(_issue("captions", "error", "Burned-in captions overlap the bottom safe zone"))
    return out


def check_media(timed: list[TimedScene], paths: ProjectPaths, deliverable: Deliverable) -> list[dict]:
    out = []
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    project = yaml.safe_load((paths.project_dir / "project.yaml").read_text())
    remotion = project.get("renderer") == "remotion"   # one picture file instead of one file per scene
    if remotion and not (paths.out / "work" / "remotion_video.mp4").exists():
        out.append(_issue("media", "error", "Missing Remotion picture work/remotion_video.mp4"))
    for t in timed:
        if t.audio_seconds and not Path(t.audio_path).exists():
            out.append(_issue("media", "error", f"Missing narration audio {t.audio_path}"))
        if not remotion and not (paths.out / "scenes" / f"{t.scene.id}.mp4").exists():
            out.append(_issue("media", "error", f"Missing rendered scene {t.scene.id}.mp4"))
        for a in t.scene.assets:
            entry = manifest.get(a)
            if entry is None:
                out.append(_issue("media", "error", f"Scene {t.scene.id} uses unlisted asset '{a}'"))
            elif entry.get("path") and not (REPO_ROOT / entry["path"]).exists():
                out.append(_issue("media", "error", f"Asset file missing: {entry['path']}"))
    expected = ["subtitles.srt", "metadata.md"]
    if not list((paths.out / "thumbnails").glob("*.png")):
        out.append(_issue("media", "error", "No thumbnail/cover rendered"))
    for name in expected:
        if not (paths.out / name).exists():
            out.append(_issue("media", "error", f"Missing deliverable {name}"))
    return out


def check_sources(script: Script, dossier: Dossier, storyboard: Storyboard) -> tuple[list[dict], list[dict]]:
    out = [_issue("sources", i["severity"], i["message"], segment=i["segment"])
           for i in sourcing_issues(script, dossier)]
    blockers = []
    used = {cid for seg in script.segments for cid in seg.claims}
    for cid in sorted(used):
        c = dossier.claim(cid)
        for sid in c.source_ids:
            s = dossier.source(sid)
            if not s.url or not s.accessed:
                out.append(_issue("sources", "error", f"Source {sid} lacks URL or access date"))
        if c.status not in VERIFIED_STATUSES:
            blockers.append({"claim": cid, "status": c.status, "text": c.text, "note": c.verification_note})
    known = {s.id for s in dossier.sources}
    for sc in storyboard.scenes:
        for sid in sc.sources:
            if sid not in known:
                out.append(_issue("sources", "error", f"Scene {sc.id} credits unknown source {sid}"))
    for seg in script.segments:
        if seg.analysis and not seg.source_note:
            out.append(_issue("sources", "warning", f"Segment {seg.id} has analysis but no note"))
    return out, blockers


def check_licensing(storyboard: Storyboard, dossier: Dossier) -> list[dict]:
    cfg = settings()["licensing"]
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    out = []
    for sc in storyboard.scenes:
        for a in sc.assets:
            lic = (manifest.get(a) or {}).get("license")
            if lic not in cfg["allowlist"]:
                out.append(_issue("licensing", "error", f"Asset {a} licence '{lic}' not on allowlist"))
            elif lic in cfg["attribution_required"] and not manifest[a].get("attribution"):
                out.append(_issue("licensing", "error", f"Asset {a} needs attribution text"))
        for sid in sc.sources:
            s = dossier.source(sid)
            if s.kind == "dataset" and s.license is None:
                out.append(_issue("licensing", "warning", f"Dataset {sid} has no licence recorded"))
    return out


def check_distinctiveness(paths: ProjectPaths, storyboard: Storyboard) -> list[dict]:
    """Compare scene grammar with every other deliverable of every project."""
    threshold = settings()["qc"]["max_scene_similarity"]
    mine = [s.type for s in storyboard.scenes]
    out = []
    for sb_file in (REPO_ROOT / "projects").glob("*/deliverables/*/storyboard.yaml"):
        if sb_file.parent == paths.deliverable_dir.resolve() or sb_file.parent == paths.deliverable_dir:
            continue
        theirs = [s["type"] for s in yaml.safe_load(sb_file.read_text())["scenes"]]
        ratio = difflib.SequenceMatcher(None, mine, theirs).ratio()
        if ratio > threshold:
            name = f"{sb_file.parent.parent.parent.name}/{sb_file.parent.name}"
            out.append(_issue("distinctiveness", "warning", f"Scene sequence {ratio:.0%} similar to '{name}'"))
    return out


def analyse_video(path: Path) -> dict:
    """Run FFmpeg detectors in one pass: black frames, frozen frames, silence, loudness."""
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
           "-vf", "blackdetect=d=0.4:pix_th=0.04,freezedetect=n=-60dB:d=4",
           "-af", "silencedetect=n=-55dB:d=1.5,ebur128=peak=true", "-f", "null", "-"]
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    res = {
        "black": re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", err),
        "freeze": re.findall(r"freeze_start: ([\d.]+)", err),
        "silence": re.findall(r"silence_start: ([\d.]+)", err),
        "integrated_lufs": None, "true_peak_dbfs": None,
    }
    summary = err[err.rfind("Summary:"):] if "Summary:" in err else ""
    m = re.search(r"I:\s+(-?[\d.]+) LUFS", summary)
    if m:
        res["integrated_lufs"] = float(m.group(1))
    m = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summary)
    if m:
        res["true_peak_dbfs"] = float(m.group(1))
    return res


def check_output(paths: ProjectPaths, timed: list[TimedScene], fmt: dict) -> tuple[list[dict], dict]:
    from hiddeneco.render.assemble import probe
    if not paths.final_video.exists():
        return [_issue("output", "error", "Final MP4 missing")], {}
    info = probe(paths.final_video)
    out = []
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    aus = [s for s in info["streams"] if s["codec_type"] == "audio"]
    if not vs or (vs[0]["width"], vs[0]["height"]) != (fmt["width"], fmt["height"]):
        out.append(_issue("output", "error", f"Video is not {fmt['width']}x{fmt['height']}"))
    if not aus:
        out.append(_issue("output", "error", "No audio stream"))
    dur = float(info["format"]["duration"])
    expected = sum(t.duration for t in timed)
    if abs(dur - expected) > 0.5:
        out.append(_issue("output", "error", f"Duration {dur:.2f}s differs from timeline {expected:.2f}s"))
    a = analyse_video(paths.final_video)
    for s0, e0 in a["black"]:
        out.append(_issue("render", "error", f"Black frames {float(s0):.2f}-{float(e0):.2f}s"))
    for s0 in a["freeze"]:
        out.append(_issue("render", "warning", f"Picture static for >4 s from {float(s0):.2f}s (pacing?)"))
    for s0 in a["silence"]:
        out.append(_issue("audio", "error", f"Audio silent for >1.5 s from {float(s0):.2f}s"))
    if a["integrated_lufs"] is None:
        out.append(_issue("audio", "error", "Could not measure loudness"))
    elif abs(a["integrated_lufs"] - fmt["loudness_lufs"]) > 2.0:
        out.append(_issue("audio", "warning", f"Loudness {a['integrated_lufs']} LUFS vs target "
                                              f"{fmt['loudness_lufs']}"))
    if a["true_peak_dbfs"] is not None and a["true_peak_dbfs"] > -0.5:
        out.append(_issue("audio", "warning", f"True peak {a['true_peak_dbfs']} dBFS (clipping risk)"))
    facts = {"width": vs[0]["width"] if vs else None, "height": vs[0]["height"] if vs else None,
             "fps": vs[0].get("r_frame_rate") if vs else None, "video_codec": vs[0].get("codec_name") if vs else None,
             "audio_codec": aus[0].get("codec_name") if aus else None,
             "audio_sample_rate": aus[0].get("sample_rate") if aus else None,
             "duration_s": round(dur, 3), "size_mb": round(int(info["format"]["size"]) / 1e6, 1),
             "integrated_lufs": a["integrated_lufs"], "true_peak_dbfs": a["true_peak_dbfs"]}
    return out, facts


FOREIGN_CURRENCY = re.compile(r"(?<![A-Za-z])(NOK|SEK|DKK|EUR|GBP|CHF|AED|JPY|CNY|INR|BRL|CAD|AUD)(?![A-Za-z])|[€£¥₹]|"
                              r"\b(kroner|krone|krona|kronor|euros?|pounds? sterling|francs?|dirhams?|yen|yuan|rupees?|reais)\b",
                              re.IGNORECASE)


def check_currency(paths: ProjectPaths, timed: list[TimedScene]) -> list[dict]:
    """Editorial rule (settings.editorial.display_currency): money is shown and spoken in US dollars."""
    project = yaml.safe_load((paths.project_dir / "project.yaml").read_text())
    if project.get("currency_exempt") or settings().get("editorial", {}).get("display_currency", "USD") != "USD":
        return []
    out = []
    for t in timed:
        on_screen = json.dumps(t.scene.params, ensure_ascii=False)
        for where, text in (("narration", t.narration), ("on-screen text", on_screen)):
            m = FOREIGN_CURRENCY.search(text)
            if m:
                out.append(_issue("currency", "error", f"Scene {t.scene.id}: non-USD amount in {where} ('{m.group(0)}'); "
                                  "convert to US dollars with a cited official exchange rate"))
    return out


def run_qc(paths: ProjectPaths, deliverable: Deliverable, fmt: dict, script: Script, dossier: Dossier,
           storyboard: Storyboard, timed: list[TimedScene]) -> dict:
    total = sum(t.duration for t in timed)
    issues = []
    issues += check_timing(timed, deliverable)
    issues += check_captions(timed, total, deliverable, fmt)
    issues += check_media(timed, paths, deliverable)
    src, blockers = check_sources(script, dossier, storyboard)
    issues += src
    issues += check_licensing(storyboard, dossier)
    issues += check_distinctiveness(paths, storyboard)
    issues += check_currency(paths, timed)
    out_issues, facts = check_output(paths, timed, fmt)
    issues += out_issues
    errors = [i for i in issues if i["severity"] == "error"]
    report = {"slug": paths.slug, "deliverable": deliverable.id, "format": deliverable.format,
              "runtime_seconds": round(total, 2), "video": facts, "errors": len(errors),
              "warnings": len(issues) - len(errors), "issues": issues, "publish_blockers": blockers,
              "passed": not errors, "publishable": not errors and not blockers}
    qc_dir = paths.out_sub("qc")
    (qc_dir / "qc_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (qc_dir / "qc_report.md").write_text(to_markdown(report), encoding="utf-8")
    return report


def to_markdown(r: dict) -> str:
    v = r.get("video", {})
    lines = [f"# QC report: {r['slug']} / {r['deliverable']} ({r['format']})", "",
             f"- Runtime: **{r['runtime_seconds']} s**",
             f"- Video: {v.get('width')}x{v.get('height')} @ {v.get('fps')} {v.get('video_codec')}, "
             f"audio {v.get('audio_codec')} {v.get('audio_sample_rate')} Hz, {v.get('size_mb')} MB",
             f"- Loudness: {v.get('integrated_lufs')} LUFS integrated, true peak {v.get('true_peak_dbfs')} dBFS",
             f"- Errors: **{r['errors']}**, warnings: **{r['warnings']}**",
             f"- Technical QC passed: **{r['passed']}**",
             f"- Publishable (no unverified claims): **{r['publishable']}**", "", "## Issues", ""]
    lines += [f"- [{i['severity'].upper()}] ({i['category']}) {i['message']}" for i in r["issues"]] or ["None."]
    lines += ["", "## Publish blockers - claims needing human verification", ""]
    lines += [f"- `{b['claim']}` ({b['status']}): {b['text']}  \n  {b['note']}" for b in r["publish_blockers"]] \
        or ["None."]
    lines += ["", "To clear a blocker: read the primary source, then set `status: human_verified` and "
              "`verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild."]
    return "\n".join(lines) + "\n"
