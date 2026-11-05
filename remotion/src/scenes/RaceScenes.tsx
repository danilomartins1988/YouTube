import React, {useMemo} from 'react';
import {getLength} from '@remotion/paths';
import {pointAt, tangentAt} from '../lib/pathsafe';
import {eio, eo, lerp, rand, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';
import {RaceCar} from '../components/RaceCar';

const Y = (p: any) => p.accent3 || '#FFD21F';

/**
 * 2.5D trackside scene: sky, distant skyline, grandstand with a flickering crowd, barrier boards (generic
 * placeholders, no real logos), scrolling kerbs and tarmac at different parallax speeds, and cars that race
 * past and overtake. Camera shakes slightly with speed. Optional text block and on-board counter.
 */
export const RaceTrack: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const speed = p.speed || 900; // px/s of the track surface
  const horizon = H * 0.5;
  const shake = Math.sin(t * 37) * 2 + Math.sin(t * 23) * 1.5;
  const scroll = (k: number, period: number) => -((t * speed * k) % period);
  const cars: any[] = p.cars || [
    {body: pal.accent, trim: '#FFFFFF', number: '05'},
    {body: pal.accent2, trim: Y(pal), number: '17'},
    {body: Y(pal), trim: '#14161B', number: '88'},
  ];
  const boards: string[] = p.boards || ['YOUR BRAND', 'SPONSOR', 'PARTNER', 'YOUR BRAND'];
  return (
    <svg width={W} height={H}>
      <defs>
        <linearGradient id="rsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={pal.bg} />
          <stop offset="100%" stopColor={pal.bg2} />
        </linearGradient>
      </defs>
      <rect width={W} height={H} fill="url(#rsky)" />
      <g transform={`translate(0 ${shake})`}>
        {/* distant skyline (slow) */}
        <g transform={`translate(${scroll(0.05, 600)} 0)`}>
          {Array.from({length: 18}, (_, i) => {
            const h = 60 + rand(i) * 140;
            return <rect key={i} x={i * 140} y={horizon - 120 - h} width={100} height={h} fill={pal.land} opacity={0.7} />;
          })}
        </g>
        {/* grandstand + crowd */}
        <g transform={`translate(${scroll(0.15, 320)} 0)`}>
          {Array.from({length: 9}, (_, s) => (
            <g key={s} transform={`translate(${s * 320} 0)`}>
              <polygon points={`0,${horizon - 20} 300,${horizon - 20} 300,${horizon - 170} 0,${horizon - 120}`} fill={pal.border} />
              <rect x={-10} y={horizon - 186} width={320} height={14} fill={pal.accent} />
              {Array.from({length: 60}, (_, i) => {
                const cx = 10 + (i % 15) * 19, cy = horizon - 40 - Math.floor(i / 15) * 28 - (i % 15) * 2.4;
                const flick = rand(i + s * 61 + Math.floor(t * 6)) > 0.75;
                return <circle key={i} cx={cx} cy={cy} r={6} fill={flick ? Y(pal) : ['#FFFFFF', pal.accent2, pal.accent, pal.muted][(i + s) % 4]} opacity={0.75} />;
              })}
            </g>
          ))}
        </g>
        {/* barrier with sponsor placeholder boards */}
        <g transform={`translate(${scroll(0.55, 1600)} 0)`}>
          {Array.from({length: 3}, (_, k) => boards.map((b, i) => (
            <g key={`${k}-${i}`} transform={`translate(${k * 1600 + i * 400} ${horizon - 16})`}>
              <rect width={380} height={70} fill={i % 2 ? pal.accent2 : '#FFFFFF'} />
              <text x={190} y={48} textAnchor="middle" fontFamily={font.display} fontWeight={800} fontSize={34}
                fill={i % 2 ? '#FFFFFF' : pal.bg} letterSpacing={3}>{b}</text>
            </g>
          )))}
        </g>
        {/* tarmac */}
        <rect x={0} y={horizon + 54} width={W} height={H - horizon} fill="#24272E" />
        {/* kerbs (fast) */}
        <g transform={`translate(${scroll(1, 160)} 0)`}>
          {Array.from({length: Math.ceil(W / 80) + 4}, (_, i) => (
            <rect key={i} x={i * 80} y={horizon + 54} width={80} height={22} fill={i % 2 ? pal.accent : '#FFFFFF'} />
          ))}
        </g>
        {/* track markings and motion streaks */}
        <g transform={`translate(${scroll(1.2, 400)} 0)`}>
          {Array.from({length: Math.ceil(W / 200) + 4}, (_, i) => (
            <rect key={i} x={i * 200} y={H - 120} width={110} height={8} fill="#FFFFFF" opacity={0.6} />
          ))}
        </g>
        {cars.map((c, i) => {
          const enter = cue(c, 0.05 + i * 0.12);
          const lane = H - 170 - (i % 2) * 120;
          const base = W * (c.x ?? (0.12 + i * 0.28));
          // each car oscillates around its slot; overtakes swap slots on cue
          const swing = Math.sin(t * (0.8 + i * 0.3) + i) * 90;
          const arrive = eo(t, enter, 1.2);
          const x = lerp(-700, base + swing, arrive);
          return (
            <RaceCar key={i} x={x} y={lane} scale={c.scale || (i % 2 ? 0.75 : 0.9)} body={c.body} trim={c.trim} spin={t * 40}
              t={t + i} speedLines={1} number={c.number} />
          );
        })}
      </g>
      {(p.title || p.value) && (() => {
        const u = eo(t, Math.min(cue(p.kicker_cue, 0), cue(p.title_cue, 0.02)), 0.5);
        return <rect x={80 - 40 * (1 - u)} y={140} width={1060} height={p.subtitle ? 380 : 320} rx={18} fill={pal.bg} opacity={0.97 * u}
          stroke={pal.accent} strokeOpacity={0.5 * u} strokeWidth={2} />;
      })()}
      {p.kicker && <RiseText x={120} y={200} at={cue(p.kicker_cue, 0)} size={30} color={Y(pal)} weight={700} tracking={6}>{String(p.kicker).toUpperCase()}</RiseText>}
      {p.title && <RiseText x={120} y={290} at={cue(p.title_cue, 0.02)} size={88} weight={800} display>{p.title}</RiseText>}
      {p.value && <RiseText x={116} y={420} at={cue(p.value_cue, 0.2)} size={124} weight={800} display color={pal.accent}>{p.value}</RiseText>}
      {p.subtitle && <RiseText x={122} y={485} at={cue(p.subtitle_cue, 0.4)} size={40} color={pal.ink}>{p.subtitle}</RiseText>}
    </svg>
  );
};

