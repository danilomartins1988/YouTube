import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * AITAXES kit for CartoonStage (Episode 69, "If AI Replaces Workers, Who Pays the Taxes?").
 *
 * Prime-time TV-cartoon GENRE (thick clean outlines, flat colour, squash and stretch), day scenes, everything ORIGINAL: a fictional small
 * town (PINEWICK), its mayor ROSA (drawn with the shared `toon` rig), STUB (a walking pay stub, the last one printed at the warehouse) and
 * RIVET (the warehouse's friendly new robot, with no paycheck and no pockets). No logos, no flags, no brand names, no real person drawn.
 * Sets:
 *  - txtown: Pinewick's Main Street by day: school, town hall with clock tower, shops whose shutters drop (`closed` KF 0..1), a road whose
 *    potholes open (`holes` KF 0..1), a school bus (`bus`), the big warehouse on the hill, a street banner (`banner` [[t, text]]).
 *  - txware: the warehouse floor: conveyor of boxes, robot arms appearing (`robots` KF 0..4), empty lockers (`lockers` KF 0..6),
 *    party bunting and confetti (`party` t), wall sign (`sign` [[t, text]]).
 *  - txpipes: the money plumbing: a BIG tap (people: income and paycheck taxes, width `big` KF 0..1) and a THIN tap (company profits,
 *    `thin` KF 0..1) fill a tank (`level` KF 0..1) that feeds SCHOOLS, ROADS and SOCIAL SECURITY; `extra` [{label, at, c}] adds new taps.
 *  - txfair: the idea fair: four striped booths (`booths` [{label, c}]), `shown` KF 0..4, `lit` [[t, i]] spotlight, ferris wheel, lights.
 *  - txscale: the Fair Scale inside a tent: GOOD REASON pan vs THE CATCH pan, cards `pro` / `con` [[t, text]], `tilt` KF -1..1, `title`.
 *  - txjars: a gallery of tax jars of rich democracies (no flags: little landscapes), work-tax part fills to about half (`fill` KF 0..1).
 *  - txalaska: snowy town, a pipeline and THE FUND vault; checks fly to mailboxes (`checks` KF 0..1); at `swap` the barrel on the sign
 *    turns into a robot head; `sign` text.
 *  - txmail: a sunny street of houses; envelopes drop into mailboxes (`env` KF 0..6); `variant` 'valley' | 'city'; `cal` [[t, text]].
 *  - txclock: the Social Security office: paycheck inflow (`inflow` KF 0..1), reserve tank (`level` KF 0..1), checks out to retirees,
 *    wall calendar (`year` [[t, text]]).
 *  - txmeeting: the town meeting: podium, easel list (`list` [text], `shown` KF), audience heads, hands up (`hands` t).
 *  - txtitle / txbumper: title card (a pay stub and a robot tug a giant coin) and chapter bumpers (a stamp slams PAID? on a stub).
 * Items: stub (walking pay stub: `x` KF, `face`/`faces` happy | worry | wow | sad, `hops`, `torn` KF 0..3 slices torn off, `label`),
 *  rivet (the robot: `x` KF, `face`/`faces`, `pockets` t (pockets turn out), `hand` t (raises a hand), `carry` 'box').
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
  PINK = '#E86A92', CY = '#29C5F6', PAPER = '#FFFDF4', SNOW = '#F4F8FC', WATER = '#5AB4E8';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: any) => <path key={'txc' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.62 + 30);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const ground = (z: Z, f: number, c = '#A6D08A', c2 = '#88B86C') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const hills = (z: Z, f: number, c = '#BFE3A0', k = 0) => { let d = `M ${z.x0} ${f}`; for (let x = z.x0; x <= z.x1 + 300; x += 300) d += ` Q ${x + 150} ${f - 160 - 80 * rnd(k + x / 300)} ${x + 300} ${f}`;
  return <path d={d + ' Z'} fill={c} stroke={OL} strokeWidth={4} />; };
const coin = (x: number, y: number, r: number, k: any) => <g key={'cn' + k} transform={`translate(${x} ${y})`}><circle r={r} fill={GOLD} stroke={OL} strokeWidth={4} /><T x={0} y={r * 0.38} s={r * 1.1} c="#8A5A00">$</T></g>;
const check = (x: number, y: number, s: number, rot: number, k: any) => <g key={'ck' + k} transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
  <rect x={-60} y={-28} width={120} height={56} rx={6} fill="#E8F6EA" stroke={OL} strokeWidth={4} /><path d="M -44 -8 L 10 -8 M -44 8 L 30 8" stroke={GREEN} strokeWidth={5} /><T x={40} y={0} s={24} c={GREEN}>$</T></g>;
