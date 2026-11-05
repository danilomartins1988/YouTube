import React, {useMemo} from 'react';
import {getLength} from '@remotion/paths';
import {pointAt} from '../lib/pathsafe';
import {easeInOut, eo, lerp, prog, rand, useCtx} from '../lib/anim';
import {RaceCar} from '../components/RaceCar';
import {CIRCUIT} from './RaceScenes';

/** Original hand-with-marker illustration; the marker tip is at (0, 0). */
const Hand: React.FC<{x: number; y: number; tilt?: number}> = ({x, y, tilt = 0}) => (
  <g transform={`translate(${x} ${y}) rotate(${tilt})`}>
    <path d="M 0 0 L 22 -12 L 120 -112 L 100 -132 L 4 -32 Z" fill="#1E9BFF" />
    <path d="M 0 0 L 10 -20 L 2 -24 Z" fill="#111" />
    <path d="M 70 -96 C 80 -140 120 -170 170 -175 C 215 -178 260 -150 275 -110 C 290 -70 270 -20 230 0 C 200 15 150 10 120 -10 Z" fill="#F2C9A8" />
    <path d="M 86 -100 C 70 -88 66 -70 80 -60 C 96 -50 116 -64 120 -84" fill="#E8B590" />
    <path d="M 150 -168 C 150 -150 170 -140 190 -146" fill="none" stroke="#D99F79" strokeWidth={4} strokeLinecap="round" />
    <path d="M 230 0 L 300 70 L 380 10 L 275 -110 Z" fill="#2B3A55" />
  </g>
);

type Stroke = {d?: string; colour?: string; w?: number; fill?: string; text?: string; x?: number; y?: number; size?: number; cue?: any; speed?: number};

/** A side-view car outline (matches RaceCar geometry at scale 0.9, origin 520,700). */
const CAR_STROKES = (ox: number, oy: number, s: number): Stroke[] => {
  const T = (d: string) => d.replace(/(-?\d+(?:\.\d+)?) (-?\d+(?:\.\d+)?)/g, (_m, a, b) => `${(ox + Number(a) * s).toFixed(1)} ${(oy + Number(b) * s).toFixed(1)}`);
  const circle = (cx: number, r: number) => T(`M ${cx - r} ${-r} C ${cx - r} ${-r * 2.33} ${cx + r} ${-r * 2.33} ${cx + r} ${-r} C ${cx + r} ${r * 0.33} ${cx - r} ${r * 0.33} ${cx - r} ${-r}`);
  return [
    {d: T('M -30 -46 L 470 -46 L 540 -60 L 545 -70 L 420 -78 L 300 -84 L 230 -118 L 150 -120 L 90 -108 L 10 -104 L -30 -90 Z'), fill: 'accent'},
    {d: T('M 150 -150 C 175 -190 230 -186 250 -128'), w: 7},
    {d: T('M -58 -178 L 12 -178 L 12 -162 L -58 -162 Z M -46 -162 L -46 -92'), fill: 'bg'},
    {d: T('M 470 -40 L 560 -40 L 566 -52 L 480 -54 Z'), fill: 'bg'},
    {d: circle(0, 58), fill: 'bg'},
    {d: circle(430, 50), fill: 'bg'},
  ];
};

