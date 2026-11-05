import React from 'react';
import type {Props} from './types';

export const GeoCtx = React.createContext<Props['geo']>({});
export const useGeo = (name: string) => {
  const g = React.useContext(GeoCtx) || {};
  if (!g[name]) throw new Error(`geo layer '${name}' missing from props`);
  return g[name];
};
