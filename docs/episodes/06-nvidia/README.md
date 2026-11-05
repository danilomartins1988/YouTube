# Episode 06: How Nvidia Took Over the AI Economy (completion report)

Status: **rendered and validated, not published.** Publishing is manual.

## Videos (in `output/`, not committed)

| File | What it is | Length |
|---|---|---|
| `output/nvidia_documentary.mp4` | **Original cut** from the Episode 06 brief. It is untouched. | 11:38.8 (698.77 s) |
| `output/nvidia_documentary_with_intro.mp4` | Original cut plus the channel intro, spliced in at 0:18.8 after the hook ("…there is one supplier."). No re-render. Its subtitles are in `.srt` next to it. | 11:43.8 (703.77 s) |
| `output/nvidia_documentary_presenter.mp4` | **Revised cut.** Same script and cached narration, with the intro built in and four presenter sequences. | 11:43.8 (703.77 s) |

Light copies for download are the same files with `_light` added to the name.

## Deliverables

| # | Deliverable | Location |
|---|---|---|
| 1 | Final MP4 | see the table above |
| 2 | English script | `scripts/nvidia_documentary.md` (source: `projects/how-nvidia-took-over-the-ai-economy/deliverables/documentary/script.yaml`) |
| 3 | Sources and fact-check log | `research/nvidia_sources.md`. Every claim has a URL, publication date, access date, the period it covers and a status. |
| 4 | Scene-by-scene storyboard | `storyboards/nvidia_storyboard.md` (timestamped) and `storyboards/nvidia_presenter_storyboard.md` |
| 4b | Machine-readable scene manifest | `docs/episodes/06-nvidia/scene_manifest.json` (34 scenes, 153 keyframes, 0 unresolved cues) and `scene_manifest_presenter.json` |
| 5 | Editable Remotion source | `remotion/src/` (technology scenes in `scenes/TechScenes.tsx`, intro in `brand/`, presenter in `presenter/`) |
| 6 | Asset attribution and licence log | `research/nvidia_asset_licenses.md` |
| 7-9 | Title options, description, chapters, keywords, hashtags, end screen, analytics | `docs/episodes/06-nvidia/youtube_package.md` |
| 10 | Technical validation | `reports/nvidia_quality_report.md`, `reports/nvidia_presenter_quality_report.md`, visual QC sheets in `visual_qc/` and `visual_qc_presenter/` |
| 11 | Narration cost | `reports/nvidia_cost_report.md` |
| 12 | Limitations | below |

## Signature animations

1. **CPU vs GPU** (`cpu_gpu`): 192 independent tasks fly into 8 large CPU cores, which work in rounds, and into 192 small GPU cores, which take one step. Then a step-by-step chain shows the reverse trade-off. It is labelled "not a benchmark".
2. **CUDA ecosystem** (`stack`): seven layers build from the bottom up (GPU, drivers, CUDA, libraries, frameworks, developers, applications), with data pulses and the "7.5M+ developers" counter. A second scene animates switching costs (port and retest code, tune again, change tools, retrain teams).
3. **Global supply chain** (`supply_chain`): a map with camera moves.
   - **Route:** Santa Clara (design), then TSMC Hsinchu (wafers) and CoWoS packaging in Taiwan, which is fed by HBM from Korea (SK Hynix, Samsung) and Micron.
   - **Downstream:** assembly in Taiwan, then data centers in the US, Europe and Asia.
   - **Other elements:** a process strip tracks the stages, and a separate shot shows Arizona against Taiwan.
   - **Bottleneck:** packaging chokes, and everything downstream slows and dims.
4. **Financial transformation** (`stacked_columns` + `line_chart`):
   - fiscal-year revenue columns for FY16-FY26;
   - segment columns for FY20-FY26 that morph into a Data Center share view (27% to 90%);
   - a separate gross-margin line for FY16-FY26 with annotations for FY23, FY25 and FY26.
5. **AI chip landscape** (`landscape`): a cursor selects each dimension for NVIDIA GPU, AMD GPU, Google TPU and AWS Trainium (built for, software, where to get it, cost at scale, switching cost). The options then slide onto a conceptual axis from general-purpose to specialised. There are no benchmarks and no winner.

**Also in the episode:**
- an opening ecosystem network (`ai_network`);
- whiteboard hand-drawings (parallel work, the developer flywheel);
- the cost-cap-style compare scenes;
- the "scan" transition.

## Revised cut: presenter sequences (mandatory standard)

| Time | Scene | What the character does |
|---|---|---|
| 1:26 | `p07_draw_parallel` | Draws a pixel grid, one big worker and many small ones, and points out that they work at once (**draws a diagram**) |
| 4:18 | `p15_build_revenue` | Builds the FY16-FY26 revenue bar chart bar by bar, laser-points at FY23 and FY26, and reacts to the jump (**interacts with a chart**) |
| 5:06 | `p17_customers` | Draws NVIDIA and arrows to cloud giants, AI labs and AI factories, then writes 22% and 14% (**explains a business relationship**) |
| 10:46 | `p33_inference` | Draws training, then model, then inference, and points at where custom chips compete |

The intro sits at 0:18, after the hook.

## Voice

OpenAI `gpt-4o-mini-tts`, voice `ash`. The episode was capped at US$1.00.
- **Spent: US$0.2623** (28 requests, original build).
- The revised cut, the intro version and all rebuilds reused the cache and made 0 paid calls.
- Nothing else paid was used.

## Limitations

- **Claims not yet checked by a person.** All 27 cited claims are `source_located`: found on 2026-11-05 but not yet read in full by a named reviewer. Verify them before publishing.
- **Secondary sources.** Google Ironwood, Project Rainier, Anthropic's TPU plans, the Arizona wafer and the capex totals come from trade press or trackers, not first-party pages. They are labelled as such.
- **Latest quarter.** Nvidia's Q3 FY2027 results (quarter ending October 2026) were not out at production time. Q2 FY2027 is the latest quarter used.
- **No images.** No photographs or official images are used: no verified licence was available, and no image-generation integration is authorised. All visuals are original SVG.
- **Handwriting font.** Comic Neue is not installed, so the whiteboard writing falls back to Inter.
- **Presenter reach.** The presenter's arms stretch up to 1.5x (cartoon style) so the marker reaches high strokes. Board content should stay below about y=330 px for natural poses.
- **Visual QC flag.** The safe-margin check flags one frame (4:02). It is the white whiteboard background touching the frame edge, which is intended, not text bleeding off-frame.
