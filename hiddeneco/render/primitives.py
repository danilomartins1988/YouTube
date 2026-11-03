"""Drawing helpers: easing, alpha text, anti-aliased shapes."""
from __future__ import annotations

from PIL import Image, ImageDraw


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def ease_out(x: float) -> float:
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x: float) -> float:
    x = clamp(x)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def prog(t: float, start: float, dur: float) -> float:
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def lerp(a, b, u):
    if isinstance(a, tuple):
        return tuple(int(round(x + (y - x) * u)) for x, y in zip(a, b))
    return a + (b - a) * u


def text_size(text: str, fnt, tracking: float = 0) -> tuple[int, int]:
    l, t, r, b = ImageDraw.Draw(Image.new("L", (1, 1))).textbbox((0, 0), text, font=fnt)
    return int(r - l + tracking * max(0, len(text) - 1)), int(b - t)


def draw_text(img: Image.Image, text: str, fnt, color, xy, anchor: str = "la",
              alpha: float = 1.0, tracking: float = 0) -> tuple[int, int, int, int]:
    """Draw text with opacity by pasting a solid colour through a glyph mask.
    anchor: Pillow anchor for the whole string (e.g. 'la', 'mm', 'rs'). Returns the drawn box."""
    if alpha <= 0.003 or not text:
        return (0, 0, 0, 0)
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    if tracking:
        widths = [probe.textlength(ch, font=fnt) + tracking for ch in text]
        total_w = sum(widths) - tracking
        _, top, _, bottom = probe.textbbox((0, 0), text, font=fnt, anchor="ls")
        pad = int(fnt.size * 0.3)
        mask = Image.new("L", (int(total_w) + 2 * pad, int(bottom - top) + 2 * pad), 0)
        d = ImageDraw.Draw(mask)
        x = pad
        for ch, w in zip(text, widths):
            d.text((x, pad - top), ch, font=fnt, fill=255, anchor="ls")
            x += w
        h_anchor, v_anchor = anchor[0], anchor[1]
        ox = {"l": 0, "m": total_w / 2, "r": total_w}[h_anchor]
        oy = {"a": 0, "t": 0, "m": (bottom - top) / 2, "s": -top, "b": bottom - top, "d": bottom - top}[v_anchor]
        x0, y0 = int(xy[0] - ox - pad), int(xy[1] - oy - pad)
    else:
        l, t, r, b = probe.textbbox((0, 0), text, font=fnt, anchor=anchor)
        pad = 4
        mask = Image.new("L", (int(r - l) + 2 * pad, int(b - t) + 2 * pad), 0)
        ImageDraw.Draw(mask).text((pad - l, pad - t), text, font=fnt, fill=255, anchor=anchor)
        x0, y0 = int(xy[0] + l - pad), int(xy[1] + t - pad)
    if alpha < 1:
        mask = mask.point(lambda v: int(v * alpha))
    img.paste(color, (x0, y0, x0 + mask.width, y0 + mask.height), mask)
    return (x0, y0, x0 + mask.width, y0 + mask.height)


def fill_rect(img: Image.Image, box, color, alpha: float = 1.0) -> None:
    x0, y0, x1, y1 = (int(round(v)) for v in box)
    if x1 <= x0 or y1 <= y0 or alpha <= 0:
        return
    if alpha >= 1:
        img.paste(color, (x0, y0, x1, y1))
    else:
        img.paste(color, (x0, y0, x1, y1), Image.new("L", (x1 - x0, y1 - y0), int(255 * alpha)))


def aa_shape(img: Image.Image, box, color, draw_fn, alpha: float = 1.0, ss: int = 3) -> None:
    """Anti-aliased shape: draw_fn(draw, scale) paints white on a supersampled mask of `box`."""
    x0, y0, x1, y1 = (int(v) for v in box)
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0 or alpha <= 0:
        return
    big = Image.new("L", (w * ss, h * ss), 0)
    draw_fn(ImageDraw.Draw(big), ss)
    mask = big.resize((w, h), Image.LANCZOS)
    if alpha < 1:
        mask = mask.point(lambda v: int(v * alpha))
    img.paste(color, (x0, y0, x1, y1), mask)


def wrap(text: str, fnt, max_width: int) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and text_size(trial, fnt)[0] > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def draw_paragraph(img: Image.Image, text: str, fnt, color, xy, max_width: int, line_height: float = 1.25,
                   alpha: float = 1.0) -> float:
    """Left-aligned wrapped text with its first baseline at xy. Returns the y after the block."""
    x, y = xy
    for line in wrap(text, fnt, max_width):
        draw_text(img, line, fnt, color, (x, y), "ls", alpha=alpha)
        y += fnt.size * line_height
    return y
