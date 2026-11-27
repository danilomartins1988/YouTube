#!/usr/bin/env python3
"""Compose model sheets from rendering/sheets_raw into assets/characters/<name>/sheet_*.png and the group image."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = f'{ROOT}/rendering/sheets_raw'
F = f'{ROOT}/assets/branding/fonts/fredoka-latin-700-normal.woff'
F6 = f'{ROOT}/assets/branding/fonts/fredoka-latin-600-normal.woff'
INFO = {
    'clara': ('Clara', '~4 anos · altura de referência 1,00 m',
              [('Pele', '#FCD6BA'), ('Cabelo', '#5C331A'), ('Olhos', '#6B3D1A'), ('Macacão', '#FFC71A'), ('Camiseta', '#F7F7F2'), ('Tênis', '#FA6B9E'), ('Detalhe tênis', '#59B3FA'), ('Bochechas', '#FA9499')],
              'Cabelo castanho liso e brilhante na altura dos ombros, franja lateral, presilha de florzinha amarela; macacão amarelo (identidade), camiseta branca, tênis rosa/azul.'),
    'ayra': ('Ayra', 'Border Collie Red Merle · ~0,36 m (altura do joelho da Clara)',
             [('Base', '#B5622F'), ('Manchas merle', '#6B3518'), ('Bege', '#E3C49B'), ('Branco', '#F7F3EC'), ('Olhos azul-claros', '#73BFF2'), ('Bandana', '#2E7AF2'), ('Nariz', '#120F0F')],
             'Manchas merle FIXAS na textura (assets/characters/ayra/ayra.blend), peito/patas/ponta da cauda brancos, orelhas semieretas, cauda longa e fofa, bandana azul.'),
    'pandora': ('Pandora', 'Lulu da Pomerânia branca · ~0,27 m',
                [('Pelagem', '#FBFAF6'), ('Creme', '#EFE4CF'), ('Olhos', '#120D0A'), ('Nariz', '#120F0F'), ('Laço', '#FC8CB8')],
                'Muito fofa (deslocamento + fur shells), focinho curto, orelhinhas triangulares, patas curtas, cauda em pluma sobre as costas, laço rosa.'),
    'tifa': ('Tifa', 'Yorkshire Terrier · ~0,24 m (a menor)',
             [('Castanho-dourado', '#D39A52'), ('Cinza-aço', '#4B5560'), ('Cinza claro', '#6C7883'), ('Olhos', '#120D0A'), ('Bandana', '#40BF4D')],
             'Rosto e patas castanho-dourados, dorso cinza-aço, orelhas pequenas e eretas, corpo compacto, bandana verde. A mais engraçada.'),
}
EXPR = [('happy', 'feliz'), ('curious', 'curiosa'), ('surprised', 'surpresa'), ('focused', 'concentrada'), ('affectionate', 'carinhosa')]


def f(sz, w=7):
    return ImageFont.truetype(F if w == 7 else F6, sz)


def header(d, W, name, sub):
    d.rectangle([0, 0, W, 130], fill=(255, 200, 26))
    d.text((40, 22), f'{name} — model sheet', font=f(64), fill=(92, 51, 26))
    d.text((40, 92), sub, font=f(30, 6), fill=(92, 51, 26))
    d.text((W - 40, 40), 'Clara e as Patinhas', font=f(40), fill=(255, 255, 255), anchor='ra', stroke_width=3, stroke_fill=(92, 51, 26))


def crop_char(p):
    im = Image.open(p).convert('RGB')
    W, H = im.size  # characters are centred; crop the central 62% for a tighter framing
    return im.crop((int(W * 0.19), int(H * 0.17), int(W * 0.81), int(H * 0.93)))


def main():
    for n, (name, sub, pal, note) in INFO.items():
        out = f'{ROOT}/assets/characters/{n}'
        # turnaround
        views = [('front', 'frente'), ('q34', '3/4'), ('side', 'lado'), ('back', 'costas')]
        W = 4 * 700 + 80; H = 130 + 860 + 280
        sh = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sh); header(d, W, name, sub)
        for i, (v, lbl) in enumerate(views):
            im = crop_char(f'{RAW}/{n}_{v}.png').resize((700, 856))
            sh.paste(im, (40 + i * 700, 140)); d.text((40 + i * 700 + 350, 150), lbl, font=f(36), fill=(60, 60, 60), anchor='ma')
        y = 140 + 860 + 20
        d.text((40, y), 'Paleta', font=f(34), fill=(92, 51, 26))
        for i, (pn, hx) in enumerate(pal):
            c = tuple(int(hx[k:k + 2], 16) for k in (1, 3, 5)); x = 40 + i * 260
            d.rounded_rectangle([x, y + 50, x + 230, y + 140], radius=18, fill=c, outline=(190, 190, 190), width=2)
            d.text((x + 115, y + 160), f'{pn} {hx}', font=f(22, 6), fill=(70, 70, 70), anchor='ma')
        d.text((40, y + 205), note, font=f(26, 6), fill=(70, 70, 70))
        sh.save(f'{out}/sheet_turnaround.png')
        # expressions
        W = 5 * 560 + 80; H = 130 + 640
        sh = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sh); header(d, W, name, 'Expressões: feliz · curiosa · surpresa · concentrada · carinhosa')
        for i, (e, lbl) in enumerate(EXPR):
            im = Image.open(f'{RAW}/{n}_expr_{e}.png').convert('RGB').resize((540, 540))
            sh.paste(im, (40 + i * 560, 150)); d.text((40 + i * 560 + 270, 700), lbl, font=f(36), fill=(60, 60, 60), anchor='ma')
        sh.save(f'{out}/sheet_expressions.png')
        # pose
        W = 700 * 2 + 80; H = 130 + 900
        sh = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sh); header(d, W, name, 'Pose de dança + proporção no grupo')
        sh.paste(crop_char(f'{RAW}/{n}_pose.png').resize((700, 856)), (40, 150))
        lu = Image.open(f'{RAW}/lineup.png').convert('RGB'); lu = lu.resize((700, int(700 * lu.height / lu.width)))
        sh.paste(lu, (740, 150 + (856 - lu.height) // 2)); d.text((1090, 160), 'escala (orto)', font=f(30, 6), fill=(90, 90, 90), anchor='ma')
        sh.save(f'{out}/sheet_pose.png')
    # proportions sheet (group lineup with ruler)
    lu = Image.open(f'{RAW}/lineup.png').convert('RGB'); W, H = lu.size
    d = ImageDraw.Draw(lu)
    # ortho: scale 1.95 m across 1800 px; camera centre z=0.52
    ppm = W / 1.95; z0 = H / 2 + 0.52 * ppm
    for k in range(0, 11):
        yy = z0 - k * 0.1 * ppm; d.line([20, yy, 60, yy], fill=(120, 120, 120), width=3)
        d.text((70, yy), f'{k * 10} cm', font=f(22, 6), fill=(90, 90, 90), anchor='lm')
    d.text((W // 2, 30), 'Proporções: Clara (1,00 m) · Ayra · Pandora · Tifa', font=f(40), fill=(92, 51, 26), anchor='ma')
    lu.save(f'{ROOT}/assets/characters/proporcoes.png')
    g = Image.open(f'{RAW}/group.png').convert('RGB'); g.save(f'{ROOT}/assets/characters/grupo.png')
    print('sheets composed')


if __name__ == '__main__':
    main()
