"""Generates projects/why-taiwan-matters-cartoon/deliverables/documentary/storyboard.yaml (Episode 07 v2).

Cartoon remake of Episode 07 with tools/cartoon_kit.py: an island with a chip fab, chips flying across the ocean
(coin streams with shape "chip"), ships and planes, a hypothetical disruption labelled as such. No mission talk.
Run: python tools/gen_taiwan_cartoon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-taiwan-matters-cartoon/deliverables/documentary/storyboard.yaml"
TW = [121.0, 23.7]
LL = {"taipei": [121.5, 25.05], "hsinchu": [120.97, 24.8], "sf": [-122.0, 37.4], "veldhoven": [5.43, 51.42], "tokyo": [139.7, 35.7],
      "seoul": [127.0, 37.5], "arizona": [-112.07, 33.45], "kumamoto": [130.7, 32.8], "dresden": [13.74, 51.05], "berlin": [13.4, 52.5]}


def fab(x, text="FAB", y=None, **kw):
    o = office(x, text, "gold", **kw)
    if y is not None:
        o["y"] = y
    return o


def chips(x, y, to, at, rate=5, until=None):
    return coins(x, y, to, at, rate=rate, until=until, shape="chip")


TAIWAN = lambda x=1500, **kw: island(x=x, text="TAIWAN", **kw)
HYPO = {"text": "Hypothetical scenario", "sub": "not a prediction"}

# ====================================================================== HOOK
cart("s01_island", "h_question", {
    "worldW": 3000, "coasts": {"plain": True, "left": True, "leftLabel": "THE WORLD"},
    "cam": [{"at": 0, "x": 1500, "y": 380, "zoom": 1.3}, {"at": C("depended on"), "x": 1100, "y": 400, "zoom": 0.85, "dur": 3.0}], "drift": 0,
    "actors": [TAIWAN(), fab(1480, y=314, scale=0.8), office(140, "PHONES", "blue"), office(300, "AI SERVERS", "purple", scale=0.85),
               chips(1500, 200, [250, 160], C("most important"), rate=6)],
    "callouts": [co("Smaller than Switzerland", 1500, 120, C("smaller than Switzerland"), "gold", size=44)]})
add("s02_map", "h_stakes", "engine_map", {
    "title": "Taiwan", "subtitle": "{{taiwan_area.display}} · Switzerland {{taiwan_area.ch_display}} (CIA World Factbook)",
    "cameras": [{"at": 0, "lon": 140, "lat": 30, "span": 110}, {"at": C("Taiwan covers"), "lon": 121, "lat": 23.7, "span": 16, "dur": 2.6},
                {"at": C("most advanced chips"), "lon": 150, "lat": 30, "span": 150, "dur": 3.0}],
    "drift": {"lon": 0.2, "zoom": 0.008}, "tilt": [[0, 12], [12, 4]],
    "highlights": [{"iso": "TWN", "color": "accent", "at": C("Taiwan covers")}],
    "hubs": [{"id": "t", "at": LL["hsinchu"], "label": "Taiwan", "sub": "most advanced chips", "color": "accent", "time": C("Taiwan covers")}],
    "routes": [{"from": LL["hsinchu"], "to": LL["sf"], "at": C("most advanced chips"), "dur": 1.8, "color": "accent2", "tokenShape": "chip", "tokens": 30, "tokenEvery": 0.4, "lift": 0.2},
               {"from": LL["hsinchu"], "to": LL["tokyo"], "at": C("made right here"), "dur": 1.2, "color": "accent2", "tokenShape": "chip", "tokens": 30, "tokenEvery": 0.4, "lift": 0.2}],
    "caption": "Real locations (Natural Earth) · arrows schematic"},
    sources=["cia_taiwan", "cia_switzerland", "natural_earth"], assets=GEO)

# ====================================================================== PART 1: how Taiwan became essential
card("s03_c1", "m1_card", "How Taiwan Became Essential", "One idea that rewired an industry")
cart("s04_q1", "m1_question", {
    "worldW": 2600, "min_seconds": 9.0, "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.2}], "drift": 0,
    "actors": [TAIWAN(x=1300), fab(1280, y=314, scale=0.8, at=C("center of chipmaking")), chips(2500, -100, [1300, 260], C("runs on chips"), rate=4)],
    "callouts": [co("A small island… the center of chipmaking?", 1300, 140, C("small island"), "gold", size=40),
                 co("Almost everything runs on chips", 960, 960, C("runs on chips"), "white", screen=True)]})
# ---- PRESENTER A: the old rule
add("p05_oldrule", "m1_conflict", "engine_draw", {
    "title": "The old rule of chips", "board": BOARD, "draw_start": C("one rule"), "speed": 1300, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("For a long time", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 300, 110), "color": "accent2", "width": 5, "start": C("designed chips"), "label": lbl("DESIGN", 710, 425, 34, "accent2")},
        {"d": dot(940, 425), "color": "ink", "width": 1, "start": C("you also built"), "label": lbl("+", 940, 438, 60)},
        {"d": rect(1020, 360, 300, 110), "color": "accent", "width": 5, "start": C("the factory"), "label": lbl("FACTORY (FAB)", 1170, 425, 30, "accent")},
        {"d": arrow((1170, 480), (1170, 640)), "color": "ink", "width": 4, "start": C("brutally expensive")},
        {"d": rect(950, 650, 440, 120), "color": "risk", "width": 6, "start": C("only giants"), "label": lbl("ONLY GIANTS CAN PLAY", 1170, 720, 30, "risk")},
        {"d": "M 1460 640 L 1460 420 L 1560 420 L 1560 640", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("brutally expensive", 0.5),
         "label": lbl("$$$", 1510, 400, 40, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("only giants", 0.4), "dur": 1.3, "target": [1170, 710]}, {"kind": "react", "at": C("only giants", 1.8)}],
    "scale": 0.86, "floor": 1040})
add("s06_tsmc", "m1_tsmc", "engine_flow", {
    "title": "The foundry idea", "subtitle": "TSMC, {{tsmc_1987.display}}: design nothing, manufacture for anyone", "cardW": 280, "cardH": 220,
    "stages": [
        {"id": "d", "label": "Designers", "sub": "Nvidia · Apple · AMD", "x": 330, "y": 600, "kind": "design", "color": "accent2", "appear": 0.3, "output": "blueprint"},
        {"id": "f", "label": "TSMC", "sub": "Taiwan · manufactures only", "x": 960, "y": 420, "kind": "fab", "color": "accent", "appear": 0.5, "output": "chip"},
        {"id": "p", "label": "Chips", "sub": "back to the designers", "x": 1590, "y": 600, "kind": "package", "color": "accent3", "appear": 0.7, "output": "chip"},
        {"id": "m", "label": "Devices", "sub": "phones · PCs · AI", "x": 960, "y": 860, "kind": "datacenter", "color": "accent2", "appear": 0.9, "output": "server"}],
    "links": [{"from": "d", "to": "f", "appear": 1.0}, {"from": "f", "to": "p", "appear": 1.1}, {"from": "p", "to": "m", "appear": 1.2}],
    "items": {"starts": [C("for anyone"), C("A small team"), C("send their blueprints")], "route": ["d", "f", "p", "m"], "travel": 0.8, "process": 1.0}},
    sources=["tsmc_about", "tsmc_history", "nvda_10k_fy2026"])
add("s07_share", "m1_discovery", "engine_chart", {"chart": "donut", "cx": 960, "cy": 610, "r": 240, "thick": 90, "start": C("Today TSMC"),
    "data": [{"label": "TSMC", "value": 72.5, "display": "72.5%"}, {"label": "other top-10 foundries", "value": 27.5, "display": "27.5%"}],
    "center": "{{foundry_share.display}}", "centerSub": "of top-10 foundry revenue, {{foundry_share.period_display}}",
    "title": "TSMC's slice", "subtitle": "2025 revenue {{tsmc_revenue_2025.display}} · {{advanced_q4.display}} from 7 nm and below (TrendForce, TSMC)"},
    sources=["trendforce_2q26", "tsmc_4q25", "tsmc_4q25_call"])
kinetic("s08_t1", "m1_transition", [("If the idea was that simple", 56, "But if the idea", None, True), ("why didn't everyone copy it?", 76, "copy it", "accent", False)])

# ====================================================================== PART 2: why chips are so hard to make
card("s09_c2", "m2_card", "Why Chips Are So Hard to Make", "Machines, yield and money")
cart("s10_q2", "m2_question", {
    "worldW": 3000, "min_seconds": 9.0, "coasts": {"plain": True, "left": True, "leftLabel": "OTHER COUNTRIES"},
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 0.85}], "drift": 0,
    "actors": [fab(150, "NEW FAB?", at=C("build its own")), fab(320, "NEW FAB?", at=C("build its own", 0.4), scale=0.8), TAIWAN(x=2100), fab(2080, y=314, scale=0.8)],
    "callouts": [co("Just copy it?", 1100, 160, C("build its own"), "gold", size=48), co("Then Taiwan wouldn't be special", 1100, 270, C("not be special"), "white")]})
# ---- PRESENTER B: the chip process
add("p11_process", "m2_process", "engine_draw", {
    "title": "How a chip is made", "board": BOARD, "draw_start": C("engineers design"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 400, 230, 110), "color": "accent2", "width": 5, "start": C("engineers design"), "label": lbl("1 · DESIGN", 635, 465, 28, "accent2")},
        {"d": arrow((760, 455), (840, 455)), "color": "ink", "width": 4, "start": C("a fab prints")},
        {"d": rect(850, 400, 230, 110), "color": "accent", "width": 5, "start": C("a fab prints", 0.3), "label": lbl("2 · PRINT", 965, 465, 28, "accent")},
        {"d": arrow((1090, 455), (1170, 455)), "color": "ink", "width": 4, "start": C("cut into chips")},
        {"d": rect(1180, 400, 230, 110), "color": "accent3", "width": 5, "start": C("cut into chips", 0.3), "label": lbl("3 · CUT + PACK", 1295, 465, 26, "accent3")},
        {"d": arrow((1295, 520), (1295, 600)), "color": "ink", "width": 4, "start": C("and tested")},
        {"d": rect(1180, 610, 230, 110), "color": "accent3", "width": 5, "start": C("and tested", 0.3), "label": lbl("4 · TEST", 1295, 675, 28, "accent3")},
        {"d": "M 965 820 m -110 0 a 110 110 0 1 0 220 0 a 110 110 0 1 0 -220 0", "color": "accent", "width": 5, "start": C("layer after layer"), "label": lbl("WAFER", 965, 980, 26, "accent")},
        {"d": dot(700, 800), "color": "risk", "width": 1, "start": C("close to perfect"), "label": lbl("every step ≈ perfect", 700, 800, 30, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("close to perfect", 0.3), "dur": 1.3, "target": [965, 820]}],
    "scale": 0.86, "floor": 1040})
cart("s12_euv", "m2_euv", {
    "worldW": 3400, "coasts": {"port": True, "left": True, "leftLabel": "NETHERLANDS"},
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 0.95}, {"at": C("In twenty twenty-five"), "x": 1900, "y": 400, "zoom": 0.9, "dur": 3.0}], "drift": 0,
    "actors": [office(150, "ASML", "blue"), ship(x=[[0, 600], [24, 2300]], flag="EUV MACHINE", name="MACHINE SHIP"), TAIWAN(x=2800), fab(2780, y=314, scale=0.8)],
    "callouts": [co("Only one maker in the world", 900, 160, C("Only one company"), "gold", size=42, sub="ASML, the Netherlands"),
                 co("{{asml_only.display}}", 1900, 170, C("it shipped"), "green", size=44)]},
    sources=["asml_euv", "asml_2025"])
add("s13_yield", "m2_yield", "engine_draw", {
    "title": "Yield: the real secret", "subtitle": "share of chips on a wafer that work (schematic)", "presenter": False, "studio": False, "push": 0.004,
    "draw_start": C("The real secret"), "speed": 1600,
    "strokes": [
        {"d": "M 960 580 m -330 0 a 330 330 0 1 0 660 0 a 330 330 0 1 0 -660 0", "color": "accent", "width": 6, "start": C("The real secret"), "label": lbl("WAFER", 960, 220, 30, "accent")},
        *[{"d": rect(700 + c2 * 90, 360 + r * 90, 70, 70), "color": "risk" if (r * 7 + c2) % 3 == 0 else "accent3", "width": 4,
           "fill": "risk" if (r * 7 + c2) % 3 == 0 else "accent3", "fillOpacity": 0.3, "start": C("actually work", 0.05 * (r * 6 + c2)), "kind": "box"}
          for r in range(5) for c2 in range(6)],
        {"d": dot(960, 1010), "color": "ink", "width": 1, "start": C("years of practice"), "label": lbl("RED = FAILED · GREEN = WORKS", 960, 1010, 28, "ink")},
        {"d": "M 1380 900 Q 1500 700 1700 450", "color": "accent3", "width": 8, "flow": 260, "start": C("endless learning"), "label": lbl("YIELD LEARNING → YEARS", 1560, 420, 26, "accent3")},
    ]})
add("s14_capex", "m2_capex", "compare", {"chapter": "Why chips are so hard to make", "title": "The price of the game", "sides": [
    {"kicker": "TSMC capital spending, 2026 plan", "value": "{{capex_2026.display}}", "label": "January 2026 guidance", "cue": "TSMC planned"},
    {"kicker": "New fabs worldwide, 2024–2032", "value": "{{fab_investment.display}}", "label": "SIA/BCG projection", "cue": "Across the industry"}]},
    sources=["tsmc_4q25_call", "sia_bcg_2024"])
add("s15_capacity", "m2_discovery", "engine_chart", {"chart": "bar", "box": {"x": 360, "y": 340, "w": 1200, "h": 480}, "start": C("most advanced logic"), "stagger": 1.0,
    "title": "Advanced logic capacity (below 10 nm), 2022", "note": "Taiwan holds {{total_capacity.display}} of ALL chip capacity, less than China (SIA/BCG)",
    "valueSuffix": "%", "data": [{"label": "Taiwan", "value": 69}, {"label": "South Korea", "value": 31}, {"label": "United States", "value": 0}],
    "highlight": 0, "highlightAt": C("Taiwan had"), "color": "accent2", "highlightColor": "accent"},
    sources=["sia_bcg_2024"])
add("s16_layers", "m2_layers", "compare", {"chapter": "Why chips are so hard to make", "title": "Chips are not one market", "sides": [
    {"kicker": "Memory (DRAM) capacity", "value": "{{total_capacity.dram_kor_display}}", "label": "South Korea", "cue": "led by South Korea"},
    {"kicker": "Advanced packaging", "value": "Bottleneck", "label": "joining chips and memory", "cue": "Advanced packaging"},
    {"kicker": "Taiwan's edge", "value": "The top", "label": "narrow, but at the very top", "cue": "very top"}]},
    sources=["sia_bcg_2024"])
kinetic("s17_t2", "m2_transition", [("Which raises the next question", 50, "Which raises", None, True), ("Who depends on that top?", 80, "Who depends", "accent", False)])

# ====================================================================== PART 3: who depends on Taiwan
card("s18_c3", "m3_card", "Who Depends on Taiwan", "Everyone depends on someone")
cart("s19_q3", "m3_question", {
    "worldW": 3000, "min_seconds": 9.0, "coasts": {"plain": True, "left": True, "leftLabel": "CUSTOMERS"},
    "cam": [{"at": 0, "x": 1400, "y": 400, "zoom": 0.85}], "drift": 0,
    "actors": [office(140, "CLOUD", "blue"), office(300, "PHONES", "green", scale=0.8), TAIWAN(x=2200), fab(2180, y=314, scale=0.8), chips(2200, 220, [250, 160], 0.4, rate=5)],
    "callouts": [co("Who depends on Taiwan?", 1300, 160, C("Who actually"), "gold", size=46), co("Power + risk", 1300, 270, C("economic power"), "risk")]})
# ---- PRESENTER C: the Pacific map
add("p20_map", "m3_map", "engine_draw", {
    "title": "California designs, Taiwan makes", "board": BOARD, "draw_start": C("Here is Taiwan"), "speed": 1300, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 1500 520 Q 1530 460 1560 520 Q 1580 600 1540 660 Q 1500 620 1500 520 Z", "color": "accent", "width": 5, "kind": "map", "fill": "accent", "fillOpacity": 0.3,
         "start": C("Here is Taiwan"), "label": lbl("TAIWAN", 1530, 720, 28, "accent")},
        {"d": "M 600 380 Q 640 500 620 640 Q 680 700 720 640 Q 740 500 700 380 Z", "color": "accent2", "width": 5, "kind": "map", "fill": "accent2", "fillOpacity": 0.3,
         "start": C("across the Pacific"), "label": lbl("CALIFORNIA", 660, 360, 28, "accent2")},
        {"d": dot(660, 760), "color": "ink", "width": 1, "start": C("Nvidia, Apple"), "label": lbl("Nvidia · Apple · AMD", 660, 760, 24, "ink")},
        {"d": arrow((740, 480), (1480, 500), -0.12), "color": "accent2", "width": 5, "start": C("TSMC does"), "label": lbl("DESIGNS →", 1100, 380, 26, "accent2")},
        {"d": arrow((1480, 600), (740, 600), -0.12), "color": "accent", "width": 5, "flow": 220, "start": C("back again"), "label": lbl("← FINISHED CHIPS", 1100, 760, 26, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("back again", 0.6), "dur": 1.3, "target": [1100, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["nvda_10k_fy2026", "apple_arizona"])
add("s21_customers", "m3_customers", "engine_chart", {"chart": "donut", "cx": 960, "cy": 610, "r": 240, "thick": 90, "start": C("largest customer alone"),
    "data": [{"label": "largest customer", "value": 19, "display": "19%"}, {"label": "second", "value": 17, "display": "17%"}, {"label": "all others", "value": 64, "display": "64%"}],
    "center": "36%", "centerSub": "of TSMC revenue from two customers (2025)",
    "title": "TSMC's biggest customers", "subtitle": "dependence runs both ways (TSMC annual report)"},
    sources=["tsmc_customers_2025"])
cart("s22_network", "m3_network", {
    "worldW": 3600, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "UNITED STATES", "rightLabel": "EUROPE · ASIA"},
    "cam": [{"at": 0, "x": 1800, "y": 400, "zoom": 1.0}, {"at": C("Phone makers"), "x": 1800, "y": 400, "zoom": 0.6, "dur": 3.0}], "drift": 0,
    "actors": [TAIWAN(x=1800), fab(1780, y=314, scale=0.8), office(140, "CLOUD", "blue"), office(300, "AI", "purple", scale=0.8),
               office(3300, "PHONES", "green"), office(3460, "CARS", "gold", scale=0.8),
               chips(1800, 220, [250, 160], C("Cloud companies"), rate=6), chips(1800, 220, [3380, 160], C("Phone makers"), rate=6),
               {"kind": "plane", "x": [[0, 2400], [24, 600]], "y": 150, "flip": True, "text": "CHIPS", "scale": 0.7}],
    "callouts": [co("Exports 2025: {{exports_2025.display}}", 960, 160, C("Taiwan's exports"), "gold", screen=True, size=44, sub="a record (Ministry of Finance)"),
                 co("+35% in one year", 960, 270, C("in a single year"), "green", screen=True)]},
    sources=["taiwan_exports_2025"])
add("s23_designers", "m3_designers", "engine_flow", {
    "title": "Everyone depends on someone", "subtitle": "designers → makers → machines, materials, software", "cardW": 270, "cardH": 210,
    "stages": [
        {"id": "d", "label": "Chip designers", "sub": "need makers", "x": 330, "y": 560, "kind": "design", "color": "accent2", "appear": 0.3, "output": "blueprint"},
        {"id": "t", "label": "Chip makers", "sub": "TSMC", "x": 960, "y": 560, "kind": "fab", "color": "accent", "appear": 0.45, "output": "chip"},
        {"id": "a", "label": "Dutch machines", "sub": "ASML", "x": 1600, "y": 300, "kind": "company", "color": "accent3", "appear": 0.6, "output": "box"},
        {"id": "j", "label": "Japanese materials", "sub": "", "x": 1600, "y": 560, "kind": "warehouse", "color": "accent3", "appear": 0.7, "output": "box"},
        {"id": "s", "label": "US design software", "sub": "", "x": 1600, "y": 820, "kind": "datacenter", "color": "accent3", "appear": 0.8, "output": "packet"}],
    "links": [{"from": "d", "to": "t", "appear": 0.9}, {"from": "a", "to": "t", "appear": 1.0}, {"from": "j", "to": "t", "appear": 1.1}, {"from": "s", "to": "t", "appear": 1.2}],
    "items": {"starts": [C("Companies that design"), C("Dutch machines"), C("Everyone depends")], "route": ["d", "t"], "travel": 0.8, "process": 0.8}})
add("s24_unequal", "m3_unequal", "compare", {"chapter": "Who depends on Taiwan", "title": "Not every chip is equal", "sides": [
    {"kicker": "AI chip · phone processor", "value": "Cutting edge", "label": "where Taiwan dominates", "cue": "cutting-edge"},
    {"kicker": "Car · washing machine", "value": "Older chips", "label": "made in many countries", "cue": "older, simpler"},
    {"kicker": "But…", "value": "1 chip", "label": "a missing cheap chip can stop a car factory", "cue": "Even so"}]})
kinetic("s25_t3", "m3_transition", [("What if the flow of chips", 56, "So what would", None, True), ("were suddenly interrupted?", 76, "interrupted", "risk", False)])

# ====================================================================== PART 4: a hypothetical disruption
card("s26_c4", "m4_card", "A Hypothetical Disruption", "A thought experiment, not a prediction")
cart("s27_q4", "m4_question", {
    "worldW": 2600, "min_seconds": 10.0, "banner": HYPO, "night": True,
    "cam": [{"at": 0, "x": 1300, "y": 400, "zoom": 1.1}], "drift": 0,
    "actors": [TAIWAN(x=1300), fab(1280, y=314, scale=0.8), ship(x=[[0, 1700], [12, 2000]], flag="CHIPS", crew=2), chips(1300, 220, [2400, 100], 0.3, rate=4, until=C("seriously disrupted"))],
    "callouts": [co("What if shipments stopped?", 1300, 170, C("What if"), "risk", size=44)]})
cart("s28_precedent", "m4_precedent", {
    "worldW": 2600, "coasts": {"plain": True, "left": True, "leftLabel": "CAR FACTORIES", "darkAt": C("hit carmakers")},
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 1.0}], "drift": 0,
    "actors": [office(150, "CAR PLANT", "blue"), office(310, "CAR PLANT", "green", scale=0.8), TAIWAN(x=2000), chips(2000, 220, [250, 160], 0.3, rate=0.8)],
    "callouts": [co("2021: a real chip shortage", 1000, 150, C("In twenty twenty-one"), "white", size=40, sub="caused by the pandemic, not by Taiwan"),
                 co("{{auto_2021.display}} lost revenue", 1000, 270, C("lost revenue"), "risk", size=42, sub="AlixPartners forecast"),
                 co("{{auto_2021.cars_display}} never built", 1000, 390, C("never built"), "risk")]},
    sources=["alix_2021"])
cart("s29_domino", "m4_domino", {
    "worldW": 3600, "banner": HYPO, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "DEVICE MAKERS", "rightLabel": "DATA CENTERS", "darkAt": C("Prices rise")},
    "cam": [{"at": 0, "x": 1800, "y": 400, "zoom": 1.0}, {"at": C("Carmakers"), "x": 1800, "y": 400, "zoom": 0.6, "dur": 3.0}], "drift": 0,
    "actors": [TAIWAN(x=1800, darkAt=C("supply stops")), fab(1780, y=314, scale=0.8), office(140, "PHONES", "green"), office(3460, "CLOUD", "blue"),
               ship(x=1200, flag="STOPPED", flagColor="risk", crew=3, sadAt=C("supply stops"), anchorAt=C("supply stops")),
               ship(x=2500, flag="STOPPED", flagColor="risk", crew=2, sadAt=C("supply stops"), anchorAt=C("supply stops", 0.4), flip=True, scale=0.8)],
    "callouts": [co("Phones slip", 600, 200, C("New phones"), "risk"), co("No new AI servers", 3000, 200, C("Cloud companies"), "risk"),
                 co("Car lines idle", 600, 310, C("Carmakers"), "risk"), co("Prices rise", 3000, 310, C("Prices rise"), "risk"),
                 co("Hard to replace quickly", 960, 960, C("very hard to replace"), "white", screen=True)]})
# ---- PRESENTER D: the chain breaks
add("p30_chain", "m4_chain", "engine_draw", {
    "title": "Break the first link (hypothetical)", "board": BOARD, "draw_start": C("Taiwan's fabs"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1650, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 420, 220, 100), "color": "accent", "width": 5, "start": C("Taiwan's fabs"), "label": lbl("FABS", 630, 480, 28, "accent")},
        {"d": arrow((750, 470), (820, 470)), "color": "ink", "width": 4, "start": C("Then packaging", -0.2)},
        {"d": rect(830, 420, 220, 100), "color": "accent2", "width": 5, "start": C("Then packaging"), "label": lbl("PACKAGING", 940, 480, 26, "accent2")},
        {"d": arrow((1060, 470), (1130, 470)), "color": "ink", "width": 4, "start": C("device makers", -0.2)},
        {"d": rect(1140, 420, 220, 100), "color": "accent2", "width": 5, "start": C("device makers"), "label": lbl("DEVICES", 1250, 480, 26, "accent2")},
        {"d": arrow((1250, 530), (1250, 610)), "color": "ink", "width": 4, "start": C("the stores", -0.2)},
        {"d": rect(1140, 620, 220, 100), "color": "accent2", "width": 5, "start": C("the stores"), "label": lbl("STORES · CLOUD", 1250, 680, 22, "accent2")},
        {"d": "M 600 440 L 660 500 M 660 440 L 600 500", "color": "risk", "width": 10, "start": C("break the very first")},
        {"d": rect(830, 420, 220, 100), "color": "risk", "width": 7, "start": C("watch the shock")},
        {"d": rect(1140, 420, 220, 100), "color": "risk", "width": 7, "start": C("watch the shock", 0.5)},
        {"d": rect(1140, 620, 220, 100), "color": "risk", "width": 7, "start": C("turns red")},
        {"d": "M 560 900 L 560 800 L 640 800 L 640 900 M 700 900 L 700 760 L 780 760 L 780 900", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar",
         "start": C("turns red", 0.4), "label": lbl("shock spreads", 670, 950, 24, "risk")},
    ],
    "actions": [{"kind": "react", "at": C("break the very first", 0.3)}, {"kind": "point", "at": C("turns red", 0.3), "dur": 1.3, "target": [1250, 670]}],
    "scale": 0.86, "floor": 1040})
add("s31_estimate", "m4_estimate", "compare", {"chapter": "A hypothetical disruption", "title": "Bloomberg Economics scenarios (2024)", "sides": [
    {"kicker": "War over Taiwan, first year", "value": "{{bloomberg_scenarios.pct_display}}", "label": "{{bloomberg_scenarios.display}}", "cue": "a war over Taiwan"},
    {"kicker": "Blockade", "value": "{{bloomberg_scenarios.blockade_display}}", "label": "scenario, depends on assumptions", "cue": "Even a blockade"}]},
    sources=["bloomberg_2024"])
kinetic("s32_t4", "m4_transition", [("Numbers like that", 56, "Numbers like", None, True), ("explain the race to make chips at home", 66, "racing", "accent", False)])

# ====================================================================== PART 5: the race to diversify
card("s33_c5", "m5_card", "The Race to Diversify", "Expensive, and slow")
cart("s34_q5", "m5_question", {
    "worldW": 3000, "min_seconds": 9.0, "coasts": {"plain": True, "left": True, "leftLabel": "NEW FABS"},
    "cam": [{"at": 0, "x": 1400, "y": 400, "zoom": 0.85}], "drift": 0,
    "actors": [fab(150, "FAB", at=C("spread the risk")), fab(320, "FAB", at=C("spread the risk", 0.5), scale=0.8), TAIWAN(x=2200), fab(2180, y=314, scale=0.8)],
    "callouts": [co("Spread the risk?", 1300, 160, C("spread the risk"), "gold", size=48), co("Expensive · slow", 1300, 270, C("expensive"), "risk")]})
add("s35_race", "m5_race", "engine_map", {
    "title": "The race to build fabs elsewhere", "subtitle": "CHIPS Act {{chips_act_figs.display}} · TSMC Arizona {{tsmc_us_165.display}} · Kumamoto {{japan_jasm.display}}",
    "cameras": [{"at": 0, "lon": 150, "lat": 30, "span": 160}, {"at": C("America's CHIPS"), "lon": -150, "lat": 30, "span": 160, "dur": 3.0},
                {"at": C("In Japan"), "lon": 140, "lat": 28, "span": 60, "dur": 2.6}],
    "drift": {"lon": 0.2, "zoom": 0.006}, "tilt": [[0, 12], [20, 5]],
    "highlights": [{"iso": "TWN", "color": "accent", "at": 0.3}, {"iso": "USA", "color": "accent2", "at": C("America's CHIPS")}, {"iso": "JPN", "color": "accent2", "at": C("In Japan")}],
    "hubs": [{"id": "t", "at": LL["hsinchu"], "label": "Taiwan", "color": "accent", "time": 0.3},
             {"id": "a", "at": LL["arizona"], "label": "Arizona", "sub": "{{tsmc_us_165.display}} (TSMC)", "color": "accent2", "time": C("in Arizona"), "anchor": "end"},
             {"id": "k", "at": LL["kumamoto"], "label": "Kumamoto", "sub": "{{japan_jasm.display}}", "color": "accent2", "time": C("In Japan")}],
    "routes": [{"from": LL["hsinchu"], "to": LL["arizona"], "at": C("TSMC plans"), "dur": 2.0, "color": "accent2", "tokenShape": "box", "tokens": 20, "tokenEvery": 0.5, "lift": 0.2},
               {"from": LL["hsinchu"], "to": LL["kumamoto"], "at": C("In Japan"), "dur": 1.0, "color": "accent2", "tokenShape": "box", "tokens": 20, "tokenEvery": 0.5, "lift": 0.25}],
    "caption": "Real locations (Natural Earth) · arrows schematic"},
    sources=["chips_act", "tsmc_165bn", "jasm", "natural_earth"], assets=GEO)
cart("s36_europe", "m5_europe", {
    "worldW": 3400, "coasts": {"plain": True, "left": True, "leftLabel": "EUROPE"},
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 1.0}, {"at": C("And Taiwan keeps"), "x": 2400, "y": 400, "zoom": 0.9, "dur": 3.0}], "drift": 0,
    "actors": [fab(150, "DRESDEN", at=C("In Germany")), office(320, "EU 20%", "blue", at=C("Europe wants"), scale=0.8), TAIWAN(x=2700), fab(2680, y=314, scale=0.8),
               fab(2850, "NEW FAB", at=C("newest fabs"), scale=0.6) | {"y": 314}],
    "callouts": [co("Dresden: ESMC (TSMC + Bosch + Infineon + NXP)", 960, 160, C("In Germany"), "white", screen=True, sub="production targeted end-2027"),
                 co("EU goal: {{eu_target.display}}", 960, 270, C("Europe wants"), "gold", screen=True, size=40),
                 co("South Korea: memory + foundries", 960, 960, C("South Korea"), "white", screen=True),
                 co("…and Taiwan keeps building", 2400, 180, C("And Taiwan keeps"), "green")]},
    sources=["esmc", "oecd_chips"])
add("s37_limits", "m5_limits", "engine_chart", {"chart": "bar", "box": {"x": 460, "y": 340, "w": 1000, "h": 480}, "start": C("still has Taiwan"), "stagger": 1.2,
    "title": "Advanced logic capacity, 2032 forecast", "note": "SIA/BCG forecast · diversification reduces the risk, it doesn't remove it",
    "valueSuffix": "%", "data": [{"label": "Taiwan", "value": 47}, {"label": "United States", "value": 28}],
    "highlight": 0, "highlightAt": C("doesn't remove"), "color": "accent2", "highlightColor": "accent"},
    sources=["sia_bcg_2024"])
cart("s38_why", "m5_why", {
    "worldW": 3000, "coasts": {"plain": True, "left": True, "leftLabel": "NEW FAB ABROAD"},
    "cam": [{"at": 0, "x": 900, "y": 400, "zoom": 1.0}, {"at": C("Taiwan has spent"), "x": 2200, "y": 400, "zoom": 0.9, "dur": 3.0}], "drift": 0,
    "actors": [fab(180, "NEW FAB", at=C("can be built")), TAIWAN(x=2300), fab(2280, y=314, scale=0.8), office(2500, "SUPPLIERS", "blue", scale=0.6) | {"y": 314},
               chips(2300, 220, [2500, 180], 0.4, rate=4)],
    "callouts": [co("The hard part: people + suppliers + yield", 960, 160, C("the hard part"), "gold", screen=True, size=40),
                 co("Building a fab: a few years", 900, 280, C("can be built"), "green"),
                 co("The whole ecosystem: much longer", 2200, 180, C("much longer"), "risk")]})

# ====================================================================== PAYOFF
cart("s39_payoff", "payoff", {
    "worldW": 4400, "coasts": {"plain": True, "left": True, "right": True, "leftLabel": "THE WORLD", "rightLabel": "THE WORLD"},
    "cam": [{"at": 0, "x": 2200, "y": 380, "zoom": 1.3}, {"at": C("at a scale"), "x": 2200, "y": 400, "zoom": 0.5, "dur": 4.0},
            {"at": C("the whole world is watching"), "x": 2200, "y": 380, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "actors": [TAIWAN(x=2200), fab(2180, y=314, scale=0.8), office(140, "AI", "purple"), office(300, "PHONES", "green", scale=0.8),
               office(4100, "CARS", "gold"), office(4260, "CLOUD", "blue", scale=0.8),
               chips(2200, 220, [250, 160], C("hardest ones"), rate=6), chips(2200, 220, [4180, 160], C("hardest ones", 0.3), rate=6),
               {"kind": "plane", "x": [[0, 2600], [30, 700]], "y": 140, "flip": True, "text": "CHIPS", "scale": 0.7}],
    "callouts": [co("Not every chip, the hardest ones", 960, 160, C("hardest ones"), "gold", screen=True, size=42),
                 co("Strength… and weak point", 960, 270, C("weak point"), "risk", screen=True, size=40)]},
    sources=["trendforce_2q26", "sia_bcg_2024"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

write(OUT, "# GENERATED by tools/gen_taiwan_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 07 v2 storyboard: cartoon remake. The channel intro is inserted automatically after the hook.\n")
