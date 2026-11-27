"""Aditivo 01 cast extension: Toby (male Yorkshire, replaces Tifa) and Milo (orange tabby cat).
Extends cp_chars WITHOUT modifying it (ep. 001/002 keep using cp_chars unchanged).
Candidates only: not canon until the owner approves (see character bible)."""
import math, numpy as np, bpy
from mathutils import Vector
from cp_lib import *
import cp_chars
from cp_chars import *

def cat_pattern_milo(P, N, part):
    x, y, z = P[:, 0], P[:, 1], P[:, 2]
    orange = np.array(hexc('f08a2c')); stripe = np.array(hexc('c9601c')); cream = np.array(hexc('f7e3c0'))
    n = fbm(P, 10.0, seed=31, oct=3)
    col = orange[None] * (1 - n[:, None] * 0.25) + stripe[None] * (n[:, None] * 0.25)
    if part in ('body', 'neck', 'tail', 'head') or part.startswith('leg'):
        k = {'tail': 70.0, 'head': 55.0}.get(part, 38.0)
        coord = y if part != 'tail' else y + z
        s = 0.5 + 0.5 * np.sin(coord * k + 2.5 * fbm(P, 6.0, seed=7, oct=2))
        sm = smooth(0.72, 0.85, s)
        if part == 'body': sm = sm * smooth(-0.3, 0.2, N[:, 2])          # stripes on back/sides, not belly
        if part == 'head': sm = sm * smooth(0.0, 0.5, N[:, 2])           # forehead "M"-ish stripes on top
        col = col * (1 - sm[:, None] * 0.8) + stripe[None] * sm[:, None] * 0.8
    w = np.zeros(len(P))
    if part in ('body', 'neck'):
        w = np.maximum(w, smooth(0.18, 0.13, z) * smooth(0.07, 0.03, np.abs(x)))          # cream belly
        w = np.maximum(w, smooth(0.02, -0.04, y + 0.06) * smooth(0.30, 0.22, z) * smooth(0.08, 0.04, np.abs(x)))  # chest
    if part in ('snout', 'jaw'): w[:] = 0.95                                               # cream muzzle
    if part == 'paw': w[:] = 0.85
    if part == 'tail': w = np.maximum(w, smooth(0.6, 0.66, y) * 0.0)
    return col * (1 - w[:, None]) + cream[None] * w[:, None]

DOGS['toby'] = dict(DOGS['tifa'])
DOGS['milo'] = dict(scale=0.52, body=(0.1, 0.17, 0.1), body_z=0.2, leg_len=0.15, leg_r=(0.036, 0.03), head_r=(0.098, 0.088, 0.09),
                    head_pos=(0, -0.18, 0.35), snout=(0.03, 0.03, 0.026), ear='tri', tail='long', eye='dark', fluff=0.006,
                    pattern=cat_pattern_milo, acc='bandana_purple', hair=None, shells=(3, 0.01), tuft=200, ruff=False)
PAL['bandana_purple'] = (0.56, 0.36, 0.78)

def _retint(obj_filter, rgb, name, **kw):
    m = mat(name, rgb, **kw)
    for o in bpy.data.objects:
        if obj_filter(o):
            o.data.materials.clear(); o.data.materials.append(m)

def build_milo():
    arm = build_dog('milo')
    s = DOGS['milo']['scale']
    arm.scale = (1, 1, 1); reset_pose(arm); bpy.context.view_layer.update()  # build extras in base (unscaled) coords
    # remove the bandana triangle + dots, add a purple collar (torus) on the neck
    for o in [o for o in bpy.data.objects if o.name.startswith('milo_bandana') or o.name.startswith('milo_dot')]:
        bpy.data.objects.remove(o, do_unlink=True)
    cfg = DOGS['milo']; bw, bl, bh = cfg['body']; bz = cfg['body_z']
    bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.011, location=(0, -bl * 0.95, bz + bh * 0.7), rotation=(math.radians(72), 0, 0))
    col_ = bpy.context.active_object; col_.name = 'milo_collar'
    col_.data.materials.append(mat('milo_collar', PAL['bandana_purple'], rough=0.45, coat=0.3))
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.012, location=(0, -bl * 0.95 - 0.05, bz + bh * 0.7 - 0.03))
    tag = bpy.context.active_object; tag.name = 'milo_moon_tag'; tag.scale = (1, 0.4, 1)
    tag.data.materials.append(mat('milo_tag', (0.98, 0.86, 0.35), rough=0.25, spec=0.9))
    for o in (col_, tag):
        o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = 'neck'
        o.matrix_parent_inverse = (arm.matrix_world @ arm.pose.bones['neck'].matrix).inverted()
    # cat ears: bigger and pointier
    for o in [o for o in bpy.data.objects if o.name.startswith('milo_ear_')]:
        o.scale = (o.scale[0] * 1.25, o.scale[1], o.scale[2] * 1.55)
    # green eyes, pink nose
    _retint(lambda o: o.name.startswith('milo_eye') and o.data and o.data.materials and 'iris' in (o.data.materials[0].name.lower()), (0.37, 0.75, 0.29), 'milo_iris')
    _retint(lambda o: o.name == 'milo_nose', (0.95, 0.63, 0.66), 'milo_nose_pink', rough=0.35)
    # whiskers
    hx, hy, hz = cfg['head_pos']; sl = cfg['snout'][0]
    for x in (1, -1):
        for k, dz in enumerate((-0.006, 0.004, 0.014)):
            p0 = Vector((0.02 * x, hy - 0.09 - sl * 0.5, hz - 0.03 + dz)); p1 = p0 + Vector((0.07 * x, 0.01, -0.01 + dz * 0.8))
            bpy.ops.mesh.primitive_cylinder_add(radius=0.0012, depth=(p1 - p0).length, location=(p0 + p1) / 2)
            w = bpy.context.active_object; w.name = f'milo_whisker_{x}_{k}'
            w.rotation_euler = (p1 - p0).to_track_quat('Z', 'Y').to_euler()
            w.data.materials.append(mat('whisker', (0.97, 0.96, 0.93), rough=0.4))
            w.parent = arm; w.parent_type = 'BONE'; w.parent_bone = 'head'
            w.matrix_parent_inverse = (arm.matrix_world @ arm.pose.bones['head'].matrix).inverted()
    arm.scale = (s, s, s); bpy.context.view_layer.update()
    return arm

_orig_build = cp_chars.build
def build(name):
    if name == 'milo': return build_milo()
    return _orig_build(name)
