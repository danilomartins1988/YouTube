import React, {useMemo} from 'react';
import {clamp, easeBack, easeInOut, eio, eo, lerp, prog, rand, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';
import {useGeo} from '../lib/geo';
import {merc, parseLayer, screenPath, mixHex2} from './MapScene';

/*
 * Technology-economics scene library (first used in Episode 06, Nvidia). All original SVG:
 *   ai_network      - opening: an ecosystem graph assembles, then the shared supplier at its centre is revealed
 *   cpu_gpu         - CPU vs GPU: a workload of tasks is distributed to few big cores vs many small cores,
 *                     then a step-by-step (serial) chain shows the opposite trade-off
 *   stack           - layered software ecosystem built bottom-up; then the cost of switching is animated
 *   supply_chain    - map + process chain: stages light up in order, packets flow, a bottleneck chokes downstream
 *   stacked_columns - revenue by business, columns grow chronologically, then morph into a 100% mix view
 *   landscape       - competitive matrix: a cursor "selects" each dimension, cells type in; a conceptual
 *                     flexibility-vs-specialisation axis places each option (no benchmarks)
 */

const C = (pal: Record<string, string>, k?: string, fb = 'accent') => (k ? pal[k] || k : pal[fb]);
const typed = (s: string, u: number) => s.slice(0, Math.round(s.length * clamp(u)));

// ------------------------------------------------------------------ ai_network
export const AINetwork: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const groups: any[] = p.groups || [];
  const cx = W * 0.5, cy = H * 0.53;
  const zoom = lerp(1.18, 1.0, eio(t, 0, Math.max(4, scene.duration * 0.7)));
  const hubAt = cue(p.hub_cue, 0.6);
  const hubU = easeBack(prog(t, hubAt, 0.8));
  const nodes: {x: number; y: number; label: string; at: number; col: string; g: number}[] = [];
  groups.forEach((g, gi) => {
    const a0 = (gi / groups.length) * Math.PI * 2 - Math.PI / 2;
    (g.nodes || []).forEach((n: string, ni: number) => {
      const spread = 0.55;
      const a = a0 + (ni - ((g.nodes.length - 1) / 2)) * (spread / Math.max(1, g.nodes.length - 1)) * 1.6;
      const r = 300 + (ni % 2) * 90;
      nodes.push({x: cx + Math.cos(a) * r * 1.55, y: cy + Math.sin(a) * r * 0.8, label: n, at: cue(g, 0.05 + gi * 0.08) + ni * 0.18,
        col: C(pal, g.colour, 'accent2'), g: gi});
    });
  });
  return (
    <svg width={W} height={H}>
      <g transform={`translate(${cx} ${cy}) scale(${zoom}) translate(${-cx} ${-cy})`}>
        {/* faint orbit rings */}
        {[300, 390, 480].map((r, i) => <ellipse key={i} cx={cx} cy={cy} rx={r * 1.55} ry={r * 0.8} fill="none" stroke={pal.border} strokeOpacity={0.35}
          strokeDasharray="4 10" strokeDashoffset={t * (8 + i * 4)} />)}
        {/* links node <-> hub with packets */}
        {nodes.map((n, i) => {
          const u = eo(t, n.at + 0.3, 0.9);
          if (u <= 0) return null;
          const hx = lerp(n.x, cx, u), hy = lerp(n.y, cy, u);
          const lit = hubU > 0.2;
          return (
            <g key={'l' + i}>
              <line x1={n.x} y1={n.y} x2={hx} y2={hy} stroke={lit ? pal.accent : n.col} strokeOpacity={lit ? 0.55 : 0.35} strokeWidth={2} />
              {u >= 1 && Array.from({length: 2}, (_, k) => {
                const q = ((t * 0.45 + k / 2 + rand(i) ) % 1);
                const inward = !lit;
                const f = inward ? q : 1 - q;
                return <circle key={k} cx={lerp(n.x, cx, f)} cy={lerp(n.y, cy, f)} r={4} fill={lit ? pal.accent : n.col} opacity={0.9} />;
              })}
            </g>
          );
        })}
        {/* nodes */}
        {nodes.map((n, i) => {
          const u = easeBack(prog(t, n.at, 0.6));
          if (u <= 0) return null;
          return (
            <g key={'n' + i} transform={`translate(${n.x} ${n.y + Math.sin(t * 1.3 + i) * 4}) scale(${u})`}>
              <circle r={30} fill={pal.bg2} stroke={n.col} strokeWidth={3} />
              <circle r={10} fill={n.col} opacity={0.8 + 0.2 * Math.sin(t * 3 + i)} />
              <text y={58} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={22}>{n.label}</text>
            </g>
          );
        })}
        {/* group labels */}
        {groups.map((g, gi) => {
          const a0 = (gi / groups.length) * Math.PI * 2 - Math.PI / 2;
          const at = cue(g, 0.05 + gi * 0.08);
          return <text key={'g' + gi} x={cx + Math.cos(a0) * 560 * 1.4} y={cy + Math.sin(a0) * 400 + 8} textAnchor="middle" fill={C(pal, g.colour, 'accent2')}
            fontFamily={font.body} fontWeight={700} fontSize={22} letterSpacing={4} opacity={eo(t, at, 0.6) * 0.95}>{String(g.label).toUpperCase()}</text>;
        })}
        {/* hub: a question mark until revealed */}
        <g transform={`translate(${cx} ${cy})`}>
          <circle r={70 + 8 * Math.sin(t * 2)} fill="none" stroke={hubU > 0 ? pal.accent : pal.border} strokeOpacity={0.6} strokeWidth={2} />
          <rect x={-62} y={-62} width={124} height={124} rx={14} fill={pal.bg2} stroke={hubU > 0 ? pal.accent : pal.muted} strokeWidth={4} />
          {Array.from({length: 8}, (_, i) => (
            <g key={i}>
              <rect x={-52 + i * 14} y={-78} width={6} height={14} fill={hubU > 0 ? pal.accent : pal.muted} />
              <rect x={-52 + i * 14} y={64} width={6} height={14} fill={hubU > 0 ? pal.accent : pal.muted} />
              <rect x={-78} y={-52 + i * 14} width={14} height={6} fill={hubU > 0 ? pal.accent : pal.muted} />
              <rect x={64} y={-52 + i * 14} width={14} height={6} fill={hubU > 0 ? pal.accent : pal.muted} />
            </g>
          ))}
          {hubU <= 0 ? <text y={26} textAnchor="middle" fill={pal.muted} fontFamily={font.display} fontWeight={800} fontSize={72}>?</text>
            : <g transform={`scale(${hubU})`}>
              <circle r={190} fill={pal.accent} opacity={0.08 * (1 + Math.sin(t * 3))} />
              <text y={14} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={800} fontSize={34}>{p.hub || 'NVIDIA'}</text>
            </g>}
        </g>
      </g>
      {p.kicker && <RiseText x={120} y={150} at={cue(p.kicker_cue, 0)} size={26} color={pal.accent3} weight={700} tracking={6}>{String(p.kicker).toUpperCase()}</RiseText>}
      {p.hub_label && <RiseText x={W / 2} y={H - 46} anchor="middle" at={hubAt + 0.5} size={46} weight={800} display>{p.hub_label}</RiseText>}
      {p.question && <RiseText x={W / 2} y={H - 60} anchor="middle" at={cue(p.question_cue, 0.85)} size={34} color={pal.accent3}>{p.question}</RiseText>}
    </svg>
  );
};

