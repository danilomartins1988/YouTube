import React from 'react';
import {E, FONT, clamp, pal, rnd, win} from '../motion';
import type {Themed} from '../types';

/**
 * Transitions and set pieces. These are overlays driven by t; the real continuity between scenes comes from
 * MORPHING objects (a chart point becomes a stage, a stage flies to its city, a hub opens into a chip), and these
 * pieces only punctuate it.
 */

/** Light sweep: a soft diagonal band of light crossing the frame (cinematic accent). */
export const LightSweep: React.FC<Themed & {t: number; at: number; dur?: number; W?: number; H?: number; color?: string; strength?: number}> = ({t, at, dur = 0.9, W = 1920, H = 1080, color, strength = 0.35, palette}) => {
  const P = pal(palette);
  const u = win(t, at, dur);
  if (u <= 0 || u >= 1) return null;
  const x = -600 + (W + 1200) * E.inOut(u);
  return (
    <g style={{mixBlendMode: 'screen'}}>
      <defs><linearGradient id={`sw-${at}`} x1="0" x2="1"><stop offset="0" stopColor={color || P.gold} stopOpacity={0} /><stop offset="0.5" stopColor={color || P.gold} stopOpacity={strength} /><stop offset="1" stopColor={color || P.gold} stopOpacity={0} /></linearGradient></defs>
      <rect x={x - 300} y={-200} width={600} height={H + 400} fill={`url(#sw-${at})`} transform={`rotate(18 ${x} ${H / 2})`} />
    </g>
  );
};

/** Iris: circular reveal (open) or close centred on a point. Returns a mask-like dark overlay. */
export const Iris: React.FC<Themed & {t: number; at: number; dur?: number; cx: number; cy: number; mode: 'open' | 'close'; W?: number; H?: number}> = ({t, at, dur = 0.8, cx, cy, mode, W = 1920, H = 1080, palette}) => {
  const P = pal(palette);
  const u = E.inOutQuint(win(t, at, dur));
  const R = Math.hypot(Math.max(cx, W - cx), Math.max(cy, H - cy)) + 20;
  const r = mode === 'open' ? R * u : R * (1 - u);
  if ((mode === 'open' && u >= 1) || (mode === 'close' && u <= 0)) return null;
  return (
    <g>
      <defs><mask id={`iris-${at}-${mode}`}><rect width={W} height={H} fill="#fff" /><circle cx={cx} cy={cy} r={Math.max(0, r)} fill="#000" /></mask></defs>
      <rect width={W} height={H} fill={P.bg} mask={`url(#iris-${at}-${mode})`} />
      {r > 2 && <circle cx={cx} cy={cy} r={r} fill="none" stroke={P.gold} strokeWidth={3} opacity={0.6} />}
    </g>
  );
};

/** Particle burst used when an object 'opens' into the next scene. */
export const Burst: React.FC<Themed & {t: number; at: number; cx: number; cy: number; n?: number; dist?: number; color?: string}> = ({t, at, cx, cy, n = 28, dist = 420, color, palette}) => {
  const P = pal(palette);
  const u = win(t, at, 0.9);
  if (u <= 0 || u >= 1) return null;
  return <g>{Array.from({length: n}, (_, i) => {
    const a = (i / n) * Math.PI * 2 + rnd(i) * 0.3, d = dist * (0.5 + 0.5 * rnd(i + 40)) * E.out(u);
    return <circle key={i} cx={cx + Math.cos(a) * d} cy={cy + Math.sin(a) * d} r={3 + 3 * rnd(i + 3)} fill={color || P.gold} opacity={1 - u} />;
  })}</g>;
};

