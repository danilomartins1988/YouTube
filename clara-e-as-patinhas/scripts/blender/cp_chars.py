"""Procedural character builders: Clara, Ayra (Border Collie red merle), Pandora (white Pomeranian),
Tifa (Yorkshire Terrier). Rigid parts bound to simple bone rigs. Forward = -Y, up = +Z, character left = +X.
Every character lives under an armature named after it; all parts in collection CH_<name>."""
import bpy, math
import numpy as np
from mathutils import Vector
from cp_lib import *
from cp_lib import _finish

# ---------------------------------------------------------------- palette (sRGB)
PAL = {
    'skin': (0.99, 0.84, 0.73), 'cheek': (0.98, 0.58, 0.60), 'hair': (0.36, 0.20, 0.10), 'eye_brown': (0.42, 0.24, 0.10),
    'overall': (1.0, 0.78, 0.10), 'overall_dark': (0.93, 0.64, 0.05), 'shirt': (0.97, 0.97, 0.95),
    'shoe_pink': (0.98, 0.42, 0.62), 'shoe_blue': (0.35, 0.70, 0.98), 'sole': (0.98, 0.98, 0.98),
    'mouth': (0.55, 0.12, 0.16), 'tongue': (0.97, 0.47, 0.52), 'nose_dog': (0.07, 0.06, 0.06),
    'eye_dark': (0.07, 0.05, 0.04), 'eye_blue': (0.45, 0.75, 0.95),
    'bandana_blue': (0.18, 0.48, 0.95), 'bandana_green': (0.25, 0.75, 0.30), 'bow_pink': (0.99, 0.55, 0.72),
    'clip': (1.0, 0.85, 0.2),
}


def eye_parts(prefix, arm, bone_lid, c, radii, iris_col, iris_scale, lid_mat, coll_, yaw=0.0, pupil=0.55, white=True,
              head_bone='head'):
    """Stylised eye at centre c facing -Y (yawed by `yaw` degrees). Lid = hemisphere bound to a lid bone
    whose head is at the eye centre (rotate about X: open ~ -60, closed ~ +95)."""
    c = Vector(c)
    rx, ry, rz = radii
    rot = (0, 0, yaw)
    fwd = Vector((math.sin(math.radians(-yaw)) * 0, -1, 0))
    R = Euler((0, 0, math.radians(yaw))).to_matrix()
    if white:
        sc = ellipsoid(f'{prefix}_sclera', c, (rx, ry, rz), rot, mat('eye_white', (0.98, 0.98, 0.98), rough=0.15, spec=0.8),
                       segs=32, rings=16, sub=1, collection=coll_)
        bind(sc, arm, head_bone)
    ir = ellipsoid(f'{prefix}_iris', c + R @ Vector((0, -ry * (0.55 if white else 0.0), 0)),
                   (rx * iris_scale, ry * 0.6, rz * iris_scale), rot,
                   mat(f'iris_{prefix}', iris_col, rough=0.12, spec=0.9, coat=0.6), sub=1, collection=coll_)
    bind(ir, arm, head_bone)
    pu = ellipsoid(f'{prefix}_pupil', c + R @ Vector((0, -ry * (0.55 if white else 0.0) - ry * 0.25, 0)),
                   (rx * iris_scale * pupil, ry * 0.4, rz * iris_scale * pupil), rot,
                   mat('pupil', (0.02, 0.02, 0.02), rough=0.1, spec=1.0, coat=0.8), sub=1, collection=coll_)
    bind(pu, arm, head_bone)
    front = -(ry * (0.55 if white else 0.0) + ry * 0.62)
    hl = ellipsoid(f'{prefix}_hl1', c + R @ Vector((rx * 0.28, front, rz * 0.32)), (rx * 0.2, rx * 0.12, rx * 0.2), rot,
                   mat('eye_hl', (1, 1, 1), emis=(1, 1, 1), emis_str=3.0), segs=12, rings=8, sub=0, collection=coll_)
    hl2 = ellipsoid(f'{prefix}_hl2', c + R @ Vector((-rx * 0.25, front + 0.001, -rz * 0.3)), (rx * 0.09, rx * 0.06, rx * 0.09),
                    rot, mat('eye_hl', (1, 1, 1)), segs=10, rings=6, sub=0, collection=coll_)
    bind(hl, arm, head_bone); bind(hl2, arm, head_bone)
    # eyelid: upper hemisphere, big enough to cover highlights when closed
    lid = ellipsoid(f'{prefix}_lid', c, (rx * 1.12, ry * 1.0 + abs(front) * 0.9 + 0.004, rz * 1.12), rot, lid_mat,
                    cut=lambda d: d.z < -0.05, segs=32, rings=16, sub=1, collection=coll_)
    bind(lid, arm, bone_lid)
    return lid