// ------------------------------------------------------------------ cpu_gpu
export const CpuGpu: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const N = p.tasks || 192;
  const cpuCores = p.cpu_cores || 8, gpuCols = 16, gpuRows = Math.ceil(N / 16);
  const run = cue(p.run_cue, 0.3);
  const gRun = p.gpu_run_cue ? cue(p.gpu_run_cue, 0.4) : run;
  const cycC = p.cpu_cycle || 0.42, cycG = p.gpu_cycle || 1.1;
  const L = {x: 120, y: 300, w: 760, h: 520}, R = {x: 1040, y: 300, w: 760, h: 520};
  const panelU = (side: number) => eo(t, cue(side ? p.gpu_cue : p.cpu_cue, side ? 0.12 : 0.02), 0.8);
  const queue = {x: W / 2, y: 210};
  const cpuCore = (k: number): [number, number] => [L.x + 120 + (k % 4) * 175, L.y + 150 + Math.floor(k / 4) * 190];
  const gpuCore = (k: number): [number, number] => [R.x + 55 + (k % gpuCols) * 43.5, R.y + 90 + Math.floor(k / gpuCols) * 34];
  let cpuDone = 0, gpuDone = 0;
  const taskEls: React.ReactNode[] = [];
  for (let i = 0; i < N; i++) {
    // CPU: 8 powerful cores take tasks in rounds; GPU: every small core takes one task at once (slower each)
    const cs = run + Math.floor(i / cpuCores) * cycC, ce = cs + cycC * 0.9;
    const gs = gRun + 0.5, ge = gs + cycG;
    if (t >= ce) cpuDone++;
    if (t >= ge) gpuDone++;
    const q0: [number, number] = [queue.x + ((i % 24) - 12) * 12, queue.y + Math.floor(i / 24) * 10];
    const draw = (start: number, end: number, core: [number, number], out: [number, number], col: string, key: string, sz: number) => {
      let x: number, y: number, o = 1;
      if (t < start - 0.35) { [x, y] = q0; o = t < run - 0.6 ? eo(t, run - 1.6 + i * 0.004, 0.4) : 1; }
      else if (t < start) { const u = easeInOut(prog(t, start - 0.35, 0.35)); x = lerp(q0[0], core[0], u); y = lerp(q0[1], core[1], u); }
      else if (t < end) { [x, y] = core; }
      else { const u = easeInOut(prog(t, end, 0.5)); x = lerp(core[0], out[0], u); y = lerp(core[1], out[1], u); o = 1 - 0.6 * u; }
      taskEls.push(<rect key={key} x={x - sz / 2} y={y - sz / 2} width={sz} height={sz} rx={2} fill={col} opacity={o} />);
    };
    if (panelU(0) > 0.5) draw(cs, ce, cpuCore(i % cpuCores), [L.x + 60 + (cpuDone % 40) * 16, L.y + L.h + 40], pal.accent2, 'c' + i, 9);
    if (panelU(1) > 0.5) draw(gs, ge, gpuCore(i), [R.x + 60 + (i % 40) * 16, R.y + R.h + 40], pal.accent, 'g' + i, 8);
  }
  const busyC = (k: number) => { for (let i = k; i < N; i += cpuCores) { const s = run + Math.floor(i / cpuCores) * cycC; if (t >= s && t < s + cycC * 0.9) return 1; } return 0; };
  const busyG = t >= gRun + 0.5 && t < gRun + 0.5 + cycG;
  // serial phase: a chain of dependent steps (each must wait for the previous one)
  const serAt = cue(p.serial_cue, 0.8);
  const serU = eo(t, serAt, 0.5);
  const steps = 6;
  const chain = (x0: number, stepT: number, col: string) => Array.from({length: steps}, (_, j) => {
    const on = t >= serAt + 0.6 + j * stepT;
    return (
      <g key={j}>
        {j > 0 && <line x1={x0 + j * 110 - 50} y1={0} x2={x0 + j * 110 - 20} y2={0} stroke={pal.muted} strokeWidth={3} />}
        <rect x={x0 + j * 110 - 20} y={-22} width={70} height={44} rx={8} fill={on ? col : pal.bg2} stroke={col} strokeWidth={2} />
      </g>
    );
  });
  const panel = (b: typeof L, side: number) => {
    const u = panelU(side);
    return (
      <g opacity={u} transform={`translate(0 ${30 * (1 - u)})`}>
        <rect x={b.x} y={b.y} width={b.w} height={b.h} rx={22} fill={pal.bg2} stroke={side ? pal.accent : pal.accent2} strokeWidth={3} />
        <text x={b.x + 30} y={b.y - 22} fill={side ? pal.accent : pal.accent2} fontFamily={font.display} fontWeight={800} fontSize={44}>{side ? 'GPU' : 'CPU'}</text>
        <text x={b.x + 150} y={b.y - 26} fill={pal.muted} fontFamily={font.body} fontSize={26}>{side ? (p.gpu_label || 'many simpler cores') : (p.cpu_label || 'a few powerful cores')}</text>
        {side === 0 && Array.from({length: cpuCores}, (_, k) => {
          const [x, y] = cpuCore(k);
          const b2 = busyC(k);
          return <rect key={k} x={x - 70} y={y - 70} width={140} height={140} rx={14} fill={b2 ? pal.accent2 : pal.bg} fillOpacity={b2 ? 0.35 : 1}
            stroke={pal.accent2} strokeWidth={b2 ? 4 : 2} />;
        })}
        {side === 1 && Array.from({length: gpuCols * gpuRows}, (_, k) => {
          const [x, y] = gpuCore(k);
          return <rect key={k} x={x - 17} y={y - 13} width={34} height={26} rx={4} fill={busyG ? pal.accent : pal.bg} fillOpacity={busyG ? 0.45 : 1}
            stroke={pal.accent} strokeOpacity={0.7} strokeWidth={1.5} />;
        })}
        <text x={b.x + b.w - 24} y={b.y + b.h - 22} textAnchor="end" fill={pal.ink} fontFamily={font.display} fontWeight={800} fontSize={40}>
          {`${side ? gpuDone : cpuDone} / ${N}`}</text>
        <text x={b.x + 24} y={b.y + b.h - 26} fill={pal.muted} fontFamily={font.body} fontSize={22} letterSpacing={2}>TASKS FINISHED</text>
      </g>
    );
  };
  return (
    <svg width={W} height={H}>
      {p.title && <RiseText x={W / 2} y={120} anchor="middle" at={cue(p.title_cue, 0)} size={54} weight={800} display>{p.title}</RiseText>}
      <text x={queue.x} y={queue.y - 30} textAnchor="middle" fill={pal.accent3} fontFamily={font.body} fontWeight={700} fontSize={24} letterSpacing={4}
        opacity={eo(t, run - 1.6, 0.5) * (t < run + 1 ? 1 : 0.5)}>{p.workload_label || 'A PARALLEL WORKLOAD'}</text>
      {panel(L, 0)}
      {panel(R, 1)}
      {taskEls}
      {serU > 0 && (
        <g opacity={serU}>
          <rect x={0} y={H - 230} width={W} height={150} fill={pal.bg} opacity={0.92} />
          <text x={W / 2} y={H - 190} textAnchor="middle" fill={pal.accent3} fontFamily={font.body} fontWeight={700} fontSize={24} letterSpacing={4}>
            {p.serial_label || 'A STEP-BY-STEP JOB: EACH STEP WAITS FOR THE LAST'}</text>
          <g transform={`translate(0 ${H - 128})`}>{chain(L.x + 80, p.serial_cpu_step || 0.5, pal.accent2)}{chain(R.x + 80, p.serial_gpu_step || 1.3, pal.accent)}</g>
        </g>
      )}
      <text x={W / 2} y={H - 34} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontSize={22} opacity={eo(t, cue(p.note_cue, 0.5), 0.6)}>
        {p.note || 'Illustration, not a benchmark: real performance depends on the workload and the chip.'}</text>
    </svg>
  );
};

