import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {AnimatedPresenter} from '../AnimatedPresenter/AnimatedPresenter';
import {BarChart, Donut, LineChart} from '../AnimatedCharts/AnimatedCharts';
import {AnimatedWorldMap} from '../AnimatedWorldMap/AnimatedWorldMap';
import {DrawOnCanvas, buildDrawTimeline, shapes} from '../DrawOnCanvas/DrawOnCanvas';
import {EconomicFlow} from '../EconomicFlow/EconomicFlow';
import {ExplodedDiagram} from '../ExplodedDiagram/ExplodedDiagram';
import {ENGINE_PALETTE as P, FONT} from '../motion';
import {DigitalBoard, Studio} from '../transitions';
import type {WorldGeo} from '../types';

/** One standalone preview per component (all 1920x1080, 30 fps). Values shown are illustrative and labelled. */
const useT = () => { const f = useCurrentFrame(); const {fps} = useVideoConfig(); return f / fps; };
const Label: React.FC<{title: string; sub: string}> = ({title, sub}) => (
  <g><text x={80} y={110} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={44}>{title}</text>
    <text x={82} y={150} fill={P.muted} fontFamily={FONT.body} fontSize={24}>{sub}</text></g>
);

export const PresenterPreview: React.FC = () => {
  const t = useT();
  const tl = useMemo(() => buildDrawTimeline([
    {d: shapes.rect(900, 330, 260, 130), speed: 1300, color: 'blue', width: 5, label: {text: 'SUPPLIER', x: 1030, y: 408, size: 30, color: 'ink', anchor: 'middle'}},
    {d: shapes.arrow([1170, 395], [1390, 395], 0), speed: 900, color: 'gold', width: 5},
    {d: shapes.rect(1400, 330, 260, 130), speed: 1300, color: 'teal', width: 5, label: {text: 'CUSTOMER', x: 1530, y: 408, size: 30, color: 'ink', anchor: 'middle'}},
  ], {start: 2.1}), []);
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Studio t={t} floorY={960} />
        <DigitalBoard t={t} at={0.3} x={760} y={240} w={1060} h={560} />
        <Label title="AnimatedPresenter" sub="enter · walk · draw · write · point · explain · react · exit (articulated IK rig)" />
        <DrawOnCanvas t={t} timeline={tl} />
        <text x={900} y={640} fill={P.gold} fontFamily={FONT.display} fontWeight={800} fontSize={40}>
          {'PAYS FOR THE PRODUCT'.slice(0, Math.max(0, Math.ceil(20 * Math.min(1, (t - 5.3) / 1.0))))}</text>
        <AnimatedPresenter t={t} floor={960} scale={0.9} startX={-250} talk={[[6.6, 8.2]]}
          actions={[
            {kind: 'enter', from: -250, to: 620, at: 0.2, dur: 1.5},
            {kind: 'draw', timeline: tl},
            {kind: 'write', at: 5.3, dur: 1.0, x: 900, y: 640, width: 520},
            {kind: 'point', at: 6.5, dur: 1.2, target: [1530, 470]},
            {kind: 'explain', at: 6.6, dur: 1.6},
            {kind: 'react', at: 8.1, dur: 0.8},
            {kind: 'exit', to: 2300, at: 9.0, dur: 1.4},
          ]} />
      </svg>
    </AbsoluteFill>
  );
};

