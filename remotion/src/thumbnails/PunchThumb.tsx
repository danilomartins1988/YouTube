import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Character} from '../presenter/Presenter';

/**
 * PunchThumb (v2 thumbnails): loud, high-contrast YouTube covers built to be clicked at phone size.
 * - Saturated two-tone sunburst background with halftone dots (no dark, moody gradients).
 * - ONE giant hero object drawn as a "sticker": thick black outline + white outer stroke + hard drop shadow.
 * - The channel's own cartoon presenter (no real people), huge, shocked, pointing at the hero.
 * - A red arrow and/or red circle on the detail that matters; a crossed-out "before" price where it fits.
 * - 2-4 words, enormous, white/yellow with a black stroke, slightly tilted; a red label for the punch word.
 * Canvas 1920x1080. No logos, no real brand designs, no photos.
 */
export type PunchText = {text: string; x: number; y: number; size: number; color?: string; rotate?: number; box?: string; anchor?: 'start' | 'middle' | 'end'};
export type PunchProps = {
  bg: [string, string];            // sunburst colors (center, edge)
  rays?: string;                   // ray color
  hero: {kind: string; x: number; y: number; s: number; rot?: number; [k: string]: any};
  presenter?: {x: number; y: number; s: number; face?: 1 | -1; point?: [number, number]};
  arrow?: {from: [number, number]; to: [number, number]; bend?: number; color?: string};
  circle?: {x: number; y: number; r: number; color?: string};
  crossed?: {text: string; x: number; y: number; size: number; rotate?: number};
  text: PunchText[];
  brand?: boolean;
};

const W = 1920, H = 1080, OL = '#0B0B0F', FONT = 'Inter Display, Inter, sans-serif';

/** sticker wrapper: white outer stroke + black outline + hard shadow, for any group of shapes */
const Sticker: React.FC<{children: React.ReactNode; shadow?: number}> = ({children, shadow = 18}) => <g>
  <g transform={`translate(${shadow} ${shadow})`} opacity={0.45} filter="url(#pblur)">{children}</g>
  <g filter="url(#pwhite)">{children}</g>
</g>;

/* ------------------------------------------------------------------------------------------------ heroes */
type HeroFn = (o: any) => React.ReactNode;
const HEROES: Record<string, HeroFn> = {
  /** a RAM stick, tilted, with black chips and gold pins; `flames` adds fire behind it */
  ram: (o) => <g>
    {o.flames && [0, 1, 2, 3, 4, 5].map((k) => <path key={k} d={`M ${-420 + k * 170} 40 Q ${-470 + k * 170} -170 ${-380 + k * 170} -330 Q ${-350 + k * 170} -200 ${-300 + k * 170} -260 Q ${-260 + k * 170} -120 ${-250 + k * 170} 40 Z`}
      fill={k % 2 ? '#FF6D00' : '#FFC400'} stroke={OL} strokeWidth={10} strokeLinejoin="round" />)}
    <rect x={-520} y={-150} width={1040} height={300} rx={18} fill="#1B7F3A" stroke={OL} strokeWidth={14} />
    {[0, 1, 2, 3, 4, 5, 6, 7].map((k) => <rect key={k} x={-480 + k * 122} y={-105} width={96} height={150} rx={8} fill="#15171C" stroke={OL} strokeWidth={8} />)}
    {Array.from({length: 30}, (_, k) => <rect key={'p' + k} x={-490 + k * 33} y={150} width={20} height={46} fill="#FFC21A" stroke={OL} strokeWidth={5} />)}
    <rect x={-40} y={140} width={40} height={60} fill="#1B7F3A" />
  </g>,
  /** a generic phone with a cracked screen showing a play icon; `money` adds banknotes flying out */
  phone: (o) => <g>
    {o.money && [[-430, -260, -25], [380, -330, 20], [-470, 120, 15], [420, 160, -18], [-250, -430, 10], [260, 380, -8]].map(([x, y, r], k) =>
      <g key={k} transform={`translate(${x} ${y}) rotate(${r})`}><rect x={-120} y={-58} width={240} height={116} rx={10} fill="#7BC67E" stroke={OL} strokeWidth={9} />
        <circle r={34} fill="#A5D6A7" stroke={OL} strokeWidth={6} /><text y={14} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={40} fill={OL}>$</text></g>)}
    <rect x={-210} y={-400} width={420} height={800} rx={60} fill="#22252C" stroke={OL} strokeWidth={16} />
    <rect x={-180} y={-350} width={360} height={700} rx={30} fill="#3B4252" />
    <path d="M -180 -120 L -40 -40 L -90 60 L 60 130 L 20 240 L 180 330" fill="none" stroke="#FFFFFF" strokeWidth={9} strokeLinejoin="round" />
    <path d="M -40 -40 L 120 -160 M 60 130 L 180 80 M -90 60 L -180 120" fill="none" stroke="#FFFFFF" strokeWidth={6} />
    <circle cx={0} cy={-200} r={70} fill="#FFC21A" stroke={OL} strokeWidth={10} /><path d="M -22 -235 L 34 -200 L -22 -165 Z" fill={OL} />
  </g>,
  /** a giant dollar bill with a thin slice cut off on the left (the farm's share) and scissors */
  dollar: (o) => <g>
    <rect x={-560} y={-250} width={1120} height={500} rx={24} fill="#8BCB8F" stroke={OL} strokeWidth={14} />
    <rect x={-520} y={-210} width={1040} height={420} rx={14} fill="none" stroke="#2E7D32" strokeWidth={8} />
    <circle cx={60} cy={0} r={150} fill="#C8E6C9" stroke={OL} strokeWidth={10} />
    <text x={60} y={62} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={190} fill="#1B5E20">$</text>
    <text x={-430} y={-120} fontFamily={FONT} fontWeight={900} fontSize={84} fill="#1B5E20">1</text>
    <text x={420} y={180} fontFamily={FONT} fontWeight={900} fontSize={84} fill="#1B5E20">1</text>
    <g transform={`translate(${o.sliceX ?? -760} 0) rotate(-8)`}>
      <rect x={-66} y={-250} width={132} height={500} rx={14} fill="#A5D6A7" stroke={OL} strokeWidth={14} />
      <path d="M -66 -170 L 66 -170 M -66 170 L 66 170" stroke="#2E7D32" strokeWidth={6} />
    </g>
    <path d="M -560 -280 L -560 280" stroke="#FFFFFF" strokeWidth={10} strokeDasharray="30 22" />
    <g transform="translate(-560 -330) rotate(80)"><circle cx={-60} cy={-40} r={38} fill="none" stroke={OL} strokeWidth={16} /><circle cx={-60} cy={40} r={38} fill="none" stroke={OL} strokeWidth={16} />
      <path d="M -28 -26 L 150 30 M -28 26 L 150 -30" stroke="#B0BEC5" strokeWidth={22} strokeLinecap="round" /><path d="M -28 -26 L 150 30 M -28 26 L 150 -30" stroke={OL} strokeWidth={4} fill="none" /></g>
  </g>,
};

