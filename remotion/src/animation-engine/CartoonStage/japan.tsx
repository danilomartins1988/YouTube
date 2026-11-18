import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * JAPAN kit for CartoonStage (Episode 66, "Will AI Make Japan Rich Again?").
 *
 * A bespoke, respectful day-time Japan drawn in the channel's prime-time cartoon GENRE (thick clean outlines, flat colour,
 * squash and stretch). Everything ORIGINAL: no logos, no brand names, no traced products or buildings; companies are named
 * only in narration or on plain plaques. No real person is drawn. HOSHIMACHI is a fictional mountain town; HIRO (workshop
 * owner), AOI (his granddaughter) and KOBO (their collaborative robot arm) are fictional.
 * Sets:
 *  - jtown: Hoshimachi by day: layered mountains, an embankment railway with a two-car local train (`train` [t...]), a small
 *    station, wooden shophouses with tiled roofs whose roll shutters come down with `shutters` (KF 0..1), utility poles and
 *    wires, a vending machine, HIRO'S WORKSHOP with an open roll door, a paper HELP WANTED sign (`signAt`, `signText`), a
 *    kei truck (`truckX` KF), and `kobo` (KF 0..1) a robot arm working inside the workshop door.
 *  - jshop: the workshop interior: lathe (chuck spins with `run` KF 0..1, chips fly), bench, parts trays, wall clock, the
 *    apprentice's empty stool (`stoolHi` [t0, t1]), the cobot KOBO rising from its crate (`arm` KF 0..1) and its load cycle
 *    (`cycle` KF 0..1), a parts board (`parts` [[t, text]]), a laptop typing code (`codeAt`).
 *  - jplatform: a commuter platform: canopy, tactile strip, a train that glides in (`trainAt`), an LED board (`board`
 *    [[t, text]]) and a rush-hour crowd that thins with `crowd` (KF 0..1).
 *  - jroad: a logistics depot: dock doors, pallets of boxes, trucks at the dock (`trucks` KF 0..6), stranded pallets
 *    tagged NO TRUCK (`left` KF 0..1), an overtime-cap sign (`capAt`), self-driving carts (`agv` KF 0..1).
 *  - jcare: a care-home day room: beds with sensor pads (`sensors` KF 0..1) feeding a monitor, a lift-assist machine
 *    (`lift` KF 0..1), a tea table, a staffing board (`need` text, `needAt`).
 *  - jhist: a sepia car plant of the late 1960s: an early hydraulic robot arm (`armAt`) among busy workers, a wall calendar
 *    (`year`), a HELP WANTED board.
 *  - jfactory: a robot maker's bright plant: orange arms assemble arms on a conveyor; crates leave through two doors, TO THE
 *    WORLD (ship) or JAPAN (truck) by `share` (KF 0..1); `plaque`, `dests` [text...].
 *  - jdensity: robots per 100 factory workers, two rooms side by side (`rows` [{label, n, at, color}]).
 *  - jkonbini: a convenience-store interior; `cut` (KF 0..1) turns the drink fridge into a cutaway showing a rail-mounted
 *    restocking arm that fills slots (`stock` KF 0..1); `fumbleAt` a bottle drops, `vrAt` a remote operator with a headset.
 *  - jdemo: a triptych hall: RETIRED walking robot in a glass case (`caseAt`), an arm AT WORK TODAY (`workAt`), a humanoid
 *    PROTOTYPE on a test stand (`protoAt`, `protoText`).
 *  - jyen: a yen coin that shrinks beside a dollar (`shrink` KF 0..1), crates out cheaper (`outAt`) and imports in pricier
 *    (`inAt`).
 *  - jscale: the catch: a balance; ROBOTS + AI on the left, `weights` [{label, at, color, big}] drop on the right; `tilt` KF.
 *  - jtitle / jbumper: the title card (KOBO writes the title over Hoshimachi) and chapter bumpers (a workshop roll shutter
 *    rolls up on the chapter title).
 * Items: jtag (top-left pill: FACT / PROJECTION / ESTIMATE / OUR CALC / COMPANY CLAIM / PLAN / FINDING / STORY...), kobo (the
 *  cobot mascot on a little cart with a screen face: `x` KF, `face`/`faces`, `wave` [t...], `carry`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#1B2333';
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

const BLUE = '#2F6FD1', GOLD = '#F5B700', RED = '#D9443A', GREEN = '#3E9B5F', TEAL = '#1F8A8C', PURPLE = '#7357C9', NAVY = '#1B2A4A', ORANGE = '#F08A24',
  INDIGO = '#2E3F7F', WOOD = '#B9844F', WOOD2 = '#8C5A33', ROOF = '#4A5878', CREAM = '#FFF4DE', CY = '#38C6F4';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'jcl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const banner = (x: number, y: number, txt: string, c = RED, s = 26) => { const w = Math.max(240, txt.length * s * 0.62 + 50);
  return <g transform={`translate(${x} ${y}) rotate(-2)`}><rect x={-w / 2} y={-s} width={w} height={s * 1.7} rx={8} fill={c} stroke={OL} strokeWidth={4} />
    <T x={0} y={s * 0.32} s={s} c="#FFFFFF">{txt}</T></g>; };
const box = (x: number, y: number, s: number, k: any, c = '#D9A86C') => <g key={'bx' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-34} y={-50} width={68} height={50} rx={3} fill={c} stroke={OL} strokeWidth={4} /><path d="M -34 -32 L 34 -32 M 0 -50 L 0 -32" stroke="#A9783F" strokeWidth={4} /></g>;

/** a simple person (never a likeness): bean body, round head; `old` = white hair */
const person = (x: number, y: number, s: number, k: number, t: number, c: string, old = false, bag = false) => {
  const bob = Math.sin(t * 2 + k) * 2;
  return <g key={'pp' + k} transform={`translate(${x} ${y + bob}) scale(${s})`}>
    <path d="M -12 0 L -12 -50 M 12 0 L 12 -50" stroke="#2D3E66" strokeWidth={12} strokeLinecap="round" />
    <path d="M -30 -46 Q -34 -120 0 -124 Q 34 -120 30 -46 Z" fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={0} cy={-148} r={26} fill={['#F6CDA6', '#E0A878', '#F3D7BD'][k % 3]} stroke={OL} strokeWidth={4} />
    <path d={`M -26 -154 Q -24 -180 0 -178 Q 24 -180 26 -154 Q 12 -166 -26 -154 Z`} fill={old ? '#E8ECEF' : ['#1B1B1B', '#3E2723', '#2B2B33'][k % 3]} stroke={OL} strokeWidth={3} />
    <circle cx={-9} cy={-148} r={3} fill={OL} /><circle cx={9} cy={-148} r={3} fill={OL} />
    {bag && <rect x={22} y={-80} width={26} height={34} rx={4} fill="#5D4037" stroke={OL} strokeWidth={3} />}
  </g>;
};

