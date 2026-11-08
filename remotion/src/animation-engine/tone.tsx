import React from 'react';
import {clamp, lerp, win} from './motion';

/**
 * Adaptive visual tone (the story sets the atmosphere, not the cartoon style).
 *
 * A tone changes HOW a scene feels without changing what it explains: sky and light, colour grading (saturation /
 * sepia), vignette, a spotlight, an alarm pulse, film grain, and which decorations may appear (a sun with a face,
 * cheerful clouds). Scenes take `tone: '<name>'` and optionally `toneShift: {at, to, dur}` to turn the mood inside
 * a scene (e.g. a bright growth story that darkens when the auditor refuses to sign). `bright` is the original
 * cheerful look and the default, so storyboards without a tone render exactly as before.
 */
export type ToneName = 'bright' | 'thriller' | 'crisis' | 'strategy' | 'trade' | 'tech' | 'history' | 'reflective';
export type ToneSpec = {
  sky: [string, string]; nightSky: [string, string];
  sun: 'face' | 'plain' | 'none'; clouds: 'white' | 'grey' | 'none'; stars: boolean;
  saturate: number; sepia: number;            // 1 = unchanged colours; sepia 0..1
  tint: string; tintOpacity: number;          // multiply wash over the world
  vignette: number;                           // 0..1 darkness at the frame edges
  spot: number;                               // 0..1 spotlight (dark frame, lit centre)
  pulse: number;                              // 0..1 slow red alarm pulse (crisis)
  grain: number;                              // 0..1 film grain / archival lines
  glow: string | null;                        // screen-blend glow colour (tech)
  bounce: number;                             // 0..1 multiplier for playful motion (bobbing, wobble)
  exposure?: number;                          // <1 darkens the world (indoor sets too); default 1
};

export const TONES: Record<ToneName, ToneSpec> = {
  bright: {sky: ['#7FD3F7', '#D8F4FF'], nightSky: ['#1B2A5A', '#3D4F8F'], sun: 'face', clouds: 'white', stars: true,
    saturate: 1, sepia: 0, tint: '#000000', tintOpacity: 0, vignette: 0, spot: 0, pulse: 0, grain: 0, glow: null, bounce: 1},
  // fraud, manipulation, missing money: dark, restrained, a single pool of light on the evidence
  thriller: {sky: ['#141B26', '#2B3546'], nightSky: ['#0B1018', '#1C2533'], sun: 'none', clouds: 'none', stars: false,
    saturate: 0.45, sepia: 0, tint: '#2A3550', tintOpacity: 0.28, vignette: 0.78, spot: 0.55, pulse: 0, grain: 0.25, glow: null, bounce: 0.25, exposure: 0.8},
  // bank runs, collapses, contagion: high contrast, storm sky, an alarm pulse that grows with the crisis
  crisis: {sky: ['#3A2226', '#7A3F38'], nightSky: ['#1E1216', '#4A2428'], sun: 'none', clouds: 'grey', stars: false,
    saturate: 0.45, sepia: 0, tint: '#5A1E1E', tintOpacity: 0.3, vignette: 0.6, spot: 0, pulse: 0.35, grain: 0.15, glow: null, bounce: 0.35, exposure: 0.88},
  // rivalries, acquisitions, decisions: clean, cool, diagrammatic
  strategy: {sky: ['#D7E2EC', '#F3F6F9'], nightSky: ['#22324A', '#3A4E6E'], sun: 'none', clouds: 'none', stars: false,
    saturate: 0.75, sepia: 0, tint: '#C9D6E3', tintOpacity: 0.12, vignette: 0.22, spot: 0, pulse: 0, grain: 0, glow: null, bounce: 0.5, exposure: 1.0},
  // shipping, ports, supply chains: bright and exploratory, but no cartoon face in the sky
  trade: {sky: ['#7FC8EE', '#DDF3FF'], nightSky: ['#1B2A5A', '#3D4F8F'], sun: 'plain', clouds: 'white', stars: true,
    saturate: 0.95, sepia: 0, tint: '#000000', tintOpacity: 0, vignette: 0.18, spot: 0, pulse: 0, grain: 0, glow: null, bounce: 0.8},
  // chips, AI, machines: deep blue, cyan glow, precise
  tech: {sky: ['#0A1630', '#17305A'], nightSky: ['#060D1E', '#10224A'], sun: 'none', clouds: 'none', stars: true,
    saturate: 0.9, sepia: 0, tint: '#0E2A55', tintOpacity: 0.16, vignette: 0.45, spot: 0.15, pulse: 0, grain: 0, glow: '#3FD0FF', bounce: 0.45, exposure: 0.62},
  // economic history: archival paper light, sepia grade, grain
  history: {sky: ['#D9C79E', '#F1E6CC'], nightSky: ['#3A3022', '#5A4A34'], sun: 'plain', clouds: 'grey', stars: false,
    saturate: 0.6, sepia: 0.55, tint: '#8A6A3A', tintOpacity: 0.14, vignette: 0.55, spot: 0, pulse: 0, grain: 0.45, glow: null, bounce: 0.4},
  // conclusions after a serious story: calm, low light, nothing playful
  reflective: {sky: ['#2A3142', '#566078'], nightSky: ['#141A26', '#2A3142'], sun: 'none', clouds: 'none', stars: false,
    saturate: 0.55, sepia: 0.08, tint: '#323A4E', tintOpacity: 0.2, vignette: 0.6, spot: 0.25, pulse: 0, grain: 0.15, glow: null, bounce: 0.2, exposure: 0.78},
};

