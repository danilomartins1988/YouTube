import React from 'react';
import {Character, type Pose} from '../../presenter/Presenter';
import {DrawTimeline, penAt} from '../DrawOnCanvas/DrawOnCanvas';
import {E, clamp, lerp, lerpV, win} from '../motion';
import type {Vec} from '../types';

/**
 * AnimatedPresenter: the channel's articulated economist (head, torso, two-bone IK arms, hands, legs, feet,
 * face) driven by a declarative list of timed actions. Each state below is real joint motion, not a sprite
 * sliding across the screen:
 *
 *   enter / walk / exit  distance-driven walk cycle (legs, arm swing, head bob), with ANTICIPATION (leans back
 *                        as it starts) and FOLLOW-THROUGH (settles forward when it stops)
 *   draw                 follows a DrawOnCanvas timeline: the marker tip sits on the active stroke, the arm
 *                        solves IK every frame and the body shuffles along with the pen
 *   write                small handwriting oscillation along a line while text is revealed
 *   point                raises the arm to a target (eased in, held, eased out)
 *   explain              open-hand gesture with the other arm while talking
 *   react                hop + raised eyebrows + 'aha' marks, then a smile
 *   idle                 breathing and blinking (always on)
 */
export type PresenterAction =
  | {kind: 'enter' | 'walk' | 'exit'; at: number; dur: number; to: number; from?: number}
  | {kind: 'draw'; timeline: DrawTimeline}
  | {kind: 'write'; at: number; dur: number; x: number; y: number; width: number}
  | {kind: 'point'; at: number; dur: number; target: Vec}
  | {kind: 'explain'; at: number; dur: number}
  | {kind: 'react'; at: number; dur?: number}
  | {kind: 'smile'; at: number; dur: number; amount?: number};

export type AnimatedPresenterProps = {
  t: number;
  actions: PresenterAction[];
  /** y of the floor line (feet) */
  floor: number;
  scale?: number;
  startX?: number;
  /** time ranges (s) in which the mouth talks */
  talk?: [number, number][];
  /** where the character looks when it has nothing to do (+1 right, -1 left) */
  faceDefault?: 1 | -1;
  /** horizontal distance kept between body and the hand target while drawing */
  reach?: number;
  /** x where the character steps aside to (off the drawing) during long pen pauses and after drawing */
  park?: number;
  /** 'serious' (thrillers, crises): never smiles or hops; 'neutral': restrained; 'warm' (default): original */
  demeanor?: 'warm' | 'neutral' | 'serious';
};

const startOf = (a: PresenterAction) => (a.kind === 'draw' ? a.timeline.start : a.at);

/** Body x position at time t (pure function of the action list). */
/** 0..1: how far the character has stepped aside during a long pause between two strokes (gap > 2.4 s). */
export const parkAmount = (tl: DrawTimeline, t: number): number => {
  const S = tl.strokes;
  for (let i = 0; i + 1 < S.length; i++) {
    const a = S[i], b = S[i + 1];
    if (b.t0 - a.t1 > 2.4 && t > a.t1 && t < b.t0)
      return Math.min(E.inOut(win(t, a.t1 + 0.2, 0.9)), 1 - E.inOut(win(t, b.t0 - 1.1, 0.9)));
  }
  return 0;
};

