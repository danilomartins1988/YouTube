import React from 'react';
import {E, FONT, clamp, col, lerp, pal, springAt, win} from '../motion';
import type {Themed, Vec} from '../types';

/**
 * ExplodedDiagram: a layered object in a rotatable isometric camera. Layers separate along the vertical
 * axis with staggered springs, turn slightly to show their faces, get labelled with leader lines, then
 * reassemble with overshoot-and-settle. Each layer kind has procedural surface detail.
 *
 * It is a SCHEMATIC (conceptual roles), not a to-scale physical cross-section; say so with `note`.
 */
export type LayerKind = 'substrate' | 'bumps' | 'die' | 'interconnect' | 'lid' | 'plain';
export type Layer = {label: string; sub?: string; kind: LayerKind; color?: string; thickness?: number; size?: number};

export type ExplodedDiagramProps = Themed & {
  t: number;
  layers: Layer[];          // bottom -> top
  cx?: number; cy?: number;
  /** world units -> px */
  scale?: [number, number][];        // camera distance keyframes [[t, scale], ...]
  yaw?: [number, number][];          // camera orbit keyframes [[t, degrees], ...]
  pitch?: number;                    // 0..1 (0.5 = classic isometric)
  explodeAt: number; explodeGap?: number; stagger?: number;
  assembleAt: number;
  labelsAt?: number;
  note?: string;
  opacity?: number;
  fps?: number;
};

const keyAt = (k: [number, number][] | undefined, t: number, d: number) => {
  if (!k || !k.length) return d;
  let v = k[0][1];
  for (let i = 1; i < k.length; i++) if (t >= k[i - 1][0]) v = t >= k[i][0] ? k[i][1] : lerp(k[i - 1][1], k[i][1], E.inOut(win(t, k[i - 1][0], k[i][0] - k[i - 1][0])));
  return v;
};

