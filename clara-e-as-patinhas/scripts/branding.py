#!/usr/bin/env python3
"""Logos for "Clara e as Patinhas" (original, drawn with PIL + Fredoka OFL font).
Outputs to assets/branding/: logo_color.png, logo_transparent.png, logo_horizontal.png, logo_compact.png,
youtube_icon.png (800x800), paleta.png. Optional: --face PATH (a rendered Clara close-up) for the icon."""
import os, sys, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = f'{ROOT}/assets/branding'
F7 = f'{B}/fonts/fredoka-latin-700-normal.woff'; F6 = f'{B}/fonts/fredoka-latin-600-normal.woff'
COL = {'sun': (255, 200, 26), 'sky': (92, 176, 245), 'sky_l': (205, 232, 252), 'green': (108, 184, 72), 'pink': (250, 140, 180),
       'white': (255, 255, 255), 'wood': (178, 117, 66), 'terracotta': (214, 107, 66), 'brown': (92, 51, 26), 'navy': (40, 70, 130)}


def font(sz, w=7):
    return ImageFont.truetype(F7 if w == 7 else F6, sz)


def paw(d, cx, cy, s, fill):
    d.ellipse([cx - 0.55 * s, cy - 0.25 * s, cx + 0.55 * s, cy + 0.6 * s], fill=fill)
    for dx, dy in ((-0.62, -0.55), (-0.22, -0.88), (0.22, -0.88), (0.62, -0.55)):
        d.ellipse([cx + dx * s - 0.2 * s, cy + dy * s - 0.26 * s, cx + dx * s + 0.2 * s, cy + dy * s + 0.26 * s], fill=fill)


def text_stroke(d, xy, txt, f, fill, stroke, sw, anchor='la'):
    d.text(xy, txt, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)


