"""Export an episode's editorial documents to top-level folders:

  research/<name>_sources.md      every source (URL, publisher, dates) and every claim (value, period, status)
  scripts/<name>_documentary.md   full narration with the claim behind every number
  storyboards/<name>_storyboard.md  timestamped, scene-by-scene animation storyboard (from timeline.json)

    python tools/export_episode_docs.py <slug> <name> [deliverable]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from hiddeneco.config import project_paths  # noqa: E402
from hiddeneco.research.dossier import load  # noqa: E402

DESCRIBE = {
    "oil_platform": "2.5D North Sea scene: parallax waves, rotating crane, flickering flare, travelling block, helicopter, supply ship, gulls, oil pulses in pipeline",
    "map": "Camera-driven vector map: highlighted countries, animated routes with moving packets, flow arcs with particles, pulsing markers, callouts",
    "big_counter": "Counter rolls up to the figure inside an orbiting tick ring; label and context rise in",
    "kinetic_text": "Kinetic typography: lines enter word by word on narration cues",
    "act_title": "Chapter card: masked title reveal, gold rule draws",
    "bar_chart": "Bars grow in a stagger with counting values",
    "line_chart": "Line chart draws progressively with the narration; event annotations pop on cues",
    "donut": "Allocation arcs sweep one after another; legend counts in",
    "timeline": "Axis draws; dated markers drop in on cues with ripple",
    "compare": "Side-by-side figures count up; bars rise",
    "fund_flow": "Animated flow diagram: nodes pop in on cues, links draw and carry moving coins",
    "race_track": "2.5D trackside: parallax skyline, crowd, placeholder sponsor boards, scrolling kerbs, original cars racing past; headline and value on narration cues",
    "circuit": "Fictional circuit draws itself, then cars lap it with trails; markers pop on narration cues",
    "whiteboard": "Whiteboard hand-drawing: an original hand traces each stroke and writes labels progressively, then the sketch colours in and comes alive",
    "isometric": "Isometric diorama builds itself: objects rise into place and keep moving (boats bob, smoke drifts, turbines spin)",
    "people_ratio": "People icons recolour to show a changing ratio",
    "end_card": "Closing words land; brand line draws",
    "ai_network": "Ecosystem graph assembles group by group (apps, labs, clouds, data centers); packets flow; the shared supplier at the centre is revealed",
    "cpu_gpu": "CPU vs GPU: a pool of independent tasks flies into a few big cores (rounds) vs many small cores (one step); then a step-by-step chain shows the opposite trade-off",
    "stack": "Layered software ecosystem builds bottom-up with data pulses; optional developer counter; switching-cost panel fills item by item",
    "supply_chain": "World map with camera moves: supply stages light up in order, packets flow along arcs, process strip tracks the stage; optional bottleneck chokes everything downstream",
    "stacked_columns": "Fiscal-year columns grow chronologically by business segment, then morph into a 100% share view",
    "landscape": "Competitive matrix: a cursor selects each dimension and cells type in; then options slide onto a conceptual flexibility-vs-specialisation axis",
}


def ts(sec: float) -> str:
    m, s = divmod(int(round(sec)), 60)
    return f"{m}:{s:02d}"


def main(slug: str, name: str, deliverable: str = "documentary") -> None:
    p = project_paths(slug, deliverable=deliverable)
    d = load(p)
    (ROOT / "research").mkdir(exist_ok=True)
    lines = [f"# Research dossier - {d.title}", "", f"Generated {d.generated_at}. Status ladder: data_derived and "
             "human_verified are publishable; source_located means located by web research, not yet read in full by "
             "a named reviewer. Reference period = the year/date the statistic describes.", "",
             "## Sources", "", "| id | Publisher | Title | Published | Accessed | Type | URL |", "|---|---|---|---|---|---|---|"]
    for s in d.sources:
        lines.append(f"| `{s.id}` | {s.publisher} | {s.title} | {s.published or '-'} | {s.accessed} | {s.kind} | {s.url} |")
    lines += ["", "## Claims", "", "| id | Claim | On screen | Reference period | Status | Sources | Note |", "|---|---|---|---|---|---|---|"]
    for c in d.claims:
        period = c.fields.get("year") or (c.fields.get("start_year") and f"{c.fields.get('start_year')}-{c.fields.get('end_year')}") or "-"
        note = (c.verification_note or "").replace("\n", " ")
        lines.append(f"| `{c.id}` | {c.text} | {c.display or '-'} | {period} | **{c.status}** | {', '.join(c.source_ids)} | {note} |")
    (ROOT / "research" / f"{name}_sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (ROOT / "scripts").mkdir(exist_ok=True)
    script_md = (p.out / "script" / "script.md").read_text(encoding="utf-8")
    (ROOT / "scripts" / f"{name}_documentary.md").write_text(script_md, encoding="utf-8")

    (ROOT / "storyboards").mkdir(exist_ok=True)
    timed = json.loads((p.out / "timeline.json").read_text())
    total = sum(t["duration"] for t in timed)
    sb = [f"# Storyboard - {d.title}", "", f"Total {ts(total)} ({total:.1f} s), {len(timed)} scenes. Timestamps come from the "
          "narration timing of the build that produced `timeline.json`. Engine: Remotion (React + SVG), 1920x1080, 30 fps.", "",
          "| # | Start | Dur | Scene | Type | Animation | Narration (start) | Sources |", "|---|---|---|---|---|---|---|---|"]
    for i, t in enumerate(timed, 1):
        sc = t["scene"]
        nar = (t["narration"][:90] + "...") if len(t["narration"]) > 90 else (t["narration"] or "(music only)")
        sb.append(f"| {i} | {ts(t['start'])} | {t['duration']:.1f}s | `{sc['id']}` | {sc['type']} | {DESCRIBE.get(sc['type'], '')} | "
                  f"{nar.replace('|', '/')} | {', '.join(sc.get('sources', [])) or '-'} |")
    (ROOT / "storyboards" / f"{name}_storyboard.md").write_text("\n".join(sb) + "\n", encoding="utf-8")
    print("wrote research/, scripts/, storyboards/ for", name)


if __name__ == "__main__":
    main(*sys.argv[1:4])
