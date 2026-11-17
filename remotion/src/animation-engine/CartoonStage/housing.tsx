import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * HOUSING kit for CartoonStage (Episode 58, "Why Americans Can No Longer Afford a Home").
 *
 * Same owner direction as Ep 56: a prime-time animated TV sitcom, at genre level only. Everything here is ORIGINAL.
 * The cast reuses the sitcom `toon` rig (sitcom.tsx) with new looks chosen in the storyboard (MAYA the first-time buyer,
 * REX her locked-in dad, DEEDEE the realtor); this file adds the episode's bespoke DAY sets and items:
 *  sets  openhouse (suburban open house with a crowd in every window), ratecoaster (an amusement-park rollercoaster whose
 *        track IS the Freddie Mac 30-year rate, drawn from supplied data on a real % / year grid), lockstreet (a cul-de-sac
 *        of padlocked homes), shrinker (the starter-home SHRINK-O-MATIC with a gauge), emptylot (a construction lot whose
 *        house frame builds on a keyframe, with tumbleweeds when idle), zoningboard (a town-hall hearing room with a dais,
 *        gavel, wall clock, protest signs and a parcel map that turns yellow), basement (the parents' basement: low pipes,
 *        swinging bulb, washer, futon, feet passing the high window), hhtitle / hhbumper reuse nothing: see below.
 *  items minihome (the running gag: a "STARTER HOME" that shrinks from bungalow to shed, doghouse, birdhouse, mailbox),
 *        placard (a hand-held protest/plea sign), paddles (a bidding war: paddles pop up with escalating offers),
 *        padlock (a giant gold padlock with a rate on it that clamps shut), savejar (a down-payment jar that fills),
 *        incomebars (two cartoon bars, needed vs. have, with a gap bracket).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx via HOUSING_SETS / HOUSING_ITEMS.
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
  if (!Array.isArray(v)) return v;
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], v[i][0] - v[i - 1][0])));
  return v[v.length - 1][1];
};
const jig = (t: number, at: number, k = 14, d = 5) => (t < at ? 0 : Math.exp(-d * (t - at)) * Math.sin(k * (t - at)));
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.62);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;
const lines = (txt: string) => String(txt).split('\n');
const vis = (a: Item, t: number) => !(t < (a.at ?? 0) || (a.until !== undefined && t > a.until + 0.4));
const outF = (a: Item, t: number) => (a.until !== undefined ? 1 - win(t, a.until, 0.35) : 1);
const HOUSE_COLS = ['#FFE0B2', '#C5E1A5', '#B3E5FC', '#F8BBD0', '#FFF59D', '#D1C4E9', '#FFCCBC'];
const ROOF_COLS = ['#C0504D', '#5D4037', '#37474F', '#7E57C2', '#2E7D32', '#E65100'];

/** a cartoon suburban house, origin at the ground centre; heads bob in the windows when `crowd` > 0 */
const house = (t: number, x: number, y: number, s: number, k: number, opt: {wall?: string; roof?: string; crowd?: number; door?: number; win?: string} = {}) => {
  const wall = opt.wall || HOUSE_COLS[k % HOUSE_COLS.length], roof = opt.roof || ROOF_COLS[k % ROOF_COLS.length], crowd = opt.crowd ?? 0;
  const winc = opt.win || '#CFEFFF';
  const heads = (wx: number, wy: number, q: number) => crowd > 0 && Array.from({length: Math.min(4, 1 + Math.floor(crowd * 3))}, (_, h) => {
    const hx = wx + 14 + h * 18 + Math.sin(t * 5 + h + q) * 6, hy = wy + 52 + Math.abs(Math.sin(t * 7 + h * 2 + q)) * -10;
    return <g key={'hd' + q + h}><circle cx={hx} cy={hy} r={12} fill={['#F6CDA6', '#B97A4B', '#E0A878', '#8A5634'][(h + q) % 4]} stroke={OL} strokeWidth={2.5} />
      <path d={`M ${hx - 12} ${hy - 4} Q ${hx} ${hy - 18} ${hx + 12} ${hy - 4}`} fill={['#3E2723', '#1B1B1B', '#F2C14E', '#C0392B'][(h * 3 + q) % 4]} stroke={OL} strokeWidth={2} /></g>; });
  return <g key={'hz' + k} transform={`translate(${x} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={6} rx={280} ry={20} fill={OL} opacity={0.15} />
    <rect x={-200} y={-280} width={400} height={280} fill={wall} stroke={OL} strokeWidth={6} />
    <path d={`M -240 -276 L 0 -450 L 240 -276 Z`} fill={roof} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    {[0, 1, 2, 3].map((r) => <path key={r} d={`M ${-200 + r * 50} ${-306 - r * 36} L ${200 - r * 50} ${-306 - r * 36}`} stroke={OL} strokeWidth={2} opacity={0.25} />)}
    <rect x={110} y={-440} width={44} height={100} fill="#8D6E63" stroke={OL} strokeWidth={5} />
    {[0, 1, 2].map((q) => { const u = (t * 0.5 + q / 3) % 1; return <circle key={'sm' + q} cx={132 + u * 40} cy={-450 - u * 120} r={14 + u * 22} fill="#ECEFF1" stroke={OL} strokeWidth={2.5} opacity={0.8 * (1 - u)} />; })}
    {[-160, 70].map((wx, q) => <g key={wx}><rect x={wx} y={-220} width={90} height={84} rx={4} fill={winc} stroke={OL} strokeWidth={5} />
      <g clipPath={undefined}>{heads(wx, -220, q)}</g>
      <path d={`M ${wx + 45} -220 L ${wx + 45} -136 M ${wx} -178 L ${wx + 90} -178`} stroke={OL} strokeWidth={3} />
      <rect x={wx - 10} y={-136} width={110} height={14} fill="#FFFFFF" stroke={OL} strokeWidth={3} /></g>)}
    <rect x={-40} y={-150} width={80} height={150} rx={6} fill="#A1662F" stroke={OL} strokeWidth={5} transform={opt.door ? `skewY(${-12 * opt.door})` : undefined} />
    <circle cx={22} cy={-72} r={6} fill="#FFC93C" stroke={OL} strokeWidth={2} />
    <rect x={-60} y={-8} width={120} height={14} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
  </g>;
};
const fence = (x0: number, x1: number, y: number, k = 0) => <g key={'fc' + k}>
  <rect x={x0} y={y - 54} width={x1 - x0} height={10} fill="#FFFFFF" stroke={OL} strokeWidth={3} />
  {Array.from({length: Math.max(0, Math.floor((x1 - x0) / 34))}, (_, q) => <path key={q} d={`M ${x0 + q * 34 + 6} ${y} L ${x0 + q * 34 + 6} ${y - 76} L ${x0 + q * 34 + 17} ${y - 90} L ${x0 + q * 34 + 28} ${y - 76} L ${x0 + q * 34 + 28} ${y} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={3} strokeLinejoin="round" />)}