export const DrawPreview: React.FC = () => {
  const t = useT();
  const tl = useMemo(() => buildDrawTimeline([
    {d: shapes.timeline(160, 860, 1600, 6), speed: 1800, color: 'muted', width: 4},
    {d: shapes.rect(160, 300, 300, 150), color: 'blue', label: {text: 'INPUTS', x: 310, y: 385, size: 30, color: 'ink', anchor: 'middle'}},
    {d: shapes.arrow([470, 375], [640, 375], 0.12), color: 'gold'},
    {d: shapes.circle([780, 375], 110), color: 'gold', label: {text: 'MARGIN', x: 780, y: 385, size: 30, color: 'ink', anchor: 'middle'}},
    {d: shapes.arrow([900, 375], [1080, 375], -0.12), color: 'gold'},
    {d: shapes.rect(1090, 300, 300, 150), color: 'teal', label: {text: 'OUTPUTS', x: 1240, y: 385, size: 30, color: 'ink', anchor: 'middle'}},
    {d: shapes.curve([[1460, 720], [1560, 620], [1660, 650], [1760, 480]]), color: 'gold', width: 7, pauseAfter: 0.3},
  ], {start: 0.6, speed: 1100}), []);
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Label title="DrawOnCanvas" sub="path-length reveal · pen follows the active stroke · lifts between strokes · labels write on" />
        <DrawOnCanvas t={t} timeline={tl} showPen />
      </svg>
    </AbsoluteFill>
  );
};

export const MapPreview: React.FC<{geo: WorldGeo}> = ({geo}) => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: P.bg}}>
      {geo?.paths && Object.keys(geo.paths).length > 0 && <AnimatedWorldMap t={t} geo={geo}
        cameras={[{at: 0, lon: 60, lat: 30, span: 320}, {at: 1.5, lon: 115, lat: 30, span: 80, dur: 1.8}, {at: 5.0, lon: 40, lat: 35, span: 300, dur: 1.8}]}
        tilt={[[0, 18], [8, 6]]}
        highlights={[{iso: 'TWN', color: 'gold', at: 2.6}, {iso: 'KOR', color: 'teal', at: 2.9}, {iso: 'JPN', color: 'teal', at: 3.1}, {iso: 'NLD', color: 'blue', at: 5.6}, {iso: 'USA', color: 'blue', at: 5.9}]}
        hubs={[{id: 'tw', at: [120.99, 24.78], label: 'Hsinchu', sub: 'foundries', color: 'gold', time: 2.7},
          {id: 'kr', at: [127.1, 37.3], label: 'Korea', sub: 'memory', color: 'teal', time: 3.0, anchor: 'end'},
          {id: 'nl', at: [5.47, 51.44], label: 'Netherlands', sub: 'lithography machines', color: 'blue', time: 5.7, anchor: 'end'}]}
        routes={[{from: [127.1, 37.3], to: [120.99, 24.78], at: 3.3, dur: 0.8, color: 'teal', tokenShape: 'box', lift: 0.3},
          {from: [5.47, 51.44], to: [120.99, 24.78], at: 6.0, dur: 1.2, color: 'blue', tokenShape: 'box', label: 'MACHINES'}]}
        caption="Real locations (Natural Earth) · schematic routes" />}
      <svg width={1920} height={1080} style={{position: 'absolute'}}><Label title="AnimatedWorldMap" sub="camera moves · highlights · hubs · drawn routes with moving tokens · tilt + parallax" /></svg>
    </AbsoluteFill>
  );
};

export const FlowPreview: React.FC = () => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Label title="EconomicFlow" sub="products move and transform · inventory · customer payments flow back" />
        <EconomicFlow t={t}
          stages={[
            {id: 'f', label: 'Factory', sub: 'makes devices', x: 330, y: 520, kind: 'fab', color: 'gold', appear: 0.3, output: 'box'},
            {id: 'w', label: 'Warehouse', sub: 'inventory', x: 800, y: 520, kind: 'warehouse', color: 'teal', appear: 0.5, output: 'box'},
            {id: 'c', label: 'Customer', sub: 'buys the product', x: 1270, y: 520, kind: 'customer', color: 'blue', appear: 0.7, output: 'coin'},
            {id: 'b', label: 'Bank', sub: 'settles payment', x: 1660, y: 820, kind: 'bank', color: 'gold', appear: 0.9, output: 'coin'},
          ]}
          links={[{from: 'f', to: 'w', appear: 1.0}, {from: 'w', to: 'c', appear: 1.1}]}
          items={{starts: [1.4, 2.6, 3.8], route: ['f', 'w', 'c'], travel: 0.7, process: 0.5}}
          money={[{from: 'c', to: 'b', starts: [3.6, 4.8, 6.0], travel: 0.8, lift: -0.2},
            {from: 'b', to: 'f', starts: [4.6, 5.8, 7.0], travel: 1.3, label: 'PAYMENT TO THE MAKER', lift: 0.14}]} />
      </svg>
    </AbsoluteFill>
  );
};

