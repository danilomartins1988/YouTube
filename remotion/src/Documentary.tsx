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
import {Circuit, RaceTrack} from './scenes/RaceScenes';
import {Whiteboard} from './scenes/Whiteboard';
import {AINetwork, CpuGpu, Landscape, Stack, StackedColumns, SupplyChain} from './scenes/TechScenes';

export const SCENES: Record<string, React.FC> = {
  act_title: ActTitle, kinetic_text: KineticText, big_counter: BigCounter, line_chart: LineChart, bar_chart: BarChart,
  donut: Donut, timeline: Timeline, compare: Compare, people_ratio: PeopleRatio, end_card: EndCard,
  oil_platform: OilPlatform, map: MapScene, fund_flow: FundFlow, isometric: Isometric,
  race_track: RaceTrack, circuit: Circuit, whiteboard: Whiteboard,
  ai_network: AINetwork, cpu_gpu: CpuGpu, stack: Stack, supply_chain: SupplyChain, stacked_columns: StackedColumns, landscape: Landscape,
};
// Scene types that paint their own full-frame background.
const OWN_BG = new Set(['oil_platform', 'map', 'race_track', 'whiteboard', 'supply_chain']);

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
        {!OWN_BG.has(scene.type) && <Background style={props.background} />}
        <AbsoluteFill style={{opacity: a, transform: `translateX(${push}px)`}}>
          <Comp />
        </AbsoluteFill>
        <AbsoluteFill style={{opacity: a}}>
          <Chrome />
        </AbsoluteFill>
        <Finish />
        {props.transition === 'race' && <RaceWipe t={t} dur={scene.duration} pal={props.palette} W={width} H={height} />}
        {props.transition === 'scan' && <ScanWipe t={t} dur={scene.duration} pal={props.palette} W={width} H={height} />}
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

/** Racing transition: three diagonal colour bands sweep across, covering the cut between scenes. */
const RaceWipe: React.FC<{t: number; dur: number; pal: Props['palette']; W: number; H: number}> = ({t, dur, pal, W, H}) => {
  const cols = [pal.accent, pal.accent2, pal.accent3 || '#FFD21F'];
  const band = (u: number, i: number) => {
    const x = lerpN(-W * 0.9, W * 1.3, u) - i * 140;
    return <polygon key={i} points={`${x},0 ${x + 260},0 ${x + 260 - 420},${H} ${x - 420},${H}`} fill={cols[i]} />;
  };
  const inU = t / 0.45, outU = (t - (dur - 0.45)) / 0.45;
  const els: React.ReactNode[] = [];
  if (inU >= 0 && inU < 1) [0, 1, 2].forEach((i) => els.push(band(0.5 + inU * 0.5, i)));      // bands leave on entry
  if (outU >= 0 && outU < 1) [0, 1, 2].forEach((i) => els.push(band(outU * 0.5, i)));          // bands arrive on exit
  return els.length ? <AbsoluteFill><svg width={W} height={H}>{els}</svg></AbsoluteFill> : null;
};
const lerpN = (a: number, b: number, u: number) => a + (b - a) * u;

/** Tech transition: a thin bright scan line with a soft glow sweeps across the cut (in on entry, out on exit). */
const ScanWipe: React.FC<{t: number; dur: number; pal: Props['palette']; W: number; H: number}> = ({t, dur, pal, W, H}) => {
  const inU = t / 0.5, outU = (t - (dur - 0.5)) / 0.5;
  const at = inU >= 0 && inU < 1 ? 0.5 + inU * 0.5 : outU >= 0 && outU < 1 ? outU * 0.5 : -1;
  if (at < 0) return null;
  const x = lerpN(-200, W + 200, at);
  const col = pal.accent2 || pal.accent;
  return (
    <AbsoluteFill>
      <svg width={W} height={H}>
        <defs><linearGradient id="scanG" x1="0" x2="1"><stop offset="0%" stopColor={col} stopOpacity={0} /><stop offset="100%" stopColor={col} stopOpacity={0.35} /></linearGradient></defs>
        <rect x={x - 260} y={0} width={260} height={H} fill="url(#scanG)" />
        <rect x={x - 3} y={0} width={6} height={H} fill="#FFFFFF" opacity={0.9} />
      </svg>
    </AbsoluteFill>
  );
};
