import React, {useMemo} from 'react';
import {merc, parseLayer, screenPath} from '../../scenes/MapScene';
import {E, FONT, clamp, col, lerp, pal, quadPt, quadTan, rnd, win} from '../motion';
import type {LonLat, Themed, Vec, WorldGeo} from '../types';

/**
 * AnimatedWorldMap: real country outlines (Natural Earth 1:50m, public domain) on a Web-Mercator camera.
 *
 * - camera keyframes (lon, lat, span in degrees of longitude) with eased moves between them; the world is drawn
 *   three times (-360°, 0, +360°) so the camera can cross the Pacific and routes take the short way round
 * - country highlights that fade in on time; hubs that pop in with a label and pulse
 * - routes that DRAW along a great-arc-like bow, then carry moving tokens (data packets, boxes, chips, coins)
 * - depth: a star/particle layer with parallax, an optional perspective tilt, vignette
 * Positions come only from the lon/lat you pass; nothing is placed by guesswork.
 */
export type MapCamera = {at: number; lon: number; lat: number; span: number; dur?: number};
export type MapHighlight = {iso: string; color?: string; at: number; dur?: number; strength?: number};
export type MapHub = {id: string; at: LonLat; label: string; sub?: string; color?: string; time: number; anchor?: 'start' | 'end'};
export type TokenShape = 'packet' | 'box' | 'chip' | 'coin' | 'dot';
export type MapRoute = {
  from: LonLat; to: LonLat; at: number; dur?: number; color?: string; lift?: number;
  tokens?: number; tokenShape?: TokenShape; tokenEvery?: number; tokenSpeed?: number; label?: string; width?: number;
  /** a blocked route draws part of the way, stops at a red barrier and carries no tokens (export bans, closures) */
  blocked?: boolean;
};

export type AnimatedWorldMapProps = Themed & {
  t: number;
  geo: WorldGeo;
  width?: number; height?: number;
  cameras: MapCamera[];
  highlights?: MapHighlight[];
  hubs?: MapHub[];
  routes?: MapRoute[];
  /** perspective tilt in degrees over time: [[t, deg], ...] (CSS 3D on the map plane) */
  tilt?: [number, number][];
  parallax?: boolean;
  opacity?: number;
  caption?: string;
};

const WS = 4096;

/** Camera state at time t: holds each keyframe, then eases to the next one over its `dur` (default 1.6 s),
 * zooming in log space so wide <-> narrow moves feel even. */
export const cameraAt = (cams: MapCamera[], t: number) => {
  let c = cams[0];
  for (let i = 1; i < cams.length; i++) {
    const b = cams[i], dur = b.dur ?? 1.6;
    if (t < b.at) break;
    if (t <= b.at + dur) {
      const w = win(t, b.at, dur), u = E.inOut(w), uc = E.inOut(clamp(w * 1.45));   // the centre arrives first, then the zoom settles
      return {lon: lerp(c.lon, b.lon, uc), lat: lerp(c.lat, b.lat, uc), span: Math.exp(lerp(Math.log(c.span), Math.log(b.span), u))};
    }
    c = b;
  }
  return {lon: c.lon, lat: c.lat, span: c.span};
};

const unwrapTo = (ref: number, lon: number) => { let L = lon; while (L - ref > 180) L -= 360; while (L - ref < -180) L += 360; return L; };
/** raw mercator x without the [-180,180] wrap (merc is linear in lon) */
const mx = (lon: number) => ((lon + 180) / 360) * WS;

export const Token: React.FC<{shape: TokenShape; x: number; y: number; ang: number; c: string; s?: number}> = ({shape, x, y, ang, c, s = 1}) => {
  const deg = (ang * 180) / Math.PI;
  if (shape === 'coin') return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <circle r={13} fill={c} stroke="#7A5A1C" strokeWidth={2} /><text y={6.5} textAnchor="middle" fontFamily={FONT.body} fontWeight={900} fontSize={18} fill="#3B2A0A">$</text>
    </g>);
  if (shape === 'box') return (
    <g transform={`translate(${x} ${y}) rotate(${deg}) scale(${s})`}>
      <rect x={-13} y={-10} width={26} height={20} rx={3} fill={c} /><path d="M -13 -2 L 13 -2" stroke="#000" strokeOpacity={0.35} strokeWidth={2} />
    </g>);
  if (shape === 'chip') return (
    <g transform={`translate(${x} ${y}) rotate(${deg}) scale(${s})`}>
      {[-8, 0, 8].map((q) => <g key={q}><rect x={q - 1.5} y={-15} width={3} height={30} fill={c} opacity={0.8} /><rect x={-15} y={q - 1.5} width={30} height={3} fill={c} opacity={0.8} /></g>)}
      <rect x={-10} y={-10} width={20} height={20} rx={3} fill="#0B1220" stroke={c} strokeWidth={3} />
    </g>);
  if (shape === 'packet') return (
    <g transform={`translate(${x} ${y}) rotate(${deg}) scale(${s})`}>
      <rect x={-14} y={-6} width={28} height={12} rx={6} fill={c} /><rect x={-28} y={-2} width={12} height={4} rx={2} fill={c} opacity={0.45} />
    </g>);
  return <circle cx={x} cy={y} r={7 * s} fill={c} />;
};