# ====================================================================== CLARA
def build_clara():
    C = coll('CH_clara')
    H = 1.0
    bones = [
        ('root', (0, 0, 0), (0, 0, 0.12), None), ('hips', (0, 0, 0.42), (0, 0, 0.52), 'root'),
        ('chest', (0, 0, 0.52), (0, 0, 0.66), 'hips'), ('head', (0, 0, 0.68), (0, 0, 0.92), 'chest'),
        ('lid_L', (0.058, -0.122, 0.83), (0.058, -0.2, 0.83), 'head'), ('lid_R', (-0.058, -0.122, 0.83), (-0.058, -0.2, 0.83), 'head'),
        ('brow_L', (0.06, -0.13, 0.89), (0.06, -0.18, 0.89), 'head'), ('brow_R', (-0.06, -0.13, 0.89), (-0.06, -0.18, 0.89), 'head'),
        ('mouth_smile', (0, -0.14, 0.768), (0, -0.19, 0.768), 'head'), ('mouth_open', (0, -0.14, 0.768), (0, -0.19, 0.768), 'head'),
        ('mouth_o', (0, -0.14, 0.765), (0, -0.19, 0.765), 'head'),
    ]
    for s, x in (('L', 1), ('R', -1)):
        bones += [(f'thigh_{s}', (0.065 * x, 0, 0.44), (0.065 * x, 0, 0.24), 'hips'),
                  (f'shin_{s}', (0.065 * x, 0, 0.24), (0.065 * x, 0, 0.065), f'thigh_{s}'),
                  (f'foot_{s}', (0.065 * x, 0, 0.065), (0.065 * x, -0.07, 0.03), f'shin_{s}'),
                  (f'upperarm_{s}', (0.12 * x, 0, 0.635), (0.165 * x, 0, 0.52), 'chest'),
                  (f'forearm_{s}', (0.165 * x, 0, 0.52), (0.18 * x, 0, 0.41), f'upperarm_{s}')]
    arm = make_armature('clara', bones, C)
    skin = mat('clara_skin', PAL['skin'], rough=0.45, sss=0.15, spec=0.4)
    ov = mat('clara_overall', PAL['overall'], rough=0.55, sheen=0.3)
    ovd = mat('clara_overall_dark', PAL['overall_dark'], rough=0.6)
    shirt = mat('clara_shirt', PAL['shirt'], rough=0.6, sheen=0.3)
    hairm = hair_mat('clara_hair', PAL['hair'])
    B = lambda o, b: bind(o, arm, b)
    # ---- legs / shoes
    for s, x in (('L', 1), ('R', -1)):
        B(capsule(f'clara_thigh_{s}', (0.065 * x, 0, 0.45), (0.066 * x, 0, 0.24), 0.056, 0.05, ov, collection=C), f'thigh_{s}')
        B(capsule(f'clara_shin_{s}', (0.066 * x, 0, 0.245), (0.066 * x, 0.0, 0.085), 0.05, 0.045, ov, collection=C), f'shin_{s}')
        B(capsule(f'clara_cuff_{s}', (0.066 * x, 0, 0.1), (0.066 * x, 0, 0.085), 0.052, 0.052, ovd, collection=C), f'shin_{s}')
        B(ellipsoid(f'clara_ankle_{s}', (0.066 * x, 0.0, 0.075), (0.036, 0.036, 0.03), m=mat('sock', (0.98, 0.98, 0.98)), collection=C), f'foot_{s}')
        B(ellipsoid(f'clara_shoe_{s}', (0.066 * x, -0.022, 0.04), (0.048, 0.08, 0.038), m=mat('shoe_pink', PAL['shoe_pink'], rough=0.4, coat=0.3),
                    deform=lambda co: Vector((co.x, co.y, max(co.z, -0.03))), collection=C), f'foot_{s}')
        B(ellipsoid(f'clara_sole_{s}', (0.066 * x, -0.022, 0.014), (0.051, 0.083, 0.016), m=mat('sole', PAL['sole'], rough=0.5),
                    deform=lambda co: Vector((co.x, co.y, max(co.z, -0.012))), collection=C), f'foot_{s}')
        B(capsule(f'clara_stripe_{s}', (0.066 * x + 0.047 * x, -0.06, 0.04), (0.066 * x + 0.047 * x, 0.02, 0.045), 0.009, 0.009,
                  mat('shoe_blue', PAL['shoe_blue'], rough=0.4), collection=C), f'foot_{s}')
        B(ellipsoid(f'clara_lace_{s}', (0.066 * x, -0.06, 0.07), (0.022, 0.02, 0.008), (20, 0, 0), mat('shoe_blue', PAL['shoe_blue']), collection=C), f'foot_{s}')
    # ---- torso
    B(ellipsoid('clara_hips', (0, 0.005, 0.462), (0.12, 0.084, 0.098), m=ov, collection=C), 'hips')
    B(ellipsoid('clara_torso', (0, 0, 0.575), (0.118, 0.09, 0.105), m=shirt, collection=C), 'chest')
    bib = ellipsoid('clara_bib', (0, 0, 0.575), (0.124, 0.096, 0.111), m=ov, segs=48, rings=24,
                    cut=lambda d: not (d.y < -0.25 and abs(d.x) < 0.62 and d.z < 0.62), collection=C)
    sd = bib.modifiers.new('solid', 'SOLIDIFY'); sd.thickness = 0.008; sd.offset = 1.0
    bib.modifiers.move(1, 0)
    B(bib, 'chest')
    B(ellipsoid('clara_pocket', (0, -0.104, 0.55), (0.04, 0.006, 0.028), m=ovd, collection=C), 'chest')
    for x in (1, -1):
        B(ellipsoid(f'clara_button_{x}', (0.058 * x, -0.088, 0.618), (0.011, 0.006, 0.011), m=mat('button', (0.98, 0.55, 0.15), rough=0.3), segs=16, rings=8, collection=C), 'chest')
        B(tube_along(f'clara_strap_{x}', [(0.062 * x, -0.086, 0.625), (0.07 * x, -0.06, 0.672), (0.072 * x, 0.0, 0.688),
                                          (0.07 * x, 0.06, 0.66), (0.062 * x, 0.088, 0.6), (0.055 * x, 0.09, 0.54)],
                      [0.011] * 6, ov, segs=10, collection=C), 'chest')
    B(capsule('clara_neck', (0, 0, 0.64), (0, 0, 0.72), 0.036, 0.034, skin, collection=C), 'chest')
    # ---- arms
    for s, x in (('L', 1), ('R', -1)):
        B(ellipsoid(f'clara_sleeve_{s}', (0.122 * x, 0, 0.615), (0.05, 0.048, 0.05), m=shirt, collection=C), f'upperarm_{s}')
        B(capsule(f'clara_uarm_{s}', (0.125 * x, 0, 0.62), (0.165 * x, 0, 0.52), 0.032, 0.029, skin, collection=C), f'upperarm_{s}')
        B(capsule(f'clara_farm_{s}', (0.165 * x, 0, 0.52), (0.18 * x, 0, 0.42), 0.029, 0.025, skin, collection=C), f'forearm_{s}')
        B(ellipsoid(f'clara_hand_{s}', (0.183 * x, -0.004, 0.39), (0.03, 0.026, 0.036), m=skin, collection=C), f'forearm_{s}')
        B(ellipsoid(f'clara_thumb_{s}', (0.172 * x, -0.024, 0.398), (0.011, 0.011, 0.016), (0, 0, 0), skin, segs=12, rings=8, collection=C), f'forearm_{s}')
    # ---- head
    hc = Vector((0, 0, 0.83))
    B(ellipsoid('clara_head', hc, (0.155, 0.145, 0.15), m=skin, segs=48, rings=24,
                deform=lambda co: Vector((co.x * (1 + 0.06 * max(0, -co.z) / 0.15), co.y, co.z)), collection=C), 'head')
    for x in (1, -1):
        B(ellipsoid(f'clara_cheek_{x}', (0.094 * x, -0.104, 0.778), (0.03, 0.012, 0.02), (0, 0, -35 * x),
                    mat('cheek', PAL['cheek'], rough=0.6, sss=0.1), collection=C), 'head')
    B(ellipsoid('clara_nose', (0, -0.146, 0.792), (0.013, 0.01, 0.011), m=mat('clara_nose', (0.99, 0.76, 0.66), sss=0.15), segs=16, rings=8, collection=C), 'head')
    lidm = mat('clara_lid', PAL['skin'], rough=0.45, sss=0.15)
    for s, x in (('L', 1), ('R', -1)):
        eye_parts(f'clara_eye_{s}', arm, f'lid_{s}', (0.058 * x, -0.122, 0.83), (0.034, 0.02, 0.04), PAL['eye_brown'], 0.8,
                  lidm, C, yaw=14 * x)
        lash = curve_tube(f'clara_lash_{s}', [(0.03 * x, -0.142, 0.848), (0.058 * x, -0.148, 0.866), (0.09 * x, -0.134, 0.85)], 0.0028,
                          mat('lash', (0.15, 0.08, 0.05)), collection=C)
        B(lash, f'lid_{s}')
        brow = curve_tube(f'clara_brow_{s}', [(0.036 * x, -0.14, 0.888), (0.062 * x, -0.142, 0.896), (0.088 * x, -0.132, 0.886)], 0.0045,
                          mat('brow', (0.33, 0.18, 0.09)), collection=C)
        B(brow, f'brow_{s}')
    # mouths
    sm = curve_tube('clara_mouth_smile', [(-0.032, -0.137, 0.773), (-0.016, -0.143, 0.762), (0, -0.145, 0.759), (0.016, -0.143, 0.762),
                                          (0.032, -0.137, 0.773)], 0.0042, mat('mouth_line', PAL['mouth']), collection=C)
    B(sm, 'mouth_smile')
    op = ellipsoid('clara_mouth_open', (0, -0.138, 0.766), (0.03, 0.012, 0.022), m=mat('mouth_in', PAL['mouth'], rough=0.5),
                   cut=lambda d: d.z > 0.25, collection=C)
    B(op, 'mouth_open')
    tg = ellipsoid('clara_tongue', (0, -0.142, 0.752), (0.016, 0.008, 0.008), m=mat('tongue', PAL['tongue']), collection=C)
    B(tg, 'mouth_open')
    th = ellipsoid('clara_teeth', (0, -0.146, 0.769), (0.02, 0.006, 0.004), m=mat('teeth', (0.98, 0.98, 0.96)), collection=C)
    B(th, 'mouth_open')
    mo = ellipsoid('clara_mouth_o', (0, -0.141, 0.765), (0.013, 0.01, 0.017), m=mat('mouth_in', PAL['mouth']), collection=C)
    B(mo, 'mouth_o')
    # ---- hair (cap + back curtain + side fringe + tucked locks)
    B(solid(ellipsoid('clara_hair_cap', (0, 0.006, 0.838), (0.166, 0.158, 0.163), m=hairm, segs=48, rings=24,
                cut=lambda d: d.y < -0.42 and d.z < 0.5, collection=C), 0.012), 'head')
    B(solid(ellipsoid('clara_hair_back', (0, 0.025, 0.79), (0.172, 0.158, 0.175), m=hairm, segs=48, rings=24,
                cut=lambda d: (d.y < -0.40 and d.z < 0.55) or d.z > 0.7,
                deform=lambda co: Vector((co.x * (1 + 0.16 * max(0, -co.z) / 0.175), co.y * (1 + 0.1 * max(0, -co.z) / 0.175), co.z)), collection=C), 0.014), 'head')
    B(ellipsoid('clara_fringe', (-0.03, -0.122, 0.915), (0.112, 0.04, 0.05), (0, -16, -6), hairm, segs=32, rings=16,
                deform=lambda co: Vector((co.x, co.y + 2.2 * (co.x ** 2), co.z)), collection=C), 'head')
    B(ellipsoid('clara_fringe2', (0.07, -0.118, 0.925), (0.065, 0.035, 0.036), (0, 20, 12), hairm, segs=24, rings=12, collection=C), 'head')
    # hair accessory: little yellow flower clip on her left
    fc = Vector((0.118, -0.075, 0.935))
    clipm = mat('clip', PAL['clip'], rough=0.3, coat=0.5)
    for k in range(5):
        a = 2 * math.pi * k / 5
        B(ellipsoid(f'clara_clip_petal{k}', fc + Vector((0.016 * math.cos(a) * 0.8, -0.006, 0.016 * math.sin(a))),
                    (0.012, 0.006, 0.012), (0, 0, 35), clipm, segs=12, rings=8, collection=C), 'head')
    B(ellipsoid('clara_clip_center', fc + Vector((0, -0.01, 0)), (0.008, 0.006, 0.008), m=mat('clip_c', (0.98, 0.45, 0.55)), segs=12, rings=8, collection=C), 'head')
    neutral_clara(arm)
    return arm


