import React, {useMemo} from 'react';
import {getLength} from '@remotion/paths';
import {pointAt, tangentAt} from '../../lib/pathsafe';
import {E, clamp, col, lerpV, pal, win} from '../motion';
import type {Themed, Vec} from '../types';

/**
 * DrawOnCanvas: progressive SVG drawing with a real drawing instrument.
 *
 * Every stroke is revealed with stroke-dasharray / stroke-dashoffset by its measured path length, at a set
 * speed (px/s) or duration. Strokes run in sequence (or at explicit start times), with pauses; between strokes
 * the pen LIFTS and travels to the next start point. `penAt(timeline, t)` returns where the pen tip is at any
 * time, so a hand (AnimatedPresenter) or the built-in pen follows the stroke being drawn.
 */
export type DrawStroke = {
  d: string;
  /** absolute start (s); default: after the previous stroke + its pause */
  start?: number;
  /** drawing speed in px/s (default timeline speed) or a fixed duration */
  speed?: number;
  duration?: number;
  pauseAfter?: number;
  color?: string;
  width?: number;
  /** fill revealed after the stroke completes */
  fill?: string;
  fillOpacity?: number;
  dash?: string;           // a dashed style applied once drawn (e.g. '10 8')
  ease?: (u: number) => number;
  /** after drawing: dashes keep flowing along the stroke (px/s; e.g. light, money, a stream) */
  flow?: number;
  /** after drawing: the stroke pulses (glow + width), e.g. a plasma or a hot spot */
  pulse?: boolean;
  /** semantic tag for QC (box, arrow, bar, map, text); has no visual effect */
  kind?: string;
  /** text label written along with the stroke (appears progressively) */
  label?: {text: string; x: number; y: number; size?: number; color?: string; anchor?: 'start' | 'middle' | 'end'};
};

export type TimedStroke = DrawStroke & {t0: number; t1: number; len: number};
export type DrawTimeline = {strokes: TimedStroke[]; start: number; end: number; liftSpeed: number};

/** Compute start/end times of each stroke. Pure function: memoise it per scene. */
export const buildDrawTimeline = (strokes: DrawStroke[], opts: {start?: number; speed?: number; pause?: number; liftSpeed?: number} = {}): DrawTimeline => {
  const speed = opts.speed ?? 900, pause = opts.pause ?? 0.12;
  let cursor = opts.start ?? 0;
  const out: TimedStroke[] = [];
  let prevEnd: Vec | null = null;
  const liftSpeed = opts.liftSpeed ?? 1800;
  for (const s of strokes) {
    const len = Math.max(1, getLength(s.d));
    const p0 = pointAt(s.d, 0);
    // time for the lifted pen to travel from the previous stroke's end to this stroke's start
    const lift = prevEnd ? Math.hypot(p0.x - prevEnd[0], p0.y - prevEnd[1]) / liftSpeed : 0;
    const t0 = s.start ?? cursor + Math.min(0.5, lift);
    const dur = s.duration ?? len / (s.speed ?? speed);
    out.push({...s, t0, t1: t0 + dur, len});
    cursor = t0 + dur + (s.pauseAfter ?? pause);
    const pe = pointAt(s.d, len);
    prevEnd = [pe.x, pe.y];
  }
  return {strokes: out, start: out.length ? out[0].t0 : 0, end: out.length ? out[out.length - 1].t1 : 0, liftSpeed};
};

export type PenState = {pt: Vec; down: boolean; angle: number; active: number /* index or -1 */};

