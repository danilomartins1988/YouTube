import React from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import {Animal} from './Animal';
import {Scenery} from './Scenery';
import {FONT, K, loadKidsFonts, RAINBOW} from './theme';

/* 1280x720 thumbnail: huge rounded title, numbers 1-2-3, four big happy animals. Readable at phone size. */
export const KidsThumb: React.FC = () => {
  loadKidsFonts();
  const {width: W, height: H} = useVideoConfig();
  const title = 'VAMOS CONTAR!';
  return (
    <AbsoluteFill style={{backgroundColor: K.sky2}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <g transform={`scale(${W / 1920})`}>
          <Scenery t={1.3} beat={0.536} w={1920} h={1080} />
          <Animal kind="duck" x={330} y={700} scale={1.25} mouth={0.8} look={0.4} tilt={-6} />
          <Animal kind="cow" x={760} y={730} scale={1.1} mouth={0.3} look={0.2} tilt={4} />
          <Animal kind="pig" x={1170} y={730} scale={1.1} mouth={0.6} look={-0.2} tilt={-4} />
          <Animal kind="frog" x={1590} y={700} scale={1.25} mouth={0.7} look={-0.4} tilt={6} />
          {['1', '2', '3'].map((n, i) => (
            <g key={n} transform={`translate(${1400 + i * 150} ${360 + (i % 2) * -40}) rotate(${(i - 1) * 10})`}>
              <circle r={78} fill={[K.coral, K.blue, K.green][i]} stroke={K.ink} strokeWidth={9} />
              <text y={40} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={120} fill="#fff" stroke={K.ink} strokeWidth={8} paintOrder="stroke">{n}</text>
            </g>
          ))}
        </g>
      </svg>
      <div style={{position: 'absolute', left: 40, top: 26, fontFamily: FONT, fontWeight: 700, fontSize: 132, lineHeight: 1,
        transform: 'rotate(-3deg)'}}>
        {title.split('').map((ch, i) => (
          <span key={i} style={{color: ch === ' ' ? 'transparent' : RAINBOW[i % RAINBOW.length], WebkitTextStroke: `11px ${K.ink}`,
            paintOrder: 'stroke fill', textShadow: '0 8px 0 rgba(43,35,80,0.3)'}}>{ch === ' ' ? ' ' : ch}</span>
        ))}
      </div>
      <div style={{position: 'absolute', left: 60, top: 172, fontFamily: FONT, fontWeight: 700, fontSize: 64, color: '#fff',
        WebkitTextStroke: `8px ${K.ink}`, paintOrder: 'stroke fill', transform: 'rotate(-3deg)'}}>
        os bichinhos de 1 a 10
      </div>
    </AbsoluteFill>
  );
};
