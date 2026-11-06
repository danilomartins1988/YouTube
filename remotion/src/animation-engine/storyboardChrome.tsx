import React from 'react';
import {E, FONT, ENGINE_PALETTE as P, win} from './motion';

/** Scene title block used by the storyboard adapters (rises in at the start of the scene). */
export const Chrome: React.FC<{title?: string; subtitle?: string; t: number}> = ({title, subtitle, t}) => {
  if (!title) return null;
  const u = E.out(win(t, 0.2, 0.6));
  return (
    <g opacity={u} transform={`translate(0 ${12 * (1 - u)})`}>
      <text x={120} y={150} fill={P.ink} fontFamily={FONT.display} fontWeight={800} fontSize={50}>{title}</text>
      {subtitle && <text x={122} y={192} fill={P.muted} fontFamily={FONT.body} fontSize={26}>{subtitle}</text>}
    </g>
  );
};
