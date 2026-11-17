import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * CARS kit for CartoonStage (Episode 61, "Why Are Chinese Cars So Cheap — And So Advanced?").
 *
 * Premium business-documentary look with cartoon energy (house style of Ep 56), bright day scenes. Every car is a GENERIC,
 * ORIGINAL design (rounded hatch, low sedan, boxy SUV): no real car shape traced, no logos, badges or grilles of any brand.
 * Companies and models are named only in text labels. Neutral toward China, the US and the EU: no flags, no stereotypes.
 * Sets:
 *  - evshow: a glass EV showroom; turntable car, a big dashboard wall, laser-scanner cone (`scanAt`), 5-minute charge bar
 *    (`chargeAt`), flip price board (`price`, `priceSub`, `priceAt`), optional grey rival car with its own price (`rivalAt`...)
 *  - costlab: the exploded $25,000 car: the car splits and slices fly into a stacked column (`slices` [[t,label,value,color,sub]],
 *    `total`, `explodeAt`, `note`); the column fills bottom-up
 *  - gigaline: car assembly hall: primer-white bodies ride the line, robot arms weld, battery packs rise into the car (`marryX`)
 *  - cellplant: battery plant: long flat "blade" cells slide into a pack tray (`fill` keyframes 0..1); chemistry jars LFP / NMC
 *    (`jarsAt`) with price tags (`tagsAt`, `lfp`, `nmc`)
 *  - chainvalley: battery supply chain landscape MINE → REFINE → POWDERS → CELLS → PACK → CAR; tokens travel on a belt; share
 *    meters pop above stations (`shades` [[t, idx, pct(0..1), label]]); `lit` keyframes of the active station
 *  - cashworks: the CASH BURN MACHINE: a revenue funnel pours coins down a plumbing column through REVENUE → GROSS → OPERATING
 *    → OPERATING CASH → FREE CASH tanks; side drains for costs/capex; `stages` [[t, idx]] reveal; `levels` {k: keyframes};
 *    `negAt` turns the last tank red (below zero); `labels` override
 *  - pricestreet: a row of dealerships with flip price boards that step down (`cuts` [[t, k, text]]), a big MARGIN gauge
 *    (`margin` keyframes 0..1), falling arrows
 *  - carport: ro-ro port: cars drive up the ramp into a car carrier, a lot that fills (`lot` keyframes 0..1), `board`
 *  - tariffgate: the road abroad splits at two gates: a tall wall labelled `usText` (rises at `wallAt`) and a toll gate with a
 *    duty board `euLines` (at `euAt`) and an optional MINIMUM PRICE sign (`minAt`)
 *  - c61title / c61bumper: show title card and act bumpers (screen-filling, static camera)
 * Items: evcar (driving generic car; `kind` hatch|sedan|suv, `color`, `tag`, `cut`), suspects (a four-card lineup board with
 * verdict stamps), cellbot (VOLTY, a battery-cell mascot whose price tag keeps dropping: the running gag), coinrain.
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#10213A';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; flip?: boolean; [k: string]: any};
type SetFn = (t: number, z: Z, f: number) => React.ReactNode;
type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const kf = (v: KF | undefined, t: number, d = 0): number => {
  if (v === undefined) return d;
  if (!Array.isArray(v)) return Number(v);
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], v[i][0] - v[i - 1][0])));
  return v[v.length - 1][1];
};
const pick = <V,>(tl: any, t: number, d: V): V => { let v = d; if (Array.isArray(tl)) for (const [pt, pv] of tl) if (t >= Number(pt)) v = pv; return v; };
const jig = (t: number, at: number, k = 14, d = 5) => (t < at ? 0 : Math.exp(-d * (t - at)) * Math.sin(k * (t - at)));
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.62);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const NAVY = '#13223A', GOLD = '#FFB627', BLUE = '#1E88E5', TEAL = '#1F9E9A', RED = '#E5484D', GREEN = '#2E9E5B', CREAM = '#FFF8E6', STEEL = '#90A4AE', SKY = '#DCEEFF';
const CARC = ['#E5484D', '#1E88E5', '#FFB627', '#2E9E5B', '#ECEFF1', '#7E57C2', '#26C6DA', '#FF7043', '#37474F'];

/* ============================================================================================ THE GENERIC CAR */
/** An ORIGINAL generic car drawn at its ground point (0,0), ~420 long at s=1. kind: hatch | sedan | suv. No badge, no grille
 *  pattern of any brand. spin = wheel angle (deg). screen: a glowing dashboard visible through the side window. */
