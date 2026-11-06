import React from 'react';
import {DrawOnCanvas, buildDrawTimeline, shapes} from '../DrawOnCanvas/DrawOnCanvas';
import {E, FONT, clamp, col, fmt, lerp, pal, win} from '../motion';
import type {Themed, Vec} from '../types';

/**
 * AnimatedCharts: data-driven charts that BUILD, CHANGE and TRANSFORM. Values are only ever taken from the
 * `data` you pass in (the component never invents numbers); pass `note` to label illustrative data.
 *
 *   <BarChart>   bars grow in sequence (staggered spring), counters run, optional value change to a second
 *                period (`dataB` at `changeAt`), automatic highlight of the largest period-on-period growth,
 *                and `morph` into a business diagram (bars fly and reshape into labelled boxes joined by arrows)
 *   <LineChart>  the line is drawn progressively (real path length), points pop, area fills, a value marker rides
 *   <Donut>      arcs sweep in segment by segment and can re-balance to new shares
 */
export type Datum = {label: string; value: number; display?: string; name?: string};
export type Box = {x: number; y: number; w: number; h: number};

export type BarChartProps = Themed & {
  t: number;
  data: Datum[];
  box: Box;
  start?: number; stagger?: number; grow?: number;
  title?: string; note?: string;
  valuePrefix?: string; valueSuffix?: string; decimals?: number;
  color?: string; highlightColor?: string;
  /** 'growth' = highlight the bar with the largest increase over the previous one; or an index; or null */
  highlight?: 'growth' | number | null;
  highlightAt?: number;
  /** compare periods: animate every bar to dataB values */
  dataB?: Datum[]; changeAt?: number; changeDur?: number; periodLabels?: [string, string];
  /** morph into a diagram: bar i becomes boxes[i] */
  morph?: {at: number; dur?: number; boxes: (Box & {label: string; sub?: string})[]; arrows?: [number, number][]};
  opacity?: number;
};

const niceMax = (v: number) => { const p = 10 ** Math.floor(Math.log10(v || 1)); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10) * p; };

