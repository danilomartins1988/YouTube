import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * EUROPE kit for CartoonStage (Episode 63, "Could AI Bring Europe Back to Power?").
 *
 * Premium-documentary day world drawn in the channel's prime-time cartoon GENRE (thick clean outlines, flat colour, gentle
 * squash and stretch). Everything ORIGINAL: no logos, flags, seals, brand names or traced product designs; companies appear only
 * as generic buildings or machines with a city name on a plaque. No real person is drawn.
 * Sets:
 *  - eurocity: an original river city by day. Old brick works with chimneys (smoke `smoke` 0..1), a stone old town with a clock
 *    tower, a bridge, and new glass labs, a robot factory and wind turbines that rise with `era` (KF 0..1). `hyp` shows a
 *    SCENARIO banner (`hypText`).
 *  - triad: three plinths (USA / EU / CHINA) whose columns grow to `bars` [{label, v (KF), color, display, at}] (px per unit =
 *    `scale`); `gapAt` draws a measuring bracket between bars `gapA`/`gapB` with `gapText`.
 *  - agewave: a town square with a giant balance: workers on the left pan (`workers` KF count shown as figures), one retiree on
 *    the right; `year` label keyframes; an hourglass that drains.
 *  - squeeze: a factory in a vise; jaws close with `press` KF; left jaw `left`, right jaw `right` labels; an electricity meter
 *    spins (`meterAt`) and price tags pop (`tags` [[t, text]]).
 *  - smartfab: an automated European factory interior with skylights: arms (`arms`), conveyor with parcels, a vision gantry
 *    (`scanX`), a motor that warns (`maintAt`), self-driving carts (`carts`), a cyan digital twin overlay (`twinAt`), technicians
 *    (`techs`), `hi` pulses one system ('vision'|'maint'|'carts'|'twin'|'arms').
 *  - pharmachain: lab -> patent vault -> trial clinic -> plant -> port -> world pharmacies along one road; `stepAt` [t...] lights
 *    each station; `flowAt` starts coins flowing back toward the start; `valueAt` grows a glow on the first three stations.
 *  - medplaza: six generic HQ towers on a plaza with city plaques (`towers` [{city, sub, at, eu}]); an EU rope `ropeAt` groups the EU
 *    towers; `crates` mode: a harbour where many crates sail out and fewer come in (`outAt`, `inAt`).
 *  - lithoweb: a giant original lithography machine (window shows the light path) in the middle; supplier nodes (`sups`) feed in on
 *    the left; chip factories (`fabs`) on the right receive machines; coins flow back (`coinAt`).
 *  - twinfab: factory floor with a holographic twin floating above (`twinAt`); crates of AUTOMATION / SOFTWARE ship out (`shipAt`)
 *    to factory silhouettes in many places.
 *  - jetyard: an assembly hall where an original generic airliner is joined from parts flown/trucked in (`join` KF 0..1); supplier
 *    tags (`sups`).
 *  - ownmap: a European campus (lab, patent vault, decision room) on the left and partner factories abroad on the right; arrows
 *    KNOW-HOW (`licAt`), PRODUCT (`prodAt`), FEE (`feeAt`) and SALES (`saleAt`); `hyp` HYPOTHETICAL banner.
 *  - profitlab: the automation profit experiment: two columns per $100 of sales (`cols` [{name, sub, at, blocks: [{label, v, color}]}])
 *    with the ILLUSTRATIVE MODEL banner always on; `hiLabel` pulses blocks with that label.
 *  - magnet: a generic continent (labelled EUROPE) under a giant horseshoe magnet pulling icons in (`pulls` [{label, at, icon}]);
 *    `risks` [{label, at}] pop as warning signs.
 *  - eutitle / eubumper: show title card (a drafting pen writes the lines over a skyline) and act bumpers.
 * Items: epitag (a pill in the top-left corner saying FACT / MECHANISM / SCENARIO / CONJECTURE / HYPOTHESIS / ILLUSTRATIVE,
 *  `tags` [[t, text]]), compasspen (the drafting-pen mascot that underlines things: `x`, `y` KF, `drawAt`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#13213B';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; flip?: boolean; [k: string]: any};
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

const BLUE = '#2A6FDB', GOLD = '#F2B33D', RED = '#D9483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', PURPLE = '#7357C9', CY = '#21B8E0', STONE = '#E8DCC4', BRICK = '#B4553F', GLASS = '#BFE6F7', NAVY = '#13213B';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'ecl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const banner = (x: number, y: number, txt: string, c = RED, s = 26) => { const w = Math.max(260, txt.length * s * 0.62 + 50);
  return <g transform={`translate(${x} ${y}) rotate(-2)`}><rect x={-w / 2} y={-s} width={w} height={s * 1.7} rx={8} fill={c} stroke={OL} strokeWidth={4} />
    <T x={0} y={s * 0.32} s={s} c="#FFFFFF">{txt}</T></g>; };
const ground = (z: Z, f: number, c = '#A9D18E', c2 = '#8DBB6F') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const pulse = (on: boolean, t: number, x: number, y: number, w: number, h: number) => on ? <rect x={x - 10} y={y - 10} width={w + 20} height={h + 20} rx={18} fill="none" stroke={GOLD} strokeWidth={8} strokeDasharray="22 12" strokeDashoffset={-t * 60} opacity={0.6 + 0.4 * Math.sin(t * 8)} /> : null;
const coin = (x: number, y: number, s = 1, k = 0) => <g key={'cn' + k} transform={`translate(${x} ${y}) scale(${s})`}><circle r={18} fill={GOLD} stroke={OL} strokeWidth={3.5} /><T x={0} y={7} s={20}>$</T></g>;

