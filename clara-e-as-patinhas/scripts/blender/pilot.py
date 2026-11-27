"""Pilot "Pata Pata Patatá" - ONE universal animation for EN (original), PT and ES (Aditivo 03).

  blender -b rendering/pilot.blend -P pilot.py -- stills OUTPREFIX F1 F2 ...   [env PILOT_FAST=1 for layout checks]
  blender -b rendering/pilot.blend -P pilot.py -- render START END OUTDIR

Choreography is driven by the shared BEAT GRID of the timing map (music/compositions/pilot/timing_map.json), not by
one language's words, so the same moves land on "au/woof/guau", "pula/jump/salta" etc. in every language.
Lip-sync is stylised and universal: Clara's mouth follows the max loudness of the EN/PT/ES vocal stems
(music/compositions/pilot/mouth_30fps.json) with a syllable flutter, no language-specific shapes.
Rig names are internal: 'tifa' = Toby (male, forelock), 'milo' = the cat (cast5.py). 30 fps, 1920x1080."""
import bpy, sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
from cp_lib import reset_pose
from cp_motion import Acc, ease, bump, breathe, tail_wag, ear_flick, blink_amount, sway, clap, wave, hop, paw_lift
from cp_chars import face

ROOTP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TM = json.load(open(os.path.join(ROOTP, 'music', 'compositions', 'pilot', 'timing_map.json')))
MOUTH = json.load(open(os.path.join(ROOTP, 'music', 'compositions', 'pilot', 'mouth_30fps.json')))['mouth']
FPS = 30
BPM = TM['bpm']; BEAT = 60.0 / BPM; BAR = 4 * BEAT
SEC = [(s['name'], s['start_ms'] / 1000, s['end_ms'] / 1000) for s in TM['sections']]
DUR = TM['duration_ms'] / 1000; END_T = DUR + 1.0
CAST = ('clara', 'ayra', 'pandora', 'tifa', 'milo')
POS = {'clara': (0.0, 0.62), 'ayra': (-0.78, 0.0), 'pandora': (-0.4, -0.32), 'tifa': (0.38, -0.32), 'milo': (0.78, 0.0)}
TEST = bool(os.environ.get('PILOT_TEST'))  # 'all five' animation test (Aditivo 01 sec. 41): every character does its move in chorus 1
VERSE_OF = {'ayra': 'ayra', 'pandora': 'pandora', 'toby': 'tifa', 'milo': 'milo'}
BASE_SCALE = {}; BASE_Z = {}


def section(t):
    for n, a, b in SEC:
        if a <= t < b:
            return n, a, b
    return ('end', DUR, END_T)


def seg(t, a, b):
    return min(1.0, max(0.0, (t - a) / (b - a))) if b > a else float(t >= b)


def events(sec_start, t):
    """Beat events of a character verse: lines 0/3 'NAME does x, x, x' -> beats 2,2.5,3 ; lines 1/2 'x, x, x' -> beats 0.25,1,1.75."""
    out = []
    for line, offs in ((0, (2.0, 2.5, 3.0)), (1, (0.25, 1.0, 1.75)), (2, (0.25, 1.0, 1.75)), (3, (2.0, 2.5, 3.0))):
        for o in offs:
            out.append(sec_start + line * BAR + o * BEAT)
    return out


def pulse(t, evs, dur=0.28):
    v = 0.0
    for e in evs:
        if e - 0.04 < t < e + dur:
            v = max(v, bump(seg(t, e - 0.04, e + dur)))
    return v


def hop_amount(t, evs, dur=0.42):
    for e in evs:
        if e - 0.08 <= t < e - 0.08 + dur:
            return seg(t, e - 0.08, e - 0.08 + dur)
    return None


