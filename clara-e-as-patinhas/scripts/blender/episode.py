"""Episode 001 - A Dança das Patinhas: scene build + procedural choreography synced to the music timeline.

  blender -b -P episode.py -- build                   -> rendering/ep001.blend
  blender -b rendering/ep001.blend -P episode.py -- render START END [OUTDIR]   (frames, resumable: skips existing PNGs)
  blender -b rendering/ep001.blend -P episode.py -- still FRAME OUT.png

Timeline source: music/compositions/timeline_final.json if it exists (real song), else estrutura.json (guide).
All motion is evaluated per frame in a frame_change_pre handler (no baked keys)."""
import bpy, sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mathutils import Vector, Euler
from cp_lib import *
from cp_motion import *
from cp_chars import face

ROOTP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FPS = 24
TL_PATH = os.path.join(ROOTP, 'music', 'compositions', 'timeline_final.json')
if not os.path.exists(TL_PATH):
    TL_PATH = os.path.join(ROOTP, 'music', 'compositions', 'estrutura.json')
TL = json.load(open(TL_PATH, encoding='utf-8'))
BPM = TL['bpm']; BEAT = 60.0 / BPM; BAR = 4 * BEAT
SEC = {s['nome']: (s['inicio_s'], s['fim_s']) for s in TL['secoes']}
END_T = TL.get('duracao_com_cauda_s', TL['duracao_musical_s'] + 1.5) + 1.0
NOTES = []  # (t0, t1, syllable)
for s in TL['secoes']:
    for ln in s['linhas']:
        for n in ln.get('notas', []):
            if 'silaba' in n:
                NOTES.append((n['inicio_beat'] * BEAT, (n['inicio_beat'] + n['dur']) * BEAT, n['silaba'], s['nome']))
NOTES.sort()
AU = [(a, b) for a, b, syl, _ in NOTES if syl.upper() == 'AU']


def line_times(sec):
    for s in TL['secoes']:
        if s['nome'] == sec:
            return [l.get('inicio_s', s['inicio_s']) for l in s['linhas']]
    return []


HOME = {'clara': (0.0, 0.0), 'pandora': (-0.58, 0.02), 'ayra': (0.6, 0.04), 'tifa': (1.02, 0.14)}
DOGHOUSE = {'ayra': (3.0, 5.0), 'pandora': (4.4, 5.0), 'tifa': (5.8, 5.0)}
MEADOW = {'clara': (-4.0, -1.0), 'pandora': (-3.45, -1.15), 'ayra': (-4.75, -0.7), 'tifa': (-4.95, -1.15)}
POND_X, POND_Y = 5.2, -1.2
BR_L = 2.6 * 2.0 / 2.0 * 1.25
BRIDGE = {'clara': (5.2, -1.2), 'ayra': (4.62, -1.15), 'pandora': (5.75, -1.15), 'tifa': (4.15, -1.12)}
STRIDE = {'clara': 0.42, 'ayra': 0.3, 'pandora': 0.22, 'tifa': 0.2}


def bridge_z(x, y):
    u = (x - POND_X) / (BR_L / 2)
    if abs(u) <= 1.0 and abs(y - POND_Y) < 0.5:
        return 0.42 * (1 - u * u) + 0.06 + 0.025
    return None


def gz(x, y):
    from cp_env import ground_h
    b = bridge_z(x, y)
    return b if b is not None else max(ground_h(x, y), 0.0 if math.hypot(x, y) < 3 else -1)


def mix(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (mix(p[0], q[0], u), mix(p[1], q[1], u))


def seg(t, t0, t1):
    return max(0.0, min(1.0, (t - t0) / max(1e-6, t1 - t0)))


# ======================================================================= build
def build():
    from cp_chars import build as build_char
    from cp_env import build_env
    from cp_render import eevee
    clear_scene(); sc = bpy.context.scene
    bfs = build_env(sc)
    for n in ('clara', 'ayra', 'pandora', 'tifa'):
        build_char(n)
    cd = bpy.data.cameras.new('CAM'); cd.lens = 35; cd.clip_start = 0.03; cd.clip_end = 300
    cam = bpy.data.objects.new('CAM', cd); sc.collection.objects.link(cam); sc.camera = cam
    eevee(sc, (1280, 720), 8, fps=FPS)
    sc.eevee.use_soft_shadows = True; sc.eevee.shadow_cube_size = '512'; sc.eevee.shadow_cascade_size = '2048'
    sc.frame_start = 1; sc.frame_end = int(END_T * FPS)
    sun = bpy.data.objects['sun']
    sun.data.shadow_cascade_max_distance = 30; sun.data.shadow_cascade_count = 4
    out = os.path.join(ROOTP, 'rendering', 'ep001.blend')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=out, compress=True)
    print('SAVED', out, 'frames', sc.frame_end)


