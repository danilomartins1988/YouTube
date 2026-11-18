import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * AUTOMATION kit for CartoonStage (Episode 62, "Could AI Make American Factories Cheaper Than China's?"; arc Episode 2 after
 * Ep 60's factory kit).
 *
 * Prime-time cartoon energy in the retro-futurist sci-fi comedy GENRE only: thick clean outlines, flat saturated colour, chrome
 * and neon trims, rubbery squash and stretch, deadpan joke signs. Everything ORIGINAL; no logos, flags, seals or brand names.
 * Day scenes. Respectful by design: workers and engineers are ordinary skilled professionals; no national caricature.
 * Sets:
 *  - ohiobot: the HYPOTHETICAL automated factory. `variant` 'us' (red-brick shell, tall day windows, water tower outside) or
 *    'cn' (long white mega-hall, dense arm rows, supplier trucks at the dock). Chrome six-axis arms with weld sparks (`arms`),
 *    toasters on a conveyor, a scan gantry (`scanX`) that sweeps and flashes ✓, self-driving carts, a scheduler wall whose
 *    bars reshuffle at `schedAt`, predictive-maintenance motor (`maintAt`: sound rings, then a WRENCH SOON flag), a cyan
 *    wireframe digital twin of the line (`twinAt`), `hi` ('vision'|'arms'|'carts'|'sched'|'maint') pulses one system,
 *    `idle` keyframes 0..1 slow the arms and light IDLE lamps, `hyp` shows the HYPOTHETICAL banner.
 *  - billbox: a glass cost box filled by slices `slices` [[t, label, share%, color]]; `pullAt`/`pullIdx` lifts one slice out on a
 *    crane hook; `robotAt` drops a smaller ROBOTS + SOFTWARE block into the gap; `title`, `note`.
 *  - toastlab: the THREE-FACTORY lab: columns `cols` [{name, sub, at, color, blocks: [{label, v (KF), color}]}], stacked cost
 *    blocks (px per $ = `scale`), totals that recount live, `judgeAt` lights the CHEAPEST lamp on the lowest visible column,
 *    knobs `knobs` [{label, v (KF), max, unit, at}], the ILLUSTRATIVE MODEL banner always on.
 *  - robotrace: country towers built from little robot tokens poured by a dispenser: `rows` [{name, value, at, color, display}],
 *    `max`, `title`, `foot`; `hi` index pulses.
 *  - chainweb: a small Ohio plant in the middle; parts fly in along arcs from depots `srcs` [{label, from, at, x, y, color}];
 *    `cutAt` + `cutIdx` turns one route red and stops it.
 *  - moneyriver: one $100 coin pours a stream that splits into channels and buckets `buckets` [{label, level, at, color}];
 *    `ownerAt` lights the last bucket; ILLUSTRATIVE banner.
 *  - aititle / aibumper: show title card (a chrome arm writes the title; `lines`, `sub`, `subs`) and act bumpers (circuit-board
 *    wipe, TORQ stamps the act number; `num`, `act`, `title`, `caption`, `color`).
 * Items: torq (TORQ, the one-armed robot on wheels with a screen face; `face`/`faces`, `legs` cardboard legs and `legsFallAt`,
 *  `hops`, `point`, `stampAt`), humanoid (a prototype humanoid on a test stand: `dance`, `wobbleAt`, `fallAt`, tag PROTOTYPE),
 *  pricemeter (an illustrative seesaw cost meter between two factories, needle `tilt` keyframes −1..1, no numbers).
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

const CY = '#00C2E8', ORANGE = '#FF9F1C', RED = '#E5484D', GREEN = '#2E9E5B', YEL = '#FFD23F', CHROME = '#CFD8E3', CHROME2 = '#8FA1B6', BRICK = '#B4553F', TEAL = '#1F7A8C', PURPLE = '#7E57C2';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'acl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const banner = (x: number, y: number, txt: string, c = RED, s = 26) => { const w = Math.max(260, txt.length * s * 0.62 + 50);
  return <g transform={`translate(${x} ${y}) rotate(-2)`}><rect x={-w / 2} y={-s} width={w} height={s * 1.7} rx={8} fill={c} stroke={OL} strokeWidth={4} />
    <T x={0} y={s * 0.32} s={s} c="#FFFFFF">{txt}</T></g>; };

/** the $100 product: a little chrome smart toaster (continuity with Mel's toaster in Ep 60) */
const toaster = (t: number, k: number, s = 1, ok = 0) => <g transform={`scale(${s})`}>
  <rect x={-34} y={-30} width={68} height={46} rx={14} fill="#ECEFF1" stroke={OL} strokeWidth={3.5} />
  <rect x={-20} y={-38} width={14} height={10} rx={3} fill={CHROME2} stroke={OL} strokeWidth={2.5} /><rect x={6} y={-38} width={14} height={10} rx={3} fill={CHROME2} stroke={OL} strokeWidth={2.5} />
  <rect x={-24} y={-14} width={30} height={14} rx={4} fill="#16232E" /><rect x={-22} y={-12} width={26} height={10} rx={3} fill={CY} opacity={0.5 + 0.4 * Math.sin(t * 4 + k)} />
  <circle cx={24} cy={-6} r={5} fill={ok ? GREEN : RED} />
</g>;