def neutral_clara(arm):
    """Default face: smile on, other mouths hidden (scale 0), eyes open."""
    reset_pose(arm)
    face(arm, 'happy')


# ---------------------------------------------------------------- face / expression controls
LID_OPEN = -105


def face(arm, expr='happy', blink=0.0, mouth_open=None, A=None):
    """Set facial pose for any character (bones present are used). With an accumulator A, add into it."""
    def P(b, rot=(0, 0, 0), loc=(0, 0, 0), scale=None):
        if A is None:
            pose(arm, b, rot=rot, loc=loc, scale=scale)
        else:
            A.rot(b, *rot); A.loc(b, *loc)
            if scale is not None:
                A.scale(b, scale)
    pb = arm.pose.bones
    lid = {'happy': LID_OPEN, 'curious': LID_OPEN, 'surprised': LID_OPEN, 'focused': -8,
           'affectionate': -40}.get(expr, LID_OPEN)
    lid = lid + (100 - lid) * blink if blink else lid
    for s in ('L', 'R'):
        if f'lid_{s}' in pb:
            P(f'lid_{s}', rot=(lid, 0, 0))
    if 'brow_L' in pb:
        for s, x in (('L', 1), ('R', -1)):
            if expr == 'surprised':
                P(f'brow_{s}', loc=(0, 0, 0.014))
            elif expr == 'curious':
                P(f'brow_{s}', loc=(0, 0, 0.012 if s == 'L' else 0.0), rot=(0, (-10 if s == 'L' else 0) * x, 0))
            elif expr == 'focused':
                P(f'brow_{s}', loc=(0, 0, -0.006), rot=(0, 14 * x, 0))
            elif expr == 'affectionate':
                P(f'brow_{s}', loc=(0, 0, 0.004), rot=(0, -8 * x, 0))
    if 'mouth_smile' in pb:
        mo = {'happy': 'open', 'curious': 'o', 'surprised': 'o', 'focused': 'smile', 'affectionate': 'smile'}[expr]
        if mouth_open is not None:
            mo = 'open' if mouth_open > 0.15 else 'smile'
        for k in ('smile', 'open', 'o'):
            s = 1.0 if k == mo else 0.0
            if k == 'open' and mo == 'open' and mouth_open is not None:
                P('mouth_open', scale=(1.0, 1.0, 0.35 + 0.75 * mouth_open))
            elif k == 'o' and expr == 'surprised' and mo == 'o':
                P('mouth_o', scale=1.3)
            elif k == 'smile' and expr == 'focused':
                P('mouth_smile', scale=(0.6, 1, 0.5))
            else:
                P(f'mouth_{k}', scale=s if s else 0.0001)
    if 'jaw' in pb:  # dogs
        jo = {'happy': 0.6, 'curious': 0.0, 'surprised': 0.8, 'focused': 0.0, 'affectionate': 0.3}[expr]
        if mouth_open is not None:
            jo = mouth_open
        P('jaw', rot=(-22 * jo, 0, 0))
        P('tongue', scale=max(0.0001, min(1, jo * 1.6)))
    if 'ear_L' in pb:
        e = {'happy': 0, 'curious': 1, 'surprised': 2, 'focused': 0, 'affectionate': 3}[expr]
        for s, x in (('L', 1), ('R', -1)):
            if e == 1:
                P(f'ear_{s}', rot=(-15 if s == 'L' else 10, 0, 0))
            elif e == 2:
                P(f'ear_{s}', rot=(-12, -10 * x, 0))
            elif e == 3:
                P(f'ear_{s}', rot=(25, 18 * x, 0))
    if 'head' in pb:
        tilt = {'happy': (0, 0, 0), 'curious': (0, 14, 0), 'surprised': (-8, 0, 0), 'focused': (6, 0, 0),
                'affectionate': (4, -10, 0)}[expr]
        P('head', rot=tilt)


