"""Scene renderers for 16:9 and 9:16. Nothing here invents data: every number drawn arrives
through storyboard params that were rendered from the dossier.

Layout conventions
* 16:9 - generous margins, chapter tag top-left, credits bottom-left.
* 9:16 - all key content inside the platform safe zone (top/bottom/right UI overlays),
         credits sit above the caption band, captions sit above the bottom UI.
"""
from __future__ import annotations

import math
import re

import numpy as np
from PIL import Image, ImageDraw

from hiddeneco import timing
from hiddeneco.config import REPO_ROOT
from hiddeneco.logging_setup import log
from hiddeneco.render import geo
from hiddeneco.render.primitives import (aa_shape, clamp, draw_paragraph, draw_text, ease_in_out,
                                         ease_out, fill_rect, lerp, prog, text_size, wrap)
from hiddeneco.render.style import Style

NUM = re.compile(r"[\d][\d,]*(?:\.\d+)?")
_WARNED: set[str] = set()


class BaseScene:
    def __init__(self, style: Style, params: dict, duration: float, narration: str = "",
                 lead: float = 0.0, speech: float | None = None, credits: list[str] | None = None,
                 chapter: str = "", words: list[dict] | None = None, captions: list[dict] | None = None,
                 fade: float = 0.35, safe: dict | None = None):
        self.s = style
        self.p = params
        self.d = duration
        self.narration = narration
        self.lead = lead
        self.speech = speech if speech is not None else max(0.1, duration - lead)
        self.credits = credits or []
        self.chapter = params.get("chapter", chapter)
        self.words = words or []
        self.captions = captions
        self.fade = fade
        self.W, self.H = style.W, style.H
        self.v = self.H > self.W
        self.safe = safe or {"top": 0, "bottom": 0, "left": 0, "right": 0}
        # content box (x0, y0, x1, y1) and caption baseline
        if self.v:
            self.box = (80, self.safe["top"] + 40, self.W - self.safe["right"] - 20,
                        self.H - self.safe["bottom"] - 290)
            self.caption_y = self.H - self.safe["bottom"] - 150
        else:
            self.box = (120, 150, self.W - 120, self.H - 110)
            self.caption_y = self.H - 150
        self.cx = (self.box[0] + self.box[2]) / 2
        self.cy = (self.box[1] + self.box[3]) / 2

    # ---- timing -------------------------------------------------------------------------
    def when(self, spec, default: float = 0.0) -> float:
        """Seconds into the scene for a cue: {'cue': phrase} | 'phrase' | {'at': fraction} | fraction."""
        if spec is None:
            return self.lead + default * self.speech
        if isinstance(spec, (int, float)):
            return self.lead + float(spec) * self.speech
        if isinstance(spec, str):
            spec = {"cue": spec}
        if "cue" in spec:
            t = timing.cue_time(self.words, str(spec["cue"])) if self.words else None
            if t is None:
                idx = self.narration.lower().find(str(spec["cue"]).lower())
                if idx < 0:
                    if spec["cue"] not in _WARNED:
                        _WARNED.add(spec["cue"])
                        log("render.cue_missing", cue=spec["cue"], narration=self.narration[:60])
                    idx = 0
                t = self.lead + self.speech * idx / max(1, len(self.narration))
            return t + float(spec.get("offset", 0.0))
        return self.lead + float(spec.get("at", default)) * self.speech

    # ---- frame --------------------------------------------------------------------------
    def frame(self, t: float, index: int) -> Image.Image:
        img = self.s.background()
        self.draw(img, t)
        self.chrome(img, t)
        fade = min(prog(t, 0, self.fade), prog(self.d - t, 0, self.fade))
        if fade < 1:
            img = Image.blend(self.s.background(), img, ease_in_out(fade))
        if self.captions:
            self.draw_captions(img, t)
        return self.s.grain(img, index)

    def draw(self, img: Image.Image, t: float) -> None:
        raise NotImplementedError

    def chrome(self, img: Image.Image, t: float) -> None:
        s = self.s
        a = ease_out(prog(t, 0.15, 0.5))
        x0, y0 = self.box[0], self.box[1]
        if self.v:
            if self.chapter and "chapter-tags" in s.motifs:
                fill_rect(img, (x0, y0 - 2, x0 + 36 * a, y0 + 2), s.c("accent"))
                draw_text(img, self.chapter.upper(), s.f("body_bold", 28), s.c("ink"), (x0 + 52, y0), "lm",
                          alpha=a, tracking=3)
            if self.credits:
                y = self.box[3] + 30
                draw_paragraph(img, "Source: " + " · ".join(self.credits), s.f("body", 24),
                               s.c("muted"), (x0, y), self.box[2] - x0, alpha=0.9 * a)
            return
        if self.chapter and "chapter-tags" in s.motifs:
            fill_rect(img, (120, 92, 120 + 36 * a, 96), s.c("accent"))
            draw_text(img, self.chapter.upper(), s.f("body_bold", 24), s.c("ink"), (172, 94), "lm",
                      alpha=a, tracking=3)
        draw_text(img, "THE HIDDEN ECONOMICS", s.f("body_bold", 20), s.c("muted"), (self.W - 120, 94),
                  "rm", alpha=0.8 * a, tracking=4)
        if self.credits:
            text = "Source: " + "  ·  ".join(self.credits)
            if getattr(self, "credit_backing", False):   # keep credits legible over map fills
                w, _ = text_size(text, s.f("body", 22))
                fill_rect(img, (108, self.H - 92, 132 + w, self.H - 54), s.c("bg"), 0.75 * a)
            draw_text(img, text, s.f("body", 22), s.c("muted"), (120, self.H - 64), "ls", alpha=0.9 * a)

    def draw_captions(self, img: Image.Image, t: float) -> None:
        """Short caption chunks with the word being spoken highlighted."""
        caps = self.captions
        active = None
        for i, c in enumerate(caps):
            nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["end"] + 0.5
            if c["start"] - 0.05 <= t < max(nxt, c["end"]):
                active = c
                break
        if active is None:
            return
        s = self.s
        fnt = s.f("body_bold", 74 if self.v else 50)
        words = [w["word"] for w in active["words"]]
        space = text_size(" ", fnt)[0] + fnt.size * 0.12
        widths = [text_size(w, fnt)[0] for w in words]
        total = sum(widths) + space * (len(words) - 1)
        max_w = (self.box[2] - self.box[0]) if self.v else self.W * 0.7
        if total > max_w:  # shrink rather than overflow
            fnt = s.f("body_bold", int(fnt.size * max_w / total))
            space = text_size(" ", fnt)[0] + fnt.size * 0.12
            widths = [text_size(w, fnt)[0] for w in words]
            total = sum(widths) + space * (len(words) - 1)
        a = ease_out(prog(t, active["start"] - 0.05, 0.12))
        cx = self.cx if self.v else self.W / 2
        y = self.caption_y + 10 * (1 - a)
        pad_x, pad_y = fnt.size * 0.45, fnt.size * 0.32
        fill_rect(img, (cx - total / 2 - pad_x, y - fnt.size * 0.62 - pad_y, cx + total / 2 + pad_x,
                        y + fnt.size * 0.45 + pad_y), s.c("bg"), 0.72 * a)
        x = cx - total / 2
        for w, wd, wi in zip(words, widths, active["words"]):
            on = wi["start"] - 0.03 <= t
            colour = s.c("accent2") if (on and t < wi["end"] + 0.05) else s.c("ink")
            draw_text(img, w, fnt, colour, (x, y), "ls", alpha=a if on else 0.55 * a)
            x += wd + space


