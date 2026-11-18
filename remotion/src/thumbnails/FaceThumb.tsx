import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Bust, BustTraits, Expr} from '../animation-engine/CartoonStage/bust';
import {SUBJECTS} from './CinematicThumb';

/**
 * FaceThumb: the `face` thumbnail archetype (owner request 2026-11-16). Use it whenever a named public figure is central
 * to the episode (or, with the sitcom cast, when the episode has a recurring cartoon character).
 *
 * - One side: a high-detail cartoon BUST (remotion/src/animation-engine/CartoonStage/bust.tsx), head and shoulders
 *   filling ~50% of the frame height, anchored on the bottom edge, white sticker outline, rim light, big expression.
 * - Other side: 0-4 huge words (exact layout computed in Python, hiddeneco/youtube_thumbnail.py `layout_face`), the
 *   accent line in a red box, plus ONE bold prop (gold price tag, pie, chip, black sale tag, giant number or any
 *   CinematicThumb subject).
 * - Background: the channel's v2 sunburst (two saturated tones, rays, halftone) with a glow behind the head and a
 *   dark edge vignette for contrast.
 * Canvas 1920x1080. No logos, no photos, no photo-traced likeness (see docs/PRODUCTION_STANDARD.md "Real people").
 */
export type FaceText = {text: string; x: number; y: number; size: number; width: number; color: string; anchor: 'start' | 'middle' | 'end';
  box?: string; rotate?: number};
export type FaceProps = {
  bg: [string, string];
  rays?: string;
  bust: {who: string | BustTraits; traits?: BustTraits; expr: Expr; x: number; y?: number; s: number; dir?: 1 | -1; point?: [number, number];
    look?: [number, number]; rim?: string};
  prop?: {kind: string; x: number; y: number; s: number; rot?: number; text?: string; pct?: number; color?: string; [k: string]: any};
  text: FaceText[];
  hideText?: boolean;
  brand?: 'none' | 'bl' | 'br';
};

const W = 1920, H = 1080, OL = '#0B0B0F', FONT = 'Inter Display, Inter, sans-serif';

const Sticker: React.FC<{children: React.ReactNode; shadow?: number; white?: boolean}> = ({children, shadow = 18, white = true}) => <g>
  <g transform={`translate(${shadow} ${shadow})`} opacity={0.5} filter="url(#fblur)">{children}</g>
  <g filter={white ? 'url(#fwhite)' : undefined}>{children}</g>
</g>;

const fitSize = (txt: string, w: number, cap: number) => Math.min(cap, w / (Math.max(1, txt.length) * 0.62));

