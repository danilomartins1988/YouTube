import React from 'react';
import {Token} from '../AnimatedWorldMap/AnimatedWorldMap';
import {E, FONT, clamp, col, lerp, pal, quadPt, quadTan, win} from '../motion';
import type {Themed, Vec} from '../types';

/**
 * EconomicFlow: objects travelling through an economic system and being TRANSFORMED by each stage.
 *
 * Stages are cards with a procedural icon that animates while it works (design screen types, fab gear turns
 * and a light beam scans, packaging press stamps, data-centre LEDs light up, bank vault turns). An item
 * enters a stage, is processed (progress bar + icon motion + glow), and leaves as the stage's OUTPUT form
 * (design file -> wafer -> chip -> server). Money can flow back the other way (payments, royalties).
 * Extra inputs (e.g. memory joining at packaging) can merge into a stage.
 */
export type FormShape = 'blueprint' | 'wafer' | 'chip' | 'server' | 'coin' | 'box' | 'packet' | 'dot';
export type StageKind = 'design' | 'fab' | 'package' | 'datacenter' | 'company' | 'bank' | 'customer' | 'warehouse';
export type FlowStage = {id: string; label: string; sub?: string; x: number; y: number; kind: StageKind; color?: string; appear?: number;
  /** form an item has when it LEAVES this stage */
  output: FormShape};
export type FlowLink = {from: string; to: string; lift?: number; appear?: number};
export type FlowItems = {starts: number[]; route: string[]; travel?: number; process?: number};
export type FlowMoney = {from: string; to: string; starts: number[]; travel?: number; label?: string; lift?: number};
export type FlowInput = {stage: string; at: number; from: Vec; shape: FormShape; label?: string; travel?: number};

export type EconomicFlowProps = Themed & {
  t: number;
  stages: FlowStage[];
  links: FlowLink[];
  items?: FlowItems;
  money?: FlowMoney[];
  inputs?: FlowInput[];
  cardW?: number; cardH?: number;
  /** 0..1 global opacity (for morph transitions) and per-stage position overrides (to fly stages elsewhere) */
  opacity?: number;
  positions?: Record<string, Vec>;
  scale?: number;
};

export const Form: React.FC<{shape: FormShape; x: number; y: number; ang?: number; s?: number; c: string}> = ({shape, x, y, ang = 0, s = 1, c}) => {
  if (shape === 'blueprint') return (
    <g transform={`translate(${x} ${y}) rotate(${(ang * 180) / Math.PI * 0.2}) scale(${s})`}>
      <rect x={-22} y={-28} width={44} height={56} rx={4} fill="#1E4E86" stroke={c} strokeWidth={2.5} />
      {[-14, -4, 6, 16].map((q) => <line key={q} x1={-14} x2={14} y1={q} y2={q} stroke="#9CC9F5" strokeWidth={2} opacity={0.8} />)}
      <rect x={-12} y={-20} width={12} height={10} fill="none" stroke="#9CC9F5" strokeWidth={2} />
    </g>);
  if (shape === 'wafer') return (
    <g transform={`translate(${x} ${y}) rotate(${(ang * 180) / Math.PI}) scale(${s})`}>
      <circle r={26} fill="#2A3350" stroke={c} strokeWidth={3} />
      {[-12, 0, 12].map((q) => <g key={q}><line x1={q} x2={q} y1={-22} y2={22} stroke={c} strokeOpacity={0.6} strokeWidth={1.5} /><line y1={q} y2={q} x1={-22} x2={22} stroke={c} strokeOpacity={0.6} strokeWidth={1.5} /></g>)}
      <circle r={26} fill="url(#eng-sheen)" />
    </g>);
  if (shape === 'server') return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <rect x={-22} y={-30} width={44} height={60} rx={4} fill="#121B2B" stroke={c} strokeWidth={2.5} />
      {[-18, -4, 10].map((q, i) => <g key={q}><rect x={-16} y={q} width={32} height={9} rx={2} fill="#1F2B40" /><circle cx={11} cy={q + 4.5} r={2.6} fill={i === 1 ? '#7FC8B8' : c} /></g>)}
    </g>);
  return <Token shape={shape as any} x={x} y={y} ang={ang} c={c} s={s * 1.4} />;
};

