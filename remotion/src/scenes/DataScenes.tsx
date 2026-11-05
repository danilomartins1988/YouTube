import React from 'react';
import {countDisplay, eio, eo, easeBack, focusIndex, fmtNum, keywords, lerp, mix, norm, prog, rand, spokenAt, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';

const W0 = 1920;

/** Chapter card: number ticks in, title revealed through a sliding mask, gold rule draws. */
export const ActTitle: React.FC = () => {
  const {t, pal, font, scene, W, H} = useCtx();
  const p = scene.params;
  const m = eio(t, 0.2, 0.9);
  const r = eo(t, 0.5, 0.9);
  return (
    <svg width={W} height={H}>
      <defs>
        <clipPath id="actmask"><rect x={0} y={H / 2 - 110} width={W * m} height={160} /></clipPath>
      </defs>
      <text x={W / 2} y={H / 2 - 140} textAnchor="middle" fill={pal.accent} fontFamily={font.body} fontWeight={600} fontSize={28}
        letterSpacing={10} opacity={eo(t, 0.1, 0.5)}>{String(p.number || '').toUpperCase()}</text>
      <g clipPath="url(#actmask)">
        <text x={W / 2} y={H / 2 + 20} textAnchor="middle" fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={p.size || 110}>
          {p.title}
        </text>
      </g>
      <rect x={W / 2 - 160 * r} y={H / 2 + 62} width={320 * r} height={4} fill={pal.accent} />
      {p.subtitle && (
        <text x={W / 2} y={H / 2 + 130} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontSize={36} opacity={eo(t, 0.9, 0.6)}>
          {p.subtitle}
        </text>
      )}
    </svg>
  );
};

/** Kinetic typography: lines enter word by word on narration cues; optional strike-through. */
export const KineticText: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const lines: any[] = scene.params.lines || [];
  const align = scene.params.align || 'left';
  const x0 = align === 'center' ? W / 2 : 240;
  let y = H / 2 - (lines.reduce((s, l) => s + (l.size || 64) * 1.35, 0)) / 2; // top of the block
  const first = cue(lines[0], 0);
  const bar = eo(t, Math.min(first, scene.lead + 0.4), 0.8);
  const total = lines.reduce((s, l) => s + (l.size || 64) * 1.35, 0);
  return (
    <svg width={W} height={H}>
      {align !== 'center' && <rect x={x0 - 50} y={H / 2 - total / 2} width={8} height={total * bar} fill={pal.accent} />}
      {align !== 'center' && bar >= 1 && (() => {
        // a gold pulse travels down the accent bar every few seconds
        const q = ((t - first) % 3.5) / 3.5;
        return <rect x={x0 - 54} y={H / 2 - total / 2 + q * (total - 60)} width={16} height={60} rx={6} fill={pal.accent} opacity={0.9 * (1 - q)} />;
      })()}
      {lines.map((ln, i) => {
        const size = ln.size || 64;
        const start = i === 0 ? Math.min(cue(ln, 0), scene.lead + 0.4) : cue(ln, i * 0.15);
        const words = String(ln.text).split(' ');
        const now = spokenAt(scene, t);
        const yy = y + size * 1.02; // baseline of this line
        y += size * 1.35;
        const ghost = 0.22 * eo(t, scene.lead + 0.3 + i * 0.25, 0.5); // the whole block is visible early, lines light up on cue
        const strike = ln.strike_cue ? eo(t, cue(ln.strike_cue), 0.35) : 0;
        const colour = ln.color ? pal[ln.color] || ln.color : pal.ink;
        return (
          <g key={i} opacity={1 - 0.5 * strike}>
            <text x={x0} y={yy} textAnchor={align === 'center' ? 'middle' : 'start'} fontFamily={ln.style === 'body' ? font.body : font.display}
              fontWeight={ln.style === 'body' ? 400 : 700} fontSize={size} fill={colour}>
              {words.map((w, j) => {
                const u = eo(t, start + j * 0.07, 0.35);
                const hot = u > 0.9 && now && norm(w) === now;
                return (
                  <tspan key={j} opacity={Math.max(ghost, u)} dy={0} fill={hot ? pal.accent : undefined}>
                    {(j ? ' ' : '') + w}
                  </tspan>
                );
              })}
            </text>
            {strike > 0 && (
              <rect x={align === 'center' ? x0 - (ln.text.length * size * 0.26) : x0 - 6} y={yy - size * 0.32}
                width={ln.text.length * size * 0.52 * strike} height={Math.max(4, size * 0.08)} fill={pal.accent} />
            )}
          </g>
        );
      })}
    </svg>
  );
};