export const BarChart: React.FC<BarChartProps> = (p) => {
  const P = pal(p.palette);
  const {t, data, box, start = 0, stagger = 0.18, grow = 0.8, decimals = 0, opacity = 1} = p;
  const pre = p.valuePrefix ?? '', suf = p.valueSuffix ?? '';
  const changeU = p.dataB ? E.inOut(win(t, p.changeAt ?? 1e9, p.changeDur ?? 1.0)) : 0;
  const vals = data.map((d, i) => lerp(d.value, p.dataB?.[i]?.value ?? d.value, changeU));
  const vmax = niceMax(Math.max(...data.map((d) => d.value), ...(p.dataB || []).map((d) => d.value)));
  const n = data.length, gap = box.w / n, bw = gap * 0.58;
  let hi = -1;
  if (p.highlight === 'growth') { let best = -Infinity; vals.forEach((v, i) => { if (i && v - vals[i - 1] > best) { best = v - vals[i - 1]; hi = i; } }); }
  else if (typeof p.highlight === 'number') hi = p.highlight;
  const hiU = hi >= 0 ? E.out(win(t, p.highlightAt ?? start + n * stagger + grow + 0.3, 0.5)) : 0;
  const mU = p.morph ? E.inOutQuint(win(t, p.morph.at, p.morph.dur ?? 1.2)) : 0;
  const axisU = E.out(win(t, start - 0.4, 0.5)) * (1 - mU);
  const baseY = box.y + box.h;
  const c = col(P, p.color, P.blue), hc = col(P, p.highlightColor, P.gold);
  return (
    <g opacity={opacity}>
      {p.title && <text x={box.x} y={box.y - 54} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={40} opacity={E.out(win(t, start - 0.5, 0.5)) * (1 - mU)}>{p.title}</text>}
      {p.note && <text x={box.x} y={box.y - 20} fill={P.muted} fontFamily={FONT.body} fontWeight={600} fontSize={20} letterSpacing={2} opacity={axisU}>{p.note.toUpperCase()}</text>}
      {/* gridlines */}
      {[0.25, 0.5, 0.75, 1].map((g) => <line key={g} x1={box.x} x2={box.x + box.w * axisU} y1={baseY - box.h * g} y2={baseY - box.h * g} stroke={P.grid} strokeWidth={2} />)}
      <line x1={box.x} x2={box.x + box.w * axisU} y1={baseY} y2={baseY} stroke={P.border} strokeWidth={3} />
      {p.dataB && p.periodLabels && (
        <g opacity={axisU}>
          <text x={box.x + box.w} y={box.y - 20} textAnchor="end" fill={changeU > 0.5 ? hc : P.muted} fontFamily={FONT.body} fontWeight={800} fontSize={24}>
            {changeU > 0.5 ? p.periodLabels[1] : p.periodLabels[0]}</text>
        </g>)}
      {data.map((d, i) => {
        const s0 = start + i * stagger;
        const g = clamp(E.outBack(win(t, s0, grow)), 0, 1.08);
        if (g <= 0 && mU === 0) return null;
        const h = (box.h * vals[i]) / vmax * g;
        const x = box.x + i * gap + (gap - bw) / 2;
        const isHi = i === hi;
        const fillC = isHi && hiU > 0 ? hc : c;
        // morph: interpolate the bar rectangle into its diagram box
        const mb = p.morph?.boxes[i];
        const R = mb ? {x: lerp(x, mb.x, mU), y: lerp(baseY - h, mb.y, mU), w: lerp(bw, mb.w, mU), h: lerp(h, mb.h, mU)} : {x, y: baseY - h, w: bw, h};
        const shown = d.display && changeU === 0 && g >= 1 ? d.display : `${pre}${fmt(vals[i] * Math.min(1, g), decimals)}${suf}`;
        return (
          <g key={i}>
            {isHi && hiU > 0 && mU < 0.5 && <rect x={R.x - 10} y={R.y - 10} width={R.w + 20} height={R.h + 20} rx={10} fill={hc} opacity={0.16 * hiU * (1 + 0.3 * Math.sin(t * 6))} />}
            <rect x={R.x} y={R.y} width={R.w} height={Math.max(0, R.h)} rx={lerp(6, 18, mU)} fill={mU > 0.5 ? P.panel : fillC}
              stroke={mU > 0 ? fillC : 'none'} strokeWidth={3} opacity={0.95} />
            <text x={x + bw / 2} y={baseY + 38} textAnchor="middle" fill={P.muted} fontFamily={FONT.body} fontWeight={600} fontSize={24} opacity={(1 - mU) * clamp(g)}>{d.label ?? d.name}</text>
            <text x={x + bw / 2} y={baseY - h - 16} textAnchor="middle" fill={isHi && hiU > 0 ? hc : P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={30}
              opacity={(1 - mU) * clamp(g * 1.5 - 0.5)}>{shown}</text>
            {mb && mU > 0.6 && <g opacity={E.out(win(mU, 0.6, 0.4))}>
              <text x={mb.x + mb.w / 2} y={mb.y + mb.h / 2 + (mb.sub ? -2 : 10)} textAnchor="middle" fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={28}>{mb.label}</text>
              {mb.sub && <text x={mb.x + mb.w / 2} y={mb.y + mb.h / 2 + 30} textAnchor="middle" fill={P.muted} fontFamily={FONT.body} fontSize={20}>{mb.sub}</text>}
            </g>}
          </g>
        );
      })}
      {hi > 0 && hiU > 0 && mU < 0.3 && (() => {
        const x0 = box.x + (hi - 1) * gap + gap / 2, x1 = box.x + hi * gap + gap / 2;
        const y0 = baseY - (box.h * vals[hi - 1]) / vmax - 60, y1 = baseY - (box.h * vals[hi]) / vmax - 60;
        const d = shapes.arrow([x0, y0], [lerp(x0, x1, hiU), lerp(y0, y1, hiU)], -0.15);
        return <g opacity={1 - mU * 3}><path d={d} fill="none" stroke={hc} strokeWidth={4} strokeLinecap="round" />
          <text x={(x0 + x1) / 2} y={Math.min(y0, y1) - 34} textAnchor="middle" fill={hc} fontFamily={FONT.body} fontWeight={800} fontSize={24} opacity={hiU}>FASTEST GROWTH</text></g>;
      })()}
      {p.morph?.arrows?.map(([a, b], k) => {
        const A = p.morph!.boxes[a], B = p.morph!.boxes[b];
        const u = E.inOut(win(t, p.morph!.at + (p.morph!.dur ?? 1.2) * 0.7 + k * 0.15, 0.5));
        if (u <= 0) return null;
        const from: Vec = [A.x + A.w + 8, A.y + A.h / 2], to: Vec = [B.x - 8, B.y + B.h / 2];
        const tl = buildDrawTimeline([{d: shapes.arrow(from, to, 0), duration: 0.5, color: P.gold, width: 4}], {start: p.morph!.at + (p.morph!.dur ?? 1.2) * 0.7 + k * 0.15});
        return <DrawOnCanvas key={k} t={t} timeline={tl} glow={false} />;
      })}
    </g>
  );
};

export type LineChartProps = Themed & {
  t: number; data: Datum[]; box: Box; start?: number; draw?: number; title?: string; note?: string;
  valuePrefix?: string; valueSuffix?: string; decimals?: number; color?: string; area?: boolean; yMax?: number; opacity?: number;
};

export const LineChart: React.FC<LineChartProps> = (p) => {
  const P = pal(p.palette);
  const {t, data, box, start = 0, draw = 2, decimals = 0, opacity = 1} = p;
  const vmax = p.yMax ?? niceMax(Math.max(...data.map((d) => d.value)));
  const pts: Vec[] = data.map((d, i) => [box.x + (box.w * i) / Math.max(1, data.length - 1), box.y + box.h - (box.h * d.value) / vmax]);
  const d = shapes.curve(pts);
  const tl = buildDrawTimeline([{d, start, duration: draw, color: col(P, p.color, P.gold), width: 6, ease: E.inOut}]);
  const s = tl.strokes[0];
  const u = E.inOut(win(t, start, draw));
  const c = col(P, p.color, P.gold);
  const ax = E.out(win(t, start - 0.5, 0.5));
  return (
    <g opacity={opacity}>
      {p.title && <text x={box.x} y={box.y - 54} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={40} opacity={ax}>{p.title}</text>}
      {p.note && <text x={box.x} y={box.y - 20} fill={P.muted} fontFamily={FONT.body} fontWeight={600} fontSize={20} letterSpacing={2} opacity={ax}>{p.note.toUpperCase()}</text>}
      {[0.25, 0.5, 0.75, 1].map((g) => <line key={g} x1={box.x} x2={box.x + box.w * ax} y1={box.y + box.h * (1 - g)} y2={box.y + box.h * (1 - g)} stroke={P.grid} strokeWidth={2} />)}
      {p.area && u > 0 && <path d={`${d} L ${pts[pts.length - 1][0]} ${box.y + box.h} L ${pts[0][0]} ${box.y + box.h} Z`} fill={c}
        opacity={0.16} style={{clipPath: `inset(0 ${(1 - u) * 100}% 0 0)`}} />}
      <DrawOnCanvas t={t} timeline={tl} />
      {pts.map((q, i) => {
        const at = start + (draw * i) / Math.max(1, pts.length - 1);
        const g = E.outBack(win(t, at - 0.05, 0.4));
        if (g <= 0) return null;
        return <g key={i}>
          <circle cx={q[0]} cy={q[1]} r={10 * g} fill={P.bg} stroke={c} strokeWidth={4} />
          <text x={q[0]} y={q[1] - 22} textAnchor="middle" fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={26} opacity={clamp(g)}>
            {data[i].display ?? `${p.valuePrefix ?? ''}${fmt(data[i].value, decimals)}${p.valueSuffix ?? ''}`}</text>
          <text x={q[0]} y={box.y + box.h + 36} textAnchor="middle" fill={P.muted} fontFamily={FONT.body} fontSize={22} opacity={clamp(g)}>{data[i].label}</text>
        </g>;
      })}
      {void s}
    </g>
  );
};

export type DonutProps = Themed & {
  t: number; data: Datum[]; cx: number; cy: number; r?: number; thick?: number; start?: number; sweep?: number;
  dataB?: Datum[]; changeAt?: number; colors?: string[]; center?: string; centerSub?: string; opacity?: number;
};

export const Donut: React.FC<DonutProps> = (p) => {
  const P = pal(p.palette);
  const {t, cx, cy, r = 220, thick = 70, start = 0, sweep = 1.4, opacity = 1} = p;
  const cu = p.dataB ? E.inOut(win(t, p.changeAt ?? 1e9, 1)) : 0;
  const vals = p.data.map((d, i) => lerp(d.value, p.dataB?.[i]?.value ?? d.value, cu));
  const tot = vals.reduce((a, b) => a + b, 0) || 1;
  const colors = p.colors || [P.gold, P.blue, P.teal, P.muted, P.border];
  let acc = 0;
  const arc = (a0: number, a1: number) => {
    const p0 = [cx + r * Math.cos(a0), cy + r * Math.sin(a0)], p1 = [cx + r * Math.cos(a1), cy + r * Math.sin(a1)];
    return `M ${p0[0]} ${p0[1]} A ${r} ${r} 0 ${a1 - a0 > Math.PI ? 1 : 0} 1 ${p1[0]} ${p1[1]}`;
  };
  return (
    <g opacity={opacity}>
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={P.grid} strokeWidth={thick} />
      {vals.map((v, i) => {
        const a0 = -Math.PI / 2 + (acc / tot) * Math.PI * 2;
        acc += v;
        const a1full = -Math.PI / 2 + (acc / tot) * Math.PI * 2;
        const u = E.inOut(win(t, start + (i * sweep) / vals.length, sweep / vals.length + 0.2));
        if (u <= 0) return null;
        const a1 = lerp(a0, a1full, u);
        const mid = (a0 + a1full) / 2;
        return <g key={i}>
          <path d={arc(a0, Math.max(a0 + 0.001, a1 - 0.01))} fill="none" stroke={colors[i % colors.length]} strokeWidth={thick} />
          <text x={cx + (r + thick) * Math.cos(mid)} y={cy + (r + thick) * Math.sin(mid)} textAnchor={Math.cos(mid) > 0 ? 'start' : 'end'}
            fill={P.ink} fontFamily={FONT.body} fontWeight={700} fontSize={24} opacity={E.out(win(t, start + sweep, 0.4))}>
            {p.data[i].label} {fmt((v / tot) * 100, 0)}%</text>
        </g>;
      })}
      {p.center && <text x={cx} y={cy + 16} textAnchor="middle" fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={56}>{p.center}</text>}
      {p.centerSub && <text x={cx} y={cy + 52} textAnchor="middle" fill={P.muted} fontFamily={FONT.body} fontSize={22}>{p.centerSub}</text>}
    </g>
  );
};