class TitleCard(BaseScene):
    def draw(self, img, t):
        s = self.s
        a = ease_out(prog(t, 0.2, 0.8))
        size = 96 if self.v else 110
        y = self.cy - 20 + 30 * (1 - a)
        for line in wrap(self.p.get("title", ""), s.f("display", size), self.box[2] - self.box[0]):
            draw_text(img, line, s.f("display", size), s.c("ink"), (self.cx, y), "mm", alpha=a)
            y += size * 1.1
        if self.p.get("subtitle"):
            draw_text(img, self.p["subtitle"], s.f("body", 40), s.c("muted"), (self.cx, y + 30), "mm",
                      alpha=ease_out(prog(t, 0.6, 0.8)))


class MapScene(BaseScene):
    credit_backing = True

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.countries = geo.load_countries(str(REPO_ROOT / "assets" / "geo" / "europe_50m.geojson"))

    def draw(self, img, t):
        s, p = self.s, self.p
        zoom_start = float(p.get("zoom_start", 1.0 if not self.v else 0.3))
        zoom_end = max(zoom_start + 1.0, self.lead + float(p.get("zoom_fraction", 0.55)) * self.speech)
        u = ease_in_out(prog(t, zoom_start, zoom_end - zoom_start))
        sv = p.get("start_view_vertical", p["start_view"]) if self.v else p["start_view"]
        ev = p.get("end_view_vertical", p["end_view"]) if self.v else p["end_view"]
        a0, a1 = ((0.5, 0.32), (0.5, 0.33)) if self.v else ((0.5, 0.52), (0.31, 0.52))
        view = geo.interpolate_view(sv, ev, u, self.W, self.H, a0, a1)
        hl = ease_in_out(prog(t, zoom_start + 0.4 * (zoom_end - zoom_start), 1.0))
        fills = {p["focus"]: lerp(s.c("land"), s.c("accent"), hl)}
        geo.draw_map(img, self.countries, view, s.c("land"), s.c("border"), fills)
        if self.v:  # fade the map out under the text area
            grad = Image.linear_gradient("L").resize((self.W, 360))
            img.paste(self.s.background().crop((0, 860, self.W, 1220)), (0, 860), grad)
            fill_rect(img, (0, 1220, self.W, self.H), s.c("bg"), 1.0)
            img.paste(self.s.background().crop((0, 1220, self.W, self.H)), (0, 1220))

        n_alpha = clamp(1 - abs(math.log(view.span / 16)) / 0.9) * 0.9
        for code, label in (p.get("neighbours") or {}).items():
            lon, lat = self.countries[code]["label_lonlat"]
            x, y = view.project(np.array([lon, lat]))
            if not (160 < x < self.W - 160 and 140 < y < (840 if self.v else self.H - 120)):
                continue
            draw_text(img, label.upper(), s.f("body_bold", 22), s.c("muted"), (x, y), "mm",
                      alpha=n_alpha, tracking=4)
        lon, lat = self.countries[p["focus"]]["label_lonlat"]
        fx, fy = view.project(np.array([lon, lat]))

        # export arrows radiating outward ("to the world")
        if p.get("arrows"):
            start = self.when(p.get("arrows_cue"), 0.3)
            d = ImageDraw.Draw(img)
            for i, bearing in enumerate(p["arrows"]):
                ua = ease_out(prog(t, start + i * 0.12, 0.9))
                if ua <= 0:
                    continue
                rad = math.radians(bearing)
                length = (520 if self.v else 640) * ua
                r0 = 150 if self.v else 190
                x0, y0 = fx + r0 * math.sin(rad), fy - r0 * math.cos(rad)
                x1, y1 = fx + (r0 + length) * math.sin(rad), fy - (r0 + length) * math.cos(rad)
                d.line((x0, y0, x1, y1), fill=s.c("accent2"), width=7)
                hx, hy = math.sin(rad), -math.cos(rad)
                px, py = -hy, hx
                tip = (x1 + hx * 22, y1 + hy * 22)
                d.polygon([tip, (x1 + px * 16, y1 + py * 16), (x1 - px * 16, y1 - py * 16)], fill=s.c("accent2"))

        draw_text(img, p.get("focus_label", "").upper(), s.f("heading", 40 if self.v else 44), s.c("ink"),
                  (fx, fy), "mm", alpha=ease_out(prog(t, zoom_end - 0.6, 0.8)) * (0.35 if p.get("markers") else 1),
                  tracking=8)
        for mk in p.get("markers", []):
            ma = ease_out(prog(t, max(self.when(mk, 0.3), zoom_end - 0.3), 0.5))
            if ma <= 0:
                continue
            mx, my = view.project(np.array([mk["lon"], mk["lat"]]))
            rr = 14 + 10 * (1 - ma)
            aa_shape(img, (mx - 26, my - 26, mx + 26, my + 26), s.c("bg"),
                     lambda d, ss: d.ellipse((0, 0, 52 * ss - 1, 52 * ss - 1), fill=255), alpha=0.6 * ma)
            aa_shape(img, (mx - rr, my - rr, mx + rr, my + rr), s.c("accent2"),
                     lambda d, ss, rr=rr: d.ellipse((0, 0, 2 * rr * ss - 1, 2 * rr * ss - 1), fill=255), alpha=ma)
            draw_text(img, mk["label"], s.f("heading", 46 if not self.v else 40), s.c("ink"),
                      (mx + 34, my), "lm", alpha=ma)
            if mk.get("sublabel"):
                draw_text(img, mk["sublabel"], s.f("body", 28), s.c("ink"), (mx + 36, my + 42), "lm", alpha=0.85 * ma)

        ta = ease_out(prog(t, 0.15, 0.6)) * (1 - ease_in_out(prog(t, zoom_start + 0.5, 0.7)))
        if p.get("title"):
            fill_rect(img, (0, self.cy - 120, self.W, self.cy + 120), s.c("bg"), 0.55 * ta)
            draw_text(img, p["title"], s.f("display", 104), s.c("ink"), (self.W / 2, self.cy), "mm", alpha=ta)

        if self.v:
            y = 960
            if p.get("headline"):
                ha = ease_out(prog(t, self.when(p.get("headline_cue"), 0.1), 0.5))
                y = draw_paragraph(img, p["headline"], s.f("display", 70), s.c("ink"), (self.box[0], y),
                                   self.box[2] - self.box[0], 1.1, alpha=ha)
            if p.get("subline"):
                sa = ease_out(prog(t, self.when(p.get("subline_cue"), 0.4), 0.5))
                draw_paragraph(img, p["subline"], s.f("body", 38), s.c("muted"), (self.box[0], y + 10),
                               self.box[2] - self.box[0], alpha=sa)
            self._callouts(img, t, self.box[0], 900, zoom_end)
        else:
            self._callouts(img, t, 1270, 330, zoom_end)

    def _callouts(self, img, t, x_base, y, zoom_end):
        s = self.s
        for i, c in enumerate(self.p.get("callouts", [])):
            # never before the camera settles; stagger if several cues already passed
            a = ease_out(prog(t, max(self.when(c), zoom_end - 0.4 + 0.35 * i), 0.6))
            step = 150 if c.get("value") else 90
            if a <= 0:
                y += step
                continue
            x = x_base + 60 * (1 - a)
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
        x_left = self.box[0]
        y = draw_paragraph(img, p.get("title", ""), s.f("display", 64), s.c("ink"), (x_left, self.box[1] + 90),
                           self.box[2] - x_left, 1.1, alpha=a0)
        draw_text(img, p.get("subtitle", ""), s.f("body", 30), s.c("muted"), (x_left + 2, y - 20), "ls", alpha=a0)
        if self.v:
            x0, x1, top = x_left, self.box[2] - 170, y + 40
            row_h = min(96, (self.box[3] - top) / len(rows))
        else:
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
            yy = top + i * row_h
            hl, ref = r["code"] == p.get("highlight"), r["code"] == p.get("reference")
            colour = s.c("accent") if hl else (s.c("ink") if ref else s.c("muted"))
            la = ease_out(prog(t, start - 0.1, 0.5))
            if self.v:
                draw_text(img, r["name"], s.f("body_bold" if hl else "body", 28),
                          s.c("ink") if (hl or ref) else s.c("muted"), (x0, yy + 26), "ls", alpha=la)
                bar = (yy + 36, yy + row_h - 14)
            else:
                draw_text(img, r["name"], s.f("body_bold" if hl else "body", 30),
                          s.c("ink") if (hl or ref) else s.c("muted"), (x0 - 24, yy + row_h * 0.42), "rm", alpha=la)
                bar = (yy + row_h * 0.14, yy + row_h * 0.72)
            w = (x1 - x0) * r["value"] / vmax * u
            fill_rect(img, (x0, bar[0], x0 + w, bar[1]), colour, 0.95 if hl else 0.75)
            if u > 0.02:
                draw_text(img, f"${r['value'] * u:,.0f}", s.f("body_bold", 28),
                          s.c("accent2") if hl else s.c("ink"), (x0 + w + 14, (bar[0] + bar[1]) / 2), "lm", alpha=u)
        if p.get("callout"):
            ca = ease_out(prog(t, self.when(p.get("callout_cue", {"cue": "That is"})) + 0.3, 0.7))
            if self.v:
                draw_paragraph(img, p["callout"], s.f("heading", 44), s.c("accent2"),
                               (x_left, self.box[3] - 10), self.box[2] - x_left, alpha=ca)
            else:
                draw_text(img, p["callout"], s.f("heading", 46), s.c("accent2"), (self.W - 120, 210), "rm", alpha=ca)