// ------------------------------------------------------------------ stack
export const Stack: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const layers: any[] = p.layers || [];
  const x0 = 140, w = 980, lh = p.layer_h || 96, gap = p.layer_gap ?? 14, base = H - (p.base_pad || 150);
  const swAt = cue(p.switch_cue, 0.75);
  const swU = p.switch_cue ? eo(t, swAt, 0.9) : 0;
  const costs: any[] = p.costs || [];
  return (
    <svg width={W} height={H}>
      {p.title && <RiseText x={x0} y={150} at={cue(p.title_cue, 0)} size={52} weight={800} display>{p.title}</RiseText>}
      {layers.map((l, i) => {
        const at = cue(l, 0.05 + i * 0.1);
        const u = easeBack(prog(t, at, 0.7));
        if (u <= 0) return null;
        const y = base - (i + 1) * (lh + gap);
        const col = C(pal, l.colour, i === 0 ? 'accent' : 'accent2');
        const lit = (t - at) < 1.6 ? 1 - (t - at) / 1.6 : 0;
        const items: string[] = l.items || [];
        return (
          <g key={i} transform={`translate(${(1 - u) * -60} ${(1 - u) * 80})`} opacity={clamp(u)}>
            <rect x={x0} y={y} width={w} height={lh} rx={14} fill={pal.bg2} stroke={col} strokeWidth={3} />
            <rect x={x0} y={y} width={w} height={lh} rx={14} fill={col} opacity={0.12 + 0.25 * lit} />
            <rect x={x0} y={y} width={12} height={lh} rx={4} fill={col} />
            <text x={x0 + 34} y={y + 44} fill={pal.ink} fontFamily={font.display} fontWeight={800} fontSize={34}>{l.label}</text>
            {l.sub && <text x={x0 + 34} y={y + 78} fill={pal.muted} fontFamily={font.body} fontSize={22}>{l.sub}</text>}
            {items.map((it, k) => {
              const iu = easeBack(prog(t, at + 0.35 + k * 0.18, 0.5));
              const ix = x0 + w - 20 - (items.length - k) * 214;
              return <g key={k} transform={`translate(${ix + 104} ${y + lh / 2}) scale(${clamp(iu, 0, 1.2)})`}>
                <rect x={-102} y={-22} width={204} height={44} rx={22} fill={col} opacity={0.2} stroke={col} strokeWidth={1.5} />
                <text y={8} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={20}>{it}</text>
              </g>;
            })}
            {/* data pulses travelling up the stack */}
            {i > 0 && t > at + 0.8 && Array.from({length: 3}, (_, k) => {
              const q = (t * 0.7 + k / 3 + i * 0.17) % 1;
              return <rect key={k} x={x0 + 120 + k * 300 + (i * 57) % 200} y={y + lh + gap - q * (lh + gap)} width={6} height={12} rx={3} fill={pal.accent} opacity={0.7 * (1 - q)} />;
            })}
          </g>
        );
      })}
      {/* side counter (e.g. developers) */}
      {p.counter && (() => {
        const at = cue(p.counter_cue, 0.5);
        const u = eo(t, at, 1.2);
        if (u <= 0) return null;
        return (
          <g opacity={clamp(u * 2)}>
            <text x={1260} y={380} fill={pal.muted} fontFamily={font.body} fontWeight={700} fontSize={24} letterSpacing={4}>{String(p.counter_label || '').toUpperCase()}</text>
            <text x={1260} y={480} fill={pal.accent} fontFamily={font.display} fontWeight={800} fontSize={104}>{p.counter}</text>
            {p.counter_sub && <text x={1262} y={530} fill={pal.muted} fontFamily={font.body} fontSize={24}>{p.counter_sub}</text>}
            {Array.from({length: 36}, (_, k) => {
              const ku = eo(t, at + k * 0.04, 0.4);
              return <circle key={k} cx={1275 + (k % 12) * 44} cy={590 + Math.floor(k / 12) * 44} r={13 * ku} fill={pal.accent2} opacity={0.75} />;
            })}
          </g>
        );
      })()}
      {/* switching cost phase */}
      {swU > 0 && (
        <g>
          <rect x={1220} y={250} width={600} height={720} rx={20} fill={pal.bg} opacity={0.96 * swU} stroke={pal.risk || '#FF5A5F'} strokeWidth={3} />
          <text x={1250} y={310} fill={pal.risk || '#FF5A5F'} fontFamily={font.body} fontWeight={700} fontSize={24} letterSpacing={4} opacity={swU}>
            {String(p.switch_label || 'THE COST OF SWITCHING').toUpperCase()}</text>
          {/* the app tries to move: dashed arrow from top layer to a rival block */}
          <rect x={1250} y={340} width={540} height={96} rx={14} fill={pal.bg2} stroke={pal.accent2} strokeDasharray="10 8" strokeWidth={3} opacity={swU} />
          <text x={1520} y={398} textAnchor="middle" fill={pal.accent2} fontFamily={font.display} fontWeight={800} fontSize={30} opacity={swU}>{p.rival || 'Alternative hardware + software'}</text>
          <path d={`M ${x0 + w} ${base - layers.length * (lh + gap) + lh / 2} C ${x0 + w + 80} ${300} ${1180} ${300} ${1250} ${388}`} fill="none"
            stroke={pal.ink} strokeWidth={3} strokeDasharray="12 10" strokeDashoffset={-t * 40} opacity={swU * 0.8} />
          {costs.map((c, k) => {
            const at = cue(c, 0.8 + k * 0.04);
            const u = eo(t, at, 0.6);
            const y = 500 + k * 100;
            return (
              <g key={k} opacity={u} transform={`translate(${40 * (1 - u)} 0)`}>
                <rect x={1250} y={y - 40} width={540} height={74} rx={12} fill={pal.bg2} />
                <rect x={1250} y={y - 40} width={540 * clamp((t - at) / 1.5) * (c.weight || 0.8)} height={74} rx={12} fill={pal.risk || '#FF5A5F'} opacity={0.22} />
                <text x={1276} y={y + 8} fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={28}>{c.label}</text>
              </g>
            );
          })}
        </g>
      )}
      {p.caption && <RiseText x={x0} y={H - 60} at={cue(p.caption_cue, 0.9)} size={32} color={pal.accent3}>{p.caption}</RiseText>}
    </svg>
  );
};