export const ChartsPreview: React.FC = () => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Label title="AnimatedCharts" sub="build · compare periods · highlight fastest growth · morph into a business diagram" />
        <BarChart t={t} box={{x: 260, y: 320, w: 1400, h: 520}} start={0.6} title="Revenue by segment" note="Illustrative data"
          data={[{label: 'Hardware', value: 30}, {label: 'Software', value: 12}, {label: 'Services', value: 20}, {label: 'Licensing', value: 8}]}
          dataB={[{label: 'Hardware', value: 34}, {label: 'Software', value: 40}, {label: 'Services', value: 24}, {label: 'Licensing', value: 15}]}
          changeAt={2.8} periodLabels={['YEAR 1', 'YEAR 2']} highlight="growth" highlightAt={4.0} valuePrefix="$" valueSuffix="bn"
          morph={{at: 6.0, dur: 1.2, boxes: [
            {x: 260, y: 470, w: 280, h: 150, label: 'Hardware', sub: 'sold once'},
            {x: 640, y: 470, w: 280, h: 150, label: 'Software', sub: 'recurring'},
            {x: 1020, y: 470, w: 280, h: 150, label: 'Services', sub: 'keeps clients'},
            {x: 1400, y: 470, w: 280, h: 150, label: 'Licensing', sub: 'royalties'}], arrows: [[0, 1], [1, 2], [2, 3]]}} />
      </svg>
    </AbsoluteFill>
  );
};

export const ChartsLinePreview: React.FC = () => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Label title="AnimatedCharts: line + donut" sub="progressive line with area fill · donut sweeps then re-balances" />
        <LineChart t={t} box={{x: 160, y: 330, w: 900, h: 480}} start={0.6} draw={2.4} area title="Gross margin" note="Illustrative data" valueSuffix="%"
          data={[{label: 'Y1', value: 52}, {label: 'Y2', value: 58}, {label: 'Y3', value: 55}, {label: 'Y4', value: 66}, {label: 'Y5', value: 72}]} yMax={80} />
        <Donut t={t} cx={1480} cy={580} r={200} start={1.2} data={[{label: 'A', value: 50}, {label: 'B', value: 30}, {label: 'C', value: 20}]}
          dataB={[{label: 'A', value: 35}, {label: 'B', value: 45}, {label: 'C', value: 20}]} changeAt={4.5} center="Share" centerSub="illustrative" />
      </svg>
    </AbsoluteFill>
  );
};

export const ExplodedPreview: React.FC = () => {
  const t = useT();
  return (
    <AbsoluteFill style={{background: P.bg}}>
      <svg width={1920} height={1080}>
        <Label title="ExplodedDiagram" sub="layers separate with staggered springs · turn · labels · reassemble" />
        <ExplodedDiagram t={t} cx={760} cy={600} explodeAt={1.0} labelsAt={1.9} assembleAt={5.6} explodeGap={82}
          scale={[[0, 0.9], [3, 1.2], [7, 1.0]]} yaw={[[0, 20], [7, 80]]} note="Conceptual layers · schematic, not a to-scale cross-section"
          layers={[
            {label: 'Package substrate', sub: 'routes signals', kind: 'substrate', color: 'teal', thickness: 18, size: 250},
            {label: 'Micro-bumps', sub: 'contacts', kind: 'bumps', color: 'muted', thickness: 7},
            {label: 'Silicon die', sub: 'transistors', kind: 'die', color: 'blue', thickness: 14},
            {label: 'Wiring layers', sub: 'interconnect', kind: 'interconnect', color: 'gold', thickness: 9},
            {label: 'Heat spreader', sub: 'cooling', kind: 'lid', color: 'muted', thickness: 15, size: 230},
          ]} />
      </svg>
    </AbsoluteFill>
  );
};
