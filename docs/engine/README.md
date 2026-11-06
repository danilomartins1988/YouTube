# Advanced animation engine: technical summary

Status: **implemented, rendered and validated** (2026-11-06). Nothing was published.

## Deliverables

| # | Deliverable | Location |
|---|---|---|
| 1 | 30-second demonstration MP4 (1920×1080, 30 fps, 900 frames) | `output/engine/engine_demo_30s.mp4` (not committed; `python tools/render_engine.py demo`) |
| 2 | Editable Remotion source | `remotion/src/animation-engine/` (composition `EngineDemo` in `examples/EngineDemo.tsx`) |
| 3 | Six reusable components | `AnimatedPresenter/`, `DrawOnCanvas/`, `AnimatedWorldMap/`, `EconomicFlow/`, `AnimatedCharts/`, `ExplodedDiagram/` (+ `transitions/`, `motion/`, `types/`) |
| 4 | One standalone preview per component | `output/engine/previews/Engine{Presenter,Draw,Map,Flow,Charts,ChartsLine,Exploded}.mp4` (`python tools/render_engine.py previews`); source `examples/Previews.tsx`; contact sheet `docs/engine/qa/previews_sheet.jpg` |
| 5 | Technical summary | this file + API docs in `remotion/src/animation-engine/README.md` |
| 6 | Visual QA report | `docs/engine/ENGINE_QA_REPORT.md`, `docs/engine/qa/` (JSON, filmstrips) |
| 7 | Future episode integration | `docs/engine/INTEGRATION.md`; scene types `engine_*`; `docs/PRODUCTION_STANDARD.md` section 1c |
| 8 | Limitations | below |

## What the demo shows (and how it is built)

| Time | Scene | Real motion |
|---|---|---|
| 0–6 s | Presenter | The character walks into a studio (distance-driven gait, anticipation lean, follow-through). The digital board boots. The presenter draws axes, a three-point line and its markers: the marker tip sits on the active stroke, the arm solves IK every frame and the body side-steps. Then it reacts and points at the last point. |
| 6–12 s | Economic flow | The chart's points fly and grow into four stages. A design file is typed on the design screen and travels to the fab (gear turns, beam scans), where it becomes a wafer. At packaging the wafer meets memory and leaves as a chip. In the data centre the LEDs light and it becomes a server. A second unit is pipelined, and payments flow back as coins. |
| 12–18 s | World map | The stages dissolve and their dots fly to their real cities on the map. The California → Taiwan route draws across the Pacific and carries data packets. The camera pulls back and tilts (parallax star field). Europe and US East light up, and chip routes carry chip tokens. Then the camera dives into Taiwan. |
| 18–24 s | Exploded chip | A burst opens into a schematic chip. The camera orbits (yaw) and moves closer. Five layers separate with staggered springs and turn, and labels with leader lines appear. The stack reassembles top-down with overshoot and a flash. |
| 24–30 s | Integration | The chip seeds an economic network (nodes spring out, links draw, packets flow). The nodes drop into place as the bases of an **illustrative** revenue chart. Bars grow, the fastest-growing year is highlighted, and the bars collapse into light streaks. Then the title (letter stagger, underline sweep), the tagline, a light sweep and a gold-line close to black. |

## Engineering choices

- **Deterministic.** Every component is a pure function of `t = frame / fps`. Randomness comes from a seeded
  hash (`rnd`), and springs from Remotion `spring()` evaluated on the frame.
- **Real drawing.** Strokes are revealed by measured path length (`@remotion/paths`). `penAt()` gives the tip
  position, including lifted travel between strokes, and the presenter's hand IK targets it.
- **Reuse.** The articulated rig from `src/presenter/Presenter.tsx` (two-bone IK arms, gait, face) is reused,
  not duplicated. Three optional pose fields were added: `lean` (anticipation and follow-through), `backHand`
  (explaining gestures) and `smile`. Existing scenes do not set them, so their renders are unchanged. The
  Natural Earth geometry and the fast culled path builder (`screenPath`) from `MapScene` are also reused.
- **Real geography.** Coordinates are passed in as lon/lat. The world is drawn as three copies so the camera
  can cross the date line without jumps.
- **Data integrity.** Charts render only the data passed in. The demo's chart is labelled "Illustrative data".
- **Typed props** for every component. Each exposes timing, position, scale, colours, speed, data, paths and
  camera keyframes.
- **Pipeline integration.**
  - Storyboard scene types `engine_draw`, `engine_flow`, `engine_map`, `engine_chart` and `engine_exploded`,
    with narration-cue timing for any time field (`animation-engine/storyboard.tsx`).
  - Python scene models updated.
  - QC counts `engine_draw` as a presenter sequence and warns when fewer than five explanatory animations are
    used (`hiddeneco/qc.py`).
- **Performance.** The 30 s demo renders in about 4 minutes on 4 CPU cores. Map frames are the heaviest
  (three culled world copies).

## Tools

- `python tools/render_engine.py demo | previews | stills <Comp> <frames> <out.jpg> [scale]`
- `python tools/engine_qa.py [video] [out_dir]`: video properties, black and frozen frames, static windows,
  edge clipping, contrast and font size, SVG runtime errors, the numerical motion probe and filmstrips.

## Compatibility

- No existing episode file or video was modified or re-rendered.
- `npx tsc --noEmit` passes.
- An existing presenter scene (Taiwan `p12_process`) was re-previewed after the change and renders as before.

## Limitations (unresolved)

- **Character style.** The presenter is a clean vector rig. It has no fingers, cloth simulation or full facial
  animation (eyes blink, brows lift, mouth talks and smiles). The arm can stretch up to 1.5× to reach high
  strokes (cartoon licence).
- **Writing.** `write` is a handwriting oscillation while the text is revealed. It is not glyph-accurate pen
  paths (no handwriting font with stroke data is installed).
- **Pen accuracy.** The marker tip stays within 9 px of the path. The worst case is a single frame where the
  target passes right next to the shoulder.
- **Map projection.** Web Mercator, with routes as bowed arcs (schematic), not true great circles. The tilt is
  CSS 3D (one plane); there is no terrain or extruded geometry.
- **Exploded diagram.** It is a schematic. Layer order and roles are conceptual, not a to-scale
  cross-section, and it is labelled so on screen.
- **Audio.** The demo is silent (the brief asked for animation only). Episodes add narration, music and SFX
  through the existing pipeline.
- **Storyboard adapters.** These are tested with still renders through the `Documentary` composition (draw,
  flow, map), not yet in a full narrated episode.
- **Taste.** Automated QA proves motion and integrity, not taste. A human should review it at full speed.