/** Pen tip position at time t: on the stroke while drawing, travelling (lifted) between strokes. */
export const penAt = (tl: DrawTimeline, t: number): PenState => {
  const S = tl.strokes;
  if (!S.length) return {pt: [0, 0], down: false, angle: 0, active: -1};
  for (let i = 0; i < S.length; i++) {
    const s = S[i];
    if (t >= s.t0 && t <= s.t1) {
      const u = (s.ease || E.inOut)(win(t, s.t0, s.t1 - s.t0));
      const p = pointAt(s.d, u * s.len), tg = tangentAt(s.d, u * s.len);
      return {pt: [p.x, p.y], down: true, angle: Math.atan2(tg.y, tg.x), active: i};
    }
    const next = S[i + 1];
    if (next && t > s.t1 && t < next.t0) {                    // lifted, moving to the next stroke
      const a = pointAt(s.d, s.len), b = pointAt(next.d, 0);
      const u = E.inOut(win(t, s.t1, next.t0 - s.t1));
      const q = lerpV([a.x, a.y], [b.x, b.y], u);
      return {pt: [q[0], q[1] - Math.sin(Math.PI * u) * 18], down: false, angle: 0, active: -1};
    }
  }
  if (t < S[0].t0) { const p = pointAt(S[0].d, 0); return {pt: [p.x, p.y], down: false, angle: 0, active: -1}; }
  const last = S[S.length - 1], p = pointAt(last.d, last.len);
  return {pt: [p.x, p.y], down: false, angle: 0, active: -1};
};

/** Revealed fraction of stroke i at time t. */
export const strokeProgress = (s: TimedStroke, t: number) => (s.ease || E.inOut)(win(t, s.t0, s.t1 - s.t0));

export type DrawOnCanvasProps = Themed & {
  t: number;
  timeline: DrawTimeline;
  /** draw a stand-alone pen/marker at the tip (when no presenter hand is used) */
  showPen?: boolean;
  defaultColor?: string;
  defaultWidth?: number;
  /** fade the whole drawing (e.g. when it morphs into the next diagram) */
  opacity?: number;
  /** glow under fresh strokes */
  glow?: boolean;
};

export const DrawOnCanvas: React.FC<DrawOnCanvasProps> = ({t, timeline, showPen, defaultColor, defaultWidth = 6, opacity = 1, glow = true, palette}) => {
  const P = pal(palette);
  const pen = penAt(timeline, t);
  return (
    <g opacity={opacity}>
      {timeline.strokes.map((s, i) => {
        const u = strokeProgress(s, t);
        if (u <= 0) return null;
        const c = col(P, s.color, col(P, defaultColor, P.ink));
        const w = s.width ?? defaultWidth;
        const fillU = s.fill ? clamp((t - s.t1) / 0.4) : 0;
        const done = u >= 1;
        return (
          <g key={i}>
            {s.fill && fillU > 0 && <path d={s.d} fill={col(P, s.fill)} opacity={(s.fillOpacity ?? 0.25) * fillU} stroke="none" />}
            {glow && !done && <path d={s.d} fill="none" stroke={c} strokeWidth={w * 3} strokeOpacity={0.18} strokeLinecap="round"
              strokeDasharray={`${s.len} ${s.len}`} strokeDashoffset={s.len * (1 - u)} />}
            <path d={s.d} fill="none" stroke={c} strokeWidth={w * (s.pulse && done ? 1 + 0.35 * Math.abs(Math.sin((t - s.t1) * 6)) : 1)} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={done && s.dash ? s.dash : `${s.len} ${s.len}`} strokeDashoffset={done && s.dash ? 0 : s.len * (1 - u)} />
            {done && s.flow ? <path d={s.d} fill="none" stroke="#FFFFFF" strokeOpacity={0.8} strokeWidth={Math.max(5, w * 1.1)} strokeLinecap="round"
              strokeDasharray="10 24" strokeDashoffset={-(t - s.t1) * s.flow} /> : null}
            {done && s.pulse ? <path d={s.d} fill="none" stroke={c} strokeOpacity={0.35 * Math.abs(Math.sin((t - s.t1) * 6))} strokeWidth={w * 4} strokeLinecap="round" /> : null}
            {s.label && (() => {
              const L = s.label!, size = L.size || 30;
              const n = L.text.length, shown = Math.ceil(n * clamp((t - s.t0) / Math.max(0.2, s.t1 - s.t0)));
              return <text x={L.x} y={L.y} fill={col(P, L.color, c)} fontFamily="Inter, sans-serif" fontWeight={800} fontSize={size}
                textAnchor={L.anchor || 'start'} letterSpacing={1}>{L.text.slice(0, shown)}</text>;
            })()}
          </g>
        );
      })}
      {showPen && t >= timeline.start - 0.6 && t <= timeline.end + 0.8 && (
        <g transform={`translate(${pen.pt[0]} ${pen.pt[1] - (pen.down ? 0 : 6)}) rotate(-35)`}>
          <rect x={-4} y={-70} width={16} height={64} rx={5} fill={P.gold} />
          <path d="M -4 -6 L 12 -6 L 4 4 Z" fill="#1A1C20" />
          {pen.down && <circle cx={4} cy={4} r={8} fill={P.gold} opacity={0.35} />}
        </g>
      )}
    </g>
  );
};

