import React from 'react';
import {AbsoluteFill} from 'remotion';
import {SUBJECTS} from './CinematicThumb';

/**
 * PosterThumb: the `poster` thumbnail archetype (owner model of 2026-11-19, docs/thumbnails/OWNER_STYLE.md).
 *
 * - A cinematic, saturated, painted BACKDROP: night world map with glowing arcs and city lights | sunset coast (sea,
 *   palms, mountains) | dusk skyline | deep ocean floor (light shafts, bubbles) | factory glow | dramatic rays.
 * - ONE big HERO object on the right, breaking the frame, with a light behind it, warm-vs-cool rim light and a glow.
 *   Heroes: wafer (chip on a glowing wafer), pylon (+ lightning), arm (factory robot arm, welding sparks), ship
 *   (container ship, optional flags), cash, datacenter, house, robot, car, shovel, card, cart, bonds, barrel, arrow,
 *   flag (accurate, simple national flags, waving), coins, taxdoc, bolt; any CinematicThumb SUBJECT also works.
 * - Effects: sparks, lightning bolts, glowing flows (energy / cash along a curve), bokeh particles, global bloom and
 *   a saturation lift (filter on the scene, not on the text).
 * - Text (exact layout computed in Python, hiddeneco/youtube_thumbnail.py `layout_poster`): Inter Display Black
 *   Italic caps, white with a thick black outline and a drop shadow; the accent line sits on a rough brush-stroke
 *   banner (SVG path with ragged edges and bristle streaks), red with white text or yellow with black text, tilted.
 * Canvas 1920x1080. Illustrated, not photographic. No logos, no real people, no imitation of real photographs.
 */
export type PosterText = {text: string; x: number; y: number; size: number; width: number; color: string; anchor: 'start' | 'middle' | 'end';
  banner?: string; box?: string; outline?: string; rotate?: number};
type Obj = {kind: string; x: number; y: number; s: number; rot?: number; flip?: boolean; [k: string]: any};
export type PosterProps = {
  backdrop: {kind: 'map' | 'coast' | 'skyline' | 'ocean' | 'factory' | 'rays'; [k: string]: any};
  hero: Obj;
  support?: Obj[];             // drawn behind the hero (with their own glow)
  front?: Obj[];               // drawn in front of the hero
  light?: {x?: number; y?: number; r?: number; color?: string; rays?: boolean};
  rim?: {warm?: string; cool?: string};
  sparks?: {x: number; y: number; n?: number; len?: number; color?: string; spread?: number; angle?: number}[];
  bolts?: {x1: number; y1: number; x2: number; y2: number; color?: string; seed?: number; w?: number}[];
  flows?: {p: [number, number][]; color?: string; n?: number; kind?: 'energy' | 'cash' | 'coins'; w?: number}[];
  particles?: {n: number; color?: string; region?: [number, number, number, number]; size?: number};
  text: PosterText[];
  hideText?: boolean;
  saturate?: number;
  bloom?: number;
  scrim?: number;
};

const W = 1920, H = 1080, OL = '#05070B';
const FONT = 'Inter Display, Inter, sans-serif';
const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const lin = (id: string, stops: [number, string, number?][], x2 = 0, y2 = 1, x1 = 0, y1 = 0) =>
  <linearGradient id={id} x1={x1} y1={y1} x2={x2} y2={y2}>{stops.map(([o, c, a], k) => <stop key={k} offset={o} stopColor={c} stopOpacity={a ?? 1} />)}</linearGradient>;
const rad = (id: string, stops: [number, string, number?][], cx = 0.5, cy = 0.5, r = 0.5) =>
  <radialGradient id={id} cx={cx} cy={cy} r={r}>{stops.map(([o, c, a], k) => <stop key={k} offset={o} stopColor={c} stopOpacity={a ?? 1} />)}</radialGradient>;
const star = (cx: number, cy: number, r: number, rot = 0, inner = 0.382) => {
  const pts: string[] = [];
  for (let k = 0; k < 10; k++) { const a = -Math.PI / 2 + (k * Math.PI) / 5 + (rot * Math.PI) / 180, rr = k % 2 ? r * inner : r; pts.push(`${cx + Math.cos(a) * rr},${cy + Math.sin(a) * rr}`); }
  return pts.join(' ');
};

/* ------------------------------------------------------------------------------------------------ world map */
const LAND: [number, number][][] = [
  // North America, Greenland, South America
  [[-168, 65], [-162, 70], [-140, 70], [-125, 72], [-95, 72], [-80, 73], [-65, 62], [-60, 55], [-55, 50], [-66, 45], [-70, 42], [-76, 38], [-76, 35], [-81, 31], [-80, 26], [-82, 25], [-84, 30], [-90, 29], [-97, 27], [-97, 22], [-92, 18], [-87, 21], [-88, 16], [-83, 10], [-78, 8], [-80, 9], [-85, 12], [-92, 15], [-105, 20], [-110, 24], [-115, 30], [-118, 34], [-124, 40], [-124, 48], [-130, 55], [-140, 60], [-152, 59], [-165, 55], [-160, 60]],
  [[-73, 78], [-60, 82], [-30, 83], [-20, 75], [-22, 70], [-40, 62], [-50, 64], [-55, 70]],
  [[-80, 9], [-75, 11], [-62, 11], [-52, 5], [-50, 0], [-35, -5], [-35, -10], [-39, -15], [-41, -22], [-48, -26], [-53, -34], [-58, -38], [-65, -42], [-68, -50], [-70, -55], [-74, -50], [-74, -40], [-71, -30], [-70, -18], [-76, -14], [-81, -5], [-80, 0], [-78, 3]],
  // Europe, Britain, Africa, Madagascar
  [[-10, 36], [-9, 43], [-2, 44], [-4, 48], [-1, 49], [2, 51], [5, 53], [8, 54], [8, 57], [10, 55], [12, 54], [15, 55], [10, 59], [5, 59], [5, 62], [12, 66], [16, 69], [25, 71], [30, 70], [40, 68], [45, 68], [60, 68], [60, 55], [50, 47], [40, 47], [35, 45], [30, 41], [26, 40], [23, 36], [20, 40], [16, 38], [18, 40], [12, 44], [13, 45], [8, 44], [3, 43], [0, 39], [-5, 36]],
  [[-5, 50], [1, 51], [2, 53], [-2, 56], [-3, 58], [-6, 58], [-5, 55], [-3, 54], [-5, 52]],
  [[-17, 15], [-17, 21], [-13, 27], [-10, 30], [-6, 35], [10, 37], [11, 33], [20, 31], [25, 32], [32, 31], [34, 28], [43, 12], [51, 12], [50, 8], [40, -3], [40, -15], [35, -24], [32, -29], [27, -34], [20, -35], [17, -29], [12, -18], [13, -10], [9, -1], [9, 4], [4, 6], [-4, 5], [-8, 4], [-13, 8]],
  [[44, -25], [47, -25], [50, -15], [49, -12], [44, -17]],
  // Asia, Japan, Taiwan, Indonesia, Australia
  [[60, 68], [70, 73], [80, 73], [90, 76], [105, 77], [115, 74], [130, 72], [140, 72], [160, 70], [170, 70], [180, 69], [178, 65], [165, 62], [160, 61], [156, 58], [150, 59], [140, 58], [137, 54], [141, 53], [140, 48], [135, 44], [131, 43], [128, 40], [129, 35], [127, 35], [126, 38], [125, 40], [121, 40], [118, 38], [122, 37], [119, 35], [121, 33], [122, 30], [120, 26], [117, 23], [109, 21], [106, 20], [108, 16], [109, 12], [106, 9], [103, 10], [100, 13], [100, 8], [101, 3], [104, 1], [103, 4], [98, 8], [98, 16], [94, 17], [91, 22], [87, 22], [80, 16], [80, 13], [77, 8], [72, 21], [67, 24], [62, 25], [57, 25], [56, 26], [50, 30], [48, 30], [52, 24], [56, 22], [58, 22], [52, 16], [43, 13], [38, 22], [35, 28], [34, 31], [36, 36], [30, 37], [26, 40], [30, 41], [35, 45], [40, 47], [50, 47], [60, 55]],
  [[130, 31], [132, 34], [135, 34], [140, 35], [141, 38], [142, 41], [140, 41], [139, 38], [137, 37], [133, 35], [130, 33]],
  [[140, 42], [143, 42], [145, 44], [142, 45]],
  [[120.1, 22.5], [121.9, 25.1], [121.5, 25.3], [120.1, 23.5]],
  [[109, 1], [111, -3], [116, -4], [119, 1], [117, 7], [110, 2]], [[95, 5], [106, -6], [104, -4], [98, 2]],
  [[114, -22], [114, -34], [118, -35], [124, -33], [132, -31], [138, -35], [141, -38], [147, -39], [150, -37], [153, -31], [153, -25], [146, -19], [142, -11], [136, -12], [136, -15], [130, -12], [125, -15], [122, -18]],
];
export const CITY: Record<string, [number, number]> = {
  ny: [-74, 40.7], la: [-118, 34], sf: [-122.4, 37.8], dc: [-77, 38.9], houston: [-95, 29.8], chicago: [-87.6, 41.9], mexico: [-99, 19.4],
  toronto: [-79.4, 43.7], montreal: [-73.6, 45.5], vancouver: [-123, 49.3], calgary: [-114, 51],
  saopaulo: [-46.6, -23.5], rio: [-43.2, -22.9], manaus: [-60, -3.1], buenosaires: [-58.4, -34.6],
  london: [-0.1, 51.5], paris: [2.35, 48.85], berlin: [13.4, 52.5], frankfurt: [8.7, 50.1], madrid: [-3.7, 40.4], rome: [12.5, 41.9], stockholm: [18, 59.3], amsterdam: [4.9, 52.4],
  dubai: [55.3, 25.2], mumbai: [72.8, 19], lagos: [3.4, 6.5], joburg: [28, -26.2], cairo: [31.2, 30],
  beijing: [116.4, 39.9], shanghai: [121.5, 31.2], shenzhen: [114, 22.5], tokyo: [139.7, 35.7], osaka: [135.5, 34.7], seoul: [127, 37.5], taipei: [121.5, 25],
  singapore: [103.8, 1.3], jakarta: [106.8, -6.2], hanoi: [105.8, 21], sydney: [151.2, -33.9], delhi: [77.2, 28.6],
};
const inPoly = (x: number, y: number, poly: [number, number][]) => {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, yi] = poly[i], [xj, yj] = poly[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) inside = !inside;
  }
  return inside;
};