export const ExplodedDiagram: React.FC<ExplodedDiagramProps> = (p) => {
  const P = pal(p.palette);
  const {t, layers, cx = 960, cy = 600, pitch = 0.52, explodeGap = 70, stagger = 0.12, opacity = 1, fps = 30} = p;
  const S = keyAt(p.scale, t, 1);
  const yawDeg = keyAt(p.yaw, t, 35);
  // per-layer separation: spring out (staggered bottom->top), spring back in reverse order
  const sep = layers.map((_, i) => {
    const out = springAt(t, p.explodeAt + i * stagger, fps, {damping: 11, stiffness: 90});
    const back = springAt(t, p.assembleAt + (layers.length - 1 - i) * stagger * 0.6, fps, {damping: 9, stiffness: 140});
    return out - back;
  });
  // stack the bottoms of the assembled layers
  let zAcc = 0;
  const base = layers.map((L) => { const z = zAcc; zAcc += L.thickness ?? 10; return z; });
  // keep the (exploding) stack centred on cy: offset by the current mid-height of all layers
  const zTops = layers.map((L, i) => base[i] + sep[i] * explodeGap * i + (L.thickness ?? 10));
  const zMid = (Math.min(...base) + Math.max(...zTops)) / 2;
  const proj = (x: number, y: number, z: number, yaw: number): Vec => {
    const a = (yaw * Math.PI) / 180;
    const rx = x * Math.cos(a) - y * Math.sin(a), ry = x * Math.sin(a) + y * Math.cos(a);
    return [cx + rx * S, cy + (ry * pitch - (z - zMid)) * S];
  };
  const labelsU = E.out(win(t, p.labelsAt ?? p.explodeAt + 0.7, 0.5)) * (1 - E.in(win(t, p.assembleAt - 0.4, 0.4)));
  const faces: React.ReactNode[] = [];
  const labels: React.ReactNode[] = [];
  layers.forEach((L, i) => {
    const a = (L.size ?? 200) / 2, h = L.thickness ?? 10;
    const z0 = base[i] + sep[i] * explodeGap * i;
    const yaw = yawDeg + sep[i] * (i % 2 ? 7 : -7);        // each layer turns a little while exploded
    const c = col(P, L.color, P.blue);
    const corners: Vec[] = [[-a, -a], [a, -a], [a, a], [-a, a]];
    const top = corners.map(([x, y]) => proj(x, y, z0 + h, yaw));
    const bot = corners.map(([x, y]) => proj(x, y, z0, yaw));
    const poly = (q: Vec[]) => q.map((v) => v[0].toFixed(1) + ',' + v[1].toFixed(1)).join(' ');
    // side faces facing the viewer (outward normal rotated has +y screen component)
    const sides: React.ReactNode[] = [];
    for (let k = 0; k < 4; k++) {
      const k2 = (k + 1) % 4;
      const mxl = (corners[k][0] + corners[k2][0]) / 2, myl = (corners[k][1] + corners[k2][1]) / 2;
      const ang = (yaw * Math.PI) / 180;
      const ny = mxl * Math.sin(ang) + myl * Math.cos(ang);
      if (ny <= 0) continue;
      sides.push(<polygon key={k} points={poly([top[k], top[k2], bot[k2], bot[k]])} fill={c} fillOpacity={k % 2 ? 0.55 : 0.4} stroke={c} strokeWidth={1.5} />);
    }
    // surface detail on the top face (local coords -> projected)
    const at = (u: number, v: number): Vec => proj(lerp(-a, a, u), lerp(-a, a, v), z0 + h + 0.5, yaw);
    const detail: React.ReactNode[] = [];
    const ln = (u0: number, v0: number, u1: number, v1: number, key: string, w = 1.6, op = 0.7, cc = P.ink) => {
      const A = at(u0, v0), B = at(u1, v1);
      detail.push(<line key={key} x1={A[0]} y1={A[1]} x2={B[0]} y2={B[1]} stroke={cc} strokeWidth={w} strokeOpacity={op} />);
    };
    if (L.kind === 'die') {
      for (let g = 1; g < 6; g++) { ln(g / 6, 0.06, g / 6, 0.94, 'v' + g, 1.2, 0.45); ln(0.06, g / 6, 0.94, g / 6, 'h' + g, 1.2, 0.45); }
      // a few 'cores' light up in sequence
      for (let q = 0; q < 6; q++) { const u = (q % 3) / 3 + 0.08, v = Math.floor(q / 3) / 3 + 0.25, on = Math.sin(t * 4 + q * 1.3) > 0.3;
        detail.push(<polygon key={'c' + q} points={poly([at(u, v), at(u + 0.22, v), at(u + 0.22, v + 0.22), at(u, v + 0.22)])} fill={on ? P.gold : c} fillOpacity={on ? 0.55 : 0.25} />); }
    } else if (L.kind === 'interconnect') {
      for (let g = 0; g < 9; g++) { const v = 0.08 + g * 0.105; ln(0.05, v, 0.95, v, 'm' + g, 2, 0.8, g % 2 ? P.gold : P.ink); }
      for (let g = 0; g < 5; g++) ln(0.15 + g * 0.18, 0.08, 0.15 + g * 0.18, 0.92, 'x' + g, 1.4, 0.5);
    } else if (L.kind === 'bumps') {
      for (let iu = 0; iu < 8; iu++) for (let iv = 0; iv < 8; iv++) { const q = at(0.08 + iu * 0.12, 0.08 + iv * 0.12);
        detail.push(<ellipse key={iu + '-' + iv} cx={q[0]} cy={q[1]} rx={4.5 * S} ry={4.5 * S * pitch} fill={P.ink} fillOpacity={0.85} />); }
    } else if (L.kind === 'substrate') {
      for (let g = 0; g < 6; g++) { ln(0.1, 0.1 + g * 0.16, 0.5, 0.1 + g * 0.16, 's' + g, 2, 0.6, P.teal); ln(0.5, 0.1 + g * 0.16, 0.9, 0.18 + g * 0.14, 'd' + g, 2, 0.6, P.teal); }
    } else if (L.kind === 'lid') {
      const sh = ((t * 0.35) % 1.6) - 0.3;     // moving sheen across the metal
      detail.push(<polygon key="sheen" points={poly([at(clamp(sh), 0), at(clamp(sh + 0.18), 0), at(clamp(sh + 0.05), 1), at(clamp(sh - 0.13), 1)])} fill="#fff" fillOpacity={0.18} />);
    }
    faces.push(<g key={i}>
      {sides}
      <polygon points={poly(top)} fill={P.panel} stroke={c} strokeWidth={2.5} />
      <polygon points={poly(top)} fill={c} fillOpacity={L.kind === 'lid' ? 0.55 : 0.22} />
      {detail}
    </g>);
    if (labelsU > 0) {
      const anchor = top[1][0] > top[2][0] ? top[1] : top[2];
      const lx = cx + 380 * Math.max(0.8, S * 0.9), ly = (top[0][1] + top[2][1]) / 2;
      labels.push(<g key={'l' + i} opacity={labelsU}>
        <path d={`M ${anchor[0]} ${anchor[1]} L ${lerp(anchor[0], lx - 20, labelsU)} ${ly}`} stroke={c} strokeWidth={2} fill="none" />
        <circle cx={anchor[0]} cy={anchor[1]} r={5} fill={c} />
        <text x={lx} y={ly + 2} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={28}>{L.label}</text>
        {L.sub && <text x={lx} y={ly + 30} fill={P.muted} fontFamily={FONT.body} fontSize={20}>{L.sub}</text>}
      </g>);
    }
  });
  const merged = 1 - Math.max(...sep.map((s) => clamp(s)));
  const flash = Math.sin(Math.PI * win(t, p.assembleAt + layers.length * stagger * 0.6 + 0.2, 0.6));
  const shadow = proj(0, 0, -6, yawDeg);
  return (
    <g opacity={opacity}>
      <ellipse cx={shadow[0]} cy={shadow[1] + 30 * S} rx={190 * S} ry={70 * S} fill="#000" opacity={0.35 + 0.1 * merged} />
      {faces}
      {flash > 0 && <circle cx={cx} cy={cy - 20 * S} r={260 * S} fill={P.gold} opacity={0.12 * flash} />}
      {labels}
      {p.note && <text x={80} y={1030} fill={P.muted} fontFamily={FONT.body} fontSize={20} letterSpacing={1}>{p.note}</text>}
    </g>
  );
};
