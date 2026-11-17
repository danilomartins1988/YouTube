import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * THUMBNAIL BUST (owner request 2026-11-16): a high-detail head-and-shoulders cartoon built to read at phone size.
 *
 * - Big expressive eyes (whites, coloured iris, pupil, two highlights, lids), thick sculpted brows, a mouth library,
 *   a thick outline, cel shading (shadow side) and a rim light on the outer edge.
 * - Expressions (`expr`): shock | smug (confident) | worry | point (an arm and hand reach into the frame) | laugh |
 *   happy | neutral.
 * - Traits: the same presets as CartoonStage's CARI caricature (huang, jassy, pichai, musk, sam, rob, penner,
 *   steuart, furner, trump), extended with age lines, beard, glasses, signature clothing and a cap, plus the sitcom
 *   cast (gloria, dash). `who` may also be a traits object; `traits` overrides fields of a preset.
 *
 * LIKENESS RULES (docs/PRODUCTION_STANDARD.md, "Real people"): a public figure is drawn ONLY as a respectful, original
 * flat cartoon, recognisable by signature traits (hair, clothes, glasses, skin tone, age). Never photo-traced, never
 * mocking a physical feature, nothing implying a crime, no logos. A private person is `who: 'silhouette'`.
 *
 * Local coordinates: origin at the bottom centre of the bust (the torso continues below y=0 and is meant to be cut by
 * the frame edge). The head is drawn at y=-890..-495 and scaled 1.22x about the chin, so on screen: crown ~-980 (cap
 * up to ~-1100), eyes -736, chin -497, shoulders -340, half-width 440. At scale 0.9 in a 1920x1080 frame with the
 * bottom at y=1090 the head and shoulders fill ~50% of the frame height.
 *
 * Used by: the `face` thumbnail archetype (remotion/src/thumbnails/FaceThumb.tsx), PunchThumb (`hero.kind: 'bust'`)
 * and CartoonStage (item `bust`, animated: blink, breathing, expression timeline, lip-flap).
 */
export const BOL = '#0B0B0F';

export type Expr = 'shock' | 'smug' | 'worry' | 'point' | 'laugh' | 'happy' | 'neutral';
export type BustTraits = {
  name?: string;
  hair?: 'swept' | 'side' | 'swoop' | 'bald' | 'short' | 'bun' | 'spiky' | 'none';
  hairColor?: string; hairShade?: string; brows?: string;
  skin?: string; iris?: string;
  clothes?: 'leather' | 'suit' | 'open' | 'shirt' | 'tee' | 'top';
  jacket?: string; shirt?: string; tie?: string | null;
  cap?: string | null; capFront?: string;
  glasses?: 'round' | 'rect' | false;
  age?: number;                       // 0..1: forehead lines, crow's feet, smile folds (never exaggerated)
  beard?: 'stubble' | 'full' | null;
  badge?: string; headset?: boolean; bags?: boolean;
};

/** presets: keys match CartoonStage CARI (+ sitcom cast). Signature traits only. */
export const BUST: Record<string, BustTraits> = {
  huang: {name: 'Jensen Huang', hair: 'swept', hairColor: '#B2B7BF', hairShade: '#5C626B', brows: '#3A3A40', skin: '#E3B48A', iris: '#3A2618',
    clothes: 'leather', jacket: '#18181C', shirt: '#25252A', age: 0.55, glasses: false},
  jassy: {name: 'Andy Jassy', hair: 'bald', hairColor: '#9A7A62', hairShade: '#6E5442', brows: '#6E5442', skin: '#E3AE86', iris: '#4A3424',
    clothes: 'open', jacket: '#2E3440', shirt: '#E9EEF3', age: 0.45},
  pichai: {name: 'Sundar Pichai', hair: 'side', hairColor: '#24201E', hairShade: '#4A4440', brows: '#1E1A18', skin: '#B98458', iris: '#2A1A10',
    clothes: 'open', jacket: '#2B3A55', shirt: '#D6E6F5', age: 0.25},
  musk: {name: 'Elon Musk', hair: 'short', hairColor: '#2B2420', hairShade: '#4A3E36', brows: '#2B2420', skin: '#EBC09C', iris: '#3E5A6E',
    clothes: 'tee', jacket: '#1C1C1E', shirt: '#1C1C1E', age: 0.35},
  sam: {name: 'Sam Walton', hair: 'side', hairColor: '#E6E8EC', hairShade: '#A9AEB6', brows: '#9EA3AA', skin: '#EDC4A0', iris: '#3E5A6E',
    clothes: 'open', jacket: '#4F7BA8', shirt: '#FFFFFF', cap: '#1F4E8C', capFront: '#F4F6F8', age: 0.85},
  rob: {name: 'Rob Walton', hair: 'side', hairColor: '#ECEDEF', hairShade: '#B0B4BA', brows: '#A4A8AE', skin: '#EDC4A0', iris: '#3E5A6E',
    clothes: 'suit', jacket: '#26344F', shirt: '#E9EEF3', tie: '#7A1F2B', age: 0.7},
  penner: {name: 'Greg Penner', hair: 'side', hairColor: '#5A4632', hairShade: '#3E3022', brows: '#4A3826', skin: '#EBC09C', iris: '#4A3424',
    clothes: 'suit', jacket: '#1F2A44', shirt: '#DCE8F5', tie: null, age: 0.3},
  steuart: {name: 'Steuart Walton', hair: 'swept', hairColor: '#6B4E33', hairShade: '#4A3522', brows: '#4A3522', skin: '#EBC09C', iris: '#4A3424',
    clothes: 'open', jacket: '#3B4A5E', shirt: '#FFFFFF', age: 0.25},
  furner: {name: 'John Furner', hair: 'side', hairColor: '#4A3B2E', hairShade: '#33281E', brows: '#33281E', skin: '#EBC09C', iris: '#4A3424',
    clothes: 'open', jacket: '#2E3440', shirt: '#E9EEF3', age: 0.35},
  trump: {name: 'Donald Trump', hair: 'swoop', hairColor: '#F2C94C', hairShade: '#C99A2E', brows: '#D9B26A', skin: '#F0BE96', iris: '#3E5A6E',
    clothes: 'suit', jacket: '#1F2A44', shirt: '#F4F7FB', tie: '#D32F2F', age: 0.7},
  // Ep 57 (Costco): signature traits only (hair colour, clothes); a plain first-name tag for Sinegal; no logos.
  vachris: {name: 'Ron Vachris', hair: 'short', hairColor: '#B9BEC6', hairShade: '#8A9099', brows: '#7E848C', skin: '#EBC09C', iris: '#3E5A6E',
    clothes: 'open', jacket: '#24324F', shirt: '#E9EEF3', age: 0.55},
  sinegal: {name: 'Jim Sinegal', hair: 'side', hairColor: '#F2F3F5', hairShade: '#C4C8CE', brows: '#B8BCC2', skin: '#EDC4A0', iris: '#3E5A6E',
    clothes: 'shirt', jacket: '#8FB3D9', shirt: '#8FB3D9', badge: 'JIM', age: 0.8},
  // sitcom cast (Episode 56), redrawn as busts: original characters
  gloria: {name: 'Gloria', hair: 'bun', hairColor: '#B5452B', hairShade: '#86301E', brows: '#7A2A1A', skin: '#F2C29A', iris: '#3E6E4A',
    clothes: 'top', jacket: '#D93A3A', shirt: '#FFFFFF', badge: 'MANAGER', headset: true, age: 0.15},
  dash: {name: 'Dash', hair: 'spiky', hairColor: '#17B3A3', hairShade: '#0E7A70', brows: '#0E7A70', skin: '#C98B5B', iris: '#3A2618',
    clothes: 'tee', jacket: '#FF8A1F', shirt: '#FF8A1F', badge: 'DEALS', bags: true, age: 0},
};

