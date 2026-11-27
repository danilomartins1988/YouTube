"""Episode 002 "Cadê? Achou!" - procedural animation synced to the REAL song timeline.

  blender -b rendering/ep002.blend -P episode2.py -- still FRAME OUT.png [eevee|cycles] [PCT]
  blender -b rendering/ep002.blend -P episode2.py -- render START END OUTDIR [eevee|cycles] [PCT]

Scene: rendering/ep002.blend (built by ep2_scene.py from the ep. 001 garden; props: giant flower, bucket, straw hat).
Timeline: music/compositions/cade_achou_timeline.json (scripts/ep2/build_timeline.py): Whisper words, beats,
ACHOU cues, bark cues, per-frame mouth opening + viseme class.
Upgrades over ep. 001: viseme mouth shapes (A/E/O/M), squash-and-stretch on hops, ears/tail lag (overlap),
blinks + brows per story beat, eased camera with focus pulls, hat prop hand-off, flower/bucket/hat reactions.
Rig names are internal: 'tifa' = the Yorkshire (Toby, male, from Aditivo 01)."""
import bpy, sys, os, math, json, bisect
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector, Euler, Matrix
from cp_lib import reset_pose
from cp_motion import Acc, ease, bump, breathe, tail_wag, ear_flick, blink_amount, walk, sway, clap, clap_pose, wave
from cp_chars import face
from cp_env import ground_h

ROOTP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TL = json.load(open(os.path.join(ROOTP, 'music', 'compositions', 'cade_achou_timeline.json'), encoding='utf-8'))
FPS = 24
BEATS = TL['beats_s']; BEAT = 60.0 / TL['bpm']; BPM = TL['bpm']
SEC = {k: tuple(v) for k, v in TL['sections'].items()}
ACH = TL['achou']; CUE = TL['cues']; BARKS = TL['barks']; MOUTH = TL['mouth']; VIS = TL['viseme']
END_T = TL['duration_s'] + 1.0
DOWN0 = TL['downbeat_beat_index']
SPOT = {'flower': (-1.05, 0.55), 'bucket': (0.05, 1.0), 'hat': (1.1, 0.5)}
DOGS = ('ayra', 'pandora', 'tifa')


def seg(t, a, b):
    return max(0.0, min(1.0, (t - a) / max(1e-6, b - a)))


def mix(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (mix(p[0], q[0], u), mix(p[1], q[1], u))


def heading_to(p, q):
    return math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1])))


def angmix(a, b, u):
    d = (b - a + 180) % 360 - 180
    return a + d * u


def gz(x, y):
    return max(ground_h(x, y), 0.0) if math.hypot(x, y) < 3 else ground_h(x, y)


def beatpos(t):
    i = bisect.bisect_right(BEATS, t) - 1
    if i < 0:
        return (t - BEATS[0]) / BEAT
    if i >= len(BEATS) - 1:
        return len(BEATS) - 1 + (t - BEATS[-1]) / BEAT
    return i + (t - BEATS[i]) / (BEATS[i + 1] - BEATS[i])


def beats_in(a, b, every=1, offset=0):
    return [x for k, x in enumerate(BEATS) if a <= x < b and (k - DOWN0 - offset) % every == 0]


