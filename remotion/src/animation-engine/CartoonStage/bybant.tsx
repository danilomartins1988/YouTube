import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * BYB ANT kit for CartoonStage ("Anthropic Stock Before You Buy", series Before You Buy, Nov 2026 edition).
 *
 * Original designs only, no logos (the company is shown by its ticker ANT). Items built for this episode:
 *  - checklist: MAYA'S CLIPBOARD (signature). A big clipboard with the buyer's questions. `rows` [{text, at, tick}] (row appears at
 *    `at`, a green check draws at `tick`), `focus` [[t, rowIndex | -1]] highlights the current question with a sliding pencil,
 *    `title`, `stamp` {text, at} slams a rubber stamp across the board.
 *  - classcards: THE SHARE-CLASS FAMILY. Cards fan out: `cards` [{cls, who, money, votes, meter (0..1), color, at}], each with a
 *    VOTES meter that fills after the card lands; `glow` [[t, idx | -1]] lifts one card; `title`.
 *  - floodgates: THE LOCK-UP DAM (signature). A reservoir of locked shares behind a dam with gates: `gates` [{date, amt, size (0..1),
 *    at}] (each gate lifts at `at` and share tokens pour through, flow width by `size`), `title`, `note`, `level` KF 0..1 (water level).
 *  - ipopath: A FIRST-YEAR CHART for a past IPO: `points` [[x 0..1, price]], `lo`/`hi` price axis, `offer` (dashed offer-price line),
 *    `draw` KF 0..1 (how much of the path is drawn), `marks` [{x, text, at, color}] callouts pinned to the path, `title`, `foot`.
 *  - govtower: WHO IS IN CHARGE. A boardroom table seen from the front: `seats` n (board seats), `trust` count of seats picked by the
 *    trust (gold), lit from `trustAt`; a ballot box for Class A holders; a FOUNDER VOTE meter (`founder` KF 0..1, label `founderText`);
 *    `labels` overrides.
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (ITEMS).
 */
const OL = '#1A2238';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; [k: string]: any};
type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

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
const gone = (a: Item, t: number) => a.until !== undefined && t > a.until + 0.4;
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;
const fitS = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, String(txt).length)) / 0.58);

const GOLD = '#E8A317', GOLD2 = '#FFD45C', RED = '#E5483B', GREEN = '#2E9E6B', BLUE = '#2F6FDB', PAPER = '#FFFDF4', WATER = '#3FA7E0';