def wordmark(scale=1.0, slogan=True):
    """Stacked wordmark on transparent canvas."""
    W, H = int(1400 * scale), int(760 * scale if slogan else 640 * scale)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f1 = font(int(300 * scale)); f2 = font(int(150 * scale)); f3 = font(int(64 * scale), 6)
    # soft shadow layer
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((W // 2 + int(8 * scale), int(250 * scale)), 'Clara', font=f1, fill=(0, 0, 0, 70), anchor='mm', stroke_width=int(22 * scale), stroke_fill=(0, 0, 0, 70))
    ds.text((W // 2 + int(8 * scale), int(500 * scale)), 'e as Patinhas', font=f2, fill=(0, 0, 0, 70), anchor='mm', stroke_width=int(16 * scale), stroke_fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(10 * scale)); im.alpha_composite(sh)
    text_stroke(d, (W // 2, int(240 * scale)), 'Clara', f1, COL['sun'], COL['brown'], int(18 * scale), 'mm')
    text_stroke(d, (W // 2, int(490 * scale)), 'e as Patinhas', f2, COL['sky'], COL['white'], int(14 * scale), 'mm')
    # paws dancing over the "i" area / around
    for (x, y, s, c, a) in ((0.12, 0.13, 46, 'pink', 0), (0.88, 0.16, 40, 'sky', 0), (0.92, 0.62, 34, 'pink', 0), (0.07, 0.6, 30, 'sun', 0)):
        paw(d, x * W, y * H, s * scale, COL[c])
    if slogan:
        text_stroke(d, (W // 2, int(660 * scale)), 'Pequenas patinhas, grandes aventuras!', f3, COL['navy'], COL['white'], int(6 * scale), 'mm')
    return im


def main():
    os.makedirs(B, exist_ok=True)
    wm = wordmark(1.0)
    wm.save(f'{B}/logo_transparent.png')
    # colour version on a sky badge
    W, H = 1600, 1000
    bg = Image.new('RGBA', (W, H), COL['sky_l'] + (255,)); d = ImageDraw.Draw(bg)
    d.rounded_rectangle([40, 40, W - 40, H - 40], radius=120, fill=COL['white'] + (255,), outline=COL['sun'], width=24)
    for k in range(9):
        x = 140 + k * 165; paw(d, x, H - 110 - (k % 2) * 26, 22, COL['pink'] if k % 2 else COL['green'])
    bg.alpha_composite(wm, ((W - wm.width) // 2, 70))
    bg.convert('RGB').save(f'{B}/logo_color.png')
    # horizontal: paw badge + one-line name
    W, H = 2000, 420
    hz = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(hz)
    d.ellipse([20, 20, 380, 380], fill=COL['sun'], outline=COL['brown'], width=12); paw(d, 200, 230, 95, COL['white'])
    f1 = font(170); f2 = font(110)
    text_stroke(d, (430, 200), 'Clara', f1, COL['sun'], COL['brown'], 12, 'lm')
    wclara = d.textlength('Clara', font=f1)
    text_stroke(d, (430 + wclara + 40, 214), 'e as Patinhas', f2, COL['sky'], COL['navy'], 8, 'lm')
    hz = hz.crop(hz.getbbox()); hz.save(f'{B}/logo_horizontal.png')
    # compact (square-ish): badge + small stacked name
    W, H = 900, 900
    cp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(cp)
    d.ellipse([60, 60, W - 60, H - 60], fill=COL['sky'], outline=COL['white'], width=24)
    paw(d, W / 2, 330, 110, COL['white'])
    text_stroke(d, (W / 2, 560), 'Clara', font(190), COL['sun'], COL['brown'], 12, 'mm')
    text_stroke(d, (W / 2, 700), 'e as Patinhas', font(92), COL['white'], COL['navy'], 8, 'mm')
    cp.save(f'{B}/logo_compact.png')
    # YouTube icon 800x800 (works when cropped to a circle)
    face = sys.argv[sys.argv.index('--face') + 1] if '--face' in sys.argv else None
    ic = Image.new('RGBA', (800, 800), COL['sun'] + (255,)); d = ImageDraw.Draw(ic)
    d.ellipse([30, 30, 770, 770], fill=COL['sky'])
    if face and os.path.exists(face):
        fim = Image.open(face).convert('RGBA'); s = min(fim.size); fim = fim.crop(((fim.width - s) // 2, 0, (fim.width + s) // 2, s)).resize((600, 600))
        mask = Image.new('L', (600, 600), 0); ImageDraw.Draw(mask).ellipse([0, 0, 600, 600], fill=255)
        ic.paste(fim, (100, 40), mask)
        d = ImageDraw.Draw(ic)
        d.rounded_rectangle([90, 560, 710, 720], radius=80, fill=COL['white'], outline=COL['brown'], width=8)
        text_stroke(d, (400, 640), 'Clara', font(120), COL['sun'], COL['brown'], 10, 'mm')
    else:
        paw(d, 400, 330, 150, COL['white'])
        text_stroke(d, (400, 600), 'Clara', font(170), COL['sun'], COL['brown'], 12, 'mm')
    for (x, y) in ((140, 170), (660, 170)):
        paw(d, x, y, 34, COL['pink'])
    ic.convert('RGB').save(f'{B}/youtube_icon.png')
    # palette
    pal = [('Amarelo-sol', '#FFC81A'), ('Azul-céu', '#5CB0F5'), ('Verde natural', '#6CB848'), ('Rosa suave', '#FA8CB4'),
           ('Branco', '#FFFFFF'), ('Madeira quente', '#B27542'), ('Terracota', '#D66B42'), ('Castanho (contorno)', '#5C331A')]
    W = 1600; pim = Image.new('RGB', (W, 420), 'white'); d = ImageDraw.Draw(pim)
    d.text((40, 30), 'Paleta Clara e as Patinhas', font=font(56), fill=COL['brown'])
    for i, (n, h) in enumerate(pal):
        x = 40 + i * 192; c = tuple(int(h[k:k + 2], 16) for k in (1, 3, 5))
        d.rounded_rectangle([x, 120, x + 172, 300], radius=28, fill=c, outline=(200, 200, 200), width=3)
        d.text((x + 86, 330), n, font=font(24, 6), fill=(60, 60, 60), anchor='mm'); d.text((x + 86, 368), h, font=font(24, 6), fill=(110, 110, 110), anchor='mm')
    pim.save(f'{B}/paleta.png')
    print('logos ok')


if __name__ == '__main__':
    main()