def surf_y(x, z, y0=-2.0, skip_bones=()):
    """First non-shell surface hit along +Y at (x, z), using evaluated geometry."""
    dg = bpy.context.evaluated_depsgraph_get(); bpy.context.view_layer.update()
    o = Vector((x, y0, z))
    for _ in range(20):
        hit, loc, nrm, idx, ob, mtx = bpy.context.scene.ray_cast(dg, o, Vector((0, 1, 0)))
        if not hit:
            return None
        if ob.get('shell') or ob.name.endswith('_lid') or 'eye' in ob.name or ob.parent_bone in skip_bones:
            o = loc + Vector((0, 1e-4, 0)); continue
        return loc.y
    return None


def tri_cloth(name, top_y, top_z, w, h, m, coll_, bend=1.2):
    """Triangular bandana cloth hanging forward/down, curved around the chest."""
    import bmesh as _bm
    bm = _bm.new(); uvl = bm.loops.layers.uv.new('UVMap')
    N_ = 8; verts = {}
    for i in range(N_ + 1):
        for j in range(N_ + 1 - i):
            u = (j - (N_ - i) / 2) / N_ * 2  # -1..1 across width (shrinks with i)
            v = i / N_
            x = u * w * (1 - v) if False else (j / max(1, N_) * 2 - (N_ - i) / N_) * w
            zz = top_z - v * h
            yy = top_y - v * h * 0.35 + bend * (x ** 2)
            verts[(i, j)] = bm.verts.new((x, yy, zz))
    for i in range(N_):
        for j in range(N_ - i):
            a, b_, c = verts[(i, j)], verts[(i, j + 1)], verts[(i + 1, j)]
            bm.faces.new((a, b_, c))
            if j < N_ - i - 1:
                bm.faces.new((b_, verts[(i + 1, j + 1)], c))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    o = _finish(name, bm, (0, 0, 0), (0, 0, 0), m, 2, coll_)
    solid(o, 0.006, 0.0)
    return o