# ======================================================================= blocking
C0 = (0.0, -0.55)
P1 = (-0.62, -0.05); P2 = (-0.05, 0.40); P3 = (0.62, 0.02); CF = (0.0, -0.25)
FINAL = {'clara': CF, 'ayra': (0.52, -0.12), 'pandora': (-0.52, -0.12), 'tifa': (0.34, -0.58)}
fx, fy = SPOT['flower']; bx, by = SPOT['bucket']; tx, ty = SPOT['hat']
A1, A2, A3, A4, A5 = ACH
S = SEC
# moves: (t0, t1, x, y). Start positions in START.
START = {'clara': C0, 'ayra': (fx + 0.06, fy + 0.32), 'pandora': (bx, by + 0.03), 'tifa': (tx, ty + 0.1)}
MOVES = {
    'clara': [(S['estrofe1'][0], S['estrofe1'][0] + 2.4, *P1), (S['estrofe2'][0], S['estrofe2'][0] + 2.4, *P2),
              (S['estrofe3'][0], S['estrofe3'][0] + 2.4, *P3), (S['ponte'][0], S['ponte'][0] + 2.2, *CF)],
    'ayra': [(CUE['orelhinha'] - 0.3, CUE['orelhinha'] + 0.2, fx + 0.19, fy + 0.30),
             (CUE['bandana_azul'] - 0.2, CUE['bandana_azul'] + 0.3, fx + 0.22, fy + 0.28),
             (A1, A1 + 0.7, fx + 0.52, fy - 0.2),
             (S['refrao_curto1'][0], S['refrao_curto1'][0] + 1.6, -0.25, -0.32),
             (S['estrofe2'][0] + 0.3, S['estrofe2'][0] + 2.6, -0.45, 0.32),
             (S['estrofe3'][0] + 0.3, S['estrofe3'][0] + 2.7, 0.18, -0.2),
             (S['ponte'][0] + 0.2, S['ponte'][0] + 2.2, *FINAL['ayra'])],
    'pandora': [(A2, A2 + 0.75, bx + 0.28, by - 0.42),
                (S['estrofe3'][0] + 0.4, S['estrofe3'][0] + 2.6, 0.36, 0.3),
                (S['ponte'][0] + 0.3, S['ponte'][0] + 2.3, *FINAL['pandora'])],
    'tifa': [(CUE['narizinho'] - 0.3, CUE['narizinho'] + 0.2, tx, ty + 0.025),
             (S['ponte'][0] + 0.4, S['ponte'][0] + 2.0, *FINAL['tifa'])],
}
# vertical baseline (hidden below ground / inside props): list of (t0, t1, dz) ramps, start value in DZ0
DZ0 = {'clara': 0.0, 'ayra': -0.10, 'pandora': -0.22, 'tifa': -0.22}
DZR = {'clara': [], 'ayra': [(CUE['orelhinha'] - 0.3, CUE['orelhinha'] + 0.2, -0.03), (A1, A1 + 0.7, 0.0)],
       'pandora': [(CUE['rabinho'] - 0.4, CUE['rabinho'] + 0.1, 0.06), (CUE['laco'] - 0.3, CUE['laco'] + 0.2, 0.10), (A2, A2 + 0.75, 0.0)],
       'tifa': [(CUE['bandana_verde'] - 0.3, CUE['bandana_verde'] + 0.2, -0.18), (A3, A3 + 0.35, 0.0)]}
# hops: (t0, dur, height)
HOPS = {n: [] for n in ('clara',) + DOGS}
HOPS['ayra'] += [(A1, 0.7, 0.24)]
HOPS['pandora'] += [(A2, 0.75, 0.30)]
HOPS['tifa'] += [(A3, 0.35, 0.10), (A3 + 0.9, 0.45, 0.07)]
for a in (A1, A2, A3):
    HOPS['clara'].append((a + 0.05, 0.42, 0.06))
for a in (A4, A5):
    HOPS['clara'].append((a + 0.02, 0.42, 0.07))
    for k, n in enumerate(DOGS):
        HOPS[n].append((a + 0.05 + 0.07 * k, 0.45, 0.09))
# short choruses + outro: dogs hop on alternate beats, Clara on downbeats in the outro
for (a, b) in (S['refrao_curto1'], S['refrao_curto2']):
    for k, n in enumerate(DOGS):
        for x in beats_in(a + 2.0, b - 0.4, 2, k % 2):
            if n == 'pandora' and b < A2: continue
            if n == 'tifa' and b < A3: continue
            HOPS[n].append((x - 0.05, 0.4, 0.045))
oa, ob = S['encerramento']
for k, n in enumerate(DOGS):
    for x in beats_in(oa, ob + 0.5, 2, k % 2):
        HOPS[n].append((x - 0.06, 0.42, 0.07))
for x in beats_in(oa, ob + 0.5, 4, 0):
    HOPS['clara'].append((x - 0.06, 0.45, 0.08))
for n in HOPS:
    HOPS[n].sort()


def move_state(name, t):
    """(x, y, moving_heading or None, distance travelled so far for the gait)."""
    p = START[name]; dist = 0.0
    for (a, b, x, y) in MOVES[name]:
        q = (x, y); L = math.hypot(q[0] - p[0], q[1] - p[1])
        if t < a:
            return p[0], p[1], None, dist
        if t < b:
            u = ease(seg(t, a, b))
            pos = lerp2(p, q, u)
            return pos[0], pos[1], (heading_to(p, q) if L > 0.15 else None), dist + L * u
        p = q; dist += L
    return p[0], p[1], None, dist


def dz_base(name, t):
    v = DZ0[name]
    for (a, b, z) in DZR[name]:
        if t < a:
            break
        v = mix(v, z, ease(seg(t, a, b)))
    return v


def hop_z(name, t):
    """Height above baseline from hops (parabolas) + stretch factor for squash-and-stretch."""
    z = 0.0; st = 1.0; air = 0.0
    for (a, d, h) in HOPS[name]:
        if a - 0.15 <= t <= a + d + 0.15:
            u = (t - a) / d
            if 0 <= u <= 1:
                z += 4 * h * u * (1 - u); air = 1.0
                st = 1.0 + 0.16 * min(1.0, h / 0.12) * (1 - 2 * u) * (1 if u < 0.5 else 0.6)
            elif u < 0:
                st = 1.0 - 0.12 * bump((u + 0.15 / d) / (0.15 / d)) * min(1.0, h / 0.08)  # anticipation squash
            else:
                st = 1.0 - 0.14 * bump((u - 1) / (0.15 / d)) * min(1.0, h / 0.08)  # landing squash
    return z, st, air


