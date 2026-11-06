import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {AnimatedPresenter, PresenterAction} from '../AnimatedPresenter/AnimatedPresenter';
import {BarChart} from '../AnimatedCharts/AnimatedCharts';
import {AnimatedWorldMap, MapCamera, mapPointAt} from '../AnimatedWorldMap/AnimatedWorldMap';
import {DrawOnCanvas, buildDrawTimeline, shapes} from '../DrawOnCanvas/DrawOnCanvas';
import {EconomicFlow, FlowStage} from '../EconomicFlow/EconomicFlow';
import {ExplodedDiagram, Layer} from '../ExplodedDiagram/ExplodedDiagram';
import {E, ENGINE_PALETTE as P, FONT, clamp, lerp, lerpV, life, quadPt, rnd, win} from '../motion';
import {Burst, DigitalBoard, Iris, LightSweep, Studio, TitleReveal} from '../transitions';
import type {Vec, WorldGeo} from '../types';

/**
 * 30-second engine demonstration (1920x1080, 30 fps, 900 frames). Five connected scenes; each hands its objects
 * to the next one instead of cutting:
 *   0-6   presenter walks in, the board boots, the presenter DRAWS a three-point chart and points at it
 *   6-12  the chart's points become the stages of a semiconductor supply chain; objects travel and transform
 *  12-18  the stages fly to their real cities on a tilted world map; routes draw and carry tokens
 *  18-24  the camera dives into Taiwan; a schematic chip explodes into layers, turns, and reassembles
 *  24-30  the chip seeds an economic network that becomes a growing chart, then the channel title
 * The chart values are ILLUSTRATIVE and labelled as such on screen.
 */
export type EngineDemoProps = {geo: WorldGeo};
export const DEMO_SECONDS = 30;

// ---------------------------------------------------------------- scene 1 layout
const FLOOR = 960, PS = 0.9;
const CH = {A: [960, 620] as Vec, B: [1260, 520] as Vec, C: [1560, 320] as Vec};
export const chartStrokes = () => buildDrawTimeline([
  {d: shapes.axes(820, 260, 880, 440), speed: 2300, color: 'muted', width: 5},
  {d: shapes.polyline([CH.A, CH.B, CH.C]), speed: 950, color: 'gold', width: 7},
  // the pen is already at the last point: mark the points on the way back (short lifts)
  {d: shapes.circle(CH.C, 15), duration: 0.2, color: 'gold', width: 6, fill: 'gold', fillOpacity: 0.9, label: {text: 'YEAR 3', x: CH.C[0], y: 745, size: 24, color: 'muted', anchor: 'middle'}},
  {d: shapes.circle(CH.B, 15), duration: 0.2, color: 'gold', width: 6, fill: 'gold', fillOpacity: 0.9, label: {text: 'YEAR 2', x: CH.B[0], y: 745, size: 24, color: 'muted', anchor: 'middle'}},
  {d: shapes.circle(CH.A, 15), duration: 0.2, color: 'gold', width: 6, fill: 'gold', fillOpacity: 0.9, label: {text: 'YEAR 1', x: CH.A[0], y: 745, size: 24, color: 'muted', anchor: 'middle'}},
], {start: 1.75, pause: 0.06, liftSpeed: 2400});

// ---------------------------------------------------------------- scene 2 layout
const STAGES: FlowStage[] = [
  {id: 'design', label: 'Chip design', sub: 'blueprint', x: 300, y: 560, kind: 'design', color: 'blue', appear: 6.85, output: 'blueprint'},
  {id: 'fab', label: 'Manufacturing', sub: 'wafer fab', x: 740, y: 560, kind: 'fab', color: 'gold', appear: 6.95, output: 'wafer'},
  {id: 'pack', label: 'Packaging', sub: 'chip + memory', x: 1180, y: 560, kind: 'package', color: 'teal', appear: 7.05, output: 'chip'},
  {id: 'dc', label: 'Data center', sub: 'AI compute', x: 1620, y: 560, kind: 'datacenter', color: 'blue', appear: 7.15, output: 'server'},
];
const STAGE_FROM: Record<string, Vec> = {design: CH.A, fab: CH.B, pack: CH.C, dc: CH.C};

