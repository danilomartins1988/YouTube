"""Build each character procedurally, add reusable Actions, save assets/characters/<name>/<name>.blend.
Usage: blender -b -P build_assets.py -- clara|ayra|pandora|tifa"""
import bpy, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cp_lib import *; from cp_chars import *; from cp_motion import *
name = sys.argv[sys.argv.index('--') + 1]
clear_scene()
arm = build(name)
FPS = 30


def act(nm, n, fn):
    def f(fr):
        A = Acc(); t = (fr - 1) / FPS; u = (fr - 1) / max(1, n - 1)
        fn(A, t, u); face(arm, 'happy', A=A) if not nm.startswith('expr_') and nm != 'blink' else None
        A.apply(arm)
    save_action(arm, f'{name}_{nm}', f, (1, n))

act('idle_breath', 94, lambda A, t, u: breathe(A, arm, t, rate=FPS / 94 / (1 / 1)))
act('blink', 8, lambda A, t, u: face(arm, 'happy', blink=bump(u), A=A))
act('walk', 24, lambda A, t, u: walk(A, arm, u))
act('run', 16, lambda A, t, u: walk(A, arm, u, run=True, amp=1.2))
act('hop', 20, lambda A, t, u: hop(A, arm, u))
act('spin', 30, lambda A, t, u: A.rot('root', 0, 0, spin_angle(u)))
if IS_DOG(arm):
    act('tail_wag', 12, lambda A, t, u: tail_wag(A, arm, t, freq=FPS / 12))
    act('ear_flick', 12, lambda A, t, u: ear_flick(A, arm, u, 'L'))
    act('paw_lift_L', 24, lambda A, t, u: paw_lift(A, arm, u, 'L'))
    act('step_back', 24, lambda A, t, u: dog_step_back(A, arm, u))
    act('sit', 2, lambda A, t, u: sit(A, arm))
else:
    act('clap', 16, lambda A, t, u: clap(A, arm, u))
    act('step_forward_L', 24, lambda A, t, u: clara_step(A, arm, u, 'L'))
    act('step_back_R', 24, lambda A, t, u: clara_step(A, arm, u, 'R', back=True))
    act('wave', 30, lambda A, t, u: wave(A, arm, t))
    act('mouth_sing', 16, lambda A, t, u: face(arm, 'happy', mouth_open=bump(u * 2 % 1), A=A))
for e in ('happy', 'curious', 'surprised', 'focused', 'affectionate'):
    act(f'expr_{e}', 1, lambda A, t, u, e=e: face(arm, e, A=A))
reset_pose(arm); face(arm, 'happy')
arm['clara_e_as_patinhas'] = 'asset v1 - procedural (scripts/blender/cp_chars.py)'
out = os.path.join(ROOT, 'assets', 'characters', name, f'{name}.blend')
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
print('SAVED', out, len(bpy.data.actions), 'actions')
