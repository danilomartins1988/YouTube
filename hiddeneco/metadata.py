"""Platform metadata suggestions: titles, descriptions, chapters, tags, sources and credits.
Text comes from deliverable.yaml (`metadata:`); sources and credits are generated from the dossier
and the asset manifest so attribution can't be forgotten."""
from __future__ import annotations

from pathlib import Path

import yaml

from hiddeneco.config import REPO_ROOT
from hiddeneco.models import Deliverable, Dossier, Script, TimedScene

TITLE_LIMIT = 100          # YouTube title limit (characters)
DESCRIPTION_LIMIT = 5000   # YouTube description limit (characters)


def mmss(sec: float) -> str:
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def chapters(timed: list[TimedScene], script: Script) -> tuple[list[str], str]:
    """YouTube chapter rules: first at 0:00, at least 3 chapters, each at least 10 s."""
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


def credits(dossier: Dossier, script: Script, timed: list[TimedScene], tts_name: str) -> tuple[list[str], list[str]]:
    used = sorted({sid for seg in script.segments for cid in seg.claims for sid in dossier.claim(cid).source_ids}
                  | {sid for ts in timed for sid in ts.scene.sources})
    manifest = yaml.safe_load((REPO_ROOT / "assets" / "manifest.yaml").read_text())["assets"]
    assets = sorted({a for ts in timed for a in ts.scene.assets})
    src = [f"- {dossier.source(s).publisher}: {dossier.source(s).title} - {dossier.source(s).url}" for s in used]
    cred = [f"- {manifest[a]['attribution']}" for a in assets if a in manifest]
    cred += ["- Graphics, animation, music and sound effects: original, made by The Hidden Economics",
             f"- Narration: synthetic voice ({tts_name})"]
    return src, cred


def fit_description(head: list[str], src: list[str], tail: list[str],
                    limit: int = DESCRIPTION_LIMIT) -> tuple[str, bool]:
    """Keep the description under YouTube's limit: full source lines, else compact 'publisher - URL'
    lines, else as many as fit plus a pointer to the pinned comment. Returns (text, overflowed)."""
    def join(lines):
        return "\n".join(head + ["Sources", *lines] + tail)
    if len(join(src)) <= limit:
        return join(src), False
    compact = [ln.split(": ", 1)[0] + " - " + ln.rsplit(" - ", 1)[-1] for ln in src]
    if len(join(compact)) <= limit:
        return join(compact), False
    kept = []
    for ln in compact:
        trial = kept + [ln, f"+ {len(compact) - len(kept) - 1} more sources in the pinned comment"]
        if len(join(trial)) > limit:
            break
        kept.append(ln)
    kept.append(f"+ {len(compact) - len(kept)} more sources in the pinned comment")
    return join(kept), True


def build(deliverable: Deliverable, meta: dict, script: Script, dossier: Dossier, timed: list[TimedScene],
          tts_name: str, out_dir: Path) -> Path:
    src, cred = credits(dossier, script, timed, tts_name)
    titles = meta.get("titles", [deliverable.title])
    md = ["# Platform metadata (suggestions - nothing is uploaded)", ""]
    if deliverable.vertical:
        caption = meta.get("caption", script.logline)
        tags = " ".join(meta.get("hashtags", []))
        md += ["## Title options", ""] + [f"{i}. {t} ({len(t)} chars)" for i, t in enumerate(titles, 1)]
        md += ["", "## Caption (Shorts / Reels / TikTok)", "", "```", caption, "", tags, "", "Sources:", *src,
               "", "Credits:", *cred, "```"]
    else:
        chap, note = chapters(timed, script)
        desc = [meta.get("description_intro", script.logline), ""]
        if not note:
            desc += ["Chapters", *chap, ""]
        tail = ["", "Credits & licences", *cred, "",
                "Some statements are the channel's interpretation; these are marked in the script notes.", "",
                " ".join(meta.get("hashtags", []))]
        text, overflow = fit_description(desc, src, tail)
        if overflow:   # full list goes in a pinned comment (YouTube comments allow 10,000 characters)
            (out_dir / "pinned_comment.md").write_text("Sources (full list)\n" + "\n".join(src) + "\n",
                                                        encoding="utf-8")
        md += ["## Title options", ""] + [f"{i}. {t} ({len(t)} chars)" for i, t in enumerate(titles, 1)]
        md += ["", f"## Description ({len(text)} chars)", "", "```", text, "```", ""]
        if note:
            md += [f"> {note} Proposed: " + "; ".join(chap), ""]
        md += ["## Tags", "", ", ".join(meta.get("tags", [])), ""]
    md += ["", "## Disclosure", "",
           "Narration uses a synthetic voice. At upload, review each platform's AI / altered-content "
           "disclosure setting and label accordingly.", ""]
    for t in titles:
        if len(t) > TITLE_LIMIT:
            raise ValueError(f"Title over {TITLE_LIMIT} chars: {t}")
    out = out_dir / "metadata.md"
    out.write_text("\n".join(md), encoding="utf-8")
    return out