class KineticTextScene(BaseScene):
    """Stacked lines that rise in on cues. A line may be struck through on a later cue."""

    def draw(self, img, t):
        s = self.s
        x = self.box[0] + (0 if self.v else 80)
        max_w = self.box[2] - x
        blocks = []
        for ln in self.p["lines"]:
            size = ln.get("size", 60) * (0.82 if self.v else 1.0)
            fnt = s.f(ln.get("style", "body"), size)
            lines = wrap(ln["text"], fnt, max_w)
            while any(text_size(li, fnt)[0] > max_w for li in lines) and size > 24:
                size *= 0.92
                fnt = s.f(ln.get("style", "body"), size)
                lines = wrap(ln["text"], fnt, max_w)
            blocks.append((ln, fnt, lines, int(size * 1.22) * len(lines) + int(size * 0.18)))
        total = sum(b[3] for b in blocks)
        y = self.cy - total / 2
        first = self.when(self.p["lines"][0], 0.0)
        bar = ease_out(prog(t, first, 0.8))
        fill_rect(img, (x - 50, y, x - 42, y + total * bar), s.c("accent"))
        for ln, fnt, lines, h in blocks:
            start = self.when(ln, 0.0)
            a = ease_out(prog(t, start, 0.45))
            strike = ease_out(prog(t, self.when(ln["strike_cue"]), 0.3)) if ln.get("strike_cue") else 0.0
            lh = h / len(lines)
            for i, li in enumerate(lines):
                cy = y + lh * (i + 0.5) + 26 * (1 - a)
                draw_text(img, li, fnt, s.c(ln.get("color", "ink")), (x, cy), "lm", alpha=a * (1 - 0.55 * strike))
                if strike > 0:
                    w = text_size(li, fnt)[0] * strike
                    th = max(4, fnt.size * 0.09)
                    fill_rect(img, (x - 6, cy - th / 2, x - 6 + w + 12, cy + th / 2), s.c("accent"))
            y += h


class RingStatScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        value = float(p["value"])
        if self.v:
            cx, cy, r, thick = self.cx, self.box[1] + 330, 250, 52
        else:
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
        disp = str(p.get("display", ""))
        decimals = len(disp.split(".")[1].rstrip("%")) if "." in disp else 0
        draw_text(img, f"{value * u:.{decimals}f}%", s.f("display", 116 if not self.v else 104), s.c("ink"),
                  (cx, cy), "mm", alpha=a0 * ease_out(prog(t, start - 0.3, 0.3)))
        la = ease_out(prog(t, start + 0.8, 0.7))
        if self.v:
            y = draw_paragraph(img, p.get("sublabel", ""), s.f("heading", 58), s.c("ink"),
                               (self.box[0], cy + r + 110), self.box[2] - self.box[0], alpha=la)
            draw_paragraph(img, p.get("label", ""), s.f("body", 40), s.c("muted"), (self.box[0], y + 6),
                           self.box[2] - self.box[0], alpha=la)
        else:
            y = draw_paragraph(img, p.get("sublabel", ""), s.f("heading", 58), s.c("ink"), (1020, 500), 780,
                               alpha=la)
            draw_paragraph(img, p.get("label", ""), s.f("body", 40), s.c("muted"), (1022, y + 6), 780, alpha=la)


class PictogramScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        n = int(p.get("columns", 3))
        k = int(round(float(p["fraction"]) * n))
        if self.v:
            size, gap = 190, 50
            x0 = self.cx - (n * size + (n - 1) * gap) / 2
            y0 = self.box[1] + 120
        else:
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
        if self.v:
            tx, ty, tw = self.box[0], y0 + size * 1.6 + 200, self.box[2] - self.box[0]
        else:
            tx, ty, tw = 986, 480, 800
        draw_text(img, str(p.get("headline", "")), s.f("display", 150), s.c("accent2"), (tx - 6, ty), "ls", alpha=ta)
        y = draw_paragraph(img, p.get("label", ""), s.f("heading", 46), s.c("ink"), (tx, ty + 90), tw, alpha=ta)
        draw_paragraph(img, p.get("sublabel", ""), s.f("body", 32), s.c("muted"), (tx + 2, y + 14), tw,
                       alpha=ease_out(prog(t, start + 2.2, 0.7)))


class RankingScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        items = list(p["items"])
        a0 = ease_out(prog(t, 0.2, 0.6))
        x0 = self.box[0]
        y = draw_paragraph(img, p.get("title", ""), s.f("display", 64), s.c("ink"), (x0, self.box[1] + 110),
                           self.box[2] - x0, 1.1, alpha=a0)
        draw_paragraph(img, p.get("subtitle", ""), s.f("body", 30), s.c("muted"), (x0 + 2, y - 14),
                       self.box[2] - x0, alpha=a0)
        top, row_h = (y + 60, 104) if self.v else (380, 108)
        width = (self.box[2] - x0) if self.v else 1100
        start = self.when(p.get("cue"), 0.0)
        if p.get("badge") and not self.v:
            ba = ease_out(prog(t, start + len(items) * 0.45 + 0.6, 0.8))
            draw_text(img, p["badge"], s.f("display", 190), s.c("accent2"), (self.W - 140, 640), "rs", alpha=ba)
            draw_text(img, p.get("badge_label", "").upper(), s.f("body_bold", 28), s.c("muted"),
                      (self.W - 146, 700), "rs", alpha=ba, tracking=4)
        for rank in range(len(items), 0, -1):
            name = items[rank - 1]
            order = len(items) - rank
            a = ease_out(prog(t, start + order * 0.45, 0.5))
            yy = top + (rank - 1) * row_h
            hl = name == p.get("highlight")
            if hl:
                sweep = ease_in_out(prog(t, start + order * 0.45 + 0.3, 0.8))
                fill_rect(img, (x0, yy, x0 + width * sweep, yy + row_h - 18), s.c("accent"), 0.9)
            mid = yy + (row_h - 18) / 2 + 20 * (1 - a)
            draw_text(img, f"{rank:02d}", s.f("display", 56), s.c("ink") if hl else s.c("muted"), (x0 + 30, mid),
                      "lm", alpha=a)
            draw_text(img, name, s.f("heading" if hl else "body", 50), s.c("ink"), (x0 + 170, mid), "lm", alpha=a)


class BigNumberScene(BaseScene):
    """A single figure that counts up to its dossier value, with label and context."""

    def draw(self, img, t):
        s, p = self.s, self.p
        disp = str(p["display"])
        m = NUM.search(disp)
        prefix, suffix = (disp[:m.start()], disp[m.end():]) if m else ("", "")
        decimals = len(m.group().split(".")[1]) if (m and "." in m.group()) else 0
        value = float(p["value"])
        start = self.when(p.get("cue"), 0.1)
        u = ease_out(prog(t, start, 1.4)) if p.get("count", True) else (1.0 if t >= start - 0.2 else 0.0)
        shown = disp if u >= 1 else f"{prefix}{value * u:,.{decimals}f}{suffix}"
        a = ease_out(prog(t, start - 0.2, 0.4))
        size = 190 if self.v else 230
        while text_size(disp, s.f("display", size))[0] > (self.box[2] - self.box[0]) and size > 60:
            size -= 8
        y = self.cy - (60 if self.v else 40)
        if p.get("kicker"):
            draw_text(img, p["kicker"].upper(), s.f("body_bold", 30), s.c("muted"), (self.cx, y - size * 0.75),
                      "mm", alpha=a, tracking=5)
        draw_text(img, shown, s.f("display", size), s.c("accent2"), (self.cx, y), "mm", alpha=a)
        la = ease_out(prog(t, start + 0.9, 0.6))
        yy = y + size * 0.78
        for line in wrap(p.get("label", ""), s.f("heading", 52), self.box[2] - self.box[0]):
            draw_text(img, line, s.f("heading", 52), s.c("ink"), (self.cx, yy), "mm", alpha=la)
            yy += 62
        if p.get("sublabel"):
            for line in wrap(p["sublabel"], s.f("body", 34), self.box[2] - self.box[0]):
                draw_text(img, line, s.f("body", 34), s.c("muted"), (self.cx, yy + 10), "mm",
                          alpha=ease_out(prog(t, start + 1.4, 0.6)))
                yy += 44


