"""Generates projects/before-you-buy-tesla-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Tesla, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit from
tools/byb_kit.py. Tesla's own world: VOLT VALLEY (new `voltvalley` set: a long car-factory roof, a highway of generic
driverless pods with sensor domes, battery cabinets whose charge bars fill, solar canopies, a generic boxy helper robot),
plus the car plant, the power grid, the money machine, the vault, the court and the exchange. One visual language per part:
- Hook: volt valley with a giant counter + edition stamp; credits sold between carmakers (bank hall); exchange; disclaimer.
- Part 1 (the machine): money machine (cars / services / energy / credits); bank hall (credits); volt valley batteries; board.
- Part 2 (the cash): vault, data center (SI capex), bank hall (share count), vault (cash pile), bar board.
- Part 3 (what's priced in): calculator (three lenses), calculator (breaks), volt valley (steady-state gap), volt valley
  (robots + pods: the bet), board.
- Part 4 (what has to happen): pods on the highway, battery charge, helper robot, car plant.
- Part 5 (risks and upside): empty chair (one person), highway at night (demand/policy), court, risk scale.
- Payoff: scorecard with the edition stamp.
Rules: no logos, generic shapes only (no real vehicle/robot designs), no real people drawn (Musk named in text only);
numbers match sources.yaml; our calculations labelled; company plans attributed; pay milestones are pay terms.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_tesla_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-tesla-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q3 2026 (SEP 30, 2026)")
SEGS = [("CAR SALES $72.3BN", 72.3, "#FF4F6B", None), ("SERVICES $16.3BN", 16.3, "#3DF5FF", None), ("ENERGY $12.3BN", 12.3, "#7DFF8A", None), ("CREDITS $1.2BN", 1.2, "#FFE14D", None)]
JOKES = ["THIN MARGINS · FAST CARS", "CREDITS DEPT · CLOSING SOON", "ROBOTS IN TRAINING", "PLEASE DO NOT AUTOPARK HERE"]
VV = ["NO DRIVER · NO PROBLEM?", "CHARGE IT TO THE FUTURE", "ROBOTS CROSSING", "BATTERIES INCLUDED · MOSTLY"]
RED = "#FF4F6B"

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("voltvalley", signs=VV, podsAt=0.5, chargeAt=1.0)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=650, y=200, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "Tesla is worth"}, 1.50]], text="TESLA MARKET VALUE (OUR CALC.)", scale=1.2),
              it("sign", x=650, y=380, text="$379.78 × 3.95BN SHARES", at=C("a share at the close"), color="#BBDEFB", size=30),
              it("letters", x=1100, y=530, text="≈ 466× ITS 12-MONTH PROFIT", at=C("By our math"), size=52, color="gold"),
              stamp(1450, 340, at=C("a share at the close"), scale=0.7),
              buddy(300, 860, at=0.5, mood="happy", moods=[[C("By our math"), "shock"]], label="TSLA", color=RED, hop=30)]},
    sources=["px", "deck"])
stage("s02_twist", "h_twist", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("Not from building cars"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=200, at=0.2, prefix="≈ ", suffix="%", decimals=0, steps=[[0.2, 0], [{"cue": "of Tesla's operating profit"}, 34]], text="OF OPERATING PROFIT FROM REGULATORY CREDITS (OUR CALC.)"),
              it("sign", x=1350, y=360, text="SOLD TO OTHER CARMAKERS", at=C("sold to other carmakers"), color="#FFE0B2", size=30),
              it("letters", x=1100, y=520, text="NOT FROM BUILDING CARS", at=C("Not from building cars"), size=54, color="gold"),
              it("pricetag", x=1650, y=720, at=C("sold to other carmakers"), text="CREDITS", pages=[[C("Not from building cars"), "CREDITS · PURE PROFIT", False]]),
              buddy(450, 860, at=0.4, mood="shock", label="CREDITS", color="#FFE14D", hop=14)]},
    sources=["deck"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=200, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=360, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=360, text="WHAT COULD BREAK IT?", at=C("what could"), color="#FFCDD2", size=34),
              buddy(1000, 860, at=0.4, mood="worry", label="TSLA", color=RED, hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: TESLA", at=0.4, size=60, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="TESLA'S", sources=["tenq"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Cars, credits and batteries")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("Car sales were")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("Over the last twelve months")),
                       (SEGS[2][0], SEGS[2][1], SEGS[2][2], C("Over the last twelve months")), (SEGS[3][0], SEGS[3][1], SEGS[3][2], C("Over the last twelve months"))],
                      "THE TESLA MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("Over the last twelve months"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Tesla brought in"}, 94.8]], text="FY2025 REVENUE (10-K)", scale=1.0),
              it("sign", x=650, y=860, text="CAR SALES $78.5BN (2023) → $65.8BN (2025)", at=C("Car sales were"), color="#FFCDD2", size=26),
              it("sign", x=600, y=960, text="MODEL 3 + Y ≈ 98% OF Q3 DELIVERIES", at=C("two models"), color="#BBDEFB", size=26)]},
    sources=["tenq", "deck"])
stage("s08_credits", "m1_credits", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But that's shrinking"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=750, y=200, at=0.2, prefix="$", suffix="BN", decimals=2, steps=[[0.2, 0], [{"cue": "they brought in"}, 1.18]], text="REGULATORY CREDITS, 12 MONTHS"),
              it("sign", x=750, y=370, text="ALMOST PURE PROFIT", at=C("almost pure"), color="#C8E6C9", size=30),
              it("sign", x=1400, y=300, text="Q3: $475M OF CREDIT REVENUE REVERSED", at=C("Last quarter Tesla reversed"), color="#FFCDD2", size=28),
              it("sign", x=1400, y=440, text="SOME CREDIT PROGRAMS 'RESTRICTED'", at=C("government actions"), color="#FFE0B2", size=28),
              coins(500, 700, [1500, 760], at=0.4, rate=4, until=C("But that's shrinking")),
              buddy(1850, 860, at=0.4, mood="happy", moods=[[C("But that's shrinking"), "worry"]], label="CREDITS", color="#FFE14D", hop=16)]},
    sources=["deck", "tenq"])
stage("s09_energy", "m1_energy", {
    "zones": [Z("voltvalley", signs=VV, chargeAt=0.3, podsAt=99)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": C("That's a better margin"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1100, y=200, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "brought in"}, 12.8]], text="ENERGY, FY2025 (WAS $6.0BN IN 2023)"),
              it("sign", x=1100, y=370, text="GROSS MARGIN ≈ 30%", at=C("at a gross margin"), color="#C8E6C9", size=30),
              it("letters", x=1700, y=520, text="BETTER THAN THE CARS", at=C("That's a better margin"), size=50, color="gold"),
              buddy(2200, 860, at=0.4, mood="cool", label="ENERGY", color="#7DFF8A", hop=20)]},
    sources=["tenq"])
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Software is creeping"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="WHERE THE CUSTOMERS ARE", at=0.2, size=56, color="gold"),
              it("sign", x=720, y=250, text="U.S. 46%", at=C("the United States brought"), color="#BBDEFB", size=32),
              it("sign", x=1000, y=250, text="CHINA 20%", at=C("China"), color="#FFE0B2", size=32),
              it("sign", x=1300, y=250, text="REST 34%", at=C("everywhere else"), color="#C8E6C9", size=32),
              it("sign", x=760, y=380, text="Q3: U.S. −14%", at=C("U S revenue fell"), color="#FFCDD2", size=30),
              it("sign", x=1260, y=380, text="Q3: OTHER INTL +32%", at=C("other international markets"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=510, text="FSD SUBSCRIPTIONS 1.04M → 1.74M", at=C("Active Full Self Driving"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=620, text="SERVICES ≈ $16.3BN / YEAR", at=C("And services"), color="#F5F5F5", size=28),
              buddy(1700, 860, at=0.3, mood="happy", label="TSLA", color="#E53935", hop=14)]},
    sources=["tenq", "deck"])
board("p10_machine", "m1_draw", "The machine (FY2025 / TTM)", C("Here are the cars"), [
    {"d": rect(1080, 420, 360, 200), "color": "risk", "width": 6, "kind": "box", "start": C("Here are the cars"), "label": lbl("CARS · THIN MARGIN", 1260, 528, 20, "risk")},
    {"d": rect(1080, 700, 360, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is energy"), "label": lbl("ENERGY · ≈ 30% GM", 1260, 768, 20, "accent3")},
    {"d": rect(640, 700, 260, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Here are the credits"), "label": lbl("CREDITS ↓", 770, 768, 20, "accent")},
    {"d": rect(640, 420, 260, 140), "color": "accent2", "width": 6, "kind": "box", "start": C("this arrow"), "label": lbl("FUTURE: NO $ YET", 770, 498, 18, "accent2")},
    {"d": arrow((905, 490), (1075, 510)), "color": "accent2", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("THE BET", 990, 470, 18, "accent2")},
], C("don't have revenue numbers yet", 0.1), [770, 490], sources=["tenq", "deck"])
kinetic("s11_t1", "m1_transition", [("So how much cash", 76, "So how much cash", None, False),
                                    ("does it throw off?", 76, "actually throw off", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Twelve months of cash")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Operating profit was"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=160, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "operating cash flow was"}, 18.7]], text="OPERATING CASH FLOW, 12 MONTHS"),
              it("sign", x=1400, y=300, text="CAPEX −$15.4BN", at=C("Capex took"), color="#FFCDD2", size=32),
              it("letters", x=1100, y=440, text="FREE CASH ≈ $3.3BN", at=C("cash flow was"), size=52, color="gold"),
              it("sign", x=1100, y=580, text="OPERATING MARGIN ≈ 3% ON $103.6BN", at=C("Operating profit was"), color="#FFE0B2", size=28),
              coins(400, 700, [1600, 760], at=0.4, rate=5, until=C("Capex took")),
              coins(1600, 700, [2200, 900], at=C("Capex took"), rate=5)]},
    sources=["deck"])
stage("s14_capex", "m2_capex", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("It signed"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="THE SPENDING IS GOING UP", at=0.2, until=C("Tesla expects capex"), size=54, color="gold"),
              it("letters", x=1000, y=130, text="2026 CAPEX: 'IN EXCESS OF $20 BILLION'", at=C("Tesla expects capex"), size=46, color="gold"),
              it("sign", x=700, y=280, text="FOR 'SI': COMPUTE + DATA CENTERS", at=C("super intelligence"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=380, text="'ADDITIONAL FUNDING BEYOND OUR OPERATING CASH FLOW'", at=C("It warns"), color="#FFCDD2", size=24),
              it("sign", x=1000, y=500, text="$30BN NEW CREDIT LINES · NOT DRAWN IN 2026", at=C("It signed"), color="#FFE0B2", size=28),
              it("isodc", x=1450, y=800, at=C("super intelligence"), n=6, step=0.25, cols=3, scale=0.55, glow=True)]},
    sources=["tenq"])
stage("s15_shares", "m2_shares", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Count only diluted shares"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("calendar", x=650, y=300, at=0.2, pages=[[0, "JAN 2025", "3.22BN SHARES"], [C("rose"), "OCT 2026", "3.95BN SHARES"]]),
              it("letters", x=1300, y=220, text="+ ≈ 23% · MOSTLY CEO PAY AWARDS", at=C("almost all from"), size=40, color="gold"),
              it("sign", x=1300, y=380, text="MANY NOT YET EARNED", at=C("not yet earned"), color="#FFE0B2", size=30),
              it("sign", x=1300, y=500, text="ON DILUTED SHARES: ≈ $1.35TN", at=C("Count only diluted shares"), color="#BBDEFB", size=30),
              buddy(1850, 860, at=0.4, mood="shock", label="SHARES", color="#FF9F1C", hop=14)]},
    sources=["tenq", "px"])
stage("s16_returns", "m2_returns", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It pays no dividend"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=180, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Tesla holds"}, 45.4]], text="CASH + SHORT-TERM INVESTMENTS (SEP 30)"),
              it("sign", x=1400, y=320, text="DEBT ≈ $9.5BN", at=C("against about"), color="#C8E6C9", size=32),
              it("sign", x=1250, y=470, text="NO DIVIDEND · NO BUYBACKS", at=C("It pays no dividend"), color="#FFE0B2", size=30),
              coins(500, 760, [1300, 860], at=0.3, rate=6)]},
    sources=["tenq"])
stage("s16b_stake", "m2_stake", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("These marks"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A PIECE OF THE MUSK UNIVERSE", at=0.2, size=54, color="gold"),
              it("sign", x=640, y=250, text="SPACEX STAKE: $2.0BN → $2.865BN", at=C("put"), color="#BBDEFB", size=28),
              it("sign", x=1420, y=250, text="LOCK-UP ENDS DECEMBER", at=C("the lock up"), color="#F5F5F5", size=28),
              it("sign", x=1000, y=370, text="SPACEX BOUGHT $626M OF MEGAPACKS", at=C("SpaceX bought"), color="#FFE0B2", size=28),
              it("sign", x=760, y=490, text="Q3: SPACEX −$142M", at=C("a loss of"), color="#FFCDD2", size=28),
              it("sign", x=1260, y=490, text="Q3: BITCOIN +$288M", at=C("on bitcoin"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=610, text="9M CAPEX $6.1BN → $13.0BN", at=C("capex in the first nine months"), color="#FFE0B2", size=28),
              buddy(1700, 860, at=0.3, mood="worry", label="TSLA", color="#E53935", hop=12)]},
    sources=["tenq"])
board("p17_cash", "m2_draw", "Twelve months of cash ($BN, our calc.)", C("Here is operating cash"), [
    {"d": "M 700 780 L 1460 780", "color": "ink", "width": 4, "start": C("Here is operating cash"), "label": lbl("$BN · TTM", 1080, 830, 18, "ink")},
    bar(760, 170, 780, 360, "accent2", C("Here is operating cash"), "OCF 18.7"),
    bar(990, 170, 780, 434, "risk", C("Here is capex"), "CAPEX 15.4"),
    bar(1220, 170, 780, 706, "accent3", C("And here is what's left"), "FCF 3.3"),
], C("A thin sliver", 0.1), [1305, 680], sources=["deck"])
kinetic("s18_t2", "m2_transition", [("At one and a half trillion…", 70, "At one and a half trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s19_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s20_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("For a car company"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (TTM, OUR CALC.)", note="FAR OUTSIDE A CAR COMPANY'S RANGE",
                    base="TO BE CHOSEN: PROFIT IS TINY",
                    lenses=[("P/E (NET INCOME)", "466×", C("Price to earnings")), ("FCF YIELD", "0.2%", C("Free cash flow")), ("PRICE / SALES", "14.5×", C("Price to sales"))]),
              stamp(400, 960, at=0.4, scale=0.6)]},
    sources=["deck", "px"])
stage("s21_breaks", "m3_breaks", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("At a yield this small"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 44.7, C("with an eight percent"), "≈ 45% / YR"), ("AT 10%", 51.8, C("at ten"), "≈ 52% / YR"),
                    ["MARKET CAP $1.50TN (NOV 10)", "TTM FCF $3.3BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85, max_=60,
                    title="IMPLIED FCF GROWTH, 10 YEARS", base="TODAY'S FCF · METHOD BREAKS", note="NOT A USEFUL NUMBER · OUR ILLUSTRATION", placardX=860, placardY=-200),
              it("sign", x=1500, y=880, text="TINY YIELD → WILD SWINGS", at=C("At a yield this small"), color="#FFCDD2", size=30),
              stamp(1150, 980, at=0.6, scale=0.5),
              buddy(1750, 640, at=0.5, mood="shock", label="MATH", color="#FF9F1C", hop=22, scale=0.8)]},
    sources=["deck", "px"])
stage("s22_steady", "m3_steady", {
    "zones": [Z("voltvalley", signs=["MIND THE GAP", "STEADY STATE · 3% A YEAR", "CHARGE IT TO THE FUTURE", "ROBOTS CROSSING"], podsAt=0, chargeAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That's"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=150, text="THE STEADY-STATE CASH THE PRICE NEEDS", at=0.2, size=50, color="gold"),
              it("sign", x=1000, y=290, text="IF TESLA GREW 3% A YEAR FROM HERE…", at=C("a steady business"), color="#BBDEFB", size=30),
              it("letters", x=1000, y=430, text="FCF NEEDED ≈ $73-102BN A YEAR", at=C("would need free cash flow"), size=48, color="gold"),
              it("sign", x=1000, y=570, text="= 22-31× TODAY · ≈ 70-98% OF ALL REVENUE", at=C("That's"), color="#FFCDD2", size=28)]},
    sources=["deck", "px"])
stage("s23_scenario", "m3_scenario", {
    "zones": [Z("voltvalley", signs=VV, podsAt=0.5, chargeAt=0.5, robotAt=2.0)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Even the C E O's pay package"), "x": 1300, "y": 500, "zoom": 1.05, "dur": 2.2}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="NOT ABOUT CARS AT TODAY'S MARGINS", at=0.2, size=50, color="gold"),
              it("sign", x=1000, y=270, text="ROBOTAXIS · SELF-DRIVING · ENERGY · ROBOTS", at=C("Robotaxis"), color="#BBDEFB", size=28),
              it("sign", x=1300, y=400, text="PAY PACKAGE: FIRST MILESTONE $2.0TN · TODAY ≈ $1.5TN", at=C("Even the C E O's pay package"), color="#FFE0B2", size=24),
              it("sign", x=1300, y=510, text="PAY TERMS, NOT FORECASTS", at=C("Those are pay terms"), color="#FFCDD2", size=30)]},
    sources=["tenq"])
board("p24_two", "m3_draw", "Today vs what the price needs (FCF, $BN, our illustration)", C("Here is free cash flow today"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is free cash flow today"), "label": lbl("$BN A YEAR · OUR CALC.", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 765, "risk", C("Here is free cash flow today"), "TODAY 3.3"),
    bar(1010, 170, 780, 555, "accent3", C("Here is what the price needs"), "NEED @8% 73"),
    bar(1240, 170, 780, 466, "accent2", C("And here it is at"), "NEED @10% 102"),
    {"d": arrow((900, 740), (1005, 580), 0.1), "color": "accent", "width": 5, "kind": "arrow", "start": C("Everything between"), "label": lbl("NEW BUSINESSES", 880, 640, 18, "accent")},
], C("from the new businesses", 0.1), [1320, 520], sources=["deck", "px"])
kinetic("s25_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s26_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s27_robotaxi", "m4_robotaxi", {
    "zones": [Z("voltvalley", signs=["NO DRIVER · NO PROBLEM?", "ROBOTAXI LANE", "UNSUPERVISED MILES ↑", "ROBOTS CROSSING"], podsAt=0.3)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Tesla doesn't report"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="1 · AUTONOMY BECOMES REVENUE", at=0.2, size=52, color="gold"),
              it("sign", x=700, y=270, text="TESLA: ROBOTAXI RIDES IN AUSTIN SINCE SEP 3", at=C("Tesla says it started"), color="#BBDEFB", size=26),
              it("sign", x=1350, y=380, text="FSD SUBSCRIPTIONS 1.04M → 1.74M", at=C("Active self-driving subscriptions"), color="#C8E6C9", size=28),
              it("sign", x=1000, y=500, text="ROBOTAXI REVENUE: NOT REPORTED", at=C("Tesla doesn't report"), color="#FFCDD2", size=30)]},
    sources=["deck"])
stage("s28_energy", "m4_energy", {
    "zones": [Z("powergrid")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": C("and a new Texas factory"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1300, y=130, text="2 · ENERGY KEEPS GROWING", at=0.2, size=56, color="gold"),
              it("sign", x=1100, y=270, text="TESLA: 'HIGHEST-EVER ORDER RATE AND BACKLOG'", at=C("highest ever order rate"), color="#C8E6C9", size=26),
              it("sign", x=1600, y=390, text="TEXAS MEGAFACTORY: 50 GWH PLANNED", at=C("and a new Texas factory"), color="#BBDEFB", size=28)]},
    sources=["deck"])
stage("s29_optimus", "m4_optimus", {
    "zones": [Z("voltvalley", signs=["ROBOTS CROSSING", "HIGH-VOLUME LINE", "NO REVENUE YET", "MIND THE ROBOT"], podsAt=99, robotAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("One of the pay package"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="3 · THE ROBOTS BECOME A PRODUCT", at=0.2, size=50, color="gold"),
              it("sign", x=700, y=270, text="TESLA: PRODUCTION BEGAN IN FREMONT", at=C("Tesla says Optimus"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=380, text="REVENUE FIGURES: NONE", at=C("There are no revenue"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=500, text="PAY MILESTONE: 1 MILLION ROBOTS DELIVERED", at=C("One of the pay package"), color="#FFE0B2", size=28)]},
    sources=["deck", "tenq"])
stage("s30_cars", "m4_cars", {
    "zones": [Z("carplant")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Margins have to hold"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="4 · CARS RECOVER WITHOUT THE CREDITS", at=0.2, size=48, color="gold"),
              it("calendar", x=650, y=320, at=C("Deliveries went from"), pages=[[0, "2024", "≈ 1.79M CARS"], [C("last year"), "2025", "≈ 1.64M CARS"]]),
              it("sign", x=1350, y=280, text="TESLA: BATTERIES LIMIT VOLUMES · BACKLOG BEST IN 4 YEARS", at=C("Tesla says batteries"), color="#BBDEFB", size=24),
              it("letters", x=1300, y=460, text="MARGINS HOLD AS CREDITS FADE", at=C("Margins have to hold"), size=44, color="gold"),
              buddy(1850, 860, at=0.4, mood="worry", label="CARS", color=RED, hop=16)]},
    sources=["deck", "tenq"])
kinetic("s31_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s32_c5", "m5_card", "Risks and Upside", "What Tesla itself warns about")
stage("s33_key", "m5_key", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it says the pay package"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 1 · ONE PERSON", at=0.2, size=58, color="gold"),
              it("emptychair", x=700, y=640, at=0.4, memoAt=C("also runs other companies")),
              it("sign", x=1350, y=270, text="'HIGHLY DEPENDENT ON THE SERVICES OF ELON MUSK'", at=C("highly dependent"), color="#FFE0B2", size=24),
              it("sign", x=1350, y=390, text="PLEDGED SHARES → MAY BE 'FORCED ... TO SELL'", at=C("if he pledged shares"), color="#FFCDD2", size=26),
              it("sign", x=1350, y=510, text="PAY PACKAGE COULD PULL FOCUS", at=C("And it says the pay package"), color="#FFCDD2", size=28)]},
    sources=["tenq"])
stage("s34_demand", "m5_demand", {
    "zones": [Z("voltvalley", night=True, signs=["DEMAND · PLEASE HOLD", "CREDITS REPEALED", "TARIFF ZONE", "COMPETITORS AHEAD"], podsAt=0, chargeAt=0)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Tax credits"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 2 · DEMAND AND POLICY", at=0.2, size=56, color="gold"),
              it("sign", x=700, y=270, text="EV DEMAND + SELF-DRIVING ADOPTION", at=C("Growth depends"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=380, text="'STRONG COMPETITION'", at=C("Competition"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=500, text="TAX CREDITS CUT · TARIFFS HIT ENERGY HARDER", at=C("Tax credits"), color="#FFCDD2", size=28)]},
    sources=["tenq"])
stage("s34b_squeeze", "m5_squeeze", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A securities class action"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A THIN MARGIN", at=0.2, size=60, color="gold"),
              it("sign", x=1000, y=250, text="TTM OPERATING MARGIN 3.3%", at=C("operating margin was"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=370, text="Q3 OPEX $3.43BN → $4.78BN", at=C("Operating expenses"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=490, text="SI + R&D + STOCK PAY (INCL. CEO AWARD)", at=C("super intelligence"), color="#F5F5F5", size=28),
              it("sign", x=1000, y=610, text="SECURITIES CLASS ACTION PENDING", at=C("A securities class action"), color="#FFCDD2", size=28),
              buddy(1700, 860, at=0.4, mood="worry", label="TSLA", color="#E53935", hop=12)]},
    sources=["deck", "tenq"])
stage("s35_legal", "m5_legal", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Regulators are asking"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 3 · COURTS AND REGULATORS", at=0.2, size=52, color="gold"),
              it("sign", x=700, y=270, text="AUTOPILOT CASE: $129M + $200M PUNITIVE (APPEAL)", at=C("In one Autopilot case"), color="#FFE0B2", size=26),
              it("sign", x=1350, y=390, text="REGULATORS: DRIVER ASSISTANCE + ROBOTAXI", at=C("Regulators are asking"), color="#BBDEFB", size=26),
              it("sign", x=1000, y=510, text="NO WRONGDOING FOUND · NO AMOUNTS DISCLOSED", at=C("found wrongdoing"), color="#C8E6C9", size=26),
              it("gavel", x=1800, y=620, hits=[C("a jury awarded"), C("is appealing")])]},
    sources=["tenq"])
stage("s36_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("None of it comes"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("ONE PERSON · PLEDGES · PAY FOCUS", 0.3), ("DEMAND · CREDITS · TARIFFS", 0.9), ("COURTS · REGULATORS", 1.5)],
                    [("SEMI IN VOLUME PRODUCTION", C("the Semi")), ("CYBERCAB CAPACITY > 125,000/YR", C("Cybercab capacity")), ("FSD IN 9 EU COUNTRIES · SPACEX STAKE", C("It also owns"))],
                    title="RISKS VS UPSIDE (TESLA'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="UPSIDE IS UNSIZED: NO REVENUE FIGURES GIVEN", at=C("None of it comes"), color="#C8E6C9", size=28)]},
    sources=["deck", "tenq"])
kinetic("s37_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
board("p38_watch", "payoff", "3 numbers to watch (next report)", C("One, fourth quarter"), [
    {"d": rect(1320, 440, 250, 140), "color": "accent", "width": 6, "kind": "box", "start": C("One, fourth quarter"), "label": lbl("NEXT REPORT", 1445, 518, 22, "accent")},
    {"d": rect(700, 300, 440, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("One, fourth quarter"), "label": lbl("Q4 DELIVERIES", 920, 362, 20, "accent2")},
    {"d": "M 720 428 L 1120 428", "color": "ink", "width": 1, "start": C("One, fourth quarter", 0.3), "label": lbl("VS 418,227 IN Q4 2025", 920, 450, 14, "ink")},
    {"d": arrow((1150, 355), (1310, 462), 0.08), "color": "accent2", "width": 5, "kind": "arrow", "start": C("One, fourth quarter", 0.6)},
    {"d": rect(700, 470, 440, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("Two, capex"), "label": lbl("CAPEX AND FREE CASH", 920, 532, 20, "accent3")},
    {"d": "M 720 598 L 1120 598", "color": "ink", "width": 1, "start": C("Two, capex", 0.3), "label": lbl("CAPEX > $20BN IN 2026 · TTM FCF $3.3BN", 920, 620, 14, "ink")},
    {"d": arrow((1150, 525), (1310, 505), 0.08), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Two, capex", 0.6)},
    {"d": rect(700, 640, 440, 110), "color": "risk", "width": 5, "kind": "box", "start": C("Three, regulatory"), "label": lbl("CREDITS + CAR MARGIN", 920, 702, 20, "risk")},
    {"d": "M 720 768 L 1120 768", "color": "ink", "width": 1, "start": C("Three, regulatory", 0.3), "label": lbl("Q3: $113M · 18.1% EX-CREDITS", 920, 790, 14, "ink")},
    {"d": arrow((1150, 695), (1310, 547), 0.08), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three, regulatory", 0.6)},
], C("Three, regulatory", 0.5), [1445, 510], sources=["deck", "tenq"])
stage("s39_edition", "payoff2", {
    "zones": [machine(SEGS, "THE TESLA MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [scorecard([("Q4 DELIVERIES", "VS 418,227 IN Q4 2025", 0.4),
                         ("CAPEX AND FREE CASH", "CAPEX > $20BN IN 2026 · TTM FCF $3.3BN", 1.0),
                         ("CREDITS + CAR MARGIN", "Q3: $113M · 18.1% EX-CREDITS", 1.6)], x=960, y=230, at=0.2, scale=0.82),
              stamp(1560, 930, at=0.6, scale=0.7),
              it("sign", x=760, y=925, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("three questions"), color="#BBDEFB", size=24)]},
    sources=["deck"])
add("s40_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_tesla_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Tesla (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
