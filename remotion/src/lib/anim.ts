import React from 'react';
import {Easing, interpolate} from 'remotion';
import type {Palette, SceneSpec} from './types';

export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));

/** 0..1 progress of an animation that starts at `start` seconds and lasts `dur` seconds. */
export const prog = (t: number, start: number, dur: number) => (dur <= 0 ? (t >= start ? 1 : 0) : clamp((t - start) / dur));

export const easeOut = Easing.out(Easing.cubic);
export const easeInOut = Easing.inOut(Easing.cubic);
export const easeBack = Easing.out(Easing.back(1.6));

export const eo = (t: number, start: number, dur: number) => easeOut(prog(t, start, dur));
export const eio = (t: number, start: number, dur: number) => easeInOut(prog(t, start, dur));

export const lerp = (a: number, b: number, u: number) => a + (b - a) * u;

export const mix = (h1: string, h2: string, u: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [a, b] = [p(h1), p(h2)];
  return `rgb(${a.map((v, i) => Math.round(lerp(v, b[i], u))).join(',')})`;
};

export const norm = (w: string) => w.toLowerCase().replace(/[^\w%]/g, '');

/** Scene context: time helpers bound to one scene's narration timing. */
export type Ctx = {
  t: number; // seconds into the scene
  frame: number;
  fps: number;
  W: number;
  H: number;
  pal: Palette;
  font: {display: string; body: string};
  scene: SceneSpec;
  /** optional game HUD (project style.hud): mission objectives */
  hud?: {missions: string[]; objectives?: string[]};
  /** seconds at which a cue phrase is spoken; falls back to fraction of speech */
  cue: (spec: any, fallback?: number) => number;
};

export const makeCue = (scene: SceneSpec) => (spec: any, fallback = 0): number => {
  const speechAt = (f: number) => scene.lead + f * scene.speech;
  if (spec === undefined || spec === null) return speechAt(fallback);
  if (typeof spec === 'number') return speechAt(spec);
  if (typeof spec === 'string') spec = {cue: spec};
  if (spec.at !== undefined) return speechAt(Number(spec.at)) + Number(spec.offset || 0);
  if (spec.cue) {
    const target = String(spec.cue).split(/\s+/).map(norm).filter(Boolean);
    const seq = scene.words.map((w) => norm(w.word));
    for (let i = 0; i + target.length <= seq.length; i++) {
      let ok = true;
      for (let j = 0; j < target.length; j++) if (seq[i + j] !== target[j]) { ok = false; break; }
      if (ok) return scene.words[i].start + Number(spec.offset || 0);
    }
    // fall back to the character position in the narration
    const idx = scene.narration.toLowerCase().indexOf(String(spec.cue).toLowerCase());
    if (idx >= 0) return scene.lead + (scene.speech * idx) / Math.max(1, scene.narration.length) + Number(spec.offset || 0);
  }
  return speechAt(fallback);
};

export const SceneCtx = React.createContext<Ctx | null>(null);
export const useCtx = () => {
  const c = React.useContext(SceneCtx);
  if (!c) throw new Error('SceneCtx missing');
  return c;
};

/** deterministic pseudo-random in [0,1) */
export const rand = (seed: number) => {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
};

export const fmtNum = (v: number, decimals = 0) =>
  v.toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});

/** Animate the numeric part of a display string ("NOK 20,000bn") from 0 to its value. */
export const countDisplay = (display: string, u: number) => {
  const m = display.match(/[\d][\d,]*(?:\.\d+)?/);
  if (!m || u >= 1) return display;
  const raw = m[0];
  const dec = raw.includes('.') ? raw.split('.')[1].length : 0;
  const v = parseFloat(raw.replace(/,/g, ''));
  return display.slice(0, m.index) + fmtNum(v * u, dec) + display.slice((m.index || 0) + raw.length);
};

export {interpolate};


/** Normalised word being spoken at time t (scene-relative), or '' between words. */
export const spokenAt = (scene: SceneSpec, t: number) => {
  const w = scene.words.find((x) => x.start <= t && t < x.end + 0.05);
  return w ? norm(w.word) : '';
};

/**
 * Which of several items should be in focus at time t: the one whose keyword was spoken most recently
 * (within `hold` seconds), otherwise a steady cycle every `period` seconds after `start`. This keeps data
 * scenes changing every few seconds and ties the change to the narration when possible.
 */
export const focusIndex = (scene: SceneSpec, t: number, keys: string[][], start: number, period = 3.2, hold = 4) => {
  let best = -1, bestT = -1;
  for (const w of scene.words) {
    if (w.start > t || w.start < t - hold) continue;
    const n = norm(w.word);
    keys.forEach((k, i) => { if (k.includes(n) && w.start > bestT) { best = i; bestT = w.start; } });
  }
  if (best >= 0) return best;
  if (t < start) return -1;
  return Math.floor((t - start) / period) % Math.max(1, keys.length);
};

export const keywords = (label: string) => String(label).split(/[\s(),&/+-]+/).map(norm).filter((x) => x.length > 2);
