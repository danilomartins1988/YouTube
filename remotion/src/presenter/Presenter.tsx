import React, {useMemo} from 'react';
import {getLength} from '@remotion/paths';
import {pointAt} from '../lib/pathsafe';
import {clamp, easeInOut, eo, lerp, prog, spokenAt, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';
import {useGeo} from '../lib/geo';
import {merc, parseLayer} from '../scenes/MapScene';

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
// arm bones (v2, 2026-11-10): shorter and closer to the torso proportions (shoulder→hip ≈ 176)
const L1 = 126, L2 = 118;
/** arms stay anatomical: at most 6% stretch; beyond that a telescopic marker / pointer bridges the gap */
const MAX_STRETCH = 1.06;

/** Two-bone IK: returns elbow point for shoulder s reaching target t (elbow bends down/back). */
const ik = (s: Pt, t: Pt, bendSign = 1, maxFrac = 0.9): {e: Pt; h: Pt} => {
  const dx = t[0] - s[0], dy = t[1] - s[1];
  const raw = Math.hypot(dx, dy);
  // cartoon stretch: a far target lengthens both bones (up to 1.5x) so the hand stays ON the drawing path
  const k = clamp(raw / (L1 + L2 - 2), 1, MAX_STRETCH);
  const l1 = L1 * k, l2 = L2 * k;
  // v3: the hand never reaches full extension, so the elbow always shows a visible bend
  const d = clamp(raw, 20, (l1 + l2) * maxFrac);
  const a = Math.atan2(dy, dx);
  const cosB = clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1, 1);
  const b = Math.acos(cosB) * bendSign;
  const e: Pt = [s[0] + Math.cos(a + b) * l1, s[1] + Math.sin(a + b) * l1];
  const h: Pt = [s[0] + Math.cos(a) * d, s[1] + Math.sin(a) * d];
  return {e, h};
};

export type Pose = {x: number; floor: number; facing: 1 | -1; walk: number; moving: number; hop: number;
  drawHand: Pt | null; pointHand: Pt | null; talking: number; blink: number; surprise: number; scale: number; holdingMarker: boolean;
  /** optional (animation engine): body lean in degrees (anticipation / follow-through), back-hand world target
   * for explaining gestures, smile 0..1 */
  lean?: number; backHand?: Pt | null; smile?: number;
  /** point with the index finger (no pointer stick): the arm reaches ~88% toward the target with a natural elbow bend */
  finger?: boolean};

/** QA helper: world positions of the front shoulder, elbow, hand and marker tip for a pose (same maths as the
 * renderer), so tests can measure whether the drawing instrument really sits on the path. */
