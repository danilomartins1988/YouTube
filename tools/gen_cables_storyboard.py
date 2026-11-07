"""Generates projects/the-cables-at-the-bottom-of-the-ocean/deliverables/documentary/storyboard.yaml (Episode 09).

Built on the animation engine: cartoon ocean scenes (engine_cartoon), presenter boards, pen drawings, maps and flows.
The five parts are an internal structure only: nothing on screen or in the narration says "mission".
Times are narration cues ({cue: "..."}) wherever possible. Run: python tools/gen_cables_storyboard.py
"""
from __future__ import annotations

import math
import re
from pathlib import Path

import yaml

OUT = Path(__file__).resolve().parents[1] / "projects/the-cables-at-the-bottom-of-the-ocean/deliverables/documentary/storyboard.yaml"
INTER = ["font:inter"]
GEO = ["geo:remotion_world", "font:inter"]
BOARD = {"x": 470, "y": 230, "w": 1370, "h": 800}
C = lambda cue, off=None: ({"cue": cue, "offset": off} if off is not None else {"cue": cue})

# Real places (lon, lat). Map routes between them are SCHEMATIC arcs, not real cable paths (said on screen).
LL = {"newyork": [-74.0, 40.7], "bude": [-4.5, 50.8], "lisbon": [-9.1, 38.7], "marseille": [5.37, 43.3], "fortaleza": [-38.5, -3.7],
      "lagos": [3.4, 6.45], "capetown": [18.4, -33.9], "mumbai": [72.8, 19.0], "singapore": [103.8, 1.35], "hongkong": [114.17, 22.3],
      "tokyo": [139.7, 35.7], "losangeles": [-118.2, 34.0], "sydney": [151.2, -33.9], "taiwan": [121.0, 25.0], "manila": [121.0, 14.6],
      "djibouti": [43.1, 11.6], "jeddah": [39.2, 21.5], "suez": [32.5, 29.9], "redsea": [41.0, 16.5], "tonga": [-175.2, -21.1],
      "mombasa": [39.7, -4.05], "portsudan": [37.2, 19.6], "aden": [45.0, 12.8], "oman": [58.4, 23.6], "usa": [-77.0, 38.9], "japan": [139.7, 35.7], "france": [2.35, 48.86], "china": [116.4, 39.9]}

scenes: list[dict] = []


def mission_of(segment: str) -> int:
    m = re.match(r"m(\d)_", segment)
    return int(m.group(1)) if m else (6 if segment in ("payoff", "teaser") else 0)


def add(id_, segment, type_, params, sources=(), assets=INTER, sfx=None, stamp=None):
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
    add(id_, seg, "act_title", {"number": "", "title": title, "subtitle": sub, "min_seconds": 4.2}, sfx=[{"kind": "hit", "at": 0.1, "gain": 0.25}])


def question(id_, seg, chapter, q, why, q_cue, why_cue):
    add(id_, seg, "kinetic_text", {"align": "center", "chapter": chapter, "lines": [
        {"text": "THE QUESTION", "size": 34, "style": "body", "color": "muted", "cue": q_cue},
        {"text": q, "size": 64, "color": "accent", "cue": q_cue, "offset": 0.4},
        {"text": "WHY IT MATTERS", "size": 34, "style": "body", "color": "muted", "cue": why_cue},
        {"text": why, "size": 48, "style": "body", "cue": why_cue, "offset": 0.4}]})


def kinetic(id_, seg, lines, chapter=None, stamp=None, sfx=None):
    p = {"align": "center", "lines": [{"text": tx, "size": sz, "cue": cu, **({"color": co} if co else {}), **({"style": "body"} if st else {})}
                                      for tx, sz, cu, co, st in lines]}
    if chapter:
        p["chapter"] = chapter
    add(id_, seg, "kinetic_text", p, stamp=stamp, sfx=sfx)


def transition(id_, seg, n, l1, l2, c1, c2, nxt, ncue, stamp_cue):
    lines = [(l1, 56, c1, None, True), (l2, 74, c2, "accent", False)]
    if nxt:
        lines.append((nxt, 44, ncue, "muted", False))
    kinetic(id_, seg, lines)


def rect(x, y, w, h):
    return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"


def circle(cx, cy, r):
    return f"M {cx - r} {cy} A {r} {r} 0 1 0 {cx + r} {cy} A {r} {r} 0 1 0 {cx - r} {cy}"


def arrow(a, b, bend=0.0):
    mx, my = (a[0] + b[0]) / 2 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2 + (b[0] - a[0]) * bend
    ang = math.atan2(b[1] - my, b[0] - mx)
    h1 = (b[0] - 24 * math.cos(ang - 0.45), b[1] - 24 * math.sin(ang - 0.45))
    h2 = (b[0] - 24 * math.cos(ang + 0.45), b[1] - 24 * math.sin(ang + 0.45))
    return f"M {a[0]} {a[1]} Q {mx:.0f} {my:.0f} {b[0]} {b[1]} M {h1[0]:.0f} {h1[1]:.0f} L {b[0]} {b[1]} L {h2[0]:.0f} {h2[1]:.0f}"


def lbl(text, x, y, size=30, color="ink", anchor="middle"):
    return {"text": text, "x": x, "y": y, "size": size, "color": color, "anchor": anchor}