/** Procedural stage icon; `work` 0..1 = processing activity, `tt` = time for cyclic motion. */
const StageIcon: React.FC<{kind: StageKind; c: string; work: number; tt: number; P: ReturnType<typeof pal>}> = ({kind, c, work, tt, P}) => {
  const spin = tt * 140 * (0.25 + work);
  if (kind === 'design') return (
    <g>
      <rect x={-46} y={-36} width={92} height={60} rx={6} fill="#0B1424" stroke={c} strokeWidth={3} />
      <rect x={-12} y={26} width={24} height={8} fill={c} />
      {[0, 1, 2, 3].map((i) => <rect key={i} x={-36} y={-26 + i * 12} width={clamp(work * 4 - i) * (40 + (i % 2) * 22)} height={5} rx={2} fill={c} opacity={0.8} />)}
    </g>);
  if (kind === 'fab') return (
    <g>
      <path d="M -50 30 L -50 -6 L -26 -20 L -26 -6 L -2 -20 L -2 -6 L 22 -20 L 22 30 Z" fill="#0B1424" stroke={c} strokeWidth={3} />
      <rect x={30} y={-40} width={14} height={70} fill="#0B1424" stroke={c} strokeWidth={3} />
      <g transform={`translate(-14 12) rotate(${spin})`}>
        {Array.from({length: 8}, (_, i) => <rect key={i} x={-3} y={-15} width={6} height={8} fill={c} transform={`rotate(${i * 45})`} />)}
        <circle r={9} fill="#0B1424" stroke={c} strokeWidth={3} />
      </g>
      {work > 0 && <rect x={-48} y={-4 + ((tt * 60) % 32)} width={68} height={3} fill={P.teal} opacity={0.8 * work} />}
      {work > 0 && [0, 1, 2].map((i) => { const q = ((tt * 0.8 + i / 3) % 1); return <circle key={i} cx={37} cy={-44 - q * 30} r={4 + q * 6} fill={P.muted} opacity={0.4 * (1 - q) * work} />; })}
    </g>);
  if (kind === 'package') {
    const press = work > 0 ? Math.abs(Math.sin(tt * 7)) : 0;
    return (
      <g>
        <rect x={-46} y={18} width={92} height={14} fill="#0B1424" stroke={c} strokeWidth={3} />
        <rect x={-8} y={-44} width={16} height={24 + press * 22} fill={c} />
        <rect x={-30} y={-22 + press * 22} width={60} height={14} rx={3} fill="#0B1424" stroke={c} strokeWidth={3} />
        <rect x={-14} y={4} width={28} height={14} fill={P.blue} opacity={0.8} />
      </g>);
  }
  if (kind === 'datacenter') return (
    <g>
      {[-34, 0, 34].map((dx, r) => (
        <g key={dx}>
          <rect x={dx - 15} y={-40} width={30} height={72} rx={3} fill="#0B1424" stroke={c} strokeWidth={2.5} />
          {[0, 1, 2, 3, 4].map((i) => { const on = work > 0 && Math.sin(tt * 9 + i * 1.7 + r * 2.3) > 0.1; return <circle key={i} cx={dx + 8} cy={-30 + i * 14} r={3} fill={on ? P.teal : P.border} />; })}
        </g>))}
    </g>);
  if (kind === 'bank') return (
    <g>
      <path d="M -48 -14 L 0 -42 L 48 -14 Z" fill="#0B1424" stroke={c} strokeWidth={3} />
      {[-32, -11, 11, 32].map((q) => <rect key={q} x={q - 5} y={-10} width={10} height={36} fill={c} opacity={0.85} />)}
      <rect x={-50} y={28} width={100} height={8} fill={c} />
    </g>);
  if (kind === 'customer') return (
    <g><circle cy={-22} r={16} fill={c} /><path d="M -32 32 Q -30 -2 0 -2 Q 30 -2 32 32 Z" fill={c} /></g>);
  if (kind === 'warehouse') return (
    <g><path d="M -48 32 L -48 -8 L 0 -36 L 48 -8 L 48 32 Z" fill="#0B1424" stroke={c} strokeWidth={3} />
      {[0, 1, 2].map((i) => <rect key={i} x={-34 + i * 24} y={8 - (work > 0 ? ((tt * 2 + i) % 1) * 6 : 0)} width={20} height={20} fill={c} opacity={0.8} />)}</g>);
  return (
    <g><rect x={-40} y={-34} width={80} height={66} rx={8} fill="#0B1424" stroke={c} strokeWidth={3} />
      {[0, 1, 2].map((i) => <rect key={i} x={-28 + i * 20} y={-20} width={12} height={12} fill={c} opacity={0.6 + 0.4 * work} />)}</g>);
};