const MapBackdrop: React.FC<{b: any}> = ({b}) => {
  const k = b.k ?? 5.4, lon0 = b.lon ?? 10, lat0 = b.lat ?? 22;
  const pr = (lon: number, lat: number): [number, number] => [W / 2 + (lon - lon0) * k, H / 2 - (lat - lat0) * k * 1.12];
  const glow = b.glow ?? '#4AA8FF', arcC = b.arcColor ?? '#FFC24A', light = b.lights ?? '#FFD58A';
  const lights: React.ReactNode[] = [];
  let seed = 1;
  LAND.forEach((poly, pi) => {
    const xs = poly.map((p) => p[0]), ys = poly.map((p) => p[1]);
    const [a0, a1, b0, b1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
    const n = Math.min(260, Math.round((a1 - a0) * (b1 - b0) * 0.09 * (b.density ?? 1)) + 6);
    for (let i = 0; i < n; i++) {
      const lo = a0 + rnd(seed++) * (a1 - a0), la = b0 + rnd(seed++) * (b1 - b0);
      if (!inPoly(lo, la, poly) || la > 66) continue;
      const [x, y] = pr(lo, la), r = 0.8 + rnd(seed++) * 1.9 * Math.min(2, k / 5.4);
      lights.push(<circle key={pi + '-' + i} cx={x} cy={y} r={r} fill={light} opacity={0.45 + rnd(seed++) * 0.55} />);
    }
  });
  const arcs: [string | [number, number], string | [number, number]][] = b.arcs ?? [];
  const pt = (c: string | [number, number]) => pr(...(typeof c === 'string' ? CITY[c] : c));
  return <g>
    <defs>
      {rad('mapsky', [[0, b.sky0 ?? '#0E2C66'], [0.55, b.sky1 ?? '#071A40'], [1, b.sky2 ?? '#020616']], b.cx ?? 0.62, b.cy ?? 0.35, 0.9)}
      <filter id="mapglow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="6" /></filter>
    </defs>
    <rect width={W} height={H} fill="url(#mapsky)" />
    {Array.from({length: 13}, (_, i) => <path key={'g' + i} d={`M 0 ${80 * i + 20} Q ${W / 2} ${80 * i - 40} ${W} ${80 * i + 20}`} stroke="#7FB8FF" strokeOpacity={0.06} fill="none" strokeWidth={2} />)}
    {Array.from({length: 25}, (_, i) => <path key={'v' + i} d={`M ${80 * i} 0 Q ${80 * i + (80 * i - W / 2) * 0.08} ${H / 2} ${80 * i} ${H}`} stroke="#7FB8FF" strokeOpacity={0.05} fill="none" strokeWidth={2} />)}
    <g>
      {LAND.map((poly, i) => <path key={'l' + i} d={'M ' + poly.map((p) => pr(p[0], p[1]).join(' ')).join(' L ') + ' Z'} fill={glow} opacity={0.75} filter="url(#mapglow)" />)}
      {LAND.map((poly, i) => <path key={'m' + i} d={'M ' + poly.map((p) => pr(p[0], p[1]).join(' ')).join(' L ') + ' Z'} fill={b.land ?? '#285FA8'} stroke="#9AD4FF" strokeOpacity={0.8}
        strokeWidth={2} strokeLinejoin="round" />)}
    </g>
    {(b.highlight ?? []).map((h: any, i: number) => { const [x, y] = pt(h.at); return <g key={'h' + i}>
      <circle cx={x} cy={y} r={h.r ?? 120} fill={h.color ?? '#FFB238'} opacity={0.55} filter="url(#mapglow)" />
      <circle cx={x} cy={y} r={(h.r ?? 120) * 0.45} fill={h.color ?? '#FFB238'} opacity={0.5} filter="url(#mapglow)" /></g>; })}
    <g>{lights}</g>
    {arcs.map(([a, c], i) => { const [x1, y1] = pt(a), [x2, y2] = pt(c), d = Math.hypot(x2 - x1, y2 - y1);
      const path = `M ${x1} ${y1} Q ${(x1 + x2) / 2} ${(y1 + y2) / 2 - d * 0.22} ${x2} ${y2}`;
      return <g key={'a' + i}>
        <path d={path} stroke={arcC} strokeWidth={16} fill="none" opacity={0.8} filter="url(#mapglow)" />
        <path d={path} stroke="#FFF6D8" strokeWidth={4.5} fill="none" />
        {[[x1, y1], [x2, y2]].map(([x, y], j) => <g key={j}><circle cx={x} cy={y} r={18} fill={arcC} opacity={0.7} filter="url(#mapglow)" /><circle cx={x} cy={y} r={6} fill="#FFFFFF" /></g>)}
      </g>; })}
    {b.limb !== false && <path d={`M -200 ${b.limbY ?? 140} Q ${W / 2} ${(b.limbY ?? 140) - 260} ${W + 200} ${b.limbY ?? 140}`} stroke="#7FD3FF" strokeWidth={26} fill="none" opacity={0.0} />}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ scenery helpers */
const Palm: React.FC<{x: number; y: number; s: number; lean?: number; c?: string}> = ({x, y, s, lean = 1, c = '#07121A'}) =>
  <g transform={`translate(${x} ${y}) scale(${s * lean} ${s})`}>
    <path d="M -14 0 Q 10 -200 60 -420 L 76 -416 Q 32 -200 14 0 Z" fill={c} />
    {[[-170, -330, -30], [-140, -460, -60], [40, -520, -95], [190, -470, -130], [230, -360, -160], [-60, -520, -80], [120, -330, -150]].map(([tx, ty], k) =>
      <path key={k} d={`M 66 -420 Q ${(66 + tx) / 2} ${ty - 70} ${tx} ${ty} Q ${(66 + tx) / 2 + 10} ${ty - 20} 66 -410 Z`} fill={c} />)}
  </g>;
const Mountains: React.FC<{y: number; seed: number; amp: number; fill: string; rim?: string; peaks?: number}> = ({y, seed, amp, fill, rim, peaks = 9}) => {
  const pts: string[] = [];
  for (let i = 0; i <= peaks * 2; i++) { const x = (i / (peaks * 2)) * (W + 200) - 100; const h = i % 2 ? amp * (0.55 + rnd(seed + i) * 0.45) : amp * rnd(seed + i * 3) * 0.35; pts.push(`${x} ${y - h}`); }
  const d = `M -100 ${y} L ${pts.join(' L ')} L ${W + 100} ${H} L -100 ${H} Z`;
  return <g><path d={d} fill={fill} />{rim && <path d={`M ${pts.join(' L ')}`} fill="none" stroke={rim} strokeWidth={4} opacity={0.55} />}</g>;
};
const Cloud: React.FC<{x: number; y: number; s: number; top: string; bot: string; id: string}> = ({x, y, s, top, bot, id}) =>
  <g transform={`translate(${x} ${y}) scale(${s})`} filter="url(#psoft)">
    <defs>{lin(id, [[0, top], [1, bot]])}</defs>
    {[[-160, 10, 150, 70], [-40, -30, 170, 95], [100, 0, 160, 75], [220, 20, 120, 50], [-260, 30, 110, 45]].map(([cx, cy, rx, ry], k) =>
      <ellipse key={k} cx={cx} cy={cy} rx={rx} ry={ry} fill={`url(#${id})`} />)}
  </g>;

const Skyline: React.FC<{base: number; seed: number; fill: string; win?: string; maxH: number; spires?: boolean; n?: number}> = ({base, seed, fill, win, maxH, spires, n = 34}) => {
  const out: React.ReactNode[] = [];
  let x = -40;
  for (let i = 0; x < W + 40; i++) {
    const w = 50 + rnd(seed + i) * 90, h = maxH * (0.25 + rnd(seed + i * 7) * 0.75) * (rnd(seed + i * 13) > 0.86 ? 1.35 : 1);
    out.push(<rect key={'b' + i} x={x} y={base - h} width={w} height={h + 400} fill={fill} />);
    if (spires && rnd(seed + i * 5) > 0.75) out.push(<path key={'s' + i} d={`M ${x + w / 2 - 14} ${base - h} L ${x + w / 2} ${base - h - 120} L ${x + w / 2 + 14} ${base - h} Z`} fill={fill} />);
    if (spires && rnd(seed + i * 11) > 0.82) out.push(<ellipse key={'d' + i} cx={x + w / 2} cy={base - h} rx={w * 0.45} ry={w * 0.4} fill={fill} />);
    if (!spires && rnd(seed + i * 17) > 0.8) out.push(<rect key={'t' + i} x={x + w / 2 - 3} y={base - h - 90} width={6} height={90} fill={fill} />);
    if (win) for (let r = 0; r < h / 26 - 1; r++) for (let c = 0; c < w / 20 - 1; c++)
      if (rnd(seed * 31 + i * 101 + r * 7 + c) > 0.62) out.push(<rect key={`w${i}-${r}-${c}`} x={x + 8 + c * 20} y={base - h + 14 + r * 26} width={9} height={12} fill={win} opacity={0.5 + 0.5 * rnd(i + r + c)} />);
    x += w + 4 + rnd(seed + i * 3) * 10;
  }
  return <g>{out}</g>;
};

/* ------------------------------------------------------------------------------------------------ backdrops */
const Backdrop: React.FC<{p: PosterProps}> = ({p}) => {
  const b = p.backdrop, kind = b.kind;
  if (kind === 'map') return <MapBackdrop b={b} />;
  if (kind === 'coast') {
    const hz = b.horizon ?? 640, sx = b.sunX ?? 330;
    return <g>
      <defs>
        {lin('csky', [[0, '#0B1A4A'], [0.3, '#3B2F86'], [0.55, '#C2457A'], [0.75, '#FF8A3D'], [0.9, '#FFD27A']])}
        {lin('csea', [[0, '#FFB46A', 0.9], [0.06, '#2E7FA8'], [0.4, '#0B4E73'], [1, '#03182A']])}
        {rad('csun', [[0, '#FFFFFF'], [0.12, '#FFF2B0'], [0.35, '#FFB347', 0.6], [1, '#FF7A2F', 0]])}
      </defs>
      <rect width={W} height={hz + 4} fill="url(#csky)" />
      <circle cx={sx} cy={hz - 70} r={520} fill="url(#csun)" />
      <Cloud x={260} y={260} s={1.1} top="#FF9DB0" bot="#FF7A3D" id="cl1" />
      <Cloud x={900} y={150} s={1.3} top="#7E5BC2" bot="#FF8F6A" id="cl2" />
      <Cloud x={1600} y={260} s={1.0} top="#6A4FB0" bot="#F2786A" id="cl3" />
      <Mountains y={hz} seed={7} amp={150} fill="#4A3470" peaks={7} />
      {b.mount !== false && <path d={`M ${b.mountX ?? 620} ${hz} Q ${(b.mountX ?? 620) + 160} ${hz - 340} ${(b.mountX ?? 620) + 300} ${hz - 370} Q ${(b.mountX ?? 620) + 420} ${hz - 330} ${(b.mountX ?? 620) + 640} ${hz} Z`} fill="#2A2350" />}
      {b.sugarloaf && <path d={`M ${b.sugarloaf} ${hz} Q ${b.sugarloaf + 30} ${hz - 300} ${b.sugarloaf + 110} ${hz - 310} Q ${b.sugarloaf + 190} ${hz - 290} ${b.sugarloaf + 230} ${hz} Z`} fill="#231C45" />}
      <rect y={hz} width={W} height={H - hz} fill="url(#csea)" />
      {Array.from({length: 60}, (_, k) => <rect key={k} x={sx - 40 - rnd(k) * 120 + rnd(k + 2) * 200} y={hz + 6 + k * 7 + rnd(k) * 6} width={30 + rnd(k + 5) * 160} height={3 + k * 0.08} rx={2}
        fill="#FFE6A8" opacity={0.75 - k * 0.011} />)}
      {Array.from({length: 30}, (_, k) => <path key={'w' + k} d={`M ${rnd(k + 40) * W} ${hz + 40 + k * 14} q 70 -8 140 0`} stroke="#9FE3FF" strokeOpacity={0.35} strokeWidth={2 + k * 0.1} fill="none" />)}
      {b.shore !== false && <path d={`M ${W * 0.45} ${H} Q ${W * 0.7} ${hz + 210} ${W + 40} ${hz + 120} L ${W + 40} ${H} Z`} fill="#14261E" />}
      {b.shore !== false && <path d={`M ${W * 0.45} ${H} Q ${W * 0.7} ${hz + 210} ${W + 40} ${hz + 120}`} stroke="#E8FBFF" strokeWidth={10} fill="none" opacity={0.6} filter="url(#psoft)" />}
      {(b.palms ?? [[1480, hz + 200, 0.9, 1], [1760, hz + 160, 1.05, -1], [150, H + 40, 1.2, 1]]).map((q: number[], k: number) => <Palm key={k} x={q[0]} y={q[1]} s={q[2]} lean={q[3]} />)}
    </g>;
  }
  if (kind === 'skyline') {
    const base = b.base ?? 840;
    return <g>
      <defs>{lin('ssky', [[0, '#050B2C'], [0.35, '#1E1C5E'], [0.62, '#7A2E78'], [0.8, '#E2556A'], [0.92, '#FF9A4A']])}
        {lin('sgnd', [[0, '#2A1840'], [1, '#05040D']])}</defs>
      <rect width={W} height={H} fill="url(#ssky)" />
      {Array.from({length: 70}, (_, k) => <circle key={k} cx={rnd(k) * W} cy={rnd(k + 9) * 380} r={0.8 + rnd(k + 4) * 1.8} fill="#FFFFFF" opacity={0.3 + rnd(k + 2) * 0.5} />)}
      {b.sun && <circle cx={b.sun[0]} cy={b.sun[1]} r={b.sun[2] ?? 200} fill={b.sunColor ?? '#FF5A4A'} opacity={0.9} filter="url(#psoft)" />}
      {b.fuji && <g><path d={`M ${b.fuji - 560} ${base - 60} Q ${b.fuji - 200} ${base - 330} ${b.fuji - 90} ${base - 470} L ${b.fuji + 90} ${base - 470} Q ${b.fuji + 200} ${base - 330} ${b.fuji + 560} ${base - 60} Z`} fill="#3C2E6E" />
        <path d={`M ${b.fuji - 90} ${base - 470} L ${b.fuji + 90} ${base - 470} L ${b.fuji + 150} ${base - 395} L ${b.fuji + 80} ${base - 410} L ${b.fuji + 30} ${base - 380} L ${b.fuji - 30} ${base - 410} L ${b.fuji - 90} ${base - 385} L ${b.fuji - 150} ${base - 400} Z`} fill="#F2E8FF" opacity={0.9} /></g>}
      <Skyline base={base} seed={3} fill="#2C1E58" maxH={(b.maxH ?? 380) * 1.1} spires={b.spires} />
      <Skyline base={base + 40} seed={11} fill="#0E0B26" win="#FFC76A" maxH={b.maxH ?? 380} spires={b.spires} />
      <rect y={base + 40} width={W} height={H - base} fill="url(#sgnd)" />
      {Array.from({length: 40}, (_, k) => <rect key={'r' + k} x={rnd(k + 70) * W} y={base + 60 + rnd(k + 3) * 160} width={4} height={30 + rnd(k) * 60} fill="#FFC76A" opacity={0.25} />)}
    </g>;
  }
  if (kind === 'ocean') {
    return <g>
      <defs>{lin('osky', [[0, '#1C8FC8'], [0.18, '#0A5A8E'], [0.6, '#042A4C'], [1, '#010A16']])}
        {lin('oshaft', [[0, '#DFF8FF', 0.55], [1, '#DFF8FF', 0]])}</defs>
      <rect width={W} height={H} fill="url(#osky)" />
      {Array.from({length: 9}, (_, k) => { const x = 120 + k * 210 + rnd(k) * 80, w = 60 + rnd(k + 3) * 120;
        return <path key={k} d={`M ${x} -20 L ${x + w} -20 L ${x + w * 2.4 - 300} ${H} L ${x - 300 + w * 0.4} ${H} Z`} fill="url(#oshaft)" opacity={0.5} filter="url(#psoft)" />; })}
      {Array.from({length: 40}, (_, k) => <path key={'s' + k} d={`M ${rnd(k) * W} ${10 + rnd(k + 1) * 50} q 50 -10 100 0`} stroke="#E6FBFF" strokeOpacity={0.3} strokeWidth={3} fill="none" />)}
      <path d="M 0 900 Q 400 840 800 890 T 1600 870 T 2000 880 L 2000 1080 L 0 1080 Z" fill="#06223A" />
      <path d="M 0 960 Q 500 910 1000 960 T 2000 950 L 2000 1080 L 0 1080 Z" fill="#031524" />
      <path d="M 0 900 Q 400 840 800 890 T 1600 870 T 2000 880" stroke="#5FD0FF" strokeOpacity={0.3} strokeWidth={4} fill="none" />
      {Array.from({length: 14}, (_, k) => <ellipse key={'rk' + k} cx={rnd(k + 50) * W} cy={950 + rnd(k + 8) * 90} rx={30 + rnd(k) * 70} ry={18 + rnd(k + 1) * 30} fill="#020D18" />)}
      {Array.from({length: b.bubbles ?? 46}, (_, k) => { const r = 4 + rnd(k + 20) * 18;
        return <g key={'bb' + k}><circle cx={W * 0.35 + rnd(k + 30) * W * 0.65} cy={rnd(k + 31) * 900} r={r} fill="#BFF3FF" fillOpacity={0.08} stroke="#DFF9FF" strokeOpacity={0.7} strokeWidth={2} />
          <circle cx={W * 0.35 + rnd(k + 30) * W * 0.65 - r * 0.35} cy={rnd(k + 31) * 900 - r * 0.35} r={r * 0.25} fill="#FFFFFF" opacity={0.8} /></g>; })}
    </g>;
  }
  if (kind === 'factory') {
    return <g>
      <defs>{lin('fsky', [[0, '#050A20'], [0.45, '#1C1A40'], [0.75, '#8A3418'], [1, '#FF8A2A']])}</defs>
      <rect width={W} height={H} fill="url(#fsky)" />
      {Array.from({length: 7}, (_, k) => { const x = 80 + k * 280, h = 300 + rnd(k) * 260;
        return <g key={k}>
          <ellipse cx={x + 60 + 80} cy={1080 - 420 - h + 40} rx={200} ry={80} fill="#C9724A" opacity={0.28} filter="url(#psoft)" />
          <rect x={x} y={1080 - 300 - h} width={46} height={h + 300} fill="#120E22" />
          <rect x={x - 6} y={1080 - 300 - h} width={58} height={14} fill="#FF8A2A" opacity={0.7} />
        </g>; })}
      <path d="M 0 760 L 240 760 L 240 690 L 520 690 L 520 740 L 860 740 L 860 660 L 1180 660 L 1180 720 L 1500 720 L 1500 640 L 1920 640 L 1920 1080 L 0 1080 Z" fill="#0B0918" />
      {Array.from({length: 60}, (_, k) => <rect key={'fw' + k} x={20 + rnd(k) * 1880} y={680 + rnd(k + 2) * 120} width={14} height={10} fill="#FFB347" opacity={0.4 + rnd(k + 5) * 0.6} />)}
      {Array.from({length: 22}, (_, k) => <path key={'tr' + k} d={`M ${k * 90} 860 L ${k * 90 + 90} 800`} stroke="#2A2340" strokeWidth={10} />)}
      <rect y={860} width={W} height={220} fill="#07060E" />
      <ellipse cx={b.glowX ?? 1300} cy={900} rx={700} ry={90} fill="#FF7A1A" opacity={0.35} filter="url(#psoft)" />
    </g>;
  }
  // rays: dramatic gradient with light rays from the hero light
  const lx = p.light?.x ?? p.hero.x, ly = p.light?.y ?? p.hero.y;
  return <g>
    <defs><radialGradient id="rbg" cx={lx / W} cy={ly / H} r="1.0"><stop offset="0" stopColor={b.c0 ?? '#FFB238'} /><stop offset="0.35" stopColor={b.c1 ?? '#B23A1A'} /><stop offset="1" stopColor={b.c2 ?? '#120612'} /></radialGradient></defs>
    <rect width={W} height={H} fill="url(#rbg)" />
    {Array.from({length: 30}, (_, k) => { const a0 = (k / 30) * Math.PI * 2, a1 = a0 + Math.PI / 40, R = 2600;
      return <path key={k} d={`M ${lx} ${ly} L ${lx + Math.cos(a0) * R} ${ly + Math.sin(a0) * R} L ${lx + Math.cos(a1) * R} ${ly + Math.sin(a1) * R} Z`} fill={b.ray ?? '#FFE7A8'} opacity={0.1 + rnd(k) * 0.08} />; })}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ flags */
const CANADA_LEAF = 'm4890 4430-45-863a95 95 0 0 1 111-98l859 151-116-320a65 65 0 0 1 20-73l941-762-212-99a65 65 0 0 1-34-79l186-572-542 115a65 65 0 0 1-73-38l-105-247-423 454a65 65 0 0 1-111-57l204-1052-327 189a65 65 0 0 1-91-27l-332-652-332 652a65 65 0 0 1-91 27l-327-189 204 1052a65 65 0 0 1-111 57l-423-454-105 247a65 65 0 0 1-73 38l-542-115 186 572a65 65 0 0 1-34 79l-212 99 941 762a65 65 0 0 1 20 73l-116 320 859-151a95 95 0 0 1 111 98l-45 863z';
export const FLAG_RATIO: Record<string, number> = {us: 1.9, cn: 1.5, jp: 1.5, ca: 2, br: 10 / 7, eu: 1.5};
const FlagArt = (code: string, w: number, h: number): React.ReactNode => {
  if (code === 'us') {
    const sh = h / 13, cw = w * 0.4, ch = sh * 7, stars: React.ReactNode[] = [];
    for (let r = 0; r < 9; r++) for (let c = 0; c < (r % 2 ? 5 : 6); c++)
      stars.push(<polygon key={r + '-' + c} points={star(((r % 2 ? 2 * c + 2 : 2 * c + 1) * cw) / 12, ((r + 1) * ch) / 10, h * 0.0308)} fill="#FFFFFF" />);
    return <g><rect width={w} height={h} fill="#FFFFFF" />{Array.from({length: 7}, (_, k) => <rect key={k} y={k * 2 * sh} width={w} height={sh} fill="#B22234" />)}
      <rect width={cw} height={ch} fill="#3C3B6E" />{stars}</g>;
  }
  if (code === 'cn') {
    const u = h / 20, small = [[10, 2], [12, 4], [12, 7], [10, 9]];
    return <g><rect width={w} height={h} fill="#EE1C25" /><polygon points={star(5 * u, 5 * u, 3 * u)} fill="#FFDE00" />
      {small.map(([x, y], k) => <polygon key={k} points={star(x * u, y * u, u, (Math.atan2(5 - y, 5 - x) * 180) / Math.PI + 90)} fill="#FFDE00" />)}</g>;
  }
  if (code === 'jp') return <g><rect width={w} height={h} fill="#FFFFFF" /><circle cx={w / 2} cy={h / 2} r={h * 0.3} fill="#BC002D" /></g>;
  if (code === 'ca') return <g><rect width={w} height={h} fill="#FFFFFF" /><rect width={w / 4} height={h} fill="#D52B1E" /><rect x={(w * 3) / 4} width={w / 4} height={h} fill="#D52B1E" />
    <g transform={`scale(${w / 9600} ${h / 4800})`}><path d={CANADA_LEAF} fill="#D52B1E" /></g></g>;
  if (code === 'br') {
    const u = h / 14;
    return <g><rect width={w} height={h} fill="#009C3B" />
      <polygon points={`${1.7 * u},${7 * u} ${w / 2},${1.7 * u} ${w - 1.7 * u},${7 * u} ${w / 2},${12.3 * u}`} fill="#FFDF00" />
      <defs><clipPath id="brglobe"><circle cx={w / 2} cy={7 * u} r={3.5 * u} /></clipPath></defs>
      <circle cx={w / 2} cy={7 * u} r={3.5 * u} fill="#002776" />
      <g clipPath="url(#brglobe)"><path d={`M ${w / 2 - 2 * u - 8.5 * u} ${15.2 * u} a ${8.5 * u} ${8.5 * u} 0 0 1 ${17 * u} 0 h ${-0.5 * u} a ${8 * u} ${8 * u} 0 0 0 ${-16 * u} 0 Z`} fill="#FFFFFF" />
        {[[-1.2, 1.4, 0.22], [0.2, 2.2, 0.18], [1.1, 1.4, 0.2], [0.3, 0.9, 0.15], [-2.2, 0.6, 0.18], [2.3, 0.4, 0.15], [0.6, 2.9, 0.14], [-0.6, 2.8, 0.13], [1.6, -0.9, 0.18]].map(([dx, dy, r], k) =>
          <polygon key={k} points={star(w / 2 + dx * u, 7 * u + dy * u, r * u)} fill="#FFFFFF" />)}</g></g>;
  }
  if (code === 'eu') return <g><rect width={w} height={h} fill="#003399" />
    {Array.from({length: 12}, (_, k) => { const a = (k / 12) * Math.PI * 2; return <polygon key={k} points={star(w / 2 + Math.sin(a) * h / 3, h / 2 - Math.cos(a) * h / 3, h / 18)} fill="#FFCC00" />; })}</g>;
  return <rect width={w} height={h} fill="#888" />;
};
let flagSeq = 0;
const Flag: React.FC<{o: Obj}> = ({o}) => {
  const id = `flag${o.code}${flagSeq++}`, h = o.h ?? 300, w = h * (FLAG_RATIO[o.code] ?? 1.5), N = 28, amp = o.wave ?? h * 0.07, sw = w / N;
  const dy = (x: number) => Math.sin((x / w) * Math.PI * 2.2 + 0.4) * amp * (0.25 + x / w);
  return <g>
    <defs><g id={id}>{FlagArt(o.code, w, h)}</g>
      {Array.from({length: N}, (_, k) => <clipPath key={k} id={`${id}c${k}`}><rect x={k * sw - 0.6} y={-10} width={sw + 1.2} height={h + 20} /></clipPath>)}
      {lin(`${id}pole`, [[0, '#7A5A12'], [0.45, '#FFE9A0'], [1, '#8A6614']], 1, 0)}</defs>
    {o.pole !== false && <g><rect x={-18} y={-40} width={22} height={o.poleH ?? h * 2.6} fill={`url(#${id}pole)`} /><circle cx={-7} cy={-48} r={22} fill="#FFD45C" stroke="#7A5A12" strokeWidth={4} /></g>}
    {Array.from({length: N}, (_, k) => { const x = k * sw + sw / 2, slope = Math.cos((x / w) * Math.PI * 2.2 + 0.4);
      return <g key={k} transform={`translate(0 ${dy(x)})`}><g clipPath={`url(#${id}c${k})`}><use href={`#${id}`} />
        <rect x={k * sw - 0.6} width={sw + 1.2} height={h} fill={slope > 0 ? '#FFFFFF' : '#000000'} opacity={Math.abs(slope) * 0.22} /></g></g>; })}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ heroes */
type HeroFn = (o: Obj, id: string) => React.ReactNode;
const HEROES: Record<string, HeroFn> = {
  flag: (o) => <Flag o={o} />,
  /** a chip in front of a glowing iridescent wafer */
  wafer: (o, id) => <g>
    <defs>
      {lin(`${id}w`, [[0, '#FF3EA5'], [0.25, '#7B5CFF'], [0.5, '#21D4FD'], [0.75, '#3CFF9E'], [1, '#FFD43B']], 1, 1)}
      {lin(`${id}rim`, [[0, '#F4F7FB'], [0.5, '#6E7A8C'], [1, '#E6EBF2']], 1, 1)}
      {lin(`${id}pk`, [[0, '#3A4152'], [1, '#0C0F16']], 1, 1)}
      {lin(`${id}die`, [[0, o.die0 ?? '#5FE3FF'], [0.5, o.die1 ?? '#2A5BFF'], [1, o.die2 ?? '#FFB238']], 1, 1)}
      <clipPath id={`${id}wc`}><ellipse cx={160} cy={-60} rx={540} ry={330} /></clipPath>
    </defs>
    {o.wafer !== false && <g>
      <ellipse cx={170} cy={-30} rx={560} ry={350} fill="#0B0F18" />
      <ellipse cx={160} cy={-60} rx={540} ry={330} fill={`url(#${id}w)`} />
      <g clipPath={`url(#${id}wc)`} opacity={0.55}>
        {Array.from({length: 30}, (_, k) => <path key={'a' + k} d={`M ${-500 + k * 46} -420 L ${-260 + k * 46} 300`} stroke="#0B0F18" strokeWidth={4} />)}
        {Array.from({length: 22}, (_, k) => <path key={'b' + k} d={`M -440 ${-420 + k * 36} L 800 ${-500 + k * 36}`} stroke="#0B0F18" strokeWidth={4} />)}
      </g>
      <ellipse cx={160} cy={-60} rx={540} ry={330} fill="none" stroke={`url(#${id}rim)`} strokeWidth={20} />
      <path d="M -260 -300 Q 120 -420 520 -280" stroke="#FFFFFF" strokeWidth={14} opacity={0.5} fill="none" strokeLinecap="round" />
    </g>}
    <g transform="translate(-140 260) matrix(0.9 0.42 -0.9 0.42 0 0)">
      <rect x={-300} y={-300} width={600} height={600} rx={30} fill="#06080C" transform="translate(40 40)" />
      {Array.from({length: 14}, (_, k) => <g key={k}>
        <rect x={-270 + k * 40} y={-340} width={18} height={44} fill="#FFC94A" /><rect x={-270 + k * 40} y={296} width={18} height={44} fill="#FFC94A" />
        <rect x={-340} y={-270 + k * 40} width={44} height={18} fill="#FFC94A" /><rect x={296} y={-270 + k * 40} width={44} height={18} fill="#FFC94A" /></g>)}
      <rect x={-300} y={-300} width={600} height={600} rx={30} fill={`url(#${id}pk)`} stroke="#FFC94A" strokeWidth={6} />
      <rect x={-210} y={-210} width={420} height={420} rx={14} fill={`url(#${id}die)`} />
      {Array.from({length: 7}, (_, k) => <path key={k} d={`M ${-180 + k * 60} -190 L ${-180 + k * 60} 190 M -190 ${-180 + k * 60} L 190 ${-180 + k * 60}`} stroke="#FFFFFF" strokeOpacity={0.22} strokeWidth={3} />)}
      <rect x={-210} y={-210} width={420} height={420} rx={14} fill="none" stroke="#FFFFFF" strokeOpacity={0.7} strokeWidth={6} />
    </g>
  </g>,
  /** a steel transmission pylon with live lines */
  pylon: (o, id) => { const lv = [-380, -200, -40];
    return <g>
      <defs>{lin(`${id}st`, [[0, '#E9EEF5'], [1, '#7C8798']], 1, 0)}</defs>
      {lv.map((y, k) => { const hw = 320 - k * 40; return <g key={'w' + k}>
        <path d={`M ${-hw} ${y + 60} Q ${-hw - 500} ${y + 220} ${-hw - 1100} ${y + 120}`} stroke={o.line ?? '#7FE0FF'} strokeWidth={10} fill="none" opacity={0.8} filter="url(#pglow)" />
        <path d={`M ${hw} ${y + 60} Q ${hw + 400} ${y + 200} ${hw + 900} ${y + 100}`} stroke={o.line ?? '#7FE0FF'} strokeWidth={10} fill="none" opacity={0.8} filter="url(#pglow)" />
        <path d={`M ${-hw} ${y + 60} Q ${-hw - 500} ${y + 220} ${-hw - 1100} ${y + 120} M ${hw} ${y + 60} Q ${hw + 400} ${y + 200} ${hw + 900} ${y + 100}`} stroke="#FFFFFF" strokeWidth={3} fill="none" /></g>; })}
      <path d="M -300 560 L -70 -520 L 70 -520 L 300 560" fill="none" stroke={`url(#${id}st)`} strokeWidth={26} strokeLinejoin="round" />
      {Array.from({length: 9}, (_, k) => { const y0 = 560 - k * 120, y1 = y0 - 120, f = (y: number) => 70 + ((y + 520) / 1080) * 230;
        return <path key={k} d={`M ${-f(y0)} ${y0} L ${f(y1)} ${y1} M ${f(y0)} ${y0} L ${-f(y1)} ${y1}`} stroke={`url(#${id}st)`} strokeWidth={12} />; })}
      {lv.map((y, k) => { const hw = 320 - k * 40; return <g key={'a' + k}>
        <path d={`M ${-hw} ${y} L ${hw} ${y} L ${hw - 60} ${y - 40} L ${-hw + 60} ${y - 40} Z`} fill="none" stroke={`url(#${id}st)`} strokeWidth={14} />
        {[-hw, hw].map((x) => <g key={x}><rect x={x - 12} y={y} width={24} height={60} rx={8} fill="#9FD8FF" stroke="#2A3A50" strokeWidth={4} /><circle cx={x} cy={y + 62} r={16} fill="#FFFFFF" filter="url(#pglow)" /></g>)}</g>; })}
      <path d="M -70 -520 L 0 -640 L 70 -520" fill="none" stroke={`url(#${id}st)`} strokeWidth={18} />
    </g>; },
  /** an orange industrial robot arm welding a glowing workpiece */
  arm: (o, id) => { const c = o.color ?? '#FF8A00';
    return <g>
      <defs>{lin(`${id}o`, [[0, '#FFD08A'], [0.35, c], [1, '#8A3A00']], 1, 1)}{lin(`${id}m`, [[0, '#E6EBF2'], [1, '#5A6474']], 1, 1)}
        {rad(`${id}hot`, [[0, '#FFFFFF'], [0.3, '#FFE27A'], [0.7, '#FF6A00', 0.8], [1, '#FF3A00', 0]])}</defs>
      <path d="M -420 520 L 560 520 L 620 600 L -480 600 Z" fill="#20242E" /><rect x={-480} y={600} width={1100} height={60} fill="#11141A" />
      <rect x={140} y={360} width={420} height={160} rx={18} fill="#7A8698" stroke="#2A2F3A" strokeWidth={8} />
      <ellipse cx={360} cy={370} rx={140} ry={34} fill={`url(#${id}hot)`} />
      <ellipse cx={-180} cy={500} rx={210} ry={50} fill="#2A2F3A" /><rect x={-330} y={380} width={300} height={120} rx={20} fill={`url(#${id}m)`} />
      <rect x={-300} y={300} width={240} height={110} rx={30} fill={`url(#${id}o)`} stroke="#3A1A00" strokeWidth={8} />
      <g transform="translate(-180 330) rotate(-62)"><rect x={-70} y={-40} width={560} height={150} rx={70} fill={`url(#${id}o)`} stroke="#3A1A00" strokeWidth={8} />
        <rect x={20} y={-10} width={380} height={20} rx={10} fill="#FFFFFF" opacity={0.35} /></g>
      <circle cx={-180} cy={330} r={95} fill={`url(#${id}m)`} stroke="#2A2F3A" strokeWidth={8} /><circle cx={-180} cy={330} r={40} fill="#2A2F3A" />
      <g transform="translate(60 -120) rotate(28)"><rect x={-50} y={-55} width={470} height={115} rx={56} fill={`url(#${id}o)`} stroke="#3A1A00" strokeWidth={8} />
        <rect x={20} y={-30} width={330} height={16} rx={8} fill="#FFFFFF" opacity={0.35} /></g>
      <circle cx={60} cy={-120} r={82} fill={`url(#${id}m)`} stroke="#2A2F3A" strokeWidth={8} /><circle cx={60} cy={-120} r={32} fill="#2A2F3A" />
      <g transform="translate(450 90) rotate(8)"><rect x={-40} y={-60} width={80} height={160} rx={18} fill={`url(#${id}m)`} stroke="#2A2F3A" strokeWidth={6} />
        <path d="M -16 100 L 16 100 L 6 230 L -6 230 Z" fill="#3A4250" /></g>
      <circle cx={450} cy={90} r={60} fill={`url(#${id}m)`} stroke="#2A2F3A" strokeWidth={6} />
      <circle cx={380} cy={352} r={80} fill={`url(#${id}hot)`} />
    </g>; },
  /** a container ship, bow towards the viewer-left; optional flags on poles above the stacks */
  ship: (o, id) => { const m = -0.1, deck = (x: number) => 40 + (x + 520) * m, cols = ['#D8352A', '#1F6FD1', '#F08A1C', '#16A39A', '#E9EEF5', '#FFC12E', '#B52A6E', '#2D4FA3'];
    return <g>
      <defs>{lin(`${id}hull`, [[0, '#24324F'], [0.7, '#0B1222'], [1, '#05080F']])}{lin(`${id}br`, [[0, '#FFFFFF'], [1, '#AAB6C8']], 1, 0)}</defs>
      {Array.from({length: 19}, (_, i) => { const x = -400 + i * 40, h = 3 + Math.floor(rnd(i + 3) * 3);
        return Array.from({length: h}, (_, k) => { const y = deck(x) - (k + 1) * 36, c = cols[Math.floor(rnd(i * 7 + k) * cols.length)];
          return <g key={i + '-' + k}><rect x={x} y={y} width={38} height={34} fill={c} stroke="#0B111C" strokeWidth={2} />
            <rect x={x} y={y} width={38} height={6} fill="#FFFFFF" opacity={0.25} />{[8, 18, 28].map((d) => <rect key={d} x={x + d} y={y + 8} width={2} height={22} fill="#000" opacity={0.2} />)}</g>; }); })}
      <rect x={380} y={deck(380) - 260} width={120} height={260} fill={`url(#${id}br)`} stroke="#0B111C" strokeWidth={4} />
      <rect x={370} y={deck(380) - 270} width={150} height={26} fill="#E9EEF5" stroke="#0B111C" strokeWidth={3} />
      {[0, 1, 2, 3].map((r) => <rect key={r} x={390} y={deck(380) - 240 + r * 50} width={100} height={14} fill="#1A2A44" />)}
      <rect x={440} y={deck(380) - 340} width={10} height={80} fill="#E9EEF5" />
      <path d={`M -520 40 L 540 ${deck(540)} L 540 ${deck(540) + 200} L -440 270 Z`} fill={`url(#${id}hull)`} stroke="#0B111C" strokeWidth={4} />
      <path d={`M -470 210 L 540 ${deck(540) + 150} L 540 ${deck(540) + 200} L -440 270 Z`} fill="#C22A2A" />
      <path d={`M -520 40 L 540 ${deck(540)}`} stroke="#FFFFFF" strokeWidth={6} opacity={0.5} />
      {o.flags && (o.flags as string[]).map((c, k) => <g key={c + k} transform={`translate(${-260 + k * 260} ${deck(-260 + k * 260) - 560}) scale(${o.flagS ?? 0.62})`}><Flag o={{kind: 'flag', code: c, x: 0, y: 0, s: 1, h: 300, poleH: 760}} /></g>)}
      <path d="M -560 250 Q -470 200 -380 270 Q -200 300 0 250 Q 200 220 560 190 L 560 240 Q 200 280 -100 300 Q -380 320 -580 290 Z" fill="#FFFFFF" opacity={0.85} filter="url(#psoft)" />
      {Array.from({length: 22}, (_, k) => <circle key={k} cx={-560 + rnd(k) * 200} cy={180 + rnd(k + 1) * 110} r={4 + rnd(k + 2) * 10} fill="#FFFFFF" opacity={0.8} />)}
    </g>; },
  /** stacks of banknotes and gold coins */
  cash: (o, id) => <g>
    <defs>{lin(`${id}b`, [[0, '#B8F2B0'], [0.5, '#4FBF5A'], [1, '#1F6E2C']], 1, 1)}{lin(`${id}g`, [[0, '#FFF3A8'], [0.5, '#FFC21A'], [1, '#B07800']], 1, 1)}</defs>
    {[[-300, 220], [0, 220], [300, 220], [-150, 60], [150, 60], [0, -100]].map(([x, y], k) => <g key={k} transform={`translate(${x} ${y})`}>
      {[0, 1, 2, 3, 4].map((l) => <rect key={l} x={-150} y={-40 - l * 22} width={300} height={70} rx={8} fill={`url(#${id}b)`} stroke="#0E3A16" strokeWidth={4} />)}
      <rect x={-40} y={-128} width={80} height={70} fill="#FFFFFF" opacity={0.9} /><text x={0} y={-74} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={54} fill="#1F6E2C">$</text></g>)}
    {[[-520, 330], [480, 320], [-420, 380], [600, 380], [360, 400]].map(([x, y], k) => <g key={'c' + k}>{[0, 1, 2, 3].map((l) =>
      <ellipse key={l} cx={x} cy={y - l * 22} rx={90} ry={32} fill={`url(#${id}g)`} stroke="#7A5200" strokeWidth={4} />)}</g>)}
  </g>,
  coins: (o, id) => <g>
    <defs>{lin(`${id}g`, [[0, '#FFF3A8'], [0.5, '#FFC21A'], [1, '#B07800']], 1, 1)}</defs>
    {Array.from({length: o.n ?? 14}, (_, k) => { const x = (rnd(k) - 0.5) * 700, y = (rnd(k + 5) - 0.3) * 300;
      return <g key={k} transform={`translate(${x} ${y}) rotate(${rnd(k + 2) * 60 - 30})`}><ellipse rx={95} ry={95 * (0.35 + rnd(k + 3) * 0.65)} fill={`url(#${id}g)`} stroke="#7A5200" strokeWidth={6} />
        <text y={30 * (0.35 + rnd(k + 3) * 0.65)} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={90} fill="#8A5A00" transform={`scale(1 ${0.35 + rnd(k + 3) * 0.65})`}>$</text></g>; })}
  </g>,
  /** a glass data center with glowing server racks */
  datacenter: (o, id) => <g>
    <defs>{lin(`${id}gl`, [[0, '#2A4E8A', 0.85], [1, '#081428', 0.95]])}{lin(`${id}sd`, [[0, '#13284A'], [1, '#060E1C']], 1, 0)}</defs>
    <ellipse cx={40} cy={300} rx={640} ry={60} fill={o.glow ?? '#3FB4FF'} opacity={0.35} filter="url(#psoft)" />
    <path d="M 300 -280 L 520 -220 L 520 290 L 300 280 Z" fill={`url(#${id}sd)`} stroke="#0A1630" strokeWidth={4} />
    <rect x={-460} y={-280} width={760} height={560} fill={`url(#${id}gl)`} stroke="#0A1630" strokeWidth={4} />
    {Array.from({length: 6}, (_, k) => <g key={k} transform={`translate(${-420 + k * 120} -200)`}>
      <rect width={96} height={440} fill="#0A1222" stroke="#2C5A9A" strokeWidth={3} />
      {Array.from({length: 18}, (_, r) => <g key={r}><rect x={10} y={14 + r * 23} width={76} height={6} fill="#13243F" />
        <circle cx={18 + (r % 3) * 22} cy={17 + r * 23} r={3.5} fill={rnd(k * 31 + r) > 0.3 ? (o.led ?? '#5FE3FF') : '#7DFFB0'} /></g>)}</g>)}
    {Array.from({length: 7}, (_, k) => <rect key={'m' + k} x={-460 + k * 126} y={-280} width={6} height={560} fill="#8FC8FF" opacity={0.4} />)}
    <path d="M -480 -290 L 300 -290 L 530 -228" stroke={o.glow ?? '#3FB4FF'} strokeWidth={14} fill="none" filter="url(#pglow)" />
    <path d="M -480 -290 L 300 -290 L 530 -228" stroke="#E6FBFF" strokeWidth={4} fill="none" />
    <path d="M -440 -250 L 280 -250" stroke="#FFFFFF" strokeWidth={8} opacity={0.25} />
  </g>,
  /** a suburban house with warm windows */
  house: (o, id) => <g>
    <defs>{lin(`${id}wall`, [[0, '#FFF1DA'], [1, '#C8A982']], 1, 1)}{lin(`${id}roof`, [[0, o.roof ?? '#B5432F'], [1, '#5A1A12']], 0, 1)}
      {rad(`${id}win`, [[0, '#FFF6C8'], [0.6, '#FFC24A'], [1, '#FF8A1A']])}</defs>
    <ellipse cx={0} cy={330} rx={520} ry={50} fill="#000" opacity={0.35} filter="url(#psoft)" />
    <rect x={190} y={-330} width={70} height={160} fill="#6A3A2A" stroke={OL} strokeWidth={6} />
    <rect x={-330} y={-90} width={660} height={420} fill={`url(#${id}wall)`} stroke={OL} strokeWidth={8} />
    <path d="M -410 -60 L 0 -380 L 410 -60 Z" fill={`url(#${id}roof)`} stroke={OL} strokeWidth={8} strokeLinejoin="round" />
    <path d="M -380 -70 L 0 -360" stroke="#FFFFFF" strokeOpacity={0.3} strokeWidth={10} />
    {[[-240, -10], [110, -10], [-240, 150]].map(([x, y], k) => <g key={k}><rect x={x} y={y} width={130} height={110} fill={`url(#${id}win)`} stroke={OL} strokeWidth={6} />
      <path d={`M ${x + 65} ${y} L ${x + 65} ${y + 110} M ${x} ${y + 55} L ${x + 130} ${y + 55}`} stroke="#6A3A2A" strokeWidth={6} /></g>)}
    <rect x={90} y={150} width={110} height={180} fill="#5A2A1C" stroke={OL} strokeWidth={6} /><circle cx={180} cy={245} r={8} fill="#FFD45C" />
    <circle cx={0} cy={-200} r={44} fill={`url(#${id}win)`} stroke={OL} strokeWidth={6} />
  </g>,
  /** a sleek white robot; chest: 'core' (glowing) | 'open' (cash pours out); hold: 'tax' */
  robot: (o, id) => <g>
    <defs>{lin(`${id}b`, [[0, '#FFFFFF'], [0.6, '#C9D2DE'], [1, '#7C8798']], 1, 1)}{rad(`${id}core`, [[0, '#FFFFFF'], [0.4, o.eye ?? '#5FE3FF'], [1, o.eye ?? '#5FE3FF', 0]])}
      {rad(`${id}gold`, [[0, '#FFFBE0'], [0.5, '#FFC21A'], [1, '#FF8A00', 0.2]])}</defs>
    {[-1, 1].map((sd) => <g key={sd}>
      <g transform={`translate(${sd * 300} -80) rotate(${sd * (o.armsUp ? -150 : 18)})`}><rect x={-60} y={0} width={120} height={330} rx={60} fill={`url(#${id}b)`} stroke="#2A3340" strokeWidth={6} />
        <circle cx={0} cy={360} r={72} fill="#5A6474" stroke="#2A3340" strokeWidth={6} /></g>
      <circle cx={sd * 300} cy={-80} r={86} fill={`url(#${id}b)`} stroke="#2A3340" strokeWidth={6} /></g>)}
    <path d="M -290 -60 Q -290 -170 -170 -190 L 170 -190 Q 290 -170 290 -60 L 240 470 L -240 470 Z" fill={`url(#${id}b)`} stroke="#2A3340" strokeWidth={6} />
    <path d="M -150 -150 L 150 -150 L 130 200 L -130 200 Z" fill="#E9EEF5" stroke="#9AA6B8" strokeWidth={4} />
    {o.chest === 'open' ? <g><rect x={-120} y={-110} width={240} height={250} rx={20} fill="#140C02" stroke="#2A3340" strokeWidth={6} />
      <rect x={-110} y={-100} width={220} height={230} rx={16} fill={`url(#${id}gold)`} />
      <path d="M -120 -110 L -230 -170 L -230 90 L -120 140 Z" fill="#C9D2DE" stroke="#2A3340" strokeWidth={6} /></g>
      : <g><circle cx={0} cy={10} r={110} fill={`url(#${id}core)`} /><circle cx={0} cy={10} r={48} fill="#FFFFFF" /></g>}
    <rect x={-60} y={-250} width={120} height={70} fill="#5A6474" />
    <rect x={-170} y={-560} width={340} height={320} rx={110} fill={`url(#${id}b)`} stroke="#2A3340" strokeWidth={6} />
    <rect x={-135} y={-480} width={270} height={140} rx={60} fill="#0A1222" />
    {[-60, 60].map((x) => <g key={x}><ellipse cx={x} cy={-410} rx={44} ry={30} fill={`url(#${id}core)`} /><ellipse cx={x} cy={-410} rx={20} ry={14} fill="#FFFFFF" /></g>)}
    {[-1, 1].map((sd) => <circle key={'e' + sd} cx={sd * 178} cy={-400} r={42} fill="#7C8798" stroke={o.eye ?? '#5FE3FF'} strokeWidth={8} />)}
    <path d="M -120 -540 Q 0 -585 120 -540" stroke="#FFFFFF" strokeWidth={14} opacity={0.6} fill="none" strokeLinecap="round" />
    {o.hold === 'tax' && <g transform="translate(330 120) rotate(10)"><rect x={-150} y={-200} width={300} height={380} rx={10} fill="#FFFDF5" stroke={OL} strokeWidth={8} />
      <rect x={-150} y={-200} width={300} height={90} fill="#C9302C" /><text x={0} y={-132} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={70} fill="#FFFFFF">TAX</text>
      {[0, 1, 2, 3, 4].map((l) => <rect key={l} x={-110} y={-80 + l * 46} width={l === 4 ? 120 : 220} height={14} fill="#B8C0CC" />)}</g>}
  </g>,
  /** a sleek electric car, side view, facing left */
  car: (o, id) => <g>
    <defs>{lin(`${id}p`, [[0, o.c0 ?? '#FF6A5A'], [0.45, o.c1 ?? '#D7192A'], [1, o.c2 ?? '#5A0610']])}{lin(`${id}gl`, [[0, '#9FD8FF'], [0.5, '#1A2A44'], [1, '#05080F']], 1, 1)}
      {rad(`${id}hl`, [[0, '#FFFFFF'], [0.4, '#BFEFFF'], [1, '#5FE3FF', 0]])}</defs>
    <ellipse cx={0} cy={210} rx={620} ry={40} fill="#000" opacity={0.6} filter="url(#psoft)" />
    {Array.from({length: 8}, (_, k) => <rect key={k} x={620 + rnd(k) * 120} y={-120 + k * 34} width={200 + rnd(k + 1) * 300} height={6} rx={3} fill="#FFFFFF" opacity={0.35} />)}
    <path d="M -580 90 Q -590 10 -500 -10 L -320 -50 Q -190 -175 -20 -185 L 170 -185 Q 320 -175 430 -80 L 540 -60 Q 600 -45 600 30 L 590 110 Q 580 140 540 140 L -540 140 Q -585 140 -580 90 Z"
      fill={`url(#${id}p)`} stroke={OL} strokeWidth={6} />
    <path d="M -270 -60 Q -160 -150 -20 -160 L 160 -160 Q 270 -152 360 -80 Z" fill={`url(#${id}gl)`} stroke={OL} strokeWidth={5} />
    <path d="M 60 -160 L 40 -60" stroke={OL} strokeWidth={10} />
    <path d="M -500 -5 Q 0 -60 560 -50" stroke="#FFFFFF" strokeOpacity={0.6} strokeWidth={6} fill="none" />
    <ellipse cx={-560} cy={20} rx={70} ry={26} fill={`url(#${id}hl)`} />
    <rect x={560} y={0} width={40} height={20} rx={8} fill="#FF2D2D" filter="url(#pglow)" />
    {[-340, 340].map((x) => <g key={x}><circle cx={x} cy={140} r={100} fill="#0B0D12" stroke={OL} strokeWidth={6} /><circle cx={x} cy={140} r={62} fill="#AEB8C6" />
      {Array.from({length: 6}, (_, k) => <path key={k} d={`M ${x} 140 L ${x + Math.cos(k) * 58} ${140 + Math.sin(k) * 58}`} stroke="#3A4250" strokeWidth={12} />)}<circle cx={x} cy={140} r={16} fill="#3A4250" /></g>)}
  </g>,
  /** a golden shovel whose blade carries a glowing chip */
  shovel: (o, id) => <g transform="rotate(-28)">
    <defs>{lin(`${id}g`, [[0, '#FFF3A8'], [0.5, '#FFC21A'], [1, '#9A6A00']], 1, 0)}{lin(`${id}die`, [[0, '#5FE3FF'], [1, '#2A5BFF']], 1, 1)}</defs>
    <rect x={-36} y={-640} width={72} height={600} rx={30} fill={`url(#${id}g)`} stroke="#5A3A00" strokeWidth={8} />
    <path d="M -140 -700 L 140 -700 L 140 -630 L -140 -630 Z" fill={`url(#${id}g)`} stroke="#5A3A00" strokeWidth={8} />
    <path d="M -250 -60 L 250 -60 L 240 260 Q 0 470 -240 260 Z" fill={`url(#${id}g)`} stroke="#5A3A00" strokeWidth={10} strokeLinejoin="round" />
    <rect x={-150} y={-10} width={300} height={260} rx={24} fill="#141A24" stroke="#FFC94A" strokeWidth={6} />
    {[-100, -40, 20, 80].map((x) => <path key={x} d={`M ${x + 10} -10 L ${x + 10} -40 M ${x + 10} 250 L ${x + 10} 280`} stroke="#FFC94A" strokeWidth={12} />)}
    <rect x={-90} y={50} width={180} height={140} rx={14} fill={`url(#${id}die)`} />
    <path d="M -200 -40 Q 0 -70 200 -40" stroke="#FFFFFF" strokeWidth={10} opacity={0.5} fill="none" />
  </g>,
  /** a generic gold membership card (no brand) */
  card: (o, id) => <g transform={`rotate(${o.r ?? -12})`}>
    <defs>{lin(`${id}c`, [[0, '#FFF0A8'], [0.4, '#FFC21A'], [1, '#B06A00']], 1, 1)}</defs>
    <rect x={-420} y={-260} width={840} height={520} rx={44} fill={`url(#${id}c)`} stroke="#5A3A00" strokeWidth={10} />
    <rect x={-330} y={-130} width={150} height={115} rx={16} fill="#E9D9A0" stroke="#8A6200" strokeWidth={5} />
    <path d="M -330 -72 L -180 -72 M -255 -130 L -255 -15" stroke="#8A6200" strokeWidth={5} />
    <text x={-340} y={130} fontFamily={FONT} fontWeight={900} fontSize={110} fontStyle="italic" fill="#3A2400">{o.label ?? 'MEMBER'}</text>
    <rect x={-340} y={170} width={400} height={24} rx={12} fill="#8A6200" opacity={0.5} />
    <path d="M -380 -230 Q 0 -300 380 -200" stroke="#FFFFFF" strokeWidth={18} opacity={0.5} fill="none" strokeLinecap="round" />
  </g>,
  /** a shopping cart heaped with bulk boxes */
  cart: (o, id) => <g>
    <defs>{lin(`${id}m`, [[0, '#F4F7FB'], [1, '#7C8798']], 1, 1)}</defs>
    {[[-280, -150, 220, 180, '#C8874A'], [-40, -200, 240, 230, '#E0A060'], [200, -140, 200, 170, '#B5743A'], [-160, -330, 200, 160, '#F2C46A'], [80, -360, 180, 170, '#D79A55']].map(([x, y, w, h, c], k) =>
      <g key={k}><rect x={x as number} y={y as number} width={w as number} height={h as number} fill={c as string} stroke={OL} strokeWidth={6} />
        <rect x={(x as number) + (w as number) / 2 - 20} y={y as number} width={40} height={h as number} fill="#000" opacity={0.12} /></g>)}
    <path d="M -420 -10 L 420 -10 L 360 260 L -340 260 Z" fill="#5FA8FF" fillOpacity={0.18} stroke={`url(#${id}m)`} strokeWidth={16} strokeLinejoin="round" />
    {Array.from({length: 9}, (_, k) => <path key={k} d={`M ${-380 + k * 90} -10 L ${-320 + k * 82} 260`} stroke={`url(#${id}m)`} strokeWidth={6} />)}
    {[70, 150].map((y) => <path key={y} d={`M ${-400 + y * 0.2} ${y} L ${400 - y * 0.18} ${y}`} stroke={`url(#${id}m)`} strokeWidth={6} />)}
    <path d="M 420 -10 L 470 -120 L 600 -120" stroke={`url(#${id}m)`} strokeWidth={18} fill="none" strokeLinecap="round" />
    <path d="M -340 260 L -360 330 L 360 330" stroke={`url(#${id}m)`} strokeWidth={14} fill="none" />
    {[-300, 300].map((x) => <circle key={x} cx={x} cy={370} r={42} fill="#1A1E26" stroke="#AEB8C6" strokeWidth={10} />)}
  </g>,
  /** a fanned stack of bond certificates with gold seals */
  bonds: (o, id) => <g>
    <defs>{lin(`${id}p`, [[0, '#FFFCEB'], [1, '#E8DDB8']], 1, 1)}{rad(`${id}s`, [[0, '#FFF3A8'], [0.7, '#FFC21A'], [1, '#B07800']])}</defs>
    {[-16, -8, 0].map((r, k) => <g key={k} transform={`rotate(${r}) translate(${k * 30} ${-k * 20})`}>
      <rect x={-420} y={-280} width={840} height={540} rx={12} fill={`url(#${id}p)`} stroke="#3A2A10" strokeWidth={8} />
      <rect x={-385} y={-245} width={770} height={470} rx={8} fill="none" stroke="#2F6E4A" strokeWidth={10} strokeDasharray="22 10" />
      <text x={0} y={-140} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={66} fill="#1E3A2C">{o.label ?? 'TREASURY BOND'}</text>
      {[0, 1, 2].map((l) => <rect key={l} x={-300} y={-80 + l * 50} width={l === 2 ? 340 : 600} height={18} fill="#B8AE8A" />)}
      <circle cx={260} cy={130} r={86} fill={`url(#${id}s)`} stroke="#7A5200" strokeWidth={6} />
      <polygon points={star(260, 130, 50)} fill="#FFF3A8" stroke="#7A5200" strokeWidth={4} /></g>)}
  </g>,
  /** an oil barrel with a glowing lightning bolt */
  barrel: (o, id) => <g>
    <defs>{lin(`${id}b`, [[0, '#0B0D12'], [0.3, '#3A4250'], [0.5, '#5A6474'], [0.7, '#2A3140'], [1, '#0B0D12']], 1, 0)}</defs>
    <rect x={-260} y={-340} width={520} height={680} rx={40} fill={`url(#${id}b)`} stroke={OL} strokeWidth={8} />
    <ellipse cx={0} cy={-340} rx={260} ry={60} fill="#5A6474" stroke={OL} strokeWidth={8} /><ellipse cx={0} cy={-340} rx={200} ry={40} fill="#2A3140" />
    {[-130, 130].map((y) => <rect key={y} x={-266} y={y - 16} width={532} height={32} rx={10} fill="#1A1E26" stroke="#5A6474" strokeWidth={3} />)}
    <polygon points="40,-260 -140,40 -20,40 -60,270 140,-40 20,-40 80,-260" fill={o.bolt ?? '#FFD23F'} stroke="#7A4A00" strokeWidth={8} strokeLinejoin="round" filter="url(#pglow)" />
  </g>,
  /** rising (or falling) glowing arrow over bars */
  arrow: (o, id) => { const up = o.dir !== 'down', c = o.color ?? (up ? '#FFC24A' : '#FF3A2A');
    const bars = (o.bars ?? 5) as number;
    return <g>
      <defs>{lin(`${id}bar`, [[0, c, 0.95], [1, c, 0.15]])}</defs>
      {o.noBars ? null : Array.from({length: bars}, (_, k) => { const h = up ? 120 + k * 90 : 120 + (bars - 1 - k) * 90; return <rect key={k} x={-360 + k * 150} y={300 - h} width={110} height={h} fill={`url(#${id}bar)`} />; })}
      <path d={up ? 'M -440 220 Q -60 160 320 -260' : 'M -440 -260 Q -60 -160 320 220'} stroke={c} strokeWidth={48} fill="none" strokeLinecap="round" filter="url(#pglow)" />
      <path d={up ? 'M -440 220 Q -60 160 320 -260' : 'M -440 -260 Q -60 -160 320 220'} stroke="#FFFFFF" strokeWidth={12} fill="none" strokeLinecap="round" opacity={0.8} />
      <polygon points={up ? '420,-380 200,-310 380,-150' : '420,340 200,270 380,110'} fill={c} stroke="#FFFFFF" strokeWidth={8} strokeLinejoin="round" filter="url(#pglow)" />
    </g>; },
  /** a big glowing lightning bolt */
  bolt: (o) => <polygon points="60,-420 -200,60 -30,60 -90,420 220,-80 50,-80 140,-420" fill={o.color ?? '#FFE14D'} stroke="#FFFFFF" strokeWidth={10} strokeLinejoin="round" filter="url(#pglow)" />,
  /** a price tag on a string (no number unless the brief sets one from FACT_CHECK) */
  pricetag: (o, id) => <g transform={`rotate(${o.r ?? 18})`}>
    <defs>{lin(`${id}t`, [[0, '#FFF0A8'], [0.5, '#FFC928'], [1, '#D99A00']], 1, 1)}</defs>
    <path d="M -250 0 Q -360 -160 -260 -280" fill="none" stroke="#FFFFFF" strokeWidth={10} />
    <path d="M -300 0 L -180 -150 L 300 -150 L 300 150 L -180 150 Z" fill={`url(#${id}t)`} stroke={OL} strokeWidth={10} strokeLinejoin="round" />
    <circle cx={-200} cy={0} r={28} fill="#1A1E26" />
    {o.text ? <text x={60} y={50} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontStyle="italic" fontSize={150} fill={OL}>{o.text}</text>
      : <polygon points="60,110 -60,-10 10,-10 10,-110 110,-110 110,-10 180,-10" fill="#E3201B" stroke={OL} strokeWidth={6} />}
  </g>,
  /** a tax document */
  taxdoc: (o) => <g transform={`rotate(${o.r ?? 8})`}><rect x={-260} y={-340} width={520} height={680} rx={14} fill="#FFFDF5" stroke={OL} strokeWidth={10} />
    <rect x={-260} y={-340} width={520} height={150} fill="#C9302C" /><text x={0} y={-230} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={110} fill="#FFFFFF">TAX</text>
    {[0, 1, 2, 3, 4, 5].map((l) => <rect key={l} x={-200} y={-140 + l * 70} width={l === 5 ? 200 : 400} height={22} fill="#B8C0CC" />)}</g>,
};

const HeroNode: React.FC<{o: Obj; i: number; fx: boolean}> = ({o, i, fx}) => {
  const id = `h${i}${o.kind}`;
  const fn = HEROES[o.kind];
  const body = fn ? <g transform={`translate(${o.x} ${o.y}) rotate(${o.rot ?? 0}) scale(${(o.flip ? -1 : 1) * o.s} ${o.s})`}>{fn(o, id)}</g>
    : SUBJECTS[o.kind] ? SUBJECTS[o.kind](o, {sky0: '#05070B', sky1: '#141B26', haze: '#FFB238', key: '#FFF3E0', accent: '#FFD23F', ink: '#FFFFFF'}) : null;
  return <g filter={fx && o.fx !== false ? 'url(#herofx)' : undefined}>{body}</g>;
};

/* ------------------------------------------------------------------------------------------------ effects */
const boltPath = (x1: number, y1: number, x2: number, y2: number, seed: number) => {
  const n = 12, dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy), nx = -dy / L, ny = dx / L, pts: string[] = [`M ${x1} ${y1}`];
  for (let k = 1; k < n; k++) { const t = k / n, off = (rnd(seed + k) - 0.5) * L * 0.16; pts.push(`L ${x1 + dx * t + nx * off} ${y1 + dy * t + ny * off}`); }
  pts.push(`L ${x2} ${y2}`);
  return pts.join(' ');
};
const qpt = (p: [number, number][], t: number): [number, number] => {
  if (p.length === 2) return [p[0][0] + (p[1][0] - p[0][0]) * t, p[0][1] + (p[1][1] - p[0][1]) * t];
  const [a, b, c] = p; const u = 1 - t;
  return [u * u * a[0] + 2 * u * t * b[0] + t * t * c[0], u * u * a[1] + 2 * u * t * b[1] + t * t * c[1]];
};
const Flow: React.FC<{f: NonNullable<PosterProps['flows']>[number]; i: number}> = ({f, i}) => {
  const c = f.color ?? '#7FE0FF', d = f.p.length === 3 ? `M ${f.p[0].join(' ')} Q ${f.p[1].join(' ')} ${f.p[2].join(' ')}` : `M ${f.p[0].join(' ')} L ${f.p[1].join(' ')}`;
  const n = f.n ?? 14;
  return <g>
    {(f.kind ?? 'energy') === 'energy' && <g><path d={d} stroke={c} strokeWidth={(f.w ?? 14) * 2.2} fill="none" opacity={0.5} filter="url(#pglow)" strokeLinecap="round" />
      <path d={d} stroke="#FFFFFF" strokeWidth={(f.w ?? 14) * 0.45} fill="none" strokeLinecap="round" /></g>}
    {Array.from({length: n}, (_, k) => { const t = (k + 0.5) / n, [x, y] = qpt(f.p, t), r = rnd(i * 50 + k) * 50 - 25;
      if (f.kind === 'cash') return <g key={k} transform={`translate(${x} ${y}) rotate(${r}) scale(${0.6 + t * 0.6})`}>
        <rect x={-90} y={-42} width={180} height={84} rx={8} fill="#5BC466" stroke="#0E3A16" strokeWidth={5} /><rect x={-70} y={-28} width={140} height={56} rx={6} fill="none" stroke="#C9F5C0" strokeWidth={4} />
        <text x={0} y={20} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={54} fill="#0E3A16">$</text></g>;
      if (f.kind === 'coins') return <g key={k} transform={`translate(${x} ${y}) scale(${0.6 + t * 0.6})`}><ellipse rx={56} ry={56 * (0.4 + rnd(k) * 0.6)} fill="#FFC21A" stroke="#7A5200" strokeWidth={6} /></g>;
      return <circle key={k} cx={x} cy={y} r={6 + rnd(k + i) * 8} fill="#FFFFFF" />; })}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ text */
const brushPath = (x0: number, y0: number, x1: number, y1: number, seed: number) => {
  const top: string[] = [], bot: string[] = [];
  const step = 26, n = Math.ceil((x1 - x0) / step);
  for (let k = 0; k <= n; k++) { const x = x0 + (k / n) * (x1 - x0); top.push(`${x} ${y0 + (rnd(seed + k) - 0.5) * 16}`); bot.push(`${x} ${y1 + (rnd(seed + 99 + k) - 0.5) * 18}`); }
  const h = y1 - y0, right: string[] = [], left: string[] = [];
  for (let k = 1; k < 8; k++) { right.push(`${x1 + 8 + rnd(seed + 200 + k) * 46} ${y0 + (k / 8) * h}`); left.push(`${x0 - 8 - rnd(seed + 300 + k) * 54} ${y1 - (k / 8) * h}`); }
  return `M ${top.join(' L ')} L ${right.join(' L ')} L ${bot.reverse().join(' L ')} L ${left.join(' L ')} Z`;
};
const PLine: React.FC<{t: PosterText; i: number}> = ({t, i}) => {
  const left = t.anchor === 'start' ? t.x : t.anchor === 'end' ? t.x - t.width : t.x - t.width / 2;
  const sw = Math.max(10, t.size * 0.12);
  const onYellow = !!t.banner && t.color !== '#FFFFFF';
  const common = {x: t.x, y: t.y, textAnchor: t.anchor, fontFamily: FONT, fontWeight: 900, fontStyle: 'italic', fontSize: t.size, textLength: t.width,
    lengthAdjust: 'spacingAndGlyphs' as const};
  const bx0 = left - t.size * 0.22, bx1 = left + t.width + t.size * 0.28, by0 = t.y - t.size * 0.9, by1 = t.y + t.size * 0.17;
  return <g transform={`rotate(${t.rotate ?? -3} ${left} ${t.y})`}>
    {t.banner && <g>
      <path d={brushPath(bx0, by0, bx1, by1, i * 37 + 5)} fill="#000" opacity={0.55} transform="translate(12 16)" filter="url(#pshadow)" />
      <path d={brushPath(bx0, by0, bx1, by1, i * 37 + 5)} fill={t.banner} />
      {Array.from({length: 7}, (_, k) => { const y = by0 + 10 + rnd(i * 13 + k) * (by1 - by0 - 20), x0 = bx0 - 40 - rnd(k + i) * 90, x1 = bx0 + 80 + rnd(k + 7) * 200;
        return <path key={'l' + k} d={`M ${x0} ${y} L ${x1} ${y - 4} L ${x1} ${y + 6 + rnd(k) * 8} L ${x0 + 20} ${y + 4} Z`} fill={t.banner} opacity={0.9} />; })}
      {Array.from({length: 6}, (_, k) => { const y = by0 + 10 + rnd(i * 17 + k + 3) * (by1 - by0 - 20), x1 = bx1 + 30 + rnd(k + i + 4) * 80, x0 = bx1 - 160 - rnd(k + 9) * 160;
        return <path key={'r' + k} d={`M ${x0} ${y} L ${x1} ${y + 3} L ${x1 - 20} ${y + 8 + rnd(k + 1) * 6} L ${x0} ${y + 8} Z`} fill={t.banner} opacity={0.9} />; })}
      {Array.from({length: 5}, (_, k) => <path key={'d' + k} d={`M ${bx0 + rnd(k + 40 + i) * (bx1 - bx0) * 0.3} ${by0 + 12 + k * (by1 - by0 - 24) / 4} L ${bx1 - rnd(k + 50) * (bx1 - bx0) * 0.3} ${by0 + 14 + k * (by1 - by0 - 24) / 4}`}
        stroke="#000" strokeOpacity={0.08} strokeWidth={6} />)}
    </g>}
    <defs>{lin(`tf${i}`, [[0, '#FFFFFF'], [0.6, '#FFFFFF'], [1, '#C9D2DE']])}</defs>
    {!onYellow && <text {...common} x={t.x + 10} y={t.y + 14} fill="#000" stroke="#000" strokeWidth={sw * 2} strokeLinejoin="round" opacity={0.6} filter="url(#pshadow)">{t.text}</text>}
    {!onYellow && <text {...common} fill="#000" stroke={t.outline ?? OL} strokeWidth={sw * 2} strokeLinejoin="round">{t.text}</text>}
    <text {...common} fill={onYellow ? t.color : `url(#tf${i})`} stroke={onYellow ? t.color : 'none'} strokeWidth={onYellow ? 2 : 0}>{t.text}</text>
  </g>;
};

/* ------------------------------------------------------------------------------------------------ composition */
export const PosterThumb: React.FC<PosterProps> = (p) => {
  flagSeq = 0;
  const h = p.hero, lx = p.light?.x ?? h.x, ly = p.light?.y ?? h.y, lr = p.light?.r ?? 620, lc = p.light?.color ?? '#FFB238';
  const warm = p.rim?.warm ?? '#FFB238', cool = p.rim?.cool ?? '#3FB4FF';
  return (
    <AbsoluteFill style={{backgroundColor: '#020818'}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id="psoft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" /></filter>
          <filter id="pshadow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="8" /></filter>
          <filter id="pglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="12" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
          <filter id="herofx" x="-40%" y="-40%" width="180%" height="180%" colorInterpolationFilters="sRGB">
            <feGaussianBlur in="SourceAlpha" stdDeviation="26" result="ob" />
            <feFlood floodColor={warm} floodOpacity="0.75" /><feComposite in2="ob" operator="in" result="glow" />
            <feOffset in="SourceAlpha" dx="14" dy="10" result="o1" /><feComposite in="SourceAlpha" in2="o1" operator="out" result="e1" />
            <feGaussianBlur in="e1" stdDeviation="3" result="e1b" /><feFlood floodColor={warm} /><feComposite in2="e1b" operator="in" result="rimW" />
            <feOffset in="SourceAlpha" dx="-14" dy="-6" result="o2" /><feComposite in="SourceAlpha" in2="o2" operator="out" result="e2" />
            <feGaussianBlur in="e2" stdDeviation="3" result="e2b" /><feFlood floodColor={cool} /><feComposite in2="e2b" operator="in" result="rimC" />
            <feMerge><feMergeNode in="glow" /><feMergeNode in="SourceGraphic" /><feMergeNode in="rimW" /><feMergeNode in="rimC" /></feMerge>
          </filter>
          <filter id="scenefx" x="0" y="0" width={W} height={H} filterUnits="userSpaceOnUse" colorInterpolationFilters="sRGB">
            <feColorMatrix type="saturate" values={String(p.saturate ?? 1.3)} result="s" />
            <feComponentTransfer in="s" result="hi"><feFuncR type="linear" slope="2.2" intercept="-1.25" /><feFuncG type="linear" slope="2.2" intercept="-1.25" /><feFuncB type="linear" slope="2.2" intercept="-1.25" /></feComponentTransfer>
            <feGaussianBlur in="hi" stdDeviation="20" result="bl" />
            <feComponentTransfer in="bl" result="bl2"><feFuncA type="linear" slope={String(p.bloom ?? 0.9)} /></feComponentTransfer>
            <feBlend in="s" in2="bl2" mode="screen" />
          </filter>
          <radialGradient id="plight" cx="50%" cy="50%" r="50%"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.9} /><stop offset="0.18" stopColor={lc} stopOpacity={0.8} />
            <stop offset="0.6" stopColor={lc} stopOpacity={0.22} /><stop offset="1" stopColor={lc} stopOpacity={0} /></radialGradient>
          <linearGradient id="pscrim" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#000" stopOpacity={p.scrim ?? 0.5} /><stop offset="0.55" stopColor="#000" stopOpacity={0} /></linearGradient>
          <radialGradient id="pvig" cx="55%" cy="50%" r="75%"><stop offset="0.55" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.6} /></radialGradient>
        </defs>
        <g filter="url(#scenefx)">
          <Backdrop p={p} />
          <rect width={W} height={H} fill="url(#pscrim)" />
          <g style={{mixBlendMode: 'screen'}}>
            <ellipse cx={lx} cy={ly} rx={lr} ry={lr * 0.85} fill="url(#plight)" />
            {p.light?.rays !== false && Array.from({length: 18}, (_, k) => { const a0 = (k / 18) * Math.PI * 2 + 0.1, a1 = a0 + 0.06, R = lr * 1.9;
              return <path key={k} d={`M ${lx} ${ly} L ${lx + Math.cos(a0) * R} ${ly + Math.sin(a0) * R} L ${lx + Math.cos(a1) * R} ${ly + Math.sin(a1) * R} Z`} fill={lc} opacity={0.16} filter="url(#psoft)" />; })}
          </g>
          {(p.support ?? []).map((o, i) => <HeroNode key={'s' + i} o={o} i={i + 10} fx />)}
          {(p.flows ?? []).filter((f) => f.kind === 'energy' || !f.kind).map((f, i) => <Flow key={'fe' + i} f={f} i={i} />)}
          <HeroNode o={h} i={0} fx />
          {(p.front ?? []).map((o, i) => <HeroNode key={'f' + i} o={o} i={i + 30} fx />)}
          {(p.flows ?? []).filter((f) => f.kind === 'cash' || f.kind === 'coins').map((f, i) => <Flow key={'fc' + i} f={f} i={i + 5} />)}
          {(p.bolts ?? []).map((b, i) => { const d = boltPath(b.x1, b.y1, b.x2, b.y2, b.seed ?? i * 17);
            return <g key={'b' + i}><path d={d} stroke={b.color ?? '#7FE0FF'} strokeWidth={(b.w ?? 10) * 3} fill="none" opacity={0.6} filter="url(#pglow)" strokeLinejoin="round" />
              <path d={d} stroke="#FFFFFF" strokeWidth={b.w ?? 10} fill="none" strokeLinejoin="round" /></g>; })}
          {(p.sparks ?? []).map((s, i) => { const n = s.n ?? 26, L = s.len ?? 160, c = s.color ?? '#FFD27A';
            return <g key={'sp' + i}>
              <circle cx={s.x} cy={s.y} r={L * 0.35} fill={c} opacity={0.7} filter="url(#psoft)" /><circle cx={s.x} cy={s.y} r={L * 0.1} fill="#FFFFFF" />
              {Array.from({length: n}, (_, k) => { const a = ((s.angle ?? -90) + (rnd(i * 70 + k) - 0.5) * (s.spread ?? 220)) * Math.PI / 180, l = L * (0.3 + rnd(k + i * 3) * 0.9), r0 = L * 0.08;
                return <path key={k} d={`M ${s.x + Math.cos(a) * r0} ${s.y + Math.sin(a) * r0} L ${s.x + Math.cos(a) * l} ${s.y + Math.sin(a) * l}`} stroke={k % 3 ? c : '#FFFFFF'} strokeWidth={2 + rnd(k) * 4} strokeLinecap="round" />; })}
              {Array.from({length: Math.round(n / 2)}, (_, k) => { const a = rnd(k * 7 + i) * Math.PI * 2, l = L * (0.6 + rnd(k + 2) * 1.2);
                return <circle key={'d' + k} cx={s.x + Math.cos(a) * l} cy={s.y + Math.sin(a) * l} r={2 + rnd(k + 9) * 4} fill={c} />; })}
            </g>; })}
          {p.particles && Array.from({length: p.particles.n}, (_, k) => { const [x0, y0, x1, y1] = p.particles!.region ?? [900, 0, W, H], r = (p.particles!.size ?? 4) * (0.4 + rnd(k + 9) * 1.4);
            return <circle key={'pt' + k} cx={x0 + rnd(k + 1) * (x1 - x0)} cy={y0 + rnd(k + 4) * (y1 - y0)} r={r} fill={p.particles!.color ?? '#FFE3A0'} opacity={0.35 + 0.6 * rnd(k + 5)}
              filter={r > 6 ? 'url(#psoft)' : undefined} />; })}
          <rect width={W} height={H} fill="url(#pvig)" />
        </g>
        {!p.hideText && p.text.map((t, i) => <PLine key={i} t={t} i={i} />)}
      </svg>
    </AbsoluteFill>
  );
};
