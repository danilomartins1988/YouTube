"""Generates projects/the-day-oil-was-worth-less-than-nothing/deliverables/documentary/storyboard.yaml (Episode 27,
WTI crude below zero on 20 April 2020).

Bespoke worlds (tones from visual_direction.yaml: thriller -> reflective -> strategy -> crisis): an emptied city and an
idle airport (the world that stopped), a night trading floor, a prairie tank farm (new `tankfarm` set) with storage tanks
whose gauges fill up (new `oiltank` item), oil drums with a negative price tag and banknotes paid away (new `barrel`
item), tankers at sea as floating storage, and the regulator's office. The price screen (`tradescreen` with a $0 line)
is the through-line and dives below zero.
Presenter: supply vs demand and storage (boxes + arrows), sell-or-take-delivery (boxes + arrows), the near-month discount
(boxes + arrow), that Monday (bars).
No exchange logos, no real trading UI, no likeness of real people (names in text only).
Run: python tools/gen_oil_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-day-oil-was-worth-less-than-nothing/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
WTI = "WTI MAY 2020 · $ / BARREL"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def screen(x=960, y=430, **kw):
    for k, v in (("text", WTI), ("max", 30), ("min", -45), ("hot", 999), ("lamp", False), ("decimals", 2)):
        kw.setdefault(k, v)
    return it("tradescreen", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("tankfarm", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.15}, {"at": 3.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 2,
    "items": [it("barrel", x=1000, at=0.2, n=3, tag="YOURS FREE", tagColor="green", tagAt=1.0),
              it("barrel", x=1000, at=0.1, n=0, payAt=C("and paid you", 0.2))],
    "callouts": [co("A barrel of oil… and money to take it?", 960, 960, C("What would you do"), "gold", screen=True, size=40)]},
    sources=["eia_apr27"])
stage("s02_stakes", "h_stakes", {
    "zones": [Z("exchange", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.0}, {"at": C("People who owned oil"), "x": 1250, "y": 480, "zoom": 0.9, "dur": 2.4}], "drift": 2,
    "items": [screen(900, 430, at=0.2, scale=0.9, price=[[0, 17.73], [{"cue": "fell below zero", "offset": -1}, 0.5], [{"cue": "it settled at", "offset": 1}, -37.63]]),
              it("barrel", x=1850, at=C("People who owned oil"), n=2, tag="−$37.63", tagAt=C("People who owned oil", 0.4), payAt=C("paying others", 0.2), scale=0.8)],
    "callouts": [co("First time below $0 since 1983", 960, 960, C("fell below zero"), "risk", screen=True, size=40, sub="CFTC staff report", until=C("At the end of the day", -0.3)),
                 co("Settled at −$37.63 a barrel", 960, 960, C("At the end of the day"), "risk", screen=True, size=42, until=C("To understand how", -0.3)),
                 co("An oil price is really a promise", 960, 960, C("To understand how"), "gold", screen=True, size=40)]},
    sources=["cftc"])

# ====================================================================== PART 1: a world that stopped
card("s03_c1", "m1_card", "A World That Stopped", "Spring 2020")
stage("s04_q1", "m1_question", {
    "zones": [Z("district", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("sign", x=960, y=380, at=0.3, text="CLOSED", sub="stay home", color="#FFCDD2", size=56)],
    "callouts": [co("When the world stops moving…", 960, 150, C("What happens"), "gold", screen=True, size=44)]})
stage("s05_demand", "m1_demand", {
    "zones": [Z("airport", -1600, 1500, night=True), Z("district", 1500, 6000, night=True)], "worldW": 3200, "night": True,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.0}, {"at": C("Roads"), "x": 1800, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Analysts cited"), "x": 2500, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("plane", x=700, y=640, at=0.2, text="GROUNDED", tilt=0),
              it("sign", x=1900, y=420, at=C("Roads"), text="EMPTY ROADS", color="#FFE082", size=40),
              it("counter", x=2500, y=220, at=C("Analysts cited"), prefix="−", suffix="M", steps=[[0, 0], [{"cue": "fell by", "offset": 1}, 30]], text="BARRELS A DAY OF DEMAND"),
              it("letters", x=2500, y=480, text="≈ 30% OF WORLD USE", at=C("around thirty percent"), size=56, color="risk")],
    "callouts": [co("Planes grounded, roads empty", 960, 960, C("In the spring"), "white", screen=True, size=40, until=C("Analysts cited", -0.3)),
                 co("Demand down ≈ 30M barrels a day (analysts)", 960, 960, C("Analysts cited"), "risk", screen=True, size=36, sub="CRS")]},
    sources=["crs"])
stage("s06_opec", "m1_opec", {
    "zones": [Z("parliament")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But it would only start"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "APR 12", "2020"], [{"cue": "But it would only start"}, "MAY 1", "CUT STARTS"]], scale=0.8),
              it("contract", x=1000, y=460, at=C("agreed to cut"), text="OPEC+ DEAL", sub="−9.7M barrels a day", signAt=C("the largest single", 0.2), scale=0.7),
              it("stack", x=1600, h=[[0, 40], [{"cue": "much smaller", "offset": 0.5}, 400]], at=C("And even a record cut"), text="DEMAND HOLE ≈ 30M", color="#C62828"),
              it("stack", x=1900, h=[[0, 40], [{"cue": "much smaller", "offset": 1}, 130]], at=C("And even a record cut"), text="CUT 9.7M", color="#1565C0")],
    "callouts": [co("Record cut: 9.7M barrels a day", 960, 960, C("On April twelfth"), "white", screen=True, size=40, sub="CFTC staff report", until=C("But it would only start", -0.3)),
                 co("Too late, and too small", 960, 960, C("But it would only start"), "risk", screen=True, size=42)]},
    sources=["cftc", "crs"])
add("p07_gap", "m1_draw", "engine_draw", {
    "title": "Where does the extra oil go?", "board": BOARD, "draw_start": C("Here is the oil coming out"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 360, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the oil coming out"), "label": lbl("PRODUCED", 670, 428, 26, "accent2")},
        {"d": rect(1200, 360, 260, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the oil the world"), "label": lbl("USED", 1330, 428, 26, "accent3")},
        {"d": arrow((810, 420), (1190, 420), 0.0), "color": "ink", "width": 5, "start": C("Here is the oil the world", 0.5)},
        {"d": rect(870, 660, 280, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Every barrel nobody wanted"), "label": lbl("STORAGE", 1010, 728, 28, "risk")},
        {"d": arrow((670, 490), (880, 650), 0.1), "color": "risk", "width": 5, "start": C("had to go somewhere"), "label": lbl("the gap", 700, 600, 22, "risk")},
        {"d": "M 880 800 L 1140 800", "color": "risk", "width": 6, "start": C("running out"), "label": lbl("FILLING UP", 1010, 840, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("running out", 0.2), "dur": 1.4, "target": [1010, 720]}],
    "scale": 0.86, "floor": 1040}, sources=["crs", "eia_apr27"])
kinetic("s08_t1", "m1_transition", [("How is oil really traded?", 60, "To see why", None, False)])

# ====================================================================== PART 2: paper barrels
card("s09_c2", "m2_card", "Paper Barrels", "How oil futures work")
stage("s10_q2", "m2_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=960, y=560, at=0.3, text="OIL CONTRACT", scale=0.8)],
    "callouts": [co("Buying oil: what do you own?", 960, 150, C("When you buy oil"), "gold", screen=True, size=44)]})
stage("s11_futures", "m2_futures", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Each month has"), "x": 1600, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("contract", x=900, y=460, at=C("A futures contract is"), text="FUTURES CONTRACT", sub="price fixed today · oil delivered later", scale=0.7),
              it("board", x=1700, y=380, at=C("Each month has"), text="WTI CONTRACTS", rows=[{"name": "MAY 2020", "color": "gold"}, {"name": "JUNE 2020"}, {"name": "JULY 2020"}]),
              it("calendar", x=2200, y=300, at=C("The May twenty twenty"), pages=[[0, "APR 21", "MAY EXPIRES"]], scale=0.75)],
    "callouts": [co("A promise to buy or sell barrels later", 960, 960, C("A futures contract is"), "white", screen=True, size=38, until=C("Each month has", -0.3)),
                 co("May contract expires 21 April", 960, 960, C("The May twenty twenty"), "gold", screen=True, size=40, sub="CFTC staff report")]},
    sources=["cftc"])
stage("s12_delivery", "m2_delivery", {
    "zones": [Z("exchange", -1600, 1300), Z("tankfarm", 1300, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("anyone still holding"), "x": 2100, "y": 500, "zoom": 0.95, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=800, y=560, at=0.3, text="MAY CONTRACT", scale=0.6, stamp="REAL OIL", stampAt=C("These contracts are for real oil")),
              it("barrel", x=2100, at=C("make or take physical delivery"), n=4, scale=0.75),
              it("sign", x=2100, y=260, at=C("anyone still holding"), text="CUSHING, OKLAHOMA", sub="delivery point", color="#FFE082", size=40)],
    "callouts": [co("At expiry: make or take delivery", 960, 960, C("anyone still holding"), "gold", screen=True, size=40, sub="EIA")]},
    sources=["eia_apr27"])
add("p13_choice", "m2_draw", "engine_draw", {
    "title": "Sell, or take the oil", "board": BOARD, "draw_start": C("Here is a trader"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 330, 300, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is a trader"), "label": lbl("MAY CONTRACT", 1010, 398, 26, "accent2")},
        {"d": rect(540, 640, 280, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Sell the contract"), "label": lbl("1 · SELL IT", 680, 708, 26, "accent3")},
        {"d": rect(1200, 640, 280, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Or keep it"), "label": lbl("2 · TAKE OIL", 1340, 708, 26, "risk")},
        {"d": arrow((930, 460), (720, 630), 0.1), "color": "ink", "width": 5, "start": C("Sell the contract")},
        {"d": arrow((1090, 460), (1300, 630), -0.1), "color": "ink", "width": 5, "start": C("Or keep it"), "label": lbl("+ find a tank", 1340, 600, 20, "risk")},
        {"d": "M 1200 790 L 1480 620", "color": "risk", "width": 7, "start": C("no tanks and no pipelines"), "label": lbl("no tank!", 1440, 800, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Sell before the deadline", 0.2), "dur": 1.4, "target": [680, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["eia_apr27", "crs"])
stage("s14_holders", "m2_holders", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But that still left"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("counter", x=1000, y=230, at=0.3, steps=[[0, 634727], [{"cue": "on the morning of", "offset": 1}, 108593]], text="OPEN MAY CONTRACTS"),
              it("calendar", x=500, y=320, at=0.3, pages=[[0, "APR 1", "2020"], [{"cue": "on the morning of"}, "APR 20", "MORNING"]], scale=0.75),
              *crowd([1500, 1620, 1740], "worry", at=C("But that still left"), scale=0.65)],
    "callouts": [co("634,727 → 108,593 open contracts", 960, 960, C("the number"), "white", screen=True, size=40, sub="CFTC staff report", until=C("But that still left", -0.3)),
                 co("One day to go", 960, 960, C("with one day to go"), "risk", screen=True, size=44)]},
    sources=["cftc"])
kinetic("s15_t2", "m2_transition", [("To take delivery, you need…", 56, "And to take delivery", None, True), ("somewhere to put the oil", 66, "Somewhere to put the oil", "gold", False)])

# ====================================================================== PART 3: nowhere to put it
card("s16_c3", "m3_card", "Nowhere to Put It", "Cushing, Oklahoma")
stage("s17_q3", "m3_question", {
    "zones": [Z("tankfarm")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("oiltank", x=960, at=0.3, fill=[[0, 0.6], [6, 0.95]], scale=0.85, fullAt=4.5)],
    "callouts": [co("When the tanks are full…", 960, 150, C("What happens"), "gold", screen=True, size=44)]})
stage("s18_cushing", "m3_cushing", {
    "zones": [Z("tankfarm")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("The three weeks"), "x": 1400, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("oiltank", x=900, at=0.2, fill=[[0, 0.0], [{"cue": "In mid-March"}, 0.5], [{"cue": "By April seventeenth", "offset": 2}, 0.76]], cap="CUSHING · 76M BARRELS", scale=0.9, warn=0.75, fullText="FILLING FAST", fullAt=C("filling fast")),
              it("calendar", x=1500, y=300, at=C("In mid-March"), pages=[[0, "MID-MAR", "≈ 50%"], [{"cue": "By April seventeenth"}, "APR 17", "76%"]], scale=0.8),
],
    "callouts": [co("76M barrels of space · 60M held", 960, 960, C("The storage tanks"), "white", screen=True, size=40, sub="EIA", until=C("The three weeks", -0.3)),
                 co("Record weekly builds in April", 960, 960, C("The three weeks"), "risk", screen=True, size=40, sub="EIA")]},
    sources=["eia_apr27", "cftc", "eia_apr30"])
stage("s19_committed", "m3_committed", {
    "zones": [Z("tankfarm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("For a trader looking"), "x": 1400, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("oiltank", x=900, at=0.2, fill=0.76, scale=0.8, warn=2),
              it("sign", x=900, y=200, at=C("some of the empty space"), text="SPACE: LEASED", sub="already promised", color="#FFCDD2", size=36),
              it("person", x=1600, pose="shrug", at=C("For a trader looking"), scale=0.8, hair=1, skin=2),
              it("magnifier", x=[[0, 1400], [6, 1900]], y=[[0, 520], [6, 480]], at=C("For a trader looking"), scale=0.7)],
    "callouts": [co("76% full ≠ 24% free", 960, 960, C("And seventy-six percent"), "gold", screen=True, size=44, sub="EIA", until=C("For a trader looking", -0.3)),
                 co("Almost nothing left to rent", 960, 960, C("For a trader looking"), "risk", screen=True, size=40)]},
    sources=["eia_apr27"])
stage("s20_sea", "m3_sea", {
    "zones": [Z("northsea")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Ships"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 4,
    "items": [it("ship", type="tanker", x=700, at=0.3, scale=0.8, flag="STORAGE"),
              it("ship", type="tanker", x=1500, at=C("rose by almost"), scale=0.75, flag="STORAGE"),
              it("ship", type="tanker", x=2250, at=C("Ships"), scale=0.7, flag="STORAGE"),
              it("counter", x=1200, y=200, at=C("In the first three weeks"), suffix="M", steps=[[0, 58], [{"cue": "rose by almost", "offset": 2}, 127]], text="BARRELS STORED AT SEA")],
    "callouts": [co("Floating storage: ≈127M barrels", 960, 960, C("In the first three weeks"), "white", screen=True, size=40, sub="CFTC staff report (Bloomberg data)", until=C("Ships", -0.3)),
                 co("Ships as floating warehouses", 960, 960, C("Ships"), "gold", screen=True, size=40)]},
    sources=["cftc"])
stage("s21_peak", "m3_peak", {
    "zones": [Z("tankfarm", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("The hub was never"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("oiltank", x=1000, at=0.2, fill=[[0, 0.76], [{"cue": "eighty-one percent", "offset": 0}, 0.81], [{"cue": "eighty-three percent", "offset": 0}, 0.83]], scale=0.9, warn=0.8, fullText="83%"),
              it("calendar", x=1600, y=300, at=0.3, pages=[[0, "APR 24", "81%"], [{"cue": "By the start of May"}, "MAY 1", "83%"]], scale=0.8)],
    "callouts": [co("81% (24 Apr) → 83% (early May)", 960, 960, C("A week later"), "white", screen=True, size=40, sub="EIA", until=C("The hub was never", -0.3)),
                 co("It didn't need to be full", 960, 960, C("The hub was never"), "risk", screen=True, size=40)]},
    sources=["eia_apr30", "eia_2021"])
add("p22_contango", "m3_draw", "engine_draw", {
    "title": "The price of a tank", "board": BOARD, "draw_start": C("Normally"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 260, 120), "color": "risk", "width": 6, "kind": "box", "start": C("oil for delivery right now"), "label": lbl("OIL NOW", 690, 488, 28, "risk")},
        {"d": rect(1200, 420, 260, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("the later months hold up"), "label": lbl("OIL LATER", 1330, 488, 28, "accent3")},
        {"d": arrow((830, 480), (1190, 480), 0.0), "color": "ink", "width": 5, "start": C("You have to pay someone"), "label": lbl("+ storage cost", 1010, 450, 22, "ink")},
        {"d": "M 690 560 L 690 760", "color": "risk", "width": 7, "start": C("So the near month falls"), "label": lbl("↓ falls", 760, 700, 24, "risk")},
        {"d": "M 1010 620 L 1010 760", "color": "accent", "width": 6, "start": C("The gap between them"), "label": lbl("GAP = PRICE OF A TANK", 1010, 800, 24, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("The gap between them", 0.2), "dur": 1.4, "target": [1010, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["eia_apr27", "cftc"])
kinetic("s23_t3", "m3_transition", [("Friday 17 April: $18.27", 60, "On Friday", None, True), ("Then came Monday", 70, "Then came Monday", "risk", False)])

# ====================================================================== PART 4: twenty minutes below zero
card("s24_c4", "m4_card", "Twenty Minutes Below Zero", "Monday, 20 April 2020")
stage("s25_q4", "m4_question", {
    "zones": [Z("exchange", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [screen(960, 430, at=0.3, scale=0.9, price=[[0, 18.27], [8, 1.0]])],
    "callouts": [co("Below nothing?", 960, 150, C("How can the price"), "gold", screen=True, size=48)]})
stage("s26_monday", "m4_monday", {
    "zones": [Z("exchange", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.0}, {"at": C("But there were very few"), "x": 1400, "y": 480, "zoom": 0.95, "dur": 2.4}], "drift": 2,
    "items": [screen(1000, 430, at=0.2, scale=0.95, price=[[0, 17.73], [{"cue": "kept falling", "offset": 1}, 10.0], [{"cue": "approaching zero", "offset": 1}, 0.5]]),
              *crowd([1700, 1820, 1940], "worry", at=C("Holders who could not"), scale=0.65),
              it("sign", x=2200, y=300, at=C("But there were very few"), text="BUYERS WITH A TANK?", color="#FFCDD2", size=36)],
    "callouts": [co("Everyone selling, few with a tank", 960, 960, C("Holders who could not"), "white", screen=True, size=40, sub="EIA · CRS", until=C("By the early afternoon", -0.3)),
                 co("Early afternoon: near $0", 960, 960, C("By the early afternoon"), "risk", screen=True, size=42)]},
    sources=["eia_apr27", "crs", "cftc"])
stage("s27_minutes", "m4_minutes", {
    "zones": [Z("exchange", night=True)], "worldW": 2200, "night": True, "min_seconds": 16,
    "shake": [{"at": 3.0, "dur": 1.6, "amp": 10}],
    "cam": [{"at": 0, "x": 1000, "y": 460, "zoom": 1.1}, {"at": C("A minute later"), "x": 1000, "y": 470, "zoom": 1.2, "dur": 2.0}], "drift": 1,
    "items": [screen(1000, 430, at=0.2, scale=1.05, price=[[0, 0.5], [{"cue": "the price fell from zero", "offset": 3}, -39.55], [{"cue": "A minute later", "offset": 1}, -40.32]]),
              it("clock", x=1700, y=300, at=0.3, period=0.5, text="2:08 → 2:28 PM"),
              it("letters", x=1000, y=110, text="$0 → −$39.55 IN 20 MINUTES", at=C("between eight minutes past two"), size=52, color="risk")],
    "callouts": [co("All-time low: −$40.32 at 2:29 p.m.", 960, 960, C("A minute later"), "risk", screen=True, size=40, sub="CFTC staff report")]},
    sources=["cftc"])
stage("s28_settle", "m4_settle", {
    "zones": [Z("tankfarm", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.0}, {"at": C("Some sellers were"), "x": 1250, "y": 490, "zoom": 0.9, "dur": 2.4}], "drift": 2,
    "items": [screen(850, 430, at=0.2, scale=0.85, price=[[0, -40.32], [3, -37.63]], haltAt=C("settled at", 1.5), haltText="SETTLED −$37.63"),
              it("barrel", x=1750, at=C("Some sellers were"), n=3, tag="−$37.63", tagAt=C("Some sellers were", 0.3), payAt=C("paying a counterparty"), scale=0.75)],
    "callouts": [co("Settled −$37.63; down $58.05 from the open", 960, 960, C("At the close"), "risk", screen=True, size=36, sub="CFTC staff report", until=C("Some sellers were", -0.3)),
                 co("Paying someone to take the contract", 960, 960, C("Some sellers were"), "gold", screen=True, size=40, sub="EIA")]},
    sources=["cftc", "eia_apr27"])
stage("s29_spread", "m4_spread", {
    "zones": [Z("exchange", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.0}, {"at": C("The June contract"), "x": 1350, "y": 470, "zoom": 0.88, "dur": 2.4}], "drift": 2,
    "items": [screen(950, 430, at=0.2, scale=0.75, price=[[0, 18.27], [4, -37.63]], text="MAY 2020"),
              screen(1780, 430, at=C("The June contract"), scale=0.75, price=[[0, 25.03], [3, 20.43]], text="JUNE 2020"),
              it("letters", x=1360, y=110, text="GAP: $6.76 → $58.06", at=C("By Monday's close"), size=52, color="gold")],
    "callouts": [co("May vs June gap: $7 → $58", 960, 960, C("On Friday"), "white", screen=True, size=40, sub="CFTC staff report", until=C("The June contract", -0.3)),
                 co("June: $20.43. Same oil, a month later", 960, 960, C("The June contract"), "gold", screen=True, size=38, sub="CRS")]},
    sources=["cftc", "crs"])
add("p30_monday", "m4_draw", "engine_draw", {
    "title": "That Monday", "board": BOARD, "draw_start": C("Here is the May contract on Friday"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 640 L 1460 640", "color": "ink", "width": 4, "start": C("Here is the May contract on Friday"), "label": lbl("$0", 570, 648, 22, "ink")},
        {"d": "M 720 640 L 720 560 L 880 560 L 880 640", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("eighteen dollars"), "label": lbl("MAY FRI $18.27", 800, 540, 22, "accent2")},
        {"d": "M 960 640 L 960 550 L 1120 550 L 1120 640", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the June contract"), "label": lbl("JUNE MON $20.43", 1040, 530, 22, "accent3")},
        {"d": "M 1200 640 L 1200 810 L 1360 810 L 1360 640", "color": "risk", "width": 7, "fill": "risk", "fillOpacity": 0.35, "kind": "bar", "start": C("almost thirty-eight dollars below zero"), "label": lbl("MAY MON −$37.63", 1280, 850, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Only the one that was about to arrive", 0.2), "dur": 1.4, "target": [1280, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["cftc", "crs"])
kinetic("s31_t4", "m4_transition", [("Headlines: negative oil", 58, "The next morning", None, True), ("The story was not over", 60, "But the story was not over", "gold", False)])

# ====================================================================== PART 5: the morning after
card("s32_c5", "m5_card", "The Morning After", "21 April 2020")
stage("s33_q5", "m5_question", {
    "zones": [Z("tankfarm")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("barrel", x=960, at=0.3, n=3, tag="WHOSE?", tagColor="gold", tagAt=1.0)],
    "callouts": [co("Who was left holding the oil?", 960, 150, C("Who was left"), "gold", screen=True, size=44)]})
stage("s34_next", "m5_next", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 470, "zoom": 1.0}, {"at": C("But the panic spread"), "x": 1600, "y": 470, "zoom": 1.0, "dur": 2.4}], "drift": 2,
    "items": [screen(800, 430, at=0.2, scale=0.75, price=[[0, -37.63], [{"cue": "positive again", "offset": 0}, 10.01]], text="MAY 2020 · LAST DAY"),
              screen(1800, 430, at=C("But the panic spread"), scale=0.75, price=[[0, 20.43], [{"cue": "fell by forty-three", "offset": 1}, 11.57]], text="JUNE 2020")],
    "callouts": [co("May's last day: +$10.01", 960, 960, C("On April twenty-first"), "white", screen=True, size=40, sub="CFTC staff report", until=C("But the panic spread", -0.3)),
                 co("June −43% to $11.57", 960, 960, C("But the panic spread"), "risk", screen=True, size=42, sub="CRS")]},
    sources=["cftc", "crs"])
stage("s35_who", "m5_who", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its interim report"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("On April twentieth"), steps=[[0, 0], [{"cue": "still held May contracts", "offset": 0}, 173]], suffix=" / 448", text="LARGE TRADERS STILL IN MAY"),
              it("docs", x=1600, y=560, at=C("Its interim report"), text="CFTC INTERIM REPORT", scale=0.6, stamp="NO SINGLE CAUSE", stampAt=C("did not name"))],
    "callouts": [co("173 of 448 large traders still in May", 960, 960, C("The regulator later"), "white", screen=True, size=38, sub="CFTC staff report", until=C("Its interim report", -0.3)),
                 co("No single cause named", 960, 960, C("did not name"), "gold", screen=True, size=42)]},
    sources=["cftc"])
stage("s36_cme", "m5_cme", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In almost forty years"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("docs", x=950, y=560, at=C("CME Group sent notices"), text="EXCHANGE NOTICE · APR 2020", scale=0.65, stamp="TEST PRICES < $0", stampAt=C("opened a testing system")),
              it("terminal", x=1600, y=F, at=C("opened a testing system"), text="PRICE: −1.00 → OK?", scale=0.8)],
    "callouts": [co("Early April: test systems for prices below $0", 960, 960, C("The exchange had seen"), "white", screen=True, size=36, sub="CFTC staff report (CME notices)", until=C("In almost forty years", -0.3)),
                 co("Never happened in ~40 years", 960, 960, C("In almost forty years"), "gold", screen=True, size=40)]},
    sources=["cftc"])
stage("s37_recovery", "m5_recovery", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.0}, {"at": C("Prices below zero"), "x": 1200, "y": 470, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [screen(1000, 430, at=0.2, scale=0.9, price=[[0, -37.63], [1.5, 10.01], [{"cue": "back at about", "offset": 1}, 40]], text="WTI · $ / BARREL", max=45),
              it("calendar", x=1800, y=300, at=C("By July first"), pages=[[0, "JUL 1", "≈ $40"]], scale=0.8)],
    "callouts": [co("1 July 2020: back at ≈ $40", 960, 960, C("By July first"), "gold", screen=True, size=42, sub="EIA")]},
    sources=["eia_2021"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("tankfarm", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 500, "zoom": 1.05}, {"at": C("On April twentieth"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 2.6}], "drift": 1,
    "items": [it("oiltank", x=700, at=0.2, fill=0.83, scale=0.75, warn=2),
              screen(1500, 430, at=C("On April twentieth"), scale=0.75, price=[[0, 17.73], [3, -37.63]]),
              it("letters", x=1300, y=110, text="WHERE · WHEN · ROOM TO STORE", at=C("It is also about where"), size=44, color="gold")],
    "callouts": [co("A price is also about where and when", 960, 960, C("That a price is not just"), "white", screen=True, size=38, until=C("On April twentieth", -0.3)),
                 co("The world ran out of places to put it", 960, 960, C("On April twentieth"), "gold", screen=True, size=38)]},
    sources=["cftc", "eia_apr27"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_oil_storyboard.py; edit the generator, not this file.\n"
           "# Episode 27 storyboard (WTI below zero, April 2020): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