def pose(name, arm, t):
    A = Acc(); breathe(A, arm, t)
    sname, s0, s1 = section(t)
    dog = name != 'clara'
    expr = 'happy'; mouth = None; z = 0.0; spin = 0.0
    beat = (t - s0) / BEAT; line = int(beat // 4); bl = beat % 4
    if dog:
        tail_wag(A, arm, t, freq={'ayra': 2.4, 'pandora': 2.8, 'tifa': 3.4, 'milo': 1.2}[name], amp=18 if name != 'milo' else 12)
    if sname == 'intro':
        if name == 'clara':
            wave(A, arm, t, 'R', k=ease(seg(t, 0.3, 0.9)) * (1 - seg(t, 2.4, 2.9)))
    elif sname.startswith('chorus'):
        sway(A, arm, t, BPM, 0.8)
        lb = line % 4
        if lb == 2:  # "bate palma, bate o pe" / "clap your hands and stomp your feet"
            if name == 'clara':
                if bl < 2.0:
                    clap(A, arm, (bl % 1.0))
                else:
                    k = bump(seg(bl, 2.0, 3.0)); A.rot('thigh_R', -28 * k, 0, 0); A.rot('shin_R', 30 * k, 0, 0)
            else:
                paw_lift(A, arm, seg(bl, 2.0, 3.2), 'L' if name in ('ayra', 'tifa') else 'R')
        elif 2.8 < bl < 3.6 and dog:  # small hop on "patata / hooray"
            hop(A, arm, seg(bl, 2.8, 3.6), height=0.05)
        elif name == 'clara' and lb in (0, 1, 3):
            clap(A, arm, (bl % 1.0) * 0.6) if bl > 3.0 else None
    elif sname in ('ayra', 'pandora', 'toby', 'milo') or (TEST and sname.startswith('chorus')):
        star = name if (TEST and sname.startswith('chorus')) else VERSE_OF[sname]; evs = events(s0, t)
        if TEST and name == 'clara':
            clap(A, arm, (bl % 1.0)); star = None
        elif name == star:
            if name == 'ayra':
                k = pulse(t, evs); mouth = 0.95 * k; A.rot('head', -14 * k, 0, 0); A.rot('neck', -8 * k, 0, 0)
                u = hop_amount(t, evs, 0.3)
                if u is not None: hop(A, arm, u, height=0.03)
            elif name == 'pandora':
                u = hop_amount(t, evs, 0.42)
                if u is not None: hop(A, arm, u, height=0.11)
                mouth = 0.4
            elif name == 'tifa':
                first = [e for i, e in enumerate(evs) if i % 3 == 0]
                for e in first:
                    if e - 0.1 <= t < e + 2 * BEAT * (0.75 if (e - s0) % BAR < 1.0 else 0.5) + 0.25:
                        L = 2 * BEAT * (0.75 if (e - s0) % BAR < 1.0 else 0.5) + 0.35
                        spin = 360 * ease(seg(t, e - 0.1, e - 0.1 + L))
                        hop(A, arm, seg(t, e - 0.1, e - 0.1 + L), height=0.02)
                mouth = 0.45 + 0.4 * pulse(t, evs)
            elif name == 'milo':
                k = pulse(t, evs, 0.35); mouth = 0.85 * k; A.rot('head', -10 * k, 18 * k, 0)
            if line == 4:  # "balanca o rabinho / wag your little tail / mueve la colita"
                tail_wag(A, arm, t, freq=4.0, amp=40)
            expr = 'happy'
        elif star is not None:
            # watchers: look toward the star, little bounces on the beat
            if dog:
                if line == 4: tail_wag(A, arm, t, freq=4.0, amp=40)
                sway(A, arm, t, BPM, 0.35)
            dx = POS[star][0] - POS[name][0]
            A.rot('head', 0, 0, max(-25, min(25, -28 * dx)))
            expr = 'curious' if bl < 1 and line == 0 else 'happy'
    elif sname == 'clara':
        if name == 'clara':
            if line < 3:
                clap(A, arm, (bl % 1.0))
            elif line == 3:
                spin = 360 * ease(seg(bl, 0.5, 3.5))
            else:
                sway(A, arm, t, BPM, 1.0); clap(A, arm, (bl % 1.0)) if bl % 2 < 1 else None
        else:
            if line < 3:
                sway(A, arm, t, BPM, 0.5)
                A.rot('head', 0, 0, max(-25, min(25, 28 * POS[name][0])))
            else:  # everybody dances: hops on beats 1 and 3
                for b0 in (0.0, 2.0):
                    if b0 <= bl < b0 + 0.9: hop(A, arm, seg(bl, b0, b0 + 0.9), height=0.06)
    elif sname == 'outro':
        u = seg(t, s0, s1)
        if name == 'clara':
            spin = 360 * ease(seg(u, 0.0, 0.5)); wave(A, arm, t, 'R', k=ease(seg(u, 0.5, 0.8)))
        else:
            if 0.55 < u < 0.8: hop(A, arm, seg(u, 0.55, 0.8), height=0.07)
            if name == 'ayra' and 0.7 < u < 0.9: mouth = 0.9 * bump(seg(u, 0.7, 0.9))
            if name == 'milo' and 0.75 < u < 0.95: mouth = 0.9 * bump(seg(u, 0.75, 0.95))
    else:  # end hold
        if name == 'clara': wave(A, arm, t, 'R', k=1.0)
    # Clara sings (universal stylised lip-sync)
    if name == 'clara' and sname not in ('intro', 'end'):
        i = int(round(t * FPS)); m = MOUTH[i] if 0 <= i < len(MOUTH) else 0.0
        flutter = 0.55 + 0.45 * abs(math.sin(math.pi * (t / (BEAT / 2))))
        mouth = m * flutter
    blink = blink_amount(t, 3.6 if name == 'clara' else 4.2, 0.15, seed={'clara': 0.0, 'ayra': 0.7, 'pandora': 1.9, 'tifa': 2.6, 'milo': 3.3}[name])
    if name == 'milo':
        blink = max(blink, 0.7 * bump(seg((t % 6.0), 4.6, 5.4)))  # slow cat blink
    face(arm, expr, blink=blink, mouth_open=(mouth if mouth is not None else (0.0 if name == 'clara' else 0.25)), A=A)
    A.apply(arm)
    return spin


def update(scene, depsgraph=None):
    tc = (scene.frame_current - 1) / FPS                       # whole frame: picks the camera shot (no blur smear across cuts)
    t = (scene.frame_current - 1 + scene.frame_subframe) / FPS  # sub-frame time: real motion blur on the characters
    for name in CAST:
        arm = bpy.data.objects[name]; reset_pose(arm)
        spin = pose(name, arm, t)
        x, y = POS[name]
        arm.location = (x, y, BASE_Z[name])
        arm.rotation_euler = (0, 0, math.radians(spin))
    camera(scene, t, tc)
    for k in range(5):
        b = bpy.data.objects.get(f'butterfly_{k}')
        if b:
            cx, cy = (-2.2, 1.6) if k < 3 else (1.8, 1.2)
            b.location = (cx + 0.9 * math.sin(0.5 * t + k * 1.7), cy + 0.6 * math.sin(0.37 * t + k), 0.6 + 0.25 * math.sin(1.3 * t + k * 0.9))
            for s in (1, -1):
                pv = bpy.data.objects.get(f'bf_wingpiv_{k}_{s}')
                if pv: pv.rotation_euler = (0, s * math.radians(55) * math.sin(2 * math.pi * 9 * t + k), 0)


WIDE = ((0.0, -2.55, 0.82), (0.0, 0.12, 0.34), 30)
def shot_for(sname, t, s0, s1):
    if sname == 'intro':
        u = ease(seg(t, s0, s1)); p0, p1 = Vector((0.0, -5.0, 1.8)), Vector(WIDE[0])
        return p0.lerp(p1, u), Vector(WIDE[1]), 30
    if sname in ('ayra', 'pandora', 'toby', 'milo'):
        n = VERSE_OF[sname]; x, y = POS[n]; u = seg(t, s0, s1)
        tg = Vector((x * 0.85, y + 0.15, 0.3)); pos = Vector((x * 0.7 + 0.2 * (u - 0.5), y - 1.95, 0.6))
        return pos, tg, 33
    if sname == 'clara':
        u = seg(t, s0, s1)
        return Vector((0.15 * (u - 0.5), -2.2, 0.75)), Vector((0, 0.1, 0.42)), 34
    if sname == 'outro' or sname == 'end':
        u = ease(seg(t, s0, END_T)); return Vector(WIDE[0]).lerp(Vector((0.0, -4.6, 1.6)), u), Vector(WIDE[1]), 30
    u = seg(t, s0, s1)  # choruses: wide, gentle drift
    return Vector(WIDE[0]) + Vector((0.35 * math.sin(math.pi * (u - 0.5)), 0.2 * u, 0)), Vector(WIDE[1]), WIDE[2]


def camera(scene, t, tc=None):
    sname, s0, s1 = section(tc if tc is not None else t)
    if tc is not None and section(t)[0] != sname:
        t = tc
    pos, tg, lens = shot_for(sname, t, s0, s1)
    cam = scene.camera; cam.location = pos; cam.data.lens = lens
    cam.rotation_euler = (tg - pos).to_track_quat('-Z', 'Y').to_euler()
    f = bpy.data.objects.get('ep2_focus')
    if f: f.location = tg


def setup(pct=100):
    sc = bpy.context.scene
    from ep2_scene import level
    level('L1M', pct)
    from cp_env import ground_h
    for n in CAST:
        o = bpy.data.objects[n]; BASE_SCALE[n] = o.scale[0]
        x, y = POS[n]; BASE_Z[n] = max(ground_h(x, y), 0.0)
    if os.environ.get('PILOT_NOMB'):  # re-render of camera-cut frames: no motion blur (avoids smear across the cut)
        sc.eevee.use_motion_blur = False
    if os.environ.get('PILOT_FAST'):
        e = sc.eevee; e.taa_render_samples = 1; e.use_motion_blur = False; e.use_soft_shadows = False; e.use_gtao = False
        e.use_bloom = False; sc.camera.data.dof.use_dof = False; sc.use_nodes = False
    sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = int(END_T * FPS)
    sc.render.image_settings.file_format = 'PNG'
    bpy.app.handlers.frame_change_pre.clear(); bpy.app.handlers.frame_change_pre.append(update)


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    if args[0] == 'stills':
        setup(int(os.environ.get('PILOT_PCT', '100'))); sc = bpy.context.scene
        import time
        for f in args[2:]:
            t0 = time.time(); sc.frame_set(int(f)); sc.render.filepath = f'{args[1]}_{int(f):05d}.png'
            bpy.ops.render.render(write_still=True); print(f'RENDER_TIME f{f} {time.time() - t0:.1f}s', flush=True)
    elif args[0] == 'render':
        s0, s1, outdir = int(args[1]), int(args[2]), args[3]
        setup(int(os.environ.get('PILOT_PCT', '100'))); sc = bpy.context.scene; os.makedirs(outdir, exist_ok=True)
        sc.frame_start = s0; sc.frame_end = s1; sc.render.use_overwrite = bool(os.environ.get('PILOT_NOMB')); sc.render.use_placeholder = False
        sc.render.filepath = os.path.join(outdir, 'f#####')
        bpy.ops.render.render(animation=True)
