import React from 'react';
import {easeBack, eio, eo, lerp, prog, useCtx} from '../lib/anim';

/**
 * Animated money-flow diagram. Nodes appear on cues; links draw as paths and then carry moving
 * 'coins'. Typical use: oil & gas revenue -> state -> fund -> world markets, and the fiscal-rule
 * withdrawal back to the budget. Node shapes: platform, state, vault, globe, budget, box.
 */
export const FundFlow: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const nodes: Record<string, any> = {};
  (p.nodes || []).forEach((n: any) => (nodes[n.id] = n));
  const appear = (n: any) => cue(n, 0);
  const icon = (n: any, u: number) => {
    const s = n.size || 1;
    const c = n.colour ? pal[n.colour] || n.colour : pal.ink;
    switch (n.shape) {
      case 'platform':
        return (
          <g>
            <rect x={-60 * s} y={-10 * s} width={120 * s} height={14 * s} fill={c} />
            {[-45, 0, 45].map((x) => <rect key={x} x={(x - 4) * s} y={4 * s} width={8 * s} height={50 * s} fill={c} />)}
            <polygon points={`${-5 * s},${-10 * s} ${15 * s},${-10 * s} ${5 * s},${-80 * s}`} fill="none" stroke={c} strokeWidth={4} />
            <circle cx={50 * s} cy={-40 * s} r={(9 + 3 * Math.sin(t * 8)) * s} fill={pal.accent} />
          </g>
        );
      case 'state':
        return (
          <g>
            <polygon points={`${-70 * s},${-30 * s} 0,${-75 * s} ${70 * s},${-30 * s}`} fill={c} />
            {[-50, -17, 17, 50].map((x) => <rect key={x} x={(x - 7) * s} y={-25 * s} width={14 * s} height={60 * s} fill={c} />)}
            <rect x={-75 * s} y={36 * s} width={150 * s} height={12 * s} fill={c} />
          </g>
        );
      case 'vault': {
        const spin = t * 40;
        return (
          <g>
            <rect x={-80 * s} y={-70 * s} width={160 * s} height={140 * s} rx={14 * s} fill={pal.bg2} stroke={pal.accent} strokeWidth={5} />
            <circle cx={0} cy={0} r={42 * s} fill="none" stroke={pal.accent} strokeWidth={5} />
            <g transform={`rotate(${spin})`}>
              {[0, 60, 120].map((a) => <line key={a} x1={0} y1={0} x2={34 * s * Math.cos((a * Math.PI) / 180)} y2={34 * s * Math.sin((a * Math.PI) / 180)} stroke={pal.accent} strokeWidth={5} />)}
            </g>
            <rect x={-80 * s} y={70 * s - 140 * s * (n.fill_u ?? u)} width={160 * s} height={140 * s * (n.fill_u ?? u)} rx={14 * s} fill={pal.accent} opacity={0.18} />
          </g>
        );
      }
      case 'globe': {
        const rot = (t * 25) % 360;
        return (
          <g>
            <circle r={70 * s} fill={pal.bg2} stroke={c} strokeWidth={4} />
            {[-40, 0, 40].map((lat) => <ellipse key={lat} cx={0} cy={lat * s * 0.9} rx={70 * s * Math.cos((lat * Math.PI) / 180)} ry={6 * s} fill="none" stroke={c} strokeOpacity={0.5} />)}
            {[0, 45, 90, 135].map((m) => {
              const rx = Math.abs(Math.cos(((m + rot) * Math.PI) / 180)) * 70 * s;
              return <ellipse key={m} cx={0} cy={0} rx={rx} ry={70 * s} fill="none" stroke={c} strokeOpacity={0.5} />;
            })}
          </g>
        );
      }
      case 'budget':
        return (
          <g>
            <rect x={-70 * s} y={-50 * s} width={140 * s} height={100 * s} rx={10 * s} fill={pal.bg2} stroke={c} strokeWidth={4} />
            {[-25, 0, 25].map((y, i) => <rect key={y} x={-45 * s} y={(y - 4) * s} width={(40 + 40 * ((i + 1) / 3)) * s} height={8 * s} fill={c} opacity={0.8} />)}
          </g>
        );
      default:
        return <rect x={-90 * s} y={-45 * s} width={180 * s} height={90 * s} rx={12 * s} fill={pal.bg2} stroke={c} strokeWidth={4} />;
    }
  };
  const links = (p.links || []).map((l: any, i: number) => {
    const a = nodes[l.from], b = nodes[l.to];
    const start = Math.max(cue(l, 0.2 + i * 0.15), appear(a), appear(b));
    const u = eio(t, start, 1.0);
    if (u <= 0) return null;
    const bend = l.bend ?? 0;
    const mx = (a.x + b.x) / 2 + bend * (b.y - a.y) * 0.3, my = (a.y + b.y) / 2 - bend * Math.abs(b.x - a.x) * 0.3;
    const B = (q: number): [number, number] => [(1 - q) ** 2 * a.x + 2 * (1 - q) * q * mx + q * q * b.x, (1 - q) ** 2 * a.y + 2 * (1 - q) * q * my + q * q * b.y];
    const pts = Array.from({length: 30}, (_, j) => B(((j / 29) * u * 0.78) + 0.11));
    const colour = l.colour ? pal[l.colour] || l.colour : pal.accent;
    const coins = u >= 1 ? Array.from({length: l.coins ?? 5}, (_, j) => {
      const q = 0.11 + 0.78 * (((t * (l.speed || 0.4)) + j / (l.coins ?? 5)) % 1);
      const [x, y] = B(q);
      return <circle key={j} cx={x} cy={y} r={l.coin_r || 8} fill={colour} stroke={pal.bg} strokeWidth={2} />;
    }) : null;
    const [lx, ly] = B(0.5);
    const head = pts[pts.length - 1], prev = pts[pts.length - 2];
    const ang = Math.atan2(head[1] - prev[1], head[0] - prev[0]);
    return (
      <g key={i}>
        <path d={'M' + pts.map((q) => q.join(',')).join(' L')} fill="none" stroke={colour} strokeWidth={l.width || 5} opacity={0.55} />
        <polygon points={`${head[0] + 14 * Math.cos(ang)},${head[1] + 14 * Math.sin(ang)} ${head[0] + 10 * Math.cos(ang + 2.4)},${head[1] + 10 * Math.sin(ang + 2.4)} ${head[0] + 10 * Math.cos(ang - 2.4)},${head[1] + 10 * Math.sin(ang - 2.4)}`} fill={colour} />
        {coins}
        {l.label && <text x={lx + (l.label_dx || 0)} y={ly - 20 + (l.label_dy || 0)} textAnchor="middle" fill={colour} fontFamily={font.body} fontWeight={700} fontSize={l.label_size || 28}
          opacity={eo(t, start + 0.8, 0.5)}>{l.label}</text>}
      </g>
    );
  });
  return (
    <svg width={W} height={H}>
      {p.title && <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={eo(t, 0.2, 0.5)}>{p.title}</text>}
      {links}
      {(p.nodes || []).map((n: any) => {
        const at = appear(n);
        const u = easeBack(prog(t, at, 0.7));
        if (u <= 0) return null;
        const bob = Math.sin(t * 1.4 + n.x * 0.01) * 4;
        return (
          <g key={n.id} transform={`translate(${n.x} ${n.y + bob}) scale(${u})`}>
            {icon(n, eo(t, at, 4))}
            <text x={0} y={(n.label_dy ?? 110) * (n.size || 1)} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={30}>{n.label}</text>
            {n.sublabel && <text x={0} y={(n.label_dy ?? 110) * (n.size || 1) + 38} textAnchor="middle" fill={n.sub_colour ? pal[n.sub_colour] : pal.muted} fontFamily={font.body} fontSize={26}>{n.sublabel}</text>}
          </g>
        );
      })}
      {p.caption && <text x={W / 2} y={H - 130} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={46}
        opacity={eo(t, cue(p.caption_cue, 0.75), 0.6)}>{p.caption}</text>}
    </svg>
  );
};

export const _lerp = lerp;