</g>;
const tree = (x: number, y: number, s: number, k: number, t: number) => <g key={'tr' + k} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 1.3 + k) * 2})`}>
  <rect x={-14} y={-160} width={28} height={160} fill="#8D6E63" stroke={OL} strokeWidth={4} />
  {[[-50, -200, 70], [40, -210, 70], [0, -270, 80], [-10, -190, 60]].map(([cx, cy, r], q) => <circle key={q} cx={cx} cy={cy} r={r} fill={['#7BC67B', '#6DB56D', '#86CF86', '#5FA85F'][(q + k) % 4]} stroke={OL} strokeWidth={4} />)}
</g>;
const lawn = (z: Z, f: number) => <g>
  <rect x={z.x0} y={f} width={z.x1 - z.x0} height={900} fill="#8CCB6E" />
  <rect x={z.x0} y={f + 30} width={z.x1 - z.x0} height={46} fill="#D9D4C7" stroke={OL} strokeWidth={4} />
  {Array.from({length: Math.ceil((z.x1 - z.x0) / 120)}, (_, k) => <path key={k} d={`M ${z.x0 + k * 120} ${f + 30} L ${z.x0 + k * 120} ${f + 76}`} stroke={OL} strokeWidth={2} opacity={0.4} />)}
  <rect x={z.x0} y={f + 76} width={z.x1 - z.x0} height={900} fill="#5E6A78" />
  {Array.from({length: Math.ceil((z.x1 - z.x0) / 260)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 260} y={f + 160} width={140} height={12} rx={6} fill="#FFE082" />)}
</g>;

/* ============================================================================================ SETS */
export const HOUSING_SETS: Record<string, SetFn> = {
  /** OPEN HOUSE (day): a street of pastel homes, the hero starter home at houseX packed with heads in every window,
   *  an OPEN HOUSE sign with balloons at signX, a queue of buyers on the path. soldAt slaps SOLD across the sign;
   *  crowd 0..1 heads in windows; queue = number of people in line. */
  openhouse: (t, z, f) => {
    const hx = z.houseX ?? 1150, sx = z.signX ?? hx - 420, crowd = z.crowd ?? 1, sold = z.soldAt !== undefined ? E.outBack(win(t, z.soldAt, 0.45)) : 0;
    const q = z.queue ?? 9;
    return <g>
      {/* far street */}
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 520)}, (_, k) => { const x = z.x0 + 260 + k * 520; if (Math.abs(x - hx) < 520) return null;
        return house(t, x, f - 150, 0.55, k + 3, {}); })}
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 700)}, (_, k) => tree(z.x0 + 120 + k * 700, f - 140, 0.6, k, t))}
      <rect x={z.x0} y={f - 150} width={z.x1 - z.x0} height={160} fill="#9CD47E" />
      {lawn(z, f)}
      {fence(z.x0, hx - 560, f, 1)}{fence(hx + 330, z.x1, f, 2)}
      {house(t, hx, f, 1.15, 0, {wall: '#FFE0B2', roof: '#D84315', crowd, door: 0.5 + 0.5 * Math.sin(t * 2.2)})}
      <rect x={hx - 40} y={f} width={80} height={30} fill="#D9D4C7" stroke={OL} strokeWidth={3} />
      {/* queue up the path */}
      {Array.from({length: q}, (_, k) => { const px = hx - 120 - k * 70, bob = Math.abs(Math.sin(t * 3 + k)) * 6, c = ['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB', '#FFC93C', '#F06292'][k % 6];
        return <g key={'qp' + k} transform={`translate(${px} ${f + 40 - bob}) scale(0.62)`}><path d="M -26 0 L -24 -90 Q 0 -110 24 -90 L 26 0 Z" fill={c} stroke={OL} strokeWidth={5} />
          <circle cx={0} cy={-130} r={30} fill={['#F6CDA6', '#B97A4B', '#E0A878', '#8A5634', '#F3D7BD'][k % 5]} stroke={OL} strokeWidth={5} />
          <circle cx={8} cy={-134} r={4} fill={OL} /><path d="M -6 -114 Q 6 -108 16 -116" stroke={OL} strokeWidth={4} fill="none" /></g>; })}
      {/* OPEN HOUSE sign */}
      <g transform={`translate(${sx} ${f + 10}) rotate(${Math.sin(t * 2) * 2})`}>
        {[[-80, '#E53950'], [-30, '#FFC93C'], [30, '#4FB3F6']].map(([dx, c], k) => <g key={k}><path d={`M 0 -190 Q ${Number(dx) * 0.6} -280 ${Number(dx) + Math.sin(t * 2 + k) * 10} -330`} stroke={OL} strokeWidth={2} fill="none" />
          <ellipse cx={Number(dx) + Math.sin(t * 2 + k) * 10} cy={-360} rx={30} ry={36} fill={String(c)} stroke={OL} strokeWidth={4} /></g>)}
        <rect x={-8} y={-200} width={16} height={200} fill="#8D6E63" stroke={OL} strokeWidth={3} />
        <rect x={-150} y={-230} width={300} height={110} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <rect x={-150} y={-230} width={300} height={36} rx={12} fill="#2F6FD1" stroke={OL} strokeWidth={6} />
        <T x={0} y={-203} s={22} c="#FFFFFF" ls={3}>WELCOME</T>
        <T x={0} y={-142} s={fit(z.signText || 'OPEN HOUSE', 270, 44)}>{z.signText || 'OPEN HOUSE'}</T>
        {sold > 0 && <g transform={`rotate(-14 0 -170) scale(${sold})`}><rect x={-140} y={-210} width={280} height={74} rx={10} fill="#E53950" stroke={OL} strokeWidth={5} />
          <T x={0} y={-157} s={50} c="#FFFFFF">{z.soldText || 'SOLD!'}</T></g>}
      </g>
      {/* mailbox */}
      <g transform={`translate(${hx + 420} ${f + 10})`}><rect x={-6} y={-110} width={12} height={110} fill="#8D6E63" stroke={OL} strokeWidth={3} />
        <path d="M -40 -110 L -40 -150 Q 0 -180 40 -150 L 40 -110 Z" fill="#2F6FD1" stroke={OL} strokeWidth={4} />
        <path d={`M 36 -150 L 36 ${-190 + 30 * Math.abs(Math.sin(t * 1.5))}`} stroke="#E53950" strokeWidth={6} /></g>
    </g>;
  },

  /** RATE COASTER: amusement park whose rollercoaster track follows supplied data pts [[year, rate%], ...] on a real grid
   *  (yearX0..yearX1 mapped to gx0..gx1; rate r -> f - base - (r - rmin) * ys). car: progress 0..1 keyframes along the track,
   *  riders' faces react to the slope. hl: [[t, year]] pops a highlight flag on the track. */
  ratecoaster: (t, z, f) => {
    const pts: [number, number][] = (z.pts || [[2019, 4.5], [2021, 2.65], [2022.8, 7.08], [2026.8, 7.11]]).map((p: any) => [Number(p[0]), Number(p[1])]);
    const Y0 = z.y0 ?? 2019, Y1 = z.y1 ?? 2027, gx0 = z.gx0 ?? 200, gx1 = z.gx1 ?? 2600, rmin = z.rmin ?? 2, ys = z.ys ?? 88, base = z.base ?? 70;
    const P = pts.map(([yr, r]) => [gx0 + ((yr - Y0) / (Y1 - Y0)) * (gx1 - gx0), f - base - (r - rmin) * ys]);
    const seg: number[] = [0]; for (let k = 1; k < P.length; k++) seg.push(seg[k - 1] + Math.hypot(P[k][0] - P[k - 1][0], P[k][1] - P[k - 1][1]));
    const L = seg[seg.length - 1];
    const at = (u: number) => { const d = clamp(u) * L; let k = 1; while (k < P.length - 1 && seg[k] < d) k++;
      const v = (d - seg[k - 1]) / Math.max(1, seg[k] - seg[k - 1]); return [lerp(P[k - 1][0], P[k][0], v), lerp(P[k - 1][1], P[k][1], v), Math.atan2(P[k][1] - P[k - 1][1], P[k][0] - P[k - 1][0])]; };
    const u = kf(z.car, t, 0), [cx, cy, ang] = at(u), shown = clamp(kf(z.reveal, t, 1));
    const nShow = Math.max(2, Math.ceil(shown * P.length));
    const d = P.slice(0, nShow).map((p, k) => `${k ? 'L' : 'M'} ${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' ');
    const climbing = Math.sin(ang) < -0.15, diving = Math.sin(ang) > 0.15;
    return <g>
      {/* park background: ferris wheel + tents */}
      <g transform={`translate(${z.wheelX ?? gx1 + 450} ${f - 360})`}>
        <path d="M -120 360 L 0 0 L 120 360" stroke="#90A4AE" strokeWidth={14} fill="none" />
        <g transform={`rotate(${t * 12})`}><circle r={300} fill="none" stroke="#B0BEC5" strokeWidth={10} />
          {Array.from({length: 10}, (_, k) => { const a2 = (k / 10) * Math.PI * 2; return <g key={k}><path d={`M 0 0 L ${Math.cos(a2) * 300} ${Math.sin(a2) * 300}`} stroke="#CFD8DC" strokeWidth={5} />
            <g transform={`translate(${Math.cos(a2) * 300} ${Math.sin(a2) * 300}) rotate(${-t * 12})`}><rect x={-34} y={0} width={68} height={50} rx={10} fill={['#E53950', '#FFC93C', '#4FB3F6', '#7BD389'][k % 4]} stroke={OL} strokeWidth={4} /></g></g>; })}</g>
        <circle r={30} fill="#FFC93C" stroke={OL} strokeWidth={5} /><T x={0} y={11} s={30}>%</T></g>
      {[gx0 - 500, gx1 + 1000].map((tx, k) => <g key={'tent' + k} transform={`translate(${tx} ${f})`}><path d="M -160 0 L -160 -140 L 0 -260 L 160 -140 L 160 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        {[-120, -40, 40, 120].map((sx) => <path key={sx} d={`M ${sx - 20} -152 L 0 -260 L ${sx + 20} -152 Z`} fill="#E53950" opacity={0.85} />)}
        <path d="M 0 -260 L 0 -320" stroke={OL} strokeWidth={4} /><path d={`M 0 -320 L ${40 + 6 * Math.sin(t * 6)} -305 L 0 -290 Z`} fill="#FFC93C" stroke={OL} strokeWidth={3} /></g>)}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={900} fill="#A5D88A" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={30} fill="#D9C9A8" stroke={OL} strokeWidth={3} />
      {/* the data grid */}
      {Array.from({length: 7}, (_, k) => { const r = rmin + 1 + k, y = f - base - (r - rmin) * ys; return <g key={'gr' + k}>
        <path d={`M ${gx0 - 40} ${y} L ${gx1 + 40} ${y}`} stroke={OL} strokeWidth={2} strokeDasharray="8 14" opacity={0.25} />
        <g transform={`translate(${gx0 - 110} ${y})`}><rect x={-46} y={-24} width={92} height={44} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><T x={0} y={10} s={26}>{r}%</T></g></g>; })}
      {Array.from({length: Math.floor(Y1 - Y0) + 1}, (_, k) => { const yr = Y0 + k, x = gx0 + (k / (Y1 - Y0)) * (gx1 - gx0); return <g key={'yr' + k} transform={`translate(${x} ${f + 70})`}>
        <rect x={-52} y={-26} width={104} height={44} rx={8} fill="#2F6FD1" stroke={OL} strokeWidth={3.5} /><T x={0} y={8} s={26} c="#FFFFFF">{yr}</T></g>; })}
      {/* supports */}
      {P.slice(0, nShow).map((p, k) => k % 5 === 0 && <g key={'sp' + k}><path d={`M ${p[0]} ${p[1] + 12} L ${p[0] - 18} ${f} M ${p[0]} ${p[1] + 12} L ${p[0] + 18} ${f}`} stroke="#C62828" strokeWidth={6} opacity={0.75} />
        <path d={`M ${p[0] - 14} ${(p[1] + f) / 2} L ${p[0] + 14} ${(p[1] + f) / 2 + 30}`} stroke="#C62828" strokeWidth={4} opacity={0.6} /></g>)}
      {/* track: double rail with ties */}
      <path d={d} fill="none" stroke={OL} strokeWidth={22} strokeLinejoin="round" strokeLinecap="round" />
      <path d={d} fill="none" stroke="#FFC93C" strokeWidth={14} strokeLinejoin="round" strokeLinecap="round" />
      <path d={d} fill="none" stroke={OL} strokeWidth={3} strokeDasharray="4 18" strokeLinejoin="round" />
      {/* the car */}
      <g transform={`translate(${cx} ${cy}) rotate(${(ang * 180) / Math.PI})`}>
        <g transform="translate(0 -14)">
          {[-46, 0, 46].map((rx, k) => { const arms = diving ? 1 : 0, sk = ['#F6CDA6', '#B97A4B', '#E0A878'][k], hr = ['#1B1B1B', '#B0BEC5', '#F2C14E'][k];
            return <g key={'rd' + k} transform={`translate(${rx} ${-40 + Math.sin(t * 20 + k) * 2})`}>
              {arms > 0 && <path d={`M -14 10 L -26 ${-40 - 6 * Math.sin(t * 14 + k)} M 14 10 L 26 ${-40 - 6 * Math.sin(t * 14 + k + 1)}`} stroke={OL} strokeWidth={8} strokeLinecap="round" />}
              <circle r={22} fill={sk} stroke={OL} strokeWidth={4} /><path d="M -22 -6 Q 0 -32 22 -6" fill={hr} stroke={OL} strokeWidth={3} />
              {climbing ? <g><circle cx={-7} cy={2} r={3} fill={OL} /><circle cx={9} cy={2} r={3} fill={OL} /><path d="M -6 13 Q 2 9 10 13" stroke={OL} strokeWidth={3} fill="none" /></g>
                : diving ? <g><circle cx={-7} cy={0} r={6} fill="#FFFFFF" stroke={OL} strokeWidth={2} /><circle cx={9} cy={0} r={6} fill="#FFFFFF" stroke={OL} strokeWidth={2} /><ellipse cx={2} cy={14} rx={6} ry={8} fill="#6B2E2A" stroke={OL} strokeWidth={2} /></g>
                : <g><circle cx={-7} cy={1} r={3.5} fill={OL} /><circle cx={9} cy={1} r={3.5} fill={OL} /><path d="M -8 11 Q 2 18 12 11" stroke={OL} strokeWidth={3} fill="none" /></g>}</g>; })}
          <path d="M -90 -30 L 90 -30 L 80 10 L -84 10 Z" fill="#E53950" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <T x={0} y={-4} s={20} c="#FFFFFF">{z.carText || 'RATE RIDE'}</T>
          {[-60, 60].map((wx) => <circle key={wx} cx={wx} cy={14} r={10} fill="#37474F" stroke={OL} strokeWidth={3} />)}
        </g>
        {diving && [0, 1, 2].map((k) => <path key={'sl' + k} d={`M ${-110 - k * 30} ${-40 + k * 18} L ${-170 - k * 40} ${-40 + k * 18}`} stroke={OL} strokeWidth={4} opacity={0.5} strokeLinecap="round" />)}
      </g>
      {/* highlight flags */}
      {(z.hl || []).map((h: any, k: number) => { const [ht, yr, lab] = [Number(h[0]), Number(h[1]), String(h[2] ?? '')]; if (t < ht) return null;
        let best = P[0]; for (const p of P) if (Math.abs(p[0] - (gx0 + ((yr - Y0) / (Y1 - Y0)) * (gx1 - gx0))) < Math.abs(best[0] - (gx0 + ((yr - Y0) / (Y1 - Y0)) * (gx1 - gx0)))) best = p;
        const s = pop(t, ht, 0.5), up = best[1] < f - 400;
        return <g key={'hl' + k} transform={`translate(${best[0]} ${best[1]}) scale(${s})`}>
          <path d={`M 0 0 L 0 ${up ? 90 : -90}`} stroke={OL} strokeWidth={4} />
          <g transform={`translate(0 ${up ? 120 : -130})`}><rect x={-fit(lab, 260, 34) * lab.length * 0.33 - 24} y={-30} width={fit(lab, 260, 34) * lab.length * 0.66 + 48} height={56} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
            <T x={0} y={10} s={fit(lab, 260, 34)} c="#C62828">{lab}</T></g>
          <circle r={14} fill="#FFFFFF" stroke="#C62828" strokeWidth={6} /></g>; })}
      {/* ticket booth */}
      <g transform={`translate(${z.boothX ?? gx0 - 340} ${f})`}><rect x={-90} y={-200} width={180} height={200} fill="#FFF3E0" stroke={OL} strokeWidth={5} />
        <path d="M -110 -200 L 0 -270 L 110 -200 Z" fill="#E53950" stroke={OL} strokeWidth={5} /><rect x={-60} y={-160} width={120} height={70} rx={6} fill="#CFEFFF" stroke={OL} strokeWidth={4} />
        <T x={0} y={-30} s={22}>{z.boothText || 'THE 30-YR'}</T></g>
    </g>;
  },

  /** LOCK STREET: a cul-de-sac of homes, each with a giant gold padlock + chain on the door (locks: list of labels, lockAt
   *  times stagger the clamps); porch rocking chairs; a big empty FOR SALE post with nothing on it. */
  lockstreet: (t, z, f) => {
    const labels: string[] = z.locks || ['2.9%', '3.1%', '2.8%', '3.4%', '3.0%'], gap = z.gap ?? 620, x0 = z.firstX ?? 300, la = z.lockAt ?? 0.5;
    return <g>
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 800)}, (_, k) => tree(z.x0 + 340 + k * 800, f - 120, 0.55, k + 4, t))}
      <rect x={z.x0} y={f - 120} width={z.x1 - z.x0} height={130} fill="#9CD47E" />
      {lawn(z, f)}
      {labels.map((lb, k) => { const hx = x0 + k * gap, s = pop(t, la + k * 0.35, 0.5), sh = jig(t, la + k * 0.35 + 0.3, 30, 6);
        return <g key={'lh' + k}>
          {house(t, hx, f, 0.85, k + 1, {})}
          <path d={`M ${hx - 110} ${f - 140} Q ${hx} ${f - 60 + 10 * Math.sin(t * 3 + k)} ${hx + 110} ${f - 140}`} stroke="#9E9E9E" strokeWidth={10} strokeDasharray="14 6" fill="none" opacity={s > 0 ? 1 : 0} />
          <g transform={`translate(${hx + sh * 8} ${f - 120}) scale(${s * 0.95}) rotate(${sh * 10})`}>
            <path d="M -40 -30 L -40 -72 Q 0 -122 40 -72 L 40 -30" fill="none" stroke="#78909C" strokeWidth={16} strokeLinecap="round" />
            <rect x={-62} y={-36} width={124} height={100} rx={16} fill="#FFC93C" stroke={OL} strokeWidth={6} />
            <circle cx={0} cy={0} r={10} fill={OL} /><path d="M 0 4 L 0 28" stroke={OL} strokeWidth={8} />
            <T x={0} y={56} s={fit(lb, 110, 26)}>{lb}</T></g>
        </g>; })}
      <g transform={`translate(${x0 + labels.length * gap - 200} ${f + 10})`}><rect x={-8} y={-210} width={16} height={210} fill="#8D6E63" stroke={OL} strokeWidth={3} />
        <path d="M 0 -200 L 130 -200" stroke="#8D6E63" strokeWidth={12} /><path d="M 30 -194 L 30 -170 M 110 -194 L 110 -170" stroke={OL} strokeWidth={3} />
        <rect x={10} y={-172} width={120} height={70} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={4} strokeDasharray="10 8" />
        <T x={70} y={-128} s={18} c="#9E9E9E">{z.emptyText || 'FOR SALE?'}</T></g>
    </g>;
  },

  /** SHRINK-O-MATIC: a riveted machine with dials and a ray dish that zaps (zaps: [t...]) a starter home on a turntable;
   *  size: keyframes for the house scale; gauge: keyframes 0..1 for the needle, gaugeText [[t, text]] under the gauge. */
  shrinker: (t, z, f) => {
    const mx = z.machX ?? 700, hx = z.houseX ?? 1500, size = kf(z.size, t, 1), g = kf(z.gauge, t, 0.5);
    const gtxt = ((z.gaugeText || []) as any[]).filter((p) => t >= Number(p[0])).pop();
    const zap = ((z.zaps || []) as number[]).some((zt) => t >= zt && t < zt + 0.6);
    const zk = ((z.zaps || []) as number[]).filter((zt) => t >= zt).pop();
    const shake = zk !== undefined ? jig(t, zk, 40, 5) * 10 : 0;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#EAF4FB" />
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 160)}, (_, k) => <path key={'pn' + k} d={`M ${z.x0 + k * 160} ${f - 900} L ${z.x0 + k * 160} ${f}`} stroke="#C9DCEB" strokeWidth={4} />)}
      <rect x={z.x0} y={f - 140} width={z.x1 - z.x0} height={20} fill="#B0C4D4" stroke={OL} strokeWidth={3} />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={900} fill="#90A4AE" />
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 120)}, (_, k) => <rect key={'fl' + k} x={z.x0 + k * 120} y={f} width={60} height={900} fill="#FFFFFF" opacity={0.07} />)}
      {/* machine */}
      <g transform={`translate(${mx + shake} ${f})`}>
        <rect x={-260} y={-520} width={420} height={520} rx={24} fill="#7E57C2" stroke={OL} strokeWidth={7} />
        {Array.from({length: 8}, (_, k) => <circle key={'rv' + k} cx={-240 + k * 54} cy={-500} r={6} fill="#B39DDB" stroke={OL} strokeWidth={2} />)}
        <rect x={-230} y={-480} width={360} height={70} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={-50} y={-433} s={36} c="#7E57C2">SHRINK-O-MATIC</T>
        {/* gauge */}
        <g transform="translate(-60 -250)"><circle r={120} fill="#FFFDE7" stroke={OL} strokeWidth={6} />
          <path d="M -100 0 A 100 100 0 0 1 100 0" fill="none" stroke="#E53950" strokeWidth={16} /><path d="M -100 0 A 100 100 0 0 1 -30 -95" fill="none" stroke="#7BD389" strokeWidth={16} />
          <g transform={`rotate(${-90 + g * 180 + Math.sin(t * 30) * 1.5})`}><path d="M -6 0 L 0 -96 L 6 0 Z" fill={OL} /></g><circle r={12} fill={OL} />
          <T x={0} y={48} s={fit(z.gaugeLabel || 'AFFORDABLE LISTINGS', 190, 20)}>{z.gaugeLabel || 'AFFORDABLE LISTINGS'}</T>
          {gtxt && <T x={0} y={90} s={40} c="#C62828">{String(gtxt[1])}</T>}</g>
        {[[-200, -80, '#E53950'], [-140, -80, '#FFC93C'], [-80, -80, '#4FB3F6'], [20, -80, '#7BD389']].map(([bx, by, c], k) => <circle key={'bt' + k} cx={Number(bx)} cy={Number(by)} r={20} fill={String(c)} stroke={OL} strokeWidth={4} opacity={Math.sin(t * 6 + k) > 0 ? 1 : 0.55} />)}
        {/* ray dish */}
        <g transform={`translate(160 -380) rotate(${-6 + Math.sin(t * 2) * 3})`}>
          <rect x={0} y={-30} width={120} height={60} rx={10} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
          <path d="M 120 -70 Q 190 0 120 70 Z" fill="#CFD8DC" stroke={OL} strokeWidth={5} /><circle cx={170} cy={0} r={14} fill={zap ? '#FFF176' : '#81D4FA'} stroke={OL} strokeWidth={4} /></g>
        {/* pipes and steam */}
        <path d="M -260 -200 Q -330 -200 -330 -320 L -330 -560" fill="none" stroke="#90A4AE" strokeWidth={26} /><path d="M -260 -200 Q -330 -200 -330 -320 L -330 -560" fill="none" stroke={OL} strokeWidth={3} />
        {[0, 1, 2].map((k) => { const u = (t * 0.9 + k / 3) % 1; return <circle key={'st' + k} cx={-330 + Math.sin(u * 6) * 20} cy={-580 - u * 200} r={20 + u * 30} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={0.85 * (1 - u)} />; })}
      </g>
      {/* beam */}
      {zap && <g opacity={0.6 + 0.4 * Math.sin(t * 60)}>
        <path d={`M ${mx + 330} ${f - 380} L ${hx - 40} ${f - 300 * size - 60} L ${hx - 40} ${f - 20} Z`} fill="#FFF59D" opacity={0.7} />
        {[0, 1, 2, 3].map((k) => <path key={'zz' + k} d={`M ${mx + 330} ${f - 380} ${Array.from({length: 6}, (_, q) => `L ${lerp(mx + 330, hx - 40, (q + 1) / 6)} ${f - 380 + lerp(0, 220 - 40 * k, (q + 1) / 6) + (rnd(q + k * 7 + Math.floor(t * 20)) - 0.5) * 60}`).join(' ')}`} stroke="#FFEB3B" strokeWidth={6} fill="none" />)}</g>}
      {/* turntable + house */}
      <g transform={`translate(${hx} ${f})`}>
        <ellipse cx={0} cy={0} rx={300} ry={40} fill="#CFD8DC" stroke={OL} strokeWidth={5} />
        {Array.from({length: 8}, (_, k) => { const a2 = t * 1.2 + (k / 8) * Math.PI * 2; return <circle key={'tt' + k} cx={Math.cos(a2) * 260} cy={Math.sin(a2) * 30} r={6} fill="#90A4AE" />; })}
        <g transform={`scale(${size * (1 + 0.08 * (zk !== undefined ? jig(t, zk, 25, 6) : 0))} ${size})`}>{house(t, 0, -6, 0.9, 0, {wall: '#FFE0B2', roof: '#D84315'})}</g>
        <g transform="translate(0 70)"><rect x={-150} y={-24} width={300} height={48} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={10} s={26}>{z.houseLabel || 'STARTER HOME'}</T></g>
      </g>
    </g>;
  },

  /** EMPTY LOT: a fenced construction lot. build: keyframes 0..1 (0 = bare dirt, 0.25 slab, 0.55 studs, 0.8 trusses, 1 sheathed);
   *  crane swings; mixer drum turns while building; tumble: true rolls tumbleweeds (idle years); sign text. */
  emptylot: (t, z, f) => {
    const b = clamp(kf(z.build, t, 0)), lx = z.lotX ?? 1200, busy = b > 0.02 && b < 0.99 && !z.tumble;
    return <g>
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 640)}, (_, k) => { const x = z.x0 + 320 + k * 640; if (Math.abs(x - lx) < 700) return null; return house(t, x, f - 110, 0.5, k + 2, {}); })}
      <rect x={z.x0} y={f - 110} width={z.x1 - z.x0} height={120} fill="#9CD47E" />
      {lawn(z, f)}
      <rect x={lx - 520} y={f - 10} width={1040} height={40} fill="#B08968" stroke={OL} strokeWidth={4} />
      {[0, 1, 2, 3, 4, 5].map((k) => <ellipse key={'dt' + k} cx={lx - 400 + k * 160} cy={f + 6} rx={50} ry={10} fill="#8D6E63" opacity={0.4} />)}
      {/* crane */}
      <g transform={`translate(${lx + 620} ${f})`}><path d="M -30 0 L -10 -620 L 10 -620 L 30 0" fill="none" stroke="#FFB300" strokeWidth={12} />
        {Array.from({length: 10}, (_, k) => <path key={k} d={`M -26 ${-k * 60} L 22 ${-k * 60 - 60}`} stroke="#FFB300" strokeWidth={5} />)}
        <g transform={`translate(0 -620) rotate(${busy ? Math.sin(t * 0.8) * 8 : 0})`}><rect x={-560} y={-20} width={760} height={30} fill="#FFB300" stroke={OL} strokeWidth={4} />
          <path d={`M -420 10 L -420 ${200 + (busy ? 40 * Math.sin(t * 1.2) : 0)}`} stroke={OL} strokeWidth={3} />
          <rect x={-470} y={190 + (busy ? 40 * Math.sin(t * 1.2) : 0)} width={100} height={40} fill="#A1662F" stroke={OL} strokeWidth={3} /></g></g>
      {/* the house being built */}
      <g transform={`translate(${lx} ${f - 10})`}>
        {b > 0.05 && <rect x={-260 * Math.min(1, b / 0.25)} y={-24} width={520 * Math.min(1, b / 0.25)} height={24} fill="#BDBDBD" stroke={OL} strokeWidth={4} />}
        {b > 0.25 && Array.from({length: 9}, (_, k) => { const v = clamp((b - 0.25) / 0.3 * 9 - k); return v > 0 && <rect key={'sd' + k} x={-250 + k * 61} y={-24 - 300 * v} width={14} height={300 * v} fill="#E0B57A" stroke={OL} strokeWidth={2.5} />; })}
        {b > 0.5 && <rect x={-256} y={-330} width={512 * clamp((b - 0.5) / 0.08)} height={14} fill="#E0B57A" stroke={OL} strokeWidth={2.5} />}
        {b > 0.55 && Array.from({length: 5}, (_, k) => { const v = clamp((b - 0.55) / 0.25 * 5 - k); return v > 0 && <path key={'ts' + k} d={`M ${-260 + k * 10} -330 L 0 ${-330 - 170 * v} L ${260 - k * 10} -330`} fill="none" stroke="#E0B57A" strokeWidth={10} strokeLinejoin="round" opacity={0.9} />; })}
        {b > 0.8 && <g opacity={clamp((b - 0.8) / 0.2)}><rect x={-256} y={-330} width={512} height={306} fill="#FFE0B2" stroke={OL} strokeWidth={5} /><path d="M -290 -326 L 0 -500 L 290 -326 Z" fill="#D84315" stroke={OL} strokeWidth={5} />
          <rect x={-40} y={-174} width={80} height={150} fill="#A1662F" stroke={OL} strokeWidth={4} />{[-190, 110].map((wx) => <rect key={wx} x={wx} y={-260} width={80} height={70} fill="#CFEFFF" stroke={OL} strokeWidth={4} />)}</g>}
      </g>
      {/* mixer */}
      <g transform={`translate(${lx - 700} ${f})`}><rect x={-120} y={-110} width={240} height={80} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <g transform={`translate(-10 -160) rotate(${busy ? t * 90 : 0})`}><ellipse rx={90} ry={60} fill="#E53950" stroke={OL} strokeWidth={5} /><path d="M -80 -20 Q 0 20 80 -20 M -80 20 Q 0 -20 80 20" stroke="#FFFFFF" strokeWidth={6} fill="none" /></g>
        {[-80, 80].map((wx) => <circle key={wx} cx={wx} cy={-18} r={24} fill="#37474F" stroke={OL} strokeWidth={4} />)}</g>
      {/* cones and the sign */}
      {[lx - 470, lx + 450].map((cx, k) => <path key={'cn' + k} d={`M ${cx - 24} ${f + 8} L ${cx} ${f - 60} L ${cx + 24} ${f + 8} Z`} fill="#FF7043" stroke={OL} strokeWidth={4} />)}
      <g transform={`translate(${lx - 380} ${f + 10}) rotate(${z.tumble ? -8 + Math.sin(t * 2) * 2 : 0})`}><rect x={-8} y={-220} width={16} height={220} fill="#8D6E63" stroke={OL} strokeWidth={3} />
        <rect x={-150} y={-260} width={300} height={100} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={-198} s={fit(z.sign || 'COMING SOON', 270, 40)}>{z.sign || 'COMING SOON'}</T></g>
      {z.tumble && [0, 1].map((k) => { const span = z.x1 - z.x0, x = z.x0 + ((t * 260 + k * span / 2) % span), r = 40 + k * 10;
        return <g key={'tw' + k} transform={`translate(${x} ${f - r + 20 - Math.abs(Math.sin(t * 4 + k)) * 40}) rotate(${t * 300})`}>
          {[0, 1, 2, 3].map((q) => <ellipse key={q} rx={r} ry={r * 0.6} transform={`rotate(${q * 45})`} fill="none" stroke="#A1887F" strokeWidth={4} />)}</g>; })}
    </g>;
  },

  /** ZONING BOARD: town-hall hearing room. A dais with five members (generic) and nameplates, a chair's gavel (gavelAt
   *  [t...] -> BAM), a wall clock with racing hands, a parcel map on the wall: cols x rows lots that turn yellow (single-
   *  family only) up to `share` from mapAt over mapDur; rows of audience chairs with protest signs popping at protestAt. */
  zoningboard: (t, z, f) => {
    const dx = z.daisX ?? 1000, mapX = z.mapX ?? 1750, share = z.share ?? 0.78, mapAt = z.mapAt ?? 999, mapDur = z.mapDur ?? 2.4;
    const cols = 8, rows = 5, n = cols * rows, k1 = Math.round(share * n), cw = 62;
    const order = Array.from({length: n}, (_, q) => q).sort((p, q) => rnd(p + 31) - rnd(q + 31)); const rank: number[] = []; order.forEach((q, r) => { rank[q] = r; });
    const gav = ((z.gavelAt || []) as number[]).filter((g) => t >= g).pop();
    const gu = gav !== undefined ? t - gav : 9;
    const signs: string[] = z.signs || ['NOT HERE!', 'PARKING?!', 'TOO TALL', 'TRAFFIC!', 'SHADOWS!'];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#E8DCC4" />
      <rect x={z.x0} y={f - 380} width={z.x1 - z.x0} height={380} fill="#A1755A" />
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={900} fill="#7B3F3F" />
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 90)}, (_, k) => <path key={'cp' + k} d={`M ${z.x0 + k * 90} ${f} L ${z.x0 + k * 90 - 200} ${f + 900}`} stroke="#6A3434" strokeWidth={6} />)}
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 140)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 140 + 10} y={f - 360} width={120} height={150} rx={6} fill="none" stroke="#7A543C" strokeWidth={4} />)}
      <rect x={z.x0} y={f - 390} width={z.x1 - z.x0} height={16} fill="#7A543C" stroke={OL} strokeWidth={3} />
      {/* civic banner (generic, no real seal) */}
      <g transform={`translate(${dx} ${f - 760})`}><rect x={-230} y={-90} width={460} height={130} rx={14} fill="#2F4A7A" stroke={OL} strokeWidth={6} />
        <T x={0} y={-30} s={26} c="#FFE082" ls={4}>TOWN OF ANYWHERE</T><T x={0} y={18} s={40} c="#FFFFFF">ZONING BOARD</T></g>
      {/* clock */}
      <g transform={`translate(${dx - 520} ${f - 720})`}><circle r={70} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {Array.from({length: 12}, (_, k) => <path key={k} d={`M ${Math.sin(k * 0.5236) * 56} ${-Math.cos(k * 0.5236) * 56} L ${Math.sin(k * 0.5236) * 64} ${-Math.cos(k * 0.5236) * 64}`} stroke={OL} strokeWidth={3} />)}
        <path d={`M 0 0 L ${Math.sin(t * 0.4 + 5.6) * 34} ${-Math.cos(t * 0.4 + 5.6) * 34}`} stroke={OL} strokeWidth={6} strokeLinecap="round" />
        <path d={`M 0 0 L ${Math.sin(t * 4.8) * 52} ${-Math.cos(t * 4.8) * 52}`} stroke="#E53950" strokeWidth={4} strokeLinecap="round" />
        <T x={0} y={110} s={22}>TUESDAY · LATE</T></g>
      {/* map on the wall */}
      <g transform={`translate(${mapX} ${f - 640})`}>
        <rect x={-cols * cw / 2 - 30} y={-rows * cw / 2 - 80} width={cols * cw + 60} height={rows * cw + 170} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <T x={0} y={-rows * cw / 2 - 34} s={30}>{z.mapTitle || 'RESIDENTIAL LAND'}</T>
        {Array.from({length: n}, (_, q) => { const r = rank[q], x = -cols * cw / 2 + (q % cols) * cw, y = -rows * cw / 2 + Math.floor(q / cols) * cw, on = t >= mapAt + (mapDur * r) / n, sf = r < k1;
          const s = on ? 1 + 0.25 * jig(t, mapAt + (mapDur * r) / n, 20, 8) : 1;
          return <g key={q} transform={`translate(${x + cw / 2} ${y + cw / 2}) scale(${s})`}><rect x={-cw / 2 + 4} y={-cw / 2 + 4} width={cw - 8} height={cw - 8} rx={5} fill={!on ? '#ECEFF1' : sf ? '#FFD54A' : '#64B5F6'} stroke={OL} strokeWidth={2} />
            {on && (sf ? <path d="M -11 9 L -11 -3 L 0 -13 L 11 -3 L 11 9 Z" fill="#FFFFFF" stroke={OL} strokeWidth={2} />
              : <g>{[-8, 4].map((bx) => <rect key={bx} x={bx} y={-13} width={8} height={22} fill="#FFFFFF" stroke={OL} strokeWidth={1.5} />)}</g>)}</g>; })}
        <g transform={`translate(${-cols * cw / 2} ${rows * cw / 2 + 44})`}><rect x={0} y={-16} width={26} height={26} rx={4} fill="#FFD54A" stroke={OL} strokeWidth={2.5} /><T x={36} y={4} s={20} a="start">SINGLE-FAMILY ONLY</T>
          <rect x={cols * cw * 0.6} y={-16} width={26} height={26} rx={4} fill="#64B5F6" stroke={OL} strokeWidth={2.5} /><T x={cols * cw * 0.6 + 36} y={4} s={20} a="start">OTHER</T></g>
      </g>
      {/* dais */}
      <g transform={`translate(${dx} ${f - 200})`}>
        {[-360, -180, 0, 180, 360].map((mx2, k) => { const nod = Math.sin(t * (1.3 + k * 0.2) + k) * 4, sk = ['#F6CDA6', '#8A5634', '#E0A878', '#B97A4B', '#F3D7BD'][k], hc = ['#B0BEC5', '#1B1B1B', '#5D4037', '#3E2723', '#F2C14E'][k];
          const sleepy = k === 4 && Math.sin(t * 0.7) > 0.3;
          return <g key={'bm' + k} transform={`translate(${mx2} ${-150 + nod})`}><path d="M -60 120 L -50 20 Q 0 -10 50 20 L 60 120 Z" fill={['#37474F', '#5C6BC0', '#6D4C41', '#455A64', '#7E57C2'][k]} stroke={OL} strokeWidth={5} />
            <circle cx={0} cy={-30} r={44} fill={sk} stroke={OL} strokeWidth={5} /><path d={`M -44 -40 Q 0 -${k % 2 ? 96 : 80} 44 -40 Q 20 -58 -44 -40 Z`} fill={hc} stroke={OL} strokeWidth={4} />
            {sleepy ? <g><path d="M -20 -30 L -6 -30 M 8 -30 L 22 -30" stroke={OL} strokeWidth={4} /><T x={50} y={-70} s={26} c="#7E57C2">z</T></g>
              : <g><circle cx={-14} cy={-30} r={5} fill={OL} /><circle cx={16} cy={-30} r={5} fill={OL} /></g>}
            {k === 1 && <g><circle cx={-14} cy={-30} r={14} fill="none" stroke={OL} strokeWidth={3} /><circle cx={16} cy={-30} r={14} fill="none" stroke={OL} strokeWidth={3} /></g>}
            <path d={k === 2 ? 'M -12 -4 L 14 -4' : 'M -12 -6 Q 2 2 14 -6'} stroke={OL} strokeWidth={4} fill="none" strokeLinecap="round" /></g>; })}
        <rect x={-500} y={-60} width={1000} height={200} rx={10} fill="#8D6E63" stroke={OL} strokeWidth={7} />
        <rect x={-490} y={-60} width={980} height={22} fill="#A1887F" stroke={OL} strokeWidth={3} />
        {[-360, -180, 0, 180, 360].map((mx2, k) => <g key={'np' + k}><rect x={mx2 - 70} y={-30} width={140} height={34} rx={4} fill="#FFF8E1" stroke={OL} strokeWidth={3} /><T x={mx2} y={-6} s={18}>{k === 2 ? 'CHAIR' : 'MEMBER'}</T></g>)}
        {/* gavel */}
        <g transform={`translate(80 -70) rotate(${gu < 0.35 ? -50 + 50 * Math.min(1, gu / 0.12) : -35 + 3 * Math.sin(t * 2)} 60 0)`}><rect x={0} y={-8} width={70} height={14} rx={5} fill="#5D4037" stroke={OL} strokeWidth={3} />
          <rect x={-20} y={-24} width={30} height={46} rx={6} fill="#6D4C41" stroke={OL} strokeWidth={3} /></g>
        {gu < 0.8 && <g transform={`translate(40 -90) scale(${E.outBack(win(gu, 0.05, 0.25)) * (1 - win(gu, 0.55, 0.25))})`}>
          <path d="M 0 -60 L 20 -20 L 64 -30 L 34 4 L 60 40 L 14 26 L 0 66 L -14 26 L -60 40 L -34 4 L -64 -30 L -20 -20 Z" fill="#FFE066" stroke={OL} strokeWidth={4} /><T x={0} y={12} s={30} c="#E53950">BAM</T></g>}
      </g>
      {/* podium */}
      <g transform={`translate(${z.podX ?? dx - 700} ${f})`}><path d="M -80 0 L -60 -200 L 60 -200 L 80 0 Z" fill="#6D4C41" stroke={OL} strokeWidth={5} />
        <path d="M 30 -200 L 50 -260" stroke={OL} strokeWidth={5} /><circle cx={52} cy={-266} r={10} fill="#37474F" stroke={OL} strokeWidth={3} />
        <T x={0} y={-90} s={18} c="#FFE082">PUBLIC COMMENT</T></g>
      {/* audience: backs of heads + signs */}
      {Array.from({length: Math.ceil((z.x1 - z.x0) / 150)}, (_, k) => { const ax = z.x0 + 60 + k * 150; if (Math.abs(ax - (z.podX ?? dx - 700)) < 110) return null;
        const pa = z.protestAt !== undefined ? pop(t, z.protestAt + (k % 5) * 0.15, 0.4) : 0, txt = signs[k % signs.length];
        return <g key={'au' + k} transform={`translate(${ax} ${f + 150 + (k % 2) * 30})`}><rect x={-60} y={-60} width={120} height={70} rx={10} fill="#5D4037" stroke={OL} strokeWidth={4} />
          <circle cx={0} cy={-100} r={42} fill={['#3E2723', '#1B1B1B', '#F2C14E', '#B0BEC5', '#8D5524'][k % 5]} stroke={OL} strokeWidth={4} />
          {pa > 0 && k % 2 === 0 && <g transform={`translate(${(k % 3 - 1) * 20} ${-170 - 20 * Math.abs(Math.sin(t * 6 + k))}) scale(${pa}) rotate(${Math.sin(t * 5 + k) * 8})`}>
            <path d="M 0 0 L 0 100" stroke="#8D6E63" strokeWidth={8} /><rect x={-80} y={-60} width={160} height={70} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
            <T x={0} y={-14} s={fit(txt, 150, 26)} c="#C62828">{txt}</T></g>}</g>; })}
    </g>;
  },

  /** BASEMENT: low concrete-block room, pipes and a swinging bare bulb, a washer that shakes, boxes, a futon, a string of
   *  lights, a high window where feet walk past, stairs up to a door that opens at doorAt (light spills). */
  basement: (t, z, f) => {
    const bx = z.bulbX ?? 1000, door = z.doorAt !== undefined ? clamp((t - z.doorAt) / 0.5) : 0, sx = z.stairsX ?? 1900;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#CFC8BC" />
      {Array.from({length: 14}, (_, r) => Array.from({length: Math.ceil((z.x1 - z.x0) / 160) + 1}, (_, c) => <rect key={r + '-' + c} x={z.x0 + c * 160 - (r % 2) * 80} y={f - 60 - r * 60} width={156} height={56} fill="none" stroke="#B5AC9C" strokeWidth={3} />))}
      <rect x={z.x0} y={f - 760} width={z.x1 - z.x0} height={60} fill="#8C8273" stroke={OL} strokeWidth={4} />
      {[0, 1].map((k) => <path key={'pp' + k} d={`M ${z.x0} ${f - 680 + k * 34} L ${z.x1} ${f - 680 + k * 34}`} stroke={k ? '#B87333' : '#90A4AE'} strokeWidth={18} />)}
      {/* high window with passing feet */}
      <g transform={`translate(${z.winX ?? 500} ${f - 600})`}><rect x={-150} y={-60} width={300} height={110} fill="#BFE6FF" stroke={OL} strokeWidth={6} />
        <rect x={-150} y={20} width={300} height={30} fill="#7CC36A" />
        <g><clipPath id="bswin"><rect x={-150} y={-60} width={300} height={110} /></clipPath><g clipPath="url(#bswin)">
          {[0, 1].map((k) => { const fx = -260 + ((t * 120 + k * 260) % 520), st = Math.sin(t * 8 + k * 3) * 16;
            return <g key={'ft' + k} transform={`translate(${fx} 20)`}><path d={`M -10 -90 L ${-10 + st} 0 M 14 -90 L ${14 - st} 0`} stroke={['#2D3E66', '#4E342E'][k]} strokeWidth={18} />
              <ellipse cx={-10 + st + 10} cy={0} rx={18} ry={8} fill="#1B1B1B" /><ellipse cx={14 - st + 10} cy={0} rx={18} ry={8} fill="#1B1B1B" /></g>; })}</g></g>
        <path d="M 0 -60 L 0 50 M -150 -5 L 150 -5" stroke={OL} strokeWidth={4} /></g>
      {/* string lights */}
      <path d={`M ${z.x0 + 100} ${f - 640} Q ${bx - 300} ${f - 560} ${bx - 100} ${f - 630} Q ${bx + 200} ${f - 560} ${sx - 200} ${f - 640}`} fill="none" stroke={OL} strokeWidth={2} />
      {Array.from({length: 16}, (_, k) => { const u = k / 15, lx = lerp(z.x0 + 100, sx - 200, u); return <circle key={'sl' + k} cx={lx} cy={f - 610 + Math.sin(u * Math.PI * 2) * 22} r={9} fill={['#FF5A5F', '#FFC93C', '#7BD389', '#4FB3F6'][k % 4]} opacity={0.6 + 0.4 * Math.sin(t * 4 + k)} />; })}
      {/* bulb */}
      <g transform={`translate(${bx} ${f - 700}) rotate(${Math.sin(t * 1.4) * 12})`}><path d="M 0 0 L 0 140" stroke={OL} strokeWidth={4} />
        <ellipse cx={0} cy={250} rx={240} ry={70} fill="#FFF59D" opacity={0.18} transform="translate(0 0)" />
        <circle cx={0} cy={160} r={26} fill="#FFF59D" stroke={OL} strokeWidth={4} /><rect x={-12} y={130} width={24} height={14} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={900} fill="#9E968A" />
      {/* washer */}
      <g transform={`translate(${z.washX ?? 230 + Math.sin(t * 30) * 3} ${f})`}><rect x={-110} y={-260} width={220} height={260} rx={14} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <circle cx={0} cy={-120} r={70} fill="#BBDEFB" stroke={OL} strokeWidth={6} /><g transform={`translate(0 -120) rotate(${t * 400})`}><path d="M -40 0 Q 0 30 40 0" stroke="#4FB3F6" strokeWidth={10} fill="none" /></g>
        <rect x={-90} y={-240} width={60} height={20} rx={4} fill="#ECEFF1" stroke={OL} strokeWidth={3} /></g>
      {/* boxes */}
      {[['HOLIDAY', 0, 0], ["DAD'S STUFF", 1, 0], ['TROPHIES', 0.5, 1]].map(([tx, cx, cy], k) => <g key={'bx' + k} transform={`translate(${(z.boxX ?? 560) + Number(cx) * 200} ${f - Number(cy) * 130})`}>
        <rect x={-95} y={-130} width={190} height={130} rx={4} fill="#D7A86E" stroke={OL} strokeWidth={5} /><path d="M -95 -96 L 95 -96" stroke="#A9783F" strokeWidth={5} />
        <T x={0} y={-48} s={fit(String(tx), 170, 26)}>{tx}</T></g>)}
      {/* futon */}
      <g transform={`translate(${z.futonX ?? 1250} ${f})`}><rect x={-260} y={-110} width={520} height={80} rx={20} fill="#5C6BC0" stroke={OL} strokeWidth={6} />
        <rect x={-260} y={-230} width={520} height={130} rx={24} fill="#7986CB" stroke={OL} strokeWidth={6} />
        {[-220, 200].map((lx) => <rect key={lx} x={lx} y={-30} width={20} height={30} fill="#5D4037" stroke={OL} strokeWidth={3} />)}
        <rect x={140} y={-160} width={90} height={60} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>
      {/* poster */}
      <g transform={`translate(${(z.futonX ?? 1250) - 30} ${f - 470}) rotate(-3)`}><rect x={-120} y={-80} width={240} height={160} fill="#FFF3E0" stroke={OL} strokeWidth={5} />
        <path d="M -60 40 L -60 -10 L 0 -50 L 60 -10 L 60 40 Z" fill="#FFCDD2" stroke={OL} strokeWidth={4} /><T x={0} y={68} s={20}>{z.poster || 'DREAM HOUSE'}</T></g>
      {/* stairs + door */}
      <g transform={`translate(${sx} ${f})`}>
        {Array.from({length: 7}, (_, k) => <rect key={'stp' + k} x={-40 + k * 70} y={-(k + 1) * 80} width={90} height={(k + 1) * 80} fill="#8D6E63" stroke={OL} strokeWidth={4} />)}
        <rect x={400} y={-760} width={130} height={200} fill={door > 0 ? '#FFF59D' : '#5D4037'} stroke={OL} strokeWidth={5} />
        {door > 0 && <path d={`M 400 -560 L 300 -100 L 640 -100 L 530 -560 Z`} fill="#FFF59D" opacity={0.25 * door} />}
        <rect x={400} y={-760} width={130 * (1 - door * 0.8)} height={200} fill="#A1662F" stroke={OL} strokeWidth={5} /></g>
    </g>;
  },
};