export const frontArmWorld = (pose: Pose) => {
  const {x, floor, facing, walk, moving, hop, drawHand, pointHand, scale: S} = pose;
  const bob = -Math.abs(Math.sin(walk)) * 7 * moving - hop;
  const W = (lx: number, ly: number): Pt => [x + lx * S * facing, floor + (ly + bob / S) * S];
  const toLocal = (p: Pt): Pt => [((p[0] - x) / S) * facing, (p[1] - floor) / S - bob / S];
  const front = drawHand || pointHand;
  let ft: Pt = front ? toLocal(front) : [70 + Math.sin(walk) * 30 * moving, -170];
  if (drawHand) { const v = [ft[0] - 58, ft[1] + 428], n = Math.hypot(v[0], v[1]) || 1; ft = [ft[0] - (v[0] / n) * 36, ft[1] - (v[1] / n) * 36]; }
  const arm = ik([58, -428], ft, front ? 1 : -1);
  const hand = W(arm.h[0], arm.h[1]);
  const dir = Math.atan2(arm.h[1] - arm.e[1], arm.h[0] - arm.e[0]);
  // marker tip: 36 local units beyond the hand along shoulder->target
  const v = [toLocal(front || hand)[0] - 58, toLocal(front || hand)[1] + 428], n = Math.hypot(v[0], v[1]) || 1;
  const tipL: Pt = [arm.h[0] + (v[0] / n) * 36, arm.h[1] + (v[1] / n) * 36];
  const want = drawHand || pointHand, tipW = W(tipL[0], tipL[1]);
  const tip: Pt = want && Math.hypot(want[0] - tipW[0], want[1] - tipW[1]) > 6 ? want : tipW;
  return {shoulder: W(58, -428), elbow: W(arm.e[0], arm.e[1]), hand, tip, forearmAngle: dir};
};

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
  const shL: Pt = [-68, -430], shR: Pt = [58, -428];   // v3.2: back shoulder at the torso edge so both arms read
  // arms: front arm (facing side) draws/points; back arm hangs or gestures
  const front = drawHand || pointHand;
  let frontTarget: Pt = front ? toLocal(front) : [70 + Math.sin(walk) * 30 * moving, -170];
  if (pose.finger && pointHand) {                       // finger point: aim, but keep the elbow bent (no rubber arm)
    const v = [frontTarget[0] - 58, frontTarget[1] + 428], n = Math.hypot(v[0], v[1]) || 1, r = Math.min(n, (L1 + L2) * 0.8);
    frontTarget = [58 + (v[0] / n) * r, -428 + (v[1] / n) * r];
  }
  if (drawHand) {                                       // marker tip (not the hand) touches the path
    const v = [frontTarget[0] - 58, frontTarget[1] + 428], n = Math.hypot(v[0], v[1]) || 1;
    frontTarget = [frontTarget[0] - (v[0] / n) * 36, frontTarget[1] - (v[1] / n) * 36];
  }
  const backTarget: Pt = pose.backHand ? toLocal(pose.backHand)
    : [-102 - Math.sin(walk) * 30 * moving, -182];   // v3.1: no talk-driven jitter (the mouth level flickers every frame)
  const armF = ik(shR, frontTarget, front ? 1 : -1, front ? 0.9 : 0.97);
  const armB = ik(shL, backTarget, -1, pose.backHand ? 0.9 : 0.97);   // resting arms hang almost straight
  const P = (p: Pt) => W(p[0], p[1]).join(',');
  const limb = (a: Pt, b: Pt, c: Pt, col: string, w: number) => (
    <path d={`M ${P(a)} L ${P(b)} L ${P(c)}`} fill="none" stroke={col} strokeWidth={w * S} strokeLinecap="round" strokeLinejoin="round" />
  );
  /** a tailored sleeve: tapered upper arm and forearm with rounded joints, a white shirt cuff at the wrist */
  const sleeve = (a: Pt, b: Pt, c: Pt, col: string, skin: string, frontArm: boolean) => {
    const A = W(a[0], a[1]), B = W(b[0], b[1]), Cw = W(c[0], c[1]);
    const seg = (p: Pt, q: Pt, w0: number, w1: number, fill: string) => {
      const an = Math.atan2(q[1] - p[1], q[0] - p[0]), nx = -Math.sin(an), ny = Math.cos(an);
      return <path d={`M ${p[0] + nx * w0} ${p[1] + ny * w0} L ${q[0] + nx * w1} ${q[1] + ny * w1} L ${q[0] - nx * w1} ${q[1] - ny * w1} L ${p[0] - nx * w0} ${p[1] - ny * w0} Z`} fill={fill} />;
    };
    const an2 = Math.atan2(Cw[1] - B[1], Cw[0] - B[0]);
    const cuff: Pt = [Cw[0] - Math.cos(an2) * 10 * S, Cw[1] - Math.sin(an2) * 10 * S];
    return <g>
      <circle cx={A[0]} cy={A[1]} r={19 * S} fill={col} />
      {seg(A, B, 19 * S, 16 * S, col)}
      <circle cx={B[0]} cy={B[1]} r={16 * S} fill={col} />
      {seg(B, cuff, 16 * S, 13.5 * S, col)}
      {seg([cuff[0] - Math.cos(an2) * 9 * S, cuff[1] - Math.sin(an2) * 9 * S], cuff, 14 * S, 13.5 * S, BRAND.jacketShade)}
      {seg(cuff, [cuff[0] + Math.cos(an2) * 7 * S, cuff[1] + Math.sin(an2) * 7 * S], 13 * S, 12 * S, BRAND.shirt)}
      <path d={`M ${B[0] - Math.cos(an2 - 1.2) * 9 * S} ${B[1] - Math.sin(an2 - 1.2) * 9 * S} q ${Math.cos(an2) * 6 * S} ${Math.sin(an2) * 6 * S} ${Math.cos(an2 + 1.6) * 8 * S} ${Math.sin(an2 + 1.6) * 8 * S}`}
        fill="none" stroke={BRAND.jacketShade} strokeWidth={2.4 * S} strokeLinecap="round" opacity={0.8} />
      {!frontArm && hand3(Cw, an2, skin, false)}
    </g>;
  };
  /** a pointing hand: closed fist, index finger extended along `an`, thumb tucked on top */
  function pointer3(c: Pt, an: number, skin: string) {
    const deg = (an * 180) / Math.PI;
    return <g transform={`translate(${c[0]} ${c[1]}) rotate(${deg}) scale(1.15)`}>
      <rect x={-2 * S} y={-11 * S} width={24 * S} height={22 * S} rx={10 * S} fill={skin} />
      <rect x={14 * S} y={-10 * S} width={30 * S} height={8.5 * S} rx={4.25 * S} fill={skin} />
      <path d={`M ${2 * S} ${4 * S} L ${18 * S} ${4 * S} M ${3 * S} ${8.5 * S} L ${17 * S} ${8.5 * S}`} stroke={BRAND.skinShade} strokeWidth={1.8 * S} strokeLinecap="round" />
      <ellipse cx={10 * S} cy={-11 * S} rx={8 * S} ry={4.2 * S} transform={`rotate(-12 ${10 * S} ${-11 * S})`} fill={skin} />
      <path d={`M ${40 * S} ${-7.5 * S} q ${3 * S} ${1.5 * S} 0 ${3.5 * S}`} stroke={BRAND.skinShade} strokeWidth={1.4 * S} fill="none" />
    </g>;
  }
  /** a simple cartoon hand (palm + thumb) oriented along angle `an` (world radians) */
  function hand3(c: Pt, an: number, skin: string, grip: boolean) {
    const deg = (an * 180) / Math.PI;
    return <g transform={`translate(${c[0]} ${c[1]}) rotate(${deg}) scale(1.22)`}>
      <ellipse cx={6 * S} cy={0} rx={15 * S} ry={grip ? 11 * S : 10 * S} fill={skin} />
      <ellipse cx={4 * S} cy={(grip ? -10 : -9) * S} rx={7 * S} ry={4.5 * S} transform={`rotate(-25 ${4 * S} ${-10 * S})`} fill={skin} />
      {grip && <path d={`M ${2 * S} ${6 * S} L ${16 * S} ${6 * S}`} stroke={BRAND.skinShade} strokeWidth={2 * S} strokeLinecap="round" />}
    </g>;
  }
  const head = W(0, -510);
  const eyeY = -512, eyeDX = 16;
  const torso = [[-64, -252], [-74, -440], [-34, -462], [34, -462], [74, -440], [64, -252]].map((p) => P(p as Pt)).join(' L ');
  const hand = armF.h;
  const handW = W(hand[0], hand[1]);
  const dirF = Math.atan2(armF.h[1] - armF.e[1], armF.h[0] - armF.e[0]);
  const smile = pose.smile || 0;
  return (
    <g transform={pose.lean ? `rotate(${pose.lean} ${x} ${floor})` : undefined}>
      {/* shadow */}
      <ellipse cx={x} cy={floor + 6} rx={90 * S * (1 - 0.15 * Math.min(1, hop / 20))} ry={12 * S} fill="#000" opacity={0.28} />
      {/* back arm */}
      {sleeve(shL, armB.e, armB.h, '#20324F', BRAND.skinShade, false)}
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
      {smile > 0.05 && talking < 0.3 && surprise < 0.3
        ? <path d={`M ${P([6, -482])} Q ${P([18, -482 + 10 * smile])} ${P([30, -482])}`} fill="none" stroke="#6B2E2A" strokeWidth={4 * S} strokeLinecap="round" />
        : <ellipse cx={W(18, -478)[0]} cy={W(18, -478)[1]} rx={(8 + 2 * surprise) * S} ry={(1.6 + 4 * talking + 5 * surprise) * S} fill="#6B2E2A" />}
      {/* front arm + hand + marker */}
      {(() => {
        // the real target (marker tip on the path, or the pointed spot) in world space
        const want: Pt | null = drawHand || pointHand || null;
        const angW = Math.atan2(Math.sin(dirF), Math.cos(dirF) * facing);
        const natural: Pt = [handW[0] + Math.cos(angW) * 40 * S, handW[1] + Math.sin(angW) * 40 * S];
        const gap = want ? Math.hypot(want[0] - natural[0], want[1] - natural[1]) : 0;
        const pole = want && gap > 8 * S && !pose.finger; // out of reach: a telescopic marker / pointer, never a rubber arm
        const tip: Pt = pole ? want! : natural;
        const pa = Math.atan2(tip[1] - handW[1], tip[0] - handW[0]);
        const len = Math.hypot(tip[0] - handW[0], tip[1] - handW[1]);
        return <g>
          {sleeve(shR, armF.e, armF.h, BRAND.jacket, BRAND.skin, true)}
          {pose.finger && pointHand && pointer3(handW, Math.atan2(pointHand[1] - handW[1], pointHand[0] - handW[0]), BRAND.skin)}
          {!pose.finger && (pose.holdingMarker || pointHand) && <g transform={`translate(${handW[0]} ${handW[1]}) rotate(${(pa * 180) / Math.PI})`}>
            {pole && <>
              <rect x={0} y={-3.2 * S} width={Math.max(0, len - 18 * S)} height={6.4 * S} rx={3 * S} fill="#B8963E" />
              <rect x={0} y={-4.6 * S} width={Math.max(0, len * 0.45)} height={9.2 * S} rx={4 * S} fill={BRAND.marker} />
              {[0.45, 0.72].map((u) => <rect key={u} x={len * u - 2 * S} y={-4.4 * S} width={4 * S} height={8.8 * S} fill="#8C6F2A" />)}
            </>}
            {pose.holdingMarker && !pointHand
              ? <g transform={`translate(${pole ? len - 22 * S : 0} 0)`}><rect x={-4 * S} y={-6 * S} width={30 * S} height={12 * S} rx={4 * S} fill={BRAND.marker} />
                  <path d={`M ${26 * S} ${-5 * S} L ${36 * S} 0 L ${26 * S} ${5 * S} Z`} fill="#1A1C20" /></g>
              : pointHand && <circle cx={len} cy={0} r={6 * S} fill="#E8D08A" />}
          </g>}
          {/* fingers wrap the marker / pointer: drawn last so the grip reads */}
          {!(pose.finger && pointHand) && hand3(handW, (pose.holdingMarker || pointHand) ? pa : angW, BRAND.skin, true)}
        </g>;
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

type Action = {kind: 'draw' | 'write' | 'point' | 'react' | 'grow' | 'shock' | 'carry'; at: number; dur: number; d?: string; len?: number; text?: string; x?: number; y?: number;
  size?: number; colour?: string; w?: number; fill?: string; anchor: Pt; end: Pt; bodyA: number; bodyB: number; walkFrom: number; walkAt: number;
  label?: string; hold?: number; group?: number; laser?: boolean; barH?: number; barRect?: [number, number, number, number];
  boxRect?: [number, number, number, number]; fillOpacity?: number; r?: number; pts?: Pt[]; display?: string};

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
  const geoAll = useGeo('world');
  const acts = useMemo(() => {
    const out: Action[] = [];
    // board-space projection of the most recent `map` item (lon/lat items are placed with it)
    let proj: ((lon: number, lat: number) => Pt) | null = null;
    const LL = (q: any, ll?: boolean): Pt => (ll && proj ? proj(q[0], q[1]) : q);
    let tEnd = enterAt + 1.3;
    let lastCue = 0;
    let bx = bodyFor([board.x + 260, 0]);
    const firstX = bx;
    const push = (a0: Omit<Action, 'at' | 'bodyA' | 'bodyB' | 'walkFrom' | 'walkAt'>, cueSpec: any, side = -1) => {
      let a = a0;
      const bA = a.kind === 'react' || (a as any).laser ? bx : bodyFor(a.anchor, side);
      const bB = a.kind === 'draw' || a.kind === 'write' ? bodyFor(a.end, side) : bA;
      let walk = Math.abs(bA - bx) / (520 * S);
      const walkAt = tEnd;
      const cueT = cueSpec !== undefined ? cue(cueSpec, 0) : 0;
      // catch-up: when the character is behind the narration, it walks and draws faster (never skips an item)
      const late = cueSpec !== undefined ? Math.max(0, tEnd + walk - cueT) : Math.max(0, tEnd - lastCue);
      if (late > 0) { walk *= 0.5; a = {...a, dur: a.dur * clamp(1 - late / 2.5, 0.35, 1)}; }
      if (cueSpec !== undefined) lastCue = cueT;
      const at = Math.max(tEnd + walk, cueT);
      out.push({...a, at, bodyA: bA, bodyB: bB, walkFrom: bx, walkAt} as Action);
      tEnd = at + a.dur;
      bx = bB;
    };
    const speed = p.speed || 950;
    for (const it of p.items || []) {
      const cs = it.cue !== undefined ? {cue: it.cue, offset: it.offset} : undefined;
      if (it.stroke || it.arrow) {
        const d: string = it.stroke || arrowPath(LL(it.arrow[0], it.ll), LL(it.arrow[1], it.ll), it.bend ?? 0.18);
        const len = getLength(d);
        const a0 = pointAt(d, 0), a1 = pointAt(d, len);
        push({kind: 'draw', dur: Math.max(0.4, len / (it.speed || speed)), d, len, colour: it.colour, w: it.w, fill: it.fill,
          anchor: [a0.x, a0.y], end: [a1.x, a1.y]}, cs);
      } else if (it.box) {
        const [x, y, w, h] = it.box;
        const d = `M ${x} ${y} L ${x + w} ${y} L ${x + w} ${y + h} L ${x} ${y + h} Z`;
        push({kind: 'draw', dur: Math.max(0.5, (2 * (w + h)) / (it.speed || speed * 1.3)), d, len: 2 * (w + h), colour: it.colour, w: it.w || 5, fill: it.fill,
          anchor: [x, y], end: [x, y + h], boxRect: [x, y, w, h]}, cs);
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
        const pp = LL(it.point, it.ll);
        push({kind: 'point', dur: it.hold || 1.6, anchor: pp, end: pp, label: it.label, colour: it.colour, laser: !!it.laser}, cs,
          it.side === 'right' ? 1 : -1);
      } else if (it.react) {
        push({kind: 'react', dur: 0.8, anchor: [0, 0], end: [0, 0]}, cs);
      } else if (it.map) {
        // the presenter DRAWS a map: each country's main outline is traced by the marker, then tinted
        const [rx, ry, rw, rh] = it.rect || [board.x + 40, board.y + 40, board.w - 80, board.h - 80];
        const v = it.map;
        const Sz = 4096;
        const [mcx, mcy] = merc(v.lon, v.lat);
        const k = rw / ((v.span / 360) * Sz);
        proj = (lon: number, lat: number): Pt => { const [mx, my] = merc(lon, lat); return [rx + rw / 2 + (mx - mcx) * k, ry + rh / 2 + (my - mcy) * k]; };
        const rings = geoAll && geoAll.paths ? parseLayer('world', geoAll.paths) : {};
        (it.countries || []).forEach((code: string, ci: number) => {
          const rs = (rings as any)[code] as {pts: Float64Array; x0: number; y0: number; x1: number; y1: number}[] | undefined;
          if (!rs || !rs.length) return;
          const big = rs.slice().sort((a, b) => (b.x1 - b.x0) * (b.y1 - b.y0) - (a.x1 - a.x0) * (a.y1 - a.y0))[0];
          const n = big.pts.length / 2, step = Math.max(1, Math.floor(n / (it.points || 140)));
          let d = '';
          for (let i = 0; i < n; i += step) {
            const X = rx + rw / 2 + (big.pts[2 * i] - mcx) * k, Y = ry + rh / 2 + (big.pts[2 * i + 1] - mcy) * k;
            d += (d ? ' L ' : 'M ') + X.toFixed(1) + ' ' + Y.toFixed(1);
          }
          d += ' Z';
          const len = getLength(d);
          const a0 = pointAt(d, 0), a1 = pointAt(d, len);
          const hl = it.highlight?.[code];
          push({kind: 'draw', dur: Math.max(0.5, len / (it.speed || speed * 1.4)), d, len, colour: hl || it.colour || 'muted', w: hl ? 4 : 3,
            fill: hl || it.fill || 'muted', fillOpacity: hl ? 0.55 : 0.18, anchor: [a0.x, a0.y], end: [a1.x, a1.y]},
            ci === 0 ? cs : (it.country_cues?.[code] !== undefined ? {cue: it.country_cues[code]} : undefined));
        });
      } else if (it.pin || it.bubble) {
        const pos = LL(it.pin || it.bubble, it.ll);
        const r = it.bubble ? Math.max(10, (it.max_r || 70) * Math.sqrt((it.value || 1) / (it.max_value || it.value || 1))) : (it.r || 12);
        push({kind: 'grow', dur: it.hold || 1.0, anchor: pos, end: pos, label: it.label, colour: it.colour, r, display: it.display, laser: !!it.laser}, cs,
          it.side === 'right' ? 1 : -1);
      } else if (it.shock) {
        const pts: Pt[] = it.shock.map((q: any) => LL(q, it.ll));
        let len = 0;
        for (let i = 1; i < pts.length; i++) len += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
        push({kind: 'shock', dur: Math.max(1.2, len / (it.speed || 380)), anchor: pts[0], end: pts[0], pts, len, colour: it.colour || 'risk', label: it.label, laser: true}, cs);
      } else if (it.carry) {
        const a0 = LL(it.carry[0], it.ll), a1 = LL(it.carry[1], it.ll);
        const len = Math.hypot(a1[0] - a0[0], a1[1] - a0[1]);
        push({kind: 'carry', dur: 0.4 + len / (it.speed || 420), anchor: a0, end: a1, len, label: it.label, colour: it.colour}, cs, it.side === 'right' ? 1 : -1);
      }
    }
    const endBy = (scene.duration || 1e9) - 1.0;
    const last = out.length ? out[out.length - 1].at + out[out.length - 1].dur : 0;
    if (last > endBy && out.length) {
      const t0 = Math.min(...out.map((o) => o.at));
      const f = Math.max(0.5, (endBy - t0) / Math.max(0.1, last - t0));
      out.forEach((o) => { o.at = t0 + (o.at - t0) * f; o.walkAt = t0 + (o.walkAt - t0) * f; o.dur *= f; });
    }
    return {out, firstX};
  }, [scene, geoAll]);
  const {out: actions, firstX} = acts;
  const carryPos = (a: Action, tt: number): Pt => {
    const u = easeInOut(clamp((tt - a.at - 0.3) / Math.max(0.1, a.dur - 0.3)));
    return [lerp(a.anchor[0], a.end[0], u), lerp(a.anchor[1], a.end[1], u) - Math.sin(Math.PI * u) * 40];
  };
  const shockPos = (a: Action, u: number): Pt => {
    const pts = a.pts!; let d = u * a.len!;
    for (let i = 1; i < pts.length; i++) {
      const sl = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
      if (d <= sl) { const f = d / Math.max(1e-6, sl); return [lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)]; }
      d -= sl;
    }
    return pts[pts.length - 1];
  };
  // when does a shock reach each point (for boxes turning red)
  const shockHits: {t: number; p: Pt}[] = [];
  actions.forEach((a) => {
    if (a.kind !== 'shock') return;
    let acc = 0;
    a.pts!.forEach((q, i) => { if (i) acc += Math.hypot(q[0] - a.pts![i - 1][0], q[1] - a.pts![i - 1][1]); shockHits.push({t: a.at + (acc / a.len!) * a.dur, p: q}); });
  });
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
      if (tt < a.at + a.dur) {
        // while drawing/writing the body follows the pen so the hand can stay on the path
        if (a.kind === 'draw' || a.kind === 'write' || a.kind === 'carry') {
          const u = (tt - a.at) / a.dur;
          const pen: Pt = a.kind === 'draw' ? (() => { const q = pointAt(a.d!, easeInOut(u) * a.len!); return [q.x, q.y] as Pt; })()
            : a.kind === 'carry' ? carryPos(a, tt) : [a.x! + a.len! * u, a.y!];
          const follow = bodyFor(pen, a.bodyA > a.anchor[0] ? 1 : -1);
          const blend = clamp(u * 6, 0, 1);              // ease from the start spot into following
          return lerp(a.bodyA, follow, blend);
        }
        return lerp(a.bodyA, a.bodyB, easeInOut((tt - a.at) / a.dur));
      }
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
    else if (a.kind === 'point' || a.kind === 'grow') { pointHand = a.anchor; target = a.anchor; }
    else if (a.kind === 'shock') { const q = shockPos(a, u); pointHand = q; target = q; }
    else if (a.kind === 'carry') { const q = carryPos(a, t); drawHand = q; target = q; }
    else if (a.kind === 'react') { const q = u; surprise = Math.sin(Math.PI * q); hop = 24 * Math.sin(Math.PI * clamp(q * 1.6)); }
  }
  const laserFrom: Pt = (() => {
    if (!target) return [x, floor - 430 * S];
    const sh: Pt = [x + 58 * S * (target[0] >= x ? 1 : -1), floor - 428 * S];
    const ang = Math.atan2(target[1] - sh[1], target[0] - sh[0]);
    const d = Math.min(Math.hypot(target[0] - sh[0], target[1] - sh[1]), (L1 + L2 - 2) * 1.5 * S);
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
          {!a.barRect && a.fill && fillU > 0 && <path d={a.d} fill={pal[a.fill] || a.fill} opacity={(a.fillOpacity ?? 0.22) * fillU} />}
          {a.boxRect && (() => {
            const hit = shockHits.find((h) => h.p[0] >= a.boxRect![0] - 4 && h.p[0] <= a.boxRect![0] + a.boxRect![2] + 4 && h.p[1] >= a.boxRect![1] - 4 && h.p[1] <= a.boxRect![1] + a.boxRect![3] + 4);
            if (!hit || t < hit.t) return null;
            const q = eo(t, hit.t, 0.4);
            return <rect x={a.boxRect![0]} y={a.boxRect![1]} width={a.boxRect![2]} height={a.boxRect![3]} fill={pal.risk || '#FF5A5F'} opacity={0.28 * q}
              stroke={pal.risk || '#FF5A5F'} strokeWidth={5} transform={`translate(${Math.sin((t - hit.t) * 40) * 4 * (1 - q)} 0)`} />;
          })()}
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
          <clipPath id={`pw-${scene.id}-${i}`}><rect x={a.x! - 6} y={a.y! - a.size! * 1.1} width={u >= 0.999 ? a.len! * 1.6 + 40 : a.len! * u * 1.12 + 10} height={a.size! * 1.5} /></clipPath>
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
    if (a.kind === 'grow') {
      if (t < a.at) return null;
      const c = a.colour ? pal[a.colour] || a.colour : pal.accent;
      const g = eo(t, a.at, 0.7);
      const q = ((t - a.at) % 1.6) / 1.6;
      return (
        <g key={i}>
          <circle cx={a.anchor[0]} cy={a.anchor[1]} r={a.r! * g} fill={c} opacity={0.35} stroke={c} strokeWidth={3} />
          <circle cx={a.anchor[0]} cy={a.anchor[1]} r={(a.r! + 22 * q) * g} fill="none" stroke={c} strokeWidth={2} opacity={0.6 * (1 - q)} />
          <circle cx={a.anchor[0]} cy={a.anchor[1]} r={6} fill={c} />
          {(a.label || a.display) && <g opacity={eo(t, a.at + 0.3, 0.4)}>
            <text x={a.anchor[0]} y={a.anchor[1] - a.r! - 14} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={22}>{a.label}</text>
            {a.display && <text x={a.anchor[0]} y={a.anchor[1] + a.r! + 30} textAnchor="middle" fill={c} fontFamily={font.display} fontWeight={800} fontSize={26}>{a.display}</text>}
          </g>}
        </g>
      );
    }
    if (a.kind === 'shock') {
      if (t < a.at) return null;
      const c = pal[a.colour!] || a.colour || '#FF5A5F';
      const uu = clamp((t - a.at) / a.dur);
      const head = shockPos(a, uu);
      const trail = Array.from({length: 14}, (_, k) => shockPos(a, Math.max(0, uu - k * 0.012)));
      const fade = 1 - eo(t, a.at + a.dur + 1.5, 1);
      return (
        <g key={i} opacity={fade}>
          {trail.map((q, k) => <circle key={k} cx={q[0]} cy={q[1]} r={14 - k * 0.8} fill={c} opacity={(1 - k / 14) * 0.7} />)}
          {uu < 1 && <circle cx={head[0]} cy={head[1]} r={18 + 6 * Math.sin(t * 20)} fill="none" stroke={c} strokeWidth={4} />}
          {shockHits.filter((h) => t >= h.t && t < h.t + 0.9).map((h, k) => {
            const q = (t - h.t) / 0.9;
            return <circle key={'b' + k} cx={h.p[0]} cy={h.p[1]} r={20 + 70 * q} fill="none" stroke={c} strokeWidth={5} opacity={1 - q} />;
          })}
          {a.label && <text x={a.pts![0][0]} y={a.pts![0][1] - 40} textAnchor="middle" fill={c} fontFamily={font.display} fontWeight={800} fontSize={28}
            opacity={eo(t, a.at, 0.4)}>{a.label}</text>}
        </g>
      );
    }
    if (a.kind === 'carry') {
      const c = a.colour ? pal[a.colour] || a.colour : pal.accent;
      const pos = t < a.at ? a.anchor : t > a.at + a.dur ? a.end : carryPos(a, t);
      const w2 = Math.max(110, String(a.label || '').length * 15 + 30);
      return (
        <g key={i} transform={`translate(${pos[0]} ${pos[1]})`} opacity={eo(t, a.at - 0.8, 0.5)}>
          <rect x={-w2 / 2} y={-26} width={w2} height={52} rx={12} fill={pal.bg} stroke={c} strokeWidth={3} />
          <text y={9} textAnchor="middle" fill={c} fontFamily={font.body} fontWeight={800} fontSize={24}>{a.label}</text>
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
