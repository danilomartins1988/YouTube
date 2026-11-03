"""Thumbnail / cover concepts defined in each deliverable.yaml (`thumbnails:`), rendered from
dossier values. Concept types are reusable layouts; the words and numbers are per video."""
from __future__ import annotations

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
