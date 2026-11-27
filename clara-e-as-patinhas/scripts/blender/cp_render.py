"""Render setup helpers: studio for sheets, EEVEE settings, cameras."""
import bpy, math
from mathutils import Vector
from cp_lib import *


def eevee(scene, res=(1920, 1080), samples=32, pct=100, fps=30):
    scene.render.engine = 'BLENDER_EEVEE'
    e = scene.eevee
    e.taa_render_samples = samples
    e.use_gtao = True; e.gtao_distance = 0.4; e.gtao_factor = 1.0
    e.use_bloom = True; e.bloom_intensity = 0.02; e.bloom_threshold = 1.2
    e.use_soft_shadows = True
    e.shadow_cube_size = '1024'; e.shadow_cascade_size = '2048'
    e.use_ssr = False
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = pct
    scene.render.fps = fps
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
    scene.view_settings.exposure = 0.0
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGB'


def studio(scene, bg=(0.86, 0.92, 0.98)):
    w = bpy.data.worlds.new('studio'); scene.world = w; w.use_nodes = True
    bgn = w.node_tree.nodes['Background']; bgn.inputs[0].default_value = L(*bg); bgn.inputs[1].default_value = 0.9
    sun = bpy.data.lights.new('key', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(12); sun.color = (1.0, 0.96, 0.9)
    o = bpy.data.objects.new('key', sun); scene.collection.objects.link(o); o.rotation_euler = (math.radians(50), 0, math.radians(-35))
    fill = bpy.data.lights.new('fill', 'AREA'); fill.energy = 120; fill.size = 3; fill.color = (0.85, 0.9, 1.0)
    f = bpy.data.objects.new('fill', fill); scene.collection.objects.link(f); f.location = (3, -3, 2)
    f.rotation_euler = Vector((-3, 3, -1.5)).to_track_quat('-Z', 'Y').to_euler()
    rim = bpy.data.lights.new('rim', 'AREA'); rim.energy = 150; rim.size = 2
    r = bpy.data.objects.new('rim', rim); scene.collection.objects.link(r); r.location = (-2, 3, 2.5)
    r.rotation_euler = Vector((2, -3, -2)).to_track_quat('-Z', 'Y').to_euler()
    m = mat('floor', bg, rough=0.9)
    fl = cylinder('floor', (0, 0, -0.005), 6, 0.01, m, segs=64)
    return fl


def camera(scene, loc, target, lens=50, name='cam'):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.clip_start = 0.02; cd.clip_end = 400
    c = bpy.data.objects.new(name, cd); scene.collection.objects.link(c)
    c.location = Vector(loc)
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    scene.camera = c
    return c


def aim(c, loc, target):
    c.location = Vector(loc)
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
