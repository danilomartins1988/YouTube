import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * FACTORY kit for CartoonStage (Episode 60, "Why the World Still Depends on Chinese Factories").
 *
 * Prime-time sitcom look (genre level only; everything ORIGINAL), bright day scenes, no flags, seals, logos or brand names.
 * Respectful by design: workers and engineers are drawn as ordinary skilled professionals; no national caricature.
 * Sets:
 *  - megafloor: the giant "everything" factory floor (skylights, five product lines on conveyors, robot arms, overhead gantry,
 *    line signs `lines`, a big board `board`; `hi` highlights one line)
 *  - partsstreet: the supplier-cluster street (workshops `shops` with awnings and product piles, scooters zipping parts down
 *    the street to the FINAL ASSEMBLY hall at `asmX`; `hi` lights one shop; `rush` speeds traffic from a time)
 *  - megaport: container port (ship-to-shore gantry cranes lifting boxes, colourful stacks, a ship that fills, straddle carriers,
 *    a counter board `board`)
 *  - refinery: rare-earth separation hall (ore heap + dump truck at the door, a cascade of mixer-settler tanks with flowing
 *    liquor, element jars Nd/Pr/Dy/Tb, magnets rolling out; `stages` count)
 *  - solarline: solar panel line (POLYSILICON -> INGOT -> WAFER -> CELL -> MODULE; parts morph along the belt; `hi` stage)
 *  - tariffwall: a wall between a factory dock and a store that grows by dated rows `rows` [{at, label, h, color, out?}] and loses
 *    rows (they topple) at `out`; parcels hop over / bonk
 *  - movingday: a factory trying to move abroad (OLD PLANT with its supplier huddle on the left, sea strait with a little ship,
 *    NEW PLANT under construction on the right: `build` keyframes 0..1, `newName`, `suppliersAt` when the first supplier hut pops)
 *  - fctitle: show title card (rays, a turning gear, crates riding a conveyor that drop the title letters; `lines`, `sub`, `subs`)
 *  - fcbumper: act bumper (hazard-stripe wipe, crate badge with the act number, title plate, joke caption)
 * Items:
 *  - gizmo: the running gag, Mel's replacement toaster being assembled: `parts` [[t, label]] add pieces with a pop; `toastAt`
 *    pops toast; `stampAt`/`stamp` shows a tag; it has googly eyes (`face`)
 *  - homebox: a cardboard box on little legs that walks (x keyframes), `label`, `face`, `hop` times
 *  - stackbox: a stack of shipping containers (`cols`, `rows`, `fill` keyframes 0..1) with a pennant `text`
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS).
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