// ------------------------------------------------------------------ supply_chain
export const SupplyChain: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const geo = useGeo(p.geo || 'world');
  const rings = useMemo(() => parseLayer(p.geo || 'world', geo.paths), [geo, p.geo]);
  const views: any[] = p.views || [{lon: 60, lat: 25, span: 260}];
  let v = views[0];
  for (let i = 1; i < views.length; i++) {
    const u = eio(t, cue(views[i], 0.3 + i * 0.2), p.move || 2.4);
    v = {lon: lerp(v.lon, views[i].lon, u), lat: lerp(v.lat, views[i].lat, u), span: Math.exp(lerp(Math.log(v.span), Math.log(views[i].span), u))};
  }
  const S = 4096;
  const [cx, cy] = merc(v.lon + Math.sin(t * 0.2) * 0.003 * v.span, v.lat);
  const k = W / ((v.span / 360) * S);
  const ox = W * (p.anchor_x ?? 0.5), oy = H * (p.anchor_y ?? 0.46);
  const toS = (lon: number, lat: number): [number, number] => { const [x, y] = merc(lon, lat); return [(x - cx) * k + ox, (y - cy) * k + oy]; };
  const nodes: Record<string, any> = {};
  (p.nodes || []).forEach((n: any, i: number) => (nodes[n.id] = {...n, i, at: cue(n, 0.05 + i * 0.08)}));
  const bn = p.bottleneck ? {...p.bottleneck, at: cue(p.bottleneck, 0.8)} : null;
  const bnU = bn ? eo(t, bn.at, 0.8) : 0;
  // downstream of the bottleneck = nodes reachable from it
  const down = new Set<string>();
  if (bn) {
    const stack = [bn.node];
    while (stack.length) { const c = stack.pop()!; (p.links || []).forEach((l: any) => { if (l.from === c && !down.has(l.to)) { down.add(l.to); stack.push(l.to); } }); }
  }
  const highlights: Record<string, string> = {};
  Object.values(nodes).forEach((n: any) => { if (n.country) highlights[n.country] = C(pal, n.colour, 'accent2'); });
  return (
    <svg width={W} height={H}>
      <rect width={W} height={H} fill={pal.bg} />
      {Object.entries(rings).map(([code, rs]) => {
        const d = screenPath(rs as any, cx, cy, k, ox, oy, W, H);
        if (!d) return null;
        const hl = highlights[code];
        const hu = hl ? eo(t, Math.min(...Object.values(nodes).filter((n: any) => n.country === code).map((n: any) => n.at)), 0.8) : 0;
        return <path key={code} d={d} fill={hl ? mixHex2(pal.land, hl, 0.45 * hu) : pal.land} stroke={pal.border} strokeWidth={1} />;
      })}
      {(p.links || []).map((l: any, i: number) => {
        const a = nodes[l.from], b = nodes[l.to];
        if (!a || !b) return null;
        const start = Math.max(a.at, b.at) + 0.3 + (l.offset || 0);
        const u = eio(t, start, 1.1);
        if (u <= 0) return null;
        const [x1, y1] = toS(a.lon, a.lat), [x2, y2] = toS(b.lon, b.lat);
        const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - Math.hypot(x2 - x1, y2 - y1) * (l.lift ?? 0.25);
        const B = (q: number): [number, number] => [(1 - q) ** 2 * x1 + 2 * (1 - q) * q * mx + q * q * x2, (1 - q) ** 2 * y1 + 2 * (1 - q) * q * my + q * q * y2];
        const pts = Array.from({length: 32}, (_, j) => B((j / 31) * u));
        const isDown = bn && (down.has(l.to) || l.from === bn.node);
        const slow = isDown ? lerp(1, 0.18, bnU) : 1;
        const col = isDown && bnU > 0.3 ? pal.risk || '#FF5A5F' : C(pal, l.colour || a.colour, 'accent2');
        const n = 4;
        return (
          <g key={i}>
            <path d={'M' + pts.map((q) => q.map((z) => z.toFixed(1)).join(',')).join(' L')} fill="none" stroke={col} strokeWidth={3} opacity={0.75} />
            {u >= 1 && Array.from({length: n}, (_, j) => {
              const q = ((t - start) * 0.33 * slow + j / n) % 1;
              const [x, y] = B(q);
              return <rect key={j} x={x - 6} y={y - 6} width={12} height={12} rx={3} fill={col} opacity={isDown ? lerp(1, 0.35, bnU) : 1} />;
            })}
          </g>
        );
      })}
      {/* queue piling up before the bottleneck */}
      {bn && bnU > 0 && nodes[bn.node] && (() => {
        const [x, y] = toS(nodes[bn.node].lon, nodes[bn.node].lat);
        const pile = Math.min(18, Math.floor((t - bn.at) * 4));
        return <g>{Array.from({length: pile}, (_, j) => <rect key={j} x={x - 90 - (j % 6) * 16} y={y + 30 + Math.floor(j / 6) * 16} width={12} height={12} rx={2}
          fill={pal.risk || '#FF5A5F'} opacity={0.85} />)}
          <circle cx={x} cy={y} r={30 + 26 * ((t * 1.4) % 1)} fill="none" stroke={pal.risk || '#FF5A5F'} strokeWidth={4} opacity={1 - ((t * 1.4) % 1)} />
          <text x={x} y={y + (bn.label_dy ?? 110)} textAnchor="middle" fill={pal.risk || '#FF5A5F'} fontFamily={font.display} fontWeight={800} fontSize={30} opacity={bnU}>{bn.label || 'BOTTLENECK'}</text>
        </g>;
      })()}
      {Object.values(nodes).map((n: any) => {
        const [x, y] = toS(n.lon, n.lat);
        const u = easeBack(prog(t, n.at, 0.6));
        if (u <= 0) return null;
        const col = C(pal, n.colour, 'accent2');
        const dim = bn && down.has(n.id) ? lerp(1, 0.45, bnU) : 1;
        const dx = n.dx ?? 24, dy = n.dy ?? 0;
        const wide = v.span > (p.wide_span || 120);
        if (n.wide_only && !wide) return null;
        const showLabel = !(n.hide_wide && wide);
        return (
          <g key={n.id} opacity={dim}>
            <circle cx={x} cy={y} r={14 * u} fill={col} stroke={pal.bg} strokeWidth={3} />
            <circle cx={x} cy={y} r={14 + 22 * ((t * 0.8 + n.i * 0.2) % 1)} fill="none" stroke={col} opacity={0.6 * (1 - ((t * 0.8 + n.i * 0.2) % 1))} />
            <g opacity={eo(t, n.at + 0.2, 0.5) * (showLabel ? 1 : 0)}>
              <text x={x + dx} y={y + dy - 4} textAnchor={dx < 0 ? 'end' : 'start'} fill={pal.ink} fontFamily={font.display} fontWeight={800} fontSize={26}>{n.label}</text>
              {n.role && <text x={x + dx} y={y + dy + 24} textAnchor={dx < 0 ? 'end' : 'start'} fill={col} fontFamily={font.body} fontWeight={600} fontSize={20}>{n.role}</text>}
            </g>
          </g>
        );
      })}
      {/* process strip */}
      {p.steps && (() => {
        const steps: any[] = p.steps;
        const sw = (W - 200) / steps.length;
        return (
          <g>
            <rect x={60} y={H - 150} width={W - 120} height={96} rx={16} fill={pal.bg} opacity={0.9} />
            {steps.map((s, i) => {
              const at = cue(s, 0.05 + i * 0.1);
              const u = eo(t, at, 0.5);
              const bad = bn && s.node === bn.node && bnU > 0.3;
              const col = bad ? pal.risk || '#FF5A5F' : C(pal, s.colour, 'accent2');
              const x = 100 + i * sw;
              return (
                <g key={i}>
                  {i > 0 && <text x={x - 14} y={H - 92} textAnchor="middle" fill={pal.muted} fontSize={26} fontFamily={font.body}>›</text>}
                  <rect x={x} y={H - 130} width={sw - 30} height={56} rx={28} fill={u > 0 ? col : pal.bg2} fillOpacity={0.18 + 0.5 * u * (bad ? 0.6 + 0.4 * Math.sin(t * 8) : 1) * 0.6}
                    stroke={u > 0 ? col : pal.border} strokeWidth={2} />
                  <text x={x + (sw - 30) / 2} y={H - 94} textAnchor="middle" fill={u > 0 ? pal.ink : pal.muted} fontFamily={font.body} fontWeight={700} fontSize={20}>{s.label}</text>
                </g>
              );
            })}
          </g>
        );
      })()}
      {p.title && <RiseText x={110} y={130} at={cue(p.title_cue, 0)} size={50} weight={800} display>{p.title}</RiseText>}
      {p.subtitle && <RiseText x={112} y={172} at={cue(p.subtitle_cue, 0.05)} size={26} color={pal.muted}>{p.subtitle}</RiseText>}
    </svg>
  );
};

