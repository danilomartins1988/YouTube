"""Pilot thumbnails: 3 localized (PT main, EN, ES) + 1 universal without text. Source: a rendered frame of the universal animation."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = sys.argv[1]; OUT = f'{ROOT}/thumbnails/pilot'; os.makedirs(OUT, exist_ok=True)
F7 = f'{ROOT}/assets/branding/fonts/fredoka-latin-700-normal.woff'
im = Image.open(src).convert('RGB').crop((330, 110, 1610, 830)).resize((1280, 720), Image.LANCZOS)
im = ImageEnhance.Color(im).enhance(1.12); im = ImageEnhance.Contrast(im).enhance(1.05)
im.save(f'{OUT}/thumb_universal_notext.jpg', quality=90)
TXT = {'pt-BR': ('DANÇA DAS', 'PATINHAS!'), 'en-US': ('HAPPY PAW', 'DANCE!'), 'es-LATAM': ('¡BAILE DE', 'PATITAS!')}
for lg, (a, b) in TXT.items():
    t = im.copy(); d = ImageDraw.Draw(t)
    for txt, y, sz, col in ((a, 78, 84, '#FFFFFF'), (b, 172, 104, '#FFC81A')):
        f = ImageFont.truetype(F7, sz)
        d.text((1250, y), txt, font=f, fill=col, stroke_width=11, stroke_fill='#5C331A', anchor='rm')
    t.save(f'{OUT}/thumb_{lg}.jpg', quality=90)
print(sorted(os.listdir(OUT)))