/** the clipboard with the buyer's questions */
const checklist: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 540), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || gone(a, t)) return null;
  const rows: any[] = a.rows || [], RH = a.rowH ?? 88, W = a.w ?? 820, H = 190 + rows.length * RH;
  const fi: number = pick(a.focus, t, -1), wob = Math.sin(t * 0.9 + i) * 0.8;
  const st = a.stamp, stU = st ? win(t, st.at, 0.35) : 0;
  return <g key={'ck' + i} transform={`translate(${x} ${y}) scale(${s}) rotate(${wob})`}>
    <rect x={-W / 2 + 10} y={-H / 2 + 14} width={W} height={H} rx={26} fill="#000" opacity={0.18} />
    <rect x={-W / 2} y={-H / 2} width={W} height={H} rx={26} fill="#B07A44" stroke={OL} strokeWidth={7} />
    <rect x={-W / 2 + 28} y={-H / 2 + 46} width={W - 56} height={H - 70} rx={10} fill={PAPER} stroke={OL} strokeWidth={4} />
    <rect x={-120} y={-H / 2 - 26} width={240} height={70} rx={14} fill="#B0BEC5" stroke={OL} strokeWidth={6} />
    <circle cx={0} cy={-H / 2 - 4} r={12} fill="#78909C" stroke={OL} strokeWidth={4} />
    {a.title && <T x={0} y={-H / 2 + 112} s={fitS(a.title, W - 120, 44)}>{a.title}</T>}
    <path d={`M ${-W / 2 + 60} ${-H / 2 + 136} L ${W / 2 - 60} ${-H / 2 + 136}`} stroke={RED} strokeWidth={3} opacity={0.6} />
    {rows.map((r, k) => {
      const ry = -H / 2 + 150 + k * RH + RH / 2, ap = pop(t, r.at ?? 0, 0.4);
      if (ap <= 0) return null;
      const tick = r.tick !== undefined ? clamp((t - r.tick) / 0.45) : 0, on = k === fi;
      return <g key={k} transform={`translate(0 ${ry})`} opacity={Math.min(1, ap)}>
        {on && <rect x={-W / 2 + 40} y={-RH / 2 + 6} width={W - 80} height={RH - 12} rx={12} fill={GOLD2} opacity={0.55 + 0.15 * Math.sin(t * 5)} />}
        <rect x={-W / 2 + 60} y={-24} width={48} height={48} rx={8} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        {tick > 0 && <path d="M -10 2 L 2 16 L 30 -20" transform={`translate(${-W / 2 + 80} 0)`} fill="none" stroke={GREEN} strokeWidth={9}
          strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={`${tick} 1`} />}
        <T x={-W / 2 + 132} y={12} s={fitS(r.text, W - 220, 34)} a="start" w={on ? 900 : 700}>{r.text}</T>
      </g>;
    })}
    {fi >= 0 && fi < rows.length && (() => { const py = -H / 2 + 150 + fi * RH + RH / 2, bob = Math.sin(t * 6) * 6;
      return <g transform={`translate(${W / 2 - 40 + bob} ${py - 10}) rotate(-35)`}>
        <rect x={-10} y={-90} width={20} height={110} rx={4} fill={GOLD2} stroke={OL} strokeWidth={4} />
        <path d="M -10 20 L 0 44 L 10 20 Z" fill="#F5D0A9" stroke={OL} strokeWidth={4} /><rect x={-10} y={-104} width={20} height={16} rx={4} fill="#F48FB1" stroke={OL} strokeWidth={4} /></g>; })()}
    {st && stU > 0 && <g transform={`rotate(-12) scale(${1 + 0.6 * (1 - E.outBack(stU))})`} opacity={Math.min(1, stU * 2)}>
      <rect x={-fitS(st.text, 700, 64) * st.text.length * 0.31 - 30} y={-56} width={fitS(st.text, 700, 64) * st.text.length * 0.62 + 60} height={96} rx={14} fill="none" stroke={RED} strokeWidth={9} />
      <T x={0} y={14} s={fitS(st.text, 700, 64)} c={RED}>{st.text}</T></g>}
  </g>;
};

/** the share-class family */
const classcards: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 560), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.4);
  if (s <= 0 || gone(a, t)) return null;
  const cards: any[] = a.cards || [], n = cards.length, CW = a.cw ?? 300, gap = a.gap ?? 34, CH = a.ch ?? 430;
  const gi: number = pick(a.glow, t, -1), tot = n * CW + (n - 1) * gap;
  return <g key={'cc' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {a.title && <T x={0} y={-CH / 2 - 50} s={44} c="#FFFFFF" st={OL} sw={8}>{a.title}</T>}
    {cards.map((c, k) => {
      const at = c.at ?? 0, u = win(t, at, 0.6); if (t < at) return null;
      const cx = -tot / 2 + k * (CW + gap) + CW / 2, fromX = -tot / 2 - 300, px = lerp(fromX, cx, E.outBack(u)), lift = k === gi ? -26 : 0;
      const rot = (1 - E.out(u)) * -20 + Math.sin(t * 1.2 + k) * 0.8, m = clamp(c.meter ?? 0) * E.inOut(win(t, at + 0.6, 0.9));
      const colr = c.color || BLUE;
      return <g key={k} transform={`translate(${px} ${lift}) rotate(${rot})`} opacity={k === gi || gi < 0 ? 1 : 0.55}>
        <rect x={-CW / 2 + 8} y={-CH / 2 + 12} width={CW} height={CH} rx={22} fill="#000" opacity={0.2} />
        <rect x={-CW / 2} y={-CH / 2} width={CW} height={CH} rx={22} fill={PAPER} stroke={OL} strokeWidth={6} />
        <rect x={-CW / 2} y={-CH / 2} width={CW} height={110} rx={22} fill={colr} stroke={OL} strokeWidth={6} />
        <T x={0} y={-CH / 2 + 56} s={28} c="#FFFFFF" st={OL} sw={5}>CLASS</T>
        <T x={0} y={-CH / 2 + 100} s={48} c="#FFFFFF" st={OL} sw={6}>{c.cls}</T>
        {String(c.who || '').split('\n').map((ln: string, q: number) => <T key={q} x={0} y={-CH / 2 + 160 + q * 32} s={fitS(ln, CW - 40, 26)} w={700}>{ln}</T>)}
        <T x={0} y={40} s={22} w={700} c="#5E6B85">MONEY</T>
        <T x={0} y={76} s={fitS(c.money || '', CW - 30, 30)} c={c.money === 'NONE' ? RED : GREEN}>{c.money}</T>
        <T x={0} y={124} s={22} w={700} c="#5E6B85">VOTES</T>
        <rect x={-CW / 2 + 30} y={140} width={CW - 60} height={34} rx={10} fill="#E3E8F2" stroke={OL} strokeWidth={4} />
        {m > 0 && <rect x={-CW / 2 + 32} y={142} width={(CW - 64) * m} height={30} rx={8} fill={GOLD} />}
        <T x={0} y={202} s={fitS(c.votes || '', CW - 30, 24)}>{c.votes}</T>
      </g>;
    })}
  </g>;
};

