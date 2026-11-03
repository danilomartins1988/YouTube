"""Original vector illustrations drawn in code: skylines, ports, airports, an old creek, offshore oil.

Nothing here is traced from photographs or depicts a specific copyrighted/trademarked building:
towers are generic, the 'supertall' is a stylised stepped spire, aircraft and ships carry no livery.
Each illustration is a few RGBA layers drawn once at 2x and downsampled; scenes pan the layers at
different speeds for parallax, thumbnails composite a single still.
"""
from __future__ import annotations

import math
import random
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFilter

SS = 2  # supersampling factor for the static layers


def _rgba(rgb, a=255):
    return (int(rgb[0]), int(rgb[1]), int(rgb[2]), int(a))


def _mix(a, b, u):
    return tuple(int(a[i] + (b[i] - a[i]) * u) for i in range(3))


class Canvas:
    """A supersampled RGBA layer; coordinates are given in output pixels."""

    def __init__(self, w: int, h: int):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def poly(self, pts, fill):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=fill)

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle((x0 * SS, y0 * SS, x1 * SS, y1 * SS), fill=fill)

    def line(self, pts, fill, width):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=fill, width=max(1, int(width * SS)))

    def ellipse(self, x0, y0, x1, y1, fill):
        self.d.ellipse((x0 * SS, y0 * SS, x1 * SS, y1 * SS), fill=fill)

    def done(self) -> Image.Image:
        return self.img.resize((self.w, self.h), Image.LANCZOS)


# ---- building blocks --------------------------------------------------------------------------
def tower(c: Canvas, x, base, w, h, fill, rng, windows=None, crown=None):
    """Generic rectangular tower with optional setbacks and lit windows."""
    c.rect(x, base - h, x + w, base, fill)
    if crown == "setback" and h > 120:
        c.rect(x + w * 0.15, base - h - h * 0.08, x + w * 0.85, base - h, fill)
    elif crown == "slant":
        c.poly([(x, base - h), (x + w, base - h - w * 0.6), (x + w, base - h)], fill)
    elif crown == "mast":
        c.rect(x + w * 0.46, base - h - h * 0.12, x + w * 0.54, base - h, fill)
    if windows:
        col, density = windows
        step = 9 if w < 60 else 11
        for wy in range(int(base - h + 12), int(base - 8), step):
            for wx in range(int(x + 6), int(x + w - 6), 8):
                if rng.random() < density:
                    c.rect(wx, wy, wx + 3, wy + 4, col)


def supertall(c: Canvas, cx, base, h, fill, glint=None):
    """A stylised, generic stepped spire (no real building's profile)."""
    w = h * 0.16
    tiers = 7
    y = base
    for i in range(tiers):
        tw = w * (1 - i / tiers * 0.85)
        th = h * 0.62 / tiers * (1.15 if i == 0 else 1.0)
        c.poly([(cx - tw / 2, y), (cx + tw / 2, y), (cx + tw / 2 * 0.92, y - th), (cx - tw / 2 * 0.92, y - th)], fill)
        y -= th
    c.poly([(cx - w * 0.07, y), (cx + w * 0.07, y), (cx, base - h)], fill)        # spire
    if glint:
        c.line([(cx - w * 0.02, base - h * 0.15), (cx - w * 0.02, base - h * 0.9)], glint, 2)


def crane(c: Canvas, x, base, h, fill, boom_up=False):
    """Ship-to-shore gantry crane silhouette."""
    leg = h * 0.55
    span = h * 0.38
    for lx in (x, x + span):
        c.rect(lx, base - leg, lx + 7, base, fill)
    c.rect(x - 4, base - leg - 10, x + span + 11, base - leg, fill)               # portal beam
    c.rect(x + span * 0.35, base - h, x + span * 0.35 + 8, base - leg, fill)     # A-frame
    if boom_up:
        c.line([(x + span * 0.4, base - leg - 6), (x - h * 0.35, base - h * 1.15)], fill, 8)
    else:
        c.rect(x - h * 0.55, base - leg - 26, x + span + h * 0.3, base - leg - 14, fill)   # boom
    c.line([(x + span * 0.39, base - h), (x - h * 0.5, base - leg - 24)], fill, 2)        # stays
    c.line([(x + span * 0.39, base - h), (x + span + h * 0.25, base - leg - 24)], fill, 2)


