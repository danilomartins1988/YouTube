import React from 'react';
import {AbsoluteFill} from 'remotion';
import {eo, rand, useCtx} from '../lib/anim';

/** Navy gradient with slow-drifting particles and a faint grid: never a dead static background. */
export const Background: React.FC<{grid?: boolean; particles?: number; style?: string}> = ({grid = true, particles = 40, style}) => {
  const {t, W, H, pal} = useCtx();
  const dots = Array.from({length: particles}, (_, i) => {
    const x = (rand(i) * W + t * (6 + rand(i + 7) * 14)) % W;
    const y = (rand(i + 3) * H + Math.sin(t * 0.3 + i) * 12 + H) % H;
    const r = 1 + rand(i + 11) * 1.8;
    const o = 0.08 + rand(i + 5) * 0.18;
    return <circle key={i} cx={x} cy={y} r={r} fill={pal.accent} opacity={o} />;
  });
  const gx = (t * 8) % 80;
  return (
    <AbsoluteFill>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <defs>
          <radialGradient id="bgv" cx="50%" cy="45%" r="75%">
            <stop offset="0%" stopColor={pal.bg2} />
            <stop offset="100%" stopColor={pal.bg} />
          </radialGradient>
        </defs>
        <rect width={W} height={H} fill="url(#bgv)" />
        <defs>
          <radialGradient id="bokeh"><stop offset="0%" stopColor={pal.accent} stopOpacity={0.10} /><stop offset="100%" stopColor={pal.accent} stopOpacity={0} /></radialGradient>
          <radialGradient id="bokeh2"><stop offset="0%" stopColor={pal.accent2 || pal.ink} stopOpacity={0.08} /><stop offset="100%" stopColor={pal.accent2 || pal.ink} stopOpacity={0} /></radialGradient>
        </defs>
        {[0, 1, 2].map((i) => (
          <circle key={'g' + i} cx={W * (0.2 + 0.3 * i) + Math.sin(t * 0.21 + i * 2) * 260} cy={H * (0.35 + 0.2 * (i % 2)) + Math.cos(t * 0.17 + i) * 140}
            r={360 + 80 * Math.sin(t * 0.3 + i)} fill={i === 1 ? 'url(#bokeh2)' : 'url(#bokeh)'} />
        ))}
        {grid &&
          Array.from({length: Math.ceil(W / 80) + 2}, (_, i) => (
            <line key={'v' + i} x1={i * 80 - gx} y1={0} x2={i * 80 - gx} y2={H} stroke={pal.border} strokeOpacity={0.12} />
          ))}
        {grid &&
          Array.from({length: Math.ceil(H / 80) + 1}, (_, i) => (
            <line key={'h' + i} x1={0} y1={i * 80} x2={W} y2={i * 80} stroke={pal.border} strokeOpacity={0.1} />
          ))}
        {dots}
        {style === 'speed' && Array.from({length: 26}, (_, i) => {
          // diagonal speed streaks drifting right-to-left at different depths
          const depth = 0.4 + rand(i + 3) * 1.2;
          const x = W + 300 - ((t * 420 * depth + rand(i) * (W + 600)) % (W + 600));
          const y = rand(i + 8) * H;
          const len = 120 + rand(i + 2) * 260;
          const col = [pal.accent, pal.accent2, pal.accent3 || pal.accent, pal.ink][i % 4];
          return <line key={'s' + i} x1={x} y1={y} x2={x + len} y2={y - len * 0.18} stroke={col} strokeWidth={2 + depth * 2} strokeOpacity={0.10 + 0.08 * depth} strokeLinecap="round" />;
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Chapter tag, channel mark and on-screen source credits. */
export const Chrome: React.FC = () => {
  const {t, W, H, pal, font, scene} = useCtx();
  const a = eo(t, 0.15, 0.5);
  const chapter = scene.params.chapter ?? scene.chapter;
  const credits = scene.credits.filter(Boolean);
  const {hud} = useCtx();
  const hudOn = !!(hud && scene.params.mission && !scene.params.no_chrome);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        {chapter && !scene.params.no_chrome ? (
          <g opacity={a}>
            <rect x={120} y={92} width={36 * a} height={4} fill={pal.accent} />
            <text x={172} y={100} fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={22} letterSpacing={3}>
              {String(chapter).toUpperCase()}
            </text>
          </g>
        ) : null}
        {hudOn ? <MissionHud a={a} /> : scene.params.brand === false ? null : (
        <text x={W - 120} y={100} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={18} letterSpacing={4} opacity={0.8 * a}>
          THE HIDDEN ECONOMICS
        </text>)}
        {credits.length && !scene.params.no_credits ? (
          <text x={120} y={H - 60} fill={pal.muted} fontFamily={font.body} fontSize={20} opacity={0.9 * a}>
            {'Source: ' + credits.join('  ·  ')}
          </text>
        ) : null}
      </svg>
      {hudOn && scene.params.stamp ? <MissionStamp /> : null}
    </AbsoluteFill>
  );
};

/**
 * Game HUD (top right): "MISSION 2/5", one pip per mission (done = filled with a check, current = pulsing
 * ring, next = outline) and the current objective. A scene with params.stamp completes its mission at the stamp.
 */
const stampAt = (ctx: ReturnType<typeof useCtx>) => ctx.scene.params.stamp ? ctx.cue(ctx.scene.params.stamp_cue ?? 0.55) : Infinity;
const MissionHud: React.FC<{a: number}> = ({a}) => {
  const ctx = useCtx();
  const {t, W, pal, font, scene, hud} = ctx;
  const n = hud!.missions.length, m = Number(scene.params.mission);
  const doneNow = t >= stampAt(ctx) || scene.params.mission_done ? m : m - 1;               // missions completed at this moment
  const allDone = m > n;
  const right = W - 120, gap = 34, x0 = right - (n - 1) * gap;
  const obj = allDone ? 'ALL OBJECTIVES COMPLETE' : (hud!.objectives?.[m - 1] ? 'OBJECTIVE · ' + hud!.objectives[m - 1] : hud!.missions[m - 1]);
  const pulse = 0.5 + 0.5 * Math.sin(t * 4);
  return (
    <g opacity={a}>
      <text x={x0 - 26} y={92} textAnchor="end" fill={allDone || doneNow >= m ? pal.accent3 || pal.accent : pal.accent} fontFamily={font.body} fontWeight={800} fontSize={22} letterSpacing={3}>
        {allDone ? 'MISSIONS ' + n + '/' + n : 'MISSION ' + m + '/' + n}
      </text>
      {Array.from({length: n}, (_, i) => {
        const cx = x0 + i * gap, done = i < doneNow || allDone, cur = !allDone && i === m - 1 && !done;
        return <g key={i}>
          {cur && <circle cx={cx} cy={84} r={14 + 3 * pulse} fill="none" stroke={pal.accent} strokeOpacity={0.25 + 0.35 * pulse} strokeWidth={2} />}
          <circle cx={cx} cy={84} r={10} fill={done ? pal.accent3 || pal.accent : cur ? pal.accent : 'none'} fillOpacity={done ? 0.95 : cur ? 0.35 : 0}
            stroke={done ? pal.accent3 || pal.accent : cur ? pal.accent : pal.muted} strokeWidth={2.5} />
          {done && <path d={`M ${cx - 5} ${84} L ${cx - 1} ${88} L ${cx + 6} ${79}`} fill="none" stroke={pal.bg} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />}
        </g>;
      })}
      <text x={right + 10} y={128} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={17} letterSpacing={2.5}>
        {String(obj).toUpperCase()}
      </text>
    </g>
  );
};

/** "MISSION n COMPLETE" stamp: slams in at the stamp cue, slightly rotated, with a ring burst. */
const MissionStamp: React.FC = () => {
  const ctx = useCtx();
  const {t, W, H, pal, font, scene} = ctx;
  const at = stampAt(ctx);
  if (t < at) return null;
  const u = Math.min(1, (t - at) / 0.35);
  const sc = 1 + 1.4 * Math.pow(1 - u, 3);                       // big -> 1 with a hard landing
  const burst = Math.min(1, (t - at) / 0.8);
  const col = pal.accent3 || pal.accent;
  const label = String(scene.params.stamp).toUpperCase();
  const w = Math.max(520, label.length * 30 + 120), cx = W / 2, cy = scene.params.stamp_y ?? H - 210;
  return (
    <svg width={W} height={H} style={{position: 'absolute'}}>
      <circle cx={cx} cy={cy} r={60 + 320 * burst} fill="none" stroke={col} strokeWidth={4} strokeOpacity={0.5 * (1 - burst)} />
      <g transform={`translate(${cx} ${cy}) rotate(-5) scale(${sc})`} opacity={u}>
        <rect x={-w / 2} y={-52} width={w} height={104} rx={10} fill={pal.bg} fillOpacity={0.82} stroke={col} strokeWidth={6} />
        <rect x={-w / 2 + 12} y={-40} width={w - 24} height={80} rx={6} fill="none" stroke={col} strokeWidth={2} strokeOpacity={0.6} />
        <text x={0} y={16} textAnchor="middle" fill={col} fontFamily={font.display} fontWeight={800} fontSize={46} letterSpacing={6}>{label}</text>
      </g>
    </svg>
  );
};

/** Vignette for a filmic finish. (Per-frame SVG turbulence grain was removed: it dominated render time.) */
export const Finish: React.FC = () => {
  const {W, H} = useCtx();
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <svg width={W} height={H} style={{position: 'absolute'}}>
        <defs>
          <radialGradient id="vig" cx="50%" cy="50%" r="70%">
            <stop offset="60%" stopColor="#000" stopOpacity={0} />
            <stop offset="100%" stopColor="#000" stopOpacity={0.45} />
          </radialGradient>
        </defs>
        <rect width={W} height={H} fill="url(#vig)" />
      </svg>
    </AbsoluteFill>
  );
};

/** Text helper with fade/rise entrance. */
export const RiseText: React.FC<{
  x: number; y: number; at: number; size: number; color?: string; weight?: number; anchor?: 'start' | 'middle' | 'end';
  display?: boolean; children: React.ReactNode; dur?: number; tracking?: number; opacity?: number;
}> = ({x, y, at, size, color, weight = 400, anchor = 'start', display = false, children, dur = 0.5, tracking = 0, opacity = 1}) => {
  const {t, pal, font} = useCtx();
  const u = eo(t, at, dur);
  return (
    <text x={x} y={y + 24 * (1 - u)} opacity={u * opacity} textAnchor={anchor} fill={color || pal.ink}
      fontFamily={display ? font.display : font.body} fontWeight={weight} fontSize={size} letterSpacing={tracking}>
      {children}
    </text>
  );
};
