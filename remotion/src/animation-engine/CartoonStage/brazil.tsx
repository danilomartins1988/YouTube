import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * BRAZIL kit for CartoonStage (Episode 71, "Could Brazil Become the World's Factory for Robots?").
 *
 * Prime-time TV-cartoon GENRE (thick clean outlines, flat colour, squash and stretch), day scenes, everything ORIGINAL and drawn with
 * respect: no flags, no logos, no brand names, no real person, no stereotypes (ordinary modern places: a dam, mines, farms, a busy city,
 * a highway, a bank, a car plant). Cast: GUS (fictional factory scout of fictional Boltwell Robotics) and BIA (fictional engineer from Minas
 * Gerais) use the shared `toon` rig; the COST BACKPACK is the item `costpack` (running gag: a brick drops in at every stop).
 * Sets:
 *  - brhq: Boltwell's day-lit US office: skyline window, a big globe that spins (`spin` KF speed) and lands on South America at `land`,
 *    a wall screen (`screen` [[t, text]]), a desk model of the robot factory.
 *  - brfab: the robot-built-by-robots factory floor (skylights): orange arms (`arms` KF 0..6) assembling little robots on a conveyor,
 *    a few technicians (`people` KF 0..6 visible), `sign` [[t, text]].
 *  - brdam: a wide river with a concrete dam and spillway, a reservoir, wind turbines on the ridge (`wind` KF 0..1 appear), solar rows,
 *    pylons whose line pulses (`flow` KF 0..1) toward a factory silhouette, `plaque`.
 *  - brmine: the red hills of Minas Gerais: a terraced iron pit, an ore train that rolls (`train` KF speed), a hillside town with a white
 *    church and coloured houses, a glowing sample jar on a crate (`jar` t), `plaque`.
 *  - brfields: soybean rows to the horizon, a combine (`harvest` KF 0..1 across), silos, grain truck, `plaque`.
 *  - brcity: a busy modern Brazilian city street by day: towers, shops with awnings, a wave-patterned sidewalk, trees, a bus, a fruit
 *    stand, pedestrians (`crowd` KF 0..1), `plaque`.
 *  - brcounter: the tax counter / paperwork office: a long counter with a stamping clerk's window, paper towers that rise (`stack`
 *    KF 0..1), a wall clock that spins faster with `rush` KF, `sign` text.
 *  - brroad: a long highway to a port: a queue of trucks (`trucks` KF 0..10), distance signs, port cranes at the far end, a ghost rail
 *    line that appears (`rail` KF 0..1), `plaque`.
 *  - brbank: a bank hall with a giant rate gauge (`rate` KF 0..1 needle, `rateText`), a loan desk, papers.
 *  - brplant: a big car plant in Bahia: `busy` KF 0..1 (0 = quiet, dusty, gates shut; 1 = lights on, cars rolling out), `sign` [[t, text]].
 *  - brgate: an airport gate by day: big window, a plane taxiing (`plane` KF 0..1), a coffee kiosk, departures board (`board` text).
 *  - brtitle / brbumper: title card (a robot arm places the last piece on a green-and-gold landscape; no flag) and chapter bumpers
 *    (a brick thumps into a backpack; `act`, `title`, `caption`, `color`).
 * Items: costpack (the cost backpack: `x`/`y` KF, `drops` [[t, label]] bricks fall in with a thunk, `pulls` [t...] lift the top brick
 *  out, `face` sweat when heavy, `label`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#1A2238';
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
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.6);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#1E88E5', GOLD = '#F5B700', RED = '#E5483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', NAVY = '#1A2238', ORANGE = '#F08A24',
  PINK = '#E86A92', CY = '#29C5F6', PAPER = '#FFFDF4', WATER = '#5AB4E8', CLAY = '#C8643B', CLAY2 = '#A94E2C', LEAF = '#3E9B4F';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: any) => <path key={'bc' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const ground = (z: Z, f: number, c = '#A6D08A', c2 = '#88B86C') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const hills = (z: Z, f: number, c = '#BFE3A0', k = 0, h = 160) => { let d = `M ${z.x0} ${f}`; for (let x = z.x0; x <= z.x1 + 300; x += 300) d += ` Q ${x + 150} ${f - h - 80 * rnd(k + x / 300)} ${x + 300} ${f}`;
  return <path d={d + ' Z'} fill={c} stroke={OL} strokeWidth={4} />; };
const palm = (x: number, y: number, s: number, t: number, k: any) => <g key={'pa' + k} transform={`translate(${x} ${y}) scale(${s})`}><path d="M 0 0 Q 14 -150 -6 -280" stroke="#8A6236" strokeWidth={16} fill="none" />
  {[0, 1, 2, 3, 4].map((q) => <path key={q} transform={`translate(-6 -280) rotate(${q * 72 + Math.sin(t + q) * 4})`} d="M 0 0 Q 60 -20 120 20" stroke={LEAF} strokeWidth={14} fill="none" strokeLinecap="round" />)}</g>;
const tree = (x: number, y: number, s: number, k: any) => <g key={'tr' + k} transform={`translate(${x} ${y}) scale(${s})`}><rect x={-10} y={-90} width={20} height={90} fill="#8A6236" stroke={OL} strokeWidth={4} />
  <circle cy={-130} r={70} fill={LEAF} stroke={OL} strokeWidth={5} /><circle cx={-40} cy={-110} r={40} fill="#4FB360" stroke={OL} strokeWidth={4} /></g>;
const turbine = (x: number, y: number, s: number, t: number, k: any) => <g key={'wt' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -8 0 L -4 -300 L 4 -300 L 8 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />
  <g transform={`translate(0 -300) rotate(${t * 90 + k * 40})`}>{[0, 120, 240].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 L -10 -16 L 0 -150 L 10 -16 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />)}</g>
  <circle cy={-300} r={10} fill="#C5CDD8" stroke={OL} strokeWidth={4} /></g>;
const arm = (x: number, y: number, s: number, t: number, k: any, c = ORANGE) => { const a = Math.sin(t * 3 + k) * 26;
  return <g key={'ar' + k} transform={`translate(${x} ${y}) scale(${s})`}><rect x={-50} y={-30} width={100} height={30} fill={c} stroke={OL} strokeWidth={5} />
    <g transform={`translate(0 -30) rotate(${-30 + a})`}><rect x={-14} y={-190} width={28} height={190} rx={12} fill={c} stroke={OL} strokeWidth={5} />
      <g transform={`translate(0 -190) rotate(${70 - a * 2})`}><rect x={-12} y={-140} width={24} height={140} rx={10} fill={c} stroke={OL} strokeWidth={5} /><path d="M -22 -140 L -22 -170 M 22 -140 L 22 -170" stroke={OL} strokeWidth={8} strokeLinecap="round" /></g>
      <circle cy={-190} r={18} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g><circle cy={-30} r={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>; };
const minibot = (x: number, y: number, s: number, k: any) => <g key={'mb' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-34} y={-70} width={68} height={60} rx={12} fill="#CFD8E3" stroke={OL} strokeWidth={4} /><rect x={-24} y={-60} width={48} height={30} rx={6} fill="#263238" />
  <circle cx={-10} cy={-45} r={5} fill={CY} /><circle cx={10} cy={-45} r={5} fill={CY} /><rect x={-26} y={-10} width={52} height={10} rx={5} fill="#5E6B85" stroke={OL} strokeWidth={3} /></g>;
const truck = (x: number, y: number, s: number, c: string, k: any, load = '#7A4B2A') => <g key={'tk' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-170} y={-120} width={240} height={100} rx={6} fill={load} stroke={OL} strokeWidth={5} /><rect x={74} y={-100} width={86} height={80} rx={10} fill={c} stroke={OL} strokeWidth={5} />
  <rect x={92} y={-88} width={46} height={30} rx={4} fill="#BFE6F7" stroke={OL} strokeWidth={3} /><circle cx={-120} cy={-12} r={20} fill={OL} /><circle cx={-60} cy={-12} r={20} fill={OL} /><circle cx={120} cy={-12} r={20} fill={OL} /></g>;
const ppl = (x: number, y: number, s: number, k: number, t: number) => { const sw = Math.sin(t * 7 + k) * 10, c = [BLUE, ORANGE, TEAL, PINK, GREEN, '#7357C9', GOLD][k % 7];
  return <g key={'pp' + k} transform={`translate(${x} ${y}) scale(${s})`}><path d={`M -10 0 L ${-12 + sw} -60 M 10 0 L ${12 - sw} -60`} stroke="#34406A" strokeWidth={12} strokeLinecap="round" />
    <rect x={-26} y={-140} width={52} height={86} rx={20} fill={c} stroke={OL} strokeWidth={4} /><circle cy={-168} r={26} fill={['#8D5A3B', '#F1C27D', '#C68642', '#E0AC69', '#5C3A21'][k % 5]} stroke={OL} strokeWidth={4} />
    <path d="M -26 -176 Q 0 -206 26 -176" fill={['#2B1A12', '#6D4C41', '#212121', '#A1887F'][k % 4]} stroke={OL} strokeWidth={3} /></g>; };
const flowLine = (d: string, w: number, c: string, t: number, k: any) => <g key={'fl' + k}><path d={d} stroke={OL} strokeWidth={w + 8} fill="none" strokeLinecap="round" />
  <path d={d} stroke={c} strokeWidth={w} fill="none" strokeLinecap="round" /><path d={d} stroke="#FFFFFF" strokeWidth={Math.max(3, w * 0.25)} fill="none" strokeDasharray="20 40" strokeDashoffset={-t * 180} opacity={0.8} /></g>;

const RAW: Record<string, SetFn> = {
  /** Boltwell's US office */
  brhq: (t, z, f) => {
    const spin = kf(z.spin, t, 0.3), land = z.land ?? 999, scr: string = pick(z.screen, t, '');
    const rot = t < land ? t * spin * 120 : land * spin * 120 + 30 * E.outBack(win(t, land, 0.8));
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#EEF2F7" />
      <g transform="translate(240 130)"><rect x={0} y={0} width={1440} height={520} rx={10} fill="#BFE6F7" stroke={OL} strokeWidth={6} />
        {Array.from({length: 11}, (_, k) => { const h = 160 + rnd(k) * 260; return <rect key={'sk' + k} x={30 + k * 130} y={520 - h} width={100} height={h} fill={k % 2 ? '#9FB3C8' : '#B9C8D8'} stroke={OL} strokeWidth={3} />; })}
        {[0, 1].map((k) => cloud(300 + k * 700 + ((t * 10) % 300), 90, 0.7, 'h' + k))}<path d="M 720 0 L 720 520 M 0 260 L 1440 260" stroke={OL} strokeWidth={6} /></g>
      {/* globe */}
      <g transform="translate(560 760)"><path d="M -70 260 L 70 260 L 30 200 L -30 200 Z" fill="#8A6236" stroke={OL} strokeWidth={5} /><path d="M 0 200 L 0 150" stroke={OL} strokeWidth={10} />
        <circle r={160} cy={-20} fill={WATER} stroke={OL} strokeWidth={7} />
        <clipPath id="brglobe"><circle r={156} cy={-20} /></clipPath>
        <g clipPath="url(#brglobe)">{[0, 1, 2].map((q) => { const x = ((rot + q * 240) % 720) - 360; return <g key={q} transform={`translate(${x} -20)`}>
          <path d="M -60 -120 Q -10 -140 20 -100 Q 40 -60 10 -30 Q -30 -20 -50 -60 Z" fill={GREEN} stroke={OL} strokeWidth={4} />
          <path d="M 30 -10 Q 90 -20 100 30 Q 90 90 50 130 Q 30 90 20 50 Q 10 20 30 -10 Z" fill="#4FB360" stroke={OL} strokeWidth={4} />
          <path d="M 140 -110 Q 200 -120 220 -70 Q 190 -30 150 -50 Z" fill={GREEN} stroke={OL} strokeWidth={4} /></g>; })}</g>
        {t >= land && <g opacity={clamp((t - land - 0.5) / 0.3)}><circle cx={60} cy={20} r={16 + 4 * Math.sin(t * 6)} fill="none" stroke={RED} strokeWidth={6} /><path d="M 60 20 L 60 -40" stroke={RED} strokeWidth={5} /><circle cx={60} cy={-46} r={10} fill={RED} stroke={OL} strokeWidth={3} /></g>}</g>
      {/* desk with factory model */}
      <g transform="translate(1340 860)"><rect x={-360} y={-30} width={720} height={40} rx={8} fill="#B07A4A" stroke={OL} strokeWidth={5} /><path d="M -330 10 L -330 200 M 330 10 L 330 200" stroke={OL} strokeWidth={12} />
        <rect x={-200} y={-150} width={400} height={120} fill="#E4E9F0" stroke={OL} strokeWidth={5} /><path d="M -210 -150 L -140 -200 L -70 -150 L 0 -200 L 70 -150 L 140 -200 L 210 -150" fill="#C5CDD8" stroke={OL} strokeWidth={4} />
        {arm(-90, -40, 0.32, t, 1)}{arm(60, -40, 0.32, t, 2)}{plaque(0, -230, 'NEW PLANT · SITE: ?', GOLD, 20)}</g>
      {scr && <g transform="translate(1340 330)"><rect x={-330} y={-110} width={660} height={200} rx={12} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={10} s={fit(scr, 600, 46)} c={GOLD}>{scr}</T></g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C9B79C" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#A8946F" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** robots building robots */
  brfab: (t, z, f) => {
    const arms = kf(z.arms, t, 6), people = kf(z.people, t, 1), sign: string = pick(z.sign, t, '');
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E4E9F0" />
      {Array.from({length: 10}, (_, k) => <path key={'sl' + k} d={`M ${z.x0 + 100 + k * 420} 80 l 160 -60 l 160 60 Z`} fill="#BFE6F7" stroke={OL} strokeWidth={5} />)}
      <rect x={z.x0} y={80} width={z.x1 - z.x0} height={16} fill="#9AA6B8" />
      {sign && <g transform="translate(960 250)"><rect x={-440} y={-50} width={880} height={86} rx={12} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={0} y={14} s={fit(sign, 820, 44)} c={GOLD}>{sign}</T></g>}
      <rect x={200} y={f - 150} width={1560} height={40} rx={20} fill="#5E6B85" stroke={OL} strokeWidth={6} />
      {Array.from({length: 17}, (_, k) => <circle key={'rl' + k} cx={220 + k * 94} cy={f - 130} r={12} fill="#9AA6B8" stroke={OL} strokeWidth={3} transform={`rotate(${t * 200} ${220 + k * 94} ${f - 130})`} />)}
      {Array.from({length: 8}, (_, k) => { const x = 200 + (((t * 150) + k * 200) % 1560); return minibot(x, f - 150, 0.9, 'fb' + k); })}
      {Array.from({length: 6}, (_, q) => { const u = clamp(arms - q); if (u <= 0) return null; return <g key={'fa' + q} transform={`translate(${330 + q * 250} 0) scale(${E.outBack(u)}) translate(${-(330 + q * 250)} 0)`}>{arm(330 + q * 250, f - 150, 0.9, t, q)}</g>; })}
      {Array.from({length: 6}, (_, q) => { const u = clamp(people - q); if (u <= 0) return null; return <g key={'fp' + q} opacity={u}>{ppl(260 + q * 300, f + 40, 0.9, q + 2, t * 0.2)}</g>; })}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#B8C0CC" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#9AA6B8" stroke={OL} strokeWidth={4} />
      {Array.from({length: 24}, (_, k) => <path key={'ys' + k} d={`M ${z.x0 + k * 300} ${f + 120} l 120 0`} stroke={GOLD} strokeWidth={10} />)}
    </g>;
  },

  /** a dam, wind on the ridge, solar rows, the line to the plant */
  brdam: (t, z, f) => {
    const wind = kf(z.wind, t, 1), flow = kf(z.flow, t, 1);
    return <g>
      {sky(z, f, '#7EC8F2', '#E2F5FF', 'brds' + (z.ox ?? 0))}
      {[0, 1, 2, 3].map((k) => cloud(z.x0 + 300 + k * 700 + ((t * 14) % 700), 140 + 40 * (k % 2), 0.9, 'd' + k))}
      {hills(z, f - 300, '#8FCB7A', 2, 220)}
      {Array.from({length: 6}, (_, k) => { const u = clamp(wind * 6 - k); return u > 0 ? <g key={'wd' + k} opacity={u}>{turbine(200 + k * 330, f - 330 - 40 * rnd(k), 0.8 * E.outBack(u), t, k)}</g> : null; })}
      {/* reservoir + dam */}
      <path d={`M ${z.x0} ${f - 260} L 1100 ${f - 260} L 1100 ${f - 120} L ${z.x0} ${f - 120} Z`} fill={WATER} stroke={OL} strokeWidth={4} />
      {Array.from({length: 8}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + 80 + k * 160 + ((t * 30) % 60)} ${f - 210} q 20 -10 40 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" />)}
      <path d={`M 1100 ${f - 290} L 1260 ${f - 290} L 1340 ${f} L 1040 ${f} Z`} fill="#D9DEE6" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      {[0, 1, 2].map((k) => <rect key={'sp' + k} x={1120 + k * 50} y={f - 280} width={30} height={280} fill={WATER} opacity={0.7 + 0.3 * Math.sin(t * 8 + k)} />)}
      {plaque(1200, f - 320, z.damLabel || 'HYDRO DAM', '#FFFFFF', 22)}
      <path d={`M 1340 ${f - 40} Q 1600 ${f - 10} ${z.x1} ${f - 30}`} stroke={WATER} strokeWidth={60} fill="none" />
      {/* solar rows */}
      {Array.from({length: 5}, (_, k) => <g key={'so' + k} transform={`translate(${160 + k * 170} ${f - 40})`}><path d="M -60 0 L -40 -50 L 60 -50 L 40 0 Z" fill="#2F5DA8" stroke={OL} strokeWidth={4} /><path d="M -10 -50 L -20 0 M 20 -50 L 10 0" stroke="#9EC5FF" strokeWidth={3} /></g>)}
      {/* pylons to plant */}
      {[0, 1, 2].map((k) => <path key={'py' + k} d={`M ${1460 + k * 160} ${f} L ${1490 + k * 160} ${f - 260} L ${1520 + k * 160} ${f} M ${1468 + k * 160} ${f - 220} L ${1512 + k * 160} ${f - 220}`} stroke={OL} strokeWidth={6} fill="none" />)}
      {flow > 0.02 && flowLine(`M 1300 ${f - 300} Q 1500 ${f - 330} 1650 ${f - 260} T 1900 ${f - 240}`, 14 * flow, GOLD, t, 'pw')}
      <g transform={`translate(1960 ${f})`}><rect x={-120} y={-200} width={240} height={200} fill="#E4E9F0" stroke={OL} strokeWidth={5} /><path d="M -130 -200 L -60 -250 L 10 -200 L 80 -250 L 130 -200" fill="#C5CDD8" stroke={OL} strokeWidth={4} />
        {plaque(0, -280, 'ROBOT PLANT?', GOLD, 20)}</g>
      {z.plaque && plaque(960, 330, z.plaque, '#FFFFFF', 26)}
      {ground(z, f, '#9ED07F', '#7DB85F')}
    </g>;
  },

  /** the red hills of Minas Gerais */
  brmine: (t, z, f) => {
    const train = kf(z.train, t, 1), jar = z.jar ?? 999;
    const tx = ((t * 180 * train) % 3400) - 1000;
    return <g>
      {sky(z, f, '#86CCF4', '#FFF1DC', 'brms' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 400 + k * 800 + ((t * 10) % 800), 150, 0.85, 'm' + k))}
      {hills(z, f - 260, '#9BC97F', 6, 200)}
      {/* terraced pit */}
      <g transform={`translate(560 ${f - 120})`}>{[0, 1, 2, 3, 4].map((q) => <path key={q} d={`M ${-420 + q * 60} ${-q * 50} L ${420 - q * 60} ${-q * 50} L ${400 - q * 60} ${-q * 50 - 40} L ${-400 + q * 60} ${-q * 50 - 40} Z`} fill={q % 2 ? CLAY : CLAY2} stroke={OL} strokeWidth={4} />)}
        <g transform={`translate(${-200 + ((t * 40) % 400)} -170)`}>{truck(0, 0, 0.35, GOLD, 'pt', '#7A2E1A')}</g>{plaque(0, -300, 'IRON ORE', '#FFFFFF', 22)}</g>
      {/* hillside town */}
      <g transform={`translate(1450 ${f - 230})`}>{[0, 1, 2, 3, 4].map((q) => <g key={q} transform={`translate(${-260 + q * 110} ${-((q * 37) % 60)})`}><rect x={-46} y={-80} width={92} height={80} fill={['#FFE08A', '#9AD3F5', '#F7B6C8', '#B8E6B0', '#FFFFFF'][q]} stroke={OL} strokeWidth={4} />
          <path d="M -54 -80 L 0 -116 L 54 -80 Z" fill={CLAY} stroke={OL} strokeWidth={4} strokeLinejoin="round" /><rect x={-14} y={-46} width={28} height={46} fill="#2E6BA8" stroke={OL} strokeWidth={3} /></g>)}
        <g transform="translate(330 -60)"><rect x={-70} y={-150} width={140} height={150} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={-70} y={-250} width={40} height={100} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><rect x={30} y={-250} width={40} height={100} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
          <path d="M -74 -250 L -50 -290 L -26 -250 M 26 -250 L 50 -290 L 74 -250" fill={GOLD} stroke={OL} strokeWidth={4} /><path d="M -24 0 L -24 -60 Q 0 -86 24 -60 L 24 0 Z" fill="#2E6BA8" stroke={OL} strokeWidth={4} /></g></g>
      {/* ore train */}
      <path d={`M ${z.x0} ${f - 30} L ${z.x1} ${f - 30}`} stroke="#5E6B85" strokeWidth={10} /><path d={`M ${z.x0} ${f - 14} L ${z.x1} ${f - 14}`} stroke="#5E6B85" strokeWidth={10} />
      {Array.from({length: 40}, (_, k) => <rect key={'sl' + k} x={z.x0 + k * 120} y={f - 34} width={16} height={26} fill="#8A6236" />)}
      <g transform={`translate(${tx} ${f - 40})`}>{Array.from({length: 9}, (_, k) => <g key={'wg' + k} transform={`translate(${-k * 190} 0)`}>
        {k === 0 ? <g><rect x={-90} y={-150} width={180} height={130} rx={10} fill={GOLD} stroke={OL} strokeWidth={5} /><rect x={20} y={-130} width={50} height={40} fill="#BFE6F7" stroke={OL} strokeWidth={3} /></g>
          : <g><path d="M -85 -110 L 85 -110 L 70 -20 L -70 -20 Z" fill="#5E6B85" stroke={OL} strokeWidth={5} /><path d="M -80 -110 Q 0 -160 80 -110 Z" fill="#7A2E1A" stroke={OL} strokeWidth={4} /></g>}
        <circle cx={-50} cy={-14} r={16} fill={OL} /><circle cx={50} cy={-14} r={16} fill={OL} /></g>)}</g>
      {/* sample jar */}
      {t >= jar && <g transform={`translate(1040 ${f - 60}) scale(${pop(t, jar, 0.5)})`}><rect x={-80} y={-60} width={160} height={60} fill="#C99A5B" stroke={OL} strokeWidth={5} />
        <circle cy={-120} r={70 + 6 * Math.sin(t * 4)} fill={GOLD} opacity={0.25} /><rect x={-34} y={-150} width={68} height={90} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={-28} y={-110} width={56} height={46} rx={8} fill="#8E99A6" />
        <rect x={-38} y={-166} width={76} height={20} rx={6} fill="#5E6B85" stroke={OL} strokeWidth={4} /><T x={0} y={-80} s={20} c="#FFFFFF">Nb</T></g>}
      {z.plaque && plaque(960, 330, z.plaque, '#FFFFFF', 26)}
      {ground(z, f, '#C98A5E', CLAY2)}
    </g>;
  },

  /** soybean fields */
  brfields: (t, z, f) => {
    const hv = kf(z.harvest, t, 0.5);
    return <g>
      {sky(z, f, '#7EC8F2', '#FFF6DE', 'brfs' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 300 + k * 800 + ((t * 12) % 800), 150, 0.9, 'f' + k))}
      <rect x={z.x0} y={f - 420} width={z.x1 - z.x0} height={420} fill="#B9D86B" />
      {Array.from({length: 14}, (_, k) => <path key={'rw' + k} d={`M 960 ${f - 420} L ${z.x0 + k * ((z.x1 - z.x0) / 13)} ${f}`} stroke="#7FB048" strokeWidth={10} />)}
      {Array.from({length: 22}, (_, k) => <circle key={'sb' + k} cx={z.x0 + 100 + k * 220} cy={f - 20} r={26} fill="#9CC458" stroke={OL} strokeWidth={3} />)}
      <g transform={`translate(1560 ${f - 380})`}>{[0, 1, 2].map((q) => <g key={q} transform={`translate(${q * 110} 0)`}><rect x={-44} y={-200} width={88} height={200} fill="#D9DEE6" stroke={OL} strokeWidth={5} /><path d="M -44 -200 Q 0 -250 44 -200" fill="#C5CDD8" stroke={OL} strokeWidth={5} /></g>)}</g>
      <g transform={`translate(${lerp(-200, 2100, hv)} ${f - 200})`}><rect x={-140} y={-130} width={240} height={110} rx={12} fill={GREEN} stroke={OL} strokeWidth={5} /><rect x={20} y={-200} width={90} height={80} rx={8} fill={GREEN} stroke={OL} strokeWidth={5} />
        <rect x={34} y={-190} width={60} height={46} fill="#BFE6F7" stroke={OL} strokeWidth={3} /><rect x={110} y={-70} width={90} height={40} fill={GOLD} stroke={OL} strokeWidth={4} transform={`rotate(${Math.sin(t * 9) * 3} 155 -50)`} />
        <circle cx={-90} cy={-14} r={34} fill={OL} /><circle cx={60} cy={-10} r={24} fill={OL} /></g>
      {truck(((t * 120) % 2600) - 400, f + 120, 0.8, BLUE, 'ft', GOLD)}
      {z.plaque && plaque(960, 330, z.plaque, '#FFFFFF', 26)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C98A5E" /><rect x={z.x0} y={f + 60} width={z.x1 - z.x0} height={90} fill="#8F9AA8" />
    </g>;
  },

  /** a busy city street */
  brcity: (t, z, f) => {
    const crowd = kf(z.crowd, t, 1);
    return <g>
      {sky(z, f, '#7EC8F2', '#FFF0DA', 'brcs' + (z.ox ?? 0))}
      {Array.from({length: 14}, (_, k) => { const h = 380 + rnd(k + 2) * 420, x = z.x0 + 60 + k * 240; return <g key={'tw' + k}><rect x={x} y={f - 160 - h} width={190} height={h} fill={['#D8E2EC', '#F2E6CF', '#C9D8E8', '#E8D9C6'][k % 4]} stroke={OL} strokeWidth={4} />
        {Array.from({length: Math.floor(h / 70)}, (_, r) => <rect key={r} x={x + 22} y={f - 130 - h + r * 70} width={146} height={30} fill="#BFE6F7" stroke={OL} strokeWidth={2} />)}</g>; })}
      {[0, 1, 2, 3, 4, 5, 6].map((q) => { const x = z.x0 + 120 + q * 470, c = [PINK, TEAL, ORANGE, BLUE, GREEN, GOLD, RED][q];
        return <g key={'sh' + q} transform={`translate(${x} ${f})`}><rect x={-190} y={-200} width={380} height={200} fill="#FFF3DD" stroke={OL} strokeWidth={5} />
          {[0, 1, 2, 3, 4, 5].map((s) => <path key={s} d={`M ${-190 + s * 64} -200 l 64 0 l -8 44 l -48 0 Z`} fill={s % 2 ? '#FFFFFF' : c} stroke={OL} strokeWidth={3} />)}
          <rect x={-150} y={-140} width={300} height={100} fill="#BFE6F7" stroke={OL} strokeWidth={4} /></g>; })}
      {/* fruit stand */}
      <g transform={`translate(1500 ${f + 40})`}><rect x={-140} y={-80} width={280} height={80} fill="#B07A4A" stroke={OL} strokeWidth={5} />{Array.from({length: 9}, (_, k) => <circle key={k} cx={-110 + k * 28} cy={-90} r={16} fill={[ORANGE, GOLD, RED, GREEN][k % 4]} stroke={OL} strokeWidth={3} />)}
        <path d="M -150 -200 L 150 -200 L 120 -150 L -120 -150 Z" fill={GREEN} stroke={OL} strokeWidth={5} /><path d="M -130 -150 L -130 -80 M 130 -150 L 130 -80" stroke={OL} strokeWidth={6} /></g>
      {tree(300, f + 30, 0.9, 'c1')}{palm(1880, f + 30, 0.9, t, 'c2')}
      {/* wave sidewalk */}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={180} fill="#FFFFFF" />
      {Array.from({length: 4}, (_, r) => <path key={'wv' + r} d={`M ${z.x0} ${f + 30 + r * 40} ${Array.from({length: 40}, (_, k) => `q 60 ${k % 2 ? 24 : -24} 120 0`).join(' ')}`} stroke={OL} strokeWidth={10} fill="none" />)}
      {Array.from({length: 14}, (_, k) => { const u = clamp(crowd * 14 - k); if (u <= 0) return null; const dir = k % 2 ? 1 : -1, x = ((k * 330 + dir * t * 60) % 2600 + 2600) % 2600 - 300;
        return <g key={'cw' + k} opacity={u}>{ppl(x, f + 150, 0.85, k, t)}</g>; })}
      <rect x={z.x0} y={f + 180} width={z.x1 - z.x0} height={600} fill="#8F9AA8" />
      <g transform={`translate(${((t * 160) % 3000) - 600} ${f + 330})`}><rect x={-180} y={-130} width={360} height={120} rx={18} fill={GREEN} stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3].map((q) => <rect key={q} x={-160 + q * 80} y={-112} width={60} height={44} fill="#BFE6F7" stroke={OL} strokeWidth={3} />)}<circle cx={-110} cy={-6} r={24} fill={OL} /><circle cx={110} cy={-6} r={24} fill={OL} /></g>
      {z.plaque && plaque(960, 330, z.plaque, '#FFFFFF', 26)}
    </g>;
  },

  /** the tax counter and the paperwork */
  brcounter: (t, z, f) => {
    const stack = kf(z.stack, t, 0.2), rush = kf(z.rush, t, 1), sign: string = z.sign || 'TAX COUNTER';
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#F2EBDD" />
      {Array.from({length: 8}, (_, k) => <rect key={'wn' + k} x={z.x0 + 100 + k * 460} y={90} width={220} height={240} rx={14} fill="#BFE6F7" stroke={OL} strokeWidth={5} />)}
      <g transform="translate(1600 210)"><circle r={80} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><path d={`M 0 0 L ${50 * Math.sin(t * rush * 2)} ${-50 * Math.cos(t * rush * 2)} M 0 0 L ${34 * Math.sin(t * rush * 0.2)} ${-34 * Math.cos(t * rush * 0.2)}`} stroke={OL} strokeWidth={6} strokeLinecap="round" /></g>
      <g transform="translate(960 360)"><rect x={-360} y={-50} width={720} height={90} rx={12} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={0} y={14} s={fit(sign, 680, 44)} c={GOLD}>{sign}</T></g>
      {/* paper towers */}
      {[0, 1, 2, 3, 4].map((q) => { const h = 40 + stack * (160 + q * 70) * (0.7 + 0.3 * rnd(q)), x = 340 + q * 320;
        return <g key={'pt' + q} transform={`translate(${x} ${f - 240}) rotate(${Math.sin(t * 2 + q) * stack * 2})`}>{Array.from({length: Math.max(1, Math.floor(h / 16))}, (_, r) => <rect key={r} x={-80 + (rnd(q * 9 + r) - 0.5) * 14} y={-r * 16 - 16} width={160} height={14} fill={r % 5 === 4 ? '#FFE9A8' : PAPER} stroke={OL} strokeWidth={2} />)}</g>; })}
      <rect x={z.x0} y={f - 240} width={z.x1 - z.x0} height={240} fill="#B07A4A" stroke={OL} strokeWidth={6} />
      {Array.from({length: 12}, (_, k) => <rect key={'pn' + k} x={z.x0 + 40 + k * 340} y={f - 200} width={280} height={160} rx={8} fill="#C48A57" stroke={OL} strokeWidth={4} />)}
      {/* stamp */}
      <g transform={`translate(1700 ${f - 260 - 80 * Math.max(0, Math.sin(t * 5))})`}><rect x={-50} y={-30} width={100} height={36} rx={6} fill="#8A6236" stroke={OL} strokeWidth={5} /><rect x={-16} y={-120} width={32} height={90} rx={8} fill="#8A6236" stroke={OL} strokeWidth={5} /><circle cy={-130} r={26} fill={RED} stroke={OL} strokeWidth={5} /></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#D7C7A8" />
    </g>;
  },

  /** a long highway to the port */
  brroad: (t, z, f) => {
    const n = kf(z.trucks, t, 6), rail = kf(z.rail, t, 0);
    return <g>
      {sky(z, f, '#86CCF4', '#FFF4DE', 'brrs' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 500 + k * 800 + ((t * 12) % 800), 150, 0.8, 'r' + k))}
      {hills(z, f - 220, '#A9D58C', 9, 140)}
      {/* port at far right */}
      <g transform={`translate(1760 ${f - 220})`}><rect x={-140} y={-20} width={500} height={40} fill={WATER} />{[0, 1].map((q) => <g key={q} transform={`translate(${q * 150} 0)`}><path d="M -20 0 L -20 -300 L 120 -300 L 120 -270 L 0 -270 L 0 0" fill={RED} stroke={OL} strokeWidth={5} /><path d={`M 100 -270 L 100 ${-200 + 40 * Math.sin(t + q)}`} stroke={OL} strokeWidth={4} /></g>)}
        {[0, 1, 2].map((q) => <rect key={'ct' + q} x={-120 + q * 70} y={-60} width={64} height={40} fill={[BLUE, ORANGE, GREEN][q]} stroke={OL} strokeWidth={4} />)}{plaque(80, -340, 'PORT', '#FFFFFF', 22)}</g>
      {/* ghost rail */}
      {rail > 0.02 && <g opacity={rail * 0.8}><path d={`M ${z.x0} ${f - 150} L 1700 ${f - 150}`} stroke="#5E6B85" strokeWidth={8} strokeDasharray="30 14" />
        <g transform={`translate(${lerp(-300, 1300, (t * 0.15) % 1)} ${f - 160})`}>{[0, 1, 2, 3].map((k) => <rect key={k} x={-k * 130 - 60} y={-70} width={120} height={60} rx={8} fill={k ? '#9AA6B8' : GOLD} stroke={OL} strokeWidth={4} />)}</g>
        {plaque(900, f - 250, 'FEWER RAILWAYS', '#FFFFFF', 20)}</g>}
      {/* highway */}
      <rect x={z.x0} y={f - 100} width={z.x1 - z.x0} height={800} fill="#8F9AA8" /><rect x={z.x0} y={f - 100} width={z.x1 - z.x0} height={14} fill="#C9CED6" stroke={OL} strokeWidth={4} />
      {Array.from({length: 30}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 220 - ((t * 200) % 220)} y={f + 50} width={110} height={12} fill="#FFFFFF" />)}
      {Array.from({length: 10}, (_, k) => { const u = clamp(n - k); if (u <= 0) return null; return <g key={'tq' + k} opacity={u}>{truck(1520 - k * 300 + Math.sin(t * 2 + k) * 6, f + 20, 0.9, [RED, BLUE, GREEN, ORANGE, TEAL][k % 5], 'rq' + k)}</g>; })}
      <g transform={`translate(260 ${f - 160})`}><path d="M 0 0 L 0 -160" stroke={OL} strokeWidth={8} /><rect x={-120} y={-260} width={240} height={110} rx={8} fill={GREEN} stroke={OL} strokeWidth={5} /><T x={0} y={-212} s={26} c="#FFFFFF">{z.km1 || 'PORT  ➜'}</T><T x={0} y={-172} s={22} c="#FFFFFF">{z.km2 || 'A LONG WAY'}</T></g>
      {z.plaque && plaque(960, 330, z.plaque, '#FFFFFF', 26)}
    </g>;
  },

  /** the bank and its rate gauge */
  brbank: (t, z, f) => {
    const rate = kf(z.rate, t, 0.8), a = lerp(-80, 80, rate) + Math.sin(t * 9) * 1.5 * rate;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#EAF1EA" />
      {Array.from({length: 7}, (_, k) => <rect key={'cl' + k} x={z.x0 + 100 + k * 520} y={120} width={60} height={f - 120} fill="#FFFFFF" stroke={OL} strokeWidth={5} />)}
      <g transform="translate(960 560)"><path d="M -360 0 A 360 360 0 0 1 360 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        <path d="M -330 0 A 330 330 0 0 1 -165 -286" stroke={GREEN} strokeWidth={36} fill="none" /><path d="M -165 -286 A 330 330 0 0 1 165 -286" stroke={GOLD} strokeWidth={36} fill="none" /><path d="M 165 -286 A 330 330 0 0 1 330 0" stroke={RED} strokeWidth={36} fill="none" />
        <g transform={`rotate(${a})`}><path d="M -14 0 L 0 -300 L 14 0 Z" fill={NAVY} stroke={OL} strokeWidth={4} /></g><circle r={30} fill={GOLD} stroke={OL} strokeWidth={6} />
        <T x={-300} y={50} s={26} c={GREEN}>CHEAP</T><T x={300} y={50} s={26} c={RED}>PRICEY</T>
        {plaque(0, -400, z.title || 'THE PRICE OF A LOAN', GOLD, 30)}{z.rateText && <T x={0} y={110} s={54} c={NAVY} st="#FFFFFF" sw={10}>{z.rateText}</T>}</g>
      <g transform={`translate(400 ${f})`}><rect x={-200} y={-180} width={400} height={180} fill="#B07A4A" stroke={OL} strokeWidth={6} />{[0, 1, 2].map((q) => <rect key={q} x={-140 + q * 90} y={-206 - q * 4} width={110} height={26} rx={4} fill={PAPER} stroke={OL} strokeWidth={3} transform={`rotate(${q * 4 - 4})`} />)}{plaque(0, -90, 'LOANS', '#FFFFFF', 22)}</g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C9D3C4" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#A9B5A3" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** a big car plant in Bahia: quiet, then busy */
  brplant: (t, z, f) => {
    const busy = kf(z.busy, t, 1), sign: string = pick(z.sign, t, '');
    return <g>
      {sky(z, f, lerp(0, 1, busy) > 0.5 ? '#7EC8F2' : '#A9C4D6', '#FFF3DE', 'brps' + (z.ox ?? 0))}
      {palm(160, f, 1.0, t, 'p1')}{palm(1820, f, 1.0, t, 'p2')}
      <g transform={`translate(960 ${f})`}><rect x={-700} y={-380} width={1400} height={380} fill={busy > 0.5 ? '#E9EEF5' : '#C9CED6'} stroke={OL} strokeWidth={7} />
        {Array.from({length: 8}, (_, k) => <path key={k} d={`M ${-700 + k * 175} -380 l 88 -70 l 88 70 Z`} fill={busy > 0.5 ? '#BFE6F7' : '#9AA6B8'} stroke={OL} strokeWidth={5} />)}
        {Array.from({length: 7}, (_, k) => <rect key={'wd' + k} x={-640 + k * 190} y={-320} width={130} height={110} fill={busy > 0.5 ? '#FFE9A8' : '#8C99AB'} stroke={OL} strokeWidth={4} opacity={0.6 + 0.4 * busy} />)}
        <rect x={-180} y={-180} width={360} height={180} fill="#5E6B85" stroke={OL} strokeWidth={6} />
        <rect x={-170} y={-170} width={340} height={170 * (1 - busy)} fill="#9AA6B8" stroke={OL} strokeWidth={3} />
        {sign && <g transform="translate(0 -420)"><rect x={-360} y={-46} width={720} height={80} rx={10} fill={busy > 0.5 ? NAVY : '#5E6B85'} stroke={OL} strokeWidth={5} /><T x={0} y={12} s={fit(sign, 680, 40)} c={busy > 0.5 ? GOLD : '#FFFFFF'}>{sign}</T></g>}</g>
      {busy < 0.5 && Array.from({length: 6}, (_, k) => <path key={'dst' + k} d={`M ${400 + k * 200 + ((t * 30) % 60)} ${f - 20} q 30 -30 60 0`} stroke="#C9B79C" strokeWidth={6} fill="none" opacity={0.7 * (1 - busy * 2)} />)}
      {busy > 0.5 && Array.from({length: 5}, (_, k) => { const x = 960 + (((t * 200) + k * 360) % 1300); return <g key={'car' + k} transform={`translate(${x} ${f + 90})`} opacity={clamp((busy - 0.5) * 2)}>
        <path d="M -90 0 L -90 -40 Q -60 -80 0 -80 Q 60 -80 80 -40 L 100 -40 L 100 0 Z" fill={[BLUE, RED, '#FFFFFF', GREEN, GOLD][k]} stroke={OL} strokeWidth={5} /><circle cx={-50} cy={0} r={20} fill={OL} /><circle cx={60} cy={0} r={20} fill={OL} /></g>; })}
      {ground(z, f, '#B9D88F', '#98C06E')}
      <rect x={z.x0} y={f + 40} width={z.x1 - z.x0} height={100} fill="#8F9AA8" />
    </g>;
  },

  /** an airport gate */
  brgate: (t, z, f) => {
    const pl = kf(z.plane, t, 0.2);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E8EDF3" />
      <rect x={120} y={90} width={1680} height={560} rx={12} fill="#9ED8FF" stroke={OL} strokeWidth={6} />
      {Array.from({length: 8}, (_, k) => <path key={'mul' + k} d={`M ${120 + k * 240} 90 L ${120 + k * 240} 650`} stroke={OL} strokeWidth={6} />)}
      <rect x={120} y={540} width={1680} height={110} fill="#A9B5A3" />
      <g transform={`translate(${lerp(1500, 300, pl)} 520)`}><path d="M -260 0 Q -280 -50 -200 -50 L 220 -50 Q 270 -40 280 -10 Q 260 10 220 10 L -200 10 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <path d="M -40 -40 L 60 -140 L 110 -140 L 60 -40 Z M -200 -50 L -240 -130 L -200 -130 L -150 -50 Z" fill={TEAL} stroke={OL} strokeWidth={4} />{[0, 1, 2, 3, 4, 5].map((q) => <circle key={q} cx={-140 + q * 50} cy={-26} r={8} fill="#BFE6F7" stroke={OL} strokeWidth={2} />)}</g>
      <g transform="translate(1500 300)"><rect x={-230} y={-90} width={460} height={180} rx={10} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={0} y={-30} s={26} c={GOLD}>DEPARTURES</T><T x={0} y={30} s={fit(z.board || 'BOARDING', 420, 32)} c="#FFFFFF">{z.board || 'BOARDING'}</T></g>
      <g transform={`translate(420 ${f})`}><rect x={-160} y={-200} width={320} height={200} fill="#8A6236" stroke={OL} strokeWidth={5} /><path d="M -180 -260 L 180 -260 L 150 -200 L -150 -200 Z" fill={GREEN} stroke={OL} strokeWidth={5} /><T x={0} y={-218} s={24} c="#FFFFFF">CAFÉ</T>
        {[0, 1, 2].map((q) => <g key={q} transform={`translate(${-80 + q * 80} -210)`}><rect x={-18} y={-40} width={36} height={40} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><path d={`M -6 -50 q 6 -${10 + 4 * Math.sin(t * 3 + q)} 0 -24`} stroke="#B0BEC5" strokeWidth={3} fill="none" /></g>)}</g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C9CED6" />{Array.from({length: 20}, (_, k) => <path key={'tl' + k} d={`M ${z.x0 + k * 200} ${f} l 0 700`} stroke="#B3BAC4" strokeWidth={4} />)}
    </g>;
  },

  /** title card */
  brtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['COULD BRAZIL BECOME', "THE WORLD'S FACTORY", 'FOR ROBOTS?'];
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#E9F6EC" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(960 1000) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#D4EEDB' : '#FFF6D2'} />)}
      {hills({set: '', x0: -200, x1: 2200}, 1000, '#4FB360', 4, 200)}
      <circle cx={1600} cy={260} r={90} fill={GOLD} stroke={OL} strokeWidth={6} />
      {turbine(260, 1000, 0.9, t, 1)}{turbine(420, 1000, 0.7, t, 2)}
      <g transform="translate(960 960)">{arm(0, 0, 1.4, t * 0.5, 3)}</g>
      <g transform={`translate(1500 ${lerp(700, 960, E.outBack(win(t, 1.6, 0.6)))})`}>{minibot(0, 0, 2.2, 'tb')}</g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.55) / 0.5) * ln.length);
        return <T key={k} x={960} y={190 + k * 135} s={fit(ln, 1500, k === lines.length - 1 ? 130 : 100)} c={k === lines.length - 1 ? GREEN : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={960} y={620} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a brick thumps into the backpack */
  brbumper: (t, z, f) => {
    const c = z.color || GREEN, drop = lerp(-400, 0, E.inOut(win(t, 0.2, 0.5))), sq = t > 0.7 ? 1 - 0.12 * Math.exp(-(t - 0.7) * 6) * Math.cos((t - 0.7) * 30) : 1;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g transform={`translate(960 900) scale(${2 - sq} ${sq})`}><rect x={-150} y={-230} width={300} height={230} rx={50} fill="#C8643B" stroke={OL} strokeWidth={7} /><rect x={-110} y={-150} width={220} height={90} rx={20} fill="#A94E2C" stroke={OL} strokeWidth={5} />
        <path d="M -100 -230 Q 0 -300 100 -230" stroke={OL} strokeWidth={10} fill="none" /></g>
      {t < 0.75 && <g transform={`translate(960 ${700 + drop})`}><rect x={-80} y={-46} width={160} height={92} rx={8} fill="#9AA6B8" stroke={OL} strokeWidth={6} /><T x={0} y={14} s={36} c={NAVY}>+1</T></g>}
      {t >= 0.7 && t < 1.3 && <T x={960} y={640} s={70} c="#FFFFFF" st={OL} sw={8} o={1 - clamp((t - 1.0) / 0.3)}>THUNK!</T>}
      <g opacity={clamp((t - 0.5) / 0.3)}><T x={960} y={220} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={300} width={1200} height={140} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={960} y={392} s={fit(z.title || '', 1140, 62)} c={GOLD}>{z.title || ''}</T>
        {t >= 1.2 && <T x={960} y={530} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.2) / 0.3)}>{z.caption || ''}</T>}</g>
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const BRAZIL_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

