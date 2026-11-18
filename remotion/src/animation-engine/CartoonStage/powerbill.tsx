import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * POWERBILL kit for CartoonStage (Episode 65, "Why AI Could Make Your Electricity Bill Explode").
 *
 * A sunny American suburb that shares its wires with an AI data-center campus, drawn in the channel's prime-time cartoon GENRE
 * (thick clean outlines, flat colour, squash and stretch). Everything ORIGINAL: no logos, no brand names on buildings, no traced
 * plants or products; companies appear only as generic buildings with a plain plaque when the narration names them. No real person
 * is drawn (regulators and executives are anonymous silhouettes).
 * Sets:
 *  - pbtown: a day street (hero house with a spinning meter, poles and wires) and, behind it, a data-center campus that rises with
 *    `dc` (KF 0..1: halls appear one by one, roof chillers spin). `zap` (KF 0..1) sends glowing pulses along the wires toward the
 *    campus; `cranes` shows tower cranes; `heat` waves above the halls; `campusText` plaque.
 *  - bigbill: a kitchen-table close-up of a giant paper bill. `total` text; `slices` [{label, v, color, at}] stack into a column on
 *    the bill; `push` [{label, at, dv}] grows a red hatched "pushed" cap on the slice with that label; `illus` banner text; `stamp`
 *    [[t, text]] a rubber stamp on the bill.
 *  - auction: an auction hall: podium and gavel (`gavel` [t...]), a split-flap price board (`prices` [[t, text]], `board` title),
 *    a cap rail (`capAt`, `capText`), a balance with SUPPLY crates (`supply` KF height 0..1) and DEMAND servers (`demand` KF), a
 *    shortfall bracket (`shortAt`, `shortText`), silhouette bidders.
 *  - gridbuild: towers march in with `build` (KF 0..1), a construction odometer (`cost` [[t, text]], `costTitle`), and on the
 *    right four customer buckets (HOMES, SHOPS, FACTORIES, DATA CENTERS) filling with coins per `split` [{who, v KF 0..1}]; `hi`
 *    pulses one bucket.
 *  - hearing: a regulators' hearing room: bench with three silhouettes, lectern; a contract scroll unrolls (`unroll` KF 0..1,
 *    `years` count, `yearsText`); a padlock (`lockAt`, `lockText`); `ghostAt` shows a ghost data center that never arrives with a
 *    dangling line; `strand` coins flow to the HOMES jar until `lockAt`, then to the DATA CENTER jar.
 *  - plantdeal: a riverside power plant with cooling towers (`steam` KF 0..1 restart), a cable to a data-center hall, a solar field
 *    and turbines appearing with `supply` (KF 0..1); `tags` [[t, text]] deal cards; `shakeAt` handshake silhouettes.
 *  - gaugeroom: a utility control room: a giant price gauge (`needle` KF value, `lo`/`hi` scale, `unit`, `marks` [{v, label, at}])
 *    and a dial bank `dials` [{label, at, v KF -1..1, l, r}] (verdict knobs).
 *  - pbtitle / pbbumper: the title card (a bill envelope bursts with a spark) and chapter bumpers (plug meets socket).
 * Items: pbtag (top-left pill: FACT / FORECAST / ESTIMATE / OUR CALC / ILLUSTRATIVE / MECHANISM, `tags` [[t, text]]), billpaper
 *  (a flying paper bill with `amount`, x/y KF), sparky (the plug mascot that hops and points, x KF, `hops`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#14213D';
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

const BLUE = '#1E88E5', GOLD = '#F5B700', RED = '#E5483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', PURPLE = '#7357C9', CY = '#29C5F6', NAVY = '#14213D', ORANGE = '#F08A24', GREY = '#8E9AAF';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'pcl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const ground = (z: Z, f: number, c = '#A9D18E', c2 = '#8DBB6F') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const banner = (x: number, y: number, txt: string, c = RED, s = 26) => { const w = Math.max(260, txt.length * s * 0.62 + 50);
  return <g transform={`translate(${x} ${y}) rotate(-2)`}><rect x={-w / 2} y={-s} width={w} height={s * 1.7} rx={8} fill={c} stroke={OL} strokeWidth={4} />
    <T x={0} y={s * 0.32} s={s} c="#FFFFFF">{txt}</T></g>; };
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const coin = (x: number, y: number, s = 1, k: any = 0) => <g key={'cn' + k} transform={`translate(${x} ${y}) scale(${s})`}><circle r={18} fill={GOLD} stroke={OL} strokeWidth={3.5} /><T x={0} y={7} s={20}>$</T></g>;
const bolt = (x: number, y: number, s: number, c = GOLD) => <path transform={`translate(${x} ${y}) scale(${s})`} d="M 10 -60 L -26 6 L -2 6 L -14 60 L 28 -10 L 4 -10 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />;
/** anonymous silhouette (never a likeness) */
const sil = (x: number, y: number, s: number, k: number, t: number, c = '#3B4A66') => <g key={'sil' + k} transform={`translate(${x} ${y + 2 * Math.sin(t * 2 + k)}) scale(${s})`}>
  <path d="M -42 0 Q -42 -70 0 -76 Q 42 -70 42 0 Z" fill={c} stroke={OL} strokeWidth={4} /><circle cx={0} cy={-104} r={28} fill={c} stroke={OL} strokeWidth={4} /></g>;

/** generic suburban house */
const house = (x: number, y: number, s: number, k: number, body: string, roof: string, t: number, meter = 0) => <g key={'hs' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-120} y={-170} width={240} height={170} fill={body} stroke={OL} strokeWidth={5} />
  <path d="M -140 -170 L 0 -270 L 140 -170 Z" fill={roof} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
  <rect x={-30} y={-90} width={60} height={90} rx={4} fill="#8D5A3B" stroke={OL} strokeWidth={4} /><circle cx={18} cy={-44} r={4} fill={GOLD} />
  {[-80, 80].map((wx) => <g key={wx}><rect x={wx - 30} y={-140} width={60} height={50} fill="#BFE6F7" stroke={OL} strokeWidth={4} /><path d={`M ${wx} -140 L ${wx} -90 M ${wx - 30} -115 L ${wx + 30} -115`} stroke={OL} strokeWidth={3} /></g>)}
  {meter > 0 && <g transform="translate(-100 -60)"><rect x={-22} y={-26} width={44} height={52} rx={8} fill="#E6ECF2" stroke={OL} strokeWidth={4} />
    <circle cx={0} cy={-4} r={14} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><path d={`M 0 -4 L ${Math.sin(t * 6 * meter) * 11} ${-4 - Math.cos(t * 6 * meter) * 11}`} stroke={RED} strokeWidth={3} strokeLinecap="round" /></g>}
