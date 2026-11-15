import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * SITCOM kit for CartoonStage (Episode 56, "How Black Friday Actually Makes Money").
 *
 * The owner asked for an episode that feels like a prime-time animated TV sitcom. Everything here is ORIGINAL (genre
 * level only): an expressive character rig (`toon`) with squash-and-stretch entrances, anticipation, overshoot, walk/run
 * cycles with smears and speed lines, blinking, lip-flap during `talk` windows, and a face library (happy, grin, panic,
 * smug, shock, deadpan, angry, dizzy, worry, dollar); a recurring cast (GLORIA the store manager, DASH the deal-hunter,
 * generic shoppers), TAGBOT (a deadpan price-tag printer robot), BUZZ (a delivery drone), LIFT (a forklift with headlight
 * eyes), a STAMPEDE crowd, speech BUBBLEs, a heaped CART that fills on cue, a swinging BIGTAG; and bespoke sets:
 * megamall (5 a.m.), philly61, tvfactory, quarterhq, payrails, bnplride, adarena, returnsmtn, plus the show TITLECARD and
 * act BUMPER sets (screen-filling, designed to be filmed with a static camera).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS).
 */
export const OL = '#10213A';
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
const inWins = (w: any, t: number) => Array.isArray(w) && w.some((p: any) => Array.isArray(p) && t >= Number(p[0]) && t <= Number(p[1]));
/** damped wobble after an event: 0 before, decays to 0 */
const jig = (t: number, at: number, k = 14, d = 5) => (t < at ? 0 : Math.exp(-d * (t - at)) * Math.sin(k * (t - at)));
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;
/** fits text into a box width (shrinks the font, never clips) */
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.62);
const SKIN = ['#F6CDA6', '#E0A878', '#B97A4B', '#8A5634', '#F3D7BD'];
const HAIR = ['#3E2723', '#1B1B1B', '#8D5524', '#F2C14E', '#C0392B', '#5D4037', '#B0BEC5'];
const SHIRT = ['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB', '#FFC93C', '#F06292', '#26A69A', '#FF7043', '#5C6BC0'];

/* ============================================================================================ CHARACTER RIG */
type Look = {skin: string; hair: string; hairStyle: number; top: string; pants: string; shoes: string; w: number; h: number;
  hat?: string; scarf?: string; glasses?: boolean; who: string};
const looks = (a: Item, i: number): Look => {
  if (a.who === 'gloria') return {who: 'gloria', skin: '#F2C29A', hair: '#B5452B', hairStyle: 10, top: '#D93A3A', pants: '#2C3E66', shoes: '#1B1B1B', w: 1, h: 1.08};
  if (a.who === 'dash') return {who: 'dash', skin: '#C98B5B', hair: '#17B3A3', hairStyle: 11, top: '#FF8A1F', pants: '#34406A', shoes: '#F2F2F2', w: 0.86, h: 1.12, scarf: undefined};
  const v = a.v ?? i;
  return {who: 'shopper', skin: SKIN[(a.skin ?? v * 3) % SKIN.length], hair: HAIR[(a.hair ?? v * 5 + 1) % HAIR.length], hairStyle: (a.hairStyle ?? v * 7) % 6,
    top: a.color ?? SHIRT[(v * 4 + 1) % SHIRT.length], pants: ['#2D3E66', '#4E342E', '#37474F', '#5D4E8C'][v % 4], shoes: ['#1B1B1B', '#ECEFF1', '#8D6E63'][v % 3],
    w: [1, 1.18, 0.9, 1.05, 1.28][v % 5], h: [1, 0.92, 1.08, 0.86, 0.96][(v * 3) % 5],
    hat: a.hat ?? (rnd(v * 9 + 2) > 0.62 ? ['#E53950', '#2F6FD1', '#2E9E5B', '#FFB300'][v % 4] : undefined),
    scarf: a.scarf ?? (rnd(v * 13 + 5) > 0.55 ? ['#FFB300', '#E53950', '#7E57C2', '#26A69A'][(v + 1) % 4] : undefined), glasses: a.glasses ?? rnd(v * 17) > 0.75};
};

/** two-segment noodle arm: angle from straight down (deg, + = forward), elbow bend (deg, + = forward/up) */
const limb = (sx: number, sy: number, ang: number, bend: number, l1: number, l2: number) => {
  const r1 = (ang * Math.PI) / 180, r2 = ((ang + bend) * Math.PI) / 180;
  const ex = sx + Math.sin(r1) * l1, ey = sy + Math.cos(r1) * l1;
  return {ex, ey, hx: ex + Math.sin(r2) * l2, hy: ey + Math.cos(r2) * l2};
};
const ARMS: Record<string, (t: number, i: number) => [number, number, number, number]> = {   // [backAng, backBend, frontAng, frontBend]
  stand: (t, i) => [8 + 3 * Math.sin(t * 2 + i), 12, -8 - 3 * Math.sin(t * 2 + i), 12],
  talk: (t, i) => [10, 15, 55 + 25 * Math.sin(t * 4.2 + i), 40 + 25 * Math.sin(t * 5.1 + i)],
  wave: (t) => [10, 12, 150, 20 + 35 * Math.sin(t * 13)],
  point: (t) => [12, 14, 92 + 4 * Math.sin(t * 3), 4],
  armsup: (t, i) => [165 + 14 * Math.sin(t * 15 + i), 10, 165 + 14 * Math.sin(t * 15 + i + 2), 10],
  cheer: (t) => [168 + 8 * Math.sin(t * 9), 0, 168 + 8 * Math.sin(t * 9 + 1), 0],
  hold: (t, i) => [70 + 3 * Math.sin(t * 6 + i), 45, 70 + 3 * Math.sin(t * 6 + i), 45],
  carry: (t, i) => [165, 15 + 6 * Math.sin(t * 9 + i), 165, 15 + 6 * Math.sin(t * 9 + i)],
  shrug: () => [100, 85, 100, 85],
  facepalm: () => [10, 12, 150, 140],
  clipboard: (t) => [62, 75, 60 + 8 * Math.sin(t * 7), 85 + 10 * Math.sin(t * 11)],
  sip: (t) => { const u = (t % 3.2) < 0.9 ? Math.sin(((t % 3.2) / 0.9) * Math.PI) : 0; return [12, 12, 60 + 70 * u, 70 + 60 * u]; },
  key: (t) => [12, 12, 85 + 8 * Math.sin(t * 9), 20],
  sit: (t, i) => [40, 50, 40 + 4 * Math.sin(t * 3 + i), 50],
};
const sweat = (t: number, k: number, x: number, y: number) => {
  const u = ((t * 1.6 + k * 0.37) % 1);
  return <path key={'sw' + k} transform={`translate(${x + (k % 2 ? 1 : -1) * u * 26} ${y + u * 40 - 10}) scale(${1 - u * 0.4})`} d="M 0 -10 Q 7 0 0 8 Q -7 0 0 -10 Z"
    fill="#8FDBFF" stroke={OL} strokeWidth={2.5} opacity={1 - u} />;
};

/**
 * `toon`: the sitcom character rig. Params: who ('gloria' | 'dash' | 'shopper' with v=variant), x/y keyframes,
 * pose / poses [[t,pose]], face / faces [[t,face]], talk [[t0,t1],...] (lip-flap), hold ('tv'|'bag'|'clipboard'|'coffee'|
 * 'tag'|'box'|'card'|'phone'), hops [t,...] (anticipation-squash jump), takes [t,...] (double-take shake), look (-1..1),
 * label (name tag on entrance), labelUntil.
 */
