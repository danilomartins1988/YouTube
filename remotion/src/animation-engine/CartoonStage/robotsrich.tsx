import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * ROBOTS-RICH kit for CartoonStage (Episode 64, "Who Gets Rich When Robots Do the Work?").
 *
 * Prime-time TV-cartoon GENRE (thick clean outlines, flat colour, squash and stretch), day scenes, everything ORIGINAL: no logos,
 * brand marks or traced products; companies appear only as generic buildings with a text plaque. No real person is drawn.
 * Sets:
 *  - robotown: an original American town by day: a warehouse where BOLT-style robots carry boxes (`robots` KF 0..6), workers' houses
 *    on the left, an OWNERS tower on the right; `flowAt` sends coins from the warehouse to `flowTo` ('tower'|'houses'|'both').
 *  - splitter: the $100 SPLITTER machine: coins drop from a hopper into three jars PAY / PROFITS / OTHER whose levels follow `pay`,
 *    `profit`, `other` (KF, dollars); `year` [[t, text]] badge; `note` ribbon.
 *  - sharestreet: a hillside street of 100 households sorted by wealth; four groups (`groups` [{label, n, v, at, color}]) each get a
 *    stack of share certificates sized by v (dollars of every $100 of stock); `flowAt` coins climb the hill toward the top group.
 *  - dcfield: generic AI data-center campuses under construction (`camps` [{name, v, at}] with $bn gauges), cranes and fans; a CHIP
 *    SHOP on the right (`chipAt`) with a coin pie of `margin` (0..1) labelled `marginText`.
 *  - moneyloop: four stations in a ring (BUSINESS, CLOUD, CHIPS, SHAREHOLDERS) with coins circling (`loopAt`), a worker outside the
 *    loop (`outAt`) and a dashed door to the loop labelled OWN SHARES (`doorAt`).
 *  - evidencelab: a bright lab with a FINDINGS board (left) and a FORECASTS board (right); cards pop by `cards` [{text, sub, kind:
 *    'finding'|'forecast'|'descriptive', at}].
 *  - millyard: an 1830s British mill town by day (brick mills, canal, chimneys) under a sky chart of output per worker vs real wage
 *    (`prog` KF 0..1 along 1780-1880; `pauseAt` shades ENGELS' PAUSE; `catchAt` labels the catch-up). Illustrative shape only.
 *  - newjobs: a street of doors; old job signs fade (`old` [{text, at}]) while new ones pop (`fresh` [{text, at}]).
 *  - doorways: three doors (`doors` [{label, sub, at, color}]) that open to reveal tiny scenes; EDUCATION, NOT ADVICE banner always on;
 *    `riskAt` shows a seesaw of risks (`risks` [[t, text]]).
 *  - rrtitle / rrbumper: title card and act bumpers.
 * Items: rrtag (top-left pill: FACT / FINDING / FORECAST / DESCRIPTIVE / OUR MATH / ILLUSTRATIVE / EDUCATION...), bolt (the original
 *  helper robot: `x`, `y` KF, `carry` 'box'|'coin'|'none', `wave`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#1B2333';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; flip?: boolean; [k: string]: any};
type SetFn = (t: number, z: Z, f: number) => React.ReactNode;
type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

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
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#2A6FDB', GOLD = '#F2B33D', RED = '#D9483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', PURPLE = '#7357C9', ORANGE = '#E07A2F', GREY = '#8E9AAF', NAVY = '#1B2333', GLASS = '#BFE6F7', BRICK = '#B4553F';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'rcl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const clouds = (z: Z, t: number, n = 4) => Array.from({length: n}, (_, k) => cloud(((k * 640 + t * 12) % (z.x1 - z.x0 + 600)) + z.x0 - 300, 100 + (k % 2) * 90, 0.8, k));
const ground = (z: Z, f: number, c = '#B7D7A0', c2 = '#9CC487') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const banner = (x: number, y: number, txt: string, c = PURPLE, s = 24) => { const w = Math.max(260, txt.length * s * 0.62 + 50);
  return <g transform={`translate(${x} ${y}) rotate(-1.5)`}><rect x={-w / 2} y={-s} width={w} height={s * 1.7} rx={8} fill={c} stroke={OL} strokeWidth={4} />
    <T x={0} y={s * 0.32} s={s} c="#FFFFFF">{txt}</T></g>; };
const coin = (x: number, y: number, s = 1, k: number | string = 0, spin = 0) => <g key={'rc' + k} transform={`translate(${x} ${y}) scale(${s * (0.35 + 0.65 * Math.abs(Math.cos(spin)))} ${s})`}>
  <circle r={18} fill={GOLD} stroke={OL} strokeWidth={3.5} /><T x={0} y={7} s={20}>$</T></g>;
const cert = (x: number, y: number, s: number, k: number | string, c = '#FFF6D8') => <g key={'ct' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-40} y={-26} width={80} height={52} rx={4} fill={c} stroke={OL} strokeWidth={3} /><rect x={-32} y={-18} width={64} height={36} rx={2} fill="none" stroke={GREEN} strokeWidth={2.5} />
  <T x={0} y={6} s={14} c={GREEN}>SHARE</T></g>;
/** a coin flying from a to b along an arc; u 0..1 */
const flyer = (ax: number, ay: number, bx: number, by: number, u: number, k: number | string, h = 160) => coin(lerp(ax, bx, u), lerp(ay, by, u) - Math.sin(u * Math.PI) * h, 0.9, k, u * 12);

/** generic person (worker / suit / retiree); kind 'vest'|'suit'|'grey'|'coat' */
const fig = (x: number, y: number, s: number, k: number, t: number, kind = 'vest') => {
  const skin = ['#F6CDA6', '#B97A4B', '#E0A878', '#F3D7BD', '#8D5A3B'][k % 5], body = kind === 'suit' ? '#2B3A5C' : kind === 'grey' ? GREY : kind === 'coat' ? '#FFFFFF' : [TEAL, BLUE, ORANGE, GREEN][k % 4];
  const bob = 3 * Math.sin(t * 3 + k);
  return <g key={'fg' + k + kind} transform={`translate(${x} ${y + bob}) scale(${s})`}>
    <path d="M -8 -40 L -8 0 M 8 -40 L 8 0" stroke="#2B3A50" strokeWidth={12} strokeLinecap="round" />
    <rect x={-20} y={-94} width={40} height={58} rx={13} fill={body} stroke={OL} strokeWidth={3.5} />
    {kind === 'vest' && <path d="M -14 -90 L -6 -40 M 14 -90 L 6 -40" stroke="#FFE14D" strokeWidth={5} />}
    <path d={`M -18 -84 L -28 -52 M 18 -84 L ${28 + 4 * Math.sin(t * 2 + k)} -54`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
    <circle cx={0} cy={-112} r={18} fill={skin} stroke={OL} strokeWidth={3.5} />
    {kind === 'vest' && <path d="M -20 -114 Q 0 -146 20 -114 Z" fill={GOLD} stroke={OL} strokeWidth={3.5} />}
    {kind === 'grey' && <path d="M -18 -118 Q 0 -138 18 -118" stroke="#E0E0E0" strokeWidth={9} fill="none" strokeLinecap="round" />}
    {kind === 'suit' && <path d="M -16 -122 Q 0 -138 16 -122" stroke="#2D2018" strokeWidth={9} fill="none" />}
    {kind === 'coat' && <path d="M -16 -122 Q 0 -140 16 -122" stroke="#3E2C22" strokeWidth={8} fill="none" />}
    <circle cx={-6} cy={-112} r={2.5} fill={OL} /><circle cx={6} cy={-112} r={2.5} fill={OL} /><path d="M -6 -102 Q 0 -98 6 -102" stroke={OL} strokeWidth={2.5} fill="none" />
  </g>;
};

/** BOLT: the original helper robot (boxy body, round screen face, tread base) */
const boltBot = (x: number, y: number, s: number, t: number, k: number | string, carry = 'box', mood = 'happy') => {
  const bob = 4 * Math.abs(Math.sin(t * 5 + Number(String(k).length)));
  return <g key={'bb' + k} transform={`translate(${x} ${y - bob}) scale(${s})`}>
    <rect x={-46} y={-26} width={92} height={26} rx={13} fill="#4A5A70" stroke={OL} strokeWidth={4} />
    {[-30, 0, 30].map((q) => <circle key={q} cx={q} cy={-13} r={8} fill="#2B3440" stroke={OL} strokeWidth={2} />)}
    <rect x={-40} y={-110} width={80} height={86} rx={16} fill="#E9EEF4" stroke={OL} strokeWidth={4.5} />
    <rect x={-28} y={-98} width={56} height={40} rx={12} fill="#13314F" stroke={OL} strokeWidth={3} />
    {mood === 'happy' ? <g><circle cx={-11} cy={-82} r={5} fill="#5EE6FF" /><circle cx={11} cy={-82} r={5} fill="#5EE6FF" /><path d="M -10 -70 Q 0 -63 10 -70" stroke="#5EE6FF" strokeWidth={3} fill="none" /></g>
      : <g><path d="M -16 -84 L -6 -80 M 16 -84 L 6 -80" stroke="#5EE6FF" strokeWidth={4} /><path d="M -10 -66 Q 0 -72 10 -66" stroke="#5EE6FF" strokeWidth={3} fill="none" /></g>}
    <path d="M 0 -110 L 0 -130" stroke={OL} strokeWidth={4} /><circle cx={0} cy={-134} r={7} fill={RED} stroke={OL} strokeWidth={3} opacity={0.6 + 0.4 * Math.sin(t * 6)} />
    <path d={`M -40 -80 L -62 ${-56 + 6 * Math.sin(t * 4)} M 40 -80 L 62 -56`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
    {carry === 'box' && <g transform="translate(0 -152)"><rect x={-34} y={-30} width={68} height={50} rx={4} fill="#D9A066" stroke={OL} strokeWidth={4} /><path d="M -34 -12 L 34 -12" stroke="#9C6B3E" strokeWidth={4} /></g>}
    {carry === 'coin' && <g transform="translate(0 -160)">{coin(0, 0, 1.6, 'bc' + k, t * 3)}</g>}
  </g>;
};

const house = (x: number, y: number, s: number, k: number, c: string) => <g key={'hs' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-60} y={-90} width={120} height={90} fill={c} stroke={OL} strokeWidth={4} />
  <path d="M -72 -90 L 0 -150 L 72 -90 Z" fill={['#B85C3F', '#5B6F8F', '#7A5C99', '#3F7F5F'][k % 4]} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
  <rect x={-40} y={-66} width={28} height={28} fill={GLASS} stroke={OL} strokeWidth={3} /><rect x={12} y={-60} width={28} height={60} fill="#7A4E2D" stroke={OL} strokeWidth={3} />
</g>;

const tower = (x: number, y: number, w: number, h: number, t: number, glow = 0) => <g>
  {glow > 0 && <rect x={x - 26} y={y - h - 26} width={w + 52} height={h + 26} rx={26} fill={GOLD} opacity={0.3 * glow * (0.7 + 0.3 * Math.sin(t * 4))} />}
  <rect x={x} y={y - h} width={w} height={h} rx={8} fill="#DDEFFB" stroke={OL} strokeWidth={5} />
  {Array.from({length: Math.floor((h - 40) / 56)}, (_, r) => Array.from({length: Math.floor((w - 20) / 50)}, (_, c) => <rect key={r + '-' + c} x={x + 14 + c * 50} y={y - h + 20 + r * 56} width={36} height={38} fill={(r + c) % 3 ? '#9ED4F0' : '#FFF3C4'} />))}
  <path d={`M ${x - 10} ${y - h} L ${x + w + 10} ${y - h}`} stroke={OL} strokeWidth={8} />
</g>;

/** a generic data-center hall with rooftop fans */
const dchall = (x: number, y: number, w: number, h: number, t: number, k: number, build = 1) => <g key={'dc' + k}>
  <g transform={`translate(0 ${(1 - build) * h})`}>
    <rect x={x} y={y - h} width={w} height={h} rx={6} fill="#CBD5E1" stroke={OL} strokeWidth={5} />
    {Array.from({length: Math.floor(w / 48)}, (_, q) => <rect key={q} x={x + 10 + q * 48} y={y - h + 26} width={30} height={h - 52} rx={3} fill="#5B6B80" stroke={OL} strokeWidth={2} />)}
    {Array.from({length: Math.floor(w / 48)}, (_, q) => <circle key={'l' + q} cx={x + 25 + q * 48} cy={y - h / 2} r={3.5} fill={(q + Math.floor(t * 4)) % 3 ? '#5EE6FF' : '#7CFF8A'} />)}
    {Array.from({length: Math.max(1, Math.floor(w / 110))}, (_, q) => <g key={'fn' + q} transform={`translate(${x + 50 + q * 110} ${y - h - 16})`}>
      <rect x={-34} y={-14} width={68} height={28} rx={6} fill="#E9EEF4" stroke={OL} strokeWidth={3.5} />
      <g transform={`rotate(${t * 360 + q * 40})`}><path d="M 0 0 L -12 -4 L 0 -10 Z M 0 0 L 12 4 L 0 10 Z" fill={OL} /></g></g>)}
  </g>
  {build < 1 && <rect x={x - 6} y={y - h * build - 4} width={w + 12} height={8} fill={GOLD} stroke={OL} strokeWidth={2} />}
</g>;

const crane = (x: number, y: number, s: number, t: number, k: number) => { const sw = 10 * Math.sin(t * 0.8 + k);
  return <g key={'cr' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -10 0 L -10 -420 L 10 -420 L 10 0" fill="none" stroke={GOLD} strokeWidth={10} />
    {Array.from({length: 10}, (_, q) => <path key={q} d={`M -10 ${-q * 42} L 10 ${-q * 42 - 42}`} stroke={GOLD} strokeWidth={4} />)}
    <g transform={`rotate(${sw} 0 -420)`}><path d="M -80 -420 L 300 -420" stroke={GOLD} strokeWidth={12} /><path d={`M 220 -420 L 220 ${-300 + 20 * Math.sin(t)}`} stroke={OL} strokeWidth={3} />
      <rect x={200} y={-300 + 20 * Math.sin(t)} width={40} height={30} fill={GREY} stroke={OL} strokeWidth={3} /></g>
  </g>; };

const jar = (x: number, y: number, w: number, h: number, lvl: number, c: string, label: string, val: string, hot = false) => <g>
  <rect x={x - w / 2} y={y - h} width={w} height={h} rx={22} fill="#FFFFFF" fillOpacity={0.55} stroke={hot ? GOLD : OL} strokeWidth={hot ? 8 : 5} />
  <rect x={x - w / 2 + 8} y={y - 8 - (h - 16) * clamp(lvl)} width={w - 16} height={(h - 16) * clamp(lvl)} rx={14} fill={c} />
  {Array.from({length: Math.floor(((h - 16) * clamp(lvl)) / 26)}, (_, q) => <path key={q} d={`M ${x - w / 2 + 16} ${y - 20 - q * 26} L ${x + w / 2 - 16} ${y - 20 - q * 26}`} stroke="#FFFFFF" strokeWidth={3} opacity={0.35} />)}
  <rect x={x - w / 2 - 10} y={y - h - 14} width={w + 20} height={22} rx={8} fill="#E9EEF4" stroke={OL} strokeWidth={4} />
  <T x={x} y={y + 50} s={fit(label, w + 80, 34)}>{label}</T>
  {val && <g transform={`translate(${x} ${y - h - 60})`}><rect x={-100} y={-30} width={200} height={50} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={6} s={fit(val, 180, 32)} c={c === GREY ? OL : c}>{val}</T></g>}
</g>;

export const ROBOTSRICH_SETS: Record<string, SetFn> = {
  /** an original American town: houses (left), warehouse with robots (middle), owners' tower (right) */
  robotown: (t, z, f) => {
    const nb = Math.round(clamp(kf(z.robots, t, 3), 0, 6)), fa = z.flowAt, to = z.flowTo || 'tower', hum = clamp(kf(z.workers, t, 3), 0, 4);
    return <g>
      {sky(z, f, '#7EC8F2', '#EAF6FD', 'rtsky' + Math.round(z.x0))}
      {clouds(z, t)}
      <circle cx={1700} cy={150} r={70} fill="#FFE27A" stroke={OL} strokeWidth={4} />
      <path d={`M ${z.x0} ${f - 160} Q ${z.x0 + 900} ${f - 300} ${z.x0 + 1900} ${f - 190} T ${z.x1} ${f - 210} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#BFDDB0" />
      {[0, 1, 2, 3].map((k) => house(-420 + k * 170, f, 0.95, k, ['#F1D9B5', '#E8C7A0', '#F5E6CC', '#DCE8F5'][k]))}
      {plaque(-170, f - 220, z.homesLabel || 'WORKERS', '#FFFFFF', 22)}
      {/* warehouse */}
      <g>
        <path d={`M 160 ${f} L 160 ${f - 300} L 450 ${f - 360} L 740 ${f - 300} L 740 ${f} Z`} fill="#E9C46A" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        {[0, 1, 2].map((q) => <g key={q}><rect x={200 + q * 180} y={f - 170} width={140} height={170} fill="#5B6B80" stroke={OL} strokeWidth={4} />
          {Array.from({length: 6}, (_, r) => <path key={r} d={`M ${200 + q * 180} ${f - 150 + r * 26} L ${340 + q * 180} ${f - 150 + r * 26}`} stroke="#8796AA" strokeWidth={4} />)}</g>)}
        {plaque(450, f - 250, z.whLabel || 'WAREHOUSE', '#FFFFFF', 26)}
      </g>
      {Array.from({length: nb}, (_, k) => { const u = ((t * 0.12 + k / Math.max(1, nb)) % 1), x = 120 + u * 700; return boltBot(x, f + 70, 0.75, t, 'rt' + k, k % 2 ? 'box' : 'none'); })}
      {Array.from({length: Math.round(hum)}, (_, k) => fig(-430 + k * 140, f + 90, 0.9, k, t, 'vest'))}
      {/* owners' tower */}
      {tower(1000, f, 240, 520, t, fa !== undefined && t >= fa ? 1 : 0)}
      {plaque(1120, f - 560, z.towerLabel || 'OWNERS', NAVY, 26, '#FFFFFF')}
      {fa !== undefined && t >= fa && Array.from({length: 7}, (_, k) => { const u = ((t - fa) * 0.6 + k / 7) % 1;
        const both = to === 'both', toT = to === 'tower' || (both && k % 3 !== 0), bx = toT ? 1120 : -170, by = toT ? f - 420 : f - 120;
        return flyer(450, f - 320, bx, by, u, 'rf' + k, 180); })}
      {ground(z, f)}
      <rect x={z.x0} y={f + 110} width={z.x1 - z.x0} height={60} fill="#9AA5B4" />
      {Array.from({length: 18}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 260 - ((t * 60) % 260)} y={f + 136} width={120} height={8} fill="#FFFFFF" />)}
    </g>;
  },

  /** the $100 SPLITTER machine */
  splitter: (t, z, f) => {
    const pay = kf(z.pay, t, 0), prof = kf(z.profit, t, 0), oth = kf(z.other, t, 0), yr = pick(z.year, t, ''), hot = pick<string>(z.hiAt, t, '');
    const cx = z.mx ?? 960, run = z.runAt === undefined || t >= z.runAt;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f + 700} fill="#F4F1E8" />
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 120)}, (_, k) => <path key={'sg' + k} d={`M ${z.x0 + k * 120} -200 L ${z.x0 + k * 120} ${f + 300}`} stroke="#E8E2D2" strokeWidth={3} />)}
      {/* hopper */}
      <path d={`M ${cx - 220} 120 L ${cx + 220} 120 L ${cx + 90} 300 L ${cx - 90} 300 Z`} fill={TEAL} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <T x={cx} y={190} s={36} c="#FFFFFF" st={OL} sw={6}>$100 OF INCOME</T>
      {run && Array.from({length: 6}, (_, k) => { const u = ((t * 0.9 + k / 6) % 1); return coin(cx - 120 + k * 48, 40 + u * 120, 0.9, 'hp' + k, t * 4 + k); })}
      {/* machine body */}
      <rect x={cx - 170} y={300} width={340} height={170} rx={24} fill="#E9EEF4" stroke={OL} strokeWidth={6} />
      {[0, 1, 2].map((q) => <g key={q} transform={`translate(${cx - 100 + q * 100} 385) rotate(${(run ? t : 0) * (q % 2 ? -90 : 90)})`}>
        <circle r={34} fill={GOLD} stroke={OL} strokeWidth={4} />{[0, 60, 120].map((r) => <rect key={r} transform={`rotate(${r})`} x={-4} y={-40} width={8} height={80} fill={OL} />)}<circle r={10} fill="#FFFFFF" stroke={OL} strokeWidth={3} /></g>)}
      {/* chutes */}
      {[[-1, BLUE], [0, GOLD], [1, GREY]].map(([d, c], q) => <path key={'ch' + q} d={`M ${cx + Number(d) * 60} 470 Q ${cx + Number(d) * 200} 560 ${cx + Number(d) * 520} 600`} stroke={OL} strokeWidth={46} fill="none" strokeLinecap="round" />)}
      {[[-1, BLUE], [0, GOLD], [1, GREY]].map(([d, c], q) => <path key={'ci' + q} d={`M ${cx + Number(d) * 60} 470 Q ${cx + Number(d) * 200} 560 ${cx + Number(d) * 520} 600`} stroke={String(c)} strokeWidth={34} fill="none" strokeLinecap="round" />)}
      {run && [-1, 0, 1].map((d) => Array.from({length: 3}, (_, k) => { const u = ((t * 1.1 + k / 3 + d * 0.17) % 1), x = cx + d * 60 + (d * 460) * u, y = 470 + 130 * u - 40 * Math.sin(u * Math.PI);
        return coin(x, y, 0.7, 'cu' + d + k, t * 5 + k); }))}
      {jar(cx - 520, f + 40, 220, 300, pay / 70, BLUE, z.payLabel || 'PAY', `$${pay.toFixed(0)}`, hot === 'pay')}
      {jar(cx, f + 40, 220, 300, prof / 70, GOLD, z.profitLabel || 'PROFITS AFTER TAX', z.hideProfit ? '' : `$${prof.toFixed(0)}`, hot === 'profit')}
      {jar(cx + 520, f + 40, 220, 300, oth / 70, GREY, z.otherLabel || 'EVERYTHING ELSE', z.hideOther ? '' : `$${oth.toFixed(0)}`, hot === 'other')}
      {yr && <g transform={`translate(${cx - 520} 160) rotate(-4)`}><circle r={86} fill={RED} stroke={OL} strokeWidth={6} /><T x={0} y={18} s={fit(yr, 150, 52)} c="#FFFFFF">{yr}</T></g>}
      {z.note && <T x={cx} y={f + 160} s={fit(z.note, 1700, 22)} c="#4A5870" w={700}>{z.note}</T>}
    </g>;
  },

  /** 100 households on a hill, sorted by wealth; share stacks per group */
  sharestreet: (t, z, f) => {
    const gs: any[] = z.groups || [], fa = z.flowAt;
    const X = [-200, 480, 1100, 1660], W = [560, 520, 300, 120];
    return <g>
      {sky(z, f, '#86CDEF', '#F1F8FD', 'ssky' + Math.round(z.x0))}
      {clouds(z, t, 3)}
      {ground(z, f + 40, '#B7D7A0', '#9CC487')}
      {gs.map((g, k) => { const x = X[k] ?? 0, w = W[k] ?? 200, n = Math.min(g.n ?? 10, 40), on = t >= (g.at ?? 0), baseY = f - 40 - [0, 40, 120, 220][k];
        const cols = Math.max(1, Math.round(w / 52)), hs = k === 3 ? 1.3 : k === 2 ? 0.75 : 0.42;
        const stacks = Math.max(0, Math.round((g.v ?? 0) * 0.55)), sh = on ? E.out(win(t, (g.at ?? 0) + 0.3, 1.0)) : 0, ns = Math.round(stacks * sh), top = -Math.ceil(ns / 4) * 14;
        return <g key={'gp' + k}>
          <rect x={x - 30} y={baseY} width={w + 60} height={f + 40 - baseY} rx={10} fill={['#B7D7A0', '#A9D18E', '#9CC487', '#8DBB6F'][k]} stroke={OL} strokeWidth={4} />
          {Array.from({length: n}, (_, q) => house(x + (q % cols) * (w / cols) + (k === 3 ? 60 : 20), baseY - Math.floor(q / cols) * 22 + 4, hs * (k === 3 ? 1 : 0.6), q + k, ['#F1D9B5', '#E8C7A0', '#F5E6CC', '#DCE8F5'][q % 4]))}
          <g transform={`translate(${x + w / 2} ${baseY - (k === 3 ? 230 : k === 2 ? 150 : 140)})`}>
            {Array.from({length: ns}, (_, q) => cert((q % 4) * 26 - 39, -Math.floor(q / 4) * 14, 0.7, 'sc' + k + q))}
            {on && g.display && <g transform={`translate(0 ${top - 60}) scale(${pop(t, g.at ?? 0)})`}>
              <rect x={-120} y={-34} width={240} height={60} rx={14} fill={g.color || BLUE} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={30} c="#FFFFFF">{g.display || ''}</T></g>}
          </g>
          <T x={x + w / 2} y={f + 80} s={fit(g.label || '', w + 140, 30)}>{g.label || ''}</T>
        </g>; })}
      {fa !== undefined && t >= fa && Array.from({length: 8}, (_, k) => { const u = ((t - fa) * 0.5 + k / 8) % 1; return flyer(100, f - 120, 1720, f - 760, u, 'sf' + k, 120); })}
      {z.foot && <T x={960} y={f + 140} s={20} c="#4A5870" w={700}>{z.foot}</T>}
    </g>;
  },

  /** AI data-center campuses + chip shop */
  dcfield: (t, z, f) => {
    const cs: any[] = z.camps || [], ca = z.chipAt, mg = clamp(kf(z.margin, t, 0));
    return <g>
      {sky(z, f, '#8FD0F4', '#EEF8FD', 'dcsky' + Math.round(z.x0))}
      {clouds(z, t, 3)}
      {ground(z, f, '#C8C1A8', '#B0A88C')}
      {cs.map((c, k) => { const x = -280 + k * 520, at = c.at ?? 0, b = t < at ? 0.15 : 0.15 + 0.85 * E.out(win(t, at, 1.6)), v = c.v ?? 0, gh = v * 1.6 * E.out(win(t, at + 0.4, 1.4));
        return <g key={'cp' + k}>
          {crane(x + 380, f, 0.75, t, k)}
          {dchall(x, f, 360, 210, t, k, b)}
          {plaque(x + 180, f + 60, c.name || '', '#FFFFFF', 26)}
          {t >= at && <g><rect x={x + 130} y={f - 280 - gh} width={100} height={gh} rx={8} fill={GOLD} stroke={OL} strokeWidth={4} />
            {Array.from({length: Math.floor(gh / 26)}, (_, q) => coin(x + 180, f - 296 - q * 26, 0.75, 'g' + k + q, t * 2 + q))}
            {c.display && <g transform={`translate(${x + 180} ${f - 320 - gh}) scale(${pop(t, at + 1.2)})`}><rect x={-100} y={-30} width={200} height={50} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
              <T x={0} y={6} s={fit(c.display || '', 180, 30)}>{c.display || ''}</T></g>}</g>}
        </g>; })}
      {ca !== undefined && t >= ca && <g transform={`translate(${z.chipX ?? 1900} ${f}) scale(${pop(t, ca)})`}>
        <rect x={-180} y={-260} width={360} height={260} rx={10} fill="#7357C9" stroke={OL} strokeWidth={6} />
        <path d="M -200 -260 L 0 -340 L 200 -260 Z" fill="#5A43A8" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <g transform="translate(0 -150)"><rect x={-60} y={-60} width={120} height={120} rx={10} fill="#2B3440" stroke={OL} strokeWidth={5} />
          {[-40, -13, 13, 40].map((q) => <path key={q} d={`M ${q} -60 L ${q} -80 M ${q} 60 L ${q} 80 M -60 ${q} L -80 ${q} M 60 ${q} L 80 ${q}`} stroke={GOLD} strokeWidth={6} />)}
          <rect x={-30} y={-30} width={60} height={60} rx={6} fill="#5EE6FF" opacity={0.6 + 0.4 * Math.sin(t * 5)} /></g>
        <T x={0} y={-290} s={28} c="#FFFFFF">CHIP SHOP</T>
        {mg > 0 && <g transform="translate(0 -470)"><circle r={90} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <path d={`M 0 0 L 0 -86 A 86 86 0 ${mg > 0.5 ? 1 : 0} 1 ${86 * Math.sin(mg * 2 * Math.PI)} ${-86 * Math.cos(mg * 2 * Math.PI)} Z`} fill={GOLD} stroke={OL} strokeWidth={4} />
          <T x={0} y={130} s={fit(z.marginText || '', 380, 26)} c={OL} st="#FFFFFF" sw={6}>{z.marginText || ''}</T></g>}
      </g>}
      {z.foot && <T x={960} y={f + 160} s={20} c="#4A5870" w={700}>{z.foot}</T>}
    </g>;
  },

  /** the money loop: BUSINESS -> CLOUD -> CHIPS -> SHAREHOLDERS */
  moneyloop: (t, z, f) => {
    const cx = 960, cy = 470, R = 300, la = z.loopAt ?? 0, oa = z.outAt, da = z.doorAt;
    const st = [{n: 'BUSINESS', c: BLUE}, {n: 'CLOUD', c: TEAL}, {n: 'CHIPS', c: PURPLE}, {n: 'SHAREHOLDERS', c: GOLD}];
    return <g>
      {sky(z, f, '#9AD5F5', '#F3FAFE', 'mlsky' + Math.round(z.x0))}
      {clouds(z, t, 3)}
      {ground(z, f)}
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={OL} strokeWidth={34} /><circle cx={cx} cy={cy} r={R} fill="none" stroke="#E9EEF4" strokeWidth={24} />
      <circle cx={cx} cy={cy} r={R} fill="none" stroke={GOLD} strokeWidth={8} strokeDasharray="30 30" strokeDashoffset={-t * 120} opacity={t >= la ? 1 : 0.2} />
      {st.map((s, k) => { const a = -Math.PI / 2 + k * Math.PI / 2, x = cx + R * Math.cos(a), y = cy + R * Math.sin(a), at = (z.stAt || [])[k] ?? la;
        return t >= at ? <g key={'st' + k} transform={`translate(${x} ${y}) scale(${pop(t, at)})`}>
          <rect x={-130} y={-60} width={260} height={110} rx={20} fill={s.c} stroke={OL} strokeWidth={5} />
          <T x={0} y={12} s={fit(s.n, 240, 34)} c="#FFFFFF" st={OL} sw={5}>{s.n}</T></g> : null; })}
      {t >= la && Array.from({length: 10}, (_, k) => { const a = -Math.PI / 2 + ((t - la) * 0.7 + k / 10) * 2 * Math.PI; return coin(cx + R * Math.cos(a), cy + R * Math.sin(a), 0.8, 'ml' + k, t * 4 + k); })}
      {oa !== undefined && t >= oa && <g transform={`translate(${1560} ${f}) scale(${pop(t, oa)})`}>{fig(0, 0, 1.6, 2, t, 'vest')}
        <g transform="translate(0 -300)"><circle r={44} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={18} s={54} c={RED}>?</T></g>
        {plaque(0, 70, 'TASK AUTOMATED', '#FFFFFF', 22)}</g>}
      {da !== undefined && t >= da && <g opacity={clamp((t - da) / 0.4)}>
        <path d={`M 1480 ${f - 200} Q 1380 ${cy + 120} ${cx + R * 0.72} ${cy + R * 0.72}`} stroke={GREEN} strokeWidth={10} strokeDasharray="22 16" strokeDashoffset={-t * 60} fill="none" />
        {plaque(1330, cy + 260, 'UNLESS: OWNS SHARES', GREEN, 24, '#FFFFFF')}</g>}
    </g>;
  },

  /** evidence lab: FINDINGS board vs FORECASTS board */
  evidencelab: (t, z, f) => {
    const cards: any[] = z.cards || [], C: Record<string, string> = {finding: GREEN, forecast: ORANGE, descriptive: TEAL};
    let nl = 0, nr = 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EAF3F8" />
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 160)}, (_, k) => <rect key={'tl' + k} x={z.x0 + k * 160} y={f - 40} width={150} height={40} fill={k % 2 ? '#DDE7EE' : '#E8EFF4'} />)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C9D3DC" />
      {[[80, 'FINDINGS · MEASURED', GREEN], [1000, 'FORECASTS · MODELS', ORANGE]].map(([x, l, c], k) => <g key={'bd' + k}>
        <rect x={Number(x)} y={150} width={840} height={600} rx={18} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <rect x={Number(x)} y={150} width={840} height={70} rx={18} fill={String(c)} stroke={OL} strokeWidth={6} />
        <T x={Number(x) + 420} y={198} s={34} c="#FFFFFF">{String(l)}</T>
        {k === 1 && <g transform={`translate(${Number(x) + 760} 700)`}><circle r={46} fill="#D9C8FF" stroke={OL} strokeWidth={4} opacity={0.9} /><circle cx={-14} cy={-14} r={12} fill="#FFFFFF" opacity={0.7 + 0.3 * Math.sin(t * 3)} />
          <rect x={-36} y={40} width={72} height={18} rx={6} fill="#7A5C3E" stroke={OL} strokeWidth={3} /></g>}
        {k === 0 && <g transform={`translate(${Number(x) + 770} 700)`}><rect x={-12} y={-60} width={24} height={70} rx={8} fill="#BFE6F7" stroke={OL} strokeWidth={3} /><rect x={-12} y={-20 - 20 * Math.sin(t * 2) ** 2} width={24} height={30 + 20 * Math.sin(t * 2) ** 2} rx={8} fill={GREEN} /></g>}
      </g>)}
      {cards.map((c, k) => { const at = c.at ?? 0; if (t < at) return null; const right = c.kind === 'forecast', slot = right ? nr++ : nl++;
        const x = (right ? 1000 : 80) + 420, y = 290 + slot * 150, col = C[c.kind] || GREEN;
        return <g key={'cd' + k} transform={`translate(${x} ${y}) scale(${pop(t, at)}) rotate(${(k % 2 ? 1 : -1) * 1.2})`}>
          <rect x={-380} y={-56} width={760} height={120} rx={12} fill="#FFFBEA" stroke={col} strokeWidth={6} />
          <circle cx={0} cy={-56} r={9} fill={RED} stroke={OL} strokeWidth={2.5} />
          <T x={0} y={-6} s={fit(c.text || '', 720, 32)}>{c.text || ''}</T>
          {c.sub && <T x={0} y={36} s={fit(c.sub, 720, 20)} c="#4A5870" w={700}>{c.sub}</T>}</g>; })}
    </g>;
  },

  /** 1830s British mill town by day + a sky chart: output per worker vs real wage */
  millyard: (t, z, f) => {
    const p = clamp(kf(z.prog, t, 1)), pa = z.pauseAt, ca = z.catchAt;
    const X0 = 260, X1 = 1660, Y0 = 520, Y1 = 150;
    const outY = (u: number) => Y0 - (Y0 - Y1) * (0.05 + 0.9 * u);
    const wageY = (u: number) => Y0 - (Y0 - Y1) * (u < 0.55 ? 0.05 + 0.06 * u : 0.083 + 0.9 * (u - 0.55) * 1.0);
    const path = (fn: (u: number) => number) => Array.from({length: 41}, (_, k) => k / 40).filter((u) => u <= p).map((u, k) => `${k ? 'L' : 'M'} ${X0 + (X1 - X0) * u} ${fn(u)}`).join(' ');
    return <g>
      {sky(z, f, '#A9D6F0', '#F4EEDF', 'mysky' + Math.round(z.x0))}
      {clouds(z, t, 3)}
      {/* mills */}
      {[[-200, 380, 260], [260, 300, 200], [1300, 420, 300], [1820, 320, 220]].map(([x, w, h], k) => <g key={'ml' + k}>
        {[0, 1].map((q) => { const cx = Number(x) + 40 + q * 120; return <g key={q}><rect x={cx} y={f - Number(h) - 200} width={36} height={210} fill={BRICK} stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((r) => { const u = ((t * 0.3 + r / 3 + q * 0.3) % 1); return <circle key={r} cx={cx + 18 + u * 50} cy={f - Number(h) - 210 - u * 140} r={14 + u * 26} fill="#A3A9B2" opacity={(1 - u) * 0.7} />; })}</g>; })}
        <rect x={Number(x)} y={f - Number(h)} width={Number(w)} height={Number(h)} fill="#C2694E" stroke={OL} strokeWidth={5} />
        {Array.from({length: Math.floor(Number(h) / 60)}, (_, r) => Array.from({length: Math.floor(Number(w) / 56)}, (_, c) => <rect key={r + '-' + c} x={Number(x) + 14 + c * 56} y={f - Number(h) + 18 + r * 60} width={30} height={36} fill="#FFE9A8" stroke={OL} strokeWidth={2} />))}
      </g>)}
      <rect x={z.x0} y={f - 50} width={z.x1 - z.x0} height={50} fill="#6FA6C9" />
      {Array.from({length: 14}, (_, k) => <path key={'cw' + k} d={`M ${z.x0 + k * 260 + ((t * 25) % 260)} ${f - 28} q 20 -7 40 0`} stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.6} />)}
      {ground(z, f, '#B9C79A', '#9FAE7E')}
      {/* sky chart */}
      <g>
        <rect x={X0 - 70} y={Y1 - 90} width={X1 - X0 + 140} height={Y0 - Y1 + 150} rx={20} fill="#FFFFFF" fillOpacity={0.92} stroke={OL} strokeWidth={5} />
        <path d={`M ${X0} ${Y0} L ${X1} ${Y0} M ${X0} ${Y0} L ${X0} ${Y1 - 20}`} stroke={OL} strokeWidth={4} />
        {['1780', '1800', '1820', '1840', '1860', '1880'].map((l, k) => <T key={l} x={X0 + (X1 - X0) * (k / 5)} y={Y0 + 34} s={20} c="#4A5870">{l}</T>)}
        {pa !== undefined && t >= pa && <g opacity={clamp((t - pa) / 0.6)}><rect x={X0 + (X1 - X0) * 0.2} y={Y1 - 20} width={(X1 - X0) * 0.35} height={Y0 - Y1 + 20} fill={RED} opacity={0.12} />
          <T x={X0 + (X1 - X0) * 0.375} y={Y1 + 10} s={30} c={RED}>ENGELS' PAUSE</T></g>}
        <path d={path(outY)} stroke={BLUE} strokeWidth={9} fill="none" strokeLinecap="round" />
        <path d={path(wageY)} stroke={ORANGE} strokeWidth={9} fill="none" strokeLinecap="round" />
        {p > 0.1 && <g><T x={X0 + (X1 - X0) * Math.min(p, 0.95)} y={outY(Math.min(p, 0.95)) - 22} s={24} c={BLUE}>OUTPUT PER WORKER</T>
          <T x={X0 + (X1 - X0) * Math.min(p, 0.95)} y={wageY(Math.min(p, 0.95)) + 40} s={24} c={ORANGE}>REAL WAGE</T></g>}
        {ca !== undefined && t >= ca && <T x={X0 + (X1 - X0) * 0.82} y={Y0 - 60} s={24} c={GREEN} o={clamp((t - ca) / 0.5)}>WAGES CATCH UP</T>}
        <T x={(X0 + X1) / 2} y={Y0 + 66} s={18} c="#4A5870" w={700}>{z.chartNote || "ILLUSTRATIVE SHAPE OF ALLEN'S FINDINGS (BRITAIN) · NOT PLOTTED DATA"}</T>
      </g>
    </g>;
  },

  /** a street of doors: old jobs fade, new jobs pop */
  newjobs: (t, z, f) => {
    const old: any[] = z.old || [], fresh: any[] = z.fresh || [];
    return <g>
      {sky(z, f, '#86CDEF', '#F1F8FD', 'njsky' + Math.round(z.x0))}
      {clouds(z, t)}
      {ground(z, f)}
      {Array.from({length: 7}, (_, k) => { const x = -300 + k * 360, h = 380 + (k % 3) * 60; return <g key={'sh' + k}>
        <rect x={x} y={f - h} width={320} height={h} fill={['#F1D9B5', '#DCE8F5', '#E8C7A0', '#E3F2DA', '#F5E6CC', '#E6DDF5', '#FDE2D0'][k]} stroke={OL} strokeWidth={5} />
        <rect x={x + 110} y={f - 170} width={100} height={170} rx={6} fill="#7A4E2D" stroke={OL} strokeWidth={4} />
        <rect x={x + 30} y={f - h + 40} width={60} height={60} fill={GLASS} stroke={OL} strokeWidth={3} /><rect x={x + 230} y={f - h + 40} width={60} height={60} fill={GLASS} stroke={OL} strokeWidth={3} /></g>; })}
      {old.map((o, k) => { const x = -140 + (o.slot ?? k) * 360, gone = t >= (o.at ?? 0) ? clamp((t - (o.at ?? 0)) / 0.8) : 0;
        return <g key={'od' + k} opacity={1 - 0.75 * gone} transform={`translate(${x} ${f - 250}) rotate(${gone * 14})`}>
          <rect x={-150} y={-34} width={300} height={56} rx={8} fill="#D7D2C8" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(o.text, 280, 24)} c="#5A5348">{o.text}</T>
          {gone > 0.3 && <path d="M -140 -20 L 140 14" stroke={RED} strokeWidth={6} />}</g>; })}
      {fresh.map((o, k) => { const at = o.at ?? 0; if (t < at) return null; const x = -140 + (o.slot ?? k) * 360;
        return <g key={'fr' + k} transform={`translate(${x} ${f - 330 - (o.up ?? 0)}) scale(${pop(t, at)})`}>
          <rect x={-150} y={-34} width={300} height={56} rx={8} fill={GREEN} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(o.text, 280, 24)} c="#FFFFFF">{o.text}</T>
          <path d="M 120 -48 l 8 -18 l 8 18 l 18 8 l -18 8 l -8 18 l -8 -18 l -18 -8 Z" fill={GOLD} stroke={OL} strokeWidth={2} transform={`rotate(${t * 40} 128 -40)`} /></g>; })}
    </g>;
  },

  /** three doors to ownership (education, not advice) */
  doorways: (t, z, f) => {
    const ds: any[] = z.doors || [], ra = z.riskAt, rk = pick(z.risks, t, '');
    return <g>
      {sky(z, f, '#8FD0F4', '#F2F9FD', 'dwsky' + Math.round(z.x0))}
      {clouds(z, t, 3)}
      {ground(z, f, '#C5DDB2', '#A9C98F')}
      <rect x={-100} y={f - 520} width={2120} height={520} fill="#F5E6CC" stroke={OL} strokeWidth={6} />
      <path d={`M -140 ${f - 520} L 960 ${f - 680} L 2060 ${f - 520} Z`} fill="#5B6F8F" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      {ds.map((d, k) => { const x = 360 + k * 600, at = d.at ?? 0, o = t >= at ? E.inOut(win(t, at, 0.8)) : 0;
        return <g key={'dr' + k}>
          <rect x={x - 130} y={f - 380} width={260} height={380} fill="#FFF6D8" stroke={OL} strokeWidth={5} />
          {o > 0 && <g opacity={o}>
            {k === 0 && Array.from({length: 4}, (_, q) => coin(x - 60 + q * 40, f - 80 - ((t * 40 + q * 30) % 160), 0.9, 'd0' + q, t * 3 + q))}
            {k === 1 && Array.from({length: 12}, (_, q) => <rect key={q} x={x - 100 + (q % 4) * 52} y={f - 330 + Math.floor(q / 4) * 70} width={40} height={50} rx={4} fill={[BLUE, GOLD, GREEN, PURPLE, TEAL, ORANGE][q % 6]} stroke={OL} strokeWidth={2.5} />)}
            {k === 2 && <g>{fig(x - 40, f - 20, 1.1, 3, t, 'vest')}{cert(x + 60, f - 200, 1.0, 'd2')}</g>}
          </g>}
          <g transform={`translate(${x - 130} ${f - 380}) scale(${1 - 0.85 * o} 1)`}><rect x={0} y={0} width={260} height={380} fill={d.color || BLUE} stroke={OL} strokeWidth={5} />
            <circle cx={225} cy={200} r={12} fill={GOLD} stroke={OL} strokeWidth={3} /></g>
          {plaque(x, f - 430, d.label || '', '#FFFFFF', 30)}
          {d.sub && t >= at && <T x={x} y={f + 60} s={fit(d.sub, 540, 24)} c={OL} o={o}>{d.sub}</T>}
        </g>; })}
      {banner(960, 70, z.bannerText || 'EDUCATION, NOT INVESTMENT ADVICE · NOTHING HERE IS A RECOMMENDATION', NAVY, 24)}
      {ra !== undefined && t >= ra && <g transform={`translate(960 ${f - 600}) scale(${pop(t, ra)})`}>
        <g transform={`rotate(${8 * Math.sin(t * 1.6)})`}><rect x={-360} y={-12} width={720} height={24} rx={10} fill="#8B5E3C" stroke={OL} strokeWidth={4} />
          {coin(-300, -40, 1.4, 'sw1', t * 2)}<g transform="translate(300 -46)"><path d="M -40 30 L 0 -40 L 40 30 Z" fill={RED} stroke={OL} strokeWidth={4} strokeLinejoin="round" /><T x={0} y={22} s={36} c="#FFFFFF">!</T></g></g>
        <path d="M -30 60 L 0 12 L 30 60 Z" fill={GREY} stroke={OL} strokeWidth={4} />
        {rk && <g transform="translate(0 -130)"><rect x={-330} y={-34} width={660} height={58} rx={14} fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={fit(rk, 620, 30)} c="#FFFFFF">{rk}</T></g>}
      </g>}
    </g>;
  },

  /** title card: robots carry the letters in */
  rrtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['WHO GETS RICH', 'WHEN ROBOTS', 'DO THE WORK?'];
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#FFF3D6" />
      {Array.from({length: 24}, (_, k) => <path key={'rr' + k} d={`M ${-200 + k * 100} -200 L ${-200 + k * 100 + 900} 1300`} stroke="#FFE6B0" strokeWidth={40} />)}
      {lines.map((ln, k) => { const at = 0.3 + k * 0.6, u = E.outBack(win(t, at, 0.7)), x = lerp(-900, 960, u);
        return t >= at ? <g key={k}><T x={x} y={330 + k * 170} s={fit(ln, 1500, 150)} c={k === lines.length - 1 ? GOLD : NAVY} st={OL} sw={k === lines.length - 1 ? 14 : 0}>{ln}</T>
          {u < 0.98 && boltBot(x - 700, 330 + k * 170 + 60, 0.9, t, 'tt' + k, 'none')}</g> : null; })}
      {z.sub && t >= 2.2 && <g transform="translate(960 870)"><rect x={-620} y={-42} width={1240} height={66} rx={33} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={0} y={4} s={fit(z.sub, 1180, 32)} c="#FFFFFF">{z.sub}</T></g>}
      <T x={960} y={140} s={34} c={ORANGE}>THE HIDDEN ECONOMICS</T>
      {t >= 2.0 && boltBot(lerp(2100, 1600, E.out(win(t, 2.0, 1.0))), 1060, 1.2, t, 'tb', 'coin')}
    </g>;
  },

  /** act bumper: a conveyor belt delivers a crate with the act number */
  rrbumper: (t, z, f) => {
    const c = z.color || BLUE, u = E.out(win(t, 0.1, 1.0));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 14}, (_, k) => <circle key={'bd' + k} cx={(k * 170 + t * 40) % 2200 - 100} cy={140 + (k % 3) * 60} r={10} fill="#FFFFFF" opacity={0.25} />)}
      <rect x={-200} y={700} width={2400} height={60} fill="#4A5A70" stroke={OL} strokeWidth={6} />
      {Array.from({length: 26}, (_, k) => <circle key={'rl' + k} cx={-200 + k * 96 + ((t * 200) % 96)} cy={730} r={20} fill="#2B3440" stroke={OL} strokeWidth={3} />)}
      <g transform={`translate(${lerp(-400, 520, u)} 700)`}>
        <rect x={-150} y={-300} width={300} height={300} rx={10} fill="#D9A066" stroke={OL} strokeWidth={6} /><path d="M -150 -200 L 150 -200" stroke="#9C6B3E" strokeWidth={6} />
        <T x={0} y={-30} s={170} c="#FFFFFF" st={OL} sw={10}>{z.num || '1'}</T></g>
      {boltBot(lerp(-700, 220, u), 700, 1.2, t, 'bmp', 'none')}
      <g transform={`translate(1230 ${430 - 20 * pop(t, 1.0)})`}><rect x={-580} y={-90} width={1160} height={130} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={0} y={0} s={fit(z.title || '', 1100, 56)} c="#FFFFFF">{z.title || ''}</T></g>
      {t >= 1.4 && <T x={1230} y={600} s={fit(z.caption || '', 1100, 32)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.4) / 0.3)}>{z.caption || ''}</T>}
    </g>;
  },
};

/** rrtag: FACT / FINDING / FORECAST / DESCRIPTIVE / OUR MATH / ILLUSTRATIVE / EDUCATION pill (top-left) */
const TAGC: Record<string, string> = {FACT: GREEN, FINDING: GREEN, FORECAST: ORANGE, DESCRIPTIVE: TEAL, OUR: PURPLE, ILLUSTRATIVE: PURPLE, MECHANISM: BLUE, EDUCATION: NAVY, VERDICT: RED, HISTORY: BRICK, QUESTION: PURPLE};
const rrtag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const txt: string = pick(a.tags, t, a.text || 'FACT'); if (!txt) return null;
  const key = txt.split(/[ ,·]/)[0], c = TAGC[key] || NAVY, w = txt.length * 17 + 70, x = kf(a.x, t, 36), y = kf(a.y, t, 36);
  return <g key={'rt' + i} transform={`translate(${x} ${y}) scale(${pop(t, at, 0.35)})`}>
    <rect x={0} y={0} width={w} height={46} rx={23} fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={26} cy={23} r={9} fill="#FFFFFF" /><T x={44} y={32} s={24} a="start" c="#FFFFFF">{txt}</T></g>;
};

/** bolt: the original helper robot as a free item */
const bolt: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f + 60), s = (a.scale ?? 1) * pop(t, at, 0.4), carry = pick(a.carries, t, a.carry || 'none'), mood = pick(a.moods, t, a.mood || 'happy');
  return <g key={'bo' + i} transform={a.flip ? `translate(${2 * x} 0) scale(-1 1)` : undefined}>{boltBot(x, y, s, t, 'it' + i, carry, mood)}</g>;
};

export const ROBOTSRICH_ITEMS: Record<string, ItemFn> = {rrtag, bolt};
export const ROBOTSRICH_INDOOR = ['splitter', 'evidencelab', 'rrtitle', 'rrbumper'];
