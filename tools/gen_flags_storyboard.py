"""Generates projects/why-ships-fly-foreign-flags/deliverables/documentary/storyboard.yaml (Episode 11).

Cartoon-first, built with tools/cartoon_kit.py: ships carry text pennants (country names as labels, never real
flag designs) that can switch mid-scene, and crews that turn sad when abandoned. Five parts, internal only.
Run: python tools/gen_flags_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-ships-fly-foreign-flags/deliverables/documentary/storyboard.yaml"
LL = {"athens": [23.7, 37.98], "shanghai": [121.47, 31.23], "tokyo": [139.7, 35.7], "monrovia": [-10.8, 6.3],
      "panama": [-79.5, 8.98], "majuro": [171.38, 7.09], "virginia": [-77.45, 38.95], "suez": [32.55, 29.97]}
FLAGS3 = ["LIBERIA", "PANAMA", "MARSHALL IS."]

# ====================================================================== HOOK
cart("s01_ships", "h_question", {
    "worldW": 3600, "coasts": {"port": True, "left": True, "leftLabel": "YOUR CITY"},
    "cam": [{"at": 0, "x": 2400, "y": 420, "zoom": 1.0}, {"at": C("registered"), "x": 1500, "y": 400, "zoom": 0.85, "dur": 3.0},
            {"at": C("choice of flag"), "x": 1200, "y": 360, "zoom": 1.1, "dur": 2.4}],
    "drift": 0,
    "actors": [ship(x=[[0, 3000], [20, 1500]], flag="LIBERIA", flip=True, crew=3), ship(x=[[0, 2200], [20, 900]], flag="PANAMA", flip=True, scale=0.8),
               ship(x=[[0, 3500], [20, 2300]], flag="MARSHALL IS.", flip=True, scale=0.9)],
    "callouts": [co("your phone · your clothes · your coffee", 960, 960, C("your phone"), "white", screen=True, size=36),
                 co("Registered… where?", 1500, 180, C("registered"), "gold", size=44, until=C("choice of flag", -0.4)),
                 co("Rules · taxes · crew", 1200, 180, C("choice of flag"), "risk", size=40)]},
    sfx=[{"kind": "hit", "cue": "registered", "gain": 0.3}])
add("s02_share", "h_stakes", "engine_chart", {"chart": "donut", "cx": 960, "cy": 600, "r": 250, "thick": 90, "start": C("just three flags"),
    "data": [{"label": "Liberia · Panama · Marshall Islands", "value": 45.1, "display": "45.1%"}, {"label": "every other flag", "value": 54.9, "display": "54.9%"}],
    "center": "{{top3.display}}", "centerSub": "of world shipping capacity (1 Jan 2025)",
    "title": "Three flags", "subtitle": "biggest owners: Greece · China · Japan (UNCTAD)"},
    sources=["unctad_2025"])

# ====================================================================== PART 1: whose ship is it
card("s03_c1", "m1_card", "Whose Ship Is It?", "One ship, many countries")
cart("s04_q1", "m1_question", {
    "worldW": 2400, "cam": [{"at": 0, "x": 1200, "y": 400, "zoom": 1.3}], "drift": 0,
    "actors": [ship(x=[[0, 900], [12, 1500]], flag="?", crew=4)],
    "callouts": [co("Whose ship is it?", 1200, 160, C("Whose ship"), "gold", size=48), co("Stranger than you think", 1200, 260, C("stranger"), "white")]})
# ---- PRESENTER A: the flag is a passport
add("p05_flag", "m1_flag", "engine_draw", {
    "title": "A flag is a ship's passport", "board": BOARD, "draw_start": C("Every ship"), "speed": 1300,
    "enter": {"from": -260, "to": 430, "at": C("Every ship", -0.6), "dur": 1.3},
    "strokes": [
        {"d": "M 600 560 L 1000 560 L 950 640 L 640 640 Z", "color": "accent2", "width": 6, "start": C("Every ship"), "kind": "box", "label": lbl("SHIP", 800, 610, 30, "accent2")},
        {"d": rect(700, 380, 160, 120), "color": "accent", "width": 5, "start": C("flag state"), "label": lbl("FLAG", 780, 450, 30, "accent")},
        {"d": arrow((1010, 520), (1240, 380), -0.1), "color": "ink", "width": 4, "start": C("decides")},
        {"d": rect(1250, 330, 420, 90), "color": "accent3", "width": 5, "start": C("safety rules"), "label": lbl("SAFETY RULES", 1460, 388, 30, "accent3")},
        {"d": arrow((1010, 590), (1240, 520)), "color": "ink", "width": 4, "start": C("labor rules", -0.3)},
        {"d": rect(1250, 470, 420, 90), "color": "accent3", "width": 5, "start": C("labor rules"), "label": lbl("LABOR RULES", 1460, 528, 30, "accent3")},
        {"d": arrow((1010, 640), (1240, 660), 0.1), "color": "ink", "width": 4, "start": C("and taxes", -0.3)},
        {"d": rect(1250, 610, 420, 90), "color": "accent", "width": 5, "start": C("and taxes"), "label": lbl("TAXES", 1460, 668, 30, "accent")},
        {"d": dot(800, 760), "color": "ink", "width": 1, "start": C("passport"), "label": lbl("= THE SHIP'S PASSPORT", 800, 760, 34, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("passport", 0.2), "dur": 1.4, "target": [800, 610]}, {"kind": "smile", "at": C("passport", 1.6), "dur": 1.5}],
    "scale": 0.86, "floor": 1040})
cart("s06_evergiven", "m1_evergiven", {
    "worldW": 1920, "coasts": {"port": True, "left": True, "right": True, "leftLabel": "EGYPT", "rightLabel": "EGYPT"}, "sea": 420,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 0.9}, {"at": C("One ship"), "x": 960, "y": 380, "zoom": 1.1, "dur": 2.0}], "drift": 0,
    "shake": [{"at": C("stuck in the Suez"), "dur": 1.0, "amp": 10}],
    "actors": [ship(x=960, flag="PANAMA", name="EVER GIVEN", crew=5)],
    "callouts": [co("Owner: Japan", 520, 150, C("Japanese company"), "white"), co("Operator: Taiwan", 960, 110, C("Taiwanese"), "white"),
                 co("Flag: Panama", 1400, 150, C("flagged in"), "gold"), co("Stuck in: Egypt", 960, 960, C("stuck in Egypt"), "risk", screen=True),
                 co("One ship, four countries", 960, 230, C("One ship"), "green", size=44, screen=True)]},
    sources=["ap_evergiven"])
add("s07_map", "m1_owners", "engine_map", {
    "title": "Who owns the ships · whose flags they fly", "subtitle": "Greece owns {{owners.display}} of capacity · Asian owners {{regs_2026.asia_display}} · European {{regs_2026.europe_display}}",
    "cameras": [{"at": 0, "lon": 60, "lat": 30, "span": 200}, {"at": C("look at the flags"), "lon": 20, "lat": 15, "span": 330, "dur": 3.0}],
    "drift": {"lon": 0.2, "zoom": 0.003}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "GRC", "color": "accent2", "at": C("Greek owners")}, {"iso": "CHN", "color": "accent2", "at": C("Asian companies")}, {"iso": "JPN", "color": "accent2", "at": C("Asian companies", 0.3)},
                   {"iso": "LBR", "color": "accent", "at": C("look at the flags")}, {"iso": "PAN", "color": "accent", "at": C("look at the flags", 0.3)}, {"iso": "MHL", "color": "accent", "at": C("look at the flags", 0.6)}],
    "hubs": [{"id": "g", "at": LL["athens"], "label": "Greece", "sub": "owners", "color": "accent2", "time": C("Greek owners")},
             {"id": "c", "at": LL["shanghai"], "label": "China", "sub": "owners", "color": "accent2", "time": C("Asian companies")},
             {"id": "j", "at": LL["tokyo"], "label": "Japan", "sub": "owners", "color": "accent2", "time": C("Asian companies", 0.3)},
             {"id": "l", "at": LL["monrovia"], "label": "Liberia", "sub": "flag", "color": "accent", "time": C("look at the flags")},
             {"id": "p", "at": LL["panama"], "label": "Panama", "sub": "flag", "color": "accent", "time": C("look at the flags", 0.3), "anchor": "end"},
             {"id": "m", "at": LL["majuro"], "label": "Marshall Islands", "sub": "flag", "color": "accent", "time": C("look at the flags", 0.6)}],
    "routes": [{"from": LL["athens"], "to": LL["monrovia"], "at": C("small countries"), "dur": 1.2, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["shanghai"], "to": LL["majuro"], "at": C("small countries", 0.4), "dur": 1.2, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["tokyo"], "to": LL["panama"], "at": C("small countries", 0.8), "dur": 1.6, "color": "accent", "tokenShape": "box", "lift": 0.15}],
    "caption": "Real locations (Natural Earth) · arrows are schematic"},
    sources=["unctad_2025", "unctadstat_2026", "natural_earth"], assets=GEO)
kinetic("s08_t1", "m1_transition", [("How did a few small countries", 54, "So how", None, True), ("end up flying the world's fleet?", 64, "flying the world", "accent", False),
                                    ("It started with a drink", 44, "with a drink", "accent2", True)])

# ====================================================================== PART 2: how it started
card("s09_c2", "m2_card", "How It Started", "A drink, a war and an office in Virginia")
cart("s10_q2", "m2_question", {
    "worldW": 2400, "cam": [{"at": 0, "x": 1200, "y": 400, "zoom": 1.1}], "drift": 20,
    "actors": [ship(x=[[0, 700], [10, 1300]], flag=[[0, "HOME"], [{"cue": "borrowing"}, "???"]], crew=3)],
    "callouts": [co("Borrow a flag?", 1200, 170, C("borrowing"), "gold", size=48)]})
cart("s11_prohibition", "m2_prohibition", {
    "worldW": 2600, "coasts": {"port": True, "left": True, "leftLabel": "UNITED STATES"},
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 1.0}, {"at": C("open registry"), "x": 1500, "y": 400, "zoom": 0.95, "dur": 2.4}], "drift": 0,
    "actors": [ship(x=[[0, 700], [20, 1900]], flag=[[0, "UNITED STATES"], [{"cue": "registered their ships"}, "PANAMA"]], crew=6, name="PASSENGER SHIP")],
    "callouts": [co("1920s: alcohol banned in the U.S.", 960, 150, C("alcohol was banned"), "risk", screen=True, size=40),
                 co("Drinks on board!", 1300, 260, C("serve drinks"), "gold"),
                 co("Panama: the first open registry", 960, 960, C("first open registry"), "green", screen=True, sub="any owner, any country (Windward)")]},
    sources=["windward_foc"])
add("s12_liberia", "m2_liberia", "engine_map", {
    "title": "From Panama to Liberia", "subtitle": "a new registry opened with Liberia's government in 1948",
    "cameras": [{"at": 0, "lon": -70, "lat": 15, "span": 100}, {"at": C("government of Liberia"), "lon": -40, "lat": 20, "span": 120, "dur": 2.6}],
    "drift": {"lon": 0.1, "zoom": 0.004}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "PAN", "color": "risk", "at": C("private payments")}, {"iso": "LBR", "color": "accent", "at": C("government of Liberia")}],
    "hubs": [{"id": "p", "at": LL["panama"], "label": "Panama", "sub": "private payments demanded (Carlisle)", "color": "risk", "time": C("Panama's officials"), "anchor": "end"},
             {"id": "l", "at": LL["monrovia"], "label": "Liberia", "sub": "{{liberia_1948.display}} · Edward Stettinius", "color": "accent", "time": C("government of Liberia")},
             {"id": "v", "at": LL["virginia"], "label": "Virginia, U.S.", "sub": "where the registry is run today", "color": "accent2", "time": C("Virginia")}],
    "routes": [{"from": LL["panama"], "to": LL["monrovia"], "at": C("an alternative"), "dur": 1.6, "color": "accent", "tokenShape": "box", "lift": 0.2},
               {"from": LL["virginia"], "to": LL["monrovia"], "at": C("Virginia", 0.4), "dur": 1.4, "color": "accent2", "tokenShape": "packet", "lift": 0.18}],
    "caption": "Real locations (Natural Earth) · arrows are schematic"},
    sources=["carlisle_1980", "windward_foc", "natural_earth"], assets=GEO)
kinetic("s13_term", "m2_term", [("1950s: a new name", 44, "nineteen fifties", "muted", True), ("“Flag of convenience”", 88, "calling it", "accent", False),
                                ("chosen not for where the ship comes from, but for what it saves", 36, "not for where", None, True)])
# ---- PRESENTER B: how an open registry works
add("p14_registry", "m2_draw", "engine_draw", {
    "title": "How an open registry works", "board": BOARD, "draw_start": C("A ship owner"), "speed": 1400,
    "enter": {"from": 2200, "to": 1620, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 330, 300, 110), "color": "accent2", "width": 5, "start": C("A ship owner"), "label": lbl("SHIP OWNER", 670, 395, 30, "accent2")},
        {"d": dot(670, 470), "color": "muted", "width": 1, "start": C("Athens"), "label": lbl("Athens · Shanghai · Tokyo", 670, 470, 22, "muted")},
        {"d": arrow((830, 385), (960, 385)), "color": "ink", "width": 4, "start": C("picks a flag")},
        {"d": rect(970, 300, 300, 200), "color": "accent", "width": 5, "start": C("from a menu"), "label": lbl("FLAG MENU", 1120, 340, 26, "accent")},
        {"d": dot(1120, 400), "color": "ink", "width": 1, "start": C("from a menu", 0.3), "label": lbl("LIBERIA  ·  PANAMA", 1120, 400, 22, "ink")},
        {"d": dot(1120, 440), "color": "ink", "width": 1, "start": C("from a menu", 0.6), "label": lbl("MARSHALL IS.  ·  …", 1120, 440, 22, "ink")},
        {"d": arrow((1120, 510), (1120, 600)), "color": "ink", "width": 4, "start": C("The registry")},
        {"d": rect(930, 610, 380, 120), "color": "accent3", "width": 5, "start": C("private company"), "label": lbl("REGISTRY COMPANY", 1120, 678, 28, "accent3")},
        {"d": arrow((920, 690), (760, 820), 0.06), "color": "accent", "width": 5, "start": C("sends part")},
        {"d": rect(470, 820, 360, 110), "color": "accent", "width": 5, "start": C("to the government"), "label": lbl("FLAG GOVERNMENT", 650, 885, 28, "accent")},
        {"d": dot(1120, 800), "color": "risk", "width": 1, "start": C("never has to visit"), "label": lbl("the ship never visits", 1120, 800, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("never has to visit", 0.4), "dur": 1.4, "target": [1120, 790]}],
    "scale": 0.86, "floor": 1040}, sources=["windward_foc", "allafrica_2026"])
kinetic("s15_t2", "m2_transition", [("A flag you choose like a product", 58, "A flag you can choose", None, True), ("Why a faraway flag?", 80, "faraway flag", "accent", False)])

# ====================================================================== PART 3: why owners do it
card("s16_c3", "m3_card", "Why Owners Do It", "Lighter rules, lower costs")
cart("s17_q3", "m3_question", {
    "worldW": 2600, "coasts": {"port": True, "left": True, "leftLabel": "OWNER"},
    "cam": [{"at": 0, "x": 1200, "y": 400, "zoom": 0.9}], "drift": 0,
    "actors": [office(160, "SHIP OWNER", "blue"), island(x=2000, text="FLAG STATE"), ship(x=[[0, 700], [12, 1300]], flag="FLAG STATE", crew=3),
               coins(200, 120, [2000, 260], C("in return"), rate=2)],
    "callouts": [co("What does the owner gain?", 1100, 160, C("actually gain"), "gold", size=42), co("…and the small country?", 1100, 260, C("in return"), "white")]})
cart("s18_reasons", "m3_reasons", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.0}], "drift": 0,
    "actors": [ship(x=[[0, 900], [24, 1700]], flag=[[0, "HOME"], [{"cue": "flag of convenience"}, "LIBERIA"]], crew=4)],
    "callouts": [co("Fewer rules", 500, 160, C("stricter rules"), "green"), co("Lower costs", 500, 260, C("operating costs"), "green"),
                 co("Lower taxes", 2100, 160, C("high taxes"), "green"), co("Weaker crew protection", 2100, 260, C("worst cases"), "risk"),
                 co("Panama: register online, hire low-cost crews", 960, 960, C("Panama, for example"), "white", screen=True, sub="Windward")]},
    sources=["windward_foc"])
add("s19_scale", "m3_scale", "compare", {"chapter": "Why owners do it", "title": "The Liberian flag, 2026", "sides": [
    {"kicker": "Fleet size", "value": "{{liberia_2026.display}}", "label": "first registry ever to pass it", "cue": "first registry"},
    {"kicker": "Ships", "value": "{{liberia_2026.ships_display}}", "label": "flying the flag (IHS)", "cue": "flying its flag"},
    {"kicker": "World capacity", "value": "{{top3.liberia_display}}", "label": "Liberia alone (UNCTAD, 2025)", "cue": "Liberia alone"},
    {"kicker": "Container ships", "value": "{{liberia_new.container_display}}", "label": "the registry's own figure", "cue": "container ships"}]},
    sources=["fpa_2026", "unctad_2025", "liscr_2026"])
cart("s20_money", "m3_money", {
    "worldW": 2600, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.05}], "drift": 0,
    "actors": [island(x=1300, text="LIBERIA"), coins(2500, -80, [1300, 260], C("Registration fees"), rate=3),
               ship(x=[[0, 2300], [20, 1900]], flag="LIBERIA", flip=True, scale=1.3)],
    "callouts": [co("fees · tonnage taxes · inspections", 960, 150, C("Registration fees"), "white", screen=True),
                 co("{{liberia_rev.display}} a year", 700, 250, C("maritime revenue"), "gold", size=48, sub="researcher's estimate, 2026 (AllAfrica)"),
                 co("A tiny slice of world shipping", 960, 960, C("tiny slice"), "risk", screen=True)]},
    sources=["allafrica_2026"])
kinetic("s21_t3", "m3_transition", [("Cheaper · simpler · lighter rules", 52, "Cheaper", None, True), ("Who is responsible at sea?", 74, "who is responsible", "risk", False)])

# ====================================================================== PART 4: the dark side
card("s22_c4", "m4_card", "The Dark Side", "Abandoned crews and false flags")
cart("s23_q4", "m4_question", {
    "worldW": 2400, "night": True, "cam": [{"at": 0, "x": 1200, "y": 420, "zoom": 1.3}], "drift": 0,
    "actors": [ship(x=1200, flag="???", flagColor="grey", crew=5, sadAt=C("disappears"), anchorAt=0.3)],
    "callouts": [co("The owner disappears…", 1200, 180, C("disappears"), "risk", size=44)]})
add("s24_abandon", "m4_abandon", "engine_chart", {"chart": "bar", "box": {"x": 460, "y": 330, "w": 1000, "h": 500}, "start": C("up from"), "stagger": 1.6,
    "title": "Seafarers abandoned by ship owners", "note": "ITF report to the IMO (via gCaptain)",
    "data": [{"label": "2023", "value": 1676, "display": "{{abandon.prev_display}}"}, {"label": "2024", "value": 3133, "display": "{{abandon.display}}"}],
    "highlight": 1, "highlightAt": C("Left on board"), "color": "accent2", "highlightColor": "risk"},
    sources=["itf_2024"])
cart("s25_ships", "m4_ships", {
    "worldW": 2400, "coasts": {"port": True, "right": True, "rightLabel": "FOREIGN PORT"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.1}], "drift": 0,
    "actors": [ship(x=1500, flag="FLAG ?", flagColor="grey", crew=5, sadAt=0.0, anchorAt=0.0), ship(x=800, flag="FLAG ?", flagColor="grey", crew=3, sadAt=0.0, anchorAt=0.5, scale=0.7)],
    "callouts": [co("{{abandon.ships_display}} ships abandoned in 2024", 960, 150, C("In total"), "risk", screen=True, size=44),
                 co("more than twice 2023", 960, 250, C("twice as many"), "white", screen=True),
                 co("Waiting…", 1500, 330, C("waiting"), "white")]},
    sources=["itf_2024"])
add("s26_foc", "m4_foc", "engine_chart", {"chart": "donut", "cx": 960, "cy": 600, "r": 250, "thick": 90, "start": C("abandoned ships were"),
    "data": [{"label": "flag of convenience", "value": 81, "display": "81%"}, {"label": "other flags", "value": 19, "display": "19%"}],
    "center": "{{abandon.foc_display}}", "centerSub": "of abandoned ships, 2024",
    "title": "Abandoned ships and their flags", "subtitle": "most abandonments: Panama (43) · ITF"},
    sources=["itf_2024"])
# ---- PRESENTER C: five countries, no one responsible
add("p27_five", "m4_draw", "engine_draw", {
    "title": "Five countries, no one responsible", "board": BOARD, "draw_start": C("The owner lives"), "speed": 1500,
    "enter": {"from": -260, "to": 420, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 1000 600 L 1300 600 L 1260 660 L 1040 660 Z", "color": "accent2", "width": 6, "kind": "box", "start": C("The owner lives", -0.5), "label": lbl("SHIP", 1150, 640, 26, "accent2")},
        {"d": rect(560, 300, 260, 90), "color": "ink", "width": 4, "start": C("The owner lives"), "label": lbl("1 · OWNER", 690, 357, 26)},
        {"d": rect(1480, 300, 280, 90), "color": "ink", "width": 4, "start": C("legally owns"), "label": lbl("2 · COMPANY", 1620, 357, 26)},
        {"d": rect(1480, 760, 280, 90), "color": "accent", "width": 4, "start": C("The flag"), "label": lbl("3 · FLAG", 1620, 817, 26, "accent")},
        {"d": rect(1010, 800, 280, 90), "color": "ink", "width": 4, "start": C("The crew"), "label": lbl("4 · CREW", 1150, 857, 26)},
        {"d": rect(560, 760, 260, 90), "color": "risk", "width": 4, "start": C("stuck in the port"), "label": lbl("5 · PORT", 690, 817, 26, "risk")},
        {"d": arrow((820, 390), (1010, 590), 0.05), "color": "muted", "width": 3, "start": C("stuck in the port", 0.6)},
        {"d": arrow((1480, 390), (1300, 590), -0.05), "color": "muted", "width": 3, "start": C("stuck in the port", 0.8)},
        {"d": dot(1150, 470), "color": "risk", "width": 1, "start": C("not my problem"), "label": lbl("“NOT MY PROBLEM”", 1150, 470, 40, "risk")},
    ],
    "actions": [{"kind": "explain", "at": C("The crew", 0.3), "dur": 2.0}, {"kind": "react", "at": C("not my problem", 0.3)}],
    "scale": 0.86, "floor": 1040})
cart("s28_false", "m4_falseflags", {
    "worldW": 2600, "night": True, "cam": [{"at": 0, "x": 1300, "y": 420, "zoom": 1.05}], "drift": 0,
    "actors": [ship(x=[[0, 2200], [22, 900]], flip=True, crew=0, flagColor="risk", name="TANKER",
                    flag=[[0, "FLAG A"], [{"cue": "not real"}, "FAKE"], [{"cue": "counted"}, "???"], [{"cue": "first nine months"}, "FAKE"], [{"cue": "dodge sanctions"}, "???"]])],
    "callouts": [co("Flags that aren't real", 1300, 160, C("not real"), "risk", size=44),
                 co("{{falseflags.display}} Russian vessels", 960, 960, C("counted"), "gold", screen=True, size=44, sub="false flags, Jan–Sep 2025 (CREA)"),
                 co("…to dodge oil sanctions", 960, 1040, C("dodge sanctions"), "white", screen=True)]},
    sources=["crea_2025"])
kinetic("s29_t4", "m4_transition", [("So why doesn't the world", 56, "So why", None, True), ("simply ban it?", 88, "ban it", "accent", False)])

# ====================================================================== PART 5: why it survives
card("s30_c5", "m5_card", "Why It Survives", "Everyone gains something")
cart("s31_q5", "m5_question", {
    "worldW": 3000, "cam": [{"at": 0, "x": 1500, "y": 400, "zoom": 0.8}], "drift": 30,
    "actors": [ship(x=[[0, 400 + i * 700], [16, 1100 + i * 700]], flag=FLAGS3[i % 3], scale=0.7 + 0.1 * (i % 2)) for i in range(4)],
    "callouts": [co("…and they keep growing", 1500, 160, C("keep growing"), "gold", size=44)]})
# ---- PRESENTER D: who gains
add("p32_gains", "m5_everyone", "engine_draw", {
    "title": "Who gains?", "board": BOARD, "draw_start": C("Owners save"), "speed": 1400,
    "enter": {"from": 2200, "to": 1640, "at": C("Because almost", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 560 900 L 1420 900", "color": "border", "width": 4, "start": C("Owners save", -0.4)},
        {"d": "M 620 900 L 620 520 L 800 520 L 800 900", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.35, "kind": "bar", "start": C("Owners save"), "label": lbl("OWNERS SAVE", 710, 495, 26, "accent2")},
        {"d": "M 900 900 L 900 700 L 1080 700 L 1080 900", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("earn fees"), "label": lbl("FLAGS EARN FEES", 990, 675, 26, "accent")},
        {"d": "M 1180 900 L 1180 600 L 1360 600 L 1360 900", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("stays cheap"), "label": lbl("CHEAP SHIPPING", 1270, 575, 26, "accent3")},
        {"d": dot(990, 950), "color": "muted", "width": 1, "start": C("local store"), "label": lbl("schematic, not to scale", 990, 950, 22, "muted")},
        {"d": dot(990, 360), "color": "ink", "width": 1, "start": C("cargo capacity"), "label": lbl("world fleet: {{regs_2026.display}}", 990, 360, 34, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("stays cheap", 0.6), "dur": 1.3, "target": [1270, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["unctadstat_2026"])
add("s33_quality", "m5_quality", "compare", {"chapter": "Why it survives", "title": "Safe choice, or not?", "sides": [
    {"kicker": "New ships choosing Liberia", "value": "{{liberia_new.display}}", "label": "the registry's own figure", "cue": "newly built"},
    {"kicker": "Most abandonments, 2024", "value": "Panama · 43", "label": "then Palau 37 · Tanzania 30 · Comoros 29 (ITF)", "cue": "Panama tops"}]},
    sources=["liscr_2026", "itf_2024"])
kinetic("s34_lesson", "m5_lesson", [("Not where a ship is registered", 54, "The real question", None, True), ("but whether anyone is truly responsible", 60, "truly responsible", "accent", False)])

# ====================================================================== PAYOFF
cart("s35_payoff", "payoff", {
    "worldW": 4200, "coasts": {"port": True, "left": True, "leftLabel": "YOUR CITY"},
    "cam": [{"at": 0, "x": 600, "y": 380, "zoom": 1.1}, {"at": C("look at the back"), "x": 1700, "y": 400, "zoom": 1.15, "dur": 2.6},
            {"at": C("Monrovia"), "x": 2600, "y": 400, "zoom": 0.85, "dur": 3.0}, {"at": C("chosen like a product"), "x": 3200, "y": 380, "zoom": 0.95, "dur": 3.0}],
    "drift": 0,
    "actors": [ship(x=[[0, 2000], [40, 1300]], flag="LIBERIA", name="MONROVIA", flip=True, crew=3),
               ship(x=[[0, 2900], [40, 2300]], flag="PANAMA", name="PANAMA", flip=True, scale=0.9, crew=2),
               ship(x=[[0, 3700], [40, 3100]], flag="MARSHALL IS.", name="MAJURO", flip=True, scale=0.9, crew=2),
               {"kind": "whale", "x": [[0, 3400], [40, 2600]], "y": 720, "flip": True}],
    "callouts": [co("Look at the stern", 1700, 160, C("look at the back"), "gold", size=44, until=C("Monrovia")),
                 co("Monrovia · Panama · Majuro", 2600, 160, C("Monrovia"), "white", size=44),
                 co("A flag chosen like a product", 3200, 270, C("chosen like a product"), "green", size=44)]},
    sources=["unctad_2025"])
add("s36_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

write(OUT, "# GENERATED by tools/gen_flags_storyboard.py; edit the generator, not this file.\n"
           "# Episode 11 storyboard: cartoon-first. The channel intro is inserted automatically after the hook.\n")
