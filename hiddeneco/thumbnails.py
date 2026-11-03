"""Three deliberately different thumbnail concepts, drawn from dossier values only."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from hiddeneco.config import REPO_ROOT
from hiddeneco.models import Dossier
from hiddeneco.render import geo
from hiddeneco.render.primitives import aa_shape, draw_text, fill_rect
from hiddeneco.render.style import Style

W, H = 1280, 720


def _style(style_cfg: dict) -> Style:
    st = Style({**style_cfg, "motifs": [m for m in style_cfg.get("motifs", []) if m != "film-grain"]}, W, H)
    return st


def concept_number(st: Style, d: Dossier) -> Image.Image:
    img = st.background()
    countries = geo.load_countries(str(REPO_ROOT / "assets" / "geo" / "europe_50m.geojson"))
    view = geo.View(8.25, 46.8, 9.5, W, H, anchor=(0.74, 0.5))
    geo.draw_map(img, countries, view, st.c("land"), st.c("border"), {"CHE": st.c("accent")}, border_px=1.5)
    fill_rect(img, (0, 0, 640, H), st.c("bg"), 0.82)
    gd = d.claim("gdppc_che_2023")
    draw_text(img, gd.display, st.f("display", 132), st.c("accent2"), (60, 330), "ls")
    draw_text(img, f"PER PERSON · {gd.fields['year']}", st.f("body_bold", 38), st.c("ink"), (66, 400), "ls",
              tracking=4)
    draw_text(img, "HOW?", st.f("display", 120), st.c("ink"), (60, 600), "ls")
    return img


def concept_versus(st: Style, d: Dossier) -> Image.Image:
    img = st.background()
    rows = {r["code"]: r for r in d.claim("gdppc_chart_2023").value}
    che, deu = rows["CHE"]["value"], rows["DEU"]["value"]
    base, maxh = 640, 470
    for i, (code, v, col) in enumerate((("CHE", che, st.c("accent")), ("DEU", deu, st.c("muted")))):
        x = 760 + i * 230
        h = maxh * v / che
        fill_rect(img, (x, base - h, x + 180, base), col)
        draw_text(img, rows[code]["name"].upper(), st.f("body_bold", 30), st.c("ink"), (x + 90, base + 40), "mm",
                  tracking=2)
    draw_text(img, d.claim("ratio_che_deu_2023").display, st.f("display", 210), st.c("accent2"), (60, 330), "ls")
    draw_text(img, "GERMANY'S", st.f("display", 80), st.c("ink"), (66, 430), "ls")
    draw_text(img, "INCOME PER PERSON", st.f("heading", 44), st.c("ink"), (66, 495), "ls")
    return img


def concept_ring(st: Style, d: Dossier) -> Image.Image:
    img = st.background()
    c = d.claim("pharma_share_2024")
    cx, cy, r, th = 1035, 360, 195, 52
    box = (cx - r, cy - r, cx + r, cy + r)

    def arc(ext):
        return lambda dr, ss: dr.arc((0, 0, 2 * r * ss, 2 * r * ss), -90, -90 + 360 * ext, fill=255, width=th * ss)
    aa_shape(img, box, st.c("land"), arc(1.0))
    aa_shape(img, box, st.c("accent"), arc(float(c.value) / 100))
    draw_text(img, c.display, st.f("display", 84), st.c("ink"), (cx, cy), "mm")
    draw_text(img, "WHAT", st.f("display", 100), st.c("ink"), (60, 260), "ls")
    draw_text(img, "SWITZERLAND", st.f("display", 100), st.c("accent2"), (60, 370), "ls")
    draw_text(img, "REALLY SELLS", st.f("display", 100), st.c("ink"), (60, 480), "ls")
    return img


CONCEPTS = [
    ("a_the_number", concept_number,
     "Single huge number over a red Switzerland. Curiosity gap: the figure plus 'HOW?'."),
    ("b_versus", concept_versus,
     "Two-bar comparison with Germany - instantly readable on mobile; relies on a familiar benchmark."),
    ("c_what_it_sells", concept_ring,
     "Ring chart teasing the export answer (chemicals & pharma) without stating it in the text."),
]


def make_thumbnails(style_cfg: dict, dossier: Dossier, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    st = _style(style_cfg)
    paths, md = [], ["# Thumbnail concepts", ""]
    for name, fn, why in CONCEPTS:
        p = out_dir / f"thumb_{name}.png"
        fn(st, dossier).save(p, optimize=True)
        paths.append(p)
        md.append(f"- **{p.name}** - {why}")
    md += ["", "All numbers are pulled from the dossier; all graphics are original. "
           "Run an A/B test (YouTube 'Test & compare') only after approval."]
    (out_dir / "thumbnails.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return paths