/* ------------------------------------------------------------------------------------------------ props */
const PROPS: Record<string, (o: any) => React.ReactNode> = {
  /** a giant electric plug drawn like an oil barrel (Ep 67), cable curling off, sparks; optional o.text on the barrel band */
  plug: (o) => { const t = String(o.text ?? ''), fs = fitSize(t, 380, 120);
    return <g>
      <path d="M -260 260 Q -520 300 -560 80" fill="none" stroke={OL} strokeWidth={34} strokeLinecap="round" />
      <rect x={-260} y={-300} width={520} height={600} rx={70} fill="#2F3B52" stroke={OL} strokeWidth={18} />
      <rect x={-260} y={-120} width={520} height={90} fill="#F5B700" stroke={OL} strokeWidth={12} />
      <rect x={-260} y={60} width={520} height={40} fill="#4A5874" stroke={OL} strokeWidth={10} />
      <path d="M -120 -300 L -120 -470 M 120 -300 L 120 -470" stroke="#D7DEE8" strokeWidth={60} strokeLinecap="round" />
      {[[-330, -420, 1], [330, -440, -1], [0, -560, 1]].map(([x, y, f], k) => <path key={k} transform={`translate(${x} ${y}) scale(${f} 1)`} d="M 10 -60 L -26 6 L -2 6 L -14 60 L 28 -10 L 4 -10 Z" fill="#FFD23F" stroke={OL} strokeWidth={8} strokeLinejoin="round" />)}
      {t && <text x={0} y={-75 + fs * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fs} fill={OL}>{t}</text>}
    </g>; },
  /** a gold price tag on a string with a big label (e.g. a sourced figure) */
  tag: (o) => { const t = String(o.text ?? ''), fs = fitSize(t, 600, 230);
    return <g>
      <defs><linearGradient id="ftag" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFF0A8" /><stop offset="0.5" stopColor="#FFC928" /><stop offset="1" stopColor="#D99A00" /></linearGradient></defs>
      <path d="M -420 -10 Q -560 -220 -420 -330" fill="none" stroke="#FFFFFF" strokeWidth={14} strokeLinecap="round" />
      <path d="M -470 0 L -330 -170 L 330 -170 Q 370 -170 370 -130 L 370 130 Q 370 170 330 170 L -330 170 Z" fill="url(#ftag)" stroke={OL} strokeWidth={16} strokeLinejoin="round" />
      <path d="M -420 0 L -308 -134 L 326 -134 L 326 134 L -308 134 Z" fill="none" stroke="#B07A00" strokeWidth={6} strokeDasharray="18 12" />
      <circle cx={-360} cy={0} r={34} fill="#FFFFFF" stroke={OL} strokeWidth={12} />
      <path d="M -250 -150 Q 60 -175 340 -150" stroke="#FFFFFF" strokeWidth={12} opacity={0.55} fill="none" strokeLinecap="round" />
      <text x={30} y={fs * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fs} fill={OL} letterSpacing={-4}>{t}</text>
    </g>; },
  /** a pie with one slice pulled out (o.pct %), label on the slice; `mid` (deg, 180 = left) turns the slice towards the bust */
  pie: (o) => { const pct = Math.max(1, Math.min(99, o.pct ?? 44)), sw = (pct / 100) * Math.PI * 2, R = 300;
    const a0 = o.mid !== undefined ? (o.mid * Math.PI) / 180 - sw / 2 : -Math.PI / 2, a1 = a0 + sw;
    const mid = (a0 + a1) / 2, ox = Math.cos(mid) * 40, oy = Math.sin(mid) * 40, big = pct > 50 ? 1 : 0;
    const slice = `M ${ox} ${oy} L ${ox + Math.cos(a0) * R} ${oy + Math.sin(a0) * R} A ${R} ${R} 0 ${big} 1 ${ox + Math.cos(a1) * R} ${oy + Math.sin(a1) * R} Z`;
    const rest = `M 0 0 L ${Math.cos(a1) * R} ${Math.sin(a1) * R} A ${R} ${R} 0 ${1 - big} 1 ${Math.cos(a0) * R} ${Math.sin(a0) * R} Z`;
    const t = String(o.text ?? `${pct}%`), fs = fitSize(t, 300, 170);
    return <g>
      <path d={rest} fill="#E8EDF5" stroke={OL} strokeWidth={16} strokeLinejoin="round" />
      {[0.25, 0.5, 0.75].map((k) => { const a = a1 + (Math.PI * 2 - (a1 - a0)) * k; return <path key={k} d={`M 0 0 L ${Math.cos(a) * R} ${Math.sin(a) * R}`} stroke="#AAB4C3" strokeWidth={6} />; })}
      <path d={slice} fill={o.color || '#FFC928'} stroke={OL} strokeWidth={16} strokeLinejoin="round" />
      <text x={ox + Math.cos(mid) * R * 0.5 + 10} y={oy + Math.sin(mid) * R * 0.5 + fs * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fs}
        fill="#FFFFFF" stroke={OL} strokeWidth={fs * 0.1} paintOrder="stroke" strokeLinejoin="round" letterSpacing={-3}>{t}</text>
    </g>; },
  /** a generic chip (no brand), gold die, pins; optional label */
  chip: (o) => <g>
    <defs><linearGradient id="fchip" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#3A3F4A" /><stop offset="1" stopColor="#12141A" /></linearGradient>
      <linearGradient id="fdie" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFF0A8" /><stop offset="1" stopColor="#D99A00" /></linearGradient></defs>
    {Array.from({length: 8}, (_, k) => [-1, 1].map((s) => <g key={k + '' + s}>
      <rect x={-250 + k * 66} y={s < 0 ? -360 : 280} width={34} height={80} rx={8} fill="#C9CED6" stroke={OL} strokeWidth={8} />
      <rect x={s < 0 ? -360 : 280} y={-250 + k * 66} width={80} height={34} rx={8} fill="#C9CED6" stroke={OL} strokeWidth={8} /></g>))}
    <rect x={-300} y={-300} width={600} height={600} rx={44} fill="url(#fchip)" stroke={OL} strokeWidth={16} />
    <rect x={-190} y={-190} width={380} height={380} rx={24} fill="url(#fdie)" stroke={OL} strokeWidth={12} />
    {[-120, -40, 40, 120].map((v) => <g key={v}><path d={`M ${v} -170 L ${v} 170`} stroke="#B07A00" strokeWidth={6} opacity={0.6} /><path d={`M -170 ${v} L 170 ${v}`} stroke="#B07A00" strokeWidth={6} opacity={0.6} /></g>)}
    <path d="M -270 -240 Q -100 -290 180 -270" stroke="#FFFFFF" strokeWidth={12} opacity={0.3} fill="none" strokeLinecap="round" />
    {o.text && <text x={0} y={fitSize(o.text, 320, 160) * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fitSize(o.text, 320, 160)} fill={OL}>{o.text}</text>}
  </g>,
  /** a black sale tag with a gold rim and a big % (Black Friday), slashed "was" bar */
  saletag: (o) => <g>
    <defs><linearGradient id="fsg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFE08A" /><stop offset="0.5" stopColor="#B8860B" /><stop offset="1" stopColor="#FFE08A" /></linearGradient></defs>
    <path d="M -470 -40 Q -640 -330 -400 -500" fill="none" stroke="#FFFFFF" strokeWidth={14} strokeLinecap="round" />
    <path d="M -520 0 L -300 -300 L 480 -300 L 480 300 L -300 300 Z" fill="url(#fsg)" stroke={OL} strokeWidth={16} strokeLinejoin="round" />
    <path d="M -470 0 L -280 -255 L 435 -255 L 435 255 L -280 255 Z" fill="#111317" stroke={OL} strokeWidth={8} strokeLinejoin="round" />
    <circle cx={-330} cy={0} r={52} fill="#FFFFFF" stroke="url(#fsg)" strokeWidth={16} />
    {o.text ? <text x={90} y={fitSize(o.text, 600, 300) * 0.36 + 30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fitSize(o.text, 600, 300)} fill="#FFD23F">{o.text}</text>
      : <g transform="translate(110 30)"><circle cx={-120} cy={-110} r={70} fill="none" stroke="#FFD23F" strokeWidth={34} />
        <circle cx={130} cy={120} r={70} fill="none" stroke="#FFD23F" strokeWidth={34} /><path d="M 150 -180 L -140 190" stroke="#FFD23F" strokeWidth={40} strokeLinecap="round" /></g>}
    <rect x={-200} y={-215} width={560} height={30} rx={15} fill="#9AA3B5" opacity={0.6} /><path d="M -220 -170 L 380 -235" stroke="#FF2D2D" strokeWidth={18} strokeLinecap="round" />
  </g>,
  /** a giant number/word, white with black stroke and a yellow drop */
  number: (o) => { const t = String(o.text ?? ''), fs = fitSize(t, 900, 330);
    return <g><text x={14} y={fs * 0.36 + 16} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fs} fill={OL} letterSpacing={-6}>{t}</text>
      <text x={0} y={fs * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={fs} fill={o.color || '#FFE14D'} stroke={OL} strokeWidth={fs * 0.08}
        paintOrder="stroke" strokeLinejoin="round" letterSpacing={-6}>{t}</text></g>; },
};

