# The Hidden Economics: production standard (default from Episode 06)

Every episode is an original animated economic documentary, not a narrated slideshow. This file is the
reusable standard. `README.md` covers how to run the pipeline; this file covers what a finished episode must be.

## 1. Visual language

- **Animated explanation first.** Motion graphics carry the argument: objects move between places, charts
  grow and change form, diagrams assemble, relationships appear, components separate and combine, and the
  camera moves to reveal new information. Use photographs only when the licence is verified.
- **Narration-driven.** Every animation step is tied to a narration cue (a phrase matched to the word
  timings). When a number is spoken, it appears. When a relationship is explained, it is drawn. When a
  process is described, it unfolds.
- **Pacing.**
  - No shot stays visually unchanged for more than **5 s**.
  - Aim for a meaningful change every 2-4 s, but give viewers time to read complex charts.
  - No meaningless motion added only to pass the rule.
- **Diversity.** Mix scene types across the film:
  - charts and models;
  - maps;
  - technology or process diagrams;
  - 2.5D parallax illustrations;
  - selective whiteboard sequences;
  - cinematic typography.

  Never run the same layout three times in a row.
- **Signature animations.** Each episode names three to five signature animations in its storyboard header and
  reviews each one in visual QC. Signature animations must be built explicitly for the episode, not reused templates.
- **Whiteboard sequences (2-4, only where they teach).**
  - The hand follows the real stroke path, and the drawing builds progressively at narration speed.
  - The hand glides between strokes. It never sweeps over a finished picture.
  - The sketch then colours in or transforms into the film's style.
- **Identity.**
  - One palette per episode, with a fixed meaning for each colour and the same colours used for the same concepts throughout.
  - Restrained gradients and depth. No logos or brand graphics of the companies covered, and nothing that implies affiliation.
- **Scene library.** Use `remotion/src/scenes/*`:
  - data scenes;
  - maps;
  - flows;
  - isometric;
  - race scenes;
  - whiteboard;
  - technology scenes: `ai_network`, `cpu_gpu`, `stack`, `supply_chain`, `stacked_columns`, `landscape`.

  Add new components when a story needs them and register them in `remotion/src/Documentary.tsx`, `hiddeneco/models.py` and `tools/export_episode_docs.py`.

## 1a. Channel intro (permanent, default on)

- **Structure.** Every episode runs: opening hook, then the channel intro, then the documentary, then the conclusion.
- **What it is.** `TheHiddenEconomicsIntro` (`remotion/src/brand/TheHiddenEconomicsIntro.tsx`, composition `Intro`). It is 5 s at 1920x1080 and 30 fps, in a fixed brand palette of navy, charcoal, metallic gold and white.
- **Sound.** An original 5 s sonic signature generated in code by `hiddeneco/intro.py` and stored at `assets/brand/intro_signature.wav`. The music bed is muted underneath it.
- **Placement.**
  - `hiddeneco/intro.py:insert_intro()` adds it automatically at the first scene boundary after about 10 s of narration, which is the natural end of the hook.
  - It never goes before the hook, never inside a sentence, and never twice.
  - To place it after a specific segment, set `intro: {after_segment: <id>}`. To leave it out, set `intro: {enabled: false}` in `project.yaml`, or `intro: false` in a `deliverable.yaml`.
- **Standalone version.** `python tools/render_intro.py` writes `output/brand/the_hidden_economics_intro.mp4`.
- **Already rendered episodes.** `python tools/splice_intro.py <mp4> <timeline.json> <out.mp4>` inserts the intro at the hook boundary under a new filename. The original is never overwritten.

## 1b. Presenter (mandatory: an animated character who explains by drawing)

- **The character.** An original minimalist economist (navy blazer, gold tie, round glasses), drawn with the `presenter` scene type (`remotion/src/presenter/Presenter.tsx`). Its moves:
  - walks in and leaves;
  - walks to the board and draws with a marker whose tip follows the real SVG path;
  - writes labels and builds bar charts bar by bar;
  - points at figures, either by hand or with a laser for distant ones;
  - reacts with a small "aha".
