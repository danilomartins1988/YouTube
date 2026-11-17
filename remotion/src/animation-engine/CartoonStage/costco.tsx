import React from 'react';
import {E, clamp, lerp, win} from '../motion';
import {OL} from './sitcom';

/**
 * CLUB kit for CartoonStage (Episode 57, "How Costco Makes Billions Selling Almost Nothing").
 *
 * Same owner direction as Ep 56 (feel like a prime-time animated TV sitcom, genre level only, everything original), but a new
 * show world: a members-only warehouse club. No store logos, typefaces or store designs: names appear only as plain text.
 * Sets (day scenes): clubfloor (warehouse floor, racks to the ceiling, skylights, pallets, sample stand, register lane),
 * memberdesk (membership desk, card printer, photo flash, queue rope), foodcourt (counter, menu board with the running-gag price,
 * roller grill, condiment pumps, picnic tables), housebrand (house-brand factory: plain boxes get the house label on a conveyor),
 * treasureaisle (spotlit turntable pallet whose item changes on cue, "HERE TODAY" banner), loadingdock (dock doors, trucks,
 * pallets that empty, a 30-day bill clock), gasbar (fuel canopy, pumps, a queue of cars), seattle83 (1983 opening day, rainy
 * Pacific Northwest), cashvault (special-dividend chute), clubtitle (show title card), clubbumper (act bumper with the
 * running gag: someone tries to change the hot-dog price board and fails).
 * Items: cardie (a walking membership-card mascot), membercard (giant flipping card), combo (hot dog + soda), palletstack
 * (goods that sell out on cue), receipt (unrolling receipt), feeladder (price-board gag prop).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS).
 */
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; night?: boolean; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; flip?: boolean; [k: string]: any};
export type SetFn = (t: number, z: Z, f: number) => React.ReactNode;
export type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const kf = (v: KF | undefined, t: number, d = 0): number => {
  if (v === undefined) return d;
  if (!Array.isArray(v)) return v;
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], v[i][0] - v[i - 1][0])));
  return v[v.length - 1][1];
};
const pick = <V,>(tl: any, t: number, d: V): V => { let v = d; if (Array.isArray(tl)) for (const [pt, pv] of tl) if (t >= Number(pt)) v = pv; return v; };
const jig = (t: number, at: number, k = 14, d = 5) => (t < at ? 0 : Math.exp(-d * (t - at)) * Math.sin(k * (t - at)));
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.62);
const GOODS = ['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB', '#FFC93C', '#F06292', '#26A69A', '#FF7043', '#5C6BC0', '#E0E0E0'];
const BOXT = ['PAPER TOWELS x30', 'KETCHUP x3', 'COFFEE 3 LB', 'BATTERIES x48', 'OLIVE OIL 2 L', 'SOCKS x12', 'NUTS 2.5 LB', 'TV 75"', 'DIAPERS x200', 'WATER x40'];

/* ------------------------------------------------------------------------------------------------ shared pieces */
const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
/** a pallet of bulk goods: wooden pallet + stacked cartons (n rows x 3), wrap shine; `left` 0..1 fraction still on it */
const pallet = (x: number, y: number, k: number, t: number, s = 1, left = 1, label?: string) => {
  const rows = 3, n = rows * 3, keep = Math.round(n * clamp(left));
  return <g key={'pl' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-120} y={-26} width={240} height={26} fill="#C99A5B" stroke={OL} strokeWidth={4} />
    {[-90, 0, 90].map((px) => <rect key={px} x={px - 16} y={-20} width={32} height={20} fill="#A9783F" stroke={OL} strokeWidth={2.5} />)}
    {Array.from({length: n}, (_, q) => { if (q >= keep) return null; const r = Math.floor(q / 3), c = q % 3, cc = GOODS[(k * 3 + q) % GOODS.length];
      return <g key={q}><rect x={-114 + c * 76} y={-26 - (r + 1) * 66} width={72} height={64} rx={4} fill={cc} stroke={OL} strokeWidth={3.5} />
        <rect x={-108 + c * 76} y={-26 - (r + 1) * 66 + 8} width={60} height={14} rx={3} fill="#FFFFFF" opacity={0.75} /></g>; })}
    {keep > 0 && <path d={`M -110 ${-30 - Math.ceil(keep / 3) * 66} L -60 -30`} stroke="#FFFFFF" strokeWidth={6} opacity={0.35 + 0.1 * Math.sin(t * 2 + k)} />}
    {label && keep > 0 && <g transform={`translate(0 ${-40 - Math.ceil(keep / 3) * 66})`}><rect x={-110} y={-30} width={220} height={40} rx={8} fill="#FFFDF4" stroke={OL} strokeWidth={3.5} />
      <T x={0} y={-2} s={fit(label, 200, 22)}>{label}</T></g>}
  </g>;
};
/** steel pallet rack bay: orange beams, blue uprights, shrink-wrapped overstock on top levels */
const rack = (x: number, f: number, k: number, t: number, h = 760, w = 420) => <g key={'rk' + k}>
  {[0, w].map((ux) => <rect key={ux} x={x + ux - 10} y={f - h} width={20} height={h} fill="#2F6FD1" stroke={OL} strokeWidth={4} />)}
  {[0.42, 0.7].map((lv, li) => { const by = f - h * lv; return <g key={li}>
    <rect x={x - 10} y={by} width={w + 20} height={22} fill="#FF8F1F" stroke={OL} strokeWidth={4} />
    {[0, 1, 2].map((q) => { const cc = GOODS[(k * 5 + li * 3 + q) % GOODS.length], bh = 100 + rnd(k * 13 + li * 3 + q) * 80;
      return <g key={q}><rect x={x + 14 + q * 134} y={by - bh} width={124} height={bh} rx={4} fill={cc} stroke={OL} strokeWidth={3.5} />
        <path d={`M ${x + 20 + q * 134} ${by - bh + 10} L ${x + 60 + q * 134} ${by - 8}`} stroke="#FFFFFF" strokeWidth={5} opacity={0.35} /></g>; })}</g>; })}
  {Array.from({length: 7}, (_, q) => <path key={q} d={`M ${x} ${f - h + q * 100 + 40} L ${x + 10} ${f - h + q * 100 + 90}`} stroke="#1E4F9E" strokeWidth={3} />)}
</g>;
const concrete = (z: Z, f: number, line = '#FFD23F') => { const w = z.x1 - z.x0; return <g>
  <rect x={z.x0} y={f} width={w} height={800} fill="#C8CDD2" />
  {Array.from({length: Math.ceil(w / 260)}, (_, k) => <path key={'cj' + k} d={`M ${z.x0 + k * 260} ${f} L ${z.x0 + k * 260 - 160} ${f + 600}`} stroke="#B3B9BF" strokeWidth={4} />)}
  <path d={`M ${z.x0} ${f + 120} L ${z.x1} ${f + 120}`} stroke={line} strokeWidth={14} strokeDasharray="80 50" />
  <rect x={z.x0} y={f} width={w} height={16} fill="#AEB4BA" stroke={OL} strokeWidth={4} /></g>; };
const ceiling = (z: Z, f: number, t: number, top = 980) => { const w = z.x1 - z.x0; return <g>
  <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E8ECEF" />
  {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const sx = z.x0 + k * 360; return <g key={'sl' + k}>
    <path d={`M ${sx} ${f - top} L ${sx + 180} ${f - top - 70} L ${sx + 360} ${f - top}`} fill="none" stroke="#90A4AE" strokeWidth={8} />
    <rect x={sx + 120} y={f - top - 40} width={120} height={36} rx={4} fill="#DDF3FF" stroke={OL} strokeWidth={3} />
    <path d={`M ${sx + 130} ${f - top} L ${sx + 40} ${f - 200} L ${sx + 330} ${f - 200} L ${sx + 230} ${f - top} Z`} fill="#FFFDE7" opacity={0.18 + 0.03 * Math.sin(t * 1.3 + k)} /></g>; })}
  <path d={`M ${z.x0} ${f - top + 8} L ${z.x1} ${f - top + 8}`} stroke="#78909C" strokeWidth={10} /></g>; };

/* ================================================================================================ ITEMS */
/** CARDIE: a walking membership card with a deadpan LED face. x/y keyframes, face/faces ('deadpan'|'happy'|'alarm'|'wink'|'dollar'|'sleepy'),
 *  hops [t], say [[t0,t1,text]] (speech bubble), flips [t] (spins 360 to show the back "$65/YR" or `back` text), label */