/* ------------------------------------------------------------------------------------------------ text */
const Line: React.FC<{t: FaceText}> = ({t}) => {
  const left = t.anchor === 'start' ? t.x : t.anchor === 'end' ? t.x - t.width : t.x - t.width / 2;
  const sw = Math.max(10, t.size * 0.1);
  return <g transform={`rotate(${t.rotate ?? -3} ${t.x} ${t.y})`}>
    {t.box && <g><rect x={left - 34 + 12} y={t.y - t.size * 0.86 + 14} width={t.width + 68} height={t.size * 1.08} rx={16} fill={OL} />
      <rect x={left - 34} y={t.y - t.size * 0.86} width={t.width + 68} height={t.size * 1.08} rx={16} fill={t.box} stroke={OL} strokeWidth={10} /></g>}
    {!t.box && <text x={t.x + 10} y={t.y + 12} textAnchor={t.anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} textLength={t.width}
      lengthAdjust="spacingAndGlyphs" fill={OL} stroke={OL} strokeWidth={sw} strokeLinejoin="round">{t.text}</text>}
    <text x={t.x} y={t.y} textAnchor={t.anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} textLength={t.width} lengthAdjust="spacingAndGlyphs"
      fill={t.color} stroke={t.box ? 'none' : OL} strokeWidth={t.box ? 0 : sw} paintOrder="stroke" strokeLinejoin="round">{t.text}</text>
  </g>;
};