</g>;

/** data-center hall: windowless box, roof chillers (fans spin), status lights */
const hall = (x: number, y: number, w: number, h: number, k: number, t: number, rise = 1) => {
  const hh = h * rise; if (rise <= 0.01) return null;
  return <g key={'dh' + k}>
    <rect x={x} y={y - hh} width={w} height={hh} fill="#DCE3EC" stroke={OL} strokeWidth={5} />
    <rect x={x} y={y - hh} width={w} height={18} fill="#B7C3D3" stroke={OL} strokeWidth={4} />
    {Array.from({length: Math.floor(w / 60)}, (_, q) => <rect key={q} x={x + 14 + q * 60} y={y - hh + 40} width={40} height={Math.max(4, hh - 70)} fill="#C7D1DE" stroke={OL} strokeWidth={2} />)}
    {rise > 0.9 && Array.from({length: Math.floor(w / 90)}, (_, q) => <g key={'ch' + q} transform={`translate(${x + 45 + q * 90} ${y - hh - 22})`}>
      <rect x={-34} y={-14} width={68} height={28} rx={6} fill="#9FB0C5" stroke={OL} strokeWidth={3} />
      <g transform={`rotate(${t * 400 + q * 30})`}><path d="M -11 0 L 11 0 M 0 -11 L 0 11" stroke={OL} strokeWidth={4} /></g></g>)}
    {rise > 0.9 && Array.from({length: 4}, (_, q) => <circle key={'lt' + q} cx={x + 20 + q * 22} cy={y - hh + 30} r={5} fill={(Math.floor(t * 3 + q + k) % 3) ? CY : GREEN} />)}
  </g>;
};

