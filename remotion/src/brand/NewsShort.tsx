import React from 'react';
import {AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from 'remotion';

/** Professional vertical "news explainer" Short (1080x1920) for the owner's pt-BR personal-brand channel.
 *  Real photos (free-licence, credited) with Ken Burns motion, cuts synced to the narration, a recreated news card
 *  with a highlighter, clean flat motion-graphics and one consistent caption style (2-3 words, key word highlighted).
 *  Audio is muxed afterwards (tools/make_pt_news_short.py). */

export type Word = {w: string; s: number; e: number; hl?: boolean};
export type Shot = {src: string; start: number; end: number; credit?: string;
  /** crop focus 0..1 in the source image and zoom range */ fx?: number; fy?: number; z0?: number; z1?: number; dx?: number; dy?: number; dim?: number};
export type Overlay =
  | {kind: 'news'; start: number; end: number; outlet: string; date: string; headline: string; highlight: string}
  | {kind: 'badge'; start: number; end: number; big: string; small?: string}
  | {kind: 'lower'; start: number; end: number; title: string; sub?: string}
  | {kind: 'timeline'; start: number; end: number; steps: {at: number; month: string; label: string}[]}
  | {kind: 'label'; start: number; end: number; text: string; tone?: 'warn' | 'info'}
  | {kind: 'end'; start: number; end: number; lines: string[]; date: string; sources: string};
export type NewsShortProps = {words: Word[]; shots: Shot[]; overlays: Overlay[]; lead: number; accent?: string};

const W = 1080, H = 1920, PH = 1920;   // full-height photo (blurred Fill stays behind as a safety layer for crossfades)
const FONT = 'Inter, "Inter Display", Arial, sans-serif';
const INK = '#0B1220';

const ease = Easing.bezier(0.22, 1, 0.36, 1);
const win = (t: number, a: number, d: number) => Math.min(1, Math.max(0, (t - a) / d));

const Photo: React.FC<{shot: Shot; t: number; fps: number}> = ({shot, t}) => {
  const u = win(t, shot.start, Math.max(0.1, shot.end - shot.start));
  const z = (shot.z0 ?? 1.0) + ((shot.z1 ?? 1.12) - (shot.z0 ?? 1.0)) * u;
  const fadeIn = interpolate(t, [shot.start, shot.start + 0.18], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // source images are 2:1 landscape (1600x800); cover the photo band, keep the focus point centred
  const scaleToBand = PH / 800, iw = 1600 * scaleToBand * z, ih = PH * z;
  const fx = shot.fx ?? 0.5, fy = shot.fy ?? 0.5;
  let x = W / 2 - iw * fx + (shot.dx ?? 0) * u, y = PH / 2 - ih * fy + (shot.dy ?? 0) * u;
  x = Math.min(0, Math.max(W - iw, x)); y = Math.min(0, Math.max(PH - ih, y));
  return <div style={{position: 'absolute', left: 0, top: 0, width: W, height: PH, overflow: 'hidden', opacity: fadeIn}}>
    <Img src={staticFile(shot.src)} style={{position: 'absolute', left: x, top: y, width: iw, height: ih, objectFit: 'cover',
      filter: `brightness(${1 - (shot.dim ?? 0.12)}) saturate(1.05) contrast(1.05)`}} />
    {shot.credit && <div style={{position: 'absolute', right: 28, top: 150, fontFamily: FONT, fontSize: 22, color: 'rgba(255,255,255,0.78)',
      textShadow: '0 1px 3px rgba(0,0,0,0.8)', letterSpacing: 0.3}}>{shot.credit}</div>}
  </div>;
};

/** Blurred full-frame copy of the current photo: no empty/dark areas anywhere in the 9:16 frame. */
const Fill: React.FC<{shot: Shot; t: number}> = ({shot, t}) => {
  const u = win(t, shot.start, Math.max(0.1, shot.end - shot.start));
  const s = 1.15 + 0.08 * u, ih = H * s, iw = ih * 2;
  return <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, overflow: 'hidden'}}>
    <Img src={staticFile(shot.src)} style={{position: 'absolute', left: W / 2 - iw * (shot.fx ?? 0.5), top: (H - ih) / 2, width: iw, height: ih,
      objectFit: 'cover', filter: 'blur(38px) brightness(0.5) saturate(1.2)'}} />
  </div>;
};