- **Built-in motion.** Inverse-kinematic arms, a walk cycle driven by distance travelled, blinking, and a mouth that moves with the narration.
- **Board items.** Each item is gated by a narration cue:
  - `stroke`, `arrow` and `box` for drawn diagrams, flowcharts, timelines and supply chains;
  - `text` for written labels;
  - `bars` for a chart built bar by bar;
  - `point` (with `laser`) for pointing;
  - `react` for the reaction;
  - `map` (the hand traces country outlines; later items can use `ll: true` to place on lon/lat);
  - `pin` and `bubble` (a marker or a value-sized circle grows while the hand points at it);
  - `shock` (a red disruption travels along a path; boxes it passes turn red and shake);
  - `carry` (the hand moves a labelled token from one place to another).
- **Frequency** (documentaries of 10-15 min, enforced by QC in `hiddeneco/qc.py:check_presenter`). An episode needs at least **3** presenter sequences (an episode brief can raise this with `presenter_min` in `project.yaml`; Episode 07 uses 4) of about 10-25 s each, spread through the film and not back to back, including:
  - one that draws a diagram (boxes, strokes or arrows);
  - one that builds or interacts with a chart or a map (`bars`, `map` or `bubble`);
  - one that explains a business or economic relationship (at least two boxes joined by an arrow).
- **Exemptions.** Missing sequences fail QC. Only projects marked `presenter_exempt: true` (the episodes published before this standard) or deliverables with `presenter: false` are exempt.
- **Demo.** `python tools/render_presenter_demo.py` writes `output/brand/presenter_demo.mp4`.

## 1c. Animation engine (default from 2026-11-06)

Documentaries are animated explanations, not narrated slideshows. Use the reusable engine in
`remotion/src/animation-engine/` (docs: its `README.md`; integration: `docs/engine/INTEGRATION.md`):

- Storyboard scene types:
  - `engine_draw`: the presenter really draws (the marker tip follows the path; IK arm; the body side-steps).
  - `engine_flow`: objects travel and are transformed by each stage; money can flow back.
  - `engine_map`: real geography; routes draw and carry tokens; camera, tilt and parallax.
  - `engine_chart`: build, compare periods, highlight growth, morph into a diagram.
  - `engine_exploded`: a schematic layered object that explodes and reassembles.
- Every time field accepts a narration cue: `{cue: "phrase"}`.
- **For an 11–13 minute documentary:** at least four character-assisted sequences and at least five
  substantial explanatory animations, subject to editorial relevance. QC enforces the first and warns on the
  second.
- **Continuity:** objects morph between scenes (point → stage → city → product). Do not cover a scene change
  with a zoom or slide transition.
- **Charts:** they use only supplied data; label illustrative values on screen.
- **QA:** run `tools/engine_qa.py` (motion energy, frozen and black frames, edges, contrast, motion probe) on
  engine-heavy cuts, and inspect the filmstrips.

## 2. Story

- **Hook.** Grab attention in the first 10-15 seconds with a picture, a surprising fact and an open question. The channel intro follows the hook (see 1a), never before it.
- **Structure: five parts, used internally only (user decision of 2026-11-06, from Episode 09).** Each part still has
  a question, stakes, a conflict, an investigation, a discovery and a transition, but this is a **writing structure,
  not something the viewer is told about**. Never narrate "Mission one", "That is mission two", "Today we have five
  missions", "Here is the discovery" or "Mission complete". Never show a mission HUD, "MISSION n COMPLETE" stamps,
  mission lists or `THE QUESTION / WHY IT MATTERS` labels. Chapter cards show only the chapter title (no "Mission n").
  Episodes 07 and 08 used the older, spoken mission model; do not copy that part from them.
- **Visual style: cartoon first (user decision of 2026-11-06).** The user wants episodes "like a cartoon": bright,
  flat colours, thick outlines, characters and objects that move (ships, anchors, fish, a smiling sun, speech-bubble
  callouts), camera tracking shots. Use `engine_cartoon` (`remotion/src/animation-engine/CartoonOcean/`) or new
  cartoon worlds built the same way for most beats; keep maps for geography and the presenter boards for
  explanations. Plain text cards should be the exception.
