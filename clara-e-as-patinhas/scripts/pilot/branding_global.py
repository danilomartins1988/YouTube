"""Global brand drafts (Aditivo 03): 'Clara & Paws' logo + YouTube banner (2560x1440, safe area 1546x423) + localized wordmarks.
Fredoka (SIL OFL). Drafts only - owner approval needed."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = f'{ROOT}/assets/branding/global'; os.makedirs(OUT, exist_ok=True)
F7 = f'{ROOT}/assets/branding/fonts/fredoka-latin-700-normal.woff'
YEL, BLUE, BROWN, PINK, GREEN, PURP, WHITE = '#FFC81A', '#5CB0F5', '#5C331A', '#FA8CB4', '#6CB848', '#8E5CC8', '#FFFFFF'

def font(sz): return ImageFont.truetype(F7, sz)

def paw(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 1.1], fill=col)
    for k, (dx, dy) in enumerate(((-0.95, -1.05), (-0.35, -1.55), (0.35, -1.55), (0.95, -1.05))):
        rr = r * 0.38; x, y = cx + dx * r, cy + dy * r
        d.ellipse([x - rr, y - rr * 1.15, x + rr, y + rr * 1.15], fill=col)

def outlined(d, xy, text, f, fill, stroke=BROWN, sw=10, anchor='mm'):
    d.text(xy, text, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)

def wordmark(w, h, l1, l2, l1col=YEL, l2col=BLUE, bg=None):
    im = Image.new('RGBA', (w, h), bg or (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    paw(d, int(h * 0.3), int(h * 0.58), int(h * 0.2), PINK)
    x0 = int(h * 0.62); avail = w - x0 - int(h * 0.08)
    def fit(text, sz):
        while sz > 10 and d.textlength(text, font=font(sz)) > avail: sz -= 2
        return font(sz)
    outlined(d, (x0, int(h * 0.38)), l1, fit(l1, int(h * 0.34)), l1col, sw=max(6, h // 40), anchor='lm')
    outlined(d, (x0, int(h * 0.74)), l2, fit(l2, int(h * 0.2)), l2col, sw=max(4, h // 60), anchor='lm')
    return im

# global logo + localized wordmarks
wordmark(1600, 600, 'Clara & Paws', 'Kids Songs').save(f'{OUT}/logo_global_clara_paws.png')
wordmark(1600, 600, 'Clara', 'e as Patinhas').save(f'{OUT}/wordmark_pt_clara_e_as_patinhas.png')
wordmark(1600, 600, 'Clara', 'y sus Patitas').save(f'{OUT}/wordmark_es_clara_y_sus_patitas.png')
# profile picture (800x800, works in a circle)
pp = Image.new('RGB', (800, 800), BLUE); d = ImageDraw.Draw(pp)
d.ellipse([60, 60, 740, 740], fill=YEL); paw(d, 400, 360, 110, WHITE)
outlined(d, (400, 600), 'Clara & Paws', font(88), WHITE, sw=8); pp.save(f'{OUT}/profile_800.png')
# banner 2560x1440, everything important inside the 1546x423 safe area (centre)
bn = Image.new('RGB', (2560, 1440), '#BFE4FB'); d = ImageDraw.Draw(bn)
for i in range(7):  # soft hills
    y = 980 + i * 40; d.ellipse([-400 + i * 420, y, 900 + i * 420, y + 900], fill=('#8DD36B' if i % 2 else '#78C45A'))
for k in range(26):  # paw trail
    paw(d, 160 + k * 92, 1260 - int(60 * math.sin(k / 2)), 18, '#FFFFFF')
lg = wordmark(1540, 420, 'Clara & Paws', 'Kids Songs  ·  Músicas Infantis  ·  Canciones Infantiles')
bn.paste(lg, (510, 510), lg)
bn.save(f'{OUT}/banner_2560x1440_draft.png')
print('ok', sorted(os.listdir(OUT)))