/* ============================================================================================ ITEMS */
/** the running gag: a little home with a sign. type: 'house' | 'shed' | 'dog' | 'bird' | 'mailbox'; size keyframes; sign text */
const minihome: ItemFn = (a, {t, f}, i) => {
  if (!vis(a, t)) return null;
  const at = a.at ?? 0, x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * kf(a.size, t, 1) * pop(t, at, 0.5) * outF(a, t), ty: string = a.type || 'house';
  const wob = jig(t, at + 0.1, 18, 5) * 0.1;
  const body = (() => {
    switch (ty) {
      case 'shed': return <g><rect x={-120} y={-170} width={240} height={170} fill="#BCAAA4" stroke={OL} strokeWidth={6} /><path d="M -140 -166 L 0 -240 L 140 -166 Z" fill="#6D4C41" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <rect x={-50} y={-120} width={100} height={120} fill="#8D6E63" stroke={OL} strokeWidth={5} /><path d="M -50 -120 L 50 0 M 50 -120 L -50 0" stroke={OL} strokeWidth={3} /></g>;
      case 'dog': return <g><path d="M -110 0 L -110 -110 L 0 -190 L 110 -110 L 110 0 Z" fill="#E53950" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <path d="M -40 0 L -40 -70 Q 0 -110 40 -70 L 40 0 Z" fill="#3E2723" stroke={OL} strokeWidth={5} /><rect x={-70} y={-160} width={140} height={30} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-138} s={18}>{a.plate || 'HOME'}</T></g>;
      case 'bird': return <g><rect x={-8} y={-10} width={16} height={180} fill="#8D6E63" stroke={OL} strokeWidth={3} transform="translate(0 -10)" />
        <g transform="translate(0 -20)"><rect x={-60} y={-110} width={120} height={110} fill="#4FB3F6" stroke={OL} strokeWidth={5} /><path d="M -76 -106 L 0 -160 L 76 -106 Z" fill="#FFC93C" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <circle cx={0} cy={-60} r={20} fill="#1B2433" /><path d="M -10 -24 L 10 -24" stroke="#8D6E63" strokeWidth={6} /></g></g>;
      case 'mailbox': return <g><rect x={-8} y={-120} width={16} height={120} fill="#8D6E63" stroke={OL} strokeWidth={3} /><path d="M -60 -120 L -60 -170 Q 0 -210 60 -170 L 60 -120 Z" fill="#2F6FD1" stroke={OL} strokeWidth={5} />
        <path d={`M 56 -170 L 56 ${-220 + 20 * Math.abs(Math.sin(t * 3))}`} stroke="#E53950" strokeWidth={7} /></g>;
      default: return <g><rect x={-150} y={-200} width={300} height={200} fill="#FFE0B2" stroke={OL} strokeWidth={6} /><path d="M -180 -196 L 0 -320 L 180 -196 Z" fill="#D84315" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <rect x={-36} y={-120} width={72} height={120} fill="#A1662F" stroke={OL} strokeWidth={5} />{[-120, 60].map((wx) => <rect key={wx} x={wx} y={-170} width={60} height={56} fill="#CFEFFF" stroke={OL} strokeWidth={4} />)}
        <rect x={80} y={-310} width={34} height={70} fill="#8D6E63" stroke={OL} strokeWidth={4} /></g>;
    }
  })();
  const sign = a.sign ?? 'STARTER HOME';
  return <g key={'mh' + i} transform={`translate(${x} ${y}) scale(${s * (1 + wob)} ${s * (1 - wob)})`}>
    <ellipse cx={0} cy={6} rx={170} ry={14} fill={OL} opacity={0.15} />{body}
    {sign && <g transform={`translate(${a.signDX ?? 0} ${a.signDY ?? ({house: -380, shed: -300, dog: -250, bird: -380, mailbox: -270} as Record<string, number>)[ty] ?? -380}) rotate(${Math.sin(t * 2 + i) * 3})`}><rect x={-fit(sign, 400, 34) * sign.length * 0.33 - 24} y={-32} width={fit(sign, 400, 34) * sign.length * 0.66 + 48} height={56} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      <T x={0} y={8} s={fit(sign, 400, 34)} c="#2E7D32">{sign}</T></g>}
  </g>;
};