const TEAL = '#1F7A8C', ORANGE = '#FF9F1C', RED = '#E5484D', GREEN = '#2E9E5B', YEL = '#FFD23F', CREAM = '#FFF8E6', STEEL = '#90A4AE', BOX = '#D7A86E';
const CTR = ['#E5484D', '#1F7A8C', '#FF9F1C', '#2E9E5B', '#5C6BC0', '#F2C14E', '#26A69A', '#8E5BD6'];

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: number) => <path key={'cl' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
/** a cardboard box glyph centred at 0,0 */
const cbox = (w: number, h: number, label?: string, c = BOX) => <g>
  <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={4} fill={c} stroke={OL} strokeWidth={3.5} />
  <path d={`M ${-w / 2} ${-h / 2 + h * 0.28} L ${w / 2} ${-h / 2 + h * 0.28} M 0 ${-h / 2} L 0 ${-h / 2 + h * 0.28}`} stroke="#A9783F" strokeWidth={3} />
  {label && <T x={0} y={h * 0.26} s={fit(label, w - 8, h * 0.3)}>{label}</T>}
</g>;
/** product glyphs riding the lines */
const product = (kind: number, t: number, k: number) => {
  switch (kind % 6) {
    case 0: return <g><rect x={-30} y={-26} width={60} height={42} rx={12} fill="#ECEFF1" stroke={OL} strokeWidth={3.5} /><rect x={-18} y={-34} width={12} height={10} rx={2} fill="#B0BEC5" stroke={OL} strokeWidth={2.5} /><rect x={6} y={-34} width={12} height={10} rx={2} fill="#B0BEC5" stroke={OL} strokeWidth={2.5} /><circle cx={22} cy={0} r={4} fill={RED} /></g>; // toaster
    case 1: return <g><rect x={-14} y={-24} width={28} height={36} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><path d="M -6 -24 L -6 -32 M 6 -24 L 6 -32" stroke={OL} strokeWidth={3} /><path d="M 0 12 Q 0 26 20 26" stroke={OL} strokeWidth={3} fill="none" /></g>; // charger
    case 2: return <g><path d="M -34 10 L -34 -10 Q -20 -24 0 -14 L 14 -2 Q 30 0 34 10 Z" fill={['#FF7043', '#4FB3F6', '#7BD389'][k % 3]} stroke={OL} strokeWidth={3.5} strokeLinejoin="round" /><path d="M -34 10 L 34 10" stroke="#FFFFFF" strokeWidth={4} /></g>; // sneaker
    case 3: return <g><rect x={-16} y={-26} width={32} height={46} rx={5} fill={GREEN} stroke={OL} strokeWidth={3.5} /><rect x={-7} y={-32} width={14} height={7} rx={2} fill={STEEL} stroke={OL} strokeWidth={2} /><path d="M -4 -8 L 4 -8 M 0 -12 L 0 -4" stroke="#FFFFFF" strokeWidth={3} /></g>; // battery
    case 4: return <g><rect x={-34} y={-22} width={68} height={40} rx={3} fill="#1E4E8C" stroke={OL} strokeWidth={3.5} />{[-17, 0, 17].map((q) => <path key={q} d={`M ${q} -22 L ${q} 18`} stroke="#9EC9FF" strokeWidth={1.5} />)}<path d="M -34 -2 L 34 -2" stroke="#9EC9FF" strokeWidth={1.5} /></g>; // panel
    default: return <g><rect x={-22} y={-30} width={44} height={56} rx={8} fill="#263238" stroke={OL} strokeWidth={3.5} /><rect x={-16} y={-22} width={32} height={38} rx={3} fill="#80DEEA" opacity={0.6 + 0.3 * Math.sin(t * 3 + k)} /></g>; // phone
  }
};
/** an articulated robot arm at 0,0 (floor), swinging on a period, gripper opens */
const robotArm = (t: number, k: number, s = 1, color = ORANGE) => {
  const ph = (t * 0.9 + k * 0.37) % 1, a1 = -30 + 50 * Math.sin(ph * Math.PI * 2), a2 = 60 + 40 * Math.cos(ph * Math.PI * 2);
  const r1 = (a1 * Math.PI) / 180, r2 = ((a1 + a2) * Math.PI) / 180;
  const ex = Math.sin(r1) * 120, ey = -Math.cos(r1) * 120 - 60, hx = ex + Math.sin(r2) * 100, hy = ey + Math.cos(r2) * 100;
  return <g transform={`scale(${s})`}>
    <rect x={-50} y={-30} width={100} height={30} rx={8} fill="#546E7A" stroke={OL} strokeWidth={4} />
    <rect x={-26} y={-70} width={52} height={44} rx={10} fill={color} stroke={OL} strokeWidth={4} />
    <path d={`M 0 -60 L ${ex} ${ey} L ${hx} ${hy}`} stroke={OL} strokeWidth={30} strokeLinecap="round" strokeLinejoin="round" fill="none" />
    <path d={`M 0 -60 L ${ex} ${ey} L ${hx} ${hy}`} stroke={color} strokeWidth={20} strokeLinecap="round" strokeLinejoin="round" fill="none" />
    <circle cx={0} cy={-60} r={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={ex} cy={ey} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
    <g transform={`translate(${hx} ${hy})`}><path d={`M -14 0 L ${-10 - 6 * Math.abs(Math.sin(ph * 6.28))} 22 M 14 0 L ${10 + 6 * Math.abs(Math.sin(ph * 6.28))} 22`} stroke={OL} strokeWidth={6} strokeLinecap="round" /><circle r={9} fill="#37474F" stroke={OL} strokeWidth={3} /></g>
  </g>;
};
/** a little generic worker silhouette (hard hat + overalls) for distant crowds; walk phase from t */
const worker = (x: number, y: number, s: number, k: number, t: number, walk = 0) => {
  const sw = walk ? Math.sin(t * 9 + k) * 18 : 0;
  return <g key={'wk' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    <path d={`M -8 -40 L ${-8 - sw * 0.5} 0 M 8 -40 L ${8 + sw * 0.5} 0`} stroke="#2B4A5E" strokeWidth={12} strokeLinecap="round" />
    <rect x={-18} y={-92} width={36} height={56} rx={12} fill={[TEAL, '#5C6BC0', '#26A69A', ORANGE][k % 4]} stroke={OL} strokeWidth={3.5} />
    <path d={`M -16 -84 L ${-26 - sw * 0.3} -48 M 16 -84 L ${26 + sw * 0.3} -48`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
    <circle cx={0} cy={-110} r={18} fill={['#F6CDA6', '#E0A878', '#B97A4B', '#F3D7BD'][k % 4]} stroke={OL} strokeWidth={3.5} />
    <path d="M -20 -112 Q 0 -146 20 -112 Z" fill={YEL} stroke={OL} strokeWidth={3.5} /><rect x={-23} y={-116} width={46} height={7} rx={3} fill={YEL} stroke={OL} strokeWidth={2.5} />
  </g>;
};

export const FACTORY_SETS: Record<string, SetFn> = {
  /** the EVERYTHING FACTORY floor */
  megafloor: (t, z, f) => {
    const w = z.x1 - z.x0, lines: string[] = z.lines || ['TOASTERS', 'CHARGERS', 'SNEAKERS', 'BATTERIES', 'SOLAR PANELS'], sp = z.speed ?? 140, hi0 = z.hiAt ? pick(z.hiAt, t, z.hi) : z.hi, hi = hi0 === null ? undefined : hi0;
    const board: string = z.board || 'TODAY: EVERYTHING';
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E8EEF2" />
      {/* skylight roof with daylight shafts */}
      <rect x={z.x0} y={f - 900} width={w} height={70} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const sx = z.x0 + k * 420 + 60; return <g key={'sl' + k}>
        <path d={`M ${sx} ${f - 900} L ${sx + 300} ${f - 900} L ${sx + 380} ${f - 830} L ${sx + 80} ${f - 830} Z`} fill="#CFEFFF" stroke={OL} strokeWidth={4} />
        <path d={`M ${sx + 80} ${f - 830} L ${sx + 380} ${f - 830} L ${sx + 560} ${f} L ${sx + 160} ${f} Z`} fill="#FFF8D6" opacity={0.28 + 0.04 * Math.sin(t * 0.8 + k)} /></g>; })}
      {/* back wall: windows + the big board */}
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'bw' + k} x={z.x0 + k * 300 + 40} y={f - 780} width={220} height={120} rx={8} fill="#D6ECF5" stroke={OL} strokeWidth={4} />)}
      <g transform={`translate(${z.boardX ?? 1100} ${f - 720})`}><rect x={-330} y={-56} width={660} height={100} rx={14} fill="#16232E" stroke={OL} strokeWidth={6} />
        <T x={0} y={14} s={fit(board, 600, 46)} c={YEL}>{board}</T>
        {[0, 1, 2, 3, 4, 5].map((q) => <circle key={q} cx={-300 + q * 120} cy={-44} r={6} fill={Math.floor(t * 4 + q) % 2 ? ORANGE : '#FFFFFF'} />)}</g>
      {/* overhead gantry crane carrying a crate back and forth */}
      <rect x={z.x0} y={f - 640} width={w} height={22} fill="#FFC93C" stroke={OL} strokeWidth={4} />
      {(() => { const gx = 400 + 900 * (0.5 + 0.5 * Math.sin(t * 0.45)), drop = 60 + 40 * Math.abs(Math.sin(t * 0.9));
        return <g transform={`translate(${gx} ${f - 640})`}><rect x={-60} y={-10} width={120} height={40} rx={6} fill={ORANGE} stroke={OL} strokeWidth={4} />
          <path d={`M -20 30 L -20 ${30 + drop} M 20 30 L 20 ${30 + drop}`} stroke={OL} strokeWidth={4} /><g transform={`translate(0 ${60 + drop})`}>{cbox(110, 70, 'PARTS')}</g></g>; })()}
      {/* five product lines at three depths */}
      {lines.map((ln, k) => { const ly = f - 540 + k * 108, sc = 1.0 + k * 0.14, on = hi === undefined || hi === k;
        return <g key={'ln' + k} opacity={on ? 1 : 0.55}>
          <rect x={z.x0} y={ly} width={w} height={26} fill="#455A64" stroke={OL} strokeWidth={4} />
          {Array.from({length: Math.ceil(w / 60)}, (_, q) => <circle key={q} cx={z.x0 + q * 60 + ((t * sp * (k % 2 ? -1 : 1)) % 60 + 60) % 60} cy={ly + 13} r={6} fill="#90A4AE" />)}
          {Array.from({length: Math.ceil(w / 200)}, (_, q) => { const px = z.x0 + (((q * 200 + t * sp * (k % 2 ? -1 : 1)) % w) + w) % w;
            return <g key={'p' + q} transform={`translate(${px} ${ly - 30 * sc}) scale(${sc})`}>{product(k === 4 ? 4 : k, t, q)}</g>; })}
          <g transform={`translate(${(z.signX ?? 200) + k * 40} ${ly - 70 * sc}) scale(${on && hi !== undefined ? 1 + 0.06 * Math.sin(t * 6) : 1})`}>
            <rect x={-110} y={-26} width={220} height={40} rx={10} fill={on && hi !== undefined ? YEL : '#FFFFFF'} stroke={OL} strokeWidth={3.5} />
            <T x={0} y={4} s={fit(`LINE ${k + 1} · ${ln}`, 200, 20)}>{`LINE ${k + 1} · ${ln}`}</T></g>
        </g>; })}
      {/* robot arms and workers along the front line */}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => <g key={'ra' + k} transform={`translate(${z.x0 + 350 + k * 700} ${f - 10})`}>{robotArm(t, k, 1.25, k % 2 ? TEAL : ORANGE)}</g>)}
      {Array.from({length: Math.ceil(w / 700)}, (_, k) => worker(z.x0 + 650 + k * 700 + Math.sin(t * 0.7 + k) * 30, f - 4, 1.15, k, t, 0))}
      {/* floor */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#CFD8DC" />
      <rect x={z.x0} y={f + 40} width={w} height={14} fill={YEL} opacity={0.9} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <rect key={'hz' + k} x={z.x0 + k * 80} y={f + 40} width={40} height={14} fill={OL} opacity={0.75} />)}
      <rect x={z.x0} y={f} width={w} height={16} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the SUPPLIER-CLUSTER street: every part is down the street */
  partsstreet: (t, z, f) => {
    const w = z.x1 - z.x0, shops: string[] = z.shops || ['SCREWS', 'CABLES', 'MOLDS', 'MOTORS', 'GLASS', 'BATTERIES', 'CIRCUIT BOARDS', 'SPRINGS'];
    const asm = z.asmX ?? 2500, x0s = z.shopX ?? -200, gap = z.gap ?? 330, rush = z.rushAt !== undefined && t > z.rushAt ? 1.8 : 1;
    const awn = ['#E5484D', '#1F7A8C', '#FF9F1C', '#2E9E5B', '#5C6BC0', '#F2C14E', '#26A69A', '#8E5BD6'];
    return <g>
      {sky(z, f, '#8FD3F4', '#E9F8FF', 'pssky' + Math.round(z.x0))}
      {[0, 1, 2, 3].map((k) => cloud(((k * 760 + t * 14) % (w + 600)) + z.x0 - 300, 150 + (k % 2) * 80, 1, k))}
      {/* distant hills and generic apartment blocks */}
      <path d={`M ${z.x0} ${f - 260} Q ${z.x0 + w * 0.25} ${f - 420} ${z.x0 + w * 0.5} ${f - 280} Q ${z.x0 + w * 0.75} ${f - 400} ${z.x1} ${f - 270} L ${z.x1} ${f} L ${z.x0} ${f} Z`} fill="#A9D18E" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => { const bx = z.x0 + k * 260 + rnd(k) * 80, bh = 220 + rnd(k + 9) * 180;
        return <g key={'ap' + k}><rect x={bx} y={f - 160 - bh} width={120} height={bh} fill={['#F3E3C3', '#D8E4EE', '#F1D3C6', '#DDEBD5'][k % 4]} stroke={OL} strokeWidth={4} />
          {Array.from({length: Math.floor(bh / 46)}, (_, r) => [0, 1, 2].map((c) => <rect key={r + '-' + c} x={bx + 14 + c * 34} y={f - 150 - bh + 14 + r * 46} width={22} height={24} rx={3} fill="#9FD3F0" stroke={OL} strokeWidth={2} />))}</g>; })}
      {/* workshops */}
      {shops.map((s, k) => { const sx = x0s + k * gap, on = z.hi === k || (Array.isArray(z.lit) && z.lit.some((p: any) => t >= p[0] && p[1] === k));
        return <g key={'sh' + k} transform={`translate(${sx} ${f})`}>
          <rect x={-140} y={-300} width={280} height={300} fill={['#FFF3E0', '#E8F5E9', '#E3F2FD', '#FCE4EC'][k % 4]} stroke={OL} strokeWidth={5} />
          <rect x={-150} y={-330} width={300} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-298} s={fit(s, 270, 28)}>{s}</T>
          <path d={`M -150 -286 L 150 -286 L 170 -230 L -170 -230 Z`} fill={awn[k % awn.length]} stroke={OL} strokeWidth={4} />
          {Array.from({length: 6}, (_, q) => <path key={q} d={`M ${-170 + q * 57} -230 q 28 22 57 0`} fill={q % 2 ? '#FFFFFF' : awn[k % awn.length]} stroke={OL} strokeWidth={3} />)}
          <rect x={-110} y={-200} width={130} height={200} fill="#5B6577" stroke={OL} strokeWidth={4} />
          {/* product pile in the window */}
          {[0, 1, 2].map((q) => <g key={q} transform={`translate(${70} ${-40 - q * 46}) scale(0.75)`}>{cbox(90, 50, s.split(' ')[0].slice(0, 7))}</g>)}
          {on && <g><circle cx={0} cy={-380} r={22 + 4 * Math.sin(t * 8)} fill={YEL} stroke={OL} strokeWidth={4} /><T x={0} y={-371} s={26}>!</T></g>}
        </g>; })}
      {/* final assembly hall */}
      <g transform={`translate(${asm} ${f})`}>
        <path d="M -260 0 L -260 -360 L 0 -460 L 260 -360 L 260 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <rect x={-210} y={-330} width={420} height={60} rx={10} fill={TEAL} stroke={OL} strokeWidth={4} /><T x={0} y={-290} s={34} c="#FFFFFF">FINAL ASSEMBLY</T>
        <rect x={-120} y={-220} width={240} height={220} fill="#5B6577" stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((q) => <rect key={q} x={-120} y={-220 + q * 70} width={240} height={8} fill="#78909C" />)}
        <path d="M 180 -400 L 180 -520 L 230 -520 L 230 -380" fill="#B0BEC5" stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((q) => { const u = ((t * 0.5 + q / 3) % 1); return <circle key={q} cx={205 + u * 40} cy={-540 - u * 120} r={16 + u * 26} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={0.8 * (1 - u)} />; })}
      </g>
      {/* road */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#8D99AE" />
      <rect x={z.x0} y={f} width={w} height={16} fill="#B8C2CF" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'rd' + k} x={z.x0 + k * 160 - ((t * 120) % 160)} y={f + 120} width={80} height={10} rx={5} fill="#FFFFFF" opacity={0.8} />)}
      {/* scooters carrying parts toward the assembler */}
      {Array.from({length: 6}, (_, k) => { const span = asm - x0s + 400, u = ((t * 0.11 * rush + k / 6) % 1), sx = x0s - 200 + u * span, bob = Math.abs(Math.sin(t * 12 + k)) * 4;
        return <g key={'sc' + k} transform={`translate(${sx} ${f + 70 + (k % 2) * 70 - bob})`}>
          <circle cx={-40} cy={20} r={16} fill="#263238" stroke={OL} strokeWidth={4} /><circle cx={40} cy={20} r={16} fill="#263238" stroke={OL} strokeWidth={4} />
          <path d="M -50 10 L 40 10 L 56 -30" stroke={awn[k % awn.length]} strokeWidth={14} strokeLinecap="round" fill="none" />
          <g transform="translate(-30 -26)">{cbox(60, 40, shops[k % shops.length].split(' ')[0].slice(0, 6))}</g>
          <circle cx={30} cy={-60} r={14} fill={['#F6CDA6', '#B97A4B', '#E0A878'][k % 3]} stroke={OL} strokeWidth={3} />
          <path d="M 16 -64 Q 30 -86 44 -64 Z" fill={awn[(k + 3) % awn.length]} stroke={OL} strokeWidth={3} />
          <path d="M 26 -46 L 22 -8" stroke={OL} strokeWidth={8} strokeLinecap="round" />
          {[0, 1].map((q) => <path key={q} d={`M ${-70 - q * 26} ${-6 + q * 14} L ${-110 - q * 40} ${-6 + q * 14}`} stroke={OL} strokeWidth={4} strokeLinecap="round" opacity={0.4} />)}
        </g>; })}
    </g>;
  },

  /** container PORT: gantry cranes, stacks, a ship that fills, straddle carriers */
  megaport: (t, z, f) => {
    const w = z.x1 - z.x0, quay = z.quayX ?? 1500, fill = clamp(kf(z.fill, t, 0.5));
    return <g>
      {sky(z, f, '#86CCF0', '#E6F6FF', 'mpsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 900 + t * 10) % (w + 600)) + z.x0 - 300, 140 + (k % 2) * 90, 1.1, k))}
      {/* sea behind the quay */}
      <rect x={quay} y={f - 150} width={z.x1 - quay} height={900} fill="#3E8EC4" />
      {Array.from({length: 14}, (_, k) => <path key={'wv' + k} d={`M ${quay + k * 160 + ((t * 30) % 160)} ${f - 110 + (k % 3) * 30} q 20 -12 40 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.6} />)}
      {/* the ship (hull + container bays filling) */}
      <g transform={`translate(${quay + 520} ${f - 90 + Math.sin(t * 1.2) * 4})`}>
        <path d="M -620 0 L 600 0 L 540 110 L -560 110 Z" fill="#2B4A5E" stroke={OL} strokeWidth={6} />
        <rect x={-620} y={0} width={1220} height={22} fill={RED} stroke={OL} strokeWidth={4} />
        <rect x={420} y={-220} width={140} height={220} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        {[0, 1, 2].map((q) => <rect key={q} x={440} y={-200 + q * 60} width={100} height={26} rx={4} fill="#9FD3F0" stroke={OL} strokeWidth={3} />)}
        {Array.from({length: 9}, (_, c) => Array.from({length: 4}, (_, r) => { const idx = c * 4 + r, on = idx / 36 < fill;
          return on ? <rect key={c + '-' + r} x={-580 + c * 108} y={-44 - r * 44} width={100} height={42} rx={3} fill={CTR[(c * 3 + r) % CTR.length]} stroke={OL} strokeWidth={3} /> : null; }))}
      </g>
      {/* ship-to-shore cranes with moving trolleys */}
      {[0, 1, 2].map((k) => { const cx = quay - 120 + k * 420, ph = (t * 0.35 + k * 0.33) % 1, tx = lerp(-180, 360, 0.5 + 0.5 * Math.sin(ph * Math.PI * 2)), dr = 120 + 140 * Math.abs(Math.cos(ph * Math.PI * 2));
        return <g key={'cr' + k} transform={`translate(${cx} ${f})`}>
          <path d="M -120 0 L -100 -560 M 120 0 L 100 -560 M -100 -560 L 100 -560 M -110 -300 L 110 -300 M -110 -300 L 110 0 M 110 -300 L -110 0" stroke={['#E5484D', '#1F7A8C', '#FF9F1C'][k]} strokeWidth={18} strokeLinecap="round" fill="none" />
          <path d="M -260 -560 L 520 -560" stroke={OL} strokeWidth={24} strokeLinecap="round" /><path d="M -260 -560 L 520 -560" stroke={['#E5484D', '#1F7A8C', '#FF9F1C'][k]} strokeWidth={14} strokeLinecap="round" />
          <rect x={-60} y={-640} width={120} height={70} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
          <g transform={`translate(${tx} -560)`}><rect x={-30} y={-14} width={60} height={28} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
            <path d={`M -14 14 L -14 ${dr} M 14 14 L 14 ${dr}`} stroke={OL} strokeWidth={3} />
            <rect x={-50} y={dr} width={100} height={44} rx={3} fill={CTR[(k * 2 + Math.floor(t * 0.35 + k * 0.33)) % CTR.length]} stroke={OL} strokeWidth={3.5} /></g>
        </g>; })}
      {/* container stacks in the yard */}
      {Array.from({length: Math.ceil((quay - z.x0 - 300) / 260)}, (_, c) => { const sx = z.x0 + 200 + c * 260, hgt = 2 + Math.floor(rnd(c) * 4);
        return <g key={'yd' + c}>{Array.from({length: hgt}, (_, r) => <g key={r}><rect x={sx} y={f - 60 - r * 58} width={220} height={56} rx={4} fill={CTR[(c + r * 3) % CTR.length]} stroke={OL} strokeWidth={3.5} />
          {[1, 2, 3, 4].map((q) => <path key={q} d={`M ${sx + q * 44} ${f - 56 - r * 58} L ${sx + q * 44} ${f - 8 - r * 58}`} stroke={OL} strokeWidth={1.5} opacity={0.4} />)}</g>)}</g>; })}
      {/* straddle carriers */}
      {[0, 1].map((k) => { const span = quay - z.x0, sx = z.x0 + ((t * (90 + k * 30) + k * 700) % span);
        return <g key={'st' + k} transform={`translate(${sx} ${f})`}><path d="M -70 0 L -60 -170 L 60 -170 L 70 0" fill="none" stroke={YEL} strokeWidth={16} /><rect x={-70} y={-200} width={140} height={36} rx={6} fill={YEL} stroke={OL} strokeWidth={4} />
          <rect x={-56} y={-150} width={112} height={50} rx={3} fill={CTR[(k + 4) % CTR.length]} stroke={OL} strokeWidth={3} />{[-60, 60].map((wx) => <circle key={wx} cx={wx} cy={-6} r={14} fill="#263238" stroke={OL} strokeWidth={3} />)}</g>; })}
      {z.board && <g transform={`translate(${z.boardX ?? 700} ${f - 560})`}><rect x={-300} y={-60} width={600} height={100} rx={14} fill="#16232E" stroke={OL} strokeWidth={6} /><T x={0} y={8} s={fit(z.board, 560, 44)} c={YEL}>{z.board}</T></g>}
      <rect x={z.x0} y={f} width={quay - z.x0 + 200} height={700} fill="#9AA3B5" />
      <rect x={z.x0} y={f} width={quay - z.x0 + 200} height={18} fill="#C9D1DC" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** RARE-EARTH refinery: ore heap at the door, a cascade of separation tanks, element jars, magnets out */
  refinery: (t, z, f) => {
    const w = z.x1 - z.x0, n = z.stages ?? 8, tx0 = z.tankX ?? 300, flowOn = z.flowAt === undefined || t > z.flowAt;
    const EL: string[] = z.elements || ['Nd', 'Pr', 'Dy', 'Tb'];
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E6EEF0" />
      {/* outdoor door on the left: the mine side */}
      <g transform={`translate(${z.mineX ?? -520} ${f})`}>
        <rect x={-260} y={-520} width={520} height={520} fill="#9ED6F5" stroke={OL} strokeWidth={6} />
        <path d="M -260 -60 Q -120 -250 0 -140 Q 120 -260 260 -80 L 260 0 L -260 0 Z" fill="#B08968" stroke={OL} strokeWidth={4} />
        {Array.from({length: 9}, (_, k) => <circle key={k} cx={-180 + k * 44} cy={-30 - rnd(k) * 40} r={14 + rnd(k + 3) * 8} fill={['#8D6E63', '#A1887F', '#795548'][k % 3]} stroke={OL} strokeWidth={3} />)}
        <rect x={-200} y={-560} width={400} height={56} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-522} s={30}>{z.mineLabel || 'ORE IN (MINED)'}</T>
      </g>
      {/* pipes along the top */}
      <path d={`M ${z.x0} ${f - 560} L ${z.x1} ${f - 560}`} stroke={OL} strokeWidth={30} /><path d={`M ${z.x0} ${f - 560} L ${z.x1} ${f - 560}`} stroke={TEAL} strokeWidth={20} />
      {flowOn && Array.from({length: Math.ceil(w / 120)}, (_, k) => <circle key={'fl' + k} cx={z.x0 + ((k * 120 + t * 220) % w)} cy={f - 560} r={6} fill="#CFF6FF" />)}
      {/* the cascade of mixer-settler tanks */}
      {Array.from({length: n}, (_, k) => { const x = tx0 + k * 190, lvl = 0.55 + 0.12 * Math.sin(t * 2 + k), hue = ['#7FDBFF', '#9BE7C4', '#C3B5FF', '#FFD59E', '#FFB3C1', '#B5F0FF', '#D7F59B', '#FFC6E8'][k % 8];
        return <g key={'tk' + k} transform={`translate(${x} ${f})`}>
          <path d={`M 0 -560 L 0 -300`} stroke={OL} strokeWidth={10} />
          <rect x={-70} y={-300} width={140} height={300} rx={14} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
          <rect x={-60} y={-290 + 280 * (1 - lvl)} width={120} height={280 * lvl} rx={8} fill={hue} opacity={0.9} />
          {flowOn && [0, 1, 2].map((q) => { const u = ((t * 0.8 + q / 3 + k * 0.13) % 1); return <circle key={q} cx={-30 + q * 30} cy={-20 - u * 240 * lvl} r={5 + 3 * u} fill="#FFFFFF" opacity={0.8 * (1 - u)} />; })}
          {/* mixer paddle */}
          <g transform={`translate(0 -150) rotate(${flowOn ? t * 240 + k * 30 : 0})`}><path d="M -40 0 L 40 0 M 0 -40 L 0 40" stroke={OL} strokeWidth={6} opacity={0.6} /></g>
          <rect x={-46} y={-330} width={92} height={34} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><T x={0} y={-305} s={18}>{`STAGE ${k + 1}`}</T>
          {k < n - 1 && <path d={`M 70 -120 L 120 -120`} stroke={OL} strokeWidth={14} />}
        </g>; })}
      {/* element jars and magnets */}
      <g transform={`translate(${tx0 + n * 190 + 120} ${f})`}>
        <rect x={-40} y={-130} width={340} height={130} rx={10} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
        {EL.map((el, k) => { const on = z.jarsAt === undefined || t > z.jarsAt + k * 0.25; return on ? <g key={el} transform={`translate(${10 + k * 82} -130) scale(${pop(t, (z.jarsAt ?? -1) + k * 0.25, 0.4)})`}>
          <rect x={-30} y={-96} width={60} height={96} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><rect x={-26} y={-60} width={52} height={56} rx={6} fill={['#C5B3E6', '#9BE7C4', '#FFD59E', '#FFB3C1'][k % 4]} />
          <rect x={-34} y={-110} width={68} height={18} rx={5} fill={STEEL} stroke={OL} strokeWidth={3} /><T x={0} y={-68} s={26}>{el}</T></g> : null; })}
        {/* magnets rolling out on a little belt */}
        <rect x={-40} y={-10} width={600} height={20} fill="#455A64" stroke={OL} strokeWidth={4} />
        {Array.from({length: 5}, (_, q) => { const mx = -20 + ((q * 120 + t * 90) % 600);
          return <g key={'mg' + q} transform={`translate(${mx} -34)`}><path d="M -26 24 L -26 -6 Q -26 -30 0 -30 Q 26 -30 26 -6 L 26 24 L 12 24 L 12 -4 Q 12 -14 0 -14 Q -12 -14 -12 -4 L -12 24 Z" fill={RED} stroke={OL} strokeWidth={3.5} />
            <rect x={-26} y={14} width={14} height={10} fill="#ECEFF1" stroke={OL} strokeWidth={2} /><rect x={12} y={14} width={14} height={10} fill="#ECEFF1" stroke={OL} strokeWidth={2} /></g>; })}
      </g>
      {z.board && <g transform={`translate(${z.boardX ?? 1000} ${f - 680})`}><rect x={-320} y={-54} width={640} height={92} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={8} s={fit(z.board, 600, 40)}>{z.board}</T></g>}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B8C4C8" />
      <rect x={z.x0} y={f} width={w} height={16} fill="#D3DCDF" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** SOLAR PANEL line: five stages, parts morph along the belt */
  solarline: (t, z, f) => {
    const w = z.x1 - z.x0, st: string[] = z.stagesTxt || ['POLYSILICON', 'INGOT', 'WAFER', 'CELL', 'MODULE'], x0 = z.lineX ?? 0, gap = z.gap ?? 480, sp = z.speed ?? 110, hi0 = z.hiAt ? pick(z.hiAt, t, z.hi) : z.hi, hi = hi0 === null ? undefined : hi0;
    const glyph = (k: number) => {
      switch (k) {
        case 0: return <g>{[0, 1, 2, 3].map((q) => <path key={q} d={`M ${-26 + q * 16} 10 L ${-20 + q * 16} -14 L ${-8 + q * 16} -18 L ${-2 + q * 16} 8 Z`} fill="#B0BEC5" stroke={OL} strokeWidth={2.5} />)}</g>;
        case 1: return <g><rect x={-18} y={-50} width={36} height={60} rx={14} fill="#78909C" stroke={OL} strokeWidth={3.5} /><path d="M -10 -40 L -10 0" stroke="#CFD8DC" strokeWidth={4} /></g>;
        case 2: return <g>{[0, 1, 2].map((q) => <rect key={q} x={-26 + q * 6} y={-26 - q * 6} width={42} height={42} rx={6} fill="#455A64" stroke={OL} strokeWidth={2.5} />)}</g>;
        case 3: return <g><rect x={-24} y={-24} width={48} height={48} rx={4} fill="#1E4E8C" stroke={OL} strokeWidth={3} /><path d="M -24 -8 L 24 -8 M -24 8 L 24 8 M 0 -24 L 0 24" stroke="#C9E3FF" strokeWidth={2} /></g>;
        default: return <g>{product(4, t, 0)}</g>;
      }
    };
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#EAF4F8" />
      {/* big windows with the sun outside */}
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => <g key={'wn' + k}><rect x={z.x0 + k * 520 + 60} y={f - 820} width={400} height={240} rx={12} fill="#BFE8FF" stroke={OL} strokeWidth={5} />
        <path d={`M ${z.x0 + k * 520 + 260} ${f - 820} L ${z.x0 + k * 520 + 260} ${f - 580} M ${z.x0 + k * 520 + 60} ${f - 700} L ${z.x0 + k * 520 + 460} ${f - 700}`} stroke={OL} strokeWidth={4} />
        <path d={`M ${z.x0 + k * 520 + 120} ${f - 580} L ${z.x0 + k * 520 + 400} ${f - 580} L ${z.x0 + k * 520 + 520} ${f} L ${z.x0 + k * 520 + 40} ${f} Z`} fill="#FFF6C8" opacity={0.22} /></g>)}
      {/* stage machines */}
      {st.map((s, k) => { const mx = x0 + k * gap, on = hi === undefined || hi === k || hi === 'all';
        return <g key={'ms' + k} transform={`translate(${mx} ${f - 200})`} opacity={on ? 1 : 0.6}>
          <rect x={-150} y={-260} width={300} height={200} rx={20} fill={['#FFFFFF', '#E3F2FD', '#E8F5E9', '#FFF3E0', '#F3E5F5'][k % 5]} stroke={OL} strokeWidth={5} />
          <rect x={-120} y={-230} width={240} height={90} rx={10} fill="#16232E" />
          {Array.from({length: 4}, (_, q) => <rect key={q} x={-104 + q * 56} y={-216} width={40} height={60 * (0.3 + 0.7 * Math.abs(Math.sin(t * 2 + q + k)))} rx={4} fill={[TEAL, ORANGE, GREEN, YEL][q]} opacity={0.85} />)}
          <rect x={-160} y={-320} width={320} height={52} rx={12} fill={on && hi !== undefined ? YEL : '#FFFFFF'} stroke={OL} strokeWidth={4} /><T x={0} y={-284} s={fit(s, 290, 30)}>{s}</T>
          <rect x={-60} y={-60} width={120} height={60} fill="#5B6577" stroke={OL} strokeWidth={4} />
          {k === 1 && <g transform={`translate(0 ${-140 + 20 * Math.sin(t * 1.5)})`}><path d="M 0 -120 L 0 -40" stroke={OL} strokeWidth={4} /><rect x={-14} y={-40} width={28} height={50} rx={10} fill="#78909C" stroke={OL} strokeWidth={3} /></g>}
          {k === 2 && <g transform={`rotate(${t * 400})`}><circle cx={0} cy={-100} r={0} /></g>}
        </g>; })}
      {/* belt with morphing parts */}
      <rect x={z.x0} y={f - 140} width={w} height={28} fill="#455A64" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 50)}, (_, q) => <circle key={q} cx={z.x0 + q * 50 + ((t * sp) % 50)} cy={f - 126} r={5} fill="#90A4AE" />)}
      {Array.from({length: Math.ceil((st.length * gap + 400) / 200)}, (_, q) => { const px = x0 - 300 + ((q * 200 + t * sp) % (st.length * gap + 400)), stage = clamp(Math.floor((px - x0 + gap / 2) / gap), 0, st.length - 1);
        return <g key={'pt' + q} transform={`translate(${px} ${f - 172})`}>{glyph(stage)}</g>; })}
      {/* finished panels stacking at the end */}
      <g transform={`translate(${x0 + st.length * gap + 120} ${f})`}>{Array.from({length: 1 + Math.floor((t * 0.6) % 8)}, (_, q) => <g key={q} transform={`translate(0 ${-30 - q * 26}) scale(1.6 0.5)`}>{product(4, t, q)}</g>)}</g>
      <rect x={z.x0} y={f} width={w} height={700} fill="#CFD8DC" />
      <rect x={z.x0} y={f} width={w} height={16} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the TARIFF WALL: dated rows stack up between the factory dock and the store; some rows topple */
  tariffwall: (t, z, f) => {
    const w = z.x1 - z.x0, wx = z.wallX ?? 1100, rows: any[] = z.rows || [];
    let yTop = f;
    const rowNodes: React.ReactNode[] = [];
    rows.forEach((r, k) => {
      const at = Number(r.at ?? 0), h = Number(r.h ?? 60), out = r.out !== undefined ? Number(r.out) : undefined;
      if (t < at) return;
      const fall = out !== undefined ? win(t, out, 0.9) : 0;
      if (fall >= 1) return;
      const drop = E.outBack(win(t, at, 0.5)), y = yTop - h;
      const gone = fall > 0;
      rowNodes.push(<g key={'rw' + k} transform={`translate(${wx + (gone ? fall * 380 : 0)} ${y - (1 - drop) * 400 + (gone ? fall * fall * 600 : 0)}) rotate(${gone ? fall * 50 : jig(t, at + 0.5, 20, 7) * 2})`} opacity={gone ? 1 - fall : 1}>
        <rect x={-260} y={0} width={520} height={h} rx={6} fill={r.color || '#C76B4A'} stroke={OL} strokeWidth={4} />
        {Array.from({length: 6}, (_, q) => <path key={q} d={`M ${-260 + q * 87 + (k % 2) * 43} 0 L ${-260 + q * 87 + (k % 2) * 43} ${h}`} stroke={OL} strokeWidth={2} opacity={0.35} />)}
        <T x={0} y={h / 2 + 11} s={fit(String(r.label || ''), 500, Math.min(34, h * 0.62))} c="#FFFFFF" st={OL} sw={5}>{r.label}</T>
      </g>);
      if (!gone) yTop = y;
    });
    return <g>
      {sky(z, f, '#9AD6F5', '#EEF9FF', 'twsky' + Math.round(z.x0))}
      {[0, 1, 2].map((k) => cloud(((k * 820 + t * 12) % (w + 600)) + z.x0 - 300, 130 + (k % 2) * 90, 1, k))}
      {/* left: factory dock with crates */}
      <g transform={`translate(${wx - 760} ${f})`}><rect x={-260} y={-380} width={520} height={380} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <path d="M -260 -380 L -170 -460 L -80 -380 L 10 -460 L 100 -380 L 190 -460 L 260 -380" fill="#B0BEC5" stroke={OL} strokeWidth={5} />
        <rect x={-200} y={-330} width={400} height={56} rx={10} fill={TEAL} stroke={OL} strokeWidth={4} /><T x={0} y={-292} s={30} c="#FFFFFF">{z.leftLabel || 'FACTORY'}</T>
        <rect x={-140} y={-220} width={280} height={220} fill="#5B6577" stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((q) => <g key={q} transform={`translate(${200 + q * 60} ${-36 - (q % 2) * 50})`}>{cbox(70, 50)}</g>)}</g>
      {/* right: a store */}
      <g transform={`translate(${wx + 760} ${f})`}><rect x={-260} y={-340} width={520} height={340} fill="#FFF3E0" stroke={OL} strokeWidth={6} />
        <path d="M -280 -340 L 280 -340 L 300 -280 L -300 -280 Z" fill={RED} stroke={OL} strokeWidth={5} />
        {Array.from({length: 7}, (_, q) => <path key={q} d={`M ${-300 + q * 86} -280 q 43 26 86 0`} fill={q % 2 ? '#FFFFFF' : RED} stroke={OL} strokeWidth={3} />)}
        <rect x={-200} y={-410} width={400} height={56} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-372} s={30}>{z.rightLabel || 'U.S. STORE'}</T>
        <rect x={-180} y={-220} width={150} height={220} fill="#9FD3F0" stroke={OL} strokeWidth={4} /><rect x={30} y={-220} width={150} height={150} fill="#9FD3F0" stroke={OL} strokeWidth={4} /></g>
      {/* ground */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#A9D18E" />
      <rect x={z.x0} y={f} width={w} height={18} fill="#8BBF6E" stroke={OL} strokeWidth={4} />
      {/* conveyor of parcels from factory to store through the wall's gate */}
      <rect x={wx - 520} y={f - 34} width={1040} height={20} fill="#455A64" stroke={OL} strokeWidth={3} />
      {Array.from({length: 6}, (_, k) => { const u = ((t * 0.16 + k / 6) % 1), px = wx - 520 + u * 1040, near = Math.abs(px - wx) < 280, hop = near ? Math.sin(((px - wx + 280) / 560) * Math.PI) * Math.min(300, (f - yTop) + 40) : 0;
        return <g key={'pc' + k} transform={`translate(${px} ${f - 60 - hop})`}>{cbox(64, 46, 'GOODS')}</g>; })}
      {rowNodes}
      {/* the toll gate kiosk at the wall foot */}
      <g transform={`translate(${wx - 330} ${f})`}><rect x={-46} y={-130} width={92} height={130} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><rect x={-36} y={-112} width={72} height={40} rx={4} fill="#9FD3F0" stroke={OL} strokeWidth={3} /><T x={0} y={-30} s={18}>TARIFF</T></g>
    </g>;
  },

  /** MOVING DAY: OLD PLANT (left) with its supplier huddle, a strait, NEW PLANT under construction (right) */
  movingday: (t, z, f) => {
    const w = z.x1 - z.x0, ox = z.oldX ?? 300, nx = z.newX ?? 2200, sea0 = z.sea0 ?? 950, sea1 = z.sea1 ?? 1550, bld = clamp(kf(z.build, t, 0.3));
    const supAt: number | undefined = z.suppliersAt;
    return <g>
      {sky(z, f, '#93D2F2', '#ECF8FF', 'mdsky' + Math.round(z.x0))}
      {[0, 1, 2, 3].map((k) => cloud(((k * 700 + t * 16) % (w + 600)) + z.x0 - 300, 140 + (k % 2) * 80, 0.9, k))}
      <rect x={z.x0} y={f} width={w} height={700} fill="#A9D18E" />
      <rect x={sea0} y={f - 6} width={sea1 - sea0} height={706} fill="#3E8EC4" />
      {Array.from({length: 6}, (_, k) => <path key={'wv' + k} d={`M ${sea0 + 30 + k * 95 + ((t * 25) % 95)} ${f + 40 + (k % 2) * 40} q 18 -10 36 0`} stroke="#FFFFFF" strokeWidth={4} fill="none" opacity={0.7} />)}
      <rect x={z.x0} y={f} width={sea0 - z.x0} height={18} fill="#8BBF6E" stroke={OL} strokeWidth={4} />
      <rect x={sea1} y={f} width={z.x1 - sea1} height={18} fill="#8BBF6E" stroke={OL} strokeWidth={4} />
      {/* little ship shuttling across */}
      {(() => { const u = 0.5 + 0.5 * Math.sin(t * 0.7), sx = lerp(sea0 + 90, sea1 - 90, u);
        return <g transform={`translate(${sx} ${f + 10 + Math.sin(t * 2) * 4}) scale(${u > 0.5 ? 1 : -1} 1)`}><path d="M -80 0 L 80 0 L 60 34 L -60 34 Z" fill={RED} stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((q) => <rect key={q} x={-60 + q * 40} y={-30} width={36} height={30} fill={CTR[q + 1]} stroke={OL} strokeWidth={3} />)}<rect x={50} y={-44} width={22} height={44} fill="#FFFFFF" stroke={OL} strokeWidth={3} /></g>; })()}
      {/* OLD PLANT + supplier huddle */}
      <g transform={`translate(${ox} ${f})`}>
        <rect x={-240} y={-360} width={480} height={360} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <path d="M -240 -360 L -160 -440 L -80 -360 L 0 -440 L 80 -360 L 160 -440 L 240 -360" fill="#B0BEC5" stroke={OL} strokeWidth={5} />
        <rect x={-190} y={-320} width={380} height={56} rx={10} fill={TEAL} stroke={OL} strokeWidth={4} /><T x={0} y={-282} s={30} c="#FFFFFF">{z.oldName || 'OLD PLANT'}</T>
        <rect x={-120} y={-210} width={240} height={210} fill="#5B6577" stroke={OL} strokeWidth={4} />
        {(z.oldShops || ['SCREWS', 'MOLDS', 'CABLES', 'MOTORS', 'GLASS', 'CHIPS']).map((s: string, k: number) => { const hx = (k % 2 ? 1 : -1) * (320 + Math.floor(k / 2) * 150), bob = Math.sin(t * 3 + k) * 3;
          return <g key={'oh' + k} transform={`translate(${hx} ${bob})`}><rect x={-62} y={-130} width={124} height={130} fill={['#FFF3E0', '#E3F2FD', '#E8F5E9'][k % 3]} stroke={OL} strokeWidth={4} />
            <path d="M -72 -130 L 0 -184 L 72 -130 Z" fill={CTR[k % CTR.length]} stroke={OL} strokeWidth={4} /><rect x={-58} y={-110} width={116} height={30} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-88} s={fit(s, 110, 18)}>{s}</T></g>; })}
      </g>
      {/* NEW PLANT under construction */}
      <g transform={`translate(${nx} ${f})`}>
        <rect x={-240} y={-360 * bld} width={480} height={360 * bld} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {bld < 0.98 && Array.from({length: 5}, (_, q) => <path key={q} d={`M ${-260 + q * 130} 0 L ${-260 + q * 130} -400 M ${-260 + q * 130} -400 L ${-130 + q * 130} -300`} stroke="#C49A6C" strokeWidth={8} />)}
        {bld < 0.98 && <path d="M -280 -400 L 300 -400 M -280 -260 L 300 -260 M -280 -120 L 300 -120" stroke="#C49A6C" strokeWidth={8} />}
        {/* tower crane */}
        <g transform="translate(300 0)"><path d="M 0 0 L 0 -620 M -220 -600 L 160 -600" stroke={YEL} strokeWidth={16} /><path d="M 0 0 L 0 -620 M -220 -600 L 160 -600" stroke={OL} strokeWidth={3} strokeDasharray="10 14" />
          <g transform={`translate(${-120 + 60 * Math.sin(t * 0.8)} -600)`}><path d={`M 0 0 L 0 ${160 + 60 * Math.sin(t * 1.2)}`} stroke={OL} strokeWidth={3} /><rect x={-40} y={160 + 60 * Math.sin(t * 1.2)} width={80} height={24} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g></g>
        <rect x={-190} y={-440} width={380} height={56} rx={10} fill={ORANGE} stroke={OL} strokeWidth={4} /><T x={0} y={-402} s={fit(z.newName || 'NEW PLANT', 360, 30)} c="#FFFFFF">{z.newName || 'NEW PLANT'}</T>
        {/* suppliers: an empty lot with a sign, then a first hut pops */}
        <g transform="translate(-420 0)">{supAt !== undefined && t > supAt ? <g transform={`scale(${pop(t, supAt, 0.5)})`}><rect x={-62} y={-130} width={124} height={130} fill="#E8F5E9" stroke={OL} strokeWidth={4} />
          <path d="M -72 -130 L 0 -184 L 72 -130 Z" fill={GREEN} stroke={OL} strokeWidth={4} /><rect x={-58} y={-110} width={116} height={30} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-88} s={16}>{z.supplierName || 'SUPPLIER #1'}</T></g>
          : <g><path d="M 0 0 L 0 -150" stroke={OL} strokeWidth={6} /><rect x={-110} y={-200} width={220} height={70} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-172} s={20}>SUPPLIERS:</T><T x={0} y={-146} s={20} c={RED}>COMING SOON</T></g>}</g>
      </g>
    </g>;
  },

  /** MEL'S KITCHEN (day): window, cabinets, a counter of appliances; `tags` [[t, idx]] pop a little origin tag on appliance idx */
  kitchen: (t, z, f) => {
    const w = z.x1 - z.x0, cx = z.counterX ?? 300, tagTxt: string = z.tagText || 'MADE IN CHINA', top = f - 250;
    const tags: [number, number][] = (z.tags || []).map((p: any) => [Number(p[0]), Number(p[1])]);
    const tagAt = (k: number) => { const m = tags.find((p) => p[1] === k); return m ? m[0] : undefined; };
    const app = (k: number, x: number, node: React.ReactNode) => { const ta = tagAt(k);
      return <g key={'ap' + k} transform={`translate(${x} ${top})`}>{node}
        {ta !== undefined && t >= ta && <g transform={`translate(0 -${k === 1 ? 300 : 190}) scale(${pop(t, ta, 0.4)}) rotate(${-6 + 3 * Math.sin(t * 3 + k)})`}>
          <path d="M 0 40 L 0 70" stroke={OL} strokeWidth={3} /><rect x={-92} y={-4} width={184} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><T x={0} y={26} s={20} c={RED}>{tagTxt}</T></g>}</g>; };
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#FFF2D6" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 90} y={-2500} width={45} height={2500 + f} fill="#FBE6BE" opacity={0.6} />)}
      {/* window */}
      <g transform={`translate(${z.windowX ?? 1250} ${f - 640})`}><rect x={-230} y={-150} width={460} height={300} rx={10} fill="#9ED9F7" stroke={OL} strokeWidth={6} />
        <circle cx={120} cy={-70} r={40} fill="#FFE27A" stroke={OL} strokeWidth={4} />
        <path d="M -230 90 Q -120 20 0 80 Q 120 30 230 90 L 230 150 L -230 150 Z" fill="#A9D18E" stroke={OL} strokeWidth={4} />
        <g transform={`translate(-120 60) rotate(${Math.sin(t * 1.3) * 3})`}><path d="M 0 0 L 0 -60" stroke="#8A5428" strokeWidth={10} /><circle cx={0} cy={-90} r={46} fill="#6CBF66" stroke={OL} strokeWidth={4} /></g>
        <path d="M 0 -150 L 0 150 M -230 0 L 230 0" stroke={OL} strokeWidth={6} />
        <path d={`M -250 -170 Q -150 ${-120 + 6 * Math.sin(t)} -60 -170 Z M 250 -170 Q 150 ${-120 + 6 * Math.sin(t + 1)} 60 -170 Z`} fill="#E5484D" stroke={OL} strokeWidth={4} /></g>
      {/* upper cabinets */}
      {Array.from({length: 4}, (_, k) => <g key={'uc' + k}><rect x={cx - 380 + k * 190} y={f - 820} width={180} height={220} rx={10} fill="#7FC8C0" stroke={OL} strokeWidth={5} /><circle cx={cx - 380 + k * 190 + 150} cy={f - 700} r={8} fill={OL} /></g>)}
      {/* counter */}
      <rect x={cx - 420} y={top} width={1500} height={250} fill="#5FA8A0" stroke={OL} strokeWidth={6} />
      <rect x={cx - 440} y={top - 22} width={1540} height={30} rx={8} fill="#F4F1E6" stroke={OL} strokeWidth={5} />
      {Array.from({length: 6}, (_, k) => <g key={'dr' + k}><rect x={cx - 400 + k * 245} y={top + 30} width={225} height={190} rx={10} fill="#73BDB4" stroke={OL} strokeWidth={4} /><rect x={cx - 320 + k * 245} y={top + 60} width={70} height={12} rx={6} fill={OL} /></g>)}
      {/* appliances: 0 kettle, 1 lamp, 2 mixer, 3 phone + charger */}
      {app(0, cx - 280, <g><path d="M -60 -10 L -50 -130 Q 0 -160 50 -130 L 60 -10 Z" fill="#E5484D" stroke={OL} strokeWidth={5} /><path d="M 50 -110 Q 100 -100 70 -40" stroke={OL} strokeWidth={8} fill="none" /><path d="M -50 -100 L -90 -130" stroke={OL} strokeWidth={10} strokeLinecap="round" />
        {[0, 1].map((q) => { const u = (t * 0.7 + q / 2) % 1; return <circle key={q} cx={-96 - u * 20} cy={-140 - u * 70} r={10 + u * 14} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={1 - u} />; })}</g>)}
      {app(1, cx - 40, <g><path d="M -10 -10 L -10 -200 M 10 -10 L 10 -200" stroke={OL} strokeWidth={6} /><rect x={-40} y={-16} width={80} height={16} rx={6} fill="#5C6BC0" stroke={OL} strokeWidth={4} /><path d="M -70 -200 L 70 -200 L 40 -280 L -40 -280 Z" fill="#FFD23F" stroke={OL} strokeWidth={5} />
        <path d="M -70 -200 L -120 -20 L 120 -20 L 70 -200 Z" fill="#FFF6B0" opacity={0.25 + 0.05 * Math.sin(t * 4)} /></g>)}
      {app(2, cx + 220, <g><rect x={-60} y={-40} width={120} height={40} rx={8} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><path d="M -40 -40 L -40 -150 L 50 -150 L 60 -110 L 0 -110" fill="#26A69A" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <g transform={`translate(0 -80) rotate(${t * 600})`}><path d="M -16 0 L 16 0 M 0 -16 L 0 16" stroke={OL} strokeWidth={4} /></g><path d="M -50 -60 Q 0 -10 50 -60" fill="#CFD8DC" stroke={OL} strokeWidth={4} /></g>)}
      {app(3, cx + 470, <g><rect x={-26} y={-90} width={52} height={86} rx={8} fill="#263238" stroke={OL} strokeWidth={4} /><rect x={-20} y={-82} width={40} height={64} rx={4} fill="#80DEEA" opacity={0.8} /><path d="M 0 -4 Q 30 20 80 -6" stroke="#FFFFFF" strokeWidth={6} fill="none" /><path d="M 0 -4 Q 30 20 80 -6" stroke={OL} strokeWidth={2} fill="none" /><rect x={74} y={-30} width={40} height={36} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>)}
      {/* fridge */}
      <g transform={`translate(${cx + 1250} ${f})`}><rect x={-140} y={-560} width={280} height={560} rx={20} fill="#ECEFF1" stroke={OL} strokeWidth={6} /><path d="M -140 -360 L 140 -360" stroke={OL} strokeWidth={5} /><rect x={100} y={-520} width={14} height={120} rx={7} fill={OL} /><rect x={100} y={-320} width={14} height={160} rx={7} fill={OL} />
        <rect x={-90} y={-520} width={80} height={60} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3} transform="rotate(-6)" /><circle cx={-50} cy={-470} r={14} fill="#FFD23F" stroke={OL} strokeWidth={3} /></g>
      {/* floor */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#E9D8B6" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'ft' + k} x={z.x0 + k * 120} y={f + (k % 2) * 60} width={60} height={60} fill="#D9C39A" opacity={0.7} />)}
      <rect x={z.x0} y={f} width={w} height={14} fill="#CDB487" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** SHOW TITLE CARD (screen-filling, static camera) */
  fctitle: (t, z, f) => {
    const cx = 960, cy = 470, lines: string[] = z.lines || ['STILL MADE', 'IN CHINA'], sub: string = z.sub || 'WHY THE WORLD STILL DEPENDS ON CHINESE FACTORIES';
    const subs: [number, string][] = (z.subs || []).map((p: any) => [Number(p[0]), String(p[1])]);
    const cur = subs.filter((p) => t >= p[0]).pop();
    const typed = cur ? cur[1].slice(0, Math.floor((t - cur[0]) * 32)) : '';
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#0F5E6E" />
      <g transform={`translate(${cx} ${cy}) rotate(${-t * 10})`}>{Array.from({length: 20}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos((k / 20) * Math.PI * 2) * 2400} ${Math.sin((k / 20) * Math.PI * 2) * 2400} L ${Math.cos(((k + 0.5) / 20) * Math.PI * 2) * 2400} ${Math.sin(((k + 0.5) / 20) * Math.PI * 2) * 2400} Z`} fill={k % 2 ? '#1F7A8C' : ORANGE} opacity={k % 2 ? 1 : 0.9} />)}</g>
      {/* the gear */}
      <g transform={`translate(${cx} ${cy}) rotate(${t * 30}) scale(${E.outBack(win(t, 0, 0.8))})`}>
        {Array.from({length: 16}, (_, k) => <rect key={k} x={-46} y={-470} width={92} height={90} rx={12} fill="#FFD23F" stroke={OL} strokeWidth={10} transform={`rotate(${k * 22.5})`} />)}
        <circle r={410} fill="#FFD23F" stroke={OL} strokeWidth={12} /><circle r={360} fill="#E5484D" stroke={OL} strokeWidth={10} />
        <circle r={330} fill="none" stroke="#FFFFFF" strokeWidth={8} strokeDasharray="4 22" /></g>
      <g transform={`translate(${cx} ${cy - 250}) scale(${pop(t, 0.3, 0.5)})`}><rect x={-360} y={-36} width={720} height={60} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={8} s={26} ls={3}>{z.kicker || 'THE HIDDEN ECONOMICS PRESENTS'}</T></g>
      {/* letters ride in on little crates and drop */}
      {lines.map((word, wi) => { const adv = (c: string) => (c === 'I' ? 0.48 : c === ' ' ? 0.5 : c === 'L' || c === 'T' || c === '.' ? 0.78 : c === 'M' || c === 'W' ? 1.18 : 1);
        const tot = word.split('').reduce((q, c) => q + adv(c), 0), cw = Math.min(104, 1500 / Math.max(1, tot));
        const xs: number[] = []; let acc = 0; word.split('').forEach((c) => { xs.push((acc + adv(c) / 2 - tot / 2) * cw); acc += adv(c); });
        return <g key={wi} transform={`translate(${cx} ${cy - 60 + wi * 160})`}>{word.split('').map((ch, k) => {
        const st = 0.45 + wi * 0.4 + k * 0.05, u = E.outBack(win(t, st, 0.45)), x = xs[k];
        const sq = 1 + 0.25 * jig(t, st + 0.3, 20, 8), wob = Math.sin(t * 4 + k * 0.7 + wi) * 5;
        if (ch === ' ') return null;
        return <g key={k} transform={`translate(${x + (1 - u) * 900} ${wob}) scale(${(2 - sq)} ${sq}) rotate(${Math.sin(t * 3 + k) * 3})`}>
          <T x={8} y={12} s={150} c={OL}>{ch}</T><T x={0} y={0} s={150} c={wi ? '#FFFFFF' : '#FFD23F'} st={OL} sw={14}>{ch}</T></g>; })}</g>; })}
      <g transform={`translate(${cx} ${cy + 300}) scale(${pop(t, 1.6, 0.45)}) rotate(${-2 + Math.sin(t * 2) * 1.5})`}>
        <path d="M -560 -42 L 560 -42 L 530 0 L 560 42 L -560 42 L -530 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={7} strokeLinejoin="round" /><T x={0} y={14} s={fit(sub, 1040, 38)} c="#0F5E6E">{sub}</T></g>
      {/* conveyor along the bottom with crates */}
      <rect x={-200} y={900} width={2400} height={30} fill="#455A64" stroke={OL} strokeWidth={5} />
      {Array.from({length: 9}, (_, k) => <g key={'cb' + k} transform={`translate(${((k * 260 + t * 160) % 2340) - 200} 868)`}>{cbox(90, 60, ['BOLT', 'COIL', 'KNOB', 'PLUG', 'LEVER', 'TRAY', 'SPRING', 'SCREW', 'CASE'][k])}</g>)}
      {cur && <g transform="translate(960 1010)"><rect x={-760} y={-40} width={1520} height={70} rx={14} fill="#0B1A3A" opacity={0.88} />
        <T x={0} y={8} s={34} c="#FFE066" w={800}>{typed}{Math.floor(t * 3) % 2 ? '▌' : ' '}</T></g>}
    </g>;
  },

  /** ACT BUMPER (screen-filling, static camera) */
  fcbumper: (t, z, f) => {
    const act: string = z.act || 'ACT ONE', title: string = z.title || '', cap: string = z.caption || '', col2 = z.color || TEAL;
    const wipe = E.out(win(t, 0, 0.45)), spin = E.outBack(win(t, 0.2, 0.7));
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#F3F7F4" />
      <g transform={`translate(${2600 - 2600 * wipe} 0)`}>{Array.from({length: 26}, (_, k) => <path key={k} d={`M ${k * 140 - 400} -200 L ${k * 140 - 330} -200 L ${k * 140 + 290} 1300 L ${k * 140 + 220} 1300 Z`} fill={k % 2 ? col2 : YEL} opacity={0.92} />)}</g>
      <rect x={-200} y={960} width={2400} height={34} fill="#455A64" stroke={OL} strokeWidth={5} />
      {Array.from({length: 22}, (_, k) => <circle key={'rl' + k} cx={((k * 100 + t * 200) % 2200) - 100} cy={977} r={9} fill="#90A4AE" />)}
      <g transform={`translate(560 520) rotate(${(1 - spin) * 360}) scale(${spin})`}>
        <rect x={-180} y={-170} width={360} height={340} rx={18} fill={BOX} stroke={OL} strokeWidth={10} />
        <path d="M -180 -80 L 180 -80 M 0 -170 L 0 -80" stroke="#A9783F" strokeWidth={10} />
        <rect x={-120} y={-40} width={240} height={170} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <T x={0} y={4} s={40} c={col2} ls={3}>ACT</T><T x={0} y={116} s={120} c={OL}>{z.num || '1'}</T>
        <path d="M -150 -150 L -110 -110 M 150 -150 L 110 -110" stroke={OL} strokeWidth={5} opacity={0.5} /></g>
      <g transform={`translate(1240 470) scale(${pop(t, 0.45, 0.45)}) rotate(-3)`}><rect x={-520} y={-100} width={1040} height={150} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={9} />
        <T x={0} y={22} s={fit(title, 960, 72)} c={OL}>{title}</T><T x={0} y={-62} s={26} c={col2} ls={6}>{act}</T></g>
      {cap && <g transform={`translate(1240 650) scale(${pop(t, 0.9, 0.4)}) rotate(${Math.sin(t * 2.4) * 1.5})`}><rect x={-480} y={-38} width={960} height={64} rx={32} fill="#16232E" />
        <T x={0} y={8} s={fit(cap, 900, 30)} c="#FFE066" w={800}>{cap}</T></g>}
    </g>;
  },
};

/* ============================================================================================ ITEMS */
/** GIZMO: Mel's replacement toaster, assembled part by part (the running gag) */
const gizmo: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45);
  const parts: [number, string][] = (a.parts || []).map((p: any) => [Number(p[0]), String(p[1])]);
  const has = (k: number) => parts.length > k && t >= parts[k][0];
  const pp = (k: number) => (parts.length > k ? pop(t, parts[k][0], 0.4) : 0);
  const face: string = pick(a.faces, t, a.face || 'happy'), bl = ((t + i) % 3.1) < 0.12 || face === 'dead';
  const toast = a.toastAt !== undefined ? E.outBack(win(t, a.toastAt, 0.5)) * (1 - win(t, a.toastAt + 1.6, 0.8) * 0.6) : 0;
  const shake = a.toastAt !== undefined && t > a.toastAt - 0.6 && t < a.toastAt ? Math.sin(t * 60) * 4 : 0;
  // the last part added flashes its label
  const last = parts.filter((p) => t >= p[0]).pop();
  return <g key={'gz' + i} transform={`translate(${x + shake} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={4} rx={150} ry={14} fill={OL} opacity={0.18} />
    {a.smokeAt !== undefined && t >= a.smokeAt && Array.from({length: 4}, (_, q) => { const u = ((t - a.smokeAt) * 0.6 + q / 4) % 1;
      return <circle key={'sm' + q} cx={-40 + q * 26 + Math.sin(t * 2 + q) * 20} cy={-220 - u * 260} r={20 + u * 40} fill="#78909C" stroke={OL} strokeWidth={3} opacity={0.85 * (1 - u)} />; })}
    {/* toast slices */}
    {toast > 0 && [-40, 40].map((q) => <g key={q} transform={`translate(${q} ${-200 - 160 * toast})`}><rect x={-34} y={-50} width={68} height={70} rx={20} fill="#E3A857" stroke={OL} strokeWidth={4} /><rect x={-26} y={-42} width={52} height={54} rx={14} fill="#F7D79A" /></g>)}
    {/* body (part 0) */}
    {has(0) ? <g transform={`scale(${pp(0)})`}><rect x={-130} y={-200} width={260} height={190} rx={50} fill="#E9EEF2" stroke={OL} strokeWidth={6} />
      <rect x={-110} y={-120} width={220} height={18} rx={9} fill="#FFFFFF" opacity={0.6} /></g>
      : <rect x={-130} y={-200} width={260} height={190} rx={50} fill="none" stroke={OL} strokeWidth={4} strokeDasharray="14 12" opacity={0.5} />}
    {/* slots (part 1) */}
    {has(1) && <g transform={`scale(${pp(1)})`}>{[-40, 40].map((q) => <rect key={q} x={q - 30} y={-206} width={60} height={16} rx={6} fill="#37474F" stroke={OL} strokeWidth={3.5} />)}</g>}
    {/* heating coil glow (part 2) */}
    {has(2) && <g transform={`scale(${pp(2)})`}><path d="M -90 -70 q 15 -20 30 0 q 15 20 30 0 q 15 -20 30 0 q 15 20 30 0 q 15 -20 30 0 q 15 20 30 0" stroke="#FF7043" strokeWidth={6} fill="none" opacity={0.6 + 0.4 * Math.sin(t * 6)} /></g>}
    {/* lever (part 3) */}
    {has(3) && <g transform={`translate(150 ${-120 + (a.toastAt !== undefined && t > a.toastAt - 1.5 && t < a.toastAt ? 50 : 0)}) scale(${pp(3)})`}><rect x={-10} y={-14} width={50} height={28} rx={10} fill={RED} stroke={OL} strokeWidth={4} /></g>}
    {/* knob (part 4) */}
    {has(4) && <g transform={`translate(-150 -100) scale(${pp(4)}) rotate(${t * 40})`}><circle r={24} fill={ORANGE} stroke={OL} strokeWidth={4} /><path d="M 0 -18 L 0 0" stroke={OL} strokeWidth={4} /></g>}
    {/* plug + cord (part 5) */}
    {has(5) && <g transform={`scale(${pp(5)})`}><path d="M 120 -30 Q 200 0 230 -10" stroke={OL} strokeWidth={6} fill="none" /><rect x={226} y={-26} width={40} height={30} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><path d="M 266 -18 L 280 -18 M 266 -6 L 280 -6" stroke={OL} strokeWidth={4} /></g>}
    {/* feet (part 6) */}
    {has(6) && <g transform={`scale(${pp(6)})`}>{[-90, 90].map((q) => <rect key={q} x={q - 22} y={-14} width={44} height={16} rx={6} fill="#37474F" stroke={OL} strokeWidth={3} />)}</g>}
    {/* googly eyes once the body is in */}
    {has(0) && <g transform={`translate(0 -150) scale(${pp(0)})`}>{[-36, 36].map((q, k) => <g key={k}><circle cx={q} cy={0} r={face === 'shock' ? 24 : 20} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
      {bl ? <path d={`M ${q - 14} 0 L ${q + 14} 0`} stroke={OL} strokeWidth={4} /> : <circle cx={q + 4 * Math.sin(t * 2)} cy={face === 'worry' ? 6 : 2} r={face === 'shock' ? 6 : 9} fill={OL} />}</g>)}
      <path d={face === 'worry' || face === 'shock' ? 'M -16 46 Q 0 34 16 46' : 'M -18 36 Q 0 52 18 36'} stroke={OL} strokeWidth={5} fill="none" strokeLinecap="round" /></g>}
    {/* the label flash of the newest part */}
    {last && t < last[0] + 2.2 && <g transform={`translate(0 -300) scale(${pop(t, last[0], 0.35)})`}><rect x={-Math.max(110, last[1].length * 10 + 20)} y={-28} width={Math.max(220, last[1].length * 20 + 40)} height={46} rx={23} fill={YEL} stroke={OL} strokeWidth={4} /><T x={0} y={4} s={22}>{last[1]}</T></g>}
    {/* the bottom tag */}
    {a.stamp && t >= (a.stampAt ?? 1e9) && <g transform={`translate(${a.stampX ?? 0} ${a.stampY ?? 40}) scale(${pop(t, a.stampAt, 0.4)}) rotate(-6)`}><rect x={-Math.max(120, a.stamp.length * 11 + 24)} y={-26} width={Math.max(240, a.stamp.length * 22 + 48)} height={48} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={8} s={24} c={RED}>{a.stamp}</T></g>}
  </g>;
};

/** HOMEBOX: a cardboard box on little legs that walks (x keyframes); walks back home in the moving act */
const homebox: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, moving = Math.abs(vx) > 20, dir = vx < -20 ? -1 : 1;
  const ph = t * 12 + i, lg = moving ? Math.sin(ph) * 16 : 0, bob = moving ? Math.abs(Math.cos(ph)) * 8 : 0;
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.5) hy += Math.sin((u / 0.5) * Math.PI) * 90; }
  const face: string = pick(a.faces, t, a.face || 'happy'), bl = ((t + i * 0.7) % 2.7) < 0.12;
  return <g key={'hb' + i} transform={`translate(${x} ${y - bob - hy}) scale(${s * dir} ${s})`}>
    <ellipse cx={0} cy={4 + bob + hy} rx={60} ry={10} fill={OL} opacity={0.18} />
    <path d={`M -22 -40 L ${-22 - lg} 0 M 22 -40 L ${22 + lg} 0`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
    <ellipse cx={-22 - lg + 8} cy={-2} rx={14} ry={7} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><ellipse cx={22 + lg + 8} cy={-2} rx={14} ry={7} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
    <g transform="translate(0 -96)">{cbox(130, 100)}</g>
    <g transform={`translate(${moving ? 6 : 0} -110)`}>{[-24, 24].map((q, k) => <g key={k}><circle cx={q} cy={0} r={13} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
      {bl ? <path d={`M ${q - 9} 0 L ${q + 9} 0`} stroke={OL} strokeWidth={3.5} /> : <circle cx={q + 4} cy={face === 'worry' ? 4 : 1} r={6} fill={OL} />}</g>)}
      <path d={face === 'worry' ? 'M -12 30 Q 0 22 12 30' : face === 'grin' ? 'M -16 22 Q 0 38 16 22 Z' : 'M -12 24 Q 0 34 12 24'} stroke={OL} strokeWidth={4} fill={face === 'grin' ? '#FFFFFF' : 'none'} strokeLinecap="round" /></g>
    {a.label && <g transform={`scale(${dir} 1) translate(0 -62)`}><rect x={-60} y={-14} width={120} height={26} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={2.5} /><T x={0} y={6} s={fit(a.label, 112, 16)} c={RED}>{a.label}</T></g>}
    {moving && [0, 1].map((k) => { const u = ((t * 2.4 + k / 2) % 1); return <circle key={k} cx={-80 - u * 50} cy={-8 - u * 14} r={8 + u * 14} fill="#E8DCC8" stroke={OL} strokeWidth={2.5} opacity={0.8 * (1 - u)} />; })}
  </g>;
};

/** STACKBOX: a stack of shipping containers that fills (fill keyframes 0..1) with a pennant `text` */
const stackbox: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45), cols = a.cols ?? 3, rows = a.rows ?? 4, fl = clamp(kf(a.fill, t, 1));
  const n = Math.round(cols * rows * fl);
  return <g key={'sb' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {Array.from({length: n}, (_, k) => { const c = k % cols, r = Math.floor(k / cols), cx = (c - (cols - 1) / 2) * 150;
      return <g key={k} transform={`translate(${cx} ${-30 - r * 58})`}><rect x={-70} y={-28} width={140} height={56} rx={4} fill={CTR[(k * 3 + i) % CTR.length]} stroke={OL} strokeWidth={3.5} />
        {[1, 2, 3].map((q) => <path key={q} d={`M ${-70 + q * 35} -24 L ${-70 + q * 35} 24`} stroke={OL} strokeWidth={1.5} opacity={0.4} />)}</g>; })}
    {a.text && <g transform={`translate(0 ${-60 - rows * 58})`}><path d="M 0 0 L 0 -80" stroke={OL} strokeWidth={5} /><path d={`M 0 -80 L ${Math.max(140, a.text.length * 14)} ${-66 + 4 * Math.sin(t * 5)} L 0 -46 Z`} fill={YEL} stroke={OL} strokeWidth={4} /><T x={Math.max(60, a.text.length * 6)} y={-58} s={18}>{a.text}</T></g>}
  </g>;
};

export const FACTORY_ITEMS: Record<string, ItemFn> = {gizmo, homebox, stackbox};
export const FACTORY_INDOOR = ['kitchen', 'megafloor', 'refinery', 'solarline', 'fctitle', 'fcbumper'];
