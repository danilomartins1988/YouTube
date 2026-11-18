import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * POWERMAP kit for CartoonStage (Episode 67, "Could Cheap Electricity Become the New Oil?").
 *
 * A sunny, travelling world drawn in the channel's prime-time cartoon GENRE (thick clean outlines, flat colour, squash and stretch):
 * a site scout (NIA, fictional, drawn with the shared `toon` rig) flies from pin to pin looking for a home for a giant AI campus,
 * with CUBBY, the walking scale model of that campus. Everything ORIGINAL: no logos, no flags, no brand names on buildings, no traced
 * plants; companies appear only as generic buildings with plain plaques when the narration names them. No real person is drawn.
 * Countries are drawn as landscapes (fjords, geothermal steam, rivers, plains, dunes), never as flags or stereotypes.
 * Sets:
 *  - pmoffice: the client's day-lit office: skyline window, desk + laptop, a wall screen (`screen` [[t, text]]), a whiteboard
 *    checklist (`list` [text...], `shown` KF 0..n rows revealed, `ticks` [[t, n]] rows ticked).
 *  - pmmap: a cork pin-board world map (stylized original continents): `pins` [{x, y, label, at, c}], Nia's little plane flies
 *    between pins with `fly` [[t, pinIndex]] (1.6 s hops), `hi` [[t, pinIndex]] pulses a pin, `title` card, `strings` draws the route.
 *  - pmoil: split world. Left: a 20th-century oil port (pumpjacks nod with `pump` KF, tanks, a tanker that crosses with `ship`
 *    KF 0..1). Right: a dam whose power line runs to the shore (`wire` KF 0..1) and stops in a dangling plug with sparks (`stopAt`).
 *    `focus` 'oil' | 'power' | 'both' dims the other half.
 *  - pmsmelter: a fjord smelter: dam with spillway, pylons, a long potline hall with glowing vents, power pulses (`flow` KF 0..1),
 *    an ore ship docking (`ore` KF 0..1), ingots stacking (`ingots` KF 0..12), an ingot ship leaving (`out` KF 0..1), `plaque`.
 *  - pmnorth: a cold hydro/geothermal valley, `variant` 'fjord' | 'geo' | 'river': snowy peaks, dam (or steam vents for geo),
 *    data halls appearing with `halls` KF 0..4, cool-air arrows (`air` KF 0..1), snowfall (`snow`), a reservoir level `level`
 *    KF 0..1 (drops to show a dry year), a tenant board `tenant` [[t, text]], `plaque`.
 *  - pmsun: a sunny plain, `variant` 'texas' | 'gulf': solar rows that fill (`solar` KF 0..1), wind turbines (texas), a gas plant
 *    with a plume (`gas` KF 0..1), data halls (`halls` KF 0..5), ghost halls on the horizon for requests (`ghosts` KF 0..14),
 *    `night` KF 0..1 sunset to night, heat shimmer (`heat` KF), `plaque`.
 *  - pmtropic: a tropical river dam and coastal wind farm feeding a line, and a giant bill stack at right (`stack`
 *    [{label, v, color, at}] blocks rising, `stackTitle`), `tax` [[t, text]] stamp.
 *  - pmqueue: the line at the plug: a substation with a big socket, a queue of small data-center cubes (`n` KF 0..12) waiting,
 *    a wall calendar flipping (`flip` KF 0..1 speed), `plugAt` the first cube plugs in, `bring` KF 0..1 cubes carry batteries.
 *  - pmscore: Nia's clipboard scorecard: `rows` [{label, at, mark: 'yes' | 'no' | 'maybe'}], `title`.
 *  - pmtitle / pmbumper: the title card (a giant plug pumps like an oil derrick) and chapter bumpers (a plug slides into a
 *    socket and the panel lights up with the chapter title).
 * Items: pmtag (top-left claim pill, `tags` [[t, text]]), cubby (CUBBY: a walking server-cube with an LED face, little legs and a
 *  cable tail ending in a plug; `x` KF, `y`, `face` / `faces` [[t, face]] (happy | worry | wow | sleep), `hops` [t...],
 *  `plugged` t: glows, `carry` 'suitcase' | 'battery').
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#16223A';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; [k: string]: any};
type SetFn = (t: number, z: Z, f: number) => React.ReactNode;
type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const kf = (v: KF | undefined, t: number, d = 0): number => {
  if (v === undefined || v === null) return d;
  if (!Array.isArray(v)) return Number(v);
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], Math.max(0.001, v[i][0] - v[i - 1][0]))));
  return v[v.length - 1][1];
};
const pick = <V,>(tl: any, t: number, d: V): V => { let v = d; if (Array.isArray(tl)) for (const [pt, pv] of tl) if (t >= Number(pt)) v = pv; return v; };
const lastAt = (tl: any, t: number): number => { let v = -99; if (Array.isArray(tl)) for (const [pt] of tl) if (t >= Number(pt)) v = Number(pt); return v; };
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.6);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#1E88E5', GOLD = '#F5B700', RED = '#E5483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', PURPLE = '#7357C9', NAVY = '#16223A', ORANGE = '#F08A24',
  CY = '#29C5F6', OIL = '#3B2A20', SNOW = '#F4F8FC', WATER = '#5AB4E8', ROCK = '#8C9BAE';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'pmc' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const stamp = (x: number, y: number, txt: string, c = RED, s = 40, k: any = 0, sc = 1) => { const w = txt.length * s * 0.64 + 50;
  return <g key={'stp' + k} transform={`translate(${x} ${y}) rotate(-8) scale(${sc})`}><rect x={-w / 2} y={-s} width={w} height={s * 1.5} rx={8} fill="#FFFFFF" stroke={c} strokeWidth={7} opacity={0.95} />
    <T x={0} y={s * 0.32} s={s} c={c}>{txt}</T></g>; };