/** Big number that counts up, with a ring of orbiting ticks and label lines. */
export const BigCounter: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const start = cue(p.cue, 0.1);
  const u = p.count === false ? (t >= start - 0.2 ? 1 : 0) : eo(t, start, 1.6);
  const a = eo(t, Math.min(start - 0.3, scene.lead + 0.2), 0.5);
  const shown = t >= start - 0.2 ? countDisplay(String(p.display), u) : '';
  const cx = W / 2, cy = H / 2 - 40;
  const ticks = Array.from({length: 72}, (_, i) => {
    const ang = (i / 72) * Math.PI * 2 + t * 0.45;
    const on = i / 72 <= u;
    const r1 = 360, r2 = on ? 382 : 372;
    return <line key={i} x1={cx + r1 * Math.cos(ang)} y1={cy + r1 * Math.sin(ang) * 0.42} x2={cx + r2 * Math.cos(ang)} y2={cy + r2 * Math.sin(ang) * 0.42}
      stroke={on ? pal.accent : pal.border} strokeWidth={3} opacity={a * (on ? 0.8 : 0.35)} />;
  });
  const size = Math.min(230, (1500 / Math.max(4, String(p.display).length)) * 1.6);
  const arcU = eio(t, start + 1.6, Math.max(1, scene.lead + scene.speech - start - 1.6));
  const pulse = u >= 1 ? ((t - start - 1.6) % 3) / 3 : 0;
  const arc = (r: number, f: number) => {
    const a1 = -Math.PI / 2 + f * Math.PI * 2;
    return `M ${cx} ${cy - r * 0.42} A ${r} ${r * 0.42} 0 ${f > 0.5 ? 1 : 0} 1 ${cx + r * Math.cos(a1)} ${cy + r * 0.42 * Math.sin(a1)}`;
  };
  return (
    <svg width={W} height={H}>
      {ticks}
      {arcU > 0 && arcU < 1 && <path d={arc(400, arcU)} fill="none" stroke={pal.accent} strokeWidth={4} opacity={0.7} />}
      {u >= 1 && <ellipse cx={cx} cy={cy} rx={360 + 120 * pulse} ry={(360 + 120 * pulse) * 0.42} fill="none" stroke={pal.accent} strokeWidth={2} opacity={0.5 * (1 - pulse)} />}
      {p.kicker && <text x={cx} y={cy - size * 0.72} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontWeight={600}
        fontSize={30} letterSpacing={5} opacity={a}>{String(p.kicker).toUpperCase()}</text>}
      <text x={cx} y={cy + size * 0.35} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={size}
        opacity={a} transform={`translate(0 ${14 * (1 - a)})`}>{shown}</text>
      <RiseText x={cx} y={cy + size * 0.35 + 90} at={start + 0.9} size={50} weight={600} anchor="middle" display>{p.label}</RiseText>
      {p.sublabel && <RiseText x={cx} y={cy + size * 0.35 + 150} at={start + 1.4} size={32} anchor="middle" color={pal.muted}>{p.sublabel}</RiseText>}
    </svg>
  );
};

