import {KineticShort} from './brand/KineticShort';
import {ChannelAvatar, ChannelBanner, ChannelWatermark} from './brand/ChannelArt';
import React from 'react';
import {Composition} from 'remotion';
import {Documentary} from './Documentary';
import {Thumbnail} from './Thumbnail';
import {ToneThumbnail} from './ToneThumbnail';
import {CinematicThumb} from './thumbnails/CinematicThumb';
import {PunchThumb} from './thumbnails/PunchThumb';
import {INTRO_SECONDS, TheHiddenEconomicsIntro} from './brand/TheHiddenEconomicsIntro';
import type {Props} from './lib/types';
import {DEMO_SECONDS, EngineDemo} from './animation-engine/examples/EngineDemo';
import {ChartsLinePreview, ChartsPreview, DrawPreview, ExplodedPreview, FlowPreview, MapPreview, PresenterPreview} from './animation-engine/examples/Previews';

const ENGINE_COMPS: {id: string; c: React.FC<any>; s: number}[] = [
  {id: 'EnginePresenter', c: PresenterPreview, s: 10}, {id: 'EngineDraw', c: DrawPreview, s: 8}, {id: 'EngineMap', c: MapPreview, s: 9},
  {id: 'EngineFlow', c: FlowPreview, s: 9}, {id: 'EngineCharts', c: ChartsPreview, s: 9}, {id: 'EngineChartsLine', c: ChartsLinePreview, s: 7},
  {id: 'EngineExploded', c: ExplodedPreview, s: 8}];

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
  <Composition id="ChannelAvatar" component={ChannelAvatar as unknown as React.FC<Record<string, unknown>>} defaultProps={{variant: 'mascot'}} fps={30} width={800} height={800} durationInFrames={1} />
  <Composition id="KineticShort" component={KineticShort as unknown as React.FC<Record<string, unknown>>} defaultProps={{words: [], beats: [], total: 5, endCard: 3, disclaimer: 'Conteúdo educativo.', asof: ''}} fps={30} width={1080} height={1920} durationInFrames={30 * 120} />
  <Composition id="ChannelWatermark" component={ChannelWatermark as unknown as React.FC<Record<string, unknown>>} defaultProps={{}} fps={30} width={300} height={300} durationInFrames={1} />
  <Composition id="ChannelBanner" component={ChannelBanner as unknown as React.FC<Record<string, unknown>>} defaultProps={{}} fps={30} width={2560} height={1440} durationInFrames={1} />
  <Composition
    id="PunchThumb"
    component={PunchThumb as unknown as React.FC<Record<string, unknown>>}
    defaultProps={{bg: ['#FFE14D', '#FF8A00'], hero: {kind: 'ram', x: 1100, y: 540, s: 1}, text: []} as unknown as Record<string, unknown>}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={1}
  />
  <Composition
    id="CinematicThumb"
    component={CinematicThumb as unknown as React.FC<Record<string, unknown>>}
    defaultProps={{palette: {sky0: '#05070B', sky1: '#141B26', haze: '#7FA6C9', key: '#9FC3E8', accent: '#D9A441', ink: '#F4EFE4'}, backdrop: 'room',
      subject: {kind: 'vault', x: 1250, y: 520, s: 1}, text: []} as unknown as Record<string, unknown>}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={1}
  />
  <Composition
    id="ToneThumbnail"
    component={ToneThumbnail as unknown as React.FC<Record<string, unknown>>}
    defaultProps={{tone: 'bright', scene: {world: 'hills'}, headline: ['DEMO']} as unknown as Record<string, unknown>}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={1}
  />
  <Composition
    id="Intro"
    component={TheHiddenEconomicsIntro}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={INTRO_SECONDS * 30}
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
  {/* animation engine: 30 s demo + one preview per component (geo passed via --props) */}
  <Composition id="EngineDemo" component={EngineDemo as unknown as React.FC<Record<string, unknown>>} defaultProps={{geo: {paths: {}}}}
    fps={30} width={1920} height={1080} durationInFrames={DEMO_SECONDS * 30} />
  {ENGINE_COMPS.map((e) => <Composition key={e.id} id={e.id} component={e.c as unknown as React.FC<Record<string, unknown>>}
    defaultProps={{geo: {paths: {}}}} fps={30} width={1920} height={1080} durationInFrames={e.s * 30} />)}
  </>
);