// An original, fictional circuit (not a real track layout), designed to fit 1920x1080.
export const CIRCUIT =
  'M 420 760 L 1180 760 C 1300 760 1360 700 1380 620 L 1420 470 C 1440 400 1520 360 1590 380 L 1660 400 ' +
  'C 1740 425 1760 330 1700 290 L 1480 170 C 1420 140 1340 150 1300 200 L 1180 360 C 1150 400 1090 410 1050 380 ' +
  'L 900 270 C 850 235 780 240 740 285 L 620 430 C 590 465 540 470 505 445 L 400 370 C 330 320 240 360 240 440 ' +
  'L 250 620 C 255 710 330 760 420 760 Z';

/**
 * Top-down circuit: the track draws itself, then cars run laps with fading trails; sector markers and
 * optional callouts appear on cues along the lap (e.g. revenue streams 'around the calendar').
 */
export const Circuit: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const d = p.path || CIRCUIT;
  const L = useMemo(() => getLength(d), [d]);
  const draw = eio(t, cue(p.draw_cue, 0.0), p.draw_seconds || 2.2);
  const lapT = p.lap_seconds || 7;
  const cars: any[] = p.cars || [{colour: 'accent'}, {colour: 'accent2', offset: 0.06}, {colour: 'accent3', offset: 0.11}];
  const lapsStart = cue(p.draw_cue, 0) + (p.draw_seconds || 2.2);
  const markers: any[] = p.markers || [];
  const S = p.scale || 1, ox = p.ox ?? 0, oy = p.oy ?? 60;
  const tr = `translate(${ox} ${oy}) scale(${S})`;
  return (
    <svg width={W} height={H}>
      <g transform={tr}>
        <path d={d} fill="none" stroke="#2C3038" strokeWidth={58} strokeLinejoin="round" strokeDasharray={L} strokeDashoffset={L * (1 - draw)} />
        <path d={d} fill="none" stroke="#FFFFFF" strokeOpacity={0.9} strokeWidth={4} strokeDasharray="18 16" strokeDashoffset={-t * 40}
          opacity={draw >= 1 ? 0.5 : 0} />
        <path d={d} fill="none" stroke={pal.accent} strokeWidth={6} strokeDasharray={L} strokeDashoffset={L * (1 - draw)} opacity={0.9}
          transform="translate(0 0)" />
        {/* start/finish line */}
        {draw >= 1 && Array.from({length: 6}, (_, i) => <rect key={i} x={560 + (i % 2) * 10} y={732 + Math.floor(i / 2) * 18} width={10} height={18} fill={i % 2 ? '#000' : '#fff'} />)}
        {cars.map((c, i) => {
          if (t < lapsStart) return null;
          const prog = (((t - lapsStart) / (lapT * (1 + (c.slow || 0))) + (c.offset || 0)) % 1 + 1) % 1;
          const colour = pal[c.colour] || c.colour;
          const trail = Array.from({length: 10}, (_, k) => {
            const q = ((prog - k * 0.006) % 1 + 1) % 1;
            const pt = pointAt(d, q * L);
            return <circle key={k} cx={pt.x} cy={pt.y} r={12 - k} fill={colour} opacity={(1 - k / 10) * 0.6} />;
          });
          const pt = pointAt(d, prog * L);
          const tg = tangentAt(d, prog * L);
          const ang = (Math.atan2(tg.y, tg.x) * 180) / Math.PI;
          return (
            <g key={i}>
              {trail}
              <g transform={`translate(${pt.x} ${pt.y}) rotate(${ang})`}>
                <rect x={-22} y={-10} width={44} height={20} rx={8} fill={colour} stroke="#000" strokeOpacity={0.4} />
                <rect x={10} y={-12} width={8} height={24} fill="#14161B" />
              </g>
            </g>
          );
        })}
        {markers.map((m, i) => {
          const at = cue(m, 0.2 + i * 0.15);
          const u = eo(t, at, 0.5);
          if (u <= 0) return null;
          const pt = pointAt(d, (m.along || 0) * L);
          const dx = m.dx ?? 60, dy = m.dy ?? -60;
          return (
            <g key={i} opacity={u}>
              <line x1={pt.x} y1={pt.y} x2={pt.x + dx * u} y2={pt.y + dy * u} stroke={pal[m.colour || 'accent3'] || m.colour} strokeWidth={3} />
              <circle cx={pt.x} cy={pt.y} r={10} fill={pal[m.colour || 'accent3'] || m.colour} />
              <rect x={pt.x + dx - (dx < 0 ? 300 : 0)} y={pt.y + dy - 40} width={300} height={m.value ? 96 : 56} rx={10} fill={pal.bg} opacity={0.9}
                stroke={pal[m.colour || 'accent3'] || m.colour} strokeWidth={2} />
              <text x={pt.x + dx - (dx < 0 ? 284 : -16)} y={pt.y + dy - 6} fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={24}>{m.label}</text>
              {m.value && <text x={pt.x + dx - (dx < 0 ? 284 : -16)} y={pt.y + dy + 40} fill={pal[m.colour || 'accent3'] || m.colour}
                fontFamily={font.display} fontWeight={800} fontSize={40}>{m.value}</text>}
            </g>
          );
        })}
      </g>
      {p.title && <RiseText x={120} y={200} at={cue(p.title_cue, 0)} size={60} weight={800} display>{p.title}</RiseText>}
      {p.subtitle && <RiseText x={122} y={246} at={cue(p.subtitle_cue, 0.05)} size={30} color={pal.muted}>{p.subtitle}</RiseText>}
      {p.lap_label && t >= lapsStart && (
        <g>
          <rect x={W - 340} y={170} width={220} height={90} rx={12} fill={pal.bg2} stroke={pal.accent} strokeWidth={2} />
          <text x={W - 230} y={208} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontWeight={700} fontSize={20} letterSpacing={3}>{String(p.lap_label).toUpperCase()}</text>
          <text x={W - 230} y={248} textAnchor="middle" fill={pal.ink} fontFamily={font.display} fontWeight={800} fontSize={36}>
            {`${Math.min(p.laps_total || 99, 1 + Math.floor((t - lapsStart) / lapT))}${p.laps_total ? ' / ' + p.laps_total : ''}`}
          </text>
        </g>
      )}
    </svg>
  );
};

export const _r = rand;