/** Progressive line chart: axes build, series draw with the narration, event annotations pop at cues. */
export const LineChart: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const series: {name: string; code: string; points: {year: number; value: number}[]}[] = p.series;
  const x0 = 260, x1 = 1560, y0 = 290, y1 = 900;
  const years = series[0].points.map((q) => q.year);
  const vmax = p.y_max || Math.max(...series.flatMap((s) => s.points.map((q) => q.value))) * 1.08;
  const X = (yr: number) => x0 + ((x1 - x0) * (yr - years[0])) / (years[years.length - 1] - years[0]);
  const Y = (v: number) => y1 - ((y1 - y0) * v) / vmax;
  const a0 = eo(t, 0.2, 0.6);
  const start = cue(p.cue, 0.05);
  const u = eio(t, start, p.draw_seconds || Math.max(3, scene.speech * 0.85));
  const steps = p.y_steps || 5;
  const fmt = (v: number) => `${p.axis_prefix ?? ''}${fmtNum(v / (p.axis_divisor || 1), p.axis_decimals || 0)}${p.axis_suffix ?? ''}`;
  const head: React.ReactNode[] = [];
  return (
    <svg width={W} height={H}>
      <text x={x0 - 140} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={a0}>{p.title}</text>
      <text x={x0 - 138} y={244} fill={pal.muted} fontFamily={font.body} fontSize={28} opacity={a0}>{p.subtitle}</text>
      {Array.from({length: steps + 1}, (_, i) => {
        const v = (vmax / steps) * i;
        const g = eo(t, 0.3 + i * 0.06, 0.5);
        return (
          <g key={i} opacity={g}>
            <line x1={x0} x2={x0 + (x1 - x0) * g} y1={Y(v)} y2={Y(v)} stroke={pal.border} strokeOpacity={0.6} />
            <text x={x0 - 16} y={Y(v) + 8} textAnchor="end" fill={pal.muted} fontFamily={font.body} fontSize={22}>{fmt(v)}</text>
          </g>
        );
      })}
      {years.filter((yr, i) => i === 0 || i === years.length - 1 || yr % (p.year_every || 10) === 0).map((yr) => (
        <text key={yr} x={X(yr)} y={y1 + 40} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontSize={22} opacity={a0}>{yr}</text>
      ))}
      {series.map((s, si) => {
        const pts = s.points.map((q) => [X(q.year), Y(q.value)]);
        const pos = u * (pts.length - 1);
        const n = Math.floor(pos);
        const f = pos - n;
        const drawn = pts.slice(0, n + 1);
        if (n + 1 < pts.length) drawn.push([lerp(pts[n][0], pts[n + 1][0], f), lerp(pts[n][1], pts[n + 1][1], f)]);
        if (drawn.length < 2) return null;
        const hl = s.code === p.highlight;
        const colour = hl ? pal.accent : si === 1 ? pal.ink : pal.muted;
        const d = 'M' + drawn.map((q) => q.join(',')).join(' L');
        const area = d + ` L${drawn[drawn.length - 1][0]},${y1} L${drawn[0][0]},${y1} Z`;
        const [hx, hy] = drawn[drawn.length - 1];
        const idx = Math.min(s.points.length - 1, Math.round(pos));
        head.push(
          <g key={'h' + si}>
            <circle cx={hx} cy={hy} r={hl ? 9 : 6} fill={colour} />
            <text x={hx + 18} y={hy - 6} fill={colour} fontFamily={font.body} fontWeight={hl ? 700 : 400} fontSize={hl ? 28 : 24}>{s.name}</text>
            <text x={hx + 18} y={hy + 24} fill={hl ? pal.accent : pal.muted} fontFamily={font.body} fontSize={22}>
              {`${p.value_prefix ?? ''}${fmtNum(s.points[idx].value / (p.value_divisor || 1), p.value_decimals || 0)}${p.value_suffix ?? ''}`}
            </text>
          </g>,
        );
        return (
          <g key={si}>
            {hl && <path d={area} fill={pal.accent} opacity={0.08} />}
            <path d={d} fill="none" stroke={colour} strokeWidth={hl ? 6 : 3.5} strokeLinejoin="round" strokeLinecap="round" />
          </g>
        );
      })}
      {(p.events || []).map((ev: any, i: number) => {
        const at = cue(ev, 0.5);
        const e = eo(t, at, 0.5);
        if (e <= 0) return null;
        const ex = X(ev.year);
        return (
          <g key={i} opacity={e}>
            <line x1={ex} x2={ex} y1={y0 - 10} y2={y1} stroke={pal.accent} strokeDasharray="6 8" strokeOpacity={0.7} />
            <rect x={ex - 6} y={y0 - 64} width={Math.max(160, ev.label.length * 13)} height={44} rx={6} fill={pal.bg2} stroke={pal.accent} strokeOpacity={0.6} />
            <text x={ex + 8} y={y0 - 34} fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={22}>{ev.label}</text>
          </g>
        );
      })}
      {head}
    </svg>
  );
};