// ------------------------------------------------------------------ stacked_columns
export const StackedColumns: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const years: any[] = p.years || [];
  const series: any[] = p.series || [];
  const x0 = 220, x1 = W - 160, yb = H - 190, top = 310;
  const maxV = p.y_max || Math.max(...years.map((y) => y.total));
  const colW = (x1 - x0) / years.length;
  const growAt = Math.min(cue(p.grow_cue, 0.05), scene.lead + 0.8);
  const step = p.step_seconds || 0.55;
  const mixU = p.mix_cue ? eio(t, cue(p.mix_cue, 0.75), 1.6) : 0;
  const sc = (v: number) => ((yb - top) * v) / maxV;
  const ticks: number[] = p.ticks || [];
  return (
    <svg width={W} height={H}>
      {p.title && <RiseText x={120} y={150} at={cue(p.title_cue, 0)} size={50} weight={800} display>{mixU > 0.5 ? (p.mix_title || p.title) : p.title}</RiseText>}
      {p.subtitle && <RiseText x={122} y={192} at={cue(p.title_cue, 0.03)} size={26} color={pal.muted}>{mixU > 0.5 ? (p.mix_subtitle || p.subtitle) : p.subtitle}</RiseText>}
      {/* axis */}
      <line x1={x0 - 20} y1={yb} x2={x1} y2={yb} stroke={pal.border} strokeWidth={2} />
      {ticks.map((v, i) => (
        <g key={i} opacity={(1 - mixU) * eo(t, growAt, 0.6)}>
          <line x1={x0 - 20} y1={yb - sc(v)} x2={x1} y2={yb - sc(v)} stroke={pal.border} strokeOpacity={0.35} strokeDasharray="4 8" />
          <text x={x0 - 34} y={yb - sc(v) + 8} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontSize={22}>{`${p.axis_prefix ?? '$'}${v}${p.axis_suffix ?? 'bn'}`}</text>
        </g>
      ))}
      {[25, 50, 75, 100].map((v, i) => (
        <g key={'m' + i} opacity={mixU}>
          <line x1={x0 - 20} y1={yb - ((yb - top) * v) / 100} x2={x1} y2={yb - ((yb - top) * v) / 100} stroke={pal.border} strokeOpacity={0.35} strokeDasharray="4 8" />
          <text x={x0 - 34} y={yb - ((yb - top) * v) / 100 + 8} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontSize={22}>{`${v}%`}</text>
        </g>
      ))}
      {years.map((y, i) => {
        const at = growAt + i * step;
        const u = easeInOut(prog(t, at, 0.9));
        const cxx = x0 + i * colW + colW / 2, bw = Math.min(110, colW * 0.62);
        let acc = 0;
        const segs = series.map((s, k) => {
          const val = y.parts?.[s.key] ?? 0;
          const hAbs = sc(val) * u, hMix = ((yb - top) * val) / y.total;
          const h = lerp(hAbs, hMix * clamp(u * 2), mixU);
          const yTop = yb - acc - h;
          acc += h;
          return <rect key={k} x={cxx - bw / 2} y={yTop} width={bw} height={Math.max(0, h)} fill={C(pal, s.colour)} opacity={0.92} />;
        });
        const hTot = lerp(sc(y.total) * u, (yb - top) * clamp(u * 2), mixU);
        const first = series[0];
        const share = first ? Math.round(((y.parts?.[first.key] ?? 0) / y.total) * 100) : 0;
        const glow = (t - at) > 0 && (t - at) < 1.4 ? 1 - (t - at) / 1.4 : 0;
        return (
          <g key={i} opacity={u > 0 ? 1 : 0}>
            {segs}
            {glow > 0 && <rect x={cxx - bw / 2} y={yb - hTot} width={bw} height={6} fill="#fff" opacity={0.6 * glow} />}
            <text x={cxx} y={yb - hTot - 16} textAnchor="middle" fill={mixU > 0.5 ? C(pal, first?.colour) : pal.ink} fontFamily={font.display} fontWeight={800}
              fontSize={colW > 150 ? 30 : 24} opacity={eo(t, at + 0.6, 0.4)}>{mixU > 0.5 ? `${share}%` : y.display || `$${y.total}`}</text>
            <text x={cxx} y={yb + 40} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={22}>{y.label}</text>
          </g>
        );
      })}
      {/* legend */}
      {series.map((s, k) => (
        <g key={k} opacity={eo(t, growAt + 0.3 + k * 0.15, 0.5)}>
          <rect x={122 + k * 420} y={222} width={24} height={24} rx={4} fill={C(pal, s.colour)} />
          <text x={158 + k * 420} y={242} fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={24}>{s.label}</text>
        </g>
      ))}
      {(p.notes || []).map((n: any, i: number) => {
        const at = cue(n, 0.5 + i * 0.1);
        const u = eo(t, at, 0.5);
        return <g key={i} opacity={u}>
          <rect x={n.x - 16} y={n.y - 40} width={String(n.text).length * 14 + 32} height={56} rx={10} fill={pal.bg} opacity={0.9} stroke={C(pal, n.colour, 'accent3')} />
          <text x={n.x} y={n.y - 4} fill={C(pal, n.colour, 'accent3')} fontFamily={font.body} fontWeight={700} fontSize={24}>{n.text}</text>
        </g>;
      })}
    </svg>
  );
};

