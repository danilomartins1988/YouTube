// Batch still renderer: bundles once, renders many compositions/props. Usage:
//   node scripts/render_stills.mjs jobs.json        (jobs: [{composition, props, out, scale}])
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';

const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
for (const j of jobs) {
  const composition = await selectComposition({serveUrl, id: j.composition, inputProps: j.props});
  await renderStill({serveUrl, composition, output: j.out, inputProps: j.props, scale: j.scale ?? 1, imageFormat: 'png'});
  console.log('rendered', j.out);
}