const Captions: React.FC<{words: Word[]; t: number; accent: string}> = ({words, t, accent}) => {
  // group into chunks of up to 3 words, breaking at punctuation
  const chunks: Word[][] = []; let cur: Word[] = [];
  const endP = (w?: Word) => !!w && /[.?!]$/.test(w.w);
  words.forEach((w, k) => { cur.push(w);
    const brk = /[.,?!:;]$/.test(w.w);
    const nextEnds = endP(words[k + 1]) && cur.length === 3 && !brk;            // pull a sentence's last word into this chunk
    if (brk || (cur.length >= 3 && !nextEnds) || cur.length >= 4) { chunks.push(cur); cur = []; } });
  if (cur.length) chunks.push(cur);
  const c = chunks.find((ch, i) => t >= ch[0].s && t < (chunks[i + 1] ? chunks[i + 1][0].s : ch[ch.length - 1].e + 0.4));
  if (!c) return null;
  const pop = interpolate(t, [c[0].s, c[0].s + 0.12], [0.92, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // fit: the longest word must fit the 900 px text column (~0.7 em per uppercase glyph); lines wrap, centred
  const longest = Math.max(...c.map((w) => w.w.replace(/[,;:.?!]$/, '').length));
  const fs = Math.max(56, Math.min(84, Math.floor(900 / (0.72 * longest))));
  return <div style={{position: 'absolute', left: 90, right: 90, top: 1230, display: 'flex', flexWrap: 'wrap', justifyContent: 'center',
    columnGap: 20, rowGap: 0, transform: `scale(${pop})`}}>
    {c.map((w, i) => { const on = t >= w.s - 0.02;
      return <span key={i} style={{fontFamily: FONT, fontWeight: 900, fontSize: fs, lineHeight: 1.1, letterSpacing: -1,
        color: w.hl ? accent : '#FFFFFF', opacity: on ? 1 : 0.38, textShadow: '0 4px 14px rgba(0,0,0,0.7), 0 0 2px rgba(0,0,0,0.8)',
        textTransform: 'uppercase', whiteSpace: 'nowrap'}}>{w.w.replace(/[,;:]$/, '')}</span>; })}
  </div>;
};

const NewsCard: React.FC<{o: Extract<Overlay, {kind: 'news'}>; t: number; fps: number; accent: string}> = ({o, t, fps}) => {
  const f = Math.round((t - o.start) * fps);
  const inS = spring({frame: f, fps, config: {damping: 16, stiffness: 140}});
  const out = interpolate(t, [o.end - 0.25, o.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const hiU = ease(win(t, o.start + 0.45, 0.7));
  const i = o.headline.indexOf(o.highlight);
  const pre = i >= 0 ? o.headline.slice(0, i) : o.headline, mid = i >= 0 ? o.highlight : '', post = i >= 0 ? o.headline.slice(i + mid.length) : '';
  return <div style={{position: 'absolute', left: 70, right: 70, top: 380, opacity: out,
    transform: `translateY(${(1 - inS) * 160}px) rotate(${(1 - inS) * -2}deg)`}}>
    <div style={{background: '#FFFFFF', borderRadius: 26, padding: '38px 44px 40px', boxShadow: '0 30px 80px rgba(0,0,0,0.45)'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, fontFamily: FONT, fontSize: 28, fontWeight: 800, color: '#5A6478', letterSpacing: 1}}>
        <div style={{width: 12, height: 12, borderRadius: 6, background: '#E53935'}} />{o.outlet.toUpperCase()} · {o.date}
      </div>
      <div style={{marginTop: 20, fontFamily: FONT, fontSize: 56, fontWeight: 850, lineHeight: 1.18, color: INK, letterSpacing: -0.5}}>
        {pre}
        <span style={{backgroundImage: 'linear-gradient(#FFE066, #FFE066)', backgroundRepeat: 'no-repeat', backgroundPosition: '0 85%',
          backgroundSize: `${hiU * 100}% 62%`, WebkitBoxDecorationBreak: 'clone', boxDecorationBreak: 'clone', padding: '0 6px', margin: '0 -6px'}}>{mid}</span>
        {post}
      </div>
      <div style={{marginTop: 22, fontFamily: FONT, fontSize: 24, color: '#8A93A6'}}>Manchete reproduzida como citação</div>
    </div>
  </div>;
};

const Badge: React.FC<{o: Extract<Overlay, {kind: 'badge'}>; t: number; fps: number; accent: string}> = ({o, t, fps, accent}) => {
  const f = Math.round((t - o.start) * fps), s = spring({frame: f, fps, config: {damping: 13, stiffness: 170}});
  const out = interpolate(t, [o.end - 0.2, o.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', left: 0, right: 0, top: 470, display: 'flex', justifyContent: 'center', opacity: out}}>
    <div style={{transform: `scale(${0.6 + 0.4 * s})`, background: accent, borderRadius: 30, padding: '26px 54px', textAlign: 'center',
      boxShadow: '0 24px 60px rgba(0,0,0,0.4)'}}>
      <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 150, lineHeight: 1, color: INK, letterSpacing: -4}}>{o.big}</div>
      {o.small && <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 36, color: INK, marginTop: 8, letterSpacing: 2}}>{o.small}</div>}
    </div>
  </div>;
};

const Lower: React.FC<{o: Extract<Overlay, {kind: 'lower'}>; t: number; accent: string}> = ({o, t, accent}) => {
  const u = ease(win(t, o.start, 0.45)), out = interpolate(t, [o.end - 0.25, o.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'absolute', left: 60, top: 860, opacity: out, transform: `translateX(${(1 - u) * -120}px)`}}>
    <div style={{display: 'flex', alignItems: 'stretch'}}>
      <div style={{width: 12, background: accent, borderRadius: 4, transform: `scaleY(${u})`}} />
      <div style={{background: 'rgba(11,18,32,0.88)', padding: '22px 30px', borderRadius: '0 16px 16px 0'}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 64, color: '#FFFFFF', letterSpacing: -0.5}}>{o.title}</div>
        {o.sub && <div style={{fontFamily: FONT, fontWeight: 600, fontSize: 32, color: '#C9D3E6', marginTop: 4}}>{o.sub}</div>}
      </div>
    </div>
  </div>;
};

const Timeline: React.FC<{o: Extract<Overlay, {kind: 'timeline'}>; t: number; fps: number; accent: string}> = ({o, t, fps, accent}) => {
  const out = interpolate(t, [o.end - 0.3, o.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const inU = ease(win(t, o.start, 0.4));
  const X0 = 150, X1 = 930, Y = 700;
  const done = o.steps.filter((s) => t >= s.at).length;
  const lineU = done <= 1 ? 0 : (done - 1) / (o.steps.length - 1);
  const lastAt = o.steps[Math.max(0, done - 1)]?.at ?? o.start;
  const lineNow = lineU - (1 - ease(win(t, lastAt, 0.45))) * (done > 1 ? 1 / (o.steps.length - 1) : 0);
  return <div style={{position: 'absolute', left: 0, top: 0, width: W, height: H, opacity: out * inU}}>
    <div style={{position: 'absolute', left: 70, right: 70, top: Y - 230, height: 470, borderRadius: 34, background: 'rgba(11,18,32,0.86)',
      border: '2px solid rgba(255,255,255,0.10)', boxShadow: '0 30px 80px rgba(0,0,0,0.45)'}} />
    <div style={{position: 'absolute', left: 0, right: 0, top: Y - 190, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 34,
      letterSpacing: 3, color: '#C9D3E6'}}>CBS · COMO FICARIA (PROPOSTA)</div>
    <div style={{position: 'absolute', left: X0, width: X1 - X0, top: Y - 4, height: 8, borderRadius: 4, background: 'rgba(255,255,255,0.18)'}} />
    <div style={{position: 'absolute', left: X0, width: (X1 - X0) * Math.max(0, lineNow), top: Y - 4, height: 8, borderRadius: 4, background: accent}} />
    {o.steps.map((s, i) => { const x = X0 + ((X1 - X0) * i) / (o.steps.length - 1), f = Math.round((t - s.at) * fps);
      const sp = t >= s.at ? spring({frame: f, fps, config: {damping: 14, stiffness: 170}}) : 0;
      return <div key={i}>
        <div style={{position: 'absolute', left: x - 30, top: Y - 30, width: 60, height: 60, borderRadius: 30, transform: `scale(${0.4 + 0.6 * sp})`,
          background: sp > 0.05 ? accent : 'rgba(255,255,255,0.25)', boxShadow: sp > 0.05 ? `0 0 30px ${accent}` : 'none'}} />
        <div style={{position: 'absolute', left: x - 170, width: 340, top: Y - 120, textAlign: 'center', fontFamily: FONT, fontWeight: 900,
          fontSize: 58, color: '#FFFFFF', opacity: 0.25 + 0.75 * sp, transform: `translateY(${(1 - sp) * 20}px)`}}>{s.month}</div>
        <div style={{position: 'absolute', left: x - 170, width: 340, top: Y + 52, textAlign: 'center', fontFamily: FONT, fontWeight: 800,
          fontSize: 32, letterSpacing: 1, color: sp > 0.05 ? accent : 'rgba(255,255,255,0.4)', opacity: 0.25 + 0.75 * sp}}>{s.label}</div>
      </div>; })}
  </div>;
};

const Label: React.FC<{o: Extract<Overlay, {kind: 'label'}>; t: number; fps: number}> = ({o, t, fps}) => {
  const f = Math.round((t - o.start) * fps), s = spring({frame: f, fps, config: {damping: 15, stiffness: 160}});
  const out = interpolate(t, [o.end - 0.25, o.end], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const warn = (o.tone ?? 'warn') === 'warn', col = warn ? '#FF5A4E' : '#4FC3F7';
  return <div style={{position: 'absolute', left: 0, right: 0, top: 560, display: 'flex', justifyContent: 'center', opacity: out}}>
    <div style={{transform: `scale(${0.85 + 0.15 * s}) translateY(${(1 - s) * 40}px)`, background: 'rgba(11,18,32,0.9)', border: `5px solid ${col}`,
      borderRadius: 24, padding: '30px 46px', textAlign: 'center', boxShadow: '0 24px 60px rgba(0,0,0,0.45)'}}>
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 30, letterSpacing: 3, color: col}}>{warn ? 'ATENÇÃO' : 'INFO'}</div>
      <div style={{fontFamily: FONT, fontWeight: 900, fontSize: 64, color: '#FFFFFF', marginTop: 6, letterSpacing: -0.5, lineHeight: 1.1}}>{o.text}</div>
    </div>
  </div>;
};

const EndCard: React.FC<{o: Extract<Overlay, {kind: 'end'}>; t: number; accent: string}> = ({o, t, accent}) => {
  const u = ease(win(t, o.start, 0.5));
  return <AbsoluteFill style={{opacity: u}}>
    <AbsoluteFill style={{background: 'rgba(11,18,32,0.82)'}} />
    <div style={{position: 'absolute', left: 90, right: 90, top: 640 + (1 - u) * 40, textAlign: 'center'}}>
      <div style={{width: 120, height: 8, borderRadius: 4, background: accent, margin: '0 auto 40px'}} />
      {o.lines.map((l, i) => <div key={i} style={{fontFamily: FONT, fontWeight: i ? 600 : 900, fontSize: i ? 40 : 62, color: i ? '#C9D3E6' : '#FFFFFF',
        lineHeight: 1.2, marginBottom: 14}}>{l}</div>)}
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 36, color: accent, marginTop: 36}}>{o.date}</div>
      <div style={{fontFamily: FONT, fontWeight: 500, fontSize: 28, color: '#AEB6C6', marginTop: 28, lineHeight: 1.4, whiteSpace: 'pre-line'}}>{o.sources}</div>
    </div>
  </AbsoluteFill>;
};

