import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * CANADA kit for CartoonStage (Episode 70, "Why Canada Could Be the Biggest Winner of the AI Boom").
 *
 * Prime-time TV-cartoon GENRE (thick clean outlines, flat colour, squash and stretch), day scenes, everything ORIGINAL: MAYA (a fictional young
 * AI researcher in Montreal, drawn with the shared `toon` rig), LUC (her dad, a fictional Sudbury miner, `toon` rig) and WHIRR (a fictional walking
 * data center that flees the desert heat for the north). No logos, no flags, no maple-leaf symbols, no real person drawn; companies appear only as
 * plain plaques when the narration names them. Places are landscapes (rivers, dams, rock and lakes, snow), never stereotypes.
 * Sets:
 *  - caapt: Maya's Montreal apartment by day: a window on a street of triplexes with outdoor staircases, desk + laptop, a giant phone
 *    (`phone` KF 0..1) whose feed shows headline cards (`feed` [[t, text]]), an offer card sliding in (`offer` t, `offerText`).
 *  - cadesert: a hot desert campus: pulsing sun, heat shimmer, a data hall with roof fans (`fans` KF speed), a thermometer (`temp` KF 0..1) and
 *    a spinning power meter (`meter` KF 0..1), a sign (`sign` [[t, text]]).
 *  - cachart: a city street with a billboard chart whose line draws (`draw` KF 0..1: rise, the spring dip, the rebound), a car-parts shop with a
 *    shutter (`closed` KF 0..1), a stamp (`stamp` [[t, text]]), `focus` 'dip' | 'rebound' ring.
 *  - camap: an original stylized map of the north (not a traced outline) with pins (`pins` [{x, y, label, at}]), Whirr's dashed route from the
 *    desert (`route` KF 0..1) and the AI shopping list card (`ticks` KF 0..4: A PLUG, A FRIDGE, A MINE, A BRAIN).
 *  - cadam: a river valley, an arch dam with spillway (`spill` KF 0..1), turbines, pylons with power pulses (`flow` KF 0..1), `plaque`,
 *    a price tag (`price` [[t, text]]), a permission boom gate (`gate` t), a stamp (`stamp` [[t, text]]), `variant` 'quebec' | 'bc'.
 *  - castage: B.C.'s power talent show: a stage between mountains, sweeping spotlights, a POWER LEFT meter (`left` KF 0..1), a line of small
 *    data-center cubes waiting (`n` KF 0..8), `lit` [[t, i]] spotlight on one cube, banner `title`.
 *  - cacold: a snowy field: pines, snowfall, a data hall breathing cold air in (`air` KF 0..1), a heat pipe to a campus (`pipe` KF 0..1,
 *    `campus` text), a crane raising a new hall (`build` KF 0..1), a lot sign (`lot` t).
 *  - camine: Canadian-shield rock and lakes, a headframe with spinning wheels, ore carts, mineral gems popping (`gems` KF 0..5: CU, NI, LI,
 *    C, U), a wall calendar counting years (`years` KF 0..16), a stamp (`stamp` [[t, text]]).
 *  - calab: a Montreal AI lab: snowy street window, a whiteboard neural net lighting up (`net` KF 0..1), racks, a monitor (`screen`
 *    [[t, text]]), a supercomputer tower assembling (`super` KF 0..1).
 *  - caborder: a river crossing: trucks of goods drive across a bridge to a big market building (`trucks` on; `share` 0..1 of trucks that
 *    cross), a tariff barrier (`tariff` t), a glowing cable under the river carrying data packets (`cable` KF 0..1).
 *  - careceipt: the AI shopping receipt printing from a register (`print` KF 0..1), rows [{label, note, at, mark: 'yes' | 'catch'}].
 *  - catitle / cabumper: title card (a snowy hill, the title, snow) and chapter bumpers (a snowball rolls in and becomes the title panel).
 * Items: whirr (WHIRR: `x` KF, `y`, `face`/`faces` happy | worry | wow | hot | calm, `hops`, `fan` KF speed, `sweat` [t0, t1], `frost` t
 *  (cold breath puffs), `scarf` t (a scarf pops on), `carry` 'suitcase', `wave` t, `label`).
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
const lastAt = (tl: any, t: number): number => { let v = -99; if (Array.isArray(tl)) for (const [pt] of tl) if (t >= Number(pt)) v = Number(pt); return v; };
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.6);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#1E88E5', GOLD = '#F5B700', RED = '#E5483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', PURPLE = '#7357C9', NAVY = '#1A2238', ORANGE = '#F08A24',
  CY = '#29C5F6', PAPER = '#FFFDF4', SNOW = '#F4F8FC', WATER = '#5AB4E8', ROCK = '#8C9BAE', PINE = '#2F7D5B', SAND = '#F2CF8A', BRICK = '#B5543C';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: any) => <path key={'cac' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const stamp = (x: number, y: number, txt: string, t: number, at: number, c = RED, s = 54) => { if (!txt || t < at) return null; const w = txt.length * s * 0.64 + 60, u = E.outBack(win(t, at, 0.35));
  return <g transform={`translate(${x} ${y}) rotate(-8) scale(${2 - u})`} opacity={clamp(u * 2)}><rect x={-w / 2} y={-s} width={w} height={s * 1.5} rx={8} fill="#FFFFFF" stroke={c} strokeWidth={8} opacity={0.96} />
    <T x={0} y={s * 0.32} s={s} c={c}>{txt}</T></g>; };
const ground = (z: Z, f: number, c = '#A6D08A', c2 = '#88B86C') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const hills = (z: Z, f: number, c = '#BFE3A0', k = 0, amp = 160) => { let d = `M ${z.x0} ${f}`; for (let x = z.x0; x <= z.x1 + 300; x += 300) d += ` Q ${x + 150} ${f - amp - 80 * rnd(k + x / 300)} ${x + 300} ${f}`;
  return <path d={d + ' Z'} fill={c} stroke={OL} strokeWidth={4} />; };
const peaks = (z: Z, base: number, h: number, c: string, k: number, snow = true) => { const out: React.ReactNode[] = [];
  for (let x = z.x0 - 200, q = 0; x < z.x1 + 200; x += 360, q++) { const hh = h * (0.7 + 0.5 * rnd(k + q)), w = 260 + 120 * rnd(k + q + 9);
    out.push(<g key={'pk' + k + q}><path d={`M ${x - w} ${base} L ${x} ${base - hh} L ${x + w} ${base} Z`} fill={c} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {snow && <path d={`M ${x - w * 0.28} ${base - hh * 0.72} L ${x} ${base - hh} L ${x + w * 0.28} ${base - hh * 0.72} L ${x + w * 0.12} ${base - hh * 0.66} L ${x} ${base - hh * 0.74} L ${x - w * 0.14} ${base - hh * 0.66} Z`} fill={SNOW} stroke={OL} strokeWidth={3} strokeLinejoin="round" />}</g>); }
  return <g>{out}</g>; };
const pine = (x: number, y: number, s: number, k: any, snowy = false) => <g key={'pn' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-10} y={-40} width={20} height={40} fill="#6D4C41" stroke={OL} strokeWidth={3} />
  {[0, 1, 2].map((q) => <path key={q} d={`M ${-70 + q * 14} ${-30 - q * 55} L 0 ${-120 - q * 55} L ${70 - q * 14} ${-30 - q * 55} Z`} fill={PINE} stroke={OL} strokeWidth={4} strokeLinejoin="round" />)}
  {snowy && [0, 1, 2].map((q) => <path key={'s' + q} d={`M ${-30 + q * 8} ${-95 - q * 55} L 0 ${-120 - q * 55} L ${30 - q * 8} ${-95 - q * 55} Q 0 ${-88 - q * 55} ${-30 + q * 8} ${-95 - q * 55} Z`} fill={SNOW} stroke={OL} strokeWidth={2.5} />)}</g>;
const snowfall = (z: Z, t: number, n = 60, k = 0) => <g>{Array.from({length: n}, (_, q) => { const x = z.x0 + rnd(q + k) * (z.x1 - z.x0) + 30 * Math.sin(t + q), y = ((t * (60 + 40 * rnd(q + 3)) + rnd(q + 7) * 1200) % 1200) - 100;
  return <circle key={'sn' + q} cx={x} cy={y} r={4 + 4 * rnd(q + 11)} fill="#FFFFFF" stroke="#BFD3E6" strokeWidth={1.5} />; })}</g>;
/** a generic data-hall building */
const hall = (x: number, y: number, s: number, k: any, t: number, glow = 1) => <g key={'hl' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-220} y={-200} width={440} height={200} fill="#DDE3EC" stroke={OL} strokeWidth={6} />
  <rect x={-230} y={-222} width={460} height={26} rx={6} fill="#9AA6B8" stroke={OL} strokeWidth={5} />
  {[0, 1, 2, 3, 4, 5].map((q) => <rect key={q} x={-190 + q * 64} y={-160} width={44} height={110} rx={4} fill="#263238" stroke={OL} strokeWidth={3} />)}
  {[0, 1, 2, 3, 4, 5].map((q) => [0, 1, 2].map((r) => <circle key={q + '-' + r} cx={-168 + q * 64} cy={-140 + r * 32} r={5} fill={(Math.floor(t * 3 + q + r * 2) % 3) ? CY : GREEN} opacity={glow} />))}
  <rect x={-40} y={-60} width={80} height={60} fill="#7A8699" stroke={OL} strokeWidth={4} /></g>;
const iconPlug = (s = 1) => <g transform={`scale(${s})`}><rect x={-30} y={-26} width={60} height={52} rx={12} fill={GOLD} stroke={OL} strokeWidth={5} /><path d="M -14 -26 L -14 -50 M 14 -26 L 14 -50" stroke={OL} strokeWidth={8} strokeLinecap="round" /><path d="M 0 26 Q 0 50 30 54" stroke={OL} strokeWidth={6} fill="none" /></g>;
const iconFlake = (s = 1) => <g transform={`scale(${s})`}>{[0, 60, 120].map((r) => <g key={r} transform={`rotate(${r})`}><path d="M 0 -44 L 0 44 M -12 -32 L 0 -22 L 12 -32 M -12 32 L 0 22 L 12 32" stroke={CY} strokeWidth={8} strokeLinecap="round" fill="none" /></g>)}<circle r={9} fill="#FFFFFF" stroke={OL} strokeWidth={3} /></g>;
const iconPick = (s = 1) => <g transform={`scale(${s})`}><path d="M -30 40 L 26 -24" stroke="#8D6E63" strokeWidth={10} strokeLinecap="round" /><path d="M -6 -44 Q 30 -40 50 -8 L 40 -2 Q 26 -24 0 -32 Z" fill={ROCK} stroke={OL} strokeWidth={4} /><circle cx={-24} cy={30} r={10} fill={GOLD} stroke={OL} strokeWidth={3} /></g>;
const iconBrain = (s = 1) => <g transform={`scale(${s})`}><path d="M -40 10 Q -50 -30 -14 -36 Q 0 -54 18 -36 Q 50 -34 42 2 Q 52 30 20 36 Q 0 50 -16 36 Q -50 36 -40 10 Z" fill="#F48FB1" stroke={OL} strokeWidth={5} /><path d="M 0 -34 Q -6 0 4 34 M -26 -10 Q -10 -2 -24 16 M 26 -12 Q 12 0 26 18" stroke={OL} strokeWidth={3.5} fill="none" /></g>;
const ICONS = [iconPlug, iconFlake, iconPick, iconBrain];

const RAW: Record<string, SetFn> = {
  /** Maya's Montreal apartment by day */
  caapt: (t, z, f) => {
    const ph = kf(z.phone, t, 0), feedAt = lastAt(z.feed, t), feed: string = pick(z.feed, t, ''), off = z.offer !== undefined ? E.outBack(win(t, z.offer, 0.6)) : 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#F6E7D3" />
      <rect x={z.x0} y={f - 260} width={z.x1 - z.x0} height={260} fill="#EAD3B6" stroke={OL} strokeWidth={4} />
      {/* window on the street */}
      <g transform="translate(560 150)"><rect x={0} y={0} width={760} height={520} rx={14} fill="#9ED8FF" stroke={OL} strokeWidth={8} />
        <clipPath id={'caw' + (z.ox ?? 0)}><rect x={8} y={8} width={744} height={504} rx={8} /></clipPath>
        <g clipPath={`url(#caw${z.ox ?? 0})`}>
          {cloud(160 + ((t * 10) % 300), 90, 0.7, 'w1')}{cloud(560 - ((t * 7) % 200), 70, 0.6, 'w2')}
          {[0, 1, 2].map((q) => { const x = 40 + q * 250, c = [BRICK, '#9C6B4E', '#C98A5B'][q];
            return <g key={q} transform={`translate(${x} 200)`}><rect x={0} y={0} width={220} height={330} fill={c} stroke={OL} strokeWidth={5} />
              {[0, 1, 2].map((r) => <g key={r}><rect x={24} y={30 + r * 100} width={56} height={60} fill="#FFF3C4" stroke={OL} strokeWidth={3} /><rect x={140} y={30 + r * 100} width={56} height={60} fill="#FFF3C4" stroke={OL} strokeWidth={3} />
                <rect x={0} y={96 + r * 100} width={220} height={8} fill="#5E6B85" /></g>)}
              <path d={`M 200 330 Q 260 270 200 210 Q 150 160 200 110`} stroke={OL} strokeWidth={7} fill="none" /><path d={`M 214 330 Q 274 270 214 210 Q 164 160 214 110`} stroke="#5E6B85" strokeWidth={4} fill="none" />
              <rect x={-6} y={-14} width={232} height={16} fill={SNOW} stroke={OL} strokeWidth={3} /></g>; })}
        </g><path d="M 380 0 L 380 520 M 0 260 L 760 260" stroke={OL} strokeWidth={8} /></g>
      {/* plant + desk */}
      <g transform="translate(340 760)"><rect x={-40} y={-60} width={80} height={60} fill={ORANGE} stroke={OL} strokeWidth={5} />{[-1, 0, 1].map((q) => <ellipse key={q} cx={q * 30} cy={-110 - Math.abs(q) * -20} rx={22} ry={56} fill={GREEN} stroke={OL} strokeWidth={4} transform={`rotate(${q * 25 + Math.sin(t * 1.5 + q) * 3} ${q * 30} -70)`} />)}</g>
      <g transform="translate(940 820)"><rect x={-330} y={-30} width={660} height={34} rx={6} fill="#A1887F" stroke={OL} strokeWidth={6} /><path d="M -300 4 L -300 200 M 300 4 L 300 200" stroke={OL} strokeWidth={14} />
        <g transform="translate(-60 -30)"><rect x={-130} y={-150} width={260} height={150} rx={10} fill="#37474F" stroke={OL} strokeWidth={6} /><rect x={-116} y={-136} width={232} height={122} rx={6} fill="#1E2A38" />
          {[0, 1, 2, 3].map((q) => <rect key={q} x={-100} y={-124 + q * 26} width={60 + 120 * rnd(q + Math.floor(t * 2))} height={10} rx={4} fill={[CY, GREEN, GOLD, PURPLE][q]} />)}
          <path d="M -160 0 L 160 0 L 140 14 L -140 14 Z" fill="#90A4AE" stroke={OL} strokeWidth={4} /></g>
        <g transform="translate(200 -30)"><path d="M -36 0 L -30 -70 L 30 -70 L 36 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} /><path d="M 30 -56 Q 60 -50 32 -22" stroke={OL} strokeWidth={5} fill="none" />{[0, 1].map((q) => <path key={q} d={`M ${-10 + q * 20} -84 q 8 -16 0 -30`} stroke="#B0BEC5" strokeWidth={4} fill="none" opacity={0.5 + 0.5 * Math.sin(t * 3 + q)} />)}</g></g>
      {/* giant phone */}
      {ph > 0.01 && <g transform={`translate(1560 ${560 + (1 - ph) * 700}) rotate(${4 * Math.sin(t * 9) * clamp(1 - (t - feedAt) * 2)})`}>
        <rect x={-190} y={-380} width={380} height={720} rx={50} fill={NAVY} stroke={OL} strokeWidth={8} /><rect x={-168} y={-340} width={336} height={640} rx={26} fill="#FFFFFF" />
        <rect x={-50} y={-366} width={100} height={14} rx={7} fill="#3A4560" />
        {feed && [0, 1, 2].map((q) => { const u = clamp((t - feedAt) * 3 - q * 0.5); return <g key={q} transform={`translate(0 ${-250 + q * 170 + (1 - u) * 60})`} opacity={u}>
          <rect x={-150} y={-66} width={300} height={140} rx={14} fill={q === 0 ? '#FFE3E0' : '#F1F4F8'} stroke={OL} strokeWidth={3} /><rect x={-130} y={-50} width={70} height={70} rx={10} fill={q === 0 ? RED : ROCK} />
          <T x={-50} y={-18} s={fit(feed, 190, 20)} a="start" c={q === 0 ? RED : NAVY}>{q === 0 ? feed : q === 1 ? 'ECONOMY IN TROUBLE?' : 'TARIFF NEWS'}</T>
          <rect x={-50} y={0} width={180} height={10} rx={5} fill="#C5CDD8" /><rect x={-50} y={22} width={130} height={10} rx={5} fill="#C5CDD8" /></g>; })}
        {off > 0 && <g transform={`translate(0 ${120 - 20 * Math.sin(t * 4)}) scale(${off})`}><rect x={-160} y={-90} width={320} height={190} rx={18} fill={GOLD} stroke={OL} strokeWidth={6} />
          <circle cx={-100} cy={-30} r={34} fill="#FFDD55" stroke={OL} strokeWidth={4} />{Array.from({length: 8}, (_, q) => <path key={q} d={`M ${-100 + 44 * Math.cos(q * 0.785 + t)} ${-30 + 44 * Math.sin(q * 0.785 + t)} L ${-100 + 58 * Math.cos(q * 0.785 + t)} ${-30 + 58 * Math.sin(q * 0.785 + t)}`} stroke={OL} strokeWidth={4} />)}
          <T x={40} y={-30} s={30} c={NAVY}>OFFER!</T><T x={0} y={50} s={fit(z.offerText || 'CALIFORNIA AI LAB', 290, 26)} c={NAVY}>{z.offerText || 'CALIFORNIA AI LAB'}</T></g>}
      </g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C79E74" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#A47B52" stroke={OL} strokeWidth={4} />
      {Array.from({length: 22}, (_, k) => <path key={'fb' + k} d={`M ${z.x0 + k * 240} ${f} L ${z.x0 + k * 240 - 60} ${f + 300}`} stroke="#A47B52" strokeWidth={4} />)}
    </g>;
  },

  /** the hot desert campus */
  cadesert: (t, z, f) => {
    const temp = kf(z.temp, t, 0.7), meter = kf(z.meter, t, 0.6), fans = kf(z.fans, t, 1), sign: string = pick(z.sign, t, '');
    return <g>
      {sky(z, f, '#FFB86B', '#FFE7B0', 'casd' + (z.ox ?? 0))}
      <g transform="translate(1650 190)"><circle r={110 + 8 * Math.sin(t * 4)} fill="#FFD54F" stroke={OL} strokeWidth={6} />{Array.from({length: 12}, (_, q) => { const a = q * 0.5236 + t * 0.4, r0 = 140 + 10 * Math.sin(t * 6 + q);
        return <path key={q} d={`M ${r0 * Math.cos(a)} ${r0 * Math.sin(a)} L ${(r0 + 60) * Math.cos(a)} ${(r0 + 60) * Math.sin(a)}`} stroke="#FF9800" strokeWidth={12} strokeLinecap="round" />; })}
        <circle cx={-34} cy={-10} r={10} fill={OL} /><circle cx={34} cy={-10} r={10} fill={OL} /><path d="M -40 40 Q 0 20 40 40" stroke={OL} strokeWidth={6} fill="none" /></g>
      {hills(z, f - 120, '#F0B872', 5, 120)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={SAND} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill="#E0B266" stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3, 4, 5].map((q) => <path key={'hs' + q} d={`M ${200 + q * 300} ${f - 20} q 30 -30 0 -60 q -30 -30 0 -60`} stroke="#FFFFFF" strokeWidth={5} fill="none" opacity={0.25 + 0.25 * Math.sin(t * 5 + q)} />)}
      {hall(820, f, 1.1, 'd1', t)}
      {[0, 1, 2, 3].map((q) => <g key={'rf' + q} transform={`translate(${620 + q * 130} ${f - 250})`}><rect x={-46} y={-30} width={92} height={36} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
        <g transform={`translate(0 -30) rotate(${t * 900 * fans})`}><path d="M 0 0 L 34 -8 L 34 8 Z M 0 0 L -34 -8 L -34 8 Z" fill={OL} /></g></g>)}
      {/* thermometer */}
      <g transform="translate(1500 860)"><rect x={-34} y={-480} width={68} height={460} rx={34} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><circle cy={-10} r={56} fill={RED} stroke={OL} strokeWidth={6} />
        <rect x={-18} y={-440 * temp - 20} width={36} height={440 * temp} rx={18} fill={RED} />{[0, 1, 2, 3, 4].map((q) => <path key={q} d={`M 34 ${-100 - q * 80} l 22 0`} stroke={OL} strokeWidth={4} />)}
        {temp > 0.8 && <T x={0} y={-520} s={40} c={RED}>HOT!</T>}</g>
      {/* power meter */}
      <g transform="translate(1800 760)"><rect x={-110} y={-110} width={220} height={200} rx={20} fill="#ECEFF1" stroke={OL} strokeWidth={6} /><circle cy={-20} r={70} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <path d={`M 0 -20 L ${60 * Math.cos(-Math.PI + meter * Math.PI + Math.sin(t * 20) * 0.05)} ${-20 + 60 * Math.sin(-Math.PI + meter * Math.PI)}`} stroke={RED} strokeWidth={8} strokeLinecap="round" />
        <T x={0} y={70} s={22}>POWER BILL</T></g>
      {sign && plaque(820, f - 300, sign, GOLD, 30)}
    </g>;
  },

  /** the crash street: a billboard chart */
  cachart: (t, z, f) => {
    const dr = kf(z.draw, t, 1), closed = kf(z.closed, t, 0), st: string = pick(z.stamp, t, ''), stAt = lastAt(z.stamp, t), focus: string = pick(z.focus, t, '');
    const P: [number, number][] = [[0, 0.55], [0.15, 0.6], [0.3, 0.66], [0.42, 0.7], [0.52, 0.48], [0.62, 0.52], [0.74, 0.64], [0.86, 0.7], [1, 0.74]];
    const W = 1100, Hh = 380, px = (u: number) => -W / 2 + u * W, py = (v: number) => Hh / 2 - v * Hh;
    let d = '', n = 0; for (let k = 0; k < P.length; k++) { if (P[k][0] > dr) break; d += (k ? ' L ' : 'M ') + px(P[k][0]) + ' ' + py(P[k][1]); n = k; }
    if (n < P.length - 1 && dr > P[n][0]) { const a = P[n], b = P[n + 1], u = (dr - a[0]) / (b[0] - a[0]); d += ` L ${px(lerp(a[0], b[0], u))} ${py(lerp(a[1], b[1], u))}`; }
    return <g>
      {sky(z, f, '#7EC8F2', '#DDF2FF', 'cach' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 300 + k * 800 + ((t * 12) % 600), 120 + 40 * (k % 2), 0.9, k))}
      {[0, 1, 2, 3, 4, 5, 6].map((q) => <rect key={'bd' + q} x={z.x0 + q * 380} y={f - 420 - 120 * rnd(q)} width={300} height={420 + 120 * rnd(q)} fill={['#C9D6E8', '#B7C7DD', '#D6E0EE'][q % 3]} stroke={OL} strokeWidth={4} />)}
      <g transform="translate(960 400)"><rect x={-W / 2 - 50} y={-Hh / 2 - 70} width={W + 100} height={Hh + 130} rx={16} fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        <path d={`M 0 ${Hh / 2 + 60} L 0 ${f - 400}`} stroke={OL} strokeWidth={16} />
        <T x={-W / 2} y={-Hh / 2 - 24} s={30} a="start" c={NAVY}>CANADA'S ECONOMY (ILLUSTRATIVE)</T>
        <path d={`M ${-W / 2} ${Hh / 2} L ${W / 2} ${Hh / 2}`} stroke="#C5CDD8" strokeWidth={4} />
        <path d={d} stroke={BLUE} strokeWidth={12} fill="none" strokeLinejoin="round" strokeLinecap="round" />
        {focus === 'dip' && <ellipse cx={px(0.52)} cy={py(0.5)} rx={90 + 8 * Math.sin(t * 6)} ry={70} fill="none" stroke={RED} strokeWidth={7} />}
        {focus === 'rebound' && <ellipse cx={px(0.86)} cy={py(0.7)} rx={110 + 8 * Math.sin(t * 6)} ry={80} fill="none" stroke={GREEN} strokeWidth={7} />}
        {stamp(0, 0, st, t, stAt)}</g>
      {/* car parts shop */}
      <g transform={`translate(${z.shopX ?? 1700} ${f})`}><rect x={-160} y={-260} width={320} height={260} fill="#FFF3DD" stroke={OL} strokeWidth={6} />{[0, 1, 2, 3, 4, 5, 6].map((s) => <path key={s} d={`M ${-160 + s * 46} -260 l 46 0 l -6 40 l -34 0 Z`} fill={s % 2 ? '#FFFFFF' : RED} stroke={OL} strokeWidth={3} />)}
        <rect x={-120} y={-190} width={240} height={150} fill="#BFE6F7" stroke={OL} strokeWidth={4} /><circle cx={-40} cy={-110} r={30} fill="none" stroke={OL} strokeWidth={10} /><circle cx={50} cy={-110} r={22} fill="none" stroke="#5E6B85" strokeWidth={8} />
        <rect x={-120} y={-190} width={240} height={150 * closed} fill="#9AA6B8" stroke={OL} strokeWidth={4} />{plaque(0, -290, 'CAR PARTS', '#FFFFFF', 22)}</g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#8F9AA8" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={16} fill="#C9CED6" stroke={OL} strokeWidth={4} />
      {Array.from({length: 30}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 220} y={f + 110} width={110} height={12} fill="#FFFFFF" />)}
    </g>;
  },

  /** the stylized map of the north + the AI shopping list */
  camap: (t, z, f) => {
    const route = kf(z.route, t, 0), ticks = kf(z.ticks, t, 0), pins: any[] = z.pins || [], list: string[] = z.list || ['A PLUG', 'A FRIDGE', 'A MINE', 'A BRAIN'];
    const land = 'M 120 330 Q 200 180 380 200 Q 470 120 600 170 Q 700 100 820 150 L 900 260 Q 960 330 1000 250 Q 1060 160 1160 210 Q 1250 260 1220 380 Q 1200 470 1100 520 L 1000 600 Q 900 640 800 600 L 700 640 Q 560 650 420 640 L 160 640 Q 90 520 120 330 Z';
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#CFE8F7" />
      {Array.from({length: 26}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + (k % 6) * 400 + 40 * Math.sin(t + k)} ${100 + Math.floor(k / 6) * 240} q 30 -16 60 0 t 60 0`} stroke="#9FCCEA" strokeWidth={4} fill="none" />)}
      <g transform="translate(60 60)">
        <path d={land} fill="#BFE3A0" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
        <path d="M 820 150 Q 880 300 860 380 Q 800 420 760 360 Q 760 260 820 150 Z" fill="#CFE8F7" stroke={OL} strokeWidth={5} />
        {Array.from({length: 7}, (_, q) => <path key={'mt' + q} d={`M ${200 + q * 40} ${600 - q * 50} l 30 -60 l 30 60 Z`} fill="#E6EEF5" stroke={OL} strokeWidth={3} />)}
        <path d="M 160 640 L 1000 640" stroke={OL} strokeWidth={5} strokeDasharray="20 14" /><T x={580} y={690} s={24} c="#5E6B85">THE U.S. BORDER (SIMPLIFIED)</T>
        <T x={620} y={420} s={64} c="#5C8A45" ls={10}>CANADA</T>
        {route > 0 && <path d={`M 360 980 Q 420 800 ${lerp(360, 700, route)} ${lerp(980, 560, route)}`} stroke={RED} strokeWidth={7} strokeDasharray="18 14" strokeDashoffset={-t * 60} fill="none" />}
        {route > 0 && <T x={360} y={1020} s={24} c={RED}>THE DESERT</T>}
        {pins.map((p, k) => { const u = pop(t, p.at ?? 0, 0.5); if (u <= 0) return null; return <g key={'pin' + k} transform={`translate(${p.x} ${p.y}) scale(${u})`}>
          <path d="M 0 0 C -30 -40 -30 -70 0 -70 C 30 -70 30 -40 0 0 Z" fill={p.c || RED} stroke={OL} strokeWidth={4} /><circle cy={-48} r={10} fill="#FFFFFF" />{plaque(0, -100, p.label, '#FFFFFF', 20)}</g>; })}
      </g>
      {/* shopping list */}
      {z.showList !== false && <g transform={`translate(1560 ${520 + 6 * Math.sin(t * 1.5)}) rotate(3)`}><rect x={-230} y={-360} width={460} height={720} rx={10} fill={PAPER} stroke={OL} strokeWidth={6} />
        <path d="M -230 -300 L 230 -300" stroke={RED} strokeWidth={4} /><T x={0} y={-318} s={34} c={NAVY}>AI'S SHOPPING LIST</T>
        {list.map((lb, k) => { const u = clamp(ticks - k); return <g key={'li' + k} transform={`translate(0 ${-200 + k * 150})`} opacity={0.35 + 0.65 * clamp(u * 3)}>
          <g transform="translate(-150 0)">{ICONS[k % 4](0.9)}</g><T x={-80} y={14} s={fit(lb, 220, 40)} a="start">{lb}</T>
          {u > 0.5 && <path d={`M 150 0 l 20 24 l 44 -54`} stroke={GREEN} strokeWidth={12} fill="none" strokeLinecap="round" strokeLinejoin="round" transform={`scale(${E.outBack(clamp((u - 0.5) * 2))})`} />}</g>; })}</g>}
    </g>;
  },

  /** a hydro dam in a river valley */
  cadam: (t, z, f) => {
    const spill = kf(z.spill, t, 0.8), flow = kf(z.flow, t, 1), price: string = pick(z.price, t, ''), prAt = lastAt(z.price, t), st: string = pick(z.stamp, t, ''), stAt = lastAt(z.stamp, t);
    const bc = z.variant === 'bc';
    return <g>
      {sky(z, f, '#6EC1F0', '#DDF2FF', 'cadm' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 200 + k * 700 + ((t * 10) % 500), 110 + 50 * (k % 2), 1, k))}
      {peaks(z, 560, bc ? 420 : 280, bc ? '#7F95B5' : '#8FB2A0', bc ? 3 : 7, true)}
      {hills(z, 640, '#6FAE6A', 4, 120)}
      {/* reservoir */}
      <path d={`M ${z.x0} 560 L 700 560 L 760 700 L ${z.x0} 700 Z`} fill={WATER} stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3].map((q) => <path key={'rw' + q} d={`M ${z.x0 + 100 + q * 180 + 20 * Math.sin(t + q)} ${600 + q * 20} q 20 -10 40 0 t 40 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.7} />)}
      {Array.from({length: 8}, (_, q) => pine(z.x0 + 60 + q * 150, 560, 0.55, 'rp' + q, bc))}
      {/* dam */}
      <path d="M 700 520 Q 860 470 1020 520 L 1060 860 L 660 860 Z" fill="#D7DCE3" stroke={OL} strokeWidth={8} strokeLinejoin="round" />
      {[0, 1, 2, 3, 4].map((q) => <path key={'dl' + q} d={`M ${720 + q * 70} 540 L ${700 + q * 80} 860`} stroke="#AEB7C4" strokeWidth={4} />)}
      {spill > 0.02 && <g>{[0, 1, 2].map((q) => <path key={'sp' + q} d={`M ${790 + q * 60} 540 Q ${800 + q * 60} 700 ${780 + q * 70} 860`} stroke={WATER} strokeWidth={36 * spill} fill="none" opacity={0.95} />)}
        {[0, 1, 2].map((q) => <path key={'sw' + q} d={`M ${790 + q * 60} 540 Q ${800 + q * 60} 700 ${780 + q * 70} 860`} stroke="#FFFFFF" strokeWidth={6} strokeDasharray="20 30" strokeDashoffset={-t * 300} fill="none" opacity={0.8 * spill} />)}
        {Array.from({length: 10}, (_, q) => <circle key={'fo' + q} cx={760 + rnd(q) * 220} cy={850 - ((t * 120 + q * 30) % 60)} r={12 + 6 * rnd(q + 2)} fill="#FFFFFF" stroke="#9FCCEA" strokeWidth={2} />)}</g>}
      {/* powerhouse with turbines */}
      <g transform="translate(1140 860)"><rect x={-110} y={-150} width={220} height={150} fill="#ECEFF1" stroke={OL} strokeWidth={6} />{[0, 1].map((q) => <g key={q} transform={`translate(${-50 + q * 100} -80) rotate(${t * 400 * flow})`}>
        <circle r={34} fill="#FFFFFF" stroke={OL} strokeWidth={4} />{[0, 1, 2].map((b) => <path key={b} d="M 0 0 L 28 -10 L 28 10 Z" fill={BLUE} transform={`rotate(${b * 120})`} />)}</g>)}
        {z.plaque && plaque(0, -180, z.plaque, '#FFFFFF', 22)}</g>
      {/* pylons */}
      {[0, 1, 2, 3].map((q) => { const x = 1330 + q * 230, y = 760 - q * 30; return <g key={'py' + q} transform={`translate(${x} ${y})`}>
        <path d="M -40 100 L 0 -180 L 40 100 M -26 0 L 26 0 M -54 -120 L 54 -120 M -40 -150 L 40 -150" stroke={OL} strokeWidth={6} fill="none" /></g>; })}
      {[0, 1].map((w) => <path key={'wr' + w} d={`M 1180 ${700 - w * 30} Q 1250 ${660 - w * 30} 1290 ${640 - w * 30} Q 1440 ${670 - w * 30} 1520 ${610 - w * 30} Q 1680 ${640 - w * 30} 1750 ${580 - w * 30} Q 1900 ${610 - w * 30} 1980 ${550 - w * 30}`} stroke={OL} strokeWidth={4} fill="none" />)}
      {flow > 0.05 && Array.from({length: 6}, (_, q) => { const u = ((t * 0.5 * flow + q / 6) % 1), x = lerp(1180, 1980, u), y = lerp(700, 550, u) - 40 * Math.sin(u * 12);
        return <circle key={'pp' + q} cx={x} cy={y} r={12} fill={GOLD} stroke={OL} strokeWidth={3} />; })}
      {ground(z, f, '#7FB86A', '#5E9A50')}
      <path d={`M 660 ${f} Q 900 ${f + 60} 1200 ${f + 40} L 1400 ${f + 120} L 500 ${f + 120} Z`} fill={WATER} stroke={OL} strokeWidth={4} />
      {price && <g transform={`translate(400 330) rotate(${-8 + 6 * Math.sin((t - prAt) * 5) * Math.exp(-(t - prAt))}) scale(${pop(t, prAt, 0.5)})`}><path d="M -10 -70 L 220 -70 L 270 0 L 220 70 L -10 70 Z" fill={GOLD} stroke={OL} strokeWidth={6} /><circle cx={20} cy={0} r={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        <T x={130} y={14} s={fit(price, 220, 40)} c={NAVY}>{price}</T></g>}
      {z.gate !== undefined && t >= z.gate && <g transform={`translate(${z.gateX ?? 560} ${f})`}><rect x={-26} y={-150} width={52} height={150} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
        <g transform={`translate(0 -120) rotate(${-80 + 80 * E.outBack(win(t, z.gate, 0.6))})`}><rect x={0} y={-14} width={460} height={28} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={5} />{[0, 1, 2, 3, 4].map((q) => <rect key={q} x={20 + q * 90} y={-14} width={44} height={28} fill={RED} />)}</g>
        {plaque(230, -210, z.gateText || 'PERMISSION NEEDED', '#FFFFFF', 26)}</g>}
      {stamp(960, 300, st, t, stAt)}
    </g>;
  },

  /** B.C.'s power talent show */
  castage: (t, z, f) => {
    const left = kf(z.left, t, 1), n = kf(z.n, t, 6), lit = Number(pick(z.lit, t, -1)), litAt = lastAt(z.lit, t);
    return <g>
      {sky(z, f, '#7EC8F2', '#DDF2FF', 'cast' + (z.ox ?? 0))}
      {peaks(z, 620, 380, '#7F95B5', 11, true)}
      {Array.from({length: 10}, (_, q) => pine(z.x0 + 40 + q * 260, 640, 0.7, 'sp' + q, true))}
      <rect x={180} y={360} width={1560} height={330} fill="#5A2A4A" stroke={OL} strokeWidth={6} />
      <path d="M 180 360 Q 300 520 220 690 L 180 690 Z M 1740 360 Q 1620 520 1700 690 L 1740 690 Z" fill="#B23A48" stroke={OL} strokeWidth={5} />
      <rect x={160} y={300} width={1600} height={70} rx={10} fill={GOLD} stroke={OL} strokeWidth={6} /><T x={960} y={350} s={fit(z.title || "B.C.'S POWER TALENT SHOW", 1500, 44)} c={NAVY}>{z.title || "B.C.'S POWER TALENT SHOW"}</T>
      {[0, 1, 2].map((q) => { const a = Math.sin(t * 0.9 + q * 2) * 0.35; return <path key={'sl' + q} d={`M ${500 + q * 460} 380 L ${500 + q * 460 + 700 * Math.sin(a) - 120} 700 L ${500 + q * 460 + 700 * Math.sin(a) + 120} 700 Z`} fill="#FFF6C8" opacity={0.25} />; })}
      <rect x={160} y={690} width={1600} height={60} fill="#8D6E63" stroke={OL} strokeWidth={6} />
      {Array.from({length: 8}, (_, q) => { const u = clamp(n - q); if (u <= 0) return null; const x = 360 + q * 170, on = lit === q, hy = on ? Math.abs(Math.sin((t - litAt) * 6)) * 30 * Math.exp(-(t - litAt) * 0.6) : Math.sin(t * 2 + q) * 4;
        return <g key={'cb' + q} transform={`translate(${x} ${690 - hy}) scale(${E.outBack(u) * 0.8})`}>{on && <ellipse cx={0} cy={6} rx={110} ry={26} fill="#FFF6C8" opacity={0.9} />}
          <rect x={-60} y={-130} width={120} height={130} rx={12} fill={on ? '#E1F5FE' : '#DDE3EC'} stroke={OL} strokeWidth={5} />{[0, 1, 2].map((r) => <rect key={r} x={-44} y={-112 + r * 36} width={88} height={22} rx={4} fill="#263238" />)}
          <circle cx={-26} cy={-101} r={5} fill={CY} /><circle cx={26} cy={-101} r={5} fill={CY} /><T x={0} y={-150} s={24} c={NAVY}>{'#' + (q + 1)}</T></g>; })}
      <g transform="translate(1600 190)"><rect x={-150} y={-60} width={300} height={120} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={-22} s={22}>POWER LEFT</T>
        <rect x={-120} y={-4} width={240} height={40} rx={10} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><rect x={-116} y={0} width={232 * left} height={32} rx={8} fill={left > 0.4 ? GREEN : left > 0.2 ? GOLD : RED} /></g>
      {ground(z, f, '#7FB86A', '#5E9A50')}
    </g>;
  },

  /** the snowy north: cold air in, heat out to a campus */
  cacold: (t, z, f) => {
    const air = kf(z.air, t, 1), pipe = kf(z.pipe, t, 0), build = kf(z.build, t, 0);
    return <g>
      {sky(z, f, '#8FD3FF', '#EAF7FF', 'cacd' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 260 + k * 700 + ((t * 8) % 400), 120 + 40 * (k % 2), 0.9, k))}
      {peaks(z, 640, 260, '#A9BCD6', 17, true)}
      <rect x={z.x0} y={640} width={z.x1 - z.x0} height={f - 640} fill={SNOW} stroke={OL} strokeWidth={4} />
      {Array.from({length: 9}, (_, q) => pine(z.x0 + 20 + q * 300 + 60 * rnd(q), 700 + 30 * rnd(q + 4), 0.75, 'cp' + q, true))}
      {hall(760, f, 1.15, 'c1', t)}
      {/* intake louvers + cold arrows */}
      <g transform="translate(470 760)"><rect x={-30} y={-110} width={60} height={160} fill="#B0BEC5" stroke={OL} strokeWidth={4} />{[0, 1, 2, 3, 4].map((q) => <path key={q} d={`M -26 ${-96 + q * 30} l 52 10`} stroke={OL} strokeWidth={4} />)}</g>
      {air > 0.02 && Array.from({length: 5}, (_, q) => { const u = ((t * 0.6 + q / 5) % 1); return <g key={'ca' + q} opacity={air * Math.sin(u * Math.PI)} transform={`translate(${lerp(80, 440, u)} ${680 + q * 26})`}>
        <path d="M -60 0 L 30 0 M 10 -18 L 34 0 L 10 18" stroke={CY} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /></g>; })}
      {Array.from({length: 4}, (_, q) => { const u = ((t * 0.5 + q / 4) % 1); return <path key={'ha' + q} d={`M ${900 + q * 60} ${f - 260 - u * 220} q 20 -20 0 -40 q -20 -20 0 -40`} stroke={RED} strokeWidth={8} fill="none" opacity={(1 - u) * 0.8} />; })}
      {/* heat pipe to campus */}
      {pipe > 0.01 && <g><path d={`M 1010 ${f - 60} L ${lerp(1010, 1500, pipe)} ${f - 60}`} stroke={OL} strokeWidth={30} strokeLinecap="round" /><path d={`M 1010 ${f - 60} L ${lerp(1010, 1500, pipe)} ${f - 60}`} stroke={ORANGE} strokeWidth={20} strokeLinecap="round" />
        <path d={`M 1010 ${f - 60} L ${lerp(1010, 1500, pipe)} ${f - 60}`} stroke="#FFE0B2" strokeWidth={6} strokeDasharray="20 30" strokeDashoffset={-t * 120} /></g>}
      {(pipe > 0 || z.campus) && <g transform={`translate(1700 ${f})`}><rect x={-200} y={-300} width={400} height={300} fill="#F2E6CF" stroke={OL} strokeWidth={6} /><path d="M -220 -300 L 0 -380 L 220 -300 Z" fill={BRICK} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        {[0, 1, 2].map((r) => [0, 1, 2, 3].map((q) => <rect key={r + '-' + q} x={-160 + q * 85} y={-270 + r * 80} width={56} height={50} fill={pipe > 0.95 ? '#FFD180' : '#BFE6F7'} stroke={OL} strokeWidth={4} />))}
        {plaque(0, -410, z.campus || 'CAMPUS', '#FFFFFF', 22)}<path d="M -210 -300 Q 0 -316 210 -300" stroke={SNOW} strokeWidth={14} fill="none" /></g>}
      {/* crane + new hall */}
      {build > 0.01 && <g><path d={`M 1300 ${f} L 1300 300 L 1640 300 M 1300 340 L 1380 300`} stroke={GOLD} strokeWidth={14} fill="none" /><path d={`M 1560 300 L 1560 ${lerp(360, f - 240, build)}`} stroke={OL} strokeWidth={4} />
        <g transform={`translate(1560 ${f}) scale(${0.8} ${0.8 * build})`}>{hall(0, 0, 1, 'nb', t, build)}</g></g>}
      {z.lot !== undefined && t >= z.lot && <g transform={`translate(1500 ${f}) scale(${pop(t, z.lot, 0.5)})`}><path d="M 0 0 L 0 -170" stroke={OL} strokeWidth={10} /><rect x={-130} y={-260} width={260} height={110} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={-216} s={30} c={GREEN}>LOT</T><T x={0} y={-176} s={26} c={NAVY}>AVAILABLE</T></g>}
      {snowfall(z, t, 50, 3)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#E3ECF5" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill="#C9D8E8" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the Sudbury-style mine */
  camine: (t, z, f) => {
    const gems = kf(z.gems, t, 0), years = kf(z.years, t, -1), st: string = pick(z.stamp, t, ''), stAt = lastAt(z.stamp, t);
    const G = [['CU', 'COPPER', '#D9773B'], ['NI', 'NICKEL', '#9CB0A8'], ['LI', 'LITHIUM', '#C9B8F0'], ['C', 'GRAPHITE', '#4A4F5C'], ['U', 'URANIUM', '#B7E05A']];
    return <g>
      {sky(z, f, '#7EC8F2', '#E3F4FF', 'camn' + (z.ox ?? 0))}
      {[0, 1].map((k) => cloud(z.x0 + 400 + k * 900 + ((t * 9) % 400), 130, 0.9, k))}
      {/* shield rock and lakes */}
      <path d={`M ${z.x0} 640 Q 300 520 520 600 Q 700 500 900 590 Q 1150 500 1400 600 Q 1650 520 ${z.x1} 620 L ${z.x1} 700 L ${z.x0} 700 Z`} fill="#A7A39A" stroke={OL} strokeWidth={5} />
      <ellipse cx={360} cy={690} rx={260} ry={34} fill={WATER} stroke={OL} strokeWidth={4} />
      {Array.from({length: 7}, (_, q) => pine(z.x0 + 80 + q * 330 + 50 * rnd(q), 640 + 20 * rnd(q + 1), 0.6, 'mp' + q))}
      <rect x={z.x0} y={680} width={z.x1 - z.x0} height={f - 680} fill="#C2B59B" stroke={OL} strokeWidth={4} />
      {/* headframe */}
      <g transform="translate(1180 860)"><path d="M -110 0 L -50 -460 L 50 -460 L 110 0 M -90 -150 L 90 -150 M -70 -300 L 70 -300 M -90 -150 L 70 -300 M 90 -150 L -70 -300" stroke="#C0392B" strokeWidth={14} fill="none" strokeLinejoin="round" />
        {[0, 1].map((q) => <g key={q} transform={`translate(${-28 + q * 56} -470) rotate(${t * (q ? -120 : 120)})`}><circle r={40} fill="none" stroke={OL} strokeWidth={8} />{[0, 1, 2, 3].map((b) => <path key={b} d="M 0 -40 L 0 40" stroke={OL} strokeWidth={5} transform={`rotate(${b * 45})`} />)}</g>)}
        <path d={`M -28 -430 L -28 ${-200 + 120 * Math.sin(t * 0.8)}`} stroke={OL} strokeWidth={3} /><rect x={-50} y={-120} width={100} height={120} fill="#ECEFF1" stroke={OL} strokeWidth={5} /></g>
      {/* ore pile + carts */}
      <path d="M 1350 860 Q 1500 640 1700 860 Z" fill="#7D7466" stroke={OL} strokeWidth={5} />
      {[0, 1].map((q) => { const x = 1300 + ((t * 90 + q * 350) % 700); return <g key={'ct' + q} transform={`translate(${x} ${f - 20})`}><path d="M -60 -60 L 60 -60 L 46 0 L -46 0 Z" fill="#78909C" stroke={OL} strokeWidth={5} /><path d="M -50 -60 Q 0 -100 50 -60" fill="#6D6457" stroke={OL} strokeWidth={4} />
        <circle cx={-30} cy={6} r={14} fill={OL} /><circle cx={30} cy={6} r={14} fill={OL} /></g>; })}
      {/* mineral gems */}
      {G.map(([sym, name, c], k) => { const u = clamp(gems - k); if (u <= 0) return null; const x = 260 + k * 170, y = 360 + 14 * Math.sin(t * 2 + k);
        return <g key={'gm' + k} transform={`translate(${x} ${y}) scale(${E.outBack(u)})`}><path d="M 0 -70 L 60 -20 L 36 60 L -36 60 L -60 -20 Z" fill={c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
          <path d="M -60 -20 L 60 -20 M 0 -70 L -20 -20 L 0 60 L 20 -20 Z" stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.6} /><T x={0} y={18} s={36} c="#FFFFFF" st={OL} sw={6}>{sym}</T>
          <T x={0} y={100} s={22} c={NAVY}>{name}</T></g>; })}
      {/* calendar */}
      {years >= 0 && <g transform="translate(1660 330)"><rect x={-130} y={-120} width={260} height={250} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><rect x={-130} y={-120} width={260} height={64} rx={14} fill={RED} stroke={OL} strokeWidth={6} />
        <T x={0} y={-74} s={30} c="#FFFFFF">YEAR</T><T x={0} y={74} s={110} c={NAVY}>{String(Math.max(1, Math.floor(years)))}</T>
        {years % 1 > 0.05 && years < 16 && <path d={`M -130 -56 L 130 -56 L 130 ${-56 + 180 * (1 - (years % 1))} Z`} fill="#F1F4F8" stroke={OL} strokeWidth={3} />}</g>}
      {ground(z, f, '#B5A88C', '#9A8D72')}
      {stamp(960, 260, st, t, stAt)}
    </g>;
  },

  /** the Montreal AI lab */
  calab: (t, z, f) => {
    const net = kf(z.net, t, 0.5), sup = kf(z.super, t, 0), scr: string = pick(z.screen, t, '');
    const L = [[0, 3], [1, 4], [2, 4], [3, 2]];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EEF3F8" />
      {/* window */}
      <g transform="translate(120 130)"><rect x={0} y={0} width={520} height={400} rx={12} fill="#BFE6F7" stroke={OL} strokeWidth={7} />
        {[0, 1, 2].map((q) => <g key={q}><rect x={20 + q * 170} y={170 - 40 * rnd(q)} width={150} height={240} fill={['#C98A5B', BRICK, '#9C6B4E'][q]} stroke={OL} strokeWidth={4} /><rect x={14 + q * 170} y={160 - 40 * rnd(q)} width={162} height={14} fill={SNOW} stroke={OL} strokeWidth={3} /></g>)}
        {Array.from({length: 20}, (_, q) => <circle key={q} cx={20 + rnd(q) * 480} cy={((t * 50 + rnd(q + 4) * 400) % 400)} r={4} fill="#FFFFFF" />)}
        <path d="M 260 0 L 260 400" stroke={OL} strokeWidth={7} /></g>
      {/* whiteboard neural net */}
      <g transform="translate(720 120)"><rect x={0} y={0} width={760} height={440} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
        {L.map(([li, n], a) => Array.from({length: n}, (_, b) => { const x = 110 + li * 180, y = 220 + (b - (n - 1) / 2) * 90;
          const nx = a < 3 ? L[a + 1] : null;
          return <g key={a + '-' + b}>{nx && Array.from({length: nx[1]}, (_, c) => { const x2 = 110 + nx[0] * 180, y2 = 220 + (c - (nx[1] - 1) / 2) * 90, on = net * 4 > a + 0.5;
            return <path key={c} d={`M ${x} ${y} L ${x2} ${y2}`} stroke={on ? BLUE : '#CFD8E3'} strokeWidth={on ? 4 : 2.5} />; })}
            <circle cx={x} cy={y} r={24} fill={net * 4 > a ? [GOLD, CY, PURPLE, GREEN][a] : '#FFFFFF'} stroke={OL} strokeWidth={4} /></g>; }))}
        <T x={380} y={420} s={24} c="#5E6B85">DEEP LEARNING</T></g>
      {/* racks */}
      {[0, 1].map((q) => <g key={'rk' + q} transform={`translate(${1600 + q * 170} ${f})`}><rect x={-70} y={-460} width={140} height={460} rx={8} fill="#37474F" stroke={OL} strokeWidth={6} />
        {Array.from({length: 9}, (_, r) => <g key={r}><rect x={-56} y={-440 + r * 48} width={112} height={36} rx={4} fill="#263238" /><circle cx={-40} cy={-422 + r * 48} r={5} fill={(Math.floor(t * 4 + r + q) % 3) ? CY : GREEN} /></g>)}</g>)}
      {/* monitor */}
      {scr && <g transform="translate(560 660)"><rect x={-220} y={-130} width={440} height={240} rx={14} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={8} s={fit(scr, 400, 40)} c={GOLD}>{scr}</T><path d="M -30 110 L -50 170 L 50 170 L 30 110" fill="#90A4AE" stroke={OL} strokeWidth={4} /></g>}
      {/* supercomputer tower assembling */}
      {sup > 0.01 && <g transform={`translate(1180 ${f})`}>{Array.from({length: 6}, (_, r) => { const u = clamp(sup * 6 - r); if (u <= 0) return null;
        return <g key={r} transform={`translate(0 ${-r * 80 - 80 - (1 - E.outBack(u)) * 300})`} opacity={clamp(u * 3)}><rect x={-160} y={0} width={320} height={74} rx={10} fill={r % 2 ? '#455A64' : '#37474F'} stroke={OL} strokeWidth={5} />
          {[0, 1, 2, 3, 4, 5].map((q) => <circle key={q} cx={-120 + q * 48} cy={37} r={7} fill={(Math.floor(t * 5 + q + r) % 2) ? CY : GOLD} />)}</g>; })}
        {sup > 0.98 && plaque(0, -580, z.superText || 'OWNED IN CANADA', GOLD, 26)}</g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#B0BEC5" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#90A4AE" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the river crossing: trucks, tariff barrier, data cable */
  caborder: (t, z, f) => {
    const share = Number(z.share ?? 0.75), tar = z.tariff, cable = kf(z.cable, t, 0);
    const jam = tar !== undefined && t >= tar ? E.inOut(win(t, tar, 1.2)) : 0;
    return <g>
      {sky(z, f, '#7EC8F2', '#DDF2FF', 'cabr' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 300 + k * 650 + ((t * 10) % 400), 120, 0.9, k))}
      {/* river */}
      <rect x={z.x0} y={700} width={z.x1 - z.x0} height={500} fill={WATER} />
      {Array.from({length: 12}, (_, q) => <path key={'rv' + q} d={`M ${z.x0 + (q % 6) * 400 + ((t * 40) % 400)} ${760 + Math.floor(q / 6) * 120} q 30 -14 60 0 t 60 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.7} />)}
      {/* banks */}
      <path d={`M ${z.x0} 620 L 640 620 L 700 1100 L ${z.x0} 1100 Z`} fill="#A6D08A" stroke={OL} strokeWidth={5} />
      <path d={`M 1280 620 L ${z.x1} 620 L ${z.x1} 1100 L 1220 1100 Z`} fill="#C8DDA6" stroke={OL} strokeWidth={5} />
      <T x={330} y={1000} s={30} c={NAVY}>CANADA</T><T x={1600} y={1000} s={30} c={NAVY}>UNITED STATES</T>
      {hall(300, 620, 0.6, 'b1', t)}{pine(560, 620, 0.6, 'bp1', false)}
      <g transform="translate(1620 620)"><rect x={-260} y={-280} width={520} height={280} fill="#F2E6CF" stroke={OL} strokeWidth={6} /><rect x={-280} y={-310} width={560} height={40} rx={8} fill={BLUE} stroke={OL} strokeWidth={5} />
        <T x={0} y={-282} s={26} c="#FFFFFF">BIG CUSTOMER NEXT DOOR</T>{[0, 1, 2, 3].map((q) => <rect key={q} x={-220 + q * 115} y={-220} width={80} height={120} fill="#BFE6F7" stroke={OL} strokeWidth={4} />)}<rect x={-60} y={-90} width={120} height={90} fill="#7A4B2A" stroke={OL} strokeWidth={5} /></g>
      {/* bridge */}
      <rect x={620} y={590} width={680} height={36} fill="#9AA6B8" stroke={OL} strokeWidth={5} />{[0, 1, 2, 3].map((q) => <path key={'br' + q} d={`M ${660 + q * 200} 626 L ${660 + q * 200} 900`} stroke={OL} strokeWidth={14} />)}
      <path d="M 620 590 Q 960 420 1300 590" stroke={OL} strokeWidth={8} fill="none" />
      {/* trucks */}
      {Array.from({length: 8}, (_, q) => { const goes = (q % 4) < Math.round(share * 4); const base = ((t * 0.12 + q / 8) % 1);
        if (!goes) { const u = base; return <g key={'sh' + q} transform={`translate(${lerp(560, 380, u)} ${lerp(720, 1080, u)}) scale(0.6)`} opacity={Math.sin(u * Math.PI)}><path d="M -70 0 L 70 0 L 50 30 L -50 30 Z" fill={RED} stroke={OL} strokeWidth={5} /><rect x={-30} y={-40} width={50} height={40} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>; }
        let x = lerp(260, 1600, base); if (jam > 0 && x > 900) x = lerp(x, 900 - (q % 4) * 130, jam);
        return <g key={'tk' + q} transform={`translate(${x} ${x > 620 && x < 1300 ? 590 : 620})`}><rect x={-80} y={-70} width={110} height={64} rx={6} fill={['#FFC93C', '#7BD389', '#4FB3F6', '#FF8A65'][q % 4]} stroke={OL} strokeWidth={4} />
          <rect x={30} y={-56} width={46} height={50} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><circle cx={-50} cy={0} r={12} fill={OL} /><circle cx={50} cy={0} r={12} fill={OL} /></g>; })}
      {tar !== undefined && t >= tar && <g transform="translate(960 590)"><rect x={-20} y={-160} width={40} height={160} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
        <g transform={`translate(0 -130) rotate(${-80 + 80 * E.outBack(win(t, tar, 0.5))})`}><rect x={-180} y={-14} width={360} height={28} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={5} />{[0, 1, 2, 3].map((q) => <rect key={q} x={-160 + q * 90} y={-14} width={44} height={28} fill={RED} />)}</g>
        {plaque(0, -220, 'TARIFF', RED, 34, '#FFFFFF')}</g>}
      {/* data cable */}
      {cable > 0.01 && <g><path d={`M 300 640 Q 500 1000 960 1010 Q 1420 1000 ${lerp(960, 1620, clamp(cable))} 640`} stroke={OL} strokeWidth={22} fill="none" /><path d={`M 300 640 Q 500 1000 960 1010 Q 1420 1000 ${lerp(960, 1620, clamp(cable))} 640`} stroke={PURPLE} strokeWidth={12} fill="none" />
        {Array.from({length: 6}, (_, q) => { const u = (t * 0.25 + q / 6) % 1; const x = u < 0.5 ? lerp(300, 960, u * 2) : lerp(960, 1620, (u - 0.5) * 2), y = u < 0.5 ? lerp(640, 1010, Math.sin(u * Math.PI)) : lerp(1010, 640, (u - 0.5) * 2);
          return <rect key={q} x={x - 14} y={y - 14} width={28} height={28} rx={6} fill={CY} stroke={OL} strokeWidth={3} opacity={cable} />; })}
        {plaque(960, 1060, 'COMPUTING TRAVELS BY CABLE', '#FFFFFF', 24)}</g>}
    </g>;
  },

  /** the AI shopping receipt (scorecard) */
  careceipt: (t, z, f) => {
    const pr = kf(z.print, t, 1), rows: any[] = z.rows || [];
    const H = 140 + rows.length * 130;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#FFF4E0" />
      {Array.from({length: 30}, (_, k) => <circle key={'dt' + k} cx={z.x0 + (k % 10) * 260 + 60} cy={120 + Math.floor(k / 10) * 380} r={8} fill="#F4DDB5" />)}
      <g transform="translate(960 920)"><rect x={-360} y={-60} width={720} height={160} rx={20} fill="#5E6B85" stroke={OL} strokeWidth={7} /><rect x={-300} y={-30} width={600} height={24} rx={8} fill="#263238" />
        <T x={0} y={70} s={30} c="#FFFFFF">AI'S CHECKOUT</T></g>
      <clipPath id={'carc' + (z.ox ?? 0)}><rect x={560} y={890 - H * pr} width={800} height={H * pr + 10} /></clipPath>
      <g clipPath={`url(#carc${z.ox ?? 0})`}><g transform={`translate(960 ${890 - H * pr})`}>
        <path d={`M -300 0 ${Array.from({length: 13}, (_, q) => `L ${-300 + (q + 0.5) * 46} ${q % 2 ? 12 : -12}`).join(' ')} L 300 0 L 300 ${H} L -300 ${H} Z`} fill={PAPER} stroke={OL} strokeWidth={5} />
        <T x={0} y={80} s={36} c={NAVY}>{z.title || 'THE SCORECARD'}</T>
        {rows.map((r, k) => { const u = clamp((t - (r.at ?? 0)) / 0.4); return <g key={'rw' + k} transform={`translate(0 ${160 + k * 130})`} opacity={u}>
          <T x={-260} y={10} s={40} a="start" c={NAVY}>{r.label}</T><T x={-260} y={56} s={fit(r.note || '', 440, 26)} a="start" w={700} c="#5E6B85">{r.note || ''}</T>
          {r.mark === 'yes' ? <path d="M 200 0 l 20 24 l 44 -54" stroke={GREEN} strokeWidth={12} fill="none" strokeLinecap="round" strokeLinejoin="round" transform={`scale(${E.outBack(u)})`} />
            : <g transform={`translate(230 0) scale(${E.outBack(u)})`}><circle r={30} fill={GOLD} stroke={OL} strokeWidth={4} /><T x={0} y={14} s={40} c={NAVY}>!</T></g>}</g>; })}
      </g></g>
    </g>;
  },

  /** title card */
  catitle: (t, z, f) => <g>
    {sky(z, f, '#7CC8F5', '#E6F6FF', 'catt')}
    {peaks(z, 760, 360, '#A9BCD6', 23, true)}
    <path d={`M ${z.x0} 860 Q 600 640 1300 800 Q 1700 880 ${z.x1} 760 L ${z.x1} 1200 L ${z.x0} 1200 Z`} fill={SNOW} stroke={OL} strokeWidth={5} />
    {Array.from({length: 6}, (_, q) => pine(200 + q * 320, 840 - 60 * Math.sin(q), 0.7, 'tp' + q, true))}
    {snowfall(z, t, 50, 9)}
    <g opacity={clamp((t - 0.3) / 0.4)} transform={`translate(960 330) scale(${E.outBack(win(t, 0.3, 0.6))})`}>
      <rect x={-760} y={-130} width={1520} height={250} rx={28} fill={NAVY} stroke={OL} strokeWidth={8} />
      <T x={0} y={-30} s={58} c="#FFFFFF">WHY CANADA COULD BE</T><T x={0} y={60} s={62} c={GOLD}>THE BIGGEST WINNER OF THE AI BOOM</T></g>
  </g>,

  /** chapter bumper */
  cabumper: (t, z, f) => {
    const roll = E.inOut(win(t, 0, 1.0));
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill={z.color || BLUE} />
      {Array.from({length: 40}, (_, k) => <circle key={'bf' + k} cx={(rnd(k) * 2200 + t * 30 * (1 + rnd(k + 1))) % 2100 - 90} cy={(rnd(k + 5) * 1200 + t * 60) % 1200} r={5 + 6 * rnd(k + 3)} fill="#FFFFFF" opacity={0.5} />)}
      {roll < 1 && <g transform={`translate(${lerp(-200, 960, roll)} 460) rotate(${roll * 720})`}><circle r={60 + roll * 120} fill={SNOW} stroke={OL} strokeWidth={6} /><path d="M -30 -20 Q 0 -40 30 -10" stroke="#BFD3E6" strokeWidth={6} fill="none" /></g>}
      <g opacity={clamp((t - 0.9) / 0.3)}><T x={960} y={250} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={340} width={1200} height={140} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={960} y={432} s={fit(z.title || '', 1140, 62)} c={GOLD}>{z.title || ''}</T>
        {t >= 1.3 && <T x={960} y={570} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.3) / 0.3)}>{z.caption || ''}</T>}</g>
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const CANADA_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

const hopY = (a: Item, t: number) => { let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.6) hy = Math.sin((u / 0.6) * Math.PI) * 90; } return hy; };

/** whirr: the walking data center */
const whirr: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, walking = Math.abs(vx) > 20;
  const step = walking ? Math.sin(t * 12) : 0, bob = walking ? Math.abs(step) * 8 : Math.sin(t * 2.2 + i) * 3;
  const face: string = pick(a.faces, t, a.face || 'happy'), hot = face === 'hot';
  const shake = hot ? Math.sin(t * 40) * 3 : 0;
  const y = kf(a.y, t, f) - hopY(a, t) - bob, s = (a.scale ?? 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const fl = vx < -20 ? -1 : 1, fan = kf(a.fan, t, hot ? 3 : 1), blink = (Math.floor(t * 0.6 + i) % 5 === 0 && (t % 1.7) < 0.12);
  const sq = 1 + (walking ? 0.03 * Math.abs(step) : 0), wv = a.wave !== undefined && t >= a.wave && t < a.wave + 2.2 ? Math.sin((t - a.wave) * 10) * 30 : 0;
  const sweat = Array.isArray(a.sweat) && t >= a.sweat[0] && t < a.sweat[1], scarf = a.scarf !== undefined && t >= a.scarf ? E.outBack(win(t, a.scarf, 0.4)) : 0;
  const eye = (cx: number) => face === 'wow' ? <circle key={cx} cx={cx} cy={-286} r={15} fill={CY} /> : face === 'calm' ? <path key={cx} d={`M ${cx - 14} -284 Q ${cx} -296 ${cx + 14} -284`} stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" />
    : <rect key={cx} x={cx - 12} y={face === 'worry' || hot ? -292 : -298} width={24} height={blink ? 3 : face === 'worry' || hot ? 14 : 24} rx={6} fill={hot ? '#FF8A80' : CY} />;
  const mouth = face === 'worry' || hot ? 'M -24 -246 Q 0 -260 24 -246' : face === 'wow' ? 'M -12 -252 a 12 12 0 1 0 24 0 a 12 12 0 1 0 -24 0' : 'M -26 -256 Q 0 -236 26 -256';
  return <g key={'wh' + i} transform={`translate(${x + shake} ${y}) scale(${s * fl} ${s / sq})`}>
    <ellipse cx={0} cy={0} rx={90} ry={14} fill="#000000" opacity={0.12} />
    <path d={`M -34 -40 L ${-38 + step * 16} 0 M 34 -40 L ${38 - step * 16} 0`} stroke={OL} strokeWidth={12} strokeLinecap="round" />
    <ellipse cx={-38 + step * 16} cy={0} rx={22} ry={10} fill={OL} /><ellipse cx={38 - step * 16} cy={0} rx={22} ry={10} fill={OL} />
    {/* arms */}
    <path d={`M -86 -170 Q -130 -120 -120 ${-80 + Math.sin(t * 2.4 + i) * 6}`} stroke={OL} strokeWidth={10} fill="none" strokeLinecap="round" />
    <path d={`M 86 -170 Q ${130 + wv * 0.3} ${-220 + (wv ? -40 : 80)} ${120 + wv} ${wv ? -300 : -80 - Math.sin(t * 2.4 + i) * 6}`} stroke={OL} strokeWidth={10} fill="none" strokeLinecap="round" />
    {a.carry === 'suitcase' && <g transform="translate(-126 -60)"><rect x={-44} y={-10} width={88} height={64} rx={8} fill={BRICK} stroke={OL} strokeWidth={5} /><path d="M -16 -10 L -16 -24 L 16 -24 L 16 -10" stroke={OL} strokeWidth={5} fill="none" /></g>}
    {/* cabinet */}
    <rect x={-90} y={-340} width={180} height={300} rx={22} fill="#DDE3EC" stroke={OL} strokeWidth={6} />
    <rect x={-72} y={-320} width={144} height={92} rx={14} fill="#263238" />
    {eye(-30)}{eye(30)}<path d={mouth} stroke={hot ? '#FF8A80' : CY} strokeWidth={5} fill={face === 'wow' ? CY : 'none'} strokeLinecap="round" />
    {[0, 1, 2].map((r) => <g key={r}><rect x={-72} y={-214 + r * 30} width={144} height={20} rx={4} fill="#37474F" /><circle cx={56} cy={-204 + r * 30} r={4} fill={(Math.floor(t * 4 + r) % 2) ? GREEN : CY} /></g>)}
    <g transform="translate(0 -92)"><circle r={34} fill="#B0BEC5" stroke={OL} strokeWidth={5} /><g transform={`rotate(${t * 360 * fan})`}>{[0, 1, 2, 3].map((b) => <path key={b} d="M 0 0 Q 18 -10 26 -4 L 4 4 Z" fill={OL} transform={`rotate(${b * 90})`} />)}</g><circle r={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /></g>
    {hot && [0, 1, 2].map((q) => <path key={'hw' + q} d={`M ${-50 + q * 50} -360 q 12 -16 0 -32 q -12 -16 0 -32`} stroke={RED} strokeWidth={5} fill="none" opacity={0.4 + 0.4 * Math.sin(t * 8 + q)} />)}
    {sweat && [0, 1].map((q) => { const u = ((t * 1.4 + q * 0.5) % 1); return <path key={'sw' + q} d={`M ${q ? 96 : -96} ${-300 + u * 90} q 10 16 0 24 q -10 -8 0 -24 Z`} fill={WATER} stroke={OL} strokeWidth={2.5} opacity={1 - u} />; })}
    {a.frost !== undefined && t >= a.frost && [0, 1].map((q) => { const u = ((t - a.frost) * 0.7 + q * 0.5) % 1; return <circle key={'fr' + q} cx={40 + u * 90} cy={-250 - u * 30} r={10 + u * 26} fill="#FFFFFF" stroke="#BFD3E6" strokeWidth={2} opacity={(1 - u) * 0.85} />; })}
    {scarf > 0 && <g transform={`scale(${scarf})`}><rect x={-96} y={-236} width={192} height={28} rx={12} fill={RED} stroke={OL} strokeWidth={4} /><path d={`M 50 -214 L ${60 + Math.sin(t * 4) * 8} -150 L 90 -152 L 76 -214 Z`} fill={RED} stroke={OL} strokeWidth={4} />{[0, 1, 2, 3].map((q) => <path key={q} d={`M ${-80 + q * 50} -236 l 0 28`} stroke="#FFFFFF" strokeWidth={5} />)}</g>}
    {a.label && t < (a.labelUntil ?? at + 3) && <g transform={`scale(${fl} 1)`}>{plaque(0, -400, a.label, '#FFFFFF', 20)}</g>}
  </g>;
};

export const CANADA_ITEMS: Record<string, ItemFn> = {whirr};
export const CANADA_INDOOR = ['caapt', 'calab', 'careceipt', 'cabumper'];