const robotHead = (x: number, y: number, s: number, k: any) => <g key={'rh' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M 0 -70 L 0 -92" stroke={OL} strokeWidth={6} /><circle cy={-98} r={9} fill={RED} stroke={OL} strokeWidth={4} />
  <rect x={-60} y={-70} width={120} height={96} rx={20} fill="#CFD8E3" stroke={OL} strokeWidth={6} /><rect x={-44} y={-54} width={88} height={60} rx={12} fill="#263238" />
  <circle cx={-18} cy={-26} r={9} fill={CY} /><circle cx={18} cy={-26} r={9} fill={CY} /></g>;
const barrel = (x: number, y: number, s: number, k: any) => <g key={'br' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-50} y={-70} width={100} height={140} rx={14} fill="#3B2A20" stroke={OL} strokeWidth={6} /><path d="M -50 -26 L 50 -26 M -50 26 L 50 26" stroke="#7A5A40" strokeWidth={8} /></g>;
/** generic house with a mailbox */
const house = (x: number, y: number, s: number, c: string, k: any, env = 0, t = 0) => <g key={'hs' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-110} y={-170} width={220} height={170} fill={c} stroke={OL} strokeWidth={6} /><path d="M -135 -165 L 0 -270 L 135 -165 Z" fill="#B5543C" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
  <rect x={-30} y={-90} width={60} height={90} fill="#7A4B2A" stroke={OL} strokeWidth={5} /><rect x={-90} y={-140} width={46} height={40} fill="#BFE6F7" stroke={OL} strokeWidth={4} /><rect x={44} y={-140} width={46} height={40} fill="#BFE6F7" stroke={OL} strokeWidth={4} />
  <g transform="translate(170 0)"><path d="M 0 0 L 0 -90" stroke={OL} strokeWidth={8} /><rect x={-34} y={-130} width={68} height={44} rx={18} fill="#5E6B85" stroke={OL} strokeWidth={5} />
    <path d={`M 30 -128 L 30 ${-160 + (env > 0 ? 0 : 26)} L 52 ${-160 + (env > 0 ? 0 : 26)}`} stroke={RED} strokeWidth={6} fill="none" />
    {env > 0 && <g transform={`translate(0 ${-112 - 40 * (1 - clamp(env))})`} opacity={clamp(env * 3)}><rect x={-26} y={-18} width={52} height={34} rx={4} fill={PAPER} stroke={OL} strokeWidth={3} /><T x={0} y={8} s={22} c={GREEN}>$</T></g>}</g>
</g>;

const RAW: Record<string, SetFn> = {
  /** Pinewick's Main Street by day */
  txtown: (t, z, f) => {
    const closed = kf(z.closed, t, 0), holes = kf(z.holes, t, 0), ban: string = pick(z.banner, t, z.bannerText || '');
    const busX = z.bus ? ((t * 220) % 3200) - 700 : -9999;
    return <g>
      {sky(z, f, '#7EC8F2', '#DDF2FF', 'txsk' + (z.ox ?? 0))}
      {[0, 1, 2, 3].map((k) => cloud(z.x0 + 300 + k * 700 + ((t * 14) % 700), 150 + 40 * (k % 2), 0.9, k))}
      {hills(z, f - 130, '#BFE3A0', 3)}
      {/* warehouse on the hill */}
      <g transform="translate(1720 620)"><rect x={-260} y={-150} width={520} height={150} fill="#D9DEE6" stroke={OL} strokeWidth={6} /><path d="M -280 -150 L 0 -230 L 280 -150 Z" fill="#9AA6B8" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        {[0, 1, 2, 3].map((q) => <rect key={q} x={-220 + q * 120} y={-90} width={80} height={90} fill="#8C99AB" stroke={OL} strokeWidth={4} />)}{plaque(0, -170, z.wareLabel || 'WAREHOUSE', '#FFFFFF', 20)}</g>
      {/* school */}
      <g transform="translate(260 860)"><rect x={-200} y={-240} width={400} height={240} fill="#E9A36B" stroke={OL} strokeWidth={6} /><path d="M -220 -240 L 0 -330 L 220 -240 Z" fill="#B5543C" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        {[0, 1, 2, 3].map((q) => <rect key={q} x={-170 + q * 90} y={-200} width={60} height={56} fill="#BFE6F7" stroke={OL} strokeWidth={4} />)}<rect x={-40} y={-110} width={80} height={110} fill="#7A4B2A" stroke={OL} strokeWidth={5} />{plaque(0, -262, 'SCHOOL', '#FFFFFF', 22)}</g>
      {/* town hall */}
      <g transform="translate(840 860)"><rect x={-230} y={-280} width={460} height={280} fill="#F2E6CF" stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3, 4].map((q) => <rect key={q} x={-200 + q * 90} y={-250} width={34} height={250} fill="#FFFFFF" stroke={OL} strokeWidth={4} />)}
        <path d="M -250 -280 L 0 -360 L 250 -280 Z" fill="#C9B48E" stroke={OL} strokeWidth={6} strokeLinejoin="round" /><rect x={-60} y={-470} width={120} height={120} fill="#F2E6CF" stroke={OL} strokeWidth={6} />
        <circle cy={-410} r={42} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><path d={`M 0 -410 L ${30 * Math.sin(t * 0.5)} ${-410 - 30 * Math.cos(t * 0.5)} M 0 -410 L ${20 * Math.sin(t * 0.04)} ${-410 - 20 * Math.cos(t * 0.04)}`} stroke={OL} strokeWidth={5} strokeLinecap="round" />
        {plaque(0, -300, 'PINEWICK TOWN HALL', '#FFFFFF', 22)}</g>
      {/* shops */}
      {[0, 1, 2].map((q) => { const x = 1240 + q * 230, c = [PINK, TEAL, ORANGE][q], sh = clamp(closed * 3 - q);
        return <g key={'sp' + q} transform={`translate(${x} 860)`}><rect x={-105} y={-220} width={210} height={220} fill="#FFF3DD" stroke={OL} strokeWidth={6} />
          {[0, 1, 2, 3, 4].map((s) => <path key={s} d={`M ${-105 + s * 42} -220 l 42 0 l -6 40 l -30 0 Z`} fill={s % 2 ? '#FFFFFF' : c} stroke={OL} strokeWidth={3} />)}
          <rect x={-80} y={-160} width={160} height={110} fill="#BFE6F7" stroke={OL} strokeWidth={4} />
          <rect x={-80} y={-160} width={160} height={110 * sh} fill="#9AA6B8" stroke={OL} strokeWidth={4} />{sh > 0.95 && <T x={0} y={-96} s={24} c={RED}>CLOSED</T>}</g>; })}
      {ban && <g transform="translate(960 470)"><path d="M -700 -40 Q 0 20 700 -40" stroke={OL} strokeWidth={4} fill="none" />
        <rect x={-fit(ban, 900, 44) * ban.length * 0.33 - 40} y={-30} width={fit(ban, 900, 44) * ban.length * 0.66 + 80} height={70} rx={10} fill={GOLD} stroke={OL} strokeWidth={5} /><T x={0} y={18} s={fit(ban, 900, 44)} c={NAVY}>{ban}</T></g>}
      {/* road */}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#8F9AA8" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={16} fill="#C9CED6" stroke={OL} strokeWidth={4} />
      {Array.from({length: 30}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 220} y={f + 110} width={110} height={12} fill="#FFFFFF" />)}
      {Array.from({length: 6}, (_, k) => { const u = clamp(holes * 6 - k); if (u <= 0) return null; return <ellipse key={'ph' + k} cx={200 + k * 300 + 60 * rnd(k)} cy={f + 60 + 90 * rnd(k + 4)} rx={44 * u} ry={14 * u} fill="#4A525E" stroke={OL} strokeWidth={3} />; })}
      {busX > -900 && <g transform={`translate(${busX} ${f + 70})`}><rect x={-150} y={-120} width={300} height={110} rx={16} fill={GOLD} stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3].map((q) => <rect key={q} x={-130 + q * 64} y={-104} width={50} height={40} fill="#BFE6F7" stroke={OL} strokeWidth={3} />)}
        <circle cx={-90} cy={-6} r={24} fill={OL} /><circle cx={90} cy={-6} r={24} fill={OL} /><T x={0} y={-40} s={20} c={NAVY}>SCHOOL BUS</T></g>}
    </g>;
  },

  /** the warehouse floor */
  txware: (t, z, f) => {
    const robots = kf(z.robots, t, 0), lockers = kf(z.lockers, t, 0), party = z.party ?? -1, sign: string = pick(z.sign, t, z.signText || '');
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill="#E4E9F0" />
      {Array.from({length: 12}, (_, k) => <rect key={'wn' + k} x={z.x0 + 120 + k * 380} y={90} width={260} height={130} fill="#BFE6F7" stroke={OL} strokeWidth={5} />)}
      <path d={`M ${z.x0} 260 L ${z.x1} 260`} stroke="#9AA6B8" strokeWidth={10} />
      {sign && <g transform="translate(960 330)"><rect x={-430} y={-46} width={860} height={82} rx={12} fill={NAVY} stroke={OL} strokeWidth={5} /><T x={0} y={14} s={fit(sign, 800, 44)} c={GOLD}>{sign}</T></g>}
      {/* lockers at left */}
      <g transform="translate(-60 860)">{Array.from({length: 6}, (_, q) => { const empty = q < lockers; return <g key={q} transform={`translate(${q * 70} 0)`}>
        <rect x={0} y={-300} width={64} height={300} fill={empty ? '#C6CCD6' : '#6FA8DC'} stroke={OL} strokeWidth={4} /><rect x={14} y={-280} width={36} height={8} fill={OL} />
        {empty ? <path d="M 4 -296 L 60 -4" stroke="#9AA6B8" strokeWidth={4} /> : <rect x={10} y={-200} width={44} height={22} rx={4} fill={PAPER} stroke={OL} strokeWidth={2} />}</g>; })}</g>
      {/* conveyor */}
      <rect x={480} y={f - 150} width={1500} height={40} rx={20} fill="#5E6B85" stroke={OL} strokeWidth={6} />
      {Array.from({length: 16}, (_, k) => <circle key={'rl' + k} cx={500 + k * 96} cy={f - 130} r={12} fill="#9AA6B8" stroke={OL} strokeWidth={3} />)}
      <path d={`M 520 ${f - 110} L 520 ${f} M 1940 ${f - 110} L 1940 ${f}`} stroke={OL} strokeWidth={12} />
      {Array.from({length: 9}, (_, k) => { const x = 480 + (((t * 160) + k * 170) % 1500); return <g key={'bx' + k} transform={`translate(${x} ${f - 150})`}>
        <rect x={-40} y={-70} width={80} height={70} fill="#C99A5B" stroke={OL} strokeWidth={4} /><path d="M -40 -40 L 40 -40" stroke="#8A6236" strokeWidth={4} /></g>; })}
      {/* robot arms */}
      {Array.from({length: 4}, (_, q) => { const u = clamp(robots - q); if (u <= 0) return null; const x = 700 + q * 340, a = Math.sin(t * 3 + q) * 30;
        return <g key={'ra' + q} transform={`translate(${x} ${f - 150}) scale(${E.outBack(u)})`}><rect x={-50} y={-30} width={100} height={30} fill={ORANGE} stroke={OL} strokeWidth={5} />
          <g transform={`translate(0 -30) rotate(${-30 + a})`}><rect x={-14} y={-200} width={28} height={200} rx={12} fill={ORANGE} stroke={OL} strokeWidth={5} />
            <g transform={`translate(0 -200) rotate(${70 - a * 2})`}><rect x={-12} y={-150} width={24} height={150} rx={10} fill={ORANGE} stroke={OL} strokeWidth={5} /><path d="M -22 -150 L -22 -180 M 22 -150 L 22 -180" stroke={OL} strokeWidth={8} strokeLinecap="round" /></g>
            <circle cy={-200} r={18} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g><circle cy={-30} r={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} /></g>; })}
      {/* party */}
      {party >= 0 && t >= party && <g>
        <path d={`M ${z.x0} 380 Q 960 470 ${z.x1} 380`} stroke={OL} strokeWidth={3} fill="none" />
        {Array.from({length: 30}, (_, k) => { const x = z.x0 + 80 + k * ((z.x1 - z.x0) / 30); return <path key={'bt' + k} d={`M ${x - 26} ${384 + 80 * Math.sin((x - z.x0) / (z.x1 - z.x0) * Math.PI)} l 26 44 l 26 -44 Z`} fill={[RED, GOLD, BLUE, GREEN][k % 4]} stroke={OL} strokeWidth={3} />; })}
        {Array.from({length: 50}, (_, k) => { const u = ((t - party) * 0.35 + rnd(k)) % 1; return <rect key={'cf' + k} x={z.x0 + rnd(k + 7) * (z.x1 - z.x0)} y={-60 + u * 1000} width={14} height={8} fill={[RED, GOLD, BLUE, GREEN, PINK][k % 5]} transform={`rotate(${t * 200 + k * 40} ${z.x0 + rnd(k + 7) * (z.x1 - z.x0)} ${-60 + u * 1000})`} />; })}</g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#B8C0CC" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#9AA6B8" stroke={OL} strokeWidth={4} />
      {Array.from({length: 24}, (_, k) => <path key={'st' + k} d={`M ${z.x0 + k * 300} ${f + 40} l 120 0`} stroke={GOLD} strokeWidth={10} />)}
    </g>;
  },

  /** the money plumbing */
  txpipes: (t, z, f) => {
    const big = kf(z.big, t, 1), thin = kf(z.thin, t, 0.18), level = kf(z.level, t, 0.8), extra: any[] = z.extra || [];
    const flowD = (w: number, d: string, c: string, k: any) => w > 0.02 ? <g key={'fl' + k}><path d={d} stroke={OL} strokeWidth={w * 90 + 10} fill="none" strokeLinecap="round" />
      <path d={d} stroke={c} strokeWidth={w * 90} fill="none" strokeLinecap="round" /><path d={d} stroke="#FFFFFF" strokeWidth={Math.max(3, w * 18)} fill="none" strokeDasharray="20 40" strokeDashoffset={-t * 160} opacity={0.7} /></g> : null;
    const out = clamp(level * 1.2);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#EAF4FB" />
      {Array.from({length: 24}, (_, k) => <path key={'gr' + k} d={`M ${z.x0 + k * 200} -200 L ${z.x0 + k * 200} 1300`} stroke="#D5E6F2" strokeWidth={3} />)}
      <g transform="translate(96 150) scale(0.9)">
      {/* big tap: people */}
      <g transform="translate(250 380)"><rect x={-150} y={-90} width={300} height={170} rx={14} fill={PAPER} stroke={OL} strokeWidth={6} /><path d="M -120 -40 L 120 -40 M -120 0 L 80 0 M -120 40 L 100 40" stroke="#B0BEC5" strokeWidth={8} />
        <T x={0} y={-110} s={fit(z.bigLabel || 'PEOPLE: INCOME + PAYCHECK TAXES', 420, 28)} c={BLUE}>{z.bigLabel || 'PEOPLE: INCOME + PAYCHECK TAXES'}</T></g>
      {flowD(big, 'M 400 380 Q 600 380 700 330', BLUE, 'big')}
      {/* thin tap: companies */}
      <g transform="translate(250 700)"><rect x={-130} y={-110} width={260} height={150} fill="#C5CDD8" stroke={OL} strokeWidth={6} /><path d="M -130 -110 L -60 -170 L 20 -110 L 90 -170 L 130 -110" fill="#9AA6B8" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <T x={0} y={90} s={28} c={TEAL}>{z.thinLabel || 'COMPANY PROFITS'}</T></g>
      {flowD(thin, 'M 380 650 Q 600 640 700 560', TEAL, 'thin')}
      {extra.map((e, k) => { const u = clamp((t - (e.at ?? 0)) / 0.8); if (u <= 0) return null; const y = 860 + k * 0;
        return <g key={'ex' + k} opacity={u}>{flowD(0.22 * u, `M ${300 + k * 160} ${y + 80} Q 600 ${y} 760 680`, e.c || GOLD, 'ex' + k)}{plaque(300 + k * 160, y + 110, e.label, '#FFFFFF', 20)}</g>; })}
      {/* tank */}
      <g transform="translate(960 640)"><rect x={-220} y={-380} width={440} height={420} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={8} />
        <rect x={-210} y={30 - 400 * level} width={420} height={400 * level} rx={20} fill={WATER} />
        <path d={`M -210 ${30 - 400 * level} q 50 ${-10 * Math.sin(t * 3)} 105 0 t 105 0 t 105 0 t 105 0`} stroke="#FFFFFF" strokeWidth={5} fill="none" opacity={level > 0.03 ? 1 : 0} />
        {plaque(0, -410, z.tankLabel || "THE GOVERNMENT'S TANK", GOLD, 28)}</g>
      {/* outflows */}
      {[['SCHOOLS', 340, ORANGE], ['ROADS', 560, '#5E6B85'], ['SOCIAL SECURITY', 780, GREEN]].map(([lab, y, c], k) => <g key={'of' + k}>
        {flowD(0.32 * out, `M 1180 ${560 + k * 60} Q 1350 ${y} 1500 ${y}`, WATER, 'o' + k)}
        <g transform={`translate(1650 ${Number(y) + 40})`}><rect x={-120} y={-110} width={240} height={120} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><path d="M -140 -110 L 0 -170 L 140 -110 Z" fill={c as string} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <T x={0} y={-36} s={fit(lab as string, 220, 28)} c={NAVY}>{lab}</T></g></g>)}
      </g>
    </g>;
  },

  /** the idea fair */
  txfair: (t, z, f) => {
    const booths: any[] = z.booths || [{label: 'TAX THE ROBOTS', c: ORANGE}, {label: 'TAX THE OWNERS', c: TEAL}, {label: 'TAX THE SHOPPING', c: PINK}, {label: 'SEND EVERYONE A CHECK', c: GREEN}];
    const shown = kf(z.shown, t, booths.length), lit = Number(pick(z.lit, t, -1)), litAt = lastAt(z.lit, t);
    return <g>
      {sky(z, f, '#7EC8F2', '#E6F6FF', 'txfs' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 400 + k * 800 + ((t * 10) % 800), 140, 0.9, 'f' + k))}
      <g transform={`translate(1700 520) rotate(${t * 8})`}>{Array.from({length: 10}, (_, k) => <g key={k} transform={`rotate(${k * 36})`}><path d="M 0 0 L 0 -300" stroke="#9AA6B8" strokeWidth={6} />
        <g transform={`translate(0 -300) rotate(${-t * 8 - k * 36})`}><rect x={-28} y={0} width={56} height={44} rx={8} fill={[RED, GOLD, BLUE, GREEN, PINK][k % 5]} stroke={OL} strokeWidth={4} /></g></g>)}
        <circle r={300} fill="none" stroke="#9AA6B8" strokeWidth={8} /><circle r={24} fill="#FFFFFF" stroke={OL} strokeWidth={5} /></g>
      <path d="M 1700 520 L 1560 860 M 1700 520 L 1840 860" stroke="#5E6B85" strokeWidth={12} />
      {hills(z, f - 60, '#BFE3A0', 8)}
      <path d={`M ${z.x0} 300 Q 960 380 ${z.x1} 300`} stroke={OL} strokeWidth={3} fill="none" />
      {Array.from({length: 26}, (_, k) => { const x = z.x0 + 60 + k * ((z.x1 - z.x0) / 26); return <circle key={'lt' + k} cx={x} cy={300 + 80 * Math.sin((x - z.x0) / (z.x1 - z.x0) * Math.PI)} r={9} fill={(k + Math.floor(t * 3)) % 2 ? GOLD : '#FFF3B0'} stroke={OL} strokeWidth={2} />; })}
      {booths.map((b, k) => { const u = clamp(shown - k); if (u <= 0) return null; const x = 260 + k * 440, on = lit === k, pu = on ? 1 + 0.06 * Math.max(0, Math.sin((t - litAt) * 8)) * Math.exp(-(t - litAt) * 1.5) : 1;
        return <g key={'bo' + k} transform={`translate(${x} 860) scale(${E.outBack(u) * pu})`} opacity={lit >= 0 && !on ? 0.55 : 1}>
          {on && <ellipse cx={0} cy={-10} rx={230} ry={30} fill={GOLD} opacity={0.5} />}
          <rect x={-170} y={-300} width={340} height={300} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
          {[0, 1, 2, 3, 4, 5].map((s) => <path key={s} d={`M ${-190 + s * 63} -300 l 63 0 l -10 60 l -43 0 Z`} fill={s % 2 ? '#FFFFFF' : b.c} stroke={OL} strokeWidth={4} />)}
          <path d="M -190 -300 L 0 -400 L 190 -300 Z" fill={b.c} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
          <rect x={-150} y={-220} width={300} height={90} rx={10} fill={NAVY} stroke={OL} strokeWidth={4} /><T x={0} y={-162} s={fit(b.label, 270, 30)} c={GOLD}>{b.label}</T>
          <rect x={-170} y={-70} width={340} height={70} fill={b.c} stroke={OL} strokeWidth={5} /><T x={0} y={-24} s={30} c="#FFFFFF">{['1', '2', '3', '4', '5'][k]}</T></g>; })}
      {ground(z, f, '#A6D08A', '#88B86C')}
    </g>;
  },

  /** the Fair Scale */
  txscale: (t, z, f) => {
    const tilt = kf(z.tilt, t, 0), pro: string = pick(z.pro, t, ''), con: string = pick(z.con, t, ''), proAt = lastAt(z.pro, t), conAt = lastAt(z.con, t);
    const a = tilt * 14 + Math.sin(t * 1.6) * 1.2, rad = a / 57.3, ly = -Math.sin(rad) * 420, ry = Math.sin(rad) * 420;
    const card = (x: number, y: number, txt: string, c: string, at: number, head: string) => { const s = pop(t, at, 0.4); const words = txt.split(' '), lines: string[] = [];
      let cur = ''; for (const w of words) { if ((cur + ' ' + w).trim().length > 20) { lines.push(cur.trim()); cur = w; } else cur += ' ' + w; } if (cur.trim()) lines.push(cur.trim());
      return <g transform={`translate(${x} ${y}) scale(${s})`}><rect x={-300} y={-60 - lines.length * 46} width={600} height={100 + lines.length * 46} rx={18} fill="#FFFFFF" stroke={c} strokeWidth={8} />
        <T x={0} y={-24 - lines.length * 46 + 30} s={28} c={c} ls={3}>{head}</T>{lines.map((l, k) => <T key={k} x={0} y={-lines.length * 46 + 46 + k * 46 + 10} s={38} c={NAVY}>{l}</T>)}</g>; };
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#FFF4E0" />
      {Array.from({length: 16}, (_, k) => <path key={'tn' + k} d={`M ${960 + (k - 8) * 260} 1100 L 960 -260`} stroke={k % 2 ? '#F7D9A8' : '#FFF4E0'} strokeWidth={130} />)}
      {z.title && <g transform="translate(960 120)"><rect x={-420} y={-50} width={840} height={90} rx={16} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={16} s={fit(z.title, 780, 48)} c={GOLD}>{z.title}</T></g>}
      <g transform="translate(960 560)">
        <path d="M -60 300 L 0 -10 L 60 300 Z" fill="#C9A15B" stroke={OL} strokeWidth={6} strokeLinejoin="round" /><rect x={-160} y={290} width={320} height={30} rx={10} fill="#8A6236" stroke={OL} strokeWidth={5} />
        <g transform={`rotate(${a})`}><rect x={-440} y={-14} width={880} height={28} rx={14} fill="#C9A15B" stroke={OL} strokeWidth={6} /></g>
        <circle r={26} fill={GOLD} stroke={OL} strokeWidth={5} />
        {[[-420, ly, GREEN, 'GOOD REASON'], [420, ry, RED, 'THE CATCH']].map(([x, y, c, lab], k) => <g key={'pn' + k} transform={`translate(${Math.cos(rad) * Number(x)} ${Number(y)})`}>
          <path d="M 0 0 L -120 160 M 0 0 L 120 160" stroke={OL} strokeWidth={4} /><path d="M -150 160 Q 0 250 150 160 Z" fill={c as string} stroke={OL} strokeWidth={6} />
          <T x={0} y={205} s={26} c="#FFFFFF">{lab}</T></g>)}
      </g>
      {pro && card(640, 400 + ly, pro, GREEN, proAt, 'GOOD REASON')}
      {con && card(1280, 400 + ry, con, RED, conAt, 'THE CATCH')}
      <rect x={z.x0} y={f + 40} width={z.x1 - z.x0} height={700} fill="#C9A15B" /><rect x={z.x0} y={f + 40} width={z.x1 - z.x0} height={12} fill="#A07C3E" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** tax jars of rich democracies (no flags: little landscapes) */
  txjars: (t, z, f) => {
    const fill = kf(z.fill, t, 1), lv = [0.46, 0.55, 0.5, 0.42, 0.58, 0.49];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#F3EEFF" />
      {z.title && <T x={960} y={170} s={44} c={NAVY}>{z.title}</T>}
      {lv.map((l, k) => { const x = 260 + k * 280, h = 400, y0 = 760, u = clamp(fill * 1.3 - k * 0.06);
        return <g key={'jr' + k} transform={`translate(${x} 0)`}>
          <rect x={-100} y={y0 - h} width={200} height={h} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
          <rect x={-92} y={y0 - 8 - (h - 16) * l * u} width={184} height={(h - 16) * l * u} rx={22} fill={BLUE} />
          <rect x={-92} y={y0 - 8 - (h - 16) * u} width={184} height={(h - 16) * (1 - l) * u} rx={22} fill="#C5CDD8" />
          <rect x={-70} y={y0 - h - 30} width={140} height={36} rx={10} fill="#8A6236" stroke={OL} strokeWidth={5} />
          <g transform={`translate(0 ${y0 + 80})`}>{k % 3 === 0 ? <path d="M -70 20 L -20 -40 L 10 0 L 40 -30 L 80 20 Z" fill="#9AA6B8" stroke={OL} strokeWidth={4} />
            : k % 3 === 1 ? <g><path d="M -80 20 L 80 20" stroke={OL} strokeWidth={4} /><rect x={-50} y={-40} width={30} height={60} fill="#D9DEE6" stroke={OL} strokeWidth={3} /><rect x={-10} y={-60} width={30} height={80} fill="#D9DEE6" stroke={OL} strokeWidth={3} /><rect x={30} y={-30} width={30} height={50} fill="#D9DEE6" stroke={OL} strokeWidth={3} /></g>
              : <g><path d="M -80 20 Q 0 -40 80 20 Z" fill="#A6D08A" stroke={OL} strokeWidth={4} /><circle cx={40} cy={-40} r={16} fill={GOLD} stroke={OL} strokeWidth={3} /></g>}</g>
        </g>; })}
      <g transform="translate(960 990)"><rect x={-26} y={-26} width={36} height={36} fill={BLUE} stroke={OL} strokeWidth={3} transform="translate(-380 0)" /><T x={-330} y={4} s={28} a="start" c={NAVY}>{z.legend || 'TAXES ON WORK AND PERSONAL INCOME'}</T></g>
    </g>;
  },

  /** Alaska-style fund: snow, pipeline, the fund vault, checks to mailboxes */
  txalaska: (t, z, f) => {
    const checks = kf(z.checks, t, 0), swapped = z.swap !== undefined && t >= z.swap;
    return <g>
      {sky(z, f, '#8FD0F5', '#EAF7FF', 'txak' + (z.ox ?? 0))}
      {[0, 1, 2, 3, 4, 5].map((k) => <path key={'mt' + k} d={`M ${z.x0 + k * 420 - 100} ${f - 120} L ${z.x0 + k * 420 + 140} ${f - 470 - 60 * rnd(k)} L ${z.x0 + k * 420 + 380} ${f - 120} Z`} fill="#9FB3C8" stroke={OL} strokeWidth={5} strokeLinejoin="round" />)}
      {[0, 1, 2, 3, 4, 5].map((k) => <path key={'sc' + k} d={`M ${z.x0 + k * 420 + 80} ${f - 400 - 60 * rnd(k) + 40} L ${z.x0 + k * 420 + 140} ${f - 470 - 60 * rnd(k)} L ${z.x0 + k * 420 + 200} ${f - 400 - 60 * rnd(k) + 40} Z`} fill={SNOW} stroke={OL} strokeWidth={4} strokeLinejoin="round" />)}
      <rect x={z.x0} y={f - 140} width={z.x1 - z.x0} height={200} fill={SNOW} />
      {/* pipeline */}
      <path d={`M ${z.x0} ${f - 200} L 420 ${f - 200}`} stroke="#9AA6B8" strokeWidth={26} /><path d={`M ${z.x0} ${f - 200} L 420 ${f - 200}`} stroke={OL} strokeWidth={4} strokeDasharray="4 120" />
      {Array.from({length: 8}, (_, k) => <path key={'pp' + k} d={`M ${z.x0 + 80 + k * 160} ${f - 190} L ${z.x0 + 80 + k * 160} ${f - 120}`} stroke={OL} strokeWidth={6} />)}
      {/* the fund */}
      <g transform={`translate(640 ${f - 40})`}><rect x={-230} y={-330} width={460} height={330} fill="#E9EEF5" stroke={OL} strokeWidth={6} />
        <path d="M -250 -330 L 0 -420 L 250 -330 Z" fill="#9AA6B8" stroke={OL} strokeWidth={6} strokeLinejoin="round" />
        <circle cy={-150} r={100} fill="#C5CDD8" stroke={OL} strokeWidth={7} /><g transform={`rotate(${t * 30} 0 -150)`}>{[0, 60, 120].map((r) => <path key={r} transform={`rotate(${r} 0 -150)`} d="M -70 -150 L 70 -150" stroke={OL} strokeWidth={6} />)}</g>
        {plaque(0, -360, z.sign || 'THE FUND', GOLD, 26)}
        <g transform="translate(-170 -380)">{swapped ? robotHead(0, 30, 0.55, 'sw') : barrel(0, 0, 0.5, 'ab')}</g></g>
      {/* houses */}
      {[0, 1, 2, 3].map((k) => house(1120 + k * 260, f - 20, 0.7, ['#F2E6CF', '#FFD7C2', '#D8ECFF', '#E3F4D9'][k], 'ah' + k, clamp(checks * 4 - k)))}
      {checks > 0.01 && Array.from({length: 10}, (_, k) => { const u = ((t * 0.5 + k / 10) % 1); const x = lerp(700, 1200 + (k % 4) * 260, u), y = f - 300 - Math.sin(u * Math.PI) * 300;
        return check(x, y, 0.8, Math.sin(t * 3 + k) * 20, 'fc' + k); })}
      {Array.from({length: 40}, (_, k) => <circle key={'sn' + k} cx={z.x0 + rnd(k) * (z.x1 - z.x0)} cy={((t * 40 + rnd(k + 3) * 1000) % 1000)} r={4} fill="#FFFFFF" opacity={0.8} />)}
      {ground(z, f, SNOW, '#D5E2EE')}
    </g>;
  },

  /** a sunny street; envelopes drop into mailboxes */
  txmail: (t, z, f) => {
    const env = kf(z.env, t, 0), cal: string = pick(z.cal, t, ''), city = z.variant === 'city';
    return <g>
      {sky(z, f, '#86CCF4', '#FFF4DE', 'txml' + (z.ox ?? 0))}
      {[0, 1, 2].map((k) => cloud(z.x0 + 500 + k * 800 + ((t * 12) % 800), 150, 0.8, 'm' + k))}
      {city ? Array.from({length: 10}, (_, k) => { const h = 260 + rnd(k) * 260; return <rect key={'cb' + k} x={z.x0 + 200 + k * 260} y={f - 250 - h} width={180} height={h} fill={k % 2 ? '#C5D3E3' : '#B3C4D8'} stroke={OL} strokeWidth={4} />; })
        : Array.from({length: 6}, (_, k) => <g key={'pl' + k} transform={`translate(${z.x0 + 300 + k * 500} ${f - 260})`}><path d="M 0 0 Q 10 -160 -10 -300" stroke="#8A6236" strokeWidth={16} fill="none" />
          {[0, 1, 2, 3, 4].map((q) => <path key={q} transform={`translate(-10 -300) rotate(${q * 72 + Math.sin(t + k) * 4})`} d="M 0 0 Q 60 -20 120 20" stroke={GREEN} strokeWidth={14} fill="none" strokeLinecap="round" />)}</g>)}
      {[0, 1, 2, 3, 4, 5].map((k) => house(210 + k * 300, f, 0.8, ['#F2E6CF', '#FFD7C2', '#D8ECFF', '#E3F4D9', '#FCE3EC', '#FFF0C2'][k], 'mh' + k, clamp(env - k)))}
      {cal && <g transform="translate(1700 230)"><rect x={-130} y={-80} width={260} height={160} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={-130} y={-80} width={260} height={44} rx={12} fill={RED} stroke={OL} strokeWidth={5} />
        <T x={0} y={40} s={fit(cal, 230, 40)} c={NAVY}>{cal}</T></g>}
      {z.plaque && plaque(960, 420, z.plaque, '#FFFFFF', 26)}
      {ground(z, f, '#BFC6CF', '#9AA6B8')}
    </g>;
  },

  /** the Social Security office and its reserve tank */
  txclock: (t, z, f) => {
    const inflow = kf(z.inflow, t, 1), level = kf(z.level, t, 0.6), yr: string = pick(z.year, t, '');
    return <g>
      {sky(z, f, '#86CCF4', '#E8F6FF', 'txcl' + (z.ox ?? 0))}
      {hills(z, f - 40, '#BFE3A0', 11)}
      <g transform={`translate(760 ${f})`}><rect x={-300} y={-360} width={600} height={360} fill="#EEF0F4" stroke={OL} strokeWidth={6} />
        {[0, 1, 2, 3, 4, 5].map((q) => <rect key={q} x={-270 + q * 92} y={-320} width={40} height={320} fill="#FFFFFF" stroke={OL} strokeWidth={4} />)}
        <path d="M -330 -360 L 0 -460 L 330 -360 Z" fill="#C5CDD8" stroke={OL} strokeWidth={6} strokeLinejoin="round" />{plaque(0, -390, 'SOCIAL SECURITY', '#FFFFFF', 26)}</g>
      {inflow > 0.02 && <g><path d="M 0 520 Q 220 520 380 600" stroke={OL} strokeWidth={inflow * 60 + 10} fill="none" strokeLinecap="round" /><path d="M 0 520 Q 220 520 380 600" stroke={BLUE} strokeWidth={inflow * 60} fill="none" strokeLinecap="round" />
        <path d="M 0 520 Q 220 520 380 600" stroke="#FFFFFF" strokeWidth={6} fill="none" strokeDasharray="20 40" strokeDashoffset={-t * 160} />{plaque(160, 470, 'PAYCHECK TAXES', '#FFFFFF', 22)}</g>}
      <g transform={`translate(1260 ${f})`}><rect x={-120} y={-420} width={240} height={420} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={7} />
        <rect x={-110} y={-10 - 400 * level} width={220} height={400 * level} rx={18} fill={GOLD} />{plaque(0, -450, 'RESERVE', GOLD, 24)}
        <path d="M 120 -40 Q 220 -40 260 0" stroke={OL} strokeWidth={14} fill="none" /></g>
      {level > 0.02 && Array.from({length: 5}, (_, k) => { const u = ((t * 0.6 + k / 5) % 1); return check(lerp(1420, 1860, u), f - 60 - Math.sin(u * Math.PI) * 120, 0.7, -10, 'sc' + k); })}
      {yr && <g transform="translate(1660 240)"><rect x={-150} y={-90} width={300} height={180} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><rect x={-150} y={-90} width={300} height={50} rx={12} fill={RED} stroke={OL} strokeWidth={5} />
        <T x={0} y={50} s={fit(yr, 270, 64)} c={NAVY}>{yr}</T></g>}
      {ground(z, f, '#A6D08A', '#88B86C')}
    </g>;
  },

  /** the town meeting */
  txmeeting: (t, z, f) => {
    const list: string[] = z.list || [], shown = kf(z.shown, t, list.length), hands = z.hands ?? 999;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#F4EBDD" />
      {Array.from({length: 8}, (_, k) => <rect key={'wn' + k} x={z.x0 + 100 + k * 460} y={100} width={200} height={260} rx={90} fill="#BFE6F7" stroke={OL} strokeWidth={5} />)}
      <rect x={z.x0} y={560} width={z.x1 - z.x0} height={30} fill="#B07A4A" stroke={OL} strokeWidth={4} />
      <g transform="translate(1300 560)"><rect x={-330} y={-330} width={660} height={360} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><path d="M -200 30 L -260 300 M 200 30 L 260 300" stroke={OL} strokeWidth={10} />
        <T x={0} y={-270} s={34} c={NAVY}>{z.boardTitle || 'WHO COULD PAY?'}</T>
        {list.map((ln, k) => { const u = clamp(shown - k); if (u <= 0) return null; return <g key={k} opacity={u}><circle cx={-280} cy={-206 + k * 56} r={10} fill={[BLUE, ORANGE, TEAL, PINK, GREEN][k % 5]} />
          <T x={-255} y={-196 + k * 56} s={fit(ln, 560, 32)} a="start" c={NAVY}>{ln}</T></g>; })}</g>
      <g transform="translate(560 600)"><path d="M -90 0 L -60 -200 L 60 -200 L 90 0 Z" fill="#8A6236" stroke={OL} strokeWidth={6} /><rect x={-80} y={-230} width={160} height={30} rx={8} fill="#B07A4A" stroke={OL} strokeWidth={5} /></g>
      {Array.from({length: 18}, (_, k) => { const row = Math.floor(k / 9), x = 160 + (k % 9) * 200 + row * 100, y = 950 + row * 90, up = t >= hands + (k % 5) * 0.15;
        return <g key={'au' + k} transform={`translate(${x} ${y})`}>{up && <path d={`M 40 -60 L 60 ${-170 + 6 * Math.sin(t * 6 + k)}`} stroke={['#8D5A3B', '#F1C27D', '#C68642', '#E0AC69'][k % 4]} strokeWidth={18} strokeLinecap="round" />}
          <path d="M -70 60 Q -70 -30 0 -30 Q 70 -30 70 60 Z" fill={[BLUE, ORANGE, TEAL, PINK, GREEN, PURPLE][k % 6]} stroke={OL} strokeWidth={4} />
          <circle cy={-70} r={44} fill={['#2B1A12', '#6D4C41', '#212121', '#A1887F'][k % 4]} stroke={OL} strokeWidth={4} /></g>; })}
    </g>;
  },

  /** title card: a pay stub and a robot tug a giant coin */
  txtitle: (t, z, f) => {
    const lines: string[] = z.lines || ['IF AI REPLACES WORKERS,', 'WHO PAYS', 'THE TAXES?'];
    const tug = Math.sin(t * 2.6) * 40;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#E6F4FF" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(960 980) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#CFE8FB' : '#E6F4FF'} />)}
      {hills({set: '', x0: -200, x1: 2200}, 1000, '#A6D08A', 5)}
      <g transform={`translate(${960 + tug} 860)`}>{coin(0, 0, 110, 'tc')}</g>
      <path d={`M ${560} 860 L ${850 + tug} 860 M ${1070 + tug} 860 L 1360 860`} stroke={OL} strokeWidth={10} />
      <g transform="translate(470 900)"><rect x={-70} y={-200} width={140} height={190} rx={6} fill={PAPER} stroke={OL} strokeWidth={6} /><path d="M -46 -150 L 46 -150 M -46 -110 L 30 -110" stroke="#B0BEC5" strokeWidth={8} />
        <circle cx={-22} cy={-70} r={8} fill={OL} /><circle cx={22} cy={-70} r={8} fill={OL} /><path d="M -20 -40 Q 0 -54 20 -40" stroke={OL} strokeWidth={5} fill="none" /></g>
      <g transform="translate(1460 900)">{robotHead(0, -60, 1.0, 'tt')}</g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.55) / 0.5) * ln.length);
        return <T key={k} x={960} y={200 + k * 140} s={fit(ln, 1500, k === lines.length - 1 ? 140 : 100)} c={k === lines.length - 1 ? RED : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={960} y={640} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a stamp slams onto a pay stub */
  txbumper: (t, z, f) => {
    const c = z.color || BLUE, u = E.outBack(win(t, 0.5, 0.35)), stamped = t > 0.8;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g transform="translate(960 800)"><rect x={-220} y={-110} width={440} height={220} rx={8} fill={PAPER} stroke={OL} strokeWidth={6} />
        {Array.from({length: 9}, (_, q) => <circle key={q} cx={-220} cy={-90 + q * 22} r={6} fill={c} />)}<path d="M -170 -60 L 170 -60 M -170 -10 L 120 -10 M -170 40 L 140 40" stroke="#B0BEC5" strokeWidth={10} />
        {stamped && <g transform={`rotate(-10) scale(${u})`}><rect x={-170} y={-50} width={340} height={100} rx={10} fill="none" stroke={RED} strokeWidth={10} /><T x={0} y={24} s={64} c={RED}>WHO PAYS?</T></g>}
        <g transform={`translate(0 ${lerp(-500, -120, E.inOut(win(t, 0.1, 0.4))) - (t > 0.6 ? 120 * E.inOut(win(t, 0.6, 0.5)) : 0)})`}><rect x={-60} y={-40} width={120} height={50} rx={8} fill="#8A6236" stroke={OL} strokeWidth={5} /><rect x={-24} y={-160} width={48} height={120} rx={10} fill="#B07A4A" stroke={OL} strokeWidth={5} /></g></g>
      <g opacity={clamp((t - 0.5) / 0.3)}><T x={960} y={250} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={340} width={1200} height={140} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={960} y={432} s={fit(z.title || '', 1140, 62)} c={GOLD}>{z.title || ''}</T>
        {t >= 1.2 && <T x={960} y={570} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.2) / 0.3)}>{z.caption || ''}</T>}</g>
    </g>;
  },
};

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const AITAXES_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

