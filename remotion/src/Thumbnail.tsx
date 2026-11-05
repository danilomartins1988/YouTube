import React from 'react';
import {AbsoluteFill} from 'remotion';
import {makeCue, SceneCtx} from './lib/anim';
import {GeoCtx} from './lib/geo';
import type {Props, SceneSpec} from './lib/types';
import {Background} from './components/Chrome';
import {SCENES} from './Documentary';

/** YouTube thumbnail: one frozen frame of an animated scene + a big, legible headline. Rendered at
 * 1920x1080 and scaled to 1280x720 (`remotion still --scale=0.6667`). */
export type ThumbProps = Props & {
  thumb: {scene: SceneSpec; at: number; headline: string[]; kicker?: string; footer?: string; side?: 'left' | 'right'; accent_line?: number};
};

export const Thumbnail: React.FC<ThumbProps> = (props) => {
  const {thumb, palette: pal, fonts} = props;
  const W = 1920, H = 1080;
  const scene = thumb.scene;
  const Comp = SCENES[scene.type];
  const ctx = {t: thumb.at, frame: Math.round(thumb.at * 30), fps: 30, W, H, pal, font: fonts, scene, cue: makeCue(scene)};
  const left = (thumb.side || 'left') === 'left';
  const x = left ? 90 : W - 90;
  const anchor = left ? 'start' : 'end';
  const size = Math.min(230, 1500 / Math.max(...thumb.headline.map((l) => l.length)) * 1.45);
  return (
    <GeoCtx.Provider value={props.geo || {}}>
      <SceneCtx.Provider value={ctx}>
        <AbsoluteFill style={{backgroundColor: pal.bg}}>
          {scene.type !== 'oil_platform' && scene.type !== 'map' && <Background />}
          <AbsoluteFill><Comp /></AbsoluteFill>
          <AbsoluteFill>
            <svg width={W} height={H}>
              <defs>
                <linearGradient id="shade" x1={left ? '0' : '1'} y1="0" x2={left ? '1' : '0'} y2="0">
                  <stop offset="0%" stopColor={pal.bg} stopOpacity={0.92} />
                  <stop offset="55%" stopColor={pal.bg} stopOpacity={0.55} />
                  <stop offset="100%" stopColor={pal.bg} stopOpacity={0} />
                </linearGradient>
              </defs>
              <rect width={W} height={H} fill="url(#shade)" />
              {thumb.kicker && <text x={x} y={170} textAnchor={anchor} fill={pal.accent} fontFamily={fonts.body} fontWeight={700} fontSize={44} letterSpacing={8}>{thumb.kicker.toUpperCase()}</text>}
              {thumb.headline.map((ln, i) => (
                <text key={i} x={x} y={330 + i * size * 1.02 + size * 0.5} textAnchor={anchor} fontFamily={fonts.display} fontWeight={800} fontSize={size}
                  fill={i === (thumb.accent_line ?? -1) ? pal.accent : pal.ink} stroke={pal.bg} strokeWidth={6} paintOrder="stroke">{ln}</text>
              ))}
              {thumb.footer && <text x={x} y={H - 70} textAnchor={anchor} fill={pal.ink} opacity={0.85} fontFamily={fonts.body} fontWeight={600} fontSize={34} letterSpacing={3}>{thumb.footer.toUpperCase()}</text>}
            </svg>
          </AbsoluteFill>
        </AbsoluteFill>
      </SceneCtx.Provider>
    </GeoCtx.Provider>
  );
};