/* ---------------------------------------------------------------- shape builders (return SVG path data) */
const f = (n: number) => n.toFixed(1);
export const shapes = {
  line: (a: Vec, b: Vec) => `M ${f(a[0])} ${f(a[1])} L ${f(b[0])} ${f(b[1])}`,
  polyline: (pts: Vec[]) => pts.map((p, i) => `${i ? 'L' : 'M'} ${f(p[0])} ${f(p[1])}`).join(' '),
  /** smooth curve through points (Catmull-Rom converted to cubic Béziers) */
  curve: (pts: Vec[]) => {
    if (pts.length < 3) return shapes.polyline(pts);
    let d = `M ${f(pts[0][0])} ${f(pts[0][1])}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      const c1: Vec = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2: Vec = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += ` C ${f(c1[0])} ${f(c1[1])} ${f(c2[0])} ${f(c2[1])} ${f(p2[0])} ${f(p2[1])}`;
    }
    return d;
  },
  circle: (c: Vec, r: number) => `M ${f(c[0] - r)} ${f(c[1])} A ${r} ${r} 0 1 0 ${f(c[0] + r)} ${f(c[1])} A ${r} ${r} 0 1 0 ${f(c[0] - r)} ${f(c[1])}`,
  rect: (x: number, y: number, w: number, h: number) => `M ${x} ${y} L ${x + w} ${y} L ${x + w} ${y + h} L ${x} ${y + h} Z`,
  /** arrow with a bowed shaft and a two-stroke head drawn in the same path */
  arrow: (a: Vec, b: Vec, bend = 0.15) => {
    const mx = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, my = (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend;
    const ang = Math.atan2(b[1] - my, b[0] - mx);
    const h1: Vec = [b[0] - 24 * Math.cos(ang - 0.45), b[1] - 24 * Math.sin(ang - 0.45)];
    const h2: Vec = [b[0] - 24 * Math.cos(ang + 0.45), b[1] - 24 * Math.sin(ang + 0.45)];
    return `M ${f(a[0])} ${f(a[1])} Q ${f(mx)} ${f(my)} ${f(b[0])} ${f(b[1])} M ${f(h1[0])} ${f(h1[1])} L ${f(b[0])} ${f(b[1])} L ${f(h2[0])} ${f(h2[1])}`;
  },
  /** chart axes for a box (origin bottom-left) */
  axes: (x: number, y: number, w: number, h: number) => `M ${x} ${y} L ${x} ${y + h} L ${x + w} ${y + h}`,
  /** timeline baseline with ticks */
  timeline: (x: number, y: number, w: number, ticks: number) =>
    `M ${x} ${y} L ${x + w} ${y}` + Array.from({length: ticks}, (_, i) => ` M ${f(x + (w * i) / Math.max(1, ticks - 1))} ${y - 12} L ${f(x + (w * i) / Math.max(1, ticks - 1))} ${y + 12}`).join(''),
};
