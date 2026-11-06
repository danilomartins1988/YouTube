import {Easing, spring} from 'remotion';
import type {Vec} from '../types';

export * from './theme';

/* ---------------------------------------------------------------- deterministic time helpers (seconds) */
export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, u: number) => a + (b - a) * u;
export const lerpV = (a: Vec, b: Vec, u: number): Vec => [lerp(a[0], b[0], u), lerp(a[1], b[1], u)];
/** linear 0..1 progress of a window [start, start+dur] */
export const win = (t: number, start: number, dur: number) => (dur <= 0 ? (t >= start ? 1 : 0) : clamp((t - start) / dur));

export const E = {
  linear: (u: number) => u,
  out: Easing.out(Easing.cubic),
  in: Easing.in(Easing.cubic),
  inOut: Easing.inOut(Easing.cubic),
  outBack: Easing.out(Easing.back(1.7)),
  inBack: Easing.in(Easing.back(1.7)),          // anticipation: pulls back before moving
  inOutBack: Easing.inOut(Easing.back(1.4)),
  outExpo: Easing.out(Easing.exp),
  inOutQuint: Easing.inOut(Easing.poly(5)),
};
export const ease = (t: number, start: number, dur: number, fn: (u: number) => number = E.inOut) => fn(win(t, start, dur));

/** Physically based spring (Remotion spring) driven by seconds; returns ~0..1 with natural overshoot. */
export const springAt = (t: number, start: number, fps = 30, config: {damping?: number; stiffness?: number; mass?: number} = {}) =>
  t < start ? 0 : spring({frame: (t - start) * fps, fps, config: {damping: 12, stiffness: 120, mass: 0.8, ...config}});

/** Fade envelope for an element that lives in [a, b] with fade-in fi and fade-out fo. */
export const life = (t: number, a: number, b: number, fi = 0.4, fo = 0.4) => Math.min(ease(t, a, fi, E.out), 1 - ease(t, b - fo, fo, E.in));

/** Stagger helper: start time of item i. */
export const stagger = (start: number, i: number, step: number) => start + i * step;

/* ---------------------------------------------------------------- geometry */
export const quadPt = (a: Vec, c: Vec, b: Vec, u: number): Vec => [
  (1 - u) ** 2 * a[0] + 2 * (1 - u) * u * c[0] + u * u * b[0], (1 - u) ** 2 * a[1] + 2 * (1 - u) * u * c[1] + u * u * b[1]];
export const quadTan = (a: Vec, c: Vec, b: Vec, u: number): number =>
  Math.atan2(2 * (1 - u) * (c[1] - a[1]) + 2 * u * (b[1] - c[1]), 2 * (1 - u) * (c[0] - a[0]) + 2 * u * (b[0] - c[0]));
/** Control point that bows a straight a->b segment into an arc: `lift` is a fraction of the segment length,
 * applied perpendicular to it (negative = to the left of travel, i.e. upward for left-to-right routes). */
export const arcCtrl = (a: Vec, b: Vec, lift = -0.25): Vec => {
  const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2, dx = b[0] - a[0], dy = b[1] - a[1];
  const L = Math.hypot(dx, dy) || 1;
  void L;
  return [mx - dy * lift, my + dx * lift];
};
export const quadPath = (a: Vec, c: Vec, b: Vec, u = 1, n = 40) => {
  let d = '';
  for (let i = 0; i <= n; i++) { const q = quadPt(a, c, b, (i / n) * u); d += (i ? ' L ' : 'M ') + q[0].toFixed(1) + ' ' + q[1].toFixed(1); }
  return d;
};

/** Deterministic pseudo-random in [0,1) from an integer seed (no Math.random in renders). */
export const rnd = (seed: number) => { const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export const fmt = (v: number, d = 0) => v.toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d});