class TimelineScene(BaseScene):
    """An axis drawn from start_year to 'today' with dated markers revealed on cues."""

    def draw(self, img, t):
        s, p = self.s, self.p
        y0, y1 = float(p["start_year"]), float(p["end_year"])
        start = self.when(p.get("cue"), 0.0)
        grow = ease_in_out(prog(t, start, float(p.get("draw_seconds", 2.2))))
        a0 = ease_out(prog(t, 0.2, 0.5))
        if p.get("title"):
            draw_text(img, p["title"], s.f("display", 60), s.c("ink"), (self.box[0], self.box[1] + 100), "ls",
                      alpha=a0)
        if self.v:
            ax, top, bot = self.box[0] + 60, self.box[1] + 190, self.box[3] - 40
            pos = lambda yr: top + (bot - top) * (yr - y0) / (y1 - y0)  # noqa: E731
            fill_rect(img, (ax - 3, top, ax + 3, top + (bot - top) * grow), s.c("border"))
        else:
            ax0, ax1, ay = 200, self.W - 200, self.cy + 40
            pos = lambda yr: ax0 + (ax1 - ax0) * (yr - y0) / (y1 - y0)  # noqa: E731
            fill_rect(img, (ax0, ay - 3, ax0 + (ax1 - ax0) * grow, ay + 3), s.c("border"))
        tick = int(p.get("tick_every", 50))
        for yr in range(int(math.ceil(y0 / tick) * tick), int(y1) + 1, tick):
            ta = a0 * (1.0 if (yr - y0) / (y1 - y0) <= grow else 0.0)
            if self.v:
                fill_rect(img, (ax - 12, pos(yr) - 1, ax + 12, pos(yr) + 1), s.c("muted"), ta)
                draw_text(img, str(yr), s.f("body", 24), s.c("muted"), (ax - 24, pos(yr)), "rm", alpha=ta)
            else:
                fill_rect(img, (pos(yr) - 1, ay - 12, pos(yr) + 1, ay + 12), s.c("muted"), ta)
                draw_text(img, str(yr), s.f("body", 24), s.c("muted"), (pos(yr), ay + 44), "mm", alpha=ta)
        end_a = ease_out(prog(t, start + float(p.get("draw_seconds", 2.2)) - 0.3, 0.5))
        crowded = any((float(it["year"]) - y0) / (y1 - y0) > 0.8 for it in p.get("items", []))
        if p.get("end_label") and not (crowded and not self.v):
            if self.v:
                draw_text(img, p["end_label"].upper(), s.f("body_bold", 28), s.c("ink"), (ax + 30, bot), "lm",
                          alpha=end_a, tracking=3)
            else:
                draw_text(img, p["end_label"].upper(), s.f("body_bold", 28), s.c("ink"), (ax1, ay - 40), "rm",
                          alpha=end_a, tracking=3)
        prev_text_x = -1e9
        for item in p.get("items", []):
            ia = ease_out(prog(t, self.when(item, 0.1), 0.5))
            yr = float(item["year"])
            if self.v:
                py = pos(yr)
                aa_shape(img, (ax - 16, py - 16, ax + 16, py + 16), s.c("accent"),
                         lambda d, ss: d.ellipse((0, 0, 32 * ss - 1, 32 * ss - 1), fill=255), alpha=ia)
                draw_text(img, str(item.get("display", int(yr))), s.f("display", 110), s.c("accent2"),
                          (ax + 50, py + 36), "ls", alpha=ia)
                draw_paragraph(img, item.get("label", ""), s.f("heading", 40), s.c("ink"), (ax + 54, py + 96),
                               self.box[2] - ax - 54, alpha=ia)
            else:
                px = pos(yr)
                aa_shape(img, (px - 16, ay - 16, px + 16, ay + 16), s.c("accent"),
                         lambda d, ss: d.ellipse((0, 0, 32 * ss - 1, 32 * ss - 1), fill=255), alpha=ia)
                block_w = 520
                # keep text blocks apart and inside the frame; a leader line links text to its dot
                tx = max(px - 10, prev_text_x + block_w + 40)
                tx = min(tx, self.W - 120 - block_w)
                prev_text_x = tx
                if abs(tx - (px - 10)) > 4:
                    fill_rect(img, (min(px, tx + 10), ay - 230, max(px, tx + 10) + 2, ay - 228), s.c("border"), ia)
                    fill_rect(img, (px - 1, ay - 230, px + 1, ay - 16), s.c("border"), ia)
                draw_text(img, str(item.get("display", int(yr))), s.f("display", 150), s.c("accent2"),
                          (tx, ay - 70), "ls", alpha=ia)
                draw_paragraph(img, item.get("label", ""), s.f("heading", 40), s.c("ink"), (tx + 10, ay + 120),
                               block_w, alpha=ia)
        if p.get("footer"):
            fa = ease_out(prog(t, self.when(p.get("footer_cue"), 0.7), 0.5))
            if self.v:
                draw_paragraph(img, p["footer"], s.f("heading", 46), s.c("accent"), (ax + 54, bot - 140),
                               self.box[2] - ax - 54, alpha=fa)
            else:
                draw_text(img, p["footer"], s.f("heading", 50), s.c("accent"), (self.W - 200, ay + 230), "rs",
                          alpha=fa)


