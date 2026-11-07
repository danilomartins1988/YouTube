# Episode 11: Why Almost Half the World's Ships Fly Three Small Flags (completion report)

Status: **rendered, fact-checked by AI before writing, validated; not published.** A named human reviewer should
still sign off the claims (see `FACT_CHECK.md`).

## Video (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/flags_documentary.mp4` | Final cut: 1920x1080, 30 fps, H.264/AAC, −16.2 LUFS; subtitles in `output/why-ships-fly-foreign-flags/documentary/subtitles.srt` | 11:02 |
| `output/flags_documentary_light.mp4` | 1280x720 copy (≈ 29 MB) | 11:02 |

## Style

Cartoon-first (user decision of 2026-11-06), bright "cartoon day" palette on every scene (maps, boards and charts
included). New CartoonOcean features: text pennants on ships that switch mid-scene (flag hopping, false flags),
crews on deck that turn sad when abandoned, ports with container cranes. Generators use the shared `tools/cartoon_kit.py`.
The five parts are an internal structure only; the teaser is generic.

## Chapters

0:00 hook · 0:16 channel intro · 0:40 Whose ship is it? · 2:30 How it started · 4:34 Why owners do it ·
6:30 The dark side · 8:50 Why it survives · 10:19 payoff and generic teaser

Presenter sequences: 4 (`p05_flag`, `p14_registry`, `p27_five`, `p32_gains`).

## Deliverables

| Deliverable | Location |
|---|---|
| Script | `scripts/flags_documentary.md` (source `projects/why-ships-fly-foreign-flags/deliverables/documentary/script.yaml`) |
| Storyboard | `storyboards/flags_storyboard.md`; generator `tools/gen_flags_storyboard.py` + `tools/cartoon_kit.py` |
| Scene manifest | `docs/episodes/11-flags/scene_manifest.json` |
| Sources / fact-check / licences | `research/flags_sources.md`, `docs/episodes/11-flags/FACT_CHECK.md`, `research/flags_asset_licenses.md` |
| YouTube package | `docs/episodes/11-flags/youtube_package.md` |
| Reports | `reports/flags_cost_report.md`, `reports/flags_quality_report.md`, `docs/episodes/11-flags/visual_qc/` |

## Voice and QC

OpenAI `gpt-4o-mini-tts`, voice `ash`: **US$0.27** in total (cap US$1.00). QC: 0 errors; every
`tools/episode_reports.py` check PASS (no black gaps, no frozen picture, captions in sync). One cue ("flying the
world", whose apostrophe does not match) falls back to the scene start; harmless. All 13 claims are `source_located`.
