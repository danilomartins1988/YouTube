import React from 'react';
import {E, clamp, lerp, win} from '../motion';

/**
 * ANT IPO kit for CartoonStage (Episode 72, "Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble?").
 *
 * Prime-time TV-cartoon GENRE, day scenes, everything ORIGINAL: no logos, no brand marks, no real photos. Companies appear only as
 * plain text plaques; the company is shown through its ticker "ANT". Cast: JUNE (fictional nurse from Ohio, shared `toon` rig) and her
 * ONE SHARE (item `share`, a golden ticket with a face). Public figures use the shared `caricature` item (respectful traits only).
 * Sets:
 *  - ajkitchen: June's kitchen in Ohio by day: window on a leafy street, fridge, coffee, a big tablet on a stand showing the broker app
 *    (`app` [[t, title]], `price` KF number, `chart` KF 0..1 intraday line progress, `pill` [[t, text]]).
 *  - ajmarket: the stock-market plaza by day: a tall tower with a giant curved screen (ticker ANT, `price` KF, `chart` KF 0..1), a crawl
 *    (`crawl` [[t, text]]), a podium bell that rings at `ring`, a crowd of anonymous silhouettes (`crowd` KF 0..1).
 *  - ajlab: a modest 2021 research office: whiteboard of network sketches, desks, plants, door plaque (`plaque`), a big monitor with a
 *    chat that types (`chat` [[t, text]]), boxes of hardware.
 *  - ajrocket: the revenue rocket on a pad (`lift` KF 0..1), an altitude ruler with flags (`marks` [[label, frac]]) that pop as the rocket
 *    passes, smoke, a golden ticket strapped on (`ticket`).
 *  - ajhall: a bright compute hall: racks with blinking lights, ducts, and THE DOLLAR MACHINE: a coin drops in (`coins` rate), cost bricks
 *    come out; a big gauge "COMPUTE COST PER $1 OF SALES" (`cost` KF 0..2, `costText` [[t, text]]).
 *  - ajscroll: a long warehouse where a contract scroll unrolls across the years (`unroll` KF 0..1, `years` [labels]), crates of CHIPS /
 *    DATA CENTERS / POWER stack along it, a NON-CANCELABLE stamp (`stamp` t).
 *  - ajloop: THE MONEY LOOP (signature): AMAZON cloud building (left), ANTHROPIC / ANT tower (centre), BUSINESSES (right), GOOGLE (top
 *    right, `google` KF 0..1). Flows (KF 0..1 each): `invest` (Amazon → Anthropic), `pay` (Anthropic → Amazon), `compute` (Amazon →
 *    Anthropic), `resell` (businesses → Amazon → Anthropic, minus a cut), `stake` (Amazon's stake meter), `gloop` (Google loop),
 *    `spin` (highlight ring around the loop). Labels: `labels` overrides.
 *  - ajsupply: the round table of the concurrent private placement: seven plaques around the ANT tower (`reveal` KF 0..7), each flips to its
 *    supplier role (`flip` KF 0..7), coins flow in and chips flow back (`flow` KF 0..1).
 *  - ajcase: the detective's corkboard of who owns what: cards (`cards` [[t, label]]), red strings (`strings` KF 0..1), a sweeping
 *    magnifier (`lens` KF x), a PAPER GAIN stamp (`paper` t).
 *  - ajvault: the lockup vault: a round door with a day counter (`days` KF), share stacks behind bars, a queue of anonymous silhouettes,
 *    `crack` KF 0..1 (door ajar, a trickle), `open` KF 0..1, `sign`.
 *  - ajroads: THE FORK (signature): a plaza where several roads leave: the bright road up to a sunlit hill city, the middle road to a
 *    plain town, the dark road down to a storm cliff. `focus` [[t, 0..3]] (0 all, 1 bright, 2 middle, 3 dark) lights one road and dims
 *    the others; `walk` KF 0..1 moves the share along the focused road. Weather follows the focus.
 *  - ajgold: a gold-rush river valley: anonymous prospectors pan for gold, a SHOVEL SHOP sells CHIPS / CLOUD / POWER, coins flow to the
 *    shop (`flow` KF 0..1), `twice` t shows PAID TWICE.
 *  - ajtitle / ajbumper: title card (a ticker board flips to ANT, a rising line that bends into a warning sign) and chapter bumpers (a golden
 *    share ticket stamps down; `act`, `title`, `caption`, `color`).
 * Items: share (the golden ticket: `x`/`y` KF, `scale`, `mood` [[t, happy|wow|worry|calm]], `label`, `labelUntil`).
 * All motion is a pure function of t (seconds). Registered in CartoonStage.tsx (SETS / ITEMS / INDOOR).
 */
const OL = '#1A2238';
const FONT = 'Inter, sans-serif';
type KF = number | [number, number][];
type Z = {set: string; x0: number; x1: number; [k: string]: any};
type Ctx = {t: number; f: number};
type Item = {kind: string; x?: KF; y?: KF; at?: number; until?: number; scale?: number; [k: string]: any};
type SetFn = (t: number, z: Z, f: number) => React.ReactNode;
type ItemFn = (a: Item, c: Ctx, i: number) => React.ReactNode;

const rnd = (i: number) => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
const kf = (v: KF | undefined, t: number, d = 0): number => {
  if (v === undefined || v === null) return d;
  if (!Array.isArray(v)) return Number(v);
  if (!v.length) return d;
  if (t <= v[0][0]) return v[0][1];
  for (let i = 1; i < v.length; i++) if (t <= v[i][0]) return lerp(v[i - 1][1], v[i][1], E.inOut(win(t, v[i - 1][0], Math.max(0.001, v[i][0] - v[i - 1][0]))));
  return v[v.length - 1][1];
};
const pick = <V,>(tl: any, t: number, d: V): V => { let v = d; if (Array.isArray(tl)) for (const [pt, pv] of tl) if (t >= Number(pt)) v = pv; return v; };
const pop = (t: number, at = 0, d = 0.45) => (t < at ? 0 : E.outBack(win(t, at, d)));
const fit = (txt: string, w: number, s: number) => Math.min(s, (w / Math.max(1, txt.length)) / 0.6);
const T: React.FC<{x: number; y: number; s: number; c?: string; w?: number; a?: 'middle' | 'start' | 'end'; children: React.ReactNode; o?: number; ls?: number; st?: string; sw?: number}> =
  ({x, y, s, c = OL, w = 900, a = 'middle', children, o, ls, st, sw}) =>
    <text x={x} y={y} textAnchor={a} fontFamily={FONT} fontWeight={w} fontSize={s} fill={c} opacity={o} letterSpacing={ls}
      stroke={st} strokeWidth={sw} paintOrder={st ? 'stroke' : undefined} strokeLinejoin="round">{children}</text>;

const BLUE = '#2F6FDB', GOLD = '#E8A317', GOLD2 = '#FFD45C', RED = '#E5483B', GREEN = '#2E9E6B', TEAL = '#1F8A8C', NAVY = '#1A2238', ORANGE = '#F08A24',
  PURPLE = '#7357C9', CY = '#29C5F6', PAPER = '#FFFDF4', LEAF = '#3E9B4F', GREY = '#9AA6B8';

const sky = (z: Z, f: number, top: string, bot: string, id: string) => <g>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={top} /><stop offset="100%" stopColor={bot} /></linearGradient></defs>
  <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={2500 + f} fill={`url(#${id})`} /></g>;
const cloud = (x: number, y: number, s: number, k: any, c = '#FFFFFF') => <path key={'ac' + k} transform={`translate(${x} ${y}) scale(${s})`}
  d="M -90 20 Q -100 -20 -50 -20 Q -30 -60 20 -40 Q 70 -60 90 -10 Q 120 20 80 30 L -80 30 Q -110 30 -90 20 Z" fill={c} stroke={OL} strokeWidth={4} opacity={0.95} />;
const plaque = (x: number, y: number, txt: string, c = '#FFFFFF', s = 22, tc = OL) => { const w = Math.max(120, txt.length * s * 0.64 + 34);
  return <g transform={`translate(${x} ${y})`}><rect x={-w / 2} y={-s * 1.05} width={w} height={s * 1.6} rx={10} fill={c} stroke={OL} strokeWidth={4} /><T x={0} y={s * 0.25} s={s} c={tc}>{txt}</T></g>; };
const ground = (z: Z, f: number, c = '#A6D08A', c2 = '#88B86C') => <g><rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill={c} /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={14} fill={c2} stroke={OL} strokeWidth={4} /></g>;
const tree = (x: number, y: number, s: number, k: any, c = LEAF) => <g key={'tr' + k} transform={`translate(${x} ${y}) scale(${s})`}><rect x={-10} y={-90} width={20} height={90} fill="#8A6236" stroke={OL} strokeWidth={4} />
  <circle cy={-130} r={70} fill={c} stroke={OL} strokeWidth={5} /><circle cx={-40} cy={-110} r={40} fill="#4FB360" stroke={OL} strokeWidth={4} /></g>;
