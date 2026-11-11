"""Generates projects/before-you-buy-amazon-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Amazon, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit from
tools/byb_kit.py. Amazon's own world: the BOX PORT (new `boxport` set: a fulfillment hall with snaking conveyors of generic
boxes, robot carts, and a glowing cloud gate where boxes turn into server bricks), plus the data center, the money machine,
the bank hall, the court and the exchange. One visual language per part:
- Hook: box port with a giant counter + edition stamp; cloud gate lighting up (backlog); exchange; the disclaimer.
- Part 1 (the machine): money machine (stores / ads / AWS); box port past the gate (AWS); office (backlog); board.
- Part 2 (the cash): vault, bank hall (debt), cloud port (stakes in AI labs), site (capex outlook), bar board.
- Part 3 (what's priced in): calculator (three lenses), data center (proxy), calculator (gauge), box port (steady-state gap), board.
- Part 4 (what has to happen): office (backlog), data center (margins), box port (stores), site (capex peak).
- Part 5 (risks and upside): box port jammed, cloud port (the loop), court, risk scale.
- Payoff: scorecard with the edition stamp.
Rules: no logos (no smile arrow), generic shapes only, no real people drawn; numbers match sources.yaml; our calcs labelled.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_amazon_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-amazon-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q3 2026 (SEP 30, 2026)")
SEGS = [("NORTH AMERICA $460.3BN", 460.3, "#FF9F1C", None), ("INTERNATIONAL $175.8BN", 175.8, "#FFE14D", None), ("AWS $161.4BN", 161.4, "#3DF5FF", None)]
JOKES = ["THIN MARGINS · THICK BOXES", "AWS · THE PROFIT FLOOR", "CAPEX ZONE · HARD HATS", "NEXT-DAY OR BUST"]
PORT = ["SMILE · YOU ARE A PARCEL", "NEXT-DAY OR BUST", "CLOUD GATE · NO BOXES BEYOND", "ROBOTS HAVE RIGHT OF WAY"]
ORANGE = "#FF9F1C"

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("boxport", signs=PORT, gateAt=99, gateWX=2300)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=650, y=300, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "Amazon is worth"}, 2.93]], text="AMAZON MARKET VALUE (OUR CALC.)", scale=1.2),
              it("sign", x=650, y=480, text="$270.87 × 10.81BN SHARES", at=C("a share at the close"), color="#BBDEFB", size=30),
              it("letters", x=1100, y=640, text="FREE CASH, 12 MONTHS: −$42.4BN", at=C("its free cash flow was"), size=50, color="gold"),
              stamp(1450, 420, at=C("a share at the close"), scale=0.7),
              buddy(320, 880, at=0.5, mood="happy", moods=[[C("Negative"), "shock"]], label="AMZN", color=ORANGE, hop=30)]},
    sources=["px", "rel"])
stage("s02_twist", "h_twist", {
    "zones": [Z("boxport", signs=PORT, gateAt=4.0, gateWX=1180)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And the bet behind it"), "x": 1300, "y": 520, "zoom": 0.92, "dur": 2.4}], "drift": 2,
    "items": [it("counter", x=750, y=260, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "into capex"}, 210.7]], text="CAPEX, LAST 12 MONTHS (NET)"),
              it("sign", x=750, y=430, text="MOSTLY AWS DATA CENTERS", at=C("mostly data centers"), color="#FFE0B2", size=30),
              it("counter", x=1750, y=260, at=C("A W S says"), prefix="≈ $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "customers have committed"}, 578]], text="AWS BACKLOG (10-Q)"),
              it("sign", x=1750, y=430, text="WAS ≈ $244BN IN JANUARY", at=C("up from"), color="#C8E6C9", size=30),
              buddy(400, 880, at=0.4, mood="worry", moods=[[C("And the bet behind it"), "happy"]], label="FCF", color="#7DFF8A", hop=14)]},
    sources=["rel", "tenq"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=200, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=360, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=360, text="WHAT COULD BREAK IT?", at=C("what could"), color="#FFCDD2", size=34),
              buddy(1000, 880, at=0.4, mood="worry", label="AMZN", color=ORANGE, hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: AMAZON", at=0.4, size=60, color="gold")]})
stage("s05_disc", "h_disclaimer", {
    "zones": [Z("chipcity", signs=["NOT FINANCIAL ADVICE", "FILINGS ONLY", "OUR MATH · LABELLED", "DATED EDITION"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": 1.0, "x": 1100, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=170, text="NOT FINANCIAL ADVICE", at=0.2, size=64, color="gold"),
              it("sign", x=1000, y=320, text="AMAZON'S FILINGS + OUR MATH, DATED", at=C("Everything here"), color="#BBDEFB", size=32),
              stamp(1000, 460, at=C("Everything here"), scale=1.0),
              it("sign", x=1000, y=640, text="DISCLOSURE: DRAFTED WITH AN AI MADE BY ANTHROPIC (AN AMAZON INVESTEE)", at=C("one disclosure"), color="#FFE0B2", size=24),
              buddy(500, 880, at=0.3, mood="cool", hop=16), buddy(1500, 880, at=0.5, mood="happy", color=ORANGE, hop=22)]},
    sources=["tenq"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Stores, ads and the cloud")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("The stores in North America")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("International")),
                       (SEGS[2][0], SEGS[2][1], SEGS[2][2], C("But the profit engine"))], "THE AMAZON MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("But the profit engine"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Amazon sold"}, 797.5]], text="NET SALES, LAST 12 MONTHS", scale=1.0),
              it("sign", x=650, y=860, text="STORES: ≈ 8% (NA) · ≈ 3% (INTL) MARGIN", at=C("an operating margin"), color="#FFE0B2", size=28),
              it("sign", x=600, y=960, text="ADS ≈ $78BN", at=C("Advertising brought in"), color="#C8E6C9", size=30)]},
    sources=["rel"])
stage("s08_aws", "m1_aws", {
    "zones": [Z("boxport", signs=["AWS · THE PROFIT FLOOR", "CLOUD GATE · NO BOXES BEYOND", "FASTEST IN 5 YEARS", "ROBOTS HAVE RIGHT OF WAY"], gateAt=0.3, gateLabel="AWS", gateWX=500)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 1.0}, {"at": C("And in the September quarter"), "x": 1350, "y": 520, "zoom": 0.95, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1300, y=230, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "It made"}, 161.4]], text="AWS SALES, 12 MONTHS"),
              it("sign", x=1300, y=400, text="20% OF SALES → 58% OF OPERATING INCOME", at=C("of all operating income"), color="#BBDEFB", size=28),
              it("sign", x=1500, y=520, text="MARGIN ≈ 38% · Q3 GROWTH +39%", at=C("And in the September quarter"), color="#C8E6C9", size=28),
              buddy(2050, 880, at=0.4, mood="happy", label="AWS", color="#3DF5FF", hop=28)]},
    sources=["rel"])
stage("s09_backlog", "m1_backlog", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Two expansions"), "x": 1200, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=750, y=200, at=0.2, prefix="≈ $", suffix="BN", decimals=0, steps=[[0.2, 0], [{"cue": "of commitments"}, 578]], text="AWS BACKLOG · AVG. LIFE ≈ 6 YEARS"),
              it("sign", x=1400, y=330, text="OPENAI: +$100BN OVER 8 YEARS", at=C("OpenAI added"), color="#BBDEFB", size=28),
              it("sign", x=1400, y=450, text="ANTHROPIC: +$100BN+ OVER 10 YEARS", at=C("and Anthropic added"), color="#BBDEFB", size=28),
              it("letters", x=1100, y=600, text="SHARE OF THE TOTAL: NOT DISCLOSED", at=C("doesn't say what share"), size=44, color="gold"),
              buddy(400, 880, at=0.4, mood="shock", moods=[[C("doesn't say what share"), "worry"]], label="BACKLOG", color="#7DFF8A", hop=20)]},
    sources=["tenq"])
stage("s09b_streams", "m1_streams", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And the cloud is speeding up"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE QUIETER STREAMS", at=0.2, size=58, color="gold"),
              it("sign", x=720, y=250, text="SELLER SERVICES $187.7BN", at=C("Fees from outside sellers"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=330, text="ADS $78.0BN", at=C("over the year"), color="#FFE0B2", size=28),
              it("sign", x=1300, y=250, text="SUBSCRIPTIONS $54.3BN", at=C("Prime and other"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=470, text="AWS GROWTH: 24% → 28% → 37% → 39%", at=C("A W S growth went"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=590, text="PRIME DAY SHIFT: ≈ −4 PTS IN Q3", at=C("Prime Day moved"), color="#F5F5F5", size=28),
              buddy(1700, 860, at=0.3, mood="happy", label="AWS", color="#FF9F1C", hop=14)]},
    sources=["rel"])
board("p10_machine", "m1_draw", "The machine (TTM to Q3 2026)", C("Here are the stores"), [
    {"d": rect(1080, 420, 360, 200), "color": "accent", "width": 6, "kind": "box", "start": C("Here are the stores"), "label": lbl("STORES · THIN MARGIN", 1260, 528, 20, "accent")},
    {"d": rect(1080, 700, 360, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is A W S"), "label": lbl("AWS · 58% OF PROFIT", 1260, 768, 20, "accent2")},
    {"d": rect(640, 700, 260, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is the backlog"), "label": lbl("BACKLOG $578BN", 770, 768, 20, "accent3")},
    {"d": arrow((905, 760), (1075, 760)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("flowing into A W S"), "label": lbl("REVENUE", 990, 740, 18, "accent3")},
    {"d": arrow((770, 450), (770, 690), 0.15), "color": "risk", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("CAPEX $211BN", 770, 430, 20, "risk")},
], C("to serve that backlog", 0.1), [770, 600], sources=["rel", "tenq"])
kinetic("s11_t1", "m1_transition", [("That profitable…", 76, "A machine that profitable", None, False),
                                    ("…why is free cash below zero?", 70, "why is free cash flow below zero", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Where twelve months of cash went")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So free cash flow"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=160, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Operating cash flow"}, 168.3]], text="OPERATING CASH FLOW, 12 MONTHS"),
              it("sign", x=1400, y=300, text="NET INCOME $134.8BN · ≈ $70BN PAPER GAINS", at=C("Net income was"), color="#FFE0B2", size=26),
              it("sign", x=1400, y=420, text="CAPEX −$210.7BN", at=C("Capex took"), color="#FFCDD2", size=32),
              it("letters", x=1100, y=560, text="FREE CASH: −$42.4BN", at=C("So free cash flow"), size=54, color="gold"),
              coins(400, 700, [1600, 760], at=0.4, rate=6, until=C("Capex took")),
              coins(1600, 700, [2200, 900], at=C("Capex took"), rate=8)]},
    sources=["rel"])
stage("s14_debt", "m2_debt", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And there are no buybacks"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("calendar", x=650, y=300, at=0.2, pages=[[0, "DEC 2025", "DEBT $68.8BN"], [C("in just nine months"), "SEP 2026", "DEBT $180.9BN"]]),
              it("letters", x=1300, y=220, text="+ ≈ $112BN OF DEBT IN NINE MONTHS", at=C("in just nine months"), size=42, color="gold"),
              it("sign", x=1350, y=380, text="BUYBACKS: $0 · DIVIDEND: NONE", at=C("And there are no buybacks"), color="#FFCDD2", size=30),
              it("sign", x=1350, y=500, text="SHARE COUNT +1.2% (STOCK PAY)", at=C("The share count"), color="#FFE0B2", size=28),
              buddy(1850, 880, at=0.4, mood="worry", label="AMZN", color=ORANGE, hop=14)]},
    sources=["tenq"])
stage("s15_stakes", "m2_stakes", {
    "zones": [Z("cloudport", signs=["INVESTOR + SUPPLIER", "AI LABS · DOCK 1", "CAPACITY · PLEASE WAIT", "MARKED TO MODEL"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Those labs are also"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("sign", x=700, y=200, text="OPENAI PREFERRED: $50BN", at=C("into OpenAI"), color="#BBDEFB", size=30),
              it("sign", x=1300, y=200, text="ANTHROPIC: $10BN", at=C("into Anthropic"), color="#BBDEFB", size=30),
              it("counter", x=1000, y=340, at=C("In total"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "are carried at"}, 298.8]], text="STAKES + CONVERTIBLES, CARRIED VALUE (10-Q)"),
              it("letters", x=1000, y=540, text="INVESTOR AND SUPPLIER AT THE SAME TIME", at=C("Investor and supplier"), size=42, color="gold"),
              buddy(1850, 880, at=0.4, mood="shock", label="LOOP", color="#FF4FD8", hop=20)]},
    sources=["tenq"])
stage("s15b_bsheet", "m2_bsheet", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("On top of that"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BALANCE SHEET FLIPPED", at=0.2, size=56, color="gold"),
              it("sign", x=760, y=250, text="CASH + SECURITIES $114.2BN", at=C("Amazon held"), color="#C8E6C9", size=30),
              it("sign", x=1260, y=250, text="LONG-TERM DEBT $180.9BN", at=C("It owed"), color="#FFCDD2", size=30),
              it("sign", x=1260, y=360, text="INCL. $17.5BN TERM LOAN (SEPT)", at=C("term loan"), color="#FFCDD2", size=26),
              it("sign", x=1000, y=480, text="LEASE LIABILITIES $98.8BN", at=C("lease liabilities"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=590, text="+$164.9BN OF LEASES NOT YET STARTED", at=C("signed but haven't"), color="#FFE0B2", size=28),
              buddy(1700, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenq"])
stage("s16_outlook", "m2_returns", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("and it says"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="THE SPENDING ISN'T DONE", at=0.2, size=60, color="gold"),
              it("sign", x=700, y=300, text="2026 CASH CAPEX: 'APPROXIMATELY $220 BILLION'", at=C("It expects cash capex"), color="#FFE0B2", size=26),
              it("sign", x=1350, y=420, text="2027: 'MEANINGFULLY INCREASE'", at=C("and it says"), color="#FFCDD2", size=30),
              it("isodc", x=1500, y=800, at=C("and it says"), n=9, step=0.18, cols=3, scale=0.6, glow=True)]},
    sources=["rel", "tenq"])
board("p17_cash", "m2_draw", "Where twelve months of cash went ($BN, our calc.)", C("Here is the operating cash bar"), [
    {"d": "M 700 640 L 1560 640", "color": "ink", "width": 4, "start": C("Here is the operating cash bar"), "label": lbl("ZERO LINE", 1130, 690, 18, "ink")},
    bar(740, 150, 640, 360, "accent2", C("Here is the operating cash bar"), "OCF 168"),
    bar(940, 150, 640, 290, "risk", C("Here is the capex bar"), "CAPEX 211"),
    {"d": "M 1140 640 L 1140 710 L 1290 710 L 1290 640 Z", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.4, "kind": "bar", "start": C("Here is what's left"), "label": lbl("FCF −42", 1215, 750, 20, "risk")},
    bar(1340, 150, 640, 460, "accent", C("And here is the new debt"), "NEW DEBT 112"),
], C("filled the hole", 0.1), [1415, 520], sources=["rel", "tenq"])
kinetic("s18_t2", "m2_transition", [("At three trillion dollars…", 70, "At three trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s19_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s20_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Operating cash flow yield"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (TTM, OUR CALC.)", note="P/E ≈ 37× WITHOUT THE PAPER GAINS",
                    base="TO BE CHOSEN: FCF IS NEGATIVE",
                    lenses=[("P/E (NET INCOME)", "21.7×", C("Price to earnings")), ("FCF YIELD", "< 0", C("Free cash flow yield")), ("OCF YIELD", "5.7%", C("Operating cash flow yield"))]),
              stamp(400, 960, at=0.4, scale=0.6)]},
    sources=["rel", "px"])
stage("s21_proxy", "m3_proxy", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It's a proxy"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="A PROXY FOR A BUILDING SPREE", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=340, text="OCF $168.3BN", at=C("We take operating cash"), color="#BBDEFB", size=32),
              it("sign", x=1150, y=340, text="− D&A ≈ $79.4BN", at=C("subtract depreciation"), color="#FFCDD2", size=32),
              it("letters", x=1000, y=500, text="= ≈ $88.9BN · YIELD ≈ 3.0%", at=C("That leaves"), size=50, color="gold"),
              it("sign", x=1300, y=640, text="ASSUMES CAPEX FALLS BACK TOWARD D&A", at=C("It's a proxy"), color="#FFE0B2", size=26),
              buddy(1850, 880, at=0.4, mood="cool", label="PROXY", color="#FFE14D", hop=16)]},
    sources=["tenq", "px"])
stage("s22_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 8.9, C("With an eight percent"), "≈ 8.9% / YR"), ("AT 10%", 13.9, C("With ten percent"), "≈ 13.9% / YR"),
                    ["MARKET CAP $2.93TN (NOV 10)", "PROXY: OCF − D&A $88.9BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED GROWTH, 10 YEARS", base="PROXY (FCF IS NEGATIVE)", placardX=860, placardY=-200),
              it("sign", x=1500, y=880, text="ON TODAY'S FCF: CAN'T BE SOLVED (< 0)", at=C("On actual free cash"), color="#FFCDD2", size=28),
              stamp(1150, 980, at=0.6, scale=0.5),
              buddy(1750, 640, at=0.5, mood="happy", moods=[[C("because it's negative"), "shock"]], label="AMZN", color=ORANGE, hop=22, scale=0.8)]},
    sources=["tenq", "px"])
stage("s23_steady", "m3_steady", {
    "zones": [Z("boxport", signs=["MIND THE GAP", "STEADY STATE · AISLE 3", "CLOUD GATE · NO BOXES BEYOND", "NEXT-DAY OR BUST"], gateAt=0, gateWX=1750)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That gap is the whole bet"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="THE STEADY-STATE CASH THE PRICE NEEDS", at=0.2, size=50, color="gold"),
              it("sign", x=1000, y=300, text="IF AMAZON GREW 3% A YEAR FROM HERE…", at=C("a steady business"), color="#BBDEFB", size=30),
              it("letters", x=1000, y=450, text="FCF NEEDED ≈ $142-199BN A YEAR", at=C("would need free cash flow"), size=48, color="gold"),
              it("sign", x=1000, y=590, text="TODAY: −$42.4BN · OUR ROUGH ILLUSTRATION", at=C("Today it's"), color="#FFCDD2", size=28),
              buddy(1850, 880, at=0.4, mood="worry", moods=[[C("That gap is the whole bet"), "shock"]], label="GAP", color="#FF4F6B", hop=18)]},
    sources=["tenq", "px"])
board("p24_two", "m3_draw", "Today vs what the price needs (FCF, $BN, our illustration)", C("Here is free cash flow today"), [
    {"d": "M 720 700 L 1520 700", "color": "ink", "width": 4, "start": C("Here is free cash flow today"), "label": lbl("ZERO LINE · OUR CALC.", 1120, 840, 18, "ink")},
    {"d": "M 780 700 L 780 760 L 950 760 L 950 700 Z", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.4, "kind": "bar", "start": C("Here is free cash flow today"), "label": lbl("TODAY −42", 865, 800, 20, "risk")},
    bar(1010, 170, 700, 488, "accent3", C("Here is what the price needs"), "NEED @8% 142"),
    bar(1240, 170, 700, 403, "accent2", C("And here it is at the higher rate"), "NEED @10% 199"),
    {"d": arrow((900, 690), (1005, 520), 0.1), "color": "accent", "width": 5, "kind": "arrow", "start": C("The difference"), "label": lbl("THE BET", 900, 560, 18, "accent")},
], C("have to deliver", 0.1), [1320, 460], sources=["tenq", "px"])
kinetic("s25_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s26_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s27_aws", "m4_aws", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That's his projection"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="1 · THE BACKLOG CONVERTS", at=0.2, size=56, color="gold"),
              it("sign", x=700, y=280, text="$578BN OVER ≈ 6 YEARS", at=C("of commitments"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=380, text="CEO: AWS GROWTH 'OVER 40%' IN 2027 AND 2028", at=C("The C E O says"), color="#BBDEFB", size=26),
              it("letters", x=1100, y=530, text="HIS PROJECTION · NOT OURS", at=C("That's his projection"), size=44, color="gold"),
              buddy(1800, 880, at=0.4, mood="happy", label="AWS", color="#3DF5FF", hop=20)]},
    sources=["tenq", "rel"])
stage("s28_margin", "m4_margin", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("every new data center"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="2 · AWS MARGINS HOLD", at=0.2, size=56, color="gold"),
              it("sign", x=700, y=280, text="Q3 AWS MARGIN 38.7%", at=C("The margin was"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=380, text="D&A ALREADY ≈ $79BN A YEAR", at=C("depreciation and amortization is already"), color="#FFCDD2", size=30),
              it("isodc", x=1450, y=800, at=C("every new data center"), n=9, step=0.18, cols=3, scale=0.6, glow=True)]},
    sources=["rel", "tenq"])
stage("s29_retail", "m4_retail", {
    "zones": [Z("boxport", signs=PORT, gateAt=0, gateWX=1750)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("This year"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="3 · THE STORES KEEP IMPROVING", at=0.2, size=54, color="gold"),
              it("sign", x=700, y=310, text="Q4 GUIDE: OP. INCOME $28.5-33.5BN", at=C("guided fourth quarter"), color="#C8E6C9", size=28),
              it("sign", x=1350, y=310, text="SALES $240-247BN", at=C("and sales"), color="#BBDEFB", size=28),
              it("letters", x=1000, y=470, text="BEAT THE TOP OF ITS RANGE 3 TIMES IN 2026", at=C("This year"), size=40, color="gold")]},
    sources=["rel"])
stage("s30_capex", "m4_capex", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The price needs"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="4 · CAPEX PEAKS, FREE CASH TURNS POSITIVE", at=0.2, size=48, color="gold"),
              it("sign", x=700, y=290, text="UNTIL THEN: THE GAP = DEBT", at=C("Until then"), color="#FFCDD2", size=30),
              it("letters", x=1100, y=450, text="YEARS, NOT A DECADE", at=C("not a decade"), size=50, color="gold"),
              buddy(1800, 880, at=0.4, mood="worry", label="FCF", color="#7DFF8A", hop=18)]},
    sources=["tenq"])
kinetic("s31_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s32_c5", "m5_card", "Risks and Upside", "What Amazon itself warns about")
stage("s33_capacity", "m5_capacity", {
    "zones": [Z("boxport", signs=["CAPACITY CHECK", "IMPAIRMENT AHEAD?", "CLOUD GATE · NO BOXES BEYOND", "PLEASE HOLD"], gateAt=0, jamAt=4.0, gateWX=1750)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it has"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=160, text="RISK 1 · THE BUILD-OUT ITSELF", at=0.2, size=54, color="gold"),
              it("sign", x=1000, y=300, text="MISJUDGED DEMAND → EXCESS CAPACITY → IMPAIRMENTS", at=C("misjudging demand"), color="#FFE0B2", size=26),
              it("sign", x=1000, y=420, text="AI 'MAY NOT ... RECOUP OUR INVESTMENTS'", at=C("may not earn enough"), color="#FFCDD2", size=28),
              it("sign", x=1000, y=540, text="COMMITMENTS SIGNED: $883.6BN", at=C("And it has"), color="#FFCDD2", size=30)]},
    sources=["tenq"])
stage("s34_loop", "m5_circular", {
    "zones": [Z("cloudport", signs=["INVESTOR + SUPPLIER", "MARKED TO MODEL", "DOCK 1 · AI LABS", "HANDLE WITH CARE"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("If those labs stumble"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 2 · THE LOOP", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=270, text="SAME LABS: INVESTEES + BIG AWS CUSTOMERS", at=C("Amazon is an investor"), color="#BBDEFB", size=26),
              it("sign", x=1350, y=390, text="'VALUATIONS OF PRIVATE COMPANIES ARE INHERENTLY MORE COMPLEX'", at=C("the filing admits"), color="#FFE0B2", size=22),
              it("letters", x=1000, y=540, text="ONE STUMBLE → BACKLOG AND STAKES HIT", at=C("If those labs stumble"), size=42, color="gold"),
              buddy(1850, 880, at=0.4, mood="worry", label="LOOP", color="#FF4FD8", hop=12)]},
    sources=["tenq"])
stage("s35_legal", "m5_legal", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And last year's Prime"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 3 · REGULATORS", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=270, text="FTC + 22 STATES: SPONSORED AD AUCTIONS (AUG 2026)", at=C("In August"), color="#FFE0B2", size=26),
              it("sign", x=1350, y=390, text="OLDER ANTITRUST CASES SEEK 'BILLIONS'", at=C("Older antitrust cases"), color="#FFCDD2", size=28),
              it("sign", x=1000, y=510, text="PRIME SETTLEMENT (2025): $2.5BN", at=C("And last year's Prime"), color="#BBDEFB", size=28),
              it("gavel", x=1800, y=620, hits=[C("sued over"), C("cost")])]},
    sources=["tenq", "rel"])
stage("s34b_chips", "m5_chips", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A patent case"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 4 · SUPPLY", at=0.2, size=60, color="gold"),
              it("sign", x=760, y=260, text="'A LIMITED GROUP OF SUPPLIERS'", at=C("relies on a limited"), color="#FFE0B2", size=28),
              it("sign", x=1260, y=260, text="MEMORY CHIP SWINGS", at=C("memory chips"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=390, text="PATENT CASE VS AWS SERVERS (ITC)", at=C("A patent case"), color="#FFCDD2", size=28),
              it("sign", x=1000, y=510, text="TAX POSITIONS ≈ $7.3BN", at=C("uncertain tax"), color="#F5F5F5", size=30),
              buddy(1700, 860, at=0.4, mood="worry", label="AWS", color="#FF9F1C", hop=12)]},
    sources=["tenq"])
stage("s36_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("are marks and claims"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("BUILD-OUT · $884BN COMMITMENTS", 0.3), ("THE LOOP · INVESTOR + SUPPLIER", 0.9), ("REGULATORS · AD AUCTIONS", 1.5)],
                    [("CEO: 'MAY HAVE TWO' $1TN BUSINESSES", C("The C E O says")), ("AI-LAB STAKES MARKED ≈ $289BN", C("Its stakes")), ("AWS: FASTEST GROWTH IN ~5 YEARS", C("trillion dollar revenue"))],
                    title="RISKS VS UPSIDE (AMAZON'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="MARKS AND CLAIMS, NOT CASH", at=C("are marks and claims"), color="#C8E6C9", size=28)]},
    sources=["rel", "tenq"])
kinetic("s37_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
stage("s38_score", "payoff", {
    "zones": [Z("boxport", signs=["SCOREBOARD", "NEXT REPORT: EARLY FEB 2027?", "WATCH THE CAPEX", "BACKLOG CHECK"], gateAt=0, gateWX=1800)], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}, {"at": C("If those hold up"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [scorecard([("AWS GROWTH + MARGIN", "Q3: +39% · 38.7% · BACKLOG VS $578BN", C("One, A W S")),
                         ("Q4 OPERATING INCOME", "VS $28.5-33.5BN GUIDE", C("Two, fourth quarter")),
                         ("CAPEX AND FREE CASH", "TTM FCF −$42.4BN · 2027 OUTLOOK", C("Three, capex"))], x=960, y=300, at=0.2, scale=0.9),
              stamp(1500, 960, at=0.5, scale=0.6),
              buddy(250, 900, at=0.4, mood="happy", moods=[[C("If they crack"), "worry"]], label="AMZN", color=ORANGE, hop=20)]},
    sources=["rel", "tenq"])
stage("s39_edition", "payoff2", {
    "zones": [machine(SEGS, "THE AMAZON MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [stamp(800, 900, at=0.3, scale=0.9),
              it("sign", x=1100, y=330, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=26)]},
    sources=["rel"])
add("s40_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_amazon_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Amazon (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
