import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {clamp, E, ease, springAt} from '../animation-engine/motion';
import {Animal} from './Animal';
import {Karaoke} from './Karaoke';
import {Scenery} from './Scenery';
import {ALL_ANIMALS, AnimalKind, FONT, hop, K, landing, Line, loadKidsFonts, RAINBOW, Timeline} from './theme';

export type KidsSongProps = {timeline: Timeline; offset?: number};

const blinkAt = (t: number, seed: number) => (((t + seed * 1.37) % 3.9) < 0.13 ? 1 : 0);
/** mouth movement while a word is being sung: quick syllable flaps */
const singing = (line: Line | undefined, t: number, from = 0) => {
  if (!line) return 0;
  const ws = line.words.slice(from);
  const on = ws.some((w) => t >= w.s - 0.02 && t <= w.e);
  return on ? 0.35 + 0.65 * Math.abs(Math.sin(t * 17)) : 0;
};
const pPer = (n: number) => (n <= 4 ? 2 : n <= 6 ? 3 : 4);
const P_AREA = (W: number, H: number, n: number) => ({x: 30, y: H * 0.29, w: W - 60, h: H * 0.46, per: pPer(n)});
const clapAt = (claps: number[], t: number) => claps.reduce((m, c) => Math.max(m, Math.exp(-(((t - c) / 0.09) ** 2))), 0);

type Slot = {x: number; y: number; s: number};
/** grid of N character slots (feet positions) inside an area */
const grid = (n: number, x0: number, y0: number, w: number, h: number, perRow: number): Slot[] => {
  const rows = Math.ceil(n / perRow);
  const cellH = h / rows;
  const out: Slot[] = [];
  for (let r = 0; r < rows; r++) {
    const inRow = Math.min(perRow, n - r * perRow);
    const cellW = w / Math.max(inRow, Math.min(perRow, n));
    const s = Math.min(1.15, cellW / 270, cellH / 360);
    for (let c = 0; c < inRow; c++) {
      out.push({x: x0 + w / 2 + (c - (inRow - 1) / 2) * cellW, y: y0 + (r + 1) * cellH - 175 * s, s});
    }
  }
  return out;
};

