import React from 'react';
import {E, clamp, ease, lerp, win} from '../motion';
import {ToneFilterDef, ToneOverlay, ToneShift, isNeutral, toneAt} from '../tone';

/**
 * CartoonStage: land-based cartoon WORLDS built for a specific story (flat colours, thick outlines, bouncy motion).
 *
 * Unlike CartoonOcean (one sea for every story), a stage is assembled from topic-specific SETS laid side by side
 * across the world (`zones`), e.g. a Bavarian city street, a stock-exchange floor, a newsroom, a bank vault, a
 * tropical business district, a courtroom, a night airport, an auditor's office. ITEMS are placed on top: glass
 * towers that grow or crumble, a split-flap stock board whose rows swap, line charts that climb or crash, generic
 * cartoon people (never a real person: no likeness, names only appear in callouts), a watchdog, newspapers that
 * spin in, a printing press, document stacks with a stamp slam, coins, a vault door that swings open onto empty
 * shelves, a piggy bank that cracks open empty, a calendar that flips, a gavel, a contract nobody signs.
 * A CAMERA pans and zooms across the world. All times in seconds; a pure function of t.
 */
type Key = {at: number; x?: number; y?: number; zoom?: number; dur?: number};
type KF = number | [number, number][];
export type StageZone = {set: string; x0: number; x1: number; night?: boolean; label?: string};
export type StageItem = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; flip?: boolean;
  text?: string; sub?: string; color?: string; [k: string]: any};
export type StageCallout = {text: string; sub?: string; x: number; y: number; at: number; until?: number; color?: string;
  tail?: [number, number]; size?: number; screen?: boolean};
export type CartoonStageProps = {
  t: number; W?: number; H?: number; world?: string; zones?: StageZone[]; worldW?: number; floor?: number;
  cam?: Key[]; drift?: number; shake?: {at: number; dur?: number; amp?: number}[]; night?: boolean;
  items?: StageItem[]; callouts?: StageCallout[]; banner?: {text: string; sub?: string; at?: number};
  /** adaptive visual tone (see ../tone.tsx); default 'bright' = original look */
  tone?: string; toneShift?: ToneShift; spot?: [number, number];
};

export const OL = '#10213A';
const K = {sky1: '#7FD3F7', sky2: '#D8F4FF', sun: '#FFD54A', white: '#FFFFFF', cream: '#FFF5E1', gold: '#FFC93C', red: '#FF5A5F',
  green: '#3DBE6B', green2: '#7BD389', blue: '#2F6FD1', blue2: '#4FB3F6', purple: '#7E57C2', orange: '#F28C28', grey: '#8C8FA3',
  road: '#5B6577', wood: '#B8763E', wood2: '#8A5428', stone: '#9AA3B5', glass: '#9FE3FF', skin: ['#F6C9A0', '#D9A066', '#A86B3C', '#F2D3B3']};
const COL: Record<string, string> = {purple: K.purple, gold: K.gold, blue: K.blue, green: K.green, red: K.red, risk: K.red, white: K.white,
  grey: K.grey, orange: K.orange, teal: '#26A69A', pink: '#F06292', navy: '#28407A', cyan: K.blue2};
const col = (c?: string, d = K.blue) => (c ? COL[c] || c : d);
const FONT = 'Inter, sans-serif';
const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
export const kf = (v: KF | undefined, t: number, d = 0): number => {
  if (v === undefined) return d;
  if (!Array.isArray(v)) return v;
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], v[i][0] - v[i - 1][0])));
  return v[v.length - 1][1];
};
const pop = (t: number, at = 0, d = 0.5) => (t < at ? 0 : E.outBack(win(t, at, d)));
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o}>{children}</text>;

/* =============================================================================================== SETS (backdrops) */
type SetFn = (t: number, z: StageZone, f: number) => React.ReactNode;

const house = (x: number, f: number, w: number, h: number, c: string, roof: string, k: number, lit = false) => <g key={'h' + k}>
  <rect x={x} y={f - h} width={w} height={h} fill={c} stroke={OL} strokeWidth={4} />
  {/* stepped Bavarian gable */}
  <path d={`M ${x - 6} ${f - h} L ${x + w * 0.2} ${f - h} L ${x + w * 0.2} ${f - h - 22} L ${x + w * 0.35} ${f - h - 22} L ${x + w * 0.35} ${f - h - 44}
    L ${x + w * 0.65} ${f - h - 44} L ${x + w * 0.65} ${f - h - 22} L ${x + w * 0.8} ${f - h - 22} L ${x + w * 0.8} ${f - h} L ${x + w + 6} ${f - h} Z`}
    fill={roof} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
  {Array.from({length: Math.floor(h / 70)}, (_, r) => Array.from({length: Math.max(1, Math.floor(w / 46))}, (_, c2) =>
    <rect key={r + '-' + c2} x={x + 14 + c2 * 46} y={f - h + 22 + r * 70} width={22} height={32} rx={3}
      fill={lit && rnd(k * 31 + r * 7 + c2) > 0.4 ? '#FFE08A' : '#CFEFFF'} stroke={OL} strokeWidth={2.5} />))}
</g>;

const SETS: Record<string, SetFn> = {
  /** A Bavarian city: Alps, gabled houses, a twin-domed church, a tram on the street. */
  city: (t, z, f) => {
    const w = z.x1 - z.x0, n = Math.ceil(w / 180), night = !!z.night;
    const tramX = z.x0 + ((t * 140) % (w + 900)) - 450;
    return <g>
      <path d={`M ${z.x0} ${f - 330} ${Array.from({length: Math.ceil(w / 160) + 1}, (_, k) => `L ${z.x0 + k * 160 + 80} ${f - 430 - 90 * rnd(k + 3)} L ${z.x0 + k * 160 + 160} ${f - 340}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`}
        fill={night ? '#5A6A9A' : '#B9C7E8'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {Array.from({length: Math.ceil(w / 160) + 1}, (_, k) => { const px = z.x0 + k * 160 + 80, py = f - 430 - 90 * rnd(k + 3);
        return <path key={'sn' + k} d={`M ${px - 30} ${py + 34} L ${px} ${py} L ${px + 30} ${py + 34} L ${px + 12} ${py + 26} L ${px} ${py + 38} L ${px - 12} ${py + 26} Z`} fill={K.white} stroke={OL} strokeWidth={3} strokeLinejoin="round" />; })}
      {/* church with two onion domes (generic Bavarian silhouette) */}
      {z.label !== 'nochurch' && <g transform={`translate(${z.x0 + w * 0.5} ${f})`}>
        {[-55, 55].map((dx) => <g key={dx}><rect x={dx - 32} y={-330} width={64} height={330} fill="#C98A5A" stroke={OL} strokeWidth={4} />
          <path d={`M ${dx - 36} -330 Q ${dx - 46} -380 ${dx} -400 Q ${dx + 46} -380 ${dx + 36} -330 Z`} fill="#4CAF7A" stroke={OL} strokeWidth={4} />
          <path d={`M ${dx} -400 L ${dx} -428`} stroke={OL} strokeWidth={4} />
          <rect x={dx - 12} y={-290} width={24} height={40} rx={10} fill={night ? '#FFE08A' : '#CFEFFF'} stroke={OL} strokeWidth={3} /></g>)}
        <path d="M -120 -150 L 0 -240 L 120 -150 Z" fill="#B0623A" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <rect x={-110} y={-150} width={220} height={150} fill="#D9A06C" stroke={OL} strokeWidth={4} />
        <path d="M -24 0 L -24 -70 Q 0 -100 24 -70 L 24 0 Z" fill={K.wood2} stroke={OL} strokeWidth={4} /></g>}
      {Array.from({length: n}, (_, k) => { const x = z.x0 + k * 180 + 10; if (z.label !== 'nochurch' && Math.abs(x + 75 - (z.x0 + w * 0.5)) < 190) return null;
        return house(x, f, 150, 170 + 90 * rnd(k), ['#FFE0B2', '#FFCDD2', '#C8E6C9', '#FFF59D', '#D1C4E9', '#B3E5FC'][k % 6], ['#C0504D', '#8D5A3B', '#C0504D'][k % 3], k, night); })}
      <rect x={z.x0} y={f} width={w} height={40} fill="#D8D2C4" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 40} width={w} height={400} fill={K.road} />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ld' + k} x={z.x0 + k * 120} y={f + 120} width={60} height={8} fill={K.white} opacity={0.7} />)}
      <g transform={`translate(${tramX} ${f + 34})`}>
        <rect x={-150} y={-90} width={300} height={86} rx={22} fill="#2F7FD8" stroke={OL} strokeWidth={4} />
        <rect x={-150} y={-40} width={300} height={16} fill={K.white} stroke={OL} strokeWidth={3} />
        {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-130 + i * 54} y={-78} width={40} height={30} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={3} />)}
        <path d="M 0 -90 L -20 -130 L 30 -130" fill="none" stroke={OL} strokeWidth={3} />
        {[-90, 90].map((dx) => <circle key={dx} cx={dx} cy={2} r={12} fill="#333" stroke={OL} strokeWidth={3} />)}
      </g>
    </g>;
  },
  /** Stock-exchange trading floor: panelled wall, ceiling lamps, rows of desks with blinking screens. */
  exchange: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#E3E9F4" />
      <rect x={z.x0} y={f - 140} width={w} height={140} fill="#C8D3E6" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <g key={'lamp' + k} transform={`translate(${z.x0 + 130 + k * 260} 0)`}>
        <path d="M 0 -400 L 0 40" stroke={OL} strokeWidth={3} />
        <path d="M -44 40 L 44 40 L 26 10 L -26 10 Z" fill={K.gold} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <path d="M -40 44 L -120 200 L 120 200 L 40 44 Z" fill="#FFF7C2" opacity={0.25} /></g>)}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => { const x = z.x0 + 60 + k * 300;
        return <g key={'desk' + k}>
          {[0, 1].map((m) => { const up = Math.sin(t * 2 + k * 2 + m) > 0;
            return <g key={m} transform={`translate(${x + m * 110} ${f - 200})`}>
              <rect x={0} y={0} width={96} height={64} rx={6} fill="#1E2A44" stroke={OL} strokeWidth={4} />
              <path d={`M 8 ${up ? 50 : 18} L 30 ${up ? 40 : 26} L 52 ${up ? 34 : 36} L 72 ${up ? 22 : 44} L 88 ${up ? 14 : 52}`} fill="none" stroke={up ? '#7DF29A' : '#FF7B7B'} strokeWidth={4} />
              <rect x={42} y={64} width={12} height={22} fill={OL} /></g>; })}
          <rect x={x - 20} y={f - 116} width={250} height={26} rx={6} fill={K.wood} stroke={OL} strokeWidth={4} />
          <rect x={x} y={f - 90} width={16} height={90} fill={K.wood2} /><rect x={x + 194} y={f - 90} width={16} height={90} fill={K.wood2} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#A9B4C8" />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <rect key={'tile' + k} x={z.x0 + k * 80} y={f} width={40} height={600} fill={K.white} opacity={0.12} />)}
    </g>;
  },
  /** Newspaper newsroom: windows on the city, a wall clock, desks with computers and paper piles. */
  newsroom: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#F3E9D7" />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 80 + k * 420;
        return <g key={'win' + k}><rect x={x} y={f - 560} width={260} height={300} rx={8} fill="#BFE8FA" stroke={OL} strokeWidth={5} />
          {[0, 1, 2, 3].map((b) => <rect key={b} x={x + 20 + b * 60} y={f - 260 - 80 - 120 * rnd(k * 4 + b)} width={44} height={80 + 120 * rnd(k * 4 + b)} fill="#9FB3CF" stroke={OL} strokeWidth={2} />)}
          <path d={`M ${x + 130} ${f - 560} L ${x + 130} ${f - 260} M ${x} ${f - 410} L ${x + 260} ${f - 410}`} stroke={OL} strokeWidth={5} /></g>; })}
      <g transform={`translate(${z.x0 + w * 0.5} ${f - 640})`}>
        <circle r={56} fill={K.white} stroke={OL} strokeWidth={6} />
        <path d={`M 0 0 L ${36 * Math.sin(t * 0.5)} ${-36 * Math.cos(t * 0.5)}`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
        <path d={`M 0 0 L ${46 * Math.sin(t * 6)} ${-46 * Math.cos(t * 6)}`} stroke={K.red} strokeWidth={3} strokeLinecap="round" /></g>
      <rect x={z.x0} y={f - 70} width={w} height={70} fill="#E2D2B5" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#8D6E63" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <rect key={'pl' + k} x={z.x0 + k * 60} y={f} width={4} height={600} fill={OL} opacity={0.15} />)}
    </g>;
  },
  /** Bank vault basement: stone wall, a swinging lamp, a tiled floor. The vault door itself is an item. */
  vault: (t, z, f) => {
    const w = z.x1 - z.x0, sw = Math.sin(t * 1.4) * 10;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#59627A" />
      {Array.from({length: 14}, (_, r) => Array.from({length: Math.ceil(w / 120) + 1}, (_, c2) =>
        <rect key={r + '-' + c2} x={z.x0 + c2 * 120 - (r % 2) * 60} y={f - 60 - r * 60} width={116} height={56} rx={6} fill={rnd(r * 13 + c2) > 0.5 ? '#6B7590' : '#646E88'} stroke="#3E4660" strokeWidth={3} />))}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => <g key={'lamp' + k} transform={`translate(${z.x0 + 350 + k * 700} 0) rotate(${sw})`}>
        <path d="M 0 -600 L 0 120" stroke={OL} strokeWidth={4} />
        <path d="M -40 120 L 40 120 L 26 96 L -26 96 Z" fill={K.gold} stroke={OL} strokeWidth={4} />
        <path d="M -36 124 L -200 520 L 200 520 L 36 124 Z" fill="#FFF3B0" opacity={0.18} /></g>)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#3E4660" />
      {Array.from({length: Math.ceil(w / 100)}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 100} ${f} L ${z.x0 + k * 100 - 60} ${f + 600}`} stroke="#2E354C" strokeWidth={4} />)}
    </g>;
  },
  /** Tropical business district: a bay, glass towers, palm trees, a colourful minibus on the road. */
  tropic: (t, z, f) => {
    const w = z.x1 - z.x0, busX = z.x1 - ((t * 120) % (w + 800)) + 400;
    return <g>
      <rect x={z.x0} y={f - 260} width={w} height={260} fill="#3FB6D9" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 60} ${f - 200 + 40 * rnd(k)} q 15 -8 30 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.6} />)}
      {Array.from({length: Math.ceil(w / 150)}, (_, k) => { const x = z.x0 + 20 + k * 150, h = 300 + 280 * rnd(k + 40), c = ['#7FC8F8', '#A5D8FF', '#8FD3C7', '#B3C6F7'][k % 4];
        return <g key={'tw' + k}><rect x={x} y={f - h} width={110} height={h} fill={c} stroke={OL} strokeWidth={4} />
          {Array.from({length: Math.floor(h / 40)}, (_, r) => <rect key={r} x={x + 10} y={f - h + 14 + r * 40} width={90} height={14} fill={z.night ? (rnd(k * 9 + r) > 0.5 ? '#FFE08A' : '#3A4A70') : K.white} opacity={0.75} />)}
          {k % 3 === 1 && <path d={`M ${x + 55} ${f - h} L ${x + 55} ${f - h - 50}`} stroke={OL} strokeWidth={4} />}</g>; })}
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => { const x = z.x0 + 160 + k * 340, sw = Math.sin(t * 1.5 + k) * 8;
        return <g key={'palm' + k} transform={`translate(${x} ${f})`}>
          <path d={`M 0 0 Q ${-10 + sw * 0.3} -90 ${sw} -190`} fill="none" stroke="#8A5A2B" strokeWidth={14} strokeLinecap="round" />
          {[-150, -100, -40, 20, 70].map((a, i) => <path key={i} d={`M ${sw} -190 q ${Math.cos(a * Math.PI / 180) * 60} ${Math.sin(a * Math.PI / 180) * 60 - 20} ${Math.cos(a * Math.PI / 180) * 110} ${Math.sin(a * Math.PI / 180) * 110 + 30}`}
            fill="none" stroke="#2E9E5B" strokeWidth={16} strokeLinecap="round" />)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={40} fill="#E9D9A6" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 40} width={w} height={400} fill={K.road} />
      <g transform={`translate(${busX} ${f + 30})`}>
        <path d="M -140 0 L -140 -80 Q -140 -96 -120 -96 L 100 -96 L 150 -50 L 150 0 Z" fill="#FFB300" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <rect x={-140} y={-40} width={290} height={12} fill="#E53935" />
        {[0, 1, 2, 3].map((i) => <rect key={i} x={-124 + i * 52} y={-84} width={40} height={30} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={3} />)}
        {[-90, 100].map((dx) => <circle key={dx} cx={dx} cy={2} r={13} fill="#333" stroke={OL} strokeWidth={3} />)}
      </g>
    </g>;
  },
  /** Courtroom: wood panelling, windows with light beams, the judge's bench, scales of justice on the wall. */
  court: (t, z, f) => {
    const w = z.x1 - z.x0, cx = (z as any).cx ?? z.x0 + w / 2;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#EADBC4" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <rect key={'pn' + k} x={z.x0 + k * 90} y={f - 300} width={86} height={300} fill={k % 2 ? '#B5793F' : '#A86C36'} stroke={OL} strokeWidth={2} />)}
      {[-560, 560].map((dx) => <g key={dx}><path d={`M ${cx + dx - 80} ${f - 760} L ${cx + dx - 80} ${f - 460} L ${cx + dx + 80} ${f - 460} L ${cx + dx + 80} ${f - 760} Q ${cx + dx} ${f - 860} ${cx + dx - 80} ${f - 760} Z`} fill="#CFEFFF" stroke={OL} strokeWidth={5} />
        <path d={`M ${cx + dx - 80} ${f - 460} L ${cx + dx - 240} ${f} L ${cx + dx + 160} ${f} L ${cx + dx + 80} ${f - 460} Z`} fill="#FFF8D6" opacity={0.25 + 0.05 * Math.sin(t)} /></g>)}
      <g transform={`translate(${cx} ${f - 690})`}>
        <path d="M 0 -60 L 0 60 M -70 -40 L 70 -40" stroke={K.gold} strokeWidth={8} strokeLinecap="round" />
        {[-70, 70].map((dx, i) => { const tilt = Math.sin(t * 0.9) * 10 * (i ? 1 : -1);
          return <g key={dx}><path d={`M ${dx} -40 L ${dx - 26} ${10 + tilt} M ${dx} -40 L ${dx + 26} ${10 + tilt}`} stroke={K.gold} strokeWidth={4} />
            <path d={`M ${dx - 36} ${10 + tilt} Q ${dx} ${44 + tilt} ${dx + 36} ${10 + tilt} Z`} fill={K.gold} stroke={OL} strokeWidth={4} /></g>; })}
        <path d="M -40 60 L 40 60" stroke={K.gold} strokeWidth={10} strokeLinecap="round" /></g>
      <rect x={cx - 380} y={f - 380} width={760} height={380} rx={10} fill="#8A5428" stroke={OL} strokeWidth={6} />
      <rect x={cx - 400} y={f - 400} width={800} height={40} rx={10} fill="#A86C36" stroke={OL} strokeWidth={5} />
      <rect x={cx - 120} y={f - 330} width={240} height={160} rx={8} fill="#A86C36" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#7A4A26" />
    </g>;
  },
  /** Night airport: runway lights, a control tower with a rotating beacon, a hangar. */
  airport: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={f - 40} width={w} height={40} fill="#3B4A6B" />
      <g transform={`translate(${z.x0 + 260} ${f - 40})`}>
        <rect x={-30} y={-300} width={60} height={300} fill="#6B7CA8" stroke={OL} strokeWidth={4} />
        <path d="M -80 -300 L 80 -300 L 60 -380 L -60 -380 Z" fill="#9FE3FF" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <path d="M -70 -380 L 70 -380 L 0 -420 Z" fill="#6B7CA8" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <path d={`M 0 -420 L ${600 * Math.cos(t * 2)} ${-420 - 120 * Math.abs(Math.sin(t * 2))} L ${600 * Math.cos(t * 2 + 0.15)} ${-420 - 120 * Math.abs(Math.sin(t * 2 + 0.15))} Z`} fill="#FFF3B0" opacity={0.25} /></g>
      <path d={`M ${z.x0 + 520} ${f - 40} L ${z.x0 + 520} ${f - 200} Q ${z.x0 + 720} ${f - 320} ${z.x0 + 920} ${f - 200} L ${z.x0 + 920} ${f - 40} Z`} fill="#4E5F87" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#2C3550" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <circle key={'rl' + k} cx={z.x0 + k * 90} cy={f + 60} r={7} fill={Math.sin(t * 5 - k * 0.6) > 0.3 ? '#FFE08A' : '#7A6A3A'} />)}
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'rw' + k} x={z.x0 + k * 160} y={f + 150} width={90} height={10} fill={K.white} opacity={0.7} />)}
    </g>;
  },
  /** Auditor's office: wallpaper, a window, filing cabinets, a big desk lamp. */
  office: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#DCEBDD" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 60} y={-2000} width={24} height={2000 + f} fill={K.white} opacity={0.25} />)}
      {Array.from({length: Math.ceil(w / 640)}, (_, k) => { const x = z.x0 + 100 + k * 640;
        return <g key={'fc' + k}>
          <rect x={x} y={f - 260} width={130} height={260} rx={6} fill="#9AA7B8" stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((d) => <g key={d}><rect x={x + 12} y={f - 246 + d * 84} width={106} height={72} rx={4} fill="#B7C3D3" stroke={OL} strokeWidth={3} />
            <rect x={x + 50} y={f - 216 + d * 84} width={30} height={10} rx={4} fill={OL} /></g>)}
          <rect x={x + 260} y={f - 600} width={240} height={200} rx={8} fill="#BFE8FA" stroke={OL} strokeWidth={5} />
          <path d={`M ${x + 380} ${f - 600} L ${x + 380} ${f - 400}`} stroke={OL} strokeWidth={5} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#7C8A6E" />
    </g>;
  },
  /** Semiconductor clean room: pale walls, an overhead rail, tool rows with signal towers, perforated floor; label 'yellow' tints a lithography bay. */
  fab: (t, z, f) => {
    const w = z.x1 - z.x0, yel = z.label === 'yellow';
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={yel ? '#FFF4C9' : '#EEF4FB'} />
      {Array.from({length: Math.ceil(w / 220)}, (_, k) => <rect key={'pnl' + k} x={z.x0 + k * 220} y={-2000} width={6} height={2000 + f} fill={OL} opacity={0.08} />)}
      <rect x={z.x0} y={70} width={w} height={22} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'hg' + k} x={z.x0 + 140 + k * 300} y={-400} width={10} height={470} fill="#90A4AE" />)}
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => { const x = z.x0 + 60 + k * 340, st = Math.floor(t * 0.7 + k) % 5;
        return <g key={'tool' + k}>
          <rect x={x} y={f - 330} width={250} height={330} rx={14} fill={k % 2 ? '#DDE6F0' : '#E8EEF5'} stroke={OL} strokeWidth={4} />
          <rect x={x + 24} y={f - 300} width={110} height={70} rx={8} fill="#1E2A44" stroke={OL} strokeWidth={3} />
          <path d={`M ${x + 34} ${f - 250} L ${x + 60} ${f - 270} L ${x + 86} ${f - 260} L ${x + 120} ${f - 286}`} fill="none" stroke="#7DF29A" strokeWidth={3} />
          <rect x={x + 24} y={f - 200} width={200} height={14} rx={7} fill="#B0BEC5" />
          <rect x={x + 214} y={f - 400} width={16} height={70} fill="#90A4AE" stroke={OL} strokeWidth={2} />
          {['#E53935', '#FFC93C', '#3DBE6B'].map((c, j) => <rect key={j} x={x + 208} y={f - 440 + j * 16} width={28} height={16} fill={(st === 0 && j === 1) || (st > 1 && j === 2) ? c : '#5C6B7A'} stroke={OL} strokeWidth={2} />)}
        </g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#CFD8DC" />
      {Array.from({length: Math.ceil(w / 40)}, (_, k) => Array.from({length: 6}, (_, r) => <circle key={k + '-' + r} cx={z.x0 + 20 + k * 40} cy={f + 20 + r * 34} r={4} fill="#90A4AE" />))}
    </g>;
  },
  /** Science park: lush rounded mountains, big white fab buildings with exhaust stacks, scooters zipping along the road. */
  sciencepark: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <path d={`M ${z.x0} ${f - 220} ${Array.from({length: Math.ceil(w / 300) + 1}, (_, k) => `Q ${z.x0 + k * 300 + 150} ${f - 470 - 120 * rnd(k + 11)} ${z.x0 + k * 300 + 300} ${f - 230}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`}
        fill={night ? '#2E5B4A' : '#4FAF6A'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <circle key={'tr' + k} cx={z.x0 + k * 120 + 40 * rnd(k)} cy={f - 240 - 60 * rnd(k + 2)} r={30} fill={night ? '#24493B' : '#3E9A57'} stroke={OL} strokeWidth={3} />)}
      {Array.from({length: Math.ceil(w / 760)}, (_, k) => { const x = z.x0 + 120 + k * 760;
        return <g key={'fb' + k}>
          {[0, 1].map((j) => { const u = ((t * 0.25 + j * 0.5 + k * 0.3) % 1);
            return <circle key={j} cx={x + 470 + j * 70 + 20 * u} cy={f - 330 - 160 * u} r={24 + 30 * u} fill={K.white} opacity={0.8 * (1 - u)} />; })}
          {[0, 1].map((j) => <rect key={'sk' + j} x={x + 450 + j * 70} y={f - 330} width={36} height={110} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}
          <rect x={x} y={f - 230} width={560} height={230} rx={10} fill="#F4F7FB" stroke={OL} strokeWidth={5} />
          <rect x={x} y={f - 200} width={560} height={22} fill="#1E7FD8" />
          {Array.from({length: 7}, (_, c2) => <rect key={c2} x={x + 30 + c2 * 74} y={f - 150} width={50} height={36} rx={4} fill={night ? '#FFE08A' : '#CFEFFF'} stroke={OL} strokeWidth={3} />)}
        </g>; })}
      <rect x={z.x0} y={f} width={w} height={40} fill="#D8D2C4" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 40} width={w} height={400} fill={K.road} />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ld' + k} x={z.x0 + k * 120} y={f + 130} width={60} height={8} fill={K.white} opacity={0.7} />)}
      {Array.from({length: 9}, (_, k) => { const dir = k % 2 ? -1 : 1, sp = 180 + 90 * rnd(k), span = w + 400;
        const x = dir > 0 ? z.x0 - 200 + ((t * sp + rnd(k + 3) * span) % span) : z.x1 + 200 - ((t * sp + rnd(k + 3) * span) % span), y = f + 80 + (k % 3) * 34;
        return <g key={'sc' + k} transform={`translate(${x} ${y}) scale(${dir * 0.8} 0.8)`}>
          <path d="M -40 0 L 30 0 L 44 -30 L 20 -30 L 10 -10 L -30 -10 Z" fill={['#FF8A65', '#4FB3F6', '#FFC93C', '#7BD389', '#F06292'][k % 5]} stroke={OL} strokeWidth={3} strokeLinejoin="round" />
          <circle cx={-30} cy={4} r={11} fill="#333" stroke={OL} strokeWidth={2} /><circle cx={34} cy={4} r={11} fill="#333" stroke={OL} strokeWidth={2} />
          <path d="M -6 -12 L -2 -50" stroke={K.skin[k % 4]} strokeWidth={9} strokeLinecap="round" />
          <circle cx={-2} cy={-62} r={14} fill={['#E53935', '#FFFFFF', '#1E7FD8'][k % 3]} stroke={OL} strokeWidth={3} />
          <path d="M 4 -36 L 40 -32" stroke={K.skin[k % 4]} strokeWidth={7} strokeLinecap="round" /></g>; })}
    </g>;
  },
  /** Electronics shop: wall shelves of generic boxes with price tags, a neon sign, a glass counter, ceiling lights. */
  shop: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2A2F45' : '#EDE7F6'} />
      <rect x={z.x0} y={f - 640} width={w} height={20} fill="#B39DDB" opacity={0.5} />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 40 + k * 420;
        return <g key={'sh' + k}>
          {[0, 1, 2].map((r) => <g key={r}>
            <rect x={x} y={f - 560 + r * 150} width={360} height={14} fill={K.wood} stroke={OL} strokeWidth={3} />
            {[0, 1, 2, 3].map((b) => { const bw = 70, bh = 80 + ((k + r + b) % 3) * 14, c = ['#4FB3F6', '#FFC93C', '#7BD389', '#F06292', '#9575CD', '#FF8A65'][(k * 3 + r * 2 + b) % 6];
              return <g key={b}><rect x={x + 14 + b * 86} y={f - 560 + r * 150 - bh} width={bw} height={bh} rx={4} fill={c} stroke={OL} strokeWidth={3} />
                <rect x={x + 24 + b * 86} y={f - 560 + r * 150 - bh + 12} width={50} height={14} rx={3} fill={K.white} opacity={0.8} /></g>; })}
            <rect x={x + 150} y={f - 560 + r * 150 + 16} width={60} height={24} rx={4} fill={K.white} stroke={OL} strokeWidth={2} />
          </g>)}
        </g>; })}
      {(z as any).label !== 'none' && <g transform={`translate(${z.x0 + w / 2} ${f - 690})`}>
        <rect x={-260} y={-56} width={520} height={92} rx={18} fill="#1B2438" stroke={OL} strokeWidth={5} />
        <text x={0} y={10} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={52} fill={Math.sin(t * 3) > -0.8 ? '#FF4FD8' : '#7A2A6A'}>{(z as any).label || 'COMPUTERS'}</text></g>}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <g key={'lt' + k}><rect x={z.x0 + 100 + k * 300} y={f - 900} width={120} height={14} rx={7} fill="#FFF8E1" />
        <path d={`M ${z.x0 + 100 + k * 300} ${f - 886} L ${z.x0 + 60 + k * 300} ${f - 640} L ${z.x0 + 260 + k * 300} ${f - 640} L ${z.x0 + 220 + k * 300} ${f - 886} Z`} fill="#FFF8E1" opacity={night ? 0.08 : 0.18} /></g>)}
      <rect x={z.x0} y={f - 70} width={w} height={70} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3A3550' : '#D7CCC8'} />
      {Array.from({length: Math.ceil(w / 100)}, (_, k) => <rect key={'ft' + k} x={z.x0 + k * 100} y={f} width={4} height={600} fill={OL} opacity={0.08} />)}
    </g>;
  },
  /** A snowy winter city square (generic, no real landmark): pale sky, falling snow, tall stone blocks with lit windows,
   *  street lamps, snow on the ground. `night` for a dark blue evening. */
  wintersquare: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1C2A44' : '#C9D8E6'} />
      <rect x={z.x0} y={f - 520} width={w} height={520} fill={night ? '#26375A' : '#DCE6F0'} opacity={0.7} />
      {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const x = z.x0 + k * 360 + 20, h = 420 + ((k * 7) % 4) * 70, c = ['#C9A27E', '#B98A6A', '#D8C3A5', '#A9B4C2'][k % 4];
        return <g key={'wb' + k}>
          <rect x={x} y={f - h} width={300} height={h} fill={c} stroke={OL} strokeWidth={4} />
          <rect x={x - 8} y={f - h - 18} width={316} height={22} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
          {k % 3 === 1 && <path d={`M ${x + 120} ${f - h - 18} L ${x + 150} ${f - h - 120} L ${x + 180} ${f - h - 18} Z`} fill={c} stroke={OL} strokeWidth={4} />}
          {Array.from({length: Math.floor((h - 60) / 80)}, (_, r) => Array.from({length: 5}, (_, c2) =>
            <rect key={r + '-' + c2} x={x + 22 + c2 * 56} y={f - h + 30 + r * 80} width={30} height={44} rx={3}
              fill={night ? (rnd(k * 13 + r * 5 + c2) > 0.35 ? '#FFE08A' : '#33415E') : '#EAF4FF'} stroke={OL} strokeWidth={2.5} />))}
        </g>; })}
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 200 + k * 420;
        return <g key={'lp' + k}><rect x={x - 6} y={f - 300} width={12} height={300} fill="#2E3A4F" />
          <circle cx={x} cy={f - 310} r={22} fill={night ? '#FFE9A8' : '#F5F5F5'} stroke={OL} strokeWidth={3} />
          {night && <circle cx={x} cy={f - 310} r={70} fill="#FFE9A8" opacity={0.18} />}</g>; })}
      <rect x={z.x0} y={f - 18} width={w} height={600} fill={night ? '#B7C6DA' : '#F4F8FC'} />
      <path d={`M ${z.x0} ${f - 18} ${Array.from({length: Math.ceil(w / 80) + 1}, (_, k) => `Q ${z.x0 + k * 80 + 40} ${f - 34} ${z.x0 + k * 80 + 80} ${f - 18}`).join(' ')}`} fill="none" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 40)}, (_, k) => { const sx = z.x0 + rnd(k) * w + Math.sin(t * 0.8 + k) * 30, sp = 40 + rnd(k + 5) * 50;
        const sy = -400 + ((rnd(k + 9) * 1600 + t * sp) % (f + 400));
        return <circle key={'sn' + k} cx={sx} cy={sy} r={3 + rnd(k + 2) * 5} fill="#FFFFFF" opacity={0.85} />; })}
    </g>;
  },
  /** Potato fields under a big sky: furrowed brown rows with green plants, a barn, a few trees. */
  farm: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#BFE6FA" />
      <circle cx={z.x0 + w * 0.7} cy={f - 700} r={70} fill={K.sun} stroke={OL} strokeWidth={4} />
      <path d={`M ${z.x0} ${f - 160} Q ${z.x0 + w * 0.3} ${f - 260} ${z.x0 + w * 0.6} ${f - 170} T ${z.x1} ${f - 180} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#9CD67E" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + 300 + k * 900;
        return <g key={'bn' + k}><rect x={x} y={f - 330} width={220} height={160} fill="#C0504D" stroke={OL} strokeWidth={4} />
          <path d={`M ${x - 14} ${f - 330} L ${x + 110} ${f - 420} L ${x + 234} ${f - 330} Z`} fill="#8E3B38" stroke={OL} strokeWidth={4} />
          <rect x={x + 80} y={f - 260} width={60} height={90} fill="#F5E6C8" stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={z.x0} y={f - 140} width={w} height={740} fill="#8D6E4F" />
      {Array.from({length: 6}, (_, r) => <g key={'fr' + r}>
        <rect x={z.x0} y={f - 130 + r * 34} width={w} height={14} fill="#6D4C36" opacity={0.8} />
        {Array.from({length: Math.ceil(w / 90)}, (_, k) => { const x = z.x0 + 30 + k * 90 + (r % 2) * 45, y = f - 132 + r * 34, sw = Math.sin(t * 2 + k + r) * 3;
          return <path key={k} d={`M ${x} ${y} q ${-10 + sw} -18 -16 -26 M ${x} ${y} q ${sw} -22 0 -32 M ${x} ${y} q ${10 + sw} -18 16 -26`} stroke="#3E9B4F" strokeWidth={6} strokeLinecap="round" fill="none" />; })}
      </g>)}
    </g>;
  },
  /** An American suburb: sky, rolling hills, a row of gabled houses with lawns, picket fences and round trees behind a
   *  sidewalk and a quiet street. `night` lights the windows and darkens the sky. */
  suburb: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const roofs = ['#C0504D', '#5C6BC0', '#8D6E63', '#26A69A', '#EF6C00'], walls = ['#FFF3E0', '#E3F2FD', '#F1F8E9', '#FCE4EC', '#FFFDE7'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1A2346' : '#BFE6FA'} />
      {night ? <circle cx={z.x0 + w * 0.72} cy={f - 720} r={56} fill="#FFF8E1" stroke={OL} strokeWidth={4} />
        : <circle cx={z.x0 + w * 0.72} cy={f - 720} r={70} fill={K.sun} stroke={OL} strokeWidth={4} />}
      <path d={`M ${z.x0} ${f - 230} ${Array.from({length: Math.ceil(w / 500) + 1}, (_, k) => `Q ${z.x0 + k * 500 + 250} ${f - 330 - 50 * rnd(k + 2)} ${z.x0 + k * 500 + 500} ${f - 240}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`}
        fill={night ? '#2E4A3A' : '#A5D68A'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 330)}, (_, k) => { const x = z.x0 + 60 + k * 330, j = k % 5, hw = 210, hh = 150 + 30 * rnd(k + 7);
        return <g key={'sh' + k}>
          <circle cx={x + hw + 50} cy={f - 200} r={58} fill={night ? '#2F5D3A' : '#5DBB63'} stroke={OL} strokeWidth={4} />
          <rect x={x + hw + 44} y={f - 160} width={12} height={40} fill={K.wood2} />
          <rect x={x} y={f - 120 - hh} width={hw} height={hh} fill={walls[j]} stroke={OL} strokeWidth={4} />
          <path d={`M ${x - 18} ${f - 120 - hh} L ${x + hw / 2} ${f - 200 - hh} L ${x + hw + 18} ${f - 120 - hh} Z`} fill={roofs[j]} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          {[0, 1].map((q) => <rect key={q} x={x + 26 + q * 110} y={f - 100 - hh + 30} width={48} height={40} rx={3} fill={night ? (rnd(k * 3 + q) > 0.35 ? '#FFE082' : '#34405E') : K.glass} stroke={OL} strokeWidth={3} />)}
          <rect x={x + hw / 2 - 22} y={f - 186} width={44} height={66} fill={K.wood} stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={z.x0} y={f - 120} width={w} height={60} fill={night ? '#3B6B44' : '#7BCB6B'} />
      {Array.from({length: Math.ceil(w / 40)}, (_, k) => <rect key={'pf' + k} x={z.x0 + k * 40} y={f - 112} width={14} height={44} rx={5} fill={night ? '#B0BEC5' : K.white} stroke={OL} strokeWidth={2} />)}
      <rect x={z.x0} y={f - 96} width={w} height={8} fill={night ? '#B0BEC5' : K.white} stroke={OL} strokeWidth={2} />
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3E4656' : K.road} />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 200} y={f + 80} width={100} height={12} rx={6} fill="#FFD54A" />)}
    </g>;
  },
  /** A generic membership warehouse store inside: high corrugated ceiling with hanging lights, tall orange-and-blue
   *  steel pallet racks loaded with shrink-wrapped boxes up to the roof, polished concrete floor. `night` dims the lights. */
  warehouse: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, boxes = ['#C8A27A', '#D7B98E', '#B48A5E', '#E0C9A6', '#90CAF9', '#EF9A9A', '#A5D6A7'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#4A5266' : '#DDE3EA'} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <rect key={'cg' + k} x={z.x0 + k * 60} y={-2000} width={30} height={2000 + f - 820} fill={night ? '#3F4759' : '#CFD6DE'} />)}
      <rect x={z.x0} y={f - 830} width={w} height={14} fill="#90A4AE" stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 210 + k * 420;
        return <g key={'lt' + k}><path d={`M ${x} ${f - 816} L ${x} ${f - 780}`} stroke={OL} strokeWidth={3} />
          <path d={`M ${x - 50} ${f - 760} L ${x - 30} ${f - 780} L ${x + 30} ${f - 780} L ${x + 50} ${f - 760} Z`} fill="#ECEFF1" stroke={OL} strokeWidth={3} />
          <ellipse cx={x} cy={f - 756} rx={46} ry={8} fill={night ? '#FFE9A8' : '#FFFDE7'} opacity={0.9} /></g>; })}
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => { const x0 = z.x0 + 30 + k * 520;
        return <g key={'rk' + k}>
          {[0, 1, 2].map((r) => <g key={r}>
            {[0, 1, 2].map((b) => { const bx = x0 + 22 + b * 150, by = f - 140 - r * 170, c = boxes[(k * 7 + r * 3 + b) % boxes.length], hb = 100 + 20 * rnd(k * 11 + r * 3 + b);
              return <g key={b}><rect x={bx} y={by - hb} width={130} height={hb} rx={4} fill={c} stroke={OL} strokeWidth={3} />
                <path d={`M ${bx} ${by - hb / 2} L ${bx + 130} ${by - hb / 2}`} stroke="#FFFFFF" strokeWidth={4} opacity={0.4} />
                <rect x={bx + 4} y={by} width={122} height={12} fill="#A1887F" stroke={OL} strokeWidth={2} /></g>; })}
            <rect x={x0} y={f - 128 - r * 170} width={480} height={16} fill="#EF6C00" stroke={OL} strokeWidth={3} /></g>)}
          {[0, 480].map((dx) => <rect key={dx} x={x0 + dx - 8} y={f - 600} width={16} height={600} fill="#1565C0" stroke={OL} strokeWidth={3} />)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#6B7280' : '#B9C1C9'} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'fl' + k} x={z.x0 + k * 300} y={f + 4} width={4} height={600} fill="#9EA7B0" />)}
      <rect x={z.x0} y={f + 60} width={w} height={8} fill="#FFD54A" opacity={0.8} />
    </g>;
  },
  /** A generic American college quad: red-brick halls with white columns and a pediment, a central clock tower, a green lawn
   *  with diagonal paths and round trees. `night` lights the windows. No real campus. */
  campus: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1C2448' : '#BFE6FA'} />
      {Array.from({length: Math.ceil(w / 1100)}, (_, k) => { const x = z.x0 + 120 + k * 1100;
        return <g key={'hall' + k}>
          <rect x={x} y={f - 420} width={700} height={300} fill="#B5533C" stroke={OL} strokeWidth={4} />
          {Array.from({length: 4}, (_, r) => Array.from({length: 9}, (_, c) => <rect key={r + '-' + c} x={x + 30 + c * 74} y={f - 400 + r * 64} width={40} height={40} rx={4}
            fill={night ? (rnd(k * 50 + r * 9 + c) > 0.4 ? '#FFE082' : '#2B3352') : '#CFEFFF'} stroke={OL} strokeWidth={2} />))}
          <path d={`M ${x + 220} ${f - 420} L ${x + 350} ${f - 500} L ${x + 480} ${f - 420} Z`} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3, 4].map((c) => <rect key={c} x={x + 236 + c * 52} y={f - 420} width={20} height={300} fill="#FAFAFA" stroke={OL} strokeWidth={3} />)}
          <rect x={x + 900} y={f - 640} width={110} height={520} fill="#A84A35" stroke={OL} strokeWidth={4} />
          <path d={`M ${x + 885} ${f - 640} L ${x + 955} ${f - 760} L ${x + 1025} ${f - 640} Z`} fill="#546E7A" stroke={OL} strokeWidth={4} />
          <circle cx={x + 955} cy={f - 570} r={38} fill={K.cream} stroke={OL} strokeWidth={4} />
          <path d={`M ${x + 955} ${f - 570} L ${x + 955 + 26 * Math.sin(t * 0.5)} ${f - 570 - 26 * Math.cos(t * 0.5)} M ${x + 955} ${f - 570} L ${x + 955 + 16 * Math.sin(t * 0.04)} ${f - 570 - 16 * Math.cos(t * 0.04)}`} stroke={OL} strokeWidth={4} strokeLinecap="round" />
        </g>; })}
      <rect x={z.x0} y={f - 120} width={w} height={720} fill={night ? '#2F5D3A' : '#7BCB6B'} />
      {Array.from({length: Math.ceil(w / 600)}, (_, k) => { const x = z.x0 + k * 600;
        return <path key={'pt' + k} d={`M ${x} ${f + 600} L ${x + 300} ${f - 120} L ${x + 600} ${f + 600}`} fill="none" stroke={night ? '#8D8F7A' : '#E8DDB5'} strokeWidth={26} />; })}
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const x = z.x0 + 190 + k * 380;
        return <g key={'tr' + k}><rect x={x - 7} y={f - 150} width={14} height={50} fill={K.wood2} />
          <circle cx={x} cy={f - 190} r={52} fill={night ? '#2E5E39' : '#4CAF50'} stroke={OL} strokeWidth={4} /></g>; })}
    </g>;
  },
  /** A generic car dealership seen from the lot: a glass showroom with a flat canopy, a row of pennant strings, light
   *  poles and a paved lot with parking lines. `night` lights the showroom. No real brand. */
  dealership: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1A2346' : '#BFE6FA'} />
      {Array.from({length: Math.ceil(w / 1400)}, (_, k) => { const x = z.x0 + 200 + k * 1400;
        return <g key={'sr' + k}>
          <rect x={x} y={f - 420} width={900} height={330} fill={night ? '#FFE9A8' : '#D6EEF8'} stroke={OL} strokeWidth={5} />
          {Array.from({length: 7}, (_, c) => <rect key={c} x={x + c * 128} y={f - 420} width={10} height={330} fill="#90A4AE" />)}
          <rect x={x - 40} y={f - 470} width={980} height={56} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
          <rect x={x + 300} y={f - 462} width={380} height={40} rx={6} fill="#1565C0" stroke={OL} strokeWidth={3} />
          <T x={x + 490} y={f - 432} s={30} c="#FFFFFF">AUTO SALES</T>
          <rect x={x + 1000} y={f - 360} width={280} height={270} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
          {[0, 1, 2, 3, 4].map((r) => <rect key={r} x={x + 1020} y={f - 330 + r * 46} width={240} height={36} fill="#CFD8DC" stroke={OL} strokeWidth={2} />)}
          <rect x={x + 1000} y={f - 400} width={280} height={40} fill="#455A64" stroke={OL} strokeWidth={3} />
          <T x={x + 1140} y={f - 371} s={24} c="#FFFFFF">SERVICE</T></g>; })}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => { const x = z.x0 + 100 + k * 700;
        return <g key={'pn' + k}><rect x={x - 6} y={f - 620} width={12} height={530} fill="#90A4AE" />
          <path d={`M ${x} ${f - 600} Q ${x + 350} ${f - 520 + Math.sin(t * 2 + k) * 10} ${x + 700} ${f - 600}`} fill="none" stroke={OL} strokeWidth={2} />
          {Array.from({length: 10}, (_, j) => { const px = x + 35 + j * 66, py = f - 600 + 80 * Math.sin(Math.PI * (j + 0.5) / 10.6) * 0.9;
            return <path key={j} d={`M ${px - 14} ${py} L ${px + 14} ${py} L ${px} ${py + 30 + Math.sin(t * 6 + j) * 3} Z`} fill={['#E53935', '#FFC21A', '#1E88E5'][j % 3]} stroke={OL} strokeWidth={2} />; })}</g>; })}
      <rect x={z.x0} y={f - 90} width={w} height={690} fill={night ? '#3E4656' : '#78838F'} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <rect key={'pl' + k} x={z.x0 + k * 260} y={f - 80} width={8} height={120} fill="#FFFFFF" opacity={0.8} transform={`skewX(-20)`} />)}
    </g>;
  },
  /** A dealership service bay inside: two-post car lifts, a tool wall with pegboard, tire stacks, epoxy floor. */
  garage: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#4A5266' : '#E3E7EC'} />
      <rect x={z.x0} y={f - 700} width={w} height={14} fill="#90A4AE" />
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + 80 + k * 900;
        return <g key={'gb' + k}>
          <rect x={x} y={f - 560} width={360} height={260} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
          {Array.from({length: 8}, (_, r) => Array.from({length: 14}, (_, c) => <circle key={r + '-' + c} cx={x + 14 + c * 24} cy={f - 546 + r * 32} r={3} fill="#78909C" />))}
          {[0, 1, 2, 3].map((q) => <path key={q} d={`M ${x + 40 + q * 80} ${f - 520} l 0 70 m -10 -70 l 20 0`} stroke="#E53935" strokeWidth={8} strokeLinecap="round" />)}
          {[0, 1, 2].map((q) => <ellipse key={q} cx={x + 600} cy={f - 40 - q * 60} rx={70} ry={30} fill="#263238" stroke={OL} strokeWidth={4} />)}
          {[x + 420, x + 820].map((px) => <rect key={px} x={px - 12} y={f - 520} width={24} height={520} fill="#FFC21A" stroke={OL} strokeWidth={3} />)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#5B6577' : '#A7B0BA'} />
      <rect x={z.x0} y={f + 30} width={w} height={8} fill="#FFD54A" opacity={0.8} />
    </g>;
  },
  /** High-voltage country: rolling hills, a march of lattice transmission towers with sagging lines, a fenced substation
   *  with transformers, and wooden distribution poles along a road. `night` adds a dusk sky and glowing insulators. */
  powergrid: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const tower = (x: number, y: number, sc: number, k: number) => <g key={'tw' + k} transform={`translate(${x} ${y}) scale(${sc})`}>
      <path d="M -60 0 L -14 -300 L 14 -300 L 60 0 M -40 -100 L 40 -100 M -28 -190 L 28 -190 M -60 0 L 28 -190 M 60 0 L -28 -190 M -40 -100 L 14 -300 M 40 -100 L -14 -300" fill="none" stroke={night ? '#B0BEC5' : '#607D8B'} strokeWidth={6} />
      <path d="M -110 -250 L 110 -250 M -80 -300 L 80 -300" stroke={night ? '#B0BEC5' : '#607D8B'} strokeWidth={8} />
      {[-110, 110, -80, 80].map((dx, q) => <circle key={q} cx={dx} cy={q < 2 ? -244 : -294} r={6} fill={night ? '#FFE082' : '#ECEFF1'} />)}</g>;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#22284A' : '#BFE6FA'} />
      <path d={`M ${z.x0} ${f - 200} ${Array.from({length: Math.ceil(w / 600) + 1}, (_, k) => `Q ${z.x0 + k * 600 + 300} ${f - 300 - 50 * rnd(k + 4)} ${z.x0 + k * 600 + 600} ${f - 210}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#2E4A3A' : '#9CCC65'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => tower(z.x0 + 200 + k * 520, f - 210, 0.9, k))}
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => { const x = z.x0 + 200 + k * 520;
        return [[-99, -225], [99, -225], [-72, -270], [72, -270]].map(([dx, dy], q) => <path key={k + '-' + q} d={`M ${x + dx} ${f - 210 + dy} Q ${x + dx + 260} ${f - 210 + dy + 60} ${x + dx + 520} ${f - 210 + dy}`} fill="none" stroke={OL} strokeWidth={2} />); })}
      {Array.from({length: Math.ceil(w / 1600)}, (_, k) => { const x = z.x0 + 900 + k * 1600;
        return <g key={'ss' + k}><rect x={x} y={f - 170} width={360} height={170} fill={night ? '#3E4656' : '#CFD8DC'} stroke={OL} strokeWidth={3} />
          {Array.from({length: 13}, (_, c) => <path key={c} d={`M ${x + c * 30} ${f} L ${x + c * 30} ${f - 170}`} stroke="#90A4AE" strokeWidth={2} />)}
          {[0, 1, 2].map((q) => <g key={q}><rect x={x + 30 + q * 110} y={f - 130} width={80} height={110} rx={6} fill="#78909C" stroke={OL} strokeWidth={3} />
            {[0, 1, 2].map((j) => <rect key={j} x={x + 40 + q * 110 + j * 22} y={f - 160} width={10} height={30} fill="#ECEFF1" stroke={OL} strokeWidth={2} />)}</g>)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3E4656' : K.road} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => { const x = z.x0 + 150 + k * 300;
        return <g key={'wp' + k}><rect x={x - 7} y={f - 230} width={14} height={230} fill={K.wood2} stroke={OL} strokeWidth={2} />
          <rect x={x - 40} y={f - 222} width={80} height={10} fill={K.wood2} stroke={OL} strokeWidth={2} />
          <path d={`M ${x - 36} ${f - 216} Q ${x + 114} ${f - 180} ${x + 264} ${f - 216}`} fill="none" stroke={OL} strokeWidth={2} /></g>; })}
    </g>;
  },
  /** An American interstate: distant hills, a concrete overpass with pillars, green guide signs, a guardrail and a
   *  multi-lane road with dashed lines and moving headlights at `night`. */
  highway: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1A2040' : '#BFE6FA'} />
      <path d={`M ${z.x0} ${f - 260} ${Array.from({length: Math.ceil(w / 700) + 1}, (_, k) => `Q ${z.x0 + k * 700 + 350} ${f - 360 - 40 * rnd(k + 8)} ${z.x0 + k * 700 + 700} ${f - 270}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#2B3B4A' : '#A5D68A'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 1800)}, (_, k) => { const x = z.x0 + 600 + k * 1800;
        return <g key={'ov' + k}><rect x={x} y={f - 330} width={1100} height={60} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
          <rect x={x} y={f - 345} width={1100} height={18} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
          {[120, 540, 960].map((dx) => <rect key={dx} x={x + dx} y={f - 270} width={40} height={230} fill="#90A4AE" stroke={OL} strokeWidth={3} />)}
          <rect x={x + 380} y={f - 470} width={340} height={110} rx={10} fill="#2E7D32" stroke="#FFFFFF" strokeWidth={5} />
          <T x={x + 550} y={f - 425} s={34} c="#FFFFFF">INTERSTATE</T>
          <T x={x + 550} y={f - 385} s={24} c="#FFFFFF">EXIT 42 · 1 MILE</T>
          <rect x={x + 540} y={f - 360} width={14} height={20} fill="#90A4AE" /></g>; })}
      <rect x={z.x0} y={f - 40} width={w} height={640} fill={night ? '#3E4656' : K.road} />
      <rect x={z.x0} y={f - 60} width={w} height={14} fill="#CFD8DC" stroke={OL} strokeWidth={2} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'gp' + k} x={z.x0 + k * 160} y={f - 60} width={10} height={36} fill="#90A4AE" />)}
      {[60, 180].map((dy) => Array.from({length: Math.ceil(w / 220)}, (_, k) => <rect key={dy + '-' + k} x={z.x0 + ((k * 220 - t * 300) % w + w) % w} y={f + dy} width={110} height={10} fill="#FFFFFF" opacity={0.85} />))}
      {night && Array.from({length: 6}, (_, k) => { const x = z.x0 + ((k * 700 + t * 500) % w); return <g key={'hl' + k}><circle cx={x} cy={f + 120} r={8} fill="#FFF8E1" /><circle cx={x + 26} cy={f + 120} r={8} fill="#FFF8E1" /></g>; })}
    </g>;
  },
  /** A giant parcel sort center inside: steel roof trusses, a mezzanine of yellow conveyor lanes, cardboard boxes stacked
   *  on carts, numbered loading-dock doors along the back wall. Boxes ride the upper belt continuously. */
  sortcenter: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#3E4656' : '#D5DBE1'} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <path key={'tr' + k} d={`M ${z.x0 + k * 300} ${f - 820} L ${z.x0 + k * 300 + 150} ${f - 760} L ${z.x0 + k * 300 + 300} ${f - 820}`} fill="none" stroke="#90A4AE" strokeWidth={6} />)}
      <rect x={z.x0} y={f - 830} width={w} height={12} fill="#78909C" />
      {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const x = z.x0 + 40 + k * 360;
        return <g key={'dk' + k}><rect x={x} y={f - 420} width={260} height={300} fill="#90A4AE" stroke={OL} strokeWidth={4} />
          {Array.from({length: 7}, (_, r) => <rect key={r} x={x + 10} y={f - 410 + r * 42} width={240} height={34} fill="#B0BEC5" stroke={OL} strokeWidth={2} />)}
          <rect x={x + 90} y={f - 470} width={80} height={40} rx={6} fill="#263238" stroke={OL} strokeWidth={3} />
          <T x={x + 130} y={f - 441} s={26} c="#FFC21A">{String(101 + k)}</T></g>; })}
      <rect x={z.x0} y={f - 580} width={w} height={26} fill="#FFC21A" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 500)}, (_, k) => <rect key={'lg' + k} x={z.x0 + 200 + k * 500} y={f - 554} width={16} height={430} fill="#607D8B" />)}
      {Array.from({length: Math.ceil(w / 180)}, (_, k) => { const x = z.x0 + ((k * 180 + t * 160) % w + w) % w;
        return <g key={'bx' + k}><rect x={x} y={f - 640} width={70} height={60} rx={4} fill="#C8A27A" stroke={OL} strokeWidth={3} />
          <rect x={x + 28} y={f - 640} width={14} height={60} fill="#E0C9A6" /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#5B6577' : '#AEB6BF'} />
      <rect x={z.x0} y={f + 40} width={w} height={10} fill="#FFD54A" opacity={0.8} />
    </g>;
  },
  /** An airport terminal concourse inside: a wall of tall windows with an apron and parked jets outside (planes taxi by),
   *  gate signs, rows of seats, a glossy floor and a departures board. `night` darkens the sky outside. */
  terminal: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#3E4656' : '#ECEFF1'} />
      <rect x={z.x0} y={f - 640} width={w} height={420} fill={night ? '#16204A' : '#BFE6FA'} />
      <rect x={z.x0} y={f - 300} width={w} height={80} fill={night ? '#2B3242' : '#90A4AE'} />
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + ((k * 900 + t * 60) % (w + 900)) - 300;
        return <g key={'jet' + k} transform={`translate(${x} ${f - 300})`}>
          <path d="M -180 -10 L 160 -10 Q 200 -10 210 -30 L 150 -50 L -150 -50 Q -190 -50 -180 -10 Z" fill="#FFFFFF" stroke={OL} strokeWidth={3} />
          <path d="M -150 -50 L -190 -120 L -160 -120 L -100 -50 Z" fill="#90A4AE" stroke={OL} strokeWidth={3} />
          <path d="M -20 -30 L 40 -30 L -40 20 L -70 20 Z" fill="#CFD8DC" stroke={OL} strokeWidth={3} />
          {Array.from({length: 8}, (_, q) => <circle key={q} cx={-100 + q * 28} cy={-36} r={5} fill="#455A64" />)}</g>; })}
      {Array.from({length: Math.ceil(w / 220)}, (_, k) => <rect key={'mul' + k} x={z.x0 + k * 220} y={f - 650} width={16} height={440} fill="#607D8B" />)}
      <rect x={z.x0} y={f - 660} width={w} height={24} fill="#607D8B" />
      <rect x={z.x0} y={f - 210} width={w} height={210} fill={night ? '#4A5266' : '#D5DBE1'} />
      {Array.from({length: Math.ceil(w / 1000)}, (_, k) => { const x = z.x0 + 300 + k * 1000;
        return <g key={'gate' + k}><rect x={x} y={f - 760} width={160} height={70} rx={8} fill="#1565C0" stroke={OL} strokeWidth={3} />
          <T x={x + 80} y={f - 714} s={30} c="#FFFFFF">{'B' + (12 + k * 2)}</T></g>; })}
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => { const x = z.x0 + 40 + k * 120;
        return <g key={'seat' + k}><rect x={x} y={f - 70} width={90} height={22} rx={6} fill="#455A64" stroke={OL} strokeWidth={2} />
          <rect x={x} y={f - 110} width={90} height={44} rx={8} fill="#546E7A" stroke={OL} strokeWidth={2} /><rect x={x + 40} y={f - 48} width={10} height={48} fill="#37474F" /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#6B7280' : '#CFD8DC'} />
      <rect x={z.x0} y={f + 4} width={w} height={6} fill="#FFFFFF" opacity={0.6} />
    </g>;
  },
  /** A multi-level airport parking garage: concrete decks with cars parked in rows, a ramp, a ticket booth with a striped
   *  barrier and a big price sign ("$ / DAY"). */
  parkingdeck: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, cols = ['#E53935', '#1E88E5', '#43A047', '#FB8C00', '#8E24AA', '#B0BEC5', '#FFFFFF'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1A2346' : '#BFE6FA'} />
      {[0, 1, 2].map((lv) => <g key={'lv' + lv}>
        <rect x={z.x0} y={f - 210 - lv * 190} width={w} height={30} fill={night ? '#78909C' : '#B0BEC5'} stroke={OL} strokeWidth={3} />
        {Array.from({length: Math.ceil(w / 400)}, (_, k) => <rect key={k} x={z.x0 + k * 400} y={f - 180 - lv * 190} width={36} height={160} fill={night ? '#90A4AE' : '#CFD8DC'} stroke={OL} strokeWidth={2} />)}
        {Array.from({length: Math.ceil(w / 130)}, (_, k) => rnd(k * 7 + lv * 31) > 0.25 && <g key={'c' + k} transform={`translate(${z.x0 + 60 + k * 130} ${f - 40 - lv * 190})`}>
          <path d="M -50 0 L -50 -30 Q -40 -48 -20 -50 L 30 -50 Q 45 -48 52 -30 L 52 0 Z" fill={cols[(k + lv * 3) % cols.length]} stroke={OL} strokeWidth={2} />
          <rect x={-30} y={-46} width={50} height={16} rx={3} fill={K.glass} /><circle cx={-30} cy={2} r={10} fill="#263238" /><circle cx={32} cy={2} r={10} fill="#263238" /></g>)}</g>)}
      <rect x={z.x0} y={f - 720} width={w} height={30} fill={night ? '#78909C' : '#B0BEC5'} stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.ceil(w / 1600)}, (_, k) => { const x = z.x0 + 1000 + k * 1600;
        return <g key={'pb' + k}><rect x={x} y={f - 160} width={120} height={160} rx={8} fill="#FFC21A" stroke={OL} strokeWidth={4} />
          <rect x={x + 120} y={f - 100} width={300} height={16} rx={8} fill="#E53935" stroke={OL} strokeWidth={3} />
          {[0, 1, 2].map((q) => <rect key={q} x={x + 160 + q * 80} y={f - 100} width={30} height={16} fill="#FFFFFF" />)}
          <rect x={x - 40} y={f - 900} width={260} height={120} rx={10} fill="#1565C0" stroke={OL} strokeWidth={4} />
          <T x={x + 90} y={f - 850} s={34} c="#FFFFFF">PARKING</T><T x={x + 90} y={f - 806} s={30} c="#FFC21A">$ / DAY</T></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3E4656' : K.road} />
    </g>;
  },
  /** A 1950s-style bank hall: marble floor, fluted columns, brass teller windows between them, a wall clock and a
   *  banner (`label`). `night` dims it into an after-hours hall lit by desk lamps. */
  bankhall: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, n = Math.ceil(w / 520) + 1;
    const wall = night ? '#3B3A4F' : '#F3E9D2', trim = night ? '#6D5F45' : '#C9A85C';
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={wall} />
      <rect x={z.x0} y={f - 760} width={w} height={26} fill={trim} stroke={OL} strokeWidth={3} />
      {Array.from({length: n}, (_, k) => { const x = z.x0 + k * 520;
        return <g key={'bh' + k}>
          <rect x={x} y={f - 734} width={70} height={734} fill={night ? '#5C5B70' : '#FFFFFF'} stroke={OL} strokeWidth={4} />
          {[16, 35, 54].map((dx) => <path key={dx} d={`M ${x + dx} ${f - 720} L ${x + dx} ${f - 20}`} stroke={OL} strokeWidth={2} opacity={0.35} />)}
          <rect x={x - 14} y={f - 760} width={98} height={30} fill={trim} stroke={OL} strokeWidth={3} />
          <rect x={x - 14} y={f - 26} width={98} height={26} fill={trim} stroke={OL} strokeWidth={3} />
          <g transform={`translate(${x + 120} ${f - 420})`}>
            <rect x={0} y={0} width={330} height={420} fill={night ? '#4A3B2C' : '#8D6E4A'} stroke={OL} strokeWidth={4} />
            <rect x={20} y={40} width={290} height={170} fill={night ? '#2A3550' : '#DDF1FA'} stroke={OL} strokeWidth={3} />
            {Array.from({length: 9}, (_, q) => <rect key={q} x={30 + q * 32} y={40} width={6} height={170} fill="#D4AF37" stroke={OL} strokeWidth={1} />)}
            <rect x={10} y={210} width={310} height={22} fill="#D4AF37" stroke={OL} strokeWidth={3} />
            {night && <g><circle cx={260} cy={196} r={18} fill="#FFE08A" opacity={0.85} /><rect x={256} y={196} width={8} height={14} fill={OL} /></g>}
            <rect x={110} y={8} width={110} height={26} rx={4} fill={night ? '#2B2B3A' : '#1B3A5C'} stroke={OL} strokeWidth={2} />
            <T x={165} y={27} s={16} c="#FFE08A">{['TELLER', 'LOANS', 'CARDS', 'DEPOSITS'][k % 4]}</T></g></g>; })}
      <g transform={`translate(${z.x0 + w * 0.5} ${f - 640})`}>
        <circle r={70} fill="#FFFDF5" stroke={OL} strokeWidth={6} /><circle r={58} fill="none" stroke="#D4AF37" strokeWidth={4} />
        <path d={`M 0 0 L ${40 * Math.sin(t * 0.2)} ${-40 * Math.cos(t * 0.2)}`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
        <path d={`M 0 0 L ${52 * Math.sin(t * 2.4)} ${-52 * Math.cos(t * 2.4)}`} stroke={OL} strokeWidth={3} strokeLinecap="round" /></g>
      {z.label && <g transform={`translate(${z.x0 + w * 0.5} ${f - 790})`}><rect x={-340} y={-46} width={680} height={80} rx={8} fill="#1B3A5C" stroke={OL} strokeWidth={4} />
        <T x={0} y={8} s={40} c="#FFE08A">{z.label}</T></g>}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#4B4A5E' : '#E8E2D4'} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'tl' + k} x={z.x0 + k * 160} y={f} width={80} height={600} fill={night ? '#55546A' : '#D9D1BF'} opacity={0.6} />)}
      <rect x={z.x0} y={f} width={w} height={10} fill={trim} />
    </g>;
  },
  /** A supermarket: ceiling with hanging aisle signs, produce bins (apples, oranges, greens) at the front, checkout lanes
   *  with conveyor belts and lane-number lights, a deli counter at the back. `night` = after-hours lights. `label` = store banner. */
  supermarket: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, fruit = ['#E53935', '#FB8C00', '#7CB342', '#FDD835', '#8E24AA'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2E3A4E' : '#F6F1E7'} />
      <rect x={z.x0} y={f - 470} width={w} height={210} fill={night ? '#3B4A60' : '#E9F3E1'} />
      {Array.from({length: Math.ceil(w / 220)}, (_, k) => { const x = z.x0 + k * 220;
        return <g key={'sh' + k}>{[0, 1].map((r) => <g key={r}><rect x={x + 10} y={f - 380 + r * 92} width={200} height={10} fill="#8D6E63" />
          {Array.from({length: 6}, (_, q) => <rect key={q} x={x + 18 + q * 32} y={f - 440 + r * 92} width={26} height={58 - (q % 2) * 10} rx={3} fill={fruit[(k + q + r) % 5]} stroke={OL} strokeWidth={2} opacity={0.9} />)}</g>)}</g>; })}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => { const x = z.x0 + 300 + k * 700;
        return <g key={'as' + k}><path d={`M ${x + 90} ${f - 900} L ${x + 90} ${f - 800}`} stroke={OL} strokeWidth={3} />
          <rect x={x} y={f - 800} width={180} height={60} rx={6} fill="#2E7D32" stroke={OL} strokeWidth={3} />
          <T x={x + 90} y={f - 760} s={24} c="#FFFFFF">{['PRODUCE', 'DAIRY', 'MEAT', 'BAKERY', 'AISLE 5', 'FROZEN'][k % 6]}</T></g>; })}
      {Array.from({length: Math.ceil(w / 560)}, (_, k) => { const x = z.x0 + 80 + k * 560;
        return <g key={'ck' + k}>
          <rect x={x} y={f - 130} width={300} height={130} fill={night ? '#546E7A' : '#B0BEC5'} stroke={OL} strokeWidth={4} />
          <rect x={x + 10} y={f - 146} width={240} height={20} rx={8} fill="#263238" />
          {Array.from({length: 6}, (_, q) => <rect key={q} x={x + 14 + ((q * 40 + t * 40) % 230)} y={f - 152} width={2} height={26} fill="#78909C" />)}
          <rect x={x + 250} y={f - 220} width={50} height={90} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={3} />
          <path d={`M ${x + 150} ${f - 130} L ${x + 150} ${f - 330}`} stroke={OL} strokeWidth={4} />
          <circle cx={x + 150} cy={f - 350} r={26} fill={night ? '#FFE08A' : '#FFC21A'} stroke={OL} strokeWidth={3} />
          <T x={x + 150} y={f - 341} s={26} c={OL}>{String(k % 9 + 1)}</T>
          <g transform={`translate(${x + 390} ${f - 90})`}><rect x={-80} y={0} width={160} height={90} rx={10} fill="#8D6E63" stroke={OL} strokeWidth={4} />
            {Array.from({length: 7}, (_, q) => <circle key={q} cx={-60 + q * 20} cy={-4 - (q % 2) * 12} r={14} fill={fruit[(k + q) % 5]} stroke={OL} strokeWidth={2} />)}</g></g>; })}
      {z.label && <g transform={`translate(${z.x0 + w * 0.5} ${f - 700})`}><rect x={-260} y={-40} width={520} height={70} rx={10} fill="#C62828" stroke={OL} strokeWidth={4} />
        <T x={0} y={10} s={36} c="#FFFFFF">{z.label}</T></g>}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#45505E' : '#E7E1D6'} />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ft' + k} x={z.x0 + k * 120} y={f} width={60} height={600} fill={night ? '#4E5968' : '#DAD3C5'} opacity={0.7} />)}
    </g>;
  },
  /** A cattle ranch and feedlot: rolling yellow grass, wooden fence rails, generic brown/black cattle that sway, and a
   *  large boxy packing plant with a smokestack in the distance. `night` for dusk. */
  ranch: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, hide = ['#6D4C41', '#3E2723', '#8D6E63', '#4E342E'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#3A2F4A' : '#CDEBFA'} />
      <path d={`M ${z.x0} ${f - 260} ${Array.from({length: Math.ceil(w / 600) + 1}, (_, k) => `Q ${z.x0 + k * 600 + 300} ${f - 330 - 40 * rnd(k)} ${z.x0 + k * 600 + 600} ${f - 260}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#6B5B3E' : '#E6C76A'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 2200)}, (_, k) => { const x = z.x0 + 1500 + k * 2200;
        return <g key={'pp' + k}><rect x={x} y={f - 480} width={520} height={200} fill={night ? '#8E8AA8' : '#ECEFF1'} stroke={OL} strokeWidth={4} />
          <rect x={x + 420} y={f - 620} width={40} height={140} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
          {[0, 1, 2].map((q) => <circle key={q} cx={x + 440 + q * 18} cy={f - 650 - q * 34 - ((t * 20) % 30)} r={18 + q * 6} fill="#FFFFFF" opacity={0.6 - q * 0.15} />)}
          {Array.from({length: 6}, (_, q) => <rect key={q} x={x + 30 + q * 64} y={f - 440} width={40} height={30} fill={night ? '#FFE08A' : '#90CAF9'} stroke={OL} strokeWidth={2} />)}
          <rect x={x + 180} y={f - 360} width={120} height={80} fill="#78909C" stroke={OL} strokeWidth={3} /></g>; })}
      {Array.from({length: Math.ceil(w / 150)}, (_, k) => { const x = z.x0 + 40 + k * 150 + 40 * rnd(k), y = f - 60 - 40 * rnd(k + 4), b = Math.sin(t * 1.5 + k) * 3;
        return rnd(k * 3) > 0.2 && <g key={'cw' + k} transform={`translate(${x} ${y + b})`}>
          <rect x={-46} y={-40} width={92} height={46} rx={18} fill={hide[k % 4]} stroke={OL} strokeWidth={3} />
          <rect x={36} y={-56} width={34} height={30} rx={10} fill={hide[k % 4]} stroke={OL} strokeWidth={3} />
          {[-36, -18, 18, 36].map((lx) => <rect key={lx} x={lx - 5} y={2} width={10} height={26} fill={hide[k % 4]} stroke={OL} strokeWidth={2} />)}
          <circle cx={58} cy={-46} r={3} fill="#FFFFFF" /></g>; })}
      {[0, 1].map((r) => <rect key={'rl' + r} x={z.x0} y={f - 70 + r * 36} width={w} height={10} fill="#8D6E63" stroke={OL} strokeWidth={2} />)}
      {Array.from({length: Math.ceil(w / 240)}, (_, k) => <rect key={'po' + k} x={z.x0 + k * 240} y={f - 90} width={16} height={90} fill="#6D4C41" stroke={OL} strokeWidth={2} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#5A4A33' : '#C9A86A'} />
    </g>;
  },
  /** A granite bullion depository (generic, Fort Knox-like): two-storey stone block with columns of narrow windows, a
   *  central entrance with an eagle-less pediment, a guard box, a double fence and green Kentucky hills. `night` = floodlit. */
  depository: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, cx = z.x0 + w * 0.5;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#1C2340' : '#BFE6FA'} />
      {night && <circle cx={cx + 700} cy={f - 700} r={50} fill="#FFF3C4" opacity={0.9} />}
      <path d={`M ${z.x0} ${f - 240} ${Array.from({length: Math.ceil(w / 700) + 1}, (_, k) => `Q ${z.x0 + k * 700 + 350} ${f - 330 - 50 * rnd(k)} ${z.x0 + k * 700 + 700} ${f - 240}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#2E4A33' : '#7CB342'} stroke={OL} strokeWidth={4} />
      <g transform={`translate(${cx} ${f})`}>
        <rect x={-560} y={-460} width={1120} height={460} fill={night ? '#9FA5AE' : '#D7D2C8'} stroke={OL} strokeWidth={6} />
        <rect x={-600} y={-500} width={1200} height={50} fill={night ? '#8A9099' : '#C6C0B4'} stroke={OL} strokeWidth={6} />
        {Array.from({length: 10}, (_, k) => { const x = -520 + k * 110; if (Math.abs(x + 25) < 170) return null;
          return <g key={k}>{[0, 1].map((r) => <rect key={r} x={x} y={-420 + r * 200} width={44} height={130} fill={night ? '#FFE08A' : '#5D6B7A'} stroke={OL} strokeWidth={4} />)}</g>; })}
        <rect x={-180} y={-560} width={360} height={560} fill={night ? '#B0B6BF' : '#E4DFD5'} stroke={OL} strokeWidth={6} />
        <path d="M -200 -560 L 0 -640 L 200 -560 Z" fill={night ? '#9FA5AE' : '#CFC9BE'} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <rect x={-70} y={-230} width={140} height={230} fill="#3E4A57" stroke={OL} strokeWidth={6} />
        {[-130, 130].map((x) => <rect key={x} x={x - 14} y={-500} width={28} height={500} fill={night ? '#C9CED6' : '#F1EDE5'} stroke={OL} strokeWidth={4} />)}
        <T x={0} y={-500} s={34} c={OL}>BULLION DEPOSITORY</T>
      </g>
      <g transform={`translate(${cx - 900} ${f})`}><rect x={-60} y={-200} width={120} height={200} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
        <rect x={-40} y={-170} width={80} height={60} fill={night ? '#FFE08A' : '#90CAF9'} stroke={OL} strokeWidth={4} /><path d="M -80 -200 L 0 -250 L 80 -200 Z" fill="#78909C" stroke={OL} strokeWidth={5} /></g>
      {[0, 1].map((r) => <g key={'fn' + r}><rect x={z.x0} y={f - 120 + r * 50} width={w} height={6} fill="#90A4AE" />
        {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={k} x={z.x0 + k * 120 + r * 40} y={f - 140 + r * 50} width={8} height={90} fill="#78909C" />)}</g>)}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3A4A3A' : '#8BC34A'} />
      <rect x={cx - 120} y={f} width={240} height={600} fill={night ? '#6B6F75' : '#BDBDBD'} />
    </g>;
  },
  /** A mint production floor: big coin presses with a pumping ram, a conveyor carrying copper/silver coins, coin bins and
   *  ceiling lamps. `night` = dim after-hours floor. `label` = banner. */
  mintfloor: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2A3140' : '#DCE3EA'} />
      <rect x={z.x0} y={f - 700} width={w} height={30} fill={night ? '#3A4456' : '#B0BEC5'} />
      {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const x = z.x0 + 180 + k * 360; return <g key={'lp' + k}>
        <path d={`M ${x} ${f - 700} L ${x} ${f - 640}`} stroke={OL} strokeWidth={3} /><path d={`M ${x - 40} ${f - 600} L ${x} ${f - 640} L ${x + 40} ${f - 600} Z`} fill="#546E7A" stroke={OL} strokeWidth={3} />
        <path d={`M ${x - 40} ${f - 600} L ${x - 120} ${f - 300} L ${x + 120} ${f - 300} L ${x + 40} ${f - 600} Z`} fill="#FFF8E1" opacity={night ? 0.12 : 0.22} /></g>; })}
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + 300 + k * 900, ram = 30 * Math.abs(Math.sin(t * 3 + k));
        return <g key={'pr' + k}>
          <rect x={x - 130} y={f - 520} width={260} height={90} rx={10} fill="#78909C" stroke={OL} strokeWidth={5} />
          <rect x={x - 110} y={f - 430} width={40} height={300} fill="#90A4AE" stroke={OL} strokeWidth={4} /><rect x={x + 70} y={f - 430} width={40} height={300} fill="#90A4AE" stroke={OL} strokeWidth={4} />
          <rect x={x - 40} y={f - 430 + ram} width={80} height={90} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
          <rect x={x - 150} y={f - 130} width={300} height={130} fill="#607D8B" stroke={OL} strokeWidth={5} />
          <rect x={x - 100} y={f - 500} width={200} height={40} rx={6} fill={night ? '#263238' : '#37474F'} />
          <T x={x} y={f - 472} s={22} c="#FFC21A">PRESS {k + 1}</T></g>; })}
      <rect x={z.x0} y={f - 150} width={w} height={26} fill="#37474F" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => { const cx = z.x0 + ((k * 60 + t * 90) % w);
        return <circle key={'cn' + k} cx={cx} cy={f - 162} r={14} fill={k % 3 ? '#C77B3A' : '#CFD8DC'} stroke={OL} strokeWidth={3} />; })}
      {Array.from({length: Math.ceil(w / 1100)}, (_, k) => { const x = z.x0 + 750 + k * 1100;
        return <g key={'bn' + k}><path d={`M ${x - 120} ${f - 100} L ${x + 120} ${f - 100} L ${x + 100} ${f} L ${x - 100} ${f} Z`} fill="#8D6E63" stroke={OL} strokeWidth={5} />
          {Array.from({length: 9}, (_, q) => <circle key={q} cx={x - 80 + (q % 5) * 40} cy={f - 110 - Math.floor(q / 5) * 18} r={16} fill="#C77B3A" stroke={OL} strokeWidth={3} />)}</g>; })}
      {z.label && <g transform={`translate(${z.x0 + w * 0.5} ${f - 760})`}><rect x={-300} y={-40} width={600} height={70} rx={10} fill="#1B3A5C" stroke={OL} strokeWidth={4} />
        <T x={0} y={10} s={36} c="#FFE08A">{z.label}</T></g>}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3B4250' : '#9EA7B0'} />
    </g>;
  },
  /** An oil storage hub on the flat prairie (generic, Cushing-like): big sky, rows of white cylindrical tanks in the back,
   *  pipelines on short legs, a few grain-elevator silhouettes. `night` for dusk. */
  tankfarm: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2B2440' : '#BFE3F5'} />
      {night ? <circle cx={z.x0 + w * 0.6} cy={f - 520} r={60} fill="#FFB74D" opacity={0.85} /> : <circle cx={z.x0 + w * 0.6} cy={f - 680} r={70} fill={K.sun} stroke={OL} strokeWidth={4} />}
      <rect x={z.x0} y={f - 260} width={w} height={260} fill={night ? '#3D3A55' : '#D8E8B0'} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const x = z.x0 + 40 + k * 260, h = 120 + (k % 3) * 30, r = 100;
        return <g key={'tk' + k}>
          <rect x={x} y={f - 230 - h} width={r * 2} height={h} fill={night ? '#8E8AA8' : '#F4F6F8'} stroke={OL} strokeWidth={4} />
          <ellipse cx={x + r} cy={f - 230 - h} rx={r} ry={16} fill={night ? '#A7A3C0' : '#FFFFFF'} stroke={OL} strokeWidth={4} />
          <path d={`M ${x + 20} ${f - 230 - h} L ${x + 60} ${f - 230}`} stroke={OL} strokeWidth={3} opacity={0.5} />
          <ellipse cx={x + r} cy={f - 230} rx={r} ry={16} fill="none" stroke={OL} strokeWidth={3} opacity={0.4} /></g>; })}
      <rect x={z.x0} y={f - 150} width={w} height={22} fill="#78909C" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f - 110} width={w} height={16} fill="#90A4AE" stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'pl' + k} x={z.x0 + 60 + k * 200} y={f - 128} width={10} height={128} fill="#546E7A" />)}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#4A4560' : '#C9B88F'} />
      <rect x={z.x0} y={f} width={w} height={14} fill={night ? '#5B5575' : '#B5A27A'} />
    </g>;
  },
  /** A clean studio backdrop for full-screen data moments: soft vertical gradient, faint grid, a horizon line.
   *  `night` = dark navy studio. Lets big charts and typography carry the scene (a different "language"). */
  studio: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const id = 'stg' + Math.round(z.x0);
    return <g>
      <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={night ? '#0E1726' : '#F6F3EC'} /><stop offset="1" stopColor={night ? '#1B2A40' : '#E4DDCF'} /></linearGradient></defs>
      <rect x={z.x0} y={-2000} width={w} height={3600} fill={`url(#${id})`} />
      {Array.from({length: Math.ceil(w / 120) + 1}, (_, k) => <rect key={'gv' + k} x={z.x0 + k * 120} y={-600} width={2} height={f + 600} fill={night ? '#FFFFFF' : OL} opacity={0.05} />)}
      {Array.from({length: 14}, (_, k) => <rect key={'gh' + k} x={z.x0} y={f - k * 120} width={w} height={2} fill={night ? '#FFFFFF' : OL} opacity={0.05} />)}
      <rect x={z.x0} y={f} width={w} height={8} fill={night ? '#4FC3F7' : OL} opacity={0.5} />
    </g>;
  },
  /** An investigator's evidence wall: cork board in a wooden frame on a dim wall, a desk lamp glow. Pair with `pinboard`. */
  corkboard: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#2E2A26" />
      <rect x={z.x0} y={f - 900} width={w} height={860} fill="#B7864F" />
      {Array.from({length: Math.ceil(w / 18) * 4}, (_, k) => <circle key={'ck' + k} cx={z.x0 + rnd(k) * w} cy={f - 900 + rnd(k + 7) * 860} r={1.5 + rnd(k + 3) * 2.5} fill={rnd(k + 9) > 0.5 ? '#9C6E3C' : '#CFA06A'} opacity={0.6} />)}
      <rect x={z.x0} y={f - 920} width={w} height={26} fill="#5D4029" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f - 52} width={w} height={26} fill="#5D4029" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f - 26} width={w} height={700} fill="#3A2C22" />
      <ellipse cx={z.x0 + w * 0.5} cy={f - 500} rx={w * 0.45} ry={520} fill="#FFE9B0" opacity={0.10 + 0.02 * Math.sin(t * 1.3)} />
    </g>;
  },
  /** A mountain valley factory: blue ridges, a long white plant with a sawtooth roof and stacks, a levee and a river in
   *  front; `floodAt` (s) makes the river rise over the levee and spread across the floor; `night` dims it. Generic. */
  riverplant: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, fa = (z as any).floodAt as number | undefined;
    const fl = fa !== undefined ? clamp((t - fa) / 4) : 0, wl = f + 110 - fl * 190;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2A3550' : '#BFE3F5'} />
      {[0, 1].map((r) => <path key={'rg' + r} d={`M ${z.x0} ${f - 260 + r * 80} ${Array.from({length: Math.ceil(w / 260) + 1}, (_, k) => `Q ${z.x0 + k * 260 + 130} ${f - 520 + r * 120 - 120 * rnd(k + r * 9)} ${z.x0 + (k + 1) * 260} ${f - 260 + r * 80}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`}
        fill={night ? (r ? '#34466A' : '#2C3B5C') : (r ? '#7FA9C9' : '#9CC2DD')} stroke={OL} strokeWidth={3} />)}
      {Array.from({length: Math.ceil(w / 1400)}, (_, k) => { const x = z.x0 + 300 + k * 1400;
        return <g key={'pl' + k}>
          <rect x={x} y={f - 300} width={1000} height={300} fill={night ? '#7D8AA6' : '#F4F7FA'} stroke={OL} strokeWidth={5} />
          <path d={`M ${x} ${f - 300} ${Array.from({length: 8}, (_, q) => `L ${x + q * 125 + 60} ${f - 370} L ${x + q * 125 + 125} ${f - 300}`).join(' ')}`} fill={night ? '#6A7794' : '#DCE5EC'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          {[0, 1].map((q) => <g key={q}><rect x={x + 760 + q * 90} y={f - 520} width={50} height={220} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
            <circle cx={x + 785 + q * 90 + Math.sin(t + q) * 8} cy={f - 560 - ((t * 30 + q * 40) % 80)} r={22} fill="#FFFFFF" opacity={0.6} /></g>)}
          {Array.from({length: 7}, (_, q) => <rect key={'w' + q} x={x + 50 + q * 130} y={f - 230} width={80} height={60} fill={night ? '#FFE08A' : '#BFE8FF'} stroke={OL} strokeWidth={3} />)}
          <rect x={x + 420} y={f - 120} width={160} height={120} fill="#90A4AE" stroke={OL} strokeWidth={4} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3E4A3A' : '#8FBF6A'} />
      <path d={`M ${z.x0} ${f + 60} L ${z.x1} ${f + 60} L ${z.x1} ${f + 120} L ${z.x0} ${f + 120} Z`} fill="#A1887F" stroke={OL} strokeWidth={4} />
      {fl > 0.6 && <path d={`M ${z.x0 + w * 0.48} ${f + 60} l 40 60 l -70 0 Z`} fill={night ? '#3E4A3A' : '#8FBF6A'} />}
      <rect x={z.x0} y={Math.min(wl, f + 130)} width={w} height={600} fill={night ? '#2F5D86' : '#4FA3D9'} opacity={0.92} />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 200 + ((t * 60) % 200)} ${Math.min(wl, f + 130) + 30} q 30 -14 60 0`} fill="none" stroke="#FFFFFF" strokeWidth={4} opacity={0.6} />)}
    </g>;
  },
  /** A generic stadium at game time: tiered stands with a waving crowd, floodlights, a striped field, a scoreboard showing
   *  `label` (default 'HOME 0 – 0 AWAY'); `night` lights the floodlights. No team names or logos. */
  stadium: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, lab = (z as any).label || 'HOME 0 – 0 AWAY';
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#121A33' : '#9FD3F2'} />
      {[0, 1, 2].map((r) => <rect key={'st' + r} x={z.x0} y={f - 520 + r * 130} width={w} height={130} fill={['#5C6B8A', '#4E5C7A', '#43506B'][r]} stroke={OL} strokeWidth={3} />)}
      {Array.from({length: Math.ceil(w / 46) * 3}, (_, k) => { const r = k % 3, x = z.x0 + Math.floor(k / 3) * 46 + (r % 2) * 23, up = Math.sin(t * 4 + x * 0.02) > 0.6 ? 14 : 0;
        return <circle key={'cr' + k} cx={x} cy={f - 470 + r * 130 - up} r={14} fill={['#FF7043', '#FFCA28', '#42A5F5', '#EC407A', '#66BB6A'][(k * 7) % 5]} stroke={OL} strokeWidth={2} />; })}
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + 300 + k * 900;
        return <g key={'fl' + k}><rect x={x - 8} y={f - 900} width={16} height={380} fill="#78909C" />
          <rect x={x - 70} y={f - 960} width={140} height={70} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
          {Array.from({length: 6}, (_, q) => <circle key={q} cx={x - 50 + (q % 3) * 50} cy={f - 940 + Math.floor(q / 3) * 30} r={10} fill={night ? '#FFF59D' : '#FFFDE7'} />)}
          {night && <path d={`M ${x - 70} ${f - 890} L ${x - 300} ${f} L ${x + 300} ${f} L ${x + 70} ${f - 890} Z`} fill="#FFF9C4" opacity={0.08} />}</g>; })}
      <g transform={`translate(${z.x0 + w * 0.6} ${f - 760})`}><rect x={-230} y={-80} width={460} height={140} rx={14} fill="#1B1F27" stroke={OL} strokeWidth={6} />
        <rect x={-20} y={60} width={40} height={180} fill="#455A64" />
        <T x={0} y={14} s={44} c="#FFC21A">{lab}</T></g>
      <rect x={z.x0} y={f} width={w} height={600} fill="#4CAF50" />
      {Array.from({length: Math.ceil(w / 240)}, (_, k) => <rect key={'fs' + k} x={z.x0 + k * 240} y={f} width={120} height={600} fill="#43A047" />)}
      <rect x={z.x0} y={f} width={w} height={8} fill="#FFFFFF" opacity={0.8} />
    </g>;
  },
  /** A generic post office lobby: a wall of numbered PO boxes, a service counter with a scale, stacked parcels and mail
   *  bins, an eagle-free plain sign with `label` (default 'POST OFFICE'); `night` dims it. No real logos. */
  postoffice: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, lab = (z as any).label || 'POST OFFICE';
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#2E3A52' : '#EAF1F8'} />
      <rect x={z.x0} y={f - 700} width={w} height={60} fill="#1F4E8C" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 1600)}, (_, k) => <T key={'ps' + k} x={z.x0 + 800 + k * 1600} y={f - 658} s={36} c="#FFFFFF">{lab}</T>)}
      {Array.from({length: Math.ceil(w / 1600)}, (_, k) => { const x0 = z.x0 + 120 + k * 1600;
        return <g key={'pb' + k}>
          {Array.from({length: 40}, (_, q) => { const c = q % 10, r = Math.floor(q / 10);
            return <g key={q}><rect x={x0 + c * 62} y={f - 600 + r * 70} width={56} height={62} rx={4} fill={night ? '#8D99AE' : '#C9A227'} stroke={OL} strokeWidth={3} />
              <circle cx={x0 + c * 62 + 44} cy={f - 600 + r * 70 + 31} r={5} fill={OL} />
              <T x={x0 + c * 62 + 22} y={f - 600 + r * 70 + 38} s={14} c={OL}>{String(100 + k * 40 + q)}</T></g>; })}
          <rect x={x0 + 760} y={f - 260} width={620} height={260} fill={night ? '#6D5A4A' : '#A1887F'} stroke={OL} strokeWidth={5} />
          <rect x={x0 + 740} y={f - 280} width={660} height={30} fill="#5D4037" stroke={OL} strokeWidth={4} />
          <rect x={x0 + 840} y={f - 330} width={110} height={50} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
          <T x={x0 + 895} y={f - 297} s={22} c={OL}>{(1.2 + Math.sin(t + k) * 0.1).toFixed(1) + ' LB'}</T>
          {[0, 1, 2].map((q) => <rect key={'pc' + q} x={x0 + 1100 + q * 70 - (q === 2 ? 35 : 0)} y={f - 280 - (q === 2 ? 130 : 65)} width={q === 2 ? 70 : 64} height={q === 2 ? 65 : 65} fill="#C8A26B" stroke={OL} strokeWidth={4} />)}
          <rect x={x0 + 1440} y={f - 160} width={120} height={160} fill="#1F4E8C" stroke={OL} strokeWidth={4} />
          <rect x={x0 + 1440} y={f - 190} width={120} height={40} rx={20} fill="#1F4E8C" stroke={OL} strokeWidth={4} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#3D4658' : '#CFD8DC'} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'pt' + k} x={z.x0 + k * 160} y={f} width={3} height={600} fill={OL} opacity={0.1} />)}
    </g>;
  },
  /** Alaska-like north (generic): snowy peaks, spruce trees, a silver pipeline on stilts zig-zagging across the tundra,
   *  a small town of cabins; `night` = dark sky with green northern lights. */
  tundra: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#0B1630' : '#CFE8F7'} />
      {night && [0, 1, 2].map((q) => <path key={'au' + q} d={`M ${z.x0} ${f - 820 + q * 50} ${Array.from({length: Math.ceil(w / 300) + 1}, (_, k) => `Q ${z.x0 + k * 300 + 150} ${f - 900 + q * 50 + 80 * Math.sin(t * 0.6 + k + q)} ${z.x0 + (k + 1) * 300} ${f - 820 + q * 50}`).join(' ')}`}
        fill="none" stroke={['#5CFFB0', '#3DDC97', '#9B7BFF'][q]} strokeWidth={26 - q * 6} opacity={0.35} strokeLinecap="round" />)}
      <path d={`M ${z.x0} ${f - 250} ${Array.from({length: Math.ceil(w / 340) + 1}, (_, k) => `L ${z.x0 + k * 340 + 170} ${f - 560 - 140 * rnd(k + 5)} L ${z.x0 + (k + 1) * 340} ${f - 250}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#3A4A6E' : '#9DB5CC'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {Array.from({length: Math.ceil(w / 340) + 1}, (_, k) => { const px = z.x0 + k * 340 + 170, py = f - 560 - 140 * rnd(k + 5);
        return <path key={'sn' + k} d={`M ${px - 55} ${py + 80} L ${px} ${py} L ${px + 55} ${py + 80} L ${px + 20} ${py + 64} L ${px} ${py + 86} L ${px - 20} ${py + 64} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={3} strokeLinejoin="round" />; })}
      <rect x={z.x0} y={f - 120} width={w} height={720} fill={night ? '#C9D6E8' : '#F4F8FB'} />
      {Array.from({length: Math.ceil(w / 130)}, (_, k) => { const x = z.x0 + k * 130 + 40 * rnd(k), h = 90 + 50 * rnd(k + 9);
        return <path key={'tr' + k} d={`M ${x} ${f - 120} L ${x - 26} ${f - 120} L ${x} ${f - 120 - h} L ${x + 26} ${f - 120} Z`} fill={night ? '#1E4A3A' : '#2E7D5B'} stroke={OL} strokeWidth={3} />; })}
      <path d={`M ${z.x0} ${f - 40} ${Array.from({length: Math.ceil(w / 400) + 1}, (_, k) => `L ${z.x0 + k * 400 + 200} ${f - 70 + (k % 2) * 40} L ${z.x0 + (k + 1) * 400} ${f - 40}`).join(' ')}`} fill="none" stroke="#B0BEC5" strokeWidth={18} strokeLinejoin="round" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'pl' + k} x={z.x0 + k * 200} y={f - 40} width={8} height={60} fill="#78909C" />)}
      {Array.from({length: Math.ceil(w / 1500)}, (_, k) => <g key={'cb' + k}>{[0, 1, 2].map((q) => { const x = z.x0 + 900 + k * 1500 + q * 150;
        return <g key={q}><rect x={x} y={f + 10} width={110} height={80} fill="#8D6E63" stroke={OL} strokeWidth={4} />
          <path d={`M ${x - 12} ${f + 14} L ${x + 55} ${f - 40} L ${x + 122} ${f + 14} Z`} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
          <rect x={x + 40} y={f + 36} width={30} height={30} fill={night ? '#FFE082' : '#BFE8FF'} stroke={OL} strokeWidth={3} /></g>; })}</g>)}
    </g>;
  },
  /** A coastal launch site: sky (night = stars), the sea on the horizon, a lattice launch tower with a service arm,
   *  spherical fuel tanks, a concrete pad and, further along, a round landing pad with a painted target ring. */
  launchpad: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, tx = z.x0 + w * ((z as any).towerAt ?? 0.38), lx = z.x0 + w * ((z as any).landAt ?? 0.72);
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#0B1430' : '#8FD3FF'} />
      <rect x={z.x0} y={f - 520} width={w} height={520} fill={night ? '#16244A' : '#CDEEFF'} opacity={0.8} />
      {night && Array.from({length: Math.ceil(w / 60)}, (_, k) => <circle key={'st' + k} cx={z.x0 + k * 60 + 40 * rnd(k)} cy={f - 1100 + 560 * rnd(k + 5)} r={1.5 + 2 * rnd(k + 9)}
        fill="#FFFFFF" opacity={0.4 + 0.5 * Math.abs(Math.sin(t * (0.7 + rnd(k)) + k))} />)}
      <rect x={z.x0} y={f - 150} width={w} height={70} fill={night ? '#1C3B6B' : '#2E9BD6'} />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 90 + 18 * Math.sin(t + k)} ${f - 120 + 30 * rnd(k)} q 15 -7 30 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.6} />)}
      <rect x={z.x0} y={f - 80} width={w} height={80} fill={night ? '#5E6B4A' : '#C9D98A'} stroke={OL} strokeWidth={4} />
      {Array.from({length: 3}, (_, k) => <g key={'tk' + k} transform={`translate(${tx - 520 + k * 120} ${f - 80})`}>
        <circle cx={0} cy={-60} r={56} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><rect x={-40} y={-10} width={80} height={10} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g>)}
      <rect x={tx - 260} y={f - 30} width={520} height={30} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      <g transform={`translate(${tx - 150} ${f - 30})`}>
        <rect x={-30} y={-780} width={60} height={780} fill="none" stroke="#C62828" strokeWidth={8} />
        {Array.from({length: 13}, (_, k) => <path key={k} d={`M -30 ${-k * 60} L 30 ${-k * 60 - 60} M 30 ${-k * 60} L -30 ${-k * 60 - 60}`} stroke="#C62828" strokeWidth={4} />)}
        <rect x={30} y={-560} width={110} height={16} fill="#90A4AE" stroke={OL} strokeWidth={3} />
        <circle cx={0} cy={-800} r={10} fill={Math.sin(t * 3) > 0 ? '#FF5252' : '#7F0000'} />
      </g>
      <g transform={`translate(${lx} ${f - 34})`}>
        <ellipse cx={0} cy={0} rx={230} ry={34} fill="#9E9E9E" stroke={OL} strokeWidth={4} />
        <ellipse cx={0} cy={0} rx={150} ry={22} fill="none" stroke={K.white} strokeWidth={8} />
        <ellipse cx={0} cy={0} rx={60} ry={9} fill={K.gold} stroke={OL} strokeWidth={3} />
      </g>
      {Array.from({length: Math.ceil(w / 500)}, (_, k) => <path key={'pl' + k} d={`M ${z.x0 + 120 + k * 500} ${f - 80} l 0 -60 m -16 18 q 16 -30 32 0`} stroke="#4E7D3A" strokeWidth={6} fill="none" />)}
    </g>;
  },
  /** Retro-future neon CHIP CITY (original design): towers shaped like computer chips (pin "legs" on the sides, a glowing
   *  die window, antennas), glass transit tubes with capsules zipping through, bubble-canopy flying cars, joke neon signs.
   *  `dimAt`: the neon flickers and dims (mood drop). `signs`: override the joke signs. */
  /** BEFORE YOU BUY series: the MONEY MACHINE (original design). A retro-futurist factory hall with a big chrome
   *  machine; one labelled intake pipe per revenue segment (`segments` [{label, value, color, at?}]; pipe thickness ∝
   *  value), glowing blobs flowing in, pistons pumping, gauges wobbling, coins tumbling out of the output chute into a
   *  bin labelled `out`. Joke signs on the back wall (`signs`). `night`: darker hall. `boomAt`: the machine shudders. */
  moneymachine: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, night = !!z.night;
    const segs: {label: string; value: number; color?: string; at?: number}[] = zz.segments || [{label: 'REVENUE', value: 1}];
    const total = segs.reduce((s, q) => s + Math.max(0, q.value), 0) || 1;
    const mx = zz.mx ?? z.x0 + w * (zz.machineAt ?? 0.55), my = f - 330;
    const shud = zz.boomAt !== undefined && t > zz.boomAt && t < zz.boomAt + 1.2 ? 6 * Math.sin(t * 60) * (1 - (t - zz.boomAt) / 1.2) : 0;
    const signs: string[] = zz.signs || ['PROFIT DEPT · 3RD FLOOR', 'NO FREE LUNCH (ASK)', 'MIND THE MARGIN', 'QUARTERLY HUMS ONLY'];
    const pal = ['#FF4FD8', '#3DF5FF', '#FFE14D', '#7DFF8A', '#FF9F1C', '#7B61FF'];
    const pump = (k: number) => Math.sin(t * 4.2 + k * 1.7);
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#140A2E' : '#2B1860'} />
      {Array.from({length: Math.ceil(w / 240)}, (_, k) => <g key={'pn' + k}>
        <rect x={z.x0 + k * 240} y={f - 1100} width={236} height={1040} fill={night ? '#1C1140' : '#3A2378'} stroke="#24154F" strokeWidth={4} />
        {[0, 1, 2, 3, 4, 5].map((r) => <circle key={r} cx={z.x0 + k * 240 + 14} cy={f - 1080 + r * 190} r={5} fill="#7E6BC4" />)}</g>)}
      {signs.map((s, k) => { const sx = mx - 1150 + k * 1000, on = Math.sin(t * (1.3 + k) + k) > -0.85;
        return <g key={'ms' + k} transform={`translate(${sx} ${f - 800}) rotate(${-3 + 2 * Math.sin(t * 0.9 + k)})`}>
          <rect x={-190} y={-34} width={380} height={64} rx={32} fill="#120A2A" stroke={pal[k % pal.length]} strokeWidth={5} opacity={on ? 1 : 0.5} />
          <T x={0} y={10} s={24} c={pal[k % pal.length]} o={on ? 1 : 0.4}>{s}</T></g>; })}
      {/* intake pipes from the left wall into the machine */}
      {segs.map((q, k) => { const th = 26 + 120 * (Math.max(0, q.value) / total), py = my - 170 + k * (360 / Math.max(1, segs.length - 1 || 1)) * (segs.length > 1 ? 1 : 0),
          c = q.color || pal[k % pal.length], on = q.at === undefined || t >= q.at, x0 = Math.max(z.x0 + 40, mx - 1250), x1 = mx - 230;
        const grow = q.at === undefined ? 1 : clamp((t - q.at) / 0.8), xe = lerp(x0, x1, E.out(grow));
        return <g key={'pp' + k}>
          <rect x={x0} y={py - th / 2} width={Math.max(0, xe - x0)} height={th} rx={th / 2} fill="#B0BEC5" stroke={OL} strokeWidth={6} />
          <rect x={x0} y={py - th / 2 + 6} width={Math.max(0, xe - x0)} height={Math.max(4, th * 0.22)} rx={4} fill="#FFFFFF" opacity={0.35} />
          {on && Array.from({length: 6}, (_, b) => { const u = ((t * 0.45 + b / 6 + k * 0.13) % 1), bx = lerp(x0 + 20, xe - 10, u);
            return bx < xe - 8 && <ellipse key={b} cx={bx} cy={py} rx={Math.min(th * 0.42, 34)} ry={th * 0.3} fill={c} stroke={OL} strokeWidth={3} opacity={0.95} />; })}
          {[0.25, 0.6].map((u) => <rect key={u} x={lerp(x0, x1, u) - 10} y={py - th / 2 - 8} width={20} height={th + 16} rx={6} fill="#78909C" stroke={OL} strokeWidth={4} opacity={grow > u ? 1 : 0} />)}
          <g opacity={grow} transform={`translate(${Math.max(x0 + 30, x1 - Math.max(160, q.label.length * 17 + 30) - 60)} ${py - th / 2 - 30})`}>
            <rect x={0} y={-30} width={Math.max(160, q.label.length * 17 + 30)} height={44} rx={10} fill="#FFF8E1" stroke={OL} strokeWidth={4} />
            <T x={14} y={2} s={24} a="start">{q.label}</T></g>
        </g>; })}
      {/* the machine */}
      <g transform={`translate(${mx + shud} ${my})`}>
        <rect x={-240} y={-260} width={480} height={520} rx={60} fill="#CFD8DC" stroke={OL} strokeWidth={8} />
        <rect x={-210} y={-232} width={70} height={464} rx={30} fill="#FFFFFF" opacity={0.35} />
        <path d="M -200 -260 Q 0 -440 200 -260 Z" fill="#90A4AE" stroke={OL} strokeWidth={8} />
        <circle cx={0} cy={-330} r={34} fill={Math.sin(t * 5) > 0 ? '#FF4F6B' : '#FFE14D'} stroke={OL} strokeWidth={6} />
        {[-1, 1].map((d, k) => <g key={'pi' + k} transform={`translate(${d * 120} ${-260 - 40 - 28 * Math.max(0, pump(k))})`}>
          <rect x={-22} y={-60} width={44} height={90} rx={8} fill="#78909C" stroke={OL} strokeWidth={5} />
          <circle cx={0} cy={-66} r={14} fill="#B0BEC5" stroke={OL} strokeWidth={4} /></g>)}
        {[-1, 0, 1].map((d) => { const ang = -60 + 50 * Math.sin(t * (1.6 + d) + d) + 20 * d;
          return <g key={'gg' + d} transform={`translate(${d * 140} -120)`}>
            <circle r={52} fill="#FFF8E1" stroke={OL} strokeWidth={6} />
            {[-60, -30, 0, 30, 60].map((g) => <path key={g} d={`M ${Math.sin((g * Math.PI) / 180) * 38} ${-Math.cos((g * Math.PI) / 180) * 38} L ${Math.sin((g * Math.PI) / 180) * 46} ${-Math.cos((g * Math.PI) / 180) * 46}`} stroke={OL} strokeWidth={4} />)}
            <path d={`M 0 0 L ${Math.sin((ang * Math.PI) / 180) * 40} ${-Math.cos((ang * Math.PI) / 180) * 40}`} stroke="#E53935" strokeWidth={6} strokeLinecap="round" />
            <circle r={7} fill={OL} /></g>; })}
        <rect x={-170} y={0} width={340} height={120} rx={18} fill="#14102E" stroke={OL} strokeWidth={6} />
        {Array.from({length: 12}, (_, q) => { const on = Math.sin(t * (3 + (q % 4)) + q) > 0;
          return <rect key={q} x={-150 + (q % 6) * 52} y={18 + Math.floor(q / 6) * 50} width={40} height={34} rx={6} fill={on ? pal[q % pal.length] : '#2A2350'} />; })}
        <T x={0} y={215} s={40} c={OL}>{zz.name || 'THE MONEY MACHINE'}</T>
        {/* output chute + coins */}
        <path d="M 230 120 L 380 170 L 380 250 L 230 230 Z" fill="#90A4AE" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      </g>
      {Array.from({length: 9}, (_, k) => { const u = ((t * 0.9 + k / 9) % 1), cx2 = mx + 390 + 40 * u + 20 * rnd(k), cy2 = my + 210 + u * u * 300;
        return <g key={'mc' + k} transform={`translate(${cx2} ${cy2}) rotate(${t * 300 + k * 40})`} opacity={u < 0.92 ? 1 : 0}>
          <ellipse rx={22} ry={22 * Math.abs(Math.cos(t * 6 + k))} fill="#FFC93C" stroke={OL} strokeWidth={4} /></g>; })}
      <g transform={`translate(${mx + 440} ${f - 10})`}>
        <path d="M -120 -150 L 120 -150 L 100 0 L -100 0 Z" fill="#FF9F1C" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
        <ellipse cx={0} cy={-150} rx={120} ry={20} fill="#FFC93C" stroke={OL} strokeWidth={6} />
        <T x={0} y={-62} s={26} c={OL}>{zz.out || 'CASH'}</T></g>
      <rect x={z.x0} y={f - 20} width={w} height={20} fill="#4A2F8A" stroke={OL} strokeWidth={5} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#1E1040" />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <path key={'hz' + k} d={`M ${z.x0 + k * 160} ${f + 40} l 80 0 l -30 40 l -80 0 Z`} fill="#FFE14D" opacity={0.25} />)}
    </g>;
  },
  /** CLOUD PORT (original design, series Before You Buy): a retro-futurist sky harbor. Data-center towers on stilts with
   *  glowing rack windows, round cloud-blimps (server pods) floating in to dock on cables, chrome cooling fans spinning,
   *  joke signs (`signs`). `busyAt`: from that time, blimps queue and the dock lights flash (demand > supply). */
  cloudport: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, busy = zz.busyAt !== undefined && t >= zz.busyAt ? 1 : 0;
    const signs: string[] = zz.signs || ['NOW DOCKING: MORE GPUS', 'CAPACITY · PLEASE WAIT', 'NO EMPTY RACKS', 'CLOUD PARKING · 1 HR'];
    const neon = ['#3DF5FF', '#FFE14D', '#7DFF8A', '#FF4FD8'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#0C1F4A" />
      <rect x={z.x0} y={f - 1000} width={w} height={1000} fill="#1C3A7A" opacity={0.85} />
      <rect x={z.x0} y={f - 380} width={w} height={380} fill="#3DF5FF" opacity={0.08} />
      {Array.from({length: Math.ceil(w / 70)}, (_, k) => <circle key={'cps' + k} cx={z.x0 + k * 70 + 25 * rnd(k)} cy={f - 1150 + 480 * rnd(k + 5)} r={1.5 + 2 * rnd(k + 9)}
        fill="#FFFFFF" opacity={0.25 + 0.5 * Math.abs(Math.sin(t * (0.7 + rnd(k)) + k))} />)}
      {Array.from({length: 6}, (_, k) => { const cx = z.x0 + ((t * (40 + 12 * k) + k * 700) % (w + 600)) - 300, cy = f - 960 + 90 * k;
        return <g key={'cl' + k} opacity={0.35}><ellipse cx={cx} cy={cy} rx={160} ry={34} fill="#B3E5FC" /><ellipse cx={cx + 60} cy={cy - 22} rx={80} ry={30} fill="#B3E5FC" /></g>; })}
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 80 + k * 420, bw = 240, h = 420 + 160 * rnd(k + 11), top = f - 130 - h;
        return <g key={'dt' + k}>
          {[-1, 1].map((d) => <path key={'st' + d} d={`M ${x + bw / 2 + d * 70} ${f - 130} L ${x + bw / 2 + d * 100} ${f}`} stroke="#90A4AE" strokeWidth={14} />)}
          <rect x={x} y={top} width={bw} height={h} rx={30} fill={['#3A86FF', '#7B61FF', '#2EC4B6'][k % 3]} stroke={OL} strokeWidth={6} />
          {Array.from({length: Math.floor((h - 80) / 52)}, (_, r) => <g key={r}>
            <rect x={x + 24} y={top + 40 + r * 52} width={bw - 48} height={32} rx={8} fill="#0E1633" stroke={OL} strokeWidth={3} />
            {Array.from({length: 7}, (_, q) => { const on = Math.sin(t * (2.5 + rnd(k * 31 + r * 7 + q) * 4) + q + r) > -0.3;
              return <circle key={q} cx={x + 44 + q * ((bw - 88) / 6)} cy={top + 56 + r * 52} r={5} fill={on ? neon[(q + r) % 4] : '#24305C'} />; })}</g>)}
          <g transform={`translate(${x + bw / 2} ${top - 34})`}><circle r={40} fill="#CFD8DC" stroke={OL} strokeWidth={5} />
            <g transform={`rotate(${t * (220 + 80 * busy)})`}>{[0, 120, 240].map((a2) => <path key={a2} d="M 0 0 L 34 -10 L 30 12 Z" fill="#607D8B" transform={`rotate(${a2})`} />)}</g>
            <circle r={8} fill={OL} /></g>
          {k % 2 === 1 && <g transform={`translate(${x + bw / 2} ${top + h * 0.5}) rotate(${-3 + 2 * Math.sin(t * 1.2 + k)})`}>
            <rect x={-160} y={-30} width={320} height={56} rx={28} fill="#081028" stroke={neon[k % 4]} strokeWidth={5} />
            <T x={0} y={10} s={22} c={neon[k % 4]}>{signs[Math.floor(k / 2) % signs.length]}</T></g>}
        </g>; })}
      {Array.from({length: 4 + 2 * busy}, (_, k) => { const span = w + 800, u = ((t * (90 + 20 * k) + k * 610) % span), bx = z.x0 - 400 + u,
          by = f - 760 + 70 * (k % 3) + 26 * Math.sin(t * 1.6 + k), dock = Math.min(1, Math.max(0, (bx - z.x0) / w));
        return <g key={'bl' + k} transform={`translate(${bx} ${by}) rotate(${4 * Math.sin(t * 1.3 + k)})`}>
          <path d={`M 0 40 L ${-60 + 30 * dock} 200`} stroke="#B0BEC5" strokeWidth={3} strokeDasharray="8 8" />
          <ellipse rx={120} ry={56} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
          <ellipse cx={-30} cy={-18} rx={50} ry={14} fill="#FFFFFF" opacity={0.7} />
          <rect x={-60} y={-14} width={120} height={36} rx={8} fill="#14102E" stroke={OL} strokeWidth={4} />
          {Array.from({length: 5}, (_, q) => <rect key={q} x={-50 + q * 22} y={-6} width={14} height={20} rx={3} fill={Math.sin(t * 5 + q + k) > 0 ? neon[q % 4] : '#2A2350'} />)}
          <path d="M 110 -8 L 150 -26 L 150 26 L 110 8 Z" fill="#FF9F1C" stroke={OL} strokeWidth={4} />
        </g>; })}
      <rect x={z.x0} y={f - 20} width={w} height={900} fill="#1A2330" />
      <rect x={z.x0} y={f - 20} width={w} height={60} fill="#263238" />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'dl' + k} x={z.x0 + k * 160} y={f + 6} width={90} height={10} rx={5} fill={busy && Math.sin(t * 8 + k) > 0 ? '#FF4F6B' : '#FFE14D'} opacity={0.7} />)}
    </g>;
  },
  /** FEED CITY (original design, series Before You Buy): a neon town of tall phone-shaped towers whose screens scroll
   *  generic feed cards (avatar dot + bars + a picture block); generic heart / thumb-up / chat bubbles float up; ad
   *  billboards flip between `ads`; an ad-auction ticker runs along the street. `adAt`: ad cards start appearing in feeds.
   *  No real app UI or logos: shapes only. */
  feedcity: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, ads = zz.adAt !== undefined && t >= zz.adAt;
    const signs: string[] = zz.ads || ['YOUR AD HERE · $', 'SCROLL RESPONSIBLY', 'NOW SHOWING: YOU', 'LIKES REDEEMABLE NEVER'];
    const neon = ['#FF4FD8', '#3DF5FF', '#FFE14D', '#7DFF8A', '#FF9F1C'], body = ['#3A86FF', '#7B61FF', '#E71D73', '#2EC4B6'];
    const heart = (s: number, c: string) => <path d={`M 0 ${6 * s} C ${-16 * s} ${-6 * s} ${-8 * s} ${-18 * s} 0 ${-8 * s} C ${8 * s} ${-18 * s} ${16 * s} ${-6 * s} 0 ${6 * s} Z`} fill={c} stroke={OL} strokeWidth={3} />;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#22093F" />
      <rect x={z.x0} y={f - 950} width={w} height={950} fill="#3B1466" opacity={0.85} />
      <rect x={z.x0} y={f - 420} width={w} height={420} fill="#FF4FD8" opacity={0.1} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <circle key={'fcs' + k} cx={z.x0 + k * 60 + 25 * rnd(k + 2)} cy={f - 1150 + 500 * rnd(k + 7)} r={1.5 + 2 * rnd(k)}
        fill="#FFFFFF" opacity={0.3 + 0.5 * Math.abs(Math.sin(t * (0.9 + rnd(k)) + k))} />)}
      {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const x = z.x0 + 70 + k * 360, bw = 230, h = 520 + 180 * rnd(k + 3), top = f - 70 - h, c = body[k % body.length];
        const scr = {x: x + 18, y: top + 50, w: bw - 36, h: h - 110};
        return <g key={'ft' + k}>
          <rect x={x} y={top} width={bw} height={h} rx={40} fill={c} stroke={OL} strokeWidth={6} />
          <rect x={x + bw / 2 - 30} y={top + 16} width={60} height={12} rx={6} fill={OL} />
          <clipPath id={'fcc' + k + '_' + Math.round(z.x0)}><rect x={scr.x} y={scr.y} width={scr.w} height={scr.h} rx={18} /></clipPath>
          <rect x={scr.x} y={scr.y} width={scr.w} height={scr.h} rx={18} fill="#F5F0FF" stroke={OL} strokeWidth={4} />
          <g clipPath={`url(#fcc${k}_${Math.round(z.x0)})`}>
            {Array.from({length: 6}, (_, q) => { const cardH = 150, off = (t * (60 + 25 * rnd(k)) + q * cardH) % (cardH * 6), cy = scr.y + scr.h - off, isAd = ads && (q + k) % 3 === 0;
              return <g key={q} transform={`translate(${scr.x + 10} ${cy})`}>
                <rect x={0} y={0} width={scr.w - 20} height={cardH - 14} rx={12} fill={isAd ? '#FFF3B0' : '#FFFFFF'} stroke={OL} strokeWidth={3} />
                <circle cx={22} cy={22} r={12} fill={neon[(q + k) % 5]} stroke={OL} strokeWidth={2} />
                <rect x={42} y={14} width={scr.w - 90} height={8} rx={4} fill="#B39DDB" /><rect x={42} y={28} width={(scr.w - 90) * 0.6} height={6} rx={3} fill="#D1C4E9" />
                <rect x={10} y={44} width={scr.w - 40} height={cardH - 72} rx={8} fill={isAd ? '#FFB703' : ['#90CAF9', '#A5D6A7', '#F8BBD0'][(q + k) % 3]} />
                {isAd && <T x={(scr.w - 20) / 2} y={44 + (cardH - 72) / 2 + 8} s={22} c={OL}>AD</T>}</g>; })}
          </g>
          {k % 2 === 0 && <g transform={`translate(${x + bw / 2} ${top - 40}) rotate(${-4 + 3 * Math.sin(t * 1.1 + k)})`}>
            <rect x={-160} y={-30} width={320} height={56} rx={28} fill="#14062A" stroke={neon[k % 5]} strokeWidth={5} />
            <T x={0} y={10} s={22} c={neon[k % 5]}>{signs[Math.floor(k / 2) % signs.length]}</T></g>}
        </g>; })}
      {Array.from({length: 14}, (_, k) => { const u = ((t * (0.18 + 0.05 * rnd(k)) + rnd(k + 40)) % 1), bx = z.x0 + rnd(k + 13) * w + 30 * Math.sin(t * 2 + k), by = f - 80 - u * 900;
        const kind = k % 3, c = neon[k % 5];
        return <g key={'fl' + k} transform={`translate(${bx} ${by}) scale(${1 + 0.3 * Math.sin(t * 4 + k)})`} opacity={1 - u}>
          {kind === 0 ? heart(2, c) : kind === 1 ? <g><rect x={-18} y={-16} width={36} height={26} rx={10} fill={c} stroke={OL} strokeWidth={3} /><path d="M -6 10 L -12 20 L 4 10 Z" fill={c} stroke={OL} strokeWidth={3} /></g>
            : <g><rect x={-10} y={-4} width={18} height={20} rx={4} fill={c} stroke={OL} strokeWidth={3} /><rect x={-4} y={-20} width={10} height={20} rx={4} fill={c} stroke={OL} strokeWidth={3} /></g>}
        </g>; })}
      <rect x={z.x0} y={f - 70} width={w} height={900} fill="#14062A" />
      <g>{(() => { const SP_ = 380, n = Math.ceil((w + 760) / SP_), P_ = n * SP_; return Array.from({length: n}, (_, k) => { const tx = z.x0 - 380 + ((k * SP_ - t * 160) % P_ + P_) % P_;
        return <T key={'tk' + k} x={tx} y={f - 26} s={22} c={neon[k % 5]}>{['AD SLOT SOLD', 'PRICE PER AD ↑', 'IMPRESSIONS ↑', 'BID · BID · BID'][k % 4]}</T>; }); })()}</g>
    </g>;
  },
  chipcity: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, dim = zz.dimAt !== undefined ? clamp((t - zz.dimAt) / 1.6) : 0;
    const flick = dim > 0 && dim < 1 ? (Math.sin(t * 47) > 0 ? 1 : 0.35) : 1, glow = (1 - 0.65 * dim) * flick;
    const signs: string[] = zz.signs || ['GPU PARKING ONLY', 'NO TENSORS AFTER 9 PM', 'COOLING TOWER · STAY CHILL', 'NOW HIRING: MORE CORES', 'CACHE ONLY · NO CHECKS', 'FAB-ULOUS DINER'];
    const neon = ['#FF4FD8', '#3DF5FF', '#FFE14D', '#7DFF8A'], body = ['#2EC4B6', '#FF9F1C', '#7B61FF', '#E71D73', '#3A86FF'];
    const tubeY = (x: number) => f - 330 + 60 * Math.sin((x - z.x0) / 380);
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#1B0B3F" />
      <rect x={z.x0} y={f - 900} width={w} height={900} fill="#341A6B" opacity={0.85} />
      <rect x={z.x0} y={f - 420} width={w} height={420} fill="#FF6EC7" opacity={0.14 * glow} />
      {Array.from({length: Math.ceil(w / 55)}, (_, k) => <circle key={'cs' + k} cx={z.x0 + k * 55 + 30 * rnd(k)} cy={f - 1150 + 520 * rnd(k + 3)} r={1.5 + 2 * rnd(k + 8)}
        fill="#FFFFFF" opacity={0.3 + 0.6 * Math.abs(Math.sin(t * (0.8 + rnd(k)) + k))} />)}
      <g transform={`translate(${z.x0 + w * 0.82} ${f - 960})`}>
        <circle r={110} fill="#FFE9B0" stroke={OL} strokeWidth={6} />
        <circle cx={-34} cy={-20} r={20} fill="#F2CF7E" /><circle cx={30} cy={34} r={14} fill="#F2CF7E" /><circle cx={40} cy={-40} r={9} fill="#F2CF7E" />
      </g>
      {Array.from({length: Math.ceil(w / 150)}, (_, k) => { const x = z.x0 + k * 150, h = 220 + 200 * rnd(k + 21);
        return <path key={'bk' + k} d={`M ${x} ${f - 120} L ${x} ${f - 120 - h} Q ${x + 65} ${f - 170 - h} ${x + 130} ${f - 120 - h} L ${x + 130} ${f - 120} Z`} fill="#2A1658" />; })}
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const x = z.x0 + 60 + k * 380, bw = 210 + 50 * rnd(k + 2), h = 380 + 260 * rnd(k + 5), c = body[k % body.length], top = f - 60 - h;
        return <g key={'ct' + k}>
          <rect x={x} y={top} width={bw} height={h} rx={26} fill={c} stroke={OL} strokeWidth={6} />
          {Array.from({length: Math.floor((h - 60) / 46)}, (_, r) => <g key={r}>
            <rect x={x - 22} y={top + 40 + r * 46} width={24} height={14} rx={3} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
            <rect x={x + bw - 2} y={top + 40 + r * 46} width={24} height={14} rx={3} fill="#CFD8DC" stroke={OL} strokeWidth={3} /></g>)}
          <rect x={x + bw * 0.2} y={top + h * 0.18} width={bw * 0.6} height={bw * 0.6} rx={12} fill="#14102E" stroke={OL} strokeWidth={5} />
          {Array.from({length: 16}, (_, q) => { const on = Math.sin(t * (2 + rnd(k * 16 + q) * 3) + q) > -0.2;
            return <rect key={'d' + q} x={x + bw * 0.24 + (q % 4) * bw * 0.135} y={top + h * 0.18 + bw * 0.04 + Math.floor(q / 4) * bw * 0.135} width={bw * 0.1} height={bw * 0.1} rx={3}
              fill={on ? neon[(k + q) % 4] : '#2A2350'} opacity={on ? glow : 1} />; })}
          {Array.from({length: Math.floor((h * 0.5) / 56)}, (_, r) => Array.from({length: 3}, (_, q) =>
            <rect key={'w' + r + q} x={x + 26 + q * (bw - 52) / 3 + 4} y={top + h * 0.18 + bw * 0.66 + r * 56} width={(bw - 52) / 3 - 10} height={30} rx={8}
              fill={rnd(k * 97 + r * 7 + q) > 0.35 ? '#FFF3B0' : '#1B1440'} opacity={0.4 + 0.6 * glow} stroke={OL} strokeWidth={3} />))}
          <ellipse cx={x + bw / 2} cy={top + 6} rx={bw * 0.62} ry={22} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
          <path d={`M ${x + bw / 2} ${top - 16} L ${x + bw / 2} ${top - 90}`} stroke={OL} strokeWidth={6} />
          <circle cx={x + bw / 2} cy={top - 96} r={13} fill={Math.sin(t * 4 + k) > 0 ? '#FF4F6B' : '#5A1020'} stroke={OL} strokeWidth={4} />
          {k % 2 === 0 && <g transform={`translate(${x + bw / 2} ${top + h * 0.1}) rotate(${-4 + 3 * Math.sin(t * 1.3 + k)})`}>
            <rect x={-150} y={-30} width={300} height={56} rx={28} fill="#120A2A" stroke={neon[k % 4]} strokeWidth={5} opacity={glow} />
            <T x={0} y={10} s={24} c={neon[k % 4]} o={glow}>{signs[Math.floor(k / 2) % signs.length]}</T></g>}
        </g>; })}
      <path d={Array.from({length: Math.ceil(w / 40) + 1}, (_, k) => `${k ? 'L' : 'M'} ${z.x0 + k * 40} ${tubeY(z.x0 + k * 40)}`).join(' ')} fill="none" stroke="#B3E5FC" strokeWidth={46} opacity={0.3} />
      <path d={Array.from({length: Math.ceil(w / 40) + 1}, (_, k) => `${k ? 'L' : 'M'} ${z.x0 + k * 40} ${tubeY(z.x0 + k * 40) - 23}`).join(' ')} fill="none" stroke={OL} strokeWidth={4} />
      <path d={Array.from({length: Math.ceil(w / 40) + 1}, (_, k) => `${k ? 'L' : 'M'} ${z.x0 + k * 40} ${tubeY(z.x0 + k * 40) + 23}`).join(' ')} fill="none" stroke={OL} strokeWidth={4} />
      {Array.from({length: 4}, (_, k) => { const cx2 = z.x0 + ((t * 700 + k * 900) % (w + 200)) - 100;
        return <g key={'cap' + k} transform={`translate(${cx2} ${tubeY(cx2)})`}><rect x={-46} y={-16} width={92} height={32} rx={16} fill="#FFE14D" stroke={OL} strokeWidth={4} />
          <rect x={-30} y={-9} width={24} height={14} rx={4} fill="#3DF5FF" /><rect x={4} y={-9} width={24} height={14} rx={4} fill="#3DF5FF" /></g>; })}
      {Array.from({length: 5}, (_, k) => { const dir = k % 2 ? -1 : 1, sp = 180 + 70 * k, span = w + 600;
        const u = ((t * sp + k * 830) % span), cx2 = dir > 0 ? z.x0 - 300 + u : z.x1 + 300 - u, cy2 = f - 700 + k * 85 + 18 * Math.sin(t * 2.2 + k);
        const cc = ['#FF4F6B', '#FFE14D', '#3DF5FF', '#7DFF8A', '#FF9F1C'][k];
        return <g key={'fc' + k} transform={`translate(${cx2} ${cy2}) scale(${dir} 1) rotate(${4 * Math.sin(t * 3 + k)})`}>
          {[0, 1, 2].map((p) => <circle key={p} cx={-90 - p * 26 - ((t * 60) % 26)} cy={6} r={9 - p * 2} fill="#FFFFFF" opacity={0.5 - p * 0.15} />)}
          <path d="M -80 10 Q -70 -18 -20 -20 L 50 -20 Q 92 -16 96 8 Q 70 26 -60 24 Q -84 22 -80 10 Z" fill={cc} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <path d="M -24 -20 Q 6 -62 40 -20 Z" fill="#B3E5FC" opacity={0.8} stroke={OL} strokeWidth={4} />
          <path d="M -80 6 L -100 -18 L -66 -6 Z" fill={cc} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <ellipse cx={10} cy={30} rx={46} ry={6} fill="#3DF5FF" opacity={0.5} /></g>; })}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#3A2470" stroke={OL} strokeWidth={5} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#1E1040" />
      {Array.from({length: Math.ceil(w / 140)}, (_, k) => <rect key={'nl' + k} x={z.x0 + k * 140} y={f + 110} width={70} height={8} rx={4} fill="#3DF5FF" opacity={0.5 * glow} />)}
    </g>;
  },
  /** A sea route at dusk (original design): layered sky, distant hills, a choppy sea with waves, gulls, and a striped
   *  CHECKPOINT BUOY (`buoyAt`, fraction of the width) with a rotating lamp and a sweeping searchlight; its sign reads
   *  `sign` (default "EXPORT RULES CHECKPOINT"). `night`: darker sky and a stronger beam. */
  searoute: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, night = !!z.night, bx = z.x0 + w * (zz.buoyAt ?? 0.62), sea = f - 240;
    const sweep = Math.sin(t * 0.9) * 32 - 8, bob = 10 * Math.sin(t * 2.1);
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + sea} fill={night ? '#120E2E' : '#FF9E6B'} />
      <rect x={z.x0} y={sea - 520} width={w} height={520} fill={night ? '#2B1B55' : '#FFC27A'} />
      <rect x={z.x0} y={sea - 200} width={w} height={200} fill={night ? '#3E2A6E' : '#FFD9A0'} />
      <circle cx={z.x0 + w * 0.25} cy={sea - 60} r={130} fill={night ? '#F5F1D0' : '#FFF1C1'} opacity={0.9} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <path key={'hl' + k} d={`M ${z.x0 + k * 260 - 40} ${sea} Q ${z.x0 + k * 260 + 90} ${sea - 70 - 60 * rnd(k + 4)} ${z.x0 + k * 260 + 230} ${sea} Z`}
        fill={night ? '#241640' : '#C9746A'} opacity={0.9} />)}
      <rect x={z.x0} y={sea} width={w} height={2600} fill={night ? '#103A6B' : '#1E7FD8'} />
      {Array.from({length: 5}, (_, r) => Array.from({length: Math.ceil(w / 150) + 1}, (_, k) =>
        <path key={'wv' + r + '-' + k} d={`M ${z.x0 + k * 150 + 40 * Math.sin(t * (1 + r * 0.3) + k + r)} ${sea + 40 + r * 70} q 25 -14 50 0 q 25 14 50 0`} fill="none" stroke="#FFFFFF" strokeWidth={4} opacity={0.35 + 0.1 * r} />))}
      {Array.from({length: 4}, (_, k) => { const gx = z.x0 + ((t * (60 + 20 * k) + k * 600) % w), gy = sea - 420 + 70 * k + 20 * Math.sin(t * 3 + k);
        return <path key={'gl' + k} d={`M ${gx - 22} ${gy} q 11 ${-12 - 6 * Math.sin(t * 9 + k)} 22 0 q 11 ${-12 - 6 * Math.sin(t * 9 + k)} 22 0`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />; })}
      <g transform={`translate(${bx} ${sea + 30 + bob})`}>
        <path d="M 0 -250 L -1100 -90 L -1100 190 Z" fill="#FFF59D" opacity={night ? 0.32 : 0.2} transform={`rotate(${sweep} 0 -250)`} />
        <path d="M -80 40 L -60 -120 L 60 -120 L 80 40 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <path d="M -73 -20 L 73 -20 L 70 0 L -70 0 Z M -66 -80 L 66 -80 L 64 -60 L -64 -60 Z" fill="#E53935" />
        <rect x={-30} y={-210} width={60} height={90} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
        <circle cx={0} cy={-250} r={34} fill={Math.sin(t * 5) > 0 ? '#FFEB3B' : '#FFA000'} stroke={OL} strokeWidth={5} />
        <path d="M -40 -284 L 40 -284 L 0 -320 Z" fill="#E53935" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <g transform={`translate(0 -400) rotate(${3 * Math.sin(t * 1.7)})`}>
          <path d="M 0 60 L 0 110" stroke={OL} strokeWidth={6} />
          <rect x={-250} y={-40} width={500} height={100} rx={14} fill="#FFF8E1" stroke={OL} strokeWidth={6} />
          <T x={0} y={8} s={32}>{zz.sign || 'EXPORT RULES CHECKPOINT'}</T>
          <T x={0} y={44} s={20} c="#5D4037" w={700}>{zz.sub || 'PLEASE HAVE YOUR LICENSE READY'}</T></g>
      </g>
    </g>;
  },
  /** A closed-door BRIEFING ROOM (original design): dark wood panels with rivets, a giant round chrome vault door (spoked
   *  wheel spins from `spinAt`), an IN SESSION light, joke house-rule signs, a long table with empty chairs and a cactus.
   *  `doorAt`: fraction of the width for the door. */
  secretroom: (t, z, f) => {
    const w = z.x1 - z.x0, zz = z as any, dx = z.x0 + w * (zz.doorAt ?? 0.5), spin = zz.spinAt !== undefined ? Math.max(0, t - zz.spinAt) * 120 : 0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#2B1D16" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <g key={'pn' + k}>
        <rect x={z.x0 + k * 200 + 10} y={f - 760} width={180} height={700} rx={10} fill="#4E342E" stroke={OL} strokeWidth={5} />
        {[0, 1].map((q) => <rect key={q} x={z.x0 + k * 200 + 30} y={f - 730 + q * 340} width={140} height={300} rx={8} fill="#5D4037" stroke={OL} strokeWidth={3} />)}</g>)}
      <rect x={z.x0} y={f - 800} width={w} height={40} fill="#3E2723" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <g key={'lp' + k} transform={`translate(${z.x0 + 150 + k * 300} ${f - 760})`}>
        <path d="M -60 0 L 60 0 L 30 40 L -30 40 Z" fill="#FFCA28" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <path d="M -30 40 L -110 300 L 110 300 L 30 40 Z" fill="#FFE082" opacity={0.08} /></g>)}
      <g transform={`translate(${dx} ${f - 380})`}>
        <circle r={300} fill="#455A64" stroke={OL} strokeWidth={8} />
        <circle r={262} fill="#CFD8DC" stroke={OL} strokeWidth={7} />
        {Array.from({length: 16}, (_, k) => <circle key={k} cx={236 * Math.cos(k * Math.PI / 8)} cy={236 * Math.sin(k * Math.PI / 8)} r={11} fill="#90A4AE" stroke={OL} strokeWidth={3} />)}
        <circle r={190} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
        <g transform={`rotate(${spin})`}>
          {[0, 1, 2].map((k) => <rect key={k} x={-150} y={-12} width={300} height={24} rx={12} fill="#78909C" stroke={OL} strokeWidth={4} transform={`rotate(${k * 60})`} />)}
          <circle r={52} fill="#546E7A" stroke={OL} strokeWidth={5} /></g>
        <path d="M -80 -150 Q 0 -120 80 -150" fill="none" stroke="#FFFFFF" strokeWidth={8} opacity={0.4} strokeLinecap="round" />
      </g>
      <g transform={`translate(${dx} ${f - 740})`}>
        <rect x={-210} y={-34} width={420} height={60} rx={12} fill="#1B0F0B" stroke="#FF5252" strokeWidth={4} />
        <T x={-30} y={8} s={26} c="#FF8A80">{zz.title || 'CLOSED-DOOR BRIEFING'}</T>
        <circle cx={170} cy={-4} r={14} fill={Math.sin(t * 4) > 0 ? '#FF1744' : '#5D0A0A'} stroke={OL} strokeWidth={3} /></g>
      {[[-560, 'NO PHONES'], [-560, 'NO SNACKS'], [560, 'NO LEAKS'], [560, 'WHISPER ONLY']].map(([o, s], k) =>
        <g key={'rs' + k} transform={`translate(${dx + (o as number)} ${f - 620 + (k % 2) * 110}) rotate(${(k % 2 ? 3 : -3) + 1.5 * Math.sin(t + k)})`}>
          <rect x={-120} y={-34} width={240} height={64} rx={8} fill="#FFF8E1" stroke={OL} strokeWidth={4} />
          <T x={0} y={10} s={26}>{s as string}</T></g>)}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#3E2723" />
      <rect x={z.x0} y={f} width={w} height={600} fill="#6D1B1B" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <rect key={'cp' + k} x={z.x0 + k * 90} y={f} width={4} height={600} fill="#000000" opacity={0.12} />)}
      <g transform={`translate(${dx} ${f + 40})`}>
        <rect x={-520} y={-40} width={1040} height={60} rx={14} fill="#8D6E63" stroke={OL} strokeWidth={5} />
        {Array.from({length: 7}, (_, k) => <g key={'ch' + k} transform={`translate(${-450 + k * 150} -40)`}>
          <rect x={-40} y={-120} width={80} height={110} rx={20} fill="#212121" stroke={OL} strokeWidth={4} /></g>)}
        <g transform="translate(470 -40)"><rect x={-24} y={-20} width={48} height={30} fill="#A1887F" stroke={OL} strokeWidth={3} />
          <path d="M 0 -20 L 0 -90 M 0 -60 L -20 -70 L -20 -90 M 0 -50 L 18 -58 L 18 -76" stroke="#43A047" strokeWidth={12} strokeLinecap="round" fill="none" /></g>
      </g>
    </g>;
  },
  /** A hospital corridor: pale mint walls, numbered doors with small windows, a handrail, ceiling light panels, a glossy
   *  tiled floor; `night` dims it to an evening shift. Generic, no real hospital branding. */
  hospital: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill={night ? '#3C5A5A' : '#DDF0EA'} />
      <rect x={z.x0} y={f - 360} width={w} height={360} fill={night ? '#355050' : '#C8E6DE'} />
      <rect x={z.x0} y={f - 380} width={w} height={20} fill="#9CCFC3" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f - 190} width={w} height={14} rx={7} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 80 + k * 420;
        return <g key={'hd' + k}>
          <rect x={x} y={f - 560} width={200} height={560} fill={night ? '#6E8E8A' : '#F5FBF9'} stroke={OL} strokeWidth={4} />
          <rect x={x + 60} y={f - 500} width={80} height={110} fill="#BFE8FF" stroke={OL} strokeWidth={3} />
          <circle cx={x + 170} cy={f - 280} r={9} fill="#90A4AE" stroke={OL} strokeWidth={2} />
          <rect x={x + 40} y={f - 620} width={120} height={40} rx={8} fill="#2E7D74" stroke={OL} strokeWidth={3} />
          <T x={x + 100} y={f - 591} s={24} c="#FFFFFF">{'ROOM ' + (101 + k)}</T></g>; })}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'hl' + k} x={z.x0 + 60 + k * 300} y={f - 900} width={180} height={22} rx={6} fill={night ? '#C9E8FF' : '#FFFFFF'} opacity={0.9} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#4E6B68' : '#E9F3F1'} />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ht' + k} x={z.x0 + k * 120} y={f} width={3} height={600} fill={OL} opacity={0.08} />)}
      <rect x={z.x0} y={f + 30} width={w} height={8} fill="#FFFFFF" opacity={0.4} />
    </g>;
  },
  /** Financial district at night: dark glass towers with lit windows, a distant skyline, wet street with reflections. */
  district: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#0E1424" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => { const x = z.x0 + k * 120, h = 260 + 220 * rnd(k + 40);
        return <rect key={'bg' + k} x={x} y={f - 140 - h} width={110} height={h} fill="#141C30" />; })}
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => { const x = z.x0 + 40 + k * 340, h = 420 + 320 * rnd(k + 7), bw = 200 + 60 * rnd(k + 2);
        return <g key={'tw' + k}>
          <rect x={x} y={f - 60 - h} width={bw} height={h} fill={['#1B2640', '#202B47', '#18223A'][k % 3]} stroke="#2E3B5C" strokeWidth={3} />
          <path d={`M ${x} ${f - 60 - h} L ${x + bw} ${f - 60 - h} L ${x + bw * 0.7} ${f - 60 - h - 50} L ${x + bw * 0.3} ${f - 60 - h - 50} Z`} fill="#1B2640" stroke="#2E3B5C" strokeWidth={3} />
          {Array.from({length: Math.floor(h / 44)}, (_, r) => Array.from({length: Math.floor(bw / 34)}, (_, c) => {
            const on = rnd(k * 131 + r * 17 + c) > 0.55; const fl = on && rnd(k + r + c + Math.floor(t * 0.5)) > 0.97;
            return <rect key={r + '-' + c} x={x + 10 + c * 34} y={f - 40 - h + 20 + r * 44} width={20} height={24} fill={on ? (fl ? '#FFFFFF' : '#F2C76E') : '#26324F'} opacity={on ? 0.85 : 1} />; }))}
        </g>; })}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#0A0F1C" />
      <rect x={z.x0} y={f} width={w} height={600} fill="#0B111F" />
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => <rect key={'rf' + k} x={z.x0 + 60 + k * 340} y={f + 10} width={160} height={120 + 40 * rnd(k)} fill="#F2C76E" opacity={0.06} />)}
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 160} y={f + 150} width={80} height={6} fill="#C9D2E0" opacity={0.25} />)}
    </g>;
  },
  /** A state parliament chamber: curved rows of benches, a speaker's desk, tall windows, a public gallery. */
  parliament: (t, z, f) => {
    const w = z.x1 - z.x0, cx = (z as any).cx ?? z.x0 + w / 2;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#E8E2D6" />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <g key={'wn' + k}><rect x={z.x0 + 60 + k * 260} y={f - 720} width={120} height={360} rx={60} fill="#BFD3E6" stroke={OL} strokeWidth={4} />
        <path d={`M ${z.x0 + 120 + k * 260} ${f - 720} L ${z.x0 + 120 + k * 260} ${f - 360}`} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f - 340} width={w} height={18} fill="#8D6E63" />
      <rect x={cx - 180} y={f - 300} width={360} height={140} fill="#6D4C41" stroke={OL} strokeWidth={5} />
      <rect x={cx - 40} y={f - 360} width={80} height={60} fill="#8D6E63" stroke={OL} strokeWidth={4} />
      {[0, 1, 2].map((r) => <path key={r} d={`M ${cx - 860 + r * 90} ${f - 40 - r * 40} Q ${cx} ${f - 200 - r * 40} ${cx + 860 - r * 90} ${f - 40 - r * 40}`} fill="none" stroke="#5D4037" strokeWidth={28} />)}
      {Array.from({length: 26}, (_, k) => { const r = k % 3, u = (Math.floor(k / 3) + 0.5) / 9, x = cx - 800 + r * 90 + u * (1600 - r * 180), y = f - 70 - r * 40 - Math.sin(u * Math.PI) * 120;
        return <circle key={k} cx={x} cy={y - 26} r={16} fill={K.skin[k % 4]} stroke={OL} strokeWidth={3} />; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#7B5E57" />
    </g>;
  },
  /** Car plant interior: steel trusses, orange welding robots with sparks in the back. */
  carplant: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#DCE3EA" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'tr' + k} d={`M ${z.x0 + k * 200} 60 L ${z.x0 + k * 200 + 100} 0 L ${z.x0 + k * 200 + 200} 60 M ${z.x0 + k * 200} 60 L ${z.x0 + k * 200 + 200} 60`} fill="none" stroke="#90A4AE" strokeWidth={8} />)}
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => { const x = z.x0 + 200 + k * 520, a1 = Math.sin(t * 2 + k) * 18, on = (z as any).idle === undefined || t < (z as any).idle;
        return <g key={'rb' + k} transform={`translate(${x} ${f - 260})`}>
          <rect x={-40} y={150} width={80} height={110} fill="#FF8F00" stroke={OL} strokeWidth={4} />
          <g transform={`rotate(${on ? a1 - 30 : -60} 0 150)`}><rect x={-14} y={30} width={28} height={130} rx={10} fill="#FFA726" stroke={OL} strokeWidth={4} />
            <g transform={`rotate(${on ? -a1 + 60 : 20} 0 30)`}><rect x={-12} y={-70} width={24} height={110} rx={10} fill="#FFA726" stroke={OL} strokeWidth={4} />
              {on && Math.sin(t * 9 + k) > 0.2 && Array.from({length: 5}, (_, j) => <path key={j} d={`M 0 -74 l ${Math.cos(j + t * 20) * 26} ${Math.sin(j + t * 20) * 26}`} stroke={K.gold} strokeWidth={4} />)}</g></g>
        </g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#9EA9B5" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'st' + k} d={`M ${z.x0 + k * 90} ${f + 20} l 40 0`} stroke="#FFC93C" strokeWidth={8} />)}
    </g>;
  },
  /** Data center: rows of server racks with blinking LEDs, cool blue light, raised floor. */
  datacenter: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#1F2B47" />
      {Array.from({length: Math.ceil(w / 150)}, (_, k) => { const x = z.x0 + 20 + k * 150, dark = (z as any).darkAt !== undefined && t >= (z as any).darkAt;
        return <g key={'rk' + k}><rect x={x} y={f - 420} width={120} height={420} rx={6} fill="#2E3B5E" stroke={OL} strokeWidth={4} />
          {Array.from({length: 12}, (_, r) => <g key={r}><rect x={x + 10} y={f - 404 + r * 33} width={100} height={24} rx={3} fill="#3D4D75" />
            {[0, 1, 2].map((d) => <circle key={d} cx={x + 22 + d * 14} cy={f - 392 + r * 33} r={4} fill={dark ? '#4A5675' : Math.sin(t * (6 + d) + r * 1.3 + k) > 0 ? ['#7DF29A', '#7DF9FF', '#FFC93C'][d] : '#4A5675'} />)}</g>)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#3D4D75" />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <rect key={'tl' + k} x={z.x0 + k * 80} y={f} width={76} height={600} fill="none" stroke="#2E3B5E" strokeWidth={3} />)}
    </g>;
  },
  /** Construction site: dirt lot, fence, traffic cones, hills behind. */
  /** Low Earth orbit: black space with twinkling stars and the blue curve of the Earth (with a sunrise rim) below. */
  orbit: (t, z, f) => {
    const w = z.x1 - z.x0, cx = (z.x0 + z.x1) / 2;
    return <g>
      <rect x={z.x0} y={-1600} width={w} height={f + 2400} fill="#030712" />
      {Array.from({length: Math.ceil(w / 40)}, (_, k) => <circle key={'st' + k} cx={z.x0 + k * 40 + 30 * rnd(k)} cy={-300 + 1000 * rnd(k + 3)} r={1.5 + 2 * rnd(k + 7)}
        fill="#FFFFFF" opacity={0.35 + 0.6 * Math.abs(Math.sin(t * (0.6 + rnd(k)) + k))} />)}
      <ellipse cx={cx} cy={f + 2600} rx={Math.max(w, 3000)} ry={2700} fill="#1565C0" />
      <ellipse cx={cx} cy={f + 2600} rx={Math.max(w, 3000)} ry={2700} fill="none" stroke="#81D4FA" strokeWidth={26} opacity={0.6} />
      {Array.from({length: 7}, (_, k) => <ellipse key={'cl' + k} cx={z.x0 + ((k * 520 + t * 12) % w)} cy={f + 40 + 40 * rnd(k)} rx={160} ry={26} fill="#FFFFFF" opacity={0.35} />)}
    </g>;
  },
  site: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <path d={`M ${z.x0} ${f - 120} ${Array.from({length: Math.ceil(w / 400) + 1}, (_, k) => `Q ${z.x0 + k * 400 + 200} ${f - 260 - 60 * rnd(k + 5)} ${z.x0 + k * 400 + 400} ${f - 130}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#9CCC65" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#B98B5E" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <circle key={'pb' + k} cx={z.x0 + k * 60 + 30 * rnd(k)} cy={f + 40 + 160 * rnd(k + 9)} r={5} fill="#8D6E63" />)}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => <g key={'cn' + k} transform={`translate(${z.x0 + 80 + k * 700} ${f + 6})`}>
        <path d="M -20 0 L 0 -50 L 20 0 Z" fill="#FF7043" stroke={OL} strokeWidth={3} /><rect x={-11} y={-30} width={22} height={8} fill={K.white} /></g>)}
    </g>;
  },
  /** Caribbean beach: turquoise sea on the horizon, white sand, pastel houses on stilts, palms, a beach umbrella, a little sailboat. */
  beach: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const boatX = z.x0 + ((t * 40) % (w + 400)) - 200;
    return <g>
      <rect x={z.x0} y={f - 300} width={w} height={300} fill={night ? '#1F5B7A' : '#2EC4D6'} />
      <rect x={z.x0} y={f - 300} width={w} height={60} fill={night ? '#2A6E8E' : '#7FE3EC'} opacity={0.7} />
      {Array.from({length: Math.ceil(w / 70)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 70 + 20 * Math.sin(t + k)} ${f - 230 + 50 * rnd(k)} q 15 -8 30 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.7} />)}
      <g transform={`translate(${boatX} ${f - 250})`}><path d="M -50 0 L 50 0 L 36 20 L -36 20 Z" fill={K.white} stroke={OL} strokeWidth={3} />
        <path d="M 0 0 L 0 -90 L 46 -10 Z" fill="#FF8A65" stroke={OL} strokeWidth={3} strokeLinejoin="round" /></g>
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => { const x = z.x0 + 120 + k * 520, c = ['#FFCDD2', '#B3E5FC', '#FFF59D', '#C8E6C9', '#E1BEE7'][k % 5];
        return <g key={'hs' + k} transform={`translate(${x} ${f - 110})`}>
          <rect x={-70} y={-110} width={140} height={110} fill={c} stroke={OL} strokeWidth={4} />
          <path d="M -86 -110 L 0 -170 L 86 -110 Z" fill={['#E53935', '#1E88E5', '#43A047'][k % 3]} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <rect x={-46} y={-80} width={34} height={34} rx={3} fill={night ? '#FFE08A' : '#FFFFFF'} stroke={OL} strokeWidth={3} />
          <rect x={14} y={-70} width={34} height={70} rx={3} fill={K.wood2} stroke={OL} strokeWidth={3} />
          {[-56, 56].map((dx) => <rect key={dx} x={dx - 6} y={0} width={12} height={110} fill={K.wood} stroke={OL} strokeWidth={2} />)}</g>; })}
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const x = z.x0 + 330 + k * 380, sw = Math.sin(t * 1.5 + k) * 8;
        return <g key={'pm' + k} transform={`translate(${x} ${f + 20})`}>
          <path d={`M 0 0 Q ${-14 + sw * 0.3} -110 ${sw} -230`} fill="none" stroke="#8A5A2B" strokeWidth={15} strokeLinecap="round" />
          {[-160, -110, -50, 10, 60].map((a, i) => <path key={i} d={`M ${sw} -230 q ${Math.cos(a * Math.PI / 180) * 70} ${Math.sin(a * Math.PI / 180) * 70 - 24} ${Math.cos(a * Math.PI / 180) * 130} ${Math.sin(a * Math.PI / 180) * 130 + 36}`}
            fill="none" stroke="#2E9E5B" strokeWidth={18} strokeLinecap="round" />)}
          <circle cx={sw - 8} cy={-222} r={10} fill="#8D6E63" stroke={OL} strokeWidth={2} /></g>; })}
      <path d={`M ${z.x0} ${f} ${Array.from({length: Math.ceil(w / 60) + 1}, (_, k) => `L ${z.x0 + k * 60} ${f - 6 * Math.sin(k + t * 2)}`).join(' ')} L ${z.x1} ${f + 600} L ${z.x0} ${f + 600} Z`} fill="#F8E3B0" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <circle key={'sd' + k} cx={z.x0 + k * 90 + 40 * rnd(k)} cy={f + 50 + 150 * rnd(k + 3)} r={4} fill="#E3C27E" />)}
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => <g key={'um' + k} transform={`translate(${z.x0 + 600 + k * 900} ${f + 120})`}>
        <path d="M 0 0 L 0 -150" stroke={OL} strokeWidth={6} />
        <path d="M -110 -140 Q 0 -230 110 -140 Z" fill={['#FF7043', '#29B6F6'][k % 2]} stroke={OL} strokeWidth={4} />
        <path d="M -40 -140 Q 0 -230 40 -140" fill="none" stroke={K.white} strokeWidth={10} /></g>)}
    </g>;
  },
  /** Cartoon internet: a soft lavender space with a dotted grid, floating cursors, links and little cloud icons. */
  web: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={-3000} width={w} height={6000} fill="#EDE7FF" />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => Array.from({length: 20}, (_, r) => <circle key={k + '-' + r} cx={z.x0 + k * 80} cy={-300 + r * 80} r={3} fill="#B39DDB" opacity={0.6} />))}
      {Array.from({length: 10}, (_, k) => { const x = z.x0 + rnd(k) * w + Math.sin(t * 0.8 + k) * 30, y = 100 + rnd(k + 4) * 700 + Math.cos(t * 0.7 + k) * 20, ty = k % 3;
        return <g key={'ic' + k} transform={`translate(${x} ${y})`} opacity={0.55}>
          {ty === 0 && <path d="M 0 0 L 0 40 L 10 30 L 18 46 L 24 43 L 16 28 L 30 28 Z" fill={K.white} stroke={OL} strokeWidth={3} strokeLinejoin="round" />}
          {ty === 1 && <g><rect x={-30} y={-12} width={34} height={24} rx={12} fill="none" stroke="#7E57C2" strokeWidth={6} /><rect x={-4} y={-12} width={34} height={24} rx={12} fill="none" stroke="#7E57C2" strokeWidth={6} /></g>}
          {ty === 2 && <T x={0} y={10} s={34} c="#7E57C2">www</T>}</g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill="#D1C4E9" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'gl' + k} d={`M ${z.x0 + k * 120} ${f} L ${z.x0 + k * 120 - 200} ${f + 600}`} stroke="#B39DDB" strokeWidth={3} />)}
    </g>;
  },
  /** Container port: distant hills, a concrete quay with stacked boxes and gantry cranes whose trolleys lift boxes; water in front. */
  port: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, q = f - 120;
    return <g>
      <path d={`M ${z.x0} ${q - 120} ${Array.from({length: Math.ceil(w / 500) + 1}, (_, k) => `Q ${z.x0 + k * 500 + 250} ${q - 260 - 60 * rnd(k + 21)} ${z.x0 + k * 500 + 500} ${q - 130}`).join(' ')} L ${z.x1} ${q} L ${z.x0} ${q} Z`} fill={night ? '#3A4A70' : '#A5C8E4'} stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={q} width={w} height={120} fill="#B0B7C3" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const x = z.x0 + 30 + k * 260; if (k % 3 === 2) return null;
        return <g key={'cs' + k}>{Array.from({length: 3}, (_, r) => Array.from({length: 2}, (_, c2) => <rect key={r + '-' + c2} x={x + c2 * 104} y={q - 46 - r * 46} width={100} height={44} rx={3}
          fill={['#E53935', '#1E88E5', '#FFB300', '#43A047', '#8E24AA', '#F4511E'][(k * 5 + r * 2 + c2) % 6]} stroke={OL} strokeWidth={3} />))}</g>; })}
      {Array.from({length: Math.ceil(w / 780)}, (_, k) => { const x = z.x0 + 520 + k * 780, tr = 160 * Math.sin(t * 0.5 + k * 2), lift = 120 + 100 * Math.sin(t * 0.9 + k);
        return <g key={'gc' + k}>
          <path d={`M ${x - 80} ${q} L ${x - 80} ${q - 460} M ${x + 80} ${q} L ${x + 80} ${q - 460} M ${x - 80} ${q - 300} L ${x + 80} ${q - 300}`} stroke={['#E53935', '#1E7FD8'][k % 2]} strokeWidth={16} strokeLinecap="round" />
          <path d={`M ${x - 200} ${q - 460} L ${x + 380} ${q - 460}`} stroke={['#E53935', '#1E7FD8'][k % 2]} strokeWidth={20} strokeLinecap="round" />
          <path d={`M ${x} ${q - 560} L ${x - 200} ${q - 460} M ${x} ${q - 560} L ${x + 380} ${q - 460}`} stroke={OL} strokeWidth={3} />
          <rect x={x + 120 + tr - 30} y={q - 480} width={60} height={30} fill="#FFC93C" stroke={OL} strokeWidth={3} />
          <path d={`M ${x + 120 + tr} ${q - 450} L ${x + 120 + tr} ${q - 460 + lift}`} stroke={OL} strokeWidth={3} />
          <rect x={x + 70 + tr} y={q - 460 + lift} width={100} height={44} rx={3} fill={['#43A047', '#FFB300', '#8E24AA'][k % 3]} stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#1C4466' : '#2B8FC9'} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 80 + 30 * Math.sin(t + k)} ${f + 40 + 160 * rnd(k)} q 18 -10 36 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.5} />)}
      <rect x={z.x0} y={f - 6} width={w} height={14} fill="#7BC4EA" opacity={0.7} />
    </g>;
  },
  /** Inside a ship's cabin: riveted steel walls, portholes onto a rocking sea, bunks, a swinging lamp; the room rolls gently. */
  cabin: (t, z, f) => {
    const w = z.x1 - z.x0, roll = Math.sin(t * 0.9) * 2.2, cx = z.x0 + w / 2, night = !!z.night;
    return <g transform={`rotate(${roll} ${cx} ${f})`}>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#9FB3C8" />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <g key={'pl' + k}><rect x={z.x0 + k * 160} y={-2000} width={4} height={2000 + f} fill={OL} opacity={0.2} />
        {Array.from({length: 8}, (_, r) => <circle key={r} cx={z.x0 + k * 160 + 14} cy={f - 40 - r * 90} r={4} fill={OL} opacity={0.3} />)}</g>)}
      {Array.from({length: Math.ceil(w / 560)}, (_, k) => { const x = z.x0 + 280 + k * 560, sea = Math.sin(t * 1.2 + k) * 14;
        return <g key={'ph' + k}><clipPath id={`phc${k}`}><circle cx={x} cy={f - 480} r={70} /></clipPath>
          <circle cx={x} cy={f - 480} r={70} fill={night ? '#1B2A5A' : '#BFE8FA'} />
          <g clipPath={`url(#phc${k})`}><rect x={x - 80} y={f - 470 + sea} width={160} height={120} fill={night ? '#1C4466' : '#2B8FC9'} transform={`rotate(${-roll * 3} ${x} ${f - 480})`} /></g>
          <circle cx={x} cy={f - 480} r={70} fill="none" stroke="#C9A227" strokeWidth={14} />
          {Array.from({length: 8}, (_, j) => <circle key={j} cx={x + 70 * Math.cos(j * 0.785)} cy={f - 480 + 70 * Math.sin(j * 0.785)} r={4} fill={OL} />)}</g>; })}
      {Array.from({length: Math.ceil(w / 900)}, (_, k) => { const x = z.x0 + 600 + k * 900;
        return <g key={'bk' + k}>{[0, 1].map((b) => <g key={b}><rect x={x} y={f - 120 - b * 170} width={300} height={40} rx={8} fill="#E8EEF5" stroke={OL} strokeWidth={4} />
          <rect x={x} y={f - 140 - b * 170} width={300} height={22} rx={8} fill={['#EF9A9A', '#90CAF9'][b]} stroke={OL} strokeWidth={3} /></g>)}
          <path d={`M ${x} ${f} L ${x} ${f - 330} M ${x + 300} ${f} L ${x + 300} ${f - 330}`} stroke="#607D8B" strokeWidth={10} /></g>; })}
      <g transform={`rotate(${-roll * 4 + Math.sin(t * 1.8) * 6} ${cx} -200)`}><path d={`M ${cx} -200 L ${cx} ${f - 640}`} stroke={OL} strokeWidth={3} />
        <path d={`M ${cx - 40} ${f - 640} L ${cx + 40} ${f - 640} L ${cx + 24} ${f - 670} L ${cx - 24} ${f - 670} Z`} fill={K.gold} stroke={OL} strokeWidth={4} />
        <path d={`M ${cx - 40} ${f - 636} L ${cx - 200} ${f - 300} L ${cx + 200} ${f - 300} L ${cx + 40} ${f - 636} Z`} fill="#FFF3B0" opacity={0.2} /></g>
      <rect x={z.x0 - 200} y={f} width={w + 400} height={600} fill="#6D7F91" />
      {Array.from({length: Math.ceil(w / 70)}, (_, k) => <path key={'tp' + k} d={`M ${z.x0 + k * 70} ${f} l 0 600`} stroke={OL} strokeWidth={2} opacity={0.2} />)}
    </g>;
  },
  /** A 1920s ship's saloon: wood panelling, a bar counter with bottles and glasses, portholes, a gramophone. */
  saloon: (t, z, f) => {
    const w = z.x1 - z.x0, roll = Math.sin(t * 0.8) * 1.5, cx = z.x0 + w / 2;
    return <g transform={`rotate(${roll} ${cx} ${f})`}>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#8D5A3B" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 120} y={-2000} width={110} height={2000 + f} fill="#9C6644" stroke="#6D3F25" strokeWidth={3} />)}
      {Array.from({length: Math.ceil(w / 600)}, (_, k) => { const x = z.x0 + 300 + k * 600;
        return <g key={'ph' + k}><circle cx={x} cy={f - 560} r={60} fill="#BFE8FA" stroke="#C9A227" strokeWidth={14} />
          <path d={`M ${x - 56} ${f - 550 + Math.sin(t * 1.2 + k) * 10} L ${x + 56} ${f - 550 + Math.sin(t * 1.2 + k) * 10} L ${x + 56} ${f - 510} L ${x - 56} ${f - 510} Z`} fill="#2B8FC9" /></g>; })}
      <rect x={z.x0 + 200} y={f - 470} width={Math.min(w - 400, 1400)} height={18} fill="#6D3F25" stroke={OL} strokeWidth={3} />
      {Array.from({length: 14}, (_, k) => <g key={'bt' + k} transform={`translate(${z.x0 + 260 + k * 90} ${f - 470})`}>
        <rect x={-14} y={-80} width={28} height={80} rx={8} fill={['#2E7D32', '#8D6E63', '#C62828', '#F9A825'][k % 4]} stroke={OL} strokeWidth={3} />
        <rect x={-6} y={-104} width={12} height={28} fill={['#2E7D32', '#8D6E63', '#C62828', '#F9A825'][k % 4]} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0 + 150} y={f - 200} width={Math.min(w - 300, 1500)} height={200} rx={12} fill="#5D3A1A" stroke={OL} strokeWidth={5} />
      <rect x={z.x0 + 130} y={f - 220} width={Math.min(w - 260, 1540)} height={30} rx={10} fill="#A1662F" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#B23A48" />
      {Array.from({length: Math.ceil(w / 100)}, (_, k) => <path key={'cp' + k} d={`M ${z.x0 + k * 100} ${f + 40} l 50 30 l 50 -30`} fill="none" stroke="#FFC93C" strokeWidth={4} opacity={0.5} />)}
    </g>;
  },
  /** A desert canal: dunes, a sandy bank behind, a narrow blue channel, the near bank in front. */
  canal: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <path d={`M ${z.x0} ${f - 160} ${Array.from({length: Math.ceil(w / 360) + 1}, (_, k) => `Q ${z.x0 + k * 360 + 180} ${f - 280 - 50 * rnd(k + 31)} ${z.x0 + k * 360 + 360} ${f - 170}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#F2C987" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#E0B072" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={150} fill="#2B8FC9" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 90 + 20 * Math.sin(t + k)} ${f + 30 + 80 * rnd(k)} q 18 -10 36 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.5} />)}
      <path d={`M ${z.x0} ${f + 150} ${Array.from({length: Math.ceil(w / 80) + 1}, (_, k) => `L ${z.x0 + k * 80} ${f + 140 + 8 * rnd(k)}`).join(' ')} L ${z.x1} ${f + 600} L ${z.x0} ${f + 600} Z`} fill="#F2C987" stroke={OL} strokeWidth={4} />
    </g>;
  },
  /** A Dutch town: flat green polder, a windmill turning, narrow canal-house gables, a canal, cyclists riding by. */
  dutch: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <rect x={z.x0} y={f - 200} width={w} height={200} fill="#8BD47A" />
      {Array.from({length: Math.ceil(w / 1100)}, (_, k) => { const x = z.x0 + 300 + k * 1100, a = t * 40 + k * 20;
        return <g key={'wm' + k} transform={`translate(${x} ${f - 200})`}>
          <path d="M -50 0 L -30 -230 L 30 -230 L 50 0 Z" fill="#8D6E63" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <path d="M -40 -230 L 0 -280 L 40 -230 Z" fill="#5D4037" stroke={OL} strokeWidth={4} />
          <g transform={`translate(0 -240) rotate(${a})`}>{[0, 90, 180, 270].map((r) => <g key={r} transform={`rotate(${r})`}>
            <rect x={-12} y={-190} width={24} height={180} fill="#FFF8E1" stroke={OL} strokeWidth={3} />
            {[0, 1, 2, 3].map((l) => <path key={l} d={`M -12 ${-170 + l * 40} L 12 ${-170 + l * 40}`} stroke={OL} strokeWidth={2} />)}</g>)}
            <circle r={12} fill={OL} /></g></g>; })}
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => { const x = z.x0 + k * 120, h = 200 + 60 * rnd(k + 51), c = ['#C0504D', '#8D5A3B', '#E8D5B7', '#4E6E8E', '#A0522D'][k % 5];
        if (k % 9 === 2) return null;
        return <g key={'ch' + k}>
          <path d={`M ${x} ${f} L ${x} ${f - h} L ${x + 20} ${f - h} L ${x + 20} ${f - h - 20} L ${x + 40} ${f - h - 20} L ${x + 40} ${f - h - 40} L ${x + 76} ${f - h - 40} L ${x + 76} ${f - h - 20} L ${x + 96} ${f - h - 20} L ${x + 96} ${f - h} L ${x + 116} ${f - h} L ${x + 116} ${f} Z`}
            fill={c} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          {Array.from({length: Math.floor(h / 60)}, (_, r) => [0, 1].map((c2) => <rect key={r + '-' + c2} x={x + 18 + c2 * 46} y={f - h + 24 + r * 60} width={32} height={40} rx={3} fill={K.white} stroke={OL} strokeWidth={3} />))}
        </g>; })}
      <rect x={z.x0} y={f} width={w} height={40} fill="#D8D2C4" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 40} width={w} height={90} fill="#5BA3C9" stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.ceil(w / 100)}, (_, k) => <path key={'cw' + k} d={`M ${z.x0 + k * 100 + 20 * Math.sin(t + k)} ${f + 80} q 15 -8 30 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.6} />)}
      <rect x={z.x0} y={f + 130} width={w} height={500} fill="#C9A26A" />
      {Array.from({length: 5}, (_, k) => { const dir = k % 2 ? -1 : 1, sp = 90 + 40 * rnd(k + 70), span = w + 400;
        const x = dir > 0 ? z.x0 - 200 + ((t * sp + rnd(k) * span) % span) : z.x1 + 200 - ((t * sp + rnd(k) * span) % span), y = f + 190 + (k % 2) * 40, pd = t * 8 * (sp / 90);
        return <g key={'bk' + k} transform={`translate(${x} ${y}) scale(${dir * 0.9} 0.9)`}>
          <circle cx={-32} cy={0} r={20} fill="none" stroke={OL} strokeWidth={4} /><circle cx={32} cy={0} r={20} fill="none" stroke={OL} strokeWidth={4} />
          <path d="M -32 0 L -6 -30 L 22 -30 L 32 0 M -6 -30 L 0 0 L 22 -30 M 22 -30 L 26 -44" fill="none" stroke={['#E53935', '#1E88E5', '#FFB300'][k % 3]} strokeWidth={5} strokeLinejoin="round" />
          <path d={`M 0 0 L ${8 * Math.cos(pd)} ${8 * Math.sin(pd)}`} stroke={OL} strokeWidth={4} />
          <path d={`M -4 -36 L 4 -80`} stroke={['#FF8A65', '#7BD389', '#B39DDB'][k % 3]} strokeWidth={16} strokeLinecap="round" />
          <circle cx={6} cy={-96} r={14} fill={K.skin[k % 4]} stroke={OL} strokeWidth={3} />
          <path d={`M 4 -50 L ${0 + 8 * Math.cos(pd)} ${-10 + 8 * Math.sin(pd)}`} stroke="#2D3E66" strokeWidth={8} strokeLinecap="round" />
          <path d="M 4 -70 L 26 -46" stroke={K.skin[k % 4]} strokeWidth={6} strokeLinecap="round" /></g>; })}
    </g>;
  },
  /** A gamer's bedroom: posters, a desk with a glowing PC tower and a big monitor showing a racing game, a bean bag. */
  den: (t, z, f) => {
    const w = z.x1 - z.x0, cx = (z as any).cx ?? z.x0 + w / 2;
    const rgb = ['#FF5252', '#FFC93C', '#3DBE6B', '#4FB3F6', '#B388FF'][Math.floor(t * 2) % 5];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f} fill="#3A3F6B" />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'ps' + k} x={z.x0 + 60 + k * 300} y={f - 640 + 40 * rnd(k)} width={150} height={200} rx={6}
        fill={['#FF8A65', '#4FB3F6', '#7BD389', '#F06292'][k % 4]} stroke={OL} strokeWidth={4} transform={`rotate(${(rnd(k + 3) - 0.5) * 8} ${z.x0 + 135 + k * 300} ${f - 540})`} />)}
      <rect x={cx - 360} y={f - 200} width={720} height={26} rx={6} fill="#263238" stroke={OL} strokeWidth={4} />
      <rect x={cx - 340} y={f - 174} width={18} height={174} fill="#263238" /><rect x={cx + 322} y={f - 174} width={18} height={174} fill="#263238" />
      <rect x={cx - 230} y={f - 480} width={420} height={260} rx={14} fill="#111827" stroke={OL} strokeWidth={6} />
      <clipPath id="denscr"><rect x={cx - 216} y={f - 466} width={392} height={232} rx={8} /></clipPath>
      <g clipPath="url(#denscr)">
        <rect x={cx - 216} y={f - 466} width={392} height={232} fill="#7FD3F7" />
        <path d={`M ${cx - 216} ${f - 340} L ${cx + 176} ${f - 340} L ${cx + 176} ${f - 234} L ${cx - 216} ${f - 234} Z`} fill="#7BCB6B" />
        <path d={`M ${cx - 90} ${f - 234} L ${cx - 10} ${f - 340} L ${cx + 10} ${f - 340} L ${cx + 90} ${f - 234} Z`} fill="#5B6577" />
        {Array.from({length: 5}, (_, k) => { const u = ((t * 1.5 + k / 5) % 1); return <rect key={k} x={cx - 4 - 2 * u} y={f - 340 + 106 * u} width={8 + 4 * u} height={10 + 10 * u} fill={K.white} />; })}
        <g transform={`translate(${cx + 30 * Math.sin(t * 1.3)} ${f - 262})`}><rect x={-36} y={-22} width={72} height={30} rx={8} fill="#E53935" stroke={OL} strokeWidth={3} />
          <circle cx={-22} cy={10} r={9} fill={OL} /><circle cx={22} cy={10} r={9} fill={OL} /></g></g>
      <rect x={cx - 30} y={f - 220} width={20} height={20} fill="#111827" />
      <rect x={cx + 220} y={f - 430} width={110} height={230} rx={10} fill="#1F2937" stroke={OL} strokeWidth={5} />
      <rect x={cx + 232} y={f - 418} width={86} height={150} rx={6} fill="#0F172A" stroke={rgb} strokeWidth={4} />
      {[0, 1, 2].map((k) => <circle key={k} cx={cx + 275} cy={f - 380 + k * 45} r={16} fill="none" stroke={rgb} strokeWidth={4} transform={`rotate(${t * 300} ${cx + 275} ${f - 380 + k * 45})`} strokeDasharray="10 8" />)}
      <rect x={cx - 120} y={f - 220} width={200} height={20} rx={6} fill="#455A64" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#6D4C41" />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'fb' + k} d={`M ${z.x0 + k * 80} ${f} l 0 600`} stroke={OL} strokeWidth={2} opacity={0.2} />)}
      <ellipse cx={cx - 520} cy={f - 40} rx={120} ry={70} fill="#FF7043" stroke={OL} strokeWidth={5} />
    </g>;
  },
  /** A Norwegian fjord: steep snowy mountains, a waterfall into the fjord, red wooden houses on the shore, a jetty. */
  fjord: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      {Array.from({length: Math.ceil(w / 520) + 1}, (_, k) => { const x = z.x0 + k * 520 - 100, h = 520 + 140 * rnd(k + 81);
        return <g key={'mt' + k}><path d={`M ${x - 340} ${f - 120} L ${x} ${f - 120 - h} L ${x + 340} ${f - 120} Z`} fill={night ? '#3D4F7A' : '#7C8DB0'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <path d={`M ${x - 90} ${f - 120 - h + 130} L ${x} ${f - 120 - h} L ${x + 90} ${f - 120 - h + 130} L ${x + 40} ${f - 120 - h + 100} L ${x} ${f - 120 - h + 140} L ${x - 40} ${f - 120 - h + 100} Z`} fill={K.white} stroke={OL} strokeWidth={3} strokeLinejoin="round" /></g>; })}
      {Array.from({length: Math.ceil(w / 1400)}, (_, k) => { const x = z.x0 + 700 + k * 1400;
        return <g key={'wf' + k}><path d={`M ${x - 20} ${f - 480} Q ${x} ${f - 300} ${x - 10} ${f - 130} L ${x + 30} ${f - 130} Q ${x + 40} ${f - 300} ${x + 20} ${f - 480} Z`} fill="#BFE8FA" stroke={OL} strokeWidth={3} />
          {Array.from({length: 6}, (_, j) => { const u = ((t * 0.8 + j / 6) % 1); return <path key={j} d={`M ${x - 6 + 10 * (j % 3)} ${f - 470 + u * 330} l 0 40`} stroke={K.white} strokeWidth={4} opacity={0.8} />; })}
          {Array.from({length: 5}, (_, j) => <circle key={'sp' + j} cx={x + 10 + 30 * Math.cos(j + t * 3)} cy={f - 130 + 10 * Math.sin(j * 2 + t * 4)} r={10} fill={K.white} opacity={0.7} />)}</g>; })}
      <rect x={z.x0} y={f - 130} width={w} height={130} fill={night ? '#1F4E6E' : '#3C8FB8'} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 80 + 20 * Math.sin(t + k)} ${f - 100 + 70 * rnd(k)} q 16 -8 32 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.5} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#7BAF5E" />
      <rect x={z.x0} y={f} width={w} height={22} fill="#9E8E78" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => { const x = z.x0 + 120 + k * 340;
        return <g key={'rh' + k} transform={`translate(${x} ${f})`}>
          <rect x={-70} y={-120} width={140} height={120} fill={['#B22222', '#C0392B', '#F2C14E', '#ECEFF1'][k % 4]} stroke={OL} strokeWidth={4} />
          {Array.from({length: 7}, (_, j) => <path key={j} d={`M ${-70 + j * 20} -120 L ${-70 + j * 20} 0`} stroke={OL} strokeWidth={1.5} opacity={0.3} />)}
          <path d="M -84 -120 L 0 -180 L 84 -120 Z" fill="#37474F" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <rect x={-46} y={-90} width={30} height={30} fill={night ? '#FFE08A' : K.white} stroke={OL} strokeWidth={3} />
          <rect x={14} y={-70} width={30} height={70} fill="#5D4037" stroke={OL} strokeWidth={3} /></g>; })}
    </g>;
  },
  /** The North Sea: a grey-blue sea to the horizon with rolling swell; the floor line is the sea surface. */
  northsea: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      <rect x={z.x0} y={f - 240} width={w} height={840} fill={night ? '#16324F' : '#3F7CA6'} />
      {Array.from({length: 4}, (_, r) => <path key={'sw' + r} d={`M ${z.x0} ${f - 200 + r * 70} ${Array.from({length: Math.ceil(w / 60) + 1}, (_, k) => `L ${z.x0 + k * 60} ${f - 200 + r * 70 + (6 + r * 3) * Math.sin(k * 0.8 + t * (1 + r * 0.3))}`).join(' ')}`}
        fill="none" stroke={K.white} strokeWidth={3} opacity={0.25 + r * 0.1} />)}
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'wc' + k} d={`M ${z.x0 + k * 90 + 30 * Math.sin(t * 0.7 + k)} ${f + 40 + 200 * rnd(k + 13)} q 20 -12 40 0`} fill="none" stroke={K.white} strokeWidth={4} opacity={0.5} />)}
    </g>;
  },
  /** Race circuit: a packed grandstand of waving fans, generic advertising boards (text only), a track with red-white kerbs. */
  circuit: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const boards: string[] = (z as any).boards || ['SPONSOR', 'YOUR BRAND HERE', 'SPONSOR', 'BRAND', 'SPONSOR'];
    return <g>
      <path d={`M ${z.x0} ${f - 160} L ${z.x0} ${f - 520} L ${z.x1} ${f - 520} L ${z.x1} ${f - 160} Z`} fill="#90A4AE" stroke={OL} strokeWidth={4} />
      <path d={`M ${z.x0} ${f - 560} L ${z.x1} ${f - 560} L ${z.x1} ${f - 520} L ${z.x0} ${f - 520} Z`} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
      {Array.from({length: 7}, (_, r) => Array.from({length: Math.ceil(w / 34)}, (_, k) => { const x = z.x0 + 17 + k * 34 + (r % 2) * 17, y = f - 500 + r * 48, j = rnd(r * 977 + k);
        const jump = Math.max(0, Math.sin(t * 6 + j * 30)) * 6;
        return <g key={r + '-' + k}><circle cx={x} cy={y - jump} r={11} fill={K.skin[Math.floor(j * 4)]} />
          <rect x={x - 12} y={y + 10 - jump} width={24} height={20} rx={6} fill={['#E53935', '#1E88E5', '#FFB300', '#43A047', '#8E24AA', '#FF7043'][Math.floor(j * 6)]} /></g>; }))}
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => <g key={'ad' + k}><rect x={z.x0 + 10 + k * 420} y={f - 150} width={400} height={70} fill={['#FFFFFF', '#FFF59D', '#BBDEFB', '#FFCDD2'][k % 4]} stroke={OL} strokeWidth={4} />
        <T x={z.x0 + 210 + k * 420} y={f - 104} s={28}>{boards[k % boards.length]}</T></g>)}
      <rect x={z.x0} y={f - 80} width={w} height={80} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f} width={w} height={150} fill="#455A64" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <rect key={'kb' + k} x={z.x0 + k * 60} y={f} width={30} height={16} fill={K.red} />)}
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <rect key={'kw' + k} x={z.x0 + k * 60 + 30} y={f} width={30} height={16} fill={K.white} />)}
      <rect x={z.x0} y={f + 150} width={w} height={500} fill={night ? '#2E5B3A' : '#66BB6A'} />
    </g>;
  },
  /** Pit lane: a row of team garages with mechanics' tools, overhead gantry lights, the pit wall. */
  pitlane: (t, z, f) => {
    const w = z.x1 - z.x0;
    const teams: string[] = (z as any).teams || ['TEAM A', 'TEAM B', 'TEAM C', 'TEAM D', 'TEAM E'];
    return <g>
      <rect x={z.x0} y={-2000} width={w} height={2000 + f - 380} fill="#ECEFF1" />
      {Array.from({length: Math.ceil(w / 480)}, (_, k) => { const x = z.x0 + 20 + k * 480, c = ['#E53935', '#1E88E5', '#FF9800', '#00897B', '#7E57C2', '#546E7A'][k % 6];
        return <g key={'gr' + k}>
          <rect x={x} y={f - 380} width={460} height={380} fill="#37474F" stroke={OL} strokeWidth={4} />
          <rect x={x} y={f - 440} width={460} height={60} fill={c} stroke={OL} strokeWidth={4} />
          <T x={x + 230} y={f - 398} s={30} c={K.white}>{teams[k % teams.length]}</T>
          {[0, 1, 2].map((j) => <rect key={j} x={x + 40 + j * 140} y={f - 340} width={100} height={60} rx={6} fill="#263238" stroke={c} strokeWidth={3} />)}
          <rect x={x + 30} y={f - 200} width={50} height={200} fill="#B0BEC5" stroke={OL} strokeWidth={3} /><rect x={x + 380} y={f - 200} width={50} height={200} fill="#B0BEC5" stroke={OL} strokeWidth={3} /></g>; })}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <circle key={'gl' + k} cx={z.x0 + 150 + k * 300} cy={f - 470} r={10} fill={Math.sin(t * 3 + k) > 0 ? '#FFEB3B' : '#FFF9C4'} stroke={OL} strokeWidth={2} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#546E7A" />
      <path d={`M ${z.x0} ${f + 60} L ${z.x1} ${f + 60}`} stroke={K.white} strokeWidth={6} strokeDasharray="40 30" />
    </g>;
  },
  /** Modern Gulf city: desert dunes, a sea strip, a skyline of glass towers with one needle-like supertall, palm trees. */
  gulf: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night, cx = (z as any).cx ?? z.x0 + w / 2;
    return <g>
      <path d={`M ${z.x0} ${f - 120} ${Array.from({length: Math.ceil(w / 300) + 1}, (_, k) => `Q ${z.x0 + k * 300 + 150} ${f - 200 - 40 * rnd(k + 91)} ${z.x0 + k * 300 + 300} ${f - 130}`).join(' ')} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill={night ? '#8D6E63' : '#F2C987'} stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 130)}, (_, k) => { const x = z.x0 + 10 + k * 130; if (Math.abs(x + 50 - cx) < 140) return null;
        const h = 260 + 300 * rnd(k + 17), c = ['#90CAF9', '#B3E5FC', '#80DEEA', '#9FA8DA', '#B0BEC5'][k % 5];
        return <g key={'gt' + k}><path d={k % 3 === 0 ? `M ${x} ${f - 120} L ${x} ${f - 120 - h} Q ${x + 50} ${f - 120 - h - 60} ${x + 100} ${f - 120 - h} L ${x + 100} ${f - 120} Z` : `M ${x} ${f - 120} L ${x} ${f - 120 - h} L ${x + 100} ${f - 120 - h + (k % 2 ? 30 : 0)} L ${x + 100} ${f - 120} Z`}
          fill={c} stroke={OL} strokeWidth={4} />
          {Array.from({length: Math.floor(h / 36)}, (_, r) => <rect key={r} x={x + 10} y={f - 120 - h + 30 + r * 36} width={80} height={10} fill={night ? (rnd(k * 7 + r) > 0.5 ? '#FFE08A' : '#2A3550') : K.white} opacity={0.75} />)}</g>; })}
      <g transform={`translate(${cx} ${f - 120})`}>
        <path d="M -70 0 L -50 -380 L -30 -560 L -14 -720 L 0 -860 L 14 -720 L 30 -560 L 50 -380 L 70 0 Z" fill="#CFD8DC" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <path d="M 0 -860 L 0 -960" stroke={OL} strokeWidth={6} />
        {Array.from({length: 16}, (_, r) => <path key={r} d={`M ${-60 + r * 3.5} ${-40 - r * 50} L ${60 - r * 3.5} ${-40 - r * 50}`} stroke={night ? '#FFE08A' : '#78909C'} strokeWidth={3} />)}
        {night && <circle cx={0} cy={-960} r={8} fill={Math.sin(t * 4) > 0 ? K.red : '#7A2A2A'} />}</g>
      <rect x={z.x0} y={f - 120} width={w} height={120} fill={night ? '#1E5A7A' : '#29B6F6'} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 80 + 20 * Math.sin(t + k)} ${f - 90 + 60 * rnd(k)} q 16 -8 32 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.6} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#F2D29B" />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const x = z.x0 + 200 + k * 420, sw = Math.sin(t * 1.4 + k) * 6;
        return <g key={'pm' + k} transform={`translate(${x} ${f + 10})`}><path d={`M 0 0 Q -8 -80 ${sw} -170`} fill="none" stroke="#8A5A2B" strokeWidth={12} strokeLinecap="round" />
          {[-150, -100, -40, 20, 70].map((a2, j) => <path key={j} d={`M ${sw} -170 q ${Math.cos(a2 * Math.PI / 180) * 55} ${Math.sin(a2 * Math.PI / 180) * 55 - 20} ${Math.cos(a2 * Math.PI / 180) * 100} ${Math.sin(a2 * Math.PI / 180) * 100 + 30}`} fill="none" stroke="#2E9E5B" strokeWidth={14} strokeLinecap="round" />)}</g>; })}
    </g>;
  },
  /** Old trading town on a creek: sand-coloured houses with wind towers, a souk awning, the creek water at the front. */
  creek: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    return <g>
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const x = z.x0 + 20 + k * 260, h = 150 + 60 * rnd(k + 33);
        return <g key={'oh' + k}>
          <rect x={x} y={f - 60 - h} width={200} height={h} fill={['#E8CFA0', '#DDBF8C', '#EAD7B0'][k % 3]} stroke={OL} strokeWidth={4} />
          {k % 2 === 0 && <g><rect x={x + 130} y={f - 60 - h - 110} width={56} height={110} fill="#D7B98A" stroke={OL} strokeWidth={4} />
            {[0, 1].map((j) => <rect key={j} x={x + 138 + j * 22} y={f - 60 - h - 100} width={14} height={80} fill="#8D6E63" />)}</g>}
          <rect x={x + 30} y={f - 60 - h + 40} width={36} height={50} rx={18} fill={night ? '#FFE08A' : '#8D6E63'} stroke={OL} strokeWidth={3} />
          <rect x={x + 80} y={f - 140} width={44} height={80} fill="#6D4C41" stroke={OL} strokeWidth={3} /></g>; })}
      {Array.from({length: Math.ceil(w / 600)}, (_, k) => <g key={'aw' + k}><path d={`M ${z.x0 + 100 + k * 600} ${f - 60} L ${z.x0 + 120 + k * 600} ${f - 150} L ${z.x0 + 380 + k * 600} ${f - 150} L ${z.x0 + 400 + k * 600} ${f - 60}`} fill="none" stroke={OL} strokeWidth={3} />
        <path d={`M ${z.x0 + 110 + k * 600} ${f - 150} L ${z.x0 + 390 + k * 600} ${f - 150} L ${z.x0 + 370 + k * 600} ${f - 120} L ${z.x0 + 130 + k * 600} ${f - 120} Z`} fill={['#EF5350', '#42A5F5', '#FFCA28'][k % 3]} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#C9A66B" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill={night ? '#1E5A7A' : '#3FA9C9'} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'cw' + k} d={`M ${z.x0 + k * 80 + 20 * Math.sin(t + k)} ${f + 40 + 160 * rnd(k)} q 16 -8 32 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.5} />)}
    </g>;
  },
  /** Swiss Alps: snowy peaks, a blue lake, wooden chalets with flower boxes, a red cable car, a red train along the shore. */
  swiss: (t, z, f) => {
    const w = z.x1 - z.x0, night = !!z.night;
    const trainX = z.x0 + ((t * 170) % (w + 1200)) - 600;
    return <g>
      {Array.from({length: Math.ceil(w / 460) + 1}, (_, k) => { const x = z.x0 + k * 460 - 80, h = 460 + 170 * rnd(k + 121);
        return <g key={'pk' + k}><path d={`M ${x - 320} ${f - 180} L ${x} ${f - 180 - h} L ${x + 320} ${f - 180} Z`} fill={night ? '#46557F' : '#8A9BC0'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <path d={`M ${x - 110} ${f - 180 - h + 150} L ${x} ${f - 180 - h} L ${x + 110} ${f - 180 - h + 150} L ${x + 50} ${f - 180 - h + 115} L ${x} ${f - 180 - h + 160} L ${x - 50} ${f - 180 - h + 115} Z`} fill={K.white} stroke={OL} strokeWidth={3} strokeLinejoin="round" /></g>; })}
      <path d={`M ${z.x0} ${f - 330} L ${z.x0 + w * 0.5} ${f - 640} L ${z.x1} ${f - 340}`} fill="none" stroke={OL} strokeWidth={3} />
      {(() => { const u = (Math.sin(t * 0.35) + 1) / 2, cx2 = lerp(z.x0 + 200, z.x0 + w * 0.5 - 60, u), cy2 = lerp(f - 340, f - 610, u);
        return <g transform={`translate(${cx2} ${cy2})`}><path d="M 0 0 L 0 26" stroke={OL} strokeWidth={3} /><rect x={-34} y={26} width={68} height={52} rx={8} fill="#E53935" stroke={OL} strokeWidth={4} />
          <rect x={-24} y={34} width={48} height={20} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={2} /></g>; })()}
      <rect x={z.x0} y={f - 180} width={w} height={120} fill={night ? '#1F4E6E' : '#4FB3E8'} />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'lw' + k} d={`M ${z.x0 + k * 90 + 20 * Math.sin(t + k)} ${f - 150 + 70 * rnd(k)} q 16 -8 32 0`} fill="none" stroke={K.white} strokeWidth={3} opacity={0.5} />)}
      <rect x={z.x0} y={f - 60} width={w} height={14} fill="#9E9E9E" />
      <g transform={`translate(${trainX} ${f - 62})`}>{[0, 1, 2].map((k) => <g key={k} transform={`translate(${k * 190} 0)`}>
        <rect x={0} y={-70} width={180} height={66} rx={14} fill="#E53935" stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((j) => <rect key={j} x={14 + j * 54} y={-60} width={40} height={26} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={2} />)}</g>)}</g>
      <rect x={z.x0} y={f - 46} width={w} height={600} fill="#7BCB6B" />
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const x = z.x0 + 150 + k * 380;
        return <g key={'ch' + k} transform={`translate(${x} ${f})`}>
          <rect x={-80} y={-130} width={160} height={130} fill="#A1662F" stroke={OL} strokeWidth={4} />
          {Array.from({length: 6}, (_, j) => <path key={j} d={`M -80 ${-130 + j * 22} L 80 ${-130 + j * 22}`} stroke={OL} strokeWidth={1.5} opacity={0.35} />)}
          <path d="M -110 -120 L 0 -200 L 110 -120 Z" fill="#6D4C41" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <rect x={-50} y={-100} width={36} height={34} fill={night ? '#FFE08A' : K.white} stroke={OL} strokeWidth={3} />
          <rect x={14} y={-100} width={36} height={34} fill={night ? '#FFE08A' : K.white} stroke={OL} strokeWidth={3} />
          {[-32, 32].map((dx) => <rect key={dx} x={dx - 24} y={-64} width={48} height={12} fill="#E53935" />)}
          <rect x={-16} y={-46} width={32} height={46} fill="#5D4037" stroke={OL} strokeWidth={3} /></g>; })}
    </g>;
  },
  /** Plain studio-like sky with rolling hills (fallback / neutral). */
  hills: (t, z, f) => {
    const w = z.x1 - z.x0;
    return <g>
      <path d={`M ${z.x0} ${f} ${Array.from({length: Math.ceil(w / 200) + 1}, (_, k) => `Q ${z.x0 + k * 200 + 100} ${f - 120 - 60 * rnd(k)} ${z.x0 + k * 200 + 200} ${f}`).join(' ')} L ${z.x1} ${f + 600} L ${z.x0} ${f + 600} Z`} fill="#8BD47A" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#7BCB6B" />
    </g>;
  },
};
const INDOOR = new Set(['parliament', 'shop', 'pitlane', 'den', 'cabin', 'saloon', 'web', 'exchange', 'newsroom', 'vault', 'court', 'office', 'fab', 'carplant', 'datacenter']);

/* =============================================================================================== ITEMS */
type Ctx = {t: number; f: number};
type ItemFn = (a: StageItem, c: Ctx, i: number) => React.ReactNode;

/** A generic cartoon person (no likeness to anyone): bean body, round head, simple face. Origin at the feet. */
const person: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = a.scale ?? 1, fl = a.flip ? -1 : 1, pose = a.pose || 'stand';
  const shirt = a.suit ? '#F4F7FB' : col(a.color, ['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB', '#FFC93C', '#F06292'][i % 6]);
  const skin = K.skin[(a.skin ?? i) % 4], hair = a.old ? '#CFD8DC' : ['#3E2723', '#212121', '#8D6E63', '#F4C542', '#5D4037'][(a.hair ?? i) % 5];
  const walk = pose === 'walk' || pose === 'run' ? Math.sin(t * (pose === 'run' ? 14 : 8)) : 0;
  const bob = pose === 'cheer' ? Math.abs(Math.sin(t * 7)) * 18 : pose === 'walk' || pose === 'run' ? Math.abs(walk) * 6 : Math.sin(t * 2 + i) * 2;
  const app = pop(t, a.at ?? 0, 0.45);
  if (app <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const sad = a.sadAt !== undefined && t >= a.sadAt || pose === 'worry';
  let la = 20, ra = -20;                                 // arm angles (deg from down)
  if (pose === 'walk' || pose === 'run') { la = 30 * walk; ra = -30 * walk; }
  if (pose === 'type') { la = 70 + 12 * Math.sin(t * 18 + i); ra = -70 - 12 * Math.sin(t * 18 + i + 1.5); }
  if (pose === 'point') { ra = -100 - 6 * Math.sin(t * 3); }
  if (pose === 'cheer') { la = 160 + 10 * Math.sin(t * 7); ra = -160 - 10 * Math.sin(t * 7); }
  if (pose === 'worry') { la = 150; ra = -150; }
  if (pose === 'shrug') { la = 110; ra = -110; }
  if (pose === 'read' || pose === 'phone') { la = 60; ra = -120; }
  const arm = (side: number, ang: number) => { const r = (ang * Math.PI) / 180, sx = side * 26, sy = -140;
    return <path d={`M ${sx} ${sy} L ${sx + Math.sin(r) * 58 * -1 * -1} ${sy + Math.cos(r) * 58}`} stroke={skin} strokeWidth={13} strokeLinecap="round" />; };
  const out = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'p' + i} opacity={out} transform={`translate(${x} ${y - bob}) scale(${s * fl * app} ${s * app})`}>
    <path d={`M -14 -80 L ${-14 + 16 * walk} 0 M 14 -80 L ${14 - 16 * walk} 0`} stroke="#2D3E66" strokeWidth={16} strokeLinecap="round" />
    <path d={`M -26 -2 l -10 0 M 26 -2 l 10 0`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
    {arm(-1, la)}
    <rect x={-34} y={-158} width={68} height={86} rx={26} fill={shirt} stroke={OL} strokeWidth={4} />
    {a.tie && <path d="M 0 -150 L -7 -126 L 0 -100 L 7 -126 Z" fill={K.red} stroke={OL} strokeWidth={2.5} />}
    {a.badge && <circle cx={18} cy={-132} r={9} fill={K.gold} stroke={OL} strokeWidth={3} />}
    {arm(1, ra)}
    {(pose === 'read') && <g transform="translate(34 -150) rotate(-8)"><rect x={-4} y={-30} width={64} height={46} fill={K.white} stroke={OL} strokeWidth={3} />
      {[0, 1, 2].map((l) => <path key={l} d={`M 4 ${-20 + l * 12} L 52 ${-20 + l * 12}`} stroke={OL} strokeWidth={2.5} opacity={0.6} />)}</g>}
    {pose === 'phone' && <rect x={30} y={-210} width={16} height={30} rx={4} fill={OL} />}
    <circle cx={0} cy={-192} r={32} fill={skin} stroke={OL} strokeWidth={4} />
    <path d={['M -32 -196 Q -30 -232 0 -230 Q 30 -232 32 -196 Q 16 -214 -32 -196 Z', 'M -33 -190 Q -36 -236 0 -228 Q 36 -236 33 -190 L 26 -206 L -26 -206 Z',
      'M -30 -200 Q 0 -244 30 -200 Z', 'M -34 -180 Q -40 -236 0 -232 Q 40 -236 34 -180 Q 28 -214 0 -214 Q -28 -214 -34 -180 Z', 'M -28 -208 Q 0 -230 28 -208 Z'][(a.hair ?? i) % 5]}
      fill={hair} stroke={OL} strokeWidth={3} strokeLinejoin="round" />
    {a.glasses ? <g><circle cx={-11} cy={-192} r={9} fill="none" stroke={OL} strokeWidth={3} /><circle cx={13} cy={-192} r={9} fill="none" stroke={OL} strokeWidth={3} /></g> : null}
    <circle cx={-11} cy={-192} r={3.5} fill={OL} /><circle cx={13} cy={-192} r={3.5} fill={OL} />
    <path d={sad ? 'M -11 -170 Q 1 -180 13 -170' : 'M -11 -176 Q 1 -164 13 -176'} fill="none" stroke={OL} strokeWidth={3.5} strokeLinecap="round" />
    {a.suit && <g><path d="M -38 -186 Q -40 -240 0 -238 Q 40 -240 38 -186 L 38 -150 L -38 -150 Z" fill="#F4F7FB" stroke={OL} strokeWidth={4} />
      <rect x={-26} y={-206} width={52} height={22} rx={10} fill={skin} stroke={OL} strokeWidth={3} /><circle cx={-11} cy={-195} r={3.5} fill={OL} /><circle cx={13} cy={-195} r={3.5} fill={OL} />
      <rect x={-24} y={-182} width={48} height={22} rx={8} fill="#B3E5FC" stroke={OL} strokeWidth={3} /></g>}
    {a.old && <g><path d="M 44 -110 L 60 0" stroke={K.wood2} strokeWidth={8} strokeLinecap="round" /><path d="M 30 -112 Q 44 -124 50 -110" stroke={K.wood2} strokeWidth={8} fill="none" strokeLinecap="round" /></g>}
    {a.hat && <path d="M -36 -214 L 36 -214 L 26 -236 L -26 -236 Z" fill={col(a.hat)} stroke={OL} strokeWidth={3} />}
    {sad && <path d={`M 34 -208 q 4 ${8 + 4 * Math.sin(t * 6)} 0 12 q -4 -4 0 -12`} fill="#7FD3F7" stroke={OL} strokeWidth={2} />}
  </g>;
};

/** A watchdog (the regulator as a cartoon dog with a cap and badge); it barks on cue. */
const dog: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0), fl = a.flip ? -1 : 1;
  if (s <= 0) return null;
  const barks: number[] = a.barks || [], bk = barks.some((b) => t >= b && t < b + 0.8), wag = Math.sin(t * 12) * 18;
  return <g key={'d' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <path d={`M -70 -70 q -30 ${-20 + wag * 0.3} -40 -50`} fill="none" stroke="#C68B4E" strokeWidth={12} strokeLinecap="round" />
    <ellipse cx={0} cy={-70} rx={80} ry={44} fill="#E0A96D" stroke={OL} strokeWidth={4} />
    {[-50, -20, 30, 56].map((dx) => <rect key={dx} x={dx - 9} y={-40} width={18} height={40} rx={8} fill="#E0A96D" stroke={OL} strokeWidth={4} />)}
    <g transform={`translate(70 -120) rotate(${bk ? -12 : Math.sin(t * 2) * 4})`}>
      <ellipse cx={0} cy={0} rx={46} ry={40} fill="#E0A96D" stroke={OL} strokeWidth={4} />
      <ellipse cx={-30} cy={-8} rx={14} ry={30} fill="#8A5428" stroke={OL} strokeWidth={3} transform="rotate(20 -30 -8)" />
      <ellipse cx={42} cy={10} rx={24} ry={18} fill="#F2C38E" stroke={OL} strokeWidth={4} />
      <circle cx={60} cy={4} r={7} fill={OL} />
      <circle cx={10} cy={-8} r={6} fill={OL} />
      {bk ? <path d="M 30 22 Q 50 46 66 24 Z" fill="#E53935" stroke={OL} strokeWidth={3} /> : <path d="M 32 24 Q 46 30 58 22" fill="none" stroke={OL} strokeWidth={3} />}
      <path d="M -40 -26 L 34 -26 L 26 -52 L -30 -52 Z" fill="#28407A" stroke={OL} strokeWidth={3} />
      <rect x={-46} y={-30} width={88} height={10} rx={4} fill="#1E2F5C" stroke={OL} strokeWidth={2} />
      <circle cx={-2} cy={-40} r={6} fill={K.gold} stroke={OL} strokeWidth={2} /></g>
    <path d="M 30 -100 L 60 -86" stroke="#E53935" strokeWidth={10} strokeLinecap="round" />
    <circle cx={50} cy={-80} r={10} fill={K.gold} stroke={OL} strokeWidth={3} />
    {bk && <g transform={`translate(160 -150) scale(${E.outBack(win(t, barks.find((b) => t >= b && t < b + 0.8)!, 0.3))})`}>
      <path d="M 0 0 L 90 -30 L 70 0 L 100 24 Z" fill={K.white} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <T x={58} y={4} s={26}>{a.text || 'WOOF!'}</T></g>}
  </g>;
};

/** A glass corporate tower with a label panel. growAt: rises from the ground; darkAt: lights go out;
 * crumbleAt: it shakes, sinks into the ground and leaves a dust cloud. */
const tower: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 300), s = a.scale ?? 1, w = (a.w ?? 220) * s, h = kf(a.h, t, 560) * s, c = col(a.color, K.purple);
  const grow = a.growAt !== undefined ? E.outBack(win(t, a.growAt, 1.6)) : pop(t, a.at ?? 0, 0.6);
  const crumble = a.crumbleAt !== undefined ? E.in(win(t, a.crumbleAt, 2.4)) : 0;
  const dark = a.darkAt !== undefined && t >= a.darkAt;
  const hh = h * Math.max(0, grow) * (1 - crumble * 0.92), shk = crumble > 0 && crumble < 1 ? Math.sin(t * 50) * 6 : 0;
  if (hh <= 2 && crumble === 0) return null;
  const cols = Math.max(2, Math.floor(w / 46)), rows = Math.max(2, Math.floor(hh / 52));
  return <g key={'tw' + i} transform={`translate(${x + shk} ${f}) rotate(${crumble * 6})`}>
    <rect x={-w / 2} y={-hh} width={w} height={hh} rx={8} fill={c} stroke={OL} strokeWidth={5} />
    {Array.from({length: rows}, (_, r) => r).filter((r) => 70 * s + r * 52 + 30 < hh - 10).map((r) => Array.from({length: cols}, (_, k) => {
      const on = !dark && rnd(i * 97 + r * 11 + k + Math.floor(t * 1.2)) > 0.3;
      return <rect key={r + '-' + k} x={-w / 2 + 14 + k * ((w - 28) / cols)} y={-hh + 70 * s + r * 52} width={(w - 28) / cols - 10} height={30}
        rx={3} fill={on ? '#FFE9A8' : dark ? '#2A3550' : '#C9B8F5'} stroke={OL} strokeWidth={2} />; }))}
    <rect x={-w / 2 - 10} y={-hh - 8} width={w + 20} height={58 * s} rx={10} fill={K.white} stroke={OL} strokeWidth={4} />
    <T x={0} y={-hh + 34 * s} s={Math.min(34 * s, (w + 10) / Math.max(4, (a.text || '').length) * 1.6)}>{a.text || 'COMPANY'}</T>
    {a.antenna !== false && <path d={`M 0 ${-hh - 8} L 0 ${-hh - 60 * s}`} stroke={OL} strokeWidth={5} />}
    {a.antenna !== false && <circle cx={0} cy={-hh - 60 * s} r={8} fill={Math.sin(t * 5) > 0 ? K.red : '#7A2A2A'} stroke={OL} strokeWidth={3} />}
    {crumble > 0 && <g opacity={1 - win(t, a.crumbleAt + 3, 2)}>{Array.from({length: 9}, (_, k) =>
      <circle key={k} cx={(k - 4) * w * 0.22} cy={-20 - 30 * rnd(k)} r={(40 + 30 * rnd(k + 3)) * Math.min(1, crumble * 2)} fill="#D7CCC8" stroke={OL} strokeWidth={3} />)}</g>}
  </g>;
};

/** A smaller building: style 'office' | 'bank' (columns) | 'gov' (columns + dome) | 'news' (printing house). */
const building: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6), c = col(a.color, K.gold), st = a.style || 'office';
  if (s <= 0) return null;
  const dark = a.darkAt !== undefined && t >= a.darkAt;
  return <g key={'b' + i} transform={`translate(${x} ${kf(a.y, t, f)}) scale(${s})`}>
    {st === 'office' && <g><rect x={-120} y={-300} width={240} height={300} rx={8} fill={c} stroke={OL} strokeWidth={5} />
      {[0, 1, 2, 3].map((r) => [0, 1, 2].map((k) => <rect key={r + '' + k} x={-96 + k * 70} y={-250 + r * 60} width={52} height={36} rx={4} fill={dark ? '#2A3550' : '#CFEFFF'} stroke={OL} strokeWidth={3} />))}</g>}
    {(st === 'bank' || st === 'gov') && <g>
      {st === 'gov' && <path d="M -90 -330 Q 0 -440 90 -330 Z" fill="#9FB3CF" stroke={OL} strokeWidth={5} />}
      <path d="M -170 -280 L 0 -360 L 170 -280 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-170} y={-290} width={340} height={30} fill={c} stroke={OL} strokeWidth={5} />
      {[-130, -65, 0, 65, 130].map((dx) => <rect key={dx} x={dx - 16} y={-260} width={32} height={230} fill={dark ? '#7D8597' : K.cream} stroke={OL} strokeWidth={4} />)}
      <rect x={-190} y={-30} width={380} height={30} fill={c} stroke={OL} strokeWidth={5} /></g>}
    {st === 'news' && <g><rect x={-150} y={-280} width={300} height={280} rx={8} fill={c} stroke={OL} strokeWidth={5} />
      <rect x={-120} y={-230} width={240} height={110} rx={6} fill="#CFEFFF" stroke={OL} strokeWidth={4} />
      <rect x={-40} y={-90} width={80} height={90} fill={K.wood2} stroke={OL} strokeWidth={4} /></g>}
    {a.text && <g><rect x={-Math.max(90, a.text.length * 11 + 24)} y={st === 'office' ? -350 : -404 - (st === 'gov' ? 60 : 0)} width={Math.max(180, a.text.length * 22 + 48)} height={46} rx={10} fill={K.white} stroke={OL} strokeWidth={4} />
      <T x={0} y={(st === 'office' ? -350 : -404 - (st === 'gov' ? 60 : 0)) + 33} s={26}>{a.text}</T></g>}
  </g>;
};

/** Split-flap stock board. rows [{name, value, color}]; swap {at, out: rowIndex, in: {name, value}} slides one out and one in. */
const board: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), w = a.w ?? 900, rows: any[] = a.rows || [], rh = a.rh ?? 70, s = pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const sw = a.swap, out = sw ? E.inBack(win(t, sw.at, 0.9)) : 0, inn = sw ? E.outBack(win(t, sw.at + 0.9, 0.8)) : 0;
  const h = 100 + rows.length * rh;
  return <g key={'bd' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-w / 2 - 16} y={-16} width={w + 32} height={h + 32} rx={20} fill="#1B2438" stroke={OL} strokeWidth={6} />
    <T x={0} y={58} s={46} c={K.gold}>{a.text || 'STOCK INDEX'}</T>
    {rows.map((r, k) => { const isOut = sw && sw.out === k, yy = 90 + k * rh;
      const show = isOut && inn > 0 ? sw.in : r, dx = isOut ? (inn > 0 ? 0 : out * (w + 300)) : 0, flap = isOut && inn > 0 ? 1 - inn : 0;
      const ok = t >= (r.at ?? a.at ?? 0) + 0.3 + k * 0.12;
      if (!ok) return null;
      const hi = isOut && inn > 0;
      return <g key={k} transform={`translate(${dx} ${yy + rh / 2}) scale(1 ${1 - Math.min(0.9, flap)}) translate(0 ${-rh / 2})`}>
        <rect x={-w / 2 + 10} y={4} width={w - 20} height={rh - 10} rx={8} fill={hi ? '#3A2F0B' : isOut && out > 0 ? '#4A1C24' : '#26324D'} stroke={hi ? K.gold : '#3A4A6E'} strokeWidth={hi ? 5 : 3} />
        <T x={-w / 2 + 36} y={rh / 2 + 12} s={32} a="start" c={hi ? K.gold : K.white}>{show.name}</T>
        <T x={w / 2 - 36} y={rh / 2 + 12} s={32} a="end" c={show.color === 'red' ? '#FF7B7B' : show.color === 'gold' ? K.gold : '#7DF29A'}>{show.value}</T>
      </g>; })}
    {sw && out > 0 && inn === 0 && <T x={w / 2 + 120} y={90 + sw.out * rh + rh / 2} s={40} c={K.red}>OUT</T>}
  </g>;
};

/** A line chart on a screen: pts are 0..1 heights; drawn from `at` over `dur`; crashAt plunges it in red. */
const chart: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), w = a.w ?? 700, h = a.h ?? 380, s = pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const pts: number[] = a.pts || [0.1, 0.2, 0.18, 0.35, 0.5, 0.45, 0.7, 0.9];
  const u = clamp(win(t, (a.at ?? 0) + 0.3, a.dur ?? 3)), cr = a.crashAt !== undefined ? E.in(win(t, a.crashAt, 1.2)) : 0;
  const n = pts.length - 1, px = (k: number) => -w / 2 + 40 + (k / n) * (w - 80), py = (v: number) => h / 2 - 40 - v * (h - 100);
  const m = u * n, path: string[] = [];
  for (let k = 0; k <= Math.floor(m); k++) path.push(`${k ? 'L' : 'M'} ${px(k)} ${py(pts[k])}`);
  const fr = m - Math.floor(m), k0 = Math.floor(m);
  let tip: [number, number] = [px(k0), py(pts[k0])];
  if (k0 < n) { tip = [lerp(px(k0), px(k0 + 1), fr), lerp(py(pts[k0]), py(pts[k0 + 1]), fr)]; path.push(`L ${tip[0]} ${tip[1]}`); }
  if (cr > 0) { tip = [tip[0] + 40 * cr, lerp(tip[1], h / 2 - 30, cr)]; path.push(`L ${tip[0]} ${tip[1]}`); }
  const c = cr > 0 ? K.red : col(a.color, '#3DBE6B');
  return <g key={'ch' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={18} fill="#1B2438" stroke={OL} strokeWidth={6} />
    {[0.25, 0.5, 0.75].map((g) => <path key={g} d={`M ${-w / 2 + 30} ${-h / 2 + g * h} L ${w / 2 - 30} ${-h / 2 + g * h}`} stroke="#33415F" strokeWidth={2} />)}
    {a.text && <T x={-w / 2 + 34} y={-h / 2 + 46} s={30} a="start" c={K.white}>{a.text}</T>}
    <path d={path.join(' ')} fill="none" stroke={c} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
    <circle cx={tip[0]} cy={tip[1]} r={12 + 3 * Math.sin(t * 8)} fill={c} stroke={K.white} strokeWidth={3} />
  </g>;
};

/** A newspaper that spins in (classic cartoon headline shot). */
const paper: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0;
  if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const u = E.out(win(t, at, 1.0)), x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * u, o = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'np' + i} opacity={o} transform={`translate(${x} ${y}) rotate(${(1 - u) * 720 + (a.tilt ?? -4)}) scale(${s})`}>
    <rect x={-260} y={-180} width={520} height={360} fill="#FAF6EC" stroke={OL} strokeWidth={6} />
    <T x={0} y={-130} s={34} w={900}>{a.name || 'THE DAILY PAPER'}</T>
    <path d="M -230 -112 L 230 -112" stroke={OL} strokeWidth={4} />
    <T x={0} y={-56} s={a.size ?? 44}>{a.text}</T>
    {a.sub && <T x={0} y={-12} s={24} w={700}>{a.sub}</T>}
    <rect x={-230} y={14} width={180} height={140} fill="#D6D0C0" stroke={OL} strokeWidth={3} />
    {Array.from({length: 7}, (_, l) => <path key={l} d={`M -30 ${24 + l * 20} L 230 ${24 + l * 20}`} stroke={OL} strokeWidth={4} opacity={0.35} />)}
  </g>;
};

/** Printing press: spinning drums, papers sliding out on a belt. */
const press: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const on = t >= (a.runAt ?? a.at ?? 0);
  return <g key={'pr' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-200} y={-260} width={300} height={260} rx={14} fill="#5C6B8A" stroke={OL} strokeWidth={5} />
    {[-130, -30].map((dx, k) => <g key={k} transform={`translate(${dx + 30} -170) rotate(${on ? t * 300 : 0})`}>
      <circle r={50} fill="#9AA7B8" stroke={OL} strokeWidth={5} />
      {[0, 60, 120].map((r) => <path key={r} d="M -44 0 L 44 0" stroke={OL} strokeWidth={4} transform={`rotate(${r})`} />)}</g>)}
    <rect x={100} y={-80} width={380} height={20} rx={8} fill="#3E4660" stroke={OL} strokeWidth={4} />
    {on && Array.from({length: 4}, (_, k) => { const u = ((t - (a.runAt ?? a.at ?? 0)) * 0.6 + k / 4) % 1;
      return <g key={k} transform={`translate(${110 + u * 360} -92)`}><rect x={0} y={-36} width={70} height={36} fill="#FAF6EC" stroke={OL} strokeWidth={3} />
        <path d="M 8 -26 L 62 -26 M 8 -14 L 50 -14" stroke={OL} strokeWidth={3} /></g>; })}
    <rect x={-170} y={-230} width={240} height={30} rx={6} fill={K.gold} stroke={OL} strokeWidth={3} />
    <T x={-50} y={-207} s={20}>{a.text || 'PRINTING'}</T>
  </g>;
};

/** Document stack with a big stamp that slams on `stampAt`. */
const docs: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const sa = a.stampAt, down = sa !== undefined ? win(t, sa - 0.5, 0.5) : 0, hit = sa !== undefined && t >= sa;
  const stampY = sa === undefined ? -999 : hit ? lerp(-210, -330, E.out(win(t, sa + 0.15, 0.5))) : lerp(-520, -210, E.in(down));
  const c = col(a.color, K.red);
  return <g key={'dc' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {[0, 1, 2, 3, 4].map((k) => <rect key={k} x={-130 + (k % 2) * 6} y={-30 - k * 26} width={260} height={30} fill="#FAF6EC" stroke={OL} strokeWidth={3} />)}
    <g transform={`translate(0 -200) rotate(-3)`}>
      <rect x={-140} y={-170} width={280} height={180} fill={K.white} stroke={OL} strokeWidth={4} />
      <T x={0} y={-130} s={22}>{a.text || 'BANK CONFIRMATION'}</T>
      {[0, 1, 2, 3].map((l) => <path key={l} d={`M -110 ${-100 + l * 22} L 110 ${-100 + l * 22}`} stroke={OL} strokeWidth={3} opacity={0.35} />)}
      {hit && <g transform={`rotate(-14) scale(${E.outBack(win(t, sa, 0.3))})`}>
        <rect x={-120} y={-100} width={240} height={70} rx={8} fill="none" stroke={c} strokeWidth={8} />
        <T x={0} y={-48} s={44} c={c}>{a.stamp || 'FALSE'}</T></g>}
    </g>
    {sa !== undefined && t < sa + 1.4 && <g transform={`translate(70 ${stampY})`}>
      <rect x={-50} y={-30} width={100} height={30} rx={6} fill={c} stroke={OL} strokeWidth={4} />
      <rect x={-14} y={-110} width={28} height={84} fill={K.wood} stroke={OL} strokeWidth={4} />
      <circle cx={0} cy={-120} r={26} fill={K.wood2} stroke={OL} strokeWidth={4} /></g>}
    {hit && t < sa + 0.5 && Array.from({length: 8}, (_, k) => { const an = k * 0.785, r = 160 + 80 * win(t, sa, 0.5);
      return <path key={k} d={`M ${Math.cos(an) * 140} ${-260 + Math.sin(an) * 100} L ${Math.cos(an) * r} ${-260 + Math.sin(an) * r * 0.7}`} stroke={K.gold} strokeWidth={6} strokeLinecap="round" />; })}
  </g>;
};

/** A contract with a signature line: a pen hovers... then a big red X "NOT SIGNED" on refuseAt; or signAt for a tick. */
const contract: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const ra = a.refuseAt, no = ra !== undefined && t >= ra, hov = Math.sin(t * 3) * 12;
  return <g key={'ct' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(-2)`}>
    <rect x={-230} y={-300} width={460} height={600} rx={8} fill={K.white} stroke={OL} strokeWidth={5} />
    <T x={0} y={-240} s={34}>{a.text || 'ANNUAL ACCOUNTS'}</T>
    {Array.from({length: 9}, (_, l) => <path key={l} d={`M -190 ${-190 + l * 34} L ${150 - 60 * rnd(l)} ${-190 + l * 34}`} stroke={OL} strokeWidth={4} opacity={0.3} />)}
    <path d="M -190 200 L 190 200" stroke={OL} strokeWidth={4} />
    <T x={-190} y={236} s={22} a="start" w={700}>{a.sub || 'Auditor signature'}</T>
    {!no && <g transform={`translate(${60 + hov} ${150 + hov * 0.5}) rotate(35)`}>
      <rect x={-12} y={-130} width={24} height={130} rx={8} fill={K.blue} stroke={OL} strokeWidth={4} />
      <path d="M -12 0 L 0 28 L 12 0 Z" fill={K.gold} stroke={OL} strokeWidth={3} /></g>}
    {no && <g transform={`scale(${E.outBack(win(t, ra, 0.4))})`}>
      <path d="M -170 -170 L 170 170 M 170 -170 L -170 170" stroke={K.red} strokeWidth={34} strokeLinecap="round" opacity={0.9} />
      <rect x={-200} y={240} width={400} height={70} rx={12} fill={K.red} stroke={OL} strokeWidth={5} />
      <T x={0} y={288} s={40} c={K.white}>{a.stamp || 'NOT SIGNED'}</T></g>}
  </g>;
};

/** Coins arc from `from` to `to` (a stream), from at until `until`. */
const coins: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0, until = a.until ?? 1e9, rate = a.rate ?? 4, fr: [number, number] = a.from, to: [number, number] = a.to;
  if (t < at) return null;
  const n = Math.ceil((Math.min(t, until) - at) * rate), out: React.ReactNode[] = [];
  for (let k = Math.max(0, n - 12); k < n; k++) {
    const t0 = at + k / rate, u = win(t, t0, 1.4);
    if (u >= 1 || u <= 0) continue;
    const px = lerp(fr[0], to[0], u), py = lerp(fr[1], to[1], u) - Math.sin(u * Math.PI) * (a.arc ?? 160);
    out.push(<g key={k} transform={`translate(${px} ${py}) scale(${Math.abs(Math.cos(t * 6 + k))} 1)`}>
      {a.shape === 'note' ? <g><rect x={-30} y={-16} width={60} height={32} rx={4} fill="#9BE39B" stroke={OL} strokeWidth={3} /><circle r={9} fill="#5DBB63" stroke={OL} strokeWidth={2} /></g>
        : <g><circle r={20} fill={a.ghost ? 'none' : K.gold} stroke={OL} strokeWidth={4} strokeDasharray={a.ghost ? '6 6' : undefined} /><T x={0} y={8} s={22}>$</T></g>}</g>);
  }
  return <g key={'cn' + i}>{out}</g>;
};

/** The bank vault door: a wheel spins, then the door swings open (on openAt) on an empty interior. */
const vaultdoor: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), r = a.r ?? 260, cy = f - r - 30, oa = a.openAt ?? 1e9;
  const spin = win(t, oa - 2, 2) * 540, open = E.inOut(win(t, oa, 1.6));
  return <g key={'vd' + i}>
    <circle cx={x} cy={cy} r={r + 26} fill="#3A4056" stroke={OL} strokeWidth={6} />
    <circle cx={x} cy={cy} r={r} fill="#1E2233" stroke={OL} strokeWidth={4} />
    {/* empty interior: shelves, cobweb, dust */}
    {open > 0 && <g opacity={open}>
      {[-0.4, 0, 0.4].map((dy) => <rect key={dy} x={x - r * 0.7} y={cy + dy * r} width={r * 1.4} height={12} fill="#5A6280" stroke={OL} strokeWidth={3} />)}
      <path d={`M ${x + r * 0.2} ${cy - r * 0.75} L ${x + r * 0.6} ${cy - r * 0.35} M ${x + r * 0.35} ${cy - r * 0.68} Q ${x + r * 0.42} ${cy - r * 0.55} ${x + r * 0.55} ${cy - r * 0.48} M ${x + r * 0.27} ${cy - r * 0.7} Q ${x + r * 0.36} ${cy - r * 0.6} ${x + r * 0.48} ${cy - r * 0.55}`} stroke="#C8CEDD" strokeWidth={3} fill="none" />
      {Array.from({length: 10}, (_, k) => <circle key={k} cx={x + (rnd(k) - 0.5) * r * 1.2} cy={cy + (rnd(k + 5) - 0.5) * r - ((t * 10 + k * 13) % 40)} r={3} fill="#D7CCC8" opacity={0.6} />)}
      {(() => { const mx = x + Math.sin(t * 2.3) * r * 0.5, my = cy - r * 0.2 + Math.cos(t * 3.1) * r * 0.3, fl = Math.sin(t * 30) * 10;
        return <g transform={`translate(${mx} ${my})`}><ellipse rx={8} ry={5} fill="#8D6E63" /><path d={`M 0 0 L -14 ${-8 - fl} L -4 -2 Z M 0 0 L 14 ${-8 - fl} L 4 -2 Z`} fill="#BCAAA4" stroke={OL} strokeWidth={2} /></g>; })()}
      <T x={x} y={cy + r * 0.85} s={34} c="#C8CEDD">{a.text || 'EMPTY'}</T></g>}
    <g transform={`translate(${x - r - 20} ${cy}) scale(${1 - open * 0.85} 1) translate(${r + 20} 0)`}>
      <circle r={r} fill="#AEB7CC" stroke={OL} strokeWidth={8} />
      <circle r={r * 0.8} fill="none" stroke="#8C95AB" strokeWidth={8} />
      {Array.from({length: 12}, (_, k) => { const an = k * Math.PI / 6; return <circle key={k} cx={Math.cos(an) * r * 0.9} cy={Math.sin(an) * r * 0.9} r={9} fill="#8C95AB" stroke={OL} strokeWidth={3} />; })}
      <g transform={`rotate(${spin})`}>
        <circle r={r * 0.32} fill="none" stroke={OL} strokeWidth={10} />
        {[0, 60, 120].map((k) => <path key={k} d={`M ${-r * 0.42} 0 L ${r * 0.42} 0`} stroke={OL} strokeWidth={12} strokeLinecap="round" transform={`rotate(${k})`} />)}
        <circle r={22} fill={K.gold} stroke={OL} strokeWidth={5} /></g>
      {a.label && <g><rect x={-120} y={r * 0.45} width={240} height={46} rx={8} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={r * 0.45 + 33} s={24}>{a.label}</T></g>}
    </g>
  </g>;
};

/** Piggy bank (a trust account); crackAt breaks it open: empty, a moth flies out. */
const piggy: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const ca = a.crackAt ?? 1e9, cr = E.out(win(t, ca, 0.8)), bob = Math.sin(t * 2.4) * 4 * (1 - cr);
  const half = (side: number) => <g transform={`translate(${side * cr * 70} ${cr * 20}) rotate(${side * cr * 18})`}>
    <clipPath id={`pg${i}${side}`}><rect x={side < 0 ? -200 : 0} y={-300} width={200} height={400} /></clipPath>
    <g clipPath={`url(#pg${i}${side})`}>
      <ellipse cx={0} cy={-100} rx={130} ry={95} fill="#F8A5C2" stroke={OL} strokeWidth={5} />
      <ellipse cx={128} cy={-100} rx={26} ry={30} fill="#F48FB1" stroke={OL} strokeWidth={4} />
      <circle cx={134} cy={-104} r={4} fill={OL} /><circle cx={124} cy={-92} r={4} fill={OL} />
      <path d="M 50 -180 L 70 -220 L 90 -175 Z" fill="#F48FB1" stroke={OL} strokeWidth={4} />
      <circle cx={70} cy={-128} r={7} fill={OL} />
      {[-70, -20, 30, 80].map((dx) => <rect key={dx} x={dx - 14} y={-24} width={28} height={30} rx={6} fill="#F48FB1" stroke={OL} strokeWidth={4} />)}
      <rect x={-40} y={-196} width={80} height={12} rx={6} fill={OL} />
      {a.text && <T x={-10} y={-80} s={26}>{a.text}</T>}
    </g></g>;
  return <g key={'pg' + i} transform={`translate(${x} ${y - bob}) scale(${s})`}>
    {cr > 0 && <g opacity={cr}><path d="M -10 -190 L 10 -150 L -8 -110 L 12 -60 L -6 -10" fill="none" stroke={OL} strokeWidth={4} />
      {(() => { const u = win(t, ca + 0.4, 3), mx = Math.sin(t * 5) * 40 * u, my = -100 - u * 260;
        return <g transform={`translate(${mx} ${my})`}><ellipse rx={9} ry={6} fill="#8D6E63" /><path d={`M 0 0 L -16 ${-10 - Math.sin(t * 30) * 10} L -4 -2 Z M 0 0 L 16 ${-10 - Math.sin(t * 30) * 10} L 4 -2 Z`} fill="#BCAAA4" stroke={OL} strokeWidth={2} /></g>; })()}
      <T x={0} y={40} s={30} c={K.red}>{a.empty || 'EMPTY'}</T></g>}
    {half(-1)}{half(1)}
  </g>;
};

/** A magnifying glass that sweeps across. */
const magnifier: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until)) return null;
  return <g key={'mg' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 2) * 8})`}>
    <path d="M 70 70 L 170 170" stroke={K.wood2} strokeWidth={30} strokeLinecap="round" />
    <circle r={100} fill="#CFEFFF" fillOpacity={0.35} stroke={OL} strokeWidth={12} />
    {a.text && <T x={0} y={14} s={40}>{a.text}</T>}
  </g>;
};

/** A plane with a text tail; x/y keyframes. */
const plane: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = a.scale ?? 1, fl = a.flip ? -1 : 1;
  if (t < (a.at ?? 0)) return null;
  return <g key={'pl' + i} transform={`translate(${x} ${y + Math.sin(t * 2) * 6}) scale(${s * fl} ${s}) rotate(${a.tilt ?? -6})`}>
    <path d="M -170 0 Q -170 -40 -100 -40 L 140 -40 Q 200 -30 200 0 Q 200 30 140 30 L -100 30 Q -170 30 -170 0 Z" fill={K.white} stroke={OL} strokeWidth={5} />
    <path d="M -130 -36 L -170 -110 L -110 -110 L -70 -36 Z" fill={col(a.color, K.red)} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    <path d="M -10 10 L -80 90 L 0 90 L 60 10 Z" fill="#DDE3EE" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    {[0, 1, 2, 3, 4].map((k) => <circle key={k} cx={-40 + k * 36} cy={-10} r={10} fill="#9FE3FF" stroke={OL} strokeWidth={3} />)}
    {a.text && <T x={-140} y={-62} s={44} c={K.white}>{a.text}</T>}
  </g>;
};

/** A hanging / standing sign with text. */
const sign: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 300), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const w = Math.max(200, (a.text || '').length * (a.size ?? 34) * 0.62 + 60, (a.sub || '').length * 12.5 + 60), sw = a.swing ? Math.sin(t * 2.4) * 5 : 0;
  return <g key={'sg' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${sw})`}>
    {a.post && <rect x={-8} y={0} width={16} height={f - y} fill={K.wood2} stroke={OL} strokeWidth={3} />}
    {a.hang && <g><path d={`M ${-w / 3} -50 L ${-w / 3} -130 M ${w / 3} -50 L ${w / 3} -130`} stroke={OL} strokeWidth={4} /><rect x={-w / 2 - 20} y={-142} width={w + 40} height={14} rx={7} fill={K.wood2} stroke={OL} strokeWidth={3} /></g>}
    <rect x={-w / 2} y={-50} width={w} height={a.sub ? 112 : 84} rx={14} fill={col(a.color, K.white)} stroke={OL} strokeWidth={5} />
    <T x={0} y={4} s={a.size ?? 34}>{a.text}</T>
    {a.sub && <T x={0} y={44} s={22} w={700}>{a.sub}</T>}
  </g>;
};

/** Gavel: strikes its block at each time in `hits`. */
const gavel: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 400), s = a.scale ?? 1, hits: number[] = a.hits || [];
  let ang = -40;
  for (const h of hits) { if (t >= h - 0.35 && t < h) ang = lerp(-40, 10, E.in(win(t, h - 0.35, 0.35))); else if (t >= h && t < h + 0.6) ang = lerp(10, -40, E.out(win(t, h, 0.6))); }
  const hit = hits.find((h) => t >= h && t < h + 0.4);
  return <g key={'gv' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-70} y={-14} width={140} height={28} rx={8} fill={K.wood2} stroke={OL} strokeWidth={4} />
    <g transform={`translate(90 -40) rotate(${ang})`}>
      <rect x={-130} y={-8} width={130} height={16} rx={6} fill={K.wood} stroke={OL} strokeWidth={4} />
      <rect x={-180} y={-34} width={60} height={68} rx={10} fill={K.wood2} stroke={OL} strokeWidth={4} /></g>
    {hit !== undefined && Array.from({length: 6}, (_, k) => { const an = Math.PI + k * 0.63, r = 50 + 60 * win(t, hit, 0.4);
      return <path key={k} d={`M ${Math.cos(an) * 40} ${-20 + Math.sin(an) * 30} L ${Math.cos(an) * r} ${-20 + Math.sin(an) * r * 0.7}`} stroke={K.gold} strokeWidth={6} strokeLinecap="round" />; })}
  </g>;
};

/** Wall calendar whose page flips to each [time, text] in pages. */
const calendar: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const pages: [number, string, string?][] = a.pages || [];
  let cur = 0; pages.forEach((p, k) => { if (t >= p[0]) cur = k; });
  const flip = win(t, pages[cur][0], 0.5), pg = pages[cur];
  return <g key={'cal' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-150} y={-170} width={300} height={340} rx={16} fill={K.white} stroke={OL} strokeWidth={6} />
    <rect x={-150} y={-170} width={300} height={80} rx={16} fill={col(a.color, K.red)} stroke={OL} strokeWidth={6} />
    {[-80, 80].map((dx) => <rect key={dx} x={dx - 8} y={-196} width={16} height={46} rx={8} fill="#9AA7B8" stroke={OL} strokeWidth={3} />)}
    <T x={0} y={-116} s={36} c={K.white}>{pg[2] || a.text || 'JUNE 2020'}</T>
    <g transform={`translate(0 30) scale(1 ${E.outBack(flip)})`}><T x={0} y={40} s={Math.min(120, 440 / Math.max(1, pg[1].length))}>{pg[1]}</T></g>
    {flip < 1 && cur > 0 && <path d={`M -150 -90 L 150 -90 L 150 ${-90 + 260 * (1 - flip)} L -150 ${-90 + 260 * (1 - flip)} Z`} fill="#F1F1F1" stroke={OL} strokeWidth={3} opacity={1 - flip} />}
  </g>;
};

/** Thunder cloud with rain and an occasional lightning bolt. */
const storm: ItemFn = (a, {t}, i) => {
  if (t < (a.at ?? 0)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 160), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.8), bolt = Math.sin(t * 1.7) > 0.93;
  return <g key={'st' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {Array.from({length: 14}, (_, k) => { const u = (t * 1.8 + rnd(k)) % 1; return <path key={k} d={`M ${-140 + k * 20} ${40 + u * 300} l -8 26`} stroke="#7FB8E6" strokeWidth={4} strokeLinecap="round" />; })}
    {bolt && <path d="M 10 30 L -30 130 L 10 130 L -20 240" fill="none" stroke={K.gold} strokeWidth={10} strokeLinejoin="round" />}
    <path d="M -180 30 Q -200 -40 -120 -40 Q -100 -110 -10 -90 Q 60 -130 120 -60 Q 200 -60 190 20 Q 190 50 150 50 L -150 50 Q -190 50 -180 30 Z" fill="#6E7891" stroke={OL} strokeWidth={5} />
    <circle cx={-40} cy={-10} r={7} fill={OL} /><circle cx={30} cy={-10} r={7} fill={OL} />
    <path d="M -30 22 Q -5 6 20 22" fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
  </g>;
};

/** An office chair; spinAt makes it spin, empty (someone left). nameplate in text. */
const chair: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const sp = a.spinAt !== undefined ? Math.max(0, 1 - win(t, a.spinAt, 4)) * (t >= a.spinAt ? 1 : 0) : 0, sq = Math.cos((t - (a.spinAt ?? 0)) * 10 * sp);
  return <g key={'chr' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <path d="M -60 0 L 60 0 M 0 0 L 0 -90" stroke={OL} strokeWidth={10} strokeLinecap="round" />
    <g transform={`scale(${sp > 0 ? sq : 1} 1)`}>
      <rect x={-70} y={-120} width={140} height={34} rx={14} fill="#28407A" stroke={OL} strokeWidth={5} />
      <rect x={-60} y={-280} width={120} height={170} rx={30} fill="#28407A" stroke={OL} strokeWidth={5} /></g>
    {a.text && <g><rect x={-90} y={-40} width={180} height={40} rx={8} fill={K.gold} stroke={OL} strokeWidth={3} transform="translate(0 -360)" /><T x={0} y={-370} s={24}>{a.text}</T></g>}
  </g>;
};

/** Desk with a computer screen (for newsroom / office scenes); `glow` a screen colour. */
const desk: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = a.scale ?? 1;
  return <g key={'dk' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={30} y={-250} width={130} height={90} rx={8} fill="#1E2A44" stroke={OL} strokeWidth={4} />
    {[0, 1, 2].map((l) => <rect key={l} x={42} y={-236 + l * 22} width={((t * 40 + l * 30 + i * 17) % 100)} height={8} rx={4} fill={col(a.glow, '#7DF29A')} opacity={0.8} />)}
    <rect x={88} y={-160} width={14} height={30} fill={OL} />
    <rect x={-150} y={-130} width={300} height={24} rx={6} fill={K.wood} stroke={OL} strokeWidth={4} />
    <rect x={-130} y={-106} width={16} height={106} fill={K.wood2} /><rect x={114} y={-106} width={16} height={106} fill={K.wood2} />
    {a.pile && [0, 1, 2, 3].map((k) => <rect key={k} x={-130 + (k % 2) * 4} y={-150 - k * 10} width={70} height={10} fill="#FAF6EC" stroke={OL} strokeWidth={2} />)}
  </g>;
};

/** Card terminal: a card taps on each time in taps, a green tick and a coin pop out. */
const terminal: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 200), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0) return null;
  const taps: number[] = a.taps || [], last = taps.filter((h) => t >= h - 0.6).pop();
  const near = last !== undefined ? Math.sin(Math.PI * win(t, last - 0.6, 1.2)) : 0, ok = last !== undefined && t >= last && t < last + 1.2;
  return <g key={'tm' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-80} y={-130} width={160} height={260} rx={24} fill="#37474F" stroke={OL} strokeWidth={5} />
    <rect x={-60} y={-110} width={120} height={80} rx={8} fill={ok ? '#7DF29A' : '#9FE3FF'} stroke={OL} strokeWidth={4} />
    {ok && <path d="M -26 -70 L -6 -50 L 30 -92" fill="none" stroke={OL} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />}
    {Array.from({length: 9}, (_, k) => <rect key={k} x={-52 + (k % 3) * 38} y={-10 + Math.floor(k / 3) * 38} width={28} height={28} rx={6} fill="#B0BEC5" stroke={OL} strokeWidth={2} />)}
    <g transform={`translate(${150 - near * 120} ${-80 + near * 20}) rotate(-12)`}>
      <rect x={-80} y={-50} width={160} height={100} rx={12} fill={col(a.color, K.blue2)} stroke={OL} strokeWidth={5} />
      <rect x={-60} y={-20} width={36} height={26} rx={4} fill={K.gold} stroke={OL} strokeWidth={3} />
      <path d="M -60 28 L 50 28" stroke={OL} strokeWidth={4} opacity={0.5} /></g>
    {ok && <T x={0} y={-160 - 30 * win(t, last!, 1.2)} s={34} c={K.green} o={1 - win(t, last!, 1.2)}>BEEP!</T>}
  </g>;
};

/** Big bouncy text in the world (labels, ? marks). */
const letters: ItemFn = (a, {t}, i) => {
  const s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), sz = a.size ?? 90, o = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'lt' + i} opacity={o} transform={`translate(${x} ${y + Math.sin(t * 3 + i) * 8}) scale(${s}) rotate(${Math.sin(t * 2 + i) * 4})`}>
    <text x={0} y={sz * 0.35} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={sz} fill={col(a.color, K.gold)} stroke={OL} strokeWidth={Math.max(3, sz / 22)} paintOrder="stroke">{a.text}</text>
  </g>;
};

/** A cartoon arrow from -> to with an optional label. */
const bigArrow: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0;
  if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const u = E.out(win(t, at, 0.7)), [x1, y1] = a.from as [number, number], [x2, y2] = a.to as [number, number];
  const ex = lerp(x1, x2, u), ey = lerp(y1, y2, u), an = Math.atan2(y2 - y1, x2 - x1), c = col(a.color, K.red);
  return <g key={'ar' + i}>
    <path d={`M ${x1} ${y1} L ${ex} ${ey}`} stroke={OL} strokeWidth={26} strokeLinecap="round" />
    <path d={`M ${x1} ${y1} L ${ex} ${ey}`} stroke={c} strokeWidth={16} strokeLinecap="round" />
    <path d={`M ${ex + Math.cos(an) * 30} ${ey + Math.sin(an) * 30} L ${ex + Math.cos(an + 2.4) * 44} ${ey + Math.sin(an + 2.4) * 44} L ${ex + Math.cos(an - 2.4) * 44} ${ey + Math.sin(an - 2.4) * 44} Z`} fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    {a.text && u > 0.8 && <T x={(x1 + x2) / 2} y={(y1 + y2) / 2 - 30} s={30}>{a.text}</T>}
  </g>;
};

/** A world-space ticker tape (scrolling headlines). */
const ticker: ItemFn = (a, {t}, i) => {
  const y = kf(a.y, t, 980), x0 = a.x0 ?? -400, x1 = a.x1 ?? 2400, items: string[] = a.items || [];
  if (t < (a.at ?? 0)) return null;
  const txt = items.join('   •   ') + '   •   ', len = txt.length * 17, off = ((t * 160) % len);
  return <g key={'tk' + i}>
    <rect x={x0} y={y - 34} width={x1 - x0} height={56} fill={col(a.color, '#1B2438')} stroke={OL} strokeWidth={4} />
    <clipPath id={`tkc${i}`}><rect x={x0} y={y - 34} width={x1 - x0} height={56} /></clipPath>
    <g clipPath={`url(#tkc${i})`}>{[0, 1, 2].map((k) => <text key={k} x={x0 + k * len - off} y={y + 6} fontFamily={FONT} fontWeight={800} fontSize={28} fill={K.gold}>{txt}</text>)}</g>
  </g>;
};

/** Confetti / dust burst at `at`. */
const burst: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0, u = win(t, at, 1.6);
  if (t < at || u >= 1) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400);
  return <g key={'bs' + i}>{Array.from({length: 22}, (_, k) => { const an = rnd(k) * Math.PI * 2, r = 40 + 260 * E.out(u) * (0.5 + rnd(k + 2));
    return <rect key={k} x={x + Math.cos(an) * r} y={y + Math.sin(an) * r + 200 * u * u} width={14} height={8} fill={['#FFC93C', '#4FB3F6', '#FF8A65', '#7BD389', '#F06292'][k % 5]}
      transform={`rotate(${t * 300 + k * 40} ${x + Math.cos(an) * r} ${y + Math.sin(an) * r + 200 * u * u})`} opacity={1 - u} />; })}</g>;
};

/** Silicon wafer: rainbow sheen, a grid of dies; on revealAt each die turns green (works) or red (fails) with `fail` share. */
const wafer: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), r = a.r ?? 220, s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const n = a.n ?? 9, cell = (2 * r) / n, ra = a.revealAt, fail = kf(a.fail, t, 0.3);
  const dies: React.ReactNode[] = [];
  for (let r2 = 0; r2 < n; r2++) for (let c2 = 0; c2 < n; c2++) {
    const dx = -r + c2 * cell + cell / 2, dy = -r + r2 * cell + cell / 2;
    if (dx * dx + dy * dy > (r - cell * 0.55) ** 2) continue;
    const k = r2 * n + c2, on = ra !== undefined && t >= ra + 0.03 * k, bad = rnd(k * 7 + 3) < fail;
    dies.push(<rect key={k} x={dx - cell * 0.42} y={dy - cell * 0.42} width={cell * 0.84} height={cell * 0.84} rx={3}
      fill={on ? (bad ? '#FF7B7B' : '#7DF29A') : 'url(#wafg)'} stroke={OL} strokeWidth={2} opacity={on ? 1 : 0.85} />);
  }
  return <g key={'wf' + i} transform={`translate(${x} ${y}) scale(${s})`}><g transform={`rotate(${(a.spin ?? 0) * t})`}>
    <defs><linearGradient id="wafg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stopColor="#B39DDB" /><stop offset="35%" stopColor="#80DEEA" />
      <stop offset="65%" stopColor="#FFF59D" /><stop offset="100%" stopColor="#F48FB1" /></linearGradient></defs>
    <circle r={r + 8} fill="#CFD8DC" stroke={OL} strokeWidth={6} />
    <path d={`M ${-r * 0.3} ${r + 6} L ${r * 0.3} ${r + 6}`} stroke={OL} strokeWidth={8} />
    {dies}
    <path d={`M ${-r * 0.7} ${-r * 0.3} Q ${-r * 0.2} ${-r * 0.9} ${r * 0.5} ${-r * 0.7}`} fill="none" stroke={K.white} strokeWidth={10} opacity={0.5 + 0.3 * Math.sin(t * 2)} strokeLinecap="round" />
    </g>
    {a.text && <T x={0} y={r + 60} s={30}>{a.text}</T>}
  </g>;
};

/** EUV lithography machine: a huge box with a window; violet light pulses print onto a wafer stage. */
const litho: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.7);
  if (s <= 0) return null;
  const on = t >= (a.fireAt ?? a.at ?? 0), pulse = on ? 0.5 + 0.5 * Math.sin(t * 14) : 0;
  return <g key={'li' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-330} y={-520} width={660} height={520} rx={26} fill="#F4F7FB" stroke={OL} strokeWidth={6} />
    <rect x={-330} y={-520} width={660} height={60} rx={26} fill={col(a.color, '#1E7FD8')} stroke={OL} strokeWidth={6} />
    <T x={0} y={-478} s={30} c={K.white}>{a.text || 'EUV MACHINE'}</T>
    <rect x={-240} y={-420} width={480} height={300} rx={16} fill="#1B2438" stroke={OL} strokeWidth={5} />
    <circle cx={-150} cy={-330} r={44} fill="#7E57C2" opacity={0.4 + 0.6 * pulse} stroke={OL} strokeWidth={4} />
    {[0, 1, 2].map((k) => <circle key={k} cx={-150} cy={-330} r={44 + ((t * 60 + k * 30) % 90)} fill="none" stroke="#B388FF" strokeWidth={3} opacity={on ? 1 - ((t * 60 + k * 30) % 90) / 90 : 0} />)}
    <path d="M -110 -330 L 60 -330 L 0 -180" fill="none" stroke="#B388FF" strokeWidth={on ? 10 : 3} opacity={0.3 + 0.7 * pulse} strokeLinejoin="round" />
    {[50, 0].map((mx, k) => <rect key={k} x={mx - 26} y={(k ? -200 : -350) - 8} width={52} height={16} rx={4} fill="#CFD8DC" stroke={OL} strokeWidth={3} transform={`rotate(${k ? 0 : 30} ${mx} ${k ? -200 : -350})`} />)}
    <ellipse cx={0} cy={-150} rx={110} ry={20} fill="url(#wafg2)" stroke={OL} strokeWidth={4} />
    <defs><linearGradient id="wafg2" x1="0" x2="1"><stop offset="0%" stopColor="#B39DDB" /><stop offset="50%" stopColor="#80DEEA" /><stop offset="100%" stopColor="#F48FB1" /></linearGradient></defs>
    {on && <circle cx={((t * 70) % 160) - 80} cy={-150} r={8} fill={K.white} opacity={pulse} />}
    {[-260, 200].map((dx) => <rect key={dx} x={dx} y={-90} width={60} height={60} rx={8} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}
    {a.sub && <g><rect x={-220} y={-110} width={440} height={50} rx={10} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={-75} s={24}>{a.sub}</T></g>}
  </g>;
};

/** Overhead transport: a wafer pod rides the ceiling rail (x keyframes) and lowers its hoist on dropAt. */
const pod: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), rail = a.rail ?? 92, drop = a.dropAt !== undefined ? Math.sin(Math.PI * win(t, a.dropAt, 3)) : 0, hy = rail + 40 + drop * (a.depth ?? 300);
  return <g key={'pd' + i}>
    <rect x={x - 50} y={rail - 8} width={100} height={46} rx={8} fill="#FFC93C" stroke={OL} strokeWidth={4} />
    <path d={`M ${x - 30} ${rail + 38} L ${x - 30} ${hy} M ${x + 30} ${rail + 38} L ${x + 30} ${hy}`} stroke={OL} strokeWidth={3} />
    <rect x={x - 46} y={hy} width={92} height={70} rx={10} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
    <rect x={x - 30} y={hy + 16} width={60} height={8} fill="#90A4AE" /><rect x={x - 30} y={hy + 32} width={60} height={8} fill="#90A4AE" />
  </g>;
};

/** Robot arm that swings back and forth handing over a wafer. */
const arm: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5), ph = Math.sin(t * (a.speed ?? 1.6) + i);
  if (s <= 0) return null;
  return <g key={'am' + i} transform={`translate(${x} ${f}) scale(${s * (a.flip ? -1 : 1)} ${s})`}>
    <rect x={-60} y={-60} width={120} height={60} rx={10} fill="#90A4AE" stroke={OL} strokeWidth={4} />
    <g transform={`translate(0 -60) rotate(${-20 + ph * 25})`}>
      <rect x={-16} y={-180} width={32} height={180} rx={14} fill={col(a.color, '#FF8F00')} stroke={OL} strokeWidth={4} />
      <circle cx={0} cy={0} r={22} fill="#607D8B" stroke={OL} strokeWidth={4} />
      <g transform={`translate(0 -180) rotate(${70 - ph * 40})`}>
        <rect x={-14} y={-150} width={28} height={150} rx={12} fill={col(a.color, '#FFA726')} stroke={OL} strokeWidth={4} />
        <circle cx={0} cy={0} r={18} fill="#607D8B" stroke={OL} strokeWidth={4} />
        <path d="M -30 -150 L 30 -150" stroke={OL} strokeWidth={8} strokeLinecap="round" />
        <ellipse cx={0} cy={-162} rx={48} ry={10} fill="url(#wafg2)" stroke={OL} strokeWidth={3} /></g></g>
  </g>;
};

/** Conveyor belt carrying goods ('box' | 'chip' | 'car' | 'phone'); stopAt halts it, gapAt leaves gaps (missing parts). */
const conveyor: ItemFn = (a, {t, f}, i) => {
  const x0 = a.x0 ?? 200, x1 = a.x1 ?? 1700, y = kf(a.y, t, f - 40), sp = a.speed ?? 120, n = a.n ?? 6, len = x1 - x0;
  if (t < (a.at ?? 0)) return null;
  const tt = a.stopAt !== undefined ? Math.min(t, a.stopAt + 0.6 * (1 - Math.exp(-(t - a.stopAt) * 2)) * (t > a.stopAt ? 1 : 0) + (t > a.stopAt ? 0 : 0)) : t;
  const stopped = a.stopAt !== undefined && t >= a.stopAt;
  const goods: React.ReactNode[] = [];
  for (let k = 0; k < n; k++) {
    const gx = x0 + (((stopped ? a.stopAt : tt) * sp + (k * len) / n) % len);
    const missing = a.gapAt !== undefined && t >= a.gapAt && k % 2 === 1;
    const g = a.goods || 'box';
    goods.push(<g key={k} transform={`translate(${gx} ${y - 18})`}>
      {missing ? <g><rect x={-46} y={-60} width={92} height={60} rx={8} fill="none" stroke={K.red} strokeWidth={4} strokeDasharray="8 6" /><T x={0} y={-22} s={20} c={K.red}>{a.gapText || 'NO CHIP'}</T></g>
        : g === 'car' ? <g><path d="M -70 0 L -70 -34 L -40 -36 L -20 -64 L 40 -64 L 60 -36 L 76 -32 L 76 0 Z" fill={['#E53935', '#1E7FD8', '#FFC93C', '#3DBE6B'][k % 4]} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <rect x={-14} y={-58} width={44} height={20} rx={3} fill="#CFEFFF" stroke={OL} strokeWidth={2} /><circle cx={-40} cy={2} r={14} fill="#333" stroke={OL} strokeWidth={3} /><circle cx={46} cy={2} r={14} fill="#333" stroke={OL} strokeWidth={3} /></g>
        : g === 'chip' ? <g><rect x={-30} y={-60} width={60} height={60} rx={6} fill="#37474F" stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3].map((p2) => <path key={p2} d={`M ${-22 + p2 * 15} -60 l 0 -10 M ${-22 + p2 * 15} 0 l 0 10`} stroke={K.gold} strokeWidth={4} />)}<rect x={-16} y={-46} width={32} height={32} rx={4} fill={K.gold} opacity={0.8} /></g>
        : g === 'bun' ? <g><path d="M -44 0 Q -46 -52 0 -54 Q 46 -52 44 0 Z" fill="#F0A84E" stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3].map((q) => <ellipse key={q} cx={-24 + q * 16} cy={-34 + (q % 2) * 10} rx={5} ry={3} fill="#FFF5E1" />)}</g>
        : g === 'patty' ? <g><ellipse cx={0} cy={-14} rx={46} ry={14} fill="#6B3E26" stroke={OL} strokeWidth={4} /><path d="M -30 -18 L 30 -18" stroke="#8D5A3B" strokeWidth={3} /></g>
        : g === 'potato' ? <g><ellipse cx={0} cy={-22} rx={36} ry={22} fill="#C8A26B" stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((q) => <circle key={q} cx={-14 + q * 14} cy={-26 + (q % 2) * 8} r={2.5} fill="#8A6A3E" />)}</g>
        : g === 'fries' ? <g><path d="M -26 0 L -32 -46 L 32 -46 L 26 0 Z" fill="#D84315" stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3, 4].map((q) => <rect key={q} x={-26 + q * 11} y={-76 + (q % 2) * 8} width={8} height={36} fill="#FFD54F" stroke={OL} strokeWidth={2} />)}</g>
        : g === 'phone' ? <g><rect x={-22} y={-76} width={44} height={76} rx={8} fill="#263238" stroke={OL} strokeWidth={4} /><rect x={-16} y={-68} width={32} height={56} rx={4} fill="#80DEEA" /></g>
        : <g><rect x={-40} y={-60} width={80} height={60} rx={6} fill="#D7A86E" stroke={OL} strokeWidth={4} /><path d="M -40 -40 L 40 -40" stroke={OL} strokeWidth={3} />
          {a.label && <T x={0} y={-12} s={16}>{a.label}</T>}</g>}
    </g>);
  }
  return <g key={'cv' + i}>
    {goods}
    <rect x={x0 - 40} y={y - 18} width={len + 80} height={36} rx={18} fill="#455A64" stroke={OL} strokeWidth={4} />
    {Array.from({length: Math.ceil(len / 60) + 2}, (_, k) => <circle key={k} cx={x0 - 20 + k * 60} cy={y} r={11} fill="#90A4AE" stroke={OL} strokeWidth={2}
      transform={`rotate(${stopped ? 0 : t * 400} ${x0 - 20 + k * 60} ${y})`} />)}
    {Array.from({length: Math.ceil(len / 300) + 1}, (_, k) => <rect key={'lg' + k} x={x0 + k * 300 - 8} y={y + 18} width={16} height={f - y - 18 + 4} fill="#607D8B" stroke={OL} strokeWidth={2} />)}
    {stopped && <g><circle cx={x1 + 80} cy={y - 140} r={24} fill={Math.sin(t * 8) > 0 ? K.red : '#7A2A2A'} stroke={OL} strokeWidth={4} />
      <rect x={x1 + 76} y={y - 116} width={8} height={98} fill={OL} /></g>}
  </g>;
};

/** A device: phone | laptop | car | server | washer | chip; redAt puts a red ✗ badge on it. */
const device: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5), ty = a.type || 'phone';
  if (s <= 0) return null;
  const red = a.redAt !== undefined && t >= a.redAt, bob = Math.sin(t * 2.5 + i) * 4;
  return <g key={'dv' + i} transform={`translate(${x} ${y + bob}) scale(${s})`}>
    {ty === 'phone' && <g><rect x={-50} y={-200} width={100} height={190} rx={16} fill="#263238" stroke={OL} strokeWidth={5} /><rect x={-40} y={-186} width={80} height={150} rx={8} fill={red ? '#5C6B7A' : '#80DEEA'} /></g>}
    {ty === 'laptop' && <g><rect x={-110} y={-170} width={220} height={140} rx={10} fill="#455A64" stroke={OL} strokeWidth={5} /><rect x={-96} y={-158} width={192} height={114} rx={4} fill={red ? '#5C6B7A' : '#A5D6A7'} />
      <path d="M -140 -20 L 140 -20 L 120 0 L -120 0 Z" fill="#90A4AE" stroke={OL} strokeWidth={5} strokeLinejoin="round" /></g>}
    {ty === 'car' && <g><path d="M -140 -20 L -140 -70 L -90 -74 L -50 -130 L 70 -130 L 110 -74 L 150 -66 L 150 -20 Z" fill={col(a.color, '#E53935')} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-30} y={-118} width={90} height={40} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={3} /><circle cx={-80} cy={-16} r={28} fill="#333" stroke={OL} strokeWidth={4} /><circle cx={92} cy={-16} r={28} fill="#333" stroke={OL} strokeWidth={4} /></g>}
    {ty === 'server' && <g><rect x={-70} y={-300} width={140} height={300} rx={8} fill="#2E3B5E" stroke={OL} strokeWidth={5} />
      {Array.from({length: 8}, (_, r) => <g key={r}><rect x={-58} y={-286 + r * 35} width={116} height={26} rx={3} fill="#3D4D75" />
        <circle cx={-44} cy={-273 + r * 35} r={5} fill={red ? '#4A5675' : Math.sin(t * 7 + r) > 0 ? '#7DF29A' : '#4A5675'} /></g>)}</g>}
    {ty === 'tv' && <g><rect x={-150} y={-230} width={300} height={200} rx={18} fill="#37474F" stroke={OL} strokeWidth={5} />
      <rect x={-132} y={-214} width={264} height={168} rx={10} fill={red ? '#5C6B7A' : '#B388FF'} />
      {!red && <path d="M -20 -160 L 30 -130 L -20 -100 Z" fill={K.white} stroke={OL} strokeWidth={3} />}
      <path d="M -60 -30 L -80 0 M 60 -30 L 80 0" stroke={OL} strokeWidth={6} /></g>}
    {ty === 'hospital' && <g><rect x={-130} y={-220} width={260} height={220} rx={10} fill={K.white} stroke={OL} strokeWidth={5} />
      <rect x={-22} y={-200} width={44} height={110} fill={K.red} /><rect x={-55} y={-167} width={110} height={44} fill={K.red} />
      <rect x={-30} y={-70} width={60} height={70} fill="#90CAF9" stroke={OL} strokeWidth={3} /></g>}
    {ty === 'washer' && <g><rect x={-90} y={-210} width={180} height={210} rx={12} fill={K.white} stroke={OL} strokeWidth={5} /><circle cx={0} cy={-90} r={60} fill="#B3E5FC" stroke={OL} strokeWidth={5} />
      <path d={`M -40 -90 Q 0 ${-90 + 30 * Math.sin(t * 5)} 40 -90`} stroke="#4FB3F6" strokeWidth={6} fill="none" /></g>}
    {ty === 'chip' && <g><rect x={-60} y={-130} width={120} height={120} rx={10} fill="#37474F" stroke={OL} strokeWidth={5} />
      {[0, 1, 2, 3, 4].map((p2) => <path key={p2} d={`M ${-48 + p2 * 24} -130 l 0 -16 M ${-48 + p2 * 24} -10 l 0 16 M -60 ${-118 + p2 * 24} l -16 0 M 60 ${-118 + p2 * 24} l 16 0`} stroke={K.gold} strokeWidth={5} />)}
      <rect x={-34} y={-104} width={68} height={68} rx={6} fill={col(a.color, K.gold)} opacity={0.85} /></g>}
    {a.text && <g><rect x={-Math.max(70, a.text.length * 9 + 20)} y={14} width={Math.max(140, a.text.length * 18 + 40)} height={40} rx={10} fill={K.white} stroke={OL} strokeWidth={3} /><T x={0} y={42} s={22}>{a.text}</T></g>}
    {red && <g transform={`translate(${ty === 'car' ? 120 : 70} -200) scale(${E.outBack(win(t, a.redAt, 0.4))})`}><circle r={30} fill={K.red} stroke={OL} strokeWidth={4} />
      <path d="M -12 -12 L 12 12 M 12 -12 L -12 12" stroke={K.white} strokeWidth={7} strokeLinecap="round" /></g>}
  </g>;
};

/** A row of labelled dominoes; each falls in turn starting at fallAt (step seconds apart). */
const domino: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 300), labels: string[] = a.labels || [], gap = a.gap ?? 230, step = a.step ?? 1.2, fa = a.fallAt ?? 1e9, h = a.h ?? 300;
  return <g key={'dm' + i}>{labels.map((lb, k) => { const st = Array.isArray(fa) ? fa[k] : fa + k * step, ang = E.in(win(t, st, 0.6)) * 72, show = t >= (a.at ?? 0) + k * 0.15;
    if (!show) return null;
    return <g key={k} transform={`translate(${x + k * gap} ${f}) rotate(${ang})`}>
      <rect x={-34} y={-h} width={68} height={h} rx={12} fill={ang > 1 ? '#FFCDD2' : K.white} stroke={OL} strokeWidth={5} />
      <circle cx={0} cy={-h * 0.75} r={10} fill={OL} /><circle cx={0} cy={-h * 0.6} r={10} fill={OL} />
      <text x={0} y={-h * 0.2} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={24} fill={OL} transform={`rotate(-90 0 ${-h * 0.2})`}>{lb}</text>
    </g>; })}</g>;
};

/** Construction crane building a fab: the building rises with `progress` (0..1 keyframes); the hook swings. */
const crane: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6), pr = clamp(kf(a.progress, t, 0.3));
  if (s <= 0) return null;
  const bh = 260 * pr, sw = Math.sin(t * 1.5 + i) * 30;
  return <g key={'cr' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-200} y={-bh} width={400} height={bh} fill="#F4F7FB" stroke={OL} strokeWidth={5} />
    {pr > 0.4 && <rect x={-200} y={-bh + 30} width={400} height={18} fill="#1E7FD8" />}
    {Array.from({length: Math.floor(bh / 60)}, (_, r) => <path key={r} d={`M -210 ${-r * 60 - 30} L 210 ${-r * 60 - 30}`} stroke="#8D6E63" strokeWidth={4} opacity={pr < 1 ? 1 : 0} />)}
    <path d={`M 260 0 L 260 -560 M 240 0 L 240 -560 ${Array.from({length: 14}, (_, k) => `M 240 ${-k * 40} L 260 ${-k * 40 - 40}`).join(' ')}`} stroke="#FFB300" strokeWidth={6} />
    <path d="M 120 -560 L 520 -560 M 250 -620 L 120 -560 M 250 -620 L 520 -560 M 250 -620 L 250 -560" stroke="#FFB300" strokeWidth={8} strokeLinecap="round" fill="none" />
    <rect x={430} y={-560} width={70} height={60} fill="#78909C" stroke={OL} strokeWidth={3} />
    <path d={`M 160 -560 L ${160 + sw * 0.2} ${-380 + sw * 0.4}`} stroke={OL} strokeWidth={3} />
    <rect x={120 + sw * 0.2} y={-380 + sw * 0.4} width={80} height={40} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
    {a.text && <g><rect x={-Math.max(90, a.text.length * 11 + 24)} y={-bh - 70} width={Math.max(180, a.text.length * 22 + 48)} height={46} rx={10} fill={K.white} stroke={OL} strokeWidth={4} /><T x={0} y={-bh - 37} s={26}>{a.text}</T></g>}
    {pr < 1 && <T x={0} y={-bh / 2 + 12} s={34} c="#8D6E63">{Math.round(pr * 100)}%</T>}
  </g>;
};

/** A stack of banknotes growing to height h (keyframes) with a label. */
const stack: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5), h = kf(a.h, t, 300);
  if (s <= 0) return null;
  const n = Math.max(1, Math.floor(h / 22));
  return <g key={'sk' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    {Array.from({length: n}, (_, k) => <g key={k}><rect x={-110 + (k % 3) * 4} y={-22 - k * 22} width={220} height={20} rx={4} fill={k % 2 ? '#9BE39B' : '#7BD389'} stroke={OL} strokeWidth={3} />
      <circle cx={(k % 3) * 4} cy={-12 - k * 22} r={6} fill="#5DBB63" /></g>)}
    {a.text && <g><rect x={-150} y={-n * 22 - 90} width={300} height={a.sub ? 74 : 52} rx={12} fill={col(a.color, K.white)} stroke={OL} strokeWidth={4} />
      <T x={0} y={-n * 22 - 54} s={30}>{a.text}</T>{a.sub && <T x={0} y={-n * 22 - 28} s={18} w={700}>{a.sub}</T>}</g>}
  </g>;
};

/** Cartoon browser window: the address bar types `url` from typeAt (the ending, e.g. ".ai", glows gold); page: 'site' | 'sold' | 'expired' | 'chat' | 'price'. */
const browser: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), w = a.w ?? 760, h = a.h ?? 470, s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const url: string = a.url || 'my-startup.ai', ta = a.typeAt ?? (a.at ?? 0) + 0.4, n = Math.floor(clamp(win(t, ta, a.typeDur ?? 1.6)) * url.length);
  const shown = url.slice(0, n), dot = url.lastIndexOf('.'), base = shown.slice(0, Math.min(n, dot)), tld = n > dot ? shown.slice(dot) : '';
  const caret = Math.sin(t * 8) > 0 && n < url.length;
    let page: string = a.page || 'site';
  if (Array.isArray(a.pages)) for (const [pt, pv] of a.pages as [number, string][]) if (t >= pt) page = pv;
  const o = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'br' + i} opacity={o} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.tilt ?? 0})`}>
    <rect x={-w / 2 + 10} y={-h / 2 + 12} width={w} height={h} rx={22} fill={OL} opacity={0.25} />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={22} fill={K.white} stroke={OL} strokeWidth={6} />
    <path d={`M ${-w / 2} ${-h / 2 + 70} L ${w / 2} ${-h / 2 + 70}`} stroke={OL} strokeWidth={5} />
    {['#FF5A5F', '#FFC93C', '#3DBE6B'].map((c, k) => <circle key={k} cx={-w / 2 + 34 + k * 30} cy={-h / 2 + 36} r={10} fill={c} stroke={OL} strokeWidth={3} />)}
    <rect x={-w / 2 + 140} y={-h / 2 + 14} width={w - 170} height={44} rx={22} fill="#F1F3F8" stroke={OL} strokeWidth={4} />
    <text x={-w / 2 + 166} y={-h / 2 + 46} fontFamily={FONT} fontWeight={800} fontSize={28} fill={OL}>{base}<tspan fill="#E89A00" fontWeight={900}>{tld}</tspan>{caret ? '|' : ''}</text>
    {page === 'site' && <g><rect x={-w / 2 + 40} y={-h / 2 + 100} width={w * 0.5} height={40} rx={8} fill={col(a.color, '#7E57C2')} />
      {[0, 1, 2].map((l) => <rect key={l} x={-w / 2 + 40} y={-h / 2 + 170 + l * 36} width={w * (0.75 - l * 0.15)} height={18} rx={9} fill="#D9DEEA" />)}
      <rect x={w / 2 - 230} y={h / 2 - 130} width={190} height={90} rx={14} fill="#B3E5FC" stroke={OL} strokeWidth={3} />
      <circle cx={w / 2 - 135} cy={h / 2 - 85} r={26} fill={K.gold} stroke={OL} strokeWidth={3} /></g>}
    {page === 'chat' && <g>{[0, 1, 2].map((k) => { const ap = t >= (a.at ?? 0) + 0.6 + k * 0.9; if (!ap) return null; const me = k % 2 === 0;
      return <g key={k}><rect x={me ? -w / 2 + 40 : -w / 2 + w * 0.35} y={-h / 2 + 100 + k * 100} width={w * 0.58} height={70} rx={24} fill={me ? '#E3F2FD' : '#EDE7F6'} stroke={OL} strokeWidth={3} />
        {[0, 1].map((l) => <rect key={l} x={(me ? -w / 2 + 64 : -w / 2 + w * 0.35 + 24)} y={-h / 2 + 118 + k * 100 + l * 22} width={w * (0.45 - l * 0.12)} height={12} rx={6} fill="#B0BEC5" />)}</g>; })}</g>}
    {(page === 'sold' || page === 'price') && <g><T x={0} y={-h / 2 + 170} s={44}>{a.text || 'SOLD!'}</T>
      {a.sub && <T x={0} y={-h / 2 + 220} s={26} w={700}>{a.sub}</T>}
      <rect x={-130} y={h / 2 - 140} width={260} height={80} rx={40} fill={K.green} stroke={OL} strokeWidth={5} /><T x={0} y={h / 2 - 88} s={34} c={K.white}>{a.button || 'BUY'}</T></g>}
    {page === 'expired' && <g><T x={0} y={-h / 2 + 190} s={60} c={K.red}>EXPIRED</T><T x={0} y={-h / 2 + 250} s={26} w={700}>{a.sub || 'not renewed'}</T>
      <path d={`M ${-w * 0.3} ${h / 2 - 100} L ${w * 0.3} ${h / 2 - 100}`} stroke="#D9DEEA" strokeWidth={18} strokeLinecap="round" /></g>}
  </g>;
};

/** A rolling counter from `from` to `to` (between at and at+dur), with prefix/suffix and a label underneath. */
const counter: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const steps: [number, number][] = a.steps || [[a.at ?? 0, a.from ?? 0], [(a.at ?? 0) + (a.dur ?? 2), a.to ?? 100]];
  const v = kf(steps, t), dec = a.decimals ?? 0, str = v.toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec});
  const txt = (a.prefix || '') + str + (a.suffix || ''), w = Math.max(320, txt.length * 44 + 80);
  return <g key={'cn' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-w / 2} y={-70} width={w} height={130} rx={24} fill="#1B2438" stroke={OL} strokeWidth={6} />
    <T x={0} y={20} s={72} c={K.gold}>{txt}</T>
    {a.text && <g><rect x={-Math.max(140, a.text.length * 9 + 30)} y={74} width={Math.max(280, a.text.length * 18 + 60)} height={44} rx={12} fill={K.white} stroke={OL} strokeWidth={4} /><T x={0} y={105} s={24}>{a.text}</T></g>}
  </g>;
};

/** 100 share certificates in a 10x10 grid; `groups` [{n, color, label, at}] fill cells in order (who owns what);
 *  `owed` {n, at, label}: a column of dashed red certificates that short sellers must buy back, shaking when they can't. */
const shares: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 420), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5), cw = 54, ch = 38, gap = 8;
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const groups: any[] = a.groups || [], cells: React.ReactNode[] = [], W = 10 * (cw + gap) - gap, H = 10 * (ch + gap) - gap;
  let idx = 0;
  groups.forEach((g, gi) => { const at = g.at ?? 0, n = g.n ?? 0;
    for (let k = 0; k < n && idx < 100; k++, idx++) { const ap = pop(t, at + k * (g.step ?? 0.02), 0.3); if (ap <= 0) continue;
      const cx = -W / 2 + (idx % 10) * (cw + gap) + cw / 2, cy = -H / 2 + Math.floor(idx / 10) * (ch + gap) + ch / 2;
      cells.push(<g key={'c' + idx} transform={`translate(${cx} ${cy}) scale(${ap})`}><rect x={-cw / 2} y={-ch / 2} width={cw} height={ch} rx={6} fill={col(g.color, K.white)} stroke={OL} strokeWidth={3} />
        <path d={`M ${-cw / 2 + 10} ${-4} L ${cw / 2 - 10} ${-4} M ${-cw / 2 + 10} 8 L ${cw / 2 - 22} 8`} stroke={OL} strokeWidth={2} opacity={0.4} /></g>); } });
  const ow = a.owed, owN = ow ? ow.n ?? 12 : 0, shake = ow && ow.shakeAt !== undefined && t >= ow.shakeAt ? Math.sin(t * 40) * 5 : 0;
  return <g key={'sh' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 - 24} y={-H / 2 - 24} width={W + 48} height={H + 48} rx={20} fill="#1B2438" stroke={OL} strokeWidth={6} />
    {cells}
    {groups.map((g, gi) => g.label && t >= (g.at ?? 0) ? <g key={'l' + gi}><rect x={-W / 2 - 24 + gi * ((W + 48) / Math.max(3, groups.length))} y={H / 2 + 40} width={(W + 48) / Math.max(3, groups.length) - 12} height={56} rx={12} fill={col(g.color, K.white)} stroke={OL} strokeWidth={4} />
      <T x={-W / 2 - 24 + gi * ((W + 48) / Math.max(3, groups.length)) + ((W + 48) / Math.max(3, groups.length) - 12) / 2} y={H / 2 + 78} s={24}>{g.label}</T></g> : null)}
    {ow && t >= ow.at && <g transform={`translate(${W / 2 + 120 + shake} 0)`}>
      {Array.from({length: owN}, (_, k) => { const ap = pop(t, ow.at + k * 0.08, 0.3); return ap <= 0 ? null : <g key={k} transform={`translate(${(k % 2) * (cw + 10) - cw / 2 - 5} ${-H / 2 + Math.floor(k / 2) * (ch + gap) + ch / 2}) scale(${ap})`}>
        <rect x={-cw / 2} y={-ch / 2} width={cw} height={ch} rx={6} fill="#FFE1E1" stroke={K.red} strokeWidth={4} strokeDasharray="8 5" /><T x={0} y={9} s={22} c={K.red}>?</T></g>; })}
      <rect x={-110} y={H / 2 + 40} width={220} height={56} rx={12} fill="#FFCDD2" stroke={OL} strokeWidth={4} /><T x={0} y={H / 2 + 78} s={24}>{ow.label || 'OWED'}</T></g>}
  </g>;
};

/** A DDR memory stick (generic, no brand): green PCB, eight black chips, gold contacts; chips glow red from hotAt;
 *  `liftAt` raises the eight chips off the board (to count them); `label` sticker (e.g. "16 GB"). */
const ramstick: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const hot = a.hotAt !== undefined ? clamp(win(t, a.hotAt, 1.2)) : 0, lift = a.liftAt !== undefined ? E.outBack(win(t, a.liftAt, 0.9)) : 0;
  return <g key={'rs' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.tilt ?? 0})`}>
    <rect x={-420} y={-110} width={840} height={220} rx={14} fill="#2E7D4F" stroke={OL} strokeWidth={6} />
    {Array.from({length: 24}, (_, k) => <path key={k} d={`M ${-400 + k * 34} -96 l 0 ${30 + (k % 3) * 10}`} stroke="#7BD389" strokeWidth={2} opacity={0.5} />)}
    {Array.from({length: 40}, (_, k) => <rect key={'c' + k} x={-400 + k * 20} y={92} width={12} height={26} fill="#FFC93C" stroke={OL} strokeWidth={1.5} />)}
    <rect x={-20} y={96} width={24} height={30} fill={K.sky2} />
    {Array.from({length: 8}, (_, k) => { const cx = -350 + k * 100, ly = -lift * (60 + (k % 2) * 30);
      const g = hot * (0.6 + 0.4 * Math.sin(t * 6 + k));
      return <g key={k} transform={`translate(${cx} ${-10 + ly})`}>
        {g > 0 && <rect x={-46} y={-56} width={92} height={112} rx={10} fill={K.red} opacity={g * 0.5} />}
        <rect x={-38} y={-48} width={76} height={96} rx={6} fill="#1B1F27" stroke={OL} strokeWidth={4} />
        <circle cx={-26} cy={-36} r={4} fill="#5C6B7A" />
        {lift > 0.5 && <text x={0} y={8} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={24} fill={K.gold}>{k + 1}</text>}
      </g>; })}
    {a.label && <g><rect x={-120} y={-96} width={240} height={36} rx={6} fill={K.white} stroke={OL} strokeWidth={3} transform="translate(0 -40)" />
      <T x={0} y={-112} s={26}>{a.label}</T></g>}
  </g>;
};

/** A hanging price tag on a string; `pages` [[t, text]] flip the price; a page with red: true turns it red. */
const pricetag: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  let txt = a.text || '$0', red = false, lastT = -99;
  for (const p of (a.pages || []) as any[]) if (t >= p[0]) { txt = p[1]; red = !!p[2]; lastT = p[0]; }
  const flip = Math.abs(Math.cos(Math.min(1, (t - lastT) / 0.5) * Math.PI)), sw = Math.sin(t * 1.6) * 6;
  const w = Math.max(220, txt.length * 44 + 70);
  return <g key={'pt' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${sw})`}>
    <path d={`M 0 ${-220} L 0 -70`} stroke={OL} strokeWidth={4} />
    <g transform={`scale(1 ${t - lastT < 0.5 ? flip : 1})`}>
      <path d={`M ${-w / 2} -60 L ${w / 2 - 50} -60 L ${w / 2} 0 L ${w / 2 - 50} 60 L ${-w / 2} 60 Z`} fill={red ? '#FFCDD2' : K.white} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <circle cx={w / 2 - 54} cy={0} r={12} fill={K.sky2} stroke={OL} strokeWidth={4} />
      <T x={-26} y={22} s={64} c={red ? K.red : OL}>{txt}</T>
      {a.sub && <T x={-26} y={96} s={22} w={700}>{a.sub}</T>}
    </g>
  </g>;
};

/** An AI accelerator package: a glowing processor die flanked by HBM stacks whose layers build up from `at`. */
const hbm: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 520), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const layers = a.layers ?? 8, build = clamp(win(t, (a.at ?? 0) + 0.4, a.dur ?? 3));
  const stack = (sx: number, k: number) => <g key={k} transform={`translate(${sx} 0)`}>
    {Array.from({length: Math.ceil(layers * build)}, (_, l) => <rect key={l} x={-60} y={60 - l * 22} width={120} height={18} rx={3}
      fill={l % 2 ? '#4FB3F6' : '#2F6FD1'} stroke={OL} strokeWidth={3} />)}
    {build >= 1 && <T x={0} y={60 - layers * 22 - 14} s={22} c={K.white}>HBM</T>}
  </g>;
  return <g key={'hb' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-520} y={80} width={1040} height={60} rx={10} fill="#2E7D4F" stroke={OL} strokeWidth={5} />
    <rect x={-170} y={-120} width={340} height={200} rx={14} fill="#1B1F27" stroke={OL} strokeWidth={6} />
    <rect x={-140} y={-92} width={280} height={144} rx={8} fill="#7DF29A" opacity={0.25 + 0.15 * Math.sin(t * 3)} />
    <T x={0} y={-6} s={32} c="#7DF29A">{a.text || 'AI CHIP'}</T>
    {[-420, -280, 280, 420].map((sx, k) => stack(sx, k))}
  </g>;
};

/** Renewal clock: the hand sweeps a full turn every `period` s; each lap pops a coin ("PAY AGAIN"). */
const clock: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5), per = a.period ?? 3;
  if (s <= 0) return null;
  const st = a.at ?? 0, u = ((t - st) / per) % 1, lap = Math.floor((t - st) / per), stop = a.stopAt !== undefined && t >= a.stopAt;
  const an = (stop ? ((a.stopAt - st) / per) % 1 : u) * Math.PI * 2;
  return <g key={'ck' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={110} fill={K.white} stroke={OL} strokeWidth={7} />
    <path d={`M 0 0 L 0 -100 A 100 100 0 ${an > Math.PI ? 1 : 0} 1 ${100 * Math.sin(an)} ${-100 * Math.cos(an)} Z`} fill={stop ? '#FFCDD2' : '#C8E6C9'} />
    {Array.from({length: 12}, (_, k) => <path key={k} d={`M ${92 * Math.sin(k * Math.PI / 6)} ${-92 * Math.cos(k * Math.PI / 6)} L ${104 * Math.sin(k * Math.PI / 6)} ${-104 * Math.cos(k * Math.PI / 6)}`} stroke={OL} strokeWidth={4} />)}
    <path d={`M 0 0 L ${80 * Math.sin(an)} ${-80 * Math.cos(an)}`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
    <circle r={10} fill={OL} />
    <rect x={-80} y={120} width={160} height={44} rx={12} fill={col(a.color, K.gold)} stroke={OL} strokeWidth={4} /><T x={0} y={152} s={24}>{stop ? (a.stopText || 'STOPPED') : (a.text || '2 YEARS')}</T>
    {!stop && lap >= 0 && u < 0.35 && t > st + 0.5 && <g transform={`translate(0 ${-130 - 120 * u}) scale(${Math.abs(Math.cos(t * 6))} 1)`} opacity={1 - u / 0.35}>
      <circle r={26} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={10} s={28}>$</T></g>}
  </g>;
};

/** A ship in the water (waterline at the floor): 'container' | 'tanker' | 'liner'. Its stern pennant shows a TEXT label (never a real
 * national flag design); `flag` may be keyframes [[t, text]]. `port` is the home port painted on the stern. rustAt/sadAt for abandoned ships. */
const ship: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6), fl = a.flip ? -1 : 1, ty = a.type || 'container';
  if (s <= 0) return null;
  let flag: string = typeof a.flag === 'string' ? a.flag : '';
  if (Array.isArray(a.flag)) for (const [ft, fv] of a.flag as [number, string][]) if (t >= ft) flag = fv;
  const rust = a.rustAt !== undefined ? clamp(win(t, a.rustAt, 2)) : a.rust ? 1 : 0, sad = a.sadAt !== undefined && t >= a.sadAt;
  const bob = Math.sin(t * 1.6 + i) * 5, tilt = Math.sin(t * 1.1 + i) * 1.2, hull = col(a.color, ty === 'tanker' ? '#C62828' : ty === 'liner' ? K.white : ty === 'dhow' ? '#8D5A3B' : '#1E5AA8');
  const flagSwap = Array.isArray(a.flag) ? (a.flag as [number, string][]).some(([ft]) => t >= ft && t < ft + 0.5) : false;
  return <g key={'sh' + i} transform={`translate(${x} ${f + 30 + bob}) rotate(${tilt}) scale(${s * fl} ${s})`}>
    {ty === 'container' && Array.from({length: 3}, (_, r) => Array.from({length: 8}, (_, c2) => <rect key={r + '-' + c2} x={-330 + c2 * 64} y={-150 - r * 40} width={60} height={38} rx={3}
      fill={['#E53935', '#1E88E5', '#FFB300', '#43A047', '#8E24AA', '#F4511E'][(r * 3 + c2 + i) % 6]} stroke={OL} strokeWidth={3} />))}
    {ty === 'tanker' && <g><rect x={-330} y={-130} width={480} height={20} fill="#9E9E9E" stroke={OL} strokeWidth={3} />
      {[-260, -120, 20].map((dx) => <ellipse key={dx} cx={dx} cy={-128} rx={46} ry={14} fill="#BDBDBD" stroke={OL} strokeWidth={3} />)}</g>}
    {ty === 'dhow' && <g><path d="M 40 -110 L 40 -420 M 40 -400 Q 260 -300 300 -120 L 40 -120 Z" fill="#FFF3E0" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      {[0, 1, 2].map((k) => <rect key={k} x={-280 + k * 90} y={-160} width={70} height={50} rx={6} fill={['#8D6E63', '#A1887F', '#BCAAA4'][k]} stroke={OL} strokeWidth={3} />)}</g>}
    {ty === 'fishing' && <g><rect x={-60} y={-200} width={140} height={90} rx={8} fill={K.cream} stroke={OL} strokeWidth={4} />
      <rect x={-44} y={-186} width={40} height={28} rx={4} fill="#9FE3FF" stroke={OL} strokeWidth={2} /><rect x={14} y={-186} width={40} height={28} rx={4} fill="#9FE3FF" stroke={OL} strokeWidth={2} />
      <path d="M 160 -110 L 160 -300 L 330 -130" fill="none" stroke={OL} strokeWidth={6} strokeLinecap="round" />
      <path d={`M 330 -130 L ${330 + 10 * Math.sin(t * 2)} -40`} stroke={OL} strokeWidth={3} /></g>}
    {ty === 'liner' && <g><rect x={-320} y={-200} width={560} height={90} rx={12} fill={K.white} stroke={OL} strokeWidth={4} />
      {Array.from({length: 10}, (_, k) => <circle key={k} cx={-290 + k * 54} cy={-155} r={10} fill="#9FE3FF" stroke={OL} strokeWidth={2} />)}
      {[-120, 40].map((dx) => <g key={dx}><rect x={dx} y={-290} width={60} height={90} fill="#E53935" stroke={OL} strokeWidth={4} /><rect x={dx} y={-290} width={60} height={22} fill={OL} /></g>)}</g>}
    <rect x={190} y={-260} width={110} height={150} rx={8} fill={K.cream} stroke={OL} strokeWidth={4} />
    {[0, 1, 2].map((r) => <rect key={r} x={204} y={-246 + r * 40} width={82} height={20} rx={3} fill={sad ? '#5C6B7A' : '#9FE3FF'} stroke={OL} strokeWidth={2} />)}
    <path d="M -380 -110 L 400 -110 L 350 40 L -340 40 Z" fill={hull} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <path d="M -370 -60 L 386 -60" stroke={K.white} strokeWidth={8} opacity={0.6} />
    {rust > 0 && Array.from({length: 7}, (_, k) => <ellipse key={k} cx={-300 + k * 100 + 20 * rnd(k)} cy={-40 + 30 * rnd(k + 2)} rx={30 * rust} ry={16 * rust} fill="#8D4E2A" opacity={0.8} />)}
    <path d="M -340 40 L 350 40" stroke="#B71C1C" strokeWidth={10} />
    {a.name && <text x={-330} y={-74} fontFamily={FONT} fontWeight={900} fontSize={30} fill={K.white} transform={a.flip ? 'scale(-1 1) translate(660 0)' : undefined}>{a.name}</text>}
    {a.port && <g transform={a.flip ? 'scale(-1 1)' : undefined}><rect x={a.flip ? 250 : -380} y={-34} width={150} height={40} rx={6} fill={K.white} stroke={OL} strokeWidth={3} />
      <T x={a.flip ? 325 : -305} y={-6} s={22}>{a.port}</T></g>}
    <path d="M -360 -110 L -360 -330" stroke={OL} strokeWidth={6} />
    {flag && <g transform={`translate(-360 -330) scale(${flagSwap ? 1 - 0.6 * Math.sin(Math.PI * win(t, (a.flag as [number, string][]).find(([ft]) => t >= ft && t < ft + 0.5)![0], 0.5)) : 1} 1)`}>
      <path d={`M 0 0 L ${-(flag.length * 17 + 40)} ${4 + 6 * Math.sin(t * 5)} L ${-(flag.length * 17 + 40)} ${56 + 6 * Math.sin(t * 5 + 1)} L 0 60 Z`} fill={col(a.flagColor, K.gold)} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <text x={-(flag.length * 17 + 40) / 2} y={40} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={28} fill={OL} transform={a.flip ? `scale(-1 1) translate(${flag.length * 17 + 40} 0)` : undefined}>{flag}</text></g>}
    {Array.from({length: a.crew ?? 0}, (_, k) => <g key={'cw' + k} transform={`translate(${-200 + k * 70} ${ty === 'container' ? -270 : -150})`}>
      <rect x={-12} y={-10} width={24} height={34} rx={8} fill={['#FF8A65', '#4FB3F6', '#FFC93C', '#7BD389'][k % 4]} stroke={OL} strokeWidth={3} />
      <circle cx={0} cy={-24} r={15} fill={K.skin[k % 4]} stroke={OL} strokeWidth={3} />
      <path d={sad ? 'M -6 -14 Q 0 -20 6 -14' : 'M -6 -18 Q 0 -12 6 -18'} fill="none" stroke={OL} strokeWidth={2.5} />
      {!sad && <path d={`M 12 -4 L ${26} ${-24 - 10 * Math.abs(Math.sin(t * 4 + k))}`} stroke={K.skin[k % 4]} strokeWidth={7} strokeLinecap="round" />}</g>)}
    {a.smoke !== false && !sad && Array.from({length: 3}, (_, k) => { const u = (t * 0.4 + k / 3) % 1; return <circle key={'sm' + k} cx={240 - u * 80} cy={-280 - u * 160} r={14 + 24 * u} fill="#ECEFF1" opacity={0.8 * (1 - u)} />; })}
  </g>;
};

/** The ship's passport: a booklet that opens (openAt) on fields [[label, value]] and gets a stamp (stampAt). */
const passport: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const op = a.openAt !== undefined ? E.inOut(win(t, a.openAt, 0.9)) : 0, fields: [string, string][] = a.fields || [];
  let fv = fields;
  if (Array.isArray(a.swaps)) for (const [st, k, v] of a.swaps as [number, number, string][]) if (t >= st) fv = fv.map((r, j) => (j === k ? [r[0], v] : r));
  const sa = a.stampAt, hit = sa !== undefined && t >= sa, o = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'pp' + i} opacity={o} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 1.2) * 1.5})`}>
    <rect x={-10} y={-210} width={340} height={420} rx={18} fill="#F5F0E1" stroke={OL} strokeWidth={5} />
    {fv.map(([l, v], k) => <g key={k}><T x={30} y={-150 + k * 74} s={18} a="start" w={700} c="#6B7280">{l}</T><T x={30} y={-122 + k * 74} s={30} a="start">{v}</T></g>)}
    {hit && <g transform={`translate(200 130) rotate(-14) scale(${E.outBack(win(t, sa, 0.3))})`}>
      <rect x={-110} y={-36} width={220} height={72} rx={10} fill="none" stroke={col(a.stampColor, K.green)} strokeWidth={7} />
      <T x={0} y={12} s={32} c={col(a.stampColor, K.green)}>{a.stamp || 'REGISTERED'}</T></g>}
    <g transform={`translate(-10 0) scale(${1 - 2 * op} 1) translate(10 0)`}>
      <rect x={-10} y={-210} width={340} height={420} rx={18} fill={op > 0.5 ? '#F5F0E1' : col(a.color, '#1E3A6E')} stroke={OL} strokeWidth={5} />
      {op < 0.5 && <g><circle cx={160} cy={-40} r={60} fill="none" stroke={K.gold} strokeWidth={6} />
        <path d="M 120 -40 L 200 -40 M 160 -80 L 160 0 M 130 -10 Q 160 20 190 -10" stroke={K.gold} strokeWidth={5} fill="none" />
        <T x={160} y={-140} s={30} c={K.gold}>{a.text || 'SHIP PASSPORT'}</T><T x={160} y={90} s={22} c={K.gold} w={700}>{a.sub || 'certificate of registry'}</T></g>}
    </g>
  </g>;
};

/** EUV light source: tin droplets fall; a pre-pulse flattens one, the main pulse turns it into a bright plasma;
 * a collector mirror gathers the violet light (rate = droplets shown per second, slowed down for the eye). */
const tinsource: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const st = a.at ?? 0, per = 1 / (a.rate ?? 1.2), u = ((t - st) % per) / per, on = t >= (a.laserAt ?? st), pl = a.plasmaAt === undefined || t >= a.plasmaAt;
  const dy = lerp(-260, 0, Math.min(1, u / 0.55)), flat = on && u > 0.55 ? Math.min(1, (u - 0.55) / 0.12) : 0, boom = on && pl && u > 0.7 ? 1 - (u - 0.7) / 0.3 : 0;
  return <g key={'ts' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-360} y={-330} width={720} height={560} rx={30} fill="#1B2438" stroke={OL} strokeWidth={6} />
    <path d="M -200 160 Q 0 0 200 160" fill="none" stroke="#B0BEC5" strokeWidth={22} strokeLinecap="round" />
    <path d="M -200 160 Q 0 0 200 160" fill="none" stroke={K.white} strokeWidth={6} opacity={0.6} />
    <T x={0} y={205} s={22} c="#B0BEC5">COLLECTOR MIRROR</T>
    <rect x={-30} y={-320} width={60} height={50} rx={8} fill="#78909C" stroke={OL} strokeWidth={3} />
    <T x={0} y={-282} s={16} c={K.white}>TIN</T>
    {u < 0.7 && <ellipse cx={0} cy={dy} rx={12 + 26 * flat} ry={12 - 8 * flat} fill="#CFD8DC" stroke={OL} strokeWidth={3} />}
    {[0.25, 0.5].map((o, k) => { const uu = (u + o) % 1; if (uu > 0.55) return null; return <circle key={k} cx={0} cy={lerp(-260, 0, uu / 0.55)} r={10} fill="#CFD8DC" stroke={OL} strokeWidth={2} opacity={0.8} />; })}
    {on && u > 0.5 && u < 0.6 && <path d="M -340 0 L -20 0" stroke="#FF5252" strokeWidth={8} opacity={0.8} />}
    {on && u > 0.66 && u < 0.76 && <path d="M -340 0 L -20 0" stroke="#FF1744" strokeWidth={22} />}
    {boom > 0 && <g><circle r={30 + 90 * (1 - boom)} fill="#E1BEE7" opacity={boom} /><circle r={20 + 40 * (1 - boom)} fill={K.white} opacity={boom} />
      {Array.from({length: 10}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos(k * 0.63) * (90 + 120 * (1 - boom))} ${Math.sin(k * 0.63) * (90 + 120 * (1 - boom))}`} stroke="#B388FF" strokeWidth={6} opacity={boom} />)}</g>}
    {on && pl && <path d={`M -150 120 L 0 0 L 150 120 M 0 0 L 0 -200`} stroke="#B388FF" strokeWidth={4} opacity={0.3 + 0.3 * Math.sin(t * 20)} />}
    <T x={-200} y={-30} s={20} c="#FF8A80" a="middle">{on ? 'LASER' : ''}</T>
    {a.text && <T x={0} y={-350} s={30}>{a.text}</T>}
  </g>;
};

/** A vacuum chamber where a violet beam bounces down a chain of mirrors onto a wafer. */
const mirrors: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6), n = a.n ?? 6;
  if (s <= 0) return null;
  const pts: [number, number][] = Array.from({length: n}, (_, k) => [-300 + (k % 2) * 520 - (k % 2 ? 0 : 0), -220 + k * 80]);
  const u = clamp(win(t, a.beamAt ?? (a.at ?? 0) + 0.5, a.dur ?? 3)) * (n - 1);
  const path: string[] = [];
  for (let k = 0; k <= Math.floor(u) && k < n; k++) path.push(`${k ? 'L' : 'M'} ${pts[k][0]} ${pts[k][1]}`);
  const k0 = Math.floor(u);
  if (k0 < n - 1) path.push(`L ${lerp(pts[k0][0], pts[k0 + 1][0], u - k0)} ${lerp(pts[k0][1], pts[k0 + 1][1], u - k0)}`);
  return <g key={'mr' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-400} y={-300} width={800} height={600} rx={40} fill="#263238" stroke={OL} strokeWidth={6} />
    <T x={0} y={-250} s={26} c="#90A4AE">VACUUM</T>
    {pts.map((q, k) => <rect key={k} x={q[0] - 50} y={q[1] - 10} width={100} height={20} rx={8} fill="#CFD8DC" stroke={OL} strokeWidth={3} transform={`rotate(${k % 2 ? -20 : 20} ${q[0]} ${q[1]})`} />)}
    <path d={path.join(' ')} fill="none" stroke="#B388FF" strokeWidth={10} strokeLinejoin="round" opacity={0.85} />
    <ellipse cx={pts[n - 1][0]} cy={pts[n - 1][1] + 90} rx={120} ry={22} fill="url(#wafg2)" stroke={OL} strokeWidth={4} />
    {u >= n - 1.01 && <circle cx={pts[n - 1][0]} cy={pts[n - 1][1] + 80} r={10 + 4 * Math.sin(t * 10)} fill={K.white} />}
    <defs><linearGradient id="wafg2" x1="0" x2="1"><stop offset="0%" stopColor="#B39DDB" /><stop offset="50%" stopColor="#80DEEA" /><stop offset="100%" stopColor="#F48FB1" /></linearGradient></defs>
  </g>;
};

/** Nanoimprint lithography (step and repeat): an inkjet head drops resist on one field of the wafer, the quartz mold presses
 *  down like a stamp, a UV lamp flashes, the mold lifts and the field shows its printed lines; then the wafer steps on.
 *  `rate` = imprints per second; `defectAt` lands a dust particle (that field prints red); `stopAt` freezes the cycle. */
const imprint: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.7);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const st = (a.at ?? 0) + 0.6, per = 1 / (a.rate ?? 0.5), tt = Math.max(0, (a.stopAt !== undefined ? Math.min(t, a.stopAt) : t) - st);
  const cyc = Math.floor(tt / per), u = (tt % per) / per, running = t >= st;
  const drop = running && u < 0.25, press = running ? (u < 0.25 ? 0 : u < 0.45 ? E.inOut((u - 0.25) / 0.2) : u < 0.7 ? 1 : 1 - E.inOut((u - 0.7) / 0.2)) : 0;
  const uv = running && u > 0.48 && u < 0.66, n = 7, cell = 64, done = running ? Math.min(cyc + (u > 0.7 ? 1 : 0), n * 2) : 0;
  const defect = a.defectAt !== undefined && t >= a.defectAt, defCell = a.defectCell ?? 5;
  const fields: React.ReactNode[] = [];
  for (let k = 0; k < n * 2; k++) {
    const fx = -((n - 1) * cell) / 2 + (k % n) * cell, fy = k < n ? -22 : 22, on = k < done, bad = defect && k === defCell;
    fields.push(<g key={k}><rect x={fx - 28} y={fy - 18} width={56} height={36} rx={3} fill={on ? (bad ? '#FF7B7B' : '#2A3550') : '#C5CAE9'} stroke={OL} strokeWidth={2} />
      {on && !bad && [0, 1, 2, 3].map((l) => <path key={l} d={`M ${fx - 22 + l * 13} ${fy - 13} L ${fx - 22 + l * 13} ${fy + 13}`} stroke="#7DF29A" strokeWidth={3} />)}</g>);
  }
  const cur = Math.min(done, n * 2 - 1), hx = -((n - 1) * cell) / 2 + (cur % n) * cell, hy = cur < n ? -22 : 22;
  const mb = lerp(-400, -150 + hy - 16, press);   // mold bottom (world y inside the machine)
  return <g key={'ni' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-470} y={-560} width={940} height={560} rx={26} fill="#EEF1F6" stroke={OL} strokeWidth={6} />
    <rect x={-470} y={-560} width={940} height={60} rx={26} fill={col(a.color, '#C62828')} stroke={OL} strokeWidth={6} />
    <T x={0} y={-518} s={30} c={K.white}>{a.text || 'NANOIMPRINT'}</T>
    <rect x={-400} y={-480} width={800} height={400} rx={16} fill="#1B2438" stroke={OL} strokeWidth={5} />
    {/* wafer stage (top view squashed) */}
    <g transform="translate(0 -150)">
      <ellipse cx={0} cy={0} rx={300} ry={70} fill="url(#wafg3)" stroke={OL} strokeWidth={5} />
      <defs><linearGradient id="wafg3" x1="0" x2="1"><stop offset="0%" stopColor="#B39DDB" /><stop offset="50%" stopColor="#80DEEA" /><stop offset="100%" stopColor="#F48FB1" /></linearGradient></defs>
      {fields}
      {defect && <circle cx={-((n - 1) * cell) / 2 + (defCell % n) * cell} cy={defCell < n ? -22 : 22} r={7 + 2 * Math.sin(t * 9)} fill="#FFEB3B" stroke={OL} strokeWidth={2} />}
      {drop && [0, 1, 2, 3, 4].map((d) => { const v = clamp((u - d * 0.03) / 0.18); return v > 0 && v < 1 ? <circle key={d} cx={hx - 20 + d * 10} cy={lerp(-200, hy, v) - hy + hy} r={5} fill="#80D8FF" /> : null; })}
    </g>
    {/* inkjet head on a rail */}
    <rect x={-380} y={-460} width={760} height={14} rx={6} fill="#90A4AE" />
    <rect x={hx - 34} y={-452} width={68} height={40} rx={8} fill="#FFB300" stroke={OL} strokeWidth={3} />
    <T x={hx} y={-426} s={14}>INK</T>
    {/* quartz mold (stamp) */}
    <path d={`M ${hx} -478 L ${hx} ${mb - 62}`} stroke="#B0BEC5" strokeWidth={18} />
    <rect x={hx - 80} y={mb - 70} width={160} height={58} rx={8} fill="#B3E5FC" stroke={OL} strokeWidth={5} opacity={0.95} />
    <path d={`M ${hx - 70} ${mb - 58} L ${hx + 70} ${mb - 58}`} stroke={K.white} strokeWidth={4} opacity={0.8} />
    {Array.from({length: 9}, (_, k) => <rect key={k} x={hx - 68 + k * 16} y={mb - 12} width={8} height={12} fill="#81D4FA" stroke={OL} strokeWidth={2} />)}
    <T x={hx + 130} y={mb - 30} s={18} c="#B3E5FC" a="start">QUARTZ MOLD</T>
    {uv && <g><path d={`M ${hx - 120} -470 L ${hx - 60} ${mb - 70} M ${hx + 120} -470 L ${hx + 60} ${mb - 70} M ${hx - 40} -470 L ${hx - 20} ${mb - 70} M ${hx + 40} -470 L ${hx + 20} ${mb - 70}`} stroke="#E1BEE7" strokeWidth={6} opacity={0.85} />
      <circle cx={hx - 150} cy={-462} r={20} fill="#EA80FC" stroke={OL} strokeWidth={3} /></g>}
    <T x={330} y={-440} s={18} c="#B0BEC5">{uv ? 'UV LAMP' : press > 0.9 ? 'PRESS' : drop ? 'RESIST' : ''}</T>
    {a.sub && <g><rect x={-250} y={-70} width={500} height={50} rx={10} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={-35} s={24}>{a.sub}</T></g>}
  </g>;
};

/** A compact accelerator (mode 'xray') or a helium-atom source (mode 'atoms') firing a beam down onto a small wafer. */
const beamsrc: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const atoms = a.mode === 'atoms', on = t >= (a.fireAt ?? (a.at ?? 0) + 0.8), c = atoms ? '#FFD54F' : '#80D8FF';
  const ang = t * 4.2;
  return <g key={'bm' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {atoms ? <g>
      <path d="M -90 -260 L 90 -260 L 60 -80 L -60 -80 Z" fill="#455A64" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <ellipse cx={0} cy={-80} rx={60} ry={16} fill="#263238" stroke={OL} strokeWidth={4} />
      {[0, 1, 2].map((k) => <path key={k} d={`M -70 ${-220 + k * 45} L 70 ${-220 + k * 45}`} stroke="#90A4AE" strokeWidth={5} />)}
      <T x={0} y={-285} s={24} c={K.white}>HELIUM ATOMS</T>
    </g> : <g>
      <ellipse cx={0} cy={-200} rx={230} ry={90} fill="none" stroke="#546E7A" strokeWidth={30} />
      <ellipse cx={0} cy={-200} rx={230} ry={90} fill="none" stroke="#90A4AE" strokeWidth={10} />
      {Array.from({length: 8}, (_, k) => <rect key={k} x={230 * Math.cos(k * Math.PI / 4) - 16} y={-200 + 90 * Math.sin(k * Math.PI / 4) - 22} width={32} height={44} rx={6} fill="#FF7043" stroke={OL} strokeWidth={3} />)}
      <circle cx={230 * Math.cos(ang)} cy={-200 + 90 * Math.sin(ang)} r={12} fill={K.white} stroke={c} strokeWidth={5} />
      <T x={0} y={-195} s={24} c={K.white}>ACCELERATOR</T>
    </g>}
    {on && (atoms
      ? Array.from({length: 14}, (_, k) => { const v = ((t * 1.3 + k / 14) % 1); return <circle key={k} cx={(rnd(k) - 0.5) * 40 * (1 - v)} cy={lerp(-80, 140, v)} r={6} fill={c} stroke={OL} strokeWidth={1.5} />; })
      : <g><path d="M 0 -110 L 0 140" stroke={c} strokeWidth={14} opacity={0.35 + 0.3 * Math.sin(t * 18)} /><path d="M 0 -110 L 0 140" stroke={K.white} strokeWidth={4} /></g>)}
    <ellipse cx={0} cy={160} rx={150} ry={30} fill="url(#wafg2)" stroke={OL} strokeWidth={4} />
    {on && <circle cx={0} cy={156} r={10 + 5 * Math.sin(t * 12)} fill={K.white} opacity={0.9} />}
    {a.text && <g><rect x={-190} y={215} width={380} height={52} rx={12} fill={col(a.color, K.gold)} stroke={OL} strokeWidth={4} /><T x={0} y={251} s={26}>{a.text}</T></g>}
    {a.sub && <T x={0} y={300} s={22} c={a.subc || OL}>{a.sub}</T>}
  </g>;
};

/** A giant low factory that builds section by section (progress 0..1 keyframes); `compare` draws a dashed outline of a
 *  reference building (e.g. the current largest) at `compareW` of its width; `glowAt` lights the windows. */
const megafab: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.7);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const W = a.w ?? 1400, H = a.h ?? 220, n = a.n ?? 10, prog = clamp(kf(a.progress, t, 1)), built = prog * n;
  const lit = a.glowAt !== undefined && t >= a.glowAt, cw = W * (a.compareW ?? 0.65);
  const secs: React.ReactNode[] = [];
  for (let k = 0; k < n; k++) {
    const u = clamp(built - k); if (u <= 0) continue;
    const sx = -W / 2 + (k * W) / n, sw = W / n, sh = H * E.outBack(u);
    secs.push(<g key={k}>
      <rect x={sx} y={-sh} width={sw + 1} height={sh} fill={k % 2 ? '#E3E8F0' : '#D5DCE7'} stroke={OL} strokeWidth={4} />
      <path d={`M ${sx} ${-sh} Q ${sx + sw / 2} ${-sh - 34 * u} ${sx + sw} ${-sh}`} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {u >= 1 && [0, 1, 2].map((r) => <rect key={r} x={sx + 14 + r * (sw - 28) / 3} y={-H + 50} width={(sw - 28) / 3 - 10} height={34} rx={4}
        fill={lit ? '#FFE082' : '#90A4AE'} opacity={lit ? 0.75 + 0.25 * Math.sin(t * 3 + k + r) : 0.8} stroke={OL} strokeWidth={2} />)}
      {u >= 1 && <rect x={sx + sw / 2 - 18} y={-60} width={36} height={60} fill="#546E7A" stroke={OL} strokeWidth={3} />}
    </g>);
  }
  const crane = prog < 1 ? -W / 2 + built * (W / n) : null;
  return <g key={'mf' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    {a.compareAt !== undefined && t >= a.compareAt && <g opacity={E.out(win(t, a.compareAt, 0.8))}>
      <rect x={-W / 2} y={-H - 70} width={cw} height={H + 70} fill="none" stroke={K.red} strokeWidth={6} strokeDasharray="22 14" />
      <rect x={-W / 2 + 10} y={-H - 120} width={Math.min(cw - 20, 560)} height={42} rx={10} fill={K.red} stroke={OL} strokeWidth={3} />
      <T x={-W / 2 + 10 + Math.min(cw - 20, 560) / 2} y={-H - 90} s={22} c={K.white}>{a.compareText || "TODAY'S LARGEST"}</T></g>}
    {secs}
    {crane !== null && <g transform={`translate(${crane} 0)`}>
      <path d={`M 0 0 L 0 ${-H - 220} L 160 ${-H - 220}`} fill="none" stroke="#FFB300" strokeWidth={10} />
      <path d={`M 120 ${-H - 220} L 120 ${-H - 120}`} stroke={OL} strokeWidth={3} /><rect x={104} y={-H - 124} width={32} height={22} fill="#90A4AE" stroke={OL} strokeWidth={2} /></g>}
    {a.text && prog > 0.3 && <g><rect x={-200} y={-H - 34 - 70} width={400} height={56} rx={12} fill={col(a.color, K.gold)} stroke={OL} strokeWidth={4} />
      <T x={0} y={-H - 64} s={30}>{a.text}</T></g>}
    {a.sub && <T x={0} y={44} s={24} c={a.subc || OL}>{a.sub}</T>}
  </g>;
};

/** An orbital AI satellite: solar wings unfold from `at`, a glowing compute core; optional sun rays from the left. */
const satellite: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 380) + Math.sin(t * 0.9 + i) * 10, s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const open = E.outBack(win(t, (a.at ?? 0) + 0.3, 1.2)), wing = 300 * open;
  return <g key={'sat' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.rot ?? -8})`}>
    {a.rays && Array.from({length: 6}, (_, k) => <path key={k} d={`M ${-900} ${-140 + k * 56} L ${-wing - 40} ${-60 + k * 24}`} stroke="#FFE082" strokeWidth={6}
      opacity={0.35 + 0.25 * Math.sin(t * 4 + k)} />)}
    {[-1, 1].map((d) => <g key={d}>
      <path d={`M ${d * 60} 0 L ${d * (60 + wing)} 0`} stroke="#B0BEC5" strokeWidth={8} />
      {Array.from({length: 4}, (_, k) => <rect key={k} x={d > 0 ? 70 + k * wing / 4 : -70 - (k + 1) * wing / 4} y={-70} width={wing / 4 - 6} height={140}
        fill="#1E3A8A" stroke="#90CAF9" strokeWidth={3} opacity={open} />)}
    </g>)}
    <rect x={-60} y={-80} width={120} height={160} rx={16} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
    <rect x={-40} y={-50} width={80} height={80} rx={8} fill="#1B1F27" stroke={OL} strokeWidth={3} />
    <rect x={-30} y={-40} width={60} height={60} rx={6} fill="#7DF29A" opacity={0.35 + 0.3 * Math.sin(t * 3)} />
    <T x={0} y={4} s={18} c="#7DF29A">AI</T>
    {a.text && <T x={0} y={130} s={26} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** Back-end line (OSAT): a wafer is diced (saw lines), dies hop onto a belt, drop into black packages with gold legs,
 *  and pass a test gate that lights a green tick (or red on `failEvery`). `rate` = chips per second once running. */
const osat: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.7);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const st = (a.at ?? 0) + 0.5, cut = clamp(win(t, st, 1.6)), run = t >= st + 1.6, rate = a.rate ?? 1.1, n = 7, failEvery = a.failEvery ?? 0;
  const L = -620, R = 620, belt = -150, chips: React.ReactNode[] = [];
  if (run) for (let k = 0; k < n; k++) {
    const u = ((t - st - 1.6) * rate * 0.18 + k / n) % 1, cx = lerp(L + 260, R, u), id = Math.floor((t - st - 1.6) * rate * 0.18 + k / n) * n + k;
    const packed = u > 0.38, tested = u > 0.7, bad = failEvery > 0 && id % failEvery === failEvery - 1;
    chips.push(<g key={k} transform={`translate(${cx} ${belt - 26})`}>
      {packed ? <g><rect x={-30} y={-22} width={60} height={44} rx={5} fill="#1B1F27" stroke={OL} strokeWidth={3} />
        {[-20, -7, 7, 20].map((lx) => <path key={lx} d={`M ${lx} 22 L ${lx} 32 M ${lx} -22 L ${lx} -32`} stroke="#FFC93C" strokeWidth={4} />)}
        <circle cx={-18} cy={-10} r={3} fill="#90A4AE" /></g>
        : <rect x={-18} y={-14} width={36} height={28} rx={3} fill="#80DEEA" stroke={OL} strokeWidth={2} />}
      {tested && <circle cx={0} cy={-56} r={14} fill={bad ? K.red : K.green} stroke={OL} strokeWidth={3} />}
      {tested && <path d={bad ? 'M -6 -62 L 6 -50 M 6 -62 L -6 -50' : 'M -7 -56 L -2 -50 L 8 -62'} stroke={K.white} strokeWidth={4} fill="none" />}
    </g>);
  }
  return <g key={'os' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    {/* wafer on the dicing table */}
    <rect x={L - 40} y={-120} width={280} height={120} rx={12} fill="#CFD8DC" stroke={OL} strokeWidth={5} />
    <g transform={`translate(${L + 100} -200)`}>
      <circle r={110} fill="url(#wafg2)" stroke={OL} strokeWidth={5} />
      {Array.from({length: 5}, (_, k) => <path key={'h' + k} d={`M -110 ${-80 + k * 40} L ${-110 + 220 * cut} ${-80 + k * 40}`} stroke={OL} strokeWidth={2.5} opacity={0.8} />)}
      {Array.from({length: 5}, (_, k) => <path key={'v' + k} d={`M ${-80 + k * 40} -110 L ${-80 + k * 40} ${-110 + 220 * cut}`} stroke={OL} strokeWidth={2.5} opacity={0.8} />)}
      {cut < 1 && <circle cx={-110 + 220 * cut} cy={-80 + (Math.floor(t * 3) % 5) * 40} r={16} fill="#B0BEC5" stroke={OL} strokeWidth={3} />}
      <defs><linearGradient id="wafg2" x1="0" x2="1"><stop offset="0%" stopColor="#B39DDB" /><stop offset="50%" stopColor="#80DEEA" /><stop offset="100%" stopColor="#F48FB1" /></linearGradient></defs>
    </g>
    <T x={L + 100} y={-330} s={22}>{cut < 1 ? 'DICING' : 'DIES'}</T>
    {/* belt */}
    <rect x={L + 240} y={belt} width={R - L - 220} height={26} rx={12} fill="#455A64" stroke={OL} strokeWidth={4} />
    {Array.from({length: 14}, (_, k) => <circle key={k} cx={L + 260 + ((k * 82 + t * 60) % (R - L - 240))} cy={belt + 13} r={6} fill="#90A4AE" />)}
    <rect x={L + 240} y={belt + 26} width={R - L - 220} height={-belt - 26} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
    {/* packaging press and test gate */}
    <g transform="translate(-20 0)"><rect x={-70} y={-360} width={140} height={130} rx={12} fill="#FFB300" stroke={OL} strokeWidth={4} />
      <path d={`M 0 -230 L 0 ${-200 + 30 * Math.abs(Math.sin(t * 3))}`} stroke={OL} strokeWidth={10} /><T x={0} y={-290} s={20}>PACKAGE</T></g>
    <g transform="translate(260 0)"><path d="M -70 -150 L -70 -330 L 70 -330 L 70 -150" fill="none" stroke="#26A69A" strokeWidth={12} />
      <rect x={-70} y={-370} width={140} height={44} rx={10} fill="#26A69A" stroke={OL} strokeWidth={4} /><T x={0} y={-340} s={20} c={K.white}>TEST</T></g>
    {chips}
    {a.text && <g><rect x={-260} y={-470} width={520} height={56} rx={12} fill={col(a.color, K.gold)} stroke={OL} strokeWidth={4} /><T x={0} y={-432} s={28}>{a.text}</T></g>}
  </g>;
};

/** A strategic material: mode 'bottle' (amber resist bottle, liquid level), 'tank' (gas cylinder with a pressure gauge) or
 *  'ingot' (stack of silver bars). `level` keyframes 0..1 drain it; `lockAt` drops a padlock and chain on it; `glow` pulses. */
const vessel: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6), y = a.y !== undefined ? kf(a.y, t, f) : f;
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const mode = a.mode || 'bottle', lv = clamp(kf(a.level, t, 1)), locked = a.lockAt !== undefined && t >= a.lockAt;
  const lk = locked ? E.outBack(win(t, a.lockAt, 0.6)) : 0, glow = a.glow ? 0.25 + 0.2 * Math.sin(t * 3 + i) : 0;
  let body: React.ReactNode = null, top = -300;
  if (mode === 'bottle') {
    const h = 240, liq = h * lv;
    body = <g>
      {glow > 0 && <ellipse cx={0} cy={-130} rx={120} ry={160} fill="#FFB74D" opacity={glow} />}
      <rect x={-24} y={-300} width={48} height={46} rx={6} fill="#37474F" stroke={OL} strokeWidth={4} />
      <path d="M -80 -250 Q -80 -270 -40 -270 L 40 -270 Q 80 -270 80 -250 L 80 -10 Q 80 0 70 0 L -70 0 Q -80 0 -80 -10 Z" fill="#5D4037" opacity={0.35} stroke={OL} strokeWidth={5} />
      <rect x={-74} y={-6 - liq} width={148} height={liq} rx={8} fill="#FF8F00" opacity={0.85} />
      <path d={`M -74 ${-6 - liq} q 37 ${-8 + 4 * Math.sin(t * 3)} 74 0 q 37 ${8 - 4 * Math.sin(t * 3)} 74 0`} fill="none" stroke="#FFE082" strokeWidth={4} opacity={lv > 0.02 ? 1 : 0} />
      <rect x={-64} y={-190} width={128} height={70} rx={8} fill={K.white} stroke={OL} strokeWidth={3} />
      <T x={0} y={-162} s={18}>{a.label || 'RESIST'}</T><T x={0} y={-136} s={14} c="#78909C">{a.sub || 'EUV'}</T>
    </g>;
  } else if (mode === 'tank') {
    const needle = -150 + 120 * lv;
    top = -440;
    body = <g>
      <rect x={-70} y={-380} width={140} height={380} rx={60} fill={col(a.color, '#B0BEC5')} stroke={OL} strokeWidth={5} />
      <rect x={-26} y={-430} width={52} height={56} rx={8} fill="#78909C" stroke={OL} strokeWidth={4} />
      <circle cx={0} cy={-470} r={40} fill={K.white} stroke={OL} strokeWidth={4} />
      <path d={`M 0 -470 L ${40 * Math.cos((needle * Math.PI) / 180) * 0.8} ${-470 + 40 * Math.sin((needle * Math.PI) / 180) * 0.8}`} stroke={lv < 0.25 ? K.red : OL} strokeWidth={5} strokeLinecap="round" />
      <rect x={-56} y={-250} width={112} height={60} rx={8} fill={K.white} stroke={OL} strokeWidth={3} />
      <T x={0} y={-212} s={24}>{a.label || 'NEON'}</T>
      {glow > 0 && <rect x={-70} y={-380} width={140} height={380} rx={60} fill="#FF80AB" opacity={glow} />}
    </g>;
  } else {
    const n = Math.max(0, Math.round((a.n ?? 6) * lv)), bars: React.ReactNode[] = [];
    for (let k = 0; k < n; k++) { const r = k < 3 ? 0 : k < 5 ? 1 : 2, c2 = k < 3 ? k : k < 5 ? k - 3 : 0, bx = -150 + c2 * 100 + r * 50, by = -50 - r * 50;
      bars.push(<g key={k}><path d={`M ${bx - 46} ${by} L ${bx + 46} ${by} L ${bx + 34} ${by - 44} L ${bx - 34} ${by - 44} Z`} fill="#CFD8DC" stroke={OL} strokeWidth={4} />
        <path d={`M ${bx - 26} ${by - 36} L ${bx + 10} ${by - 36}`} stroke={K.white} strokeWidth={4} opacity={0.8} /></g>); }
    top = -220;
    body = <g>{glow > 0 && <ellipse cx={0} cy={-80} rx={220} ry={110} fill="#E0F7FA" opacity={glow} />}{bars}
      {a.label && <g><rect x={-90} y={-6} width={180} height={40} rx={8} fill={K.white} stroke={OL} strokeWidth={3} /><T x={0} y={22} s={20}>{a.label}</T></g>}</g>;
  }
  return <g key={'vs' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {body}
    {locked && <g transform={`translate(0 ${top + 140 - 160 * (1 - lk)})`} opacity={lk}>
      <path d="M -110 30 L 110 -30 M -110 -30 L 110 30" stroke="#90A4AE" strokeWidth={12} strokeDasharray="18 8" />
      <rect x={-34} y={-10} width={68} height={56} rx={8} fill={K.gold} stroke={OL} strokeWidth={4} />
      <path d="M -20 -10 L -20 -32 Q 0 -56 20 -32 L 20 -10" fill="none" stroke={OL} strokeWidth={7} />
      <circle cx={0} cy={16} r={7} fill={OL} /></g>}
    {a.text && <T x={0} y={top - 30} s={28}>{a.text}</T>}
  </g>;
};

/** A giant phone playing a short show: `rot` keyframes (0 = portrait, 90 = landscape, the Turnstyle trick); the scene
 *  re-frames as it turns; a progress bar runs over `len` seconds and loops ("10 MIN"); `offAt` blacks the screen out. */
const bigphone: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const rot = kf(a.rot, t, 0), land = clamp(rot / 90), off = a.offAt !== undefined && t >= a.offAt;
  const W = 300, H = 560, prog = ((t - (a.at ?? 0)) / (a.len ?? 12)) % 1;
  const sw = lerp(W - 40, H - 60, land), sh = lerp(H - 90, W - 40, land);
  return <g key={'bp' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <g transform={`rotate(${rot})`}>
      <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={44} fill="#1B1F27" stroke={OL} strokeWidth={6} />
      <rect x={-30} y={-H / 2 + 14} width={60} height={10} rx={5} fill="#37474F" />
    </g>
    <g>
      <clipPath id={'bpc' + i}><rect x={-sw / 2} y={-sh / 2} width={sw} height={sh} rx={18} /></clipPath>
      <g clipPath={`url(#bpc${i})`}>
        <rect x={-sw / 2} y={-sh / 2} width={sw} height={sh} fill={off ? '#0B0D12' : col(a.color, '#4FB3F6')} />
        {!off && <g>
          <rect x={-sw / 2} y={sh * 0.15} width={sw} height={sh * 0.35} fill="#7BD389" />
          <circle cx={sw * 0.28} cy={-sh * 0.28} r={Math.min(sw, sh) * 0.09} fill="#FFE082" />
          {[-0.18, 0.12].map((dx, k) => { const px = sw * dx + Math.sin(t * 2 + k) * 10, ph = Math.min(sw, sh) * 0.32;
            return <g key={k} transform={`translate(${px} ${sh * 0.15})`}>
              <rect x={-ph * 0.18} y={-ph} width={ph * 0.36} height={ph * 0.7} rx={ph * 0.12} fill={k ? '#F06292' : '#FFB74D'} stroke={OL} strokeWidth={3} />
              <circle cx={0} cy={-ph * 1.08} r={ph * 0.18} fill="#F6C9A0" stroke={OL} strokeWidth={3} /></g>; })}
          <rect x={-sw / 2 + 16} y={sh / 2 - 22} width={sw - 32} height={8} rx={4} fill="#FFFFFF" opacity={0.4} />
          <rect x={-sw / 2 + 16} y={sh / 2 - 22} width={(sw - 32) * prog} height={8} rx={4} fill={K.red} />
          <T x={sw / 2 - 20} y={-sh / 2 + 34} s={20} c={K.white} a="end">{a.label || '10 MIN'}</T>
        </g>}
        {off && <T x={0} y={8} s={26} c="#90A4AE">{a.offText || 'NO SIGNAL'}</T>}
      </g>
    </g>
    {a.text && <T x={0} y={H / 2 + 50} s={28} c={a.textc || OL}>{a.text}</T>}
  </g>;
};

/** A school bus (for size comparisons). */
const bus: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  return <g key={'bs' + i} transform={`translate(${x} ${f}) scale(${s * (a.flip ? -1 : 1)} ${s})`}>
    <path d="M -300 -30 L -300 -230 Q -300 -250 -280 -250 L 230 -250 Q 260 -250 270 -220 L 300 -130 L 300 -30 Z" fill="#FFC107" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    {Array.from({length: 7}, (_, k) => <rect key={k} x={-280 + k * 70} y={-230} width={56} height={60} rx={6} fill="#CFEFFF" stroke={OL} strokeWidth={3} />)}
    <path d="M -300 -120 L 300 -120" stroke={OL} strokeWidth={4} />
    {[-200, 200].map((dx) => <circle key={dx} cx={dx} cy={-30} r={34} fill="#333" stroke={OL} strokeWidth={4} />)}
    {a.text && <T x={0} y={-140} s={28}>{a.text}</T>}
  </g>;
};

/** A border barrier (export control): the boom lowers on closeAt and lifts on openAt; a sign shows the destination. */
const barrier: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const closed = a.closeAt !== undefined && t >= a.closeAt && !(a.openAt !== undefined && t >= a.openAt);
  const ang = closed ? lerp(-70, 0, E.outBack(win(t, a.closeAt, 0.6))) : a.openAt !== undefined && t >= a.openAt ? lerp(0, -70, E.out(win(t, a.openAt, 0.6))) : -70;
  return <g key={'bar' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-40} y={-160} width={80} height={160} rx={10} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
    <circle cx={0} cy={-190} r={22} fill={closed ? K.red : K.green} stroke={OL} strokeWidth={4} />
    <g transform={`translate(30 -120) rotate(${ang})`}>
      <rect x={0} y={-14} width={520} height={28} rx={14} fill={K.white} stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3, 4].map((k) => <rect key={k} x={20 + k * 100} y={-14} width={50} height={28} fill={K.red} />)}</g>
    {a.text && <g><rect x={-130} y={-300} width={260} height={56} rx={10} fill={closed ? '#FFCDD2' : '#C8E6C9'} stroke={OL} strokeWidth={4} /><T x={0} y={-262} s={28}>{a.text}</T></g>}
  </g>;
};

/** Offshore oil platform on legs over the sea (floor = sea surface): deck, derrick, flare, helideck. drillAt: the drill
 * turns; dryAt shows "DRY"; strikeAt: a gusher of oil and a gold burst; flowAt: a pipe of oil barrels flows away. */
const rig: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.7);
  if (s <= 0) return null;
  const drill = a.drillAt !== undefined && t >= a.drillAt, strike = a.strikeAt !== undefined && t >= a.strikeAt, dry = a.dryAt !== undefined && t >= a.dryAt && !strike;
  const g = strike ? E.out(win(t, a.strikeAt, 0.8)) : 0, night = !!a.night;
  return <g key={'rg' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    {[-200, -70, 70, 200].map((dx) => <rect key={dx} x={dx - 16} y={-240} width={32} height={320} fill="#F9A825" stroke={OL} strokeWidth={4} />)}
    <path d="M -200 -150 L 200 -30 M 200 -150 L -200 -30" stroke="#F9A825" strokeWidth={10} />
    <rect x={-280} y={-300} width={560} height={70} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
    <rect x={-260} y={-380} width={200} height={80} rx={6} fill="#E53935" stroke={OL} strokeWidth={4} />
    {[0, 1, 2].map((k) => <rect key={k} x={-244 + k * 60} y={-366} width={40} height={22} rx={3} fill={night ? '#FFE08A' : '#CFEFFF'} stroke={OL} strokeWidth={2} />)}
    <ellipse cx={-160} cy={-392} rx={100} ry={16} fill="#90A4AE" stroke={OL} strokeWidth={4} />
    <T x={-160} y={-386} s={18} c={K.white}>H</T>
    <path d="M 60 -300 L 110 -560 L 160 -300 M 72 -360 L 148 -360 M 84 -430 L 136 -430 M 96 -500 L 124 -500 M 72 -360 L 136 -430 M 148 -360 L 84 -430" fill="none" stroke="#B0BEC5" strokeWidth={8} strokeLinejoin="round" />
    {drill && <g transform={`translate(110 -260) rotate(${t * 400})`}><path d="M -20 0 L 20 0 M 0 -20 L 0 20" stroke={OL} strokeWidth={6} /></g>}
    <path d="M 240 -300 L 330 -470" stroke="#90A4AE" strokeWidth={14} strokeLinecap="round" />
    {a.flare !== false && <path d={`M 330 -470 Q ${310 + 10 * Math.sin(t * 9)} -520 ${330 + 6 * Math.sin(t * 7)} ${-560 - 20 * Math.abs(Math.sin(t * 5))} Q ${352 + 8 * Math.sin(t * 11)} -510 330 -470 Z`} fill="#FF7043" stroke={OL} strokeWidth={3} />}
    {dry && <g transform={`translate(110 -640) scale(${E.outBack(win(t, a.dryAt, 0.4))})`}><rect x={-80} y={-36} width={160} height={66} rx={14} fill="#FFCDD2" stroke={OL} strokeWidth={4} /><T x={0} y={12} s={36} c={K.red}>DRY</T></g>}
    {strike && <g>
      <path d={`M 90 -560 Q ${60 + 20 * Math.sin(t * 8)} ${-560 - 260 * g} 110 ${-580 - 300 * g} Q ${160 + 20 * Math.sin(t * 7)} ${-560 - 260 * g} 130 -560 Z`} fill="#212121" stroke={OL} strokeWidth={3} />
      {Array.from({length: 10}, (_, k) => { const u = ((t - a.strikeAt) * 0.8 + k / 10) % 1; return <circle key={k} cx={110 + (k % 2 ? 1 : -1) * 120 * u} cy={-860 * g + 400 * u * u + (-580 + 280 * u) * (1 - g)} r={10} fill="#212121" opacity={1 - u} />; })}
      {t < a.strikeAt + 1.5 && Array.from({length: 12}, (_, k) => { const an = k * 0.52, r = 80 + 220 * win(t, a.strikeAt, 1.2);
        return <path key={'bb' + k} d={`M ${110 + Math.cos(an) * 60} ${-700 + Math.sin(an) * 60} L ${110 + Math.cos(an) * r} ${-700 + Math.sin(an) * r}`} stroke={K.gold} strokeWidth={8} strokeLinecap="round" opacity={1 - win(t, a.strikeAt, 1.5)} />; })}</g>}
    {a.text && <g><rect x={-170} y={-230} width={340} height={50} rx={10} fill={K.white} stroke={OL} strokeWidth={4} /><T x={0} y={-195} s={26}>{a.text}</T></g>}
  </g>;
};

/** A race car (or a motorbike with bike:true), side view, wheels spinning; x keyframes or `loop` (speed px/s across x0..x1). */
const racecar: ItemFn = (a, {t, f}, i) => {
  const s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.3), c = col(a.color, K.red);
  if (s <= 0) return null;
  let x = kf(a.x, t, 960);
  if (a.loop) { const x0 = a.x0 ?? -600, x1 = a.x1 ?? 2600, sp = a.loop; x = x0 + (((t - (a.at ?? 0)) * sp + (a.phase ?? 0)) % (x1 - x0)); }
  const y = kf(a.y, t, f + 70), spin = t * 1400, fl = a.flip ? -1 : 1;
  const wheel = (wx: number, r: number) => <g transform={`translate(${wx} 0) rotate(${spin})`}><circle r={r} fill="#212121" stroke={OL} strokeWidth={3} /><path d={`M ${-r * 0.6} 0 L ${r * 0.6} 0 M 0 ${-r * 0.6} L 0 ${r * 0.6}`} stroke="#9E9E9E" strokeWidth={3} /></g>;
  return <g key={'rc' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    {(a.loop || Array.isArray(a.x)) && [0, 1, 2].map((k) => <path key={k} d={`M ${-170 - k * 40} ${-30 + k * 14} L ${-240 - k * 60} ${-30 + k * 14}`} stroke={K.white} strokeWidth={4} opacity={0.7} />)}
    {a.bike ? <g>
      {wheel(-60, 30)}{wheel(70, 30)}
      <path d="M -60 0 L -10 -50 L 50 -50 L 70 0 M -10 -50 L -30 -70 M 50 -50 L 60 -80" fill="none" stroke={c} strokeWidth={12} strokeLinejoin="round" strokeLinecap="round" />
      <path d="M -10 -60 Q 20 -110 60 -80" fill="none" stroke={OL} strokeWidth={16} strokeLinecap="round" />
      <circle cx={40} cy={-112} r={22} fill={c} stroke={OL} strokeWidth={4} /><rect x={44} y={-122} width={20} height={12} rx={4} fill="#263238" /></g>
    : <g>
      <path d="M -170 -20 L -150 -60 L -40 -64 L -10 -100 L 40 -100 L 60 -60 L 180 -44 L 190 -20 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-190} y={-96} width={40} height={50} rx={4} fill={c} stroke={OL} strokeWidth={4} />
      <rect x={170} y={-40} width={40} height={20} rx={3} fill={c} stroke={OL} strokeWidth={4} />
      <circle cx={10} cy={-96} r={18} fill={a.helmet ? col(a.helmet) : K.gold} stroke={OL} strokeWidth={4} />
      <T x={-60} y={-30} s={30} c={K.white}>{a.text ?? String((i % 20) + 1)}</T>
      {wheel(-110, 32)}{wheel(130, 32)}</g>}
  </g>;
};

/** A big cartoon wristwatch: ticking second hand, strap, glinting crystal; text on a tag below. */
const watch: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 450), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0) return null;
  const sec = Math.floor(t) * 6, mn = t * 0.5, hr = t * 0.04;
  return <g key={'wt' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 1.2) * 3})`}>
    <rect x={-80} y={-330} width={160} height={180} rx={30} fill="#5D4037" stroke={OL} strokeWidth={5} />
    <rect x={-80} y={150} width={160} height={180} rx={30} fill="#5D4037" stroke={OL} strokeWidth={5} />
    {[-260, -200, 200, 260].map((dy) => <path key={dy} d={`M -60 ${dy} L 60 ${dy}`} stroke="#3E2723" strokeWidth={4} />)}
    <circle r={185} fill={col(a.color, '#B0BEC5')} stroke={OL} strokeWidth={7} />
    <circle r={160} fill={K.white} stroke={OL} strokeWidth={4} />
    <rect x={182} y={-22} width={30} height={44} rx={8} fill={col(a.color, '#B0BEC5')} stroke={OL} strokeWidth={4} />
    {Array.from({length: 12}, (_, k) => { const an = k * Math.PI / 6; return <path key={k} d={`M ${Math.sin(an) * 130} ${-Math.cos(an) * 130} L ${Math.sin(an) * 148} ${-Math.cos(an) * 148}`} stroke={OL} strokeWidth={k % 3 ? 4 : 8} />; })}
    <path d={`M 0 0 L ${Math.sin(hr) * 70} ${-Math.cos(hr) * 70}`} stroke={OL} strokeWidth={12} strokeLinecap="round" />
    <path d={`M 0 0 L ${Math.sin(mn) * 110} ${-Math.cos(mn) * 110}`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
    <path d={`M 0 20 L ${Math.sin(sec * Math.PI / 180) * 130} ${-Math.cos(sec * Math.PI / 180) * 130}`} stroke={K.red} strokeWidth={4} strokeLinecap="round" />
    <circle r={12} fill={OL} />
    <path d="M -110 -90 Q -60 -140 0 -130" fill="none" stroke={K.white} strokeWidth={10} opacity={0.6} strokeLinecap="round" />
    {a.text && <g><rect x={-170} y={210} width={340} height={56} rx={12} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={248} s={28}>{a.text}</T></g>}
  </g>;
};

/** A wall of office PCs. From infectAt, a wiper spreads from `origin` [col,row] at `speed` cells/s: each screen flashes and turns
 *  to a red ransom note. From healAt, machines are rebuilt one by one (blue with a tick) at `healSpeed` cells/s. */
const pcgrid: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const cols = a.cols ?? 8, rows = a.rows ?? 4, cw = a.cell ?? 120, ch = cw * 0.8, [oc, or] = a.origin || [0, 0];
  const ia = a.infectAt ?? 1e9, sp = a.speed ?? 4, ha = a.healAt ?? 1e9, hs = a.healSpeed ?? 3;
  const cells = [];
  let bad = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const d = Math.hypot(c - oc, r - or) + ((c * 7 + r * 13) % 5) * 0.15, ti = ia + d / sp, th = ha + (r * cols + c) / (hs * 1.0) * 0.5;
    const inf = t >= ti && t < th, healed = t >= th, flash = inf && t < ti + 0.25;
    if (inf) bad++;
    const px = (c - (cols - 1) / 2) * cw, py = (r - (rows - 1) / 2) * ch;
    cells.push(<g key={r + '-' + c} transform={`translate(${px} ${py})`}>
      <rect x={-cw * 0.4} y={-ch * 0.42} width={cw * 0.8} height={ch * 0.6} rx={6} fill="#37474F" stroke={OL} strokeWidth={3} />
      <rect x={-cw * 0.34} y={-ch * 0.37} width={cw * 0.68} height={ch * 0.5} rx={3} fill={flash ? '#FFFFFF' : inf ? '#B71C1C' : healed ? '#81D4FA' : '#A5D6A7'} />
      {inf && !flash && [0, 1, 2].map((k) => <rect key={k} x={-cw * 0.28} y={-ch * 0.3 + k * ch * 0.12} width={cw * (k === 2 ? 0.3 : 0.56)} height={ch * 0.05} fill="#FFCDD2" />)}
      {healed && <path d={`M ${-cw * 0.1} ${-ch * 0.12} l ${cw * 0.07} ${cw * 0.07} l ${cw * 0.14} ${-cw * 0.14}`} stroke={OL} strokeWidth={4} fill="none" strokeLinecap="round" />}
      {!inf && !healed && Math.sin(t * 4 + r + c) > 0 && <rect x={-cw * 0.28} y={-ch * 0.3} width={cw * 0.05} height={ch * 0.1} fill={OL} />}
      <rect x={-cw * 0.06} y={ch * 0.18} width={cw * 0.12} height={ch * 0.12} fill="#546E7A" />
      <rect x={-cw * 0.2} y={ch * 0.29} width={cw * 0.4} height={ch * 0.06} rx={3} fill="#546E7A" stroke={OL} strokeWidth={2} />
    </g>);
  }
  const tw = cols * cw;
  return <g key={'pg' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {cells}
    {a.text && <T x={0} y={-(rows / 2) * ch - 26} s={30} c={a.textc || OL}>{a.text}</T>}
    {a.count && <g transform={`translate(${tw / 2 + 30} ${-(rows / 2) * ch})`}><rect x={0} y={0} width={210} height={70} rx={12} fill={bad ? K.red : '#455A64'} stroke={OL} strokeWidth={4} />
      <T x={105} y={46} s={30} c={K.white}>{bad ? `${bad} DOWN` : 'ALL OK'}</T></g>}
  </g>;
};

/** A generic (redrawn) loan-payment form: three wash-account checkboxes FRONT / FUND / PRINCIPAL that tick at the
 *  times in `checks` ([front, fund, principal], null = never), an approval stamp row (`approvals`: times), a warning
 *  dialog at warnAt ("Funds will be sent out of the bank. Continue?") whose YES is clicked at yesAt, after which the
 *  `sent` line counts up. */
const wireform: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const W = 620, H = 470, ch: (number | null)[] = a.checks || [null, null, null], names = ['FRONT', 'FUND', 'PRINCIPAL'];
  const apv: number[] = a.approvals || [], warn = a.warnAt ?? 1e9, yes = a.yesAt ?? 1e9;
  const showWarn = t >= warn && t < yes + 0.6, sent = t >= yes;
  const amt = sent ? Math.min(1, (t - yes) / 2.5) : 0;
  return <g key={'wf' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={14} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
    <rect x={-W / 2} y={-H / 2} width={W} height={56} rx={14} fill="#37474F" />
    <T x={-W / 2 + 24} y={-H / 2 + 38} s={24} c={K.white} a="start">{a.title || 'LOAN PAYMENT · WASH ACCOUNT'}</T>
    {names.map((n, k) => { const on = ch[k] !== null && ch[k] !== undefined && t >= (ch[k] as number), yy = -H / 2 + 110 + k * 62;
      const pulse = on && t < (ch[k] as number) + 0.4 ? 1.25 : 1;
      return <g key={n} transform={`translate(${-W / 2 + 40} ${yy})`}>
        <g transform={`scale(${pulse})`}><rect x={-16} y={-16} width={32} height={32} rx={5} fill={K.white} stroke={OL} strokeWidth={4} />
          {on && <path d="M -10 0 L -2 9 L 12 -10" stroke={K.green2} strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round" />}</g>
        <T x={34} y={10} s={28} a="start">{n}</T>
        <rect x={250} y={-18} width={260} height={36} rx={6} fill={on ? '#C8E6C9' : '#FFFFFF'} stroke="#90A4AE" strokeWidth={3} />
        <T x={262} y={8} s={20} a="start" c="#546E7A">{on ? 'WASH ACCOUNT' : (t >= (a.at ?? 0) + 1 && k < 2 && ch[2] !== null ? '— (default)' : '')}</T>
      </g>; })}
    <g transform={`translate(${-W / 2 + 40} ${H / 2 - 120})`}>
      {['MAKER', 'CHECKER', 'APPROVER'].map((r, k) => { const ok = apv[k] !== undefined && t >= apv[k];
        return <g key={r} transform={`translate(${k * 190} 0)`}><rect x={0} y={-24} width={170} height={44} rx={22} fill={ok ? K.green2 : '#CFD8DC'} stroke={OL} strokeWidth={3} />
          <T x={85} y={6} s={20} c={ok ? K.white : '#546E7A'}>{(ok ? '✓ ' : '') + r}</T></g>; })}
    </g>
    <g transform={`translate(0 ${H / 2 - 40})`}>
      <T x={-W / 2 + 40} y={8} s={24} a="start">SENT OUT:</T>
      <T x={W / 2 - 40} y={8} s={32} a="end" c={amt > 0.05 ? K.red : OL}>{sent ? '$' + (7.8 + amt * (a.total ?? 894)).toFixed(1) + 'M' : '$0'}</T>
    </g>
    {showWarn && <g transform={`translate(0 -10) scale(${E.outBack(win(t, warn, 0.4))})`}>
      <rect x={-250} y={-110} width={500} height={220} rx={16} fill="#FFF8E1" stroke={OL} strokeWidth={6} />
      <path d="M -200 -60 l 26 -46 l 26 46 Z" fill={K.gold} stroke={OL} strokeWidth={4} strokeLinejoin="round" /><T x={-174} y={-68} s={30}>!</T>
      <T x={-130} y={-74} s={22} a="start">Funds will be sent out</T>
      <T x={-130} y={-46} s={22} a="start">of the bank. Continue?</T>
      <g transform="translate(-90 50)"><rect x={-70} y={-26} width={140} height={52} rx={10} fill={t >= yes ? K.green2 : K.white} stroke={OL} strokeWidth={4} /><T x={0} y={9} s={26}>YES</T></g>
      <g transform="translate(90 50)"><rect x={-70} y={-26} width={140} height={52} rx={10} fill={K.white} stroke={OL} strokeWidth={4} /><T x={0} y={9} s={26}>NO</T></g>
      {t >= yes - 0.8 && <path d={`M ${-60 + 40 * clamp(1 - (t - yes + 0.8) / 0.8)} ${70 + 40 * clamp(1 - (t - yes + 0.8) / 0.8)} l 0 40 l 10 -10 l 12 22 l 8 -4 l -12 -22 l 14 0 Z`} fill={K.white} stroke={OL} strokeWidth={3} />}
    </g>}
  </g>;
};

/** A small island carrying three bank towers. `grow` (0..1 keyframes) raises the towers far above the island;
 *  from wobbleAt they sway; at fallAt they crack and topple into the sea one after another (0.6 s apart). */
const bankisle: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 760), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const g = clamp(kf(a.grow, t, 0.1)), wob = a.wobbleAt !== undefined && t >= a.wobbleAt ? Math.sin(t * 6) * Math.min(1, (t - a.wobbleAt) / 2) * 4 : 0;
  const names: string[] = a.names || ['K', 'L', 'G'], cols = ['#6A1B9A', '#1565C0', '#C62828'];
  return <g key={'bi' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={40} rx={330} ry={34} fill="#4FB3F6" opacity={0.6} />
    <path d="M -220 30 Q -170 -40 -60 -50 Q 40 -70 120 -40 Q 210 -20 230 30 Z" fill="#7CB342" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    <path d="M -120 -40 l 40 -50 l 30 40 Z M 60 -48 l 30 -36 l 26 32 Z" fill="#ECEFF1" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    {names.map((n, k) => { const fa = a.fallAt !== undefined ? a.fallAt + k * 0.6 : 1e9, f = clamp((t - fa) / 1.4);
      const h = 60 + g * (a.maxH ?? 520) * (1 - 0.12 * k), bx = -110 + k * 110, ang = (k - 1 || 1) * 80 * E.in(f) + wob * (k + 1) * 0.6;
      return <g key={k} transform={`translate(${bx} ${-44 + 160 * E.in(f)}) rotate(${ang})`} opacity={1 - clamp((t - fa - 1.2) / 0.8)}>
        <rect x={-38} y={-h} width={76} height={h} rx={6} fill={cols[k % 3]} stroke={OL} strokeWidth={5} />
        {Array.from({length: Math.floor(h / 46)}, (_, r) => <g key={r}><rect x={-26} y={-h + 16 + r * 46} width={18} height={20} fill="#FFE082" opacity={0.85} /><rect x={8} y={-h + 16 + r * 46} width={18} height={20} fill="#FFE082" opacity={0.85} /></g>)}
        <path d={`M -44 ${-h} L 0 ${-h - 34} L 44 ${-h} Z`} fill="#ECEFF1" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <T x={0} y={-h - 44} s={30} c={K.white}>{n}</T>
        {f > 0 && <path d={`M -20 ${-h * 0.5} l 18 30 l -10 22 l 16 26`} stroke={OL} strokeWidth={4} fill="none" />}
      </g>; })}
    {a.text && <T x={0} y={100} s={28} c={a.textc || OL}>{a.text}</T>}
  </g>;
};

/** A big balance scale: `left` / `right` labels on the pans (`lsub` / `rsub` small lines); the beam starts tipped
 *  (`tilt` degrees, + = right side down) and settles to `to` (default 0 = level) at balanceAt; `lsize`/`rsize` scale the
 *  load drawn on each pan (a walled garden on the left, a big block of land on the right). */
const balance: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const ba = a.balanceAt ?? 1e9, u = E.outBack(win(t, ba, 1.6)), ang = lerp(a.tilt ?? 14, a.to ?? 0, u) + Math.sin(t * 2) * 0.6;
  const L = 300, rad = ang * Math.PI / 180, ly = -L * Math.sin(rad), ry = L * Math.sin(rad);
  const pan = (px: number, py: number, label: string, sub: string | undefined, sz: number, garden: boolean) =>
    <g transform={`translate(${px} ${py})`}>
      <path d="M 0 0 L -110 120 M 0 0 L 110 120" stroke={OL} strokeWidth={4} />
      <path d="M -130 120 Q 0 170 130 120 Z" fill="#B0BEC5" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <g transform={`translate(0 118) scale(${sz})`}>
        {garden ? <g><rect x={-70} y={-60} width={140} height={60} rx={6} fill="#7CB342" stroke={OL} strokeWidth={4} />
          <rect x={-78} y={-68} width={156} height={12} fill="#BCAAA4" stroke={OL} strokeWidth={3} />
          <circle cx={-30} cy={-34} r={14} fill="#33691E" /><circle cx={24} cy={-30} r={16} fill="#33691E" /></g>
          : <path d="M -90 0 L -100 -70 L -40 -96 L 30 -84 L 96 -50 L 90 0 Z" fill="#FFCC80" stroke={OL} strokeWidth={4} strokeLinejoin="round" />}
      </g>
      <T x={0} y={210} s={30} c={a.textc || OL}>{label}</T>
      {sub && <T x={0} y={244} s={20} c={a.textc || '#455A64'}>{sub}</T>}
    </g>;
  return <g key={'bl' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <path d="M -90 0 L 90 0 L 30 -40 L -30 -40 Z" fill="#8D6E63" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    <rect x={-14} y={-460} width={28} height={420} fill="#A1887F" stroke={OL} strokeWidth={5} />
    <g transform={`translate(0 -460)`}>
      <line x1={-L * Math.cos(rad)} y1={ly} x2={L * Math.cos(rad)} y2={ry} stroke={OL} strokeWidth={12} strokeLinecap="round" />
      <circle r={20} fill={K.gold} stroke={OL} strokeWidth={5} />
      {pan(-L * Math.cos(rad), ly, a.left || 'LEFT', a.lsub, a.lsize ?? 1, true)}
      {pan(L * Math.cos(rad), ry, a.right || 'RIGHT', a.rsub, a.rsize ?? 1, false)}
    </g>
  </g>;
};

/** A big brilliant-cut diamond with sparkles. `n` stones in a row (default 1, `gap` px apart); `dimAt` greys them out
 *  (the price story fading); `label` under it; `color` tints the stone (e.g. a lab stone). */
const gem: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const n = a.n ?? 1, gap = a.gap ?? 260, dim = a.dimAt !== undefined ? clamp((t - a.dimAt) / 1.5) : 0, c = col(a.color, '#B3E5FC');
  return <g key={'gm' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {Array.from({length: n}, (_, k) => { const dx = (k - (n - 1) / 2) * gap, bob = Math.sin(t * 1.8 + k) * 6;
      return <g key={k} transform={`translate(${dx} ${bob})`} opacity={1 - dim * 0.55}>
        <path d="M -110 -40 L -60 -100 L 60 -100 L 110 -40 L 0 110 Z" fill={c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <path d="M -110 -40 L 110 -40 M -60 -100 L -30 -40 L 0 -100 L 30 -40 L 60 -100 M -30 -40 L 0 110 L 30 -40" stroke={OL} strokeWidth={3} fill="none" strokeLinejoin="round" opacity={0.7} />
        <path d="M -60 -100 L -30 -40 L -110 -40 Z" fill="#FFFFFF" opacity={0.5} />
        {[0, 1, 2].map((q) => { const ph = (t * 1.3 + q * 0.7 + k) % 2.1, sc = ph < 0.5 ? Math.sin(ph / 0.5 * Math.PI) : 0;
          return sc > 0 ? <path key={q} transform={`translate(${[-70, 50, 10][q]} ${[-110, -70, 20][q]}) scale(${sc * (1 - dim)})`} d="M 0 -26 L 6 -6 L 26 0 L 6 6 L 0 26 L -6 6 L -26 0 L -6 -6 Z" fill="#FFFFFF" /> : null; })}
      </g>; })}
    {a.label && <T x={0} y={170} s={30} c={a.textc || OL}>{a.label}</T>}
  </g>;
};

/** A big cartoon hamburger (generic: sesame bun, patty, cheese, lettuce). `bites` keyframes 0..3 bites taken; `steam`. */
const burger: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const bites = Math.round(kf(a.bites, t, 0)), bob = Math.sin(t * 2.2 + i) * 6, sq = 1 + Math.sin(t * 2.2 + i) * 0.015;
  const clip = 'bclip' + i;
  return <g key={'bg' + i} transform={`translate(${x} ${y + bob}) scale(${s * sq} ${s / sq})`}>
    <defs><clipPath id={clip}><path d={`M -260 -260 L 260 -260 L 260 260 L -260 260 Z ${Array.from({length: bites}, (_, k) =>
      `M ${200 - k * 10} ${-150 + k * 70} a 60 60 0 1 0 0.1 0 Z`).join(' ')}`} clipRule="evenodd" /></clipPath></defs>
    <ellipse cx={0} cy={150} rx={210} ry={26} fill="#000" opacity={0.18} />
    <g clipPath={`url(#${clip})`}>
      <path d="M -190 60 Q -200 130 -150 135 L 150 135 Q 200 130 190 60 Z" fill="#E7A55A" stroke={OL} strokeWidth={6} />
      <path d="M -205 30 L 205 30 L 195 66 L -195 66 Z" fill="#6B3E26" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <path d="M -200 20 L 200 20 L 150 52 L 110 26 L 40 60 L -20 26 L -90 56 L -140 26 Z" fill="#FFC93C" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <path d={`M -215 6 ${Array.from({length: 10}, (_, k) => `Q ${-195 + k * 43} ${28 + (k % 2) * 8} ${-172 + k * 43} 6`).join(' ')} L 215 6 L 215 20 L -215 20 Z`} fill="#7BD389" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <path d="M -200 0 Q -200 -150 0 -150 Q 200 -150 200 0 Z" fill="#F0A84E" stroke={OL} strokeWidth={6} />
      {Array.from({length: 11}, (_, k) => <ellipse key={k} cx={-120 + rnd(k) * 240} cy={-110 + rnd(k + 4) * 80} rx={9} ry={5} transform={`rotate(${rnd(k + 7) * 60 - 30})`} fill="#FFF5E1" stroke={OL} strokeWidth={2} />)}
    </g>
    {a.steam !== false && [0, 1, 2].map((q) => { const ph = (t * 0.6 + q / 3) % 1;
      return <path key={'st' + q} d={`M ${-60 + q * 60} ${-170 - ph * 120} q 14 -20 0 -40 q -14 -20 0 -40`} fill="none" stroke="#FFFFFF" strokeWidth={8} strokeLinecap="round" opacity={0.7 * (1 - ph)} />; })}
    {a.label && <T x={0} y={200} s={34} c={a.textc || OL}>{a.label}</T>}
  </g>;
};

/** A generic fast-food restaurant front (no real brand): sign text `text` (swaps to `newText` at `swapAt`, with a flash),
 *  big windows with diners, doors that open at `openAt` (lights come on). Colours via `color` / `newColor`. */
const restaurant: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const swapped = a.swapAt !== undefined && t >= a.swapAt, flash = a.swapAt !== undefined ? Math.max(0, 1 - Math.abs(t - a.swapAt) / 0.35) : 0;
  const lit = a.openAt === undefined || t >= a.openAt, dOpen = a.openAt !== undefined ? clamp((t - a.openAt) / 0.8) : 1;
  const c = col(swapped ? a.newColor || '#2E7D32' : a.color, '#C62828'), txt = swapped ? a.newText || '' : a.text || 'BURGERS';
  const W = 900, H = 520;
  return <g key={'rs' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-W / 2} y={-H} width={W} height={H} fill="#EFE6D8" stroke={OL} strokeWidth={6} />
    <rect x={-W / 2 - 20} y={-H - 110} width={W + 40} height={120} rx={14} fill={c} stroke={OL} strokeWidth={6} />
    <T x={0} y={-H - 30} s={Math.min(72, 1500 / Math.max(6, txt.length))} c="#FFFFFF">{txt}</T>
    {flash > 0 && <rect x={-W / 2 - 20} y={-H - 110} width={W + 40} height={120} rx={14} fill="#FFFFFF" opacity={flash} />}
    {[-1, 1].map((sd) => <g key={sd}>
      <rect x={sd < 0 ? -W / 2 + 40 : 120} y={-H + 60} width={290} height={300} rx={8} fill={lit ? '#FFF3C4' : '#5E6B80'} stroke={OL} strokeWidth={5} />
      {lit && [0, 1, 2].map((q) => <g key={q} transform={`translate(${(sd < 0 ? -W / 2 + 90 : 170) + q * 90} ${-H + 300})`}>
        <circle cx={0} cy={-60} r={22} fill={K.skin[(q + (sd > 0 ? 2 : 0)) % 4]} stroke={OL} strokeWidth={3} />
        <rect x={-26} y={-38} width={52} height={50} rx={16} fill={['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB'][(q + sd + 2) % 4]} stroke={OL} strokeWidth={3} /></g>)}
    </g>)}
    <rect x={-80} y={-260} width={160} height={260} fill="#3B4A63" stroke={OL} strokeWidth={5} />
    <rect x={-76} y={-256} width={76 * (1 - dOpen) + 2} height={252} fill="#9FE3FF" opacity={0.8} />
    <rect x={76 - 76 * (1 - dOpen) - 2} y={-256} width={76 * (1 - dOpen) + 2} height={252} fill="#9FE3FF" opacity={0.8} />
    {a.sub && <T x={0} y={-H + 40} s={26} c={OL} w={700}>{a.sub}</T>}
  </g>;
};

/** A long winding queue of people in winter coats and fur hats (generic), shuffling slowly towards `x` (the door).
 *  `n` people, `gap` spacing, `rows` how many back-and-forth rows, `move` px/s shuffle. */
const queue: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), app = pop(t, a.at ?? 0, 0.6);
  if (app <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const n = a.n ?? 24, gap = a.gap ?? 70, s = a.scale ?? 0.55, rows = a.rows ?? 1, per = Math.ceil(n / rows), shift = ((t - (a.at ?? 0)) * (a.move ?? 8)) % gap;
  return <g key={'q' + i} opacity={app}>
    {Array.from({length: n}, (_, k) => { const r = Math.floor(k / per), c = k % per, dir = r % 2 === 0 ? 1 : -1;
      const px = x + (r % 2 === 0 ? c : per - 1 - c) * gap + 70 - shift * dir, py = f - r * 40, bob = Math.sin(t * 3 + k) * 2;
      const coat = ['#5D4037', '#37474F', '#6D4C41', '#455A64', '#4E342E', '#263238', '#795548'][k % 7], skin = K.skin[k % 4], scarf = ['#C62828', '#1565C0', '#F9A825', '#2E7D32'][k % 4];
      return <g key={k} transform={`translate(${px} ${py - bob}) scale(${s * (1 - r * 0.06)})`}>
        <path d="M -14 -80 L -14 0 M 14 -80 L 14 0" stroke="#212121" strokeWidth={16} strokeLinecap="round" />
        <path d="M -40 -160 Q -46 -60 -42 -60 L 42 -60 Q 46 -60 40 -160 Q 0 -176 -40 -160 Z" fill={coat} stroke={OL} strokeWidth={4} />
        <rect x={-30} y={-168} width={60} height={16} rx={8} fill={scarf} stroke={OL} strokeWidth={3} />
        <circle cx={0} cy={-196} r={30} fill={skin} stroke={OL} strokeWidth={4} />
        <circle cx={-10} cy={-196} r={3.5} fill={OL} /><circle cx={12} cy={-196} r={3.5} fill={OL} />
        <path d="M -38 -206 Q -40 -250 0 -248 Q 40 -250 38 -206 Q 0 -214 -38 -206 Z" fill={['#8D6E63', '#BCAAA4', '#5D4037', '#D7CCC8'][k % 4]} stroke={OL} strokeWidth={4} />
        <path d="M -40 -206 L -44 -176 M 40 -206 L 44 -176" stroke={['#8D6E63', '#BCAAA4', '#5D4037', '#D7CCC8'][k % 4]} strokeWidth={12} strokeLinecap="round" />
        <circle cx={14 * dir} cy={-90 + Math.sin(t * 5 + k) * 3} r={4} fill="#FFFFFF" opacity={(Math.sin(t * 2 + k) + 1) / 3} />
      </g>; })}
    {a.label && <T x={x + per * gap / 2} y={f + 70} s={34} c={a.textc || OL}>{a.label}</T>}
  </g>;
};

/** A big storage tank seen from the side with a cut-away showing the oil level: `fill` keyframes 0..1, `cap` text,
 *  label shows the % full; above `warn` (default 0.8) the gauge flashes red and a FULL? sign pops. */
const oiltank: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const fill = clamp(kf(a.fill, t, 0.5)), W = 360, H = 420, warn = a.warn ?? 0.8, hot = fill >= warn, fl = Math.sin(t * 9) > 0;
  const lvl = H * fill, wave = Math.sin(t * 2.4) * 6;
  return <g key={'ot' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-W / 2} y={-H} width={W} height={H} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
    <rect x={-W / 2 + 40} y={-H + 30} width={W - 80} height={H - 50} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
    <path d={`M ${-W / 2 + 40} ${-20 - lvl + 30 * fill} Q ${-60} ${-20 - lvl + 30 * fill - wave} 0 ${-20 - lvl + 30 * fill} T ${W / 2 - 40} ${-20 - lvl + 30 * fill} L ${W / 2 - 40} -20 L ${-W / 2 + 40} -20 Z`}
      fill="#1B1B1B" opacity={0.92} />
    <ellipse cx={0} cy={-H} rx={W / 2} ry={26} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    <path d={`M ${W / 2 - 10} ${-H + 10} L ${W / 2 + 40} ${-H + 60} L ${W / 2 + 40} 0`} fill="none" stroke="#90A4AE" strokeWidth={8} />
    <g transform={`translate(0 ${-H - 90})`}><rect x={-120} y={-44} width={240} height={80} rx={14} fill={hot && fl ? K.red : '#263238'} stroke={OL} strokeWidth={4} />
      <T x={0} y={14} s={44} c="#FFFFFF">{Math.round(fill * 100) + '%'}</T></g>
    {a.cap && <T x={0} y={60} s={30} c={a.textc || OL}>{a.cap}</T>}
    {hot && a.fullText !== '' && <g transform={`translate(${W / 2 + 120} ${-H - 40}) rotate(8) scale(${E.outBack(win(t, a.fullAt ?? 0, 0.4))})`}>
      <rect x={-110} y={-40} width={220} height={74} rx={10} fill="#FFF3E0" stroke={K.red} strokeWidth={6} /><T x={0} y={12} s={36} c={K.red}>{a.fullText || 'FULL?'}</T></g>}
  </g>;
};

/** A row of oil drums (barrels). `n` drums; `tag` text on a price tag above (e.g. "−$37.63"), `tagAt`; `pay` makes
 *  banknotes fly OUT of the seller's side towards +x from `payAt` (paying someone to take the oil). */
const barrel: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const n = a.n ?? 3, gap = 150;
  return <g key={'br' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    {Array.from({length: n}, (_, k) => { const dx = (k - (n - 1) / 2) * gap, bob = Math.sin(t * 2 + k) * 2;
      return <g key={k} transform={`translate(${dx} ${bob})`}>
        <rect x={-60} y={-190} width={120} height={190} rx={14} fill={col(a.color, '#263238')} stroke={OL} strokeWidth={5} />
        {[-140, -60].map((yy) => <rect key={yy} x={-64} y={yy} width={128} height={12} rx={6} fill="#455A64" stroke={OL} strokeWidth={3} />)}
        <ellipse cx={0} cy={-190} rx={60} ry={14} fill="#37474F" stroke={OL} strokeWidth={4} />
        <path d="M -10 -110 q 10 -26 20 0 a 10 10 0 1 1 -20 0 Z" fill="#FFC93C" stroke={OL} strokeWidth={2.5} />
      </g>; })}
    {a.tag && t >= (a.tagAt ?? 0) && <g transform={`translate(0 -300) rotate(${-4 + Math.sin(t * 2) * 3}) scale(${E.outBack(win(t, a.tagAt ?? 0, 0.4))})`}>
      <rect x={-170} y={-50} width={340} height={96} rx={16} fill={a.tagColor ? col(a.tagColor) : K.red} stroke={OL} strokeWidth={5} />
      <T x={0} y={18} s={52} c="#FFFFFF">{a.tag}</T>{a.tagSub && <T x={0} y={80} s={26} c={OL}>{a.tagSub}</T>}</g>}
    {a.payAt !== undefined && t >= a.payAt && Array.from({length: 6}, (_, k) => { const ph = ((t - a.payAt) * 0.7 + k / 6) % 1;
      return <g key={'pm' + k} transform={`translate(${-n * gap / 2 - 60 + ph * (n * gap + 360)} ${-260 - Math.sin(ph * Math.PI) * 160}) rotate(${ph * 360})`} opacity={1 - ph * 0.6}>
        <rect x={-44} y={-22} width={88} height={44} rx={5} fill="#3E6B48" stroke="#9FD3A8" strokeWidth={3} /><circle r={11} fill="none" stroke="#9FD3A8" strokeWidth={3} /></g>; })}
  </g>;
};

/** A full-screen bar chart (data "language"): `bars` [{label, value, color?, at?, display?}] grow at their own times with
 *  rolling value labels; `max` scale; area x,y (top-left), w,h; `title`; `prefix`/`suffix`/`decimals` for values;
 *  `highlight` index pulses; `min` (< 0) allows negative bars below a raised baseline. Horizontal baseline, no axes clutter. */
const bigchart: ItemFn = (a, {t}, i) => {
  const app = pop(t, a.at ?? 0, 0.5);
  if (app <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const X = (a.x as number) ?? 260, Y = (a.y as number) ?? 180, W = a.w ?? 1400, H = a.h ?? 620, bars = a.bars || [], n = Math.max(1, bars.length);
  const mx = a.max ?? Math.max(...bars.map((b: any) => b.value)), mn = Math.min(0, a.min ?? 0), base = Y + H - (H - 40) * (-mn) / (mx - mn), gap = W / n, bw = Math.min(220, gap * 0.62), dark = !!a.dark;
  return <g key={'bc' + i} opacity={app}>
    {a.title && <T x={X} y={Y - 30} s={40} c={dark ? '#FFFFFF' : OL} a="start">{a.title}</T>}
    <rect x={X - 20} y={base} width={W + 40} height={6} fill={dark ? '#FFFFFF' : OL} opacity={0.8} />
    {bars.map((b: any, k: number) => {
      const st = b.at ?? (a.at ?? 0) + 0.4 + k * 0.5, u = E.out(clamp((t - st) / 1.1)), v = b.value * u, h = (H - 40) * v / (mx - mn), neg = h < 0, ah = Math.abs(h);
      const cx = X + gap * (k + 0.5), c = col(b.color, ['#2F6FD1', '#E89A00', '#23995A', '#E53935', '#7E57C2'][k % 5]);
      const hl = a.highlight === k ? 1 + 0.03 * Math.sin(t * 6) : 1;
      const txt = b.display && u >= 1 ? b.display : (a.prefix || '') + v.toLocaleString('en-US', {minimumFractionDigits: a.decimals ?? 0, maximumFractionDigits: a.decimals ?? 0}) + (a.suffix || '');
      return t < st ? null : <g key={k} transform={`translate(${cx} ${base}) scale(${hl})`}>
        <rect x={-bw / 2} y={neg ? 0 : -h} width={bw} height={ah} rx={10} fill={c} stroke={OL} strokeWidth={5} />
        <rect x={-bw / 2 + 10} y={(neg ? 0 : -h) + 10} width={bw * 0.18} height={Math.max(0, ah - 20)} rx={6} fill="#FFFFFF" opacity={0.22} />
        <T x={0} y={neg ? ah + 52 : -h - 22} s={46} c={dark ? '#FFFFFF' : OL}>{txt}</T>
        <T x={0} y={neg ? -24 : 50} s={30} c={dark ? '#CFD8DC' : OL} w={800}>{b.label}</T>
        {b.sub && <T x={0} y={84} s={22} c={dark ? '#90A4AE' : '#4D6680'} w={600}>{b.sub}</T>}
      </g>;
    })}
  </g>;
};

/** Evidence cards pinned to a cork board with red string between them. `cards` [{x, y, text, sub?, at?, color?, rot?}],
 *  `links` [[i, j, at]] draw a sagging string from card i to card j; `stampAt`/`stamp` slam a stamp on the last card. */
const pinboard: ItemFn = (a, {t}, i) => {
  const cards = a.cards || [];
  const pos = (c: any) => [kf(c.x, t, 960), kf(c.y, t, 400)];
  return <g key={'pb' + i}>
    {(a.links || []).map(([p, q, at]: [number, number, number], k: number) => {
      if (t < at || !cards[p] || !cards[q]) return null;
      const u = E.out(clamp((t - at) / 0.8)), [x1, y1] = pos(cards[p]), [x2, y2] = pos(cards[q]);
      const ex = x1 + (x2 - x1) * u, ey = y1 + (y2 - y1) * u, mx = (x1 + ex) / 2, my = (y1 + ey) / 2 + 60 * u;
      return <path key={'l' + k} d={`M ${x1} ${y1 - 70} Q ${mx} ${my - 70} ${ex} ${ey - 70}`} fill="none" stroke="#D32F2F" strokeWidth={5} />;
    })}
    {cards.map((c: any, k: number) => {
      const sc = pop(t, c.at ?? 0, 0.45);
      if (sc <= 0) return null;
      const [x, y] = pos(c), w = c.w ?? 300, h = c.h ?? 190;
      return <g key={k} transform={`translate(${x} ${y}) rotate(${c.rot ?? ((k % 3) - 1) * 3}) scale(${sc})`}>
        <rect x={-w / 2 + 8} y={-h / 2 + 10} width={w} height={h} fill="#000" opacity={0.3} />
        <rect x={-w / 2} y={-h / 2} width={w} height={h} fill={c.color ? col(c.color) : '#FFF8E7'} stroke={OL} strokeWidth={3} />
        <T x={0} y={c.sub ? -4 : 14} s={c.size ?? 40} c={OL}>{c.text}</T>
        {c.sub && <T x={0} y={44} s={22} c="#5D4037" w={700}>{c.sub}</T>}
        <circle cx={0} cy={-h / 2 + 4} r={11} fill="#D32F2F" stroke={OL} strokeWidth={3} />
      </g>;
    })}
    {a.stamp && a.stampAt !== undefined && t >= a.stampAt && cards.length > 0 && (() => {
      const [x, y] = pos(cards[cards.length - 1]), u = E.outBack(win(t, a.stampAt, 0.35));
      return <g transform={`translate(${x + 120} ${y - 150}) rotate(-12) scale(${1.6 - 0.6 * u})`} opacity={u}>
        <rect x={-150} y={-40} width={300} height={80} rx={8} fill="none" stroke={K.red} strokeWidth={8} />
        <T x={0} y={16} s={44} c={K.red}>{a.stamp}</T></g>;
    })()}
  </g>;
};

/** An isometric data-center campus that builds itself: `n` halls appear one after another (`at` + k*`step`), each an iso
 *  box with blinking server lights and spinning roof fans; `label`; `glow` adds a power-line glow. */
const isodc: ItemFn = (a, {t, f}, i) => {
  const x0 = kf(a.x, t, 960), y0 = kf(a.y, t, f - 120), s = a.scale ?? 1, n = a.n ?? 6, step = a.step ?? 0.4, at = a.at ?? 0;
  if (t < at) return null;
  const cols = a.cols ?? 3, W = 220, D = 120, H = 110;
  const iso = (gx: number, gy: number): [number, number] => [(gx - gy) * W * 0.62, (gx + gy) * D * 0.62];
  const halls = Array.from({length: n}, (_, k) => ({gx: k % cols, gy: Math.floor(k / cols), k})).sort((p, q) => (p.gx + p.gy) - (q.gx + q.gy));
  return <g key={'iso' + i} transform={`translate(${x0} ${y0}) scale(${s})`}>
    {halls.map(({gx, gy, k}) => {
      const st = at + k * step, u = E.outBack(clamp((t - st) / 0.6));
      if (u <= 0) return null;
      const [cx, cy] = iso(gx, gy), h = H * u;
      const top = `M ${cx} ${cy - h} L ${cx + W / 2} ${cy - h + D / 2} L ${cx} ${cy - h + D} L ${cx - W / 2} ${cy - h + D / 2} Z`;
      return <g key={k}>
        <path d={`M ${cx - W / 2} ${cy + D / 2 - h} L ${cx} ${cy + D - h} L ${cx} ${cy + D} L ${cx - W / 2} ${cy + D / 2} Z`} fill="#9FB3C8" stroke={OL} strokeWidth={3} />
        <path d={`M ${cx} ${cy + D - h} L ${cx + W / 2} ${cy + D / 2 - h} L ${cx + W / 2} ${cy + D / 2} L ${cx} ${cy + D} Z`} fill="#7D93AB" stroke={OL} strokeWidth={3} />
        <path d={top} fill="#E3EBF3" stroke={OL} strokeWidth={3} />
        {u > 0.9 && [0, 1, 2].map((q) => <g key={q} transform={`translate(${cx - 40 + q * 40} ${cy - h + D / 2})`}>
          <ellipse rx={15} ry={8} fill="#546E7A" stroke={OL} strokeWidth={2} />
          <path d={`M ${-11 * Math.cos(t * 9 + q)} ${-6 * Math.sin(t * 9 + q)} L ${11 * Math.cos(t * 9 + q)} ${6 * Math.sin(t * 9 + q)}`} stroke="#CFD8DC" strokeWidth={3} /></g>)}
        {u > 0.9 && Array.from({length: 5}, (_, q) => <circle key={'l' + q} cx={cx - W / 2 + 24 + q * 20} cy={cy + D / 2 - h * 0.5 + q * 10} r={3.5}
          fill={Math.sin(t * 7 + q * 1.7 + k) > 0 ? '#7DF29A' : '#2E7D32'} />)}
      </g>;
    })}
    {a.glow && <path d={`M ${-W * 2} ${D * 2.2} L ${W * 2} ${-D * 0.4}`} stroke="#FFC93C" strokeWidth={6} strokeDasharray="18 14" strokeDashoffset={-t * 60} opacity={0.8} />}
    {a.label && <T x={0} y={D * 2.6} s={34} c={a.textc || OL}>{a.label}</T>}
  </g>;
};

/** An itemized medical bill that unrolls line by line: `lines` [{text, amount, at}] (amount is a display string),
 *  `total` {text, amount, at} stamped at the bottom in red; `title`. Paper curls at the bottom while unrolling. */
const medbill: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const lines = a.lines || [], W = 560, LH = 64, shown = lines.filter((l: any) => t >= (l.at ?? 0)).length;
  const tot = a.total && t >= (a.total.at ?? 1e9), H = 150 + shown * LH + (tot ? 120 : 0);
  return <g key={'mb' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.rot ?? -2})`}>
    <rect x={-W / 2 + 10} y={12} width={W} height={H} fill="#000" opacity={0.25} />
    <rect x={-W / 2} y={0} width={W} height={H} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
    <rect x={-W / 2} y={0} width={W} height={90} fill="#E0F2F1" stroke={OL} strokeWidth={4} />
    <T x={-W / 2 + 30} y={58} s={34} a="start">{a.title || 'STATEMENT'}</T>
    {lines.slice(0, shown).map((l: any, k: number) => { const u = E.out(clamp((t - (l.at ?? 0)) / 0.4));
      return <g key={k} opacity={u} transform={`translate(${(1 - u) * -30} ${130 + k * LH})`}>
        <T x={-W / 2 + 30} y={0} s={28} a="start" w={700}>{l.text}</T>
        <T x={W / 2 - 30} y={0} s={30} a="end">{l.amount}</T>
        <rect x={-W / 2 + 30} y={18} width={W - 60} height={2} fill={OL} opacity={0.15} /></g>; })}
    {tot && <g transform={`translate(0 ${150 + shown * LH + 40})`}>
      <rect x={-W / 2 + 20} y={-50} width={W - 40} height={90} rx={8} fill="#FFEBEE" stroke={K.red} strokeWidth={5} />
      <T x={-W / 2 + 40} y={10} s={34} a="start" c={K.red}>{a.total.text || 'TOTAL'}</T>
      <T x={W / 2 - 40} y={12} s={44} a="end" c={K.red}>{a.total.amount}</T></g>}
    <path d={`M ${-W / 2} ${H} q ${W / 4} 26 ${W / 2} 0 t ${W / 2} 0`} fill="#F5F5F5" stroke={OL} strokeWidth={4} />
  </g>;
};

/** A prescription pill bottle with a label and a swinging price tag (`price`, keyframes via `prices` [[t, text]]). */
const pills: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  let price = a.price || '';
  for (const [pt, pv] of (a.prices || []) as [number, string][]) if (t >= pt) price = pv;
  const c = col(a.color, '#FF8F00'), sw = Math.sin(t * 2.2 + i) * 6;
  return <g key={'pl' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-90} y={-300} width={180} height={300} rx={22} fill={c} opacity={0.85} stroke={OL} strokeWidth={5} />
    <rect x={-104} y={-350} width={208} height={64} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
    <rect x={-80} y={-230} width={160} height={150} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
    <T x={0} y={-180} s={26}>{a.label || 'Rx'}</T>
    {[0, 1, 2].map((q) => <rect key={q} x={-60} y={-150 + q * 22} width={120 - q * 20} height={8} rx={4} fill={OL} opacity={0.25} />)}
    {price && <g transform={`translate(110 -330) rotate(${10 + sw})`}>
      <path d="M 0 0 L 40 -20 L 230 -20 L 230 60 L 40 60 L 0 40 Z" fill={K.gold} stroke={OL} strokeWidth={4} />
      <circle cx={30} cy={20} r={7} fill="#FFFFFF" stroke={OL} strokeWidth={2} />
      <T x={140} y={34} s={40}>{price}</T></g>}
    {a.sub && <T x={0} y={60} s={28} c={a.textc || OL}>{a.sub}</T>}
  </g>;
};

/** A generic credit card (no brand): chip, embossed dots, a coloured gradient; `tapAt` swings it towards a reader with
 *  contactless waves; `text` label on the card; `flip` shows the back with a magnetic stripe. */
const creditcard: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 420), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const tap = a.tapAt !== undefined ? Math.sin(Math.PI * clamp((t - a.tapAt) / 0.9)) : 0;
  const c1 = col(a.color, '#3949AB'), id = 'ccg' + i;
  return <g key={'cc' + i} transform={`translate(${x + tap * 60} ${y - tap * 30}) scale(${s}) rotate(${(a.rot ?? -8) + tap * 10})`}>
    <defs><linearGradient id={id} x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={c1} /><stop offset="1" stopColor="#0D1B4C" /></linearGradient></defs>
    <rect x={-230} y={-145} width={460} height={290} rx={26} fill="#000" opacity={0.3} transform="translate(12 16)" />
    <rect x={-230} y={-145} width={460} height={290} rx={26} fill={`url(#${id})`} stroke={OL} strokeWidth={6} />
    {a.flip ? <rect x={-230} y={-95} width={460} height={60} fill="#1A1A1A" /> : <g>
      <rect x={-180} y={-60} width={80} height={60} rx={10} fill="#E0C068" stroke={OL} strokeWidth={3} />
      <path d="M -180 -30 L -100 -30 M -140 -60 L -140 0" stroke="#A88A3C" strokeWidth={3} />
      {[0, 1, 2, 3].map((g) => <T key={g} x={-170 + g * 100} y={70} s={30} c="#FFFFFF" o={0.85} a="start">{'••••'}</T>)}
      <path d="M 150 -70 q 14 14 0 28 M 168 -82 q 26 26 0 52 M 186 -94 q 38 38 0 76" fill="none" stroke="#FFFFFF" strokeWidth={5} strokeLinecap="round" opacity={0.8} />
      {a.text && <T x={-180} y={122} s={26} c="#FFFFFF" a="start" w={700}>{a.text}</T>}</g>}
    {tap > 0.2 && [0, 1, 2].map((q) => <path key={q} d={`M ${250 + q * 26} -60 q ${30 + q * 8} 60 0 120`} fill="none" stroke={K.gold} strokeWidth={6} strokeLinecap="round" opacity={tap * (1 - q * 0.25)} />)}
  </g>;
};

/** A highway toll booth with a barrier arm that lifts for each passing coin; `fee` text on the booth sign; `rate` coins/s
 *  flow left to right through it and a small cut drops into the booth's bin (`binLabel`). */
const tollbooth: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const rate = a.rate ?? 1.4, ph = ((t - (a.at ?? 0)) * rate) % 1, lift = Math.sin(Math.PI * clamp((ph - 0.35) / 0.3));
  return <g key={'tb' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-700} y={-10} width={1400} height={20} fill="#5B6577" />
    <rect x={-110} y={-330} width={220} height={330} rx={10} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
    <rect x={-80} y={-290} width={160} height={110} rx={8} fill="#B3E5FC" stroke={OL} strokeWidth={4} />
    <rect x={-150} y={-400} width={300} height={70} rx={12} fill={K.gold} stroke={OL} strokeWidth={5} />
    <T x={0} y={-353} s={34}>{a.fee || 'TOLL 1–3%'}</T>
    <g transform={`translate(110 -150) rotate(${-80 * lift})`}><rect x={0} y={-10} width={360} height={20} rx={10} fill="#E53935" stroke={OL} strokeWidth={4} />
      {[0, 1, 2].map((q) => <rect key={q} x={60 + q * 100} y={-10} width={40} height={20} fill="#FFFFFF" />)}</g>
    {[0, 1, 2].map((q) => { const u = (ph + q / 3) % 1, cx = -650 + u * 1300;
      return <g key={q} transform={`translate(${cx} -60)`}><circle r={34} fill={K.gold} stroke={OL} strokeWidth={4} /><T x={0} y={12} s={34}>$</T></g>; })}
    <rect x={-60} y={-60} width={120} height={60} fill="#455A64" stroke={OL} strokeWidth={4} />
    <circle cx={0} cy={-80 - 120 * clamp(1 - Math.abs(ph - 0.5) * 4)} r={12} fill={K.gold} stroke={OL} strokeWidth={2} opacity={ph > 0.3 && ph < 0.7 ? 1 : 0} />
    {a.binLabel && <T x={0} y={60} s={30} c={a.textc || OL}>{a.binLabel}</T>}
  </g>;
};

/** A trading screen for one contract. `price` is a keyframed value (e.g. [[0, 29000], [cue, 48075], ...]); the line is
 *  drawn from `at` up to now by sampling it; `max` sets the y scale. `bandsOffAt` turns the "PRICE BANDS" lamp red (OFF),
 *  `haltAt` stamps SUSPENDED, `suffix` (e.g. '%') replaces the $ prefix, `cancelAt` greys the part of the line after `cancelFrom` (seconds) and stamps CANCELLED. */
const tradescreen: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 460), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const W = 760, H = 460, at = a.at ?? 0, mx = a.max ?? 110000, mn = a.min ?? 0, span = Math.max(0.5, t - at), N = 60;
  const pts: string[] = [], grey: string[] = [];
  const cf = a.cancelFrom ?? 1e9, cancelled = a.cancelAt !== undefined && t >= a.cancelAt;
  for (let k = 0; k <= N; k++) { const tt = at + span * k / N, v = kf(a.price, tt, 0), px = -W / 2 + 60 + (W - 120) * k / N, py = H / 2 - 70 - (H - 160) * clamp((v - mn) / (mx - mn));
    (cancelled && tt >= cf ? grey : pts).push(`${px.toFixed(1)},${py.toFixed(1)}`); if (cancelled && tt >= cf && grey.length === 1 && pts.length) grey.unshift(pts[pts.length - 1]); }
  const now = kf(a.price, t, 0), off = a.bandsOffAt !== undefined && t >= a.bandsOffAt, halt = a.haltAt !== undefined && t >= a.haltAt;
  return <g key={'ts' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={18} fill="#0E1621" stroke={OL} strokeWidth={6} />
    {[0, 1, 2, 3].map((g) => <line key={g} x1={-W / 2 + 60} x2={W / 2 - 60} y1={H / 2 - 70 - (H - 160) * g / 3} y2={H / 2 - 70 - (H - 160) * g / 3} stroke="#24384F" strokeWidth={2} />)}
    <T x={-W / 2 + 30} y={-H / 2 + 44} s={26} c="#B0BEC5" a="start">{a.text || '3M NICKEL · $ / TONNE'}</T>
    {mn < 0 && <g><line x1={-W / 2 + 60} x2={W / 2 - 60} y1={H / 2 - 70 - (H - 160) * clamp(-mn / (mx - mn))} y2={H / 2 - 70 - (H - 160) * clamp(-mn / (mx - mn))} stroke="#B0BEC5" strokeWidth={3} strokeDasharray="6 6" />
      <T x={-W / 2 + 54} y={H / 2 - 62 - (H - 160) * clamp(-mn / (mx - mn))} s={20} c="#B0BEC5" a="end">{a.suffix !== undefined ? '0' + a.suffix : '$0'}</T></g>}
    <T x={W / 2 - 30} y={-H / 2 + 46} s={34} c={now > (a.hot ?? 60000) || now < 0 ? K.red : '#7DF29A'} a="end">{(a.suffix !== undefined ? (now < 0 ? '−' : '') : (now < 0 ? '−$' : '$')) + Math.abs(now).toLocaleString('en-US', {minimumFractionDigits: a.decimals ?? 0, maximumFractionDigits: a.decimals ?? 0}) + (a.suffix ?? '')}</T>
    <polyline points={pts.join(' ')} fill="none" stroke={now > (a.hot ?? 60000) || now < 0 ? K.red : '#7DF29A'} strokeWidth={6} strokeLinejoin="round" />
    {grey.length > 1 && <polyline points={grey.join(' ')} fill="none" stroke="#546E7A" strokeWidth={5} strokeDasharray="10 8" />}
    {a.lamp !== false && <g transform={`translate(${-W / 2 + 40} ${H / 2 - 30})`}><circle r={12} fill={off ? K.red : '#7DF29A'} stroke={OL} strokeWidth={3} />
      <T x={24} y={9} s={22} c="#B0BEC5" a="start">{off ? 'PRICE BANDS: OFF' : 'PRICE BANDS: ON'}</T></g>}
    {halt && <g transform={`rotate(-8) scale(${E.outBack(win(t, a.haltAt, 0.4))})`}><rect x={-210} y={-44} width={420} height={88} rx={10} fill="none" stroke={K.red} strokeWidth={8} />
      <T x={0} y={18} s={52} c={K.red}>{a.haltText || (cancelled ? 'CANCELLED' : 'SUSPENDED')}</T></g>}
  </g>;
};

/** A single American house (item `home`). `color` walls, `roof` colour, `sign` for-sale sign text (with `pages` [[at, text], ...] to
 *  swap the price on it), `soldAt` stamps SOLD, `lockAt` hangs a padlock on the door, `frameAt` → `doneAt`: built from a
 *  bare timber frame to a finished home, `night` lights the windows. */
const home: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const wall = col(a.color, '#FFF3E0'), roof = col(a.roof, '#C0504D');
  const built = a.frameAt !== undefined ? clamp((t - a.frameAt) / Math.max(0.3, (a.doneAt ?? a.frameAt + 3) - a.frameAt)) : 1;
  let sign = a.sign as string | undefined;
  for (const [at, txt] of (a.pages || []) as [number, string][]) if (t >= at) sign = txt;
  const lock = a.lockAt !== undefined ? E.outBack(win(t, a.lockAt, 0.5)) : 0, sold = a.soldAt !== undefined ? E.outBack(win(t, a.soldAt, 0.4)) : 0;
  return <g key={'hs' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={6} rx={300} ry={22} fill="#000" opacity={0.18} />
    {built < 1 && <g>
      {[-200, -120, -40, 40, 120, 200].map((dx) => <rect key={dx} x={dx - 6} y={-300} width={12} height={300} fill="#D7A86E" stroke={OL} strokeWidth={2} />)}
      <rect x={-210} y={-306} width={420} height={14} fill="#D7A86E" stroke={OL} strokeWidth={2} />
      <path d="M -230 -300 L 0 -470 L 230 -300" fill="none" stroke="#D7A86E" strokeWidth={14} strokeLinejoin="round" />
      <path d="M -230 -300 L 0 -470 L 230 -300" fill="none" stroke={OL} strokeWidth={2} /></g>}
    <g opacity={built} transform={`translate(0 ${(1 - built) * 40})`}>
      <rect x={-210} y={-300} width={420} height={300} fill={wall} stroke={OL} strokeWidth={6} />
      <path d="M -250 -300 L 0 -480 L 250 -300 Z" fill={roof} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <rect x={110} y={-470} width={50} height={110} fill="#8D6E63" stroke={OL} strokeWidth={5} />
      <circle cx={0} cy={-370} r={34} fill={a.night ? '#FFE082' : K.glass} stroke={OL} strokeWidth={5} />
      {[-150, 70].map((dx) => <g key={dx}><rect x={dx} y={-240} width={80} height={80} rx={4} fill={a.night ? '#FFE082' : K.glass} stroke={OL} strokeWidth={5} />
        <path d={`M ${dx + 40} -240 L ${dx + 40} -160 M ${dx} -200 L ${dx + 80} -200`} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={-40} y={-150} width={80} height={150} rx={6} fill={K.wood} stroke={OL} strokeWidth={5} />
      <circle cx={24} cy={-70} r={6} fill={K.gold} stroke={OL} strokeWidth={2} />
      {lock > 0 && <g transform={`translate(0 -86) scale(${lock})`}><path d="M -26 -20 L -26 -44 Q 0 -78 26 -44 L 26 -20" fill="none" stroke="#546E7A" strokeWidth={10} />
        <rect x={-38} y={-24} width={76} height={62} rx={10} fill={K.gold} stroke={OL} strokeWidth={5} /><circle cx={0} cy={4} r={8} fill={OL} /></g>}
    </g>
    {sign && <g transform={`translate(${a.signX ?? -330} 0)`}>
      <rect x={-6} y={-200} width={12} height={200} fill={K.wood2} stroke={OL} strokeWidth={3} />
      <rect x={-130} y={-230} width={260} height={110} rx={10} fill={K.white} stroke={OL} strokeWidth={5} />
      <rect x={-130} y={-230} width={260} height={34} rx={10} fill={K.red} stroke={OL} strokeWidth={5} />
      <T x={0} y={-204} s={22} c={K.white}>{a.signHead || 'FOR SALE'}</T>
      <T x={0} y={-140} s={sign.length > 9 ? 34 : 44} w={240}>{sign}</T>
      {sold > 0 && <g transform={`rotate(-12 0 -170) scale(${sold})`}><rect x={-110} y={-200} width={220} height={64} rx={8} fill={K.red} stroke={OL} strokeWidth={4} />
        <T x={0} y={-154} s={40} c={K.white}>SOLD</T></g>}</g>}
    {a.text && <T x={0} y={60} s={a.textSize ?? 34} c={a.textc || OL}>{a.text}</T>}
  </g>;
};

/** A zoning map seen from above: `cols` × `rows` lots; the first `share` (0-1) of lots light up yellow, one by one, as
 *  "single-family only" (`label`); the rest are blue ("other homes"). `upzoneAt` turns the yellow lots into small
 *  apartment blocks. `title` above the map. */
const zonemap: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 460), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const cols = a.cols ?? 10, rows = a.rows ?? 6, cw = a.cell ?? 70, n = cols * rows, k1 = Math.round((a.share ?? 0.78) * n);
  const W = cols * cw, H = rows * cw, fillAt = a.fillAt ?? (a.at ?? 0) + 0.4, fd = a.fillDur ?? 2.5, up = a.upzoneAt !== undefined ? win(t, a.upzoneAt, 1.2) : 0;
  const order = Array.from({length: n}, (_, q) => q).sort((p, q) => rnd(p + 17) - rnd(q + 17));
  const rank: number[] = []; order.forEach((q, r) => { rank[q] = r; });
  return <g key={'zm' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 - 24} y={-H / 2 - 24} width={W + 48} height={H + 48} rx={16} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
    {a.title && <T x={0} y={-H / 2 - 50} s={36} c={a.titlec || OL}>{a.title}</T>}
    {Array.from({length: n}, (_, q) => { const r = rank[q], cx = -W / 2 + (q % cols) * cw, cy = -H / 2 + Math.floor(q / cols) * cw;
      const on = t >= fillAt + fd * r / n, sf = r < k1;
      const fill = !on ? '#CFD8DC' : sf ? '#FFD54A' : '#64B5F6';
      const u = sf && up > 0 ? clamp(up * 1.6 - (r / k1) * 0.6) : 0;
      return <g key={q}><rect x={cx + 4} y={cy + 4} width={cw - 8} height={cw - 8} rx={6} fill={u > 0.5 ? '#81C784' : fill} stroke={OL} strokeWidth={2} />
        {on && !(u > 0.5) && <path d={`M ${cx + cw / 2 - 12} ${cy + cw / 2 + 10} L ${cx + cw / 2 - 12} ${cy + cw / 2 - 4} L ${cx + cw / 2} ${cy + cw / 2 - 16} L ${cx + cw / 2 + 12} ${cy + cw / 2 - 4} L ${cx + cw / 2 + 12} ${cy + cw / 2 + 10} Z`} fill={K.white} stroke={OL} strokeWidth={2} />}
        {u > 0.5 && [0, 1].map((b) => <rect key={b} x={cx + 12 + b * (cw / 2 - 8)} y={cy + 12} width={cw / 2 - 16} height={cw - 24} rx={3} fill={K.white} stroke={OL} strokeWidth={2} />)}</g>; })}
    {a.label && <g transform={`translate(${-W / 2} ${H / 2 + 60})`}><rect x={-16} y={-40} width={W + 32} height={66} rx={12} fill={K.white} stroke={OL} strokeWidth={4} />
      <rect x={0} y={-22} width={30} height={30} rx={5} fill="#FFD54A" stroke={OL} strokeWidth={3} />
      <T x={44} y={2} s={22} a="start" c={a.labelc || OL}>{a.label}</T>
      {a.label2 && <g transform={`translate(${W * 0.62} 0)`}><rect x={0} y={-22} width={30} height={30} rx={5} fill="#64B5F6" stroke={OL} strokeWidth={3} />
        <T x={44} y={2} s={22} a="start" c={a.labelc || OL}>{a.label2}</T></g>}</g>}
  </g>;
};

/** A big shopping cart piled with bulk packs; `x` keyframable (it rolls, wheels spin), `load` 0-3 how full, `text` on the
 *  biggest box, `price` tag on the handle. */
const cart: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const load = a.load ?? 3, spin = x * 0.02, cols = ['#C8A27A', '#90CAF9', '#EF9A9A', '#A5D6A7', '#FFE082', '#CE93D8'];
  const packs = [[-150, -250, 120, 90], [-20, -250, 140, 100], [130, -250, 100, 80], [-120, -350, 130, 100], [20, -360, 120, 110], [-60, -450, 150, 90]].slice(0, load * 2);
  return <g key={'ct' + i} transform={`translate(${x} ${kf(a.y, t, f)}) scale(${s})`}>
    {packs.map(([px, py, pw, ph], k) => <g key={k}><rect x={px} y={py + 100 - ph} width={pw} height={ph} rx={6} fill={cols[k % cols.length]} stroke={OL} strokeWidth={4} />
      <path d={`M ${px} ${py + 100 - ph / 2} L ${px + pw} ${py + 100 - ph / 2}`} stroke="#FFFFFF" strokeWidth={5} opacity={0.5} /></g>)}
    {a.text && <T x={-60 + 75} y={-372 + 70} s={22}>{a.text}</T>}
    <path d="M -200 -160 L 220 -160 L 190 -40 L -170 -40 Z" fill="#B0BEC5" fillOpacity={0.35} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    {[-120, -40, 40, 120].map((dx) => <path key={dx} d={`M ${dx} -160 L ${dx + 4} -40`} stroke={OL} strokeWidth={3} />)}
    <path d="M -186 -110 L 206 -110" stroke={OL} strokeWidth={3} />
    <path d="M 220 -160 L 270 -240 L 320 -240" fill="none" stroke={OL} strokeWidth={8} strokeLinecap="round" />
    <rect x={296} y={-252} width={50} height={22} rx={8} fill={K.red} stroke={OL} strokeWidth={3} />
    <path d="M -150 -40 L -140 -20 L 170 -20 L 180 -40" fill="none" stroke={OL} strokeWidth={6} />
    {[-130, 150].map((dx) => <g key={dx} transform={`translate(${dx} -10) rotate(${spin * 57})`}><circle r={20} fill="#37474F" stroke={OL} strokeWidth={4} /><path d="M -12 0 L 12 0" stroke="#90A4AE" strokeWidth={4} /></g>)}
    {a.price && <g transform="translate(330 -200)"><rect x={-60} y={0} width={120} height={50} rx={8} fill={K.white} stroke={OL} strokeWidth={4} /><T x={0} y={35} s={28}>{a.price}</T></g>}
  </g>;
};

/** A wooden pallet stacked with shrink-wrapped cases; `rows` high, `text` printed on the wrap; `arriveAt` slides it in
 *  from the left on a forklift tine path; `goneAt` empties it (cases vanish one by one, as if sold). */
const pallet: ItemFn = (a, {t, f}, i) => {
  const s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const arr = a.arriveAt !== undefined ? E.out(win(t, a.arriveAt, 1.2)) : 1, x = kf(a.x, t, 960) - (1 - arr) * 900;
  const rows = a.rows ?? 3, n = rows * 3, gone = a.goneAt !== undefined ? clamp((t - a.goneAt) / (a.goneDur ?? 3)) : 0, c = col(a.color, '#C8A27A');
  return <g key={'pl' + i} transform={`translate(${x} ${kf(a.y, t, f)}) scale(${s})`}>
    <rect x={-170} y={-30} width={340} height={30} fill="#A1887F" stroke={OL} strokeWidth={4} />
    {[-140, -10, 120].map((dx) => <rect key={dx} x={dx} y={-30} width={22} height={30} fill="#6D4C41" />)}
    {Array.from({length: n}, (_, k) => { const r = Math.floor(k / 3), cc = k % 3, vis = k >= Math.round(gone * n);
      return vis && <g key={k}><rect x={-165 + cc * 110} y={-30 - (r + 1) * 90} width={108} height={88} rx={4} fill={c} stroke={OL} strokeWidth={3} />
        <path d={`M ${-165 + cc * 110} ${-30 - (r + 1) * 90 + 44} L ${-57 + cc * 110} ${-30 - (r + 1) * 90 + 44}`} stroke="#FFFFFF" strokeWidth={4} opacity={0.4} /></g>; })}
    {gone < 0.2 && <rect x={-172} y={-30 - rows * 90 - 6} width={344} height={rows * 90 + 6} fill="#E3F2FD" opacity={0.18} stroke="#FFFFFF" strokeOpacity={0.6} strokeWidth={3} />}
    {a.text && <T x={0} y={-30 - rows * 45 + 10} s={a.textSize ?? 30} c={OL}>{a.text}</T>}
  </g>;
};

/** A rolled diploma with a ribbon that unrolls at `openAt` to reveal `text` (e.g. a balance owed) in red. */
const diploma: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 460), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const u = a.openAt !== undefined ? E.out(win(t, a.openAt, 0.9)) : 0, W = 120 + 520 * u;
  return <g key={'dp' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.rot ?? -6})`}>
    <rect x={-W / 2} y={-150} width={W} height={300} rx={8} fill="#FFF8E1" stroke={OL} strokeWidth={5} />
    {u > 0.6 && <g opacity={(u - 0.6) / 0.4}>
      <T x={0} y={-80} s={30} c="#6D4C41">{a.title || 'BACHELOR OF ARTS'}</T>
      <path d="M -200 -50 L 200 -50" stroke="#BCAAA4" strokeWidth={3} />
      <T x={0} y={40} s={a.size ?? 64} c={K.red}>{a.text || ''}</T>
      {a.sub && <T x={0} y={100} s={24} c="#6D4C41">{a.sub}</T>}</g>}
    {[-1, 1].map((d) => <g key={d}><ellipse cx={d * W / 2} cy={0} rx={30} ry={160} fill="#FFECB3" stroke={OL} strokeWidth={5} /></g>)}
    <rect x={-14} y={-160} width={28} height={320} fill={K.red} opacity={1 - u} stroke={OL} strokeWidth={3} />
    {u < 0.3 && <path d="M 0 140 L -30 220 M 0 140 L 30 220" stroke={K.red} strokeWidth={14} strokeLinecap="round" />}
  </g>;
};

/** Graduation caps tossed in the air: `n` caps launched at `at` (staggered), they fly up, spin and fall back. */
const gradcaps: ItemFn = (a, {t, f}, i) => {
  if (t < (a.at ?? 0) || (a.until !== undefined && t > a.until + 0.4)) return null;
  const n = a.n ?? 6, x0 = kf(a.x, t, 960), sp = a.spread ?? 700, s = a.scale ?? 1;
  return <g key={'gc' + i}>{Array.from({length: n}, (_, k) => {
    const tt = (t - (a.at ?? 0) - k * 0.18) % 3.2; if (tt < 0) return null;
    const x = x0 - sp / 2 + sp * (k + 0.5) / n + 40 * Math.sin(k), y = f - 200 - (520 * tt - 330 * tt * tt / 1.6) * (0.8 + 0.3 * rnd(k)) * (a.h ?? 1);
    return <g key={k} transform={`translate(${x} ${Math.min(y, f - 140)}) rotate(${tt * 220 * (k % 2 ? 1 : -1)}) scale(${s})`}>
      <path d="M -70 0 L 0 -28 L 70 0 L 0 28 Z" fill="#212121" stroke={OL} strokeWidth={4} />
      <path d="M -36 12 L -36 40 Q 0 56 36 40 L 36 12" fill="#212121" stroke={OL} strokeWidth={4} />
      <path d="M 0 0 L 52 18 L 52 50" stroke={K.gold} strokeWidth={5} fill="none" /><circle cx={52} cy={54} r={7} fill={K.gold} /></g>; })}</g>;
};

/** A generic sedan, side view (no brand): `color`, `x` keyframable (wheels spin), `sticker` window price sticker text,
 *  `lift` keyframable 0-1 raises it on a service lift, `soldAt` stamps SOLD on the windshield. */
const sedan: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const c = col(a.color, '#1E88E5'), lift = kf(a.lift, t, 0) * 220, spin = x * 0.03, sold = a.soldAt !== undefined ? E.outBack(win(t, a.soldAt, 0.4)) : 0;
  return <g key={'sd' + i} transform={`translate(${x} ${kf(a.y, t, f) - lift}) scale(${s})`}>
    {lift > 0 && <rect x={-200} y={60} width={400} height={16} fill="#FFC21A" stroke={OL} strokeWidth={3} />}
    <ellipse cx={0} cy={60 + lift / s} rx={300} ry={16} fill="#000" opacity={0.2} />
    <path d="M -300 20 L -300 -40 Q -290 -70 -240 -76 L -150 -84 L -80 -150 Q -60 -164 -20 -164 L 110 -164 Q 140 -164 165 -140 L 230 -84 L 280 -76 Q 310 -66 310 -30 L 310 20 Z" fill={c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <path d="M -130 -88 L -70 -146 L 20 -146 L 20 -88 Z" fill={K.glass} stroke={OL} strokeWidth={4} />
    <path d="M 40 -88 L 40 -146 L 105 -146 Q 125 -146 140 -128 L 190 -88 Z" fill={K.glass} stroke={OL} strokeWidth={4} />
    <path d="M -300 -20 L 310 -20" stroke="#FFFFFF" strokeWidth={4} opacity={0.35} />
    <rect x={-290} y={-40} width={30} height={16} rx={4} fill="#FFE082" stroke={OL} strokeWidth={2} />
    {[-180, 190].map((dx) => <g key={dx} transform={`translate(${dx} 20) rotate(${spin * 57})`}><circle r={52} fill="#263238" stroke={OL} strokeWidth={5} />
      <circle r={24} fill="#B0BEC5" stroke={OL} strokeWidth={3} /><path d="M -20 0 L 20 0 M 0 -20 L 0 20" stroke="#78909C" strokeWidth={4} /></g>)}
    {a.sticker && <g transform="translate(-20 -118)"><rect x={-60} y={-30} width={120} height={60} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
      <T x={0} y={12} s={a.sticker.length > 7 ? 18 : 26}>{a.sticker}</T></g>}
    {sold > 0 && <g transform={`translate(80 -118) rotate(-12) scale(${sold})`}><rect x={-60} y={-24} width={120} height={48} rx={6} fill={K.red} stroke={OL} strokeWidth={3} /><T x={0} y={12} s={30} c="#FFFFFF">SOLD</T></g>}
  </g>;
};

/** A home electricity meter: glass dome, spinning disc (speed `spin` keyframable), and a digital `$` readout counting
 *  with `steps` (like counter) or fixed `text`; `label` below. */
const meter: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 420), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const sp = kf(a.spin, t, 1), ang = (t * 180 * sp) % 360, v = a.steps ? kf(a.steps, t, 0) : null;
  const txt = v !== null ? (a.prefix ?? '$') + v.toLocaleString('en-US', {minimumFractionDigits: a.decimals ?? 0, maximumFractionDigits: a.decimals ?? 0}) + (a.suffix ?? '') : (a.text ?? '');
  return <g key={'mt' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-120} y={-40} width={240} height={330} rx={20} fill="#B0BEC5" stroke={OL} strokeWidth={6} />
    <circle cx={0} cy={0} r={150} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
    <circle cx={0} cy={0} r={130} fill="#E3F2FD" opacity={0.6} />
    <rect x={-90} y={-80} width={180} height={60} rx={8} fill="#0E1621" stroke={OL} strokeWidth={4} />
    <T x={0} y={-38} s={txt.length > 7 ? 30 : 38} c="#7DF29A">{txt}</T>
    <ellipse cx={0} cy={50} rx={90} ry={16} fill="#90A4AE" stroke={OL} strokeWidth={3} />
    <rect x={-6 + 80 * Math.cos(ang * Math.PI / 180)} y={42} width={12} height={16} fill={K.red} opacity={Math.sin(ang * Math.PI / 180) > 0 ? 1 : 0.3} />
    <T x={0} y={110} s={20} c="#546E7A">kWh</T>
    {a.label && <T x={0} y={250} s={28}>{a.label}</T>}
  </g>;
};

/** A modern bumper in cutaway: the painted cover slides away at `openAt` to reveal radar, parking sensors, wiring and a
 *  camera; `price` tag shows the repair bill (keyframable via `pages` [[t, text]]). */
const bumper: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const u = a.openAt !== undefined ? E.out(win(t, a.openAt, 1.0)) : 0;
  let price = a.price as string | undefined; for (const [at, txt] of (a.pages || []) as [number, string][]) if (t >= at) price = txt;
  const blink = Math.sin(t * 6) > 0;
  return <g key={'bp' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-420} y={-120} width={840} height={240} rx={60} fill="#263238" stroke={OL} strokeWidth={6} />
    <rect x={-240} y={-30} width={140} height={60} rx={10} fill="#90A4AE" stroke={OL} strokeWidth={4} />
    <T x={-170} y={8} s={22} c="#FFFFFF">RADAR</T>
    {[-360, -40, 120, 300].map((dx, q) => <g key={q}><circle cx={dx} cy={-60} r={20} fill="#B0BEC5" stroke={OL} strokeWidth={3} /><circle cx={dx} cy={-60} r={7} fill={blink ? '#7DF29A' : '#1B5E20'} /></g>)}
    <path d="M -360 -40 Q -300 60 -240 20 M -40 -40 Q -60 60 -100 20 M 120 -40 Q 60 80 -100 30 M 300 -40 Q 200 90 -100 40" fill="none" stroke="#FFC21A" strokeWidth={4} />
    <rect x={180} y={-10} width={130} height={80} rx={10} fill="#455A64" stroke={OL} strokeWidth={4} />
    <circle cx={245} cy={30} r={24} fill="#0E1621" stroke="#90A4AE" strokeWidth={4} />
    <T x={245} y={100} s={20} c="#FFFFFF">CAMERA</T>
    <g transform={`translate(${-u * 900} 0)`} opacity={1 - u}>
      <rect x={-440} y={-140} width={880} height={280} rx={70} fill={col(a.color, '#D32F2F')} stroke={OL} strokeWidth={6} />
      <path d="M -400 -80 Q 0 -130 400 -80" stroke="#FFFFFF" strokeWidth={8} opacity={0.3} fill="none" />
      <rect x={-120} y={-20} width={240} height={60} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={4} /></g>
    {price && <g transform="translate(0 -230)"><rect x={-170} y={-50} width={340} height={90} rx={12} fill={K.white} stroke={OL} strokeWidth={5} />
      <T x={0} y={14} s={42} c={K.red}>{price}</T></g>}
  </g>;
};

/** A generic delivery van (no brand): `x` keyframable, wheels spin, rear doors open at `openAt` showing parcels;
 *  `text` on the side. */
const van: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const spin = x * 0.03, op = a.openAt !== undefined ? E.out(win(t, a.openAt, 0.7)) : 0, c = col(a.color, '#ECEFF1');
  return <g key={'vn' + i} transform={`translate(${x} ${kf(a.y, t, f)}) scale(${s})`}>
    <ellipse cx={0} cy={60} rx={330} ry={16} fill="#000" opacity={0.2} />
    <path d="M -320 30 L -320 -250 L 160 -250 L 250 -140 L 320 -110 L 320 30 Z" fill={c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <path d="M 170 -235 L 240 -145 L 170 -145 Z" fill={K.glass} stroke={OL} strokeWidth={4} />
    <rect x={-320} y={-60} width={640} height={16} fill="#1565C0" />
    {a.text && <T x={-90} y={-130} s={44} c="#1565C0">{a.text}</T>}
    {op > 0 && <g><rect x={-330 - 80 * op} y={-250} width={20 + 70 * op} height={260} fill={c} stroke={OL} strokeWidth={4} />
      {[0, 1, 2].map((k) => <rect key={k} x={-300} y={-80 - k * 60} width={90} height={56} rx={4} fill="#C8A27A" stroke={OL} strokeWidth={3} />)}</g>}
    {[-200, 200].map((dx) => <g key={dx} transform={`translate(${dx} 30) rotate(${spin * 57})`}><circle r={54} fill="#263238" stroke={OL} strokeWidth={5} />
      <circle r={22} fill="#B0BEC5" stroke={OL} strokeWidth={3} /><path d="M -18 0 L 18 0 M 0 -18 L 0 18" stroke="#78909C" strokeWidth={4} /></g>)}
  </g>;
};

/** A row of phone screens that appear one by one (`stepAt` [times]), each with a `titles[k]` line and option buttons,
 *  showing a long multi-step flow; `counter` text (e.g. "6 CLICKS") pops at the end. `short` draws a single-button screen. */
const flowscreens: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const steps: number[] = a.stepAt || [0], titles: string[] = a.titles || [], n = steps.length, gap = a.gap ?? 260;
  return <g key={'fs' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {steps.map((st, k) => { const u = E.outBack(win(t, st, 0.4)); if (u <= 0) return null; const cx = (k - (n - 1) / 2) * gap;
      return <g key={k} transform={`translate(${cx} 0) scale(${u})`}>
        <rect x={-100} y={-180} width={200} height={360} rx={26} fill="#263238" stroke={OL} strokeWidth={5} />
        <rect x={-86} y={-160} width={172} height={310} rx={14} fill="#FFFFFF" />
        <T x={0} y={-118} s={20} w={160}>{titles[k] || 'Are you sure?'}</T>
        {Array.from({length: a.short ? 1 : 3}, (_, b) => <rect key={b} x={-70} y={-70 + b * 62} width={140} height={44} rx={10} fill={b === 0 ? (a.short ? '#43A047' : '#FFC21A') : '#ECEFF1'} stroke={OL} strokeWidth={2} />)}
        {k < n - 1 && <path d={`M 108 0 L ${gap - 108} 0`} stroke={K.red} strokeWidth={5} strokeDasharray="10 8" />}</g>; })}
    {a.counter && a.counterAt !== undefined && t >= a.counterAt && <g transform={`translate(0 250) scale(${E.outBack(win(t, a.counterAt, 0.4))})`}>
      <rect x={-220} y={-46} width={440} height={80} rx={14} fill={a.short ? '#43A047' : K.red} stroke={OL} strokeWidth={4} /><T x={0} y={12} s={40} c="#FFFFFF">{a.counter}</T></g>}
  </g>;
};

/** A growing two-sided network: cardholders (blue cards, left) and stores (orange awnings, right) joined by lines.
 *  `steps` [[t, nCards, nStores], ...] grows the counts; `labels` [left, right]; `rival` draws a tiny lonely pair below
 *  from `rivalAt` (a new network with no links). */
const netmesh: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 460), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const st: [number, number, number][] = a.steps || [[0, 2, 2]];
  let nc = st[0][1], ns = st[0][2];
  for (let k = 1; k < st.length; k++) { if (t < st[k][0]) break; const u = E.out(clamp((t - st[k][0]) / 1.2)); nc = lerp(st[k - 1][1], st[k][1], u); ns = lerp(st[k - 1][2], st[k][2], u); }
  const C_ = Math.max(1, Math.round(nc)), S_ = Math.max(1, Math.round(ns)), H = 520;
  const cy = (k: number, n: number) => -H / 2 + (H * (k + 0.5)) / n;
  const lab: string[] = a.labels || ['CARDHOLDERS', 'STORES'];
  const ra = a.rivalAt;
  return <g transform={`translate(${x} ${y}) scale(${s})`} key={i}>
    {Array.from({length: C_}, (_, p) => Array.from({length: S_}, (_, q) => <path key={p + '-' + q} d={`M -300 ${cy(p, C_)} C -60 ${cy(p, C_)} 60 ${cy(q, S_)} 300 ${cy(q, S_)}`} stroke="#4FC3F7" strokeWidth={2} opacity={0.35} fill="none" />))}
    {Array.from({length: C_}, (_, p) => <g key={'c' + p} transform={`translate(-330 ${cy(p, C_)})`}><rect x={-34} y={-20} width={68} height={42} rx={6} fill="#1E88E5" stroke={OL} strokeWidth={3} /><rect x={-24} y={-8} width={14} height={11} rx={2} fill="#FFD54F" /></g>)}
    {Array.from({length: S_}, (_, q) => <g key={'s' + q} transform={`translate(330 ${cy(q, S_)})`}><rect x={-30} y={-14} width={60} height={34} fill="#FFF3E0" stroke={OL} strokeWidth={3} /><path d="M -36 -14 L -28 -30 L 28 -30 L 36 -14 Z" fill="#FB8C00" stroke={OL} strokeWidth={3} /></g>)}
    {[-330, 330].map((lx, q) => <g key={"lb" + q}><rect x={lx - 130} y={-H / 2 - 78} width={260} height={52} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={lx} y={-H / 2 - 42} s={26} c="#1B3A5C">{lab[q]}</T></g>)}
    <T x={0} y={H / 2 + 60} s={34} c="#FFC21A">{`${C_ * S_} LINKS`}</T>
    {ra !== undefined && t >= ra && <g opacity={clamp((t - ra) / 0.6)} transform={`translate(0 ${H / 2 + 150})`}>
      <rect x={-140} y={-20} width={56} height={36} rx={6} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
      <rect x={90} y={-14} width={52} height={30} fill="#ECEFF1" stroke={OL} strokeWidth={3} />
      <path d="M -80 0 L 86 0" stroke="#B0BEC5" strokeWidth={3} strokeDasharray="10 10" />
      <T x={0} y={-36} s={24} c="#B0BEC5">{a.rivalText || 'A NEW NETWORK: NO LINKS'}</T></g>}
  </g>;
};

/** An egg carton (12 eggs) with a price tag; `pages` [[t, price]] changes the price; `empty` [[t, n]] removes eggs (supply). */
const eggcarton: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  let price = a.price ?? '$1.46'; for (const p of (a.pages || [])) if (t >= p[0]) price = p[1];
  let gone = 0; for (const e of (a.empty || [])) if (t >= e[0]) gone = e[1];
  return <g transform={`translate(${x} ${y}) scale(${s})`} key={i}>
    <path d="M -260 -40 L 260 -40 L 230 90 L -230 90 Z" fill="#B0A48E" stroke={OL} strokeWidth={5} />
    {Array.from({length: 12}, (_, k) => { const cx = -205 + (k % 6) * 82, cy = k < 6 ? -40 : 10;
      return k >= 12 - gone ? <ellipse key={k} cx={cx} cy={cy + 20} rx={30} ry={14} fill="#8C806B" /> : <ellipse key={k} cx={cx} cy={cy} rx={32} ry={40} fill="#FFF8E7" stroke={OL} strokeWidth={4} />; })}
    <path d="M -260 -40 L -240 -160 L 240 -160 L 260 -40" fill="none" stroke={OL} strokeWidth={5} opacity={0.5} />
    <g transform="translate(210 -150) rotate(8)"><rect x={-110} y={-44} width={220} height={88} rx={10} fill="#FFC21A" stroke={OL} strokeWidth={5} />
      <T x={0} y={18} s={52} c={OL}>{price}</T></g>
    {a.text && <T x={0} y={150} s={32} c="#FFFFFF">{a.text}</T>}
  </g>;
};

/** A pyramid of gold bars (`rows`), each bar a trapezoid with a shine; optional `tag` price label in front. */
const bars: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 700), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const rows = a.rows ?? 4, out: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) { const n = rows - r;
    for (let k = 0; k < n; k++) { const bx = (k - (n - 1) / 2) * 150, by = -r * 62;
      out.push(<g key={r + '-' + k} transform={`translate(${bx} ${by})`}><path d="M -70 0 L 70 0 L 52 -56 L -52 -56 Z" fill="#F4C430" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <path d="M -50 -48 L 50 -48 L 42 -36 L -42 -36 Z" fill="#FFE58A" /><path d="M 52 -56 L 70 0" stroke="#C99A00" strokeWidth={6} /></g>); } }
  return <g transform={`translate(${x} ${y}) scale(${s})`} key={i}>{out}
    {a.tag && <g transform="translate(0 50)"><rect x={-150} y={-36} width={300} height={72} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
      <T x={0} y={14} s={42} c={OL}>{a.tag}</T></g>}</g>;
};

/** A giant generic coin (no real coin design): `metal` copper|silver, `value` text (e.g. "1¢"), optional price `tag`
 *  hanging from it ("COST 3.69¢"), `spin` makes it turn (scaleX). */
const bigcoin: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 460), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const cu = (a.metal ?? 'copper') === 'copper', fill = cu ? '#C77B3A' : '#CFD8DC', rim = cu ? '#9C5A25' : '#90A4AE';
  const sx = a.spin ? Math.max(0.15, Math.abs(Math.cos(t * 1.6))) : 1;
  return <g transform={`translate(${x} ${y}) scale(${s})`} key={i}>
    <g transform={`scale(${sx} 1)`}><circle r={170} fill={rim} stroke={OL} strokeWidth={8} /><circle r={140} fill={fill} stroke={OL} strokeWidth={5} />
      {Array.from({length: 40}, (_, k) => { const an = (k / 40) * Math.PI * 2; return <path key={k} d={`M ${Math.cos(an) * 152} ${Math.sin(an) * 152} L ${Math.cos(an) * 166} ${Math.sin(an) * 166}`} stroke={OL} strokeWidth={3} />; })}
      <T x={0} y={36} s={110} c={OL}>{a.value || '1¢'}</T></g>
    {a.tag && <g transform="translate(150 150) rotate(12)"><path d="M -10 -40 L 20 -40" stroke={OL} strokeWidth={4} />
      <rect x={-20} y={-30} width={260} height={80} rx={12} fill="#FFC21A" stroke={OL} strokeWidth={6} /><T x={110} y={22} s={40} c={OL}>{a.tag}</T></g>}
  </g>;
};

/** A generic bank-app statement (no bank name or logo): `start` balance, `rows` [{at, label, amt, fee?}] appear one by one;
 *  the big running balance turns red below zero and fee rows flash red. `title` header text. */
const statement: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 480), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const rows: any[] = a.rows ?? [], shown = rows.filter((r) => t >= (r.at ?? 0));
  const bal = (a.start ?? 0) + shown.reduce((q, r) => q + (r.amt ?? 0), 0), neg = bal < 0;
  const fmt = (v: number) => (v < 0 ? '−$' : '$') + Math.abs(v).toFixed(2);
  const W = 520, H = 130 + Math.max(rows.length, 3) * 74 + 40;
  return <g key={'st' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 + 14} y={-H / 2 + 18} width={W} height={H} rx={34} fill="#000" opacity={0.25} />
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={34} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    <rect x={-W / 2} y={-H / 2} width={W} height={130} rx={34} fill={neg ? '#E53935' : '#1E88E5'} stroke={OL} strokeWidth={6} />
    <rect x={-W / 2 + 3} y={-H / 2 + 100} width={W - 6} height={30} fill={neg ? '#E53935' : '#1E88E5'} />
    <T x={-W / 2 + 30} y={-H / 2 + 42} s={24} c="#FFFFFF" a="start" o={0.85}>{a.title || 'CHECKING · BALANCE'}</T>
    <T x={-W / 2 + 30} y={-H / 2 + 104} s={60} c="#FFFFFF" a="start">{fmt(bal)}</T>
    {shown.map((r, k) => { const ry = -H / 2 + 175 + k * 74, fl = r.fee ? 0.5 + 0.5 * Math.sin(Math.PI * clamp((t - r.at) / 0.6)) : 0;
      const ap = clamp((t - r.at) / 0.35);
      return <g key={k} opacity={ap} transform={`translate(${(1 - ap) * 40} 0)`}>
        {r.fee && <rect x={-W / 2 + 14} y={ry - 44} width={W - 28} height={64} rx={12} fill="#FFCDD2" opacity={0.6 + 0.4 * fl} />}
        <T x={-W / 2 + 34} y={ry} s={30} c={r.fee ? '#C62828' : OL} a="start">{r.label}</T>
        <T x={W / 2 - 34} y={ry} s={30} c={r.fee ? '#C62828' : (r.amt ?? 0) < 0 ? OL : '#2E7D32'} a="end">{fmt(r.amt ?? 0)}</T>
        <path d={`M ${-W / 2 + 24} ${ry + 26} L ${W / 2 - 24} ${ry + 26}`} stroke="#ECEFF1" strokeWidth={3} /></g>; })}
  </g>;
};

/** A generic IV bag on a pole (no brand): fluid `level` 0..1 (keyframes ok), drips fall from the line; `text` label on the bag;
 *  `pole` false hides the stand. */
const ivbag: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 600), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const lv = clamp(kf(a.level, t, 0.8)), W = 150, H = 210, top = -H / 2 + 20, fy = top + (H - 40) * (1 - lv);
  const drip = (t * 1.3) % 1;
  return <g key={'iv' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {a.pole !== false && <g><path d={`M 0 ${-H / 2 - 70} L 0 520`} stroke="#90A4AE" strokeWidth={12} strokeLinecap="round" />
      <path d={`M -60 ${-H / 2 - 70} L 60 ${-H / 2 - 70}`} stroke="#90A4AE" strokeWidth={10} strokeLinecap="round" />
      <path d="M -90 520 L 90 520 M 0 520 L -70 560 M 0 520 L 70 560" stroke="#78909C" strokeWidth={10} strokeLinecap="round" /></g>}
    <path d={`M 0 ${-H / 2 - 70} L 0 ${-H / 2 - 10}`} stroke="#B0BEC5" strokeWidth={5} />
    <clipPath id={'ivc' + i}><rect x={-W / 2} y={-H / 2} width={W} height={H} rx={34} /></clipPath>
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={34} fill="#F5FBFF" stroke={OL} strokeWidth={6} />
    <g clipPath={`url(#ivc${i})`}><rect x={-W / 2} y={fy} width={W} height={H} fill={lv < 0.2 ? '#FFAB91' : '#B3E5FC'} />
      <path d={`M ${-W / 2} ${fy} q ${W / 4} ${-8 * Math.sin(t * 3)} ${W / 2} 0 t ${W / 2} 0`} fill="none" stroke="#4FC3F7" strokeWidth={4} /></g>
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={34} fill="none" stroke={OL} strokeWidth={6} />
    {[0, 1, 2, 3].map((k) => <path key={k} d={`M ${W / 2 - 34} ${-H / 2 + 40 + k * 36} L ${W / 2 - 12} ${-H / 2 + 40 + k * 36}`} stroke={OL} strokeWidth={3} />)}
    {a.text && <T x={-8} y={10} s={26} c={OL}>{a.text}</T>}
    <path d={`M -16 ${H / 2} L 16 ${H / 2} L 10 ${H / 2 + 34} L -10 ${H / 2 + 34} Z`} fill="#E0E0E0" stroke={OL} strokeWidth={4} />
    <rect x={-12} y={H / 2 + 34} width={24} height={46} rx={6} fill="#F5FBFF" stroke={OL} strokeWidth={4} />
    {lv > 0.02 && <circle cx={0} cy={H / 2 + 44 + drip * 30} r={6} fill="#4FC3F7" opacity={1 - drip} />}
    <path d={`M 0 ${H / 2 + 80} q 40 120 -20 260`} fill="none" stroke="#B0BEC5" strokeWidth={5} />
  </g>;
};

/** A generic yes/no event-contract ticket: `q` question text, `yes` price in cents (keyframes ok); the bar splits YES/NO
 *  at that price; `settle` = 'yes' | 'no' with `settleAt` (s) flashes the winner and drops the $1 to that side. */
const yesno: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 420), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const p = clamp(kf(a.yes, t, 50) / 100), W = 620, done = a.settleAt !== undefined && t >= a.settleAt, win = a.settle || 'yes';
  const fl = done ? 0.5 + 0.5 * Math.sin((t - a.settleAt) * 8) : 0;
  return <g key={'yn' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 + 12} y={-150 + 16} width={W} height={300} rx={28} fill="#000" opacity={0.25} />
    <rect x={-W / 2} y={-150} width={W} height={300} rx={28} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    <T x={0} y={-90} s={32} c={OL} w={W - 60}>{a.q || 'WILL IT HAPPEN?'}</T>
    <rect x={-W / 2 + 30} y={-40} width={(W - 60) * p} height={90} rx={14} fill="#43A047" stroke={OL} strokeWidth={4} opacity={done && win !== 'yes' ? 0.35 : 1 - fl * 0.3} />
    <rect x={-W / 2 + 30 + (W - 60) * p} y={-40} width={(W - 60) * (1 - p)} height={90} rx={14} fill="#E53935" stroke={OL} strokeWidth={4} opacity={done && win !== 'no' ? 0.35 : 1 - fl * 0.3} />
    {p > 0.18 && <T x={-W / 2 + 30 + (W - 60) * p / 2} y={18} s={34} c="#FFFFFF">{'YES ' + Math.round(p * 100) + '¢'}</T>}
    {p < 0.82 && <T x={-W / 2 + 30 + (W - 60) * (p + (1 - p) / 2)} y={18} s={34} c="#FFFFFF">{'NO ' + Math.round((1 - p) * 100) + '¢'}</T>}
    <T x={0} y={110} s={26} c="#546E7A">{done ? (win === 'yes' ? 'YES WINS · PAYS $1' : 'NO WINS · PAYS $1') : 'WINNER GETS $1 PER CONTRACT'}</T>
  </g>;
};

/** A giant generic paper check (no bank name): `amount` text, `memo`, `payee`; `ghost` true draws it faint and dashed
 *  (a check that was not paid). */
const bigcheck: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 420), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const g = !!a.ghost, W = 760, H = 330;
  return <g key={'bc' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${a.rot ?? -3})`} opacity={g ? 0.45 : 1}>
    {!g && <rect x={-W / 2 + 14} y={-H / 2 + 18} width={W} height={H} rx={18} fill="#000" opacity={0.25} />}
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={18} fill={g ? 'none' : '#E8F5E9'} stroke={g ? '#FFFFFF' : OL} strokeWidth={6} strokeDasharray={g ? '18 12' : undefined} />
    <T x={-W / 2 + 30} y={-H / 2 + 50} s={26} c={g ? '#FFFFFF' : '#2E7D32'} a="start">{a.title || 'DIVIDEND PAYMENT'}</T>
    <T x={W / 2 - 30} y={-H / 2 + 50} s={22} c={g ? '#FFFFFF' : '#546E7A'} a="end">{a.date || ''}</T>
    <T x={-W / 2 + 30} y={-10} s={26} c={g ? '#FFFFFF' : OL} a="start">{'PAY TO: ' + (a.payee || 'EVERY RESIDENT')}</T>
    <rect x={W / 2 - 300} y={-60} width={270} height={80} rx={10} fill={g ? 'none' : '#FFFFFF'} stroke={g ? '#FFFFFF' : OL} strokeWidth={4} />
    <T x={W / 2 - 165} y={-6} s={46} c={g ? '#FFFFFF' : OL}>{a.amount || ',000'}</T>
    <path d={`M ${-W / 2 + 30} 70 L ${W / 2 - 30} 70`} stroke={g ? '#FFFFFF' : '#90A4AE'} strokeWidth={3} />
    <T x={-W / 2 + 30} y={120} s={22} c={g ? '#FFFFFF' : '#546E7A'} a="start">{a.memo || 'MEMO: PERMANENT FUND'}</T>
  </g>;
};

/** A team bench: `n` seats in a row with seated players (generic jerseys, no logos); after `cutAt` the last `cut` seats empty
 *  and turn red; `label` sign above. */
const bench: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const n = a.n ?? 10, cut = a.cut ?? 0, done = a.cutAt !== undefined && t >= a.cutAt, W = n * 90;
  const cols = ['#E53935', '#1E88E5', '#43A047', '#FB8C00', '#8E24AA'];
  return <g key={'bn' + i} transform={`translate(${x} ${f}) scale(${s})`}>
    <rect x={-W / 2 - 20} y={-110} width={W + 40} height={26} rx={8} fill="#8D6E63" stroke={OL} strokeWidth={4} />
    {[-W / 2, W / 2].map((lx, k) => <rect key={k} x={lx - 8} y={-84} width={16} height={84} fill="#6D4C41" />)}
    {Array.from({length: n}, (_, k) => { const sx = -W / 2 + 45 + k * 90, empty = done && k >= n - cut;
      const bob = Math.sin(t * 2 + k) * 3;
      return <g key={k}>
        {empty ? <rect x={sx - 30} y={-150} width={60} height={40} rx={8} fill="#FFCDD2" stroke="#C62828" strokeWidth={4} strokeDasharray="8 6" />
          : <g transform={`translate(${sx} ${bob})`}>
            <rect x={-26} y={-190} width={52} height={80} rx={14} fill={cols[k % 5]} stroke={OL} strokeWidth={4} />
            <T x={0} y={-140} s={22} c="#FFFFFF">{String(k + 1)}</T>
            <circle cx={0} cy={-212} r={22} fill={['#F6C9A0', '#C68B59', '#8D5524', '#FFDBAC'][k % 4]} stroke={OL} strokeWidth={4} />
            <path d="M -16 -110 L -16 -60 M 16 -110 L 16 -60" stroke={OL} strokeWidth={8} strokeLinecap="round" /></g>}
      </g>; })}
    {a.label && <g transform={`translate(0 -300)`}><rect x={-230} y={-36} width={460} height={66} rx={12} fill="#1B1F27" stroke={OL} strokeWidth={5} />
      <T x={0} y={12} s={32} c="#FFC21A">{a.label}</T></g>}
  </g>;
};

/** A glass box of segregated customer money: coins inside, a padlock; `label` on the plate; `crackAt` cracks the glass,
 *  `drainAt` lowers the coin level to `drainTo` (0..1); `watchAt` adds a camera watching it; `fill` 0..1 initial level. */
const glassbox: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 240), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const W = 420, H = 320, crack = a.crackAt !== undefined && t >= a.crackAt;
  const d = a.drainAt !== undefined ? clamp((t - a.drainAt) / 2.5) : 0, lv = (a.fill ?? 0.8) * (1 - d * (1 - (a.drainTo ?? 0.3)));
  const rows = Math.round(6 * lv), out: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) for (let k = 0; k < 7; k++) out.push(<ellipse key={r + '-' + k} cx={-W / 2 + 40 + k * 56 + (r % 2) * 20} cy={H / 2 - 30 - r * 44} rx={24} ry={12} fill="#FFC21A" stroke={OL} strokeWidth={3} />);
  return <g key={'gb' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 - 20} y={H / 2} width={W + 40} height={40} rx={8} fill="#546E7A" stroke={OL} strokeWidth={5} />
    {out}
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={10} fill="#B3E5FC" opacity={0.35} stroke={OL} strokeWidth={6} />
    <path d={`M ${-W / 2 + 30} ${-H / 2 + 20} L ${-W / 2 + 90} ${-H / 2 + 120}`} stroke="#FFFFFF" strokeWidth={8} opacity={0.6} strokeLinecap="round" />
    {crack && <path d={`M 40 ${-H / 2} L 10 -60 L 60 -20 L 20 40 L 70 90 M 10 -60 L -40 -30 M 60 -20 L 120 -50`} fill="none" stroke="#FFFFFF" strokeWidth={6} />}
    {crack && <path d={`M 40 ${-H / 2} L 10 -60 L 60 -20 L 20 40 L 70 90`} fill="none" stroke={OL} strokeWidth={2} />}
    <g transform={`translate(0 ${-H / 2 - 30})`}><path d="M -28 0 L -28 -26 A 28 28 0 0 1 28 -26 L 28 0" fill="none" stroke="#90A4AE" strokeWidth={10} />
      <rect x={-40} y={-4} width={80} height={60} rx={10} fill={crack ? '#E53935' : '#FFC21A'} stroke={OL} strokeWidth={5} /></g>
    <rect x={-W / 2 + 40} y={H / 2 + 50} width={W - 80} height={46} rx={8} fill="#1B1F27" />
    <T x={0} y={H / 2 + 82} s={26} c="#FFFFFF">{a.label || 'CUSTOMER MONEY'}</T>
    {a.watchAt !== undefined && t >= a.watchAt && <g transform={`translate(${W / 2 + 60} ${-H / 2 - 40}) rotate(${20 + Math.sin(t * 1.5) * 10})`}>
      <rect x={-50} y={-24} width={100} height={48} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><circle cx={-50} cy={0} r={14} fill="#1B1F27" />
      <circle cx={46} cy={-14} r={6} fill={Math.sin(t * 6) > 0 ? '#E53935' : '#7F0000'} /></g>}
  </g>;
};

/** A generic two-stage reusable rocket (no markings). `launchAt`: lifts off with flame and smoke. `landAt`: draws the
 *  booster only, dropping from the sky with a landing burn, legs unfolding, until it stands on the pad. */
const rocket: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), base = kf(a.y, t, f - 30), s = (a.scale ?? 0.5) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const land = a.landAt !== undefined, up = a.launchAt !== undefined ? clamp((t - a.launchAt) / 4) : 0;
  let dy = -2800 * up * up, burn = up > 0 && up < 1, legs = 1;
  if (land) { const u = clamp((t - a.landAt) / 2.8); dy = -2200 * Math.pow(1 - u, 2.2); burn = u > 0.05 && u < 1; legs = clamp((u - 0.6) / 0.3); if (t < a.landAt) return null; }
  const shake = burn ? Math.sin(t * 70) * 3 : 0, fl = 90 + 40 * Math.abs(Math.sin(t * 31));
  const smoke = !land && a.launchAt !== undefined && t > a.launchAt ? Array.from({length: 9}, (_, k) => { const g = clamp((t - a.launchAt - k * 0.12) / 2.5);
    return g > 0 ? <circle key={'sm' + k} cx={(k - 4) * 70 * (0.6 + g)} cy={-20 - 40 * g} r={70 + 120 * g} fill="#ECEFF1" opacity={0.85 * (1 - g * 0.6)} stroke={OL} strokeWidth={3} /> : null; }) : null;
  return <g key={'rk' + i} transform={`translate(${x} ${base}) scale(${s})`}>
    {smoke}
    <g transform={`translate(${shake} ${dy})`}>
      {burn && <path d={`M -34 0 Q 0 ${fl * 2.6} 34 0 Z`} fill="#FFC93C" stroke="#FF7043" strokeWidth={8} />}
      {burn && <path d={`M -18 0 Q 0 ${fl * 1.5} 18 0 Z`} fill="#FFFFFF" />}
      {[-1, 1].map((d) => <path key={d} d={`M ${d * 40} -90 L ${d * (40 + 70 * legs)} ${-20 + 20 * legs}`} stroke="#37474F" strokeWidth={10} strokeLinecap="round" />)}
      <rect x={-40} y={-620} width={80} height={620} rx={6} fill="#F5F7FA" stroke={OL} strokeWidth={5} />
      <rect x={-40} y={-420} width={80} height={18} fill="#B0BEC5" />
      {land && <path d="M -40 -560 Q 0 -540 40 -560 L 40 -300 Q 0 -280 -40 -300 Z" fill="#8D8D8D" opacity={0.35} />}
      {[-1, 1].map((d) => <rect key={'gf' + d} x={d > 0 ? 40 : -66} y={-600} width={26} height={30} fill="#546E7A" stroke={OL} strokeWidth={3} />)}
      {!land && <g>
        <rect x={-40} y={-670} width={80} height={50} fill="#263238" stroke={OL} strokeWidth={4} />
        <rect x={-40} y={-860} width={80} height={190} fill="#F5F7FA" stroke={OL} strokeWidth={5} />
        <path d="M -46 -860 L 46 -860 L 46 -940 Q 30 -1040 0 -1060 Q -30 -1040 -46 -940 Z" fill="#F5F7FA" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      </g>}
    </g>
    {a.text && <T x={0} y={120} s={44} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** A broadband satellite constellation: rows of small flat satellites drifting across low orbit. From `beamAt`, a few
 *  of them shine beams down to little dishes on the ground line (`ground`, default y + 520). */
const constellation: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const W = a.w ?? 1600, n = a.n ?? 14, rows = a.rows ?? 3, g = a.ground ?? 520, beam = a.beamAt !== undefined && t >= a.beamAt;
  const sats: React.ReactNode[] = [], beams: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) for (let k = 0; k < n; k++) {
    const u = ((k / n + t * (0.02 + 0.006 * r)) % 1), sx = -W / 2 + u * W, sy = -r * 90 + 30 * Math.sin(u * Math.PI * 2 + r);
    sats.push(<g key={r + '-' + k} transform={`translate(${sx} ${sy}) rotate(${-12 + r * 6})`}>
      <rect x={-30} y={-6} width={60} height={12} rx={3} fill="#ECEFF1" stroke={OL} strokeWidth={2} />
      <rect x={-26} y={-26} width={52} height={18} fill="#1E3A8A" stroke="#90CAF9" strokeWidth={2} /></g>);
    if (beam && r === 0 && k % 3 === 0) beams.push(<path key={'b' + k} d={`M ${sx} ${sy} L ${sx - 50} ${g} L ${sx + 50} ${g} Z`} fill="#7DF9FF" opacity={0.12 + 0.08 * Math.sin(t * 4 + k)} />);
  }
  return <g key={'cs' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {beams}{sats}
    {beam && Array.from({length: 5}, (_, k) => <g key={'d' + k} transform={`translate(${-W / 2 + 160 + k * (W - 320) / 4} ${g})`}>
      <rect x={-6} y={-40} width={12} height={40} fill="#546E7A" /><rect x={-44} y={-70} width={88} height={34} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={3} transform="rotate(-18)" /></g>)}
    {a.text && <T x={0} y={g + 70} s={34} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** CHIP BUDDY (original design): a cute computer chip with a face, pin legs and little arms, bouncing with squash and
 *  stretch. `mood` (happy | worry | shock | cool | sad) or `moods` [[t, mood], ...] to change it over time; `hop` jump
 *  height (0 = idle wobble), `hopRate`, `look` (-1..1 pupils), `label` printed on the die, `color`. */
const chipbuddy: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  let mood: string = a.mood ?? 'happy';
  for (const [mt, m] of (a.moods || []) as [number, string][]) if (t >= mt) mood = m;
  const hopH = a.hop ?? 26, ph = Math.abs(Math.sin(t * (a.hopRate ?? 3.2) + i * 1.3)), air = hopH * ph;
  const st = hopH > 0 ? 0.1 * ph - 0.12 * Math.max(0, 0.25 - ph) * 4 : 0.03 * Math.sin(t * 3 + i);
  const sy = 1 + st, sx = 1 / sy, c = col(a.color, '#2EC4B6'), look = (a.look ?? 0) * 8 + 3 * Math.sin(t * 0.9 + i);
  const shake = mood === 'shock' ? 4 * Math.sin(t * 50) : 0, B = 150;
  const mouth = mood === 'happy' ? <path d="M -30 34 Q 0 64 30 34" fill="#3B0A1A" stroke={OL} strokeWidth={4} />
    : mood === 'shock' ? <ellipse cx={0} cy={44} rx={16} ry={22} fill="#3B0A1A" stroke={OL} strokeWidth={4} />
    : mood === 'cool' ? <path d="M -24 42 L 26 38" stroke={OL} strokeWidth={5} strokeLinecap="round" />
    : mood === 'sad' ? <path d="M -28 52 Q 0 28 28 52" fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
    : <path d="M -30 46 q 10 -10 20 0 q 10 10 20 0 q 10 -10 20 0" fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />;
  const brow = mood === 'worry' || mood === 'sad' ? [12, -12] : mood === 'shock' ? [-6, 6] : mood === 'cool' ? [0, 0] : [-4, 4];
  return <g key={'cb' + i} transform={`translate(${x + shake} ${y}) scale(${s * (a.flip ? -1 : 1)} ${s})`}>
    <ellipse cx={0} cy={4} rx={70 - air * 0.6} ry={12} fill="#000000" opacity={0.25} />
    <g transform={`translate(0 ${-air})`}>
      {[-1, 1].map((d) => <g key={'lg' + d}><path d={`M ${d * 30} -14 L ${d * 34} -2`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
        <ellipse cx={d * 40} cy={0} rx={18} ry={9} fill="#263238" stroke={OL} strokeWidth={3} /></g>)}
      <g transform={`translate(0 -14) scale(${sx} ${sy}) translate(0 ${-B / 2})`}>
        {[-1, 1].map((d) => Array.from({length: 4}, (_, k) => <rect key={'p' + d + k} x={d > 0 ? B / 2 - 2 : -B / 2 - 16} y={-50 + k * 30} width={18} height={12} rx={3} fill="#CFD8DC" stroke={OL} strokeWidth={3} />))}
        {[-1, 1].map((d) => { const wave = mood === 'happy' ? Math.sin(t * 8 + d) * 25 : mood === 'shock' ? -60 : 10;
          return <path key={'ar' + d} d={`M ${d * (B / 2 + 14)} 6 q ${d * 30} ${-10 + wave * 0.3} ${d * 40} ${wave}`} fill="none" stroke={OL} strokeWidth={7} strokeLinecap="round" />; })}
        <rect x={-B / 2} y={-B / 2} width={B} height={B} rx={26} fill={c} stroke={OL} strokeWidth={6} />
        <rect x={-B / 2 + 14} y={-B / 2 + 12} width={B - 28} height={20} rx={8} fill="#FFFFFF" opacity={0.25} />
        {[-1, 1].map((d) => <g key={'e' + d}>
          <ellipse cx={d * 28} cy={-10} rx={20} ry={mood === 'shock' ? 26 : 22} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
          <circle cx={d * 28 + look} cy={-6} r={mood === 'shock' ? 6 : 9} fill={OL} />
          <path d={`M ${d * 28 - 16} ${-40 + (d < 0 ? brow[0] : brow[1]) * 0.5} L ${d * 28 + 16} ${-40 + (d < 0 ? brow[1] : brow[0]) * 0.5}`} stroke={OL} strokeWidth={5} strokeLinecap="round" /></g>)}
        {mood === 'cool' && <path d="M -54 -20 L 54 -20 L 46 2 L 10 2 L 4 -10 L -4 -10 L -10 2 L -46 2 Z" fill="#111" stroke={OL} strokeWidth={3} />}
        {mouth}
        {(mood === 'worry' || mood === 'sad') && <path d={`M ${B / 2 - 18} -40 q 8 14 0 22 q -8 -8 0 -22 Z`} fill="#81D4FA" stroke={OL} strokeWidth={2} transform={`translate(0 ${(t * 30) % 30})`} />}
        {a.label && <T x={0} y={B / 2 - 12} s={20} c="#FFFFFF">{a.label}</T>}
      </g>
      {mood === 'shock' && [0, 1, 2, 3].map((k) => <path key={'sk' + k} d={`M ${-110 + k * 70} ${-215} l ${-10 + k * 7} -30`} stroke={K.gold} strokeWidth={6} strokeLinecap="round" />)}
    </g>
    {a.text && <T x={0} y={60} s={30} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** STOCK ELEVATOR (original design): a chrome elevator shaft whose floors are labelled with values (`floors`, top to
 *  bottom); the gold car drops one floor at each time in `stops` (accelerating fall, then a squashy landing), its LED
 *  display shows the current floor's label, a worried chip rides inside. `text` caption below. */
const stockelevator: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 160), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const floors: string[] = a.floors || ['$4.50TN', '$4.31TN', '$4.07TN'], stops: number[] = a.stops || [], FH = a.fh ?? 230, n = floors.length;
  let pos = 0, sq = 0, falling = false;
  stops.forEach((ts, k) => { const u = clamp((t - (ts - 0.7)) / 0.7); pos += u * u; if (u > 0 && u < 1) falling = true;
    const g = t - ts; if (g > 0 && g < 0.45) sq = Math.max(sq, Math.sin(Math.PI * g / 0.45) * Math.exp(-g * 3)); void k; });
  const cur = Math.min(n - 1, Math.round(pos)), carY = 60 + pos * FH, shaftH = (n - 1) * FH + 300;
  return <g key={'se' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-170} y={0} width={340} height={shaftH} rx={18} fill="#1B2440" stroke={OL} strokeWidth={6} />
    {[-1, 1].map((d) => <rect key={'rl' + d} x={d * 150 - 8} y={10} width={16} height={shaftH - 20} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}
    {floors.map((lab, k) => <g key={'fl' + k}>
      <path d={`M -170 ${60 + k * FH + 210} L 170 ${60 + k * FH + 210}`} stroke="#90A4AE" strokeWidth={6} />
      <rect x={-430} y={60 + k * FH + 60} width={230} height={70} rx={14} fill={k === cur ? '#FFE14D' : '#2A1658'} stroke={OL} strokeWidth={5} />
      <T x={-315} y={60 + k * FH + 108} s={36} c={k === cur ? OL : '#3DF5FF'}>{lab}</T>
      <path d={`M -200 ${60 + k * FH + 95} L -172 ${60 + k * FH + 95}`} stroke={OL} strokeWidth={5} /></g>)}
    <g transform="translate(0 -20)"><circle r={44} fill="#CFD8DC" stroke={OL} strokeWidth={6} />
      <g transform={`rotate(${pos * 400})`}>{[0, 1, 2].map((k) => <rect key={k} x={-36} y={-5} width={72} height={10} fill="#78909C" transform={`rotate(${k * 60})`} />)}</g></g>
    {[-30, 30].map((dx) => <path key={'cb' + dx} d={`M ${dx} 20 L ${dx} ${carY}`} stroke="#90A4AE" strokeWidth={4} />)}
    <g transform={`translate(0 ${carY + 200}) scale(${1 + sq * 0.12} ${1 - sq * 0.16}) translate(0 -200)`}>
      <rect x={-120} y={0} width={240} height={200} rx={16} fill="#FFC93C" stroke={OL} strokeWidth={6} />
      <rect x={-90} y={14} width={180} height={50} rx={8} fill="#1A0A0A" stroke={OL} strokeWidth={4} />
      <T x={0} y={52} s={34} c="#FF5252">{floors[cur]}</T>
      <rect x={-90} y={76} width={180} height={110} rx={10} fill="#FFF3C4" stroke={OL} strokeWidth={4} />
      <g transform="translate(0 186) scale(0.55)">
        <rect x={-75} y={-150} width={150} height={150} rx={24} fill="#2EC4B6" stroke={OL} strokeWidth={6} />
        {[-1, 1].map((d) => <g key={'ey' + d}><ellipse cx={d * 28} cy={-90} rx={20} ry={26} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={d * 28} cy={falling ? -100 : -86} r={7} fill={OL} /></g>)}
        <ellipse cx={0} cy={-40} rx={falling ? 18 : 12} ry={falling ? 22 : 8} fill="#3B0A1A" stroke={OL} strokeWidth={4} /></g>
      <path d="M -120 100 L 120 100" stroke={OL} strokeWidth={3} opacity={0.3} />
      {falling && [0, 1, 2, 3].map((k) => <path key={'sp' + k} d={`M ${k % 2 ? 128 : -128} ${20 + k * 30} l ${k % 2 ? 26 : -26} ${-18 - 10 * Math.sin(t * 40 + k)}`} stroke={K.gold} strokeWidth={6} strokeLinecap="round" />)}
      {falling && [0, 1, 2].map((k) => <path key={'ml' + k} d={`M ${-70 + k * 70} ${-20 - k * 6} l 0 -60`} stroke="#FFFFFF" strokeWidth={5} opacity={0.6} strokeLinecap="round" />)}
    </g>
    <path d={`M 230 ${carY + 70} l 30 0 l -15 26 Z`} fill={Math.sin(t * 8) > 0 ? '#FF5252' : '#7F0000'} stroke={OL} strokeWidth={3} />
    {a.text && <T x={0} y={shaftH + 60} s={36} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** DETECTIVE (original, generic design; never a real person): a trench-coat investigator with a wide-brim hat and a
 *  magnifying glass. Walks when `x` keyframes move (bobbing, legs swinging). `searchAt`: sweeps the lens left/right with
 *  a giant magnified eye. `findAt`: a "!" pops above the hat. `text`: caption. */
const detective: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const vx = kf(a.x, t + 0.05, 960) - kf(a.x, t - 0.05, 960), walk = Math.abs(vx) > 0.5, dir = vx < -0.5 ? -1 : (a.flip ? -1 : 1);
  const bob = walk ? Math.abs(Math.sin(t * 9)) * 10 : 2 * Math.sin(t * 2), leg = walk ? Math.sin(t * 9) * 22 : 0;
  const search = a.searchAt !== undefined && t >= a.searchAt, lensA = search ? Math.sin(t * 2.6) * 22 : -8, found = a.findAt !== undefined && t >= a.findAt;
  const skin = K.skin[a.skin ?? 3];
  return <g key={'dt' + i} transform={`translate(${x} ${y}) scale(${s * dir} ${s})`}>
    <ellipse cx={0} cy={4} rx={90} ry={12} fill="#000000" opacity={0.25} />
    <g transform={`translate(0 ${-bob})`}>
      {[-1, 1].map((d) => <g key={'lg' + d} transform={`rotate(${d * leg} ${d * 22} -110)`}>
        <rect x={d * 22 - 12} y={-110} width={24} height={100} rx={10} fill="#37474F" stroke={OL} strokeWidth={4} />
        <ellipse cx={d * 22 + 14} cy={-6} rx={30} ry={14} fill="#3E2723" stroke={OL} strokeWidth={4} /></g>)}
      <path d="M -70 -110 L -52 -330 Q 0 -350 52 -330 L 74 -110 Q 0 -96 -70 -110 Z" fill="#C9A66B" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <path d="M 0 -340 L 0 -112" stroke={OL} strokeWidth={4} opacity={0.5} />
      <rect x={-62} y={-232} width={128} height={18} fill="#8D6E3F" stroke={OL} strokeWidth={4} />
      <rect x={-10} y={-236} width={22} height={26} rx={4} fill="#FFD54F" stroke={OL} strokeWidth={3} />
      {[-300, -270, -180].map((by) => <circle key={by} cx={18} cy={by} r={5} fill={OL} />)}
      <path d="M -54 -336 L -10 -296 L -6 -350 Z M 54 -336 L 10 -296 L 6 -350 Z" fill="#B8925A" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <path d="M -50 -310 Q -84 -250 -60 -200" fill="none" stroke="#B8925A" strokeWidth={26} strokeLinecap="round" />
      <path d="M -50 -310 Q -84 -250 -60 -200" fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" opacity={0.6} />
      <g transform={`rotate(${lensA} 46 -300)`}>
        <path d="M 46 -300 L 130 -300" stroke="#B8925A" strokeWidth={26} strokeLinecap="round" />
        <circle cx={140} cy={-300} r={16} fill={skin} stroke={OL} strokeWidth={4} />
        <path d="M 150 -300 L 186 -300" stroke="#5D4037" strokeWidth={14} strokeLinecap="round" />
        <circle cx={232} cy={-300} r={50} fill="#B3E5FC" opacity={0.55} stroke={OL} strokeWidth={8} />
        {search && <g><ellipse cx={232} cy={-300} rx={30} ry={22} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><circle cx={236 + 6 * Math.sin(t * 5)} cy={-300} r={12} fill={OL} /></g>}
        <path d="M 208 -324 Q 220 -336 236 -334" stroke="#FFFFFF" strokeWidth={6} fill="none" strokeLinecap="round" /></g>
      <circle cx={8} cy={-388} r={44} fill={skin} stroke={OL} strokeWidth={5} />
      <circle cx={26} cy={-394} r={6} fill={OL} />
      <path d="M 14 -410 L 38 -414" stroke={OL} strokeWidth={5} strokeLinecap="round" />
      <path d="M 50 -380 q 10 6 0 12" fill="none" stroke={OL} strokeWidth={4} />
      <path d="M -40 -372 Q 8 -340 56 -372 L 56 -350 Q 8 -326 -40 -350 Z" fill="#B8925A" stroke={OL} strokeWidth={4} />
      <ellipse cx={8} cy={-420} rx={86} ry={16} fill="#4E5B4A" stroke={OL} strokeWidth={5} />
      <path d="M -36 -424 L -30 -486 Q 8 -508 46 -486 L 52 -424 Z" fill="#5E6B58" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-34} y={-446} width={84} height={14} fill="#2E3A2C" />
      {found && <g transform={`translate(10 ${-560 - 10 * Math.abs(Math.sin(t * 6))}) scale(${pop(t, a.findAt, 0.4)})`}>
        <circle r={40} fill="#FFE14D" stroke={OL} strokeWidth={5} /><T x={0} y={20} s={56}>!</T></g>}
    </g>
    {a.text && <g transform={`scale(${dir} 1)`}><T x={0} y={60} s={32} c={a.textc || K.white}>{a.text}</T></g>}
  </g>;
};

/** EMPTY CHAIR (original design): a tall executive chair, nobody in it, slowly swivelling under a spotlight. From
 *  `memoAt`, a memo flutters down from above and lands on the seat (`memo`: its title). `text`: caption. */
const emptychair: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const sw = 0.82 + 0.18 * Math.cos(t * 0.8), m = a.memoAt !== undefined ? clamp((t - a.memoAt) / 2.4) : -1;
  const mx = m >= 0 ? 160 * Math.sin(m * Math.PI * 3) * (1 - m) : 0, my = m >= 0 ? -900 + 700 * E.out(m) : 0, mr = m >= 0 ? 25 * Math.sin(m * Math.PI * 4) * (1 - m) : 0;
  return <g key={'ec' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -60 -900 L 60 -900 L 300 0 L -300 0 Z" fill="#FFF59D" opacity={0.12} />
    <ellipse cx={0} cy={0} rx={240} ry={28} fill="#FFF59D" opacity={0.25} />
    <g transform={`scale(${sw} 1)`}>
      {Array.from({length: 5}, (_, k) => { const ang = k * 72 + t * 20;
        return <g key={'lg' + k}><path d={`M 0 -20 L ${150 * Math.cos(ang * Math.PI / 180)} ${-6 + 16 * Math.sin(ang * Math.PI / 180)}`} stroke="#90A4AE" strokeWidth={14} strokeLinecap="round" />
          <circle cx={150 * Math.cos(ang * Math.PI / 180)} cy={6 + 16 * Math.sin(ang * Math.PI / 180)} r={14} fill="#263238" stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={-14} y={-150} width={28} height={130} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      <rect x={-170} y={-200} width={340} height={60} rx={26} fill="#3E2723" stroke={OL} strokeWidth={6} />
      <path d="M -150 -200 L -170 -560 Q 0 -640 170 -560 L 150 -200 Z" fill="#4E342E" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      {Array.from({length: 9}, (_, k) => <circle key={'tf' + k} cx={-90 + (k % 3) * 90} cy={-500 + Math.floor(k / 3) * 100} r={9} fill="#2B1B17" />)}
      {[-1, 1].map((d) => <rect key={'ar' + d} x={d > 0 ? 160 : -200} y={-300} width={40} height={110} rx={16} fill="#3E2723" stroke={OL} strokeWidth={5} />)}
      <path d="M -120 -590 Q 0 -630 100 -585" stroke="#FFFFFF" strokeWidth={8} opacity={0.25} fill="none" strokeLinecap="round" />
    </g>
    {m >= 0 && <g transform={`translate(${mx} ${my - 230}) rotate(${mr})`}>
      <rect x={-90} y={-60} width={180} height={120} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      <T x={0} y={-22} s={26}>{a.memo || 'MEMO'}</T>
      {[0, 1, 2].map((k) => <rect key={k} x={-64} y={-4 + k * 18} width={128 - k * 24} height={6} rx={3} fill="#B0BEC5" />)}</g>}
    {a.text && <T x={0} y={80} s={34} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/** FREIGHTER (original design): a chunky cartoon cargo boat bobbing on the waves, stacked crates with stencilled
 *  `labels`, a puffing funnel. Moves with `x` keyframes; `stopAt`: it brakes (wake stops) and a "?" pops over it. */
const freighter: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 210), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const labels: string[] = a.labels || ['CARGO'], moving = Math.abs(kf(a.x, t + 0.05, 960) - kf(a.x, t - 0.05, 960)) > 0.5;
  const rock = 4 * Math.sin(t * 1.9 + i), bob = 8 * Math.sin(t * 2.1 + i), q = a.stopAt !== undefined && t >= a.stopAt;
  const cc = ['#E53935', '#1E88E5', '#FFB300', '#43A047', '#8E24AA', '#00ACC1'];
  return <g key={'fr' + i} transform={`translate(${x} ${y + bob}) scale(${s * (a.flip ? -1 : 1)} ${s}) rotate(${rock})`}>
    {moving && [0, 1, 2].map((k) => <path key={'wk' + k} d={`M ${-300 - k * 60 - ((t * 120) % 60)} ${40 + k * 8} q 30 -12 60 0`} fill="none" stroke="#FFFFFF" strokeWidth={5} opacity={0.6 - k * 0.15} />)}
    <path d="M -290 -20 L 300 -20 L 250 70 L -250 70 Z" fill="#37474F" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <rect x={-290} y={-34} width={590} height={18} fill="#ECEFF1" stroke={OL} strokeWidth={4} />
    <path d="M -250 50 L 250 50" stroke="#E53935" strokeWidth={10} />
    {Array.from({length: 6}, (_, k) => { const r = k < 4 ? 0 : 1, c2 = k < 4 ? k : k - 4;
      return <g key={'cr' + k} transform={`translate(${-230 + c2 * 104 + r * 52} ${-110 - r * 76})`}>
        <rect x={0} y={0} width={100} height={76} rx={4} fill={cc[k % cc.length]} stroke={OL} strokeWidth={4} />
        {[1, 2, 3].map((v) => <path key={v} d={`M ${v * 25} 6 L ${v * 25} 70`} stroke={OL} strokeWidth={2} opacity={0.3} />)}
        <T x={50} y={46} s={labels[k % labels.length].length > 7 ? 15 : 20} c="#FFFFFF">{labels[k % labels.length]}</T></g>; })}
    <rect x={190} y={-150} width={90} height={116} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
    {[0, 1].map((k) => <rect key={'wd' + k} x={202 + k * 38} y={-136} width={28} height={24} rx={4} fill="#81D4FA" stroke={OL} strokeWidth={3} />)}
    <rect x={214} y={-220} width={40} height={70} fill="#E53935" stroke={OL} strokeWidth={5} />
    {[0, 1, 2].map((k) => { const g = ((t * 0.8 + k / 3) % 1); return <circle key={'pf' + k} cx={234 - 40 * g} cy={-240 - 140 * g} r={16 + 26 * g} fill="#ECEFF1" opacity={0.8 * (1 - g)} stroke={OL} strokeWidth={3} />; })}
    {q && <g transform={`translate(0 ${-330 - 8 * Math.abs(Math.sin(t * 5))}) scale(${pop(t, a.stopAt, 0.4)})`}><circle r={46} fill="#FFE14D" stroke={OL} strokeWidth={5} /><T x={0} y={22} s={62}>?</T></g>}
    {a.text && <T x={0} y={130} s={34} c={a.textc || K.white}>{a.text}</T>}
  </g>;
};

/* ------------------------------------------------------------------ BEFORE YOU BUY series kit (original designs) */
/** PRICED-IN CALCULATOR (series method, docs/series/BEFORE_YOU_BUY.md): an optional `lenses` strip of three values
 *  [{label, value, at}] (P/E, FCF yield, OCF yield / capex lens) above the dial, and a `base` label naming the cash base the
 *  gauge uses (FCF / OCF minus depreciation proxy / revenue scenario). A retro-futurist contraption with a half-dial from 0 to `max` (% a year). Two needles swing in:
 *  `low` {label, value, at} and `high` {label, value, at}; a shaded band marks the range between them. An inputs placard
 *  (`inputs`: lines) hangs beside it, `title` on top, `note` under the dial (e.g. "OUR ILLUSTRATION"). Lights blink,
 *  a crank turns while the needles move. */
const pricedin: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 520), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const max = a.max ?? 25, R = 260, lo = a.low || {value: 0}, hi = a.high || {value: 0};
  const ang = (v: number) => -90 + 180 * clamp(v / max);
  const needle = (n: any, k: number) => { const u = n.at === undefined ? 1 : E.outBack(clamp((t - n.at) / 1.1)), v = lerp(0, n.value, u) + (u >= 1 ? 0.15 * Math.sin(t * 7 + k) : 0);
    const r = (ang(v) * Math.PI) / 180;
    return <g key={'nd' + k} opacity={n.at === undefined || t >= n.at ? 1 : 0}>
      <path d={`M 0 0 L ${Math.sin(r) * (R - 40)} ${-Math.cos(r) * (R - 40)}`} stroke={k ? '#FF4F6B' : '#3DF5FF'} strokeWidth={12} strokeLinecap="round" />
      <g transform={`translate(${Math.sin(r) * (R + 70 + k * 95)} ${-Math.cos(r) * (R + 70 + k * 95)})`}>
        <rect x={-110} y={-36} width={220} height={66} rx={14} fill={k ? '#FF4F6B' : '#3DF5FF'} stroke={OL} strokeWidth={5} />
        <T x={0} y={-6} s={22} c={OL}>{n.label || ''}</T><T x={0} y={22} s={26} c={OL}>{n.text || `≈ ${n.value}% / YR`}</T></g></g>; };
  const band = (() => { const a0 = (ang(lo.value) * Math.PI) / 180, a1 = (ang(hi.value) * Math.PI) / 180, show = (hi.at === undefined || t >= hi.at + 0.6) ? 1 : 0;
    return <path d={`M 0 0 L ${Math.sin(a0) * R} ${-Math.cos(a0) * R} A ${R} ${R} 0 0 1 ${Math.sin(a1) * R} ${-Math.cos(a1) * R} Z`} fill="#FFE14D" opacity={0.35 * show} />; })();
  const moving = [lo, hi].some((n) => n.at !== undefined && t >= n.at && t < n.at + 1.2);
  const inputs: string[] = a.inputs || [], lenses: {label: string; value: string; at?: number}[] = a.lenses || [];
  return <g key={'pin' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-360} y={-60} width={720} height={260} rx={40} fill="#7B61FF" stroke={OL} strokeWidth={8} />
    <rect x={-330} y={-40} width={660} height={36} rx={14} fill="#FFFFFF" opacity={0.18} />
    {[-1, 1].map((d) => <g key={'lt' + d}><circle cx={d * 300} cy={140} r={20} fill={Math.sin(t * 6 + d) > 0 ? '#7DFF8A' : '#2A4A30'} stroke={OL} strokeWidth={4} /></g>)}
    <g transform="translate(0 40)">
      <path d={`M ${-R - 30} 0 A ${R + 30} ${R + 30} 0 0 1 ${R + 30} 0 Z`} fill="#CFD8DC" stroke={OL} strokeWidth={8} />
      <path d={`M ${-R} 0 A ${R} ${R} 0 0 1 ${R} 0 Z`} fill="#FFF8E1" stroke={OL} strokeWidth={5} />
      {band}
      {Array.from({length: 6}, (_, k) => { const v = (max / 5) * k, r = (ang(v) * Math.PI) / 180;
        return <g key={'tk' + k}><path d={`M ${Math.sin(r) * (R - 26)} ${-Math.cos(r) * (R - 26)} L ${Math.sin(r) * R} ${-Math.cos(r) * R}`} stroke={OL} strokeWidth={5} />
          <T x={Math.sin(r) * (R - 58)} y={-Math.cos(r) * (R - 58) + 9} s={24} c={OL}>{`${Math.round(v)}%`}</T></g>; })}
      {needle(lo, 0)}{needle(hi, 1)}
      <circle r={30} fill="#37474F" stroke={OL} strokeWidth={6} />
    </g>
    <g transform={`translate(${R + 40} 150) rotate(${moving ? t * 400 : 0})`}><path d="M 0 0 L 60 0" stroke={OL} strokeWidth={10} strokeLinecap="round" /><circle cx={60} cy={0} r={14} fill="#FF9F1C" stroke={OL} strokeWidth={4} /></g>
    {a.title && <T x={0} y={-R - 150} s={40} c="#FFF8E1">{a.title}</T>}
    {a.base && <g transform="translate(0 120)"><rect x={-230} y={-26} width={460} height={44} rx={22} fill="#FFE14D" stroke={OL} strokeWidth={4} />
      <T x={0} y={6} s={22} c={OL}>{`BASE: ${a.base}`}</T></g>}
    {a.note && <T x={0} y={180} s={24} c="#FFF8E1" w={800}>{a.note}</T>}
    {lenses.length > 0 && <g transform={`translate(0 ${a.lensY ?? -R - 270})`}>
      {lenses.map((l, k) => { const n = lenses.length, lx = (k - (n - 1) / 2) * 300, u = l.at === undefined ? 1 : E.outBack(clamp((t - l.at) / 0.5));
        return u > 0 && <g key={'ln' + k} transform={`translate(${lx} 0) scale(${u}) rotate(${1.5 * Math.sin(t * 1.4 + k)})`}>
          <rect x={-135} y={-52} width={270} height={98} rx={18} fill="#120A2A" stroke={['#3DF5FF', '#7DFF8A', '#FF9F1C'][k % 3]} strokeWidth={5} />
          <T x={0} y={-18} s={19} c="#C9B8F0" w={800}>{l.label}</T>
          <T x={0} y={28} s={36} c={['#3DF5FF', '#7DFF8A', '#FF9F1C'][k % 3]}>{l.value}</T></g>; })}</g>}
    {inputs.length > 0 && <g transform={`translate(${a.placardX ?? 560} ${a.placardY ?? -220}) rotate(${2 * Math.sin(t * 1.1)})`}>
      <path d="M 0 -60 L 0 -20" stroke={OL} strokeWidth={4} />
      <rect x={-200} y={-20} width={400} height={inputs.length * 40 + 60} rx={14} fill="#FFF8E1" stroke={OL} strokeWidth={5} />
      <T x={0} y={18} s={22} c="#7B61FF">INPUTS (ON SCREEN)</T>
      {inputs.map((ln, k) => <T key={k} x={-180} y={58 + k * 40} s={21} c={OL} w={800} a="start">{ln}</T>)}</g>}
  </g>;
};

/** RISK SCALE: a big balance; RISKS on the left pan, UPSIDE on the right. `risks` / `upside`: [{text, at}] blocks that drop
 *  in (squash on landing); the beam tilts toward the heavier side as blocks land. `title` above. */
const riskscale: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const L: {text: string; at: number}[] = a.risks || [], Rr: {text: string; at: number}[] = a.upside || [];
  const landed = (b: {at: number}) => clamp((t - b.at) / 0.6);
  const wl = L.reduce((q, b) => q + landed(b), 0), wr = Rr.reduce((q, b) => q + landed(b), 0);
  const tilt = clamp((wr - wl) * 6, -14, 14) + 1.2 * Math.sin(t * 2.2), rad = (tilt * Math.PI) / 180, arm = 420;
  const pan = (side: number, list: {text: string; at: number}[], label: string, c: string) => {
    const px = side * arm * Math.cos(rad), py = side * arm * Math.sin(rad);
    return <g transform={`translate(${px} ${py})`}>
      <path d="M 0 0 L -150 220 M 0 0 L 150 220" stroke={OL} strokeWidth={4} />
      <path d="M -190 220 L 190 220 Q 170 270 0 272 Q -170 270 -190 220 Z" fill={c} stroke={OL} strokeWidth={6} />
      <T x={0} y={254} s={26} c={OL}>{label}</T>
      {list.map((b, k) => { const u = landed(b); if (t < b.at - 0.01) return null;
        const drop = (1 - E.out(u)) * -500, sq = u >= 1 ? 1 : 1 + 0.15 * Math.sin(u * Math.PI);
        return <g key={k} transform={`translate(0 ${200 - k * 62 + drop}) scale(${1 / sq} ${sq})`}>
          <rect x={-175} y={-56} width={350} height={54} rx={12} fill="#FFF8E1" stroke={OL} strokeWidth={4} />
          <T x={0} y={-20} s={b.text.length > 24 ? 18 : 22} c={OL}>{b.text}</T></g>; })}
    </g>; };
  return <g key={'rs' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -60 560 L 60 560 L 24 40 L -24 40 Z" fill="#B0BEC5" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
    <rect x={-160} y={550} width={320} height={40} rx={14} fill="#78909C" stroke={OL} strokeWidth={6} />
    <g transform={`rotate(${tilt})`}><rect x={-arm - 20} y={-14} width={arm * 2 + 40} height={28} rx={14} fill="#FFE14D" stroke={OL} strokeWidth={6} /></g>
    {pan(-1, L, a.leftLabel || 'RISKS', '#FF8A80')}{pan(1, Rr, a.rightLabel || 'UPSIDE', '#B9F6CA')}
    <circle r={26} fill="#FF4FD8" stroke={OL} strokeWidth={6} />
    {a.title && <T x={0} y={-80} s={42} c="#FFF8E1">{a.title}</T>}
  </g>;
};

/** EDITION STAMP: a red rubber stamp that slams in at `at` (overshoot + ink splat), double border, `text` (1-2 lines via
 *  `sub`). Used at the hook, the priced-in section and the end card so every edition is dated on screen. */
const editionstamp: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 160), at = a.at ?? 0;
  if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const u = clamp((t - at) / 0.35), sc = (a.scale ?? 1) * (u < 1 ? lerp(2.4, 1, E.in(u)) : 1 + 0.04 * Math.exp(-(t - at - 0.35) * 8) * Math.sin((t - at) * 40));
  const txt: string = a.text || 'DATA AS OF', sub: string | undefined = a.sub, c = a.color || '#FF6B81';
  const w = Math.max(txt.length * 21, (sub || '').length * 16) + 80, h = sub ? 112 : 76, o = a.until !== undefined ? 1 - win(t, a.until, 0.4) : 1;
  return <g key={'es' + i} opacity={o * (u < 1 ? 0.6 + 0.4 * u : 0.92)} transform={`translate(${x} ${y}) rotate(${a.rot ?? -6}) scale(${sc})`}>
    {u >= 1 && [0, 1, 2, 3, 4].map((k) => <circle key={k} cx={(rnd(k + i) - 0.5) * w} cy={(rnd(k + 9) - 0.5) * h * 1.4} r={4 + 6 * rnd(k + 3)} fill={c} opacity={0.35} />)}
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={10} fill="#120A2A" fillOpacity={0.78} stroke={c} strokeWidth={7} />
    <rect x={-w / 2 + 10} y={-h / 2 + 10} width={w - 20} height={h - 20} rx={6} fill="none" stroke={c} strokeWidth={3} />
    <T x={0} y={sub ? -8 : 12} s={34} c={c}>{txt}</T>
    {sub && <T x={0} y={34} s={26} c={c} w={800}>{sub}</T>}
  </g>;
};

/** SCORECARD: the end card of each edition: a retro-futurist scoreboard with `title` and up to 3 `rows`
 *  [{label, value, at}] that flip in (split-flap), plus an edition line `stamp` at the bottom. */
const scorecard: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 260), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.6);
  if (s <= 0 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const rows: {label: string; value: string; at?: number}[] = a.rows || [], W = 1100, RH = 130;
  return <g key={'sc' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d={`M ${-W / 2 - 40} -90 L ${W / 2 + 40} -90 L ${W / 2 + 20} ${rows.length * RH + 120} L ${-W / 2 - 20} ${rows.length * RH + 120} Z`} fill="#24154F" stroke={OL} strokeWidth={8} strokeLinejoin="round" />
    {[-1, 1].map((d) => <circle key={d} cx={d * (W / 2 + 10)} cy={-60} r={16} fill={Math.sin(t * 5 + d) > 0 ? '#FFE14D' : '#5A4A10'} stroke={OL} strokeWidth={4} />)}
    <T x={0} y={-34} s={40} c="#FFE14D">{a.title || '3 NUMBERS TO WATCH'}</T>
    {rows.map((r, k) => { const at = r.at ?? 0, u = clamp((t - at) / 0.5), flip = Math.abs(Math.cos(u * Math.PI * 2)), shown = t >= at;
      return <g key={k} transform={`translate(0 ${20 + k * RH})`}>
        <rect x={-W / 2} y={0} width={W} height={RH - 20} rx={16} fill="#120A2A" stroke="#3DF5FF" strokeWidth={4} />
        <circle cx={-W / 2 + 56} cy={(RH - 20) / 2} r={34} fill="#FF4FD8" stroke={OL} strokeWidth={4} />
        <T x={-W / 2 + 56} y={(RH - 20) / 2 + 12} s={34} c={OL}>{String(k + 1)}</T>
        {shown && <g transform={`translate(0 ${(RH - 20) / 2}) scale(1 ${u < 1 ? flip : 1}) translate(0 ${-(RH - 20) / 2})`}>
          <T x={-W / 2 + 120} y={46} s={30} c="#FFF8E1" a="start">{r.label}</T>
          <T x={-W / 2 + 120} y={88} s={26} c="#3DF5FF" w={800} a="start">{r.value}</T></g>}
      </g>; })}
    {a.stamp && <T x={0} y={rows.length * RH + 80} s={22} c="#C9B8F0" w={800}>{a.stamp}</T>}
  </g>;
};

const ITEMS: Record<string, ItemFn> = {person, dog, tower, building, board, chart, paper, press, docs, contract, coins, vaultdoor, piggy, magnifier,
  plane, sign, gavel, calendar, storm, chair, desk, terminal, letters, arrow: bigArrow, ticker, burst,
  wafer, litho, pod, arm, conveyor, device, domino, crane, stack, browser, counter, clock, ship, passport, tinsource, mirrors, bus, barrier, rig, racecar, watch, shares, ramstick, pricetag, hbm, imprint, beamsrc, megafab, satellite, osat, vessel, bigphone, pcgrid, wireform, bankisle, balance, gem, tradescreen, burger, restaurant, queue, oiltank, barrel, bigchart, pinboard, isodc, medbill, pills, creditcard, tollbooth, home, zonemap, cart, pallet, diploma, gradcaps, sedan, meter, bumper, van, flowscreens, netmesh, eggcarton, bars, bigcoin, statement, ivbag, yesno, bigcheck, bench, glassbox, rocket, constellation, chipbuddy, stockelevator, detective, emptychair, freighter, pricedin, riskscale, editionstamp, scorecard};
const BACK = new Set(['restaurant', 'rig', 'tower', 'building', 'board', 'chart', 'vaultdoor', 'desk', 'press', 'chair', 'calendar', 'storm', 'ticker', 'litho', 'imprint', 'megafab', 'crane', 'arm', 'shares']);

/* =============================================================================================== STAGE */
export const CartoonStage: React.FC<CartoonStageProps> = (p) => {
  const {t, W = 1920, H = 1080, worldW = 1920, floor = 860, items = [], callouts = []} = p;
  const zones: StageZone[] = p.zones?.length ? p.zones : [{set: p.world || 'hills', x0: -1600, x1: worldW + 1600, night: p.night}];
  const cams = p.cam?.length ? p.cam : [{at: 0, x: 960, y: 540, zoom: 1}];
  let cx = cams[0].x ?? 960, cy = cams[0].y ?? 540, cz = cams[0].zoom ?? 1;
  for (const k of cams.slice(1)) { const u = ease(t, k.at, k.dur ?? 2.2, E.inOutQuint); cx = lerp(cx, k.x ?? cx, u); cy = lerp(cy, k.y ?? cy, u); cz = lerp(cz, k.zoom ?? cz, u); }
  cx += (p.drift ?? 6) * t;
  cz *= 1 + 0.004 * t;                                                        // gentle push so nothing ever sits still
  let sx = 0, sy = 0;
  for (const s of p.shake || []) { const u = win(t, s.at, s.dur ?? 1.2); if (u > 0 && u < 1) { const a = (s.amp ?? 14) * (1 - u); sx += Math.sin(t * 61) * a; sy += Math.cos(t * 47) * a; } }
  const camT = `translate(${W / 2 + sx} ${H / 2 + sy}) scale(${cz}) translate(${-cx} ${-cy})`;
  const night = p.night || zones.every((z) => z.night);
  const ctx: Ctx = {t, f: floor};

  const calloutNode = (c: StageCallout, i: number) => {
    if (t < c.at || (c.until !== undefined && t > c.until + 0.4)) return null;
    const u = E.outBack(win(t, c.at, 0.45)), o = c.until !== undefined ? 1 - win(t, c.until, 0.4) : 1;
    const size = c.size ?? 34, w = Math.max(c.text.length * size * 0.6, (c.sub || '').length * 13) + 60, h = c.sub ? size + 56 : size + 34;
    const cc = c.color === 'risk' ? K.red : c.color === 'gold' ? K.gold : c.color === 'green' ? K.green2 : K.white;
    return <g key={'co' + i} opacity={o} transform={`translate(${c.x} ${c.y}) scale(${u}) rotate(${Math.sin(t * 1.5 + i) * 1.2})`}>
      {c.tail && <path d={`M -16 ${h / 2 - 4} L ${c.tail[0] - c.x} ${c.tail[1] - c.y} L 16 ${h / 2 - 4} Z`} fill={cc} stroke={OL} strokeWidth={4} strokeLinejoin="round" />}
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.4} fill={cc} stroke={OL} strokeWidth={5} />
      <T x={0} y={c.sub ? -4 : size * 0.36} s={size}>{c.text}</T>
      {c.sub && <T x={0} y={size * 0.36 + 20} s={20} w={700} o={0.8}>{c.sub}</T>}
    </g>;
  };
  const render = (list: StageItem[], off: number) => list.map((a, k) => { const fn = ITEMS[a.kind]; return fn ? <React.Fragment key={off + k}>{fn(a, ctx, off + k)}</React.Fragment> : null; });
  const tn = toneAt(p.tone, p.toneShift, t), graded = !isNeutral(tn);
  const sky = night ? tn.nightSky : tn.sky;
  const ban = p.banner, bu = ban ? E.outBack(win(t, ban.at ?? 0.3, 0.6)) : 0;
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <defs><linearGradient id="stgsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={sky[0]} /><stop offset="100%" stopColor={sky[1]} /></linearGradient>
        {graded && <ToneFilterDef id="stgtone" s={tn} />}</defs>
      <rect width={W} height={H} fill={sky[0]} />
      <g transform={camT}>
        <rect x={-4000} y={-3000} width={worldW + 8000} height={3000 + floor} fill="url(#stgsky)" />
        <g filter={graded ? 'url(#stgtone)' : undefined}>
        {night ? <g transform={`translate(${cx * 0.9} 0)`}>
          {tn.stars && Array.from({length: 40}, (_, k) => <circle key={k} cx={(rnd(k) - 0.5) * 2600} cy={-200 + rnd(k + 7) * 600} r={2 + 2 * rnd(k + 3)} fill={K.white} opacity={0.5 + 0.5 * Math.sin(t * 3 + k)} />)}
          {tn.sun !== 'none' && <g><circle cx={560} cy={210} r={60} fill="#FFF3B0" stroke={OL} strokeWidth={5} /><circle cx={585} cy={195} r={52} fill={sky[0]} /></g>}</g>
          : tn.sun !== 'none' && <g transform={`translate(${cx + 560} 0)`}>
            <circle cx={0} cy={220 + Math.sin(t * 0.8) * 8 * tn.bounce} r={66} fill={K.sun} stroke={OL} strokeWidth={5} />
            {tn.sun === 'face' && <g><circle cx={-20} cy={210} r={6} fill={OL} /><circle cx={20} cy={210} r={6} fill={OL} />
            <path d="M -22 236 Q 0 254 22 236" fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" /></g>}</g>}
        {tn.clouds !== 'none' && <g transform={`translate(${cx * 0.6} 0)`}>
          {[0, 1, 2, 3].map((i) => { const x = ((i * 700 + t * 18) % 3400) - 1700, y = 90 + (i % 2) * 70;
            return <path key={i} transform={`translate(${x} ${y})`} d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill={night ? '#5A6A9A' : tn.clouds === 'grey' ? '#8C93A6' : K.white} stroke={OL} strokeWidth={4} />; })}
        </g>}
        {zones.map((z, k) => { const fn = SETS[z.set] || SETS.hills;
          return <g key={'z' + k}>
            <clipPath id={`zc${k}`}><rect x={z.x0} y={INDOOR.has(z.set) ? -3000 : -3000} width={z.x1 - z.x0} height={6000} /></clipPath>
            <g clipPath={`url(#zc${k})`}>{fn(t, z, floor)}</g>
            {k > 0 && <rect x={z.x0 - 8} y={-3000} width={16} height={6000} fill={OL} opacity={INDOOR.has(z.set) || INDOOR.has(zones[k - 1].set) ? 1 : 0} />}
          </g>; })}
        {render(items.filter((a) => BACK.has(a.kind)), 0)}
        {render(items.filter((a) => !BACK.has(a.kind)), 500)}
        </g>
        {callouts.filter((c) => !c.screen).map(calloutNode)}
      </g>
      <ToneOverlay s={tn} t={t} W={W} H={H} id="stgtn" spotX={p.spot?.[0]} spotY={p.spot?.[1]} />
      {callouts.filter((c) => c.screen).map((c, i) => calloutNode(c, 100 + i))}
      {ban && bu > 0 && <g transform={`translate(120 96) scale(${bu})`}>
        <rect x={0} y={0} width={Math.max(ban.text.length * 27, (ban.sub || '').length * 13) + 60} height={ban.sub ? 100 : 70} rx={18} fill={K.white} stroke={OL} strokeWidth={5} />
        <T x={30} y={48} s={44} a="start">{ban.text}</T>
        {ban.sub && <T x={32} y={82} s={22} a="start" w={700} o={0.75}>{ban.sub}</T>}
      </g>}
    </svg>
  );
};
