import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';

/** Kinetic-typography Short (1080x1920), text + voice only, no characters (owner request 2026-11-12).
 *  Continuous motion: animated gradient/grid/particles/light sweep background, a per-beat camera (push-in, slight 3D tilt,
 *  whip pan + glitch between beats), physics text (slam with squash-and-stretch + overshoot), split-flap numbers,
 *  tearing calendar pages, self-drawing arrows, a stamp with screen shake and ink splatter, karaoke captions, end card. */

type Word = {w: string; s: number; e: number; seg: string; i: number};
type El = {type: string; at: number; until?: number; text?: string; sub?: string; color?: string; x?: number; y?: number; size?: number;
  rot?: number; items?: {label: string; sub?: string; cue?: number}[]; cues?: number[]; from?: [number, number]; to?: [number, number]; ok?: boolean};
type Beat = {seg: string; s: number; e: number; bg?: string[]; els: El[]};
type Props = {words: Word[]; beats: Beat[]; total: number; endCard: number; disclaimer: string; asof: string};

const W = 1080, H = 1920, FONT = 'Inter Display, Inter, sans-serif', INK = '#0B0B12';
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const win = (t: number, a: number, d: number) => clamp((t - a) / d);
const easeOut = (u: number) => 1 - Math.pow(1 - u, 3);
const outBack = (u: number, k = 1.9) => 1 + (k + 1) * Math.pow(u - 1, 3) + k * Math.pow(u - 1, 2);
const spring = (u: number) => u >= 1 ? 1 : 1 - Math.exp(-6 * u) * Math.cos(11 * u);   // overshoot + settle
const rnd = (k: number) => { const x = Math.sin(k * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

const Background: React.FC<{t: number; bg: string[]}> = ({t, bg}) => {
  const [c0, c1] = bg;
  const gx = 50 + 30 * Math.sin(t * 0.35), gy = 40 + 25 * Math.cos(t * 0.27);
  return <svg width={W} height={H} style={{position: 'absolute'}}>
    <defs>
      <radialGradient id="g" cx={`${gx}%`} cy={`${gy}%`} r="85%"><stop offset="0" stopColor={c1} /><stop offset="1" stopColor={c0} /></radialGradient>
      <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stopColor="#FFFFFF" stopOpacity={0} /><stop offset="0.5" stopColor="#FFFFFF" stopOpacity={0.13} /><stop offset="1" stopColor="#FFFFFF" stopOpacity={0} /></linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#g)" />
    {/* perspective grid scrolling toward the viewer */}
    <g opacity={0.16} stroke="#FFFFFF" strokeWidth={2}>
      {Array.from({length: 14}, (_, k) => { const u = ((k / 14) + t * 0.12) % 1, y = 1250 + Math.pow(u, 2.2) * 700;
        return <line key={'h' + k} x1={0} y1={y} x2={W} y2={y} opacity={u} />; })}
      {Array.from({length: 13}, (_, k) => { const x = (k - 6) * 180; return <line key={'v' + k} x1={W / 2 + x * 0.25} y1={1250} x2={W / 2 + x * 2.2} y2={H} />; })}
    </g>
    {Array.from({length: 46}, (_, k) => { const sp = 0.03 + rnd(k) * 0.07, u = (rnd(k + 9) + t * sp) % 1;
      return <circle key={k} cx={rnd(k + 3) * W + 30 * Math.sin(t * 0.8 + k)} cy={H - u * H} r={2 + rnd(k + 5) * 5} fill="#FFFFFF" opacity={0.08 + 0.25 * Math.sin(u * Math.PI)} />; })}
    <rect x={-600 + ((t * 420) % 2600)} y={0} width={500} height={H} fill="url(#sweep)" transform="skewX(-18)" />
  </svg>;
};

/** big word that slams in: drops from scale 2.4 with squash-and-stretch and overshoot, then breathes */
const Slam: React.FC<{e: El; t: number}> = ({e, t}) => {
  const u = win(t, e.at, 0.55), sp = spring(u), size = e.size ?? 150;
  const sq = u < 1 ? 1 + 0.35 * Math.sin(u * Math.PI * 2.2) * (1 - u) : 1;
  const breathe = 1 + 0.015 * Math.sin((t - e.at) * 3);
  const s = (2.4 - 1.4 * sp) * breathe;
  return <g transform={`translate(${e.x ?? W / 2} ${e.y ?? 700}) rotate(${(e.rot ?? 0) * sp + 1.2 * Math.sin((t - e.at) * 1.7)}) scale(${s * sq} ${s / sq})`} opacity={clamp(u * 4)}>
    <text x={8} y={10} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill={INK} opacity={0.35} letterSpacing={-3}>{e.text}</text>
    <text textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill={e.color ?? '#FFFFFF'} stroke={INK} strokeWidth={size * 0.06} paintOrder="stroke" letterSpacing={-3}>{e.text}</text>
    {e.sub && <text y={size * 0.62} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={Math.min(size * 0.32, 880 / (e.sub.length * 0.64))} fill="#FFFFFF" opacity={clamp((t - e.at - 0.25) * 3)}>{e.sub}</text>}
  </g>;
};

/** bouncy letters: each letter hops in with a stagger and keeps a gentle wave */
const Bounce: React.FC<{e: El; t: number}> = ({e, t}) => {
  const txt = e.text ?? '', size = e.size ?? 110, cw = size * 0.66, x0 = (e.x ?? W / 2) - (txt.length * cw) / 2 + cw / 2;
  return <g>{txt.split('').map((ch, k) => { const u = win(t, e.at + k * 0.045, 0.45), y = (e.y ?? 700) - 160 * (1 - outBack(u)) + 8 * Math.sin((t - e.at) * 5 + k * 0.6);
    return <text key={k} x={x0 + k * cw} y={y} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill={e.color ?? '#FFFFFF'}
      stroke={INK} strokeWidth={size * 0.06} paintOrder="stroke" opacity={clamp(u * 3)} transform={`rotate(${(1 - u) * -25} ${x0 + k * cw} ${y})`}>{ch}</text>; })}</g>;
};

/** split-flap board: each tile flips through random glyphs before settling on its character */
const Flap: React.FC<{e: El; t: number}> = ({e, t}) => {
  const txt = e.text ?? '', size = e.size ?? 170, tw = size * 0.78, th = size * 1.15, x0 = (e.x ?? W / 2) - (txt.length * (tw + 12)) / 2;
  const glyphs = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  return <g transform={`translate(0 ${(e.y ?? 700) - th / 2}) scale(1)`}>
    {txt.split('').map((ch, k) => { const settle = e.at + 0.12 + k * 0.06, done = t >= settle, flipU = (t * 14) % 1;
      const g = ch === ' ' ? ' ' : done ? ch : glyphs[Math.floor(rnd(Math.floor(t * 14) + k * 7) * glyphs.length)];
      const vis = t >= e.at; if (!vis || ch === ' ') return null;
      const sy = done ? 1 - 0.25 * Math.max(0, 1 - (t - settle) * 6) : Math.abs(Math.cos(flipU * Math.PI));
      return <g key={k} transform={`translate(${x0 + k * (tw + 12) + tw / 2} ${th / 2}) scale(1 ${sy})`}>
        <rect x={-tw / 2} y={-th / 2} width={tw} height={th} rx={16} fill="#14161F" stroke="#000" strokeWidth={6} />
        <line x1={-tw / 2} y1={0} x2={tw / 2} y2={0} stroke="#000" strokeWidth={5} />
        <text y={size * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill={e.color ?? '#FFD23F'}>{g}</text></g>; })}
    {e.sub && <text x={e.x ?? W / 2} y={th + 90} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size * 0.5} fill="#FFFFFF" stroke={INK} strokeWidth={8} paintOrder="stroke"
      opacity={clamp((t - e.at - 0.12 - txt.length * 0.06) * 3)}>{e.sub}</text>}
  </g>;
};

/** strike: text that gets crossed out by a red line drawing itself, then shakes */
const Strike: React.FC<{e: El; t: number}> = ({e, t}) => {
  const u = win(t, e.at, 0.4), cut = win(t, e.at + 0.55, 0.35), size = e.size ?? 100, w = (e.text ?? '').length * size * 0.6;
  const sh = cut > 0 && cut < 1 ? 6 * Math.sin(t * 60) : 0;
  return <g transform={`translate(${(e.x ?? W / 2) + sh} ${e.y ?? 700}) scale(${0.6 + 0.4 * easeOut(u)})`} opacity={u}>
    <text textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill="#FFFFFF" stroke={INK} strokeWidth={6} paintOrder="stroke" opacity={1 - 0.45 * cut}>{e.text}</text>
    <line x1={-w / 2} y1={-size * 0.32} x2={-w / 2 + w * cut} y2={-size * 0.32 + 10 * cut} stroke="#FF3B47" strokeWidth={18} strokeLinecap="round" />
  </g>;
};

/** arrow that draws itself with a glowing head */
const Arrow: React.FC<{e: El; t: number}> = ({e, t}) => {
  const [a, b] = [e.from ?? [300, 900], e.to ?? [780, 900]], u = easeOut(win(t, e.at, 0.5));
  const mx = (a[0] + b[0]) / 2, my = Math.min(a[1], b[1]) - 120, len = 900;
  const ang = Math.atan2(b[1] - my, b[0] - mx) * 180 / Math.PI;
  return <g opacity={clamp(u * 3)}>
    <path d={`M ${a[0]} ${a[1]} Q ${mx} ${my} ${b[0]} ${b[1]}`} fill="none" stroke={e.color ?? '#FFD23F'} strokeWidth={16} strokeLinecap="round"
      strokeDasharray={len} strokeDashoffset={len * (1 - u)} />
    {u > 0.92 && <g transform={`translate(${b[0]} ${b[1]}) rotate(${ang}) scale(${outBack(win(t, e.at + 0.45, 0.3))})`}><path d="M 0 0 L -44 -26 L -44 26 Z" fill={e.color ?? '#FFD23F'} stroke={INK} strokeWidth={4} /></g>}
  </g>;
};

/** three calendar pages JAN -> FEV -> MAR; at each cue the current page tears off and flies away */
const Cal: React.FC<{e: El; t: number}> = ({e, t}) => {
  const items = e.items ?? [], cues = e.cues ?? [], cx = e.x ?? W / 2, cy = e.y ?? 760;
  const appear = outBack(win(t, e.at, 0.5));
  let cur = 0; cues.forEach((c, k) => { if (t >= c) cur = k; });
  return <g transform={`translate(${cx} ${cy}) scale(${appear}) rotate(${2 * Math.sin(t * 1.3)})`}>
    {/* stack behind */}
    {[2, 1].map((d) => <rect key={d} x={-260 + d * 10} y={-300 + d * 10} width={520} height={600} rx={30} fill="#E6E9F2" stroke={INK} strokeWidth={8} />)}
    {items.map((it, k) => { if (k < cur - 1 || k > cur) return null;
      const tear = k < cur ? win(t, cues[k + 1], 0.6) : 0, fly = easeOut(tear);
      return <g key={k} transform={`translate(${380 * fly} ${-520 * fly + 900 * tear * tear}) rotate(${50 * fly})`} opacity={1 - tear * 0.9}>
        <rect x={-260} y={-300} width={520} height={600} rx={30} fill="#FFFFFF" stroke={INK} strokeWidth={8} />
        <rect x={-260} y={-300} width={520} height={150} rx={30} fill={['#FF3B47', '#2E86FF', '#00B37E'][k % 3]} stroke={INK} strokeWidth={8} />
        {[-140, 140].map((dx) => <rect key={dx} x={dx - 14} y={-336} width={28} height={78} rx={14} fill="#9AA7B8" stroke={INK} strokeWidth={5} />)}
        <text y={-200} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={90} fill="#FFFFFF">{it.label}</text>
        <text y={40} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={84} fill={INK}>{it.sub}</text>
        <text y={150} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={54} fill="#5A6680">2027</text>
      </g>; })}
    {/* progress dots */}
    {items.map((_, k) => <circle key={'d' + k} cx={-60 + k * 60} cy={360} r={16} fill={k <= cur ? '#FFD23F' : '#FFFFFF'} stroke={INK} strokeWidth={5} />)}
  </g>;
};

/** rubber stamp: drops from above, hits with screen shake (returned via shake()), ink splatter */
const stampHit = (e: El) => e.at + 0.35;
const Stamp: React.FC<{e: El; t: number}> = ({e, t}) => {
  const hit = stampHit(e), u = win(t, e.at, 0.35), s = t < hit ? 3 - 2 * easeOut(u) : 1 + 0.08 * Math.max(0, 1 - (t - hit) * 5);
  const w = (e.text ?? '').length * (e.size ?? 84) * 0.62 + 80, hgt = (e.size ?? 84) * 1.6;
  return <g transform={`translate(${e.x ?? W / 2} ${e.y ?? 1000}) rotate(${e.rot ?? -9}) scale(${s})`} opacity={clamp(u * 3)}>
    {t >= hit && Array.from({length: 18}, (_, k) => { const a = rnd(k) * Math.PI * 2, d = (w / 2 + 40) * (0.6 + rnd(k + 4) * 0.7) * easeOut(win(t, hit, 0.25));
      return <circle key={k} cx={Math.cos(a) * d} cy={Math.sin(a) * d * 0.5} r={6 + rnd(k + 8) * 16} fill="#E0252F" opacity={0.85} />; })}
    <rect x={-w / 2} y={-hgt / 2} width={w} height={hgt} rx={18} fill="none" stroke="#E0252F" strokeWidth={14} />
    <rect x={-w / 2 + 16} y={-hgt / 2 + 16} width={w - 32} height={hgt - 32} rx={10} fill="none" stroke="#E0252F" strokeWidth={5} />
    <text y={(e.size ?? 84) * 0.35} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={e.size ?? 84} fill="#E0252F" letterSpacing={2}>{e.text}</text>
  </g>;
};

/** check or X badge popping in */
const Badge: React.FC<{e: El; t: number}> = ({e, t}) => {
  const u = outBack(win(t, e.at, 0.45)), ok = e.ok !== false, c = ok ? '#00C27A' : '#FF3B47';
  return <g transform={`translate(${e.x ?? W / 2} ${e.y ?? 900}) scale(${u}) rotate(${6 * Math.sin((t - e.at) * 4)})`}>
    <circle r={70} fill={c} stroke={INK} strokeWidth={8} />
    <path d={ok ? 'M -32 2 L -8 28 L 36 -24' : 'M -28 -28 L 28 28 M 28 -28 L -28 28'} fill="none" stroke="#FFFFFF" strokeWidth={18} strokeLinecap="round" strokeLinejoin="round" />
    {e.text && <text x={100} y={22} fontFamily={FONT} fontWeight={900} fontSize={e.size ?? 60} fill="#FFFFFF" stroke={INK} strokeWidth={6} paintOrder="stroke">{e.text}</text>}
  </g>;
};

const EL: Record<string, React.FC<{e: El; t: number}>> = {slam: Slam, bounce: Bounce, flap: Flap, strike: Strike, arrow: Arrow, cal: Cal, stamp: Stamp, badge: Badge};

/** karaoke caption: the current phrase (<= 4 words), current word highlighted and lifted */
const Caption: React.FC<{words: Word[]; t: number}> = ({words, t}) => {
  let i = words.findIndex((w) => t >= w.s - 0.05 && t <= w.e + 0.25);
  if (i < 0) return null;
  // phrase groups inside the segment: at most 4 words and ~20 characters, so the caption stays big
  const seg = words.filter((w) => w.seg === words[i].seg), groups: Word[][] = [];
  for (const w of seg) { const g = groups[groups.length - 1]; const len = g ? g.reduce((a, x) => a + x.w.length + 1, 0) : 99;
    if (!g || g.length >= 4 || len + w.w.length > 20) groups.push([w]); else g.push(w); }
  const grp = groups.find((g) => g.includes(words[i]))!;
  const raw = grp.reduce((a, w) => a + w.w.length * 0.7, 0) + 0.45 * (grp.length - 1);
  const size = Math.min(70, 940 / Math.max(1, raw)), gap = size * 0.45, widths = grp.map((w) => w.w.length * size * 0.7), tot = widths.reduce((a, b) => a + b, 0) + gap * (grp.length - 1);
  let x = W / 2 - tot / 2;
  return <svg width={W} height={H} style={{position: 'absolute'}}>
    {grp.map((w, k) => { const cx = x + widths[k] / 2; x += widths[k] + gap; const on = t >= w.s && t <= w.e + 0.15, lift = on ? -10 : 0;
      return <text key={k} x={cx} y={1395 + lift} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={size} fill={on ? '#FFD23F' : '#FFFFFF'}
        stroke={INK} strokeWidth={12} paintOrder="stroke">{w.w.toUpperCase()}</text>; })}
  </svg>;
};

export const KineticShort: React.FC<Props> = ({words, beats, total, endCard, disclaimer, asof}) => {
  const f = useCurrentFrame(), {fps} = useVideoConfig(), t = f / fps;
  const bi = Math.max(0, beats.findIndex((b, k) => t >= b.s - 0.15 && (k === beats.length - 1 || t < beats[k + 1].s - 0.15)));
  const beat = beats[bi], bg = beat?.bg ?? ['#0E1530', '#2B3FA0'];
  // camera: push-in over the beat, slight 3D tilt, whip pan + glitch on beat change, shake on stamp hits
  const local = t - (beat?.s ?? 0), push = 1 + 0.05 * clamp(local / Math.max(1, (beat.e - beat.s)));
  const enter = win(t, (beat?.s ?? 0) - 0.15, 0.32), whip = (1 - easeOut(enter)) * (bi % 2 ? -1 : 1) * W * 0.9;
  const stamps = beats.flatMap((b) => b.els.filter((e) => e.type === 'stamp')), sh = stamps.reduce((a, e) => { const d = t - stampHit(e); return d > 0 && d < 0.35 ? a + 22 * (1 - d / 0.35) : a; }, 0);
  const shx = sh * Math.sin(t * 90), shy = sh * Math.cos(t * 77);
  const tilt = 4 * Math.sin(t * 0.6), glitch = enter < 1 && enter > 0;
  const inEnd = t >= total;
  return (
    <AbsoluteFill style={{backgroundColor: '#0B0F1A', overflow: 'hidden'}}>
      <Background t={t} bg={inEnd ? ['#0B0F1A', '#1B2440'] : bg} />
      {!inEnd && beat && <AbsoluteFill style={{transform: `translate(${whip + shx}px, ${shy}px) perspective(1600px) rotateY(${tilt}deg) rotateX(${1.5 * Math.cos(t * 0.5)}deg) scale(${push})`,
        filter: glitch ? `blur(${(1 - enter) * 8}px)` : undefined}}>
        <svg width={W} height={H}>
          {beat.els.map((e, k) => { if (t < e.at || (e.until !== undefined && t > e.until)) return null; const C = EL[e.type]; return C ? <C key={k} e={e} t={t} /> : null; })}
        </svg>
      </AbsoluteFill>}
      {glitch && !inEnd && <svg width={W} height={H} style={{position: 'absolute', mixBlendMode: 'screen'}}>
        {Array.from({length: 7}, (_, k) => <rect key={k} x={0} y={rnd(k + Math.floor(t * 30)) * H} width={W} height={8 + rnd(k + 3) * 30} fill={k % 2 ? '#FF2D6F' : '#22E6FF'} opacity={0.35 * (1 - enter)} />)}
      </svg>}
      {!inEnd && <Caption words={words} t={t} />}
      {inEnd && (() => { const u = win(t, total, 0.5), v = outBack(u);
        return <svg width={W} height={H} style={{position: 'absolute'}}>
          <g transform={`translate(${W / 2} 820) scale(${v}) rotate(${2 * Math.sin(t * 2)})`}>
            <rect x={-440} y={-230} width={880} height={460} rx={40} fill="#FFFFFF" stroke={INK} strokeWidth={10} />
            {disclaimer.split('|').map((ln, k) => <text key={k} y={-80 + k * 100} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={k ? 54 : 64} fill={k ? '#3A4560' : INK}>{ln}</text>)}
          </g>
          <text x={W / 2} y={1180} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={44} fill="#FFD23F" opacity={clamp((t - total - 0.4) * 3)}>{asof}</text>
          {Array.from({length: 3}, (_, k) => <circle key={k} cx={W / 2 - 50 + k * 50} cy={1290} r={12} fill="#FFFFFF" opacity={0.3 + 0.7 * Math.abs(Math.sin(t * 4 + k))} />)}
        </svg>; })()}
    </AbsoluteFill>
  );
};