const Bubble: React.FC<{x: number; y: number; text: string; pop: number; color: string; size: number}> = ({x, y, text, pop, color, size}) => {
  if (pop <= 0.01) return null;
  const wdt = Math.max(260, text.length * size * 0.62 + 90);
  return (
    <g transform={`translate(${x} ${y}) scale(${pop})`}>
      <path d={`M ${-30} ${size * 0.75} L ${-70} ${size * 1.7} L ${30} ${size * 0.8} Z`} fill="#fff" stroke={K.ink} strokeWidth={7} strokeLinejoin="round" />
      <rect x={-wdt / 2} y={-size * 0.9} width={wdt} height={size * 1.8} rx={size * 0.9} fill="#fff" stroke={K.ink} strokeWidth={7} />
      <rect x={-34} y={size * 0.6} width={66} height={16} fill="#fff" />
      <text y={size * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={size} fill={color}
        stroke={K.ink} strokeWidth={3} paintOrder="stroke">{text}</text>
    </g>
  );
};

const Star: React.FC<{x: number; y: number; r: number; c: string; rot: number; o: number}> = ({x, y, r, c, rot, o}) => {
  const pts = Array.from({length: 10}, (_, i) => {
    const a = (Math.PI / 5) * i - Math.PI / 2;
    const rr = i % 2 ? r * 0.45 : r;
    return `${Math.cos(a) * rr},${Math.sin(a) * rr}`;
  }).join(' ');
  return <polygon points={pts} transform={`translate(${x} ${y}) rotate(${rot})`} fill={c} stroke={K.ink} strokeWidth={4} opacity={o} />;
};

const Balloon: React.FC<{x: number; y: number; n: string; c: string; pop: number; sway: number}> = ({x, y, n, c, pop, sway}) =>
  pop <= 0.01 ? null : (
    <g transform={`translate(${x} ${y}) rotate(${sway}) scale(${pop})`}>
      <path d="M 0 95 q -12 40 6 80 q 14 30 -4 60" fill="none" stroke={K.ink} strokeWidth={4} />
      <ellipse rx={78} ry={92} fill={c} stroke={K.ink} strokeWidth={6} />
      <ellipse cx={-30} cy={-40} rx={14} ry={24} fill="#fff" opacity={0.5} />
      <path d="M -12 92 L 12 92 L 0 104 Z" fill={c} stroke={K.ink} strokeWidth={4} />
      <text y={34} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={104} fill="#fff" stroke={K.ink} strokeWidth={6} paintOrder="stroke">{n}</text>
    </g>
  );

/* ------------------------------------------------------------------------------------------------ */
export const KidsSong: React.FC<KidsSongProps> = ({timeline: tl, offset = 0}) => {
  loadKidsFonts();
  const frame = useCurrentFrame();
  const {fps, width: W, height: H} = useVideoConfig();
  const t = frame / fps + offset;
  const portrait = H > W;
  const beat = tl.beat;
  const lines = tl.lines;
  let li = -1;
  lines.forEach((l, i) => { if (t >= l.start - 0.25) li = i; });
  const line = li >= 0 ? lines[li] : undefined;
  const next = li + 1 < lines.length ? lines[li + 1] : undefined;
  const section = tl.sections.find((s) => t >= s.start && t < s.end) ?? tl.sections[tl.sections.length - 1];
  const kind = section.kind;
  const lt = line ? t - line.start : 0;          // time inside the current line
  const sq = landing(t, beat);

  const stage: React.ReactNode[] = [];
  const overlay: React.ReactNode[] = [];

  /* ---------------- INTRO: title card */
  if (kind === 'intro') {
    const out = ease(t, section.end - 0.6, 0.6, E.in);
    const words = tl.title.replace('!', '').split(' ');
    const lineA = words.slice(0, 2).join(' ').toUpperCase();
    const lineB = words.slice(2).join(' ').toUpperCase() + '!';
    let k = 0;
    const renderLetters = (s: string, size: number) => s.split('').map((ch, i) => {
      const idx = k++;
      const p = springAt(t, 0.25 + idx * 0.06, fps, {damping: 9, stiffness: 140});
      const bob = Math.sin(t * 4 + idx * 0.6) * 8;
      return (
        <span key={i} style={{display: 'inline-block', transform: `translateY(${(1 - p) * -160 + bob}px) scale(${p})`,
          color: ch === ' ' ? 'transparent' : RAINBOW[idx % RAINBOW.length], fontSize: size, width: ch === ' ' ? size * 0.32 : undefined,
          WebkitTextStroke: `${size * 0.07}px ${K.ink}`, paintOrder: 'stroke fill', textShadow: `0 ${size * 0.08}px 0 rgba(43,35,80,0.25)`}}>
          {ch}
        </span>
      );
    });
    overlay.push(
      <div key="title" style={{position: 'absolute', left: 0, right: 0, top: portrait ? H * 0.13 : H * 0.1, textAlign: 'center',
        fontFamily: FONT, fontWeight: 700, lineHeight: 1.02, opacity: 1 - out, transform: `translateY(${-out * 120}px)`}}>
        <div>{renderLetters(lineA, portrait ? 130 : 150)}</div>
        <div>{renderLetters(lineB, portrait ? 112 : 130)}</div>
      </div>,
    );
    const pals: AnimalKind[] = ['chick', 'duck', 'pig'];
    const slots = portrait ? [{x: W * 0.25, y: H * 0.5}, {x: W * 0.5, y: H * 0.56}, {x: W * 0.75, y: H * 0.5}]
      : [{x: W * 0.24, y: H * 0.56}, {x: W * 0.5, y: H * 0.6}, {x: W * 0.76, y: H * 0.56}];
    pals.forEach((a, i) => {
      const p = springAt(t, 1.0 + i * 0.35, fps);
      stage.push(<Animal key={a} kind={a} x={slots[i].x} y={slots[i].y + (1 - p) * 500} scale={(portrait ? 0.95 : 1.0) * (0.6 + 0.4 * p)}
        bounce={t > 2 ? hop(t, beat, i * 0.5) * 0.6 : 0} squash={sq} mouth={singing(line, t) * (i === 1 ? 1 : 0.6)}
        blink={blinkAt(t, i)} wave={clamp((t - 3) / 0.4) * (i !== 1 ? 1 : 0)} waveT={t} look={Math.sin(t) * 0.5} opacity={1 - out} />);
    });
  }

  /* ---------------- CHORUS: dancing band */
  if (kind === 'chorus') {
    const band: AnimalKind[] = section.name === 'chorus1' ? ['duck', 'cat', 'dog', 'pig', 'frog']
      : section.name === 'chorus2' ? ['duck', 'cat', 'dog', 'cow', 'sheep'] : ALL_ANIMALS;
    const inT = ease(t, section.start, 0.5, E.outBack);
    const outT = ease(t, section.end - 0.35, 0.35, E.in);
    const area = portrait ? P_AREA(W, H, band.length)
      : {x: 120, y: H * 0.33, w: W - 240, h: H * 0.5, per: 5};
    const slots = grid(band.length, area.x, area.y, area.w, area.h, area.per);
    const cl = line?.chorus_line ?? 0;
    const claps = line?.claps ?? [];
    const clap = cl === 2 ? clapAt(claps, t) : 0;
    const waving = cl === 3 ? clamp((lt - beat * 1.8) / 0.3) : 0;
    band.forEach((a, i) => {
      const sl = slots[i];
      const big = cl === 1 ? 1.25 : 0.8;
      stage.push(<Animal key={a + i} kind={a} x={sl.x} y={sl.y + (1 - inT) * 600 + outT * 600} scale={sl.s}
        bounce={hop(t, beat, (i % 2) * 0.5) * big} squash={landing(t, beat, (i % 2) * 0.5)} mouth={singing(line, t)}
        blink={blinkAt(t, i)} clap={clap} wave={waving} waveT={t + i} tilt={Math.sin((t / beat) * Math.PI + i) * 6}
        look={Math.sin(t * 0.8 + i) * 0.6} flap={t * 30} />);
    });
    // line-specific props
    if (line && line.kind === 'chorus') {
      if (cl === 0) {
        line.words.slice(0, 3).forEach((wd, i) => {
          const p = springAt(t, wd.s - 0.05, fps, {damping: 10});
          const bx = portrait ? W * (0.22 + 0.28 * i) : W * (0.3 + 0.2 * i);
          const by = (portrait ? H * 0.2 : H * 0.2) - Math.max(0, t - wd.s) * 12;
          overlay.push(<svg key={'b' + i} width={W} height={H} style={{position: 'absolute', inset: 0}}>
            <Balloon x={bx} y={by} n={String(i + 1)} c={[K.coral, K.blue, K.green][i]} pop={p * (1 - outT)} sway={Math.sin(t * 2 + i) * 6} />
          </svg>);
        });
      }
      if (cl === 2) {
        claps.forEach((c, ci) => {
          const u = (t - c) / 0.6;
          if (u < 0 || u > 1) return;
          const cx = portrait ? W * 0.5 : W * (ci % 2 ? 0.62 : 0.38);
          const cy = portrait ? H * 0.24 : H * 0.2;
          overlay.push(<svg key={'c' + ci} width={W} height={H} style={{position: 'absolute', inset: 0}}>
            {Array.from({length: 6}, (_, k) => {
              const a = (k / 6) * Math.PI * 2 + ci;
              return <Star key={k} x={cx + Math.cos(a) * 140 * E.out(u)} y={cy + Math.sin(a) * 100 * E.out(u)} r={34 * (1 - u * 0.5)}
                c={RAINBOW[(k + ci) % RAINBOW.length]} rot={u * 90} o={1 - u} />;
            })}
          </svg>);
        });
      }
      if (cl === 3 || cl === 1) {
        // gentle confetti drifting down (slow, soft colours, no flashing)
        const n = 26;
        overlay.push(<svg key="conf" width={W} height={H} style={{position: 'absolute', inset: 0}}>
          {Array.from({length: n}, (_, k) => {
            const sp = 120 + ((k * 37) % 90);
            const y = ((lt * sp + k * 97) % (H * 0.75)) - 40;
            const x = ((k * 211) % W) + Math.sin(t * 2 + k) * 30;
            return <rect key={k} x={x} y={y} width={22} height={13} rx={4} fill={RAINBOW[k % RAINBOW.length]}
              transform={`rotate(${(t * 90 + k * 40) % 360} ${x + 11} ${y + 6})`} opacity={0.9 * clamp(lt / 0.4) * (1 - outT)} />;
          })}
        </svg>);
      }
    }
  }

  /* ---------------- VERSE: count the animals */
  if (kind === 'verse' && line) {
    const outT = ease(t, line.end - 0.3, 0.3, E.in);
    if (line.kind === 'number' && line.number && line.animal) {
      const n = line.number;
      const col = RAINBOW[(n - 1) % RAINBOW.length];
      const pIn = springAt(t, line.start - 0.1, fps, {damping: 9, stiffness: 150});
      // big number badge
      const nb = portrait ? {x: W * 0.28, y: H * 0.13, r: 140} : {x: 330, y: H * 0.36, r: 185};
      const pulse = 1 + 0.04 * landing(t, beat);
      overlay.push(<svg key="num" width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <g transform={`translate(${nb.x} ${nb.y}) scale(${pIn * pulse * (1 - outT)}) rotate(${Math.sin(t * 2) * 4})`}>
          <circle r={nb.r + 14} fill="#fff" stroke={K.ink} strokeWidth={8} />
          <circle r={nb.r - 4} fill={col} />
          <text y={nb.r * 0.36} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={nb.r * (n >= 10 ? 1.05 : 1.25)}
            fill="#fff" stroke={K.ink} strokeWidth={10} paintOrder="stroke">{n}</text>
        </g>
        <g transform={`translate(${nb.x} ${nb.y + nb.r + 84}) scale(${pIn * (1 - outT)})`}>
          <text textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={portrait ? 84 : 78} fill={col}
            stroke={K.ink} strokeWidth={8} paintOrder="stroke">{line.number_word}</text>
        </g>
      </svg>);
      // animals pop in one by one over the first 4 beats, each with a little count tag
      const area = portrait ? P_AREA(W, H, n)
        : {x: 560, y: H * 0.2, w: W - 620, h: H * 0.63, per: n <= 5 ? 5 : 5};
      const slots = grid(n, area.x, area.y, area.w, area.h, area.per);
      const step = Math.min(beat * 0.5, (beat * 3.2) / n);
      const soundFrom = line.words.findIndex((w) => /^[a-zá]/.test(w.w) && w.s >= line.start + beat * 3.5);
      const soundOn = soundFrom >= 0 ? singing(line, t, soundFrom) : 0;
      const counting: React.ReactNode[] = [];
      slots.forEach((sl, i) => {
        const at = line.start + beat * 0.6 + i * step;
        const p = springAt(t, at, fps, {damping: 10, stiffness: 160});
        if (p <= 0.001) return;
        const jump = soundOn > 0 ? hop(t, beat / 2, i * 0.13) * 0.8 : hop(t, beat, i * 0.25) * 0.35;
        stage.push(<Animal key={'a' + i} kind={line.animal as AnimalKind} x={sl.x} y={sl.y} scale={sl.s * p * (1 - outT * 0.9)}
          bounce={jump} squash={landing(t, beat, i * 0.25)} mouth={soundOn} blink={blinkAt(t, i)} tilt={Math.sin(t * 3 + i) * 5}
          look={Math.sin(t * 0.9 + i) * 0.7} flap={t * 30} wave={0} />);
        const tagO = clamp((t - at) / 0.15) * (1 - clamp((t - at - beat * 2.2) / 0.4));
        if (tagO > 0) {
          counting.push(<g key={'t' + i} transform={`translate(${sl.x} ${sl.y - 225 * sl.s - 40}) scale(${tagO})`}>
            <circle r={36} fill={col} stroke={K.ink} strokeWidth={5} />
            <text y={14} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={42} fill="#fff" stroke={K.ink} strokeWidth={4} paintOrder="stroke">{i + 1}</text>
          </g>);
        }
      });
      overlay.push(<svg key="cnt" width={W} height={H} style={{position: 'absolute', inset: 0}}>{counting}</svg>);
      // sound bubble on the animal sounds
      if (soundFrom >= 0) {
        const ws = line.words.slice(soundFrom);
        const a = ws[0].s - 0.05;
        const pop = springAt(t, a, fps, {damping: 9}) * (1 - outT);
        const said = ws.filter((w) => t >= w.s - 0.05).map((w) => w.w.replace(/[,!]/g, '').toUpperCase()).join(' ') + '!';
        overlay.push(<svg key="bub" width={W} height={H} style={{position: 'absolute', inset: 0}}>
          <Bubble x={portrait ? W * 0.72 : W * 0.66} y={portrait ? H * 0.1 : H * 0.12} text={said} pop={pop} color={col} size={portrait ? 56 : 80} />
        </svg>);
      }
    } else if (line.kind === 'tag') {
      const total = line.total ?? 5;
      const kinds = total === 5 ? ALL_ANIMALS.slice(0, 5) : ALL_ANIMALS;
      const area = portrait ? P_AREA(W, H, kinds.length)
        : {x: 100, y: H * 0.33, w: W - 200, h: H * 0.5, per: 5};
      const slots = grid(kinds.length, area.x, area.y, area.w, area.h, area.per);
      kinds.forEach((a, i) => {
        const p = springAt(t, line.start - 0.1 + i * 0.07, fps, {damping: 11});
        stage.push(<Animal key={'g' + a} kind={a} x={slots[i].x} y={slots[i].y} scale={slots[i].s * p * (1 - outT * 0.9)}
          bounce={hop(t, beat, i * 0.2) * 0.6} squash={landing(t, beat, i * 0.2)} mouth={singing(line, t)} blink={blinkAt(t, i)}
          wave={clamp((t - line.start - beat) / 0.3)} waveT={t + i} flap={t * 30} />);
      });
      const pop = springAt(t, line.start, fps, {damping: 9}) * (1 - outT);
      overlay.push(<div key="tag" style={{position: 'absolute', left: 0, right: 0, top: portrait ? H * 0.12 : H * 0.05, textAlign: 'center',
        fontFamily: FONT, fontWeight: 700, fontSize: portrait ? 150 : 150, color: K.yellow, WebkitTextStroke: `12px ${K.ink}`,
        paintOrder: 'stroke fill', transform: `scale(${pop}) rotate(${Math.sin(t * 3) * 3}deg)`}}>
        {total} AMIGOS!
      </div>);
    }
  }

  /* ---------------- OUTRO: everyone waves goodbye */
  if (kind === 'outro') {
    const area = portrait ? P_AREA(W, H, 10) : {x: 100, y: H * 0.3, w: W - 200, h: H * 0.52, per: 5};
    const slots = grid(10, area.x, area.y, area.w, area.h, area.per);
    ALL_ANIMALS.forEach((a, i) => {
      const p = springAt(t, section.start + i * 0.06, fps, {damping: 11});
      stage.push(<Animal key={'o' + a} kind={a} x={slots[i].x} y={slots[i].y} scale={slots[i].s * p}
        bounce={hop(t, beat, i * 0.2) * 0.4} squash={landing(t, beat, i * 0.2)} mouth={singing(line, t)} blink={blinkAt(t, i)}
        wave={1} waveT={t + i * 0.3} flap={t * 30} />);
    });
    const p = springAt(t, section.start, fps, {damping: 9});
    const p2 = springAt(t, section.start + tl.bar * 2.6, fps, {damping: 9});
    overlay.push(<div key="tchau" style={{position: 'absolute', left: 0, right: 0, top: portrait ? H * 0.1 : H * 0.05, textAlign: 'center',
      fontFamily: FONT, fontWeight: 700, color: K.pink, WebkitTextStroke: `12px ${K.ink}`, paintOrder: 'stroke fill'}}>
      <div style={{fontSize: 160, transform: `scale(${p}) rotate(${Math.sin(t * 3) * 3}deg)`}}>TCHAU!</div>
      <div style={{fontSize: portrait ? 76 : 70, color: K.yellow, WebkitTextStroke: `9px ${K.ink}`, transform: `scale(${p2})`}}>ATÉ A PRÓXIMA!</div>
    </div>);
  }

  const endFade = ease(t, tl.duration - 1.0, 0.9, E.inOut);
  const startFade = offset > 0 ? 1 - clamp((frame / fps) / 0.4) : 0;
  return (
    <AbsoluteFill style={{backgroundColor: K.sky2}}>
      <svg width={W} height={H} style={{position: 'absolute', inset: 0}}>
        <Scenery t={t} beat={beat} w={W} h={H} />
        {stage}
      </svg>
      {overlay}
      <Karaoke line={line && line.words.length ? line : undefined} next={next} t={t} portrait={portrait} w={W} h={H} />
      <AbsoluteFill style={{backgroundColor: '#fff', opacity: Math.max(endFade * 0.85, startFade)}} />
    </AbsoluteFill>
  );
};
