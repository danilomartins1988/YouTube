import React from 'react';
import {FONT, K, Line} from './theme';
import {clamp} from '../animation-engine/motion';

/* Karaoke lyric bar: the current line in a rounded card; each word fills with colour as it is sung
 * (left-to-right sweep over the word's [s, e] window) and pops slightly. */
export const Karaoke: React.FC<{line?: Line; next?: Line; t: number; portrait: boolean; w: number; h: number}> = ({line, next, t, portrait, w, h}) => {
  if (!line) return null;
  const appear = clamp((t - (line.start - 0.25)) / 0.25);
  const leave = next ? clamp((next.start - 0.25 - t) / 0.2) : clamp((line.end + 1.2 - t) / 0.4);
  const o = Math.min(appear, leave);
  if (o <= 0) return null;
  const size = portrait ? 66 : 74;
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: portrait ? h * 0.775 : h * 0.835, display: 'flex',
      justifyContent: 'center', opacity: o, transform: `translateY(${(1 - appear) * 20}px)`}}>
      <div style={{background: 'rgba(255,255,255,0.93)', borderRadius: 48, padding: portrait ? '22px 34px' : '16px 46px',
        boxShadow: '0 10px 0 rgba(43,35,80,0.18)', border: `6px solid ${K.ink}`, maxWidth: portrait ? w - 90 : w - 200,
        display: 'flex', flexWrap: 'wrap', justifyContent: 'center', columnGap: size * 0.32, rowGap: 4}}>
        {line.words.map((wd, i) => {
          const u = clamp((t - wd.s) / Math.max(0.12, wd.e - wd.s));
          const active = t >= wd.s && t <= wd.e + 0.12;
          const pct = Math.round(u * 100);
          return (
            <span key={i} style={{fontFamily: FONT, fontWeight: 700, fontSize: size, lineHeight: 1.18, display: 'inline-block',
              transform: `scale(${active ? 1.1 : 1}) translateY(${active ? -4 : 0}px)`,
              backgroundImage: `linear-gradient(90deg, ${K.pink} 0%, ${K.pink} ${pct}%, ${K.ink} ${pct}%, ${K.ink} 100%)`,
              WebkitBackgroundClip: 'text', backgroundClip: 'text', color: 'transparent'}}>
              {wd.w}
            </span>
          );
        })}
      </div>
    </div>
  );
};