// ---------------------------------------------------------------- scene 3 layout (real coordinates)
export const LL = {santaClara: [-121.96, 37.37] as Vec, hsinchu: [120.99, 24.78] as Vec, frankfurt: [8.68, 50.11] as Vec, ashburn: [-77.49, 39.04] as Vec};
export const CAMS: MapCamera[] = [
  {at: 0, lon: 178, lat: 33, span: 150},
  {at: 14.5, lon: 18, lat: 33, span: 340, dur: 2.0},
  {at: 17.25, lon: 120.99, lat: 24.4, span: 9, dur: 1.0},
];
const EU = ['DEU', 'FRA', 'NLD', 'BEL', 'ITA', 'ESP', 'POL', 'AUT', 'IRL', 'CZE', 'SWE', 'DNK', 'PRT', 'FIN'];

// ---------------------------------------------------------------- scene 4
const LAYERS: Layer[] = [
  {label: 'Package substrate', sub: 'routes signals to the board', kind: 'substrate', color: 'teal', thickness: 18, size: 250},
  {label: 'Micro-bumps', sub: 'thousands of tiny contacts', kind: 'bumps', color: 'muted', thickness: 7, size: 200},
  {label: 'Silicon die', sub: 'billions of transistors', kind: 'die', color: 'blue', thickness: 14, size: 200},
  {label: 'Wiring layers', sub: 'connect the transistors', kind: 'interconnect', color: 'gold', thickness: 9, size: 200},
  {label: 'Heat spreader', sub: 'carries heat away', kind: 'lid', color: 'muted', thickness: 15, size: 230},
];

// ---------------------------------------------------------------- scene 5
const NET = Array.from({length: 16}, (_, i) => {
  const a = (i / 16) * Math.PI * 2 + rnd(i) * 0.25, r = 260 + rnd(i + 20) * 190;
  return {p: [960 + Math.cos(a) * r * 1.35, 540 + Math.sin(a) * r * 0.82] as Vec, at: 24.2 + rnd(i + 50) * 0.9};
});
const NET_LABELS = ['Clouds', 'AI labs', 'Phones', 'Carmakers', 'Banks', 'Factories'];
const BARS = [{label: 'Y1', value: 12}, {label: 'Y2', value: 18}, {label: 'Y3', value: 24}, {label: 'Y4', value: 41}, {label: 'Y5', value: 47}, {label: 'Y6', value: 55}];
const BAR_BOX = {x: 560, y: 330, w: 800, h: 460};

export const demoPresenterActions = (tl: ReturnType<typeof chartStrokes>): PresenterAction[] => [
  {kind: 'enter', from: -260, to: 540, at: 0.25, dur: 1.55},
  {kind: 'draw', timeline: tl},
  {kind: 'react', at: tl.end + 0.05, dur: 0.7},
  {kind: 'point', at: tl.end + 0.55, dur: Math.max(0.8, 5.95 - (tl.end + 0.55)), target: [CH.C[0] - 4, CH.C[1] + 6]},
  {kind: 'explain', at: tl.end + 0.6, dur: Math.max(0.7, 5.9 - (tl.end + 0.6))},
  {kind: 'exit', to: 2300, at: 6.0, dur: 1.4},
];
export const DEMO_PRESENTER = {floor: FLOOR, scale: PS, startX: -260};

