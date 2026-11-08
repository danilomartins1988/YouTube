# The Hidden Economics animation engine

Reusable, deterministic Remotion components for **explanatory** animation: things that walk, draw, travel,
transform, build and come apart. Every component is a pure function of `t` (seconds = frame / fps), with no
timers and no `Math.random` (use `rnd(seed)`), so every render is identical.

```
remotion/src/animation-engine/
  AnimatedPresenter/   articulated character state machine (wraps the rig in src/presenter/Presenter.tsx)
  DrawOnCanvas/        progressive stroke drawing + pen timeline + shape builders
  AnimatedWorldMap/    real-geography map camera, highlights, hubs, drawn routes with tokens, tilt + parallax
  EconomicFlow/        stages that process and transform travelling objects; money flowing back
  AnimatedCharts/      BarChart (build / compare / highlight / morph to diagram), LineChart, Donut
  ExplodedDiagram/     layered isometric object that explodes, turns, gets labelled and reassembles
  CartoonOcean/        side-view cartoon sea (ships, cables with light, volcano): stories that happen at sea
  CartoonStage/        topic-specific cartoon worlds: `zones` of sets (city, exchange, newsroom, vault, court, fab,
                       sciencepark, datacenter, beach, web, port, cabin...) + items; used via engine_cartoon `zones`
  tone.tsx             adaptive visual tone: thriller, crisis, strategy, trade, tech, history, reflective, bright
                       (sky, sun/clouds, grade, exposure, vignette, spotlight, alarm pulse, grain, glow); scenes take
                       `tone` + `toneShift: {at, to, dur}`; presenter `demeanor` (serious/neutral/warm). Default = old look
  transitions/         LightSweep, Iris, Burst, Studio set, DigitalBoard, TitleReveal
  motion/              easing, springs, windows, arcs, deterministic noise, palette
  types/               shared types
  examples/            EngineDemo (30 s) + one preview per component
  qa/probe.ts          numerical motion probe used by tools/engine_qa.py
  storyboard.tsx       adapters so hiddeneco storyboards can use the engine (scene types engine_*)
```

Render: `python tools/render_engine.py demo|previews|stills <Comp> <frames> <out.jpg>`.
QA: `python tools/engine_qa.py [video] [out_dir]`.
Compositions: `EngineDemo`, `EnginePresenter`, `EngineDraw`, `EngineMap`, `EngineFlow`, `EngineCharts`,
`EngineChartsLine`, `EngineExploded`. Pass `{geo}` (the world JSON) via `--props`; `render_engine.py` does this.

All coordinates are in a 1920x1080 SVG space. Colours accept palette keys (`gold`, `blue`, `teal`, `ink`,
`muted`, `risk`) or literal hex.

---

## 1. AnimatedPresenter

```tsx
<AnimatedPresenter t={t} floor={960} scale={0.9} startX={-260} talk={[[2, 5]]} actions={[
  {kind: 'enter', from: -260, to: 540, at: 0.25, dur: 1.5},   // walk in (anticipation lean, follow-through)
  {kind: 'draw', timeline},                                     // marker tip follows DrawOnCanvas strokes
  {kind: 'write', at: 5.3, dur: 1.0, x: 900, y: 640, width: 520},
  {kind: 'point', at: 6.5, dur: 1.2, target: [1530, 470]},      // arm rises with overshoot, holds, lowers
  {kind: 'explain', at: 6.6, dur: 1.6},                         // open-hand gesture with the other arm + talking
  {kind: 'react', at: 8.1},                                     // hop, eyebrows, 'aha' marks, then smile
  {kind: 'smile', at: 9, dur: 1},
  {kind: 'exit', to: 2300, at: 9.0, dur: 1.4},
]} />
```

- The rig has a head (eyes with blinking, glasses, eyebrows, mouth that talks and smiles), torso, two-bone IK
  arms with hands, legs with knees and feet. The walk cycle is driven by distance travelled, not by time.
