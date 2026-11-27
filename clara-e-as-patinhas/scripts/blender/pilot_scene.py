"""Pilot "Pata Pata Patatá" scene: ep. 002 garden (L1M lights, Toby forelock, paw emblems) without the ep. 002 hiding
props, plus Milo (cast5). blender -b rendering/ep002.blend -P pilot_scene.py  -> rendering/pilot.blend"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cast5
ROOTP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for o in list(bpy.data.objects):
    if o.name.startswith(('gf_', 'ep2_bucket', 'ep2_hat', 'ep2_flower')):
        bpy.data.objects.remove(o, do_unlink=True)
arm = cast5.build_milo()
print('MILO', arm.name, len([o for o in bpy.data.objects if o.name.startswith('milo')]))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOTP, 'rendering', 'pilot.blend'), compress=True, copy=True)
print('SAVED pilot.blend')