const REVENUE_STROKES: Stroke[] = [
  {d: 'M 820 430 L 1100 430 L 1100 560 L 820 560 Z', fill: 'accent', cue: 'business model'},
  {text: 'FORMULA 1', x: 842, y: 508, size: 44, cue: 'business model'},
  {d: 'M 160 170 L 470 170 L 470 280 L 160 280 Z', fill: 'accent2', cue: 'broadcasters'},
  {text: 'BROADCASTERS', x: 176, y: 238, size: 31, cue: 'broadcasters'},
  {d: 'M 480 250 C 620 300 700 360 812 440', w: 6, cue: 'broadcasters'},
  {d: 'M 160 470 L 470 470 L 470 580 L 160 580 Z', fill: 'accent3', cue: 'race promoters'},
  {text: 'PROMOTERS', x: 196, y: 538, size: 36, cue: 'race promoters'},
  {d: 'M 480 525 L 812 500', w: 6, cue: 'race promoters'},
  {d: 'M 160 770 L 470 770 L 470 880 L 160 880 Z', fill: 'ink', cue: 'sponsors'},
  {text: 'SPONSORS', x: 206, y: 838, size: 38, cue: 'sponsors'},
  {d: 'M 480 800 C 620 740 700 640 812 560', w: 6, cue: 'sponsors'},
  {d: 'M 1450 440 L 1760 440 L 1760 550 L 1450 550 Z', fill: 'accent2', cue: 'flows back'},
  {text: 'TEAMS', x: 1530, y: 510, size: 44, cue: 'flows back'},
  {d: 'M 1110 495 L 1440 495', w: 6, cue: 'flows back'},
];

/**
 * Whiteboard hand-drawing: an original hand illustration traces each stroke progressively (its marker tip
 * follows the path being drawn, measured with @remotion/paths); text is written left-to-right with the hand
 * moving along the baseline. Then the sketch 'comes alive': fills colour in and the drawing transforms
 * (car -> animated car driving off; circuit -> live track with a car lapping; revenue -> money flows on arrows).
 */
