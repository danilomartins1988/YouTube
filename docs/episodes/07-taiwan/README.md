# Episode 07: Why Taiwan Matters So Much to the Global Economy (completion report)

Status: **rendered and validated, not published.** Publishing is manual.

## Video (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/taiwan_documentary.mp4` | Final cut: 1920x1080, 30 fps, H.264/AAC, −16.1 LUFS, true peak −4.2 dBFS. Intro and presenter built in. Subtitles: `output/why-taiwan-matters/documentary/subtitles.srt` | 11:53.5 (713.5 s) |
| `output/taiwan_documentary_light.mp4` | 1280x720 copy of the same cut (19.9 MB), for download | 11:53.5 |

## Mission structure (new standard: `docs/PRODUCTION_STANDARD.md`, section 2)

| Time | Part | Question → discovery |
|---|---|---|
| 0:00 | Hook | "What if one of the world's most important industries depended on an island smaller than Switzerland?" |
| 0:16 | Channel intro (5 s, exactly once) | |
| 0:21 | Mission roadmap | five missions announced |
| 0:38 | Mission 1 | How did Taiwan become essential? → the foundry model; TSMC 72.5% of foundry revenue |
| 2:30 | Mission 2 | Why can't everyone make chips? → EUV, yield, capex; Taiwan 18% of all capacity but 69% below 10 nm |
| 5:10 | Mission 3 | Who depends on Taiwan? → designers vs makers; not every industry equally |
| 7:31 | Mission 4 | What if supply were disrupted? → **labelled hypothetical**, 2021 shortage as real precedent, Bloomberg scenario estimates |
| 9:32 | Mission 5 | Can the world spread the risk? → US, Japan, Germany/EU, Korea; Taiwan still 47% in 2032 (forecast) |
| 11:12 | Payoff + teaser | "Mission complete" |

Every mission has question, why it matters, conflict, investigation, discovery and transition beats (see `scripts/taiwan_documentary.md`).

## Presenter sequences (4, all with progressive drawing)

| Time | Scene | Length | What the character does |
|---|---|---|---|
| 2:45 | `p12_process` (A) | 22.9 s | Draws the manufacturing process: design → wafer fab → package → test, with a circuit, a wafer, chip + memory and a check mark |
| 5:24 | `p21_map` (B) | 24.7 s | Traces Taiwan and the US on a world map, pins TSMC and NVIDIA/Apple/AMD, draws the design and finished-chip arrows |
| 8:39 | `p31_chain` (C) | 21.5 s | Draws a supply chain, breaks the first link, and drives a red shock down the chain (boxes turn red) |
| 9:44 | `p36_race` (D) | 23.1 s | Traces the US and Japan and grows investment bubbles (CHIPS Act, TSMC Arizona $165bn, Kumamoto $20bn+) |

## Signature animations

1. **Timeline → network** (`s07_timeline_network`, 1:08): 1987 TSMC, its backers and 1993 Nvidia on a time axis; the dots fly to their places on a world map and link to Hsinchu.
2. **Manufacturing diagram built by the character** (`p12_process`, 2:45).
3. **Global dependency network map** (`s23_dependency`, 6:17): chips from Taiwan to clouds in the US/Europe/Asia, device makers and carmakers.
4. **Domino-effect disruption** (`s30_domino`, 8:09): red "Hypothetical scenario" banner; the shock spreads depth by depth, with the 2021 precedent panel.
5. **Race-to-diversify map** (`p36_race`, 9:44 + `s37_race_map`, 10:07): investment bubbles, then Dresden, the EU 20% target, Korea and Taiwan.

## Deliverables

| Deliverable | Location |
|---|---|
| Final MP4 | see above |
| Script | `scripts/taiwan_documentary.md` (source: `projects/why-taiwan-matters/deliverables/documentary/script.yaml`) |
| Mission storyboard | `storyboards/taiwan_storyboard.md`; generator `tools/gen_taiwan_storyboard.py` → `storyboard.yaml` |
| Scene manifest | `docs/episodes/07-taiwan/scene_manifest.json` (42 scenes, 192 keyframes) |
| Remotion project | `remotion/src/` (new: `TimelineNetwork`, `Domino` in `scenes/TechScenes.tsx`) |
| Character components | `remotion/src/presenter/Presenter.tsx` (new items: `map`, `pin`, `bubble`, `shock`, `carry`; catch-up timing) |
| Sources and fact-check log | `research/taiwan_sources.md` |
| Asset attribution | `research/taiwan_asset_licenses.md` |
| YouTube materials | `docs/episodes/07-taiwan/youtube_package.md` (3 titles, description, chapters, keywords, hashtags, hook, pinned comment, end screen) |
| TTS cost report | `reports/taiwan_cost_report.md` |
| QA report | `reports/taiwan_quality_report.md`; visual QC sheets in `docs/episodes/07-taiwan/visual_qc/` |

## QC results

- Pipeline QC: 0 errors. Warnings are number words outside placeholders (mission numbers and years written in words, checked) and three slow-pace segments.
- Intro appears exactly once (0:16). Presenter: 4 sequences, all between 21.5 and 24.7 s, all drawing on the board.
- Static picture: none over 4 s in the final render (two earlier ones were fixed). No black gaps, no audio clipping, no silences over 2.5 s.
- All assets on the licence allowlist.

## Voice

OpenAI `gpt-4o-mini-tts`, voice `ash`. Cap US$1.00. **Spent: US$0.3040** (40 requests, including 4 re-syntheses for trimmed lines). Nothing else paid was used.

## Limitations

- **Claims not yet checked by a person.** All 21 cited claims are `source_located`; verify before publishing.
- **Secondary sources** for some figures: TSMC customer shares (CNA/Taiwan News), ASML 2025 shipments (trade press), AlixPartners (press coverage), the CHIPS Act (CFR explainer), ESMC (TrendForce). The Bloomberg figures are scenario estimates.
- AMD's use of TSMC is stated as general knowledge; it has no dedicated claim in the dossier.
- Three cue words fell back to default timing (`most of the world`, `below ten nanometers`, `This is The Hidden Economics`); the visuals still land within the right sentence.
- The presenter can stand in front of a label for a moment while writing next to it (e.g. the end of `p12_process`).
