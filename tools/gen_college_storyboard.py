"""Generates projects/college-sports-just-got-a-20-million-payroll/deliverables/documentary/storyboard.yaml
(Episode 49, new topics N9: College Sports Just Got a $20.5 Million Payroll).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the stadium at night with a giant counter; the campus.
- Part 1 (the settlement): the courtroom, the studio, a revenue-pie drawing.
- Part 2 (year one): the stadium by day, the skyline (TV money), a budget drawing.
- Part 3 (fewer seats): the team bench (new `bench` item), the campus, a bench drawing.
- Part 4 (the referee): the office, the airport-style checkpoint, a checkpoint drawing.
- Part 5 (students or employees): the court, Congress, a two-doors drawing.
No school, league or conference logos (names in text only), no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_college_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/college-sports-just-got-a-20-million-payroll/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("stadium", night=True, label="HOME 21 – 17 AWAY")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=220, at=0.05, prefix="$", suffix="M", decimals=1, steps=[[0.05, 0], [1.5, 20.5]], text="MAX PAID BY EACH SCHOOL TO ITS ATHLETES, 2025-26 (CSC)", scale=1.4)]},
    sources=["csc"])
stage("s02_twist", "h_twist", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("In its first year"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="A CENTURY OF 'AMATEURS'", at=0.3, size=58, color="gold"),
              it("counter", x=1200, y=300, at=C("In its first year"), prefix="≈ $", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "to athletes"}, 1.77]], text="REVENUE SHARING PAID IN YEAR ONE (CSC)", scale=1.1),
              *crowd([500, 1500], "walk", at=0.3, scale=0.7)]},
    sources=["csc"])
stage("s03_question", "h_question", {
    "zones": [Z("stadium", night=True, label="FINAL")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="A PAYROLL? WHO PAYS?", at=0.3, size=72, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · THE COURT CASE", at=C("how a court case"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · WHO CHECKS THE DEALS", at=C("who checks"), color="#FFE0B2", size=30),
              it("sign", x=1560, y=380, text="3 · WHO PAYS THE PRICE", at=C("smaller sports"), color="#C8E6C9", size=30),
              it("letters", x=960, y=700, text="FOLLOW THE PAYCHECK", at=0.4, size=70, color="gold")]})

# ====================================================================== PART 1: the settlement
card("s05_c1", "m1_card", "The Settlement", "House v. NCAA, June 2025")
stage("s06_case", "m1_case", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Most of the damages"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="CLASS ACTION · NIL", scale=0.7),
              it("sign", x=1300, y=250, text="NAMES · IMAGES · LIKENESSES · TV DEALS", at=C("The case was about"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=360, text="≈ $2BN FOR PAST NIL MONEY", at=C("Most of the damages"), color="#BBDEFB", size=32)]},
    sources=["order"])
stage("s07_order", "m1_order", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1100, y=130, text="FINAL APPROVAL · JUNE 6, 2025", at=0.3, size=50, color="gold"),
              it("counter", x=1100, y=290, at=C("The back damages"), prefix="$", suffix="BN", decimals=3, steps=[[0, 0], [{"cue": "every year over ten years"}, 2.576]], text="BACK DAMAGES, PAID OVER 10 YEARS (COURT ORDER)"),
              it("sign", x=1100, y=460, text="CLASS OF ≈ 389,700 ATHLETES", at=C("to a class of"), color="#BBDEFB", size=32),
              it("gavel", x=1650, y=F - 20, hits=[C("gave final approval")], at=0.2)]},
    sources=["order"])
stage("s08_future", "m1_future", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In the first year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="THE REAL CHANGE: THE FUTURE", at=0.3, size=52, color="gold"),
              it("sign", x=800, y=260, text="SHARE UP TO 22% OF AVERAGE POWER-CONFERENCE REVENUE", at=C("Schools may now share"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=370, text="YEAR ONE CAP: $20.5M PER SCHOOL", at=C("In the first year"), color="#C8E6C9", size=32)]},
    sources=["order", "csc"])
stage("s09_rises", "m1_rises", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2025-26", "value": 20.5, "color": "#1E88E5", "at": 0.4, "display": "$20.5M"},
                     {"label": "2026-27", "value": 21.58, "color": "#1E88E5", "at": C("the cap went up"), "display": "$21.58M"},
                     {"label": "2034-35 (EST.)", "value": 32.9, "color": "#90A4AE", "at": C("own expert estimated"), "display": "≈ $32.9M"}],
                    at=0.2, max=36, title="CAP PER SCHOOL (CSC; 2034-35 = PLAINTIFFS' EXPERT ESTIMATE)", x=300, w=1100),
              it("letters", x=1640, y=420, text="AN ESTIMATE", at=C("That\n    is an estimate") if False else C("is an estimate"), size=40, color="gold")]},
    sources=["csc", "order"])
add("p10_pie", "m1_draw", "engine_draw", {
    "title": "The revenue pie (illustration)", "board": BOARD, "draw_start": C("Let me draw the pie"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1200 600 m -220 0 a 220 220 0 1 0 440 0 a 220 220 0 1 0 -440 0", "color": "ink", "width": 6, "kind": "stroke", "start": C("Let me draw the pie"), "label": lbl("ATHLETIC REVENUE", 1200, 350, 22, "ink")},
        {"d": "M 1200 600 L 1200 380 M 1200 600 L 1405 520", "color": "accent", "width": 7, "kind": "stroke", "start": C("Now cut a slice"), "label": lbl("≤ 22% → PAYROLL", 1460, 430, 22, "accent")},
        {"d": "M 1040 700 L 1120 700", "color": "accent2", "width": 1, "kind": "stroke", "start": C("The rest still has to pay"), "label": lbl("COACHES · STADIUMS · OTHER TEAMS", 1150, 720, 18, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("That slice is the payroll", 0.1), "dur": 1.4, "target": [1300, 480]}],
    "scale": 0.86, "floor": 1040}, sources=["order"])
kinetic("s11_t1", "m1_transition", [("Where did the money go?", 66, "where did that money go", None, False),
                                    ("…the new regulator has the numbers", 56, "has the numbers", "gold", False)])

# ====================================================================== PART 2: year one
card("s12_c2", "m2_card", "Year One", "College Sports Commission data")
stage("s13_paid", "m2_paid", {
    "zones": [Z("stadium", label="HOME 0 – 0 AWAY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Schools paid"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="COLLEGE SPORTS COMMISSION · OCT 2026", at=0.3, size=44, color="white"),
              it("counter", x=800, y=270, at=C("Schools paid"), prefix="≈ $", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "in revenue sharing"}, 1.77]], text="REVENUE SHARING, YEAR ONE"),
              it("counter", x=1450, y=270, at=C("athletes"), prefix="", suffix="", steps=[[0, 0], [{"cue": "at three hundred and seven"}, 34915]], text="ATHLETES PAID · 307 SCHOOLS")]},
    sources=["csc"])
stage("s14_total", "m2_total", {
    "zones": [Z("campus", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For context"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=260, at=0.3, prefix="≈ $", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "in that first year"}, 1.98]], text="ALL TRACKED PAYMENTS INCL. SCHOLARSHIPS (CSC)", scale=1.2),
              it("sign", x=1300, y=450, text="≈ THE WHOLE 10-YEAR NIL DAMAGES FUND, IN ONE SEASON", at=C("For context"), color="#FFE0B2", size=28)]},
    sources=["csc", "order"])
stage("s15_who", "m2_who", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Most schools in the system"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="NOT EVERY SCHOOL WENT ALL IN", at=0.3, size=52, color="gold"),
              it("sign", x=800, y=260, text="319 OPTED IN", at=C("three hundred and nineteen"), color="#BBDEFB", size=38),
              it("sign", x=1350, y=260, text="68 AT (OR NEAR) THE CAP", at=C("sixty-eight"), color="#FFCDD2", size=38)]},
    sources=["csc"])
stage("s16_tv", "m2_tv", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For a school in a conference"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="THE TELEVISION MONEY", at=0.3, size=56, color="gold"),
              it("counter", x=1000, y=280, at=C("The Southeastern Conference"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "to its sixteen schools"}, 1.03]], text="SEC DISTRIBUTION TO 16 SCHOOLS, 2024-25", scale=1.2),
              it("sign", x=1300, y=460, text="A BIG BILL, BUT A PAYABLE ONE", at=C("For a school in a conference"), color="#C8E6C9", size=32)]},
    sources=["schools"])
stage("s17_ohio", "m2_ohio", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "REVENUE", "value": 336.1, "color": "#43A047", "at": C("record athletic revenue"), "display": "$336.1M"},
                     {"label": "EXPENSES", "value": 320.4, "color": "#E53935", "at": C("and expenses"), "display": "$320.4M"},
                     {"label": "DIFFERENCE", "value": 15.7, "color": "#FFC21A", "at": C("By our calculation"), "display": "$15.7M"}],
                    at=0.2, max=360, title="OHIO STATE ATHLETICS, FY2025 (DIFFERENCE = OUR CALC.)", x=300, w=1100),
              it("letters", x=1650, y=420, text="< ONE YEAR'S CAP", at=C("payroll cap"), size=40, color="gold")]},
    sources=["schools"])
add("p18_budget", "m2_draw", "engine_draw", {
    "title": "The budget squeeze (illustration)", "board": BOARD, "draw_start": C("Here is the revenue bar"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1380 860", "color": "ink", "width": 4, "start": C("Let me draw the budget")},
        {"d": "M 640 860 L 640 400 L 820 400 L 820 860", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the revenue bar"), "label": lbl("REVENUE", 730, 380, 22, "accent3")},
        {"d": "M 960 860 L 960 422 L 1140 422 L 1140 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is the expense bar"), "label": lbl("EXPENSES", 1050, 470, 22, "risk")},
        {"d": "M 960 422 L 960 360 L 1140 360 L 1140 422", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("Now add a twenty million"), "label": lbl("+ $20M PAYROLL", 1050, 340, 20, "accent")},
        {"d": "M 820 400 L 960 400", "color": "muted", "width": 3, "start": C("Even a record year"), "label": lbl("GAP GONE", 890, 380, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("without changes", 0.1), "dur": 1.4, "target": [1050, 390]}],
    "scale": 0.86, "floor": 1040}, sources=["schools", "csc"])
kinetic("s19_t2", "m2_transition", [("And changes did come…", 66, "And changes did come", None, False),
                                    ("…starting with the size of every team", 56, "the size of every team", "gold", False)])

# ====================================================================== PART 3: fewer seats
card("s20_c3", "m3_card", "Fewer Seats", "Roster limits")
stage("s21_roster", "m3_roster", {
    "zones": [Z("stadium", label="ROSTER LIMITS")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Softball"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("bench", x=1000, at=0.3, n=11, scale=0.8, label="FOOTBALL: 105"),
              it("sign", x=700, y=150, text="BASKETBALL 15 · BASEBALL 34", at=C("Basketball"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=150, text="SOFTBALL 25 · GOLF 9", at=C("Softball"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=250, text="115,000+ NEW SCHOLARSHIPS? (EXPERT ESTIMATE)", at=C("The plaintiffs' expert"), color="#C8E6C9", size=28)]},
    sources=["ncaa", "order"])
stage("s22_exempt", "m3_exempt", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Athletes who were cut"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("bench", x=1000, at=0.3, n=8, cut=2, cutAt=C("could mean losing a spot"), scale=0.8, label="THE END OF THE BENCH"),
              it("sign", x=1000, y=150, text="WALK-ONS: A SPOT AT RISK", at=C("for walk-ons"), color="#FFCDD2", size=34),
              it("sign", x=1000, y=250, text="ALREADY CUT? EXEMPT FOR THEIR CAREERS", at=C("Athletes who were cut"), color="#C8E6C9", size=30)]},
    sources=["ncaa"])
stage("s23_cuts", "m3_cuts", {
    "zones": [Z("campus", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The university said"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="STEPHEN F. AUSTIN: FOUR SPORTS CUT", at=0.3, size=48, color="gold"),
              it("sign", x=800, y=260, text="BOWLING · GOLF ×2 · BEACH VOLLEYBALL", at=C("dropped bowling"), color="#FFCDD2", size=30),
              it("sign", x=1350, y=370, text="'FINANCIAL IMPACT OF … REVENUE-SHARING'", at=C("The university said"), color="#FFE0B2", size=30)]},
    sources=["schools"])
stage("s24_titleix", "m3_titleix", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Lawsuits over the split"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1100, y=130, text="TITLE IX", at=0.3, size=64, color="gold"),
              it("sign", x=1100, y=270, text="JUDGE: SCHOOLS 'FREE TO ALLOCATE' — TITLE IX CLAIMS NOT RELEASED", at=C("The judge said"), color="#BBDEFB", size=26),
              it("docs", x=700, y=560, at=C("Lawsuits over the split"), text="TITLE IX SUITS", scale=0.6, stamp="PENDING", stampAt=C("still pending"))]},
    sources=["order"])
add("p25_bench", "m3_draw", "engine_draw", {
    "title": "The bench (illustration)", "board": BOARD, "draw_start": C("Here is a football team"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": " ".join(rect(780 + k * 56, 500, 40, 40) for k in range(11)), "color": "accent2", "width": 4, "kind": "stroke", "start": C("Here is a football team"), "label": lbl("105 SEATS", 1060, 480, 22, "accent2")},
        {"d": " ".join(rect(1396 + k * 56, 500, 40, 40) for k in range(2)), "color": "muted", "width": 3, "kind": "stroke", "start": C("Before, the roster could be bigger"), "label": lbl("WALK-ONS", 1450, 480, 18, "muted")},
        {"d": "M 1388 470 L 1388 570", "color": "risk", "width": 7, "start": C("Now the bench has a hard edge"), "label": lbl("LIMIT", 1388, 600, 20, "risk")},
        {"d": " ".join(rect(780 + k * 70, 700, 50, 50) for k in range(4)), "color": "risk", "width": 3, "kind": "stroke", "start": C("the smaller sports"), "label": lbl("SMALLER SPORTS · SOME EMPTY", 900, 790, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("an empty bench", 0.1), "dur": 1.4, "target": [900, 725]}],
    "scale": 0.86, "floor": 1040}, sources=["ncaa", "schools"])
kinetic("s26_t3", "m3_transition", [("One more source of money…", 62, "one more source", None, False),
                                    ("…with its own referee", 66, "its own referee", "gold", False)])

# ====================================================================== PART 4: the referee
card("s27_c4", "m4_card", "The Referee", "NIL Go")
stage("s28_nil", "m4_nil", {
    "zones": [Z("airport")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It checks whether"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="NIL GO: A CHECKPOINT FOR DEALS ≥ $600", at=C("NIL Go"), size=44, color="gold"),
              it("sign", x=800, y=270, text="'VALID BUSINESS PURPOSE'?", at=C("valid business purpose"), color="#BBDEFB", size=34),
              it("sign", x=1400, y=370, text="'REASONABLE RANGE OF COMPENSATION'?", at=C("reasonable range"), color="#FFE0B2", size=32),
              it("letters", x=1000, y=120, text="OUTSIDE DEALS: NIL", at=0.3, until=C("NIL Go"), size=56, color="gold")]},
    sources=["csc"])
stage("s29_numbers", "m4_numbers", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "CLEARED", "value": 775.11, "color": "#43A047", "at": C("deals were cleared"), "display": "$775M · 56,570 DEALS"},
                     {"label": "NOT CLEARED", "value": 177.14, "color": "#E53935", "at": C("were not cleared"), "display": "$177M · 2,877 DEALS"}],
                    at=0.2, max=850, dark=True, title="NIL GO RESULTS THROUGH OCT 31, 2026 (CSC)", x=300, w=900),
              it("letters", x=1560, y=400, text="PUBLIC DATA", at=0.3, size=44, color="gold")]},
    sources=["csc"])
stage("s30_boosters", "m4_boosters", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The line between"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=250, at=C("rose by"), prefix="+", suffix="%", steps=[[0, 0], [{"cue": "sixty-four percent"}, 364]], text="VALUE OF DEALS WITH 'ASSOCIATED' ENTITIES, EARLY 2026 (CSC)", scale=1.2),
              it("letters", x=1000, y=110, text="WHO IS PAYING?", at=0.3, size=56, color="gold"),
              it("sign", x=1300, y=450, text="SPONSORSHIP OR DISGUISED SALARY?", at=C("The line between"), color="#FFCDD2", size=34)]},
    sources=["csc"])
add("p31_gate", "m4_draw", "engine_draw", {
    "title": "The checkpoint (CSC data, our share)", "board": BOARD, "draw_start": C("Here comes a line of deals"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": " ".join(rect(560 + k * 60, 580, 44, 44) for k in range(5)), "color": "accent2", "width": 4, "kind": "stroke", "start": C("Here comes a line of deals"), "label": lbl("DEALS", 680, 560, 20, "accent2")},
        {"d": "M 900 480 L 900 720 M 980 480 L 980 720 M 900 480 L 980 480", "color": "ink", "width": 6, "start": C("Most of them pass"), "label": lbl("NIL GO", 940, 460, 22, "ink")},
        {"d": arrow((985, 600), (1240, 560)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("Most of them pass", 0.4), "label": lbl("CLEARED", 1300, 540, 22, "accent3")},
        {"d": arrow((940, 725), (940, 830)), "color": "risk", "width": 6, "kind": "arrow", "start": C("A few are stopped"), "label": lbl("≈ 1 IN 5 DOLLARS STOPPED", 1150, 830, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("where the money meets", 0.1), "dur": 1.4, "target": [940, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["csc"])
kinetic("s32_t4", "m4_transition", [("The biggest question of all…", 62, "biggest question", None, False),
                                    ("…students, or employees?", 66, "students, or employees", "gold", False)])

# ====================================================================== PART 5: students or employees
card("s33_c5", "m5_card", "Students or Employees", "The open question")
stage("s34_johnson", "m5_johnson", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The court sent the case back"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1100, y=130, text="JOHNSON v. NCAA (3RD CIR., 2024)", at=0.3, size=48, color="gold"),
              it("sign", x=1100, y=270, text="'CANNOT BE BARRED AS A MATTER OF LAW'", at=C("cannot be barred"), color="#FFE0B2", size=32),
              it("sign", x=1100, y=380, text="SENT BACK: 'ECONOMIC REALITIES' TEST", at=C("The court sent the case back"), color="#BBDEFB", size=30),
              it("gavel", x=1650, y=F - 20, hits=[C("a federal appeals court ruled")], at=0.2)]},
    sources=["law"])
stage("s35_congress", "m5_congress", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In September"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="WASHINGTON STEPS IN", at=0.3, size=56, color="gold"),
              it("sign", x=750, y=250, text="EXECUTIVE ORDER 14400 (APR 2026)", at=C("signed an executive order"), color="#FFE0B2", size=30),
              it("sign", x=1400, y=250, text="SENATE: 77–22 · HOUSE: NO VOTE YET", at=C("In September"), color="#BBDEFB", size=30),
              it("letters", x=1100, y=380, text="NOT LAW", at=C("so it is not law"), size=60, color="risk")]},
    sources=["law"])
add("p36_doors", "m5_draw", "engine_draw", {
    "title": "Two doors (illustration)", "board": BOARD, "draw_start": C("One door says student"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(760, 400, 200, 340), "color": "accent2", "width": 6, "kind": "box", "start": C("One door says student"), "label": lbl("STUDENT", 860, 380, 24, "accent2")},
        {"d": rect(1260, 400, 200, 340), "color": "accent", "width": 6, "kind": "box", "start": C("The other says employee"), "label": lbl("EMPLOYEE", 1360, 380, 24, "accent")},
        {"d": "M 960 760 L 1260 760", "color": "ink", "width": 4, "start": C("stand in the hallway"), "label": lbl("THE HALLWAY", 1110, 800, 22, "ink")},
        {"d": arrow((965, 570), (1255, 570)), "color": "risk", "width": 5, "kind": "arrow", "start": C("stand in the hallway", 0.5), "label": lbl("WHICH WAY?", 1110, 540, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("a payroll in one hand", 0.1), "dur": 1.4, "target": [1110, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["law"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("stadium", night=True, label="FINAL")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The money is real"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=120, text="A COURT ENDED THE OLD RULES", at=0.3, size=54, color="gold"),
              it("sign", x=800, y=260, text="RICH PROGRAMS: CAN CARRY IT", at=C("The\n    rich programs") if False else C("rich programs"), color="#C8E6C9", size=30),
              it("sign", x=1400, y=260, text="THE REST: REMOVING SEATS", at=C("The rest are deciding"), color="#FFCDD2", size=30)]},
    sources=["csc", "schools"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_college_storyboard.py; edit the generator, not this file.\n"
           "# Episode 49 storyboard (college sports): one visual language per part; tones from visual_direction.yaml.\n")