- While drawing, the body side-steps along a smoothed copy of the pen path (never trailing beyond arm reach),
  keeps facing the board, and the marker tip sits on the active stroke. The QA probe measures this
  (mean 0.2 px in the demo).
- `presenterPose(props)` returns the pose for any time. `frontArmWorld(pose)` (from `src/presenter/Presenter.tsx`)
  returns the shoulder, elbow, hand and marker-tip positions in world space, for tests.

## 2. DrawOnCanvas

```tsx
const timeline = buildDrawTimeline([
  {d: shapes.axes(820, 260, 880, 440), speed: 2300, color: 'muted'},
  {d: shapes.polyline([[960, 620], [1260, 520], [1560, 320]]), speed: 950, color: 'gold', width: 7},
  {d: shapes.circle([1560, 320], 15), duration: 0.2, fill: 'gold', label: {text: 'YEAR 3', x: 1560, y: 745, anchor: 'middle'}},
], {start: 1.75, pause: 0.06, liftSpeed: 2400});
<DrawOnCanvas t={t} timeline={timeline} showPen />
```

- Strokes are revealed with `stroke-dasharray` / `stroke-dashoffset` by their measured length (`@remotion/paths`).
- Strokes run sequentially (or at explicit `start` times). Between strokes the pen lifts and travels.
- Options: `speed` (px/s) or `duration`, `pauseAfter`, `ease`, `width`, `color`, `dash` (applied after drawing),
  `fill` (revealed after the stroke), and `label` (written on character by character).
- `penAt(timeline, t)` gives `{pt, down, angle, active}` for hands or pens. `strokeProgress()` gives per-stroke
  progress.
- `shapes`: `line`, `polyline`, `curve` (Catmull-Rom), `circle`, `rect`, `arrow`, `axes`, `timeline`.

## 3. AnimatedWorldMap

```tsx
<AnimatedWorldMap t={t} geo={geo} cameras={[{at: 0, lon: 178, lat: 33, span: 150}, {at: 14.5, lon: 18, lat: 33, span: 340, dur: 2}]}
  tilt={[[12.9, 0], [14.4, 18], [17.25, 0]]}
  highlights={[{iso: 'TWN', color: 'gold', at: 12.85}]}
  hubs={[{id: 'tw', at: [120.99, 24.78], label: 'Taiwan', sub: 'fabrication', color: 'gold', time: 12.8}]}
  routes={[{from: [-121.96, 37.37], to: [120.99, 24.78], at: 13, dur: 1.2, tokenShape: 'packet', tokens: 4, label: 'DESIGNS'}]}
  caption="Real locations (Natural Earth) · routes are schematic" />
```

- The geometry is Natural Earth 1:50m (public domain), from `assets/geo/remotion_world.json`. Every position
  comes from the lon/lat you pass.
- Camera moves ease between keyframes. The centre leads and the zoom follows, in log space.
- The world is drawn three times (−360°, 0, +360°), so the camera and routes can cross the Pacific without jumps.
- Routes draw on as bowed arcs, then carry tokens: `packet`, `box`, `chip`, `coin`, `dot`.
- Depth comes from a parallax star field (25% of the pan speed), an optional CSS 3D tilt and a vignette. The map
  plane is overscanned, so tilting never shows its edges.
- `mapPointAt(cameras, t, lonlat)` gives a screen position, for handing objects into or out of the map.

## 4. EconomicFlow

```tsx
<EconomicFlow t={t} cardW={310} cardH={250}
  stages={[{id: 'design', label: 'Chip design', x: 300, y: 560, kind: 'design', color: 'blue', appear: 6.85, output: 'blueprint'}, ...]}
  links={[{from: 'design', to: 'fab', appear: 7.1}, ...]}
  items={{starts: [7.35, 8.55], route: ['design', 'fab', 'pack', 'dc'], travel: 0.6, process: 0.55}}
  inputs={[{stage: 'pack', at: 9.4, from: [1180, 300], shape: 'box', label: 'memory'}]}
  money={[{from: 'dc', to: 'design', starts: [11, 11.25, 11.5], label: 'PAYMENTS'}]} />
```