/** generic person figure (worker/scientist/retiree); `kind`: 'hat'|'coat'|'grey'|'suit' */
const fig = (x: number, y: number, s: number, k: number, t: number, kind = 'hat') => {
  const skin = ['#F6CDA6', '#B97A4B', '#E0A878', '#F3D7BD', '#8D5A3B'][k % 5], body = kind === 'coat' ? '#FFFFFF' : kind === 'grey' ? '#8E9AAF' : kind === 'suit' ? '#2B3A5C' : [TEAL, BLUE, '#E07A2F', GREEN][k % 4];
  const bob = 3 * Math.sin(t * 3 + k);
  return <g key={'fg' + k + kind} transform={`translate(${x} ${y + bob}) scale(${s})`}>
    <path d="M -8 -40 L -8 0 M 8 -40 L 8 0" stroke="#2B3A50" strokeWidth={12} strokeLinecap="round" />
    <rect x={-20} y={-94} width={40} height={58} rx={13} fill={body} stroke={OL} strokeWidth={3.5} />
    <path d={`M -18 -84 L -28 -52 M 18 -84 L ${28 + 4 * Math.sin(t * 2 + k)} -54`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
    <circle cx={0} cy={-112} r={18} fill={skin} stroke={OL} strokeWidth={3.5} />
    {kind === 'hat' && <path d="M -20 -114 Q 0 -148 20 -114 Z" fill={GOLD} stroke={OL} strokeWidth={3.5} />}
    {kind === 'grey' && <path d="M -18 -118 Q 0 -138 18 -118" stroke="#E0E0E0" strokeWidth={9} fill="none" strokeLinecap="round" />}
    {kind === 'coat' && <g><path d="M -16 -122 Q 0 -140 16 -122" stroke="#3E2C22" strokeWidth={8} fill="none" /><rect x={-11} y={-116} width={22} height={7} rx={3} fill="none" stroke={OL} strokeWidth={2.5} /></g>}
    {kind === 'suit' && <path d="M -16 -122 Q 0 -138 16 -122" stroke="#2D2018" strokeWidth={9} fill="none" />}
    <circle cx={-6} cy={-112} r={2.5} fill={OL} /><circle cx={6} cy={-112} r={2.5} fill={OL} /><path d="M -6 -102 Q 0 -98 6 -102" stroke={OL} strokeWidth={2.5} fill="none" />
  </g>;
};

/** a compact original robot arm (two links, gripper), sway speed sp */
const arm = (t: number, k: number, s = 1, color = GOLD) => {
  const ph = t * 1.1 + k * 0.7, a1 = -20 + 30 * Math.sin(ph), a2 = 60 + 30 * Math.cos(ph * 1.3);
  const r1 = (a1 * Math.PI) / 180, r2 = ((a1 + a2) * Math.PI) / 180, ex = Math.sin(r1) * 120, ey = -70 - Math.cos(r1) * 120, wx = ex + Math.sin(r2) * 100, wy = ey - Math.cos(r2) * 100;
  return <g transform={`scale(${s})`}>
    <path d="M -54 0 L -40 -36 L 40 -36 L 54 0 Z" fill="#4A5A70" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    <rect x={-28} y={-80} width={56} height={48} rx={18} fill={color} stroke={OL} strokeWidth={4} />
    <path d={`M 0 -70 L ${ex} ${ey}`} stroke={OL} strokeWidth={32} strokeLinecap="round" /><path d={`M 0 -70 L ${ex} ${ey}`} stroke={color} strokeWidth={22} strokeLinecap="round" />
    <path d={`M ${ex} ${ey} L ${wx} ${wy}`} stroke={OL} strokeWidth={26} strokeLinecap="round" /><path d={`M ${ex} ${ey} L ${wx} ${wy}`} stroke="#D7DEE8" strokeWidth={16} strokeLinecap="round" />
    <circle cx={ex} cy={ey} r={13} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={ex} cy={ey} r={5} fill={CY} />
    <path d={`M ${wx - 12} ${wy} L ${wx - 14} ${wy + 22} M ${wx + 12} ${wy} L ${wx + 14} ${wy + 22}`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
  </g>;
};

/** a generic factory building (sawtooth roof), w x h, colour */
const works = (x: number, y: number, w: number, h: number, c: string, k: number, chimney = 0, smoke = 0, t = 0) => <g key={'wk' + k}>
  {chimney > 0 && Array.from({length: chimney}, (_, q) => { const cx = x + 40 + q * 70; return <g key={q}><rect x={cx} y={y - h - 130} width={34} height={140} fill={BRICK} stroke={OL} strokeWidth={4} />
    {smoke > 0 && [0, 1, 2].map((p) => { const u = ((t * 0.35 + p / 3 + q * 0.2) % 1); return <circle key={p} cx={cx + 17 + u * 60} cy={y - h - 140 - u * 160} r={16 + u * 30} fill="#9EA7B3" opacity={smoke * (1 - u) * 0.8} />; })}</g>; })}
  <path d={`M ${x} ${y} L ${x} ${y - h} ${Array.from({length: Math.max(1, Math.round(w / 80))}, (_, q) => `L ${x + (q + 1) * (w / Math.max(1, Math.round(w / 80))) - (w / Math.max(1, Math.round(w / 80)))} ${y - h - 40} L ${x + (q + 1) * (w / Math.max(1, Math.round(w / 80)))} ${y - h}`).join(' ')} L ${x + w} ${y} Z`}
    fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
  {Array.from({length: Math.max(1, Math.floor(w / 70))}, (_, q) => <rect key={q} x={x + 18 + q * 70} y={y - h + 30} width={40} height={Math.min(60, h - 60)} rx={4} fill={GLASS} stroke={OL} strokeWidth={3} />)}
</g>;

const lab = (x: number, y: number, w: number, h: number, k: number, t: number, glow = 0) => <g key={'lb' + k}>
  {glow > 0 && <rect x={x - 20} y={y - h - 20} width={w + 40} height={h + 20} rx={24} fill={GOLD} opacity={0.25 * glow * (0.7 + 0.3 * Math.sin(t * 4))} />}
  <rect x={x} y={y - h} width={w} height={h} rx={10} fill="#DDEFFB" stroke={OL} strokeWidth={5} />
  {Array.from({length: Math.floor(h / 60)}, (_, r) => Array.from({length: Math.floor(w / 60)}, (_, c) => <rect key={r + '-' + c} x={x + 12 + c * 60} y={y - h + 14 + r * 60} width={46} height={44} fill={(r + c + k) % 3 ? '#9ED4F0' : '#FFFFFF'} opacity={0.9} />))}
  <path d={`M ${x - 10} ${y - h} L ${x + w + 10} ${y - h}`} stroke={OL} strokeWidth={8} />
</g>;

const turbine = (x: number, y: number, s: number, t: number, k: number) => <g key={'tb' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -6 0 L -3 -260 L 3 -260 L 6 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={3} />
  <g transform={`translate(0 -260) rotate(${t * 70 + k * 40})`}>{[0, 120, 240].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 L -8 -14 L 0 -120 L 8 -14 Z" fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}<circle r={8} fill={OL} /></g>
</g>;

const molecule = (x: number, y: number, s: number, t: number) => <g transform={`translate(${x} ${y}) scale(${s}) rotate(${t * 20})`}>
  {[[0, 0], [50, -30], [50, 30], [-50, -30], [-50, 30], [0, 60]].map(([a, b], q) => <g key={q}><path d={`M 0 0 L ${a} ${b}`} stroke={OL} strokeWidth={6} /></g>)}
  {[[0, 0, GOLD], [50, -30, BLUE], [50, 30, RED], [-50, -30, GREEN], [-50, 30, BLUE], [0, 60, PURPLE]].map(([a, b, c], q) => <circle key={q} cx={a as number} cy={b as number} r={q ? 16 : 22} fill={c as string} stroke={OL} strokeWidth={4} />)}
</g>;

/** generic original airliner side view (not a traced design): tube, wing, tail, two engines */
const jet = (x: number, y: number, s: number, join: number) => { const gap = 140 * (1 - join);
  return <g transform={`translate(${x} ${y}) scale(${s})`}>
    <g transform={`translate(${-gap} 0)`}><path d="M -420 -40 Q -480 -40 -500 0 Q -480 40 -420 40 L -120 40 L -120 -40 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      <path d="M -470 -14 L -440 -24 L -440 -6 Z" fill={NAVY} />{Array.from({length: 7}, (_, q) => <circle key={q} cx={-400 + q * 40} cy={-12} r={7} fill={GLASS} stroke={OL} strokeWidth={2} />)}</g>
    <rect x={-120} y={-40} width={240} height={80} fill="#F4F7FA" stroke={OL} strokeWidth={5} />{Array.from({length: 6}, (_, q) => <circle key={q} cx={-100 + q * 40} cy={-12} r={7} fill={GLASS} stroke={OL} strokeWidth={2} />)}
    <g transform={`translate(${gap} 0)`}><path d="M 120 -40 L 380 -40 L 470 -170 L 520 -170 L 500 -20 Q 470 40 380 40 L 120 40 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={470} y={-160} width={30} height={60} fill={BLUE} opacity={0.8} />{Array.from({length: 5}, (_, q) => <circle key={q} cx={150 + q * 40} cy={-12} r={7} fill={GLASS} stroke={OL} strokeWidth={2} />)}</g>
    <g transform={`translate(0 ${120 * (1 - join)})`}><path d="M -60 20 L 160 20 L 40 150 L -20 150 Z" fill="#DCE3EC" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-10} y={70} width={80} height={44} rx={20} fill="#B9C4D3" stroke={OL} strokeWidth={4} /></g>
  </g>; };

/** original lithography machine: a long cabinet with a window showing the light path */
const litho = (x: number, y: number, s: number, t: number) => <g transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-330} y={-330} width={660} height={330} rx={26} fill="#F2F5F9" stroke={OL} strokeWidth={6} />
  <rect x={-310} y={-310} width={180} height={290} rx={16} fill="#E1E8F0" stroke={OL} strokeWidth={4} />
  <rect x={-110} y={-300} width={400} height={200} rx={14} fill="#0F2440" stroke={OL} strokeWidth={5} />
  <path d={`M -90 -150 L 0 -260 L 110 -170 L 200 -270 L 270 -140`} stroke="#B48CFF" strokeWidth={8} fill="none" strokeDasharray="24 14" strokeDashoffset={-t * 120} />
  {[[0, -260], [110, -170], [200, -270]].map(([a, b], q) => <rect key={q} x={a - 22} y={b - 6} width={44} height={12} rx={4} fill="#D7DEE8" stroke={OL} strokeWidth={3} transform={`rotate(${q % 2 ? 20 : -20} ${a} ${b})`} />)}
  <circle cx={-90} cy={-150} r={14} fill="#B48CFF" opacity={0.6 + 0.4 * Math.sin(t * 9)} />
  <rect x={-110} y={-80} width={400} height={50} rx={10} fill="#CFD8E3" stroke={OL} strokeWidth={4} /><circle cx={240} cy={-55} r={16} fill={Math.floor(t * 2) % 2 ? GREEN : '#9BE3BE'} stroke={OL} strokeWidth={3} />
  <rect x={-330} y={-10} width={660} height={20} rx={8} fill="#8D9BB0" stroke={OL} strokeWidth={4} />
</g>;

export const EUROPE_SETS: Record<string, SetFn> = {
  /** original river city: old works, old town, new labs that rise with `era` */
  eurocity: (t, z, f) => {
    const w = z.x1 - z.x0, era = clamp(kf(z.era, t, 0)), smoke = clamp(kf(z.smoke, t, 1 - era));
    return <g>
      {sky(z, f, '#86CDEF', '#EAF6FD', 'ecsky' + Math.round(z.x0))}
      {[0, 1, 2, 3].map((k) => cloud(((k * 700 + t * 10) % (w + 600)) + z.x0 - 300, 110 + (k % 2) * 80, 0.8, k))}
      {/* far hills */}
      <path d={`M ${z.x0} ${f - 220} Q ${z.x0 + w * 0.25} ${f - 330} ${z.x0 + w * 0.5} ${f - 240} T ${z.x1} ${f - 250} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#BFDDB0" />
      {/* old works (left) */}
      {works(-260, f - 60, 520, 230, '#C98468', 1, 3, smoke, t)}
      {/* old town: stone houses + clock tower */}
      {Array.from({length: 6}, (_, k) => { const hx = 340 + k * 95, hh = 170 + (k % 3) * 40; return <g key={'oh' + k}>
        <rect x={hx} y={f - 60 - hh} width={90} height={hh} fill={['#F1D9B5', '#E8C7A0', '#F5E6CC', '#E2B98F'][k % 4]} stroke={OL} strokeWidth={4} />
        <path d={`M ${hx - 6} ${f - 60 - hh} L ${hx + 45} ${f - 60 - hh - 60} L ${hx + 96} ${f - 60 - hh} Z`} fill={k % 2 ? '#B85C3F' : '#5B6F8F'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        {[0, 1].map((r) => <rect key={r} x={hx + 18} y={f - 40 - hh + r * 60} width={22} height={30} fill={GLASS} stroke={OL} strokeWidth={2.5} />)}
        {[0, 1].map((r) => <rect key={'b' + r} x={hx + 52} y={f - 40 - hh + r * 60} width={22} height={30} fill={GLASS} stroke={OL} strokeWidth={2.5} />)}</g>; })}
      <g transform={`translate(700 ${f - 60})`}><rect x={-40} y={-430} width={80} height={430} fill={STONE} stroke={OL} strokeWidth={5} />
        <path d="M -50 -430 L 0 -540 L 50 -430 Z" fill="#5B6F8F" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <circle cx={0} cy={-370} r={30} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        <path d={`M 0 -370 L ${Math.sin(t * 0.5) * 20} ${-370 - Math.cos(t * 0.5) * 20} M 0 -370 L ${Math.sin(t * 6) * 14} ${-370 - Math.cos(t * 6) * 14}`} stroke={OL} strokeWidth={4} strokeLinecap="round" /></g>
      {/* new district (right) rises with era */}
      <g transform={`translate(0 ${(1 - era) * 520})`} opacity={0.25 + 0.75 * era}>
        {lab(1060, f - 60, 240, 420, 1, t, era)}{lab(1320, f - 60, 200, 300, 2, t)}
        {works(1560, f - 60, 380, 200, '#E9EEF4', 3)}
        <g transform={`translate(1750 ${f - 300})`}>{arm(t, 1, 0.6, GOLD)}</g>
        {[0, 1, 2].map((k) => turbine(2050 + k * 170, f - 60, 0.9 - k * 0.12, t, k))}
      </g>
      {/* river and bridge */}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#5FA8D8" />
      {Array.from({length: 16}, (_, k) => <path key={'rw' + k} d={`M ${z.x0 + k * 220 + ((t * 30) % 220)} ${f - 34} q 20 -8 40 0`} stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.6} />)}
      <path d={`M 860 ${f - 60} Q 960 ${f - 130} 1060 ${f - 60}`} stroke={STONE} strokeWidth={22} fill="none" /><path d={`M 860 ${f - 60} Q 960 ${f - 130} 1060 ${f - 60}`} stroke={OL} strokeWidth={4} fill="none" />
      {ground(z, f, '#B7D7A0', '#9CC487')}
      {z.hyp && t >= (z.hypAt ?? 0) && banner(z.hypX ?? 960, z.hypY ?? 90, z.hypText || 'SCENARIO · NOT A FORECAST', PURPLE, 26)}
    </g>;
  },

  /** three plinths with growing columns (USA / EU / CHINA) */
  triad: (t, z, f) => {
    const w = z.x1 - z.x0, bars: any[] = z.bars || [], sc = z.scale ?? 18, gap = z.gap ?? 420, x0 = z.colX ?? (960 - ((bars.length - 1) * gap) / 2), base = f - 40;
    const top = (k: number) => base - kf(bars[k].v, t, 0) * sc * E.out(win(t, bars[k].at ?? 0, 1.2));
    return <g>
      {sky(z, f, '#DCE7F2', '#F6F9FC', 'trsky' + Math.round(z.x0))}
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'gl' + k} d={`M ${z.x0 + k * 120} ${f - 1000} L ${z.x0 + k * 120} ${f}`} stroke="#E4ECF4" strokeWidth={3} />)}
      {ground(z, f, '#C9D6E3', '#B2C3D5')}
      {z.title && plaque(960, 110, z.title, NAVY, 30, '#FFFFFF')}
      {bars.map((b, k) => { const x = x0 + k * gap, at = b.at ?? 0, y = top(k), on = t >= at;
        return <g key={'tb' + k}>
          <rect x={x - 150} y={base} width={300} height={40} rx={8} fill="#8FA1B6" stroke={OL} strokeWidth={4} />
          {on && <g><rect x={x - 110} y={y} width={220} height={base - y} rx={10} fill={b.color || BLUE} stroke={OL} strokeWidth={5} />
            {Array.from({length: Math.floor((base - y) / 60)}, (_, q) => <rect key={q} x={x - 90} y={base - 50 - q * 60} width={180} height={10} rx={5} fill="#FFFFFF" opacity={0.25} />)}
            <g transform={`translate(${x} ${y - 44}) scale(${pop(t, at + 1.0)})`}><rect x={-120} y={-32} width={240} height={52} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(b.display || '', 220, 30)}>{b.display || ''}</T></g></g>}
          <T x={x} y={base + 110} s={fit(b.label, 280, 44)} c={OL}>{b.label}</T>
        </g>; })}
      {z.gapAt !== undefined && t >= z.gapAt && bars.length > Math.max(z.gapA ?? 0, z.gapB ?? 1) && (() => { const a = z.gapA ?? 0, b = z.gapB ?? 1, xa = x0 + a * gap + 130, ya = top(a), yb = top(b), u = E.out(win(t, z.gapAt, 0.8)), xb = x0 + b * gap - 130;
        const xm = (xa + xb) / 2; return <g opacity={u}>
          <path d={`M ${xa} ${ya} L ${xm + 40} ${ya} M ${xb} ${yb} L ${xm + 40} ${yb}`} stroke={RED} strokeWidth={4} strokeDasharray="10 8" />
          <path d={`M ${xm + 40} ${ya} L ${xm + 40} ${lerp(ya, yb, u)}`} stroke={RED} strokeWidth={8} strokeLinecap="round" />
          {z.gapText && <g transform={`translate(${xm + 40} ${(ya + yb) / 2})`}><rect x={-150} y={-30} width={300} height={50} rx={12} fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={5} s={fit(z.gapText, 280, 26)} c="#FFFFFF">{z.gapText}</T></g>}</g>; })()}
      {z.foot && <T x={960} y={f + 175} s={20} c="#4A5870" w={700}>{z.foot}</T>}
    </g>;
  },

  /** workers vs retirees on a giant balance */
  agewave: (t, z, f) => {
    const w = z.x1 - z.x0, nW = kf(z.workers, t, 3), tilt = clamp((nW - 1) / 3) * -10, cx = 960, py = f - 520;
    const yr = pick(z.years, t, z.year || '');
    return <g>
      {sky(z, f, '#9AD4F2', '#ECF7FD', 'agsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 800 + t * 9) % (w + 600)) + z.x0 - 300, 120 + k * 50, 0.8, k))}
      {/* square: arcades */}
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => { const ax = z.x0 + k * 200; return <g key={'ar' + k}><rect x={ax} y={f - 420} width={200} height={360} fill={k % 2 ? '#F1D9B5' : '#EBCFA6'} stroke={OL} strokeWidth={3} />
        <path d={`M ${ax + 30} ${f - 60} L ${ax + 30} ${f - 200} Q ${ax + 100} ${f - 280} ${ax + 170} ${f - 200} L ${ax + 170} ${f - 60}`} fill="#7A5B45" opacity={0.55} stroke={OL} strokeWidth={3} />
        <rect x={ax + 60} y={f - 390} width={80} height={60} fill={GLASS} stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={z.x0} y={f - 60} width={w} height={60} fill="#D9CDB8" />
      {ground(z, f, '#CDBFA6', '#B9A98C')}
      {/* balance */}
      <path d={`M ${cx - 40} ${f - 60} L ${cx} ${py} L ${cx + 40} ${f - 60} Z`} fill="#8D9BB0" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <g transform={`translate(${cx} ${py}) rotate(${tilt})`}>
        <rect x={-560} y={-12} width={1120} height={24} rx={12} fill={GOLD} stroke={OL} strokeWidth={5} />
        <g transform={`rotate(${-tilt} -520 0)`}><path d="M -520 0 L -640 160 M -520 0 L -400 160" stroke={OL} strokeWidth={4} />
          <path d="M -680 160 L -360 160 L -390 200 L -650 200 Z" fill="#CFD8E3" stroke={OL} strokeWidth={5} />
          {Array.from({length: 4}, (_, q) => <g key={q} opacity={clamp(nW - q)}>{fig(-610 + q * 72, 160, 0.72, q, t, q % 2 ? 'hat' : 'suit')}</g>)}
          {plaque(-520, 250, 'WORKERS', BLUE, 26, '#FFFFFF')}</g>
        <g transform={`rotate(${-tilt} 520 0)`}><path d="M 520 0 L 400 160 M 520 0 L 640 160" stroke={OL} strokeWidth={4} />
          <path d="M 360 160 L 680 160 L 650 200 L 390 200 Z" fill="#CFD8E3" stroke={OL} strokeWidth={5} />
          {fig(520, 160, 0.72, 2, t, 'grey')}
          {plaque(520, 250, 'RETIREE', '#8E9AAF', 26, '#FFFFFF')}</g>
      </g>
      <g transform={`translate(${cx} ${py - 90})`}><rect x={-170} y={-50} width={340} height={80} rx={16} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={8} s={40}>{`${nW.toFixed(1).replace('.0', '')} : 1`}</T></g>
      {yr && plaque(cx, 120, yr, NAVY, 34, '#FFFFFF')}
      {/* hourglass */}
      {z.glass !== false && <g transform={`translate(${z.glassX ?? 1720} ${f - 380})`}><path d="M -60 -120 L 60 -120 L 6 0 L 60 120 L -60 120 L -6 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <path d={`M ${-48 * (1 - clamp(t / 12))} ${-110 + 100 * clamp(t / 12)} L ${48 * (1 - clamp(t / 12))} ${-110 + 100 * clamp(t / 12)} L 4 -6 L -4 -6 Z`} fill={GOLD} />
        <path d={`M -50 112 L 50 112 L ${36 * clamp(t / 12) + 4} ${112 - 70 * clamp(t / 12)} L ${-36 * clamp(t / 12) - 4} ${112 - 70 * clamp(t / 12)} Z`} fill={GOLD} /></g>}
    </g>;
  },

  /** a factory in a vise */
  squeeze: (t, z, f) => {
    const w = z.x1 - z.x0, p = clamp(kf(z.press, t, 0)), jx = 520 - 140 * p, tags: [number, string][] = z.tags || [];
    return <g>
      {sky(z, f, '#DCE7F2', '#F6F9FC', 'sqsky' + Math.round(z.x0))}
      {ground(z, f, '#C9D6E3', '#B2C3D5')}
      {/* the works, squashed */}
      <g transform={`translate(960 ${f}) scale(${1 - 0.18 * p} ${1 + 0.08 * p})`}>{works(-260, 0, 520, 260, '#C98468', 9, 2, 0.6, t)}</g>
      {/* vise jaws */}
      {[-1, 1].map((d) => <g key={d} transform={`translate(${960 + d * (jx + 60)} ${f - 200})`}>
        <rect x={-60} y={-200} width={120} height={360} rx={14} fill={d < 0 ? RED : PURPLE} stroke={OL} strokeWidth={6} />
        <g transform="rotate(-90)"><T x={0} y={10} s={fit(d < 0 ? (z.left || 'ENERGY') : (z.right || 'COMPETITION'), 320, 34)} c="#FFFFFF" st={OL} sw={5}>{d < 0 ? (z.left || 'ENERGY') : (z.right || 'COMPETITION')}</T></g>
        <rect x={d * 60 + (d < 0 ? -380 : 0)} y={-20} width={380} height={40} fill="#8D9BB0" stroke={OL} strokeWidth={4} />
      </g>)}
      {/* electricity meter */}
      {z.meterAt !== undefined && t >= z.meterAt && <g transform={`translate(${z.meterX ?? 300} ${f - 620}) scale(${pop(t, z.meterAt)})`}>
        <rect x={-110} y={-110} width={220} height={200} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><circle cx={0} cy={-20} r={60} fill="#F6F9FC" stroke={OL} strokeWidth={4} />
        <path d={`M 0 -20 L ${Math.sin(t * 6) * 50} ${-20 - Math.cos(t * 6) * 50}`} stroke={RED} strokeWidth={6} strokeLinecap="round" />
        <T x={0} y={70} s={22}>{z.meterText || 'POWER BILL'}</T><path d="M -14 -150 L 6 -150 L -4 -120 L 14 -120 L -10 -80 L -2 -112 L -18 -112 Z" fill={GOLD} stroke={OL} strokeWidth={3} /></g>}
      {tags.map(([at, txt], k) => t >= at ? <g key={'tg' + k} transform={`translate(${z.tagX ?? 1560} ${f - 640 + k * 120}) rotate(${-6 + 4 * Math.sin(t * 2 + k)}) scale(${pop(t, at)})`}>
        <path d="M -150 -40 L 130 -40 L 170 0 L 130 40 L -150 40 Z" fill={GOLD} stroke={OL} strokeWidth={5} strokeLinejoin="round" /><circle cx={130} cy={0} r={8} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
        <T x={-10} y={10} s={fit(txt, 270, 28)}>{txt}</T></g> : null)}
    </g>;
  },

  /** automated European factory interior */
  smartfab: (t, z, f) => {
    const w = z.x1 - z.x0, hi: string = z.hiAt ? pick(z.hiAt, t, z.hi) : z.hi, nA = z.arms ?? 4, ax0 = z.armX ?? 200, ag = z.armGap ?? 420, beltY = f - 140, scanX = z.scanX ?? 1500;
    const twin = z.twinAt !== undefined ? E.out(win(t, z.twinAt, 1.2)) : 0, maint = z.maintAt !== undefined && t >= z.maintAt;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EEF3F8" />
      {/* skylights */}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => { const sx = z.x0 + k * 300; return <g key={'sk' + k}><path d={`M ${sx} ${f - 760} L ${sx + 150} ${f - 840} L ${sx + 300} ${f - 760} Z`} fill={GLASS} stroke={OL} strokeWidth={4} />
        <path d={`M ${sx + 100} ${f - 790} L ${sx + 200} ${f - 790} L ${sx + 300} ${f} L ${sx} ${f} Z`} fill="#FFF8D6" opacity={0.15} /></g>; })}
      <rect x={z.x0} y={f - 760} width={w} height={14} fill="#8D9BB0" stroke={OL} strokeWidth={4} />
      {/* overhead rail */}
      <rect x={z.x0} y={f - 600} width={w} height={18} fill="#A9B6C6" stroke={OL} strokeWidth={3} />
      {/* conveyor */}
      <rect x={z.x0} y={beltY} width={w} height={34} fill="#3D4B5E" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <circle key={'rl' + k} cx={z.x0 + k * 60 + ((t * 80) % 60)} cy={beltY + 17} r={9} fill="#6C7A8E" />)}
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const px = z.x0 + ((k * 260 + t * 80) % (w + 260)) - 130; return <g key={'pc' + k} transform={`translate(${px} ${beltY})`}>
        <rect x={-34} y={-50} width={68} height={50} rx={6} fill="#D7A86E" stroke={OL} strokeWidth={3.5} /><path d="M -34 -34 L 34 -34" stroke={OL} strokeWidth={2} /></g>; })}
      {/* arms */}
      {Array.from({length: nA}, (_, k) => <g key={'am' + k} transform={`translate(${ax0 + k * ag} ${beltY - 10})`}>{arm(t, k, 0.95, [GOLD, '#E07A2F', BLUE][k % 3])}</g>)}
      {pulse(hi === 'arms', t, ax0 - 90, beltY - 300, (nA - 1) * ag + 180, 300)}
      {/* vision gantry */}
      <g transform={`translate(${scanX} ${beltY})`}>
        <path d="M -120 0 L -120 -320 L 120 -320 L 120 0" stroke="#4A5A70" strokeWidth={16} fill="none" /><rect x={-40} y={-340} width={80} height={46} rx={10} fill={NAVY} stroke={OL} strokeWidth={4} />
        <circle cx={0} cy={-317} r={13} fill={CY} />
        <path d={`M -14 -296 L ${-90 + 80 * Math.sin(t * 3)} -6 L ${90 + 80 * Math.sin(t * 3)} -6 L 14 -296 Z`} fill={CY} opacity={0.25} />
        {Math.sin(t * 3) > 0.6 && <g transform="translate(0 -380)"><circle r={26} fill={GREEN} stroke={OL} strokeWidth={4} /><path d="M -12 0 L -3 10 L 14 -10" stroke="#FFFFFF" strokeWidth={6} fill="none" strokeLinecap="round" /></g>}
      </g>
      {pulse(hi === 'vision', t, scanX - 140, beltY - 420, 280, 420)}
      {/* maintenance motor */}
      <g transform={`translate(${z.maintX ?? 700} ${f - 470})`}>
        <rect x={-80} y={-50} width={160} height={100} rx={20} fill="#90A4BC" stroke={OL} strokeWidth={5} /><circle cx={0} cy={0} r={30} fill="#5D6E84" stroke={OL} strokeWidth={4} />
        <path d={`M 0 0 L ${Math.cos(t * 9) * 26} ${Math.sin(t * 9) * 26}`} stroke="#FFFFFF" strokeWidth={5} />
        {maint && [0, 1, 2].map((q) => { const u = ((t - z.maintAt) * 0.8 + q / 3) % 1; return <circle key={q} r={40 + u * 90} fill="none" stroke={RED} strokeWidth={5} opacity={1 - u} />; })}
        {maint && <g transform={`translate(0 -110) scale(${pop(t, z.maintAt + 0.6)})`}><rect x={-120} y={-30} width={240} height={48} rx={12} fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={22} c="#FFFFFF">SERVICE SOON</T></g>}
      </g>
      {pulse(hi === 'maint', t, (z.maintX ?? 700) - 100, f - 540, 200, 140)}
      {/* carts */}
      {Array.from({length: z.carts ?? 2}, (_, k) => { const cx = z.x0 + ((k * 900 + t * 150) % (w + 300)) - 150; return <g key={'ct' + k} transform={`translate(${cx} ${f - 6})`}>
        <rect x={-70} y={-30} width={140} height={30} rx={10} fill="#37474F" stroke={OL} strokeWidth={4} /><rect x={-60} y={-26} width={120} height={7} rx={3} fill={Math.floor(t * 3 + k) % 2 ? CY : '#FFFFFF'} />
        <rect x={-46} y={-78} width={92} height={48} rx={4} fill="#D7A86E" stroke={OL} strokeWidth={3} /></g>; })}
      {pulse(hi === 'carts', t, z.x0 + 20, f - 100, w - 40, 100)}
      {/* technicians */}
      {Array.from({length: z.techs ?? 2}, (_, k) => fig((z.techX ?? 420) + k * (z.techGap ?? 900), f, 1.0, k + 1, t, k % 2 ? 'coat' : 'hat'))}
      {/* digital twin overlay */}
      {twin > 0 && <g opacity={twin} transform={`translate(0 ${-30 * (1 - twin)})`}>
        <rect x={z.twinX0 ?? 200} y={f - 720} width={z.twinW ?? 1520} height={300} rx={20} fill="#0E2A4A" opacity={0.75} stroke={CY} strokeWidth={4} />
        {Array.from({length: 6}, (_, k) => <g key={'tw' + k} transform={`translate(${(z.twinX0 ?? 200) + 140 + k * ((z.twinW ?? 1520) - 280) / 5} ${f - 470})`}>
          <path d={`M -40 0 L -30 -30 L 30 -30 L 40 0 Z M 0 -30 L ${30 * Math.sin(t * 2 + k)} -110 L ${60 * Math.sin(t * 2 + k)} -140`} stroke={CY} strokeWidth={4} fill="none" /></g>)}
        <path d={`M ${(z.twinX0 ?? 200) + 40} ${f - 470} L ${(z.twinX0 ?? 200) + (z.twinW ?? 1520) - 40} ${f - 470}`} stroke={CY} strokeWidth={3} strokeDasharray="14 10" strokeDashoffset={-t * 60} />
        <T x={(z.twinX0 ?? 200) + (z.twinW ?? 1520) / 2} y={f - 670} s={30} c={CY}>DIGITAL TWIN · TEST THE LINE BEFORE YOU BUILD IT</T></g>}
      {pulse(hi === 'twin', t, z.twinX0 ?? 200, f - 720, z.twinW ?? 1520, 300)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B8C4D2" /><rect x={z.x0} y={f} width={w} height={14} fill="#9DACBE" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the medicine value chain along one road */
  pharmachain: (t, z, f) => {
    const w = z.x1 - z.x0, steps: number[] = z.stepAt || [], on = (k: number) => steps[k] !== undefined && t >= steps[k], sx = z.sx ?? 260, sg = z.sg ?? 340, y = f - 40;
    const val = z.valueAt !== undefined ? E.out(win(t, z.valueAt, 1.0)) : 0;
    const names = z.names || ['RESEARCH', 'PATENTS', 'TRIALS', 'FACTORY', 'SHIPPING', 'PHARMACIES'];
    const st = (k: number) => { const x = sx + k * sg, g = on(k) ? pop(t, steps[k], 0.5) : 0.0, glow = k < 3 ? val : 0;
      return <g key={'st' + k} transform={`translate(${x} ${y})`} opacity={0.3 + 0.7 * Math.min(1, g)}>
        {glow > 0 && <circle cx={0} cy={-150} r={150} fill={GOLD} opacity={0.3 * glow * (0.75 + 0.25 * Math.sin(t * 4 + k))} />}
        {k === 0 && <g>{lab(-110, 0, 220, 230, 0, t)}{molecule(0, -300, 0.7, t)}</g>}
        {k === 1 && <g><rect x={-100} y={-230} width={200} height={230} rx={14} fill="#B0BEC5" stroke={OL} strokeWidth={5} /><circle cx={0} cy={-115} r={70} fill="#90A4AE" stroke={OL} strokeWidth={5} />
          <circle cx={0} cy={-115} r={20} fill={GOLD} stroke={OL} strokeWidth={4} />{[0, 60, 120, 180, 240, 300].map((r) => <path key={r} transform={`rotate(${r + t * 10} 0 -115)`} d="M 0 -170 L 0 -150" stroke={OL} strokeWidth={6} />)}
          <g transform={`translate(0 -290) rotate(${Math.sin(t * 2) * 5})`}><rect x={-70} y={-40} width={140} height={70} rx={6} fill="#FFF8E1" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={22}>PATENT</T></g></g>}
        {k === 2 && <g><rect x={-120} y={-200} width={240} height={200} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><path d="M -20 -150 L 20 -150 M 0 -170 L 0 -130" stroke={RED} strokeWidth={12} />
          <g transform="translate(0 -280)"><rect x={-60} y={-60} width={120} height={150} rx={8} fill="#F5F0E1" stroke={OL} strokeWidth={4} />{[0, 1, 2].map((q) => <path key={q} d={`M -36 ${-28 + q * 34} L -26 ${-18 + q * 34} L -10 ${-38 + q * 34}`} stroke={t > (steps[2] ?? 0) + 0.5 + q * 0.4 ? GREEN : '#CCCCCC'} strokeWidth={6} fill="none" />)}</g></g>}
        {k === 3 && <g>{works(-160, 0, 320, 200, '#E9EEF4', 30)}</g>}
        {k === 4 && <g><path d="M -150 -60 L 150 -60 L 120 0 L -120 0 Z" fill={BLUE} stroke={OL} strokeWidth={5} /><rect x={-110} y={-130} width={70} height={70} fill={GOLD} stroke={OL} strokeWidth={4} /><rect x={-30} y={-130} width={70} height={70} fill={GREEN} stroke={OL} strokeWidth={4} /><rect x={50} y={-130} width={70} height={70} fill={RED} stroke={OL} strokeWidth={4} /></g>}
        {k === 5 && <g>{[-90, 0, 90].map((dx, q) => <g key={q} transform={`translate(${dx} 0)`}><rect x={-40} y={-150} width={80} height={150} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><path d="M -12 -120 L 12 -120 M 0 -132 L 0 -108" stroke={GREEN} strokeWidth={8} /><rect x={-24} y={-70} width={48} height={70} fill={GLASS} stroke={OL} strokeWidth={3} /></g>)}</g>}
        <rect x={-140} y={20} width={280} height={56} rx={12} fill={on(k) ? (k < 3 ? GOLD : BLUE) : '#CFD8E3'} stroke={OL} strokeWidth={4} />
        <T x={0} y={58} s={fit(names[k], 260, 26)} c={on(k) && k >= 3 ? '#FFFFFF' : OL}>{names[k]}</T>
      </g>; };
    return <g>
      {sky(z, f, '#9AD4F2', '#EEF8FD', 'pcsky' + Math.round(z.x0))}
      {[0, 1].map((k) => cloud(((k * 1000 + t * 9) % (w + 600)) + z.x0 - 300, 120 + k * 60, 0.8, k))}
      {ground(z, f, '#B7D7A0', '#9CC487')}
      <rect x={z.x0} y={y + 4} width={w} height={36} fill="#8E99A8" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 120} y={y + 18} width={60} height={8} fill="#FFFFFF" />)}
      {[0, 1, 2, 3, 4, 5].map(st)}
      {/* product boxes travel right, coins travel back */}
      {on(3) && Array.from({length: 4}, (_, k) => { const u = ((t * 0.3 + k / 4) % 1), px = sx + 3 * sg + u * 2 * sg; return <g key={'bx' + k} transform={`translate(${px} ${y - 6})`}><rect x={-18} y={-26} width={36} height={26} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><path d="M -6 -14 L 6 -14 M 0 -20 L 0 -8" stroke={RED} strokeWidth={3} /></g>; })}
      {z.flowAt !== undefined && t >= z.flowAt && Array.from({length: 10}, (_, k) => { const u = ((t - z.flowAt) * 0.25 + k / 10) % 1, px = sx + 5 * sg - u * 5 * sg; return coin(px, f - 480 - Math.sin(u * Math.PI) * 120, 1.1, k); })}
      {z.flowAt !== undefined && t >= z.flowAt && <g transform={`translate(${sx + 2.5 * sg} ${f - 700}) scale(${pop(t, z.flowAt)})`}><rect x={-330} y={-34} width={660} height={56} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={26}>{z.flowText || 'MONEY FLOWS BACK TO THE IDEAS'}</T></g>}
    </g>;
  },

  /** six HQ towers on a plaza with an EU rope; or a harbour of medicine crates */
  medplaza: (t, z, f) => {
    const w = z.x1 - z.x0, tw: any[] = z.towers || [], gap = z.gap ?? 290, x0 = z.tx0 ?? (960 - ((tw.length - 1) * gap) / 2);
    const rope = z.ropeAt !== undefined ? E.out(win(t, z.ropeAt, 1.0)) : 0;
    return <g>
      {sky(z, f, '#9AD4F2', '#EEF8FD', 'mpsky' + Math.round(z.x0))}
      {[0, 1].map((k) => cloud(((k * 1000 + t * 9) % (w + 600)) + z.x0 - 300, 110 + k * 60, 0.8, k))}
      {z.harbour ? <g>
        <rect x={z.x0} y={f - 200} width={w} height={900} fill="#5FA8D8" />
        {Array.from({length: 16}, (_, k) => <path key={'hw' + k} d={`M ${z.x0 + k * 240 + ((t * 26) % 240)} ${f - 150 + (k % 3) * 50} q 20 -10 40 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.5} />)}
        <rect x={z.x0} y={f - 210} width={760 - z.x0} height={60} fill="#B0A48E" stroke={OL} strokeWidth={4} />
        {plaque(380, f - 260, 'EU PORT', NAVY, 28, '#FFFFFF')}
        {z.outAt !== undefined && t >= z.outAt && [0, 1].map((k) => { const u = clamp((t - z.outAt - k * 1.6) / 6); return <g key={'so' + k} transform={`translate(${800 + u * 1400} ${f - 130 + k * 90})`}>
          <path d="M -200 -40 L 200 -40 L 160 30 L -170 30 Z" fill={BLUE} stroke={OL} strokeWidth={5} />
          {Array.from({length: 5}, (_, q) => <rect key={q} x={-180 + q * 72} y={-100} width={64} height={60} fill={[GOLD, GREEN, RED, '#FFFFFF', PURPLE][q]} stroke={OL} strokeWidth={3} />)}
          {Array.from({length: 4}, (_, q) => <rect key={'b' + q} x={-150 + q * 72} y={-160} width={64} height={60} fill={[GREEN, '#FFFFFF', GOLD, RED][q]} stroke={OL} strokeWidth={3} />)}
          <T x={0} y={8} s={22} c="#FFFFFF">EXPORTS</T></g>; })}
        {z.inAt !== undefined && t >= z.inAt && (() => { const u = clamp((t - z.inAt) / 5); return <g transform={`translate(${2300 - u * 1000} ${f - 40})`}>
          <path d="M -140 -30 L 140 -30 L 110 24 L -120 24 Z" fill={'#7E8DA3'} stroke={OL} strokeWidth={5} />
          {Array.from({length: 3}, (_, q) => <rect key={q} x={-110 + q * 72} y={-86} width={64} height={56} fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}
          <T x={0} y={8} s={20} c="#FFFFFF">IMPORTS</T></g>; })()}
      </g> : <g>
        <rect x={z.x0} y={f - 40} width={w} height={40} fill="#DCD3C2" />
        {ground(z, f, '#CFC5B2', '#BBAF98')}
        {rope > 0 && (() => { const eu = tw.map((o, k) => ({o, k})).filter((p) => p.o.eu); if (!eu.length) return null; const xa = x0 + eu[0].k * gap - 140, xb = x0 + eu[eu.length - 1].k * gap + 140;
          return <g opacity={rope}><rect x={xa} y={f - 640} width={(xb - xa) * rope} height={640} rx={30} fill="#2A6FDB" opacity={0.1} stroke={BLUE} strokeWidth={6} strokeDasharray="20 12" />
            {plaque((xa + xb) / 2, f - 670, z.ropeText || 'EU MEMBERS', BLUE, 28, '#FFFFFF')}</g>; })()}
        {tw.map((o, k) => { const x = x0 + k * gap, at = o.at ?? 0; if (t < at) return null; const h = 380 + (k % 3) * 70, g = E.outBack(win(t, at, 0.6));
          return <g key={'tw' + k} transform={`translate(${x} ${f - 40}) scale(1 ${g})`}>
            <rect x={-100} y={-h} width={200} height={h} rx={10} fill={['#DDEFFB', '#E8E2F7', '#E2F4EA', '#FCEBD9', '#E6ECF5', '#F7E1E1'][k % 6]} stroke={OL} strokeWidth={5} />
            {Array.from({length: Math.floor(h / 56) - 1}, (_, r) => [0, 1, 2].map((c) => <rect key={r + '-' + c} x={-80 + c * 56} y={-h + 20 + r * 56} width={44} height={38} fill={GLASS} stroke={OL} strokeWidth={2} />))}
            <g transform={`translate(0 ${-h - 50})`}><rect x={-120} y={-36} width={240} height={64} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-2} s={fit(o.city, 220, 28)}>{o.city}</T>
              {o.sub && <T x={0} y={22} s={fit(o.sub, 220, 18)} c="#4A5870">{o.sub}</T>}</g>
          </g>; })}
      </g>}
      {z.balance && t >= (z.balanceAt ?? 0) && <g transform={`translate(${z.balanceX ?? 1500} ${z.balanceY ?? 200}) scale(${pop(t, z.balanceAt ?? 0)})`}><rect x={-300} y={-50} width={600} height={90} rx={18} fill={GREEN} stroke={OL} strokeWidth={5} /><T x={0} y={8} s={fit(z.balance, 560, 34)} c="#FFFFFF">{z.balance}</T></g>}
    </g>;
  },

  /** ASML-style ecosystem: an original machine at the centre of suppliers and fabs */
  lithoweb: (t, z, f) => {
    const w = z.x1 - z.x0, sups: any[] = z.sups || [], fabs: any[] = z.fabs || [], mx = z.mx ?? 960, my = f - 60;
    return <g>
      {sky(z, f, '#DCE7F2', '#F6F9FC', 'lwsky' + Math.round(z.x0))}
      {Array.from({length: Math.ceil(w / 140)}, (_, k) => <path key={'gl' + k} d={`M ${z.x0 + k * 140} ${f - 1000} L ${z.x0 + k * 140} ${f}`} stroke="#E4ECF4" strokeWidth={3} />)}
      {ground(z, f, '#C9D6E3', '#B2C3D5')}
      {sups.map((s, k) => { if (t < (s.at ?? 0)) return null; const sx = s.x ?? 220, sy = s.y ?? (180 + k * 150), u = E.out(win(t, s.at ?? 0, 0.8));
        const d = `M ${sx + 110} ${sy} C ${sx + 300} ${sy} ${mx - 380} ${my - 200} ${mx - 300} ${my - 180}`;
        return <g key={'sp' + k}><path d={d} stroke={OL} strokeWidth={12} fill="none" opacity={u} /><path d={d} stroke={s.color || TEAL} strokeWidth={6} fill="none" strokeDasharray="18 12" strokeDashoffset={-t * 90} opacity={u} />
          <g transform={`translate(${sx} ${sy}) scale(${pop(t, s.at ?? 0)})`}><rect x={-110} y={-36} width={220} height={66} rx={14} fill={s.color || TEAL} stroke={OL} strokeWidth={4} /><T x={0} y={8} s={fit(s.label, 200, 24)} c="#FFFFFF">{s.label}</T></g></g>; })}
      {litho(mx, my, z.ms ?? 1.0, t)}
      {plaque(mx, my - 380, z.machine || 'THE MACHINE', NAVY, 28, '#FFFFFF')}
      {fabs.map((s, k) => { if (t < (s.at ?? 0)) return null; const fx = s.x ?? 1700, fy = s.y ?? (240 + k * 200), u = E.out(win(t, s.at ?? 0, 0.8));
        const d = `M ${mx + 330} ${my - 180} C ${mx + 450} ${my - 200} ${fx - 300} ${fy} ${fx - 130} ${fy}`;
        const v = ((t * 0.4 + k / 3) % 1);
        return <g key={'fb' + k}><path d={d} stroke={OL} strokeWidth={12} fill="none" opacity={u} /><path d={d} stroke={PURPLE} strokeWidth={6} fill="none" opacity={u} />
          {z.coinAt !== undefined && t >= z.coinAt && coin(lerp(fx - 130, mx + 330, v), lerp(fy, my - 180, v) - Math.sin(v * Math.PI) * 60, 0.9, k)}
          <g transform={`translate(${fx} ${fy}) scale(${pop(t, s.at ?? 0)})`}><rect x={-120} y={-60} width={240} height={110} rx={10} fill="#F4F7FA" stroke={OL} strokeWidth={4} />
            <path d="M -120 -60 L -80 -100 L -40 -60 L 0 -100 L 40 -60 L 80 -100 L 120 -60" fill="#E1E8F0" stroke={OL} strokeWidth={4} />
            <rect x={-100} y={-40} width={50} height={36} fill={GLASS} stroke={OL} strokeWidth={2} /><rect x={-30} y={-40} width={50} height={36} fill={GLASS} stroke={OL} strokeWidth={2} /><rect x={40} y={-40} width={50} height={36} fill={GLASS} stroke={OL} strokeWidth={2} />
            <T x={0} y={36} s={fit(s.label, 220, 22)}>{s.label}</T></g></g>; })}
    </g>;
  },

  /** Siemens-style: a factory with a holographic twin; automation crates ship to the world */
  twinfab: (t, z, f) => {
    const w = z.x1 - z.x0, twin = z.twinAt !== undefined ? E.out(win(t, z.twinAt, 1.2)) : 0, ship = z.shipAt;
    const dests: string[] = z.dests || ['FACTORY · ASIA', 'FACTORY · AMERICAS', 'FACTORY · EUROPE', 'FACTORY · AFRICA'];
    return <g>
      {sky(z, f, '#9AD4F2', '#EEF8FD', 'twsky' + Math.round(z.x0))}
      {[0, 1].map((k) => cloud(((k * 1000 + t * 9) % (w + 600)) + z.x0 - 300, 110 + k * 60, 0.8, k))}
      {ground(z, f, '#B7D7A0', '#9CC487')}
      {works(z.fx ?? 340, f, 620, 260, '#E9EEF4', 50)}
      <g transform={`translate(${(z.fx ?? 340) + 160} ${f - 30})`}>{arm(t, 2, 0.6, GOLD)}</g><g transform={`translate(${(z.fx ?? 340) + 440} ${f - 30})`}>{arm(t, 5, 0.6, BLUE)}</g>
      {twin > 0 && <g opacity={twin} transform={`translate(0 ${-40 * (1 - twin)})`}>
        <path d={`M ${(z.fx ?? 340) + 310} ${f - 300} L ${(z.fx ?? 340) + 150} ${f - 470} L ${(z.fx ?? 340) + 470} ${f - 470} Z`} fill={CY} opacity={0.18} />
        <g transform={`translate(${z.fx ?? 340} ${f - 470})`}>
          <path d="M 0 0 L 0 -200 L 80 -240 L 160 -200 L 240 -240 L 320 -200 L 400 -240 L 480 -200 L 620 -200 L 620 0 Z" fill="none" stroke={CY} strokeWidth={5} strokeDasharray="16 10" strokeDashoffset={-t * 50} />
          {[120, 320, 500].map((x, q) => <path key={q} d={`M ${x} 0 L ${x} -60 L ${x + 30 * Math.sin(t * 2 + q)} -130`} stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" />)}
          <T x={310} y={-260} s={28} c={CY} st={OL} sw={5}>DIGITAL TWIN</T></g></g>}
      {ship !== undefined && t >= ship && dests.map((d, k) => { const dx = 1250 + (k % 2) * 380, dy = f - 520 + Math.floor(k / 2) * 300, u = clamp((t - ship - k * 0.5) / 2.2), sx = (z.fx ?? 340) + 620;
        if (t < ship + k * 0.5) return null;
        return <g key={'ds' + k}>
          <path d={`M ${sx} ${f - 120} Q ${(sx + dx) / 2} ${dy - 200} ${dx} ${dy}`} stroke={GOLD} strokeWidth={5} fill="none" strokeDasharray="14 10" opacity={0.8} />
          {u < 1 && <g transform={`translate(${lerp(sx, dx, u)} ${lerp(f - 120, dy, u) - Math.sin(u * Math.PI) * 140})`}><rect x={-46} y={-34} width={92} height={60} rx={6} fill="#D7A86E" stroke={OL} strokeWidth={3.5} /><T x={0} y={4} s={14}>{k % 2 ? 'SOFTWARE' : 'CONTROLS'}</T></g>}
          <g transform={`translate(${dx} ${dy}) scale(${pop(t, ship + k * 0.5 + 2.0)})`}>{works(-120, 60, 240, 110, ['#F1D9B5', '#E2F4EA', '#DDEFFB', '#E8E2F7'][k % 4], 60 + k)}<T x={0} y={100} s={fit(d, 260, 20)}>{d}</T></g></g>; })}
    </g>;
  },

  /** an assembly hall where a generic airliner is joined */
  jetyard: (t, z, f) => {
    const w = z.x1 - z.x0, j = clamp(kf(z.join, t, 0)), sups: any[] = z.sups || [];
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EDF2F7" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'tr' + k} d={`M ${z.x0 + k * 200} ${f - 820} L ${z.x0 + k * 200 + 100} ${f - 760} L ${z.x0 + k * 200 + 200} ${f - 820}`} stroke="#A9B6C6" strokeWidth={8} fill="none" />)}
      <rect x={z.x0} y={f - 760} width={w} height={14} fill="#8D9BB0" stroke={OL} strokeWidth={4} />
      {/* gantry crane */}
      <rect x={z.x0} y={f - 700} width={w} height={20} fill={GOLD} stroke={OL} strokeWidth={4} />
      <g transform={`translate(${960 + 260 * Math.sin(t * 0.4)} ${f - 680})`}><rect x={-40} y={0} width={80} height={40} fill="#4A5A70" stroke={OL} strokeWidth={4} /><path d="M 0 40 L 0 160" stroke={OL} strokeWidth={4} /><path d="M -16 160 L 16 160 L 0 180 Z" fill={OL} /></g>
      {jet(960, f - 320, z.js ?? 1.25, j)}
      {j >= 0.98 && <g transform={`translate(960 ${f - 560}) scale(${pop(t, (z.joinDone ?? 0))})`}>{plaque(0, 0, z.doneText || 'JOINED · TESTED · CERTIFIED', GREEN, 28, '#FFFFFF')}</g>}
      {sups.map((s, k) => { if (t < (s.at ?? 0)) return null; const sx = s.x ?? (200 + k * 400), sy = s.y ?? (f - 40);
        return <g key={'js' + k} transform={`translate(${sx} ${sy}) scale(${pop(t, s.at ?? 0)})`}><rect x={-130} y={-40} width={260} height={64} rx={12} fill={s.color || BLUE} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(s.label, 240, 22)} c="#FFFFFF">{s.label}</T></g>; })}
      {Array.from({length: z.techs ?? 3}, (_, k) => fig(300 + k * 620, f, 0.95, k + 2, t, k % 2 ? 'coat' : 'hat'))}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B8C4D2" /><rect x={z.x0} y={f} width={w} height={14} fill="#9DACBE" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'fl' + k} x={z.x0 + k * 160} y={f + 40} width={80} height={10} fill={GOLD} opacity={0.6} />)}
    </g>;
  },

  /** owning vs operating: a European campus and partner factories abroad */
  ownmap: (t, z, f) => {
    const w = z.x1 - z.x0, A = (k: string) => z[k] !== undefined && t >= z[k], hx = z.hqX ?? 470, fx = z.fX ?? 1450;
    const flow = (d: string, c: string, at: number, label: string, lx: number, ly: number, k: number) => { const u = E.out(win(t, at, 0.9));
      return <g key={'fl' + k}><path d={d} stroke={OL} strokeWidth={14} fill="none" opacity={u} /><path d={d} stroke={c} strokeWidth={8} fill="none" strokeDasharray="22 14" strokeDashoffset={-t * 100} opacity={u} />
        <g transform={`translate(${lx} ${ly}) scale(${pop(t, at + 0.3)})`}><rect x={-120} y={-30} width={240} height={50} rx={12} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(label, 220, 22)} c="#FFFFFF">{label}</T></g></g>; };
    return <g>
      {sky(z, f, '#9AD4F2', '#EEF8FD', 'omsky' + Math.round(z.x0))}
      {[0, 1].map((k) => cloud(((k * 1000 + t * 9) % (w + 600)) + z.x0 - 300, 100 + k * 60, 0.7, k))}
      {/* sea between */}
      <rect x={hx + 300} y={f - 40} width={fx - hx - 560} height={700} fill="#5FA8D8" />
      <rect x={z.x0} y={f - 40} width={hx + 300 - z.x0} height={40} fill="#B7D7A0" /><rect x={fx - 260} y={f - 40} width={z.x1 - fx + 260} height={40} fill="#D9C79E" />
      <rect x={z.x0} y={f} width={hx + 300 - z.x0} height={700} fill="#B7D7A0" /><rect x={fx - 260} y={f} width={z.x1 - fx + 260} height={700} fill="#D9C79E" />
      {/* campus */}
      {lab(hx - 260, f - 40, 220, 330, 7, t, A('glowAt') ? 1 : 0)}
      <g transform={`translate(${hx + 90} ${f - 40})`}><rect x={-80} y={-200} width={160} height={200} rx={12} fill="#B0BEC5" stroke={OL} strokeWidth={5} /><circle cx={0} cy={-100} r={52} fill="#90A4AE" stroke={OL} strokeWidth={4} /><circle cx={0} cy={-100} r={14} fill={GOLD} stroke={OL} strokeWidth={3} /><T x={0} y={-220} s={22}>PATENTS</T></g>
      <g transform={`translate(${hx + 230} ${f - 40})`}><rect x={-60} y={-260} width={120} height={260} rx={8} fill="#E8E2F7" stroke={OL} strokeWidth={5} /><rect x={-40} y={-230} width={80} height={60} fill={GLASS} stroke={OL} strokeWidth={3} /><T x={0} y={-280} s={20}>DECISIONS</T></g>
      {plaque(hx, f + 70, z.hqText || 'COMPANY E · EUROPE', NAVY, 28, '#FFFFFF')}
      {Array.from({length: 3}, (_, k) => fig(hx - 200 + k * 140, f - 40, 0.7, k, t, k === 1 ? 'suit' : 'coat'))}
      {/* partner factories */}
      {[0, 1, 2].map((k) => <g key={'pf' + k} transform={`translate(${fx - 120 + k * 230} ${f - 40 - (k % 2) * 30})`}>{works(-100, 0, 200, 130, ['#E9EEF4', '#F1D9B5', '#E2F4EA'][k], 70 + k)}<g transform="translate(0 -20)">{arm(t, k + 3, 0.35, GOLD)}</g></g>)}
      {plaque(fx + 110, f + 70, z.fText || 'PARTNER FACTORIES · ABROAD', '#7E8DA3', 26, '#FFFFFF')}
      {A('licAt') && flow(`M ${hx + 120} ${f - 420} Q ${(hx + fx) / 2} ${f - 640} ${fx} ${f - 260}`, PURPLE, z.licAt, z.licText || 'KNOW-HOW · LICENCE', (hx + fx) / 2, f - 560, 1)}
      {A('prodAt') && flow(`M ${fx + 200} ${f - 220} Q ${fx + 340} ${f - 420} ${fx + 360} ${f - 560}`, BLUE, z.prodAt, 'PRODUCT → WORLD', fx + 330, f - 610, 2)}
      {A('feeAt') && flow(`M ${fx - 40} ${f - 170} Q ${(hx + fx) / 2} ${f - 120} ${hx + 300} ${f - 150}`, GREEN, z.feeAt, z.feeText || 'STEADY FEE', (hx + fx) / 2 + 40, f - 100, 3)}
      {A('saleAt') && <g>{Array.from({length: 7}, (_, k) => { const u = ((t - z.saleAt) * 0.3 + k / 7) % 1; return coin(lerp(fx + 360, hx + 100, u), f - 700 - Math.sin(u * Math.PI) * 120, 1.0, k); })}
        {plaque((hx + fx) / 2 + 180, f - 770, z.saleText || 'SALES · WHAT\'S LEFT GOES TO THE OWNER', GOLD, 24)}</g>}
      {z.hyp && t >= (z.hypAt ?? 0) && banner(z.hypX ?? 960, z.hypY ?? 70, z.hypText || 'HYPOTHETICAL COMPANY', PURPLE, 26)}
    </g>;
  },

  /** the automation profit experiment: per $100 of sales, before vs after */
  profitlab: (t, z, f) => {
    const w = z.x1 - z.x0, cols: any[] = z.cols || [], sc = z.scale ?? 6, base = f + 20, gap = z.gap ?? 560, cx0 = z.colX ?? 700;
    const hiL = z.hiAt ? pick(z.hiAt, t, z.hiLabel) : z.hiLabel;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f + 700} fill="#EEF3F8" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'pg' + k} d={`M ${z.x0 + k * 120} ${f - 1000} L ${z.x0 + k * 120} ${f + 200}`} stroke="#E1E8F0" strokeWidth={3} />)}
      {banner(z.bannerX ?? 960, 60, 'ILLUSTRATIVE MODEL · MADE-UP NUMBERS · PER $100 OF SALES', PURPLE, 24)}
      <g transform={`translate(${cx0 - 220} 0)`}>{[0, 20, 40, 60, 80, 100].map((v) => <g key={v}><path d={`M 0 ${base - v * sc} L 24 ${base - v * sc}`} stroke={OL} strokeWidth={3} /><T x={-8} y={base - v * sc + 7} s={18} a="end" c="#4A5870">{`$${v}`}</T></g>)}
        <path d={`M 12 ${base} L 12 ${base - 100 * sc}`} stroke={OL} strokeWidth={3} /></g>
      {cols.map((c, k) => { if (t < (c.at ?? 0)) return null; const x = cx0 + k * gap, bw = 300; let acc = 0;
        return <g key={'pl' + k} transform={`translate(${x} 0)`}>
          {(c.blocks || []).map((b: any, q: number) => { const bv = kf(b.v, t, 0), h = bv * sc, y = base - acc - h; acc += h; if (bv <= 0.05) return null;
            const sAt = b.at ?? ((c.at ?? 0) + q * 0.25); if (t < sAt) return null; const d = 1 - E.outBack(win(t, sAt, 0.45)), hot = hiL && b.label === hiL;
            return <g key={q} transform={`translate(0 ${-200 * d})`}><rect x={-bw / 2} y={y} width={bw} height={Math.max(2, h - 2)} rx={6} fill={b.color || BLUE} stroke={hot ? GOLD : OL} strokeWidth={hot ? 7 : 3} />
              {h > 22 && <T x={0} y={y + h / 2 + 7} s={Math.min(22, h * 0.55)} c="#FFFFFF" st={OL} sw={4}>{`${b.label} $${Number.isInteger(bv) || Math.abs(bv - Math.round(bv)) < 0.02 ? Math.round(bv) : bv.toFixed(2)}`}</T>}</g>; })}
          <rect x={-170} y={base + 20} width={340} height={70} rx={12} fill={c.color || NAVY} stroke={OL} strokeWidth={4} />
          <T x={0} y={base + 52} s={fit(c.name, 320, 26)} c="#FFFFFF">{c.name}</T>{c.sub && <T x={0} y={base + 80} s={fit(c.sub, 320, 16)} c="#FFFFFF">{c.sub}</T>}
        </g>; })}
      {(z.notes || []).map((n: any, k: number) => t >= n.at ? <g key={'nt' + k} transform={`translate(${n.x ?? 1640} ${n.y ?? (300 + k * 130)}) scale(${pop(t, n.at)})`}>
        <rect x={-200} y={-46} width={400} height={84} rx={16} fill={n.color || '#FFFFFF'} stroke={OL} strokeWidth={4} />
        <T x={0} y={-6} s={fit(n.text, 380, 24)} c={n.color ? '#FFFFFF' : OL}>{n.text}</T>{n.sub && <T x={0} y={24} s={fit(n.sub, 380, 18)} c={n.color ? '#FFFFFF' : '#4A5870'}>{n.sub}</T>}</g> : null)}
    </g>;
  },

  /** a generic continent labelled EUROPE under a giant magnet */
  magnet: (t, z, f) => {
    const w = z.x1 - z.x0, pulls: any[] = z.pulls || [], risks: any[] = z.risks || [], mx = 960, my = f - 330;
    const ICON: Record<string, (k: number) => React.ReactNode> = {
      cash: (k) => coin(0, 0, 1.6, k),
      lab: () => <g><path d="M -14 -30 L -14 -6 L -34 30 L 34 30 L 14 -6 L 14 -30 Z" fill="#DDEFFB" stroke={OL} strokeWidth={4} /><rect x={-24} y={10} width={48} height={18} fill={GREEN} opacity={0.7} /></g>,
      hq: () => <g><rect x={-28} y={-40} width={56} height={70} fill="#E6ECF5" stroke={OL} strokeWidth={4} />{[0, 1, 2].map((r) => <rect key={r} x={-18} y={-32 + r * 20} width={36} height={10} fill={GLASS} />)}</g>,
      people: (k) => <g transform="translate(0 40)">{fig(0, 0, 0.5, k, t, 'suit')}</g>,
      cap: () => <g><path d="M -40 -6 L 0 -26 L 40 -6 L 0 14 Z" fill={NAVY} stroke={OL} strokeWidth={4} /><path d="M 30 -2 L 30 22" stroke={GOLD} strokeWidth={4} /></g>,
    };
    return <g>
      {sky(z, f, '#DCE7F2', '#F6F9FC', 'mgsky' + Math.round(z.x0))}
      <rect x={z.x0} y={f - 200} width={w} height={900} fill="#7DB8E0" />
      {/* generic continent (not a real coastline) */}
      <path d={`M ${mx - 420} ${f - 60} Q ${mx - 470} ${f - 180} ${mx - 360} ${f - 230} Q ${mx - 260} ${f - 330} ${mx - 120} ${f - 270} Q ${mx - 20} ${f - 360} ${mx + 120} ${f - 290} Q ${mx + 280} ${f - 330} ${mx + 360} ${f - 220} Q ${mx + 460} ${f - 140} ${mx + 400} ${f - 60} Z`}
        fill="#B7D7A0" stroke={OL} strokeWidth={6} />
      <T x={mx} y={f - 150} s={56} c={OL} ls={8}>EUROPE</T>
      {/* magnet */}
      <g transform={`translate(${mx} ${my - 300 + 10 * Math.sin(t * 2)})`}>
        <path d="M -180 0 L -180 -120 A 180 180 0 0 1 180 -120 L 180 0 L 100 0 L 100 -120 A 100 100 0 0 0 -100 -120 L -100 0 Z" fill={RED} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <rect x={-180} y={-10} width={80} height={60} fill="#D7DEE8" stroke={OL} strokeWidth={5} /><rect x={100} y={-10} width={80} height={60} fill="#D7DEE8" stroke={OL} strokeWidth={5} />
        {[0, 1, 2].map((q) => <path key={q} d={`M ${-140} ${70 + q * 26} Q 0 ${110 + q * 40} 140 ${70 + q * 26}`} stroke={GOLD} strokeWidth={4} fill="none" opacity={0.5 + 0.5 * Math.sin(t * 6 - q)} />)}
      </g>
      {pulls.map((p, k) => { if (t < (p.at ?? 0)) return null; const sx = k % 2 ? 1840 : 80, sy = 180 + (k % 3) * 220, u = E.inOut(win(t, p.at ?? 0, 2.4)), ex = mx - 300 + (k % 5) * 150, ey = f - 400;
        return <g key={'pl' + k} transform={`translate(${lerp(sx, ex, u)} ${lerp(sy, ey, u)}) scale(${pop(t, p.at ?? 0)})`}>
          <circle r={56} fill="#FFFFFF" stroke={OL} strokeWidth={4} />{(ICON[p.icon] || ICON.cash)(k)}
          <g transform="translate(0 86)"><rect x={-110} y={-24} width={220} height={40} rx={10} fill={NAVY} stroke={OL} strokeWidth={3} /><T x={0} y={4} s={fit(p.label, 200, 20)} c="#FFFFFF">{p.label}</T></g></g>; })}
      {risks.map((r, k) => t >= (r.at ?? 0) ? <g key={'rk' + k} transform={`translate(${r.x ?? (300 + k * 440)} ${r.y ?? 150}) rotate(${-4 + 3 * Math.sin(t * 2 + k)}) scale(${pop(t, r.at ?? 0)})`}>
        <path d="M 0 -70 L 70 50 L -70 50 Z" fill={GOLD} stroke={OL} strokeWidth={5} strokeLinejoin="round" /><T x={0} y={36} s={56}>!</T>
        <rect x={-150} y={64} width={300} height={50} rx={12} fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={98} s={fit(r.label, 280, 24)} c="#FFFFFF">{r.label}</T></g> : null)}
    </g>;
  },

  /** energy-rich location: dam, wind and solar power an automated plant; a power-bill column stacks `bill` blocks */
  cleanpower: (t, z, f) => {
    const w = z.x1 - z.x0, bill: any[] = z.bill || [], fac: any[] = z.factors || [], bx = z.billX ?? 1640, sc = z.billScale ?? 5;
    let acc = 0;
    return <g>
      {sky(z, f, '#8FD3F4', '#EEF9FF', 'cpsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 800 + t * 10) % (w + 600)) + z.x0 - 300, 120 + (k % 2) * 60, 0.8, k))}
      <path d={`M ${z.x0} ${f - 260} Q ${z.x0 + 500} ${f - 420} 700 ${f - 280} T 1500 ${f - 300} L ${z.x1} ${f - 260} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#8CC48A" />
      {/* hydro dam with falling water */}
      <path d={`M 40 ${f} L 90 ${f - 330} L 330 ${f - 330} L 380 ${f} Z`} fill="#C9CFD8" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={z.x0} y={f - 330} width={90 - z.x0} height={330} fill="#5FA8D8" />
      {[0, 1, 2].map((q) => <path key={q} d={`M ${150 + q * 60} ${f - 250} L ${150 + q * 60} ${f}`} stroke="#DDF1FF" strokeWidth={14} strokeDasharray="30 20" strokeDashoffset={-t * 160} />)}
      {[0, 1].map((k) => turbine(480 + k * 150, f, 0.85, t, k))}
      {[0, 1, 2].map((k) => <g key={'sl' + k} transform={`translate(${380 + k * 110} ${f - 20}) skewX(-20)`}><rect x={0} y={-50} width={90} height={50} fill="#2A4F8F" stroke={OL} strokeWidth={3} /><path d="M 30 -50 L 30 0 M 60 -50 L 60 0 M 0 -25 L 90 -25" stroke="#8FB8F0" strokeWidth={2} /></g>)}
      {/* power line to the plant */}
      <path d={`M 340 ${f - 330} Q 620 ${f - 420} 900 ${f - 300}`} stroke={OL} strokeWidth={4} fill="none" />
      {Array.from({length: 5}, (_, k) => { const u = ((t * 0.6 + k / 5) % 1); return <circle key={'el' + k} cx={lerp(340, 900, u)} cy={f - 330 - Math.sin(u * Math.PI) * 70 + u * 30} r={8} fill={GOLD} stroke={OL} strokeWidth={2} />; })}
      {works(860, f, 520, 230, '#E9EEF4', 80)}
      <g transform={`translate(1000 ${f - 30})`}>{arm(t, 1, 0.55, GOLD)}</g><g transform={`translate(1220 ${f - 30})`}>{arm(t, 4, 0.55, BLUE)}</g>
      {z.plantText && plaque(1120, f + 70, z.plantText, NAVY, 24, '#FFFFFF')}
      {ground(z, f, '#8CC48A', '#76AE74')}
      {/* bill column */}
      {bill.length > 0 && <g><rect x={bx - 140} y={f - 40} width={280} height={30} rx={6} fill="#8D9BB0" stroke={OL} strokeWidth={4} />
        {bill.map((b, k) => { if (t < (b.at ?? 0)) return null; const h = b.v * sc * E.out(win(t, b.at ?? 0, 0.6)), y = f - 40 - acc - h; acc += h;
          return <g key={'bl' + k}><rect x={bx - 110} y={y} width={220} height={Math.max(2, h - 2)} rx={6} fill={b.color || BLUE} stroke={OL} strokeWidth={3} />
            {h > 26 && <T x={bx} y={y + h / 2 + 8} s={Math.min(22, h * 0.5)} c="#FFFFFF" st={OL} sw={4}>{b.label}</T>}</g>; })}
        {plaque(bx, f + 60, z.billText || 'A FACTORY POWER BILL', GOLD, 22)}</g>}
      {fac.map((o, k) => t >= (o.at ?? 0) ? <g key={'fc' + k} transform={`translate(${(z.facX ?? 260) + k * (z.facGap ?? 300)} ${z.facY ?? 90}) scale(${pop(t, o.at ?? 0)})`}>
        <rect x={-130} y={-30} width={260} height={52} rx={26} fill={o.color || '#FFFFFF'} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={fit(o.label, 240, 24)}>{o.label}</T></g> : null)}
    </g>;
  },

  /** show title card: a drafting pen writes the title over a skyline */
  eutitle: (t, z, f) => {
    const lines: string[] = z.lines || ['EUROPE', 'BACK TO POWER?'], sub = pick(z.subs, t, z.sub || '');
    const n0 = lines.map((ln, k) => Math.floor(clamp((t - 0.3 - k * 0.8) / 0.6) * ln.length));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#10264A" />
      {Array.from({length: 20}, (_, k) => <path key={'gr' + k} d={`M ${-100 + k * 110} -100 L ${-100 + k * 110} 1200`} stroke="#1A3560" strokeWidth={3} />)}
      {Array.from({length: 12}, (_, k) => <path key={'gh' + k} d={`M -100 ${k * 100} L 2100 ${k * 100}`} stroke="#1A3560" strokeWidth={3} />)}
      {/* skyline silhouette: old works -> spires -> labs -> turbines */}
      <g opacity={0.9}>{works(-40, 1080, 420, 160, '#24406E', 90, 2, 0.4, t)}
        {[0, 1, 2, 3].map((k) => <path key={'sp' + k} d={`M ${480 + k * 90} 1080 L ${480 + k * 90} ${920 - (k % 2) * 60} L ${520 + k * 90} ${860 - (k % 2) * 80} L ${560 + k * 90} ${920 - (k % 2) * 60} L ${560 + k * 90} 1080 Z`} fill="#24406E" stroke="#3A5C94" strokeWidth={3} />)}
        <rect x={900} y={800} width={160} height={280} fill="#24406E" stroke="#3A5C94" strokeWidth={3} /><rect x={1080} y={860} width={200} height={220} fill="#24406E" stroke="#3A5C94" strokeWidth={3} />
        {[0, 1, 2].map((k) => <g key={'tt' + k} opacity={0.8}>{turbine(1420 + k * 170, 1080, 0.8, t, k)}</g>)}</g>
      {lines.map((ln, k) => <T key={k} x={960} y={360 + k * 160} s={fit(ln, 1500, 150)} c={k === lines.length - 1 ? GOLD : '#FFFFFF'} st={OL} sw={14}>{ln.slice(0, n0[k])}</T>)}
      {(() => { const k = Math.min(lines.length - 1, Math.max(0, Math.floor((t - 0.3) / 0.8))), frac = clamp((t - 0.3 - k * 0.8) / 0.6), L = lines[k].length * fit(lines[k], 1500, 150) * 0.6;
        const px = 960 - L / 2 + L * frac, py = 360 + k * 160 + 10; return t < 0.3 + lines.length * 0.8 ? <g transform={`translate(${px} ${py}) rotate(30)`}>
          <path d="M 0 0 L -14 -40 L -14 -200 L 14 -200 L 14 -40 Z" fill={GOLD} stroke={OL} strokeWidth={5} strokeLinejoin="round" /><rect x={-14} y={-220} width={28} height={30} fill="#D7DEE8" stroke={OL} strokeWidth={4} /></g> : null; })()}
      {sub && <g transform="translate(960 720)"><rect x={-640} y={-40} width={1280} height={64} rx={32} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={4} s={fit(sub, 1220, 32)}>{sub}</T></g>}
      <T x={960} y={150} s={34} c={GOLD} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** act bumper: a map-fold wipe, a compass badge with the act number */
  eubumper: (t, z, f) => {
    const c = z.color || BLUE, wipe = E.inOut(win(t, 0, 0.6));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#F4F7FB" />
      {[0, 1, 2, 3, 4, 5].map((k) => <rect key={'fold' + k} x={-200 + k * 400} y={-200} width={400} height={1500 * wipe} fill={k % 2 ? c : c} opacity={k % 2 ? 0.92 : 1} />)}
      {Array.from({length: 10}, (_, k) => <path key={'ct' + k} d={`M -100 ${100 + k * 100} Q 500 ${60 + k * 100 + 40 * Math.sin(k)} 960 ${100 + k * 100} T 2100 ${100 + k * 100}`} stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.18 * wipe} />)}
      <g transform={`translate(560 470) scale(${pop(t, 0.8, 0.5)}) rotate(${-6 + 2 * Math.sin(t * 3)})`}>
        <circle r={160} fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        {[0, 90, 180, 270].map((r) => <path key={r} transform={`rotate(${r + t * 8})`} d="M 0 -150 L 14 -120 L -14 -120 Z" fill={c} stroke={OL} strokeWidth={3} />)}
        <T x={0} y={-44} s={30} c={OL}>{z.act || 'ACT ONE'}</T><T x={0} y={80} s={130} c={c} st={OL} sw={8}>{z.num || '1'}</T></g>
      <g transform={`translate(1240 ${470 - 20 * pop(t, 1.1)})`}><rect x={-560} y={-90} width={1120} height={130} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={0} y={0} s={fit(z.title || '', 1060, 56)} c="#FFFFFF">{z.title || ''}</T></g>
      {t >= 1.5 && <T x={1240} y={640} s={fit(z.caption || '', 1100, 34)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.5) / 0.3)}>{z.caption || ''}</T>}
    </g>;
  },
};

/** epitag: FACT / MECHANISM / SCENARIO / CONJECTURE pill (top-left) */
const TAGC: Record<string, string> = {FACT: GREEN, MECHANISM: BLUE, SCENARIO: PURPLE, CONJECTURE: '#E07A2F', HYPOTHESIS: PURPLE, ILLUSTRATIVE: PURPLE};
const epitag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const txt: string = pick(a.tags, t, a.text || 'FACT'); if (!txt) return null;
  const key = txt.split(' ')[0], c = TAGC[key] || NAVY, w = txt.length * 17 + 70, x = kf(a.x, t, 40), y = kf(a.y, t, 40);
  return <g key={'et' + i} transform={`translate(${x} ${y}) scale(${pop(t, at, 0.35)})`}>
    <rect x={0} y={0} width={w} height={46} rx={23} fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={26} cy={23} r={9} fill="#FFFFFF" /><T x={44} y={32} s={24} a="start" c="#FFFFFF">{txt}</T></g>;
};

/** compasspen: the drafting-pen mascot that draws an underline */
const compasspen: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 200), s = (a.scale ?? 1) * pop(t, at, 0.4), d = a.drawAt !== undefined ? clamp((t - a.drawAt) / 0.8) : 0, L = a.len ?? 300;
  return <g key={'cp' + i}>
    {d > 0 && <path d={`M ${x - L / 2} ${y + 30} L ${x - L / 2 + L * d} ${y + 30}`} stroke={a.color || GOLD} strokeWidth={10} strokeLinecap="round" />}
    <g transform={`translate(${a.drawAt !== undefined && d < 1 ? x - L / 2 + L * d : x} ${y}) scale(${s}) rotate(${20 + 6 * Math.sin(t * 3)})`}>
      <path d="M 0 30 L -16 -10 L -16 -170 L 16 -170 L 16 -10 Z" fill={GOLD} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-16} y={-200} width={32} height={34} fill="#D7DEE8" stroke={OL} strokeWidth={4} />
      <circle cx={-5} cy={-110} r={5} fill={OL} /><circle cx={7} cy={-110} r={5} fill={OL} /><path d="M -6 -92 Q 1 -86 8 -92" stroke={OL} strokeWidth={3} fill="none" /></g></g>;
};

export const EUROPE_ITEMS: Record<string, ItemFn> = {epitag, compasspen};
export const EUROPE_INDOOR = ['smartfab', 'profitlab', 'eutitle', 'eubumper', 'jetyard'];