/** the lock-up dam: a reservoir of locked shares with gates that lift on dates */
const floodgates: ItemFn = (a, {t, f}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 620), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || gone(a, t)) return null;
  const gates: any[] = a.gates || [], n = gates.length, W = a.w ?? 1600, GW = (W - 80) / Math.max(1, n), lvl = kf(a.level, t, 1);
  const top = -260, wall = 0, base = 230;
  void f;
  return <g key={'fg' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {/* reservoir behind the dam */}
    <rect x={-W / 2} y={top + (1 - lvl) * 120} width={W} height={wall - top - (1 - lvl) * 120} fill={WATER} opacity={0.85} stroke={OL} strokeWidth={5} />
    {Array.from({length: 16}, (_, k) => { const tx = -W / 2 + 60 + ((k * 97 + t * 30) % (W - 120)), ty = top + 40 + (1 - lvl) * 120 + (k % 3) * 60 + Math.sin(t * 2 + k) * 6;
      return <g key={'tk' + k} transform={`translate(${tx} ${ty})`}><rect x={-26} y={-16} width={52} height={32} rx={6} fill={GOLD2} stroke={OL} strokeWidth={3} /><path d="M -14 -2 L 14 -2 M -14 7 L 6 7" stroke={OL} strokeWidth={2} opacity={0.4} /></g>; })}
    {a.title && <g><rect x={-Math.max(260, a.title.length * 13 + 40)} y={top - 98} width={Math.max(520, a.title.length * 26 + 80)} height={64} rx={16} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      <T x={0} y={top - 54} s={fitS(a.title, 1000, 36)}>{a.title}</T></g>}
    {/* dam wall with gates */}
    <rect x={-W / 2 - 20} y={wall} width={W + 40} height={base} rx={10} fill="#9AA6B8" stroke={OL} strokeWidth={6} />
    {gates.map((g, k) => {
      const gx = -W / 2 + 40 + k * GW + GW / 2, open = E.inOut(win(t, g.at ?? 1e9, 0.8)), gwid = Math.max(40, GW * 0.34 + GW * 0.5 * (g.size ?? 0.3));
      const flowW = gwid * 0.8 * open;
      return <g key={k}>
        {open > 0.05 && <g>
          <rect x={gx - flowW / 2} y={wall + 40} width={flowW} height={base + 150} fill={WATER} opacity={0.9} />
          {Array.from({length: 5}, (_, q) => { const u = (t * 0.9 + q / 5 + k * 0.13) % 1, px = gx + Math.sin(q * 3 + k) * flowW * 0.25;
            return <g key={q} transform={`translate(${px} ${wall + 60 + u * (base + 120)}) rotate(${q * 30 + t * 40})`} opacity={open}>
              <rect x={-20} y={-13} width={40} height={26} rx={5} fill={GOLD2} stroke={OL} strokeWidth={3} /></g>; })}
        </g>}
        <rect x={gx - gwid / 2 - 8} y={wall + 30 - open * 150} width={gwid + 16} height={150} rx={8} fill={open > 0.5 ? '#C8E6C9' : '#607D8B'} stroke={OL} strokeWidth={5} />
        <path d={`M ${gx} ${wall + 30 - open * 150} L ${gx} ${wall - 40 - open * 150}`} stroke={OL} strokeWidth={6} />
        <g transform={`translate(${gx} ${wall + base + 70})`}>
          <rect x={-GW / 2 + 8} y={-34} width={GW - 16} height={g.amt ? 112 : 64} rx={12} fill={open > 0.5 ? GOLD2 : '#FFFFFF'} stroke={OL} strokeWidth={4} />
          <T x={0} y={8} s={fitS(g.date, GW - 30, 28)}>{g.date}</T>
          {g.amt && <T x={0} y={56} s={fitS(g.amt, GW - 30, 24)} w={700}>{g.amt}</T>}
        </g>
      </g>;
    })}
    {a.note && <T x={0} y={wall + base + 230} s={fitS(a.note, W, 26)} c="#FFFFFF" st={OL} sw={6} w={800}>{a.note}</T>}
  </g>;
};