def dot(x, y):  # an invisible anchor stroke that only writes a label
    return f"M {x} {y} L {x} {y}"


# a schematic "web" of cables between real coastal cities (hook + payoff)
WEB = [("newyork", "bude"), ("newyork", "lisbon"), ("fortaleza", "lisbon"), ("lagos", "lisbon"), ("capetown", "lagos"),
       ("marseille", "mumbai"), ("mumbai", "singapore"), ("singapore", "hongkong"), ("hongkong", "tokyo"), ("tokyo", "losangeles"),
       ("losangeles", "sydney"), ("singapore", "sydney"), ("capetown", "mumbai")]


def web_routes(at0, step, color="accent2"):
    return [{"from": LL[a], "to": LL[b], "at": (at0 + i * step) if isinstance(at0, (int, float)) else at0, "dur": 1.2, "color": color,
             "tokenShape": "packet", "tokens": 4, "tokenEvery": 0.5, "lift": 0.18} for i, (a, b) in enumerate(WEB)]


# ====================================================================== HOOK
add("s01_seabed", "h_question", "engine_draw", {
    "title": "Not in the sky", "presenter": False, "studio": False, "push": 0.004, "draw_start": 0.3, "speed": 1500,
    "strokes": [
        {"d": "M 200 330 Q 520 300 840 330 Q 1160 360 1480 330 Q 1640 315 1720 330", "color": "accent2", "width": 4, "flow": 90, "start": 0.3, "label": lbl("SEA SURFACE", 220, 300, 24, "accent2", "start")},
        {"d": "M 1500 160 L 1560 200 M 1530 180 L 1590 140", "color": "muted", "width": 4, "start": C("in the sky"), "label": lbl("SATELLITE?", 1600, 130, 24, "muted", "start")},
        {"d": "M 200 900 Q 600 860 960 920 Q 1320 970 1720 900", "color": "border", "width": 5, "start": C("but at the bottom"), "label": lbl("SEABED", 220, 960, 24, "muted", "start")},
        {"d": "M 200 880 Q 600 840 960 900 Q 1320 950 1720 880", "color": "accent2", "width": 7, "flow": 320, "pulse": True, "start": C("bottom of the ocean"), "label": lbl("THE INTERNET", 960, 820, 40, "accent2")},
    ]})
add("s02_web", "h_stakes", "engine_map", {
    "title": "{{itu_99.display}} of international data", "subtitle": "{{itu_99.cables_display}} cables · {{itu_99.km_display}} (ITU, 2025)",
    "cameras": [{"at": 0, "lon": 20, "lat": 15, "span": 330}, {"at": C("Every video"), "lon": 40, "lat": 20, "span": 260, "dur": 3.0}],
    "drift": {"lon": 0.4, "zoom": 0.004}, "tilt": [[0, 14], [12, 6]],
    "routes": web_routes(C("travels through"), 0.25),
    "caption": "Schematic links between real coastal cities (Natural Earth), not actual cable routes"},
    sources=["itu_2025", "natural_earth"], assets=GEO)
kinetic("s03_missions", "h_missions", [
    ("Today: five missions", 64, "five missions", "accent", False),
    ("1 · Follow the light across the ocean", 40, "Follow the light", None, True),
    ("2 · Find out who owns the cables", 40, "who owns", None, True),
    ("3 · Meet who builds and fixes them", 40, "build and fix", None, True),
    ("4 · See what happens when one breaks", 40, "one breaks", None, True),
    ("5 · The fight over the seabed", 40, "fight", "risk", True)], chapter="Five missions")

# ====================================================================== MISSION 1
card("s04_m1", "m1_card", "Mission 1", "How the Internet Crosses the Ocean", "Follow the light")
question("s05_m1q", "m1_question", "How the internet crosses the ocean", "How does the internet cross an ocean?",
         "Most people think it goes through satellites", "How does", "It matters")
add("s06_sat", "m1_satellite", "compare", {"chapter": "Not satellites", "title": "Cables, not satellites", "sides": [
    {"kicker": "Satellites, U.S. international capacity", "value": "{{satellite.display}}", "label": "FCC statistics, via TeleGeography", "cue": "government"},
    {"kicker": "Traffic between continents", "value": "{{tg_check.display}}", "label": "carried by cables (TeleGeography)", "cue": "between continents"}]},
    sources=["tg_faq", "tg_myth_2023"])