export const toon: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0;
  if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const L = looks(a, i), s0 = a.scale ?? 1;
  let x = kf(a.x, t, 960);
  const y = kf(a.y, t, f);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08;
  let pose: string = pick(a.poses, t, a.pose || 'stand');
  if ((pose === 'stand' || pose === 'talk') && Math.abs(vx) > 320) pose = 'run'; else if (pose === 'stand' && Math.abs(vx) > 30) pose = 'walk';
  const face: string = pick(a.faces, t, a.face || 'happy');
  const fl = a.flip !== undefined ? (a.flip ? -1 : 1) : (vx < -30 ? -1 : 1);
  const talking = inWins(a.talk, t) || pose === 'talk';
  if (L.who === 'dash') x += Math.sin(t * 57 + i) * 1.6;                                       // caffeine tremble
  // entrance: squash-and-stretch spring; exit: stretch up and zip
  const ent = t - at, sp = Math.exp(-5.5 * ent) * Math.cos(16 * ent);
  let sx = 1 - 0.28 * sp, sy = 1 + 0.32 * sp;
  let app = pop(t, at, 0.35);
  if (a.until !== undefined && t > a.until) { const u = win(t, a.until, 0.35); sx *= 1 - u * 0.7; sy *= 1 + u * 1.2; app *= 1 - u; }
  // hops: anticipation squash (0.12 s) -> stretch jump -> land squash
  let hy = 0;
  for (const h of (a.hops || []) as number[]) {
    const u = t - h;
    if (u > -0.14 && u < 0) { const q = (u + 0.14) / 0.14; sx *= 1 + 0.18 * q; sy *= 1 - 0.2 * q; }
    else if (u >= 0 && u < 0.55) { const q = u / 0.55; hy += Math.sin(q * Math.PI) * 120; sy *= 1 + 0.18 * Math.sin(q * Math.PI); sx *= 1 - 0.1 * Math.sin(q * Math.PI); }
    else if (u >= 0.55 && u < 0.8) { const q = jig(t, h + 0.55, 18, 9); sx *= 1 + 0.2 * q; sy *= 1 - 0.2 * q; }
  }
  let shake = 0;
  for (const k of (a.takes || []) as number[]) shake += jig(t, k, 40, 6) * 14;
  const run = pose === 'run', walk = pose === 'walk';
  const cyc = run ? t * 15 + i : walk ? t * 8.5 + i : 0, sw = Math.sin(cyc);
  const bob = run ? Math.abs(Math.cos(cyc)) * 14 : walk ? Math.abs(Math.cos(cyc)) * 6 : Math.sin(t * 2.2 + i) * 2.5;
  const lean = run ? 14 : walk ? 4 : pose === 'armsup' ? -3 + 3 * Math.sin(t * 15) : 0;
  const W = L.w, H = L.h;
  const hipY = -72 * H, shY = -150 * H, headY = -205 * H;
  // arms
  let [ba, bb, fa, fb] = (ARMS[pose] || ARMS.stand)(t, i);
  if (run) { ba = -55 * sw; bb = 80; fa = 55 * sw; fb = 80; }
  if (walk) { ba = -28 * sw; bb = 20; fa = 28 * sw; fb = 20; }
  if (a.hold && (pose === 'run' || pose === 'walk' || pose === 'stand')) { ba = 70 + 4 * sw; bb = 45; fa = 70 - 4 * sw; fb = 45; }
  const back = limb(-24 * W, shY + 8, ba, bb, 40, 38), front = limb(24 * W, shY + 8, fa, fb, 40, 38);
  // legs
  const legA = run ? 42 * sw : walk ? 22 * sw : pose === 'sit' ? 80 : 0, legB = -legA;
  const knee = (ang: number) => (run ? Math.max(0, -ang) * 1.3 + 20 : walk ? Math.max(0, -ang) * 0.8 : pose === 'sit' ? -80 : 0);
  const l1 = limb(-12 * W, hipY, legA, -knee(legA), 36 * H, 36 * H), l2 = limb(12 * W, hipY, legB, -knee(legB), 36 * H, 36 * H);
  const ink = (d: string, c: string, w: number) => <g><path d={d} stroke={OL} strokeWidth={w + 8} strokeLinecap="round" strokeLinejoin="round" fill="none" /><path d={d} stroke={c} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" fill="none" /></g>;
  const armD = (p: any, sxp: number) => `M ${sxp} ${shY + 8} L ${p.ex} ${p.ey} L ${p.hx} ${p.hy}`;
  // face
  const blink = ((t + rnd(i) * 3) % 3.3) < 0.12 || face === 'deadpan' && ((t + i) % 4.1) < 0.1;
  const eyeS = face === 'shock' ? 1.55 : face === 'panic' ? 1.3 : face === 'smug' || face === 'deadpan' ? 1 : 1.08;
  const pupR = face === 'shock' || face === 'panic' ? 3.2 : 6;
  const lookX = (a.look ?? 0.4) * 4 + (face === 'panic' ? Math.sin(t * 23) * 2.5 : 0);
  const lid = face === 'smug' || face === 'deadpan' ? 0.5 : face === 'angry' ? 0.3 : 0;
  const flap = talking ? clamp(0.5 + 0.5 * Math.sin(t * 21 + i) * Math.sin(t * 7.3 + i * 2) + 0.15 * Math.sin(t * 37)) : 0;
  const ex1 = -15, ex2 = 17, ey = headY - 6;
  const eye = (cx: number, k: number) => <g key={'e' + k}>
    {blink ? <path d={`M ${cx - 12} ${ey} Q ${cx} ${ey + 5} ${cx + 12} ${ey}`} stroke={OL} strokeWidth={4} fill="none" strokeLinecap="round" />
      : face === 'dizzy' ? <g transform={`translate(${cx} ${ey}) rotate(${t * 720 * (k ? 1 : -1)})`}><ellipse rx={13} ry={15} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
        <path d="M 0 0 Q 6 -3 4 4 Q -2 9 -7 2 Q -9 -7 1 -9 Q 11 -9 10 2" fill="none" stroke={OL} strokeWidth={2.5} /></g>
      : <g><ellipse cx={cx} cy={ey} rx={13 * eyeS} ry={16 * eyeS} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
        {face === 'dollar' ? <T x={cx + lookX} y={ey + 8} s={22} c="#1E9E52">$</T>
          : face === 'love' ? <path transform={`translate(${cx + lookX} ${ey}) scale(${0.9 + 0.15 * Math.sin(t * 9)})`} d="M 0 6 L -7 -1 Q -9 -7 -4 -8 Q 0 -8 0 -4 Q 0 -8 4 -8 Q 9 -7 7 -1 Z" fill="#E53950" />
          : <circle cx={cx + lookX} cy={ey + 2} r={pupR} fill={OL} />}
        {face !== 'dollar' && face !== 'love' && <circle cx={cx + lookX + 2} cy={ey - 1} r={1.6} fill="#FFFFFF" />}
        {lid > 0 && <path d={`M ${cx - 14} ${ey - 17} L ${cx + 14} ${ey - 17} L ${cx + 14} ${ey - 17 + 32 * lid} L ${cx - 14} ${ey - 17 + 32 * lid} Z`} fill={L.skin} stroke={OL} strokeWidth={3} />}
      </g>}
  </g>;
  const browY = ey - 22 * eyeS;
  const brow = (cx: number, k: number) => { const dir = k ? 1 : -1;
    const tilt = face === 'angry' ? -10 * dir : face === 'panic' || face === 'worry' ? 9 * dir : face === 'smug' ? (k ? -8 : 2) : face === 'shock' ? 0 : -2 * dir;
    const lift = face === 'shock' ? -10 : face === 'panic' ? -6 : face === 'happy' || face === 'grin' ? -3 : 0;
    return <path key={'b' + k} d={`M ${cx - 11} ${browY + lift - tilt * 0.5} L ${cx + 11} ${browY + lift + tilt * 0.5}`} stroke={L.who === 'dash' ? '#0E7A70' : OL} strokeWidth={5} strokeLinecap="round" />; };
  const my = headY + 28;
  let mouth: React.ReactNode;
  if (talking || flap > 0) {
    const o = 3 + 15 * flap;
    mouth = <g><path d={`M -12 ${my - 2} Q 2 ${my - 6} 14 ${my - 2} Q 12 ${my + o} 1 ${my + o + 2} Q -10 ${my + o} -12 ${my - 2} Z`} fill="#6B2E2A" stroke={OL} strokeWidth={3.5} strokeLinejoin="round" />
      {o > 9 && <ellipse cx={2} cy={my + o - 2} rx={6} ry={3} fill="#F48FB1" />}</g>;
  } else if (face === 'grin' || face === 'dollar' || face === 'love') {
    mouth = <g><path d={`M -16 ${my - 4} Q 2 ${my - 2} 20 ${my - 4} Q 16 ${my + 16} 2 ${my + 16} Q -12 ${my + 16} -16 ${my - 4} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} strokeLinejoin="round" />
      <path d={`M -14 ${my + 3} L 18 ${my + 3}`} stroke={OL} strokeWidth={2} /></g>;
  } else if (face === 'shock') {
    const o = 22 + 6 * Math.sin(t * 9);
    mouth = <ellipse cx={2} cy={my + o / 2 - 2} rx={11} ry={o / 2} fill="#6B2E2A" stroke={OL} strokeWidth={3.5} />;
  } else if (face === 'panic') {
    mouth = <path d={`M -12 ${my + 6} Q -6 ${my - 4} 0 ${my + 6} Q 6 ${my - 4} 14 ${my + 6} Q 2 ${my + 18} -12 ${my + 6} Z`} fill="#6B2E2A" stroke={OL} strokeWidth={3.5} strokeLinejoin="round" />;
  } else if (face === 'smug') {
    mouth = <path d={`M -10 ${my + 2} Q 6 ${my + 6} 16 ${my - 6}`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />;
  } else if (face === 'deadpan') {
    mouth = <path d={`M -10 ${my + 3} L 14 ${my + 3}`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />;
  } else if (face === 'angry') {
    mouth = <g><rect x={-13} y={my - 2} width={28} height={12} rx={3} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><path d={`M -13 ${my + 4} L 15 ${my + 4} M -4 ${my - 2} L -4 ${my + 10} M 6 ${my - 2} L 6 ${my + 10}`} stroke={OL} strokeWidth={2} /></g>;
  } else if (face === 'worry' || face === 'dizzy') {
    mouth = <path d={`M -11 ${my + 6} Q -5 ${my} 0 ${my + 5} Q 6 ${my + 10} 13 ${my + 3}`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />;
  } else {
    mouth = <path d={`M -12 ${my - 2} Q 2 ${my + 13} 16 ${my - 2}`} fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />;
  }
  // hair (back layer / front layer)
  const hr = L.hairStyle, hc = L.hair;
  const hairBack = hr === 10 ? <g><circle cx={-6} cy={headY - 58} r={30} fill={hc} stroke={OL} strokeWidth={4} /><path d={`M -2 ${headY - 92} L 18 ${headY - 40}`} stroke="#FFC93C" strokeWidth={6} strokeLinecap="round" /><path d={`M 16 ${headY - 46} L 20 ${headY - 36}`} stroke="#F48FB1" strokeWidth={6} strokeLinecap="round" /></g>
    : hr === 4 ? <path d={`M -46 ${headY} Q -52 ${headY + 60} -30 ${headY + 70} L 30 ${headY + 70} Q 52 ${headY + 60} 46 ${headY} Z`} fill={hc} stroke={OL} strokeWidth={4} /> : null;
  const hairFront = hr === 11 ? <path d={`M -44 ${headY - 8} L -52 ${headY - 46} L -28 ${headY - 40} L -30 ${headY - 76} L -6 ${headY - 52} L 6 ${headY - 88} L 18 ${headY - 52} L 42 ${headY - 74} L 34 ${headY - 34} L 52 ${headY - 30} L 44 ${headY - 6} Q 0 ${headY - 34} -44 ${headY - 8} Z`} fill={hc} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
    : hr === 10 ? <path d={`M -46 ${headY - 2} Q -50 ${headY - 52} 0 ${headY - 52} Q 48 ${headY - 54} 46 ${headY - 4} Q 30 ${headY - 34} 4 ${headY - 30} Q -24 ${headY - 34} -46 ${headY - 2} Z`} fill={hc} stroke={OL} strokeWidth={4} />
    : [<path key={0} d={`M -45 ${headY - 2} Q -44 ${headY - 52} 0 ${headY - 50} Q 44 ${headY - 52} 45 ${headY - 2} Q 24 ${headY - 30} -45 ${headY - 2} Z`} fill={hc} stroke={OL} strokeWidth={4} />,
      <path key={1} d={`M -40 ${headY - 20} Q -30 ${headY - 64} 10 ${headY - 56} Q 46 ${headY - 46} 42 ${headY - 16} L 30 ${headY - 34} L 18 ${headY - 26} L 6 ${headY - 36} L -10 ${headY - 26} L -24 ${headY - 36} Z`} fill={hc} stroke={OL} strokeWidth={4} strokeLinejoin="round" />,
      <path key={2} d={`M -44 ${headY - 10} Q -40 ${headY - 50} 0 ${headY - 48} Q 40 ${headY - 50} 44 ${headY - 10} L 44 ${headY - 26} Q 0 ${headY - 40} -44 ${headY - 26} Z`} fill={hc} stroke={OL} strokeWidth={4} />,
      <g key={3}><path d={`M -42 ${headY - 14} Q -40 ${headY - 50} 0 ${headY - 50} Q 40 ${headY - 50} 42 ${headY - 14} Q 0 ${headY - 34} -42 ${headY - 14} Z`} fill={hc} stroke={OL} strokeWidth={4} />{[-30, -10, 10, 30].map((c) => <circle key={c} cx={c} cy={headY - 50} r={12} fill={hc} stroke={OL} strokeWidth={3} />)}</g>,
      <path key={4} d={`M -46 ${headY + 6} Q -50 ${headY - 52} 0 ${headY - 52} Q 50 ${headY - 52} 46 ${headY + 6} Q 30 ${headY - 30} -46 ${headY + 6} Z`} fill={hc} stroke={OL} strokeWidth={4} />,
      <path key={5} d={`M -30 ${headY - 40} Q 0 ${headY - 58} 30 ${headY - 40}`} fill="none" stroke={hc} strokeWidth={8} strokeLinecap="round" />][hr % 6];
  // held props (drawn at the front hand)
  const hmx = (back.hx + front.hx) / 2, hmy = (back.hy + front.hy) / 2;
  const held = (() => {
    switch (a.hold) {
      case 'tv': return <g transform={`translate(${hmx + 10} ${hmy - 30}) rotate(${run ? 4 * sw : 0})`}><rect x={-62} y={-48} width={124} height={88} rx={6} fill="#D7A86E" stroke={OL} strokeWidth={4} />
        <rect x={-46} y={-38} width={92} height={56} rx={4} fill="#263238" stroke={OL} strokeWidth={3} /><path d="M -40 -30 L -10 -30" stroke="#80DEEA" strokeWidth={4} opacity={0.7} />
        <rect x={-50} y={22} width={100} height={14} rx={3} fill="#E53950" stroke={OL} strokeWidth={2.5} /><T x={0} y={33} s={11} c="#FFFFFF">DOORBUSTER</T></g>;
      case 'bag': return <g transform={`translate(${front.hx} ${front.hy + 22}) rotate(${10 * sw})`}><path d="M -10 -24 Q 0 -40 10 -24" fill="none" stroke={OL} strokeWidth={4} /><rect x={-24} y={-24} width={48} height={50} rx={6} fill={['#FFC93C', '#E53950', '#4FB3F6'][i % 3]} stroke={OL} strokeWidth={4} /></g>;
      case 'box': return <g transform={`translate(${hmx + 6} ${hmy - 26})`}><rect x={-44} y={-40} width={88} height={70} rx={5} fill="#D7A86E" stroke={OL} strokeWidth={4} /><path d="M -44 -14 L 44 -14 M 0 -40 L 0 -14" stroke="#A9783F" strokeWidth={4} />{a.boxText && <T x={0} y={18} s={fit(String(a.boxText), 80, 15)}>{a.boxText}</T>}</g>;
      case 'clipboard': return <g transform={`translate(${back.hx + 8} ${back.hy - 26}) rotate(-8)`}><rect x={-26} y={-34} width={52} height={66} rx={5} fill="#A1887F" stroke={OL} strokeWidth={3.5} /><rect x={-20} y={-26} width={40} height={52} fill="#FFFFFF" stroke={OL} strokeWidth={2} />
        {[0, 1, 2, 3].map((l) => <path key={l} d={`M -14 ${-18 + l * 11} L ${4 + 10 * ((l + Math.floor(t * 3)) % 2)} ${-18 + l * 11}`} stroke={OL} strokeWidth={2} opacity={0.6} />)}<rect x={-10} y={-38} width={20} height={8} rx={2} fill="#B0BEC5" stroke={OL} strokeWidth={2} /></g>;
      case 'coffee': return <g transform={`translate(${front.hx} ${front.hy - 12}) rotate(${pose === 'sip' && (t % 3.2) < 0.9 ? -40 * Math.sin(((t % 3.2) / 0.9) * Math.PI) : 0})`}><rect x={-12} y={-34} width={24} height={46} rx={5} fill="#90A4AE" stroke={OL} strokeWidth={3.5} /><rect x={-14} y={-40} width={28} height={10} rx={3} fill="#37474F" stroke={OL} strokeWidth={3} />
        {[0, 1].map((k) => { const u = (t * 0.9 + k * 0.5) % 1; return <path key={k} d={`M ${-4 + k * 8} ${-46 - u * 30} q 6 -8 0 -16`} stroke="#B0BEC5" strokeWidth={3} fill="none" opacity={1 - u} />; })}</g>;
      case 'tag': return <g transform={`translate(${front.hx + 10} ${front.hy - 8}) rotate(${8 * Math.sin(t * 4)})`}><path d="M -6 0 L 18 -16 L 70 -16 L 70 16 L 18 16 Z" fill="#FFF8E1" stroke={OL} strokeWidth={3.5} strokeLinejoin="round" /><circle cx={8} cy={0} r={4} fill={OL} /><T x={44} y={6} s={14} c="#E53950">{a.tagText || 'SALE'}</T></g>;
      case 'card': return <g transform={`translate(${front.hx + 8} ${front.hy - 6}) rotate(-15)`}><rect x={-6} y={-22} width={64} height={40} rx={6} fill="#2F6FD1" stroke={OL} strokeWidth={3.5} /><rect x={2} y={-12} width={14} height={10} rx={2} fill="#FFC93C" /></g>;
      case 'phone': return <g transform={`translate(${front.hx + 4} ${front.hy - 10})`}><rect x={-10} y={-26} width={22} height={38} rx={5} fill="#263238" stroke={OL} strokeWidth={3} /><rect x={-6} y={-21} width={14} height={26} rx={2} fill="#80DEEA" opacity={0.6 + 0.4 * Math.sin(t * 6)} /></g>;
      default: return null;
    }
  })();
  const lab: string | null = a.label && t < (a.labelUntil ?? at + 4) ? String(a.label) : null;
  const smear = run ? <g opacity={0.35}>{[1, 2, 3].map((k) => <path key={k} d={`M ${-60 - k * 22} ${-180 * H + k * 38} L ${-150 - k * 34} ${-180 * H + k * 38}`} stroke={OL} strokeWidth={5} strokeLinecap="round" />)}</g> : null;
  const dust = run ? [0, 1, 2].map((k) => { const u = ((t * 2.2 + k / 3) % 1); return <circle key={'d' + k} cx={-30 - u * 90} cy={-8 - u * 24} r={8 + u * 22} fill="#E8DCC8" stroke={OL} strokeWidth={3} opacity={0.85 * (1 - u)} />; }) : null;
  return <g key={'toon' + i} transform={`translate(${x + shake} ${y - bob - hy}) scale(${s0 * app * fl * sx} ${s0 * app * sy})`}>
    {dust}{smear}
    <ellipse cx={0} cy={4 + hy / Math.max(0.01, s0)} rx={46 * W} ry={10} fill={OL} opacity={0.18} />
    <g transform={`rotate(${lean})`}>
      {ink(`M ${-12 * W} ${hipY} L ${l1.ex} ${l1.ey} L ${l1.hx} ${l1.hy}`, L.pants, 19)}
      {ink(`M ${12 * W} ${hipY} L ${l2.ex} ${l2.ey} L ${l2.hx} ${l2.hy}`, L.pants, 19)}
      <ellipse cx={l1.hx + 9} cy={l1.hy - 2} rx={17} ry={10} fill={L.shoes} stroke={OL} strokeWidth={4} />
      <ellipse cx={l2.hx + 9} cy={l2.hy - 2} rx={17} ry={10} fill={L.shoes} stroke={OL} strokeWidth={4} />
      {hairBack && <g opacity={hr === 4 ? 1 : 1}>{hr === 4 ? hairBack : null}</g>}
      {ink(armD(back, -24 * W), L.top, 17)}
      <circle cx={back.hx} cy={back.hy} r={11} fill={L.skin} stroke={OL} strokeWidth={4} />
      {/* torso */}
      <path d={`M ${-30 * W} ${shY} Q ${-36 * W} ${hipY + 8} ${-26 * W} ${hipY + 6} L ${26 * W} ${hipY + 6} Q ${36 * W} ${hipY + 8} ${30 * W} ${shY} Q 0 ${shY - 14} ${-30 * W} ${shY} Z`}
        fill={L.top} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
      {L.who === 'gloria' && <g><path d={`M -8 ${shY - 6} L 0 ${shY + 30} L 8 ${shY - 6}`} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><rect x={6} y={shY + 18} width={40} height={18} rx={3} fill="#FFFFFF" stroke={OL} strokeWidth={2.5} /><T x={26} y={shY + 31} s={9}>MANAGER</T></g>}
      {L.who === 'dash' && <g><path d={`M -22 ${shY + 40} L 22 ${shY + 40}`} stroke="#C7621A" strokeWidth={4} /><rect x={-14} y={shY + 6} width={30} height={16} rx={3} fill="#FFF3B0" stroke={OL} strokeWidth={2.5} /><T x={1} y={shY + 18} s={10}>DEALS</T>
        {[0, 1, 2].map((k) => <rect key={k} x={-30 + k * 22} y={hipY - 4} width={18} height={12} fill="#FFF8E1" stroke={OL} strokeWidth={2} transform={`rotate(${-10 + k * 10} ${-21 + k * 22} ${hipY + 2})`} />)}</g>}
      {L.scarf && <path d={`M -28 ${shY - 2} Q 0 ${shY + 12} 28 ${shY - 2} L 26 ${shY + 8} Q 0 ${shY + 22} -26 ${shY + 8} Z M 10 ${shY + 12} L 18 ${shY + 44} L 4 ${shY + 44} Z`} fill={L.scarf} stroke={OL} strokeWidth={3} strokeLinejoin="round" />}
      {/* head */}
      <g transform={`rotate(${face === 'shock' ? -4 : pose === 'talk' ? 3 * Math.sin(t * 3 + i) : Math.sin(t * 1.3 + i) * 2} 0 ${headY + 40})`}>
        {hr === 10 && hairBack}
        <rect x={-12} y={headY + 34} width={24} height={20} fill={L.skin} stroke={OL} strokeWidth={3.5} />
        <ellipse cx={-44} cy={headY + 2} rx={8} ry={11} fill={L.skin} stroke={OL} strokeWidth={3.5} />
        <ellipse cx={0} cy={headY} rx={46} ry={50} fill={L.skin} stroke={OL} strokeWidth={4.5} />
        {L.who === 'dash' && <g opacity={0.5}><path d={`M ${ex1 - 10} ${ey + 18} Q ${ex1} ${ey + 24} ${ex1 + 10} ${ey + 18}`} stroke="#7A4A9A" strokeWidth={3} fill="none" /><path d={`M ${ex2 - 10} ${ey + 18} Q ${ex2} ${ey + 24} ${ex2 + 10} ${ey + 18}`} stroke="#7A4A9A" strokeWidth={3} fill="none" /></g>}
        {eye(ex1, 0)}{eye(ex2, 1)}
        {brow(ex1, 0)}{brow(ex2, 1)}
        <path d={`M 26 ${headY + 4} Q 40 ${headY + 12} 28 ${headY + 18}`} fill={L.skin} stroke={OL} strokeWidth={3.5} strokeLinecap="round" />
        {mouth}
        {(face === 'happy' || face === 'grin') && <g opacity={0.35}><ellipse cx={-28} cy={headY + 20} rx={8} ry={5} fill="#FF6F61" /><ellipse cx={34} cy={headY + 20} rx={7} ry={5} fill="#FF6F61" /></g>}
        {hairFront}
        {L.glasses && <g><circle cx={ex1} cy={ey} r={17} fill="none" stroke={OL} strokeWidth={3.5} /><circle cx={ex2} cy={ey} r={17} fill="none" stroke={OL} strokeWidth={3.5} /><path d={`M ${ex1 + 17} ${ey} L ${ex2 - 17} ${ey}`} stroke={OL} strokeWidth={3} /></g>}
        {L.hat && <g><path d={`M -46 ${headY - 26} Q 0 ${headY - 92} 46 ${headY - 26} Z`} fill={L.hat} stroke={OL} strokeWidth={4} /><rect x={-48} y={headY - 34} width={96} height={16} rx={7} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /><circle cx={0} cy={headY - 76} r={11} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} /></g>}
        {L.who === 'gloria' && <g><path d={`M -48 ${headY - 6} Q -56 ${headY - 50} 0 ${headY - 58} Q 56 ${headY - 50} 48 ${headY - 6}`} fill="none" stroke="#37474F" strokeWidth={5} /><rect x={-56} y={headY - 14} width={14} height={22} rx={5} fill="#37474F" stroke={OL} strokeWidth={3} /><path d={`M -50 ${headY + 8} Q -40 ${headY + 40} -8 ${headY + 34}`} fill="none" stroke="#37474F" strokeWidth={4} /><circle cx={-8} cy={headY + 34} r={5} fill={OL} /></g>}
        {(face === 'panic' || face === 'worry') && [0, 1].map((k) => sweat(t, k + i, 40, headY - 30))}
        {face === 'angry' && [0, 1].map((k) => { const u = (t * 1.4 + k * 0.5) % 1; return <circle key={'st' + k} cx={(k ? 30 : -30) + (k ? 1 : -1) * u * 30} cy={headY - 60 - u * 50} r={10 + u * 14} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={1 - u} />; })}
        {face === 'dizzy' && [0, 1, 2].map((k) => { const ang = t * 4 + (k * Math.PI * 2) / 3; return <path key={'dz' + k} transform={`translate(${Math.cos(ang) * 50} ${headY - 62 + Math.sin(ang) * 12})`} d="M 0 -10 L 3 -3 L 10 -3 L 4 2 L 6 10 L 0 5 L -6 10 L -4 2 L -10 -3 L -3 -3 Z" fill="#FFD54F" stroke={OL} strokeWidth={2} />; })}
        {face === 'shock' && <g transform={`translate(0 ${headY - 92}) scale(${0.9 + 0.1 * Math.sin(t * 12)})`}><T x={0} y={0} s={56} c="#E53950" st={OL} sw={6}>!</T></g>}
      </g>
      {ink(armD(front, 24 * W), L.top, 17)}
      <circle cx={front.hx} cy={front.hy} r={11} fill={L.skin} stroke={OL} strokeWidth={4} />
      {held}
    </g>
    {lab && <g transform={`translate(0 ${headY - 120}) scale(${fl} 1) scale(${pop(t, at + 0.2, 0.4)})`}>
      <rect x={-lab.length * 9 - 18} y={-26} width={lab.length * 18 + 36} height={40} rx={20} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
      <T x={0} y={2} s={22}>{lab}</T></g>}
  </g>;
};

/** `stampede`: a crowd of generic shoppers sprinting from x0 to x1 starting at `at` (staggered), dust cloud behind. */
export const stampede: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0, n = a.n ?? 14, x0 = a.x0 ?? -400, x1 = a.x1 ?? 2400, dur = a.dur ?? 3.2, y = kf(a.y, t, f);
  if (t < at - 0.2 || (a.until !== undefined && t > a.until + 0.4)) return null;
  const out: React.ReactNode[] = [];
  for (let k = 0; k < n; k++) {
    const st = at + (k % 7) * 0.16 + Math.floor(k / 7) * 0.5 + rnd(k + i) * 0.1, row = k % 3;
    const u = clamp((t - st) / dur);
    if (t < st) continue;
    const xx = lerp(x0, x1, E.in(u) * 0.35 + u * 0.65), sc = (a.scale ?? 0.8) * (0.82 + 0.12 * row);
    out.push(<g key={k}>{toon({kind: 'toon', who: 'shopper', v: k + (a.seed ?? 0), x: xx, y: y - 30 + row * 26, at: st, pose: 'run', face: ['grin', 'panic', 'dollar', 'grin', 'angry'][k % 5],
      hold: ['bag', undefined, 'tv', undefined, 'box', undefined][k % 6] as any, scale: sc, flip: x1 < x0}, {t, f}, 900 + k)}</g>);
  }
  const cu = clamp((t - at) / (dur * 1.2));
  const cloud = cu > 0 && cu < 1 ? Array.from({length: 9}, (_, k) => { const cx = lerp(x0, x1, cu) - (x1 > x0 ? 1 : -1) * (120 + k * 70), r = 40 + rnd(k * 3) * 50 + 30 * Math.sin(t * 5 + k);
    return <circle key={'cl' + k} cx={cx} cy={y - 40 - rnd(k) * 80} r={r} fill="#EFE3CF" stroke={OL} strokeWidth={4} opacity={0.9 * (1 - cu)} />; }) : null;
  return <g key={'stp' + i}>{cloud}{out}</g>;
};

/** comic speech bubble with a tail pointing at [tx,ty]; wobbles in, holds, pops out at `until` */
export const bubble: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), txt: string = a.text || '', size = a.size ?? 34;
  const lines = txt.split('\n'), w = Math.max(...lines.map((l) => l.length)) * size * 0.6 + 56, h = lines.length * size * 1.15 + 34;
  const u = E.outBack(win(t, at, 0.35)) * (a.until !== undefined ? 1 - win(t, a.until, 0.3) : 1);
  const tx = (a.tail?.[0] ?? x) - x, ty = (a.tail?.[1] ?? y + h) - y;
  const shout = a.shout;
  const shape = shout ? (() => { const n = 14; let d = ''; for (let k = 0; k <= n * 2; k++) { const ang = (k / (n * 2)) * Math.PI * 2, r = k % 2 ? 1 : 1.16;
    d += (k ? ' L ' : 'M ') + (Math.cos(ang) * (w / 2) * r).toFixed(1) + ' ' + (Math.sin(ang) * (h / 2) * r).toFixed(1); } return d + ' Z'; })() : null;
  return <g key={'bb' + i} transform={`translate(${x} ${y}) scale(${u}) rotate(${Math.sin(t * 2.4 + i) * 1.5})`}>
    <path d={`M -18 ${h / 2 - 8} L ${tx} ${ty} L 18 ${h / 2 - 8} Z`} fill={a.color || '#FFFFFF'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
    {shape ? <path d={shape} fill={a.color || '#FFF59D'} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      : <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={Math.min(h / 2, 30)} fill={a.color || '#FFFFFF'} stroke={OL} strokeWidth={5} />}
    <path d={`M -14 ${h / 2 - 9} L 14 ${h / 2 - 9}`} stroke={a.color || (shape ? '#FFF59D' : '#FFFFFF')} strokeWidth={6} />
    {lines.map((l, k) => <T key={k} x={0} y={-h / 2 + 17 + size * 0.95 + k * size * 1.15} s={size} c={a.ink || OL}>{l}</T>)}
  </g>;
};

/** TAGBOT: deadpan price-tag printer robot on one wheel. prints [[t, text]], face/faces ('deadpan'|'happy'|'alarm'|'dollar'|'wink'), x keyframes, talk windows */
export const tagbot: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45);
  const vx = (kf(a.x, t + 0.04, 960) - kf(a.x, t - 0.04, 960)) / 0.08, fl = a.flip ? -1 : 1;
  const face: string = pick(a.faces, t, a.face || 'deadpan');
  const prints: [number, string][] = (a.prints || []).map((p: any) => [Number(p[0]), String(p[1])]);
  const cur = prints.filter((p) => t >= p[0]), last = cur[cur.length - 1];
  const talking = inWins(a.talk, t);
  const lean = clamp(vx / 600, -1, 1) * 12, wob = Math.sin(t * 3 + i) * 2 + jig(t, last?.[0] ?? -9, 20, 6) * 6;
  const printing = last && t - last[0] < 0.6;
  const scr = '#0E1E36', led = face === 'alarm' ? (Math.sin(t * 14) > 0 ? '#FF5252' : '#7A1A1A') : '#5CF2FF';
  const eyes = (() => {
    if (face === 'happy') return <g>{[-26, 26].map((c) => <path key={c} d={`M ${c - 12} -132 Q ${c} -150 ${c + 12} -132`} stroke={led} strokeWidth={6} fill="none" strokeLinecap="round" />)}</g>;
    if (face === 'alarm') return <g>{[-26, 26].map((c) => <circle key={c} cx={c} cy={-136} r={12} stroke={led} strokeWidth={6} fill="none" />)}</g>;
    if (face === 'dollar') return <g>{[-26, 26].map((c) => <T key={c} x={c} y={-124} s={34} c="#7CFF8A">$</T>)}</g>;
    if (face === 'wink') return <g><path d="M -38 -136 L -14 -136" stroke={led} strokeWidth={6} strokeLinecap="round" /><rect x={16} y={-148} width={20} height={22} rx={4} fill={led} /></g>;
    const bl = ((t + i) % 3.7) < 0.12;
    return <g>{[-26, 26].map((c) => bl ? <path key={c} d={`M ${c - 12} -136 L ${c + 12} -136`} stroke={led} strokeWidth={6} strokeLinecap="round" />
      : <rect key={c} x={c - 12} y={-142} width={24} height={10} rx={3} fill={led} />)}</g>;
  })();
  const mouthW = talking ? 18 + 14 * Math.abs(Math.sin(t * 19)) : 30;
  const tagEl = (txt: string, u: number, k: number) => {
    const lines = txt.split('\n'), w = Math.max(150, Math.max(...lines.map((l) => l.length)) * 17 + 40), h = 36 + lines.length * 30;
    return <g key={'tg' + k} transform={`translate(0 ${-78 + u * (h * 0.5 + 20)}) rotate(${(1 - u) * 6 + Math.sin(t * 3) * 2})`}>
      <path d={`M ${-w / 2} -12 L ${-w / 2 + 18} -26 L ${w / 2} -26 L ${w / 2} ${h - 26} L ${-w / 2 + 18} ${h - 26} L ${-w / 2} ${h - 40} Z`} fill="#FFFDF4" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      <circle cx={-w / 2 + 16} cy={-6} r={5} fill={OL} />
      {lines.map((l, q) => <T key={q} x={8} y={6 + q * 30} s={fit(l, w - 50, 26)} c={q === 0 && lines.length > 1 ? '#6B7385' : '#E53950'}>{l}</T>)}
    </g>;
  };
  // previous tags fall to a pile at the robot's side
  const pile = cur.slice(0, -1).map((p, k) => { const nt = prints[prints.indexOf(p) + 1]?.[0] ?? t, u = clamp((t - nt) / 0.6);
    return <g key={'pl' + k} transform={`translate(${70 + (k % 3) * 34 + u * 40} ${lerp(-60, -10 - k * 6, E.in(u))}) rotate(${u * (40 + k * 25)}) scale(0.5)`}>{tagEl(p[1], 1, k)}</g>; });
  return <g key={'tb' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <ellipse cx={0} cy={4} rx={70} ry={11} fill={OL} opacity={0.18} />
    <g transform={`rotate(${lean + wob})`}>
      {/* wheel */}
      <g transform="translate(0 -30)"><circle r={30} fill="#37474F" stroke={OL} strokeWidth={5} /><circle r={12} fill="#B0BEC5" stroke={OL} strokeWidth={3} />
        <path transform={`rotate(${x * 2})`} d="M -26 0 L 26 0 M 0 -26 L 0 26" stroke="#90A4AE" strokeWidth={4} /></g>
      <path d="M -16 -60 L -16 -40 M 16 -60 L 16 -40" stroke={OL} strokeWidth={8} />
      {/* body */}
      <rect x={-78} y={-200} width={156} height={142} rx={26} fill="#F3EEDC" stroke={OL} strokeWidth={5} />
      <rect x={-78} y={-104} width={156} height={20} fill="#2F6FD1" stroke={OL} strokeWidth={4} />
      <rect x={-62} y={-186} width={124} height={72} rx={14} fill={scr} stroke={OL} strokeWidth={4} />
      {eyes}
      {/* print slot (mouth) */}
      <rect x={-mouthW} y={-82} width={mouthW * 2} height={12} rx={5} fill="#1B1B1B" stroke={OL} strokeWidth={3} />
      {last && <g clipPath={undefined}>{tagEl(last[1], printing ? E.out(win(t, last[0], 0.6)) : 1, 99)}</g>}
      {/* arms */}
      {[-1, 1].map((sd) => { const wv = sd > 0 ? Math.sin(t * 4 + i) * 20 + (printing ? 30 : 0) : -10;
        return <g key={sd} transform={`translate(${sd * 78} -150) rotate(${sd * (40 + wv)})`}>
          <path d="M 0 0 L 0 40 L 6 44 L -6 50 L 6 56 L 0 60 L 0 74" stroke={OL} strokeWidth={6} fill="none" strokeLinejoin="round" />
          <path d="M -10 74 L -14 92 M 10 74 L 14 92" stroke={OL} strokeWidth={6} strokeLinecap="round" /></g>; })}
      {/* antenna */}
      <path d={`M 0 -200 Q ${6 * Math.sin(t * 5)} -224 ${10 * Math.sin(t * 5)} -240`} stroke={OL} strokeWidth={5} fill="none" />
      <circle cx={10 * Math.sin(t * 5)} cy={-246} r={10} fill={Math.sin(t * 6 + i) > 0 ? '#FFD54F' : '#E53950'} stroke={OL} strokeWidth={4} />
      <rect x={-34} y={-216} width={68} height={18} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={0} y={-202} s={13}>TAGBOT</T>
    </g>
    {pile}
  </g>;
};

/** BUZZ the delivery drone: one big eye, four rotors, a swinging parcel. x/y keyframes, carry (label), face ('happy'|'squint'|'shock') */
export const drone: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 300), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const vx = (kf(a.x, t + 0.05, 960) - kf(a.x, t - 0.05, 960)) / 0.1, tilt = clamp(vx / 900, -1, 1) * 18;
  const face: string = pick(a.faces, t, a.face || 'happy'), hov = Math.sin(t * 3.1 + i) * 10;
  const swing = -tilt * 1.3 + Math.sin(t * 2.6 + i) * 8, bl = ((t + i * 0.7) % 2.9) < 0.12;
  return <g key={'dr' + i} transform={`translate(${x} ${y + hov}) scale(${s})`}>
    <g transform={`rotate(${swing})`}>
      <path d="M 0 30 L 0 92" stroke={OL} strokeWidth={4} />
      {a.carry !== false && <g transform="translate(0 120)"><rect x={-42} y={-30} width={84} height={60} rx={5} fill="#D7A86E" stroke={OL} strokeWidth={4} /><path d="M -42 -6 L 42 -6 M 0 -30 L 0 -6" stroke="#A9783F" strokeWidth={4} />
        {a.carry && <T x={0} y={20} s={fit(String(a.carry), 76, 16)}>{a.carry}</T>}</g>}
    </g>
    <g transform={`rotate(${tilt})`}>
      {[-1, 1].map((sd) => <g key={sd}>
        <path d={`M ${sd * 40} -6 L ${sd * 96} -30`} stroke={OL} strokeWidth={8} strokeLinecap="round" />
        <ellipse cx={sd * 100} cy={-38} rx={52 * Math.abs(Math.cos(t * 40 + sd))} ry={7} fill="#B0BEC5" stroke={OL} strokeWidth={3} opacity={0.85} />
        <circle cx={sd * 100} cy={-36} r={6} fill={OL} /></g>)}
      <ellipse cx={0} cy={0} rx={54} ry={40} fill="#FFD23F" stroke={OL} strokeWidth={5} />
      <path d="M -54 6 Q 0 26 54 6" fill="none" stroke="#E0A800" strokeWidth={5} />
      <circle cx={6} cy={-4} r={22} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
      {bl ? <path d="M -12 -4 L 24 -4" stroke={OL} strokeWidth={5} strokeLinecap="round" />
        : <g><circle cx={10} cy={-2} r={face === 'shock' ? 5 : 10} fill={OL} /><circle cx={13} cy={-6} r={3} fill="#FFFFFF" /></g>}
      {face === 'squint' && <path d="M -16 -16 L 28 -10" stroke={OL} strokeWidth={6} strokeLinecap="round" />}
      <rect x={-20} y={30} width={40} height={10} rx={4} fill="#37474F" />
    </g>
  </g>;
};

/** LIFT the forklift: headlight eyes, grill mouth, forks at `lift` (0..1 keyframes), carries `load` boxes with labels */
export const forklift: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.45), fl = a.flip ? -1 : 1;
  const vx = (kf(a.x, t + 0.05, 960) - kf(a.x, t - 0.05, 960)) / 0.1, lift = kf(a.lift, t, 0);
  const face: string = pick(a.faces, t, a.face || 'happy'), bounce = Math.abs(Math.sin(t * 9)) * (Math.abs(vx) > 20 ? 5 : 1.5);
  const talking = inWins(a.talk, t), load: string[] = a.load || [];
  const fy = -40 - lift * 220;
  return <g key={'fk' + i} transform={`translate(${x} ${y}) scale(${s * fl} ${s})`}>
    <ellipse cx={0} cy={6} rx={170} ry={14} fill={OL} opacity={0.18} />
    {/* mast + forks + load */}
    <rect x={118} y={-330} width={16} height={310} fill="#546E7A" stroke={OL} strokeWidth={4} />
    <g transform={`translate(0 ${fy})`}>
      <path d="M 132 0 L 132 40 L 260 40" stroke="#37474F" strokeWidth={12} fill="none" strokeLinejoin="round" />
      {load.map((l, k) => <g key={k} transform={`translate(${195} ${16 - k * 62}) rotate(${Math.sin(t * 5 + k) * (Math.abs(vx) > 20 ? 3 : 0.8)})`}>
        <rect x={-60} y={-38} width={120} height={60} rx={4} fill={['#D7A86E', '#C99A5B', '#E2B47C'][k % 3]} stroke={OL} strokeWidth={4} />
        <path d="M -60 -16 L 60 -16" stroke="#A9783F" strokeWidth={3} /><T x={0} y={12} s={fit(l, 110, 18)}>{l}</T></g>)}
    </g>
    {/* body */}
    <g transform={`translate(0 ${-bounce})`}>
      <path d="M -150 -40 L -150 -150 Q -150 -170 -130 -170 L 40 -170 L 110 -110 L 110 -40 Z" fill="#F5B800" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <rect x={-170} y={-120} width={36} height={80} rx={8} fill="#37474F" stroke={OL} strokeWidth={4} />
      <path d="M -110 -170 L -110 -290 L 40 -290 L 70 -170 M -110 -290 L -130 -290" stroke="#37474F" strokeWidth={10} fill="none" strokeLinejoin="round" />
      <rect x={-118} y={-300} width={168} height={18} rx={6} fill="#37474F" stroke={OL} strokeWidth={3} />
      {/* headlight eyes */}
      {[0, 1].map((k) => { const cx = 66 + k * 34, cy = -138, bl = ((t + i) % 3.1) < 0.12;
        return <g key={k}><circle cx={cx} cy={cy} r={16} fill="#FFF8D6" stroke={OL} strokeWidth={4} />
          {bl ? <path d={`M ${cx - 10} ${cy} L ${cx + 10} ${cy}`} stroke={OL} strokeWidth={4} /> : <circle cx={cx + 4} cy={cy + 1} r={face === 'shock' ? 3 : 7} fill={OL} />}
          {face === 'angry' && <path d={`M ${cx - 16} ${cy - 22 + (k ? 6 : 0)} L ${cx + 16} ${cy - 22 + (k ? 0 : 6)}`} stroke={OL} strokeWidth={5} />}</g>; })}
      <rect x={70} y={-98} width={30 + (talking ? 8 * Math.abs(Math.sin(t * 18)) : 0)} height={talking ? 10 + 12 * Math.abs(Math.sin(t * 18)) : 10} rx={4} fill="#37474F" stroke={OL} strokeWidth={3} />
      <rect x={-140} y={-160} width={80} height={24} rx={5} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={-100} y={-142} s={16}>LIFT</T>
      {[0, 1].map((k) => { const u = (t * 1.3 + k * 0.5) % 1; return <circle key={'ex' + k} cx={-175 - u * 40} cy={-130 - u * 60} r={8 + u * 16} fill="#CFD8DC" stroke={OL} strokeWidth={3} opacity={1 - u} />; })}
    </g>
    {[-90, 60].map((wx) => <g key={wx} transform={`translate(${wx} -30) rotate(${(x * 2.2) % 360})`}><circle r={34} fill="#263238" stroke={OL} strokeWidth={5} /><circle r={13} fill="#90A4AE" stroke={OL} strokeWidth={3} /><path d="M -28 0 L 28 0" stroke="#90A4AE" strokeWidth={4} /></g>)}
  </g>;
};

/** heaped shopping cart; `adds` [[t, label]] drop in with a bounce (attach sales) */
export const heapcart: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = (a.scale ?? 1) * pop(t, at, 0.4);
  const adds: [number, string, string?][] = (a.adds || []).map((p: any) => [Number(p[0]), String(p[1]), p[2]]);
  const vx = (kf(a.x, t + 0.05, 960) - kf(a.x, t - 0.05, 960)) / 0.1;
  const cols = ['#4FB3F6', '#FF8A65', '#7BD389', '#B39DDB', '#FFC93C', '#F06292', '#26A69A'];
  return <g key={'hc' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={4} rx={150} ry={12} fill={OL} opacity={0.18} />
    {adds.map(([ta, lab, c], k) => { if (t < ta) return null; const u = E.outBack(win(t, ta, 0.5)), drop = (1 - E.out(win(t, ta, 0.45))) * -260;
      const col2 = Math.floor(k / 3), px = -90 + (k % 3) * 90 + (col2 % 2) * 40, py = -170 - col2 * 62;
      return <g key={k} transform={`translate(${px} ${py + drop}) rotate(${(k % 2 ? 6 : -6) + jig(t, ta + 0.45, 18, 6) * 10}) scale(${u})`}>
        <rect x={-48} y={-30} width={96} height={56} rx={8} fill={c || cols[k % cols.length]} stroke={OL} strokeWidth={4} />
        <T x={0} y={8} s={fit(lab, 86, 19)}>{lab}</T></g>; })}
    <path d="M -150 -170 L 140 -170 L 120 -50 L -120 -50 Z" fill="#CFD8DC" fillOpacity={0.55} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    {[-90, -30, 30, 90].map((gx) => <path key={gx} d={`M ${gx} -170 L ${gx * 0.85} -50`} stroke={OL} strokeWidth={3} opacity={0.6} />)}
    <path d="M -132 -110 L 130 -110" stroke={OL} strokeWidth={3} opacity={0.6} />
    <path d="M 140 -170 L 190 -230 L 220 -230" stroke={OL} strokeWidth={8} fill="none" strokeLinecap="round" />
    <path d="M -120 -50 L -110 -14 L 110 -14" stroke={OL} strokeWidth={6} fill="none" />
    {[-90, 90].map((wx) => <g key={wx} transform={`translate(${wx} -2) rotate(${x * 3})`}><circle r={14} fill="#37474F" stroke={OL} strokeWidth={4} /><path d="M -10 0 L 10 0" stroke="#B0BEC5" strokeWidth={3} /></g>)}
    {Math.abs(vx) > 40 && [0, 1, 2].map((k) => <path key={k} d={`M ${-170 - k * 10} ${-150 + k * 40} L ${-260 - k * 30} ${-150 + k * 40}`} stroke={OL} strokeWidth={5} strokeLinecap="round" opacity={0.4} />)}
  </g>;
};

/** swinging price tag with WAS / NOW and a slash that animates across WAS */
export const bigtag: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), s = (a.scale ?? 1) * pop(t, at, 0.5);
  const sw = 10 * Math.sin(t * 2.2 + i) * Math.exp(-0.15 * (t - at)) + 3 * Math.sin(t * 1.3);
  const slash = a.slashAt !== undefined ? E.out(win(t, a.slashAt, 0.4)) : 0, nowU = a.nowAt !== undefined ? pop(t, a.nowAt, 0.45) : 1;
  return <g key={'bt' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${sw})`}>
    <path d="M 0 -120 L 0 -40" stroke={OL} strokeWidth={4} />
    <path d="M -150 -10 L -110 -50 L 150 -50 L 150 150 L -110 150 L -150 110 Z" fill={a.color || '#FFFDF4'} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <circle cx={-118} cy={50} r={10} fill={OL} />
    <T x={20} y={-4} s={fit(a.was || '', 250, 46)} c="#6B7385">{a.was}</T>
    {slash > 0 && <path d={`M -90 -20 L ${-90 + 230 * slash} ${-20 + 30 * slash}`} stroke="#E53950" strokeWidth={9} strokeLinecap="round" />}
    {nowU > 0 && <g transform={`translate(20 80) scale(${nowU})`}><T x={0} y={18} s={fit(a.now || '', 250, 60)} c="#E53950">{a.now}</T></g>}
    {a.sub && <T x={20} y={136} s={fit(a.sub, 250, 18)} c="#6B7385" w={700}>{a.sub}</T>}
  </g>;
};