export const AnimatedWorldMap: React.FC<AnimatedWorldMapProps> = (props) => {
  const {t, geo, width: W = 1920, height: H = 1080, cameras, highlights = [], hubs = [], routes = [], opacity = 1, parallax = true} = props;
  const P = pal(props.palette);
  const rings = useMemo(() => parseLayer('engine-world', geo.paths), [geo]);
  const cam = cameraAt(cameras, t);
  const [ccx, ccy] = merc(cam.lon, cam.lat);
  const k = W / ((cam.span / 360) * WS);
  const proj = (lon: number, lat: number): Vec => {
    const L = unwrapTo(cam.lon, lon);
    const [, y] = merc(L, lat);
    return [(mx(L) - mx(cam.lon)) * k + W / 2, (y - ccy) * k + H / 2];
  };
  void ccx;
  const hl = new Map(highlights.map((h) => [h.iso, h]));
  // overscan: the map plane is larger than the frame so a perspective tilt never reveals its edges
  const MX = Math.round(W * 0.2), MY = Math.round(H * 0.25);
  // countries, drawn for three world copies; screenPath culls what is off-screen
  const countries: React.ReactNode[] = [];
  for (const off of [-1, 0, 1]) {
    const cx = mx(cam.lon) - off * WS;
    for (const [code, rs] of Object.entries(rings)) {
      const d = screenPath(rs as any, cx, ccy, k, W / 2 + MX, H / 2 + MY, W + 2 * MX, H + 2 * MY);
      if (!d) continue;
      const h = hl.get(code);
      const u = h ? E.out(win(t, h.at, h.dur ?? 0.8)) * (h.strength ?? 1) : 0;
      const c = h ? col(P, h.color) : P.land;
      countries.push(<path key={off + code} d={d} fill={P.land} stroke={P.border} strokeWidth={0.8} />);
      if (u > 0) countries.push(<path key={off + code + 'h'} d={d} fill={c} fillOpacity={0.62 * u} stroke={c} strokeWidth={1.6} strokeOpacity={u} />);
    }
  }
  const tilt = props.tilt ? (() => {
    const tk = props.tilt!; let v = tk[0][1];
    for (let i = 1; i < tk.length; i++) if (t >= tk[i - 1][0]) v = t >= tk[i][0] ? tk[i][1] : lerp(tk[i - 1][1], tk[i][1], E.inOut(win(t, tk[i - 1][0], tk[i][0] - tk[i - 1][0])));
    return v;
  })() : 0;
  // parallax star field: moves at 25% of the camera's pan, so the map reads as a plane in front of it
  const panX = (mx(cam.lon) * k) * 0.25, panY = (ccy * k) * 0.25;
  return (
    <div style={{position: 'absolute', inset: 0, opacity, perspective: 1600, overflow: 'hidden'}}>
      {parallax && (
        <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
          {Array.from({length: 90}, (_, i) => {
            const x = ((rnd(i) * W * 1.6 - panX) % (W * 1.6) + W * 1.6) % (W * 1.6) - W * 0.3;
            const y = ((rnd(i + 300) * H * 1.6 - panY) % (H * 1.6) + H * 1.6) % (H * 1.6) - H * 0.3;
            return <circle key={i} cx={x} cy={y} r={0.8 + rnd(i + 7) * 1.6} fill={P.ink} opacity={0.12 + 0.2 * rnd(i + 9)} />;
          })}
        </svg>
      )}
      <svg width={W + 2 * MX} height={H + 2 * MY} style={{position: 'absolute', left: -MX, top: -MY, transform: `rotateX(${tilt}deg)`, transformOrigin: '50% 55%'}}>
        <g>{countries}</g>
        <g transform={`translate(${MX} ${MY})`}>
        {routes.map((r, i) => {
          // `from` is unwrapped toward the camera, `to` toward `from` (shortest way round); the route is then drawn
          // for three world copies so a trans-Pacific arc leaves one edge and re-enters on the other, without jumps
          const a0 = proj(r.from[0], r.from[1]);
          const Lf = unwrapTo(cam.lon, r.from[0]), Lt = unwrapTo(Lf, r.to[0]);
          const [, yt] = merc(Lt, r.to[1]);
          const b0: Vec = [(mx(Lt) - mx(cam.lon)) * k + W / 2, (yt - ccy) * k + H / 2];
          const dur = r.dur ?? 1.2;
          const stop = r.blocked ? 0.55 : 1;
          const u = E.inOut(win(t, r.at, dur)) * stop;
          if (u <= 0) return null;
          const color = r.blocked ? P.risk : col(P, r.color);
          return [-1, 0, 1].map((off) => {
            const dx = off * WS * k;
            const a: Vec = [a0[0] + dx, a0[1]], b: Vec = [b0[0] + dx, b0[1]];
            if (Math.max(a[0], b[0]) < -200 || Math.min(a[0], b[0]) > W + 200) return null;
            const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
            const c: Vec = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - len * (r.lift ?? 0.28)];
            const n = 48, pts: string[] = [];
            for (let j = 0; j <= n; j++) { const q = quadPt(a, c, b, (j / n) * u); pts.push(q[0].toFixed(1) + ',' + q[1].toFixed(1)); }
            const head = quadPt(a, c, b, u);
            const tokens = r.tokens ?? 3, every = r.tokenEvery ?? 0.55, speed = r.tokenSpeed ?? 0.55;
            const mid = quadPt(a, c, b, 0.5);
            return (
              <g key={i + ':' + off}>
                <polyline points={pts.join(' ')} fill="none" stroke={color} strokeWidth={(r.width ?? 3) * 3} strokeOpacity={0.15} strokeLinecap="round" />
                <polyline points={pts.join(' ')} fill="none" stroke={color} strokeWidth={r.width ?? 3} strokeLinecap="round" strokeDasharray={u >= 1 ? '2 10' : undefined} />
                {u < stop && <circle cx={head[0]} cy={head[1]} r={9} fill={color} />}
                {r.blocked && u >= stop && (() => { const g = E.outBack(win(t, r.at + dur, 0.4)), sh = Math.sin(Math.max(0, t - r.at - dur) * 30) * 4 * (1 - win(t, r.at + dur, 0.6));
                  return <g transform={`translate(${head[0] + sh} ${head[1]}) scale(${g})`}>
                    <circle r={22} fill={P.bg} stroke={P.risk} strokeWidth={4} />
                    <path d="M -10 -10 L 10 10 M 10 -10 L -10 10" stroke={P.risk} strokeWidth={5} strokeLinecap="round" />
                  </g>; })()}
                {!r.blocked && u >= 1 && Array.from({length: tokens}, (_, j) => {
                  const q = (t - r.at - dur) * speed - j * every * speed;
                  if (q < 0) return null;
                  const f = q % 1;
                  const pp = quadPt(a, c, b, E.inOut(f));
                  const fade = Math.min(1, f * 8, (1 - f) * 8);
                  return <g key={j} opacity={fade}><Token shape={r.tokenShape || 'dot'} x={pp[0]} y={pp[1]} ang={quadTan(a, c, b, f)} c={color} /></g>;
                })}
                {r.label && u >= stop && mid[0] > 80 && mid[0] < W - 80 && (
                  <text x={mid[0]} y={mid[1] - 18} textAnchor="middle" fill={color} fontFamily={FONT.body} fontWeight={700} fontSize={22}
                    opacity={E.out(win(t, r.at + dur, 0.4))} letterSpacing={2}>{r.label}</text>)}
              </g>
            );
          });
        })}
        {hubs.map((h) => {
          const [x, y] = proj(h.at[0], h.at[1]);
          const u = E.outBack(win(t, h.time, 0.6));
          if (u <= 0) return null;
          const color = col(P, h.color);
          const pulse = ((t - h.time) * 0.9) % 1;
          const end = h.anchor === 'end';
          return (
            <g key={h.id}>
              <circle cx={x} cy={y} r={16 + 34 * pulse} fill="none" stroke={color} strokeWidth={2} opacity={0.7 * (1 - pulse)} />
              <circle cx={x} cy={y} r={11 * u} fill={color} stroke={P.bg} strokeWidth={3} />
              <g opacity={clamp(u)} transform={`translate(${x + (end ? -22 : 22)} ${y})`}>
                <text y={-4} textAnchor={end ? 'end' : 'start'} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={30}>{h.label}</text>
                {h.sub && <text y={28} textAnchor={end ? 'end' : 'start'} fill={color} fontFamily={FONT.body} fontWeight={600} fontSize={21}>{h.sub}</text>}
              </g>
            </g>
          );
        })}
        </g>
      </svg>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
        <defs><radialGradient id="eng-vig" cx="50%" cy="50%" r="70%"><stop offset="55%" stopColor={P.bg} stopOpacity={0} /><stop offset="100%" stopColor={P.bg} stopOpacity={0.85} /></radialGradient></defs>
        <rect width={W} height={H} fill="url(#eng-vig)" />
        {props.caption && <text x={60} y={H - 46} fill={P.muted} fontFamily={FONT.body} fontSize={20}>{props.caption}</text>}
      </svg>
    </div>
  );
};

/** Screen position of a lon/lat for the camera at time t (to hand off objects between scenes). */
export const mapPointAt = (cameras: MapCamera[], t: number, lonlat: LonLat, W = 1920, H = 1080): Vec => {
  const cam = cameraAt(cameras, t);
  const [, ccy] = merc(cam.lon, cam.lat);
  const k = W / ((cam.span / 360) * WS);
  const L = unwrapTo(cam.lon, lonlat[0]);
  const [, y] = merc(L, lonlat[1]);
  return [(mx(L) - mx(cam.lon)) * k + W / 2, (y - ccy) * k + H / 2];
};