export type ToneShift = {at: number; to: ToneName; dur?: number};
const hex = (c: string) => [1, 3, 5].map((i) => parseInt(c.slice(i, i + 2), 16));
const mix = (a: string, b: string, u: number) => '#' + hex(a).map((v, i) => Math.round(lerp(v, hex(b)[i], u)).toString(16).padStart(2, '0')).join('');

/** The tone in effect at time t (numbers and colours interpolate during a toneShift). */
export const toneAt = (name: string | undefined, shift: ToneShift | undefined, t: number): ToneSpec & {name: string; u: number} => {
  const a = TONES[(name as ToneName)] || TONES.bright;
  if (!shift || !TONES[shift.to]) return {...a, name: name || 'bright', u: 0};
  const b = TONES[shift.to], u = clamp(win(t, shift.at, shift.dur ?? 2.5));
  if (u <= 0) return {...a, name: name || 'bright', u};
  const n = (k: keyof ToneSpec) => lerp(a[k] as number, b[k] as number, u);
  return {
    sky: [mix(a.sky[0], b.sky[0], u), mix(a.sky[1], b.sky[1], u)], nightSky: [mix(a.nightSky[0], b.nightSky[0], u), mix(a.nightSky[1], b.nightSky[1], u)],
    sun: u < 0.5 ? a.sun : b.sun, clouds: u < 0.5 ? a.clouds : b.clouds, stars: u < 0.5 ? a.stars : b.stars,
    saturate: n('saturate'), sepia: n('sepia'), tint: mix(a.tint, b.tint, u), tintOpacity: n('tintOpacity'), vignette: n('vignette'),
    spot: n('spot'), pulse: n('pulse'), grain: n('grain'), exposure: lerp(a.exposure ?? 1, b.exposure ?? 1, u), glow: u < 0.5 ? a.glow : b.glow, bounce: n('bounce'), name: u < 0.5 ? (name || 'bright') : shift.to, u,
  };
};

/** True when the tone changes nothing (so the original rendering path is used untouched). */
export const isNeutral = (s: ToneSpec) => s.saturate === 1 && s.sepia === 0 && s.tintOpacity === 0 && s.vignette === 0 && s.spot === 0 &&
  s.pulse === 0 && s.grain === 0 && !s.glow && (s.exposure ?? 1) === 1;

