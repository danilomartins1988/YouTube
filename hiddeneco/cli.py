"""Command-line interface: python -m hiddeneco <command> ..."""
from __future__ import annotations

import argparse
import sys

from hiddeneco.config import REPO_ROOT, project_paths, settings


def _estimate(slug: str, providers: list[str]) -> str:
    from hiddeneco import script as script_mod
    from hiddeneco.costs import tts_cost
    from hiddeneco.research.dossier import build_dossier

    paths = project_paths(slug)
    d = build_dossier(paths)
    sc = script_mod.load_script(paths.project_dir)
    chars = sum(len(script_mod.render_text(s.narration, d)) for s in sc.segments)
    words = sum(script_mod.word_count(script_mod.render_text(s.narration, d)) for s in sc.segments)
    full_lo, full_hi = 8 * 150 * 6, 12 * 150 * 6   # 8-12 min at ~150 wpm, ~6 chars per word incl. spaces
    rows = [f"Script: {words} words / {chars} characters (~{words / 150 * 60:.0f}s at 150 wpm)", "",
            f"{'provider':<12}{'this video':>16}{'full doc (8-12 min)':>26}  pricing basis"]
    for p in providers:
        a, lo, hi = tts_cost(p, chars), tts_cost(p, full_lo), tts_cost(p, full_hi)
        fmt = (lambda c: "unknown" if c.usd is None else f"${c.usd:.2f}")
        rows.append(f"{p:<12}{fmt(a):>16}{fmt(lo) + ' - ' + fmt(hi):>26}  {a.note}")
    rows += ["", "Rendering, research data, maps and fonts: $0 (local, open data, open licences).",
             "No paid service is called unless you pass --tts <paid provider> --allow-paid."]
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hiddeneco", description="The Hidden Economics production pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("topics", help="Rank the 10 topic candidates and write output/topics/topics.md")
    p = sub.add_parser("research", help="Build the source-backed dossier")
    p.add_argument("slug")
    p = sub.add_parser("estimate", help="Estimate costs before building")
    p.add_argument("slug")
    p.add_argument("--tts", nargs="*", default=["espeak", "piper", "openai", "elevenlabs"])
    p = sub.add_parser("build", help="Full build: dossier, script, storyboard, TTS, video, thumbnails, QC")
    p.add_argument("slug")
    p.add_argument("--tts", default=None, help="espeak | piper | elevenlabs | openai | silent")
    p.add_argument("--allow-paid", action="store_true", help="Permit paid TTS providers")
    p.add_argument("--scenes", nargs="*", help="Re-render only these scene ids")
    p = sub.add_parser("qc", help="Re-run QC on an existing build")
    p.add_argument("slug")
    p = sub.add_parser("approve", help="Human approval checkpoint")
    p.add_argument("slug")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--notes", default="")
    p = sub.add_parser("publish", help="Prepare an upload package (requires approval; never uploads)")
    p.add_argument("slug")
    p = sub.add_parser("data", help="Data utilities")
    p.add_argument("action", choices=["refresh"])
    sub.add_parser("tts-check", help="Show which TTS providers are usable here")

    a = ap.parse_args(argv)

    if a.cmd == "topics":
        from hiddeneco.research.topics import load_candidates, report
        path = report(load_candidates(), REPO_ROOT / "output" / "topics")
        print(path.read_text())
        return 0
    if a.cmd == "research":
        from hiddeneco.pipeline import research
        d = research(project_paths(a.slug))
        print(f"Dossier: output/{a.slug}/research/dossier.md ({len(d.claims)} claims)")
        return 0
    if a.cmd == "estimate":
        print(_estimate(a.slug, a.tts))
        return 0
    if a.cmd == "build":
        from hiddeneco.pipeline import build
        r = build(project_paths(a.slug), a.tts, a.allow_paid, a.scenes)
        print(f"\nVideo: output/{a.slug}/{a.slug}.mp4  ({r['runtime_seconds']} s)")
        print(f"QC: {r['errors']} errors, {r['warnings']} warnings, "
              f"{len(r['publish_blockers'])} claims awaiting human verification")
        print(f"See output/{a.slug}/qc/qc_report.md and output/{a.slug}/cost_report.md")
        return 0 if r["passed"] else 1
    if a.cmd == "qc":
        from hiddeneco import qc, storyboard
        from hiddeneco import script as script_mod
        from hiddeneco.pipeline import load_project, load_timeline
        from hiddeneco.research.dossier import load
        paths = project_paths(a.slug)
        d = load(paths)
        sc = script_mod.load_script(paths.project_dir)
        sb = storyboard.rendered(storyboard.load_storyboard(paths.project_dir), d)
        r = qc.run_qc(paths, sc, d, sb, load_timeline(paths), load_project(paths))
        print(qc.to_markdown(r))
        return 0 if r["passed"] else 1
    if a.cmd == "approve":
        from hiddeneco.approval import ApprovalError, approve
        try:
            rec = approve(project_paths(a.slug), a.reviewer, a.notes)
        except ApprovalError as e:
            print(f"NOT APPROVED: {e}", file=sys.stderr)
            return 2
        print(f"Approved by {rec['reviewer']} (video sha256 {rec['video_sha256'][:12]}...)")
        return 0
    if a.cmd == "publish":
        from hiddeneco.approval import ApprovalError, package_for_upload
        try:
            print(package_for_upload(project_paths(a.slug)))
        except ApprovalError as e:
            print(f"BLOCKED: {e}", file=sys.stderr)
            return 2
        return 0
    if a.cmd == "data":
        from hiddeneco.research.data_sources import refresh_snapshot
        print(f"Snapshot rows: {refresh_snapshot()}")
        return 0
    if a.cmd == "tts-check":
        from hiddeneco.tts.providers import PROVIDERS
        cfg = settings()
        for name, cls in PROVIDERS.items():
            ok, why = cls(cfg["tts"]["providers"].get(name, {})).available()
            print(f"{name:<11} {'paid' if cls.paid else 'free':<5} {'OK' if ok else 'unavailable: ' + why}")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
