import React, {useMemo} from 'react';
import {getLength} from '@remotion/paths';
import {pointAt} from '../lib/pathsafe';
import {clamp, easeInOut, eo, lerp, prog, spokenAt, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';

/*
 * THE HIDDEN ECONOMICS presenter: an original, minimalist 2D economist (navy blazer, gold tie, round glasses)
 * who walks to the board, DRAWS diagrams with a marker whose tip follows the real SVG path, writes labels,
 * builds bar charts bar by bar, points at figures and reacts to discoveries. Fully procedural (no images):
 * two-bone inverse kinematics for the arms, a distance-driven walk cycle, blinking and narration-synced mouth.
 *
 * Scene type `presenter`. Params:
 *   title, title_cue, board: {x, y, w, h}, enter: {from: left|right, cue}, exit: {cue}
 *   items: ordered actions, each gated by an optional narration `cue`:
 *     {stroke: "M ...", colour, w, speed}            draw any path (charts, flowcharts, timelines, supply chains)
 *     {arrow: [[x1,y1],[x2,y2]], bend, colour}       draw an arrow
 *     {box: [x, y, w, h], label, colour, size}       draw a box, then write its label
 *     {text: "...", x, y, size, colour}              write a label
 *     {bars: [{label, value, display}], x, base, width, max_h, max_v, colour}   build a bar chart, bar by bar
 *     {point: [x, y], label, hold, colour}           point at something (ring pulse + optional label)
 *     {react: true}                                  small 'aha' reaction
 */

export const BRAND = {skin: '#E7B791', skinShade: '#D29E78', hair: '#2B221D', jacket: '#24385E', jacketShade: '#1B2B49',
  shirt: '#F1F2F4', tie: '#D9B25F', trousers: '#2A2E37', shoe: '#121418', glasses: '#C9A253', marker: '#D9B25F'};

type Pt = [number, number];
const L1 = 150, L2 = 145;

/** Two-bone IK: returns elbow point for shoulder s reaching target t (elbow bends down/back). */
const ik = (s: Pt, t: Pt, bendSign = 1): {e: Pt; h: Pt} => {
  const dx = t[0] - s[0], dy = t[1] - s[1];
  const d = clamp(Math.hypot(dx, dy), 20, L1 + L2 - 2);
  const a = Math.atan2(dy, dx);
  const cosB = clamp((L1 * L1 + d * d - L2 * L2) / (2 * L1 * d), -1, 1);
  const b = Math.acos(cosB) * bendSign;
  const e: Pt = [s[0] + Math.cos(a + b) * L1, s[1] + Math.sin(a + b) * L1];
  const h: Pt = [s[0] + Math.cos(a) * d, s[1] + Math.sin(a) * d];
  return {e, h};
};

export type Pose = {x: number; floor: number; facing: 1 | -1; walk: number; moving: number; hop: number;
  drawHand: Pt | null; pointHand: Pt | null; talking: number; blink: number; surprise: number; scale: number; holdingMarker: boolean};

/** The character, drawn in world coordinates. Hand targets are world points. */
export const Character: React.FC<{pose: Pose}> = ({pose}) => {
  const {x, floor, facing, walk, moving, hop, drawHand, pointHand, talking, blink, surprise, scale: S} = pose;
  const bob = -Math.abs(Math.sin(walk)) * 7 * moving - hop;
  // local -> world
  const W = (lx: number, ly: number): Pt => [x + lx * S * facing, floor + (ly + bob / S) * S];
  const toLocal = (p: Pt): Pt => [((p[0] - x) / S) * facing, (p[1] - floor) / S - bob / S];
  const sw = Math.sin(walk) * 0.42 * moving;
  const hipY = -250;
  const leg = (side: number) => {
    const ang = side * sw;
    const knee: Pt = [Math.sin(ang) * 125, hipY + Math.cos(ang) * 125];
    const ang2 = ang - Math.max(0, -side * Math.cos(walk)) * 0.5 * moving;
    const foot: Pt = [knee[0] + Math.sin(ang2) * 125, knee[1] + Math.cos(ang2) * 125];
    return {knee, foot};
  };
  const legs = [leg(1), leg(-1)];
  const shL: Pt = [-58, -428], shR: Pt = [58, -428];
  // arms: front arm (facing side) draws/points; back arm hangs or gestures
  const front = drawHand || pointHand;
  const frontTarget: Pt = front ? toLocal(front) : [70 + Math.sin(walk) * 30 * moving, -170];
  const backTarget: Pt = [-62 - Math.sin(walk) * 30 * moving, -175 + (talking > 0.5 && !front ? -40 * Math.sin(talking * 3) : 0)];
  const armF = ik(shR, frontTarget, front ? 1 : -1);
  const armB = ik(shL, backTarget, -1);
  const P = (p: Pt) => W(p[0], p[1]).join(',');
  const limb = (a: Pt, b: Pt, c: Pt, col: string, w: number) => (
    <path d={`M ${P(a)} L ${P(b)} L ${P(c)}`} fill="none" stroke={col} strokeWidth={w * S} strokeLinecap="round" strokeLinejoin="round" />
  );
  const head = W(0, -510);
  const eyeY = -512, eyeDX = 16;
  const torso = [[-64, -252], [-74, -440], [-34, -462], [34, -462], [74, -440], [64, -252]].map((p) => P(p as Pt)).join(' L ');
  const hand = armF.h;
  const handW = W(hand[0], hand[1]);
  const dirF = Math.atan2(armF.h[1] - armF.e[1], armF.h[0] - armF.e[0]);
  return (
    <g>
      {/* shadow */}
      <ellipse cx={x} cy={floor + 6} rx={90 * S * (1 - 0.15 * Math.min(1, hop / 20))} ry={12 * S} fill="#000" opacity={0.28} />
      {/* back arm */}
      {limb(shL, armB.e, armB.h, BRAND.jacketShade, 30)}
      <circle cx={W(armB.h[0], armB.h[1])[0]} cy={W(armB.h[0], armB.h[1])[1]} r={15 * S} fill={BRAND.skinShade} />
      {/* legs */}
      {legs.map((l, i) => (
        <g key={i}>
          {limb([i ? -22 : 22, hipY], l.knee, l.foot, i ? '#23262E' : BRAND.trousers, 36)}
          <ellipse cx={W(l.foot[0] + 14, l.foot[1] + 6)[0]} cy={W(l.foot[0] + 14, l.foot[1] + 6)[1]} rx={30 * S} ry={11 * S} fill={BRAND.shoe} />
        </g>
      ))}
      {/* torso: blazer, shirt, tie */}
      <path d={`M ${torso} Z`} fill={BRAND.jacket} />
      <path d={`M ${P([-34, -462])} L ${P([0, -392])} L ${P([34, -462])} Z`} fill={BRAND.shirt} />
      <path d={`M ${P([-6, -452])} L ${P([6, -452])} L ${P([10, -360])} L ${P([0, -340])} L ${P([-10, -360])} Z`} fill={BRAND.tie} />
      <path d={`M ${P([-34, -462])} L ${P([-12, -390])} L ${P([-40, -420])} Z`} fill={BRAND.jacketShade} />
      <path d={`M ${P([34, -462])} L ${P([12, -390])} L ${P([40, -420])} Z`} fill={BRAND.jacketShade} />
      <rect x={Math.min(...[W(-64, -262)[0], W(64, -262)[0]])} y={W(0, -262)[1]} width={128 * S} height={12 * S} fill={BRAND.jacketShade} />
      {/* neck + head */}
      <rect x={W(-12, -470)[0] - (facing < 0 ? 24 * S : 0)} y={W(0, -478)[1]} width={24 * S} height={22 * S} fill={BRAND.skinShade} />
      <circle cx={head[0]} cy={head[1]} r={52 * S} fill={BRAND.skin} />
      <path d={`M ${P([-52, -515])} C ${P([-56, -578])} ${P([40, -592])} ${P([54, -526])} C ${P([30, -548])} ${P([-10, -552])} ${P([-52, -515])} Z`} fill={BRAND.hair} />
      <circle cx={W(50, -508)[0]} cy={W(50, -508)[1]} r={9 * S} fill={BRAND.skinShade} />
      {/* eyebrows lift on surprise */}
      {[-1, 1].map((k) => <path key={k} d={`M ${P([k * eyeDX + 14 - 9, eyeY - 18 - surprise * 7])} L ${P([k * eyeDX + 14 + 9, eyeY - 20 - surprise * 7])}`}
        stroke={BRAND.hair} strokeWidth={4 * S} strokeLinecap="round" />)}
      {/* glasses + eyes (blink) */}
      {[-1, 1].map((k) => (
        <g key={'g' + k}>
          <circle cx={W(k * eyeDX + 14, eyeY)[0]} cy={W(k * eyeDX + 14, eyeY)[1]} r={13 * S} fill="none" stroke={BRAND.glasses} strokeWidth={3 * S} />
          <ellipse cx={W(k * eyeDX + 16, eyeY)[0]} cy={W(k * eyeDX + 16, eyeY)[1]} rx={3.6 * S} ry={4.2 * S * (1 - blink * 0.9)} fill="#1A1C20" />
        </g>
      ))}
      <path d={`M ${P([1, eyeY])} L ${P([27, eyeY])}`} stroke={BRAND.glasses} strokeWidth={2.5 * S} />
      {/* mouth: talks with the narration, opens on surprise */}
      <ellipse cx={W(18, -478)[0]} cy={W(18, -478)[1]} rx={(8 + 2 * surprise) * S} ry={(1.6 + 4 * talking + 5 * surprise) * S} fill="#6B2E2A" />
      {/* front arm + hand + marker */}
      {limb(shR, armF.e, armF.h, BRAND.jacket, 30)}
      <circle cx={handW[0]} cy={handW[1]} r={16 * S} fill={BRAND.skin} />
      {pose.holdingMarker && !pointHand && (
        <g transform={`translate(${handW[0]} ${handW[1]}) rotate(${(Math.atan2(Math.sin(dirF), Math.cos(dirF) * facing) * 180) / Math.PI})`}>
          <rect x={-6} y={-6} width={34 * S} height={12 * S} rx={4} fill={BRAND.marker} />
          <rect x={28 * S} y={-3} width={8 * S} height={6 * S} fill="#1A1C20" />
        </g>
      )}
      {pointHand && (() => {
        const tip = [handW[0] + Math.cos(dirF) * 26 * S * facing, handW[1] + Math.sin(dirF) * 26 * S];
        return <line x1={handW[0]} y1={handW[1]} x2={tip[0]} y2={tip[1]} stroke={BRAND.skin} strokeWidth={9 * S} strokeLinecap="round" />;
      })()}
      {/* 'aha' marks */}
      {surprise > 0.05 && [-0.6, 0, 0.6].map((a, i) => {
        const r0 = 72, r1 = 96;
        const ang = -Math.PI / 2 + a;
        const c = W(10, -515);
        return <line key={i} x1={c[0] + Math.cos(ang) * r0 * S} y1={c[1] + Math.sin(ang) * r0 * S} x2={c[0] + Math.cos(ang) * r1 * S} y2={c[1] + Math.sin(ang) * r1 * S}
          stroke={BRAND.tie} strokeWidth={5 * S} strokeLinecap="round" opacity={surprise} />;
      })}
    </g>
  );
};

type Action = {kind: 'draw' | 'write' | 'point' | 'react'; at: number; dur: number; d?: string; len?: number; text?: string; x?: number; y?: number;
  size?: number; colour?: string; w?: number; fill?: string; anchor: Pt; end: Pt; bodyA: number; bodyB: number; walkFrom: number; walkAt: number;
  label?: string; hold?: number; group?: number; laser?: boolean; barH?: number; barRect?: [number, number, number, number]};

const arrowPath = (a: Pt, b: Pt, bend = 0.18) => {
  const mx = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, my = (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend;
  const ang = Math.atan2(b[1] - my, b[0] - mx);
  const h1: Pt = [b[0] - 26 * Math.cos(ang - 0.45), b[1] - 26 * Math.sin(ang - 0.45)];
  const h2: Pt = [b[0] - 26 * Math.cos(ang + 0.45), b[1] - 26 * Math.sin(ang + 0.45)];
  return `M ${a[0]} ${a[1]} Q ${mx} ${my} ${b[0]} ${b[1]} M ${h1[0].toFixed(1)} ${h1[1].toFixed(1)} L ${b[0]} ${b[1]} L ${h2[0].toFixed(1)} ${h2[1].toFixed(1)}`;
};

export const PresenterScene: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const floor = p.floor ?? H - 60;
  const S = p.scale ?? 1;
  const board = p.board || {x: 470, y: 150, w: 1370, h: 790};
  const enterFrom = p.enter?.from === 'right' ? W + 220 : -220;
  const enterAt = cue(p.enter, 0) - 0.2;
  const reach = 210 * S;
  const bodyFor = (pt: Pt, side = -1): number => clamp(pt[0] + side * reach, 140, W - 140);
  const acts = useMemo(() => {
    const out: Action[] = [];
    let tEnd = enterAt + 1.3;
    let bx = bodyFor([board.x + 260, 0]);
    const firstX = bx;
    const push = (a: Omit<Action, 'at' | 'bodyA' | 'bodyB' | 'walkFrom' | 'walkAt'>, cueSpec: any, side = -1) => {
      const bA = a.kind === 'react' || (a as any).laser ? bx : bodyFor(a.anchor, side);
      const bB = a.kind === 'draw' || a.kind === 'write' ? bodyFor(a.end, side) : bA;
      const walk = Math.abs(bA - bx) / (520 * S);
      const walkAt = tEnd;
      const at = Math.max(tEnd + walk, cueSpec !== undefined ? cue(cueSpec, 0) : 0);
      out.push({...a, at, bodyA: bA, bodyB: bB, walkFrom: bx, walkAt} as Action);
      tEnd = at + a.dur;
      bx = bB;
    };
    const speed = p.speed || 950;
    for (const it of p.items || []) {
      const cs = it.cue !== undefined ? {cue: it.cue, offset: it.offset} : undefined;
      if (it.stroke || it.arrow) {
        const d: string = it.stroke || arrowPath(it.arrow[0], it.arrow[1], it.bend ?? 0.18);
        const len = getLength(d);
        const a0 = pointAt(d, 0), a1 = pointAt(d, len);
        push({kind: 'draw', dur: Math.max(0.4, len / (it.speed || speed)), d, len, colour: it.colour, w: it.w, fill: it.fill,
          anchor: [a0.x, a0.y], end: [a1.x, a1.y]}, cs);
      } else if (it.box) {
        const [x, y, w, h] = it.box;
        const d = `M ${x} ${y} L ${x + w} ${y} L ${x + w} ${y + h} L ${x} ${y + h} Z`;
        push({kind: 'draw', dur: Math.max(0.5, (2 * (w + h)) / (it.speed || speed * 1.3)), d, len: 2 * (w + h), colour: it.colour, w: it.w || 5, fill: it.fill,
          anchor: [x, y], end: [x, y + h]}, cs);
        if (it.label) {
          const size = it.size || 34;
          const len = String(it.label).length * size * 0.62;
          const tx = x + w / 2 - len / 2, ty = y + h / 2 + size * 0.35;
          push({kind: 'write', dur: Math.max(0.35, len / (speed * 1.1)), text: it.label, x: tx, y: ty, size, len, colour: it.label_colour,
            anchor: [tx, ty], end: [tx + len, ty]}, undefined);
        }
      } else if (it.text) {
        const size = it.size || 36;
        const len = String(it.text).length * size * 0.62;
        push({kind: 'write', dur: Math.max(0.35, len / (speed * 1.1)), text: it.text, x: it.x, y: it.y, size, len, colour: it.colour,
          anchor: [it.x, it.y], end: [it.x + len, it.y]}, cs);
      } else if (it.bars) {
        const data: any[] = it.bars;
        const n = data.length, bw = (it.width || 900) / n;
        const maxV = it.max_v || Math.max(...data.map((b) => b.value ?? b.total));
        data.forEach((b, i) => {
          const v = b.value ?? b.total;
          const h = Math.max(4, ((it.max_h || 480) * v) / maxV);
          const x = it.x + i * bw + bw * 0.18, w = bw * 0.64, base = it.base;
          const d = `M ${x} ${base} L ${x} ${base - h} L ${x + w} ${base - h} L ${x + w} ${base}`;
          const barCue = b.cue !== undefined ? {cue: b.cue} : i === 0 ? cs : undefined;
          push({kind: 'draw', dur: Math.max(0.3, (2 * h + w) / (speed * 1.6)), d, len: 2 * h + w, colour: it.colour, w: 4, fill: b.colour || it.colour,
            anchor: [x + w, base - h * 0.5], end: [x + w, base - h * 0.5], label: b.label, text: b.display, barH: h, barRect: [x, base - h, w, h], group: i}, barCue,
            it.side === 'left' ? -1 : 1);
        });
      } else if (it.point) {
        push({kind: 'point', dur: it.hold || 1.6, anchor: it.point, end: it.point, label: it.label, colour: it.colour, laser: !!it.laser}, cs,
          it.side === 'right' ? 1 : -1);
      } else if (it.react) {
        push({kind: 'react', dur: 0.8, anchor: [0, 0], end: [0, 0]}, cs);
      }
    }
    return {out, firstX};
  }, [scene]);
  const {out: actions, firstX} = acts;
  // ------------------------------------------------------------------ body position over time
  const bodyX = (tt: number): number => {
    if (tt < enterAt) return enterFrom;
    if (tt < enterAt + 1.3) return lerp(enterFrom, firstX, easeInOut((tt - enterAt) / 1.3));
    let x = firstX;
    for (const a of actions) {
      const walkDur = Math.max(0.001, a.at - a.walkAt);
      const walkEnd = a.walkAt + Math.min(walkDur, Math.abs(a.bodyA - a.walkFrom) / (520 * S) + 0.001);
      if (tt < a.walkAt) return x;
      if (tt < walkEnd) return lerp(a.walkFrom, a.bodyA, easeInOut((tt - a.walkAt) / (walkEnd - a.walkAt)));
      if (tt < a.at) return a.bodyA;
      if (tt < a.at + a.dur) return lerp(a.bodyA, a.bodyB, easeInOut((tt - a.at) / a.dur));
      x = a.bodyB;
    }
    const exAt = p.exit ? cue(p.exit, 0.95) : Infinity;
    if (tt > exAt) return lerp(x, W + 260, easeInOut(clamp((tt - exAt) / 1.4)));
    // after the last action: step back to the rest spot beside the board so the finished diagram is visible
    const last = actions[actions.length - 1];
    const restX = p.rest_x ?? Math.max(150, board.x - 190);
    if (last && p.rest !== false) {
      const r0 = last.at + last.dur + 0.5;
      const rd = Math.max(0.6, Math.abs(x - restX) / (520 * S));
      if (tt > r0) return lerp(x, restX, easeInOut(clamp((tt - r0) / rd)));
    }
    return x;
  };
  const x = bodyX(t);
  const v = (bodyX(t + 0.04) - bodyX(t - 0.04)) / 0.08;
  const moving = clamp(Math.abs(v) / 260);
  const walkPhase = x / (46 * S);
  // ------------------------------------------------------------------ what the hand is doing now
  let drawHand: Pt | null = null, pointHand: Pt | null = null, target: Pt | null = null, surprise = 0, hop = 0;
  for (const a of actions) {
    const u = prog(t, a.at, a.dur);
    if (u <= 0 || u >= 1) {
      if (a.kind === 'react' && t >= a.at && t < a.at + 1.1) { const q = (t - a.at) / 1.1; surprise = Math.sin(Math.PI * q); hop = 24 * Math.sin(Math.PI * clamp(q * 1.6)); }
      continue;
    }
    if (a.kind === 'draw') { const q = pointAt(a.d!, easeInOut(u) * a.len!); drawHand = [q.x, q.y]; target = drawHand; }
    else if (a.kind === 'write') { drawHand = [a.x! + a.len! * u, a.y! + 4 + Math.sin(u * 40) * 5]; target = drawHand; }
    else if (a.kind === 'point') { pointHand = a.anchor; target = a.anchor; }
    else if (a.kind === 'react') { const q = u; surprise = Math.sin(Math.PI * q); hop = 24 * Math.sin(Math.PI * clamp(q * 1.6)); }
  }
  const laserFrom: Pt = (() => {
    if (!target) return [x, floor - 430 * S];
    const sh: Pt = [x + 58 * S * (target[0] >= x ? 1 : -1), floor - 428 * S];
    const ang = Math.atan2(target[1] - sh[1], target[0] - sh[0]);
    const d = Math.min(Math.hypot(target[0] - sh[0], target[1] - sh[1]), (L1 + L2 - 2) * S);
    return [sh[0] + Math.cos(ang) * (d + 26 * S), sh[1] + Math.sin(ang) * (d + 26 * S)];
  })();
  const facing: 1 | -1 = moving > 0.3 ? (v > 0 ? 1 : -1) : target ? (target[0] >= x ? 1 : -1) : 1;
  const talking = spokenAt(scene, t) ? 0.5 + 0.5 * Math.abs(Math.sin(t * 22)) : 0;
  const blinkPhase = (t + 0.7) % 3.6;
  const blink = blinkPhase < 0.12 ? 1 : 0;
  // ------------------------------------------------------------------ the board content
  const drawn = actions.map((a, i) => {
    const u = easeInOut(prog(t, a.at, a.dur));
    if (u <= 0 && a.kind !== 'point') return null;
    const col = a.colour ? pal[a.colour] || a.colour : pal.ink;
    if (a.kind === 'draw') {
      const fillU = a.fill ? eo(t, a.at + a.dur, 0.5) : 0;
      return (
        <g key={i}>
          {a.barRect && fillU > 0 && <rect x={a.barRect[0]} y={a.barRect[1] + a.barRect[3] * (1 - fillU)} width={a.barRect[2]} height={a.barRect[3] * fillU}
            fill={pal[a.fill!] || a.fill} opacity={0.85} />}
          {!a.barRect && a.fill && fillU > 0 && <path d={a.d} fill={pal[a.fill] || a.fill} opacity={0.22 * fillU} />}
          <path d={a.d} fill="none" stroke={col} strokeWidth={a.w || 6} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={a.len} strokeDashoffset={a.len! * (1 - u)} />
          {a.barRect && a.label && <text x={a.barRect[0] + a.barRect[2] / 2} y={a.barRect[1] + a.barRect[3] + 34} textAnchor="middle" fill={pal.muted}
            fontFamily={font.body} fontWeight={600} fontSize={22} opacity={eo(t, a.at, 0.4)}>{a.label}</text>}
          {a.barRect && a.text && <text x={a.barRect[0] + a.barRect[2] / 2} y={a.barRect[1] - 14} textAnchor="middle" fill={pal.ink}
            fontFamily={font.display} fontWeight={800} fontSize={24} opacity={eo(t, a.at + a.dur, 0.4)}>{a.text}</text>}
        </g>
      );
    }
    if (a.kind === 'write') {
      return (
        <g key={i}>
          <clipPath id={`pw-${scene.id}-${i}`}><rect x={a.x! - 6} y={a.y! - a.size! * 1.1} width={a.len! * u + 10} height={a.size! * 1.5} /></clipPath>
          <text x={a.x} y={a.y} clipPath={`url(#pw-${scene.id}-${i})`} fill={a.colour ? col : pal.ink} fontFamily={font.display} fontWeight={800} fontSize={a.size}>{a.text}</text>
        </g>
      );
    }
    if (a.kind === 'point') {
      const on = t >= a.at && t < a.at + a.dur + 0.6;
      if (!on) return null;
      const q = ((t - a.at) % 1.1) / 1.1;
      const c = a.colour ? pal[a.colour] || a.colour : pal.accent3 || pal.accent;
      return (
        <g key={i} opacity={eo(t, a.at, 0.25) * (1 - eo(t, a.at + a.dur, 0.6))}>
          {a.laser && pointHand && t >= a.at && t < a.at + a.dur && <line x1={pointHand === a.anchor ? laserFrom[0] : laserFrom[0]} y1={laserFrom[1]} x2={a.anchor[0]} y2={a.anchor[1]}
            stroke={c} strokeWidth={3} opacity={0.85} strokeDasharray="2 0" />}
          <circle cx={a.anchor[0]} cy={a.anchor[1]} r={26 + 34 * q} fill="none" stroke={c} strokeWidth={4} opacity={1 - q} />
          <circle cx={a.anchor[0]} cy={a.anchor[1]} r={9} fill={c} />
          {a.label && <g>
            <rect x={a.anchor[0] + 24} y={a.anchor[1] - 74} width={String(a.label).length * 16 + 28} height={50} rx={10} fill={pal.bg} stroke={c} strokeWidth={2} />
            <text x={a.anchor[0] + 38} y={a.anchor[1] - 40} fill={c} fontFamily={font.body} fontWeight={700} fontSize={26}>{a.label}</text>
          </g>}
        </g>
      );
    }
    return null;
  });
  const boardU = eo(t, enterAt, 0.7);
  return (
    <svg width={W} height={H}>
      {/* board */}
      <g opacity={boardU}>
        <rect x={board.x} y={board.y} width={board.w} height={board.h} rx={22} fill={pal.bg2} opacity={0.92} stroke={pal.border} strokeWidth={2} />
        {Array.from({length: Math.floor(board.w / 60)}, (_, i) => <line key={'gx' + i} x1={board.x + 30 + i * 60} y1={board.y + 12} x2={board.x + 30 + i * 60}
          y2={board.y + board.h - 12} stroke={pal.border} strokeOpacity={0.25} />)}
        {Array.from({length: Math.floor(board.h / 60)}, (_, i) => <line key={'gy' + i} x1={board.x + 12} y1={board.y + 30 + i * 60} x2={board.x + board.w - 12}
          y2={board.y + 30 + i * 60} stroke={pal.border} strokeOpacity={0.25} />)}
      </g>
      {drawn}
      {/* floor line */}
      <rect x={0} y={floor + 4} width={W} height={H - floor} fill="#000" opacity={0.18} />
      <Character pose={{x, floor, facing, walk: walkPhase, moving, hop, drawHand, pointHand, talking, blink, surprise, scale: S, holdingMarker: true}} />
      {p.title && <RiseText x={120} y={110} at={cue(p.title_cue, 0)} size={46} weight={800} display>{p.title}</RiseText>}
    </svg>
  );
};
