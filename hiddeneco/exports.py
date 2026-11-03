"""Platform export packages. Built as DRAFTS on every build; `publish` copies them to a final
package only after human approval. Nothing here talks to any platform API."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from hiddeneco.config import ProjectPaths
from hiddeneco.models import Deliverable

# Official starting points. Requirements change: verify them at publish time, every time.
POLICY_LINKS = {
    "youtube": [
        ("YouTube channel monetization policies", "https://support.google.com/youtube/answer/1311392"),
        ("YouTube Partner Program overview & eligibility", "https://support.google.com/youtube/answer/72851"),
        ("Disclosing altered or synthetic content", "https://support.google.com/youtube/answer/14328491"),
    ],
    "youtube_shorts": [
        ("YouTube Shorts help", "https://support.google.com/youtube/topic/10343432"),
        ("YouTube Partner Program overview & eligibility", "https://support.google.com/youtube/answer/72851"),
        ("Disclosing altered or synthetic content", "https://support.google.com/youtube/answer/14328491"),
    ],
    "instagram_reels": [("Instagram Help Center", "https://help.instagram.com/")],
    "tiktok": [("TikTok Support (creator programs, AI-generated content labels)", "https://support.tiktok.com/")],
}

ASPECT = {"youtube": "16:9", "youtube_shorts": "9:16", "instagram_reels": "9:16", "tiktok": "9:16"}


def _link_or_copy(src: Path, dst: Path) -> None:
    dst.unlink(missing_ok=True)
    try:
        os.link(src, dst)          # hard link: no extra disk for large videos
    except OSError:
        shutil.copy2(src, dst)


def build_drafts(paths: ProjectPaths, deliverable: Deliverable) -> list[Path]:
    root = paths.out_sub("exports_draft")
    made = []
    for platform in deliverable.platforms:
        d = root / platform
        d.mkdir(parents=True, exist_ok=True)
        _link_or_copy(paths.final_video, d / paths.final_video.name)
        for name in ("subtitles.srt", "metadata.md"):
            if (paths.out / name).exists():
                shutil.copy2(paths.out / name, d / name)
        for t in sorted((paths.out / "thumbnails").glob("*.png")):
            shutil.copy2(t, d / t.name)
        lines = [f"# {platform} package - DRAFT (not approved)", "",
                 f"- Aspect ratio: {ASPECT.get(platform, '?')}; video: `{paths.final_video.name}`",
                 "- Captions: `subtitles.srt`" + (" (also burned into the picture)" if deliverable.captions.get(
                     "burn_in") else ""),
                 "- Title/description/caption suggestions: `metadata.md`", "",
                 "## Before uploading (manual checklist)", "",
                 "- [ ] Approval recorded (`python -m hiddeneco approve ...`) and QC passed",
                 "- [ ] Every claim in the dossier is `human_verified` or `data_derived`",
                 "- [ ] Re-read the current platform rules below (eligibility, monetization, AI disclosure)",
                 "- [ ] Mark synthetic narration with the platform's AI-content disclosure where required",
                 "- [ ] Upload as private/unlisted first and watch it end-to-end on a phone", "",
                 "Monetization and creator-programme eligibility are never guaranteed and must be checked "
                 "against the platform's current terms.", "", "## Official references", ""]
        lines += [f"- [{n}]({u})" for n, u in POLICY_LINKS.get(platform, [])]
        (d / "CHECKLIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        made.append(d)
    return made
