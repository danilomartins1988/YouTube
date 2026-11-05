// Shapes of the render input produced by hiddeneco (python -m hiddeneco build ... --renderer remotion).

export type Word = {word: string; start: number; end: number}; // seconds, relative to scene start

export type SceneSpec = {
  id: string;
  type: string;
  params: Record<string, any>;
  narration: string;
  duration: number; // seconds
  lead: number; // seconds before speech starts
  speech: number; // seconds of narration audio
  words: Word[];
  credits: string[];
  chapter: string;
  preview_t?: number; // layout previews only
  frames?: number; // layout previews only
};

export type Palette = {
  bg: string;
  bg2: string;
  ink: string;
  muted: string;
  land: string;
  border: string;
  accent: string;
  accent2: string;
  [k: string]: string;
};

export type Props = {
  fps: number;
  width: number;
  height: number;
  palette: Palette;
  fonts: {display: string; body: string};
  brand: string;
  transition?: 'fade' | 'race';
  background?: 'grid' | 'speed';
  scenes: SceneSpec[];
  geo?: Record<string, {view: [number, number, number, number]; paths: Record<string, string>; labels?: Record<string, [number, number]>}>;
};
