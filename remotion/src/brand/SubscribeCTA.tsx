import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {Character} from '../presenter/Presenter';
import {clamp, easeBack, easeInOut, easeOut, lerp} from '../lib/anim';

/**
 * Channel call to action (docs/CTA_STANDARD.md): a generic red rounded SUBSCRIBE pill, a thumbs-up LIKE button and a
 * small bell, in the channel's cartoon style (thick dark outlines, flat colours). A cartoon glove clicks the thumb (it
 * fills) and then the pill (it turns grey "SUBSCRIBED"), and the bell rings. No platform logo of any kind.
 *
 *   SubscribeWidget   the animated widget in a 760x260 local box (t = seconds since it started; CTA_SECONDS long)
 *   SubscribeCTA      composition: the widget alone on a transparent canvas (overlay asset, alpha)
 *   CTACard           composition / scene type `cta_card`: full-frame brand card (mascot + big widget + two lines),
 *                     used for the narrated CTA that sits right before the channel intro (and the like ask at the end)
 *   CTAOverlayLayer   Documentary layer: the widget in a lower corner at the times listed in props.cta
 */
export const CTA_SECONDS = 4;
export const CTA_W = 760, CTA_H = 260;

const OL = '#0B0B0F', RED = '#E5262B', RED_HI = '#FF5A4E', GREY = '#8C8F96', WHITE = '#FFFFFF', GOLD = '#FFC21A',
  BLUE = '#2F7BFF', FONT = 'Inter Display, Inter, sans-serif';
const NAVY0 = '#0A1430', NAVY1 = '#1E3A7A';

// timeline of the widget (seconds)
const T_IN = 0.0, T_THUMB = 1.05, T_PILL = 1.95, T_BELL = 2.2, T_OUT = 3.55;

/** Cartoon glove pointing up-left (fingertip at 0,0). */
const Glove: React.FC<{press: number}> = ({press}) => (
  <g transform={`scale(${1 - press * 0.12})`}>
    <path d="M 0 0 C -6 -2 -14 6 -10 14 L 8 62 C -8 58 -22 66 -18 80 C -6 96 10 104 26 118 C 44 132 74 134 92 118 C 108 104 112 82 104 62
             L 94 36 C 90 26 78 26 74 34 C 72 24 60 22 56 32 C 54 22 40 22 38 34 L 20 6 C 16 -2 6 -4 0 0 Z"
      fill={WHITE} stroke={OL} strokeWidth={7} strokeLinejoin="round" />
    <path d="M 56 32 L 64 58 M 74 34 L 80 58 M 38 34 L 48 60" stroke={OL} strokeWidth={5} strokeLinecap="round" fill="none" />
    <path d="M 30 120 L 84 124" stroke={OL} strokeWidth={6} strokeLinecap="round" />
  </g>
);

const ThumbIcon: React.FC<{fill: number}> = ({fill}) => {
  const col = fill > 0.5 ? BLUE : WHITE;
  return (
    <g>
      <path d="M -38 -2 L -38 44 L -18 44 L -18 -2 Z" fill={col} stroke={OL} strokeWidth={7} strokeLinejoin="round" />
      <path d="M -12 -2 L 6 -38 C 10 -50 28 -48 26 -32 L 22 -10 L 44 -10 C 56 -10 62 0 58 10 L 48 38 C 46 44 40 46 34 46 L -12 46 Z"
        fill={col} stroke={OL} strokeWidth={7} strokeLinejoin="round" />
    </g>
  );
};

const Bell: React.FC<{swing: number}> = ({swing}) => (
  <g transform={`rotate(${swing})`}>
    <path d="M -26 18 C -22 4 -24 -22 0 -26 C 24 -22 22 4 26 18 L 32 26 L -32 26 Z" fill={GOLD} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <circle cx={0} cy={32} r={7} fill={GOLD} stroke={OL} strokeWidth={5} />
    <circle cx={0} cy={-28} r={5} fill={GOLD} stroke={OL} strokeWidth={4} />
  </g>
);

