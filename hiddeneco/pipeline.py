"""End-to-end build for one project. Each stage writes inspectable files under output/<slug>/."""
from __future__ import annotations

import json
import time

import yaml

from hiddeneco import metadata, qc, thumbnails
from hiddeneco import script as script_mod
from hiddeneco import storyboard as sb_mod
from hiddeneco.config import ProjectPaths, settings
from hiddeneco.costs import CostLedger, compute_cost
from hiddeneco.logging_setup import attach_run_log, log, step
from hiddeneco.models import TimedScene
from hiddeneco.render import assemble
from hiddeneco.render.style import Style
from hiddeneco.research import dossier as dossier_mod
from hiddeneco.tts.providers import get_provider


class BuildError(RuntimeError):
    pass


def load_project(paths: ProjectPaths) -> dict:
    return yaml.safe_load((paths.project_dir / "project.yaml").read_text(encoding="utf-8"))


def research(paths: ProjectPaths):
    with step("research.dossier", slug=paths.slug):
        d = dossier_mod.build_dossier(paths)
        dossier_mod.write(d, paths)
    return d


def write_script_and_storyboard(paths: ProjectPaths, d):
    with step("script.check"):
        sc = script_mod.load_script(paths.project_dir)
        issues = script_mod.sourcing_issues(sc, d)
        errors = [i for i in issues if i["severity"] == "error"]
        (paths.out_sub("script") / "script.md").write_text(script_mod.to_markdown(sc, d), encoding="utf-8")
        for i in issues:
            log("script.issue", **i)
        if errors:
            raise BuildError("Script sourcing errors: " + "; ".join(e["message"] for e in errors))
    with step("storyboard.render_params"):
        raw = sb_mod.load_storyboard(paths.project_dir)
        problems = sb_mod.check_alignment(raw, sc)
        if problems:
            raise BuildError("; ".join(problems))
        sb = sb_mod.rendered(raw, d)
        (paths.out_sub("storyboard") / "storyboard.md").write_text(sb_mod.to_markdown(sb, d), encoding="utf-8")
        (paths.out / "storyboard" / "storyboard.json").write_text(sb.model_dump_json(indent=2), encoding="utf-8")
    return sc, sb


def build(paths: ProjectPaths, tts_name: str | None = None, allow_paid: bool = False,
          only_scenes: list[str] | None = None) -> dict:
    cfg = settings()
    vcfg = cfg["video"]
    attach_run_log(paths.out_sub("logs"))
    log("build.start", slug=paths.slug)
    assemble.require_ffmpeg()
    project = load_project(paths)
    ledger = CostLedger(paths.out / "cost_report.json")

    d = research(paths)
    sc, sb = write_script_and_storyboard(paths, d)

    tts_name = tts_name or cfg["tts"]["default_provider"]
    tts = get_provider(tts_name, cfg, allow_paid=allow_paid)
    with step("tts", provider=tts_name):
        timed = assemble.synthesize_narration(sc, d, sb, tts, paths.out_sub("audio"), vcfg)
        chars = sum(len(t.narration) for t in timed)
        ledger.replace_step("tts", tts.estimate_cost(chars))
        (paths.out / "timeline.json").write_text(
            json.dumps([t.model_dump() for t in timed], indent=2), encoding="utf-8")

    style = Style(project["style"], vcfg["width"], vcfg["height"], vcfg["fps"])
    t0 = time.perf_counter()
    with step("render.scenes"):
        scene_dir = paths.out_sub("scenes")
        files = []
        for ts in timed:
            out = scene_dir / f"{ts.scene.id}.mp4"
            if only_scenes is None or ts.scene.id in only_scenes or not out.exists():
                credits = [d.source(s).credit or d.source(s).publisher for s in ts.scene.sources]
                credits = list(dict.fromkeys(credits))
                assemble.render_scene(ts, style, credits, out, vcfg, vcfg["scene_lead_in"])
            files.append(out)
    with step("render.assemble"):
        audio = assemble.build_audio_track(timed, paths.out / "audio" / "narration.wav",
                                           vcfg["scene_lead_in"], vcfg["audio_sample_rate"])
        assemble.concat_and_mux(files, paths.out / "audio" / "narration.wav", paths.final_video,
                                paths.out_sub("work"))
        assemble.write_srt(timed, vcfg["scene_lead_in"], paths.out / "subtitles.srt")
        log("render.final", path=str(paths.final_video), seconds=round(audio, 2))
    ledger.replace_step("render", compute_cost(time.perf_counter() - t0, "render"))

    with step("thumbnails"):
        thumbnails.make_thumbnails(project["style"], d, paths.out_sub("thumbnails"))
    with step("metadata"):
        metadata.build(sc, d, timed, tts_name, paths.out)
    with step("qc"):
        report = qc.run_qc(paths, sc, d, sb, timed, project)
    (paths.out / "cost_report.md").write_text("# Cost report\n\n" + ledger.markdown() + "\n", encoding="utf-8")
    log("build.done", slug=paths.slug, qc_errors=report["errors"], blockers=len(report["publish_blockers"]))
    return report


def load_timeline(paths: ProjectPaths) -> list[TimedScene]:
    return [TimedScene(**x) for x in json.loads((paths.out / "timeline.json").read_text())]
