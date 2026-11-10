"""Generates projects/the-hidden-business-behind-americas-grocery-prices/deliverables/documentary/storyboard.yaml
(Episode 40, US batch #20: The Hidden Business Behind America's Grocery Prices).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the farm field with a giant cents counter; the supermarket (new `supermarket` set) by day and after hours.
- Part 1 (the food dollar): USDA office, farm, highway trucks, the supermarket, a stacked food-dollar bar.
- Part 2 (the price shock): numbers, the egg carton (new `eggcarton` item) in the store and on the farm, the cattle ranch
  (new `ranch` set), a forecast chart.
- Part 3 (the penny business): the supermarket, an office, the warehouse with pallets.
- Part 4 (the profit debate): two charts (FTC vs FMI), Washington, shrinkflation in the aisle.
- Part 5 (fewer, bigger players): ranch and packing plant, the courtroom, the shelf at night.
No store or brand logos; names in text only. Lint: tools/lint_storyboard.py.  Run: python tools/gen_grocery_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-hidden-business-behind-americas-grocery-prices/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


def hbar(x0, x1, y, h, color, start, label, lx=None, up=False):
    return {"d": f"M {x0} {y} L {x1} {y} L {x1} {y + h} L {x0} {y + h} Z", "color": color, "width": 5, "fill": color, "fillOpacity": 0.3,
            "kind": "bar", "start": start, "label": lbl(label, lx if lx is not None else (x0 + x1) / 2, (y - 18) if up else (y + h + 34), 18, color)}


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("farm")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=260, at=0.05, prefix="", suffix="¢", decimals=1, steps=[[0.05, 0], [1.5, 11.8]], text="FARM SHARE OF EACH FOOD DOLLAR, 2024 (USDA)", scale=1.5),
              it("letters", x=1000, y=560, text="THE REST: 88.2¢", at=C("that is all that ends up"), size=56, color="gold")]},
    sources=["ersfd"])
stage("s02_twist", "h_twist", {
    "zones": [Z("supermarket", label="GROCERY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("So if the farmer"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=270, text="< 2¢ PROFIT PER $1 OF SALES", at=0.3, size=56, color="risk"),
              it("letters", x=1000, y=340, text="(KROGER, FY2024, OUR CALCULATION)", at=0.6, size=32, color="white"),
              it("sign", x=1050, y=440, text="FARM ≈ 12¢", at=C("the farmer gets a dime"), color="#C8E6C9", size=40),
              it("sign", x=1400, y=440, text="STORE ≈ 2¢", at=C("the store gets"), color="#FFE0B2", size=40),
              it("letters", x=1750, y=440, text="THE REST?", at=C("where does the rest"), size=60, color="gold")]},
    sources=["kroger", "ersfd"])
stage("s03_question", "h_question", {
    "zones": [Z("supermarket", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [*crowd([700, 800, 1200, 1300], "walk", at=0.1, scale=0.6),
              it("letters", x=1000, y=200, text="WHY DID THE BILL JUMP?", at=0.3, size=70, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · WHO TAKES EACH SLICE", at=C("who takes each slice"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · WHY PRICES SPIKED", at=C("why prices spiked"), color="#FFE0B2", size=32),
              it("sign", x=1560, y=380, text="3 · WHO PROFITED?", at=C("who profited"), color="#C8E6C9", size=32),
              it("letters", x=960, y=700, text="FOLLOW THE FOOD DOLLAR", at=0.4, size=68, color="gold")]})

# ====================================================================== PART 1: the food dollar
card("s05_c1", "m1_card", "The Food Dollar", "Who earns each cent")
stage("s06_dollar", "m1_dollar", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It counts both"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="USDA FOOD DOLLAR SERIES", scale=0.7, stamp="$1 SPLIT", stampAt=C("splits it into pieces")),
              it("letters", x=1300, y=200, text="GROCERIES + RESTAURANT MEALS", at=C("It counts both"), size=46, color="gold"),
              it("letters", x=1300, y=300, text="WHO EARNED EACH CENT?", at=C("Who earned each cent"), size=52, color="white")]},
    sources=["ersfd"])
stage("s07_farm", "m1_farm", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The other eighty-eight"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("pricetag", x=800, y=320, at=C("the farm share"), text="FARM: 11.8¢", scale=1.0),
              it("letters", x=1000, y=150, text="2024 (USDA ERS)", at=0.3, size=48, color="gold"),
              it("letters", x=1500, y=420, text="88.2¢ AFTER THE FARM GATE", at=C("The other eighty-eight"), size=46, color="white")]},
    sources=["ersfd"])
stage("s08_chain", "m1_chain", {
    "zones": [Z("highway")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Transportation and storage"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 3,
    "items": [it("letters", x=1000, y=220, text="AFTER THE FARM GATE", at=0.3, until=C("Food processing"), size=56, color="gold"),
              it("sign", x=600, y=220, text="PROCESSING 16.1¢", at=C("Food processing"), color="#FFE0B2", size=32),
              it("sign", x=1060, y=220, text="WHOLESALE 6.3¢", at=C("Wholesalers"), color="#BBDEFB", size=32),
              it("sign", x=1560, y=220, text="TRUCKS & STORAGE 4.1¢", at=C("Transportation and storage"), color="#C8E6C9", size=32),
              it("sign", x=1300, y=380, text="ENERGY 3.1¢", at=C("Energy,"), color="#FFF59D", size=34),
              it("sign", x=1780, y=380, text="ADS 2.2¢", at=C("Advertising,"), color="#FFCDD2", size=34)]},
    sources=["ersfd"])
stage("s09_store", "m1_store", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And the biggest slice"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=300, text="THE LAST STEPS", at=0.3, until=C("Grocery stores and other"), size=56, color="gold"),
              it("sign", x=850, y=280, text="GROCERY STORES 13.8¢", at=C("Grocery stores and other"), color="#FFE0B2", size=38),
              it("sign", x=1500, y=280, text="RESTAURANTS 38.6¢", at=C("And the biggest slice"), color="#FFCDD2", size=40),
              it("letters", x=1250, y=360, text="MOST OF IT IS NOT THE FOOD", at=C("Much of what we pay"), size=50, color="gold")]},
    sources=["ersfd"])
add("p10_dollar", "m1_draw", "engine_draw", {
    "title": "Your food dollar, 2024 (USDA ERS)", "board": BOARD, "draw_start": C("Here is one dollar"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 880, 120), "color": "ink", "width": 5, "kind": "box", "start": C("Here is one dollar"), "label": lbl("$1.00", 1000, 640, 30, "ink")},
        hbar(560, 664, 420, 120, "accent3", C("The farm gets a thin slice"), "FARM 12¢", 612),
        hbar(664, 806, 420, 120, "accent", C("Then processing"), "PROCESS 16¢", 735, up=True),
        hbar(806, 896, 420, 120, "accent2", C("Then wholesale and trucks"), "MOVE 10¢", 851),
        hbar(896, 1017, 420, 120, "muted", C("Then the grocery store"), "STORE 14¢", 956, up=True),
        hbar(1017, 1357, 420, 120, "risk", C("And the biggest piece"), "RESTAURANTS 39¢", 1187),
    ],
    "actions": [{"kind": "point", "at": C("Most of the", 0.1), "dur": 1.4, "target": [1100, 480]}],
    "scale": 0.86, "floor": 1040}, sources=["ersfd"])
kinetic("s11_t1", "m1_transition", [("The slices barely move…", 64, "fairly stable", None, False),
                                    ("…the price of the whole dollar does", 60, "The price of the whole dollar", "gold", False)])

# ====================================================================== PART 2: the price shock
card("s12_c2", "m2_card", "The Price Shock", "Eggs, beef and the whole bill")
stage("s13_cpi", "m2_cpi", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=960, y=300, at=0.3, prefix="+", suffix="%", steps=[[0, 0], [{"cue": "since January twenty twenty"}, 32]], text="GROCERY PRICES SINCE JAN 2020 (OUR CALCULATION, BLS)", scale=1.3),
              it("letters", x=960, y=640, text="2022: ALL FOOD +9.9% (USDA)", at=C("twenty twenty-two was the worst"), size=56, color="gold")]},
    sources=["blscpi", "ersfpo"])
stage("s14_eggs", "m2_eggs", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The main reason"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("eggcarton", x=900, y=380, at=0.3, scale=0.8, price="$1.46", pages=[[{"cue": "the average price hit"}, "$6.23"]]),
              it("letters", x=900, y=120, text="JAN 2020 → MARCH 2025", at=C("In March twenty"), size=50, color="gold"),
              it("sign", x=1550, y=330, text="BIRD FLU, SINCE 2022 (USDA)", at=C("of bird flu"), color="#FFCDD2", size=36)]},
    sources=["blscpi", "ersfpo"])
stage("s15_eggsdown", "m2_eggsdown", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Department of Agriculture expects"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("eggcarton", x=900, y=430, at=0.2, scale=0.9, price="$6.23", pages=[[{"cue": "By September"}, "$2.27"]], text="SEPT 2026"),
              it("letters", x=900, y=170, text="SUPPLY CAME BACK", at=0.3, size=56, color="gold"),
              it("letters", x=1550, y=330, text="2026 FORECAST: −29.3% (USDA)", at=C("expects egg prices"), size=40, color="white")]},
    sources=["blscpi", "ersfpo"])
stage("s16_beef", "m2_beef", {
    "zones": [Z("ranch")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And beef prices"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("pricetag", x=900, y=300, at=C("A pound of ground beef"), text="$3.89 / LB", pages=[[{"cue": "In August twenty"}, "$6.92 / LB", True]], scale=1.0),
              it("letters", x=900, y=150, text="GROUND BEEF (BLS AVERAGE PRICE)", at=0.3, size=44, color="gold"),
              it("letters", x=1600, y=330, text="2026 FORECAST: +8.7% (USDA)", at=C("forecast to rise"), size=42, color="white")]},
    sources=["blscpi", "ersfpo"])
stage("s17_now", "m2_now", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "12 MONTHS TO SEP 2026", "value": 1.8, "color": "#4FC3F7", "at": C("grocery prices rose"), "display": "1.8%"},
                     {"label": "2026 FORECAST", "value": 2.3, "color": "#FFB300", "at": C("The forecast for this year"), "display": "2.3%"},
                     {"label": "AVERAGE 2006–2025", "value": 2.6, "color": "#90A4AE", "at": C("the long-run average"), "display": "2.6%"}],
                    at=0.2, max=3.2, title="FOOD-AT-HOME PRICE CHANGE (BLS, USDA ERS)", x=300, w=1000),
              it("letters", x=1580, y=420, text="THE HIGHER LEVEL STAYS", at=C("slower growth"), size=40, color="risk")]},
    sources=["blscpi", "ersfpo"])
add("p18_shapes", "m2_draw", "engine_draw", {
    "title": "Three shapes of a price rise (illustration)", "board": BOARD, "draw_start": C("Eggs went up like a rocket"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 540 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw the two kinds")},
        {"d": "M 560 800 L 640 780 L 700 400 L 760 760 L 820 780", "color": "accent", "width": 6, "start": C("Eggs went up like a rocket"), "label": lbl("EGGS", 700, 370, 24, "accent")},
        {"d": "M 900 800 L 960 800 L 960 740 L 1020 740 L 1020 680 L 1080 680 L 1080 620 L 1140 620", "color": "risk", "width": 6, "start": C("Beef climbed like a staircase"), "label": lbl("BEEF", 1080, 590, 24, "risk")},
        {"d": "M 1200 800 L 1320 640 L 1440 620", "color": "accent2", "width": 6, "start": C("the whole grocery bill moved like a ramp"), "label": lbl("THE BILL", 1360, 600, 22, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("never went back down", 0.1), "dur": 1.4, "target": [1380, 630]}],
    "scale": 0.86, "floor": 1040}, sources=["blscpi"])
kinetic("s19_t2", "m2_transition", [("Many shoppers blamed the stores…", 62, "many shoppers blamed", None, False),
                                    ("…so how does a supermarket make money?", 58, "how a supermarket", "gold", False)])

# ====================================================================== PART 3: the penny business
card("s20_c3", "m3_card", "The Penny Business", "Thin margins, huge volume")
stage("s21_kroger", "m3_kroger", {
    "zones": [Z("supermarket", label="SUPERMARKET")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("By our calculation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=330, text="ONE OF AMERICA'S BIGGEST CHAINS", at=0.3, until=C("it sold"), size=50, color="gold"),
              it("counter", x=800, y=330, at=C("it sold"), prefix="$", suffix="BN", steps=[[0, 0], [{"cue": "of goods"}, 147]], text="KROGER SALES, FY2024 (10-K)"),
              it("counter", x=1400, y=330, at=C("By our calculation"), prefix="≈ ", suffix="¢", decimals=1, steps=[[0, 0], [{"cue": "on every dollar"}, 1.8]], text="NET PROFIT PER $1 (OUR CALCULATION)"),
              it("letters", x=1400, y=520, text="NEXT YEAR: < 1¢ (WRITE-DOWN)", at=C("The next year"), size=40, color="risk")]},
    sources=["kroger"])
stage("s22_others", "m3_others", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The industry's"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=300, text="AND THE OTHERS?", at=0.3, until=C("Albertsons"), size=56, color="gold"),
              it("sign", x=850, y=300, text="ALBERTSONS FY2024: 1.2%", at=C("Albertsons"), color="#BBDEFB", size=40),
              it("sign", x=1500, y=300, text="FMI AVERAGE, 2025: 2.1%", at=C("The industry's"), color="#FFE0B2", size=40),
              it("letters", x=1250, y=470, text="THIN, EVEN FOR RETAIL", at=C("Those are thin"), size=52, color="gold")]},
    sources=["aci", "fmi"])
stage("s23_volume", "m3_volume", {
    "zones": [Z("warehouse")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Walmart's American stores"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="VOLUME + SPEED", at=C("Volume and speed"), size=64, color="gold"),
              it("pallet", x=[[0, 300], [6, 900]], at=0.3, rows=3, scale=0.8),
              it("counter", x=1400, y=330, at=C("Walmart's American stores"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "of groceries"}, 285.5]], text="WALMART U.S. GROCERY SALES, FY2026 (10-K)")]},
    sources=["wmt"])
add("p24_grocer", "m3_draw", "engine_draw", {
    "title": "A grocer's dollar (illustration; profit from the 10-Ks)", "board": BOARD, "draw_start": C("Most of it pays for the products"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 860 L 1240 860", "color": "ink", "width": 4, "start": C("Let me draw a grocer's dollar")},
        {"d": "M 860 860 L 860 540 L 1140 540 L 1140 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.25, "kind": "bar", "start": C("Most of it pays for the products"), "label": lbl("PRODUCTS", 1000, 710, 26, "accent2")},
        {"d": "M 860 540 L 860 360 L 1140 360 L 1140 540", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Then wages"), "label": lbl("WAGES · RENT · POWER", 1000, 440, 20, "accent")},
        {"d": "M 860 360 L 860 350 L 1140 350 L 1140 360", "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.6, "kind": "bar", "start": C("the profit, is a sliver"), "label": lbl("PROFIT ≈ 2¢", 1290, 360, 24, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("About two cents", 0.1), "dur": 1.4, "target": [1140, 355]}],
    "scale": 0.86, "floor": 1040}, sources=["kroger", "fmi"])
kinetic("s25_t3", "m3_transition", [("That is the industry's side…", 62, "That is the industry's side", None, False),
                                    ("…the government saw something different", 60, "saw something", "gold", False)])

# ====================================================================== PART 4: the profit debate
card("s26_c4", "m4_card", "The Profit Debate", "Two rulers, the same years")
stage("s27_ftc", "m4_ftc", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2015 (PEAK)", "value": 5.6, "color": "#90A4AE", "at": C("their last peak"), "display": "5.6%"},
                     {"label": "2021", "value": 6.1, "color": "#4FC3F7", "at": C("rose to"), "display": "> 6%"},
                     {"label": "2023 (Q1–Q3)", "value": 7.0, "color": "#E53935", "at": C("they reached"), "display": "7%"}],
                    at=0.2, max=8, dark=True, title="RETAILER REVENUE OVER TOTAL COSTS (FTC STAFF REPORT, 2024)", x=360, w=1200)]},
    sources=["ftc24"])
stage("s28_caveat", "m4_caveat", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It did not test"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=750, y=560, at=0.3, text="FTC STAFF REPORT (2024)", scale=0.7, stamp="CAVEAT", stampAt=C("an important caveat")),
              it("letters", x=1300, y=200, text="'DID NOT TEST' SPECIFIC COMPANIES", at=C("It did not test"), size=44, color="gold")]},
    sources=["ftc24"])
stage("s29_fmi", "m4_fmi", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2022", "value": 2.3, "color": "#FFB300", "at": C("fell from two point three"), "display": "2.3%"},
                     {"label": "2023", "value": 1.6, "color": "#43A047", "at": C("in twenty twenty-three, back"), "display": "1.6%"}],
                    at=0.2, max=3, title="FOOD RETAILER NET MARGIN (FMI, INDUSTRY GROUP)", x=300, w=800),
              it("letters", x=1500, y=380, text="DIFFERENT MEASURES", at=C("different measures"), size=48, color="gold"),
              it("letters", x=1500, y=470, text="BOTH CAN BE ACCURATE", at=C("both can be accurate"), size=40, color="white")]},
    sources=["fmi"])
stage("s30_shrink", "m4_shrink", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In its own example"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=170, text="SHRINKFLATION", at=0.3, size=70, color="gold"),
              it("sign", x=900, y=330, text="64 OZ", at=C("a sixty-four ounce"), color="#BBDEFB", size=52),
              it("sign", x=1350, y=330, text="→ 60 OZ, SAME PRICE", at=C("cut to sixty ounces"), color="#FFE0B2", size=44),
              it("letters", x=1250, y=470, text="= +6.7% IN THE CPI (BLS)", at=C("price increase"), size=52, color="risk")]},
    sources=["blsshrink"])
add("p31_rulers", "m4_draw", "engine_draw", {
    "title": "Same years, different rulers", "board": BOARD, "draw_start": C("On the left, the FTC's view"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 400, 360, 320), "color": "risk", "width": 6, "kind": "box", "start": C("On the left, the FTC's view"), "label": lbl("FTC: REVENUE vs ALL COSTS", 720, 380, 20, "risk")},
        {"d": rect(1100, 400, 360, 320), "color": "accent3", "width": 6, "kind": "box", "start": C("On the right, the grocers' view"), "label": lbl("GROCERS: NET PROFIT / SALES", 1280, 380, 20, "accent3")},
        {"d": arrow((910, 560), (1090, 560)) + " " + arrow((1090, 600), (910, 600)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Same years, different rulers"), "label": lbl("SAME YEARS", 1000, 660, 20, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("the debate never ends", 0.1), "dur": 1.4, "target": [1000, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["ftc24", "fmi"])
kinetic("s32_t4", "m4_transition", [("Margins are only half the question…", 60, "only half the question", None, False),
                                    ("…how many companies are left?", 64, "how many companies", "gold", False)])

# ====================================================================== PART 5: fewer, bigger players
card("s33_c5", "m5_card", "Fewer, Bigger Players", "Packers, mergers and the shelf")
stage("s34_meat", "m5_meat", {
    "zones": [Z("ranch", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In nineteen eighty"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=260, text="BEEF", at=0.3, until=C("the four largest"), size=80, color="gold"),
              it("counter", x=1250, y=260, at=C("the four largest"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "of all"}, 85]], text="TOP 4 PACKERS: STEER & HEIFER PURCHASES (USDA ERS)", scale=1.2),
              it("letters", x=1600, y=460, text="1980: 36%", at=C("In nineteen eighty"), size=60, color="gold")]},
    sources=["ersmeat"])
stage("s35_merger", "m5_merger", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The FTC sued"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="KROGER + ALBERTSONS ($24.6BN)", scale=0.7, stamp="BLOCKED", stampAt=C("a federal court stopped")),
              it("letters", x=1250, y=200, text="5,000+ STORES COMBINED", at=C("more than five thousand"), size=50, color="gold"),
              it("gavel", x=1650, y=F - 20, hits=[C("a federal court stopped")], at=0.2),
              it("letters", x=1300, y=320, text="DECEMBER 2024: DEAL OFF", at=C("both companies walked away"), size=44, color="white")]},
    sources=["ftcmerge", "kroger", "aci"])
stage("s36_slot", "m5_slot", {
    "zones": [Z("supermarket", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("ranged from"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=170, text="PAYING FOR SHELF SPACE", at=0.3, size=60, color="gold"),
              it("sign", x=1250, y=330, text="$2,313 – $21,768 PER ITEM", at=C("ranged from"), color="#FFE0B2", size=44),
              it("letters", x=1250, y=470, text="(FTC CASE STUDIES, 2003)", at=C("That study is from"), size=36, color="white")]},
    sources=["ftcslot"])
stage("s37_brands", "m5_brands", {
    "zones": [Z("supermarket", label="STORE BRAND")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When the store makes"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=250, text="THE STORE'S OWN WEAPON", at=0.3, size=54, color="gold"),
              it("counter", x=1000, y=400, at=C("they made up"), prefix="", suffix="%", decimals=1, steps=[[0, 0], [{"cue": "of grocery dollar sales"}, 21.3]], text="STORE BRANDS, SHARE OF DOLLAR SALES 2025 (PLMA)")]},
    sources=["plma"])
add("p38_funnel", "m5_draw", "engine_draw", {
    "title": "The food funnel", "board": BOARD, "draw_start": C("At the top, many farms"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 330, 880, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("At the top, many farms"), "label": lbl("MANY FARMS & RANCHES", 1000, 378, 24, "accent3")},
        {"d": rect(860, 480, 280, 70), "color": "risk", "width": 6, "kind": "box", "start": C("a few big processors"), "label": lbl("FEW PROCESSORS", 1000, 523, 20, "risk")},
        {"d": rect(820, 610, 360, 70), "color": "accent", "width": 6, "kind": "box", "start": C("Then a few big grocery chains"), "label": lbl("FEW BIG CHAINS", 1000, 653, 20, "accent")},
        {"d": rect(560, 750, 880, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("millions of shoppers"), "label": lbl("MILLIONS OF SHOPPERS", 1000, 798, 24, "accent2")},
        {"d": arrow((1000, 415), (1000, 475)) + " " + arrow((1000, 555), (1000, 605)) + " " + arrow((1000, 685), (1000, 745)), "color": "ink", "width": 4, "kind": "arrow", "start": C("The narrower the middle")},
    ],
    "actions": [{"kind": "point", "at": C("the more power sits there", 0.1), "dur": 1.4, "target": [1000, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["ersmeat", "ftcmerge"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("Most of your money"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="SO WHO IS BEHIND YOUR BILL?", at=0.3, until=C("It is not one villain"), size=54, color="gold"),
              it("letters", x=1000, y=150, text="NOT ONE VILLAIN", at=C("It is not one villain"), size=60, color="gold"),
              it("sign", x=850, y=300, text="FARM ≈ 12¢", at=C("The farmer gets about"), color="#C8E6C9", size=40),
              it("sign", x=1250, y=300, text="STORE ≈ 2¢", at=C("The store keeps"), color="#FFE0B2", size=40),
              it("letters", x=1150, y=440, text="THE REST: THE LONG CHAIN", at=C("Most of your money"), size=48, color="white")]},
    sources=["ersfd", "kroger", "ersmeat"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_grocery_storyboard.py; edit the generator, not this file.\n"
           "# Episode 40 storyboard (US grocery prices): one visual language per part; tones from visual_direction.yaml.\n")