/** a past IPO's first year, relative to its offer price */
const ipopath: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 560), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || gone(a, t)) return null;
  const W = a.w ?? 1100, H = a.h ?? 520, lo = a.lo ?? 0, hi = a.hi ?? 100, pts: [number, number][] = a.points || [], d = clamp(kf(a.draw, t, 1));
  const px = (u: number) => -W / 2 + u * W, py = (v: number) => H / 2 - ((v - lo) / (hi - lo)) * H;
  let path = '';
  for (let k = 0; k < pts.length; k++) { const [u, v] = pts[k]; if (u > d) { if (k) { const [u0, v0] = pts[k - 1]; const r = (d - u0) / Math.max(1e-6, u - u0); path += ` L ${px(d).toFixed(1)} ${py(lerp(v0, v, r)).toFixed(1)}`; } break; }
    path += `${k ? ' L' : 'M'} ${px(u).toFixed(1)} ${py(v).toFixed(1)}`; }
  const off = a.offer ?? lo, color = a.color || GOLD;
  return <g key={'ip' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-W / 2 - 60} y={-H / 2 - 110} width={W + 120} height={H + 200} rx={26} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
    {a.title && <T x={0} y={-H / 2 - 50} s={fitS(a.title, W, 40)}>{a.title}</T>}
    <path d={`M ${-W / 2} ${H / 2} L ${W / 2} ${H / 2}`} stroke={OL} strokeWidth={4} />
    <path d={`M ${-W / 2} ${py(off)} L ${W / 2} ${py(off)}`} stroke={RED} strokeWidth={4} strokeDasharray="16 12" />
    <g transform={`translate(${W / 2 - 10} ${py(off) - 16})`}><T x={0} y={0} s={26} a="end" c={RED}>{a.offerText || 'OFFER PRICE'}</T></g>
    <path d={path} fill="none" stroke={OL} strokeWidth={14} strokeLinejoin="round" strokeLinecap="round" />
    <path d={path} fill="none" stroke={color} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" />
    {(a.marks || []).map((m: any, k: number) => {
      if (t < (m.at ?? 0) || m.x > d + 0.001) return null;
      let v = pts[0]?.[1] ?? lo; for (let q = 1; q < pts.length; q++) if (pts[q][0] >= m.x) { const r = (m.x - pts[q - 1][0]) / Math.max(1e-6, pts[q][0] - pts[q - 1][0]); v = lerp(pts[q - 1][1], pts[q][1], r); break; }
      const mx = px(m.x), my = py(v), sc = E.outBack(win(t, m.at ?? 0, 0.4)), up = m.below ? 1 : -1, lw = Math.max(160, String(m.text).length * 14 + 30);
      const bx = clamp(mx, -W / 2 + lw / 2, W / 2 - lw / 2);
      return <g key={k}><circle cx={mx} cy={my} r={12 * sc} fill={m.color || color} stroke={OL} strokeWidth={4} />
        <g transform={`translate(${bx} ${my + up * 70}) scale(${sc})`}><rect x={-lw / 2} y={-28} width={lw} height={52} rx={12} fill={m.color || GOLD2} stroke={OL} strokeWidth={4} />
          <T x={0} y={8} s={24}>{m.text}</T></g></g>;
    })}
    {a.foot && <T x={0} y={H / 2 + 60} s={fitS(a.foot, W, 22)} w={700} c="#5E6B85">{a.foot}</T>}
  </g>;
};