/** SVG colour-matrix filter for the world layer (saturation + sepia). Put inside <defs>. */
export const ToneFilterDef: React.FC<{id: string; s: ToneSpec}> = ({id, s}) => {
  const sp = s.sepia, k = 1 - sp;
  // sepia matrix blended with identity
  const sep = [0.393 * sp + k, 0.769 * sp, 0.189 * sp, 0, 0, 0.349 * sp, 0.686 * sp + k, 0.168 * sp, 0, 0, 0.272 * sp, 0.534 * sp, 0.131 * sp + k, 0, 0, 0, 0, 0, 1, 0];
  return <filter id={id} colorInterpolationFilters="sRGB" x="0" y="0" width="100%" height="100%">
    <feColorMatrix type="saturate" values={String(s.saturate)} result="sat" />
    {sp > 0 && <feColorMatrix in="sat" type="matrix" values={sep.join(' ')} />}
    {(s.exposure ?? 1) !== 1 && <feComponentTransfer><feFuncR type="linear" slope={s.exposure} /><feFuncG type="linear" slope={s.exposure} /><feFuncB type="linear" slope={(s.exposure ?? 1) * (s.glow ? 1.12 : 1)} /></feComponentTransfer>}
  </filter>;
};

/** Screen-space grade drawn ON TOP of the world (before screen callouts): tint, vignette, spotlight, pulse, grain, glow. */
export const ToneOverlay: React.FC<{s: ToneSpec; t: number; W: number; H: number; id: string; spotX?: number; spotY?: number}> = ({s, t, W, H, id, spotX = 0.5, spotY = 0.45}) => {
  if (isNeutral(s)) return null;
  const pulse = s.pulse > 0 ? s.pulse * (0.5 + 0.5 * Math.sin(t * 2.4)) : 0;
  return <g pointerEvents="none">
    <defs>
      <radialGradient id={`${id}v`} cx="50%" cy="50%" r="75%"><stop offset="55%" stopColor="#000" stopOpacity={0} /><stop offset="100%" stopColor="#000" stopOpacity={s.vignette} /></radialGradient>
      <radialGradient id={`${id}s`} cx={`${spotX * 100}%`} cy={`${spotY * 100}%`} r="55%"><stop offset="0%" stopColor="#000" stopOpacity={0} /><stop offset="60%" stopColor="#000" stopOpacity={s.spot * 0.4} /><stop offset="100%" stopColor="#000" stopOpacity={s.spot} /></radialGradient>
      <radialGradient id={`${id}p`} cx="50%" cy="50%" r="80%"><stop offset="40%" stopColor="#FF2D2D" stopOpacity={0} /><stop offset="100%" stopColor="#FF2D2D" stopOpacity={0.55} /></radialGradient>
      {s.glow && <radialGradient id={`${id}g`} cx="50%" cy="60%" r="60%"><stop offset="0%" stopColor={s.glow} stopOpacity={0.3} /><stop offset="100%" stopColor={s.glow} stopOpacity={0} /></radialGradient>}
    </defs>
    {s.tintOpacity > 0 && <rect width={W} height={H} fill={s.tint} opacity={s.tintOpacity} style={{mixBlendMode: 'multiply'}} />}
    {s.glow && <rect width={W} height={H} fill={`url(#${id}g)`} style={{mixBlendMode: 'screen'}} />}
    {s.spot > 0 && <rect width={W} height={H} fill={`url(#${id}s)`} />}
    {s.vignette > 0 && <rect width={W} height={H} fill={`url(#${id}v)`} />}
    {pulse > 0 && <rect width={W} height={H} fill={`url(#${id}p)`} opacity={pulse} />}
    {s.grain > 0 && <g opacity={s.grain * 0.5}>{Array.from({length: 26}, (_, k) => {
      const r = Math.sin((k + 1) * 91.7 + Math.floor(t * 12) * 13.3) * 43758.5453, y = (r - Math.floor(r)) * H;
      return <rect key={k} x={0} y={y} width={W} height={1 + (k % 3)} fill={k % 2 ? '#000' : '#fff'} opacity={0.18} />; })}</g>}
  </g>;
};

/** Presenter demeanour from a tone: serious tones never smile or hop. */
export const demeanorFor = (tone?: string): 'warm' | 'neutral' | 'serious' =>
  tone === 'thriller' || tone === 'crisis' || tone === 'reflective' ? 'serious' : tone === 'strategy' || tone === 'tech' || tone === 'history' ? 'neutral' : 'warm';
