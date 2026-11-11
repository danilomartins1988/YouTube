import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Character} from '../presenter/Presenter';
import {SUBJECTS} from './CinematicThumb';

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
  /** palette for heroes borrowed from CinematicThumb SUBJECTS */
  pal?: {sky0: string; sky1: string; haze: string; key: string; accent: string; ink: string};
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
  /** a generic IV bag on a pole, almost empty, with a red low-level band and a drip */
  ivbag: (o) => <g>
    <path d="M 0 -560 L 0 520 M -140 -560 L 140 -560 M -160 520 L 160 520" stroke="#90A4AE" strokeWidth={22} strokeLinecap="round" />
    <path d="M 0 -560 L 0 -470" stroke="#B0BEC5" strokeWidth={10} />
    <rect x={-210} y={-470} width={420} height={560} rx={90} fill="#F5FBFF" stroke={OL} strokeWidth={16} />
    <clipPath id="ivpt"><rect x={-210} y={-470} width={420} height={560} rx={90} /></clipPath>
    <g clipPath="url(#ivpt)"><rect x={-210} y={-10} width={420} height={120} fill="#FF7A6B" /></g>
    <rect x={-210} y={-470} width={420} height={560} rx={90} fill="none" stroke={OL} strokeWidth={16} />
    {[0, 1, 2, 3, 4].map((k) => <path key={k} d={`M 120 ${-400 + k * 80} L 180 ${-400 + k * 80}`} stroke={OL} strokeWidth={8} />)}
    <text x={-20} y={-250} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={110} fill={OL}>IV</text>
    <path d="M -40 90 L 40 90 L 26 170 L -26 170 Z" fill="#E0E0E0" stroke={OL} strokeWidth={10} />
    <circle cx={0} cy={230} r={18} fill="#4FC3F7" stroke={OL} strokeWidth={6} />
    <path d="M 0 270 q 120 160 -60 300" fill="none" stroke="#B0BEC5" strokeWidth={12} />
  </g>,
  /** a giant YES/NO contract ticket with a coin flipping above it */
  yesnoticket: (o) => <g>
    <rect x={-470} y={-270} width={940} height={540} rx={40} fill="#FFFFFF" stroke={OL} strokeWidth={16} />
    <text x={0} y={-150} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={64} fill={OL}>WILL IT HAPPEN?</text>
    <rect x={-410} y={-70} width={480} height={190} rx={22} fill="#43A047" stroke={OL} strokeWidth={12} />
    <rect x={70} y={-70} width={340} height={190} rx={22} fill="#E53935" stroke={OL} strokeWidth={12} />
    <text x={-170} y={50} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={84} fill="#FFFFFF">YES 65¢</text>
    <text x={240} y={50} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={84} fill="#FFFFFF">NO 35¢</text>
    <rect x={-150} y={170} width={300} height={70} rx={14} fill="#FFC21A" stroke={OL} strokeWidth={10} />
    <text x={0} y={222} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={46} fill={OL}>FEE</text>
  </g>,
  /** a giant generic paper check */
  bigcheck: (o) => <g transform="rotate(-6)">
    <rect x={-560} y={-260} width={1120} height={520} rx={30} fill="#E8F5E9" stroke={OL} strokeWidth={16} />
    <text x={-500} y={-170} fontFamily={FONT} fontWeight={900} fontSize={54} fill="#2E7D32">DIVIDEND</text>
    <text x={-500} y={-20} fontFamily={FONT} fontWeight={800} fontSize={48} fill={OL}>PAY TO: EVERY RESIDENT</text>
    <rect x={120} y={60} width={380} height={130} rx={16} fill="#FFFFFF" stroke={OL} strokeWidth={12} />
    <text x={310} y={155} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill={OL}>{o.amount || '$1,200'}</text>
    <path d="M -500 120 L 60 120 M -500 200 L 60 200" stroke="#90A4AE" strokeWidth={8} />
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
  /** colourful cartoon skyscrapers; `spire` adds one very tall needle tower in the middle (Dubai) */
  towers: (o) => { const cols = ['#4FC3F7', '#FFB74D', '#81C784', '#BA68C8', '#FF8A65', '#90CAF9'];
    const b = [[-470, 300], [-330, 420], [-180, 340], [140, 380], [300, 460], [460, 330]];
    return <g>
      {o.spire && <g><path d="M -60 380 L -30 -420 L 0 -560 L 30 -420 L 60 380 Z" fill="#B3E5FC" stroke={OL} strokeWidth={12} strokeLinejoin="round" />
        {[-300, -180, -60, 60, 180, 300].map((y) => <path key={y} d={`M -40 ${y} L 40 ${y}`} stroke={OL} strokeWidth={6} />)}</g>}
      {b.map(([x, h], k) => <g key={k}><rect x={x - 70} y={380 - h} width={140} height={h} rx={8} fill={cols[k % 6]} stroke={OL} strokeWidth={12} />
        {Array.from({length: Math.floor(h / 70)}, (_, r) => [0, 1].map((c) => <rect key={r + '-' + c} x={x - 48 + c * 56} y={400 - h + r * 70} width={40} height={36} rx={4} fill="#FFF59D" stroke={OL} strokeWidth={5} />))}</g>)}
      <rect x={-560} y={370} width={1120} height={36} rx={10} fill="#5D4037" stroke={OL} strokeWidth={10} />
    </g>; },
  /** a giant chunky 3D arrow over a small bar chart: `dir` up (green) or down (red) */
  bigarrow: (o) => { const up = o.dir !== 'down', c = up ? '#2ECC40' : '#FF1E1E';
    const d = up ? 'M -480 300 L -160 20 L 20 160 L 300 -160 L 220 -240 L 500 -300 L 440 -20 L 360 -100 L 20 260 L -160 120 L -420 360 Z'
                 : 'M -480 -300 L -160 -20 L 20 -160 L 300 160 L 220 240 L 500 300 L 440 20 L 360 100 L 20 -260 L -160 -120 L -420 -360 Z';
    return <g>
      {[-420, -260, -100, 60, 220, 380].map((x, k) => { const h = up ? 80 + k * 50 : 330 - k * 50;
        return <rect key={k} x={x} y={380 - h} width={110} height={h} fill="#FFFFFF" stroke={OL} strokeWidth={10} opacity={0.9} />; })}
      <path d={d} fill={c} stroke={OL} strokeWidth={16} strokeLinejoin="round" transform="translate(14 14)" opacity={0.35} />
      <path d={d} fill={c} stroke={OL} strokeWidth={16} strokeLinejoin="round" />
      {o.label && <g transform={up ? 'translate(-330 -170)' : 'translate(-330 210)'}><circle r={92} fill="#FFFFFF" stroke={OL} strokeWidth={12} />
        <text y={34} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill={OL}>{o.label}</text></g>}
    </g>; },
  /** a laptop with a red skull on screen (generic ransomware) */
  hacked: (o) => <g>
    <path d="M -520 300 L 520 300 L 600 380 L -600 380 Z" fill="#B0BEC5" stroke={OL} strokeWidth={14} strokeLinejoin="round" />
    <rect x={-440} y={-330} width={880} height={620} rx={30} fill="#263238" stroke={OL} strokeWidth={16} />
    <rect x={-400} y={-290} width={800} height={540} rx={12} fill="#B71C1C" />
    <g transform="translate(0 -30)"><path d="M -150 -20 Q -150 -200 0 -200 Q 150 -200 150 -20 Q 150 60 90 80 L 90 140 L -90 140 L -90 80 Q -150 60 -150 -20 Z" fill="#FFFFFF" stroke={OL} strokeWidth={10} />
      <circle cx={-60} cy={-40} r={40} fill={OL} /><circle cx={60} cy={-40} r={40} fill={OL} /><path d="M 0 10 L -22 50 L 22 50 Z" fill={OL} />
      {[-50, 0, 50].map((x) => <rect key={x} x={x - 12} y={100} width={24} height={40} fill={OL} />)}</g>
    <text x={0} y={230} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={64} fill="#FFFFFF">LOCKED</text>
  </g>,
  /** a globe wrapped by thick glowing undersea cables */
  globecables: (o) => <g>
    <circle r={360} fill="#1E88E5" stroke={OL} strokeWidth={16} />
    <path d="M -250 -150 Q -150 -260 -20 -210 Q 60 -120 -60 -60 Q -180 -20 -250 -150 Z M 60 40 Q 200 -40 280 60 Q 260 200 140 240 Q 40 180 60 40 Z M -280 80 Q -200 60 -170 150 Q -210 230 -290 170 Z" fill="#66BB6A" stroke={OL} strokeWidth={10} />
    {[[-420, -60, 420, 120, -120], [-400, 160, 420, -200, 160], [-200, -400, 220, 400, 60]].map(([x0, y0, x1, y1, b], k) =>
      <g key={k}><path d={`M ${x0} ${y0} Q ${b} ${(y0 + y1) / 2 + b} ${x1} ${y1}`} fill="none" stroke={OL} strokeWidth={46} strokeLinecap="round" />
        <path d={`M ${x0} ${y0} Q ${b} ${(y0 + y1) / 2 + b} ${x1} ${y1}`} fill="none" stroke="#FFC21A" strokeWidth={28} strokeLinecap="round" /></g>)}
  </g>,
  /** a green tropical island with a giant chip on it */
  chipland: (o) => <g>
    <ellipse cx={0} cy={250} rx={560} ry={110} fill="#4FC3F7" stroke={OL} strokeWidth={12} />
    <path d="M -440 250 Q -400 60 -120 40 Q 200 20 420 110 Q 470 200 420 250 Z" fill="#81C784" stroke={OL} strokeWidth={14} strokeLinejoin="round" />
    <g transform="translate(0 -120) rotate(-6)"><rect x={-230} y={-230} width={460} height={460} rx={30} fill="#212121" stroke={OL} strokeWidth={14} />
      <rect x={-150} y={-150} width={300} height={300} rx={14} fill="#FFC21A" stroke={OL} strokeWidth={10} />
      {Array.from({length: 7}, (_, k) => <g key={k}><rect x={-200 + k * 60} y={-280} width={26} height={50} fill="#B0BEC5" stroke={OL} strokeWidth={5} />
        <rect x={-200 + k * 60} y={230} width={26} height={50} fill="#B0BEC5" stroke={OL} strokeWidth={5} /></g>)}</g>
  </g>,
  /** a chunky open-wheel race car (generic, no livery) */
  racer: (o) => <g>
    <path d="M -560 60 L -420 -20 L -120 -40 L -40 -120 L 140 -120 L 200 -40 L 480 -10 L 560 60 L 520 120 L -540 120 Z" fill={o.color || '#E53935'} stroke={OL} strokeWidth={16} strokeLinejoin="round" />
    <rect x={-620} y={-90} width={140} height={60} rx={10} fill={OL} /><rect x={500} y={-40} width={150} height={40} rx={10} fill={OL} />
    <path d="M -60 -120 Q 40 -200 140 -120" fill="#90CAF9" stroke={OL} strokeWidth={12} />
    <text x={20} y={60} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={96} fill="#FFFFFF" stroke={OL} strokeWidth={8} paintOrder="stroke">1</text>
    {[-380, 380].map((x) => <g key={x}><circle cx={x} cy={120} r={120} fill="#212121" stroke={OL} strokeWidth={14} /><circle cx={x} cy={120} r={48} fill="#9E9E9E" stroke={OL} strokeWidth={8} /></g>)}
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
  const pal = p.pal || {sky0: '#0A0E1A', sky1: '#1E2A4A', haze: '#FFFFFF', key: '#FFF3E0', accent: '#FFC21A', ink: '#FFFFFF'};
  const Hero = HEROES[p.hero.kind] || (SUBJECTS[p.hero.kind] ? ((o: any) => SUBJECTS[o.kind]({...o, x: 0, y: 0, s: 1}, pal)) : null);
  const pr = p.presenter;
  return (
    <AbsoluteFill style={{backgroundColor: p.bg[1]}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
          <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" /></filter>
          <linearGradient id="paperShade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.2} /><stop offset="1" stopColor="#000" stopOpacity={0.35} /></linearGradient>
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
            surprise: 1, scale: 1, holdingMarker: false, smile: 0, finger: true} as any} />
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