const ridge = (x0: number, x1: number, base: number, amp: number, per: number, seed: number) => {
  let d = `M ${x0} ${base + 400} L ${x0} ${base}`;
  for (let x = x0; x <= x1 + per; x += per / 2) d += ` L ${x} ${base - amp * (0.35 + 0.65 * rnd(seed + Math.round(x / per * 2)))}`;
  return d + ` L ${x1 + per} ${base + 400} Z`;
};
const bolt = (x: number, y: number, s: number, c = GOLD, k: any = 0) => <path key={'bl' + k} transform={`translate(${x} ${y}) scale(${s})`} d="M 10 -60 L -26 6 L -2 6 L -14 60 L 28 -10 L 4 -10 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />;
const pylon = (x: number, y: number, s: number, k: any) => <g key={'py' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -40 0 L -8 -300 L 8 -300 L 40 0 M -30 -80 L 30 -80 M -22 -160 L 22 -160 M -70 -240 L 70 -240 M -50 -200 L 50 -200 M -30 0 L 22 -160 M 30 0 L -22 -160" stroke="#5E6B85" strokeWidth={7} fill="none" strokeLinejoin="round" /></g>;
/** data hall block with roof fans */
const hall = (x: number, y: number, w: number, k: any, t: number, sc = 1, ghost = false) => <g key={'hl' + k} transform={`translate(${x} ${y}) scale(${sc})`} opacity={ghost ? 0.5 : 1}>
  <rect x={0} y={-150} width={w} height={150} fill={ghost ? 'none' : '#E7ECF3'} stroke={ghost ? PURPLE : OL} strokeWidth={5} strokeDasharray={ghost ? '16 10' : undefined} />
  {!ghost && Array.from({length: Math.floor(w / 70)}, (_, q) => <g key={q} transform={`translate(${35 + q * 70} -168)`}><rect x={-26} y={-12} width={52} height={20} fill="#B9C3D1" stroke={OL} strokeWidth={3} />
    <g transform={`rotate(${t * 400 + q * 40})`}><path d="M -16 0 L 16 0 M 0 -6 L 0 6" stroke={OL} strokeWidth={3} /></g></g>)}
  {!ghost && Array.from({length: Math.floor(w / 46)}, (_, q) => <rect key={'ld' + q} x={14 + q * 46} y={-110} width={22} height={60} fill="#263238" stroke={OL} strokeWidth={2} />)}
  {!ghost && Array.from({length: Math.floor(w / 46)}, (_, q) => <circle key={'lg' + q} cx={25 + q * 46} cy={-100 + 20 * ((q + Math.floor(t * 3)) % 3)} r={4} fill={(q + Math.floor(t * 4)) % 2 ? CY : GREEN} />)}
</g>;
const turbine = (x: number, y: number, s: number, k: any, t: number) => <g key={'wt' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -8 0 L -4 -300 L 4 -300 L 8 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />
  <g transform={`translate(0 -300) rotate(${t * 90 + k * 37})`}>{[0, 120, 240].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 L -10 -20 L 0 -150 L 10 -20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} strokeLinejoin="round" />)}
    <circle r={10} fill="#CFD8DC" stroke={OL} strokeWidth={4} /></g></g>;
const dam = (x: number, y: number, s: number, t: number, level = 1, k: any = 0) => <g key={'dm' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-420} y={-260 + 200 * (1 - level)} width={360} height={60 + 200 * level} fill={WATER} stroke={OL} strokeWidth={4} />
  <path d="M -60 -300 L 60 -300 L 140 0 L -60 0 Z" fill="#C9D1DC" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
  {[0, 1, 2].map((q) => <path key={q} d={`M ${-20 + q * 40} -260 L ${10 + q * 50} -10`} stroke="#AEB9C6" strokeWidth={5} />)}
  {level > 0.15 && Array.from({length: 6}, (_, q) => { const u = ((t * 1.6 + q / 6) % 1); return <path key={'sp' + q} d={`M ${60 + q * 6} ${-120 + u * 110} q 10 8 0 16`} stroke="#FFFFFF" strokeWidth={5} fill="none" opacity={1 - u} />; })}
  <rect x={140} y={-80} width={120} height={80} fill="#EDE7DB" stroke={OL} strokeWidth={5} />{bolt(200, -40, 0.4, GOLD, 'db' + k)}
</g>;
const ship = (x: number, y: number, s: number, k: any, cargo: 'oil' | 'ore' | 'ingot', t: number) => <g key={'sh' + k} transform={`translate(${x} ${y + 4 * Math.sin(t * 2 + String(k).length)}) scale(${s})`}>
  <path d="M -260 -40 L 260 -40 L 210 40 L -230 40 Z" fill={cargo === 'oil' ? '#7A2E2E' : cargo === 'ore' ? '#3E5A7A' : '#2E6B5A'} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
  <rect x={150} y={-120} width={80} height={80} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={165} y={-106} width={50} height={20} fill="#BFE6F7" stroke={OL} strokeWidth={3} />
  {cargo === 'oil' && [0, 1, 2].map((q) => <ellipse key={q} cx={-170 + q * 110} cy={-46} rx={46} ry={14} fill="#9E9E9E" stroke={OL} strokeWidth={4} />)}
  {cargo === 'ore' && <path d="M -220 -40 Q -120 -120 -20 -40 Q 40 -100 110 -40 Z" fill="#B5651D" stroke={OL} strokeWidth={4} />}
  {cargo === 'ingot' && Array.from({length: 6}, (_, q) => <path key={q} d={`M ${-220 + q * 60} -40 l 10 -28 h 34 l 10 28 Z`} fill="#CFD8DC" stroke={OL} strokeWidth={3} />)}
</g>;
const sea = (z: Z, f: number, t: number, c = '#4FA6DE') => <g><rect x={z.x0} y={f - 40} width={z.x1 - z.x0} height={700} fill={c} />
  {Array.from({length: 26}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 260 + ((t * 30) % 260)} ${f + 30 + (k % 3) * 60} q 30 -14 60 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.6} />)}</g>;
const ground = (z: Z, f: number, c = '#A6D08A', c2 = '#88B86C') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const pumpjack = (x: number, y: number, s: number, t: number, k: number, speed: number) => { const a = Math.sin(t * 2.2 * speed + k) * 14;
  return <g key={'pj' + k} transform={`translate(${x} ${y}) scale(${s})`}><path d="M -90 0 L -20 -150 L 40 0" stroke={OL} strokeWidth={8} fill="none" />
    <g transform={`translate(-20 -150) rotate(${a})`}><rect x={-120} y={-16} width={240} height={32} rx={6} fill={OIL} stroke={OL} strokeWidth={5} /><path d="M 120 -30 Q 160 0 120 40 Z" fill={OIL} stroke={OL} strokeWidth={5} />
      <path d="M 130 30 L 130 150" stroke={OL} strokeWidth={4} /></g><rect x={-130} y={-10} width={260} height={14} fill="#6D6458" stroke={OL} strokeWidth={4} /></g>; };
/** stylized original continents for the pin board (not traced) */
const LAND = ['M 230 230 Q 330 140 520 160 Q 640 190 600 300 Q 560 380 470 430 Q 420 470 380 440 Q 300 380 250 330 Q 200 280 230 230 Z',
  'M 600 520 Q 680 500 740 560 Q 760 660 700 760 Q 660 820 640 760 Q 610 660 600 520 Z',
  'M 960 200 Q 1060 160 1140 200 Q 1160 260 1100 300 Q 1040 320 990 300 Q 950 260 960 200 Z',
  'M 980 340 Q 1100 330 1160 400 Q 1180 500 1120 600 Q 1060 680 1020 600 Q 980 500 960 420 Z',
  'M 1160 200 Q 1400 140 1640 200 Q 1720 280 1640 360 Q 1520 420 1400 400 Q 1260 380 1180 320 Q 1140 260 1160 200 Z',
  'M 1560 600 Q 1660 580 1720 630 Q 1700 690 1620 700 Q 1560 680 1560 600 Z', 'M 860 220 Q 900 200 930 225 Q 915 250 875 245 Z', 'M 520 110 Q 600 70 660 110 Q 620 150 560 140 Z'];