/** a hand-held sign on a stick (bobs). text (\n for lines), color, x/y keyframes (y = top of the stick) */
const placard: ItemFn = (a, {t}, i) => {
  if (!vis(a, t)) return null;
  const at = a.at ?? 0, x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, at, 0.4) * outF(a, t), L = lines(a.text || 'PLEASE');
  const w = Math.max(...L.map((l) => l.length)) * (a.size ?? 40) * 0.66 + 60, h = L.length * (a.size ?? 40) * 1.15 + 34;
  return <g key={'pl' + i} transform={`translate(${x} ${y + Math.sin(t * 5 + i) * 6}) scale(${s}) rotate(${Math.sin(t * 3 + i) * 5 + (a.rot ?? 0)})`}>
    <path d={`M 0 ${h / 2} L 0 ${h / 2 + 120}`} stroke="#8D6E63" strokeWidth={10} />
    <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={10} fill={a.color || '#FFFFFF'} stroke={OL} strokeWidth={5} />
    {L.map((l, k) => <T key={k} x={0} y={-h / 2 + 17 + (k + 0.85) * (a.size ?? 40) * 1.15} s={a.size ?? 40} c={a.textColor || '#C62828'}>{l}</T>)}
  </g>;
};

/** BIDDING WAR: paddles pop up across a line (x0..x1) at raises [[t, text], ...], each with a hand, then hold, jiggling */
const paddles: ItemFn = (a, {t, f}, i) => {
  if (!vis(a, t)) return null;
  const raises: [number, string][] = (a.raises || []).map((p: any) => [Number(p[0]), String(p[1])]), x0 = a.x0 ?? 400, x1 = a.x1 ?? 1600, y = kf(a.y, t, f - 300), n = raises.length, o = outF(a, t);
  return <g key={'pd' + i} opacity={o}>{raises.map(([rt, txt], k) => { if (t < rt) return null;
    const px = n > 1 ? lerp(x0, x1, k / (n - 1)) : x0, u = E.outBack(win(t, rt, 0.35)), sh = jig(t, rt + 0.3, 22, 4) * 8, last = k === n - 1 || t < raises[k + 1][0];
    return <g key={k} transform={`translate(${px} ${y + (1 - u) * 260 + (k % 2) * 40}) rotate(${sh + (k % 2 ? 6 : -6)})`}>
      <path d="M 0 40 L 0 170" stroke="#8D6E63" strokeWidth={14} strokeLinecap="round" />
      <circle cx={0} cy={180} r={22} fill={['#F6CDA6', '#B97A4B', '#E0A878', '#8A5634'][k % 4]} stroke={OL} strokeWidth={4} />
      <ellipse cx={0} cy={-10} rx={Math.max(90, txt.length * 13)} ry={70} fill={last ? '#FFE066' : '#FFFFFF'} stroke={OL} strokeWidth={6} />
      <T x={0} y={4} s={fit(txt, Math.max(150, txt.length * 22), 32)} c={last ? '#C62828' : OL}>{txt}</T></g>; })}</g>;
};

