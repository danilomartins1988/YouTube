import React from 'react';
import {eio, eo, lerp, rand, useCtx} from '../lib/anim';
import {RiseText} from '../components/Chrome';

/**
 * Layered 2.5D North Sea scene. Independently moving parts: rolling wave layers (parallax), a platform
 * with a rotating crane, a flickering gas flare with heat haze, a pumping derrick block, blinking aviation
 * lights, a helicopter with spinning rotor flying in, a supply ship crossing, gulls, and an optional
 * pipeline whose oil 'pulses' travel towards shore. Variants via params.mode: night | dawn | storm.
 */
export const OilPlatform: React.FC = () => {
  const {t, W, H, pal, font, scene, cue} = useCtx();
  const p = scene.params;
  const night = p.mode !== 'dawn';
  const horizon = H * (p.horizon || 0.64);
  const cam = eio(t, 0, scene.duration) ; // slow camera push across the whole scene
  const camScale = 1 + 0.06 * cam;
  const camX = -60 * cam;

  const wave = (amp: number, len: number, speed: number, y: number, phase: number) => {
    let d = `M -100 ${H}`;
    for (let x = -100; x <= W + 100; x += 20) {
      const yy = y + Math.sin((x / len) * Math.PI * 2 + t * speed + phase) * amp + Math.sin((x / (len * 0.37)) + t * speed * 1.7) * amp * 0.3;
      d += ` L ${x} ${yy}`;
    }
    return d + ` L ${W + 100} ${H} Z`;
  };

  // platform geometry (world coords before camera)
  const px = W * (p.platform_x || 0.58), deck = horizon - 120;
  const craneAng = -25 + Math.sin(t * 0.35) * 28; // slow slewing crane
  const flare = 0.75 + 0.25 * Math.sin(t * 9) * Math.sin(t * 5.3 + 1);
  const blink = Math.floor(t * 1.2) % 2 === 0 ? 1 : 0.15;
  const drill = (t * 2) % 1; // travelling block

  // helicopter path (enters from right, settles over the helideck)
  const hu = eio(t, cue(p.heli_cue, 0.15), 6);
  const hx = lerp(W + 200, px + 150, hu), hy = lerp(horizon - 420, deck - 70, hu) + Math.sin(t * 2) * 4 * (1 - hu);
  const rotor = Math.sin(t * 40);

  // supply ship crossing
  const sx = ((t * 38 + 200) % (W + 600)) - 300;

  const sky = night ? [pal.bg, pal.bg2] : ['#1B2E4A', '#7A6A55'];
  const stars = night ? Array.from({length: 60}, (_, i) => (
    <circle key={i} cx={rand(i) * W} cy={rand(i + 9) * horizon * 0.8} r={rand(i + 3) * 1.6 + 0.4} fill={pal.ink}
      opacity={(0.2 + 0.5 * rand(i + 5)) * (0.6 + 0.4 * Math.sin(t * 2 + i))} />
  )) : null;

  const pulses = p.pipeline ? Array.from({length: 6}, (_, i) => {
    const u = ((t * 0.25 + i / 6) % 1);
    const x = lerp(px - 40, -50, u), y = lerp(horizon + 160, horizon + 230, u);
    return <circle key={i} cx={x} cy={y} r={6} fill={pal.accent} opacity={0.85 * eo(t, cue(p.pipeline_cue, 0.3), 0.6)} />;
  }) : null;

  return (
    <svg width={W} height={H}>
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={sky[0]} />
          <stop offset="100%" stopColor={sky[1]} />
        </linearGradient>
        <radialGradient id="flareGlow">
          <stop offset="0%" stopColor="#FFD27A" stopOpacity={0.9} />
          <stop offset="40%" stopColor={pal.accent} stopOpacity={0.35} />
          <stop offset="100%" stopColor={pal.accent} stopOpacity={0} />
        </radialGradient>
        <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={pal.land} />
          <stop offset="100%" stopColor={pal.bg} />
        </linearGradient>
      </defs>
      <rect width={W} height={H} fill="url(#sky)" />
      {stars}
      <g transform={`translate(${camX} 0) scale(${camScale})`} style={{transformOrigin: `${px}px ${horizon}px`}}>
        {/* distant platforms */}
        {[0.12, 0.27, 0.86].map((f, i) => (
          <g key={i} opacity={0.35} transform={`translate(${W * f} ${horizon - 30}) scale(0.28)`}>
            <rect x={-60} y={-80} width={120} height={20} fill={pal.border} />
            {[-50, 0, 50].map((lx) => <rect key={lx} x={lx - 4} y={-60} width={8} height={120} fill={pal.border} />)}
            <polygon points="10,-80 30,-80 20,-260" fill={pal.border} />
            <circle cx={50} cy={-130} r={10 + 4 * Math.sin(t * 7 + i)} fill={pal.accent} opacity={0.8} />
          </g>
        ))}
        <path d={wave(6, 380, 0.6, horizon, 0)} fill={pal.land} opacity={0.9} />
        {/* legs */}
        {[-150, -50, 50, 150].map((lx, i) => (
          <rect key={i} x={px + lx - 9} y={deck} width={18} height={horizon - deck + 260} fill={pal.border} />
        ))}
        <line x1={px - 150} y1={deck + 60} x2={px + 150} y2={deck + 150} stroke={pal.border} strokeWidth={6} />
        <line x1={px + 150} y1={deck + 60} x2={px - 150} y2={deck + 150} stroke={pal.border} strokeWidth={6} />
        {/* deck + modules */}
        <rect x={px - 220} y={deck - 26} width={440} height={30} fill={mixHex(pal.border, pal.ink, 0.15)} />
        <rect x={px - 200} y={deck - 110} width={170} height={84} fill={pal.border} />
        {Array.from({length: 6}, (_, i) => <rect key={i} x={px - 190 + i * 26} y={deck - 96} width={12} height={8} fill={pal.accent} opacity={0.5 + 0.5 * rand(i + Math.floor(t * 2))} />)}
        <rect x={px + 40} y={deck - 70} width={150} height={44} fill={pal.border} />
        {/* helideck */}
        <rect x={px + 90} y={deck - 84} width={130} height={12} fill={mixHex(pal.border, pal.ink, 0.25)} />
        {/* derrick with moving travelling block */}
        <polygon points={`${px - 10},${deck - 26} ${px + 40},${deck - 26} ${px + 20},${deck - 330}`} fill="none" stroke={mixHex(pal.border, pal.ink, 0.35)} strokeWidth={6} />
        {Array.from({length: 6}, (_, i) => {
          const y = deck - 26 - i * 50;
          const half = 25 - i * 3.5;
          return <line key={i} x1={px + 15 - half} y1={y} x2={px + 25 + half} y2={y - 50} stroke={mixHex(pal.border, pal.ink, 0.3)} strokeWidth={3} />;
        })}
        <rect x={px + 10} y={deck - 300 + 220 * drill} width={20} height={22} fill={pal.accent} />
        <circle cx={px + 20} cy={deck - 334} r={7} fill="#FF5A4A" opacity={blink} />
        {/* rotating crane */}
        <g transform={`translate(${px - 180} ${deck - 110}) rotate(${craneAng})`}>
          <rect x={-8} y={-6} width={16} height={40} fill={mixHex(pal.border, pal.ink, 0.35)} />
          <line x1={0} y1={0} x2={-210} y2={-120} stroke={pal.accent} strokeWidth={9} strokeLinecap="round" />
          <line x1={-210} y1={-120} x2={-210} y2={-40 + 20 * Math.sin(t)} stroke={pal.ink} strokeWidth={2} />
          <rect x={-222} y={-40 + 20 * Math.sin(t)} width={24} height={16} fill={pal.muted} />
        </g>
        {/* flare boom + flame */}
        <line x1={px + 190} y1={deck - 50} x2={px + 380} y2={deck - 230} stroke={mixHex(pal.border, pal.ink, 0.3)} strokeWidth={8} />
        <circle cx={px + 392} cy={deck - 246} r={120 * flare} fill="url(#flareGlow)" />
        <path d={`M ${px + 380} ${deck - 232} q ${10 + 8 * flare} ${-40 * flare} ${4} ${-70 * flare - 10} q ${18} ${30} ${12} ${70 * flare}`} fill="#FFD27A" opacity={0.95} />
        {/* gulls */}
        {Array.from({length: 4}, (_, i) => {
          const gx = ((t * (30 + i * 6) + i * 400) % (W + 200)) - 100, gy = horizon - 320 - i * 40 + Math.sin(t + i) * 10;
          const flap = Math.sin(t * 8 + i) * 8;
          return <path key={i} d={`M ${gx - 14} ${gy} q 7 ${-flap} 14 0 q 7 ${-flap} 14 0`} stroke={pal.ink} strokeWidth={2} fill="none" opacity={0.6} />;
        })}
        {/* helicopter */}
        <g transform={`translate(${hx} ${hy})`} opacity={eo(t, cue(p.heli_cue, 0.15), 0.6)}>
          <ellipse cx={0} cy={0} rx={46} ry={16} fill={pal.ink} />
          <rect x={30} y={-6} width={70} height={8} fill={pal.ink} />
          <rect x={96} y={-18} width={6} height={22} fill={pal.ink} />
          <line x1={-70 * rotor} y1={-20} x2={70 * rotor} y2={-20} stroke={pal.ink} strokeWidth={4} />
          <rect x={-4} y={-22} width={8} height={6} fill={pal.ink} />
          <circle cx={-30} cy={2} r={3} fill="#FF5A4A" opacity={blink} />
        </g>
        {/* supply ship */}
        <g transform={`translate(${sx} ${horizon + 60})`}>
          <polygon points="-90,0 90,0 70,26 -80,26" fill={pal.border} />
          <rect x={30} y={-34} width={44} height={34} fill={mixHex(pal.border, pal.ink, 0.25)} />
          <rect x={-80} y={-10} width={100} height={10} fill={pal.muted} />
        </g>
        <path d={wave(10, 260, 1.1, horizon + 90, 1.3)} fill={pal.land} opacity={0.7} />
        {pulses && <path d={`M ${px - 40} ${horizon + 160} L -50 ${horizon + 230}`} stroke={pal.border} strokeWidth={10} opacity={eo(t, cue(p.pipeline_cue, 0.3), 0.6)} />}
        {pulses}
        <path d={wave(16, 200, 1.6, horizon + 200, 2.1)} fill="url(#sea)" />
        {/* light reflection of the flare on the water */}
        {Array.from({length: 8}, (_, i) => (
          <rect key={i} x={px + 360 + Math.sin(t * 2 + i) * 20 - 30} y={horizon + 20 + i * 18} width={60 - i * 5} height={3} fill={pal.accent} opacity={0.25 * flare} />
        ))}
      </g>
      {/* text overlay */}
      {p.kicker && <RiseText x={120} y={210} at={cue(p.kicker_cue, 0)} size={28} color={pal.accent} weight={600} tracking={6}>{String(p.kicker).toUpperCase()}</RiseText>}
      {p.title && <RiseText x={120} y={300} at={cue(p.title_cue, 0.02)} size={84} weight={700} display>{p.title}</RiseText>}
      {p.value && <RiseText x={116} y={440} at={cue(p.value_cue, 0.2)} size={150} weight={700} display color={pal.accent}>{p.value}</RiseText>}
      {p.subtitle && <RiseText x={122} y={510} at={cue(p.subtitle_cue, 0.4)} size={38} color={pal.ink}>{p.subtitle}</RiseText>}
    </svg>
  );
};

export const mixHex = (a: string, b: string, u: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [x, y] = [p(a), p(b)];
  return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * u).toString(16).padStart(2, '0')).join('');
};
