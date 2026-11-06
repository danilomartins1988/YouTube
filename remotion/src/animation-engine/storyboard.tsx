import React, {useMemo} from 'react';
import {useCtx} from '../lib/anim';
import {useGeo} from '../lib/geo';
import {Chrome} from './storyboardChrome';
import {AnimatedPresenter, PresenterAction} from './AnimatedPresenter/AnimatedPresenter';
import {BarChart, Donut, LineChart} from './AnimatedCharts/AnimatedCharts';
import {AnimatedWorldMap} from './AnimatedWorldMap/AnimatedWorldMap';
import {DrawOnCanvas, DrawStroke, buildDrawTimeline} from './DrawOnCanvas/DrawOnCanvas';
import {EconomicFlow} from './EconomicFlow/EconomicFlow';
import {ExplodedDiagram} from './ExplodedDiagram/ExplodedDiagram';
import {DigitalBoard, Studio} from './transitions';
import {CartoonOcean} from './CartoonOcean/CartoonOcean';
import {fromEpisodePalette} from './motion';

/**
 * Storyboard adapters: lets hiddeneco storyboards (YAML) use the engine directly, timed to the narration.
 *
 *   type: engine_draw | engine_flow | engine_map | engine_chart | engine_exploded
 *
 * Every time value in `params` may be a number (seconds from scene start) OR a narration cue:
 *   {cue: "the phrase", offset: 0.3}
 * Cues are resolved recursively before the component sees its props, so any engine prop can follow the voice.
 */
const isCue = (v: any) => v && typeof v === 'object' && !Array.isArray(v) && typeof v.cue === 'string' && Object.keys(v).every((k) => k === 'cue' || k === 'offset');
const resolve = (v: any, cue: (s: any, f?: number) => number): any => {
  if (isCue(v)) return cue(v, 0);
  if (Array.isArray(v)) return v.map((x) => resolve(x, cue));
  if (v && typeof v === 'object') return Object.fromEntries(Object.entries(v).map(([k, x]) => [k, resolve(x, cue)]));
  return v;
};
const useParams = () => {
  const ctx = useCtx();
  const p = useMemo(() => ({palette: fromEpisodePalette(ctx.pal as any), ...resolve(ctx.scene.params, ctx.cue)}), [ctx.scene]);
  return {ctx, p};
};

/** engine_draw: optional studio + board; the presenter (or a pen) draws `strokes`, then follows `actions`. */
export const EngineDrawScene: React.FC = () => {
  const {ctx, p} = useParams();
  const strokes: DrawStroke[] = p.strokes || [];
  const tl = useMemo(() => buildDrawTimeline(strokes, {start: p.draw_start ?? 1.2, speed: p.speed, pause: p.pause}), [p]);
  const actions: PresenterAction[] = [
    ...(p.enter !== false ? [{kind: 'enter', from: p.enter?.from ?? -260, to: p.enter?.to ?? 520, at: p.enter?.at ?? 0.2, dur: p.enter?.dur ?? 1.4} as PresenterAction] : []),
    {kind: 'draw', timeline: tl},
    ...((p.actions || []) as PresenterAction[]),
  ];
  return (
    <svg width={ctx.W} height={ctx.H}>
      {p.studio !== false && <Studio t={ctx.t} floorY={p.floor ?? 960} palette={p.palette} />}
      {p.board && <DigitalBoard t={ctx.t} at={p.board.at ?? 0.3} x={p.board.x} y={p.board.y} w={p.board.w} h={p.board.h} palette={p.palette} />}
      {/* optional slow camera push (scale per second) so long pen drawings never sit still */}
      <g transform={p.push ? `translate(${ctx.W / 2} ${ctx.H / 2}) scale(${1 + p.push * ctx.t}) translate(${-ctx.W / 2} ${-ctx.H / 2})` : undefined}>
        <DrawOnCanvas t={ctx.t} timeline={tl} showPen={p.presenter === false} palette={p.palette} />
      </g>
      {p.presenter !== false && <AnimatedPresenter t={ctx.t} actions={actions} floor={p.floor ?? 960} scale={p.scale ?? 0.9}
        startX={p.enter?.from ?? -260} talk={[[ctx.scene.lead, ctx.scene.lead + ctx.scene.speech]]} />}
      <Chrome title={p.title} subtitle={p.subtitle} t={ctx.t} />
    </svg>
  );
};

export const EngineFlowScene: React.FC = () => {
  const {ctx, p} = useParams();
  return <svg width={ctx.W} height={ctx.H}><EconomicFlow t={ctx.t} {...p} /><Chrome title={p.title} subtitle={p.subtitle} t={ctx.t} /></svg>;
};

export const EngineMapScene: React.FC = () => {
  const {ctx, p} = useParams();
  const geo = useGeo(p.geo || 'world');
  return <div style={{position: 'absolute', inset: 0}}>
    <AnimatedWorldMap t={ctx.t} geo={geo} {...p} />
    <svg width={ctx.W} height={ctx.H} style={{position: 'absolute', inset: 0}}><Chrome title={p.title} subtitle={p.subtitle} t={ctx.t} /></svg>
  </div>;
};

export const EngineChartScene: React.FC = () => {
  const {ctx, p} = useParams();
  const C = p.chart === 'line' ? LineChart : p.chart === 'donut' ? Donut : BarChart;
  return <svg width={ctx.W} height={ctx.H}><C t={ctx.t} {...(p as any)} />{p.chart === 'donut' && <Chrome title={p.title} subtitle={p.subtitle} t={ctx.t} />}</svg>;
};

export const EngineExplodedScene: React.FC = () => {
  const {ctx, p} = useParams();
  return <svg width={ctx.W} height={ctx.H}><ExplodedDiagram t={ctx.t} {...(p as any)} /><Chrome title={p.title} subtitle={p.subtitle} t={ctx.t} /></svg>;
};

/** engine_cartoon: cartoon ocean world (ships, anchors, cables with light, volcano, callouts), camera tracking. */
export const EngineCartoonScene: React.FC = () => {
  const {ctx, p} = useParams();
  return <CartoonOcean t={ctx.t} W={ctx.W} H={ctx.H} {...(p as any)} />;
};

export const ENGINE_SCENES: Record<string, React.FC> = {
  engine_draw: EngineDrawScene, engine_flow: EngineFlowScene, engine_map: EngineMapScene,
  engine_chart: EngineChartScene, engine_exploded: EngineExplodedScene, engine_cartoon: EngineCartoonScene,
};
