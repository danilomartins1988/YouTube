"""YouTube title/description/tags suggestions with chapters, sources and licence attributions."""
from __future__ import annotations

from pathlib import Path

import yaml

from hiddeneco.config import REPO_ROOT
from hiddeneco.models import Dossier, Script, TimedScene

TITLE_OPTIONS = [
    "Why Switzerland Is So Rich",
    "How Did Switzerland Get So Rich?",
    "Switzerland Has No Coastline. So Why Is It This Rich?",
    "The Three Things That Made Switzerland Rich",
    "Switzerland's Wealth, Explained in 90 Seconds",
]


def mmss(sec: float) -> str:
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def chapters(timed: list[TimedScene], script: Script) -> tuple[list[str], str]:
    """Merge consecutive scenes with the same chapter; check YouTube's rules
    (first at 0:00, at least 3 chapters, each at least 10 s)."""
    names = {s.id: s.chapter for s in script.segments}
    merged: list[list] = []
    for ts in timed:
        name = names.get(ts.scene.segment) or "Conclusion"
        if merged and merged[-1][0] == name:
            continue
        merged.append([name, ts.start])
    merged[0][1] = 0.0
    ends = [m[1] for m in merged[1:]] + [sum(t.duration for t in timed)]
    ok = len(merged) >= 3 and all(e - m[1] >= 10 for m, e in zip(merged, ends))
    lines = [f"{mmss(m[1])} {m[0]}" for m in merged]
    return lines, "" if ok else "Chapters omitted: YouTube needs >=3 chapters of >=10 s each."


def build(script: Script, dossier: Dossier, timed: list[TimedScene], tts_name: str, out_dir: Path) -> Path:
    used = sorted({sid for seg in script.segments for cid in seg.claims
                   for sid in dossier.claim(cid).source_ids})
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    assets = sorted({a for ts in timed for a in ts.scene.assets})
    chap, chap_note = chapters(timed, script)
    desc = [script.logline, ""]
    if not chap_note:
        desc += ["Chapters", *chap, ""]
    desc += ["Sources"]
    for sid in used:
        s = dossier.source(sid)
        desc.append(f"- {s.publisher}: {s.title} - {s.url}")
    desc += ["", "Credits & licences"]
    desc += [f"- {manifest[a]['attribution']}" for a in assets if a in manifest]
    desc += ["- Graphics and animation: original, made by The Hidden Economics",
             f"- Narration: synthetic voice ({tts_name})" if tts_name != "human" else "",
             "", "Some statements are the channel's interpretation; these are marked in the script notes.",
             "", "#economics #switzerland #documentary"]
    tags = ["Switzerland", "Swiss economy", "economics explained", "GDP per capita",
            "why is Switzerland rich", "economic history", "documentary"]
    md = ["# YouTube metadata (suggestions - nothing is uploaded)", "", "## Title options", ""]
    md += [f"{i}. {t} ({len(t)} chars)" for i, t in enumerate(TITLE_OPTIONS, 1)]
    md += ["", "## Description", "", "```", *[x for x in desc if x is not None], "```", "",
           "## Tags", "", ", ".join(tags), ""]
    if chap_note:
        md += [f"> {chap_note} Proposed: " + "; ".join(chap), ""]
    md += ["## Disclosure", "",
           "Narration uses a synthetic voice. Review YouTube's altered/synthetic content disclosure "
           "setting at upload time.", ""]
    out = out_dir / "youtube_metadata.md"
    out.write_text("\n".join(md), encoding="utf-8")
    return out