/** a flying "$" coin swarm between two points, arcing (fees, revenue) */
export const feeflow: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.5)) return null;
  const [x0, y0] = a.from || [0, 0], [x1, y1] = a.to || [500, 0], n = a.n ?? 6, per = a.per ?? 1.2, lift = a.lift ?? 160;
  const fade = a.until !== undefined ? 1 - win(t, a.until, 0.5) : 1;
  return <g key={'ff' + i} opacity={fade}>{Array.from({length: n}, (_, k) => {
    const u = ((t - at) / per + k / n) % 1; if (t - at < (k / n) * per) return null;
    const px = lerp(x0, x1, u), py = lerp(y0, y1, u) - Math.sin(u * Math.PI) * lift;
    return <g key={k} transform={`translate(${px} ${py}) scale(${Math.abs(Math.cos(t * 6 + k)) * 0.6 + 0.4} 1)`}><circle r={a.r ?? 18} fill={a.color || '#FFC93C'} stroke={OL} strokeWidth={4} />
      <T x={0} y={(a.r ?? 18) * 0.4} s={(a.r ?? 18) * 1.1} c="#7A5200">{a.sym || '$'}</T></g>; })}</g>;
};

/** big title-style word art that bounces in letter by letter (for on-screen punchlines) */
export const toonwords: ItemFn = (a, {t}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, 200), txt: string = a.text || '', size = a.size ?? 80, cw = size * 0.66;
  const out = a.until !== undefined ? 1 - win(t, a.until, 0.3) : 1;
  return <g key={'tw' + i} transform={`translate(${x} ${y}) rotate(${a.rot ?? -3})`} opacity={out}>{txt.split('').map((ch, k) => {
    const st = at + k * 0.035, u = E.outBack(win(t, st, 0.4)), wv = Math.sin(t * 5 + k * 0.6) * 4;
    return <g key={k} transform={`translate(${(k - (txt.length - 1) / 2) * cw} ${wv - (1 - u) * 80}) scale(${u})`}>
      <T x={4} y={6} s={size} c={OL}>{ch}</T><T x={0} y={0} s={size} c={a.color || '#FFC93C'} st={OL} sw={size * 0.12}>{ch}</T></g>; })}</g>;
};