export const EngineDemo: React.FC<EngineDemoProps> = ({geo}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const tl = useMemo(chartStrokes, []);
  const W = 1920, H = 1080;
  const hasGeo = !!geo && !!geo.paths && Object.keys(geo.paths).length > 0;

  // ----- scene envelopes
  const s1 = 1 - E.inOut(win(t, 6.0, 0.7));
  const boardOp = 1 - E.inOut(win(t, 5.95, 0.6));
  const chartOp = 1 - E.inOut(win(t, 6.2, 0.6));
  const flowOp = E.out(win(t, 6.7, 0.3)) * (1 - E.inOut(win(t, 11.85, 0.3)));   // cards dissolve; their dots fly on
  const mapOp = hasGeo ? E.out(win(t, 11.9, 0.8)) * (1 - E.inOut(win(t, 17.95, 0.45))) : 0;
  const chipOp = E.out(win(t, 18.05, 0.3)) * (1 - E.inOut(win(t, 24.1, 0.5)));

  // ----- scene 2 -> 3 hand-off: stages fly to their cities (positions on the map camera at the landing time)
  const land = 12.75;
  const cityOf: Record<string, Vec> = {design: LL.santaClara, fab: LL.hsinchu, pack: LL.hsinchu, dc: LL.hsinchu};
  const flying = t > 11.85 && t < 13.0 ? STAGES.map((s) => {
    const u = E.inOutQuint(win(t, 11.9 + (s.id === 'dc' ? 0.1 : 0), 0.85));
    const to = mapPointAt(CAMS, land, cityOf[s.id] as any, W, H);
    const c: Vec = [(s.x + to[0]) / 2, Math.min(s.y, to[1]) - 160];
    return {id: s.id, p: quadPt([s.x, s.y], c, to, u), u, color: (P as any)[s.color || 'gold'] || P.gold};
  }) : [];

  // ----- scene 1 -> 2 hand-off: chart points grow into stage cards
  const morph12 = t > 6.05 && t < 7.3 ? STAGES.map((s, i) => {
    const u = E.inOutQuint(win(t, 6.1 + i * 0.05, 0.75));
    const from = STAGE_FROM[s.id];
    const c: Vec = [(from[0] + s.x) / 2, Math.min(from[1], s.y) - 120];
    return {p: quadPt(from, c, [s.x, s.y], u), r: lerp(15, 60, u), op: 1 - E.in(win(t, (s.appear || 7) - 0.05, 0.3)), color: (P as any)[s.color || 'gold']};
  }) : [];

  // ----- scene 4 -> 5: network
  const netU = (i: number) => E.outBack(win(t, NET[i].at, 0.6));
  const netOut = E.inOut(win(t, 25.35, 0.7));
  const taiwanScreen = hasGeo ? mapPointAt(CAMS, 17.9, LL.hsinchu as any, W, H) : [960, 540] as Vec;

  return (
    <AbsoluteFill style={{background: P.bg}}>
      {/* SCENE 3 map (HTML layer so it can tilt in 3D) */}
      {hasGeo && mapOp > 0 && (
        <AnimatedWorldMap t={t} geo={geo} cameras={CAMS} opacity={mapOp}
          tilt={[[12.9, 0], [14.4, 18], [16.4, 14], [17.25, 0]]}
          highlights={[{iso: 'USA', color: 'blue', at: 12.75}, {iso: 'TWN', color: 'gold', at: 12.85, dur: 0.5},
            ...EU.map((iso, i) => ({iso, color: 'teal', at: 15.0 + i * 0.04, strength: 0.8}))]}
          hubs={[
            {id: 'sc', at: LL.santaClara as any, label: 'California', sub: 'chip design', color: 'blue', time: land, anchor: 'end'},
            {id: 'tw', at: LL.hsinchu as any, label: 'Taiwan', sub: 'fabrication + packaging', color: 'gold', time: land + 0.05},
            {id: 'eu', at: LL.frankfurt as any, label: 'Europe', sub: 'data centers', color: 'teal', time: 15.6},
            {id: 'us', at: LL.ashburn as any, label: 'US East', sub: 'data centers', color: 'blue', time: 15.75},
          ]}
          routes={[
            {from: LL.santaClara as any, to: LL.hsinchu as any, at: 13.0, dur: 1.2, color: 'blue', tokenShape: 'packet', tokens: 4, label: 'DESIGNS', lift: 0.22},
            {from: LL.hsinchu as any, to: LL.frankfurt as any, at: 15.55, dur: 1.1, color: 'gold', tokenShape: 'chip', tokens: 3, label: 'CHIPS', lift: 0.25},
            {from: LL.hsinchu as any, to: LL.ashburn as any, at: 15.8, dur: 1.1, color: 'gold', tokenShape: 'chip', tokens: 3, lift: 0.22},
          ]}
          caption="Real locations (Natural Earth, public domain) · routes are schematic" />
      )}

      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        {/* ================= SCENE 1: studio, board, presenter draws a chart */}
        {s1 > 0 && <g opacity={s1}>
          <Studio t={t} floorY={FLOOR} opacity={E.out(win(t, 0, 0.5))} />
          <DigitalBoard t={t} at={0.45} x={700} y={150} w={1120} h={640} opacity={boardOp} />
          <text x={760} y={215} fill={P.muted} fontFamily={FONT.body} fontWeight={700} fontSize={22} letterSpacing={3}
            opacity={E.out(win(t, 1.1, 0.4)) * boardOp}>REVENUE · ILLUSTRATIVE</text>
        </g>}
        <DrawOnCanvas t={t} timeline={tl} opacity={chartOp} />
        {t < 7.6 && <g opacity={1 - E.in(win(t, 6.9, 0.6))}>
          <AnimatedPresenter t={t} floor={FLOOR} scale={PS} startX={-260}
            actions={demoPresenterActions(tl)}
            talk={[[tl.end + 0.4, tl.end + 1.5]]} />
        </g>}

        {/* ================= SCENE 2: the points become a supply chain */}
        {morph12.map((m, i) => <g key={'m' + i} opacity={m.op}>
          <circle cx={m.p[0]} cy={m.p[1]} r={m.r} fill={m.color} opacity={0.25} />
          <circle cx={m.p[0]} cy={m.p[1]} r={m.r * 0.4} fill={m.color} />
        </g>)}
        {flowOp > 0 && <g>
          <text x={120} y={170} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={48} opacity={flowOp}>From design to data center</text>
          <text x={122} y={212} fill={P.muted} fontFamily={FONT.body} fontSize={24} opacity={flowOp}>each stage transforms the product before passing it on</text>
          <EconomicFlow t={t} opacity={flowOp} stages={STAGES} cardW={310} cardH={250}
            links={[{from: 'design', to: 'fab', appear: 7.1}, {from: 'fab', to: 'pack', appear: 7.2}, {from: 'pack', to: 'dc', appear: 7.3}]}
            items={{starts: [7.35, 8.55], route: ['design', 'fab', 'pack', 'dc'], travel: 0.6, process: 0.55}}
            inputs={[{stage: 'pack', at: 9.4, from: [1180, 300], shape: 'box', label: 'memory'}]}
            money={[{from: 'dc', to: 'design', starts: [11.0, 11.25, 11.5], travel: 0.95, label: 'PAYMENTS', lift: 0.16}]}
 />
        </g>}
        {flying.map((f) => <g key={'f' + f.id} opacity={E.out(win(t, 11.85, 0.15)) * (1 - win(t, 12.75, 0.2))}>
          <circle cx={f.p[0]} cy={f.p[1]} r={lerp(40, 11, f.u)} fill={f.color} opacity={0.35} />
          <circle cx={f.p[0]} cy={f.p[1]} r={9} fill={f.color} />
        </g>)}

        {/* ================= SCENE 3 -> 4 dive */}
        <Burst t={t} at={17.95} cx={taiwanScreen[0]} cy={taiwanScreen[1]} n={34} dist={520} />

        {/* ================= SCENE 4: exploded chip */}
        {chipOp > 0 && <g>
          <text x={120} y={170} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={48}
            opacity={chipOp * E.out(win(t, 18.6, 0.5))}>Inside a chip</text>
          <text x={122} y={212} fill={P.muted} fontFamily={FONT.body} fontSize={24} opacity={chipOp * E.out(win(t, 18.7, 0.5))}>conceptual layers · schematic, not to scale</text>
          <ExplodedDiagram t={t} layers={LAYERS} cx={lerp(960, 760, E.inOut(win(t, 19.0, 1.0)) * (1 - E.inOut(win(t, 22.4, 1.0))))} cy={610} opacity={chipOp}
            scale={[[18.0, 0.25], [18.8, 1.25], [21.6, 1.45], [23.4, 1.3], [24.4, 0.3]]}
            yaw={[[18.0, 10], [21.0, 48], [24.0, 75]]}
            explodeAt={19.0} labelsAt={19.9} assembleAt={22.2} explodeGap={62} />
        </g>}

        {/* ================= SCENE 5: network -> chart -> title */}
        {t > 23.9 && t < 26.4 && <g opacity={1 - netOut}>
          {NET.map((n, i) => {
            const u = netU(i);
            if (u <= 0) return null;
            const p = lerpV([960, 560], n.p, clamp(u));
            const j = (i + 5) % NET.length, q = NET[j].p;
            const pk = ((t * 0.7 + i * 0.13) % 1);
            return <g key={i}>
              <line x1={960} y1={560} x2={p[0]} y2={p[1]} stroke={P.gold} strokeOpacity={0.35} strokeWidth={2} />
              {u >= 1 && <line x1={p[0]} y1={p[1]} x2={lerp(p[0], q[0], E.inOut(win(t, n.at + 0.6, 0.5)))} y2={lerp(p[1], q[1], E.inOut(win(t, n.at + 0.6, 0.5)))} stroke={P.blue} strokeOpacity={0.35} strokeWidth={2} />}
              {u >= 1 && <circle cx={lerp(960, p[0], pk)} cy={lerp(560, p[1], pk)} r={4} fill={P.gold} />}
              <circle cx={p[0]} cy={p[1]} r={12 * clamp(u)} fill={i % 3 ? P.blue : P.teal} stroke={P.bg} strokeWidth={3} />
              {i % 3 === 0 && <text x={p[0]} y={p[1] - 22} textAnchor="middle" fill={P.ink} fontFamily={FONT.body} fontWeight={700} fontSize={22} opacity={clamp(u)}>{NET_LABELS[(i / 3) % NET_LABELS.length]}</text>}
            </g>;
          })}
          <circle cx={960} cy={560} r={36 + 4 * Math.sin(t * 6)} fill={P.gold} opacity={0.9} />
        </g>}
        {/* network nodes fall into place as the bases of the bars */}
        {t > 25.3 && t < 26.6 && BARS.map((b, i) => {
          const gap = BAR_BOX.w / BARS.length;
          const to: Vec = [BAR_BOX.x + i * gap + gap / 2, BAR_BOX.y + BAR_BOX.h];
          const from = NET[(i * 3 + 1) % NET.length].p;
          const u = E.inOutQuint(win(t, 25.35 + i * 0.06, 0.7));
          const p = quadPt(from, [(from[0] + to[0]) / 2, Math.min(from[1], to[1]) - 120], to, u);
          return <circle key={'nb' + i} cx={p[0]} cy={p[1]} r={12} fill={P.blue} opacity={1 - win(t, 26.2, 0.3)} />;
        })}
        {t > 25.6 && t < 28.3 && (
          <BarChart t={t} data={BARS} box={BAR_BOX} start={26.0} stagger={0.12} grow={0.6} title="Revenue by year" note="Illustrative data"
            valuePrefix="$" valueSuffix="bn" highlight="growth" highlightAt={27.0}
            opacity={E.out(win(t, 25.7, 0.3)) * (1 - E.inOut(win(t, 27.75, 0.45)))} />
        )}
        {t > 27.6 && t < 28.6 && BARS.map((b, i) => {
          const gap = BAR_BOX.w / BARS.length, x = BAR_BOX.x + i * gap + gap / 2;
          const u = E.inOut(win(t, 27.7 + i * 0.03, 0.6));
          return <line key={'st' + i} x1={lerp(x, 960, u)} y1={lerp(BAR_BOX.y + BAR_BOX.h - 200, 520, u)} x2={lerp(x, 960, Math.max(0, u - 0.2))}
            y2={lerp(BAR_BOX.y + BAR_BOX.h, 540, Math.max(0, u - 0.2))} stroke={P.gold} strokeWidth={6} strokeLinecap="round" opacity={1 - win(t, 28.2, 0.3)} />;
        })}
        {t > 27.9 && <g opacity={1 - E.in(win(t, 29.55, 0.45))}>
          <circle cx={960} cy={500} r={lerp(0, 700, E.out(win(t, 28.0, 1.2)))} fill="none" stroke={P.gold} strokeOpacity={0.25 * (1 - win(t, 28.0, 1.4))} strokeWidth={3} />
          <TitleReveal t={t} at={28.05} title="THE HIDDEN ECONOMICS" tagline="The Stories Behind Money, Power and the World." cx={960} cy={520} />
        </g>}
        <LightSweep t={t} at={28.75} dur={0.9} />
        <Iris t={t} at={0.0} dur={0.6} cx={W / 2} cy={H / 2} mode="open" />
        {/* final transition: gold line collapses the frame to black */}
        {t > 29.3 && <rect width={W} height={H} fill="#000" opacity={E.inOut(win(t, 29.55, 0.45))} />}
        {t > 29.25 && <rect x={0} y={540 - 2} width={W * (1 - E.inOut(win(t, 29.3, 0.6)))} height={4} fill={P.gold}
          transform={`translate(${W * E.inOut(win(t, 29.3, 0.6)) / 2} 0)`} opacity={life(t, 29.25, 30, 0.1, 0.25)} />}
      </svg>
    </AbsoluteFill>
  );
};
