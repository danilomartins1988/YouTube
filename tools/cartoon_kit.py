"""Shared helpers for cartoon-first storyboards (engine_cartoon worlds, presenter boards, kinetic text).

Import it in a generator: `from cartoon_kit import *`, append scenes with the helpers, then `write(OUT, header)`.
First used by Episode 11; Episode 10's generator holds the same helpers inline.
"""
from __future__ import annotations

import math

import yaml

INTER = ["font:inter"]
GEO = ["geo:remotion_world", "font:inter"]
BOARD = {"x": 470, "y": 230, "w": 1370, "h": 800}
C = lambda cue, off=None: ({"cue": cue, "offset": off} if off is not None else {"cue": cue})
scenes: list[dict] = []


def add(id_, segment, type_, params, sources=(), assets=INTER, sfx=None):
    if type_ == "engine_draw":
        for st in params.get("strokes", []):
            d = st["d"]
            if "kind" not in st:
                st["kind"] = "box" if d.rstrip().endswith("Z") and d.count(" L ") == 3 else ("arrow" if " Q " in d and d.count("M ") == 2 else "stroke")
    s = {"id": id_, "segment": segment, "type": type_, "params": params}
    if sfx:
        s["sfx"] = sfx
    if sources:
        s["sources"] = list(sources)
    s["assets"] = list(assets)
    scenes.append(s)


def cart(id_, seg, params, sources=(), sfx=None):
    params.setdefault("fish", 3)
    add(id_, seg, "engine_cartoon", params, sources, sfx=sfx)


def card(id_, seg, title, sub):
    add(id_, seg, "act_title", {"number": "", "title": title, "subtitle": sub, "min_seconds": 5.4}, sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


def kinetic(id_, seg, lines, chapter=None):
    p = {"align": "center", "lines": [{"text": tx, "size": sz, "cue": cu, **({"color": co} if co else {}), **({"style": "body"} if st else {})}
                                      for tx, sz, cu, co, st in lines]}
    if chapter:
        p["chapter"] = chapter
    add(id_, seg, "kinetic_text", p)


def rect(x, y, w, h):
    return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"


def arrow(a, b, bend=0.0):
    mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
    ang = math.atan2(b[1] - my, b[0] - mx)
    h1 = (b[0] - 24 * math.cos(ang - 0.45), b[1] - 24 * math.sin(ang - 0.45))
    h2 = (b[0] - 24 * math.cos(ang + 0.45), b[1] - 24 * math.sin(ang + 0.45))
    return f"M {a[0]} {a[1]} Q {mx:.0f} {my:.0f} {b[0]} {b[1]} M {h1[0]:.0f} {h1[1]:.0f} L {b[0]} {b[1]} L {h2[0]:.0f} {h2[1]:.0f}"


def lbl(text, x, y, size=30, color="ink", anchor="middle"):
    return {"text": text, "x": x, "y": y, "size": size, "color": color, "anchor": anchor}


def dot(x, y):
    return f"M {x} {y} L {x} {y}"


def island(x=1300, w=440, **kw):
    return {"kind": "island", "x": x, "w": w, "text": "ANGUILLA", **kw}


def letters(x=1260, y=150, at=0.0, size=150, **kw):
    return {"kind": "letters", "text": ".ai", "x": x, "y": y, "at": at, "size": size, **kw}


def coins(x, y, to, at, rate=4, until=None, shape=None):
    c = {"kind": "coins", "x": x, "y": y, "to": to, "at": at, "rate": rate}
    if shape:
        c["shape"] = shape
    if until is not None:
        c["until"] = until
    return c


def office(x, text, color="purple", at=None, scale=1.0):
    o = {"kind": "office", "x": x, "text": text, "color": color, "scale": scale}
    if at is not None:
        o["at"] = at
    return o


def co(text, x, y, at, color="white", sub=None, tail=None, until=None, size=None, screen=False):
    c = {"text": text, "x": x, "y": y, "at": at, "color": color}
    for k, v in (("sub", sub), ("tail", tail), ("until", until), ("size", size)):
        if v is not None:
            c[k] = v
    if screen:
        c["screen"] = True
    return c



def ship(kind="cargo", x=960, flag=None, crew=0, **kw):
    a = {"kind": kind, "x": x, **kw}
    if flag is not None:
        a["flag"] = flag
    if crew:
        a["crew"] = crew
    return a


def write(out, header):
    for s in scenes:
        d = s["params"].pop("coasts_dark", None)
        if d is not None:
            s["params"].setdefault("coasts", {})["darkAt"] = d
    out.write_text(header + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
    print(f"{len(scenes)} scenes -> {out}")


def stage(id_, seg, params, sources=(), sfx=None):
    """A CartoonStage world (topic-specific sets + items) rendered through the engine_cartoon scene type."""
    add(id_, seg, "engine_cartoon", params, sources, sfx=sfx)


def it(kind, **kw):
    """Shorthand for a CartoonStage item."""
    return {"kind": kind, **kw}