/** Horizontal bars grow in a stagger; values count with them. */
export const BarChart: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const rows: any[] = p.sort === false ? p.data : [...p.data].sort((a, b) => b.value - a.value);
  const vmax = Math.max(...rows.map((r) => r.value));
  const a0 = eo(t, 0.2, 0.6);
  const x0 = 560, x1 = 1600, top = 330;
  const rowH = Math.min(96, 560 / rows.length);
  const start = Math.min(cue(p.cue, 0.05), scene.lead + 0.8);
  return (
    <svg width={W} height={H}>
      <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={a0}>{p.title}</text>
      <text x={122} y={244} fill={pal.muted} fontFamily={font.body} fontSize={28} opacity={a0}>{p.subtitle}</text>
      {rows.map((r, i) => {
        const u = eo(t, start + i * 0.22, 1.1);
        const yy = top + i * rowH;
        const settled = start + rows.length * 0.22 + 1.2;
        const fi = focusIndex(scene, t, rows.map((x) => keywords(x.name)), settled);
        const focus = fi === i;
        const hl = r.code === p.highlight;
        const colour = hl ? pal.accent : r.code === p.reference ? pal.ink : pal.muted;
        const w = ((x1 - x0) * r.value) / vmax;
        return (
          <g key={r.code} opacity={eo(t, start + i * 0.22 - 0.1, 0.4)}>
            <text x={x0 - 28} y={yy + rowH * 0.5} textAnchor="end" fill={hl ? pal.ink : pal.muted} fontFamily={font.body} fontWeight={hl ? 700 : 400} fontSize={30}>{r.name}</text>
            <rect x={x0} y={yy + rowH * 0.18} width={w * u} height={rowH * 0.55} rx={4} fill={colour} opacity={hl ? 1 : focus ? 0.95 : 0.7} />
            {focus && (() => {
              const q = ((t - settled) % 3.2) / 3.2;
              return <rect x={x0 + w * u * q - 40} y={yy + rowH * 0.18} width={80} height={rowH * 0.55} fill="#ffffff" opacity={0.25 * Math.sin(q * Math.PI)} />;
            })()}
            {focus && <rect x={x0 - 8} y={yy + rowH * 0.12} width={4} height={rowH * 0.67} fill={pal.accent} />}
            <text x={x0 + w * u + 16} y={yy + rowH * 0.56} fill={hl ? pal.accent : pal.ink} fontFamily={font.body} fontWeight={700} fontSize={28}>
              {`${p.value_prefix ?? ''}${fmtNum(r.value * u, p.value_decimals || 0)}${p.value_suffix ?? ''}`}
            </text>
          </g>
        );
      })}
      {p.callout && <RiseText x={W - 120} y={H - 130} at={cue(p.callout_cue, 0.7)} size={40} anchor="end" color={pal.accent} weight={600}>{p.callout}</RiseText>}
    </svg>
  );
};