export const cardie: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45) * (a.until !== undefined ? 1 - win(t, a.until, 0.35) : 1);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, moving = Math.abs(vx) > 30, fl = a.flip !== undefined ? (a.flip ? -1 : 1) : (vx < -30 ? -1 : 1);
  const face: string = pick(a.faces, t, a.face || 'deadpan');
  let hy = 0, sq = 1;
  for (const h of (a.hops || []) as number[]) { const u = t - h; if (u > -0.12 && u < 0) sq = 1 - 0.18 * ((u + 0.12) / 0.12); else if (u >= 0 && u < 0.5) { hy = Math.sin((u / 0.5) * Math.PI) * 110; sq = 1 + 0.12 * Math.sin((u / 0.5) * Math.PI); } }
  let spin = 1;
  for (const fp of (a.flips || []) as number[]) { const u = win(t, fp, 0.7); if (u > 0 && u < 1) spin = Math.cos(u * Math.PI * 2); }
  const back = spin < 0, cyc = moving ? t * 10 + i : 0, legA = moving ? Math.sin(cyc) * 26 : 0;
  const led = face === 'alarm' ? (Math.sin(t * 14) > 0 ? '#FF5252' : '#7A1A1A') : '#5CF2FF';
  const bl = ((t + i) % 3.4) < 0.12;
  const eyes = face === 'happy' ? [-34, 34].map((c) => <path key={c} d={`M ${c - 14} -150 Q ${c} -170 ${c + 14} -150`} stroke={led} strokeWidth={7} fill="none" strokeLinecap="round" />)
    : face === 'alarm' ? [-34, 34].map((c) => <circle key={c} cx={c} cy={-156} r={13} stroke={led} strokeWidth={7} fill="none" />)
    : face === 'dollar' ? [-34, 34].map((c) => <T key={c} x={c} y={-142} s={38} c="#7CFF8A">$</T>)
    : face === 'wink' ? [<path key="w1" d="M -48 -156 L -20 -156" stroke={led} strokeWidth={7} strokeLinecap="round" />, <rect key="w2" x={22} y={-170} width={24} height={26} rx={5} fill={led} />]
    : face === 'sleepy' ? [-34, 34].map((c) => <path key={c} d={`M ${c - 14} -154 L ${c + 14} -154`} stroke={led} strokeWidth={7} strokeLinecap="round" />)
    : [-34, 34].map((c) => bl ? <path key={c} d={`M ${c - 14} -156 L ${c + 14} -156`} stroke={led} strokeWidth={7} strokeLinecap="round" /> : <rect key={c} x={c - 14} y={-164} width={28} height={12} rx={4} fill={led} />);
  const says: any[] = (a.say || []).filter((sy: any) => t >= Number(sy[0]) && t <= Number(sy[1]));
  const lab: string | null = a.label && t < (a.labelUntil ?? at + 4) ? String(a.label) : null;
  return <g key={'cd' + i} transform={`translate(${x} ${y - hy}) scale(${s * fl} ${s})`}>
    <ellipse cx={0} cy={4 + hy} rx={90} ry={12} fill={OL} opacity={0.18} />
    {[-1, 1].map((sd) => { const la = sd * legA; return <g key={'lg' + sd}><path d={`M ${sd * 34} -40 L ${sd * 34 + Math.sin((la * Math.PI) / 180) * 40} 0`} stroke={OL} strokeWidth={10} strokeLinecap="round" />
      <ellipse cx={sd * 34 + Math.sin((la * Math.PI) / 180) * 40 + 10} cy={-4} rx={20} ry={10} fill="#E53950" stroke={OL} strokeWidth={4} /></g>; })}
    <g transform={`scale(${Math.max(0.06, Math.abs(spin)) * (2 - sq)} ${sq}) rotate(${moving ? Math.sin(cyc) * 3 : Math.sin(t * 2 + i) * 2} 0 -120)`}>
      <rect x={-110} y={-220} width={220} height={180} rx={22} fill={back ? '#F5F7FA' : '#FFFFFF'} stroke={OL} strokeWidth={6} />
      {!back ? <g>
        <rect x={-110} y={-220} width={220} height={44} rx={22} fill="#E53950" stroke={OL} strokeWidth={6} /><rect x={-104} y={-196} width={208} height={20} fill="#E53950" />
        <T x={0} y={-188} s={22} c="#FFFFFF" ls={3}>MEMBER</T>
        <rect x={-72} y={-176} width={144} height={60} rx={10} fill="#0E1E36" stroke={OL} strokeWidth={4} />{eyes}
        <rect x={-30} y={-104} width={60} height={10} rx={5} fill={OL} />
        <rect x={-96} y={-84} width={70} height={30} rx={5} fill="#FFC93C" stroke={OL} strokeWidth={3} /><path d="M -96 -69 L -26 -69 M -61 -84 L -61 -54" stroke="#C99A1E" strokeWidth={2.5} />
        <rect x={-10} y={-80} width={100} height={8} rx={4} fill="#B0BEC5" /><rect x={-10} y={-64} width={70} height={8} rx={4} fill="#B0BEC5" />
      </g> : <g><rect x={-110} y={-190} width={220} height={34} fill="#37474F" /><T x={0} y={-90} s={fit(a.back || '$65 / YEAR', 200, 40)} c="#E53950">{a.back || '$65 / YEAR'}</T></g>}
      {[-1, 1].map((sd) => <path key={'ar' + sd} d={`M ${sd * 110} -140 Q ${sd * 150} ${-120 + Math.sin(t * 4 + sd + i) * 16} ${sd * 156} ${-90 + Math.sin(t * 4 + sd + i) * 20}`} stroke={OL} strokeWidth={10} fill="none" strokeLinecap="round" />)}
    </g>
    {says.map((sy, k) => { const txt = String(sy[2]), u = E.outBack(win(t, Number(sy[0]), 0.3)), w = Math.max(...txt.split('\n').map((l) => l.length)) * 20 + 50, h = txt.split('\n').length * 36 + 26;
      return <g key={'sy' + k} transform={`translate(${fl * 0 + 120} -300) scale(${u * fl} ${u})`}><path d="M -40 30 L -90 90 L -10 30 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={18} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        {txt.split('\n').map((l, q) => <T key={q} x={0} y={-h / 2 + 40 + q * 36} s={30}>{l}</T>)}</g>; })}
    {lab && <g transform={`translate(0 -270) scale(${fl} 1)`}><rect x={-lab.length * 9 - 18} y={-26} width={lab.length * 18 + 36} height={40} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={2} s={22}>{lab}</T></g>}
  </g>;
};

/** giant membership card that flips on cue: front "MEMBER" (+ `name`), back `back` text; sparkles; flipAt */
export const membercard: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, at, 0.55) * (a.until !== undefined ? 1 - win(t, a.until, 0.35) : 1);
  const fu = a.flipAt !== undefined ? win(t, a.flipAt, 0.6) : 0, sc = Math.cos(fu * Math.PI), back = sc < 0;
  const tilt = Math.sin(t * 1.4 + i) * 4;
  return <g key={'mc' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${tilt})`}>
    {Array.from({length: 10}, (_, k) => { const an = t * 0.8 + (k / 10) * Math.PI * 2; return <path key={'ry' + k} d={`M 0 0 L ${Math.cos(an) * 520} ${Math.sin(an) * 360} L ${Math.cos(an + 0.18) * 520} ${Math.sin(an + 0.18) * 360} Z`} fill="#FFE082" opacity={0.25} />; })}
    <g transform={`scale(${Math.max(0.04, Math.abs(sc))} 1)`}>
      <rect x={-330} y={-200} width={660} height={400} rx={36} fill="#FFFFFF" stroke={OL} strokeWidth={10} />
      {!back ? <g><rect x={-330} y={-200} width={660} height={96} rx={36} fill={a.color || '#E53950'} stroke={OL} strokeWidth={10} /><rect x={-320} y={-150} width={640} height={46} fill={a.color || '#E53950'} />
        <T x={0} y={-132} s={56} c="#FFFFFF" ls={10}>{a.title || 'MEMBER'}</T>
        <rect x={-280} y={-60} width={170} height={200} rx={16} fill="#CFD8DC" stroke={OL} strokeWidth={5} /><circle cx={-195} cy={10} r={44} fill="#90A4AE" stroke={OL} strokeWidth={4} /><path d="M -260 130 Q -195 50 -130 130" fill="#90A4AE" stroke={OL} strokeWidth={4} />
        <T x={70} y={-10} s={fit(a.name || 'HOUSEHOLD: 2 CARDS', 380, 34)} a="middle">{a.name || 'HOUSEHOLD: 2 CARDS'}</T>
        <rect x={-80} y={30} width={300} height={16} rx={8} fill="#B0BEC5" /><rect x={-80} y={64} width={220} height={16} rx={8} fill="#B0BEC5" />
        <rect x={-80} y={100} width={360} height={56} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={3} />{Array.from({length: 26}, (_, k) => <rect key={k} x={-72 + k * 13.5} y={106} width={k % 3 ? 5 : 9} height={44} fill={OL} />)}</g>
        : <g><rect x={-330} y={-130} width={660} height={70} fill="#37474F" /><T x={0} y={40} s={fit(a.back || '$65 A YEAR', 600, 96)} c="#E53950">{a.back || '$65 A YEAR'}</T>
          {a.backSub && <T x={0} y={120} s={fit(a.backSub, 600, 34)} c="#6B7385" w={700}>{a.backSub}</T>}</g>}
      <path d={`M ${-300 + ((t * 300) % 900)} -200 L ${-380 + ((t * 300) % 900)} 200`} stroke="#FFFFFF" strokeWidth={30} opacity={0.35} />
    </g>
    {Array.from({length: 6}, (_, k) => { const u = (t * 0.7 + k / 6) % 1, an = k * 1.1; return <path key={'sp' + k} transform={`translate(${Math.cos(an) * (360 + u * 60)} ${Math.sin(an) * (240 + u * 40)}) scale(${Math.sin(u * Math.PI)})`}
      d="M 0 -18 L 5 -5 L 18 0 L 5 5 L 0 18 L -5 5 L -18 0 L -5 -5 Z" fill="#FFD23F" stroke={OL} strokeWidth={2.5} />; })}
  </g>;
};

/** hot dog + soda combo, steaming, with a swinging price tag (`price`), bounce on `boing` times; `face` gives the dog eyes */
export const combo: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, at, 0.5) * (a.until !== undefined ? 1 - win(t, a.until, 0.35) : 1);
  let sq = 0; for (const b of (a.boing || []) as number[]) sq += jig(t, b, 18, 5);
  const face: string = pick(a.faces, t, a.face || 'happy');
  return <g key={'cb' + i} transform={`translate(${x} ${y}) scale(${s * (1 + 0.15 * sq)} ${s * (1 - 0.15 * sq)})`}>
    <ellipse cx={0} cy={110} rx={300} ry={22} fill={OL} opacity={0.15} />
    {/* soda */}
    <g transform="translate(190 0)"><path d="M -70 -150 L 70 -150 L 54 110 L -54 110 Z" fill="#FFFFFF" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
      <path d="M -66 -90 L 66 -90 L 60 10 L -60 10 Z" fill="#E53950" /><path d="M -80 -170 L 80 -170 L 76 -148 L -76 -148 Z" fill="#ECEFF1" stroke={OL} strokeWidth={6} />
      <path d={`M 20 -170 L 46 -280 L 70 -280`} stroke="#FFC93C" strokeWidth={14} fill="none" strokeLinecap="round" /><path d="M 20 -170 L 46 -280" stroke={OL} strokeWidth={3} />
      {[0, 1, 2].map((k) => { const u = (t * 0.8 + k / 3) % 1; return <circle key={k} cx={-30 + k * 26} cy={60 - u * 140} r={6 * (1 - u) + 2} fill="#FFFFFF" opacity={0.8} />; })}</g>
    {/* hot dog */}
    <g transform="translate(-130 30)"><path d="M -200 -10 Q -200 -70 -150 -70 L 150 -70 Q 200 -70 200 -10 Q 200 40 150 40 L -150 40 Q -200 40 -200 -10 Z" fill="#F2C179" stroke={OL} strokeWidth={7} />
      <path d="M -230 -40 Q -236 -86 -190 -88 L 190 -88 Q 236 -86 230 -40 Q 226 -10 190 -12 L -190 -12 Q -226 -10 -230 -40 Z" fill="#C8553D" stroke={OL} strokeWidth={7} />
      <path d={`M -170 -54 ${Array.from({length: 9}, (_, k) => `Q ${-150 + k * 40} ${-70 + (k % 2 ? 22 : -22) * (1 + 0.15 * Math.sin(t * 4 + k))} ${-130 + k * 40} -54`).join(' ')}`} fill="none" stroke="#FFD23F" strokeWidth={12} strokeLinecap="round" />
      {face !== 'none' && <g>{[-50, 30].map((c) => <g key={c}><ellipse cx={c} cy={-44} rx={18} ry={22} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={c + 4} cy={-40} r={face === 'shock' ? 4 : 8} fill={OL} /></g>)}
        {face === 'smug' ? <path d="M -30 -2 Q 0 6 26 -12" stroke={OL} strokeWidth={6} fill="none" strokeLinecap="round" /> : face === 'shock' ? <ellipse cx={-6} cy={0} rx={12} ry={16} fill="#6B2E2A" stroke={OL} strokeWidth={4} />
          : <path d="M -36 -10 Q -6 20 24 -10" stroke={OL} strokeWidth={6} fill="none" strokeLinecap="round" />}</g>}
      {[0, 1, 2].map((k) => { const u = (t * 0.6 + k / 3) % 1; return <path key={k} d={`M ${-100 + k * 90} ${-110 - u * 120} q 16 -20 0 -40 q -16 -20 0 -40`} stroke="#FFFFFF" strokeWidth={8} fill="none" strokeLinecap="round" opacity={0.8 * (1 - u)} />; })}</g>
    {a.price && <g transform={`translate(-20 -230) rotate(${Math.sin(t * 2.2) * 8})`}><path d="M 0 -60 L 0 -20" stroke={OL} strokeWidth={4} />
      <path d="M -130 0 L -100 -30 L 130 -30 L 130 70 L -100 70 L -130 40 Z" fill="#FFFDF4" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
      <T x={10} y={42} s={fit(String(a.price), 220, 70)} c="#E53950">{a.price}</T></g>}
  </g>;
};

/** a row of `n` pallets; each sells out (cartons vanish) between sellFrom and sellTo; optional labels */
export const palletstack: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45), n = a.n ?? 3, labels: string[] = a.labels || [];
  return <g key={'ps' + i} transform={`translate(${x} ${y}) scale(${s})`}>{Array.from({length: n}, (_, k) => {
    const left = a.sellFrom !== undefined ? 1 - win(t, a.sellFrom + k * 0.25, (a.sellTo ?? a.sellFrom + 2) - a.sellFrom) : 1;
    return pallet((k - (n - 1) / 2) * 270, 0, k + i, t, 1, left, labels[k]); })}</g>;
};

/** long receipt that unrolls line by line: lines [[t, text, amount?]], total at totalAt */
export const receipt: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const lines: [number, string, string?][] = (a.lines || []).map((l: any) => [Number(l[0]), String(l[1]), l[2] !== undefined ? String(l[2]) : undefined]);
  const shown = lines.filter((l) => t >= l[0]), tot = a.totalAt !== undefined && t >= a.totalAt;
  const h = 120 + shown.length * 50 + (tot ? 90 : 0);
  return <g key={'rc' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 1.6 + i) * 1.5})`}>
    <path d={`M -200 0 L 200 0 L 200 ${h} ${Array.from({length: 16}, (_, k) => `L ${200 - (k + 0.5) * 25} ${h + (k % 2 ? 0 : 14)}`).join(' ')} L -200 ${h} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    <T x={0} y={56} s={30} ls={4}>{a.title || 'RECEIPT'}</T><path d="M -170 80 L 170 80" stroke={OL} strokeWidth={3} strokeDasharray="8 8" />
    {shown.map((l, k) => <g key={k} opacity={E.out(win(t, l[0], 0.3))}><T x={-170} y={124 + k * 50} s={fit(l[1], 260, 28)} a="start" w={700}>{l[1]}</T>
      {l[2] && <T x={170} y={124 + k * 50} s={28} a="end" c={l[2].startsWith('-') ? '#2E9E5B' : OL}>{l[2]}</T>}</g>)}
    {tot && <g transform={`translate(0 ${120 + shown.length * 50 + 40}) scale(${pop(t, a.totalAt, 0.4)})`}><path d="M -170 -36 L 170 -36" stroke={OL} strokeWidth={4} />
      <T x={-170} y={14} s={34} a="start">{a.totalLabel || 'TOTAL'}</T><T x={170} y={14} s={40} a="end" c="#E53950">{a.total}</T></g>}
  </g>;
};

/* ================================================================================================ SETS */
export const CLUB_SETS: Record<string, SetFn> = {
  /** WAREHOUSE FLOOR: skylights and trusses, steel racks to the ceiling with overstock, pallets of bulk goods on the floor, hanging
   *  aisle signs, optional register lane (regX) with a conveyor of giant packs, optional sample stand (sampleX) */
  clubfloor: (t, z, f) => {
    const w = z.x1 - z.x0, reg = z.regX, smp = z.sampleX, signs: string[] = z.signs || ['AISLE 1', 'BULK', 'AISLE 2', 'PALLETS', 'AISLE 3'];
    const gap = (x: number) => (reg !== undefined && Math.abs(x - reg) < 420) || (smp !== undefined && Math.abs(x - smp) < 300);
    return <g>
      {ceiling(z, f, t)}
      {Array.from({length: Math.ceil(w / 480)}, (_, k) => { const rx = z.x0 + k * 480 + 30; return gap(rx + 210) ? null : rack(rx, f - 20, k, t); })}
      {Array.from({length: Math.ceil(w / 960)}, (_, k) => { const hx = z.x0 + 480 + k * 960, txt = signs[k % signs.length];
        return <g key={'as' + k} transform={`translate(${hx} ${f - 900}) rotate(${Math.sin(t * 1.2 + k) * 3})`}><path d="M -50 -60 L -50 0 M 50 -60 L 50 0" stroke={OL} strokeWidth={3} />
          <rect x={-120} y={0} width={240} height={64} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={44} s={fit(txt, 220, 34)}>{txt}</T></g>; })}
      {concrete(z, f)}
      {Array.from({length: Math.ceil(w / 480)}, (_, k) => { const px = z.x0 + k * 480 + 240; return gap(px) ? null : pallet(px, f + 6, k + 3, t, 0.85, 1, z.palletLabels ? z.palletLabels[k % z.palletLabels.length] : undefined); })}
      {smp !== undefined && <g transform={`translate(${smp} ${f})`}><rect x={-120} y={-150} width={240} height={150} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <path d="M -140 -170 L 140 -170 L 120 -150 L -120 -150 Z" fill="#7BD389" stroke={OL} strokeWidth={4} /><rect x={-150} y={-330} width={300} height={70} rx={12} fill="#FFC93C" stroke={OL} strokeWidth={4} /><T x={0} y={-284} s={34}>FREE SAMPLES</T>
        <path d="M -140 -260 L -140 -170 M 140 -260 L 140 -170" stroke={OL} strokeWidth={5} />
        {Array.from({length: 6}, (_, k) => <g key={k}><circle cx={-90 + k * 36} cy={-176} r={13} fill={['#FFB74D', '#A1887F', '#FFF176'][k % 3]} stroke={OL} strokeWidth={3} /><path d={`M ${-90 + k * 36} -176 L ${-86 + k * 36} -206`} stroke="#8D6E63" strokeWidth={3} /></g>)}</g>}
      {reg !== undefined && <g transform={`translate(${reg} ${f})`}>
        <rect x={-380} y={-130} width={600} height={130} fill="#ECEFF1" stroke={OL} strokeWidth={5} /><rect x={-380} y={-150} width={600} height={26} rx={6} fill="#546E7A" stroke={OL} strokeWidth={4} />
        {Array.from({length: 4}, (_, k) => { const u = ((t * 0.35 + k / 4) % 1), bx = -360 + u * 520; return <g key={k} transform={`translate(${bx} -150)`} opacity={u < 0.92 ? 1 : (1 - u) * 12}>
          <rect x={-50} y={-90} width={100} height={90} rx={6} fill={GOODS[(k * 3 + 1) % GOODS.length]} stroke={OL} strokeWidth={4} /><rect x={-40} y={-74} width={80} height={18} rx={4} fill="#FFFFFF" opacity={0.8} /></g>; })}
        <g transform="translate(300 -150)"><rect x={-70} y={-110} width={140} height={110} rx={10} fill="#37474F" stroke={OL} strokeWidth={4} /><rect x={-56} y={-98} width={112} height={56} rx={4} fill="#80CBC4" />
          <T x={0} y={-58} s={24} c="#0E1E36">{Math.floor(t * 2.5) % 2 ? 'BEEP' : 'BULK!'}</T></g>
        <path d="M 240 -420 L 240 -260" stroke={OL} strokeWidth={6} /><rect x={170} y={-480} width={140} height={70} rx={12} fill="#2E9E5B" stroke={OL} strokeWidth={4} /><T x={240} y={-434} s={30} c="#FFFFFF">OPEN</T>
      </g>}
    </g>;
  },

  /** MEMBERSHIP DESK: long counter, sign (plain text), card printer spitting cards (printAt), photo camera with flash (flashAt list),
   *  queue rope with brass posts, wall poster `feeText`, wall screen `screen` text */
  memberdesk: (t, z, f) => {
    const w = z.x1 - z.x0, dx = z.deskX ?? z.x0 + w * 0.5, flashes: number[] = z.flashAt || [], pr = z.printAt ?? 1e9;
    const fl = flashes.some((fa) => t >= fa && t < fa + 0.25);
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#F3E9DA" />
      <rect x={z.x0} y={f - 980} width={w} height={40} fill="#D7CCC8" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'pn' + k} x={z.x0 + k * 300} y={f - 940} width={300} height={940} fill={k % 2 ? '#F7EFE3' : '#F0E5D4'} />)}
      {/* big sign */}
      <g transform={`translate(${dx} ${f - 780}) rotate(${Math.sin(t * 1.1) * 1.5})`}><rect x={-360} y={-70} width={720} height={130} rx={20} fill="#2F6FD1" stroke={OL} strokeWidth={7} />
        <T x={0} y={20} s={70} c="#FFFFFF" ls={6}>{z.title || 'MEMBERSHIP'}</T></g>
      {/* poster + screen */}
      <g transform={`translate(${dx - 620} ${f - 600})`}><rect x={-150} y={-120} width={300} height={240} rx={14} fill="#FFFDF4" stroke={OL} strokeWidth={5} />
        <T x={0} y={-58} s={28} c="#6B7385">{z.posterTop || 'JOIN TODAY'}</T><T x={0} y={20} s={fit(z.feeText || '$65 / YEAR', 270, 62)} c="#E53950">{z.feeText || '$65 / YEAR'}</T>
        <T x={0} y={80} s={22} w={700}>{z.posterSub || 'U.S. GOLD STAR'}</T></g>
      {z.screen && <g transform={`translate(${dx + 620} ${f - 620})`}><rect x={-190} y={-110} width={380} height={220} rx={14} fill="#263238" stroke={OL} strokeWidth={6} />
        <rect x={-170} y={-92} width={340} height={184} rx={8} fill="#0E2A3A" /><T x={0} y={-36} s={24} c="#80DEEA">{z.screenTop || 'RENEWALS'}</T>
        <T x={0} y={36} s={fit(z.screen, 320, 64)} c="#7CFF8A">{z.screen}</T>{Math.floor(t * 2) % 2 ? <circle cx={150} cy={-70} r={8} fill="#FF5252" /> : null}</g>}
      {/* counter */}
      <rect x={dx - 460} y={f - 230} width={920} height={230} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
      <rect x={dx - 480} y={f - 254} width={960} height={32} rx={8} fill="#8D6E63" stroke={OL} strokeWidth={5} />
      <path d={`M ${dx - 460} ${f - 140} L ${dx + 460} ${f - 140}`} stroke="#2F6FD1" strokeWidth={16} />
      {/* card printer */}
      <g transform={`translate(${dx + 280} ${f - 254})`}><rect x={-90} y={-110} width={180} height={110} rx={12} fill="#546E7A" stroke={OL} strokeWidth={5} /><rect x={-60} y={-40} width={120} height={14} rx={7} fill="#1B1B1B" />
        <circle cx={60} cy={-80} r={9} fill={Math.sin(t * 7) > 0 ? '#7CFF8A' : '#2E7D32'} stroke={OL} strokeWidth={2} />
        {t > pr && Array.from({length: 5}, (_, k) => { const u = clamp((t - pr - k * 0.7) / 0.9); if (u <= 0) return null; const flyU = clamp((t - pr - k * 0.7 - 0.9) / 1.4);
          return <g key={k} transform={`translate(${lerp(0, 120 + k * 40, E.out(flyU))} ${lerp(-34 - u * 46, 40 + k * 4 - 160, flyU) + flyU * 150}) rotate(${flyU * (40 + k * 30)})`}>
            <rect x={-46} y={-30} width={92} height={60} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><rect x={-46} y={-30} width={92} height={16} rx={8} fill="#E53950" /></g>; })}</g>
      {/* photo camera on a pole */}
      <g transform={`translate(${dx - 240} ${f - 254})`}><path d="M 0 0 L 0 -150" stroke={OL} strokeWidth={8} /><rect x={-50} y={-210} width={100} height={66} rx={10} fill="#37474F" stroke={OL} strokeWidth={4} />
        <circle cx={0} cy={-177} r={22} fill="#90CAF9" stroke={OL} strokeWidth={4} />{fl && <circle cx={0} cy={-177} r={90} fill="#FFFFFF" opacity={0.8} />}</g>
      {fl && <rect x={z.x0} y={-2500} width={w} height={4000} fill="#FFFFFF" opacity={0.35} />}
      {/* queue rope */}
      {[-1, 1].map((sd) => <g key={sd}>{[0, 1, 2].map((q) => { const px = dx + sd * (560 + q * 220); return <g key={q}><rect x={px - 10} y={f - 120} width={20} height={120} fill="#C9A227" stroke={OL} strokeWidth={3} /><circle cx={px} cy={f - 124} r={14} fill="#E0B93A" stroke={OL} strokeWidth={3} /></g>; })}
        <path d={`M ${dx + sd * 560} ${f - 110} Q ${dx + sd * 670} ${f - 60} ${dx + sd * 780} ${f - 110} Q ${dx + sd * 890} ${f - 60} ${dx + sd * 1000} ${f - 110}`} fill="none" stroke="#C62828" strokeWidth={10} /></g>)}
      <rect x={z.x0} y={f} width={w} height={800} fill="#D9CBB5" />
      {Array.from({length: Math.ceil(w / 140)}, (_, k) => <rect key={'tl' + k} x={z.x0 + k * 140} y={f} width={70} height={800} fill="#E2D6C2" opacity={0.6} />)}
      <rect x={z.x0} y={f} width={w} height={16} fill="#BFAE93" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** FOOD COURT: counter + menu board (the running-gag hot-dog price `price`, default $1.50), roller grill, soda fountain, condiment
   *  pumps that squirt, picnic tables with umbrellas; `boardX`, `tablesX` list; `shakeAt` jolts the board (gag) */
  foodcourt: (t, z, f) => {
    const w = z.x1 - z.x0, bx = z.boardX ?? z.x0 + w * 0.45, price: string = z.price || '$1.50', sh = z.shakeAt !== undefined ? jig(t, z.shakeAt, 30, 4) * 6 : 0;
    const tables: number[] = z.tablesX || [bx - 900, bx + 900];
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#FFF3E0" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <rect key={'st' + k} x={z.x0 + k * 120} y={f - 1000} width={60} height={110} fill={k % 2 ? '#E53950' : '#FFFFFF'} opacity={0.9} />)}
      <rect x={z.x0} y={f - 890} width={w} height={20} fill="#B71C1C" stroke={OL} strokeWidth={4} />
      {/* menu board */}
      <g transform={`translate(${bx + sh} ${f - 640}) rotate(${sh * 0.4})`}>
        <path d="M -200 -230 L -200 -300 M 200 -230 L 200 -300" stroke={OL} strokeWidth={5} />
        <rect x={-520} y={-230} width={1040} height={330} rx={18} fill="#1B2433" stroke={OL} strokeWidth={8} />
        <T x={0} y={-176} s={34} c="#FFE066" ls={6}>FOOD COURT</T>
        <rect x={-490} y={-150} width={560} height={220} rx={12} fill="#FFFDF4" stroke={OL} strokeWidth={4} />
        <T x={-210} y={-96} s={40}>HOT DOG + SODA</T>
        <g transform={`translate(-210 30) scale(${1 + 0.05 * Math.sin(t * 3)})`}><T x={0} y={0} s={fit(price, 480, 110)} c="#E53950">{price}</T></g>
        {['PIZZA', 'BAKE', 'SALAD', 'SMOOTHIE'].map((m, k) => <g key={m}><T x={300} y={-110 + k * 52} s={30} c="#FFFFFF">{m}</T><path d={`M 180 ${-100 + k * 52} L 420 ${-100 + k * 52}`} stroke="#FFFFFF" strokeWidth={2} strokeDasharray="4 8" opacity={0.4} /></g>)}
        {[0, 1, 2, 3, 4, 5].map((k) => <circle key={k} cx={-500 + k * 200} cy={-216} r={7} fill={(k + Math.floor(t * 3)) % 2 ? '#FFE066' : '#FF8A65'} />)}
      </g>
      {/* counter */}
      <rect x={bx - 640} y={f - 260} width={1280} height={260} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
      <rect x={bx - 660} y={f - 284} width={1320} height={30} rx={8} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
      {/* roller grill */}
      <g transform={`translate(${bx - 330} ${f - 284})`}><rect x={-170} y={-70} width={340} height={70} rx={10} fill="#78909C" stroke={OL} strokeWidth={5} />
        {Array.from({length: 6}, (_, k) => <g key={k} transform={`translate(${-140 + k * 56} -46) rotate(${t * 120 + k * 40})`}><rect x={-24} y={-11} width={48} height={22} rx={11} fill="#C8553D" stroke={OL} strokeWidth={3} /><path d="M -14 -4 L 14 -4" stroke="#8E3B2A" strokeWidth={3} /></g>)}
        {[0, 1].map((k) => { const u = (t * 0.6 + k / 2) % 1; return <path key={k} d={`M ${-60 + k * 100} ${-80 - u * 80} q 12 -16 0 -32`} stroke="#FFFFFF" strokeWidth={6} fill="none" opacity={1 - u} strokeLinecap="round" />; })}</g>
      {/* soda fountain */}
      <g transform={`translate(${bx + 300} ${f - 284})`}><rect x={-120} y={-200} width={240} height={200} rx={14} fill="#37474F" stroke={OL} strokeWidth={5} />
        {[0, 1, 2].map((k) => <g key={k}><rect x={-96 + k * 70} y={-180} width={52} height={70} rx={6} fill={['#E53950', '#FFC93C', '#7BD389'][k]} stroke={OL} strokeWidth={3} /><rect x={-80 + k * 70} y={-100} width={20} height={20} fill="#B0BEC5" stroke={OL} strokeWidth={2} /></g>)}</g>
      {/* condiment pumps */}
      <g transform={`translate(${bx + 560} ${f - 284})`}>{['#E53950', '#FFD23F', '#7BD389'].map((c, k) => { const pump = ((t * 0.9 + k * 0.33) % 1) < 0.15;
        return <g key={k} transform={`translate(${(k - 1) * 46} 0)`}><rect x={-18} y={-110} width={36} height={110} rx={8} fill={c} stroke={OL} strokeWidth={3.5} /><rect x={-6} y={pump ? -126 : -140} width={12} height={30} fill="#ECEFF1" stroke={OL} strokeWidth={2.5} />
          {pump && <circle cx={14} cy={-118} r={7} fill={c} stroke={OL} strokeWidth={2} />}</g>; })}</g>
      {/* picnic tables */}
      {tables.map((tx, k) => <g key={'tb' + k} transform={`translate(${tx} ${f})`}><path d={`M 0 -360 L 0 -150`} stroke={OL} strokeWidth={8} />
        <path d={`M -220 -340 Q 0 -${430 + 10 * Math.sin(t + k)} 220 -340 Z`} fill={k % 2 ? '#E53950' : '#2F6FD1'} stroke={OL} strokeWidth={5} />
        <path d="M -220 -340 L -170 -320 M 220 -340 L 170 -320" stroke={OL} strokeWidth={3} />
        <rect x={-200} y={-160} width={400} height={26} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><path d="M -170 -134 L -200 0 M 170 -134 L 200 0" stroke={OL} strokeWidth={8} />
        <rect x={-240} y={-80} width={480} height={18} rx={6} fill="#ECEFF1" stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f} width={w} height={800} fill="#E6DCCB" />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'ft' + k} x={z.x0 + k * 160} y={f} width={80} height={800} fill={k % 2 ? '#D7CBB6' : '#E6DCCB'} />)}
      <rect x={z.x0} y={f} width={w} height={16} fill="#C5B79E" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** HOUSE-BRAND FACTORY: plain brown boxes ride a conveyor through a labeller (machX) and come out with the house label (`label`,
   *  default "HOUSE BRAND") and a smaller price; a QC lamp; a quality-check robot arm; "SAVES 15-20%" ticker (`ticker`) */
  housebrand: (t, z, f) => {
    const w = z.x1 - z.x0, mx = z.x0 + w * (z.machX ?? 0.5), speed = z.speed ?? 150, lab: string = z.label || 'HOUSE BRAND', st = (t * 0.75) % 1;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E7F0E4" />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <g key={'wn' + k}><rect x={z.x0 + k * 300 + 50} y={f - 760} width={200} height={170} rx={10} fill="#D6F0FF" stroke={OL} strokeWidth={4} />
        <path d={`M ${z.x0 + k * 300 + 150} ${f - 760} L ${z.x0 + k * 300 + 150} ${f - 590}`} stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f - 520} width={w} height={22} fill="#A5B8A0" stroke={OL} strokeWidth={3} />
      {z.ticker && <g transform={`translate(${mx} ${f - 880})`}><rect x={-420} y={-50} width={840} height={90} rx={16} fill="#1B2433" stroke={OL} strokeWidth={5} />
        <T x={0} y={14} s={fit(z.ticker, 790, 44)} c="#FFE066">{z.ticker}</T></g>}
      {/* conveyor */}
      <rect x={z.x0} y={f - 150} width={w} height={40} rx={20} fill="#546E7A" stroke={OL} strokeWidth={5} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => <circle key={'rl' + k} cx={z.x0 + ((k * 60 + t * speed) % w)} cy={f - 130} r={12} fill="#90A4AE" stroke={OL} strokeWidth={2.5} />)}
      <rect x={z.x0} y={f - 110} width={w} height={110} fill="#78909C" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 320) + 1}, (_, k) => { const bx = z.x0 - 320 + ((k * 320 + t * speed) % (w + 320)), done = bx > mx + 100;
        return <g key={'bx' + k} transform={`translate(${bx} ${f - 150})`}>
          <rect x={-90} y={-150} width={180} height={150} rx={6} fill={done ? '#FFFFFF' : '#C99A5B'} stroke={OL} strokeWidth={5} />
          {!done && <path d="M -90 -110 L 90 -110 M 0 -150 L 0 -110" stroke="#A9783F" strokeWidth={4} />}
          {done && <g><rect x={-80} y={-138} width={160} height={46} rx={6} fill="#B71C1C" /><T x={0} y={-106} s={fit(lab, 150, 24)} c="#FFFFFF">{lab}</T>
            <T x={0} y={-54} s={22} w={700}>{BOXT[k % BOXT.length].split(' ')[0]}</T>
            <g transform="translate(60 -10) rotate(-10)"><rect x={-44} y={-20} width={88} height={36} rx={6} fill="#FFF59D" stroke={OL} strokeWidth={3} /><T x={0} y={7} s={20} c="#2E9E5B">LOWER</T></g></g>}
        </g>; })}
      {/* labeller machine */}
      <g transform={`translate(${mx} ${f - 150})`}>
        <path d="M -150 -40 L -150 -380 Q -150 -430 -100 -430 L 100 -430 Q 150 -430 150 -380 L 150 -40" fill="#2E9E5B" stroke={OL} strokeWidth={6} />
        <rect x={-110} y={-220} width={220} height={180} fill="#1B5E20" stroke={OL} strokeWidth={5} />
        <g transform={`translate(0 ${-370 + (st < 0.2 ? E.in(st / 0.2) * 130 : 130 * (1 - E.out((st - 0.2) / 0.8)))})`}><rect x={-16} y={-60} width={32} height={60} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
          <rect x={-80} y={0} width={160} height={44} rx={6} fill="#B71C1C" stroke={OL} strokeWidth={5} /></g>
        <rect x={-140} y={-424} width={280} height={52} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-388} s={26}>{z.machLabel || 'LABEL-O-MATIC'}</T>
        {[0, 1, 2].map((k) => <circle key={k} cx={-70 + k * 70} cy={-270} r={14} fill={(k + Math.floor(t * 4)) % 3 === 0 ? '#FFD54F' : '#7CFF8A'} stroke={OL} strokeWidth={3} />)}
      </g>
      {/* QC arm */}
      <g transform={`translate(${mx + 420} ${f - 150})`}><rect x={-40} y={-30} width={80} height={30} fill="#455A64" stroke={OL} strokeWidth={4} />
        <g transform={`rotate(${-30 + 20 * Math.sin(t * 2.4)})`}><rect x={-12} y={-230} width={24} height={200} rx={10} fill="#FFB300" stroke={OL} strokeWidth={4} />
          <g transform={`translate(0 -230) rotate(${60 + 30 * Math.sin(t * 2.4 + 1)})`}><rect x={-10} y={-140} width={20} height={140} rx={8} fill="#FFB300" stroke={OL} strokeWidth={4} />
            <g transform="translate(0 -150)"><circle r={26} fill="#ECEFF1" stroke={OL} strokeWidth={4} /><path d="M -12 0 L -3 10 L 14 -10" stroke="#2E9E5B" strokeWidth={6} fill="none" strokeLinecap="round" /></g></g></g></g>
      <rect x={z.x0} y={f} width={w} height={800} fill="#C9D3C6" />
      <path d={`M ${z.x0} ${f + 60} L ${z.x1} ${f + 60}`} stroke="#FFD54F" strokeWidth={14} strokeDasharray="60 40" />
    </g>;
  },

  /** TREASURE-HUNT AISLE: dim aisle, a spotlit turntable pallet in the middle (spotX) whose item changes per `goods` [[t, label, color]],
   *  "HERE TODAY" banner, a "GONE NEXT WEEK?" countdown clock (spin), sparkles, a velvet rope */
  treasureaisle: (t, z, f) => {
    const w = z.x1 - z.x0, sx = z.spotX ?? z.x0 + w * 0.5, items: [number, string, string?][] = (z.goods || [[0, 'MYSTERY']]).map((p: any) => [Number(p[0]), String(p[1]), p[2]]);
    const cur = items.filter((p) => t >= p[0]).pop() || items[0], since = t - cur[0], swap = since < 0.5 ? E.outBack(win(since, 0, 0.5)) : 1;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#2A3350" />
      {Array.from({length: Math.ceil(w / 480)}, (_, k) => { const rx = z.x0 + k * 480 + 30; return Math.abs(rx + 210 - sx) < 520 ? null : <g key={k} opacity={0.6}>{rack(rx, f - 20, k + 7, t)}</g>; })}
      {Array.from({length: 30}, (_, k) => { const u = (t * 0.2 + rnd(k)) % 1; return <circle key={'dst' + k} cx={sx - 400 + rnd(k * 3) * 800} cy={f - 900 + u * 900} r={2 + rnd(k) * 3} fill="#FFF9C4" opacity={0.6 * Math.sin(u * Math.PI)} />; })}
      <path d={`M ${sx - 90} ${f - 1100} L ${sx - 420} ${f} L ${sx + 420} ${f} L ${sx + 90} ${f - 1100} Z`} fill="#FFF59D" opacity={0.22 + 0.04 * Math.sin(t * 3)} />
      <g transform={`translate(${sx} ${f - 880}) rotate(${Math.sin(t * 1.6) * 3})`}><path d="M -360 -60 L 360 -60 L 330 0 L 360 60 L -360 60 L -330 0 Z" fill="#E53950" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <T x={0} y={18} s={fit(z.banner || 'HERE TODAY', 620, 58)} c="#FFFFFF" ls={4}>{z.banner || 'HERE TODAY'}</T></g>
      {/* turntable + pallet with the item */}
      <g transform={`translate(${sx} ${f})`}>
        <ellipse cx={0} cy={-10} rx={330} ry={46} fill="#B0BEC5" stroke={OL} strokeWidth={6} />
        {Array.from({length: 8}, (_, k) => { const an = t * 1.2 + (k / 8) * Math.PI * 2; return <circle key={k} cx={Math.cos(an) * 290} cy={-10 + Math.sin(an) * 34} r={8} fill={Math.sin(an) > 0 ? '#FFD23F' : '#8D6E63'} />; })}
        <rect x={-200} y={-80} width={400} height={50} fill="#C99A5B" stroke={OL} strokeWidth={4} />
        <g transform={`translate(0 -80) scale(${swap * Math.cos(t * 1.2) * 0.25 + 0.75 * swap + 0.0001} ${swap})`}>
          <rect x={-170} y={-300} width={340} height={300} rx={14} fill={cur[2] || '#4FB3F6'} stroke={OL} strokeWidth={6} />
          <rect x={-140} y={-270} width={280} height={80} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
          <T x={0} y={-216} s={fit(cur[1], 260, 40)}>{cur[1]}</T>
          <T x={0} y={-90} s={110} c="#FFFFFF" st={OL} sw={8}>?</T></g>
      </g>
      {/* countdown clock */}
      <g transform={`translate(${sx + 620} ${f - 560})`}><circle r={110} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
        {Array.from({length: 12}, (_, k) => <path key={k} d={`M ${Math.cos((k / 12) * Math.PI * 2) * 92} ${Math.sin((k / 12) * Math.PI * 2) * 92} L ${Math.cos((k / 12) * Math.PI * 2) * 102} ${Math.sin((k / 12) * Math.PI * 2) * 102}`} stroke={OL} strokeWidth={4} />)}
        <path d={`M 0 0 L ${Math.cos(t * 3 - 1.57) * 80} ${Math.sin(t * 3 - 1.57) * 80}`} stroke="#E53950" strokeWidth={7} strokeLinecap="round" />
        <path d={`M 0 0 L ${Math.cos(t * 0.25 - 1.57) * 54} ${Math.sin(t * 0.25 - 1.57) * 54}`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
        <rect x={-140} y={124} width={280} height={52} rx={12} fill="#FFE066" stroke={OL} strokeWidth={4} /><T x={0} y={160} s={26}>{z.clockText || 'GONE NEXT WEEK?'}</T></g>
      {[-1, 1].map((sd) => <g key={sd}><rect x={sx + sd * 470 - 10} y={f - 120} width={20} height={120} fill="#C9A227" stroke={OL} strokeWidth={3} />
        <path d={`M ${sx + sd * 470} ${f - 110} Q ${sx + sd * 560} ${f - 50} ${sx + sd * 650} ${f - 110}`} fill="none" stroke="#7B1FA2" strokeWidth={10} /></g>)}
      <rect x={z.x0} y={f} width={w} height={800} fill="#59617A" />
      <ellipse cx={sx} cy={f + 40} rx={500} ry={60} fill="#FFF59D" opacity={0.18} />
      <rect x={z.x0} y={f} width={w} height={16} fill="#4A5068" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** LOADING DOCK (exterior, day): warehouse wall with dock doors, a truck backing in (truckAt), pallets that sell out (sellAt..),
   *  a big "DAYS" strip along the top with a moving marker (dayFrom..dayTo over 0..30), a "SOLD" stamp at soldAt and the supplier's
   *  bill arriving at billAt */
  loadingdock: (t, z, f) => {
    const w = z.x1 - z.x0, dx = z.dockX ?? z.x0 + w * 0.5, ta = z.truckAt ?? 0, tu = E.out(win(t, ta, 2.2));
    const d0 = z.dayFrom ?? 0, d1 = z.dayTo ?? 1e9, day = clamp((t - d0) / Math.max(0.1, d1 - d0)) * 30, sold = z.soldAt !== undefined && t >= z.soldAt, bill = z.billAt !== undefined && t >= z.billAt;
    return <g>
      {sky(z, f, '#7CCBF2', '#E8F7FF', 'ldsky' + Math.round(z.x0))}
      <rect x={z.x0} y={f - 640} width={w} height={640} fill="#D0D6DB" stroke={OL} strokeWidth={6} />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <path key={'rib' + k} d={`M ${z.x0 + k * 80} ${f - 640} L ${z.x0 + k * 80} ${f - 260}`} stroke="#B6BEC5" strokeWidth={6} />)}
      <rect x={z.x0} y={f - 680} width={w} height={44} fill="#2F6FD1" stroke={OL} strokeWidth={5} />
      {[-1, 0, 1].map((k) => <g key={'dd' + k}><rect x={dx + k * 520 - 170} y={f - 470} width={340} height={360} fill="#37474F" stroke={OL} strokeWidth={6} />
        {Array.from({length: 7}, (_, q) => <path key={q} d={`M ${dx + k * 520 - 170} ${f - 470 + q * 40} L ${dx + k * 520 + 170} ${f - 470 + q * 40}`} stroke="#546E7A" strokeWidth={4} />)}
        <rect x={dx + k * 520 - 60} y={f - 520} width={120} height={36} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={dx + k * 520} y={f - 494} s={22}>DOCK {k + 2}</T></g>)}
      <rect x={z.x0} y={f - 110} width={w} height={110} fill="#90A4AE" stroke={OL} strokeWidth={5} />
      {/* day strip */}
      {z.dayFrom !== undefined && <g transform={`translate(${dx} ${f - 880})`}><rect x={-760} y={-50} width={1520} height={100} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {Array.from({length: 31}, (_, k) => <g key={k}><path d={`M ${-700 + k * 46.6} -10 L ${-700 + k * 46.6} ${k % 5 ? 10 : 24}`} stroke={OL} strokeWidth={3} />{k % 10 === 0 && <T x={-700 + k * 46.6} y={-18} s={22}>{`DAY ${k}`}</T>}</g>)}
        <rect x={-700} y={14} width={day * 46.6} height={18} rx={9} fill="#2E9E5B" />
        <g transform={`translate(${-700 + day * 46.6} 0)`}><path d="M 0 -60 L -18 -86 L 18 -86 Z" fill="#E53950" stroke={OL} strokeWidth={3} /></g>
        {sold && <g transform={`translate(${-700 + 26 * 46.6} 70) scale(${pop(t, z.soldAt, 0.4)}) rotate(-8)`}><rect x={-120} y={-30} width={240} height={60} rx={10} fill="#2E9E5B" stroke={OL} strokeWidth={4} /><T x={0} y={12} s={28} c="#FFFFFF">{z.soldText || 'SOLD BY ≈ DAY 26'}</T></g>}
        {bill && <g transform={`translate(${-700 + 30 * 46.6} 70) scale(${pop(t, z.billAt, 0.4)}) rotate(6)`}><rect x={-110} y={-30} width={220} height={60} rx={10} fill="#E53950" stroke={OL} strokeWidth={4} /><T x={0} y={12} s={28} c="#FFFFFF">{z.billText || 'BILL DUE'}</T></g>}
      </g>}
      {/* truck */}
      <g transform={`translate(${lerp(dx + 1700, dx + 360, tu)} ${f + 120})`}>
        <rect x={-30} y={-420} width={560} height={330} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><path d="M -30 -330 L 530 -330" stroke="#E53950" strokeWidth={22} />
        <T x={250} y={-200} s={44} c="#2F6FD1">{z.truckText || 'SUPPLIER'}</T>
        <path d="M 530 -320 L 640 -320 L 700 -240 L 700 -90 L 530 -90 Z" fill="#FFB300" stroke={OL} strokeWidth={6} strokeLinejoin="round" /><path d="M 560 -300 L 630 -300 L 670 -240 L 560 -240 Z" fill="#CFEFFF" stroke={OL} strokeWidth={4} />
        {[60, 200, 600].map((wx) => <g key={wx} transform={`translate(${wx} -70) rotate(${-tu * 720})`}><circle r={44} fill="#263238" stroke={OL} strokeWidth={5} /><circle r={16} fill="#B0BEC5" /><path d="M -36 0 L 36 0" stroke="#90A4AE" strokeWidth={5} /></g>)}
        {tu < 0.98 && t > ta && [0, 1].map((k) => { const u = (t * 2 + k / 2) % 1; return <circle key={k} cx={720 + u * 70} cy={-120 - u * 50} r={14 + u * 20} fill="#CFD8DC" stroke={OL} strokeWidth={3} opacity={1 - u} />; })}
      </g>
      {/* pallets on the apron */}
      {[-1, 0].map((k) => pallet(dx - 640 + k * 290, f - 110, 20 + k, t, 0.9, z.sellAt !== undefined ? 1 - win(t, z.sellAt + (k + 1) * 0.5, z.sellDur ?? 3) : 1))}
      <rect x={z.x0} y={f} width={w} height={800} fill="#9EA7AE" />
      <path d={`M ${z.x0} ${f + 80} L ${z.x1} ${f + 80}`} stroke="#FFD23F" strokeWidth={12} strokeDasharray="70 50" />
    </g>;
  },

  /** GAS BAR: canopy, pumps with members filling up, a queue of cars rolling in (carsAt), sign (`signText`, no prices), pharmacy and
   *  optical storefronts behind (ancillary), the warehouse wall */
  gasbar: (t, z, f) => {
    const w = z.x1 - z.x0, gx = z.gasX ?? z.x0 + w * 0.5, cars = z.cars ?? 5;
    return <g>
      {sky(z, f, '#6EC6F5', '#E6F7FF', 'gbsky' + Math.round(z.x0))}
      <rect x={z.x0} y={f - 520} width={w} height={520} fill="#CFD6DC" stroke={OL} strokeWidth={5} />
      {['PHARMACY', 'OPTICAL', 'TIRES', 'HEARING'].map((s2, k) => <g key={s2} transform={`translate(${gx - 1300 + k * 380} ${f - 440})`}><rect x={-150} y={-40} width={300} height={70} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        <T x={0} y={8} s={30} c="#2F6FD1">{s2}</T><rect x={-130} y={50} width={260} height={150} fill="#BFE9FF" stroke={OL} strokeWidth={4} /></g>)}
      <rect x={z.x0} y={f - 140} width={w} height={140} fill="#8E99A3" />
      {/* canopy */}
      <g transform={`translate(${gx} 0)`}>
        {[-460, 0, 460].map((px) => <rect key={px} x={px - 22} y={f - 560} width={44} height={560} fill="#ECEFF1" stroke={OL} strokeWidth={5} />)}
        <rect x={-640} y={f - 640} width={1280} height={100} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={7} /><path d={`M -640 ${f - 560} L 640 ${f - 560}`} stroke="#E53950" strokeWidth={22} />
        <T x={0} y={f - 574} s={44} c="#2F6FD1" ls={6}>{z.canopy || 'MEMBER FUEL'}</T>
        {[-230, 230].map((px, k) => <g key={px} transform={`translate(${px} ${f})`}><rect x={-60} y={-260} width={120} height={260} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
          <rect x={-44} y={-236} width={88} height={60} rx={6} fill="#263238" /><T x={0} y={-196} s={22} c="#7CFF8A">{Math.floor(t * 4 + k) % 2 ? 'FILL' : 'UP!'}</T>
          <path d={`M 60 -150 Q 120 -${120 - 20 * Math.sin(t * 2 + k)} 110 -60`} stroke={OL} strokeWidth={8} fill="none" /><rect x={-30} y={-150} width={60} height={60} rx={6} fill="#E53950" stroke={OL} strokeWidth={4} /></g>)}
      </g>
      {/* sign */}
      <g transform={`translate(${gx + 900} ${f})`}><rect x={-14} y={-560} width={28} height={560} fill="#90A4AE" stroke={OL} strokeWidth={4} />
        <rect x={-170} y={-640} width={340} height={140} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={-590} s={30} c="#E53950">{z.signText || 'GAS'}</T><T x={0} y={-534} s={28}>{z.signSub || 'MEMBERS ONLY'}</T></g>
      {/* car queue */}
      {Array.from({length: cars}, (_, k) => { const at = (z.carsAt ?? 0) + k * 0.5, u = E.out(win(t, at, 2.2)), tx = k === 0 ? gx + 380 : k === 1 ? gx - 80 : gx - 760 - (k - 2) * 290, cx = lerp(gx - 2300 - k * 200, tx, u);
        const c = ['#FF8A65', '#4FB3F6', '#7BD389', '#FFC93C', '#B39DDB', '#F06292'][k % 6];
        return <g key={'car' + k} transform={`translate(${cx} ${f + 10})`}>
          <path d="M -120 -24 L -120 -66 Q -100 -80 -66 -82 L -40 -120 Q 0 -132 50 -120 L 76 -82 Q 120 -78 126 -54 L 126 -24 Z" fill={c} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <path d="M -30 -112 Q 0 -122 44 -112 L 60 -86 L -48 -86 Z" fill="#CFEFFF" stroke={OL} strokeWidth={3} />
          {[-76, 80].map((wx) => <g key={wx} transform={`translate(${wx} -18) rotate(${u * 900})`}><circle r={22} fill="#263238" stroke={OL} strokeWidth={4} /><path d="M -14 0 L 14 0" stroke="#CFD8DC" strokeWidth={4} /></g>)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={800} fill="#6F7A84" />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 300} y={f + 90} width={150} height={14} fill="#FFFFFF" opacity={0.8} />)}
    </g>;
  },

  /** SEATTLE 1983: opening day of a low warehouse in the rain-washed Pacific Northwest: evergreen hills, a distant snowy volcano,
   *  drizzle, 1980s cars, an "OPENING DAY" banner (`banner`), a calendar sign 1983 */
  seattle83: (t, z, f) => {
    const w = z.x1 - z.x0, wx = z.x0 + w * (z.whX ?? 0.5);
    return <g>
      {sky(z, f, '#9FB6C8', '#E9EEF1', 's83sky' + Math.round(z.x0))}
      <path d={`M ${wx + 300} ${f - 360} L ${wx + 700} ${f - 820} L ${wx + 1100} ${f - 360} Z`} fill="#B8C7D3" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <path d={`M ${wx + 590} ${f - 690} L ${wx + 700} ${f - 820} L ${wx + 810} ${f - 690} Q ${wx + 760} ${f - 660} ${wx + 720} ${f - 700} Q ${wx + 680} ${f - 650} ${wx + 640} ${f - 700} Q ${wx + 620} ${f - 660} ${wx + 590} ${f - 690} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => { const tx = z.x0 + k * 90 + rnd(k) * 40, th = 160 + rnd(k * 3) * 120;
        return <path key={'tr' + k} d={`M ${tx} ${f - 300 - th} L ${tx - 50} ${f - 300} L ${tx + 50} ${f - 300} Z`} fill={k % 2 ? '#2E6B4A' : '#3C7D57'} stroke={OL} strokeWidth={3.5} />; })}
      <rect x={z.x0} y={f - 310} width={w} height={310} fill="#6C8C6A" />
      {/* the warehouse */}
      <g transform={`translate(${wx} ${f})`}>
        <rect x={-560} y={-360} width={1120} height={360} fill="#E3DCCF" stroke={OL} strokeWidth={6} />
        <path d="M -580 -360 L 580 -360 L 560 -400 L -560 -400 Z" fill="#A1887F" stroke={OL} strokeWidth={5} />
        {Array.from({length: 14}, (_, k) => <path key={k} d={`M ${-560 + k * 80} -360 L ${-560 + k * 80} -140`} stroke="#CBBFAE" strokeWidth={5} />)}
        <rect x={-130} y={-200} width={260} height={200} fill="#5D4037" stroke={OL} strokeWidth={5} /><path d="M 0 -200 L 0 0" stroke={OL} strokeWidth={4} />
        <g transform={`translate(0 -290) rotate(${Math.sin(t * 1.6) * 1.5})`}><path d="M -400 -50 L 400 -50 L 380 0 L 400 50 L -400 50 L -380 0 Z" fill="#FFF8E1" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <T x={0} y={16} s={fit(z.banner || 'GRAND OPENING · WAREHOUSE CLUB', 740, 40)} c="#8D3B2A">{z.banner || 'GRAND OPENING · WAREHOUSE CLUB'}</T></g>
        {[-470, 470].map((bx) => <g key={bx}>{Array.from({length: 5}, (_, k) => <circle key={k} cx={bx + Math.sin(t * 2 + k) * 6} cy={-470 - k * 34} r={20} fill={['#E57373', '#FFD54F', '#81C784', '#64B5F6', '#BA68C8'][k]} stroke={OL} strokeWidth={3} />)}
          <path d={`M ${bx} -450 L ${bx} -360`} stroke={OL} strokeWidth={3} /></g>)}
      </g>
      <rect x={z.x0} y={f} width={w} height={800} fill="#7D8A93" />
      {[0, 1, 2].map((k) => { const cx = z.x0 + 300 + k * 700 + ((t * 30) % 200); return <g key={'c83' + k} transform={`translate(${cx} ${f + 90})`}>
        <rect x={-130} y={-70} width={260} height={56} rx={6} fill={['#8D6E63', '#5C7A99', '#A1887F'][k]} stroke={OL} strokeWidth={4} />
        <path d="M -80 -70 L -60 -114 L 70 -114 L 90 -70 Z" fill={['#8D6E63', '#5C7A99', '#A1887F'][k]} stroke={OL} strokeWidth={4} /><path d="M -56 -108 L 64 -108 L 80 -74 L -70 -74 Z" fill="#D7E6EF" stroke={OL} strokeWidth={3} />
        {[-80, 80].map((q) => <circle key={q} cx={q} cy={-12} r={22} fill="#263238" stroke={OL} strokeWidth={4} />)}</g>; })}
      {Array.from({length: 60}, (_, k) => { const u = (t * 1.4 + rnd(k)) % 1, rx = z.x0 + rnd(k * 7) * w; return <path key={'rn' + k} d={`M ${rx - u * 40} ${f - 1200 + u * 1400} l -8 26`} stroke="#5C7A99" strokeWidth={3} opacity={0.5} />; })}
    </g>;
  },

  /** CASH VAULT: a round vault door that swings open at openAt, a chute pouring coins at pourAt into a crowd of faceless shareholder
   *  silhouettes (raised hands), a counter screen `screen` */
  cashvault: (t, z, f) => {
    const w = z.x1 - z.x0, vx = z.x0 + w * (z.vaultX ?? 0.4), op = z.openAt !== undefined ? E.inOut(win(t, z.openAt, 1.2)) : 0, pour = z.pourAt !== undefined && t >= z.pourAt;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E4E8EE" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'pn' + k} x={z.x0 + k * 200} y={f - 1000} width={100} height={1000} fill="#D9DEE5" />)}
      <g transform={`translate(${vx} ${f - 430})`}><circle r={330} fill="#78909C" stroke={OL} strokeWidth={8} /><circle r={280} fill="#263238" />
        {Array.from({length: 14}, (_, k) => <rect key={k} x={-120 + (k % 7) * 36} y={-40 - Math.floor(k / 7) * 80} width={30} height={70} fill="#FFC93C" stroke={OL} strokeWidth={3} />)}
        <g transform={`translate(${-280 * op} 0) scale(${1 - 0.65 * op} 1)`}><circle r={290} fill="#B0BEC5" stroke={OL} strokeWidth={8} /><circle r={220} fill="none" stroke="#90A4AE" strokeWidth={10} />
          <g transform={`rotate(${t * 40 + op * 360})`}>{[0, 1, 2, 3, 4, 5].map((k) => <path key={k} d={`M 0 0 L ${Math.cos((k / 6) * Math.PI * 2) * 120} ${Math.sin((k / 6) * Math.PI * 2) * 120}`} stroke={OL} strokeWidth={12} strokeLinecap="round" />)}<circle r={34} fill="#ECEFF1" stroke={OL} strokeWidth={5} /></g></g></g>
      {/* chute */}
      <path d={`M ${vx + 200} ${f - 420} L ${vx + 760} ${f - 200} L ${vx + 760} ${f - 140} L ${vx + 200} ${f - 360} Z`} fill="#CFD8DC" stroke={OL} strokeWidth={6} />
      {pour && Array.from({length: 14}, (_, k) => { const u = ((t - z.pourAt) * 0.9 + k / 14) % 1; const px = lerp(vx + 220, vx + 900, u), py = lerp(f - 420, f - 160, Math.min(1, u * 1.25)) + (u > 0.8 ? (u - 0.8) * 400 : 0);
        return <g key={k} transform={`translate(${px} ${py}) scale(${Math.abs(Math.cos(t * 6 + k)) * 0.6 + 0.4} 1)`}><circle r={20} fill="#FFC93C" stroke={OL} strokeWidth={4} /><T x={0} y={8} s={22} c="#7A5200">$</T></g>; })}
      {/* shareholder silhouettes */}
      {Array.from({length: 7}, (_, k) => { const sx = vx + 840 + k * 120, bob = Math.abs(Math.sin(t * 4 + k)) * (pour ? 16 : 3);
        return <g key={'sh' + k} transform={`translate(${sx} ${f - bob})`} opacity={0.92}><circle cx={0} cy={-210} r={36} fill="#3A4256" /><path d="M -46 0 L -46 -140 Q 0 -176 46 -140 L 46 0 Z" fill="#3A4256" />
          {pour && <path d={`M 40 -150 L ${70 + Math.sin(t * 8 + k) * 8} -250`} stroke="#3A4256" strokeWidth={20} strokeLinecap="round" />}</g>; })}
      {z.screen && <g transform={`translate(${vx + 1100} ${f - 720})`}><rect x={-260} y={-90} width={520} height={180} rx={16} fill="#1B2438" stroke={OL} strokeWidth={6} />
        <T x={0} y={-24} s={26} c="#80DEEA">{z.screenTop || 'SPECIAL DIVIDEND'}</T><T x={0} y={46} s={fit(z.screen, 480, 60)} c="#FFC93C">{z.screen}</T></g>}
      <rect x={z.x0} y={f} width={w} height={800} fill="#B9C0C9" />
      <rect x={z.x0} y={f} width={w} height={16} fill="#A3ABB5" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** SHOW TITLE CARD (static camera): a giant member card flies in and flips; the show title stamps on; typed joke subtitle (subs) */
  clubtitle: (t, z, f) => {
    const cx = 960, cy = 480, title: string = z.title || 'THE CLUB', sub: string = z.sub || 'MEMBERS ONLY';
    const subs: [number, string][] = (z.subs || []).map((p: any) => [Number(p[0]), String(p[1])]);
    const cur = subs.filter((p) => t >= p[0]).pop();
    const typed = cur ? cur[1].slice(0, Math.floor((t - cur[0]) * 32)) : '';
    const fly = E.outBack(win(t, 0.1, 0.8)), flip = Math.cos(win(t, 0.9, 0.5) * Math.PI);
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#C62828" />
      <g transform={`translate(${cx} ${cy}) rotate(${-t * 10})`}>{Array.from({length: 20}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos((k / 20) * Math.PI * 2) * 2400} ${Math.sin((k / 20) * Math.PI * 2) * 2400} L ${Math.cos(((k + 0.5) / 20) * Math.PI * 2) * 2400} ${Math.sin(((k + 0.5) / 20) * Math.PI * 2) * 2400} Z`} fill={k % 2 ? '#E53950' : '#2F6FD1'} />)}</g>
      {Array.from({length: 16}, (_, k) => { const u = (t * 0.5 + rnd(k)) % 1; return <rect key={'cf' + k} x={rnd(k * 3) * 1920} y={-60 + u * 1200} width={70} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={0.5} transform={`rotate(${u * 360 + k * 20} ${rnd(k * 3) * 1920 + 35} ${-38 + u * 1200})`} />; })}
      <g transform={`translate(${cx} ${lerp(-700, cy, fly)}) rotate(${(1 - fly) * -30 + Math.sin(t * 2) * 2}) scale(${Math.max(0.05, Math.abs(flip))} 1)`}>
        <rect x={-640} y={-330} width={1280} height={660} rx={60} fill="#FFFFFF" stroke={OL} strokeWidth={14} />
        <rect x={-640} y={-330} width={1280} height={150} rx={60} fill="#2F6FD1" stroke={OL} strokeWidth={14} /><rect x={-626} y={-250} width={1252} height={70} fill="#2F6FD1" />
        <g transform="translate(0 -236) scale(1)"><rect x={-360} y={-40} width={720} height={64} rx={32} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={6} s={28} ls={3}>{z.kicker || 'THE HIDDEN ECONOMICS PRESENTS'}</T></g>
        {flip < 0.3 && title.split(' ').map((word, wi, arr) => <g key={wi} transform={`translate(0 ${-30 + wi * 150 - (arr.length - 1) * 40})`}>{word.split('').map((ch, k) => {
          const st = 1.3 + wi * 0.3 + k * 0.05, u = E.outBack(win(t, st, 0.45)), cw = 104, xx = (k - (word.length - 1) / 2) * cw;
          return <g key={k} transform={`translate(${xx} ${(1 - u) * -260}) scale(${u})`}><T x={8} y={10} s={150} c={OL}>{ch}</T><T x={0} y={0} s={150} c={wi % 2 ? '#E53950' : '#FFD23F'} st={OL} sw={14}>{ch}</T></g>; })}</g>)}
        <g transform={`translate(0 252) scale(${pop(t, 2.0, 0.45)})`}><rect x={-420} y={-40} width={840} height={70} rx={14} fill="#FFE066" stroke={OL} strokeWidth={6} /><T x={0} y={10} s={fit(sub, 800, 40)} c="#1B2433">{sub}</T></g>
      </g>
      {cur && <g transform="translate(960 1010)"><rect x={-800} y={-40} width={1600} height={70} rx={14} fill="#0B1A3A" opacity={0.85} />
        <T x={0} y={8} s={fit(cur[1], 1540, 34)} c="#FFE066" w={800}>{typed}{Math.floor(t * 3) % 2 ? '▌' : ' '}</T></g>}
    </g>;
  },

  /** ACT BUMPER (static camera): pallet-wood stripes wipe in, a forklift crate carries the act number, title plank, joke caption, and
   *  THE RUNNING GAG: the food-court board says $1.50 and someone tries to change it (`gag`: 'ladder'|'crane'|'drone'|'sticker'|
   *  'robot'), a buzzer goes off at ~2.3 s and the attempt fails ("NOPE.") */
  clubbumper: (t, z, f) => {
    const act: string = z.act || 'ACT ONE', title: string = z.title || '', cap: string = z.caption || '', col2 = z.color || '#2F6FD1', gag: string = z.gag || 'ladder';
    const wipe = E.out(win(t, 0, 0.45)), crate = E.outBack(win(t, 0.2, 0.7)), buzz = t >= 2.3 && t < 3.0, fail = E.in(win(t, 2.4, 0.8));
    const bx = 1500, by = 330;
    // the attempt: a "NEW PRICE?" card approaches the board, then gets yanked away
    const appr = E.inOut(win(t, 0.9, 1.3));
    const cardX = gag === 'drone' ? lerp(2200, bx + 40, appr) + fail * 900 : gag === 'crane' ? bx + 40 : gag === 'robot' ? lerp(bx + 360, bx + 40, appr) + fail * 600 : bx + 40;
    const cardY = gag === 'crane' ? lerp(-200, by + 40, appr) - fail * 700 : gag === 'ladder' ? lerp(900, by + 40, appr) + fail * 900 : gag === 'sticker' ? lerp(1300, by + 40, appr) + fail * 1000 : by + 40 + (gag === 'drone' ? Math.sin(t * 6) * 10 : 0);
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#FFF6E8" />
      <g transform={`translate(${-2600 + 2600 * wipe} 0)`}>{Array.from({length: 24}, (_, k) => <rect key={k} x={k * 180 - 400} y={-200} width={150} height={1500} fill={k % 2 ? '#D9A866' : '#C99A5B'} opacity={0.9} />)}
        {Array.from({length: 24}, (_, k) => <path key={'g' + k} d={`M ${k * 180 - 390} 0 Q ${k * 180 - 330} 540 ${k * 180 - 380} 1080`} stroke="#A9783F" strokeWidth={4} fill="none" opacity={0.6} />)}</g>
      {/* forklift + crate with the act number */}
      <g transform={`translate(${lerp(-500, 470, crate)} 760)`}>
        <rect x={-200} y={-90} width={260} height={90} rx={10} fill="#FFB300" stroke={OL} strokeWidth={7} /><rect x={-170} y={-200} width={150} height={110} fill="none" stroke="#37474F" strokeWidth={12} />
        {[-150, 20].map((wx) => <circle key={wx} cx={wx} cy={10} r={34} fill="#263238" stroke={OL} strokeWidth={5} />)}
        <rect x={60} y={-380} width={18} height={380} fill="#546E7A" stroke={OL} strokeWidth={4} /><path d="M 78 -30 L 260 -30" stroke="#37474F" strokeWidth={14} />
        <g transform={`translate(170 -200) rotate(${Math.sin(t * 3) * 2})`}><rect x={-130} y={-160} width={260} height={160} rx={10} fill="#D7A86E" stroke={OL} strokeWidth={8} />
          <path d="M -130 -110 L 130 -110" stroke="#A9783F" strokeWidth={6} /><T x={0} y={-118} s={28} c={col2} ls={3}>ACT</T><T x={0} y={-14} s={100}>{z.num || '1'}</T></g></g>
      <g transform={`translate(780 300) scale(${pop(t, 0.45, 0.45)}) rotate(-2)`}><rect x={-520} y={-100} width={1040} height={150} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={9} />
        <T x={0} y={22} s={fit(title, 960, 70)} c={OL}>{title}</T><T x={0} y={-62} s={26} c={col2} ls={6}>{act}</T></g>
      {cap && <g transform={`translate(780 480) scale(${pop(t, 0.9, 0.4)}) rotate(${Math.sin(t * 2.4) * 1.5})`}><rect x={-480} y={-38} width={960} height={64} rx={32} fill="#1B2433" />
        <T x={0} y={8} s={fit(cap, 900, 30)} c="#FFE066" w={800}>{cap}</T></g>}
      {/* the price board (running gag) */}
      <g transform={`translate(${bx} ${by}) rotate(${buzz ? Math.sin(t * 60) * 3 : 0})`}>
        <rect x={-230} y={-150} width={460} height={300} rx={20} fill="#1B2433" stroke={OL} strokeWidth={8} /><T x={0} y={-96} s={30} c="#FFE066" ls={4}>HOT DOG + SODA</T>
        <rect x={-200} y={-70} width={400} height={190} rx={14} fill="#FFFDF4" stroke={OL} strokeWidth={5} /><T x={0} y={80} s={120} c="#E53950">$1.50</T>
        {buzz && <g><circle cx={0} cy={-200} r={40} fill={Math.sin(t * 40) > 0 ? '#FF5252' : '#B71C1C'} stroke={OL} strokeWidth={5} /><T x={0} y={-188} s={30} c="#FFFFFF">!</T></g>}
      </g>
      {/* the attempt */}
      {t > 0.9 && <g>
        {gag === 'ladder' && <g transform={`translate(${bx + 120} ${lerp(1200, 560, appr) + fail * 700}) rotate(${fail * 30})`}><path d="M -40 0 L -10 -380 M 40 0 L 70 -380" stroke="#8D6E63" strokeWidth={14} />{Array.from({length: 7}, (_, k) => <path key={k} d={`M ${-38 + k * 4} ${-30 - k * 50} L ${42 + k * 4} ${-30 - k * 50}`} stroke="#8D6E63" strokeWidth={10} />)}</g>}
        {gag === 'crane' && <path d={`M ${bx + 40} -400 L ${bx + 40} ${cardY - 50}`} stroke={OL} strokeWidth={6} />}
        {gag === 'drone' && <g transform={`translate(${cardX} ${cardY - 90})`}>{[-1, 1].map((sd) => <ellipse key={sd} cx={sd * 70} cy={-20} rx={50 * Math.abs(Math.cos(t * 40 + sd))} ry={8} fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}<ellipse rx={50} ry={30} fill="#FFD23F" stroke={OL} strokeWidth={5} /><circle cx={8} cy={-2} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><circle cx={10} cy={0} r={6} fill={OL} /></g>}
        {gag === 'robot' && <path d={`M ${bx + 760} 1100 L ${cardX + 160} ${cardY + 120} L ${cardX + 60} ${cardY + 30}`} stroke="#FFB300" strokeWidth={30} fill="none" strokeLinejoin="round" />}
        <g transform={`translate(${cardX} ${cardY}) rotate(${-6 + fail * 90})`}><rect x={-150} y={-60} width={300} height={120} rx={14} fill="#FFF59D" stroke={OL} strokeWidth={6} />
          <T x={0} y={-6} s={34} c="#6B7385">NEW PRICE?</T><T x={0} y={40} s={36} c="#E53950">$ ? . ??</T></g>
      </g>}
      {t > 2.5 && <g transform={`translate(${bx - 120} ${by + 300}) scale(${pop(t, 2.5, 0.35)}) rotate(-8)`}><path d="M -150 -60 L 150 -60 L 130 0 L 150 60 L -150 60 L -130 0 Z" fill="#E53950" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
        <T x={0} y={20} s={56} c="#FFFFFF">NOPE.</T></g>}
    </g>;
  },
};

export const CLUB_ITEMS: Record<string, ItemFn> = {cardie, membercard, combo, palletstack, receipt};
export const CLUB_INDOOR = ['clubfloor', 'memberdesk', 'foodcourt', 'housebrand', 'treasureaisle', 'cashvault', 'clubtitle', 'clubbumper'];