/* ------------------------------------------------------------------------------------------------ parts */
const Sunburst: React.FC<{bg: [string, string]; rays?: string}> = ({bg, rays}) => <g>
  <defs><radialGradient id="psb" cx="58%" cy="48%" r="75%"><stop offset="0" stopColor={bg[0]} /><stop offset="1" stopColor={bg[1]} /></radialGradient>
    <pattern id="pdots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="3.2" fill="#000" opacity="0.12" /></pattern></defs>
  <rect width={W} height={H} fill="url(#psb)" />
  {Array.from({length: 24}, (_, k) => { const a0 = (k / 24) * Math.PI * 2, a1 = a0 + Math.PI / 24, cx = W * 0.58, cy = H * 0.48, R = 2400;
    return <path key={k} d={`M ${cx} ${cy} L ${cx + Math.cos(a0) * R} ${cy + Math.sin(a0) * R} L ${cx + Math.cos(a1) * R} ${cy + Math.sin(a1) * R} Z`} fill={rays || '#FFFFFF'} opacity={0.13} />; })}
  <rect width={W} height={H} fill="url(#pdots)" />
</g>;

const Arrow: React.FC<{a: NonNullable<PunchProps['arrow']>}> = ({a}) => {
  const [x0, y0] = a.from, [x1, y1] = a.to, b = a.bend ?? 0.25;
  const mx = (x0 + x1) / 2 - (y1 - y0) * b, my = (y0 + y1) / 2 + (x1 - x0) * b;
  const ang = Math.atan2(y1 - my, x1 - mx), L = 120;
  const h1 = [x1 - L * Math.cos(ang - 0.5), y1 - L * Math.sin(ang - 0.5)], h2 = [x1 - L * Math.cos(ang + 0.5), y1 - L * Math.sin(ang + 0.5)];
  const d = `M ${x0} ${y0} Q ${mx} ${my} ${x1 - 40 * Math.cos(ang)} ${y1 - 40 * Math.sin(ang)}`;
  const head = `M ${x1} ${y1} L ${h1[0]} ${h1[1]} L ${h2[0]} ${h2[1]} Z`;
  const c = a.color || '#FF1E1E';
  return <g>
    <path d={d} stroke="#FFFFFF" strokeWidth={62} fill="none" strokeLinecap="round" /><path d={head} fill="#FFFFFF" stroke="#FFFFFF" strokeWidth={26} strokeLinejoin="round" />
    <path d={d} stroke={OL} strokeWidth={44} fill="none" strokeLinecap="round" /><path d={head} fill={OL} stroke={OL} strokeWidth={10} strokeLinejoin="round" />
    <path d={d} stroke={c} strokeWidth={30} fill="none" strokeLinecap="round" /><path d={head} fill={c} />
  </g>;
};

