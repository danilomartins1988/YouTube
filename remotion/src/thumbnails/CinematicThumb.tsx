import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Character} from '../presenter/Presenter';

/**
 * CinematicThumb: a YouTube thumbnail designed as a documentary cover, NOT a frame of the film and NOT the cartoon
 * look. Original vector illustration with cinematic lighting (volumetric beams, haze, rim light, glow, particles,
 * vignette, film grain), one dominant SUBJECT built for the story, and typography composited on top from an exact
 * layout computed in Python (tools/thumbnails.py), so text never clips and QC knows every text box.
 *
 * Canvas 1920x1080 (rendered with --scale=2 for a 3840x2160 master). No logos, no real flag designs, no likeness of
 * real people, no photographs: subjects are generic, story-specific objects.
 */
export type ThumbText = {text: string; x: number; y: number; size: number; width: number; color: string; anchor: 'start' | 'middle' | 'end';
  box?: string; boxPad?: number; underline?: string; rotate?: number};
export type CinematicProps = {
  palette: {sky0: string; sky1: string; haze: string; key: string; accent: string; ink: string};
  backdrop: 'room' | 'sky' | 'sea' | 'deep' | 'desert' | 'alps' | 'track' | 'cleanroom' | 'void';
  subject: {kind: string; x: number; y: number; s: number; [k: string]: any};
  support?: {kind: string; x: number; y: number; s: number; [k: string]: any}[];
  beams?: {x: number; y: number; angle: number; width: number; length: number; opacity?: number; color?: string}[];
  particles?: {n: number; color?: string; region?: [number, number, number, number]; size?: number};
  text: ThumbText[];
  hideText?: boolean;
  brand?: 'tl' | 'tr' | 'bl' | 'none';
  /** layout archetype: classic | bignum | split | presenter (see docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md) */
  archetype?: string;
  /** split archetype: subject drawn on the right half (the left uses `subject`) */
  after?: {kind: string; x: number; y: number; s: number; [k: string]: any};
  /** presenter archetype: the channel's own character, surprised, pointing at the subject */
  presenter?: {x: number; y: number; s: number; face?: 1 | -1};
  grain?: number; vignette?: number;
};

const W = 1920, H = 1080;
const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const FONT = 'Inter Display, Inter, sans-serif';