const coin = (x: number, y: number, s: number, k: any, c = GOLD2, txt = '$') => <g key={'cn' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <ellipse rx={24} ry={24} fill={c} stroke={OL} strokeWidth={4} /><ellipse rx={15} ry={15} fill="none" stroke={OL} strokeWidth={2} opacity={0.4} /><T x={0} y={9} s={24} c={OL}>{txt}</T></g>;
const chipTok = (x: number, y: number, s: number, k: any) => <g key={'ch' + k} transform={`translate(${x} ${y}) scale(${s})`}>
  <rect x={-22} y={-22} width={44} height={44} rx={6} fill="#263238" stroke={OL} strokeWidth={3} /><rect x={-12} y={-12} width={24} height={24} rx={3} fill={CY} />
  {[-14, 0, 14].map((q) => <path key={q} d={`M ${q} -22 L ${q} -30 M ${q} 22 L ${q} 30 M -22 ${q} L -30 ${q} M 22 ${q} L 30 ${q}`} stroke={OL} strokeWidth={3} />)}</g>;
const ppl = (x: number, y: number, s: number, k: number, t: number, sil = false) => { const sw = Math.sin(t * 6 + k) * 8, c = sil ? '#5E6B85' : [BLUE, ORANGE, TEAL, '#E86A92', GREEN, PURPLE, GOLD][k % 7];
  return <g key={'pp' + k} transform={`translate(${x} ${y}) scale(${s})`}><path d={`M -10 0 L ${-12 + sw} -60 M 10 0 L ${12 - sw} -60`} stroke={sil ? '#4A5570' : '#34406A'} strokeWidth={12} strokeLinecap="round" />
    <rect x={-26} y={-140} width={52} height={86} rx={20} fill={c} stroke={sil ? 'none' : OL} strokeWidth={4} /><circle cy={-168} r={26} fill={sil ? '#4A5570' : ['#8D5A3B', '#F1C27D', '#C68642', '#E0AC69', '#5C3A21'][k % 5]} stroke={sil ? 'none' : OL} strokeWidth={4} /></g>; };
// a path that rises fast then fades: the first-day price line (normalised 0..1 in x)
const DAY = [[0, 83], [0.05, 83], [0.12, 111.5], [0.18, 115.1], [0.3, 108], [0.45, 101], [0.6, 103], [0.75, 96.5], [0.9, 98.4], [1, 97.17]];
const dayPath = (w: number, h: number, u: number, lo = 78, hi = 118) => { let d = ''; const n = 60;
  for (let i = 0; i <= n; i++) { const x = (i / n) * u; let k = 1; while (k < DAY.length - 1 && DAY[k][0] < x) k++;
    const a = DAY[k - 1], b = DAY[k], v = lerp(a[1], b[1], clamp((x - a[0]) / Math.max(0.001, b[0] - a[0])));
    d += `${i ? ' L' : 'M'} ${(x * w).toFixed(1)} ${(h - ((v - lo) / (hi - lo)) * h).toFixed(1)}`; }
  return d; };
const money = (v: number) => (v > 0 ? '$' + v.toFixed(2) : '');
/** a curved pipe between two points with tokens travelling along it (computed positions, no CSS motion) */
const pipe = (a: [number, number], b: [number, number], bend: number, w: number, c: string, t: number, on: number, k: any, tok: 'coin' | 'chip' = 'coin', label?: string, lc = c) => {
  if (on <= 0.01) return null;
  const mx = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, my = (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend;
  const d = `M ${a[0]} ${a[1]} Q ${mx} ${my} ${b[0]} ${b[1]}`, grow = clamp(on * 1.25);
  const P = (u: number): [number, number] => [(1 - u) * (1 - u) * a[0] + 2 * (1 - u) * u * mx + u * u * b[0], (1 - u) * (1 - u) * a[1] + 2 * (1 - u) * u * my + u * u * b[1]];
  const lp = P(0.5);
  return <g key={'pi' + k}>
    <path d={d} stroke={OL} strokeWidth={w + 8} fill="none" strokeLinecap="round" pathLength={1} strokeDasharray={`${grow} 1`} />
    <path d={d} stroke={c} strokeWidth={w} fill="none" strokeLinecap="round" pathLength={1} strokeDasharray={`${grow} 1`} />
    {grow >= 1 && Array.from({length: 4}, (_, q) => { const u = (t * 0.3 + q / 4) % 1, p = P(u);
      return tok === 'coin' ? coin(p[0], p[1], 0.85, k + 'c' + q) : chipTok(p[0], p[1], 0.7, k + 'h' + q); })}
    {label && grow >= 1 && <g transform={`translate(${lp[0]} ${lp[1]}) scale(${E.outBack(clamp((on - 0.8) * 5))})`}>{plaque(0, -40, label, '#FFFFFF', 22, lc === GOLD2 ? OL : lc)}</g>}
  </g>; };

const building = (x: number, f: number, w: number, h: number, c: string, name: string, k: any, roof: 'flat' | 'cloud' | 'tower' = 'flat', glow = 0) => <g key={'bd' + k}>
  {glow > 0 && <ellipse cx={x} cy={f - h / 2} rx={w * 0.9} ry={h * 0.7} fill={GOLD2} opacity={0.25 * glow} />}
  <rect x={x - w / 2} y={f - h} width={w} height={h} rx={8} fill={c} stroke={OL} strokeWidth={6} />
  {Array.from({length: Math.floor((h - 120) / 70)}, (_, r) => Array.from({length: Math.max(1, Math.floor((w - 40) / 60))}, (_, q) =>
    <rect key={r + '-' + q} x={x - w / 2 + 24 + q * 60} y={f - h + 90 + r * 70} width={36} height={40} rx={4} fill="#DDEBFA" stroke={OL} strokeWidth={2.5} opacity={0.9} />))}
  {roof === 'cloud' && <path transform={`translate(${x} ${f - h - 10}) scale(${w / 300})`} d="M -120 10 Q -130 -40 -70 -40 Q -50 -90 10 -70 Q 70 -100 100 -40 Q 150 -30 130 10 Z" fill="#FFFFFF" stroke={OL} strokeWidth={5} />}
  {roof === 'tower' && <path d={`M ${x - w / 2 + 20} ${f - h} L ${x} ${f - h - 90} L ${x + w / 2 - 20} ${f - h} Z`} fill={c} stroke={OL} strokeWidth={6} />}
  {plaque(x, f - 30, name, '#FFFFFF', 26)}
</g>;

const RAW: Record<string, SetFn> = {
  /** June's kitchen, Ohio, by day */
  ajkitchen: (t, z, f) => {
    const app: string = pick(z.app, t, 'MY PORTFOLIO'), price = kf(z.price, t, 0), ch = kf(z.chart, t, 0), pill: string = pick(z.pill, t, '');
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#FCEFD9" />
      {Array.from({length: 30}, (_, k) => <rect key={'tile' + k} x={z.x0 + k * 140} y={560} width={136} height={70} fill={k % 2 ? '#FFFFFF' : '#EAF4F4'} stroke="#D7E3E3" strokeWidth={2} />)}
      {/* window on a leafy street */}
      <g transform="translate(120 110)"><rect x={0} y={0} width={620} height={420} rx={14} fill="#BFE6F7" stroke={OL} strokeWidth={7} />
        <clipPath id="ajwin"><rect x={6} y={6} width={608} height={408} rx={10} /></clipPath>
        <g clipPath="url(#ajwin)">{[0, 1].map((k) => cloud(120 + k * 330 + ((t * 8) % 200), 80, 0.6, 'kw' + k))}
          <rect x={0} y={300} width={620} height={120} fill="#A6D08A" /><path d="M 0 330 L 620 330" stroke="#88B86C" strokeWidth={6} />
          {[0, 1, 2].map((k) => <g key={'hs' + k} transform={`translate(${80 + k * 200} 300)`}><rect x={-60} y={-90} width={120} height={90} fill={['#F5B7A3', '#A3C9F5', '#F5E3A3'][k]} stroke={OL} strokeWidth={4} />
            <path d="M -70 -90 L 0 -150 L 70 -90 Z" fill="#B04A3A" stroke={OL} strokeWidth={4} /><rect x={-14} y={-46} width={28} height={46} fill="#7A4B2A" stroke={OL} strokeWidth={3} /></g>)}
          {tree(560, 320, 0.8, 'kt', '#E08A2E')}{tree(20, 330, 0.7, 'kt2', '#D9A441')}</g>
        <path d="M 310 0 L 310 420 M 0 210 L 620 210" stroke={OL} strokeWidth={6} /></g>
      {/* fridge */}
      <g transform="translate(1720 1040)"><rect x={-120} y={-700} width={240} height={700} rx={20} fill="#F2F5F8" stroke={OL} strokeWidth={6} /><path d="M -120 -420 L 120 -420" stroke={OL} strokeWidth={5} />
        <rect x={86} y={-640} width={14} height={140} rx={7} fill={GREY} stroke={OL} strokeWidth={3} /><rect x={86} y={-380} width={14} height={140} rx={7} fill={GREY} stroke={OL} strokeWidth={3} />
        {[[-60, -600, RED], [10, -560, BLUE], [-40, -500, GOLD]].map(([x, y, c], k) => <circle key={k} cx={x as number} cy={y as number} r={14} fill={c as string} stroke={OL} strokeWidth={3} />)}
        <rect x={-80} y={-650} width={110} height={80} fill="#FFFFFF" stroke={OL} strokeWidth={3} transform="rotate(-6)" /><T x={-28} y={-602} s={14} c={OL}>NIGHT SHIFT</T></g>
      {/* counter */}
      <rect x={z.x0} y={760} width={z.x1 - z.x0} height={40} fill="#C9A27A" stroke={OL} strokeWidth={5} /><rect x={z.x0} y={800} width={z.x1 - z.x0} height={300} fill="#8FB8C9" stroke={OL} strokeWidth={5} />
      {Array.from({length: 14}, (_, k) => <rect key={'cab' + k} x={z.x0 + 40 + k * 300} y={830} width={260} height={180} rx={8} fill="#A5C9D8" stroke={OL} strokeWidth={4} />)}
      <g transform="translate(560 760)"><rect x={-34} y={-70} width={68} height={70} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={5} /><path d="M 34 -54 Q 64 -40 34 -18" stroke={OL} strokeWidth={6} fill="none" />
        {[0, 1].map((q) => <path key={q} d={`M ${-10 + q * 20} -84 Q ${-20 + q * 20 + Math.sin(t * 2 + q) * 8} -110 ${-10 + q * 20} -136`} stroke="#B0BEC5" strokeWidth={5} fill="none" opacity={0.7} />)}</g>
      {/* tablet with the app */}
      <g transform="translate(1180 470)"><rect x={-330} y={-250} width={660} height={460} rx={34} fill="#263238" stroke={OL} strokeWidth={7} />
        <rect x={-300} y={-222} width={600} height={404} rx={18} fill="#FFFFFF" />
        <rect x={-300} y={-222} width={600} height={64} rx={18} fill={BLUE} /><T x={-276} y={-178} s={28} c="#FFFFFF" a="start">{app}</T>
        <g transform="translate(-270 -132)"><rect x={0} y={0} width={96} height={56} rx={12} fill={GOLD2} stroke={OL} strokeWidth={3} /><T x={48} y={39} s={30} c={OL}>ANT</T></g>
        <T x={270} y={-88} s={60} c={OL} a="end">{money(price)}</T>
        <g transform="translate(-270 -50)"><path d="M 0 180 L 540 180" stroke="#CFD8E3" strokeWidth={3} />
          {/* offer-price reference line */}<path d={`M 0 ${180 - ((83 - 78) / 40) * 180} L 540 ${180 - ((83 - 78) / 40) * 180}`} stroke={GREY} strokeWidth={3} strokeDasharray="10 8" />
          <T x={540} y={180 - ((83 - 78) / 40) * 180 - 8} s={18} c="#5E6B85" a="end">OFFER $83</T>
          {ch > 0 && <path d={dayPath(540, 180, ch)} stroke={GREEN} strokeWidth={7} fill="none" strokeLinejoin="round" strokeLinecap="round" />}</g>
        {pill && <g transform="translate(0 160)">{plaque(0, 0, pill, '#E9F7EF', 22, GREEN)}</g>}
        <rect x={-60} y={210} width={120} height={60} fill="#455A64" stroke={OL} strokeWidth={5} /><rect x={-160} y={262} width={320} height={22} rx={8} fill="#455A64" stroke={OL} strokeWidth={5} /></g>
    </g>;
  },

  /** the stock-market plaza and its giant screen */
  ajmarket: (t, z, f) => {
    const price = kf(z.price, t, 83), ch = kf(z.chart, t, 0), crawl: string = pick(z.crawl, t, ''), ring = z.ring ?? 999, crowd = kf(z.crowd, t, 1);
    return <g>
      {sky(z, f, '#7EC3F2', '#D8F0FB', 'ajmsky')}{[0, 1, 2].map((k) => cloud(z.x0 + 300 + k * 700 + ((t * 12) % 300), 120 + k * 30, 0.8, 'm' + k))}
      {Array.from({length: 12}, (_, k) => { const h = 380 + rnd(k + 3) * 420, x = z.x0 + k * 340; return <rect key={'bk' + k} x={x} y={f - h} width={300} height={h} fill={k % 2 ? '#AFC2D6' : '#C7D5E3'} stroke={OL} strokeWidth={3} />; })}
      {/* the tower */}
      <g transform={`translate(960 ${f})`}><rect x={-430} y={-960} width={860} height={960} fill="#E7ECF2" stroke={OL} strokeWidth={7} />
        {Array.from({length: 7}, (_, r) => Array.from({length: 8}, (_, q) => <rect key={r + '-' + q} x={-400 + q * 102} y={-940 + r * 52} width={80} height={34} fill="#CFE3F5" stroke={OL} strokeWidth={2} />))}
        <path d="M -470 -580 Q 0 -640 470 -580 L 470 -130 Q 0 -190 -470 -130 Z" fill="#0E1A2C" stroke={OL} strokeWidth={8} />
        <g transform="translate(-400 -520)"><rect x={0} y={0} width={190} height={92} rx={14} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={95} y={68} s={64} c={OL}>ANT</T>
          <T x={220} y={70} s={70} c={price >= 83 ? '#7CF29C' : '#FF8A80'} a="start">{money(price)}</T>
          <T x={220} y={-12} s={22} c="#9FB3C8" a="start">NASDAQ · CLASS A</T></g>
        <g transform="translate(-400 -400)"><path d={`M 0 ${200 - ((83 - 78) / 40) * 200} L 800 ${200 - ((83 - 78) / 40) * 200}`} stroke="#5E6B85" strokeWidth={3} strokeDasharray="12 10" />
          <T x={800} y={200 - ((83 - 78) / 40) * 200 + 28} s={20} c="#9FB3C8" a="end">OFFER PRICE $83</T>
          {ch > 0 && <path d={dayPath(800, 200, ch)} stroke="#7CF29C" strokeWidth={8} fill="none" strokeLinejoin="round" strokeLinecap="round" />}</g>
        <rect x={-430} y={-110} width={860} height={60} fill={NAVY} stroke={OL} strokeWidth={5} />
        <clipPath id="ajcrawl"><rect x={-428} y={-108} width={856} height={56} /></clipPath>
        {crawl && <g clipPath="url(#ajcrawl)"><T x={430 - ((t * 160) % (crawl.length * 21 + 900))} y={-68} s={32} c={GOLD2} a="start">{crawl}</T></g>}
        <rect x={-120} y={-50} width={240} height={50} fill="#9AA6B8" stroke={OL} strokeWidth={4} /></g>
      {/* podium + bell */}
      <g transform={`translate(1560 ${f})`}><rect x={-90} y={-180} width={180} height={180} fill="#5E6B85" stroke={OL} strokeWidth={5} />
        <g transform={`translate(0 -240) rotate(${t > ring && t < ring + 2 ? 18 * Math.sin((t - ring) * 22) * (1 - (t - ring) / 2) : 0})`}><path d="M -50 40 Q -50 -50 0 -60 Q 50 -50 50 40 Z" fill={GOLD} stroke={OL} strokeWidth={5} /><circle cy={48} r={10} fill={OL} /></g>
        {t > ring && t < ring + 2 && [0, 1, 2].map((q) => <circle key={q} cy={-250} r={70 + q * 40 + (t - ring) * 120} fill="none" stroke={GOLD} strokeWidth={5} opacity={clamp(1 - (t - ring) / 2) * 0.7} />)}</g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#D8D2C4" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#BDB6A6" stroke={OL} strokeWidth={4} />
      {crowd > 0 && Array.from({length: 16}, (_, k) => <g key={'cw' + k} opacity={crowd}>{ppl(120 + k * 115 + Math.sin(t + k) * 6, f + 40 + (k % 3) * 18, 0.7, k, t, true)}</g>)}
    </g>;
  },

  /** the 2021 lab */
  ajlab: (t, z, f) => {
    const chat: string = pick(z.chat, t, ''), n = Math.floor(clamp((t - (z.chatAt ?? 0)) / 2.4) * chat.length);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#EFEAE0" />
      <g transform="translate(160 150)"><rect x={0} y={0} width={680} height={400} rx={10} fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        {[0, 1, 2].map((col) => [0, 1, 2, 3].map((r) => { const x = 110 + col * 230, y = 70 + r * 85; const p = clamp((t * 0.6) - col * 0.3 - r * 0.1);
          return <g key={col + '-' + r}>{col < 2 && [0, 1, 2, 3].map((r2) => <path key={r2} d={`M ${x} ${y} L ${x + 230} ${70 + r2 * 85}`} stroke={BLUE} strokeWidth={2.5} opacity={0.5 * p} />)}
            <circle cx={x} cy={y} r={18} fill={p > 0.5 ? GOLD2 : '#FFFFFF'} stroke={OL} strokeWidth={4} /></g>; }))}
        <T x={340} y={385} s={22} c="#5E6B85">SKETCHES · NOT A REAL DIAGRAM</T></g>
      {/* plants and boxes */}
      {[0, 1].map((k) => <g key={'pl' + k} transform={`translate(${100 + k * 1700} ${f})`}><rect x={-40} y={-80} width={80} height={80} rx={10} fill={ORANGE} stroke={OL} strokeWidth={4} />
        {[0, 1, 2, 3].map((q) => <path key={q} d={`M 0 -80 Q ${-60 + q * 40} -180 ${-50 + q * 34 + Math.sin(t + q) * 6} -230`} stroke={LEAF} strokeWidth={14} fill="none" strokeLinecap="round" />)}</g>)}
      {[0, 1, 2].map((k) => <g key={'bx' + k} transform={`translate(${380 + k * 90} ${f - k * 0})`}><rect x={-40} y={-80 - (k % 2) * 0} width={80} height={80} fill="#C9A27A" stroke={OL} strokeWidth={4} /><path d="M -40 -50 L 40 -50" stroke={OL} strokeWidth={3} /></g>)}
      {/* monitor with chat */}
      <g transform="translate(1340 420)"><rect x={-330} y={-230} width={660} height={420} rx={20} fill="#263238" stroke={OL} strokeWidth={7} /><rect x={-306} y={-206} width={612} height={372} rx={10} fill="#FBF7EF" />
        <T x={-280} y={-160} s={26} c="#C1643B" a="start">CLAUDE</T>
        <rect x={-280} y={-140} width={560} height={150} rx={14} fill="#FFFFFF" stroke="#E0D6C4" strokeWidth={3} />
        <foreignObject x={-266} y={-132} width={532} height={140}><div style={{fontFamily: FONT, fontSize: 36, fontWeight: 600, color: NAVY, lineHeight: 1.3}}>{chat.slice(0, n)}{n < chat.length && Math.floor(t * 3) % 2 ? '|' : ''}</div></foreignObject>
        <rect x={-50} y={190} width={100} height={70} fill="#455A64" stroke={OL} strokeWidth={5} /><rect x={-150} y={252} width={300} height={22} rx={8} fill="#455A64" stroke={OL} strokeWidth={5} /></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#B8A88E" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#9C8B70" stroke={OL} strokeWidth={4} />
      {z.plaque && plaque(560, 620, z.plaque, GOLD2, 26)}
    </g>;
  },

  /** the revenue rocket */
  ajrocket: (t, z, f) => {
    const lift = kf(z.lift, t, 0), marks: [string, number][] = z.marks || [], H = 2200, climb = Math.min(lift * H, 420), sc = lift * H - climb, ry = f - 40 - climb;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={6000} fill="#CFEAFB" />{sky(z, f, '#3B86D9', '#CFEAFB', 'ajrsky')}<g transform={`translate(0 ${sc})`}>{[0, 1, 2, 3, 4, 5].map((k) => cloud(z.x0 + 1700 + (k % 3) * 520, 200 - k * 420, 1, 'r' + k))}
      {Array.from({length: 8}, (_, k) => <path key={'mt' + k} d={`M ${z.x0 + k * 520} ${f} L ${z.x0 + k * 520 + 260} ${f - 220 - rnd(k) * 160} L ${z.x0 + k * 520 + 520} ${f} Z`} fill={k % 2 ? '#C9B79C' : '#D8C8AE'} stroke={OL} strokeWidth={4} />)}
      {ground(z, f, '#E3D4B8', '#C9B79C')}
      {/* altitude ruler */}
      <g transform="translate(330 0)"><rect x={-14} y={f - 40 - H} width={28} height={H} fill="#FFFFFF" stroke={OL} strokeWidth={4} />
        {marks.map(([lab, fr], k) => { const y = f - 40 - fr * H, on = lift >= fr - 0.02; const s = on ? E.outBack(clamp((lift - fr + 0.02) * 12)) : 0;
          return <g key={'mk' + k}><path d={`M -14 ${y} L 60 ${y}`} stroke={OL} strokeWidth={4} />
            <g transform={`translate(70 ${y}) scale(${Math.max(0.0001, s)})`}><path d="M 0 0 L 0 -70 L 70 -55 L 0 -40" fill={RED} stroke={OL} strokeWidth={4} />{plaque(Math.max(150, lab.length * 9 + 100), -10, lab, '#FFFFFF', 24)}</g></g>; })}
      </g>
      {/* launch pad */}
      <rect x={760} y={f - 60} width={420} height={60} fill={GREY} stroke={OL} strokeWidth={5} /></g>
      {plaque(330, 120, 'NOT TO SCALE', '#FFFFFF', 20)}
      {lift > 0.005 && Array.from({length: 10}, (_, k) => { const a = rnd(k) * Math.PI, r = 60 + ((t * 120 + k * 40) % 200); return <circle key={'sm' + k} cx={970 + Math.cos(a) * r * 1.6} cy={f - 50 - Math.sin(a) * r * 0.3} r={40 + r * 0.2} fill="#FFFFFF" stroke={OL} strokeWidth={3} opacity={0.85 * clamp(1 - lift * 2)} />; })}
      <g transform={`translate(970 ${ry}) rotate(${Math.sin(t * 9) * (lift > 0.01 ? 1.2 : 0)})`}>
        {lift > 0.005 && <path d={`M -40 0 Q 0 ${150 + Math.sin(t * 30) * 20} 40 0 Z`} fill={ORANGE} stroke={OL} strokeWidth={4} />}
        {lift > 0.005 && <path d={`M -22 0 Q 0 ${90 + Math.sin(t * 40) * 14} 22 0 Z`} fill={GOLD2} />}
        <path d="M -70 -60 L -110 10 L -60 0 Z M 70 -60 L 110 10 L 60 0 Z" fill={RED} stroke={OL} strokeWidth={5} />
        <path d="M -60 0 L -60 -300 Q 0 -420 60 -300 L 60 0 Z" fill="#FFFFFF" stroke={OL} strokeWidth={6} />
        <circle cy={-250} r={30} fill="#BFE6F7" stroke={OL} strokeWidth={5} /><T x={0} y={-150} s={18} c={NAVY}>REVENUE</T>
        {z.ticket !== false && <g transform="translate(78 -70) rotate(8)"><rect x={-40} y={-26} width={80} height={52} rx={6} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={9} s={22} c={OL}>ANT</T></g>}</g>
    </g>;
  },

  /** the compute hall + the dollar machine */
  ajhall: (t, z, f) => {
    const cost = kf(z.cost, t, 1), ctext: string = pick(z.costText, t, ''), rate = kf(z.coins, t, 1);
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#E6EEF5" />
      {Array.from({length: 10}, (_, k) => <rect key={'sk' + k} x={z.x0 + 80 + k * 420} y={60} width={300} height={60} rx={8} fill="#BFE6F7" stroke={OL} strokeWidth={4} />)}
      <rect x={z.x0} y={150} width={z.x1 - z.x0} height={40} fill="#C5CDD8" stroke={OL} strokeWidth={4} />
      {Array.from({length: 9}, (_, k) => { const x = z.x0 + 40 + k * 230; return <g key={'rk' + k}><rect x={x} y={300} width={170} height={f - 300} fill="#37474F" stroke={OL} strokeWidth={5} />
        {Array.from({length: 12}, (_, r) => <g key={r}><rect x={x + 14} y={320 + r * 58} width={142} height={42} rx={4} fill="#263238" />
          <circle cx={x + 30} cy={341 + r * 58} r={6} fill={(Math.floor(t * 4 + k * 3 + r) % 3) ? '#7CF29C' : '#2E5E3E'} /><circle cx={x + 50} cy={341 + r * 58} r={6} fill={(Math.floor(t * 5 + r) % 4) ? CY : '#1E4A5C'} /></g>)}</g>; })}
      {/* power line + fans */}
      {[0, 1, 2].map((k) => <g key={'fan' + k} transform={`translate(${300 + k * 640} 240) rotate(${t * 300 + k * 40})`}>{[0, 90, 180, 270].map((r) => <path key={r} transform={`rotate(${r})`} d="M 0 0 Q 20 -20 0 -40 Q -12 -20 0 0" fill="#B0BEC5" stroke={OL} strokeWidth={3} />)}</g>)}
      {/* the dollar machine */}
      <g transform={`translate(960 ${f})`}><rect x={-300} y={-520} width={600} height={520} rx={30} fill="#F2F5F8" stroke={OL} strokeWidth={7} />
        <path d="M -90 -620 L 90 -620 L 40 -520 L -40 -520 Z" fill={GREY} stroke={OL} strokeWidth={5} />
        {rate > 0 && Array.from({length: 3}, (_, q) => { const u = ((t * 0.9 * rate + q / 3) % 1); return u < 0.6 ? coin(0, -900 + u * 600, 1.4, 'dm' + q, GOLD2, '$1') : null; })}
        <T x={0} y={-478} s={30} c={NAVY}>COMPUTE COST PER $1 OF SALES</T>
        <g transform="translate(0 -190)"><path d="M -200 0 A 200 200 0 0 1 200 0" fill="none" stroke="#CFD8E3" strokeWidth={34} />
          <path d="M -200 0 A 200 200 0 0 1 0 -200" fill="none" stroke={GREEN} strokeWidth={34} opacity={0.6} /><path d="M 0 -200 A 200 200 0 0 1 200 0" fill="none" stroke={RED} strokeWidth={34} opacity={0.6} />
          <T x={-200} y={46} s={24} c={NAVY}>$0</T><T x={0} y={-226} s={24} c={NAVY}>$1</T><T x={200} y={46} s={24} c={NAVY}>$2</T>
          <g transform={`rotate(${clamp(cost / 2) * 180 - 90})`}><path d="M 0 0 L 0 -180" stroke={OL} strokeWidth={10} strokeLinecap="round" /></g>
          <circle r={20} fill={NAVY} /></g>
        {ctext && <g transform="translate(0 -70)">{plaque(0, 0, ctext, cost > 1 ? '#FDECEA' : '#E9F7EF', 34, cost > 1 ? RED : GREEN)}</g>}
        {Array.from({length: Math.min(6, Math.round(cost * 3))}, (_, k) => <rect key={'br' + k} x={330} y={-60 - k * 56} width={150} height={50} rx={6} fill={cost > 1 ? '#F5B7A3' : '#BFE3C9'} stroke={OL} strokeWidth={4} />)}
        <T x={405} y={-80 - Math.min(6, Math.round(cost * 3)) * 56} s={22} c={NAVY}>COMPUTE</T></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#CFD8E3" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#B0BEC5" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** commitments: the contract scroll */
  ajscroll: (t, z, f) => {
    const u = kf(z.unroll, t, 0), years: string[] = z.years || ['2026', '2030', '2035', '2040', '2045'], stamp = z.stamp ?? 999, L = 1500, x0 = 220;
    const crates = ['CHIPS', 'DATA CENTERS', 'POWER', 'CLOUD', 'CHIPS', 'LEASES', 'POWER', 'CLOUD', 'DATA CENTERS', 'CHIPS'];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#ECE6DA" />
      {Array.from({length: 8}, (_, k) => <path key={'tr' + k} d={`M ${z.x0 + k * 400} 120 L ${z.x0 + k * 400 + 200} 40 L ${z.x0 + k * 400 + 400} 120`} fill="none" stroke="#B9A98E" strokeWidth={10} />)}
      <rect x={z.x0} y={120} width={z.x1 - z.x0} height={20} fill="#B9A98E" />
      {/* the scroll */}
      <g transform={`translate(${x0} ${f - 150})`}><rect x={0} y={-36} width={L * u} height={120} fill={PAPER} stroke={OL} strokeWidth={5} />
        {Array.from({length: 18}, (_, k) => (k + 1) / 19 < u ? <path key={'ln' + k} d={`M ${20 + k * (L / 19)} -12 L ${60 + k * (L / 19)} -12 M ${20 + k * (L / 19)} 10 L ${70 + k * (L / 19)} 10`} stroke="#B0BEC5" strokeWidth={4} /> : null)}
        {years.map((y, k) => { const fx = k / Math.max(1, years.length - 1); return fx <= u + 0.001 ? <g key={'yr' + k}><path d={`M ${fx * L} 84 L ${fx * L} 110`} stroke={OL} strokeWidth={4} /><T x={fx * L} y={146} s={30} c={NAVY}>{y}</T></g> : null; })}
        <g transform={`translate(${L * u} 24)`}><ellipse rx={30} ry={64} fill="#F3E5C3" stroke={OL} strokeWidth={5} /><ellipse rx={12} ry={30} fill="#D8C59A" /></g></g>
      {crates.map((c, k) => { const fx = (k + 0.5) / crates.length; if (fx > u) return null; const s = E.outBack(clamp((u - fx) * 8)), stackH = 1 + (k % 3);
        return <g key={'cr' + k} transform={`translate(${x0 + fx * L} ${f - 190}) scale(${s})`}>{Array.from({length: stackH}, (_, q) =>
          <g key={q} transform={`translate(0 ${-q * 92})`}><rect x={-62} y={-88} width={124} height={88} rx={6} fill={['#C9A27A', '#B88E62'][q % 2]} stroke={OL} strokeWidth={4} /><T x={0} y={-36} s={fit(c, 110, 20)} c={NAVY}>{c}</T></g>)}</g>; })}
      {t >= stamp && <g transform={`translate(1320 330) rotate(-10) scale(${lerp(2.2, 1, E.out(win(t, stamp, 0.25)))})`} opacity={clamp((t - stamp) / 0.15)}>
        <rect x={-400} y={-60} width={800} height={120} rx={12} fill="#FFFFFFCC" stroke={RED} strokeWidth={10} /><T x={0} y={20} s={54} c={RED}>MOSTLY NON-CANCELABLE</T></g>}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#B8A88E" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#9C8B70" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** THE MONEY LOOP */
  ajloop: (t, z, f) => {
    const inv = kf(z.invest, t, 0), pay = kf(z.pay, t, 0), comp = kf(z.compute, t, 0), res = kf(z.resell, t, 0), stake = kf(z.stake, t, 0), g = kf(z.google, t, 0),
      gl = kf(z.gloop, t, 0), spin = kf(z.spin, t, 0), L = {invest: 'INVESTMENT', pay: 'PAYS FOR COMPUTE', compute: 'COMPUTING POWER', buy: 'BUY CLAUDE VIA THE CLOUD', pass: 'PASSED ON, MINUS A CUT', ...(z.labels || {})};
    const AM: [number, number] = [600, 600], AN: [number, number] = [1180, 560], BU: [number, number] = [170, 700], GO: [number, number] = [1680, 330];
    return <g>
      {sky(z, f, '#86C8F0', '#E4F4FC', 'ajlsky')}{[0, 1].map((k) => cloud(z.x0 + 500 + k * 900 + ((t * 10) % 300), 110, 0.7, 'l' + k))}
      {ground(z, f, '#B7DB9C', '#93C47A')}
      {spin > 0 && <ellipse cx={(AM[0] + AN[0]) / 2} cy={f - 360} rx={470} ry={330} fill="none" stroke={GOLD} strokeWidth={10} strokeDasharray="30 22" strokeDashoffset={-t * 120} opacity={spin} />}
      {building(AM[0], f, 380, 560, '#F6C27A', 'AMAZON · CLOUD', 'am', 'cloud', inv > 0 ? 0 : 0)}
      {/* stake meter on Amazon's building */}
      {stake > 0 && <g transform={`translate(${BU[0]} ${f - 470})`} opacity={clamp(stake * 4)}><rect x={-130} y={-24} width={260} height={48} rx={12} fill="#FFFFFF" stroke={OL} strokeWidth={5} />
        <rect x={-123} y={-17} width={246 * stake} height={34} rx={9} fill={GREEN} /><T x={0} y={-38} s={20} c={NAVY}>AMAZON'S STAKE</T><T x={0} y={52} s={18} c={NAVY}>ON PAPER</T></g>}
      {building(AN[0], f, 300, 720, '#E7ECF2', 'ANTHROPIC', 'an', 'tower', 0)}
      <g transform={`translate(${AN[0]} ${f - 640})`}><rect x={-80} y={-30} width={160} height={60} rx={10} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={14} s={36} c={OL}>ANT</T></g>
      {[0, 1, 2].map((k) => <g key={'bu' + k}>{building(BU[0] - 110 + k * 110, f, 96, 220 + k * 50, ['#BFD7EA', '#D6E6C7', '#F1D7C2'][k], '', 'b' + k)}</g>)}
      {plaque(BU[0], f + 50, 'BUSINESSES', '#FFFFFF', 26)}
      {g > 0 && <g opacity={g} transform={`translate(0 ${(1 - g) * 40})`}>{building(GO[0], f, 300, 480, '#CFE3F5', 'GOOGLE · CLOUD', 'go', 'flat')}</g>}
      {pipe([AM[0] + 120, f - 560], [AN[0] - 110, f - 600], -0.25, 22, GOLD, t, inv, 'inv', 'coin', L.invest, OL)}
      {pipe([AM[0] + 190, f - 420], [AN[0] - 150, f - 420], 0.0, 14, CY, t, comp, 'cmp', 'chip', L.compute, TEAL)}
      {pipe([AN[0] - 150, f - 300], [AM[0] + 190, f - 290], -0.18, 22, BLUE, t, pay, 'pay', 'coin', L.pay)}
      {pipe([BU[0] + 60, f - 330], [AM[0] - 190, f - 400], -0.3, 16, PURPLE, t, res, 'buy', 'coin', L.buy)}
      {pipe([AM[0] + 190, f - 120], [AN[0] - 150, f - 120], 0.1, 12, GREEN, t, clamp(res * 2 - 1), 'pass', 'coin', L.pass)}
      {gl > 0 && <g>{pipe([GO[0] - 150, f - 420], [AN[0] + 150, f - 520], 0.22, 16, GOLD, t, gl, 'g1', 'coin', 'INVESTMENT', OL)}
        {pipe([AN[0] + 150, f - 260], [GO[0] - 150, f - 200], 0.2, 16, BLUE, t, gl, 'g2', 'coin', 'PAYS FOR COMPUTE')}</g>}
    </g>;
  },

  /** the round table of the private placement */
  ajsupply: (t, z, f) => {
    const rv = kf(z.reveal, t, 7), fl = kf(z.flip, t, 0), fw = kf(z.flow, t, 0);
    const P: [string, string][] = z.parts || [['GOOGLE', 'CLOUD + AI CHIPS'], ['NVIDIA', 'GPUS (VIA PROVIDERS)'], ['AMD', 'GPU SYSTEMS'], ['BROADCOM', 'ACCELERATORS'],
      ['MICRON', 'MEMORY (INDIRECT)'], ['MICROSOFT', 'CLOUD'], ['TSMC', 'MAKES CHIPS (INDIRECT)']];
    const cx = 960, cy = 560;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#EEF2F7" />
      {Array.from({length: 6}, (_, k) => <rect key={'wn' + k} x={z.x0 + 100 + k * 340} y={80} width={240} height={300} rx={10} fill="#BFE6F7" stroke={OL} strokeWidth={5} />)}
      <ellipse cx={cx} cy={cy + 300} rx={760} ry={190} fill="#8D6E63" stroke={OL} strokeWidth={7} /><ellipse cx={cx} cy={cy + 290} rx={720} ry={168} fill="#A1887F" />
      <g transform={`translate(${cx} ${cy + 250})`}><rect x={-110} y={-420} width={220} height={420} rx={8} fill="#E7ECF2" stroke={OL} strokeWidth={6} /><path d="M -110 -420 L 0 -500 L 110 -420 Z" fill="#E7ECF2" stroke={OL} strokeWidth={6} />
        <rect x={-80} y={-360} width={160} height={60} rx={10} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={-316} s={36} c={OL}>ANT</T></g>
      {P.map(([nm, role], k) => { const a = Math.PI * (0.06 + 0.88 * k / (P.length - 1)), x = cx - Math.cos(a) * 660, y = 800 - Math.sin(a) * 520;
        const s = E.outBack(clamp(rv - k)), flip = clamp(fl - k), sx = Math.abs(Math.cos(flip * Math.PI)), back = flip > 0.5;
        if (s <= 0) return null;
        return <g key={'pt' + k}>
          {fw > 0 && <g opacity={fw}>{[0, 1].map((q) => { const u = (t * 0.45 + q / 2 + k * 0.13) % 1, inb = q === 0;
            const px = inb ? lerp(x, cx, u) : lerp(cx, x, u), py = inb ? lerp(y - 20, cy + 40, u) - Math.sin(u * Math.PI) * 50 : lerp(cy + 120, y + 30, u) + Math.sin(u * Math.PI) * 40;
            return inb ? coin(px, py, 0.8, 'pc' + k + q) : chipTok(px, py, 0.65, 'pk' + k + q); })}</g>}
          <g transform={`translate(${x} ${y}) scale(${s * sx} ${s})`}>{back ? plaque(0, 0, role, '#E3F2FD', fit(role, 330, 26), BLUE) : plaque(0, 0, nm, '#FFFFFF', 28)}</g></g>; })}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#C9B79C" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#A8946F" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the detective's corkboard */
  ajcase: (t, z, f) => {
    const cards: [number, string][] = z.cards || [], st = kf(z.strings, t, 0), lens = kf(z.lens, t, -500), paper = z.paper ?? 999;
    const POS: [number, number][] = [[520, 300], [960, 240], [1400, 300], [600, 560], [1320, 560], [960, 640]];
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#DCE6EE" />
      <rect x={300} y={140} width={1320} height={640} rx={14} fill="#C79A63" stroke={OL} strokeWidth={8} />
      {Array.from({length: 40}, (_, k) => <circle key={'dt' + k} cx={330 + rnd(k) * 1260} cy={170 + rnd(k + 50) * 580} r={3} fill="#A47A47" />)}
      {cards.map(([at, lab], k) => k > 0 && t >= at && st > 0 ? <path key={'s' + k} d={`M ${POS[0][0]} ${POS[0][1]} Q ${(POS[0][0] + POS[k % 6][0]) / 2} ${(POS[0][1] + POS[k % 6][1]) / 2 + 60} ${POS[k % 6][0]} ${POS[k % 6][1]}`}
        stroke={RED} strokeWidth={5} fill="none" pathLength={1} strokeDasharray={`${clamp(st)} 1`} /> : null)}
      {cards.map(([at, lab], k) => { const p = POS[k % 6], s = pop(t, at, 0.45); if (s <= 0) return null;
        return <g key={'cd' + k} transform={`translate(${p[0]} ${p[1]}) rotate(${(rnd(k) - 0.5) * 8}) scale(${s})`}><rect x={-150} y={-56} width={300} height={112} rx={6} fill={PAPER} stroke={OL} strokeWidth={4} />
          <circle cy={-46} r={12} fill={RED} stroke={OL} strokeWidth={3} /><T x={0} y={14} s={fit(lab, 270, 30)} c={NAVY}>{lab}</T></g>; })}
      {t >= paper && <g transform={`translate(1320 760) rotate(-8) scale(${lerp(2, 1, E.out(win(t, paper, 0.25)))})`} opacity={clamp((t - paper) / 0.15)}>
        <rect x={-210} y={-50} width={420} height={100} rx={10} fill="#FFFFFF" stroke={RED} strokeWidth={8} /><T x={0} y={18} s={50} c={RED}>PAPER GAIN</T></g>}
      <g transform={`translate(${lens} 520) rotate(-25)`}><circle r={120} fill="#BFE6F7" opacity={0.35} stroke={OL} strokeWidth={14} /><rect x={-16} y={120} width={32} height={180} rx={10} fill="#5D4037" stroke={OL} strokeWidth={5} /></g>
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#9AA6B8" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#7D899B" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** the lockup vault */
  ajvault: (t, z, f) => {
    const days = kf(z.days, t, 180), crack = kf(z.crack, t, 0), open = kf(z.open, t, 0), sign: string = pick(z.sign, t, 'LOCKUP');
    const dx = 1100, dy = 520;
    return <g>
      <rect x={z.x0} y={-2500} width={z.x1 - z.x0} height={4000} fill="#D7DEE6" />
      {Array.from({length: 40}, (_, k) => <rect key={'st' + k} x={z.x0 + (k % 10) * 400 + (Math.floor(k / 10) % 2) * 200} y={60 + Math.floor(k / 10) * 160} width={390} height={150} fill="#CBD3DD" stroke="#B5BFCB" strokeWidth={4} />)}
      {/* inside the vault */}
      <circle cx={dx} cy={dy} r={330} fill="#3A4558" stroke={OL} strokeWidth={8} />
      {Array.from({length: 12}, (_, k) => <g key={'sh' + k} transform={`translate(${dx - 220 + (k % 4) * 140} ${dy - 120 + Math.floor(k / 4) * 100})`}><rect x={-56} y={-36} width={112} height={72} rx={6} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={10} s={22} c={OL}>ANT</T></g>)}
      {crack > 0 && Array.from({length: 4}, (_, q) => { const u = (t * 0.5 + q / 4) % 1; return <g key={'tk' + q} opacity={crack}><g transform={`translate(${dx - 360 - u * 520} ${dy + 180 + Math.sin(u * 9) * 10}) scale(0.7)`}><rect x={-56} y={-36} width={112} height={72} rx={6} fill={GOLD2} stroke={OL} strokeWidth={4} /><T x={0} y={10} s={22} c={OL}>ANT</T></g></g>; })}
      {/* the door */}
      <g transform={`translate(${dx - 330} ${dy}) scale(${Math.max(0.05, 1 - 0.18 * crack - 0.8 * open)} 1) translate(330 0)`}>
        <circle r={340} fill="#AEB8C6" stroke={OL} strokeWidth={10} /><circle r={290} fill="#C5CDD8" stroke={OL} strokeWidth={6} />
        {Array.from({length: 8}, (_, k) => <rect key={'bo' + k} transform={`rotate(${k * 45}) translate(0 -310)`} x={-20} y={-14} width={40} height={28} rx={6} fill="#8A97A8" stroke={OL} strokeWidth={4} />)}
        <g transform={`rotate(${t * 30})`}>{[0, 60, 120].map((r) => <rect key={r} transform={`rotate(${r})`} x={-150} y={-12} width={300} height={24} rx={12} fill="#8A97A8" stroke={OL} strokeWidth={4} />)}</g>
        <circle r={110} fill={NAVY} stroke={OL} strokeWidth={6} /><T x={0} y={-20} s={24} c="#9FB3C8">DAYS LEFT</T><T x={0} y={44} s={66} c={GOLD2}>{Math.max(0, Math.round(days))}</T></g>
      {plaque(dx, dy + 400, sign, NAVY, 34, GOLD2)}
      {/* queue of anonymous holders */}
      {Array.from({length: 7}, (_, k) => ppl(160 + k * 95, f, 1.0, k, t * 0.4, true))}
      <rect x={z.x0} y={f} width={z.x1 - z.x0} height={700} fill="#8D99AA" /><rect x={z.x0} y={f} width={z.x1 - z.x0} height={12} fill="#6F7B8C" stroke={OL} strokeWidth={4} />
    </g>;
  },

  /** THE FORK: bright, middle and dark roads */
  ajroads: (t, z, f) => {
    const fc = pick(z.focus, t, 0) as number, wk = kf(z.walk, t, 0);
    const dim = (k: number) => (fc === 0 || fc === k ? 1 : 0.28);
    const roads: [string, string, [number, number, number, number, number, number]][] = [
      ['BRIGHT ROAD', GOLD, [960, 1040, 700, 760, 330, 330]], ['MIDDLE ROAD', BLUE, [960, 1040, 960, 760, 960, 450]], ['DARK ROAD', '#4A5570', [960, 1040, 1220, 760, 1600, 520]]];
    const storm = fc === 3 ? clamp((t - (z.focusAt3 ?? 0)) / 0.6) : 0, sun = fc === 1 ? 1 : 0;
    return <g>
      {sky(z, f, fc === 3 ? '#5D6C82' : '#6FB6EE', fc === 3 ? '#AEB9C8' : '#E2F3FC', 'ajrd' + (fc === 3 ? 'x' : 'y'))}
      {/* bright hill city (left) */}
      <g opacity={dim(1)}><path d="M -200 560 Q 330 180 860 560 Z" fill="#9ED37D" stroke={OL} strokeWidth={5} />
        {sun > 0 && <circle cx={330} cy={170} r={90 + 6 * Math.sin(t * 3)} fill={GOLD2} opacity={0.9} stroke={OL} strokeWidth={5} />}
        {Array.from({length: 6}, (_, k) => <rect key={'bc' + k} x={190 + k * 50} y={330 - (k % 3) * 60 - 40} width={44} height={120 + (k % 3) * 60} fill={k % 2 ? '#FFE9A8' : '#FFFFFF'} stroke={OL} strokeWidth={4} />)}</g>
      {/* plain town (middle) */}
      <g opacity={dim(2)}><path d="M 700 560 Q 960 400 1220 560 Z" fill="#C2D9A4" stroke={OL} strokeWidth={5} />
        {Array.from({length: 5}, (_, k) => <g key={'mt' + k} transform={`translate(${860 + k * 50} ${470 - (k % 2) * 10})`}><rect x={-20} y={-40} width={40} height={40} fill="#E8E1D0" stroke={OL} strokeWidth={3} /><path d="M -24 -40 L 0 -62 L 24 -40 Z" fill="#B04A3A" stroke={OL} strokeWidth={3} /></g>)}</g>
      {/* storm cliff (right) */}
      <g opacity={dim(3)}><path d="M 1100 560 L 1500 420 L 1680 520 L 1680 560 Z" fill="#8C8F7A" stroke={OL} strokeWidth={5} /><path d="M 1680 520 L 1680 1100 L 2200 1100 L 2200 600 Z" fill="#5A7BA6" />
        {[0, 1].map((k) => cloud(1500 + k * 220, 300 + k * 30, 1.2, 'sc' + k, fc === 3 ? '#6B778A' : '#D7DEE6'))}
        {storm > 0 && Array.from({length: 26}, (_, k) => { const x = 1300 + rnd(k) * 600, y = ((t * 900 + rnd(k + 9) * 600) % 700) + 300; return <path key={'rn' + k} d={`M ${x} ${y} l -10 30`} stroke="#DCE6F2" strokeWidth={4} opacity={storm} />; })}
        {storm > 0 && Math.floor(t * 1.3) % 3 === 0 && (t * 1.3) % 1 < 0.15 && <path d="M 1640 260 L 1600 360 L 1640 360 L 1590 480" stroke={GOLD2} strokeWidth={8} fill="none" />}</g>
      {ground(z, f, '#B7DB9C', '#93C47A')}<rect x={z.x0} y={560} width={z.x1 - z.x0} height={f - 560} fill="#B7DB9C" />
      {roads.map(([nm, c, p], k) => { const d = `M ${p[0]} ${p[1]} Q ${p[2]} ${p[3]} ${p[4]} ${p[5]}`;
        return <g key={'rd' + k} opacity={dim(k + 1)}><path d={d} stroke={OL} strokeWidth={96} fill="none" strokeLinecap="round" /><path d={d} stroke={c === GOLD ? '#F5D27A' : c === BLUE ? '#BFD3EA' : '#8C95A8'} strokeWidth={84} fill="none" strokeLinecap="round" />
          <path d={d} stroke="#FFFFFF" strokeWidth={6} fill="none" strokeDasharray="30 30" opacity={0.8} />
          <g transform={`translate(${lerp(p[0], p[4], 0.55) + (k - 1) * 40} ${lerp(p[1], p[5], 0.55) - 30})`}><path d="M 0 0 L 0 -150" stroke="#6D4C41" strokeWidth={12} />{plaque(0, -160, nm, c === GOLD ? GOLD2 : c === BLUE ? '#E3F2FD' : '#D7DEE6', 26)}</g></g>; })}
      {/* the walking share */}
      {(() => { const k = fc === 0 ? 1 : fc - 1, p = roads[k][2], u = fc === 0 ? 0.12 : 0.12 + 0.88 * wk;
        const x = (1 - u) * (1 - u) * p[0] + 2 * (1 - u) * u * p[2] + u * u * p[4], y = (1 - u) * (1 - u) * p[1] + 2 * (1 - u) * u * p[3] + u * u * p[5], s = 0.9 - 0.45 * u;
        return <g transform={`translate(${x} ${y - 20 - Math.abs(Math.sin(t * 6)) * 12 * (u > 0 && u < 1 ? 1 : 0)}) scale(${s})`}>{ticket(t, fc === 3 ? 'worry' : fc === 1 ? 'wow' : 'calm')}</g>; })()}
      {plaque(960, f + 60, z.note || 'SCENARIOS · ILLUSTRATIVE · NO PROBABILITIES', '#FFFFFF', 22)}
    </g>;
  },

  /** the gold-rush valley and the shovel shop */
  ajgold: (t, z, f) => {
    const fw = kf(z.flow, t, 0), twice = z.twice ?? 999;
    return <g>
      {sky(z, f, '#79BDEB', '#F3E7C8', 'ajgsky')}
      {Array.from({length: 6}, (_, k) => <path key={'cy' + k} d={`M ${z.x0 + k * 560} ${f} L ${z.x0 + k * 560 + 120} ${f - 360 - rnd(k) * 140} L ${z.x0 + k * 560 + 420} ${f - 300 - rnd(k + 4) * 100} L ${z.x0 + k * 560 + 560} ${f} Z`} fill={k % 2 ? '#D49A6A' : '#C98B5B'} stroke={OL} strokeWidth={5} />)}
      {ground(z, f, '#E3C79A', '#C9A77A')}
      <path d={`M ${z.x0} ${f + 60} Q 400 ${f + 20} 800 ${f + 80} T 1700 ${f + 60} L 1700 ${f + 140} Q 1200 ${f + 170} 800 ${f + 140} T ${z.x0} ${f + 130} Z`} fill="#6FB6E8" stroke={OL} strokeWidth={4} />
      {Array.from({length: 5}, (_, k) => { const x = 160 + k * 230, sw = Math.sin(t * 3 + k) * 12;
        return <g key={'pr' + k}>{ppl(x, f + 70, 0.95, k, t * 0.5, true)}<g transform={`translate(${x + 50} ${f + 50 + sw * 0.3}) rotate(${sw})`}><ellipse rx={50} ry={14} fill="#6D4C41" stroke={OL} strokeWidth={4} />
          {Math.floor(t + k) % 4 === 0 && <circle cx={10} cy={-6} r={6} fill={GOLD2} stroke={OL} strokeWidth={2} />}</g></g>; })}
      {/* the shovel shop */}
      <g transform={`translate(1500 ${f})`}><rect x={-240} y={-420} width={480} height={420} fill="#F2E3C6" stroke={OL} strokeWidth={6} /><path d="M -280 -420 L 0 -540 L 280 -420 Z" fill={RED} stroke={OL} strokeWidth={6} />
        {plaque(0, -460, 'SHOVELS · ALWAYS OPEN', GOLD2, 26)}
        {['CHIPS', 'CLOUD', 'POWER'].map((c, k) => <g key={c} transform={`translate(${-150 + k * 150} -90)`}><rect x={-62} y={-90} width={124} height={90} rx={6} fill="#C9A27A" stroke={OL} strokeWidth={4} /><T x={0} y={-36} s={24} c={NAVY}>{c}</T>
          <path d={`M ${-30} -90 L ${-30} -220 M -50 -220 L -10 -220`} stroke="#6D4C41" strokeWidth={8} /><path d="M -46 -88 L -14 -88 L -20 -60 L -40 -60 Z" fill="#B0BEC5" stroke={OL} strokeWidth={3} /></g>)}
        <rect x={-200} y={-360} width={400} height={120} rx={8} fill="#BFE6F7" stroke={OL} strokeWidth={5} />
        {t >= twice && <g transform={`translate(0 -300) scale(${E.outBack(win(t, twice, 0.4))})`}><rect x={-170} y={-40} width={340} height={80} rx={12} fill={GREEN} stroke={OL} strokeWidth={5} /><T x={0} y={16} s={40} c="#FFFFFF">PAID TWICE</T></g>}</g>
      {fw > 0 && Array.from({length: 8}, (_, q) => { const u = (t * 0.35 + q / 8) % 1, x = lerp(300 + (q % 5) * 220, 1400, u), y = f - 120 - Math.sin(u * Math.PI) * 260; return <g key={'gf' + q} opacity={fw}>{coin(x, y, 0.9, 'g' + q)}</g>; })}
    </g>;
  },

  /** title card */
  ajtitle: (t, z, f) => {
    const lines: string[] = z.lines || ["ANTHROPIC'S $1.5 TRILLION IPO", 'GOLD RUSH', 'OR BUBBLE?'];
    const flipN = Math.floor(clamp(t / 1.2) * 12);
    const u = clamp((t - 0.6) / 2.2);
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill="#F7F1E3" />
      {Array.from({length: 20}, (_, k) => <path key={'ray' + k} transform={`translate(960 1100) rotate(${k * 18 + t * 4})`} d="M 0 0 L -70 -1500 L 70 -1500 Z" fill={k % 2 ? '#F1E6CC' : '#FFF8E8'} />)}
      <g transform="translate(960 830)"><rect x={-420} y={-120} width={840} height={240} rx={20} fill={NAVY} stroke={OL} strokeWidth={8} />
        {['A', 'N', 'T'].map((ch, k) => { const done = flipN > 3 + k * 3; const shown = done ? ch : String.fromCharCode(65 + ((Math.floor(t * 14) + k * 5) % 26));
          return <g key={k} transform={`translate(${-220 + k * 220} 0)`}><rect x={-90} y={-95} width={180} height={190} rx={14} fill="#26344F" stroke={GOLD} strokeWidth={4} /><path d="M -90 0 L 90 0" stroke="#0E1A2C" strokeWidth={4} /><T x={0} y={62} s={170} c={done ? GOLD2 : '#9FB3C8'}>{shown}</T></g>; })}</g>
      <g transform="translate(150 1000)"><path d={`M 0 0 L ${300 * Math.min(1, u * 1.6)} ${-300 * Math.min(1, u * 1.6)}`} stroke={GREEN} strokeWidth={14} strokeLinecap="round" />
        {u > 0.62 && <g transform={`translate(300 -300) scale(${E.outBack(clamp((u - 0.62) * 4))})`}><path d="M 0 -80 L 80 60 L -80 60 Z" fill={GOLD2} stroke={OL} strokeWidth={8} strokeLinejoin="round" /><T x={0} y={44} s={90} c={OL}>!</T></g>}</g>
      {lines.map((ln, k) => { const n = Math.floor(clamp((t - 0.4 - k * 0.55) / 0.5) * ln.length);
        return <T key={k} x={1060} y={170 + k * 130} s={fit(ln, k === 0 ? 1500 : 1100, k === 0 ? 84 : 120)} c={k === 2 ? RED : NAVY} st="#FFFFFF" sw={14}>{ln.slice(0, n)}</T>; })}
      <T x={960} y={1060} s={30} c={NAVY} ls={6}>THE HIDDEN ECONOMICS</T>
    </g>;
  },

  /** chapter bumper: a golden share ticket stamps down */
  ajbumper: (t, z, f) => {
    const c = z.color || BLUE, drop = lerp(-500, 0, E.inOut(win(t, 0.2, 0.5))), sq = t > 0.7 ? 1 - 0.12 * Math.exp(-(t - 0.7) * 6) * Math.cos((t - 0.7) * 30) : 1;
    return <g>
      <rect x={-200} y={-200} width={2400} height={1500} fill={c} />
      {Array.from({length: 12}, (_, k) => <rect key={'st' + k} x={-200 + k * 200} y={-200} width={100} height={1500} fill="#FFFFFF" opacity={0.06} />)}
      <g transform={`translate(960 ${790 + drop}) scale(${2 - sq} ${sq})`}>{ticket(t, 'calm', 2.0)}</g>
      {t >= 0.7 && t < 1.3 && <T x={960} y={640} s={70} c="#FFFFFF" st={OL} sw={8} o={1 - clamp((t - 1.0) / 0.3)}>CLICK!</T>}
      <g opacity={clamp((t - 0.5) / 0.3)}><T x={960} y={220} s={40} c="#FFFFFF" ls={6}>{z.act || 'CHAPTER ONE'}</T>
        <rect x={360} y={300} width={1200} height={140} rx={20} fill={NAVY} stroke={OL} strokeWidth={6} />
        <T x={960} y={392} s={fit(z.title || '', 1140, 62)} c={GOLD2}>{z.title || ''}</T>
        {t >= 1.2 && <T x={960} y={530} s={fit(z.caption || '', 1300, 36)} c="#FFFFFF" st={OL} sw={6} o={clamp((t - 1.2) / 0.3)}>{z.caption || ''}</T>}</g>
    </g>;
  },
};

/** the golden share ticket with a face */
function ticket(t: number, mood: string, s = 1) {
  const bob = Math.sin(t * 3) * 4;
  return <g transform={`scale(${s}) translate(0 ${bob})`}>
    <ellipse cx={0} cy={86} rx={90} ry={12} fill="#000" opacity={0.15} />
    <path d="M -110 -60 L 110 -60 Q 110 -40 126 -30 L 126 30 Q 110 40 110 60 L -110 60 Q -110 40 -126 30 L -126 -30 Q -110 -40 -110 -60 Z" fill={GOLD2} stroke={OL} strokeWidth={6} strokeLinejoin="round" />
    <path d="M -90 -44 L 90 -44 L 90 44 L -90 44 Z" fill="none" stroke="#C98A12" strokeWidth={3} strokeDasharray="8 6" />
    <T x={0} y={-16} s={22} c="#8A5A00">1 SHARE · ANT</T>
    <circle cx={-26} cy={12} r={mood === 'wow' ? 9 : 7} fill={OL} /><circle cx={26} cy={12} r={mood === 'wow' ? 9 : 7} fill={OL} />
    {mood === 'worry' ? <path d="M -16 40 Q 0 30 16 40" stroke={OL} strokeWidth={5} fill="none" strokeLinecap="round" />
      : mood === 'wow' ? <ellipse cx={0} cy={38} rx={9} ry={11} fill="#6B2E2A" stroke={OL} strokeWidth={3} />
      : <path d="M -16 32 Q 0 46 16 32" stroke={OL} strokeWidth={5} fill="none" strokeLinecap="round" />}
    {mood === 'worry' && <path d="M 60 -10 Q 66 4 60 12 Q 54 4 60 -10 Z" fill="#7FC8F8" stroke={OL} strokeWidth={2} />}
  </g>;
}

/** every set accepts `ox`: a horizontal offset so a set can sit in a later zone of a multi-zone world */
export const ANTIPO_SETS: Record<string, SetFn> = Object.fromEntries(Object.entries(RAW).map(([k, fn]) => [k, (t: number, z: Z, f: number) => {
  const ox = Number(z.ox ?? 0); if (!ox) return fn(t, z, f);
  return <g transform={`translate(${ox} 0)`}>{fn(t, {...z, x0: z.x0 - ox, x1: z.x1 - ox}, f)}</g>;
}]));

/** share: the golden ticket character */
const share: ItemFn = (a, {t, f}, i) => {
  const at = a.at ?? 0; if (t < at || (a.until !== undefined && t > a.until + 0.3)) return null;
  const x = kf(a.x, t, 960), y = kf(a.y, t, f - 120), s = kf(a.scale, t, 1) * pop(t, at, 0.4) * (a.until !== undefined && t > a.until ? 1 - clamp((t - a.until) / 0.3) : 1);
  const mood: string = pick(a.mood, t, 'happy');
  return <g key={'sh' + i} transform={`translate(${x} ${y})`}>{ticket(t + i, mood, s)}
    {a.label && t < (a.labelUntil ?? at + 3) && plaque(0, -100 * s, a.label, '#FFFFFF', 20)}</g>;
};

export const ANTIPO_ITEMS: Record<string, ItemFn> = {share};
export const ANTIPO_INDOOR = ['ajkitchen', 'ajlab', 'ajhall', 'ajscroll', 'ajsupply', 'ajcase', 'ajvault', 'ajtitle', 'ajbumper'];