export const Whiteboard: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const kind = p.drawing || 'car';
  const strokes: Stroke[] = useMemo(() => (kind === 'car' ? CAR_STROKES(560, 760, 1.25)
    : kind === 'circuit' ? [{d: CIRCUIT, w: 10, speed: 650}]
      : kind === 'revenue' ? REVENUE_STROKES : (p.strokes || [])), [kind, p.strokes]);
  const speed = p.speed || 1100; // px of path per second
  // schedule strokes: each starts at max(previous end, its cue)
  const sched = useMemo(() => {
    let tEnd = scene.lead + 0.2;
    return strokes.map((s) => {
      const len = s.d ? getLength(s.d) : (s.text || '').length * (s.size || 40) * 0.74;
      const dur = Math.max(0.35, len / (s.speed || speed)) * (s.text ? 0.8 : 1);
      const at = s.cue ? Math.max(tEnd, cue(s.cue, 0)) : tEnd;
      tEnd = at + dur;
      return {at, dur, len};
    });
  }, [strokes, scene, speed]);
  const doneT = sched.length ? sched[sched.length - 1].at + sched[sched.length - 1].dur : 0;
  const colourise = eo(t, doneT + 0.2, 0.8);
  const col = (k?: string) => (k ? pal[k] || k : '#1A1C22');

  // where is the hand?
  let hand: [number, number] | null = null;
  sched.forEach((sc, i) => {
    const u = prog(t, sc.at, sc.dur);
    if (u > 0 && u < 1) {
      const s = strokes[i];
      if (s.d) { const pt = pointAt(s.d, easeInOut(u) * sc.len); hand = [pt.x, pt.y]; }
      else hand = [(s.x || 0) + sc.len * u, (s.y || 0) + 6];
    }
  });
  const lastPt: [number, number] = hand || [W * 0.75, H * 0.85];
  const handOut = eo(t, doneT, 0.6);
  const paper = '#F7F5EF';
  const transform = kind === 'car' ? eo(t, doneT + 0.6, 0.8) : kind === 'circuit' ? eo(t, doneT + 0.4, 0.8) : 0;
  const driveOff = kind === 'car' ? eo(t, doneT + 1.8, 2.0) : 0;
  const darkBg = transform; // the board fades to charcoal as the sketch comes alive
  return (
    <svg width={W} height={H}>
      <rect width={W} height={H} fill={paper} />
      {Array.from({length: 40}, (_, i) => (
        <circle key={i} cx={rand(i) * W} cy={rand(i + 4) * H} r={1 + rand(i + 9) * 2} fill="#000" opacity={0.03} />
      ))}
      <rect width={W} height={H} fill={pal.bg} opacity={darkBg} />
      {strokes.map((s, i) => {
        const sc = sched[i];
        const u = easeInOut(prog(t, sc.at, sc.dur));
        if (u <= 0) return null;
        if (s.text) {
          const clipW = sc.len * u + 8;
          return (
            <g key={i}>
              <clipPath id={`wb-t${scene.id}-${i}`}><rect x={(s.x || 0) - 4} y={(s.y || 0) - (s.size || 40)} width={clipW} height={(s.size || 40) * 1.4} /></clipPath>
              <text x={s.x} y={s.y} clipPath={`url(#wb-t${scene.id}-${i})`} fontFamily="'Comic Neue', 'Segoe Print', 'Inter', sans-serif"
                fontWeight={700} fontSize={s.size || 40} fill={colourise > 0.5 && kind === 'revenue' ? (s.y && s.y > 760 ? pal.bg : '#FFFFFF') : '#1A1C22'}>{s.text}</text>
            </g>
          );
        }
        return (
          <g key={i} opacity={1 - transform}>
            {s.fill && <path d={s.d} fill={col(s.fill)} opacity={colourise * 0.95} />}
            <path d={s.d} fill="none" stroke={colourise > 0 && s.fill ? '#000' : '#1A1C22'} strokeWidth={s.w || 6} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={sc.len} strokeDashoffset={sc.len * (1 - u)} />
            {/* money flowing on arrows once the model is complete */}
            {kind === 'revenue' && !s.fill && colourise >= 1 && Array.from({length: 4}, (_, k) => {
              const q = ((t * 0.5 + k / 4) % 1);
              const pt = pointAt(s.d!, q * sc.len);
              return <circle key={k} cx={pt.x} cy={pt.y} r={9} fill={pal.accent3 || '#FFD21F'} stroke="#000" strokeWidth={2} />;
            })}
          </g>
        );
      })}
      {kind === 'car' && transform > 0 && (
        <RaceCar x={560 + driveOff * 380 + Math.sin(t * 1.3) * 20 * driveOff} y={760} scale={1.25} body={pal.accent} trim="#FFFFFF" spin={t * (8 + 40 * driveOff)} t={t}
          speedLines={driveOff} number="05" opacity={transform} />
      )}
      {kind === 'circuit' && transform > 0 && (() => {
        const L = getLength(CIRCUIT);
        const q = ((t - doneT) / 5) % 1;
        const pt = pointAt(CIRCUIT, q * L);
        return (
          <g opacity={transform}>
            <path d={CIRCUIT} fill="none" stroke="#2C3038" strokeWidth={58} strokeLinejoin="round" />
            <path d={CIRCUIT} fill="none" stroke={pal.accent} strokeWidth={6} />
            <path d={CIRCUIT} fill="none" stroke="#FFFFFF" strokeWidth={3} strokeDasharray="18 16" strokeDashoffset={-t * 40} opacity={0.6} />
            <circle cx={pt.x} cy={pt.y} r={16} fill={pal.accent3 || '#FFD21F'} stroke="#000" strokeWidth={3} />
          </g>
        );
      })()}
      {hand && handOut < 1 && <g opacity={1 - handOut}><Hand x={hand[0]} y={hand[1]} tilt={-8 + Math.sin(t * 6) * 2} /></g>}
      {!hand && handOut < 1 && t < doneT + 0.6 && t > scene.lead && <g opacity={1 - handOut}><Hand x={lastPt[0]} y={lastPt[1]} /></g>}
      {p.caption && (
        <text x={W / 2} y={H - 130} textAnchor="middle" fill={transform > 0.5 ? pal.ink : '#1A1C22'} fontFamily={font.display} fontWeight={800}
          fontSize={48} opacity={eo(t, cue(p.caption_cue, 0.85), 0.5)}>{p.caption}</text>
      )}
    </svg>
  );
};

export const _wb = lerp;