/** Donut allocation: arcs sweep one after another, legend counts in. */
export const Donut: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const segs: any[] = p.segments;
  const total = segs.reduce((s, x) => s + x.value, 0);
  const cx = 640, cy = 560, r = 270, th = 70;
  const cols = [pal.accent, pal.ink, pal.accent2, pal.muted, pal.border];
  let acc = 0;
  const start = Math.min(cue(p.cue, 0.05), scene.lead + 0.8);
  const settled = start + segs.length * 0.5 + 1.0;
  const fi = focusIndex(scene, t, segs.map((x) => keywords(x.label)), settled);
  const arcs = segs.map((s, i) => {
    const a0 = (acc / total) * Math.PI * 2 - Math.PI / 2;
    acc += s.value;
    const a1full = (acc / total) * Math.PI * 2 - Math.PI / 2;
    const u = eio(t, cue(s, 0) > start ? cue(s, 0) : start + i * 0.5, 0.9);
    const a1 = a0 + (a1full - a0) * u;
    if (u <= 0) return null;
    const large = a1 - a0 > Math.PI ? 1 : 0;
    const pop = fi === i ? 22 * eo(t, settled, 0.4) : 0;
    const mid = (a0 + a1) / 2;
    const P = (a: number, rr: number) => `${cx + pop * Math.cos(mid) + rr * Math.cos(a)},${cy + pop * Math.sin(mid) + rr * Math.sin(a)}`;
    const d = `M${P(a0, r)} A${r},${r} 0 ${large} 1 ${P(a1, r)} L${P(a1, r - th)} A${r - th},${r - th} 0 ${large} 0 ${P(a0, r - th)} Z`;
    return <path key={i} d={d} fill={cols[i % cols.length]} opacity={0.95} />;
  });
  const a = eo(t, 0.2, 0.6);
  return (
    <svg width={W} height={H}>
      <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={a}>{p.title}</text>
      <text x={122} y={244} fill={pal.muted} fontFamily={font.body} fontSize={28} opacity={a}>{p.subtitle}</text>
      <circle cx={cx} cy={cy} r={r - th / 2} fill="none" stroke={pal.border} strokeOpacity={0.4} strokeWidth={th} />
      {arcs}
      {p.center && <text x={cx} y={cy + 18} textAnchor="middle" fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={54} opacity={eo(t, start + 0.5, 0.6)}>{p.center}</text>}
      {segs.map((s, i) => {
        const u = eo(t, start + i * 0.5 + 0.3, 0.5);
        const yy = 380 + i * 100;
        return (
          <g key={i} opacity={u * (fi < 0 || fi === i ? 1 : 0.55)} transform={`translate(${40 * (1 - u) + (fi === i ? 16 : 0)} 0)`}>
            {fi === i && <rect x={1060} y={yy - 50} width={760} height={76} rx={10} fill={pal.bg2} stroke={pal.accent} strokeOpacity={0.5} />}
            <rect x={1080} y={yy - 30} width={36} height={36} rx={6} fill={cols[i % cols.length]} />
            <text x={1140} y={yy} fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={36}>{s.label}</text>
            <text x={1780} y={yy} textAnchor="end" fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={40}>
              {`${fmtNum(s.value * u, p.value_decimals ?? 1)}%`}
            </text>
          </g>
        );
      })}
    </svg>
  );
};