const Words: React.FC<{t: PunchText}> = ({t}) => {
  const anchor = t.anchor || 'middle';
  return <g transform={`rotate(${t.rotate ?? -3} ${t.x} ${t.y})`}>
    {t.box && (() => { const w = t.text.length * t.size * 0.62 + 60, x = anchor === 'start' ? t.x - 30 : anchor === 'end' ? t.x - w + 30 : t.x - w / 2;
      return <rect x={x} y={t.y - t.size * 0.88} width={w} height={t.size * 1.12} rx={14} fill={t.box} stroke={OL} strokeWidth={10} />; })()}
    <text x={t.x + 10} y={t.y + 12} textAnchor={anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} fill={OL} letterSpacing={-2}>{t.text}</text>
    <text x={t.x} y={t.y} textAnchor={anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} fill={t.color || '#FFFFFF'} letterSpacing={-2}
      stroke={OL} strokeWidth={t.box ? 0 : Math.max(10, t.size * 0.09)} paintOrder="stroke" strokeLinejoin="round">{t.text}</text>
  </g>;
};

export const PunchThumb: React.FC<PunchProps> = (p) => {
  const Hero = HEROES[p.hero.kind];
  const pr = p.presenter;
  return (
    <AbsoluteFill style={{backgroundColor: p.bg[1]}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id="pblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" /><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
          <filter id="pwhite" x="-20%" y="-20%" width="140%" height="140%">
            <feMorphology in="SourceAlpha" operator="dilate" radius="12" result="d" /><feFlood floodColor="#FFFFFF" /><feComposite in2="d" operator="in" result="w" />
            <feMerge><feMergeNode in="w" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
        </defs>
        <Sunburst bg={p.bg} rays={p.rays} />
        {Hero && <Sticker><g transform={`translate(${p.hero.x} ${p.hero.y}) rotate(${p.hero.rot ?? 0}) scale(${p.hero.s})`}>{Hero(p.hero)}</g></Sticker>}
        {p.circle && <g><circle cx={p.circle.x} cy={p.circle.y} r={p.circle.r} fill="none" stroke="#FFFFFF" strokeWidth={34} />
          <circle cx={p.circle.x} cy={p.circle.y} r={p.circle.r} fill="none" stroke={p.circle.color || '#FF1E1E'} strokeWidth={18} /></g>}
        {pr && <Sticker shadow={14}><g transform={`translate(${pr.x} ${pr.y}) scale(${pr.s})`}>
          <Character pose={{x: 0, floor: 0, facing: pr.face ?? -1, walk: 0, moving: 0, hop: 0, drawHand: null,
            pointHand: pr.point ? [(pr.point[0] - pr.x) / pr.s, (pr.point[1] - pr.y) / pr.s] : null, talking: 1, blink: 0,
            surprise: 1, scale: 1, holdingMarker: false, smile: 0} as any} />
        </g></Sticker>}
        {p.arrow && <Arrow a={p.arrow} />}
        {p.crossed && <g transform={`rotate(${p.crossed.rotate ?? -6} ${p.crossed.x} ${p.crossed.y})`}>
          <text x={p.crossed.x} y={p.crossed.y} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={p.crossed.size} fill="#FFFFFF" stroke={OL}
            strokeWidth={p.crossed.size * 0.09} paintOrder="stroke">{p.crossed.text}</text>
          <path d={`M ${p.crossed.x - p.crossed.size * 1.4} ${p.crossed.y - p.crossed.size * 0.32} L ${p.crossed.x + p.crossed.size * 1.4} ${p.crossed.y - p.crossed.size * 0.32}`}
            stroke="#FF1E1E" strokeWidth={p.crossed.size * 0.14} strokeLinecap="round" />
        </g>}
        {p.text.map((t, i) => <Words key={i} t={t} />)}
        {p.brand !== false && <g transform="translate(1500 1046)"><rect width={8} height={30} y={-24} fill="#0B0B0F" />
          <text x={18} y={0} fontFamily="Inter, sans-serif" fontWeight={900} fontSize={22} letterSpacing={4} fill="#0B0B0F" opacity={0.75}>THE HIDDEN ECONOMICS</text></g>}
      </svg>
    </AbsoluteFill>
  );
};
