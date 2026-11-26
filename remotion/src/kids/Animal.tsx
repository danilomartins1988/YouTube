import React from 'react';
import type {AnimalKind} from './theme';

/* Cute "chibi" animals drawn from big simple shapes. Local coordinates: head centred at (0,0), r~100,
 * feet at y~155. Everything is a pure function of the props (deterministic for Remotion). */

type Pal = {head: string; body: string; dark: string; light: string; feet: string};
const PAL: Record<AnimalKind, Pal> = {
  duck: {head: '#FFD93B', body: '#FFD93B', dark: '#FF9F1C', light: '#FFF3B0', feet: '#FF9F1C'},
  cat: {head: '#FFB054', body: '#FFB054', dark: '#E07B24', light: '#FFE2BF', feet: '#E07B24'},
  dog: {head: '#D29A6A', body: '#D29A6A', dark: '#8A5631', light: '#F6DDC4', feet: '#8A5631'},
  cow: {head: '#FFFFFF', body: '#FFFFFF', dark: '#3D3A4B', light: '#FFC2CF', feet: '#3D3A4B'},
  sheep: {head: '#FFE6D2', body: '#FFFFFF', dark: '#6E6A80', light: '#FFFFFF', feet: '#6E6A80'},
  chick: {head: '#FFE34D', body: '#FFE34D', dark: '#FF9F1C', light: '#FFF6B8', feet: '#FF9F1C'},
  pig: {head: '#FFB3C8', body: '#FFB3C8', dark: '#F27DA0', light: '#FFD3DF', feet: '#F27DA0'},
  frog: {head: '#73D86B', body: '#73D86B', dark: '#3FA535', light: '#D8F7C9', feet: '#3FA535'},
  bee: {head: '#FFD23F', body: '#FFD23F', dark: '#3D3A4B', light: '#FFF3B0', feet: '#3D3A4B'},
  monkey: {head: '#A86F4C', body: '#A86F4C', dark: '#7A4A2E', light: '#F4D3B3', feet: '#7A4A2E'},
};
const INK = '#2B2350';

export type AnimalProps = {
  kind: AnimalKind; x: number; y: number; scale?: number;
  bounce?: number;   // 0..1 hop height
  squash?: number;   // 0..1 landing squash
  mouth?: number;    // 0..1 open
  blink?: number;    // 0..1 closed
  clap?: number;     // 0..1 hands together
  wave?: number;     // 0..1 waving arm up
  waveT?: number;    // time for the wave wiggle
  tilt?: number;     // degrees
  look?: number;     // -1..1 pupils left/right
  flap?: number;     // wing phase for the bee
  opacity?: number;
};

const Eyes: React.FC<{y: number; dx: number; r: number; blink: number; look: number}> = ({y, dx, r, blink, look}) => (
  <g>
    {[-1, 1].map((s) => (
      <g key={s} transform={`translate(${s * dx} ${y}) scale(1 ${Math.max(0.08, 1 - blink)})`}>
        <ellipse rx={r} ry={r * 1.12} fill="#fff" stroke={INK} strokeWidth={4} />
        <circle cx={look * r * 0.3} cy={r * 0.12} r={r * 0.6} fill={INK} />
        <circle cx={look * r * 0.3 - r * 0.22} cy={-r * 0.15} r={r * 0.22} fill="#fff" />
      </g>
    ))}
  </g>
);

const Cheeks: React.FC<{y: number; dx: number}> = ({y, dx}) => (
  <g opacity={0.55}>
    <ellipse cx={-dx} cy={y} rx={17} ry={11} fill="#FF7E9D" />
    <ellipse cx={dx} cy={y} rx={17} ry={11} fill="#FF7E9D" />
  </g>
);

/** smile that opens into a round singing mouth */
const Mouth: React.FC<{y: number; w: number; open: number}> = ({y, w, open}) =>
  open > 0.08 ? (
    <g transform={`translate(0 ${y})`}>
      <ellipse rx={w * (0.55 + 0.15 * open)} ry={6 + 20 * open} fill="#7A1F3D" stroke={INK} strokeWidth={4} />
      <ellipse cy={8 + 9 * open} rx={w * 0.35} ry={4 + 7 * open} fill="#FF7E9D" />
    </g>
  ) : (
    <path d={`M ${-w} ${y - 4} Q 0 ${y + w * 0.9} ${w} ${y - 4}`} fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
  );

