"""Clara e as Patinhas - shared Blender helpers (Blender 4.0, bpy).
Geometry primitives with UVs, materials, numpy noise, UV-space pattern baking (fixed fur textures),
simple bone rigs with bone-parented rigid parts, and pose helpers in armature axes.
Everything is procedural/original."""
import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector, Matrix, Euler, Quaternion

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def srgb_to_lin(c):
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def L(r, g, b, a=1.0):
    """sRGB 0-1 -> linear RGBA tuple (for node default values)."""
    v = srgb_to_lin([r, g, b])
    return (float(v[0]), float(v[1]), float(v[2]), a)


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


# ---------------------------------------------------------------- scene
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def coll(name, parent=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    p = parent or bpy.context.scene.collection
    if c.name not in [x.name for x in p.children]:
        p.children.link(c)
    return c


# ---------------------------------------------------------------- materials
def _set(bsdf, names, val):
    for n in names if isinstance(names, (list, tuple)) else [names]:
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = val
            return


def mat(name, color, rough=0.5, sss=0.0, spec=0.5, metallic=0.0, emis=None, emis_str=0.0, coat=0.0, sheen=0.0,
        alpha=1.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    _set(b, 'Base Color', L(*color) if len(color) == 3 else color)
    _set(b, 'Roughness', rough)
    _set(b, ['Subsurface Weight', 'Subsurface'], sss)
    if sss:
        _set(b, 'Subsurface Radius', (0.6, 0.25, 0.15))
        _set(b, 'Subsurface Scale', 0.01)
    _set(b, ['Specular IOR Level', 'Specular'], spec)
    _set(b, 'Metallic', metallic)
    _set(b, ['Coat Weight', 'Clearcoat'], coat)
    _set(b, ['Sheen Weight', 'Sheen'], sheen)
    if emis:
        _set(b, ['Emission Color', 'Emission'], L(*emis))
        _set(b, 'Emission Strength', emis_str)
    if alpha < 1:
        _set(b, 'Alpha', alpha)
        m.blend_method = 'BLEND'
    m.diffuse_color = L(*color) if len(color) == 3 else color
    return m


def img_mat(name, img, rough=0.6, sss=0.0, sheen=0.0, spec=0.4, bump=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = img; t.location = (-400, 200)
    uv = nt.nodes.new('ShaderNodeUVMap'); uv.uv_map = 'UVMap'; uv.location = (-650, 200)
    nt.links.new(uv.outputs['UV'], t.inputs['Vector'])
    nt.links.new(t.outputs['Color'], b.inputs['Base Color'])
    _set(b, 'Roughness', rough); _set(b, ['Subsurface Weight', 'Subsurface'], sss)
    _set(b, ['Sheen Weight', 'Sheen'], sheen); _set(b, ['Specular IOR Level', 'Specular'], spec)
    if bump:
        n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 180.0; n.inputs['Detail'].default_value = 4
        bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.002
        nt.links.new(n.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    return m


def hair_mat(name, color, rough=0.42):
    """Glossy stylized hair: base colour + wave-texture strand bump + lighter sheen."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    _set(b, 'Base Color', L(*color)); _set(b, 'Roughness', rough); _set(b, ['Specular IOR Level', 'Specular'], 0.45)
    _set(b, ['Coat Weight', 'Clearcoat'], 0.08)
    w = nt.nodes.new('ShaderNodeTexWave'); w.wave_type = 'BANDS'; w.bands_direction = 'Z'
    w.inputs['Scale'].default_value = 30.0; w.inputs['Distortion'].default_value = 3.0; w.inputs['Detail'].default_value = 2
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tc.outputs['Object'], w.inputs['Vector'])
    bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.25; bp.inputs['Distance'].default_value = 0.003
    nt.links.new(w.outputs['Fac'], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m.diffuse_color = L(*color)
    return m


# ---------------------------------------------------------------- noise (numpy, deterministic)
def _hash(ix, iy, iz, seed):
    h = (ix * 374761393 + iy * 668265263 + iz * 1274126177 + seed * 974634511) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return (h & 0xFFFF) / 65535.0


def vnoise(P, freq=1.0, seed=0):
    P = np.asarray(P, dtype=np.float64) * freq
    i = np.floor(P).astype(np.int64); f = P - i
    u = f * f * (3 - 2 * f)
    out = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (u[:, 0] if dx else 1 - u[:, 0]) * (u[:, 1] if dy else 1 - u[:, 1]) * (u[:, 2] if dz else 1 - u[:, 2])
                out = out + w * _hash(i[:, 0] + dx, i[:, 1] + dy, i[:, 2] + dz, seed)
    return out


def fbm(P, freq=1.0, seed=0, oct=4, gain=0.5):
    s, a, norm = 0, 1.0, 0
    for o in range(oct):
        s = s + a * vnoise(P, freq * (2 ** o), seed + o * 17)
        norm += a; a *= gain
    return s / norm


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


# ---------------------------------------------------------------- geometry
def _new_bm():
    bm = bmesh.new()
    bm.loops.layers.uv.new('UVMap')
    return bm


def bm_sphere(segs=32, rings=16):
    bm = _new_bm()
    bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=rings, radius=1.0, calc_uvs=True)
    return bm


def ellipsoid(name, center, radii, rot=(0, 0, 0), m=None, segs=32, rings=16, cut=None, sub=1, collection=None,
              deform=None):
    """cut: function(unit_dir Vector)->bool, faces whose all verts True are deleted.
    deform: function(co Vector)->Vector in local (pre-rotation) space after scaling."""
    bm = bm_sphere(segs, rings)
    if cut:
        kill = [v for v in bm.verts if cut(v.co.normalized())]
        bmesh.ops.delete(bm, geom=kill, context='VERTS')
    for v in bm.verts:
        v.co = Vector((v.co.x * radii[0], v.co.y * radii[1], v.co.z * radii[2]))
        if deform:
            v.co = deform(v.co)
    return _finish(name, bm, center, rot, m, sub, collection)


def capsule(name, p0, p1, r0, r1, m=None, segs=24, rings=12, sub=1, collection=None, squash=(1, 1)):
    """Tapered capsule from p0 (radius r0) to p1 (radius r1)."""
    p0, p1 = Vector(p0), Vector(p1)
    Ln = (p1 - p0).length
    bm = bm_sphere(segs, rings)
    for v in bm.verts:
        x, y, z = v.co
        if z <= 1e-6:
            v.co = Vector((x * r0 * squash[0], y * r0 * squash[1], z * r0))
        else:
            v.co = Vector((x * r1 * squash[0], y * r1 * squash[1], Ln + z * r1))
    # add intermediate loops so the shaft subdivides nicely
    edges = [e for e in bm.edges if (e.verts[0].co.z <= 1e-6) != (e.verts[1].co.z <= 1e-6)]
    bmesh.ops.subdivide_edges(bm, edges=edges, cuts=3, use_grid_fill=True)
    q = Vector((0, 0, 1)).rotation_difference((p1 - p0).normalized())
    return _finish(name, bm, p0, q, m, sub, collection)


def tube_along(name, pts, radii, m=None, segs=16, sub=1, collection=None):
    """Smooth tube along a polyline of points (Vector-like) with per-point radii; ends capped by small spheres."""
    pts = [Vector(p) for p in pts]
    bm = _new_bm()
    uvl = bm.loops.layers.uv['UVMap']
    rings = []
    n = len(pts)
    up = Vector((0, 0, 1))
    for i, p in enumerate(pts):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        a = up.cross(t)
        if a.length < 1e-4:
            a = Vector((1, 0, 0))
        a.normalize(); b = t.cross(a).normalized()
        ring = []
        for k in range(segs):
            ang = 2 * math.pi * k / segs
            ring.append(bm.verts.new(p + radii[i] * (math.cos(ang) * a + math.sin(ang) * b)))
        rings.append(ring)
    for i in range(n - 1):
        for k in range(segs):
            f = bm.faces.new((rings[i][k], rings[i][(k + 1) % segs], rings[i + 1][(k + 1) % segs], rings[i + 1][k]))
            for li, (ii, kk) in enumerate([(i, k), (i, k + 1), (i + 1, k + 1), (i + 1, k)]):
                f.loops[li][uvl].uv = (kk / segs, ii / (n - 1))
    # caps
    for ring, tip in ((rings[0], pts[0] - (pts[1] - pts[0]).normalized() * radii[0] * 0.6),
                      (rings[-1], pts[-1] + (pts[-1] - pts[-2]).normalized() * radii[-1] * 0.6)):
        c = bm.verts.new(tip)
        for k in range(segs):
            f = bm.faces.new((ring[k], ring[(k + 1) % segs], c))
            for li in range(3):
                f.loops[li][uvl].uv = (0.5, 0.5)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return _finish(name, bm, (0, 0, 0), (0, 0, 0), m, sub, collection)


def box(name, center, size, m=None, bevel=0.0, collection=None, rot=(0, 0, 0)):
    bm = _new_bm()
    bmesh.ops.create_cube(bm, size=1.0, calc_uvs=True)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    o = _finish(name, bm, center, rot, m, 0, collection, smooth=False)
    if bevel:
        md = o.modifiers.new('bevel', 'BEVEL'); md.width = bevel; md.segments = 3
        o.data.shade_smooth() if hasattr(o.data, 'shade_smooth') else None
        for p in o.data.polygons:
            p.use_smooth = True
        md2 = o.modifiers.new('wn', 'WEIGHTED_NORMAL') if False else None
    return o


def cylinder(name, center, radius, depth, m=None, segs=32, rot=(0, 0, 0), collection=None, smooth=True, sub=0):
    bm = _new_bm()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=radius, radius2=radius,
                          depth=depth, calc_uvs=True)
    return _finish(name, bm, center, rot, m, sub, collection, smooth=smooth, autosmooth=True)


def cone(name, center, r1, r2, depth, m=None, segs=32, rot=(0, 0, 0), collection=None, sub=0):
    bm = _new_bm()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=segs, radius1=r1, radius2=r2, depth=depth,
                          calc_uvs=True)
    return _finish(name, bm, center, rot, m, sub, collection, smooth=True, autosmooth=True)


def _finish(name, bm, loc, rot, m, sub, collection, smooth=True, autosmooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for p in me.polygons:
        p.use_smooth = smooth
    if autosmooth and hasattr(me, 'use_auto_smooth'):
        me.use_auto_smooth = True; me.auto_smooth_angle = math.radians(40)
    o = bpy.data.objects.new(name, me)
    (collection or bpy.context.scene.collection).objects.link(o)
    o.location = Vector(loc)
    if isinstance(rot, Quaternion):
        o.rotation_mode = 'QUATERNION'; o.rotation_quaternion = rot
    else:
        o.rotation_euler = Euler([math.radians(a) for a in rot])
    if m:
        me.materials.append(m)
    if sub:
        md = o.modifiers.new('subsurf', 'SUBSURF'); md.levels = sub; md.render_levels = sub
    return o


def apply_transform(o):
    """Bake object transform into mesh (keeps world placement, identity matrix)."""
    o.data.transform(o.matrix_basis)
    o.matrix_basis = Matrix.Identity(4)


def curve_tube(name, pts, bevel, m=None, collection=None, res=12):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    sp = cu.splines.new('BEZIER'); sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = Vector(p); bp.handle_left_type = bp.handle_right_type = 'AUTO'
    cu.bevel_depth = bevel; cu.bevel_resolution = 4; cu.resolution_u = res; cu.use_fill_caps = True
    o = bpy.data.objects.new(name, cu)
    (collection or bpy.context.scene.collection).objects.link(o)
    if m:
        cu.materials.append(m)
    return o


# ---------------------------------------------------------------- pattern baking (fixed textures)
def bake_pattern(o, fn, size=512, name=None):
    """Rasterise mesh triangles in UV space, interpolate rest-space (world at build time) positions and
    normals, evaluate fn(P, N) -> Nx3 sRGB colours, write to a packed image. Deterministic: the pattern is
    permanently fixed in the texture."""
    me = o.data
    me.calc_loop_triangles()
    uv = me.uv_layers['UVMap'].data
    mw = o.matrix_world.copy()
    nm = mw.to_3x3().inverted().transposed()
    V = np.array([tuple(mw @ v.co) for v in me.vertices])
    Nn = np.array([tuple((nm @ v.normal).normalized()) for v in me.vertices])
    acc = np.zeros((size, size, 3)); filled = np.zeros((size, size), bool)
    Pbuf = np.zeros((size, size, 3)); Nbuf = np.zeros((size, size, 3))
    for tri in me.loop_triangles:
        uvs = np.array([tuple(uv[l].uv) for l in tri.loops]) * (size - 1)
        vi = list(tri.vertices)
        xmin, ymin = np.floor(uvs.min(0)).astype(int); xmax, ymax = np.ceil(uvs.max(0)).astype(int)
        xmin, ymin = max(xmin, 0), max(ymin, 0); xmax, ymax = min(xmax, size - 1), min(ymax, size - 1)
        if xmax < xmin or ymax < ymin:
            continue
        xs, ys = np.meshgrid(np.arange(xmin, xmax + 1), np.arange(ymin, ymax + 1))
        (x0, y0), (x1, y1), (x2, y2) = uvs
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        a = ((y1 - y2) * (xs - x2) + (x2 - x1) * (ys - y2)) / den
        b = ((y2 - y0) * (xs - x2) + (x0 - x2) * (ys - y2)) / den
        c = 1 - a - b
        inside = (a >= -0.02) & (b >= -0.02) & (c >= -0.02)
        if not inside.any():
            continue
        P = a[..., None] * V[vi[0]] + b[..., None] * V[vi[1]] + c[..., None] * V[vi[2]]
        Nv = a[..., None] * Nn[vi[0]] + b[..., None] * Nn[vi[1]] + c[..., None] * Nn[vi[2]]
        yy, xx = ys[inside], xs[inside]
        Pbuf[yy, xx] = P[inside]; Nbuf[yy, xx] = Nv[inside]; filled[yy, xx] = True
    idx = np.nonzero(filled)
    cols = fn(Pbuf[idx], Nbuf[idx])
    acc[idx] = cols
    # dilate to hide seams
    for _ in range(6):
        if filled.all():
            break
        sh = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        add = np.zeros_like(acc); cnt = np.zeros(filled.shape)
        for dy, dx in sh:
            r = np.roll(np.roll(acc, dy, 0), dx, 1); rf = np.roll(np.roll(filled, dy, 0), dx, 1)
            add += r * rf[..., None]; cnt += rf
        new = (~filled) & (cnt > 0)
        acc[new] = add[new] / cnt[new][:, None]; filled = filled | new
    img = bpy.data.images.new(name or (o.name + '_tex'), size, size, alpha=False)
    rgba = np.concatenate([np.clip(acc, 0, 1), np.ones((size, size, 1))], axis=2)
    img.pixels.foreach_set(rgba.astype(np.float32).ravel())
    img.pack()
    return img


# ---------------------------------------------------------------- rigging
def make_armature(name, bones, collection=None):
    """bones: list of (name, head, tail, parent_or_None)."""
    ad = bpy.data.armatures.new(name + '_rig'); ad.display_type = 'STICK'
    arm = bpy.data.objects.new(name, ad)
    (collection or bpy.context.scene.collection).objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode='EDIT')
    for bn, h, t, p in bones:
        eb = ad.edit_bones.new(bn); eb.head = Vector(h); eb.tail = Vector(t); eb.roll = 0
        if p:
            eb.parent = ad.edit_bones[p]; eb.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')
    for pb in arm.pose.bones:
        pb.rotation_mode = 'QUATERNION'
    return arm


def bind(o, arm, bone):
    """Rigidly parent object to a bone keeping its world transform."""
    bpy.context.view_layer.update()
    mw = o.matrix_world.copy()
    o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = bone
    bpy.context.view_layer.update()
    o.matrix_world = mw


def pose(arm, bone, rot=(0, 0, 0), loc=(0, 0, 0), scale=None):
    """Set a pose bone using rotations/offsets expressed in ARMATURE axes (degrees, metres)."""
    pb = arm.pose.bones[bone]
    rest = pb.bone.matrix_local.to_quaternion()
    q = Euler([math.radians(a) for a in rot], 'XYZ').to_quaternion()
    pb.rotation_quaternion = rest.inverted() @ q @ rest
    pb.location = rest.inverted() @ Vector(loc)
    if scale is not None:
        pb.scale = (scale,) * 3 if isinstance(scale, (int, float)) else scale


def reset_pose(arm):
    for pb in arm.pose.bones:
        pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0); pb.scale = (1, 1, 1)


def key_pose(arm, frame):
    for pb in arm.pose.bones:
        pb.keyframe_insert('rotation_quaternion', frame=frame)
        pb.keyframe_insert('location', frame=frame)
        pb.keyframe_insert('scale', frame=frame)


def save_action(arm, name, frames_fn, frame_range):
    """frames_fn(frame) -> applies a pose; keys every frame in range into a new action with fake user."""
    act = bpy.data.actions.new(name); act.use_fake_user = True
    arm.animation_data_create(); arm.animation_data.action = act
    for f in range(frame_range[0], frame_range[1] + 1):
        reset_pose(arm); frames_fn(f); key_pose(arm, f)
    arm.animation_data.action = None
    reset_pose(arm)
    return act


def solid(o, t=0.01, offset=-1.0):
    md = o.modifiers.new('solid', 'SOLIDIFY'); md.thickness = t; md.offset = offset
    md.use_even_offset = True
    o.modifiers.move(len(o.modifiers) - 1, 0)
    return o
