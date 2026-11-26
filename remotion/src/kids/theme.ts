import {continueRender, delayRender, staticFile} from 'remotion';

/* Kids channel look: bright, saturated, friendly. No pure red flashes, no strobe; every change eases. */
export const K = {
  sky1: '#7FD3FF', sky2: '#C9EEFF', sun: '#FFD23F', sunCheek: '#FF9DA7',
  hill1: '#7ED957', hill2: '#56C23F', hill3: '#3FA535',
  ink: '#2B2350', white: '#FFFFFF', cream: '#FFF8E7',
  pink: '#FF7EB6', orange: '#FF9F1C', yellow: '#FFD23F', green: '#3BCE6B', blue: '#3FA9F5', purple: '#9B6BFF',
  teal: '#2EC4B6', coral: '#FF6B6B',
};
export const RAINBOW = [K.coral, K.orange, K.yellow, K.green, K.blue, K.purple, K.pink, K.teal, K.orange, K.blue];
export const FONT = 'KidsFredoka, Fredoka, "Arial Rounded MT Bold", sans-serif';

let fontsLoaded = false;
export const loadKidsFonts = () => {
  if (fontsLoaded || typeof document === 'undefined') return;
  fontsLoaded = true;
  const handle = delayRender('kids fonts');
  const faces = [
    new FontFace('KidsFredoka', `url(${staticFile('kids/fonts/fredoka-latin-600-normal.woff2')})`, {weight: '600'}),
    new FontFace('KidsFredoka', `url(${staticFile('kids/fonts/fredoka-latin-700-normal.woff2')})`, {weight: '700'}),
  ];
  Promise.all(faces.map((f) => f.load()))
    .then((loaded) => {
      loaded.forEach((f) => (document.fonts as unknown as {add: (x: FontFace) => void}).add(f));
      continueRender(handle);
    })
    .catch(() => continueRender(handle));
};

/* ---------------------------------------------------------------- timeline (written by tools/kids_voice.py) */
export type Word = {w: string; s: number; e: number};
export type Line = {
  text: string; bar: number; section: string; kind: 'intro' | 'chorus' | 'number' | 'tag' | 'outro';
  start: number; end: number; words: Word[]; claps: number[];
  number?: number; animal?: AnimalKind; number_word?: string; sound?: string; total?: number; chorus_line?: number;
};
export type Timeline = {
  title: string; bpm: number; beat: number; bar: number; duration: number; voice: string;
  sections: {name: string; kind: string; start: number; end: number}[]; lines: Line[];
};
export type AnimalKind = 'duck' | 'cat' | 'dog' | 'cow' | 'sheep' | 'chick' | 'pig' | 'frog' | 'bee' | 'monkey';
export const ALL_ANIMALS: AnimalKind[] = ['duck', 'cat', 'dog', 'cow', 'sheep', 'chick', 'pig', 'frog', 'bee', 'monkey'];

/* ---------------------------------------------------------------- beat helpers */
/** 0..1 hop on every beat: up quickly, land softly (|sin| shaped). */
export const hop = (t: number, beat: number, phase = 0) => Math.abs(Math.sin(Math.PI * ((t / beat + phase) % 1)));
/** squash at the landing of each beat: 1 at the downbeat decaying to 0 */
export const landing = (t: number, beat: number, phase = 0) => {
  const u = (t / beat + phase) % 1;
  return Math.exp(-u * 9);
};
export const lineAt = (tl: Timeline, t: number): Line | undefined => {
  let cur: Line | undefined;
  for (const l of tl.lines) if (t >= l.start - 0.25) cur = l;
  return cur;
};
export const isTalking = (line: Line | undefined, t: number) =>
  !!line && line.words.some((w) => t >= w.s && t <= w.e);
