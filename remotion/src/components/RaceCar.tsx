import React from 'react';

/**
 * Original, generic open-wheel race car (side view), drawn in SVG. No team livery, logo or real car's shape.
 * Moving parts: wheels spin with `spin` (radians), suspension bob, exhaust heat shimmer, optional speed lines.
 * Origin = rear-axle ground point; length ~ 560 px at scale 1.
 */
export const RaceCar: React.FC<{
  x: number; y: number; scale?: number; body: string; trim: string; dark?: string; spin: number; t: number;
  speedLines?: number; number?: string; flip?: boolean; opacity?: number;
}> = ({x, y, scale = 1, body, trim, dark = '#14161B', spin, t, speedLines = 0, number, flip = false, opacity = 1}) => {
  const bob = Math.sin(t * 22) * 1.4;
  const wheel = (cx: number, r: number) => (
    <g transform={`translate(${cx} ${-r})`}>
      <circle r={r} fill={dark} />
      <circle r={r * 0.62} fill="#2A2E36" />
      <g transform={`rotate(${(spin * 180) / Math.PI})`}>
        {[0, 72, 144, 216, 288].map((a) => (
          <rect key={a} x={-3} y={-r * 0.6} width={6} height={r * 0.6} fill="#8C949E" transform={`rotate(${a})`} />
        ))}
      </g>
      <circle r={r * 0.16} fill={trim} />
      <circle r={r} fill="none" stroke="#000" strokeOpacity={0.35} strokeWidth={4} />
    </g>
  );
  return (
    <g transform={`translate(${x} ${y}) scale(${flip ? -scale : scale} ${scale})`} opacity={opacity}>
      {speedLines > 0 && Array.from({length: 7}, (_, i) => {
        const len = 180 + ((i * 53 + t * 900) % 220);
        return <rect key={i} x={-90 - len} y={-150 + i * 18} width={len} height={3} fill="#FFFFFF" opacity={0.18 * speedLines} />;
      })}
      {/* exhaust heat */}
      {Array.from({length: 4}, (_, i) => {
        const q = (t * 3 + i / 4) % 1;
        return <ellipse key={i} cx={-40 - q * 120} cy={-92 - Math.sin(q * 9 + i) * 6} rx={14 + q * 30} ry={6 + q * 8} fill="#FFFFFF" opacity={0.08 * (1 - q)} />;
      })}
      <g transform={`translate(0 ${bob})`}>
        {/* floor + sidepod + nose */}
        <path d="M -30 -46 L 470 -46 L 540 -60 L 545 -70 L 420 -78 L 300 -84 L 230 -118 L 150 -120 L 90 -108 L 10 -104 L -30 -90 Z" fill={body} />
        <path d="M 60 -104 L 160 -146 L 215 -146 L 235 -118 Z" fill={dark} />
        <path d="M 150 -146 C 170 -178, 205 -178, 220 -146 Z" fill={dark} />
        {/* halo */}
        <path d="M 150 -150 C 175 -190, 230 -186, 250 -128" fill="none" stroke={dark} strokeWidth={9} strokeLinecap="round" />
        {/* livery stripe */}
        <path d="M 10 -96 L 300 -80 L 420 -74 L 420 -66 L 300 -70 L 10 -84 Z" fill={trim} />
        {/* rear wing */}
        <rect x={-58} y={-178} width={70} height={16} rx={3} fill={dark} />
        <rect x={-50} y={-162} width={8} height={70} fill={dark} />
        <rect x={-58} y={-196} width={70} height={10} rx={3} fill={trim} />
        {/* front wing */}
        <path d="M 470 -40 L 560 -40 L 566 -52 L 480 -54 Z" fill={dark} />
        <rect x={520} y={-58} width={44} height={6} fill={trim} />
        {/* mirror */}
        <rect x={238} y={-128} width={22} height={8} rx={3} fill={dark} />
        {number && <text x={340} y={-88} fontFamily="Inter Display, Inter, sans-serif" fontWeight={800} fontSize={30} fill="#FFFFFF">{number}</text>}
      </g>
      {wheel(0, 58)}
      {wheel(430, 50)}
    </g>
  );
};
