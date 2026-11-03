"""Quality-control report: narration timing, missing media, source attribution, licensing,
editorial distinctiveness and output format. Errors block approval; warnings need a human look."""
from __future__ import annotations

import difflib
import json
from pathlib import Path

import yaml

from hiddeneco.config import REPO_ROOT, ProjectPaths, settings
from hiddeneco.models import VERIFIED_STATUSES, Dossier, Script, Storyboard, TimedScene
from hiddeneco.script import sourcing_issues, word_count


def _issue(cat, sev, msg, **kw):
    return {"category": cat, "severity": sev, "message": msg, **kw}


def check_timing(timed: list[TimedScene], project: dict) -> list[dict]:
    cfg = settings()["qc"]
    out = []
    total = sum(t.duration for t in timed)
    lo, hi = project["target_seconds"]["min"], project["target_seconds"]["max"]
    if not lo <= total <= hi:
        out.append(_issue("timing", "error", f"Runtime {total:.1f}s outside target {lo}-{hi}s"))
    for t in timed:
        if t.audio_seconds <= 0:
            out.append(_issue("timing", "error", f"Segment {t.scene.segment} has no audio"))
            continue
        wpm = word_count(t.narration) / t.audio_seconds * 60
        if not cfg["narration_wpm_min"] <= wpm <= cfg["narration_wpm_max"]:
            out.append(_issue("timing", "warning", f"Segment {t.scene.segment} pace {wpm:.0f} wpm"))
        if t.duration < t.audio_seconds:
            out.append(_issue("timing", "error", f"Scene {t.scene.id} shorter than its narration"))
    return out


def check_media(timed: list[TimedScene], paths: ProjectPaths) -> list[dict]:
    out = []
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    for t in timed:
        if not Path(t.audio_path).exists():
            out.append(_issue("media", "error", f"Missing narration audio {t.audio_path}"))
        scene_file = paths.out / "scenes" / f"{t.scene.id}.mp4"
        if not scene_file.exists():
            out.append(_issue("media", "error", f"Missing rendered scene {scene_file.name}"))
        for a in t.scene.assets:
            entry = manifest.get(a)
            if entry is None:
                out.append(_issue("media", "error", f"Scene {t.scene.id} uses unlisted asset '{a}'"))
            elif entry.get("path") and not (REPO_ROOT / entry["path"]).exists():
                out.append(_issue("media", "error", f"Asset file missing: {entry['path']}"))
    for name in ("thumbnails/thumb_a_the_number.png", "subtitles.srt", "youtube_metadata.md"):
        if not (paths.out / name).exists():
            out.append(_issue("media", "warning", f"Missing deliverable {name}"))
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
            if s.kind == "dataset" and s.license in cfg["attribution_required"] and sid not in sc.sources:
                out.append(_issue("licensing", "error", f"Scene {sc.id} must credit {sid}"))
    return out


def check_distinctiveness(slug: str, storyboard: Storyboard, project: dict) -> list[dict]:
    """Compare scene grammar and style with every other project to avoid template sameness."""
    threshold = settings()["qc"]["max_scene_similarity"]
    mine = [s.type for s in storyboard.scenes]
    out = []
    for other in (REPO_ROOT / "projects").iterdir():
        if other.name == slug or not (other / "storyboard.yaml").exists():
            continue
        theirs = [s["type"] for s in yaml.safe_load((other / "storyboard.yaml").read_text())["scenes"]]
        ratio = difflib.SequenceMatcher(None, mine, theirs).ratio()
        if ratio > threshold:
            out.append(_issue("distinctiveness", "warning",
                              f"Scene sequence {ratio:.0%} similar to '{other.name}'"))
        oproj = yaml.safe_load((other / "project.yaml").read_text())
        if oproj.get("style", {}).get("palette") == project.get("style", {}).get("palette"):
            out.append(_issue("distinctiveness", "warning", f"Same palette as '{other.name}'"))
    return out


def check_output(paths: ProjectPaths, timed: list[TimedScene]) -> list[dict]:
    from hiddeneco.render.assemble import probe
    v = settings()["video"]
    if not paths.final_video.exists():
        return [_issue("output", "error", "Final MP4 missing")]
    info = probe(paths.final_video)
    out = []
    vs = [s for s in info["streams"] if s["codec_type"] == "video"]
    aus = [s for s in info["streams"] if s["codec_type"] == "audio"]
    if not vs or (vs[0]["width"], vs[0]["height"]) != (v["width"], v["height"]):
        out.append(_issue("output", "error", f"Video is not {v['width']}x{v['height']}"))
    if not aus:
        out.append(_issue("output", "error", "No audio stream"))
    dur = float(info["format"]["duration"])
    expected = sum(t.duration for t in timed)
    if abs(dur - expected) > 0.5:
        out.append(_issue("output", "error", f"Duration {dur:.2f}s differs from timeline {expected:.2f}s"))
    return out


def run_qc(paths: ProjectPaths, script: Script, dossier: Dossier, storyboard: Storyboard,
           timed: list[TimedScene], project: dict) -> dict:
    issues = []
    issues += check_timing(timed, project)
    issues += check_media(timed, paths)
    src, blockers = check_sources(script, dossier, storyboard)
    issues += src
    issues += check_licensing(storyboard, dossier)
    issues += check_distinctiveness(paths.slug, storyboard, project)
    issues += check_output(paths, timed)
    errors = [i for i in issues if i["severity"] == "error"]
    report = {
        "slug": paths.slug,
        "runtime_seconds": round(sum(t.duration for t in timed), 2),
        "errors": len(errors),
        "warnings": len(issues) - len(errors),
        "issues": issues,
        "publish_blockers": blockers,
        "passed": not errors,
        "publishable": not errors and not blockers,
    }
    qc_dir = paths.out_sub("qc")
    (qc_dir / "qc_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (qc_dir / "qc_report.md").write_text(to_markdown(report), encoding="utf-8")
    return report


def to_markdown(r: dict) -> str:
    lines = [f"# QC report: {r['slug']}", "",
             f"- Runtime: **{r['runtime_seconds']} s**",
             f"- Errors: **{r['errors']}**, warnings: **{r['warnings']}**",
             f"- Technical QC passed: **{r['passed']}**",
             f"- Publishable (no unverified claims): **{r['publishable']}**", "",
             "## Issues", ""]
    lines += [f"- [{i['severity'].upper()}] ({i['category']}) {i['message']}" for i in r["issues"]] or ["None."]
    lines += ["", "## Publish blockers - claims needing human verification", ""]
    lines += [f"- `{b['claim']}` ({b['status']}): {b['text']}  \n  {b['note']}" for b in r["publish_blockers"]] \
        or ["None."]
    lines += ["", "To clear a blocker: read the primary source, then set `status: human_verified` and "
              "`verified_by: <name>` for that claim in projects/<slug>/sources.yaml and rebuild."]
    return "\n".join(lines) + "\n"