/* ------------------------------------------------------------------------------------------------ colour helpers */
const rgb = (h: string) => { const s = h.replace('#', ''); const n = s.length === 3 ? s.split('').map((c) => c + c).join('') : s;
  return [0, 2, 4].map((i) => parseInt(n.slice(i, i + 2), 16)); };
export const mix = (a: string, b: string, k: number) => { const A = rgb(a), B = rgb(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * k).toString(16).padStart(2, '0')).join(''); };
const shade = (c: string, k = 0.26) => mix(c, '#2A1020', k);
const lite = (c: string, k = 0.3) => mix(c, '#FFFFFF', k);

export type BustProps = {
  who?: string | BustTraits; traits?: BustTraits;
  expr?: Expr;
  /** open side of the composition (where text / prop are): +1 right, -1 left. Eyes look there, light comes from there. */
  dir?: 1 | -1;
  /** extra gaze offset [-1..1, -1..1] */
  look?: [number, number];
  /** point target in LOCAL coordinates (expr 'point'); default: towards `dir`, slightly up */
  point?: [number, number];
  rim?: string;            // rim light colour
  blink?: number;          // 0..1 (animation)
  talk?: number;           // 0..1 mouth openness while talking (animation)
  id?: string;             // unique prefix for clip paths
  outline?: number;        // outline width (default 9)
};

const HEAD = 'M -165 -700 C -170 -822 -98 -892 0 -892 C 98 -892 170 -822 165 -700 C 162 -606 128 -540 72 -508 Q 0 -478 -72 -508 C -128 -540 -162 -606 -165 -700 Z';
const TORSO = 'M -440 60 L -432 -170 Q -420 -296 -286 -338 L -100 -396 Q 0 -414 100 -396 L 286 -338 Q 420 -296 432 -170 L 440 60 Z';

/** brows: [inner y, outer y, arch control y] per side, for the side nearest the open direction (n) and the far one (f) */
const BROWS: Record<Expr, {n: [number, number, number]; f: [number, number, number]}> = {
  neutral: {n: [-772, -770, -790], f: [-772, -770, -790]},
  happy: {n: [-786, -780, -806], f: [-786, -780, -806]},
  point: {n: [-792, -784, -814], f: [-792, -784, -814]},
  shock: {n: [-812, -800, -846], f: [-812, -800, -846]},
  smug: {n: [-768, -770, -782], f: [-782, -796, -812]},
  worry: {n: [-806, -764, -800], f: [-806, -764, -800]},
  laugh: {n: [-800, -790, -824], f: [-800, -790, -824]},
};

