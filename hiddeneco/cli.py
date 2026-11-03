"""Command-line interface: python -m hiddeneco <command> ..."""
from __future__ import annotations

import argparse
import sys

from hiddeneco.config import REPO_ROOT, project_paths, settings


def _estimate(slug: str, providers: list[str]) -> str:
    from hiddeneco.costs import tts_cost
    from hiddeneco.pipeline import estimate_chars
    from hiddeneco.research.dossier import build_dossier

    topic = project_paths(slug)
    d = build_dossier(topic)
    rows = []
    total_chars = 0
    for name in topic.deliverables():
        chars = estimate_chars(topic.for_deliverable(name), d)
        total_chars += chars
        rows.append(f"  {name:<14}{chars:>6} characters")
    full_lo, full_hi = 8 * 150 * 6, 12 * 150 * 6   # 8-12 min at ~150 wpm, ~6 chars/word incl. spaces
    out = [f"Narration to synthesise for '{slug}':", *rows, f"  {'total':<14}{total_chars:>6} characters", "",
           f"{'provider':<12}{'this topic':>14}{'full doc (8-12 min)':>26}  pricing basis"]
    for p in providers:
        a, lo, hi = tts_cost(p, total_chars), tts_cost(p, full_lo), tts_cost(p, full_hi)
        fmt = (lambda c: "unknown" if c.usd is None else f"${c.usd:.2f}")
        out.append(f"{p:<12}{fmt(a):>14}{fmt(lo) + ' - ' + fmt(hi):>26}  {a.note}")
    out += ["", "Rendering, research data, maps, fonts, music and sound effects: $0 (local, original or open).",
            "No paid service is called unless you pass --tts <paid provider> --allow-paid."]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="hiddeneco", description="The Hidden Economics production pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("topics", help="Rank topic candidates and write output/topics/topics.md")
    p = sub.add_parser("research", help="Build the source-backed dossier")
    p.add_argument("slug")
    p = sub.add_parser("estimate", help="Estimate costs before building")
    p.add_argument("slug")
    p.add_argument("--tts", nargs="*", default=["festival", "kokoro", "espeak", "openai", "elevenlabs"])
    p = sub.add_parser("build", help="Build deliverables: dossier, script, voice, video, thumbnails, QC, exports")
    p.add_argument("slug")
    p.add_argument("-d", "--deliverable", nargs="*", help="Deliverable ids (default: all)")
    p.add_argument("--tts", default=None, help="festival | kokoro | piper | espeak | elevenlabs | openai | silent")
    p.add_argument("--allow-paid", action="store_true", help="Permit paid TTS providers")
    p.add_argument("--scenes", nargs="*", help="Re-render only these scene ids (others reused if present)")
    for name, help_ in (("qc", "Re-run QC"), ("publish", "Prepare approved upload packages (never uploads)")):
        p = sub.add_parser(name, help=help_)
        p.add_argument("slug")
        p.add_argument("deliverable")
    p = sub.add_parser("approve", help="Human approval checkpoint for one deliverable")
    p.add_argument("slug")
    p.add_argument("deliverable")
    p.add_argument("--reviewer", required=True)
    p.add_argument("--notes", default="")
    p = sub.add_parser("data", help="Data utilities")
    p.add_argument("action", choices=["refresh"])
    sub.add_parser("tts-check", help="Show which TTS providers are usable here")

    a = ap.parse_args(argv)

    if a.cmd == "topics":
        from hiddeneco.research.topics import load_candidates, report
        print(report(load_candidates(), REPO_ROOT / "output" / "topics").read_text())
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
        topic = project_paths(a.slug)
        reports = build(topic, a.deliverable, a.tts, a.allow_paid, a.scenes)
        ok = True
        for name, r in reports.items():
            v = r.get("video", {})
            print(f"\n[{name}] {topic.for_deliverable(name).final_video.relative_to(REPO_ROOT)}")
            print(f"  {v.get('width')}x{v.get('height')}, {r['runtime_seconds']} s, {v.get('size_mb')} MB, "
                  f"{v.get('integrated_lufs')} LUFS")
            print(f"  QC: {r['errors']} errors, {r['warnings']} warnings, "
                  f"{len(r['publish_blockers'])} claims awaiting human verification")
            ok &= r["passed"]
        return 0 if ok else 1
    if a.cmd == "qc":
        from hiddeneco import qc, storyboard
        from hiddeneco import script as script_mod
        from hiddeneco.pipeline import format_cfg, load_deliverable, load_timeline
        from hiddeneco.research.dossier import load
        paths = project_paths(a.slug, deliverable=a.deliverable)
        d = load(paths)
        deliverable, _ = load_deliverable(paths)
        sc = script_mod.load_script(paths.deliverable_dir)
        sb = storyboard.rendered(storyboard.load_storyboard(paths.deliverable_dir), d)
        r = qc.run_qc(paths, deliverable, format_cfg(deliverable), sc, d, sb, load_timeline(paths))
        print(qc.to_markdown(r))
        return 0 if r["passed"] else 1
    if a.cmd == "approve":
        from hiddeneco.approval import ApprovalError, approve
        try:
            rec = approve(project_paths(a.slug, deliverable=a.deliverable), a.reviewer, a.notes)
        except ApprovalError as e:
            print(f"NOT APPROVED: {e}", file=sys.stderr)
            return 2
        print(f"Approved by {rec['reviewer']} (video sha256 {rec['video_sha256'][:12]}...)")
        return 0
    if a.cmd == "publish":
        from hiddeneco.approval import ApprovalError, package_for_upload
        try:
            print(package_for_upload(project_paths(a.slug, deliverable=a.deliverable)))
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
