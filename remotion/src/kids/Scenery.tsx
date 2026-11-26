import React from 'react';
import {K, hop} from './theme';

/* Sunny meadow: gradient sky, smiling sun, drifting clouds, layered hills and flowers that sway on the beat.
 * Calm, slow background motion (the characters carry the energy); no flashing. */

const Cloud: React.FC<{x: number; y: number; s: number}> = ({x, y, s}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} opacity={0.95}>
    <ellipse cx={0} cy={20} rx={120} ry={40} fill="#fff" />
    <circle cx={-50} cy={0} r={48} fill="#fff" />
    <circle cx={20} cy={-20} r={62} fill="#fff" />
    <circle cx={80} cy={10} r={40} fill="#fff" />
  </g>
);

const Flower: React.FC<{x: number; y: number; c: string; sway: number; s?: number}> = ({x, y, c, sway, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s}) rotate(${sway})`}>
    <path d="M 0 0 L 0 -60" stroke="#3FA535" strokeWidth={7} strokeLinecap="round" />
    <ellipse cx={14} cy={-26} rx={14} ry={7} fill="#56C23F" transform="rotate(-30 14 -26)" />
    {[0, 72, 144, 216, 288].map((a) => (
      <ellipse key={a} cx={0} cy={-80} rx={13} ry={20} fill={c} transform={`rotate(${a} 0 -62)`} />
    ))}
    <circle cx={0} cy={-62} r={12} fill={K.yellow} stroke="#E8A400" strokeWidth={3} />
  </g>
);

export const Scenery: React.FC<{t: number; beat: number; w: number; h: number; sun?: boolean}> = ({t, beat, w, h, sun = true}) => {
  const portrait = h > w;
  const horizon = portrait ? h * 0.47 : h * 0.66;
  const sway = Math.sin((t / beat) * Math.PI) * 6;
  const flowers = Array.from({length: portrait ? 7 : 11}, (_, i) => i);
  const cols = [K.pink, K.coral, K.purple, K.orange, K.blue];
  return (
    <g>
      <defs>
        <linearGradient id="kidsSky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={K.sky1} />
          <stop offset="1" stopColor={K.sky2} />
        </linearGradient>
      </defs>
      <rect width={w} height={h} fill="url(#kidsSky)" />
      {sun && (
        <g transform={`translate(${portrait ? w - 170 : w - 220} ${portrait ? 230 : 170})`}>
          <g transform={`rotate(${t * 12})`}>
            {Array.from({length: 12}, (_, i) => (
              <path key={i} d="M -14 -112 L 0 -150 L 14 -112 Z" fill={K.yellow} transform={`rotate(${i * 30})`} />
            ))}
          </g>
          <circle r={100} fill={K.sun} stroke="#F2B400" strokeWidth={6} />
          <circle cx={-32} cy={-14} r={10} fill={K.ink} />
          <circle cx={32} cy={-14} r={10} fill={K.ink} />
          <ellipse cx={-56} cy={22} rx={16} ry={10} fill={K.sunCheek} opacity={0.7} />
          <ellipse cx={56} cy={22} rx={16} ry={10} fill={K.sunCheek} opacity={0.7} />
          <path d="M -34 22 Q 0 58 34 22" fill="none" stroke={K.ink} strokeWidth={7} strokeLinecap="round" />
        </g>
      )}
      <Cloud x={((t * 22 + 200) % (w + 500)) - 250} y={portrait ? 360 : 150} s={0.9} />
      <Cloud x={((t * 15 + 900) % (w + 500)) - 250} y={portrait ? 560 : 300} s={0.6} />
      <Cloud x={((t * 18 + 1500) % (w + 500)) - 250} y={portrait ? 160 : 90} s={0.7} />
      {/* hills */}
      <path d={`M 0 ${horizon} Q ${w * 0.25} ${horizon - 120} ${w * 0.5} ${horizon - 20} T ${w} ${horizon - 60} L ${w} ${h} L 0 ${h} Z`} fill={K.hill1} />
      <path d={`M 0 ${horizon + 80} Q ${w * 0.3} ${horizon - 10} ${w * 0.62} ${horizon + 70} T ${w} ${horizon + 40} L ${w} ${h} L 0 ${h} Z`} fill={K.hill2} />
      <rect x={0} y={horizon + 150} width={w} height={h - horizon - 150} fill={K.hill3} />
      <path d={`M 0 ${horizon + 150} Q ${w * 0.5} ${horizon + 110} ${w} ${horizon + 150}`} fill={K.hill3} />
      {flowers.map((i) => (
        <Flower key={i} x={(i + 0.5) * (w / flowers.length) + ((i * 37) % 40) - 20} y={horizon + 60 + ((i * 53) % 60)}
          c={cols[i % cols.length]} sway={sway * (i % 2 ? 1 : -1) - 4 * hop(t, beat, i * 0.25)} s={0.8 + (i % 3) * 0.12} />
      ))}
    </g>
  );
};