# ---- PRESENTER A: data crossing the ocean
add("p07_draw", "m1_draw", "engine_draw", {
    "title": "How your data crosses the ocean", "board": BOARD, "draw_start": C("Your data"), "speed": 1200,
    "enter": {"from": -260, "to": 420, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(540, 290, 190, 100), "color": "accent", "width": 5, "start": C("leaves a data center"), "label": lbl("DATA CENTER", 635, 350, 24, "accent")},
        {"d": arrow((640, 400), (690, 445)), "color": "ink", "width": 4, "start": C("reaches the coast")},
        {"d": rect(610, 450, 180, 66), "color": "accent3", "width": 5, "start": C("landing station"), "label": lbl("LANDING STATION", 700, 492, 19, "accent3")},
        {"d": "M 520 520 L 800 520 L 880 900", "color": "border", "width": 4, "start": C("landing station", 0.6), "kind": "map"},
        {"d": "M 820 520 Q 1000 500 1160 520 Q 1320 540 1490 520", "color": "accent2", "width": 3, "dash": "12 10", "start": C("enters a cable")},
        {"d": "M 790 516 Q 840 880 1000 900 L 1320 900 Q 1480 880 1530 516", "color": "accent2", "width": 7, "flow": 320, "start": C("on the seabed"), "label": lbl("CABLE ON THE SEABED", 1160, 960, 26, "accent2")},
        {"d": dot(1160, 850), "color": "accent2", "width": 1, "start": C("pulses of light"), "label": lbl("PULSES OF LIGHT IN GLASS", 1160, 860, 22, "ink")},
        {"d": "M 1820 520 L 1520 520 L 1440 900", "color": "border", "width": 4, "start": C("another continent", -0.4), "kind": "map"},
        {"d": rect(1530, 450, 180, 66), "color": "accent3", "width": 5, "start": C("another landing station"), "label": lbl("LANDING STATION", 1620, 492, 19, "accent3")},
        {"d": arrow((1620, 445), (1680, 400)), "color": "ink", "width": 4, "start": C("goes on")},
        {"d": rect(1590, 290, 190, 100), "color": "accent", "width": 5, "start": C("its destination"), "label": lbl("DESTINATION", 1685, 350, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("glass fibers", 0.2), "dur": 1.4, "target": [1000, 880]}, {"kind": "explain", "at": C("Then it goes", -0.2), "dur": 2.5}],
    "scale": 0.86, "floor": 1040}, sources=["tg_faq"])
# ---- pen drawing: light in a fibre
pulses = " ".join(f"M {500 + i * 120} 560 L {560 + i * 120} 560" for i in range(10))
add("s08_light", "m1_light", "engine_draw", {
    "title": "Data as flashes of light", "subtitle": "each fiber is roughly as thin as a human hair", "presenter": False, "studio": False, "push": 0.003,
    "draw_start": C("Why light"), "speed": 1500,
    "strokes": [
        {"d": "M 420 500 L 1700 500 M 420 620 L 1700 620", "color": "border", "width": 4, "start": C("Why light"), "label": lbl("GLASS FIBER", 420, 470, 28, "muted", "start")},
        {"d": "M 420 560 L 1700 560", "color": "accent2", "width": 6, "flow": 400, "start": C("enormous amount"), "label": lbl("LIGHT", 1720, 570, 28, "accent2", "start")},
        {"d": dot(960, 420), "color": "ink", "width": 1, "start": C("human hair"), "label": lbl("≈ THE WIDTH OF A HUMAN HAIR", 960, 420, 30, "ink")},
        {"d": pulses, "color": "accent", "width": 10, "pulse": True, "start": C("on and off"), "label": lbl("ON · OFF · ON · ON · OFF = DATA", 960, 720, 30, "accent")},
        {"d": " ".join(f"M 420 {820 + i * 22} L 1700 {820 + i * 22}" for i in range(6)), "color": "accent2", "width": 3, "flow": 260, "start": C("many fibers"),
         "label": lbl("MANY FIBERS IN ONE CABLE", 960, 1000, 28, "accent2")},
    ]}, sources=["tg_faq"])
add("s09_size", "m1_discovery", "compare", {"chapter": "The discovery", "title": "One cable", "sides": [
    {"kicker": "Width, in the deep ocean", "value": "Garden hose", "label": "for most of its journey", "cue": "as wide as"},
    {"kicker": "Near the shore", "value": "+ armor", "label": "against fishing gear and anchors", "cue": "extra armor"},
    {"kicker": "Built to last at least", "value": "{{design_life.display}}", "label": "minimum design life", "cue": "built to last"}]},
    sources=["tg_faq"])
transition("s10_m1t", "m1_transition", 1, "Something this important", "belongs to someone", "So something", "belong to", None, None, "But who")

# ====================================================================== MISSION 2
card("s11_m2", "m2_card", "Mission 2", "Who Owns the Cables", "From phone clubs to tech giants")
question("s12_m2q", "m2_question", "Who owns the cables", "Who owns the cables at the bottom of the ocean?",
         "Whoever owns the road decides who uses it, and what it costs", "Who owns", "It matters")