export const Bust: React.FC<BustProps> = (p) => {
  const base = typeof p.who === 'string' ? (BUST[p.who] || {}) : (p.who || {});
  const sil = p.who === 'silhouette';
  const tr: BustTraits = sil ? {hair: 'side', hairColor: '#1A1A22', skin: '#1A1A22', clothes: 'suit', jacket: '#1A1A22', shirt: '#1A1A22'} : {...base, ...(p.traits || {})};
  const id = p.id || 'b';
  if (sil) {        // a private person: faceless dark shadow, no likeness, never named
    return <g opacity={0.95}>
      <path d={TORSO} fill="#16161E" stroke={BOL} strokeWidth={p.outline ?? 9} strokeLinejoin="round" />
      <path d="M -72 -540 L -76 -380 Q 0 -350 76 -380 L 72 -540 Z" fill="#16161E" />
      <g transform="translate(0 -480) scale(1.22) translate(0 480)">
        <path d={HEAD} fill="#16161E" stroke={BOL} strokeWidth={p.outline ?? 9} />
        <path d="M -170 -700 C -186 -830 -112 -916 -6 -918 C 104 -920 184 -846 170 -704 C 150 -780 90 -820 0 -824 C -90 -820 -150 -780 -170 -700 Z" fill="#0C0C12" />
        <text x={0} y={-600} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={220} fill="#9AA3B5">?</text>
      </g>
    </g>;
  }
  const ex: Expr = p.expr || 'happy';
  const d = p.dir ?? 1;
  const OLW = p.outline ?? 9;
  const outer = -d;     // shadow / rim side (away from the open side)
  const skin = tr.skin || '#E8B88F', skinS = shade(skin, 0.24), skinD = shade(skin, 0.42);
  const hc = tr.hairColor || '#3E2723', hs = tr.hairShade || shade(hc, 0.35);
  const jk = tr.jacket || '#37474F', sh = tr.shirt || '#FFFFFF';
  const iris = tr.iris || '#4A3424', browC = tr.brows || shade(hc, 0.3);
  const rim = mix(p.rim || '#FFFFFF', '#FFFFFF', 0.65);
  const age = tr.age ?? 0;
  const tilt = ex === 'smug' ? 4 * d : ex === 'laugh' ? -5 * d : ex === 'worry' ? -2 * d : ex === 'shock' ? -2 * d : 0;
  const lookX = clamp((p.look?.[0] ?? 0) + (ex === 'laugh' ? 0 : ex === 'shock' ? 0.15 * d : 0.55 * d), -1, 1);
  const lookY = clamp((p.look?.[1] ?? 0) + (ex === 'worry' ? -0.2 : ex === 'point' ? -0.15 : 0), -1, 1);
  const blink = p.blink ?? 0;

  /* ---------- eyes */
  const eyeR: Record<Expr, [number, number, number]> = {   // white rx, ry, iris r
    neutral: [44, 52, 26], happy: [44, 50, 28], point: [45, 52, 28], shock: [52, 64, 19], smug: [44, 50, 25], worry: [44, 54, 21], laugh: [44, 50, 25]};
  const [erx, ery, ir] = eyeR[ex];
  const lid = ex === 'smug' ? 0.46 : ex === 'worry' ? 0.12 : 0;
  const lower = ex === 'happy' || ex === 'point' ? 0.22 : ex === 'smug' ? 0.12 : 0;
  const eye = (cx: number, k: number) => {
    const ey = -690, near = Math.sign(cx) === d;
    if (ex === 'laugh' || blink > 0.6) {          // closed, happy arcs (laugh) or a blink line
      return <g key={'e' + k}>{ex === 'laugh'
        ? <path d={`M ${cx - 40} ${ey + 8} Q ${cx} ${ey - 42} ${cx + 40} ${ey + 8}`} stroke={BOL} strokeWidth={13} fill="none" strokeLinecap="round" />
        : <path d={`M ${cx - 42} ${ey} Q ${cx} ${ey + 16} ${cx + 42} ${ey}`} stroke={BOL} strokeWidth={10} fill="none" strokeLinecap="round" />}</g>;
    }
    const ix = cx + lookX * (erx - ir - 6), iy = ey + 4 + lookY * (ery - ir - 8);
    const cid = `${id}eye${k}`;
    const lidY = ey - ery + 2 * ery * (lid + (ex === 'smug' && !near ? -0.06 : 0));
    return <g key={'e' + k}>
      <clipPath id={cid}><ellipse cx={cx} cy={ey} rx={erx} ry={ery} /></clipPath>
      <ellipse cx={cx} cy={ey} rx={erx} ry={ery} fill="#FFFFFF" />
      <g clipPath={`url(#${cid})`}>
        <ellipse cx={cx} cy={ey + ery * 0.55} rx={erx} ry={ery * 0.5} fill="#DCE3EE" opacity={0.6} />
        <circle cx={ix} cy={iy} r={ir} fill={iris} stroke={BOL} strokeWidth={3} />
        <circle cx={ix} cy={iy + ir * 0.35} r={ir * 0.72} fill={lite(iris, 0.18)} opacity={0.55} />
        <circle cx={ix} cy={iy} r={ir * 0.52} fill={BOL} />
        <circle cx={ix - ir * 0.38} cy={iy - ir * 0.42} r={Math.max(5, ir * 0.32)} fill="#FFFFFF" />
        <circle cx={ix + ir * 0.4} cy={iy + ir * 0.38} r={Math.max(3, ir * 0.14)} fill="#FFFFFF" />
        {lid > 0 && <path d={`M ${cx - erx - 4} ${ey - ery - 4} L ${cx + erx + 4} ${ey - ery - 4} L ${cx + erx + 4} ${lidY + (ex === 'worry' ? (near ? 8 : -8) * d : 0)} L ${cx - erx - 4} ${lidY} Z`}
          fill={skinS} stroke={BOL} strokeWidth={7} strokeLinejoin="round" />}
        {lower > 0 && <ellipse cx={cx} cy={ey + ery * (1.55 - lower)} rx={erx * 1.2} ry={ery * 0.7} fill={skin} stroke={BOL} strokeWidth={6} />}
      </g>
      <ellipse cx={cx} cy={ey} rx={erx} ry={ery} fill="none" stroke={BOL} strokeWidth={OLW * 0.8} />
      <path d={`M ${cx - erx - 2} ${ey - 6} Q ${cx - erx * 0.6} ${ey - ery - 4} ${cx} ${ey - ery - 3} Q ${cx + erx * 0.7} ${ey - ery - 2} ${cx + erx + 4} ${ey - 14}`}
        stroke={BOL} strokeWidth={OLW * 1.35} fill="none" strokeLinecap="round" />
      {blink > 0 && blink <= 0.6 && <rect x={cx - erx - 4} y={ey - ery - 4} width={2 * erx + 8} height={(2 * ery + 8) * blink} fill={skinS} />}
    </g>;
  };

  /* ---------- brows: thick tapered shapes */
  const brow = (k: number) => {
    const sx = k === 0 ? -1 : 1, near = sx === d, b = BROWS[ex][near ? 'n' : 'f'];
    const ix = sx * 26, ox = sx * 118, mx = sx * 70;
    const [iy, oy, cy] = b;
    const top = `M ${ix} ${iy} Q ${mx} ${cy - 10} ${ox} ${oy}`;
    return <g key={'br' + k}>
      <path d={`${top} Q ${ox + sx * 6} ${oy + 14} ${ox - sx * 6} ${oy + 16} Q ${mx} ${cy + 18} ${ix} ${iy + 22} Q ${ix - sx * 8} ${iy + 11} ${ix} ${iy} Z`}
        fill={browC} stroke={BOL} strokeWidth={5} strokeLinejoin="round" />
    </g>;
  };

  /* ---------- mouth */
  const my = -566;
  const teeth = (y0: number, w: number, h: number) => <rect x={-w} y={y0} width={2 * w} height={h} fill="#FFFFFF" />;
  const talk = p.talk ?? 0;
  const mouth = (() => {
    const cid = `${id}mouth`;
    const open = (path: string, tY: number, tongueY: number, tongueR: [number, number]) => <g>
      <clipPath id={cid}><path d={path} /></clipPath>
      <path d={path} fill="#4A1416" />
      <g clipPath={`url(#${cid})`}>{teeth(tY - 30, 90, 30 + 18)}<ellipse cx={8 * d} cy={tongueY} rx={tongueR[0]} ry={tongueR[1]} fill="#E2606A" />
        <ellipse cx={8 * d} cy={tongueY - tongueR[1] * 0.4} rx={tongueR[0] * 0.5} ry={tongueR[1] * 0.25} fill="#F48A92" opacity={0.7} /></g>
      <path d={path} fill="none" stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
    </g>;
    switch (ex) {
      case 'shock': return open(`M -40 ${my - 26} Q 0 ${my - 48} 40 ${my - 26} Q 50 ${my + 30} 0 ${my + 52} Q -50 ${my + 30} -40 ${my - 26} Z`, my - 24, my + 40, [30, 18]);
      case 'laugh': return open(`M -86 ${my - 24} Q 0 ${my - 10} 86 ${my - 24} Q 78 ${my + 56} 0 ${my + 70} Q -78 ${my + 56} -86 ${my - 24} Z`, my - 6, my + 50, [44, 24]);
      case 'point': case 'happy': return open(`M -70 ${my - 20} Q 0 ${my - 6} 70 ${my - 20} Q 60 ${my + 42} 0 ${my + 50} Q -60 ${my + 42} -70 ${my - 20} Z`, my - 4, my + 34, [34, 18]);
      case 'smug': return <g>
        <path d={`M ${-58 * d} ${my - 4} Q ${-6 * d} ${my + 20} ${62 * d} ${my - 26}`} fill="none" stroke={BOL} strokeWidth={OLW * 1.2} strokeLinecap="round" />
        <path d={`M ${54 * d} ${my - 36} Q ${72 * d} ${my - 28} ${64 * d} ${my - 12}`} fill="none" stroke={BOL} strokeWidth={OLW * 0.8} strokeLinecap="round" />
        <path d={`M ${-50 * d} ${my + 26} Q ${0} ${my + 36} ${36 * d} ${my + 22}`} fill="none" stroke={skinD} strokeWidth={6} strokeLinecap="round" opacity={0.6} />
      </g>;
      case 'worry': {    // clenched-teeth grimace, corners down
        const path = `M -64 ${my - 6} Q -30 ${my - 22} 0 ${my - 16} Q 30 ${my - 10} 64 ${my - 20} Q 66 ${my + 14} 48 ${my + 24} Q 0 ${my + 16} -50 ${my + 28} Q -68 ${my + 18} -64 ${my - 6} Z`;
        return <g><path d={path} fill="#FFFFFF" stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
          <path d={`M -60 ${my + 6} Q 0 ${my + 2} 60 ${my + 2}`} stroke={BOL} strokeWidth={4} fill="none" />
          {[-36, -12, 12, 36].map((x) => <path key={x} d={`M ${x} ${my - 16} L ${x} ${my + 22}`} stroke={BOL} strokeWidth={3.5} />)}</g>;
      }
      default: {
        if (talk > 0.1) return open(`M -46 ${my - 12} Q 0 ${my - 4} 46 ${my - 12} Q 40 ${my + 14 + 36 * talk} 0 ${my + 20 + 36 * talk} Q -40 ${my + 14 + 36 * talk} -46 ${my - 12} Z`, my - 2, my + 12 + 30 * talk, [24, 12]);
        return <path d={`M -54 ${my - 8} Q 0 ${my + 22} 54 ${my - 8}`} fill="none" stroke={BOL} strokeWidth={OLW * 1.1} strokeLinecap="round" />;
      }
    }
  })();

  /* ---------- hair (front) */
  const strands = (lines: string[], c: string, w = 7, o = 0.9) => lines.map((l, k) => <path key={k} d={l} stroke={c} strokeWidth={w} fill="none" strokeLinecap="round" opacity={o} />);
  const hairFront = (() => {
    switch (tr.hair) {
      case 'swept': return <g>
        <path d="M -172 -690 C -200 -820 -184 -950 -56 -996 C 62 -1036 200 -980 198 -840 C 198 -776 186 -730 172 -692 C 170 -764 152 -818 112 -846 C 62 -880 -14 -888 -72 -870 C -128 -852 -162 -782 -172 -690 Z"
          fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        {strands(['M -120 -856 Q -120 -940 -40 -984', 'M -60 -872 Q -40 -956 50 -994', 'M 10 -880 Q 60 -950 140 -962', 'M 80 -862 Q 140 -910 186 -880', 'M -156 -800 Q -176 -880 -130 -940'], hs, 12)}
        {strands(['M -92 -884 Q -78 -950 -10 -980', 'M -20 -896 Q 20 -960 100 -974', 'M 120 -884 Q 166 -912 186 -900'], lite(hc, 0.6), 8, 0.9)}
      </g>;
      case 'side': return <g>
        <path d="M -170 -700 C -186 -830 -112 -916 -6 -918 C 104 -920 184 -846 170 -704 C 164 -756 150 -788 120 -806 C 80 -830 10 -834 -50 -826 Q -64 -812 -76 -812 C -110 -808 -146 -786 -156 -740 Z"
          fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -60 -824 Q -40 -880 -2 -912" stroke={hs} strokeWidth={8} fill="none" strokeLinecap="round" />
        {strands(['M -40 -830 Q 40 -880 140 -850', 'M -10 -860 Q 60 -894 128 -868', 'M -90 -820 Q -140 -840 -150 -780', 'M -110 -860 Q -150 -860 -160 -800'], hs, 7)}
        {strands(['M 10 -884 Q 56 -898 104 -882'], lite(hc, 0.35), 7, 0.7)}
      </g>;
      case 'short': return <g>
        <path d="M -168 -712 C -180 -836 -104 -906 0 -906 C 104 -906 180 -836 168 -712 C 160 -770 136 -800 100 -810 Q 0 -834 -100 -810 C -136 -800 -160 -770 -168 -712 Z"
          fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        {strands(['M -110 -820 Q -60 -870 0 -878', 'M 0 -840 Q 60 -872 120 -850', 'M -40 -828 Q 10 -850 50 -846'], hs, 7)}
      </g>;
      case 'swoop': return <g>
        <path d="M -174 -700 C -198 -864 -90 -934 24 -930 C 146 -926 206 -860 194 -778 C 190 -748 178 -730 168 -716 C 158 -786 120 -812 62 -818 C 0 -820 -66 -806 -114 -770 C -142 -748 -162 -724 -174 -700 Z"
          fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -130 -800 C -60 -860 80 -870 176 -820 C 150 -790 90 -800 40 -800 C -20 -800 -80 -790 -130 -800 Z" fill={lite(hc, 0.15)} stroke={BOL} strokeWidth={6} strokeLinejoin="round" />
        {strands(['M -100 -840 Q 0 -900 150 -860', 'M -60 -880 Q 40 -920 160 -880'], hs, 7)}
      </g>;
      case 'bald': return <g>
        {[-1, 1].map((s) => <path key={s} d={`M ${s * 160} -650 C ${s * 176} -700 ${s * 176} -760 ${s * 150} -800 C ${s * 140} -760 ${s * 128} -720 ${s * 126} -660 Z`} fill={hc} stroke={BOL} strokeWidth={OLW * 0.8} strokeLinejoin="round" />)}
        <path d="M -60 -860 Q 0 -880 50 -866" stroke="#FFFFFF" strokeWidth={14} opacity={0.35} strokeLinecap="round" fill="none" />
      </g>;
      case 'bun': return <g>
        <circle cx={-10} cy={-930} r={76} fill={hc} stroke={BOL} strokeWidth={OLW} />
        <path d="M -40 -990 L 40 -870" stroke="#FFC93C" strokeWidth={16} strokeLinecap="round" /><path d="M 30 -884 L 44 -862" stroke="#F48FB1" strokeWidth={16} strokeLinecap="round" />
        <path d="M -174 -690 C -196 -830 -110 -908 0 -908 C 110 -908 196 -830 174 -690 C 160 -760 110 -806 30 -808 Q 0 -790 -30 -808 C -110 -806 -160 -760 -174 -690 Z" fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        {strands(['M -20 -806 Q -80 -860 -150 -780', 'M 20 -806 Q 90 -860 150 -780'], hs, 7)}
      </g>;
      case 'spiky': return <g>
        <path d="M -170 -700 L -200 -830 L -126 -812 L -150 -930 L -64 -858 L -30 -980 L 22 -868 L 100 -960 L 104 -850 L 196 -880 L 160 -790 L 200 -760 L 168 -700 C 150 -770 100 -808 0 -812 C -90 -808 -150 -770 -170 -700 Z"
          fill={hc} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        {strands(['M -120 -820 L -136 -900', 'M -30 -830 L -30 -940', 'M 60 -830 L 96 -920'], lite(hc, 0.4), 8, 0.8)}
      </g>;
      default: return null;
    }
  })();
  const sideburns = tr.hair && tr.hair !== 'bald' && tr.hair !== 'spiky' && tr.hair !== 'bun' && tr.hair !== 'none'
    ? [-1, 1].map((s) => <path key={'sb' + s} d={`M ${s * 166} -730 Q ${s * 172} -680 ${s * 160} -640 L ${s * 146} -650 Q ${s * 150} -690 ${s * 148} -726 Z`} fill={hc} stroke={BOL} strokeWidth={5} strokeLinejoin="round" />) : null;

  /* ---------- clothes */
  const clothes = (() => {
    const lap = (s: number, c: string) => <path d={`M ${s * 96} -398 L ${s * 214} -318 L ${s * 168} -250 L ${s * 200} -200 L ${s * 140} 60 L ${s * 118} 60 L ${s * 96} -300 Z`} fill={c} stroke={BOL} strokeWidth={OLW * 0.8} strokeLinejoin="round" />;
    const collar = (s: number) => <path d={`M ${s * 8} -372 L ${s * 82} -420 L ${s * 120} -390 L ${s * 70} -312 Z`} fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />;
    switch (tr.clothes) {
      case 'leather': return <g>
        <path d={TORSO} fill={jk} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -104 -398 Q 0 -360 104 -398 L 150 60 L -150 60 Z" fill={sh} stroke={BOL} strokeWidth={OLW * 0.8} strokeLinejoin="round" />
        <path d="M -78 -396 Q 0 -350 78 -396" fill="none" stroke={shade(sh, 0.3)} strokeWidth={10} />
        {[-1, 1].map((s) => <g key={s}>
          <path d={`M ${s * 104} -404 L ${s * 250} -330 L ${s * 186} -252 L ${s * 230} -168 L ${s * 158} 60 L ${s * 128} 60 L ${s * 104} -300 Z`} fill={lite(jk, 0.08)} stroke={BOL} strokeWidth={OLW * 0.8} strokeLinejoin="round" />
          <path d={`M ${s * 130} 60 L ${s * 106} -300`} stroke="#8D9097" strokeWidth={5} strokeDasharray="10 8" />
          <path d={`M ${s * 300} -300 Q ${s * 360} -240 ${s * 380} -120`} stroke="#FFFFFF" strokeWidth={14} opacity={0.22} fill="none" strokeLinecap="round" />
          <path d={`M ${s * 220} -40 Q ${s * 260} -10 ${s * 300} -30`} stroke="#FFFFFF" strokeWidth={8} opacity={0.14} fill="none" strokeLinecap="round" />
          <path d={`M ${s * 340} -60 L ${s * 340} 60`} stroke={BOL} strokeWidth={4} opacity={0.5} />
        </g>)}
      </g>;
      case 'suit': return <g>
        <path d={TORSO} fill={jk} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -100 -398 Q 0 -370 100 -398 L 120 60 L -120 60 Z" fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} />
        {tr.tie && <path d="M 0 -360 L -30 -318 L -10 -290 L -36 60 L 36 60 L 10 -290 L 30 -318 Z" fill={tr.tie} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />}
        {tr.tie && <path d="M -30 -318 L 30 -318" stroke={BOL} strokeWidth={4} opacity={0.4} />}
        {[-1, 1].map((s) => <g key={s}>{collar(s)}{lap(s, shade(jk, 0.12))}</g>)}
      </g>;
      case 'open': return <g>
        <path d={TORSO} fill={jk} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -100 -398 Q 0 -370 100 -398 L 120 60 L -120 60 Z" fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} />
        <path d="M -46 -392 L 0 -318 L 46 -392 Z" fill={skinS} stroke={BOL} strokeWidth={5} strokeLinejoin="round" />
        <path d="M 0 -318 L 0 60" stroke={shade(sh, 0.25)} strokeWidth={4} />
        {[-250, -150, -50].map((y) => <circle key={y} cx={10} cy={y} r={6} fill={shade(sh, 0.3)} />)}
        {[-1, 1].map((s) => <g key={s}><path d={`M ${s * 46} -392 L ${s * 104} -420 L ${s * 130} -380 L ${s * 70} -300 Z`} fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />{lap(s, shade(jk, 0.12))}</g>)}
      </g>;
      case 'shirt': return <g>
        <path d={TORSO} fill={sh} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        <path d="M -46 -392 L 0 -318 L 46 -392 Z" fill={skinS} stroke={BOL} strokeWidth={5} />
        {[-1, 1].map((s) => <path key={s} d={`M ${s * 46} -392 L ${s * 104} -420 L ${s * 140} -370 L ${s * 70} -300 Z`} fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />)}
        <path d="M 0 -318 L 0 60" stroke={shade(sh, 0.25)} strokeWidth={4} />
        <rect x={-230} y={-250} width={110} height={100} rx={8} fill="none" stroke={shade(sh, 0.3)} strokeWidth={5} />
      </g>;
      case 'tee': case 'top': default: return <g>
        <path d={TORSO} fill={jk} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
        {tr.clothes === 'top' ? <path d="M -60 -398 L 0 -300 L 60 -398" fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />
          : <path d="M -96 -398 Q 0 -330 96 -398" fill="none" stroke={shade(jk, 0.3)} strokeWidth={18} strokeLinecap="round" />}
        {[-1, 1].map((s) => <path key={s} d={`M ${s * 290} -330 Q ${s * 330} -250 ${s * 320} -150`} stroke={shade(jk, 0.25)} strokeWidth={8} fill="none" opacity={0.6} />)}
      </g>;
    }
  })();
  const badge = tr.badge ? <g transform={`translate(${-210 * d} -170) rotate(${-4 * d})`}>
    <rect x={-104} y={-38} width={208} height={76} rx={12} fill="#FFF8E1" stroke={BOL} strokeWidth={OLW * 0.8} />
    <text x={0} y={16} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={Math.min(46, 172 / (tr.badge.length * 0.74))} fill={BOL}>{tr.badge}</text></g> : null;

  /* ---------- cap (front view, no logo) */
  const cap = tr.cap ? <g>
    <path d="M -178 -786 C -190 -930 -96 -992 0 -992 C 96 -992 190 -930 178 -786 Q 0 -820 -178 -786 Z" fill={tr.cap} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
    <path d="M -110 -800 C -118 -920 -60 -976 0 -978 C 60 -976 118 -920 110 -800 Q 0 -816 -110 -800 Z" fill={tr.capFront || tr.cap} stroke={BOL} strokeWidth={6} strokeLinejoin="round" />
    <path d="M 0 -978 L 0 -808" stroke={BOL} strokeWidth={3} opacity={0.3} />
    <circle cx={0} cy={-990} r={14} fill={tr.cap} stroke={BOL} strokeWidth={5} />
    <path d="M -196 -800 Q 0 -840 196 -800 Q 214 -780 192 -766 Q 0 -722 -192 -766 Q -214 -780 -196 -800 Z" fill={tr.cap} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
    <path d="M -150 -786 Q 0 -810 150 -786" stroke="#FFFFFF" strokeWidth={6} opacity={0.3} fill="none" strokeLinecap="round" />
    <path d={`M ${-150 * d} -900 Q ${-120 * d} -950 ${-60 * d} -968`} stroke="#FFFFFF" strokeWidth={10} opacity={0.25} fill="none" strokeLinecap="round" />
  </g> : null;

  /* ---------- glasses */
  const glasses = tr.glasses ? <g>
    {[-68, 68].map((x) => tr.glasses === 'round'
      ? <g key={x}><circle cx={x} cy={-690} r={66} fill="#CFE8FF" opacity={0.18} /><circle cx={x} cy={-690} r={66} fill="none" stroke={BOL} strokeWidth={OLW} />
        <path d={`M ${x - 36} ${-724} L ${x - 6} ${-750}`} stroke="#FFFFFF" strokeWidth={8} opacity={0.6} strokeLinecap="round" /></g>
      : <g key={x}><rect x={x - 68} y={-746} width={136} height={110} rx={24} fill="#CFE8FF" opacity={0.18} /><rect x={x - 68} y={-746} width={136} height={110} rx={24} fill="none" stroke={BOL} strokeWidth={OLW} />
        <path d={`M ${x - 40} ${-724} L ${x - 10} ${-740}`} stroke="#FFFFFF" strokeWidth={8} opacity={0.6} strokeLinecap="round" /></g>)}
    <path d="M -2 -700 Q 0 -716 2 -700" stroke={BOL} strokeWidth={OLW} fill="none" />
    <path d="M -134 -700 L -166 -706 M 134 -700 L 166 -706" stroke={BOL} strokeWidth={OLW * 0.8} />
  </g> : null;

  /* ---------- age lines, beard */
  const ageLines = age > 0.05 ? <g stroke={skinD} strokeWidth={5} fill="none" strokeLinecap="round" opacity={clamp(0.22 + age * 0.38, 0, 0.6)}>
    {age > 0.3 && !tr.cap && <path d="M -64 -830 Q 0 -842 64 -830" />}
    {age > 0.5 && !tr.cap && <path d="M -48 -806 Q 0 -816 48 -806" />}
    {[-1, 1].map((s) => <g key={s}>
      {age > 0.2 && <path d={`M ${s * 64} -588 Q ${s * 92} -566 ${s * 88} -530`} />}
      {age > 0.45 && ex !== 'laugh' && s !== outer && <path d={`M ${s * 128} -700 L ${s * 146} -708 M ${s * 126} -684 L ${s * 146} -680`} />}
      {age > 0.6 && s !== outer && <path d={`M ${s * 44} -628 Q ${s * 68} -622 ${s * 92} -632`} />}
    </g>)}
  </g> : null;
  const beard = tr.beard === 'full' ? <path d="M -158 -660 C -150 -560 -90 -490 0 -484 C 90 -490 150 -560 158 -660 C 130 -600 100 -560 60 -560 Q 0 -590 -60 -560 C -100 -560 -130 -600 -158 -660 Z" fill={hc} stroke={BOL} strokeWidth={OLW * 0.8} strokeLinejoin="round" />
    : tr.beard === 'stubble' ? <path d="M -150 -640 C -140 -560 -80 -496 0 -492 C 80 -496 140 -560 150 -640 C 110 -560 60 -540 0 -540 C -60 -540 -110 -560 -150 -640 Z" fill={hc} opacity={0.22} /> : null;

  /* ---------- head assembly */
  const hid = `${id}head`;
  const head = <g transform={`rotate(${tilt} 0 -500)`}>
    {/* ears */}
    {[-1, 1].map((s) => <g key={'ear' + s}><ellipse cx={s * 166} cy={-676} rx={32} ry={52} fill={s === outer ? skinS : skin} stroke={BOL} strokeWidth={OLW} />
      <path d={`M ${s * 160} -700 Q ${s * 180} -676 ${s * 162} -652`} stroke={skinD} strokeWidth={7} fill="none" strokeLinecap="round" /></g>)}
    <clipPath id={hid}><path d={HEAD} /></clipPath>
    <path d={HEAD} fill={skin} />
    <g clipPath={`url(#${hid})`}>
      {/* cel shade on the outer side + under the brow line + rim light */}
      <ellipse cx={outer * 250} cy={-690} rx={120} ry={320} fill={skinS} />
      <ellipse cx={0} cy={-470} rx={170} ry={40} fill={skinS} opacity={0.7} />
      <path d={HEAD} fill="none" stroke={rim} strokeWidth={14} opacity={0.55} transform={`translate(${-outer * 6} 0)`} clipPath={`url(#${hid}r)`} />
      {(ex === 'laugh' || ex === 'happy' || ex === 'point') && [-1, 1].map((s) => <ellipse key={'bl' + s} cx={s * 108} cy={-604} rx={34} ry={20} fill="#FF6F61" opacity={0.3} />)}
    </g>
    <clipPath id={`${hid}r`}><rect x={outer > 0 ? 120 : -400} y={-1000} width={280} height={600} /></clipPath>
    <path d={HEAD} fill="none" stroke={BOL} strokeWidth={OLW * 1.15} strokeLinejoin="round" />
    {beard}
    {ageLines}
    {/* nose */}
    <path d={`M ${6 * d} -664 Q ${26 * d} -618 ${14 * d} -598 Q ${0} -588 ${-16 * d} -598`} fill="none" stroke={BOL} strokeWidth={OLW * 0.8} strokeLinecap="round" strokeLinejoin="round" />
    <path d={`M ${-14 * d} -640 Q ${-24 * d} -616 ${-12 * d} -604`} fill="none" stroke={skinD} strokeWidth={6} strokeLinecap="round" opacity={0.6} />
    {eye(-68, 0)}{eye(68, 1)}
    {[0, 1].map((k) => brow(k))}
    {tr.bags && [-68, 68].map((x) => <path key={'bag' + x} d={`M ${x - 34} -620 Q ${x} -604 ${x + 34} -620`} stroke="#7A4A9A" strokeWidth={6} fill="none" opacity={0.55} strokeLinecap="round" />)}
    {mouth}
    {sideburns}
    {hairFront}
    {cap}
    {glasses}
    {tr.headset && <g><path d="M -186 -700 Q -200 -930 0 -940 Q 200 -930 186 -700" fill="none" stroke="#37474F" strokeWidth={14} />
      <rect x={-210} y={-730} width={42} height={84} rx={14} fill="#37474F" stroke={BOL} strokeWidth={6} />
      <path d="M -196 -650 Q -170 -560 -70 -560" fill="none" stroke="#37474F" strokeWidth={9} /><circle cx={-66} cy={-560} r={13} fill={BOL} /></g>}
    {ex === 'worry' && <path transform={`translate(${outer * -150} -800) rotate(${outer * -12})`} d="M 0 -40 Q 30 0 0 30 Q -30 0 0 -40 Z" fill="#8FDBFF" stroke={BOL} strokeWidth={6} />}
    {ex === 'shock' && <g stroke={BOL} strokeWidth={10} strokeLinecap="round">{[[-1, -0.6], [0, -1], [1, -0.6]].map(([a, b], k) =>
      <path key={k} d={`M ${a * 190} ${-930 + b * 20} L ${a * 240} ${-990 + b * 30}`} />)}</g>}
  </g>;

  /* ---------- pointing arm (in front of the torso) */
  const arm = ex === 'point' ? (() => {
    const tgt = p.point || [d * 900, -760];
    const S: [number, number] = [d * 290, -300];
    const Eb: [number, number] = [d * 430, -150];
    const vx = tgt[0] - Eb[0], vy = tgt[1] - Eb[1], L = Math.hypot(vx, vy) || 1;
    const fl = Math.min(330, Math.max(160, L - 340));
    const Wr: [number, number] = [Eb[0] + (vx / L) * fl, Eb[1] + (vy / L) * fl];
    const ang = (Math.atan2(vy, vx) * 180) / Math.PI;
    const path = `M ${S[0]} ${S[1]} Q ${Eb[0] + d * 20} ${Eb[1] + 30} ${Eb[0]} ${Eb[1]} L ${Wr[0]} ${Wr[1]}`;
    return <g>
      <path d={path} stroke={BOL} strokeWidth={122} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={path} stroke={tr.clothes === 'shirt' ? sh : jk} strokeWidth={104} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M ${Eb[0]} ${Eb[1] + 34} L ${Wr[0]} ${Wr[1] + 34}`} stroke={shade(tr.clothes === 'shirt' ? sh : jk, 0.3)} strokeWidth={22} opacity={0.5} strokeLinecap="round" />
      <g transform={`translate(${Wr[0]} ${Wr[1]}) rotate(${ang}) scale(1.25 ${d < 0 ? -1.25 : 1.25})`}>
        <rect x={-56} y={-58} width={58} height={116} rx={16} fill={tr.clothes === 'leather' || tr.clothes === 'tee' || tr.clothes === 'top' ? shade(jk, 0.1) : sh} stroke={BOL} strokeWidth={7} />
        <path d="M -6 -50 Q 60 -64 108 -46 Q 126 -6 110 46 Q 60 66 -6 56 Q -18 0 -6 -50 Z" fill={skin} stroke={BOL} strokeWidth={7} strokeLinejoin="round" />
        <rect x={84} y={-56} width={150} height={42} rx={21} fill={skin} stroke={BOL} strokeWidth={7} />
        <path d="M 212 -48 Q 224 -36 214 -24" stroke={skinD} strokeWidth={4} fill="none" opacity={0.6} />
        {[-10, 14, 36].map((y) => <rect key={y} x={78} y={y} width={52} height={24} rx={12} fill={skin} stroke={BOL} strokeWidth={6} />)}
        <path d="M 16 -20 Q 70 -30 118 -6 Q 132 6 116 16 Q 70 4 22 14 Z" fill={lite(skin, 0.08)} stroke={BOL} strokeWidth={6} strokeLinejoin="round" />
        <path d="M 0 40 Q 50 56 100 40" stroke={skinS} strokeWidth={10} fill="none" opacity={0.7} />
      </g>
    </g>;
  })() : null;

  /* ---------- torso shading + neck */
  const tid = `${id}torso`;
  return <g>
    <clipPath id={tid}><path d={TORSO} /></clipPath>
    {clothes}
    <g clipPath={`url(#${tid})`} style={{pointerEvents: 'none'}}>
      <path d={`M ${outer * 440} 60 L ${outer * 432} -170 Q ${outer * 420} -296 ${outer * 286} -338 L ${outer * 250} -350 Q ${outer * 320} -200 ${outer * 300} 60 Z`} fill="#000000" opacity={0.22} />
      <path d={TORSO} fill="none" stroke={rim} strokeWidth={20} opacity={0.55} transform={`translate(${-outer * 8} 6)`} clipPath={`url(#${hid}r2)`} />
    </g>
    <clipPath id={`${hid}r2`}><rect x={outer > 0 ? 300 : -460} y={-400} width={160} height={460} /></clipPath>
    {badge}
    <path d="M -72 -540 L -76 -380 Q 0 -350 76 -380 L 72 -540 Z" fill={skin} stroke={BOL} strokeWidth={OLW} strokeLinejoin="round" />
    <path d="M -72 -520 Q 0 -440 72 -520 L 72 -470 Q 0 -410 -72 -470 Z" fill={skinS} />
    {tr.clothes === 'suit' || tr.clothes === 'open' ? [-1, 1].map((s) => <path key={'cl' + s} d={`M ${s * 8} -372 L ${s * 82} -420 L ${s * 120} -390 L ${s * 70} -312 Z`} fill={sh} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />) : null}
    {tr.clothes === 'suit' && tr.tie && <path d="M -26 -372 L 26 -372 L 30 -326 L -30 -326 Z" fill={tr.tie} stroke={BOL} strokeWidth={OLW * 0.7} strokeLinejoin="round" />}
    {tr.clothes === 'leather' && <path d="M -78 -392 Q 0 -344 78 -392" fill="none" stroke={BOL} strokeWidth={6} />}
    <g transform="translate(0 -480) scale(1.22) translate(0 480)">{head}</g>
    {arm}
  </g>;
};

/* ------------------------------------------------------------------------------------------------ CartoonStage item */
type KF = number | [number, number][];
const kf = (v: KF | undefined, t: number, dflt = 0): number => {
  if (v === undefined) return dflt;
  if (!Array.isArray(v)) return v;
  if (!v.length) return dflt;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], v[i][0] - v[i - 1][0])));
  return v[v.length - 1][1];
};
const pick = <V,>(tl: any, t: number, dflt: V): V => { let v = dflt; if (Array.isArray(tl)) for (const [pt, pv] of tl) if (t >= Number(pt)) v = pv; return v; };