/* ============================================================================================ SETS */
const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
/** retro-futurist skyline: rounded towers with rings, antenna balls, saucer cars drifting (parallax handled by caller offset) */
const skyline = (t: number, x0: number, x1: number, base: number, k0: number, tint = 1) => <g>
  {Array.from({length: Math.ceil((x1 - x0) / 230)}, (_, k) => { const x = x0 + k * 230 + rnd(k + k0) * 60, h = 260 + rnd(k * 3 + k0) * 340, w = 90 + rnd(k * 7 + k0) * 70;
    const c = ['#8EC5E8', '#A9D8C8', '#C5B3E6', '#F3C6A5', '#9FB8E8'][(k + k0) % 5];
    return <g key={'sk' + k} opacity={tint}>
      <path d={`M ${x} ${base} L ${x + w * 0.12} ${base - h} Q ${x + w / 2} ${base - h - 60} ${x + w * 0.88} ${base - h} L ${x + w} ${base} Z`} fill={c} stroke={OL} strokeWidth={4} />
      <ellipse cx={x + w / 2} cy={base - h * 0.62} rx={w * 0.7} ry={14} fill="none" stroke={OL} strokeWidth={4} />
      <path d={`M ${x + w / 2} ${base - h - 30} L ${x + w / 2} ${base - h - 80}`} stroke={OL} strokeWidth={4} />
      <circle cx={x + w / 2} cy={base - h - 86} r={9} fill={Math.sin(t * 3 + k) > 0 ? '#FF5A5F' : '#FFD54F'} stroke={OL} strokeWidth={3} />
      {Array.from({length: Math.floor(h / 70)}, (_, r) => <rect key={r} x={x + w * 0.3} y={base - h + 30 + r * 70} width={w * 0.4} height={18} rx={9} fill="#FFFFFF" opacity={0.5} />)}
    </g>; })}
  {[0, 1, 2].map((q) => { const xx = x0 + ((t * (70 + q * 30) + q * 900) % (x1 - x0)), yy = base - 520 - q * 90 + Math.sin(t * 2 + q) * 14;
    return <g key={'sc' + q} transform={`translate(${xx} ${yy})`}><ellipse rx={56} ry={16} fill={['#FF8A65', '#4FB3F6', '#7BD389'][q]} stroke={OL} strokeWidth={4} />
      <path d="M -26 -10 Q 0 -40 26 -10 Z" fill="#CFEFFF" stroke={OL} strokeWidth={3.5} /><circle cx={-60} cy={0} r={6} fill="#FFD54F" opacity={0.6 + 0.4 * Math.sin(t * 12)} /></g>; })}