/** Animated timeline: axis draws, camera pans to keep the newest event in view, markers drop in on cues. */
export const Timeline: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const items: any[] = p.items;
  const y0 = p.start_year, y1 = p.end_year;
  const span = p.span || W - 400; // world width of the axis; > screen width makes the camera pan
  const X = (yr: number) => 200 + (span * (yr - y0)) / (y1 - y0);
  const times = items.map((it, i) => cue(it, (i + 0.5) / items.length));
  let focus = X(items[0].year);
  items.forEach((it, i) => { const u = eio(t, times[i] - 0.3, 0.9); focus = lerp(focus, X(it.year), u); });
  const camX = Math.max(0, Math.min(span + 400 - W, focus - W * 0.45));
  const ay = H / 2 + 40;
  const grow = eio(t, 0.2, 1.6);
  return (
    <svg width={W} height={H}>
      <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={eo(t, 0.2, 0.5)}>{p.title}</text>
      <g transform={`translate(${-camX} 0)`}>
        <line x1={200} x2={200 + span * grow} y1={ay} y2={ay} stroke={pal.border} strokeWidth={4} />
        {(() => {
          // playhead: glides from event to event as they are narrated, then keeps sweeping to 'today'
          // the playhead moves continuously: towards each event in the time before it is narrated, then on to 'today'
          const keysT = [scene.lead, ...times, scene.duration];
          const keysX = [200, ...items.map((it) => X(it.year)), 200 + span];
          let hx = keysX[0];
          for (let i = 1; i < keysT.length; i++) {
            if (t >= keysT[i]) { hx = keysX[i]; continue; }
            hx = lerp(keysX[i - 1], keysX[i], eio(t, keysT[i - 1], Math.max(0.5, keysT[i] - keysT[i - 1])));
            break;
          }
          return <g><line x1={200} x2={hx} y1={ay} y2={ay} stroke={pal.accent} strokeWidth={4} />
            <circle cx={hx} cy={ay} r={9 + 3 * Math.sin(t * 5)} fill={pal.ink} /></g>;
        })()}
        {Array.from({length: Math.floor((y1 - y0) / (p.tick_every || 10)) + 1}, (_, i) => {
          const yr = y0 + i * (p.tick_every || 10);
          return (
            <g key={yr} opacity={grow}>
              <line x1={X(yr)} x2={X(yr)} y1={ay - 10} y2={ay + 10} stroke={pal.muted} strokeWidth={2} />
              <text x={X(yr)} y={ay + 44} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontSize={22}>{yr}</text>
            </g>
          );
        })}
        {items.map((it, i) => {
          const u = easeBack(prog(t, times[i], 0.6));
          const fade = eo(t, times[i], 0.4);
          const x = X(it.year);
          const up = i % 2 === 0;
          const ty = up ? ay - 200 : ay + 120;
          return (
            <g key={i} opacity={fade}>
              <line x1={x} x2={x} y1={ay} y2={lerp(ay, up ? ay - 150 : ay + 80, fade)} stroke={pal.accent} strokeWidth={2} />
              <circle cx={x} cy={ay} r={14 * u} fill={pal.accent} />
              <circle cx={x} cy={ay} r={14 + 26 * prog(t, times[i], 1.2)} fill="none" stroke={pal.accent} opacity={1 - prog(t, times[i], 1.2)} />
              <text x={x} y={ty} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={96}>{it.display ?? it.year}</text>
              <text x={x} y={ty + 52} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontWeight={600} fontSize={32}>{it.label}</text>
            </g>
          );
        })}
      </g>
    </svg>
  );
};

/** Side-by-side comparison with animated bars under each figure. */
export const Compare: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const sides: any[] = p.sides;
  const a = eo(t, 0.2, 0.5);
  const colW = (W - 240) / sides.length;
  const vmax = Math.max(...sides.map((s) => Number(s.bar ?? 0)), 1);
  return (
    <svg width={W} height={H}>
      {p.title && <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={a}>{p.title}</text>}
      {sides.map((s, i) => {
        const at = cue(s, (i + 0.3) / sides.length);
        const enter = Math.min(at, scene.lead + 0.5 + i * 0.6);
        const u = eo(t, enter, 0.6);
        const settled = Math.max(...sides.map((x, k) => cue(x, (k + 0.3) / sides.length))) + 1.4;
        const fi = focusIndex(scene, t, sides.map((x) => keywords(`${x.kicker} ${x.label}`)), settled, 2.8);
        const glow = fi === i ? eo(t, settled - 0.2, 0.4) : 0;
        const cx = 120 + colW * (i + 0.5);
        const barH = s.bar !== undefined ? (380 * Number(s.bar)) / vmax : 0;
        const hl = i === sides.length - 1 || s.highlight;
        return (
          <g key={i} opacity={u}>
            {i > 0 && <line x1={120 + colW * i} x2={120 + colW * i} y1={330} y2={330 + 520 * u} stroke={pal.accent} strokeOpacity={0.5} strokeWidth={2} />}
            {glow > 0 && <ellipse cx={cx} cy={420} rx={260} ry={110} fill={pal.accent} opacity={0.08 + 0.05 * Math.sin(t * 4)} />}
            <text x={cx} y={330} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontWeight={600} fontSize={28} letterSpacing={4}>{String(s.kicker || '').toUpperCase()}</text>
            <text x={cx} y={460} textAnchor="middle" fill={hl ? pal.accent : pal.ink} fontFamily={font.display} fontWeight={700}
              opacity={eo(t, at - 0.15, 0.3)}
              fontSize={Math.min(150, 1100 / sides.length / Math.max(3, String(s.value).length) * 1.7)}>{countDisplay(String(s.value), eo(t, at, 1.2))}</text>
            <text x={cx} y={530} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontSize={34}>{s.label}</text>
            {barH > 0 && <rect x={cx - 70} y={930 - barH * eo(t, at + 0.2, 1.0)} width={140} height={barH * eo(t, at + 0.2, 1.0)} rx={6} fill={hl ? pal.accent : pal.muted} opacity={0.85} />}
            {barH > 0 && glow > 0 && (() => {
              const q = ((t - settled) % 2.8) / 2.8;
              return <rect x={cx - 70} y={930 - barH * q} width={140} height={10} fill="#ffffff" opacity={0.35 * (1 - q)} />;
            })()}
          </g>
        );
      })}
    </svg>
  );
};