# look-at heading targets (when standing)
def look_heading(name, t, x, y):
    if name == 'clara':
        if t < S['estrofe1'][0]:
            return 0.0
        if t < S['refrao_curto1'][0]:
            return heading_to(P1, SPOT['flower']) if t < A1 + 0.3 else heading_to(P1, (fx + 0.52, fy - 0.2))
        if t < S['estrofe2'][0]:
            return 0.0
        if t < S['refrao_curto2'][0]:
            return heading_to(P2, SPOT['bucket']) if t < A2 + 0.3 else heading_to(P2, (bx + 0.28, by - 0.42))
        if t < S['estrofe3'][0]:
            return 0.0
        if t < S['ponte'][0]:
            return heading_to(P3, SPOT['hat'])
        return 0.0
    out = {'ayra': A1, 'pandora': A2, 'tifa': A3}[name]
    if t < out:
        return {'ayra': 15.0, 'pandora': 180.0, 'tifa': 0.0}[name]
    if t < out + 0.75:
        return angmix({'ayra': 15.0, 'pandora': 180.0, 'tifa': 0.0}[name], heading_to((x, y), CPOS(t)), ease(seg(t, out, out + 0.75)))
    if S['ponte'][0] + 2.3 < t < S['final'][0]:
        return heading_to((x, y), CF)  # look at the girl hiding
    if name == 'tifa' and A3 + 0.9 < t < A3 + 1.35:
        return 360 * ease(seg(t, A3 + 0.9, A3 + 1.35))  # happy spin
    if t < S['ponte'][0] + 2.3 and (S['refrao_curto1'][0] < t < S['estrofe2'][0] or S['refrao_curto2'][0] < t < S['estrofe3'][0]):
        return 0.0
    if t < S['ponte'][0]:
        return heading_to((x, y), CPOS(t))
    return 0.0


def CPOS(t):
    x, y, _, _ = move_state('clara', t)
    return (x, y)


HEAD_SMOOTH = 0.45


def heading(name, t):
    x, y, mh, _ = move_state(name, t)
    if mh is not None:
        return mh
    # smooth turn: average target heading over a short window (deterministic, no state)
    hs = [look_heading(name, t - HEAD_SMOOTH * k / 6, *move_state(name, t - HEAD_SMOOTH * k / 6)[:2]) for k in range(7)]
    base = hs[0]
    acc = sum(((h - base + 180) % 360 - 180) for h in hs) / len(hs)
    return base + acc


# ======================================================================= hat prop
def clara_world(t, local, lrot=(0, 0, 0)):
    x, y, _, _ = move_state('clara', t); h = math.radians(heading('clara', t))
    Rz = Matrix.Rotation(h, 4, 'Z')
    p = Vector((x, y, gz(x, y) + hop_z('clara', t)[0])) + (Rz @ Vector(local).to_4d()).to_3d()
    r = (Rz @ Euler([math.radians(v) for v in lrot]).to_matrix().to_4x4()).to_euler()
    return p, r


HAT_REST = None
HOLD = ((-0.25, -0.05, 0.38), (80, 0, -90)); FACE = ((0, -0.33, 0.80), (88, 0, 0)); HEAD = ((0, 0.02, 0.975), (-8, 10, 0))


def hat_state(t):
    loc0, rot0 = HAT_REST
    if t < A3:
        p = Vector(loc0); r = list(rot0)
        if S['estrofe3'][0] < t:  # wiggles while the little one moves underneath
            k = 0.4 + 0.6 * (t > CUE['narizinho']) + 0.6 * (t > CUE['bandana_verde'])
            r[0] += math.radians(2.0 * k * math.sin(2 * math.pi * 3.1 * t)); r[1] += math.radians(2.5 * k * math.sin(2 * math.pi * 2.3 * t + 1))
            p.z += 0.006 * k * abs(math.sin(2 * math.pi * 3.1 * t)) + 0.04 * seg(t, CUE['bandana_verde'] - 0.3, CUE['bandana_verde'] + 0.2)
        return p, Euler(r)
    if t < A3 + 0.4:  # rises on the little dog's head
        u = ease(seg(t, A3, A3 + 0.35)); p = Vector(loc0) + Vector((0, 0, 0.16 * u)); return p, Euler(rot0)
    def blend(t, a, b, s0, s1, arc=0.0):
        p0, r0 = s0; p1, r1 = s1; u = ease(seg(t, a, b))
        p = p0.lerp(p1, u) + Vector((0, 0, arc * 4 * u * (1 - u)))
        return p, r0.to_quaternion().slerp(r1.to_quaternion(), u).to_euler()
    rise = (Vector(loc0) + Vector((0, 0, 0.16)), Euler(rot0))
    if t < A3 + 1.2:
        return blend(t, A3 + 0.4, A3 + 1.2, rise, clara_world(t, *HOLD), arc=0.35)
    seq = [(CUE['tapou'], CUE['tapou'] + 0.7, HOLD, FACE), (A4, A4 + 0.45, FACE, HEAD),
           (CUE['tapa'], CUE['tapa'] + 0.7, HEAD, FACE), (A5, A5 + 0.45, FACE, HEAD)]
    cur = HOLD
    for (a, b, s0, s1) in seq:
        if t < a:
            return clara_world(t, *cur)
        if t < b:
            return blend(t, a, b, clara_world(t, *s0), clara_world(t, *s1), arc=0.08 if s1 is HEAD else 0.0)
        cur = s1
    return clara_world(t, *cur)