const hopY = (a: Item, t: number) => { let hy = 0; for (const h of (a.hops || []) as number[]) { const u = t - h; if (u >= 0 && u < 0.6) hy = Math.sin((u / 0.6) * Math.PI) * 90; } return hy; };

/** stub: the walking pay stub */
const stub: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, walking = Math.abs(vx) > 20;
  const step = walking ? Math.sin(t * 14) : 0, bob = walking ? Math.abs(step) * 8 : Math.sin(t * 2.5 + i) * 3;
  const y = kf(a.y, t, f) - hopY(a, t) - bob, s = (a.scale ?? 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const face: string = pick(a.faces, t, a.face || 'happy'), fl = vx < -20 ? -1 : 1, torn = kf(a.torn, t, 0), h = 220 - 40 * torn;
  const blink = (Math.floor(t * 0.7 + i) % 4 === 0 && (t % 1.43) < 0.12);
  const mouth = face === 'worry' || face === 'sad' ? 'M -22 -' + (h - 150) + ' Q 0 -' + (h - 138) + ' 22 -' + (h - 150) : face === 'wow' ? '' : 'M -24 -' + (h - 146) + ' Q 0 -' + (h - 166) + ' 24 -' + (h - 146);
  const sway = Math.sin(t * 3 + i) * 3;
  return <g key={'sb' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <path d={`M -22 -14 L ${-26 + step * 12} 0 M 22 -14 L ${26 - step * 12} 0`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
    <path d={`M -70 ${-h + 70} L ${-110} ${-h + 120 + sway * 4} M 70 ${-h + 70} L 110 ${-h + 120 - sway * 4}`} stroke={OL} strokeWidth={7} strokeLinecap="round" />
    <g transform={`rotate(${sway})`}>
      <rect x={-70} y={-h - 14} width={140} height={h} rx={6} fill={PAPER} stroke={OL} strokeWidth={6} />
      {Array.from({length: Math.floor(h / 22)}, (_, q) => <circle key={q} cx={-70} cy={-h - 2 + q * 22} r={5} fill="#E6F4FF" stroke={OL} strokeWidth={2} />)}
      <rect x={-56} y={-h} width={112} height={34} rx={4} fill={GREEN} /><T x={0} y={-h + 26} s={24} c="#FFFFFF">PAY $</T>
      {face === 'wow' ? <g><circle cx={-24} cy={-h + 68} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={24} cy={-h + 68} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={-24} cy={-h + 68} r={5} fill={OL} /><circle cx={24} cy={-h + 68} r={5} fill={OL} />
        <ellipse cx={0} cy={-h + 106} rx={12} ry={14} fill={OL} /></g>
        : <g><ellipse cx={-24} cy={-h + 68} rx={8} ry={blink ? 2 : 10} fill={OL} /><ellipse cx={24} cy={-h + 68} rx={8} ry={blink ? 2 : 10} fill={OL} />
          {face === 'sad' && <path d={`M -36 ${-h + 52} L -14 ${-h + 58} M 36 ${-h + 52} L 14 ${-h + 58}`} stroke={OL} strokeWidth={4} />}
          <path d={mouth} stroke={OL} strokeWidth={5} fill="none" strokeLinecap="round" /></g>}
      {[0, 1].map((q) => <path key={q} d={`M -46 ${-h + 130 + q * 26} L ${30 - q * 20} ${-h + 130 + q * 26}`} stroke="#B0BEC5" strokeWidth={7} />)}
      <path d={`M -70 -14 ${Array.from({length: 7}, (_, q) => `L ${-70 + (q + 0.5) * 20} ${-14 + (q % 2 ? -10 : 8)}`).join(' ')} L 70 -14`} stroke={OL} strokeWidth={4} fill="none" opacity={torn > 0.05 ? 1 : 0} />
    </g>
    {a.label && t < (a.labelUntil ?? at + 3) && <g transform={`scale(${fl} 1)`}>{plaque(0, -h - 60, a.label, '#FFFFFF', 20)}</g>}
  </g>;
};

/** rivet: the friendly warehouse robot */
const rivet: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, moving = Math.abs(vx) > 20;
  const y = kf(a.y, t, f) - hopY(a, t) - (moving ? Math.abs(Math.sin(t * 12)) * 4 : Math.sin(t * 2 + i) * 3);
  const s = (a.scale ?? 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const face: string = pick(a.faces, t, a.face || 'happy'), fl = vx < -20 ? -1 : 1;
  const pk = a.pockets !== undefined ? E.outBack(win(t, a.pockets, 0.4)) : 0, hand = a.hand !== undefined ? E.inOut(win(t, a.hand, 0.5)) : 0;
  const blink = (Math.floor(t * 0.6 + i) % 5 === 0 && (t % 1.7) < 0.12);
  const eyes = face === 'wow' ? <g><circle cx={-26} cy={-262} r={14} fill={CY} /><circle cx={26} cy={-262} r={14} fill={CY} /></g>
    : face === 'worry' ? <g><rect x={-38} y={-268} width={24} height={blink ? 3 : 14} rx={5} fill={CY} /><rect x={14} y={-268} width={24} height={blink ? 3 : 14} rx={5} fill={CY} /><path d="M -40 -284 L -14 -278 M 40 -284 L 14 -278" stroke={CY} strokeWidth={4} /></g>
      : <g><rect x={-38} y={-274} width={24} height={blink ? 3 : 22} rx={6} fill={CY} /><rect x={14} y={-274} width={24} height={blink ? 3 : 22} rx={6} fill={CY} /></g>;
  const mouth = face === 'worry' ? 'M -22 -222 Q 0 -234 22 -222' : face === 'wow' ? 'M -10 -226 a 10 10 0 1 0 20 0 a 10 10 0 1 0 -20 0' : 'M -24 -230 Q 0 -212 24 -230';
  return <g key={'rv' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <ellipse cx={0} cy={0} rx={90} ry={14} fill="#000000" opacity={0.12} />
    <rect x={-80} y={-46} width={160} height={46} rx={23} fill="#5E6B85" stroke={OL} strokeWidth={5} />
    {[-50, 0, 50].map((q) => <circle key={q} cx={q} cy={-23} r={14} fill="#9AA6B8" stroke={OL} strokeWidth={3} transform={`rotate(${t * 300} ${q} -23)`} />)}
    <rect x={-70} y={-180} width={140} height={136} rx={18} fill={ORANGE} stroke={OL} strokeWidth={6} />
    <rect x={-40} y={-150} width={80} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-118} s={22} c={NAVY}>RIVET</T>
    {pk > 0 && <g>{[-1, 1].map((q) => <g key={q} transform={`translate(${q * 48} -70) scale(${pk})`}><path d="M -22 0 L 22 0 L 14 34 L -14 34 Z" fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={30} s={24} c={RED}>?</T></g>)}</g>}
    <g transform={`translate(-70 -160) rotate(${a.carry === 'box' ? -60 : 20 + Math.sin(t * 2.4 + i) * 6})`}><rect x={-14} y={0} width={28} height={110} rx={12} fill="#CFD8E3" stroke={OL} strokeWidth={5} /><circle cy={116} r={18} fill="#CFD8E3" stroke={OL} strokeWidth={5} /></g>
    <g transform={`translate(70 -160) rotate(${a.carry === 'box' ? 60 : lerp(-20 - Math.sin(t * 2.4 + i) * 6, -160 + Math.sin(t * 8) * 8, hand)})`}><rect x={-14} y={0} width={28} height={110} rx={12} fill="#CFD8E3" stroke={OL} strokeWidth={5} /><circle cy={116} r={18} fill="#CFD8E3" stroke={OL} strokeWidth={5} /></g>
    {a.carry === 'box' && <g transform="translate(0 -250)"><rect x={-70} y={-60} width={140} height={90} fill="#C99A5B" stroke={OL} strokeWidth={5} /><path d="M -70 -20 L 70 -20" stroke="#8A6236" strokeWidth={4} /></g>}
    <rect x={-14} y={-196} width={28} height={18} fill="#9AA6B8" stroke={OL} strokeWidth={4} />
    <g transform={a.carry === 'box' ? 'translate(0 -110)' : ''}>
      <rect x={-78} y={-310} width={156} height={118} rx={26} fill="#CFD8E3" stroke={OL} strokeWidth={6} /><rect x={-60} y={-294} width={120} height={86} rx={16} fill="#263238" />
      {eyes}<path d={mouth} stroke={CY} strokeWidth={5} fill={face === 'wow' ? CY : 'none'} strokeLinecap="round" />
      <path d="M 0 -310 L 0 -340" stroke={OL} strokeWidth={6} /><circle cy={-348} r={11} fill={(Math.floor(t * 2) % 2) ? RED : GOLD} stroke={OL} strokeWidth={4} /></g>
    {a.label && t < (a.labelUntil ?? at + 3) && <g transform={`scale(${fl} 1)`}>{plaque(0, -390, a.label, '#FFFFFF', 20)}</g>}
  </g>;
};

export const AITAXES_ITEMS: Record<string, ItemFn> = {stub, rivet};
export const AITAXES_INDOOR = ['txware', 'txpipes', 'txscale', 'txjars', 'txmeeting', 'txtitle', 'txbumper'];
