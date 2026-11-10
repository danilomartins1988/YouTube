"""Builds docs/UPLOAD_KIT/: an ordered, copy-paste upload kit for every finished video not yet on the channel.

Reads docs/UPLOAD_KIT/published.json (what is already on YouTube), each episode's youtube-package (title, description,
tags, thumbnail) and docs/SHORTS_COPY_PASTE.md (Short title/description/tags). Writes:
  docs/UPLOAD_KIT/README.md            index + day-by-day order + checklist
  docs/UPLOAD_KIT/NN_<episode>.md      one file per pending upload, every field ready to paste
Videos are not copied (MP4s stay in output/, light versions only, never committed).
Run: python tools/build_upload_kit.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs/UPLOAD_KIT"
EP = ROOT / "docs/episodes"

# Long videos still to upload, in the recommended order (Shorts 14 and 18 are already live and point to these first).
ORDER = ["14-memory", "18-chip-chemicals", "29-us-healthcare", "27-oil", "31-us-housing", "19-quibi", "32-costco",
         "24-debeers", "37-amazon-prime", "28-bigtech-ai", "30-credit-cards", "39-visa-mastercard", "25-nickel",
         "36-car-insurance", "16-terafab", "34-car-dealers", "26-mcdonalds", "33-student-debt", "15-nanoimprint",
         "35-electricity", "17-india-chips", "38-airports", "40-grocery"]
# Shorts whose long video is already on the channel: one per day alongside the new long video.
BACKLOG_SHORTS = ["08-asml", "12-wirecard", "03-formula1", "20-notpetya", "21-citibank", "06-nvidia", "02-dubai",
                  "09-cables", "11-flags", "10-anguilla", "07-taiwan-v2", "04-norway", "01-switzerland"]


def light(video_txt: Path) -> str:
    v = video_txt.read_text().splitlines()[0].strip()
    p = Path(v)
    lp = p.with_name(p.stem + "_light.mp4")
    return str(lp) if (ROOT / lp).exists() else v + " (MISSING)"


def short_block(ep: str) -> dict | None:
    sheet = (ROOT / "docs/SHORTS_COPY_PASTE.md").read_text()
    sec = re.search(rf"## {re.escape(ep)}\s*\n(.*?)(?=\n## |\Z)", sheet, re.S)
    if not sec:
        return None
    get = lambda k: (re.search(rf"\*\*{k}\*\*\s*\n```\n(.*?)\n```", sec.group(1), re.S) or [None, ""])[1].strip()
    f = ROOT / "output/shorts" / f"{ep}_short.mp4"
    return {"file": f"output/shorts/{ep}_short.mp4" + ("" if f.exists() else " (MISSING)"),
            "title": get("Title"), "description": get("Description"), "tags": get("Tags")}


def code(s: str) -> str:
    return f"```\n{s}\n```\n"


def main() -> None:
    pub = json.loads((KIT / "published.json").read_text())
    for old in KIT.glob("[0-9][0-9]_*.md"):
        old.unlink()
    rows, day_rows = [], []
    backlog = [b for b in BACKLOG_SHORTS if b not in pub["short"]]
    for n, ep in enumerate(ORDER, 1):
        if ep in pub["long"]:
            continue
        pkg = EP / ep / "youtube-package"
        title = (pkg / "title.txt").read_text().strip().splitlines()[0]
        desc = (pkg / "description.txt").read_text().strip()
        tags = (pkg / "tags.txt").read_text().strip()
        alts = re.findall(r"^\d\. \*\*(.+?)\*\*", (EP / ep / "youtube_package.md").read_text(), re.M)
        srt = EP / ep / "subtitles_en.srt"
        sh = None if ep in pub["short"] else short_block(ep)
        md = [f"# {n:02d}. {title}\n",
              f"Episode folder: `docs/episodes/{ep}/`. Upload as **Private** (or schedule); the owner sets it public.\n",
              "## Files\n",
              f"- Video: `{light(pkg / 'video.txt')}`",
              f"- Thumbnail: `docs/episodes/{ep}/youtube-package/thumbnail.png` (alternative: "
              f"`{next((p.name for p in sorted(pkg.glob('thumbnail-alt-*.png'))), 'none')}`)",
              f"- Subtitles (English): `docs/episodes/{ep}/subtitles_en.srt`" + ("" if srt.exists() else " (none)"), "",
              "## Title\n", code(title),
              "Other title options: " + " · ".join(a for a in alts if a != title) + "\n",
              f"## Description ({len(desc)} characters, chapters included)\n", code(desc),
              "## Tags\n", code(tags),
              "## Settings in YouTube Studio\n",
              "- Audience: **No, it's not made for kids**\n- Category: **Education**\n- Video language: **English**\n"
              "- Captions: upload the `.srt` above (Subtitles → Upload file → With timing)\n"
              "- End screen: add *Best for viewer* video + *Subscribe*\n- Visibility: **Private**, publish when you want\n"]
        if sh:
            md += ["---\n", "## Short for this episode (upload after the long video is public)\n",
                   f"- File: `{sh['file']}`\n", "**Title**\n", code(sh["title"]), "**Description**\n", code(sh["description"]),
                   "**Tags**\n", code(sh["tags"]),
                   "In Studio: link the Short to the long video (*Related video*).\n"]
        fn = KIT / f"{n:02d}_{ep}.md"
        fn.write_text("\n".join(md))
        rows.append((n, ep, title, fn.name, bool(sh)))
    for k, (n, ep, title, fname, has_short) in enumerate(rows):
        extra = backlog[k] if k < len(backlog) else ""
        day_rows.append(f"| Day {k + 1} | [{title}]({fname}) | {'its Short' if has_short else '—'} | "
                        f"{f'Short of {extra} ([sheet](../SHORTS_COPY_PASTE.md#{extra}))' if extra else '—'} |")
    left_shorts = backlog[len(rows):]
    readme = ["# Upload kit: everything still to go on the channel\n",
              "Built by `tools/build_upload_kit.py` from `published.json` (channel read on 2026-11-10). "
              "Every file below has the title, description, tags, thumbnail and subtitle paths ready to paste. "
              "Videos are the **light** versions in `output/` (not committed). Upload everything as **Private**; "
              "you make it public.\n",
              f"Long videos still to upload: **{len(rows)}**. Shorts still to upload: **{sum(r[4] for r in rows) + len(backlog)}**.\n",
              "## Suggested order (one long video + its Short per day, plus one older Short)\n",
              "| Day | Long video | Short of the same episode | Extra Short (long already live) |", "|---|---|---|---|", *day_rows,
              ("\nRemaining older Shorts: " + ", ".join(left_shorts) + "\n") if left_shorts else "",
              "\n## Fixes for videos already on the channel\n", "See [00_FIXES_PUBLISHED.md](00_FIXES_PUBLISHED.md).\n",
              "\n## After each upload\n", "Add the video ID to `docs/UPLOAD_KIT/published.json` (or tell Claude) and rebuild the kit.\n"]
    (KIT / "README.md").write_text("\n".join(readme))
    print(f"{len(rows)} long uploads written to {KIT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