# ======================================================================= camera shots
SHOTS = []  # (t0, t1, pos0, pos1, tgt0, tgt1, lens0, lens1)


def shot(t0, t1, p0, p1, g0, g1, l0=35, l1=None):
    SHOTS.append((t0, t1, p0, p1, g0, g1, l0, l1 or l0))


def plan_cameras():
    S = SEC
    a, b = S['assinatura']; shot(a, b, (2.5, -16, 4.0), (1.8, -12.5, 3.0), (-0.5, 4, 1.2), (-0.8, 4, 1.0), 26)
    a, b = S['intro_instrumental']; shot(a, b, (-0.6, -6.0, 1.6), (-0.8, -4.4, 1.2), (-1.6, 2.0, 0.6), (-0.8, 0.6, 0.6), 30)
    L = line_times('intro') + [S['intro'][1]]
    shot(L[0], L[1], (0.0, -2.2, 0.85), (0.1, -1.9, 0.8), (0.0, 0, 0.72), (0.0, 0, 0.72), 40)
    shot(L[1], L[2], (-1.6, -4.2, 1.5), (-0.5, -4.6, 1.4), (2.0, 2.4, 0.3), (1.0, 0.6, 0.3), 28)
    shot(L[2], L[3], (0.0, -1.7, 0.42), (0.9, -1.6, 0.38), (0.1, 0.0, 0.25), (0.95, 0.1, 0.22), 35)
    shot(L[3], L[4], (0.3, -3.3, 0.9), (0.3, -3.0, 0.8), (0.3, 0, 0.42), (0.3, 0, 0.42), 35)
    # chorus 1 + break
    a, b = S['refrao_1']; m = a + 4 * BAR
    shot(a, m, (0.25, -3.0, 0.62), (0.25, -2.6, 0.6), (0.25, 0, 0.38), (0.25, 0, 0.38), 35)
    shot(m, b, (-2.2, -2.2, 0.9), (2.0, -2.5, 0.8), (0.2, 0, 0.35), (0.2, 0, 0.35), 32)
    a, b = S['pausa_danca_1']; shot(a, b, (1.4, -1.5, 0.28), (-0.6, -1.7, 0.3), (0.3, 0.1, 0.25), (0.2, 0.1, 0.25), 28)
    # Ayra verse (tracking) + chorus 2 + break
    a, b = S['verso_ayra']; shot(a, b, (0.0, -3.6, 1.0), (0.0, -3.6, 1.0), 'ayra', 'ayra', 30)
    a, b = S['refrao_2_curto']; shot(a, b, (2.4, -2.4, 0.7), (-2.0, -2.6, 0.75), (0.25, 0, 0.38), (0.25, 0, 0.38), 32)
    a, b = S['pausa_danca_2']; shot(a, b, (0.3, -2.0, 0.25), (0.3, -1.7, 0.3), (0.3, 0.1, 0.22), (0.3, 0.1, 0.25), 26)
    # Pandora meadow
    a, b = S['verso_pandora']; L = line_times('verso_pandora') + [b]
    shot(L[0], L[1], (-3.3, -2.15, 0.32), (-3.15, -1.95, 0.3), (-3.45, -1.15, 0.22), (-3.45, -1.15, 0.2), 45)
    shot(L[1], L[3], (-2.4, -3.6, 0.8), (-5.6, -3.4, 0.9), (-3.8, -1.1, 0.35), (-3.8, -1.1, 0.35), 30)
    shot(L[3], L[4], (-3.75, -2.9, 0.75), (-3.75, -2.5, 0.65), (-3.75, -1.1, 0.45), (-3.75, -1.1, 0.45), 35)
    # Tifa (low, funny)
    a, b = S['verso_tifa']; L = line_times('verso_tifa') + [b]
    shot(L[0], L[2], (0.6, -2.6, 0.32), (1.4, -2.4, 0.3), 'tifa', 'tifa', 30)
    shot(L[2], L[3], (1.0, -1.2, 0.16), (1.0, -1.1, 0.16), (1.02, 0.14, 0.18), (1.02, 0.14, 0.2), 32)
    shot(L[3], L[4], (0.4, -2.8, 0.55), (0.4, -2.4, 0.5), (0.45, 0.05, 0.3), (0.45, 0.05, 0.3), 30)
    # Bridge reveal (crane up)
    a, b = S['ponte']; m = a + 4 * BAR
    shot(a, m, (2.6, -4.2, 0.25), (3.0, -6.2, 1.6), (4.3, -1.2, 0.45), (5.0, -1.2, 0.5), 28)
    shot(m, b, (5.2, -4.4, 0.95), (5.2, -3.8, 0.9), (5.0, -1.2, 0.6), (5.0, -1.2, 0.62), 30)
    # final chorus: big orbit
    a, b = S['refrao_final']; m = a + 6 * BAR
    shot(a, m, (0.3, -3.6, 1.5), (0.3, -2.8, 0.7), (0.25, 0, 0.35), (0.25, 0, 0.38), 32)
    shot(m, b, (-2.6, -1.8, 0.8), (2.6, -1.9, 1.1), (0.25, 0, 0.35), (0.25, 0, 0.4), 30)
    # ending
    a, b = S['final']; shot(a, b, (0.1, -2.0, 0.6), (0.1, -1.7, 0.55), (0.1, 0, 0.4), (0.1, 0, 0.42), 38)
    a = S['assinatura_final'][0]
    shot(a, END_T + 1, (0.2, -2.4, 0.7), (0.4, -7.5, 2.6), (0.15, 0, 0.45), (0.0, 2.0, 0.8), 34)


