"""Thumbnail / cover concepts defined in each deliverable.yaml (`thumbnails:`), rendered from
dossier values. Concept types are reusable layouts; the words and numbers are per video."""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image

from hiddeneco.config import REPO_ROOT
from hiddeneco.render import geo
from hiddeneco.render.primitives import aa_shape, draw_text, fill_rect, text_size
from hiddeneco.render.style import Style


def _fit(st: Style, text: str, role: str, size: int, max_w: int):
    while size > 20 and text_size(text, st.f(role, size))[0] > max_w:
        size -= 4
    return st.f(role, size)


def number_over_map(st: Style, c: dict) -> Image.Image:
    img = st.background()
    W, H = st.W, st.H
    countries = geo.load_countries(str(REPO_ROOT / "assets" / "geo" / "europe_50m.geojson"))
    v = c["view"]
    vertical = H > W
    view = geo.View(v["lon"], v["lat"], v["span_deg"], W, H, anchor=(0.5, 0.3) if vertical else (0.74, 0.5))
    geo.draw_map(img, countries, view, st.c("land"), st.c("border"), {c["focus"]: st.c("accent")}, border_px=1.5)
    if vertical:
        fill_rect(img, (0, H * 0.55, W, H), st.c("bg"), 0.85)
        x, y = 70, int(H * 0.66)
    else:
        fill_rect(img, (0, 0, W * 0.5, H), st.c("bg"), 0.82)
        x, y = 60, 330
    draw_text(img, c["number"], _fit(st, c["number"], "display", 150, int(W * 0.45 if not vertical else W - 140)),
              st.c("accent2"), (x, y), "ls")
    draw_text(img, c.get("kicker", ""), st.f("body_bold", 38), st.c("ink"), (x + 6, y + 70), "ls", tracking=4)
    draw_text(img, c.get("hook", ""), st.f("display", 120), st.c("ink"), (x, y + 270), "ls")
    return img


def versus_bars(st: Style, c: dict) -> Image.Image:
    img = st.background()
    W, H = st.W, st.H
    rows = {r["code"]: r for r in c["data"]}
    va, vb = rows[c["a"]]["value"], rows[c["b"]]["value"]
    base, maxh = int(H * 0.89), int(H * 0.65)
    for i, (code, v, col) in enumerate(((c["a"], va, st.c("accent")), (c["b"], vb, st.c("muted")))):
        x = int(W * 0.6) + i * int(W * 0.18)
        h = maxh * v / max(va, vb)
        fill_rect(img, (x, base - h, x + int(W * 0.14), base), col)
        draw_text(img, rows[code]["name"].upper(), st.f("body_bold", 30), st.c("ink"),
                  (x + int(W * 0.07), base + 40), "mm", tracking=2)
    draw_text(img, c["number"], st.f("display", 210), st.c("accent2"), (60, 330), "ls")
    draw_text(img, c.get("line1", ""), st.f("display", 80), st.c("ink"), (66, 430), "ls")
    draw_text(img, c.get("line2", ""), st.f("heading", 44), st.c("ink"), (66, 495), "ls")
    return img