/** who is in charge: board seats, the trust's seats, the founder vote meter and the Class A ballot box */
const govtower: ItemFn = (a, {t}, i) => {
  const x = kf(a.x, t, 960), y = kf(a.y, t, 640), s = (a.scale ?? 1) * pop(t, a.at ?? 0, 0.5);
  if (s <= 0 || gone(a, t)) return null;
  const n = a.seats ?? 9, tr = a.trust ?? 5, ta = a.trustAt ?? 1e9, W = 1100, L = a.labels || {};
  const fm = clamp(kf(a.founder, t, 0)), bal = a.ballotAt ?? 1e9;
  return <g key={'gv' + i} transform={`translate(${x} ${y}) scale(${s})`}>
    {/* table */}
    <path d={`M ${-W / 2} 60 L ${W / 2} 60 L ${W / 2 - 60} 140 L ${-W / 2 + 60} 140 Z`} fill="#8D6E63" stroke={OL} strokeWidth={6} />
    {Array.from({length: n}, (_, k) => { const cx = -W / 2 + 90 + k * ((W - 180) / Math.max(1, n - 1)), lit = k < tr && t >= ta + k * 0.18;
      const sc = lit ? 1 + 0.08 * Math.sin(t * 4 + k) : 1;
      return <g key={k} transform={`translate(${cx} 0) scale(${sc})`}>
        <rect x={-40} y={-150} width={80} height={170} rx={20} fill={lit ? GOLD : '#90A4AE'} stroke={OL} strokeWidth={5} />
        <circle cx={0} cy={-80} r={26} fill={lit ? GOLD2 : '#CFD8DC'} stroke={OL} strokeWidth={4} />
        <rect x={-30} y={-46} width={60} height={56} rx={14} fill={lit ? GOLD2 : '#CFD8DC'} stroke={OL} strokeWidth={4} />
      </g>; })}
    {t >= ta && <g transform={`translate(0 ${-230}) scale(${E.outBack(win(t, ta, 0.4))})`}>{(() => { const tx = L.trust || 'MAJORITY PICKED BY THE TRUST (CLASS T)', tw = Math.max(640, tx.length * 17 + 60);
        return <g><rect x={-tw / 2} y={-34} width={tw} height={60} rx={14} fill={GOLD2} stroke={OL} strokeWidth={5} /><T x={0} y={8} s={28}>{tx}</T></g>; })()}</g>}
    {/* founder vote meter */}
    {a.founder !== undefined && kf(a.founder, t, 0) > 0.001 && <g transform="translate(-700 -60)">
      <rect x={-90} y={-220} width={180} height={300} rx={18} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
      <rect x={-60} y={-190 + 240 * (1 - fm)} width={120} height={240 * fm} rx={10} fill={BLUE} />
      <path d="M -70 -70 L 70 -70" stroke={RED} strokeWidth={4} strokeDasharray="10 8" />
      <T x={0} y={120} s={24}>{L.founder || 'FOUNDER VOTE'}</T>
      {a.founderText && <T x={0} y={154} s={22} w={700}>{a.founderText}</T>}</g>}
    {/* class A ballot box */}
    {t >= bal && <g transform={`translate(${a.bx ?? 720} -40) scale(${E.outBack(win(t, bal, 0.4))})`}>
      <rect x={-90} y={-80} width={180} height={150} rx={12} fill="#ECEFF1" stroke={OL} strokeWidth={5} />
      <rect x={-50} y={-86} width={100} height={14} rx={6} fill={OL} />
      {Array.from({length: 3}, (_, q) => { const u = (t * 0.7 + q / 3) % 1; return <g key={q} transform={`translate(${-20 + q * 20} ${-200 + u * 120}) rotate(${q * 12 - 12})`} opacity={1 - u}>
        <rect x={-24} y={-16} width={48} height={32} rx={4} fill="#FFFFFF" stroke={OL} strokeWidth={3} /><path d="M -10 0 L -2 8 L 12 -8" fill="none" stroke={GREEN} strokeWidth={4} /></g>; })}
      <T x={0} y={110} s={24}>{L.ballot || 'CLASS A: 1 VOTE EACH'}</T></g>}
  </g>;
};

export const BYBANT_ITEMS: Record<string, ItemFn> = {checklist, classcards, floodgates, ipopath, govtower};