# ---- PRESENTER B: the consortium model
add("p13_club", "m2_draw", "engine_draw", {
    "title": "The old way: a club of phone companies", "board": BOARD, "draw_start": C("owned by telephone"), "speed": 1300,
    "enter": {"from": 2200, "to": 1560, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(560, 330, 240, 90), "color": "accent2", "width": 5, "start": C("telephone companies"), "label": lbl("TELECOM A", 680, 387, 26)},
        {"d": rect(560, 480, 240, 90), "color": "accent2", "width": 5, "start": C("telephone companies", 0.4), "label": lbl("TELECOM B", 680, 537, 26)},
        {"d": rect(560, 630, 240, 90), "color": "accent2", "width": 5, "start": C("telephone companies", 0.8), "label": lbl("TELECOM C", 680, 687, 26)},
        {"d": rect(1010, 450, 300, 150), "color": "accent", "width": 6, "start": C("consortium"), "label": lbl("CONSORTIUM", 1160, 535, 34, "accent")},
        {"d": arrow((810, 375), (1000, 480), -0.06), "color": "ink", "width": 4, "start": C("paid for a share")},
        {"d": arrow((810, 525), (1000, 525), 0), "color": "ink", "width": 4},
        {"d": arrow((810, 675), (1000, 570), 0.06), "color": "ink", "width": 4},
        {"d": "M 1160 610 L 1160 760", "color": "accent2", "width": 6, "flow": 260, "start": C("share of its capacity"), "label": lbl("CABLE CAPACITY", 1160, 800, 26, "accent2")},
        {"d": rect(560, 860, 300, 90), "color": "accent3", "width": 5, "start": C("new companies"), "label": lbl("PRIVATE CABLE", 710, 917, 26, "accent3")},
        {"d": arrow((870, 905), (1090, 905)), "color": "accent3", "width": 4, "start": C("selling the")},
        {"d": dot(1240, 915), "color": "ink", "width": 1, "start": C("anyone who"), "label": lbl("SOLD TO ANYONE", 1240, 915, 26, "ink")},
    ],
    "actions": [{"kind": "explain", "at": C("Several of them", 0.3), "dur": 3.0}, {"kind": "point", "at": C("new companies", 0.6), "dur": 1.2, "target": [740, 905]}],
    "scale": 0.86, "floor": 1040}, sources=["tg_faq"])
add("s14_shift", "m2_shift", "compare", {"chapter": "The users changed", "title": "Who uses the international bandwidth", "sides": [
    {"kicker": "2016", "value": "Majority", "label": "internet backbone providers", "cue": "backbone companies"},
    {"kicker": "2024", "value": "{{content_share.display}}", "label": "content and cloud companies", "cue": "content and"},
    {"kicker": "A handful of names", "value": "4", "label": "Google · Meta · Microsoft · Amazon", "cue": "handful"}]},
    sources=["tg_bandwidth_2025"])
kinetic("s15_demand", "m2_demand", [
    ("International bandwidth demand", 44, "demand keeps", None, True),
    ("× 3", 120, "tripled", "accent2", False),
    ("2020 → 2024 · more than {{demand_2024.display}}", 44, "more than", None, True),
    ("streaming · cloud · AI", 40, "Streaming", "muted", True)], chapter="Demand")
AFR = [("marseille", "lagos"), ("lagos", "capetown"), ("capetown", "mombasa"), ("mombasa", "oman"), ("oman", "suez"), ("suez", "marseille")]
add("s16_africa", "m2_africa", "engine_map", {
    "title": "2Africa (as planned in 2020)", "subtitle": "{{africa2.display}} · {{africa2.countries_display}} countries · Africa, Middle East, Europe",
    "cameras": [{"at": 0, "lon": 40, "lat": 25, "span": 300}, {"at": C("One example"), "lon": 20, "lat": 5, "span": 120, "dur": 2.4}],
    "drift": {"lon": 0.15, "zoom": 0.003}, "tilt": [[0, 12], [20, 5]],
    "routes": [{"from": LL[a], "to": LL[b], "at": C("planned at", i * 0.35), "dur": 1.0, "color": "accent", "tokenShape": "packet", "tokens": 4, "tokenEvery": 0.5, "lift": 0.12}
               for i, (a, b) in enumerate(AFR)],
    "caption": "Planned loop shown schematically (Natural Earth basemap)"},
    sources=["meta_2africa", "natural_earth"], assets=GEO)
add("s17_private", "m2_discovery", "engine_flow", {
    "title": "From renting to owning", "subtitle": "the companies that fill the cables now pay to lay them", "cardW": 280, "cardH": 220,
    "stages": [
        {"id": "u", "label": "Users", "sub": "videos · cloud · AI", "x": 300, "y": 600, "kind": "customer", "color": "accent3", "appear": 0.3, "output": "packet"},
        {"id": "c", "label": "Tech giant", "sub": "content + cloud", "x": 760, "y": 600, "kind": "datacenter", "color": "accent", "appear": 0.45, "output": "packet"},
        {"id": "k", "label": "Its own cable", "sub": "no waiting, no renting", "x": 1220, "y": 600, "kind": "company", "color": "accent2", "appear": 0.6, "output": "packet"},
        {"id": "d", "label": "Data center", "sub": "another continent", "x": 1660, "y": 600, "kind": "datacenter", "color": "accent", "appear": 0.75, "output": "packet"}],
    "links": [{"from": "u", "to": "c", "appear": 0.9}, {"from": "c", "to": "k", "appear": 1.0}, {"from": "k", "to": "d", "appear": 1.1}],
    "items": {"starts": [C("fill the cables"), C("fill the cables", 0.8), C("Owning the cable")], "route": ["u", "c", "k", "d"], "travel": 0.7, "process": 0.8},
    "money": [{"from": "c", "to": "k", "starts": [C("paying to lay"), C("paying to lay", 0.4)], "travel": 1.0, "label": "PAYS TO BUILD", "lift": 0.2}]},
    sources=["tg_faq", "tg_bandwidth_2025"])
