import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * DEBT kit for CartoonStage (Episode 59, "Who Actually Owns America's $40 Trillion in Debt?").
 *
 * Prime-time sitcom look (genre level only; everything ORIGINAL), day scenes, no flags, seals or logos.
 * Sets: iouvault (the giant IOU vault + debt odometer), auctionhouse (Treasury auction hall: podium, bidder paddles, results
 * board), dinnerparty (the holders' dining room; the table itself is the `feast` item so seated `toon`s sit behind it),
 * mainstreet (holders' street: fund, bank, pension, insurer, city hall, houses; bond certificates pop in the windows),
 * fedwarehouse (the Fed's balance-sheet warehouse: shelves of bond crates that thin out and refill, a holdings gauge),
 * trustcabinet (Social Security trust fund filing-cabinet room; drawers of IOU folders that empty; a tube to the Treasury),
 * meterscale (a giant interest meter vs a defense balance scale), debttitle (show title card), debtbumper (act bumper).
 * Items: owen (OWEN, a living IOU note: the running gag, grows every act), feast (the dinner table: plates sized by holdings,
 * place cards, no flags), ioustack (a stack of IOU notes that grows), bondpop (a bond certificate that pops with sparkle).
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
/** a position param: > 1 = absolute world x; 0..1 = fraction of the zone width */
const PX = (z: Z, v: any, def: number) => (v === undefined ? def : Number(v) > 1 ? Number(v) : z.x0 + (z.x1 - z.x0) * Number(v));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.62);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const PAPER = '#FFF8E6', GOLD = '#F2B63A', GREEN = '#2E9E6B', BLUE = '#2E6BD1', RED = '#D93A49', NAVY = '#1B2A4A';

/** a small IOU note (paper with "IOU" and a signature line) at 0,0 */
const note = (w: number, h: number, txt = 'IOU', fill = PAPER, k = 0) => <g>
  <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={Math.min(10, h * 0.12)} fill={fill} stroke={OL} strokeWidth={Math.max(2, w * 0.03)} />
  <rect x={-w / 2 + w * 0.06} y={-h / 2 + h * 0.1} width={w * 0.88} height={h * 0.8} rx={4} fill="none" stroke={GREEN} strokeWidth={Math.max(1.5, w * 0.015)} opacity={0.6} />
  <T x={0} y={h * 0.08} s={h * 0.36} c={GREEN}>{txt}</T>
  <path d={`M ${-w * 0.3} ${h * 0.3} q ${w * 0.1} ${-h * 0.12} ${w * 0.2} 0 t ${w * 0.2} 0`} stroke={OL} strokeWidth={Math.max(1.5, w * 0.012)} fill="none" opacity={0.6} transform={`translate(${(rnd(k) - 0.5) * 6} 0)`} />
</g>;

/** a bond certificate (gold border, ribbon) at 0,0 */
const bond = (w: number, h: number, txt = 'T-BOND', k = 0) => <g>
  <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={6} fill="#FFFDF4" stroke={OL} strokeWidth={Math.max(2, w * 0.025)} />
  <rect x={-w / 2 + 5} y={-h / 2 + 5} width={w - 10} height={h - 10} rx={4} fill="none" stroke={GOLD} strokeWidth={Math.max(2, w * 0.03)} />
  <T x={0} y={-h * 0.08} s={h * 0.24} c={NAVY}>{txt}</T>
  <circle cx={w * 0.3} cy={h * 0.22} r={h * 0.14} fill={k % 2 ? RED : BLUE} stroke={OL} strokeWidth={2} />
  <path d={`M ${-w * 0.36} ${h * 0.22} L ${w * 0.1} ${h * 0.22}`} stroke={OL} strokeWidth={2} opacity={0.4} />
</g>;

/** daylight window with sky + drifting clouds-free haze (no smiley sun) */
const windowPane = (x: number, y: number, w: number, h: number, t: number, k: number) => <g key={'wp' + k}>
  <rect x={x} y={y} width={w} height={h} rx={w * 0.08} fill="#9FD3F5" stroke={OL} strokeWidth={6} />
  <rect x={x + 8} y={y + h * 0.62} width={w - 16} height={h * 0.3} fill="#BFE6FF" opacity={0.7} />
  <path d={`M ${x + w / 2} ${y} L ${x + w / 2} ${y + h} M ${x} ${y + h / 2} L ${x + w} ${y + h / 2}`} stroke={OL} strokeWidth={5} />
  <path d={`M ${x + w * 0.15} ${y + h * 0.12} L ${x + w * 0.38} ${y + h * 0.4}`} stroke="#FFFFFF" strokeWidth={8} opacity={0.5 + 0.2 * Math.sin(t * 2 + k)} strokeLinecap="round" />
</g>;

/** flip-digit odometer: shows `txt` (string) with digits wobbling when they change */
const odometer = (txt: string, t: number, cw = 64, ch = 96, changeT = -9) => {
  const n = txt.length, w = n * cw;
  return <g>
    <rect x={-w / 2 - 20} y={-ch / 2 - 20} width={w + 40} height={ch + 40} rx={18} fill="#22314F" stroke={OL} strokeWidth={6} />
    {txt.split('').map((c, k) => { const isD = /[0-9]/.test(c), wob = isD ? Math.sin(t * 30 + k) * 2 * Math.max(0, 1 - (t - changeT)) : 0;
      return <g key={k} transform={`translate(${-w / 2 + k * cw + cw / 2} ${wob})`}>
        {isD && <rect x={-cw / 2 + 4} y={-ch / 2} width={cw - 8} height={ch} rx={8} fill="#0E1729" stroke="#3B4C70" strokeWidth={3} />}
        {isD && <path d={`M ${-cw / 2 + 4} 0 L ${cw / 2 - 4} 0`} stroke="#3B4C70" strokeWidth={2} />}
        <T x={0} y={ch * 0.32} s={ch * 0.8} c={isD ? '#FFE27A' : '#FFFFFF'}>{c}</T></g>; })}
  </g>;
};

/* ================================================================================================ SETS */
export const DEBT_SETS: Record<string, SetFn> = {
  /** THE IOU VAULT: riveted steel interior lit by skylights; a round vault door (opens at openAt) revealing towering IOU
   *  stacks; an IOU printing press on the right feeding notes onto a conveyor; the DEBT ODOMETER on the back wall (odo:
   *  [[t, trillions]], decimals odoDec; label odoLabel). doorX/pressX are fractions of the zone width. */
  iouvault: (t, z, f) => {
    const w = z.x1 - z.x0, dx = PX(z, z.doorX, 760), px = PX(z, z.pressX, 2050);
    const open = z.openAt !== undefined ? E.inOutBack(win(t, z.openAt, 1.1)) : (z.open ?? 1);
    const odo = kf(z.odo, t, 40.6), dec = z.odoDec ?? 1, str = '$' + odo.toFixed(dec) + 'T';
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#B9C4D3" />
      {Array.from({length: Math.ceil(w / 240) + 1}, (_, k) => <g key={'pl' + k}><rect x={z.x0 + k * 240} y={-400} width={236} height={f + 400} fill={k % 2 ? '#AEBACB' : '#B5C1D1'} stroke="#8E9BB0" strokeWidth={3} />
        {Array.from({length: 9}, (_, r) => <circle key={r} cx={z.x0 + k * 240 + 14} cy={-360 + r * 140} r={6} fill="#8E9BB0" />)}</g>)}
      {/* skylights with god rays */}
      {[200, 1200, 2200].map((p, k) => { const sx = p; return <g key={'sk' + k}>
        <path d={`M ${sx - 90} -60 L ${sx + 90} -60 L ${sx + 260} ${f} L ${sx - 260} ${f} Z`} fill="#FFF6D0" opacity={0.18 + 0.05 * Math.sin(t * 1.5 + k)} />
        <rect x={sx - 110} y={-90} width={220} height={40} rx={8} fill="#CFEFFF" stroke={OL} strokeWidth={5} /></g>; })}
      {/* odometer */}
      <g transform={`translate(${PX(z, z.odoX, 1200)} ${z.odoY ?? 150}) scale(${z.odoS ?? 1})`}>
        <rect x={-420} y={-130} width={840} height={52} rx={12} fill={RED} stroke={OL} strokeWidth={5} />
        <T x={0} y={-92} s={30} c="#FFFFFF" ls={3}>{z.odoLabel || 'TOTAL PUBLIC DEBT'}</T>
        {odometer(str, t)}
        {[-1, 1].map((sd) => <circle key={sd} cx={sd * 380} cy={0} r={18} fill={(Math.floor(t * 4) % 2) ? '#FF6B6B' : '#7A1E28'} stroke={OL} strokeWidth={4} />)}
      </g>
      {/* inner vault: IOU stacks seen through the door */}
      <g>
        <circle cx={dx} cy={f - 330} r={320} fill="#5A6680" stroke={OL} strokeWidth={8} />
        <clipPath id={'vclip' + Math.round(z.x0)}><circle cx={dx} cy={f - 330} r={300} /></clipPath>
        <g clipPath={`url(#vclip${Math.round(z.x0)})`}>
          <rect x={dx - 320} y={f - 660} width={640} height={660} fill="#FFE9A8" opacity={0.25 + 0.2 * open} />
          {Array.from({length: 7}, (_, k) => { const h = 6 + Math.floor(rnd(k * 3) * 6); return <g key={'st' + k} transform={`translate(${dx - 270 + k * 90} ${f - 40})`}>
            {Array.from({length: h}, (_, q) => <g key={q} transform={`translate(${(rnd(k * 9 + q) - 0.5) * 10} ${-q * 42})`}>{note(80, 40, 'IOU', PAPER, k * 11 + q)}</g>)}</g>; })}
        </g>
        {/* the door: a thick round slab swinging open (scaleX squash) */}
        <g transform={`translate(${dx - 300 * open * 0.98} ${f - 330}) scale(${1 - 0.82 * open} 1)`}>
          <circle r={310} fill="#C9D3E0" stroke={OL} strokeWidth={10} />
          <circle r={250} fill="#B4C0D0" stroke={OL} strokeWidth={6} />
          {Array.from({length: 12}, (_, k) => { const an = (k / 12) * Math.PI * 2; return <circle key={k} cx={Math.cos(an) * 280} cy={Math.sin(an) * 280} r={12} fill="#8E9BB0" stroke={OL} strokeWidth={3} />; })}
          <g transform={`rotate(${(z.openAt !== undefined ? win(t, z.openAt - 1.2, 1.2) : 1) * 360})`}>
            <circle r={70} fill="#E3E9F1" stroke={OL} strokeWidth={6} />
            {[0, 1, 2].map((k) => <rect key={k} x={-150} y={-12} width={300} height={24} rx={12} fill="#E3E9F1" stroke={OL} strokeWidth={5} transform={`rotate(${k * 60})`} />)}
          </g>
          <T x={0} y={-180} s={40} c={NAVY} ls={4}>{z.doorText || 'IOU VAULT'}</T>
        </g>
      </g>
      {/* IOU press + conveyor */}
      <g transform={`translate(${px} ${f})`}>
        <rect x={-150} y={-420} width={300} height={300} rx={20} fill="#2E9E6B" stroke={OL} strokeWidth={7} />
        <rect x={-120} y={-390} width={240} height={90} rx={10} fill="#DFF5E8" stroke={OL} strokeWidth={4} />
        <T x={0} y={-332} s={34} c={NAVY}>IOU PRESS</T>
        <g transform={`translate(0 ${-250 + 30 * Math.abs(Math.sin(t * 5))})`}><rect x={-110} y={-20} width={220} height={40} rx={8} fill="#9AA7B8" stroke={OL} strokeWidth={5} /></g>
        {[-90, 90].map((gx, k) => <g key={k} transform={`translate(${gx} -170) rotate(${t * 140 * (k ? -1 : 1)})`}><circle r={40} fill={GOLD} stroke={OL} strokeWidth={5} />{[0, 1, 2, 3].map((q) => <rect key={q} x={-6} y={-52} width={12} height={20} fill={GOLD} stroke={OL} strokeWidth={3} transform={`rotate(${q * 45})`} />)}</g>)}
        <rect x={-150} y={-120} width={300} height={120} fill="#25704D" stroke={OL} strokeWidth={6} />
        {/* conveyor towards the vault */}
        <rect x={-900} y={-150} width={760} height={34} rx={17} fill="#4A5874" stroke={OL} strokeWidth={5} />
        {Array.from({length: 9}, (_, k) => <circle key={k} cx={-880 + k * 90} cy={-133} r={10} fill="#9AA7B8" stroke={OL} strokeWidth={3} />)}
        {Array.from({length: 6}, (_, k) => { const u = ((t * (z.pressRate ?? 0.35)) + k / 6) % 1; return <g key={'n' + k} transform={`translate(${-170 - u * 720} ${-178}) rotate(${Math.sin(u * 20) * 4})`}>{note(90, 46, 'IOU', PAPER, k)}</g>; })}
      </g>
      {/* floor */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#7D879A" />
      <rect x={z.x0} y={f} width={w} height={20} fill="#9AA4B6" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 160} ${f + 20} L ${z.x0 + k * 160 - 120} ${f + 400}`} stroke="#6E788B" strokeWidth={4} />)}
    </g>;
  },

  /** TREASURY AUCTION HOUSE: a bright hall with columns and tall windows; an auctioneer podium (podX); a results board
   *  (board: {title, rows: [[t, text]]}); three tiers of generic bidders (silhouette heads) whose paddles rise at bidsAt
   *  (colour-coded INDIRECT / DIRECT / DEALER); a SOLD! burst at soldAt. */
  auctionhouse: (t, z, f) => {
    const w = z.x1 - z.x0, pod = PX(z, z.podX, 1200), bids = z.bidsAt, sold = z.soldAt;
    const rows: [number, string][] = (z.board?.rows || []).map((r: any) => [Number(r[0]), String(r[1])]);
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#F3EBDA" />
      <rect x={z.x0} y={f - 760} width={w} height={40} fill="#E2D3B5" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const cx = z.x0 + 100 + k * 420; if (Math.abs(cx - pod) < 520) return null;
        return <g key={'w' + k}>{windowPane(cx + 60, f - 640, 200, 320, t, k)}</g>; })}
      {Array.from({length: Math.ceil(w / 420) + 1}, (_, k) => { const cx = z.x0 + k * 420; return <g key={'c' + k}>
        <rect x={cx - 34} y={f - 720} width={68} height={720} fill="#FFFDF6" stroke={OL} strokeWidth={5} />
        {[-18, 0, 18].map((d) => <path key={d} d={`M ${cx + d} ${f - 700} L ${cx + d} ${f - 20}`} stroke="#E2D3B5" strokeWidth={4} />)}
        <rect x={cx - 50} y={f - 740} width={100} height={30} rx={6} fill="#FFFDF6" stroke={OL} strokeWidth={5} /></g>; })}
      {/* results board */}
      <g transform={`translate(${pod} ${f - 560})`}>
        <rect x={-380} y={-170} width={760} height={330} rx={18} fill="#16243F" stroke={OL} strokeWidth={8} />
        <rect x={-380} y={-170} width={760} height={64} rx={18} fill={GOLD} stroke={OL} strokeWidth={6} />
        <T x={0} y={-126} s={fit(z.board?.title || 'TODAY: 10-YEAR NOTE', 700, 36)} c={NAVY}>{z.board?.title || 'TODAY: 10-YEAR NOTE'}</T>
        {rows.filter((r) => t >= r[0]).slice(-4).map((r, k) => { const typed = r[1].slice(0, Math.floor((t - r[0]) * 40));
          return <T key={k} x={-340} y={-54 + k * 56} s={fit(r[1], 680, 36)} c="#7CF2C8" a="start" w={800}>{typed}</T>; })}
        {Array.from({length: 24}, (_, k) => <circle key={k} cx={-370 + k * 32.2} cy={150} r={5} fill={(k + Math.floor(t * 8)) % 4 === 0 ? '#FFE27A' : '#4A5874'} />)}
      </g>
      {/* podium */}
      <g transform={`translate(${pod} ${f})`}>
        <path d="M -170 0 L -140 -230 L 140 -230 L 170 0 Z" fill="#8B5A3C" stroke={OL} strokeWidth={7} strokeLinejoin="round" />
        <rect x={-190} y={-262} width={380} height={40} rx={10} fill="#A56E4A" stroke={OL} strokeWidth={6} />
        <rect x={-110} y={-190} width={220} height={70} rx={10} fill="#FFFDF4" stroke={OL} strokeWidth={4} />
        <T x={0} y={-145} s={30} c={NAVY}>AUCTION</T>
        <path d="M 120 -262 L 160 -330" stroke={OL} strokeWidth={5} /><circle cx={164} cy={-336} r={12} fill="#37474F" stroke={OL} strokeWidth={3} />
      </g>
      {/* bidder tiers (front, drawn over the floor) */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#C77D4E" />
      {Array.from({length: Math.ceil(w / 140)}, (_, k) => <rect key={'pq' + k} x={z.x0 + k * 140} y={f} width={140} height={700} fill={k % 2 ? '#B96F42' : '#C77D4E'} />)}
      <rect x={z.x0} y={f} width={w} height={20} fill="#8B5A3C" stroke={OL} strokeWidth={4} />
      {[0, 1, 2].map((r) => <g key={'tier' + r}>{Array.from({length: Math.ceil(w / 150)}, (_, k) => {
        const bx = z.x0 + 60 + k * 150 + (r % 2) * 75; if (Math.abs(bx - pod) < 260 && r === 0) return null;
        const by = f + 30 + r * 105, cls = (k + r) % 5 < 3 ? 0 : (k + r) % 5 === 3 ? 1 : 2;
        const pc = [BLUE, GREEN, RED][cls], up = bids !== undefined ? E.outBack(win(t, bids + rnd(k * 7 + r) * 1.4, 0.35)) : 0;
        const wave = up > 0 ? Math.sin(t * 9 + k) * 8 : 0;
        return <g key={k} transform={`translate(${bx} ${by})`}>
          <g transform={`translate(30 ${-40 - up * 90}) rotate(${wave})`}><path d="M 0 70 L 0 0" stroke={OL} strokeWidth={6} /><circle cx={0} cy={-18} r={28} fill={pc} stroke={OL} strokeWidth={4} />
            <T x={0} y={-10} s={20} c="#FFFFFF">{((k * 7 + r * 13) % 89) + 10}</T></g>
          <ellipse cx={0} cy={30} rx={46} ry={40} fill="#33415C" stroke={OL} strokeWidth={4} />
          <circle cx={0} cy={-26} r={30} fill={['#F2C29A', '#C98B5B', '#8A5634', '#E0A878'][(k + r) % 4]} stroke={OL} strokeWidth={4} />
          <path d="M -30 -34 Q 0 -66 30 -34" fill={['#3E2723', '#1B1B1B', '#8D5524', '#B0BEC5'][(k * 3 + r) % 4]} stroke={OL} strokeWidth={3} />
        </g>; })}</g>)}
      {sold !== undefined && t >= sold && <g transform={`translate(${pod + 380} ${f - 300}) scale(${E.outBack(win(t, sold, 0.4)) * (1 + 0.05 * Math.sin(t * 12))}) rotate(-8)`}>
        {Array.from({length: 14}, (_, k) => { const an = (k / 14) * Math.PI * 2; return <path key={k} d={`M ${Math.cos(an) * 150} ${Math.sin(an) * 90} L ${Math.cos(an) * 230} ${Math.sin(an) * 150}`} stroke={GOLD} strokeWidth={14} strokeLinecap="round" />; })}
        <ellipse rx={190} ry={100} fill={RED} stroke={OL} strokeWidth={8} /><T x={0} y={26} s={78} c="#FFFFFF" st={OL} sw={6}>{z.soldText || 'SOLD!'}</T></g>}
    </g>;
  },

  /** HOLDERS' DINING ROOM (day): wallpaper, three tall windows, a swinging chandelier, a sideboard with a stack of IOUs,
   *  a SEATING CHART easel (chart: text). The table is the `feast` item (so seated guests sit behind it). */
  dinnerparty: (t, z, f) => {
    const w = z.x1 - z.x0, cx = PX(z, z.chX, 1200);
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E8DCC4" />
      {Array.from({length: Math.ceil(w / 80)}, (_, k) => <rect key={'wp' + k} x={z.x0 + k * 80} y={-400} width={40} height={f + 400} fill="#DFD0B3" />)}
      <rect x={z.x0} y={f - 260} width={w} height={260} fill="#9C6B4E" stroke={OL} strokeWidth={5} />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'wc' + k} x={z.x0 + 20 + k * 200} y={f - 230} width={160} height={200} rx={8} fill="none" stroke="#7E5239" strokeWidth={4} />)}
      {[150, 1200, 2250].map((p, k) => windowPane(p - 130, f - 820, 260, 460, t, k))}
      {[150 / w - z.x0 / w, 2250 / w - z.x0 / w].map((p, k) => <g key={'cur' + k}>{[-1, 1].map((sd) => <path key={sd} d={`M ${z.x0 + w * p + sd * 150} ${f - 840} Q ${z.x0 + w * p + sd * (170 + 8 * Math.sin(t + k))} ${f - 600} ${z.x0 + w * p + sd * 150} ${f - 340} L ${z.x0 + w * p + sd * 120} ${f - 340} Q ${z.x0 + w * p + sd * 140} ${f - 600} ${z.x0 + w * p + sd * 120} ${f - 840} Z`} fill={RED} stroke={OL} strokeWidth={4} />)}</g>)}
      {/* chandelier */}
      <g transform={`translate(${cx} -120) rotate(${Math.sin(t * 1.4) * 3})`}>
        <path d="M 0 -400 L 0 120" stroke={OL} strokeWidth={6} />
        <path d="M -220 120 Q 0 230 220 120" fill="none" stroke={GOLD} strokeWidth={12} />
        <path d="M -220 120 Q 0 230 220 120" fill="none" stroke={OL} strokeWidth={3} />
        {[-220, -110, 0, 110, 220].map((bx, k) => <g key={k}><rect x={bx - 8} y={90 + Math.abs(bx) * -0.1 + (k === 2 ? 70 : 0)} width={16} height={34} fill="#FFFDF4" stroke={OL} strokeWidth={3} />
          <ellipse cx={bx} cy={82 + Math.abs(bx) * -0.1 + (k === 2 ? 70 : 0)} rx={9} ry={14} fill="#FFD54F" opacity={0.7 + 0.3 * Math.sin(t * 9 + k)} /></g>)}
      </g>
      {/* seating chart easel */}
      {z.chart && <g transform={`translate(${PX(z, z.easelX, 2350)} ${f}) rotate(2)`}>
        <path d="M -90 0 L -30 -420 M 90 0 L 30 -420 M 0 -420 L 0 0" stroke="#7E5239" strokeWidth={10} strokeLinecap="round" />
        <rect x={-150} y={-560} width={300} height={260} rx={8} fill="#FFFDF4" stroke={OL} strokeWidth={6} />
        <T x={0} y={-510} s={30} c={NAVY}>SEATING CHART</T>
        {String(z.chart).split('\n').map((ln, k) => <T key={k} x={0} y={-462 + k * 36} s={fit(ln, 260, 26)} w={700}>{ln}</T>)}
      </g>}
      <rect x={z.x0} y={f} width={w} height={700} fill="#7B4E36" />
      {Array.from({length: Math.ceil(w / 90)}, (_, k) => <path key={'fb' + k} d={`M ${z.x0 + k * 90} ${f} L ${z.x0 + k * 90} ${f + 700}`} stroke="#6A4230" strokeWidth={3} />)}
      <rect x={z.x0} y={f} width={w} height={16} fill="#5C3A28" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** HOLDERS' STREET (day): a row of facades for the domestic holders (shops: [[label, color]]), each with a window where a
   *  bond certificate pops at its `pops` time; leafy trees, a passing bus, pedestrians' shadows. */
  mainstreet: (t, z, f) => {
    const w = z.x1 - z.x0;
    const shops: [string, string][] = z.shops || [['MONEY MARKET FUND', '#4FB3F6'], ['HOUSEHOLDS', '#FFB74D'], ['MUTUAL FUND', '#9575CD'], ['BANK', '#7BD389'], ['CITY HALL', '#E0E0E0'], ['PENSION FUND', '#F06292'], ['INSURANCE CO.', '#4DB6AC']];
    const pops: number[] = z.pops || [];
    const gap = z.gap ?? 420, start = PX(z, z.startX, 1200 - ((shops.length - 1) * gap) / 2);
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#8EC9F2" />
      <rect x={z.x0} y={f - 900} width={w} height={500} fill="#B7DEF7" opacity={0.6} />
      {/* far hills of rooftops */}
      {Array.from({length: Math.ceil(w / 180)}, (_, k) => <rect key={'far' + k} x={z.x0 + k * 180} y={f - 620 - rnd(k) * 160} width={170} height={700} fill="#A9C6DE" />)}
      {shops.map(([lab, c], k) => { const sx = start + k * gap, house = lab === 'HOUSEHOLDS', hall = lab === 'CITY HALL', h = house ? 360 : 460 + (k % 3) * 40;
        const pu = pops[k] !== undefined ? E.outBack(win(t, pops[k], 0.5)) : 0;
        return <g key={'sh' + k} transform={`translate(${sx} ${f})`}>
          {house ? <path d={`M -180 0 L -180 -${h} L 0 -${h + 160} L 180 -${h} L 180 0 Z`} fill={c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
            : <rect x={-180} y={-h} width={360} height={h} fill={c} stroke={OL} strokeWidth={6} />}
          {hall && <g><path d={`M -200 -${h} L 0 -${h + 120} L 200 -${h} Z`} fill="#F5F5F5" stroke={OL} strokeWidth={6} />{[-120, -40, 40, 120].map((cx) => <rect key={cx} x={cx - 14} y={-h + 20} width={28} height={h - 40} fill="#FFFFFF" stroke={OL} strokeWidth={4} />)}</g>}
          {!hall && <rect x={-150} y={-h + 30} width={300} height={56} rx={10} fill="#FFFDF4" stroke={OL} strokeWidth={4} />}
          <T x={0} y={hall ? -h - 26 : -h + 70} s={fit(lab, 270, 30)} c={NAVY}>{lab}</T>
          {/* shop window with the bond on display */}
          <rect x={-130} y={-260} width={260} height={170} rx={10} fill="#CFEFFF" stroke={OL} strokeWidth={5} />
          {pu > 0 && <g transform={`translate(0 -175) scale(${pu}) rotate(${Math.sin(t * 2 + k) * 3})`}>{bond(170, 100, 'TREASURY', k)}
            {t - pops[k] < 1.2 && Array.from({length: 8}, (_, q) => { const an = (q / 8) * Math.PI * 2, r = 70 + 90 * win(t, pops[k], 1); return <path key={q} d={`M ${Math.cos(an) * r} ${Math.sin(an) * r * 0.7} l ${Math.cos(an) * 20} ${Math.sin(an) * 14}`} stroke={GOLD} strokeWidth={6} strokeLinecap="round" opacity={1 - win(t, pops[k] + 0.6, 0.6)} />; })}</g>}
          <rect x={-40} y={-80} width={80} height={80} fill="#5D4037" stroke={OL} strokeWidth={4} />
          {house && <rect x={-100} y={-h - 60} width={70} height={60} fill="#CFEFFF" stroke={OL} strokeWidth={4} />}
        </g>; })}
      {/* trees */}
      {shops.map((_, k) => { const tx = start + k * gap + gap / 2; return <g key={'tr' + k} transform={`translate(${tx} ${f}) rotate(${Math.sin(t * 1.3 + k) * 1.5})`}>
        <rect x={-10} y={-160} width={20} height={160} fill="#7B4E36" stroke={OL} strokeWidth={4} />
        <circle cx={0} cy={-200} r={70} fill="#5DBB63" stroke={OL} strokeWidth={5} /><circle cx={-36} cy={-170} r={44} fill="#66C46C" stroke={OL} strokeWidth={4} /></g>; })}
      {/* sidewalk + road + bus */}
      <rect x={z.x0} y={f} width={w} height={60} fill="#D9D4C7" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 60} width={w} height={700} fill="#6E7685" />
      {Array.from({length: Math.ceil(w / 220)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 220} y={f + 160} width={120} height={10} fill="#FFFFFF" opacity={0.7} />)}
      {(() => { const bx = z.x0 - 700 + ((t * 260) % (w + 1400)); return <g transform={`translate(${bx} ${f + 140})`}>
        <rect x={-260} y={-150} width={520} height={150} rx={30} fill={GOLD} stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3, 4].map((q) => <rect key={q} x={-230 + q * 92} y={-128} width={72} height={56} rx={8} fill="#CFEFFF" stroke={OL} strokeWidth={3} />)}
        {[-170, 170].map((wx) => <g key={wx} transform={`translate(${wx} 0) rotate(${t * 300})`}><circle r={30} fill="#263238" stroke={OL} strokeWidth={4} /><path d="M -14 0 L 14 0" stroke="#90A4AE" strokeWidth={4} /></g>)}</g>; })()}
    </g>;
  },

  /** THE FED'S BALANCE-SHEET WAREHOUSE: tall steel shelving (bays) of bond crates; `level` [[t, 0..1]] = how full the shelves
   *  are (crates pop in/out from the top as it changes); a big HOLDINGS gauge (gauge: [[t, trillions]], max gaugeMax);
   *  `billsAt`: small yellow BILL crates ride a floor conveyor; roll-up doors with daylight. */
  fedwarehouse: (t, z, f) => {
    const w = z.x1 - z.x0, lvl = clamp(kf(z.level, t, 0.8)), bays = z.bays ?? 5, bw = 300, rowsN = 5, start = PX(z, z.shelfX, 1200 - (bays * (bw + 40)) / 2);
    const g = kf(z.gauge, t, 4.6), gmax = z.gaugeMax ?? 6;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#D5DCE5" />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <path key={'tr' + k} d={`M ${z.x0 + k * 300} -300 L ${z.x0 + k * 300 + 150} -150 L ${z.x0 + k * 300 + 300} -300`} stroke="#AAB6C5" strokeWidth={10} fill="none" />)}
      {[start - 300, start + bays * (bw + 40) + 260].map((dx0, k) => { const dx = dx0; return <g key={'dr' + k}><rect x={dx - 150} y={f - 420} width={300} height={420} fill="#BFE6FF" stroke={OL} strokeWidth={6} />
        <rect x={dx - 150} y={f - 420} width={300} height={140} fill="#9AA7B8" stroke={OL} strokeWidth={5} />{[0, 1, 2, 3].map((q) => <path key={q} d={`M ${dx - 150} ${f - 400 + q * 32} L ${dx + 150} ${f - 400 + q * 32}`} stroke={OL} strokeWidth={2} opacity={0.5} />)}</g>; })}
      {/* shelving bays */}
      {Array.from({length: bays}, (_, b) => { const bx = start + b * (bw + 40); return <g key={'bay' + b}>
        <rect x={bx} y={f - 700} width={bw} height={700} fill="none" stroke="#3D5A80" strokeWidth={10} />
        {Array.from({length: rowsN}, (_, r) => <g key={r}><rect x={bx} y={f - 700 + r * 140 + 126} width={bw} height={14} fill="#F2994A" stroke={OL} strokeWidth={3} />
          {Array.from({length: 3}, (_, c) => { const idx = b * rowsN * 3 + (rowsN - 1 - r) * 3 + c, frac = (idx + 0.5) / (bays * rowsN * 3), filled = frac < lvl;
            const app = filled ? clamp((lvl - frac) * bays * rowsN * 3 * 0.6) : 0; if (app <= 0) return null;
            const lab = (idx * 7) % 5 === 0 ? 'BILLS' : (idx * 3) % 4 === 0 ? 'T-BOND' : 'T-NOTE';
            return <g key={c} transform={`translate(${bx + 52 + c * 98} ${f - 700 + r * 140 + 126}) scale(${E.outBack(app)})`}>
              <rect x={-44} y={-104} width={88} height={104} rx={6} fill={lab === 'BILLS' ? '#FFD54F' : lab === 'T-BOND' ? '#C8A26B' : '#D9B98A'} stroke={OL} strokeWidth={4} />
              <path d="M -44 -70 L 44 -70" stroke={OL} strokeWidth={2} opacity={0.4} /><T x={0} y={-36} s={17}>{lab}</T></g>; })}</g>)}
      </g>; })}
      <rect x={start - 20} y={f - 790} width={bays * (bw + 40)} height={64} rx={12} fill={NAVY} stroke={OL} strokeWidth={5} />
      <T x={start - 20 + (bays * (bw + 40)) / 2} y={f - 745} s={36} c="#FFE27A" ls={3}>{z.banner || 'FEDERAL RESERVE · BALANCE SHEET'}</T>
      {/* gauge */}
      {z.gauge !== undefined && <g transform={`translate(${PX(z, z.gaugeX, start + bays * (bw + 40) + 240)} ${z.gaugeY ?? 200})`}>
        <circle r={170} fill="#FFFDF4" stroke={OL} strokeWidth={8} />
        {Array.from({length: 13}, (_, k) => { const an = Math.PI * (0.75 + k * 0.125); return <path key={k} d={`M ${Math.cos(an) * 140} ${Math.sin(an) * 140} L ${Math.cos(an) * 160} ${Math.sin(an) * 160}`} stroke={OL} strokeWidth={k % 2 ? 3 : 6} />; })}
        <path d={`M ${Math.cos(Math.PI * 0.75) * 120} ${Math.sin(Math.PI * 0.75) * 120} A 120 120 0 1 1 ${Math.cos(Math.PI * 2.25) * 120} ${Math.sin(Math.PI * 2.25) * 120}`} fill="none" stroke={GREEN} strokeWidth={14} opacity={0.4} />
        <g transform={`rotate(${135 + 270 * clamp(g / gmax) + Math.sin(t * 13) * 0.8})`}><path d="M -10 0 L 130 0" stroke={RED} strokeWidth={10} strokeLinecap="round" /></g>
        <circle r={18} fill={OL} />
        <rect x={-120} y={50} width={240} height={64} rx={12} fill={NAVY} stroke={OL} strokeWidth={4} /><T x={0} y={96} s={40} c="#FFE27A">${g.toFixed(2)}T</T>
        <T x={0} y={-60} s={22} c={NAVY}>TREASURIES HELD</T>
      </g>}
      {/* floor + conveyor of bills */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#A9B3C1" />
      <rect x={z.x0} y={f} width={w} height={16} fill="#C5CDD8" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'st' + k} d={`M ${z.x0 + k * 200} ${f + 60} L ${z.x0 + k * 200 + 100} ${f + 60}`} stroke={GOLD} strokeWidth={10} />)}
      {z.billsAt !== undefined && t >= z.billsAt && <g>
        <rect x={z.x0} y={f + 110} width={w} height={30} rx={15} fill="#4A5874" stroke={OL} strokeWidth={4} />
        {Array.from({length: 10}, (_, k) => { const u = ((t - z.billsAt) * 0.12 + k / 10) % 1; return <g key={k} transform={`translate(${z.x0 + u * w} ${f + 108}) scale(${pop(t, z.billsAt + k * 0.15, 0.4)})`}>
          <rect x={-40} y={-56} width={80} height={56} rx={5} fill="#FFD54F" stroke={OL} strokeWidth={4} /><T x={0} y={-20} s={18}>BILLS</T></g>; })}</g>}
    </g>;
  },

  /** SOCIAL SECURITY TRUST FUND RECORDS ROOM (day): a giant 5-drawer filing cabinet (cabX) whose drawer `openAt` slides out to
   *  show IOU folders; `fill` [[t, 0..1]] = how full the open drawer is (folders vanish as it empties); a pneumatic tube
   *  from the cabinet to a "TREASURY" hatch with IOU capsules flying at tubeAt; a wall clock; a desk plant. */
  trustcabinet: (t, z, f) => {
    const w = z.x1 - z.x0, cx = PX(z, z.cabX, 1000), open = z.openAt !== undefined ? E.outBack(win(t, z.openAt, 0.7)) : (z.open ?? 0);
    const fill = clamp(kf(z.fill, t, 1)), nF = 14;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#DCE8E2" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'ws' + k} d={`M ${z.x0 + k * 120} -400 L ${z.x0 + k * 120} ${f}`} stroke="#CDDCD5" strokeWidth={10} />)}
      {windowPane(cx - 900, f - 760, 300, 420, t, 1)}
      {windowPane(cx + 640, f - 900, 260, 360, t, 2)}
      {/* wall clock */}
      <g transform={`translate(${PX(z, z.clockX, cx + 470)} ${f - 720})`}><circle r={70} fill="#FFFDF4" stroke={OL} strokeWidth={7} />
        <path d={`M 0 0 L ${Math.cos(t * 2) * 50} ${Math.sin(t * 2) * 50}`} stroke={OL} strokeWidth={6} strokeLinecap="round" /><path d={`M 0 0 L ${Math.cos(t * 0.2) * 32} ${Math.sin(t * 0.2) * 32}`} stroke={RED} strokeWidth={8} strokeLinecap="round" /></g>
      {/* the cabinet */}
      <g transform={`translate(${cx} ${f})`}>
        <rect x={-260} y={-820} width={520} height={820} rx={16} fill="#8FA8BF" stroke={OL} strokeWidth={8} />
        <rect x={-280} y={-860} width={560} height={60} rx={12} fill="#6E8AA6" stroke={OL} strokeWidth={6} />
        <T x={0} y={-818} s={28} c="#FFFFFF" ls={2}>{z.label || 'SOCIAL SECURITY TRUST FUNDS'}</T>
        {[0, 1, 2, 3, 4].map((d) => { const isOpen = d === (z.drawer ?? 2), dy = -780 + d * 154, out = isOpen ? open : 0;
          return <g key={d}>
            {isOpen && out > 0 && <g transform={`translate(0 ${dy + 70})`}>
              <path d={`M -230 0 L 230 0 L ${230 + 90 * out} ${110 * out} L ${-230 - 90 * out} ${110 * out} Z`} fill="#5F7891" stroke={OL} strokeWidth={5} />
              {Array.from({length: nF}, (_, q) => { const vis = (q + 0.5) / nF < fill; if (!vis) return null; const fx = -220 + q * (440 / nF) + 14;
                return <g key={q} transform={`translate(${fx * (1 + 0.35 * out)} ${-10 + 60 * out}) rotate(${-8 + (q % 3) * 6})`}>
                  <rect x={-14} y={-80} width={28} height={84} rx={3} fill={q % 2 ? '#FFE9A8' : '#FFF8E6'} stroke={OL} strokeWidth={3} />
                  <rect x={-14} y={-92} width={18} height={14} rx={3} fill={q % 3 ? GREEN : BLUE} stroke={OL} strokeWidth={2} /></g>; })}
              <T x={0} y={-96 + 40 * out} s={24} c={NAVY} o={out}>IOU · IOU · IOU</T>
            </g>}
            <g transform={`translate(0 ${out * 120}) scale(${1 + out * 0.35})`}>
              <rect x={-240} y={dy} width={480} height={140} rx={10} fill={isOpen ? '#A6BCD1' : '#9DB4C9'} stroke={OL} strokeWidth={6} />
              <rect x={-60} y={dy + 30} width={120} height={34} rx={8} fill="#FFFDF4" stroke={OL} strokeWidth={4} />
              <T x={0} y={dy + 55} s={18}>{['1940s', 'OASI', 'IOUs', 'DI', 'MISC.'][d]}</T>
              <rect x={-50} y={dy + 86} width={100} height={18} rx={9} fill="#5A6E85" stroke={OL} strokeWidth={4} /></g>
          </g>; })}
      </g>
      {/* pneumatic tube */}
      {z.tubeAt !== undefined && <g>
        <path d={`M ${cx + 260} ${f - 700} Q ${cx + 600} ${f - 980} ${(cx + 1050)} ${f - 300}`} fill="none" stroke="#B0BEC5" strokeWidth={56} opacity={0.8} />
        <path d={`M ${cx + 260} ${f - 700} Q ${cx + 600} ${f - 980} ${(cx + 1050)} ${f - 300}`} fill="none" stroke={OL} strokeWidth={6} strokeDasharray="1 0" opacity={0.25} />
        <g transform={`translate(${(cx + 1050)} ${f - 300})`}><rect x={-110} y={-20} width={220} height={240} rx={14} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={40} s={30} c="#FFE27A">TREASURY</T>
          <rect x={-60} y={80} width={120} height={60} rx={8} fill="#2B3E63" stroke={OL} strokeWidth={4} /></g>
        {t >= z.tubeAt && Array.from({length: 4}, (_, k) => { const u = ((t - z.tubeAt) * 0.6 + k / 4) % 1, p0x = cx + 260, p0y = f - 700, c1x = cx + 600, c1y = f - 980, p2x = (cx + 1050), p2y = f - 300;
          const qx = (1 - u) * (1 - u) * p0x + 2 * (1 - u) * u * c1x + u * u * p2x, qy = (1 - u) * (1 - u) * p0y + 2 * (1 - u) * u * c1y + u * u * p2y;
          return <g key={k} transform={`translate(${qx} ${qy}) rotate(${u * 160 - 40})`}>{note(70, 38, 'IOU', PAPER, k)}</g>; })}
      </g>}
      {/* floor + desk */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B9A587" />
      {Array.from({length: Math.ceil(w / 110)}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 110} ${f} L ${z.x0 + k * 110} ${f + 700}`} stroke="#A8957A" strokeWidth={3} />)}
      <rect x={z.x0} y={f} width={w} height={16} fill="#8E7B60" stroke={OL} strokeWidth={4} />
      <g transform={`translate(${cx - 640} ${f})`}><rect x={-160} y={-200} width={320} height={30} rx={6} fill="#A56E4A" stroke={OL} strokeWidth={5} />
        {[-140, 120].map((lx) => <rect key={lx} x={lx} y={-170} width={20} height={170} fill="#8B5A3C" stroke={OL} strokeWidth={4} />)}
        <g transform="translate(110 -200)"><rect x={-26} y={-50} width={52} height={50} rx={6} fill={RED} stroke={OL} strokeWidth={4} />
          {[-1, 0, 1].map((q) => <ellipse key={q} cx={q * 16} cy={-80 + Math.abs(q) * 10} rx={12} ry={30} fill="#5DBB63" stroke={OL} strokeWidth={3} transform={`rotate(${q * 25 + Math.sin(t * 2 + q) * 4} ${q * 16} -50)`} />)}</g>
        <g transform="translate(-60 -200)">{[0, 1, 2].map((q) => <rect key={q} x={-60} y={-14 - q * 12} width={120} height={12} fill="#FFF8E6" stroke={OL} strokeWidth={2} />)}</g></g>
    </g>;
  },

  /** INTEREST METER vs DEFENSE SCALE (a bright civic hall): left, a giant taxi-style meter (meter: [[t, billions]] -> "$1,052B",
   *  label meterLabel) with spinning wheels and a flag that pops at flagAt; right, a balance scale (scaleX) with two pans
   *  (left/right: {label, sub, at}) that tips toward the heavier pan at tipAt (tip: -1..1). */
  meterscale: (t, z, f) => {
    const w = z.x1 - z.x0, mx = PX(z, z.meterX, 640), sx = PX(z, z.scaleX, 1700);
    const mv = kf(z.meter, t, 0), mtxt = '$' + Math.round(mv).toLocaleString('en-US') + (z.meterUnit ?? 'B');
    const tip = z.tipAt !== undefined ? (z.tip ?? 0.25) * E.outBack(win(t, z.tipAt, 1.0)) + jig(t, z.tipAt + 0.9, 10, 3) * 0.03 : 0;
    const L = z.left, R = z.right, ang = tip * 18, arm = 360;
    const panY = (sd: number) => Math.sin((ang * Math.PI) / 180) * arm * sd;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#CFE6F7" />
      <rect x={z.x0} y={f - 420} width={w} height={420} fill="#E9F1F8" />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <g key={'col' + k}><rect x={z.x0 + 40 + k * 260} y={f - 640} width={44} height={640} fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.9} /></g>)}
      <rect x={z.x0} y={f - 680} width={w} height={44} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
      {/* meter */}
      <g transform={`translate(${mx} ${f})`}>
        <rect x={-30} y={-260} width={60} height={260} fill="#455A64" stroke={OL} strokeWidth={6} />
        <g transform={`translate(0 -500) rotate(${Math.sin(t * 7) * 0.6})`}>
          <rect x={-330} y={-230} width={660} height={420} rx={40} fill="#F2B63A" stroke={OL} strokeWidth={9} />
          <rect x={-290} y={-196} width={580} height={70} rx={14} fill={NAVY} stroke={OL} strokeWidth={5} />
          <T x={0} y={-148} s={fit(z.meterLabel || 'NET INTEREST', 540, 40)} c="#FFE27A" ls={2}>{z.meterLabel || 'NET INTEREST'}</T>
          <g transform="translate(0 -20)">{odometer(mtxt, t, 62, 100)}</g>
          {[-200, 0, 200].map((wx, k) => <g key={k} transform={`translate(${wx} 120) rotate(${t * (200 + k * 90)})`}><circle r={34} fill="#FFFDF4" stroke={OL} strokeWidth={5} /><path d="M -30 0 L 30 0 M 0 -30 L 0 30" stroke={OL} strokeWidth={4} /></g>)}
          {/* flag */}
          <g transform={`translate(300 -230) rotate(${z.flagAt !== undefined ? -90 * E.outBack(win(t, z.flagAt, 0.5)) : 0})`}>
            <rect x={-8} y={-160} width={16} height={160} fill="#455A64" stroke={OL} strokeWidth={3} />
            <rect x={-8} y={-160} width={130} height={70} rx={6} fill={RED} stroke={OL} strokeWidth={4} /><T x={57} y={-114} s={26} c="#FFFFFF">{z.flagText || 'RUNNING'}</T></g>
        </g>
        {Array.from({length: 5}, (_, k) => { const u = (t * 0.9 + k / 5) % 1; return <g key={'cn' + k} transform={`translate(${340 + u * 140} ${-560 - u * 220}) scale(${1 - u * 0.4})`} opacity={1 - u}>
          <circle r={22} fill={GOLD} stroke={OL} strokeWidth={4} /><T x={0} y={9} s={24} c="#7A5200">$</T></g>; })}
      </g>
      {/* balance scale */}
      <g transform={`translate(${sx} ${f})`}>
        <path d="M -150 0 L -60 -40 L 60 -40 L 150 0 Z" fill="#8B5A3C" stroke={OL} strokeWidth={6} />
        <rect x={-22} y={-560} width={44} height={530} fill="#C9A36B" stroke={OL} strokeWidth={6} />
        <circle cx={0} cy={-580} r={34} fill={GOLD} stroke={OL} strokeWidth={6} />
        <g transform={`translate(0 -560) rotate(${ang})`}><rect x={-arm - 20} y={-14} width={2 * arm + 40} height={28} rx={14} fill="#C9A36B" stroke={OL} strokeWidth={6} /></g>
        {[-1, 1].map((sd) => { const P = sd < 0 ? L : R, px = sd * Math.cos((ang * Math.PI) / 180) * arm, py = -560 + panY(sd), app = P ? pop(t, P.at ?? 0, 0.5) : 0;
          return <g key={sd} transform={`translate(${px} ${py})`}>
            <path d="M 0 0 L -140 260 M 0 0 L 140 260" stroke={OL} strokeWidth={4} />
            <path d="M -170 260 Q 0 330 170 260 Z" fill="#E0B872" stroke={OL} strokeWidth={6} />
            {app > 0 && <g transform={`translate(0 252) scale(${app})`}>
              <path d="M -120 0 Q -130 -150 -40 -170 L 40 -170 Q 130 -150 120 0 Z" fill={P.color || (sd < 0 ? '#7E8FA6' : RED)} stroke={OL} strokeWidth={6} />
              <path d="M -50 -170 Q 0 -210 50 -170" fill="none" stroke={OL} strokeWidth={6} />
              <T x={0} y={-96} s={fit(P.label || '', 220, 32)} c="#FFFFFF" st={OL} sw={5}>{P.label}</T>
              {P.sub && <T x={0} y={-52} s={fit(P.sub, 220, 28)} c="#FFE27A" st={OL} sw={4}>{P.sub}</T>}</g>}
          </g>; })}
      </g>
      <rect x={z.x0} y={f} width={w} height={700} fill="#B8C7D6" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <rect key={'tl' + k} x={z.x0 + k * 200} y={f} width={100} height={700} fill="#AFBFCF" />)}
      <rect x={z.x0} y={f} width={w} height={18} fill="#97A9BC" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** SHOW TITLE CARD (screen-filling, static camera): a giant IOU note unrolls over a money-green sunburst; title words drop
   *  in letter by letter with squash; a ribbon subtitle; a typed joke subtitle (subs: [[t, text]]). */
  debttitle: (t, z, f) => {
    const cx = 960, cy = 480, title: string = z.title || 'WHO OWNS THE DEBT?', sub: string = z.sub || 'A HIDDEN ECONOMICS EPISODE';
    const subs: [number, string][] = (z.subs || []).map((p: any) => [Number(p[0]), String(p[1])]);
    const cur = subs.filter((p) => t >= p[0]).pop(), typed = cur ? cur[1].slice(0, Math.floor((t - cur[0]) * 32)) : '';
    const unroll = E.out(win(t, 0.1, 0.9));
    const words = title.split(' '), lines: string[] = [];
    words.forEach((wd) => { if (lines.length && (lines[lines.length - 1] + ' ' + wd).length <= (z.lineLen ?? 11)) lines[lines.length - 1] += ' ' + wd; else lines.push(wd); });
    const fs = Math.min(150, 1300 / Math.max(...lines.map((l) => l.length)) / 0.62);
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#1F6B4A" />
      <g transform={`translate(${cx} ${cy}) rotate(${t * 10})`}>{Array.from({length: 28}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos((k / 28) * Math.PI * 2) * 2600} ${Math.sin((k / 28) * Math.PI * 2) * 2600} L ${Math.cos(((k + 0.5) / 28) * Math.PI * 2) * 2600} ${Math.sin(((k + 0.5) / 28) * Math.PI * 2) * 2600} Z`} fill={k % 2 ? '#2A8A60' : '#F2B63A'} opacity={k % 2 ? 1 : 0.9} />)}</g>
      {/* the IOU paper */}
      <g transform={`translate(${cx} ${cy}) rotate(${-2 + Math.sin(t * 1.6) * 1})`}>
        <rect x={-760 * unroll} y={-330} width={1520 * unroll} height={640} rx={26} fill={PAPER} stroke={OL} strokeWidth={12} />
        {unroll > 0.95 && <rect x={-720} y={-292} width={1440} height={564} rx={18} fill="none" stroke={GREEN} strokeWidth={8} strokeDasharray="30 12" />}
        {[-1, 1].map((sd) => <g key={sd} transform={`translate(${sd * 760 * unroll} 0)`}><rect x={-34} y={-350} width={68} height={680} rx={34} fill="#E9D9A8" stroke={OL} strokeWidth={10} /></g>)}
        <g transform={`translate(0 -250) scale(${pop(t, 0.6, 0.5)})`}><rect x={-380} y={-36} width={760} height={60} rx={30} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={8} s={26} c="#FFE27A" ls={3}>{z.kicker || 'THE HIDDEN ECONOMICS PRESENTS'}</T></g>
        {lines.map((ln, li) => <g key={li} transform={`translate(0 ${-110 + li * fs * 1.05 + (lines.length < 3 ? 60 : 0)})`}>{ln.split('').map((ch, k) => {
          const st = 0.9 + li * 0.3 + k * 0.05, u = E.outBack(win(t, st, 0.45)), sq = 1 + 0.25 * jig(t, st + 0.3, 20, 8), cw = fs * 0.66;
          const x = (k - (ln.length - 1) / 2) * cw, wob = Math.sin(t * 4 + k * 0.7 + li) * 5;
          return <g key={k} transform={`translate(${x} ${wob - (1 - u) * 260}) scale(${u * (2 - sq)} ${u * sq})`}>
            <T x={8} y={10} s={fs} c={OL}>{ch}</T><T x={0} y={0} s={fs} c={li === lines.length - 1 ? RED : GREEN} st={OL} sw={fs * 0.09}>{ch}</T></g>; })}</g>)}
        <g transform={`translate(0 248) scale(${pop(t, 2.0, 0.45)})`}><path d="M -420 -40 L 420 -40 L 390 0 L 420 40 L -420 40 L -390 0 Z" fill={GOLD} stroke={OL} strokeWidth={7} strokeLinejoin="round" /><T x={0} y={14} s={fit(sub, 760, 40)} c={NAVY}>{sub}</T></g>
      </g>
      {cur && <g transform="translate(960 1010)"><rect x={-760} y={-40} width={1520} height={70} rx={14} fill="#0B2A1E" opacity={0.88} />
        <T x={0} y={8} s={fit(cur[1], 1460, 34)} c="#FFE27A" w={800}>{typed}{Math.floor(t * 3) % 2 ? '▌' : ' '}</T></g>}
    </g>;
  },

  /** ACT BUMPER (screen-filling, static camera): green banknote stripes wipe in, a rubber stamp slams the act number on an
   *  IOU card, the act title drops in, a rotating joke caption types on. */
  debtbumper: (t, z, f) => {
    const act: string = z.act || 'ACT ONE', title: string = z.title || '', cap: string = z.caption || '', c2 = z.color || GREEN;
    const wipe = E.out(win(t, 0, 0.4)), slam = t < 0.55 ? lerp(-600, 0, E.in(win(t, 0.2, 0.35))) : lerp(0, -420, E.out(win(t, 0.75, 0.5)));
    const hit = t >= 0.55, sh = hit ? jig(t, 0.55, 30, 7) * 18 : 0;
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill={c2} />
      <g transform={`translate(${(1 - wipe) * -2600} 0)`}>{Array.from({length: 16}, (_, k) => <path key={k} d={`M ${-400 + k * 220} -200 L ${-200 + k * 220} -200 L ${-700 + k * 220} 1300 L ${-900 + k * 220} 1300 Z`} fill="#FFFFFF" opacity={0.1} />)}</g>
      <g transform={`translate(${960 + sh} 430) rotate(${-4 + sh * 0.1})`}>
        <rect x={-430} y={-210} width={860} height={420} rx={26} fill={PAPER} stroke={OL} strokeWidth={10} />
        <rect x={-396} y={-176} width={792} height={352} rx={16} fill="none" stroke={GREEN} strokeWidth={6} strokeDasharray="24 10" />
        <T x={-200} y={40} s={190} c={GREEN} st={OL} sw={10}>IOU</T>
        {hit && <g transform={`translate(210 10) rotate(-12) scale(${E.outBack(win(t, 0.55, 0.3))})`}>
          <circle r={150} fill="none" stroke={RED} strokeWidth={16} /><circle r={122} fill="none" stroke={RED} strokeWidth={5} />
          <T x={0} y={-40} s={36} c={RED}>{act}</T><T x={0} y={60} s={120} c={RED}>{z.num || '1'}</T></g>}
        {/* the stamp */}
        <g transform={`translate(210 ${slam - 10})`}><rect x={-110} y={-170} width={220} height={60} rx={10} fill={RED} stroke={OL} strokeWidth={6} />
          <rect x={-30} y={-300} width={60} height={140} rx={10} fill="#8B5A3C" stroke={OL} strokeWidth={6} /><ellipse cx={0} cy={-310} rx={70} ry={34} fill="#A56E4A" stroke={OL} strokeWidth={6} /></g>
      </g>
      <g opacity={t < 0.8 ? 0 : 1} transform={`translate(960 ${790 - (1 - E.outBack(win(t, 0.8, 0.5))) * 500})`}><T x={6} y={10} s={fit(title, 1600, 92)} c={OL}>{title}</T><T x={0} y={0} s={fit(title, 1600, 92)} c="#FFFFFF" st={OL} sw={9}>{title}</T></g>
      {cap && t > 1.2 && <g transform="translate(960 900)"><rect x={-640} y={-40} width={1280} height={70} rx={35} fill={NAVY} opacity={0.85} />
        <T x={0} y={8} s={fit(cap, 1200, 36)} c="#FFE27A" w={800}>{cap.slice(0, Math.floor((t - 1.2) * 34))}</T></g>}
    </g>;
  },
};

/* =============================================================================================== ITEMS */
/** OWEN, a living IOU note (the running gag): paper body with "IOU" and an amount (`amount`, or `amounts` [[t, text]]),
 *  cartoon eyes and mouth (face: happy, grin, shock, worry, smug, sweat), stick arms and legs that walk/run with x keyframes,
 *  `grow` [[t, scale]] makes him swell (with a boing), `hops` [t...], `wave` true waves an arm. Origin at the feet. */
const owen: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08;
  const g = kf(a.grow, t, 1) * (a.scale ?? 1), app = pop(t, at, 0.4);
  const growing = Array.isArray(a.grow) && a.grow.some((p: any) => t >= p[0] && t < p[0] + 0.6);
  const boing = Array.isArray(a.grow) ? a.grow.reduce((s: number, p: any) => s + jig(t, p[0], 18, 5) * 0.12, 0) : 0;
  const moving = Math.abs(vx) > 30, run = Math.abs(vx) > 320, cyc = t * (run ? 15 : 8.5) + i, sw = Math.sin(cyc);
  let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.55) hy += Math.sin((u / 0.55) * Math.PI) * 110; }
  const face: string = pick(a.faces, t, a.face || 'happy');
  const amount: string = pick(a.amounts, t, a.amount || '$40.6T');
  const fl = a.flip !== undefined ? (a.flip ? -1 : 1) : vx < -30 ? -1 : 1;
  const W = 220, H = 150, by = -110 - H / 2, bob = moving ? Math.abs(Math.cos(cyc)) * 10 : Math.sin(t * 2.4 + i) * 3;
  const legA = moving ? (run ? 40 : 24) * sw : 0;
  const leg = (sd: number) => { const an = ((sd > 0 ? legA : -legA) * Math.PI) / 180, kx = sd * 36 + Math.sin(an) * 50, ky = -60 + Math.cos(an) * 50 - 50;
    return <g key={'lg' + sd}><path d={`M ${sd * 40} ${by + H / 2 - 6} L ${kx} ${-8}`} stroke={OL} strokeWidth={9} strokeLinecap="round" />
      <ellipse cx={kx + 12} cy={-6} rx={22} ry={11} fill="#33415C" stroke={OL} strokeWidth={4} /></g>; };
  const armAng = (sd: number) => a.wave && sd > 0 ? -150 + 30 * Math.sin(t * 12) : face === 'shock' ? -140 * (sd > 0 ? 1 : 1) : moving ? 30 * sw * sd : 20;
  const arm = (sd: number) => { const an = (armAng(sd) * Math.PI) / 180, hx = sd * (W / 2 + 10) + sd * Math.sin(-an) * -60 * 0 + Math.cos(an) * 0, ax = sd * (W / 2 - 4), ay = by + 10;
    const ex = ax + sd * Math.sin(Math.abs(an)) * 70, ey = ay + Math.cos(an) * 70; void hx;
    return <g key={'ar' + sd}><path d={`M ${ax} ${ay} L ${ex} ${ey}`} stroke={OL} strokeWidth={9} strokeLinecap="round" /><circle cx={ex} cy={ey} r={13} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>; };
  const eyeY = by - 18, sh = face === 'shock' ? 1.5 : 1, blink = ((t + i * 0.7) % 3.1) < 0.12;
  const eye = (ex: number) => blink ? <path key={ex} d={`M ${ex - 14} ${eyeY} Q ${ex} ${eyeY + 6} ${ex + 14} ${eyeY}`} stroke={OL} strokeWidth={4} fill="none" />
    : <g key={ex}><ellipse cx={ex} cy={eyeY} rx={15 * sh} ry={18 * sh} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={ex + 3} cy={eyeY + 2} r={face === 'shock' ? 4 : 7} fill={OL} />
      {face === 'smug' && <path d={`M ${ex - 16} ${eyeY - 4} L ${ex + 16} ${eyeY - 4} L ${ex + 16} ${eyeY - 20} L ${ex - 16} ${eyeY - 20} Z`} fill={PAPER} stroke={OL} strokeWidth={3} />}</g>;
  const my = by + 22;
  const mouth = face === 'shock' ? <ellipse cx={0} cy={my + 10} rx={14} ry={18 + 4 * Math.sin(t * 9)} fill="#6B2E2A" stroke={OL} strokeWidth={4} />
    : face === 'worry' || face === 'sweat' ? <path d={`M -16 ${my + 10} Q 0 ${my - 2} 16 ${my + 10}`} fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
    : face === 'grin' ? <path d={`M -24 ${my} Q 0 ${my + 4} 24 ${my} Q 20 ${my + 24} 0 ${my + 24} Q -20 ${my + 24} -24 ${my} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
    : face === 'smug' ? <path d={`M -14 ${my + 6} Q 6 ${my + 10} 20 ${my - 4}`} fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
    : <path d={`M -18 ${my} Q 0 ${my + 18} 18 ${my}`} fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />;
  const lab: string | null = a.label && t < (a.labelUntil ?? at + 4) ? String(a.label) : null;
  return <g key={'owen' + i} transform={`translate(${x} ${y - bob - hy}) scale(${g * app * fl * (1 + boing)} ${g * app * (1 - boing)})`}>
    <ellipse cx={0} cy={4} rx={110} ry={14} fill={OL} opacity={0.18} />
    {leg(-1)}{leg(1)}
    {arm(-1)}
    <g transform={`rotate(${moving ? 4 * Math.sin(cyc * 0.5) : Math.sin(t * 1.7 + i) * 2} 0 ${by})`}>
      <rect x={-W / 2} y={by - H / 2} width={W} height={H} rx={14} fill={PAPER} stroke={OL} strokeWidth={6} />
      <rect x={-W / 2 + 10} y={by - H / 2 + 10} width={W - 20} height={H - 20} rx={8} fill="none" stroke={GREEN} strokeWidth={3} strokeDasharray="12 6" />
      <path d={`M ${W / 2 - 34} ${by - H / 2} L ${W / 2} ${by - H / 2 + 34}`} stroke={OL} strokeWidth={4} />
      <path d={`M ${W / 2 - 34} ${by - H / 2} L ${W / 2 - 34} ${by - H / 2 + 34} L ${W / 2} ${by - H / 2 + 34}`} fill="#EADBB4" stroke={OL} strokeWidth={4} />
      <T x={-62} y={by - H / 2 + 34} s={26} c={GREEN}>IOU</T>
      {eye(-26)}{eye(26)}
      {mouth}
      <rect x={-W / 2 + 20} y={by + H / 2 - 40} width={W - 40} height={32} rx={8} fill={growing ? '#FFE27A' : '#FFFFFF'} stroke={OL} strokeWidth={3} />
      <T x={0} y={by + H / 2 - 16} s={fit(amount, W - 50, 24)} c={RED}>{amount}</T>
      {(face === 'sweat' || face === 'worry') && [0, 1].map((k) => { const u = (t * 1.3 + k * 0.5) % 1; return <path key={'sw' + k} d={`M ${W / 2 - 10 + k * 8} ${by - 40 + u * 60} q 8 12 0 18 q -8 -6 0 -18`} fill="#7FD1FF" stroke={OL} strokeWidth={2} opacity={1 - u} />; })}
    </g>
    {arm(1)}
    {lab && <g transform={`translate(0 ${by - H / 2 - 50}) scale(${fl} 1) scale(${pop(t, at + 0.2, 0.4)})`}>
      <rect x={-lab.length * 9 - 18} y={-26} width={lab.length * 18 + 36} height={40} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={2} s={22}>{lab}</T></g>}
  </g>;
};

/** FEAST: the holders' dinner table (front edge at y, default f-60): white cloth, `guests` [{x, label, value, at, color}],
 *  each with a plate whose bond-pancake stack height follows value (vmax) and pops at `at`; place cards with the label and an
 *  optional display figure; `shrink` {idx, at, to} animates one stack down (a shrinking plate). No flags. */
const feast: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const x0 = a.x0 ?? 200, x1 = a.x1 ?? 2200, y = a.y ?? f - 40, vmax = a.vmax ?? 1400, app = E.out(win(t, at, 0.5));
  const guests: any[] = a.guests || [];
  return <g key={'feast' + i} opacity={app}>
    <rect x={x0} y={y - 70} width={x1 - x0} height={170} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    <path d={`M ${x0} ${y - 70} L ${x1} ${y - 70}`} stroke="#E6E1D6" strokeWidth={14} />
    {Array.from({length: Math.ceil((x1 - x0) / 60)}, (_, k) => <path key={'sc' + k} d={`M ${x0 + k * 60 + 30} ${y + 100} q 15 14 30 0`} fill="none" stroke="#D9D2C2" strokeWidth={4} />)}
    {(a.candles || [0.25, 0.5, 0.75]).map((p: number, k: number) => { const cx = p > 1 ? p : x0 + (x1 - x0) * p; if (guests.some((g) => Math.abs((g.x ?? 0) - cx) < 110)) return null; return <g key={'cd' + k} transform={`translate(${cx} ${y - 70})`}>
      <rect x={-8} y={-90} width={16} height={90} fill="#FFFDF4" stroke={OL} strokeWidth={3} /><ellipse cx={0} cy={-100} rx={8 + Math.sin(t * 11 + k)} ry={16} fill="#FFD54F" opacity={0.9} /></g>; })}
    {guests.map((g, k) => { const gat = g.at ?? at, u = E.outBack(win(t, gat, 0.5)); let v = g.value ?? 0;
      if (a.shrink && a.shrink.idx === k) v = lerp(v, a.shrink.to ?? v * 0.5, E.inOut(win(t, a.shrink.at ?? 0, 1.4)));
      const n = Math.max(1, Math.round((v / vmax) * 9)), gx = g.x ?? x0 + 150 + k * 300;
      return <g key={k} transform={`translate(${gx} ${y - 66})`}>
        <ellipse cx={0} cy={0} rx={100} ry={22} fill="#F5F5F5" stroke={OL} strokeWidth={4} />
        <ellipse cx={0} cy={-2} rx={70} ry={14} fill="#E0E0E0" />
        {u > 0 && Array.from({length: n}, (_, q) => <g key={q} transform={`translate(${(rnd(k * 5 + q) - 0.5) * 8} ${-10 - q * 18 * u})`}><rect x={-56} y={-14} width={112} height={18} rx={6} fill={q % 2 ? '#FFF3D1' : '#F2D9A0'} stroke={OL} strokeWidth={3} />
          <path d="M -40 -6 L 40 -6" stroke={GOLD} strokeWidth={3} /></g>)}
        {u > 0 && <g transform={`translate(0 ${-26 - n * 18 * u}) scale(${u})`}><path d="M -6 0 L 0 -26 L 6 0" fill={GOLD} stroke={OL} strokeWidth={2} /></g>}
        <g transform={`translate(0 120) scale(${pop(t, gat - 0.2, 0.4)})`}><path d="M -110 -34 L 110 -34 L 96 34 L -96 34 Z" fill="#FFFDF4" stroke={OL} strokeWidth={4} />
          <T x={0} y={g.display ? -4 : 10} s={fit(g.label || '', 190, 28)} c={NAVY}>{g.label}</T>
          {g.display && <T x={0} y={24} s={fit(g.display, 190, 22)} c={g.color || RED}>{g.display}</T>}</g>
      </g>; })}
  </g>;
};