class EndCardScene(BaseScene):
    def draw(self, img, t):
        s, p = self.s, self.p
        words = p.get("words", [])
        brand_t = self.when(p.get("brand_cue", {"cue": "The Hidden Economics"}), 0.85)
        out = ease_in_out(prog(t, brand_t - 0.6, 0.6))
        size, step = (96, 118) if self.v else (110, 130)
        y = self.cy - step * (len(words) - 1) / 2
        for i, w in enumerate(words):
            a = ease_out(prog(t, self.when({"cue": w.rstrip(".")}, 0.0), 0.45)) * (1 - out)
            wsize = size
            while text_size(w, s.f("display", wsize))[0] > (self.box[2] - self.box[0]) and wsize > 30:
                wsize -= 4
            draw_text(img, w, s.f("display", wsize), s.c("accent2") if i == len(words) - 1 else s.c("ink"),
                      (self.cx, y + i * step + 20 * (1 - a)), "mm", alpha=a)
        ba = ease_out(prog(t, brand_t, 0.8))
        bsize = 62 if self.v else 84
        brand = p.get("brand", "").upper()
        tw, _ = text_size(brand, s.f("display", bsize), tracking=8)
        while tw > (self.box[2] - self.box[0]) and bsize > 30:
            bsize -= 4
            tw, _ = text_size(brand, s.f("display", bsize), tracking=8)
        fill_rect(img, (self.cx - tw / 2 * ba, self.cy - bsize - 10, self.cx + tw / 2 * ba, self.cy - bsize - 6),
                  s.c("accent"))
        draw_text(img, brand, s.f("display", bsize), s.c("ink"), (self.cx, self.cy), "mm", alpha=ba, tracking=8)
        teaser_t = max(self.when(p.get("teaser_cue", {"cue": "full"}), 0.5), brand_t)
        yy = self.cy + bsize + 40
        for line in wrap(p.get("teaser", ""), s.f("body", 34), self.box[2] - self.box[0]):
            draw_text(img, line, s.f("body", 34), s.c("muted"), (self.cx, yy), "mm",
                      alpha=ease_out(prog(t, teaser_t, 0.8)))
            yy += 46


class LineChartScene(BaseScene):
    """Time series drawn left to right; highlighted series in accent, end labels follow the pen."""

    def draw(self, img, t):
        s, p = self.s, self.p
        series = p["series"]
        a0 = ease_out(prog(t, 0.2, 0.6))
        x_left = self.box[0]
        y = draw_paragraph(img, p.get("title", ""), s.f("display", 60 if not self.v else 56), s.c("ink"),
                           (x_left, self.box[1] + 90), self.box[2] - x_left, 1.1, alpha=a0)
        draw_text(img, p.get("subtitle", ""), s.f("body", 30), s.c("muted"), (x_left + 2, y - 18), "ls", alpha=a0)
        if self.v:
            x0, x1, y0, y1 = x_left + 70, self.box[2] - 230, y + 60, self.box[3] - 60
        else:
            x0, x1, y0, y1 = 260, 1500, 300, 900
        years = [pt["year"] for pt in series[0]["points"]]
        vmax = max(pt["value"] for sr in series for pt in sr["points"])
        step = 20000 if vmax > 60000 else 10000
        top = math.ceil(vmax / step) * step
        X = lambda yr: x0 + (x1 - x0) * (yr - years[0]) / (years[-1] - years[0])  # noqa: E731
        Y = lambda v: y1 - (y1 - y0) * v / top  # noqa: E731
        for gv in range(0, int(top) + 1, step):
            fill_rect(img, (x0, Y(gv), x1, Y(gv) + 1), s.c("border"), 0.6 * a0)
            draw_text(img, f"${gv // 1000}k", s.f("body", 22), s.c("muted"), (x0 - 14, Y(gv)), "rm", alpha=a0)
        for yr in years:
            if yr % 5 == 0 or yr == years[-1]:
                draw_text(img, str(yr), s.f("body", 22), s.c("muted"), (X(yr), y1 + 30), "mm", alpha=a0)
        start = self.when(p.get("cue"), 0.05)
        u = ease_in_out(prog(t, start, float(p.get("draw_seconds", 4.0))))
        pos = u * (len(years) - 1)
        n_full = int(pos)
        frac = pos - n_full
        box = (x0 - 10, y0 - 20, x1 + 10, y1 + 10)
        order = sorted(series, key=lambda sr: sr["code"] == p.get("highlight"))
        labels = []
        for sr in order:
            pts = [(X(pt["year"]), Y(pt["value"])) for pt in sr["points"]]
            drawn = pts[: n_full + 1]
            if n_full + 1 < len(pts):
                (ax, ay), (bx, by) = pts[n_full], pts[n_full + 1]
                drawn.append((ax + (bx - ax) * frac, ay + (by - ay) * frac))
            if len(drawn) < 2 or u <= 0:
                continue
            hl = sr["code"] == p.get("highlight")
            ref = sr["code"] in p.get("emphasis", [])
            colour = s.c("accent") if hl else (s.c("ink") if ref else s.c("muted"))
            width = 7 if hl else 4
            rel = [((x - box[0]), (yy - box[1])) for x, yy in drawn]

            def line(d, ss, rel=rel, width=width):
                d.line([(x * ss, yy * ss) for x, yy in rel], fill=255, width=width * ss, joint="curve")
            aa_shape(img, box, colour, line, ss=2)
            ex, ey = drawn[-1]
            idx = min(len(sr["points"]) - 1, n_full + (1 if frac > 0.5 else 0))
            labels.append([ey, sr["name"], sr["points"][idx]["value"], colour, hl])
        labels.sort(key=lambda lb: lb[0])
        for i in range(1, len(labels)):           # keep end labels from overlapping
            if labels[i][0] - labels[i - 1][0] < 44:
                labels[i][0] = labels[i - 1][0] + 44
        ex = X(years[0]) + (X(years[-1]) - X(years[0])) * u
        for ly, name, val, colour, hl in labels:
            draw_text(img, name, s.f("body_bold" if hl else "body", 26), colour if hl else s.c("ink"),
                      (ex + 16, ly - 4), "ls", alpha=u)
            draw_text(img, f"${val:,.0f}", s.f("body", 22), s.c("accent2") if hl else s.c("muted"),
                      (ex + 16, ly + 22), "ls", alpha=u)
        if p.get("callout"):
            ca = ease_out(prog(t, self.when(p.get("callout_cue"), 0.7), 0.6))
            if self.v:
                draw_paragraph(img, p["callout"], s.f("heading", 42), s.c("accent2"), (x_left, self.box[3] + 10),
                               self.box[2] - x_left, alpha=ca)
            else:
                draw_text(img, p["callout"], s.f("heading", 44), s.c("accent2"), (self.W - 120, 210), "rm", alpha=ca)