export const Animal: React.FC<AnimalProps> = (p) => {
  const {kind, scale = 1, bounce = 0, squash = 0, mouth = 0, blink = 0, clap = 0, wave = 0, waveT = 0, tilt = 0,
    look = 0, flap = 0, opacity = 1} = p;
  const c = PAL[kind];
  const lift = -bounce * 60;
  const sx = 1 + 0.07 * squash, sy = 1 - 0.07 * squash;
  const feet = kind !== 'bee';
  // hands: rest at the sides, clap -> in front, wave -> right hand up and wiggling
  const handY = 92 - 25 * clap;
  const lh: [number, number] = [-78 + 58 * clap, handY];
  const wv = wave * (Math.sin(waveT * 10) * 18);
  const rh: [number, number] = wave > 0.01 ? [78 + 40 * wave + wv, handY - 120 * wave] : [78 - 58 * clap, handY];
  const body = (
    <g>
      {feet && (
        <g>
          <ellipse cx={-36} cy={160} rx={30} ry={15} fill={c.feet} stroke={INK} strokeWidth={4} />
          <ellipse cx={36} cy={160} rx={30} ry={15} fill={c.feet} stroke={INK} strokeWidth={4} />
        </g>
      )}
      {kind === 'pig' && <path d="M 62 110 q 34 -6 26 -26 q -8 -16 -20 -2" fill="none" stroke={c.dark} strokeWidth={7} strokeLinecap="round" />}
      {kind === 'monkey' && <path d="M 60 120 q 70 10 62 -50 q -4 -26 -26 -18" fill="none" stroke={c.dark} strokeWidth={10} strokeLinecap="round" />}
      {kind === 'sheep' ? (
        <g>
          {[-50, -18, 18, 50].map((dx, i) => <circle key={i} cx={dx} cy={100 + (i % 2) * 14} r={40} fill="#fff" stroke={INK} strokeWidth={4} />)}
          <ellipse cx={0} cy={110} rx={62} ry={44} fill="#fff" />
        </g>
      ) : kind === 'bee' ? (
        <g>
          <ellipse cx={0} cy={100} rx={74} ry={60} fill={c.body} stroke={INK} strokeWidth={5} />
          <clipPath id="beeclip"><ellipse cx={0} cy={100} rx={72} ry={58} /></clipPath>
          <g clipPath="url(#beeclip)">
            <rect x={-80} y={88} width={160} height={18} fill={INK} />
            <rect x={-80} y={124} width={160} height={18} fill={INK} />
          </g>
          <path d="M 0 158 l -10 18 l 20 0 z" fill={INK} />
        </g>
      ) : (
        <ellipse cx={0} cy={102} rx={68} ry={58} fill={c.body} stroke={INK} strokeWidth={5} />
      )}
      {kind === 'cow' && <ellipse cx={-26} cy={100} rx={20} ry={15} fill={c.dark} />}
      {(kind === 'duck' || kind === 'chick') && (
        <g>
          <ellipse cx={0} cy={110} rx={40} ry={32} fill={c.light} opacity={0.8} />
        </g>
      )}
      {kind === 'bee' && (
        <g opacity={0.75}>
          {[-1, 1].map((s) => (
            <ellipse key={s} cx={s * 70} cy={40} rx={46} ry={26} fill="#E8F8FF" stroke={INK} strokeWidth={4}
              transform={`rotate(${s * (-30 + 18 * Math.sin(flap))} ${s * 30} 70)`} />
          ))}
        </g>
      )}
      {/* hands */}
      {kind !== 'bee' && [lh, rh].map(([hx, hy], i) => (
        <circle key={i} cx={hx} cy={hy} r={20} fill={kind === 'cow' || kind === 'sheep' ? c.dark : c.body} stroke={INK} strokeWidth={4} />
      ))}
    </g>
  );

  let head: React.ReactNode;
  const eyes = (y = -12, dx = 38, r = 24) => <Eyes y={y} dx={dx} r={r} blink={blink} look={look} />;
  switch (kind) {
    case 'duck':
    case 'chick': {
      const r = kind === 'chick' ? 92 : 100;
      head = (
        <g>
          <path d={`M -6 ${-r + 6} q -6 -38 14 -40 M 4 ${-r + 6} q 10 -30 28 -22`} fill="none" stroke={c.dark} strokeWidth={8} strokeLinecap="round" />
          <circle r={r} fill={c.head} stroke={INK} strokeWidth={5} />
          {eyes(-18, 36, 22)}
          <Cheeks y={26} dx={62} />
          {/* beak opens on singing */}
          <ellipse cx={0} cy={30 - 6 * mouth} rx={kind === 'chick' ? 24 : 40} ry={12} fill={c.dark} stroke={INK} strokeWidth={4} />
          <ellipse cx={0} cy={44 + 14 * mouth} rx={kind === 'chick' ? 18 : 32} ry={9} fill="#E8830F" stroke={INK} strokeWidth={4} />
        </g>
      );
      break;
    }
    case 'cat':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <g key={s}>
              <path d={`M ${s * 88} -30 L ${s * 82} -122 L ${s * 20} -88 Z`} fill={c.head} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
              <path d={`M ${s * 76} -48 L ${s * 74} -100 L ${s * 38} -82 Z`} fill="#FF9DB5" />
            </g>
          ))}
          <circle r={100} fill={c.head} stroke={INK} strokeWidth={5} />
          <path d="M -30 -98 l 8 22 M 0 -100 l 0 24 M 30 -98 l -8 22" stroke={c.dark} strokeWidth={8} strokeLinecap="round" />
          {eyes()}
          <Cheeks y={30} dx={64} />
          <path d="M -10 16 L 10 16 L 0 27 Z" fill="#FF6F91" stroke={INK} strokeWidth={3} strokeLinejoin="round" />
          {[-1, 1].map((s) => (
            <path key={s} d={`M ${s * 44} 28 l ${s * 60} -8 M ${s * 44} 38 l ${s * 60} 6`} stroke={INK} strokeWidth={3} strokeLinecap="round" />
          ))}
          <Mouth y={40} w={22} open={mouth} />
        </g>
      );
      break;
    case 'dog':
      head = (
        <g>
          <circle r={100} fill={c.head} stroke={INK} strokeWidth={5} />
          {[-1, 1].map((s) => (
            <ellipse key={s} cx={s * 92} cy={-10} rx={32} ry={64} fill={c.dark} stroke={INK} strokeWidth={5}
              transform={`rotate(${s * 18} ${s * 92} -60)`} />
          ))}
          <ellipse cx={34} cy={-26} rx={30} ry={26} fill={c.light} opacity={0.7} />
          {eyes()}
          <ellipse cx={0} cy={38} rx={50} ry={36} fill={c.light} stroke={INK} strokeWidth={4} />
          <ellipse cx={0} cy={18} rx={18} ry={12} fill={INK} />
          <Cheeks y={34} dx={66} />
          <Mouth y={48} w={20} open={mouth} />
        </g>
      );
      break;
    case 'cow':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <g key={s}>
              <path d={`M ${s * 44} -88 q ${s * 8} -40 ${s * 30} -44`} stroke="#F2E3B3" strokeWidth={16} strokeLinecap="round" fill="none" />
              <ellipse cx={s * 104} cy={-36} rx={34} ry={18} fill="#fff" stroke={INK} strokeWidth={4} transform={`rotate(${s * 20} ${s * 104} -36)`} />
            </g>
          ))}
          <circle r={100} fill={c.head} stroke={INK} strokeWidth={5} />
          <path d="M 30 -94 q 50 4 60 50 q -40 10 -60 -50 Z" fill={c.dark} />
          <ellipse cx={-56} cy={-30} rx={20} ry={16} fill={c.dark} />
          {eyes(-20, 36, 22)}
          <ellipse cx={0} cy={44} rx={64} ry={40} fill={c.light} stroke={INK} strokeWidth={4} />
          <ellipse cx={-20} cy={36} rx={8} ry={6} fill="#D9667F" />
          <ellipse cx={20} cy={36} rx={8} ry={6} fill="#D9667F" />
          <Mouth y={60} w={20} open={mouth} />
        </g>
      );
      break;
    case 'sheep':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <ellipse key={s} cx={s * 96} cy={-6} rx={36} ry={18} fill={c.dark} stroke={INK} strokeWidth={4} transform={`rotate(${s * 24} ${s * 96} -6)`} />
          ))}
          <ellipse rx={84} ry={92} cy={8} fill={c.head} stroke={INK} strokeWidth={5} />
          {[-60, -30, 0, 30, 60].map((dx, i) => <circle key={i} cx={dx} cy={-74 - (i % 2) * 12} r={34} fill="#fff" stroke={INK} strokeWidth={4} />)}
          <ellipse cx={0} cy={-60} rx={70} ry={26} fill="#fff" />
          {eyes(-4, 34, 21)}
          <Cheeks y={36} dx={52} />
          <Mouth y={48} w={18} open={mouth} />
        </g>
      );
      break;
    case 'pig':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <path key={s} d={`M ${s * 84} -40 L ${s * 92} -116 L ${s * 30} -90 Z`} fill={c.dark} stroke={INK} strokeWidth={5} strokeLinejoin="round" />
          ))}
          <circle r={100} fill={c.head} stroke={INK} strokeWidth={5} />
          {eyes(-24, 40, 22)}
          <Cheeks y={34} dx={70} />
          <ellipse cx={0} cy={18} rx={42} ry={28} fill={c.dark} stroke={INK} strokeWidth={4} />
          <ellipse cx={-14} cy={18} rx={7} ry={11} fill="#B8486B" />
          <ellipse cx={14} cy={18} rx={7} ry={11} fill="#B8486B" />
          <Mouth y={62} w={20} open={mouth} />
        </g>
      );
      break;
    case 'frog':
      head = (
        <g>
          <ellipse rx={112} ry={86} cy={6} fill={c.head} stroke={INK} strokeWidth={5} />
          {[-1, 1].map((s) => <circle key={s} cx={s * 50} cy={-66} r={40} fill={c.head} stroke={INK} strokeWidth={5} />)}
          <ellipse cx={0} cy={-30} rx={100} ry={30} fill={c.head} />
          <Eyes y={-68} dx={50} r={25} blink={blink} look={look} />
          <Cheeks y={24} dx={76} />
          {mouth > 0.08 ? <Mouth y={30} w={48} open={mouth} /> : (
            <path d="M -66 18 Q 0 70 66 18" fill="none" stroke={INK} strokeWidth={7} strokeLinecap="round" />
          )}
        </g>
      );
      break;
    case 'bee':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <g key={s}>
              <path d={`M ${s * 28} -86 q ${s * 10} -40 ${s * 34} -46`} fill="none" stroke={INK} strokeWidth={6} strokeLinecap="round" />
              <circle cx={s * 62} cy={-132} r={13} fill={INK} />
            </g>
          ))}
          <circle r={92} fill={c.head} stroke={INK} strokeWidth={5} />
          {eyes(-8, 34, 22)}
          <Cheeks y={34} dx={58} />
          <Mouth y={44} w={20} open={mouth} />
        </g>
      );
      break;
    case 'monkey':
      head = (
        <g>
          {[-1, 1].map((s) => (
            <g key={s}>
              <circle cx={s * 100} cy={-4} r={38} fill={c.head} stroke={INK} strokeWidth={5} />
              <circle cx={s * 100} cy={-4} r={22} fill={c.light} />
            </g>
          ))}
          <circle r={100} fill={c.head} stroke={INK} strokeWidth={5} />
          <path d="M 0 -8 C -30 -66 -96 -40 -76 10 C -70 62 -30 82 0 82 C 30 82 70 62 76 10 C 96 -40 30 -66 0 -8 Z" fill={c.light} />
          {eyes(-14, 34, 22)}
          <ellipse cx={-8} cy={24} rx={5} ry={4} fill={c.dark} />
          <ellipse cx={8} cy={24} rx={5} ry={4} fill={c.dark} />
          <Cheeks y={36} dx={56} />
          <Mouth y={50} w={24} open={mouth} />
        </g>
      );
      break;
  }

  return (
    <g transform={`translate(${p.x} ${p.y + lift * scale}) scale(${scale}) rotate(${tilt}) scale(${sx} ${sy})`} opacity={opacity}>
      <ellipse cx={0} cy={176 - lift} rx={80 * (1 - 0.3 * bounce)} ry={14} fill="#000" opacity={0.12} />
      {body}
      {head}
    </g>
  );
};