/** lattice transmission tower */
const tower = (x: number, y: number, s: number, k: number, o = 1) => <g key={'tw' + k} transform={`translate(${x} ${y}) scale(${s})`} opacity={o}>
  <path d="M -60 0 L -12 -300 L 12 -300 L 60 0 M -48 -60 L 48 -60 M -36 -130 L 36 -130 M -24 -200 L 24 -200 M -48 -60 L 36 -130 M 48 -60 L -36 -130 M -36 -130 L 24 -200 M 36 -130 L -24 -200"
    stroke="#5B6B82" strokeWidth={8} fill="none" strokeLinejoin="round" />
  <path d="M -90 -250 L 90 -250 M -70 -290 L 70 -290" stroke="#5B6B82" strokeWidth={10} strokeLinecap="round" />
  {[-90, 90, -70, 70].map((cx, q) => <circle key={q} cx={cx} cy={q < 2 ? -244 : -284} r={7} fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}
</g>;

/** wooden pole */
const pole = (x: number, y: number, k: number) => <g key={'pl' + k}><rect x={x - 8} y={y - 300} width={16} height={300} fill="#8D5A3B" stroke={OL} strokeWidth={4} />
  <rect x={x - 60} y={y - 290} width={120} height={12} fill="#8D5A3B" stroke={OL} strokeWidth={3} /></g>;

/** cooling tower */
const cooling = (x: number, y: number, s: number, k: number, t: number, steam: number) => <g key={'ct' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -120 0 Q -70 -150 -90 -300 L 90 -300 Q 70 -150 120 0 Z" fill="#E4E8EE" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
  <path d="M -95 -270 L 95 -270" stroke="#C3CAD5" strokeWidth={8} />
  {steam > 0 && [0, 1, 2, 3].map((p) => { const u = ((t * 0.3 + p / 4 + k * 0.13) % 1); return <circle key={p} cx={-20 + u * 80 + 20 * Math.sin(p)} cy={-320 - u * 260} r={(40 + u * 70) * (0.5 + 0.5 * steam)} fill="#FFFFFF" stroke="#D7DEE8" strokeWidth={3} opacity={steam * (1 - u) * 0.95} />; })}
</g>;

/** solar panel row */
const panels = (x: number, y: number, n: number, k: number) => <g key={'sp' + k}>{Array.from({length: n}, (_, q) => <g key={q} transform={`translate(${x + q * 100} ${y}) skewX(-18)`}>
  <rect x={0} y={-50} width={88} height={50} fill="#2A4F8F" stroke={OL} strokeWidth={3} /><path d="M 29 -50 L 29 0 M 58 -50 L 58 0 M 0 -25 L 88 -25" stroke="#8FB8F0" strokeWidth={2} /></g>)}</g>;
const turbine = (x: number, y: number, s: number, t: number, k: number) => <g key={'tb' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -6 0 L -3 -260 L 3 -260 L 6 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={3} />
  <g transform={`translate(0 -260) rotate(${t * 70 + k * 40})`}>{[0, 120, 240].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 L -8 -14 L 0 -120 L 8 -14 Z" fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}<circle r={8} fill={OL} /></g>
</g>;

/** electric pulses travelling along a quadratic wire a->b (sag) */
const pulses = (ax: number, ay: number, bx: number, by: number, sag: number, n: number, t: number, sp: number, on: number, c = GOLD, k = 0) => on <= 0 ? null :
  <g key={'pu' + k} opacity={on}>{Array.from({length: n}, (_, q) => { const u = ((t * sp + q / n) % 1);
    return <circle key={q} cx={lerp(ax, bx, u)} cy={lerp(ay, by, u) + Math.sin(u * Math.PI) * sag} r={9} fill={c} stroke={OL} strokeWidth={2.5} />; })}</g>;

export const POWERBILL_SETS: Record<string, SetFn> = {
  /** the street that shares its wires with an AI campus */
  pbtown: (t, z, f) => {
    const w = z.x1 - z.x0, dc = clamp(kf(z.dc, t, 1)), zap = clamp(kf(z.zap, t, 0)), heat = clamp(kf(z.heat, t, dc));
    const halls = [[1150, 300, 230], [1480, 280, 260], [1790, 340, 210], [2160, 300, 250], [2490, 260, 220]];
    return <g>
      {sky(z, f, '#7FC8F0', '#EAF7FF', 'pbsky' + Math.round(z.x0))}
      {[0, 1, 2, 3].map((k) => cloud(((k * 760 + t * 12) % (w + 600)) + z.x0 - 300, 100 + (k % 2) * 70, 0.8, k))}
      <path d={`M ${z.x0} ${f - 200} Q ${z.x0 + w * 0.3} ${f - 300} ${z.x0 + w * 0.55} ${f - 210} T ${z.x1} ${f - 230} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#C2E0B4" />
      {/* campus behind the street */}
      <g>{halls.map(([hx, hw, hh], k) => { const r = clamp(dc * halls.length - k); return <g key={'hl' + k}>{hall(hx, f - 120, hw, hh, k, t, E.out(r))}
        {heat > 0 && r > 0.95 && [0, 1, 2].map((q) => { const u = (t * 0.5 + q / 3 + k * 0.2) % 1; return <path key={q} d={`M ${hx + 40 + q * 80} ${f - 120 - hh - 40 - u * 120} q 12 -18 0 -36 q -12 -18 0 -36`} stroke="#FFB4A8" strokeWidth={5} fill="none" opacity={heat * (1 - u) * 0.8} />; })}</g>; })}
        {z.cranes && dc < 0.98 && [0, 1].map((k) => { const cx = 1700 + k * 650, sw = 20 * Math.sin(t * 0.8 + k);
          return <g key={'cr' + k}><path d={`M ${cx} ${f - 120} L ${cx} ${f - 640} M ${cx - 120} ${f - 620} L ${cx + 300} ${f - 620}`} stroke={GOLD} strokeWidth={12} />
            <path d={`M ${cx + 220 + sw} ${f - 620} L ${cx + 220 + sw} ${f - 480}`} stroke={OL} strokeWidth={4} /><rect x={cx + 196 + sw} y={f - 480} width={48} height={30} fill="#B7C3D3" stroke={OL} strokeWidth={3} /></g>; })}
        {/* substation + tower line feeding the campus */}
        <g transform={`translate(1000 ${f - 120})`}><rect x={-90} y={-70} width={180} height={70} fill="#C9D2DE" stroke={OL} strokeWidth={4} />
          {[-60, -20, 20, 60].map((q) => <path key={q} d={`M ${q} -70 L ${q} -130 M ${q - 14} -110 L ${q + 14} -110`} stroke={OL} strokeWidth={4} />)}</g>
        {tower(820, f - 120, 0.7, 1)}
        <path d={`M 760 ${f - 300} Q 900 ${f - 250} 1000 ${f - 210}`} stroke={OL} strokeWidth={3} fill="none" />
        {z.campusText && dc > 0.5 && plaque(1800, f - 520, z.campusText, NAVY, 26, '#FFFFFF')}
      </g>
      {/* street: poles, wires, houses */}
      <rect x={z.x0} y={f - 120} width={w} height={120} fill="#B9DDA6" />
      {[-180, 300, 780].map((px, k) => pole(px, f - 20, k))}
      <path d={`M -180 ${f - 300} Q 60 ${f - 260} 300 ${f - 300} Q 540 ${f - 260} 780 ${f - 300} Q 900 ${f - 270} 1000 ${f - 210}`} stroke={OL} strokeWidth={3.5} fill="none" />
      {pulses(1000, f - 210, -180, f - 300, 22, 8, t, 0.5, zap * 0.6, GOLD, 1)}
      {pulses(760, f - 300, 1000, f - 210, 10, 5, t, 0.9, zap, CY, 2)}
      {house(80, f - 20, 1.05, 1, '#FFE3B3', '#C9583F', t, z.meter ?? 1)}
      {house(560, f - 20, 0.95, 2, '#CDE7FF', '#4E6D9C', t)}
      {house(-420, f - 20, 0.95, 3, '#D9F2D0', '#7A5A9C', t)}
      {/* mailbox */}
      <g transform={`translate(300 ${f - 20})`}><rect x={-6} y={-90} width={12} height={90} fill="#6D4C41" /><rect x={-34} y={-130} width={68} height={44} rx={20} fill={BLUE} stroke={OL} strokeWidth={4} />
        <rect x={30} y={-150} width={8} height={30} fill={RED} transform={`rotate(${z.flagAt !== undefined && t > z.flagAt ? -90 : 0} 34 -122)`} /></g>
      {ground(z, f, '#9CCB86', '#86B872')}
      <rect x={z.x0} y={f + 30} width={w} height={70} fill="#9AA5B4" />
      {Array.from({length: 18}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 260} y={f + 62} width={120} height={8} fill="#FFFFFF" />)}
      {z.hyp && t >= (z.hypAt ?? 0) && banner(z.hypX ?? 960, z.hypY ?? 90, z.hypText || 'FORECAST', PURPLE, 26)}
    </g>;
  },

  /** kitchen table: the giant bill with stacked slices */
  bigbill: (t, z, f) => {
    const slices: any[] = z.slices || [], push: any[] = z.push || [], sc = z.scale ?? 3.2, bx = z.billX ?? 1120, by = z.billY ?? 930;
    const stamp = pick(z.stamp, t, ''), st0 = lastAt(z.stamp, t);
    let acc = 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#FFF4DD" />
      {/* wallpaper stripes + window with the campus outside */}
      {Array.from({length: 30}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 120} y={-400} width={50} height={1400} fill="#FCE9C4" />)}
      <g transform="translate(200 120)"><rect x={0} y={0} width={420} height={330} fill="#9ED8F5" stroke={OL} strokeWidth={8} />
        {[0, 1].map((k) => hall(30 + k * 190, 300, 170, 120 + k * 30, 60 + k, t, 1))}
        <path d="M 210 0 L 210 330 M 0 165 L 420 165" stroke={OL} strokeWidth={6} /></g>
      {/* table */}
      <rect x={z.x0} y={by + 30} width={z.x1 - z.x0} height={500} fill="#C98E5A" stroke={OL} strokeWidth={6} />
      {/* bill paper */}
      <g transform={`translate(${bx} ${by}) rotate(${-2 + 0.6 * Math.sin(t * 0.7)})`}>
        <path d="M -330 20 L -330 -820 L 330 -820 L 330 20 L 300 0 L 270 20 L 240 0 L 210 20 L 180 0 L 150 20 L 120 0 L 90 20 L 60 0 L 30 20 L 0 0 L -30 20 L -60 0 L -90 20 L -120 0 L -150 20 L -180 0 L -210 20 L -240 0 L -270 20 L -300 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <T x={-290} y={-770} s={34} a="start">{z.head || 'ELECTRIC BILL'}</T>
        <T x={-290} y={-736} s={20} a="start" w={600} c={GREY}>{z.sub || 'TYPICAL HOME · 1,000 kWh · ONE MONTH'}</T>
        <path d="M -290 -716 L 290 -716" stroke={OL} strokeWidth={3} />
        {(() => { const tot = pick(z.totals, t, z.total || '$150'); return <T x={290} y={-650} s={fit(tot, 420, 60)} a="end" c={RED}>{tot}</T>; })()}
        <T x={-290} y={-660} s={22} a="start" c={GREY}>AMOUNT DUE</T>
        <rect x={-280} y={-40} width={260} height={16} fill="#D7DEE8" />
        {slices.map((b, k) => { if (t < (b.at ?? 0)) return null; const h = b.v * sc * E.out(win(t, b.at ?? 0, 0.6)), y = -60 - acc - h; acc += h;
          const ps = push.find((p) => p.label === b.label), pu = ps && t >= ps.at ? E.outBack(win(t, ps.at, 0.7)) * ps.dv * sc : 0;
          const hi = z.hi && z.hi === b.label;
          return <g key={'bs' + k}>
            <rect x={-270} y={y} width={240} height={Math.max(2, h - 4)} rx={8} fill={b.color || BLUE} stroke={OL} strokeWidth={4} />
            {hi && <rect x={-282} y={y - 8} width={264} height={h + 8} rx={12} fill="none" stroke={GOLD} strokeWidth={8} strokeDasharray="18 10" strokeDashoffset={-t * 60} />}
            {pu > 0 && <g><rect x={-20} y={y + 4} width={pu} height={Math.max(2, h - 12)} rx={6} fill={RED} stroke={OL} strokeWidth={3} opacity={0.92} />
              {Array.from({length: Math.floor(pu / 24)}, (_, q) => <path key={q} d={`M ${-14 + q * 24} ${y + h - 10} L ${2 + q * 24} ${y + 10}`} stroke="#FFFFFF" strokeWidth={3} opacity={0.6} />)}
              {ps.text && <T x={-10 + pu + 12} y={y + h / 2 + 8} s={22} a="start" c={RED}>{ps.text}</T>}</g>}
            <T x={-150} y={y + h / 2 + 9} s={fit(b.label, 220, Math.min(26, h * 0.42))} c="#FFFFFF" st={OL} sw={4}>{b.label}</T>
          </g>; })}
        {z.illus && <g>{banner(0, -585, z.illus, PURPLE, 22)}</g>}
        {stamp && <g transform={`translate(120 -330) rotate(-12) scale(${1 + 1.2 * (1 - E.out(win(t, st0, 0.3)))})`} opacity={E.out(win(t, st0, 0.3))}>
          <rect x={-170} y={-50} width={340} height={100} rx={14} fill="none" stroke={RED} strokeWidth={10} /><T x={0} y={16} s={fit(stamp, 300, 46)} c={RED}>{stamp}</T></g>}
      </g>
      {/* coffee mug and pen */}
      <g transform={`translate(${bx - 470} ${by + 20})`}><rect x={-50} y={-110} width={100} height={110} rx={14} fill={BLUE} stroke={OL} strokeWidth={5} />
        <path d="M 50 -90 Q 90 -60 50 -30" stroke={OL} strokeWidth={8} fill="none" />
        {[0, 1].map((q) => { const u = (t * 0.6 + q / 2) % 1; return <path key={q} d={`M ${-14 + q * 28} ${-130 - u * 80} q 12 -16 0 -32`} stroke="#FFFFFF" strokeWidth={6} fill="none" opacity={1 - u} />; })}</g>
    </g>;
  },

  /** the capacity auction hall */
  auction: (t, z, f) => {
    const price = pick(z.prices, t, ''), p0 = lastAt(z.prices, t), flip = 1 - E.out(win(t, p0, 0.35));
    const sup = clamp(kf(z.supply, t, 0.6)), dem = clamp(kf(z.demand, t, 0.6)), gav = (z.gavel || []).some((g: number) => t >= g && t < g + 0.25);
    const tilt = clamp((dem - sup) * 30, -12, 12);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E9E1F5" />
      {Array.from({length: 24}, (_, k) => <rect key={'pn' + k} x={z.x0 + k * 160} y={-300} width={80} height={1300} fill="#E1D7F0" />)}
      {/* price board */}
      <g transform="translate(960 140)"><rect x={-520} y={-90} width={1040} height={220} rx={18} fill={NAVY} stroke={OL} strokeWidth={8} />
        <T x={0} y={-48} s={26} c="#BFD3FF" ls={3}>{z.board || 'CAPACITY PRICE · $ PER MEGAWATT-DAY'}</T>
        <g transform={`translate(0 ${40}) scale(1 ${1 - 0.9 * flip})`}><T x={0} y={34} s={fit(price, 960, 104)} c={GOLD}>{price}</T></g></g>
      {z.capAt !== undefined && t >= z.capAt && <g opacity={E.out(win(t, z.capAt, 0.4))}>
        <path d={`M 360 330 L 1560 330`} stroke={RED} strokeWidth={12} strokeDasharray="40 18" strokeDashoffset={-t * 40} />
        {plaque(1560, 334, z.capText || 'PRICE CAP', RED, 26, '#FFFFFF')}</g>}
      {/* balance */}
      <g transform={`translate(960 ${f - 40})`}>
        <path d="M -40 0 L 0 -300 L 40 0 Z" fill="#A58BD0" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <g transform={`translate(0 -300) rotate(${tilt})`}>
          <rect x={-560} y={-12} width={1120} height={24} rx={12} fill="#7357C9" stroke={OL} strokeWidth={5} />
          {/* supply crates (left) */}
          <g transform="translate(-430 -12)">{Array.from({length: Math.round(sup * 6)}, (_, q) => <g key={q} transform={`translate(${(q % 2) * 110 - 55} ${-60 - Math.floor(q / 2) * 64})`}>
            <rect x={-50} y={-30} width={100} height={60} rx={6} fill="#F5C26B" stroke={OL} strokeWidth={4} /><path d="M -50 -30 L 50 30 M 50 -30 L -50 30" stroke="#C48F2C" strokeWidth={4} />{bolt(0, 0, 0.3)}</g>)}
            <T x={0} y={60} s={30} c={NAVY}>SUPPLY</T></g>
          {/* demand servers (right) */}
          <g transform="translate(430 -12)">{Array.from({length: Math.round(dem * 7)}, (_, q) => <g key={q} transform={`translate(${(q % 2) * 110 - 55} ${-60 - Math.floor(q / 2) * 64})`}>
            <rect x={-50} y={-30} width={100} height={60} rx={6} fill="#DCE3EC" stroke={OL} strokeWidth={4} />{[0, 1, 2].map((r) => <rect key={r} x={-40} y={-22 + r * 16} width={80} height={10} fill="#B7C3D3" />)}
            <circle cx={36} cy={-18} r={5} fill={(Math.floor(t * 4 + q) % 2) ? CY : GREEN} /></g>)}
            <T x={0} y={60} s={30} c={NAVY}>DEMAND</T></g>
        </g>
      </g>
      {z.shortAt !== undefined && t >= z.shortAt && <g transform={`translate(1400 ${f - 560}) scale(${pop(t, z.shortAt)})`}>
        <path d="M 0 -120 L 30 -120 L 30 120 L 0 120" stroke={RED} strokeWidth={8} fill="none" />
        {banner(210, 10, z.shortText || 'SHORT', RED, 28)}</g>}
      {/* podium + gavel */}
      <g transform={`translate(360 ${f})`}><path d="M -110 0 L -90 -230 L 90 -230 L 110 0 Z" fill="#7357C9" stroke={OL} strokeWidth={6} />
        <rect x={-120} y={-260} width={240} height={34} rx={8} fill="#5B44A8" stroke={OL} strokeWidth={5} />
        {sil(0, -270, 0.9, 1, t, '#2E3B55')}
        <g transform={`translate(70 -330) rotate(${gav ? 40 : -20})`}><rect x={-6} y={-70} width={12} height={80} fill="#8D5A3B" stroke={OL} strokeWidth={3} /><rect x={-34} y={-96} width={68} height={34} rx={8} fill="#6D4C41" stroke={OL} strokeWidth={4} /></g>
        {gav && <g>{[0, 1, 2, 3, 4].map((q) => <path key={q} transform={`translate(110 -250) rotate(${q * 40 - 80})`} d="M 30 0 L 70 0" stroke={GOLD} strokeWidth={6} strokeLinecap="round" />)}</g>}</g>
      {/* bidders */}
      {Array.from({length: 7}, (_, k) => sil(1520 + (k % 4) * 110 - (k > 3 ? 55 : 0), f + 10 - (k > 3 ? 0 : 60), 0.7, k + 4, t + k * 0.4, k % 2 ? '#47577A' : '#3B4A66'))}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={600} fill="#B9A6DC" stroke={OL} strokeWidth={5} />
    </g>;
  },

  /** towers march in; buckets show who pays */
  gridbuild: (t, z, f) => {
    const w = z.x1 - z.x0, b = clamp(kf(z.build, t, 1)), cost = pick(z.cost, t, ''), split: any[] = z.split || [];
    const who = [{n: 'HOMES', c: BLUE}, {n: 'SHOPS', c: GREEN}, {n: 'FACTORIES', c: ORANGE}, {n: 'DATA CENTERS', c: PURPLE}];
    return <g>
      {sky(z, f, '#86CFF2', '#F0FAFF', 'gbsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 800 + t * 14) % (w + 600)) + z.x0 - 300, 110 + (k % 2) * 60, 0.75, k))}
      <path d={`M ${z.x0} ${f - 160} Q ${z.x0 + w * 0.3} ${f - 260} ${z.x0 + w * 0.6} ${f - 170} T ${z.x1} ${f - 190} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#BDE0AB" />
      {Array.from({length: 6}, (_, k) => { const r = clamp(b * 6 - k), x = -200 + k * 260; return r > 0 ? <g key={'tg' + k}>
        <g transform={`translate(0 ${(1 - E.outBack(r)) * 60})`}>{tower(x, f, 0.95, k, r)}</g>
        {k > 0 && r > 0.9 && <path d={`M ${x - 260 - 85} ${f - 237} Q ${x - 130} ${f - 190} ${x - 85} ${f - 237} M ${x - 260 + 85} ${f - 237} Q ${x - 130} ${f - 190} ${x + 85} ${f - 237}`} stroke={OL} strokeWidth={3} fill="none" />}
        {r > 0 && r < 1 && <g transform={`translate(${x + 120} ${f})`}><path d="M 0 0 L 0 -420 M -60 -400 L 200 -400" stroke={GOLD} strokeWidth={10} /><path d={`M 150 -400 L 150 ${-300 + 40 * Math.sin(t * 2)}`} stroke={OL} strokeWidth={3} /></g>}</g> : null; })}
      {pulses(-200, f - 240, 1100, f - 240, 30, 10, t, 0.4, b > 0.95 ? 1 : 0, GOLD, 5)}
      {ground(z, f, '#9CCB86', '#86B872')}
      {/* odometer */}
      {cost && <g transform={`translate(${z.costX ?? 640} 150)`}><rect x={-330} y={-70} width={660} height={150} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={0} y={-30} s={fit(z.costTitle || 'PLANNED SPENDING', 600, 22)} c="#BFD3FF">{z.costTitle || 'PLANNED SPENDING'}</T><T x={0} y={50} s={fit(cost, 600, 60)} c={GOLD}>{cost}</T></g>}
      {/* buckets */}
      {split.length > 0 && <g>{who.map((o, k) => { const s = split.find((q) => q.who === o.n); const v = s ? clamp(kf(s.v, t, 0)) : 0, x = (z.bucketX ?? 1150) + k * 190, hi = z.hi === o.n;
        return <g key={'bk' + k}>
          {hi && <rect x={x - 90} y={f - 330} width={180} height={340} rx={20} fill="none" stroke={GOLD} strokeWidth={8} strokeDasharray="20 10" strokeDashoffset={-t * 60} />}
          <path d={`M ${x - 70} ${f - 220} L ${x - 56} ${f - 10} L ${x + 56} ${f - 10} L ${x + 70} ${f - 220} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <rect x={x - 62 + 6 * (1 - v)} y={f - 12 - 200 * v} width={124 - 12 * (1 - v)} height={200 * v} fill={GOLD} opacity={0.9} />
          {v > 0.05 && Array.from({length: 3}, (_, q) => { const u = (t * 1.2 + q / 3 + k * 0.2) % 1; return coin(x + (q - 1) * 20, f - 420 + u * (200 - 200 * v + 160), 0.7, k * 10 + q); })}
          <rect x={x - 80} y={f - 280} width={160} height={40} rx={20} fill={o.c} stroke={OL} strokeWidth={4} /><T x={x} y={f - 252} s={fit(o.n, 150, 20)} c="#FFFFFF">{o.n}</T>
          {s && s.text && v > 0.05 && <T x={x} y={f + 60} s={26} c={OL}>{s.text}</T>}
        </g>; })}</g>}
    </g>;
  },

  /** regulators' hearing room: contracts, locks and a ghost data center */
  hearing: (t, z, f) => {
    const un = clamp(kf(z.unroll, t, 0)), yrs = z.years ?? 14, lockOn = z.lockAt !== undefined && t >= z.lockAt;
    const ghost = z.ghostAt !== undefined && t >= z.ghostAt ? E.out(win(t, z.ghostAt, 0.8)) : 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E3EEF6" />
      {Array.from({length: 18}, (_, k) => <rect key={'cl' + k} x={z.x0 + k * 220} y={-200} width={36} height={1100} fill="#D2E1EC" />)}
      {/* bench */}
      <g transform="translate(960 420)"><rect x={-520} y={-60} width={1040} height={170} rx={12} fill="#8D5A3B" stroke={OL} strokeWidth={6} />
        {[-300, 0, 300].map((sx, k) => sil(sx, -60, 1, k + 20, t, '#3B4A66'))}
        <rect x={-520} y={-80} width={1040} height={34} rx={8} fill="#6D4C41" stroke={OL} strokeWidth={5} />
        <T x={0} y={60} s={28} c="#FFE9C4" ls={3}>{z.bench || 'STATE UTILITY COMMISSION'}</T></g>
      {/* lectern + presenter of the tariff */}
      {z.lectern !== false && <g transform={`translate(330 ${f})`}><path d="M -70 0 L -50 -170 L 50 -170 L 70 0 Z" fill="#B7C3D3" stroke={OL} strokeWidth={5} />{sil(0, -160, 0.85, 31, t, '#47577A')}</g>}
      {/* contract scroll unrolling */}
      {un > 0 && <g transform={`translate(560 ${f - 20})`}>
        <rect x={0} y={-60} width={1100 * un} height={70} fill="#FFFDF5" stroke={OL} strokeWidth={4} />
        {Array.from({length: yrs}, (_, q) => { const x = ((q + 0.5) / yrs) * 1100; return x < 1100 * un ? <g key={q}><path d={`M ${x} -60 L ${x} -40`} stroke={OL} strokeWidth={3} />
          <T x={x} y={-6} s={20} c={q < (z.ramp ?? 0) ? ORANGE : NAVY}>{q + 1}</T></g> : null; })}
        <circle cx={1100 * un} cy={-25} r={40} fill="#F3E9CF" stroke={OL} strokeWidth={5} />
        <T x={550} y={-80} s={26} c={NAVY}>{z.yearsText || `${yrs}-YEAR CONTRACT`}</T></g>}
      {/* lock */}
      {lockOn && <g transform={`translate(${z.lockX ?? 1720} ${f - 170}) scale(${1.3 * pop(t, z.lockAt, 0.5)}) rotate(${4 * Math.sin(t * 2)})`}>
        <path d="M -50 -40 L -50 -90 Q 0 -150 50 -90 L 50 -40" stroke={GREY} strokeWidth={18} fill="none" />
        <rect x={-80} y={-50} width={160} height={130} rx={18} fill={GOLD} stroke={OL} strokeWidth={6} /><T x={0} y={30} s={fit(z.lockText || 'MINIMUM BILL', 150, 30)}>{z.lockText || 'MINIMUM BILL'}</T></g>}
      {/* ghost data center + stranded line */}
      {ghost > 0 && <g opacity={ghost}>
        <g opacity={0.35 + 0.15 * Math.sin(t * 3)}>{hall(1500, f - 300, 340, 200, 90, t, 1)}</g>
        {plaque(1670, f - 540, z.ghostText || 'NEVER BUILT?', '#FFFFFF', 24, RED)}
        {tower(1250, f - 300, 0.55, 91)}<path d={`M 1300 ${f - 440} Q 1400 ${f - 380} 1480 ${f - 400}`} stroke={OL} strokeWidth={3} fill="none" strokeDasharray="12 8" />
        {/* jars: HOMES vs DATA CENTER */}
        {[['HOMES', 760, BLUE, !lockOn], ['DATA CENTER', 1160, PURPLE, lockOn]].map(([n, jx, c, on], k) => <g key={'jr' + k}>
          <path d={`M ${Number(jx) - 70} ${f - 210} L ${Number(jx) - 60} ${f - 20} L ${Number(jx) + 60} ${f - 20} L ${Number(jx) + 70} ${f - 210} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <rect x={Number(jx) - 80} y={f - 260} width={160} height={40} rx={20} fill={String(c)} stroke={OL} strokeWidth={4} /><T x={Number(jx)} y={f - 232} s={fit(String(n), 150, 20)} c="#FFFFFF">{n}</T>
          {on && Array.from({length: 4}, (_, q) => { const u = (t * 1.1 + q / 4) % 1; return coin(lerp(1420, Number(jx), u), f - 420 + Math.sin(u * Math.PI) * -120 + u * 260, 0.8, k * 10 + q); })}
        </g>)}
      </g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={600} fill="#B9C9D6" stroke={OL} strokeWidth={5} />
    </g>;
  },

  /** power plants, deals and new supply */
  plantdeal: (t, z, f) => {
    const w = z.x1 - z.x0, steam = clamp(kf(z.steam, t, 1)), sup = clamp(kf(z.supply, t, 0)), tag = pick(z.tags, t, ''), t0 = lastAt(z.tags, t);
    return <g>
      {sky(z, f, '#80C9F1', '#EEF9FF', 'pdsky' + Math.round(z.x0))}
      {[0, 1, 2, 3].map((k) => cloud(((k * 720 + t * 12) % (w + 600)) + z.x0 - 300, 100 + (k % 2) * 60, 0.8, k))}
      <rect x={z.x0} y={f - 70} width={w} height={70} fill="#5FA8D8" />
      {Array.from({length: 14}, (_, k) => <path key={'rw' + k} d={`M ${z.x0 + k * 260 + ((t * 30) % 260)} ${f - 40} q 20 -8 40 0`} stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.6} />)}
      {/* plant */}
      {cooling(-160, f - 60, 1, 1, t, steam)}{cooling(140, f - 60, 1, 2, t, steam)}
      <g transform={`translate(420 ${f - 60})`}><rect x={-80} y={-230} width={160} height={230} fill="#C9D2DE" stroke={OL} strokeWidth={5} />
        <path d="M -80 -230 Q 0 -330 80 -230 Z" fill="#E4E8EE" stroke={OL} strokeWidth={5} />
        {z.plantText && plaque(0, 60, z.plantText, NAVY, 22, '#FFFFFF')}</g>
      {/* cable to the campus */}
      {tower(700, f - 60, 0.7, 3)}{tower(1060, f - 60, 0.7, 4)}
      <path d={`M 500 ${f - 230} Q 600 ${f - 200} 700 ${f - 260} Q 880 ${f - 220} 1060 ${f - 260} Q 1200 ${f - 220} 1320 ${f - 200}`} stroke={OL} strokeWidth={3.5} fill="none" />
      {pulses(500, f - 230, 1320, f - 200, 30, 8, t, 0.5, steam, GOLD, 7)}
      {hall(1300, f - 60, 330, 240, 70, t, 1)}{hall(1660, f - 60, 280, 200, 71, t, 1)}
      {z.campusText && plaque(1560, f - 360, z.campusText, NAVY, 22, '#FFFFFF')}
      {/* new supply */}
      {sup > 0 && <g opacity={sup} transform={`translate(0 ${(1 - sup) * 80})`}>{panels(2020, f - 70, 6, 1)}{[0, 1, 2].map((k) => turbine(2700 + k * 170, f - 70, 0.85 - k * 0.1, t, k))}</g>}
      {ground(z, f, '#9CCB86', '#86B872')}
      {/* deal card */}
      {tag && <g transform={`translate(${kf(z.tagX, t, 960)} ${z.tagY ?? 150}) scale(${pop(t, t0, 0.45)}) rotate(${-2 + Math.sin(t * 2)})`}>
        <rect x={-430} y={-70} width={860} height={130} rx={18} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <rect x={-430} y={-70} width={40} height={130} rx={10} fill={GREEN} stroke={OL} strokeWidth={4} />
        <T x={20} y={12} s={fit(tag, 760, 40)}>{tag}</T></g>}
      {z.shakeAt !== undefined && t >= z.shakeAt && <g transform={`translate(${z.shakeX ?? 960} ${f + 20})`}>{sil(-80, 0, 0.9, 40, t)}{sil(80, 0, 0.9, 41, t, '#47577A')}
        <path d={`M -40 -70 Q 0 ${-90 + 8 * Math.sin(t * 14)} 40 -70`} stroke={OL} strokeWidth={14} strokeLinecap="round" fill="none" /></g>}
    </g>;
  },

  /** control room: the price gauge and the verdict dials */
  gaugeroom: (t, z, f) => {
    const lo = z.lo ?? 0, hi = z.hi ?? 30, v = kf(z.needle, t, lo), u = clamp((v - lo) / (hi - lo)), ang = -120 + 240 * u, marks: any[] = z.marks || [], dials: any[] = z.dials || [];
    const gx = z.gaugeX ?? 700, gy = z.gaugeY ?? 560;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E6EEF7" />
      {Array.from({length: 14}, (_, k) => <rect key={'scr' + k} x={z.x0 + 200 + k * 300} y={80} width={240} height={120} rx={10} fill="#1F3358" stroke={OL} strokeWidth={4} />)}
      {Array.from({length: 14}, (_, k) => <path key={'sl' + k} d={`M ${z.x0 + 220 + k * 300} ${170 - 30 * rnd(k)} L ${z.x0 + 290 + k * 300} ${150 - 40 * rnd(k + 3)} L ${z.x0 + 420 + k * 300} ${120 - 20 * Math.sin(t + k)}`} stroke={k % 3 ? CY : GOLD} strokeWidth={4} fill="none" />)}
      {z.gauge !== false && <g transform={`translate(${gx} ${gy})`}>
        <circle r={300} fill="#FFFFFF" stroke={OL} strokeWidth={10} />
        <path d="M -225 130 A 260 260 0 1 1 225 130" stroke="#E8EEF5" strokeWidth={40} fill="none" />
        {[0, 0.25, 0.5, 0.75, 1].map((q) => { const a = ((-120 + 240 * q) * Math.PI) / 180; return <g key={q}><path d={`M ${Math.sin(a) * 230} ${-Math.cos(a) * 230} L ${Math.sin(a) * 280} ${-Math.cos(a) * 280}`} stroke={OL} strokeWidth={6} />
          <T x={Math.sin(a) * 190} y={-Math.cos(a) * 190 + 10} s={30}>{(lo + (hi - lo) * q).toFixed(z.dec ?? 0)}</T></g>; })}
        {marks.map((m, k) => { if (t < (m.at ?? 0)) return null; const a = ((-120 + 240 * clamp((m.v - lo) / (hi - lo))) * Math.PI) / 180;
          return <g key={'mk' + k} opacity={E.out(win(t, m.at ?? 0, 0.4))}><circle cx={Math.sin(a) * 255} cy={-Math.cos(a) * 255} r={14} fill={m.color || BLUE} stroke={OL} strokeWidth={3} />
            <T x={Math.sin(a) * 340} y={-Math.cos(a) * 340 + 8} s={22} c={m.color || NAVY}>{m.label}</T></g>; })}
        <g transform={`rotate(${ang + Math.sin(t * 9) * 0.8})`}><path d="M -14 0 L 0 -250 L 14 0 Z" fill={RED} stroke={OL} strokeWidth={4} /></g>
        <circle r={30} fill={NAVY} stroke={OL} strokeWidth={4} />
        <T x={0} y={130} s={64} c={NAVY}>{v.toFixed(z.dec ?? 1)}</T><T x={0} y={170} s={24} c={GREY}>{z.unit || 'CENTS PER kWh'}</T></g>}
      {dials.map((d, k) => { if (t < (d.at ?? 0)) return null; const x = (z.dialX ?? 1340) + (z.gauge === false ? k * 420 : 0), y = z.gauge === false ? 600 : 300 + k * 230, vv = clamp(kf(d.v, t, 0), -1, 1);
        return <g key={'dl' + k} transform={`translate(${x} ${y}) scale(${pop(t, d.at ?? 0, 0.45)})`}>
          <circle r={95} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
          <path d="M -80 30 A 85 85 0 0 1 80 30" stroke={RED} strokeWidth={14} fill="none" opacity={0.25} />
          <g transform={`rotate(${vv * 70})`}><rect x={-10} y={-85} width={20} height={70} rx={8} fill={NAVY} /></g>
          <circle r={26} fill={vv > 0.2 ? GREEN : vv < -0.2 ? RED : GOLD} stroke={OL} strokeWidth={4} />
          <T x={-110} y={60} s={18} a="end" c={RED}>{d.l || ''}</T><T x={110} y={60} s={18} a="start" c={GREEN}>{d.r || ''}</T>
          <T x={0} y={140} s={fit(d.label, 380, 26)}>{d.label}</T></g>; })}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={600} fill="#B7C6D8" stroke={OL} strokeWidth={5} />
    </g>;
  },

  /** title card: an envelope bursts with a spark */
  pbtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['WHY AI COULD MAKE', 'YOUR ELECTRICITY BILL', 'EXPLODE'], burst = E.outBack(win(t, 0.4, 0.6));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#0F2547" />
      {Array.from({length: 24}, (_, k) => <path key={'ray' + k} transform={`translate(960 600) rotate(${k * 15 + t * 6})`} d="M 0 0 L -60 -1400 L 60 -1400 Z" fill={k % 2 ? '#14305A' : '#0F2547'} />)}
      <g transform={`translate(960 780) scale(${0.55 + 0.3 * burst})`}>
        <rect x={-260} y={-160} width={520} height={320} rx={16} fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        <path d={`M -260 -160 L 0 ${-10 - 160 * burst} L 260 -160`} fill="#F3F6FA" stroke={OL} strokeWidth={8} strokeLinejoin="round" />
        <T x={0} y={40} s={44} c={RED}>ELECTRIC BILL</T>{bolt(0, -170 - 60 * burst, 1.3 * burst)}
        {Array.from({length: 10}, (_, k) => { const a = (k / 10) * Math.PI * 2 + t; return <circle key={k} cx={Math.cos(a) * 380 * burst} cy={-120 + Math.sin(a) * 120 * burst} r={10} fill={k % 2 ? GOLD : CY} opacity={burst} />; })}
      </g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.5 - k * 0.6) / 0.5) * ln.length); return <T key={k} x={960} y={190 + k * 120} s={fit(ln, 1600, k === lines.length - 1 ? 120 : 92)} c={k === lines.length - 1 ? GOLD : '#FFFFFF'} st={OL} sw={12}>{ln.slice(0, n)}</T>; })}
      <T x={960} y={1010} s={30} c={GOLD} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a plug flies into a socket, sparks, the chapter title drops */
  pbbumper: (t, z, f) => {
    const c = z.color || BLUE, plug = E.inOut(win(t, 0.2, 0.7)), hit = t > 0.9 ? E.out(win(t, 0.9, 0.4)) : 0;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g transform="translate(1500 500)"><rect x={-110} y={-150} width={220} height={300} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        {[-36, 36].map((q) => <rect key={q} x={q - 10} y={-50} width={20} height={56} rx={6} fill={OL} />)}<circle cx={0} cy={60} r={14} fill={OL} /></g>
      <g transform={`translate(${lerp(400, 1330, plug)} 500)`}><path d={`M -900 0 Q -600 ${-80 * (1 - plug)} -120 0`} stroke={OL} strokeWidth={22} fill="none" />
        <rect x={-130} y={-70} width={140} height={140} rx={22} fill={GOLD} stroke={OL} strokeWidth={8} />
        {[-36, 36].map((q) => <rect key={q} x={10} y={q - 10} width={60} height={20} rx={6} fill="#D7DEE8" stroke={OL} strokeWidth={4} />)}</g>
      {hit > 0 && t < 1.8 && Array.from({length: 10}, (_, k) => { const a = (k / 10) * Math.PI * 2; return <path key={k} transform={`translate(1400 500) rotate(${(a * 180) / Math.PI})`} d={`M ${60 + 100 * hit} 0 L ${120 + 160 * hit} 0`} stroke={GOLD} strokeWidth={10} strokeLinecap="round" opacity={1 - win(t, 1.3, 0.5)} />; })}
      <g transform={`translate(700 ${300 - 60 * (1 - pop(t, 0.9))})`} opacity={clamp((t - 0.8) / 0.3)}>
        <T x={0} y={0} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T></g>
      <g transform={`translate(700 ${740})`} opacity={clamp((t - 1.0) / 0.3)}><rect x={-600} y={-90} width={1200} height={130} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={0} y={0} s={fit(z.title || '', 1140, 58)} c="#FFFFFF">{z.title || ''}</T></g>
      {t >= 1.6 && <T x={700} y={900} s={fit(z.caption || '', 1200, 34)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.6) / 0.3)}>{z.caption || ''}</T>}
    </g>;
  },
};