const Background: React.FC<{t: number}> = ({t}) => <AbsoluteFill style={{background: `linear-gradient(180deg, #0E1A33 0%, #0B1220 100%)`}}>
  <div style={{position: 'absolute', left: -300 + 60 * Math.sin(t * 0.4), top: 1150, width: 1700, height: 900, borderRadius: '50%',
    background: 'radial-gradient(closest-side, rgba(255,210,63,0.10), rgba(255,210,63,0))'}} />
</AbsoluteFill>;

export const NewsShort: React.FC<NewsShortProps> = ({words, shots, overlays, lead, accent = '#FFD23F'}) => {
  const frame = useCurrentFrame(), {fps} = useVideoConfig();
  const t = frame / fps, ta = t - lead;   // ta = narration clock
  const shot = [...shots].reverse().find((s) => ta >= s.start) || shots[0];
  const prev = shots[shots.indexOf(shot) - 1];
  return <AbsoluteFill style={{backgroundColor: '#0B1220'}}>
    <Background t={t} />
    <Fill shot={shot} t={ta} />
    {prev && ta < shot.start + 0.2 && <Photo shot={prev} t={ta} fps={fps} />}
    <Photo shot={shot} t={ta} fps={fps} />
    {/* photo band fades into the caption area */}
    <div style={{position: 'absolute', left: 0, top: 1150, width: W, height: 420, background: 'linear-gradient(180deg, rgba(11,18,32,0) 0%, rgba(11,18,32,0.78) 45%, rgba(11,18,32,0) 100%)'}} />
    <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 260, background: 'linear-gradient(180deg, rgba(11,18,32,0.55), rgba(11,18,32,0))'}} />
    {/* thin progress bar */}
    <div style={{position: 'absolute', left: 0, top: 0, height: 8, width: `${Math.min(1, t / (useVideoConfig().durationInFrames / fps)) * 100}%`, background: accent}} />
    {overlays.map((o, i) => (ta >= o.start && ta <= o.end) && (
      o.kind === 'news' ? <NewsCard key={i} o={o} t={ta} fps={fps} accent={accent} />
        : o.kind === 'badge' ? <Badge key={i} o={o} t={ta} fps={fps} accent={accent} />
          : o.kind === 'lower' ? <Lower key={i} o={o} t={ta} accent={accent} />
            : o.kind === 'timeline' ? <Timeline key={i} o={o} t={ta} fps={fps} accent={accent} />
              : o.kind === 'label' ? <Label key={i} o={o} t={ta} fps={fps} />
                : o.kind === 'end' ? <EndCard key={i} o={o} t={ta} accent={accent} /> : null))}
    {!overlays.some((o) => o.kind === 'end' && ta >= o.start) && <Captions words={words} t={ta} accent={accent} />}
  </AbsoluteFill>;
};

