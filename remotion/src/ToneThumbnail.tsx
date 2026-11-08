import React from 'react';
import {AbsoluteFill} from 'remotion';
import {CartoonStage} from './animation-engine/CartoonStage/CartoonStage';
import {CartoonOcean} from './animation-engine/CartoonOcean/CartoonOcean';

/**
 * Tone thumbnail: designed for the thumbnail, NOT a frame of the film. One dominant visual idea (a purpose-built
 * cartoon stage), the episode's tone (same grade as the film), 2-4 big words, and the channel mark that every
 * thumbnail shares. Rendered at 1920x1080, saved at 1280x720 (`remotion still --scale=0.6667`).
 */
export type ToneThumbProps = {
  tone: string;
  scene: Record<string, any>;            // CartoonStage params (zones/world/items...) or CartoonOcean params (ocean: true)
  at?: number;                           // time of the frozen frame
  headline: string[];                    // 1-2 lines, 2-4 words in total
  accent_line?: number;                  // which line takes the accent colour
  side?: 'left' | 'right';
};

const STYLE: Record<string, {ink: string; accent: string; stroke: string; shade: string; glow?: string; font: string}> = {
  thriller: {ink: '#F4EFE4', accent: '#FF4A3D', stroke: '#05080D', shade: '#05080D', font: 'Inter Display, Inter, sans-serif'},
  crisis: {ink: '#FFF4EC', accent: '#FFC21A', stroke: '#1A0507', shade: '#1A0507', font: 'Inter Display, Inter, sans-serif'},
  tech: {ink: '#FFFFFF', accent: '#3FD0FF', stroke: '#03122B', shade: '#03122B', glow: '#3FD0FF', font: 'Inter Display, Inter, sans-serif'},
  trade: {ink: '#FFFFFF', accent: '#FFC93C', stroke: '#0B2A4A', shade: '#0B2A4A', font: 'Inter Display, Inter, sans-serif'},
  strategy: {ink: '#14202E', accent: '#E08A00', stroke: '#FFFFFF', shade: '#E9EEF3', font: 'Inter Display, Inter, sans-serif'},
  history: {ink: '#2E2416', accent: '#A8322D', stroke: '#F7F0DE', shade: '#EFE4CC', font: 'Inter Display, Inter, sans-serif'},
  bright: {ink: '#FFFFFF', accent: '#FFC93C', stroke: '#10213A', shade: '#10213A', font: 'Inter Display, Inter, sans-serif'},
};

export const ToneThumbnail: React.FC<ToneThumbProps> = (p) => {
  const W = 1920, H = 1080, t = p.at ?? 3, st = STYLE[p.tone] || STYLE.bright;
  const left = (p.side || 'left') === 'left', x = left ? 96 : W - 96, anchor = left ? 'start' : 'end';
  const longest = Math.max(...p.headline.map((l) => l.length));
  const size = Math.min(210, (W * 0.56) / Math.max(4, longest) * 1.75);
  const Scene = p.scene.ocean ? CartoonOcean : CartoonStage;
  return (
    <AbsoluteFill style={{backgroundColor: st.shade}}>
      <AbsoluteFill><Scene t={t} W={W} H={H} {...(p.scene as any)} tone={p.tone} /></AbsoluteFill>
      <AbsoluteFill>
        <svg width={W} height={H}>
          <defs>
            <linearGradient id="tts" x1={left ? '0' : '1'} y1="0" x2={left ? '1' : '0'} y2="0">
              <stop offset="0%" stopColor={st.shade} stopOpacity={0.85} /><stop offset="48%" stopColor={st.shade} stopOpacity={0.35} />
              <stop offset="70%" stopColor={st.shade} stopOpacity={0} />
            </linearGradient>
            {st.glow && <filter id="ttg" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="14" result="b" />
              <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>}
          </defs>
          <rect width={W} height={H} fill="url(#tts)" />
          {p.headline.map((ln, i) => (
            <text key={i} x={x} y={H * 0.5 - (p.headline.length - 1) * size * 0.52 + i * size * 1.04 + size * 0.34} textAnchor={anchor}
              fontFamily={st.font} fontWeight={900} fontSize={size} letterSpacing={-2}
              fill={i === (p.accent_line ?? 1) ? st.accent : st.ink} stroke={st.stroke} strokeWidth={14} paintOrder="stroke" strokeLinejoin="round"
              filter={st.glow && i === (p.accent_line ?? 1) ? 'url(#ttg)' : undefined}>{ln}</text>
          ))}
          {/* channel mark: identical on every thumbnail (identity), small enough not to compete */}
          <g transform={`translate(${left ? 96 : W - 96 - 520} ${H - 104})`}>
            <rect width={520} height={56} rx={10} fill="#0B1424" opacity={0.88} />
            <rect width={10} height={56} rx={4} fill="#D4AF5A" />
            <text x={30} y={38} fontFamily="Inter, sans-serif" fontWeight={800} fontSize={28} letterSpacing={6} fill="#F4F1EA">THE HIDDEN ECONOMICS</text>
          </g>
        </svg>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
