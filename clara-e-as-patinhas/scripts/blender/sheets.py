"""Model-sheet raw renders. blender -b -P sheets.py -- NAME|lineup|group
Writes rendering/sheets_raw/<name>_<view>.png ; compose with scripts/compose_sheets.py"""
import bpy, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
from cp_lib import *; from cp_chars import *; from cp_render import *; from cp_motion import *
OUT = os.path.join(ROOT, 'rendering', 'sheets_raw'); os.makedirs(OUT, exist_ok=True)
arg = sys.argv[sys.argv.index('--') + 1]
HZ = {'clara': 0.83}
SIZE = {'clara': 1.0, 'ayra': 0.36, 'pandora': 0.27, 'tifa': 0.24}


def render(path):
    bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True)


def char_sheet(name):
    clear_scene(); sc = bpy.context.scene
    arm = build(name); eevee(sc, (900, 1100), 24); studio(sc)
    h = SIZE[name]; mid = h * 0.52
    dist = h * 3.4 if name == 'clara' else h * 4.2
    views = {'front': (0, -1), 'q34': (0.72, -0.7), 'side': (1, 0), 'back': (0, 1)}
    for v, (dx, dy) in views.items():
        reset_pose(arm); face(arm, 'happy', mouth_open=0.0)
        camera(sc, (dx * dist, dy * dist, mid + h * 0.08), (0, 0, mid), 50, f'c_{v}')
        render(f'{OUT}/{name}_{v}.png')
    # expressions (head close-ups, slight 3/4)
    sc.render.resolution_x = sc.render.resolution_y = 700
    if name == 'clara':
        hc = Vector((0, 0, 0.83)); d = 0.75
    else:
        s = DOGS[name]['scale']; hx, hy, hz = DOGS[name]['head_pos']; hc = Vector((0, hy * s, hz * s)); d = 0.42 * s / 0.72
    for e in ('happy', 'curious', 'surprised', 'focused', 'affectionate'):
        reset_pose(arm); A = Acc(); face(arm, e, A=A); A.apply(arm)
        camera(sc, hc + Vector((0.3, -1, 0.12)).normalized() * d, hc, 85, f'e_{e}')
        render(f'{OUT}/{name}_expr_{e}.png')
    # dance pose
    sc.render.resolution_x, sc.render.resolution_y = 900, 1100
    reset_pose(arm); A = Acc()
    if name == 'clara':
        arms_up(A, arm, 0.8); clara_step(A, arm, 0.5, 'L'); face(arm, 'happy', A=A)
    else:
        paw_lift(A, arm, 0.5, 'L'); A.rot('tail', 0, 0, 25); A.rot('head', 0, 12, 0); face(arm, 'happy', A=A)
    A.apply(arm)
    camera(sc, (0.72 * dist, -0.7 * dist, mid + h * 0.1), (0, 0, mid), 50, 'c_pose')
    render(f'{OUT}/{name}_pose.png')


def lineup():
    clear_scene(); sc = bpy.context.scene
    arms = {n: build(n) for n in ('clara', 'ayra', 'pandora', 'tifa')}
    xs = {'clara': 0.0, 'ayra': 0.55, 'pandora': 0.98, 'tifa': 1.33}
    for n, a in arms.items():
        a.location = (xs[n], 0, 0); reset_pose(a); face(a, 'happy', mouth_open=0.0)
    eevee(sc, (1800, 1100), 24); studio(sc)
    cd = bpy.data.cameras.new('o'); cd.type = 'ORTHO'; cd.ortho_scale = 1.95
    c = bpy.data.objects.new('o', cd); sc.collection.objects.link(c); c.location = (0.66, -5, 0.52); c.rotation_euler = (math.radians(90), 0, 0)
    sc.camera = c
    render(f'{OUT}/lineup.png')


def group():
    """Group image in the garden (uses the episode build helpers at full LOD)."""
    from cp_env import build_env
    clear_scene(); sc = bpy.context.scene
    build_env(sc)
    arms = {n: build(n) for n in ('clara', 'ayra', 'pandora', 'tifa')}
    pos = {'clara': (0.0, 0.0, 0), 'ayra': (0.55, -0.15, 10), 'pandora': (-0.5, -0.2, -15), 'tifa': (0.95, -0.25, 20)}
    for n, a in arms.items():
        x, y, hd = pos[n]; a.location = (x, y, 0); a.rotation_euler = (0, 0, math.radians(hd)); reset_pose(a)
        A = Acc()
        if n == 'clara':
            wave(A, a, 0.1, 'R', 1.0)
        else:
            A.rot('head', 0, 10, 0); A.rot('tail', 0, 0, 20)
        face(a, 'happy', A=A); A.apply(a)
    eevee(sc, (1920, 1080), 32)
    camera(sc, (0.35, -2.85, 0.62), (0.2, 0, 0.42), 32)
    render(f'{OUT}/group.png')


if arg == 'lineup':
    lineup()
elif arg == 'group':
    group()
else:
    char_sheet(arg)
print('SHEETS DONE', arg)