/** costpack: the cost backpack. Bricks drop in (`drops` [[t, label]]) and can be pulled out (`pulls` [t...]). */
const costpack: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = kf(a.scale, t, 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const drops: [number, string][] = a.drops || [], pulls: number[] = a.pulls || [], base: string[] = a.base || [];
  const inBag: {label: string; t0: number}[] = base.map((l) => ({label: l, t0: -99}));
  for (const [dt, lab] of drops) if (t >= dt) inBag.push({label: lab, t0: dt});
  let pulled = 0, lastPull = -99; for (const p of pulls) if (t >= p) { pulled++; lastPull = p; }
  const n = Math.max(0, inBag.length - pulled), lastDrop = drops.length ? Math.max(-99, ...drops.filter((d) => t >= d[0]).map((d) => d[0])) : -99;
  const thunk = t - lastDrop < 0.6 ? Math.exp(-(t - lastDrop) * 7) * Math.cos((t - lastDrop) * 34) : 0;
  const sy = 1 - 0.16 * thunk, sx = 1 + 0.12 * thunk, bulge = 1 + Math.min(n, 6) * 0.07;
  return <g key={'cp' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <g transform={`scale(${sx * bulge} ${sy})`}>
      <path d="M -70 -250 Q 0 -320 70 -250" stroke={OL} strokeWidth={12} fill="none" />
      <rect x={-110} y={-260} width={220} height={260} rx={44} fill={CLAY} stroke={OL} strokeWidth={7} />
      <rect x={-84} y={-120} width={168} height={90} rx={18} fill={CLAY2} stroke={OL} strokeWidth={5} />
      <T x={0} y={-150} s={20} c="#FFFFFF">COST BACKPACK</T>
    </g>
    {inBag.slice(0, n).map((b, k) => { const fall = b.t0 > -50 ? clamp((t - b.t0) / 0.35) : 1, yy = -280 - k * 58 - (1 - E.inOut(fall)) * 500;
      return <g key={'bk' + k} transform={`translate(${(k % 2 ? 8 : -8)} ${yy}) rotate(${k % 2 ? 3 : -3})`} opacity={fall > 0 ? 1 : 0}>
        <rect x={-100} y={-26} width={200} height={52} rx={6} fill="#9AA6B8" stroke={OL} strokeWidth={5} /><T x={0} y={10} s={fit(b.label, 180, 24)} c={NAVY}>{b.label}</T></g>; })}
    {lastPull > -50 && t - lastPull < 1.2 && <g transform={`translate(${140 + 200 * (t - lastPull)} ${-300 - 160 * (t - lastPull)}) rotate(${(t - lastPull) * 60})`} opacity={1 - clamp((t - lastPull - 0.7) / 0.5)}>
      <rect x={-100} y={-26} width={200} height={52} rx={6} fill="#C5CDD8" stroke={OL} strokeWidth={5} /><T x={0} y={10} s={22} c={GREEN}>LIGHTER!</T></g>}
    {t - lastDrop < 1.0 && <T x={150} y={-200} s={44} c={RED} st="#FFFFFF" sw={8} o={1 - clamp((t - lastDrop - 0.5) / 0.5)}>THUNK!</T>}
    {a.label && t < (a.labelUntil ?? at + 3) && plaque(0, -360 - n * 58, a.label, '#FFFFFF', 20)}
  </g>;
};

export const BRAZIL_ITEMS: Record<string, ItemFn> = {costpack};
export const BRAZIL_INDOOR = ['brhq', 'brfab', 'brcounter', 'brbank', 'brgate', 'brtitle', 'brbumper'];
