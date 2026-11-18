import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * SHOVELS kit for CartoonStage (Episode 68, "The Countries That Could Win the AI Economy Without Building AI").
 *
 * Picks-and-shovels for nations, drawn in the channel's prime-time cartoon GENRE (thick clean outlines, flat colour, squash and
 * stretch, sunny day scenes). Cast (fictional, drawn with the shared `toon` rig): HATTIE, a gold-country hardware-store owner; and
 * NUGGET (item `nugget`), a talking AI chip with a passport. Everything ORIGINAL: no logos, no flags, no brand names on buildings;
 * companies appear only as generic buildings with plain plaques when the narration names them; countries are landscapes
 * (green hills, flat polders, hillside cities, deserts, mountains), never flags or stereotypes. No real person is drawn.
 * Sets:
 *  - svcreek: 1849 gold-field hills: a creek, tents, little miners panning (most find mud; one glint), a rush of tiny prospectors
 *    walking in (`rush` KF 0..1), `glint` t when one pan shines.
 *  - svstore: the general store. `era` '1849' (false-front timber store, shovel rack, barrels, coins stacking on the counter
 *    `coins` KF 0..12, a queue of miners `queue` KF 0..8) | 'today' (Hattie's hardware store: same false front, repainted, pickup
 *    truck, `motto` painted above the door, a parcel that lands on the counter `pkg` t). `sign` text.
 *  - svmap: a parchment treasure map (original stylized continents): `stamps` [{x, y, label, c, at}] thump on, `route` KF 0..n a
 *    dotted trail drawn stamp to stamp with a little balloon riding it, `hi` [[t, idx]] pulses a stamp, `title`.
 *  - svfoundry: green layered hills + a river, a long clean fab with glowing windows, a service window (`plaque`), a customer queue of
 *    crates on legs (`queue` KF 0..8, labelled "DESIGN"), wafers rolling out on a conveyor (`wafers` KF 0..1 speed), `glow` KF.
 *  - svpolder: a flat polder: big sky, canals, a low high-tech hall, a giant crate that opens (`crate` KF 0..1) to show a boxy
 *    light machine, a bus beside it for scale (`bus`), cargo planes taking off with pieces (`planes` KF 0..3), `plaque`.
 *  - svmemory: a hillside city with a fab; a giant HBM "pancake" tower dropping layers onto a chip base (`layers` KF 0..12),
 *    syrup drip gag (`syrup` t), `plaque`.
 *  - svlab: a bright precision workshop: bottle shelves that fill (`bottles` KF 0..24), a spin-coater with a spinning wafer, gas
 *    cylinders, wafers riding out to trucks (`out` KF 0..1), `plaque`.
 *  - svdesert: dunes and solar rows (`solar` KF 0..1), a glass vault (`vault` KF 0..1 doors open) whose coins arc out to data halls
 *    and over the horizon (`cash` KF 0..1), data halls appearing (`halls` KF 0..5), `plaque`.
 *  - svmine: `variant` 'andes' (snowy peaks, terraced copper pit, haul trucks, cathode stack) | 'outback' (red earth, lithium pit,
 *    white bags); `trucks` KF 0..1 speed, `stock` KF 0..10, a price gauge (`gauge` KF -1..1), `plaque`.
 *  - svledger: Hattie's chalkboard scorecard: `rows` [{label, at, mark: 'yes' | 'no' | 'maybe' | 'ride'}], `title`.
 *  - svtitle / svbumper: the title card (a golden shovel whose blade is a chip digs and flips coins) and chapter bumpers (a shovel
 *    digs, a signpost pops up with the chapter title).
 * Items: nugget (NUGGET: a gold AI chip with pin legs, an LED face and a passport; `x` KF, `y`, `face`/`faces` [[t, face]]
 *  (happy | worry | wow | grin), `hops` [t...], `passport` true, `talk` [[t0, t1]]), shovel (`x`, `y`, `rot`, `gold`, `chip`),
 *  svpass (an open passport, `stamps` [{label, c, at}] thump in), svcoin (a coin shower from `x`,`y`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#1E2233';
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
const jig = (t: number, at: number, k = 14, d = 5) => (t < at ? 0 : Math.exp(-d * (t - at)) * Math.sin(k * (t - at)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.6);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#2F7DE1', GOLD = '#E8A317', GOLD2 = '#FFD45C', RED = '#E5483B', GREEN = '#2E9E6B', PURPLE = '#7357C9', NAVY = '#1E2233',
  COPPER = '#D9773A', CY = '#29C5F6', WOOD = '#B9814A', WOOD2 = '#8A5A2B', SAND = '#F2D49B', WATER = '#5AB4E8';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const sun = (x: number, y: number, t: number, r = 70) => <g transform={`translate(${x} ${y})`}>
  {Array.from({length: 12}, (_, k) => <path key={k} transform={`rotate(${k * 30 + t * 8})`} d={`M 0 ${-r - 14} L 0 ${-r - 44}`} stroke={GOLD2} strokeWidth={8} strokeLinecap="round" />)}
  <circle r={r} fill={GOLD2} stroke={OL} strokeWidth={5} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'svc' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const clouds = (z: Z, t: number, n = 6, y0 = 120) => <g>{Array.from({length: n}, (_, k) => cloud(z.x0 + ((k * 520 + t * (10 + k * 3)) % Math.max(600, z.x1 - z.x0)), y0 + (k % 3) * 70, 0.6 + (k % 3) * 0.2, k))}</g>;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const ridge = (x0: number, x1: number, base: number, amp: number, per: number, seed: number) => {
  let d = `M ${x0} ${base + 400} L ${x0} ${base}`;
  for (let x = x0; x <= x1 + per; x += per / 2) d += ` Q ${x - per / 4} ${base - amp * (0.4 + 0.6 * rnd(seed + Math.round(x / per * 2)))} ${x} ${base - amp * (0.2 + 0.5 * rnd(seed + 7 + Math.round(x / per * 2)))}`;
  return d + ` L ${x1 + per} ${base + 400} Z`;
};
const peaks = (x0: number, x1: number, base: number, amp: number, per: number, seed: number) => {
  let d = `M ${x0} ${base + 400} L ${x0} ${base}`;
  for (let x = x0; x <= x1 + per; x += per / 2) d += ` L ${x} ${base - amp * (0.35 + 0.65 * rnd(seed + Math.round(x / per * 2)))}`;
  return d + ` L ${x1 + per} ${base + 400} Z`;
};
const ground = (z: Z, f: number, c = '#B9D98F', c2 = '#97BF6E') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
/** a shovel drawn upright at (x, y) = bottom of blade */
const shovelG = (x: number, y: number, s: number, rot: number, k: any, gold = false, chip = false, t = 0) => <g key={'shv' + k} transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
  <rect x={-7} y={-330} width={14} height={240} rx={6} fill={gold ? GOLD : WOOD} stroke={OL} strokeWidth={4} />
  <path d="M -30 -350 L 30 -350 L 30 -330 L -30 -330 Z M -30 -350 Q 0 -380 30 -350" fill={gold ? GOLD2 : WOOD2} stroke={OL} strokeWidth={4} />
  <path d="M -50 -100 L 50 -100 L 48 -30 Q 0 20 -48 -30 Z" fill={gold ? GOLD2 : '#B0BEC5'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
  {chip && <g><rect x={-28} y={-88} width={56} height={52} rx={6} fill="#263238" stroke={OL} strokeWidth={3} />
    {[0, 1, 2].map((q) => <path key={q} d={`M ${-20 + q * 20} -88 L ${-20 + q * 20} -96 M ${-20 + q * 20} -36 L ${-20 + q * 20} -28`} stroke={OL} strokeWidth={3} />)}
    <rect x={-16} y={-76} width={32} height={28} rx={4} fill={CY} opacity={0.6 + 0.4 * Math.sin(t * 5)} /></g>}
  {gold && <path d={`M 30 -80 l 6 -14 l 6 14 l 14 6 l -14 6 l -6 14 l -6 -14 l -14 -6 Z`} fill="#FFFFFF" opacity={0.5 + 0.5 * Math.sin(t * 6 + Number(String(k).length))} />}
</g>;
const coin = (x: number, y: number, s: number, k: any, t = 0) => <g key={'cn' + k} transform={`translate(${x} ${y}) scale(${s * (0.6 + 0.4 * Math.abs(Math.cos(t * 6 + Number(String(k).length))))} ${s})`}>
  <circle r={22} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={9} s={24} c={WOOD2}>$</T></g>;
const tinyMiner = (x: number, y: number, s: number, k: number, t: number, mode: 'walk' | 'pan' | 'shovel') => {
  const sw = Math.sin(t * 8 + k), skin = ['#F1C9A5', '#C98B5B', '#8D5A3B', '#E7B48F'][k % 4], shirt = ['#E5483B', '#2F7DE1', '#2E9E6B', '#7357C9', '#F08A24'][k % 5];
  return <g key={'mn' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d={mode === 'walk' ? `M -6 -40 L ${-10 + sw * 10} 0 M 6 -40 L ${10 - sw * 10} 0` : 'M -8 -40 L -16 0 M 8 -40 L 16 0'} stroke={OL} strokeWidth={7} strokeLinecap="round" />
    <rect x={-16} y={-92} width={32} height={56} rx={10} fill={shirt} stroke={OL} strokeWidth={4} />
    <circle cx={0} cy={-108} r={18} fill={skin} stroke={OL} strokeWidth={4} />
    <path d="M -26 -116 L 26 -116 L 18 -132 L -18 -132 Z" fill="#6D4C41" stroke={OL} strokeWidth={3} />
    {mode === 'pan' && <g transform={`translate(30 ${-40 + 4 * Math.sin(t * 6 + k)}) rotate(${10 * Math.sin(t * 6 + k)})`}><ellipse rx={30} ry={8} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g>}
    {mode !== 'pan' && <g transform={`translate(20 -50) rotate(${mode === 'shovel' ? -30 + 30 * Math.sin(t * 5 + k) : 20})`}><path d="M 0 0 L 0 -70" stroke={WOOD2} strokeWidth={5} /><path d="M -10 0 L 10 0 L 0 18 Z" fill="#B0BEC5" stroke={OL} strokeWidth={3} /></g>}
  </g>;
};

const RAW: Record<string, SetFn> = {
  /** 1849 gold-field hills with a creek */
  svcreek: (t, z, f) => {
    const rush = kf(z.rush, t, 0), glint = z.glint ?? -9;
    return <g>
      {sky(z, f, '#7EC8F2', '#FFF1D6', 'svcrsky')}{sun(1700, 180, t)}{clouds(z, t, 5)}
      <path d={ridge(z.x0, z.x1, 640, 220, 520, 3)} fill="#C9B27A" stroke={OL} strokeWidth={4} />
      <path d={ridge(z.x0, z.x1, 760, 160, 380, 9)} fill="#A8C47A" stroke={OL} strokeWidth={4} />
      {Array.from({length: 18}, (_, k) => { const x = z.x0 + 120 + k * 260, y = 700 - rnd(k) * 60; return <g key={'pn' + k} transform={`translate(${x} ${y})`}><path d="M 0 0 L -24 60 L 24 60 Z" fill="#3F7D4E" stroke={OL} strokeWidth={3} /><path d="M 0 30 L -30 100 L 30 100 Z" fill="#3F7D4E" stroke={OL} strokeWidth={3} /></g>; })}
      {ground(z, f, '#C8B48A', '#A99467')}
      <path d={`M ${z.x0} ${f + 120} Q 400 ${f + 60} 960 ${f + 140} T ${z.x1} ${f + 110} L ${z.x1} ${f + 230} Q 960 ${f + 260} ${z.x0} ${f + 220} Z`} fill={WATER} stroke={OL} strokeWidth={4} />
      {Array.from({length: 12}, (_, k) => <path key={'cw' + k} d={`M ${z.x0 + k * 300 + ((t * 40) % 300)} ${f + 170} q 20 -10 40 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" />)}
      {[300, 620, 1500, 1900].map((x, k) => <g key={'tn' + k} transform={`translate(${x} ${f + 4})`}><path d="M -70 0 L 0 -110 L 70 0 Z" fill={k % 2 ? '#F5EBD8' : '#EADBC0'} stroke={OL} strokeWidth={5} strokeLinejoin="round" /><path d="M 0 -110 L 0 0" stroke={OL} strokeWidth={3} /></g>)}
      {[460, 800, 1100, 1300, 1700].map((x, k) => tinyMiner(x, f + 130, 0.9, k, t, k === 2 ? 'shovel' : 'pan'))}
      {t > glint && t < glint + 1.6 && <g transform={`translate(1130 ${f + 80}) scale(${pop(t, glint, 0.3)})`}>{Array.from({length: 8}, (_, q) => <path key={q} transform={`rotate(${q * 45 + t * 60})`} d="M 0 -20 L 0 -60" stroke={GOLD2} strokeWidth={6} strokeLinecap="round" />)}<circle r={16} fill={GOLD2} stroke={OL} strokeWidth={4} /></g>}
      {rush > 0 && Array.from({length: 14}, (_, k) => { const u = clamp(rush * 1.4 - k * 0.04), x = lerp(z.x0 - 200, 300 + k * 110, u); return u > 0 ? tinyMiner(x, f + 20 + (k % 3) * 24, 0.75, k + 7, t, 'walk') : null; })}
    </g>;
  },

  /** the general store: 1849 or today */
  svstore: (t, z, f) => {
    const today = z.era === 'today', coins = Math.floor(kf(z.coins, t, 0)), q = Math.floor(kf(z.queue, t, 0));
    const sign: string = z.sign || (today ? "HATTIE'S HARDWARE" : 'GENERAL STORE');
    const pkg = z.pkg ?? -9, pk = t < pkg ? -900 : lerp(-900, 0, E.outBack(win(t, pkg, 0.7)));
    return <g>
      {sky(z, f, today ? '#8FD3F5' : '#9ED2EE', today ? '#EAF7FF' : '#FFF0D2', today ? 'svstsk2' : 'svstsk1')}{sun(1750, 170, t, 60)}{clouds(z, t, 5, 110)}
      <path d={ridge(z.x0, z.x1, 700, 140, 420, 21)} fill={today ? '#A8CF8A' : '#CDB884'} stroke={OL} strokeWidth={4} />
      {ground(z, f, today ? '#C9C3B5' : '#D7BE8E', today ? '#AFA796' : '#B89C6C')}
      {/* the store */}
      <g transform="translate(560 0)">
        <rect x={-380} y={f - 520} width={760} height={520} fill={today ? '#E9D3B0' : WOOD} stroke={OL} strokeWidth={7} />
        <path d={`M -420 ${f - 520} L -420 ${f - 640} L 420 ${f - 640} L 420 ${f - 520} Z`} fill={today ? '#C84B3A' : WOOD2} stroke={OL} strokeWidth={7} />
        {!today && Array.from({length: 12}, (_, k) => <path key={'pl' + k} d={`M ${-380 + k * 64} ${f - 520} L ${-380 + k * 64} ${f}`} stroke={WOOD2} strokeWidth={3} opacity={0.6} />)}
        <T x={0} y={f - 562} s={fit(sign, 780, 58)} c="#FFF3D6" st={OL} sw={6}>{sign}</T>
        {today && z.motto && <g><rect x={-300} y={f - 500} width={600} height={70} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={f - 452} s={fit(z.motto, 560, 34)} c={GOLD}>{z.motto}</T></g>}
        <rect x={-340} y={f - 410} width={260} height={220} fill="#BFE6F7" stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3, 4].map((k) => shovelG(-310 + k * 50, f - 200, 0.5, -4 + k * 2, 'win' + k, false, false, t))}
        <rect x={-40} y={f - 360} width={160} height={360} fill={today ? '#7A4E2D' : '#5D3A1E'} stroke={OL} strokeWidth={6} />
        <circle cx={90} cy={f - 180} r={9} fill={GOLD2} stroke={OL} strokeWidth={3} />
        <rect x={160} y={f - 410} width={200} height={220} fill="#BFE6F7" stroke={OL} strokeWidth={6} />
        <path d={`M -400 ${f - 30} L 400 ${f - 30} L 400 ${f} L -400 ${f} Z`} fill={WOOD2} stroke={OL} strokeWidth={5} />
        {/* porch counter with coins */}
        <rect x={180} y={f - 150} width={240} height={120} fill={WOOD} stroke={OL} strokeWidth={5} />
        {Array.from({length: coins}, (_, k) => coin(220 + (k % 4) * 52, f - 168 - Math.floor(k / 4) * 22, 0.8, 'pc' + k, t))}
        {pkg > 0 && t >= pkg && <g transform={`translate(300 ${f - 200 + pk})`}><rect x={-60} y={-70} width={120} height={80} fill="#D7A86E" stroke={OL} strokeWidth={5} /><path d="M -60 -40 L 60 -40 M 0 -70 L 0 10" stroke="#8D6E63" strokeWidth={6} />
          {t > pkg + 0.6 && t < pkg + 1.1 && <T x={0} y={-90} s={34} c={RED} o={1 - win(t, pkg + 0.6, 0.5)}>THUMP!</T>}</g>}
      </g>
      {/* rack of shovels and barrels outside */}
      {Array.from({length: 7}, (_, k) => shovelG(1050 + k * 46, f + 6, 0.7, -6 + k * 2, 'rk' + k, false, false, t))}
      <rect x={1030} y={f - 120} width={340} height={14} fill={WOOD2} stroke={OL} strokeWidth={4} />
      {[1450, 1560].map((x, k) => <g key={'br' + k}><ellipse cx={x} cy={f - 6} rx={46} ry={12} fill={WOOD2} /><path d={`M ${x - 44} ${f} L ${x - 50} ${f - 110} L ${x + 50} ${f - 110} L ${x + 44} ${f} Z`} fill={WOOD} stroke={OL} strokeWidth={5} /><path d={`M ${x - 48} ${f - 40} L ${x + 48} ${f - 40} M ${x - 50} ${f - 80} L ${x + 50} ${f - 80}`} stroke={OL} strokeWidth={4} /></g>)}
      {today && <g transform={`translate(1850 ${f})`}><rect x={-200} y={-120} width={400} height={80} rx={14} fill={BLUE} stroke={OL} strokeWidth={6} /><path d="M -120 -120 L -80 -190 L 60 -190 L 90 -120 Z" fill="#BFE6F7" stroke={OL} strokeWidth={6} />
        {[-120, 120].map((x) => <circle key={x} cx={x} cy={-30} r={38} fill="#37474F" stroke={OL} strokeWidth={6} />)}</g>}
      {!today && Array.from({length: q}, (_, k) => tinyMiner(1000 - k * 90 - (k > 0 ? 40 * Math.sin(t * 2 + k) * 0 : 0), f + 20, 1.1, k + 3, t + k * 0.3, 'walk'))}
    </g>;
  },

  /** the parchment treasure map */
  svmap: (t, z, f) => {
    const st: any[] = z.stamps || [], r = kf(z.route, t, 0), hi = Number(pick(z.hi, t, -1));
    const LAND = ['M 180 240 Q 320 130 520 160 Q 640 200 600 320 Q 560 400 460 450 Q 400 480 360 440 Q 280 380 230 330 Q 160 290 180 240 Z',
      'M 560 520 Q 650 500 720 560 Q 740 680 680 800 Q 640 850 610 790 Q 580 670 560 520 Z', 'M 900 190 Q 1000 150 1080 190 Q 1100 250 1040 290 Q 980 300 930 280 Q 890 240 900 190 Z',
      'M 940 340 Q 1060 330 1110 410 Q 1130 520 1070 620 Q 1010 690 980 610 Q 940 510 920 420 Z', 'M 1120 190 Q 1380 120 1660 190 Q 1740 280 1650 360 Q 1520 420 1380 400 Q 1230 380 1150 320 Q 1100 250 1120 190 Z',
      'M 1560 620 Q 1680 590 1760 650 Q 1740 730 1640 740 Q 1560 710 1560 620 Z'];
    let d = ''; st.forEach((s, k) => { d += `${k ? 'L' : 'M'} ${s.x} ${s.y} `; });
    const segs = Math.max(1, st.length - 1), u = clamp(r / segs);
    const ki = Math.min(st.length - 2, Math.floor(r)), fr = r - Math.floor(r);
    const bx = st.length > 1 ? (r >= segs ? st[st.length - 1].x : lerp(st[Math.max(0, ki)].x, st[Math.max(0, ki) + 1].x, E.inOut(clamp(fr)))) : 0;
    const by = st.length > 1 ? (r >= segs ? st[st.length - 1].y : lerp(st[Math.max(0, ki)].y, st[Math.max(0, ki) + 1].y, E.inOut(clamp(fr)))) : 0;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#8A5A2B" />
      <g transform={`rotate(${-1 + 0.3 * Math.sin(t * 0.7)} 960 540)`}>
        <path d="M 60 60 L 1860 50 Q 1880 300 1850 540 Q 1880 800 1860 1030 L 70 1040 Q 40 800 60 540 Q 30 300 60 60 Z" fill="#F6E7C1" stroke={OL} strokeWidth={8} />
        {Array.from({length: 30}, (_, k) => <circle key={'sp' + k} cx={100 + rnd(k) * 1720} cy={100 + rnd(k + 40) * 880} r={6 + rnd(k + 9) * 18} fill="#E9D3A0" opacity={0.6} />)}
        {Array.from({length: 22}, (_, k) => <path key={'wv' + k} d={`M ${120 + (k * 190) % 1700} ${130 + ((k * 137) % 820)} q 14 -8 28 0 q 14 8 28 0`} stroke="#9DC3D6" strokeWidth={3} fill="none" />)}
        {LAND.map((p, k) => <path key={'ld' + k} d={p} fill="#CFE3A8" stroke="#6B5A3A" strokeWidth={5} />)}
        <g transform="translate(1720 900)"><circle r={60} fill="none" stroke="#6B5A3A" strokeWidth={4} /><path d="M 0 -70 L 12 0 L 0 70 L -12 0 Z" fill={RED} stroke={OL} strokeWidth={3} transform={`rotate(${8 * Math.sin(t)})`} /><T x={0} y={-80} s={24} c="#6B5A3A">N</T></g>
        {st.length > 1 && <path d={d} stroke={RED} strokeWidth={8} fill="none" pathLength={1000} strokeDasharray={`${u * 1000} 1000`} />}
        {st.map((s, k) => { const p = pop(t, s.at ?? 0, 0.35); if (p <= 0) return null; const hh = hi === k ? 1 + 0.12 * Math.sin(t * 10) : 1, land = jig(t, s.at ?? 0, 22, 7);
          return <g key={'st' + k} transform={`translate(${s.x} ${s.y}) rotate(${-8 + (k % 3) * 6}) scale(${p * hh * (1 - 0.15 * land)})`}>
            <rect x={-92} y={-50} width={184} height={100} rx={12} fill="#FFFFFF" fillOpacity={0.75} stroke={s.c || RED} strokeWidth={7} strokeDasharray="4 6" />
            <T x={0} y={-6} s={fit(s.label || '', 170, 30)} c={s.c || RED}>{s.label}</T><T x={0} y={30} s={18} c={s.c || RED}>{s.sub || 'SHOVEL SHOP'}</T></g>; })}
        {st.length > 1 && r > 0 && <g transform={`translate(${bx} ${by - 70 + 8 * Math.sin(t * 3)})`}><path d="M -14 40 L -22 8 M 14 40 L 22 8" stroke={OL} strokeWidth={3} />
          <path d="M 0 -50 Q 46 -50 46 -6 Q 46 22 16 40 L -16 40 Q -46 22 -46 -6 Q -46 -50 0 -50 Z" fill={GOLD2} stroke={OL} strokeWidth={4} /><path d="M -16 -48 Q -24 0 -10 40 M 16 -48 Q 24 0 10 40" stroke={GOLD} strokeWidth={4} fill="none" />
          <rect x={-14} y={40} width={28} height={20} fill={WOOD} stroke={OL} strokeWidth={3} /></g>}
        {z.title && <g><rect x={560} y={70} width={800} height={86} rx={16} fill={WOOD2} stroke={OL} strokeWidth={6} /><T x={960} y={130} s={fit(z.title, 760, 44)} c="#FFF3D6">{z.title}</T></g>}
      </g>
    </g>;
  },

  /** Taiwan-style green hills with a long clean foundry */
  svfoundry: (t, z, f) => {
    const q = kf(z.queue, t, 0), wv = kf(z.wafers, t, 0), glow = kf(z.glow, t, 1);
    return <g>
      {sky(z, f, '#7CCBF2', '#E9F8FF', 'svfdsk')}{sun(260, 160, t, 55)}{clouds(z, t, 6, 120)}
      <path d={ridge(z.x0, z.x1, 560, 260, 460, 31)} fill="#6FB36E" stroke={OL} strokeWidth={4} />
      <path d={ridge(z.x0, z.x1, 680, 180, 340, 37)} fill="#8CCB7A" stroke={OL} strokeWidth={4} />
      {ground(z, f, '#B9D98F', '#97BF6E')}
      <path d={`M ${z.x0} ${f + 150} Q 600 ${f + 110} 1200 ${f + 170} T ${z.x1} ${f + 150} L ${z.x1} ${f + 230} L ${z.x0} ${f + 230} Z`} fill={WATER} stroke={OL} strokeWidth={4} />
      <g transform={`translate(1150 ${f})`}>
        <rect x={-560} y={-330} width={1120} height={330} fill="#EEF2F7" stroke={OL} strokeWidth={7} />
        <rect x={-560} y={-370} width={1120} height={40} fill="#C9D3E0" stroke={OL} strokeWidth={6} />
        {Array.from({length: 14}, (_, k) => <rect key={'fw' + k} x={-530 + k * 78} y={-300} width={58} height={90} rx={6} fill={CY} opacity={0.35 + 0.5 * glow * (0.6 + 0.4 * Math.sin(t * 3 + k))} stroke={OL} strokeWidth={3} />)}
        {Array.from({length: 6}, (_, k) => <g key={'fn' + k} transform={`translate(${-470 + k * 190} -390)`}><rect x={-34} y={-14} width={68} height={24} fill="#B9C3D1" stroke={OL} strokeWidth={3} /><g transform={`rotate(${t * 300 + k * 30})`}><path d="M -20 0 L 20 0 M 0 -8 L 0 8" stroke={OL} strokeWidth={3} /></g></g>)}
        <rect x={-560} y={-150} width={300} height={150} fill="#D9E2EC" stroke={OL} strokeWidth={6} />
        <path d="M -580 -150 L -240 -150 L -260 -190 L -560 -190 Z" fill={BLUE} stroke={OL} strokeWidth={5} />
        <rect x={-520} y={-130} width={220} height={80} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        {z.plaque && plaque(0, -420, z.plaque, '#FFFFFF', 24)}
        {/* conveyor of wafers out of the right side */}
        <rect x={560} y={-80} width={560} height={26} fill="#90A4AE" stroke={OL} strokeWidth={4} />
        {wv > 0 && Array.from({length: 7}, (_, k) => { const u = ((t * 0.25 * wv + k / 7) % 1); return <g key={'wf' + k} transform={`translate(${580 + u * 520} -104)`}><ellipse rx={34} ry={12} fill="#B39DDB" stroke={OL} strokeWidth={3} /><ellipse rx={22} ry={7} fill="#E1F5FE" opacity={0.7} /></g>; })}
      </g>
      {/* customer queue: crates on legs labelled DESIGN */}
      {Array.from({length: Math.floor(q)}, (_, k) => { const x = 360 - k * 120, b = Math.abs(Math.sin(t * 5 + k)) * 6;
        return <g key={'cq' + k} transform={`translate(${x} ${f - b})`}><path d={`M -14 -6 L -18 0 M 14 -6 L 18 0`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
          <rect x={-46} y={-96} width={92} height={90} rx={8} fill={['#FFE082', '#B3E5FC', '#C8E6C9', '#F8BBD0', '#D1C4E9'][k % 5]} stroke={OL} strokeWidth={5} />
          <T x={0} y={-44} s={18} c={NAVY}>DESIGN</T><circle cx={-14} cy={-72} r={5} fill={OL} /><circle cx={14} cy={-72} r={5} fill={OL} /></g>; })}
    </g>;
  },

  /** a flat polder with the machine crate and cargo planes */
  svpolder: (t, z, f) => {
    const cr = kf(z.crate, t, 0), pl = kf(z.planes, t, 0);
    return <g>
      {sky(z, f, '#86C8F0', '#F1FAFF', 'svpdsk')}{sun(1600, 150, t, 55)}{clouds(z, t, 8, 110)}
      <rect x={z.x0} y={f - 120} width={z.x1 - z.x0} height={120} fill="#9FCF7E" stroke={OL} strokeWidth={4} />
      {Array.from({length: 9}, (_, k) => <path key={'cn' + k} d={`M ${z.x0 + k * 520} ${f - 118} L ${z.x0 + k * 520 - 140} ${f}`} stroke={WATER} strokeWidth={10} />)}
      {ground(z, f, '#B9D98F', '#97BF6E')}
      {[200, 2000].map((x, k) => <g key={'wt' + k} transform={`translate(${x} ${f - 110}) scale(0.6)`}><path d="M -8 0 L -4 -300 L 4 -300 L 8 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        <g transform={`translate(0 -300) rotate(${t * 70 + k * 40})`}>{[0, 120, 240].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 L -10 -20 L 0 -150 L 10 -20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} />)}<circle r={10} fill="#CFD8DC" stroke={OL} strokeWidth={4} /></g></g>)}
      {/* low high-tech hall */}
      <g transform={`translate(560 ${f})`}><rect x={-420} y={-220} width={840} height={220} fill="#F2F5F9" stroke={OL} strokeWidth={7} />
        <rect x={-420} y={-250} width={840} height={30} fill="#5C6BC0" stroke={OL} strokeWidth={5} />
        {Array.from({length: 9}, (_, k) => <rect key={'hw' + k} x={-390 + k * 90} y={-190} width={60} height={60} rx={6} fill="#BFE6F7" stroke={OL} strokeWidth={3} />)}
        {z.plaque && plaque(0, -300, z.plaque, '#FFFFFF', 24)}</g>
      {/* the crate / machine */}
      <g transform={`translate(1240 ${f})`}>
        <g opacity={cr > 0.05 ? 1 : 1}><rect x={-230} y={-300} width={460} height={300} rx={16} fill="#E7ECF3" stroke={OL} strokeWidth={7} />
          <rect x={-200} y={-270} width={220} height={200} rx={10} fill="#CFD8DC" stroke={OL} strokeWidth={5} /><rect x={40} y={-270} width={160} height={120} rx={10} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
          <path d={`M -90 -170 L ${-90 + 60 * Math.sin(t * 2)} -60`} stroke="#B388FF" strokeWidth={10} opacity={0.8} />
          {Array.from({length: 4}, (_, k) => <circle key={k} cx={80 + k * 30} cy={-110} r={8} fill={(k + Math.floor(t * 3)) % 2 ? GREEN : GOLD} />)}</g>
        {/* crate walls fall away */}
        {cr < 1 && <g><g transform={`translate(-250 0) rotate(${-90 * E.inOut(clamp(cr))})`}><rect x={0} y={-330} width={30} height={330} fill={WOOD} stroke={OL} strokeWidth={5} /></g>
          <g transform={`translate(250 0) rotate(${90 * E.inOut(clamp(cr))})`}><rect x={-30} y={-330} width={30} height={330} fill={WOOD} stroke={OL} strokeWidth={5} /></g>
          <g opacity={1 - clamp(cr * 1.6)}><rect x={-250} y={-330} width={500} height={330} fill={WOOD} stroke={OL} strokeWidth={7} />
            {Array.from({length: 6}, (_, k) => <path key={k} d={`M -250 ${-300 + k * 55} L 250 ${-300 + k * 55}`} stroke={WOOD2} strokeWidth={4} />)}
            <path d="M -250 -330 L 250 0 M 250 -330 L -250 0" stroke={WOOD2} strokeWidth={8} /><T x={0} y={-150} s={40} c="#FFF3D6" st={OL} sw={6}>FRAGILE</T></g></g>}
        {z.bus && <g transform="translate(-500 0)"><rect x={-170} y={-150} width={340} height={120} rx={20} fill={GOLD2} stroke={OL} strokeWidth={6} />
          {[0, 1, 2, 3].map((k) => <rect key={k} x={-150 + k * 76} y={-134} width={58} height={44} rx={6} fill="#BFE6F7" stroke={OL} strokeWidth={3} />)}
          {[-110, 110].map((x) => <circle key={x} cx={x} cy={-26} r={28} fill="#37474F" stroke={OL} strokeWidth={5} />)}<T x={0} y={-176} s={24} c={NAVY}>FOR SCALE: A BUS</T></g>}
      </g>
      {/* cargo planes */}
      {Array.from({length: 3}, (_, k) => { const u = clamp(pl - k); if (u <= 0) return null; const x = lerp(1600, 2700, E.in(u)), y = lerp(f - 60, f - 700, E.in(u));
        return <g key={'pl' + k} transform={`translate(${x} ${y}) rotate(${-20 * clamp(u * 3)})`}><path d="M -160 0 Q -160 -40 -80 -40 L 140 -40 Q 190 -30 200 0 Q 190 20 140 24 L -140 24 Q -170 20 -160 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <path d="M -20 -10 L -90 -100 L -50 -100 L 50 -10 Z" fill="#CFD8DC" stroke={OL} strokeWidth={4} /><path d="M -140 -30 L -170 -90 L -130 -90 L -100 -36 Z" fill="#CFD8DC" stroke={OL} strokeWidth={4} />
          <rect x={-60} y={-30} width={60} height={30} fill={WOOD} stroke={OL} strokeWidth={3} /></g>; })}
    </g>;
  },

  /** Korea-style hillside city + the HBM pancake tower */
  svmemory: (t, z, f) => {
    const n = Math.floor(kf(z.layers, t, 0)), sy = z.syrup ?? -9;
    return <g>
      {sky(z, f, '#80C9F1', '#EEF9FF', 'svmmsk')}{sun(1680, 160, t, 55)}{clouds(z, t, 5, 120)}
      <path d={ridge(z.x0, z.x1, 600, 240, 480, 51)} fill="#79B47A" stroke={OL} strokeWidth={4} />
      {Array.from({length: 10}, (_, k) => { const h = 200 + rnd(k + 60) * 220, x = z.x0 + 260 + k * 190; return x > 900 && x < 1500 ? null : <g key={'ap' + k}><rect x={x} y={f - h} width={110} height={h} fill={k % 2 ? '#E3E8EF' : '#D3DCE6'} stroke={OL} strokeWidth={4} />
        {Array.from({length: Math.floor(h / 50)}, (_, r) => <rect key={r} x={x + 18} y={f - h + 20 + r * 50} width={74} height={18} fill="#BFE6F7" stroke={OL} strokeWidth={2} />)}</g>; })}
      {ground(z, f, '#B9D98F', '#97BF6E')}
      {z.plaque && plaque(1200, 150, z.plaque, '#FFFFFF', 24)}
      <g transform={`translate(1200 ${f})`}>
        <rect x={-260} y={-60} width={520} height={60} rx={8} fill="#37474F" stroke={OL} strokeWidth={6} />
        {Array.from({length: 12}, (_, k) => <path key={'pn' + k} d={`M ${-240 + k * 44} 0 L ${-240 + k * 44} 14`} stroke={OL} strokeWidth={5} />)}
        <rect x={-240} y={-130} width={200} height={70} rx={8} fill="#263238" stroke={OL} strokeWidth={5} /><T x={-140} y={-84} s={22} c={CY}>AI CHIP</T>
        {Array.from({length: n}, (_, k) => { const drop = clamp((t - (z.t0 ?? 0)) * 3 - k * 0.0); const land = jig(t, (z.t0 ?? 0) + k * 0.25, 20, 8);
          return <g key={'hb' + k} transform={`translate(110 ${-70 - k * 36}) scale(${1 + 0.08 * land} ${1 - 0.12 * land})`} opacity={drop > 0 ? 1 : 1}>
            <rect x={-120} y={-30} width={240} height={32} rx={14} fill={k % 2 ? '#F2C179' : '#E8A95C'} stroke={OL} strokeWidth={4} />
            <path d="M -100 -14 L 100 -14" stroke="#FFFFFF" strokeWidth={3} opacity={0.5} /></g>; })}
        {n > 0 && <g transform={`translate(110 ${-70 - n * 36 - 10})`}><rect x={-30} y={-20} width={60} height={20} rx={4} fill="#FFF3B0" stroke={OL} strokeWidth={3} /></g>}
        {t > sy && n > 0 && <path d={`M 40 ${-70 - n * 36} Q 30 ${-70 - n * 36 + 40} 50 ${-70 - n * 36 + lerp(10, 160, clamp((t - sy) / 1.5))}`} stroke="#B8651B" strokeWidth={16} strokeLinecap="round" fill="none" />}
        <path d={`M -40 -95 L 0 -95`} stroke={GOLD} strokeWidth={6} strokeDasharray="8 6" strokeDashoffset={-t * 30} />
        <T x={110} y={-90 - Math.max(n, 1) * 36 - 40} s={30} c={NAVY} st="#FFFFFF" sw={6}>{n > 0 ? 'HBM' : ''}</T>
      </g>
    </g>;
  },

  /** a bright precision workshop with bottles and a spin-coater */
  svlab: (t, z, f) => {
    const nb = Math.floor(kf(z.bottles, t, 0)), out = kf(z.out, t, 0);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#F3F6FA" />
      <rect x={-200} y={f - 40} width={2400} height={40} fill="#DDE3EA" stroke={OL} strokeWidth={4} />
      <rect x={1560} y={160} width={420} height={300} fill="#BFE6F7" stroke={OL} strokeWidth={7} />{cloud(1700 + ((t * 10) % 140), 260, 0.6, 1)}
      <path d="M 1770 160 L 1770 460 M 1560 310 L 1980 310" stroke={OL} strokeWidth={5} />
      {/* shelves */}
      {[0, 1, 2].map((r) => <rect key={'sh' + r} x={80} y={300 + r * 170} width={640} height={16} fill={WOOD} stroke={OL} strokeWidth={4} />)}
      {Array.from({length: nb}, (_, k) => { const r = Math.floor(k / 8), c = k % 8, x = 120 + c * 78, y = 300 + r * 170, p = pop(t, (z.t0 ?? 0) + k * 0.08, 0.3);
        return <g key={'bt' + k} transform={`translate(${x} ${y}) scale(${p})`}><rect x={-22} y={-96} width={44} height={96} rx={10} fill={['#E1F5FE', '#FFF8E1', '#F3E5F5', '#E8F5E9'][k % 4]} stroke={OL} strokeWidth={4} />
          <rect x={-12} y={-116} width={24} height={20} fill="#90A4AE" stroke={OL} strokeWidth={3} /><rect x={-22} y={-60} width={44} height={22} fill={[BLUE, PURPLE, GREEN, GOLD][k % 4]} opacity={0.8} /></g>; })}
      {/* gas cylinders */}
      {[820, 890, 960].map((x, k) => <g key={'gc' + k}><rect x={x - 24} y={f - 260} width={48} height={220} rx={22} fill={['#90CAF9', '#A5D6A7', '#FFE082'][k]} stroke={OL} strokeWidth={5} /><rect x={x - 10} y={f - 284} width={20} height={26} fill="#78909C" stroke={OL} strokeWidth={3} /></g>)}
      {/* spin-coater */}
      <g transform={`translate(1280 ${f - 40})`}><rect x={-200} y={-200} width={400} height={200} rx={20} fill="#E7ECF3" stroke={OL} strokeWidth={6} />
        <rect x={-150} y={-330} width={300} height={130} rx={16} fill="#FFFFFF" fillOpacity={0.6} stroke={OL} strokeWidth={5} />
        <g transform={`translate(0 -240) scale(1 0.32) rotate(${t * 720})`}><circle r={110} fill="#B39DDB" stroke={OL} strokeWidth={8} /><path d="M -110 0 L 110 0 M 0 -110 L 0 110" stroke="#E1F5FE" strokeWidth={8} /></g>
        <path d={`M 0 -330 L 0 ${-280 + 6 * Math.sin(t * 8)}`} stroke={BLUE} strokeWidth={8} />
        {z.plaque && plaque(0, -380, z.plaque, '#FFFFFF', 24)}</g>
      {/* wafers ride out the door */}
      <rect x={1500} y={f - 80} width={700} height={22} fill="#90A4AE" stroke={OL} strokeWidth={4} />
      {out > 0 && Array.from({length: 6}, (_, k) => { const u = ((t * 0.3 * out + k / 6) % 1); return <g key={'wo' + k} transform={`translate(${1520 + u * 660} ${f - 96})`}><rect x={-34} y={-30} width={68} height={30} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-8} s={14} c={NAVY}>TO A FAB</T></g>; })}
    </g>;
  },

  /** desert, solar rows, a capital vault and data halls */
  svdesert: (t, z, f) => {
    const so = kf(z.solar, t, 0), va = kf(z.vault, t, 0), ca = kf(z.cash, t, 0), nh = Math.floor(kf(z.halls, t, 0));
    return <g>
      {sky(z, f, '#7CC4F0', '#FFF3DA', 'svdssk')}{sun(1700, 170, t, 70)}
      <path d={ridge(z.x0, z.x1, 700, 120, 600, 71)} fill="#EBC78A" stroke={OL} strokeWidth={4} />
      <path d={ridge(z.x0, z.x1, 790, 70, 420, 77)} fill={SAND} stroke={OL} strokeWidth={4} />
      {ground(z, f, '#F2D49B', '#DDB574')}
      {/* solar rows */}
      {Array.from({length: 4}, (_, r) => Array.from({length: 9}, (_, c) => { const k = r * 9 + c, on = so * 36 > k; return on ? <g key={'sl' + k} transform={`translate(${1350 + c * 90 - r * 30} ${f + 40 + r * 70})`}>
        <path d="M -40 0 L 40 0 L 30 -26 L -30 -26 Z" fill="#2B4F8C" stroke={OL} strokeWidth={3} /><path d="M -10 -26 L -14 0 M 10 -26 L 14 0" stroke="#7FA7E0" strokeWidth={2} /></g> : null; }))}
      {/* vault */}
      <g transform={`translate(420 ${f})`}><path d="M -230 0 L -230 -300 Q 0 -420 230 -300 L 230 0 Z" fill="#E0F2F1" stroke={OL} strokeWidth={7} />
        <circle cx={0} cy={-160} r={110} fill="#B0BEC5" stroke={OL} strokeWidth={7} />
        <g transform={`translate(0 -160) rotate(${va * 220})`}><circle r={80} fill="#CFD8DC" stroke={OL} strokeWidth={6} />{[0, 60, 120].map((r) => <path key={r} transform={`rotate(${r})`} d="M -70 0 L 70 0" stroke={OL} strokeWidth={8} strokeLinecap="round" />)}</g>
        {va > 0.6 && <circle cx={0} cy={-160} r={60} fill={GOLD2} opacity={0.5 + 0.3 * Math.sin(t * 6)} />}
        {z.plaque && plaque(0, -440, z.plaque, '#FFFFFF', 24)}</g>
      {ca > 0 && Array.from({length: 14}, (_, k) => { const u = ((t * 0.5 + k / 14) % 1) * clamp(ca * 1.2), x = lerp(420, k % 3 === 0 ? 2300 : 1000 + (k % 5) * 90, u), y = f - 160 - Math.sin(u * Math.PI) * (300 + (k % 4) * 60) + u * 120;
        return u > 0.02 ? coin(x, y, 0.9, 'dc' + k, t) : null; })}
      {/* data halls */}
      {Array.from({length: nh}, (_, k) => { const p = pop(t, (z.t0 ?? 0) + k * 0.4, 0.4); return <g key={'dh' + k} transform={`translate(${840 + k * 200} ${f}) scale(${p})`}>
        <rect x={0} y={-130} width={170} height={130} fill="#E7ECF3" stroke={OL} strokeWidth={5} />
        {[0, 1, 2].map((q) => <g key={q} transform={`translate(${30 + q * 55} -146)`}><rect x={-20} y={-10} width={40} height={18} fill="#B9C3D1" stroke={OL} strokeWidth={3} /><g transform={`rotate(${t * 400 + q * 40})`}><path d="M -12 0 L 12 0" stroke={OL} strokeWidth={3} /></g></g>)}
        {[0, 1, 2].map((q) => <rect key={'r' + q} x={20 + q * 50} y={-100} width={26} height={70} fill="#263238" stroke={OL} strokeWidth={2} />)}
        {[0, 1, 2].map((q) => <circle key={'l' + q} cx={33 + q * 50} cy={-90 + 20 * ((q + Math.floor(t * 3)) % 3)} r={4} fill={(q + Math.floor(t * 4)) % 2 ? CY : GREEN} />)}</g>; })}
      {ca > 0.3 && <g transform={`translate(2150 ${f - 420})`}><path d="M -120 0 L 80 0 L 80 -30 L 140 20 L 80 70 L 80 40 L -120 40 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={28} s={20} c={NAVY}>ABROAD</T></g>}
    </g>;
  },

  /** a mine: Andes copper or outback lithium */
  svmine: (t, z, f) => {
    const out = z.variant === 'outback', tr = kf(z.trucks, t, 1), nst = Math.floor(kf(z.stock, t, 0)), g = kf(z.gauge, t, 0);
    const rock = out ? '#C8643B' : '#9C8C7A', rock2 = out ? '#A9502E' : '#7E705F';
    return <g>
      {sky(z, f, out ? '#7EC7F2' : '#86C6EE', out ? '#FFEBD2' : '#EEF7FF', out ? 'svmnsk2' : 'svmnsk1')}{sun(1700, 170, t, 60)}{clouds(z, t, 4, 120)}
      {!out && <g><path d={peaks(z.x0, z.x1, 640, 380, 420, 81)} fill="#8E8FA8" stroke={OL} strokeWidth={4} />
        {Array.from({length: 12}, (_, k) => { const x = z.x0 + 210 + k * 420; return <path key={'sn' + k} d={`M ${x - 60} ${420 + rnd(k) * 60} L ${x} ${340 + rnd(k + 3) * 40} L ${x + 60} ${420 + rnd(k) * 60} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={3} />; })}</g>}
      {out && <path d={ridge(z.x0, z.x1, 760, 80, 600, 91)} fill="#D98A5A" stroke={OL} strokeWidth={4} />}
      {ground(z, f, rock, rock2)}
      {/* terraced pit */}
      <g transform={`translate(900 ${f + 40})`}>{Array.from({length: 5}, (_, k) => <ellipse key={'tp' + k} cx={0} cy={k * 22} rx={560 - k * 100} ry={120 - k * 20} fill={k % 2 ? rock2 : rock} stroke={OL} strokeWidth={4} />)}
        {!out && <ellipse cx={0} cy={110} rx={120} ry={22} fill="#3FA796" stroke={OL} strokeWidth={3} />}</g>
      {/* haul trucks circling */}
      {Array.from({length: 3}, (_, k) => { const a = t * 0.35 * tr + k * 2.1, x = 900 + Math.cos(a) * (420 - k * 60), y = f + 40 + Math.sin(a) * (80 - k * 10), fl = Math.sin(a) > 0 ? -1 : 1;
        return <g key={'tk' + k} transform={`translate(${x} ${y}) scale(${0.55 * fl} 0.55)`}><path d="M -110 -60 L 70 -60 L 110 -10 L -110 -10 Z" fill={GOLD2} stroke={OL} strokeWidth={6} />
          <path d="M -100 -60 Q -20 -110 60 -60" fill={out ? '#ECEFF1' : COPPER} stroke={OL} strokeWidth={4} /><rect x={70} y={-100} width={50} height={44} fill={GOLD} stroke={OL} strokeWidth={5} />
          {[-70, 60].map((q) => <circle key={q} cx={q} cy={0} r={30} fill="#37474F" stroke={OL} strokeWidth={6} />)}</g>; })}
      {/* product stack: copper cathodes or white lithium bags */}
      <g transform={`translate(1650 ${f})`}>{Array.from({length: nst}, (_, k) => { const p = pop(t, (z.t0 ?? 0) + k * 0.18, 0.3);
        return out ? <g key={'bg' + k} transform={`translate(${(k % 4) * 80 - 120} ${-Math.floor(k / 4) * 70}) scale(${p})`}><path d="M -34 0 L -38 -64 Q 0 -76 38 -64 L 34 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-26} s={16} c={NAVY}>Li</T></g>
          : <g key={'ct' + k} transform={`translate(${(k % 2) * 140 - 70} ${-k * 18}) scale(${p})`}><rect x={-62} y={-18} width={124} height={18} fill={COPPER} stroke={OL} strokeWidth={3} /></g>; })}
        {z.plaque && plaque(0, -300, z.plaque, '#FFFFFF', 22)}</g>
      {z.gauge !== undefined && <g transform={`translate(300 ${f - 420})`}><rect x={-170} y={-130} width={340} height={200} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <path d="M -120 40 A 120 120 0 0 1 120 40" stroke="#CFD8DC" strokeWidth={22} fill="none" /><path d="M -120 40 A 120 120 0 0 1 -60 -64" stroke={RED} strokeWidth={22} fill="none" /><path d="M 60 -64 A 120 120 0 0 1 120 40" stroke={GREEN} strokeWidth={22} fill="none" />
        <g transform={`translate(0 40) rotate(${g * 70 + 4 * Math.sin(t * 9) * Math.abs(g)})`}><path d="M -8 0 L 0 -110 L 8 0 Z" fill={NAVY} /></g><circle cx={0} cy={40} r={12} fill={NAVY} />
        <T x={0} y={-96} s={24} c={NAVY}>WORLD PRICE</T></g>}
    </g>;
  },

  /** Hattie's chalkboard scorecard */
  svledger: (t, z, f) => {
    const rows: any[] = z.rows || [];
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#E9D3B0" />
      {Array.from({length: 14}, (_, k) => <path key={'pl' + k} d={`M ${-200 + k * 180} -200 L ${-200 + k * 180} 1300`} stroke={WOOD} strokeWidth={4} opacity={0.5} />)}
      <g transform={`translate(960 560) rotate(${-1 + Math.sin(t * 0.8) * 0.6})`}><rect x={-560} y={-440} width={1120} height={900} rx={18} fill={WOOD2} stroke={OL} strokeWidth={8} />
        <rect x={-520} y={-400} width={1040} height={820} rx={8} fill="#2F4A3A" stroke={OL} strokeWidth={5} />
        <T x={0} y={-320} s={fit(z.title || "HATTIE'S SCORECARD", 900, 54)} c="#FFF8E1">{z.title || "HATTIE'S SCORECARD"}</T>
        <path d="M -440 -290 L 440 -290" stroke="#FFF8E1" strokeWidth={3} opacity={0.6} />
        {rows.map((r, k) => { const u = pop(t, r.at ?? 0, 0.4); if (u <= 0) return null; const y = -210 + k * 104, m = r.mark || 'yes', n = Math.floor(clamp((t - (r.at ?? 0)) / 0.6) * (r.label || '').length);
          return <g key={k}><T x={-450} y={y + 14} s={fit(r.label || '', 720, 38)} a="start" c="#FFF8E1">{(r.label || '').slice(0, n)}</T>
            <g transform={`translate(380 ${y}) scale(${u})`}>{m === 'yes' ? <path d="M -30 0 l 20 22 l 40 -46" stroke="#8BE28B" strokeWidth={12} fill="none" strokeLinecap="round" />
              : m === 'no' ? <path d="M -26 -26 L 26 26 M 26 -26 L -26 26" stroke="#FF8A80" strokeWidth={12} strokeLinecap="round" />
                : m === 'ride' ? <path d="M -50 10 Q -25 -40 0 10 T 50 10" stroke={GOLD2} strokeWidth={10} fill="none" strokeLinecap="round" />
                  : <T x={0} y={18} s={56} c={GOLD2}>?</T>}</g></g>; })}</g>
    </g>;
  },

  /** title card: a golden chip-shovel digs and flips coins */
  svtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['THE COUNTRIES THAT COULD', 'WIN THE AI ECONOMY', 'WITHOUT BUILDING AI'];
    const dig = Math.sin(t * 2.6) * 14;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#FFF1D2" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(1500 900) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#FBE0B0' : '#FFF1D2'} />)}
      <path d={ridge(-200, 2200, 930, 90, 260, 5)} fill="#D7BE8E" stroke={OL} strokeWidth={4} />
      {shovelG(1500, 980, 1.5, dig, 'ttl', true, true, t)}
      {Array.from({length: 6}, (_, k) => { const u = ((t * 0.6 + k / 6) % 1); return coin(1500 + (k - 2.5) * 50 * u * 4, 900 - Math.sin(u * Math.PI) * 300, 1, 'tc' + k, t); })}
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.55) / 0.5) * ln.length);
        return <T key={k} x={720} y={260 + k * 140} s={fit(ln, 1300, k === lines.length - 1 ? 120 : 96)} c={k === lines.length - 1 ? GOLD : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={720} y={720} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a shovel digs and a signpost pops up */
  svbumper: (t, z, f) => {
    const c = z.color || GOLD, u = pop(t, 0.6, 0.5), dig = E.inOut(win(t, 0.1, 0.5));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.07} />)}
      <rect x={-200} y={860} width={2400} height={400} fill="#C8A26B" stroke={OL} strokeWidth={6} />
      {shovelG(1500, lerp(760, 900, dig), 1.2, lerp(-30, 10, dig), 'bmp', true, false, t)}
      {Array.from({length: 7}, (_, q) => { const v = clamp((t - 0.55) / 0.8); return v > 0 && v < 1 ? <circle key={q} cx={1500 + (q - 3) * 40 * v * 3} cy={880 - Math.sin(v * Math.PI) * (120 + q * 20)} r={12} fill="#8A6A3F" stroke={OL} strokeWidth={3} /> : null; })}
      <g transform={`translate(760 ${860 - 260 * u})`}><rect x={-14} y={0} width={28} height={300} fill={WOOD2} stroke={OL} strokeWidth={5} />
        <path d="M -560 -150 L 520 -150 L 590 -70 L 520 10 L -560 10 Z" fill="#FFF3D6" stroke={OL} strokeWidth={7} />
        <T x={-10} y={-96} s={36} c={WOOD2} ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <T x={-10} y={-26} s={fit(z.title || '', 1000, 58)} c={NAVY}>{z.title || ''}</T></g>
      {t >= 1.4 && <T x={760} y={1000} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.4) / 0.3)}>{z.caption || ''}</T>}
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const SHOVELS_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

