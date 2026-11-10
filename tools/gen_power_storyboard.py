"""Generates projects/why-americas-electricity-bills-are-rising/deliverables/documentary/storyboard.yaml (Episode 35,
US batch #08: Why America's Electricity Bills Are Rising).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: a big auction chart and a spinning home meter (new `meter` item).
- Part 1 (the bill): the suburb at night, the meter, state price charts.
- Part 2 (the wires): high-voltage country (new `powergrid` set), spending charts.
- Part 3 (the fuel paradox): a gas hub at dusk (tankfarm set), price screens.
- Part 4 (the data center rush): the data-center campus (datacenter set, isodc item), PJM auction charts, an evidence board.
- Part 5 (the utility deal): the state commission (parliament), the rate-base balance.
No real logos of utilities; names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_power_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-americas-electricity-bills-are-rising/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


def meter(x=960, y=420, **kw):
    return it("meter", x=x, y=y, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.15}, {"at": 1.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [chart([{"label": "2024/25", "value": 28.92, "color": "#90A4AE", "at": 0.05, "display": "$28.92"},
                     {"label": "2025/26", "value": 269.92, "color": "#E53935", "at": C("Then two hundred"), "display": "$269.92"}],
                    at=0.05, max=300, dark=True, title="PJM CAPACITY PRICE, $ PER MW-DAY (PJM AUCTION REPORTS)", x=360, w=880),
              meter(1560, 420, at=0.4, scale=0.9, spin=[[0, 1], [{"cue": "jumped"}, 6]], text="$$$")]},
    sources=["pjm"])
stage("s02_twist", "h_twist", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("It flows"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("letters", x=1000, y=170, text="× 9+ (OUR CALCULATION)", at=0.2, size=84, color="risk"),
              it("home", x=900, at=0.3, scale=0.6, night=True),
              it("home", x=1500, at=0.5, scale=0.6, night=True, color="#E3F2FD", roof="#5C6BC0"),
              it("letters", x=1250, y=330, text="→ INTO YOUR BILL", at=C("It flows"), size=56, color="gold")]},
    sources=["pjm"])
stage("s03_question", "h_question", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.15}, {"at": 0.8, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [meter(960, 400, at=0.1, scale=1.1, spin=3, text="$ ? ? ?"),
              it("letters", x=960, y=900, text="WHY IS THE LIGHT BILL RISING?", at=0.4, size=64, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE WIRES", at=0.3, color="#BBDEFB", size=44),
              it("sign", x=750, y=380, text="2 · THE FUEL", at=C("the fuel"), color="#FFE0B2", size=44),
              it("sign", x=1170, y=380, text="3 · DATA CENTERS", at=C("the data"), color="#FFCDD2", size=44),
              it("sign", x=1590, y=380, text="4 · THE PROFIT", at=C("allowed to earn"), color="#C8E6C9", size=44),
              it("letters", x=960, y=700, text="FOUR FORCES", at=C("the four forces"), size=72, color="gold")]})

# ====================================================================== PART 1: the bill (suburb night + meter + charts)
card("s05_c1", "m1_card", "The Bill", "Price per kilowatt hour")
stage("s06_price", "m1_price", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So far in twenty twenty-six"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [meter(700, 380, at=0.2, scale=0.8, steps=[[0, 12.65], [{"cue": "So far in twenty twenty-six"}, 12.65], [{"cue": "based on preliminary"}, 18.19]], prefix="", suffix="¢", decimals=2, label="PER kWh"),
              it("home", x=1500, at=0.3, scale=0.65, night=True),
              it("letters", x=1400, y=170, text="2015: 12.65¢ → 2026: 18.19¢ (EIA)", at=C("So far in twenty twenty-six"), size=44, color="gold"),
              it("letters", x=1400, y=260, text="≈ +36% IN 10 YEARS (TO 2025)", at=C("rose about thirty-six"), size=40, color="white")]},
    sources=["epa", "epm"])
stage("s07_cpi", "m1_cpi", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "ELECTRICITY", "value": 34.8, "color": "#FFB300", "at": C("for electricity rose"), "display": "+34.8%"},
                     {"label": "ALL PRICES", "value": 22.8, "color": "#90A4AE", "at": C("Prices in general"), "display": "+22.8%"}],
                    at=0.2, max=40, title="CPI, SEP 2021 → SEP 2026 (BLS; OUR CALCULATION)", x=520, w=880),
              it("letters", x=960, y=470, text="OUTRUNNING INFLATION", at=0.3, until=C("for electricity rose"), size=84, color="risk"),
              it("letters", x=960, y=990, text="EIA: FASTER THAN INFLATION SINCE 2022", at=C("EIA itself says"), size=42, color="risk")]},
    sources=["bls", "tie_infl"])
stage("s08_bill", "m1_bill", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("In the summer"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("home", x=800, at=0.2, scale=0.75, night=True, sign="$142", signHead="AVG BILL / MONTH"),
              meter(1550, 380, at=0.4, scale=0.7, spin=[[0, 1], [{"cue": "In the summer"}, 5]], text="863 kWh", label="2024 AVG / MONTH"),
              it("letters", x=1300, y=150, text="SUMMER: AIR CONDITIONING", at=C("In the summer"), size=46, color="gold")]},
    sources=["srp"])
stage("s09_states", "m1_states", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "HAWAII", "value": 46.41, "color": "#E53935", "at": 0.5, "display": "46.4¢"},
                     {"label": "CALIFORNIA", "value": 32.58, "color": "#FF7043", "at": C("and California"), "display": "32.6¢"},
                     {"label": "U.S. AVG", "value": 18.19, "color": "#FFB300", "at": C("and California", 0.5), "display": "18.2¢"},
                     {"label": "N. DAKOTA", "value": 12.46, "color": "#43A047", "at": C("In North Dakota"), "display": "12.5¢"}],
                    at=0.2, max=50, dark=True, title="RESIDENTIAL PRICE, JAN–AUG 2026 (EIA, PRELIMINARY)", x=300, w=1080),
              it("letters", x=1650, y=380, text="≈ 3.7×", at=C("three point seven times"), size=90, color="gold"),
              it("letters", x=1580, y=500, text="OHIO, VIRGINIA ≈ +13%", at=C("Ohio and Virginia"), size=32, color="risk")]},
    sources=["epm"])
add("p10_slices", "m1_draw", "engine_draw", {
    "title": "Inside one bill (schematic)", "board": BOARD, "draw_start": C("A slice for the power plants"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw what is inside")},
        {"d": "M 600 860 L 600 560 L 760 560 L 760 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("A slice for the power plants"), "label": lbl("POWER PLANTS", 680, 540, 20, "accent2")},
        {"d": "M 820 860 L 820 640 L 980 640 L 980 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("high-voltage lines"), "label": lbl("TRANSMISSION", 900, 620, 20, "accent")},
        {"d": "M 1040 860 L 1040 520 L 1200 520 L 1200 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("the local wires and poles"), "label": lbl("LOCAL WIRES", 1120, 500, 20, "risk")},
        {"d": "M 1260 860 L 1260 760 L 1420 760 L 1420 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("a slice of profit"), "label": lbl("PROFIT", 1340, 740, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("which slices are growing", 0.1), "dur": 1.4, "target": [1120, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["tie_grid"])
kinetic("s11_t1", "m1_transition", [("Not the power itself…", 64, "the fastest-growing part", None, True), ("…the wires", 84, "It is the wires", "gold", False)])

# ====================================================================== PART 2: the wires (powergrid set + spending charts)
card("s12_c2", "m2_card", "The Wires", "Twenty years of grid spending")
stage("s13_capex", "m2_capex", {
    "zones": [Z("powergrid")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Spending on long-distance"), "x": 1400, "y": 500, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=380, text="20 YEARS OF UTILITY SPENDING (EIA)", at=0.3, until=C("capital spending on local distribution"), size=54, color="white"),
              it("counter", x=1000, y=150, at=C("capital spending on local distribution"), prefix="+", suffix="%", steps=[[0, 0], [{"cue": "rose", "offset": 0.5}, 160]], text="LOCAL DISTRIBUTION CAPEX, 2003→2023 (EIA)", scale=1.1),
              it("letters", x=1000, y=380, text="≈ $51BN A YEAR", at=C("fifty-one billion"), size=50, color="gold"),
              it("letters", x=1650, y=230, text="TRANSMISSION ×3 → $28BN", at=C("nearly tripled"), size=46, color="white")]},
    sources=["tie_grid"])
stage("s14_gen", "m2_gen", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "MAKING POWER", "value": -24, "color": "#43A047", "at": 0.5, "display": "−24%"},
                     {"label": "LOCAL WIRES (CAPEX)", "value": 160, "color": "#E53935", "at": C("Delivering the power"), "display": "+160%"},
                     {"label": "TRANSMISSION", "value": 190, "color": "#FF7043", "at": C("Delivering the power", 0.6), "display": "≈ ×3"}],
                    at=0.2, max=200, min=-40, title="UTILITY SPENDING CHANGE, 2003→2023 (EIA, REAL $)", x=360, w=1200)]},
    sources=["tie_grid"])
stage("s15_why", "m2_why", {
    "zones": [Z("powergrid", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("In California"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="OLD GRID · STORMS · WILDFIRES", at=0.3, until=C("In California"), size=56, color="gold"),
              it("storm", x=700, y=260, at=C("Storms and wildfires"), scale=0.8),
              it("counter", x=1350, y=160, at=C("In California"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "approved for recovery", "offset": 0}, 40]], text="CALIFORNIA WILDFIRE COSTS RECOVERED, 2019–2024 (CPUC)"),
              it("letters", x=1350, y=380, text="PG&E 2024: ≈ 27% WILDFIRE-RELATED", at=C("about twenty-seven percent"), size=40, color="risk")]},
    sources=["cpuc"])
add("p16_spend", "m2_draw", "engine_draw", {
    "title": "Twenty years of spending (schematic)", "board": BOARD, "draw_start": C("Here is the money spent making"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Let me draw twenty years")},
        {"d": "M 580 600 L 1440 680", "color": "accent3", "width": 7, "start": C("Here is the money spent making"), "label": lbl("MAKING POWER −24%", 1300, 710, 20, "accent3")},
        {"d": "M 580 800 L 1440 620", "color": "accent", "width": 7, "start": C("almost tripling"), "label": lbl("TRANSMISSION ≈ ×3", 1300, 600, 20, "accent")},
        {"d": "M 580 760 L 1440 440", "color": "risk", "width": 8, "start": C("more than doubling"), "label": lbl("LOCAL WIRES +160%", 1300, 420, 20, "risk")},
        {"d": "M 1440 860 L 1440 440 L 1460 440 L 1460 860", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.2, "kind": "bar", "start": C("The bill follows the wires")},
    ],
    "actions": [{"kind": "point", "at": C("The bill follows the wires", 0.1), "dur": 1.4, "target": [1300, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["tie_grid"])
kinetic("s17_t2", "m2_transition", [("A second surprise:", 64, "But there is a second", None, False), ("the fuel got cheaper", 70, "actually got cheaper", "gold", False)])

# ====================================================================== PART 3: the fuel paradox (gas hub + screens)
card("s18_c3", "m3_card", "The Fuel Paradox", "Gas fell, bills rose")
stage("s19_gas", "m3_gas", {
    "zones": [Z("tankfarm", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="GAS SETS THE WHOLESALE PRICE MOST HOURS (EIA)", at=0.3, size=40, color="white"),
              it("tradescreen", x=1000, y=480, at=C("In twenty twenty-two"), scale=1.0, text="HENRY HUB GAS, $/MMBTU (EIA, ANNUAL)", decimals=2, max=7, min=0, hot=5, lamp=False,
                 price=[[0, 3.89], [{"cue": "the average Henry Hub"}, 6.45], [{"cue": "By twenty twenty-four"}, 6.45], [{"cue": "it had fallen"}, 2.19]])]},
    sources=["hh", "tie_demand"])
stage("s20_paradox", "m3_paradox", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "GAS 2022→2024", "value": -66, "color": "#43A047", "at": C("a drop of about two thirds"), "display": "−66%"},
                     {"label": "HOME POWER 2022→2024", "value": 9.6, "color": "#E53935", "at": C("It rose almost ten"), "display": "+9.6%"}],
                    at=0.2, max=20, min=-75, title="CHANGE, 2022→2024 (EIA; OUR CALCULATION)", x=520, w=880),
              it("letters", x=960, y=990, text="BILLS FOLLOW AVERAGE COSTS", at=C("Most customers pay"), size=44, color="gold")]},
    sources=["hh", "epa"])
stage("s21_back", "m3_back", {
    "zones": [Z("tankfarm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So households"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("pricetag", x=800, y=320, at=0.3, text="2024: $2.19", pages=[[{"cue": "to three dollars"}, "2025: $3.52", True]], scale=1.0),
              it("letters", x=1450, y=200, text="WIRES ↑ + FUEL ↑", at=C("both pressures"), size=64, color="risk")]},
    sources=["hh"])
add("p22_lines", "m3_draw", "engine_draw", {
    "title": "The paradox (schematic)", "board": BOARD, "draw_start": C("Here is the gas price"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Let me draw the paradox")},
        {"d": "M 580 700 L 800 420 L 1000 760 L 1200 740 L 1440 650", "color": "accent3", "width": 7, "start": C("Here is the gas price"), "label": lbl("GAS", 800, 400, 24, "accent3")},
        {"d": "M 580 760 L 800 700 L 1000 640 L 1200 580 L 1440 520", "color": "risk", "width": 8, "start": C("Here is your electricity price"), "label": lbl("YOUR POWER PRICE", 1300, 500, 22, "risk")},
        {"d": "M 1440 860 L 1440 520 L 1460 520 L 1460 860", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.2, "kind": "bar", "start": C("going their separate ways")},
    ],
    "actions": [{"kind": "point", "at": C("going their separate ways", 0.1), "dur": 1.4, "target": [1200, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["hh", "epa"])
kinetic("s23_t3", "m3_transition", [("A new customer arrives…", 64, "And now a new customer", None, True), ("…hungrier than any before", 60, "hungrier for power", "risk", False)])

# ====================================================================== PART 4: the data center rush (datacenter + PJM charts)
card("s24_c4", "m4_card", "The Data Center Rush", "AI, servers and the grid")
stage("s25_dc", "m4_dc", {
    "zones": [Z("datacenter")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("and could use"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("isodc", x=900, y=700, at=0.2, n=9, step=0.2, cols=3, scale=0.75, glow=True),
              it("counter", x=1450, y=180, at=C("they used about"), prefix="", suffix="%", decimals=1, steps=[[0, 0], [{"cue": "of all US electricity", "offset": 0}, 4.4]], text="DATA CENTERS' SHARE OF U.S. POWER, 2023 (DOE/LBNL)"),
              it("letters", x=1500, y=400, text="2028: 6.7–12%", at=C("and could use"), size=62, color="gold")]},
    sources=["doe"])
stage("s26_demand", "m4_demand", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2005–2019", "value": 0.1, "color": "#90A4AE", "at": 0.5, "display": "0.1%/yr"},
                     {"label": "2020–2025", "value": 1.7, "color": "#E53935", "at": C("Between twenty twenty and"), "display": "1.7%/yr"}],
                    at=0.2, max=2, dark=True, title="U.S. ELECTRICITY DEMAND GROWTH (EIA)", x=420, w=860),
              it("letters", x=1560, y=430, text="DRIVEN BY", at=C("data centers are driving"), size=50, color="white"),
              it("letters", x=1560, y=520, text="DATA CENTERS", at=C("data centers are driving", 0.3), size=60, color="gold")]},
    sources=["tie_demand"])
stage("s27_pjm", "m4_pjm", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="PJM PEAK: 162.6 GW (JUL 2, 2026)", at=C("PJM's demand peaked"), size=40, color="white"),
              chart([{"label": "2024/25", "value": 28.92, "color": "#90A4AE", "at": 0.5, "display": "$28.92"},
                     {"label": "2025/26", "value": 269.92, "color": "#FF7043", "at": C("per megawatt day to"), "display": "$269.92"},
                     {"label": "2026/27", "value": 329.17, "color": "#E53935", "at": C("hit the cap"), "display": "$329 (cap)"},
                     {"label": "2027/28", "value": 333.44, "color": "#B71C1C", "at": C("hit the cap", 0.5), "display": "$333 (cap)"}],
                    at=0.3, max=360, dark=True, title="PJM CAPACITY PRICE, $/MW-DAY", x=420, y=230, w=1080, h=520),
              it("letters", x=1000, y=900, text="ONE YEAR'S COST TO CUSTOMERS: ≈ $14.7BN", at=C("about fourteen point"), size=40, color="gold")]},
    sources=["pjm", "tie_demand"])
stage("s28_blame", "m4_blame", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("Its independent market monitor"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "\"FAR OUTSTRIP\"", "sub": "PJM: data center demand vs new supply", "at": 0.3, "w": 480, "color": "#FFF59D", "size": 48},
                {"x": 1550, "y": 380, "text": "≈ $29.4BN", "sub": "monitor's estimate, last 4 auctions", "at": C("about twenty-nine"), "w": 440, "color": "#FFCDD2", "size": 54},
                {"x": 1100, "y": 680, "text": "≈ 46%", "sub": "of capacity charges from data center load", "at": C("around forty-six"), "w": 460, "color": "#FFCDD2", "size": 60}],
              links=[[0, 1, C("about twenty-nine", 0.3)], [1, 2, C("around forty-six", 0.3)]],
              stamp="DATA CENTERS", stampAt=C("data center load"))]},
    sources=["pjm", "imm"])
add("p29_squeeze", "m4_draw", "engine_draw", {
    "title": "The squeeze (schematic)", "board": BOARD, "draw_start": C("Here is the supply"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Let me draw the squeeze")},
        {"d": "M 580 560 L 1440 500", "color": "accent2", "width": 7, "start": C("Here is the supply"), "label": lbl("SUPPLY", 1400, 480, 22, "accent2")},
        {"d": "M 580 760 L 1000 740 Q 1250 700 1440 520", "color": "risk", "width": 8, "start": C("Here is demand"), "label": lbl("DEMAND + DATA CENTERS", 1150, 780, 20, "risk")},
        {"d": "M 1380 860 L 1380 400 L 1430 400 L 1430 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("the price of being ready"), "label": lbl("PRICE ↑", 1405, 380, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("every household", 0.1), "dur": 1.4, "target": [1400, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["pjm"])
kinetic("s30_t4", "m4_transition", [("Who decides what you pay…", 60, "who decides", None, True), ("…and who profits?", 70, "who profits", "gold", False)])

# ====================================================================== PART 5: the utility deal (commission + balance)
card("s31_c5", "m5_card", "The Utility Deal", "Regulated returns")
stage("s32_model", "m5_model", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Texas rules"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.2, text="STATE COMMISSION", scale=0.7, stamp="RATE SET", stampAt=C("A state commission")),
              it("sign", x=1350, y=230, text="COST OF SERVICE =", at=C("The cost of service"), color="#FFFFFF", size=40),
              it("sign", x=1350, y=340, text="EXPENSES + RETURN ON CAPITAL", at=C("allowable expenses"), color="#C8E6C9", size=38),
              it("letters", x=1350, y=470, text="(TEXAS PUC RULE §25.231)", at=C("Texas rules"), size=32, color="white")]},
    sources=["puct"])
stage("s33_incentive", "m5_incentive", {
    "zones": [Z("powergrid")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Other things being equal"), "x": 1250, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("balance", x=1000, at=0.2, left="FUEL", lsub="no markup", right="WIRES", rsub="earn a return", tilt=0, to=10, balanceAt=C("they can earn a profit")),
              it("letters", x=1000, y=130, text="BIGGER RATE BASE → HIGHER INCOME (CPUC)", at=C("Other things being equal"), size=42, color="gold")]},
    sources=["cpuc"])
stage("s34_roe", "m5_roe", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=720, y=330, at=0.3, prefix="", suffix="%", decimals=2, steps=[[0, 0], [{"cue": "for twenty twenty-six", "offset": 1}, 9.98]], text="PG&E AUTHORIZED RETURN ON EQUITY, 2026 (CPUC)", scale=1.2),
              it("letters", x=1400, y=300, text="+ EVERY NEW MILE OF WIRE", at=C("Every new mile"), size=46, color="gold"),
              it("letters", x=1400, y=400, text="= BIGGER BASE", at=C("adds to the base"), size=56, color="white"),
              it("letters", x=1400, y=520, text="PAID FOR DECADES", at=C("for decades"), size=50, color="risk")]},
    sources=["cpuc"])
add("p35_all", "m5_draw", "engine_draw", {
    "title": "Why the bill keeps climbing", "board": BOARD, "draw_start": C("Old wires to replace"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(880, 640, 240, 110), "color": "ink", "width": 6, "kind": "box", "start": C("Let me put the whole bill"), "label": lbl("YOUR BILL", 1000, 703, 26, "ink")},
        {"d": rect(560, 380, 220, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Old wires to replace"), "label": lbl("WIRES", 670, 428, 22, "risk")},
        {"d": rect(860, 380, 220, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("Fuel that swings"), "label": lbl("FUEL", 970, 428, 22, "accent3")},
        {"d": rect(1160, 380, 260, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("Data centers bidding"), "label": lbl("DATA CENTERS", 1290, 428, 22, "accent2")},
        {"d": arrow((670, 470), (900, 630)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Each one is a reason")},
        {"d": arrow((970, 470), (990, 630)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Each one is a reason", 0.3)},
        {"d": arrow((1290, 470), (1100, 630)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Each one is a reason", 0.6)},
        {"d": "M 1180 860 L 1180 780 L 1260 780 L 1260 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("a business model"), "label": lbl("UTILITY RETURN", 1300, 760, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Together, they explain", 0.1), "dur": 1.4, "target": [1000, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["tie_grid", "hh", "pjm", "cpuc"])

# ====================================================================== PAYOFF
stage("s36_payoff", "payoff", {
    "zones": [Z("suburb", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The light switch"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("home", x=1000, at=0.2, scale=0.8, night=True),
              meter(1650, 380, at=0.4, scale=0.6, spin=2, text="$$$"),
              it("letters", x=1000, y=130, text="THE SYSTEM IS BEING REBUILT", at=C("the system that delivers"), size=54, color="gold"),
              it("letters", x=1000, y=230, text="SAME SWITCH · NEW ECONOMICS", at=C("The light switch"), size=44, color="white")]},
    sources=["tie_grid", "doe"])
add("s37_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_power_storyboard.py; edit the generator, not this file.\n"
           "# Episode 35 storyboard (US electricity bills): one visual language per part; tones from visual_direction.yaml.\n")
