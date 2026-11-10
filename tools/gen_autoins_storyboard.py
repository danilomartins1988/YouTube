"""Generates projects/why-your-car-insurance-got-so-expensive/deliverables/documentary/storyboard.yaml (Episode 36,
US batch #10: Why Your Car Insurance Got So Expensive).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: a price screen of the insurance CPI (peak 22.6%) and a generic sedan.
- Part 1 (the bill): the suburb by day, policy price tags, state charts.
- Part 2 (the car itself): the body shop (garage set) and a bumper cutaway full of sensors (new `bumper` item).
- Part 3 (the crashes): the interstate at night (new `highway` set), death-rate charts.
- Part 4 (the courts and the states): courtroom, state capitol, two-driver comparison.
- Part 5 (the insurers' books): combined-ratio screens, profit charts, an evidence board.
No insurer logos or real people; names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_autoins_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-your-car-insurance-got-so-expensive/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.15}, {"at": 1.0, "x": 960, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("tradescreen", x=960, y=470, at=0.05, scale=1.15, text="CAR INSURANCE CPI, 12-MO CHANGE", decimals=1, max=25, min=-8, hot=10, lamp=False, suffix="%",
                 price=[[0, 3.0], [1.2, 9.0], [2.2, 20.3], [3.0, 22.6]]),
              it("letters", x=960, y=120, text="BIGGEST JUMP SINCE 1976", at=C("the biggest jump"), size=60, color="risk")]},
    sources=["bls"])
stage("s02_twist", "h_twist", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And here is the twist"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(800, at=0.2, scale=0.7, color="#1E88E5"),
              it("letters", x=1000, y=170, text="5 YEARS: ≈ +49% (ALL PRICES ≈ +23%)", at=0.4, size=44, color="gold"),
              it("letters", x=1500, y=330, text="2026: STARTING TO FALL", at=C("they have started to fall"), size=52, color="green")]},
    sources=["bls"])
stage("s03_question", "h_question", {
    "zones": [Z("highway", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [car([[0, 300], [8, 1800]], at=0.1, scale=0.6, color="#E53935"),
              it("letters", x=1000, y=150, text="WHO MADE MONEY?", at=0.4, size=80, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE CARS", at=0.3, color="#BBDEFB", size=44),
              it("sign", x=750, y=380, text="2 · THE CRASHES", at=C("the crashes"), color="#FFCDD2", size=44),
              it("sign", x=1170, y=380, text="3 · THE COURTS", at=C("the courts"), color="#FFE0B2", size=44),
              it("sign", x=1590, y=380, text="4 · THE INSURERS", at=C("the insurers' own books"), color="#C8E6C9", size=44),
              it("letters", x=960, y=700, text="FOUR FORCES", at=C("the four forces"), size=72, color="gold")]})

# ====================================================================== PART 1: the bill (suburb + tags + charts)
card("s05_c1", "m1_card", "The Bill", "What drivers actually pay")
stage("s06_naic", "m1_naic", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In twenty twenty, it was"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("home", x=700, at=0.2, scale=0.6),
              car(1150, at=0.3, scale=0.55, color="#43A047"),
              it("counter", x=1500, y=200, at=C("average American household"), prefix="$", suffix="/YR", steps=[[0, 0], [{"cue": "on auto insurance", "offset": 0}, 1431]], text="AVG AUTO INSURANCE SPEND, 2024 (NAIC)"),
              it("letters", x=1550, y=420, text="2020: ≈ $1,048 → +37%", at=C("In twenty twenty, it was"), size=44, color="gold")]},
    sources=["naic"])
stage("s07_states", "m1_states", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "FLORIDA", "value": 2018, "color": "#E53935", "at": 0.5, "display": "$2,018"},
                     {"label": "NEW YORK", "value": 1981, "color": "#FF7043", "at": C("followed by New York"), "display": "$1,981"},
                     {"label": "LOUISIANA", "value": 1880, "color": "#FFB300", "at": C("and Louisiana"), "display": "$1,880"},
                     {"label": "N. DAKOTA", "value": 907, "color": "#43A047", "at": C("The cheapest was"), "display": "$907"}],
                    at=0.2, max=2200, title="AVERAGE YEARLY SPEND BY STATE, 2024 (NAIC)", x=300, w=1080),
              it("letters", x=1650, y=420, text="COMPARE WITH CAUTION", at=C("treated with caution"), size=36, color="risk")]},
    sources=["naic"])
stage("s08_cpi", "m1_cpi", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "CAR INSURANCE", "value": 49.4, "color": "#E53935", "at": C("car insurance prices rose"), "display": "+49%"},
                     {"label": "ALL PRICES", "value": 22.8, "color": "#90A4AE", "at": C("car insurance prices rose", 0.6), "display": "+23%"},
                     {"label": "NEW CARS", "value": 12.2, "color": "#4FC3F7", "at": C("the price of new cars"), "display": "+12%"}],
                    at=0.2, max=55, dark=True, title="CPI, SEP 2021 → SEP 2026 (BLS; OUR CALCULATION)", x=420, w=1080),
              it("letters", x=960, y=470, text="5 YEARS OF PRICES", at=0.3, until=C("car insurance prices rose"), size=84, color="gold")]},
    sources=["bls"])
stage("s09_drop", "m1_drop", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Paying less today"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("person", x=700, pose="worry", at=0.2, scale=0.8, hair=3, skin=1),
              it("docs", x=1100, y=560, at=0.4, text="AUTO POLICY", scale=0.7, stamp="COVERAGE CUT", stampAt=C("Drivers drop coverage")),
              it("pricetag", x=1600, y=320, at=C("raise their deductibles"), text="DEDUCTIBLE ↑", scale=0.9),
              it("letters", x=1300, y=150, text="PAY LESS NOW, RISK MORE LATER", at=C("Paying less today"), size=46, color="gold")]},
    sources=["naicdb"])
add("p10_slices", "m1_draw", "engine_draw", {
    "title": "Inside a premium (schematic)", "board": BOARD, "draw_start": C("A slice to repair"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860", "color": "ink", "width": 4, "start": C("Let me draw what is inside")},
        {"d": "M 600 860 L 600 540 L 760 540 L 760 860", "color": "accent2", "width": 5, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("A slice to repair"), "label": lbl("CAR REPAIRS", 680, 520, 20, "accent2")},
        {"d": "M 820 860 L 820 600 L 980 600 L 980 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("people injured"), "label": lbl("INJURIES", 900, 580, 20, "risk")},
        {"d": "M 1040 860 L 1040 720 L 1200 720 L 1200 860", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.3, "kind": "bar", "start": C("lawyers and claims"), "label": lbl("LEGAL + CLAIMS", 1120, 700, 20, "accent")},
        {"d": "M 1260 860 L 1260 740 L 1420 740 L 1420 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("costs and profit"), "label": lbl("COSTS + PROFIT", 1340, 720, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("When any slice grows", 0.1), "dur": 1.4, "target": [900, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["naic"])
kinetic("s11_t1", "m1_transition", [("The first slice to explode…", 60, "The first slice", None, True), ("…fixing the car", 74, "fixing the car", "gold", False)])

# ====================================================================== PART 2: the car itself (garage + bumper)
card("s12_c2", "m2_card", "The Car Itself", "Used prices, repairs and sensors")
stage("s13_used", "m2_used", {
    "zones": [Z("dealership")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When a car is"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [car(800, at=0.2, scale=0.6, color="#78909C", sticker="USED"),
              it("letters", x=1100, y=180, text="USED CARS +36% (2019–2023, NAIC)", at=C("used vehicle prices rose"), size=46, color="gold"),
              it("docs", x=1650, y=560, at=C("When a car is"), text="TOTAL LOSS", scale=0.6, stamp="PAY CAR'S VALUE", stampAt=C("the insurer pays"))]},
    sources=["naicdb"])
stage("s14_repair", "m2_repair", {
    "zones": [Z("garage")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [car(900, at=0.2, scale=0.7, color="#FB8C00", lift=[[0, 0], [1.5, 0], [3.5, 1]]),
              it("counter", x=1500, y=200, at=0.4, prefix="+", suffix="%", steps=[[0, 0], [{"cue": "forty-six percent", "offset": 0}, 46]], text="CAR REPAIR PRICES, 5 YEARS (BLS; OUR CALCULATION)"),
              it("sign", x=1500, y=420, text="PARTS · PAINT · LABOR", at=C("Parts, paint"), color="#FFE0B2", size=40)]},
    sources=["bls"])
stage("s15_tech", "m2_tech", {
    "zones": [Z("garage")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}], "drift": 1,
    "items": [it("bumper", x=1000, y=520, at=0.2, scale=0.9, openAt=C("Cameras and radar"), pages=[[0, ""], [{"cue": "cost about ten percent more"}, "+≈10% PER CLAIM"]]),
              it("letters", x=1000, y=100, text="HLDI (INSURER-FUNDED)", at=C("Highway Loss"), size=40, color="white")]},
    sources=["iihs"])
stage("s16_safer", "m2_safer", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [car([[0, 300], [10, 1600]], at=0.2, scale=0.45, y=980, color="#1E88E5"),
              chart([{"label": "COLLISION CLAIMS", "value": 10, "color": "#43A047", "at": C("fewer collision claims"), "display": "≈ −10%"},
                     {"label": "PROPERTY-DAMAGE CLAIMS", "value": 40, "color": "#2E7D32", "at": C("almost forty percent"), "display": "≈ −40%"}],
                    at=0.4, max=45, title="CLAIMS WITH DRIVER-ASSIST FEATURES (HLDI)", x=520, y=200, w=880, h=520)]},
    sources=["iihs"])
add("p17_bumper", "m2_draw", "engine_draw", {
    "title": "A modern bumper (illustration)", "board": BOARD, "draw_start": C("On the outside"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 480, 840, 160), "color": "ink", "width": 6, "kind": "box", "start": C("On the outside"), "label": lbl("PLASTIC + PAINT", 1000, 465, 22, "ink")},
        {"d": rect(640, 520, 160, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("a radar unit"), "label": lbl("RADAR", 720, 568, 22, "accent2")},
        {"d": "M 860 520 L 900 520 M 980 520 L 1020 520 M 1100 520 L 1140 520", "color": "accent3", "width": 8, "start": C("sensors"), "label": lbl("SENSORS", 1000, 620, 20, "accent3")},
        {"d": arrow((1200, 460), (1300, 380)), "color": "risk", "width": 4, "kind": "arrow", "start": C("a camera behind"), "label": lbl("CAMERA", 1320, 360, 22, "risk")},
        {"d": "M 600 760 L 760 760 L 760 700 L 920 700 L 920 760 L 1080 760", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.2, "kind": "bar", "start": C("replacing and recalibrating"), "label": lbl("REPAIR BILL ↑", 840, 680, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("A small bump", 0.2), "dur": 1.4, "target": [720, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["iihs"])
kinetic("s18_t2", "m2_transition", [("Then, the crashes…", 64, "Then there were the crashes", None, True), ("…at the worst moment", 64, "the worst possible moment", "risk", False)])

# ====================================================================== PART 3: the crashes (highway at night + charts)
card("s19_c3", "m3_card", "The Crashes", "Deadlier roads")
stage("s20_deaths", "m3_deaths", {
    "zones": [Z("highway", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}, {"at": C("The death rate per mile"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 1.5}], "drift": 3,
    "items": [it("counter", x=1000, y=170, at=0.3, prefix="", suffix="", steps=[[0, 36355], [{"cue": "in twenty twenty-one", "offset": 0}, 43230]], text="U.S. ROAD DEATHS, 2019 → 2021 (FARS VIA IIHS)", scale=1.1),
              it("letters", x=1650, y=360, text="DEATHS PER 100M MILES: 1.11 → 1.38", at=C("The death rate per mile"), size=40, color="gold")]},
    sources=["iihs"])
stage("s21_speed", "m3_speed", {
    "zones": [Z("highway", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}], "drift": 6,
    "items": [car([[0, 0], [5, 2400]], at=0.2, scale=0.55, color="#E53935"),
              it("counter", x=1000, y=170, at=0.4, prefix="", suffix="%", steps=[[0, 0], [{"cue": "a factor in twenty-nine", "offset": 0}, 29]], text="CRASH DEATHS WHERE SPEEDING WAS A FACTOR, 2024 (IIHS)"),
              it("sign", x=1000, y=380, text="INJURIES · HOSPITAL BILLS · BIGGER CLAIMS", at=C("Faster crashes"), color="#FFCDD2", size=36)]},
    sources=["iihs"])
stage("s22_better", "m3_better", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2019", "value": 36355, "color": "#90A4AE", "at": 0.4, "display": "36,355"},
                     {"label": "2021", "value": 43230, "color": "#E53935", "at": 0.8, "display": "43,230"},
                     {"label": "2024", "value": 39254, "color": "#FFB300", "at": C("Deaths fell to"), "display": "39,254"}],
                    at=0.2, max=46000, title="U.S. ROAD DEATHS (FARS VIA IIHS)", x=420, w=1080)]},
    sources=["iihs"])
stage("s23_uninsured", "m3_uninsured", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When they cause"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [*[car(500 + 200 * k, at=0.2 + 0.1 * k, scale=0.32, color="#90A4AE" if k != 3 else "#E53935") for k in range(7)],
              it("letters", x=1000, y=170, text="≈ 1 IN 7 DRIVERS UNINSURED (IRC, 2023)", at=C("about one in seven"), size=44, color="gold"),
              it("letters", x=1250, y=300, text="→ COST LANDS ON INSURED DRIVERS", at=C("When they cause"), size=40, color="risk")]},
    sources=["irc"])
add("p24_rate", "m3_draw", "engine_draw", {
    "title": "Deaths per 100 million miles (schematic)", "board": BOARD, "draw_start": C("Here is twenty nineteen"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Let me draw the death rate")},
        {"d": "M 600 700 L 760 700", "color": "accent3", "width": 7, "start": C("Here is twenty nineteen"), "label": lbl("2019: 1.11", 680, 680, 20, "accent3")},
        {"d": "M 760 700 L 920 520 L 1000 500", "color": "risk", "width": 8, "start": C("a sharp climb"), "label": lbl("2021: 1.38", 980, 480, 20, "risk")},
        {"d": "M 1000 500 L 1440 620", "color": "accent", "width": 7, "start": C("a slow decline"), "label": lbl("2024: 1.19", 1400, 600, 20, "accent")},
        {"d": "M 1400 860 L 1400 620 L 1440 620 L 1440 860", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.2, "kind": "bar", "start": C("has not returned")},
    ],
    "actions": [{"kind": "point", "at": C("Insurers price", 0.1), "dur": 1.4, "target": [980, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["iihs"])
kinetic("s25_t3", "m3_transition", [("After the crash, the claim…", 60, "After the crash", None, True), ("…and sometimes, court", 64, "the claim goes to court", "gold", False)])

# ====================================================================== PART 4: the courts and the states (court + capitol)
card("s26_c4", "m4_card", "The Courts and the States", "Lawsuits, laws and rating rules")
stage("s27_legal", "m4_legal", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The insurance industry blames"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [chart([{"label": "LEGAL SERVICES", "value": 20.88, "color": "#E53935", "at": C("the price of legal services"), "display": "+21%"},
                     {"label": "MEDICAL CARE", "value": 8.5, "color": "#90A4AE", "at": C("more than double the rise"), "display": "+8.5%"}],
                    at=0.3, max=25, title="CPI 2019→2023 (NAIC REPORT)", x=380, y=200, w=720, h=480),
              it("pinboard", cards=[{"x": 1650, "y": 360, "text": "\"LEGAL SYSTEM ABUSE\"", "sub": "insurance industry's framing (Triple-I/CAS)", "at": C("The insurance industry blames"), "w": 520, "color": "#FFF59D", "size": 34}])]},
    sources=["naicdb", "iii"])
stage("s28_florida", "m4_florida", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Three years later"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.2, text="FLORIDA HB 837", scale=0.7, stamp="SIGNED MAR 2023", stampAt=C("changed its laws")),
              it("sign", x=1350, y=230, text="ONE-WAY ATTORNEY FEES: REPEALED", at=C("repealed one-way"), color="#BBDEFB", size=34),
              it("sign", x=1350, y=330, text="TIME TO SUE: 4 → 2 YEARS", at=C("cut the time to file"), color="#BBDEFB", size=34),
              it("letters", x=1450, y=470, text="STATE: LOSS RATIO 112% → < 50%", at=C("the state says loss ratios"), size=38, color="gold"),
              it("letters", x=1450, y=560, text="RATE CUTS ≈ −8% SIGNALED (2026)", at=C("signaling rate cuts"), size=38, color="green")]},
    sources=["flhb", "flcfo"])
stage("s29_rules", "m4_rules", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Elsewhere"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("letters", x=1000, y=130, text="STATES SET THE PRICING RULES", at=0.3, size=54, color="gold"),
              it("sign", x=760, y=280, text="CALIFORNIA: RECORD · MILES · EXPERIENCE", at=C("In California"), color="#C8E6C9", size=32),
              it("counter", x=1400, y=230, at=C("Elsewhere"), prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "of auto insurers use", "offset": 0}, 95]], text="AUTO INSURERS USING CREDIT SCORES WHERE ALLOWED (NAIC)"),
              it("sign", x=1100, y=480, text="HAWAII · MASSACHUSETTS: NO CREDIT-BASED RATES", at=C("Hawaii and Massachusetts"), color="#FFE0B2", size=32)]},
    sources=["cdi", "naiccredit"])
add("p30_twins", "m4_draw", "engine_draw", {
    "title": "Same driver, different state (illustration)", "board": BOARD, "draw_start": C("two drivers with the same car"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(580, 420, 300, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("two drivers with the same car"), "label": lbl("DRIVER A", 730, 488, 26, "accent2")},
        {"d": rect(1120, 420, 300, 120), "color": "accent", "width": 6, "kind": "box", "start": C("the same clean record"), "label": lbl("DRIVER B", 1270, 488, 26, "accent")},
        {"d": arrow((730, 560), (730, 680)), "color": "accent2", "width": 5, "kind": "arrow", "start": C("allows credit scores"), "label": lbl("CREDIT SCORE USED", 730, 720, 20, "accent2")},
        {"d": arrow((1270, 560), (1270, 680)), "color": "accent", "width": 5, "kind": "arrow", "start": C("the other does not"), "label": lbl("NOT ALLOWED", 1270, 720, 20, "accent")},
        {"d": "M 1000 400 L 1000 760", "color": "risk", "width": 4, "start": C("different price"), "label": lbl("≠ PRICE", 1000, 380, 26, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("different price", 0.2), "dur": 1.4, "target": [1000, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["naiccredit"])
kinetic("s31_t4", "m4_transition", [("The companies in the middle…", 60, "Which brings us", None, True), ("victims or winners?", 70, "or the winners", "gold", False)])

# ====================================================================== PART 5: the insurers' books (screens + charts)
card("s32_c5", "m5_card", "The Insurers' Books", "From losses to record profits")
stage("s33_loss", "m5_loss", {
    "zones": [Z("exchange")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("tradescreen", x=1000, y=470, at=0.3, scale=1.1, text="ALLSTATE AUTO COMBINED RATIO (10-K)", decimals=1, max=115, min=75, hot=100, lamp=False, suffix="",
                 price=[[0, 95], [{"cue": "Above one hundred"}, 100], [{"cue": "auto combined ratio was"}, 110.1]]),
              it("letters", x=1000, y=110, text="ABOVE 100 = LOSING MONEY ON POLICIES", at=C("Above one hundred"), size=44, color="risk")]},
    sources=["allstate"])
stage("s34_rates", "m5_rates", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=140, text="THEN: RAISE PRICES, HARD", at=0.3, size=56, color="gold"),
              it("pricetag", x=480, y=330, at=C("about thirteen percent"), text="2022: +13%", scale=1.0),
              it("pricetag", x=960, y=330, at=C("about nineteen percent"), text="2023: +19%", scale=1.0),
              it("letters", x=720, y=580, text="PROGRESSIVE, PERSONAL AUTO", at=C("Progressive says"), size=36, color="white"),
              it("pricetag", x=1520, y=330, at=C("Allstate took rate increases"), text="+17.9%", scale=1.0),
              it("letters", x=1500, y=580, text="ALLSTATE BRAND, 55 LOCATIONS (2023)", at=C("fifty-five locations"), size=30, color="white")]},
    sources=["progressive", "allstate"])
stage("s35_profit", "m5_profit", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "ALLSTATE 2022", "value": -1.39, "color": "#E53935", "at": 0.4, "display": "−$1.39bn"},
                     {"label": "ALLSTATE 2025", "value": 10.17, "color": "#43A047", "at": C("its net income"), "display": "$10.17bn", "sub": "incl. business sales"},
                     {"label": "PROGRESSIVE 2022", "value": 0.722, "color": "#90A4AE", "at": C("Progressive's net income"), "display": "$0.72bn"},
                     {"label": "PROGRESSIVE 2025", "value": 11.3, "color": "#2E7D32", "at": C("in twenty twenty-five."), "display": "$11.3bn"}],
                    at=0.2, max=12, min=-3, dark=True, title="NET INCOME (SEC FILINGS)", x=300, w=1300)]},
    sources=["allstate", "progressive"])
stage("s36_refund", "m5_refund", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("And this year"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 650, "y": 380, "text": "FLORIDA PROFIT CAP", "sub": "profits exceeded the statutory limit", "at": 0.3, "w": 480, "color": "#FFF59D", "size": 40},
                {"x": 1550, "y": 380, "text": "$1.22BN", "sub": "credits to policyholders (Progressive)", "at": C("one point two two billion"), "w": 440, "color": "#C8E6C9", "size": 58},
                {"x": 1100, "y": 680, "text": "PREMIUMS EASING", "sub": "avg personal auto premium per policy falling (2026)", "at": C("And this year"), "w": 520, "color": "#BBDEFB", "size": 44}],
              links=[[0, 1, C("one point two two billion", 0.4)], [1, 2, C("And this year", 0.4)]])]},
    sources=["progressive"])
add("p37_cycle", "m5_draw", "engine_draw", {
    "title": "The insurance cycle", "board": BOARD, "draw_start": C("Costs rise faster"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(880, 360, 240, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Costs rise faster"), "label": lbl("LOSSES", 1000, 408, 24, "risk")},
        {"d": rect(1220, 540, 240, 80), "color": "accent", "width": 5, "kind": "box", "start": C("Insurers raise prices"), "label": lbl("PRICES ↑↑", 1340, 588, 24, "accent")},
        {"d": rect(880, 720, 240, 80), "color": "accent3", "width": 5, "kind": "box", "start": C("profits soar"), "label": lbl("PROFITS", 1000, 768, 24, "accent3")},
        {"d": rect(540, 540, 240, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("push prices back down"), "label": lbl("PRICES ↓", 660, 588, 24, "accent2")},
        {"d": arrow((1120, 420), (1260, 530)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Insurers raise prices", 0.3)},
        {"d": arrow((1300, 630), (1120, 740)), "color": "ink", "width": 4, "kind": "arrow", "start": C("profits soar", 0.3)},
        {"d": arrow((880, 750), (720, 630)), "color": "ink", "width": 4, "kind": "arrow", "start": C("push prices back down", 0.3)},
        {"d": arrow((700, 530), (880, 420)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Drivers live through")},
    ],
    "actions": [{"kind": "point", "at": C("Drivers live through", 0.2), "dur": 1.4, "target": [1340, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["allstate", "progressive"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("highway", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": C("Prices are finally easing"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 4,
    "items": [car([[0, 200], [12, 1900]], at=0.2, scale=0.6, color="#1E88E5"),
              it("letters", x=1000, y=130, text="CARS · CRASHES · COURTS · INSURERS", at=0.4, size=50, color="gold"),
              it("letters", x=1000, y=230, text="EASING NOW, STILL FAR ABOVE 2021", at=C("Prices are finally easing"), size=44, color="white")]},
    sources=["bls", "allstate", "progressive"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_autoins_storyboard.py; edit the generator, not this file.\n"
           "# Episode 36 storyboard (car insurance): one visual language per part; tones from visual_direction.yaml.\n")
