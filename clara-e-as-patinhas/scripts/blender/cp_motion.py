"""Procedural motion library (shared by the asset Actions and the episode animation).
Motions add rotations (degrees, armature axes) / offsets into an accumulator; apply() writes the pose."""
import math
from cp_lib import pose, reset_pose


def ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)


def bump(u):
    """0 -> 1 -> 0 over u in [0,1] (smooth)."""
    u = max(0.0, min(1.0, u))
    return math.sin(math.pi * u) ** 2


class Acc:
    def __init__(self):
        self.r = {}; self.l = {}; self.s = {}

    def rot(self, b, x=0, y=0, z=0):
        a = self.r.setdefault(b, [0, 0, 0]); a[0] += x; a[1] += y; a[2] += z

    def loc(self, b, x=0, y=0, z=0):
        a = self.l.setdefault(b, [0, 0, 0]); a[0] += x; a[1] += y; a[2] += z

    def scale(self, b, s):
        self.s[b] = s

    def apply(self, arm):
        names = arm.pose.bones.keys()
        for b in set(self.r) | set(self.l) | set(self.s):
            if b in names:
                pose(arm, b, rot=tuple(self.r.get(b, (0, 0, 0))), loc=tuple(self.l.get(b, (0, 0, 0))),
                     scale=self.s.get(b))


IS_DOG = lambda arm: 'tail' in arm.pose.bones


# ------------------------------------------------------------------ basic layers
def breathe(A, arm, t, rate=0.32):
    ph = math.sin(2 * math.pi * rate * t)
    if IS_DOG(arm):
        A.rot('body', ph * 1.2, 0, 0); A.rot('head', -ph * 1.0, 0, 0)
    else:
        A.rot('chest', ph * 1.6, 0, 0); A.rot('head', -ph * 1.0, 0, 0)
        A.rot('upperarm_L', 0, -ph * 1.5, 0); A.rot('upperarm_R', 0, ph * 1.5, 0)


def tail_wag(A, arm, t, freq=2.6, amp=28):
    if IS_DOG(arm):
        A.rot('tail', 0, 0, amp * math.sin(2 * math.pi * freq * t))
        A.rot('tail', 6 * math.sin(4 * math.pi * freq * t), 0, 0)


def ear_flick(A, arm, u, side='L', amp=22):
    """u in [0,1] over the flick duration."""
    if 'ear_L' in arm.pose.bones:
        k = bump(u) * amp * (1 if side == 'L' else -1)
        A.rot(f'ear_{side}', -abs(k) * 0.6, k, 0)


def blink_amount(t, period=3.7, dur=0.16, seed=0.0):
    """Natural-ish blinks: returns 0..1 closure."""
    ph = (t + seed) % period
    jitter = (math.sin((t + seed) // period * 12.9898) * 0.5 + 0.5) * 1.2
    ph2 = (t + seed + jitter) % period
    if ph2 < dur:
        return bump(ph2 / dur)
    return 0.0


# ------------------------------------------------------------------ locomotion
def walk(A, arm, phase, amp=1.0, run=False):
    """phase in cycles (float). Quadruped diagonal gait / biped walk."""
    s = math.sin(2 * math.pi * phase); c = math.cos(2 * math.pi * phase)
    if IS_DOG(arm):
        a = (34 if run else 24) * amp
        A.rot('leg_FL', a * s, 0, 0); A.rot('leg_BR', a * s, 0, 0)
        A.rot('leg_FR', -a * s, 0, 0); A.rot('leg_BL', -a * s, 0, 0)
        A.loc('root', 0, 0, abs(c) * (0.025 if run else 0.012) * amp)
        A.rot('body', (3 if run else 1.5) * math.sin(4 * math.pi * phase), 0, 0)
        A.rot('head', -2 * math.sin(4 * math.pi * phase), 0, 0)
    else:
        a = 26 * amp
        A.rot('thigh_L', -a * s, 0, 0); A.rot('thigh_R', a * s, 0, 0)
        A.rot('shin_L', max(0, -c) * 30 * amp, 0, 0); A.rot('shin_R', max(0, c) * 30 * amp, 0, 0)
        A.rot('upperarm_L', a * 0.8 * s, 0, 0); A.rot('upperarm_R', -a * 0.8 * s, 0, 0)
        A.rot('forearm_L', -12, 0, 0); A.rot('forearm_R', -12, 0, 0)
        A.loc('root', 0, 0, abs(math.sin(4 * math.pi * phase)) * 0.012 * amp)
        A.rot('chest', 0, 0, 4 * s * amp)


def hop(A, arm, u, height=0.12):
    """Single hop, u in [0,1]: crouch, jump (parabola), land."""
    u = max(0.0, min(1.0, u))
    if u < 0.2:
        k = bump(u / 0.4); z = -0.015 * k
    elif u < 0.85:
        v = (u - 0.2) / 0.65; z = 4 * height * v * (1 - v); k = 0
    else:
        k = bump((u - 0.85) / 0.3); z = -0.012 * k
    A.loc('root', 0, 0, z)
    air = 1.0 if 0.2 <= u < 0.85 else 0.0
    if IS_DOG(arm):
        A.rot('leg_FL', -25 * air, 0, 0); A.rot('leg_FR', -25 * air, 0, 0)
        A.rot('leg_BL', 25 * air, 0, 0); A.rot('leg_BR', 25 * air, 0, 0)
        A.rot('body', -8 * air, 0, 0)
    else:
        A.rot('thigh_L', -20 * (air + k), 0, 0); A.rot('thigh_R', -20 * (air + k), 0, 0)
        A.rot('shin_L', 35 * (air + k), 0, 0); A.rot('shin_R', 35 * (air + k), 0, 0)
        A.rot('upperarm_L', 0, -50 * air, 0); A.rot('upperarm_R', 0, 50 * air, 0)


def spin_angle(u):
    return 360.0 * ease(u)


# ------------------------------------------------------------------ dance
def paw_lift(A, arm, u, side='L'):
    """Dog lifts a front paw forward (Patinha pra frente)."""
    k = bump(u)
    A.rot(f'leg_F{side}', -55 * k, 0, 0)
    A.loc(f'leg_F{side}', 0, 0, 0.0)
    A.rot('body', -6 * k, 0, 0)
    A.rot('head', 4 * k, 0, 0)


def dog_step_back(A, arm, u):
    k = bump(u)
    A.loc('root', 0, 0.035 * k, 0)
    A.rot('leg_FL', 14 * k, 0, 0); A.rot('leg_FR', 14 * k, 0, 0)
    A.rot('body', 4 * k, 0, 0)


def clara_step(A, arm, u, side='L', back=False):
    k = bump(u)
    sgn = 1 if back else -1
    A.rot(f'thigh_{side}', sgn * 28 * k, 0, 0)
    if back:
        A.rot(f'shin_{side}', 22 * k, 0, 0)
    else:
        A.rot(f'foot_{side}', -12 * k, 0, 0)
    A.loc('root', 0, -sgn * 0.0 * k, -0.01 * k)
    A.rot('chest', -sgn * 4 * k, 0, 0)
    A.rot('upperarm_L', 0, -18 * k, 0); A.rot('upperarm_R', 0, 18 * k, 0)


def clap(A, arm, u):
    """Clara claps; u in [0,1] one clap (hands meet at u=0.5)."""
    k = bump(u)
    base = 1.0
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -62 * base, 0, -(14 + 10 * k) * x)
        A.rot(f'forearm_{s}', -38 * base, 0, -(26 + 22 * k) * x)


def clap_pose(A, arm, k=1.0):
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -62 * k, 0, -14 * x * k)
        A.rot(f'forearm_{s}', -38 * k, 0, -26 * x * k)


