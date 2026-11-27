#!/usr/bin/env python3
"""Resumable episode renderer. Each call works for at most --budget seconds (default 540):
renders missing frames of the next incomplete 240-frame segment (blender, frame-skip resumable),
then encodes every complete segment to rendering/segs/seg_KKK.mp4 (720p H.264 crf 16) and deletes its PNGs.
Segments are always the fixed ranges [k*240+1, (k+1)*240] (last one ends at --end).
Usage: python3 scripts/render_driver.py [--budget 540] [--from-seg K] [--to-seg K]"""
import argparse, glob, os, subprocess, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLEND = f'{ROOT}/rendering/ep001.blend'; EP = f'{ROOT}/scripts/blender/episode.py'
FR = f'{ROOT}/rendering/frames'; SEGS = f'{ROOT}/rendering/segs'; SEG = 240; FPS = 24
ap = argparse.ArgumentParser(); ap.add_argument('--budget', type=float, default=540)
ap.add_argument('--end', type=int, default=4016)
ap.add_argument('--from-seg', type=int, default=0); ap.add_argument('--to-seg', type=int, default=999)
a = ap.parse_args(); T0 = time.time()
os.makedirs(FR, exist_ok=True); os.makedirs(SEGS, exist_ok=True)
NSEG = (a.end + SEG - 1) // SEG
KS = [k for k in range(NSEG) if a.from_seg <= k <= a.to_seg]


def seg_range(k):
    return k * SEG + 1, min((k + 1) * SEG, a.end)


def encode_done():
    for k in KS:
        s0, s1 = seg_range(k)
        out = f'{SEGS}/seg_{k:03d}.mp4'
        if os.path.exists(out):
            continue
        need = [f'{FR}/f{f:05d}.png' for f in range(s0, s1 + 1)]
        if all(os.path.exists(p) and os.path.getsize(p) > 10000 for p in need):
            r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-start_number', str(s0),
                                '-i', f'{FR}/f%05d.png', '-frames:v', str(s1 - s0 + 1), '-c:v', 'libx264', '-preset', 'medium',
                                '-crf', '16', '-pix_fmt', 'yuv420p', out + '.tmp.mp4'])
            if r.returncode == 0:
                os.rename(out + '.tmp.mp4', out)
                for p in need:
                    os.remove(p)
                print('ENCODED', out, flush=True)


encode_done()
for k in KS:
    s0, s1 = seg_range(k)
    if os.path.exists(f'{SEGS}/seg_{k:03d}.mp4'):
        continue
    left = a.budget - (time.time() - T0)
    if left < 60:
        break
    for p in glob.glob(f'{FR}/f*.png'):  # drop possibly truncated frames
        if os.path.getsize(p) < 10000:
            os.remove(p)
    t1 = time.time()
    try:
        subprocess.run(['blender', '-b', BLEND, '-P', EP, '--', 'render', str(s0), str(s1), FR], timeout=left - 25,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        pass
    encode_done()
done = sum(os.path.exists(f'{SEGS}/seg_{k:03d}.mp4') for k in range(NSEG))
pending = len(glob.glob(f'{FR}/f*.png'))
print(f'STATUS segments {done}/{NSEG}, loose frames {pending}, elapsed {time.time() - T0:.0f}s', flush=True)
