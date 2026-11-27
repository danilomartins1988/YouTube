"""Ep. 002 thumbnail plate: the girl on the 4th ACHOU (hat on head, arms up), low close camera, shallow focus.
  blender -b rendering/ep002.blend -P ep2_thumb.py -- OUT.png [T_SECONDS]"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector
import episode2 as E
args = sys.argv[sys.argv.index('--') + 1:]
out = args[0]; t = float(args[1]) if len(args) > 1 else E.ACH[3] + 0.55
E.setup('eevee', 100)
sc = bpy.context.scene; sc.frame_set(int(round(t * E.FPS)) + 1)
bpy.app.handlers.frame_change_pre.clear()
cam = sc.camera; x, y, _, _ = E.move_state('clara', t)
tgt = Vector((x, y, 0.62)); pos = Vector((x + 0.35, y - 1.55, 0.5))
cam.location = pos; cam.rotation_euler = (tgt - pos).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = 50
cam.data.dof.aperture_fstop = 1.4; bpy.data.objects['ep2_focus'].location = Vector((x, y - 0.1, 0.75))
sc.eevee.use_motion_blur = False
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080; sc.render.filepath = out
bpy.ops.render.render(write_still=True); print('THUMB', out)