def containers(c: Canvas, x0, x1, base, rows, palette, rng, size=(26, 13)):
    w, h = size
    for r in range(rows):
        x = x0 + (r % 2) * w * 0.5
        while x + w < x1:
            if rng.random() < 0.9:
                c.rect(x, base - (r + 1) * h, x + w - 2, base - r * h - 2, palette[rng.randrange(len(palette))])
            x += w


def ship(c: Canvas, x, waterline, length, hull, stack_palette, rng):
    hh = length * 0.07
    c.poly([(x, waterline - hh), (x + length, waterline - hh), (x + length * 0.94, waterline),
            (x + length * 0.04, waterline)], hull)
    c.rect(x + length * 0.82, waterline - hh - length * 0.11, x + length * 0.92, waterline - hh, hull)  # bridge
    containers(c, x + length * 0.08, x + length * 0.8, waterline - hh, 3, stack_palette, rng, (22, 11))


def aircraft(c: Canvas, cx, cy, span, fill, angle_deg=-12):
    """Generic wide-body silhouette seen from below/side, rotated (no livery)."""
    L = span * 1.05
    pts_body = [(-L / 2, -span * 0.035), (L * 0.42, -span * 0.035), (L / 2, 0), (L * 0.42, span * 0.035),
                (-L / 2 + span * 0.05, span * 0.035), (-L / 2, 0)]
    wing = [(-span * 0.05, 0), (span * 0.12, 0), (-span * 0.18, -span / 2), (-span * 0.26, -span / 2)]
    wing2 = [(-span * 0.05, 0), (span * 0.12, 0), (-span * 0.18, span / 2), (-span * 0.26, span / 2)]
    tail = [(-L / 2 + span * 0.02, 0), (-L / 2 + span * 0.14, 0), (-L / 2 + span * 0.02, -span * 0.2),
            (-L / 2 - span * 0.03, -span * 0.2)]
    stab = [(-L / 2 + span * 0.03, 0), (-L / 2 + span * 0.1, 0), (-L / 2 - span * 0.02, span * 0.14),
            (-L / 2 - span * 0.06, span * 0.14)]
    a = math.radians(angle_deg)
    rot = lambda p: (cx + p[0] * math.cos(a) - p[1] * math.sin(a), cy + p[0] * math.sin(a) + p[1] * math.cos(a))  # noqa: E731
    for shape in (wing2, stab, pts_body, wing, tail):
        c.poly([rot(p) for p in shape], fill)


def dhow(c: Canvas, x, waterline, length, fill):
    c.poly([(x, waterline - length * 0.12), (x + length, waterline - length * 0.2),
            (x + length * 0.86, waterline), (x + length * 0.12, waterline)], fill)
    mast = x + length * 0.45
    c.line([(mast, waterline - length * 0.12), (mast + length * 0.05, waterline - length * 0.85)], fill, 3)
    c.poly([(mast + length * 0.05, waterline - length * 0.86), (mast + length * 0.5, waterline - length * 0.3),
            (mast - length * 0.32, waterline - length * 0.22)], fill)


def windtower_house(c: Canvas, x, base, w, h, fill):
    c.rect(x, base - h, x + w, base, fill)
    tw = w * 0.3
    c.rect(x + w * 0.6, base - h - h * 0.7, x + w * 0.6 + tw, base - h, fill)
    for i in range(3):
        c.rect(x + w * 0.6 + tw * (0.15 + i * 0.3), base - h - h * 0.62, x + w * 0.6 + tw * (0.15 + i * 0.3) + 2,
               base - h - h * 0.2, (0, 0, 0, 0))


def platform(c: Canvas, x, waterline, w, fill, flare=None):
    deck = waterline - w * 0.45
    for lx in (x + w * 0.1, x + w * 0.45, x + w * 0.8):
        c.rect(lx, deck, lx + 6, waterline + 10, fill)
    c.rect(x, deck - 18, x + w, deck, fill)
    c.rect(x + w * 0.1, deck - 60, x + w * 0.5, deck - 18, fill)
    c.poly([(x + w * 0.62, deck - 18), (x + w * 0.72, deck - 18), (x + w * 0.68, deck - w * 0.9)], fill)  # derrick
    c.line([(x + w * 0.9, deck - 18), (x + w * 1.15, deck - w * 0.6)], fill, 5)                          # flare boom
    if flare:
        c.ellipse(x + w * 1.12, deck - w * 0.68, x + w * 1.2, deck - w * 0.56, flare)


