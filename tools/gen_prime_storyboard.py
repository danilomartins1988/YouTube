"""Generates projects/the-hidden-economics-of-amazon-prime/deliverables/documentary/storyboard.yaml (Episode 37,
US batch #11: The Hidden Economics of Amazon Prime).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: a giant shipping-cost counter and a generic delivery van (new `van` item).
- Part 1 (the fee): the suburb with parcels on the porch, price tags of each Prime price.
- Part 2 (the flywheel): a parcel sort center (new `sortcenter` set) with conveyors and vans.
- Part 3 (the hidden engines): a phone full of sponsored listings, the data-center campus, segment charts.
- Part 4 (the Iliad): a row of cancellation screens (new `flowscreens` item) vs a one-click sign-up; the courtroom.
- Part 5 (the membership economy): the suburb at night, parcels and calendars.
No Amazon logos, smile or real interface designs; names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_prime_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-hidden-economics-of-amazon-prime/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def chart(bars, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars, at=at, **kw)


def van(x=960, **kw):
    return it("van", x=x, **kw)


def boxes(xs, y=F, at=0.3, rows=1, scale=0.5):
    stamp = (lambda k: {**at, "offset": (at.get("offset") or 0) + 0.15 * k}) if isinstance(at, dict) else (lambda k: at + 0.15 * k)
    return [it("pallet", x=x, y=y, at=stamp(k), rows=rows, scale=scale) for k, x in enumerate(xs)]


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("suburb")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1100, y=170, at=0.05, prefix="$", suffix="BN", decimals=1, steps=[[0.05, 0], [1.5, 102.7]], text="AMAZON SHIPPING COSTS, 2025 (10-K)", scale=1.4),
              van([[0, -300], [3.0, 1100]], at=0.2, scale=0.75, text="DELIVERY")]},
    sources=["k25"])
stage("s02_twist", "h_twist", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "SHIPPING COSTS", "value": 102.7, "color": "#E53935", "at": 0.4, "display": "$102.7bn"},
                     {"label": "ALL SUBSCRIPTIONS", "value": 49.6, "color": "#FFB300", "at": C("Now compare it"), "display": "$49.6bn", "sub": "Prime + music, audiobooks…"}],
                    at=0.2, max=115, title="AMAZON, 2025 (10-K)", x=360, w=860),
              it("letters", x=1560, y=400, text="≈ 2×", at=C("about twice as big"), size=110, color="gold"),
              it("letters", x=1560, y=510, text="\"INDEFINITELY\"", at=C("indefinitely"), size=46, color="white")]},
    sources=["k25"])
stage("s03_question", "h_question", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("home", x=1000, at=0.1, scale=0.75, night=True),
              *boxes([780, 860], at=0.3),
              it("letters", x=1000, y=140, text="A MONEY-LOSING DEAL… OR GENIUS?", at=0.4, size=60, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE FEE", at=0.3, color="#BBDEFB", size=38),
              it("sign", x=750, y=380, text="2 · THE FLYWHEEL", at=C("the flywheel"), color="#FFE0B2", size=38),
              it("sign", x=1170, y=380, text="3 · HIDDEN ENGINES", at=C("hidden"), color="#C8E6C9", size=38),
              it("sign", x=1590, y=380, text="4 · THE MAZE", at=C("the cancellation maze"), color="#FFCDD2", size=38),
              it("letters", x=960, y=700, text="THE PRIME MACHINE", at=C("the four parts"), size=72, color="gold")]})

# ====================================================================== PART 1: the fee (suburb + parcels + price tags)
card("s05_c1", "m1_card", "The Fee", "From $79 to $139")
stage("s06_launch", "m1_launch", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Jeff Bezos called it"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("calendar", x=600, y=300, at=0.2, pages=[[0, "FEB 2", "2005"]], scale=0.8),
              it("pricetag", x=1000, y=300, at=C("For a flat"), text="$79 / YEAR", scale=1.0),
              it("letters", x=1450, y=520, text="UNLIMITED 2-DAY SHIPPING", at=C("unlimited two-day"), size=44, color="gold"),
              it("letters", x=1550, y=180, text="\"ALL-YOU-CAN-EAT\"", at=C("all-you-can-eat"), size=56, color="white")]},
    sources=["launch"])
stage("s07_prices", "m1_prices", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2005", "value": 79, "color": "#90A4AE", "at": 0.4, "display": "$79"},
                     {"label": "2015", "value": 99, "color": "#4FC3F7", "at": C("ninety-nine dollar"), "display": "$99"},
                     {"label": "2018", "value": 119, "color": "#FFB300", "at": C("one hundred and nineteen"), "display": "$119"},
                     {"label": "2022–2026", "value": 139, "color": "#E53935", "at": C("thirty-nine dollars a year"), "display": "$139"}],
                    at=0.2, max=150, title="U.S. PRIME ANNUAL PRICE (AMAZON)", x=300, w=1100),
              it("letters", x=1650, y=420, text="OR $14.99/MO", at=C("fourteen ninety-nine"), size=46, color="gold")]},
    sources=["launch", "prices"])
stage("s08_members", "m1_members", {
    "zones": [Z("suburb")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Three years later"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [*boxes([600, 680, 1200, 1280, 1360, 1800, 1880, 1960], at=0.3, scale=0.45),
              it("counter", x=1000, y=170, at=0.4, prefix="", suffix="M+", steps=[[0, 0], [{"cue": "one hundred million paid members", "offset": 0}, 100], [{"cue": "Prime members worldwide"}, 200]], text="PRIME MEMBERS (AMAZON SHAREHOLDER LETTERS)"),
              it("letters", x=1600, y=330, text="LAST OFFICIAL COUNT: 2021", at=C("the last official total"), size=40, color="white")]},
    sources=["letters"])
stage("s09_revenue", "m1_revenue", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2023", "value": 40.2, "color": "#90A4AE", "at": 0.4, "display": "$40.2bn"},
                     {"label": "2024", "value": 44.4, "color": "#FFB300", "at": C("forty-four"), "display": "$44.4bn"},
                     {"label": "2025", "value": 49.6, "color": "#E89A00", "at": C("in twenty twenty-five"), "display": "$49.6bn"}],
                    at=0.2, max=55, dark=True, title="SUBSCRIPTION SERVICES REVENUE (AMAZON 10-K)", x=360, w=1000),
              it("letters", x=1580, y=380, text="PRIME + MUSIC +", at=C("That line includes"), size=34, color="white"),
              it("letters", x=1580, y=450, text="AUDIOBOOKS + VIDEO", at=C("That line includes", 0.5), size=34, color="white"),
              it("letters", x=1580, y=560, text="Q3 2026: ≈ $14BN", at=C("In the third quarter"), size=44, color="gold")]},
    sources=["k25", "q3"])
add("p10_deal", "m1_draw", "engine_draw", {
    "title": "The deal (illustration)", "board": BOARD, "draw_start": C("On one side, what a member pays"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1000 800 L 1000 470 M 900 800 L 1100 800", "color": "ink", "width": 6, "start": C("Let me draw the deal")},
        {"d": "M 700 500 L 1300 470", "color": "ink", "width": 6, "start": C("On one side, what a member pays")},
        {"d": "M 620 500 L 780 500 L 760 560 L 640 560 Z", "color": "accent", "width": 6, "kind": "box", "start": C("one hundred and thirty-nine dollars a year"), "label": lbl("$139 PAID", 700, 600, 22, "accent")},
        {"d": "M 1220 470 L 1380 470 L 1360 530 L 1240 530 Z", "color": "accent3", "width": 6, "kind": "box", "start": C("what the member gets"), "label": lbl("SHIPPING · VIDEO · MUSIC", 1300, 570, 20, "accent3")},
        {"d": arrow((1000, 380), (1000, 440)), "color": "risk", "width": 5, "kind": "arrow", "start": C("So where does Amazon win"), "label": lbl("WHERE'S THE WIN?", 1000, 360, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("So where does Amazon win", 0.1), "dur": 1.4, "target": [1000, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["prices"])
kinetic("s11_t1", "m1_transition", [("The answer is one word…", 60, "The answer starts", None, True), ("Marketing.", 90, "Marketing", "gold", False)])

# ====================================================================== PART 2: the flywheel (sort center)
card("s12_c2", "m2_card", "The Flywheel", "Shipping, warehouses and video")
stage("s13_marketing", "m2_marketing", {
    "zones": [Z("sortcenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 3,
    "items": [it("docs", x=700, y=560, at=0.2, text="AMAZON 10-K", scale=0.7, stamp="NOT MARKETING EXPENSE", stampAt=C("not counted in marketing")),
              it("letters", x=1350, y=150, text="\"EFFECTIVE WORLDWIDE MARKETING TOOLS\"", at=C("effective worldwide marketing"), size=40, color="gold"),
              it("letters", x=1350, y=240, text="\"…INDEFINITELY\"", at=C("indefinitely"), size=48, color="white")]},
    sources=["k25"])
stage("s14_costs", "m2_costs", {
    "zones": [Z("sortcenter")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Fulfillment"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [van([[0, 500], [{"cue": "Fulfillment"}, 500], [{"cue": "These numbers cover"}, 2300]], at=0.2, scale=0.6, openAt=0.6, text="DELIVERY"),
              it("counter", x=1000, y=170, at=0.4, prefix="$", suffix="BN", decimals=1, steps=[[0, 89.5], [{"cue": "in twenty twenty-five"}, 102.7]], text="SHIPPING COSTS, 2023 → 2025 (10-K)", scale=1.1),
              it("letters", x=1700, y=330, text="+ FULFILLMENT ≈ $109BN", at=C("Fulfillment"), size=44, color="gold"),
              it("letters", x=1700, y=420, text="(ALL CUSTOMERS, NOT ONLY PRIME)", at=C("These numbers cover"), size=30, color="white")]},
    sources=["k25"])
stage("s15_video", "m2_video", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("home", x=800, at=0.2, scale=0.7, night=True),
              it("bigphone", x=1500, y=440, at=0.3, scale=0.8, rot=90, len=8),
              it("counter", x=1300, y=140, at=C("Amazon spent"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "on video and music", "offset": 0}, 22.4]], text="VIDEO AND MUSIC EXPENSE, 2025 (10-K)")]},
    sources=["k25"])
stage("s16_value", "m2_value", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("A member who has paid"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "BUY MORE", "sub": "members shop more often", "at": 0.3, "w": 400, "color": "#C8E6C9", "size": 52},
                {"x": 1550, "y": 380, "text": "≈ $630", "sub": "value per member (Amazon's own estimate, 2020)", "at": C("about six hundred"), "w": 480, "color": "#FFF59D", "size": 58},
                {"x": 1100, "y": 680, "text": "SHOP HERE FIRST", "sub": "already paid for shipping", "at": C("A member who has paid"), "w": 440, "color": "#FFCDD2", "size": 46}],
              links=[[0, 1, C("about six hundred", 0.4)], [1, 2, C("A member who has paid", 0.4)]])]},
    sources=["letters"])
add("p17_flywheel", "m2_draw", "engine_draw", {
    "title": "The flywheel", "board": BOARD, "draw_start": C("Lower prices and fast"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 360, 280, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("Lower prices and fast"), "label": lbl("LOW PRICES · FAST", 1000, 408, 22, "accent3")},
        {"d": rect(1200, 560, 240, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("bring more customers"), "label": lbl("CUSTOMERS", 1320, 608, 22, "accent2")},
        {"d": rect(880, 740, 240, 80), "color": "accent", "width": 5, "kind": "box", "start": C("More customers bring more sellers"), "label": lbl("SELLERS", 1000, 788, 22, "accent")},
        {"d": rect(560, 560, 240, 80), "color": "risk", "width": 5, "kind": "box", "start": C("More sellers bring more choice"), "label": lbl("CHOICE", 680, 608, 22, "risk")},
        {"d": arrow((1140, 420), (1270, 550)), "color": "ink", "width": 4, "kind": "arrow", "start": C("bring more customers", 0.3)},
        {"d": arrow((1290, 650), (1120, 760)), "color": "ink", "width": 4, "kind": "arrow", "start": C("More customers bring more sellers", 0.3)},
        {"d": arrow((880, 770), (720, 650)), "color": "ink", "width": 4, "kind": "arrow", "start": C("More sellers bring more choice", 0.3)},
        {"d": arrow((700, 550), (860, 420)), "color": "ink", "width": 4, "kind": "arrow", "start": C("which brings more customers again")},
        {"d": rect(940, 560, 120, 80), "color": "ink", "width": 6, "kind": "box", "start": C("Prime sits at the center"), "label": lbl("PRIME", 1000, 608, 26, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("Prime sits at the center", 0.2), "dur": 1.4, "target": [1000, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["k25"])
kinetic("s18_t2", "m2_transition", [("The flywheel isn't the profit…", 56, "But the flywheel alone", None, True), ("…two hidden businesses", 64, "two businesses most shoppers", "gold", False)])

# ====================================================================== PART 3: the hidden engines (phone ads + data centers)
card("s19_c3", "m3_card", "The Hidden Engines", "Advertising and the cloud")
stage("s20_ads", "m3_ads", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("browser", x=520, y=480, at=0.2, scale=0.8),
              it("letters", x=520, y=150, text="\"SPONSORED\"", at=C("Every sponsored product"), size=56, color="risk"),
              chart([{"label": "2023", "value": 46.9, "color": "#90A4AE", "at": C("forty-seven billion"), "display": "$46.9bn"},
                     {"label": "2024", "value": 56.2, "color": "#FFB300", "at": C("forty-seven billion", 0.6), "display": "$56.2bn"},
                     {"label": "2025", "value": 68.6, "color": "#E53935", "at": C("in twenty twenty-five"), "display": "$68.6bn"}],
                    at=0.4, max=75, title="ADVERTISING REVENUE (10-K)", x=960, y=230, w=820, h=520)]},
    sources=["k25"])
stage("s21_video", "m3_video", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In twenty twenty-six"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("bigphone", x=800, y=440, at=0.2, scale=0.8, rot=90, len=6),
              it("sign", x=800, y=150, text="ADS ON BY DEFAULT (JAN 2024)", at=C("started showing ads"), color="#FFCDD2", size=36),
              it("pricetag", x=1450, y=320, at=C("Watching without them"), text="+$2.99/MO", pages=[[{"cue": "In twenty twenty-six"}, "+$4.99/MO", True]], scale=1.0),
              it("letters", x=1650, y=540, text="AD-FREE COSTS EXTRA", at=C("Watching without them"), size=40, color="gold")]},
    sources=["video"])
stage("s22_aws", "m3_aws", {
    "zones": [Z("datacenter")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In the third quarter"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("isodc", x=900, y=700, at=0.2, n=9, step=0.2, cols=3, scale=0.75, glow=True),
              it("counter", x=1450, y=180, at=C("By our calculation"), prefix="", suffix="%", steps=[[0, 0], [{"cue": "operating income"}, 57]], text="AWS SHARE OF AMAZON'S OPERATING INCOME, 2025 (OUR CALC.)"),
              it("letters", x=1500, y=380, text="ON ONLY 18% OF SALES", at=C("only eighteen percent"), size=48, color="gold"),
              it("letters", x=1500, y=470, text="Q3 2026: ≈ 63%", at=C("In the third quarter"), size=44, color="white")]},
    sources=["k25", "q3"])
stage("s23_margin", "m3_margin", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "AWS (CLOUD)", "value": 35.4, "color": "#4FC3F7", "at": C("A W S kept about"), "display": "35¢"},
                     {"label": "NORTH AMERICA STORE", "value": 6.9, "color": "#FFB300", "at": C("The North American store"), "display": "7¢"}],
                    at=0.2, max=40, dark=True, title="OPERATING PROFIT PER $1 OF SALES, 2025 (OUR CALCULATION)", x=520, w=880),
              it("letters", x=960, y=470, text="WHERE THE PROFIT IS", at=0.3, until=C("A W S kept about"), size=84, color="gold"),
              it("letters", x=960, y=990, text="THE CLOUD PAYS · THE STORE BUILDS THE HABIT", at=C("The cloud pays"), size=40, color="white")]},
    sources=["k25"])
add("p24_profit", "m3_draw", "engine_draw", {
    "title": "Where Amazon's profit comes from (schematic)", "board": BOARD, "draw_start": C("Here is the store"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw where")},
        {"d": "M 600 860 L 600 400 L 760 400 L 760 860 M 600 800 L 760 800", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.25, "kind": "bar", "start": C("Here is the store"), "label": lbl("STORE: BIG SALES, THIN PROFIT", 680, 380, 18, "accent")},
        {"d": "M 860 860 L 860 700 L 1020 700 L 1020 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("Here is advertising"), "label": lbl("ADS: FAST GROWTH", 940, 680, 18, "risk")},
        {"d": "M 1120 860 L 1120 640 L 1280 640 L 1280 860 M 1120 700 L 1280 700", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.4, "kind": "bar", "start": C("And here is the cloud"), "label": lbl("CLOUD: MOST PROFIT", 1200, 620, 18, "accent2")},
        {"d": arrow((1360, 560), (700, 380)) , "color": "ink", "width": 4, "kind": "arrow", "start": C("Prime feeds the first two"), "label": lbl("PRIME FEEDS", 1300, 540, 20, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("Prime feeds the first two", 0.2), "dur": 1.4, "target": [940, 760]}],
    "scale": 0.86, "floor": 1040}, sources=["k25"])
kinetic("s25_t3", "m3_transition", [("Keeping members inside…", 60, "Keeping members inside", None, True), ("…hard to leave?", 72, "hard to leave", "risk", False)])

# ====================================================================== PART 4: the Iliad (screens + court)
card("s26_c4", "m4_card", "The Iliad", "The FTC and the cancellation maze")
stage("s27_complaint", "m4_complaint", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It alleged"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("calendar", x=650, y=320, at=0.2, pages=[[0, "JUN", "2023"]], scale=0.75),
              it("docs", x=1050, y=560, at=0.4, text="FTC v. AMAZON", scale=0.7, stamp="COMPLAINT", stampAt=C("sued Amazon")),
              it("letters", x=1550, y=200, text="\"DARK PATTERNS\" (ALLEGED)", at=C("dark patterns"), size=46, color="risk")]},
    sources=["ftc"])
stage("s28_iliad", "m4_iliad", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=120, text="\"ILIAD\" — AMAZON'S NAME FOR THE FLOW (FTC COMPLAINT)", at=C("internal name"), size=40, color="gold"),
              it("flowscreens", x=900, y=470, at=0.3, scale=1.05, gap=250, stepAt=[0.3, C("Cancelling meant"), C("four-page", 0.3), C("six-click")],
                 titles=["Cancel Prime?", "Are you sure?", "Before you go…", "Last chance!"], counter="4 PAGES · 6 CLICKS · 15 OPTIONS", counterAt=C("fifteen-option")),
              it("flowscreens", x=1700, y=780, at=C("Joining took"), scale=0.55, short=True, stepAt=[C("Joining took")], titles=["Join Prime"], counter="1–2 CLICKS", counterAt=C("one or two clicks"))]},
    sources=["ftc"])
stage("s29_settle", "m4_settle", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The settlement also"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("gavel", x=700, y=420, hits=[C("Amazon settled", 0.2)]),
              it("counter", x=1200, y=170, at=C("Amazon settled"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "civil penalty"}, 1.0], [{"cue": "in refunds"}, 2.5]], text="FTC SETTLEMENT, SEPT 2025: PENALTY + REFUNDS"),
              it("letters", x=1250, y=360, text="≈ 35 MILLION CONSUMERS", at=C("thirty-five million"), size=44, color="gold"),
              it("sign", x=1550, y=480, text="CLEAR DECLINE · EASY CANCEL", at=C("The settlement also"), color="#C8E6C9", size=34),
              it("letters", x=1250, y=620, text="ALLEGATIONS · NO ADMISSION", at=C("did not admit"), size=36, color="white")]},
    sources=["ftc", "q3"])
add("p30_doors", "m4_draw", "engine_draw", {
    "title": "Two doors (illustration)", "board": BOARD, "draw_start": C("The way in"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 420, 160, 240), "color": "accent3", "width": 6, "kind": "box", "start": C("The way in"), "label": lbl("WAY IN: 1 CLICK", 660, 400, 22, "accent3")},
        {"d": arrow((760, 540), (900, 540)), "color": "accent3", "width": 5, "kind": "arrow", "start": C("one button")},
        {"d": "M 960 420 L 1120 420 L 1120 520 L 1000 520 L 1000 620 L 1160 620 L 1160 720 L 1040 720 L 1040 800 L 1400 800", "color": "risk", "width": 6, "start": C("The way out"), "label": lbl("WAY OUT: A CORRIDOR", 1180, 400, 22, "risk")},
        {"d": rect(1380, 740, 60, 100), "color": "risk", "width": 5, "kind": "box", "start": C("each one asking"), "label": lbl("EXIT", 1410, 870, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("people stay", 0.1), "dur": 1.4, "target": [1100, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["ftc"])
kinetic("s31_t4", "m4_transition", [("Every summer…", 64, "And every summer", None, False), ("…one giant shopping event", 60, "one giant shopping event", "gold", False)])

# ====================================================================== PART 5: the membership economy (night suburb + parcels)
card("s32_c5", "m5_card", "The Membership Economy", "Prime Day and the habit")
stage("s33_primeday", "m5_primeday", {
    "zones": [Z("sortcenter", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It is so important"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 4,
    "items": [it("calendar", x=720, y=330, at=0.2, pages=[[0, "4 DAYS", "JULY 2025"], [{"cue": "when it moved"}, "JUNE", "2026"]], scale=0.8),
              it("letters", x=1250, y=150, text="\"BIGGEST PRIME DAY EVENT EVER\" (AMAZON)", at=C("biggest Prime Day"), size=42, color="gold"),
              it("sign", x=1500, y=360, text="Q3 → Q2: EXPLAINED TO INVESTORS", at=C("had to explain"), color="#FFE0B2", size=34)]},
    sources=["primeday", "q3"])
stage("s34_bundle", "m5_bundle", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("But it changes behavior"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("home", x=800, at=0.2, scale=0.7, night=True),
              *boxes([600, 680, 760], at=C("then you shop"), scale=0.4),
              it("letters", x=1000, y=150, text="A STORE BECOMES A CLUB", at=C("Prime turns a store"), size=58, color="gold"),
              it("sign", x=1500, y=330, text="PAY FIRST · SHOP AFTER", at=C("You pay first"), color="#BBDEFB", size=38),
              it("sign", x=1550, y=440, text="EVERY VISIT FEEDS THE ADS", at=C("every visit feeds"), color="#FFCDD2", size=34)]},
    sources=["k25"])
add("p35_machine", "m5_draw", "engine_draw", {
    "title": "The Prime machine", "board": BOARD, "draw_start": C("A fee that locks in"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(880, 560, 240, 90), "color": "ink", "width": 6, "kind": "box", "start": C("Let me put the whole"), "label": lbl("YOUR HABIT", 1000, 613, 24, "ink")},
        {"d": rect(560, 360, 220, 80), "color": "accent", "width": 5, "kind": "box", "start": C("A fee that locks in"), "label": lbl("FEE", 670, 408, 22, "accent")},
        {"d": rect(1220, 360, 220, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("Shipping and video"), "label": lbl("SHIPPING + VIDEO", 1330, 408, 20, "accent3")},
        {"d": rect(560, 760, 220, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Advertising that profits"), "label": lbl("ADS", 670, 808, 22, "risk")},
        {"d": rect(1220, 760, 220, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("A cloud business"), "label": lbl("CLOUD CASH", 1330, 808, 22, "accent2")},
        {"d": arrow((780, 430), (880, 570)), "color": "ink", "width": 4, "kind": "arrow", "start": C("A fee that locks in", 0.4)},
        {"d": arrow((1220, 430), (1120, 570)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Shipping and video", 0.4)},
        {"d": arrow((880, 640), (780, 760)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Advertising that profits", 0.4)},
    ],
    "actions": [{"kind": "point", "at": C("And an exit door", 0.2), "dur": 1.4, "target": [1000, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["k25", "ftc"])

# ====================================================================== PAYOFF
stage("s36_payoff", "payoff", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("But what it buys"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("home", x=1000, at=0.2, scale=0.75, night=True),
              van([[0, 2400], [{"cue": "It is the glue"}, 1500]], at=0.2, scale=0.55, text="DELIVERY"),
              it("letters", x=1000, y=130, text="PRIME IS THE GLUE", at=C("It is the glue"), size=64, color="gold"),
              it("letters", x=1000, y=230, text="WHAT AMAZON BUYS: YOUR HABIT", at=C("Your habit"), size=46, color="white")]},
    sources=["k25", "letters"])
add("s37_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_prime_storyboard.py; edit the generator, not this file.\n"
           "# Episode 37 storyboard (Amazon Prime): one visual language per part; tones from visual_direction.yaml.\n")