/** Cover/thumbnail for a news Short (1080x1920): full-bleed photo, hook headline in the safe middle, badge, label. */
export const NewsCover: React.FC<{src: string; fx?: number; credit?: string; kicker: string; lines: string[]; hl: string[]; tag?: string; accent?: string}> =
  ({src, fx = 0.5, credit, kicker, lines, hl, tag, accent = '#FFD23F'}) => {
    const iw = H * 2;
    return <AbsoluteFill style={{backgroundColor: '#0B1220', overflow: 'hidden'}}>
      <Img src={staticFile(src)} style={{position: 'absolute', top: 0, left: W / 2 - iw * fx, width: iw, height: H, objectFit: 'cover', filter: 'brightness(0.62) saturate(1.1)'}} />
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(11,18,32,0.55) 0%, rgba(11,18,32,0.1) 30%, rgba(11,18,32,0.25) 55%, rgba(11,18,32,0.85) 100%)'}} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 560}}>
        <div style={{display: 'inline-block', background: accent, color: '#0B1220', fontFamily: FONT, fontWeight: 900, fontSize: 40, letterSpacing: 2,
          padding: '10px 22px', borderRadius: 10}}>{kicker}</div>
        {lines.map((l, i) => <div key={i} style={{fontFamily: FONT, fontWeight: 900, fontSize: 118, lineHeight: 1.02, letterSpacing: -3, marginTop: i ? 0 : 26,
          color: hl.includes(l) ? accent : '#FFFFFF', textShadow: '0 6px 24px rgba(0,0,0,0.6)', textTransform: 'uppercase'}}>{l}</div>)}
        {tag && <div style={{display: 'inline-block', marginTop: 40, border: '5px solid #FF5A4E', color: '#FFFFFF', background: 'rgba(11,18,32,0.85)',
          fontFamily: FONT, fontWeight: 900, fontSize: 48, padding: '14px 26px', borderRadius: 16}}>{tag}</div>}
      </div>
      {credit && <div style={{position: 'absolute', right: 40, bottom: 330, fontFamily: FONT, fontWeight: 600, fontSize: 24, color: 'rgba(255,255,255,0.75)'}}>{credit}</div>}
    </AbsoluteFill>;
  };