export const FaceThumb: React.FC<FaceProps> = (p) => {
  const b = p.bust, by = b.y ?? H + 10, dir = b.dir ?? (b.x < W / 2 ? 1 : -1);
  const headX = b.x, headY = by - 736 * b.s;
  const pr = p.prop;
  const pal = {sky0: '#0A0E1A', sky1: '#1E2A4A', haze: '#FFFFFF', key: '#FFF3E0', accent: '#FFD23F', ink: '#FFFFFF'};
  const propNode = pr ? (PROPS[pr.kind] ? <g transform={`translate(${pr.x} ${pr.y}) rotate(${pr.rot ?? 0}) scale(${pr.s})`}>{PROPS[pr.kind](pr)}</g>
    : SUBJECTS[pr.kind] ? SUBJECTS[pr.kind](pr, pal) : null) : null;
  const pt = b.point ? [(b.point[0] - b.x) / b.s, (b.point[1] - by) / b.s] as [number, number] : undefined;
  const cx = headX, cy = headY;
  return (
    <AbsoluteFill style={{backgroundColor: p.bg[1]}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <radialGradient id="fsb" cx={cx / W} cy={cy / H} r="0.95"><stop offset="0" stopColor={p.bg[0]} /><stop offset="1" stopColor={p.bg[1]} /></radialGradient>
          <radialGradient id="fhalo" cx="50%" cy="50%" r="50%"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.75} /><stop offset="0.55" stopColor="#FFFFFF" stopOpacity={0.18} /><stop offset="1" stopColor="#FFFFFF" stopOpacity={0} /></radialGradient>
          <radialGradient id="fvig" cx="50%" cy="50%" r="75%"><stop offset="0.6" stopColor="#000" stopOpacity={0} /><stop offset="1" stopColor="#000" stopOpacity={0.5} /></radialGradient>
          <pattern id="fdots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="3.2" fill="#000" opacity="0.13" /></pattern>
          <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" /></filter>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
          <linearGradient id="paperShade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.2} /><stop offset="1" stopColor="#000" stopOpacity={0.35} /></linearGradient>
          <filter id="fblur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7" /><feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" /></filter>
          <filter id="fwhite" x="-20%" y="-20%" width="140%" height="140%">
            <feMorphology in="SourceAlpha" operator="dilate" radius="11" result="d" /><feFlood floodColor="#FFFFFF" /><feComposite in2="d" operator="in" result="w" />
            <feMerge><feMergeNode in="w" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
        </defs>
        <rect width={W} height={H} fill="url(#fsb)" />
        {Array.from({length: 28}, (_, k) => { const a0 = (k / 28) * Math.PI * 2, a1 = a0 + Math.PI / 28, R = 2600;
          return <path key={k} d={`M ${cx} ${cy} L ${cx + Math.cos(a0) * R} ${cy + Math.sin(a0) * R} L ${cx + Math.cos(a1) * R} ${cy + Math.sin(a1) * R} Z`} fill={p.rays || '#FFFFFF'} opacity={0.14} />; })}
        <rect width={W} height={H} fill="url(#fdots)" />
        <rect width={W} height={H} fill="url(#fvig)" />
        <ellipse cx={cx} cy={cy + 60 * b.s} rx={620 * b.s} ry={620 * b.s} fill="url(#fhalo)" />
        {propNode && <Sticker>{propNode}</Sticker>}
        <Sticker shadow={20}><g transform={`translate(${b.x} ${by}) scale(${b.s})`}>
          <Bust who={b.who} traits={b.traits} expr={b.expr} dir={dir} point={pt} look={b.look} rim={b.rim || p.bg[0]} id="fb" outline={10} />
        </g></Sticker>
        {!p.hideText && p.text.map((t, i) => <Line key={i} t={t} />)}
        {p.brand && p.brand !== 'none' && <g transform={`translate(${p.brand === 'bl' ? 40 : 1500} 1046)`}><rect width={8} height={30} y={-24} fill="#FFFFFF" />
          <text x={18} y={0} fontFamily="Inter, sans-serif" fontWeight={900} fontSize={22} letterSpacing={4} fill="#FFFFFF" opacity={0.85}>THE HIDDEN ECONOMICS</text></g>}
      </svg>
    </AbsoluteFill>
  );
};