- Stage kinds: `design`, `fab`, `package`, `datacenter`, `bank`, `customer`, `warehouse`, `company`. Each has a
  procedural icon that works while it processes:
  - `design`: screen lines type in;
  - `fab`: the gear turns, a beam scans and smoke rises;
  - `package`: the press stamps;
  - `datacenter`: LEDs blink.
- A progress bar fills while a stage processes, and the card glows.
- Items travel along arcs with a fading trail and squash and stretch. They enter a stage and leave as that
  stage's `output` form: `blueprint`, `wafer`, `chip`, `server`, `coin`, `box`, `packet`.
- `inputs` merge into a stage (for example, memory joining at packaging). `money` sends coins back (payments,
  royalties).

## 5. AnimatedCharts

```tsx
<BarChart t={t} data={[{label: 'Y1', value: 12}, ...]} box={{x: 560, y: 330, w: 800, h: 460}} start={26} title="Revenue by year"
  note="Illustrative data" valuePrefix="$" valueSuffix="bn" highlight="growth"
  dataB={...} changeAt={2.8} periodLabels={['YEAR 1', 'YEAR 2']}
  morph={{at: 6, boxes: [{x, y, w, h, label, sub}, ...], arrows: [[0, 1], [1, 2]]}} />
<LineChart t={t} data={...} box={...} draw={2.4} area />
<Donut t={t} data={...} cx={1480} cy={580} dataB={...} changeAt={4.5} />
```

- Values come only from `data` and `dataB`: the components never invent numbers. Use `note` to label
  illustrative data.
- Bars grow with a staggered spring. Value labels count up. `highlight: 'growth'` finds and marks the largest
  period-on-period increase. `dataB` re-animates every bar to a second period.
- `morph` turns each bar into a labelled box of a business diagram, then draws the arrows.

## 6. ExplodedDiagram

```tsx
<ExplodedDiagram t={t} layers={[{label: 'Silicon die', sub: 'billions of transistors', kind: 'die', color: 'blue', thickness: 14}, ...]}
  cx={960} cy={610} scale={[[18, 0.25], [18.8, 1.25], [21.6, 1.45]]} yaw={[[18, 10], [24, 75]]}
  explodeAt={19} labelsAt={19.9} assembleAt={22.2} explodeGap={62} note="Schematic, not to scale" />
```

- Rotatable isometric camera: `yaw` and `scale` keyframes, plus `pitch`.
- Layers separate with staggered springs (bottom to top). Each turns slightly while separated. Labels and
  leader lines appear, then the layers reassemble top-down with overshoot and settle, and a soft flash.
- Surface kinds: `substrate` (traces), `bumps` (contact grid), `die` (core grid with active cores),
  `interconnect` (wiring), `lid` (metal with a moving sheen), `plain`.
- It is a **schematic** (conceptual roles), not a physical cross-section. Say so on screen.

## Transitions and set pieces (`transitions/`)

- `Studio`: dark set with drifting light.
- `DigitalBoard`: the frame draws, a scan line passes, then the grid fades in.
- `LightSweep`: a cinematic light band crosses the frame.
- `Iris`: open or close.
- `Burst`: particles, for when an object opens into the next scene.
- `TitleReveal`: letter stagger plus an underline sweep.

The real continuity between scenes should come from **morphing objects**:
- a chart point becomes a stage;
- a stage flies to its city (`mapPointAt`);
- a hub opens into a chip.

`EngineDemo.tsx` shows each pattern.

## Using the engine in an episode storyboard

Scene types `engine_draw`, `engine_flow`, `engine_map`, `engine_chart` and `engine_exploded` pass `params`
straight to the components. **Any time value can be a narration cue**, `{cue: "phrase", offset: 0.3}`, and it is
resolved to seconds before rendering. See `docs/engine/INTEGRATION.md`.