/** IOUSTACK: a teetering stack of IOU notes that grows by `rate` notes/s from `at` (max n), sways, and spills one at spillAt */
const ioustack: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4), n = Math.min(a.n ?? 30, 1 + Math.floor((t - at) * (a.rate ?? 6)));
  return <g key={'ious' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {Array.from({length: n}, (_, q) => { const sway = Math.sin(t * 2 + i) * q * q * 0.04; return <g key={q} transform={`translate(${sway + (rnd(q + i * 13) - 0.5) * 10} ${-20 - q * 30}) rotate(${(rnd(q * 3 + i) - 0.5) * 6})`}>{note(130, 34, 'IOU', PAPER, q)}</g>; })}
    {a.label && <g transform={`translate(0 ${-60 - n * 30})`}><rect x={-a.label.length * 10 - 20} y={-30} width={a.label.length * 20 + 40} height={46} rx={14} fill={RED} stroke={OL} strokeWidth={4} /><T x={0} y={2} s={26} c="#FFFFFF">{a.label}</T></g>}
  </g>;
};

/** BONDPOP: a bond certificate (text) that pops in at `at` with a sparkle ring, optional tag below (sub) */
const bondpop: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.4)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 400), s = (a.scale ?? 1) * pop(t, at, 0.5);
  return <g key={'bp' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${Math.sin(t * 2 + i) * 3})`}>
    {t - at < 1.2 && Array.from({length: 10}, (_, q) => { const an = (q / 10) * Math.PI * 2, r = 120 + 80 * win(t, at, 1); return <path key={q} d={`M ${Math.cos(an) * r} ${Math.sin(an) * r * 0.7} l ${Math.cos(an) * 24} ${Math.sin(an) * 18}`} stroke={GOLD} strokeWidth={7} strokeLinecap="round" opacity={1 - win(t, at + 0.6, 0.6)} />; })}
    {bond(240, 140, a.text || 'T-BOND', i)}
    {a.sub && <g transform="translate(0 110)"><rect x={-Math.max(110, a.sub.length * 9 + 20)} y={-24} width={Math.max(220, a.sub.length * 18 + 40)} height={44} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={8} s={22}>{a.sub}</T></g>}
  </g>;
};

export const DEBT_ITEMS: Record<string, ItemFn> = {owen, feast, ioustack, bondpop};
export const DEBT_INDOOR = ['iouvault', 'auctionhouse', 'dinnerparty', 'fedwarehouse', 'trustcabinet', 'debttitle', 'debtbumper'];