# ====================================================================== DOGS
def dog_pattern_ayra(P, N, part):
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    base = np.array(hexc('b5622f'))           # warm reddish-brown
    dark = np.array(hexc('6b3518'))           # merle brown patches
    beige = np.array(hexc('e3c49b'))          # beige marbling
    white = np.array(hexc('f7f3ec'))
    col = np.tile(base, (len(P), 1)).astype(float)
    n1 = fbm(P, 9.0, seed=11, oct=4); n2 = fbm(P + 3.1, 14.0, seed=23, oct=3); n3 = vnoise(P, 40.0, seed=5)
    beige_m = smooth(0.56, 0.62, n2) * (part not in ('nose',))
    col = col * (1 - beige_m[:, None] * 0.75) + beige[None] * beige_m[:, None] * 0.75
    dark_m = smooth(0.60, 0.65, n1)
    col = col * (1 - dark_m[:, None]) + dark[None] * dark_m[:, None]
    fleck = smooth(0.86, 0.9, n3) * 0.8
    col = col * (1 - fleck[:, None]) + white[None] * fleck[:, None]
    w = np.zeros(len(P))
    if part in ('body', 'neck'):
        w = np.maximum(w, smooth(0.02, -0.04, y - (-0.06)) * smooth(0.30, 0.24, z) * smooth(0.085, 0.05, np.abs(x)))  # chest bib
        w = np.maximum(w, smooth(0.20, 0.16, z) * smooth(0.06, 0.03, np.abs(x)))  # belly
        if part == 'neck':
            w = np.maximum(w, smooth(-0.0, -0.06, N[:, 1] * 0 + y + 0.20) * smooth(0.33, 0.28, z))
    if part == 'head':
        w = np.maximum(w, smooth(0.022, 0.01, np.abs(x)) * smooth(-0.24, -0.3, y))  # blaze
    if part == 'snout':
        w = np.maximum(w, np.clip(smooth(0.022, 0.008, np.abs(x)) + smooth(-0.2, -0.6, N[:, 2]), 0, 1) * 0.95)
    if part.startswith('leg'):
        w = np.maximum(w, smooth(0.08, 0.04, z))
    if part == 'paw':
        w[:] = 1.0
    if part == 'tail':
        w = np.maximum(w, smooth(0.62, 0.66, y))  # tip (tail extends to +Y)
    if part == 'ear':
        col = col * 0.8 + dark[None] * 0.2
    return col * (1 - w[:, None]) + white[None] * w[:, None]


def dog_pattern_pandora(P, N, part):
    white = np.array(hexc('fbfaf6')); cream = np.array(hexc('efe4cf'))
    n = fbm(P, 12.0, seed=3, oct=3)
    m = smooth(0.55, 0.75, n) * 0.35
    if part == 'ear':
        m = m * 0 + 0.45
    return white[None] * (1 - m[:, None]) + cream[None] * m[:, None]


def dog_pattern_tifa(P, N, part):
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    tan = np.array(hexc('d39a52')); tan2 = np.array(hexc('b97a35'))
    steel = np.array(hexc('4b5560')); steel2 = np.array(hexc('6c7883'))
    n = fbm(P, 16.0, seed=9, oct=3)
    tanc = tan[None] * (1 - n[:, None] * 0.5) + tan2[None] * (n[:, None] * 0.5)
    stc = steel[None] * (1 - n[:, None] * 0.6) + steel2[None] * (n[:, None] * 0.6)
    if part in ('body', 'tail'):
        if part == 'body':
            m = smooth(-0.35, 0.05, N[:, 2]) * smooth(-0.16, -0.08, y)  # back + sides steel; chest/belly tan
        else:
            m = np.ones(len(P))
        return tanc * (1 - m[:, None]) + stc * m[:, None]
    if part == 'neck':
        m = smooth(-0.1, 0.4, N[:, 1] + N[:, 2] * 0.5) * 0.9
        return tanc * (1 - m[:, None]) + stc * m[:, None]
    if part == 'ear':
        return tanc * 0.9
    return tanc


DOGS = {
    'ayra': dict(scale=0.72, body=(0.115, 0.2, 0.118), body_z=0.235, leg_len=0.2, leg_r=(0.046, 0.038), head_r=(0.092, 0.088, 0.085),
                 head_pos=(0, -0.2, 0.39), snout=(0.088, 0.036, 0.034), ear='semi', tail='long', eye='blue', fluff=0.012,
                 pattern=dog_pattern_ayra, acc='bandana_blue', hair=None, shells=(4, 0.016), tuft=260, ruff=True),
    'pandora': dict(scale=0.55, body=(0.14, 0.155, 0.135), body_z=0.2, leg_len=0.13, leg_r=(0.045, 0.038), head_r=(0.105, 0.095, 0.098),
                    head_pos=(0, -0.155, 0.345), snout=(0.05, 0.03, 0.028), ear='tri', tail='plume', eye='dark', fluff=0.03,
                    pattern=dog_pattern_pandora, acc='bow_pink', hair=None, shells=(5, 0.03), tuft=180, ruff=True),
    'tifa': dict(scale=0.5, body=(0.108, 0.155, 0.102), body_z=0.19, leg_len=0.135, leg_r=(0.042, 0.035), head_r=(0.092, 0.088, 0.088),
                 head_pos=(0, -0.175, 0.33), snout=(0.055, 0.032, 0.03), ear='erect', tail='short', eye='dark', fluff=0.01,
                 pattern=dog_pattern_tifa, acc='bandana_green', hair=None, shells=(4, 0.018), tuft=300, ruff=False),
}