def hat_mode(t):
    """What Clara's arms are doing with the hat."""
    if t < A3 + 0.9:
        return None
    marks = [(A3 + 0.9, 'hold'), (CUE['tapou'], 'face'), (A4, 'joy'), (A4 + 1.6, None), (CUE['tapa'], 'face'), (A5, 'joy'), (A5 + 1.6, None)]
    m = None
    for (a, k) in marks:
        if t >= a:
            m = k
    return m


# ======================================================================= poses
def clara_pose(A, arm, t):
    expr = 'happy'
    sway(A, arm, beatpos(t) * BEAT, BPM, 0.55)
    x, y, mh, dist = move_state('clara', t)
    if mh is not None:
        walk(A, arm, dist / 0.42, amp=1.0)
    mode = hat_mode(t)
    srch = False
    if t < S['estrofe1'][0]:
        if t < CUE['vem'] - 4.3 or True:
            # looks left/right on each "cadê"
            for k, c in enumerate(CUE['cade_words']):
                if c - 0.15 < t < c + 0.9 and c < S['estrofe1'][0]:
                    A.rot('head', 0, 0, (28 if k % 2 else -28) * bump(seg(t, c - 0.15, c + 0.9)))
        if S['refrao'][0] < t < 14.4:
            srch = True; expr = 'curious'
        if CUE['vem'] - 0.2 < t < S['estrofe1'][0] - 0.3:
            wave(A, arm, t, 'R', ease(seg(t, CUE['vem'] - 0.2, CUE['vem'] + 0.3)) * (1 - seg(t, S['estrofe1'][0] - 0.9, S['estrofe1'][0] - 0.3)))
    for (vs, cue1, a) in ((S['estrofe1'], CUE['orelhinha'], A1), (S['estrofe2'], CUE['rabinho'], A2), (S['estrofe3'], CUE['narizinho'], A3)):
        if vs[0] + 2.4 < t < a:
            srch = True; expr = 'curious'
            if cue1 - 0.1 < t < cue1 + 2.2:  # "olha lá!" pointing
                k = bump(seg(t, cue1 - 0.1, cue1 + 2.2)) ** 0.5
                A.rot('upperarm_R', -78 * k, 0, 8 * k); A.rot('forearm_R', -10 * k, 0, 0)
            if a - 1.6 < t:  # suspense: lean in, brows up
                expr = 'surprised' if t > a - 0.7 else 'curious'
                A.rot('chest', 10 * seg(t, a - 1.6, a - 0.2), 0, 0)
        if a <= t < a + 1.4 and mode is None:
            k = bump(seg(t, a, a + 1.4)) ** 0.6
            A.rot('upperarm_L', -15 * k, -105 * k, 0); A.rot('upperarm_R', -15 * k, 105 * k, 0)
            A.rot('forearm_L', 0, -25 * k, 0); A.rot('forearm_R', 0, 25 * k, 0)
            expr = 'surprised' if t < a + 0.5 else 'happy'
    if srch and mode is None and not (t > S['estrofe1'][0] and any(c - 0.1 < t < c + 2.2 for c in (CUE['orelhinha'], CUE['rabinho'], CUE['narizinho']))):
        k = 0.8
        A.rot('chest', 10 * k, 0, 0); A.rot('head', 4 * k, 0, 0)
        for s, xx in (('L', 1), ('R', -1)):
            A.rot(f'upperarm_{s}', -25 * k, 0, -18 * xx * k); A.rot(f'forearm_{s}', -50 * k, 0, -20 * xx * k)
    # short choruses: clap on 2 and 4
    for (a, b) in (S['refrao_curto1'], S['refrao_curto2']):
        if a + 1.5 < t < b - 0.2 and mode is None:
            ph = ((beatpos(t) - DOWN0) % 2 - 0.75) / 0.5
            clap(A, arm, ph) if 0 <= ph <= 1 else clap_pose(A, arm, 1.0)
    # hat hand-off poses
    HOLDP = {'L': (-10, -25, 0, -20, 0, 0), 'R': (0, 0, 0, 0, 0, 0)}
    FACEP = {'L': (-88, 0, -22, -35, 0, -30), 'R': (-88, 0, 22, -35, 0, 30)}
    def arms(P, k=1.0, Q=None, u=0.0):
        for s_ in ('L', 'R'):
            v = P[s_] if Q is None else tuple(mix(a_, b_, u) for a_, b_ in zip(P[s_], Q[s_]))
            A.rot(f'upperarm_{s_}', v[0] * k, v[1] * k, v[2] * k); A.rot(f'forearm_{s_}', v[3] * k, v[4] * k, v[5] * k)
    if mode == 'hold':
        arms(HOLDP, ease(seg(t, A3 + 0.8, A3 + 1.25)))
    elif mode == 'face':
        t0 = CUE['tapou'] if t < A4 else CUE['tapa']
        k = ease(seg(t, t0, t0 + 0.7))
        arms(HOLDP if t < A4 else {'L': (0,) * 6, 'R': (0,) * 6}, 1.0, FACEP, k)
        A.rot('head', 6 * k, 0, 0); expr = 'happy'
    elif mode == 'joy':
        t0 = A4 if t < A4 + 2 else A5
        k = ease(seg(t, t0, t0 + 0.35)) * (1 - ease(seg(t, t0 + 1.2, t0 + 1.6)))
        for s, xx in (('L', 1), ('R', -1)):
            A.rot(f'upperarm_{s}', -15 * k, -105 * xx * k, 0); A.rot(f'forearm_{s}', 0, -25 * xx * k, 0)
        expr = 'surprised' if t < t0 + 0.45 else 'happy'
    # bridge: "E a menina? Cadê?" playful look around before hiding
    if S['ponte'][0] + 2.2 < t < CUE['tapou']:
        A.rot('head', 0, 8 * math.sin(2 * math.pi * 0.5 * t), 22 * math.sin(2 * math.pi * 0.42 * (t - S['ponte'][0])))
        expr = 'curious'
    # final verse: talks to the viewer, points at the camera on "você"
    if S['final'][0] < t < CUE['tapa']:
        expr = 'affectionate' if t < CUE['voce'] else 'happy'
        if CUE['voce'] - 0.2 < t < CUE['voce'] + 3.2:
            k = bump(seg(t, CUE['voce'] - 0.2, CUE['voce'] + 3.2)) ** 0.5
            A.rot('upperarm_R', -80 * k, 0, 18 * k); A.rot('forearm_R', -8 * k, 0, 0)
            A.rot('head', 0, 10 * k, 0)
    # outro: arms up on the hops
    if t > S['encerramento'][0] + 0.2:
        k = 0.5 + 0.5 * abs(math.sin(math.pi * beatpos(t) / 2))
        A.rot('upperarm_L', 0, -120 * k, 0); A.rot('upperarm_R', 0, 120 * k, 0)
    return expr