// ------------------------------------------------------------------ landscape
export const Landscape: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const cols: any[] = p.players || [];
  const rows: any[] = p.rows || [];
  const x0 = 110, labelW = 330, top = 250, rh = p.row_h || 104;
  const cw = (W - x0 * 2 - labelW) / cols.length;
  // cursor: glides to each row's header as the row is cued and "clicks"
  const rowAt = rows.map((r, i) => cue(r, 0.08 + i * 0.12));
  let cur: [number, number] = [W * 0.6, H * 0.9];
  let click = -1;
  rowAt.forEach((a, i) => {
    const u = easeInOut(prog(t, a - 0.6, 0.6));
    const target: [number, number] = [x0 + 240, top + i * rh + rh / 2 + 10];
    if (t >= a - 0.6) { cur = [lerp(cur[0], target[0], u), lerp(cur[1], target[1], u)]; }
    if (t >= a && t < a + 0.5) click = i;
  });
  const axAt = cue(p.axis_cue, 0.85);
  const axU = eo(t, axAt, 0.8);
  return (
    <svg width={W} height={H}>
      {p.title && <RiseText x={x0} y={140} at={cue(p.title_cue, 0)} size={50} weight={800} display>{p.title}</RiseText>}
      {p.subtitle && <RiseText x={x0 + 2} y={182} at={cue(p.title_cue, 0.03)} size={24} color={pal.muted}>{p.subtitle}</RiseText>}
      {cols.map((c, j) => {
        const u = eo(t, cue(c, 0.02 + j * 0.05), 0.6);
        const x = x0 + labelW + j * cw;
        const col = C(pal, c.colour, 'accent2');
        return (
          <g key={j} opacity={u} transform={`translate(0 ${-20 * (1 - u)})`}>
            <rect x={x + 8} y={top - 70} width={cw - 16} height={64} rx={12} fill={col} opacity={0.18} stroke={col} strokeWidth={2} />
            <text x={x + cw / 2} y={top - 44} textAnchor="middle" fill={pal.ink} fontFamily={font.display} fontWeight={800} fontSize={26}>{c.name}</text>
            <text x={x + cw / 2} y={top - 16} textAnchor="middle" fill={col} fontFamily={font.body} fontWeight={600} fontSize={18}>{c.kind}</text>
          </g>
        );
      })}
      {rows.map((r, i) => {
        const a = rowAt[i];
        const u = eo(t, a, 0.4);
        const y = top + i * rh;
        const active = t >= a && (i === rows.length - 1 || t < rowAt[i + 1]) && axU < 0.5;
        return (
          <g key={i} opacity={u > 0 ? 1 : 0.25}>
            <rect x={x0} y={y + 4} width={W - x0 * 2} height={rh - 8} rx={12} fill={active ? pal.accent3 : pal.bg2} opacity={active ? 0.1 : 0.7} />
            <text x={x0 + 24} y={y + rh / 2 + 9} fill={active ? pal.accent3 : pal.ink} fontFamily={font.body} fontWeight={700} fontSize={26}>{r.label}</text>
            {(r.cells || []).map((cell: string, j: number) => {
              const cu = prog(t, a + 0.25 + j * 0.25, 0.8);
              const x = x0 + labelW + j * cw;
              const lines = String(cell).split('\n');
              return lines.map((ln, li) => (
                <text key={j + '-' + li} x={x + cw / 2} y={y + rh / 2 + 8 + (li - (lines.length - 1) / 2) * 28} textAnchor="middle" fill={pal.ink}
                  fontFamily={font.body} fontSize={22} opacity={0.92}>{typed(ln, cu * lines.length - li)}</text>
              ));
            })}
          </g>
        );
      })}
      {/* conceptual axis */}
      {axU > 0 && (
        <g opacity={axU}>
          <rect x={0} y={H - 250} width={W} height={250} fill={pal.bg} opacity={0.95} />
          <text x={W / 2} y={H - 196} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontWeight={700} fontSize={22} letterSpacing={4}>
            {String(p.axis_label || 'Conceptual, not a ranking').toUpperCase()}</text>
          <line x1={260} y1={H - 120} x2={W - 260} y2={H - 120} stroke={pal.border} strokeWidth={4} />
          <text x={240} y={H - 112} textAnchor="end" fill={pal.accent} fontFamily={font.body} fontWeight={700} fontSize={26}>{p.axis_left || 'Flexible'}</text>
          <text x={W - 240} y={H - 112} fill={pal.accent2} fontFamily={font.body} fontWeight={700} fontSize={26}>{p.axis_right || 'Specialised'}</text>
          {cols.map((c, j) => {
            const u = easeBack(prog(t, axAt + 0.5 + j * 0.35, 0.8));
            const x = lerp(W / 2, 260 + (W - 520) * (c.axis ?? 0.5), u);
            const col = C(pal, c.colour, 'accent2');
            return <g key={j} transform={`translate(${x} ${H - 120})`} opacity={clamp(u)}>
              <circle r={18} fill={col} stroke={pal.bg} strokeWidth={4} />
              <text y={j % 2 ? 52 : -32} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={700} fontSize={22}>{c.short || c.name}</text>
            </g>;
          })}
        </g>
      )}
      {/* cursor */}
      {axU < 0.5 && t > rowAt[0] - 0.8 && (
        <g transform={`translate(${cur[0]} ${cur[1]})`}>
          {click >= 0 && <circle r={10 + 40 * ((t - rowAt[click]) / 0.5)} fill="none" stroke={pal.accent3} strokeWidth={3} opacity={1 - (t - rowAt[click]) / 0.5} />}
          <path d="M 0 0 L 0 34 L 9 26 L 16 42 L 22 39 L 15 24 L 27 24 Z" fill="#FFFFFF" stroke="#000" strokeWidth={2} />
        </g>
      )}
    </svg>
  );
};