/** giant gold padlock with a label; clamps (shackle drops) at lockAt with a CLANK burst; chain to the left (chainTo x) */
const padlock: ItemFn = (a, {t}, i) => {
  if (!vis(a, t)) return null;
  const at = a.at ?? 0, x = kf(a.x, t, 960), y = kf(a.y, t, 500), s = (a.scale ?? 1) * pop(t, at, 0.5) * outF(a, t), la = a.lockAt ?? at + 0.8;
  const closed = clamp((t - la) / 0.18), sh = jig(t, la + 0.18, 30, 6);
  return <g key={'lk' + i} transform={`translate(${x + sh * 6} ${y}) scale(${s}) rotate(${sh * 6})`}>
    {a.chainTo !== undefined && <path d={`M -100 30 Q ${(a.chainTo - x) / 2 / Math.max(0.01, s)} ${140 + 20 * Math.sin(t * 2)} ${(a.chainTo - x) / Math.max(0.01, s)} 30`} fill="none" stroke="#9E9E9E" strokeWidth={14} strokeDasharray="20 8" />}
    <path d={`M -70 -40 L -70 ${-120 - 50 * (1 - closed)} Q 0 ${-220 - 50 * (1 - closed)} 70 ${-120 - 50 * (1 - closed)} L 70 ${-40 - 50 * (1 - closed)}`} fill="none" stroke="#90A4AE" strokeWidth={30} strokeLinecap="round" />
    <path d={`M -70 -40 L -70 ${-120 - 50 * (1 - closed)} Q 0 ${-220 - 50 * (1 - closed)} 70 ${-120 - 50 * (1 - closed)} L 70 ${-40 - 50 * (1 - closed)}`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />
    <rect x={-120} y={-60} width={240} height={190} rx={30} fill="#FFC93C" stroke={OL} strokeWidth={8} />
    <rect x={-100} y={-44} width={30} height={150} rx={12} fill="#FFFFFF" opacity={0.35} />
    <circle cx={0} cy={10} r={18} fill={OL} /><path d="M 0 16 L 0 56" stroke={OL} strokeWidth={14} strokeLinecap="round" />
    {a.text && <T x={0} y={112} s={fit(String(a.text), 200, 40)}>{a.text}</T>}
    {t > la && t < la + 0.7 && <g transform={`translate(110 -160) scale(${E.outBack(win(t, la, 0.2)) * (1 - win(t, la + 0.45, 0.25))})`}>
      <path d="M 0 -50 L 16 -16 L 54 -24 L 28 4 L 50 34 L 12 22 L 0 56 L -12 22 L -50 34 L -28 4 L -54 -24 L -16 -16 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={10} s={24} c="#C62828">CLANK</T></g>}
  </g>;
};

/** a glass jar of savings that fills to `level` keyframes (0..1) with coins dropping in; label */
const savejar: ItemFn = (a, {t}, i) => {
  if (!vis(a, t)) return null;
  const at = a.at ?? 0, x = kf(a.x, t, 960), y = kf(a.y, t, 700), s = (a.scale ?? 1) * pop(t, at, 0.45) * outF(a, t), lv = clamp(kf(a.level, t, 0.3));
  return <g key={'jr' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-90} y={-260} width={180} height={260} rx={30} fill="#E1F5FE" fillOpacity={0.6} stroke={OL} strokeWidth={6} />
    <clipPath id={`jr${i}`}><rect x={-86} y={-256} width={172} height={252} rx={28} /></clipPath>
    <g clipPath={`url(#jr${i})`}><rect x={-90} y={-250 * lv} width={180} height={260} fill="#FFC93C" />
      {Array.from({length: 10}, (_, k) => <ellipse key={k} cx={-70 + (k % 5) * 35} cy={-250 * lv + 10 + Math.floor(k / 5) * 22} rx={16} ry={6} fill="#FFB300" stroke={OL} strokeWidth={2} />)}</g>
    <rect x={-100} y={-290} width={200} height={40} rx={10} fill="#8D6E63" stroke={OL} strokeWidth={5} />
    {[0, 1].map((k) => { const u = ((t - at) * 1.2 + k * 0.5) % 1; return <ellipse key={'cd' + k} cx={-20 + k * 40} cy={-420 + u * 300} rx={16} ry={6} fill="#FFC93C" stroke={OL} strokeWidth={2} opacity={u < 0.85 ? 1 : 0} />; })}
    <rect x={-110} y={-150} width={220} height={60} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-110} s={fit(a.text || 'DOWN PAYMENT', 200, 26)}>{a.text || 'DOWN PAYMENT'}</T>
  </g>;
};

/** two cartoon bars: NEEDED vs HAVE (values supplied), with labels, a gap bracket and a GAP tag (all text supplied) */
const incomebars: ItemFn = (a, {t, f}, i) => {
  if (!vis(a, t)) return null;
  const at = a.at ?? 0, x = kf(a.x, t, 960), y = kf(a.y, t, f), o = outF(a, t), mx = a.max ?? 120, H = a.h ?? 560;
  const bars: any[] = a.bars || [];
  return <g key={'ib' + i} transform={`translate(${x} ${y})`} opacity={o}>
    <path d={`M -260 0 L 260 0`} stroke={OL} strokeWidth={6} />
    {bars.map((b, k) => { const u = E.out(win(t, b.at ?? at + k * 0.6, 0.9)), h = (Number(b.value) / mx) * H * u, bx = -150 + k * 300;
      return <g key={k}><rect x={bx - 90} y={-h} width={180} height={h} rx={10} fill={b.color || '#4FB3F6'} stroke={OL} strokeWidth={6} />
        {u > 0.6 && <g><T x={bx} y={-h - 26} s={40}>{b.display}</T><T x={bx} y={44} s={fit(String(b.label), 280, 26)}>{b.label}</T></g>}</g>; })}
    {bars.length === 2 && a.gapAt !== undefined && t >= a.gapAt && (() => { const h0 = (Number(bars[0].value) / mx) * H, h1 = (Number(bars[1].value) / mx) * H, u = E.outBack(win(t, a.gapAt, 0.5));
      return <g transform={`translate(330 0)`}><path d={`M 0 ${-h0} L 30 ${-h0} L 30 ${-h1} L 0 ${-h1}`} fill="none" stroke="#C62828" strokeWidth={6} />
        <path d={`M -190 ${-h1} L 20 ${-h1}`} stroke="#C62828" strokeWidth={4} strokeDasharray="10 8" />
        <g transform={`translate(110 ${-(h0 + h1) / 2}) scale(${u})`}><rect x={-80} y={-34} width={160} height={60} rx={14} fill="#C62828" stroke={OL} strokeWidth={4} /><T x={0} y={8} s={30} c="#FFFFFF">{a.gapText || 'GAP'}</T></g></g>; })()}
  </g>;
};

export const HOUSING_ITEMS: Record<string, ItemFn> = {minihome, placard, paddles, padlock, savejar, incomebars};
export const HOUSING_INDOOR = ['shrinker', 'zoningboard', 'basement'];
