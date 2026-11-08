"""Generates projects/why-taiwan-matters-cartoon/deliverables/documentary/storyboard.yaml (Episode 07 v2).

Cartoon remake of Episode 07 in bespoke CartoonStage worlds: a semiconductor clean room (bunny suits, wafers, an EUV
machine with violet light, overhead wafer pods, robot arms), a science park with scooters, data centers, a car plant
whose line stops, falling dominoes for the hypothetical, construction sites for fabs abroad. No mission talk.
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

F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
FAB = lambda x0=-1600, x1=4600, **kw: Z("fab", x0, x1, **kw)
PARK = lambda x0=-1600, x1=4600, **kw: Z("sciencepark", x0, x1, **kw)


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def suits(xs, pose="stand", at=0.2):
    """Clean-room workers in bunny suits (generic, no likeness)."""
    return crowd(xs, pose, at=at, suit=True, scale=1.0)


# ====================================================================== HOOK
stage("s01_island", "h_question", {
    "zones": [PARK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 760, "y": 640, "zoom": 1.5}, {"at": C("depended on"), "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("conveyor", x0=1100, x1=1800, y=F - 30, goods="chip", n=6, speed=140),
              it("plane", x=[[0, 1250], [{"cue": "depended on"}, 1250], [{"cue": "depended on", "offset": 6}, 2600]], y=[[0, 420], [{"cue": "depended on", "offset": 6}, 150]], text="", scale=0.6, tilt=-10),
              it("device", type="phone", x=300, y=520, at=C("most important"), scale=0.7), it("device", type="laptop", x=520, y=540, at=C("most important", 0.3), scale=0.7),
              it("device", type="car", x=1500, y=560, at=C("most important", 0.6), scale=0.6)],
    "callouts": [co("One of the world's most important industries", 960, 150, C("most important"), "white", screen=True, until=C("smaller than Switzerland", -0.3)),
                 co("…on an island smaller than Switzerland?", 960, 150, C("smaller than Switzerland"), "gold", screen=True, size=44)]})
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
stage("s04_q1", "m1_question", {
    "zones": [FAB()], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.3}, {"at": C("runs on chips"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("wafer", x=960, y=430, r=190, at=0.3, spin=8, n=9),
              it("pod", x=[[0, -100], [8, 2000]], dropAt=99), *suits([520, 1400]),
              it("device", type="phone", x=380, y=420, at=C("runs on chips"), scale=0.55), it("device", type="laptop", x=1560, y=440, at=C("runs on chips", 0.3), scale=0.55),
              it("device", type="car", x=1500, y=F, at=C("someone has to"), scale=0.55), it("device", type="washer", x=420, y=F, at=C("someone has to", 0.3), scale=0.5)],
    "callouts": [co("A small island… the center of chipmaking?", 960, 140, C("small island"), "gold", screen=True, size=40),
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
stage("s10_q2", "m2_question", {
    "zones": [Z("site", -1600, 1500), PARK(1500, 5000)], "worldW": 3000, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.0}, {"at": C("not be special"), "x": 1700, "y": 540, "zoom": 0.85, "dur": 2.6}], "drift": 0,
    "items": [it("crane", x=500, text="NEW FAB?", at=C("build its own"), progress=[[0, 0.05], [12, 0.2]], scale=1.0),
              *crowd([1050], "shrug", at=C("build its own", 0.6), hat="#FFC93C")],
    "callouts": [co("Just copy it?", 960, 150, C("build its own"), "gold", screen=True, size=48, until=C("not be special", -0.3)),
                 co("Then Taiwan wouldn't be special", 960, 150, C("not be special"), "white", screen=True)]})
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
stage("s12_euv", "m2_euv", {
    "zones": [FAB(label="yellow")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.25}, {"at": C("Only one company"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("litho", x=760, at=0.2, fireAt=C("smallest features"), text="EUV MACHINE", sub="extreme ultraviolet light"),
              it("sign", x=1500, y=340, text="ONLY ONE MAKER", sub="ASML · the Netherlands", at=C("Only one company"), color="#FFF59D", size=40),
              it("conveyor", x0=1250, x1=1800, y=F - 30, goods="box", label="EUV", n=4, speed=60, at=C("it shipped")),
              *suits([1150])],
    "callouts": [co("To print the smallest features…", 960, 150, C("smallest features"), "white", screen=True, until=C("Only one company", -0.3)),
                 co("{{asml_only.display}}", 960, 960, C("it shipped"), "green", screen=True, size=44)]},
    sources=["asml_euv", "asml_2025"])
stage("s13_yield", "m2_yield", {
    "zones": [FAB()], "worldW": 2400,
    "cam": [{"at": 0, "x": 760, "y": 500, "zoom": 1.15}, {"at": C("brand-new factory"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("wafer", x=700, y=430, r=230, at=0.3, n=11, revealAt=C("actually work"), fail=[[0, 0.45], [{"cue": "endless learning"}, 0.45], [{"cue": "endless learning", "offset": 4}, 0.08]], text="GREEN = WORKS · RED = FAILS"),
              *suits([1080], pose="read"),
              it("chart", x=1650, y=380, w=560, h=330, at=C("brand-new factory"), dur=5, text="YIELD OVER TIME (schematic)", pts=[0.1, 0.15, 0.25, 0.4, 0.55, 0.7, 0.8, 0.88]),
              it("sign", x=1650, y=720, text="NEW FAB", sub="same machines, lower yield at first", at=C("same machines"), color="#FFCDD2", size=30)],
    "callouts": [co("Yield: the share of chips that work", 960, 150, C("The real secret"), "gold", screen=True, size=40, until=C("brand-new factory", -0.3)),
                 co("Know-how: hard to buy, harder to copy", 960, 150, C("hard to buy"), "white", screen=True)]})
stage("s14_capex", "m2_capex", {
    "zones": [PARK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.1}, {"at": C("Across the industry"), "x": 960, "y": 480, "zoom": 0.9, "dur": 2.6}], "drift": 0,
    "items": [it("stack", x=560, at=C("TSMC planned"), h=[[0, 40], [{"cue": "TSMC planned"}, 40], [{"cue": "TSMC planned", "offset": 3}, 260]], text="{{capex_2026.display}}", sub="TSMC, 2026 plan"),
              it("stack", x=1350, at=C("Across the industry"), h=[[0, 40], [{"cue": "Across the industry"}, 40], [{"cue": "Across the industry", "offset": 4}, 640]], text="{{fab_investment.display}}", sub="new fabs worldwide, 2024–2032", color="gold"),
              it("crane", x=1800, progress=[[0, 0.2], [20, 0.9]], scale=1.0)],
    "callouts": [co("The price of the game", 960, 150, C("the money"), "gold", screen=True, size=44)]},
    sources=["tsmc_4q25_call", "sia_bcg_2024"])
add("s15_capacity", "m2_discovery", "engine_chart", {"chart": "bar", "box": {"x": 360, "y": 340, "w": 1200, "h": 480}, "start": C("most advanced logic"), "stagger": 1.0,
    "title": "Advanced logic capacity (below 10 nm), 2022", "note": "Taiwan holds {{total_capacity.display}} of ALL chip capacity, less than China (SIA/BCG)",
    "valueSuffix": "%", "data": [{"label": "Taiwan", "value": 69}, {"label": "South Korea", "value": 31}, {"label": "United States", "value": 0}],
    "highlight": 0, "highlightAt": C("Taiwan had"), "color": "accent2", "highlightColor": "accent"},
    sources=["sia_bcg_2024"])
stage("s16_layers", "m2_layers", {
    "zones": [FAB()], "worldW": 3000,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.05}, {"at": C("Advanced packaging"), "x": 1550, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("narrow"), "x": 2300, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("device", type="chip", x=600, y=640, at=C("Memory"), color="cyan", text="MEMORY (DRAM)"),
              it("sign", x=600, y=280, text="SOUTH KOREA: {{total_capacity.dram_kor_display}}", sub="of world DRAM capacity", at=C("led by South Korea"), color="#BBDEFB", size=32),
              it("conveyor", x0=1200, x1=1900, y=F - 30, goods="chip", n=9, speed=30, at=C("Advanced packaging", -0.5)),
              it("sign", x=1550, y=380, text="BOTTLENECK", sub="packaging joins chips + memory", at=C("bottleneck"), color="#FFCDD2", size=40, hang=True, swing=True),
              it("device", type="chip", x=2300, y=560, at=C("Taiwan's edge"), color="gold", text="THE MOST ADVANCED", scale=1.2),
              it("letters", x=2300, y=230, text="TOP", at=C("very top"), size=110, color="gold")],
    "callouts": [co("Chips are not one market", 960, 150, C("not one market"), "white", screen=True, size=40, until=C("Advanced packaging", -0.3)),
                 co("Taiwan's edge: narrow, but at the very top", 960, 150, C("narrow"), "gold", screen=True)]},
    sources=["sia_bcg_2024"])
kinetic("s17_t2", "m2_transition", [("Which raises the next question", 50, "Which raises", None, True), ("Who depends on that top?", 80, "Who depends", "accent", False)])

# ====================================================================== PART 3: who depends on Taiwan
card("s18_c3", "m3_card", "Who Depends on Taiwan", "Everyone depends on someone")
stage("s19_q3", "m3_question", {
    "zones": [FAB(x1=1200), Z("datacenter", 1200, 5000)], "worldW": 2600, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.05}, {"at": C("economic power"), "x": 1500, "y": 540, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("wafer", x=600, y=430, r=170, at=0.2, spin=6), *suits([300]),
              it("coins", **{"from": [800, 520], "to": [1900, 520]}, at=0.6, rate=4, shape="chip", arc=200)],
    "callouts": [co("Who depends on Taiwan?", 960, 150, C("Who actually"), "gold", screen=True, size=46, until=C("economic power", -0.3)),
                 co("Dependence = power + risk", 960, 150, C("economic power"), "risk", screen=True, size=42)]})
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
stage("s22_network", "m3_network", {
    "zones": [FAB(x1=1300), Z("datacenter", 1300, 2900), Z("carplant", 2900, 7000)], "worldW": 4300,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Cloud companies"), "x": 2100, "y": 540, "zoom": 1.0, "dur": 2.6},
            {"at": C("Phone makers"), "x": 3550, "y": 540, "zoom": 1.0, "dur": 2.6}, {"at": C("Taiwan's exports"), "x": 2200, "y": 520, "zoom": 0.55, "dur": 3.0}], "drift": 0,
    "items": [it("conveyor", x0=200, x1=1150, y=F - 30, goods="chip", n=7, speed=160),
              it("coins", **{"from": [1150, 500], "to": [2100, 420]}, at=C("Cloud companies"), rate=5, shape="chip"),
              it("device", type="server", x=2100, y=F, at=C("data centers"), text="AI SERVERS"),
              it("conveyor", x0=3100, x1=4100, y=F - 30, goods="car", n=5, speed=90, at=C("Phone makers", -1)),
              it("device", type="phone", x=3200, y=560, at=C("Phone makers"), scale=0.8), it("device", type="laptop", x=3500, y=560, at=C("PC makers"), scale=0.8),
              it("plane", x=[[0, 2600], [26, 300]], y=180, flip=True, text="", scale=0.6)],
    "callouts": [co("Cloud: data centers full of AI chips", 960, 150, C("Cloud companies"), "white", screen=True, until=C("Phone makers", -0.3)),
                 co("Phones · PCs · cars", 960, 150, C("Phone makers"), "white", screen=True, until=C("Taiwan's exports", -0.3)),
                 co("Exports 2025: {{exports_2025.display}}", 960, 150, C("Taiwan's exports"), "gold", screen=True, size=44, sub="a record (Ministry of Finance)"),
                 co("+35% in one year", 960, 960, C("in a single year"), "green", screen=True)]},
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
stage("s24_unequal", "m3_unequal", {
    "zones": [FAB(x1=1500), Z("carplant", 1500, 5000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("older, simpler", -0.6), "x": 2300, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("device", type="chip", x=560, y=600, at=C("cutting-edge"), color="gold", text="AI CHIP", scale=1.1),
              it("device", type="phone", x=960, y=640, at=C("phone processor"), text="NEW PHONE"),
              it("sign", x=760, y=280, text="MOST ADVANCED FABS", sub="where Taiwan dominates", at=C("that is where"), color="#FFF59D", size=32),
              it("device", type="car", x=1900, y=560, at=C("A car"), scale=0.8), it("device", type="washer", x=2250, y=560, at=C("washing machine"), scale=0.8),
              it("sign", x=2080, y=280, text="OLDER, SIMPLER CHIPS", sub="made in many countries", at=C("older, simpler"), color="#C8E6C9", size=32),
              it("conveyor", x0=2500, x1=3300, y=F - 30, goods="car", n=4, speed=90, at=C("Even so", -1.0), stopAt=C("stop a car factory"), gapAt=C("missing cheap chip"))],
    "callouts": [co("Not every chip is equal", 960, 150, C("not every industry"), "white", screen=True, size=40, until=C("Even so", -0.3)),
                 co("One missing cheap chip can stop a car factory", 960, 150, C("Even so"), "risk", screen=True)]})
kinetic("s25_t3", "m3_transition", [("What if the flow of chips", 56, "So what would", None, True), ("were suddenly interrupted?", 76, "interrupted", "risk", False)])

# ====================================================================== PART 4: a hypothetical disruption
card("s26_c4", "m4_card", "A Hypothetical Disruption", "A thought experiment, not a prediction")
stage("s27_q4", "m4_question", {
    "zones": [PARK(night=True)], "worldW": 1920, "min_seconds": 10.0, "banner": HYPO, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.15}], "drift": 0,
    "items": [it("conveyor", x0=1000, x1=1750, y=F - 30, goods="chip", n=6, speed=130, stopAt=C("seriously disrupted")),
              it("letters", x=1380, y=420, text="?", at=C("seriously disrupted", 0.4), size=130, color="gold")],
    "callouts": [co("What if shipments stopped?", 960, 960, C("What if"), "risk", screen=True, size=44)]})
stage("s28_precedent", "m4_precedent", {
    "zones": [{"set": "carplant", "x0": -1600, "x1": 4000, "idle": None}], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.15}, {"at": C("lost revenue"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("conveyor", x0=250, x1=1650, y=F - 30, goods="car", n=7, speed=100, stopAt=C("hit carmakers", 0.4), gapAt=C("hit carmakers")),
              *crowd([500, 1400], "worry", at=C("hit carmakers", 0.6), hat="#FFC93C"),
              it("calendar", x=330, y=300, at=0.2, pages=[[0, "2021", "THE SHORTAGE"]], scale=0.75)],
    "callouts": [co("2021: a real chip shortage", 960, 150, C("In twenty twenty-one"), "white", screen=True, size=40, sub="caused by the pandemic, not by Taiwan", until=C("lost revenue", -0.3)),
                 co("{{auto_2021.display}} lost revenue", 960, 150, C("lost revenue"), "risk", screen=True, size=42, sub="AlixPartners forecast"),
                 co("{{auto_2021.cars_display}} never built", 960, 960, C("never built"), "risk", screen=True)]},
    sources=["alix_2021"])
stage("s29_domino", "m4_domino", {
    "zones": [PARK(night=True)], "worldW": 2600, "banner": HYPO, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.05}, {"at": C("Carmakers"), "x": 1350, "y": 520, "zoom": 0.9, "dur": 3.0}], "drift": 0,
    "items": [it("domino", x=300, gap=300, h=400, at=0.3, labels=["CHIP SUPPLY", "PHONES + PCs", "AI SERVERS", "CAR LINES", "PRICES", "OTHER INDUSTRIES"],
                 fallAt=[C("supply stops"), C("New phones"), C("Cloud companies"), C("Carmakers"), C("Prices rise"), C("never thought")])],
    "callouts": [co("Supply stops", 960, 150, C("supply stops"), "risk", screen=True, until=C("New phones", -0.2)),
                 co("Phones and computers slip", 960, 150, C("New phones"), "risk", screen=True, until=C("Cloud companies", -0.2)),
                 co("No new AI servers", 960, 150, C("Cloud companies"), "risk", screen=True, until=C("Carmakers", -0.2)),
                 co("Car lines idle", 960, 150, C("Carmakers"), "risk", screen=True, until=C("Prices rise", -0.2)),
                 co("Prices rise… the shock spreads", 960, 150, C("Prices rise"), "risk", screen=True, until=C("very hard to replace", -0.3)),
                 co("Hard to replace quickly", 960, 150, C("very hard to replace"), "white", screen=True)]})
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
stage("s34_q5", "m5_question", {
    "zones": [Z("site")], "worldW": 2400, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("expensive"), "x": 1300, "y": 520, "zoom": 0.9, "dur": 2.6}], "drift": 4,
    "items": [it("crane", x=500, text="NEW FAB", at=C("spread the risk"), progress=[[0, 0.1], [14, 0.35]], scale=1.0),
              it("crane", x=1500, text="NEW FAB", at=C("spread the risk", 0.5), progress=[[0, 0.05], [14, 0.3]], scale=1.0),
              it("stack", x=2100, at=C("expensive"), h=[[0, 40], [{"cue": "expensive"}, 40], [{"cue": "expensive", "offset": 3}, 360]], text="$$$")],
    "callouts": [co("Spread the risk?", 960, 150, C("spread the risk"), "gold", screen=True, size=48, until=C("expensive", -0.3)),
                 co("Expensive · slow", 960, 150, C("expensive"), "risk", screen=True, size=44)]})
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
stage("s36_europe", "m5_europe", {
    "zones": [Z("site", -1600, 1700), PARK(1700, 5000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("And Taiwan keeps"), "x": 2500, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 0,
    "items": [it("sign", x=230, y=560, text="DRESDEN, GERMANY", post=True, at=C("In Germany"), color="#FFF59D", size=28),
              it("crane", x=800, text="ESMC", at=C("In Germany"), progress=[[0, 0.2], [{"cue": "South Korea"}, 0.55]], scale=1.05),
              it("sign", x=1300, y=360, text="EU GOAL: {{eu_target.display}}", sub="of global chip production", at=C("Europe wants"), color="#BBDEFB", size=34),
              it("crane", x=2700, text="NEW FAB", at=C("newest fabs", -0.4), progress=[[0, 0.3], [{"cue": "newest fabs"}, 0.3], [{"cue": "newest fabs", "offset": 4}, 0.85]], scale=1.0)],
    "callouts": [co("Dresden: ESMC (TSMC + Bosch + Infineon + NXP)", 960, 150, C("In Germany"), "white", screen=True, sub="production targeted end-2027", until=C("Europe wants", -0.3)),
                 co("EU goal: {{eu_target.display}}", 960, 150, C("Europe wants"), "gold", screen=True, size=40, until=C("South Korea", -0.3)),
                 co("South Korea: memory + its own foundries", 960, 150, C("South Korea"), "white", screen=True, until=C("And Taiwan keeps", -0.3)),
                 co("…and Taiwan keeps building at home", 960, 150, C("And Taiwan keeps"), "green", screen=True)]},
    sources=["esmc", "oecd_chips"])
add("s37_limits", "m5_limits", "engine_chart", {"chart": "bar", "box": {"x": 460, "y": 340, "w": 1000, "h": 480}, "start": C("still has Taiwan"), "stagger": 1.2,
    "title": "Advanced logic capacity, 2032 forecast", "note": "SIA/BCG forecast · diversification reduces the risk, it doesn't remove it",
    "valueSuffix": "%", "data": [{"label": "Taiwan", "value": 47}, {"label": "United States", "value": 28}],
    "highlight": 0, "highlightAt": C("doesn't remove"), "color": "accent2", "highlightColor": "accent"},
    sources=["sia_bcg_2024"])
stage("s38_why", "m5_why", {
    "zones": [Z("site", -1600, 1500), FAB(1500, 5000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.0}, {"at": C("Taiwan has spent"), "x": 2300, "y": 540, "zoom": 0.95, "dur": 3.0}], "drift": 0,
    "items": [it("crane", x=700, text="NEW FAB", at=0.2, progress=[[0, 0.2], [{"cue": "can be built"}, 0.25], [{"cue": "can be built", "offset": 3}, 1.0]], scale=1.0),
              it("sign", x=1150, y=330, text="EMPTY INSIDE?", sub="engineers · suppliers · yield learning", at=C("the engineers"), color="#FFCDD2", size=30),
              *suits([1800, 1950, 2100, 2250, 2400, 2550, 2700], at=C("decades")),
              it("arm", x=2950, at=C("decades")), it("pod", x=[[0, 1700], [30, 3100]], dropAt=C("ecosystem"))],
    "callouts": [co("The hard part isn't the building", 960, 150, C("the hard part"), "gold", screen=True, size=40, until=C("can be built", -0.3)),
                 co("A fab: a few years", 960, 150, C("can be built"), "green", screen=True, until=C("much longer", -0.3)),
                 co("The whole ecosystem: much longer", 960, 150, C("much longer"), "risk", screen=True)]})

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [PARK()], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.4}, {"at": C("at a scale"), "x": 960, "y": 540, "zoom": 1.0, "dur": 3.5},
            {"at": C("the whole world is watching"), "x": 960, "y": 520, "zoom": 1.08, "dur": 3.0}], "drift": 0,
    "items": [it("device", type="chip", x=960, y=520, at=0.3, color="gold", text="THE HARDEST CHIPS", scale=1.3),
              it("coins", **{"from": [960, 420], "to": [200, 200]}, at=C("hardest ones"), rate=4, shape="chip"),
              it("coins", **{"from": [960, 420], "to": [1750, 200]}, at=C("hardest ones", 0.3), rate=4, shape="chip"),
              *crowd([180, 300, 1620, 1740], "point", at=C("the whole world is watching"))],
    "callouts": [co("Not every chip: the hardest ones", 960, 150, C("hardest ones"), "gold", screen=True, size=42, until=C("weak point", -0.3)),
                 co("Strength… and weak point", 960, 150, C("weak point"), "risk", screen=True, size=40, until=C("the whole world is watching", -0.3)),
                 co("The whole world is watching", 960, 960, C("the whole world is watching"), "white", screen=True, size=44)]},
    sources=["trendforce_2q26", "sia_bcg_2024"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})

write(OUT, "# GENERATED by tools/gen_taiwan_cartoon_storyboard.py; edit the generator, not this file.\n"
           "# Episode 07 v2 storyboard: cartoon remake. The channel intro is inserted automatically after the hook.\n")
