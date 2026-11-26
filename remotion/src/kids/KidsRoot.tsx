import React from 'react';
import {Composition} from 'remotion';
import {KidsSong} from './KidsSong';
import {KidsThumb} from './KidsThumb';
import type {Timeline} from './theme';

/* Separate Remotion entry for the kids-channel test (does not touch the documentary Root).
 * Render: npx remotion render src/kids/index.ts KidsSong out.mp4 --props=timeline_props.json */
const EMPTY: Timeline = {title: 'Vamos Contar os Bichinhos!', bpm: 112, beat: 60 / 112, bar: 240 / 112, duration: 10, voice: '',
  sections: [{name: 'intro', kind: 'intro', start: 0, end: 10}], lines: []};
const FPS = 30;

export const KidsRoot: React.FC = () => (
  <>
    <Composition id="KidsSong" component={KidsSong as unknown as React.FC<Record<string, unknown>>} fps={FPS} width={1920} height={1080}
      durationInFrames={300} defaultProps={{timeline: EMPTY, offset: 0}}
      calculateMetadata={({props}) => {
        const p = props as unknown as {timeline: Timeline; offset?: number; seconds?: number};
        const secs = p.seconds ?? p.timeline.duration - (p.offset ?? 0);
        return {durationInFrames: Math.max(1, Math.round(secs * FPS))};
      }} />
    <Composition id="KidsShort" component={KidsSong as unknown as React.FC<Record<string, unknown>>} fps={FPS} width={1080} height={1920}
      durationInFrames={300} defaultProps={{timeline: EMPTY, offset: 0}}
      calculateMetadata={({props}) => {
        const p = props as unknown as {timeline: Timeline; offset?: number; seconds?: number};
        const secs = p.seconds ?? p.timeline.duration - (p.offset ?? 0);
        return {durationInFrames: Math.max(1, Math.round(secs * FPS))};
      }} />
    <Composition id="KidsThumb" component={KidsThumb} fps={FPS} width={1280} height={720} durationInFrames={1} />
  </>
);
