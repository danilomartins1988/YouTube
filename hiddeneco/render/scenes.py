"""Scene renderers. Each scene turns (params, timing) into frames; nothing here invents data -
every number drawn arrives through storyboard params rendered from the dossier."""
from __future__ import annotations

import math

import numpy as np
from PIL import Image

from hiddeneco.config import REPO_ROOT
from hiddeneco.logging_setup import log
from hiddeneco.render import geo
from hiddeneco.render.primitives import (aa_shape, clamp, draw_paragraph, draw_text, ease_in_out,
                                         ease_out, fill_rect, lerp, prog, text_size)
from hiddeneco.render.style import Style

FADE = 0.35


class BaseScene:
    def __init__(self, style: Style, params: dict, duration: float, narration: str = "",
                 lead: float = 0.0, speech: float | None = None, credits: list[str] | None = None,
                 chapter: str = ""):
        self.s = style
        self.p = params
        self.d = duration
        self.narration = narration
        self.lead = lead
        self.speech = speech if speech is not None else max(0.1, duration - lead)
        self.credits = credits or []
        self.chapter = params.get("chapter", chapter)
        self.W, self.H = style.W, style.H

    # ---- timing -------------------------------------------------------------------------
    def when(self, spec: dict | float | None, default: float = 0.0) -> float:
        """Seconds into the scene for a cue. Accepts {'cue': 'phrase'} (estimated from the
        phrase's position in the narration), {'at': fraction of speech} or a bare fraction."""
        if spec is None:
            return self.lead + default * self.speech
        if isinstance(spec, (int, float)):
            return self.lead + float(spec) * self.speech
        if isinstance(spec, str):
            spec = {"cue": spec}
        if "cue" in spec:
            idx = self.narration.lower().find(str(spec["cue"]).lower())
            if idx < 0:
                log("render.cue_missing", cue=spec["cue"])
                idx = 0
            return self.lead + self.speech * idx / max(1, len(self.narration))
        return self.lead + float(spec.get("at", default)) * self.speech

    # ---- frame --------------------------------------------------------------------------
    def frame(self, t: float, index: int) -> Image.Image:
        img = self.s.background()
        self.draw(img, t)
        self.chrome(img, t)
        fade = min(prog(t, 0, FADE), prog(self.d - t, 0, FADE))
        if fade < 1:
            img = Image.blend(self.s.background(), img, ease_in_out(fade))
        return self.s.grain(img, index)

    def draw(self, img: Image.Image, t: float) -> None:
        raise NotImplementedError

    def chrome(self, img: Image.Image, t: float) -> None:
        s = self.s
        a = ease_out(prog(t, 0.2, 0.6))
        if self.chapter and "chapter-tags" in s.motifs:
            fill_rect(img, (120, 92, 120 + 36 * a, 96), s.c("accent"))
            draw_text(img, self.chapter.upper(), s.f("body_bold", 24), s.c("ink"), (172, 94), "lm",
                      alpha=a, tracking=3)
        draw_text(img, "THE HIDDEN ECONOMICS", s.f("body_bold", 20), s.c("muted"), (self.W - 120, 94),
                  "rm", alpha=0.8 * a, tracking=4)
        if self.credits:
            draw_text(img, "Source: " + "  ·  ".join(self.credits), s.f("body", 22), s.c("muted"),
                      (120, self.H - 64), "ls", alpha=0.9 * a)


class TitleCard(BaseScene):
    def draw(self, img, t):
        s = self.s
        a = ease_out(prog(t, 0.2, 0.8))
        draw_text(img, self.p.get("title", ""), s.f("display", 110), s.c("ink"),
                  (self.W / 2, self.H / 2 - 20 + 30 * (1 - a)), "mm", alpha=a)
        if self.p.get("subtitle"):
            draw_text(img, self.p["subtitle"], s.f("body", 40), s.c("muted"), (self.W / 2, self.H / 2 + 80),
                      "mm", alpha=ease_out(prog(t, 0.6, 0.8)))