/**
 * CartoonStage item `bust` (same rules as `caricature`): who (preset | traits | 'silhouette'), traits, x/y keyframes
 * (bottom centre), scale (1 = 900 px tall), dir (+1 looks right), expr or exprs [[t, expr]], point [x, y] (stage coords),
 * talk [[t0, t1], ...] lip-flap windows, at/until (pop in / out), label + labelUntil (name tag on first appearance).
 */
export const bustItem = (a: any, {t, f}: {t: number; f: number}, i: number): React.ReactNode => {
  const at = a.at ?? 0;
  if (t < at || (a.until !== undefined && t > a.until + 0.35)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f), s = a.scale ?? 0.6;
  const app = t < at ? 0 : E.outBack(win(t, at, 0.4)) * (a.until !== undefined ? 1 - win(t, a.until, 0.35) : 1);
  const expr: Expr = pick(a.exprs, t, a.expr || 'happy');
  const ph = (t + i * 0.73) % 3.6, blink = ph < 0.14 ? Math.sin((ph / 0.14) * Math.PI) : 0;
  const talking = Array.isArray(a.talk) && a.talk.some((w: any) => t >= Number(w[0]) && t <= Number(w[1]));
  const talk = talking ? clamp(0.5 + 0.5 * Math.sin(t * 19 + i) * Math.sin(t * 6.7 + i * 2)) : 0;
  const breathe = Math.sin(t * 2 + i) * 4;
  const pt = a.point ? [(a.point[0] - x) / s, (a.point[1] - y) / s] as [number, number] : undefined;
  const lab: string | null = a.label && t < (a.labelUntil ?? at + 4) ? String(a.label) : null;
  return <g key={'bust' + i} transform={`translate(${x} ${y - breathe}) scale(${s * app})`}>
    <Bust who={a.who} traits={a.traits} expr={expr} dir={a.dir ?? 1} look={a.look} point={pt} rim={a.rim} blink={blink}
      talk={talking && (expr === 'neutral' || expr === 'happy' || expr === 'smug') ? talk : 0} id={`bi${i}`} />
    {lab && <g transform="translate(0 -1150)">
      <rect x={-lab.length * 17 - 30} y={-50} width={lab.length * 34 + 60} height={76} rx={38} fill="#FFFFFF" stroke={BOL} strokeWidth={8} />
      <text x={0} y={10} textAnchor="middle" fontFamily="Inter, sans-serif" fontWeight={900} fontSize={44} fill={BOL}>{lab}</text></g>}
  </g>;
};
