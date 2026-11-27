"""Episode 002 "Cadê? Achou!" - scene build from the ep. 001 garden + quality-level still tests.

  blender -b rendering/ep001.blend -P ep2_scene.py -- build            -> rendering/ep002.blend (ep001.blend is never saved)
  blender -b rendering/ep002.blend -P ep2_scene.py -- still SHOT LEVEL OUT.png [RESPCT]

Ep. 002 changes to the set: name labels on the dog houses removed (owner rule: no names on screen) and replaced by
paw emblems; new hiding props: giant flower, big toy bucket, straw sun hat.
LEVELS: L0 = ep. 001 settings; L1 = native 1080p + key/rim/fill + Standard view + compositor grade/vignette + DOF;
L1M = L1 + motion blur, contact shadows, 2048 cube shadows (no SSR); L2 = L1 + 32 samples, contact
shadows, SSR, motion blur, larger shadow maps; L3 = L2 + 64 samples + particle hair on the dogs."""
import bpy, sys, os, math, time, bmesh
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
from cp_lib import *
from cp_lib import _finish, _new_bm
from cp_motion import Acc, breathe, sit, clap_pose, ease
from cp_chars import face
from cp_env import ground_h

ROOTP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPOT = {'flower': (-1.05, 0.55), 'bucket': (0.05, 1.0), 'hat': (1.1, 0.5)}


# ------------------------------------------------------------------ props
def open_bucket(name, loc, r1, r2, h, m, inner, C):
    bm = _new_bm()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=40, radius1=r1, radius2=r2, depth=h, calc_uvs=True)
    top = [f for f in bm.faces if all(v.co.z > h / 2 - 1e-5 for v in f.verts)]
    bmesh.ops.delete(bm, geom=top, context='FACES_ONLY')
    o = _finish(name, bm, loc, (0, 0, 0), m, 0, C)
    o.data.materials.append(inner)
    so = o.modifiers.new('solid', 'SOLIDIFY'); so.thickness = 0.012; so.material_offset = 1; so.offset = -1
    sb = o.modifiers.new('sub', 'SUBSURF'); sb.levels = sb.render_levels = 1
    return o


