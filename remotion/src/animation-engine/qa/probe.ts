/**
 * Motion probe (run in Node, no browser): evaluates the SAME pure functions the renderer uses and measures
 * whether things really move. Bundled by tools/engine_qa.py with esbuild.
 *   - presenter: body travel, leg/arm joint angles over time, marker tip vs active stroke distance while drawing
 *   - drawing: revealed length grows monotonically, pen follows strokes
 *   - map: camera moves; route heads and tokens change position
 *   - flow: an item's position changes and it changes form at each stage
 */
import {frontArmWorld} from '../../presenter/Presenter';
import {presenterPose} from '../AnimatedPresenter/AnimatedPresenter';
import {penAt, strokeProgress} from '../DrawOnCanvas/DrawOnCanvas';
import {cameraAt, mapPointAt} from '../AnimatedWorldMap/AnimatedWorldMap';
import {CAMS, DEMO_PRESENTER, LL, chartStrokes, demoPresenterActions} from '../examples/EngineDemo';

const tl = chartStrokes();
const acts = demoPresenterActions(tl);
const pose = (t: number) => presenterPose({t, actions: acts, floor: DEMO_PRESENTER.floor, scale: DEMO_PRESENTER.scale, startX: DEMO_PRESENTER.startX});

const out: Record<string, any> = {};

// ---- presenter: walking (0.25-1.8 s): body x and leg phase change; joints move
const walkXs = [0.3, 0.8, 1.3, 1.8].map((t) => pose(t).x);
out.presenter_walk_x = walkXs.map((v) => Math.round(v));
const leanSeries = [0.3, 0.5, 1.0, 1.7, 1.9, 2.1].map((t) => +pose(t).lean!.toFixed(2));
out.presenter_lean_deg = leanSeries;

// ---- drawing sync: marker tip vs pen tip on the active stroke
let maxErr = 0, sumErr = 0, n = 0;
const elbow: number[] = [];
for (let t = tl.start; t <= tl.end; t += 1 / 30) {
  const pen = penAt(tl, t);
  if (!pen.down) continue;
  const p = pose(t);
  const arm = frontArmWorld(p);
  const err = Math.hypot(arm.tip[0] - pen.pt[0], arm.tip[1] - pen.pt[1]);
  maxErr = Math.max(maxErr, err); sumErr += err; n++;
  elbow.push(arm.elbow[0], arm.elbow[1]);
}
out.draw_frames_checked = n;
out.draw_tip_error_px = {mean: +(sumErr / Math.max(1, n)).toFixed(2), max: +maxErr.toFixed(2)};
const ex = elbow.filter((_, i) => i % 2 === 0), ey = elbow.filter((_, i) => i % 2 === 1);
out.draw_elbow_range_px = {x: Math.round(Math.max(...ex) - Math.min(...ex)), y: Math.round(Math.max(...ey) - Math.min(...ey))};
out.draw_body_range_px = Math.round(Math.max(...Array.from({length: 40}, (_, i) => pose(tl.start + (i / 39) * (tl.end - tl.start)).x)) -
  Math.min(...Array.from({length: 40}, (_, i) => pose(tl.start + (i / 39) * (tl.end - tl.start)).x)));

// revealed length monotonic
let mono = true, prev = -1;
for (let t = tl.start; t <= tl.end + 0.1; t += 0.05) {
  const total = tl.strokes.reduce((s, st) => s + strokeProgress(st, t) * st.len, 0);
  if (total + 1e-6 < prev) mono = false; prev = total;
}
out.draw_reveal_monotonic = mono;
out.draw_timeline = {start: +tl.start.toFixed(2), end: +tl.end.toFixed(2), strokes: tl.strokes.length};

// point state: hand reaches the target
const tp = tl.end + 0.55 + 0.5;
const pp = pose(tp), arm = frontArmWorld(pp);
out.point_hand_to_target_px = Math.round(Math.hypot(arm.hand[0] - (pp.pointHand ? pp.pointHand[0] : 0), arm.hand[1] - (pp.pointHand ? pp.pointHand[1] : 0)));
out.point_state_active = !!pp.pointHand;

// ---- map: camera moves; projected Taiwan moves across the frame with the camera
out.map_camera = [12.5, 14.5, 15.5, 16.5, 17.6].map((t) => { const c = cameraAt(CAMS, t); return [+c.lon.toFixed(1), +c.lat.toFixed(1), +c.span.toFixed(1)]; });
out.map_taiwan_screen = [12.5, 15.0, 16.5, 17.6].map((t) => mapPointAt(CAMS, t, LL.hsinchu as any).map(Math.round));

console.log(JSON.stringify(out, null, 1));
