import React from 'react';
import {Composition} from 'remotion';
import {Documentary} from './Documentary';
import {Thumbnail} from './Thumbnail';
import type {Props} from './lib/types';

const defaults: Props = {
  fps: 30, width: 1920, height: 1080, brand: 'The Hidden Economics',
  palette: {bg: '#07111F', bg2: '#0E1D33', ink: '#F4F1EA', muted: '#8B98AA', land: '#18283D', border: '#33475F', accent: '#D4AF5A', accent2: '#9FB7D0'},
  fonts: {display: 'Inter Display, Inter, sans-serif', body: 'Inter, sans-serif'},
  scenes: [{id: 'demo', type: 'act_title', params: {number: 'Part 1', title: 'Demo'}, narration: '', duration: 3, lead: 0.3, speech: 2, words: [], credits: [], chapter: ''}],
  geo: {},
};

export const RemotionRoot: React.FC = () => (
  <>
  <Composition
    id="Thumbnail"
    component={Thumbnail as unknown as React.FC<Record<string, unknown>>}
    defaultProps={{...defaults, thumb: {scene: defaults.scenes[0], at: 1, headline: ['DEMO']}} as unknown as Record<string, unknown>}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={1}
  />
  <Composition
    id="Documentary"
    component={Documentary as unknown as React.FC<Record<string, unknown>>}
    defaultProps={defaults as unknown as Record<string, unknown>}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={90}
    calculateMetadata={({props}) => {
      const p = props as unknown as Props;
      const frames = p.scenes.reduce((s, x) => s + (x.frames ?? Math.max(1, Math.round(x.duration * p.fps))), 0);
      return {durationInFrames: frames, fps: p.fps, width: p.width, height: p.height};
    }}
  />
  </>
);
