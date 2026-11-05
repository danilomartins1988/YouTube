# Episode 04 - "Why Norway Is So Rich — The Secret Behind Its Oil Fortune"

Produced 2026-11-05 with the Remotion (React + SVG) engine. Nothing was uploaded or scheduled.

## Deliverables

| File | Status |
|---|---|
| `output/norway_documentary.mp4` | 1920x1080, H.264 High yuv420p 30 fps, AAC 48 kHz stereo, 654.7 s (10:54), 182 MB. Not in git (too large); see "Retrieving the video". |
| `output/norway_thumbnail_01.png` … `_03.png` | 1280x720, rendered with Remotion (copies in this folder) |
| `research/norway_sources.md` | 42 sources and 52 claims (2 computed from World Bank data) with URLs, dates, reference periods and status |
| `scripts/norway_documentary.md` | Full narration with the claim behind every number |
| `storyboards/norway_storyboard.md` | 48 scenes, timestamped from the final narration timing |
| `reports/norway_quality_report.md` | All 10 automated checks pass (format, codecs, duration, sync, black/frozen frames, licences) |
| `reports/norway_cost_report.md` | Paid: US$0.2368 of the US$1.00 cap (OpenAI narration only) |
| `reports/norway_youtube_metadata.md` | Titles, description with chapters (4,888 chars, under YouTube's 5,000 limit), tags; `reports/norway_pinned_comment.md` has the full source list if the description had to be shortened |
| `norway_documentary.srt` | English subtitles (sidecar) |

## Before publishing

Publishing stays blocked by QC until a named reviewer verifies the 49 `source_located` claims used in the film in
`projects/why-norway-is-so-rich/sources.yaml` (set `status: human_verified`, `verified_by`). Priorities:
Ministry of Finance figures taken from search snippets (regjeringen.no returned 403): fiscal rule wording,
2026 budget NOK 579.4bn / 2.8%; OECD trust survey figures (snippet); derived figures labelled "our
calculation" (NOK 3.9m per person, mainland 79.8%, ageing ratios); NBIM fund-value timeline year mapping;
the approximate median line drawn on the 1965 map.

## Retrieving the video

The MP4 is only in this session's cloud container (`output/` is git-ignored). It was sent as a file attachment
in the chat, together with a lighter copy (`output/downloads/norway_documentary_light.mp4`, 50.6 MB, same
1920x1080 picture and sound, CRF 25). To rebuild anywhere: clone the repo, `pip install -r requirements.txt`,
install FFmpeg and Node 18+, `cd remotion && npm ci`, then
`python -m hiddeneco build why-norway-is-so-rich -d documentary --tts openai --allow-paid`
(narration is cached only in the container, so a fresh rebuild pays for it again, about US$0.24; the US$1.00 cap still applies).