class MapScene(BaseScene):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.countries = geo.load_countries(str(REPO_ROOT / "assets" / "geo" / "europe_50m.geojson"))

    def draw(self, img, t):
        s, p = self.s, self.p
        zoom_start, zoom_end = 1.0, max(2.0, self.lead + 0.55 * self.speech)
        u = ease_in_out(prog(t, zoom_start, zoom_end - zoom_start))
        view = geo.interpolate_view(p["start_view"], p["end_view"], u, self.W, self.H,
                                    (0.5, 0.52), (0.31, 0.52))
        hl = ease_in_out(prog(t, zoom_start + 0.4 * (zoom_end - zoom_start), 1.2))
        fills = {p["focus"]: lerp(s.c("land"), s.c("accent"), hl)}
        geo.draw_map(img, self.countries, view, s.c("land"), s.c("border"), fills)

        # neighbour labels fade out as we zoom past them
        n_alpha = clamp(1 - abs(math.log(view.span / 16)) / 0.9) * 0.9
        for code, label in (p.get("neighbours") or {}).items():
            lon, lat = self.countries[code]["label_lonlat"]
            x, y = view.project(np.array([lon, lat]))
            if not (160 < x < self.W - 160 and 140 < y < self.H - 120):
                continue  # never show a label clipped by the frame edge
            draw_text(img, label.upper(), s.f("body_bold", 22), s.c("muted"), (x, y), "mm",
                      alpha=n_alpha, tracking=4)
        # focus label
        lon, lat = self.countries[p["focus"]]["label_lonlat"]
        x, y = view.project(np.array([lon, lat]))
        draw_text(img, p.get("focus_label", "").upper(), s.f("heading", 44), s.c("ink"), (x, y), "mm",
                  alpha=ease_out(prog(t, zoom_end - 0.6, 0.8)), tracking=8)

        # opening title over the wide shot
        ta = ease_out(prog(t, 0.15, 0.6)) * (1 - ease_in_out(prog(t, zoom_start + 0.5, 0.7)))
        if p.get("title"):
            fill_rect(img, (0, self.H / 2 - 120, self.W, self.H / 2 + 120), s.c("bg"), 0.55 * ta)
            draw_text(img, p["title"], s.f("display", 104), s.c("ink"), (self.W / 2, self.H / 2), "mm", alpha=ta)

        # callout panel
        y = 330
        for c in p.get("callouts", []):
            start = self.when(c)
            a = ease_out(prog(t, start, 0.6))
            if a <= 0:
                y += 150 if c.get("value") else 90
                continue
            x = 1270 + 60 * (1 - a)
            fill_rect(img, (x, y, x + 4, y + (110 if c.get("value") else 50)),
                      s.c("accent") if c.get("accent") else s.c("muted"), a)
            draw_text(img, c["label"].upper(), s.f("body_bold", 26), s.c("muted"), (x + 28, y + 4), "la",
                      alpha=a, tracking=3)
            if c.get("value"):
                draw_text(img, c["value"], s.f("display", 72),
                          s.c("accent2") if c.get("accent") else s.c("ink"), (x + 26, y + 40), "la", alpha=a)
                y += 160
            else:
                y += 90


class BarChartScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        rows = sorted(p["data"], key=lambda r: r["value"], reverse=True)
        vmax = max(r["value"] for r in rows)
        a0 = ease_out(prog(t, 0.2, 0.6))
        draw_text(img, p.get("title", ""), s.f("display", 64), s.c("ink"), (120, 170), "la", alpha=a0)
        draw_text(img, p.get("subtitle", ""), s.f("body", 30), s.c("muted"), (122, 252), "la", alpha=a0)
        x0, x1, top = 540, 1600, 340
        row_h = min(78, 600 / len(rows))
        step = 20000 if vmax > 60000 else 10000
        for gx in range(0, int(vmax) + 1, step):
            xx = x0 + (x1 - x0) * gx / vmax
            fill_rect(img, (xx, top - 20, xx + 1, top + row_h * len(rows)), s.c("border"), 0.6 * a0)
            draw_text(img, f"${gx // 1000}k", s.f("body", 20), s.c("muted"),
                      (xx, top + row_h * len(rows) + 14), "ma", alpha=a0)
        for i, r in enumerate(rows):
            start = self.lead * 0.5 + 0.3 + i * 0.12
            u = ease_out(prog(t, start, 1.1))
            y = top + i * row_h
            hl = r["code"] == p.get("highlight")
            ref = r["code"] == p.get("reference")
            colour = s.c("accent") if hl else (s.c("ink") if ref else s.c("muted"))
            draw_text(img, r["name"], s.f("body_bold" if hl else "body", 30),
                      s.c("ink") if (hl or ref) else s.c("muted"), (x0 - 24, y + row_h * 0.42), "rm",
                      alpha=ease_out(prog(t, start - 0.1, 0.5)))
            w = (x1 - x0) * r["value"] / vmax * u
            fill_rect(img, (x0, y + row_h * 0.14, x0 + w, y + row_h * 0.72), colour, 0.95 if hl else 0.75)
            if u > 0.02:
                draw_text(img, f"${r['value'] * u:,.0f}", s.f("body_bold", 28),
                          s.c("accent2") if hl else s.c("ink"), (x0 + w + 16, y + row_h * 0.42), "lm", alpha=u)
        if p.get("callout"):
            ca = ease_out(prog(t, self.when(p.get("callout_cue", {"cue": "That is"})) + 0.3, 0.7))
            draw_text(img, p["callout"], s.f("heading", 46), s.c("accent2"), (self.W - 120, 210), "rm", alpha=ca)


