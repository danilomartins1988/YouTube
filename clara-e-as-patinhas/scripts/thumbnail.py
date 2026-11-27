#!/usr/bin/env python3
"""Thumbnail 1280x720 "DANÇA DAS PATINHAS!" from the group render + logo (original assets only)."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = f'{ROOT}/assets/branding/fonts/fredoka-latin-700-normal.woff'
bg = Image.open(f'{ROOT}/assets/characters/grupo.png').convert('RGB')
# crop towards the characters and enlarge them
W, H = bg.size
bg = bg.crop((int(W * 0.04), int(H * 0.0), int(W * 0.96), int(W * 0.92 * 9 / 16))).resize((1280, 720), Image.LANCZOS)
bg = ImageEnhance.Color(bg).enhance(1.15)
im = bg.convert('RGBA')
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for k in range(170):  # bottom gradient for legibility
    d.line([(0, 719 - k), (1280, 719 - k)], fill=(255, 255, 255, int(120 * (1 - k / 170))))
im.alpha_composite(ov)
d = ImageDraw.Draw(im)
f = ImageFont.truetype(F, 118)
txt = 'DANÇA DAS PATINHAS!'
sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
ds.text((646, 652), txt, font=f, fill=(0, 0, 0, 140), anchor='mm', stroke_width=16, stroke_fill=(0, 0, 0, 140))
im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
d.text((640, 644), txt, font=f, fill=(255, 200, 26), anchor='mm', stroke_width=14, stroke_fill=(92, 51, 26))
# paw badges
def paw(cx, cy, s, fill):
    d.ellipse([cx - 0.55 * s, cy - 0.25 * s, cx + 0.55 * s, cy + 0.6 * s], fill=fill)
    for dx, dy in ((-0.62, -0.55), (-0.22, -0.88), (0.22, -0.88), (0.62, -0.55)):
        d.ellipse([cx + dx * s - 0.2 * s, cy + dy * s - 0.26 * s, cx + dx * s + 0.2 * s, cy + dy * s + 0.26 * s], fill=fill)
paw(1200, 80, 46, (250, 140, 180)); paw(1120, 120, 30, (92, 176, 245))
logo = Image.open(f'{ROOT}/assets/branding/logo_horizontal.png').convert('RGBA')
logo = logo.resize((430, int(430 * logo.height / logo.width)), Image.LANCZOS)
im.alpha_composite(logo, (24, 20))
os.makedirs(f'{ROOT}/thumbnails', exist_ok=True)
im.convert('RGB').save(f'{ROOT}/thumbnails/ep001_thumbnail.png')
print('thumbnail ok')
