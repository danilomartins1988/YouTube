# Using the animation engine in documentaries

The engine is wired into the normal pipeline (`python -m hiddeneco build ...`). In a storyboard, use these scene
types:

| Scene type | Component | Typical use |
|---|---|---|
| `engine_draw` | AnimatedPresenter + DrawOnCanvas (+ Studio, DigitalBoard) | character-assisted diagram, chart or relationship |
| `engine_flow` | EconomicFlow | products, money and royalties moving through an economy |
| `engine_map` | AnimatedWorldMap | supply chains, trade routes, investment races |
| `engine_chart` | BarChart / LineChart / Donut (`chart: bar\|line\|donut`) | revenue growth, market share, margins, period comparisons, chart → diagram |
| `engine_exploded` | ExplodedDiagram | how a product or an organisation is built |

`params` are passed straight to the component (see `remotion/src/animation-engine/README.md`).

**Any time value can be a narration cue**: `{cue: "the phrase", offset: 0.3}`. It resolves to seconds into the
scene, so animation follows the voice. For `engine_map`, add `remotion_geo: [world]` to `project.yaml`.

## Examples

```yaml
- id: s12_flow
  segment: m2_chain
  type: engine_flow
  params:
    title: From design to data center
    cardW: 300
    cardH: 240
    stages:
      - {id: design, label: Chip design, x: 300, y: 560, kind: design, color: blue, appear: {cue: "designs"}, output: blueprint}
      - {id: fab, label: Manufacturing, x: 760, y: 560, kind: fab, color: gold, appear: {cue: "foundry"}, output: wafer}
      - {id: dc, label: Data center, x: 1620, y: 560, kind: datacenter, color: teal, appear: {cue: "data centers"}, output: server}
    links: [{from: design, to: fab, appear: {cue: "sends"}}, {from: fab, to: dc, appear: {cue: "ships"}}]
    items: {starts: [{cue: "sends"}], route: [design, fab, dc], travel: 0.7, process: 0.6}
    money: [{from: dc, to: design, starts: [{cue: "pays"}], label: PAYMENTS}]

- id: p20_draw
  segment: m3_explain
  type: engine_draw
  params:
    title: Why margins rise
    board: {x: 700, y: 180, w: 1120, h: 620}
    draw_start: {cue: "Let's draw"}
    strokes:
      - {d: "M 820 260 L 820 700 L 1700 700", color: muted, speed: 2300}
      - {d: "M 960 620 L 1260 520 L 1560 320", color: gold, width: 7, speed: 950}
    actions:
      - {kind: point, at: {cue: "look at"}, dur: 1.2, target: [1560, 320]}
      - {kind: react, at: {cue: "jumped"}}
```

## Rules for an 11–13 minute documentary (added to docs/PRODUCTION_STANDARD.md)

- **Mission model** (section 2): question, why it matters, conflict, investigation, discovery and transition.
- **Five-second channel intro** after the hook (inserted automatically).
- **At least four character-assisted sequences** (`presenter` or `engine_draw`; `presenter_min: 4`), each with
  genuine progressive drawing. QC counts both types.
- **At least five substantial explanatory animations** (engine scenes or signature scenes: flows, maps with
  routes, transforming charts, exploded diagrams, domino networks). QC warns below five
  (`check_animation_density`).
- Continuity comes from **morphing objects** between scenes (a point becomes a stage, a stage flies to its city,
  a hub opens into a product), not from slide transitions.
- **No fabricated values**: charts render only the data passed in; label illustrative data on screen.
- **Visual QA**: `tools/visual_qc.py` for episodes, plus `tools/engine_qa.py` checks (motion energy, frozen and
  black frames, edges, contrast) for engine-heavy cuts.

Existing documentaries are unchanged. The engine only adds scene types; the character gained three optional
pose fields (`lean`, `backHand`, `smile`) that older scenes do not set.