class KineticTextScene(BaseScene):
    def draw(self, img, t):
        s = self.s
        lines = self.p["lines"]
        heights = [int(ln.get("size", 60) * 1.25) for ln in lines]
        y = self.H / 2 - sum(heights) / 2 + 20
        first = self.when(lines[0], 0.0)
        bar = ease_out(prog(t, first, 0.8))
        fill_rect(img, (150, y, 158, y + sum(heights) * bar), s.c("accent"))
        for ln, h in zip(lines, heights):
            start = self.when(ln, 0.0)
            a = ease_out(prog(t, start, 0.55))
            role = ln.get("style", "body")
            draw_text(img, ln["text"], s.f(role, ln.get("size", 60)), s.c(ln.get("color", "ink")),
                      (200, y + h * 0.5 + 26 * (1 - a)), "lm", alpha=a)
            y += h


class RingStatScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        value = float(p["value"])
        cx, cy, r, thick = 620, 560, 290, 54
        start = self.when(p.get("cue"), 0.15)
        u = ease_in_out(prog(t, start, 1.8))
        a0 = ease_out(prog(t, 0.2, 0.6))
        box = (cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4)

        def ring(extent):
            def fn(d, ss):
                bb = (4 * ss, 4 * ss, (2 * r + 4) * ss, (2 * r + 4) * ss)
                d.arc(bb, -90, -90 + 360 * extent, fill=255, width=thick * ss)
            return fn
        aa_shape(img, box, s.c("land"), ring(1.0), alpha=a0)
        if u > 0:
            aa_shape(img, box, s.c("accent"), ring(value / 100 * u))
        shown = value * u
        decimals = len(str(p.get("display", "")).split(".")[1].rstrip("%")) if "." in str(p.get("display", "")) else 0
        draw_text(img, f"{shown:.{decimals}f}%", s.f("display", 120), s.c("ink"), (cx, cy), "mm", alpha=a0)
        la = ease_out(prog(t, start + 0.8, 0.7))
        y = draw_paragraph(img, p.get("sublabel", ""), s.f("heading", 58), s.c("ink"), (1020, 500), 780,
                           alpha=la)
        draw_paragraph(img, p.get("label", ""), s.f("body", 40), s.c("muted"), (1022, y + 6), 780, alpha=la)


class PictogramScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        n = int(p.get("columns", 3))
        k = int(round(float(p["fraction"]) * n))
        size, gap, x0, y0 = 200, 60, 150, 360
        start = self.when(p.get("cue"), 0.05)
        for i in range(n):
            a = ease_out(prog(t, start + i * 0.25, 0.6))
            hl = ease_in_out(prog(t, start + 1.2 + i * 0.2, 0.6)) if i < k else 0
            colour = lerp(s.c("land"), s.c("accent"), hl)
            x = x0 + i * (size + gap)
            box = (x, y0 + 30 * (1 - a), x + size, y0 + 30 * (1 - a) + int(size * 1.6))

            def person(d, ss, size=size):
                head = size * 0.36 * ss
                cxp = size * ss / 2
                d.ellipse((cxp - head / 2, 0, cxp + head / 2, head), fill=255)
                d.rounded_rectangle((size * 0.12 * ss, head * 1.15, size * 0.88 * ss, size * 1.6 * ss),
                                    radius=int(size * 0.3 * ss), fill=255)
            aa_shape(img, box, colour, person, alpha=a)
        ta = ease_out(prog(t, start + 1.4, 0.7))
        draw_text(img, str(p.get("headline", "")), s.f("display", 150), s.c("accent2"), (980, 480), "ls", alpha=ta)
        y = draw_paragraph(img, p.get("label", ""), s.f("heading", 46), s.c("ink"), (986, 570), 800, alpha=ta)
        draw_paragraph(img, p.get("sublabel", ""), s.f("body", 32), s.c("muted"), (988, y + 14), 800,
                       alpha=ease_out(prog(t, start + 2.2, 0.7)))


class RankingScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        items = list(p["items"])
        a0 = ease_out(prog(t, 0.2, 0.6))
        draw_text(img, p.get("title", ""), s.f("display", 64), s.c("ink"), (120, 190), "la", alpha=a0)
        draw_text(img, p.get("subtitle", ""), s.f("body", 30), s.c("muted"), (122, 272), "la", alpha=a0)
        top, row_h = 380, 108
        start = self.when(p.get("cue"), 0.0)
        if p.get("badge"):
            ba = ease_out(prog(t, start + len(items) * 0.45 + 0.6, 0.8))
            draw_text(img, p["badge"], s.f("display", 190), s.c("accent2"), (self.W - 140, 640), "rs", alpha=ba)
            draw_text(img, p.get("badge_label", "").upper(), s.f("body_bold", 28), s.c("muted"),
                      (self.W - 146, 700), "rs", alpha=ba, tracking=4)
        # reveal from the bottom of the top five up to number one
        for rank in range(len(items), 0, -1):
            name = items[rank - 1]
            order = len(items) - rank
            a = ease_out(prog(t, start + order * 0.45, 0.5))
            y = top + (rank - 1) * row_h
            hl = name == p.get("highlight")
            if hl:
                sweep = ease_in_out(prog(t, start + order * 0.45 + 0.3, 0.8))
                fill_rect(img, (120, y, 120 + 1100 * sweep, y + row_h - 18), s.c("accent"), 0.9)
            draw_text(img, f"{rank:02d}", s.f("display", 56), s.c("ink") if hl else s.c("muted"),
                      (150, y + (row_h - 18) / 2 + 20 * (1 - a)), "lm", alpha=a)
            draw_text(img, name, s.f("heading" if hl else "body", 50), s.c("ink"),
                      (290, y + (row_h - 18) / 2 + 20 * (1 - a)), "lm", alpha=a)


class EndCardScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        words = p.get("words", [])
        brand_t = self.when(p.get("brand_cue", {"cue": "This is"}), 0.85)
        out = ease_in_out(prog(t, brand_t - 0.6, 0.6))
        y = self.H / 2 - 150
        for i, w in enumerate(words):
            a = ease_out(prog(t, self.when({"cue": w.rstrip(".")}, 0.0), 0.45)) * (1 - out)
            draw_text(img, w, s.f("display", 110), s.c("accent2") if i == len(words) - 1 else s.c("ink"),
                      (self.W / 2, y + i * 130 + 20 * (1 - a)), "mm", alpha=a)
        ba = ease_out(prog(t, brand_t, 0.8))
        tw, _ = text_size(p.get("brand", "").upper(), s.f("display", 84), tracking=10)
        fill_rect(img, (self.W / 2 - tw / 2 * ba, self.H / 2 - 90, self.W / 2 + tw / 2 * ba, self.H / 2 - 86),
                  s.c("accent"))
        draw_text(img, p.get("brand", "").upper(), s.f("display", 84), s.c("ink"), (self.W / 2, self.H / 2),
                  "mm", alpha=ba, tracking=10)
        teaser_t = self.when({"cue": "full documentary"}, 0.5)
        draw_text(img, p.get("teaser", ""), s.f("body", 34), s.c("muted"), (self.W / 2, self.H / 2 + 110), "mm",
                  alpha=ease_out(prog(t, max(teaser_t, brand_t), 0.8)))


SCENES = {"title_card": TitleCard, "map": MapScene, "bar_chart": BarChartScene,
          "kinetic_text": KineticTextScene, "ring_stat": RingStatScene, "pictogram": PictogramScene,
          "ranking": RankingScene, "end_card": EndCardScene}
