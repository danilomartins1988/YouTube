"""Generates projects/the-business-behind-americas-student-debt/deliverables/documentary/storyboard.yaml (Episode 33,
US batch #06: The Business Behind America's Student Debt).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: typography + graduation caps in the air (new `gradcaps` item) and the delinquency screen.
- Part 1 (the price of a degree): a generic college quad (new `campus` set), price tags, tuition charts.
- Part 2 (the biggest lender): Washington (parliament set), a balance scale of the GAO estimate.
- Part 3 (the middlemen): servicer offices, an evidence board of servicers, bills.
- Part 4 (when the pause ended): the delinquency screen, the campus at night, a diploma that unrolls into a debt (new `diploma`).
- Part 5 (the new rules): a courtroom (SAVE vacated) and Congress.
No real logos or campuses; company names in text only. Lint: tools/lint_storyboard.py.
Run: python tools/gen_studentdebt_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-business-behind-americas-student-debt/deliverables/documentary/storyboard.yaml"
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


def screen(at=0.2, **kw):
    return it("tradescreen", x=kw.pop("x", 960), y=kw.pop("y", 470), at=at, scale=kw.pop("scale", 1.15), text="STUDENT DEBT 90+ DAYS LATE (NY FED)",
              decimals=1, max=12, min=0, hot=5, lamp=False, suffix="%", **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("campus")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.2}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("counter", x=1000, y=200, at=0.05, prefix="$", suffix=" TRILLION", decimals=2, steps=[[0.05, 0], [1.5, 1.65]], text="U.S. STUDENT LOAN DEBT, Q2 2026 (NY FED)", scale=1.4),
              it("gradcaps", x=1000, at=0.3, n=7, spread=900, h=0.5),
              it("letters", x=1000, y=420, text="MORE THAN ALL CREDIT CARDS", at=C("more than they owe"), size=50, color="gold")]},
    sources=["nyfed"])
stage("s02_twist", "h_twist", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 0,
    "items": [screen(at=0.2, price=[[0, 0.6], [{"cue": "Then missed payments"}, 0.53], [{"cue": "In three months"}, 0.6], [{"cue": "jumped from"}, 7.74]]),
              it("letters", x=960, y=120, text="THE PAUSE ENDS", at=C("Then missed payments"), size=60, color="risk")]},
    sources=["nyfed"])
stage("s03_question", "h_question", {
    "zones": [Z("campus", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("diploma", x=1000, y=460, at=0.1, scale=0.9, openAt=0.6, text="$ ? ? ?", title="WHO PROFITS?"),
              it("letters", x=1000, y=130, text="WHO'S IN THE BUSINESS?", at=0.4, size=70, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · COLLEGES", at=0.3, color="#BBDEFB", size=44),
              it("sign", x=750, y=380, text="2 · THE LENDER", at=C("the government that lends"), color="#FFCDD2", size=44),
              it("sign", x=1170, y=380, text="3 · COLLECTORS", at=C("the companies that collect"), color="#FFE0B2", size=44),
              it("sign", x=1590, y=380, text="4 · BORROWERS", at=C("the borrowers who fall behind"), color="#C8E6C9", size=44),
              it("letters", x=960, y=700, text="FOUR PLAYERS", at=C("the four players"), size=72, color="gold")]})

# ====================================================================== PART 1: the price of a degree (campus + charts)
card("s05_c1", "m1_card", "The Price of a Degree", "Sticker price vs real price")
stage("s06_tuition", "m1_tuition", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("At private nonprofit"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("pricetag", x=800, y=300, at=0.3, text="1996: $6,320", pages=[[{"cue": "This year, it is"}, "NOW: $12,290", True]], scale=1.0),
              it("pricetag", x=1550, y=300, at=C("At private nonprofit"), text="1996: $27,530", pages=[[{"cue": "to forty-six thousand"}, "NOW: $46,350", True]], scale=1.0),
              it("letters", x=800, y=450, text="PUBLIC 4-YR, IN-STATE (COLLEGE BOARD)", at=0.6, size=30, color="white"),
              it("letters", x=1150, y=120, text="ADJUSTED FOR INFLATION", at=C("already adjusted"), size=50, color="gold")]},
    sources=["cb"])
stage("s07_cpi", "m1_cpi", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=470, text="30 YEARS OF PRICES", at=0.3, until=C("rose about two hundred"), size=84, color="gold"),
              chart([{"label": "COLLEGE TUITION", "value": 249, "color": "#E53935", "at": C("rose about two hundred"), "display": "≈ +250%"},
                     {"label": "ALL PRICES", "value": 114, "color": "#90A4AE", "at": C("Prices in general"), "display": "≈ +114%"}],
                    at=0.2, max=280, title="CPI, SEP 1996 → SEP 2026 (BLS; OUR CALCULATION)", x=520, w=880)]},
    sources=["bls"])
stage("s08_twist", "m1_twist", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="LAST 10 YEARS: −8%", at=C("actually fell by eight"), size=60, color="green"),
              chart([{"label": "NET PRICE PEAK 2012-13", "value": 4600, "color": "#90A4AE", "at": C("dropped from a peak"), "display": "$4,600"},
                     {"label": "NET PRICE 2026-27", "value": 1920, "color": "#23995A", "at": C("to an estimated"), "display": "$1,920"}],
                    at=0.4, max=5200, title="AFTER GRANTS · PUBLIC 4-YR IN-STATE (2026 $)", x=600, y=270, w=820, h=520),
              it("letters", x=1000, y=900, text="STICKER PRICE ≠ REAL PRICE", at=C("The sticker price"), size=48, color="risk")]},
    sources=["cb"])
stage("s09_grads", "m1_grads", {
    "zones": [Z("campus")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("and the average borrower"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [*crowd([600 + 100 * k for k in range(6)], "cheer", at=0.2, scale=0.6),
              it("gradcaps", x=850, at=0.5, n=5, spread=600, scale=0.7, h=0.5),
              it("letters", x=850, y=180, text="47% GRADUATED WITH DEBT", at=C("forty-seven percent"), size=50, color="gold"),
              it("diploma", x=1650, y=440, at=C("and the average borrower"), scale=0.7, openAt=C("owed"), text="$30,220", title="AVERAGE DEBT, 2024-25", sub="College Board")]},
    sources=["cb"])
add("p10_gap", "m1_draw", "engine_draw", {
    "title": "Sticker price vs real price (schematic)", "board": BOARD, "draw_start": C("Here is the sticker price"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Here is the sticker price")},
        {"d": "M 580 700 L 1440 420", "color": "risk", "width": 7, "start": C("almost doubling"), "label": lbl("STICKER PRICE ≈ ×2", 1300, 400, 22, "risk")},
        {"d": "M 580 780 L 1000 740 L 1440 800", "color": "accent3", "width": 7, "start": C("what a typical student actually pays"), "label": lbl("NET PRICE", 1300, 830, 22, "accent3")},
        {"d": "M 1100 590 L 1100 740 M 1250 545 L 1250 770 M 1400 500 L 1400 790", "color": "accent", "width": 5, "fill": "accent", "kind": "bar", "start": C("The space between"), "label": lbl("GRANTS · SAVINGS · LOANS", 1250, 470, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("the loan was the easiest", 0.2), "dur": 1.4, "target": [1250, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["cb"])
kinetic("s11_t1", "m1_transition", [("Now, the lender", 64, "Which brings us", None, False), ("…and it's not a bank", 64, "is not a bank", "gold", False)])

# ====================================================================== PART 2: the biggest lender (Washington + balance)
card("s12_c2", "m2_card", "The Biggest Lender", "Washington's loan book")
stage("s13_gov", "m2_gov", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Education Department counts"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("counter", x=1000, y=200, at=0.3, prefix="$", suffix=" TRILLION", decimals=2, steps=[[0, 0], [{"cue": "trillion dollars of student loans", "offset": 0}, 1.63]], text="STUDENT LOANS HELD BY THE FEDERAL GOVERNMENT (FED G.19, SEP 2026)", scale=1.1),
              it("letters", x=1500, y=420, text="≈ 42 MILLION PEOPLE", at=C("The Education Department counts"), size=56, color="gold")]},
    sources=["g19", "fsa"])
stage("s14_growth", "m2_growth", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2003", "value": 240.7, "color": "#90A4AE", "at": 0.5, "display": "$241bn"},
                     {"label": "2026", "value": 1651, "color": "#E53935", "at": C("Today it is"), "display": "$1.65tn"}],
                    at=0.2, max=1800, dark=True, title="STUDENT DEBT OUTSTANDING (NY FED)", x=420, w=860),
              it("letters", x=1560, y=420, text="≈ ×7", at=C("almost seven times"), size=110, color="gold"),
              it("letters", x=1560, y=530, text="(our calculation)", at=C("almost seven times", 0.4), size=32, color="white")]},
    sources=["nyfed"])
stage("s15_profit", "m2_profit", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Later estimates flipped"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("docs", x=650, y=560, at=0.2, text="GAO-22-105365", scale=0.7, stamp="$311BN SWING", stampAt=C("A swing of")),
              it("tradescreen", x=1350, y=430, at=C("At first"), scale=0.9, text="LOANS 1997–2021 (GAO, $BN)", decimals=0, max=150, min=-220, hot=1e9, lamp=False,
                 price=[[0, 0], [{"cue": "expected them to earn"}, 114], [{"cue": "Later estimates flipped"}, 114], [{"cue": "to a cost of"}, -197]])]},
    sources=["gao22"])
stage("s16_why", "m2_why", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("pinboard", cards=[
                {"x": 560, "y": 380, "text": "$102BN", "sub": "pandemic emergency relief", "at": 0.3, "w": 420, "color": "#FFCDD2", "size": 60},
                {"x": 1360, "y": 380, "text": "THE REST", "sub": "repayment-plan changes · optimistic estimates", "at": C("The rest came from"), "w": 520, "color": "#FFF59D", "size": 52}],
              links=[[0, 1, C("The rest came from", 0.4)]])]},
    sources=["gao22"])
add("p17_scale", "m2_draw", "engine_draw", {
    "title": "The government's scale", "board": BOARD, "draw_start": C("On one side, the interest"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1000 820 L 1000 480 M 900 820 L 1100 820", "color": "ink", "width": 6, "start": C("Let me draw the government's")},
        {"d": "M 720 520 L 1280 440", "color": "ink", "width": 6, "start": C("On one side, the interest")},
        {"d": "M 640 520 L 800 520 L 780 580 L 660 580 Z", "color": "accent3", "width": 6, "kind": "box", "start": C("the interest it expected"), "label": lbl("INTEREST IN", 720, 620, 22, "accent3")},
        {"d": "M 1200 440 L 1360 440 L 1340 500 L 1220 500 Z", "color": "risk", "width": 6, "kind": "box", "start": C("On the other, the money"), "label": lbl("LOANS + LOSSES", 1280, 540, 22, "risk")},
        {"d": "M 1450 380 L 1450 700 M 1430 680 L 1450 700 L 1470 680", "color": "risk", "width": 6, "start": C("tipped into a loss"), "label": lbl("→ LOSS", 1500, 740, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The taxpayer", 0.2), "dur": 1.4, "target": [1280, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["gao22"])
kinetic("s18_t2", "m2_transition", [("Washington lends…", 64, "But the government", None, False), ("…private companies collect", 60, "it hires private companies", "gold", False)])

# ====================================================================== PART 3: the middlemen (servicer offices + evidence board)
card("s19_c3", "m3_card", "The Middlemen", "Loan servicers and private lenders")
stage("s20_servicers", "m3_servicers", {
    "zones": [Z("corkboard")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1100, "y": 470, "zoom": 1.1}, {"at": C("Four other companies"), "x": 1100, "y": 480, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("pinboard", cards=[
                {"x": 1100, "y": 330, "text": "NELNET", "sub": "$506bn · 12.4M borrowers", "at": C("the biggest of them"), "w": 460, "color": "#FFF59D", "size": 54},
                {"x": 520, "y": 620, "text": "AIDVANTAGE", "sub": "$384bn · 9.8M", "at": C("Four other companies"), "w": 340, "size": 34},
                {"x": 900, "y": 680, "text": "MOHELA", "sub": "$324bn · 6.5M", "at": C("Four other companies", 0.3), "w": 300, "size": 34},
                {"x": 1300, "y": 680, "text": "EDFINANCIAL", "sub": "$225bn · 6.8M", "at": C("Four other companies", 0.6), "w": 320, "size": 32},
                {"x": 1690, "y": 620, "text": "CRI", "sub": "$52bn · 2.8M", "at": C("Four other companies", 0.9), "w": 260, "size": 34}],
              links=[[0, 1, C("split most of the rest")], [0, 2, C("split most of the rest", 0.2)], [0, 3, C("split most of the rest", 0.4)], [0, 4, C("split most of the rest", 0.6)]]),
              it("letters", x=1100, y=140, text="LOAN SERVICERS · SEPT 2025 (GAO)", at=0.3, size=46, color="white")]},
    sources=["gao26"])
stage("s21_fees", "m3_fees", {
    "zones": [Z("office")], "worldW": 2000,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=140, text="PAID PER BORROWER, PER MONTH (OLDER CONTRACTS, GAO 2016)", at=0.3, size=34, color="white"),
              it("pricetag", x=550, y=330, at=C("for a borrower in repayment"), text="$2.85", scale=1.0),
              it("sign", x=550, y=560, text="IN REPAYMENT", at=C("for a borrower in repayment"), color="#C8E6C9", size=34),
              it("pricetag", x=1000, y=330, at=C("still in school"), text="$1.05", scale=1.0),
              it("sign", x=1000, y=560, text="IN SCHOOL", at=C("still in school"), color="#BBDEFB", size=34),
              it("pricetag", x=1450, y=330, at=C("And only forty-five"), text="$0.45", pages=[[0, "$0.45", True]], scale=1.0),
              it("sign", x=1450, y=560, text="270+ DAYS BEHIND", at=C("And only forty-five"), color="#FFCDD2", size=34)]},
    sources=["gao16"])
stage("s22_incentive", "m3_incentive", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But the government's own watchdog"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("docs", x=650, y=560, at=0.2, text="2024 CONTRACTS", scale=0.7, stamp="UP TO −20%", stampAt=C("with penalties")),
              chart([{"label": "FSA STAFF, JAN 2025", "value": 1433, "color": "#90A4AE", "at": C("from one thousand four hundred"), "display": "1,433"},
                     {"label": "DEC 2025", "value": 777, "color": "#E53935", "at": C("to seven hundred"), "display": "777"}],
                    at=C("But the government's own watchdog"), max=1600, title="WHO WATCHES THE SERVICERS? (GAO-26-108534)", x=1000, y=230, w=760, h=520)]},
    sources=["gao26b"])
stage("s23_private", "m3_private", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("building", x=420, at=0.2, style="bank", text="PRIVATE LENDERS", scale=0.8, color="#90A4AE"),
              chart([{"label": "2007-08", "value": 34.7, "color": "#90A4AE", "at": C("far less than before"), "display": "$34.7bn"},
                     {"label": "2010-11", "value": 11.4, "color": "#B0BEC5", "at": C("far less than before", 0.6), "display": "$11.4bn"},
                     {"label": "2025-26", "value": 15.4, "color": "#E89A00", "at": C("in the last school year"), "display": "$15.4bn"}],
                    at=0.4, max=40, title="NEW PRIVATE LOANS A YEAR (COLLEGE BOARD)", x=760, y=230, w=760, h=520, dark=True)]},
    sources=["cb"])
add("p24_chain", "m3_draw", "engine_draw", {
    "title": "The chain", "board": BOARD, "draw_start": C("The student signs"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 190, 90), "color": "ink", "width": 6, "kind": "box", "start": C("The student signs"), "label": lbl("STUDENT", 655, 473, 24, "ink")},
        {"d": rect(860, 420, 190, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("The government lends"), "label": lbl("GOVERNMENT", 955, 473, 22, "accent2")},
        {"d": rect(1160, 420, 190, 90), "color": "accent", "width": 6, "kind": "box", "start": C("A servicer"), "label": lbl("SERVICER", 1255, 473, 22, "accent")},
        {"d": arrow((760, 465), (850, 465)) + " " + arrow((1060, 465), (1150, 465)), "color": "ink", "width": 4, "start": C("owns the debt")},
        {"d": rect(860, 640, 190, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("And the college"), "label": lbl("COLLEGE", 955, 693, 24, "accent3")},
        {"d": arrow((955, 520), (955, 630)), "color": "accent3", "width": 5, "start": C("receives the money"), "label": lbl("PAID ON DAY ONE", 1150, 600, 20, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("before anyone knows", 0.2), "dur": 1.4, "target": [955, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["gao26", "cb"])
kinetic("s25_t3", "m3_transition", [("The chain was frozen…", 64, "that chain was frozen", None, False), ("Then the pause ended", 70, "Then the pause ended", "risk", False)])

# ====================================================================== PART 4: when the pause ended (screen + night campus + diploma)
card("s26_c4", "m4_card", "When the Pause Ended", "Delinquency and default")
stage("s27_scores", "m4_scores", {
    "zones": [Z("campus", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("New York Fed found"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [*crowd([600 + 90 * k for k in range(7)], "worry", at=0.3, scale=0.6),
              it("counter", x=1400, y=230, at=C("New York Fed found"), prefix="", suffix="M+", decimals=1, steps=[[0, 0], [{"cue": "newly delinquent", "offset": 0}, 2.2]], text="BORROWERS WHOSE SCORE FELL 100+ POINTS (NY FED)"),
              it("letters", x=1400, y=450, text="CREDIT SCORE −100", at=C("drop by more than"), size=60, color="risk")]},
    sources=["lse25"])
stage("s28_rate", "m4_rate", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}], "drift": 0,
    "items": [screen(at=0.2, price=[[0, 0.53], [1.0, 7.74], [{"cue": "And it kept climbing"}, 10.16], [{"cue": "of all student loan balances"}, 10.6]]),
              it("letters", x=960, y=120, text="Q4 2024 → Q2 2026", at=0.4, size=50, color="white")]},
    sources=["nyfed"])
stage("s29_default", "m4_default", {
    "zones": [Z("corkboard")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Education Department's"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("diploma", x=700, y=440, at=0.2, scale=0.75, openAt=0.8, text="DEFAULT", title="FEDERAL LOAN", sub="Q4 2025: ≈ 1M · Q1 2026: 2.6M borrowers"),
              chart([{"label": "JUN 2025", "value": 82.6, "color": "#90A4AE", "at": C("from"), "display": "$82.6bn"},
                     {"label": "JUN 2026", "value": 187.8, "color": "#E53935", "at": C("more than doubling"), "display": "$187.8bn"}],
                    at=C("The Education Department's"), max=210, title="DIRECT LOANS IN DEFAULT (FSA)", x=1150, y=230, w=700, h=500)]},
    sources=["lse26", "fsa"])
stage("s30_collect", "m4_collect", {
    "zones": [Z("office")], "worldW": 2200,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("restarted in May"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("letters", x=900, y=130, text="WHAT DEFAULT CAN MEAN", at=0.3, size=56, color="risk"),
              it("sign", x=500, y=260, text="PAYCHECK", at=C("part of a paycheck"), color="#FFCDD2", size=40),
              it("sign", x=900, y=260, text="TAX REFUND", at=C("a tax refund"), color="#FFCDD2", size=40),
              it("sign", x=1300, y=260, text="SOCIAL SECURITY", at=C("even Social Security"), color="#FFCDD2", size=40),
              it("calendar", x=800, y=560, at=C("restarted in May"), pages=[[0, "MAY", "2025"], [{"cue": "then put on hold"}, "HOLD", "ON"]], scale=0.7),
              it("letters", x=1500, y=520, text="MAY 2026: SUSPENDED, NO CLEAR TIMELINE", at=C("suspended with no clear"), size=34, color="gold")]},
    sources=["lse25", "lse26"])
add("p31_cliff", "m4_draw", "engine_draw", {
    "title": "The cliff (schematic)", "board": BOARD, "draw_start": C("Here is the share of student debt"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1700, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 860 L 1460 860 M 560 860 L 560 380", "color": "ink", "width": 4, "start": C("Here is the share of student debt")},
        {"d": "M 580 850 L 1180 845", "color": "accent3", "width": 7, "start": C("a flat line near zero"), "label": lbl("2020–2024 ≈ 0%", 880, 820, 22, "accent3")},
        {"d": "M 1180 845 L 1230 470 L 1440 440", "color": "risk", "width": 8, "start": C("Then, in a single quarter"), "label": lbl("10.6%", 1400, 420, 28, "risk")},
        {"d": "M 1230 860 L 1230 470 L 1300 470 L 1300 860", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.2, "kind": "bar", "start": C("Every point on that wall"), "label": lbl("A PERSON", 1265, 900, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Every point on that wall", 0.2), "dur": 1.4, "target": [1230, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["nyfed"])
kinetic("s32_t4", "m4_transition", [("Washington's answer:", 64, "Washington's answer", None, False), ("change the rules", 72, "change the rules", "gold", False)])

# ====================================================================== PART 5: the new rules (court + Congress)
card("s33_c5", "m5_card", "The New Rules", "SAVE, Grad PLUS and the 2025 law")
stage("s34_save", "m5_save", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On March tenth"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 2,
    "items": [it("docs", x=800, y=560, at=0.2, text="SAVE PLAN", scale=0.7, stamp="VACATED", stampAt=C("vacated the plan")),
              it("letters", x=1300, y=200, text="≈ 8 MILLION IN FORBEARANCE", at=C("About eight million"), size=50, color="gold"),
              it("gavel", x=1600, y=420, hits=[C("vacated the plan", 0.2)]),
              it("calendar", x=1250, y=430, at=C("On March tenth"), pages=[[0, "MAR 10", "2026"]], scale=0.7)]},
    sources=["gao26"])
stage("s35_obbb", "m5_obbb", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Parents face new limits"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.5}], "drift": 1,
    "items": [it("calendar", x=650, y=320, at=0.2, pages=[[0, "JUL 4", "2025"]], scale=0.75),
              it("docs", x=650, y=600, at=C("It eliminated"), text="GRAD PLUS", scale=0.6, stamp="ELIMINATED", stampAt=C("Grad PLUS loans")),
              it("sign", x=1300, y=250, text="GRAD: $20,500/YR · $100,000 TOTAL", at=C("New graduate students"), color="#BBDEFB", size=34),
              it("sign", x=1300, y=360, text="PARENT PLUS: $20,000/YR · $65,000", at=C("Parents face new limits"), color="#FFE0B2", size=34),
              it("sign", x=1300, y=470, text="NEW REPAYMENT PLAN BY JULY 2026", at=C("a new Repayment Assistance"), color="#C8E6C9", size=34)]},
    sources=["obbb"])
add("p36_business", "m5_draw", "engine_draw", {
    "title": "The business, together", "board": BOARD, "draw_start": C("Colleges set the price"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 330, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 360, 280, 80), "color": "accent3", "width": 6, "kind": "box", "start": C("Colleges set the price"), "label": lbl("COLLEGES · PRICE", 1000, 408, 22, "accent3")},
        {"d": rect(560, 520, 260, 80), "color": "accent2", "width": 6, "kind": "box", "start": C("The government lends"), "label": lbl("GOV · LOSSES", 690, 568, 22, "accent2")},
        {"d": rect(1180, 520, 260, 80), "color": "accent", "width": 6, "kind": "box", "start": C("Servicers collect"), "label": lbl("SERVICERS · FEES", 1310, 568, 22, "accent")},
        {"d": rect(860, 680, 280, 80), "color": "risk", "width": 6, "kind": "box", "start": C("And the borrowers carry"), "label": lbl("BORROWERS · DECADES", 1000, 728, 22, "risk")},
        {"d": "M 1000 300 L 1000 350 M 940 300 L 1060 300", "color": "ink", "width": 7, "start": C("The new limits cap"), "label": lbl("CAP", 1000, 285, 24, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("The new limits cap", 0.3), "dur": 1.4, "target": [1000, 330]}],
    "scale": 0.86, "floor": 1040}, sources=["obbb", "gao22", "gao16"])

# ====================================================================== PAYOFF
stage("s37_payoff", "payoff", {
    "zones": [Z("campus", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("But the bill"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 0,
    "items": [it("diploma", x=1000, y=470, at=0.2, scale=0.85, openAt=C("But the bill"), text="$1.65 TRILLION", size=52, title="THE BILL", sub="students · parents · taxpayers"),
              it("letters", x=1000, y=130, text="BORROW TODAY, EARN TOMORROW", at=C("Borrow today"), size=56, color="gold")]},
    sources=["nyfed", "gao22"])
add("s38_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_studentdebt_storyboard.py; edit the generator, not this file.\n"
           "# Episode 33 storyboard (US student debt): one visual language per part; tones from visual_direction.yaml.\n")