# ---- compositions -----------------------------------------------------------------------------
def _water(c: Canvas, y, w, h, col, line_col, rng):
    c.rect(0, y, w, h, col)
    for i in range(40):
        yy = y + 6 + rng.random() * (h - y - 6)
        xx = rng.random() * w
        c.rect(xx, yy, xx + 30 + rng.random() * 90, yy + 1.5, line_col)


@lru_cache(maxsize=16)
def layers(kind: str, W: int, H: int, pal: tuple, horizon: float = 0.8, pad: int = 240):
    """Static parallax layers: list of (RGBA image of width W+pad, speed in px/s)."""
    P = dict(pal)
    rng = random.Random(f"{kind}-{W}x{H}")
    base = H * horizon
    far, mid, near = (_rgba(_mix(P["bg2"], P["land"], 0.55), 255), _rgba(P["land"], 255),
                      _rgba(_mix(P["land"], P["bg"], 0.55), 255))
    steel = _rgba(_mix(P["land"], P["ink"], 0.32), 255)      # lighter structures that must read on dark sky
    lit = _rgba(P["accent2"], 170)
    lit_dim = _rgba(P["accent2"], 90)
    out = []
    Wp = W + pad
    scale = H / 1080 if W > H else W / 1080
    if kind in ("skyline", "skyline_wide"):
        back = Canvas(Wp, H)
        x = -20
        while x < Wp:
            w = rng.uniform(40, 90) * scale
            tower(back, x, base, w, rng.uniform(90, 260) * scale, far, rng, (lit_dim, 0.06))
            x += w + rng.uniform(4, 18) * scale
        out.append((back.done(), 4.0))
        midc = Canvas(Wp, H)
        x = 0
        while x < Wp:
            w = rng.uniform(46, 110) * scale
            h = rng.uniform(160, 430) * scale
            tower(midc, x, base, w, h, mid, rng, (lit, 0.09), rng.choice([None, "setback", "slant", "mast"]))
            x += w + rng.uniform(20, 70) * scale
        st = Canvas(Wp, H)
        supertall(st, Wp * 0.56, base, H * (0.66 if W > H else 0.42), mid, glint=_rgba(P["accent2"], 140))
        midc.img.alpha_composite(st.img)
        out.append((midc.done(), 9.0))
        water = Canvas(Wp, H)
        _water(water, base, Wp, H, _rgba(_mix(P["bg"], P["bg2"], 0.5), 255), _rgba(P["accent2"], 60), rng)
        out.append((water.done(), 14.0))
    elif kind == "port":
        back = Canvas(Wp, H)
        x = 0
        while x < Wp:
            w = rng.uniform(40, 80) * scale
            tower(back, x, base - 40 * scale, w, rng.uniform(60, 160) * scale, far, rng, (lit_dim, 0.05))
            x += w + rng.uniform(10, 40) * scale
        out.append((back.done(), 3.0))
        quay = Canvas(Wp, H)
        quay.rect(0, base - 6 * scale, Wp, base + 4 * scale, near)
        cpal = [_rgba(P["accent"], 255), _rgba(P["accent2"], 255), _rgba(P["muted"], 255),
                _rgba(_mix(P["accent"], P["bg"], 0.4), 255), _rgba(_mix(P["land"], P["ink"], 0.25), 255)]
        containers(quay, 0, Wp, base - 6 * scale, 4, cpal, rng, (int(30 * scale), int(15 * scale)))
        for i in range(5):
            crane(quay, Wp * (0.08 + i * 0.2), base - 6 * scale, rng.uniform(380, 440) * scale, steel,
                  boom_up=(i == 3))
        out.append((quay.done(), 8.0))
        sea = Canvas(Wp, H)
        _water(sea, base + 4 * scale, Wp, H, _rgba(_mix(P["bg"], P["bg2"], 0.5), 255), _rgba(P["accent2"], 50), rng)
        ship(sea, Wp * 0.22, base + 120 * scale, 760 * scale, mid, cpal, rng)
        out.append((sea.done(), 16.0))
    elif kind == "airport":
        back = Canvas(Wp, H)
        x = 0
        while x < Wp:
            w = rng.uniform(50, 100) * scale
            tower(back, x, base, w, rng.uniform(80, 240) * scale, far, rng, (lit_dim, 0.06))
            x += w + rng.uniform(10, 40) * scale
        tw = Canvas(Wp, H)   # control tower
        tx = Wp * 0.72
        tw.rect(tx, base - 260 * scale, tx + 22 * scale, base, mid)
        tw.poly([(tx - 30 * scale, base - 260 * scale), (tx + 52 * scale, base - 260 * scale),
                 (tx + 40 * scale, base - 300 * scale), (tx - 18 * scale, base - 300 * scale)], mid)
        back.img.alpha_composite(tw.img)
        out.append((back.done(), 4.0))
        ground = Canvas(Wp, H)
        ground.rect(0, base, Wp, H, _rgba(_mix(P["bg"], P["land"], 0.4), 255))
        for i in range(-6, 20):    # runway perspective lights
            ground.line([(Wp * 0.5 + i * 80 * scale, base + 2), (Wp * 0.5 + i * 420 * scale, H)],
                        _rgba(P["accent2"], 50), 2)
        out.append((ground.done(), 10.0))
        plane = Canvas(Wp, H)
        aircraft(plane, Wp * 0.4, base - 300 * scale, 420 * scale, _rgba(P["ink"], 235), -14)
        out.append((plane.done(), -60.0))     # flies against the pan
    elif kind == "creek":
        back = Canvas(Wp, H)
        x = 0
        while x < Wp:
            w = rng.uniform(70, 130) * scale
            windtower_house(back, x, base, w, rng.uniform(40, 80) * scale, mid)
            x += w + rng.uniform(4, 20) * scale
        out.append((back.done(), 5.0))
        water = Canvas(Wp, H)
        _water(water, base, Wp, H, _rgba(_mix(P["bg"], P["bg2"], 0.5), 255), _rgba(P["accent2"], 50), rng)
        for i in range(4):
            dhow(water, Wp * (0.1 + i * 0.24), base + (40 + 30 * (i % 2)) * scale, rng.uniform(150, 220) * scale, steel)
        out.append((water.done(), 12.0))
    elif kind == "offshore":
        sea = Canvas(Wp, H)
        _water(sea, base, Wp, H, _rgba(_mix(P["bg"], P["bg2"], 0.5), 255), _rgba(P["accent2"], 50), rng)
        platform(sea, Wp * 0.42, base, 340 * scale, steel, flare=_rgba(P["accent"], 240))
        platform(sea, Wp * 0.12, base, 170 * scale, mid)
        out.append((sea.done(), 6.0))
    else:
        raise ValueError(f"Unknown illustration kind '{kind}'")
    return out