/** a robot arm by forward kinematics; angles in degrees from vertical (a1 shoulder, a2 elbow, a3 wrist); grip 0..1 open */
const armFK = (x: number, y: number, s: number, a1: number, a2: number, a3: number, grip: number, c: string, k: any, held?: string, base = true) => {
  const L1 = 170, L2 = 150, L3 = 46, r = Math.PI / 180;
  const p0 = [0, -90], p1 = [p0[0] + L1 * Math.sin(a1 * r), p0[1] - L1 * Math.cos(a1 * r)];
  const p2 = [p1[0] + L2 * Math.sin((a1 + a2) * r), p1[1] - L2 * Math.cos((a1 + a2) * r)];
  const aw = a1 + a2 + a3, p3 = [p2[0] + L3 * Math.sin(aw * r), p2[1] - L3 * Math.cos(aw * r)];
  const seg = (a: number[], b: number[], w: number) => <g><path d={`M ${a[0]} ${a[1]} L ${b[0]} ${b[1]}`} stroke={OL} strokeWidth={w + 9} strokeLinecap="round" />
    <path d={`M ${a[0]} ${a[1]} L ${b[0]} ${b[1]}`} stroke={c} strokeWidth={w} strokeLinecap="round" /></g>;
  const g = 10 + 16 * grip, ux = Math.sin(aw * r), uy = -Math.cos(aw * r), nx = -uy, ny = ux;
  return <g key={'arm' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    {base && <g><rect x={-62} y={-40} width={124} height={40} rx={8} fill="#5B6B82" stroke={OL} strokeWidth={5} />
      <path d="M -40 -40 L -30 -90 L 30 -90 L 40 -40 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" /></g>}
    {seg(p0, p1, 34)}{seg(p1, p2, 28)}{seg(p2, p3, 20)}
    {[p0, p1, p2].map((p, q) => <circle key={q} cx={p[0]} cy={p[1]} r={20 - q * 3} fill="#ECEFF1" stroke={OL} strokeWidth={4.5} />)}
    {[-1, 1].map((sd) => <path key={sd} d={`M ${p3[0] + nx * g * sd} ${p3[1] + ny * g * sd} L ${p3[0] + nx * g * sd + ux * 30} ${p3[1] + ny * g * sd + uy * 30}`} stroke={OL} strokeWidth={9} strokeLinecap="round" />)}
    {held === 'part' && <rect x={p3[0] + ux * 26 - 13} y={p3[1] + uy * 26 - 13} width={26} height={26} rx={5} fill="#B0BEC5" stroke={OL} strokeWidth={3} />}
    {held === 'bottle' && <g transform={`translate(${p3[0] + ux * 30} ${p3[1] + uy * 30})`}><rect x={-11} y={-26} width={22} height={44} rx={8} fill={CY} stroke={OL} strokeWidth={3} /><rect x={-6} y={-34} width={12} height={9} fill="#FFFFFF" stroke={OL} strokeWidth={2} /></g>}
    {held === 'arm' && <g transform={`translate(${p3[0] + ux * 34} ${p3[1] + uy * 34})`}><rect x={-14} y={-30} width={28} height={50} rx={10} fill={ORANGE} stroke={OL} strokeWidth={3} /></g>}
  </g>;
};
/** blend between poses: list of [a1,a2,a3,grip] over a looping cycle */
const cyc = (t: number, P: number, poses: number[][], ph = 0) => {
  const u = (((t + ph) / P) % 1 + 1) % 1, n = poses.length, q = u * n, i = Math.floor(q), fr = E.inOut(clamp((q - i) * 1.6));
  const A = poses[i % n], B = poses[(i + 1) % n];
  return {v: A.map((x, j) => lerp(x, B[j], fr)), i, fr};
};

const ridge = (x0: number, x1: number, base: number, amp: number, per: number, seed: number) => {
  let d = `M ${x0} ${base + 400} L ${x0} ${base}`;
  for (let x = x0; x <= x1; x += 120) d += ` L ${x} ${base - amp * (0.5 + 0.5 * Math.sin(x / per + seed)) - amp * 0.35 * Math.sin(x / (per * 0.37) + seed * 2)}`;
  return d + ` L ${x1} ${base + 400} Z`;
};

/** two-car local train (generic cream/green), front at x */
const train = (x: number, y: number, s: number, k: any, doors = 0) => <g key={'tr' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  {[0, 1].map((c) => <g key={c} transform={`translate(${c * 520} 0)`}>
    <rect x={0} y={-170} width={500} height={150} rx={c === 0 ? 40 : 14} fill={CREAM} stroke={OL} strokeWidth={6} />
    <rect x={0} y={-80} width={500} height={26} fill="#3E9B5F" stroke={OL} strokeWidth={4} />
    {[0, 1, 2, 3].map((w) => <rect key={w} x={40 + w * 110} y={-150} width={70} height={52} rx={6} fill="#BFE6F7" stroke={OL} strokeWidth={4} />)}
    {[150, 330].map((dx) => <g key={dx}><rect x={dx - 30 * (1 + doors)} y={-150} width={30} height={128} fill="#E0E6EC" stroke={OL} strokeWidth={4} /><rect x={dx + 30 * doors} y={-150} width={30} height={128} fill="#E0E6EC" stroke={OL} strokeWidth={4} /></g>)}
    {[90, 410].map((wx) => <circle key={wx} cx={wx} cy={-14} r={22} fill="#455A64" stroke={OL} strokeWidth={5} />)}
  </g>)}
  <path d="M 200 -170 L 240 -210 M 300 -170 L 260 -210 M 230 -210 L 270 -210" stroke={OL} strokeWidth={5} />
</g>;

/** wooden shophouse with tiled roof, lattice front, plain curtain; roll shutter 0..1 */
const shophouse = (x: number, y: number, w: number, k: number, body: string, shut: number, curtain: string) => <g key={'sh' + k}>
  <rect x={x} y={y - 330} width={w} height={330} fill={body} stroke={OL} strokeWidth={5} />
  <path d={`M ${x - 30} ${y - 330} Q ${x + w / 2} ${y - 300} ${x + w + 30} ${y - 330} L ${x + w - 10} ${y - 390} L ${x + 10} ${y - 390} Z`} fill={ROOF} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
  {Array.from({length: Math.floor(w / 40)}, (_, q) => <path key={q} d={`M ${x + 20 + q * 40} ${y - 386} L ${x + 14 + q * 40} ${y - 334}`} stroke="#33405C" strokeWidth={3} />)}
  <rect x={x + 30} y={y - 300} width={w - 60} height={90} fill="#D7C2A0" stroke={OL} strokeWidth={4} />
  {Array.from({length: Math.floor((w - 60) / 18)}, (_, q) => <path key={'lt' + q} d={`M ${x + 40 + q * 18} ${y - 300} L ${x + 40 + q * 18} ${y - 210}`} stroke={WOOD2} strokeWidth={4} />)}
  <path d={`M ${x - 18} ${y - 196} L ${x + w + 18} ${y - 196} L ${x + w} ${y - 176} L ${x} ${y - 176} Z`} fill={ROOF} stroke={OL} strokeWidth={4} />
  <rect x={x + 24} y={y - 176} width={w - 48} height={176} fill="#5A4636" stroke={OL} strokeWidth={4} />
  {shut < 0.98 && <g>{[0, 1, 2].map((q) => <path key={q} d={`M ${x + 34 + q * (w - 68) / 3} ${y - 172} L ${x + 34 + (q + 1) * (w - 68) / 3 - 6} ${y - 172} L ${x + 34 + (q + 1) * (w - 68) / 3 - 6} ${y - 110} L ${x + 34 + q * (w - 68) / 3} ${y - 110} Z`} fill={curtain} stroke={OL} strokeWidth={3} />)}
    <circle cx={x + w / 2} cy={y - 140} r={14} fill="none" stroke="#FFFFFF" strokeWidth={4} opacity={0.8} /></g>}
  {shut > 0 && <g><rect x={x + 24} y={y - 176} width={w - 48} height={176 * shut} fill="#AEB7C2" stroke={OL} strokeWidth={4} />
    {Array.from({length: Math.floor(176 * shut / 14)}, (_, q) => <path key={'sl' + q} d={`M ${x + 24} ${y - 176 + q * 14} L ${x + w - 24} ${y - 176 + q * 14}`} stroke="#8E99A6" strokeWidth={2.5} />)}
    <rect x={x + 18} y={y - 190} width={w - 36} height={20} rx={4} fill="#8E99A6" stroke={OL} strokeWidth={3} /></g>}
</g>;

/** utility pole with crossarm and transformer */
const jpole = (x: number, y: number, k: number) => <g key={'jp' + k}>
  <rect x={x - 9} y={y - 470} width={18} height={470} fill="#B8B2A7" stroke={OL} strokeWidth={4} />
  <rect x={x - 70} y={y - 450} width={140} height={12} fill="#8E8A80" stroke={OL} strokeWidth={3} />
  <rect x={x - 50} y={y - 400} width={100} height={10} fill="#8E8A80" stroke={OL} strokeWidth={3} />
  <rect x={x + 12} y={y - 380} width={40} height={60} rx={10} fill="#9AA4AE" stroke={OL} strokeWidth={4} />
</g>;

/** generic vending machine (no brands) */
const vending = (x: number, y: number, t: number) => <g transform={`translate(${x} ${y})`}>
  <rect x={-70} y={-250} width={140} height={250} rx={8} fill="#F4F6F8" stroke={OL} strokeWidth={5} />
  <rect x={-58} y={-236} width={116} height={120} rx={4} fill="#DDEFFA" stroke={OL} strokeWidth={3} />
  {Array.from({length: 12}, (_, q) => <rect key={q} x={-52 + (q % 4) * 28} y={-228 + Math.floor(q / 4) * 38} width={18} height={30} rx={6} fill={[CY, RED, GOLD, GREEN][(q + 1) % 4]} stroke={OL} strokeWidth={2} />)}
  {Array.from({length: 4}, (_, q) => <circle key={'b' + q} cx={-40 + q * 27} cy={-100} r={6} fill={(Math.floor(t * 2) + q) % 4 === 0 ? GOLD : '#C8D2DC'} stroke={OL} strokeWidth={2} />)}
  <rect x={-50} y={-60} width={100} height={30} rx={4} fill="#37474F" stroke={OL} strokeWidth={3} />
</g>;

const RAW: Record<string, SetFn> = {
  /** Hoshimachi by day */
  jtown: (t, z, f) => {
    const w = z.x1 - z.x0, shut = clamp(kf(z.shutters, t, 0.2)), kobo = clamp(kf(z.kobo, t, 0)), tx = kf(z.truckX, t, -9999);
    const shops = [[-760, 380, '#E9D8B8', INDIGO], [-340, 400, '#E3CFA9', '#7A2E2E'], [700, 380, '#EAD9BA', '#2E5E4E'], [1120, 400, '#E6D3B0', INDIGO], [1560, 360, '#E9D8B8', '#6B4A2B']];
    let tr: React.ReactNode = null;
    for (const t0 of (z.train || []) as number[]) { const u = (t - t0) / 6; if (u > 0 && u < 1) tr = train(lerp(z.x1, z.x0 - 1200, u), f - 290, 0.75, 'jt' + t0); }
    return <g>
      {sky(z, f, '#86CDF2', '#EEF9FF', 'jsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 900 + t * 10) % (w + 600)) + z.x0 - 300, 110 + (k % 2) * 60, 0.8, k))}
      <path d={ridge(z.x0, z.x1, f - 360, 220, 260, 1)} fill="#A9C7D6" />
      <path d={ridge(z.x0, z.x1, f - 300, 170, 180, 3)} fill="#7FB08C" stroke={OL} strokeWidth={3} />
      {Array.from({length: 7}, (_, k) => <path key={'ter' + k} d={`M ${-200 + k * 90} ${f - 300 - k * 14} Q ${200 + k * 60} ${f - 320 - k * 14} ${700 + k * 30} ${f - 296 - k * 14}`} stroke="#9CCB86" strokeWidth={6} fill="none" opacity={0.8} />)}
      {/* embankment railway + station */}
      <rect x={z.x0} y={f - 300} width={w} height={60} fill="#B7A98F" stroke={OL} strokeWidth={4} />
      <path d={`M ${z.x0} ${f - 300} L ${z.x1} ${f - 300}`} stroke="#6D6458" strokeWidth={6} />
      <g transform={`translate(2150 ${f - 300})`}><rect x={-200} y={-14} width={400} height={14} fill="#D8D2C6" stroke={OL} strokeWidth={3} />
        <path d="M -180 -14 L -180 -150 M 180 -14 L 180 -150" stroke={OL} strokeWidth={8} /><path d="M -220 -150 L 220 -150 L 200 -180 L -200 -180 Z" fill={ROOF} stroke={OL} strokeWidth={4} />
        {plaque(0, -110, z.station || 'HOSHIMACHI STA.', '#FFFFFF', 20)}</g>
      {tr}
      {/* street */}
      <rect x={z.x0} y={f - 240} width={w} height={240} fill="#D9D2C3" />
      {shops.map(([sx, sw, c, cu], k) => shophouse(sx as number, f, sw as number, k, c as string, clamp(shut * 5 - (k === 2 ? 0 : k === 4 ? 1 : k === 0 ? 2 : k === 3 ? 3 : 4)), cu as string))}
      {/* Hiro's workshop */}
      <g transform={`translate(100 ${f})`}>
        <rect x={0} y={-360} width={520} height={360} fill="#C9D3DC" stroke={OL} strokeWidth={5} />
        {Array.from({length: 13}, (_, q) => <path key={q} d={`M ${20 + q * 40} -360 L ${20 + q * 40} -200`} stroke="#AEB9C4" strokeWidth={4} />)}
        <path d="M -20 -360 L 540 -360 L 520 -400 L 0 -400 Z" fill="#7C8A9E" stroke={OL} strokeWidth={4} />
        <rect x={40} y={-200} width={300} height={200} fill="#3A3530" stroke={OL} strokeWidth={5} />
        <rect x={40} y={-200} width={300} height={200} fill="#FFC970" opacity={0.25 + 0.05 * Math.sin(t * 3)} />
        <g opacity={0.9}><rect x={90} y={-110} width={130} height={60} fill="#5B6B82" stroke={OL} strokeWidth={3} /><circle cx={230} cy={-80} r={22} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g>
        {kobo > 0 && (() => { const c = cyc(t, 3.2, [[50, 60, 30, 1], [-30, -60, -20, 0], [-30, -60, -20, 1], [50, 60, 30, 0]]);
          return <g opacity={kobo}>{armFK(290, -10, 0.42, c.v[0], c.v[1], c.v[2], c.v[3], ORANGE, 'kt', c.i === 1 || c.i === 2 ? undefined : 'part')}</g>; })()}
        <rect x={40} y={-214} width={300} height={18} fill="#8E99A6" stroke={OL} strokeWidth={3} />
        <rect x={380} y={-300} width={110} height={120} fill="#BFE6F7" stroke={OL} strokeWidth={4} />
        {z.signAt !== undefined && t >= z.signAt && <g transform={`translate(435 -240) rotate(${-3 + 2 * Math.sin(t * 1.7)}) scale(${pop(t, z.signAt, 0.4)})`}>
          <rect x={-48} y={-50} width={96} height={100} fill="#FFFDF5" stroke={OL} strokeWidth={3} />
          <rect x={-40} y={-42} width={80} height={84} fill="none" stroke={RED} strokeWidth={3} />
          {String(z.signText || 'HELP\nWANTED').split('\n').map((ln, q) => <T key={q} x={0} y={-8 + q * 26} s={18} c={RED}>{ln}</T>)}</g>}
        {plaque(260, -440, z.shopText || "HIRO'S WORKSHOP", '#FFFFFF', 24)}
      </g>
      {[-480, 640, 1500, 2600].map((px, k) => jpole(px, f, k))}
      <path d={`M -480 ${f - 450} Q 80 ${f - 400} 640 ${f - 450} Q 1070 ${f - 400} 1500 ${f - 450} Q 2050 ${f - 400} 2600 ${f - 450}`} stroke={OL} strokeWidth={3} fill="none" />
      <path d={`M -480 ${f - 400} Q 80 ${f - 360} 640 ${f - 400} Q 1070 ${f - 362} 1500 ${f - 400} Q 2050 ${f - 360} 2600 ${f - 400}`} stroke={OL} strokeWidth={2.5} fill="none" />
      <path d={`M -480 ${f - 430} Q 80 ${f - 385} 640 ${f - 430} Q 1070 ${f - 388} 1500 ${f - 430} Q 2050 ${f - 386} 2600 ${f - 430}`} stroke={OL} strokeWidth={2} fill="none" />
      {vending(1990, f, t)}
      {/* pine */}
      <g transform={`translate(2400 ${f})`}><rect x={-12} y={-220} width={24} height={220} fill={WOOD2} stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((q) => <ellipse key={q} cx={(q - 1) * 50} cy={-230 - q * 50} rx={90 - q * 15} ry={34} fill="#3E7D4F" stroke={OL} strokeWidth={4} />)}</g>
      {/* road */}
      <rect x={z.x0} y={f} width={w} height={260} fill="#9AA0A8" />
      <rect x={z.x0} y={f} width={w} height={12} fill="#C9CDD2" stroke={OL} strokeWidth={3} />
      {Array.from({length: 22}, (_, k) => <rect key={'rl' + k} x={z.x0 + k * 300} y={f + 110} width={150} height={10} fill="#FFFFFF" />)}
      {tx > -9000 && <g transform={`translate(${tx} ${f + 150})`}>
        <rect x={-120} y={-80} width={150} height={70} fill="#F4F6F8" stroke={OL} strokeWidth={5} /><path d="M 30 -10 L 30 -110 L 100 -110 L 120 -60 L 120 -10 Z" fill="#F4F6F8" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <rect x={44} y={-100} width={50} height={36} fill="#BFE6F7" stroke={OL} strokeWidth={3} />{box(-80, -80, 0.8, 'tb1')}{box(-20, -80, 0.8, 'tb2', '#E8BE83')}
        {[-80, 80].map((wx) => <circle key={wx} cx={wx} cy={0} r={24} fill="#37474F" stroke={OL} strokeWidth={5} />)}</g>}
    </g>;
  },

  /** the workshop interior */
  jshop: (t, z, f) => {
    const run = clamp(kf(z.run, t, 0)), arm = clamp(kf(z.arm, t, 0)), on = clamp(kf(z.cycle, t, 0)), parts = pick(z.parts, t, '');
    const hi = z.stoolHi && t >= z.stoolHi[0] && t <= z.stoolHi[1];
    const c = cyc(t, 3.6, [[48, 70, 40, 1], [48, 70, 40, 0], [-38, -58, -30, 0], [-38, -58, -30, 1]]);
    const rest = [10, 30, 20, 1], ang = c.v.map((v, j) => lerp(rest[j], v, on));
    const carrying = on > 0.5 && (c.i === 1 || (c.i === 2 && c.fr < 0.95));
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#DDE6DC" />
      <rect x={z.x0} y={f - 640} width={z.x1 - z.x0} height={16} fill="#B8C4B6" />
      {/* windows to the mountains */}
      {[300, 1500].map((wx, k) => <g key={'wn' + k}><rect x={wx} y={f - 600} width={380} height={170} fill="#BFE6F7" stroke={OL} strokeWidth={5} />
        <path d={`M ${wx} ${f - 470} Q ${wx + 100} ${f - 560} ${wx + 190} ${f - 490} Q ${wx + 290} ${f - 570} ${wx + 380} ${f - 480} L ${wx + 380} ${f - 430} L ${wx} ${f - 430} Z`} fill="#7FB08C" />
        <path d={`M ${wx + 190} ${f - 600} L ${wx + 190} ${f - 430}`} stroke={OL} strokeWidth={4} /></g>)}
      {/* pegboard + clock */}
      <rect x={760} y={f - 600} width={520} height={220} fill="#C9A26E" stroke={OL} strokeWidth={5} />
      {Array.from({length: 6}, (_, q) => <path key={q} d={`M ${800 + q * 80} ${f - 560} l 0 ${60 + (q % 3) * 20}`} stroke="#5B6B82" strokeWidth={8} strokeLinecap="round" />)}
      <g transform={`translate(1380 ${f - 520})`}><circle r={50} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <path d={`M 0 0 L ${30 * Math.sin(t * 0.5)} ${-30 * Math.cos(t * 0.5)}`} stroke={OL} strokeWidth={5} strokeLinecap="round" />
        <path d={`M 0 0 L ${40 * Math.sin(t * 6)} ${-40 * Math.cos(t * 6)}`} stroke={RED} strokeWidth={3} /></g>
      {/* floor */}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#A8ADB3" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={10} fill="#8E949B" />
      {/* bench + trays + laptop */}
      <g transform={`translate(160 ${f})`}><rect x={0} y={-200} width={460} height={26} fill={WOOD} stroke={OL} strokeWidth={5} />
        <path d="M 20 -174 L 20 0 M 440 -174 L 440 0" stroke={OL} strokeWidth={14} />
        <rect x={30} y={-262} width={90} height={62} fill="#5B6B82" stroke={OL} strokeWidth={4} />
        {[0, 1].map((q) => <g key={q}><rect x={150 + q * 110} y={-246} width={96} height={46} rx={4} fill={q ? GOLD : BLUE} stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3].map((p) => <rect key={p} x={160 + q * 110 + p * 20} y={-262} width={14} height={18} rx={3} fill="#B0BEC5" stroke={OL} strokeWidth={2} />)}</g>)}
        {z.codeAt !== undefined && t >= z.codeAt && <g transform="translate(400 -200)"><path d="M -60 0 L -40 -80 L 60 -80 L 40 0 Z" fill="#263238" stroke={OL} strokeWidth={4} />
          {[0, 1, 2, 3].map((l) => { const n = clamp((t - z.codeAt - l * 0.6) / 0.6); return <rect key={l} x={-36 + l * 2} y={-70 + l * 15} width={70 * n * (0.5 + 0.5 * rnd(l))} height={6} fill={[CY, GOLD, '#A5D6A7', CY][l]} transform="skewX(-14)" />; })}</g>}
      </g>
      {/* the empty stool */}
      <g transform={`translate(760 ${f})`}>{hi && <ellipse cx={0} cy={-4} rx={110} ry={24} fill={GOLD} opacity={0.35 + 0.2 * Math.sin(t * 6)} />}
        <path d="M -40 0 L -30 -130 M 40 0 L 30 -130 M -36 -60 L 36 -60" stroke={WOOD2} strokeWidth={10} strokeLinecap="round" />
        <ellipse cx={0} cy={-136} rx={56} ry={16} fill={WOOD} stroke={OL} strokeWidth={5} />
        {hi && <path d="M -80 -230 Q 0 -290 80 -230" stroke={GOLD} strokeWidth={6} fill="none" strokeDasharray="14 10" />}</g>
      {/* lathe */}
      <g transform={`translate(1000 ${f})`}><rect x={0} y={-160} width={360} height={160} fill="#5B7A6E" stroke={OL} strokeWidth={5} />
        <rect x={0} y={-300} width={130} height={140} rx={10} fill="#6E8F82" stroke={OL} strokeWidth={5} />
        <rect x={240} y={-260} width={100} height={100} rx={8} fill="#6E8F82" stroke={OL} strokeWidth={5} />
        <g transform="translate(170 -230)"><circle r={42} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
          {[0, 1, 2].map((q) => <path key={q} transform={`rotate(${q * 120 + t * 900 * run})`} d="M 0 -10 L 0 -38" stroke={OL} strokeWidth={8} strokeLinecap="round" />)}</g>
        <rect x={210} y={-238} width={34} height={16} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
        {run > 0.2 && Array.from({length: 6}, (_, q) => { const u = (t * 2.4 + q / 6) % 1; return <circle key={q} cx={230 + u * 80} cy={-226 + u * u * 120 - 30 * u} r={4} fill={GOLD} opacity={1 - u} />; })}
      </g>
      {/* KOBO: crate + arm */}
      <g transform={`translate(1560 ${f})`}>
        {arm < 1 && <g opacity={1 - E.in(clamp((arm - 0.6) / 0.4))}><rect x={-120} y={-150} width={240} height={150} fill="#D9A86C" stroke={OL} strokeWidth={5} />
          <path d={`M -120 -150 L ${-120 - 120 * arm} ${-210 * arm - 150 * (1 - arm)}`} stroke={OL} strokeWidth={5} /><T x={0} y={-60} s={26} c="#7A4F22">KOBO</T></g>}
        {arm > 0 && <g transform={`translate(0 ${80 * (1 - E.out(arm))})`} opacity={clamp(arm * 3)}>{armFK(0, 0, 1.05, ang[0], ang[1], ang[2], ang[3], ORANGE, 'kobo', carrying ? 'part' : undefined)}
          <g transform="translate(0 -120)"><rect x={-34} y={-22} width={68} height={40} rx={10} fill="#263238" stroke={OL} strokeWidth={3} />
            <circle cx={-12} cy={-2} r={6} fill={CY} /><circle cx={12} cy={-2} r={6} fill={CY} /></g></g>}
        <rect x={180} y={-170} width={160} height={24} fill={WOOD} stroke={OL} strokeWidth={4} /><path d="M 200 -146 L 200 0 M 320 -146 L 320 0" stroke={OL} strokeWidth={10} />
        {[0, 1, 2].map((p) => <rect key={p} x={200 + p * 40} y={-196} width={26} height={26} rx={5} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}
      </g>
      {parts && <g transform={`translate(560 ${f - 470})`}><rect x={-150} y={-60} width={300} height={110} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <T x={0} y={-22} s={22} c="#5E6B85">PARTS TODAY</T><T x={0} y={32} s={46} c={GREEN}>{parts}</T></g>}
    </g>;
  },

  /** commuter platform: crowd thins with `crowd` */
  jplatform: (t, z, f) => {
    const crowd = clamp(kf(z.crowd, t, 1)), board = pick(z.board, t, ''), tA = z.trainAt ?? -99, u = E.out(clamp((t - tA) / 3));
    const N = 54;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#CFE8F5" />
      <path d={ridge(z.x0, z.x1, f - 380, 120, 220, 2)} fill="#A9C7D6" />
      {t >= tA && train(lerp(2600, 120, u), f - 70, 1.0, 'pl', clamp((t - tA - 3) / 0.6))}
      <rect x={z.x0} y={f - 70} width={z.x1 - z.x0} height={30} fill="#6D6458" />
      <rect x={z.x0} y={f - 40} width={z.x1 - z.x0} height={340} fill="#C9C3B6" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f - 30} width={z.x1 - z.x0} height={26} fill={GOLD} stroke={OL} strokeWidth={3} />
      {Array.from({length: 60}, (_, k) => <circle key={'dot' + k} cx={z.x0 + k * 110 + 30} cy={f - 17} r={4} fill="#C99A00" />)}
      {/* canopy */}
      <path d={`M ${z.x0} ${f - 640} L ${z.x1} ${f - 640} L ${z.x1} ${f - 600} L ${z.x0} ${f - 600} Z`} fill="#E6E9EE" stroke={OL} strokeWidth={5} />
      {[-200, 500, 1200, 1900, 2600].map((px) => <rect key={px} x={px - 12} y={f - 600} width={24} height={560} fill="#9AA4AE" stroke={OL} strokeWidth={4} />)}
      <g transform={`translate(960 ${f - 560})`}><rect x={-260} y={-30} width={520} height={80} rx={8} fill="#1C1F26" stroke={OL} strokeWidth={5} />
        <T x={0} y={24} s={fit(board || ' ', 480, 40)} c="#FFA726" ls={3}>{board}</T></g>
      {Array.from({length: N}, (_, k) => { const vis = clamp((crowd * N - k) * 1.5), row = k % 3;
        if (vis <= 0) return null;
        const x = -260 + ((k * 173) % 2420) + 30 * rnd(k), y = f + 40 + row * 70;
        return <g key={'cw' + k} opacity={vis}>{person(x, y, 0.9 + 0.1 * row, k, t, ['#2E3F5C', '#5B6B82', '#8D7B68', '#3E5A6B', '#6B4E3D', '#455A64'][k % 6], false, k % 4 === 0)}</g>; })}
    </g>;
  },

  /** logistics depot */
  jroad: (t, z, f) => {
    const trucks = kf(z.trucks, t, 6), left = clamp(kf(z.left, t, 0)), agv = clamp(kf(z.agv, t, 0));
    return <g>
      {sky(z, f, '#9AD3F2', '#F0FAFF', 'jrsky' + Math.round(z.x0))}
      <path d={ridge(z.x0, z.x1, f - 420, 120, 200, 4)} fill="#A9C7D6" />
      {/* expressway on pillars */}
      <rect x={z.x0} y={f - 470} width={z.x1 - z.x0} height={40} fill="#B0B8C2" stroke={OL} strokeWidth={4} />
      {[-300, 300, 900, 1500, 2100, 2700].map((px) => <rect key={px} x={px - 20} y={f - 430} width={40} height={120} fill="#9AA4AE" stroke={OL} strokeWidth={3} />)}
      {z.capAt !== undefined && t >= z.capAt && <g transform={`translate(1700 ${f - 560}) scale(${pop(t, z.capAt)})`}>
        <rect x={-190} y={-60} width={380} height={110} rx={10} fill={BLUE} stroke={OL} strokeWidth={5} />
        <circle cx={-130} cy={-5} r={36} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><path d={`M -130 -5 L -130 -30 M -130 -5 L ${-130 + 18 * Math.sin(t)} 8`} stroke={OL} strokeWidth={4} />
        <T x={40} y={-10} s={26} c="#FFFFFF">OVERTIME CAP</T><T x={40} y={28} s={22} c="#FFFFFF">FOR TRUCK DRIVERS</T></g>}
      {/* warehouse */}
      <rect x={-100} y={f - 400} width={1250} height={400} fill="#E4E8EE" stroke={OL} strokeWidth={5} />
      <path d={`M -130 ${f - 400} L 1180 ${f - 400} L 1120 ${f - 450} L -70 ${f - 450} Z`} fill="#8E9AAF" stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3, 4, 5].map((d) => <rect key={'dr' + d} x={-60 + d * 200} y={f - 300} width={160} height={260} fill="#5B6B82" stroke={OL} strokeWidth={4} />)}
      <rect x={-120} y={f - 40} width={1290} height={40} fill="#B0B8C2" stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3, 4, 5].map((d) => { const here = trucks > d + 0.5, gone = clamp(d + 1 - trucks);
        const tx = -60 + d * 200 + 80, ty = f + 170 + gone * 0;
        return <g key={'tk' + d} transform={`translate(${tx} ${ty + 260 * gone})`} opacity={here ? 1 : 1 - gone}>
          <rect x={-80} y={-200} width={160} height={150} fill={['#FFFFFF', '#E3F2FD', '#FFF8E1'][d % 3]} stroke={OL} strokeWidth={5} />
          <rect x={-70} y={-50} width={140} height={60} fill="#90A4AE" stroke={OL} strokeWidth={4} /><rect x={-50} y={-40} width={100} height={30} fill="#BFE6F7" stroke={OL} strokeWidth={3} />
          {[-50, 50].map((wx) => <circle key={wx} cx={wx} cy={16} r={20} fill="#37474F" stroke={OL} strokeWidth={4} />)}</g>; })}
      {/* pallets of boxes in the yard */}
      {Array.from({length: 9}, (_, p) => { const px = 1300 + (p % 3) * 230, py = f + 40 + Math.floor(p / 3) * 70, strand = p / 9 < left;
        return <g key={'pal' + p}><rect x={px - 80} y={py - 12} width={160} height={14} fill={WOOD} stroke={OL} strokeWidth={3} />
          {[0, 1, 2, 3].map((q) => box(px - 40 + (q % 2) * 80, py - 12 - Math.floor(q / 2) * 50, 0.95, `pb${p}${q}`, strand ? '#E7B57A' : '#D9A86C'))}
          {strand && <g transform={`translate(${px} ${py - 130}) rotate(${-6 + 3 * Math.sin(t * 2 + p)})`}><rect x={-62} y={-18} width={124} height={34} rx={6} fill={RED} stroke={OL} strokeWidth={3} /><T x={0} y={8} s={18} c="#FFFFFF">NO TRUCK</T></g>}</g>; })}
      {agv > 0 && [0, 1, 2].map((q) => { const u = (t * 0.25 + q / 3) % 1, x = lerp(1250, 2100, u);
        return <g key={'agv' + q} transform={`translate(${x} ${f + 250})`} opacity={agv}><rect x={-50} y={-30} width={100} height={30} rx={8} fill={ORANGE} stroke={OL} strokeWidth={4} />
          {box(0, -30, 0.7, 'ag' + q)}<circle cx={-30} cy={2} r={8} fill={OL} /><circle cx={30} cy={2} r={8} fill={OL} /><circle cx={0} cy={-20} r={4} fill={CY} /></g>; })}
    </g>;
  },

  /** care-home day room */
  jcare: (t, z, f) => {
    const sens = clamp(kf(z.sensors, t, 0)), lift = clamp(kf(z.lift, t, 0));
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#F6EFE4" />
      {[200, 1100].map((wx) => <g key={wx}><rect x={wx} y={f - 620} width={640} height={300} fill="#CDEBD8" stroke={OL} strokeWidth={5} />
        <path d={`M ${wx} ${f - 400} Q ${wx + 200} ${f - 470} ${wx + 360} ${f - 410} Q ${wx + 500} ${f - 460} ${wx + 640} ${f - 400} L ${wx + 640} ${f - 320} L ${wx} ${f - 320} Z`} fill="#8FC79A" />
        <circle cx={wx + 480} cy={f - 470} r={40} fill="#5E9E6B" stroke={OL} strokeWidth={3} /><path d={`M ${wx + 320} ${f - 620} L ${wx + 320} ${f - 320}`} stroke={OL} strokeWidth={4} /></g>)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#D9B98C" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={10} fill="#B9925F" />
      {/* beds with sensor pads */}
      {[0, 1].map((b) => { const bx = 120 + b * 470;
        return <g key={'bed' + b}><rect x={bx} y={f - 150} width={380} height={70} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <rect x={bx} y={f - 220} width={30} height={220} fill={WOOD} stroke={OL} strokeWidth={4} /><path d={`M ${bx + 20} ${f - 80} L ${bx + 20} ${f} M ${bx + 360} ${f - 80} L ${bx + 360} ${f}`} stroke={OL} strokeWidth={10} />
          <ellipse cx={bx + 90} cy={f - 162} rx={50} ry={22} fill="#E3F2FD" stroke={OL} strokeWidth={4} />
          <path d={`M ${bx + 80} ${f - 160} Q ${bx + 220} ${f - 210} ${bx + 360} ${f - 160}`} fill="#9FC5E8" stroke={OL} strokeWidth={4} />
          {sens > 0 && <rect x={bx + 60} y={f - 92} width={260} height={10} rx={5} fill={CY} opacity={sens * (0.6 + 0.4 * Math.sin(t * 4 + b))} />}</g>; })}
      {sens > 0 && <g transform={`translate(560 ${f - 540})`} opacity={sens}><rect x={-170} y={-70} width={340} height={150} rx={12} fill="#263238" stroke={OL} strokeWidth={5} />
        {[0, 1].map((l) => <path key={l} d={Array.from({length: 30}, (_, q) => `${q ? 'L' : 'M'} ${-150 + q * 10} ${-20 + l * 60 + 12 * Math.sin(q * 0.8 + t * 3 + l)}`).join(' ')} stroke={l ? GOLD : CY} strokeWidth={4} fill="none" />)}
        <path d={`M -150 70 L 150 70`} stroke="#546E7A" strokeWidth={2} /><T x={0} y={-80} s={20} c={OL}>SLEEP SENSORS</T></g>}
      {/* lift-assist machine */}
      <g transform={`translate(1300 ${f})`}><rect x={-40} y={-30} width={260} height={30} rx={8} fill="#90A4AE" stroke={OL} strokeWidth={4} />
        <rect x={-20} y={-380} width={40} height={350} fill="#CFD8DC" stroke={OL} strokeWidth={4} />
        <path d={`M 0 -370 L 180 -370`} stroke={OL} strokeWidth={10} /><path d={`M 160 -370 L 160 ${-300 + 60 * (1 - lift)}`} stroke={OL} strokeWidth={4} />
        <g transform={`translate(160 ${-240 + 60 * (1 - lift) - 40 * lift})`}><path d="M -50 0 Q 0 50 50 0" stroke={TEAL} strokeWidth={14} fill="none" />
          {person(0, 30, 0.8, 1, t, '#9575CD', true)}</g>
        <circle cx={0} cy={10} r={12} fill={OL} /><circle cx={200} cy={10} r={12} fill={OL} />
        <g transform="translate(380 0)"><rect x={-60} y={-130} width={120} height={20} fill="#546E7A" stroke={OL} strokeWidth={3} /><path d="M -50 -110 L -50 -230 M 50 -110 L 50 -170" stroke={OL} strokeWidth={8} />
          <circle cx={-30} cy={-40} r={40} fill="none" stroke={OL} strokeWidth={8} /><circle cx={40} cy={-14} r={14} fill={OL} /></g></g>
      {/* tea table */}
      <g transform={`translate(2150 ${f})`}><rect x={-160} y={-150} width={320} height={22} fill={WOOD} stroke={OL} strokeWidth={4} /><path d="M -130 -128 L -130 0 M 130 -128 L 130 0" stroke={OL} strokeWidth={10} />
        <path d="M -40 -150 Q -40 -200 0 -200 Q 40 -200 40 -150 Z" fill="#7FB08C" stroke={OL} strokeWidth={4} />
        {[-100, 90].map((cx) => <rect key={cx} x={cx - 14} y={-174} width={28} height={24} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}
        {[0, 1].map((k) => { const u = (t * 0.7 + k * 0.5) % 1; return <path key={k} d={`M ${-100 + k * 190} ${-180 - u * 40} q 6 -10 0 -20`} stroke="#B0BEC5" strokeWidth={3} fill="none" opacity={1 - u} />; })}</g>
      {z.need && t >= (z.needAt ?? 0) && <g transform={`translate(1800 ${f - 560}) scale(${pop(t, z.needAt ?? 0)})`}>
        <rect x={-210} y={-60} width={420} height={120} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <T x={0} y={-16} s={24} c="#5E6B85">CAREGIVERS NEEDED</T><T x={0} y={34} s={fit(String(z.need), 380, 40)} c={RED}>{z.need}</T></g>}
    </g>;
  },

  /** a sepia late-1960s car plant with an early hydraulic robot */
  jhist: (t, z, f) => {
    const aU = pop(t, z.armAt ?? 0.5, 0.6), sw = Math.sin(t * 1.6);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#E8D9BC" />
      {Array.from({length: 6}, (_, k) => <path key={'sk' + k} d={`M ${-100 + k * 420} ${f - 600} L ${100 + k * 420} ${f - 700} L ${300 + k * 420} ${f - 600} Z`} fill="#D6C29C" stroke="#6B5A40" strokeWidth={4} />)}
      <rect x={z.x0} y={f - 600} width={z.x1 - z.x0} height={14} fill="#9C8763" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#BFA982" />
      {/* car bodies on a line */}
      {[0, 1, 2, 3].map((k) => { const x = ((k * 520 + t * 40) % 2400) - 300;
        return <g key={'cb' + k} transform={`translate(${x} ${f - 40})`}><path d="M -160 0 L -160 -70 Q -110 -80 -80 -120 L 60 -120 Q 100 -80 160 -70 L 160 0 Z" fill="#C9B48E" stroke="#5B4A33" strokeWidth={5} />
          {[-100, 100].map((wx) => <circle key={wx} cx={wx} cy={0} r={26} fill="#5B4A33" />)}</g>; })}
      <rect x={z.x0} y={f - 40} width={z.x1 - z.x0} height={40} fill="#8C7A5B" stroke="#5B4A33" strokeWidth={4} />
      {/* early hydraulic robot: boxy body with a telescoping arm */}
      <g transform={`translate(1150 ${f - 40}) scale(${aU})`}>
        <rect x={-90} y={-160} width={180} height={160} rx={10} fill="#A88E62" stroke="#4A3B26" strokeWidth={6} />
        <g transform={`translate(0 -190) rotate(${-8 + 10 * sw})`}><rect x={-60} y={-40} width={120} height={70} rx={12} fill="#BBA174" stroke="#4A3B26" strokeWidth={6} />
          <rect x={50} y={-22} width={180 + 40 * Math.sin(t * 1.6 + 1)} height={34} fill="#9C8763" stroke="#4A3B26" strokeWidth={5} />
          <path d={`M ${235 + 40 * Math.sin(t * 1.6 + 1)} -24 l 30 -16 M ${235 + 40 * Math.sin(t * 1.6 + 1)} 10 l 30 16`} stroke="#4A3B26" strokeWidth={8} strokeLinecap="round" />
          {t > (z.armAt ?? 0.5) + 0.6 && Array.from({length: 4}, (_, q) => { const u = (t * 3 + q / 4) % 1; return <circle key={q} cx={270 + u * 40} cy={-10 + u * 60} r={4} fill="#FFF3B0" opacity={1 - u} />; })}</g></g>
      {[260, 520, 1700, 1950].map((px, k) => <g key={'w' + k} opacity={0.95}>{person(px, f - 40, 1.1, k, t, ['#7D6B52', '#8E7A5C', '#6F5E46', '#9A8563'][k])}</g>)}
      <g transform={`translate(1750 ${f - 470})`}><rect x={-90} y={-80} width={180} height={150} fill="#F3E9D4" stroke="#5B4A33" strokeWidth={5} />
        <rect x={-90} y={-80} width={180} height={36} fill="#B5543A" stroke="#5B4A33" strokeWidth={4} /><T x={0} y={40} s={56} c="#5B4A33">{z.year || '1969'}</T></g>
      {z.helpAt !== undefined && t >= z.helpAt && <g transform={`translate(400 ${f - 470}) rotate(-3) scale(${pop(t, z.helpAt)})`}>
        <rect x={-150} y={-60} width={300} height={110} fill="#F3E9D4" stroke="#5B4A33" strokeWidth={5} /><T x={0} y={-10} s={30} c="#B5543A">WORKERS</T><T x={0} y={30} s={30} c="#B5543A">WANTED</T></g>}
    </g>;
  },

  /** robot maker's plant: crates to the world or to Japan */
  jfactory: (t, z, f) => {
    const share = clamp(kf(z.share, t, 0.5)), dests: string[] = z.dests || ['AMERICAS', 'EUROPE', 'CHINA', 'ASIA', 'AMERICAS', 'EUROPE', 'ASIA', 'CHINA', 'JAPAN'];
    const N = 10;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EEF2F6" />
      {Array.from({length: 7}, (_, k) => <rect key={'sl' + k} x={-200 + k * 400} y={f - 700} width={240} height={60} fill="#CFE8F5" stroke={OL} strokeWidth={4} />)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#B9C3CE" />
      {Array.from({length: 20}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 300} ${f + 20} L ${z.x0 + k * 300 + 150} ${f + 20}`} stroke={GOLD} strokeWidth={8} />)}
      {/* conveyor */}
      <rect x={-200} y={f - 130} width={1900} height={40} fill="#5B6B82" stroke={OL} strokeWidth={5} />
      {Array.from({length: 24}, (_, k) => <circle key={'rl' + k} cx={-180 + k * 80 + ((t * 120) % 80)} cy={f - 110} r={10} fill="#90A4AE" stroke={OL} strokeWidth={2} />)}
      {/* parts riding the belt: base -> half arm -> full arm (robots building robots) */}
      {Array.from({length: 6}, (_, k) => { const x = ((k * 320 + t * 120) % 1920) - 200, st = x < 300 ? 0 : x < 900 ? 1 : 2;
        return <g key={'pt' + k} transform={`translate(${x} ${f - 130})`}><rect x={-34} y={-30} width={68} height={30} rx={6} fill="#5B6B82" stroke={OL} strokeWidth={3} />
          {st >= 1 && <rect x={-14} y={-90} width={28} height={60} rx={10} fill={ORANGE} stroke={OL} strokeWidth={3} />}
          {st >= 2 && <rect x={-10} y={-136} width={60} height={22} rx={10} fill={ORANGE} stroke={OL} strokeWidth={3} transform="rotate(-25 0 -100)" />}</g>; })}
      {[200, 600, 1000, 1400].map((ax, k) => { const c = cyc(t, 2.6, [[30, 70, 40, 1], [10, 40, 60, 0], [-20, 50, 70, 1]], k * 0.6);
        return <g key={'fa' + k}>{armFK(ax, f - 140, 0.9, c.v[0], c.v[1], c.v[2], c.v[3], k % 2 ? ORANGE : '#F2A541', 'fa' + k, k % 2 ? 'arm' : undefined)}</g>; })}
      {z.plaque && plaque(700, f - 600, z.plaque, NAVY, 30, '#FFFFFF')}
      {/* doors */}
      <g transform={`translate(1900 ${f})`}><rect x={0} y={-460} width={520} height={460} fill="#2D8FD0" stroke={OL} strokeWidth={6} />
        <path d={`M 0 -200 Q 260 -230 520 -200 L 520 0 L 0 0 Z`} fill="#1F6FA8" />
        <g transform={`translate(260 -150)`}><path d="M -200 0 L 200 0 L 160 70 L -170 70 Z" fill="#E5483B" stroke={OL} strokeWidth={5} />
          {[-120, -40, 40, 120].map((cx, q) => <rect key={q} x={cx - 34} y={-60} width={68} height={60} fill={[ORANGE, GOLD, GREEN, BLUE][q]} stroke={OL} strokeWidth={4} />)}</g>
        {plaque(260, -400, 'TO THE WORLD', '#FFFFFF', 30)}</g>
      <g transform={`translate(2500 ${f})`}><rect x={0} y={-260} width={260} height={260} fill="#DDE3EA" stroke={OL} strokeWidth={6} />
        <rect x={40} y={-110} width={150} height={70} fill="#F4F6F8" stroke={OL} strokeWidth={4} />
        <circle cx={70} cy={-30} r={18} fill={OL} /><circle cx={170} cy={-30} r={18} fill={OL} />
        {plaque(130, -210, 'JAPAN', '#FFFFFF', 30)}</g>
      {Array.from({length: N}, (_, k) => { const u = ((t * 0.22 + k / N) % 1), toWorld = (k + 0.5) / N <= share + 1e-6;
        const x = toWorld ? lerp(1600, 2160, u) : lerp(1600, 2630, u), y = f - 30 - Math.sin(u * Math.PI) * 40;
        return <g key={'cr' + k} transform={`translate(${x} ${y})`} opacity={u < 0.9 ? 1 : (1 - u) * 10}>
          <rect x={-46} y={-60} width={92} height={60} rx={4} fill={toWorld ? '#D9A86C' : '#C5D3E0'} stroke={OL} strokeWidth={4} />
          <T x={0} y={-22} s={14} c={OL}>{toWorld ? dests[k % (dests.length - 1)] : 'JAPAN'}</T></g>; })}
    </g>;
  },

  /** robots per 100 factory workers: rows [{label, n, at, color}] */
  jdensity: (t, z, f) => {
    const rows: any[] = z.rows || [];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#F1F4F8" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#C9D2DE" />
      {rows.map((r, k) => { const y0 = 230 + k * 330, n = Number(r.n), shown = clamp((t - r.at) / 1.6) * n;
        return <g key={'row' + k}>
          <rect x={120} y={y0 - 40} width={1680} height={260} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <T x={270} y={y0 + 40} s={48} c={r.color || NAVY}>{r.label}</T>
          <T x={270} y={y0 + 90} s={20} c="#5E6B85">PER 100 FACTORY WORKERS</T>
          {Array.from({length: Math.ceil(n)}, (_, q) => { const v = clamp(shown - q); if (v <= 0) return null; const frac = Math.min(1, n - q);
            return <g key={q} transform={`translate(${480 + q * 108} ${y0 + 170}) scale(${E.outBack(v)})`} opacity={frac < 1 ? 0.45 : 1}>{armFK(0, 0, 0.38, 20 + 8 * Math.sin(t * 2 + q), 50, 30, 0.5, r.color || ORANGE, 'd' + k + q, undefined)}</g>; })}
        </g>; })}
    </g>;
  },

  /** convenience-store interior with a restocking arm behind the drink fridge */
  jkonbini: (t, z, f) => {
    const cut = clamp(kf(z.cut, t, 0)), stock = clamp(kf(z.stock, t, 0.4));
    const fx = 820, fy = f - 560, cols = 5, rowsN = 4, cw = 150, rh = 110, slots = cols * rowsN, filled = Math.floor(stock * slots);
    const fum = z.fumbleAt !== undefined ? t - z.fumbleAt : -1;
    const tgt = Math.min(slots - 1, filled), tc = tgt % cols, tr = Math.floor(tgt / cols);
    const ax = fx + 75 + tc * cw, ay = fy + 60 + tr * rh;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#FDFBF6" />
      <rect x={z.x0} y={f - 660} width={z.x1 - z.x0} height={24} fill={TEAL} />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#E3E6EA" />
      {Array.from({length: 20}, (_, k) => <path key={'tl' + k} d={`M ${z.x0 + k * 160} ${f} L ${z.x0 + k * 160} ${f + 300}`} stroke="#CDD2D8" strokeWidth={3} />)}
      {/* snack shelves (no brands) */}
      {[0, 1].map((s) => <g key={'sh' + s} transform={`translate(${60 + s * 340} ${f})`}><rect x={0} y={-420} width={300} height={420} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
        {[0, 1, 2, 3].map((r) => <g key={r}><rect x={0} y={-420 + r * 105 + 90} width={300} height={12} fill="#B0BEC5" stroke={OL} strokeWidth={2} />
          {Array.from({length: 6}, (_, q) => <rect key={q} x={14 + q * 47} y={-420 + r * 105 + 36} width={38} height={54} rx={5} fill={['#FFB74D', '#E57373', '#81C784', '#64B5F6', '#FFD54F', '#BA68C8'][(q + r + s) % 6]} stroke={OL} strokeWidth={2.5} />)}</g>)}</g>)}
      {/* drink fridge */}
      <rect x={fx - 30} y={fy - 40} width={cols * cw + 60} height={rowsN * rh + 100} fill="#CFD8DC" stroke={OL} strokeWidth={6} />
      {cut > 0 && <g opacity={cut}><rect x={fx} y={fy - 20} width={cols * cw} height={rowsN * rh + 40} fill="#2B3445" />
        <path d={`M ${fx} ${fy - 10} L ${fx + cols * cw} ${fy - 10}`} stroke="#90A4AE" strokeWidth={10} />
        {armFK(ax, ay + 90 + (fum >= 0 && fum < 1.6 ? 0 : 0), 0.42, -10, 40, 50, 0.4, '#ECEFF1', 'kn', fum >= 0 && fum < 0.4 ? undefined : 'bottle', false)}
        <rect x={ax - 40} y={fy - 30} width={80} height={30} rx={6} fill={ORANGE} stroke={OL} strokeWidth={4} /></g>}
      {Array.from({length: slots}, (_, k) => { const c = k % cols, r = Math.floor(k / cols); const on = k < filled;
        return on ? <g key={'bt' + k}>{[0, 1, 2].map((q) => <g key={q} transform={`translate(${fx + 30 + c * cw + q * 40} ${fy + 20 + r * rh})`}><rect x={-12} y={0} width={26} height={60} rx={9} fill={[CY, '#FF8A65', '#A5D6A7', GOLD][(k + q) % 4]} stroke={OL} strokeWidth={2.5} />
          <rect x={-6} y={-10} width={14} height={12} fill="#FFFFFF" stroke={OL} strokeWidth={2} /></g>)}</g> : null; })}
      {Array.from({length: rowsN}, (_, r) => <rect key={'sr' + r} x={fx} y={fy + 82 + r * rh} width={cols * cw} height={8} fill="#90A4AE" />)}
      {Array.from({length: cols}, (_, c) => <rect key={'gd' + c} x={fx + c * cw + 4} y={fy - 20} width={cw - 8} height={rowsN * rh + 40} fill="#DDF3FF" opacity={0.22 * (1 - cut * 0.7)} stroke={OL} strokeWidth={4} />)}
      {fum >= 0 && fum < 2.2 && <g transform={`translate(${ax + 20} ${ay + 40 + Math.min(260, 300 * fum * fum)}) rotate(${fum * 400})`}><rect x={-12} y={-30} width={26} height={60} rx={9} fill={CY} stroke={OL} strokeWidth={3} /></g>}
      {/* counter + register */}
      <g transform={`translate(1900 ${f})`}><rect x={0} y={-200} width={480} height={200} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={0} y={-200} width={480} height={20} fill={TEAL} stroke={OL} strokeWidth={3} />
        <rect x={300} y={-290} width={120} height={90} rx={8} fill="#455A64" stroke={OL} strokeWidth={4} /><rect x={312} y={-280} width={96} height={46} fill="#A5D6A7" /></g>
      {z.vrAt !== undefined && t >= z.vrAt && <g transform={`translate(1500 ${f - 640}) scale(${pop(t, z.vrAt)})`}>
        <path d={`M ${ax - 1500} ${ay - f + 640} Q -80 120 -10 60`} stroke={CY} strokeWidth={5} strokeDasharray="12 10" fill="none" />
        <circle cx={120} cy={0} r={130} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {person(120, 110, 0.8, 2, t, '#5C6BC0')}<rect x={84} y={-30} width={72} height={30} rx={10} fill="#263238" stroke={OL} strokeWidth={3} />
        <T x={120} y={-150} s={24} c={NAVY}>REMOTE OPERATOR</T></g>}
    </g>;
  },

  /** retired demo robot / arm at work / humanoid prototype */
  jdemo: (t, z, f) => {
    const c1 = pop(t, z.caseAt ?? 0.3), c2 = pop(t, z.workAt ?? 1.0), c3 = pop(t, z.protoAt ?? 2.0);
    const humanoid = (x: number, y: number, s: number, col: string, walk: number) => <g transform={`translate(${x} ${y}) scale(${s})`}>
      <path d={`M -18 0 L -18 -90 M 18 0 L 18 -90`} stroke={OL} strokeWidth={26} strokeLinecap="round" /><path d={`M -18 0 L -18 -90 M 18 0 L 18 -90`} stroke={col} strokeWidth={18} strokeLinecap="round" transform={`rotate(${walk} 0 -90)`} />
      <rect x={-50} y={-210} width={100} height={130} rx={24} fill={col} stroke={OL} strokeWidth={5} />
      <path d="M -50 -190 L -80 -110 M 50 -190 L 80 -110" stroke={OL} strokeWidth={20} strokeLinecap="round" /><path d="M -50 -190 L -80 -110 M 50 -190 L 80 -110" stroke={col} strokeWidth={13} strokeLinecap="round" />
      <rect x={-36} y={-280} width={72} height={64} rx={18} fill={col} stroke={OL} strokeWidth={5} /><rect x={-26} y={-266} width={52} height={24} rx={10} fill="#263238" />
      <circle cx={-10} cy={-254} r={4} fill={CY} /><circle cx={10} cy={-254} r={4} fill={CY} /></g>;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EEF0F5" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#CBD2DC" />
      {[0, 1].map((k) => <rect key={k} x={620 + k * 680} y={f - 700} width={12} height={700} fill="#D5DBE4" />)}
      {/* 1: retired, under glass */}
      <g transform={`translate(300 ${f}) scale(${c1})`}><rect x={-160} y={-60} width={320} height={60} fill="#8E9AAF" stroke={OL} strokeWidth={5} />
        {humanoid(0, -60, 1.1, '#F4F6F8', 0)}
        <path d="M -150 -60 L -150 -420 Q 0 -500 150 -420 L 150 -60" fill="#DDF3FF" opacity={0.35} stroke={OL} strokeWidth={5} />
        {plaque(0, -540, 'RETIRED · DEMOS ONLY', '#FFFFFF', 24)}</g>
      {/* 2: at work today */}
      <g transform={`translate(960 ${f}) scale(${c2})`}>{(() => { const c = cyc(t, 2.4, [[40, 70, 40, 1], [-30, -60, -30, 0]]); return armFK(0, 0, 1.0, c.v[0], c.v[1], c.v[2], c.v[3], ORANGE, 'dw', c.i === 0 ? 'part' : undefined); })()}
        <rect x={160} y={-150} width={200} height={24} fill={WOOD} stroke={OL} strokeWidth={4} />{[0, 1, 2].map((q) => <rect key={q} x={180 + q * 50} y={-180} width={30} height={30} rx={5} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}
        {plaque(60, -540, 'AT WORK TODAY', GREEN, 28, '#FFFFFF')}</g>
      {/* 3: humanoid prototype on a test stand */}
      <g transform={`translate(1640 ${f}) scale(${c3})`}><rect x={-170} y={-40} width={340} height={40} fill="#5B6B82" stroke={OL} strokeWidth={5} />
        <path d="M -140 -40 L -140 -470 L 140 -470 L 140 -40" stroke="#90A4AE" strokeWidth={12} fill="none" /><path d="M 0 -470 L 0 -380" stroke={OL} strokeWidth={4} />
        {humanoid(0, -40, 1.05, '#B3C7E6', 14 * Math.sin(t * 2))}
        <path d="M -140 -200 Q -90 -180 -60 -150" stroke={GOLD} strokeWidth={5} fill="none" /><path d="M 140 -260 Q 90 -230 60 -190" stroke={RED} strokeWidth={5} fill="none" />
        {plaque(0, -540, z.protoText || 'PROTOTYPE · A PLAN', PURPLE, 26, '#FFFFFF')}</g>
    </g>;
  },

  /** the yen shrinks beside the dollar */
  jyen: (t, z, f) => {
    const sh = clamp(kf(z.shrink, t, 0)), r = 230 * (1 - 0.286 * sh);
    const out = z.outAt !== undefined ? clamp((t - z.outAt) / 1.2) : 0, inn = z.inAt !== undefined ? clamp((t - z.inAt) / 1.2) : 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#FFF7E8" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#E8D7B5" />
      <g transform={`translate(640 ${f - 330})`}><circle r={r + 8} fill="#B0BEC5" opacity={sh * 0.35} strokeDasharray="12 10" stroke={OL} strokeWidth={3} />
        <circle r={r} fill="#D9DEE3" stroke={OL} strokeWidth={8} /><circle r={r * 0.82} fill="none" stroke="#9AA4AE" strokeWidth={5} />
        <T x={0} y={r * 0.32} s={r * 0.9} c="#5B6B82">¥</T></g>
      <g transform={`translate(1300 ${f - 330})`}><circle r={230} fill="#E7C66A" stroke={OL} strokeWidth={8} /><circle r={190} fill="none" stroke="#C9A440" strokeWidth={5} />
        <T x={0} y={74} s={210} c="#7A5A12">$</T></g>
      {out > 0 && <g transform={`translate(${lerp(900, 1900, out)} ${f - 60})`}><rect x={-60} y={-70} width={120} height={70} fill="#D9A86C" stroke={OL} strokeWidth={4} />
        <T x={0} y={-26} s={18}>ROBOTS</T>{banner(0, -120, 'CHEAPER ABROAD', GREEN, 22)}</g>}
      {inn > 0 && ['CHIPS', 'FUEL', 'SOFTWARE'].map((lb, q) => <g key={lb} transform={`translate(${lerp(2300, 200 + q * 170, clamp(inn * 1.2 - q * 0.1))} ${f - 40})`}>
        <rect x={-70} y={-60} width={140} height={60} rx={6} fill={[PURPLE, '#8D6E63', BLUE][q]} stroke={OL} strokeWidth={4} /><T x={0} y={-22} s={18} c="#FFFFFF">{lb}</T></g>)}
      {inn > 0.6 && banner(400, f - 170, 'PRICIER AT HOME', RED, 22)}
    </g>;
  },

  /** the catch: a balance */
  jscale: (t, z, f) => {
    const ws: any[] = z.weights || [], tilt = kf(z.tilt, t, 0), ang = 14 * tilt;
    const cx = 960, cy = f - 520, L = 560, r = (ang * Math.PI) / 180;
    const lx = cx - L * Math.cos(r), ly = cy - L * Math.sin(r), rx = cx + L * Math.cos(r), ry = cy + L * Math.sin(r);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#F3F0FA" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={300} fill="#D7D0E6" />
      <path d={`M ${cx - 120} ${f} L ${cx} ${cy} L ${cx + 120} ${f} Z`} fill="#8E7CC3" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <path d={`M ${lx} ${ly} L ${rx} ${ry}`} stroke={OL} strokeWidth={22} strokeLinecap="round" /><path d={`M ${lx} ${ly} L ${rx} ${ry}`} stroke={GOLD} strokeWidth={12} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={22} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      {[[lx, ly], [rx, ry]].map(([px, py], k) => <g key={'pan' + k}><path d={`M ${px} ${py} L ${px - 150} ${py + 220} M ${px} ${py} L ${px + 150} ${py + 220}`} stroke={OL} strokeWidth={4} />
        <path d={`M ${px - 190} ${py + 220} L ${px + 190} ${py + 220} Q ${px} ${py + 300} ${px - 190} ${py + 220} Z`} fill="#CFD8DC" stroke={OL} strokeWidth={5} /></g>)}
      <g transform={`translate(${lx} ${ly + 220})`}>{armFK(-60, 0, 0.45, 20 + 10 * Math.sin(t * 2), 50, 30, 0.5, ORANGE, 'sc')}<rect x={20} y={-80} width={140} height={80} rx={10} fill={CY} stroke={OL} strokeWidth={4} /><T x={90} y={-30} s={24} c={NAVY}>AI</T>
        {plaque(0, 120, z.leftText || 'ROBOTS + AI', GREEN, 26, '#FFFFFF')}</g>
      {ws.map((w, k) => { const u = clamp((t - w.at) / 0.6); if (u <= 0) return null; const big = !!w.big, ww = big ? 260 : 190, hh = big ? 150 : 100;
        const sx = rx - 120 + k * 120 - (big ? 60 : 0), sy = lerp(ry - 700, ry + 220, E.outBack(u));
        return <g key={'wt' + k} transform={`translate(${sx} ${sy})`}><path d={`M ${-ww / 2} 0 L ${ww / 2} 0 L ${ww / 2 - 24} ${-hh} L ${-ww / 2 + 24} ${-hh} Z`} fill={w.color || '#5B6B82'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <T x={0} y={-hh / 2 + 9} s={fit(String(w.label), ww - 40, big ? 34 : 24)} c="#FFFFFF">{w.label}</T></g>; })}
    </g>;
  },

  /** title card: KOBO writes the title over Hoshimachi */
  jtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['WILL AI MAKE', 'JAPAN RICH', 'AGAIN?'];
    const c = cyc(t, 1.4, [[30, 50, 20, 0.5], [10, 30, 40, 0.5], [40, 60, 10, 0.5]]);
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#FCEBD3" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(960 900) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#F9DDB8' : '#FCEBD3'} />)}
      <path d={ridge(-200, 2200, 900, 160, 200, 1)} fill="#9EC4B0" stroke={OL} strokeWidth={4} />
      <path d={ridge(-200, 2200, 980, 90, 140, 3)} fill="#6FA584" stroke={OL} strokeWidth={4} />
      {[200, 420, 1480, 1700].map((x, k) => <g key={k} transform={`translate(${x} 1000) scale(0.55)`}><rect x={0} y={-200} width={300} height={200} fill="#E9D8B8" stroke={OL} strokeWidth={6} />
        <path d="M -20 -200 L 320 -200 L 290 -250 L 10 -250 Z" fill={ROOF} stroke={OL} strokeWidth={6} /></g>)}
      <g transform="translate(1650 760)">{armFK(0, 0, 1.0, c.v[0], c.v[1], c.v[2], c.v[3], ORANGE, 'tt')}</g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.6) / 0.5) * ln.length); return <T key={k} x={860} y={220 + k * 140} s={fit(ln, 1400, k === lines.length - 1 ? 150 : 110)} c={k === lines.length - 1 ? RED : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={860} y={680} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a workshop roll shutter rolls up on the chapter title */
  jbumper: (t, z, f) => {
    const c = z.color || BLUE, up = E.inOut(win(t, 0.3, 0.9));
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g opacity={clamp((t - 0.5) / 0.3)}><T x={960} y={330} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={420} width={1200} height={140} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={960} y={512} s={fit(z.title || '', 1140, 62)} c="#FFFFFF">{z.title || ''}</T>
        {t >= 1.4 && <T x={960} y={680} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.4) / 0.3)}>{z.caption || ''}</T>}</g>
      <g transform={`translate(0 ${-1150 * up})`}><rect x={-200} y={-200} width={2400} height={1300} fill="#AEB7C2" stroke={OL} strokeWidth={6} />
        {Array.from({length: 46}, (_, k) => <path key={'sl' + k} d={`M -200 ${-200 + k * 28} L 2200 ${-200 + k * 28}`} stroke="#8E99A6" strokeWidth={4} />)}
        <rect x={880} y={1020} width={160} height={30} rx={8} fill="#5B6B82" stroke={OL} strokeWidth={4} /></g>
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const JAPAN_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

/** jtag: top-left claim pill */
const TAGC: Record<string, string> = {FACT: GREEN, PROJECTION: PURPLE, ESTIMATE: ORANGE, OUR: TEAL, COMPANY: '#8D6E63', PLAN: PURPLE, FINDING: BLUE, STORY: '#5E6B85', MECHANISM: BLUE, VERDICT: NAVY, LIBRARY: NAVY, ANALYSIS: NAVY};
const jtag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const txt: string = pick(a.tags, t, a.text || 'FACT'); if (!txt) return null;
  const key = txt.split(' ')[0], c = TAGC[key] || NAVY, w = txt.length * 17 + 70, x = kf(a.x, t, 36), y = kf(a.y, t, 36), t0 = Math.max(at, lastAt(a.tags, t));
  return <g key={'jt' + i} transform={`translate(${x} ${y}) scale(${pop(t, t0, 0.35)})`}>
    <rect x={0} y={0} width={w} height={46} rx={23} fill={c} stroke={OL} strokeWidth={4} />
    <circle cx={26} cy={23} r={9} fill="#FFFFFF" /><T x={44} y={32} s={24} a="start" c="#FFFFFF">{txt}</T></g>;
};

/** kobo: the cobot mascot on a little cart with a screen face */
const kobo: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4), face = pick(a.faces, t, a.face || 'happy');
  let wv = 0; for (const h of (a.wave || []) as number[]) { const u = t - h; if (u >= 0 && u < 1.4) wv = Math.sin(u * 14) * (1 - u / 1.4); }
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, roll = t * vx * 0.02;
  return <g key={'kb' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-80} y={-60} width={160} height={50} rx={12} fill="#5B6B82" stroke={OL} strokeWidth={5} />
    {[-50, 50].map((wx) => <g key={wx} transform={`translate(${wx} -6) rotate(${roll * 57})`}><circle r={18} fill="#37474F" stroke={OL} strokeWidth={4} /><path d="M -12 0 L 12 0" stroke="#90A4AE" strokeWidth={3} /></g>)}
    {armFK(0, -60, 0.6, 20 + 40 * wv, 40 - 30 * wv, 30, 0.5 + 0.5 * Math.abs(wv), ORANGE, 'kbm' + i, a.carry === 'part' ? 'part' : undefined)}
    <g transform="translate(0 -130)"><rect x={-44} y={-30} width={88} height={56} rx={14} fill="#263238" stroke={OL} strokeWidth={4} />
      {face === 'think' ? <g><rect x={-24} y={-8} width={14} height={6} rx={3} fill={CY} /><rect x={10} y={-8} width={14} height={6} rx={3} fill={CY} /></g>
        : <g><circle cx={-16} cy={-6} r={7} fill={CY} /><circle cx={16} cy={-6} r={7} fill={CY} /></g>}
      {face === 'worry' ? <path d="M -14 14 Q 0 6 14 14" stroke={CY} strokeWidth={4} fill="none" /> : <path d="M -14 8 Q 0 18 14 8" stroke={CY} strokeWidth={4} fill="none" />}</g>
  </g>;
};

export const JAPAN_ITEMS: Record<string, ItemFn> = {jtag, kobo};
export const JAPAN_INDOOR = ['jshop', 'jplatform', 'jcare', 'jhist', 'jfactory', 'jdensity', 'jkonbini', 'jdemo', 'jyen', 'jscale', 'jtitle', 'jbumper'];
