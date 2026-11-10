"""Generates projects/how-prediction-markets-make-money-off-your-hunches/deliverables/documentary/storyboard.yaml
(Episode 45, new topics N5: How Prediction Markets Make Money Off Your Hunches).

Diversity rules (docs/ANALYSIS_HOOKS_THUMBS_VISUALS.md), one visual language per part:
- Hook: the exchange floor with a giant counter; the stadium at night (new `stadium` set).
- Part 1 (the contract): yes/no tickets (new `yesno` item), the exchange, a matched-contract drawing.
- Part 2 (the toll): the studio (formula), trading screens, a toll-curve drawing.
- Part 3 (mostly sports): the stadium, the exchange (Wall Street money), a pie drawing.
- Part 4 (the fight): the courtroom, Congress, a tug-of-war drawing.
- Part 5 (the house always gets paid): the studio, a business-model drawing.
No company or league logos (names in text only), no real people drawn. Lint: tools/lint_storyboard.py.
Run: python tools/gen_predmkt_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/how-prediction-markets-make-money-off-your-hunches/deliverables/documentary/storyboard.yaml"
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
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 480, "zoom": 1.15}, {"at": 1.0, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 2,
    "items": [it("counter", x=1000, y=200, at=0.05, prefix="$", suffix="BN", steps=[[0.05, 0], [1.5, 25]], text="EVENT CONTRACTS TRADED, MARCH 2026 (CFTC)", scale=1.4),
              it("sign", x=1000, y=450, text="ELECTIONS · RATES · SPORTS", at=C("Contracts on elections"), color="#FFE0B2", size=38)]},
    sources=["cftc"])
stage("s02_twist", "h_twist", {
    "zones": [Z("stadium", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.05}, {"at": C("They\n    do not need") if False else C("They do"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="NOT BETTING AGAINST YOU?", at=0.3, size=60, color="gold"),
              it("sign", x=1200, y=300, text="THEY JUST NEED YOU TO TRADE", at=C("They just need"), color="#FFCDD2", size=38)]},
    sources=["kalshi"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.15}, {"at": 0.8, "x": 1000, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="FINANCE… OR GAMBLING?", at=0.3, size=72, color="gold")]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=360, y=380, text="1 · THE YES/NO CONTRACT", at=C("yes-or-no contract works"), color="#BBDEFB", size=32),
              it("sign", x=960, y=380, text="2 · WHERE THE FEE HIDES", at=C("where the fee hides"), color="#FFE0B2", size=32),
              it("sign", x=1560, y=380, text="3 · THE COURTS", at=C("why the courts"), color="#C8E6C9", size=32),
              it("letters", x=960, y=700, text="FOLLOW THE TOLL", at=0.4, size=72, color="gold")]})

# ====================================================================== PART 1: the contract
card("s05_c1", "m1_card", "The Contract", "One question, one dollar")
stage("s06_how", "m1_how", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=150, text="A YES-OR-NO QUESTION", at=0.3, size=60, color="gold"),
              it("yesno", x=960, y=480, at=C("Will this team win"), q="WILL THE HOME TEAM WIN TONIGHT?", yes=50, settle="yes", settleAt=C("a yes contract pays"))]},
    sources=["kalshi"])
stage("s07_price", "m1_price", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The price\n    is the prediction") if False else C("is the prediction"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("yesno", x=1000, y=420, at=0.3, q="WILL IT HAPPEN?", yes=[[0, 40], [{"cue": "sixty-five cents"}, 65]]),
              it("letters", x=1200, y=150, text="PRICE = THE CROWD'S ODDS (≈ 65%)", at=C("the crowd is saying"), size=46, color="gold")]},
    sources=["kalshi"])
stage("s08_member", "m1_member", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Someone buys yes"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="NOT A SPORTSBOOK", at=0.3, until=C("you are always"), size=56, color="gold"),
              it("letters", x=1000, y=130, text="'AGAINST ANOTHER MEMBER … NOT THE EXCHANGE' (KALSHI)", at=C("you are always"), size=38, color="gold"),
              it("sign", x=700, y=300, text="BUYER OF YES", at=C("Someone buys yes"), color="#C8E6C9", size=36),
              it("sign", x=1300, y=300, text="BUYER OF NO", at=C("Someone else buys no"), color="#FFCDD2", size=36),
              it("sign", x=1000, y=420, text="THE EXCHANGE MATCHES THEM", at=C("matches them in the middle"), color="#BBDEFB", size=34)]},
    sources=["kalshi"])
stage("s09_regulated", "m1_regulated", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="AN EXCHANGE, NOT A BOOKMAKER", at=0.3, size=54, color="gold"),
              it("docs", x=700, y=560, at=C("designated it as a contract market"), text="CFTC DESIGNATION · NOV 2020", scale=0.7, stamp="LICENSED", stampAt=C("The same kind of license")),
              it("sign", x=1350, y=300, text="SAME KIND OF LICENSE AS FUTURES EXCHANGES", at=C("The same kind of license"), color="#BBDEFB", size=30)]},
    sources=["cftc"])
add("p10_match", "m1_draw", "engine_draw", {
    "title": "One contract (illustration)", "board": BOARD, "draw_start": C("Here is the question"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(860, 330, 320, 80), "color": "ink", "width": 6, "kind": "box", "start": C("Here is the question"), "label": lbl("THE QUESTION", 1020, 378, 24, "ink")},
        {"d": rect(660, 520, 220, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("a buyer of yes"), "label": lbl("YES · 65¢", 770, 573, 24, "accent3")},
        {"d": rect(1160, 520, 220, 90), "color": "risk", "width": 5, "kind": "box", "start": C("a buyer of no"), "label": lbl("NO · 35¢", 1270, 573, 24, "risk")},
        {"d": rect(910, 700, 220, 90), "color": "accent", "width": 5, "kind": "box", "start": C("Together, they put in"), "label": lbl("$1 HELD", 1020, 753, 24, "accent")},
        {"d": arrow((800, 615), (930, 700)) + " " + arrow((1240, 615), (1110, 700)), "color": "ink", "width": 4, "kind": "arrow", "start": C("Together, they put in", 0.4)},
        {"d": arrow((1020, 795), (1020, 880)), "color": "accent", "width": 5, "kind": "arrow", "start": C("one side takes the whole"), "label": lbl("TO THE WINNER", 1150, 860, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("The exchange simply holds", 0.1), "dur": 1.4, "target": [1020, 745]}],
    "scale": 0.86, "floor": 1040}, sources=["kalshi"])
kinetic("s11_t1", "m1_transition", [("The exchange never takes a side…", 60, "never takes a side", None, False),
                                    ("…so where is the money?", 66, "where does its money", "gold", False)])

# ====================================================================== PART 2: the toll
card("s12_c2", "m2_card", "The Toll", "A fee on every trade")
stage("s13_fee", "m2_fee", {
    "zones": [Z("tollzone" if False else "highway")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Not on who wins"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("tollbooth", x=1100, at=0.3, fee="FEE PER TRADE", rate=1.2),
              it("letters", x=1000, y=130, text="'A TRANSACTION FEE ON THE EXPECTED EARNINGS' (KALSHI)", at=C("In its own words"), size=36, color="gold"),
              it("sign", x=1100, y=260, text="WIN OR LOSE", at=C("On every trade"), color="#FFCDD2", size=40)]},
    sources=["kalshi"])
stage("s14_formula", "m2_formula", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=200, text="FEE = 7% × CONTRACTS × PRICE × (1 − PRICE)", at=C("Seven percent"), size=52, color="gold"),
              it("letters", x=960, y=300, text="(FORMULA FILED WITH THE CFTC, 2022)", at=0.3, size=30, color="white"),
              it("counter", x=960, y=520, at=C("At a price of fifty cents"), prefix="≈ ", suffix="¢", decimals=2, steps=[[0, 0], [{"cue": "per contract"}, 1.75]], text="FEE PER CONTRACT AT 50¢ (ROUNDED UP)", scale=1.3)]},
    sources=["kalshi"])
stage("s15_shape", "m2_shape", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [chart([{"label": "PRICE 10¢", "value": 0.63, "color": "#90A4AE", "at": C("It shrinks near zero"), "display": "0.63¢"},
                     {"label": "PRICE 30¢", "value": 1.47, "color": "#4FC3F7", "at": C("It shrinks near zero", 0.5), "display": "1.47¢"},
                     {"label": "PRICE 50¢", "value": 1.75, "color": "#E53935", "at": C("The fee is biggest"), "display": "1.75¢"},
                     {"label": "PRICE 70¢", "value": 1.47, "color": "#4FC3F7", "at": C("near one dollar"), "display": "1.47¢"},
                     {"label": "PRICE 90¢", "value": 0.63, "color": "#90A4AE", "at": C("near one dollar", 0.5), "display": "0.63¢"}],
                    at=0.2, max=2, title="FEE PER CONTRACT BY PRICE (OUR CALC., FILED FORMULA)", x=300, w=1300)]},
    sources=["kalshi"])
stage("s16_poly", "m2_poly", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And traders who post"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=120, text="POLYMARKET US: THE SAME SHAPE (CFTC FILING)", at=0.3, size=44, color="gold"),
              it("sign", x=800, y=270, text="TAKERS: 6.95% × P × (1 − P)", at=C("its rate for traders"), color="#FFCDD2", size=34),
              it("sign", x=1500, y=270, text="MAKERS: A SMALL REBATE", at=C("And traders who post"), color="#C8E6C9", size=34)]},
    sources=["poly"])
stage("s17_spread", "m2_spread", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And Kalshi has said"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("tradescreen", x=800, y=420, at=0.3, scale=0.8, price=[[0, 48], [3, 52], [6, 49], [9, 53], [12, 50]], max=100, min=0, suffix="¢", text="ONE CONTRACT · YES PRICE (ILLUSTRATION)"),
              it("letters", x=1000, y=110, text="MARKET MAKERS: 'COLLECTING THE SPREAD'", at=C("make money by collecting"), size=44, color="gold"),
              it("sign", x=1550, y=300, text="A KALSHI AFFILIATE TRADES TOO", at=C("And Kalshi has said"), color="#FFE0B2", size=32),
              it("sign", x=1550, y=400, text="YOUR OTHER SIDE MAY BE A PRO", at=C("may be a professional"), color="#FFCDD2", size=32)]},
    sources=["kalshi"])
add("p18_hill", "m2_draw", "engine_draw", {
    "title": "The toll curve (filed formula)", "board": BOARD, "draw_start": C("Along the bottom, the price"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 840 L 1400 840", "color": "ink", "width": 4, "start": C("Along the bottom, the price"), "label": lbl("PRICE: 0¢ → $1", 1000, 880, 22, "ink")},
        {"d": "M 600 840 L 600 420", "color": "ink", "width": 4, "start": C("Up the side, the fee"), "label": lbl("FEE", 570, 410, 22, "ink")},
        {"d": "M 600 840 Q 1000 100 1400 840", "color": "risk", "width": 7, "kind": "stroke", "start": C("It starts\n    near zero") if False else C("climbs to its peak")},
        {"d": rect(940, 410, 120, 60), "color": "accent", "width": 5, "kind": "box", "start": C("A hill, with the toll booth"), "label": lbl("TOLL", 1000, 448, 22, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("most uncertain", 0.1), "dur": 1.4, "target": [1000, 470]}],
    "scale": 0.86, "floor": 1040}, sources=["kalshi"])
kinetic("s19_t2", "m2_transition", [("A small toll on a huge number of trades…", 56, "A small toll", None, False),
                                    ("…and the biggest source is not politics", 54, "is not politics", "gold", False)])

# ====================================================================== PART 3: mostly sports
card("s20_c3", "m3_card", "Mostly Sports", "Where the volume is")
stage("s21_share", "m3_share", {
    "zones": [Z("stadium", label="HOME 2 – 1 AWAY")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("By our\n    calculation") if False else C("By our"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="PEW ANALYSIS OF THE BLOCK DATA · JULY 2026", at=0.3, size=40, color="white"),
              it("sign", x=800, y=300, text="KALSHI: ≈ 78% SPORTS", at=C("By our"), color="#BBDEFB", size=36),
              it("sign", x=1400, y=300, text="POLYMARKET: ≈ 82% SPORTS", at=C("By our", 0.6), color="#FFE0B2", size=36)]},
    sources=["pew"])
stage("s22_growth", "m3_growth", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("None of those numbers"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="KALSHI'S OWN CLAIMS (OCT 2026)", at=0.3, size=48, color="gold"),
              it("sign", x=700, y=250, text="'ANNUALIZED VOLUME > $1 TRILLION'", at=C("annualized trading volume"), color="#BBDEFB", size=30),
              it("sign", x=1300, y=250, text="'OVER 75% OF THE MARKET'", at=C("over seventy-five percent"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=350, text="$1BN RAISED AT A $40BN VALUATION", at=C("It raised one billion"), color="#FFE0B2", size=32),
              it("docs", x=1700, y=560, at=C("None of those numbers"), text="AUDITED?", scale=0.6, stamp="NOT AUDITED", stampAt=C("audited figure"))]},
    sources=["kalshi"])
stage("s23_ice", "m3_ice", {
    "zones": [Z("district")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="WALL STREET NOTICED", at=0.3, size=58, color="gold"),
              it("counter", x=1000, y=300, at=C("said it would"), prefix="UP TO $", suffix="BN", steps=[[0, 0], [{"cue": "in Polymarket"}, 2]], text="ICE INVESTMENT IN POLYMARKET (8-K)", scale=1.2),
              it("sign", x=1000, y=470, text="≈ $8BN VALUATION BEFORE THE INVESTMENT", at=C("at a valuation"), color="#FFE0B2", size=32)]},
    sources=["poly"])
stage("s24_books", "m3_books", {
    "zones": [Z("stadium", night=True, label="HOME 0 – 0 AWAY")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The NBA named"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="THE SPORTSBOOKS JOIN IN", at=0.3, size=52, color="gold"),
              it("sign", x=750, y=200, text="DRAFTKINGS PREDICTIONS (DEC 2025)", at=C("DraftKings launched"), color="#C8E6C9", size=30),
              it("sign", x=750, y=300, text="FANDUEL PREDICTS + CME (DEC 2025)", at=C("FanDuel launched"), color="#BBDEFB", size=30),
              it("sign", x=1500, y=250, text="NBA: 'PREFERRED PREDICTION MARKET EXCHANGES'", at=C("The NBA named"), color="#FFE0B2", size=28)]},
    sources=["books"])
add("p25_pie", "m3_draw", "engine_draw", {
    "title": "Where the volume goes (Pew/The Block, rounded)", "board": BOARD, "draw_start": C("Here is one big circle"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 1150 600 m -220 0 a 220 220 0 1 0 440 0 a 220 220 0 1 0 -440 0", "color": "ink", "width": 6, "kind": "stroke", "start": C("Here is one big circle"), "label": lbl("ALL TRADING, JULY", 1150, 350, 22, "ink")},
        {"d": "M 1150 600 L 1150 380 M 1150 600 L 1359 532", "color": "accent2", "width": 6, "kind": "stroke", "start": C("Now cut it"), "label": lbl("POLITICS, ECONOMY, OTHER", 1420, 430, 18, "accent2")},
        {"d": "M 1000 640 L 1080 640", "color": "risk", "width": 1, "kind": "stroke", "start": C("about four fifths"), "label": lbl("SPORTS ≈ 4/5", 1080, 700, 30, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("mostly about who", 0.1), "dur": 1.4, "target": [1080, 690]}],
    "scale": 0.86, "floor": 1040}, sources=["pew"])
kinetic("s26_t3", "m3_transition", [("If it looks like sports betting…", 60, "If it looks like", None, False),
                                    ("…why isn't it regulated like it?", 60, "why is it not regulated", "gold", False)])

# ====================================================================== PART 4: the fight
card("s27_c4", "m4_card", "The Fight", "Exchange or casino?")
stage("s28_past", "m4_past", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Then the climate changed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("docs", x=700, y=560, at=0.3, text="CFTC ORDER · JAN 2022", scale=0.7, stamp="$1.4M", stampAt=C("penalty for running")),
              it("letters", x=1000, y=130, text="'AN ILLEGAL UNREGISTERED … FACILITY' (CFTC)", at=C("penalty for running"), size=42, color="gold"),
              it("sign", x=1450, y=300, text="JULY 2025: POLYMARKET US DESIGNATED", at=C("Then the climate changed"), color="#C8E6C9", size=32)]},
    sources=["cftc"])
stage("s29_states", "m4_states", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The platforms answered"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("letters", x=1000, y=120, text="THE STATES PUSH BACK", at=0.3, size=58, color="gold"),
              it("sign", x=800, y=260, text="STATES: 'ILLEGAL SPORTS BETS'", at=C("Several states told"), color="#FFCDD2", size=34),
              it("sign", x=1450, y=360, text="PLATFORMS: 'FEDERAL EXCHANGES'", at=C("The platforms answered"), color="#BBDEFB", size=34)]},
    sources=["courts"])
stage("s30_split", "m4_split", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("One judge disagreed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("sign", x=1150, y=320, text="3RD CIRCUIT, APRIL 2026: FOR KALSHI (2–1)", at=0.3, color="#C8E6C9", size=34),
              it("letters", x=1150, y=180, text="'SWAPS TRADED ON A CFTC-LICENSED DCM'", at=C("It said the sports contracts"), size=40, color="gold"),
              it("sign", x=1350, y=440, text="DISSENT: 'A PERFORMATIVE SLEIGHT'", at=C("One judge disagreed"), color="#FFCDD2", size=32),
              it("gavel", x=1650, y=F - 20, hits=[C("sided with Kalshi")], at=0.2)]},
    sources=["courts"])
stage("s31_ninth", "m4_ninth", {
    "zones": [Z("court", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}], "drift": 1,
    "items": [it("sign", x=1150, y=320, text="9TH CIRCUIT, AUGUST 2026: AGAINST KALSHI", at=0.3, color="#FFCDD2", size=34),
              it("letters", x=1150, y=180, text="'NOT SWAPS … SPORTS BETS'", at=C("It said the contracts"), size=48, color="gold"),
              it("letters", x=1150, y=450, text="TWO COURTS · TWO ANSWERS", at=C("Two appeals courts"), size=44, color="white"),
              it("gavel", x=1650, y=F - 20, hits=[C("went the other way")], at=0.2)]},
    sources=["courts"])
stage("s32_supreme", "m4_supreme", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Meanwhile, the federal regulator"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 1,
    "items": [it("docs", x=700, y=560, at=0.3, text="NO. 26-299 · NEW JERSEY", scale=0.7, stamp="PENDING", stampAt=C("they have not decided")),
              it("letters", x=1150, y=150, text="SUPREME COURT: NOT YET DECIDED WHETHER TO HEAR IT", at=C("New Jersey has asked"), size=38, color="gold"),
              it("sign", x=1350, y=320, text="CFTC: BAN PLAN DROPPED · SUED STATES", at=C("Meanwhile, the federal regulator"), color="#BBDEFB", size=32)]},
    sources=["courts", "cftc"])
add("p33_tug", "m4_draw", "engine_draw", {
    "title": "The tug of war (cases pending)", "board": BOARD, "draw_start": C("On one side, the platforms"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 520, 240, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("On one side, the platforms"), "label": lbl("PLATFORMS + CFTC", 680, 573, 20, "accent2")},
        {"d": rect(1200, 520, 240, 90), "color": "risk", "width": 5, "kind": "box", "start": C("On the\n    other side") if False else C("the states and their"), "label": lbl("STATES", 1320, 573, 22, "risk")},
        {"d": "M 800 565 L 1200 565", "color": "ink", "width": 8, "kind": "stroke", "start": C("In the middle, the rope"), "label": lbl("YES/NO ON TONIGHT'S GAME", 1000, 530, 18, "ink")},
        {"d": "M 1000 600 L 1000 700", "color": "accent", "width": 4, "kind": "stroke", "start": C("the referee"), "label": lbl("COURTS: NO WHISTLE YET", 1000, 730, 20, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("blown the whistle", 0.1), "dur": 1.4, "target": [1000, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["courts"])
kinetic("s34_t4", "m4_transition", [("Whatever the courts decide…", 62, "Whatever the courts decide", None, False),
                                    ("…one part is already clear", 62, "already clear", "gold", False)])

# ====================================================================== PART 5: the house always gets paid
card("s35_c5", "m5_card", "The House Always Gets Paid", "The toll, in numbers")
stage("s36_math", "m5_math", {
    "zones": [Z("studio")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}], "drift": 0,
    "items": [it("letters", x=960, y=140, text="ONE TRADE (EXAMPLE)", at=0.3, size=56, color="gold"),
              it("sign", x=500, y=320, text="100 CONTRACTS × 50¢ = $50", at=C("You buy one hundred"), color="#BBDEFB", size=34),
              it("sign", x=1420, y=320, text="FEE ≈ $1.75", at=C("the fee is about"), color="#FFCDD2", size=40),
              it("sign", x=500, y=460, text="WIN: $100", at=C("If you win"), color="#C8E6C9", size=36),
              it("sign", x=1420, y=460, text="LOSE: $0", at=C("If you lose"), color="#FFCDD2", size=36),
              it("letters", x=960, y=640, text="THE TOLL WAS PAID AT THE START", at=C("Either way"), size=46, color="gold")]},
    sources=["kalshi"])
stage("s37_tiny", "m5_tiny", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Small for Wall"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.6}], "drift": 2,
    "items": [it("counter", x=1000, y=260, at=C("But it is"), prefix="≈ ", suffix="%", decimals=2, steps=[[0, 0], [{"cue": "the commission oversees"}, 0.08]], text="OF ALL CFTC-REGULATED FUTURES TRADING (CFTC)", scale=1.3),
              it("letters", x=1000, y=130, text="$25BN IN A MONTH…", at=0.3, size=54, color="gold"),
              it("sign", x=1300, y=470, text="SMALL FOR WALL STREET · HUGE FOR A NEW PRODUCT", at=C("Small for Wall"), color="#FFE0B2", size=30)]},
    sources=["cftc"])
add("p38_model", "m5_draw", "engine_draw", {
    "title": "The business model", "board": BOARD, "draw_start": C("On one side, thousands of traders"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(700, 500, 220, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("On one side, thousands of traders"), "label": lbl("TRADERS", 810, 553, 24, "accent2")},
        {"d": rect(1010, 500, 220, 90), "color": "accent", "width": 6, "kind": "box", "start": C("In the middle, the exchange"), "label": lbl("TOLL BOOTH", 1120, 553, 24, "accent")},
        {"d": rect(1320, 500, 220, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("On the other side, the market makers"), "label": lbl("MARKET MAKERS", 1430, 553, 20, "accent3")},
        {"d": arrow((925, 545), (1005, 545)) + " " + arrow((1315, 545), (1235, 545)), "color": "ink", "width": 4, "kind": "arrow", "start": C("taking\n    a small toll") if False else C("a small toll on every match")},
        {"d": "M 810 600 Q 1120 760 1430 600", "color": "muted", "width": 4, "kind": "stroke", "start": C("win and lose against each"), "label": lbl("WIN / LOSE BETWEEN THEMSELVES", 1120, 720, 18, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("The toll booth is the only", 0.1), "dur": 1.4, "target": [1120, 545]}],
    "scale": 0.86, "floor": 1040}, sources=["kalshi"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("stadium", night=True, label="FINAL")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.1}, {"at": C("Whether that makes them"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="NOT BETTING AGAINST YOU · CHARGING YOU TO TRADE", at=0.3, size=44, color="gold"),
              it("sign", x=800, y=270, text="FINANCE OR CASINO? COURTS STILL FIGHTING", at=C("Whether that makes them"), color="#FFE0B2", size=30),
              it("sign", x=1450, y=270, text="THE TOLL GETS PAID EITHER WAY", at=C("But the toll booth"), color="#FFCDD2", size=30)]},
    sources=["kalshi", "courts"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_predmkt_storyboard.py; edit the generator, not this file.\n"
           "# Episode 45 storyboard (prediction markets): one visual language per part; tones from visual_direction.yaml.\n")