/** Dark studio set: back wall with soft light panels, floor with reflection gradient, slow ambient light drift. */
export const Studio: React.FC<Themed & {t: number; W?: number; H?: number; floorY?: number; opacity?: number}> = ({t, W = 1920, H = 1080, floorY = 960, opacity = 1, palette}) => {
  const P = pal(palette);
  // a light episode palette (cartoon style) gets a sunny studio: sky-blue wall, sandy floor
  const hex = (P.bg || '#000000').replace('#', ''), lum = (parseInt(hex.slice(0, 2), 16) * 0.3 + parseInt(hex.slice(2, 4), 16) * 0.59 + parseInt(hex.slice(4, 6), 16) * 0.11) / 255;
  const light = lum > 0.6;
  const drift = Math.sin(t * 0.4) * 40;
  return (
    <g opacity={opacity}>
      <defs>
        <linearGradient id="st-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={light ? P.bg2 : '#0A1628'} /><stop offset="1" stopColor={light ? P.bg : '#0C1A2E'} /></linearGradient>
        <linearGradient id="st-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={light ? '#E9C98A' : '#111D30'} /><stop offset="1" stopColor={light ? '#C9A266' : '#060C16'} /></linearGradient>
        <radialGradient id="st-spot" cx="50%" cy="0%" r="80%"><stop offset="0" stopColor={P.gold} stopOpacity={0.12} /><stop offset="1" stopColor={P.gold} stopOpacity={0} /></radialGradient>
      </defs>
      <rect width={W} height={floorY} fill="url(#st-wall)" />
      {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={120 + i * 360 + drift * (i % 2 ? 1 : -1) * 0.2} y={60} width={6} height={floorY - 120} fill={light ? P.border : P.grid} opacity={light ? 0.12 : 0.7} />)}
      <rect width={W} height={floorY} fill="url(#st-spot)" transform={`translate(${drift} 0)`} />
      <rect y={floorY} width={W} height={H - floorY} fill="url(#st-floor)" />
      <line x1={0} x2={W} y1={floorY} y2={floorY} stroke={P.border} strokeWidth={2} />
    </g>
  );
};

/** Digital whiteboard that 'boots': frame draws, a scan line passes, then the grid fades in. */
export const DigitalBoard: React.FC<Themed & {t: number; at: number; x: number; y: number; w: number; h: number; opacity?: number}> = ({t, at, x, y, w, h, opacity = 1, palette}) => {
  const P = pal(palette);
  const frame = E.inOut(win(t, at, 0.6)), scan = win(t, at + 0.3, 0.6), grid = E.out(win(t, at + 0.6, 0.5));
  if (frame <= 0) return null;
  const per = 2 * (w + h);
  return (
    <g opacity={opacity}>
      <rect x={x} y={y} width={w} height={h} rx={18} fill={P.panel} opacity={0.92 * grid} />
      {Array.from({length: Math.floor(w / 60)}, (_, i) => <line key={'v' + i} x1={x + 60 * (i + 1)} x2={x + 60 * (i + 1)} y1={y + 10} y2={y + h - 10} stroke={P.grid} strokeWidth={1} opacity={grid * 0.7} />)}
      {Array.from({length: Math.floor(h / 60)}, (_, i) => <line key={'h' + i} x1={x + 10} x2={x + w - 10} y1={y + 60 * (i + 1)} y2={y + 60 * (i + 1)} stroke={P.grid} strokeWidth={1} opacity={grid * 0.7} />)}
      <rect x={x} y={y} width={w} height={h} rx={18} fill="none" stroke={P.blue} strokeOpacity={0.7} strokeWidth={3} strokeDasharray={`${per} ${per}`} strokeDashoffset={per * (1 - frame)} />
      {scan > 0 && scan < 1 && <rect x={x + 4} y={y + h * scan} width={w - 8} height={6} fill={P.blue} opacity={0.6} />}
    </g>
  );
};

/** Title card text with letter stagger + underline sweep. */
export const TitleReveal: React.FC<Themed & {t: number; at: number; title: string; tagline?: string; cx?: number; cy?: number}> = ({t, at, title, tagline, cx = 960, cy = 520, palette}) => {
  const P = pal(palette);
  const letters = title.split('');
  const line = E.inOut(win(t, at + 0.5, 0.8));
  return (
    <g>
      <text x={cx} y={cy} textAnchor="middle" fontFamily={FONT.display} fontWeight={800} fontSize={104} letterSpacing={14}>
        {letters.map((ch, i) => {
          const u = E.outBack(win(t, at + i * 0.035, 0.5));
          return <tspan key={i} fill={P.ink} opacity={clamp(u)} dy={i === 0 ? 0 : 0}>{ch}</tspan>;
        })}
      </text>
      <rect x={cx - 420 * line} y={cy + 34} width={840 * line} height={4} fill={P.gold} />
      {tagline && <text x={cx} y={cy + 100} textAnchor="middle" fill={P.gold} fontFamily={FONT.body} fontWeight={600} fontSize={36} letterSpacing={2}
        opacity={E.out(win(t, at + 0.9, 0.6))}>{tagline}</text>}
    </g>
  );
};