</g>;
const car50 = (x: number, y: number, c: string, k: number, t: number, s = 1) => <g key={'c' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <path d="M -95 -20 L -95 -48 Q -80 -60 -50 -62 L -30 -90 Q 0 -100 40 -90 L 60 -62 Q 96 -58 100 -40 L 100 -20 Z" fill={c} stroke={OL} strokeWidth={4.5} strokeLinejoin="round" />
  <path d="M -24 -84 Q 0 -92 36 -84 L 50 -64 L -40 -64 Z" fill="#CFEFFF" stroke={OL} strokeWidth={3} />
  <path d="M 100 -40 L 116 -52 L 112 -30 Z" fill={c} stroke={OL} strokeWidth={3} />
  {[-60, 62].map((wx) => <g key={wx} transform={`translate(${wx} -16)`}><circle r={18} fill="#263238" stroke={OL} strokeWidth={4} /><circle r={7} fill="#CFD8DC" /></g>)}
  <circle cx={96} cy={-42} r={6} fill="#FFF59D" stroke={OL} strokeWidth={2} />
</g>;

export const SITCOM_SETS: Record<string, SetFn> = {
  /** STORE FLOOR interior: shelves of colourful products, swinging sale signs, ceiling lights, a TV wall, a checkout with a register (checkX), a glowing doorbuster pedestal (padX) */
  storefloor: (t, z, f) => {
    const w = z.x1 - z.x0, chk = z.checkX ?? 1500, pad = z.padX, tvw = z.tvX ?? 300;
    const signs: string[] = z.signs || ['SALE!', 'DEALS', 'DOORBUSTERS', 'LIMIT 2', 'HOT!', 'SALE!'];
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#FFF1D6" />
      <rect x={z.x0} y={f - 700} width={w} height={60} fill="#E3D5BC" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 300)}, (_, k) => <g key={'lt' + k}><rect x={z.x0 + k * 300 + 60} y={f - 690} width={180} height={18} rx={9} fill="#FFFDE7" stroke={OL} strokeWidth={3} />
        <ellipse cx={z.x0 + k * 300 + 150} cy={f - 660} rx={130} ry={30} fill="#FFF59D" opacity={0.25 + 0.05 * Math.sin(t * 8 + k)} /></g>)}
      {/* back shelves */}
      {Array.from({length: Math.ceil(w / 420)}, (_, k) => { const sx = z.x0 + k * 420 + 20;
        if (Math.abs(sx + 190 - chk) < 330 || (pad !== undefined && Math.abs(sx + 190 - pad) < 250) || Math.abs(sx + 190 - tvw) < 330) return null;
        return <g key={'sh' + k}><rect x={sx} y={f - 560} width={380} height={560} fill="#90A4AE" stroke={OL} strokeWidth={5} />
          {[0, 1, 2, 3].map((r) => <g key={r}><rect x={sx + 10} y={f - 540 + r * 130 + 100} width={360} height={14} fill="#CFD8DC" stroke={OL} strokeWidth={3} />
            {Array.from({length: 6}, (_, q) => { const h2 = 50 + rnd(k * 31 + r * 7 + q) * 40, c = SHIRT[(k + r * 3 + q) % SHIRT.length];
              return <rect key={q} x={sx + 18 + q * 58} y={f - 540 + r * 130 + 100 - h2} width={46} height={h2} rx={5} fill={c} stroke={OL} strokeWidth={3} />; })}</g>)}</g>; })}
      {/* hanging sale signs */}
      {Array.from({length: Math.ceil(w / 520)}, (_, k) => { const hx = z.x0 + 260 + k * 520, txt = signs[k % signs.length];
        return <g key={'hs' + k} transform={`translate(${hx} ${f - 640}) rotate(${Math.sin(t * 1.8 + k) * 6})`}><path d="M -40 0 L -40 60 M 40 0 L 40 60" stroke={OL} strokeWidth={3} />
          <rect x={-110} y={60} width={220} height={74} rx={12} fill={k % 2 ? '#E53950' : '#FFC93C'} stroke={OL} strokeWidth={5} /><T x={0} y={110} s={fit(txt, 200, 36)} c={k % 2 ? '#FFFFFF' : OL}>{txt}</T></g>; })}
      {/* TV wall */}
      <g transform={`translate(${tvw} ${f - 560})`}>{[0, 1].map((r) => [0, 1, 2].map((c2) => <g key={r + '-' + c2}><rect x={-300 + c2 * 200} y={r * 150} width={180} height={120} rx={8} fill="#263238" stroke={OL} strokeWidth={4} />
        <rect x={-290 + c2 * 200} y={r * 150 + 10} width={160} height={100} rx={4} fill={['#4FC3F7', '#81C784', '#FFB74D', '#BA68C8'][(r * 3 + c2 + Math.floor(t * 1.5)) % 4]} />
        <circle cx={-210 + c2 * 200 + 30 * Math.sin(t * 2 + c2 + r)} cy={r * 150 + 60} r={16} fill="#FFFFFF" opacity={0.6} /></g>))}</g>
      {/* doorbuster pedestal */}
      {pad !== undefined && <g transform={`translate(${pad} ${f})`}>
        <path d={`M -220 -720 L 220 -720 L 300 0 L -300 0 Z`} fill="#FFF59D" opacity={0.28 + 0.06 * Math.sin(t * 5)} />
        <rect x={-130} y={-170} width={260} height={170} fill="#E53950" stroke={OL} strokeWidth={5} /><rect x={-150} y={-190} width={300} height={30} rx={8} fill="#FFC93C" stroke={OL} strokeWidth={4} />
        <T x={0} y={-80} s={30} c="#FFFFFF">DOORBUSTER</T>
        <g transform={`translate(0 ${-190 - 10 * Math.abs(Math.sin(t * 3))})`}><rect x={-140} y={-170} width={280} height={170} rx={10} fill="#263238" stroke={OL} strokeWidth={6} />
          <rect x={-124} y={-154} width={248} height={130} rx={6} fill="#4FC3F7" /><path d="M -100 -130 L -40 -130" stroke="#FFFFFF" strokeWidth={6} opacity={0.6} />
          {Array.from({length: 6}, (_, q) => { const ang = t * 2 + q; return <path key={q} d={`M ${Math.cos(ang) * 170} ${-90 + Math.sin(ang) * 110} l ${Math.cos(ang) * 30} ${Math.sin(ang) * 30}`} stroke="#FFD54F" strokeWidth={6} strokeLinecap="round" />; })}</g></g>}
      {/* checkout */}
      <g transform={`translate(${chk} ${f})`}>
        <rect x={-260} y={-150} width={520} height={150} fill="#ECEFF1" stroke={OL} strokeWidth={5} /><rect x={-260} y={-170} width={520} height={26} rx={6} fill="#546E7A" stroke={OL} strokeWidth={4} />
        <rect x={-240} y={-163} width={300} height={12} fill={OL} strokeDasharray="10 10" opacity={0.4} />
        <g transform="translate(150 -170)"><rect x={-60} y={-90} width={120} height={90} rx={8} fill="#37474F" stroke={OL} strokeWidth={4} /><rect x={-48} y={-80} width={96} height={50} rx={4} fill="#80CBC4" /><T x={0} y={-46} s={22} c="#0E1E36">{Math.floor(t * 3) % 2 ? '$$$' : 'BEEP'}</T></g>
        <path d="M -200 -360 L -200 -170" stroke={OL} strokeWidth={6} /><rect x={-260} y={-420} width={120} height={70} rx={10} fill="#2E9E5B" stroke={OL} strokeWidth={4} /><T x={-200} y={-374} s={30} c="#FFFFFF">OPEN</T>
      </g>
      {/* floor */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#E9DFC9" />
      {Array.from({length: Math.ceil(w / 120)}, (_, k) => <path key={'tl' + k} d={`M ${z.x0 + k * 120} ${f} L ${z.x0 + k * 120 - 80} ${f + 400}`} stroke="#D2C4A8" strokeWidth={4} />)}
      <rect x={z.x0} y={f} width={w} height={18} fill="#CDBE9F" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** retro-futurist MEGA-MALL at 5 a.m.: dawn sky, domed mall with ring + neon sign, sliding doors open at doorsAt, clock 4:59 -> 5:00 at clockAt, monorail, queue rope, parking */
  megamall: (t, z, f) => {
    const w = z.x1 - z.x0, mx = z.x0 + w * (z.mallX ?? 0.5), dawn = clamp(z.dawn ?? 0.6), open = z.doorsAt !== undefined ? E.inOutBack(win(t, z.doorsAt, 0.7)) : 0;
    const shakeD = z.doorsAt !== undefined && t > z.doorsAt - 0.8 && t < z.doorsAt ? Math.sin(t * 70) * 4 : 0;
    const five = z.clockAt !== undefined && t >= z.clockAt;
    return <g>
      {sky(z, f, lerp(0, 1, dawn) > 0.5 ? '#7FA8E8' : '#3D4F8F', '#FFC79A', 'mmsky' + Math.round(z.x0))}
      <circle cx={mx + 700} cy={f - 380 + (1 - dawn) * 120} r={90} fill="#FFD27A" stroke={OL} strokeWidth={5} opacity={0.95} />
      <g transform={`translate(${-0.2 * 0} 0)`}>{skyline(t, z.x0 - 200, z.x1 + 200, f - 180, 3, 0.85)}</g>
      {/* monorail on pylons */}
      <g>{Array.from({length: Math.ceil(w / 600) + 1}, (_, k) => <path key={k} d={`M ${z.x0 + k * 600} ${f - 120} L ${z.x0 + k * 600 + 30} ${f - 470} L ${z.x0 + k * 600 + 60} ${f - 120} Z`} fill="#B0BEC5" stroke={OL} strokeWidth={4} />)}
        <rect x={z.x0} y={f - 486} width={w} height={22} fill="#CFD8DC" stroke={OL} strokeWidth={4} />
        {(() => { const tx = z.x0 - 900 + ((t * 420) % (w + 1800)); return <g transform={`translate(${tx} ${f - 486})`}>
          {[0, 1, 2].map((c) => <g key={c}><rect x={c * 250} y={-80} width={240} height={78} rx={34} fill={c === 0 ? '#E53950' : '#FFFFFF'} stroke={OL} strokeWidth={4} />
            {[0, 1, 2, 3].map((wn) => <rect key={wn} x={c * 250 + 30 + wn * 50} y={-62} width={34} height={26} rx={10} fill="#CFEFFF" stroke={OL} strokeWidth={2.5} />)}</g>)}</g>; })()}</g>
      {/* the mall */}
      <g transform={`translate(${mx + shakeD} ${f}) scale(${z.mallS ?? 1.45})`}>
        <path d="M -560 0 L -560 -300 Q 0 -520 560 -300 L 560 0 Z" fill="#F4F1E6" stroke={OL} strokeWidth={7} />
        <path d="M -380 -360 Q 0 -640 380 -360 Z" fill="#9FE3FF" stroke={OL} strokeWidth={7} />
        {[-240, -120, 0, 120, 240].map((rx) => <path key={rx} d={`M ${rx} -${360 + (1 - Math.abs(rx) / 380) * 130} L ${rx * 1.2} -360`} stroke={OL} strokeWidth={3} opacity={0.5} />)}
        <ellipse cx={0} cy={-370} rx={600} ry={46} fill="none" stroke="#E53950" strokeWidth={14} />
        <ellipse cx={0} cy={-370} rx={600} ry={46} fill="none" stroke={OL} strokeWidth={3} />
        {/* neon sign with chasing bulbs */}
        <g transform="translate(0 -290)"><rect x={-300} y={-60} width={600} height={100} rx={50} fill="#1B2A5A" stroke={OL} strokeWidth={6} />
          {Array.from({length: 22}, (_, k) => { const ang = (k / 22) * Math.PI * 2; return <circle key={k} cx={Math.cos(ang) * 290} cy={-10 + Math.sin(ang) * 44} r={6} fill={(k + Math.floor(t * 10)) % 3 === 0 ? '#FFF59D' : '#FF8A65'} />; })}
          <T x={0} y={8} s={52} c="#FFE066" st="#E53950" sw={4}>{z.sign || 'VALUE-O-RAMA'}</T></g>
        {/* banner */}
        <g transform={`translate(0 -215) rotate(${Math.sin(t * 2) * 1.2})`}><path d="M -330 -34 L 330 -34 L 310 0 L 330 34 L -330 34 L -310 0 Z" fill="#E53950" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
          <T x={0} y={14} s={fit(z.banner || 'DOORBUSTERS · 5 A.M.', 600, 38)} c="#FFFFFF">{z.banner || 'DOORBUSTERS · 5 A.M.'}</T></g>
        {/* sliding doors */}
        <rect x={-200} y={-170} width={400} height={170} fill="#2B3A55" stroke={OL} strokeWidth={6} />
        {open > 0 && <g><rect x={-196} y={-166} width={392} height={166} fill="#FFE9A8" opacity={0.95} />{[-120, 0, 120].map((sx) => <rect key={sx} x={sx - 40} y={-120} width={80} height={120} fill="#FFC93C" stroke={OL} strokeWidth={3} opacity={0.6} />)}</g>}
        {[-1, 1].map((sd) => <g key={sd} transform={`translate(${sd * open * 190} 0)`}><rect x={sd < 0 ? -196 : 0} y={-166} width={196} height={166} fill="#BFE9FF" fillOpacity={0.85} stroke={OL} strokeWidth={5} />
          <path d={`M ${sd * 40} -150 L ${sd * 90} -70`} stroke="#FFFFFF" strokeWidth={6} opacity={0.7} /><rect x={sd < 0 ? -30 : 14} y={-100} width={16} height={40} rx={6} fill="#90A4AE" stroke={OL} strokeWidth={3} /></g>)}
        {[-470, -360, 360, 470].map((wx) => <rect key={wx} x={wx - 45} y={-220} width={90} height={110} rx={10} fill="#BFE9FF" stroke={OL} strokeWidth={4} />)}
        {/* clock tower */}
        <g transform="translate(470 -430)"><rect x={-40} y={-30} width={80} height={180} fill="#F4F1E6" stroke={OL} strokeWidth={5} />
          <rect x={-70} y={-110} width={140} height={84} rx={14} fill="#1B2A5A" stroke={OL} strokeWidth={5} />
          <T x={0} y={-52} s={44} c={five ? '#FF5A5F' : '#5CF2FF'}>{five ? '5:00' : '4:59'}</T>
          {five && <g transform={`scale(${1 + 0.1 * Math.sin(t * 20)})`}>{[0, 1, 2, 3, 4, 5].map((k) => { const ang = k * 1.05; return <path key={k} d={`M ${Math.cos(ang) * 82} ${-68 + Math.sin(ang) * 52} L ${Math.cos(ang) * 104} ${-68 + Math.sin(ang) * 66}`} stroke="#FF5A5F" strokeWidth={6} strokeLinecap="round" />; })}</g>}</g>
      </g>
      {/* ground: plaza + parking */}
      <rect x={z.x0} y={f} width={w} height={700} fill="#B8C2CF" />
      <rect x={z.x0} y={f} width={w} height={24} fill="#DDE3EA" stroke={OL} strokeWidth={4} />
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <path key={'pk' + k} d={`M ${z.x0 + k * 160} ${f + 70} L ${z.x0 + k * 160 + 40} ${f + 170}`} stroke="#FFFFFF" strokeWidth={6} opacity={0.75} />)}
      {[0, 1, 2, 3, 4].map((k) => car50(z.x0 + w * (0.08 + k * 0.2) + (k % 2 ? 60 : 0), f + 150, ['#E57373', '#4FB3F6', '#F2C14E', '#7BD389', '#B39DDB'][k], k, t, 0.9))}
      {/* queue rope */}
      {Array.from({length: 7}, (_, k) => { const px = mx - 900 + k * 110; return <g key={'qr' + k}><rect x={px - 6} y={f - 80} width={12} height={80} fill="#FFC93C" stroke={OL} strokeWidth={3} /><circle cx={px} cy={f - 84} r={10} fill="#FFC93C" stroke={OL} strokeWidth={3} />
        {k < 6 && <path d={`M ${px} ${f - 74} Q ${px + 55} ${f - 40 + 4 * Math.sin(t * 3 + k)} ${px + 110} ${f - 74}`} stroke="#E53950" strokeWidth={7} fill="none" />}</g>; })}
      {/* lamp posts */}
      {[0.12, 0.88].map((p, k) => { const lx = z.x0 + w * p; return <g key={'lp' + k}><path d={`M ${lx} ${f} L ${lx} ${f - 300} Q ${lx} ${f - 340} ${lx + 40} ${f - 340}`} stroke="#546E7A" strokeWidth={10} fill="none" />
        <ellipse cx={lx + 50} cy={f - 336} rx={26} ry={14} fill={dawn < 0.7 ? '#FFF59D' : '#ECEFF1'} stroke={OL} strokeWidth={4} /></g>; })}
    </g>;
  },

  /** PHILADELPHIA 1961: downtown street, department-store facades with awnings, gridlocked rounded cars honking, a traffic cop on a podium */
  philly61: (t, z, f) => {
    const w = z.x1 - z.x0;
    const shops = ['DEPT. STORE', 'HATS', 'RADIO & TV', 'SHOES', 'TOYS', 'DEPT. STORE', 'BAKERY', 'FURS'];
    return <g>
      {sky(z, f, '#9CCBEA', '#E9F3F7', 'phsky' + Math.round(z.x0))}
      {Array.from({length: Math.ceil(w / 360)}, (_, k) => { const x = z.x0 + k * 360, h = 380 + rnd(k + 11) * 220, c = ['#C98B6B', '#D9B48A', '#B07A5A', '#E3C9A0', '#A9776B'][k % 5];
        return <g key={'ps' + k}>
          <rect x={x} y={f - h} width={350} height={h} fill={c} stroke={OL} strokeWidth={5} />
          <rect x={x - 6} y={f - h - 20} width={362} height={24} fill="#8D6E63" stroke={OL} strokeWidth={4} />
          {Array.from({length: Math.floor((h - 200) / 80)}, (_, r) => [0, 1, 2].map((c2) => <rect key={r + '-' + c2} x={x + 40 + c2 * 100} y={f - h + 40 + r * 80} width={60} height={50} fill="#F3E5AB" stroke={OL} strokeWidth={3} />))}
          <path d={`M ${x + 10} ${f - 190} L ${x + 340} ${f - 190} L ${x + 330} ${f - 140} L ${x + 20} ${f - 140} Z`} fill={k % 2 ? '#C0392B' : '#2E7D32'} stroke={OL} strokeWidth={4} />
          {Array.from({length: 8}, (_, q) => <path key={q} d={`M ${x + 20 + q * 40} ${f - 140} l 20 0`} stroke="#FFFFFF" strokeWidth={10} opacity={0.6} />)}
          <rect x={x + 60} y={f - 236} width={230} height={40} rx={4} fill="#FFF8E1" stroke={OL} strokeWidth={3} /><T x={x + 175} y={f - 207} s={24}>{shops[k % shops.length]}</T>
          <rect x={x + 30} y={f - 130} width={290} height={130} fill="#BFE3F5" stroke={OL} strokeWidth={4} />
          {[0, 1, 2].map((q) => <rect key={q} x={x + 50 + q * 90} y={f - 70} width={60} height={70} fill={['#E57373', '#FFD54F', '#81C784'][(q + k) % 3]} stroke={OL} strokeWidth={3} />)}
        </g>; })}
      {/* sidewalk + street */}
      <rect x={z.x0} y={f} width={w} height={40} fill="#D7CCC8" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f + 40} width={w} height={600} fill="#6D6D6D" />
      {Array.from({length: Math.ceil(w / 220)}, (_, k) => <rect key={'ln' + k} x={z.x0 + k * 220} y={f + 175} width={110} height={10} fill="#FFF59D" opacity={0.8} />)}
      {/* gridlock: cars inch forward and honk */}
      {Array.from({length: Math.ceil(w / 130)}, (_, k) => { const lane = k % 2, inch = Math.max(0, Math.sin(t * 0.9 + k)) * 18, x = z.x0 + Math.floor(k / 2) * 260 + lane * 120 + inch, y = f + (lane ? 300 : 160);
        const honk = Math.sin(t * 2.3 + k * 1.7) > 0.85;
        return <g key={'gc' + k}>{car50(x, y + Math.abs(Math.sin(t * 8 + k)) * (honk ? 4 : 1), ['#E57373', '#4FB3F6', '#F2C14E', '#7BD389', '#B39DDB', '#FFAB91'][k % 6], k, t, 1)}
          {honk && <g transform={`translate(${x + 60} ${y - 120}) scale(${0.9 + 0.2 * Math.sin(t * 20)})`}><path d="M -50 -26 L -30 -40 L -8 -26 L 14 -42 L 30 -26 L 56 -32 L 46 -6 L 60 14 L 30 16 L 14 36 L -6 16 L -34 26 L -36 6 L -60 -4 Z" fill="#FFF59D" stroke={OL} strokeWidth={3.5} /><T x={0} y={8} s={22}>HONK!</T></g>}</g>; })}
      {/* traffic cop on a podium */}
      {(() => { const cx = z.x0 + w * (z.copX ?? 0.5), wave = Math.sin(t * 5); return <g transform={`translate(${cx} ${f + 230})`}>
        <path d="M -60 0 L -50 -70 L 50 -70 L 60 0 Z" fill="#ECEFF1" stroke={OL} strokeWidth={5} /><path d="M -55 -30 L 55 -30" stroke="#E53950" strokeWidth={10} />
        <g transform="translate(0 -70)">
          <path d="M -12 -70 L -16 0 M 12 -70 L 16 0" stroke="#1A237E" strokeWidth={16} strokeLinecap="round" />
          <rect x={-32} y={-160} width={64} height={96} rx={20} fill="#283593" stroke={OL} strokeWidth={4} /><circle cx={14} cy={-134} r={7} fill="#FFD54F" stroke={OL} strokeWidth={2} />
          <path d={`M -28 -150 L ${-80} ${-210 + wave * 30}`} stroke="#283593" strokeWidth={15} strokeLinecap="round" /><circle cx={-82} cy={-214 + wave * 30} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
          <path d={`M 28 -150 L ${84} ${-150 - wave * 50}`} stroke="#283593" strokeWidth={15} strokeLinecap="round" /><circle cx={86} cy={-152 - wave * 50} r={12} fill="#FFFFFF" stroke={OL} strokeWidth={3.5} />
          <circle cx={0} cy={-196} r={34} fill="#F6CDA6" stroke={OL} strokeWidth={4} />
          <circle cx={-10} cy={-200} r={4} fill={OL} /><circle cx={12} cy={-200} r={4} fill={OL} />
          <path d="M 4 -178 L 30 -174" stroke="#B0BEC5" strokeWidth={8} strokeLinecap="round" /><circle cx={34} cy={-174} r={7} fill="#B0BEC5" stroke={OL} strokeWidth={2} />
          <path d="M -40 -214 L 40 -214 L 30 -244 Q 0 -256 -30 -244 Z" fill="#1A237E" stroke={OL} strokeWidth={4} /><rect x={-44} y={-218} width={88} height={10} rx={4} fill={OL} />
          {Math.sin(t * 6) > 0.2 && <T x={78} y={-196} s={26} c={OL}>TWEET!</T>}
        </g></g>; })()}
    </g>;
  },

  /** the DOORBUSTER FACTORY: TVs ride a conveyor through a spec-trimming machine (ports pop out) and a stamp press ("SPECIAL EDITION") */
  tvfactory: (t, z, f) => {
    const w = z.x1 - z.x0, mx = z.x0 + w * (z.machX ?? 0.5), speed = z.speed ?? 160, stampT = (t * 0.8) % 1;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f} fill="#E3EDF5" />
      <rect x={z.x0} y={f - 640} width={w} height={20} fill="#B0BEC5" />
      {Array.from({length: Math.ceil(w / 260)}, (_, k) => <g key={'win' + k}><rect x={z.x0 + k * 260 + 40} y={f - 600} width={180} height={140} rx={10} fill="#BFE9FF" stroke={OL} strokeWidth={4} />
        <path d={`M ${z.x0 + k * 260 + 130} ${f - 600} L ${z.x0 + k * 260 + 130} ${f - 460} M ${z.x0 + k * 260 + 40} ${f - 530} L ${z.x0 + k * 260 + 220} ${f - 530}`} stroke={OL} strokeWidth={3} /></g>)}
      {/* pipes with steam */}
      <path d={`M ${z.x0} ${f - 420} L ${z.x1} ${f - 420}`} stroke="#90A4AE" strokeWidth={26} /><path d={`M ${z.x0} ${f - 420} L ${z.x1} ${f - 420}`} stroke={OL} strokeWidth={3} strokeDasharray="2 160" />
      {Array.from({length: Math.ceil(w / 500)}, (_, k) => { const px = z.x0 + 200 + k * 500, u = (t * 0.7 + k * 0.3) % 1;
        return <g key={'pp' + k}><path d={`M ${px} ${f - 420} L ${px} ${f - 300}`} stroke="#90A4AE" strokeWidth={20} />
          <circle cx={px + 10 + u * 40} cy={f - 440 - u * 90} r={16 + u * 30} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={1 - u} />
          <g transform={`translate(${px + 60} ${f - 360})`}><circle r={30} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><path d={`M 0 0 L ${Math.cos(-2 + Math.sin(t * 3 + k) * 0.8) * 22} ${Math.sin(-2 + Math.sin(t * 3 + k) * 0.8) * 22}`} stroke="#E53950" strokeWidth={4} strokeLinecap="round" /></g></g>; })}
      {/* safety sign joke */}
      <g transform={`translate(${z.x0 + w * 0.18} ${f - 520})`}><rect x={-170} y={-50} width={340} height={100} rx={10} fill="#FFD54F" stroke={OL} strokeWidth={5} />
        <T x={0} y={-12} s={22}>DAYS SINCE LAST DISCOUNT</T><T x={0} y={34} s={44} c="#E53950">0</T></g>
      {/* conveyor */}
      <rect x={z.x0} y={f - 140} width={w} height={40} rx={20} fill="#546E7A" stroke={OL} strokeWidth={5} />
      {Array.from({length: Math.ceil(w / 60)}, (_, k) => { const rx = z.x0 + ((k * 60 + t * speed) % w); return <circle key={'rl' + k} cx={rx} cy={f - 120} r={12} fill="#90A4AE" stroke={OL} strokeWidth={2.5} />; })}
      <rect x={z.x0} y={f - 100} width={w} height={100} fill="#78909C" stroke={OL} strokeWidth={4} />
      <rect x={z.x0} y={f} width={w} height={800} fill="#C9D3DC" />
      {Array.from({length: Math.ceil(w / 200)}, (_, k) => <path key={'fl' + k} d={`M ${z.x0 + k * 200} ${f} L ${z.x0 + k * 200 - 120} ${f + 500}`} stroke="#AEB9C4" strokeWidth={4} />)}
      <path d={`M ${z.x0} ${f + 60} L ${z.x1} ${f + 60}`} stroke="#FFD54F" strokeWidth={14} strokeDasharray="60 40" />
      {/* TVs on the belt: regular -> through machine -> "SPECIAL EDITION" */}
      {Array.from({length: Math.ceil(w / 340) + 1}, (_, k) => { const tx = z.x0 - 340 + ((k * 340 + t * speed) % (w + 340)), done = tx > mx + 120;
        return <g key={'tv' + k} transform={`translate(${tx} ${f - 140})`}>
          <rect x={-90} y={-130} width={180} height={120} rx={8} fill="#263238" stroke={OL} strokeWidth={5} />
          <rect x={-78} y={-118} width={156} height={96} rx={4} fill={done ? '#4FC3F7' : '#80DEEA'} />
          <path d="M -60 -100 L -20 -100" stroke="#FFFFFF" strokeWidth={5} opacity={0.6} />
          <path d="M -20 -10 L -30 0 M 20 -10 L 30 0" stroke={OL} strokeWidth={6} />
          {/* ports on the side: 3 before, 1 after */}
          {[0, 1, 2].map((p) => (!done || p === 0) && <rect key={p} x={84} y={-110 + p * 26} width={14} height={16} rx={2} fill="#B0BEC5" stroke={OL} strokeWidth={2} />)}
          {done && <g transform={`rotate(-8) translate(0 -150)`}><rect x={-88} y={-22} width={176} height={36} rx={6} fill="#E53950" stroke={OL} strokeWidth={4} /><T x={0} y={4} s={18} c="#FFFFFF">SPECIAL EDITION</T></g>}
        </g>; })}
      {/* the spec-trimmer machine */}
      <g transform={`translate(${mx} ${f - 140})`}>
        <path d="M -150 -40 L -150 -330 Q -150 -380 -100 -380 L 100 -380 Q 150 -380 150 -330 L 150 -40" fill="#7E57C2" stroke={OL} strokeWidth={6} />
        <rect x={-110} y={-200} width={220} height={160} fill="#311B92" stroke={OL} strokeWidth={5} />
        {/* stamp press */}
        <g transform={`translate(0 ${-330 + (stampT < 0.2 ? E.in(stampT / 0.2) * 120 : 120 * (1 - E.out((stampT - 0.2) / 0.8)))})`}>
          <rect x={-16} y={-60} width={32} height={60} fill="#B0BEC5" stroke={OL} strokeWidth={4} /><rect x={-70} y={0} width={140} height={40} rx={6} fill="#E53950" stroke={OL} strokeWidth={5} /></g>
        <rect x={-130} y={-372} width={260} height={50} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-338} s={26}>{z.label || 'SPEC-O-MATIC'}</T>
        {[0, 1, 2].map((k) => <circle key={k} cx={-80 + k * 80} cy={-250} r={14} fill={(k + Math.floor(t * 4)) % 3 === 0 ? '#FFD54F' : '#4FB3F6'} stroke={OL} strokeWidth={3} />)}
        {/* ports flying out of the machine */}
        {Array.from({length: 4}, (_, k) => { const u = ((t * 0.9 + k * 0.25) % 1), px = 120 + u * 260, py = -260 - Math.sin(u * Math.PI) * 220 + u * 200;
          return <g key={'po' + k} transform={`translate(${px} ${py}) rotate(${u * 540})`} opacity={1 - u * 0.6}><rect x={-12} y={-8} width={24} height={16} rx={2} fill="#B0BEC5" stroke={OL} strokeWidth={2.5} /></g>; })}
        <g transform={`translate(270 -300) rotate(${Math.sin(t * 3) * 4})`}><rect x={-80} y={-22} width={160} height={44} rx={22} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={9} s={22}>− 1 HDMI PORT</T></g>
      </g>
    </g>;
  },

  /** QUARTER HQ: retail HQ tower whose floors are Q1-Q4; Q4 grows huge and bustling at growAt; retro-futurist skyline */
  quarterhq: (t, z, f) => {
    const w = z.x1 - z.x0, tx = z.x0 + w * (z.towerX ?? 0.5), g = z.growAt !== undefined ? E.outBack(win(t, z.growAt, 1.2)) : 1;
    const fl = [{q: 'Q1', h: 150}, {q: 'Q2', h: 150}, {q: 'Q3', h: 150}, {q: 'Q4', h: 150 + 210 * g}];
    let yy = f;
    return <g>
      {sky(z, f, '#5CC8F5', '#E3F6FF', 'qhsky' + Math.round(z.x0))}
      {skyline(t, z.x0 - 200, z.x1 + 200, f, 7, 0.8)}
      <rect x={z.x0} y={f} width={w} height={700} fill="#9CCB7A" />
      <rect x={z.x0} y={f} width={w} height={30} fill="#B9DD9A" stroke={OL} strokeWidth={4} />
      <g transform={`translate(${tx} 0)`}>
        {fl.map((fq, k) => { const top = yy - fq.h, q4 = fq.q === 'Q4'; const el = <g key={fq.q}>
          <rect x={-260 - (q4 ? 40 * g : 0)} y={top} width={520 + (q4 ? 80 * g : 0)} height={fq.h} fill={q4 ? '#FFE082' : ['#E3F2FD', '#E8F5E9', '#F3E5F5'][k]} stroke={OL} strokeWidth={6} />
          <rect x={-300 - (q4 ? 40 * g : 0)} y={top + fq.h / 2 - 30} width={70} height={60} rx={10} fill={q4 ? '#E53950' : '#2F6FD1'} stroke={OL} strokeWidth={4} />
          <T x={-265 - (q4 ? 40 * g : 0)} y={top + fq.h / 2 + 14} s={34} c="#FFFFFF">{fq.q}</T>
          {Array.from({length: q4 ? 6 : 4}, (_, c2) => { const wx = -200 + c2 * (q4 ? 86 : 110); return <g key={c2}>
            <rect x={wx} y={top + 26} width={q4 ? 66 : 80} height={fq.h - 52} rx={8} fill={q4 ? (Math.sin(t * 6 + c2) > 0 ? '#FFF59D' : '#FFCA28') : '#BFE3F5'} stroke={OL} strokeWidth={3} />
            {q4 && <circle cx={wx + 33} cy={top + fq.h - 50 - Math.abs(Math.sin(t * 7 + c2)) * 30} r={14} fill={SKIN[c2 % 5]} stroke={OL} strokeWidth={3} />}</g>; })}
          {q4 && g > 0.5 && <g transform={`translate(${330 + 40 * g} ${top + 40}) rotate(${Math.sin(t * 4) * 6})`}><path d="M -70 -30 L 70 -30 L 60 0 L 70 30 L -70 30 L -60 0 Z" fill="#E53950" stroke={OL} strokeWidth={4} /><T x={0} y={10} s={24} c="#FFFFFF">13 WEEKS</T></g>}
        </g>; yy = top; return el; })}
        <path d={`M -240 ${yy} L 0 ${yy - 90} L 240 ${yy} Z`} fill="#90A4AE" stroke={OL} strokeWidth={6} />
        <path d={`M 0 ${yy - 90} L 0 ${yy - 170}`} stroke={OL} strokeWidth={6} /><circle cx={0} cy={yy - 178} r={14} fill={Math.sin(t * 4) > 0 ? '#FF5A5F' : '#FFD54F'} stroke={OL} strokeWidth={4} />
        {/* coins pour from the Q4 floor */}
        {g > 0.6 && Array.from({length: 8}, (_, k) => { const u = ((t * 0.8 + k / 8) % 1); return <g key={'cn' + k} transform={`translate(${-200 + k * 60 + Math.sin(k) * 20} ${lerp(f - 360, f - 10, E.in(u))}) scale(${Math.abs(Math.cos(t * 6 + k))} 1)`}>
          <circle r={16} fill="#FFC93C" stroke={OL} strokeWidth={3.5} /><T x={0} y={7} s={18} c="#7A5200">$</T></g>; })}
      </g>
    </g>;
  },

  /** PAYMENT-RAILS HIGHWAY: elevated highway, card-shaped trucks, toll gantries ("INTERCHANGE", "NETWORK FEE") with arms that lift and coins that fly off */
  payrails: (t, z, f) => {
    const w = z.x1 - z.x0, deckY = f - 200, gates: string[] = z.gates || ['INTERCHANGE', 'NETWORK FEE'];
    return <g>
      {sky(z, f, '#5CC8F5', '#E3F6FF', 'prsky' + Math.round(z.x0))}
      {skyline(t, z.x0 - 200, z.x1 + 200, deckY + 40, 11, 0.85)}
      {/* bank towers */}
      {[z.bank1X ?? 260, z.bank2X ?? 1680].map((bx0, k) => { const bx = bx0; return <g key={'bk' + k} transform={`translate(${bx} ${deckY - 20})`}>
        <path d="M -120 0 L -120 -340 L 0 -400 L 120 -340 L 120 0 Z" fill={k ? '#C5CAE9' : '#C8E6C9'} stroke={OL} strokeWidth={6} />
        {[-80, -27, 27, 80].map((cx) => <rect key={cx} x={cx - 14} y={-320} width={28} height={300} fill="#FFFFFF" stroke={OL} strokeWidth={3} />)}
        <rect x={-110} y={-380} width={220} height={44} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-350} s={24}>{k ? (z.bank2 || 'CARD NETWORK') : (z.bank1 || 'ISSUING BANK')}</T>
      </g>; })}
      {/* deck + pillars */}
      <rect x={z.x0} y={deckY} width={w} height={60} fill="#90A4AE" stroke={OL} strokeWidth={6} />
      {Array.from({length: Math.ceil(w / 400)}, (_, k) => <rect key={'pl' + k} x={z.x0 + k * 400 + 160} y={deckY + 60} width={60} height={f - deckY + 200} fill="#B0BEC5" stroke={OL} strokeWidth={5} />)}
      {Array.from({length: Math.ceil(w / 160)}, (_, k) => <rect key={'dl' + k} x={z.x0 + ((k * 160 - t * 300) % w + w) % w} y={deckY + 26} width={70} height={8} fill="#FFFFFF" opacity={0.8} />)}
      <rect x={z.x0} y={f - 40} width={w} height={800} fill="#9CCB7A" />
      <rect x={z.x0} y={f - 40} width={w} height={22} fill="#B9DD9A" stroke={OL} strokeWidth={4} />
      {/* card trucks */}
      {Array.from({length: 5}, (_, k) => { const span = w + 800, tx = z.x0 - 400 + ((t * (260 + k * 30) + k * span / 5) % span), cc = ['#2F6FD1', '#E53950', '#2E9E5B', '#7E57C2', '#FFB300'][k];
        return <g key={'ct' + k} transform={`translate(${tx} ${deckY - 6})`}>
          <g transform={`translate(0 ${-Math.abs(Math.sin(t * 9 + k)) * 3})`}>
            <rect x={-150} y={-120} width={210} height={110} rx={14} fill={cc} stroke={OL} strokeWidth={5} />
            <rect x={-130} y={-96} width={40} height={30} rx={5} fill="#FFD54F" stroke={OL} strokeWidth={3} />
            <path d="M -130 -40 L 30 -40" stroke="#FFFFFF" strokeWidth={6} opacity={0.6} strokeDasharray="22 10" />
            <path d="M 60 -10 L 60 -90 L 110 -90 Q 132 -86 136 -50 L 140 -10 Z" fill="#ECEFF1" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
            <circle cx={112} cy={-64} r={10} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><circle cx={115} cy={-63} r={4} fill={OL} />
            <rect x={-60} y={-160} width={60} height={42} rx={5} fill="#D7A86E" stroke={OL} strokeWidth={3.5} /><T x={-30} y={-130} s={24} c="#7A5200">$</T>
          </g>
          {[-110, 10, 110].map((wx) => <g key={wx} transform={`translate(${wx} -6) rotate(${t * 500})`}><circle r={18} fill="#263238" stroke={OL} strokeWidth={4} /><path d="M -12 0 L 12 0" stroke="#90A4AE" strokeWidth={3} /></g>)}
        </g>; })}
      {/* toll gantries */}
      {gates.map((gname, k) => { const gx = (z.gateX ?? 620) + k * (z.gateGap ?? 760), lift = Math.max(0, Math.sin(t * 2.2 + k * 1.3));
        return <g key={'gt' + k} transform={`translate(${gx} ${deckY})`}>
          <path d="M -210 0 L -210 -330 M 210 0 L 210 -330" stroke="#546E7A" strokeWidth={22} />
          <rect x={-240} y={-380} width={480} height={70} rx={12} fill="#2E7D32" stroke={OL} strokeWidth={5} /><T x={0} y={-334} s={fit(gname, 440, 34)} c="#FFFFFF">{gname}</T>
          <rect x={-200} y={-90} width={60} height={90} fill="#FFC93C" stroke={OL} strokeWidth={4} />
          <g transform={`translate(-140 -60) rotate(${-70 * lift})`}><rect x={0} y={-8} width={200} height={16} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} />{[1, 3, 5, 7].map((q) => <rect key={q} x={q * 22} y={-8} width={18} height={16} fill="#E53950" />)}</g>
          {Array.from({length: 3}, (_, q) => { const u = ((t * 1.1 + q / 3 + k * 0.2) % 1), px = -20 + (k ? 1 : -1) * u * 480, py = -200 - Math.sin(u * Math.PI) * 220 + u * 60;
            return <g key={'tc' + q} transform={`translate(${px} ${py}) scale(${Math.abs(Math.cos(t * 7 + q)) * 0.7 + 0.3} 1)`} opacity={1 - u * 0.3}><circle r={16} fill="#FFC93C" stroke={OL} strokeWidth={3.5} /><T x={0} y={6} s={17} c="#7A5200">¢</T></g>; })}
        </g>; })}
    </g>;
  },

  /** BUY-NOW-PAY-LATER CAROUSEL: a fairground carousel whose seats are shopping bags labelled 1/4..4/4 that go round, a ticket booth "PAY IN 4" and a merchant-fee jar */
  bnplride: (t, z, f) => {
    const w = z.x1 - z.x0, cx = z.x0 + w * (z.rideX ?? 0.5), rot = t * (z.spin ?? 0.9), feeU = z.feeAt !== undefined ? clamp((t - z.feeAt) / 6) : 0;
    const seats = [0, 1, 2, 3].map((k) => { const ang = rot + (k * Math.PI) / 2; return {k, ang, x: Math.sin(ang) * 330, depth: Math.cos(ang)}; }).sort((a2, b2) => a2.depth - b2.depth);
    return <g>
      {sky(z, f, '#5CC8F5', '#FFE3EE', 'bnsky' + Math.round(z.x0))}
      {/* ferris wheel */}
      <g transform={`translate(${cx - 980} ${f - 380})`}><g transform={`rotate(${t * 12})`}><circle r={260} fill="none" stroke="#E53950" strokeWidth={10} />{Array.from({length: 10}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos(k * 0.628) * 260} ${Math.sin(k * 0.628) * 260}`} stroke={OL} strokeWidth={4} />)}</g>
        {Array.from({length: 10}, (_, k) => { const a2 = (t * 12 * Math.PI) / 180 + k * 0.628; return <rect key={'gd' + k} x={Math.cos(a2) * 260 - 22} y={Math.sin(a2) * 260 - 4} width={44} height={36} rx={8} fill={SHIRT[k % 9]} stroke={OL} strokeWidth={3} />; })}
        <path d="M -120 380 L 0 0 L 120 380" stroke="#546E7A" strokeWidth={14} fill="none" /></g>
      {/* striped tents */}
      {[cx + 1050, cx + 1330].map((tx, k) => { return <g key={'tn' + k}><path d={`M ${tx - 140} ${f} L ${tx - 140} ${f - 160} L ${tx} ${f - 300} L ${tx + 140} ${f - 160} L ${tx + 140} ${f} Z`} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        {[-100, -40, 20, 80].map((sx) => <path key={sx} d={`M ${tx + sx} ${f} L ${tx + sx} ${f - 175} L ${tx + sx / 4 + 4} ${f - 290} L ${tx + sx / 4 + 16} ${f - 280} L ${tx + sx + 30} ${f - 168} L ${tx + sx + 30} ${f} Z`} fill="#E53950" opacity={0.85} />)}</g>; })}
      <rect x={z.x0} y={f} width={w} height={700} fill="#F3D9A4" />
      <rect x={z.x0} y={f} width={w} height={24} fill="#E8C47A" stroke={OL} strokeWidth={4} />
      {/* carousel */}
      <g transform={`translate(${cx} ${f})`}>
        <ellipse cx={0} cy={-20} rx={430} ry={60} fill="#7E57C2" stroke={OL} strokeWidth={6} />
        <path d="M 0 -520 L 0 -40" stroke="#FFC93C" strokeWidth={30} /><path d="M 0 -520 L 0 -40" stroke={OL} strokeWidth={4} strokeDasharray="10 30" />
        {seats.map((sItem) => { const sx = sItem.x, sc = 0.78 + 0.22 * (sItem.depth + 1) / 2, bobY = Math.sin(rot * 3 + sItem.k * 1.6) * 40;
          return <g key={'st' + sItem.k} opacity={0.6 + 0.4 * (sItem.depth + 1) / 2}>
            <path d={`M ${sx} -470 L ${sx} ${-180 + bobY}`} stroke="#FFD54F" strokeWidth={10} /><path d={`M ${sx} -470 L ${sx} ${-180 + bobY}`} stroke={OL} strokeWidth={3} />
            <g transform={`translate(${sx} ${-150 + bobY}) scale(${sc * 1.3})`}>
              <path d="M -26 -60 Q 0 -96 26 -60" fill="none" stroke={OL} strokeWidth={7} />
              <rect x={-70} y={-62} width={140} height={120} rx={14} fill={['#FFC93C', '#4FB3F6', '#7BD389', '#F06292'][sItem.k]} stroke={OL} strokeWidth={5} />
              <T x={0} y={14} s={40}>{`${sItem.k + 1}/4`}</T></g></g>; })}
        <path d="M -470 -470 Q 0 -640 470 -470 Z" fill="#E53950" stroke={OL} strokeWidth={7} />
        {[-350, -175, 0, 175, 350].map((sx) => <path key={sx} d={`M ${sx * 0.98} -470 Q ${sx * 0.5} -560 0 -600`} stroke="#FFFFFF" strokeWidth={14} fill="none" opacity={0.8} />)}
        {Array.from({length: 13}, (_, k) => <circle key={'bl' + k} cx={-460 + k * 76.6} cy={-468} r={11} fill={(k + Math.floor(t * 8)) % 2 ? '#FFF59D' : '#FFB300'} stroke={OL} strokeWidth={3} />)}
        <rect x={-200} y={-650} width={400} height={64} rx={32} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><T x={0} y={-606} s={38} c="#7E57C2">{z.title || 'PAY-IN-4 GO-ROUND'}</T>
      </g>
      {/* ticket booth + fee jar */}
      <g transform={`translate(${cx + (z.boothDX ?? 640)} ${f})`}>
        <rect x={-110} y={-240} width={220} height={240} fill="#FFF3E0" stroke={OL} strokeWidth={5} />
        <path d="M -130 -240 L 0 -320 L 130 -240 Z" fill="#2E9E5B" stroke={OL} strokeWidth={5} />
        <rect x={-80} y={-200} width={160} height={90} rx={10} fill="#BFE3F5" stroke={OL} strokeWidth={4} />
        <rect x={-100} y={-300} width={200} height={44} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-269} s={26}>{z.booth || 'PAY IN 4'}</T>
        {z.feeAt !== undefined && <g transform="translate(200 0)">
          <path d="M -60 -170 L 60 -170 L 54 0 L -54 0 Z" fill="#E3F2FD" fillOpacity={0.6} stroke={OL} strokeWidth={5} />
          <rect x={-56} y={-150 * feeU} width={112} height={150 * feeU} fill="#FFC93C" stroke={OL} strokeWidth={3} />
          <rect x={-70} y={-196} width={140} height={34} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-172} s={18}>MERCHANT FEE</T></g>}
      </g>
    </g>;
  },

  /** AD ARENA inside a giant phone: a stadium of bidder bots holding paddles, a scoreboard, spotlights, and product cards that win the TOP SLOT */
  adarena: (t, z, f) => {
    const w = z.x1 - z.x0, px = z.x0 + w * (z.phoneX ?? 0.5), slots: string[] = z.slots || ['SPONSORED', 'SPONSORED', 'DEAL'];
    const winAt = z.winAt ?? 999, won = t >= winAt;
    return <g>
      <rect x={z.x0} y={-2500} width={w} height={2500 + f + 600} fill="#2A1B5C" />
      {Array.from({length: 40}, (_, k) => <circle key={'st' + k} cx={z.x0 + rnd(k) * w} cy={f - 900 + rnd(k + 5) * 600} r={2 + rnd(k + 2) * 3} fill="#FFFFFF" opacity={0.4 + 0.4 * Math.sin(t * 3 + k)} />)}
      {/* stands with bidder bots */}
      {[0, 1, 2].map((row) => Array.from({length: Math.ceil(w / 90)}, (_, k) => { const bx = z.x0 + k * 90 + (row % 2) * 45, by = f - 120 - row * 110, up = Math.sin(t * 4 + k * 1.3 + row) > 0.6;
        if (Math.abs(bx - px) < 470) return null;
        return <g key={row + '-' + k} transform={`translate(${bx} ${by})`}><rect x={-30} y={-50} width={60} height={50} rx={10} fill={['#90CAF9', '#CE93D8', '#A5D6A7'][row]} stroke={OL} strokeWidth={3} />
          <rect x={-20} y={-40} width={40} height={18} rx={4} fill="#0E1E36" /><rect x={-14} y={-36} width={8} height={8} fill="#5CF2FF" /><rect x={6} y={-36} width={8} height={8} fill="#5CF2FF" />
          {up && <g><path d="M 26 -40 L 34 -100" stroke={OL} strokeWidth={5} /><rect x={14} y={-136} width={44} height={36} rx={6} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><T x={36} y={-111} s={18} c="#2E9E5B">$</T></g>}</g>; }))}
      {/* spotlights */}
      {[-1, 1].map((sd) => { const ang = Math.sin(t * 1.3 + sd) * 25; return <path key={sd} d={`M ${px + sd * 700} ${f - 900} L ${px + sd * 700 + Math.tan(((ang - 10) * Math.PI) / 180) * 900 - sd * 300} ${f} L ${px + sd * 700 + Math.tan(((ang + 10) * Math.PI) / 180) * 900 - sd * 300} ${f} Z`} fill="#FFF59D" opacity={0.18} />; })}
      {/* giant phone */}
      <g transform={`translate(${px} ${f - 30})`}>
        <rect x={-420} y={-860} width={840} height={860} rx={80} fill="#1B1B1B" stroke={OL} strokeWidth={8} />
        <rect x={-380} y={-800} width={760} height={760} rx={40} fill="#F5F7FA" />
        <rect x={-80} y={-844} width={160} height={24} rx={12} fill="#333" />
        <rect x={-360} y={-780} width={720} height={70} rx={35} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><circle cx={-310} cy={-745} r={18} fill="none" stroke={OL} strokeWidth={5} /><path d="M -297 -732 L -284 -719" stroke={OL} strokeWidth={5} />
        <T x={20} y={-733} s={30} c="#6B7385" w={700}>{z.query || 'black friday tv deals'}</T>
        {slots.map((sl, k) => { const sy = -690 + k * 210, isTop = k === 0, bounce = isTop && won ? jig(t, winAt, 16, 5) * 20 : 0, scroll = (t * 30) % 10;
          return <g key={'sl' + k} transform={`translate(0 ${sy - scroll * 0 + bounce})`}>
            <rect x={-360} y={0} width={720} height={190} rx={22} fill={isTop && won ? '#FFF8E1' : '#FFFFFF'} stroke={isTop && won ? '#FFB300' : OL} strokeWidth={isTop && won ? 8 : 4} />
            <rect x={-340} y={20} width={150} height={150} rx={14} fill={['#4FB3F6', '#F06292', '#7BD389'][k]} stroke={OL} strokeWidth={4} />
            <rect x={-320} y={52} width={110} height={70} rx={6} fill="#263238" />
            <rect x={-170} y={30} width={300} height={22} rx={8} fill="#CFD8DC" /><rect x={-170} y={66} width={220} height={22} rx={8} fill="#CFD8DC" />
            <rect x={-170} y={120} width={sl.length * 15 + 30} height={38} rx={10} fill={sl === 'DEAL' ? '#2E9E5B' : '#FFB300'} stroke={OL} strokeWidth={3} /><T x={-155} y={146} s={22} a="start" c="#FFFFFF">{sl}</T>
          </g>; })}
        {won && <g transform={`translate(380 -690) scale(${pop(t, winAt, 0.5)}) rotate(14)`}><path d="M -90 -40 L 90 -40 L 80 0 L 90 40 L -90 40 L -80 0 Z" fill="#E53950" stroke={OL} strokeWidth={5} /><T x={0} y={11} s={30} c="#FFFFFF">TOP SLOT!</T></g>}
      </g>
      {/* scoreboard */}
      <g transform={`translate(${px - 760} ${f - 700}) rotate(-4)`}><rect x={-300} y={-70} width={600} height={110} rx={16} fill="#0E1E36" stroke={OL} strokeWidth={6} />
        <T x={0} y={8} s={46} c="#FFD54F">{z.board || 'AD AUCTION · LIVE'}</T>
        {Array.from({length: 16}, (_, k) => <circle key={k} cx={-280 + k * 37.3} cy={-56} r={6} fill={(k + Math.floor(t * 9)) % 4 === 0 ? '#FF5A5F' : '#5CF2FF'} />)}</g>
      <rect x={z.x0} y={f} width={w} height={600} fill="#3D2A7A" />
    </g>;
  },

  /** RETURNS MOUNTAIN: a mountain of returned boxes behind the warehouse, a flag on top, a box ski-lift, a sorting chute, trucks arriving */
  returnsmtn: (t, z, f) => {
    const w = z.x1 - z.x0, mx = z.x0 + w * (z.mtnX ?? 0.55), grow = z.growAt !== undefined ? E.out(win(t, z.growAt, 3)) : 1, H = 520 * (0.55 + 0.45 * grow);
    const boxes: React.ReactNode[] = [];
    let k = 0;
    for (let row = 0; row < 12; row++) {
      const yb = f - 30 - row * (H / 12), half = 520 * (1 - row / 12.5);
      for (let bx = -half; bx < half; bx += 64) { k++; const c = ['#D7A86E', '#C99A5B', '#E2B47C', '#BF8F55'][k % 4];
        boxes.push(<g key={'bx' + k} transform={`translate(${mx + bx + (row % 2) * 30} ${yb}) rotate(${(rnd(k) - 0.5) * 18})`}>
          <rect x={-30} y={-24} width={60} height={46} rx={3} fill={c} stroke={OL} strokeWidth={3} /><path d="M -30 -6 L 30 -6" stroke="#A9783F" strokeWidth={3} />
          {rnd(k * 3) > 0.8 && <rect x={-18} y={2} width={36} height={14} fill="#FFFFFF" stroke={OL} strokeWidth={2} />}</g>); }
    }
    return <g>
      {sky(z, f, '#7FC8EE', '#EAF7FF', 'rmsky' + Math.round(z.x0))}
      {/* warehouse */}
      <g transform={`translate(${mx - 1080} ${f})`}><rect x={-260} y={-330} width={520} height={330} fill="#ECEFF1" stroke={OL} strokeWidth={6} />
        <path d="M -280 -330 L 0 -420 L 280 -330 Z" fill="#90A4AE" stroke={OL} strokeWidth={6} />
        <rect x={-180} y={-180} width={160} height={180} fill="#5B6577" stroke={OL} strokeWidth={4} /><rect x={20} y={-180} width={160} height={180} fill="#5B6577" stroke={OL} strokeWidth={4} />
        <rect x={-200} y={-300} width={400} height={60} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={4} /><T x={0} y={-258} s={30} c="#E53950">{z.sign || 'RETURNS · OPEN 24/7'}</T></g>
      {boxes}
      {/* flag on top */}
      <g transform={`translate(${mx + 20} ${f - 30 - H - 20})`}><path d="M 0 0 L 0 -150" stroke={OL} strokeWidth={6} />
        <path d={`M 0 -150 Q 50 ${-140 + 10 * Math.sin(t * 6)} 110 -130 Q 60 ${-110 + 8 * Math.sin(t * 6 + 1)} 0 -96 Z`} fill="#E53950" stroke={OL} strokeWidth={4} /><T x={44} y={-118} s={16} c="#FFFFFF">RETURNS</T></g>
      {/* ski lift carrying boxes up */}
      <path d={`M ${mx - 760} ${f - 40} L ${mx - 40} ${f - 40 - H}`} stroke={OL} strokeWidth={4} />
      {Array.from({length: 5}, (_, q) => { const u = ((t * 0.12 + q / 5) % 1), lx = lerp(mx - 760, mx - 40, u), ly = lerp(f - 40, f - 40 - H, u);
        return <g key={'lf' + q} transform={`translate(${lx} ${ly})`}><path d="M 0 0 L 0 50" stroke={OL} strokeWidth={4} /><rect x={-30} y={50} width={60} height={44} rx={4} fill="#D7A86E" stroke={OL} strokeWidth={3} /></g>; })}
      <rect x={z.x0} y={f} width={w} height={700} fill="#9AA3B5" />
      <rect x={z.x0} y={f} width={w} height={20} fill="#B8C2CF" stroke={OL} strokeWidth={4} />
      {/* return trucks arriving */}
      {[0, 1].map((q) => { const span = w + 1200, tx = z.x1 + 600 - ((t * (180 + q * 40) + q * 1100) % span);
        return <g key={'rt' + q} transform={`translate(${tx} ${f + 150}) scale(-0.85 0.85)`}><rect x={-330} y={-130} width={400} height={120} rx={6} fill="#F7F9FB" stroke={OL} strokeWidth={5} />
          <T x={-130} y={-56} s={40} c="#E53950" >{'←'}</T>
          <path d="M 80 -10 L 80 -110 L 150 -110 Q 180 -108 190 -70 L 196 -10 Z" fill="#E53950" stroke={OL} strokeWidth={5} />
          {[-290, -230, 110, 170].map((wx) => <g key={wx} transform={`translate(${wx} 0) rotate(${t * 300})`}><circle r={22} fill="#263238" stroke={OL} strokeWidth={4} /><path d="M -10 0 L 10 0" stroke="#90A4AE" strokeWidth={3} /></g>)}</g>; })}
    </g>;
  },

  /** the SHOW TITLE CARD (screen-filling; use a static camera): rays, chunky bouncing title, sub-banner, and a typed joke subtitle that changes (subs [[t, text]]) */
  titlecard: (t, z, f) => {
    const cx = 960, cy = 470, title: string = z.title || 'BLACK FRIDAY', sub: string = z.sub || 'HOW IT ACTUALLY MAKES MONEY';
    const subs: [number, string][] = (z.subs || []).map((p: any) => [Number(p[0]), String(p[1])]);
    const cur = subs.filter((p) => t >= p[0]).pop();
    const typed = cur ? cur[1].slice(0, Math.floor((t - cur[0]) * 32)) : '';
    const zoomIn = E.outBack(win(t, 0, 0.8));
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#1E3FA8" />
      <g transform={`translate(${cx} ${cy}) rotate(${t * 14})`}>{Array.from({length: 24}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos((k / 24) * Math.PI * 2) * 2400} ${Math.sin((k / 24) * Math.PI * 2) * 2400} L ${Math.cos(((k + 0.5) / 24) * Math.PI * 2) * 2400} ${Math.sin(((k + 0.5) / 24) * Math.PI * 2) * 2400} Z`} fill={k % 2 ? '#2D56D6' : '#FFB300'} opacity={k % 2 ? 1 : 0.95} />)}</g>
      <circle cx={cx} cy={cy} r={420 * zoomIn} fill="#E53950" stroke={OL} strokeWidth={12} />
      <circle cx={cx} cy={cy} r={380 * zoomIn} fill="none" stroke="#FFFFFF" strokeWidth={8} strokeDasharray="4 22" />
      <g transform={`translate(${cx} ${cy - 250}) scale(${pop(t, 0.3, 0.5)})`}><rect x={-360} y={-36} width={720} height={60} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={6} /><T x={0} y={8} s={26} ls={3}>{z.kicker || 'THE HIDDEN ECONOMICS PRESENTS'}</T></g>
      {title.split(' ').map((word, wi) => <g key={wi} transform={`translate(${cx} ${cy - 70 + wi * 170})`}>{word.split('').map((ch, k) => {
        const st = 0.5 + wi * 0.35 + k * 0.06, u = E.outBack(win(t, st, 0.45)), squash = 1 + 0.25 * jig(t, st + 0.3, 20, 8), cw = 118;
        const x = (k - (word.length - 1) / 2) * cw, wob = Math.sin(t * 4 + k * 0.7 + wi) * 6;
        return <g key={k} transform={`translate(${x} ${wob - (1 - u) * 300}) scale(${u * (2 - squash)} ${u * squash}) rotate(${Math.sin(t * 3 + k) * 3})`}>
          <T x={10} y={14} s={170} c={OL}>{ch}</T><T x={0} y={0} s={170} c={wi ? '#FFFFFF' : '#FFD23F'} st={OL} sw={16}>{ch}</T></g>; })}</g>)}
      <g transform={`translate(${cx} ${cy + 290}) scale(${pop(t, 1.6, 0.45)}) rotate(${-2 + Math.sin(t * 2) * 1.5})`}>
        <path d="M -430 -46 L 430 -46 L 400 0 L 430 46 L -430 46 L -400 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={7} strokeLinejoin="round" /><T x={0} y={16} s={44} c="#1E3FA8">{sub}</T></g>
      {cur && <g transform="translate(960 1000)"><rect x={-760} y={-40} width={1520} height={70} rx={14} fill="#0B1A3A" opacity={0.85} />
        <T x={0} y={8} s={34} c="#FFE066" w={800}>{typed}{Math.floor(t * 3) % 2 ? '▌' : ' '}</T></g>}
    </g>;
  },

  /** ACT BUMPER (screen-filling, static camera): diagonal stripe wipe, spinning shopping-bag badge with the act number, act title, rotating joke caption */
  bumper: (t, z, f) => {
    const act: string = z.act || 'ACT ONE', title: string = z.title || '', cap: string = z.caption || '', col2 = z.color || '#E53950';
    const wipe = E.out(win(t, 0, 0.45)), spin = E.outBack(win(t, 0.2, 0.7));
    return <g>
      <rect x={-2000} y={-2000} width={6000} height={5000} fill="#FFF4DE" />
      <g transform={`translate(${-2600 + 2600 * wipe} 0)`}>{Array.from({length: 26}, (_, k) => <path key={k} d={`M ${k * 160 - 400} -200 L ${k * 160 - 320} -200 L ${k * 160 + 300} 1300 L ${k * 160 + 220} 1300 Z`} fill={k % 2 ? col2 : '#FFC93C'} opacity={0.9} />)}</g>
      <g transform={`translate(${(t * 40) % 160} 0)`} opacity={0.25}>{Array.from({length: 18}, (_, k) => <circle key={k} cx={-200 + k * 160} cy={120 + (k % 2) * 860} r={30} fill="#FFFFFF" />)}</g>
      <g transform={`translate(560 520) rotate(${(1 - spin) * -360}) scale(${spin})`}>
        <path d="M -60 -150 Q 0 -250 60 -150" fill="none" stroke={OL} strokeWidth={14} />
        <rect x={-170} y={-150} width={340} height={320} rx={30} fill="#FFFFFF" stroke={OL} strokeWidth={10} />
        <T x={0} y={-50} s={44} c={col2} ls={3}>ACT</T><T x={0} y={110} s={170} c={OL}>{z.num || '1'}</T></g>
      <g transform={`translate(1240 470) scale(${pop(t, 0.45, 0.45)}) rotate(-3)`}><rect x={-520} y={-100} width={1040} height={150} rx={24} fill="#FFFFFF" stroke={OL} strokeWidth={9} />
        <T x={0} y={22} s={fit(title, 960, 72)} c={OL}>{title}</T><T x={0} y={-62} s={26} c={col2} ls={6}>{act}</T></g>
      {cap && <g transform={`translate(1240 650) scale(${pop(t, 0.9, 0.4)}) rotate(${Math.sin(t * 2.4) * 1.5})`}><rect x={-480} y={-38} width={960} height={64} rx={32} fill="#1B2433" />
        <T x={0} y={8} s={fit(cap, 900, 30)} c="#FFE066" w={800}>{cap}</T></g>}
    </g>;
  },
};

export const SITCOM_ITEMS: Record<string, ItemFn> = {toon, stampede, bubble, tagbot, drone, forklift, heapcart, bigtag, feeflow, toonwords};
export const SITCOM_INDOOR = ['storefloor', 'tvfactory', 'adarena', 'titlecard', 'bumper'];