def dog_pose(A, arm, name, t):
    tail_wag(A, arm, t, freq={'ayra': 2.4, 'pandora': 2.8, 'tifa': 3.4}[name])
    out = {'ayra': A1, 'pandora': A2, 'tifa': A3}[name]
    expr = 'happy'
    x, y, mh, dist = move_state(name, t)
    if mh is not None and t > out + 0.75:
        walk(A, arm, dist / {'ayra': 0.3, 'pandora': 0.22, 'tifa': 0.2}[name], run=True)
    if t < out:
        expr = 'curious'
        if name == 'ayra':
            A.rot('head', -10, 0, -28); A.rot('neck', 0, 0, -15)
            c = CUE['orelhinha']
            if c < t < c + 2.5:
                ear_flick(A, arm, ((t - c) * 1.6) % 1.0, 'L', 30)
        elif name == 'pandora':
            A.rot('head', 30, 0, 0)
            if t > CUE['rabinho']:
                tail_wag(A, arm, t, freq=4.0, amp=30)
            if t > CUE['laco']:
                A.rot('head', -35 * seg(t, CUE['laco'] - 0.3, CUE['laco'] + 0.2), 0, 0)
        else:
            A.rot('head', -14, 0, 0)
            if t > CUE['narizinho'] - 0.3:  # sniff sniff
                A.rot('head', 5 * math.sin(2 * math.pi * 5 * t), 0, 0)
    elif t < out + 0.8:
        expr = 'surprised' if t < out + 0.4 else 'happy'
    # waiting on the girl to come out from behind the hat: curious head tilts
    if S['ponte'][0] + 2.3 < t < A4:
        expr = 'curious'; A.rot('head', 0, 14 * math.sin(2 * math.pi * 0.3 * t + len(name)), 0)
    if S['final'][0] < t < A5:
        sway(A, arm, beatpos(t) * BEAT, BPM, 0.6)
    if t > S['encerramento'][0]:
        sway(A, arm, beatpos(t) * BEAT, BPM, 0.8)
    return expr


def bark_open(name, t):
    v = 0.0
    for b in BARKS.get(name, []):
        if b - 0.05 < t < b + 0.3:
            v = max(v, 0.95 * bump(seg(t, b - 0.05, b + 0.3)) ** 0.6)
    return v


