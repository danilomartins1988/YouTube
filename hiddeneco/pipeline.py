"""End-to-end build. One topic -> shared dossier -> one or more deliverables (16:9 / 9:16).
Each stage writes inspectable files under output/<slug>/<deliverable>/."""
from __future__ import annotations

import json
import time

import yaml

from hiddeneco import exports, manifest, metadata, qc, thumbnails
from hiddeneco import script as script_mod
from hiddeneco import storyboard as sb_mod
from hiddeneco.config import ProjectPaths, settings
from hiddeneco.costs import CostLedger, compute_cost, tts_cost
from hiddeneco.logging_setup import attach_run_log, log, step
from hiddeneco.models import Deliverable, TimedScene
from hiddeneco.render import assemble
from hiddeneco.render.style import Style
from hiddeneco.research import dossier as dossier_mod
from hiddeneco.script import render_value
from hiddeneco.tts.providers import get_provider


class BuildError(RuntimeError):
    pass


def load_project(paths: ProjectPaths) -> dict:
    return yaml.safe_load((paths.project_dir / "project.yaml").read_text(encoding="utf-8"))


def load_deliverable(paths: ProjectPaths) -> tuple[Deliverable, dict]:
    raw = yaml.safe_load((paths.deliverable_dir / "deliverable.yaml").read_text(encoding="utf-8"))
    extras = {k: raw.pop(k) for k in ("thumbnails", "metadata") if k in raw}
    return Deliverable(**raw), extras


def format_cfg(deliverable: Deliverable) -> dict:
    return {**settings()["formats"][deliverable.format]}


def research(paths: ProjectPaths):
    with step("research.dossier", slug=paths.slug):
        d = dossier_mod.build_dossier(paths)
        dossier_mod.write(d, paths)
    return d


def prepare(paths: ProjectPaths, d):
    with step("script.check", deliverable=paths.deliverable):
        sc = script_mod.load_script(paths.deliverable_dir)
        issues = script_mod.sourcing_issues(sc, d)
        (paths.out_sub("script") / "script.md").write_text(script_mod.to_markdown(sc, d), encoding="utf-8")
        for i in issues:
            log("script.issue", **i)
        errors = [i for i in issues if i["severity"] == "error"]
        if errors:
            raise BuildError("Script sourcing errors: " + "; ".join(e["message"] for e in errors))
    with step("storyboard.render_params", deliverable=paths.deliverable):
        raw = sb_mod.load_storyboard(paths.deliverable_dir)
        problems = sb_mod.check_alignment(raw, sc)
        if problems:
            raise BuildError("; ".join(problems))
        sb = sb_mod.rendered(raw, d)
        (paths.out_sub("storyboard") / "storyboard.md").write_text(sb_mod.to_markdown(sb, d), encoding="utf-8")
        (paths.out / "storyboard" / "storyboard.json").write_text(sb.model_dump_json(indent=2), encoding="utf-8")
    return sc, sb


def estimate_chars(paths: ProjectPaths, d) -> int:
    sc = script_mod.load_script(paths.deliverable_dir)
    return sum(len(script_mod.render_text(s.narration, d)) for s in sc.segments)


