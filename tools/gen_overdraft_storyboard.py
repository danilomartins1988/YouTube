"""Generates projects/why-banks-still-make-billions-from-overdrafts/deliverables/documentary/storyboard.yaml
(Episode 46, new topics N6: Why Banks Still Make Billions From Overdrafts).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the shop counter with the bank-app statement going negative; the bank hall.
- Part 1 (the fee): shop + statement, the bank hall, a bad-day drawing.
- Part 2 (who pays): the studio charts, the office at night (examiners), a 100-accounts drawing.
- Part 3 (the retreat): the bank hall, the exchange floor (bank filings), the CFPB bar chart.
- Part 4 (the rule that vanished): the office (rule), the parliament (repeal), a timeline.
- Part 5 (still billions): the exchange, the bank hall at night, the overdraft machine.
New engine piece: `statement` (generic bank-app statement with a running balance). No bank logos (names in text only),
no real people drawn. Lint: tools/lint_storyboard.py. Run: python tools/gen_overdraft_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-banks-still-make-billions-from-overdrafts/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="$35", at=0.05, size=150, color="risk"),
              it("statement", x=1450, y=520, at=0.3, scale=0.8, start=4, rows=[
                  {"at": C("You can pay it"), "label": "CARD PURCHASE", "amt": -9},
                  {"at": C("more than you have"), "label": "OVERDRAFT FEE", "amt": -35, "fee": True}]),
              *crowd([600], "walk", at=0.2, scale=0.75)]},
    sources=["cfpbfee"])
stage("s02_twist", "h_twist", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("still collected"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="FEES CUT SHARPLY…", at=0.3, until=C("still collected"), size=56, color="gold"),
              it("counter", x=1200, y=260, at=C("still collected"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "bounced-payment fees"}, 5.83]], text="OVERDRAFT + NSF REVENUE 2023 (CFPB, BANKS > $1BN)", scale=1.2)]},
    sources=["cfpb23"])
stage("s03_question", "h_question", {
    "zones": [Z("bankhall", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="A HATED FEE. STILL BILLIONS. WHY?", at=0.3, size=60, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · HOW THE FEE IS MADE", at=C("how an overdraft fee is made"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · WHO PAYS MOST", at=C("a small group of customers"), color="#FFE0B2", size=32),
              it("sign", x=1560, y=380, text="3 · THE CAP THAT VANISHED", at=C("written and then erased"), color="#C8E6C9", size=32),
              it("letters", x=960, y=700, text="FOLLOW THE OVERDRAFT DOLLAR", at=0.4, size=64, color="gold")]})

# ====================================================================== PART 1: the fee
card("s05_c1", "m1_card", "The Fee", "How an overdraft is made")
stage("s06_what", "m1_what", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The bank can refuse"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="WHAT IS AN OVERDRAFT?", at=0.3, size=52, color="gold"),
              it("statement", x=1350, y=540, at=0.4, scale=0.8, start=20, rows=[
                  {"at": C("You buy something"), "label": "PURCHASE", "amt": -25},
                  {"at": C("it usually charges"), "label": "OVERDRAFT FEE", "amt": -35, "fee": True}]),
              it("sign", x=650, y=330, text="REFUSE IT… OR PAY IT?", at=C("The bank can refuse"), color="#FFE0B2", size=34)]},
    sources=["cfpbfee"])
stage("s07_median", "m1_median", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "OVERDRAFT FEE", "value": 35, "color": "#E53935", "at": C("median overdraft fee"), "display": "$35"},
                     {"label": "NSF FEE", "value": 32, "color": "#FB8C00", "at": C("non-sufficient funds"), "display": "$32"},
                     {"label": "THE PURCHASE", "value": 24, "color": "#43A047", "at": C("median debit card purchase"), "display": "$24"}],
                    at=0.2, max=40, title="MEDIANS AT THE LARGEST INSTITUTIONS (CFPB)", x=300, w=1100),
              it("letters", x=1640, y=400, text="FEE > PURCHASE", at=C("was only"), size=50, color="risk")]},
    sources=["cfpbfee"])
stage("s08_loan", "m1_loan", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("If you called that"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=250, text="BANK COVERS $24 · A FEW DAYS", at=0.3, color="#BBDEFB", size=34),
              it("sign", x=1500, y=250, text="PRICE OF THE FAVOR: $35", at=C("And it charges"), color="#FFCDD2", size=34),
              it("letters", x=1250, y=420, text="A VERY EXPENSIVE SHORT LOAN", at=C("If you called that"), size=48, color="gold")]},
    sources=["cfpbfee"])
stage("s09_stack", "m1_stack", {
    "zones": [Z("shop", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=140, text="$35 PER ITEM · UP TO 3 A DAY (WELLS FARGO)", at=0.3, size=42, color="gold"),
              it("counter", x=1000, y=330, at=C("Three small purchases"), prefix="$", suffix="", steps=[[0, 0], [{"cue": "one hundred and five dollars"}, 105]], text="FEES IN ONE BAD DAY (EXAMPLE)", scale=1.3)]},
    sources=["banks"])
add("p10_day", "m1_draw", "engine_draw", {
    "title": "A bad day (illustration)", "board": BOARD, "draw_start": C("Start at ten dollars"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 640 560 L 1500 560", "color": "ink", "width": 4, "kind": "stroke", "start": C("Start at ten dollars"), "label": lbl("$0", 610, 568, 22, "ink")},
        {"d": "M 660 470 L 820 500 L 980 640 L 1140 700 L 1300 760 L 1460 800", "color": "accent2", "width": 6, "kind": "stroke", "start": C("A coffee"), "label": lbl("BALANCE", 700, 450, 20, "accent2")},
        {"d": rect(940, 600, 90, 40), "color": "risk", "width": 4, "kind": "box", "start": C("A fee."), "label": lbl("$35", 985, 627, 20, "risk")},
        {"d": rect(1250, 700, 90, 40), "color": "risk", "width": 4, "kind": "box", "start": C("another fee"), "label": lbl("$35", 1295, 727, 20, "risk")},
        {"d": rect(1410, 740, 90, 40), "color": "risk", "width": 4, "kind": "box", "start": C("a third fee"), "label": lbl("$35", 1455, 767, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("The purchases add up", 0.1), "dur": 1.4, "target": [1300, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["banks"])
kinetic("s11_t1", "m1_transition", [("So who pays all these fees?", 62, "who actually ends up", None, False),
                                    ("…surprisingly few people", 66, "surprisingly concentrated", "gold", False)])

# ====================================================================== PART 2: who pays
card("s12_c2", "m2_card", "Who Pays", "A small group of accounts")
stage("s13_few", "m2_few", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=150, text="A CFPB STUDY OF CHECKING ACCOUNTS", at=0.3, size=46, color="gold"),
              it("counter", x=600, y=420, at=C("about\n    nine percent") if False else C("nine percent of accounts"), prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "nine percent of accounts"}, 9]], text="OF ACCOUNTS", scale=1.3),
              it("counter", x=1320, y=420, at=C("paid almost"), prefix="≈ ", suffix="%", steps=[[0, 0], [{"cue": "seventy-nine percent"}, 79]], text="OF ALL OVERDRAFT + NSF FEES", scale=1.3)]},
    sources=["cfpbfee"])
stage("s14_frequent", "m2_frequent", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For the bank"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=230, text="20+ OVERDRAFTS A YEAR: < 1 IN 20 ACCOUNTS", at=0.3, color="#BBDEFB", size=32),
              it("sign", x=1500, y=330, text="…PAID ≈ 63% OF THE FEES", at=C("sixty-three percent"), color="#FFCDD2", size=36),
              it("letters", x=1250, y=470, text="REPEAT CUSTOMERS", at=C("It depends on a small group"), size=56, color="gold")]},
    sources=["cfpbfee"])
stage("s15_tight", "m2_tight", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="WHO OVERDRAWS ON $24?", at=0.3, size=54, color="gold"),
              it("sign", x=700, y=300, text="LARGE BALANCE: RARELY", at=C("Usually not someone"), color="#C8E6C9", size=34),
              it("sign", x=1300, y=300, text="WAITING FOR PAYDAY: MORE OFTEN", at=C("someone waiting for the next"), color="#FFCDD2", size=34),
              *crowd([1250], "walk", at=0.4, scale=0.75)]},
    sources=["cfpbfee"])
add("p16_order", "m2_order", "engine_draw", {
    "title": "Largest payment first (CFPB white paper)", "board": BOARD, "draw_start": C("processed the largest payment"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 380, 260, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("processed the largest payment"), "label": lbl("BALANCE $100", 690, 428, 22, "accent2")},
        {"d": rect(560, 500, 260, 70), "color": "ink", "width": 5, "kind": "box", "start": C("Paying the big bill first"), "label": lbl("1 · BILL $110", 690, 543, 22, "ink")},
        {"d": rect(560, 600, 260, 60), "color": "risk", "width": 4, "kind": "box", "start": C("several small purchases"), "label": lbl("2 · $5 → FEE", 690, 638, 20, "risk")},
        {"d": rect(560, 680, 260, 60), "color": "risk", "width": 4, "kind": "box", "start": C("several small purchases", 0.5), "label": lbl("3 · $5 → FEE", 690, 718, 20, "risk")},
        {"d": rect(560, 760, 260, 60), "color": "risk", "width": 4, "kind": "box", "start": C("each triggered"), "label": lbl("4 · $5 → FEE", 690, 798, 20, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("each triggered", 0.2), "dur": 1.4, "target": [820, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpbfee"])
stage("s17_apsn", "m2_apsn", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its examiners found"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="A STRANGER FEE", at=0.3, until=C("likely unfair"), size=52, color="gold"),
              it("sign", x=700, y=230, text="APPROVED: ENOUGH MONEY", at=C("A purchase was approved"), color="#C8E6C9", size=32),
              it("sign", x=1200, y=330, text="SETTLED LATER: FEE ANYWAY", at=C("by the time it settled"), color="#FFCDD2", size=32),
              it("letters", x=1000, y=130, text="'LIKELY UNFAIR' (CFPB)", at=C("likely unfair"), size=50, color="gold"),
              it("counter", x=1600, y=520, at=C("refunds went to"), prefix="", suffix="+", steps=[[0, 0], [{"cue": "seventy thousand customers"}, 170000]], text="CUSTOMERS REFUNDED (CFPB EXAMS)")]},
    sources=["apsn"])
add("p18_hundred", "m2_draw", "engine_draw", {
    "title": "100 accounts (CFPB study, rounded)", "board": BOARD, "draw_start": C("Here are one hundred"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        *[{"d": rect(600 + (k % 13) * 62, 380 + (k // 13) * 62, 40, 40), "color": "muted", "width": 3, "kind": "box", "start": C("Here are one hundred", 0.02 * k)} for k in range(91)],
        *[{"d": rect(600 + ((91 + k) % 13) * 62, 380 + ((91 + k) // 13) * 62, 40, 40), "color": "risk", "width": 5, "kind": "box", "start": C("Nine accounts", 0.2 * k)} for k in range(9)],
        {"d": "M 600 880 L 1400 880", "color": "ink", "width": 1, "kind": "stroke", "start": C("And those nine pay"), "label": lbl("9 RED ACCOUNTS PAY ≈ 4 OF EVERY 5 FEE DOLLARS", 1000, 900, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("And those nine pay", 0.1), "dur": 1.4, "target": [1000, 800]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpbfee"])
kinetic("s19_t2", "m2_transition", [("A very profitable model…", 62, "very profitable", None, False),
                                    ("…then the big banks backed away", 60, "backing away", "gold", False)])

# ====================================================================== PART 3: the retreat
card("s20_c3", "m3_card", "The Retreat", "Banks cut the fee")
stage("s21_optin", "m3_optin", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Customers had to say yes"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="JULY 1, 2010: THE OPT-IN RULE (FED)", at=0.3, size=48, color="gold"),
              it("sign", x=1000, y=290, text="ATM + ONE-TIME DEBIT: NO FEE WITHOUT YOUR 'YES'", at=C("Banks could no longer"), color="#BBDEFB", size=32),
              it("creditcard", x=1600, y=520, at=C("Customers had to say yes"), scale=0.6, rot=-8)]},
    sources=["rege"])
stage("s22_capone", "m3_capone", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Weeks later"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="LATE 2021: THE BIG SHIFT", at=0.3, size=50, color="gold"),
              it("sign", x=800, y=250, text="CAPITAL ONE: NO OVERDRAFT, NO NSF FEES", at=C("Capital One announced"), color="#C8E6C9", size=30),
              it("sign", x=1500, y=360, text="WELLS FARGO: NO NSF FEE · 24-HOUR GRACE · $35 KEPT", at=C("Weeks later"), color="#FFE0B2", size=28)]},
    sources=["banks"])
stage("s23_citi", "m3_citi", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And Bank of America"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=750, y=200, text="CITI: OVERDRAFT FEES ENDED (2022)", at=0.3, color="#BBDEFB", size=32),
              it("sign", x=750, y=300, text="CHASE: $50 CUSHION", at=C("Chase added"), color="#FFE0B2", size=32),
              it("counter", x=1550, y=280, at=C("And Bank of America"), prefix="−$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in one year"}, 1.1]], text="BANK OF AMERICA SERVICE CHARGES (2022 10-K)")]},
    sources=["banks"])
stage("s24_total", "m3_total", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "2019", "value": 11.96, "color": "#90A4AE", "at": C("in twenty nineteen") if False else C("It was"), "display": "$11.96BN"},
                     {"label": "2023", "value": 5.83, "color": "#E53935", "at": C("By twenty twenty-three"), "display": "$5.83BN"}],
                    at=0.2, max=14, title="OVERDRAFT + NSF REVENUE, BANKS > $1BN IN ASSETS (CFPB)", x=300, w=900),
              it("letters", x=1550, y=380, text="−51%", at=C("down fifty-one percent"), size=90, color="risk"),
              it("letters", x=1550, y=520, text="≈ $185 / HOUSEHOLD / YEAR SAVED", at=C("saved about"), size=30, color="gold")]},
    sources=["cfpb23"])
add("p25_drop", "m3_draw", "engine_draw", {
    "title": "The drop (CFPB)", "board": BOARD, "draw_start": C("Here is twenty nineteen"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 860 L 1360 860", "color": "ink", "width": 4, "start": C("Let me draw the drop")},
        {"d": "M 680 860 L 680 380 L 860 380 L 860 860", "color": "muted", "width": 5, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Here is twenty nineteen"), "label": lbl("2019 · $11.96BN", 770, 360, 22, "muted")},
        {"d": "M 1000 860 L 1000 626 L 1180 626 L 1180 860", "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("less than half as tall"), "label": lbl("2023 · $5.83BN", 1090, 606, 22, "risk")},
        {"d": "M 1000 380 L 1180 380 L 1180 626", "color": "accent3", "width": 4, "kind": "stroke", "start": C("The banks gave up"), "label": lbl("−$6.13BN", 1250, 500, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("But look at what is left", 0.1), "dur": 1.4, "target": [1090, 740]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpb23"])
kinetic("s26_t3", "m3_transition", [("Regulators went further…", 62, "go further", None, False),
                                    ("…would the $35 fee disappear?", 62, "might disappear", "gold", False)])

# ====================================================================== PART 4: the rule that vanished
card("s27_c4", "m4_card", "The Rule That Vanished", "December 2024 to May 2025")
stage("s28_rule", "m4_rule", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Charge a fee that only"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="CFPB FINAL RULE · BANKS > $10BN", at=0.3, size=48, color="gold"),
              it("sign", x=1000, y=240, text="OPTION 1: A $5 FEE", at=C("no more than"), color="#C8E6C9", size=34),
              it("sign", x=1000, y=340, text="OPTION 2: A FEE THAT COVERS COSTS", at=C("Charge a fee that only"), color="#BBDEFB", size=34),
              it("sign", x=1000, y=440, text="OPTION 3: TREAT IT AS A LOAN", at=C("Or treat the overdraft"), color="#FFE0B2", size=34)]},
    sources=["rule"])
stage("s29_save", "m4_save", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Wells Fargo warned"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=900, y=260, at=0.3, prefix="UP TO $", suffix="BN", steps=[[0, 0], [{"cue": "save consumers"}, 5]], text="A YEAR (CFPB PROJECTION)", scale=1.2),
              it("sign", x=900, y=470, text="≈ $225 PER HOUSEHOLD · START: OCT 2025", at=C("for each\n    household") if False else C("household that pays"), color="#FFE0B2", size=30),
              it("sign", x=1600, y=330, text="WELLS FARGO: 'SIGNIFICANT REDUCTION' EXPECTED", at=C("Wells Fargo warned"), color="#FFCDD2", size=28)]},
    sources=["rule"])
stage("s30_repeal", "m4_repeal", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The House voted"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="IT NEVER TOOK EFFECT", at=0.3, size=54, color="gold"),
              it("sign", x=800, y=230, text="CONGRESSIONAL REVIEW ACT", at=C("Congressional Review Act"), color="#BBDEFB", size=32),
              it("sign", x=1500, y=230, text="SENATE: MARCH · HOUSE: 217–211, APRIL", at=C("The Senate voted"), color="#FFE0B2", size=30)]},
    sources=["repeal"])
stage("s31_signed", "m4_signed", {
    "zones": [Z("parliament", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="PUBLIC LAW 119-10 · MAY 9, 2025", at=0.3, size=50, color="gold"),
              it("docs", x=700, y=560, at=0.4, text="S.J.RES. 18", scale=0.7, stamp="REPEALED", stampAt=C("shall have no")),
              it("sign", x=1350, y=300, text="'SHALL HAVE NO FORCE OR EFFECT'", at=C("shall have no"), color="#FFCDD2", size=34)]},
    sources=["repeal"])
add("p32_timeline", "m4_draw", "engine_draw", {
    "title": "Five months on paper", "board": BOARD, "draw_start": C("December twenty twenty-four, the rule"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 620 L 1420 620", "color": "ink", "width": 5, "start": C("Let me draw the timeline")},
        {"d": rect(600, 470, 220, 80), "color": "accent2", "width": 5, "kind": "box", "start": C("December twenty twenty-four, the rule"), "label": lbl("DEC 2024: RULE", 710, 518, 20, "accent2")},
        {"d": rect(1200, 470, 220, 80), "color": "muted", "width": 5, "kind": "box", "start": C("was supposed to start"), "label": lbl("OCT 2025: START", 1310, 518, 20, "muted")},
        {"d": rect(900, 680, 220, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Congress erases it"), "label": lbl("MAY 2025: ERASED", 1010, 728, 20, "risk")},
        {"d": "M 1010 620 L 1010 675 M 1230 480 L 1390 540 M 1390 480 L 1230 540", "color": "risk", "width": 6, "start": C("The fee cap lived")},
    ],
    "actions": [{"kind": "point", "at": C("only on paper", 0.1), "dur": 1.4, "target": [1010, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["rule", "repeal"])
kinetic("s33_t4", "m4_transition", [("No federal cap…", 66, "So with no federal cap", None, False),
                                    ("…what happened next?", 66, "what happened to the fees", "gold", False)])

# ====================================================================== PART 5: still billions
card("s34_c5", "m5_card", "Still Billions", "What the bank reports show")
stage("s35_2024", "m5_2024", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In its words"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="NO NEW CFPB TOTAL SINCE 2023", at=0.3, size=48, color="white"),
              it("counter", x=1000, y=260, at=C("Bates White estimates"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in twenty twenty-four, about three"}, 6.1]], text="2024, BANKS > $1BN (BATES WHITE ANALYSIS)", scale=1.2),
              it("letters", x=1300, y=470, text="'THE APPARENT END OF STEEP DECLINES'", at=C("In its words"), size=36, color="gold")]},
    sources=["after"])
stage("s36_big", "m5_big", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="CONCENTRATED AT THE TOP", at=0.3, size=52, color="gold"),
              it("counter", x=760, y=280, at=C("counted"), prefix="$", suffix="BN", decimals=2, steps=[[0, 0], [{"cue": "in twenty twenty-four at banks"}, 4.88]], text="2024, BANKS > $10BN (CFA ANALYSIS)"),
              it("counter", x=1500, y=280, at=C("JPMorgan Chase alone"), prefix="≈ $", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "about one billion"}, 1.0]], text="JPMORGAN CHASE (CFA ANALYSIS)")]},
    sources=["after"])
stage("s37_all", "m5_all", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "CFA: BANKS > $10BN", "value": 4.88, "color": "#4FC3F7", "at": 0.4, "display": "$4.88BN"},
                     {"label": "BATES WHITE: BANKS > $1BN", "value": 6.1, "color": "#1E88E5", "at": 0.8, "display": "≈ $6.1BN"},
                     {"label": "INCL. CREDIT UNIONS", "value": 12.1, "color": "#E53935", "at": C("Counting everyone"), "display": "≈ $12.1BN"}],
                    at=0.2, max=14, dark=True, title="OVERDRAFT + NSF FEES IN 2024: THREE ESTIMATES, THREE GROUPS", x=300, w=1100),
              it("letters", x=1640, y=420, text="ESTIMATES", at=C("That is an estimate"), size=44, color="gold")]},
    sources=["after"])
stage("s38_why", "m5_why", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On a small purchase"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="A FLAT FEE", at=0.3, size=60, color="gold"),
              it("sign", x=750, y=260, text="OVERDRAW $2 → $35", at=C("whether you overdraw"), color="#FFCDD2", size=34),
              it("sign", x=1300, y=260, text="OVERDRAW $200 → $35", at=C("or by two hundred"), color="#FFE0B2", size=34),
              it("sign", x=1250, y=400, text="NO FEDERAL CAP · EACH BANK DECIDES", at=C("And without a federal cap"), color="#BBDEFB", size=32)]},
    sources=["banks"])
add("p39_machine", "m5_draw", "engine_draw", {
    "title": "The overdraft machine", "board": BOARD, "draw_start": C("On the left, a customer"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 460, 220, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("On the left, a customer"), "label": lbl("CUSTOMER ≈ $0", 670, 513, 20, "accent2")},
        {"d": rect(880, 460, 220, 90), "color": "ink", "width": 5, "kind": "box", "start": C("In the middle, the bank"), "label": lbl("BANK PAYS $24", 990, 513, 20, "ink")},
        {"d": rect(1200, 460, 220, 90), "color": "risk", "width": 5, "kind": "box", "start": C("On the right, the fee"), "label": lbl("FEE $35", 1310, 513, 22, "risk")},
        {"d": arrow((785, 505), (875, 505)) + " " + arrow((1105, 505), (1195, 505)), "color": "ink", "width": 4, "kind": "arrow", "start": C("In the middle, the bank", 0.4)},
        {"d": arrow((1310, 560), (670, 560), -0.35), "color": "accent", "width": 5, "kind": "arrow", "start": C("Then the next month"), "label": lbl("NEXT MONTH, AGAIN", 990, 760, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("the same\n    loop") if False else C("the same loop", 0.0), "dur": 1.4, "target": [990, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["cfpbfee", "banks"])

# ====================================================================== PAYOFF
stage("s40_payoff", "payoff", {
    "zones": [Z("bankhall", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("Banks cut it in"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="SMALL FOR MOST · HUGE FOR A FEW", at=0.3, size=54, color="gold"),
              it("sign", x=800, y=280, text="CUT IN HALF UNDER PRESSURE", at=C("Banks cut it in"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=280, text="THE CAP: ERASED", at=C("The cap that would"), color="#FFCDD2", size=32),
              it("sign", x=1100, y=400, text="TIP: CHECK YOUR OPT-IN", at=C("check whether you opted in"), color="#FFF9C4", size=34)]},
    sources=["cfpb23", "repeal"])
add("s41_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_overdraft_storyboard.py; edit the generator, not this file.\n"
           "# Episode 46 storyboard (overdraft fees): one visual language per part; tones from visual_direction.yaml.\n")
