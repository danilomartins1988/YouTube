"""Shared helpers for the "Before You Buy" series storyboards (docs/series/BEFORE_YOU_BUY.md).

Builds on cartoon_kit (stage/it/add/card/kinetic/write). Series pieces live in CartoonStage.tsx:
`moneymachine` set and the `pricedin`, `riskscale`, `editionstamp`, `scorecard` items. Every edition is dated on screen
(EDITION + stamp()) at the hook, the priced-in section and the end, so a quarterly refresh only swaps numbers.
Usage in a company generator:
    from byb_kit import *
    set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q4 FY2026 (SEP 26, 2026)")
    ... scenes ...
    write(OUT, header)
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F401,F403
from cartoon_kit import BOARD, C, add, it, stage, lbl, rect, arrow  # noqa: E402

EDITION = {"text": "DATA AS OF", "sub": ""}
def Z(s, x0=-1600, x1=4600, **kw):
    return {"set": s, "x0": x0, "x1": x1, **kw}


def set_edition(text: str, sub: str) -> None:
    EDITION.update(text=text, sub=sub)


def stamp(x=1500, y=170, at=0.6, **kw):
    """The edition stamp (rubber stamp slams in)."""
    return it("editionstamp", x=x, y=y, at=at, text=EDITION["text"], sub=EDITION["sub"], **kw)


def buddy(x, y=860, **kw):
    """The series mascot (the chip buddy from the engine, relabelled per company)."""
    return it("chipbuddy", x=x, y=y, **kw)


def machine(segments, name, out="CASH", signs=None, **kw):
    """The MONEY MACHINE zone: segments = [(label, value, color, at)]; pipe thickness follows value."""
    segs = [{"label": l, "value": v, **({"color": c} if c else {}), **({"at": a} if a is not None else {})} for l, v, c, a in segments]
    kw.setdefault("x0", -400); kw.setdefault("x1", 3000); kw.setdefault("mx", 1400)
    z = Z("moneymachine", segments=segs, name=name, out=out, **kw)
    if signs:
        z["signs"] = signs
    return z


def gauge(low, high, inputs, lenses=None, base="FREE CASH FLOW", title="WHAT'S PRICED IN", note="OUR ILLUSTRATION · NOT A VALUATION",
          max_=25, x=820, y=520, at=0.2, **kw):
    """The priced-in calculator: low/high = (label, value, at, text)."""
    n = lambda q: {"label": q[0], "value": q[1], "at": q[2], **({"text": q[3]} if len(q) > 3 else {})}
    d = dict(x=x, y=y, at=at, low=n(low), high=n(high), inputs=inputs, base=base, title=title, note=note, max=max_)
    if lenses:
        d["lenses"] = [{"label": l, "value": v, **({"at": a} if a is not None else {})} for l, v, a in lenses]
    return it("pricedin", **{**d, **kw})


def scale(risks, upside, title="THE SCALE", **kw):
    """Risk vs upside balance: lists of (text, at)."""
    return it("riskscale", risks=[{"text": t, "at": a} for t, a in risks], upside=[{"text": t, "at": a} for t, a in upside], title=title, **kw)


def scorecard(rows, title="3 NUMBERS TO WATCH", **kw):
    """End card: rows = (label, value, at); edition line from EDITION."""
    return it("scorecard", rows=[{"label": l, "value": v, "at": a} for l, v, a in rows], title=title,
              stamp=f"{EDITION['text']} · {EDITION['sub']}", **kw)


def board(id_, seg, title, draw_start, strokes, point_at, point_target, sources=()):
    """A presenter board (engine_draw) with the series defaults."""
    add(id_, seg, "engine_draw", {
        "title": title, "board": BOARD, "draw_start": draw_start, "speed": 1400, "push": 0.003,
        "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3}, "strokes": strokes,
        "actions": [{"kind": "point", "at": point_at, "dur": 1.4, "target": point_target}],
        "scale": 0.86, "floor": 1040}, sources=sources)


def bar(x, w, base_y, top_y, color, start, label, label_size=22):
    """A bar stroke for presenter boards (kind: bar)."""
    return {"d": f"M {x} {base_y} L {x} {top_y} L {x + w} {top_y} L {x + w} {base_y} Z", "color": color, "width": 4, "fill": color,
            "fillOpacity": 0.4, "kind": "bar", "start": start, "label": lbl(label, x + w / 2, top_y - 18, label_size, color)}


def disclaimer(id_, seg, at_cue, company="THE COMPANY", sources=()):
    """The series disclaimer scene (right after the hook): chip city + edition stamp."""
    stage(id_, seg, {
        "zones": [Z("chipcity", signs=["NOT FINANCIAL ADVICE", "FILINGS ONLY", "OUR MATH · LABELLED", "DATED EDITION"])], "worldW": 2400,
        "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": 1.0, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
        "items": [it("letters", x=1000, y=150, text="NOT FINANCIAL ADVICE", at=0.2, size=64, color="gold"),
                  it("sign", x=1000, y=300, text=f"{company} FILINGS + OUR MATH, DATED", at=at_cue, color="#BBDEFB", size=32),
                  stamp(1000, 450, at=at_cue, scale=1.1),
                  buddy(600, 860, at=0.3, mood="cool", hop=16), buddy(1450, 860, at=0.5, mood="happy", color="#FF9F1C", hop=22)]},
        sources=sources)