const RAW: Record<string, SetFn> = {
  /** the client's day-lit office */
  pmoffice: (t, z, f) => {
    const list: string[] = z.list || ['CHEAP POWER', 'LOTS OF IT', 'READY SOON', 'COOL ENOUGH', 'CLOSE TO CUSTOMERS', 'A GOVERNMENT THAT SAYS YES'];
    const shown = kf(z.shown, t, 0), ticks = Number(pick(z.ticks, t, 0)), scr: string = pick(z.screen, t, '');
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EEF2F7" />
      <rect x={-200} y={80} width={980} height={560} fill="#9FD3F2" stroke={OL} strokeWidth={8} />
      {Array.from({length: 9}, (_, k) => { const h = 180 + rnd(k + 3) * 260; return <rect key={'sk' + k} x={-180 + k * 108} y={640 - h} width={90} height={h} fill={k % 2 ? '#C5D3E3' : '#B3C4D8'} stroke={OL} strokeWidth={3} />; })}
      {cloud(200 + ((t * 12) % 500), 170, 0.7, 1)}
      <path d="M 290 80 L 290 640 M -200 360 L 780 360" stroke={OL} strokeWidth={6} />
      {/* wall screen */}
      <g transform="translate(1340 300)"><rect x={-300} y={-170} width={600} height={340} rx={16} fill="#1F2A44" stroke={OL} strokeWidth={8} />
        {scr && <T x={0} y={14} s={fit(scr, 540, 52)} c={GOLD}>{scr}</T>}{scr && <path d="M -240 100 L 240 100" stroke={CY} strokeWidth={4} opacity={0.5 + 0.5 * Math.sin(t * 4)} />}</g>
      {/* whiteboard checklist */}
      <g transform="translate(1340 520)" opacity={shown > 0.01 ? 1 : 0}>
        <rect x={-330} y={0} width={660} height={300} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {list.map((ln, k) => { const u = clamp(shown - k); if (u <= 0) return null; return <g key={k} opacity={u}>
          <rect x={-300} y={22 + k * 45} width={30} height={30} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
          {k < ticks && <path d={`M -296 ${38 + k * 45} l 10 10 l 18 -22`} stroke={GREEN} strokeWidth={6} fill="none" strokeLinecap="round" />}
          <T x={-255} y={46 + k * 45} s={26} a="start" c={NAVY}>{ln}</T></g>; })}</g>
      {/* desk */}
      <rect x={-200} y={f - 160} width={1200} height={30} rx={8} fill="#B07A4A" stroke={OL} strokeWidth={6} />
      <path d={`M -150 ${f - 130} L -150 ${f} M 950 ${f - 130} L 950 ${f}`} stroke={OL} strokeWidth={10} />
      <g transform={`translate(600 ${f - 160})`}><path d="M -110 0 L -90 -120 L 110 -120 L 90 0 Z" fill="#37474F" stroke={OL} strokeWidth={5} />
        <rect x={-80} y={-110} width={160} height={96} fill={CY} opacity={0.35 + 0.1 * Math.sin(t * 5)} />{bolt(0, -62, 0.45, GOLD, 'lap')}</g>
      <g transform={`translate(200 ${f - 160})`}><path d="M -30 0 L -20 -60 L 20 -60 L 30 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} /><path d="M 30 -40 q 20 0 20 18 q 0 18 -20 18" stroke={OL} strokeWidth={4} fill="none" /></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C8B9A6" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#A89580" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the pin-board world map with Nia's little plane */
  pmmap: (t, z, f) => {
    const pins: any[] = z.pins || [];
    const P = (i: number) => (pins[i] ? [pins[i].x, pins[i].y] : [960, 540]);
    const fly = (z.fly || []) as [number, number][];
    let px = 960, py = 540, ang = 0, show = false;
    if (fly.length) { show = t >= fly[0][0]; let cur = P(fly[0][1]); px = cur[0]; py = cur[1];
      for (let k = 1; k < fly.length; k++) { const [t0, idx] = fly[k]; if (t < t0) break; const a = P(fly[k - 1][1]), b = P(idx), u = E.inOut(win(t, t0, 1.6));
        px = lerp(a[0], b[0], u); py = lerp(a[1], b[1], u) - Math.sin(u * Math.PI) * 120; ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 57.3 * (u < 1 ? 1 : 0); } }
    const hi = Number(pick(z.hi, t, -1)), hiAt = lastAt(z.hi, t);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#D7B98E" />
      {Array.from({length: 60}, (_, k) => <circle key={'ck' + k} cx={z.x0 + rnd(k) * (z.x1 - z.x0)} cy={rnd(k + 9) * 1080} r={3 + rnd(k + 4) * 4} fill="#C4A57A" />)}
      <rect x={120} y={60} width={1680} height={860} rx={14} fill="#CFE9F7" stroke="#8A6A43" strokeWidth={18} />
      {LAND.map((d, k) => <path key={'ld' + k} d={d} fill="#A6D08A" stroke={OL} strokeWidth={5} strokeLinejoin="round" />)}
      {z.strings && fly.length > 1 && fly.slice(1).map(([t0, idx], k) => { if (t < t0) return null; const a = P(fly[k][1]), b = P(idx), u = clamp((t - t0) / 1.6);
        return <path key={'rs' + k} d={`M ${a[0]} ${a[1]} Q ${(a[0] + b[0]) / 2} ${Math.min(a[1], b[1]) - 120} ${lerp(a[0], b[0], u)} ${lerp(a[1], b[1], u)}`} stroke={RED} strokeWidth={4} fill="none" strokeDasharray="10 8" />; })}
      {pins.map((p, k) => { const s = pop(t, p.at ?? 0, 0.4); if (s <= 0) return null; const on = hi === k, pu = on ? 1 + 0.25 * Math.max(0, Math.sin((t - hiAt) * 8)) * Math.exp(-(t - hiAt)) : 1;
        return <g key={'pn' + k} transform={`translate(${p.x} ${p.y}) scale(${s * pu})`}>
          {on && <circle r={46 + 10 * Math.sin(t * 6)} fill={GOLD} opacity={0.35} />}
          <path d="M 0 0 L -14 -36 A 18 18 0 1 1 14 -36 Z" fill={p.c || RED} stroke={OL} strokeWidth={4} /><circle cy={-46} r={7} fill="#FFFFFF" />
          {p.label && plaque(0, 40, p.label, '#FFFFFF', 20)}</g>; })}
      {show && <g transform={`translate(${px} ${py - 60}) rotate(${ang * 0.3})`}>
        <path d="M -50 0 Q -40 -16 40 -12 Q 62 -6 62 0 Q 62 6 40 12 Q -40 16 -50 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        <path d="M -6 -8 L -26 -46 L 6 -46 L 18 -8 Z M -6 8 L -26 40 L 4 40 L 16 8 Z M -46 -4 L -60 -26 L -44 -26 L -34 -6 Z" fill={BLUE} stroke={OL} strokeWidth={3.5} strokeLinejoin="round" />
        {[0, 1, 2].map((q) => <circle key={q} cx={14 + q * 12} cy={-4} r={3.4} fill="#BFE6F7" stroke={OL} strokeWidth={1.5} />)}</g>}
      {z.title && plaque(960, 1000, z.title, NAVY, 34, '#FFFFFF')}
    </g>;
  },

  /** oil port (left) vs a dam whose line stops at the shore (right) */
  pmoil: (t, z, f) => {
    const pump = kf(z.pump, t, 1), sh = clamp(kf(z.ship, t, 0)), wire = clamp(kf(z.wire, t, 0)), focus = z.focus || 'both';
    const dimL = focus === 'power' ? 0.35 : 1, dimR = focus === 'oil' ? 0.35 : 1, stop = z.stopAt !== undefined && t >= z.stopAt;
    const wx = lerp(1260, 1000, wire);
    return <g>
      {sky(z, f, '#8ED0F4', '#F2FAFF', 'pmosk')}
      {[0, 1, 2].map((k) => cloud(((k * 700 + t * 14) % 2600) - 300, 120 + (k % 2) * 50, 0.8, k))}
      {sea(z, f, t)}
      <g>
        <rect x={z.x0} y={f - 180} width={700 - z.x0} height={180} fill="#D9C79F" stroke={OL} strokeWidth={4} />
        {[[-200, 0], [60, 1], [300, 2]].map(([x, k]) => pumpjack(x, f - 180, 0.9, t, k, pump))}
        {[0, 1, 2].map((q) => <g key={'tk' + q} transform={`translate(${440 + q * 90} ${f - 180})`}><rect x={-40} y={-110} width={80} height={110} fill="#E7E2D8" stroke={OL} strokeWidth={4} /><ellipse cx={0} cy={-110} rx={40} ry={12} fill="#CFC8BB" stroke={OL} strokeWidth={4} /></g>)}
        {ship(lerp(560, 2600, sh), f + 60, 0.7, 'tk', 'oil', t)}
        {plaque(260, 160, z.oilText || 'OIL: SHIPS ANYWHERE', '#FFFFFF', 26)}
      </g>
      <g>
        <path d={ridge(1300, 2400, f - 120, 360, 260, 4)} fill="#7FA6C4" stroke={OL} strokeWidth={4} />
        <rect x={1260} y={f - 160} width={1300} height={700} fill="#9CCB86" stroke={OL} strokeWidth={4} />
        {dam(1700, f - 160, 0.7, t, 1, 'od')}
        {[1520, 1360].map((x, k) => pylon(x, f - 160, 0.6, 'op' + k))}
        <path d={`M 1600 ${f - 330} Q 1440 ${f - 300} 1360 ${f - 330} Q ${(1360 + wx) / 2} ${f - 290} ${wx} ${f - 250}`} stroke={OL} strokeWidth={4} fill="none" />
        {wire > 0.98 && <g transform={`translate(${wx} ${f - 250})`}><path d="M 0 0 L 0 40" stroke={OL} strokeWidth={4} /><rect x={-16} y={40} width={32} height={30} rx={5} fill="#455A64" stroke={OL} strokeWidth={4} />
          <path d="M -8 70 L -8 86 M 8 70 L 8 86" stroke={OL} strokeWidth={5} />
          {stop && Array.from({length: 5}, (_, q) => bolt(-30 + q * 15 + 10 * Math.sin(t * 20 + q), 110 + 8 * Math.sin(t * 17 + q), 0.18, GOLD, 'spk' + q))}</g>}
        {stop && stamp(1080, f - 430, z.stopText || "CAN'T SHIP A WATERFALL", RED, 34, 'st', pop(t, z.stopAt, 0.4))}
        {plaque(1780, 160, z.powerText || 'POWER: STAYS NEAR THE DAM', '#FFFFFF', 26)}
      </g>
      {dimL < 1 && <rect x={z.x0} y={-2500} width={1100 - z.x0} height={4000} fill="#FFFFFF" opacity={0.55} />}
      {dimR < 1 && <rect x={1100} y={-2500} width={z.x1 - 1100} height={4000} fill="#FFFFFF" opacity={0.55} />}
    </g>;
  },

  /** a fjord aluminum smelter */
  pmsmelter: (t, z, f) => {
    const flow = clamp(kf(z.flow, t, 1)), ore = clamp(kf(z.ore, t, 0)), ing = Math.floor(kf(z.ingots, t, 0)), out = clamp(kf(z.out, t, 0));
    return <g>
      {sky(z, f, '#8FCBF0', '#EEF8FF', 'pmssk')}
      {[0, 1].map((k) => cloud(((k * 900 + t * 10) % 2600) - 300, 110 + k * 60, 0.8, k))}
      <path d={ridge(z.x0, z.x1, f - 120, 420, 300, 7)} fill="#8DA8C2" stroke={OL} strokeWidth={4} />
      {Array.from({length: 12}, (_, k) => <path key={'sn' + k} d={`M ${z.x0 + k * 330 + 60} ${f - 440} l 60 70 l -120 0 Z`} fill={SNOW} opacity={0.9} />)}
      {sea(z, f, t, '#3F8FCB')}
      <rect x={-300} y={f - 120} width={2000} height={120} fill="#9CCB86" stroke={OL} strokeWidth={4} />
      {dam(-60, f - 120, 0.8, t, 1, 'sd')}
      {[260, 480].map((x, k) => pylon(x, f - 120, 0.55, 'sp' + k))}
      <path d={`M 160 ${f - 270} Q 260 ${f - 250} 370 ${f - 270} Q 480 ${f - 250} 640 ${f - 230}`} stroke={OL} strokeWidth={4} fill="none" />
      {flow > 0 && Array.from({length: 4}, (_, q) => { const u = (t * 0.7 + q / 4) % 1; return <circle key={'fp' + q} cx={lerp(160, 640, u)} cy={f - 268 + 30 * u + 10 * Math.sin(u * 6.28)} r={9} fill={GOLD} stroke={OL} strokeWidth={2} opacity={flow} />; })}
      {/* potline hall */}
      <g transform={`translate(640 ${f - 120})`}><rect x={0} y={-190} width={820} height={190} fill="#D5DCE4" stroke={OL} strokeWidth={6} />
        <path d="M -10 -190 L 830 -190 L 800 -230 L 20 -230 Z" fill="#9AA7B6" stroke={OL} strokeWidth={5} />
        {Array.from({length: 10}, (_, q) => <rect key={q} x={30 + q * 80} y={-120} width={50} height={60} rx={6} fill={ORANGE} opacity={0.55 + 0.35 * Math.sin(t * 5 + q)} stroke={OL} strokeWidth={3} />)}
        {Array.from({length: 5}, (_, q) => { const u = (t * 0.4 + q / 5) % 1; return <ellipse key={'ht' + q} cx={100 + q * 160} cy={-250 - u * 120} rx={30 + u * 30} ry={14 + u * 10} fill="#FFFFFF" opacity={0.5 * (1 - u)} />; })}
        {plaque(410, -280, z.plaque || 'ALUMINUM SMELTER (GENERIC)', '#FFFFFF', 22)}</g>
      {/* ingot stack */}
      <g transform={`translate(1560 ${f - 120})`}>{Array.from({length: Math.min(12, ing)}, (_, q) => { const r = Math.floor(q / 4), c = q % 4;
        return <path key={q} d={`M ${c * 46 - 92 + (r % 2) * 22} ${-r * 26} l 8 -24 h 30 l 8 24 Z`} fill="#CFD8DC" stroke={OL} strokeWidth={3} />; })}</g>
      {ship(lerp(2700, 1700, ore), f + 50, 0.6, 'ore', 'ore', t)}
      {out > 0 && ship(lerp(1700, 2900, out), f + 140, 0.6, 'ing', 'ingot', t)}
    </g>;
  },

  /** a cold hydro / geothermal valley with a data campus */
  pmnorth: (t, z, f) => {
    const v = z.variant || 'fjord', halls = kf(z.halls, t, 0), air = clamp(kf(z.air, t, 0)), level = clamp(kf(z.level, t, 1)), ten: string = pick(z.tenant, t, '');
    const tAt = lastAt(z.tenant, t);
    return <g>
      {sky(z, f, v === 'geo' ? '#9CC7E6' : '#86C3EC', '#F3FAFF', 'pmnsk' + v)}
      {[0, 1, 2].map((k) => cloud(((k * 800 + t * 9) % 2800) - 400, 100 + (k % 2) * 60, 0.75, k))}
      <path d={ridge(z.x0, z.x1, f - 100, v === 'river' ? 220 : 460, 280, v === 'geo' ? 11 : 5)} fill={v === 'geo' ? '#7D8A80' : '#8CA3BD'} stroke={OL} strokeWidth={4} />
      {Array.from({length: 14}, (_, k) => <path key={'sc' + k} d={`M ${z.x0 + k * 300 + 80} ${f - (v === 'river' ? 280 : 480)} l 70 80 l -140 0 Z`} fill={SNOW} opacity={0.95} />)}
      {v === 'fjord' && sea({...z, x0: z.x0, x1: 200}, f + 20, t, '#3F8FCB')}
      {ground(z, f, v === 'geo' ? '#B9C4A4' : '#B8D6A0', v === 'geo' ? '#9FAB89' : '#97BC7D')}
      {v !== 'geo' && dam(360, f, 0.8, t, level, 'nd')}
      {v === 'geo' && [200, 380, 520].map((x, k) => <g key={'gv' + k}>{Array.from({length: 4}, (_, q) => { const u = (t * 0.35 + q / 4 + k * 0.2) % 1;
        return <ellipse key={q} cx={x + 20 * Math.sin(u * 5 + k)} cy={f - 40 - u * 380} rx={40 + u * 70} ry={26 + u * 30} fill="#FFFFFF" opacity={0.75 * (1 - u)} />; })}
        <rect x={x - 40} y={f - 60} width={80} height={60} fill="#CFD8DC" stroke={OL} strokeWidth={4} /></g>)}
      {[700, 860].map((x, k) => pylon(x, f, 0.45, 'np' + k))}
      {Array.from({length: 4}, (_, k) => { const u = clamp(halls - k); if (u <= 0) return null;
        return <g key={'nh' + k} transform={`translate(0 ${(1 - E.outBack(u)) * 60})`} opacity={u}>{hall(1000 + k * 250, f, 220, 'n' + k, t, 1)}</g>; })}
      {air > 0 && Array.from({length: 6}, (_, q) => { const u = (t * 0.6 + q / 6) % 1, y = f - 240 + (q % 3) * 50;
        return <path key={'ar' + q} d={`M ${lerp(1900, 1240, u)} ${y} l -50 0 l 14 -12 M ${lerp(1900, 1240, u) - 50} ${y} l 14 12`} stroke={BLUE} strokeWidth={6} fill="none" opacity={air * (1 - Math.abs(u - 0.5) * 1.6)} strokeLinecap="round" />; })}
      {z.snow && Array.from({length: 40}, (_, q) => <circle key={'sf' + q} cx={z.x0 + ((rnd(q) * (z.x1 - z.x0) + t * 20 * rnd(q + 3)) % (z.x1 - z.x0))} cy={((rnd(q + 7) * 900 + t * 60 * (0.6 + rnd(q))) % 900)} r={3 + rnd(q + 1) * 3} fill="#FFFFFF" opacity={0.85} />)}
      {ten && <g transform={`translate(1500 ${f - 260}) scale(${pop(t, tAt, 0.4)})`}>{plaque(0, 0, ten, '#FFFFFF', 22)}</g>}
      {z.plaque && plaque(z.plaqueX ?? 420, f + 110, z.plaque, NAVY, 28, '#FFFFFF')}
    </g>;
  },

  /** a sunny plain (texas) or desert coast (gulf) */
  pmsun: (t, z, f) => {
    const v = z.variant || 'texas', solar = clamp(kf(z.solar, t, 0)), gas = clamp(kf(z.gas, t, 0)), halls = kf(z.halls, t, 0), ghosts = kf(z.ghosts, t, 0);
    const night = clamp(kf(z.night, t, 0)), heat = clamp(kf(z.heat, t, 0));
    const top = night > 0 ? `rgb(${lerp(255, 30, night) | 0},${lerp(200, 40, night) | 0},${lerp(130, 90, night) | 0})` : (v === 'gulf' ? '#FFC97A' : '#8ED0F4');
    return <g>
      {sky(z, f, top, night > 0.5 ? '#3A3F6B' : v === 'gulf' ? '#FFF3D6' : '#F4FBFF', 'pmusk' + v + Math.round(night * 10))}
      <g transform={`translate(${v === 'gulf' ? 1650 : 260} ${lerp(140, 760, night)})`}><circle r={90} fill="#FFD54F" stroke={OL} strokeWidth={5} />
        {Array.from({length: 12}, (_, k) => <path key={k} transform={`rotate(${k * 30 + t * 12})`} d="M 0 -110 L 0 -150" stroke="#FFB300" strokeWidth={8} strokeLinecap="round" />)}</g>
      {night > 0.6 && Array.from({length: 30}, (_, q) => <circle key={'st' + q} cx={z.x0 + rnd(q) * (z.x1 - z.x0)} cy={rnd(q + 5) * 500} r={2.5} fill="#FFFFFF" opacity={night} />)}
      {v === 'gulf' ? <g>{sea({...z, x0: z.x0, x1: 60}, f + 10, t, '#3FB1C9')}<path d={`M 60 ${f} Q 500 ${f - 90} 900 ${f - 20} Q 1400 ${f - 110} 1900 ${f - 30} Q 2400 ${f - 90} ${z.x1} ${f} L ${z.x1} ${f + 700} L 60 ${f + 700} Z`} fill="#E8C88A" stroke={OL} strokeWidth={4} /></g>
        : <path d={ridge(z.x0, z.x1, f - 40, 70, 400, 3)} fill="#C7B58C" stroke={OL} strokeWidth={4} />}
      {Array.from({length: Math.floor(ghosts)}, (_, k) => hall(1900 + (k % 7) * 230, f - 30 - Math.floor(k / 7) * 60, 200, 'g' + k, t, 0.7, true))}
      {ground(z, f, v === 'gulf' ? '#EED39C' : '#C9D88F', v === 'gulf' ? '#D8B878' : '#AFC071')}
      {Array.from({length: 4}, (_, r) => Array.from({length: 7}, (_, c) => { const idx = r * 7 + c, u = clamp(solar * 28 - idx); if (u <= 0) return null;
        return <g key={'sp' + idx} transform={`translate(${-500 + c * 120 + r * 30} ${f + 40 + r * 60}) scale(${u})`}><path d="M -50 0 L 40 0 L 56 -30 L -34 -30 Z" fill="#2B4C8C" stroke={OL} strokeWidth={3} />
          <path d="M -40 -15 L 48 -15 M -5 0 L 10 -30" stroke="#7FB2FF" strokeWidth={2} /></g>; }))}
      {v === 'texas' && [-700, -460, 2050, 2300].map((x, k) => turbine(x, f, 0.8, k, t))}
      {gas > 0 && <g transform={`translate(560 ${f})`} opacity={gas}><rect x={-90} y={-120} width={180} height={120} fill="#D7CCC8" stroke={OL} strokeWidth={5} /><rect x={50} y={-230} width={30} height={110} fill="#BCAAA4" stroke={OL} strokeWidth={4} />
        {Array.from({length: 4}, (_, q) => { const u = (t * 0.4 + q / 4) % 1; return <ellipse key={q} cx={65 + u * 60} cy={-250 - u * 160} rx={22 + u * 40} ry={14 + u * 20} fill="#ECEFF1" opacity={0.8 * (1 - u)} />; })}
        {plaque(0, -300, 'GAS PLANT', '#FFFFFF', 18)}</g>}
      {Array.from({length: 5}, (_, k) => { const u = clamp(halls - k); if (u <= 0) return null;
        return <g key={'sh' + k} transform={`translate(0 ${(1 - E.outBack(u)) * 60})`} opacity={u}>{hall(800 + k * 240, f, 210, 's' + k, t)}
          {night > 0.5 && <rect x={810 + k * 240} y={f - 140} width={190} height={20} fill="#FFE08A" opacity={0.6} />}</g>; })}
      {heat > 0 && Array.from({length: 8}, (_, q) => { const u = (t * 0.5 + q / 8) % 1; return <path key={'hs' + q} d={`M ${850 + q * 140} ${f - 200 - u * 140} q 12 -14 0 -28 q -12 -14 0 -28`} stroke={RED} strokeWidth={4} fill="none" opacity={heat * (1 - u)} />; })}
      {z.plaque && plaque(z.plaqueX ?? 1200, f + 110, z.plaque, NAVY, 28, '#FFFFFF')}
    </g>;
  },

  /** tropical river dam + coastal wind, and a giant bill stack */
  pmtropic: (t, z, f) => {
    const stack: any[] = z.stack || [], tax: string = pick(z.tax, t, ''), taxAt = lastAt(z.tax, t);
    let acc = 0;
    return <g>
      {sky(z, f, '#7CC8F2', '#EFFAFF', 'pmtsk')}
      {[0, 1, 2].map((k) => cloud(((k * 700 + t * 12) % 2600) - 300, 110 + (k % 2) * 60, 0.8, k))}
      <path d={ridge(z.x0, 900, f - 80, 260, 260, 9)} fill="#4F9A5C" stroke={OL} strokeWidth={4} />
      {ground(z, f, '#7CC26B', '#5FA853')}
      {dam(-60, f, 0.75, t, 1, 'td')}
      {[340, 500, 660].map((x, k) => turbine(x, f, 0.7, k, t))}
      {Array.from({length: 6}, (_, k) => <g key={'pm' + k} transform={`translate(${-900 + k * 160} ${f})`}><path d="M 0 0 Q 6 -90 -4 -170" stroke="#8D6E63" strokeWidth={10} fill="none" />
        {[0, 72, 144, 216, 288].map((r) => <path key={r} transform={`translate(-4 -170) rotate(${r + 4 * Math.sin(t * 2 + k)})`} d="M 0 0 Q 40 -20 80 10" stroke="#2E7D32" strokeWidth={12} fill="none" strokeLinecap="round" />)}</g>)}
      {pylon(850, f, 0.5, 'tp')}
      {/* the bill stack */}
      <g transform={`translate(1450 ${f})`}><rect x={-230} y={-660} width={460} height={660} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <T x={0} y={-610} s={30} c={NAVY}>{z.stackTitle || 'THE POWER BILL'}</T>
        {stack.map((b, k) => { const u = clamp((t - (b.at ?? 0)) / 0.5); if (u <= 0) return null; const h = (b.v ?? 0.2) * 520 * E.outBack(u), y0 = acc; acc += h;
          return <g key={k}><rect x={-180} y={-20 - y0 - h} width={360} height={h} fill={b.color || BLUE} stroke={OL} strokeWidth={4} />
            {h > 30 && <T x={0} y={-20 - y0 - h / 2 + 10} s={fit(b.label || '', 330, 26)} c="#FFFFFF" st={OL} sw={4}>{b.label}</T>}</g>; })}
        {tax && stamp(0, -740, tax, RED, 34, 'tx', pop(t, taxAt, 0.4))}</g>
    </g>;
  },

  /** the line at the plug */
  pmqueue: (t, z, f) => {
    const n = Math.round(kf(z.n, t, 0)), flip = kf(z.flip, t, 0), bring = clamp(kf(z.bring, t, 0)), plug = z.plugAt !== undefined && t >= z.plugAt;
    const pages = Math.floor(t * flip * 2);
    return <g>
      {sky(z, f, '#8FD0F2', '#F3FAFF', 'pmqsk')}
      {[0, 1].map((k) => cloud(((k * 900 + t * 10) % 2600) - 300, 130 + k * 60, 0.8, k))}
      {ground(z, f, '#B5D49A', '#97BC7D')}
      {/* substation */}
      <g transform={`translate(250 ${f})`}><rect x={-200} y={-30} width={400} height={30} fill="#9E9E9E" stroke={OL} strokeWidth={4} />
        {[-140, -40, 60, 160].map((x, k) => <g key={k}><rect x={x - 26} y={-150} width={52} height={120} fill="#B0BEC5" stroke={OL} strokeWidth={4} /><path d={`M ${x} -150 L ${x} -220`} stroke={OL} strokeWidth={5} /></g>)}
        {Array.from({length: 9}, (_, k) => <path key={'fn' + k} d={`M ${-200 + k * 50} -30 L ${-200 + k * 50} -110`} stroke="#78909C" strokeWidth={3} />)}
        <g transform="translate(300 -200)"><rect x={-90} y={-90} width={180} height={180} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
          <rect x={-40} y={-40} width={22} height={50} rx={6} fill={OL} /><rect x={18} y={-40} width={22} height={50} rx={6} fill={OL} />
          {plug && <circle r={110 + 8 * Math.sin(t * 8)} fill={GOLD} opacity={0.3} />}</g>
        {plaque(150, -380, z.plaque || 'GRID CONNECTION', NAVY, 26, '#FFFFFF')}</g>
      {/* queue of cubes */}
      {Array.from({length: n}, (_, k) => { const x = 700 + k * 150 + (k === 0 && plug ? -80 * clamp((t - z.plugAt) / 0.5) : 0), b = Math.abs(Math.sin(t * 3 + k)) * 6;
        return <g key={'q' + k} transform={`translate(${x} ${f - b})`}><rect x={-50} y={-100} width={100} height={100} rx={12} fill={k === 0 && plug ? '#E7ECF3' : '#D5DCE6'} stroke={OL} strokeWidth={5} />
          <circle cx={-18} cy={-60} r={7} fill={k === 0 && plug ? GREEN : CY} /><circle cx={18} cy={-60} r={7} fill={k === 0 && plug ? GREEN : CY} />
          <path d={k === 0 && plug ? 'M -18 -34 Q 0 -20 18 -34' : 'M -16 -30 L 16 -30'} stroke={OL} strokeWidth={4} fill="none" />
          {bring > 0 && <g opacity={bring} transform="translate(0 -128)"><rect x={-30} y={-20} width={60} height={34} rx={6} fill={GREEN} stroke={OL} strokeWidth={4} /><rect x={-8} y={-28} width={16} height={8} fill={OL} />{bolt(0, -3, 0.2, GOLD, 'bb' + k)}</g>}
          {k === 0 && <path d={`M -50 -40 Q -100 -40 ${plug ? -140 : -110} -60`} stroke={OL} strokeWidth={5} fill="none" />}</g>; })}
      {/* calendar */}
      {flip > 0 && <g transform="translate(1500 260)"><rect x={-110} y={-90} width={220} height={190} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><rect x={-110} y={-90} width={220} height={50} rx={10} fill={RED} stroke={OL} strokeWidth={6} />
        <T x={0} y={44} s={56} c={NAVY}>{z.years ? `YEAR ${1 + (pages % 10)}` : `${1 + (pages % 12)}`}</T>
        <g transform={`translate(0 -40) rotate(${((t * flip * 2) % 1) * -120})`}><rect x={-110} y={0} width={220} height={130} fill="#F5F5F5" stroke={OL} strokeWidth={4} opacity={0.8} /></g></g>}
    </g>;
  },

  /** Nia's clipboard scorecard */
  pmscore: (t, z, f) => {
    const rows: any[] = z.rows || [];
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#FFF1D6" />
      {Array.from({length: 16}, (_, k) => <path key={'ry' + k} transform={`translate(960 1200) rotate(${k * 22.5 + t * 3})`} d="M 0 0 L -80 -1600 L 80 -1600 Z" fill="#FDE3B8" />)}
      <g transform={`translate(960 560) rotate(${-2 + Math.sin(t) * 0.8})`}><rect x={-420} y={-430} width={840} height={880} rx={30} fill="#A1887F" stroke={OL} strokeWidth={8} />
        <rect x={-380} y={-380} width={760} height={800} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <rect x={-110} y={-460} width={220} height={70} rx={14} fill="#90A4AE" stroke={OL} strokeWidth={6} />
        <T x={0} y={-310} s={fit(z.title || "NIA'S SCORECARD", 700, 48)} c={NAVY}>{z.title || "NIA'S SCORECARD"}</T>
        {rows.map((r, k) => { const u = pop(t, r.at ?? 0, 0.4); if (u <= 0) return null; const y = -220 + k * 100, m = r.mark || 'yes';
          return <g key={k} opacity={clamp(u)}><T x={-330} y={y + 14} s={fit(r.label || '', 520, 38)} a="start" c={NAVY}>{r.label}</T>
            <g transform={`translate(290 ${y}) scale(${u})`}>{m === 'yes' ? <path d="M -30 0 l 20 22 l 40 -46" stroke={GREEN} strokeWidth={12} fill="none" strokeLinecap="round" />
              : m === 'no' ? <path d="M -26 -26 L 26 26 M 26 -26 L -26 26" stroke={RED} strokeWidth={12} strokeLinecap="round" />
                : <T x={0} y={18} s={56} c={ORANGE}>?</T>}</g></g>; })}</g>
    </g>;
  },

  /** title card: a giant plug pumps like an oil derrick */
  pmtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['COULD CHEAP', 'ELECTRICITY BECOME', 'THE NEW OIL?'];
    const a = Math.sin(t * 2.4) * 12;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#FFF1D2" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(960 900) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#FBE0B0' : '#FFF1D2'} />)}
      <path d={ridge(-200, 2200, 960, 120, 220, 2)} fill="#A6D08A" stroke={OL} strokeWidth={4} />
      <g transform="translate(1600 940)"><path d="M -110 0 L -20 -260 L 70 0" stroke={OL} strokeWidth={10} fill="none" />
        <g transform={`translate(-20 -260) rotate(${a})`}><rect x={-200} y={-22} width={400} height={44} rx={8} fill={NAVY} stroke={OL} strokeWidth={6} />
          <g transform="translate(220 0)"><rect x={-30} y={-46} width={90} height={92} rx={16} fill="#37474F" stroke={OL} strokeWidth={6} /><path d="M 60 -22 L 100 -22 M 60 22 L 100 22" stroke="#B0BEC5" strokeWidth={12} strokeLinecap="round" /></g></g>
        {Array.from({length: 4}, (_, q) => bolt(140 + q * 26, 30 + 10 * Math.sin(t * 9 + q), 0.25, GOLD, 'tb' + q))}</g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.55) / 0.5) * ln.length);
        return <T key={k} x={820} y={230 + k * 140} s={fit(ln, 1300, k === lines.length - 1 ? 140 : 104)} c={k === lines.length - 1 ? ORANGE : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={820} y={690} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a plug slides into a socket and the panel lights up */
  pmbumper: (t, z, f) => {
    const c = z.color || BLUE, u = E.inOut(win(t, 0.2, 0.8)), lit = t > 1.0;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g transform="translate(960 830)"><rect x={-80} y={-80} width={160} height={160} rx={28} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
        <rect x={-36} y={-36} width={18} height={44} rx={5} fill={OL} /><rect x={18} y={-36} width={18} height={44} rx={5} fill={OL} />
        <g transform={`translate(${lerp(-900, -150, u)} 0)`}><rect x={-300} y={-12} width={260} height={24} fill={OL} /><rect x={-60} y={-50} width={90} height={100} rx={14} fill="#37474F" stroke={OL} strokeWidth={6} />
          <path d="M 30 -20 L 70 -20 M 30 20 L 70 20" stroke="#B0BEC5" strokeWidth={12} strokeLinecap="round" /></g>
        {lit && Array.from({length: 6}, (_, q) => bolt(Math.cos(q) * 150, Math.sin(q) * 110 - 20, 0.3, GOLD, 'bmb' + q))}</g>
      <g opacity={clamp((t - 0.5) / 0.3)}><T x={960} y={280} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={370} width={1200} height={140} rx={20} fill={lit ? NAVY : '#2B3550'} stroke={OL} strokeWidth={6} />
        <T x={960} y={462} s={fit(z.title || '', 1140, 62)} c={lit ? GOLD : '#FFFFFF'}>{z.title || ''}</T>
        {t >= 1.4 && <T x={960} y={620} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.4) / 0.3)}>{z.caption || ''}</T>}</g>
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const POWERMAP_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