/** pbtag: FACT / FORECAST / ESTIMATE / OUR CALC / ILLUSTRATIVE pill (top-left) */
const TAGC: Record<string, string> = {FACT: GREEN, FORECAST: PURPLE, ESTIMATE: ORANGE, OUR: TEAL, ILLUSTRATIVE: PURPLE, MECHANISM: BLUE, DISCLOSED: GREEN, VERDICT: NAVY};
const pbtag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const txt: string = pick(a.tags, t, a.text || 'FACT'); if (!txt) return null;
  const key = txt.split(' ')[0], c = TAGC[key] || NAVY, w = txt.length * 17 + 70, x = kf(a.x, t, 36), y = kf(a.y, t, 36), t0 = Math.max(at, lastAt(a.tags, t));
  return <g key={'pt' + i} transform={`translate(${x} ${y}) scale(${pop(t, t0, 0.35)})`}>
    <rect x={0} y={0} width={w} height={46} rx={23} fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={26} cy={23} r={9} fill="#FFFFFF" /><T x={44} y={32} s={24} a="start" c="#FFFFFF">{txt}</T></g>;
};

/** billpaper: a flying paper bill */
const billpaper: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 300), s = (a.scale ?? 1) * pop(t, at, 0.4), r = (a.spin ?? 0) * t + 6 * Math.sin(t * 3 + i);
  return <g key={'bp' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${r})`}>
    <rect x={-90} y={-120} width={180} height={240} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
    <T x={0} y={-74} s={20}>ELECTRIC BILL</T><path d="M -70 -60 L 70 -60" stroke={OL} strokeWidth={3} />
    {[0, 1, 2, 3].map((q) => <rect key={q} x={-70} y={-44 + q * 26} width={100 - q * 12} height={12} rx={6} fill="#D7DEE8" />)}
    <T x={0} y={92} s={44} c={RED}>{a.amount || '$150'}</T></g>;
};

/** sparky: an original plug mascot */
const sparky: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.5) hy += Math.sin((u / 0.5) * Math.PI) * 90; }
  const x = kf(a.x, t, 960), y = kf(a.y, t, f) - hy, s = (a.scale ?? 1) * pop(t, at, 0.4), face = pick(a.faces, t, a.face || 'happy');
  return <g key={'sk' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d={`M 0 -10 Q ${-80} ${30} ${-160} ${10 + 10 * Math.sin(t * 3)}`} stroke={OL} strokeWidth={12} fill="none" />
    <rect x={-60} y={-150} width={120} height={140} rx={30} fill={GOLD} stroke={OL} strokeWidth={6} />
    {[-26, 26].map((q) => <rect key={q} x={q - 8} y={-200} width={16} height={56} rx={6} fill="#D7DEE8" stroke={OL} strokeWidth={4} />)}
    <circle cx={-20} cy={-90} r={8} fill={OL} /><circle cx={20} cy={-90} r={8} fill={OL} />
    {face === 'shock' ? <ellipse cx={0} cy={-52} rx={14} ry={18} fill={OL} /> : face === 'worry' ? <path d="M -18 -46 Q 0 -60 18 -46" stroke={OL} strokeWidth={5} fill="none" /> : <path d="M -20 -56 Q 0 -36 20 -56" stroke={OL} strokeWidth={5} fill="none" />}
    {a.point && <path d={`M 60 -90 L ${100 + 6 * Math.sin(t * 6)} -130`} stroke={OL} strokeWidth={10} strokeLinecap="round" />}
  </g>;
};

export const POWERBILL_ITEMS: Record<string, ItemFn> = {pbtag, billpaper, sparky};
export const POWERBILL_INDOOR = ['bigbill', 'auction', 'hearing', 'gaugeroom', 'pbtitle', 'pbbumper'];