const bodyX = (t: number, acts: PresenterAction[], startX: number, reach: number, park?: number): number => {
  let cur = startX;
  const slack = reach * 0.55;
  for (const a of acts) {
    if (a.kind === 'enter' || a.kind === 'walk' || a.kind === 'exit') {
      const from = a.from ?? cur;
      if (t < a.at) return cur;
      if (t <= a.at + a.dur) return lerp(from, a.to, E.inOut(win(t, a.at, a.dur)));
      cur = a.to;
    } else if (a.kind === 'draw') {
      const tl = a.timeline, s = tl.start, e = tl.end;
      // the body follows a smoothed copy of the pen path (average over +-0.35 s) so steps look deliberate
      const follow = (tt: number) => {
        let sx = 0, n = 0;
        for (let k = -3; k <= 3; k++) { sx += penAt(tl, clamp(tt + k * 0.12, s, e)).pt[0]; n++; }
        // never let the smoothed body trail the pen by more than the arm can comfortably cover
        const px = penAt(tl, clamp(tt, s, e)).pt[0] - reach;
        return clamp(sx / n - reach, px - slack, px + slack);
      };
      if (t < s - 0.5) return cur;
      if (t < s) return lerp(cur, follow(s), E.inOut(win(t, s - 0.5, 0.5)));
      if (t <= e) return park === undefined ? follow(t) : lerp(follow(t), park, parkAmount(tl, t));
      if (park !== undefined) {                      // finished: step aside so the whole diagram is visible
        if (t <= e + 1.3) return lerp(follow(e), park, E.inOut(win(t, e + 0.3, 1.0)));
        cur = park;
      } else cur = follow(e);
    } else if (a.kind === 'point' || a.kind === 'write') {
      const tx = a.kind === 'point' ? a.target[0] : a.x;
      const far = park !== undefined ? reach * 5.8 : reach * 1.7;      // with a telescopic pointer he can point from aside
      const need = Math.abs(tx - cur) > far ? tx - Math.sign(tx - cur) * reach * 1.2 : cur;
      if (t < a.at - 0.45) return cur;
      if (t < a.at) return lerp(cur, need, E.inOut(win(t, a.at - 0.45, 0.45)));
      cur = need;
    }
  }
  return cur;
};

