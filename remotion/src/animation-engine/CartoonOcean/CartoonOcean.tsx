import React from 'react';
import {E, clamp, ease, lerp, win} from '../motion';

/**
 * CartoonOcean: a side-view, cartoon-style ocean world (flat colours, thick outlines, squash-and-stretch).
 *
 * Sky with a smiling sun and drifting clouds, rolling waves, light rays and bubbles, a sandy seabed with swaying
 * seaweed, coasts with a data center, a landing station and houses, one or more seabed CABLES carrying pulses of
 * light, and ACTORS: cargo ships (anchor drag, sinking), fishing boats (trawl net), repair ships (grapple lifts the
 * cable, splices it, lowers it), cable-laying ships (cable pays out behind), a satellite, an undersea volcano,
 * an island whose lights go out, fish schools and a whale. Cartoon speech-bubble CALLOUTS explain the beat.
 * A CAMERA pans/zooms across the world (sky -> seabed tracking shots). All times in seconds; pure function of t.
 */
type Key = {at: number; x?: number; y?: number; zoom?: number; dur?: number};
export type CartoonCable = {dy?: number; color?: string; lightAt?: number; breakAt?: number; breakX?: number;
  repairAt?: number; shred?: boolean; from?: number; to?: number; label?: string;
  /** index of a 'layer' actor: the cable ends at that ship and rises to its stern (cable being laid) */
  follow?: number};
export type CartoonActor = {
  kind: 'cargo' | 'fishing' | 'repair' | 'layer' | 'satellite' | 'volcano' | 'whale' | 'island'
    | 'letters' | 'coins' | 'plane' | 'storm' | 'office' | 'piggy';
  /** letters/office/plane: the text shown; coins: [x2, y2] target, rate per second, until */
  text?: string; to?: [number, number]; rate?: number; until?: number; size?: number;
  /** ships: a text pennant on the stern mast (a label, never a real national flag design); keyframes switch it */
  flag?: string | [number, string][]; flagColor?: string;
  /** ships: crew on deck; sadAt makes them sad (abandoned) */
  crew?: number; sadAt?: number;
  at?: number; x?: number | [number, number][]; y?: number; name?: string; color?: string; scale?: number;
  flip?: boolean;
  anchorAt?: number; sinkAt?: number; smokeAt?: number; netAt?: number;
  grapple?: {at: number; lift?: number; splice?: number; lower?: number};
  layAt?: number; beamAt?: number; eruptAt?: number; darkAt?: number; lightAt?: number; w?: number;
};
export type CartoonCallout = {text: string; sub?: string; x: number; y: number; at: number; until?: number; color?: string;
  tail?: [number, number]; size?: number; screen?: boolean};
export type CartoonOceanProps = {
  t: number; W?: number; H?: number;
  worldW?: number; sea?: number; bed?: number;
  cam?: Key[]; drift?: number; shake?: {at: number; dur?: number; amp?: number}[];
  /** port: a container crane and box stacks instead of the data center (shipping stories) */
  coasts?: {left?: boolean; right?: boolean; leftLabel?: string; rightLabel?: string; darkAt?: number; port?: boolean};
  cables?: CartoonCable[];
  actors?: CartoonActor[];
  callouts?: CartoonCallout[];
  fish?: number;
  banner?: {text: string; sub?: string; at?: number};
  night?: boolean;
};

const OL = '#10213A';            // outline
const K = {sky1: '#7FD3F7', sky2: '#D8F4FF', sea1: '#2BA9D8', sea2: '#0B3E73', sea3: '#06213F', sand: '#E9C98A', sand2: '#C9A266',
  land: '#7BCB6B', land2: '#4E9E4A', rock: '#8C8FA3', weed: '#3FBF7F', sun: '#FFD54A', light: '#7DF9FF', gold: '#FFC93C',
  red: '#FF5A5F', white: '#FFFFFF', hull: '#E2504C', hull2: '#2F6FD1', cream: '#FFF5E1'};

const keyAt = (keys: [number, number][], t: number) => {
  if (!keys.length) return 0;
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t <= keys[i][0]) return lerp(keys[i - 1][1], keys[i][1], E.inOut(win(t, keys[i - 1][0], keys[i][0] - keys[i - 1][0])));
  return keys[keys.length - 1][1];
};
const xOf = (a: CartoonActor, t: number) => (Array.isArray(a.x) ? keyAt(a.x, t) : a.x ?? 960);
const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };

export const CartoonOcean: React.FC<CartoonOceanProps> = (p) => {
  const {t, W = 1920, H = 1080, worldW = 1920, sea = 380, bed = 930, coasts = {}, cables = [], actors = [], callouts = [], fish = 3} = p;
  const cw = 330;                                                     // coast width
  const bedY = (x: number) => bed + 16 * Math.sin(x / 260) + 8 * Math.sin(x / 90 + 1);
  const groundY = (x: number) => {
    let y = bedY(x);
    if (coasts.left) { if (x < cw) return sea - 60; if (x < cw + 320) y = lerp(sea - 60, bedY(x), E.inOut((x - cw) / 320)); }
    if (coasts.right) { const r = worldW - cw; if (x > r) return sea - 60; if (x > r - 320) y = lerp(bedY(x), sea - 60, E.inOut((x - (r - 320)) / 320)); }
    return y;
  };
  // ------------------------------------------------ camera
  const cams = p.cam?.length ? p.cam : [{at: 0, x: 960, y: 540, zoom: 1}];
  let cx = cams[0].x ?? 960, cy = cams[0].y ?? 540, cz = cams[0].zoom ?? 1;
  for (const k of cams.slice(1)) {
    const u = ease(t, k.at, k.dur ?? 2.2, E.inOutQuint);
    cx = lerp(cx, k.x ?? cx, u); cy = lerp(cy, k.y ?? cy, u); cz = lerp(cz, k.zoom ?? cz, u);
  }
  cx += (p.drift ?? 6) * t;
  let sx = 0, sy = 0;
  for (const s of p.shake || []) { const u = win(t, s.at, s.dur ?? 1.2); if (u > 0 && u < 1) { const a = (s.amp ?? 14) * (1 - u); sx += Math.sin(t * 61) * a; sy += Math.cos(t * 47) * a; } }
  const camT = `translate(${W / 2 + sx} ${H / 2 + sy}) scale(${cz}) translate(${-cx} ${-cy})`;

  // ------------------------------------------------ actors that move the cable (grapple lift)
  const lifts = actors.filter((a) => a.kind === 'repair' && a.grapple).map((a) => {
    const g = a.grapple!, gx = xOf(a, g.at) + (a.flip ? -1 : 1) * 120 * (a.scale ?? 1);
    const up = ease(t, g.lift ?? g.at + 2, 2.2, E.inOut) * (1 - ease(t, g.lower ?? 1e9, 2.2, E.inOut));
    return {x: gx, up};
  });
  const cablePts = (c: CartoonCable) => {
    const fa = c.follow !== undefined ? actors[c.follow] : undefined;
    const from = c.from ?? (coasts.left ? cw - 70 : -200), to = fa ? xOf(fa, t) - (fa.flip ? -1 : 1) * 300 * (fa.scale ?? 1) : c.to ?? (coasts.right ? worldW - cw + 70 : worldW + 200);
    const pts: [number, number][] = [];
    for (let x = from; x <= to; x += 12) {
      let y = (x < cw - 10 && coasts.left) || (x > worldW - cw + 10 && coasts.right) ? sea - 64 : groundY(x) - 8 + (c.dy ?? 0);
      for (const l of lifts) { const d = (x - l.x) / 330; if (Math.abs(d) < 1) y = lerp(y, sea + 30, l.up * (0.5 + 0.5 * Math.cos(Math.PI * d))); }
      pts.push([x, y]);
    }
    if (fa) { const sx2 = xOf(fa, t) - (fa.flip ? -1 : 1) * 170 * (fa.scale ?? 1), e = pts[pts.length - 1] || [to, bed];
      for (let k = 1; k <= 12; k++) { const u = k / 12; pts.push([lerp(e[0], sx2, u), lerp(e[1], surfY(sx2) + 10, u * u)]); } }
    return pts;
  };
  const poly = (pts: [number, number][]) => pts.map((q, i) => `${i ? 'L' : 'M'} ${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(' ');

  // ------------------------------------------------ pieces
  const waves = (y: number, amp: number, len: number, speed: number, fill: string, op = 1) => {
    let d = `M -2000 ${y + 34}`;
    for (let x = -2000; x <= worldW + 2000; x += 40) d += ` L ${x} ${(y + amp * Math.sin((x + t * speed) / len)).toFixed(1)}`;
    d += ` L ${worldW + 2000} ${y + 34} Z`;
    return <path d={d} fill={fill} opacity={op} />;
  };
  const surfY = (x: number) => sea + 10 * Math.sin((x + t * 70) / 90);

  const Ship: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), s = a.scale ?? 1, f = a.flip ? -1 : 1;
    const sink = a.sinkAt !== undefined ? ease(t, a.sinkAt, 4.5, E.in) : 0;
    const bob = Math.sin(t * 2.2 + x / 100) * 6 * (1 - sink), tilt = Math.sin(t * 1.7 + x) * 2.5 + sink * 24;
    const y = surfY(x) + bob + sink * (bed - sea - 120);
    const hull = a.color || (a.kind === 'cargo' ? K.hull : a.kind === 'fishing' ? '#F28C28' : a.kind === 'repair' ? '#F4F7FB' : K.hull2);
    const body = (() => {
      if (a.kind === 'cargo') return <g>
        {[0, 1, 2, 3, 4].map((i) => <rect key={i} x={-150 + i * 52} y={-58} width={48} height={34} rx={4} fill={['#4FB3F6', '#FFC93C', '#7BD389', '#FF8A65', '#B39DDB'][i]} stroke={OL} strokeWidth={4} />)}
        <rect x={110} y={-100} width={50} height={78} rx={6} fill={K.cream} stroke={OL} strokeWidth={4} />
        <rect x={120} y={-90} width={30} height={14} rx={3} fill={K.light} stroke={OL} strokeWidth={3} />
        <path d="M -190 -24 L 200 -24 L 165 30 L -160 30 Z" fill={hull} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <path d="M -175 0 L 185 0" stroke={K.white} strokeWidth={6} opacity={0.7} /></g>;
      if (a.kind === 'fishing') return <g>
        <rect x={-30} y={-70} width={56} height={48} rx={6} fill={K.cream} stroke={OL} strokeWidth={4} />
        <path d="M 40 -24 L 40 -110 L 110 -40" fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
        <path d="M -100 -24 L 110 -24 L 85 22 L -80 22 Z" fill={hull} stroke={OL} strokeWidth={5} strokeLinejoin="round" /></g>;
      if (a.kind === 'repair') return <g>
        <rect x={-60} y={-92} width={90} height={70} rx={8} fill={K.cream} stroke={OL} strokeWidth={4} />
        {[0, 1, 2].map((i) => <rect key={i} x={-50 + i * 28} y={-80} width={20} height={14} rx={3} fill={K.light} stroke={OL} strokeWidth={3} />)}
        <path d="M 70 -24 L 120 -130 L 170 -24" fill="none" stroke="#FFB300" strokeWidth={9} strokeLinejoin="round" />
        <path d="M 70 -24 L 120 -130 L 170 -24" fill="none" stroke={OL} strokeWidth={3} />
        <path d="M -170 -24 L 190 -24 L 160 28 L -150 28 Z" fill={hull} stroke={OL} strokeWidth={5} strokeLinejoin="round" />
        <path d="M -160 2 L 175 2" stroke="#E2504C" strokeWidth={8} /></g>;
      return <g>{/* cable layer: big spool on deck */}
        <circle cx={-60} cy={-70} r={46} fill="#FFB300" stroke={OL} strokeWidth={5} />
        <circle cx={-60} cy={-70} r={30} fill="none" stroke={OL} strokeWidth={3} strokeDasharray="8 6" transform={`rotate(${t * 90} -60 -70)`} />
        <rect x={40} y={-96} width={70} height={72} rx={8} fill={K.cream} stroke={OL} strokeWidth={4} />
        <path d="M -180 -24 L 190 -24 L 160 28 L -150 28 Z" fill={hull} stroke={OL} strokeWidth={5} strokeLinejoin="round" /></g>;
    })();
    const out: React.ReactNode[] = [];
    // anchor: drops to the seabed, then drags behind the moving ship
    if (a.anchorAt !== undefined && t >= a.anchorAt) {
      const u = E.out(win(t, a.anchorAt, 1.4));
      const ax = x - f * 90 * s - f * 60 * u, ay = lerp(y, groundY(ax) - 18, u);
      out.push(<g key="anchor">
        <path d={`M ${x - f * 90 * s} ${y + 10} Q ${(x + ax) / 2} ${(y + ay) / 2 + 40} ${ax} ${ay}`} fill="none" stroke="#5B6475" strokeWidth={5} strokeDasharray="10 6" />
        <g transform={`translate(${ax} ${ay}) rotate(${u >= 1 ? -f * 25 : 0})`}>
          <path d="M 0 -26 L 0 18 M -22 6 Q 0 34 22 6 M -10 -16 L 10 -16" fill="none" stroke={OL} strokeWidth={9} strokeLinecap="round" />
          <path d="M 0 -26 L 0 18 M -22 6 Q 0 34 22 6 M -10 -16 L 10 -16" fill="none" stroke="#9AA3B5" strokeWidth={4} strokeLinecap="round" />
          {u >= 1 && [0, 1, 2].map((i) => <circle key={i} cx={f * (20 + i * 18) + Math.sin(t * 5 + i) * 4} cy={14 - i * 8} r={8 + i * 3} fill={K.sand} opacity={0.6} />)}
        </g></g>);
    }
    if (a.netAt !== undefined && t >= a.netAt) {
      const u = E.out(win(t, a.netAt, 1.8)), nx = x - f * 260 * s * u, ny = lerp(y, groundY(nx) - 40, u);
      out.push(<g key="net">
        <path d={`M ${x - f * 100 * s} ${y} L ${nx} ${ny - 30} M ${x - f * 100 * s} ${y} L ${nx} ${ny + 30}`} stroke="#5B6475" strokeWidth={3} />
        <path d={`M ${nx} ${ny - 34} Q ${nx - f * 90} ${ny} ${nx} ${ny + 34} Q ${nx - f * 40} ${ny} ${nx} ${ny - 34}`} fill="#C8E6C9" fillOpacity={0.35} stroke={OL} strokeWidth={3} />
        {[-20, 0, 20].map((k) => <path key={k} d={`M ${nx - f * 10} ${ny + k} L ${nx - f * 60} ${ny + k * 0.6}`} stroke={OL} strokeWidth={2} />)}</g>);
    }
    if (a.kind === 'repair' && a.grapple && t >= a.grapple.at) {
      const g = a.grapple, gx = xOf(a, g.at) + (a.flip ? -1 : 1) * 120 * s;
      const down = E.out(win(t, g.at, 1.6));
      const lift = lifts.find((l) => Math.abs(l.x - gx) < 1)?.up ?? 0;
      const hy = lerp(y - 120 * s, lerp(groundY(gx) - 14, sea + 26, lift), down);
      out.push(<g key="grapple"><path d={`M ${gx} ${y - 125 * s} L ${gx} ${hy}`} stroke={OL} strokeWidth={4} />
        <path d={`M ${gx - 14} ${hy} Q ${gx} ${hy + 22} ${gx + 14} ${hy} M ${gx} ${hy - 6} L ${gx} ${hy + 14}`} fill="none" stroke="#9AA3B5" strokeWidth={6} strokeLinecap="round" /></g>);
      if (g.splice !== undefined && t >= g.splice && t < g.splice + 2.4) {
        const sp = win(t, g.splice, 2.4);
        out.push(<g key="spark">{Array.from({length: 10}, (_, i) => { const an = i * 0.63 + t * 3; const r = 20 + 40 * ((sp * 3 + rnd(i)) % 1);
          return <path key={i} d={`M ${gx + Math.cos(an) * r * 0.4} ${sea + 30 + Math.sin(an) * r * 0.4} L ${gx + Math.cos(an) * r} ${sea + 30 + Math.sin(an) * r}`} stroke={K.gold} strokeWidth={5} strokeLinecap="round" />; })}</g>);
      }
    }
    if (a.smokeAt !== undefined && t >= a.smokeAt) {
      out.push(<g key="smoke">{Array.from({length: 7}, (_, i) => { const u = ((t - a.smokeAt!) * 0.5 + i / 7) % 1;
        return <circle key={i} cx={x + 20 + u * 60 + Math.sin(i + t) * 10} cy={y - 80 - u * 260} r={22 + u * 40} fill="#6B7280" opacity={0.55 * (1 - u) * (1 - sink)} />; })}</g>);
    }
    if (sink > 0) out.push(<g key="bub">{Array.from({length: 8}, (_, i) => { const u = ((t - a.sinkAt!) * 0.7 + i / 8) % 1;
      return <circle key={i} cx={x + (rnd(i) - 0.5) * 200} cy={y - u * (y - sea)} r={6 + rnd(i + 3) * 8} fill="none" stroke={K.white} strokeWidth={3} opacity={0.7 * (1 - u)} />; })}</g>);
    const flagTxt = Array.isArray(a.flag) ? (a.flag.filter((k) => t >= k[0]).slice(-1)[0]?.[1] ?? a.flag[0]?.[1]) : a.flag;
    const flagSwap = Array.isArray(a.flag) ? Math.max(0, ...a.flag.map((k) => (t >= k[0] && t < k[0] + 0.5 ? 1 - (t - k[0]) / 0.5 : 0))) : 0;
    const sad = a.sadAt !== undefined && t >= a.sadAt;
    const crewN = a.crew ?? 0;
    const fw = flagTxt ? flagTxt.length * 14 + 30 : 0;
    return <g>{out}
      <g transform={`translate(${x} ${y}) rotate(${f * tilt}) scale(${f * s} ${s})`}>
        {crewN > 0 && Array.from({length: crewN}, (_, i) => { const cxp = -120 + i * 34, hop = sad ? 0 : Math.abs(Math.sin(t * 3 + i)) * 4;
          return <g key={'c' + i} transform={`translate(${cxp} ${-34 - hop})`}>
            <rect x={-9} y={-6} width={18} height={20} rx={6} fill={['#FF8A65', '#4FC3F7', '#FFD54A', '#81C784'][i % 4]} stroke={OL} strokeWidth={3} />
            <circle cx={0} cy={-16} r={11} fill="#F2C29B" stroke={OL} strokeWidth={3} />
            <circle cx={-4} cy={-18} r={2} fill={OL} /><circle cx={4} cy={-18} r={2} fill={OL} />
            <path d={sad ? 'M -4 -9 Q 0 -13 4 -9' : 'M -4 -12 Q 0 -8 4 -12'} fill="none" stroke={OL} strokeWidth={2} strokeLinecap="round" />
          </g>; })}
        {body}
        {flagTxt && <g transform="translate(-178 -24)">
          <path d="M 0 0 L 0 -120" stroke={OL} strokeWidth={5} strokeLinecap="round" />
          <g transform={`translate(0 -118) scale(${(1 - flagSwap * 0.9) * f} 1) rotate(${Math.sin(t * 4) * 2})`}>
            <path d={`M 0 0 L ${-fw} 4 Q ${-fw - 12} 24 ${-fw} 44 L 0 46 Z`}
              fill={a.flagColor === 'risk' ? '#FF5A5F' : a.flagColor === 'grey' ? '#B8C1CF' : '#FFC93C'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
            <text x={-fw / 2} y={31} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={22} fill={OL}>{flagTxt}</text>
          </g></g>}
      </g>
      {a.name && <g transform={`translate(${x} ${y + 60 * s})`} opacity={1 - sink}><rect x={-80} y={-20} width={160} height={36} rx={18} fill={K.white} stroke={OL} strokeWidth={3} />
        <text x={0} y={7} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={800} fontSize={20} fill={OL}>{a.name}</text></g>}
    </g>;
  };

  const Satellite: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = (a.y ?? 120) + Math.sin(t * 1.3) * 10, s = a.scale ?? 1;
    const beam = a.beamAt !== undefined && t >= a.beamAt ? 0.5 + 0.5 * Math.sin((t - a.beamAt) * 6) : 0;
    return <g>
      {beam > 0 && <path d={`M ${x} ${y + 30} L ${x - 60} ${sea - 70} L ${x + 60} ${sea - 70} Z`} fill={K.gold} opacity={0.12 + 0.12 * beam} />}
      <g transform={`translate(${x} ${y}) rotate(${Math.sin(t) * 6}) scale(${s})`}>
        <rect x={-110} y={-22} width={70} height={44} fill="#3D7BE0" stroke={OL} strokeWidth={4} /><rect x={40} y={-22} width={70} height={44} fill="#3D7BE0" stroke={OL} strokeWidth={4} />
        <path d="M -110 0 L -40 0 M -75 -22 L -75 22 M 40 0 L 110 0 M 75 -22 L 75 22" stroke={OL} strokeWidth={2} />
        <rect x={-36} y={-30} width={72} height={60} rx={10} fill="#E0E6EF" stroke={OL} strokeWidth={4} />
        <circle cx={-12} cy={-4} r={6} fill={OL} /><circle cx={12} cy={-4} r={6} fill={OL} />
        <path d="M -12 14 Q 0 6 12 14" fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />{/* a slightly unsure face */}
      </g></g>;
  };

  const Volcano: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), gy = groundY(x), s = a.scale ?? 1;
    const er = a.eruptAt !== undefined ? win(t, a.eruptAt, 0.6) : 0, el = a.eruptAt !== undefined ? Math.max(0, t - a.eruptAt) : 0;
    return <g>
      {er > 0 && Array.from({length: 14}, (_, i) => { const u = (el * 0.35 + i / 14) % 1, h = u * (gy - sea + 400);
        return <circle key={i} cx={x + Math.sin(i * 2.1 + el) * (30 + u * 140)} cy={gy - 150 * s - h} r={(30 + u * 90) * s} fill={i % 3 ? '#5E5A66' : '#8A8494'} opacity={0.8 * (1 - u)} />; })}
      {er > 0 && [0, 1, 2].map((i) => { const u = ((el - i * 0.5) * 0.6) % 1; return u > 0 ? <circle key={'r' + i} cx={x} cy={gy - 150 * s} r={60 + u * 700} fill="none" stroke={K.white} strokeWidth={6} opacity={0.5 * (1 - u)} /> : null; })}
      <path d={`M ${x - 260 * s} ${gy + 10} L ${x - 50 * s} ${gy - 150 * s} L ${x + 50 * s} ${gy - 150 * s} L ${x + 260 * s} ${gy + 10} Z`} fill="#6D5D6E" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      <path d={`M ${x - 50 * s} ${gy - 150 * s} L ${x - 20 * s} ${gy - 110 * s} L ${x} ${gy - 140 * s} L ${x + 25 * s} ${gy - 105 * s} L ${x + 50 * s} ${gy - 150 * s}`} fill={er > 0 ? '#FF7A1A' : '#4A3F4B'} stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      {er > 0 && <circle cx={x} cy={gy - 150 * s} r={(40 + 10 * Math.sin(t * 9)) * s} fill="#FFB020" opacity={0.6} />}
    </g>;
  };

  const Island: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), w = a.w ?? 420, top = sea - 70;
    const dark = a.darkAt !== undefined && t >= a.darkAt && !(a.lightAt !== undefined && t >= a.lightAt);
    return <g>
      <path d={`M ${x - w / 2 - 80} ${sea + 30} Q ${x - w / 2} ${top} ${x} ${top - 10} Q ${x + w / 2} ${top} ${x + w / 2 + 80} ${sea + 30} Z`} fill={K.sand} stroke={OL} strokeWidth={5} />
      <path d={`M ${x - w / 2 + 10} ${top + 14} Q ${x} ${top - 40} ${x + w / 2 - 10} ${top + 14} Z`} fill={K.land} stroke={OL} strokeWidth={4} />
      <path d={`M ${x + w / 2 - 70} ${top} Q ${x + w / 2 - 60} ${top - 90} ${x + w / 2 - 50} ${top - 150}`} fill="none" stroke="#8D5A2B" strokeWidth={12} strokeLinecap="round" />
      {[0, 1, 2, 3].map((i) => <path key={i} d={`M ${x + w / 2 - 50} ${top - 150} q ${[-70, 70, -50, 50][i]} ${[-10, -10, 30, 30][i]} ${[-110, 110, -90, 90][i]} ${[30, 30, 70, 70][i]}`} fill="none" stroke={K.land2} strokeWidth={14} strokeLinecap="round" transform={`rotate(${Math.sin(t * 2 + i) * 4} ${x + w / 2 - 50} ${top - 150})`} />)}
      {[0, 1, 2].map((i) => { const hx = x - w / 2 + 70 + i * 95, hy = top - 40;
        return <g key={i}><path d={`M ${hx - 36} ${hy} L ${hx} ${hy - 36} L ${hx + 36} ${hy} Z`} fill="#E2504C" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
          <rect x={hx - 28} y={hy} width={56} height={44} fill={K.cream} stroke={OL} strokeWidth={4} />
          <rect x={hx - 10} y={hy + 10} width={20} height={18} fill={dark ? '#2A3550' : K.gold} stroke={OL} strokeWidth={3} /></g>; })}
      {a.text && <g transform={`translate(${x - 40} ${sea + 4})`}><rect x={-90} y={-4} width={180} height={34} rx={17} fill={K.white} stroke={OL} strokeWidth={3} />
        <text x={0} y={21} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={20} fill={OL}>{a.text}</text></g>}
      {dark && <text x={x - 30} y={top - 120} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={54} fill={K.white} stroke={OL} strokeWidth={3}>?!</text>}
    </g>;
  };

  const Whale: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = (a.y ?? 700) + Math.sin(t * 1.2) * 18, f = a.flip ? -1 : 1, tail = Math.sin(t * 3) * 12;
    return <g transform={`translate(${x} ${y}) scale(${f} 1)`}>
      <path d="M -170 0 Q -150 -80 0 -80 Q 150 -80 170 0 Q 150 60 0 60 Q -120 60 -170 0 Z" fill="#5C7CFA" stroke={OL} strokeWidth={5} />
      <path d="M -40 20 Q 60 60 150 12" fill="none" stroke="#DCE4FF" strokeWidth={10} strokeLinecap="round" />
      <g transform={`rotate(${tail} -170 0)`}><path d="M -170 0 L -250 -50 Q -230 0 -250 50 Z" fill="#5C7CFA" stroke={OL} strokeWidth={5} strokeLinejoin="round" /></g>
      <circle cx={110} cy={-20} r={9} fill={OL} /><path d="M 120 8 Q 140 18 150 6" fill="none" stroke={OL} strokeWidth={4} strokeLinecap="round" />
    </g>;
  };


  /** giant bouncy letters (e.g. ".ai") that land with squash and stretch, then wobble */
  const Letters: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = a.y ?? sea - 200, size = a.size ?? 150, at = a.at ?? 0;
    const fall = E.in(win(t, at, 0.5)), land = win(t, at + 0.5, 0.5);
    const sq = land > 0 && land < 1 ? Math.sin(land * Math.PI) * 0.25 : 0;
    const yy = lerp(y - 700, y, fall) + Math.sin(t * 2) * 6 * (land >= 1 ? 1 : 0);
    const col = a.color === 'blue' ? '#3D7BE0' : a.color === 'green' ? '#2EAD63' : a.color === 'grey' ? '#B8C1CF' : K.gold;
    return <g transform={`translate(${x} ${yy}) scale(${1 + sq} ${1 - sq}) rotate(${Math.sin(t * 1.6) * 3})`}>
      <text x={6} y={8} textAnchor="middle" fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={size} fill={OL}>{a.text}</text>
      <text x={0} y={0} textAnchor="middle" fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={size} fill={col} stroke={OL} strokeWidth={6} paintOrder="stroke">{a.text}</text>
      {land >= 1 && [0, 1, 2, 3].map((i) => <path key={i} d={`M ${-size * 0.9 + i * size * 0.6} ${-size * 0.95} l ${8 * Math.sin(t * 4 + i)} -22`} stroke={K.white} strokeWidth={6} strokeLinecap="round" opacity={0.5 + 0.5 * Math.sin(t * 5 + i)} />)}
    </g>;
  };
  /** a stream of gold coins arcing from one point to another (money flowing to the island) */
  const Coins: React.FC<{a: CartoonActor}> = ({a}) => {
    const x0 = xOf(a, t), y0 = a.y ?? sea - 300, [x1, y1] = a.to ?? [x0 + 600, sea - 100], at = a.at ?? 0;
    const rate = a.rate ?? 4, end = a.until ?? 1e9, fly = 1.6, out: React.ReactNode[] = [];
    const n = Math.min(200, Math.floor((Math.min(t, end) - at) * rate) + 1);
    for (let k = Math.max(0, n - Math.ceil(rate * fly) - 1); k < n; k++) {
      const u = (t - (at + k / rate)) / fly; if (u < 0 || u > 1) continue;
      const cx = lerp(x0, x1, u) + Math.sin(k * 1.7) * 30 * (1 - u), cy = lerp(y0, y1, u) - Math.sin(Math.PI * u) * 220;
      const spin = Math.abs(Math.cos(t * 8 + k));
      out.push(<g key={k} transform={`translate(${cx} ${cy}) scale(${0.3 + 0.7 * spin} 1)`}><circle r={18} fill={K.gold} stroke={OL} strokeWidth={4} />
        <text x={0} y={7} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={20} fill={OL}>$</text></g>);
    }
    return <g>{out}</g>;
  };
  const Plane: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = (a.y ?? 160) + Math.sin(t * 2) * 8, f = a.flip ? -1 : 1, s = a.scale ?? 1;
    return <g>
      {a.text && <g><path d={`M ${x - f * 150 * s} ${y} L ${x - f * 220 * s} ${y}`} stroke={OL} strokeWidth={3} />
        <rect x={f > 0 ? x - 220 * s - a.text.length * 15 - 30 : x + 220 * s} y={y - 24} width={a.text.length * 15 + 30} height={48} rx={8} fill={K.white} stroke={OL} strokeWidth={4} transform={`rotate(${Math.sin(t * 3) * 2} ${x} ${y})`} />
        <text x={f > 0 ? x - 220 * s - (a.text.length * 15 + 30) / 2 : x + 220 * s + (a.text.length * 15 + 30) / 2} y={y + 8} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={24} fill={OL}>{a.text}</text></g>}
      <g transform={`translate(${x} ${y}) scale(${f * s} ${s})`}>
        <path d="M -150 0 Q -140 -30 -60 -30 L 110 -30 Q 160 -28 170 0 Q 160 26 110 28 L -60 28 Q -140 28 -150 0 Z" fill={K.white} stroke={OL} strokeWidth={5} />
        <path d="M -20 -10 L -80 -90 L -40 -90 L 40 -10 Z M -120 -20 L -150 -70 L -125 -70 L -95 -25 Z" fill="#3D7BE0" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
        {[0, 1, 2, 3, 4].map((i) => <circle key={i} cx={-40 + i * 32} cy={-6} r={8} fill={K.light} stroke={OL} strokeWidth={3} />)}
      </g></g>;
  };
  const Storm: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = a.y ?? 150, s = a.scale ?? 1, at = a.at ?? 0, o = a.until !== undefined ? 1 - win(t, a.until, 0.8) : 1;
    return <g opacity={o}>
      {Array.from({length: 26}, (_, i) => { const u = ((t * 1.4 + i / 26) % 1); const rx = x - 260 * s + (i * 37) % (520 * s);
        return <path key={i} d={`M ${rx + u * 40} ${y + 40 + u * (sea - y - 40)} l -12 34`} stroke="#9ED0FF" strokeWidth={4} strokeLinecap="round" opacity={0.8} />; })}
      <g transform={`translate(${x} ${y}) rotate(${(t - at) * 160}) scale(${s})`}>
        {[0, 1, 2].map((i) => <path key={i} d={`M 0 0 Q ${60 + i * 50} -${40 + i * 20} ${120 + i * 70} ${10 + i * 20}`} transform={`rotate(${i * 120})`} fill="none" stroke="#6E7F99" strokeWidth={30 - i * 6} strokeLinecap="round" />)}
        <circle r={34} fill="#55627A" stroke={OL} strokeWidth={4} /></g>
      {Array.from({length: 5}, (_, i) => { const u = ((t * 0.9 + i / 5) % 1);
        return <path key={'w' + i} d={`M ${x + 200 + u * 500} ${y + 120 + i * 40} q 40 -20 80 0`} fill="none" stroke={K.white} strokeWidth={5} strokeLinecap="round" opacity={1 - u} />; })}
    </g>;
  };
  const Office: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), base = a.y ?? sea - 76, s = a.scale ?? 1, h = 190 * s, w = 130 * s;
    const col = a.color === 'blue' ? '#7FB3FF' : a.color === 'green' ? '#8FE3A8' : a.color === 'gold' ? '#FFD66B' : '#C9B8FF';
    return <g>
      <rect x={x - w / 2} y={base - h} width={w} height={h} rx={10} fill={col} stroke={OL} strokeWidth={5} />
      {Array.from({length: 4}, (_, r) => [0, 1, 2].map((c2) => <rect key={`${r}${c2}`} x={x - w / 2 + 16 + c2 * (w - 32) / 3} y={base - h + 50 + r * 34} width={(w - 32) / 3 - 10} height={20} rx={3}
        fill={Math.sin(t * 3 + r * 2 + c2) > -0.2 ? K.light : '#2A3550'} stroke={OL} strokeWidth={2} />))}
      <rect x={x - w / 2 - 20} y={base - h - 46} width={w + 40} height={42} rx={10} fill={K.white} stroke={OL} strokeWidth={4} />
      <text x={x} y={base - h - 17} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={22 * Math.min(1, 12 / Math.max(6, (a.text || '').length))} fill={OL}>{a.text}</text>
    </g>;
  };
  const Piggy: React.FC<{a: CartoonActor}> = ({a}) => {
    const x = xOf(a, t), y = a.y ?? sea - 130, s = (a.scale ?? 1) * (1 + 0.03 * Math.sin(t * 4)), at = a.at ?? 0;
    const fill = clamp((t - at) / 6);
    return <g transform={`translate(${x} ${y}) scale(${s})`}>
      <ellipse cx={0} cy={0} rx={120} ry={90} fill="#FF9EB5" stroke={OL} strokeWidth={6} />
      <rect x={-30} y={-96} width={60} height={12} rx={6} fill={OL} />
      <ellipse cx={112} cy={6} rx={28} ry={22} fill="#FF86A3" stroke={OL} strokeWidth={5} /><circle cx={106} cy={4} r={4} fill={OL} /><circle cx={120} cy={4} r={4} fill={OL} />
      <circle cx={60} cy={-30} r={9} fill={OL} />
      <path d="M -60 -70 L -40 -110 L -20 -76 Z" fill="#FF86A3" stroke={OL} strokeWidth={5} strokeLinejoin="round" />
      {[-70, -20, 30, 70].map((lx) => <rect key={lx} x={lx - 12} y={70} width={24} height={36} rx={8} fill="#FF86A3" stroke={OL} strokeWidth={5} />)}
      <rect x={-80} y={110} width={160} height={14} rx={7} fill={K.white} stroke={OL} strokeWidth={3} /><rect x={-80} y={110} width={160 * fill} height={14} rx={7} fill={K.gold} />
    </g>;
  };

  const actorNode = (a: CartoonActor, i: number) => {
    if (a.at !== undefined && t < a.at) return null;
    const pop = a.at !== undefined && !['letters', 'coins', 'storm'].includes(a.kind) ? E.outBack(win(t, a.at, 0.6)) : 1;
    const node = a.kind === 'satellite' ? <Satellite a={a} /> : a.kind === 'volcano' ? <Volcano a={a} /> : a.kind === 'island' ? <Island a={a} />
      : a.kind === 'whale' ? <Whale a={a} /> : a.kind === 'letters' ? <Letters a={a} /> : a.kind === 'coins' ? <Coins a={a} /> : a.kind === 'plane' ? <Plane a={a} />
      : a.kind === 'storm' ? <Storm a={a} /> : a.kind === 'office' ? <Office a={a} /> : a.kind === 'piggy' ? <Piggy a={a} /> : <Ship a={a} />;
    return <g key={i} opacity={clamp(pop * 1.4)}>{node}</g>;
  };

  // ------------------------------------------------ cables
  const cableNode = (c: CartoonCable, i: number) => {
    const pts = cablePts(c);
    const broken = c.breakAt !== undefined && t >= c.breakAt && !(c.repairAt !== undefined && t >= c.repairAt);
    const bx = c.breakX ?? (pts[0][0] + pts[pts.length - 1][0]) / 2;
    const color = c.color || '#1E2A44';
    const gaps = broken ? (c.shred ? [bx - 220, bx - 60, bx + 110, bx + 260] : [bx]) : [];
    const segs: [number, number][][] = [];
    let cur: [number, number][] = [];
    for (const q of pts) { if (gaps.some((g) => Math.abs(q[0] - g) < 26)) { if (cur.length > 1) segs.push(cur); cur = []; } else cur.push(q); }
    if (cur.length > 1) segs.push(cur);
    const healed = c.repairAt !== undefined && t >= c.repairAt ? 1 - win(t, c.repairAt, 1.6) : 0;
    const lit = c.lightAt !== undefined && t >= c.lightAt;
    const nP = 9, len = pts.length;
    return <g key={i}>
      {segs.map((sg, k) => <g key={k}><path d={poly(sg)} fill="none" stroke={OL} strokeWidth={15} strokeLinecap="round" strokeLinejoin="round" />
        <path d={poly(sg)} fill="none" stroke={color} strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" />
        {lit && <path d={poly(sg)} fill="none" stroke={K.light} strokeWidth={3} strokeOpacity={0.55} />}</g>)}
      {healed > 0 && <path d={poly(pts.filter((q) => Math.abs(q[0] - bx) < 90))} fill="none" stroke="#7BD389" strokeWidth={22} strokeOpacity={0.6 * healed} strokeLinecap="round" />}
      {lit && Array.from({length: nP}, (_, k) => {
        const u = ((t - c.lightAt!) * 0.22 + k / nP) % 1, idx = Math.floor(u * (len - 1)), q = pts[idx];
        if (broken && gaps.some((g) => q[0] > g - 26)) return null;
        return <g key={'p' + k}><circle cx={q[0]} cy={q[1]} r={16} fill={K.light} opacity={0.25} /><circle cx={q[0]} cy={q[1]} r={7} fill={K.white} /></g>;
      })}
      {broken && gaps.map((g, k) => { const sp = win(t, c.breakAt!, 1.4); const gy = (pts.find((q) => Math.abs(q[0] - g) < 30) || pts[0])[1];
        return <g key={'b' + k}>
          {sp < 1 && Array.from({length: 8}, (_, j) => { const an = j * 0.785; const r = 14 + 60 * sp;
            return <path key={j} d={`M ${g + Math.cos(an) * r * 0.4} ${gy + Math.sin(an) * r * 0.4} L ${g + Math.cos(an) * r} ${gy + Math.sin(an) * r}`} stroke={K.gold} strokeWidth={5} strokeLinecap="round" opacity={1 - sp} />; })}
          <path d={`M ${g - 30} ${gy - 10} l 8 8 l -8 8 M ${g + 30} ${gy - 10} l -8 8 l 8 8`} fill="none" stroke={K.red} strokeWidth={5} strokeLinecap="round" />
        </g>; })}
      {c.label && <text x={pts[Math.floor(len * 0.5)][0]} y={pts[Math.floor(len * 0.5)][1] + 46} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={800} fontSize={24} fill={K.white} stroke={OL} strokeWidth={1}>{c.label}</text>}
    </g>;
  };

  // ------------------------------------------------ coasts
  const coastNode = (side: 'left' | 'right') => {
    const L = side === 'left', x0 = L ? -2000 : worldW - cw, x1 = L ? cw : worldW + 2000, top = sea - 60;
    const ls = L ? cw - 70 : worldW - cw + 70;          // landing station x
    const dc = L ? cw - 230 : worldW - cw + 230;        // data center x
    const dark = coasts.darkAt !== undefined && t >= coasts.darkAt;
    const blink = (k: number) => (Math.sin(t * 6 + k * 1.7) > 0 ? K.light : '#2A3550');
    const slope = L ? `M ${x0} ${top} L ${cw} ${top} Q ${cw + 160} ${top + 40} ${cw + 320} ${groundY(cw + 320) + 30} L ${cw + 320} ${bed + 400} L ${x0} ${bed + 400} Z`
      : `M ${x1} ${top} L ${worldW - cw} ${top} Q ${worldW - cw - 160} ${top + 40} ${worldW - cw - 320} ${groundY(worldW - cw - 320) + 30} L ${worldW - cw - 320} ${bed + 400} L ${x1} ${bed + 400} Z`;
    return <g key={side}>
      <path d={slope} fill={K.sand2} stroke={OL} strokeWidth={5} />
      <rect x={x0} y={top - 16} width={x1 - x0} height={26} fill={K.land} stroke={OL} strokeWidth={4} />
      {coasts.port ? <g transform={`translate(${dc} ${top - 16})`}>
        {[0, 1, 2].map((r) => [0, 1, 2, 3].map((c2) => <rect key={`${r}${c2}`} x={-90 + c2 * 44} y={-34 - r * 32} width={42} height={30} rx={3}
          fill={['#4FB3F6', '#FFC93C', '#7BD389', '#FF8A65'][(r + c2) % 4]} stroke={OL} strokeWidth={3} />))}
        <g transform={`translate(${L ? 110 : -110} 0)`}>
          <path d="M -30 0 L -30 -230 M 30 0 L 30 -230 M -30 -230 L 30 -230 M -30 -120 L 30 -120 M -30 -60 L 30 -10 M 30 -60 L -30 -10" fill="none" stroke="#E2504C" strokeWidth={10} strokeLinecap="round" />
          <path d={`M ${L ? -60 : 60} -230 L ${L ? 230 : -230} -230`} stroke="#E2504C" strokeWidth={12} strokeLinecap="round" />
          <path d={`M ${L ? 150 + 40 * Math.sin(t * 0.6) : -150 - 40 * Math.sin(t * 0.6)} -230 L ${L ? 150 + 40 * Math.sin(t * 0.6) : -150 - 40 * Math.sin(t * 0.6)} ${-150 + 30 * Math.sin(t * 0.9)}`} stroke={OL} strokeWidth={3} />
          <rect x={(L ? 150 + 40 * Math.sin(t * 0.6) : -150 - 40 * Math.sin(t * 0.6)) - 21} y={-150 + 30 * Math.sin(t * 0.9)} width={42} height={28} rx={3} fill="#B39DDB" stroke={OL} strokeWidth={3} />
        </g></g> : <>
      <g transform={`translate(${dc} ${top - 16})`}>
        <rect x={-70} y={-130} width={140} height={130} rx={10} fill="#DDE3EE" stroke={OL} strokeWidth={5} />
        {[0, 1, 2].map((r) => [0, 1, 2].map((c2) => <circle key={`${r}${c2}`} cx={-36 + c2 * 36} cy={-100 + r * 34} r={7} fill={dark ? '#2A3550' : blink(r * 3 + c2)} stroke={OL} strokeWidth={2} />))}
        <text x={0} y={-146} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={20} fill={OL}>DATA CENTER</text>
      </g>
      <g transform={`translate(${ls} ${top - 16})`}>
        <rect x={-40} y={-60} width={80} height={60} rx={6} fill="#FFE08A" stroke={OL} strokeWidth={4} />
        <path d="M -48 -60 L 0 -92 L 48 -60 Z" fill="#E2504C" stroke={OL} strokeWidth={4} strokeLinejoin="round" />
      </g>
      <path d={`M ${dc + (L ? 70 : -70)} ${top - 40} L ${ls + (L ? -40 : 40)} ${top - 40}`} stroke={K.light} strokeWidth={5} strokeDasharray="10 8" strokeDashoffset={-t * 60} />
      </>}
      {(L ? coasts.leftLabel : coasts.rightLabel) && <text x={(dc + ls) / 2} y={top + 140} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={30} fill={K.white} stroke={OL} strokeWidth={1.5}>{L ? coasts.leftLabel : coasts.rightLabel}</text>}
    </g>;
  };

  // ------------------------------------------------ callouts (cartoon speech bubbles)
  const calloutNode = (c: CartoonCallout, i: number, screen: boolean) => {
    if (t < c.at || (c.until !== undefined && t > c.until + 0.4)) return null;
    const u = E.outBack(win(t, c.at, 0.45)), o = c.until !== undefined ? 1 - win(t, c.until, 0.4) : 1;
    const size = c.size ?? 34, w = Math.max(c.text.length * size * 0.6, (c.sub || '').length * 13) + 60, h = c.sub ? size + 56 : size + 34;
    const col = c.color === 'risk' ? K.red : c.color === 'gold' ? K.gold : c.color === 'green' ? '#7BD389' : K.white;
    return <g key={i} opacity={o} transform={`translate(${c.x} ${c.y}) scale(${u}) rotate(${Math.sin(t * 1.5 + i) * 1.2})`}>
      {c.tail && <path d={`M -16 ${h / 2 - 4} L ${c.tail[0] - c.x} ${c.tail[1] - c.y} L 16 ${h / 2 - 4} Z`} fill={col} stroke={OL} strokeWidth={4} strokeLinejoin="round" />}
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.4} fill={col} stroke={OL} strokeWidth={5} />
      <text x={0} y={c.sub ? -4 : size * 0.36} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={size} fill={OL}>{c.text}</text>
      {c.sub && <text x={0} y={size * 0.36 + 20} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={700} fontSize={20} fill={OL} opacity={0.8}>{c.sub}</text>}
    </g>;
  };

  // ------------------------------------------------ fish (ambient)
  const fishNode = (i: number) => {
    const dir = i % 2 ? -1 : 1, sp = 50 + rnd(i) * 60, span = worldW + 1200;
    const x = dir > 0 ? ((t * sp + rnd(i + 1) * span) % span) - 600 : worldW + 600 - ((t * sp + rnd(i + 1) * span) % span);
    const y = sea + 160 + rnd(i + 2) * (bed - sea - 300) + Math.sin(t * 2 + i) * 14;
    const c = ['#FF8A65', '#FFD54A', '#F06292', '#4DD0E1'][i % 4];
    return <g key={'f' + i}>{[0, 1, 2].map((k) => { const wig = Math.sin(t * 10 + k + i) * 8;
      return <g key={k} transform={`translate(${x - dir * k * 46} ${y + (k % 2) * 26}) scale(${dir} 1)`}>
        <path d="M -22 0 Q 0 -18 22 0 Q 0 18 -22 0 Z" fill={c} stroke={OL} strokeWidth={3} />
        <path d={`M -22 0 L -38 ${-12 + wig * 0.4} L -38 ${12 + wig * 0.4} Z`} fill={c} stroke={OL} strokeWidth={3} strokeLinejoin="round" />
        <circle cx={10} cy={-3} r={3} fill={OL} /></g>; })}</g>;
  };

  const sky = p.night ? ['#1B2A5A', '#3D4F8F'] : [K.sky1, K.sky2];
  const sunY = 240 + Math.sin(t * 0.8) * 8;
  const ban = p.banner, bu = ban ? E.outBack(win(t, ban.at ?? 0.3, 0.6)) : 0;
  return (
    <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
      <defs>
        <linearGradient id="cskyg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={sky[0]} /><stop offset="100%" stopColor={sky[1]} /></linearGradient>
        <linearGradient id="cseag" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={K.sea1} /><stop offset="45%" stopColor={K.sea2} /><stop offset="100%" stopColor={K.sea3} /></linearGradient>
      </defs>
      <rect width={W} height={H} fill={K.sea3} />
      <g transform={camT}>
        <rect x={-3000} y={-3000} width={worldW + 6000} height={3000 + sea + 40} fill="url(#cskyg)" />
        <g transform={`translate(${cx + 560} 0)`}>{/* the sun keeps its place on screen (top right) */}
          <circle cx={0} cy={sunY} r={70} fill={K.sun} stroke={OL} strokeWidth={5} />
          <circle cx={-22} cy={sunY - 10} r={7} fill={OL} /><circle cx={22} cy={sunY - 10} r={7} fill={OL} />
          <path d={`M -25 ${sunY + 18} Q 0 ${sunY + 38} 25 ${sunY + 18}`} fill="none" stroke={OL} strokeWidth={5} strokeLinecap="round" />
        </g>
        <g transform={`translate(${cx * 0.6} 0)`}>{/* clouds with parallax */}
          {[0, 1, 2, 3].map((i) => { const x = ((i * 700 + t * 18) % 3400) - 1700, y = 90 + (i % 2) * 70;
            return <g key={i} transform={`translate(${x} ${y})`}><path d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill={K.white} stroke={OL} strokeWidth={4} /></g>; })}
        </g>
        <rect x={-3000} y={sea} width={worldW + 6000} height={3000} fill="url(#cseag)" />
        {Array.from({length: 7}, (_, i) => <path key={'ray' + i} d={`M ${i * (worldW / 6) + Math.sin(t * 0.5 + i) * 40} ${sea} l 120 ${bed - sea} l 90 0 Z`} fill={K.white} opacity={0.05} />)}
        {Array.from({length: fish}, (_, i) => fishNode(i))}
        {Array.from({length: 18}, (_, i) => { const u = ((t * 0.15 + rnd(i)) % 1), x = rnd(i + 9) * worldW + Math.sin(t * 2 + i) * 10;
          return <circle key={'bb' + i} cx={x} cy={bed - u * (bed - sea)} r={4 + rnd(i + 4) * 6} fill="none" stroke={K.white} strokeWidth={2} opacity={0.4 * (1 - u)} />; })}
        <path d={`M -3000 ${bed + 400} L -3000 ${bedY(0)} ${Array.from({length: Math.ceil((worldW + 6000) / 30)}, (_, k) => { const x = -3000 + k * 30; return `L ${x} ${bedY(x).toFixed(1)}`; }).join(' ')} L ${worldW + 3000} ${bed + 400} Z`}
          fill={K.sand} stroke={OL} strokeWidth={5} />
        {Array.from({length: Math.ceil(worldW / 220)}, (_, i) => { const x = 110 + i * 220 + rnd(i) * 80, gy = bedY(x), sw = Math.sin(t * 1.6 + i) * 10;
          return <g key={'w' + i}>{rnd(i + 2) > 0.5 ? <path d={`M ${x} ${gy} Q ${x - 16 + sw} ${gy - 50} ${x + sw} ${gy - 100} M ${x + 14} ${gy} Q ${x + 30 + sw} ${gy - 40} ${x + 16 + sw} ${gy - 70}`} fill="none" stroke={K.weed} strokeWidth={9} strokeLinecap="round" />
            : <ellipse cx={x} cy={gy - 6} rx={34} ry={20} fill={K.rock} stroke={OL} strokeWidth={4} />}</g>; })}
        {coasts.left && coastNode('left')}
        {coasts.right && coastNode('right')}
        {cables.map(cableNode)}
        {actors.filter((a) => a.kind === 'volcano' || a.kind === 'whale').map(actorNode)}
        {waves(sea - 4, 10, 90, 70, K.sea1, 0.9)}
        {actors.filter((a) => a.kind === 'island').map(actorNode)}
        {actors.filter((a) => !['volcano', 'whale', 'island'].includes(a.kind)).map(actorNode)}
        <path d={Array.from({length: Math.ceil((worldW + 4000) / 40)}, (_, k) => { const x = -2000 + k * 40; return `${k ? 'L' : 'M'} ${x} ${surfY(x).toFixed(1)}`; }).join(' ')} fill="none" stroke={K.white} strokeWidth={5} opacity={0.85} />
        {callouts.filter((c) => !c.screen).map((c, i) => calloutNode(c, i, false))}
      </g>
      {callouts.filter((c) => c.screen).map((c, i) => calloutNode(c, 100 + i, true))}
      {ban && bu > 0 && <g transform={`translate(120 96) scale(${bu})`}>
        <rect x={0} y={0} width={Math.max(ban.text.length * 27, (ban.sub || '').length * 13) + 60} height={ban.sub ? 100 : 70} rx={18} fill={K.white} stroke={OL} strokeWidth={5} />
        <text x={30} y={48} fontFamily="Inter Display, Inter, sans-serif" fontWeight={900} fontSize={44} fill={OL}>{ban.text}</text>
        {ban.sub && <text x={32} y={82} fontFamily="Inter, sans-serif" fontWeight={700} fontSize={22} fill={OL} opacity={0.75}>{ban.sub}</text>}
      </g>}
    </svg>
  );
};
