import type {EnginePalette} from '../types';

/** Channel identity: navy and charcoal base, metallic gold, white, subtle blue; red only for risk. */
export const ENGINE_PALETTE: EnginePalette = {
  bg: '#07111F', bg2: '#0E1A2C', panel: '#101B2E', ink: '#F4F1EA', muted: '#8B98AA', grid: '#1B2A40',
  gold: '#D4AF5A', blue: '#5EA8E6', teal: '#7FC8B8', risk: '#FF5A5F', land: '#18283D', border: '#33475F',
};
export const FONT = {display: 'Inter Display, Inter, sans-serif', body: 'Inter, sans-serif'};
export const pal = (p?: Partial<EnginePalette>): EnginePalette => ({...ENGINE_PALETTE, ...(p || {})});
/** Resolve a palette key ('gold') or pass a literal colour through. */
export const col = (P: EnginePalette, c?: string, fallback = P.gold) => (c ? (P as any)[c] || c : fallback);
