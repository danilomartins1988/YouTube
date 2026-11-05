import React from 'react';
import {AbsoluteFill} from 'remotion';
import {eo, rand, useCtx} from '../lib/anim';

/** Navy gradient with slow-drifting particles and a faint grid: never a dead static background. */
export const Background: React.FC<{grid?: boolean; particles?: number}> = ({grid = true, particles = 40}) => {
  const {t, W, H, pal} = useCtx();
  const dots = Array.from({length: particles}, (_, i) => {
    const x = (rand(i) * W + t * (6 + rand(i + 7) * 14)) % W;
    const y = (rand(i + 3) * H + Math.sin(t * 0.3 + i) * 12 + H) % H;
    const r = 1 + rand(i + 11) * 1.8;
    const o = 0.08 + rand(i + 5) * 0.18;
    return <circle key={i} cx={x} cy={y} r={r} fill={pal.accent} opacity={o} />;
  });
  const gx = (t * 8) % 80;
  return (
    <AbsoluteFill>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <defs>
          <radialGradient id="bgv" cx="50%" cy="45%" r="75%">
            <stop offset="0%" stopColor={pal.bg2} />
            <stop offset="100%" stopColor={pal.bg} />
          </radialGradient>
        </defs>
        <rect width={W} height={H} fill="url(#bgv)" />
        {grid &&
          Array.from({length: Math.ceil(W / 80) + 2}, (_, i) => (
            <line key={'v' + i} x1={i * 80 - gx} y1={0} x2={i * 80 - gx} y2={H} stroke={pal.border} strokeOpacity={0.12} />
          ))}
        {grid &&
          Array.from({length: Math.ceil(H / 80) + 1}, (_, i) => (
            <line key={'h' + i} x1={0} y1={i * 80} x2={W} y2={i * 80} stroke={pal.border} strokeOpacity={0.1} />
          ))}
        {dots}
      </svg>
    </AbsoluteFill>
  );
};

/** Chapter tag, channel mark and on-screen source credits. */
export const Chrome: React.FC = () => {
  const {t, W, H, pal, font, scene} = useCtx();
  const a = eo(t, 0.15, 0.5);
  const chapter = scene.params.chapter ?? scene.chapter;
  const credits = scene.credits.filter(Boolean);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {chapter && !scene.params.no_chrome ? (
          <g opacity={a}>
            <rect x={120} y={92} width={36 * a} height={4} fill={pal.accent} />
            <text x={172} y={100} fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={22} letterSpacing={3}>
              {String(chapter).toUpperCase()}
            </text>
          </g>
        ) : null}
        <text x={W - 120} y={100} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={18} letterSpacing={4} opacity={0.8 * a}>
          THE HIDDEN ECONOMICS
        </text>
        {credits.length ? (
          <text x={120} y={H - 60} fill={pal.muted} fontFamily={font.body} fontSize={20} opacity={0.9 * a}>
            {'Source: ' + credits.join('  ·  ')}
          </text>
        ) : null}
      </svg>
    </AbsoluteFill>
  );
};

/** Subtle film grain + vignette for a filmic finish (deterministic per frame). */
export const Finish: React.FC = () => {
  const {W, H, frame} = useCtx();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <defs>
          <filter id="grain">
            <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed={frame % 7} />
            <feColorMatrix type="saturate" values="0" />
          </filter>
          <radialGradient id="vig" cx="50%" cy="50%" r="70%">
            <stop offset="60%" stopColor="#000" stopOpacity={0} />
            <stop offset="100%" stopColor="#000" stopOpacity={0.45} />
          </radialGradient>
        </defs>
        <rect width={W} height={H} filter="url(#grain)" opacity={0.035} />
        <rect width={W} height={H} fill="url(#vig)" />
      </svg>
    </AbsoluteFill>
  );
};

/** Text helper with fade/rise entrance. */
export const RiseText: React.FC<{
  x: number; y: number; at: number; size: number; color?: string; weight?: number; anchor?: 'start' | 'middle' | 'end';
  display?: boolean; children: React.ReactNode; dur?: number; tracking?: number; opacity?: number;
}> = ({x, y, at, size, color, weight = 400, anchor = 'start', display = false, children, dur = 0.5, tracking = 0, opacity = 1}) => {
  const {t, pal, font} = useCtx();
  const u = eo(t, at, dur);
  return (
    <text x={x} y={y + 24 * (1 - u)} opacity={u * opacity} textAnchor={anchor} fill={color || pal.ink}
      fontFamily={display ? font.display : font.body} fontWeight={weight} fontSize={size} letterSpacing={tracking}>
      {children}
    </text>
  );
};
