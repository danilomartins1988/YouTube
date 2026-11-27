# Simple test scene for render-engine benchmarking (1920x1080). Usage:
# blender -b -P diag_render_test.py -- ENGINE OUTPNG [samples]
import bpy, sys, time
args = sys.argv[sys.argv.index("--")+1:]
engine, out = args[0], args[1]
samples = int(args[2]) if len(args) > 2 else 32
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
bpy.ops.mesh.primitive_plane_add(size=20)
g = bpy.context.object; m = bpy.data.materials.new("g"); m.use_nodes=True
m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=(0.3,0.7,0.25,1); g.data.materials.append(m)
for i,c in enumerate([(1,.8,.1,1),(.9,.4,.6,1),(.3,.6,1,1)]):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(i*2-2,0,0.8), segments=48, ring_count=24)
    bpy.ops.object.shade_smooth()
    o=bpy.context.object; mm=bpy.data.materials.new(f"m{i}"); mm.use_nodes=True
    mm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value=c; o.data.materials.append(mm)
bpy.ops.object.light_add(type='SUN', rotation=(0.8,0.2,0.5)); bpy.context.object.data.energy=3; bpy.context.object.data.angle=0.2
w=bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True; w.node_tree.nodes["Background"].inputs[0].default_value=(0.5,0.7,1,1)
bpy.ops.object.camera_add(location=(0,-9,3.5), rotation=(1.25,0,0)); sc.camera=bpy.context.object
sc.render.resolution_x, sc.render.resolution_y = 1920,1080
sc.render.engine = engine
if engine=='CYCLES':
    sc.cycles.device='CPU'; sc.cycles.samples=samples; sc.cycles.use_denoising=False
elif engine=='BLENDER_EEVEE':
    sc.eevee.taa_render_samples=samples
sc.render.filepath=out
t=time.time(); bpy.ops.render.render(write_still=True); print(f"RENDERTIME {engine} {samples} {time.time()-t:.2f}s")