def wave(A, arm, t, side='R', k=1.0):
    x = 1 if side == 'L' else -1
    A.rot(f'upperarm_{side}', -20 * k, -150 * x * k, 0)
    A.rot(f'forearm_{side}', 0, -15 * x * k + 25 * x * k * math.sin(2 * math.pi * 2.2 * t), 0)


def arms_up(A, arm, k=1.0):
    A.rot('upperarm_L', 0, -150 * k, 0); A.rot('upperarm_R', 0, 150 * k, 0)
    A.rot('forearm_L', 0, -10 * k, 0); A.rot('forearm_R', 0, 10 * k, 0)


def hug_pose(A, arm, k=1.0):
    for s, x in (('L', 1), ('R', -1)):
        A.rot(f'upperarm_{s}', -70 * k, 0, -10 * x * k)
        A.rot(f'forearm_{s}', -10 * k, 0, -55 * x * k)
    A.rot('chest', 10 * k, 0, 0); A.rot('head', 8 * k, 0, 0)


def sway(A, arm, t, bpm=115, amp=1.0):
    """Groove on the beat: bounce + side sway."""
    b = t * bpm / 60.0
    if IS_DOG(arm):
        A.loc('root', 0, 0, 0.008 * amp * abs(math.sin(math.pi * b)))
        A.rot('body', 0, 4 * amp * math.sin(math.pi * b), 0)
        A.rot('head', 0, 6 * amp * math.sin(math.pi * b + 0.6), 0)
    else:
        A.loc('root', 0, 0, -0.012 * amp * abs(math.sin(math.pi * b)))
        A.rot('hips', 0, 3 * amp * math.sin(math.pi * b), 0)
        A.rot('chest', 0, -4 * amp * math.sin(math.pi * b), 0)
        A.rot('head', 0, 5 * amp * math.sin(math.pi * b + 0.5), 0)
        A.rot('shin_L', 8 * amp * abs(math.sin(math.pi * b)), 0, 0); A.rot('shin_R', 8 * amp * abs(math.sin(math.pi * b)), 0, 0)
        A.rot('thigh_L', -5 * amp * abs(math.sin(math.pi * b)), 0, 0); A.rot('thigh_R', -5 * amp * abs(math.sin(math.pi * b)), 0, 0)


def sit(A, arm, k=1.0):
    if IS_DOG(arm):
        A.rot('body', 28 * k, 0, 0); A.loc('root', 0, 0.02 * k, -0.035 * k)
        A.rot('leg_BL', -55 * k, 0, 0); A.rot('leg_BR', -55 * k, 0, 0)
        A.rot('leg_FL', -28 * k, 0, 0); A.rot('leg_FR', -28 * k, 0, 0)
        A.rot('head', -20 * k, 0, 0)