def clara_mouth(A, t):
    i = int(round(t * FPS))
    m = MOUTH[i] if 0 <= i < len(MOUTH) else 0.0
    if m < 0.06:
        return False
    v = VIS[i] if 0 <= i < len(VIS) else 'A'
    hide = 0.0001
    if v == 'M':
        A.scale('mouth_smile', (0.7, 1, 0.55)); A.scale('mouth_open', hide); A.scale('mouth_o', hide)
    elif v == 'O':
        A.scale('mouth_o', 0.75 + 0.7 * m); A.scale('mouth_open', hide); A.scale('mouth_smile', hide)
    elif v == 'E':
        A.scale('mouth_open', (1.12, 1.0, 0.3 + 0.5 * m)); A.scale('mouth_o', hide); A.scale('mouth_smile', hide)
    else:
        A.scale('mouth_open', (1.0, 1.0, 0.35 + 0.8 * m)); A.scale('mouth_o', hide); A.scale('mouth_smile', hide)
    return True


# ======================================================================= per frame
BASE_SCALE = {}
SEEDS = {'clara': 0.0, 'ayra': 0.7, 'pandora': 1.9, 'tifa': 2.6}


def update(scene, depsgraph=None):
    t = (scene.frame_current - 1) / FPS
    for name in ('clara',) + DOGS:
        arm = bpy.data.objects[name]; reset_pose(arm)
        A = Acc(); breathe(A, arm, t)
        dog = name != 'clara'
        expr = dog_pose(A, arm, name, t) if dog else clara_pose(A, arm, t)
        z, st, air = hop_z(name, t)
        if air and dog:
            A.rot('leg_FL', -25, 0, 0); A.rot('leg_FR', -25, 0, 0); A.rot('leg_BL', 25, 0, 0); A.rot('leg_BR', 25, 0, 0)
        elif air:
            A.rot('thigh_L', -18, 0, 0); A.rot('thigh_R', -18, 0, 0); A.rot('shin_L', 30, 0, 0); A.rot('shin_R', 30, 0, 0)
        # overlap: ears/tail lag behind vertical motion
        if dog:
            lag = (hop_z(name, t - 0.08)[0] + dz_base(name, t - 0.08)) - (z + dz_base(name, t))
            e = max(-40, min(40, 420 * lag))
            A.rot('ear_L', e, 0, 0); A.rot('ear_R', e, 0, 0); A.rot('tail', -0.8 * e, 0, 0)
        blink = 0.0 if expr == 'surprised' else blink_amount(t, 3.4 if not dog else 4.1, 0.15, seed=SEEDS[name])
        if dog:
            bo = bark_open(name, t)
            hidden = t < {'ayra': A1, 'pandora': A2, 'tifa': A3}[name]
            face(arm, expr, blink=blink, mouth_open=max(bo, 0.0 if hidden else 0.3), A=A)
        else:
            face(arm, expr, blink=blink, mouth_open=None, A=A)
            clara_mouth(A, t)
        A.apply(arm)
        x, y, _, _ = move_state(name, t)
        arm.location = (x, y, gz(x, y) + dz_base(name, t) + z)
        arm.rotation_euler = (0, 0, math.radians(heading(name, t)))
        s0 = BASE_SCALE[name]; sq = 1.0 / math.sqrt(st)
        arm.scale = (s0 * sq, s0 * sq, s0 * st)
    # props
    hat = bpy.data.objects['ep2_hat']; p, r = hat_state(t); hat.location = p; hat.rotation_euler = r
    fp = bpy.data.objects.get('ep2_flower_pivot')
    if fp:
        w = 0.0
        for (c, amp) in ((CUE['orelhinha'], 4), (CUE['bandana_azul'], 4), (A1, 14)):
            if c < t < c + 2.0:
                w += amp * math.exp(-3 * (t - c)) * math.sin(2 * math.pi * 3 * (t - c))
        fp.rotation_euler = (0, math.radians(w), 0)
    bp = bpy.data.objects.get('ep2_bucket_pivot')
    if bp:
        w = 0.0
        for (c, amp) in ((CUE['rabinho'], 2.5), (CUE['laco'], 2.5), (A2 + 0.2, 12)):
            if c < t < c + 2.0:
                w += amp * math.exp(-2.5 * (t - c)) * math.sin(2 * math.pi * 2.2 * (t - c))
        bp.rotation_euler = (math.radians(w), 0, 0)
    for k in range(5):
        b = bpy.data.objects.get(f'butterfly_{k}')
        if not b:
            continue
        cx, cy = (-2.2, 1.6) if k < 3 else (1.8, 1.2)
        b.location = (cx + 0.9 * math.sin(0.5 * t + k * 1.7), cy + 0.6 * math.sin(0.37 * t + k), 0.6 + 0.25 * math.sin(1.3 * t + k * 0.9))
        b.rotation_euler = (0, 0, 0.5 * t + k)
        for s in (1, -1):
            pv = bpy.data.objects.get(f'bf_wingpiv_{k}_{s}')
            if pv:
                pv.rotation_euler = (0, s * math.radians(55) * math.sin(2 * math.pi * 9 * t + k), 0)
    camera(scene, t)