/** nugget: a gold AI chip with pin legs, an LED face and a passport */
const nugget: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, walking = Math.abs(vx) > 20;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.6) hy = Math.sin((u / 0.6) * Math.PI) * 90; }
  const step = walking ? Math.sin(t * 16) : 0, bob = walking ? Math.abs(step) * 8 : Math.sin(t * 2.5 + i) * 3;
  const y = kf(a.y, t, f) - hy - bob, s = (a.scale ?? 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const face: string = (() => { let v = a.face || 'happy'; if (Array.isArray(a.faces)) for (const [pt, pv] of a.faces) if (t >= Number(pt)) v = pv; return v; })();
  const fl = vx < -20 ? -1 : 1, talking = Array.isArray(a.talk) && a.talk.some((p: any) => t >= p[0] && t <= p[1]);
  const blink = (Math.floor(t * 0.7 + i) % 4 === 0 && (t % 1.43) < 0.12);
  const eye = face === 'wow' ? <g><circle cx={-22} cy={-96} r={12} fill={CY} /><circle cx={22} cy={-96} r={12} fill={CY} /></g>
    : face === 'grin' ? <g><path d="M -34 -92 q 12 -14 24 0 M 10 -92 q 12 -14 24 0" stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" /></g>
      : <g><rect x={-30} y={-108} width={16} height={blink ? 3 : 18} rx={4} fill={CY} /><rect x={14} y={-108} width={16} height={blink ? 3 : 18} rx={4} fill={CY} /></g>;
  const mouth = face === 'worry' ? 'M -18 -58 Q 0 -70 18 -58' : face === 'wow' || talking ? `M -12 -64 a 12 ${talking ? 6 + 5 * Math.abs(Math.sin(t * 18)) : 12} 0 1 0 24 0 a 12 ${talking ? 6 + 5 * Math.abs(Math.sin(t * 18)) : 12} 0 1 0 -24 0` : 'M -20 -66 Q 0 -50 20 -66';
  return <g key={'ng' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <ellipse cx={0} cy={2} rx={60} ry={10} fill={OL} opacity={0.15} />
    <path d={`M -24 -20 L ${-28 + step * 12} 0 M 24 -20 L ${28 - step * 12} 0`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
    <path d={`M -62 -110 L ${-96} ${-80 + 10 * Math.sin(t * 3 + i)} M 62 -110 L 96 ${-80 - 10 * Math.sin(t * 3 + i)}`} stroke={OL} strokeWidth={7} strokeLinecap="round" />
    <rect x={-66} y={-170} width={132} height={150} rx={14} fill={GOLD} stroke={OL} strokeWidth={6} />
    {[0, 1, 2, 3].map((q) => <path key={'pt' + q} d={`M ${-45 + q * 30} -170 L ${-45 + q * 30} -184 M ${-45 + q * 30} -20 L ${-45 + q * 30} -10`} stroke={OL} strokeWidth={6} />)}
    <rect x={-48} y={-150} width={96} height={110} rx={10} fill="#263238" stroke={OL} strokeWidth={4} />
    {eye}<path d={mouth} stroke={CY} strokeWidth={5} fill={face === 'wow' || talking ? CY : 'none'} strokeLinecap="round" />
    <path d="M -56 -160 L -40 -160 M 40 -160 L 56 -160" stroke={GOLD2} strokeWidth={4} />
    {a.passport && <g transform={`translate(${86} -86) rotate(${8 + 6 * Math.sin(t * 2)})`}><rect x={-26} y={-34} width={52} height={68} rx={6} fill="#1F4E8C" stroke={OL} strokeWidth={4} /><circle cx={0} cy={-6} r={12} fill="none" stroke={GOLD2} strokeWidth={3} /><path d="M -14 20 L 14 20" stroke={GOLD2} strokeWidth={3} /></g>}
    {a.label && t < (a.labelUntil ?? at + 3) && <g transform={`scale(${fl} 1)`}>{plaque(0, -230, a.label, '#FFFFFF', 20)}</g>}
  </g>;
};

/** shovel prop */
const shovel: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  return <g key={'sp' + i} transform={`scale(1)`}>{shovelG(kf(a.x, t, 960), kf(a.y, t, f), (a.scale ?? 1) * pop(t, at, 0.4), kf(a.rot, t, 0), 'it' + i, !!a.gold, !!a.chip, t)}</g>;
};

/** svpass: an open passport with stamps thumping in */
const svpass: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 540), s = (a.scale ?? 1) * pop(t, at, 0.4), st: any[] = a.stamps || [];
  return <g key={'pp' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-430} y={-270} width={860} height={540} rx={20} fill="#1F4E8C" stroke={OL} strokeWidth={7} />
    <rect x={-410} y={-250} width={400} height={500} rx={8} fill="#FFF8E7" stroke={OL} strokeWidth={4} /><rect x={10} y={-250} width={400} height={500} rx={8} fill="#FFF8E7" stroke={OL} strokeWidth={4} />
    {st.map((m, k) => { const p = pop(t, m.at ?? 0, 0.3); if (p <= 0) return null; const col = k % 2, row = Math.floor(k / 2), sx = -210 + (k >= 4 ? 420 : 0) + (col ? 0 : 0), px = (k < 4 ? -300 + (k % 2) * 200 : 120 + (k % 2) * 200), py = -150 + (Math.floor((k % 4) / 2)) * 220, land = jig(t, m.at ?? 0, 22, 7);
      void sx; void row;
      return <g key={'ps' + k} transform={`translate(${px} ${py}) rotate(${-10 + (k * 7) % 20}) scale(${p * (1 - 0.15 * land)})`}>
        <circle r={86} fill="none" stroke={m.c || RED} strokeWidth={6} strokeDasharray="6 5" /><circle r={66} fill="none" stroke={m.c || RED} strokeWidth={3} />
        <T x={0} y={-6} s={fit(m.label || '', 120, 26)} c={m.c || RED}>{m.label}</T><T x={0} y={24} s={14} c={m.c || RED}>{m.sub || 'SHOVEL SHOP'}</T></g>; })}
  </g>;
};

/** svcoin: a coin shower */
const svcoin: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 540), n = a.n ?? 10;
  return <g key={'cs' + i}>{Array.from({length: n}, (_, k) => { const u = ((t - at) * 0.9 + k / n) % 1; return coin(x + (rnd(k + i) - 0.5) * 360, y - 300 + u * 420, 0.9, 'cs' + i + '_' + k, t); })}</g>;
};

export const SHOVELS_ITEMS: Record<string, ItemFn> = {nugget, shovel, svpass, svcoin};
export const SHOVELS_INDOOR = ['svmap', 'svlab', 'svledger', 'svtitle', 'svbumper'];