def straw_mat():
    m = bpy.data.materials.new('straw'); m.use_nodes = True; nt = m.node_tree; b = nt.nodes['Principled BSDF']
    w = nt.nodes.new('ShaderNodeTexWave'); w.inputs['Scale'].default_value = 40; w.inputs['Distortion'].default_value = 2
    w.wave_type = 'RINGS'
    cr = nt.nodes.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = L(0.86, 0.70, 0.40); cr.color_ramp.elements[1].color = L(0.98, 0.88, 0.60)
    nt.links.new(w.outputs['Fac'], cr.inputs['Fac']); nt.links.new(cr.outputs['Color'], b.inputs['Base Color'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.35
    nt.links.new(w.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Roughness'].default_value = 0.8
    return m


def build_props():
    C = coll('EP2_PROPS')
    # 1) giant flower (coral petals, yellow centre, two big leaves) - Ayra hides behind it
    fx, fy = SPOT['flower']; z0 = ground_h(fx, fy)
    stem = mat('gf_stem', (0.30, 0.62, 0.22), rough=0.6)
    tube_along('gf_stem', [(fx, fy + 0.02, z0), (fx + 0.01, fy + 0.03, z0 + 0.15), (fx, fy + 0.02, z0 + 0.30)], [0.022, 0.02, 0.018], stem, collection=C)
    for s in (1, -1):
        ellipsoid(f'gf_leaf_{s}', (fx + 0.15 * s, fy - 0.02, z0 + 0.09), (0.16, 0.035, 0.07), (0, -25 * s, 0), stem, segs=24, rings=12, collection=C)
    hz = z0 + 0.30; petal = mat('gf_petal', (1.0, 0.52, 0.50), rough=0.45, sss=0.15, sheen=0.3)
    for k in range(11):
        a = 2 * math.pi * k / 11
        ellipsoid(f'gf_petal_{k}', (fx + 0.13 * math.cos(a), fy - 0.01, hz + 0.13 * math.sin(a)), (0.09, 0.02, 0.05),
                  (0, -math.degrees(a), 0), petal, segs=20, rings=10, collection=C)
    ellipsoid('gf_center', (fx, fy - 0.035, hz), (0.075, 0.035, 0.075), m=mat('gf_center', (1.0, 0.78, 0.15), rough=0.7, sheen=0.4), collection=C)
    # 2) big toy bucket (sky blue, white rim stripe, yellow handle) - Pandora inside
    bx, by = SPOT['bucket']; z0 = ground_h(bx, by)
    bk = mat('ep2_bucket', (0.33, 0.66, 0.97), rough=0.3, coat=0.6); inner = mat('ep2_bucket_in', (0.20, 0.45, 0.80), rough=0.5)
    open_bucket('ep2_bucket', (bx, by, z0 + 0.12), 0.19, 0.22, 0.24, bk, inner, C)
    curve_tube('ep2_bucket_band', [(bx + 0.223 * math.cos(a), by + 0.223 * math.sin(a), z0 + 0.235) for a in [2 * math.pi * k / 24 for k in range(25)]],
               0.012, mat('ep2_white', (0.98, 0.98, 0.96), rough=0.35, coat=0.4), C)
    hm = mat('ep2_handle', (1.0, 0.80, 0.15), rough=0.35, coat=0.5)
    curve_tube('ep2_bucket_handle', [(bx - 0.22, by, z0 + 0.22), (bx - 0.19, by + 0.14, z0 + 0.25), (bx, by + 0.24, z0 + 0.27),
                                     (bx + 0.19, by + 0.14, z0 + 0.25), (bx + 0.22, by, z0 + 0.22)], 0.008, hm, C)
    # 3) straw sun hat with a yellow ribbon, tilted over Tifa
    tx, ty = SPOT['hat']; z0 = ground_h(tx, ty)
    sm = straw_mat(); rib = mat('ep2_ribbon', (1.0, 0.78, 0.12), rough=0.4, sheen=0.5)
    hat = bpy.data.objects.new('ep2_hat', None); C.objects.link(hat); hat.location = (tx, ty + 0.03, z0 + 0.075); hat.rotation_euler = (math.radians(-9), 0, 0)
    brim = cylinder('ep2_hat_brim', (0, 0, 0), 0.29, 0.012, sm, segs=48, collection=C); brim.parent = hat
    crown = ellipsoid('ep2_hat_crown', (0, 0, 0.0), (0.14, 0.14, 0.12), m=sm, segs=32, rings=16, collection=C,
                      cut=lambda d: d.z < -0.05); crown.parent = hat
    band = cylinder('ep2_hat_band', (0, 0, 0.03), 0.142, 0.035, rib, segs=40, collection=C); band.parent = hat
    return C


def paw_emblems():
    """Replace the name labels on the dog houses with a white paw (no names on screen from ep. 002 on)."""
    w = mat('label', (0.97, 0.97, 0.95))
    for o in [o for o in bpy.data.objects if o.name.startswith('lbl_')]:
        x, y, z = o.location
        C = o.users_collection[0]
        bpy.data.objects.remove(o, do_unlink=True)
        ellipsoid(f'paw_pad_{x:.1f}', (x, y - 0.005, z - 0.01), (0.055, 0.01, 0.045), m=w, segs=20, rings=10, collection=C)
        for k, (dx, dz) in enumerate([(-0.06, 0.05), (-0.02, 0.075), (0.02, 0.075), (0.06, 0.05)]):
            ellipsoid(f'paw_toe_{x:.1f}_{k}', (x + dx, y - 0.005, z - 0.01 + dz), (0.018, 0.01, 0.022), m=w, segs=12, rings=8, collection=C)


def light_rig():
    sc = bpy.context.scene
    key = bpy.data.objects['sun']
    rim = bpy.data.lights.new('ep2_rim', 'SUN'); rim.energy = 0.0; rim.angle = math.radians(6); rim.color = (1.0, 0.86, 0.70)
    r = bpy.data.objects.new('ep2_rim', rim); sc.collection.objects.link(r); r.rotation_euler = (math.radians(-62), 0, math.radians(-160))
    fill = bpy.data.lights.new('ep2_fill', 'AREA'); fill.energy = 0.0; fill.size = 6; fill.color = (0.80, 0.88, 1.0)
    f = bpy.data.objects.new('ep2_fill', fill); sc.collection.objects.link(f); f.location = (0, -6, 3.5)
    f.rotation_euler = (Vector((0, 0.5, 0.4)) - f.location).to_track_quat('-Z', 'Y').to_euler()
    foc = bpy.data.objects.new('ep2_focus', None); sc.collection.objects.link(foc)
    old = bpy.data.objects.get('bucket')
    if old:
        bpy.data.objects.remove(old, do_unlink=True)  # ep1 small toy bucket: avoid two buckets


def build():
    paw_emblems(); build_props(); light_rig()
    out = os.path.join(ROOTP, 'rendering', 'ep002.blend')
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True, copy=True)
    print('SAVED', out)


# ------------------------------------------------------------------ quality levels
def level(lv, pct=100):
    sc = bpy.context.scene; e = sc.eevee; cam = sc.camera
    key = bpy.data.objects['sun'].data; rim = bpy.data.objects['ep2_rim'].data; fill = bpy.data.objects['ep2_fill'].data
    if lv == 'L0':
        sc.render.resolution_x, sc.render.resolution_y = 1280, 720; e.taa_render_samples = 8
        return
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.resolution_percentage = pct
    e.taa_render_samples = {'L1': 16, 'L1M': 16, 'L2': 32, 'L3': 64}[lv]
    # light: softer warm key, warm rim from behind, cool sky fill from the camera side
    key.energy = 3.3; key.angle = math.radians(14); key.color = (1.0, 0.93, 0.82)
    rim.energy = 2.0; fill.energy = 90
    w = sc.world.node_tree.nodes.get('Background')
    sc.view_settings.view_transform = os.environ.get('EP2_VT', 'Standard'); sc.view_settings.look = os.environ.get('EP2_LOOK', 'None'); sc.view_settings.exposure = float(os.environ.get('EP2_EXP', '0.0'))
    e.use_gtao = True; e.gtao_distance = 0.6; e.gtao_factor = 1.2
    e.use_soft_shadows = True; e.shadow_cascade_size = '4096'; e.shadow_cube_size = '1024'
    e.use_bloom = True; e.bloom_intensity = 0.03; e.bloom_threshold = 1.0; e.bloom_radius = 5.5
    # depth of field
    cam.data.dof.use_dof = True; cam.data.dof.focus_object = bpy.data.objects['ep2_focus']; cam.data.dof.aperture_fstop = 2.2
    e.bokeh_max_size = 60
    # compositor grade: gentle warm lift/gain + soft vignette
    sc.use_nodes = True; nt = sc.node_tree; nt.nodes.clear()
    rl = nt.nodes.new('CompositorNodeRLayers'); cb = nt.nodes.new('CompositorNodeColorBalance'); cb.correction_method = 'LIFT_GAMMA_GAIN'
    cb.lift = (1.01, 1.0, 0.98); cb.gamma = (1.0, 1.0, 0.99); cb.gain = (1.03, 1.01, 0.97)
    ell = nt.nodes.new('CompositorNodeEllipseMask'); ell.width = 1.25; ell.height = 1.15
    bl = nt.nodes.new('CompositorNodeBlur'); bl.size_x = bl.size_y = 300; bl.filter_type = 'FAST_GAUSS'; bl.use_relative = False
    mr = nt.nodes.new('CompositorNodeMapRange'); mr.inputs['To Min'].default_value = 0.82
    mx = nt.nodes.new('CompositorNodeMixRGB'); mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0
    comp = nt.nodes.new('CompositorNodeComposite')
    nt.links.new(rl.outputs['Image'], cb.inputs['Image']); nt.links.new(ell.outputs['Mask'], bl.inputs['Image'])
    nt.links.new(bl.outputs['Image'], mr.inputs['Value'])
    nt.links.new(cb.outputs['Image'], mx.inputs[1]); nt.links.new(mr.outputs['Value'], mx.inputs[2]); nt.links.new(mx.outputs['Image'], comp.inputs['Image'])
    if lv in ('L1M', 'L2', 'L3'):
        e.use_ssr = lv != 'L1M'; e.use_ssr_halfres = True
        e.use_motion_blur = True; e.motion_blur_shutter = 0.5; e.motion_blur_steps = 1
        e.shadow_cube_size = '2048'
        for l in (key, rim):
            l.use_contact_shadow = True; l.contact_shadow_distance = 0.15
    if lv == 'L3':
        add_hair()


def add_hair():
    """Particle hair on the dogs' body/neck/tail shells' base meshes (strand render in EEVEE)."""
    cfgc = {'ayra': (2200, 0.028, (0.55, 0.30, 0.18)), 'pandora': (2600, 0.04, (0.97, 0.96, 0.94)), 'tifa': (1800, 0.025, (0.55, 0.42, 0.25))}
    for n, (cnt, ln, col) in cfgc.items():
        hm = mat(f'{n}_strand', col, rough=0.55, sheen=0.6)
        for o in [o for o in bpy.data.objects if o.name.startswith(f'{n}_') and o.type == 'MESH' and 'shell' not in o.name
                  and any(p in o.name for p in ('body', 'neck', 'tail', 'ruff'))]:
            o.data.materials.append(hm)
            ps = o.modifiers.new('hair', 'PARTICLE_SYSTEM').particle_system; st = ps.settings
            st.type = 'HAIR'; st.count = cnt; st.hair_length = ln; st.use_advanced_hair = True
            st.normal_factor = ln; st.factor_random = ln * 0.3; st.object_align_factor = (0, ln * 0.8, -ln * 0.3)
            st.child_type = 'INTERPOLATED'; st.rendered_child_count = 6; st.clump_factor = 0.4; st.roughness_1 = 0.003
            st.root_radius = 1.0; st.tip_radius = 0.0; st.radius_scale = 0.002; st.material = len(o.data.materials); st.hair_step = 3; st.render_step = 3


# ------------------------------------------------------------------ shots (static story poses)
def put(name, x, y, heading, dz=0.0):
    a = bpy.data.objects[name]; a.location = (x, y, max(ground_h(x, y), 0.0) + dz); a.rotation_euler = (0, 0, math.radians(heading))


def aim(loc, tgt, lens):
    cam = bpy.context.scene.camera; cam.location = Vector(loc); cam.data.lens = lens
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.data.objects['ep2_focus'].location = Vector(tgt)


def pose_all(spec):
    for n in ('clara', 'ayra', 'pandora', 'tifa'):
        arm = bpy.data.objects[n]; reset_pose(arm)
        A = Acc(); breathe(A, arm, 0.3)
        expr, extra = spec.get(n, ('happy', None))
        if extra:
            extra(A, arm)
        face(arm, expr, blink=0.0, A=A); A.apply(arm)


def clara_search(A, arm):
    A.rot('chest', 12, 0, 0); A.rot('head', 6, 0, 10)
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -25, 0, -18 * x); A.rot(f'forearm_{s}', -50, 0, -20 * x)


def clara_peek_hide(A, arm):
    # holds the straw sun hat in front of her face (the rigid chibi rig cannot reach the eyes with the hands)
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -88, 0, -22 * x); A.rot(f'forearm_{s}', -35, 0, -30 * x)
    A.rot('head', 6, 0, 0)


