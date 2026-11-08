"""Generates projects/the-machine-only-one-company-can-build/deliverables/documentary/storyboard.yaml (Episode 08).

Bespoke CartoonStage worlds (Dutch town with windmill and bikes, a lithography clean room, the tin-plasma light source,
mirrors in a vacuum, a school bus for scale, an export barrier) plus presenter boards, the exploded machine and maps. Times are narration cues
({cue: "..."}) wherever possible. Run: python tools/gen_asml_storyboard.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parents[1] / "projects/the-machine-only-one-company-can-build/deliverables/documentary/storyboard.yaml"
INTER = ["font:inter"]
GEO = ["geo:remotion_world", "font:inter"]
BOARD = {"x": 470, "y": 230, "w": 1370, "h": 800}
C = lambda cue, off=None: ({"cue": cue, "offset": off} if off is not None else {"cue": cue})

LL = {"veldhoven": [5.43, 51.42], "oberkochen": [10.10, 48.78], "wetzlar": [8.50, 50.55], "sandiego": [-117.16, 32.72],
      "hsinchu": [120.99, 24.78], "hwaseong": [127.0, 37.2], "hillsboro": [-122.99, 45.52], "shanghai": [121.47, 31.23]}

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


def card(id_, seg, number, title, sub):
    add(id_, seg, "act_title", {"number": "", "title": title, "subtitle": sub, "min_seconds": 5.4}, sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


def question(id_, seg, chapter, q, why, q_cue, why_cue):
    add(id_, seg, "kinetic_text", {"align": "center", "chapter": chapter, "lines": [
        {"text": "THE QUESTION", "size": 34, "style": "body", "color": "muted", "cue": q_cue},
        {"text": q, "size": 64, "color": "accent", "cue": q_cue, "offset": 0.4},
        {"text": "WHY IT MATTERS", "size": 34, "style": "body", "color": "muted", "cue": why_cue},
        {"text": why, "size": 48, "style": "body", "cue": why_cue, "offset": 0.4}]})


def kinetic(id_, seg, lines, chapter=None):
    p = {"align": "center", "lines": [{"text": tx, "size": sz, "cue": cu, **({"color": co} if co else {}), **({"style": "body"} if st else {})}
                                      for tx, sz, cu, co, st in lines]}
    if chapter:
        p["chapter"] = chapter
    add(id_, seg, "kinetic_text", p)


def stage(id_, seg, params, sources=(), sfx=None):
    """A bespoke CartoonStage world (Dutch town, clean room, airport...)."""
    add(id_, seg, "engine_cartoon", params, sources, sfx=sfx)


def it(kind, **kw):
    return {"kind": kind, **kw}


def co(text, x, y, at, color="white", sub=None, until=None, size=None, screen=False):
    c = {"text": text, "x": x, "y": y, "at": at, "color": color}
    for k, v in (("sub", sub), ("until", until), ("size", size)):
        if v is not None:
            c[k] = v
    if screen:
        c["screen"] = True
    return c


F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
FAB = lambda x0=-1600, x1=4600, **kw: Z("fab", x0, x1, **kw)
DUTCH = lambda x0=-1600, x1=4600, **kw: Z("dutch", x0, x1, **kw)


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def suits(xs, pose="stand", at=0.2):
    return crowd(xs, pose, at=at, suit=True, scale=1.0)


def rect(x, y, w, h):
    return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"


def circle(cx, cy, r):
    return f"M {cx - r} {cy} A {r} {r} 0 1 0 {cx + r} {cy} A {r} {r} 0 1 0 {cx - r} {cy}"


def ellipse(cx, cy, rx, ry):
    return f"M {cx - rx} {cy} A {rx} {ry} 0 1 0 {cx + rx} {cy} A {rx} {ry} 0 1 0 {cx - rx} {cy}"


def arrow(a, b, bend=0.0):
    import math
    mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
    ang = math.atan2(b[1] - my, b[0] - mx)
    h1 = (b[0] - 24 * math.cos(ang - 0.45), b[1] - 24 * math.sin(ang - 0.45))
    h2 = (b[0] - 24 * math.cos(ang + 0.45), b[1] - 24 * math.sin(ang + 0.45))
    return f"M {a[0]} {a[1]} Q {mx:.0f} {my:.0f} {b[0]} {b[1]} M {h1[0]:.0f} {h1[1]:.0f} L {b[0]} {b[1]} L {h2[0]:.0f} {h2[1]:.0f}"


def lbl(text, x, y, size=30, color="ink", anchor="middle"):
    return {"text": text, "x": x, "y": y, "size": size, "color": color, "anchor": anchor}


MACHINE = [
    {"label": "Wafer stage", "sub": "holds and moves the wafer", "kind": "substrate", "color": "teal", "thickness": 18, "size": 250},
    {"label": "Projection mirrors", "sub": "shrink the pattern", "kind": "lid", "color": "muted", "thickness": 12, "size": 220},
    {"label": "Mask (reticle)", "sub": "the chip design", "kind": "die", "color": "accent2", "thickness": 9, "size": 200},
    {"label": "Illumination optics", "sub": "shape the light", "kind": "interconnect", "color": "gold", "thickness": 10, "size": 210},
    {"label": "EUV light source", "sub": "tin plasma makes the light", "kind": "bumps", "color": "risk", "thickness": 14, "size": 230},
]

# ====================================================================== HOOK
stage("s01_machine", "h_question", {
    "zones": [FAB(label="yellow")], "worldW": 1920,
    "cam": [{"at": 0, "x": 860, "y": 470, "zoom": 1.35}, {"at": C("only one company"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("litho", x=860, at=0.2, fireAt=0.8, text="ONE MACHINE", sub="prints the most advanced chips"),
              *suits([1350, 1500]),
              it("sign", x=1450, y=330, text="ONLY ONE COMPANY", sub="knows how to build it", at=C("only one company"), color="#FFF59D", size=36)],
    "callouts": [co("The most advanced chips on Earth…", 960, 150, C("most advanced chips"), "white", screen=True, until=C("only one company", -0.3)),
                 co("…printed by one machine", 960, 150, C("only one company"), "gold", screen=True, size=44)]},
    sources=["asml_euv"], sfx=[{"kind": "hit", "at": 0.0, "gain": 0.3}])
stage("s02_town", "h_stakes", {
    "zones": [DUTCH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.25}, {"at": C("small town"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("building", x=1100, style="office", color="#90CAF9", text="ASML", at=C("That company"), scale=0.9),
              it("stack", x=600, at=C("Each machine"), h=[[0, 40], [{"cue": "Each machine"}, 40], [{"cue": "Each machine", "offset": 2.5}, 300]], text="{{euv_price.display}}", sub="per machine", color="gold"),
              it("sign", x=1550, y=640, text="VELDHOVEN", sub="the Netherlands", post=True, at=C("small town"), color="#FFE0B2", size=30)],
    "callouts": [co("That company exists", 960, 150, C("That company"), "white", screen=True, until=C("Each machine", -0.3)),
                 co("{{euv_price.display}} per machine", 960, 150, C("Each machine"), "gold", screen=True, size=44, until=C("small town", -0.3)),
                 co("…from a small Dutch town", 960, 150, C("small town"), "white", screen=True, size=44)]},
    sources=["reuters_explainer", "asml_history"])
# ====================================================================== MISSION 1
card("s04_m1", "m1_card", "Mission 1", "What the Machine Does", "Printing chips with light")
stage("s05_m1q", "m1_question", {
    "zones": [FAB()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.25}, {"at": C("every phone"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("wafer", x=960, y=420, r=180, at=0.2, spin=6),
              it("device", type="phone", x=420, y=760, at=C("every phone"), scale=0.7), it("device", type="laptop", x=760, y=820, at=C("every laptop"), scale=0.7),
              it("device", type="server", x=1450, y=F, at=C("AI data center"), text="AI DATA CENTER", scale=0.8)],
    "callouts": [co("What does this machine actually do?", 960, 150, C("What does"), "gold", screen=True, size=42)]})
# ---- PRESENTER A: draws the principle of lithography
add("p06_draw", "m1_draw", "engine_draw", {
    "title": "Lithography: printing with light", "board": BOARD, "draw_start": C("A chip is built"), "speed": 1100,
    "enter": {"from": -260, "to": 520, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 220, 120), "color": "gold", "width": 5, "start": C("with light"), "label": lbl("LIGHT", 670, 452)},
        {"d": arrow((790, 440), (1110, 440)), "color": "gold", "width": 5, "start": C("Light shines")},
        {"d": rect(1120, 370, 60, 150), "color": "accent2", "width": 5, "start": C("through a mask"), "label": lbl("MASK", 1150, 360, 26, "accent2")},
        {"d": "M 1040 640 Q 1150 600 1260 640 Q 1150 680 1040 640", "color": "teal", "width": 5, "start": C("lenses or mirrors"), "label": lbl("LENS / MIRRORS", 1340, 650, 26, "teal", "start")},
        {"d": "M 1130 525 L 1080 640 L 1145 880 M 1170 525 L 1220 640 L 1155 880", "color": "gold", "width": 4, "start": C("shrink that image")},
        {"d": ellipse(1150, 890, 220, 46), "color": "ink", "width": 5, "fill": "accent2", "fillOpacity": 0.18, "start": C("onto the wafer"), "label": lbl("WAFER", 1150, 975, 28)},
    ],
    "actions": [{"kind": "walk", "at": C("onto the wafer", 0.7), "dur": 1.0, "to": 1520}, {"kind": "point", "at": C("onto the wafer", 1.8), "dur": 1.2, "target": [1250, 885]}],
    "scale": 0.86, "floor": 1040}, sources=["asml_euv"])
stage("s07_shrink", "m1_shrink", {
    "zones": [FAB()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.1}, {"at": C("So to keep"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("wafer", x=560, y=430, r=190, at=0.3, n=6, text="BIGGER DETAILS"),
              it("wafer", x=1360, y=430, r=190, at=C("smaller details"), n=16, text="SMALLER DETAILS = MORE TRANSISTORS"),
              it("arrow", **{"from": [800, 430], "to": [1120, 430]}, at=C("smaller details"), color="green"),
              it("sign", x=960, y=780, text="NEEDED: SHORTER-WAVELENGTH LIGHT", at=C("So to keep"), color="#E1BEE7", size=32)],
    "callouts": [co("You can't print much smaller than your light", 960, 150, C("The catch"), "risk", screen=True, until=C("smaller details", -0.3)),
                 co("Smaller → faster, cheaper, more efficient", 960, 150, C("smaller details"), "green", screen=True)]})
# ---- pen drawing: the EUV light source
drops = " ".join(circle(420 + i * 52, 540, 7) for i in range(9))
stage("s08_light", "m1_light", {
    "min_seconds": 48, "zones": [FAB(label="yellow")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("A laser flattens"), "x": 960, "y": 480, "zoom": 1.15, "dur": 2.4},
            {"at": C("special mirror"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("tinsource", x=960, y=520, at=C("makes its own", -0.5), laserAt=C("A laser flattens"), plasmaAt=C("more powerful pulse"), rate=0.9, text="INSIDE THE LIGHT SOURCE (slowed down)"),
              it("sign", x=330, y=330, text="{{droplets.display}}", sub="tin drops (real speed)", at=C("tiny drops"), color="#FFF59D", size=34),
              it("sign", x=1600, y=330, text="HOTTER THAN THE SUN'S SURFACE", at=C("hotter than"), color="#FFCDD2", size=26)],
    "callouts": [co("Extreme ultraviolet: {{droplets.nm_display}}", 960, 150, C("ASML's answer"), "gold", screen=True, size=42, until=C("Nothing on Earth", -0.2)),
                 co("Nothing on Earth makes it naturally", 960, 150, C("Nothing on Earth"), "white", screen=True, until=C("tiny drops", -0.3)),
                 co("Molten tin, laser, plasma, light", 960, 150, C("tiny drops"), "white", screen=True, until=C("again and again", -0.3)),
                 co("Again and again, for hours", 960, 150, C("again and again"), "green", screen=True)]},
    sources=["asml_hot", "asml_ar_2025"])
# ---- pen drawing: mirrors in a vacuum
stage("s09_mirrors", "m1_mirrors", {
    "zones": [FAB()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.05}], "drift": 0,
    "items": [it("mirrors", x=960, y=500, at=0.2, beamAt=C("bounces off"), dur=3.5, scale=1.0)],
    "callouts": [co("Absorbed by almost everything, even air", 960, 150, C("absorbed"), "risk", screen=True, until=C("bounces off", -0.3)),
                 co("Mirrors, in a vacuum", 960, 150, C("bounces off"), "gold", screen=True, size=44)]},
    sources=["asml_euv", "ieee_euv"])
stage("s10_size", "m1_discovery", {
    "min_seconds": 21, "zones": [FAB(x1=1900), Z("airport", 1900, 6000)], "worldW": 3600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("To deliver one"), "x": 2600, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("litho", x=620, at=0.2, fireAt=0.5, text="EUV MACHINE", scale=0.8),
              it("bus", x=1400, at=C("school bus"), text="SCHOOL BUS", scale=0.9),
              it("sign", x=960, y=230, text="{{machine_size.display}}", sub="per machine", at=C("weighing"), color="#FFF59D", size=40),
              it("conveyor", x0=2100, x1=2900, y=F - 30, goods="box", label="ASML", n=6, speed=120, at=C("To deliver one", -0.5)),
              it("plane", x=[[0, 2400], [{"cue": "cargo planes"}, 2400], [{"cue": "cargo planes", "offset": 6}, 4200]], y=[[0, 720], [{"cue": "cargo planes", "offset": 6}, 200]], tilt=-12, text="", scale=0.8, at=C("cargo planes", -1))],
    "callouts": [co("The size of a school bus", 960, 960, C("school bus"), "gold", screen=True, until=C("To deliver one", -0.3)),
                 co("{{machine_size.containers_display}} containers + cargo planes", 960, 960, C("To deliver one"), "white", screen=True)]},
    sources=["reuters_explainer"])
kinetic("s11_m1t", "m1_transition", [("Why can only one company", 60, "So why", None, True), ("build it?", 80, "build it", "accent", False)])

# ====================================================================== MISSION 2
card("s12_m2", "m2_card", "Mission 2", "How One Company Ended Up Alone", "Forty years of bets")
stage("s13_m2q", "m2_question", {
    "zones": [DUTCH()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.2}, {"at": C("monopolies"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=960, style="office", color="#90CAF9", text="ASML", at=0.2, scale=0.8),
              it("letters", x=960, y=200, text="THE ONLY ONE?", at=C("the only one"), size=80, color="gold")],
    "callouts": [co("Monopolies like this rarely last", 960, 960, C("monopolies"), "white", screen=True)]})
stage("s14_origin", "m2_origin", {
    "min_seconds": 39, "zones": [DUTCH()], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Its early years"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=280, y=300, at=0.2, scale=0.75, pages=[[0, "1984", "FOUNDED"], [{"cue": "moved to Veldhoven"}, "1985", "VELDHOVEN"], [{"cue": "fully independent"}, "1995", "INDEPENDENT"]]),
              it("building", x=600, style="office", color="#B0BEC5", text="PHILIPS", at=C("Philips"), scale=0.65),
              it("building", x=1050, style="office", color="#C5E1A5", text="ASM INTERNATIONAL", at=C("A S M International"), scale=0.65),
              it("building", x=1550, style="office", color="#90CAF9", text="ASML", at=C("created a small"), scale=0.55),
              it("arrow", **{"from": [700, 380], "to": [1450, 420]}, at=C("created a small"), color="gold"),
              it("tower", x=2150, text="BIG RIVALS", color="#78909C", at=C("bigger, established"), scale=0.9),
              it("sign", x=1550, y=280, text="LISTED: AMSTERDAM + NEW YORK", at=C("fully independent"), color="#FFF59D", size=28),
              it("sign", x=1550, y=430, text="BET: EVER-SHORTER LIGHT", at=C("one idea"), color="#E1BEE7", size=28)],
    "callouts": [co("{{founded_1984.display}}: Philips + ASM International", 960, 150, C("created a small"), "white", screen=True, until=C("Its early years", -0.3)),
                 co("A small, unknown newcomer", 960, 150, C("Its early years"), "risk", screen=True, until=C("fully independent", -0.3)),
                 co("{{ipo_1995.display}}: independent and listed", 960, 150, C("fully independent"), "gold", screen=True)]},
    sources=["asml_history"])
# ---- PRESENTER B: the customers' bet (relationship)
add("p15_bet", "m2_bet", "engine_draw", {
    "title": "The customers became owners", "board": BOARD, "draw_start": C("biggest customers"), "speed": 1300,
    "enter": {"from": 2200, "to": 1500, "at": C("The conflict", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 1150 300 L 1150 300", "color": "risk", "width": 1, "start": C("took decades"), "label": lbl("DECADES · BILLIONS · NO GUARANTEE", 1150, 300, 30, "risk")},
        {"d": rect(560, 380, 260, 100), "color": "accent2", "width": 5, "start": C("Intel"), "label": lbl("INTEL", 690, 442)},
        {"d": rect(560, 530, 260, 100), "color": "accent2", "width": 5, "start": C("TSMC"), "label": lbl("TSMC", 690, 592)},
        {"d": rect(560, 680, 260, 100), "color": "accent2", "width": 5, "start": C("Samsung"), "label": lbl("SAMSUNG", 690, 742)},
        {"d": rect(1330, 500, 300, 160), "color": "gold", "width": 6, "start": C("bought"), "label": lbl("ASML", 1480, 595, 40, "gold")},
        {"d": arrow((830, 430), (1320, 540), -0.08), "color": "ink", "width": 4, "start": C("of the company")},
        {"d": arrow((830, 580), (1320, 580), 0), "color": "ink", "width": 4},
        {"d": arrow((830, 730), (1320, 620), 0.08), "color": "ink", "width": 4},
        {"d": "M 960 420 L 960 420", "color": "gold", "width": 1, "start": C("of the company", 0.6), "label": lbl("{{ccip_2012.display}} STAKE", 1075, 380, 34, "gold")},
        {"d": "M 960 800 L 960 800", "color": "gold", "width": 1, "start": C("helped pay"), "label": lbl("+ RESEARCH FUNDING", 1075, 850, 32, "gold")},
    ],
    "actions": [{"kind": "explain", "at": C("The conflict", 1.2), "dur": 4.0}, {"kind": "walk", "at": C("pay for the research", 0.5), "dur": 1.1, "to": 1790}, {"kind": "point", "at": C("pay for the research", 1.7), "dur": 1.2, "target": [1560, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["ccip_2012", "samsung_ccip"])
stage("s16_insurance", "m2_insurance", {
    "zones": [FAB()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 4,
    "items": [it("building", x=480, style="office", color="#B0BEC5", text="CHIPMAKERS", at=0.2, scale=0.75),
              it("sign", x=480, y=250, text="NO MACHINE → ROADMAPS STALL", at=C("never arrived"), color="#FFCDD2", size=28),
              it("litho", x=1350, at=C("If it did"), fireAt=C("first in line"), text="EUV MACHINE", scale=0.7),
              *crowd([1000], "cheer", at=C("first in line"), tie=True)],
    "callouts": [co("For the customers: insurance", 960, 150, C("insurance"), "gold", screen=True, size=44, until=C("If it did", -0.3)),
                 co("Machine arrives → first in line", 960, 150, C("first in line"), "green", screen=True, size=40)]})
add("s17_pieces", "m2_pieces", "timeline_network", {
    "title": "Buying the missing pieces", "title_cue": "missing pieces", "subtitle": "Light source and optics",
    "start_year": 1980, "end_year": 2025, "tick_every": 5, "axis_cue": "missing pieces",
    "items": [
        {"year": "{{founded_1984.value}}", "label": "ASML founded", "place": "ASML · Veldhoven", "role": "design + assembly", "lon": LL["veldhoven"][0], "lat": LL["veldhoven"][1], "colour": "accent", "cue": "missing pieces", "label_dx": -18},
        {"year": 2012, "label": "Moves to buy Cymer", "place": "Cymer · San Diego", "role": "light source", "lon": LL["sandiego"][0], "lat": LL["sandiego"][1], "colour": "accent2", "cue": "Cymer"},
        {"year": 2016, "label": "24.9% of Zeiss SMT", "place": "Zeiss · Oberkochen", "role": "mirrors", "lon": LL["oberkochen"][0], "lat": LL["oberkochen"][1], "colour": "accent3", "cue": "chip optics", "label_dx": 18, "label_dy": 40},
        {"year": "{{euv_2020.value}}", "label": "EUV in high-volume production", "place": "", "role": "", "lon": LL["veldhoven"][0], "lat": LL["veldhoven"][1], "colour": "accent", "cue": "high volume"},
    ],
    "links": [[1, 0], [2, 0]], "morph_cue": "production", "view": {"lon": -55, "lat": 45, "span": 160},
    "highlight": {"NLD": "accent", "USA": "accent2", "DEU": "accent3"}, "network_title": "One machine, three companies"},
    sources=["cymer_2012", "zeiss_2016", "asml_history", "natural_earth"], assets=GEO)
stage("s18_share", "m2_discovery", {
    "zones": [DUTCH()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.1}, {"at": C("the only company"), "x": 960, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("tower", x=960, text="ASML", color="#1E7FD8", growAt=C("didn't win alone", -0.5), scale=1.0),
              it("building", x=480, style="office", color="#B0BEC5", text="CUSTOMERS", at=C("customers"), scale=0.65),
              it("building", x=1450, style="office", color="#C5E1A5", text="SUPPLIERS", at=C("its suppliers"), scale=0.65),
              it("letters", x=960, y=120, text="№ 1", at=C("the only company"), size=110, color="gold")],
    "callouts": [co("It tied customers + suppliers to the same bet", 960, 960, C("didn't win alone"), "white", screen=True, until=C("the only company", -0.3)),
                 co("The only maker of EUV machines", 960, 960, C("the only company"), "gold", screen=True, until=C("most valuable", -0.3)),
                 co("Europe's most valuable company", 960, 960, C("most valuable"), "green", screen=True, sub="Reuters")]},
    sources=["reuters_explainer", "asml_euv"])
kinetic("s19_m2t", "m2_transition", [("Never built by one company", 56, "never built", None, True), ("Who else is inside it?", 76, "Who else", "accent", False)])

# ====================================================================== MISSION 3
card("s20_m3", "m3_card", "Mission 3", "Who Builds It", "The monopoly is a network")
stage("s21_m3q", "m3_question", {
    "zones": [FAB()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.2}, {"at": C("It matters"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("litho", x=960, at=0.2, fireAt=0.6, text="WHO BUILDS IT?", scale=0.75), *suits([380, 520, 1400, 1540]),
              it("arm", x=1750, at=0.4)],
    "callouts": [co("Who actually builds this machine?", 960, 150, C("Who actually"), "gold", screen=True, size=42, until=C("It matters", -0.3)),
                 co("Not one company: a network", 960, 150, C("It is a network"), "white", screen=True, size=42)]})
add("s22_inside", "m3_inside", "engine_exploded", {
    "title": "Inside the machine", "subtitle": "conceptual modules · schematic, not the physical layout", "layers": MACHINE, "cx": 760, "cy": 620,
    "scale": [[0, 0.7], [1.2, 1.2], [14, 1.35], [22, 1.15]], "yaw": [[0, 15], [22, 70]],
    "explodeAt": C("open it up", 0.4), "labelsAt": C("At the bottom"), "assembleAt": C("where the tin", 1.4), "explodeGap": 64},
    sources=["asml_euv"])
add("s23_suppliers", "m3_map", "engine_map", {
    "title": "Where the parts come from", "subtitle": "{{suppliers.display}} suppliers in total",
    "cameras": [{"at": 0, "lon": 7.5, "lat": 50.2, "span": 12}, {"at": C("In fact"), "lon": 9.2, "lat": 49.6, "span": 6, "dur": 1.8},
                {"at": C("San Diego", -0.6), "lon": -55, "lat": 44, "span": 165, "dur": 2.0},
                {"at": C("In total"), "lon": -20, "lat": 42, "span": 120, "dur": 2.0},
                {"at": C("comes together"), "lon": 6.5, "lat": 50.5, "span": 10, "dur": 1.8}],
    "drift": {"lon": 0.25, "zoom": 0.004}, "tilt": [[0, 12], [20, 4], [40, 12]],
    "highlights": [{"iso": "NLD", "color": "gold", "at": 0.3}, {"iso": "DEU", "color": "teal", "at": C("Zeiss")}, {"iso": "USA", "color": "accent2", "at": C("San Diego")}],
    "hubs": [
        {"id": "v", "at": LL["veldhoven"], "label": "Veldhoven", "sub": "ASML assembly", "color": "gold", "time": 0.5, "anchor": "end"},
        {"id": "o", "at": LL["oberkochen"], "label": "Oberkochen", "sub": "Zeiss optics · {{zeiss.buy_display}} (2025)", "color": "teal", "time": C("Zeiss")},
        {"id": "w", "at": LL["wetzlar"], "label": "Wetzlar", "sub": "Zeiss optics", "color": "teal", "time": C("Wetzlar")},
        {"id": "s", "at": LL["sandiego"], "label": "San Diego", "sub": "Cymer light source", "color": "accent2", "time": C("San Diego")}],
    "routes": [
        {"from": LL["oberkochen"], "to": LL["veldhoven"], "at": C("mirrors come from", 0.5), "dur": 1.0, "color": "teal", "tokenShape": "box", "tokens": 6, "tokenEvery": 0.35, "lift": 0.3},
        {"from": LL["wetzlar"], "to": LL["veldhoven"], "at": C("Wetzlar", 0.4), "dur": 0.8, "color": "teal", "tokenShape": "box", "tokens": 5, "tokenEvery": 0.35, "lift": 0.3},
        {"from": LL["sandiego"], "to": LL["veldhoven"], "at": C("San Diego", 0.6), "dur": 1.4, "color": "accent2", "tokenShape": "box", "tokens": 6, "tokenEvery": 0.35, "lift": 0.25}],
    "caption": "Real locations (Natural Earth) · routes are schematic"},
    sources=["asml_ar_2025", "cymer_2012", "natural_earth"], assets=GEO)
stage("s24_ship", "m3_shipping", {
    "min_seconds": 20, "zones": [FAB(x1=1700), Z("airport", 1700, 3700, night=True), FAB(3700, 7000)], "worldW": 4800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("flown to"), "x": 2700, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("rebuilt there"), "x": 4300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("litho", x=800, at=0.2, fireAt=C("tested"), text="BUILT + TESTED (NL)", scale=0.75),
              it("conveyor", x0=1150, x1=1650, y=F - 30, goods="box", label="CRATE", n=4, speed=90, at=C("taken apart")),
              it("plane", x=[[0, 2100], [{"cue": "flown to"}, 2100], [{"cue": "flown to", "offset": 6}, 3600]], y=[[0, 700], [{"cue": "flown to", "offset": 3}, 300], [{"cue": "flown to", "offset": 6}, 650]], text="", scale=0.8),
              it("litho", x=4300, at=C("rebuilt there", -0.6), fireAt=C("start printing"), text="REBUILT AT THE FAB", scale=0.75), *suits([3950, 4650], at=C("rebuilt there"))],
    "callouts": [co("Built and tested in the Netherlands", 960, 150, C("built and tested"), "white", screen=True, until=C("taken apart", -0.3)),
                 co("…taken apart, packed into crates…", 960, 150, C("taken apart"), "white", screen=True, until=C("flown to", -0.3)),
                 co("…flown to the customer", 960, 150, C("flown to"), "gold", screen=True, until=C("rebuilt there", -0.3)),
                 co("…and rebuilt there", 960, 150, C("rebuilt there"), "green", screen=True)]},
    sources=["reuters_explainer"])
kinetic("s25_m3t", "m3_transition", [("Where does all the money go?", 60, "So where", None, True)])

# ====================================================================== MISSION 4
card("s26_m4", "m4_card", "Mission 4", "How It Makes Money", "Machines, research, and a loop")
stage("s27_m4q", "m4_question", {
    "zones": [DUTCH()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.2}, {"at": C("It matters"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=960, style="office", color="#90CAF9", text="ASML", at=0.2, scale=0.8),
              it("coins", **{"from": [-100, 200], "to": [960, 500]}, at=0.5, rate=4), it("coins", **{"from": [2000, 200], "to": [960, 500]}, at=0.8, rate=4)],
    "callouts": [co("How does ASML make money?", 960, 150, C("How does"), "gold", screen=True, size=44, until=C("It matters", -0.3)),
                 co("In the middle of the AI boom", 960, 150, C("AI boom"), "white", screen=True, size=42)]})
# ---- PRESENTER C: draws the numbers
add("p28_sales", "m4_sales", "engine_draw", {
    "title": "ASML in 2025 (US dollars)", "board": BOARD, "draw_start": C("ASML sold"), "speed": 1400,
    "enter": {"from": -260, "to": 520, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 600 900 L 1760 900", "color": "border", "width": 4, "start": C("draw the numbers"), "kind": "stroke"},
        {"d": "M 660 900 L 660 438 L 860 438 L 860 900", "color": "gold", "width": 5, "fill": "gold", "fillOpacity": 0.35, "kind": "bar", "start": C("ASML sold"),
         "label": lbl("{{sales_2025.display}}", 760, 416, 40, "gold")},
        {"d": "M 760 945 L 760 945", "color": "ink", "width": 1, "start": C("ASML sold", 0.6), "label": lbl("SALES", 760, 945, 26, "muted")},
        {"d": "M 760 400 L 760 400", "color": "ink", "width": 1, "start": C("up"), "label": lbl("{{sales_2025.growth_display}} IN ONE YEAR", 760, 350, 26, "ink")},
        {"d": "M 1010 900 L 1010 765 L 1210 765 L 1210 900", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("as profit"),
         "label": lbl("{{sales_2025.ni_display}}", 1110, 743, 36, "accent3")},
        {"d": "M 1110 945 L 1110 945", "color": "ink", "width": 1, "start": C("as profit", 0.5), "label": lbl("PROFIT", 1110, 945, 26, "muted")},
        {"d": "M 1360 900 L 1360 736 L 1560 736 L 1560 900", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.35, "kind": "bar", "start": C("the star"),
         "label": lbl("{{euv_sales_2025.usd_display}}", 1460, 714, 36, "accent2")},
        {"d": "M 1460 945 L 1460 945", "color": "ink", "width": 1, "start": C("bringing in", -1.0), "label": lbl("{{euv_sales_2025.display}} EUV MACHINES", 1460, 945, 26, "muted")},
    ],
    "actions": [{"kind": "walk", "at": C("bringing in", 0.8), "dur": 1.0, "to": 1820}, {"kind": "point", "at": C("bringing in", 1.9), "dur": 1.3, "target": [1460, 820]}, {"kind": "react", "at": C("bringing in", 3.3)}],
    "scale": 0.86, "floor": 1040}, sources=["asml_q4_2025", "asml_q4_2025_deck", "asml_q4_2024", "ecb_2025_avg"])
stage("s29_avg", "m4_average", {
    "zones": [FAB(label="yellow")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 4,
    "items": [it("litho", x=700, at=0.2, fireAt=0.6, text="ONE EUV MACHINE", scale=0.8),
              it("stack", x=1450, at=0.4, h=[[0, 40], [2.5, 330]], text="{{euv_sales_2025.avg_display}}", sub="average per machine (our calculation)", color="gold")],
    "callouts": [co("{{euv_sales_2025.avg_display}} per machine", 960, 150, C("average"), "gold", screen=True, size=44, sub="{{euv_sales_2025.usd_display}} ÷ {{euv_sales_2025.display}} machines", until=C("We show", -0.3)),
                 co("All figures in US dollars", 960, 150, C("We show"), "white", screen=True, sub="converted at the official average rate for the year")]},
    sources=["asml_q4_2025_deck", "ecb_2025_avg"])
add("s30_regions", "m4_customers", "engine_chart", {"chart": "bar", "data": "{{regions.value}}", "box": {"x": 300, "y": 330, "w": 1320, "h": 500},
    "start": C("who buys"), "stagger": 0.25, "title": "Who buys from ASML", "note": "Share of 2025 sales, by customer location",
    "valueSuffix": "%", "highlight": 0, "highlightAt": C("customers in China"), "color": "accent2", "highlightColor": "risk"},
    sources=["asml_ar_2025"])
stage("s31_loop", "m4_flywheel", {
    "min_seconds": 32, "zones": [Z("sciencepark", -1600, 1300), FAB(1300, 6000)], "worldW": 2800,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 0.95}, {"at": C("already had"), "x": 1500, "y": 500, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "items": [it("coins", **{"from": [500, 500], "to": [1900, 500]}, at=C("Chipmakers pay"), rate=5),
              it("sign", x=500, y=300, text="CHIPMAKERS", at=0.2, color="#BBDEFB", size=34),
              it("stack", x=1900, at=C("on research"), h=[[0, 40], [{"cue": "on research"}, 40], [{"cue": "on research", "offset": 2.5}, 240]], text="R&D {{rd_2025.display}}", sub="a year", color="#E1BEE7"),
              it("litho", x=2350, at=C("makes the next"), fireAt=C("stay ahead"), text="NEXT MACHINE", scale=0.6),
              it("arrow", **{"from": [2200, 300], "to": [700, 300]}, at=C("order again"), color="green", text="ORDER AGAIN"),
              it("counter", x=1500, y=170, at=C("already had"), steps=[[0, 0], [{"cue": "already had"}, 0], [{"cue": "already had", "offset": 2.5}, 43.8]], prefix="$", suffix="bn", decimals=1, text="orders waiting, end of 2025")],
    "callouts": [co("The money flows in a loop", 960, 960, C("money flows"), "gold", screen=True)]},
    sources=["asml_ar_2025"])
kinetic("s32_m4t", "m4_transition", [("A machine this valuable", 58, "A machine", None, True), ("is also a weapon", 80, "weapon", "risk", False)])

# ====================================================================== MISSION 5
card("s33_m5", "m5_card", "Mission 5", "Where the Machine May Go", "Export controls and the price of a gate")
stage("s34_m5q", "m5_question", {
    "zones": [Z("airport", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.15}, {"at": C("It matters"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("barrier", x=900, at=0.2, closeAt=C("allowed to go"), text="EXPORT CHECK"),
              it("conveyor", x0=200, x1=760, y=F - 30, goods="box", label="EUV", n=3, speed=70, stopAt=C("allowed to go"))],
    "callouts": [co("Who decides where the machines may go?", 960, 150, C("Who decides"), "gold", screen=True, size=40, until=C("It matters", -0.3)),
                 co("Control the machine → control the chips", 960, 150, C("whoever controls"), "risk", screen=True, size=40)]})
add("s35_export", "m5_map", "engine_map", {
    "title": "Where EUV machines can go", "subtitle": "export rules set by the Netherlands, under pressure from the United States",
    "cameras": [{"at": 0, "lon": 35, "lat": 38, "span": 300}, {"at": C("not to China"), "lon": 80, "lat": 38, "span": 170, "dur": 2.0},
                {"at": C("older machines"), "lon": 45, "lat": 38, "span": 260, "dur": 2.4}],
    "drift": {"lon": 0.15, "zoom": 0.003}, "tilt": [[0, 14], [22, 6]],
    "highlights": [{"iso": "NLD", "color": "gold", "at": 0.3}, {"iso": "TWN", "color": "accent2", "at": C("Taiwan")}, {"iso": "KOR", "color": "accent2", "at": C("South Korea")},
                   {"iso": "USA", "color": "accent2", "at": C("United States")}, {"iso": "CHN", "color": "risk", "at": C("not to China"), "strength": 0.7}],
    "hubs": [{"id": "v", "at": LL["veldhoven"], "label": "Veldhoven", "color": "gold", "time": 0.4, "anchor": "end"},
             {"id": "t", "at": LL["hsinchu"], "label": "Taiwan", "color": "accent2", "time": C("Taiwan")},
             {"id": "k", "at": LL["hwaseong"], "label": "South Korea", "color": "accent2", "time": C("South Korea")},
             {"id": "u", "at": LL["hillsboro"], "label": "United States", "color": "accent2", "time": C("United States"), "anchor": "end"},
             {"id": "c", "at": LL["shanghai"], "label": "China", "sub": "no EUV · older machines restricted from 2023", "color": "risk", "time": C("not to China"), "anchor": "end"}],
    "routes": [{"from": LL["veldhoven"], "to": LL["hsinchu"], "at": C("Taiwan"), "dur": 1.0, "color": "accent2", "tokenShape": "box", "lift": 0.22},
               {"from": LL["veldhoven"], "to": LL["hwaseong"], "at": C("South Korea"), "dur": 1.0, "color": "accent2", "tokenShape": "box", "lift": 0.3},
               {"from": LL["veldhoven"], "to": LL["hillsboro"], "at": C("United States"), "dur": 1.0, "color": "accent2", "tokenShape": "box", "lift": 0.25},
               {"from": LL["veldhoven"], "to": LL["shanghai"], "at": C("not to China"), "dur": 1.2, "blocked": True, "lift": 0.26}],
    "caption": "Real locations (Natural Earth) · routes are schematic"},
    sources=["reuters_2019_licence", "cnbc_export", "ioplus_2024", "dutch_2024", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "not to China", "gain": 0.3}])
# ---- PRESENTER D: draws the gate
add("p36_gate", "m5_gate", "engine_draw", {
    "title": "An export license is a gate", "board": BOARD, "draw_start": C("On one side"), "speed": 1300,
    "enter": {"from": 2200, "to": 1450, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(540, 470, 330, 170), "color": "gold", "width": 6, "start": C("On one side"), "label": lbl("SUPPLY NETWORK", 705, 565, 30, "gold")},
        {"d": rect(1440, 360, 320, 120), "color": "accent2", "width": 5, "start": C("the buyers"), "label": lbl("BUYER A", 1600, 432)},
        {"d": rect(1440, 640, 320, 120), "color": "accent2", "width": 5, "start": C("the buyers", 0.4), "label": lbl("BUYER B", 1600, 712)},
        {"d": "M 1130 350 L 1130 800 M 1190 350 L 1190 800 M 1130 350 L 1190 350 M 1130 800 L 1190 800", "color": "ink", "width": 6, "start": C("is a gate"), "label": lbl("EXPORT LICENSE", 1160, 860, 28, "ink")},
        {"d": arrow((880, 520), (1430, 420), -0.06), "color": "accent3", "width": 6, "start": C("Open it")},
        {"d": arrow((880, 600), (1120, 690), 0.05), "color": "risk", "width": 6, "start": C("Close it")},
        {"d": "M 1090 650 L 1130 730 M 1130 650 L 1090 730", "color": "risk", "width": 8, "start": C("Close it", 0.6)},
        {"d": "M 1600 780 L 1600 780", "color": "risk", "width": 1, "start": C("build its own"), "label": lbl("BUILD YOUR OWN: YEARS", 1600, 820, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Close it", 1.0), "dur": 1.2, "target": [1110, 690]}],
    "scale": 0.86, "floor": 1040})
stage("s37_cost", "m5_cost", {
    "min_seconds": 37, "zones": [DUTCH(x1=1700), FAB(1700, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("next generation"), "x": 2400, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("chart", x=960, y=400, w=640, h=360, at=0.3, dur=2, text="CHINA'S SHARE OF ASML SALES", pts=[0.85, 0.65], crashAt=C("twenty twenty-six")),
              it("sign", x=960, y=700, text="2024 {{regions.china24_display}} → 2025 {{regions.display}} → 2026 {{china_2026.display}}", sub="2026: company expectation", at=C("The company expects"), color="#FFF59D", size=26),
              it("sign", x=1500, y=300, text="CHINA BUILDS ITS OWN", at=C("racing to build"), color="#FFCDD2", size=28, hang=True, swing=True),
              it("litho", x=2400, at=C("next generation", -0.4), fireAt=C("next generation"), text="HIGH-NA (NEXT GEN)", sub="{{highna_price.display}}", scale=0.8),
              it("sign", x=2400, y=210, text="FIRST ONE: {{highna_intel.display}}", at=C("The first of those"), color="#BBDEFB", size=28)],
    "callouts": [co("The gate has a price for ASML too", 960, 150, C("The gate has a price"), "white", screen=True, until=C("next generation", -0.3)),
                 co("The gap may keep growing", 960, 150, C("gap"), "risk", screen=True, size=42)]},
    sources=["asml_ar_2025", "caixin_china", "highna_2023"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "min_seconds": 36, "zones": [DUTCH(x1=1800), FAB(1800, 6000, label="yellow")], "worldW": 3200,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("small town"), "x": 960, "y": 500, "zoom": 1.1, "dur": 2.6},
            {"at": C("drop of tin"), "x": 2450, "y": 520, "zoom": 1.05, "dur": 2.6}], "drift": 0,
    "items": [it("sign", x=380, y=330, text="40 YEARS OF BETS", at=C("forty years"), color="#FFF59D", size=32, hang=True, swing=True),
              it("sign", x=960, y=480, text="A NETWORK NO ONE CAN COPY", at=C("network of suppliers"), color="#C8E6C9", size=32, hang=True, swing=True),
              it("sign", x=1540, y=330, text="CUSTOMERS WHO PAID", at=C("customers who paid"), color="#BBDEFB", size=32, hang=True, swing=True),
              it("tinsource", x=2450, y=520, at=C("drop of tin", -0.6), laserAt=C("hit by a laser"), rate=0.9, scale=0.9)],
    "callouts": [co("Not a single invention", 960, 960, C("not a single invention"), "white", screen=True, until=C("small town", -0.3)),
                 co("A small Dutch town holds a key to computing", 960, 960, C("small town"), "gold", screen=True, until=C("drop of tin", -0.3)),
                 co("It all begins as a drop of tin", 960, 960, C("drop of tin"), "green", screen=True, size=44)]},
    sources=["asml_history", "asml_hot"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

OUT.write_text("# GENERATED by tools/gen_asml_storyboard.py; edit the generator, not this file.\n"
               "# Episode 08 storyboard on the animation engine. The channel intro is inserted automatically after the hook.\n"
               + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
print(f"{len(scenes)} scenes -> {OUT}")
