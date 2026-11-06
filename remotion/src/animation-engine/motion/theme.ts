import type {EnginePalette} from '../types';

/** Channel identity: navy and charcoal base, metallic gold, white, subtle blue; red only for risk. */
export const ENGINE_PALETTE: EnginePalette = {
  bg: '#07111F', bg2: '#0E1A2C', panel: '#101B2E', ink: '#F4F1EA', muted: '#8B98AA', grid: '#1B2A40',
  gold: '#D4AF5A', blue: '#5EA8E6', teal: '#7FC8B8', risk: '#FF5A5F', land: '#18283D', border: '#33475F',
};
export const FONT = {display: 'Inter Display, Inter, sans-serif', body: 'Inter, sans-serif'};
export const pal = (p?: Partial<EnginePalette>): EnginePalette => ({...ENGINE_PALETTE, ...(p || {})});
/** Episode palettes name their colours accent / accent2 / accent3; map them onto the engine's names. */
const ALIAS: Record<string, keyof EnginePalette> = {accent: 'gold', accent2: 'blue', accent3: 'teal', land: 'land', border: 'border', bg2: 'bg2'};
/** Resolve a palette key ('gold', 'accent2', ...) or pass a literal colour through. */
export const col = (P: EnginePalette, c?: string, fallback = P.gold) => {
  if (!c) return fallback;
  const k = (P as any)[c] !== undefined ? c : ALIAS[c];
  return k ? (P as any)[k] : c;
};
/** Engine palette from an episode palette (keys bg, bg2, ink, muted, land, border, accent, accent2, accent3, risk). */
export const fromEpisodePalette = (e: Record<string, string>): Partial<EnginePalette> => ({
  bg: e.bg, bg2: e.bg2, panel: e.bg2, ink: e.ink, muted: e.muted, land: e.land, border: e.border,
  gold: e.accent, blue: e.accent2 || ENGINE_PALETTE.blue, teal: e.accent3 || ENGINE_PALETTE.teal, risk: e.risk || ENGINE_PALETTE.risk,
});