transition("s18_m2t", "m2_transition", 2, "Owning a cable is one thing", "Building and fixing one is another", "But owning", "Building one", None, None, "is another")

# ====================================================================== MISSION 3
card("s19_m3", "m3_card", "Mission 3", "Who Builds and Fixes Them", "A few factories, a small fleet")
question("s20_m3q", "m3_question", "Who builds and fixes them", "Who builds these cables, and who fixes them?",
         "Very few companies on Earth can do it", "Who builds", "It matters")
# ---- pen drawing: cable cross-section (schematic)
add("s21_layers", "m3_layers", "engine_draw", {
    "title": "Inside a cable", "subtitle": "schematic cross-section, not to scale", "presenter": False, "studio": False, "push": 0.004,
    "draw_start": C("open one up"), "speed": 1400,
    "strokes": [
        {"d": " ".join(circle(760 + dx, 600 + dy, 14) for dx, dy in [(-30, 0), (30, 0), (0, -30), (0, 30), (-21, -21), (21, 21), (21, -21), (-21, 21)]), "color": "accent2", "width": 4, "pulse": True,
         "start": C("glass fibers"), "label": lbl("GLASS FIBERS · CARRY THE LIGHT", 1060, 380, 30, "accent2", "start")},
        {"d": arrow((1050, 395), (800, 560), 0.1), "color": "accent2", "width": 3, "start": C("carry the light")},
        {"d": circle(760, 600, 110), "color": "ink", "width": 8, "start": C("layers of plastic"), "label": lbl("PLASTIC LAYERS · PROTECTION", 1060, 520, 30, "ink", "start")},
        {"d": circle(760, 600, 150), "color": "muted", "width": 10, "dash": "6 10", "start": C("steel wire"), "label": lbl("STEEL WIRE · SOMETIMES", 1060, 660, 30, "muted", "start")},
        {"d": circle(760, 600, 200), "color": "accent", "width": 14, "start": C("extra armor"), "label": lbl("EXTRA ARMOR · NEAR THE COAST", 1060, 800, 30, "accent", "start")},
        {"d": "M 420 950 L 1700 950", "color": "border", "width": 3, "flow": 200, "start": C("Very hard to make"), "label": lbl("ONE PIECE, ACROSS AN OCEAN · BUILT FOR DECADES", 1060, 1010, 26, "muted")},
    ]}, sources=["tg_faq"])
add("s22_builders", "m3_builders", "engine_map", {
    "title": "Who builds the cables", "subtitle": "three companies have dominated for decades (Reuters)",
    "cameras": [{"at": 0, "lon": 20, "lat": 35, "span": 320}, {"at": C("SubCom"), "lon": 10, "lat": 30, "span": 340, "dur": 2.0}],
    "drift": {"lon": 0.2, "zoom": 0.003}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "USA", "color": "accent2", "at": C("SubCom")}, {"iso": "JPN", "color": "accent2", "at": C("NEC")},
                   {"iso": "FRA", "color": "accent2", "at": C("Alcatel")}, {"iso": "CHN", "color": "risk", "at": C("HMN"), "strength": 0.7}],
    "hubs": [{"id": "s", "at": LL["usa"], "label": "SubCom", "sub": "United States", "color": "accent2", "time": C("SubCom"), "anchor": "end"},
             {"id": "n", "at": LL["japan"], "label": "NEC", "sub": "Japan", "color": "accent2", "time": C("NEC")},
             {"id": "a", "at": LL["france"], "label": "Alcatel Submarine Networks", "sub": "France", "color": "accent2", "time": C("Alcatel")},
             {"id": "h", "at": LL["china"], "label": "HMN Tech", "sub": "China · fastest growing", "color": "risk", "time": C("HMN"), "anchor": "end"}],
    "caption": "Markers show the company's country, not a site · Natural Earth"},
    sources=["reuters_smw6", "lightreading_smw6", "natural_earth"], assets=GEO)
add("s23_repair", "m3_repair", "engine_flow", {
    "title": "How a broken cable gets fixed", "subtitle": "repair ships are stationed around the world (ICPC)", "cardW": 270, "cardH": 220,
    "stages": [
        {"id": "f", "label": "Cable breaks", "sub": "traffic rerouted", "x": 230, "y": 580, "kind": "warehouse", "color": "risk", "appear": 0.3, "output": "packet"},
        {"id": "s", "label": "Ship sails", "sub": "repair vessel", "x": 595, "y": 580, "kind": "company", "color": "accent", "appear": 0.45, "output": "box"},
        {"id": "l", "label": "Find + lift", "sub": "damaged section", "x": 960, "y": 580, "kind": "warehouse", "color": "accent2", "appear": 0.6, "output": "box"},
        {"id": "r", "label": "Repair at sea", "sub": "new section", "x": 1325, "y": 580, "kind": "fab", "color": "accent", "appear": 0.75, "output": "packet"},
        {"id": "o", "label": "Back online", "sub": "Baltic 2024: {{repair_ships.display}}", "x": 1690, "y": 580, "kind": "datacenter", "color": "accent3", "appear": 0.9, "output": "packet"}],
    "links": [{"from": "f", "to": "s", "appear": 1.0}, {"from": "s", "to": "l", "appear": 1.1}, {"from": "l", "to": "r", "appear": 1.2}, {"from": "r", "to": "o", "appear": 1.3}],
    "items": {"starts": [C("has to sail"), C("bring it up"), C("ready to go")], "route": ["f", "s", "l", "r", "o"], "travel": 0.7, "process": 1.0}},
    sources=["icpc_media"])