/** Timing of one item: for each stage on its route, [arrive, leave]. */
const itemSchedule = (start: number, route: string[], travel: number, process: number) => {
  const out: {stage: string; arrive: number; leave: number}[] = [];
  let t0 = start;
  route.forEach((s, i) => {
    const arrive = i === 0 ? t0 : t0 + travel;
    out.push({stage: s, arrive, leave: arrive + process});
    t0 = arrive + process;
  });
  return out;
};

export const EconomicFlow: React.FC<EconomicFlowProps> = (props) => {
  const {t, stages, links, items, money = [], inputs = [], cardW = 230, cardH = 190, opacity = 1, scale = 1} = props;
  const P = pal(props.palette);
  const byId = Object.fromEntries(stages.map((s) => [s.id, s]));
  const pos = (id: string): Vec => props.positions?.[id] || [byId[id].x, byId[id].y];
  const curve = (a: Vec, b: Vec, lift = -0.18): Vec => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + Math.hypot(b[0] - a[0], b[1] - a[1]) * lift];
  const travel = items?.travel ?? 0.7, process = items?.process ?? 0.6;
  const schedules = items ? items.starts.map((s) => itemSchedule(s, items.route, travel, process)) : [];
  // processing activity per stage (0..1) at time t
  const work = (id: string) => {
    let w = 0;
    for (const sch of schedules) for (const st of sch) if (st.stage === id) w = Math.max(w, Math.min(win(t, st.arrive, 0.15), 1 - win(t, st.leave - 0.1, 0.2)));
    for (const m of inputs) if (m.stage === id) w = Math.max(w, Math.sin(Math.PI * win(t, m.at + (m.travel ?? 0.8), 0.4)));
    return w;
  };
  const progress = (id: string) => {
    for (const sch of schedules) for (const st of sch) if (st.stage === id && t >= st.arrive && t <= st.leave) return win(t, st.arrive, st.leave - st.arrive);
    return 0;
  };
  return (
    <g opacity={opacity} transform={scale !== 1 ? `translate(960 540) scale(${scale}) translate(-960 -540)` : undefined}>
      <defs>
        <radialGradient id="eng-sheen" cx="35%" cy="30%" r="70%"><stop offset="0%" stopColor="#fff" stopOpacity={0.35} /><stop offset="60%" stopColor="#fff" stopOpacity={0} /></radialGradient>
      </defs>
      {/* links: draw in, then carry a slow flowing dash */}
      {links.map((l, i) => {
        const a = pos(l.from), b = pos(l.to), c = curve(a, b, l.lift ?? -0.12);
        const u = E.inOut(win(t, l.appear ?? 0, 0.6));
        if (u <= 0) return null;
        const n = 40; let d = '';
        for (let j = 0; j <= n; j++) { const q = quadPt(a, c, b, (j / n) * u); d += (j ? ' L ' : 'M ') + q[0].toFixed(1) + ' ' + q[1].toFixed(1); }
        return <g key={i}>
          <path d={d} fill="none" stroke={P.border} strokeWidth={5} strokeLinecap="round" />
          <path d={d} fill="none" stroke={P.gold} strokeOpacity={0.5} strokeWidth={2.5} strokeDasharray="6 14" strokeDashoffset={-t * 40} />
        </g>;
      })}
      {/* money flowing back (payments) */}
      {money.map((m, i) => {
        const a = pos(m.from), b = pos(m.to), c = curve(a, b, m.lift ?? 0.22);
        return <g key={'m' + i}>{m.starts.map((s, j) => {
          const u = win(t, s, m.travel ?? 1.0);
          if (u <= 0 || u >= 1) return null;
          const q = quadPt(a, c, b, E.inOut(u));
          return <g key={j} opacity={Math.min(1, u * 6, (1 - u) * 6)}><Form shape="coin" x={q[0]} y={q[1]} c={P.gold} s={0.8} /></g>;
        })}
        {m.label && <text x={c[0]} y={c[1] + 34} textAnchor="middle" fill={P.gold} fontFamily={FONT.body} fontWeight={700} fontSize={22} letterSpacing={2}
          opacity={E.out(win(t, m.starts[0], 0.5))}>{m.label}</text>}</g>;
      })}
      {/* stages */}
      {stages.map((s) => {
        const [x, y] = pos(s.id);
        const u = E.outBack(win(t, s.appear ?? 0, 0.6));
        if (u <= 0) return null;
        const c = col(P, s.color);
        const w = work(s.id), pr = progress(s.id);
        const kk = cardW / 230;
        return (
          <g key={s.id} transform={`translate(${x} ${y}) scale(${u * (1 + 0.04 * w)})`}>
            <rect x={-cardW / 2 - 10} y={-cardH / 2 - 10} width={cardW + 20} height={cardH + 20} rx={26} fill={c} opacity={0.18 * w} />
            <rect x={-cardW / 2} y={-cardH / 2} width={cardW} height={cardH} rx={20} fill={P.panel} stroke={w > 0.05 ? c : P.border} strokeWidth={w > 0.05 ? 4 : 2.5} />
            <g transform={`translate(0 ${-22 * kk}) scale(${kk})`}><StageIcon kind={s.kind} c={c} work={w} tt={t} P={P} /></g>
            <text y={cardH / 2 - 44 * kk} textAnchor="middle" fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={26 * kk}>{s.label}</text>
            {s.sub && <text y={cardH / 2 - 18 * kk} textAnchor="middle" fill={P.muted} fontFamily={FONT.body} fontSize={19 * kk}>{s.sub}</text>}
            {pr > 0 && <rect x={-cardW / 2 + 16} y={cardH / 2 - 8} width={(cardW - 32) * pr} height={5} rx={2} fill={c} />}
          </g>
        );
      })}
      {/* extra inputs merging into a stage */}
      {inputs.map((m, i) => {
        const tr = m.travel ?? 0.8, u = win(t, m.at, tr);
        if (u <= 0 || u >= 1) return null;
        const b = pos(m.stage), q: Vec = [lerp(m.from[0], b[0], E.inOut(u)), lerp(m.from[1], b[1], E.inOut(u))];
        return <g key={'in' + i}>
          <Form shape={m.shape} x={q[0]} y={q[1]} c={P.teal} s={0.9 * (1 - 0.4 * E.in(u))} />
          {m.label && <text x={q[0] + 34} y={q[1] + 7} fill={P.teal} fontFamily={FONT.body} fontWeight={700} fontSize={20}>{m.label}</text>}
        </g>;
      })}
      {/* items: travel between stages (with trail + squash), then shrink into the stage and re-emerge transformed */}
      {items && schedules.map((sch, k) => sch.map((st, i) => {
        const out: React.ReactNode[] = [];
        const S = byId[st.stage];
        const here = pos(st.stage);
        // emerging from this stage (pop) and waiting at its right edge
        if (i === sch.length - 1) {
          const u = win(t, st.leave, 0.5);
          if (u > 0 && t < st.leave + 1.4) out.push(<g key={'e' + k + i} opacity={1 - win(t, st.leave + 1.0, 0.4)}>
            <Form shape={S.output} x={here[0]} y={here[1] - cardH / 2 - 40 * E.outBack(u)} s={E.outBack(u) * (cardW / 230)} c={col(P, S.color)} /></g>);
          return out;
        }
        const next = sch[i + 1], b = pos(next.stage), a = here, c = curve(a, b, -0.22);
        const u = win(t, st.leave, travel);
        if (u > 0 && u < 1) {
          for (let g = 3; g >= 0; g--) {                       // trail of fading ghosts
            const ug = clamp(E.inOut(u) - g * 0.035);
            const q = quadPt(a, c, b, ug), ang = quadTan(a, c, b, ug);
            const sp = Math.sin(Math.PI * u);                  // squash & stretch with speed
            out.push(<g key={'t' + k + i + g} opacity={g ? 0.18 * (4 - g) / 3 : 1}
              transform={`translate(${q[0]} ${q[1]}) rotate(${(ang * 180) / Math.PI}) scale(${1 + 0.25 * sp} ${1 - 0.15 * sp}) rotate(${(-ang * 180) / Math.PI}) translate(${-q[0]} ${-q[1]})`}>
              <Form shape={S.output} x={q[0]} y={q[1]} ang={ang} c={col(P, S.color)} s={lerp(0.7, 1, Math.sin(Math.PI * clamp(u * 1.2))) * (cardW / 230)} /></g>);
          }
        }
        return out;
      }))}
    </g>
  );
};