def clara_achou(A, arm):
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -15, -105 * x, 0); A.rot(f'forearm_{s}', 0, -25 * x, 0)
    A.rot('head', -6, 0, 0)


def ayra_peek(A, arm):
    A.rot('head', -10, 0, -28); A.rot('neck', 0, 0, -15)


def pandora_bucket(A, arm):
    sit(A, arm, 0.6); A.rot('head', 30, 0, 0)


def tifa_hat(A, arm):
    A.loc('root', 0, 0, -0.2); A.rot('head', -14, 0, 0)


def shot(name):
    fx, fy = SPOT['flower']; bx, by = SPOT['bucket']; tx, ty = SPOT['hat']
    if name in ('wide', 'flower', 'bucket', 'hat'):
        put('ayra', fx + 0.19, fy + 0.3, 15, -0.03); put('pandora', bx, by + 0.03, 180, 0.07); put('tifa', tx, ty + 0.025, 0, 0.0)
        put('clara', 0.0, -0.55, 175 if name == 'wide' else {'flower': 140, 'bucket': 180, 'hat': 215}[name])
        pose_all({'clara': ('curious', clara_search), 'ayra': ('happy', ayra_peek), 'pandora': ('happy', pandora_bucket), 'tifa': ('happy', tifa_hat)})
    if name == 'wide':
        aim((0.3, -3.6, 1.05), (0.0, 0.5, 0.3), 32); bpy.data.objects['ep2_focus'].location = (0.0, -0.55, 0.5)
    elif name == 'flower':
        aim((fx - 0.3, fy - 1.45, 0.45), (fx + 0.06, fy, 0.32), 42)
    elif name == 'bucket':
        aim((bx + 0.25, by - 1.1, 0.48), (bx, by, 0.22), 50)
    elif name == 'hat':
        aim((tx - 0.2, ty - 1.0, 0.32), (tx, ty - 0.05, 0.12), 50)
    elif name in ('finale_hide', 'finale_achou'):
        put('clara', 0.0, 0.0, 0); put('ayra', 0.55, 0.15, -20); put('pandora', -0.5, 0.15, 20); put('tifa', 0.32, -0.3, -10)
        cf = clara_peek_hide if name == 'finale_hide' else clara_achou
        hat = bpy.data.objects['ep2_hat']
        if name == 'finale_hide':
            hat.location = (0.0, -0.33, 0.80); hat.rotation_euler = (math.radians(88), 0, 0)
        else:
            hat.location = (0.0, 0.02, 0.97); hat.rotation_euler = (math.radians(-8), math.radians(10), 0)  # ACHOU: hat lands on her head
        pose_all({'clara': ('happy', cf), 'ayra': ('curious', None), 'pandora': ('curious', None), 'tifa': ('surprised', None)})
        aim((0.05, -2.3, 0.7), (0.0, 0.0, 0.62), 40)


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    if args[0] == 'build':
        build()
    elif args[0] == 'still':
        sname, lv, out = args[1], args[2], args[3]
        pct = int(args[4]) if len(args) > 4 else 100
        bpy.app.handlers.frame_change_pre.clear()
        shot(sname); level(lv, pct)
        sc = bpy.context.scene; sc.render.filepath = out
        t0 = time.time(); bpy.ops.render.render(write_still=True); t1 = time.time()
        if os.environ.get('EP2_WARM'):  # second render = steady-state time per frame (shaders already compiled)
            sc.frame_set(sc.frame_current + 1); bpy.ops.render.render(write_still=True)
        print(f'RENDER_TIME {sname} {lv} first {t1 - t0:.1f}s warm {time.time() - t1:.1f}s')