export const presenterPose = (p: AnimatedPresenterProps): Pose & {handTarget: Vec | null} => {
  const {t, floor, scale: S = 0.9, faceDefault = 1, talk = []} = p;
  const reach = p.reach ?? 230 * S;
  const acts = [...p.actions].sort((a, b) => startOf(a) - startOf(b));
  const enter = acts.find((a) => a.kind === 'enter') as any;
  const startX = p.startX ?? enter?.from ?? 300;
  const X = (tt: number) => bodyX(tt, acts, startX, reach, p.park);
  const dt = 1 / 30;
  const x = X(t), v = (X(t + dt) - X(t - dt)) / (2 * dt), acc = (X(t + 2 * dt) - 2 * x + X(t - 2 * dt)) / (4 * dt * dt);
  const moving = clamp(Math.abs(v) / 260);
  // anticipation & follow-through: lean opposite to acceleration, plus a forward lean while walking
  const lean = clamp(v * 0.01 - acc * 0.0045, -7, 7);

  let drawHand: Vec | null = null, pointHand: Vec | null = null, backHand: Vec | null = null, holding = false;
  let target: Vec | null = null;
  const rest: Vec = [x + 70 * S * faceDefault, floor - 170 * S];
  let surprise = 0, hop = 0, smile = 0, talking = 0;
  for (const a of acts) {
    if (a.kind === 'draw') {
      const tl = a.timeline;
      if (t >= tl.start - 0.45 && t <= tl.end + 0.35) {
        const pen = penAt(tl, t).pt;
        const inU = E.out(win(t, tl.start - 0.45, 0.45)), outU = E.in(win(t, tl.end, 0.35));
        drawHand = lerpV(lerpV(lerpV(rest, pen, inU), rest, outU), rest, p.park !== undefined ? parkAmount(tl, t) : 0);
        holding = true; target = p.park !== undefined && parkAmount(tl, t) > 0.5 ? null : pen;
      }
    } else if (a.kind === 'write' && t >= a.at - 0.3 && t <= a.at + a.dur + 0.3) {
      const u = win(t, a.at, a.dur);
      const pen: Vec = [a.x + a.width * u, a.y + Math.sin(u * a.width * 0.35) * 7 - Math.abs(Math.sin(u * a.width * 0.11)) * 6];
      const inU = E.out(win(t, a.at - 0.3, 0.3)), outU = E.in(win(t, a.at + a.dur, 0.3));
      drawHand = lerpV(lerpV(rest, pen, inU), rest, outU); holding = true; target = pen;
    } else if (a.kind === 'point' && t >= a.at && t <= a.at + a.dur) {
      const inU = E.outBack(win(t, a.at, 0.35)), outU = E.in(win(t, a.at + a.dur - 0.3, 0.3));
      // a tiny overshoot-and-settle on the way up (secondary motion)
      pointHand = lerpV(lerpV(rest, a.target, inU), rest, outU); target = a.target;
    } else if (a.kind === 'explain' && t >= a.at && t <= a.at + a.dur) {
      const u = win(t, a.at, a.dur), env = Math.sin(Math.PI * clamp(u * 1.15));
      const side = -faceDefault;
      backHand = [x + side * (95 + 25 * Math.sin(t * 5.2)) * S, floor - (300 + 40 * env + 18 * Math.cos(t * 4.1)) * S];
      talking = Math.max(talking, 0.6 + 0.4 * Math.abs(Math.sin(t * 17)));
    } else if (a.kind === 'react') {
      const d = a.dur ?? 0.9, u = win(t, a.at, d);
      if (u > 0 && u < 1) { surprise = Math.max(surprise, Math.sin(Math.PI * u)); hop = Math.max(hop, 26 * Math.sin(Math.PI * clamp(u * 1.6))); }
      if (t > a.at + d * 0.6) smile = Math.max(smile, 1 - win(t, a.at + d + 1.2, 0.8));
    } else if (a.kind === 'smile' && t >= a.at && t <= a.at + a.dur) {
      smile = Math.max(smile, (a.amount ?? 1) * Math.min(win(t, a.at, 0.3), 1 - win(t, a.at + a.dur - 0.3, 0.3)));
    }
  }
  for (const [a, b] of talk) if (t >= a && t <= b) talking = Math.max(talking, 0.5 + 0.5 * Math.abs(Math.sin(t * 21)));
  // a character that is drawing or pointing keeps facing its target (it side-steps); otherwise it faces travel
  const facing: 1 | -1 = target ? (target[0] >= x ? 1 : -1) : moving > 0.25 ? (v > 0 ? 1 : -1) : faceDefault;
  const blink = ((t + 0.7) % 3.4) < 0.12 ? 1 : 0;
  const breathe = Math.sin(t * 2.2) * 1.6 * (1 - moving);
  const dm = p.demeanor === 'serious' ? {smile: 0, hop: 0.15, surprise: 0.35} : p.demeanor === 'neutral' ? {smile: 0.4, hop: 0.5, surprise: 0.7} : {smile: 1, hop: 1, surprise: 1};
  smile *= dm.smile; hop *= dm.hop; surprise *= dm.surprise;
  return {x, floor, facing, walk: x / (58 * S), moving, hop: hop + breathe, drawHand, pointHand, backHand, talking, blink,
    surprise, scale: S, holdingMarker: holding, lean, smile, handTarget: drawHand || pointHand};
};

/** Renders the character for time t. Place it inside an <svg> in the same coordinate space as the board. */
export const AnimatedPresenter: React.FC<AnimatedPresenterProps> = (props) => {
  const pose = presenterPose(props);
  const pen = pose.drawHand && pose.holdingMarker;
  return (
    <g>
      {pose.pointHand && (
        <circle cx={pose.pointHand[0]} cy={pose.pointHand[1]} r={22 + 8 * Math.sin(props.t * 6)} fill="none" stroke="#D4AF5A" strokeWidth={3} opacity={0.7} />
      )}
      <Character pose={pose} />
      {pen && <circle cx={pose.drawHand![0]} cy={pose.drawHand![1]} r={5} fill="#D4AF5A" opacity={0.9} />}
    </g>
  );
};