# ======================================================================= choreography
def chorus_moves(A, name, arm, tc, final=False):
    """Chorus choreography on lyric cues. tc = time since chorus start. Returns extra heading (deg)."""
    bar = int(tc // BAR); u = (tc % BAR) / BAR; bb = (tc % BAR) / BEAT  # beat inside bar
    dog = name != 'clara'
    head = 0.0
    if final and bar >= 6:  # 2-bar lines: "Com os amigos..." / "Dançando juntos..."
        k = bar - 6; v = ((tc - 6 * BAR) % (2 * BAR)) / (2 * BAR)
        if k < 2:
            sway(A, arm, tc, BPM, 1.6)
            if not dog:
                arms_up(A, arm, 0.55 + 0.25 * math.sin(math.pi * tc / BEAT))
        else:
            if k == 2:
                head = spin_angle(min(1, v * 2))
            sway(A, arm, tc, BPM, 1.2)
            if not dog:
                arms_up(A, arm, bump(min(1, v * 1.2)))
            else:
                hop(A, arm, (v * 2) % 1.0, 0.05)
        return head
    line = bar % 8
    if line == 0:  # Patinha pra frente
        if dog:
            paw_lift(A, arm, u, 'L')
        else:
            clara_step(A, arm, u, 'L')
    elif line == 1:  # pra trás
        if dog:
            dog_step_back(A, arm, u)
        else:
            clara_step(A, arm, u, 'R', back=True)
    elif line == 2:  # Dá uma voltinha
        head = spin_angle(min(1, u * 1.15))
        sway(A, arm, tc, BPM, 0.6)
    elif line == 3:  # E dança muito mais
        sway(A, arm, tc, BPM, 1.5)
        if not dog:
            arms_up(A, arm, bump(u))
    elif line in (4, 5):  # Au au au...
        if dog:
            if bb < 1.5:
                hop(A, arm, (bb % 0.5) / 0.5, 0.045)
            else:
                sway(A, arm, tc, BPM, 1.0)
        else:
            if bb < 1.5:
                clap(A, arm, ((bb + 0.25) % 0.5) / 0.5)
            else:
                sway(A, arm, tc, BPM, 1.0)
    elif line == 6:  # Bate palma, bate o pé
        if dog:
            paw_lift(A, arm, (bb % 2) / 2, 'L' if bb < 2 else 'R')
        else:
            # hands meet exactly on beats 1 and 3 (= claps of the track)
            ph = ((bb - 0.75) % 2.0) / 0.5
            clap(A, arm, ph if ph <= 1 else 1.0) if ph <= 1 else clap_pose(A, arm, 1.0)
            if 2.4 < bb < 3.1:
                A.rot('thigh_R', -22 * bump((bb - 2.4) / 0.7), 0, 0)
    else:  # Dança junto como quiser
        sway(A, arm, tc, BPM, 1.8)
        if not dog:
            A.rot('upperarm_L', 0, -60 * abs(math.sin(math.pi * tc / BEAT)), 0)
            A.rot('upperarm_R', 0, 60 * abs(math.sin(math.pi * tc / (BEAT))), 0)
    return head


def break_moves(A, name, arm, tb):
    bb = tb / BEAT
    if name == 'clara':
        ph = ((bb % 2) - 0.75) / 0.5
        clap(A, arm, ph) if 0 <= ph <= 1 else clap_pose(A, arm, 1.0)
        sway(A, arm, tb, BPM, 1.0)
    else:
        off = {'ayra': 0.0, 'pandora': 0.5, 'tifa': 1.0}[name]
        hop(A, arm, ((bb + off) % 2) / 2, 0.06)
    return 0.0


def mouth_open_at(t, who='clara'):
    """Envelope from vocal note timings (melody guide or Whisper-aligned real vocal)."""
    best = 0.0
    for a, b, syl, sec in NOTES:
        if a - 0.1 > t:
            break
        if b + 0.08 < t:
            continue
        isau = syl.upper() == 'AU'
        if who != 'clara' and not isau:
            continue
        att = seg(t, a - 0.03, a + 0.06)
        rel = 1 - seg(t, b - 0.08, b + 0.02)
        v = att * rel * (0.95 if isau or len(syl) > 2 else 0.75)
        best = max(best, v)
    return best


def place(arm, x, y, heading, dz=0.0, name=None):
    arm.location = (x, y, gz(x, y) + dz)
    arm.rotation_euler = (0, 0, math.radians(heading))


def heading_to(p, q):
    return math.degrees(math.atan2(q[0] - p[0], -(q[1] - p[1])))


def travel(A, name, arm, t, t0, t1, p0, p1, run=False):
    """Move along a straight line with easing + gait. Returns (pos, heading)."""
    u = seg(t, t0, t1); e = ease(u)
    pos = lerp2(p0, p1, e)
    dist = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) * e
    if 0 < u < 1:
        walk(A, arm, dist / (STRIDE[name] * (1.4 if run else 1.0)), amp=min(1, 4 * min(u, 1 - u) + 0.3), run=run)
    return pos, heading_to(p0, p1)


