"""Generates projects/why-the-post-office-keeps-losing-billions/deliverables/documentary/storyboard.yaml
(Episode 47, new topics N7: Why the Post Office Keeps Losing Billions).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the post office lobby (new `postoffice` set) with a giant counter; the suburb route with a delivery van.
- Part 1 (the network): the suburb route, the sort center, a fixed-route drawing.
- Part 2 (the 2006 law): Congress, the office at night, a retiree-fund drawing.
- Part 3 (the vanishing letter): the post office, the studio charts, a two-lines drawing.
- Part 4 (the plan): the sort center at night, the studio charts, a revenue/cost gap drawing.
- Part 5 (running out of room): the office, Congress at night, a four-walls drawing.
No logos or eagle emblems, no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_postal_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-the-post-office-keeps-losing-billions/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}


def chart(bars_, at=0.2, **kw):
    return it("bigchart", x=kw.pop("x", 300), y=kw.pop("y", 200), w=kw.pop("w", 1320), h=kw.pop("h", 560), bars=bars_, at=at, **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("postoffice")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=170, at=0.05, prefix="≈ $", suffix="BN", steps=[[0.05, 0], [1.5, 118]], text="POSTAL SERVICE NET LOSSES SINCE 2006 (GAO)", scale=1.4)]},
    sources=["gao"])
stage("s02_twist", "h_twist", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.0}], "drift": 2,
    "items": [it("van", x=[[0, -300], [8, 2400]], at=0.2, text="U.S. MAIL"),
              it("sign", x=600, y=200, text="2024: −$9.5BN", at=C("in\n    twenty twenty-four") if False else C("twenty twenty-four"), color="#FFCDD2", size=38),
              it("sign", x=1000, y=200, text="2025: −$9.0BN", at=C("twenty twenty-five"), color="#FFCDD2", size=38),
              it("sign", x=1400, y=200, text="2026: −$6.5BN", at=C("a loss of"), color="#FFE0B2", size=38)]},
    sources=["usps25", "usps26"])
stage("s03_question", "h_question", {
    "zones": [Z("postoffice", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="EVERY ADDRESS. ALWAYS A LOSS. WHY?", at=0.3, size=58, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · WHAT THE LAW REQUIRES", at=C("has to do by law"), color="#BBDEFB", size=30),
              it("sign", x=960, y=380, text="2 · THE 2006 BILL", at=C("a law from twenty oh six"), color="#FFE0B2", size=32),
              it("sign", x=1560, y=380, text="3 · THE VANISHING LETTER", at=C("why the letter"), color="#C8E6C9", size=30),
              it("letters", x=960, y=700, text="FOLLOW THE STAMP", at=0.4, size=72, color="gold")]})

# ====================================================================== PART 1: the network
card("s05_c1", "m1_card", "The Network", "Every address, six days a week")
stage("s06_scale", "m1_scale", {
    "zones": [Z("suburb")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Every new house"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.3, prefix="", suffix="M+", steps=[[0, 0], [{"cue": "addresses"}, 170]], text="ADDRESSES SERVED (USPS)", scale=1.2),
              it("sign", x=1500, y=360, text="+1.8M NEW ADDRESSES IN 2025", at=C("one point eight million"), color="#FFE0B2", size=34),
              it("van", x=[[0, 2600], [10, -400]], at=0.4, text="U.S. MAIL", scale=0.8)]},
    sources=["hist"])
stage("s07_fleet", "m1_fleet", {
    "zones": [Z("sortcenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Every one of those"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="THE MACHINE BEHIND IT (USPS)", at=0.3, size=50, color="gold"),
              it("sign", x=600, y=250, text="≈ 236,000 ROUTES", at=C("delivery routes"), color="#BBDEFB", size=36),
              it("sign", x=1050, y=250, text="≈ 31,000 OFFICES", at=C("retail offices"), color="#FFE0B2", size=36),
              it("sign", x=1500, y=250, text="260,000+ VEHICLES", at=C("vehicles"), color="#C8E6C9", size=36)]},
    sources=["hist"])
stage("s08_tax", "m1_tax", {
    "zones": [Z("postoffice")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It is supposed to pay"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=130, text="WHO PAYS FOR IT?", at=0.3, until=C("generally receives no tax"), size=56, color="gold"),
              it("letters", x=1000, y=130, text="'GENERALLY RECEIVES NO TAX DOLLARS FOR OPERATING EXPENSES'", at=C("generally receives no tax"), size=36, color="gold"),
              it("sign", x=1250, y=290, text="STAMPS · PACKAGES · MAIL FEES", at=C("It is supposed to pay"), color="#BBDEFB", size=36)]},
    sources=["usps26"])
stage("s09_law", "m1_law", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That promise is called"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="BY LAW: AT LEAST 6 DAYS A WEEK", at=C("By law"), size=52, color="gold"),
              it("van", x=[[0, -300], [9, 2400]], at=0.3, text="U.S. MAIL", scale=0.8),
              it("sign", x=1250, y=280, text="'UNIVERSAL SERVICE'", at=C("That promise is called"), color="#FFE0B2", size=42)]},
    sources=["laws"])
stage("s10_cost", "m1_cost", {
    "zones": [Z("suburb", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The network is fixed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("van", x=[[0, -300], [9, 2400]], at=0.2, text="U.S. MAIL", scale=0.8),
              it("sign", x=800, y=230, text="50 LETTERS OR 5: SAME ROUTE", at=C("whether the bag holds"), color="#BBDEFB", size=34),
              it("letters", x=1250, y=380, text="FIXED NETWORK · SHRINKING REVENUE", at=C("The network is fixed"), size=44, color="gold")]})
add("p11_route", "m1_draw", "engine_draw", {
    "title": "One route (illustration)", "board": BOARD, "draw_start": C("Here is a route with ten houses"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 720 640 L 1480 640", "color": "ink", "width": 5, "kind": "stroke", "start": C("Here is a route with ten houses"), "label": lbl("THE ROUTE", 1100, 690, 22, "ink")},
        {"d": " ".join(f"M {740 + k * 80} 600 L {770 + k * 80} 570 L {800 + k * 80} 600 L {800 + k * 80} 630 L {740 + k * 80} 630 Z" for k in range(10)), "color": "accent2", "width": 4, "kind": "stroke", "start": C("Here is a route with ten houses", 0.6)},
        {"d": "M 760 520 L 760 560 M 840 520 L 840 560 M 920 520 L 920 560 M 1000 520 L 1000 560 M 1080 520 L 1080 560", "color": "accent", "width": 6, "start": C("Each day, the carrier"), "label": lbl("LETTERS", 760, 500, 20, "accent")},
        {"d": "M 1160 545 L 1160 560 M 1320 545 L 1320 560", "color": "risk", "width": 6, "start": C("Now the letters fall"), "label": lbl("HALF THE LETTERS", 1300, 500, 20, "risk")},
        {"d": "M 720 740 L 1480 740", "color": "muted", "width": 3, "start": C("The route stays the same"), "label": lbl("SAME TRUCK · SAME MILES · SAME TIME", 1100, 780, 20, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Fewer letters to pay", 0.1), "dur": 1.4, "target": [1240, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["hist"])
kinetic("s12_t1", "m1_transition", [("That alone would be hard…", 66, "That alone", None, False),
                                    ("…then came 2006", 72, "something much bigger", "gold", False)])

# ====================================================================== PART 2: the 2006 law
card("s13_c2", "m2_card", "The 2006 Law", "A bill for future retirees")
stage("s14_prefund", "m2_prefund", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our sum"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="POSTAL ACCOUNTABILITY AND ENHANCEMENT ACT (2006)", at=0.3, size=40, color="gold"),
              it("sign", x=800, y=250, text="≈ $5.5BN A YEAR · 10 YEARS", at=C("for ten years"), color="#FFE0B2", size=36),
              it("counter", x=1500, y=280, at=C("By our sum"), prefix="≈ $", suffix="BN", steps=[[0, 0], [{"cue": "over the decade"}, 56]], text="TOTAL (OUR SUM)")]},
    sources=["laws"])
stage("s15_rare", "m2_rare", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Postal Service soon stopped"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="FIXED IN THE LAW, WHATEVER HAPPENED", at=0.3, size=48, color="gold"),
              it("docs", x=700, y=560, at=C("The Postal Service soon stopped"), text="PREFUNDING PAYMENTS", scale=0.7, stamp="MISSED", stampAt=C("the missed payments")),
              it("sign", x=1400, y=300, text="MISSED PAYMENTS → BOOKED AS LOSSES", at=C("kept piling up"), color="#FFCDD2", size=32)]},
    sources=["laws", "gao"])
stage("s16_reform", "m2_reform", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it wrote"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="POSTAL SERVICE REFORM ACT (2022)", at=0.3, size=50, color="gold"),
              it("sign", x=700, y=250, text="$57BN OF MISSED PAYMENTS CANCELED", at=C("canceled"), color="#C8E6C9", size=30),
              it("sign", x=1250, y=350, text="MEDICARE: −$61BN RETIREE HEALTH BILL", at=C("moved postal retirees"), color="#BBDEFB", size=30),
              it("sign", x=1700, y=250, text="6-DAY DELIVERY IN THE LAW", at=C("And it wrote"), color="#FFE0B2", size=30)]},
    sources=["gao", "laws"])
stage("s17_still", "m2_still", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The government's auditors expect"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="THE BILLS DID NOT END", at=0.3, size=56, color="gold"),
              it("sign", x=800, y=260, text="TOP-UPS: ≈ $750M (2026) → ≈ $1.4BN (2031)", at=C("seven hundred and fifty"), color="#FFE0B2", size=30),
              it("sign", x=1400, y=380, text="HEALTH FUND EMPTY BY FY2031 (GAO)", at=C("The government's auditors expect"), color="#FFCDD2", size=32)]},
    sources=["gao"])
add("p18_fund", "m2_draw", "engine_draw", {
    "title": "The retiree bill (illustration)", "board": BOARD, "draw_start": C("Here is the Postal Service"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 460, 240, 100), "color": "accent2", "width": 5, "kind": "box", "start": C("Here is the Postal Service"), "label": lbl("POSTAL SERVICE", 680, 518, 22, "accent2")},
        {"d": rect(1120, 460, 260, 100), "color": "accent3", "width": 5, "kind": "box", "start": C("Here is the fund"), "label": lbl("RETIREE FUND", 1250, 518, 22, "accent3")},
        {"d": arrow((805, 495), (1115, 495)), "color": "accent", "width": 12, "kind": "arrow", "start": C("a big arrow of"), "label": lbl("≈ $5.5BN / YEAR", 960, 470, 20, "accent")},
        {"d": "M 900 600 L 900 760 L 1040 760 L 1040 600", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("When the arrow stopped"), "label": lbl("DEBT", 970, 800, 22, "risk")},
        {"d": "M 880 680 L 1060 680", "color": "ink", "width": 5, "start": C("Congress erased"), "label": lbl("2022: ERASED", 1150, 690, 18, "ink")},
        {"d": arrow((805, 540), (1115, 540)), "color": "accent", "width": 4, "kind": "arrow", "start": C("a smaller arrow")},
    ],
    "actions": [{"kind": "point", "at": C("a smaller arrow", 0.2), "dur": 1.4, "target": [960, 540]}],
    "scale": 0.86, "floor": 1040}, sources=["laws", "gao"])
kinetic("s19_t2", "m2_transition", [("The retiree bills explain part…", 60, "explain part", None, False),
                                    ("…the rest is in your mailbox", 62, "your own mailbox", "gold", False)])

# ====================================================================== PART 3: the vanishing letter
card("s20_c3", "m3_card", "The Vanishing Letter", "First-Class Mail since 2001")
stage("s21_peak", "m3_peak", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2001", "value": 103.7, "color": "#90A4AE", "at": C("peaked in twenty oh one"), "display": "103.7BN"},
                     {"label": "2026", "value": 39.9, "color": "#E53935", "at": C("In twenty twenty-six"), "display": "39.9BN"}],
                    at=0.2, max=120, title="FIRST-CLASS MAIL PIECES (USPS)", x=300, w=800),
              it("letters", x=1520, y=360, text="ALL MAIL PEAKED 2006: 213BN+ (GAO)", at=C("Counting every kind"), size=32, color="gold")]},
    sources=["hist", "usps26", "gao"])
stage("s22_perstop", "m3_perstop", {
    "zones": [Z("suburb")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="MAIL PER ADDRESS, PER DAY (USPS)", at=0.3, size=48, color="gold"),
              it("counter", x=700, y=280, at=C("In twenty oh seven"), prefix="", suffix="", decimals=1, steps=[[0, 0], [{"cue": "five and a half"}, 5.5]], text="2007"),
              it("counter", x=1300, y=280, at=C("In twenty twenty-six"), prefix="", suffix="", decimals=1, steps=[[0, 0], [{"cue": "two point three"}, 2.3]], text="2026")]},
    sources=["usps26"])
stage("s23_packages", "m3_packages", {
    "zones": [Z("sortcenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But packages are"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="THE BRIGHT SPOT: PACKAGES", at=0.3, size=50, color="gold"),
              it("sign", x=750, y=200, text="PACKAGES: $34.1BN", at=C("shipping and packages brought"), color="#C8E6C9", size=38),
              it("sign", x=750, y=300, text="FIRST-CLASS MAIL: $26.2BN", at=C("from First-Class Mail"), color="#FFE0B2", size=34),
              it("sign", x=1500, y=250, text="GROUND ADVANTAGE DROVE 2025 GROWTH", at=C("Ground Advantage"), color="#BBDEFB", size=30),
              it("letters", x=1250, y=420, text="A COMPETITIVE BUSINESS", at=C("But packages are"), size=46, color="gold")]},
    sources=["usps26", "usps25"])
stage("s24_stamp", "m3_stamp", {
    "zones": [Z("postoffice")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("counter", x=1000, y=230, at=0.3, prefix="", suffix="¢", steps=[[0, 55], [{"cue": "it costs"}, 82]], text="FOREVER STAMP (USPS RATE HISTORY)", scale=1.3),
              it("sign", x=1000, y=480, text="≈ +49% IN SEVEN YEARS (OUR CALCULATION)", at=C("By our calculation"), color="#FFE0B2", size=34)]},
    sources=["hist"])
add("p25_lines", "m3_draw", "engine_draw", {
    "title": "Two lines (USPS data, simplified)", "board": BOARD, "draw_start": C("Here is the letter line"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 720 860 L 1480 860", "color": "ink", "width": 4, "start": C("Let me draw the two lines"), "label": lbl("2001 → 2026", 1100, 900, 22, "ink")},
        {"d": "M 740 420 C 900 440 1000 560 1150 650 S 1400 760 1470 780", "color": "accent2", "width": 7, "kind": "stroke", "start": C("Here is the letter line"), "label": lbl("LETTERS", 800, 400, 22, "accent2")},
        {"d": "M 740 800 C 1000 790 1200 700 1300 600 S 1430 480 1470 440", "color": "risk", "width": 7, "kind": "stroke", "start": C("Here is the stamp price line"), "label": lbl("STAMP PRICE", 1420, 420, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("raising the price only", 0.1), "dur": 1.4, "target": [1300, 620]}],
    "scale": 0.86, "floor": 1040}, sources=["hist"])
kinetic("s26_t3", "m3_transition", [("In 2021…", 76, "In twenty twenty-one", None, False),
                                    ("…a plan to turn it around", 66, "turn all of this around", "gold", False)])

# ====================================================================== PART 4: the plan
card("s27_c4", "m4_card", "The Plan", "Delivering for America, 2021")
stage("s28_promise", "m4_promise", {
    "zones": [Z("sortcenter", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It also promised"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="'DELIVERING FOR AMERICA' (USPS, 2021)", at=0.3, size=48, color="gold"),
              it("sign", x=700, y=250, text="BREAK EVEN BY FY2023", at=C("break even"), color="#C8E6C9", size=36),
              it("sign", x=1200, y=350, text="AVOID $160BN OF LOSSES", at=C("and to avoid"), color="#BBDEFB", size=34),
              it("sign", x=1650, y=250, text="$40BN INVESTMENT · 95% ON TIME", at=C("It also promised"), color="#FFE0B2", size=30)]},
    sources=["dfa"])
stage("s29_result", "m4_result", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "REVENUE VS PLAN", "value": 24, "color": "#43A047", "at": C("revenue was"), "display": "+$24BN"},
                     {"label": "COSTS VS PLAN", "value": 36, "color": "#E53935", "at": C("But expenses were"), "display": "+$36BN"}],
                    at=0.2, max=40, title="FY2021–2024, ACTUAL VS THE PLAN (GAO)", x=300, w=800),
              it("letters", x=1520, y=380, text="BREAK-EVEN NEVER CAME", at=0.3, size=46, color="gold")]},
    sources=["gao"])
stage("s30_better", "m4_better", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The loss the Postal Service"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="READ THE FINE PRINT", at=0.3, size=56, color="gold"),
              it("sign", x=800, y=260, text="WORKERS' COMP ACCOUNTING: −$2.4BN SWING", at=C("That one line swung"), color="#BBDEFB", size=30),
              it("sign", x=1450, y=370, text="CONTROLLABLE LOSS: $2.4BN (2026) · $2.7BN (2025)", at=C("The loss the Postal Service"), color="#FFCDD2", size=28)]},
    sources=["usps26", "usps25"])
add("p31_gap", "m4_draw", "engine_draw", {
    "title": "The gap (GAO, simplified)", "board": BOARD, "draw_start": C("Here is the revenue the plan"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1400 860", "color": "ink", "width": 4, "start": C("Let me draw the gap")},
        {"d": "M 600 860 L 600 520 L 720 520 L 720 860", "color": "muted", "width": 4, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the revenue the plan"), "label": lbl("REVENUE: PLAN", 660, 500, 18, "muted")},
        {"d": "M 760 860 L 760 490 L 880 490 L 880 860", "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is what actually came in"), "label": lbl("ACTUAL", 820, 470, 18, "accent3")},
        {"d": "M 1000 860 L 1000 520 L 1120 520 L 1120 860", "color": "muted", "width": 4, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Now here\n    are the expected costs") if False else C("are the expected costs"), "label": lbl("COSTS: PLAN", 1060, 500, 18, "muted")},
        {"d": "M 1160 860 L 1160 400 L 1280 400 L 1280 860", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("the real costs"), "label": lbl("ACTUAL", 1220, 380, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the costs grew even faster", 0.1), "dur": 1.4, "target": [1220, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["gao"])
kinetic("s32_t4", "m4_transition", [("The most serious problem…", 62, "most serious problem", None, False),
                                    ("…no more room to borrow", 64, "running out of room", "gold", False)])

# ====================================================================== PART 5: running out of room
card("s33_c5", "m5_card", "Running Out of Room", "Debt at the legal limit")
stage("s34_cap", "m5_cap", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("counter", x=1000, y=250, at=C("only up to a legal limit"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "That limit has not"}, 15.0]], text="BORROWING LIMIT (UNCHANGED SINCE 1992)", scale=1.3),
              it("letters", x=1000, y=110, text="BORROWING FROM THE TREASURY", at=0.3, size=48, color="gold"),
              it("sign", x=1000, y=450, text="ALREADY AT THE LIMIT", at=C("already reached it"), color="#FFCDD2", size=40)]},
    sources=["usps26"])
stage("s35_skip", "m5_skip", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And in its own words"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="2026: SKIPPING BILLS", at=0.3, size=56, color="gold"),
              it("sign", x=700, y=250, text="PENSION PAYMENTS: NOT MADE (WAIVER)", at=C("it did not make"), color="#FFE0B2", size=30),
              it("sign", x=1300, y=350, text="EMPLOYER CONTRIBUTIONS PAUSED", at=C("It paused"), color="#BBDEFB", size=30),
              it("sign", x=1700, y=250, text="'DEFAULTED' ON $726M", at=C("And in its own words"), color="#FFCDD2", size=34)]},
    sources=["usps26"])
stage("s36_hole", "m5_hole", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "UNFUNDED PENSIONS", "value": 97.1, "color": "#E53935", "at": C("The Postal Service reports"), "display": "$97.1BN"},
                     {"label": "UNFUNDED RETIREE HEALTH", "value": 44.1, "color": "#FB8C00", "at": C("forty-four billion"), "display": "$44.1BN"}],
                    at=0.2, max=110, dark=True, title="LONG-TERM GAPS, FY2026 (USPS)", x=300, w=800),
              it("letters", x=1520, y=380, text="GAO HIGH-RISK LIST SINCE 2009", at=C("high-risk list"), size=34, color="gold")]},
    sources=["usps26", "gao"])
add("p37_walls", "m5_draw", "engine_draw", {
    "title": "The squeeze", "board": BOARD, "draw_start": C("On one side, a fixed network"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(1000, 520, 200, 140), "color": "accent2", "width": 5, "kind": "box", "start": C("Let me draw the squeeze"), "label": lbl("USPS", 1100, 600, 26, "accent2")},
        {"d": "M 900 480 L 900 700", "color": "ink", "width": 8, "start": C("On one side, a fixed network"), "label": lbl("FIXED NETWORK", 820, 470, 18, "ink")},
        {"d": "M 1300 480 L 1300 700", "color": "accent", "width": 8, "start": C("letters that keep falling"), "label": lbl("FEWER LETTERS", 1380, 470, 18, "accent")},
        {"d": "M 900 460 L 1300 460", "color": "risk", "width": 8, "start": C("On top, retiree bills"), "label": lbl("RETIREE BILLS", 1100, 440, 18, "risk")},
        {"d": "M 900 720 L 1300 720", "color": "muted", "width": 8, "start": C("And underneath"), "label": lbl("$15BN DEBT CAP", 1100, 760, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Four walls", 0.1), "dur": 1.4, "target": [1100, 590]}],
    "scale": 0.86, "floor": 1040}, sources=["usps26", "gao"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("postoffice", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("It must reach every address"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=110, text="RUN LIKE A BUSINESS · SERVE LIKE A UTILITY", at=0.3, size=50, color="gold"),
              it("sign", x=1000, y=250, text="WHO PAYS FOR THE PROMISE? CONGRESS HASN'T DECIDED", at=C("Until Congress decides"), color="#FFCDD2", size=30)]},
    sources=["gao", "usps26"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_postal_storyboard.py; edit the generator, not this file.\n"
           "# Episode 47 storyboard (Postal Service): one visual language per part; tones from visual_direction.yaml.\n")
