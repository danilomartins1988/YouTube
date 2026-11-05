import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig} from 'remotion';
import {eio, makeCue, SceneCtx} from './lib/anim';
import {GeoCtx} from './lib/geo';
import type {Props, SceneSpec} from './lib/types';
import {Background, Chrome, Finish} from './components/Chrome';
import {ActTitle, BarChart, BigCounter, Compare, Donut, EndCard, KineticText, LineChart, PeopleRatio, Timeline} from './scenes/DataScenes';
import {OilPlatform} from './scenes/Platform';
import {MapScene} from './scenes/MapScene';
import {FundFlow} from './scenes/FundFlow';
import {Isometric} from './scenes/Isometric';

export const SCENES: Record<string, React.FC> = {
  act_title: ActTitle, kinetic_text: KineticText, big_counter: BigCounter, line_chart: LineChart, bar_chart: BarChart,
  donut: Donut, timeline: Timeline, compare: Compare, people_ratio: PeopleRatio, end_card: EndCard,
  oil_platform: OilPlatform, map: MapScene, fund_flow: FundFlow, isometric: Isometric,
};
// Scene types that paint their own full-frame background.
const OWN_BG = new Set(['oil_platform', 'map']);

const SceneView: React.FC<{scene: SceneSpec; props: Props}> = ({scene, props}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const t = scene.preview_t ?? frame / fps; // preview_t: render one representative frame (layout checks)
  const Comp = SCENES[scene.type];
  if (!Comp) throw new Error(`Unknown scene type ${scene.type}`);
  const ctx = {t, frame, fps, W: width, H: height, pal: props.palette, font: props.fonts, scene, cue: makeCue(scene)};
  // transitions: soft fade + slight push at both ends of every scene
  const fin = eio(t, 0, 0.45), fout = eio(scene.duration - t, 0, 0.4);
  const a = Math.min(fin, fout);
  const push = (1 - fin) * 30 - (1 - fout) * 30;
  return (
    <SceneCtx.Provider value={ctx}>
      <AbsoluteFill style={{backgroundColor: props.palette.bg}}>
        {!OWN_BG.has(scene.type) && <Background />}
        <AbsoluteFill style={{opacity: a, transform: `translateX(${push}px)`}}>
          <Comp />
        </AbsoluteFill>
        <AbsoluteFill style={{opacity: a}}>
          <Chrome />
        </AbsoluteFill>
        <Finish />
      </AbsoluteFill>
    </SceneCtx.Provider>
  );
};

export const Documentary: React.FC<Props> = (props) => {
  let from = 0;
  return (
    <GeoCtx.Provider value={props.geo || {}}>
      <AbsoluteFill style={{backgroundColor: props.palette.bg}}>
        {props.scenes.map((s) => {
          const dur = s.frames ?? Math.max(1, Math.round(s.duration * props.fps));
          const el = (
            <Sequence key={s.id} from={from} durationInFrames={dur} name={s.id}>
              <SceneView scene={s} props={props} />
            </Sequence>
          );
          from += dur;
          return el;
        })}
      </AbsoluteFill>
    </GeoCtx.Provider>
  );
};