def build_dog(name):
    """All dogs are modelled at a common base size then the whole rig is scaled by cfg['scale']."""
    cfg = DOGS[name]
    C = coll(f'CH_{name}')
    bw, bl, bh = cfg['body']; bz = cfg['body_z']
    hx, hy, hz = cfg['head_pos']; hr = cfg['head_r']
    sl, sw, sh = cfg['snout']
    ll = cfg['leg_len']
    legx = bw * 0.62; legyf = -bl * 0.62; legyb = bl * 0.6
    ear_base = {'semi': (0.058, hy + 0.012, hz + hr[2] * 0.78), 'tri': (0.058, hy + 0.01, hz + hr[2] * 0.85),
                'erect': (0.05, hy + 0.012, hz + hr[2] * 0.82)}[cfg['ear']]
    bones = [('root', (0, 0, 0), (0, 0, 0.1), None), ('body', (0, bl * 0.3, bz), (0, -bl * 0.5, bz), 'root'),
             ('neck', (0, -bl * 0.55, bz + bh * 0.4), (hx, hy + 0.02, hz - 0.03), 'body'),
             ('head', (hx, hy + 0.03, hz - 0.04), (hx, hy - 0.08, hz), 'neck'),
             ('jaw', (0, hy - hr[1] * 0.4, hz - hr[2] * 0.42), (0, hy - hr[1] - sl, hz - hr[2] * 0.42), 'head'),
             ('tongue', (0, hy - hr[1] * 0.4, hz - hr[2] * 0.45), (0, hy - hr[1] - sl, hz - hr[2] * 0.45), 'jaw'),
             ('tail', (0, bl * 0.9, bz + bh * 0.45), (0, bl * 0.9 + 0.08, bz + bh * 0.8), 'body')]
    for s, x in (('L', 1), ('R', -1)):
        bones += [(f'ear_{s}', (ear_base[0] * x, ear_base[1], ear_base[2]), (ear_base[0] * x * 1.3, ear_base[1], ear_base[2] + 0.05), 'head'),
                  (f'lid_{s}', (0.036 * x, hy - hr[1] * 0.78, hz + 0.012), (0.036 * x, hy - hr[1] - 0.05, hz + 0.012), 'head'),
                  (f'leg_F{s}', (legx * x, legyf, bz - bh * 0.2), (legx * x, legyf, 0.03), 'body'),
                  (f'leg_B{s}', (legx * x, legyb, bz - bh * 0.2), (legx * x, legyb, 0.03), 'body')]
    arm = make_armature(name, bones, C)
    B = lambda o, b: bind(o, arm, b)
    furm = {}

    def fur_obj(o, part, bone, size=256, hair=True, fluff=None):
        img = bake_pattern(o, lambda P, N: cfg['pattern'](P, N, part), size, name=f'{name}_{o.name}_tex')
        m = img_mat(f'{name}_{o.name}_fur', img, rough=0.75, sss=0.05, sheen=0.6, bump=0.25)
        o.data.materials.clear(); o.data.materials.append(m)
        fl = cfg['fluff'] if fluff is None else fluff
        if fl:
            tex = bpy.data.textures.get(f'fluff_{name}') or bpy.data.textures.new(f'fluff_{name}', 'CLOUDS')
            tex.noise_scale = 0.012 if name != 'pandora' else 0.02
            md = o.modifiers.new('fluff', 'DISPLACE'); md.texture = tex; md.strength = fl; md.mid_level = 0.35
            md.texture_coords = 'OBJECT' if False else 'LOCAL'
            o.modifiers.move(len(o.modifiers) - 1, 0)
        B(o, bone)
        if hair and cfg.get('shells'):
            add_shells(o, part, img)
        return o

    def add_shells(o, part, img):
        n, depth = cfg['shells']
        mult = {'body': 1.0, 'neck': 0.8, 'head': 0.55, 'tail': 1.0, 'ruff': 1.0}.get(part, 0.0)
        if not mult:
            return
        for k in range(1, n + 1):
            sh = o.copy(); sh.data = o.data; sh.name = f'{o.name}_shell{k}'
            for c_ in o.users_collection:
                c_.objects.link(sh)
            md = sh.modifiers.new('push', 'DISPLACE'); md.direction = 'NORMAL'; md.mid_level = 0.0
            md.strength = depth * mult * k / n
            sh.modifiers.move(len(sh.modifiers) - 1, 1 if sh.modifiers[0].name == 'fluff' else 0)
            sh.data = o.data
            sh.material_slots[0].link = 'OBJECT'
            sh.material_slots[0].material = shell_mat(img, k / n)
            sh['shell'] = k

    def shell_mat(img, t):
        key = f'{name}_{img.name}_shell_{int(t * 100)}'
        m = bpy.data.materials.get(key)
        if m:
            return m
        m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree
        b = nt.nodes['Principled BSDF']
        ti = nt.nodes.new('ShaderNodeTexImage'); ti.image = img
        nt.links.new(ti.outputs['Color'], b.inputs['Base Color'])
        b.inputs['Roughness'].default_value = 0.85
        _ = [b.inputs[k_].__setattr__('default_value', v) for k_, v in (('Sheen Weight', 0.8),) if k_ in b.inputs]
        tc = nt.nodes.new('ShaderNodeTexCoord')
        vo = nt.nodes.new('ShaderNodeTexVoronoi'); vo.feature = 'F1'; vo.inputs['Scale'].default_value = cfg['tuft']
        vo.inputs['Randomness'].default_value = 1.0
        nt.links.new(tc.outputs['Object'], vo.inputs['Vector'])
        mr = nt.nodes.new('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.0
        mr.inputs['From Max'].default_value = 0.5 * (1.3 - t); mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
        nt.links.new(vo.outputs['Distance'], mr.inputs['Value'])
        nt.links.new(mr.outputs['Result'], b.inputs['Alpha'])
        m.blend_method = 'CLIP'; m.shadow_method = 'CLIP'; m.alpha_threshold = 0.5
        return m

    def add_fur(o, h, m, part):
        mult = {'body': 1.0, 'neck': 0.5, 'head': 0.45, 'tail': 0.55, 'ruff': 0.5}.get(part, 0.0)
        if not mult:
            return
        ps = o.modifiers.new('fur', 'PARTICLE_SYSTEM').particle_system
        st = ps.settings; st.type = 'HAIR'; st.use_advanced_hair = True
        st.count = int(h['count'] * mult); st.hair_length = h['len'] * (0.6 if part == 'head' else 1.0)
        st.emit_from = 'FACE'; st.use_emit_random = True; st.userjit = 1
        hl = h['len'] * (0.6 if part == 'head' else 1.0)
        st.normal_factor = hl; st.factor_random = hl * 0.25; st.tangent_factor = 0.0
        st.object_align_factor = (0, hl * 0.9 if part != 'tail' else 0, -hl * 0.35)
        st.child_type = 'INTERPOLATED'; st.child_percent = 2; st.rendered_child_count = h['children']
        st.clump_factor = 0.45; st.clump_shape = 0.2; st.roughness_1 = 0.004; st.roughness_endpoint = 0.003
        st.child_length = 0.9; st.child_length_threshold = 0.3
        st.root_radius = 1.0; st.tip_radius = 0.0; st.radius_scale = 0.0012 * (1.6 if name == 'pandora' else 1.0)
        st.display_step = 3; st.render_step = 3
        st.material = 1
        st.use_close_tip = True
        st.hair_step = 4

    eyemat = PAL['eye_blue'] if cfg['eye'] == 'blue' else PAL['eye_dark']
    # body
    body = ellipsoid(f'{name}_body', (0, 0, bz), (bw, bl, bh), segs=40, rings=20,
                     deform=lambda co: Vector((co.x * (1 - 0.12 * max(0, co.y) / bl), co.y, co.z + 0.02 * (co.y / bl) * (1 if co.y < 0 else 0))), collection=C)
    fur_obj(body, 'body', 'body', 512)
    neck = capsule(f'{name}_neck', (0, -bl * 0.55, bz + bh * 0.1), (hx, hy + 0.035, hz - 0.035), bh * 0.72, hr[0] * 0.7, collection=C)
    fur_obj(neck, 'neck', 'neck', 256)
    if cfg['ruff']:
        ruff = ellipsoid(f'{name}_ruff', (0, hy + 0.06, hz - 0.075), (hr[0] * 1.05, hr[1] * 0.7, hr[2] * 0.75), (25, 0, 0), collection=C)
        fur_obj(ruff, 'neck' if name == 'ayra' else 'ruff', 'neck', 256)
    head = ellipsoid(f'{name}_head', (hx, hy, hz), hr, segs=40, rings=20,
                     deform=lambda co: Vector((co.x * (1 + 0.08 * max(0, -co.z) / hr[2]), co.y, co.z)), collection=C)
    fur_obj(head, 'head', 'head', 512)
    # snout + nose + mouth (jaw)
    sn0 = Vector((0, hy - hr[1] * 0.55, hz - hr[2] * 0.3)); sn1 = sn0 + Vector((0, -sl, -0.01))
    snout = capsule(f'{name}_snout', sn0, sn1, sw * 1.05, sw * 0.85, segs=24, rings=12, collection=C, squash=(1.0, 0.8))
    fur_obj(snout, 'snout', 'head', 256, hair=False, fluff=0.0)
    nose = ellipsoid(f'{name}_nose', sn1 + Vector((0, -sw * 0.75, sh * 0.35)), (sw * 0.5, sw * 0.35, sw * 0.36),
                     m=mat('dog_nose', PAL['nose_dog'], rough=0.2, spec=0.8, coat=0.7), collection=C)
    B(nose, 'head')
    jaw = capsule(f'{name}_jaw', sn0 + Vector((0, 0.01, -sh * 0.75)), sn1 + Vector((0, 0.008, -sh * 0.7)), sw * 0.8, sw * 0.62,
                  segs=20, rings=10, collection=C, squash=(1.0, 0.6))
    fur_obj(jaw, 'snout', 'jaw', 128, hair=False, fluff=0.0)
    mouth_in = capsule(f'{name}_mouthin', sn0 + Vector((0, 0.0, -sh * 0.45)), sn1 + Vector((0, 0.012, -sh * 0.42)), sw * 0.7, sw * 0.55,
                       mat('dog_mouth', (0.45, 0.1, 0.12), rough=0.5), segs=16, rings=8, collection=C, squash=(1, 0.5))
    B(mouth_in, 'head')
    tongue = ellipsoid(f'{name}_tongue', sn1 + Vector((0, 0.016, -sh * 0.85)), (sw * 0.5, sw * 0.62, sw * 0.18),
                       m=mat('tongue', PAL['tongue'], rough=0.35, sss=0.1), collection=C)
    B(tongue, 'tongue')
    # eyes
    lidm = mat(f'{name}_lidmat', tuple(cfg['pattern'](np.array([[0, hy - 0.05, hz + 0.03]]), np.array([[0, 0, 1.0]]), 'head')[0]), rough=0.8)
    er = hr[0] * (0.23 if name == 'pandora' else 0.27)
    for s, x in (('L', 1), ('R', -1)):
        ex, ez = 0.038 * x, hz + 0.014
        ys = surf_y(ex, ez)
        ec = Vector((ex, (ys if ys is not None else hy - hr[1] * 0.8) - er * 0.05 - cfg['shells'][1] * 0.6, ez))
        arm.data.bones  # lid bone was placed at a nominal centre; move it to the real eye centre
        bpy.context.view_layer.objects.active = arm; bpy.ops.object.mode_set(mode='EDIT')
        eb = arm.data.edit_bones[f'lid_{s}']; eb.head = ec; eb.tail = ec + Vector((0, -0.05, 0))
        bpy.ops.object.mode_set(mode='OBJECT')
        eye_parts(f'{name}_eye_{s}', arm, f'lid_{s}', ec, (er, er * 0.62, er * 1.05), eyemat, 0.9 if cfg['eye'] == 'blue' else 0.95,
                  lidm, C, yaw=22 * x, pupil=0.5, white=False)
    # ears
    for s, x in (('L', 1), ('R', -1)):
        b0 = Vector((ear_base[0] * x, ear_base[1], ear_base[2]))
        if cfg['ear'] == 'semi':  # semi-erect, tip folds forward
            ear = ellipsoid(f'{name}_ear_{s}', b0 + Vector((0.012 * x, 0, 0.035)), (0.034, 0.014, 0.05), (12, 0, -18 * x),
                            deform=lambda co: Vector((co.x, co.y - 0.9 * max(0, co.z - 0.015) ** 1.4 * 3, co.z - 1.5 * max(0, co.z - 0.02) ** 2)),
                            collection=C)
        elif cfg['ear'] == 'tri':
            ear = ellipsoid(f'{name}_ear_{s}', b0 + Vector((0.008 * x, 0, 0.03)), (0.03, 0.014, 0.036), (0, 0, -14 * x),
                            deform=lambda co: Vector((co.x * (1 - 0.85 * max(0, co.z) / 0.036), co.y, co.z)), collection=C)
        else:  # small erect V (yorkie)
            ear = ellipsoid(f'{name}_ear_{s}', b0 + Vector((0.01 * x, 0, 0.03)), (0.026, 0.01, 0.04), (0, 18 * x, -10 * x),
                            deform=lambda co: Vector((co.x * (1 - 0.9 * max(0, co.z) / 0.04), co.y, co.z)), collection=C)
        fur_obj(ear, 'ear', f'ear_{s}', 128, hair=False, fluff=0.003 if name == 'pandora' else 0.0)
        if name in ('ayra', 'tifa'):
            inner = ellipsoid(f'{name}_earin_{s}', b0 + Vector((0.01 * x, -0.012, 0.03)), (0.016, 0.004, 0.026), (12 if name == 'ayra' else 0, 0, -16 * x),
                              m=mat('ear_inner', (0.95, 0.68, 0.66)),
                              deform=(lambda co: Vector((co.x, co.y - 0.9 * max(0, co.z - 0.01) ** 1.4 * 3, co.z))) if name == 'ayra' else None, collection=C)
            B(inner, f'ear_{s}')
    # legs + paws
    for s, x in (('L', 1), ('R', -1)):
        for fb, yy in (('F', legyf), ('B', legyb)):
            top = Vector((legx * x, yy, bz - bh * 0.15)); bot = Vector((legx * x, yy - (0.01 if fb == 'F' else -0.0), 0.04))
            leg = capsule(f'{name}_leg_{fb}{s}', top, bot, cfg['leg_r'][0] * (1.15 if fb == 'B' else 1.0), cfg['leg_r'][1], segs=20, rings=10, collection=C)
            fur_obj(leg, 'leg', f'leg_{fb}{s}', 128, hair=False)
            paw = ellipsoid(f'{name}_paw_{fb}{s}', bot + Vector((0, -0.012, -0.012)), (cfg['leg_r'][1] * 1.2, cfg['leg_r'][1] * 1.5, cfg['leg_r'][1] * 0.85),
                            deform=lambda co: Vector((co.x, co.y, max(co.z, -cfg['leg_r'][1] * 0.6))), collection=C)
            fur_obj(paw, 'paw' if name == 'ayra' else 'leg', f'leg_{fb}{s}', 64, hair=False, fluff=0.0)
    # tail
    t0 = Vector((0, bl * 0.88, bz + bh * 0.4))
    if cfg['tail'] == 'long':
        pts = [t0, t0 + Vector((0, 0.06, -0.02)), t0 + Vector((0, 0.13, -0.06)), t0 + Vector((0, 0.19, -0.06)), t0 + Vector((0, 0.235, -0.02))]
        rad = [0.03, 0.038, 0.04, 0.034, 0.018]
    elif cfg['tail'] == 'plume':
        pts = [t0, t0 + Vector((0, 0.03, 0.06)), t0 + Vector((0, 0.0, 0.12)), t0 + Vector((0, -0.07, 0.14)), t0 + Vector((0, -0.12, 0.12))]
        rad = [0.035, 0.055, 0.06, 0.05, 0.03]
    else:
        pts = [t0, t0 + Vector((0, 0.03, 0.04)), t0 + Vector((0, 0.045, 0.085))]
        rad = [0.022, 0.02, 0.012]
    tail = tube_along(f'{name}_tail', pts, rad, segs=16, collection=C)
    fur_obj(tail, 'tail', 'tail', 256)
    # accessories
    if cfg['acc'].startswith('bandana'):
        bm_ = mat(f'{name}_bandana', PAL[cfg['acc']], rough=0.6, sheen=0.4)
        zc = bz + bh * 0.55
        yc = min([v for v in (surf_y(0, zc, skip_bones=('head', 'jaw', 'tongue')), surf_y(0, zc - 0.03, skip_bones=('head', 'jaw', 'tongue'))) if v is not None] or [-bl])
        tri = tri_cloth(f'{name}_bandana', yc - 0.006, zc + 0.012, bw * 0.8, bh * 0.85, bm_, C, bend=3.0)
        B(tri, 'neck')
        for k in range(4):
            ang = (k - 1.5) * 0.5
            dot = ellipsoid(f'{name}_dot{k}', (math.sin(ang) * bw * 0.35, yc - 0.012 - bh * 0.3 * 0.35 + 3.0 * (math.sin(ang) * bw * 0.35) ** 2, zc - bh * 0.3),
                            (0.007, 0.003, 0.007), m=mat('bandana_dot', (0.98, 0.98, 0.98)), segs=10, rings=6, collection=C)
            B(dot, 'neck')
    else:  # pink bow on head (left side)
        bc = Vector((0.05, hy + 0.01, hz + hr[2] * 0.9))
        bmb = mat('bow_pink', PAL['bow_pink'], rough=0.35, sheen=0.5, coat=0.3)
        for x in (1, -1):
            B(ellipsoid(f'{name}_bow_{x}', bc + Vector((0.025 * x, 0, 0)), (0.026, 0.012, 0.018), (0, -20 * x, 0), bmb, collection=C), 'head')
        B(ellipsoid(f'{name}_bowknot', bc, (0.011, 0.012, 0.012), m=bmb, collection=C), 'head')
    s = cfg['scale']
    arm.scale = (s, s, s)
    reset_pose(arm); face(arm, 'happy')
    return arm


def build(name):
    return build_clara() if name == 'clara' else build_dog(name)
