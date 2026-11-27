#!/usr/bin/env python3
"""Ep. 002 thumbnail 1280x720: one protagonist (the girl, ACHOU pose), clean blurred garden, two words."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = f'{ROOT}/assets/branding/fonts/fredoka-latin-700-normal.woff'
plate = sys.argv[1] if len(sys.argv) > 1 else f'{ROOT}/assets/branding/ep002_thumb_plate.png'
im = Image.open(plate).convert('RGB')
base = im.resize((1280, 720), Image.LANCZOS)
SH = 270  # move the girl to the right; fill the left with a soft blurred, mirrored garden
bg = base.transpose(Image.FLIP_LEFT_RIGHT).filter(ImageFilter.GaussianBlur(18))
canvas = bg.copy(); canvas.paste(base.crop((0, 0, 1280 - SH, 720)), (SH, 0))
mask = Image.linear_gradient('L').rotate(90).resize((120, 720))  # soft seam
canvas.paste(bg.crop((SH - 10, 0, SH + 110, 720)), (SH - 10, 0), mask.transpose(Image.FLIP_LEFT_RIGHT))
im = ImageEnhance.Color(canvas).enhance(1.1).convert('RGBA')
d = ImageDraw.Draw(im)
def title(txt, y, size, fill):
    f = ImageFont.truetype(F, size)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((260, y + 8), txt, font=f, fill=(0, 0, 0, 120), anchor='mm', stroke_width=18, stroke_fill=(0, 0, 0, 120))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text((260, y), txt, font=f, fill=fill, anchor='mm', stroke_width=14, stroke_fill=(92, 51, 26))
title('CADÊ?', 250, 118, (92, 176, 245))
title('ACHOU!', 420, 118, (255, 200, 26))
os.makedirs(f'{ROOT}/thumbnails', exist_ok=True)
out = f'{ROOT}/thumbnails/ep002_cade_achou_thumbnail.png'
im.convert('RGB').save(out); print(out)
