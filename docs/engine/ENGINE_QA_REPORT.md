# Animation engine: visual QA report

Video: `output/engine/engine_demo_30s.mp4` (not committed; regenerate with `python tools/render_engine.py demo`).
QA: `python tools/engine_qa.py`. Raw results are in `docs/engine/qa/engine_qa.json`, the filmstrips (8
consecutive frames, 0.1 s apart) in `docs/engine/qa/filmstrips/`, and the preview contact sheet in
`docs/engine/qa/previews_sheet.jpg`.

Result: **all 18 automated checks pass.** Every number below was measured from the rendered file or from the
engine's own geometry, not assumed from a successful render.

## File

| Check | Result |
|---|---|
| MP4 exists | yes, 8.2 MB, H.264 |
| Duration | **30.000 s, 900 frames** |
| Resolution | **1920 × 1080** |
| Frame rate | 30 fps |

## Picture integrity

| Check | Method | Result |
|---|---|---|
| Blank or black frames | ffmpeg `blackdetect` (d=0.1 s, pix_th=0.06) | none; the final 0.45 s fade is intended |
| Frozen picture | ffmpeg `freezedetect` (>1 s) | none |
| Static stretches | mean absolute frame difference at 10 fps, in 0.5 s windows (threshold 0.15) | **no static window**; quietest is 0.17 (title hold) |
| Edge clipping | bright pixels in a 3 px border, outside the full-bleed map | none |
| Broken SVG / runtime errors | 10 stills rendered with verbose browser logs, scanned for NaN, invalid attributes and errors | none |
| Text readability | WCAG contrast on the background: ink 16.8, gold 9.1, teal 9.8, blue 7.4, muted 6.5 (on panels: 15.3 / 8.3 / 5.9); smallest font in the engine is 18 px | AA everywhere |

Motion energy per scene (mean / quietest 0.5 s window):

| Scene | Mean | Quietest |
|---|---|---|
| 1, presenter draws | 1.53 | 0.30 |
| 2, economic flow | 1.36 | 0.36 |
| 3, world map | 3.00 | 0.26 |
| 4, exploded chip | 1.69 | 0.41 |
| 5, network → chart → title | 1.50 | 0.17 |

## Motion probe (engine geometry, `remotion/src/animation-engine/qa/probe.ts`)

| Behaviour | Measurement | Result |
|---|---|---|
| Presenter walks | body x −260 → 540 px over 1.5 s | pass |
| Anticipation and follow-through | lean −4.2° as it starts, +4.1° mid-walk, settles on stop | pass |
| Hand follows the drawing | marker-tip distance to the active stroke over 57 drawing frames: **mean 0.21 px, max 9.0 px** | pass |
| Arm actually moves | elbow travels 842 px horizontally and 275 px vertically while drawing | pass |
| Body follows the pen | 839 px of side-stepping during the drawing | pass |
| Drawing is progressive | total revealed stroke length never decreases (sampled every 0.05 s) | pass |
| Pointing | hand reaches the chart's last point exactly (0 px) | pass |
| Map camera | lon/lat/span changes through 4 distinct states; Taiwan moves 230 → 1542 px across the frame | pass |

## Defects found by QA and fixed before the final render

1. **Drawing hand lost the path (max 53 px).** As the body followed the pen back to the left, the character
   turned to face its walking direction, which put the drawing arm on the wrong side. Fix: a character that is
   drawing or pointing keeps facing its target and side-steps. The smoothed body is also clamped to arm reach.
   After the fix: mean 0.21 px.
2. **Pointing missed the target (161 px).** The chart took until 5.9 s to draw, so the point overlapped the
   exit. Fix: faster axes, the dots marked in reverse order (short pen lifts) and a faster lift speed. The
   drawing now ends at 4.47 s and the hand lands on the target.
3. **Tilted map showed its edges** (trapezoid corners). Fix: an overscanned map plane, with the tilt applied
   only after the scene hand-off and levelled before the dive.
4. **Dive to Taiwan drifted off-centre** (pan and zoom interpolated at the same rate). Fix: the camera centre
   leads and the zoom follows in log space.
5. **Exploded stack rose into the title.** Fix: the stack stays centred on its live mid-height while it
   separates.
6. **Flow → map hand-off left shrunken cards behind.** Fix: the cards dissolve and their coloured dots fly to
   the real city positions (`mapPointAt`).
7. **"FASTEST GROWTH" collided with a value label.** It was moved above the growth arrow.
8. **Coin glyph at 16 px** failed the 18 px rule. It is now 18 px.

## Manual inspection (filmstrips)

- `1_presenter_draws`: the arm, hand and marker track the line point by point, and the body steps along.
- `2_flow_processing`: the blueprint, wafer and chip move along the arcs (trails, squash and stretch). The
  stages glow and the progress bars fill. Memory merges at packaging.
- `3_routes`: the trans-Pacific route draws from California to Taiwan, then turns into a dashed lane with
  packets.
- `4_explode`: five layers separate with staggered springs and turn. Labels and leader lines follow.
- `5_bars`: network nodes drop to the baseline, bars grow in sequence, and the fastest-growing year is marked.

## Not verified automatically

- Aesthetic judgement (timing taste, composition). This needs a human viewing at full speed.
- Exact readability on small phone screens. The 18 px minimum is sized for 1080p.