class SplitCompareScene(BaseScene):
    """Two states side by side (16:9) or stacked (9:16): before/after, then/now, A vs B."""

    def draw(self, img, t):
        s, p = self.s, self.p
        a0 = ease_out(prog(t, 0.2, 0.5))
        if p.get("title"):
            draw_paragraph(img, p["title"], s.f("display", 56), s.c("ink"), (self.box[0], self.box[1] + 90),
                           self.box[2] - self.box[0], alpha=a0)
        sides = [p["left"], p["right"]]
        if self.v:
            centres = [(self.cx, self.box[1] + 300), (self.cx, self.box[1] + 690)]
        else:
            centres = [(self.W * 0.29, self.cy + 30), (self.W * 0.71, self.cy + 30)]
        div = ease_out(prog(t, self.when(sides[1], 0.5) - 0.3, 0.5))
        if self.v:
            fill_rect(img, (self.cx - 160 * div, self.box[1] + 495, self.cx + 160 * div, self.box[1] + 499), s.c("accent"))
        else:
            fill_rect(img, (self.W / 2 - 2, self.cy - 200 * div + 30, self.W / 2 + 2, self.cy + 200 * div + 30), s.c("accent"))
        for i, (side, (cx, cy)) in enumerate(zip(sides, centres)):
            a = ease_out(prog(t, self.when(side, 0.05 if i == 0 else 0.5), 0.5))
            dim = 0.45 if (i == 0 and div >= 1 and p.get("dim_left_after", True)) else 1.0
            draw_text(img, side.get("kicker", "").upper(), s.f("body_bold", 28), s.c("muted"), (cx, cy - 130), "mm",
                      alpha=a * dim, tracking=4)
            size = 150 if self.v else 170
            val = str(side.get("value", ""))
            while text_size(val, s.f("display", size))[0] > (self.box[2] - self.box[0] - 40 if self.v else 760) \
                    and size > 40:
                size -= 6
            draw_text(img, val, s.f("display", size), s.c("accent2") if i == 1 else s.c("ink"),
                      (cx, cy - 10 + 20 * (1 - a)), "mm", alpha=a * dim)
            yy = cy + 100
            for line in wrap(side.get("label", ""), s.f("heading", 40), 760 if not self.v else self.box[2] - self.box[0]):
                draw_text(img, line, s.f("heading", 40), s.c("ink"), (cx, yy), "mm", alpha=a * dim)
                yy += 50


class ActTitleScene(BaseScene):
    """Chapter card between acts: number, title, optional one-line promise. Usually silent."""

    def draw(self, img, t):
        s, p = self.s, self.p
        a = ease_out(prog(t, 0.15, 0.6))
        r = ease_in_out(prog(t, 0.3, 0.8))
        draw_text(img, str(p.get("number", "")).upper(), s.f("body_bold", 30), s.c("accent"),
                  (self.cx, self.cy - 120), "mm", alpha=a, tracking=8)
        size = 120 if not self.v else 104
        title = p.get("title", "")
        while text_size(title, s.f("display", size))[0] > (self.box[2] - self.box[0]) and size > 40:
            size -= 6
        draw_text(img, title, s.f("display", size), s.c("ink"), (self.cx, self.cy + 10 * (1 - a)), "mm", alpha=a)
        fill_rect(img, (self.cx - 120 * r, self.cy + size * 0.6, self.cx + 120 * r, self.cy + size * 0.6 + 4),
                  s.c("accent"))
        if p.get("subtitle"):
            yy = self.cy + size * 0.6 + 60
            for line in wrap(p["subtitle"], s.f("body", 36), self.box[2] - self.box[0]):
                draw_text(img, line, s.f("body", 36), s.c("muted"), (self.cx, yy), "mm",
                          alpha=ease_out(prog(t, 0.6, 0.6)))
                yy += 46


SCENES = {"title_card": TitleCard, "map": MapScene, "bar_chart": BarChartScene,
          "kinetic_text": KineticTextScene, "ring_stat": RingStatScene, "pictogram": PictogramScene,
          "ranking": RankingScene, "end_card": EndCardScene, "big_number": BigNumberScene,
          "timeline": TimelineScene, "line_chart": LineChartScene, "split_compare": SplitCompareScene,
          "act_title": ActTitleScene}
