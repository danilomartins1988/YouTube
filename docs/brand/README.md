# Brand system: channel intro and presenter

Both are permanent parts of the production standard (`docs/PRODUCTION_STANDARD.md` §1a and §1b).

## 1. Channel intro: `TheHiddenEconomicsIntro`

| Item | Where |
|---|---|
| Editable Remotion component | `remotion/src/brand/TheHiddenEconomicsIntro.tsx` (composition `Intro`; scene type `channel_intro`) |
| Original audio signature | `assets/brand/intro_signature.wav`, synthesised by `hiddeneco/intro.py:signature()` (no samples, no paid API) |
| Standalone 5 s MP4 | `output/brand/the_hidden_economics_intro.mp4` (not committed; rebuild with `python tools/render_intro.py`) |
| Integration module | `hiddeneco/intro.py:insert_intro()`, called by `hiddeneco/pipeline.prepare()` |
| Re-edit of an already rendered video | `python tools/splice_intro.py <mp4> <timeline.json> <out.mp4> [--srt subtitles.srt]` |
| Tests | `tests/test_intro.py` (placement after the hook, no duplicates, disable switch, 5.000 s audio without clipping) |

**Sequence (5.000 s, 150 frames at 30 fps, 1920x1080):**
- **0.0-1.5 s:** out of darkness, a perspective globe of about 900 points turns slowly. Gold arcs draw between 20 financial centres and trade hubs, and parallax dust drifts at three depths.
- **1.5-3.0 s:** the network accelerates, collapses into the centre with converging light streaks, and releases a controlled gold pulse at 2.92 s.
- **3.0-5.0 s:**
  - **3.0 s:** "THE HIDDEN ECONOMICS" is revealed through a mask from the centre outward, in metallic gold with a moving sheen and tightening letter-spacing.
  - **3.3 s:** a gold rule draws out from the centre.
  - **3.55 s:** the tagline rises into place.
  - **3.6-4.6 s:** the full composition holds, so the tagline is readable.
  - **4.62-5.0 s:** smooth fade to dark for the hand-off into the documentary.

**Sonic identity:**
- **0-2.95 s:**
  - a filtered noise swell;
  - gliding sub and octave tones;
  - soft electronic plucks (an A-minor arpeggio) that speed up into the hit.
- **2.75-3.0 s:** a reverse swell.
- **3.0 s:** a pitched sub impact synchronised with the title reveal.
- **3.04, 3.32 and 3.60 s:** a three-note gold-bell motif (A5, E6, D6), which is the memorable signature.
- **From 3.0 s:** a resolving A-major pad, with the tail faded by 5.0 s.

When the intro is placed inside an episode, the music bed is muted underneath it.

**Validation (standalone MP4):**

| Check | Result |
|---|---|
| Duration / frames | 5.000 s, 150 frames, 30/1 fps |
| Resolution / codecs | 1920x1080 (16:9), H.264 yuv420p BT.709, AAC 48 kHz |
| Loudness / peak | -15.5 LUFS integrated, -1.5 dBFS true peak (no clipping) |
| Decode | `ffmpeg -v error ... -f null -`: no errors |
| Blank frames | Only the intended darkness in the first frames and the deliberate final fade |
| Frames inspected | 0.6, 1.2, 1.9, 2.6, 3.2 and 4.2 s, plus a crop of the title. Fixes made after inspection: <br>- the title clipped at the frame edges (font size and tracking reduced); <br>- the globe was too large and too faint (radius reduced, points brightened); <br>- some arcs looped between neighbouring cities (link set revised); <br>- leftover network dots showed behind the title (removed after 3.3 s). |

**Structure of every new episode:** opening hook, then intro, then documentary, then conclusion.
- **Placement.** The intro goes in automatically at the first scene boundary after about 10 s of narration, never inside a sentence and never twice.
- **Overrides.** `intro: {enabled: false}` or `intro: {after_segment: ...}` in `project.yaml`, or `intro: false` in a `deliverable.yaml`.
- **Python-only renderer.** Projects that do not use the Remotion renderer skip the intro.
- **Episodes already published.** The four published episodes (Switzerland, Dubai, Norway, Formula 1) are marked `intro: {enabled: false}`, so a rebuild reproduces them exactly. Setting it to `true` re-edits them with the intro; nothing was re-rendered.

## 2. Presenter and drawing system

| Item | Where |
|---|---|
| Character + scene | `remotion/src/presenter/Presenter.tsx` (`Character`, `PresenterScene`; scene type `presenter`) |
| Demo | `output/brand/presenter_demo.mp4` (18 s; `python tools/render_presenter_demo.py`). It shows: walking in, a drawn flowchart, labels, a bottleneck point, an "aha" reaction, a bar chart built bar by bar, a laser point, and walking off. |
| QC rule | `hiddeneco/qc.py:check_presenter` |

**Character.** An original minimalist economist: navy blazer, white shirt, gold tie, round gold glasses, dark hair, charcoal trousers. It is fully procedural SVG:
- inverse-kinematic arms (two bones each);
- a walk cycle driven by distance travelled, with bob and shadow;
- blinking, and a mouth that moves with the narration's word timings;
- eyebrow and "aha" marks for reactions.

**Drawing.**
- **Strokes, arrows and boxes:** the marker tip sits at `getPointAtLength` of the path while the stroke dash reveals the same length. The hand is on the line being drawn.
- **Labels:** written left to right as the hand moves along the baseline.
- **Bars:** each bar's outline is drawn upward by the hand, then filled and labelled.
- **Narration cues:** every item can wait for one. The character walks to each next item, standing on the side that keeps finished work visible, and steps back to a rest spot when done.

**Nvidia revised cut.** Four sequences, built with this system:

| Sequence | What it does |
|---|---|
| `p07_draw_parallel` | Draws a pixel grid and workers |
| `p15_build_revenue` | Builds the fiscal-year revenue chart and points at FY23 and FY26 |
| `p17_customers` | Draws how Nvidia is paid and the customer-concentration boxes and arrows |
| `p33_inference` | Draws the training, model and inference chain, and points at where custom chips compete |
