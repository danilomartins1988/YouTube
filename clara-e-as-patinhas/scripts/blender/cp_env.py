"""Garden environment for Clara e as Patinhas (procedural). Dance lawn centred at origin, characters face -Y,
cameras mostly on the -Y side. Layout (metres):
  house (Clara's) at (-5.5, 7.5); dog houses at x=3..6, y=5.5; swing (-2.6, 4.2); pond centre (5.2, -1.2) with
  wooden bridge spanning it along X; flower meadow (-4.2, -1.5); stone path from porch to lawn; hills far away."""
import bpy, math, random
import numpy as np
from mathutils import Vector, noise
from cp_lib import *
from cp_lib import _finish

P = {'sun': (1.0, 0.82, 0.2), 'sky': (0.55, 0.78, 0.98), 'green': (0.42, 0.72, 0.28), 'green2': (0.32, 0.62, 0.22),
     'pink': (0.98, 0.62, 0.75), 'white': (0.97, 0.97, 0.95), 'wood': (0.70, 0.46, 0.26), 'wood2': (0.58, 0.36, 0.2),
     'terracotta': (0.84, 0.42, 0.26), 'wall': (0.98, 0.95, 0.88), 'stone': (0.78, 0.76, 0.72), 'water': (0.35, 0.68, 0.9)}
POND_C = Vector((5.2, -1.2, 0)); POND_R = (2.0, 1.4)


def ground_h(x, y):
    """Gentle undulation, flat near the dance area and pond."""
    d = math.hypot(x, y)
    flat = min(1.0, max(0.0, (d - 3.5) / 6.0))
    h = 0.35 * flat * (noise.noise(Vector((x * 0.08, y * 0.08, 0.3))) + 0.3)
    pd = ((x - POND_C.x) / (POND_R[0] + 0.6)) ** 2 + ((y - POND_C.y) / (POND_R[1] + 0.6)) ** 2
    if pd < 1.0:
        h = h * pd - 0.12 * (1 - pd) ** 0.5
    return h


