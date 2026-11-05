import React from 'react';
import {easeBack, eo, lerp, prog, rand, useCtx} from '../lib/anim';
import {RiseText, } from '../components/Chrome';
import {mixHex} from './Platform';

const TW = 120, TH = 60; // tile size (2:1 isometric)

/**
 * Isometric diorama that builds itself on narration cues. Tiles: land / water. Objects rise into place
 * and keep moving: boats bob, ship slides, factory smoke drifts, dam water flows, turbines spin,
 * towers light up, train moves. Camera drifts and zooms gently (2.5D).
 */
export const Isometric: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const cols = p.cols || 8, rows = p.rows || 8;
  const water: number[][] = p.water || [];
  const isWater = (x: number, y: number) => water.some(([a, b]) => a === x && b === y) || (p.water_from_x !== undefined && x >= p.water_from_x);
  const iso = (gx: number, gy: number, z = 0): [number, number] => [(gx - gy) * (TW / 2), (gx + gy) * (TH / 2) - z];
  const zoom = lerp(p.zoom_start || 1.05, p.zoom_end || 1.2, eo(t, 0, scene.duration));
  const panX = Math.sin(t * 0.12) * 30;
  const top = (c: string) => c, left = (c: string) => mixHex(c, '#000000', 0.25), right = (c: string) => mixHex(c, '#000000', 0.45);

  const box = (gx: number, gy: number, w: number, d: number, h: number, c: string, key: string, rise = 1) => {
    const hh = h * rise;
    const [ax, ay] = iso(gx, gy, hh), [bx, by] = iso(gx + w, gy, hh), [cx, cy] = iso(gx + w, gy + d, hh), [dx, dy] = iso(gx, gy + d, hh);
    const [bx0, by0] = iso(gx + w, gy, 0), [cx0, cy0] = iso(gx + w, gy + d, 0), [dx0, dy0] = iso(gx, gy + d, 0);
    return (
      <g key={key}>
        <polygon points={`${dx},${dy} ${cx},${cy} ${cx0},${cy0} ${dx0},${dy0}`} fill={left(c)} />
        <polygon points={`${cx},${cy} ${bx},${by} ${bx0},${by0} ${cx0},${cy0}`} fill={right(c)} />
        <polygon points={`${ax},${ay} ${bx},${by} ${cx},${cy} ${dx},${dy}`} fill={top(c)} />
      </g>
    );
  };

  const tiles: React.ReactNode[] = [];
  for (let y = 0; y < rows; y++) for (let x = 0; x < cols; x++) {
    const w = isWater(x, y);
    const [ax, ay] = iso(x, y), [bx, by] = iso(x + 1, y), [cx, cy] = iso(x + 1, y + 1), [dx, dy] = iso(x, y + 1);
    const shimmer = w ? 0.08 * Math.sin(t * 2 + x + y) : 0;
    tiles.push(<polygon key={`t${x}-${y}`} points={`${ax},${ay} ${bx},${by} ${cx},${cy} ${dx},${dy}`}
      fill={w ? mixHex(pal.bg2, pal.accent2 || pal.ink, 0.12 + shimmer) : mixHex(pal.land, pal.ink, 0.06)} stroke={pal.bg} strokeWidth={1.5} />);
  }

  const objs = (p.objects || []).map((o: any, i: number) => {
    const at = cue(o, 0.05 + i * 0.08);
    const rise = easeBack(prog(t, at, 0.8));
    if (rise <= 0) return null;
    const k = `o${i}`;
    const [ox, oy] = iso(o.x + 0.5, o.y + 0.5);
    const lab = o.label ? (
      <text x={ox} y={oy - (o.label_h || 150)} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={24}
        opacity={eo(t, at + 0.4, 0.4)}>{o.label}</text>
    ) : null;
    switch (o.kind) {
      case 'house':
        return <g key={k}>{box(o.x + 0.2, o.y + 0.2, 0.6, 0.6, 40, pal.ink, k + 'b', rise)}{lab}</g>;
      case 'tower': {
        const h = (o.h || 160) * rise;
        const lit = Array.from({length: Math.floor(h / 24)}, (_, j) => (
          <rect key={j} x={ox - 6 + (j % 2) * 18} y={oy - 30 - j * 22} width={8} height={6} fill={pal.accent} opacity={rand(j + i + Math.floor(t * 1.5)) > 0.4 ? 0.9 : 0.2} />
        ));
        return <g key={k}>{box(o.x + 0.15, o.y + 0.15, 0.7, 0.7, o.h || 160, o.colour ? pal[o.colour] : mixHex(pal.border, pal.ink, 0.2), k + 'b', rise)}{lit}{lab}</g>;
      }
      case 'factory': {
        const smoke = Array.from({length: 5}, (_, j) => {
          const q = ((t * 0.35 + j / 5) % 1);
          return <circle key={j} cx={ox + 22 + q * 40} cy={oy - 150 - q * 120} r={10 + q * 22} fill={pal.muted} opacity={(1 - q) * 0.35 * rise} />;
        });
        return <g key={k}>{box(o.x + 0.05, o.y + 0.1, 0.9, 0.8, 60, mixHex(pal.border, pal.ink, 0.25), k + 'b', rise)}
          {box(o.x + 0.6, o.y + 0.2, 0.18, 0.18, 150, pal.muted, k + 'c', rise)}{smoke}{lab}</g>;
      }
      case 'boat': {
        const bob = Math.sin(t * 2.2 + i) * 4;
        const drift = Math.sin(t * 0.4 + i) * 18;
        return (
          <g key={k} transform={`translate(${ox + drift} ${oy + bob}) scale(${rise})`}>
            <polygon points="-36,-6 36,-6 26,10 -28,10" fill={mixHex(pal.ink, pal.border, 0.3)} />
            <line x1={0} y1={-6} x2={0} y2={-56} stroke={pal.ink} strokeWidth={3} />
            <polygon points="2,-54 28,-14 2,-14" fill={pal.accent} opacity={0.9} />
            {lab && <text x={0} y={-80} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={24}>{o.label}</text>}
          </g>
        );
      }
      case 'ship': {
        const slide = ((t * (o.speed || 18)) % 260) - 130;
        const [sx, sy] = iso(o.x + 0.5 + slide / 120, o.y + 0.5);
        return (
          <g key={k} transform={`translate(${sx} ${sy + Math.sin(t * 1.6) * 3}) scale(${rise})`}>
            <polygon points="-90,-10 70,-10 95,4 70,20 -80,20" fill={mixHex(pal.border, pal.ink, 0.35)} />
            {[-70, -40, -10, 20].map((x, j) => <rect key={j} x={x} y={-30} width={26} height={20} fill={[pal.accent, pal.ink, pal.muted, pal.accent][j]} opacity={0.9} />)}
            <rect x={44} y={-48} width={22} height={38} fill={pal.ink} />
            {lab && <text x={0} y={-70} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={24}>{o.label}</text>}
          </g>
        );
      }
      case 'dam': {
        const flows = Array.from({length: 6}, (_, j) => {
          const q = ((t * 0.8 + j / 6) % 1);
          return <rect key={j} x={ox - 40 + j * 14} y={oy - 30 + q * 60} width={6} height={14} fill={pal.ink} opacity={(1 - q) * 0.7 * rise} />;
        });
        return <g key={k}>{box(o.x, o.y + 0.3, 1, 0.4, 90, pal.muted, k + 'b', rise)}{flows}{lab}</g>;
      }
      case 'turbine': {
        const [tx, ty] = iso(o.x + 0.5, o.y + 0.5, 0);
        const h = 170 * rise;
        const ang = t * 120 + i * 40;
        return (
          <g key={k}>
            <line x1={tx} y1={ty} x2={tx} y2={ty - h} stroke={pal.ink} strokeWidth={6} />
            <g transform={`translate(${tx} ${ty - h}) rotate(${ang})`} opacity={rise}>
              {[0, 120, 240].map((a) => <line key={a} x1={0} y1={0} x2={70 * Math.cos((a * Math.PI) / 180)} y2={70 * Math.sin((a * Math.PI) / 180)} stroke={pal.ink} strokeWidth={6} strokeLinecap="round" />)}
              <circle r={7} fill={pal.accent} />
            </g>
            {lab}
          </g>
        );
      }
      case 'tank':
        return <g key={k}>{box(o.x + 0.2, o.y + 0.2, 0.6, 0.6, 70, pal.accent, k + 'b', rise)}{lab}</g>;
      case 'coin': {
        const [cx0, cy0] = iso(o.x + 0.5, o.y + 0.5, 0);
        const stack = Math.round((o.n || 6) * rise);
        return <g key={k}>{Array.from({length: stack}, (_, j) => <ellipse key={j} cx={cx0} cy={cy0 - j * 12} rx={34} ry={14} fill={j === stack - 1 ? pal.accent : mixHex(pal.accent, '#000000', 0.3)} stroke={pal.bg} />)}{lab}</g>;
      }
      default:
        return null;
    }
  });
  const [gx0, gy0] = iso(cols / 2, rows / 2);
  return (
    <svg width={W} height={H}>
      <g transform={`translate(${W * (p.cx || 0.62) + panX - gx0 * zoom} ${H * (p.cy || 0.5) - gy0 * zoom}) scale(${zoom})`}>
        {tiles}
        {objs}
      </g>
      {p.kicker && <RiseText x={120} y={210} at={cue(p.kicker_cue, 0)} size={28} color={pal.accent} weight={600} tracking={6}>{String(p.kicker).toUpperCase()}</RiseText>}
      {p.title && <RiseText x={120} y={300} at={cue(p.title_cue, 0.02)} size={72} weight={700} display>{p.title}</RiseText>}
      {(p.notes || []).map((n: any, i: number) => (
        <RiseText key={i} x={124} y={390 + i * 62} at={cue(n, 0.2 + i * 0.2)} size={36} color={n.colour ? pal[n.colour] : pal.ink}>{n.text}</RiseText>
      ))}
    </svg>
  );
};
