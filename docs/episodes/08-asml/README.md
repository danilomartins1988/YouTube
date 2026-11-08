# Episode 08: The Machine Only One Company on Earth Can Build (completion report)

Status: **rendered, fact-checked by AI against the sources, validated; not published.** Publishing is manual, and a named
human reviewer should still sign off the claims (see `FACT_CHECK.md`).

## Video (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/asml_documentary.mp4` | Final cut: 1920x1080, 30 fps, H.264/AAC, −16.2 LUFS. Intro after the hook; subtitles in `output/the-machine-only-one-company-can-build/documentary/subtitles.srt` | 11:12 |
| `output/asml_documentary_light.mp4` | 1280x720 copy for download | 11:12 |

**Cartoon redo (2026-11-08):** 19 scenes rebuilt as bespoke CartoonStage worlds (chip fab, Dutch town, tin-droplet
light source, supplier map, export gate). Mission sentences removed from the narration (structure internal only);
payoff chapter "The lesson"; generic teaser. Numbers unchanged. Generator: `tools/gen_asml_storyboard.py`.

## Structure (internal; cards show the title only)

| Time | Part |
|---|---|
| 0:00 | Hook: "What if the most advanced chips on Earth could only be printed by one machine…" (cartoon fab, one huge machine) |
| 0:19 | Channel intro (once) |
| 0:24 | What the machine does |
| 2:45 | How one company ended up alone |
| 5:05 | Who builds it |
| 6:52 | How it makes money |
| 8:46 | Where the machine may go |
| 10:26 | The lesson (payoff) and generic teaser |

## Presenter sequences (4, `engine_draw`, all drawing on the board)

| Time | Scene | Length | What the character does |
|---|---|---|---|
| 0:41 | `p06_draw` | 15.2 s | draws light → mask → lens → wafer, then steps aside and points |
| 3:40 | `p15_bet` | 24.0 s | explains, then draws Intel/TSMC/Samsung → ASML with "23% stake + research funding" |
| 7:06 | `p28_sales` | 23.6 s | draws a bar chart: $37.0bn sales, $10.8bn profit, $13.1bn from 48 EUV machines |
| 9:28 | `p36_gate` | 21.3 s | draws supply network → gate → buyers, one arrow crossed out |

## Explanatory animations (engine and signature scenes)

Cartoon fab with the lithography machine, tin droplets hit by lasers, mirror path in vacuum, Dutch town, timeline → network, supplier map, export map with a blocked route, money loop, presenter bar chart.

## Deliverables

| Deliverable | Location |
|---|---|
| Script | `scripts/asml_documentary.md` (source `projects/the-machine-only-one-company-can-build/deliverables/documentary/script.yaml`) |
| Storyboard | `storyboards/asml_storyboard.md`; generator `tools/gen_asml_storyboard.py` |
| Scene manifest | `docs/episodes/08-asml/scene_manifest.json` |
| Sources | `research/asml_sources.md` |
| Fact-check log | `docs/episodes/08-asml/FACT_CHECK.md` |
| Asset licences | `research/asml_asset_licenses.md` |
| YouTube package | `docs/episodes/08-asml/youtube_package.md` |
| Cost and QA reports | `reports/asml_cost_report.md`, `reports/asml_quality_report.md`, `docs/episodes/08-asml/visual_qc/` |

## Voice

OpenAI `gpt-4o-mini-tts`, voice `ash`, under the US$1.00 cap. Spent **US$0.3516** in total, including re-synthesis of the
sentences corrected after the fact-check. Nothing else paid.

## Limitations

- All 24 claims are `source_located`. The AI fact-check read every source (see `FACT_CHECK.md`), but the channel
  rule still requires a named human reviewer.
- The High-NA price is an estimate ($300–400 million), and it is labelled as one.
- The machine is a schematic of its conceptual modules, not its physical layout. This is stated on screen.
- Euro figures are converted at the ECB 2025 average (1.13); the narration says so.
