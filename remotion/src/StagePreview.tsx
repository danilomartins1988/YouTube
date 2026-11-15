import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {CartoonStage} from './animation-engine/CartoonStage/CartoonStage';

/** Dev preview of one CartoonStage world over time (stills and short motion tests of new sets/items before a full build).
 * Props: {scene: CartoonStage params, start?: seconds offset}. Used by tools/stage_preview.py. */
export const StagePreview: React.FC<{scene: Record<string, any>; start?: number; times?: number[]}> = ({scene, start = 0, times}) => {
  const frame = useCurrentFrame(), {fps} = useVideoConfig();
  const t = times?.length ? times[Math.min(frame, times.length - 1)] : start + frame / fps;
  return <AbsoluteFill style={{backgroundColor: '#000'}}><CartoonStage t={t} W={1920} H={1080} {...(scene as any)} /></AbsoluteFill>;
};
