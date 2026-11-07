# Episode 09: The Cables at the Bottom of the Ocean That Carry the Internet (completion report)

Status: **rendered, fact-checked by AI before writing, validated; not published.** Publishing is manual, and a named
human reviewer should still sign off the claims (see `FACT_CHECK.md`).

## Video (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/cables_documentary.mp4` | Final cut: 1920x1080, 30 fps, H.264/AAC, −16.2 LUFS. Intro after the hook; subtitles in `output/the-cables-at-the-bottom-of-the-ocean/documentary/subtitles.srt` | 11:03 |
| `output/cables_documentary_light.mp4` | 1280x720 copy for download (≈ 29 MB) | 11:03 |

## What changed after the user's feedback (2026-11-06)

- **Cartoon style:** new engine scene `engine_cartoon` (`remotion/src/animation-engine/CartoonOcean/`): bright flat
  colours, thick outlines, smiling sun, waves, fish, whale, ships (cargo, fishing, repair, cable-laying), anchors that
  drop and drag, trawl nets, a repair grapple that lifts and splices the cable, an undersea volcano, an island whose
  lights go out, glowing cables with pulses of light, speech-bubble callouts and camera tracking shots. 12 scenes use it.
- **No mission talk:** the five parts are an internal structure only. No "Mission one", no mission list, no
  "mission complete", no HUD or stamps, no "THE QUESTION / WHY IT MATTERS" labels. Recorded in `docs/PRODUCTION_STANDARD.md`.
- **Generic teaser** at the end ("another hidden link of the world economy").

## Structure (internal) and chapters

| Time | Part |
|---|---|
| 0:00 | Hook: cartoon dive from a worried satellite to the glowing cable on the seabed; ITU map (> 99%) |
| 0:31 | Channel intro |
| 0:36 | How the internet crosses the ocean: satellites vs cables (cartoon), presenter draws the route, light in a fibre, garden hose / armour (cartoon) |
| 2:32 | Who owns the cables: presenter draws the consortium, users changed, demand ×3, 2Africa map, renting → owning flow |
| 4:45 | Who builds and fixes them: cable ship laying cable (cartoon), cross-section, builders map, repair ship splicing (cartoon) |
| 6:28 | When a cable breaks: fishing net snaps a cable, faults per year, Red Sea 2024 (cartoon), presenter draws redundancy, Tonga 2022 (cartoon) |
| 8:36 | The fight over the seabed: SEA-ME-WE 6 and PLCN maps, presenter draws two networks, 600+ cables |
| 10:25 | Payoff (cartoon journey of your data) and generic teaser |

Presenter sequences: 4 (`p07_draw`, `p13_club`, `p29_backup`, `p37_split`).

## Deliverables

| Deliverable | Location |
|---|---|
| Script | `scripts/cables_documentary.md` (source `projects/the-cables-at-the-bottom-of-the-ocean/deliverables/documentary/script.yaml`) |
| Storyboard | `storyboards/cables_storyboard.md`; generators `tools/gen_cables_storyboard.py` + `tools/gen_cables_cartoons.py` |
| Scene manifest | `docs/episodes/09-cables/scene_manifest.json` |
| Sources | `research/cables_sources.md` |
| Fact-check log | `docs/episodes/09-cables/FACT_CHECK.md` |
| Asset licences | `research/cables_asset_licenses.md` |
| YouTube package | `docs/episodes/09-cables/youtube_package.md` |
| Cost and QA reports | `reports/cables_cost_report.md`, `reports/cables_quality_report.md`, `docs/episodes/09-cables/visual_qc/` |

## Voice

OpenAI `gpt-4o-mini-tts`, voice `ash`. Spent **US$0.29** in total (ledger
`output/the-cables-at-the-bottom-of-the-ocean/paid_spend.json`), including the re-synthesis after the script was
rewritten without mission lines. Cap: US$1.00. Nothing else paid.

## QC

0 errors. Warnings are number words (years written out, "A A E one", "ninety nine percent" which is sourced) and four
slower-paced segments. All `tools/episode_reports.py` checks PASS (no black gaps, no frozen picture over 5 s, captions in sync).
One unresolved cue (the end card's brand cue dict), as in Episode 08; harmless.

## Limitations

- All 17 claims are `source_located`; a named human reviewer must still sign off.
- Map routes are schematic arcs; company markers show countries, not sites (stated on screen).
- Maps, presenter boards and text cards keep the channel's dark style; the cartoon world is used for the story beats.