def build_deliverable(paths: ProjectPaths, d, project: dict, tts_name: str | None = None,
                      allow_paid: bool = False, only_scenes: list[str] | None = None) -> dict:
    cfg = settings()
    vcfg = cfg["video"]
    deliverable, extras = load_deliverable(paths)
    fmt = format_cfg(deliverable)
    rate, fps = vcfg["audio_sample_rate"], vcfg["fps"]
    log("deliverable.start", deliverable=deliverable.id, format=deliverable.format)
    ledger = CostLedger(paths.out / "cost_report.json")
    ledger.lines = []

    sc, sb = prepare(paths, d)

    tts_name = tts_name or cfg["tts"]["default_provider"]
    tts = get_provider(tts_name, cfg, allow_paid=allow_paid)
    ledger.replace_step("tts (pre-build estimate)", tts_cost(tts_name, estimate_chars(paths, d),
                                                              "tts (pre-build estimate)", estimated=True))
    with step("tts", provider=tts_name, deliverable=deliverable.id):
        timed, fresh_chars = assemble.synthesize_narration(
            sc, d, sb, tts, paths.out_sub("audio"), fmt, rate, fps, cfg["tts"].get("sentence_gap", 0.2))
        line = tts_cost(tts_name, fresh_chars, "tts (characters actually synthesised)", estimated=False)
        line.note += "; cached sentences are free"
        ledger.replace_step(line.step, line)
        (paths.out / "timeline.json").write_text(json.dumps([t.model_dump() for t in timed], indent=2),
                                                 encoding="utf-8")

    style = Style(project["style"], fmt["width"], fmt["height"], fps)
    t0 = time.perf_counter()
    with step("render.scenes", deliverable=deliverable.id):
        scene_dir = paths.out_sub("scenes")
        files = []
        for ts in timed:
            out = scene_dir / f"{ts.scene.id}.mp4"
            if only_scenes is None or ts.scene.id in only_scenes or not out.exists():
                credits = list(dict.fromkeys(d.source(s).credit or d.source(s).publisher for s in ts.scene.sources))
                assemble.render_scene(ts, style, credits, out, vcfg, fmt, deliverable.captions.get("burn_in", False))
            files.append(out)
    with step("render.assemble", deliverable=deliverable.id):
        mix, _voice = assemble.build_audio_track(timed, paths.out_sub("audio"), deliverable, fmt, rate)
        assemble.concat_and_mux(files, mix, paths.final_video, paths.out_sub("work"))
        assemble.write_srt(timed, paths.out / "subtitles.srt")
    ledger.replace_step("render", compute_cost(time.perf_counter() - t0, "render"))

    with step("thumbnails", deliverable=deliverable.id):
        concepts = render_value(extras.get("thumbnails", []), d)
        thumbnails.make_thumbnails(project["style"], concepts, paths.out_sub("thumbnails"))
    with step("metadata", deliverable=deliverable.id):
        metadata.build(deliverable, render_value(extras.get("metadata", {}), d), sc, d, timed, tts_name, paths.out)
    with step("exports.draft", deliverable=deliverable.id):
        exports.build_drafts(paths, deliverable)
    with step("qc", deliverable=deliverable.id):
        report = qc.run_qc(paths, deliverable, fmt, sc, d, sb, timed)
    manifest.write(paths.out, [paths.project_dir / "project.yaml", paths.project_dir / "sources.yaml",
                               paths.deliverable_dir / "deliverable.yaml", paths.deliverable_dir / "script.yaml",
                               paths.deliverable_dir / "storyboard.yaml"],
                   {"deliverable": deliverable.id, "format": deliverable.format, "tts_provider": tts_name,
                    "tts_options": tts.options, "video": report.get("video")})
    (paths.out / "cost_report.md").write_text(
        f"# Cost report: {paths.slug} / {deliverable.id}\n\n" + ledger.markdown(cfg.get("brl_per_usd")) + "\n",
        encoding="utf-8")
    log("deliverable.done", deliverable=deliverable.id, qc_errors=report["errors"],
        blockers=len(report["publish_blockers"]))
    return report


def build(topic: ProjectPaths, deliverables: list[str] | None = None, tts_name: str | None = None,
          allow_paid: bool = False, only_scenes: list[str] | None = None) -> dict[str, dict]:
    attach_run_log(topic.topic_out / "logs")
    assemble.require_ffmpeg()
    project = load_project(topic)
    d = research(topic)
    reports = {}
    for name in deliverables or topic.deliverables():
        reports[name] = build_deliverable(topic.for_deliverable(name), d, project, tts_name, allow_paid,
                                          only_scenes)
    return reports


def load_timeline(paths: ProjectPaths) -> list[TimedScene]:
    return [TimedScene(**x) for x in json.loads((paths.out / "timeline.json").read_text())]