- **Hypotheticals.** Any scenario that has not happened is said to be hypothetical in the narration and labelled on screen (red "Hypothetical scenario" banner). Show a real precedent next to it when one exists.
- **Pacing.** Alternate macro context with detailed mechanism. Build curiosity, pause before the reveals, and cut redundant explanation.
- **Balance.** Cover both strengths and risks. Never make it a corporate advert.
- **Ending.** Close on a memorable economic insight and a natural link to the next episode.
- **Teaser rule (from 2026-11-06, user decision).** The closing teaser is **generic** ("Next time, we follow the money
  behind another hidden link of the world economy") unless the user has explicitly chosen the next topic. Never
  promise a specific next episode on Claude's own initiative. (Episode 08 is the exception: its teaser, undersea
  cables, was kept and became Episode 09.)

## 3. Facts and money

- **Sourcing.**
  - Every number comes from a dossier claim (`projects/<slug>/sources.yaml`). The source must have a URL, a publication date, an access date and the period it covers.
  - Typed digits in narration are a build error.
  - Mark anything uncertain as "reportedly" or "estimate". Never invent precision.
- **Money is shown in US dollars.**
  - Convert other currencies with a cited official rate (US Federal Reserve H.10) and mark the result "≈".
- **Label periods.**
  - Fiscal years must be labelled as fiscal years; say when a fiscal year differs from the calendar year.
  - Comparisons across different periods or scopes must say so on screen.
- **Machine-readable scene manifest.** Every episode ships `scene_manifest.json` (`tools/scene_manifest.py`). It records, per scene:
  - the segment and its start and end times;
  - the visual objective and animation type;
  - every keyframe cue resolved to an absolute time;
  - assets, sources, and the transition out.

## 4. Voice and sound

- **Voice.**
  - The existing OpenAI TTS integration (`gpt-4o-mini-tts`, voice `ash`) in natural American English.
  - Hard cap of **US$1.00 per episode**, including retries, set with `budget.max_paid_usd` in `project.yaml`.
  - Run `python -m hiddeneco estimate <slug> --tts openai` before any paid call. Segments are cached; a re-render must make zero paid calls.
- **Sound.**
  - Sound design is generated in code and supports transitions and reveals. Keep music low.
  - Narration loudness should sit around -16 LUFS, with no clipping and no unexplained silences over 2.5 s.

## 5. Quality control (do not equate "it rendered" with "it is good")

1. **Technical checks:** `python tools/episode_reports.py <slug> <name> <deliverable> --video <mp4>`. This covers:
   - resolution, codecs and duration;
   - caption and voice sync;
   - black frames and frozen stretches over 5 s;
   - asset licences.
2. **Visual and audio checks:** `python tools/visual_qc.py <mp4> output/<slug>/<deliverable>/timeline.json <dir> --scenes <signature ids>`. This produces:
   - contact sheets of the whole film, the opening, and each signature animation;
   - safe-margin, duplicate-frame, peak and silence checks.
3. **Review and fix.** Look at every sheet:
   - Redesign any scene that reads like a static slide.
   - Improve any animation that does not explain the narration.
   - Simplify any chart that is hard to read.
   - Then render again. Layout previews are free: `rpreview`-style one-frame-per-scene renders through Remotion.
4. **Full decode:** `ffmpeg -v error -i <mp4> -f null -`.
5. **Intro and presenter check:** the intro appears exactly once, after the hook. The presenter appears, visibly moves, and draws with the hand on the path in at least three sequences (or the episode's `presenter_min`). Inspect those sheets in `tools/visual_qc.py --scenes ...`. If any of this is missing, the episode is not delivered.

## 6. Delivery and growth

- **Episode folder.** Create `docs/episodes/<nn>-<name>/` containing:
  - a completion report with limitations;
  - the YouTube package;
  - the scene manifest;
  - visual QC sheets;
  - links to the script, sources, storyboard, licence log, technical report and cost report.
- **Full video, committed nowhere.** The MP4 lives in `output/` (never committed). Also make a lighter copy for download.
- **YouTube package.**
  - Three accurate title options, an optimised description, keywords and hashtags.
  - Chapters with real timestamps from `timeline.json`.
  - An end-screen recommendation and the analytics to review after publishing.
  - Make no promises about reach.
- **Thumbnails and shorts** only when the brief asks for them.
- **Autonomy.** Production runs end to end without intermediate approvals. **Publishing is always manual.** Never upload.
