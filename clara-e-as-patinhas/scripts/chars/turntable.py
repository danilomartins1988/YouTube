"""Import an AI-generated mesh (PLY with vertex colours), clean + decimate, render a turntable (EEVEE, CPU).
blender -b -P turntable.py -- IN.ply OUTDIR NAME [frames] [target_faces]"""
import bpy, sys, os, math
from mathutils import Vector
a = sys.argv[sys.argv.index('--') + 1:]
src, out, name = a[0], a[1], a[2]; nfr = int(a[3]) if len(a) > 3 else 12; target = int(a[4]) if len(a) > 4 else 60000
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.ply_import(filepath=src)
ob = [o for o in bpy.context.scene.objects if o.type == 'MESH'][0]; ob.name = name
for o in list(bpy.context.scene.objects):
    if o != ob: bpy.data.objects.remove(o)
ob.data = ob.data.copy(); me = ob.data; nf = len(me.polygons)
dec = ob.modifiers.new('dec', 'DECIMATE'); dec.ratio = min(1.0, target / max(1, nf))
bpy.context.view_layer.objects.active = ob; bpy.ops.object.modifier_apply(modifier='dec')
bpy.ops.object.shade_smooth()
ob.rotation_euler = (math.radians(90), 0, 0); bpy.ops.object.transform_apply(rotation=True)  # undo the y-up export rotation of run_trellis.py
# normalise: feet on z=0, centre, height 1
bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
zmin = min(v.z for v in bb); h = max(v.z for v in bb) - zmin
cx = sum(v.x for v in bb) / 8; cy = sum(v.y for v in bb) / 8
ob.location = (-cx, -cy, -zmin); bpy.ops.object.transform_apply(location=True)
s = 1.0 / h; ob.scale = (s, s, s); bpy.ops.object.transform_apply(scale=True)
m = bpy.data.materials.new('vc'); m.use_nodes = True; nt = m.node_tree
bsdf = nt.nodes['Principled BSDF']; ca = nt.nodes.new('ShaderNodeVertexColor')
if me.color_attributes: ca.layer_name = me.color_attributes[0].name
nt.links.new(ca.outputs['Color'], bsdf.inputs['Base Color']); bsdf.inputs['Roughness'].default_value = 0.6
me.materials.clear(); me.materials.append(m)
sc = bpy.context.scene; sc.render.engine = 'BLENDER_EEVEE'; sc.eevee.taa_render_samples = 16
sc.render.resolution_x = sc.render.resolution_y = 640; sc.render.film_transparent = False
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; w.node_tree.nodes['Background'].inputs[0].default_value = (0.93, 0.94, 0.96, 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.9
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(30))); bpy.context.object.data.energy = 3.0
bpy.ops.mesh.primitive_plane_add(size=6); fl = bpy.context.object; fm = bpy.data.materials.new('fl'); fm.diffuse_color = (0.9, 0.92, 0.9, 1); fl.data.materials.append(fm)
bpy.ops.object.empty_add(location=(0, 0, 0.45)); piv = bpy.context.object
bpy.ops.object.camera_add(location=(0, -3.0, 0.75)); cam = bpy.context.object; sc.camera = cam; cam.data.lens = 60
tc = cam.constraints.new('TRACK_TO'); tc.target = piv; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cam.parent = piv
for i in range(nfr):
    piv.rotation_euler = (0, 0, 2 * math.pi * i / nfr)
    sc.render.filepath = f'{out}/{name}_{i:02d}.png'; bpy.ops.render.render(write_still=True)
print('DONE', name, 'faces', nf, '->', len(ob.data.polygons), 'colors', [c.name for c in me.color_attributes])
