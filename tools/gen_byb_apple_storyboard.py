"""Generates projects/before-you-buy-apple-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Apple, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit:
`moneymachine` set + `pricedin` / `riskscale` / `editionstamp` / `scorecard` items (tools/byb_kit.py helpers).
One visual language per part:
- Hook: chip city with a giant counter + edition stamp; the money machine; the disclaimer.
- Part 1 (the machine): the money machine with one pipe per revenue line; the shop; a box-and-arrow board.
- Part 2 (the cash): the bank hall (buybacks), the data center (AI costs), a bar board.
- Part 3 (what's priced in): the priced-in calculator (three lenses + gauge), the exchange, a bar board.
- Part 4 (what has to happen): the shop, the mint floor of phones, the exchange, the district at night.
- Part 5 (risks and upside): the court, parliament, the port, the risk scale.
- Payoff: the scorecard with the edition stamp.
Rules: no Apple logo, generic devices only, no real people drawn; numbers match sources.yaml; our calculations labelled.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_apple_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-apple-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q4 FY2026 (SEP 26, 2026)")
SEGS = [("IPHONE $254.1BN", 254.1, "#3DF5FF", None), ("SERVICES $123.3BN", 123.3, "#7DFF8A", None),
        ("MAC $37.9BN", 37.9, "#FF9F1C", None), ("WEARABLES $35.6BN", 35.6, "#FF4FD8", None), ("IPAD $27.9BN", 27.9, "#FFE14D", None)]
JOKES = ["NO FRUIT BEYOND THIS POINT", "MARGIN MAINTENANCE · HARD HATS", "SERVICES: QUIET, PLEASE", "UPGRADE CYCLE LANE"]

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("chipcity", signs=["FIVE TRILLION ST.", "NO LOITERING NEAR THE P/E", "PHONE PARKING ONLY", "CASH ONLY · NO CHECKS"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=700, y=230, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "Apple is worth"}, 5.06]], text="APPLE MARKET VALUE (OUR CALC.)", scale=1.3),
              it("sign", x=700, y=430, text="$348.51 × 14.53BN SHARES", at=C("at the close"), color="#BBDEFB", size=32),
              it("letters", x=1050, y=640, text="≈ 38× LAST YEAR'S PROFIT", at=C("By our math"), size=54, color="gold"),
              stamp(1480, 470, at=C("at the close"), scale=0.75),
              it("device", x=1780, y=860, type="phone", at=0.4, scale=1.5),
              buddy(480, 860, at=0.5, mood="happy", moods=[[C("By our math"), "shock"]], label="AAPL", hop=30)]},
    sources=["px", "tenk"])
stage("s02_twist", "h_twist", {
    "zones": [machine(SEGS, "THE APPLE MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("But the part"), "x": 1150, "y": 540, "zoom": 0.88, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=800, y=180, text="THE PHONE: MORE THAN HALF", at=C("the iPhone"), size=56, color="gold"),
              it("letters", x=1150, y=180, text="THE PROFIT STAR: YOU CAN'T HOLD IT", at=C("never hold"), size=50, color="gold"),
              buddy(2050, 860, at=0.4, mood="cool", label="SERVICES", color="#7DFF8A", hop=20)]},
    sources=["tenk"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=320, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=320, text="WHAT COULD BREAK IT?", at=C("what could break"), color="#FFCDD2", size=34),
              buddy(1000, 860, at=0.4, mood="worry", label="AAPL", hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: APPLE", at=0.4, size=64, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="APPLE'S", sources=["tenk"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Where the money comes from")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("The iPhone alone"))] + [(l, v, c, C("Mac, iPad")) for (l, v, c, _) in SEGS[2:]], "THE APPLE MACHINE", "SALES", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("Mac, iPad"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "of stuff"}, 478.8]], text="FY2026 NET SALES (10-K)", scale=1.0),
              it("sign", x=560, y=960, text="+15% (AFTER +6%)", at=C("the year before"), color="#C8E6C9", size=30),
              it("sign", x=650, y=860, text="IPHONE: 53% OF EVERYTHING", at=C("of everything"), color="#BBDEFB", size=30)]},
    sources=["tenk"])
stage("s08_services", "m1_services", {
    "zones": [machine(SEGS, "THE APPLE MACHINE", "PROFIT", JOKES, boomAt=4.0)], "worldW": 2600,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.0}, {"at": C("But its gross margin"), "x": 1150, "y": 540, "zoom": 0.88, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=800, y=180, text="THE INVISIBLE PIPE: SERVICES", at=0.2, size=54, color="gold"),
              it("sign", x=650, y=960, text="MARGIN: SERVICES 76% · HARDWARE 39%", at=C("But its gross margin"), color="#C8E6C9", size=30),
              it("sign", x=1300, y=960, text="25.8% OF SALES → 40% OF GROSS PROFIT", at=C("A quarter of the revenue"), color="#FFE0B2", size=30),
              buddy(2200, 860, at=0.4, mood="cool", moods=[[C("two fifths"), "happy"]], label="SERVICES", color="#7DFF8A", hop=24)]},
    sources=["tenk"])
stage("s09_where", "m1_where", {
    "zones": [Z("port", x1=1500), Z("shop", x0=1500)], "worldW": 3200,
    "cam": [{"at": 0, "x": 750, "y": 520, "zoom": 1.0}, {"at": C("About"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}, {"at": C("And almost all"), "x": 900, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 1,
    "items": [it("counter", x=750, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "came roaring back"}, 82.4]], text="GREATER CHINA, FY2026 (+28%)"),
              it("sign", x=2200, y=200, text="≈ 60% VIA CARRIERS, RETAILERS, RESELLERS", at=C("About"), color="#BBDEFB", size=28),
              it("device", x=2000, y=860, type="phone", at=C("About"), scale=1.2), it("device", x=2350, y=860, type="laptop", at=C("own stores"), scale=1.0),
              it("sign", x=900, y=330, text="BUILT BY PARTNERS: CHINA · INDIA · VIETNAM …", at=C("And almost all"), color="#FFE0B2", size=26),
              ship(kind="cargo", x=[[0, 300], [12, 1100]], y=760, scale=0.7)]},
    sources=["tenk"])
stage("s09b_rhythm", "m1_rhythm", {
    "zones": [Z("shop")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Now look at"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="ONE GIANT QUARTER", at=0.2, until=C("Now look at"), size=60, color="gold"),
              it("counter", x=800, y=280, at=C("The December quarter"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "brought in"}, 143.8]], text="DEC QUARTER = 30% OF THE YEAR", until=C("Now look at")),
              it("letters", x=1000, y=100, text="SEP QUARTER, YEAR OVER YEAR", at=C("Now look at"), size=52, color="gold"),
              it("sign", x=560, y=260, text="IPHONE +17.5%", at=C("The iPhone grew"), color="#C8E6C9", size=32),
              it("sign", x=940, y=260, text="MAC +23.7%", at=C("and the Mac"), color="#C8E6C9", size=32),
              it("sign", x=1320, y=260, text="IPAD −10.4%", at=C("the iPad fell"), color="#FFCDD2", size=32),
              it("sign", x=1700, y=360, text="WEARABLES −7.9%", at=C("wearables slipped"), color="#FFCDD2", size=30),
              buddy(450, 860, at=0.3, mood="happy", label="AAPL", hop=14)]},
    sources=["tenk", "q4"])
board("p10_machine", "m1_draw", "The machine (FY2026, 10-K)", C("Here are the products"), [
    {"d": rect(640, 420, 300, 180), "color": "accent2", "width": 6, "kind": "box", "start": C("Here are the products"), "label": lbl("PRODUCTS · 39% MARGIN", 790, 518, 20, "accent2")},
    {"d": rect(640, 700, 300, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is Services"), "label": lbl("SERVICES · 76% MARGIN", 790, 768, 20, "accent3")},
    {"d": rect(1180, 540, 300, 180), "color": "accent", "width": 6, "kind": "box", "start": C("Both pour into"), "label": lbl("GROSS PROFIT", 1330, 638, 22, "accent")},
    {"d": arrow((945, 510), (1175, 590)), "color": "ink", "width": 5, "kind": "arrow", "start": C("Both pour into"), "label": lbl("60%", 1060, 520, 18, "ink")},
    {"d": arrow((945, 760), (1175, 680)), "color": "accent3", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("40%", 1060, 760, 20, "accent3")},
], C("every point", 0.1), [1060, 720], sources=["tenk"])
kinetic("s11_t1", "m1_transition", [("A machine that profitable…", 66, "A machine that profitable", None, False),
                                    ("…where does the cash go?", 72, "where does the cash go", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Where a year of cash went")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So free cash flow"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Operating cash flow"}, 145.1]], text="OPERATING CASH FLOW FY2026"),
              it("sign", x=1350, y=280, text="CAPEX ONLY $9.0BN (≈ 6%)", at=C("Capital spending"), color="#FFE0B2", size=30),
              it("letters", x=1100, y=430, text="FREE CASH ≈ $136BN (OUR CALC.)", at=C("So free cash flow"), size=50, color="gold"),
              it("sign", x=1100, y=560, text="NET INCOME $132.2BN", at=C("more than net income"), color="#C8E6C9", size=28),
              coins(400, 700, [1600, 760], at=C("So free cash flow"), rate=6)]},
    sources=["tenk"])
stage("s14_returns", "m2_returns", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The share count"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=140, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "bought back"}, 85.8]], text="BUYBACKS FY2026 (10-K)"),
              it("sign", x=1400, y=250, text="+ DIVIDENDS ≈ $15.7BN", at=C("in dividends"), color="#FFE0B2", size=30),
              it("letters", x=1100, y=400, text="≈ 75% OF FREE CASH, HANDED BACK", at=C("Together"), size=48, color="gold"),
              it("counter", x=1300, y=640, at=C("The share count"), prefix="", suffix="BN SHARES", decimals=2, steps=[[0, 15.63], [{"cue": "so each remaining"}, 14.53]], text="SHARES OUTSTANDING, JUL 2023 → OCT 2026"),
              it("sign", x=1300, y=840, text="SHARES: −7% SINCE MID-2023", at=C("The share count"), color="#C8E6C9", size=28)]},
    sources=["tenk"])
stage("s15_ai", "m2_ai", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And Apple says"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="LOW CAPEX ≠ FREE AI", at=0.2, size=60, color="gold"),
              it("counter", x=800, y=260, at=C("Research and development"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "jumped"}, 45.8]], text="R&D FY2026 (+32%)"),
              it("sign", x=1450, y=380, text="COMPUTE: THIRD-PARTY CLOUD", at=C("And Apple says"), color="#BBDEFB", size=30),
              it("sign", x=1100, y=520, text="PART OF THE AI BILL = EXPENSE, NOT CAPEX", at=C("So part of"), color="#FFE0B2", size=28),
              buddy(500, 860, at=0.3, mood="worry", label="AI", color="#7B61FF", hop=14)]},
    sources=["tenk"])
stage("s15b_quality", "m2_quality", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Part of that"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}, {"at": C("And the day before"), "x": 1000, "y": 520, "zoom": 1.05, "dur": 1.6}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A FOOTNOTE ON THE CASH", at=0.2, size=58, color="gold"),
              it("counter", x=800, y=270, at=C("Operating cash flow"), prefix="$", suffix="BN", decimals=1, steps=[[0, 111.5], [{"cue": "jumped"}, 145.1]], text="OPERATING CASH FLOW (+30%)"),
              it("sign", x=1280, y=250, text="OTHER LIABILITIES: +$13.7BN (VS −$11.1BN)", at=C("A swing in"), color="#FFE0B2", size=28),
              it("sign", x=1280, y=360, text="INVENTORIES $5.7BN → $14.5BN", at=C("And inventories"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=520, text="NOV 9: $7.5BN OF NEW BONDS (8-K)", at=C("Apple still sold"), color="#BBDEFB", size=30),
              buddy(1700, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenk"])
board("p16_cash", "m2_draw", "Where a year of free cash went (FY2026)", C("Here is the free cash flow bar"), [
    {"d": "M 700 760 L 1560 760", "color": "ink", "width": 4, "start": C("Here is the free cash flow bar"), "label": lbl("$BN · 10-K · OUR CALC.", 1130, 810, 18, "ink")},
    bar(740, 150, 760, 360, "accent2", C("Here is the free cash flow bar"), "FCF 136"),
    bar(940, 150, 760, 507, "accent", C("Here is the buyback bar"), "BUYBACKS 86"),
    bar(1140, 150, 760, 714, "accent3", C("Here are the dividends"), "DIVIDENDS 16"),
    bar(1340, 150, 760, 660, "risk", C("this small piece"), "LEFT ≈ 34"),
], C("straight back", 0.1), [1015, 560], sources=["tenk"])
kinetic("s17_t2", "m2_transition", [("At five trillion dollars…", 70, "At five trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s18_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s19_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Apple has net cash"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (FY2026, OUR CALC.)", note="NET CASH ≈ $57BN · ≈ 1% OF THE PRICE",
                    base="FREE CASH FLOW (CAPEX STEADY)",
                    lenses=[("P/E (NET INCOME)", "38.3×", C("Price to earnings")), ("FCF YIELD", "2.7%", C("Free cash flow")), ("OCF YIELD", "2.9%", C("Operating cash flow"))]),
              stamp(1500, 900, at=0.4, scale=0.7)]},
    sources=["tenk", "px"])
stage("s20_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 10.5, C("With an eight percent"), "≈ 10.5% / YR"), ("AT 10%", 15.5, C("With ten percent"), "≈ 15.5% / YR"),
                    ["MARKET CAP $5.06TN (NOV 10)", "FCF FY2026 $136.1BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED FCF GROWTH, 10 YEARS", placardX=860, placardY=-200),
              stamp(1200, 940, at=0.6, scale=0.6),
              buddy(1740, 860, at=0.5, mood="happy", moods=[[C("With ten percent"), "shock"]], label="AAPL", hop=22)]},
    sources=["tenk", "px"])
stage("s21_zero", "m3_zero", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So more than half"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="IF CASH NEVER GREW…", at=0.2, size=60, color="gold"),
              it("sign", x=700, y=260, text="≈ $2.2TN AT 8%", at=C("worth"), color="#BBDEFB", size=34),
              it("sign", x=1300, y=260, text="≈ $1.6TN AT 10%", at=C("or"), color="#BBDEFB", size=34),
              it("letters", x=1000, y=420, text="> HALF THE PRICE = A BET ON GROWTH", at=C("So more than half"), size=46, color="gold"),
              buddy(1000, 860, at=0.4, mood="shock", moods=[[C("So more than half"), "cool"]], label="AAPL", hop=26)]},
    sources=["tenk", "px"])
board("p22_gap", "m3_draw", "Flat cash vs the price (our illustration)", C("Here is what flat cash"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is what flat cash"), "label": lbl("$TN · OUR CALC. · NOV 10, 2026", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 622, "accent2", C("Here is what flat cash"), "FLAT @10% 1.6"),
    bar(1010, 170, 780, 562, "accent3", C("Here it is at eight"), "FLAT @8% 2.2"),
    bar(1240, 170, 780, 286, "accent", C("And here is the actual price"), "PRICE 5.06"),
    {"d": arrow((1190, 560), (1235, 320), 0.1), "color": "risk", "width": 5, "kind": "arrow", "start": C("That gap"), "label": lbl("THE GAP", 1150, 450, 18, "risk")},
], C("paying for in advance", 0.1), [1320, 420], sources=["tenk", "px"])
stage("s23_history", "m3_history", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So the price assumes"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("calendar", x=600, y=300, at=0.2, pages=[[0, "FY2025", "+6%"], [C("Last year"), "FY2026", "+15%"]]),
              it("letters", x=1300, y=200, text="PRICE NEEDS ≈ 10.5–15.5% FCF GROWTH", at=C("So the price assumes"), size=42, color="gold"),
              it("sign", x=1300, y=360, text="THE STRONG YEAR CAN'T BE A ONE-OFF", at=C("not a one off"), color="#FFE0B2", size=30),
              buddy(1600, 860, at=0.4, mood="worry", label="AAPL", hop=16)]},
    sources=["tenk"])
kinetic("s24_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s25_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s26_iphone", "m4_iphone", {
    "zones": [Z("mintfloor")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A record year"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="1 · THE PHONE KEEPS COMPOUNDING", at=0.2, size=52, color="gold"),
              it("sign", x=750, y=230, text="IPHONE $254.1BN · +21%", at=C("It just grew"), color="#BBDEFB", size=32),
              it("sign", x=1350, y=340, text="NEEDS: UPGRADES + CHIPS + MEMORY", at=C("Beating that"), color="#FFE0B2", size=28),
              it("device", x=[[0, 300], [8, 900]], y=860, type="phone", at=0.4, scale=1.3), it("device", x=[[0, 100], [8, 700]], y=860, type="phone", at=0.6, scale=1.3),
              it("device", x=[[0, -100], [8, 500]], y=860, type="phone", at=0.8, scale=1.3),
              it("letters", x=1300, y=500, text="A RECORD IS ALSO A HIGHER BAR", at=C("A record year"), size=40, color="gold")]},
    sources=["tenk"])
stage("s27_services", "m4_services", {
    "zones": [machine(SEGS, "THE APPLE MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("If that line"), "x": 1150, "y": 540, "zoom": 0.88, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=900, y=180, text="2 · SERVICES KEEPS GROWING", at=0.2, size=52, color="gold"),
              it("calendar", x=2100, y=300, at=C("but its growth slowed"), pages=[[0, "Q2", "+16%"], [C("in the September quarter"), "Q4", "+9.8%"]]),
              buddy(2250, 860, at=0.3, mood="happy", moods=[[C("If that line"), "worry"]], label="SERVICES", color="#7DFF8A", hop=18)]},
    sources=["tenk", "q4"])
stage("s28_margin", "m4_margin", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Apple itself warns"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="3 · MARGINS HOLD", at=0.2, size=58, color="gold"),
              it("counter", x=750, y=240, at=C("gross margin was"), prefix="", suffix="%", decimals=1, steps=[[0, 0], [{"cue": "that included"}, 47.9]], text="GROSS MARGIN, SEP QUARTER"),
              it("sign", x=750, y=420, text="INCL. ≈ 1 PT TARIFF REFUNDS", at=C("tariff refunds"), color="#FFCDD2", size=28),
              it("sign", x=1400, y=320, text="APPLE: 'DOWNWARD PRESSURE'", at=C("Apple itself warns"), color="#FFE0B2", size=30),
              it("ramstick", x=1450, y=640, at=C("memory and storage"), scale=0.9),
              it("pricetag", x=1700, y=520, at=C("expected to rise"), text="MEMORY", pages=[[C("expected to rise"), "MEMORY ↑", True]])]},
    sources=["q4", "tenk"])
stage("s29_china", "m4_china", {
    "zones": [Z("district", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("because the region"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="4 · CHINA KEEPS BUYING", at=0.2, size=56, color="gold"),
              it("calendar", x=600, y=280, at=C("That rebound"), pages=[[0, "FY2025", "−4%"], [C("heavy lifting"), "FY2026", "+28%"]]),
              it("sign", x=1350, y=300, text="GREATER CHINA $82.4BN ≈ 17% OF SALES", at=C("because the region"), color="#BBDEFB", size=28),
              buddy(1500, 860, at=0.4, mood="happy", moods=[[C("One weak year"), "worry"]], label="AAPL", hop=24)]},
    sources=["tenk"])
kinetic("s30_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s31_c5", "m5_card", "Risks and Upside", "What Apple itself warns about")
stage("s32_courts", "m5_courts", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The App"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 1 · THE COURTS", at=0.2, size=58, color="gold"),
              it("sign", x=1000, y=240, text="GOOGLE SEARCH LICENSING: AMOUNT NOT DISCLOSED", at=C("Apple earns licensing"), color="#FFE0B2", size=24),
              it("sign", x=1300, y=360, text="APP STORE VS EPIC → SUPREME COURT", at=C("The App"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=480, text="DOJ ANTITRUST SUIT (2024): ONGOING", at=C("antitrust suit is still"), color="#FFCDD2", size=28),
              it("gavel", x=1650, y=500, hits=[C("headed to the Supreme Court"), C("is still going")])]},
    sources=["tenk"])
stage("s33_europe", "m5_europe", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On last"), "x": 1200, "y": 500, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 2 · EUROPE (DMA)", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=250, text="2025 FINE: UNDER APPEAL", at=C("already fined"), color="#FFE0B2", size=30),
              it("sign", x=1300, y=360, text="CEILING: 10% OF WORLDWIDE SALES ≈ $48BN", at=C("On last"), color="#FFCDD2", size=28),
              it("letters", x=1000, y=500, text="A LEGAL MAXIMUM, NOT AN ESTIMATE", at=C("legal maximum"), size=40, color="gold")]},
    sources=["tenk"])
stage("s34_tariffs", "m5_tariffs", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And on"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="RISK 3 · WHAT APPLE DOESN'T CONTROL", at=0.2, size=50, color="gold"),
              it("sign", x=650, y=250, text="TARIFFS", at=C("Tariffs"), color="#FFCDD2", size=34),
              it("sign", x=1000, y=250, text="MEMORY PRICES ↑", at=C("Memory prices"), color="#FFE0B2", size=34),
              it("sign", x=1400, y=250, text="THE AI RACE", at=C("artificial intelligence"), color="#BBDEFB", size=34),
              ship(kind="cargo", x=[[0, 200], [10, 1300]], y=760, scale=0.7),
              buddy(1700, 860, at=0.4, mood="worry", label="AAPL", hop=12)]},
    sources=["tenk"])
stage("s34b_partners", "m5_partners", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("On the selling side"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="RISK 4 · A FEW BIG PARTNERS", at=0.2, size=52, color="gold"),
              it("sign", x=640, y=250, text="2 SUPPLIERS: 45% + 27%", at=C("just two suppliers"), color="#FFE0B2", size=32),
              it("sign", x=1340, y=250, text="CARRIERS: 33% OF RECEIVABLES", at=C("phone carriers"), color="#BBDEFB", size=30),
              it("sign", x=1260, y=360, text="ONE CUSTOMER: 13%", at=C("one single customer"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=520, text="NAMES NOT DISCLOSED (10-K)", at=C("doesn't name"), color="#F5F5F5", size=28),
              ship(kind="cargo", x=[[0, 200], [12, 1400]], y=760, scale=0.7),
              buddy(1700, 860, at=0.4, mood="worry", label="AAPL", hop=12)]},
    sources=["tenk"])
stage("s35_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("None of that"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("COURTS · GOOGLE · APP STORE", 0.3), ("EU DMA (UP TO 10%)", 0.9), ("TARIFFS · MEMORY · AI RACE", 1.5)],
                    [("INSTALLED BASE: RECORD", C("installed base")), ("CLOUD AI SERVICES", C("New cloud services")), ("ADVERTISING", C("And advertising"))],
                    title="RISKS VS UPSIDE (APPLE'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="UPSIDE IS UNSIZED: NO NUMBERS GIVEN", at=C("None of that"), color="#C8E6C9", size=28)]},
    sources=["tenk", "q4"])
kinetic("s36_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
stage("s37_score", "payoff", {
    "zones": [Z("chipcity", night=True, signs=["SCOREBOARD", "NEXT REPORT: LATE JAN 2027?", "WATCH THE MARGIN", "SERVICES CHECK"])], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}, {"at": C("If those three"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [scorecard([("DECEMBER-QUARTER REVENUE", "VS $143.8BN A YEAR EARLIER", C("One, December")),
                         ("GROSS MARGIN", "VS 47.9% (INCL. TARIFF REFUNDS)", C("Two, gross margin")),
                         ("SERVICES GROWTH", "VS +9.8% IN THE SEP QUARTER", C("Three, Services"))], x=960, y=220, at=0.2, scale=0.92),
              stamp(1500, 900, at=0.5, scale=0.7),
              buddy(300, 900, at=0.4, mood="happy", moods=[[C("If they crack"), "worry"]], label="AAPL", hop=20)]},
    sources=["q4", "tenk"])
stage("s38_edition", "payoff2", {
    "zones": [machine(SEGS, "THE APPLE MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [stamp(800, 900, at=0.3, scale=0.9),
              it("sign", x=1100, y=200, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=26)]},
    sources=["tenk"])
add("s39_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_apple_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Apple (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