/** The widget, drawn in a 760x260 box. `t` in seconds; `hold` keeps it on screen (no exit) for cards. */
export const SubscribeWidget: React.FC<{t: number; hold?: boolean; like?: boolean}> = ({t, hold = false, like = true}) => {
  const inU = easeBack(clamp((t - T_IN) / 0.4));
  const outU = hold ? 0 : easeInOut(clamp((t - T_OUT) / 0.45));
  const thumbOn = like ? clamp((t - T_THUMB) / 0.12) : 0;
  const pillOn = clamp((t - T_PILL) / 0.14);
  // glove path: enters from the bottom right, to the thumb, then to the pill, then leaves
  const thumbX = 120, thumbY = 130, pillX = 420, pillY = 130;
  const g1 = easeInOut(clamp((t - 0.45) / 0.55)), g2 = easeInOut(clamp((t - 1.35) / 0.55)), g3 = easeInOut(clamp((t - 2.35) / 0.5));
  const start = like ? [760, 330] : [760, 330];
  let gx = lerp(start[0], like ? thumbX + 6 : pillX, g1), gy = lerp(start[1], like ? thumbY + 4 : pillY, g1);
  if (like) { gx = lerp(gx, pillX + 40, g2); gy = lerp(gy, pillY + 6, g2); }
  gx = lerp(gx, 820, g3); gy = lerp(gy, 360, g3);
  const pressAt = (c: number) => Math.max(0, 1 - Math.abs(t - c) / 0.12);
  const press = Math.max(like ? pressAt(T_THUMB) : 0, pressAt(T_PILL));
  const burst = (c: number) => clamp((t - c) / 0.35);
  const bellU = clamp((t - T_BELL) / 0.25);
  const swing = Math.sin((t - T_BELL) * 22) * 22 * Math.max(0, 1 - (t - T_BELL) / 0.9) * (t > T_BELL ? 1 : 0);
  const sc = lerp(0.2, 1, inU) * (1 - outU * 0.15);
  const op = clamp(inU * 3) * (1 - outU);
  const pillCol = pillOn > 0.5 ? GREY : RED;
  const ray = (cx: number, cy: number, u: number, col: string) => u > 0 && u < 1 ? <g opacity={1 - u}>
    {Array.from({length: 8}, (_, k) => { const a = (k / 8) * Math.PI * 2, r0 = 46 + u * 20, r1 = 60 + u * 46;
      return <line key={k} x1={cx + Math.cos(a) * r0} y1={cy + Math.sin(a) * r0} x2={cx + Math.cos(a) * r1} y2={cy + Math.sin(a) * r1}
        stroke={col} strokeWidth={7} strokeLinecap="round" />; })}</g> : null;
  return (
    <g opacity={op} transform={`translate(${CTA_W / 2} ${CTA_H / 2}) scale(${sc}) translate(${-CTA_W / 2} ${-CTA_H / 2})`}>
      {/* soft dark plate so it reads on any picture */}
      <rect x={14} y={42} width={like ? 732 : 600} height={176} rx={88} fill="#0B1226" opacity={0.82} stroke={OL} strokeWidth={6} />
      {like && <g>
        <circle cx={thumbX} cy={thumbY} r={62} fill={thumbOn > 0.5 ? '#DCE9FF' : '#24304F'} stroke={OL} strokeWidth={7} />
        <g transform={`translate(${thumbX - 8} ${thumbY + 2}) scale(${0.95 + 0.25 * pressAt(T_THUMB) + 0.1 * Math.sin(clamp((t - T_THUMB) / 0.3) * Math.PI)})`}>
          <ThumbIcon fill={thumbOn} />
        </g>
        {ray(thumbX, thumbY, burst(T_THUMB), BLUE)}
      </g>}
      {/* the pill */}
      <g transform={`translate(${like ? 0 : -190} 0)`}>
        <g transform={`translate(${pillX} ${pillY}) scale(${1 - 0.07 * pressAt(T_PILL)})`}>
          <rect x={-176} y={-50} width={352} height={100} rx={50} fill={pillCol} stroke={OL} strokeWidth={8} />
          {pillOn <= 0.5 && <rect x={-160} y={-40} width={320} height={26} rx={13} fill={RED_HI} opacity={0.55} />}
          <text x={pillOn > 0.5 ? 24 : 0} y={pillOn > 0.5 ? 13 : 15} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={pillOn > 0.5 ? 37 : 48}
            fill={WHITE} letterSpacing={1}>{pillOn > 0.5 ? 'SUBSCRIBED' : 'SUBSCRIBE'}</text>
          {pillOn > 0.5 && <path d="M -152 0 L -140 12 L -120 -12" stroke={WHITE} strokeWidth={8} fill="none" strokeLinecap="round" strokeLinejoin="round" />}
        </g>
        {ray(pillX, pillY, burst(T_PILL), GOLD)}
        {/* bell */}
        <g transform={`translate(${pillX + 252} ${pillY}) scale(${easeBack(bellU)})`} opacity={bellU > 0 ? 1 : 0}>
          <circle r={52} fill="#24304F" stroke={OL} strokeWidth={7} />
          <Bell swing={swing} />
        </g>
      </g>
      {/* glove cursor */}
      <g transform={`translate(${gx} ${gy})`} opacity={clamp(g1 * 4) * (1 - g3)}><Glove press={press} /></g>
    </g>
  );
};

/** Composition: the widget alone on a transparent canvas (rendered once to assets/brand/cta/). */
export const SubscribeCTA: React.FC<{like?: boolean}> = ({like = true}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'transparent'}}>
      <svg width={width} height={height} viewBox={`0 0 ${CTA_W} ${CTA_H}`}>
        <SubscribeWidget t={frame / fps} like={like} />
      </svg>
    </AbsoluteFill>
  );
};

const mascot = (x: number, floor: number, S: number, talking: number) => <Character pose={{x, floor, facing: 1, walk: 0, moving: 0, hop: 0,
  drawHand: null, pointHand: null, talking, blink: 0, surprise: 0, scale: S, holdingMarker: false, smile: 1} as any} />;

