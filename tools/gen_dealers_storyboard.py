"""Generates projects/how-car-dealerships-really-make-money/deliverables/documentary/storyboard.yaml (Episode 34,
US batch #07: How Car Dealerships Really Make Money).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the dealership lot (new `dealership` set) with a generic sedan (new `sedan` item) and its price sticker.
- Part 1 (the showroom): the lot by day, sedans that sell, revenue vs profit charts.
- Part 2 (the finance office): the back office, contracts and add-on price tags, the CARS Rule in court.
- Part 3 (the service bay): a service bay with lifts (new `garage` set), cars going up on the lift.
- Part 4 (the dealer's shield): the state capitol, a barrier between carmaker and buyer.
- Part 5 (the buyer's bill): the suburb at night, loan screens and charts.
No real brands, logos or car designs; company names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_dealers_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-car-dealerships-really-make-money/deliverables/documentary/storyboard.yaml"
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


def car(x=960, **kw):
    return it("sedan", x=x, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=1000, y=170, at=0.05, prefix="$", suffix="", steps=[[0.05, 0], [1.5, 2564]], text="GROSS PROFIT PER NEW CAR, AUTONATION 2025 (10-K)", scale=1.4),
              car(1000, at=0.3, scale=0.9, color="#E53935", sticker="$52,075")]},
    sources=["an10k"])
stage("s02_twist", "h_twist", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}], "drift": 0,
    "items": [chart([{"label": "SELLING THE NEW CAR", "value": 2564, "color": "#90A4AE", "at": 0.3, "display": "$2,564"},
                     {"label": "FINANCE OFFICE (F&I)", "value": 2769, "color": "#E89A00", "at": C("The finance"), "display": "$2,769"}],
                    at=0.2, max=3200, title="GROSS PROFIT PER CAR, AUTONATION 2025 (10-K)", x=420, w=860),
              it("letters", x=1560, y=420, text="MORE THAN", at=C("More than the car"), size=70, color="risk"),
              it("letters", x=1560, y=510, text="THE CAR", at=C("More than the car", 0.3), size=70, color="risk")]},
    sources=["an10k"])
stage("s03_question", "h_question", {
    "zones": [Z("dealership", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [car(1000, at=0.1, scale=0.9, color="#1E88E5"),
              it("letters", x=1000, y=150, text="WHERE'S THE MONEY?", at=0.4, size=76, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · SHOWROOM", at=0.3, color="#BBDEFB", size=44),
              it("sign", x=750, y=380, text="2 · FINANCE", at=C("the finance office"), color="#FFE0B2", size=44),
              it("sign", x=1170, y=380, text="3 · SERVICE", at=C("the service bay"), color="#C8E6C9", size=44),
              it("sign", x=1590, y=380, text="4 · THE LAW", at=C("the state laws"), color="#FFCDD2", size=44),
              it("letters", x=960, y=700, text="FOUR ENGINES", at=C("the four engines"), size=72, color="gold")]})

# ====================================================================== PART 1: the showroom (lot by day + charts)
card("s05_c1", "m1_card", "The Showroom", "Big prices, thin profits")
stage("s06_size", "m1_size", {
    "zones": [Z("dealership")], "worldW": 2800,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The average dealership"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1100, y=170, at=0.3, prefix="", suffix="", steps=[[0, 0], [{"cue": "franchised new-car dealers", "offset": 0}, 16990]], text="FRANCHISED NEW-CAR DEALERS (NADA, 2025)", scale=1.1),
              car(700, at=0.3, scale=0.6, color="#43A047", sticker="NEW"),
              car(1250, at=0.5, scale=0.6, color="#FB8C00", sticker="NEW"),
              car(1800, at=0.7, scale=0.6, color="#8E24AA", sticker="NEW"),
              it("letters", x=1700, y=330, text="$1.3 TRILLION IN SALES", at=C("topped one point three trillion"), size=48, color="gold"),
              it("letters", x=1700, y=420, text="≈ 955 NEW CARS PER DEALER", at=C("The average dealership"), size=40, color="white")]},
    sources=["nada"])
stage("s07_price", "m1_price", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Carmakers were also"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [car(800, at=0.2, scale=0.8, color="#E53935", sticker="$50,562"),
              it("letters", x=900, y=200, text="AVERAGE PRICE, SEPT 2026 (KBB)", at=0.5, size=40, color="white"),
              it("pricetag", x=1600, y=320, at=C("Carmakers were also"), text="−$3,359", scale=1.0),
              it("letters", x=1600, y=530, text="INCENTIVES PER CAR", at=C("on incentives"), size=36, color="gold")]},
    sources=["kbb"])
stage("s08_thin", "m1_thin", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2023", "value": 4342, "color": "#90A4AE", "at": C("Gross profit per new car fell"), "display": "$4,342"},
                     {"label": "2025", "value": 2564, "color": "#FFB74D", "at": C("in twenty twenty-three to"), "display": "$2,564"},
                     {"label": "Q3 2026", "value": 2176, "color": "#E53935", "at": C("and to two thousand"), "display": "$2,176"}],
                    at=0.2, max=4800, title="GROSS PROFIT PER NEW CAR (AUTONATION 10-K / 10-Q)", x=420, w=1080),
              it("letters", x=960, y=470, text="49% OF REVENUE · 13% OF PROFIT", at=0.4, until=C("Gross profit per new car fell"), size=64, color="risk")]},
    sources=["an10k", "an10q"])
stage("s09_used", "m1_used", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Many of them arrive"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(700, at=0.2, scale=0.6, color="#78909C", sticker="USED"),
              car([[0, 2300], [{"cue": "Many of them arrive"}, 2300], [{"cue": "a second chance"}, 1400]], at=0.2, scale=0.6, color="#6D4C41", sticker="TRADE-IN"),
              it("letters", x=1000, y=180, text="USED: 28% OF REVENUE · 9% OF PROFIT", at=0.4, size=46, color="gold"),
              it("letters", x=1000, y=270, text="≈ $1,555 PER USED CAR", at=C("about one thousand"), size=40, color="white")]},
    sources=["an10k"])
add("p10_pies", "m1_draw", "engine_draw", {
    "title": "Revenue vs gross profit (AutoNation 2025)", "board": BOARD, "draw_start": C("Here is AutoNation's revenue"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw the pie")},
        {"d": "M 600 860 L 600 400 L 700 400 L 700 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is AutoNation's revenue"), "label": lbl("REVENUE: NEW 49%", 650, 380, 20, "accent2")},
        {"d": "M 760 860 L 760 640 L 860 640 L 860 860", "color": "accent2", "width": 5, "start": C("almost half of it"), "label": lbl("USED 28%", 810, 620, 20, "accent2")},
        {"d": "M 1000 860 L 1000 800 L 1100 800 L 1100 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("The new-car slice shrinks"), "label": lbl("PROFIT: NEW 13%", 1050, 780, 20, "risk")},
        {"d": "M 1160 860 L 1160 440 L 1260 440 L 1260 860 M 1300 860 L 1300 600 L 1400 600 L 1400 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("The big pieces"), "label": lbl("SERVICE 48% · F&I 30%", 1280, 420, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("The big pieces", 0.3), "dur": 1.4, "target": [1280, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["an10k"])
kinetic("s11_t1", "m1_transition", [("After you choose your car…", 58, "The first is a small room", None, True), ("…the finance office", 70, "The finance office", "gold", False)])

# ====================================================================== PART 2: the finance office (back office + court)
card("s12_c2", "m2_card", "The Finance Office", "Loans, warranties and add-ons")
stage("s13_how", "m2_how", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It also sells"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("desk", x=800, at=0.2, scale=0.9),
              it("contract", x=800, y=420, at=C("They take a loan"), text="AUTO LOAN", scale=0.7),
              it("building", x=1600, at=C("places the loan with"), style="bank", text="LENDER", scale=0.7, color="#90A4AE"),
              it("coins", **{"from": [1600, 400], "to": [900, 330]}, at=C("earns a commission"), rate=5),
              it("sign", x=1300, y=200, text="WARRANTIES · SERVICE CONTRACTS · PROTECTION", at=C("It also sells"), color="#FFE0B2", size=32)]},
    sources=["an10k"])
stage("s14_markup", "m2_markup", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=150, text="HOW A RATE MARKUP WORKS (ILLUSTRATION)", at=0.3, size=44, color="white"),
              it("stack", x=700, h=[[0, 60], [{"cue": "called the buy rate", "offset": 0.5}, 300]], at=C("The lender sets a rate"), text="BUY RATE (LENDER)", color="#1E88E5"),
              it("stack", x=1200, h=[[0, 60], [{"cue": "a higher rate", "offset": 0.5}, 380]], at=C("The dealer can offer"), text="YOUR RATE", color="#E53935"),
              it("letters", x=1550, y=560, text="← DIFFERENCE SHARED", at=C("shares the difference"), size=40, color="gold"),
              it("letters", x=960, y=980, text="CFPB: \"INTEREST RATES ARE NEGOTIABLE\"", at=C("interest rates are negotiable"), size=44, color="green")]},
    sources=["cfpb13", "cfpbask"])
stage("s15_addons", "m2_addons", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So you pay interest"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("pricetag", x=600, y=300, at=0.3, text="GAP", scale=0.9),
              it("pricetag", x=950, y=300, at=C("extended warranties"), text="WARRANTY", scale=0.9),
              it("pricetag", x=1300, y=300, at=C("paint protection"), text="PAINT", scale=0.9),
              it("contract", x=1700, y=440, at=C("rolled into the loan"), text="LOAN + ADD-ONS", scale=0.7),
              it("letters", x=1300, y=640, text="+ INTEREST, FOR YEARS", at=C("So you pay interest"), size=48, color="risk")]},
    sources=["cfpbask"])
stage("s16_total", "m2_total", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "F&I", "value": 1464.4, "color": "#E89A00", "at": C("thirty percent of gross profit"), "display": "$1.46bn"},
                     {"label": "NEW CARS", "value": 664.8, "color": "#90A4AE", "at": C("the gross profit it made selling"), "display": "$665m"}],
                    at=0.2, max=1700, dark=True, title="GROSS PROFIT, AUTONATION 2025 (10-K)", x=420, w=860),
              it("letters", x=1560, y=330, text="5% OF REVENUE", at=0.5, size=50, color="white"),
              it("letters", x=1560, y=420, text="30% OF PROFIT", at=C("but thirty percent"), size=60, color="gold"),
              it("letters", x=1560, y=520, text="> 2× NEW CARS", at=C("more than twice"), size=56, color="risk")]},
    sources=["an10k"])
stage("s17_cars", "m2_cars", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The dealers' association sued"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("docs", x=750, y=560, at=0.2, text="FTC CARS RULE", scale=0.7, stamp="VACATED", stampAt=C("vacated the rule")),
              it("calendar", x=1150, y=320, at=0.4, pages=[[0, "DEC", "2023"], [{"cue": "In January twenty twenty-five"}, "JAN 27", "2025"]], scale=0.75),
              it("letters", x=1450, y=140, text="FTC: WOULD SAVE BUYERS $3.4BN+ A YEAR", at=C("It expected to save"), size=38, color="gold"),
              it("gavel", x=1650, y=440, hits=[C("vacated the rule", 0.2)])]},
    sources=["ftc", "ca5"])
add("p18_loan", "m2_draw", "engine_draw", {
    "title": "How the loan grows (illustration)", "board": BOARD, "draw_start": C("Here is the price of the car"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw the loan")},
        {"d": "M 620 860 L 620 560 L 760 560 L 760 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the price of the car"), "label": lbl("CAR", 690, 540, 22, "accent2")},
        {"d": "M 860 860 L 860 500 L 1000 500 L 1000 860 M 860 560 L 1000 560", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("Add the add-ons"), "label": lbl("+ ADD-ONS", 930, 480, 22, "accent")},
        {"d": "M 1100 860 L 1100 420 L 1240 420 L 1240 860 M 1100 500 L 1240 500", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Add a slightly higher"), "label": lbl("+ INTEREST", 1170, 400, 22, "risk")},
        {"d": arrow((1300, 600), (1440, 600)), "color": "ink", "width": 5, "start": C("Stretch it over"), "label": lbl("≈ 6 YEARS", 1370, 580, 22, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("part of that growth", 0.2), "dur": 1.4, "target": [1170, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpbask", "nada"])
kinetic("s19_t2", "m2_transition", [("The most reliable money…", 58, "the most reliable money", None, True), ("…every oil change", 70, "every time your car", "gold", False)])

# ====================================================================== PART 3: the service bay (garage + lifts)
card("s20_c3", "m3_card", "The Service Bay", "The money that keeps coming back")
stage("s21_scale", "m3_scale", {
    "zones": [Z("garage")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The average customer"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(900, at=0.2, scale=0.7, color="#43A047", lift=[[0, 0], [1.5, 0], [3.5, 1]]),
              it("counter", x=1000, y=150, at=0.4, prefix="", suffix="M+", steps=[[0, 0], [{"cue": "repair orders", "offset": 0}, 276]], text="REPAIR ORDERS, 2025 (NADA)"),
              it("letters", x=1600, y=330, text="$164BN SERVICE & PARTS", at=C("Service and parts sales"), size=46, color="gold"),
              it("pricetag", x=1650, y=440, at=C("The average customer"), text="$186/HR", scale=0.9)]},
    sources=["nada"])
stage("s22_share", "m3_share", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "SHARE OF REVENUE", "value": 17.5, "color": "#90A4AE", "at": 0.5, "display": "17%"},
                     {"label": "SHARE OF GROSS PROFIT", "value": 47.6, "color": "#23995A", "at": C("of gross profit"), "display": "48%"},
                     {"label": "Q3 2026", "value": 51.1, "color": "#1B5E20", "at": C("its share passed"), "display": "51%"}],
                    at=0.2, max=60, title="PARTS & SERVICE, AUTONATION (10-K / 10-Q)", x=420, w=1080)]},
    sources=["an10k", "an10q"])
stage("s23_stable", "m3_stable", {
    "zones": [Z("garage")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Warranty repairs"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(800, at=0.2, scale=0.7, color="#1E88E5", lift=1),
              it("letters", x=1100, y=150, text="\"LESS SENSITIVE TO THE ECONOMY\"", at=0.4, size=46, color="white"),
              it("sign", x=1500, y=300, text="BRAKES CAN'T WAIT", at=C("They cannot delay"), color="#FFCDD2", size=40),
              it("sign", x=1600, y=420, text="WARRANTY → PAID BY CARMAKER", at=C("Warranty repairs"), color="#C8E6C9", size=34)]},
    sources=["an10k"])
add("p24_life", "m3_draw", "engine_draw", {
    "title": "The life of one customer", "board": BOARD, "draw_start": C("Day one, the sale"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 760 L 1460 760", "color": "ink", "width": 4, "start": C("Let me draw the life"), "label": lbl("YEARS →", 1420, 800, 22, "ink")},
        {"d": "M 600 760 L 600 700 L 660 700 L 660 760", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Day one, the sale"), "label": lbl("SALE", 630, 680, 20, "accent2")},
        {"d": "M 680 760 L 680 600 L 740 600 L 740 760", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("the loan and the warranty"), "label": lbl("LOAN + WARRANTY", 710, 580, 20, "accent")},
        {"d": " ".join(f"M {820 + 90 * k} 760 L {820 + 90 * k} 680 L {870 + 90 * k} 680 L {870 + 90 * k} 760" for k in range(7)), "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("for years"), "label": lbl("SERVICE, AGAIN AND AGAIN", 1120, 650, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("served again and again", 0.1), "dur": 1.4, "target": [1120, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["an10k"])
kinetic("s25_t3", "m3_transition", [("Why can't carmakers sell to you?", 54, "Why can carmakers not", None, True), ("…the law", 80, "The answer is in", "gold", False)])

# ====================================================================== PART 4: the dealer's shield (capitol + barrier)
card("s26_c4", "m4_card", "The Dealer's Shield", "State franchise laws")
stage("s27_law", "m4_law", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Michigan's law"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.2, text="MCL 445.1574", scale=0.7, stamp="ONLY VIA DEALERS", stampAt=C("other than through franchised dealers")),
              it("letters", x=1350, y=200, text="MICHIGAN: NO DIRECT SALES", at=C("Michigan's law"), size=50, color="gold"),
              it("letters", x=1350, y=290, text="(manufacturer → customer)", at=C("directly to a retail customer"), size=34, color="white")]},
    sources=["mich"])
stage("s28_protect", "m4_protect", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("As AutoNation's annual report"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(700, at=0.2, scale=0.6, color="#E53935"),
              it("sign", x=1300, y=230, text="NO TERMINATION WITHOUT \"GOOD CAUSE\"", at=C("good cause"), color="#BBDEFB", size=34),
              it("sign", x=1300, y=340, text="NO SAME-BRAND RIVAL NEARBY", at=C("often cannot open nearby"), color="#FFE0B2", size=34),
              it("letters", x=1300, y=480, text="\"DESIGNED TO PROTECT DEALERS\"", at=C("to protect dealers"), size=44, color="gold")]},
    sources=["an10k"])
stage("s29_ftc", "m4_ftc", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("Some newer electric"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "\"AN ANOMALY\"", "sub": "FTC staff on direct-sales bans, 2015", "at": 0.3, "w": 480, "color": "#FFF59D", "size": 50},
                {"x": 1550, "y": 380, "text": "STATE BY STATE", "sub": "newer EV makers fight the rules", "at": C("Some newer electric"), "w": 440, "color": "#C8E6C9", "size": 44},
                {"x": 1100, "y": 680, "text": "ONE DOOR", "sub": "for most brands: the dealer", "at": C("the dealer remains"), "w": 420, "color": "#FFCDD2", "size": 52}],
              links=[[0, 1, C("Some newer electric", 0.4)], [1, 2, C("the dealer remains", 0.4)]])]},
    sources=["ftc15"])
add("p30_wall", "m4_draw", "engine_draw", {
    "title": "The wall and the door", "board": BOARD, "draw_start": C("Here is the carmaker"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 460, 200, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the carmaker"), "label": lbl("CARMAKER", 660, 518, 22, "accent2")},
        {"d": rect(1260, 460, 200, 100), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is you"), "label": lbl("YOU", 1360, 518, 26, "accent3")},
        {"d": "M 1000 360 L 1000 470 M 1000 560 L 1000 760", "color": "risk", "width": 12, "start": C("a wall built by state law"), "label": lbl("STATE LAW", 1000, 340, 22, "risk")},
        {"d": rect(970, 470, 60, 90), "color": "accent", "width": 6, "kind": "box", "start": C("with one door"), "label": lbl("DEALER", 1000, 600, 22, "accent")},
        {"d": arrow((770, 510), (960, 510)) + " " + arrow((1040, 510), (1250, 510)), "color": "ink", "width": 4, "start": C("every sale")},
    ],
    "actions": [{"kind": "point", "at": C("passes through it", 0.1), "dur": 1.4, "target": [1000, 515]}],
    "scale": 0.86, "floor": 1040}, sources=["mich", "an10k"])
kinetic("s31_t4", "m4_transition", [("On the other side of the door…", 56, "And on the other side", None, True), ("…the buyer's bill", 70, "the bill lands", "risk", False)])

# ====================================================================== PART 5: the buyer's bill (suburb night + loan charts)
card("s32_c5", "m5_card", "The Buyer's Bill", "Loans, payments, delinquency")
stage("s33_loans", "m5_loans", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Federal Reserve reports"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(800, at=0.2, scale=0.6, color="#78909C"),
              it("counter", x=1000, y=170, at=0.3, prefix="$", suffix=" TRILLION", decimals=2, steps=[[0, 0], [{"cue": "on auto loans", "offset": 0}, 1.71]], text="U.S. AUTO LOAN BALANCES, Q2 2026 (NY FED)", scale=1.1),
              it("pricetag", x=1650, y=320, at=C("The Federal Reserve reports"), text="7.17%", scale=1.0),
              it("letters", x=1650, y=520, text="72-MONTH NEW-CAR LOAN, BANKS", at=C("seventy-two month"), size=32, color="white")]},
    sources=["nyfed", "g19"])
stage("s34_payment", "m5_payment", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("counter", x=720, y=300, at=0.3, prefix="$", suffix="/MO", steps=[[0, 0], [{"cue": "monthly payment on a new car", "offset": 1}, 767]], text="AVERAGE NEW-CAR PAYMENT, Q4 2025 (EXPERIAN VIA NADA)", scale=1.1),
              it("calendar", x=1350, y=330, at=C("average term"), pages=[[0, "≈ 69", "MONTHS"]], scale=0.9),
              it("letters", x=960, y=760, text="≈ 6 YEARS OF PAYMENTS", at=C("close to six years"), size=60, color="gold")]},
    sources=["nada"])
stage("s35_late", "m5_late", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("home", x=700, at=0.2, scale=0.55, night=True),
              car(1150, at=0.3, scale=0.55, color="#6D4C41"),
              it("counter", x=1300, y=220, at=C("In the second quarter"), prefix="", suffix="%", decimals=1, steps=[[0, 0], [{"cue": "moved into serious delinquency", "offset": 0}, 3.0]], text="AUTO BALANCES ENTERING 90+ DAYS LATE (ANNUAL RATE, NY FED)"),
              it("letters", x=1500, y=440, text="\"ELEVATED LEVELS\"", at=C("remain at elevated"), size=56, color="risk")]},
    sources=["nyfed"])
add("p36_machine", "m5_draw", "engine_draw", {
    "title": "The dealership, together", "board": BOARD, "draw_start": C("A thin profit on the car"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me put the dealership")},
        {"d": "M 620 860 L 620 800 L 760 800 L 760 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("A thin profit on the car"), "label": lbl("CAR: THIN", 690, 780, 20, "accent2")},
        {"d": "M 860 860 L 860 560 L 1000 560 L 1000 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("A thick profit on the loan"), "label": lbl("LOAN + ADD-ONS", 930, 540, 20, "accent")},
        {"d": "M 1100 860 L 1100 440 L 1240 440 L 1240 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("A steady profit on every repair"), "label": lbl("SERVICE: STEADY", 1170, 420, 20, "accent3")},
        {"d": "M 1320 860 L 1320 380 M 1300 400 L 1340 400", "color": "risk", "width": 8, "start": C("And a law that keeps"), "label": lbl("THE LAW", 1370, 360, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The customer is the business", 0.1), "dur": 1.4, "target": [1170, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["an10k", "mich"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("dealership", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("Negotiate the price"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [car(1000, at=0.2, scale=0.85, color="#E53935", sticker="PRICE"),
              it("letters", x=1000, y=130, text="NEGOTIATE MORE THAN THE PRICE", at=C("Negotiate the price"), size=54, color="gold"),
              it("sign", x=1000, y=250, text="RATE · ADD-ONS · TERM", at=C("but also the rate"), color="#FFE0B2", size=40)]},
    sources=["an10k", "cfpbask"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_dealers_storyboard.py; edit the generator, not this file.\n"
           "# Episode 34 storyboard (car dealerships): one visual language per part; tones from visual_direction.yaml.\n")
