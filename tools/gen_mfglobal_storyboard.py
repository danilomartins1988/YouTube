"""Generates projects/mf-global-the-billion-dollars-that-vanished/deliverables/documentary/storyboard.yaml
(Episode 50, new topics N10: MF Global: The $1.6 Billion That Vanished).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the financial district at night with a giant counter; the farm.
- Part 1 (the firm): the farm (hedging), the glass box of customer money (new `glassbox` item), a segregation drawing.
- Part 2 (the bet): the exchange floor, the office, an invisible-bet drawing.
- Part 3 (the last week): the district at night, trading screens, a seven-day timeline.
- Part 4 (the missing money): the Senate hearing (parliament), the farm at dusk, a hole drawing.
- Part 5 (the aftermath): the court, the office, a repaired-box drawing.
No logos, no real people drawn (names in text only). Lint: tools/lint_storyboard.py.
Run: python tools/gen_mfglobal_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/mf-global-the-billion-dollars-that-vanished/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.05, prefix="≈ $", suffix="BN", decimals=1, steps=[[0.05, 0], [1.5, 1.6]], text="CUSTOMER MONEY MISSING, OCT 2011 (TRUSTEE)", scale=1.4),
              it("glassbox", x=1000, y=560, at=0.4, scale=0.7, fill=0.8, drainAt=0.8, drainTo=0.2, crackAt=0.9)]},
    sources=["trustee"])
stage("s02_twist", "h_twist", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("Among them"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="NOT THE FIRM'S MONEY", at=0.3, size=60, color="gold"),
              it("sign", x=1200, y=280, text="CO-OPS REPRESENTING UP TO 35,000 FARMERS", at=C("Among them"), color="#FFE0B2", size=32),
              *crowd([600, 1500], "worry", at=0.5, scale=0.75)]},
    sources=["house"])
stage("s03_question", "h_question", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="WHERE DID IT GO? DID IT COME BACK?", at=0.3, size=58, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · YOUR MONEY AT A BROKER", at=C("what a futures broker"), color="#BBDEFB", size=30),
              it("sign", x=960, y=380, text="2 · THE BET", at=C("the bet that sank"), color="#FFE0B2", size=34),
              it("sign", x=1560, y=380, text="3 · THE LAST WEEK", at=C("its last week"), color="#C8E6C9", size=34),
              it("letters", x=960, y=700, text="FOLLOW THE MISSING MONEY", at=0.4, size=64, color="gold")]})

# ====================================================================== PART 1: the firm
card("s05_c1", "m1_card", "The Firm", "A futures broker")
stage("s06_broker", "m1_broker", {
    "zones": [Z("farm")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A cattle rancher"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="HEDGING", at=0.3, size=64, color="gold"),
              it("sign", x=800, y=250, text="LOCK IN A CORN PRICE BEFORE HARVEST", at=C("A farmer could lock"), color="#C8E6C9", size=30),
              it("sign", x=1500, y=350, text="PROTECT AGAINST FALLING BEEF PRICES", at=C("A cattle rancher"), color="#FFE0B2", size=30)]},
    sources=["house"])
stage("s07_rule", "m1_rule", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It sits in segregated"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="THE RULE: 'SHALL NOT BE COMMINGLED'", at=C("shall not be commingled"), size=48, color="gold"),
              it("letters", x=1000, y=110, text="CUSTOMER DEPOSITS", at=0.3, until=C("shall not be commingled"), size=56, color="gold"),
              it("glassbox", x=1000, y=520, at=C("It sits in segregated"), scale=0.85, fill=0.8, label="SEGREGATED · CUSTOMERS ONLY")]},
    sources=["senate"])
stage("s08_trust", "m1_trust", {
    "zones": [Z("farm", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("He had about"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="'NO CUSTOMER HAS EVER LOST A PENNY'", at=C("no customer had ever lost"), size=46, color="gold"),
              it("counter", x=1250, y=320, at=C("He had about"), prefix="$", suffix="", steps=[[0, 0], [{"cue": "when it was frozen"}, 253000]], text="ONE FARMER'S FROZEN ACCOUNT (SENATE TESTIMONY)"),
              *crowd([600], "worry", at=0.4, scale=0.8)]},
    sources=["senate"])
stage("s09_size", "m1_size", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A senator later"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=800, y=250, at=0.3, prefix="≈ ", suffix="", steps=[[0, 0], [{"cue": "futures customers"}, 36000]], text="FUTURES CUSTOMERS (HOUSE REPORT)"),
              it("sign", x=1400, y=250, text="+ 318 SECURITIES CUSTOMERS", at=C("more\n    than three hundred") if False else C("three hundred securities"), color="#BBDEFB", size=32),
              it("letters", x=1100, y=430, text="'THE EIGHTH LARGEST BANKRUPTCY IN U.S. HISTORY'", at=C("A senator later"), size=38, color="gold")]},
    sources=["house", "senate"])
add("p10_box", "m1_draw", "engine_draw", {
    "title": "The glass box (segregation)", "board": BOARD, "draw_start": C("Here is the firm"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(760, 420, 260, 260), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the firm"), "label": lbl("FIRM'S MONEY", 890, 558, 22, "accent2")},
        {"d": rect(1200, 420, 260, 260), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the customer box"), "label": lbl("CUSTOMER BOX", 1330, 558, 22, "accent3")},
        {"d": arrow((1330, 330), (1330, 415)), "color": "accent", "width": 5, "kind": "arrow", "start": C("Farmers put their deposits"), "label": lbl("DEPOSITS", 1330, 310, 20, "accent")},
        {"d": "M 1110 380 L 1110 720", "color": "risk", "width": 8, "start": C("That line in the middle"), "label": lbl("THE LINE", 1110, 750, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the whole system", 0.1), "dur": 1.4, "target": [1110, 560]}],
    "scale": 0.86, "floor": 1040}, sources=["senate"])
kinetic("s11_t1", "m1_transition", [("In 2010…", 76, "In twenty ten", None, False),
                                    ("…a new CEO, a new strategy", 64, "a new strategy", "gold", False)])

# ====================================================================== PART 2: the bet
card("s12_c2", "m2_card", "The Bet", "European government bonds")
stage("s13_ceo", "m2_ceo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Over the next year"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="MARCH 2010: JON CORZINE, CHAIRMAN AND CEO", at=0.3, size=44, color="gold"),
              it("sign", x=1250, y=280, text="A BIG TRADING POSITION WITH ITS OWN MONEY", at=C("Over the next year"), color="#FFE0B2", size=32)]},
    sources=["cftc"])
stage("s14_bonds", "m2_bonds", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In twenty eleven"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=230, at=C("disclosed a position of"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "in short-term bonds"}, 6.3]], text="EUROPEAN GOVERNMENT BONDS (8-K, SEP 30, 2011)", scale=1.3),
              it("sign", x=1000, y=420, text="BELGIUM · ITALY · SPAIN · PORTUGAL · IRELAND", at=C("Belgium"), color="#BBDEFB", size=32),
              it("letters", x=1000, y=110, text="THE BIGGEST BET", at=0.3, until=C("disclosed a position of"), size=56, color="gold")]},
    sources=["sec"])
stage("s15_repo", "m2_repo", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But as the industry regulator"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="'REPO TO MATURITY'", at=0.3, size=60, color="gold"),
              it("sign", x=800, y=250, text="TREATED AS SALES → OFF THE BALANCE SHEET", at=C("treated as sales"), color="#FFE0B2", size=30),
              it("sign", x=1400, y=360, text="'REMAINED SUBJECT TO MARKET AND CREDIT RISK' (FINRA)", at=C("But as the industry regulator"), color="#FFCDD2", size=28)]},
    sources=["senate", "house"])
stage("s16_capital", "m2_capital", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The news was in"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=200, text="FINRA: HOLD MORE CAPITAL", at=0.3, color="#BBDEFB", size=34),
              it("counter", x=1400, y=230, at=C("The extra charges"), prefix="≈ $", suffix="M", steps=[[0, 0], [{"cue": "million dollars"}, 257]], text="EXTRA CAPITAL CHARGES (HOUSE REPORT)"),
              it("docs", x=700, y=560, at=C("The news was in"), text="AMENDED 10-Q · SEPT 2011", scale=0.65, stamp="FEW NOTICED", stampAt=C("few people noticed"))]},
    sources=["house"])
add("p17_hidden", "m2_draw", "engine_draw", {
    "title": "The invisible bet (illustration)", "board": BOARD, "draw_start": C("Here is the balance sheet"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 420, 300, 280), "color": "ink", "width": 6, "kind": "box", "start": C("Here is the balance sheet"), "label": lbl("BALANCE SHEET", 710, 400, 22, "ink")},
        {"d": rect(1080, 460, 240, 160), "color": "accent", "width": 5, "kind": "box", "start": C("Here are six point three"), "label": lbl("$6.3BN BONDS (OFF THE PAGE)", 1200, 545, 16, "accent")},
        {"d": "M 860 560 Q 970 500 1075 540", "color": "risk", "width": 4, "kind": "stroke", "start": C("And here is the risk"), "label": lbl("RISK STILL ATTACHED", 970, 480, 18, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the string pulled", 0.1), "dur": 1.4, "target": [970, 520]}],
    "scale": 0.86, "floor": 1040}, sources=["sec", "senate"])
kinetic("s18_t2", "m2_transition", [("October 2011…", 72, "In October twenty eleven", None, False),
                                    ("…the string pulled hard", 66, "pull very hard", "gold", False)])

# ====================================================================== PART 3: the last week
card("s19_c3", "m3_card", "The Last Week", "October 24 to 31, 2011")
stage("s20_downgrade", "m3_downgrade", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The next day"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=200, text="MON OCT 24: ONE NOTCH ABOVE JUNK (MOODY'S)", at=0.3, color="#FFE0B2", size=30),
              it("counter", x=1400, y=320, at=C("The next day"), prefix="−$", suffix="M", decimals=1, steps=[[0, 0], [{"cue": "and disclosed"}, 191.6]], text="TUE OCT 25: QUARTERLY LOSS (8-K)")]},
    sources=["house", "sec"])
stage("s21_run", "m3_run", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A broker that lives"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="CONFIDENCE COLLAPSES", at=0.3, size=58, color="gold"),
              it("sign", x=1000, y=280, text="THU OCT 27: JUNK (MOODY'S AND FITCH)", at=C("On Thursday"), color="#FFCDD2", size=34),
              it("tradescreen", x=1500, y=500, at=0.4, scale=0.55, price=[[0, 80], [3, 60], [6, 30], [9, 10]], max=100, min=0, suffix="", text="MARKET CONFIDENCE (ILLUSTRATION)")]},
    sources=["house"])
stage("s22_glass", "m3_glass", {
    "zones": [Z("vault", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The Commodity Futures"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("glassbox", x=1000, y=520, at=0.2, scale=0.85, fill=0.85, crackAt=C("the firm used customer money"), drainAt=C("supposed to stay"), drainTo=0.35, label="SEGREGATED · CUSTOMERS ONLY"),
              it("letters", x=1000, y=110, text="'NEARLY ONE BILLION DOLLARS' UNLAWFULLY USED (CFTC)", at=C("The Commodity Futures"), size=40, color="gold")]},
    sources=["cftc"])
stage("s23_fall", "m3_fall", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("When the trustee opened"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1100, y=130, text="MON OCT 31, 2011: BANKRUPTCY", at=0.3, size=52, color="gold"),
              it("docs", x=700, y=560, at=0.4, text="CHAPTER 11 · SIPA LIQUIDATION", scale=0.7, stamp="FILED", stampAt=C("filed for bankruptcy")),
              it("sign", x=1300, y=300, text="THE CUSTOMER ACCOUNTS DID NOT ADD UP", at=C("When the trustee opened"), color="#FFCDD2", size=32),
              it("gavel", x=1650, y=F - 20, hits=[C("filed for bankruptcy")], at=0.2)]},
    sources=["sec", "trustee"])
add("p24_week", "m3_draw", "engine_draw", {
    "title": "Seven days (sourced dates)", "board": BOARD, "draw_start": C("Monday, the downgrade"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 620 L 1500 620", "color": "ink", "width": 5, "start": C("Let me draw the last week")},
        {"d": rect(760, 480, 160, 80), "color": "accent", "width": 4, "kind": "box", "start": C("Monday, the downgrade"), "label": lbl("MON 24: DOWNGRADE", 840, 527, 16, "accent")},
        {"d": rect(950, 660, 160, 80), "color": "accent", "width": 4, "kind": "box", "start": C("Tuesday"), "label": lbl("TUE 25: LOSS + BET", 1030, 707, 16, "accent")},
        {"d": rect(1140, 480, 160, 80), "color": "risk", "width": 4, "kind": "box", "start": C("Thursday, junk"), "label": lbl("THU 27: JUNK", 1220, 527, 16, "risk")},
        {"d": rect(1330, 660, 170, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Monday,\n    bankruptcy") if False else C("bankruptcy. Seven days") if False else C("Seven days"), "label": lbl("MON 31: BANKRUPT", 1415, 707, 16, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("could not find", 0.1), "dur": 1.4, "target": [1415, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["house", "sec"])
kinetic("s25_t3", "m3_transition", [("A simple, terrifying question…", 60, "simple, and terrifying", None, False),
                                    ("…where did the money go?", 66, "Where did the money go", "gold", False)])

# ====================================================================== PART 4: the missing money
card("s26_c4", "m4_card", "The Missing Money", "The trustee's count")
stage("s27_estimates", "m4_estimates", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [chart([{"label": "NOV 2011", "value": 1.2, "color": "#90A4AE", "at": C("In November"), "display": "≥ $1.2BN"},
                     {"label": "JUN 2012", "value": 1.6, "color": "#E53935", "at": C("By June twenty twelve"), "display": "≈ $1.6BN"}],
                    at=0.2, max=2, title="SHORTFALL ESTIMATES (SIPA TRUSTEE)", x=300, w=800),
              it("sign", x=1500, y=300, text="≈ $900M U.S. ACCOUNTS", at=C("in American accounts"), color="#BBDEFB", size=30),
              it("sign", x=1500, y=400, text="≈ $700M FOREIGN EXCHANGES", at=C("trading on foreign exchanges"), color="#FFE0B2", size=30)]},
    sources=["trustee"])
stage("s28_farmer", "m4_farmer", {
    "zones": [Z("farm", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("His words were blunt"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("sign", x=800, y=200, text="HEDGES CLOSED: 'WELL OVER AN ADDITIONAL $100,000'", at=C("forced\n    to close") if False else C("to close his hedges"), color="#FFE0B2", size=28),
              it("letters", x=1200, y=330, text="'COMMINGLING MONEY IS STEALING MONEY'", at=C("His words were blunt"), size=46, color="gold"),
              *crowd([600], "worry", at=0.4, scale=0.8)]},
    sources=["senate"])
stage("s29_senate", "m4_senate", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And a senator"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=110, text="SENATE AGRICULTURE COMMITTEE · DEC 2011", at=0.3, size=44, color="white"),
              it("sign", x=800, y=250, text="'THE SANCTITY OF SEGREGATED FUNDS'", at=C("the sanctity"), color="#BBDEFB", size=32),
              it("sign", x=1400, y=350, text="'THE MOST SACRED RULE OF THE FUTURES INDUSTRY'", at=C("And a senator"), color="#FFCDD2", size=28)]},
    sources=["senate"])
add("p30_hole", "m4_draw", "engine_draw", {
    "title": "The hole (trustee's split)", "board": BOARD, "draw_start": C("Here is the glass box"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(620, 400, 320, 320), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the glass box"), "label": lbl("AS IT SHOULD BE", 780, 380, 20, "accent3")},
        {"d": rect(1040, 400, 320, 320), "color": "risk", "width": 6, "kind": "box", "start": C("Here is what the trustee found"), "label": lbl("WHAT WAS FOUND", 1200, 380, 20, "risk")},
        {"d": "M 1060 420 L 1340 420 L 1340 560 L 1060 560 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.25, "kind": "bar", "start": C("A gap of about"), "label": lbl("≈ $1.6BN GAP", 1200, 500, 22, "risk")},
        {"d": "M 1200 560 L 1200 700", "color": "ink", "width": 3, "start": C("On one side"), "label": lbl("U.S. ≈ $900M | ABROAD ≈ $700M", 1200, 760, 18, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("thousands of customers waiting", 0.1), "dur": 1.4, "target": [1200, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["trustee"])
kinetic("s31_t4", "m4_transition", [("The long work of getting it back…", 58, "the long work", None, False),
                                    ("…and of who was responsible", 62, "held responsible", "gold", False)])

# ====================================================================== PART 5: the aftermath
card("s32_c5", "m5_card", "The Aftermath", "2013 to 2017")
stage("s33_back", "m5_back", {
    "zones": [Z("farm")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The biggest group"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=230, at=C("In total"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "had gone back"}, 6.7]], text="RETURNED TO 26,000+ CUSTOMERS BY APRIL 2014 (TRUSTEE)", scale=1.3),
              it("sign", x=1000, y=470, text="'100 PERCENT WHOLE' · ≈ 2.5 YEARS LATER", at=C("In his words"), color="#C8E6C9", size=32),
              it("letters", x=1000, y=110, text="PAID BACK IN STAGES", at=0.3, size=54, color="gold"),
              *crowd([500, 1600], "cheer", at=C("one hundred percent whole"), scale=0.75)]},
    sources=["trustee"])
stage("s34_order", "m5_order", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1100, y=130, text="CFTC ORDER · NOV 2013", at=0.3, size=52, color="gold"),
              it("counter", x=1100, y=290, at=C("to pay"), prefix="$", suffix="BN", decimals=3, steps=[[0, 0], [{"cue": "in restitution"}, 1.212]], text="RESTITUTION TO CUSTOMERS"),
              it("sign", x=1100, y=450, text="+ $100M PENALTY, AFTER CUSTOMERS ARE PAID", at=C("plus a one hundred million"), color="#FFE0B2", size=30),
              it("gavel", x=1650, y=F - 20, hits=[C("a federal court order")], at=0.2)]},
    sources=["cftc"])
stage("s35_corzine", "m5_corzine", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("He settled without"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="CFTC v. CORZINE · JAN 2017", scale=0.7, stamp="SETTLED", stampAt=C("settled the regulator's")),
              it("sign", x=1350, y=220, text="$5M CIVIL PENALTY · NEVER TO REGISTER AGAIN", at=C("He agreed to pay"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=330, text="NO ADMISSION OR DENIAL · NOT CRIMINALLY CHARGED", at=C("He settled without"), color="#BBDEFB", size=28)]},
    sources=["cftc"])
stage("s36_rules", "m5_rules", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The chairman of the commission"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("glassbox", x=1000, y=540, at=0.3, scale=0.8, fill=0.8, watchAt=C("report their segregated accounts"), label="SEGREGATED · WATCHED DAILY"),
              it("letters", x=1000, y=110, text="NEW RULES (CFTC, 2013)", at=0.3, until=C("The chairman of the commission"), size=56, color="gold"),
              it("letters", x=1000, y=110, text="'THE CORE FOUNDATION' OF THE MARKETS", at=C("The chairman of the commission"), size=48, color="gold")]},
    sources=["cftc"])
add("p37_repair", "m5_draw", "engine_draw", {
    "title": "The repaired box (2013 rules)", "board": BOARD, "draw_start": C("Here is the glass box again"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(940, 440, 300, 280), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the glass box again"), "label": lbl("CUSTOMER MONEY", 1090, 588, 22, "accent3")},
        {"d": rect(1300, 380, 120, 60), "color": "accent2", "width": 4, "kind": "box", "start": C("Now add a camera"), "label": lbl("DAILY REPORT", 1360, 360, 18, "accent2")},
        {"d": rect(780, 560, 110, 60), "color": "accent", "width": 4, "kind": "box", "start": C("a second key"), "label": lbl("2ND KEY", 835, 540, 18, "accent")},
        {"d": "M 1240 600 L 1420 600 L 1420 720", "color": "ink", "width": 4, "start": C("a phone line"), "label": lbl("REGULATOR", 1420, 750, 18, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("watching the lock", 0.1), "dur": 1.4, "target": [1090, 580]}],
    "scale": 0.86, "floor": 1040}, sources=["cftc"])

# ====================================================================== PAYOFF
stage("s38_payoff", "payoff", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("The farmers got"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=120, text="A HIDDEN BET · A BROKEN RULE", at=0.3, size=56, color="gold"),
              it("sign", x=800, y=260, text="MONEY BACK, AFTER YEARS", at=C("The farmers got"), color="#C8E6C9", size=32),
              it("sign", x=1400, y=260, text="A RULE WORKS ONLY IF SOMEONE CHECKS", at=C("The lesson is"), color="#FFE0B2", size=30)]},
    sources=["trustee", "cftc"])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_mfglobal_storyboard.py; edit the generator, not this file.\n"
           "# Episode 50 storyboard (MF Global): one visual language per part; tones from visual_direction.yaml.\n")