def ring_text(st: Style, c: dict) -> Image.Image:
    img = st.background()
    W, H = st.W, st.H
    vertical = H > W
    if vertical:
        cx, cy, r, th = W // 2, int(H * 0.58), 300, 70
        tx, ty, size, max_w = 70, int(H * 0.17), 120, W - 140
    else:
        cx, cy, r, th = int(W * 0.81), H // 2, 195, 52
        tx, ty, size, max_w = 60, 260, 100, int(W * 0.58)
    box = (cx - r, cy - r, cx + r, cy + r)

    def arc(ext):
        return lambda dr, ss: dr.arc((0, 0, 2 * r * ss, 2 * r * ss), -90, -90 + 360 * ext, fill=255, width=th * ss)
    aa_shape(img, box, st.c("land"), arc(1.0))
    aa_shape(img, box, st.c("accent"), arc(float(c["value"]) / 100))
    draw_text(img, c["display"], st.f("display", 120 if vertical else 84), st.c("ink"), (cx, cy), "mm")
    for i, line in enumerate(c.get("lines", [])):
        colour = st.c("accent2") if i == c.get("highlight_line", -1) else st.c("ink")
        draw_text(img, line, _fit(st, line, "display", size, max_w), colour, (tx, ty + i * size * 1.1), "ls")
    if c.get("footer"):
        draw_text(img, c["footer"], st.f("body_bold", 40), st.c("muted"), (W // 2, cy + r + 120), "mm", tracking=3)
    return img


CONCEPTS = {"number_over_map": number_over_map, "versus_bars": versus_bars, "ring_text": ring_text}


def illustrated_headline(st: Style, c: dict) -> Image.Image:
    """Original illustration (skyline / port / airport...) with one big headline.

    Optional `panels`: several illustration kinds side by side (e.g. port | airport | skyline).
    Optional `bars`: sourced shares [{label, value}] drawn as a small chart (values from the dossier).
    """
    from hiddeneco.render import illustrate
    W, H = st.W, st.H
    img = st.background()
    panels = c.get("panels") or [c.get("kind", "skyline")]
    pw = W // len(panels)
    for i, kind in enumerate(panels):
        tile = st.background().resize((W, H))
        illustrate.compose(tile, kind, st.palette, t=0.0, horizon=float(c.get("horizon", 0.9)), pan=False)
        x0 = int(W / 2 - pw / 2) if len(panels) > 1 else 0
        img.paste(tile.crop((x0, 0, x0 + pw, H)), (i * pw, 0))
        if i:
            fill_rect(img, (i * pw - 3, 0, i * pw + 3, H), st.c("bg"))
    # darken the text side for legibility
    side = c.get("text_side", "left")
    grad = Image.linear_gradient("L").rotate(90 if side == "left" else -90, expand=True).resize((W, H))
    shade = Image.new("RGB", (W, H), st.c("bg"))
    img.paste(shade, (0, 0), grad.point(lambda v: int(v * 0.85)))
    x = 60 if side == "left" else W - 60
    anchor = "ls" if side == "left" else "rs"
    headline = c["headline"]
    lines = [ln for ln in re.split(r"\\n|\n", headline) if ln]   # YAML may give a literal backslash-n
    size = int(c.get("font_size", 190 if W > H else 220))
    y = int(H * float(c.get("y", 0.42)))
    for ln in lines:
        fnt = _fit(st, ln, "display", size, int(W * (0.5 if c.get("bars") else 0.62)))
        draw_text(img, ln, fnt, st.c(c.get("colour", "ink")), (x, y), anchor)
        y += int(fnt.size * 1.0)
    if c.get("accent_line"):
        fnt = _fit(st, c["accent_line"], "display", int(size * 0.6), int(W * 0.6))
        draw_text(img, c["accent_line"], fnt, st.c("accent2"), (x, y + 10), anchor)
        y += int(fnt.size * 1.1)
    if c.get("kicker"):
        draw_text(img, c["kicker"].upper(), st.f("body_bold", 34), st.c("accent"), (x, int(H * (0.14 if W > H else 0.08))), anchor,
                  tracking=6)
    if c.get("bars"):
        bars = c["bars"]
        n = len(bars)
        bw, gap = int(W * 0.085), int(W * 0.014)
        bx0 = W - 50 - n * bw - (n - 1) * gap
        by1 = int(H * 0.84)
        vmax = max(float(b["value"]) for b in bars)
        for i, b in enumerate(bars):
            h = int(H * 0.36 * float(b["value"]) / vmax)
            xx = bx0 + i * (bw + gap)
            fill_rect(img, (xx, by1 - h, xx + bw, by1), st.c("accent2") if i == 0 else st.c("accent"), 0.92)
            draw_text(img, f"{float(b['value']):.1f}%", st.f("display", 36), st.c("ink"), (xx + bw / 2, by1 - h - 14), "ms")
            label = b["label"].split(" (")[0].split(" &")[0].upper()
            for k, part in enumerate(label.split(" ")):
                draw_text(img, part, _fit(st, part, "body_bold", 18, bw), st.c("ink"), (xx + bw / 2, by1 + 26 + k * 20),
                          "ms", tracking=1)
    if c.get("footer"):
        draw_text(img, c["footer"].upper(), st.f("body_bold", 24), st.c("muted"), (x, H - 44), anchor, tracking=5)
    return img


CONCEPTS["illustrated_headline"] = illustrated_headline


def make_thumbnails(style_cfg: dict, concepts: list[dict], out_dir: Path) -> list[Path]:
    """concepts: rendered (placeholder-free) specs: {id, type, size: [w, h], why, ...}."""
    out_dir.mkdir(parents=True, exist_ok=True)
    cfg = {**style_cfg, "motifs": [m for m in style_cfg.get("motifs", []) if m != "film-grain"]}
    paths, md = [], ["# Thumbnail / cover concepts", ""]
    for c in concepts:
        w, h = c.get("size", [1280, 720])
        st = Style(cfg, w, h)
        p = out_dir / f"thumb_{c['id']}.png"
        CONCEPTS[c["type"]](st, c).save(p, optimize=True)
        paths.append(p)
        md.append(f"- **{p.name}** ({w}x{h}) - {c.get('why', '')}")
    md += ["", "All numbers come from the dossier and every graphic is original. Each concept must "
           "describe what the video actually shows (no misleading clickbait)."]
    (out_dir / "thumbnails.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return paths