def sky_glow(W: int, H: int, colour, horizon: float, strength: float = 0.7) -> Image.Image:
    """Soft horizon glow (RGBA)."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    cy = H * horizon
    for i in range(23, -1, -1):      # large to small so the centre stays brightest
        r = (i + 1) / 24
        d.ellipse((W * (0.5 - 0.8 * r), cy - H * 0.45 * r, W * (0.5 + 0.8 * r), cy + H * 0.15 * r),
                  fill=_rgba(colour, int(255 * strength * (1 - r) ** 2 / 2)))
    return glow.filter(ImageFilter.GaussianBlur(max(4, W // 80)))


def compose(img: Image.Image, kind: str, palette: dict, t: float = 0.0, horizon: float = 0.8,
            pan: bool = True) -> None:
    """Draw the illustration onto img (RGB) at time t (parallax pan)."""
    W, H = img.size
    pal = tuple(sorted((k, tuple(v)) for k, v in palette.items()))
    img.paste(sky_glow(W, H, palette["accent"], horizon), (0, 0), sky_glow(W, H, palette["accent"], horizon))
    for layer, speed in layers(kind, W, H, pal, horizon):
        pad = layer.width - W
        off = (speed * t) % pad if (pan and speed > 0) else (pad / 2 if speed >= 0 else 0)
        if speed < 0 and pan:
            off = 0
            x_extra = int(-speed * t) % (W + 600) - 300
            img.paste(layer.crop((0, 0, W, H)), (x_extra - int(pad / 2), -int(abs(speed) * t * 0.25)),
                      layer.crop((0, 0, W, H)))
            continue
        crop = layer.crop((int(off), 0, int(off) + W, H))
        img.paste(crop, (0, 0), crop)
