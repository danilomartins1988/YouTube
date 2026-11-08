"""Generates projects/indias-chip-plants-dont-make-chips/deliverables/documentary/storyboard.yaml (Episode 17, C4).

Bespoke worlds for India's back-end-first chip strategy (tones from visual_direction.yaml: strategy -> tech -> strategy ->
crisis -> reflective): a fab clean room for the front end, the new `osat` item (dicing, packaging and test line) as the
through-line in Sanand, a site with three plants opening one by one, an import bill of coins leaving through a port, a
phone shop where imports turn into local assembly, the Dholera construction site with a slipping calendar, ships stuck at
a port (2005), a cabinet room for Semicon 2.0, and a campus. Presenter: the value slices, why a fab is harder, the ladder.
No flags, no logos (names in text only), no likeness of real people, no smiling sun.
Run: python tools/gen_india_chips_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/indias-chip-plants-dont-make-chips/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
MIC, KAY, CGP, TATA, SAFF = "#7E57C2", "#26A69A", "#1565C0", "#283593", "#FF9933"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 4, "skin": (k % 3) + 1, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.25}, {"at": C("not one of them"), "x": 960, "y": 560, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("osat", x=960, at=0.2, rate=1.2, text="A CHIP PLANT", scale=0.95),
              it("letters", x=1600, y=200, text="?", at=C("not one of them"), size=150, color="gold")],
    "callouts": [co("A country opens its first chip plants…", 960, 150, C("opened its first"), "white", screen=True, size=40, until=C("not one of them", -0.3)),
                 co("…and none makes a chip from scratch", 960, 150, C("not one of them"), "gold", screen=True, size=42)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("site", -1600, 1700), Z("fab", 1700, 6000, label="yellow")], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 0.95}, {"at": C("But the first ones"), "x": 2300, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "2026", "INDIA"]], scale=0.8),
              *[it("megafab", x=600 + k * 230, w=280, h=150, n=3, progress=1, at=C("commercial production", 0.25 * k), color=SAFF if k % 2 else "#4CAF50", scale=0.7) for k in range(5)],
              it("plane", x=[[0, 1500], [{"cue": "made somewhere else", "offset": 3}, 2100]], y=[[0, 200], [{"cue": "made somewhere else", "offset": 3}, 420]], at=C("made somewhere else"), text="WAFERS FROM ABROAD", scale=0.6),
              it("osat", x=2550, at=C("But the first ones", -0.3), rate=1.2, text="FINISHING CHIPS", scale=0.7)],
    "callouts": [co("5 units in commercial production", 960, 960, C("commercial production"), "gold", screen=True, size=40, sub="Government of India (PIB), Sep 2026", until=C("But the first ones", -0.3)),
                 co("They finish chips made somewhere else", 960, 960, C("But the first ones"), "white", screen=True, size=40, until=C("And that, it turns out", -0.3)),
                 co("…maybe exactly the right way to start", 960, 960, C("And that, it turns out"), "gold", screen=True, size=40)]},
    sources=["pib_sep26", "tt_sites"])

# ====================================================================== PART 1: two halves
card("s03_c1", "m1_card", "Two Halves of a Chip", "Front end and back end")
stage("s04_q1", "m1_question", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("wafer", x=960, y=430, r=220, at=0.2, spin=8, revealAt=1.0, fail=0.05),
              it("magnifier", x=[[0, 500], [7, 1350]], y=[[0, 400], [7, 520]], at=0.5, scale=0.9)],
    "callouts": [co("What does 'making a chip' really mean?", 960, 150, C("What does it actually"), "gold", screen=True, size=40)]})
stage("s05_front", "m1_front", {
    "zones": [Z("fab", label="red")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("It is the hardest part"), "x": 1500, "y": 520, "zoom": 0.85, "dur": 2.6}], "drift": 3,
    "items": [it("litho", x=800, at=C("the front end", -0.3), fireAt=C("light and chemicals"), text="FRONT END · FAB", scale=0.75),
              it("wafer", x=1450, y=420, r=170, at=C("onto a silicon wafer", -0.4), spin=6, revealAt=C("layer after layer"), fail=0.05),
              it("counter", x=2100, y=230, at=C("One industry study"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "One industry study", "offset": 2}, 5], [{"cue": "One industry study", "offset": 5.5}, 20]], text="ONE MODERN FAB"),
              it("coins", **{"from": [2100, 300], "to": [900, 300]}, at=C("most expensive"), rate=6)],
    "callouts": [co("Front end: circuits built onto the wafer", 960, 960, C("the front end"), "white", screen=True, size=40, until=C("It is the hardest part", -0.3)),
                 co("A modern fab: ≈ $5bn to $20bn", 960, 960, C("One industry study"), "gold", screen=True, size=40, sub="BCG / SIA")]},
    sources=["bcg_sia"])
stage("s06_back", "m1_back", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920, "min_seconds": 18,
    "cam": [{"at": 0, "x": 700, "y": 560, "zoom": 1.25}, {"at": C("sealed inside"), "x": 960, "y": 560, "zoom": 1.15, "dur": 2.4},
            {"at": C("In India"), "x": 960, "y": 560, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("osat", x=960, at=0.2, rate=1.0, text="BACK END", scale=1.0, failEvery=6)],
    "callouts": [co("Cut · package · wire · test", 960, 150, C("The finished wafer is cut"), "white", screen=True, size=42, until=C("In India", -0.3)),
                 co("India calls it ATMP: assembly, testing, marking, packaging", 960, 150, C("In India"), "gold", screen=True, size=34, until=C("It is skilled work", -0.3)),
                 co("Skilled, but far cheaper than a fab", 960, 150, C("It is skilled work"), "white", screen=True, size=42)]},
    sources=["bcg_sia", "pib_sep26"])
add("p07_slices", "m1_draw", "engine_draw", {
    "title": "Where the money is", "board": BOARD, "draw_start": C("Split the value"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 800 L 1500 800", "color": "ink", "width": 4, "start": C("Split the value")},
        {"d": "M 600 800 L 600 360 L 820 360 L 820 800", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar",
         "start": C("Designing the chip"), "label": lbl("DESIGN 50%", 710, 340, 26, "accent2")},
        {"d": "M 900 800 L 900 580 L 1120 580 L 1120 800", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar",
         "start": C("Making the wafer"), "label": lbl("FAB ≈ 25%", 1010, 560, 26, "accent")},
        {"d": "M 1200 800 L 1200 747 L 1420 747 L 1420 800", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.4, "kind": "bar",
         "start": C("Packaging and testing"), "label": lbl("PACKAGE + TEST 6%", 1310, 727, 22, "accent3")},
        {"d": "M 1310 690 Q 1360 560 1460 520", "color": "risk", "width": 5, "start": C("the smallest slice"), "label": lbl("smallest…", 1480, 505, 24, "risk", "start")},
        {"d": rect(1240, 380, 150, 110), "color": "accent3", "width": 6, "start": C("the one door"), "label": lbl("…the open door", 1315, 520, 22, "accent3")},
        {"d": "M 1300 490 L 1300 420 M 1300 435 L 1330 435", "color": "accent3", "width": 4, "start": C("open first")},
    ],
    "actions": [{"kind": "point", "at": C("the one door", 0.2), "dur": 1.4, "target": [1315, 435]}],
    "scale": 0.86, "floor": 1040}, sources=["bcg_sia"])
kinetic("s08_t1", "m1_transition", [("India walked through that door", 58, "India walked", None, False), ("in a town called Sanand", 66, "a town called Sanand", "accent", False)])

# ====================================================================== PART 2: Sanand
card("s09_c2", "m2_card", "Sanand", "What is running today")
stage("s10_q2", "m2_question", {
    "zones": [Z("site")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 4,
    "items": [it("megafab", x=960, w=380, h=150, n=3, progress=1, at=0.3, color=MIC, text="?", scale=0.9),
              *crowd([500, 640, 1300, 1440], "walk", at=0.6, scale=0.7)],
    "callouts": [co("What is actually running in India?", 960, 150, C("What is actually"), "gold", screen=True, size=42)]})
stage("s11_sanand", "m2_sanand", {
    "zones": [Z("site")], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.0}, {"at": C("a second plant"), "x": 1600, "y": 540, "zoom": 0.95, "dur": 2.4},
            {"at": C("In July"), "x": 2300, "y": 540, "zoom": 0.95, "dur": 2.4}, {"at": C("All three"), "x": 1600, "y": 540, "zoom": 0.72, "dur": 2.6}], "drift": 3,
    "items": [it("sign", x=600, y=260, text="SANAND · GUJARAT", sub="industrial town", at=0.3, color="#FFE0B2", size=36),
              it("calendar", x=280, y=520, at=C("In February"), pages=[[0, "FEB", "2026"], [{"cue": "At the end of March"}, "MAR", "2026"], [{"cue": "In July"}, "JUL", "2026"]], scale=0.75),
              it("megafab", x=900, w=380, h=150, n=3, progress=1, at=C("Micron inaugurated"), color=MIC, text="MICRON", scale=0.9),
              it("device", type="server", x=1150, y=F, at=C("ships memory chips")),
              it("megafab", x=1650, w=380, h=150, n=3, progress=1, at=C("a second plant"), color=KAY, text="KAYNES", scale=0.9),
              it("megafab", x=2350, w=380, h=150, n=3, progress=1, at=C("a third"), color=CGP, text="CG + RENESAS", scale=0.9),
              *crowd([780, 1000, 1550, 1750, 2250, 2450], "cheer", at=C("All three"), scale=0.6)],
    "callouts": [co("Micron, Feb 2026: a {{sanand.display}} packaging and test plant", 960, 960, C("Micron inaugurated"), "gold", screen=True, size=36, sub="Tech Times", until=C("a second plant", -0.3)),
                 co("Kaynes, March · CG Power with Renesas, July", 960, 960, C("a second plant"), "white", screen=True, size=38, until=C("All three", -0.3)),
                 co("Three plants, one town", 960, 960, C("All three"), "gold", screen=True, size=42)]},
    sources=["tt_sites", "pib_apr26"])
stage("s12_inside", "m2_inside", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920, "min_seconds": 20,
    "cam": [{"at": 0, "x": 520, "y": 520, "zoom": 1.35}, {"at": C("Each die is placed"), "x": 960, "y": 560, "zoom": 1.15, "dur": 2.6},
            {"at": C("The machines and most"), "x": 960, "y": 560, "zoom": 0.95, "dur": 2.4}], "drift": 0,
    "items": [it("osat", x=960, at=0.1, rate=1.1, text="INSIDE A SANAND PLANT", scale=1.0),
              it("plane", x=[[0, -200], [4, 300]], y=[[0, 150], [4, 240]], at=C("Finished wafers arrive"), until=C("Machines cut"), text="WAFERS FROM ABROAD", scale=0.5)],
    "callouts": [co("Wafers arrive from fabs abroad", 960, 150, C("Finished wafers arrive"), "white", screen=True, size=40, until=C("Machines cut", -0.2)),
                 co("Cut → package → wire → seal → test", 960, 150, C("Machines cut"), "gold", screen=True, size=40, until=C("The machines and most", -0.3)),
                 co("Machines from the US, Japan, Taiwan, Korea…", 960, 150, C("The machines and most"), "white", screen=True, size=38, until=C("But the factory", -0.3)),
                 co("…the jobs and the know-how: India", 960, 150, C("But the factory"), "gold", screen=True, size=40)]},
    sources=["tt_sites"])
stage("s13_count", "m2_count", {
    "zones": [Z("site")], "worldW": 2800,
    "cam": [{"at": 0, "x": 1400, "y": 520, "zoom": 0.8}, {"at": C("Look at the mix"), "x": 1400, "y": 520, "zoom": 0.85, "dur": 2.2},
            {"at": C("In twenty twenty-one"), "x": 900, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=1400, y=200, at=C("In total"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "with investments", "offset": 1.5}, 17]], text="12 UNITS APPROVED (≈)"),
              it("litho", x=600, at=C("One silicon fab"), fireAt=C("One silicon fab", 0.4), text="SILICON FAB", scale=0.45, color=TATA),
              it("litho", x=950, at=C("two fabs for special"), fireAt=C("two fabs for special", 0.4), text="SiC", scale=0.35, color="#6D4C41"),
              it("litho", x=1200, at=C("two fabs for special", 0.3), fireAt=C("two fabs for special", 0.7), text="GaN", scale=0.35, color="#00838F"),
              *[it("megafab", x=1450 + k * 140, w=220, h=150, n=3, progress=1, at=C("packaging and test plants", 0.12 * k), color=SAFF if k < 5 else "#B0BEC5", text="", scale=0.55) for k in range(9)],
              it("calendar", x=700, y=300, at=C("In twenty twenty-one"), pages=[[0, "2021", "NO PLANT"]], scale=0.75)],
    "callouts": [co("12 units, ≈ {{units.display}}", 960, 960, C("In total"), "gold", screen=True, size=40, sub="PIB; converted at the Fed H.10 rate", until=C("Look at the mix", -0.3)),
                 co("1 silicon fab · 2 special fabs · 9 packaging plants", 960, 960, C("Look at the mix"), "white", screen=True, size=36, until=C("By September", -0.3)),
                 co("5 in production · in 2021: none", 960, 960, C("By September"), "gold", screen=True, size=40)]},
    sources=["pib_sep26", "pib_may26", "fred_inr"])
kinetic("s14_t2", "m2_transition", [("Why spend billions", 66, "So why would", None, False), ("on the smallest slice of the business?", 50, "the smallest slice", "accent", True)])

# ====================================================================== PART 3: the import bill
card("s15_c3", "m3_card", "The Import Bill", "Why India wants chip plants")
stage("s16_q3", "m3_question", {
    "zones": [Z("port")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 4,
    "items": [it("ship", type="cargo", x=[[0, 1700], [9, 1100]], at=0.2, scale=0.7),
              it("coins", **{"from": [700, 600], "to": [1700, 400]}, at=0.6, rate=5)],
    "callouts": [co("Why does India want chip plants at all?", 960, 150, C("Why does India"), "gold", screen=True, size=40)]})
stage("s17_bill", "m3_bill", {
    "zones": [Z("port")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("If that trend continued"), "x": 1700, "y": 520, "zoom": 0.85, "dur": 2.6}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=C("India spent"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "on imported chips", "offset": 0.5}, 150]], text="CHIP IMPORTS FY17-FY25"),
              it("coins", **{"from": [600, 640], "to": [2200, 500]}, at=C("India spent"), rate=7),
              it("ship", type="cargo", x=[[0, 2400], [30, 1300]], at=0.3, scale=0.7),
              it("chart", x=1700, y=420, w=560, h=320, at=C("If that trend continued"), dur=3, text="IMPORTS IF THE TREND CONTINUES", pts=[0.1, 0.18, 0.3, 0.5, 0.9], color="risk"),
              it("sign", x=1700, y=700, text="PROJECTION", sub="Government of India", at=C("That is a projection"), color="#FFF59D", size=32)],
    "callouts": [co("FY17-FY25: {{imports.display}} of chip imports", 960, 960, C("India spent"), "gold", screen=True, size=40, sub="PIB", until=C("If that trend continued", -0.3)),
                 co("2035, if the trend holds: {{imports.y2035_display}} a year", 960, 960, C("If that trend continued"), "risk", screen=True, size=38, sub="a projection")]},
    sources=["pib_sep26"])
stage("s18_demand", "m3_demand", {
    "zones": [Z("shop")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 540, "zoom": 0.85}, {"at": C("And every chip India buys"), "x": 1300, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("device", type="phone", x=600, y=F, at=C("phones")), it("racecar", x=[[0, 700], [18, 1400]], at=C("cars"), scale=0.5, color="orange"),
              it("device", type="server", x=1500, y=F, at=C("data centers")), it("device", type="tv", x=1800, y=F, at=C("factories")),
              it("counter", x=1300, y=220, at=C("will reach"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "will reach", "offset": 2}, 110]], text="INDIA'S CHIP DEMAND, FY2030 (PROJ.)"),
              it("coins", **{"from": [1300, 500], "to": [2700, 300]}, at=C("money that leaves"), rate=6)],
    "callouts": [co("Demand: {{imports.demand_spoken}} a year by 2030 (projection)", 960, 960, C("will reach"), "gold", screen=True, size=34, sub="PIB", until=C("And every chip India buys", -0.3)),
                 co("Every imported chip: money leaving", 960, 960, C("And every chip India buys"), "risk", screen=True, size=40)]},
    sources=["pib_sep26"])
stage("s19_phones", "m3_phones", {
    "zones": [Z("port", -1600, 1300), Z("carplant", 1300, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.0}, {"at": C("Then factories started"), "x": 1900, "y": 540, "zoom": 1.0, "dur": 2.6},
            {"at": C("Packaging chips is"), "x": 1500, "y": 540, "zoom": 0.8, "dur": 2.4}], "drift": 3,
    "items": [it("ship", type="cargo", x=[[0, 900], [12, 400]], at=0.2, scale=0.6),
              it("counter", x=700, y=220, at=C("A decade ago"), suffix="%", steps=[[0, 0], [{"cue": "A decade ago", "offset": 1.5}, 75], [{"cue": "By twenty twenty-five"}, 75], [{"cue": "By twenty twenty-five", "offset": 2}, 0]], text="PHONES IMPORTED"),
              it("conveyor", x0=1400, x1=2800, y=F - 40, at=C("Then factories started"), n=8, speed=120, goods="phone"),
              it("device", type="phone", x=2000, y=F - 200, at=C("almost every phone")),
              it("arrow", **{"from": [1500, 330], "to": [2300, 330]}, at=C("Packaging chips is"), text="SAME FIRST STEP", color="gold")],
    "callouts": [co("2014-15: 75% of phones imported", 960, 960, C("A decade ago"), "white", screen=True, size=40, sub="PIB", until=C("By twenty twenty-five", -0.3)),
                 co("2024-25: 0.02%", 960, 960, C("By twenty twenty-five"), "gold", screen=True, size=44, until=C("Packaging chips is", -0.3)),
                 co("Chips: the same first step", 960, 960, C("Packaging chips is"), "white", screen=True, size=40)]},
    sources=["pib_apr26"])
stage("s20_design", "m3_design", {
    "zones": [Z("sciencepark")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Remember the slices"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [*crowd([600, 720, 840, 960, 1080], "type", at=C("chip designers"), scale=0.7),
              it("letters", x=840, y=220, text="≈ 1 IN 5", at=C("chip designers", 0.4), size=90, color="gold"),
              it("tower", x=1600, text="DESIGN 50%", color="#1565C0", h=520, at=C("Design is the biggest"), scale=0.8),
              it("tower", x=1950, text="FAB ≈ 25%", color="#B0BEC5", h=[[0, 40], [{"cue": "The missing piece", "offset": 0.5}, 40], [{"cue": "The missing piece", "offset": 2}, 260]], at=C("The missing piece"), scale=0.8),
              it("tower", x=2300, text="PACKAGING 6%", color=SAFF, h=90, at=C("Packaging, the smallest"), scale=0.8),
              it("letters", x=1950, y=300, text="?", at=C("The missing piece", 0.6), size=120, color="risk")],
    "callouts": [co("≈ 20% of the world's chip designers work in India", 960, 960, C("chip designers"), "gold", screen=True, size=36, sub="PIB", until=C("Remember the slices", -0.3)),
                 co("Design ✓ · Packaging ✓ · The fab: missing", 960, 960, C("Packaging, the smallest"), "white", screen=True, size=40)]},
    sources=["pib_sep26", "bcg_sia"])
kinetic("s21_t3", "m3_transition", [("And the fab", 72, "And the fab", None, False), ("is where things get harder", 60, "things get harder", "risk", False)])

# ====================================================================== PART 4: the missing middle
card("s22_c4", "m4_card", "The Missing Middle", "India's first real fab")
stage("s23_q4", "m4_question", {
    "zones": [Z("site")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("crane", x=960, text="DHOLERA", at=0.3, progress=[[0, 0.2], [9, 0.5]], scale=0.9)],
    "callouts": [co("How close is India to the chip itself?", 960, 150, C("How close"), "gold", screen=True, size=42)]})
stage("s24_dholera", "m4_dholera", {
    "zones": [Z("site")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("It is worth about"), "x": 1500, "y": 540, "zoom": 0.9, "dur": 2.4},
            {"at": C("When construction began"), "x": 2200, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("crane", x=900, text="TATA · DHOLERA FAB", at=0.3, progress=[[0, 0.3], [25, 0.6]], scale=0.9),
              it("sign", x=900, y=250, text="WITH PSMC (TAIWAN)", at=C("technology from"), color="#BBDEFB", size=32),
              it("counter", x=1600, y=220, at=C("It is worth about"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "It is worth about", "offset": 1.5}, 11]], text="DHOLERA FAB (≈)"),
              it("counter", x=1600, y=480, at=C("designed for"), suffix=" / mo", steps=[[0, 0], [{"cue": "designed for", "offset": 1.5}, 50000]], text="WAFER STARTS (PLAN)"),
              it("calendar", x=2300, y=320, at=C("When construction began"), pages=[[0, "2024", "GROUNDBREAKING"], [{"cue": "the first chip would arrive"}, "DEC 2026", "28 nm PROMISED"]], scale=0.85)],
    "callouts": [co("India's first real fab: ≈ {{dholera.display}}, {{dholera.wspm_display}} wafers", 960, 960, C("It is worth about"), "gold", screen=True, size=36, sub="PIB; converted at the Fed H.10 rate", until=C("When construction began", -0.3)),
                 co("2024 promise: first chip Dec 2026, 28 nm", 960, 960, C("When construction began"), "white", screen=True, size=40, sub="IT minister (via Tech Times)")]},
    sources=["pib_apr26", "tt_dholera", "fred_inr"])
stage("s25_slip", "m4_slip", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1200, "y": 540, "zoom": 0.9}, {"at": C("A new fab has to learn"), "x": 1200, "y": 560, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=700, y=320, at=0.2, pages=[[0, "DEC 2026", "28 nm"], [{"cue": "ninety nanometer"}, "DEC 2026", "90 nm"], [{"cue": "mid twenty twenty-eight"}, "MID 2028", "90 nm"]], scale=0.9),
              it("crane", x=1500, text="DHOLERA", at=0, progress=[[0, 0.45], [20, 0.6]], scale=0.8),
              it("wafer", x=1700, y=460, r=130, at=C("A new fab has to learn"), spin=6, revealAt=C("good chips"), fail=0.45)],
    "callouts": [co("Now: 90 nm first, commercial output mid-2028 (target)", 960, 960, C("That has changed"), "risk", screen=True, size=36, sub="Tech Times", until=C("Tata and PSMC say", -0.3)),
                 co("Tata/PSMC: starting mature is normal", 960, 960, C("Tata and PSMC say"), "white", screen=True, size=40, until=C("A new fab has to learn", -0.3)),
                 co("First good chips, then small ones", 960, 960, C("A new fab has to learn"), "gold", screen=True, size=40)]},
    sources=["tt_dholera"])
stage("s26_loan", "m4_loan", {
    "zones": [Z("exchange", -1600, 1500), Z("site", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("the land pledged"), "x": 2100, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("vaultdoor", x=700, at=0.2, openAt=C("borrowed"), scale=0.7),
              it("coins", **{"from": [700, 500], "to": [2100, 500]}, at=C("borrowed", 0.5), rate=5, until=C("the land pledged", 2)),
              it("counter", x=1300, y=220, at=C("borrowed"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "borrowed", "offset": 1.5}, 735]], text="BANK LOAN, FEB 2026"),
              it("pricetag", x=2100, y=320, at=C("the land pledged"), pages=[[0, "$0", True]], sub="land value as collateral"),
              it("sign", x=2100, y=600, text="TATA", sub="the banks bet on the name", at=C("betting on the Tata name"), color="#C5CAE9", size=44)],
    "callouts": [co("Loan: {{loan.display}} from international banks", 960, 960, C("borrowed"), "gold", screen=True, size=40, sub="Tech Times", until=C("the land pledged", -0.3)),
                 co("Collateral land valued at zero", 960, 960, C("the land pledged"), "risk", screen=True, size=40)]},
    sources=["tt_dholera"])
stage("s27_rivals", "m4_rivals", {
    "zones": [Z("fab", -1600, 1600, night=True, label="red"), Z("port", 1600, 6000)], "worldW": 3200, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.0}, {"at": C("And India carries"), "x": 2300, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [*[it("litho", x=400 + k * 230, at=C("Chinese foundries", 0.2 * k), fireAt=C("Chinese foundries", 0.2 * k + 0.3), text="MATURE", scale=0.3, color="#C62828") for k in range(5)],
              it("counter", x=760, y=200, at=C("Nexchip"), suffix=" / mo", steps=[[0, 0], [{"cue": "Nexchip", "offset": 2}, 100000]], text="NEXCHIP RAMP (WAFERS)"),
              it("calendar", x=1950, y=300, at=C("In twenty oh five"), pages=[[0, "2005", "SEMINDIA"]], scale=0.8),
              it("ship", type="cargo", x=2400, at=C("stuck at Indian ports", -0.5), scale=0.7),
              it("barrier", x=2850, text="CUSTOMS", at=C("stuck at Indian ports"), closeAt=C("waiting for customs")),
              it("clock", x=2400, y=250, at=C("waiting for customs"), period=1.6, text="WAITING")],
    "callouts": [co("Chinese mature-chip capacity, state subsidised", 960, 960, C("Chinese foundries"), "risk", screen=True, size=38, sub="Tech Times", until=C("And India carries", -0.3)),
                 co("2005: a $3bn project, equipment stuck at the ports", 960, 960, C("And India carries"), "white", screen=True, size=36, sub="SemIndia (Tech Times)")]},
    sources=["tt_dholera", "tt_sites"])
add("p28_harder", "m4_draw", "engine_draw", {
    "title": "Why a fab is so much harder", "board": BOARD, "draw_start": C("A packaging plant needs"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 330, 400, 260), "color": "accent3", "width": 5, "start": C("A packaging plant needs"), "label": lbl("PACKAGING PLANT", 760, 370, 26, "accent3")},
        {"d": "M 590 430 L 930 430", "color": "accent3", "width": 3, "start": C("many companies sell"), "label": lbl("machines: many sellers", 760, 470, 22, "accent3")},
        {"d": "M 590 520 L 930 520", "color": "accent3", "width": 3, "start": C("ordinary purity"), "label": lbl("materials: ordinary purity", 760, 560, 22, "accent3")},
        {"d": rect(1040, 330, 440, 380), "color": "risk", "width": 6, "start": C("A fab needs"), "label": lbl("FAB", 1260, 370, 30, "risk")},
        {"d": "M 1070 430 L 1450 430", "color": "risk", "width": 3, "start": C("lithography machines"), "label": lbl("lithography: 1-2 suppliers", 1260, 470, 22, "risk")},
        {"d": "M 1070 520 L 1450 520", "color": "risk", "width": 3, "start": C("parts per trillion"), "label": lbl("purity: parts per trillion", 1260, 560, 22, "risk")},
        {"d": "M 1070 610 L 1450 610", "color": "risk", "width": 3, "start": C("engineers who have done it"), "label": lbl("experienced engineers", 1260, 650, 22, "risk")},
        {"d": arrow((1260, 720), (1260, 820)), "color": "accent", "width": 5, "start": C("Every one of those"), "label": lbl("ALL IMPORTED", 1260, 860, 28, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Every one of those", 0.3), "dur": 1.4, "target": [1260, 820]}],
    "scale": 0.86, "floor": 1040}, sources=["tt_sites"])
kinetic("s29_t4", "m4_transition", [("India knows this", 66, "India knows", None, False), ("Its next move targets exactly that list", 50, "Its next move", "accent", True)])

# ====================================================================== PART 5: the second step
card("s30_c5", "m5_card", "The Second Step", "After packaging")
stage("s31_q5", "m5_question", {
    "zones": [Z("parliament")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=960, y=560, at=0.3, text="SEMICON 2.0", scale=0.8)],
    "callouts": [co("What comes after packaging?", 960, 150, C("What comes after"), "gold", screen=True, size=44)]})
stage("s32_semicon2", "m5_semicon2", {
    "zones": [Z("parliament", -1600, 1500), Z("fab", 1500, 6000, label="yellow")], "worldW": 3000,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("For the first time"), "x": 2100, "y": 540, "zoom": 0.95, "dur": 2.4},
            {"at": C("Because, as one consultant"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "JUL", "2026"]], scale=0.8),
              it("counter", x=900, y=220, at=C("a second chip program"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "a second chip program", "offset": 1.5}, 13]], text="SEMICON 2.0 (≈)"),
              it("litho", x=1800, at=C("the machines"), fireAt=C("the machines", 0.3), text="MACHINES", scale=0.4),
              it("sign", x=2200, y=420, text="CHEMICALS", at=C("the special chemicals"), color="#E1BEE7", size=34),
              it("sign", x=2550, y=420, text="GASES", at=C("the gases"), color="#B3E5FC", size=34),
              it("letters", x=2200, y=220, text="30%", at=C("with an incentive"), size=110, color="gold"),
              it("ship", type="cargo", x=[[0, 3200], [20, 2200]], at=C("still be imported"), scale=0.6)],
    "callouts": [co("Semicon 2.0: ≈ {{semicon2.display}}, July 2026", 960, 960, C("a second chip program"), "gold", screen=True, size=40, sub="PIB; converted at the Fed H.10 rate", until=C("For the first time", -0.3)),
                 co("{{semicon2.inc_display}} for makers of machines, chemicals, gases", 960, 960, C("For the first time"), "white", screen=True, size=38, until=C("Because, as one consultant", -0.3)),
                 co("Kearney: most critical inputs still imported", 960, 960, C("Because, as one consultant"), "risk", screen=True, size=38, sub="Tech Times")]},
    sources=["pib_sep26", "tt_sites", "fred_inr"])
stage("s33_people", "m5_people", {
    "zones": [Z("fab", -1600, 1300, label="yellow"), Z("sciencepark", 1300, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.0}, {"at": C("And it pays for people"), "x": 1900, "y": 540, "zoom": 0.95, "dur": 2.4},
            {"at": C("Because a fab is not"), "x": 1500, "y": 540, "zoom": 0.8, "dur": 2.4}], "drift": 3,
    "items": [it("litho", x=700, at=0.2, fireAt=0.5, text="NEW FAB", scale=0.6, color=TATA),
              it("letters", x=700, y=170, text="UP TO 40%", at=C("covering up to"), size=70, color="gold"),
              *crowd([1500, 1640, 1780, 1920, 2060, 2200, 2340, 2480], "read", at=C("And it pays for people", 0.5), scale=0.62),
              it("counter", x=2000, y=220, at=C("Lam Research"), steps=[[0, 0], [{"cue": "Lam Research", "offset": 2}, 60000]], text="FAB ENGINEERS TO TRAIN (PLAN)")],
    "callouts": [co("Up to {{pillars.display}} of a new silicon fab's cost", 960, 960, C("covering up to"), "gold", screen=True, size=38, sub="Tech Times", until=C("And it pays for people", -0.3)),
                 co("300+ universities · 60,000 fab engineers planned", 960, 960, C("And it pays for people"), "white", screen=True, size=36, until=C("Because a fab is not", -0.3)),
                 co("A fab is people who know how to run it", 960, 960, C("Because a fab is not"), "gold", screen=True, size=40)]},
    sources=["tt_sites", "pib_may26"])
stage("s34_trust", "m5_trust", {
    "zones": [Z("port")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("India's real argument"), "x": 1700, "y": 540, "zoom": 0.9, "dur": 2.6}], "drift": 3,
    "items": [it("pricetag", x=700, y=300, at=C("Chinese mature chips"), pages=[[0, "CHEAP"]], sub="subsidized mature chips"),
              it("ship", type="cargo", x=[[0, 1200], [25, 2400]], at=C("India's real argument"), scale=0.7),
              it("letters", x=1900, y=220, text="TRUST", at=C("India's real argument", 0.4), size=110, color="gold"),
              it("contract", x=2400, y=480, at=C("a second source"), text="SECOND SOURCE", sub="US · Europe · Japan buyers", scale=0.6)],
    "callouts": [co("Not price: trust", 960, 960, C("India's real argument"), "gold", screen=True, size=44, sub="Tech Times", until=C("That is a selling point", -0.3)),
                 co("A selling point no subsidy can buy", 960, 960, C("That is a selling point"), "white", screen=True, size=40)]},
    sources=["tt_dholera"])
add("p35_ladder", "m5_ladder", "engine_draw", {
    "title": "The ladder", "board": BOARD, "draw_start": C("Start where the door"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 700 860 L 860 340 M 1000 860 L 1160 340", "color": "ink", "width": 6, "start": C("That is the logic")},
        {"d": "M 690 800 L 990 800", "color": "accent3", "width": 7, "start": C("Start where the door"), "label": lbl("1 · PACKAGING + TEST ✓", 1180, 805, 22, "accent3", "start")},
        {"d": "M 730 680 L 1030 680", "color": "accent3", "width": 7, "start": C("Learn to run clean"), "label": lbl("2 · PEOPLE, SUPPLIERS", 1210, 685, 22, "accent3", "start")},
        {"d": "M 770 560 L 1070 560", "color": "accent", "width": 7, "start": C("Then move up to a fab"), "label": lbl("3 · FAB, OLDER CHIPS (2028?)", 1250, 565, 22, "accent", "start")},
        {"d": "M 810 440 L 1110 440", "color": "risk", "width": 7, "start": C("the leading edge"), "label": lbl("4 · LEADING EDGE (maybe)", 1290, 445, 22, "risk", "start")},
        {"d": dot(840, 760), "color": "accent2", "width": 1, "start": C("Each step is smaller"), "label": lbl("INDIA TODAY", 600, 770, 22, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("Each step is smaller", 0.3), "dur": 1.4, "target": [840, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["pib_sep26", "tt_dholera"])

# ====================================================================== PAYOFF
stage("s36_payoff", "payoff", {
    "zones": [Z("site", -1600, 1500), Z("fab", 1500, 6000, label="yellow")], "worldW": 3000,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 0.95}, {"at": C("The real test"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.6},
            {"at": C("Until then"), "x": 2200, "y": 560, "zoom": 1.0, "dur": 2.6}], "drift": 2,
    "items": [it("crane", x=900, text="DHOLERA · 2028?", at=0.3, progress=[[0, 0.5], [30, 0.8]], scale=0.85),
              it("calendar", x=1450, y=300, at=C("The real test"), pages=[[0, "2028", "THE REAL TEST"]], scale=0.8),
              it("osat", x=2300, at=C("Until then", -0.4), rate=1.2, text="FINISH FIRST, THEN START", scale=0.6)],
    "callouts": [co("Not a failure: the first rung of the ladder", 960, 150, C("No. They are the first rung"), "gold", screen=True, size=40, until=C("The real test", -0.3)),
                 co("The real test: Dholera, 2028 (target)", 960, 150, C("The real test"), "white", screen=True, size=40, until=C("Until then", -0.3)),
                 co("Finish what others started, then learn to start", 960, 150, C("Until then"), "gold", screen=True, size=38)]},
    sources=["tt_dholera", "bcg_sia"])
add("s37_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_india_chips_storyboard.py; edit the generator, not this file.\n"
           "# Episode 17 storyboard (chip series C4): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