# ======================================================================= camera
def cpos3(name, t, z=0.0):
    x, y, _, _ = move_state(name, t)
    return Vector((x, y, gz(x, y) + z))


def mid(t, names, z=0.35):
    v = Vector((0, 0, 0))
    for n in names:
        v += cpos3(n, t)
    v /= len(names); v.z += z
    return v


def push(a, b, prop, who='clara', z=0.42):
    """target that starts between the girl and the prop and ends on the prop (suspense push-in)."""
    P = Vector(prop)
    return lambda t: (cpos3(who, t, z) + P) / 2 if t < a else ((cpos3(who, t, z) + P) / 2).lerp(P, ease(seg(t, a, b)))


SHOTS = [  # (t0, t1, pos0, pos1, target_fn, focus_fn, lens0, lens1)
    (0.0, S['refrao'][0], (0.4, -5.6, 2.6), (0.3, -3.7, 1.15), lambda t: Vector((0, 0.45, 0.35)), lambda t: cpos3('clara', t, 0.5), 30, 32),
    (S['refrao'][0], 14.4, (0.0, -2.8, 0.8), (0.3, -2.5, 0.76), lambda t: cpos3('clara', t, 0.5), lambda t: cpos3('clara', t, 0.6), 32, 34),
    (14.4, S['estrofe1'][0], (1.15, -2.7, 0.98), (0.65, -2.85, 0.92), lambda t: Vector((-0.1, 0.25, 0.42)), lambda t: cpos3('clara', t, 0.6), 32, 32),
    (S['estrofe1'][0], A1, (-1.6, -1.6, 0.7), (-1.22, -0.38, 0.45), push(CUE['orelhinha'] - 1.0, A1 - 0.3, (fx + 0.08, fy, 0.3)),
     lambda t: Vector((fx + 0.1, fy, 0.3)), 30, 40),
    (A1, S['refrao_curto1'][0], (-2.05, -0.62, 0.72), (-1.95, -0.78, 0.72), lambda t: (mid(t, ('clara', 'ayra'), 0.3) * 2 + Vector((fx, fy, 0.3))) / 3, lambda t: cpos3('ayra', t, 0.25), 30, 30),
    (S['refrao_curto1'][0], S['estrofe2'][0], (-0.45, -2.6, 0.78), (-0.25, -2.7, 0.8), lambda t: mid(t, ('clara', 'ayra'), 0.33), lambda t: cpos3('clara', t, 0.6), 34, 34),
    (S['estrofe2'][0], A2, (1.3, -1.0, 0.7), (0.8, 0.0, 0.45), push(CUE['rabinho'] - 1.0, A2 - 0.3, (bx, by, 0.24)), lambda t: Vector((bx, by, 0.24)), 30, 40),
    (A2, S['refrao_curto2'][0], (1.15, -0.95, 0.72), (1.1, -1.05, 0.72), lambda t: mid(t, ('clara', 'pandora'), 0.28), lambda t: cpos3('pandora', t, 0.2), 30, 30),
    (S['refrao_curto2'][0], S['estrofe3'][0], (0.0, -2.8, 0.85), (0.15, -2.85, 0.86), lambda t: mid(t, ('clara', 'ayra', 'pandora'), 0.3), lambda t: cpos3('clara', t, 0.6), 34, 34),
    (S['estrofe3'][0], A3, (1.9, -1.3, 0.7), (1.62, -0.5, 0.42), push(CUE['narizinho'] - 1.0, A3 - 0.3, (tx, ty, 0.12)), lambda t: Vector((tx, ty - 0.1, 0.12)), 30, 40),
    (A3, S['ponte'][0], (2.45, 1.3, 0.62), (2.5, 1.38, 0.64), lambda t: mid(t, ('clara', 'tifa'), 0.4), lambda t: cpos3('clara', t, 0.6), 30, 30),
    (S['ponte'][0], S['final'][0], (0.0, -2.9, 0.85), (0.0, -2.5, 0.8), lambda t: Vector((0, -0.25, 0.48)), lambda t: cpos3('clara', t, 0.7), 34, 36),
    (S['final'][0], S['encerramento'][0], (0.0, -2.5, 0.74), (0.0, -2.3, 0.74), lambda t: Vector((0, -0.25, 0.58)), lambda t: cpos3('clara', t, 0.75), 36, 37),
    (S['encerramento'][0], END_T + 1, (0.0, -2.6, 0.82), (0.3, -4.8, 2.1), lambda t: Vector((0, 0.15, 0.4)), lambda t: cpos3('clara', t, 0.6), 34, 30),
]


