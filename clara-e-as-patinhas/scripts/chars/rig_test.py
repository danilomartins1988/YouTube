"""Quick rig test on an AI quadruped mesh: clean floaters, auto-weight a simple quadruped armature, render 4 poses.
blender -b -P rig_test.py -- IN.ply OUTDIR NAME"""
import bpy, bmesh, sys, os, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]; src, out, name = a
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.ply_import(filepath=src)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]; ob.data = ob.data.copy()
bpy.context.view_layer.objects.active = ob; ob.select_set(True)
d = ob.modifiers.new('d', 'DECIMATE'); d.ratio = 40000 / len(ob.data.polygons); bpy.ops.object.modifier_apply(modifier='d')
ob.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(rotation=True)
# drop small floating pieces (e.g. broken whiskers)
bm = bmesh.new(); bm.from_mesh(ob.data); bm.verts.ensure_lookup_table()
seen = set(); parts = []
for v in bm.verts:
    if v.index in seen: continue
    st = [v]; comp = []; seen.add(v.index)
    while st:
        x = st.pop(); comp.append(x)
        for e in x.link_edges:
            o = e.other_vert(x)
            if o.index not in seen: seen.add(o.index); st.append(o)
    parts.append(comp)
big = max(len(p) for p in parts)
kill = [v for p in parts if len(p) < 0.02 * big for v in p]
bmesh.ops.delete(bm, geom=kill, context='VERTS'); bm.to_mesh(ob.data); bm.free()
bb = [Vector(c) for c in ob.bound_box]; zmin = min(v.z for v in bb); h = max(v.z for v in bb) - zmin
cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8
ob.location = (-cx, -cy, -zmin); bpy.ops.object.transform_apply(location=True)
s = 1 / h; ob.scale = (s, s, s); bpy.ops.object.transform_apply(scale=True)
bpy.ops.object.shade_smooth()
bb = [Vector(c) for c in ob.bound_box]; y0 = min(v.y for v in bb); y1 = max(v.y for v in bb); L = y1 - y0; W = max(v.x for v in bb)
m = bpy.data.materials.new('vc'); m.use_nodes = True; nt = m.node_tree; ca = nt.nodes.new('ShaderNodeVertexColor')
nt.links.new(ca.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color']); ob.data.materials.clear(); ob.data.materials.append(m)
# armature (front = -Y). Proportions from the bounding box
bpy.ops.object.armature_add(location=(0, 0, 0)); arm = bpy.context.object; arm.name = name + '_rig'
bpy.ops.object.mode_set(mode='EDIT'); eb = arm.data.edit_bones; eb.remove(eb[0])
def B(n, hd, tl, par=None):
    b = eb.new(n); b.head = Vector(hd); b.tail = Vector(tl)
    if par: b.parent = eb[par]
    return b
yf, yr = y0 + 0.30 * L, y0 + 0.78 * L; zb = 0.42
B('spine', (0, yr, zb), (0, yf, zb + 0.03))
B('neck', (0, yf, zb + 0.03), (0, y0 + 0.2 * L, 0.66), 'spine')
B('head', (0, y0 + 0.2 * L, 0.66), (0, y0 + 0.2 * L, 0.95), 'neck')
B('tail1', (0, yr + 0.02, zb + 0.05), (0, yr + 0.1 * L, zb + 0.2), 'spine')
B('tail2', (0, yr + 0.1 * L, zb + 0.2), (0, yr + 0.15 * L, zb + 0.45), 'tail1')
for side, x in (('L', 0.42 * W), ('R', -0.42 * W)):
    for fb, yy in (('F', yf + 0.02), ('B', yr - 0.03)):
        B(f'leg_{fb}{side}1', (x, yy, zb - 0.02), (x, yy, 0.18), 'spine')
        B(f'leg_{fb}{side}2', (x, yy, 0.18), (x, yy - 0.03, 0.0), f'leg_{fb}{side}1')
bpy.ops.object.mode_set(mode='OBJECT')
ob.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
try:
    bpy.ops.object.parent_set(type='ARMATURE_AUTO'); how = 'automatic weights'
except Exception as e:
    bpy.ops.object.parent_set(type='ARMATURE_ENVELOPE'); how = f'envelope (auto failed: {e})'
empty_groups = [g.name for g in ob.vertex_groups if not any(g.index in [x.group for x in v.groups] for v in ob.data.vertices[:20000])]
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 16; sc.render.resolution_x = sc.render.resolution_y = 520
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.93, 0.94, 0.96, 1)
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(30))); bpy.context.object.data.energy = 3
bpy.ops.object.camera_add(location=(1.9, -2.2, 0.9)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 55
bpy.ops.object.empty_add(location=(0, 0, 0.42)); t = bpy.context.object; c = cam.constraints.new('TRACK_TO'); c.target = t; c.track_axis = 'TRACK_NEGATIVE_Z'; c.up_axis = 'UP_Y'
P = arm.pose.bones
poses = {'rest': {}, 'head_tilt': {'head': (0, 0, 0.0, 0.35), 'neck': (0.2, 0, 0, 0)}, 'tail_wag': {'tail1': (0, 0, 0.6, 0), 'tail2': (0, 0, 0.6, 0)},
         'paw_lift': {'leg_FL1': (-0.9, 0, 0, 0), 'leg_FL2': (1.3, 0, 0, 0)}}
for pn, rot in poses.items():
    for pb in P: pb.rotation_mode = 'XYZ'; pb.rotation_euler = (0, 0, 0)
    for bn, (rx, ry, rz, rz2) in rot.items(): P[bn].rotation_euler = (rx, ry, rz + rz2)
    bpy.context.view_layer.update(); sc.render.filepath = f'{out}/{name}_pose_{pn}.png'; bpy.ops.render.render(write_still=True)
print('RIGDONE', name, how, 'parts removed', len([p for p in parts if len(p) < 0.02 * big]), 'empty groups(sample)', empty_groups)
