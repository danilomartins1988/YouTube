"""Generates projects/why-america-stopped-making-the-penny/deliverables/documentary/storyboard.yaml
(Episode 42, new topics N2: Why America Stopped Making the Penny).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: a giant spinning coin with its cost tag (new `bigcoin` item) on the mint floor (new `mintfloor` set).
- Part 1 (the coin that costs too much): seigniorage chart, the mint floor, numbers.
- Part 2 (the last penny): the mint floor at night, the Fed's bank hall, coins in circulation.
- Part 3 (the rounding): the supermarket checkout, Congress, the Richmond Fed estimate.
- Part 4 (before and elsewhere): an office calendar (1982), a snowy square (Canada, 2012-13).
- Part 5 (the nickel problem): silver coin, a comparison chart, the exchange floor.
Generic coins only (no real coin designs, no portraits), no logos, no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_penny_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-america-stopped-making-the-penny/deliverables/documentary/storyboard.yaml"
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


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("mintfloor")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("bigcoin", x=1000, y=330, at=0.05, scale=1.0, spin=True, value="1¢", tag="COST 3.69¢"),
              it("letters", x=1000, y=790, text="TO MAKE ONE PENNY (FY2024, U.S. MINT)", at=0.6, size=46, color="gold")]},
    sources=["mint24"])
stage("s02_twist", "h_twist", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.1}, {"at": 0.8, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 0,
    "items": [it("letters", x=960, y=200, text="EVERY NEW PENNY = A SMALL LOSS", at=0.3, size=56, color="white"),
              it("counter", x=960, y=430, at=C("Add them up"), prefix="−$", suffix="M", decimals=1, steps=[[0, 0], [{"cue": "more\n    making pennies", "offset": 0} if False else {"cue": "making pennies than"}, 85.3]], text="PENNIES: COST ABOVE FACE VALUE, FY2024 (MINT)", scale=1.3)]},
    sources=["mint24"])
stage("s03_question", "h_question", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [*crowd([700, 800, 1250], "walk", at=0.1, scale=0.6),
              it("letters", x=1000, y=230, text="WHAT HAPPENS TO YOUR CHANGE?", at=0.3, size=64, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · THE LOSING COIN", at=C("costing more than"), color="#BBDEFB", size=34),
              it("sign", x=960, y=380, text="2 · THE ROUNDING", at=C("how stores round"), color="#FFE0B2", size=34),
              it("sign", x=1560, y=380, text="3 · THE NICKEL NEXT?", at=C("the nickel may be next"), color="#C8E6C9", size=34),
              it("letters", x=960, y=700, text="THE END OF THE PENNY", at=0.4, size=68, color="gold")]})

# ====================================================================== PART 1: the coin that costs too much
card("s05_c1", "m1_card", "The Coin That Costs Too Much", "Seigniorage, and its opposite")
stage("s06_seign", "m1_seign", {
    "zones": [Z("mintfloor", label="U.S. MINT (GENERIC)")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("Economists call"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("bigcoin", x=800, y=360, at=0.3, scale=0.8, metal="silver", value="25¢", tag="COST 14.7¢"),
              it("sign", x=1450, y=330, text="PROFIT = SEIGNIORAGE", at=C("Economists call"), color="#C8E6C9", size=40),
              it("letters", x=1450, y=200, text="QUARTERS: +$165.6M (FY2024)", at=C("quarters\n    alone") if False else C("quarters"), size=44, color="gold")]},
    sources=["mint24"])
stage("s07_penny", "m1_penny", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "FY2023", "value": 3.07, "color": "#C77B3A", "at": C("from about three cents"), "display": "3.07¢"},
                     {"label": "FY2024", "value": 3.69, "color": "#E53935", "at": C("from about three cents", 1.0), "display": "3.69¢"}],
                    at=0.2, max=4.2, title="COST TO MAKE ONE PENNY (U.S. MINT)", x=300, w=760),
              it("letters", x=1500, y=360, text="+20% IN ONE YEAR", at=C("jumped about twenty percent"), size=54, color="risk"),
              it("letters", x=1500, y=470, text="≈ 1.3¢ A DECADE EARLIER (TREASURY)", at=C("one point three cents"), size=32, color="ink"),
              it("letters", x=1500, y=580, text="3.17 BILLION PENNIES SHIPPED", at=C("more than three\n    billion") if False else C("billion new pennies"), size=36, color="ink")]},
    sources=["mint24", "treas"])
stage("s08_perdollar", "m1_perdollar", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=180, text="PER $1 OF PENNIES SHIPPED", at=0.3, size=50, color="white"),
              it("counter", x=960, y=380, at=C("it spent about"), prefix="−$", suffix="", decimals=2, steps=[[0, 0], [{"cue": "sixty-nine cents more"}, 2.69]], text="COST ABOVE FACE VALUE (MINT, FY2024)", scale=1.2),
              it("letters", x=600, y=640, text="DIME: 5.8¢", at=C("A dime costs"), size=48, color="gold"),
              it("letters", x=1320, y=640, text="QUARTER: 14.7¢", at=C("A quarter"), size=48, color="gold")]},
    sources=["mint24"])
stage("s09_streak", "m1_streak", {
    "zones": [Z("mintfloor")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The nickel, worth five cents"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=140, text="19 YEARS IN A ROW ABOVE FACE VALUE", at=C("nineteen fiscal years"), size=48, color="risk"),
              it("bigcoin", x=800, y=380, at=0.3, scale=0.7, value="1¢", tag="3.69¢"),
              it("bigcoin", x=1550, y=380, at=C("The nickel, worth five cents"), scale=0.75, metal="silver", value="5¢", tag="13.78¢")]},
    sources=["mint24"])
stage("s10_total", "m1_total", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "FY2023", "value": 249.0, "color": "#90A4AE", "at": 0.4, "display": "$249.0M"},
                     {"label": "FY2024", "value": 99.5, "color": "#43A047", "at": C("about ninety-nine point five"), "display": "$99.5M"}],
                    at=0.2, max=280, title="TOTAL PROFIT ON CIRCULATING COINS (MINT)", x=300, w=760),
              it("letters", x=1500, y=420, text="−60% IN ONE YEAR", at=C("sixty percent less"), size=56, color="risk")]},
    sources=["mint24"])
add("p11_ledger", "m1_draw", "engine_draw", {
    "title": "The coin ledger, FY2024 (U.S. Mint)", "board": BOARD, "draw_start": C("Here is the quarter"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 640 L 1440 640", "color": "ink", "width": 4, "start": C("Let me draw the coin ledger"), "label": lbl("BREAK EVEN", 1480, 646, 18, "ink", "start")},
        {"d": "M 620 640 L 620 360 L 780 360 L 780 640", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("Here is the quarter"), "label": lbl("QUARTER +$165.6M", 700, 340, 18, "accent3")},
        {"d": "M 840 640 L 840 580 L 1000 580 L 1000 640", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.25, "kind": "bar", "start": C("The dime"), "label": lbl("DIME +$35.6M", 920, 560, 18, "accent3")},
        {"d": "M 1060 640 L 1060 670 L 1220 670 L 1220 640", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("the nickel, a loss"), "label": lbl("NICKEL −$17.7M", 1140, 700, 18, "risk")},
        {"d": "M 1260 640 L 1260 785 L 1420 785 L 1420 640", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.35, "kind": "bar", "start": C("And the penny"), "label": lbl("PENNY −$85.3M", 1340, 815, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Two coins cost", 0.1), "dur": 1.4, "target": [1340, 720]}],
    "scale": 0.86, "floor": 1040}, sources=["mint24"])
kinetic("s12_t1", "m1_transition", [("For years, the loss was accepted…", 62, "For years", None, False),
                                    ("…then the plug was pulled", 64, "pulled the plug", "gold", False)])

# ====================================================================== PART 2: the last penny
card("s13_c2", "m2_card", "The Last Penny", "November 12, 2025")
stage("s14_strike", "m2_strike", {
    "zones": [Z("mintfloor", night=True, label="PHILADELPHIA")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("According to the St. Louis Fed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=170, text="NOV 12, 2025: THE FINAL STRIKE", at=0.3, size=56, color="gold"),
              it("bigcoin", x=1000, y=430, at=C("ceremonial strike"), scale=0.6, value="1¢"),
              it("letters", x=1450, y=640, text="ENDING 232 YEARS (ST. LOUIS FED)", at=C("it ended"), size=40, color="white")]},
    sources=["mintpr", "stlfed"])
stage("s15_early", "m2_early", {
    "zones": [Z("bankhall", label="THE FED")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=330, text="LAST NEW PENNIES: SHORTLY AFTER MAY 2025", at=0.3, size=44, color="gold"),
              it("letters", x=1000, y=440, text="(FEDERAL RESERVE)", at=0.6, size=34, color="ink")]},
    sources=["fedcash"])
stage("s16_tender", "m2_tender", {
    "zones": [Z("bankhall", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("And the\n    Federal Reserve") if False else C("keeps moving the old ones"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="NOT GONE", at=0.3, until=C("still legal tender"), size=70, color="gold"),
              it("sign", x=900, y=300, text="STILL LEGAL TENDER", at=C("still legal tender"), color="#C8E6C9", size=42),
              it("sign", x=1450, y=300, text="COLLECTOR CENTS ONLY", at=C("for collectors"), color="#FFE0B2", size=36),
              it("letters", x=1250, y=460, text="JAN 2026: DEPOSITS RESUMED", at=C("resumed taking penny deposits"), size=44, color="gold")]},
    sources=["mintpr", "fedcash"])
stage("s17_count", "m2_count", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=160, text="HOW MANY PENNIES ARE OUT THERE?", at=0.3, size=52, color="white"),
              it("counter", x=560, y=380, at=C("roughly one hundred"), prefix="", suffix="BN", steps=[[0, 0], [{"cue": "and fourteen\n    billion"} if False else {"cue": "fourteen"}, 114]], text="TREASURY"),
              it("counter", x=1360, y=380, at=C("The Mint has estimated"), prefix="", suffix="BN", steps=[[0, 0], [{"cue": "three hundred billion"}, 300]], text="U.S. MINT"),
              it("letters", x=960, y=640, text="RECIRCULATED 'FOR AS LONG AS POSSIBLE'", at=C("for as long as possible"), size=40, color="gold")]},
    sources=["treas", "mintpr"])
stage("s18_save", "m2_save", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=260, text="THE SAVINGS", at=0.3, until=C("According to the Treasury"), size=70, color="gold"),
              it("counter", x=1000, y=260, at=C("According to the Treasury"), prefix="≈ $", suffix="M", steps=[[0, 0], [{"cue": "a year in materials"}, 56]], text="SAVED PER YEAR IN MATERIALS (TREASURY)", scale=1.2),
              it("letters", x=1000, y=430, text="A LOSS THAT GREW EVERY YEAR, ENDED", at=C("ends a loss"), size=44, color="gold")]},
    sources=["treas"])
add("p19_journey", "m2_draw", "engine_draw", {
    "title": "A penny's journey", "board": BOARD, "draw_start": C("Here is the Mint"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 150, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Here is the Mint"), "label": lbl("MINT", 635, 468, 22, "risk")},
        {"d": rect(760, 420, 150, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("Then the Fed"), "label": lbl("FED", 835, 468, 22, "accent2")},
        {"d": rect(960, 420, 150, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("then the banks"), "label": lbl("BANKS", 1035, 468, 22, "accent2")},
        {"d": rect(1160, 420, 150, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("then the stores"), "label": lbl("STORES", 1235, 468, 22, "accent3")},
        {"d": rect(1160, 600, 150, 80), "color": "accent", "width": 5, "kind": "box", "start": C("then your pocket"), "label": lbl("POCKET", 1235, 648, 22, "accent")},
        {"d": rect(960, 600, 150, 80), "color": "muted", "width": 5, "kind": "box", "start": C("often a jar"), "label": lbl("JAR", 1035, 648, 22, "muted")},
        {"d": arrow((715, 460), (755, 460)) + " " + arrow((915, 460), (955, 460)) + " " + arrow((1115, 460), (1155, 460)) + " " + arrow((1235, 505), (1235, 595)) + " " + arrow((1155, 640), (1115, 640)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Then the Fed", 0.3)},
        {"d": "M 570 410 L 700 510 M 700 410 L 570 510", "color": "risk", "width": 8, "start": C("Now the first step is gone")},
    ],
    "actions": [{"kind": "point", "at": C("Now the first step", 0.1), "dur": 1.4, "target": [635, 460]}],
    "scale": 0.86, "floor": 1040}, sources=["fedcash", "mintpr"])
kinetic("s20_t2", "m2_transition", [("A practical question…", 64, "A very practical", None, False),
                                    ("…what happens at the register?", 64, "at the cash register", "gold", False)])

# ====================================================================== PART 3: the rounding
card("s21_c3", "m3_card", "The Rounding", "Cash only, after tax")
stage("s22_rule", "m3_rule", {
    "zones": [Z("supermarket", label="CHECKOUT")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("If the total ends in one"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=270, text="TREASURY GUIDANCE (NOT A LAW)", at=0.3, size=50, color="gold"),
              it("sign", x=900, y=400, text="1 · 2 · 6 · 7 → ROUND DOWN", at=C("round down"), color="#C8E6C9", size=40),
              it("sign", x=1550, y=400, text="3 · 4 · 8 · 9 → ROUND UP", at=C("round up"), color="#FFCDD2", size=40)]},
    sources=["treas"])
stage("s23_example", "m3_example", {
    "zones": [Z("supermarket")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("If you pay by card"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("pricetag", x=800, y=320, at=0.3, text="$4.98 → $5.00", scale=1.0),
              it("pricetag", x=800, y=470, at=C("ninety-six"), text="$4.96 → $4.95", scale=1.0),
              it("letters", x=1500, y=300, text="CARD: EXACT CENT", at=C("If you pay by card"), size=52, color="gold"),
              it("letters", x=1500, y=420, text="ONCE PER RECEIPT", at=C("once, on the whole receipt"), size=48, color="white")]},
    sources=["treas"])
stage("s24_states", "m3_states", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In Congress"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="WASHINGTON SHB 2334 (2026)", scale=0.7, stamp="ALLOWED, NOT REQUIRED", stampAt=C("does not force them")),
              it("letters", x=1300, y=200, text="EXACT CHANGE STILL OK · TAX FIRST", at=C("Customers can still pay"), size=36, color="white"),
              it("letters", x=1300, y=310, text="COMMON CENTS ACT: NOT LAW YET (AUG 2026)", at=C("Common Cents Act"), size=34, color="gold")]},
    sources=["wa", "congress"])
stage("s25_tax", "m3_tax", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=160, text="A ROUNDING 'TAX'? (RICHMOND FED)", at=0.3, size=52, color="white"),
              it("counter", x=960, y=380, at=C("estimate the cost"), prefix="≈ $", suffix="M / YEAR", decimals=2, steps=[[0, 0], [{"cue": "a year"} if False else {"cue": "across the whole country"}, 6.06]], text="COST TO CONSUMERS (ESTIMATE)", scale=1.2),
              it("letters", x=960, y=640, text="< 2¢ PER AMERICAN A YEAR (OUR CALCULATION)", at=C("By our calculation"), size=40, color="gold")]},
    sources=["richfed"])
add("p26_wheel", "m3_draw", "engine_draw", {
    "title": "The rounding wheel (Treasury guidance)", "board": BOARD, "draw_start": C("Here are the last digits"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 600 L 1400 600", "color": "ink", "width": 4, "start": C("Let me draw the rounding wheel"), "label": lbl("0   1   2   3   4   5   6   7   8   9   10", 1000, 650, 26, "ink")},
        {"d": arrow((700, 560), (610, 560), 0.3), "color": "accent3", "width": 5, "kind": "arrow", "start": C("One and two go down"), "label": lbl("DOWN", 660, 520, 18, "accent3")},
        {"d": arrow((880, 560), (990, 560), 0.3), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three and"), "label": lbl("UP", 935, 520, 18, "risk")},
        {"d": arrow((1100, 560), (1010, 560), 0.3), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Six and seven"), "label": lbl("DOWN", 1060, 520, 18, "accent3")},
        {"d": arrow((1280, 560), (1390, 560), 0.3), "color": "risk", "width": 5, "kind": "arrow", "start": C("Eight and nine"), "label": lbl("UP", 1335, 520, 18, "risk")},
        {"d": "M 700 760 L 700 700 L 860 700 L 860 760 M 1140 760 L 1140 700 L 1300 700 L 1300 760", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Half the time you win"), "label": lbl("WIN · LOSE", 1000, 800, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Half the time you lose", 0.1), "dur": 1.4, "target": [1000, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["treas"])
kinetic("s27_t3", "m3_transition", [("Not the first rethink…", 64, "not the first time", None, False),
                                    ("…and not the first country", 64, "first country to drop", "gold", False)])

# ====================================================================== PART 4: before and elsewhere
card("s28_c4", "m4_card", "Before and Elsewhere", "1982 · Canada 2013")
stage("s29_zinc", "m4_zinc", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At the time"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("calendar", x=600, y=520, at=0.3, pages=[[0, "1982", "NEW RECIPE"]], scale=0.8),
              it("sign", x=1100, y=260, text="95% COPPER → ≈ 98% ZINC", at=C("ninety-five percent copper"), color="#FFE0B2", size=40),
              it("letters", x=1300, y=420, text="SAVE ≈ $25M A YEAR (1981 REPORT)", at=C("expected to save"), size=40, color="gold")]},
    sources=["zinc"])
stage("s30_canada", "m4_canada", {
    "zones": [Z("wintersquare")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its\n    mint") if False else C("stopped sending pennies"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="CANADA · MAY 4, 2012 · WINNIPEG", at=0.3, size=52, color="gold"),
              it("bigcoin", x=800, y=420, at=0.4, scale=0.6, value="1¢", tag="COST 1.6¢ (CANADA)"),
              it("sign", x=1450, y=320, text="FEB 4, 2013: NO MORE PENNIES TO BANKS", at=C("stopped sending pennies"), color="#BBDEFB", size=32)]},
    sources=["canada"])
stage("s31_canada2", "m4_canada2", {
    "zones": [Z("wintersquare", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=300, text="THE SAVINGS IN CANADA", at=0.3, until=C("eleven million Canadian dollars"), size=60, color="gold"),
              it("counter", x=1000, y=300, at=C("eleven million Canadian dollars"), prefix="≈ US$", suffix="M", decimals=1, steps=[[0, 0], [{"cue": "that is"}, 11.2]], text="SAVED A YEAR (AT JAN 2013 FED H.10 RATE)", scale=1.2),
              it("letters", x=1000, y=560, text="CANADA HAS ROUNDED CASH EVER SINCE", at=C("ever since"), size=44, color="white")]},
    sources=["canada"])
add("p32_timeline", "m4_draw", "engine_draw", {
    "title": "Same reason, three times", "board": BOARD, "draw_start": C("Nineteen eighty-two, the copper"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 580 600 L 1420 600", "color": "ink", "width": 5, "start": C("Let me draw the timeline")},
        {"d": rect(560, 450, 220, 100), "color": "accent", "width": 5, "kind": "box", "start": C("Nineteen eighty-two, the copper"), "label": lbl("1982 ZINC", 670, 508, 22, "accent")},
        {"d": rect(890, 450, 220, 100), "color": "accent2", "width": 5, "kind": "box", "start": C("Twenty thirteen, Canada"), "label": lbl("2013 CANADA", 1000, 508, 22, "accent2")},
        {"d": rect(1220, 450, 220, 100), "color": "risk", "width": 5, "kind": "box", "start": C("Twenty twenty-five, the United States"), "label": lbl("2025 U.S.", 1330, 508, 22, "risk")},
        {"d": arrow((785, 500), (885, 500)) + " " + arrow((1115, 500), (1215, 500)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Twenty thirteen, Canada", 0.4)},
        {"d": "M 900 760 L 900 680 L 1100 680 L 1100 760", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("The metal\n    cost") if False else C("cost more than the coin"), "label": lbl("METAL > COIN", 1000, 800, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the same reason", 0.1), "dur": 1.4, "target": [1000, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["zinc", "canada", "mintpr"])
kinetic("s33_t4", "m4_transition", [("The same reason…", 64, "And that same reason", None, False),
                                    ("…is staring at the next coin up", 60, "the next coin up", "gold", False)])

# ====================================================================== PART 5: the nickel problem
card("s34_c5", "m5_card", "The Nickel Problem", "Five cents that cost fourteen")
stage("s35_nickel", "m5_nickel", {
    "zones": [Z("mintfloor", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("bigcoin", x=1000, y=380, at=0.2, scale=0.9, spin=True, metal="silver", value="5¢", tag="COST 13.78¢"),
              it("letters", x=1000, y=790, text="NICKELS: −$17.7M (FY2024)", at=C("seventeen point seven"), size=48, color="risk")]},
    sources=["mint24"])
stage("s36_why", "m5_why", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "ROUND TO 5¢", "value": 6.06, "color": "#43A047", "at": C("Without pennies and nickels"), "display": "$6.06M"},
                     {"label": "ROUND TO 10¢", "value": 55.58, "color": "#E53935", "at": C("The Richmond Fed estimates"), "display": "$55.58M"}],
                    at=0.2, max=62, title="ROUNDING COST TO CONSUMERS PER YEAR (RICHMOND FED ESTIMATES)", x=300, w=900),
              it("letters", x=1560, y=420, text="≈ 9× MORE", at=C("nearly ten times"), size=60, color="risk")]},
    sources=["richfed"])
stage("s37_cash", "m5_cash", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For the Mint"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=260, text="THE BIGGER TREND", at=0.3, until=C("cash was used in only about"), size=64, color="gold"),
              it("counter", x=1000, y=260, at=C("cash was used in only about"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "fourteen\n    percent"} if False else {"cue": "percent of payments"}, 14]], text="CASH SHARE OF PAYMENTS, 2024 (ST. LOUIS FED)", scale=1.2),
              it("letters", x=1300, y=500, text="FEWER COINS · LESS METAL · ONE LESS LOSS", at=C("For the Mint"), size=38, color="gold")]},
    sources=["stlfed"])
add("p38_tradeoff", "m5_draw", "engine_draw", {
    "title": "Minting loss vs rounding cost (FY2024 / estimates)", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1440 860", "color": "ink", "width": 4, "start": C("Let me draw the trade-off")},
        {"d": "M 600 860 L 600 420 L 720 420 L 720 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("On one side"), "label": lbl("PENNY LOSS $85.3M", 660, 400, 18, "risk")},
        {"d": "M 740 860 L 740 830 L 860 830 L 860 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("On the other side"), "label": lbl("ROUND 5¢ $6M", 800, 810, 18, "accent3")},
        {"d": "M 1080 860 L 1080 770 L 1200 770 L 1200 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("For the nickel"), "label": lbl("NICKEL LOSS $17.7M", 1140, 750, 18, "risk")},
        {"d": "M 1220 860 L 1220 575 L 1340 575 L 1340 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("rounding would cost more"), "label": lbl("ROUND 10¢ $55.6M", 1280, 555, 18, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("a harder call", 0.1), "dur": 1.4, "target": [1280, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["mint24", "richfed"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("mintfloor", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The penny crossed"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("bigcoin", x=1000, y=380, at=0.2, scale=0.8, spin=True, value="1¢"),
              it("letters", x=1000, y=130, text="A COIN IS A PRODUCT", at=C("It is a product"), size=60, color="gold"),
              it("letters", x=1000, y=790, text="COST > FACE VALUE = A LOSS ON EVERY COIN", at=C("every new coin is a loss"), size=40, color="white")]},
    sources=["mint24", "mintpr"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_penny_storyboard.py; edit the generator, not this file.\n"
           "# Episode 42 storyboard (the penny): one visual language per part; tones from visual_direction.yaml.\n")