/** Grid of people icons that recolours to show a ratio (e.g. workers per retiree). */
export const PeopleRatio: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const states: any[] = p.states; // [{label, active, total, cue}]
  const n = states[0].total;
  let cur = states[0].active, prev = states[0].active, changeAt = -99;
  let label = states[0].label;
  states.forEach((s, i) => { if (i && t >= cue(s, 0.5)) { prev = cur; cur = s.active; label = s.label; changeAt = cue(s, 0.5); } });
  const cols = Math.min(10, n);
  return (
    <svg width={W} height={H}>
      <text x={120} y={200} fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={56} opacity={eo(t, 0.2, 0.5)}>{p.title}</text>
      {Array.from({length: n}, (_, i) => {
        const x = 260 + (i % cols) * 200, y = 640 + Math.floor(i / cols) * 300;
        const appear = easeBack(prog(t, 0.3 + i * 0.05, 0.5)) * 1.8;
        const flipT = changeAt + (n - 1 - i) * 0.35;           // recolour from the right, one by one
        const on = i < (t >= flipT ? cur : prev);
        const colour = on ? pal.accent : pal.muted;
        return (
          <g key={i} transform={`translate(${x} ${y + Math.sin(t * 2.2 + i) * 6}) scale(${appear})`}>
            <circle cx={0} cy={-62} r={22} fill={colour} />
            <rect x={-30} y={-34} width={60} height={92} rx={26} fill={colour} />
          </g>
        );
      })}
      <text x={1560} y={540} textAnchor="middle" fill={pal.accent} fontFamily={font.display} fontWeight={700} fontSize={110}>{label}</text>
      <text x={1560} y={610} textAnchor="middle" fill={pal.ink} fontFamily={font.body} fontSize={34}>{p.caption}</text>
    </svg>
  );
};

/** Closing card: words land one by one, brand line draws. */
export const EndCard: React.FC = () => {
  const {t, pal, font, scene, cue, W, H} = useCtx();
  const p = scene.params;
  const words: string[] = p.words || [];
  const brandT = cue(p.brand_cue, 0.8);
  const out = eio(t, brandT - 0.6, 0.6);
  const ba = eo(t, brandT, 0.8);
  return (
    <svg width={W} height={H}>
      {words.map((w, i) => {
        const u = eo(t, cue({cue: w.replace(/[.]/g, '')}, 0.15 + i * 0.2), 0.45) * (1 - out);
        return <text key={i} x={W / 2} y={H / 2 - 80 + i * 130 + 20 * (1 - u)} textAnchor="middle" opacity={u}
          fill={i === words.length - 1 ? pal.accent : pal.ink} fontFamily={font.display} fontWeight={700} fontSize={104}>{w}</text>;
      })}
      <rect x={W / 2 - 300 * ba} y={H / 2 - 92} width={600 * ba} height={4} fill={pal.accent} />
      <text x={W / 2} y={H / 2} textAnchor="middle" fill={pal.ink} fontFamily={font.display} fontWeight={700} fontSize={84} letterSpacing={8} opacity={ba}>
        {String(p.brand || 'The Hidden Economics').toUpperCase()}
      </text>
      <text x={W / 2} y={H / 2 + 80} textAnchor="middle" fill={pal.muted} fontFamily={font.body} fontSize={34} opacity={eo(t, brandT + 0.5, 0.8)}>{p.teaser}</text>
    </svg>
  );
};

export const _unused = {mix, rand, W0};
