# Episode 08: The Machine Only One Company on Earth Can Build (completion report)

Status: **rendered, fact-checked by AI against the sources, validated; not published.** Publishing is manual, and a named
human reviewer should still sign off the claims (see `FACT_CHECK.md`).

## Video (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/asml_documentary.mp4` | Final cut: 1920x1080, 30 fps, H.264/AAC, −16.2 LUFS. Intro after the hook; subtitles in `output/the-machine-only-one-company-can-build/documentary/subtitles.srt` | 11:05 |
| `output/asml_documentary_light.mp4` | 1280x720 copy for download | 11:05 |

First episode built on the **animation engine** (`remotion/src/animation-engine/`, scene types `engine_*`).

## Mission structure

| Time | Part |
|---|---|
| 0:00 | Hook: "What if the most advanced chips on Earth could only be printed by one machine…" (turning schematic machine, zoom into Veldhoven) |
| 0:19 | Channel intro (once) |
| 0:39 | Mission 1, what the machine does: presenter draws lithography; pen drawings of the tin-plasma light source and the mirror path in vacuum |
| 2:49 | Mission 2, how one company ended up alone: timeline; presenter draws the 2012 customer co-investment; timeline → network (Cymer, Zeiss) |
| 5:10 | Mission 3, who builds it: exploded machine (schematic modules); supplier map (Zeiss Oberkochen/Wetzlar, Cymer San Diego); "built twice" flow |
| 6:52 | Mission 4, how it makes money: presenter draws a bar chart (sales, profit, EUV); per-machine maths; sales by customer location; money loop |
| 8:44 | Mission 5, where the machine may go: export map with a blocked route to China; presenter draws the export-licence gate; cost of the gate |
| 10:21 | Payoff ("mission complete") and teaser (undersea cables) |

## Presenter sequences (4, `engine_draw`, all drawing on the board)

| Time | Scene | Length | What the character does |
|---|---|---|---|
| 0:54 | `p06_draw` | 15.2 s | draws light → mask → lens → wafer, then steps aside and points |
| 3:41 | `p15_bet` | 24.0 s | explains, then draws Intel/TSMC/Samsung → ASML with "23% stake + research funding" |
| 7:06 | `p28_sales` | 23.6 s | draws a bar chart: $37.0bn sales, $10.8bn profit, $13.1bn from 48 EUV machines |
| 9:26 | `p36_gate` | 21.3 s | draws supply network → gate → buyers, one arrow crossed out |

## Explanatory animations (engine and signature scenes)

Exploded machine (×2), pen-drawn light source and mirror path, timeline → network, supplier map, export map with a blocked route, payoff map, "built twice" flow, money loop, sales-by-location bar chart.

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