def camera(scene, t):
    sh = next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1])
    u = ease(seg(t, sh[0], sh[1])) * 0.85 + seg(t, sh[0], sh[1]) * 0.15
    pos = Vector(sh[2]).lerp(Vector(sh[3]), u)
    tg = sum((sh[4](t - 0.25 * k) for k in range(5)), Vector((0, 0, 0))) / 5  # smoothed target
    cam = scene.camera; cam.location = pos
    cam.rotation_euler = (tg - pos).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = mix(sh[6], sh[7], u)
    f = bpy.data.objects.get('ep2_focus')
    if f:
        f.location = sum((sh[5](t - 0.2 * k) for k in range(4)), Vector((0, 0, 0))) / 4


# ======================================================================= setup
def pivot(name, objs, loc):
    e = bpy.data.objects.get(name)
    if e:
        return e
    e = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(e); e.location = loc
    bpy.context.view_layer.update()
    for o in objs:
        mw = o.matrix_world.copy(); o.parent = e; o.matrix_parent_inverse = e.matrix_world.inverted(); o.matrix_world = mw
    return e


def setup(engine='eevee', pct=100):
    global HAT_REST
    sc = bpy.context.scene
    from ep2_scene import level
    level('L1M', pct)
    for n in ('clara',) + DOGS:
        BASE_SCALE[n] = bpy.data.objects[n].scale[0]
    hat = bpy.data.objects['ep2_hat']; HAT_REST = (tuple(hat.location), tuple(hat.rotation_euler))
    pivot('ep2_flower_pivot', [o for o in bpy.data.objects if o.name.startswith(('gf_petal', 'gf_center'))], (fx, fy - 0.02, 0.30))
    pivot('ep2_bucket_pivot', [o for o in bpy.data.objects if o.name.startswith('ep2_bucket')], (bx, by - 0.2, 0.0))
    if os.environ.get('EP2_FAST'):  # layout checks on the local CPU
        e = sc.eevee; e.taa_render_samples = 1; e.use_motion_blur = False; e.use_soft_shadows = False; e.use_gtao = False
        e.use_ssr = False; e.use_bloom = False; sc.camera.data.dof.use_dof = False; sc.use_nodes = False
    sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = int(END_T * FPS)
    if engine == 'cycles':
        sc.render.engine = 'CYCLES'
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for dt in ('OPTIX', 'CUDA'):
            try:
                prefs.compute_device_type = dt; prefs.get_devices()
                if any(d.type == dt for d in prefs.devices):
                    for d in prefs.devices:
                        d.use = d.type == dt
                    break
            except Exception:
                pass
        c = sc.cycles; c.device = 'GPU'; c.samples = int(os.environ.get('EP2_SAMPLES', '96')); c.use_adaptive_sampling = True
        c.adaptive_threshold = 0.02; c.use_denoising = True
        try:
            c.denoiser = 'OPTIX'
        except Exception:
            pass
        c.max_bounces = 6; c.diffuse_bounces = 3; c.glossy_bounces = 2; c.transparent_max_bounces = 16
        c.caustics_reflective = False; c.caustics_refractive = False; c.blur_glossy = 1.0
        sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.5
        sc.render.use_persistent_data = True
    sc.render.image_settings.file_format = 'PNG'
    bpy.app.handlers.frame_change_pre.clear(); bpy.app.handlers.frame_change_pre.append(update)


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:]
    if args[0] == 'still':
        f, out = int(args[1]), args[2]
        setup(args[3] if len(args) > 3 else 'eevee', int(args[4]) if len(args) > 4 else 100)
        sc = bpy.context.scene; sc.frame_set(f); sc.render.filepath = out
        import time; t0 = time.time(); bpy.ops.render.render(write_still=True); print(f'RENDER_TIME {time.time() - t0:.1f}s')
    elif args[0] == 'stills':  # several frames, one load: stills ENGINE PCT OUTPREFIX F1 F2 ...
        setup(args[1], int(args[2])); sc = bpy.context.scene
        import time
        for f in args[4:]:
            t0 = time.time(); sc.frame_set(int(f)); sc.render.filepath = f'{args[3]}_{int(f):05d}.png'
            bpy.ops.render.render(write_still=True); print(f'RENDER_TIME f{f} {time.time() - t0:.1f}s', flush=True)
    elif args[0] == 'render':
        s0, s1, outdir = int(args[1]), int(args[2]), args[3]
        setup(args[4] if len(args) > 4 else 'eevee', int(args[5]) if len(args) > 5 else 100)
        sc = bpy.context.scene; os.makedirs(outdir, exist_ok=True)
        sc.frame_start = s0; sc.frame_end = s1
        sc.render.use_overwrite = False; sc.render.use_placeholder = False
        sc.render.filepath = os.path.join(outdir, 'f#####')
        bpy.ops.render.render(animation=True)