/** pmtag: top-left claim pill */
const TAGC: Record<string, string> = {FACT: GREEN, FORECAST: PURPLE, PLAN: PURPLE, PROPOSED: PURPLE, ESTIMATE: ORANGE, OUR: TEAL, COMPANY: '#8D6E63', FINDING: BLUE, STORY: '#5E6B85', MECHANISM: BLUE, ANALYSIS: NAVY, LIBRARY: NAVY, VERDICT: NAVY};
const pmtag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const txt: string = pick(a.tags, t, a.text || 'FACT'); if (!txt) return null;
  const key = txt.split(' ')[0], c = TAGC[key] || NAVY, w = txt.length * 17 + 70, x = kf(a.x, t, 36), y = kf(a.y, t, 36), t0 = Math.max(at, lastAt(a.tags, t));
  return <g key={'pt' + i} transform={`translate(${x} ${y}) scale(${pop(t, t0, 0.35)})`}>
    <rect x={0} y={0} width={w} height={46} rx={23} fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={26} cy={23} r={9} fill="#FFFFFF" /><T x={44} y={32} s={24} a="start" c="#FFFFFF">{txt}</T></g>;
};

/** cubby: the walking scale model of the campus (a server cube with an LED face and a plug tail) */
const cubby: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, walking = Math.abs(vx) > 20;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.6) hy = Math.sin((u / 0.6) * Math.PI) * 90; }
  const step = walking ? Math.sin(t * 14) : 0, bob = walking ? Math.abs(step) * 8 : Math.sin(t * 2.5 + i) * 3;
  const y = kf(a.y, t, f) - hy - bob, s = (a.scale ?? 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const face: string = pick(a.faces, t, a.face || 'happy'), fl = vx < -20 ? -1 : 1, glow = a.plugged !== undefined && t >= a.plugged;
  const eye = face === 'sleep' ? <g><path d="M -34 -96 q 12 8 24 0 M 10 -96 q 12 8 24 0" stroke={CY} strokeWidth={5} fill="none" /></g>
    : face === 'wow' ? <g><circle cx={-22} cy={-98} r={11} fill={CY} /><circle cx={22} cy={-98} r={11} fill={CY} /></g>
      : <g><rect x={-30} y={-106} width={16} height={(Math.floor(t * 0.7 + i) % 4 === 0 && (t % 1.43) < 0.12) ? 3 : 16} rx={4} fill={glow ? GREEN : CY} /><rect x={14} y={-106} width={16} height={(Math.floor(t * 0.7 + i) % 4 === 0 && (t % 1.43) < 0.12) ? 3 : 16} rx={4} fill={glow ? GREEN : CY} /></g>;
  const mouth = face === 'worry' ? 'M -18 -62 Q 0 -74 18 -62' : face === 'wow' ? 'M -10 -66 a 10 10 0 1 0 20 0 a 10 10 0 1 0 -20 0' : 'M -20 -70 Q 0 -54 20 -70';
  return <g key={'cb' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    {glow && <circle cx={0} cy={-90} r={110 + 6 * Math.sin(t * 7)} fill={GOLD} opacity={0.25} />}
    <path d={`M -54 -60 Q -110 -40 -120 ${-10 + 6 * Math.sin(t * 3)}`} stroke={OL} strokeWidth={6} fill="none" />
    <g transform={`translate(-128 ${-6 + 6 * Math.sin(t * 3)})`}><rect x={-14} y={-12} width={22} height={26} rx={4} fill="#37474F" stroke={OL} strokeWidth={3} /><path d="M -14 -6 L -24 -6 M -14 8 L -24 8" stroke="#B0BEC5" strokeWidth={4} /></g>
    <path d={`M -24 -14 L ${-28 + step * 12} 0 M 24 -14 L ${28 - step * 12} 0`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
    <rect x={-62} y={-170} width={124} height={156} rx={16} fill="#E7ECF3" stroke={OL} strokeWidth={6} />
    <rect x={-48} y={-150} width={96} height={110} rx={10} fill="#263238" stroke={OL} strokeWidth={4} />
    {eye}<path d={mouth} stroke={glow ? GREEN : CY} strokeWidth={5} fill={face === 'wow' ? CY : 'none'} strokeLinecap="round" />
    {[0, 1, 2].map((q) => <circle key={q} cx={-36 + q * 14} cy={-28} r={4} fill={(q + Math.floor(t * 3)) % 3 ? GREEN : GOLD} />)}
    <g transform={`translate(0 -178) rotate(${t * 300})`}><path d="M -22 0 L 22 0 M 0 -8 L 0 8" stroke={OL} strokeWidth={5} strokeLinecap="round" /></g>
    {a.carry === 'suitcase' && <g transform="translate(70 -40)"><rect x={0} y={-30} width={70} height={52} rx={8} fill={ORANGE} stroke={OL} strokeWidth={4} /><path d="M 20 -30 L 20 -42 L 50 -42 L 50 -30" stroke={OL} strokeWidth={4} fill="none" /></g>}
    {a.carry === 'battery' && <g transform="translate(76 -50)"><rect x={0} y={-26} width={64} height={44} rx={8} fill={GREEN} stroke={OL} strokeWidth={4} />{bolt(32, -4, 0.22, GOLD, 'cbb' + i)}</g>}
    {a.label && t < (a.labelUntil ?? at + 3) && <g transform={`scale(${fl} 1)`}>{plaque(0, -230, a.label, '#FFFFFF', 20)}</g>}
  </g>;
};

export const POWERMAP_ITEMS: Record<string, ItemFn> = {pmtag, cubby};
export const POWERMAP_INDOOR = ['pmoffice', 'pmmap', 'pmscore', 'pmtitle', 'pmbumper'];
