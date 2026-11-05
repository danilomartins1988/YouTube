import {getPointAtLength as gp, getTangentAtLength as gt} from '@remotion/paths';

export const pointAt = (d: string, l: number) => gp(d, l) ?? {x: 0, y: 0};
export const tangentAt = (d: string, l: number) => gt(d, l) ?? {x: 1, y: 0};
