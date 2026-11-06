/** Shared types for The Hidden Economics animation engine. All times are SECONDS on the composition clock
 * (frame / fps); every component is a pure function of `t`, so renders are deterministic. */
export type Vec = [number, number];
export type LonLat = [number, number];

export type EnginePalette = {
  bg: string; bg2: string; panel: string; ink: string; muted: string; grid: string;
  gold: string; blue: string; teal: string; risk: string; land: string; border: string;
};

/** Optional per-component theme override. */
export type Themed = {palette?: Partial<EnginePalette>};

/** World geometry in the format of assets/geo/remotion_world.json (`paths`: ISO3 -> 'Mx,y x,y ...Z'). */
export type WorldGeo = {view?: number[]; paths: Record<string, string>};