kinetic("s23b_m3d", "m3_discovery", [
    ("A handful of factories", 58, "handful of factories", None, True),
    ("+ a small fleet of ships", 58, "small fleet", "accent2", True),
    ("Control the builder → a say in who connects", 50, "control who builds", "accent", False)], chapter="The discovery")
transition("s24_m3t", "m3_transition", 3, "Repair ships are busy", "Cables break more often than you think", "And those repair ships", "break far", None, None, "you might think")

# ====================================================================== MISSION 4
card("s25_m4", "m4_card", "Mission 4", "When a Cable Breaks", "Anchors, nets and a volcano")
question("s26_m4q", "m4_question", "When a cable breaks", "What happens when a cable breaks?",
         "One cut can slow down, or switch off, a whole region", "What happens", "It matters")
add("s27_faults", "m4_faults", "compare", {"chapter": "How often", "title": "Cables break all the time", "sides": [
    {"kicker": "Faults every year", "value": "{{faults.display}}", "label": "worldwide (ICPC)", "cue": "cable faults"},
    {"kicker": "Caused by accidents", "value": "{{faults.human_display}}", "label": "mostly fishing gear and anchors", "cue": "accidents"},
    {"kicker": "Sabotage", "value": "Rare", "label": "not the main cause", "cue": "Not sabotage"}]},
    sources=["icpc_media"])
RS = [("suez", "djibouti", False), ("suez", "aden", True), ("jeddah", "djibouti", True), ("portsudan", "aden", True), ("jeddah", "aden", False), ("portsudan", "djibouti", False)]
add("s28_redsea", "m4_redsea", "engine_map", {
    "title": "Red Sea, February 2024", "subtitle": "three of more than a dozen cables cut · {{redsea.display}} of the region's traffic (HGC estimate)",
    "cameras": [{"at": 0, "lon": 40, "lat": 22, "span": 60}, {"at": C("Rubymar"), "lon": 39.0, "lat": 20.5, "span": 42, "dur": 2.4}],
    "drift": {"lon": 0.05, "zoom": 0.006}, "tilt": [[0, 12], [20, 6]],
    "hubs": [{"id": "r", "at": LL["redsea"], "label": "Rubymar", "sub": "sank, dragging its anchor", "color": "risk", "time": C("later sank")}],
    "routes": [{"from": LL[a], "to": LL[b], "at": C("it happened", i * 0.25) if not cut else C("cut", (i % 3) * 0.3), "dur": 1.0, "color": "accent2",
                "blocked": cut, "tokenShape": "packet", "tokens": 3, "lift": 0.04 + 0.03 * (i % 3)} for i, (a, b, cut) in enumerate(RS)],
    "caption": "Cut cables: Seacom, AAE-1, EIG · routes schematic (Natural Earth basemap)"},
    sources=["redsea_2024", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "cut", "gain": 0.3}])
# ---- PRESENTER C: why redundancy matters
add("p29_backup", "m4_backup", "engine_draw", {
    "title": "Many routes vs. one route", "board": BOARD, "draw_start": C("more than a dozen"), "speed": 1500,
    "enter": {"from": -260, "to": 420, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(560, 320, 180, 360), "color": "accent", "width": 5, "start": C("more than a dozen"), "label": lbl("REGION A", 650, 300, 24, "accent")},
        {"d": rect(1180, 320, 180, 360), "color": "accent", "width": 5, "start": C("more than a dozen", 0.3), "label": lbl("REGION B", 1270, 300, 24, "accent")},
        *[{"d": f"M 740 {360 + i * 50} L 1180 {360 + i * 50}", "color": "accent2", "width": 4, "flow": 220 if i not in (1, 3, 4) else None, "start": C("more than a dozen", 0.5 + i * 0.12)}
          for i in range(7)],
        {"d": "M 940 395 L 980 435 M 980 395 L 940 435 M 940 495 L 980 535 M 980 495 L 940 535 M 940 545 L 980 585 M 980 545 L 940 585", "color": "risk", "width": 7, "start": C("three go down")},
        {"d": arrow((760, 520), (1160, 650), -0.12), "color": "accent3", "width": 5, "start": C("sent around"), "label": lbl("REROUTED", 960, 720, 24, "accent3")},
        {"d": rect(1480, 440, 140, 120), "color": "accent", "width": 5, "start": C("only one cable"), "label": lbl("ISLAND", 1550, 420, 24, "accent")},
        {"d": "M 1360 500 L 1480 500", "color": "accent2", "width": 4, "start": C("only one cable", 0.3)},
        {"d": "M 1400 470 L 1440 530 M 1440 470 L 1400 530", "color": "risk", "width": 8, "start": C("only one cable", 1.0), "label": lbl("ONE CUT = CUT OFF", 1550, 620, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("sent around", 0.4), "dur": 1.2, "target": [960, 560]}, {"kind": "react", "at": C("only one cable", 1.3)}],
    "scale": 0.86, "floor": 1040}, sources=["redsea_2024"])