/* ------------------------------------------------------------------------------------------------ backdrops */
const Backdrop: React.FC<{p: CinematicProps}> = ({p}) => {
  const P = p.palette;
  const horizon = p.backdrop === 'sea' ? 700 : p.backdrop === 'desert' ? 780 : p.backdrop === 'alps' ? 760 : p.backdrop === 'track' ? 760 : 1080;
  return <g>
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={P.sky0} /><stop offset="1" stopColor={P.sky1} /></linearGradient>
      <radialGradient id="hz" cx="62%" cy="55%" r="65%"><stop offset="0" stopColor={P.haze} stopOpacity={0.55} /><stop offset="1" stopColor={P.haze} stopOpacity={0} /></radialGradient>
      <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={P.haze} stopOpacity={0.55} /><stop offset="0.08" stopColor={P.sky1} /><stop offset="1" stopColor="#02060C" /></linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#bg)" />
    <rect width={W} height={H} fill="url(#hz)" />
    {p.backdrop === 'sea' && <g>
      <rect y={horizon} width={W} height={H - horizon} fill="url(#sea)" />
      {Array.from({length: 26}, (_, k) => <path key={k} d={`M ${-100 + rnd(k) * 2100} ${horizon + 18 + k * k * 0.55} q 60 -6 120 0`} stroke={P.haze} strokeOpacity={0.25 - k * 0.006} strokeWidth={2 + k * 0.12} fill="none" />)}
    </g>}
    {p.backdrop === 'desert' && <g>
      <path d={`M 0 ${horizon} Q 480 ${horizon - 40} 960 ${horizon - 10} T 1920 ${horizon - 30} L 1920 1080 L 0 1080 Z`} fill="#2A1A0E" />
      <path d={`M 0 ${horizon + 60} Q 600 ${horizon + 10} 1200 ${horizon + 70} T 1920 ${horizon + 40} L 1920 1080 L 0 1080 Z`} fill="#1A0F08" />
    </g>}
    {p.backdrop === 'alps' && <g>
      <path d="M 0 760 L 220 520 L 360 640 L 560 380 L 760 600 L 900 470 L 1120 690 L 1300 430 L 1520 650 L 1700 500 L 1920 700 L 1920 1080 L 0 1080 Z" fill="#1C2A3E" />
      <path d="M 560 380 L 620 450 L 590 445 L 560 470 L 530 440 L 500 450 Z M 1300 430 L 1360 500 L 1330 495 L 1300 515 L 1270 490 L 1240 500 Z" fill="#DCE6F2" opacity={0.85} />
      <path d="M 0 860 L 300 760 L 640 840 L 980 740 L 1300 850 L 1620 770 L 1920 840 L 1920 1080 L 0 1080 Z" fill="#0E1726" />
    </g>}
    {p.backdrop === 'track' && <g>
      <path d={`M 0 ${horizon} L 1920 ${horizon - 40} L 1920 1080 L 0 1080 Z`} fill="#141820" />
      {Array.from({length: 9}, (_, k) => <path key={k} d={`M ${k * 260 - 100} 1080 L ${960 + (k - 4) * 40} ${horizon - 20}`} stroke="#FFFFFF" strokeOpacity={0.05} strokeWidth={3} />)}
      <path d={`M 0 ${horizon + 40} L 1920 ${horizon}`} stroke="#E53935" strokeWidth={10} strokeDasharray="60 60" opacity={0.6} />
    </g>}
    {p.backdrop === 'room' && <g>
      <path d="M 0 840 L 1920 840 L 1920 1080 L 0 1080 Z" fill="#000" opacity={0.45} />
      {Array.from({length: 12}, (_, k) => <rect key={k} x={k * 170 - 20} y={0} width={4} height={840} fill={P.haze} opacity={0.05} />)}
    </g>}
    {p.backdrop === 'cleanroom' && <g>
      {Array.from({length: 7}, (_, k) => <rect key={k} x={140 + k * 260} y={20} width={200} height={14} rx={7} fill="#E8F6FF" opacity={0.65} />)}
      <path d="M 0 860 L 1920 860 L 1920 1080 L 0 1080 Z" fill="#050B18" opacity={0.7} />
      {Array.from({length: 22}, (_, k) => <path key={k} d={`M ${k * 96} 860 L ${960 + (k - 11) * 160} 1080`} stroke={P.haze} strokeOpacity={0.12} strokeWidth={2} />)}
    </g>}
    {p.backdrop === 'deep' && <g>
      {Array.from({length: 8}, (_, k) => <path key={k} d={`M ${200 + k * 230} 0 L ${120 + k * 260} 1080`} stroke={P.haze} strokeOpacity={0.05} strokeWidth={60} />)}
      <path d="M 0 900 Q 500 860 960 900 T 1920 880 L 1920 1080 L 0 1080 Z" fill="#03070C" />
    </g>}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ helpers */
const Beam: React.FC<{b: NonNullable<CinematicProps['beams']>[number]; i: number; color: string}> = ({b, i, color}) => {
  const a = (b.angle * Math.PI) / 180, ex = b.x + Math.sin(a) * b.length, ey = b.y + Math.cos(a) * b.length;
  const nx = Math.cos(a) * b.width / 2, ny = -Math.sin(a) * b.width / 2;
  return <g>
    <defs><linearGradient id={`bm${i}`} x1={b.x} y1={b.y} x2={ex} y2={ey} gradientUnits="userSpaceOnUse">
      <stop offset="0" stopColor={b.color || color} stopOpacity={b.opacity ?? 0.5} /><stop offset="1" stopColor={b.color || color} stopOpacity={0} /></linearGradient></defs>
    <path d={`M ${b.x - nx * 0.12} ${b.y - ny * 0.12} L ${b.x + nx * 0.12} ${b.y + ny * 0.12} L ${ex + nx} ${ey + ny} L ${ex - nx} ${ey - ny} Z`} fill={`url(#bm${i})`} filter="url(#soft)" />
  </g>;
};
const Particles: React.FC<{p: NonNullable<CinematicProps['particles']>; color: string}> = ({p, color}) => {
  const [x0, y0, x1, y1] = p.region || [0, 0, W, H];
  return <g>{Array.from({length: p.n}, (_, k) => { const r = (p.size ?? 3) * (0.4 + rnd(k + 9) * 1.2);
    return <circle key={k} cx={x0 + rnd(k) * (x1 - x0)} cy={y0 + rnd(k + 3) * (y1 - y0)} r={r} fill={p.color || color} opacity={0.25 + 0.6 * rnd(k + 5)} filter={r > 3 ? 'url(#soft)' : undefined} />; })}</g>;
};
const metal = (id: string, a: string, b: string) => <linearGradient id={id} x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={a} /><stop offset="0.5" stopColor={b} /><stop offset="1" stopColor={a} /></linearGradient>;

/* ------------------------------------------------------------------------------------------------ subjects */
type SubjectFn = (o: any, P: CinematicProps['palette']) => React.ReactNode;
const SUBJECTS: Record<string, SubjectFn> = {
  /** A massive open vault door; the chamber behind is empty; bills dissolving into dust. */
  vault: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('vm', '#5A6270', '#A9B3C2')}<radialGradient id="vin" cx="50%" cy="45%" r="60%"><stop offset="0" stopColor={P.key} stopOpacity={0.55} /><stop offset="1" stopColor="#05070B" /></radialGradient></defs>
    <circle r={360} fill="#07090D" stroke="url(#vm)" strokeWidth={46} />
    <circle r={330} fill="url(#vin)" />
    {[-120, 0, 120].map((y) => <rect key={y} x={-260} y={y} width={520} height={10} fill="#2A3140" />)}
    <g transform="translate(330 0) skewY(-12) scale(0.42 1)">
      <circle r={350} fill="url(#vm)" stroke="#1A1E26" strokeWidth={12} />
      {Array.from({length: 12}, (_, k) => <circle key={k} cx={Math.cos(k * 0.5236) * 300} cy={Math.sin(k * 0.5236) * 300} r={16} fill="#2C323D" />)}
      <circle r={110} fill="#2C323D" /><path d="M -90 0 L 90 0 M 0 -90 L 0 90" stroke="#C9D2DE" strokeWidth={20} strokeLinecap="round" />
    </g>
    {o.empty !== false && <text x={0} y={30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={110} fill={P.accent} opacity={0.9} filter="url(#glow)">{o.mark || '?'}</text>}
    {Array.from({length: o.bills ?? 9}, (_, k) => { const u = rnd(k + 2), x = -420 - u * 260 + k * 18, y = -260 + rnd(k + 7) * 420;
      return <g key={k} transform={`translate(${x} ${y}) rotate(${-30 + rnd(k) * 60})`} opacity={0.85 - u * 0.6}>
        <rect x={-70} y={-32} width={140} height={64} rx={6} fill="#3E6B48" stroke="#9FD3A8" strokeWidth={3} />
        <circle r={18} fill="none" stroke="#9FD3A8" strokeWidth={3} /></g>; })}
  </g>,
  /** A ledger / bank confirmation with one line redacted and a magnifier over it. */
  ledger: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -6})`}>
    <rect x={-330} y={-430} width={660} height={860} rx={10} fill="#E9E3D4" />
    <rect x={-330} y={-430} width={660} height={860} rx={10} fill="url(#paperShade)" />
    <text x={-280} y={-340} fontFamily={FONT} fontWeight={900} fontSize={44} fill="#1B1F27">{o.heading || 'BANK CONFIRMATION'}</text>
    {Array.from({length: 11}, (_, k) => <rect key={k} x={-280} y={-280 + k * 56} width={480 - rnd(k) * 200} height={14} rx={7} fill="#1B1F27" opacity={0.18} />)}
    <rect x={-290} y={20} width={580} height={86} fill="#0B0D12" />
    <text x={0} y={80} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={56} fill={P.accent}>{o.amount || '$ 2,000,000,000'}</text>
    {o.stamp && <g transform="translate(120 280) rotate(-14)"><rect x={-190} y={-60} width={380} height={120} rx={12} fill="none" stroke="#D3302B" strokeWidth={12} />
      <text x={0} y={30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={84} fill="#D3302B">{o.stamp}</text></g>}
    {o.magnifier !== false && <g transform="translate(150 60)"><circle r={150} fill={P.key} fillOpacity={0.12} stroke="#C9D2DE" strokeWidth={22} />
      <rect x={100} y={100} width={46} height={230} rx={20} transform="rotate(-45)" fill="#2C323D" /></g>}
  </g>,
  /** A colossal EUV lithography machine with a glowing light-source core and a laser line. */
  euv: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('em', '#C8D3E0', '#F4F8FC')}<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stopColor="#FFFFFF" /><stop offset="0.25" stopColor={P.accent} /><stop offset="1" stopColor={P.accent} stopOpacity={0} /></radialGradient></defs>
    <rect x={-560} y={-300} width={1120} height={600} rx={28} fill="url(#em)" />
    <rect x={-560} y={-300} width={1120} height={600} rx={28} fill="#0A1426" opacity={0.38} />
    <rect x={-560} y={-300} width={1120} height={70} rx={20} fill={P.key} opacity={0.85} />
    {[-380, -130, 120, 370].map((x, k) => <g key={k}><rect x={x - 100} y={-200} width={200} height={380} rx={12} fill="#0B1730" opacity={0.85} />
      <rect x={x - 80} y={-180} width={160} height={8} rx={4} fill={P.accent} opacity={0.6} /></g>)}
    <rect x={-240} y={-170} width={480} height={330} rx={20} fill="#030814" />
    <circle cx={0} cy={0} r={150} fill="url(#core)" filter="url(#glow)" />
    <path d="M -560 -40 L -40 -10" stroke="#FF4D6D" strokeWidth={10} filter="url(#glow)" />
    {Array.from({length: 6}, (_, k) => <circle key={k} cx={-20 + k * 2} cy={-140 + k * 26} r={7} fill="#FFFFFF" />)}
    <path d="M -160 120 Q 0 40 160 120" stroke="#E6F7FF" strokeWidth={10} fill="none" />
    <rect x={-600} y={300} width={1200} height={30} rx={10} fill="#05090F" opacity={0.8} />
  </g>,
  /** A container ship seen from a low bow angle, flying three blank flags (no real designs). */
  ship: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs><linearGradient id="hull" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2B3A55" /><stop offset="1" stopColor="#0B111C" /></linearGradient></defs>
    <path d="M -700 0 L 520 -60 L 640 40 L 560 220 L -640 260 Z" fill="url(#hull)" />
    <path d="M 520 -60 L 640 40 L 560 220 Z" fill="#000" opacity={0.35} />
    {Array.from({length: 7}, (_, c) => Array.from({length: 5}, (_, r) => { const x = -620 + c * 160, y = -40 - r * 70 + c * -6;
      return <rect key={c + '-' + r} x={x} y={y - 64} width={150} height={64} fill={['#B5452F', '#2F6E9E', '#C79A2A', '#3E7D55', '#6D4C8E', '#9E3D52'][(c * 5 + r) % 6]} stroke="#0B111C" strokeWidth={4} opacity={0.92} />; }))}
    <rect x={420} y={-330} width={110} height={270} fill="#E7ECF2" /><rect x={430} y={-310} width={90} height={16} fill="#0B111C" opacity={0.6} />
    {(o.flags || ['?', '?', '?']).map((f: string, k: number) => { const x = -560 + k * 360, y = -470 - k * 30, c = ['#C8CED8', '#B9C1CD', '#D3D8E0'][k];
      return <g key={k}><rect x={x} y={y} width={10} height={260} fill="#0B111C" />
        <path d={`M ${x + 10} ${y} q 90 -20 180 10 q 40 14 60 0 l 0 110 q -20 14 -60 0 q -90 -30 -180 -10 Z`} fill={c} stroke="#0B111C" strokeWidth={4} />
        <text x={x + 130} y={y + 82} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={76} fill="#0B111C">{f}</text></g>; })}
    <path d="M -700 260 Q 0 300 640 230" stroke="#FFFFFF" strokeOpacity={0.35} strokeWidth={10} fill="none" />
  </g>,
  /** An offshore oil platform at dusk, gas flare burning. */
  oilrig: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    {[-300, -120, 120, 300].map((x) => <path key={x} d={`M ${x} 0 L ${x * 0.8} 420`} stroke="#0A0F17" strokeWidth={34} />)}
    <path d="M -300 120 L 300 260 M 300 120 L -300 260 M -260 300 L 260 300" stroke="#0A0F17" strokeWidth={12} />
    <rect x={-380} y={-60} width={760} height={80} fill="#0A0F17" />
    <rect x={-340} y={-200} width={300} height={140} fill="#0E1520" /><rect x={20} y={-170} width={240} height={110} fill="#0E1520" />
    <path d="M 160 -170 L 210 -560 L 260 -170 Z" fill="none" stroke="#0A0F17" strokeWidth={14} />
    {Array.from({length: 8}, (_, k) => <path key={k} d={`M ${160 + k * 6} ${-170 - k * 48} L ${260 - k * 6} ${-170 - k * 48}`} stroke="#0A0F17" strokeWidth={8} />)}
    <path d="M -360 -200 L -560 -420 L -540 -430 L -340 -210 Z" fill="#0A0F17" />
    <ellipse cx={-575} cy={-470} rx={45} ry={90} fill="#FFB347" filter="url(#glow)" /><ellipse cx={-575} cy={-460} rx={22} ry={50} fill="#FFF3C4" />
    {Array.from({length: 10}, (_, k) => <rect key={k} x={-320 + k * 64} y={-30} width={22} height={12} fill={P.accent} opacity={0.9} />)}
    <rect x={-600} y={420} width={1200} height={14} fill={P.accent} opacity={0.25} filter="url(#soft)" />
  </g>,
  /** A rising stock line that shoots up through the frame, a generic car silhouette riding it. */
  surge: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    {Array.from({length: 7}, (_, k) => <path key={k} d={`M -700 ${-k * 110 + 300} L 700 ${-k * 110 + 300}`} stroke={P.haze} strokeOpacity={0.12} strokeWidth={2} />)}
    <path d="M -700 300 L -500 280 L -320 300 L -150 270 L 0 290 L 120 250 L 220 -40 L 300 -520" stroke={P.accent} strokeWidth={20} fill="none" strokeLinejoin="round" filter="url(#glow)" />
    <path d="M -700 300 L -500 280 L -320 300 L -150 270 L 0 290 L 120 250 L 220 -40 L 300 -520 L 300 420 L -700 420 Z" fill={P.accent} opacity={0.12} />
    <path d="M 300 -520 l -60 40 m 60 -40 l 20 70" stroke={P.accent} strokeWidth={20} strokeLinecap="round" filter="url(#glow)" />
    <g transform="translate(-120 230) rotate(-6) scale(1.2)">
      <path d="M -190 0 L -170 -50 Q -120 -110 -30 -112 L 60 -112 Q 130 -100 170 -50 L 200 -40 Q 220 -20 210 10 L -200 10 Z" fill="#0B0F16" />
      <path d="M -110 -60 Q -70 -98 -20 -100 L 40 -100 Q 90 -92 120 -60 Z" fill={P.key} opacity={0.35} />
      <circle cx={-110} cy={14} r={38} fill="#05070A" stroke="#3A4250" strokeWidth={8} /><circle cx={120} cy={14} r={38} fill="#05070A" stroke="#3A4250" strokeWidth={8} />
    </g>
    {o.label && <text x={340} y={-560} fontFamily={FONT} fontWeight={900} fontSize={64} fill={P.accent}>{o.label}</text>}
  </g>,
  /** A thick glowing arrow that BREAKS OUT of a chart frame (glass shards), a car silhouette launched on it. */
  breakout: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs><linearGradient id="arw" x1="0" y1="1" x2="0.4" y2="0"><stop offset="0" stopColor={P.accent} stopOpacity={0.35} /><stop offset="0.6" stopColor={P.accent} /><stop offset="1" stopColor="#FFFFFF" /></linearGradient>
      <radialGradient id="burst" cx="50%" cy="50%" r="50%"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.95} /><stop offset="0.25" stopColor={P.accent} stopOpacity={0.6} /><stop offset="1" stopColor={P.accent} stopOpacity={0} /></radialGradient></defs>
    <rect x={-560} y={-300} width={980} height={620} rx={16} fill="#06090F" stroke="#3A4558" strokeWidth={10} />
    {Array.from({length: 5}, (_, k) => <path key={k} d={`M -540 ${-200 + k * 110} L 400 ${-200 + k * 110}`} stroke="#1E2838" strokeWidth={3} />)}
    <path d="M -540 250 L -400 236 L -260 252 L -120 228 L 0 240 L 80 210" stroke={P.accent} strokeWidth={14} fill="none" opacity={0.7} />
    <circle cx={330} cy={-430} r={330} fill="url(#burst)" />
    <path d="M 40 240 L 240 -120 L 330 -480" stroke="url(#arw)" strokeWidth={110} fill="none" strokeLinecap="round" strokeLinejoin="round" filter="url(#glow)" />
    <path d="M 330 -480 L 200 -400 M 330 -480 L 380 -330" stroke="#FFFFFF" strokeWidth={60} strokeLinecap="round" />
    <path d="M 330 -480 L 220 -390 L 330 -620 L 450 -380 Z" fill="#FFFFFF" />
    {Array.from({length: 16}, (_, k) => { const a = -1.9 + rnd(k) * 1.6, r = 140 + rnd(k + 3) * 300, x = 250 + Math.cos(a) * r, y = -300 + Math.sin(a) * r;
      return <path key={k} d={`M ${x} ${y} l ${18 + rnd(k + 1) * 40} ${-10 - rnd(k + 2) * 30} l ${-8} ${30 + rnd(k) * 20} Z`} fill="#E8F4FF" opacity={0.85} transform={`rotate(${rnd(k + 5) * 90} ${x} ${y})`} />; })}
    {o.car !== false && <g transform="translate(150 -40) rotate(-62) scale(1.15)">
      <path d="M -190 0 L -170 -50 Q -120 -110 -30 -112 L 60 -112 Q 130 -100 170 -50 L 200 -40 Q 220 -20 210 10 L -200 10 Z" fill="#05070A" stroke={P.accent} strokeWidth={6} />
      <circle cx={-110} cy={14} r={38} fill="#05070A" stroke="#C8D2E0" strokeWidth={8} /><circle cx={120} cy={14} r={38} fill="#05070A" stroke="#C8D2E0" strokeWidth={8} />
    </g>}
  </g>,
  /** A giant glowing number used AS the subject (e.g. #1), with a crown-like glow. */
  bignum: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -4})`}>
    <defs><linearGradient id="bng" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#FFF4C2" /><stop offset="0.5" stopColor={P.accent} /><stop offset="1" stopColor="#8A5A00" /></linearGradient></defs>
    <circle r={420} fill={P.accent} opacity={0.18} filter="url(#soft)" />
    {Array.from({length: 18}, (_, k) => <path key={k} d={`M 0 0 L ${Math.cos(k * 0.349) * 900} ${Math.sin(k * 0.349) * 900}`} stroke={P.accent} strokeOpacity={0.12} strokeWidth={60} />)}
    <text x={0} y={190} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={o.size ?? 560} fill="url(#bng)" stroke="#2A1A00" strokeWidth={18} paintOrder="stroke" filter="url(#glow)">{o.label || '#1'}</text>
  </g>,
  /** A generic compact hatchback, side view, rim-lit (no real model's design, no badge). */
  hatch: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s * (o.flip ? -1 : 1)} ${o.s})`}>
    <defs><linearGradient id="hb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={o.body || '#C9D2DE'} /><stop offset="1" stopColor="#3A4250" /></linearGradient></defs>
    <ellipse cx={0} cy={118} rx={420} ry={26} fill="#000" opacity={0.6} />
    <path d="M -400 80 L -390 20 Q -380 -10 -330 -20 L -170 -40 L -60 -150 Q -30 -170 20 -170 L 210 -170 Q 260 -168 290 -120 L 360 -30 Q 400 -20 405 20 L 410 80 Q 410 96 390 96 L -385 96 Q -402 96 -400 80 Z" fill="url(#hb)" stroke={P.key} strokeWidth={5} />
    <path d="M -40 -140 L 40 -150 L 40 -50 L -150 -40 Z M 70 -152 L 200 -152 Q 240 -150 262 -112 L 300 -48 L 70 -48 Z" fill="#0B1220" opacity={0.92} />
    <path d="M -380 0 L 400 -10" stroke={P.key} strokeWidth={4} opacity={0.6} />
    {[-250, 250].map((x) => <g key={x}><circle cx={x} cy={90} r={70} fill="#05070A" stroke="#2C323D" strokeWidth={12} /><circle cx={x} cy={90} r={30} fill="#9AA6B8" /></g>)}
    <path d="M 380 0 l 26 4 l -4 22 l -28 -6 Z" fill="#FFE7A0" filter="url(#glow)" />
  </g>,
  /** A memory stick (generic, no brand) shot at an angle: glossy PCB, eight chips, gold contacts; chips glow when hot. */
  ramchip: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -12})`}>
    <defs><linearGradient id="pcb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#2F8A55" /><stop offset="1" stopColor="#14462B" /></linearGradient>
      <linearGradient id="chipg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#3A414D" /><stop offset="0.5" stopColor="#14171D" /><stop offset="1" stopColor="#05070A" /></linearGradient>
      <linearGradient id="gold2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#FFE7A0" /><stop offset="1" stopColor="#B07C12" /></linearGradient></defs>
    <rect x={-560} y={-170} width={1120} height={340} rx={22} fill="#000" opacity={0.5} transform="translate(20 40)" filter="url(#soft)" />
    <rect x={-560} y={-170} width={1120} height={340} rx={22} fill="url(#pcb)" stroke={P.key} strokeWidth={4} />
    {Array.from({length: 30}, (_, k) => <path key={k} d={`M ${-540 + k * 36} -150 l 0 ${40 + (k % 3) * 12}`} stroke="#7BD389" strokeWidth={3} opacity={0.35} />)}
    {Array.from({length: 46}, (_, k) => <rect key={'g' + k} x={-540 + k * 23.5} y={136} width={14} height={40} fill="url(#gold2)" />)}
    {Array.from({length: 8}, (_, k) => { const cx = -465 + k * 133, hot = o.hot !== false;
      return <g key={k}>
        {hot && <rect x={cx - 64} y={-104} width={128} height={168} rx={14} fill={P.accent} opacity={0.35 + 0.25 * ((k * 7) % 3) / 2} filter="url(#glow)" />}
        <rect x={cx - 52} y={-92} width={104} height={144} rx={8} fill="url(#chipg)" stroke={hot ? P.accent : '#4A5260'} strokeWidth={hot ? 5 : 3} />
        <rect x={cx - 40} y={-80} width={80} height={10} rx={4} fill="#FFFFFF" opacity={0.18} /></g>; })}
    <rect x={-90} y={-160} width={180} height={44} rx={8} fill="#E9EDF3" /><text x={0} y={-128} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={30} fill="#14171D">16 GB</text>
  </g>,
  /** Nanoimprint: a glowing quartz stamp about to press onto a patterned wafer, UV light leaking from the gap. */
  stamp: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? 0})`}>
    <defs><radialGradient id="wafr" cx="0.45" cy="0.4" r="0.7"><stop offset="0" stopColor="#B9C7E8" /><stop offset="0.45" stopColor="#5B6E99" /><stop offset="1" stopColor="#1A2440" /></radialGradient>
      <linearGradient id="quartz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#F2FBFF" stopOpacity="0.95" /><stop offset="1" stopColor="#8FD3FF" stopOpacity="0.75" /></linearGradient></defs>
    <ellipse cx={0} cy={250} rx={560} ry={150} fill="#000" opacity={0.55} filter="url(#soft)" />
    <ellipse cx={0} cy={210} rx={540} ry={140} fill="url(#wafr)" stroke={P.key} strokeWidth={4} />
    {Array.from({length: 9}, (_, r) => Array.from({length: 13}, (_, c) => { const x = -480 + c * 80, y = 120 + r * 22, dx = x / 540, dy = (y - 210) / 140;
      if (dx * dx + dy * dy > 0.82) return null; const hot = Math.abs(x) < 170 && Math.abs(y - 210) < 50;
      return <rect key={r * 20 + c} x={x - 30} y={y - 8} width={60} height={14} rx={2} fill={hot ? P.accent : '#2A3657'} opacity={hot ? 0.95 : 0.8} stroke="#0A0F1E" strokeWidth={1.5} />; }))}
    <ellipse cx={0} cy={205} rx={260} ry={46} fill={P.haze} opacity={0.55} filter="url(#glow)" />
    {Array.from({length: 7}, (_, k) => <path key={'r' + k} d={`M ${-200 + k * 66} 40 L ${-240 + k * 80} 190`} stroke="#E6B3FF" strokeWidth={6} opacity={0.55} filter="url(#glow)" />)}
    <path d="M 0 -520 L 0 -150" stroke="#9FB2C8" strokeWidth={46} />
    <rect x={-60} y={-520} width={120} height={60} rx={10} fill="#5E6E84" />
    <path d="M -250 -150 L 250 -150 L 220 20 L -220 20 Z" fill="url(#quartz)" stroke="#FFFFFF" strokeWidth={5} filter="url(#glow)" />
    <path d="M -230 -120 L 230 -120" stroke="#FFFFFF" strokeWidth={4} opacity={0.7} />
    {Array.from({length: 11}, (_, k) => <path key={'t' + k} d={`M ${-190 + k * 38} 20 L ${-190 + k * 38} 44`} stroke="#DFF4FF" strokeWidth={9} />)}
  </g>,
  /** An amber bottle of photoresist, glowing from inside, with an optional padlock and chain (strategic material). */
  flask: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -6})`}>
    <defs><linearGradient id="amber" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFD180" /><stop offset="0.5" stopColor="#FF8F00" /><stop offset="1" stopColor="#6D3A00" /></linearGradient>
      <linearGradient id="glass" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#FFFFFF" stopOpacity="0.35" /><stop offset="0.25" stopColor="#FFFFFF" stopOpacity="0.05" /><stop offset="1" stopColor="#FFFFFF" stopOpacity="0" /></linearGradient></defs>
    <ellipse cx={0} cy={330} rx={300} ry={50} fill="#000" opacity={0.55} filter="url(#soft)" />
    <ellipse cx={0} cy={60} rx={260} ry={330} fill={P.accent} opacity={0.3} filter="url(#glow)" />
    <rect x={-70} y={-380} width={140} height={90} rx={14} fill="#263238" stroke={P.key} strokeWidth={3} />
    <path d="M -190 -250 Q -190 -300 -120 -300 L 120 -300 Q 190 -300 190 -250 L 190 290 Q 190 320 160 320 L -160 320 Q -190 320 -190 290 Z" fill="url(#amber)" stroke={P.key} strokeWidth={5} />
    <path d="M -190 -250 Q -190 -300 -120 -300 L 120 -300 Q 190 -300 190 -250 L 190 290 Q 190 320 160 320 L -160 320 Q -190 320 -190 290 Z" fill="url(#glass)" />
    <rect x={-140} y={-80} width={280} height={150} rx={12} fill="#FFFFFF" opacity={0.92} />
    <text x={0} y={-12} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={52} fill="#1B1F27">{o.label ?? 'RESIST'}</text>
    <text x={0} y={42} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={28} fill="#78909C">{o.sub ?? 'EUV'}</text>
    {o.hot !== false && <g transform="translate(110 140) rotate(8)">
      <path d="M -260 -60 L 120 60 M -260 60 L 120 -60" stroke="#B0BEC5" strokeWidth={22} strokeDasharray="34 12" />
      <rect x={-70} y={-30} width={140} height={120} rx={16} fill="#FFC21A" stroke="#1B1F27" strokeWidth={6} />
      <path d="M -42 -30 L -42 -72 Q 0 -128 42 -72 L 42 -30" fill="none" stroke="#1B1F27" strokeWidth={14} />
      <circle cx={0} cy={26} r={14} fill="#1B1F27" /></g>}
  </g>,
  /** A crashing line (consequence) */
  crash: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    {Array.from({length: 7}, (_, k) => <path key={k} d={`M -700 ${-k * 110 + 300} L 700 ${-k * 110 + 300}`} stroke={P.haze} strokeOpacity={0.12} strokeWidth={2} />)}
    <path d="M -700 200 L -520 120 L -360 40 L -220 -60 L -100 -200 L 0 -320 L 80 -380 L 160 120 L 300 300 L 700 360" stroke={P.accent} strokeWidth={20} fill="none" strokeLinejoin="round" filter="url(#glow)" />
    <path d="M 80 -380 L 160 120 L 300 300 L 700 360 L 700 420 L 80 420 Z" fill={P.accent} opacity={0.14} />
  </g>,
  /** A low-angle open-wheel race car (generic) with light streaks. */
  racecar: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    {Array.from({length: 9}, (_, k) => <path key={k} d={`M ${-900 - k * 40} ${-120 + k * 30} L ${-240} ${-120 + k * 30}`} stroke={P.accent} strokeOpacity={0.5 - k * 0.04} strokeWidth={6} filter="url(#soft)" />)}
    <path d="M -520 40 L -440 -40 L -120 -60 L 40 -150 L 160 -150 L 220 -60 L 520 -40 L 560 30 L -520 50 Z" fill="#11151C" />
    <path d="M 40 -150 L 160 -150 L 200 -90 L 60 -90 Z" fill={P.key} opacity={0.4} />
    <path d="M -560 -120 L -420 -120 L -420 -20 L -560 -20 Z" fill="#0B0E13" /><path d="M 480 -10 L 640 -10 L 640 40 L 480 40 Z" fill="#0B0E13" />
    <path d="M -440 -40 L 520 -40" stroke={P.accent} strokeWidth={8} />
    {[-340, 360].map((x) => <g key={x}><circle cx={x} cy={40} r={110} fill="#05070A" stroke="#2C323D" strokeWidth={14} /><circle cx={x} cy={40} r={34} fill="#3A4250" /></g>)}
  </g>,
  /** A trophy surrounded by money (who earns from the sport) */
  trophy: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('gold', '#8A6414', '#FFE08A')}</defs>
    <path d="M -180 -380 L 180 -380 Q 170 -120 0 -40 Q -170 -120 -180 -380 Z" fill="url(#gold)" />
    <path d="M -180 -340 Q -320 -320 -240 -200 Q -200 -150 -140 -150 M 180 -340 Q 320 -320 240 -200 Q 200 -150 140 -150" stroke="url(#gold)" strokeWidth={26} fill="none" />
    <rect x={-30} y={-40} width={60} height={160} fill="url(#gold)" /><rect x={-170} y={120} width={340} height={70} rx={8} fill="url(#gold)" />
    {Array.from({length: 14}, (_, k) => <rect key={k} x={-520 + rnd(k) * 1040} y={-420 + rnd(k + 4) * 640} width={120} height={56} rx={6} transform={`rotate(${-40 + rnd(k + 1) * 80})`}
      fill="#3E6B48" stroke="#9FD3A8" strokeWidth={3} opacity={0.75} />)}
  </g>,
  /** A supertall desert tower skyline at golden hour, a jet overhead and a ship below. */
  skyline: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <path d="M -20 0 L -20 -560 L -8 -760 L 0 -980 L 8 -760 L 20 -560 L 20 0 Z" fill="#0B0F17" />
    <path d="M -60 0 L -60 -360 L -20 -420 L -20 0 Z M 60 0 L 60 -300 L 20 -380 L 20 0 Z" fill="#0E131C" />
    {[-420, -320, -230, 180, 280, 380, 470].map((x, k) => <rect key={x} x={x} y={-160 - rnd(k) * 260} width={70} height={160 + rnd(k) * 260} fill="#0E131C" />)}
    {Array.from({length: 40}, (_, k) => <rect key={k} x={-420 + rnd(k) * 960} y={-380 + rnd(k + 2) * 360} width={8} height={10} fill={P.accent} opacity={0.6} />)}
    <g transform="translate(-360 -760) rotate(-8)"><path d="M -90 0 L 90 0 L 110 -8 L 90 -16 L -60 -16 Z M -10 -10 L -50 -60 L -20 -60 L 30 -12 Z" fill="#0B0F17" /></g>
  </g>,
  /** A small bright island with a giant glowing domain sign. */
  island: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <ellipse cx={0} cy={60} rx={520} ry={70} fill="#000" opacity={0.4} />
    <path d="M -480 40 Q -300 -40 -80 -30 Q 160 -60 360 -10 Q 480 20 470 50 Q 200 80 -460 70 Z" fill="#1B3A2A" />
    <path d="M -470 50 Q -200 30 470 50" stroke="#E8D9A8" strokeWidth={14} fill="none" opacity={0.8} />
    {[-260, -120, 40].map((x, k) => <g key={x}><path d={`M ${x} -20 Q ${x + 10} -140 ${x + 30} -220`} stroke="#0E1A12" strokeWidth={12} fill="none" />
      <path d={`M ${x + 30} -220 q -90 10 -130 60 M ${x + 30} -220 q 90 0 130 50 M ${x + 30} -220 q -20 -70 -80 -100 M ${x + 30} -220 q 40 -70 100 -90`} stroke="#0E1A12" strokeWidth={14} fill="none" strokeLinecap="round" /></g>)}
    {o.sign && <text x={o.signX ?? 220} y={o.signY ?? -260} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={o.signSize ?? 330} fill={P.accent} filter="url(#glow)">{o.sign}</text>}
  </g>,
  /** A glowing processor die with traces and heat. */
  chip: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? 0})`}>
    {Array.from({length: 24}, (_, k) => { const side = k % 4, j = Math.floor(k / 4), off = -250 + j * 100;
      const d = side === 0 ? `M ${off} -300 L ${off} -560` : side === 1 ? `M ${off} 300 L ${off} 560` : side === 2 ? `M -300 ${off} L -620 ${off}` : `M 300 ${off} L 620 ${off}`;
      return <path key={k} d={d} stroke={P.accent} strokeWidth={8} opacity={0.75} filter="url(#glow)" />; })}
    <rect x={-300} y={-300} width={600} height={600} rx={30} fill="#0D1117" stroke="#3A4250" strokeWidth={10} />
    <rect x={-220} y={-220} width={440} height={440} rx={14} fill={P.accent} opacity={0.18} />
    <rect x={-220} y={-220} width={440} height={440} rx={14} fill="none" stroke={P.accent} strokeWidth={6} filter="url(#glow)" />
    {Array.from({length: 49}, (_, k) => <rect key={k} x={-200 + (k % 7) * 58} y={-200 + Math.floor(k / 7) * 58} width={44} height={44} fill={P.accent} opacity={0.15 + 0.5 * rnd(k)} />)}
    {o.label && <text x={0} y={30} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={90} fill="#FFFFFF" opacity={0.92}>{o.label}</text>}
  </g>,
  /** An island outline glowing like a circuit (a chip-making island) */
  chipisland: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <path d="M 120 -440 Q 190 -430 205 -360 Q 215 -250 190 -120 Q 170 0 120 130 Q 70 260 10 380 Q -20 440 -45 420 Q -70 330 -120 230 Q -180 120 -200 0 Q -215 -130 -170 -250 Q -120 -360 -40 -410 Q 40 -450 120 -440 Z" fill="#0D1520" stroke={P.accent} strokeWidth={12} filter="url(#glow)" />
    {Array.from({length: 14}, (_, k) => <path key={k} d={`M ${-120 + rnd(k) * 220} ${-320 + k * 50} l ${40 + rnd(k + 1) * 60} 0 l 0 ${30}`} stroke={P.accent} strokeWidth={5} fill="none" opacity={0.75} />)}
    {Array.from({length: 10}, (_, k) => <circle key={k} cx={-110 + rnd(k + 3) * 220} cy={-300 + rnd(k + 6) * 620} r={8} fill="#FFFFFF" />)}
  </g>,
  /** An undersea cable crossing the deep, pulses of light travelling along it. */
  cable: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <path d="M -1000 220 C -500 120 -200 340 200 200 S 700 60 1000 120" stroke="#1B2433" strokeWidth={46} fill="none" />
    <path d="M -1000 220 C -500 120 -200 340 200 200 S 700 60 1000 120" stroke={P.accent} strokeWidth={10} fill="none" filter="url(#glow)" />
    {Array.from({length: 7}, (_, k) => { const t = k / 7; const x = -1000 + t * 2000, y = 220 - 100 * Math.sin(t * Math.PI * 2) * 0.6;
      return <circle key={k} cx={x} cy={y} r={20} fill="#FFFFFF" filter="url(#glow)" />; })}
    <ellipse cx={0} cy={340} rx={1000} ry={60} fill="#000" opacity={0.5} />
  </g>,
  /** A gold-bar stack inside a mountain vault (Swiss story) */
  goldvault: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('gb', '#9A6E12', '#FFE7A0')}</defs>
    <path d="M -520 260 L -520 -160 Q 0 -520 520 -160 L 520 260 Z" fill="#0B0E14" stroke="#2A3140" strokeWidth={20} />
    {Array.from({length: 15}, (_, k) => { const row = k < 6 ? 0 : k < 11 ? 1 : k < 14 ? 2 : 3, inRow = [6, 5, 3, 1][row], i = k - [0, 6, 11, 14][row];
      const x = (i - (inRow - 1) / 2) * 140, y = 200 - row * 70;
      return <path key={k} d={`M ${x - 60} ${y} L ${x - 44} ${y - 60} L ${x + 44} ${y - 60} L ${x + 60} ${y} Z`} fill="url(#gb)" stroke="#6E4E0C" strokeWidth={3} />; })}
  </g>,
  /** A big coin / currency symbol glowing (fund, money). */
  coin: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('cg', '#8A6414', '#FFE08A')}</defs>
    <ellipse cx={0} cy={18} rx={200} ry={200} fill="#5A410C" /><circle r={200} fill="url(#cg)" />
    <circle r={160} fill="none" stroke="#8A6414" strokeWidth={8} />
    <text x={0} y={70} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={200} fill="#6B4C0E">{o.symbol || '$'}</text>
  </g>,
  /** A huge brilliant-cut diamond (side view): crown facets over a pointed pavilion, with star glints. */
  gem: (o, P) => {
    const W = 300, T = 150, CY = -120, GY = -40, PY = 300; // half-width, table half-width, crown top, girdle, culet
    const xs = [-W, -T, -T * 0.35, T * 0.35, T, W];
    const crown = xs.slice(0, -1).map((x, k) => {
      const x2 = xs[k + 1], top = (v: number) => (Math.abs(v) <= T + 1 ? CY : GY);
      return <path key={'c' + k} d={`M ${x} ${top(x)} L ${x2} ${top(x2)} L ${x2} ${GY} L ${x} ${GY} Z`} fill={['#BFE8FF', '#E9F8FF', '#FFFFFF', '#D6F1FF', '#9FD7F5'][k]} stroke="#5FA9D6" strokeWidth={3} />;
    });
    const pav = [-W, -W * 0.55, -W * 0.15, W * 0.15, W * 0.55, W].slice(0, -1).map((x, k, a) => {
      const x2 = [-W, -W * 0.55, -W * 0.15, W * 0.15, W * 0.55, W][k + 1];
      return <path key={'p' + k} d={`M ${x} ${GY} L ${x2} ${GY} L 0 ${PY} Z`} fill={['#7CC4EE', '#CDEEFF', '#FFFFFF', '#A9DDF7', '#5FB0E0'][k]} stroke="#4A93C2" strokeWidth={3} />;
    });
    const glint = (x: number, y: number, r: number, k: number) => <path key={'g' + k} transform={`translate(${x} ${y})`}
      d={`M 0 ${-r} L ${r * 0.16} ${-r * 0.16} L ${r} 0 L ${r * 0.16} ${r * 0.16} L 0 ${r} L ${-r * 0.16} ${r * 0.16} L ${-r} 0 L ${-r * 0.16} ${-r * 0.16} Z`} fill="#FFFFFF" filter="url(#glow)" />;
    return <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -8})`}>
      <ellipse cx={0} cy={PY + 60} rx={260} ry={40} fill="#000" opacity={0.35} filter="url(#soft)" />
      <circle r={420} fill={o.halo || P.key} opacity={0.18} filter="url(#soft)" />
      {pav}{crown}
      <path d={`M ${-T} ${CY} L ${T} ${CY}`} stroke="#FFFFFF" strokeWidth={6} />
      {glint(-T * 0.5, CY + 10, 70, 0)}{glint(W * 0.75, GY - 20, 48, 1)}{glint(-W * 0.3, 140, 36, 2)}
    </g>;
  },
  /** A stack of metal ingots (trapezoid bars) stamped with a short element mark, e.g. "Ni". */
  ingots: (o, P) => {
    const bar = (x: number, y: number, k: number) => <g key={k} transform={`translate(${x} ${y})`}>
      <path d="M -170 0 L 170 0 L 140 -70 L -140 -70 Z" fill="url(#ing)" stroke="#3B434F" strokeWidth={4} />
      <path d="M -170 0 L 170 0 L 170 22 L -170 22 Z" fill="#59616E" />
      <path d="M -140 -70 L 140 -70 L 120 -82 L -120 -82 Z" fill="#E8EDF3" opacity={0.9} />
      <text x={0} y={-22} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={44} fill="#3B434F" opacity={0.75}>{o.mark || 'Ni'}</text>
    </g>;
    return <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
      <defs>{metal('ing', '#8C96A4', '#E3E9F0')}</defs>
      <ellipse cx={0} cy={60} rx={420} ry={44} fill="#000" opacity={0.4} filter="url(#soft)" />
      {[[-180, 40], [180, 40], [0, -64]].map(([x, y], k) => bar(x, y, k))}
      {o.tag && <g transform="translate(0 -260)"><rect x={-210} y={-60} width={420} height={96} rx={14} fill={P.accent} />
        <text x={0} y={10} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={60} fill="#111">{o.tag}</text></g>}
    </g>;
  },
  /** A giant generic cartoon burger (sesame bun, patty, cheese, lettuce) with a warm glow and steam; no brand marks. */
  burger: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <circle r={430} fill={P.key} opacity={0.22} filter="url(#soft)" />
    <ellipse cx={0} cy={230} rx={300} ry={36} fill="#000" opacity={0.4} filter="url(#soft)" />
    <path d="M -280 90 Q -295 200 -220 205 L 220 205 Q 295 200 280 90 Z" fill="#E39A4C" stroke="#3A2414" strokeWidth={8} />
    <path d="M -300 45 L 300 45 L 288 100 L -288 100 Z" fill="#5A3220" stroke="#3A2414" strokeWidth={8} strokeLinejoin="round" />
    <path d="M -292 30 L 292 30 L 220 80 L 160 40 L 60 92 L -30 40 L -130 86 L -205 40 Z" fill="#FFC21A" stroke="#3A2414" strokeWidth={7} strokeLinejoin="round" />
    <path d={`M -315 10 ${Array.from({length: 12}, (_, k) => `Q ${-289 + k * 52.5} ${42 + (k % 2) * 12} ${-262 + k * 52.5} 10`).join(' ')} L 315 10 L 315 32 L -315 32 Z`} fill="#6CCB6A" stroke="#3A2414" strokeWidth={6} strokeLinejoin="round" />
    <path d="M -295 0 Q -295 -230 0 -230 Q 295 -230 295 0 Z" fill="#F2A44A" stroke="#3A2414" strokeWidth={8} />
    <path d="M -230 -60 Q -200 -190 -40 -205" fill="none" stroke="#FFFFFF" strokeWidth={18} strokeLinecap="round" opacity={0.35} />
    {Array.from({length: 14}, (_, k) => <ellipse key={k} cx={-180 + rnd(k) * 360} cy={-170 + rnd(k + 4) * 130} rx={13} ry={7} transform={`rotate(${rnd(k + 7) * 60 - 30})`} fill="#FFF5E1" stroke="#3A2414" strokeWidth={2} />)}
    {[0, 1, 2].map((q) => <path key={q} d={`M ${-90 + q * 90} ${-260 - q * 10} q 22 -30 0 -60 q -22 -30 0 -60`} fill="none" stroke="#FFFFFF" strokeWidth={12} strokeLinecap="round" opacity={0.5} />)}
  </g>,
  /** A big black oil drum with steel hoops and a drop mark; `money` sends banknotes flying away from it. */
  oilbarrel: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <defs>{metal('ob', '#1B1F26', '#3A424F')}</defs>
    <circle r={420} fill={P.haze} opacity={0.16} filter="url(#soft)" />
    <ellipse cx={0} cy={300} rx={240} ry={34} fill="#000" opacity={0.5} filter="url(#soft)" />
    <rect x={-200} y={-280} width={400} height={570} rx={40} fill="url(#ob)" stroke="#0A0C10" strokeWidth={10} />
    {[-130, 60].map((y) => <rect key={y} x={-212} y={y} width={424} height={34} rx={16} fill="#5A6472" stroke="#0A0C10" strokeWidth={6} />)}
    <ellipse cx={0} cy={-280} rx={200} ry={44} fill="#2C333D" stroke="#0A0C10" strokeWidth={8} />
    <ellipse cx={0} cy={-280} rx={150} ry={30} fill="#11151B" />
    <path d="M -150 -270 Q -60 -230 40 -262 Q 30 -200 -40 -190" fill="#000" opacity={0.9} />
    <path d="M -40 -40 q 40 -100 80 0 a 40 40 0 1 1 -80 0 Z" fill={P.accent} stroke="#0A0C10" strokeWidth={6} />
    <path d="M -150 -240 L -150 250" stroke="#FFFFFF" strokeWidth={16} strokeLinecap="round" opacity={0.12} />
    {o.money && Array.from({length: 7}, (_, k) => <g key={k} transform={`translate(${-330 - k * 60 + rnd(k) * 40} ${-200 + rnd(k + 3) * 380}) rotate(${-40 + rnd(k + 5) * 80})`} opacity={0.95 - k * 0.1}>
      <rect x={-80} y={-38} width={160} height={76} rx={8} fill="#3E6B48" stroke="#9FD3A8" strokeWidth={4} /><circle r={20} fill="none" stroke="#9FD3A8" strokeWidth={4} />
      <text x={0} y={12} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={30} fill="#9FD3A8">$</text></g>)}
  </g>,
  /** An isometric data-center campus at night: rows of halls with glowing server windows and roof fans, power lines. */
  campus: (o, P) => {
    const Wd = 230, D = 130, Hh = 120;
    const iso = (gx: number, gy: number) => [(gx - gy) * Wd * 0.62, (gx + gy) * D * 0.62];
    const cells = [] as {gx: number; gy: number}[];
    for (let gy = 0; gy < 3; gy++) for (let gx = 0; gx < 3; gx++) cells.push({gx, gy});
    return <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
      <ellipse cx={0} cy={D * 1.6} rx={620} ry={260} fill={P.haze} opacity={0.18} filter="url(#soft)" />
      {cells.map(({gx, gy}, k) => { const [cx, cy] = iso(gx, gy);
        return <g key={k}>
          <path d={`M ${cx - Wd / 2} ${cy + D / 2 - Hh} L ${cx} ${cy + D - Hh} L ${cx} ${cy + D} L ${cx - Wd / 2} ${cy + D / 2} Z`} fill="#55708F" stroke="#0A0E16" strokeWidth={4} />
          <path d={`M ${cx} ${cy + D - Hh} L ${cx + Wd / 2} ${cy + D / 2 - Hh} L ${cx + Wd / 2} ${cy + D / 2} L ${cx} ${cy + D} Z`} fill="#33445A" stroke="#0A0E16" strokeWidth={4} />
          <path d={`M ${cx} ${cy - Hh} L ${cx + Wd / 2} ${cy - Hh + D / 2} L ${cx} ${cy - Hh + D} L ${cx - Wd / 2} ${cy - Hh + D / 2} Z`} fill="#C9D6E6" stroke="#0A0E16" strokeWidth={4} />
          {Array.from({length: 6}, (_, q) => <rect key={q} x={cx - Wd / 2 + 16 + q * 16} y={cy + D / 2 - Hh * 0.6 + q * 8} width={10} height={26} fill={P.accent} opacity={0.5 + 0.5 * rnd(k * 7 + q)} filter="url(#glow)" />)}
          {[0, 1].map((q) => <ellipse key={'f' + q} cx={cx - 30 + q * 60} cy={cy - Hh + D / 2} rx={22} ry={12} fill="#1C2533" stroke="#8FA3BC" strokeWidth={3} />)}
        </g>; })}
    </g>;
  },
  /** A big generic credit card (no brand): gradient, chip, contactless mark, a few fee coins flying off it. */
  ccard: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -10})`}>
    <defs><linearGradient id="ccg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={o.c1 || '#3F51B5'} /><stop offset="1" stopColor={o.c2 || '#0B1440'} /></linearGradient></defs>
    <circle r={480} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <rect x={-380} y={-240} width={760} height={480} rx={42} fill="#000" opacity={0.45} transform="translate(18 26)" filter="url(#soft)" />
    <rect x={-380} y={-240} width={760} height={480} rx={42} fill="url(#ccg)" stroke="#05070B" strokeWidth={8} />
    <path d="M -380 -60 Q 0 -200 380 -120 L 380 -240 L -380 -240 Z" fill="#FFFFFF" opacity={0.08} />
    <rect x={-300} y={-100} width={130} height={100} rx={14} fill="#E3C46E" stroke="#05070B" strokeWidth={4} />
    <path d="M -300 -50 L -170 -50 M -235 -100 L -235 0" stroke="#A88A3C" strokeWidth={4} />
    {[0, 1, 2].map((q) => <path key={q} d={`M ${240 + q * 30} -120 q ${26 + q * 10} 50 0 100`} fill="none" stroke="#FFFFFF" strokeWidth={9} strokeLinecap="round" opacity={0.85} />)}
    {[0, 1, 2, 3].map((g) => <text key={g} x={-290 + g * 160} y={120} fontFamily={FONT} fontWeight={900} fontSize={54} fill="#FFFFFF" opacity={0.85}>••••</text>)}
    {o.coins && Array.from({length: 5}, (_, k) => <g key={k} transform={`translate(${420 + k * 70} ${-260 + k * 90})`}><circle r={46} fill={P.accent} stroke="#05070B" strokeWidth={6} />
      <text x={0} y={18} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={52} fill="#05070B">$</text></g>)}
  </g>,
  /** A suburban house with a for-sale sign (`price` on it; `lock` puts a padlock on the door; `lit` lights the windows). */
  house: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <circle r={520} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <ellipse cx={0} cy={300} rx={520} ry={40} fill="#000" opacity={0.4} filter="url(#soft)" />
    <rect x={-330} y={-60} width={660} height={360} fill={o.wall || '#F5EBDD'} stroke="#05070B" strokeWidth={8} />
    <path d="M -400 -60 L 0 -360 L 400 -60 Z" fill={o.roof || '#B23A35'} stroke="#05070B" strokeWidth={8} strokeLinejoin="round" />
    <path d="M -400 -60 L 0 -360 L 400 -60" fill="none" stroke="#FFFFFF" strokeWidth={4} opacity={0.15} />
    <rect x={170} y={-330} width={70} height={150} fill="#6D4C41" stroke="#05070B" strokeWidth={6} />
    {[-250, 110].map((dx) => <g key={dx}><rect x={dx} y={20} width={140} height={120} rx={6} fill={o.lit ? '#FFD54F' : '#9FD8F5'} stroke="#05070B" strokeWidth={6} />
      <path d={`M ${dx + 70} 20 L ${dx + 70} 140 M ${dx} 80 L ${dx + 140} 80`} stroke="#05070B" strokeWidth={4} /></g>)}
    <rect x={-60} y={110} width={120} height={190} rx={8} fill="#8A5428" stroke="#05070B" strokeWidth={6} />
    {o.lock && <g transform="translate(0 170)"><path d="M -40 -20 L -40 -60 Q 0 -110 40 -60 L 40 -20" fill="none" stroke="#B0BEC5" strokeWidth={16} />
      <rect x={-60} y={-26} width={120} height={96} rx={14} fill={P.accent} stroke="#05070B" strokeWidth={7} /><circle cx={0} cy={14} r={12} fill="#05070B" /></g>}
    {o.price && <g transform={`translate(${o.signX ?? -470} 300)`}><rect x={-8} y={-260} width={16} height={260} fill="#5D4037" stroke="#05070B" strokeWidth={4} />
      <rect x={-170} y={-300} width={340} height={150} rx={12} fill="#FFFFFF" stroke="#05070B" strokeWidth={7} />
      <rect x={-170} y={-300} width={340} height={44} rx={12} fill="#E53935" stroke="#05070B" strokeWidth={7} />
      <text x={0} y={-268} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={30} fill="#FFFFFF">FOR SALE</text>
      <text x={0} y={-180} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={o.price.length > 7 ? 54 : 70} fill="#05070B">{o.price}</text></g>}
  </g>,
  /** A graduation cap (mortarboard) with a gold tassel, optionally chained to a ball (`chain`) with `label` on it. */
  gradcap: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -8})`}>
    <circle r={500} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <path d="M -420 -40 L 0 -220 L 420 -40 L 0 140 Z" fill="#000" opacity={0.4} transform="translate(20 30)" filter="url(#soft)" />
    <path d="M -230 40 L -230 190 Q 0 290 230 190 L 230 40" fill="#1B1B1B" stroke="#05070B" strokeWidth={10} />
    <path d="M -420 -40 L 0 -220 L 420 -40 L 0 140 Z" fill="#262626" stroke="#05070B" strokeWidth={10} strokeLinejoin="round" />
    <path d="M -420 -40 L 0 -220 L 420 -40" fill="none" stroke="#FFFFFF" strokeWidth={5} opacity={0.15} />
    <circle cx={0} cy={-40} r={22} fill={P.accent} stroke="#05070B" strokeWidth={5} />
    <path d="M 0 -40 L 300 40 L 300 250" stroke={P.accent} strokeWidth={14} fill="none" strokeLinecap="round" />
    <path d="M 270 250 L 330 250 L 345 360 L 255 360 Z" fill={P.accent} stroke="#05070B" strokeWidth={6} />
    {o.chain && <g>{Array.from({length: 5}, (_, k) => <ellipse key={k} cx={-260 - k * 40} cy={230 + k * 40} rx={26} ry={16} fill="none" stroke="#9E9E9E" strokeWidth={10} transform={`rotate(${k % 2 ? 40 : -40} ${-260 - k * 40} ${230 + k * 40})`} />)}
      <circle cx={-520} cy={480} r={150} fill="#37474F" stroke="#05070B" strokeWidth={10} />
      {o.label && <text x={-520} y={500} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={56} fill="#FFFFFF">{o.label}</text>}</g>}
  </g>,
  /** A generic sedan, three-quarter-ish side view, with a window price sticker (`sticker`). No brand. */
  sedan: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s}) rotate(${o.rot ?? -4})`}>
    <circle r={540} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <ellipse cx={0} cy={150} rx={560} ry={40} fill="#000" opacity={0.45} filter="url(#soft)" />
    <path d="M -560 90 L -560 -20 Q -540 -80 -450 -90 L -300 -105 L -170 -240 Q -130 -270 -60 -270 L 200 -270 Q 260 -270 300 -230 L 420 -110 L 510 -95 Q 570 -80 570 -10 L 570 90 Z" fill={o.color || '#D32F2F'} stroke="#05070B" strokeWidth={10} strokeLinejoin="round" />
    <path d="M -560 0 Q 0 -60 570 0" stroke="#FFFFFF" strokeWidth={8} opacity={0.18} fill="none" />
    <path d="M -270 -110 L -160 -225 L 30 -225 L 30 -110 Z" fill="#9FD8F5" stroke="#05070B" strokeWidth={7} />
    <path d="M 70 -110 L 70 -225 L 190 -225 Q 230 -225 255 -195 L 340 -110 Z" fill="#9FD8F5" stroke="#05070B" strokeWidth={7} />
    {[-340, 360].map((dx) => <g key={dx} transform={`translate(${dx} 90)`}><circle r={95} fill="#1B1B1B" stroke="#05070B" strokeWidth={8} /><circle r={45} fill="#B0BEC5" stroke="#05070B" strokeWidth={5} /></g>)}
    {o.sticker && <g transform="translate(-100 -168)"><rect x={-100} y={-48} width={200} height={96} rx={6} fill="#FFFFFF" stroke="#05070B" strokeWidth={6} />
      <text x={0} y={18} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={o.sticker.length > 6 ? 40 : 52} fill="#05070B">{o.sticker}</text></g>}
  </g>,
  /** A home electricity meter with a digital readout (`text`) and a lightning bolt. */
  meter: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <circle r={520} fill={P.haze} opacity={0.2} filter="url(#soft)" />
    <rect x={-210} y={-60} width={420} height={560} rx={36} fill="#90A4AE" stroke="#05070B" strokeWidth={10} />
    <circle cx={0} cy={0} r={260} fill="#ECEFF1" stroke="#05070B" strokeWidth={10} />
    <rect x={-170} y={-140} width={340} height={110} rx={14} fill="#0E1621" stroke="#05070B" strokeWidth={8} />
    <text x={0} y={-62} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={o.text && o.text.length > 5 ? 64 : 80} fill="#7DF29A">{o.text || '$$$'}</text>
    <ellipse cx={0} cy={90} rx={160} ry={26} fill="#78909C" stroke="#05070B" strokeWidth={6} />
    <path d="M 40 -420 L -60 -230 L 10 -230 L -40 -80 L 110 -300 L 30 -300 L 90 -420 Z" fill={P.accent} stroke="#05070B" strokeWidth={8} strokeLinejoin="round" transform="translate(230 60)" />
  </g>,
  /** A stack of plain cardboard parcels with tape (no logo). */
  parcels: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <circle r={540} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <ellipse cx={0} cy={330} rx={520} ry={40} fill="#000" opacity={0.45} filter="url(#soft)" />
    {[[-230, 120, 380, 260], [180, 140, 320, 220], [-40, -150, 360, 280]].map(([bx, by, bw, bh], k) => <g key={k}>
      <rect x={bx - bw / 2} y={by - bh / 2} width={bw} height={bh} rx={10} fill={['#C8A27A', '#D7B98E', '#B98E62'][k]} stroke="#05070B" strokeWidth={9} />
      <rect x={bx - 26} y={by - bh / 2} width={52} height={bh} fill="#E9D5B5" stroke="#05070B" strokeWidth={4} />
      <rect x={bx + bw / 2 - 130} y={by + bh / 2 - 80} width={100} height={56} rx={6} fill="#FFFFFF" stroke="#05070B" strokeWidth={4} />
      <path d={`M ${bx + bw / 2 - 118} ${by + bh / 2 - 64} l 76 0 m -76 14 l 60 0 m -60 14 l 70 0`} stroke="#05070B" strokeWidth={4} /></g>)}
  </g>,
  /** A generic shopping cart full of groceries (no brands) */
  cart: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    <circle r={560} fill={P.haze} opacity={0.18} filter="url(#soft)" />
    <ellipse cx={0} cy={360} rx={520} ry={40} fill="#000" opacity={0.45} filter="url(#soft)" />
    {[['#E53935', -200, -120, 70], ['#FB8C00', -60, -150, 80], ['#7CB342', 90, -130, 75], ['#FDD835', 220, -110, 65]].map(([c, x, y, r], k) => <circle key={k} cx={x as number} cy={y as number} r={r as number} fill={c as string} stroke="#05070B" strokeWidth={9} />)}
    <rect x={-150} y={-260} width={120} height={160} rx={10} fill="#FFF8E7" stroke="#05070B" strokeWidth={9} />
    <rect x={40} y={-290} width={90} height={190} rx={10} fill="#90CAF9" stroke="#05070B" strokeWidth={9} />
    <path d="M -400 -300 L -330 -300 L -260 180 L 330 180 L 380 -100 L -300 -100" fill="none" stroke="#05070B" strokeWidth={22} strokeLinejoin="round" />
    <path d="M -300 -100 L 380 -100 L 340 120 L -270 120 Z" fill="#B0BEC5" stroke="#05070B" strokeWidth={10} opacity={0.9} />
    {Array.from({length: 7}, (_, k) => <path key={k} d={`M ${-260 + k * 95} -100 L ${-240 + k * 85} 120`} stroke="#05070B" strokeWidth={6} />)}
    <circle cx={-200} cy={250} r={44} fill="#263238" stroke="#05070B" strokeWidth={9} /><circle cx={260} cy={250} r={44} fill="#263238" stroke="#05070B" strokeWidth={9} />
  </g>,
  /** A row of numbers glitching (cyber) */
  glitch: (o, P) => <g transform={`translate(${o.x} ${o.y}) scale(${o.s})`}>
    {Array.from({length: 18}, (_, k) => <rect key={k} x={-700 + rnd(k) * 1200} y={-400 + k * 46} width={100 + rnd(k + 3) * 500} height={18} fill={k % 3 ? P.accent : '#FF2D55'} opacity={0.5} />)}
  </g>,
};

/* ------------------------------------------------------------------------------------------------ text */
const TextLine: React.FC<{t: ThumbText}> = ({t}) => {
  const left = t.anchor === 'start' ? t.x : t.anchor === 'end' ? t.x - t.width : t.x - t.width / 2;
  const pad = t.boxPad ?? 22;
  return <g transform={t.rotate ? `rotate(${t.rotate} ${t.x} ${t.y})` : undefined}>
    {t.box && <rect x={left - pad} y={t.y - t.size * 0.86 - pad * 0.5} width={t.width + pad * 2} height={t.size * 1.02 + pad} fill={t.box} />}
    <text x={t.x} y={t.y} textAnchor={t.anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} textLength={t.width} lengthAdjust="spacingAndGlyphs"
      fill="#000" opacity={0.55} transform={`translate(6 10)`} filter="url(#soft)">{t.text}</text>
    <text x={t.x} y={t.y} textAnchor={t.anchor} fontFamily={FONT} fontWeight={900} fontSize={t.size} textLength={t.width} lengthAdjust="spacingAndGlyphs"
      fill={t.color} stroke={t.box ? 'none' : '#05070B'} strokeWidth={t.box ? 0 : Math.max(6, t.size * 0.07)} paintOrder="stroke" strokeLinejoin="round">{t.text}</text>
    {t.underline && <rect x={left} y={t.y + t.size * 0.12} width={t.width} height={Math.max(8, t.size * 0.08)} fill={t.underline} />}
  </g>;
};

export const CinematicThumb: React.FC<CinematicProps> = (p) => {
  const P = p.palette, S = SUBJECTS[p.subject.kind];
  const brand = p.brand || 'tl';
  const bx = brand === 'tr' ? W - 64 - 420 : 64, by = brand === 'bl' ? H - 64 - 44 : 56;
  return (
    <AbsoluteFill style={{backgroundColor: P.sky1}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
          <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" /></filter>
          <filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={3} /><feColorMatrix type="saturate" values="0" /></filter>
          <linearGradient id="paperShade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0.2} /><stop offset="1" stopColor="#000" stopOpacity={0.35} /></linearGradient>
          <radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset="55%" stopColor="#000" stopOpacity={0} /><stop offset="100%" stopColor="#000" stopOpacity={p.vignette ?? 0.75} /></radialGradient>
          <radialGradient id="rim" cx="50%" cy="50%" r="50%"><stop offset="0" stopColor={P.key} stopOpacity={0.35} /><stop offset="1" stopColor={P.key} stopOpacity={0} /></radialGradient>
        </defs>
        <Backdrop p={p} />
        {(p.beams || []).map((b, i) => <Beam key={i} b={b} i={i} color={P.key} />)}
        <ellipse cx={p.subject.x} cy={p.subject.y} rx={700 * p.subject.s} ry={520 * p.subject.s} fill="url(#rim)" />
        {(p.support || []).map((s, i) => { const F = SUBJECTS[s.kind]; return F ? <g key={i} opacity={s.opacity ?? 1}>{F(s, P)}</g> : null; })}
        {p.archetype === 'split' && <g>
          <rect x={0} y={0} width={W / 2} height={H} fill="#0A2A4A" opacity={0.35} />
          <rect x={W / 2} y={0} width={W / 2} height={H} fill="#5A0A0A" opacity={0.35} />
          <rect x={W / 2 - 5} y={0} width={10} height={H} fill="#FFFFFF" opacity={0.85} />
          <g transform={`translate(${W / 2} ${H / 2 + 60})`}><circle r={86} fill={P.accent} stroke="#05070B" strokeWidth={8} />
            <path d="M -38 -34 L 22 0 L -38 34 M -10 -34 L 50 0 L -10 34" fill="none" stroke="#05070B" strokeWidth={16} strokeLinejoin="round" strokeLinecap="round" /></g>
        </g>}
        {S ? S(p.subject, P) : null}
        {p.archetype === 'split' && p.after && SUBJECTS[p.after.kind] ? SUBJECTS[p.after.kind](p.after, P) : null}
        {p.presenter && <g transform={`translate(${p.presenter.x} ${p.presenter.y}) scale(${p.presenter.s})`}>
          <Character pose={{x: 0, floor: 0, facing: p.presenter.face ?? -1, walk: 0, moving: 0, hop: 0, drawHand: null,
            pointHand: [(p.subject.x - p.presenter.x) / p.presenter.s, (p.subject.y - p.presenter.y) / p.presenter.s], talking: 0.9, blink: 0,
            surprise: 1, scale: 1, holdingMarker: false, smile: 0}} />
        </g>}
        {p.particles && <Particles p={p.particles} color={P.key} />}
        <rect width={W} height={H} fill="url(#vig)" />
        <rect width={W} height={H} filter="url(#grain)" opacity={p.grain ?? 0.07} style={{mixBlendMode: 'overlay'}} />
        {!p.hideText && p.text.map((t, i) => <TextLine key={i} t={t} />)}
        {/* channel mark: identical on every thumbnail, small (identity without competing) */}
        {brand !== 'none' && <g transform={`translate(${bx} ${by})`} opacity={0.92}>
          <rect width={8} height={44} fill="#D4AF5A" />
          <text x={22} y={33} fontFamily="Inter, sans-serif" fontWeight={800} fontSize={26} letterSpacing={5} fill="#F4F1EA">THE HIDDEN ECONOMICS</text>
        </g>}
      </svg>
    </AbsoluteFill>
  );
};