/** a chrome six-axis robot arm on a turntable (distinct from Ep 60's arms): rounded links, cyan joints, gripper; speed `sp` */
const arm6 = (t: number, k: number, s = 1, sp = 1, color = ORANGE, spark = false) => {
  const ph = (t * 0.8 * sp + k * 0.29), a1 = -25 + 40 * Math.sin(ph * 2.2), a2 = 70 + 35 * Math.cos(ph * 2.2), a3 = -40 + 30 * Math.sin(ph * 4.4);
  const r1 = (a1 * Math.PI) / 180, r2 = ((a1 + a2) * Math.PI) / 180, r3 = ((a1 + a2 + a3) * Math.PI) / 180;
  const ex = Math.sin(r1) * 130, ey = -Math.cos(r1) * 130 - 80, wx = ex + Math.sin(r2) * 110, wy = ey - Math.cos(r2) * 110, hx = wx + Math.sin(r3) * 40, hy = wy - Math.cos(r3) * 40;
  const lnk = (d: string, w: number, c: string) => <g><path d={d} stroke={OL} strokeWidth={w + 10} strokeLinecap="round" strokeLinejoin="round" fill="none" /><path d={d} stroke={c} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill="none" /></g>;
  return <g transform={`scale(${s})`}>
    <ellipse cx={0} cy={2} rx={70} ry={12} fill={OL} opacity={0.18} />
    <path d="M -60 0 L -46 -40 L 46 -40 L 60 0 Z" fill="#455A64" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    <rect x={-34} y={-90} width={68} height={54} rx={22} fill={color} stroke={OL} strokeWidth={4} />
    <rect x={-26} y={-66} width={52} height={8} rx={4} fill="#FFFFFF" opacity={0.55} />
    {lnk(`M 0 -80 L ${ex} ${ey}`, 26, color)}{lnk(`M ${ex} ${ey} L ${wx} ${wy}`, 20, CHROME)}{lnk(`M ${wx} ${wy} L ${hx} ${hy}`, 14, CHROME2)}
    {[[0, -80, 15], [ex, ey, 13], [wx, wy, 10]].map(([cx, cy, r], q) => <g key={q}><circle cx={cx} cy={cy} r={r} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={cx} cy={cy} r={r * 0.45} fill={CY} /></g>)}
    <g transform={`translate(${hx} ${hy}) rotate(${(a1 + a2 + a3)})`}>
      <path d={`M -12 0 L ${-9 - 5 * Math.abs(Math.sin(ph * 6))} -22 M 12 0 L ${9 + 5 * Math.abs(Math.sin(ph * 6))} -22`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
      {spark && Math.sin(ph * 9) > 0.2 && Array.from({length: 7}, (_, q) => { const an = (q / 7) * Math.PI * 2 + t * 7, L = 14 + 18 * rnd(q + Math.floor(t * 12));
        return <path key={q} d={`M 0 -26 L ${Math.cos(an) * L} ${-26 + Math.sin(an) * L}`} stroke={q % 2 ? YEL : '#FFFFFF'} strokeWidth={4} strokeLinecap="round" />; })}
    </g>
  </g>;
};

/** a self-driving floor cart (AMR) carrying a crate, light bar blinking */
const cart = (t: number, k: number, label = 'PARTS') => <g>
  <rect x={-70} y={-34} width={140} height={34} rx={10} fill="#37474F" stroke={OL} strokeWidth={4} />
  <rect x={-60} y={-30} width={120} height={8} rx={4} fill={Math.floor(t * 3 + k) % 2 ? CY : '#FFFFFF'} />
  {[-40, 40].map((q) => <circle key={q} cx={q} cy={2} r={9} fill="#263238" stroke={OL} strokeWidth={3} />)}
  <rect x={-50} y={-86} width={100} height={52} rx={4} fill="#D7A86E" stroke={OL} strokeWidth={3.5} />
  <T x={0} y={-52} s={fit(label, 90, 18)}>{label}</T>
</g>;

/** a little generic worker / technician silhouette (hard hat or cap) */
const tech = (x: number, y: number, s: number, k: number, t: number) => <g key={'tc' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -8 -40 L -8 0 M 8 -40 L 8 0" stroke="#2B4A5E" strokeWidth={12} strokeLinecap="round" />
  <rect x={-18} y={-92} width={36} height={56} rx={12} fill={[TEAL, '#5C6BC0', ORANGE, '#26A69A'][k % 4]} stroke={OL} strokeWidth={3.5} />
  <path d={`M -16 -84 L -26 -50 M 16 -84 L ${30 + 4 * Math.sin(t * 3 + k)} -70`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
  <rect x={24} y={-90} width={22} height={30} rx={3} fill="#263238" stroke={OL} strokeWidth={2.5} /><rect x={27} y={-86} width={16} height={20} rx={2} fill={CY} opacity={0.7} />
  <circle cx={0} cy={-110} r={18} fill={['#F6CDA6', '#B97A4B', '#E0A878', '#F3D7BD'][k % 4]} stroke={OL} strokeWidth={3.5} />
  <path d="M -20 -112 Q 0 -146 20 -112 Z" fill={YEL} stroke={OL} strokeWidth={3.5} />
</g>;

const pulse = (on: boolean, t: number, x: number, y: number, w: number, h: number) => on ? <rect x={x - 10} y={y - 10} width={w + 20} height={h + 20} rx={18} fill="none" stroke={YEL} strokeWidth={8} strokeDasharray="22 12" strokeDashoffset={-t * 60} opacity={0.6 + 0.4 * Math.sin(t * 8)} /> : null;

export const AUTOMATION_SETS: Record<string, SetFn> = {
  /** the hypothetical automated factory (US brick shell or CN white mega-hall) */
  ohiobot: (t, z, f) => {
    const w = z.x1 - z.x0, cn = z.variant === 'cn', hi: string = z.hiAt ? pick(z.hiAt, t, z.hi) : z.hi, idle = clamp(kf(z.idle, t, 0)), sp = 1 - 0.85 * idle;
    const nArms = z.arms ?? 4, armX0 = z.armX ?? 200, armGap = z.armGap ?? 420, scanX = z.scanX ?? 1500, beltY = f - 150;
    const wall = cn ? '#F4F7FA' : BRICK;
    return <g>
      {sky(z, f, '#7CCBF2', '#E3F6FF', 'obsky' + Math.round(z.x0) + (cn ? 'c' : 'u'))}
      {[0, 1, 2].map((k) => cloud(((k * 820 + t * 12) % (w + 600)) + z.x0 - 300, 120 + (k % 2) * 70, 0.9, k))}
      {/* shell: back wall with tall day windows */}
      <rect x={z.x0} y={f - 760} width={w} height={760} fill={wall} />
      {!cn && Array.from({length: Math.ceil(w / 60)}, (_, r) => Array.from({length: 13}, (_, c) => <rect key={r + '-' + c} x={z.x0 + r * 60 + (c % 2) * 30} y={f - 760 + c * 58} width={58} height={4} fill="#8E3B2A" opacity={0.35} />))}
      {Array.from({length: Math.ceil(w / 380)}, (_, k) => { const wx = z.x0 + 80 + k * 380;
        return <g key={'win' + k}><rect x={wx} y={f - 700} width={260} height={cn ? 140 : 300} rx={cn ? 10 : 4} fill="#CFEFFF" stroke={OL} strokeWidth={5} />
          {!cn && <path d={`M ${wx + 130} ${f - 700} L ${wx + 130} ${f - 400} M ${wx} ${f - 550} L ${wx + 260} ${f - 550}`} stroke={OL} strokeWidth={4} />}
          {!cn && k === 1 && <g transform={`translate(${wx + 190} ${f - 470})`}><rect x={-8} y={0} width={16} height={60} fill="#78909C" /><ellipse cx={0} cy={-10} rx={46} ry={34} fill="#B0BEC5" stroke={OL} strokeWidth={3} /><T x={0} y={-2} s={16}>OHIO</T></g>}
          <path d={`M ${wx + 20} ${f - 700} L ${wx + 90} ${f - 700} L ${wx + 260} ${f} L ${wx + 120} ${f} Z`} fill="#FFF8D6" opacity={0.18} /></g>; })}
      {/* scheduler wall */}
      <g transform={`translate(${z.schedX ?? 900} ${f - 640})`}>
        <rect x={-300} y={-70} width={600} height={210} rx={14} fill="#12203A" stroke={OL} strokeWidth={6} />
        <T x={-280} y={-40} s={22} c={CY} a="start">{cn ? 'LINE SCHEDULER' : 'AI SCHEDULER'}</T>
        {[0, 1, 2, 3].map((r) => { const sh = z.schedAt !== undefined ? E.inOut(win(t, z.schedAt + r * 0.15, 0.8)) : 0, x0 = -270 + (rnd(r + 3) * 160) * (1 - sh) + (rnd(r + 7) * 160) * sh;
          return <g key={r}><rect x={-280} y={-20 + r * 38} width={560} height={28} rx={6} fill="#1E3557" />
            <rect x={x0} y={-18 + r * 38} width={140 + r * 30} height={24} rx={6} fill={[ORANGE, CY, GREEN, PURPLE][r]} stroke={OL} strokeWidth={2} /></g>; })}
        <rect x={-280 + ((t * 80) % 560)} y={-24} width={4} height={160} fill={YEL} />
        {pulse(hi === 'sched', t, -300, -70, 600, 210)}
      </g>
      {/* digital twin: cyan wireframe ghost of the line above */}
      {z.twinAt !== undefined && t >= z.twinAt && <g opacity={clamp((t - z.twinAt) / 0.8) * (0.75 + 0.2 * Math.sin(t * 3))} transform={`translate(0 ${-330 - 20 * (1 - clamp((t - z.twinAt) / 0.8))})`}>
        <rect x={z.x0 + 100} y={beltY - 6} width={w - 200} height={20} fill="none" stroke={CY} strokeWidth={3} strokeDasharray="10 8" />
        {Array.from({length: nArms}, (_, k) => <g key={'tw' + k} transform={`translate(${armX0 + k * armGap} ${beltY - 4})`} opacity={0.9}><g style={{filter: 'none'}}>{arm6(t + 0.6, k, 0.6, sp, CY)}</g></g>)}
        <rect x={z.x0 + 100} y={beltY - 240} width={w - 200} height={250} fill={CY} opacity={0.06} />
        <T x={(z.twinX ?? 900)} y={beltY - 250} s={30} c={CY}>DIGITAL TWIN · VIRTUAL COPY</T>
      </g>}
      {/* floor */}
      <rect x={z.x0} y={f} width={w} height={700} fill={cn ? '#DCE3EA' : '#C9D3DB'} />
      <rect x={z.x0} y={f} width={w} height={16} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <path key={'ln' + k} d={`M ${z.x0 + k * 300} ${f + 70} L ${z.x0 + k * 300 + 160} ${f + 70}`} stroke={YEL} strokeWidth={8} strokeLinecap="round" opacity={0.8} />)}
      {/* conveyor with toasters */}
      <rect x={z.x0} y={beltY} width={w} height={26} fill="#455A64" stroke={OL} strokeWidth={4} />
      <path d={`M ${z.x0} ${beltY + 26} L ${z.x0} ${f} M ${z.x1} ${beltY + 26} L ${z.x1} ${f}`} stroke={OL} strokeWidth={6} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <rect key={'lg' + k} x={z.x0 + k * 260 + 40} y={beltY + 26} width={16} height={f - beltY - 26} fill="#607D8B" stroke={OL} strokeWidth={3} />)}
      {Array.from({length: Math.ceil(w / 220)}, (_, q) => { const px = z.x0 + (((q * 220 + t * 110 * sp) % w) + w) % w;
        return <g key={'ts' + q} transform={`translate(${px} ${beltY - 26})`}>{toaster(t, q, 1, px > scanX ? 1 : 0)}</g>; })}
      {/* robot arm cells */}
      {Array.from({length: nArms}, (_, k) => { const ax = armX0 + k * armGap, on = hi === 'arms';
        return <g key={'arm' + k} transform={`translate(${ax} ${f})`}>
          <rect x={-110} y={-6} width={220} height={10} fill={YEL} stroke={OL} strokeWidth={2} />
          {arm6(t, k, 1.25, sp, cn ? (k % 2 ? TEAL : ORANGE) : (k % 2 ? ORANGE : CY), z.sparks !== false && k % 2 === 0 && idle < 0.5)}
          {idle > 0.3 && <g transform="translate(0 -380)"><circle r={18} fill={Math.floor(t * 2) % 2 ? ORANGE : '#FFE0B2'} stroke={OL} strokeWidth={3} /><T x={0} y={-30} s={22} c={OL}>IDLE</T></g>}
          {on && pulse(true, t, -120, -330, 240, 330)}
        </g>; })}
      {/* scan gantry (machine vision) */}
      <g transform={`translate(${scanX} ${beltY})`}>
        <path d="M -90 26 L -90 -210 L 90 -210 L 90 26" fill="none" stroke={OL} strokeWidth={22} strokeLinejoin="round" /><path d="M -90 26 L -90 -210 L 90 -210 L 90 26" fill="none" stroke={CHROME} strokeWidth={13} strokeLinejoin="round" />
        <rect x={-34} y={-232} width={68} height={40} rx={10} fill="#263238" stroke={OL} strokeWidth={4} /><circle cx={0} cy={-200} r={10} fill={CY} />
        {(() => { const u = (t * 1.3) % 1; return <path d={`M 0 -196 L ${-60 + 120 * u - 30} -6 L ${-60 + 120 * u + 30} -6 Z`} fill={CY} opacity={0.28} />; })()}
        {Math.sin(t * 2.6) > 0.6 && <g transform="translate(120 -150)"><circle r={24} fill={GREEN} stroke={OL} strokeWidth={4} /><path d="M -10 0 L -2 9 L 12 -10" stroke="#FFFFFF" strokeWidth={6} fill="none" strokeLinecap="round" /></g>}
        <rect x={-80} y={-276} width={160} height={34} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-252} s={20}>VISION CHECK</T>
        {pulse(hi === 'vision', t, -110, -290, 220, 320)}
      </g>
      {/* predictive maintenance motor */}
      {z.maintAt !== undefined && <g transform={`translate(${z.maintX ?? armX0 + armGap} ${f - 30})`}>
        <rect x={-60} y={-60} width={120} height={70} rx={14} fill="#546E7A" stroke={OL} strokeWidth={4} /><circle cx={0} cy={-25} r={22} fill={CHROME} stroke={OL} strokeWidth={3} />
        <path d={`M 0 -25 L ${22 * Math.cos(t * 12)} ${-25 + 22 * Math.sin(t * 12)}`} stroke={OL} strokeWidth={4} />
        {t >= z.maintAt && [0, 1, 2].map((q) => { const u = ((t - z.maintAt) * 0.9 + q / 3) % 1; return <circle key={q} cx={0} cy={-25} r={30 + u * 110} fill="none" stroke={ORANGE} strokeWidth={5} opacity={1 - u} />; })}
        {t >= z.maintAt + 1.2 && <g transform={`translate(0 -190) scale(${pop(t, z.maintAt + 1.2)})`}><rect x={-120} y={-30} width={240} height={52} rx={10} fill={YEL} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={24}>FIX IN 3 DAYS</T></g>}
        {pulse(hi === 'maint', t, -70, -70, 140, 90)}
      </g>}
      {/* self-driving carts */}
      {Array.from({length: z.carts ?? 3}, (_, k) => { const span = w + 400, u = ((t * (0.07 + k * 0.012) + k / 3) % 1), cx = z.x0 - 200 + u * span, dir = k % 2 ? -1 : 1;
        return <g key={'ct' + k} transform={`translate(${dir > 0 ? cx : z.x1 + z.x0 - cx} ${f + 150 + k * 60})`}>{cart(t, k, ['PARTS', 'CHIPS', 'MOTORS'][k % 3])}{hi === 'carts' && pulse(true, t, -80, -96, 160, 110)}</g>; })}
      {/* CN variant: supplier trucks at the dock (suppliers down the street) */}
      {cn && [0, 1].map((q) => { const tx = z.x1 - 300 - ((t * 60 + q * 500) % 900);
        return <g key={'tk' + q} transform={`translate(${tx} ${f + 400})`}><rect x={-120} y={-90} width={180} height={80} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={-30} y={-42} s={18}>SUPPLIER</T>
          <path d="M 60 -10 L 60 -80 L 110 -80 L 130 -40 L 130 -10 Z" fill={[TEAL, ORANGE][q]} stroke={OL} strokeWidth={4} />
          {[-80, 20, 100].map((wx) => <circle key={wx} cx={wx} cy={-6} r={16} fill="#263238" stroke={OL} strokeWidth={3} />)}</g>; })}
      {/* one technician (few people) */}
      {tech(z.techX ?? (cn ? 1300 : 1150), f + 40, 1.1, 1, t)}
      {z.hyp && (z.hypUntil === undefined || t < z.hypUntil) && banner(z.hypX ?? 960, z.hypY ?? 80, 'HYPOTHETICAL FACTORY', RED, 30)}
    </g>;
  },

  /** the glass COST BOX: slices fill it, one is pulled out by a crane, robots drop into the gap */
  billbox: (t, z, f) => {
    const w = z.x1 - z.x0, bx = z.boxX ?? 960, bw = 520, bh = 560, by = f - 90, slices: any[] = z.slices || [];
    const pullAt = z.pullAt ?? 1e9, pullIdx = z.pullIdx ?? 1, pu = E.inOut(win(t, pullAt, 1.6)), rAt = z.robotAt ?? 1e9;
    let acc = 0;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#F3EEE6" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 200} y={-200} width={100} height={f + 200} fill="#EDE5D8" />)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B89B7A" /><rect x={z.x0} y={f} width={w} height={16} fill="#9C7E5C" stroke={OL} strokeWidth={4} />
      {z.title && <g transform={`translate(${bx} ${by - bh - 120})`}><rect x={-420} y={-44} width={840} height={70} rx={12} fill="#12203A" stroke={OL} strokeWidth={5} /><T x={0} y={4} s={fit(z.title, 800, 34)} c={YEL}>{z.title}</T></g>}
      {/* crane rail + hook */}
      <rect x={z.x0} y={by - bh - 260} width={w} height={20} fill="#FFC93C" stroke={OL} strokeWidth={4} />
      {/* slices stacked bottom-up */}
      {slices.map((s, k) => { const [at, label, share, color] = s, h = (share / 100) * bh, y0 = by - acc - h; acc += h;
        if (t < at) return null;
        const drop = 1 - E.outBack(win(t, at, 0.6)), isP = k === pullIdx, lift = isP ? pu : 0;
        const dx = isP ? 620 * lift : 0, dy = isP ? -(bh + 120) * Math.min(1, lift * 1.6) + 200 * Math.max(0, lift - 0.6) : -300 * drop;
        return <g key={'sl' + k} transform={`translate(${dx} ${dy})`}>
          <rect x={bx - bw / 2 + 12} y={y0 + 4} width={bw - 24} height={h - 8} rx={10} fill={color} stroke={OL} strokeWidth={4} />
          <T x={bx} y={y0 + h / 2 + 4} s={fit(label, bw - 60, Math.min(34, h * 0.45))} c="#FFFFFF" st={OL} sw={5}>{label}</T>
          {isP && lift > 0.02 && <path d={`M ${bx} ${y0 + 4} L ${bx} ${by - bh - 240}`} stroke={OL} strokeWidth={5} />}
        </g>; })}
      {t >= rAt && (() => { const s = slices[pullIdx]; if (!s) return null; let off = 0; for (let k = 0; k < pullIdx; k++) off += (slices[k][2] / 100) * bh;
        const h = (s[2] / 100) * bh * (z.robotShare ?? 0.55), y0 = by - off - h, d = 1 - E.outBack(win(t, rAt, 0.6));
        return <g transform={`translate(0 ${-400 * d})`}><rect x={bx - bw / 2 + 12} y={y0 + 4} width={bw - 24} height={h - 8} rx={10} fill={CY} stroke={OL} strokeWidth={4} strokeDasharray="14 8" />
          <T x={bx} y={y0 + h / 2 + 4} s={Math.min(26, h * 0.5)} c={OL}>ROBOTS + SOFTWARE</T></g>; })()}
      {/* glass box */}
      <rect x={bx - bw / 2} y={by - bh} width={bw} height={bh} rx={12} fill="#BFE6FF" opacity={0.18} stroke={OL} strokeWidth={6} />
      <path d={`M ${bx - bw / 2 + 30} ${by - bh + 30} L ${bx - bw / 2 + 90} ${by - bh + 30} M ${bx - bw / 2 + 30} ${by - bh + 50} L ${bx - bw / 2 + 60} ${by - bh + 50}`} stroke="#FFFFFF" strokeWidth={6} strokeLinecap="round" opacity={0.8} />
      <T x={bx} y={by + 50} s={26} c={OL}>{z.boxLabel || '$1 OF FACTORY SHIPMENTS'}</T>
      {z.note && t >= (z.noteAt ?? 0) && <T x={bx} y={by + 90} s={20} c="#5D4037">{z.note}</T>}
    </g>;
  },

  /** the THREE-FACTORY lab */
  toastlab: (t, z, f) => {
    const w = z.x1 - z.x0, cols: any[] = z.cols || [], sc = z.scale ?? 5, base = f - 30, gap = z.gap ?? 430, cx0 = z.colX ?? 430;
    const tot = (c: any) => (c.blocks || []).reduce((s: number, b: any) => s + kf(b.v, t, 0), 0);
    const vis = cols.map((c, k) => ({k, on: t >= (c.at ?? 0), v: tot(c)})).filter((o) => o.on);
    const judged = z.judgeAt !== undefined && t >= z.judgeAt && vis.length > 1, best = judged ? vis.reduce((a, b) => (b.v < a.v ? b : a)).k : -1;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E9F1F7" />
      {/* lab wall: chalkboard, pipes, retro gauges */}
      <rect x={z.x0} y={f - 900} width={w} height={60} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 340)}, (_, k) => <g key={'pp' + k}><path d={`M ${z.x0 + k * 340} ${f - 820} q 80 -40 170 0 t 170 0`} stroke={CHROME2} strokeWidth={14} fill="none" /><circle cx={z.x0 + k * 340 + 170} cy={f - 820} r={14} fill={k % 2 ? ORANGE : CY} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#CFD8DC" /><rect x={z.x0} y={f} width={w} height={16} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {banner(z.bannerX ?? 960, f - 760, 'ILLUSTRATIVE MODEL · OUR ASSUMPTIONS · NOT REAL COMPANY COSTS', '#5C6BC0', 24)}
      {/* $ scale ruler */}
      <g transform={`translate(${cx0 - 210} 0)`}>{[0, 20, 40, 60, 80, 100, 120].map((v) => <g key={v}><path d={`M 0 ${base - v * sc} L 24 ${base - v * sc}`} stroke={OL} strokeWidth={3} /><T x={-8} y={base - v * sc + 7} s={18} a="end" c="#455A64">{`$${v}`}</T></g>)}
        <path d={`M 12 ${base} L 12 ${base - 120 * sc}`} stroke={OL} strokeWidth={3} />
        <path d={`M -20 ${base - 100 * sc} L ${gap * cols.length + 200} ${base - 100 * sc}`} stroke={RED} strokeWidth={3} strokeDasharray="12 10" opacity={0.6} /></g>
      {cols.map((c, k) => { if (t < (c.at ?? 0)) return null; const x = cx0 + k * gap, bw = 240; let acc = 0; const v = tot(c), win_ = k === best;
        return <g key={'col' + k} transform={`translate(${x} 0) scale(${pop(t, c.at ?? 0, 0.5)} 1)`}>
          {(c.blocks || []).map((b: any, q: number) => { const bv = kf(b.v, t, 0), h = bv * sc, y = base - acc - h; acc += h; if (bv <= 0.05) return null;
            const sAt = b.at ?? ((c.at ?? 0) + q * 0.18); if (t < sAt) return null; const d = 1 - E.outBack(win(t, sAt, 0.45));
            return <g key={q} transform={`translate(0 ${-260 * d})`}><rect x={-bw / 2} y={y} width={bw} height={Math.max(2, h - 2)} rx={6} fill={b.color || TEAL} stroke={OL} strokeWidth={3} />
              {h > 20 && <T x={0} y={y + h / 2 + Math.min(16, h * 0.35) * 0.36} s={Math.min(18, h * 0.6)} c="#FFFFFF" st={OL} sw={4}>{`${b.label} ${Math.round(bv)}`}</T>}</g>; })}
          {/* nameplate and total */}
          <rect x={-150} y={base + 22} width={300} height={70} rx={12} fill={c.color || '#FFFFFF'} stroke={OL} strokeWidth={4} />
          <T x={0} y={base + 52} s={fit(c.name, 280, 24)} c="#FFFFFF" st={OL} sw={4}>{c.name}</T>
          {c.sub && <T x={0} y={base + 80} s={fit(c.sub, 280, 16)} c="#FFFFFF">{c.sub}</T>}
          <g transform={`translate(0 ${base - acc - 60})`}><rect x={-90} y={-34} width={180} height={56} rx={28} fill={win_ ? YEL : '#FFFFFF'} stroke={OL} strokeWidth={4} /><T x={0} y={6} s={30}>{`≈ $${Math.round(v)}`}</T></g>
          {win_ && <g transform={`translate(0 ${base - acc - 140}) scale(${pop(t, z.judgeAt, 0.5)})`}><path d="M -50 20 L -60 -30 L -25 -5 L 0 -45 L 25 -5 L 60 -30 L 50 20 Z" fill={YEL} stroke={OL} strokeWidth={4} strokeLinejoin="round" /><T x={0} y={50} s={22} c={GREEN}>CHEAPEST</T></g>}
        </g>; })}
      {/* knobs */}
      {(z.knobs || []).map((kb: any, k: number) => { if (t < (kb.at ?? 0)) return null; const v = kf(kb.v, t, 0), mx = kb.max ?? 100, an = -130 + 260 * clamp(v / mx), kx = z.knobX ?? 1740, ky = f - 600 + k * 240;
        return <g key={'kb' + k} transform={`translate(${kx} ${ky}) scale(${pop(t, kb.at ?? 0)})`}>
          <rect x={-120} y={-100} width={240} height={200} rx={20} fill="#263238" stroke={OL} strokeWidth={5} />
          <path d="M -70 30 A 80 80 0 1 1 70 30" stroke="#455A64" strokeWidth={14} fill="none" strokeLinecap="round" />
          <circle cx={0} cy={0} r={46} fill={CHROME} stroke={OL} strokeWidth={4} />
          <path d={`M 0 0 L ${Math.sin((an * Math.PI) / 180) * 40} ${-Math.cos((an * Math.PI) / 180) * 40}`} stroke={RED} strokeWidth={8} strokeLinecap="round" />
          <T x={0} y={-62} s={fit(kb.label, 210, 20)} c={CY}>{kb.label}</T>
          <T x={0} y={84} s={28} c="#FFFFFF">{`${Math.round(v)}${kb.unit ?? '%'}`}</T></g>; })}
    </g>;
  },

  /** robot towers per country, filled by a dispenser */
  robotrace: (t, z, f) => {
    const w = z.x1 - z.x0, rows: any[] = z.rows || [], mx = z.max ?? 100, H = z.h ?? 560, gap = z.gap ?? 300, x0 = z.colX ?? (960 - ((rows.length - 1) * gap) / 2);
    return <g>
      {sky(z, f, '#86D0F5', '#E8F7FF', 'rrsky' + Math.round(z.x0))}
      <rect x={z.x0} y={f - 980} width={w} height={980} fill="#F7F3EA" />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <circle key={'bulb' + k} cx={z.x0 + k * 160 + 80} cy={f - 940} r={12} fill={Math.floor(t * 3 + k) % 3 ? YEL : '#FFFFFF'} stroke={OL} strokeWidth={3} />)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#9FB3C8" /><rect x={z.x0} y={f} width={w} height={16} fill="#7E94AB" stroke={OL} strokeWidth={4} />
      {z.title && <g transform={`translate(${z.titleX ?? 960} ${f - 720})`}><rect x={-560} y={-44} width={1120} height={70} rx={14} fill="#12203A" stroke={OL} strokeWidth={5} /><T x={0} y={4} s={fit(z.title, 1080, 32)} c={YEL}>{z.title}</T></g>}
      {/* dispenser pipe across the top */}
      <rect x={x0 - 200} y={f - 650} width={gap * rows.length + 100} height={30} rx={15} fill={CHROME} stroke={OL} strokeWidth={4} />
      {rows.map((r, k) => { const x = x0 + k * gap, at = r.at ?? 0, u = E.out(win(t, at, 1.4)), hh = (r.value / mx) * H * u, on = z.hi === k, tok = 34;
        const n = Math.floor(hh / tok);
        return <g key={'rr' + k}>
          <rect x={x - 16} y={f - 625} width={32} height={40} fill={CHROME2} stroke={OL} strokeWidth={3} />
          {t >= at && u < 1 && [0, 1, 2].map((q) => { const v = ((t * 2.4 + q / 3) % 1); return <g key={q} transform={`translate(${x} ${f - 585 + v * (585 - hh)})`}><rect x={-12} y={-12} width={24} height={24} rx={6} fill={r.color || ORANGE} stroke={OL} strokeWidth={2.5} /></g>; })}
          {/* tower of robot tokens */}
          {Array.from({length: n}, (_, q) => <g key={q} transform={`translate(${x} ${f - 4 - q * tok})`}><rect x={-60} y={-tok + 3} width={120} height={tok - 4} rx={8} fill={r.color || ORANGE} stroke={OL} strokeWidth={3} />
            <circle cx={-30} cy={-tok / 2} r={5} fill="#FFFFFF" /><circle cx={30} cy={-tok / 2} r={5} fill="#FFFFFF" /><path d={`M -10 ${-tok / 2 + 4} L 10 ${-tok / 2 + 4}`} stroke={OL} strokeWidth={3} /></g>)}
          {hh - n * tok > 1 && <rect x={-60 + x} y={f - 4 - hh + 2} width={120} height={hh - n * tok} rx={6} fill={r.color || ORANGE} stroke={OL} strokeWidth={3} opacity={0.8} />}
          {on && pulse(true, t, x - 70, f - hh - 14, 140, hh + 14)}
          {t >= at && <g transform={`translate(${x} ${f - hh - 40}) scale(${pop(t, at + 0.9)})`}><rect x={-110} y={-30} width={220} height={48} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={fit(r.display || String(r.value), 200, 28)}>{r.display || String(r.value)}</T></g>}
          <rect x={x - 120} y={f + 26} width={240} height={56} rx={12} fill={r.color || ORANGE} stroke={OL} strokeWidth={4} />
          <T x={x} y={f + 64} s={fit(r.name, 220, 26)} c="#FFFFFF" st={OL} sw={4}>{r.name}</T>
        </g>; })}
      {z.foot && <T x={z.titleX ?? 960} y={f + 140} s={22} c={OL}>{z.foot}</T>}
    </g>;
  },

  /** the Ohio plant in the middle of a web of imported parts */
  chainweb: (t, z, f) => {
    const w = z.x1 - z.x0, px = z.plantX ?? 960, py = f - 60, srcs: any[] = z.srcs || [];
    return <g>
      {sky(z, f, '#7CCBF2', '#E6F7FF', 'cwsky' + Math.round(z.x0))}
      {[0, 1].map((k) => cloud(((k * 900 + t * 10) % (w + 600)) + z.x0 - 300, 110 + k * 60, 0.9, k))}
      <rect x={z.x0} y={f - 380} width={w} height={1100} fill="#4FA3D9" />
      {Array.from({length: 18}, (_, k) => <path key={'wv' + k} d={`M ${z.x0 + k * 260 + ((t * 26) % 260)} ${f - 330 + (k % 4) * 90} q 22 -12 44 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.5} />)}
      {/* home island with the plant */}
      <path d={`M ${px - 420} ${py + 60} Q ${px - 380} ${py - 120} ${px} ${py - 130} Q ${px + 380} ${py - 120} ${px + 420} ${py + 60} Z`} fill="#A9D18E" stroke={OL} strokeWidth={5} />
      <g transform={`translate(${px} ${py - 80})`}>
        <path d="M -200 0 L -200 -200 L -120 -250 L -120 -200 L -40 -250 L -40 -200 L 40 -250 L 40 -200 L 200 -200 L 200 0 Z" fill={BRICK} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        {[-140, -60, 20, 100].map((q) => <rect key={q} x={q} y={-160} width={56} height={70} rx={4} fill="#CFEFFF" stroke={OL} strokeWidth={3} />)}
        <rect x={-170} y={-60} width={340} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-30} s={24}>{z.plantName || 'MADE IN OHIO*'}</T>
        <g transform="translate(150 -250) scale(0.5)">{arm6(t, 1, 1, 1, ORANGE)}</g>
      </g>
      <T x={px} y={py + 110} s={22} c="#FFFFFF" st={OL} sw={5}>{z.foot || '*WITH PARTS FROM EVERYWHERE'}</T>
      {/* depots + routes */}
      {srcs.map((s, k) => { if (t < (s.at ?? 0)) return null; const sx = s.x, sy = s.y, cut = z.cutIdx === k && t >= (z.cutAt ?? 1e9), mx = (sx + px) / 2, my = Math.min(sy, py) - 220;
        const d = `M ${sx} ${sy} Q ${mx} ${my} ${px} ${py - 200}`, grow = E.out(win(t, s.at ?? 0, 0.9));
        return <g key={'src' + k}>
          <path d={d} stroke={cut ? RED : '#FFFFFF'} strokeWidth={7} fill="none" strokeDasharray="20 14" strokeDashoffset={-t * 60} opacity={0.9} pathLength={1000} style={{}} />
          {!cut && grow >= 1 && [0, 1].map((q) => { const u = ((t * 0.35 + q / 2 + k * 0.13) % 1), bx = (1 - u) * (1 - u) * sx + 2 * (1 - u) * u * mx + u * u * px, by = (1 - u) * (1 - u) * sy + 2 * (1 - u) * u * my + u * u * (py - 200);
            return <g key={q} transform={`translate(${bx} ${by})`}><rect x={-26} y={-18} width={52} height={36} rx={5} fill="#D7A86E" stroke={OL} strokeWidth={3} /></g>; })}
          {cut && <g transform={`translate(${mx} ${my + 110}) scale(${pop(t, z.cutAt)})`}><circle r={40} fill={RED} stroke={OL} strokeWidth={4} /><path d="M -18 -18 L 18 18 M 18 -18 L -18 18" stroke="#FFFFFF" strokeWidth={8} strokeLinecap="round" /></g>}
          <g transform={`translate(${sx} ${sy}) scale(${pop(t, s.at ?? 0)})`}>
            <ellipse cx={0} cy={30} rx={150} ry={36} fill="#C5E1A5" stroke={OL} strokeWidth={4} />
            <rect x={-110} y={-70} width={220} height={90} rx={12} fill={s.color || '#FFFFFF'} stroke={OL} strokeWidth={4} />
            <T x={0} y={-30} s={fit(s.label, 200, 26)} c="#FFFFFF" st={OL} sw={5}>{s.label}</T>
            {s.from && <T x={0} y={6} s={fit(s.from, 200, 18)} c="#FFFFFF">{s.from}</T>}
          </g>
        </g>; })}
    </g>;
  },

  /** one $100 coin pours into channels and buckets */
  moneyriver: (t, z, f) => {
    const w = z.x1 - z.x0, bk: any[] = z.buckets || [], gap = z.gap ?? 230, x0 = z.bx0 ?? (960 - ((bk.length - 1) * gap) / 2), cy = f - 720, bucketY = f - 40;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#F2F7EE" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'gr' + k} d={`M ${z.x0 + k * 120} ${f - 1000} L ${z.x0 + k * 120} ${f}`} stroke="#E1EBD9" strokeWidth={3} />)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#A8C98E" /><rect x={z.x0} y={f} width={w} height={16} fill="#8DB36F" stroke={OL} strokeWidth={4} />
      {banner(z.bannerX ?? 1500, f - 900, 'ILLUSTRATIVE SPLIT · NOT MEASURED', '#5C6BC0', 22)}
      {/* the coin */}
      <g transform={`translate(${z.coinX ?? 960} ${cy}) rotate(${Math.sin(t * 2) * 6})`}>
        <circle r={96} fill={YEL} stroke={OL} strokeWidth={6} /><circle r={74} fill="none" stroke="#E0A800" strokeWidth={6} />
        <T x={0} y={16} s={50}>$100</T><T x={0} y={-114} s={22} c={OL}>ONE TOASTER SALE</T>
      </g>
      {/* channels */}
      {bk.map((b, k) => { if (t < (b.at ?? 0)) return null; const bx = x0 + k * gap, g = E.out(win(t, b.at ?? 0, 0.8)), lvl = clamp(kf(b.level, t, 0.5)) * E.out(win(t, (b.at ?? 0) + 0.5, 1.2));
        const d = `M ${z.coinX ?? 960} ${cy + 100} C ${z.coinX ?? 960} ${cy + 300} ${bx} ${cy + 260} ${bx} ${bucketY - 230}`;
        const owner = z.ownerAt !== undefined && k === bk.length - 1 && t >= z.ownerAt;
        return <g key={'bk' + k}>
          <path d={d} stroke={OL} strokeWidth={20} fill="none" opacity={g} /><path d={d} stroke={b.color || CY} strokeWidth={12} fill="none" opacity={g} strokeDasharray="24 16" strokeDashoffset={-t * 120} />
          <g transform={`translate(${bx} ${bucketY})`}>
            <path d="M -90 -220 L 90 -220 L 70 0 L -70 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
            <clipPath id={`mrc${k}`}><path d="M -90 -220 L 90 -220 L 70 0 L -70 0 Z" /></clipPath>
            <g clipPath={`url(#mrc${k})`}><rect x={-100} y={-220 * lvl} width={200} height={240} fill={b.color || CY} opacity={0.85} />
              <path d={`M -100 ${-220 * lvl} q 25 ${-8 * Math.sin(t * 4 + k)} 50 0 t 50 0 t 50 0 t 50 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" /></g>
            <rect x={-104} y={18} width={208} height={66} rx={12} fill={owner ? YEL : '#FFFFFF'} stroke={OL} strokeWidth={4} />
            <T x={0} y={58} s={fit(b.label, 190, 20)}>{b.label}</T>
            {owner && <g transform={`translate(0 -270) scale(${pop(t, z.ownerAt)})`}><rect x={-90} y={-26} width={180} height={42} rx={10} fill={GREEN} stroke={OL} strokeWidth={3} /><T x={0} y={4} s={20} c="#FFFFFF">WHAT'S LEFT</T></g>}
          </g></g>; })}
    </g>;
  },

  /** show title card: a chrome arm writes the title */
  aititle: (t, z, f) => {
    const lines: string[] = z.lines || ['CHEAPER THAN', 'CHINA?'], sub = pick(z.subs, t, z.sub || '');
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#0E2A4A" />
      {Array.from({length: 18}, (_, k) => <path key={'ry' + k} d={`M 960 540 L ${960 + Math.cos(k / 18 * Math.PI * 2 + t * 0.15) * 1600} ${540 + Math.sin(k / 18 * Math.PI * 2 + t * 0.15) * 1600} L ${960 + Math.cos((k + 0.5) / 18 * Math.PI * 2 + t * 0.15) * 1600} ${540 + Math.sin((k + 0.5) / 18 * Math.PI * 2 + t * 0.15) * 1600} Z`} fill={k % 2 ? '#14365E' : '#0E2A4A'} />)}
      {/* circuit traces */}
      {Array.from({length: 10}, (_, k) => <path key={'tr' + k} d={`M ${-100 + k * 220} 1100 L ${-100 + k * 220} ${980 - (k % 3) * 60} L ${20 + k * 220} ${900 - (k % 3) * 60}`} stroke={CY} strokeWidth={5} fill="none" opacity={0.5} strokeDasharray="30 20" strokeDashoffset={-t * 80} />)}
      {lines.map((ln, k) => { const at = 0.3 + k * 0.8, n = Math.floor(clamp((t - at) / 0.6) * ln.length);
        return <T key={k} x={960} y={400 + k * 150} s={fit(ln, 1500, 140)} c={k === lines.length - 1 ? YEL : '#FFFFFF'} st={OL} sw={14}>{ln.slice(0, n)}</T>; })}
      <g transform={`translate(${1500 + 80 * Math.sin(t * 3)} 1080)`}>{arm6(t * 2, 0, 1.6, 1.4, ORANGE, true)}</g>
      {sub && <g transform="translate(960 760)"><rect x={-620} y={-40} width={1240} height={64} rx={32} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={4} s={fit(sub, 1180, 32)}>{sub}</T></g>}
      <T x={960} y={140} s={34} c={CY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** act bumper: circuit-board wipe, TORQ stamps the act number */
  aibumper: (t, z, f) => {
    const c = z.color || CY, wipe = E.inOut(win(t, 0, 0.5));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#F4F8FC" />
      <rect x={-200} y={-200} width={2400 * wipe} height={1500} fill={c} />
      {Array.from({length: 14}, (_, k) => <path key={'cb' + k} d={`M -100 ${80 + k * 75} L ${300 + rnd(k) * 600} ${80 + k * 75} L ${360 + rnd(k) * 600} ${120 + k * 75} L 2100 ${120 + k * 75}`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.25 * wipe} />)}
      <g transform={`translate(560 470) scale(${pop(t, 0.9, 0.5)}) rotate(${-8 + 3 * Math.sin(t * 4)})`}>
        <circle r={160} fill="#FFFFFF" stroke={OL} strokeWidth={8} /><circle r={128} fill="none" stroke={c} strokeWidth={10} strokeDasharray="20 12" />
        <T x={0} y={-40} s={34} c={OL}>{z.act || 'ACT ONE'}</T><T x={0} y={80} s={130} c={c} st={OL} sw={8}>{z.num || '1'}</T></g>
      <g transform={`translate(1240 ${470 - 20 * pop(t, 1.2)})`}>
        <rect x={-560} y={-90} width={1120} height={130} rx={20} fill="#12203A" stroke={OL} strokeWidth={6} />
        <T x={0} y={0} s={fit(z.title || '', 1060, 58)} c="#FFFFFF">{z.title || ''}</T></g>
      {t >= 1.6 && <T x={1240} y={640} s={fit(z.caption || '', 1100, 34)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.6) / 0.3)}>{z.caption || ''}</T>}
    </g>;
  },
};

/** TORQ: an original one-armed factory robot on wheels with a screen face (running gag: wants to be a humanoid) */
const torq: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, moving = Math.abs(vx) > 20, dir = a.flip ? -1 : vx < -20 ? -1 : 1;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.5) hy += Math.sin((u / 0.5) * Math.PI) * 80; }
  const face: string = pick(a.faces, t, a.face || 'happy'), legs = a.legs && (a.legsFallAt === undefined || t < a.legsFallAt + 0.6), fall = a.legsFallAt !== undefined ? clamp((t - a.legsFallAt) / 0.6) : 0;
  const lift = legs ? 120 * (1 - E.in(fall)) : 0, sq = 1 + 0.06 * Math.sin(t * 6 + i), stamp = a.stampAt !== undefined && t >= a.stampAt && t < a.stampAt + 0.4;
  const pa = a.point ? -60 : -20 + 25 * Math.sin(t * 2.4 + i);
  return <g key={'tq' + i} transform={`translate(${x} ${y - hy}) scale(${s * dir} ${s})`}>
    <ellipse cx={0} cy={4 + hy} rx={80} ry={12} fill={OL} opacity={0.18} />
    {legs && <g opacity={1 - fall}>{[-30, 30].map((q, k) => <g key={k} transform={`rotate(${fall * (k ? 40 : -40)} ${q} -10)`}><rect x={q - 14} y={-130} width={28} height={130} fill="#D7A86E" stroke={OL} strokeWidth={4} /><rect x={q - 22} y={-12} width={44} height={14} rx={4} fill="#A9783F" stroke={OL} strokeWidth={3} /></g>)}
      <T x={0} y={-60} s={14} c={OL} o={0.8}>LEGS (CARDBOARD)</T></g>}
    <g transform={`translate(0 ${-lift})`}>
      {[-46, 46].map((q) => <g key={q} transform={`translate(${q} -18) rotate(${moving ? t * 400 : 0})`}><circle r={18} fill="#263238" stroke={OL} strokeWidth={4} /><path d="M -10 0 L 10 0" stroke={CHROME2} strokeWidth={4} /></g>)}
      <g transform={`scale(${1 / sq} ${sq})`}>
        <rect x={-70} y={-150} width={140} height={120} rx={30} fill={ORANGE} stroke={OL} strokeWidth={5} />
        <rect x={-50} y={-136} width={100} height={20} rx={10} fill="#FFFFFF" opacity={0.4} />
        <rect x={-14} y={-176} width={28} height={30} fill={CHROME2} stroke={OL} strokeWidth={4} />
        <g transform="translate(0 -236)">
          <rect x={-74} y={-56} width={148} height={104} rx={24} fill={CHROME} stroke={OL} strokeWidth={5} />
          <rect x={-60} y={-44} width={120} height={80} rx={14} fill="#12203A" />
          {face === 'shock' ? <g><circle cx={-24} cy={-10} r={14} fill={CY} /><circle cx={24} cy={-10} r={14} fill={CY} /><ellipse cx={0} cy={20} rx={10} ry={8} fill={CY} /></g>
            : face === 'worry' || face === 'sad' ? <g><path d="M -36 -18 L -14 -8 M 36 -18 L 14 -8" stroke={CY} strokeWidth={6} strokeLinecap="round" /><path d="M -18 22 Q 0 10 18 22" stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" /></g>
            : face === 'smug' ? <g><path d="M -36 -10 L -12 -10 M 12 -10 L 36 -10" stroke={CY} strokeWidth={7} strokeLinecap="round" /><path d="M -18 14 Q 4 26 22 10" stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" /></g>
            : <g>{(((t + i) % 3) < 0.12) ? <path d="M -34 -10 L -14 -10 M 14 -10 L 34 -10" stroke={CY} strokeWidth={6} /> : <g><circle cx={-24} cy={-10} r={10} fill={CY} /><circle cx={24} cy={-10} r={10} fill={CY} /></g>}<path d="M -20 12 Q 0 28 20 12" stroke={CY} strokeWidth={6} fill="none" strokeLinecap="round" /></g>}
          <path d="M 0 -56 L 0 -84" stroke={OL} strokeWidth={5} /><circle cx={0} cy={-90} r={10} fill={Math.floor(t * 2) % 2 ? RED : YEL} stroke={OL} strokeWidth={3} />
        </g>
        {/* the one arm */}
        <g transform={`translate(64 -110) rotate(${stamp ? 60 : pa})`}>
          <path d="M 0 0 L 90 0" stroke={OL} strokeWidth={26} strokeLinecap="round" /><path d="M 0 0 L 90 0" stroke={CHROME} strokeWidth={16} strokeLinecap="round" />
          <circle cx={0} cy={0} r={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
          <g transform="translate(96 0)"><path d="M 0 -10 L 22 -18 M 0 10 L 22 18" stroke={OL} strokeWidth={7} strokeLinecap="round" /></g>
        </g>
        <rect x={-50} y={-70} width={100} height={26} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-51} s={18}>TORQ</T>
      </g>
    </g>
  </g>;
};

/** a PROTOTYPE humanoid robot on a test stand (demo, not deployment) */
const humanoid: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45), dance = a.dance && (a.fallAt === undefined || t < a.fallAt);
  const fall = a.fallAt !== undefined ? E.in(clamp((t - a.fallAt) / 0.7)) : 0, wob = a.wobbleAt !== undefined && t >= a.wobbleAt ? 8 * Math.sin(t * 14) : 0;
  const sw = dance ? Math.sin(t * 6) : 0;
  return <g key={'hu' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-150} y={-20} width={300} height={24} rx={6} fill="#455A64" stroke={OL} strokeWidth={4} />
    <path d="M -120 -20 L -120 -520 M 120 -20 L 120 -520 M -120 -520 L 120 -520" stroke={YEL} strokeWidth={10} fill="none" />
    <path d={`M 0 -520 L 0 ${-470 + fall * 120}`} stroke={OL} strokeWidth={3} strokeDasharray="8 6" />
    <g transform={`rotate(${wob + fall * 80} 0 -20)`}>
      <path d={`M -22 -230 L ${-30 - 20 * sw} -20 M 22 -230 L ${30 - 20 * sw} -20`} stroke={OL} strokeWidth={30} strokeLinecap="round" /><path d={`M -22 -230 L ${-30 - 20 * sw} -20 M 22 -230 L ${30 - 20 * sw} -20`} stroke={CHROME} strokeWidth={20} strokeLinecap="round" />
      <rect x={-60} y={-380} width={120} height={160} rx={30} fill="#ECEFF1" stroke={OL} strokeWidth={5} /><rect x={-30} y={-340} width={60} height={50} rx={10} fill={CY} opacity={0.6} />
      <path d={`M -60 -360 L ${-120} ${-280 - 70 * sw} M 60 -360 L 120 ${-280 + 70 * sw}`} stroke={OL} strokeWidth={24} strokeLinecap="round" /><path d={`M -60 -360 L ${-120} ${-280 - 70 * sw} M 60 -360 L 120 ${-280 + 70 * sw}`} stroke={CHROME2} strokeWidth={14} strokeLinecap="round" />
      <rect x={-44} y={-460} width={88} height={76} rx={26} fill="#ECEFF1" stroke={OL} strokeWidth={5} /><rect x={-34} y={-440} width={68} height={24} rx={12} fill="#12203A" /><circle cx={-14} cy={-428} r={5} fill={CY} /><circle cx={14} cy={-428} r={5} fill={CY} />
    </g>
    <g transform="translate(0 70) rotate(-3)"><rect x={-130} y={-26} width={260} height={46} rx={8} fill={a.tagColor || '#5C6BC0'} stroke={OL} strokeWidth={4} /><T x={0} y={8} s={24} c="#FFFFFF">{a.tag || 'PROTOTYPE · DEMO'}</T></g>
  </g>;
};

/** an illustrative seesaw COST METER between two factories (no numbers): needle `tilt` −1 (left cheaper) .. 1 (right cheaper) */
const pricemeter: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 200), s = (a.scale ?? 1) * pop(t, at, 0.45), tl = kf(a.tilt, t, 0) + 0.04 * Math.sin(t * 3);
  return <g key={'pm' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M -260 0 A 260 260 0 0 1 260 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    <path d="M -230 0 A 230 230 0 0 1 -80 -216" stroke={GREEN} strokeWidth={30} fill="none" /><path d="M 80 -216 A 230 230 0 0 1 230 0" stroke={RED} strokeWidth={30} fill="none" />
    <path d={`M 0 0 L ${Math.sin(tl * 1.2) * 210} ${-Math.cos(tl * 1.2) * 210}`} stroke={OL} strokeWidth={12} strokeLinecap="round" /><circle r={22} fill={OL} />
    <T x={0} y={-120} s={56} c={OL}>?</T>
    <T x={-170} y={44} s={22} c={OL}>{a.left || 'U.S.'}</T><T x={170} y={44} s={22} c={OL}>{a.right || 'CHINA'}</T>
    <T x={0} y={86} s={18} c="#5D6B7A">{a.note || 'ILLUSTRATIVE COST METER'}</T>
  </g>;
};

export const AUTOMATION_ITEMS: Record<string, ItemFn> = {torq, humanoid, pricemeter};
export const AUTOMATION_INDOOR = ['ohiobot', 'billbox', 'toastlab', 'moneyriver', 'aititle', 'aibumper'];