for st in scenes[-1]["params"]["strokes"]:
    if st.get("flow") is None:
        st.pop("flow", None)
add("s30_tonga", "m4_tonga", "engine_map", {
    "title": "Tonga, January 2022", "subtitle": "an eruption tore {{tonga.display}} of its cable · offline {{tonga.weeks_display}}",
    "cameras": [{"at": 0, "lon": 175, "lat": -15, "span": 120}, {"at": C("Tonga"), "lon": -176, "lat": -20, "span": 22, "dur": 2.6}],
    "drift": {"lon": 0.03, "zoom": 0.008}, "tilt": [[0, 14], [20, 6]],
    "highlights": [{"iso": "TON", "color": "risk", "at": C("erupted")}],
    "hubs": [{"id": "t", "at": LL["tonga"], "label": "Tonga", "sub": "main link cut · {{tonga.replaced_display}} of new cable", "color": "risk", "time": C("Tonga's main")}],
    "caption": "Real location (Natural Earth, public domain)"},
    sources=["tonga_techxplore", "tonga_aljazeera", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "erupted", "gain": 0.35}])
transition("s31_m4t", "m4_discovery", 4, "Many cables: an inconvenience", "One cable: a blackout", "many cables", "Where there is one", None, None, "a blackout")
kinetic("s32_m4n", "m4_transition", [("Governments want a say", 64, "governments", "accent", False), ("…and where they go", 44, "where they go", "muted", True)])

# ====================================================================== MISSION 5
card("s33_m5", "m5_card", "Mission 5", "The Fight over the Seabed", "Who builds it, who lands it")
question("s34_m5q", "m5_question", "The fight over the seabed", "Why are governments fighting over the seabed?",
         "Your data passes through, and lands in, other countries", "Why are", "It matters")
add("s35_smw6", "m5_smw6", "engine_map", {
    "title": "SEA-ME-WE 6", "subtitle": "Southeast Asia · Middle East · Western Europe",
    "cameras": [{"at": 0, "lon": 60, "lat": 25, "span": 170}, {"at": C("United States government"), "lon": 20, "lat": 30, "span": 300, "dur": 2.4}],
    "drift": {"lon": 0.12, "zoom": 0.003}, "tilt": [[0, 12], [24, 5]],
    "hubs": [{"id": "s", "at": LL["singapore"], "label": "Southeast Asia", "color": "accent2", "time": 0.4},
             {"id": "f", "at": LL["marseille"], "label": "Western Europe", "color": "accent2", "time": 0.8, "anchor": "end"},
             {"id": "h", "at": LL["china"], "label": "HMN Tech", "sub": "chosen in 2020", "color": "risk", "time": C("HMN Tech")},
             {"id": "u", "at": LL["usa"], "label": "SubCom", "sub": "won the contract · bid ≈ ⅓ higher", "color": "accent", "time": C("SubCom won"), "anchor": "end"}],
    "routes": [{"from": LL["singapore"], "to": LL["mumbai"], "at": 0.5, "dur": 1.0, "color": "border", "lift": 0.1},
               {"from": LL["mumbai"], "to": LL["marseille"], "at": 1.2, "dur": 1.2, "color": "border", "lift": 0.12},
               {"from": LL["china"], "to": LL["singapore"], "at": C("pressed the members"), "dur": 1.0, "blocked": True, "lift": 0.2},
               {"from": LL["usa"], "to": LL["marseille"], "at": C("SubCom won"), "dur": 1.2, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["singapore"], "to": LL["mumbai"], "at": C("SubCom won", 1.0), "dur": 1.0, "color": "accent2", "tokenShape": "packet", "lift": 0.1},
               {"from": LL["mumbai"], "to": LL["marseille"], "at": C("SubCom won", 1.6), "dur": 1.2, "color": "accent2", "tokenShape": "packet", "lift": 0.12}],
    "caption": "Route schematic · markers show countries, not sites (Natural Earth)"},
    sources=["reuters_smw6", "lightreading_smw6", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "pressed the members", "gain": 0.3}])
add("s36_plcn", "m5_plcn", "engine_map", {
    "title": "Pacific Light Cable Network", "subtitle": "owned by Google and Meta",
    "cameras": [{"at": 0, "lon": -130, "lat": 30, "span": 120}, {"at": C("across the Pacific"), "lon": -160, "lat": 28, "span": 160, "dur": 3.0}, {"at": C("review recommended"), "lon": 172, "lat": 25, "span": 175, "dur": 2.0}],
    "drift": {"lon": 0.5, "zoom": 0.008}, "tilt": [[0, 16], [20, 6]],
    "hubs": [{"id": "u", "at": LL["losangeles"], "label": "United States", "color": "accent2", "time": 0.4, "anchor": "end"},
             {"id": "h", "at": LL["hongkong"], "label": "Hong Kong", "sub": "leg dropped", "color": "risk", "time": C("Hong Kong"), "anchor": "end"},
             {"id": "t", "at": LL["taiwan"], "label": "Taiwan", "color": "accent3", "time": C("only to Taiwan")},
             {"id": "p", "at": LL["manila"], "label": "Philippines", "color": "accent3", "time": C("Philippines")}],
    "routes": [{"from": LL["losangeles"], "to": LL["taiwan"], "at": C("Google and Meta"), "dur": 1.4, "color": "border", "lift": 0.16},
               {"from": LL["losangeles"], "to": LL["hongkong"], "at": C("review recommended"), "dur": 1.4, "blocked": True, "lift": 0.18},
               {"from": LL["losangeles"], "to": LL["taiwan"], "at": C("only to Taiwan"), "dur": 1.4, "color": "accent3", "tokenShape": "packet", "lift": 0.16},
               {"from": LL["losangeles"], "to": LL["manila"], "at": C("Philippines"), "dur": 1.4, "color": "accent3", "tokenShape": "packet", "lift": 0.12}],
    "caption": "Route schematic (Natural Earth basemap)"},
    sources=["reuters_smw6", "natural_earth"], assets=GEO, sfx=[{"kind": "hit", "cue": "review recommended", "gain": 0.3}])