export type CTACardProps = {kind?: 'subscribe' | 'like'; top?: string; bottom?: string; seconds?: number};
export const CTA_CARD_TEXT = {
  subscribe: {top: 'LIKE FINDING THE HIDDEN MONEY?', bottom: "IT'S FREE · IT HELPS THE CHANNEL"},
  like: {top: 'DID THIS CHANGE YOUR MIND?', bottom: 'TELL US IN THE COMMENTS'},
};

/** Full-frame card art at time t (seconds) of a card lasting `dur` seconds. */
export const CTACardArt: React.FC<{t: number; dur: number; W?: number; H?: number} & CTACardProps> = ({t, dur, W = 1920, H = 1080, kind = 'subscribe', top, bottom}) => {
  const txt = CTA_CARD_TEXT[kind];
  const fin = easeOut(clamp(t / 0.35)), fout = 1 - easeInOut(clamp((t - (dur - 0.3)) / 0.3));
  const a = Math.min(fin, fout);
  const wt = Math.min(t * 1.0, CTA_SECONDS - 0.5);   // the widget plays once and holds
  return (
    <AbsoluteFill style={{backgroundColor: NAVY0}}>
      <svg width={W} height={H} viewBox="0 0 1920 1080">
        <defs><radialGradient id="ctaBg" cx="60%" cy="45%" r="75%"><stop offset="0" stopColor={NAVY1} /><stop offset="1" stopColor={NAVY0} /></radialGradient></defs>
        <rect width={1920} height={1080} fill="url(#ctaBg)" />
        <g opacity={0.06 + 0.02 * Math.sin(t * 2)}>{Array.from({length: 28}, (_, k) => { const a0 = (k / 28) * Math.PI * 2 + t * 0.05, a1 = a0 + Math.PI / 28;
          return <path key={k} d={`M 1150 520 L ${1150 + Math.cos(a0) * 1800} ${520 + Math.sin(a0) * 1800} L ${1150 + Math.cos(a1) * 1800} ${520 + Math.sin(a1) * 1800} Z`} fill="#FFFFFF" />; })}</g>
        <g opacity={a}>
          <g transform={`translate(${lerp(-200, 0, easeOut(clamp(t / 0.6)))} 0)`}>{mascot(380, 1080, 1.25, t < dur - 0.4 ? 0.6 : 0)}</g>
          <text x={1150} y={250} textAnchor="middle" fontFamily={FONT} fontWeight={900} fontSize={72} fill={WHITE} stroke={OL} strokeWidth={10}
            paintOrder="stroke" opacity={easeOut(clamp((t - 0.15) / 0.4))}>{top || txt.top}</text>
          <rect x={1150 - 380} y={282} width={760} height={10} rx={5} fill={GOLD} opacity={easeOut(clamp((t - 0.25) / 0.4))} />
          <g transform={`translate(${1150 - CTA_W * 0.82} ${330}) scale(1.64)`}><SubscribeWidget t={wt} hold like /></g>
          <text x={1150} y={850} textAnchor="middle" fontFamily={FONT} fontWeight={800} fontSize={50} fill={GOLD}
            opacity={easeOut(clamp((t - 0.5) / 0.4))}>{bottom || txt.bottom}</text>
          <text x={1150} y={930} textAnchor="middle" fontFamily={FONT} fontWeight={700} fontSize={32} fill="#C9D6F5"
            opacity={easeOut(clamp((t - 0.7) / 0.4))}>THE HIDDEN ECONOMICS</text>
        </g>
      </svg>
    </AbsoluteFill>
  );
};

/** Composition: the full-frame card (for splicing into already-rendered films). */
export const CTACard: React.FC<CTACardProps> = (p) => {
  const frame = useCurrentFrame();
  const {fps, width, height, durationInFrames} = useVideoConfig();
  return <CTACardArt t={frame / fps} dur={durationInFrames / fps} W={width} H={height} {...p} />;
};

/** Documentary overlay layer: the widget (lower corner, ~4 s) at each {at, corner} in props.cta. */
export const CTAOverlayLayer: React.FC<{cues: {at: number; corner?: 'left' | 'right'; like?: boolean}[]}> = ({cues}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const t = frame / fps;
  const live = cues.filter((c) => t >= c.at && t < c.at + CTA_SECONDS);
  if (!live.length) return null;
  const s = width / 1920, w = CTA_W * 0.75 * s, h = CTA_H * 0.75 * s;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {live.map((c, i) => (
        <svg key={i} width={w} height={h} viewBox={`0 0 ${CTA_W} ${CTA_H}`}
          style={{position: 'absolute', top: height - h - 40 * s, left: c.corner === 'right' ? width - w - 40 * s : 40 * s}}>
          <SubscribeWidget t={t - c.at} like={c.like !== false} />
        </svg>
      ))}
    </AbsoluteFill>
  );
};