export const carShape = (kind: string, color: string, spin = 0, opt: {lights?: boolean; screen?: number; primer?: boolean; lidar?: boolean; t?: number} = {}) => {
  const body = opt.primer ? '#E9EEF2' : color;
  const P: Record<string, {d: string; w1: string; w2: string; wx: [number, number]; r: number}> = {
    hatch: {d: 'M -205 -34 Q -210 -78 -176 -88 L -118 -98 Q -64 -152 18 -156 Q 96 -154 136 -102 L 182 -90 Q 210 -82 208 -40 L 206 -22 Q 204 -10 190 -10 L -192 -10 Q -206 -10 -205 -22 Z',
      w1: 'M -100 -100 Q -54 -142 10 -146 L 10 -100 Z', w2: 'M 26 -146 Q 88 -142 120 -100 L 26 -100 Z', wx: [-122, 124], r: 36},
    sedan: {d: 'M -240 -30 Q -244 -66 -212 -74 L -140 -84 Q -82 -140 4 -142 Q 92 -140 136 -88 L 214 -78 Q 244 -72 242 -36 L 240 -20 Q 238 -10 224 -10 L -226 -10 Q -240 -10 -240 -20 Z',
      w1: 'M -124 -86 Q -76 -128 -6 -132 L -6 -86 Z', w2: 'M 10 -132 Q 82 -128 120 -86 L 10 -86 Z', wx: [-150, 150], r: 34},
    suv: {d: 'M -218 -36 Q -222 -96 -190 -110 L -150 -116 Q -120 -172 -40 -178 L 120 -178 Q 168 -176 182 -120 L 200 -108 Q 222 -100 220 -44 L 218 -22 Q 216 -10 202 -10 L -204 -10 Q -218 -10 -218 -22 Z',
      w1: 'M -138 -118 Q -112 -164 -46 -168 L -10 -168 L -10 -118 Z', w2: 'M 6 -168 L 118 -168 Q 156 -166 166 -118 L 6 -118 Z', wx: [-132, 134], r: 40},
  };
  const p = P[kind] || P.hatch, sc = opt.screen ?? 0, tt = opt.t ?? 0;
  return <g>
    <ellipse cx={0} cy={2} rx={kind === 'sedan' ? 250 : 220} ry={14} fill={OL} opacity={0.2} />
    <path d={p.d} fill={body} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    {/* lower body shade + crease */}
    <path d={`M ${p.wx[0] - 80} -30 L ${p.wx[1] + 80} -30 L ${p.wx[1] + 76} -14 L ${p.wx[0] - 76} -14 Z`} fill={OL} opacity={0.14} />
    <path d={`M ${p.wx[0] - 70} -54 L ${p.wx[1] + 70} -54`} stroke="#FFFFFF" strokeWidth={4} opacity={0.35} />
    <path d={p.w1} fill={sc > 0 ? '#1B3A5C' : '#BFE3FF'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    <path d={p.w2} fill={sc > 0 ? '#1B3A5C' : '#BFE3FF'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    {sc > 0 && <g opacity={sc}><path d={`M -60 ${kind === 'suv' ? -122 : -104} L 70 ${kind === 'suv' ? -122 : -104}`} stroke="#4FC3F7" strokeWidth={5} strokeLinecap="round" opacity={0.9} />
      <rect x={-8} y={kind === 'suv' ? -138 : -118} width={40} height={12} rx={3} fill="#4FC3F7" opacity={0.55 + 0.25 * Math.sin(tt * 2)} /></g>}
    <path d={`M ${kind === 'suv' ? -14 : 12} ${kind === 'suv' ? -118 : -100} L ${kind === 'suv' ? -14 : 12} -24`} stroke={OL} strokeWidth={3} opacity={0.5} />
    {/* door handle, slim light bars (no grille) */}
    <rect x={kind === 'suv' ? 20 : 36} y={kind === 'suv' ? -96 : -84} width={26} height={6} rx={3} fill={OL} opacity={0.55} />
    <rect x={p.wx[1] + 36} y={kind === 'suv' ? -92 : -78} width={44} height={9} rx={4} fill={opt.lights ? '#FFF3B0' : '#FFFFFF'} stroke={OL} strokeWidth={3} />
    <rect x={p.wx[0] - 82} y={kind === 'suv' ? -92 : -74} width={40} height={9} rx={4} fill="#FF5A5F" stroke={OL} strokeWidth={3} />
    {opt.lights && <path d={`M ${p.wx[1] + 82} -74 L ${p.wx[1] + 260} -110 L ${p.wx[1] + 260} -30 Z`} fill="#FFF3B0" opacity={0.25} />}
    {opt.lidar && <g transform={`translate(${kind === 'suv' ? 40 : 14} ${kind === 'suv' ? -184 : -160})`}><rect x={-22} y={-14} width={44} height={16} rx={7} fill="#263238" stroke={OL} strokeWidth={3} /><circle cx={0} cy={-6} r={4} fill="#80DEEA" opacity={0.6 + 0.4 * Math.sin(tt * 9)} /></g>}
    {p.wx.map((wx, k) => <g key={k} transform={`translate(${wx} -12)`}>
      <circle r={p.r} fill="#263238" stroke={OL} strokeWidth={5} />
      <circle r={p.r * 0.55} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
      <g transform={`rotate(${spin})`}>{[0, 72, 144, 216, 288].map((a) => <path key={a} d={`M 0 0 L 0 ${-p.r * 0.5}`} stroke={OL} strokeWidth={4} transform={`rotate(${a})`} />)}</g>
      <circle r={5} fill={OL} /></g>)}
  </g>;
};

/** a flip-card price board (text pops in with a flip at `at`) */
const priceBoard = (t: number, x: number, y: number, txt: string, sub: string, at: number, w = 520, col = GOLD) => {
  const u = clamp((t - at) / 0.45), flip = Math.cos(u * Math.PI);
  return <g transform={`translate(${x} ${y})`}>
    <rect x={-w / 2} y={-80} width={w} height={150} rx={18} fill={NAVY} stroke={OL} strokeWidth={6} />
    <g transform={`scale(1 ${Math.abs(flip) < 0.05 ? 0.05 : Math.abs(flip)})`}>
      <T x={0} y={24} s={fit(u < 0.5 ? '$ - - , - - -' : txt, w - 40, 86)} c={u < 0.5 ? '#5C6B80' : col}>{u < 0.5 ? '$ - - , - - -' : txt}</T></g>
    {sub && t > at + 0.3 && <T x={0} y={58} s={fit(sub, w - 30, 20)} c="#CFD8E3" w={700}>{sub}</T>}
  </g>;
};

/* ============================================================================================ SETS */
export const CARS_SETS: Record<string, SetFn> = {
  /** EV SHOWROOM (glass, daylight) */
  evshow: (t, z, f) => {
    const w = z.x1 - z.x0, cx = z.carX ?? 900, col = z.carColor || '#26C6DA', kind = z.carKind || 'hatch';
    const scan = z.scanAt !== undefined ? win(t, z.scanAt, 0.6) : 0, ch = z.chargeAt !== undefined ? clamp((t - z.chargeAt) / 2.2) : -1;
    const turn = Math.sin(t * 0.6) * 0.04;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EAF2FA" />
      {/* glass facade with mullions and daylight */}
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const x = z.x0 + k * 260; return <g key={'gl' + k}>
        <rect x={x} y={f - 760} width={260} height={560} fill="#CFE8FF" stroke="#7FA6C9" strokeWidth={6} />
        <path d={`M ${x + 30} ${f - 740} L ${x + 120} ${f - 740} L ${x + 40} ${f - 220} Z`} fill="#FFFFFF" opacity={0.35} />
        <path d={`M ${x} ${f - 200} L ${x + 300} ${f}`} stroke="#FFFFFF" strokeWidth={1} opacity={0.2} /></g>; })}
      <rect x={z.x0} y={f - 800} width={w} height={44} fill="#2B3E5C" />
      {/* dashboard wall: a giant screen with live UI */}
      <g transform={`translate(${z.wallX ?? 1500} ${f - 520})`}>
        <rect x={-300} y={-170} width={600} height={300} rx={22} fill="#0D1B2E" stroke={OL} strokeWidth={8} />
        <circle cx={-170} cy={-20} r={86} fill="none" stroke="#1E88E5" strokeWidth={14} opacity={0.35} />
        <path d={`M -170 -20 m -86 0 a 86 86 0 0 1 ${86 + 86 * Math.cos(Math.PI * (1 - 0.6 - 0.25 * Math.sin(t)))} ${-86 * Math.sin(Math.PI * (1 - 0.6 - 0.25 * Math.sin(t)))}`} fill="none" stroke="#4FC3F7" strokeWidth={14} strokeLinecap="round" />
        <T x={-170} y={2} s={46} c="#FFFFFF">{Math.round(60 + 20 * Math.sin(t))}</T><T x={-170} y={34} s={16} c="#80DEEA" w={700}>KM/H</T>
        {[0, 1, 2, 3, 4].map((q) => <rect key={q} x={-40 + q * 62} y={60 - 120 * (0.3 + 0.7 * Math.abs(Math.sin(t * 1.4 + q)))} width={42} height={120 * (0.3 + 0.7 * Math.abs(Math.sin(t * 1.4 + q)))} rx={6} fill={q % 2 ? '#4FC3F7' : '#FFB627'} opacity={0.85} />)}
        <path d="M -40 -120 L 260 -120" stroke="#1E88E5" strokeWidth={4} /><T x={110} y={-134} s={18} c="#80DEEA" w={700}>DRIVER ASSIST · NAV · MEDIA</T></g>
      {/* reflective floor */}
      <rect x={z.x0} y={f} width={w} height={600} fill="#D5DEE8" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 200} ${f} L ${z.x0 + k * 200 - 120} ${f + 600}`} stroke="#FFFFFF" strokeWidth={3} opacity={0.5} />)}
      {/* spotlights */}
      {[-260, 0, 260].map((q, k) => <g key={'sp' + k}><path d={`M ${cx + q} ${f - 780} L ${cx + q - 160} ${f} L ${cx + q + 160} ${f} Z`} fill="#FFF6D8" opacity={0.18 + 0.04 * Math.sin(t * 2 + k)} />
        <rect x={cx + q - 20} y={f - 800} width={40} height={30} rx={6} fill="#37474F" /></g>)}
      {/* turntable + hero car */}
      <ellipse cx={cx} cy={f + 10} rx={330} ry={42} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
      <ellipse cx={cx} cy={f + 4} rx={300} ry={32} fill="#ECEFF1" stroke={OL} strokeWidth={3} strokeDasharray={`${20 + 10 * Math.sin(t * 2)} 16`} />
      <g transform={`translate(${cx} ${f}) scale(${1.15 * (1 + turn)} 1.15)`}>{carShape(kind, col, t * 0, {lights: true, screen: z.screenAt !== undefined ? win(t, z.screenAt, 0.4) : 1, lidar: !!z.lidar, t})}</g>
      {/* laser scanner cone */}
      {scan > 0 && <g opacity={scan}>{[0, 1, 2].map((q) => { const a = (t * 1.6 + q * 0.7) % 2.1; return <path key={q} d={`M ${cx + 16} ${f - 196} L ${cx + 16 + 900 * Math.cos(-0.25 + a * 0.24)} ${f - 196 + 260 * Math.sin(-0.25 + a * 0.24)}`} stroke="#4FC3F7" strokeWidth={3} opacity={0.7 - a * 0.25} />; })}
        <path d={`M ${cx + 16} ${f - 196} L ${cx + 900} ${f - 300} L ${cx + 900} ${f - 60} Z`} fill="#4FC3F7" opacity={0.12} />
        {Array.from({length: 18}, (_, q) => <circle key={'pt' + q} cx={cx + 300 + rnd(q) * 600} cy={f - 260 + rnd(q + 9) * 220} r={4} fill="#4FC3F7" opacity={0.5 + 0.5 * Math.sin(t * 5 + q)} />)}</g>}
      {/* charge bar 10% → 70% in "5 minutes" */}
      {ch >= 0 && <g transform={`translate(${cx} ${f - 380}) scale(${pop(t, z.chargeAt, 0.4)})`}>
        <rect x={-210} y={-40} width={420} height={80} rx={18} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><rect x={210} y={-16} width={16} height={32} rx={4} fill={OL} />
        <rect x={-198} y={-28} width={396 * (0.1 + 0.6 * E.inOut(ch))} height={56} rx={10} fill={GREEN} />
        <T x={0} y={14} s={36}>{`${Math.round(10 + 60 * E.inOut(ch))}%`}</T>
        <T x={0} y={-56} s={22} c={NAVY} w={800}>{z.chargeText || '10% → 70% IN ~5 MIN (MAKER CLAIM)'}</T></g>}
      {z.price && t >= (z.priceAt ?? 0) - 0.2 && priceBoard(t, z.priceX ?? cx, f - 650, z.price, z.priceSub || '', z.priceAt ?? 0, 560)}
      {/* rival: a grey generic sedan with its own price */}
      {z.rivalAt !== undefined && t >= z.rivalAt && <g>
        <g transform={`translate(${kf(z.rivalX, t, cx + 760)} ${f}) scale(1.05)`}>{carShape('sedan', '#78909C', 0, {t})}</g>
        {priceBoard(t, kf(z.rivalX, t, cx + 760), f - 300, z.rivalPrice || '$56,220', z.rivalSub || '', z.rivalAt + 0.2, 460, '#FFFFFF')}</g>}
    </g>;
  },

  /** THE EXPLODED $25,000 CAR (white lab, blueprint grid) */
  costlab: (t, z, f) => {
    const w = z.x1 - z.x0, carX = z.carX ?? 470, colX = z.colX ?? 1080, total = z.total ?? 25000, H = z.colH ?? 640, base = f + 40;
    const slices: [number, string, number, string, string][] = (z.slices || []).map((s: any) => [Number(s[0]), String(s[1]), Number(s[2]), String(s[3] || GOLD), String(s[4] || '')]);
    const ex = z.explodeAt !== undefined ? E.inOut(win(t, z.explodeAt, 1.0)) : 0;
    let acc = 0;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f + 600} fill="#F4F8FC" />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <path key={'gx' + k} d={`M ${z.x0 + k * 60} -400 L ${z.x0 + k * 60} ${f + 600}`} stroke="#D6E4F2" strokeWidth={k % 5 ? 1 : 2} />)}
      {Array.from({length: 30}, (_, k) => <path key={'gy' + k} d={`M ${z.x0} ${-400 + k * 60} L ${z.x1} ${-400 + k * 60}`} stroke="#D6E4F2" strokeWidth={k % 5 ? 1 : 2} />)}
      {/* the car, its layers lifting apart when exploded */}
      <g transform={`translate(${carX} ${f - 40}) scale(1.35)`}>
        <g transform={`translate(0 ${-60 * ex})`} opacity={1 - 0.45 * ex}>{carShape(z.carKind || 'hatch', z.carColor || '#1E88E5', t * 40 * (1 - ex), {t, screen: 1})}</g>
        {ex > 0 && <g opacity={ex}>
          <rect x={-150} y={-26 + 20 * ex} width={300} height={22} rx={6} fill={GOLD} stroke={OL} strokeWidth={4} /><T x={0} y={-9 + 20 * ex} s={14}>BATTERY PACK</T>
          <rect x={-150 - 60 * ex} y={-120 - 30 * ex} width={70} height={40} rx={8} fill={BLUE} stroke={OL} strokeWidth={3} /><T x={-115 - 60 * ex} y={-94 - 30 * ex} s={12} c="#FFFFFF">MOTOR</T>
          <rect x={60 + 70 * ex} y={-160 - 50 * ex} width={70} height={40} rx={8} fill="#7E57C2" stroke={OL} strokeWidth={3} /><T x={95 + 70 * ex} y={-134 - 50 * ex} s={12} c="#FFFFFF">CHIPS</T></g>}
      </g>
      {/* the stacked column */}
      <g transform={`translate(${colX} ${base})`}>
        <rect x={-150} y={-H - 10} width={300} height={H + 10} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeDasharray="14 10" />
        <T x={0} y={-H - 34} s={30} c={NAVY}>{z.colTitle || '$25,000 (HYPOTHETICAL)'}</T>
        {slices.map(([at, lab, val, col2, sub], k) => { const h = (val / total) * H, y0 = -acc - h; acc += h; if (t < at) return null;
          const u = E.outBack(win(t, at, 0.5)), fly = 1 - E.out(win(t, at, 0.7));
          return <g key={'sl' + k} transform={`translate(${(carX - colX) * fly} ${-200 * fly})`}>
            <rect x={-146} y={y0} width={292} height={Math.max(4, h * u)} fill={col2} stroke={OL} strokeWidth={4} />
            <g opacity={win(t, at + 0.2, 0.3)}><path d={`M 150 ${y0 + h / 2} L 196 ${y0 + h / 2}`} stroke={OL} strokeWidth={3} />
              <T x={206} y={y0 + h / 2 + 4} s={h > 60 ? 28 : 22} a="start" c={NAVY}>{lab}</T>
              {sub && <T x={206} y={y0 + h / 2 + 30} s={18} a="start" c="#5C6B80" w={700}>{sub}</T>}</g>
            {h > 46 && <T x={0} y={y0 + h / 2 + 10} s={Math.min(30, h * 0.45)} c={col2 === GOLD || col2 === '#FFFFFF' ? NAVY : '#FFFFFF'}>{sub && sub.startsWith('$') ? '' : ''}</T>}
          </g>; })}
      </g>
      {z.note && <g transform={`translate(${colX} ${base + 50})`}><rect x={-330} y={-26} width={660} height={46} rx={23} fill={RED} /><T x={0} y={6} s={fit(z.note, 620, 22)} c="#FFFFFF">{z.note}</T></g>}
    </g>;
  },

  /** CAR ASSEMBLY HALL */
  gigaline: (t, z, f) => {
    const w = z.x1 - z.x0, sp = z.speed ?? 120, mx = z.marryX ?? 1200, ly = f - 120;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E7EDF2" />
      <rect x={z.x0} y={f - 900} width={w} height={80} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const sx = z.x0 + k * 380 + 40; return <g key={'sky' + k}>
        <rect x={sx} y={f - 880} width={260} height={50} rx={6} fill="#D7F0FF" stroke={OL} strokeWidth={4} />
        <path d={`M ${sx} ${f - 830} L ${sx + 260} ${f - 830} L ${sx + 420} ${f} L ${sx + 120} ${f} Z`} fill="#FFF8D6" opacity={0.25} /></g>; })}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'win' + k} x={z.x0 + k * 300 + 40} y={f - 760} width={220} height={110} rx={8} fill="#D6ECF5" stroke={OL} strokeWidth={4} />)}
      <g transform={`translate(${z.boardX ?? 900} ${f - 600})`}><rect x={-320} y={-54} width={640} height={96} rx={14} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={0} y={12} s={fit(z.board || 'LINE 3 · ONE CAR EVERY MINUTE (ILLUSTRATIVE)', 600, 40)} c={GOLD}>{z.board || 'LINE 3 · ONE CAR EVERY MINUTE (ILLUSTRATIVE)'}</T></g>
      <rect x={z.x0} y={f} width={w} height={600} fill="#C9D3DC" />
      {/* line */}
      <rect x={z.x0} y={ly + 30} width={w} height={34} fill="#455A64" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 60)}, (_, q) => <circle key={'r' + q} cx={z.x0 + q * 60 + ((t * sp) % 60)} cy={ly + 47} r={7} fill={STEEL} />)}
      {Array.from({length: Math.ceil(w / 560)}, (_, q) => { const px = z.x0 + (((q * 560 + t * sp) % w) + w) % w, done = px > mx;
        return <g key={'car' + q} transform={`translate(${px} ${ly + 30}) scale(0.9)`}>{carShape(z.kind || 'hatch', CARC[q % CARC.length], 0, {primer: !done, t})}</g>; })}
      {/* the "marriage": a battery pack rises into each car at mx */}
      {(() => { const ph = ((t * sp) % 560) / 560, u = Math.sin(ph * Math.PI); return <g transform={`translate(${mx} ${ly + 120 - 70 * u})`}>
        <rect x={-150} y={-18} width={300} height={30} rx={6} fill={GOLD} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={16}>BATTERY</T>
        <rect x={-20} y={12} width={40} height={140} fill={STEEL} stroke={OL} strokeWidth={4} /></g>; })()}
      {/* robot arms */}
      {(z.arms || [500, 800, 1600, 1900]).map((ax: number, k: number) => { const ph = (t * 0.9 + k * 0.37) % 1, a1 = -30 + 50 * Math.sin(ph * Math.PI * 2), a2 = 70 + 40 * Math.cos(ph * Math.PI * 2);
        const r1 = (a1 * Math.PI) / 180, r2 = ((a1 + a2) * Math.PI) / 180, ex = Math.sin(r1) * 130, ey = -Math.cos(r1) * 130 - 60, hx = ex + Math.sin(r2) * 110, hy = ey + Math.cos(r2) * 110;
        const spark = Math.sin(t * 13 + k * 3) > 0.7;
        return <g key={'arm' + k} transform={`translate(${ax} ${ly + 30})`}>
          <rect x={-50} y={-30} width={100} height={30} rx={8} fill="#546E7A" stroke={OL} strokeWidth={4} /><rect x={-26} y={-70} width={52} height={44} rx={10} fill={k % 2 ? GOLD : '#FF7043'} stroke={OL} strokeWidth={4} />
          <path d={`M 0 -60 L ${ex} ${ey} L ${hx} ${hy}`} stroke={OL} strokeWidth={30} strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <path d={`M 0 -60 L ${ex} ${ey} L ${hx} ${hy}`} stroke={k % 2 ? GOLD : '#FF7043'} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" fill="none" />
          <circle cx={0} cy={-60} r={13} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={ex} cy={ey} r={11} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
          {spark && Array.from({length: 6}, (_, q) => <path key={q} d={`M ${hx} ${hy} l ${Math.cos(q) * 30} ${Math.sin(q) * 30}`} stroke="#FFE082" strokeWidth={4} />)}</g>; })}
    </g>;
  },

  /** BATTERY CELL PLANT: blade cells slide into a pack; chemistry jars */
  cellplant: (t, z, f) => {
    const w = z.x1 - z.x0, fl = clamp(kf(z.fill, t, 1)), px = z.packX ?? 820, n = 14, ja = z.jarsAt, ta = z.tagsAt;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EEF4F7" />
      {Array.from({length: Math.ceil(w / 240)}, (_, k) => <rect key={'pn' + k} x={z.x0 + k * 240 + 20} y={f - 820} width={200} height={600} rx={10} fill="#F8FBFD" stroke="#C5D3DC" strokeWidth={4} />)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#D3DDE4" />
      <rect x={z.x0} y={f - 830} width={w} height={40} fill="#2B3E5C" />
      <g transform={`translate(${z.boardX ?? 1500} ${f - 700})`}><rect x={-260} y={-44} width={520} height={80} rx={12} fill={NAVY} /><T x={0} y={10} s={fit(z.board || 'CELL-TO-PACK', 480, 34)} c={GOLD}>{z.board || 'CELL-TO-PACK'}</T></g>
      {/* pack tray */}
      <g transform={`translate(${px} ${f - 60})`}>
        <rect x={-380} y={-200} width={760} height={200} rx={16} fill="#37474F" stroke={OL} strokeWidth={6} />
        {Array.from({length: n}, (_, k) => { const on = k < Math.round(fl * n), last = k === Math.round(fl * n) - 1, slide = last ? 1 - E.out(clamp((fl * n - k) * 2)) : 0;
          return on ? <g key={k} transform={`translate(${-350 + k * 50} ${-186 - slide * 260})`}><rect x={0} y={0} width={42} height={172} rx={4} fill={k % 2 ? '#64B5F6' : '#42A5F5'} stroke={OL} strokeWidth={3} />
            <rect x={6} y={8} width={30} height={12} rx={2} fill="#FFFFFF" opacity={0.6} /></g> : <rect key={k} x={-350 + k * 50} y={-186} width={42} height={172} rx={4} fill="none" stroke="#78909C" strokeWidth={2} strokeDasharray="6 6" />; })}
        <T x={0} y={40} s={24} c={NAVY}>{z.packText || 'LONG, FLAT CELLS STRAIGHT INTO THE PACK'}</T></g>
      {/* gantry dropping the next cell */}
      <g transform={`translate(${px - 350 + Math.min(n - 1, Math.round(fl * n)) * 50 + 21} ${f - 640})`}><rect x={-60} y={-20} width={120} height={36} rx={6} fill={GOLD} stroke={OL} strokeWidth={4} />
        <path d={`M 0 16 L 0 ${120 + 40 * Math.sin(t * 3)}`} stroke={OL} strokeWidth={5} /></g>
      <rect x={z.x0} y={f - 670} width={w} height={20} fill="#FFC93C" stroke={OL} strokeWidth={4} />
      {/* chemistry jars */}
      {ja !== undefined && t >= ja && [['LFP', '#7BD389', ['Li', 'Fe', 'P']], ['NMC', '#B39DDB', ['Ni', 'Mn', 'Co']]].map(([lab, col2, els]: any, k) => {
        const jx = (z.jarX ?? 1500) + k * 300, u = pop(t, ja + k * 0.25, 0.45);
        return <g key={'jar' + k} transform={`translate(${jx} ${f - 40}) scale(${u})`}>
          <rect x={-110} y={-280} width={220} height={280} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} opacity={0.95} />
          <rect x={-100} y={-200} width={200} height={190} rx={22} fill={col2} opacity={0.8} />
          <rect x={-90} y={-320} width={180} height={50} rx={10} fill="#546E7A" stroke={OL} strokeWidth={5} />
          <T x={0} y={-226} s={44}>{lab}</T>
          {els.map((e: string, q: number) => <g key={q} transform={`translate(${-60 + q * 60} ${-100 + 10 * Math.sin(t * 3 + q + k)})`}><circle r={24} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={8} s={20}>{e}</T>
            {k === 0 && q === 0 && null}</g>)}
          {ta !== undefined && t >= ta && <g transform={`translate(0 -380) scale(${pop(t, ta + k * 0.3, 0.4)}) rotate(${k ? 6 : -6})`}>
            <path d="M -110 -34 L 90 -34 L 120 0 L 90 34 L -110 34 Z" fill={k ? '#FFFFFF' : GOLD} stroke={OL} strokeWidth={5} strokeLinejoin="round" /><circle cx={92} cy={0} r={7} fill={OL} />
            <T x={-10} y={12} s={34}>{k ? z.nmc || '$128/kWh' : z.lfp || '$81/kWh'}</T></g>}
        </g>; })}
      {ja !== undefined && t >= ja && <T x={(z.jarX ?? 1500) + 150} y={f + 60} s={22} c={NAVY} w={800}>{z.jarNote || 'NO NICKEL, NO COBALT IN LFP'}</T>}
    </g>;
  },

  /** BATTERY SUPPLY CHAIN valley */
  chainvalley: (t, z, f) => {
    const w = z.x1 - z.x0, names: string[] = z.names || ['MINE', 'REFINE', 'POWDERS', 'CELLS', 'PACK', 'CAR'];
    const sx = z.sx ?? 160, gap = z.gap ?? 330, lit = kf(z.lit, t, -1), by = f - 40;
    const shades: [number, number, number, string][] = (z.shades || []).map((s: any) => [Number(s[0]), Number(s[1]), Number(s[2]), String(s[3])]);
    const icon = (k: number) => {
      switch (k) {
        case 0: return <g><path d="M -110 0 L -40 -120 L 10 -60 L 50 -140 L 120 0 Z" fill="#A1887F" stroke={OL} strokeWidth={5} strokeLinejoin="round" /><rect x={-30} y={-40} width={60} height={40} rx={6} fill={GOLD} stroke={OL} strokeWidth={4} /><circle cx={-18} cy={2} r={10} fill={OL} /><circle cx={18} cy={2} r={10} fill={OL} /></g>;
        case 1: return <g><rect x={-100} y={-130} width={200} height={130} rx={8} fill="#B0BEC5" stroke={OL} strokeWidth={5} /><rect x={50} y={-210} width={34} height={90} fill="#78909C" stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((q) => { const u = ((t * 0.5 + q / 3) % 1); return <circle key={q} cx={67 + u * 20} cy={-220 - u * 90} r={14 + u * 18} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={0.8 * (1 - u)} />; })}
          {[-60, -10].map((q) => <rect key={q} x={q} y={-90} width={40} height={60} rx={4} fill="#4FC3F7" stroke={OL} strokeWidth={3} />)}</g>;
        case 2: return <g>{[-60, 0, 60].map((q, j) => <g key={q} transform={`translate(${q} 0)`}><path d="M -26 0 L -26 -90 Q 0 -110 26 -90 L 26 0 Z" fill={['#212121', '#90A4AE', '#7BD389'][j]} stroke={OL} strokeWidth={4} /></g>)}<T x={0} y={-118} s={16}>CATHODE · ANODE</T></g>;
        case 3: return <g>{[-60, -20, 20, 60].map((q, j) => <rect key={q} x={q - 16} y={-130 + 6 * Math.sin(t * 3 + j)} width={32} height={130} rx={4} fill="#42A5F5" stroke={OL} strokeWidth={4} />)}</g>;
        case 4: return <g><rect x={-110} y={-70} width={220} height={70} rx={10} fill={GOLD} stroke={OL} strokeWidth={5} />{[0, 1, 2, 3, 4, 5].map((q) => <path key={q} d={`M ${-90 + q * 36} -60 L ${-90 + q * 36} -10`} stroke={OL} strokeWidth={3} />)}</g>;
        default: return <g transform="scale(0.55)">{carShape('hatch', '#26C6DA', t * 80, {t})}</g>;
      }
    };
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E3F1FF" />
      <path d={`M ${z.x0} ${f - 260} Q ${z.x0 + 600} ${f - 420} ${z.x0 + 1300} ${f - 300} T ${z.x1} ${f - 280} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#C8E6C9" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={600} fill="#B5D69A" />
      {/* belt */}
      <rect x={sx - 60} y={by - 4} width={gap * (names.length - 1) + 120} height={22} rx={10} fill="#546E7A" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.round((gap * (names.length - 1)) / 80)}, (_, q) => { const u = ((q * 80 + t * 120) % (gap * (names.length - 1))), st = Math.floor(u / gap);
        return <rect key={'tok' + q} x={sx + u - 12} y={by - 26} width={24} height={20} rx={4} fill={['#A1887F', '#B0BEC5', '#7BD389', '#42A5F5', GOLD][Math.min(4, st)]} stroke={OL} strokeWidth={2.5} />; })}
      {names.map((nm, k) => { const x = sx + k * gap, on = Math.round(lit) === k;
        return <g key={'st' + k} transform={`translate(${x} ${by - 30})`}>
          <g transform={`scale(${on ? 1.12 + 0.03 * Math.sin(t * 6) : 1})`}>{icon(k)}</g>
          <g transform="translate(0 92)"><rect x={-90} y={-26} width={180} height={44} rx={22} fill={on ? GOLD : '#FFFFFF'} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={fit(nm, 160, 24)}>{nm}</T></g>
          {k < names.length - 1 && <path d={`M 120 -40 L ${gap - 120} -40`} stroke={OL} strokeWidth={4} strokeDasharray="10 10" markerEnd="" />}
        </g>; })}
      {shades.filter((s) => t >= s[0]).map(([at, k, pct, lab], j) => { const x = sx + k * gap, u = E.out(win(t, at, 0.9)), hh = 220;
        return <g key={'sh' + j} transform={`translate(${x} ${by - 300}) scale(${pop(t, at, 0.4)})`}>
          <rect x={-46} y={-hh} width={92} height={hh} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <rect x={-40} y={-hh * pct * u + -6 + 0} width={80} height={hh * pct * u} rx={6} fill={RED} transform={`translate(0 ${0})`} />
          <T x={0} y={-hh - 18} s={fit(lab, 200, 30)} c={RED}>{lab}</T></g>; })}
      {z.caption && <g transform={`translate(${sx + gap * 2.5} ${f + 140})`}><rect x={-560} y={-30} width={1120} height={54} rx={27} fill={NAVY} /><T x={0} y={8} s={fit(z.caption, 1080, 24)} c="#FFFFFF" w={800}>{z.caption}</T></g>}
    </g>;
  },

  /** THE CASH BURN MACHINE */
  cashworks: (t, z, f) => {
    const w = z.x1 - z.x0, mx = z.mx ?? 760;
    const labels: string[] = z.labels || ['REVENUE', 'GROSS PROFIT', 'OPERATING PROFIT', 'OPERATING CASH', 'FREE CASH FLOW'];
    const drains: string[] = z.drains || ['PARTS & WORKERS', 'R&D · MARKETING', 'TIMING (± SUPPLIERS)', 'NEW FACTORIES'];
    const shown = (k: number) => { const s = (z.stages || []).find((p: any) => Number(p[1]) === k); return s ? t >= Number(s[0]) : true; };
    const at = (k: number) => { const s = (z.stages || []).find((p: any) => Number(p[1]) === k); return s ? Number(s[0]) : 0; };
    const lev = (k: number) => clamp(kf((z.levels || {})[k], t, 0.6), -0.6, 1);
    const neg = z.negAt !== undefined && t >= z.negAt;
    const tankY = (k: number) => f - 700 + k * 150;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EDF1F6" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'bk' + k} x={z.x0 + k * 120} y={-400} width={4} height={1260 + f} fill="#DCE3EC" />)}
      <rect x={z.x0} y={f} width={w} height={600} fill="#C9D3DC" />
      {/* funnel + coins */}
      <g transform={`translate(${mx} ${f - 790})`}><path d="M -180 -60 L 180 -60 L 40 40 L -40 40 Z" fill={GOLD} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        {Array.from({length: 10}, (_, q) => { const u = ((t * 0.9 + q / 10) % 1); return <g key={q} transform={`translate(${-150 + rnd(q) * 300 * (1 - u)} ${-200 + u * 200})`}><ellipse rx={18} ry={8} fill="#FFD54F" stroke={OL} strokeWidth={3} /></g>; })}</g>
      {/* column pipe */}
      <rect x={mx - 26} y={f - 760} width={52} height={700} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
      {labels.map((lab, k) => { if (!shown(k)) return null; const y = tankY(k), u = pop(t, at(k), 0.45), L = lev(k), isNeg = k === labels.length - 1 && (neg || L < 0);
        return <g key={'tk' + k} transform={`translate(${mx} ${y}) scale(${u})`}>
          <rect x={-170} y={-60} width={340} height={120} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
          <clipPath id={`tkc${k}`}><rect x={-164} y={-54} width={328} height={108} rx={16} /></clipPath>
          <g clipPath={`url(#tkc${k})`}>
            {L > 0 && <rect x={-164} y={54 - 108 * L} width={328} height={108 * L} fill={k === 0 ? GOLD : k < 3 ? GREEN : BLUE} opacity={0.85} />}
            {L > 0 && <path d={`M -164 ${54 - 108 * L} q 40 ${-8 * Math.sin(t * 4)} 82 0 t 82 0 t 82 0 t 82 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.6} />}
            {isNeg && <rect x={-164} y={-54} width={328} height={108} fill={RED} opacity={0.25 + 0.15 * Math.sin(t * 6)} />}</g>
          <T x={0} y={-8} s={fit(lab, 300, 30)} c={isNeg ? RED : NAVY}>{lab}</T>
          {isNeg && <T x={0} y={34} s={30} c={RED}>{z.negText || 'BELOW ZERO'}</T>}
          {/* the drain for this stage (between tank k and k+1) */}
          {k < drains.length && shown(k + 1) && <g>
            <path d={`M 26 ${80} L 260 ${80} L 260 ${140}`} stroke={k === 3 ? RED : '#78909C'} strokeWidth={22} fill="none" strokeLinejoin="round" />
            {Array.from({length: 4}, (_, q) => { const v = ((t * 1.2 + q / 4) % 1); return <ellipse key={q} cx={40 + v * 220} cy={80} rx={9} ry={5} fill="#FFD54F" stroke={OL} strokeWidth={2} />; })}
            <g transform="translate(280 150)"><rect x={0} y={-24} width={Math.max(220, drains[k].length * 17 + 30)} height={44} rx={22} fill={k === 3 ? RED : '#FFFFFF'} stroke={OL} strokeWidth={4} />
              <T x={Math.max(220, drains[k].length * 17 + 30) / 2} y={8} s={24} c={k === 3 ? '#FFFFFF' : NAVY}>{`− ${drains[k]}`}</T></g></g>}
        </g>; })}
    </g>;
  },

  /** PRICE-WAR STREET: dealerships with flip boards stepping down */
  pricestreet: (t, z, f) => {
    const w = z.x1 - z.x0, names: string[] = z.names || ['DEALER A', 'DEALER B', 'DEALER C'], gap = z.gap ?? 520, sx = z.sx ?? 300;
    const cuts: [number, number, string][] = (z.cuts || []).map((c: any) => [Number(c[0]), Number(c[1]), String(c[2])]);
    const start: string[] = z.start || ['$30,000', '$29,500', '$31,000', '$30,500'];
    const mg = clamp(kf(z.margin, t, 0.7));
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#DCEEFF" />
      <path d={`M ${z.x0} ${f - 300} Q ${z.x0 + 900} ${f - 420} ${z.x1} ${f - 320} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#CFE3C0" />
      <rect x={z.x0} y={f} width={w} height={600} fill="#9AA6B2" /><rect x={z.x0} y={f + 120} width={w} height={8} fill="#FFFFFF" opacity={0.6} />
      {names.map((nm, k) => { const x = sx + k * gap, cur = cuts.filter((c) => c[1] === k && t >= c[0]).pop(), txt = cur ? cur[2] : start[k % start.length], hit = cur ? cur[0] : -9;
        const shake = jig(t, hit, 26, 6) * 8;
        return <g key={'d' + k} transform={`translate(${x} ${f})`}>
          <rect x={-230} y={-360} width={460} height={360} rx={10} fill={['#FFFFFF', '#F1F8E9', '#FFF8E1', '#E3F2FD'][k % 4]} stroke={OL} strokeWidth={6} />
          <rect x={-230} y={-360} width={460} height={60} fill={[BLUE, GREEN, '#FF7043', '#7E57C2'][k % 4]} stroke={OL} strokeWidth={6} /><T x={0} y={-318} s={28} c="#FFFFFF">{nm}</T>
          <rect x={-200} y={-280} width={400} height={180} rx={6} fill="#CFE8FF" stroke={OL} strokeWidth={4} />
          <g transform="translate(-30 -110) scale(0.62)">{carShape(['hatch', 'suv', 'sedan', 'hatch'][k % 4], CARC[(k * 3 + 1) % CARC.length], 0, {t})}</g>
          <g transform={`translate(${shake} -470) rotate(${shake * 0.6})`}><rect x={-170} y={-60} width={340} height={110} rx={14} fill={NAVY} stroke={OL} strokeWidth={6} />
            <T x={0} y={16} s={fit(txt, 300, 54)} c={cur ? GOLD : '#FFFFFF'}>{txt}</T>
            <path d="M -60 50 L -60 110 M 60 50 L 60 110" stroke={OL} strokeWidth={8} /></g>
          {cur && t < hit + 1.6 && <g transform={`translate(150 -560) scale(${pop(t, hit, 0.35)}) rotate(10)`}><path d="M -80 -30 L 80 -30 L 80 30 L -80 30 Z" fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={10} s={28} c="#FFFFFF">PRICE CUT!</T></g>}
        </g>; })}
      {z.gauge !== false && <g transform={`translate(${z.gaugeX ?? 1740} ${f - 520})`}>
        <path d="M -180 0 A 180 180 0 0 1 180 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <path d="M -150 0 A 150 150 0 0 1 -75 -130" stroke={RED} strokeWidth={26} fill="none" /><path d="M -75 -130 A 150 150 0 0 1 75 -130" stroke={GOLD} strokeWidth={26} fill="none" /><path d="M 75 -130 A 150 150 0 0 1 150 0" stroke={GREEN} strokeWidth={26} fill="none" />
        <g transform={`rotate(${-90 + 180 * mg + Math.sin(t * 9) * 1.5})`}><path d="M 0 0 L 0 -150" stroke={OL} strokeWidth={10} strokeLinecap="round" /></g><circle r={18} fill={OL} />
        <T x={0} y={60} s={34} c={NAVY}>{z.gaugeText || 'MARGIN'}</T></g>}
    </g>;
  },

  /** RO-RO PORT: cars drive up a ramp into a car carrier */
  carport: (t, z, f) => {
    const w = z.x1 - z.x0, shipX = z.shipX ?? 1300, lot = clamp(kf(z.lot, t, 0.5)), rows = 3, cols = 9;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#CFE9FF" />
      <rect x={z.x0} y={f - 150} width={w} height={800} fill="#4F8FC0" />
      {Array.from({length: 14}, (_, q) => <path key={q} d={`M ${z.x0 + ((q * 260 + t * 30) % w)} ${f - 110 + (q % 3) * 30} q 30 -10 60 0`} stroke="#FFFFFF" strokeWidth={3} fill="none" opacity={0.6} />)}
      {/* quay */}
      <rect x={z.x0} y={f - 40} width={shipX - 300 - z.x0} height={640} fill="#A8B3BD" stroke={OL} strokeWidth={5} />
      {/* the lot */}
      {Array.from({length: Math.round(rows * cols * lot)}, (_, k) => { const c = k % cols, r = Math.floor(k / cols);
        return <g key={'lc' + k} transform={`translate(${(z.lotX ?? -100) + c * 110 + r * 30} ${f + 20 + r * 60}) scale(0.24)`}>{carShape('hatch', CARC[(k * 5) % CARC.length], 0, {t})}</g>; })}
      {/* the ship: a tall boxy car carrier (no livery) */}
      <g transform={`translate(${shipX} ${f - 60 + 6 * Math.sin(t * 1.1)})`}>
        <path d="M -260 0 L 900 0 L 860 90 L -230 90 Z" fill="#37474F" stroke={OL} strokeWidth={6} />
        <rect x={-250} y={-430} width={1120} height={430} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {Array.from({length: 4}, (_, r) => <path key={r} d={`M -230 ${-80 - r * 90} L 850 ${-80 - r * 90}`} stroke="#CFD8DC" strokeWidth={4} />)}
        <rect x={720} y={-520} width={140} height={100} rx={10} fill="#ECEFF1" stroke={OL} strokeWidth={5} /><rect x={736} y={-500} width={108} height={30} rx={4} fill="#4FC3F7" />
        <rect x={-250} y={-200} width={1120} height={36} fill={z.stripe || BLUE} opacity={0.85} />
        <T x={300} y={-260} s={44} c={NAVY}>{z.shipText || 'CAR CARRIER'}</T>
        {/* ramp */}
        <path d="M -250 -40 L -420 60" stroke={OL} strokeWidth={22} /><path d="M -250 -40 L -420 60" stroke="#B0BEC5" strokeWidth={14} /></g>
      {/* cars driving aboard */}
      {Array.from({length: 4}, (_, q) => { const u = ((t * 0.32 + q / 4) % 1), x = lerp(z.x0 + 500, shipX - 200, u), y = u < 0.7 ? f - 20 : lerp(f - 20, f - 110, (u - 0.7) / 0.3);
        return <g key={'drv' + q} transform={`translate(${x} ${y}) scale(${0.36 * (u > 0.92 ? 1 - (u - 0.92) * 10 : 1)})`} opacity={u > 0.95 ? 0 : 1}>{carShape(['hatch', 'suv', 'sedan', 'hatch'][q], CARC[(q * 2 + 1) % CARC.length], t * 300, {t, lights: true})}</g>; })}
      {z.board && <g transform={`translate(${z.boardX ?? 400} ${f - 520})`}><rect x={-300} y={-50} width={600} height={90} rx={14} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={12} s={fit(z.board, 560, 36)} c={GOLD}>{z.board}</T></g>}
    </g>;
  },

  /** TARIFF GATES: one road, two gates */
  tariffgate: (t, z, f) => {
    const w = z.x1 - z.x0, wall = z.wallAt !== undefined ? E.outBack(win(t, z.wallAt, 0.8)) : 1, eu = z.euAt !== undefined ? pop(t, z.euAt, 0.5) : 1;
    const euLines: string[] = z.euLines || ['10% CAR DUTY', '+ 17.0% BYD', '+ 35.3% SAIC'];
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E1F0FF" />
      <rect x={z.x0} y={f} width={w} height={600} fill="#B9C5CF" />
      <path d={`M ${z.x0} ${f + 60} L ${z.x1} ${f + 60}`} stroke="#FFFFFF" strokeWidth={8} strokeDasharray="60 40" />
      {/* the wall (left gate) */}
      <g transform={`translate(${z.wallX ?? 520} ${f})`}>
        <rect x={-260} y={-620 * wall} width={520} height={620 * wall} fill="#8D6E63" stroke={OL} strokeWidth={6} />
        {Array.from({length: Math.floor(12 * wall)}, (_, r) => Array.from({length: 5}, (_, c) => <rect key={r * 9 + c} x={-256 + c * 104 + (r % 2) * 52 - (r % 2 && c === 4 ? 52 : 0)} y={-48 - r * 50} width={100} height={46} fill={['#A1887F', '#8D6E63', '#BCAAA4'][(r + c) % 3]} stroke={OL} strokeWidth={2} />))}
        {wall > 0.5 && <g transform={`translate(0 ${-620 * wall + 90})`}><rect x={-210} y={-56} width={420} height={100} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={18} s={fit(z.usText || 'U.S. · 100%', 380, 54)} c={RED}>{z.usText || 'U.S. · 100%'}</T></g>}
        {z.usSub && <T x={0} y={60} s={22} c={NAVY} w={800}>{z.usSub}</T>}</g>
      {/* the toll gate (right) */}
      <g transform={`translate(${z.euX ?? 1150} ${f}) scale(${eu})`}>
        <rect x={-30} y={-420} width={60} height={420} fill="#546E7A" stroke={OL} strokeWidth={5} /><rect x={330} y={-420} width={60} height={420} fill="#546E7A" stroke={OL} strokeWidth={5} />
        <rect x={-60} y={-480} width={480} height={80} rx={12} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={180} y={-428} s={fit(z.euTitle || 'EUROPEAN UNION', 440, 36)} c={GOLD}>{z.euTitle || 'EUROPEAN UNION'}</T>
        <g transform={`rotate(${-70 * (0.5 + 0.5 * Math.sin(t * 1.3))} 30 -150)`}><rect x={30} y={-164} width={330} height={26} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} />{[0, 1, 2, 3].map((q) => <rect key={q} x={60 + q * 80} y={-164} width={40} height={26} fill={RED} />)}</g>
        <g transform="translate(560 -300)"><rect x={-150} y={-120} width={300} height={40 + euLines.length * 46} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          {euLines.map((l, k) => <T key={k} x={0} y={-76 + k * 46} s={fit(l, 270, 30)} c={k ? RED : NAVY}>{l}</T>)}</g>
        {z.minAt !== undefined && t >= z.minAt && <g transform={`translate(560 -20) scale(${pop(t, z.minAt, 0.4)}) rotate(-4)`}><rect x={-180} y={-34} width={360} height={60} rx={30} fill={GOLD} stroke={OL} strokeWidth={5} /><T x={0} y={8} s={fit(z.minText || 'OR: MINIMUM PRICE (2026)', 330, 26)}>{z.minText || 'OR: MINIMUM PRICE (2026)'}</T></g>}
      </g>
    </g>;
  },

  /** SHOW TITLE CARD */
  c61title: (t, z, f) => {
    const cx = 960, cy = 470, lines: string[] = z.lines || ['CHEAP CARS', 'BIG QUESTIONS'], sub: string = z.sub || 'WHY ARE CHINESE CARS SO CHEAP — AND SO ADVANCED?';
    const subs: [number, string][] = (z.subs || []).map((p: any) => [Number(p[0]), String(p[1])]);
    const cur = subs.filter((p) => t >= p[0]).pop(), typed = cur ? cur[1].slice(0, Math.floor((t - cur[0]) * 32)) : '';
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill={NAVY} />
      {Array.from({length: 22}, (_, k) => { const y = -200 + k * 70, sp = 300 + (k % 5) * 120, x0 = ((t * sp + k * 377) % 2800) - 400;
        return <path key={'ln' + k} d={`M ${x0} ${y} L ${x0 + 260} ${y}`} stroke={k % 3 ? '#1E88E5' : GOLD} strokeWidth={k % 3 ? 6 : 10} strokeLinecap="round" opacity={0.5} />; })}
      <g transform={`translate(${cx} ${cy - 250}) scale(${pop(t, 0.3, 0.5)})`}><rect x={-360} y={-36} width={720} height={60} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={8} s={26} ls={3}>{z.kicker || 'THE HIDDEN ECONOMICS PRESENTS'}</T></g>
      {lines.map((word, wi) => <g key={wi} transform={`translate(${cx + (1 - E.outBack(win(t, 0.5 + wi * 0.35, 0.6))) * (wi ? -1600 : 1600)} ${cy - 40 + wi * 165}) rotate(${wi ? 2 : -2})`}>
        <T x={8} y={12} s={150} c={OL}>{word}</T><T x={0} y={0} s={150} c={wi ? '#FFFFFF' : GOLD} st={OL} sw={14}>{word}</T></g>)}
      {/* a little generic car zooms across */}
      <g transform={`translate(${((t - 0.2) * 900) % 2600 - 400} 860) scale(0.6)`}>{carShape('hatch', '#26C6DA', t * 600, {t, lights: true})}</g>
      {[0, 1, 2].map((q) => <path key={'sl' + q} d={`M ${((t - 0.2) * 900) % 2600 - 560 - q * 40} ${800 + q * 22} l -160 0`} stroke="#FFFFFF" strokeWidth={6} opacity={0.6} strokeLinecap="round" />)}
      <g transform={`translate(${cx} ${cy + 300}) scale(${pop(t, 1.4, 0.45)}) rotate(${-1.5 + Math.sin(t * 2)})`}>
        <path d="M -600 -42 L 600 -42 L 570 0 L 600 42 L -600 42 L -570 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={7} strokeLinejoin="round" /><T x={0} y={14} s={fit(sub, 1120, 38)} c={NAVY}>{sub}</T></g>
      {cur && <g transform="translate(960 1010)"><rect x={-760} y={-40} width={1520} height={70} rx={14} fill="#0B1A3A" opacity={0.88} />
        <T x={0} y={8} s={34} c="#FFE066" w={800}>{typed}{Math.floor(t * 3) % 2 ? '▌' : ' '}</T></g>}
    </g>;
  },

  /** ACT BUMPER */
  c61bumper: (t, z, f) => {
    const act: string = z.act || 'PART ONE', title: string = z.title || '', cap: string = z.caption || '', col2 = z.color || BLUE;
    const wipe = E.out(win(t, 0, 0.45)), car = (t - 0.1) * 1500 - 400;
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#F2F6FA" />
      <g transform={`translate(${2600 - 2600 * wipe} 0)`}>{Array.from({length: 26}, (_, k) => <path key={k} d={`M ${k * 140 - 400} -200 L ${k * 140 - 330} -200 L ${k * 140 + 290} 1300 L ${k * 140 + 220} 1300 Z`} fill={k % 2 ? col2 : NAVY} opacity={0.92} />)}</g>
      <rect x={-200} y={930} width={2400} height={150} fill="#37474F" /><path d="M -200 1000 L 2200 1000" stroke="#FFFFFF" strokeWidth={8} strokeDasharray="60 40" />
      <g transform={`translate(${car} 960) scale(0.75)`}>{carShape(z.carKind || 'hatch', z.carColor || GOLD, t * 700, {t, lights: true})}</g>
      {[0, 1, 2].map((q) => <path key={'sp' + q} d={`M ${car - 200 - q * 30} ${880 + q * 24} l -220 0`} stroke="#FFFFFF" strokeWidth={6} opacity={0.6} strokeLinecap="round" />)}
      <g transform={`translate(520 470) scale(${E.outBack(win(t, 0.2, 0.6))})`}>
        <circle r={190} fill={GOLD} stroke={OL} strokeWidth={10} /><circle r={160} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <T x={0} y={-40} s={36} c={col2} ls={4}>PART</T><T x={0} y={80} s={140} c={OL}>{z.num || '1'}</T></g>
      <g transform={`translate(1240 450) scale(${pop(t, 0.45, 0.45)}) rotate(-2)`}><rect x={-540} y={-100} width={1080} height={150} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={9} />
        <T x={0} y={22} s={fit(title, 1000, 70)} c={OL}>{title}</T><T x={0} y={-62} s={26} c={col2} ls={6}>{act}</T></g>
      {cap && <g transform={`translate(1240 630) scale(${pop(t, 0.9, 0.4)}) rotate(${Math.sin(t * 2.4) * 1.2})`}><rect x={-500} y={-38} width={1000} height={64} rx={32} fill={NAVY} />
        <T x={0} y={8} s={fit(cap, 940, 30)} c="#FFE066" w={800}>{cap}</T></g>}
    </g>;
  },
};

/* ============================================================================================ ITEMS */
/** EVCAR: a driving generic car (x keyframes), wheels spin with speed; optional tag above it and a price `cut` animation */
const evcar: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, dir = a.flip ? -1 : 1, bounce = Math.abs(vx) > 20 ? Math.abs(Math.sin(t * 14 + i)) * 4 : 0;
  const tag: string | undefined = pick(a.tags, t, a.tag);
  return <g key={'ev' + i} transform={`translate(${x} ${y - bounce}) scale(${s * dir} ${s})`}>
    {Math.abs(vx) > 60 && [0, 1, 2].map((q) => <path key={q} d={`M ${-260 - q * 30} ${-40 - q * 26} l -140 0`} stroke={OL} strokeWidth={5} opacity={0.35} strokeLinecap="round" />)}
    {carShape(a.carKind || 'hatch', a.color || '#26C6DA', (kf(a.x, t, 0) / 2) * dir, {lights: !!a.lights, lidar: !!a.lidar, screen: a.screen ? 1 : 0, t})}
    {tag && <g transform={`scale(${dir} 1) translate(0 -230) rotate(${Math.sin(t * 3 + i) * 4})`}><path d="M 0 -30 L 0 0" stroke={OL} strokeWidth={4} />
      <rect x={-Math.max(90, tag.length * 13 + 20)} y={-90} width={Math.max(180, tag.length * 26 + 40)} height={64} rx={14} fill={a.tagColor || GOLD} stroke={OL} strokeWidth={5} />
      <T x={0} y={-46} s={fit(tag, Math.max(160, tag.length * 26 + 10), 38)}>{tag}</T></g>}
  </g>;
};

/** SUSPECTS: a lineup board of four cards; `hi` keyframes highlight a card; `stamps` [[t, idx, text, color]] */
const suspects: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * pop(t, at, 0.45);
  const cards: string[] = a.cards || ['EFFICIENCY', 'SUBSIDIES', 'FINANCIAL ENGINEERING', 'CASH BURN'];
  const icon = (k: number) => k === 0 ? <g>{Array.from({length: 8}, (_, q) => <rect key={q} x={-12} y={-62} width={24} height={26} rx={4} fill={OL} transform={`rotate(${q * 45 + t * 30})`} />)}<circle r={44} fill={OL} /><circle r={18} fill="#90CAF9" /></g>
    : k === 1 ? <T x={0} y={34} s={100} c={OL}>$</T>
    : k === 2 ? <g><path d="M -46 -16 L 40 -16 M 22 -34 L 44 -16 L 22 2" stroke={OL} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /><path d="M 46 22 L -40 22 M -22 4 L -44 22 L -22 40" stroke={OL} strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" /></g>
    : <path d={`M 0 52 C -44 52 -50 10 -30 -14 C -26 4 -14 8 -10 2 C -18 -24 -4 -50 14 -60 C 10 -36 40 -22 40 10 C 40 36 22 52 0 52 Z`} fill="#FF7043" stroke={OL} strokeWidth={5} transform={`scale(${1 + 0.05 * Math.sin(t * 8)})`} />;
  const hi = pick(a.his, t, a.hi ?? -1);
  const stamps: [number, number, string, string][] = (a.stamps || []).map((p: any) => [Number(p[0]), Number(p[1]), String(p[2]), String(p[3] || RED)]);
  return <g key={'sus' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-860} y={-300} width={1720} height={600} rx={24} fill="#1B2A44" stroke={OL} strokeWidth={8} />
    {Array.from({length: 6}, (_, q) => <path key={q} d={`M -840 ${-240 + q * 90} L 840 ${-240 + q * 90}`} stroke="#3A4E70" strokeWidth={3} />)}
    <T x={0} y={-238} s={34} c={GOLD} ls={6}>{a.title || 'THE FOUR SUSPECTS'}</T>
    {cards.map((c, k) => { const cx = -630 + k * 420, on = hi === k, ap = pop(t, at + 0.15 + k * 0.18, 0.4);
      const st = stamps.filter((p) => p[1] === k && t >= p[0]).pop();
      return <g key={k} transform={`translate(${cx} 40) scale(${ap * (on ? 1.08 : 1)}) rotate(${(k - 1.5) * 1.5})`}>
        <rect x={-180} y={-200} width={360} height={380} rx={18} fill={on ? '#FFFFFF' : '#ECEFF1'} stroke={on ? GOLD : OL} strokeWidth={on ? 10 : 6} />
        <circle cx={0} cy={-70} r={86} fill={['#90CAF9', '#FFE082', '#CE93D8', '#FFAB91'][k]} stroke={OL} strokeWidth={5} />
        <g transform="translate(0 -70)">{icon(k)}</g>
        <T x={0} y={80} s={fit(c, 330, 34)} c={NAVY}>{c}</T>
        <T x={0} y={130} s={22} c="#5C6B80" w={700}>{`SUSPECT ${k + 1}`}</T>
        {st && <g transform={`translate(0 -20) rotate(-14) scale(${1 + 0.8 * (1 - E.out(win(t, st[0], 0.25)))})`} opacity={win(t, st[0], 0.15)}>
          <rect x={-170} y={-48} width={340} height={92} rx={10} fill="none" stroke={st[3]} strokeWidth={10} /><T x={0} y={18} s={fit(st[2], 310, 52)} c={st[3]}>{st[2]}</T></g>}
      </g>; })}
  </g>;
};

/** CELLBOT "VOLTY": a battery cell on legs (running gag) whose price tag keeps dropping (`tags` [[t, text]]) */
const cellbot: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, moving = Math.abs(vx) > 20, ph = t * 12 + i, lg = moving ? Math.sin(ph) * 16 : 0;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.5) hy += Math.sin((u / 0.5) * Math.PI) * 80; }
  const tg = (a.tags || []).filter((p: any) => t >= Number(p[0])).pop(), tgAt = tg ? Number(tg[0]) : -9;
  const face: string = pick(a.faces, t, a.face || 'happy'), bl = ((t + i) % 2.9) < 0.12;
  return <g key={'cb' + i} transform={`translate(${x} ${y - hy}) scale(${s})`}>
    <ellipse cx={0} cy={4 + hy} rx={60} ry={10} fill={OL} opacity={0.18} />
    <path d={`M -20 -30 L ${-20 - lg} 0 M 20 -30 L ${20 + lg} 0`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
    <rect x={-50} y={-210} width={100} height={180} rx={18} fill="#42A5F5" stroke={OL} strokeWidth={6} />
    <rect x={-22} y={-226} width={44} height={20} rx={5} fill={STEEL} stroke={OL} strokeWidth={4} />
    <rect x={-50} y={-90} width={100} height={60} rx={8} fill={GOLD} stroke={OL} strokeWidth={5} /><T x={0} y={-52} s={20}>LFP</T>
    <g transform="translate(0 -150)">{[-20, 20].map((q, k) => <g key={k}><circle cx={q} cy={0} r={14} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
      {bl ? <path d={`M ${q - 9} 0 L ${q + 9} 0`} stroke={OL} strokeWidth={3.5} /> : <circle cx={q + 3} cy={face === 'worry' ? 4 : 1} r={6} fill={OL} />}</g>)}
      <path d={face === 'worry' ? 'M -12 32 Q 0 24 12 32' : 'M -14 24 Q 0 38 14 24'} stroke={OL} strokeWidth={4} fill="none" strokeLinecap="round" /></g>
    <path d={`M 50 -150 Q 90 ${-180 + 10 * Math.sin(t * 5)} 110 -150`} stroke={OL} strokeWidth={7} fill="none" strokeLinecap="round" />
    {tg && <g transform={`translate(150 ${-150 + jig(t, tgAt, 20, 6) * 20}) rotate(${10 + Math.sin(t * 3) * 6})`}>
      <path d="M -10 0 L 20 -30 L 140 -30 L 140 30 L 20 30 Z" fill="#FFF8E1" stroke={OL} strokeWidth={4} strokeLinejoin="round" /><circle cx={10} cy={0} r={5} fill={OL} />
      <T x={80} y={10} s={fit(String(tg[1]), 110, 28)} c={RED}>{String(tg[1])}</T></g>}
  </g>;
};

/** COINRAIN: coins falling from (x,y) for a while (money pouring in or out) */
const coinrain: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.6)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), n = a.n ?? 14, wdt = a.w ?? 400, fall = a.fall ?? 500, red = !!a.red;
  return <g key={'cr' + i}>{Array.from({length: n}, (_, q) => { const u = ((t - at) * 0.8 + q / n) % 1;
    return <ellipse key={q} cx={x - wdt / 2 + rnd(q + i) * wdt} cy={y + u * fall} rx={16} ry={7} fill={red ? '#FF8A80' : '#FFD54F'} stroke={OL} strokeWidth={3} opacity={1 - u * 0.6} />; })}</g>;
};

export const CARS_ITEMS: Record<string, ItemFn> = {evcar, suspects, cellbot, coinrain};
export const CARS_INDOOR = ['evshow', 'costlab', 'gigaline', 'cellplant', 'cashworks', 'c61title', 'c61bumper'];