def choreo(name, arm, t):
    A = Acc(); dog = name != 'clara'
    breathe(A, arm, t)
    if dog:
        tail_wag(A, arm, t, freq={'ayra': 2.4, 'pandora': 2.8, 'tifa': 3.3}[name])
        ph = (t * 0.23 + {'ayra': 0.1, 'pandora': 0.5, 'tifa': 0.8}[name]) % 1.0
        if ph < 0.12:
            ear_flick(A, arm, ph / 0.12, 'L' if int(t) % 2 else 'R')
    expr = 'happy'; heading = 0.0; dz = 0.0
    x, y = HOME[name]
    S = SEC
    if t < S['intro'][0] + 2 * BAR + 0 * BAR:  # before "Vieram correndo"
        if dog:
            x, y = DOGHOUSE[name]; sit(A, arm, 1.0); heading = 0
        else:
            if t < S['intro'][0]:
                (x, y), heading = travel(A, name, arm, t, S['intro_instrumental'][0] - 1.0, S['intro'][0] - 0.2, (-2.2, 2.3), (0.0, 0.0))
                if t < S['intro_instrumental'][0] - 1.0:
                    x, y = -2.2, 2.3
            else:
                heading = 25 * bump(seg(t, S['intro'][0], S['intro'][0] + 2 * BAR))
                wave(A, arm, t, 'R', bump(seg(t, S['intro'][0] + 0.2, S['intro'][0] + 2 * BAR - 0.1)))
    elif t < S['refrao_1'][0]:
        L = line_times('intro')
        if dog:
            delay = {'ayra': 0.0, 'pandora': 0.35, 'tifa': 0.7}[name]
            (x, y), heading = travel(A, name, arm, t, L[1] + delay, L[2] + delay * 0.5 - 0.15, DOGHOUSE[name], HOME[name], run=True)
            if t > L[2] + delay * 0.5 - 0.15:
                heading = 0
                # named: little hop when the name is sung
                nt = {'ayra': L[2], 'pandora': L[2] + 1.0 * BEAT, 'tifa': L[2] + 2.5 * BEAT}[name]
                if nt - 0.05 < t < nt + 0.5:
                    hop(A, arm, (t - nt + 0.05) / 0.55, 0.08); expr = 'happy'
            if t > L[3]:
                sway(A, arm, t, BPM, 1.0)
        else:
            heading = mix(25, 0, seg(t, L[1], L[1] + 0.6))
            if t < L[2]:
                wave(A, arm, t, 'R', 1 - seg(t, L[2] - 0.4, L[2]))
            elif t < L[3]:
                A.rot('head', 0, 0, -10)  # looks at the dogs
                expr = 'happy'
            else:
                wave(A, arm, t, 'R', 0.9); wave(A, arm, t + 0.2, 'L', 0.9); sway(A, arm, t, BPM, 0.8)
    elif t < S['pausa_danca_1'][0]:
        heading = chorus_moves(A, name, arm, t - S['refrao_1'][0])
    elif t < S['verso_ayra'][0]:
        heading = break_moves(A, name, arm, t - S['pausa_danca_1'][0])
    elif t < S['refrao_2_curto'][0]:
        L = line_times('verso_ayra') + [S['refrao_2_curto'][0]]
        if name == 'ayra':
            if t < L[1] + 0.2:  # runs a circle around Clara
                u = seg(t, L[0], L[1] + 0.2); ang = 2 * math.pi * ease(u)
                c0 = Vector((0.0, 0.0)); r = 1.0
                start_ang = math.atan2(HOME['ayra'][1], HOME['ayra'][0])
                a_ = start_ang - ang
                x = c0.x + math.cos(a_) * (0.6 + 0.5 * math.sin(math.pi * u)); y = c0.y + math.sin(a_) * (0.6 + 0.5 * math.sin(math.pi * u)) - 0.3 * math.sin(math.pi * u)
                walk(A, arm, u * 2 * math.pi * 0.9 / STRIDE['ayra'] / 1.4, run=True, amp=min(1, 6 * min(u, 1 - u) + 0.2))
                heading = math.degrees(a_)
            elif t < L[2]:  # wags and looks at camera ("olha pra mim")
                x, y = 0.25, -0.9; heading = 0
                u = seg(t, L[1] + 0.2, L[1] + 0.8); x, y = lerp2((0.6, -0.3), (0.25, -0.9), ease(u))
                tail_wag(A, arm, t, 4.0, 40); expr = 'curious' if t > L[1] + 4 * BEAT else 'happy'
            elif t < L[3]:  # pula pra cá, pula pra lá
                bb = (t - L[2]) / BEAT
                side = [-0.35, 0.0, 0.35, 0.0][min(3, int(bb // 2))]
                prev = [0.0, -0.35, 0.0, 0.35][min(3, int(bb // 2))]
                v = (bb % 2) / 2
                x = 0.25 + mix(prev, side, ease(min(1, v * 1.6))); y = -0.9
                hop(A, arm, min(1, v * 1.6), 0.12)
            else:  # spins back home
                u = seg(t, L[3], L[4] - 0.3)
                x, y = lerp2((0.25, -0.9), HOME['ayra'], ease(u))
                heading = spin_angle(min(1, u * 1.6)) if u < 0.62 else 0
                if 0 < u < 1:
                    walk(A, arm, u * 4, amp=0.6)
        else:
            sway(A, arm, t, BPM, 0.7)
            if name == 'clara':
                bb = (t - S['verso_ayra'][0]) / BEAT
                ph = ((bb % 2) - 0.75) / 0.5
                clap(A, arm, ph) if 0 <= ph <= 1 else clap_pose(A, arm, 1.0)
                A.rot('head', 0, 0, -12 * math.sin(0.8 * t))
    elif t < S['pausa_danca_2'][0]:
        heading = chorus_moves(A, name, arm, t - S['refrao_2_curto'][0])
    elif t < S['verso_pandora'][0]:
        heading = break_moves(A, name, arm, t - S['pausa_danca_2'][0])
    elif t < S['verso_tifa'][0]:  # meadow
        L = line_times('verso_pandora') + [S['verso_tifa'][0]]
        x, y = MEADOW[name]
        if name == 'pandora':
            if t < L[1]:
                expr = 'affectionate'; sway(A, arm, t, BPM, 0.8); heading = -15
            elif t < L[2]:
                u = seg(t, L[1], L[1] + 2 * BEAT); heading = spin_angle(u) - 15
                if t > L[1] + 2 * BEAT:
                    sit(A, arm, 1.0); paw_lift(A, arm, 0.5, 'L'); paw_lift(A, arm, 0.5, 'R'); expr = 'happy'
            elif t < L[3]:
                bb = (t - L[2]) / BEAT
                if bb < 4:
                    paw_lift(A, arm, (bb % 1.0), 'L' if int(bb) % 2 == 0 else 'R')
                else:
                    heading = spin_angle(min(1, (bb - 4) / 3.0)) * 2
            else:
                u = seg(t, L[3], L[3] + 1.0)
                x, y = lerp2(MEADOW['pandora'], (-3.65, -1.35), ease(u))
                heading = spin_angle(seg(t, L[3] + 4 * BEAT, L[3] + 7 * BEAT)); sway(A, arm, t, BPM, 1.0)
        elif name == 'clara':
            heading = 25; sway(A, arm, t, BPM, 0.6)
            if t > L[3]:
                heading = mix(25, 0, seg(t, L[3], L[3] + 0.5)) + spin_angle(seg(t, L[3] + 4 * BEAT, L[3] + 7 * BEAT))
                arms_up(A, arm, 0.5 * bump(seg(t, L[3], L[4])))
            elif t > L[1]:
                ph = ((((t - L[1]) / BEAT) % 2) - 0.75) / 0.5
                clap(A, arm, ph) if 0 <= ph <= 1 else clap_pose(A, arm, 0.8)
        else:
            sit(A, arm, 1.0); heading = 30
    elif t < S['ponte'][0]:  # Tifa on the lawn
        L = line_times('verso_tifa') + [S['ponte'][0]]
        if name == 'tifa':
            if t < L[1]:  # zoomies
                u = seg(t, L[0], L[1]); ang = 2 * math.pi * 2 * ease(u)
                cx, cy = 1.25, -0.25
                x = cx + 0.32 * math.cos(ang) - 0.23 * 0; y = cy + 0.32 * math.sin(ang)
                x = mix(HOME['tifa'][0], x, min(1, u * 6)); y = mix(HOME['tifa'][1], y, min(1, u * 6))
                if u > 0.9:
                    x, y = lerp2((x, y), HOME['tifa'], (u - 0.9) / 0.1)
                walk(A, arm, u * 2 * 2 * math.pi * 0.32 / STRIDE['tifa'] / 1.4, run=True, amp=1.2)
                heading = math.degrees(ang) + 180
            elif t < L[2]:  # hop + spin, everyone laughs
                u = seg(t, L[1], L[1] + 2 * BEAT)
                hop(A, arm, u, 0.12); heading = spin_angle(u)
                if t > L[1] + 2 * BEAT:
                    sway(A, arm, t, BPM, 1.4)
            elif t < L[3]:  # "Dá um pulinho: um, dois, três" -> 3 hops on the counted syllables
                hops = [a for a, b, syl, sec in NOTES if sec == 'verso_tifa' and syl.upper() in ('UM', 'DOIS', 'TRÊS') and a >= L[2]]
                for h0 in hops:
                    if h0 - 0.12 < t < h0 + 0.33:
                        hop(A, arm, (t - h0 + 0.12) / 0.45, 0.1 + 0.03 * hops.index(h0))
                expr = 'focused' if t < (hops[0] if hops else L[2]) else 'happy'
            else:  # tries a big spin, gets dizzy and plops down (funny)
                u = seg(t, L[3], L[3] + 3 * BEAT)
                heading = spin_angle(u) * 2
                if t > L[3] + 3 * BEAT:
                    sit(A, arm, 1.0); A.rot('head', 0, 18 * math.sin(2 * math.pi * 1.5 * t), 14 * math.sin(2 * math.pi * 0.75 * t))
                    expr = 'surprised' if t < L[3] + 5 * BEAT else 'happy'
        else:
            sway(A, arm, t, BPM, 0.6)
            if name == 'clara':
                expr = 'surprised' if L[3] + 3 * BEAT < t < L[3] + 5 * BEAT else 'happy'
                A.rot('head', 0, 0, -18)
                if L[1] < t < L[2]:
                    A.rot('chest', 6 * abs(math.sin(2 * math.pi * 3 * t)), 0, 0)  # giggle
            if name in ('ayra', 'pandora') and L[1] < t < L[2]:
                hop(A, arm, ((t - L[1]) / BEAT) % 1.0, 0.03)
    elif t < S['refrao_final'][0]:  # bridge
        L = line_times('ponte') + [S['refrao_final'][0]]
        order = {'tifa': 0, 'ayra': 1, 'clara': 2, 'pandora': 3}[name]
        start = (2.4 - order * 0.25, -1.2 + (order - 1.5) * 0.04)
        t0 = L[0] + order * 0.55; t1 = L[1] + 2 * BEAT + order * 0.2
        if t < t1:
            (x, y), heading = travel(A, name, arm, t, t0, t1, start, BRIDGE[name], run=False)
            if t < t0:
                x, y = start; heading = -90
        else:
            x, y = BRIDGE[name]; heading = 0
            if t < L[2]:
                if name != 'clara':
                    hop(A, arm, ((t - t1) / BEAT) % 1.0, 0.05)
                else:
                    ph = ((((t - L[1]) / BEAT) % 2) - 0.75) / 0.5
                    clap(A, arm, ph) if 0 <= ph <= 1 else clap_pose(A, arm, 1.0)
            elif t < L[3]:
                bb = (t - L[2]) / BEAT
                if bb < 2:
                    heading = spin_angle(bb / 2)
                else:
                    hop(A, arm, min(1, (bb - 2) / 2), 0.1)
            else:
                sway(A, arm, t, BPM, 1.0)
                if name == 'clara':
                    arms_up(A, arm, bump(seg(t, L[3], L[4])) * 0.9)
    elif t < S['final'][0]:
        heading = chorus_moves(A, name, arm, t - S['refrao_final'][0], final=True)
    else:  # ending: hug, wave, logo
        L = line_times('final') + [S['assinatura_final'][0]]
        hugpos = {'clara': (0.0, 0.0), 'ayra': (0.38, -0.3), 'pandora': (-0.36, -0.3), 'tifa': (0.06, -0.42)}
        if dog:
            (x, y), heading = travel(A, name, arm, t, L[0], L[0] + 1.6, HOME[name], hugpos[name])
            if t > L[0] + 1.6:
                heading = {'ayra': 200, 'pandora': 160, 'tifa': 180}[name] if t < S['assinatura_final'][0] else 0
                if t > S['assinatura_final'][0]:
                    sway(A, arm, t, BPM, 0.8)
                else:
                    expr = 'affectionate'
        else:
            k = bump(seg(t, L[1] - 0.3, S['assinatura_final'][0] + 0.2))
            if L[1] - 0.3 < t < S['assinatura_final'][0]:
                hug_pose(A, arm, min(1, 2.2 * k)); expr = 'affectionate'
                A.rot('thigh_L', -25 * min(1, 2 * k), 0, 0); A.rot('thigh_R', -25 * min(1, 2 * k), 0, 0)
                A.rot('shin_L', 40 * min(1, 2 * k), 0, 0); A.rot('shin_R', 40 * min(1, 2 * k), 0, 0)
                A.loc('root', 0, 0, -0.05 * min(1, 2 * k))
            elif t >= S['assinatura_final'][0]:
                wave(A, arm, t, 'R', 1.0)
    # mouths
    mo = mouth_open_at(t, name)
    if dog:
        face(arm, expr, blink=blink_amount(t, 4.1, 0.14, seed={'ayra': 0.7, 'pandora': 1.9, 'tifa': 2.6}[name]),
             mouth_open=max(mo, 0.35 if expr == 'happy' else 0.0), A=A)
    else:
        face(arm, expr, blink=blink_amount(t, 3.4, 0.15), mouth_open=mo if mo > 0.05 else (None if expr != 'happy' else 0.0), A=A)
    return x, y, heading, dz, A


def update(scene, depsgraph=None):
    t = (scene.frame_current - 1) / FPS
    for name in ('clara', 'ayra', 'pandora', 'tifa'):
        arm = bpy.data.objects[name]
        reset_pose(arm)
        x, y, heading, dz, A = choreo(name, arm, t)
        A.apply(arm)
        # root loc from Acc is in bone space of 'root' (pose), placement here
        place(arm, x, y, heading, dz, name)
    # butterflies: lissajous paths around the meadow / lawn, flapping
    for k in range(5):
        b = bpy.data.objects.get(f'butterfly_{k}')
        if not b:
            continue
        cx, cy = (-4.0, -1.2) if k < 3 else (1.5, 0.8)
        b.location = (cx + 1.1 * math.sin(0.5 * t + k * 1.7), cy + 0.7 * math.sin(0.37 * t + k), 0.55 + 0.25 * math.sin(1.3 * t + k * 0.9))
        b.rotation_euler = (0, 0, 0.5 * t + k)
        for s in (1, -1):
            p = bpy.data.objects.get(f'bf_wingpiv_{k}_{s}')
            if p:
                p.rotation_euler = (0, s * math.radians(55) * math.sin(2 * math.pi * 9 * t + k), 0)
    # camera
    cam = scene.camera
    sh = None
    for s in SHOTS:
        if s[0] <= t < s[1]:
            sh = s; break
    if sh is None:
        sh = SHOTS[-1]
    u = ease(seg(t, sh[0], sh[1])) * 0.85 + seg(t, sh[0], sh[1]) * 0.15
    pos = Vector(sh[2]).lerp(Vector(sh[3]), u)

    def tgt(g):
        if isinstance(g, str):
            o = bpy.data.objects[g]; return o.location + Vector((0, 0, 0.18))
        return Vector(g)
    target = tgt(sh[4]).lerp(tgt(sh[5]), u)
    if isinstance(sh[4], str):
        pos = target + Vector((0.0, -2.4, 0.35)) + Vector(sh[2]) * 0.0
        if sh[4] == 'tifa':
            pos = target + Vector((0.25, -1.7, 0.12))
    cam.location = pos
    cam.rotation_euler = (target - pos).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = mix(sh[6], sh[7], u)


plan_cameras()


def register():
    bpy.app.handlers.frame_change_pre.clear()
    bpy.app.handlers.frame_change_pre.append(update)


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    if args and args[0] == 'build':
        build()
    elif args and args[0] == 'stills':
        register(); sc = bpy.context.scene
        pre = args[1]
        for tt in args[2:]:
            f = int(round(float(tt) * FPS)) + 1
            sc.frame_set(f); sc.render.filepath = f'{pre}_{float(tt):06.2f}.png'
            bpy.ops.render.render(write_still=True)
    elif args and args[0] in ('render', 'still'):
        register()
        sc = bpy.context.scene
        if args[0] == 'still':
            sc.frame_set(int(args[1])); sc.render.filepath = args[2]
            bpy.ops.render.render(write_still=True)
        else:
            s0, s1 = int(args[1]), int(args[2])
            outdir = args[3] if len(args) > 3 else os.path.join(ROOTP, 'rendering', 'frames')
            os.makedirs(outdir, exist_ok=True)
            import time
            for f in range(s0, s1 + 1):
                p = os.path.join(outdir, f'f{f:05d}.png')
                if os.path.exists(p):
                    continue
                t0 = time.time()
                sc.frame_set(f); sc.render.filepath = p
                bpy.ops.render.render(write_still=True)
                print(f'FRAME {f} {time.time() - t0:.2f}s', flush=True)
