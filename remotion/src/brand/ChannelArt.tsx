import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Character} from '../presenter/Presenter';

/** Channel art (original SVG, no logos): profile picture (800x800, round-crop safe) and banner (2560x1440, text inside
 *  the 1546x423 safe area that shows on every device). `variant`: 'mascot' (the channel presenter) | 'monogram'. */
const OL = '#0B0B0F', FONT = 'Inter Display, Inter, sans-serif', GOLD = '#FFC21A', NAVY0 = '#0A1430', NAVY1 = '#1E3A7A';

const Rays: React.FC<{cx: number; cy: number; r: number; n?: number; op?: number}> = ({cx, cy, r, n = 24, op = 0.12}) => <g>
  {Array.from({length: n}, (_, k) => { const a0 = (k / n) * Math.PI * 2, a1 = a0 + Math.PI / n;
    return <path key={k} d={`M ${cx} ${cy} L ${cx + Math.cos(a0) * r} ${cy + Math.sin(a0) * r} L ${cx + Math.cos(a1) * r} ${cy + Math.sin(a1) * r} Z`} fill="#FFFFFF" opacity={op} />; })}
</g>;

const Coin: React.FC<{x: number; y: number; r: number; rot?: number}> = ({x, y, r, rot = 0}) =>
  <g transform={`translate(${x} ${y}) rotate(${rot})`}>
    <circle r={r} fill={GOLD} stroke={OL} strokeWidth={r * 0.12} /><circle r={r * 0.72} fill="none" stroke="#C98E00" strokeWidth={r * 0.08} />
    <text y={r * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={r * 1.05} fill={OL}>$</text></g>;

const mascot = (x: number, floor: number, S: number) => <Character pose={{x, floor, facing: 1, walk: 0, moving: 0, hop: 0,
  drawHand: null, pointHand: null, talking: 0.4, blink: 0, surprise: 0, scale: S, holdingMarker: false, smile: 1} as any} />;

export const ChannelAvatar: React.FC<{variant?: 'mascot' | 'monogram'}> = ({variant = 'mascot'}) => (
  <AbsoluteFill style={{backgroundColor: NAVY0}}>
    <svg width={800} height={800} viewBox="0 0 800 800">
      <defs><radialGradient id="bgA" cx="50%" cy="45%" r="60%"><stop offset="0" stopColor={NAVY1} /><stop offset="1" stopColor={NAVY0} /></radialGradient></defs>
      <rect width={800} height={800} fill="url(#bgA)" />
      <Rays cx={400} cy={360} r={700} op={0.07} />
      {variant === 'mascot' ? <g>
        <Coin x={150} y={210} r={56} rot={-14} /><Coin x={655} y={250} r={44} rot={12} />
        {mascot(400, 1520, 2.05)}
      </g> : <g>
        <circle cx={400} cy={400} r={250} fill="none" stroke={GOLD} strokeWidth={14} />
        <text x={400} y={470} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={230} fill={GOLD} letterSpacing={-8}>HE</text>
        <Coin x={590} y={235} r={62} rot={14} />
      </g>}
      {/* gold ring, inside the round crop */}
      <circle cx={400} cy={400} r={388} fill="none" stroke={GOLD} strokeWidth={22} />
    </svg>
  </AbsoluteFill>
);

export const ChannelBanner: React.FC = () => {
  const W = 2560, H = 1440, sx = (W - 1546) / 2, sy = (H - 423) / 2;   // TV/desktop/mobile safe area
  return (
    <AbsoluteFill style={{backgroundColor: NAVY0}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs><linearGradient id="bgB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor={NAVY0} /><stop offset="1" stopColor={NAVY1} /></linearGradient></defs>
        <rect width={W} height={H} fill="url(#bgB)" />
        <Rays cx={W / 2} cy={H / 2} r={1700} n={36} op={0.05} />
        {/* skyline of retro-futurist chip towers along the bottom (decorative, outside the safe text block) */}
        {Array.from({length: 22}, (_, k) => { const x = k * 122 - 20, h = 120 + ((k * 73) % 5) * 55, c = ['#3DF5FF', '#FF4FD8', '#FFE14D', '#7DFF8A', '#7B61FF'][k % 5];
          return <g key={k} opacity={0.5}><rect x={x} y={H - 330 - h} width={96} height={h + 330} rx={18} fill="#16244F" stroke={OL} strokeWidth={6} />
            {Array.from({length: 4}, (_, r) => <rect key={r} x={x + 18} y={H - 300 - h + 40 + r * 52} width={60} height={22} rx={6} fill={c} opacity={0.55} />)}</g>; })}
        {/* floating coins + a rising chart line */}
        <path d={`M ${sx - 300} ${sy + 470} L ${sx + 200} ${sy + 420} L ${sx + 520} ${sy + 450} L ${sx + 900} ${sy + 330} L ${sx + 1250} ${sy + 360} L ${sx + 1846} ${sy + 120}`}
          fill="none" stroke={GOLD} strokeWidth={14} strokeLinejoin="round" opacity={0.18} />
        <Coin x={sx - 120} y={sy + 90} r={70} rot={-12} /><Coin x={sx + 1760} y={sy + 470} r={58} rot={16} /><Coin x={sx + 1620} y={sy - 60} r={40} rot={-8} />
        {/* mascot on the left of the safe area */}
        <g>{mascot(sx + 190, sy + 520, 0.95)}</g>
        {/* title block inside the safe area */}
        <text x={sx + 420} y={sy + 200} fontFamily={FONT} fontWeight={900} fontSize={88} fill="#FFFFFF" letterSpacing={-2}
          stroke={OL} strokeWidth={10} paintOrder="stroke">THE HIDDEN ECONOMICS</text>
        <rect x={sx + 424} y={sy + 236} width={1060} height={10} rx={5} fill={GOLD} />
        <text x={sx + 424} y={sy + 330} fontFamily={FONT} fontWeight={800} fontSize={58} fill={GOLD}>The money behind the headlines.</text>
        <text x={sx + 424} y={sy + 398} fontFamily={FONT} fontWeight={700} fontSize={36} fill="#C9D6F5">Companies · Stocks · Scandals · Every number sourced</text>
      </svg>
    </AbsoluteFill>
  );
};
