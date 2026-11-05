import React, {useMemo} from 'react';
import {easeBack, eio, eo, lerp, prog, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';
import {useGeo} from '../lib/geo';

const S = 4096; // Mercator world size used by tools/build_remotion_geo.py
export const merc = (lon: number, lat: number): [number, number] => {
  const x = ((lon + 180) / 360) * S;
  const phi = (Math.max(-85, Math.min(85, lat)) * Math.PI) / 180;
  const y = S / 2 - (S / (2 * Math.PI)) * Math.log(Math.tan(Math.PI / 4 + phi / 2));
  return [x, y];
};

type View = {lon: number; lat: number; span: number};

type Ring = {pts: Float64Array; x0: number; y0: number; x1: number; y1: number};
const PARSED = new Map<string, Record<string, Ring[]>>();
/** Parse 'Mx,y x,y ...Z' world-unit paths once per layer into typed arrays with bounding boxes. */
export const parseLayer = (name: string, paths: Record<string, string>) => {
  const hit = PARSED.get(name);
  if (hit) return hit;
  const out: Record<string, Ring[]> = {};
  for (const [code, d] of Object.entries(paths)) {
    out[code] = d.split('M').filter(Boolean).map((r) => {
      const nums = r.replace('Z', '').trim().split(/[ ,]/).map(Number);
      const pts = new Float64Array(nums);
      let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
      for (let i = 0; i < pts.length; i += 2) {
        x0 = Math.min(x0, pts[i]); x1 = Math.max(x1, pts[i]); y0 = Math.min(y0, pts[i + 1]); y1 = Math.max(y1, pts[i + 1]);
      }
      return {pts, x0, y0, x1, y1};
    });
  }
  PARSED.set(name, out);
  return out;
};

/** Screen-space path for the current camera: cull off-screen rings, clamp to a margin, drop sub-pixel steps.
 * (Scaling world-unit paths with an SVG transform made Chrome rasterise enormous geometry: ~4 s/frame.) */
export const screenPath = (rings: Ring[], cx: number, cy: number, k: number, ox: number, oy: number, W: number, H: number) => {
  const m = 60;
  let d = '';
  for (const r of rings) {
    const sx0 = (r.x0 - cx) * k + ox, sx1 = (r.x1 - cx) * k + ox, sy0 = (r.y0 - cy) * k + oy, sy1 = (r.y1 - cy) * k + oy;
    if (sx1 < -m || sx0 > W + m || sy1 < -m || sy0 > H + m) continue;
    if ((sx1 - sx0) < 0.8 && (sy1 - sy0) < 0.8) continue;
    let lx = NaN, ly = NaN, n = 0, seg = '';
    for (let i = 0; i < r.pts.length; i += 2) {
      let x = (r.pts[i] - cx) * k + ox, y = (r.pts[i + 1] - cy) * k + oy;
      x = x < -m ? -m : x > W + m ? W + m : x;
      y = y < -m ? -m : y > H + m ? H + m : y;
      if (n && Math.abs(x - lx) + Math.abs(y - ly) < 1.2) continue;
      seg += (n ? ' ' : 'M') + x.toFixed(1) + ',' + y.toFixed(1);
      lx = x; ly = y; n++;
    }
    if (n >= 3) d += seg + 'Z';
  }
  return d;
};

/**
 * Camera-driven vector map. Countries are pre-projected paths; the camera interpolates between views
 * (optionally keyed to narration cues). Layers: highlighted countries, field markers with pulses,
 * animated routes (pipelines/tanker lanes) with moving packets, curved flow arcs (e.g. investment
 * flows) with particles, and free labels.
 */
export const MapScene: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const geo = useGeo(p.geo || 'europe');
  const rings = useMemo(() => parseLayer(p.geo || 'europe', geo.paths), [geo, p.geo]);
  const views: (View & {cue?: any; at?: number})[] = p.views || [p.start_view, p.end_view].filter(Boolean);
  // camera: hop between successive views, each move eased over `move` seconds
  let v: View = views[0];
  for (let i = 1; i < views.length; i++) {
    const start = views[i].cue !== undefined || views[i].at !== undefined ? cue(views[i], 0) : scene.lead + (i / views.length) * scene.speech * 0.6;
    const u = eio(t, start, p.move || 2.6);
    const prev = v;
    v = {lon: lerp(prev.lon, views[i].lon, u), lat: lerp(prev.lat, views[i].lat, u),
      span: Math.exp(lerp(Math.log(prev.span), Math.log(views[i].span), u))};
  }
  const drift = Math.sin(t * 0.25) * 0.004 * v.span;
  const [cx, cy] = merc(v.lon + drift, v.lat);
  const k = W / ((v.span / 360) * S);
  const toScreen = (lon: number, lat: number): [number, number] => {
    const [x, y] = merc(lon, lat);
    return [(x - cx) * k + W * (p.anchor_x ?? 0.5), (y - cy) * k + H * (p.anchor_y ?? 0.52)];
  };
  const fills: Record<string, string> = {};
  for (const [code, spec] of Object.entries<any>(p.highlights || {})) {
    const u = eio(t, cue(spec, 0.05), 0.9);
    fills[code] = mixHex2(pal.land, pal[spec.colour || 'accent'] || spec.colour, u * (spec.strength ?? 1));
  }
  const routeEls = (p.routes || []).map((r: any, i: number) => {
    const pts = r.points.map((q: [number, number]) => toScreen(q[0], q[1]));
    const segs: number[] = [];
    let len = 0;
    for (let j = 1; j < pts.length; j++) { len += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]); segs.push(len); }
    const start = cue(r, 0.2 + i * 0.1);
    const u = eio(t, start, r.seconds || 1.8);
    if (u <= 0) return null;
    const at = (d: number): [number, number] => {
      let j = segs.findIndex((s) => s >= d);
      if (j < 0) j = segs.length - 1;
      const s0 = j ? segs[j - 1] : 0;
      const f = (d - s0) / Math.max(1e-6, segs[j] - s0);
      return [lerp(pts[j][0], pts[j + 1][0], f), lerp(pts[j][1], pts[j + 1][1], f)];
    };
    const d = 'M' + pts.map((q: number[]) => q.join(',')).join(' L');
    const colour = pal[r.colour || 'accent'] || r.colour;
    const packets = u >= 1 ? Array.from({length: r.packets ?? 5}, (_, n) => {
      const q = at(((t * (r.speed || 0.18) + n / (r.packets ?? 5)) % 1) * len);
      return <circle key={n} cx={q[0]} cy={q[1]} r={r.kind === 'tanker' ? 0 : 5} fill={pal.ink} opacity={0.9} />;
    }) : null;
    const tanker = r.kind === 'tanker' && u >= 1 ? (() => {
      const f = (t * (r.speed || 0.06)) % 1;
      const q = at(f * len), q2 = at(Math.min(len, f * len + 2));
      const ang = (Math.atan2(q2[1] - q[1], q2[0] - q[0]) * 180) / Math.PI;
      return <g transform={`translate(${q[0]} ${q[1]}) rotate(${ang})`}><polygon points="-16,-6 12,-6 20,0 12,6 -16,6" fill={pal.ink} /></g>;
    })() : null;
    const end = pts[pts.length - 1];
    return (
      <g key={i}>
        <path d={d} fill="none" stroke={colour} strokeWidth={r.width || 5} strokeLinecap="round" strokeLinejoin="round"
          strokeDasharray={r.dashed ? '14 10' : `${len}`} strokeDashoffset={r.dashed ? -t * 30 : len * (1 - u)} opacity={0.95} />
        {packets}
        {tanker}
        {r.label && <text x={end[0] + (r.anchor === 'end' ? -16 : 16)} y={end[1] + 8} textAnchor={r.anchor === 'end' ? 'end' : 'start'}
          fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={24} letterSpacing={2} opacity={eo(t, start + (r.seconds || 1.8), 0.5)}>{String(r.label).toUpperCase()}</text>}
      </g>
    );
  });
  const arcEls = (p.arcs || []).map((a: any, i: number) => {
    const [ox, oy] = toScreen(p.origin.lon, p.origin.lat);
    const [dx, dy] = toScreen(a.lon, a.lat);
    const mx = (ox + dx) / 2, my = (oy + dy) / 2 - Math.hypot(dx - ox, dy - oy) * (a.lift ?? 0.28);
    const start = cue(a, 0.15 + i * 0.12);
    const u = eio(t, start, 1.2);
    if (u <= 0) return null;
    const B = (q: number): [number, number] => [(1 - q) ** 2 * ox + 2 * (1 - q) * q * mx + q * q * dx, (1 - q) ** 2 * oy + 2 * (1 - q) * q * my + q * q * dy];
    const n = 40;
    const ptsA = Array.from({length: Math.max(2, Math.round(n * u))}, (_, j) => B((j / (n - 1)) * u));
    const parts = u >= 1 ? Array.from({length: 4}, (_, j) => {
      const q = B(((t * 0.35 + j / 4) % 1));
      return <circle key={j} cx={q[0]} cy={q[1]} r={4} fill={pal.accent} />;
    }) : null;
    const bub = easeBack(prog(t, start + 1.1, 0.6));
    return (
      <g key={i}>
        <path d={'M' + ptsA.map((q) => q.join(',')).join(' L')} fill="none" stroke={pal.accent} strokeWidth={3} opacity={0.8} />
        {parts}
        <circle cx={dx} cy={dy} r={(a.r || 22) * bub} fill={pal.accent} opacity={0.25} />
        <circle cx={dx} cy={dy} r={7 * bub} fill={pal.accent} />
        {a.label && <text x={dx} y={dy - (a.r || 22) - 14} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700}
          fontSize={26} opacity={bub}>{a.label}</text>}
        {a.value && <text x={dx} y={dy + (a.r || 22) + 34} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={700}
          fontSize={34} opacity={bub}>{a.value}</text>}
      </g>
    );
  });
  const markerEls = (p.markers || []).map((m: any, i: number) => {
    const [x, y] = toScreen(m.lon, m.lat);
    const start = cue(m, 0.3 + i * 0.1);
    const u = easeBack(prog(t, start, 0.6));
    if (u <= 0) return null;
    const ring = prog(t, start, 1.6);
    const pulse = ((t - start) % 1.8) / 1.8;
    return (
      <g key={i}>
        <circle cx={x} cy={y} r={10 + 40 * pulse} fill="none" stroke={pal.accent} strokeWidth={2} opacity={(1 - pulse) * 0.8} />
        <circle cx={x} cy={y} r={11 * u} fill={pal.accent} stroke={pal.bg} strokeWidth={3} />
        <text x={x + (m.anchor === 'end' ? -22 : 22)} y={y + 9} textAnchor={m.anchor === 'end' ? 'end' : 'start'} fill={pal.ink}
          fontFamily={font.display} fontWeight={700} fontSize={m.size || 38} opacity={ring > 0.1 ? 1 : 0}>{m.label}</text>
        {m.sublabel && <text x={x + (m.anchor === 'end' ? -22 : 22)} y={y + 44} textAnchor={m.anchor === 'end' ? 'end' : 'start'} fill={pal.muted}
          fontFamily={font.body} fontSize={26} opacity={eo(t, start + 0.4, 0.4)}>{m.sublabel}</text>}
      </g>
    );
  });
  const labelEls = (p.labels || []).map((l: any, i: number) => {
    const [x, y] = toScreen(l.lon, l.lat);
    return <text key={i} x={x} y={y} textAnchor="middle" fill={pal[l.colour || 'muted'] || l.colour} fontFamily={font.body} fontWeight={600}
      fontSize={l.size || 24} letterSpacing={4} opacity={eo(t, cue(l, 0.1), 0.6) * (l.opacity ?? 0.9)}>{String(l.text).toUpperCase()}</text>;
  });
  return (
    <svg width={W} height={H}>
      <rect width={W} height={H} fill={pal.bg} />
      {Object.entries(rings).map(([code, rs]) => {
        const d = screenPath(rs, cx, cy, k, W * (p.anchor_x ?? 0.5), H * (p.anchor_y ?? 0.52), W, H);
        return d ? <path key={code} d={d} fill={fills[code] || pal.land} stroke={pal.border} strokeWidth={1.1} /> : null;
      })}
      {labelEls}
      {routeEls}
      {arcEls}
      {markerEls}
      {p.title && <RiseText x={120} y={210} at={cue(p.title_cue, 0)} size={64} weight={700} display>{p.title}</RiseText>}
      {p.subtitle && <RiseText x={122} y={258} at={cue(p.subtitle_cue, 0.05)} size={30} color={pal.muted}>{p.subtitle}</RiseText>}
      {(p.callouts || []).map((c: any, i: number) => {
        const at = cue(c, 0.3 + i * 0.2);
        const u = eo(t, at, 0.6);
        const y = (p.callout_y || 330) + i * 150;
        const x = p.callout_x || 1360;
        return (
          <g key={i} opacity={u} transform={`translate(${50 * (1 - u)} 0)`}>
            <rect x={x - 40} y={y - 20} width={Math.max(420, String(c.label).length * 15, String(c.value || '').length * 40) + 40}
              height={c.value ? 150 : 76} rx={10} fill={pal.bg} opacity={0.82} />
            <rect x={x - 24} y={y - 4} width={5} height={c.value ? 120 : 50} fill={pal.accent} />
            <text x={x} y={y + 22} fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={24} letterSpacing={3}>{String(c.label).toUpperCase()}</text>
            {c.value && <text x={x} y={y + 100} fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={72}>{c.value}</text>}
          </g>
        );
      })}
    </svg>
  );
};

export const mixHex2 = (a: string, b: string, u: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [x, y] = [p(a), p(b)];
  return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * u).toString(16).padStart(2, '0')).join('');
};
