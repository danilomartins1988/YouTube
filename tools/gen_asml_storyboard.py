"""Generates projects/the-machine-only-one-company-can-build/deliverables/documentary/storyboard.yaml (Episode 08).

Built on the animation engine (engine_* scene types, see docs/engine/INTEGRATION.md). Times are narration cues
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
    add(id_, seg, "act_title", {"number": number, "title": title, "subtitle": sub, "min_seconds": 3.0}, sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


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
add("s01_machine", "h_question", "engine_exploded", {
    "title": "One machine. One company.", "layers": MACHINE, "cx": 960, "cy": 600,
    "scale": [[0, 0.5], [1.5, 1.15], [7, 1.35]], "yaw": [[0, 0], [8, 70]],
    "explodeAt": 99, "assembleAt": 100, "note": "Conceptual modules · schematic"},
    sources=["asml_euv"], sfx=[{"kind": "hit", "at": 0.0, "gain": 0.3}])
add("s02_town", "h_stakes", "engine_map", {
    "cameras": [{"at": 0, "lon": 15, "lat": 30, "span": 300}, {"at": C("small town"), "lon": 5.43, "lat": 51.6, "span": 7, "dur": 2.0}],
    "highlights": [{"iso": "NLD", "color": "gold", "at": C("That company")}],
    "hubs": [{"id": "v", "at": LL["veldhoven"], "label": "Veldhoven", "sub": "{{euv_price.display}} per machine", "color": "gold", "time": C("Each machine")}],
    "tilt": [[0, 10], [6, 0]], "caption": "Real location (Natural Earth, public domain)"},
    sources=["reuters_explainer", "asml_history", "natural_earth"], assets=GEO)
kinetic("s03_missions", "h_missions", [
    ("Today: five missions", 64, "five missions", "accent", False),
    ("1 · What the machine actually does", 40, "what this machine", None, True),
    ("2 · How one company ended up alone", 40, "ended up alone", None, True),
    ("3 · Who helps build it", 40, "who helps", None, True),
    ("4 · How it makes money", 40, "makes money", None, True),
    ("5 · Where it is allowed to go", 40, "allowed to go", "risk", True)], chapter="Five missions")

# ====================================================================== MISSION 1
card("s04_m1", "m1_card", "Mission 1", "What the Machine Does", "Printing chips with light")
question("s05_m1q", "m1_question", "Mission 1 · What the machine does", "What does this machine actually do?",
         "Every phone, laptop and AI data center depends on it", "What does", "It matters")
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
kinetic("s07_shrink", "m1_shrink", [
    ("You can't print details much smaller than the light", 46, "The catch", None, True),
    ("Smaller details = more transistors per chip", 50, "more transistors", "accent", False),
    ("faster · cheaper · more efficient", 44, "faster", None, True),
    ("Needed: much shorter wavelength", 58, "much shorter", "accent2", False)], chapter="Mission 1 · The catch")
# ---- pen drawing: the EUV light source
drops = " ".join(circle(420 + i * 52, 540, 7) for i in range(9))
add("s08_light", "m1_light", "engine_draw", {
    "title": "Making light that nature doesn't", "subtitle": "{{droplets.nm_display}} extreme ultraviolet", "presenter": False, "studio": False,
    "draw_start": C("ASML's answer"), "speed": 1400,
    "strokes": [
        {"d": "M 420 540 L 900 540", "color": "border", "width": 3, "start": C("molten tin"), "flow": 140},
        {"d": drops, "color": "muted", "width": 4, "start": C("tiny drops"), "label": lbl("MOLTEN TIN · {{droplets.display}}", 420, 490, 28, "muted", "start")},
        {"d": "M 920 900 L 920 560", "color": "accent2", "width": 6, "flow": 260, "start": C("A laser flattens"), "label": lbl("LASER PRE-PULSE", 895, 880, 26, "accent2", "end")},
        {"d": ellipse(920, 540, 26, 9), "color": "ink", "width": 4, "start": C("each drop")},
        {"d": "M 1010 900 L 930 560", "color": "risk", "width": 9, "flow": 320, "start": C("stronger pulse"), "label": lbl("MAIN PULSE", 1035, 900, 26, "risk", "start")},
        {"d": "M 920 470 L 920 400 M 920 610 L 920 680 M 850 540 L 780 540 M 990 540 L 1060 540 M 870 490 L 830 450 M 970 590 L 1010 630 M 970 490 L 1010 450 M 870 590 L 830 630",
         "color": "gold", "width": 6, "pulse": True, "start": C("plasma"), "label": lbl("PLASMA → EUV LIGHT", 920, 370, 30, "gold")},
        {"d": "M 760 330 Q 640 540 760 750", "color": "teal", "width": 8, "start": C("special mirror"), "label": lbl("COLLECTOR MIRROR", 640, 800, 26, "teal")},
        {"d": "M 930 520 L 1560 430 M 930 560 L 1560 650 M 1560 430 L 1700 540 L 1560 650", "color": "gold", "width": 4, "flow": 220, "start": C("sends it"), "label": lbl("INTO THE MACHINE →", 1640, 400, 26, "gold")},
        {"d": "M 420 960 L 1700 960", "color": "border", "width": 3, "start": C("again and again"), "label": lbl("REPEATED NONSTOP, FOR HOURS", 1060, 1010, 26, "muted")},
    ]}, sources=["asml_hot", "ieee_euv", "bits_1000w"])
# ---- pen drawing: mirrors in a vacuum
add("s09_mirrors", "m1_mirrors", "engine_draw", {
    "title": "Mirrors, in a vacuum", "presenter": False, "studio": False, "draw_start": C("absorbed"), "speed": 1600,
    "strokes": [
        {"d": rect(260, 300, 1400, 620), "color": "border", "width": 4, "dash": "14 10", "start": C("even air"), "label": lbl("VACUUM CHAMBER", 300, 345, 26, "muted", "start")},
        {"d": "M 470 800 Q 520 770 570 800 M 770 410 Q 820 440 870 410 M 1070 800 Q 1120 770 1170 800 M 1370 410 Q 1420 440 1470 410", "color": "teal", "width": 7, "pulse": True, "start": C("ultra smooth"), "label": lbl("MIRRORS", 820, 380, 26, "teal")},
        {"d": "M 300 600 L 520 790 L 820 420 L 1120 790 L 1420 420 L 1560 760", "color": "gold", "width": 5, "flow": 300, "start": C("bounces off", 0.3)},
        {"d": ellipse(1580, 800, 110, 26), "color": "ink", "width": 5, "fill": "accent2", "fillOpacity": 0.2, "start": C("reaches the wafer"), "label": lbl("WAFER", 1580, 870, 26)},
    ]}, sources=["asml_euv", "ieee_euv"])
add("s10_size", "m1_discovery", "compare", {"chapter": "Mission 1 · The discovery", "title": "One machine", "sides": [
    {"kicker": "Weight", "value": "{{machine_size.display}}", "label": "about the size of a bus", "cue": "weighing"},
    {"kicker": "Parts", "value": "{{machine_size.parts_display}}", "label": "in one machine", "cue": "parts"},
    {"kicker": "To deliver one", "value": "{{machine_size.containers_display}}", "label": "containers + cargo planes", "cue": "shipping containers"}]},
    sources=["reuters_explainer", "intel_euv"])
kinetic("s11_m1t", "m1_transition", [("Why can only one company", 60, "So why", None, True), ("build it?", 80, "build it", "accent", False), ("Mission 2 →", 44, "mission two", "muted", False)])

# ====================================================================== MISSION 2
card("s12_m2", "m2_card", "Mission 2", "How One Company Ended Up Alone", "Forty years of bets")
question("s13_m2q", "m2_question", "Mission 2 · How one company ended up alone", "How did a small Dutch company end up as the only one?",
         "Monopolies like this usually don't last", "How did", "It matters")
add("s14_origin", "m2_origin", "timeline", {"chapter": "Mission 2 · The origin", "title": "A small joint venture in Veldhoven",
    "start_year": 1980, "end_year": 2000, "tick_every": 5, "items": [
        {"year": "{{founded_1984.value}}", "label": "Philips + ASM International set up ASML", "cue": "joint venture"},
        {"year": 1990, "display": "Late 1980s", "label": "A newcomer against bigger Japanese rivals", "cue": "Japanese rivals"},
        {"year": "{{ipo_1995.value}}", "label": "Independent, listed in Amsterdam + New York", "cue": "fully independent"}]},
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
kinetic("s16_insurance", "m2_insurance", [
    ("For the customers: insurance", 58, "insurance", "accent", False),
    ("No machine → their roadmaps stall", 46, "never arrived", "risk", True),
    ("Machine arrives → first in line", 46, "first in", "accent3", True)], chapter="Mission 2 · The bet")
add("s17_pieces", "m2_pieces", "timeline_network", {
    "title": "Buying the missing pieces", "title_cue": "missing pieces", "subtitle": "Light source and optics",
    "start_year": 1980, "end_year": 2025, "tick_every": 5, "axis_cue": "missing pieces",
    "items": [
        {"year": "{{founded_1984.value}}", "label": "ASML founded", "place": "ASML · Veldhoven", "role": "design + assembly", "lon": LL["veldhoven"][0], "lat": LL["veldhoven"][1], "colour": "accent", "cue": "missing pieces", "label_dx": -18},
        {"year": 2012, "label": "Agrees to buy Cymer", "place": "Cymer · San Diego", "role": "light source", "lon": LL["sandiego"][0], "lat": LL["sandiego"][1], "colour": "accent2", "cue": "Cymer"},
        {"year": 2016, "label": "24.9% of Zeiss SMT", "place": "Zeiss · Oberkochen", "role": "mirrors", "lon": LL["oberkochen"][0], "lat": LL["oberkochen"][1], "colour": "accent3", "cue": "Carl Zeiss", "label_dx": 18, "label_dy": 40},
        {"year": "{{euv_2020.value}}", "label": "EUV in high-volume production", "place": "", "role": "", "lon": LL["veldhoven"][0], "lat": LL["veldhoven"][1], "colour": "accent", "cue": "high volume"},
    ],
    "links": [[1, 0], [2, 0]], "morph_cue": "production", "view": {"lon": -55, "lat": 45, "span": 160},
    "highlight": {"NLD": "accent", "USA": "accent2", "DEU": "accent3"}, "network_title": "One machine, three companies"},
    sources=["cymer_2012", "asml_ar_2025", "asml_history", "natural_earth"], assets=GEO)
add("s18_share", "m2_discovery", "engine_chart", {"chart": "donut", "title": "Who makes lithography machines?", "subtitle": "Analyst estimate (Reuters) · for EUV, ASML is the only maker",
    "data": [{"label": "ASML", "value": 90}, {"label": "Everyone else", "value": 10}], "cx": 960, "cy": 600, "r": 230, "thick": 80,
    "start": C("analysts estimate"), "sweep": 1.6, "center": "{{market_90.display}}", "centerSub": "ASML (estimate)"},
    sources=["reuters_explainer"])
kinetic("s19_m2t", "m2_transition", [("Never built by one company", 56, "never built", None, True), ("Who else is inside it?", 76, "Who else", "accent", False), ("Mission 3 →", 44, "Mission three", "muted", False)])

# ====================================================================== MISSION 3
card("s20_m3", "m3_card", "Mission 3", "Who Builds It", "The monopoly is a network")
question("s21_m3q", "m3_question", "Mission 3 · Who builds it", "Who actually builds this machine?", "The monopoly is a network, not one company", "Who actually", "It matters")
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
    sources=["asml_ar_2025", "zeiss_capacity", "cymer_2012", "natural_earth"], assets=GEO)
add("s24_ship", "m3_shipping", "engine_flow", {
    "title": "Built twice", "subtitle": "assembled and tested in the Netherlands, rebuilt at the customer", "cardW": 280, "cardH": 230,
    "stages": [
        {"id": "b", "label": "Build", "sub": "Veldhoven", "x": 230, "y": 560, "kind": "fab", "color": "gold", "appear": 0.3, "output": "box"},
        {"id": "t", "label": "Test", "sub": "full run-in", "x": 595, "y": 560, "kind": "company", "color": "accent2", "appear": 0.45, "output": "box"},
        {"id": "p", "label": "Take apart", "sub": "≈ 40 containers", "x": 960, "y": 560, "kind": "warehouse", "color": "teal", "appear": 0.6, "output": "box"},
        {"id": "f", "label": "Fly", "sub": "cargo planes", "x": 1325, "y": 560, "kind": "company", "color": "accent2", "appear": 0.75, "output": "box"},
        {"id": "r", "label": "Rebuild", "sub": "customer's fab", "x": 1690, "y": 560, "kind": "fab", "color": "gold", "appear": 0.9, "output": "wafer"}],
    "links": [{"from": "b", "to": "t", "appear": 1.0}, {"from": "t", "to": "p", "appear": 1.1}, {"from": "p", "to": "f", "appear": 1.2}, {"from": "f", "to": "r", "appear": 1.3}],
    "items": {"starts": [C("built and tested")], "route": ["b", "t", "p", "f", "r"], "travel": 0.7, "process": 1.2},
    "money": [{"from": "r", "to": "b", "starts": [C("paying"), C("paying", 0.3), C("paying", 0.6)], "travel": 1.2, "label": "FULL PAYMENT", "lift": 0.18}]},
    sources=["reuters_explainer", "intel_euv"])
kinetic("s25_m3t", "m3_transition", [("Where does all the money go?", 60, "So where", None, True), ("Mission 4 →", 44, "Mission four", "muted", False)])

# ====================================================================== MISSION 4
card("s26_m4", "m4_card", "Mission 4", "How It Makes Money", "Machines, research, and a loop")
question("s27_m4q", "m4_question", "Mission 4 · How it makes money", "How does ASML make money?", "It sits in the middle of the AI boom", "How does", "It matters")
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
add("s29_avg", "m4_average", "compare", {"chapter": "Mission 4 · Per machine", "title": "What one EUV machine brings in", "sides": [
    {"kicker": "EUV sales, 2025", "value": "{{euv_sales_2025.usd_display}}", "label": "{{euv_sales_2025.display}} machines", "cue": "average"},
    {"kicker": "Average per machine", "value": "{{euv_sales_2025.avg_display}}", "label": "our calculation", "cue": "per machine"},
    {"kicker": "Exchange rate used", "value": "{{eur_usd.display}}", "label": "ECB average rate, 2025", "cue": "converted"}]},
    sources=["asml_q4_2025_deck", "ecb_2025_avg"])
add("s30_regions", "m4_customers", "engine_chart", {"chart": "bar", "data": "{{regions.value}}", "box": {"x": 300, "y": 330, "w": 1320, "h": 500},
    "start": C("who buys"), "stagger": 0.25, "title": "Who buys ASML's machines", "note": "Share of 2025 net system sales",
    "valueSuffix": "%", "highlight": 0, "highlightAt": C("China took"), "color": "accent2", "highlightColor": "risk"},
    sources=["regions_2025"])
add("s31_loop", "m4_flywheel", "engine_flow", {
    "title": "The money loop", "subtitle": "order backlog at the end of 2025: {{backlog.display}}", "cardW": 290, "cardH": 220,
    "stages": [
        {"id": "c", "label": "Chipmakers", "sub": "buy machines", "x": 420, "y": 600, "kind": "customer", "color": "accent2", "appear": 0.3, "output": "coin"},
        {"id": "a", "label": "ASML", "sub": "sales", "x": 960, "y": 380, "kind": "bank", "color": "gold", "appear": 0.45, "output": "coin"},
        {"id": "r", "label": "Research", "sub": "{{rd_2025.display}} a year", "x": 1500, "y": 600, "kind": "design", "color": "accent3", "appear": 0.6, "output": "blueprint"},
        {"id": "m", "label": "Next machine", "sub": "they need it", "x": 960, "y": 850, "kind": "fab", "color": "gold", "appear": 0.75, "output": "box"}],
    "links": [{"from": "c", "to": "a", "appear": 0.9}, {"from": "a", "to": "r", "appear": 1.0}, {"from": "r", "to": "m", "appear": 1.1}, {"from": "m", "to": "c", "appear": 1.2}],
    "items": {"starts": [C("Chipmakers pay"), C("order again", -1.0)], "route": ["c", "a", "r", "m", "c"], "travel": 0.8, "process": 0.9}},
    sources=["asml_ar_2025", "asml_q4_2025", "ecb_2025_avg"])
kinetic("s32_m4t", "m4_transition", [("A machine this valuable", 58, "A machine", None, True), ("is also a weapon", 80, "weapon", "risk", False), ("Mission 5 →", 44, "Mission five", "muted", False)])

# ====================================================================== MISSION 5
card("s33_m5", "m5_card", "Mission 5", "Where the Machine May Go", "Export controls and the price of a gate")
question("s34_m5q", "m5_question", "Mission 5 · Where the machine may go", "Who decides where these machines can go?",
         "Control the machine, control the most advanced chips", "Who decides", "It matters")
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
    sources=["cnbc_export", "ioplus_2024", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "not to China", "gain": 0.3}])
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
add("s37_cost", "m5_cost", "compare", {"chapter": "Mission 5 · The price of the gate", "title": "The gate cuts both ways", "sides": [
    {"kicker": "China, share of ASML sales", "value": "{{regions.display}} → {{china_2026.display}}", "label": "2025 → 2026 (CFO expectation)", "cue": "chief financial officer"},
    {"kicker": "Next generation (High-NA)", "value": "{{highna_price.display}}", "label": "first one went to Intel, Dec 2023", "cue": "next"}]},
    sources=["regions_2025", "caixin_china", "highna_reuters"])

# ====================================================================== PAYOFF
add("s38_payoff", "payoff", "engine_map", {
    "cameras": [{"at": 0, "lon": 40, "lat": 35, "span": 300}, {"at": C("forty years"), "lon": 20, "lat": 45, "span": 150, "dur": 2.4},
                {"at": C("small town"), "lon": 5.43, "lat": 51.6, "span": 6, "dur": 2.4}, {"at": C("drop of tin"), "lon": 5.43, "lat": 51.5, "span": 2.5, "dur": 3.0}],
    "drift": {"lon": 0.1, "zoom": 0.006}, "tilt": [[0, 16], [30, 4]],
    "highlights": [{"iso": "NLD", "color": "gold", "at": 0.2}],
    "hubs": [{"id": "v", "at": LL["veldhoven"], "label": "Veldhoven", "sub": "one Dutch machine", "color": "gold", "time": 0.3},
             {"id": "z", "at": LL["oberkochen"], "label": "Zeiss", "color": "teal", "time": C("network of suppliers")},
             {"id": "s", "at": LL["sandiego"], "label": "Cymer", "color": "accent2", "time": C("network of suppliers", 0.3)}],
    "routes": [{"from": LL["oberkochen"], "to": LL["veldhoven"], "at": C("network of suppliers"), "dur": 0.8, "color": "teal", "tokenShape": "box", "lift": 0.3},
               {"from": LL["sandiego"], "to": LL["veldhoven"], "at": C("network of suppliers", 0.3), "dur": 1.0, "color": "accent2", "tokenShape": "box"},
               {"from": LL["veldhoven"], "to": LL["hsinchu"], "at": C("customers who paid"), "dur": 1.0, "color": "gold", "tokenShape": "box"},
               {"from": LL["veldhoven"], "to": LL["hwaseong"], "at": C("customers who paid", 0.2), "dur": 1.0, "color": "gold", "tokenShape": "box"},
               {"from": LL["veldhoven"], "to": LL["hillsboro"], "at": C("customers who paid", 0.4), "dur": 1.0, "color": "gold", "tokenShape": "box"}],
    "caption": "Mission complete"},
    sources=["asml_history", "natural_earth"], assets=GEO)
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "the cables under the ocean"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

OUT.write_text("# GENERATED by tools/gen_asml_storyboard.py; edit the generator, not this file.\n"
               "# Episode 08 storyboard on the animation engine. The channel intro is inserted automatically after the hook.\n"
               + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
print(f"{len(scenes)} scenes -> {OUT}")