def grass_mat():
    m = bpy.data.materials.new('grass'); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.6; n.inputs['Detail'].default_value = 3
    nt.links.new(tc.outputs['Object'], n.inputs['Vector'])
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].color = L(0.36, 0.66, 0.24); cr.color_ramp.elements[1].color = L(0.52, 0.80, 0.30)
    nt.links.new(n.outputs['Fac'], cr.inputs['Fac'])
    n2 = nt.nodes.new('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 120; n2.inputs['Detail'].default_value = 2
    nt.links.new(tc.outputs['Object'], n2.inputs['Vector'])
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'; mix.inputs['Fac'].default_value = 0.25
    nt.links.new(cr.outputs['Color'], mix.inputs[1]); nt.links.new(n2.outputs['Color'], mix.inputs[2])
    nt.links.new(mix.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35
    nt.links.new(n2.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = 0.85
    return m


def build_ground(C):
    bm = bmesh.new(); bm.loops.layers.uv.new('UVMap')
    bmesh.ops.create_grid(bm, x_segments=120, y_segments=120, size=45, calc_uvs=True)
    for v in bm.verts:
        v.co.z = ground_h(v.co.x, v.co.y)
    o = _finish('ground', bm, (0, 0, 0), (0, 0, 0), grass_mat(), 0, C)
    return o


def build_sky(scene):
    w = bpy.data.worlds.new('sky'); scene.world = w; w.use_nodes = True; nt = w.node_tree
    bg = nt.nodes['Background']
    tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['Generated'], sep.inputs[0])
    cr = nt.nodes.new('ShaderNodeValToRGB')
    cr.color_ramp.elements[0].position = 0.45; cr.color_ramp.elements[0].color = L(0.80, 0.90, 0.98)
    cr.color_ramp.elements[1].position = 0.85; cr.color_ramp.elements[1].color = L(0.38, 0.66, 0.97)
    nt.links.new(sep.outputs['Z'], cr.inputs['Fac'])
    nt.links.new(cr.outputs['Color'], bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
    return w


def tree(C, loc, s=1.0, seed=0):
    rnd = random.Random(seed)
    z0 = ground_h(loc[0], loc[1])
    trunk = capsule(f'trunk_{seed}', (loc[0], loc[1], z0 - 0.1), (loc[0], loc[1], z0 + 1.5 * s), 0.16 * s, 0.11 * s,
                    mat('trunk', (0.55, 0.36, 0.22), rough=0.9), collection=C)
    leaf = mat(f'leaf{seed % 3}', [(0.36, 0.70, 0.26), (0.44, 0.76, 0.30), (0.30, 0.64, 0.24)][seed % 3], rough=0.8, sheen=0.4)
    for k in range(5):
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.25, 0.55) * s
        c = (loc[0] + math.cos(a) * r, loc[1] + math.sin(a) * r, z0 + (1.7 + rnd.uniform(0, 0.8)) * s)
        rr = rnd.uniform(0.6, 0.85) * s
        e = ellipsoid(f'crown_{seed}_{k}', c, (rr, rr, rr * 0.9), m=leaf, segs=24, rings=12, collection=C)
        md = e.modifiers.new('d', 'DISPLACE'); tex = bpy.data.textures.get('crown') or bpy.data.textures.new('crown', 'CLOUDS')
        tex.noise_scale = 0.35; md.texture = tex; md.strength = 0.12 * s; md.mid_level = 0.5
        e.modifiers.move(1, 0)


def flower(C, loc, col, seed, s=1.0, link_src=None):
    z0 = ground_h(loc[0], loc[1])
    objs = []
    st = capsule(f'stem_{seed}', (loc[0], loc[1], z0), (loc[0], loc[1], z0 + 0.22 * s), 0.008 * s, 0.006 * s,
                 mat('stem', (0.3, 0.62, 0.22)), segs=8, rings=4, sub=0, collection=C)
    c = Vector((loc[0], loc[1], z0 + 0.23 * s))
    pm = mat(f'petal_{col}', col, rough=0.5, sheen=0.4, sss=0.1)
    for k in range(5):
        a = 2 * math.pi * k / 5 + seed
        objs.append(ellipsoid(f'petal_{seed}_{k}', c + Vector((math.cos(a) * 0.035 * s, math.sin(a) * 0.035 * s, 0)),
                              (0.03 * s, 0.018 * s, 0.008 * s), (0, 0, math.degrees(a)), pm, segs=12, rings=6, sub=0, collection=C))
    objs.append(ellipsoid(f'fc_{seed}', c + Vector((0, 0, 0.006 * s)), (0.016 * s, 0.016 * s, 0.01 * s),
                          m=mat('flower_c', (1.0, 0.82, 0.2)), segs=12, rings=6, sub=0, collection=C))
    return objs


def house(C):
    hx, hy = -5.5, 7.5; z0 = ground_h(hx, hy)
    wall = mat('wall', P['wall'], rough=0.85); roof = mat('roof', P['terracotta'], rough=0.7)
    trim = mat('trim', P['white'], rough=0.6); glass = mat('glass', (0.55, 0.78, 0.95), rough=0.08, spec=0.9)
    door = mat('door', (0.98, 0.72, 0.25), rough=0.5)
    box('house_body', (hx, hy, z0 + 1.3), (4.2, 3.0, 2.6), wall, bevel=0.06, collection=C)
    box('house_base', (hx, hy, z0 + 0.12), (4.35, 3.15, 0.25), mat('base', (0.85, 0.78, 0.7)), bevel=0.03, collection=C)
    # gable roof: two slabs
    for sgn in (1, -1):
        r = box(f'roof_{sgn}', (hx, hy + sgn * 0.85, z0 + 3.15), (4.7, 2.05, 0.18), roof, bevel=0.05, collection=C,
                rot=(-sgn * 34, 0, 0))
    bm = bmesh.new(); bm.loops.layers.uv.new('UVMap')
    vs = []
    for x in (hx - 2.08, hx + 2.08):
        vs.append([bm.verts.new((x, hy - 1.5, z0 + 2.58)), bm.verts.new((x, hy + 1.5, z0 + 2.58)), bm.verts.new((x, hy, z0 + 3.58))])
    bm.faces.new(vs[0]); bm.faces.new(list(reversed(vs[1])))
    for k in range(3):
        bm.faces.new((vs[0][k], vs[0][(k + 1) % 3], vs[1][(k + 1) % 3], vs[1][k]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    _finish('gable', bm, (0, 0, 0), (0, 0, 0), wall, 0, C, smooth=False)
    # big windows + door on the front (-Y)
    fy = hy - 1.51
    for wx in (-1.2, 1.2):
        box(f'win_frame_{wx}', (hx + wx, fy, z0 + 1.45), (1.0, 0.06, 1.1), trim, bevel=0.02, collection=C)
        box(f'win_glass_{wx}', (hx + wx, fy - 0.02, z0 + 1.45), (0.84, 0.04, 0.94), glass, collection=C)
        box(f'win_bar_{wx}', (hx + wx, fy - 0.045, z0 + 1.45), (0.05, 0.03, 0.94), trim, collection=C)
        box(f'win_barh_{wx}', (hx + wx, fy - 0.045, z0 + 1.45), (0.84, 0.03, 0.05), trim, collection=C)
        box(f'win_sill_{wx}', (hx + wx, fy - 0.08, z0 + 0.88), (1.1, 0.16, 0.06), trim, bevel=0.015, collection=C)
        box(f'planter_{wx}', (hx + wx, fy - 0.16, z0 + 0.8), (0.9, 0.16, 0.14), mat('planter', P['terracotta']), bevel=0.02, collection=C)
        for k in range(5):
            ellipsoid(f'pl_fl_{wx}_{k}', (hx + wx - 0.36 + k * 0.18, fy - 0.17, z0 + 0.9), (0.07, 0.06, 0.06),
                      m=mat(f'pf{k % 3}', [P['pink'], (1, 0.85, 0.3), (0.98, 0.45, 0.45)][k % 3], rough=0.6), segs=12, rings=6, sub=0, collection=C)
    box('door', (hx, fy - 0.01, z0 + 0.95), (0.85, 0.06, 1.7), door, bevel=0.03, collection=C)
    ellipsoid('knob', (hx + 0.3, fy - 0.06, z0 + 0.95), (0.04, 0.03, 0.04), m=mat('gold', (0.95, 0.8, 0.4), metallic=0.8, rough=0.3), sub=0, collection=C)
    # porch
    box('porch_floor', (hx, fy - 0.8, z0 + 0.12), (2.6, 1.4, 0.18), mat('porch', P['wood'], rough=0.7), bevel=0.02, collection=C)
    box('porch_roof', (hx, fy - 0.85, z0 + 2.35), (2.8, 1.6, 0.1), roof, bevel=0.03, collection=C, rot=(-8, 0, 0))
    for px in (-1.2, 1.2):
        cylinder(f'post_{px}', (hx + px, fy - 1.4, z0 + 1.22), 0.07, 2.2, trim, segs=16, collection=C)
    for px in (-1.6, 1.6):
        cylinder(f'pot_{px}', (hx + px, fy - 1.55, z0 + 0.2), 0.2, 0.36, mat('pot', P['terracotta'], rough=0.7), segs=24, collection=C)
        ellipsoid(f'potplant_{px}', (hx + px, fy - 1.55, z0 + 0.5), (0.26, 0.26, 0.24), m=mat('leaf0', (0.36, 0.70, 0.26)), segs=16, rings=8, collection=C)
        for k in range(4):
            a = k * 1.7
            ellipsoid(f'potfl_{px}_{k}', (hx + px + 0.15 * math.cos(a), fy - 1.55 + 0.15 * math.sin(a), z0 + 0.65), (0.06, 0.06, 0.05),
                      m=mat('pf0', P['pink']), segs=10, rings=6, sub=0, collection=C)
    box('chimney', (hx + 1.3, hy + 0.6, z0 + 3.8), (0.4, 0.4, 0.9), mat('brick', (0.8, 0.45, 0.35)), bevel=0.02, collection=C)


def dog_house(C, loc, col, label):
    z0 = ground_h(loc[0], loc[1])
    wood = mat(f'dh_{label}', col, rough=0.6)
    roof = mat('dh_roof', P['white'], rough=0.6)
    box(f'dh_body_{label}', (loc[0], loc[1], z0 + 0.35), (0.8, 0.9, 0.7), wood, bevel=0.03, collection=C)
    for sgn in (1, -1):
        box(f'dh_roof_{label}_{sgn}', (loc[0] + sgn * 0.24, loc[1], z0 + 0.86), (0.62, 1.0, 0.07), roof, bevel=0.02, collection=C, rot=(0, sgn * 40, 0))
    cylinder(f'dh_door_{label}', (loc[0], loc[1] - 0.455, z0 + 0.26), 0.2, 0.02, mat('dh_dark', (0.12, 0.08, 0.07), rough=0.9), segs=24, rot=(90, 0, 0), collection=C)
    t = bpy.data.curves.new(f'lbl_{label}', 'FONT'); t.body = label; t.align_x = 'CENTER'; t.size = 0.12; t.extrude = 0.006
    o = bpy.data.objects.new(f'lbl_{label}', t); C.objects.link(o); o.location = (loc[0], loc[1] - 0.47, z0 + 0.55)
    o.rotation_euler = (math.radians(90), 0, 0); t.materials.append(mat('label', P['white']))


def swing(C, loc):
    z0 = ground_h(loc[0], loc[1]); w = mat('swing_wood', P['wood2'], rough=0.7)
    for sx in (-0.8, 0.8):
        for sy in (-0.35, 0.35):
            capsule(f'sw_leg_{sx}_{sy}', (loc[0] + sx * 1.0, loc[1] + sy, z0), (loc[0] + sx * 0.82, loc[1], z0 + 1.9), 0.05, 0.05, w, segs=12, rings=6, sub=0, collection=C)
    capsule('sw_top', (loc[0] - 0.85, loc[1], z0 + 1.9), (loc[0] + 0.85, loc[1], z0 + 1.9), 0.055, 0.055, w, segs=12, rings=6, sub=0, collection=C)
    for sx in (-0.25, 0.25):
        capsule(f'sw_rope_{sx}', (loc[0] + sx, loc[1], z0 + 1.88), (loc[0] + sx, loc[1], z0 + 0.5), 0.012, 0.012, mat('rope', (0.9, 0.82, 0.62)), segs=8, rings=4, sub=0, collection=C)
    box('sw_seat', (loc[0], loc[1], z0 + 0.48), (0.65, 0.25, 0.05), mat('seat', (0.98, 0.45, 0.45), rough=0.5), bevel=0.015, collection=C)


def pond_bridge(C):
    z0 = 0.0
    wat = bpy.data.materials.new('water'); wat.use_nodes = True; b = wat.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = L(*P['water']); b.inputs['Roughness'].default_value = 0.05
    b.inputs['IOR'].default_value = 1.33
    n = wat.node_tree.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 6
    bp = wat.node_tree.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.08
    wat.node_tree.links.new(n.outputs['Fac'], bp.inputs['Height']); wat.node_tree.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    ellipsoid('pond_water', (POND_C.x, POND_C.y, -0.04), (POND_R[0], POND_R[1], 0.02), m=wat, segs=48, rings=8, sub=0, collection=C)
    rnd = random.Random(4)
    stm = mat('stone', P['stone'], rough=0.8)
    for k in range(34):
        a = 2 * math.pi * k / 34
        r = 1.04 + rnd.uniform(-0.02, 0.05)
        x = POND_C.x + math.cos(a) * POND_R[0] * r; y = POND_C.y + math.sin(a) * POND_R[1] * r
        ellipsoid(f'rim_{k}', (x, y, ground_h(x, y) + 0.02), (0.2, 0.16, 0.09), (0, 0, math.degrees(a)), stm, segs=12, rings=6, collection=C)
    # lily pads
    for k, (dx, dy) in enumerate([(-0.8, 0.3), (0.6, -0.5), (1.1, 0.5)]):
        cylinder(f'lily_{k}', (POND_C.x + dx, POND_C.y + dy, -0.015), 0.18, 0.01, mat('lily', (0.3, 0.65, 0.3)), segs=20, collection=C)
    # arched wooden bridge along X across the pond's narrow middle
    wood = mat('bridge_wood', P['wood'], rough=0.7); wood2 = mat('bridge_wood2', P['wood2'], rough=0.7)
    L_ = 2.6 * POND_R[0] / 2.0 * 1.25; nplank = 15
    for k in range(nplank):
        u = k / (nplank - 1) * 2 - 1
        x = POND_C.x + u * L_ / 2; z = 0.42 * (1 - u * u) + 0.06
        ang = math.degrees(math.atan(-0.84 * u / (L_ / 2) * 1.0))
        box(f'plank_{k}', (x, POND_C.y, z), (L_ / nplank * 0.92, 0.9, 0.05), wood if k % 2 else wood2, bevel=0.01, collection=C, rot=(0, ang, 0))
    for sy in (-0.47, 0.47):
        pts = [(POND_C.x + (k / 8 * 2 - 1) * L_ / 2, POND_C.y + sy, 0.42 * (1 - (k / 8 * 2 - 1) ** 2) + 0.42) for k in range(9)]
        tube_along(f'rail_{sy}', pts, [0.035] * 9, wood2, segs=10, collection=C)
        for k in range(0, 9, 2):
            p = pts[k]
            capsule(f'rpost_{sy}_{k}', (p[0], p[1], p[2] - 0.38), (p[0], p[1], p[2]), 0.035, 0.035, wood2, segs=10, rings=4, sub=0, collection=C)


def stone_path(C):
    rnd = random.Random(7)
    stm = mat('stone_path', (0.86, 0.83, 0.78), rough=0.85)
    a = Vector((-5.5, 5.4)); b = Vector((-0.6, 0.9))
    for k in range(13):
        u = k / 12; p = a.lerp(b, u) + Vector((math.sin(u * 5) * 0.4, 0))
        ellipsoid(f'path_{k}', (p.x, p.y, ground_h(p.x, p.y) + 0.0), (0.28, 0.22, 0.04), (0, 0, rnd.uniform(0, 180)), stm, segs=16, rings=6, collection=C)


def toys(C):
    ballm = [mat('toy_r', (0.95, 0.3, 0.3), rough=0.35, coat=0.5), mat('toy_y', P['sun'], rough=0.35, coat=0.5),
             mat('toy_b', (0.3, 0.55, 0.95), rough=0.35, coat=0.5)]
    # striped beach ball
    for k in range(3):
        e = ellipsoid(f'ball_{k}', (1.9, 1.6, 0.16), (0.16, 0.16, 0.16), (0, 0, 0), ballm[k], segs=24, rings=12, collection=C,
                      cut=(lambda d, k=k: not (k * 2 * math.pi / 3 <= (math.atan2(d.y, d.x) % (2 * math.pi)) < (k + 1) * 2 * math.pi / 3)))
    for k, (x, y, c) in enumerate([(-1.7, 1.9, 0), (-1.45, 2.0, 1), (-1.58, 1.95, 2)]):
        box(f'block_{k}', (x, y, 0.07 + (0.13 if k == 2 else 0)), (0.13, 0.13, 0.13), ballm[c], bevel=0.015, collection=C, rot=(0, 0, k * 20))
    ellipsoid('bone_toy', (2.6, 0.9, 0.03), (0.09, 0.025, 0.025), m=mat('toy_bone', (0.98, 0.95, 0.85)), collection=C)
    cone('bucket', (-2.4, 0.7, 0.09), 0.1, 0.13, 0.18, ballm[2], segs=24, collection=C)


def clouds(C):
    cm = mat('cloud', (1, 1, 1), rough=1.0, emis=(1, 1, 1), emis_str=0.45)
    rnd = random.Random(2)
    for k in range(9):
        cx = rnd.uniform(-45, 45); cy = rnd.uniform(38, 60); cz = rnd.uniform(9, 17)
        for j in range(5):
            r = rnd.uniform(2.0, 3.6)
            ellipsoid(f'cloud_{k}_{j}', (cx + j * 2.2 - 4.4 + rnd.uniform(-0.6, 0.6), cy, cz + rnd.uniform(-0.4, 1.0) + (1.2 if j in (1, 2, 3) else 0)),
                      (r, r * 0.8, r * 0.75), m=cm, segs=16, rings=8, collection=C)


def hills(C):
    hm = [mat('hill1', (0.48, 0.74, 0.36), rough=0.9), mat('hill2', (0.56, 0.80, 0.45), rough=0.9), mat('hill3', (0.64, 0.84, 0.55), rough=0.9)]
    rnd = random.Random(3)
    for k in range(10):
        x = rnd.uniform(-70, 70); y = rnd.uniform(30, 55)
        ellipsoid(f'hill_{k}', (x, y, -4), (rnd.uniform(14, 24), rnd.uniform(8, 12), rnd.uniform(7, 10)), m=hm[k % 3], segs=32, rings=12, collection=C)


def butterflies(C, n=5):
    objs = []
    cols = [(0.98, 0.55, 0.8), (1.0, 0.82, 0.2), (0.45, 0.7, 1.0), (0.98, 0.5, 0.3), (0.75, 0.55, 0.98)]
    for k in range(n):
        root = bpy.data.objects.new(f'butterfly_{k}', None); C.objects.link(root)
        wm = mat(f'wing_{k}', cols[k % len(cols)], rough=0.5, emis=cols[k % len(cols)], emis_str=0.15)
        ellipsoid(f'bf_body_{k}', (0, 0, 0), (0.008, 0.03, 0.008), m=mat('bf_body', (0.15, 0.1, 0.1)), segs=8, rings=6, sub=0, collection=C).parent = root
        for s in (1, -1):
            piv = bpy.data.objects.new(f'bf_wingpiv_{k}_{s}', None); C.objects.link(piv); piv.parent = root
            w = ellipsoid(f'bf_wing_{k}_{s}', (0.035 * s, 0, 0), (0.035, 0.03, 0.003), m=wm, segs=12, rings=6, sub=0, collection=C)
            w.parent = piv
            w2 = ellipsoid(f'bf_wing2_{k}_{s}', (0.025 * s, 0.03, 0), (0.022, 0.02, 0.003), m=wm, segs=12, rings=6, sub=0, collection=C)
            w2.parent = piv
        objs.append(root)
    return objs


def build_env(scene):
    C = coll('ENV')
    build_sky(scene); build_ground(C)
    house(C)
    for x, col, lbl in ((3.0, (0.35, 0.6, 0.95), 'AYRA'), (4.4, (0.98, 0.62, 0.78), 'PANDORA'), (5.8, (0.42, 0.78, 0.38), 'TIFA')):
        dog_house(C, (x, 5.6), col, lbl)
    swing(C, (-2.6, 4.4))
    pond_bridge(C); stone_path(C); toys(C); clouds(C); hills(C)
    for k, (x, y, s) in enumerate([(-9, 4, 1.3), (-8, 11, 1.5), (-1.5, 9.5, 1.2), (1.5, 10, 1.4), (8.5, 7.5, 1.3), (10, 1, 1.2),
                                   (-10, -3, 1.2), (9, -6, 1.1), (-3.5, 13, 1.5), (6, 12, 1.6), (13, 10, 1.6), (-13, 8, 1.6)]):
        tree(C, (x, y), s, seed=k)
    rnd = random.Random(11)
    cols = [P['pink'], (1.0, 0.85, 0.25), (0.98, 0.98, 0.98), (0.98, 0.45, 0.45), (0.7, 0.55, 0.98), (1.0, 0.6, 0.25)]
    k = 0
    for _ in range(70):  # meadow for Pandora
        x = -4.2 + rnd.gauss(0, 1.1); y = -1.5 + rnd.gauss(0, 0.9)
        flower(C, (x, y), cols[k % len(cols)], k, s=rnd.uniform(0.8, 1.25)); k += 1
    for _ in range(60):  # scattered
        x = rnd.uniform(-9, 9); y = rnd.uniform(-4, 6)
        if math.hypot(x, y) < 2.2 or math.hypot(x - POND_C.x, y - POND_C.y) < 2.6:
            continue
        flower(C, (x, y), cols[k % len(cols)], k, s=rnd.uniform(0.7, 1.1)); k += 1
    # grass tufts near the lawn
    gm = mat('tuft', (0.40, 0.72, 0.28), rough=0.8)
    for j in range(80):
        x = rnd.uniform(-4, 4); y = rnd.uniform(-2.5, 3)
        if math.hypot(x, y) < 1.3:
            continue
        for q in range(3):
            ellipsoid(f'tuft_{j}_{q}', (x + 0.04 * (q - 1), y + 0.02 * q, ground_h(x, y)), (0.035, 0.035, 0.07), (rnd.uniform(-20, 20), (q - 1) * 25, 0), gm,
                      segs=8, rings=6, sub=0, collection=C)
    bfs = butterflies(C)
    # sun + fill
    sun = bpy.data.lights.new('sun', 'SUN'); sun.energy = 3.6; sun.angle = math.radians(8); sun.color = (1.0, 0.95, 0.85)
    so = bpy.data.objects.new('sun', sun); C.objects.link(so); so.rotation_euler = (math.radians(48), 0, math.radians(-30))
    return bfs


def place_on_ground(obj, x, y):
    obj.location = (x, y, ground_h(x, y))


def bake_static(C):
    """Apply modifiers and join all static ENV meshes into one object per ~material group (faster EEVEE sync)."""
    keep = {o.name for o in C.objects if o.name.startswith(('butterfly', 'bf_', 'sun'))}
    objs = [o for o in C.objects if o.name not in keep and o.type in ('MESH', 'FONT')]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.convert(target='MESH')
    objs = [o for o in C.objects if o.name not in keep and o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    j = bpy.context.view_layer.objects.active; j.name = 'ENV_static'
    return j