# ---- PRESENTER D: two networks (stylised map)
add("p37_split", "m5_draw", "engine_draw", {
    "title": "One seabed, two networks", "board": BOARD, "draw_start": C("On one side"), "speed": 1300,
    "enter": {"from": 2200, "to": 1600, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 560 420 Q 640 360 740 400 Q 800 470 760 560 Q 680 620 600 560 Q 540 500 560 420 Z", "color": "border", "width": 4, "kind": "map", "start": C("Let me draw what"), "label": lbl("AMERICAS", 650, 650, 22, "muted")},
        {"d": "M 900 380 Q 980 330 1060 380 Q 1080 470 1020 520 Q 940 540 900 470 Z", "color": "border", "width": 4, "kind": "map", "start": C("Let me draw what", 0.4), "label": lbl("EUROPE", 980, 570, 22, "muted")},
        {"d": "M 1180 380 Q 1300 330 1400 400 Q 1420 520 1330 580 Q 1220 590 1180 500 Z", "color": "border", "width": 4, "kind": "map", "start": C("Let me draw what", 0.8), "label": lbl("ASIA", 1300, 630, 22, "muted")},
        {"d": "M 760 470 Q 830 430 900 440 M 1060 430 Q 1120 420 1180 440 M 740 420 Q 960 250 1200 400", "color": "accent2", "width": 6, "flow": 260, "start": C("On one side"), "label": lbl("US · JAPANESE · EUROPEAN BUILDERS", 980, 290, 26, "accent2")},
        {"d": "M 1330 580 Q 1200 760 960 800 M 1330 580 Q 1420 760 1600 820", "color": "risk", "width": 6, "flow": 260, "start": C("On the other"), "label": lbl("CHINESE BUILDERS", 1280, 880, 26, "risk")},
        {"d": rect(580, 820, 260, 90), "color": "accent", "width": 5, "start": C("Each country"), "label": lbl("COUNTRY", 710, 877, 26, "accent")},
        {"d": arrow((850, 865), (1000, 805), -0.05), "color": "accent", "width": 4, "start": C("who may land"), "label": lbl("WHO MAY LAND HERE?", 710, 960, 24, "accent")},
        {"d": "M 1100 300 L 1100 980", "color": "ink", "width": 3, "dash": "10 12", "start": C("splitting"), "label": lbl("SPLIT", 1100, 1010, 26, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("On the other", 0.5), "dur": 1.2, "target": [1300, 760]}, {"kind": "explain", "at": C("splitting", 0.3), "dur": 2.4}],
    "scale": 0.86, "floor": 1040}, sources=["reuters_smw6"])
kinetic("s38_count", "m5_count", [
    ("Active and planned cables", 44, "TeleGeography", None, True),
    ("{{cable_count.display}}", 130, "active and planned", "accent2", False),
    ("Who builds it · who pays · where it lands", 40, "Every new", None, True)], chapter="The stakes",
    sfx=[{"kind": "hit", "cue": "where it lands", "gain": 0.35}])

# ====================================================================== PAYOFF
add("s39_payoff", "payoff", "engine_map", {
    "cameras": [{"at": 0, "lon": 140, "lat": 10, "span": 200}, {"at": C("built by a few"), "lon": 60, "lat": 20, "span": 280, "dur": 3.0},
                {"at": C("Every time"), "lon": 20, "lat": 20, "span": 330, "dur": 3.0}],
    "drift": {"lon": 0.25, "zoom": 0.004}, "tilt": [[0, 16], [30, 4]],
    "routes": web_routes(C("It is glass"), 0.3),
    "caption": "Schematic links, not actual cable routes"},
    sources=["itu_2025", "natural_earth"], assets=GEO)
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

exec(open(Path(__file__).with_name('gen_cables_cartoons.py')).read())
OUT.write_text("# GENERATED by tools/gen_cables_storyboard.py; edit the generator, not this file.\n"
               "# Episode 09 storyboard on the animation engine with the game HUD. The channel intro is inserted automatically after the hook.\n"
               + yaml.safe_dump({"scenes": scenes}, sort_keys=False, allow_unicode=True, width=200))
print(f"{len(scenes)} scenes -> {OUT}")
