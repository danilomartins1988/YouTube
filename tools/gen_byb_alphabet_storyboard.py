"""Generates projects/before-you-buy-alphabet-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Alphabet, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit from
tools/byb_kit.py. Alphabet's own world: the INFO LIBRARY (new `infolibrary` set: glowing book-towers, a giant search bar
that types, ad tokens dropping down coin chutes, cloud carts on a rail), plus the data center, the money machine, the
bank hall, the court and the exchange. One visual language per part:
- Hook: info library with a giant counter + edition stamp; data center; exchange; the disclaimer.
- Part 1 (the machine): money machine (Services / Cloud / Other Bets); the library (Search); cloud carts lit (Cloud); board.
- Part 2 (the cash): vault, data center, bank hall (new shares), library (no buybacks), bar board.
- Part 3 (what's priced in): calculator (three lenses), data center (proxy), calculator (gauge), library (capex must earn), board.
- Part 4 (what has to happen): office (backlog), site (payback), library + court (Search), bank hall (funding).
- Part 5 (risks and upside): data center going dark, court, parliament-like boardroom (control), risk scale.
- Payoff: scorecard with the edition stamp.
Rules: no logos, generic shapes only, no real people drawn; numbers match sources.yaml; our calculations labelled.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_alphabet_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-alphabet-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q3 2026 (SEP 30, 2026)")
SEGS = [("SERVICES $342.7BN", 342.7, "#3DF5FF", None), ("CLOUD $58.7BN", 58.7, "#7DFF8A", None), ("OTHER BETS $1.5BN", 1.5, "#FF9F1C", None)]
JOKES = ["ANSWERS DEPT · ALL FLOORS", "ADS · NEXT TO EVERYTHING", "CAPEX ZONE · HARD HATS", "MOONSHOTS · MIND THE GAP"]
LIB = ["QUIET: INDEXING", "ANSWERS · AISLE ∞", "ADS NEXT TO EVERYTHING", "NO SHUSHING THE ROBOTS"]
BLUE = "#3DF5FF"

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("infolibrary", signs=LIB, query="WHAT IS IT WORTH?")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=650, y=420, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "is worth"}, 3.52]], text="ALPHABET MARKET VALUE (OUR CALC.)", scale=1.2),
              it("sign", x=650, y=600, text="ALL 3 SHARE CLASSES · 12.3BN SHARES", at=C("every share class"), color="#BBDEFB", size=28),
              it("letters", x=1150, y=760, text="≈ 178× LAST 12 MONTHS' FREE CASH", at=C("by our math"), size=48, color="gold"),
              stamp(1450, 470, at=C("every share class"), scale=0.7),
              buddy(300, 880, at=0.5, mood="happy", moods=[[C("by our math"), "shock"]], label="GOOG", color="#7DFF8A", hop=30)]},
    sources=["px", "tenq"])
stage("s02_twist", "h_twist", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("Free cash flow was negative"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=200, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "on property"}, 159.8]], text="CAPEX, LAST 12 MONTHS (OUR CALC.)"),
              it("sign", x=1350, y=330, text="= 89% OF OPERATING CASH", at=C("of its operating cash"), color="#FFE0B2", size=30),
              it("sign", x=1100, y=460, text="FREE CASH: NEGATIVE 2 QUARTERS IN A ROW", at=C("Free cash flow was negative"), color="#FFCDD2", size=28),
              it("letters", x=1100, y=600, text="NO BUYBACKS · NEW STOCK SOLD", at=C("instead of buying back"), size=46, color="gold"),
              it("isodc", x=1500, y=820, at=C("Free cash flow was negative"), n=6, step=0.25, cols=3, scale=0.5, glow=True),
              buddy(420, 880, at=0.4, mood="worry", label="FCF", color="#7DFF8A", hop=14)]},
    sources=["rel", "tenq"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=200, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=360, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=360, text="WHAT COULD BREAK IT?", at=C("what could"), color="#FFCDD2", size=34),
              buddy(1000, 880, at=0.4, mood="worry", label="GOOG", color="#7DFF8A", hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: ALPHABET", at=0.4, size=60, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="ALPHABET'S", sources=["tenq"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Search, Cloud and the bets")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("Google Services")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("Google Cloud made")),
                       (SEGS[2][0], SEGS[2][1], SEGS[2][2], C("the Other Bets"))], "THE ALPHABET MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("the Other Bets"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "brought in"}, 402.8]], text="FY2025 REVENUE (10-K)", scale=1.0),
              it("sign", x=650, y=860, text="SERVICES MARGIN ≈ 41%", at=C("at an operating margin"), color="#BBDEFB", size=30),
              it("sign", x=560, y=960, text="OTHER BETS: −$7.5BN", at=C("the Other Bets"), color="#FFCDD2", size=30),
              it("sign", x=1150, y=960, text="> 70% FROM ADS", at=C("seventy percent"), color="#FFE0B2", size=30)]},
    sources=["rel"])
stage("s08_search", "m1_search", {
    "zones": [Z("infolibrary", signs=LIB, query="BEST PIZZA NEAR ME")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("In the September quarter"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=750, y=560, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "brought in"}, 250.1]], text="SEARCH & OTHER, 12 MONTHS (OUR CALC.)"),
              it("sign", x=750, y=730, text="≈ 53% OF EVERYTHING", at=C("of everything"), color="#BBDEFB", size=30),
              it("sign", x=1450, y=560, text="Q3: +12% · PAID CLICKS +8%", at=C("In the September quarter"), color="#C8E6C9", size=30),
              it("sign", x=1450, y=700, text="YOUTUBE ADS $43.5BN", at=C("YouTube ads"), color="#FFE0B2", size=30),
              buddy(1850, 880, at=0.4, mood="happy", label="SEARCH", color=BLUE, hop=28)]},
    sources=["rel", "tenq"])
stage("s09_cloud", "m1_cloud", {
    "zones": [Z("infolibrary", signs=["CLOUD CARTS · NOW BOARDING", "TPU SYSTEMS · FOR SALE", "BACKLOG · PLEASE WAIT", "ANSWERS · AISLE ∞"], query="RENT ME A SUPERCOMPUTER", cloudAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Part of that growth"), "x": 1150, "y": 500, "zoom": 1.08, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=700, y=560, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Google Cloud made"}, 30.7]], text="GOOGLE CLOUD, SEP QUARTER (+103%)"),
              it("sign", x=700, y=730, text="CLOUD MARGIN ≈ 36%", at=C("at an operating margin"), color="#C8E6C9", size=30),
              it("sign", x=1450, y=560, text="NEW: SELLING ITS OWN AI CHIP SYSTEMS", at=C("Part of that growth"), color="#BBDEFB", size=28),
              it("letters", x=1300, y=760, text="CLOUD BACKLOG ≈ $568BN", at=C("the Cloud backlog"), size=46, color="gold"),
              buddy(1900, 880, at=0.5, mood="shock", moods=[[C("the Cloud backlog"), "cool"]], label="TPU", color="#7DFF8A", hop=22, scale=1.2)]},
    sources=["rel", "tenq"])
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And advertising fell"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE MIX IS SHIFTING", at=0.2, size=60, color="gold"),
              it("sign", x=760, y=250, text="U.S. 53% OF REVENUE (+39%)", at=C("the United States"), color="#BBDEFB", size=30),
              it("sign", x=1260, y=250, text="WAS 48% LAST YEAR", at=C("up from"), color="#F5F5F5", size=30),
              it("sign", x=760, y=380, text="ADS: 64% OF THE QUARTER", at=C("And advertising fell"), color="#FFE0B2", size=30),
              it("sign", x=1260, y=380, text="PARTNER IMPRESSIONS −14%", at=C("Impressions on partner"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=520, text="'HALF-TRILLION RUN RATE' (CEO CLAIM)", at=C("Sundar Pichai"), color="#C8E6C9", size=28),
              buddy(1700, 860, at=0.3, mood="happy", label="GOOG", color="#3DF5FF", hop=14)]},
    sources=["tenq", "rel"])
board("p10_machine", "m1_draw", "The machine (FY2025 + Q3 2026)", C("Here is Google Services"), [
    {"d": rect(1080, 420, 360, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is Google Services"), "label": lbl("SERVICES · 41% MARGIN", 1260, 528, 20, "accent2")},
    {"d": rect(640, 450, 260, 140), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is Google Cloud"), "label": lbl("CLOUD +103%", 770, 528, 20, "accent3")},
    {"d": rect(1080, 700, 360, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Here are the Other Bets"), "label": lbl("OTHER BETS · LOSS", 1260, 768, 20, "risk")},
    {"d": arrow((770, 780), (770, 600), 0.15), "color": "accent", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("BACKLOG ≈ $568BN", 770, 820, 20, "accent")},
    {"d": arrow((905, 520), (1075, 520)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("Cloud revenue"), "label": lbl("REVENUE", 990, 500, 18, "accent3")},
], C("Cloud revenue", 0.1), [770, 680], sources=["rel", "tenq"])
kinetic("s11_t1", "m1_transition", [("A machine that profitable…", 70, "A machine that profitable", None, False),
                                    ("…where did the cash go?", 72, "where did it all go", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Where twelve months of cash went")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("What was left"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=160, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Operating cash flow"}, 179.6]], text="OPERATING CASH FLOW, 12 MONTHS"),
              it("sign", x=1400, y=300, text="NET INCOME $235.7BN · ≈ $130BN PAPER GAINS", at=C("Net income was even higher"), color="#FFE0B2", size=26),
              it("sign", x=1400, y=420, text="CAPEX −$159.8BN", at=C("Capex took"), color="#FFCDD2", size=32),
              it("letters", x=1100, y=560, text="FREE CASH ≈ $20BN (OUR CALC.)", at=C("What was left"), size=50, color="gold"),
              coins(400, 700, [1600, 760], at=0.4, rate=6, until=C("Capex took")),
              coins(1600, 700, [2200, 900], at=C("Capex took"), rate=7)]},
    sources=["rel", "tenq"])
stage("s14_quarter", "m2_quarter", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("The company says"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("calendar", x=650, y=320, at=0.2, pages=[[0, "Q2 2026", "FCF −$5.9BN"], [C("in September"), "Q3 2026", "FCF −$9.1BN"]]),
              it("sign", x=1350, y=250, text="'SIGNIFICANTLY INCREASE' INVESTMENT IN 2026", at=C("The company says"), color="#FFE0B2", size=26),
              it("letters", x=1300, y=420, text="THE BILL IS STILL RISING", at=C("the bill is still rising"), size=48, color="gold"),
              it("isodc", x=1400, y=800, at=C("The company says"), n=9, step=0.18, cols=3, scale=0.6, glow=True)]},
    sources=["tenq"])
stage("s15_funding", "m2_funding", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Long-term debt"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("counter", x=800, y=160, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "of new common stock"}, 42.9]], text="NEW COMMON STOCK SOLD IN 2026 (10-Q)"),
              it("sign", x=1400, y=300, text="+ $19.1BN CONVERTIBLE PREFERRED", at=C("plus"), color="#FFE0B2", size=28),
              it("sign", x=1100, y=430, text="LONG-TERM DEBT $46.5BN → $126.1BN", at=C("Long-term debt"), color="#FFCDD2", size=30),
              it("sign", x=1100, y=560, text="STILL ≈ $28BN OF ROOM TO SELL MORE SHARES", at=C("room to sell"), color="#BBDEFB", size=26),
              buddy(450, 880, at=0.4, mood="worry", label="GOOG", color="#7DFF8A", hop=14)]},
    sources=["tenq"])
stage("s16_returns", "m2_returns", {
    "zones": [Z("infolibrary", signs=["BUYBACKS · CLOSED FOR NOW", "NEW SHARES · AISLE 2", "DIVIDENDS · STILL OPEN", "QUIET: INDEXING"], query="WHERE DID THE BUYBACKS GO?")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But the share count"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=540, text="BUYBACKS IN 2026: $0", at=C("the buybacks stopped"), size=60, color="gold"),
              it("sign", x=700, y=700, text="DIVIDENDS ≈ $10.7BN (12 MONTHS)", at=C("in dividends"), color="#C8E6C9", size=28),
              it("sign", x=1400, y=700, text="SHARE COUNT +1.8% IN A YEAR", at=C("But the share count"), color="#FFCDD2", size=30),
              buddy(1900, 880, at=0.4, mood="worry", label="SHARES", color="#FF9F1C", hop=16)]},
    sources=["tenq"])
stage("s16b_stakes", "m2_stakes", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Those are marks"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A PILE OF STAKES", at=0.2, size=60, color="gold"),
              it("sign", x=760, y=250, text="SPACEX SHARES $75.2BN (RESTRICTED)", at=C("of SpaceX shares"), color="#BBDEFB", size=28),
              it("sign", x=1260, y=250, text="ONE PRIVATE CO. ≈ $128.2BN", at=C("one unnamed private"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=370, text="≈ 6% OF MARKET VALUE (OUR CALC.)", at=C("Together, by our math"), color="#FFF8E1", size=28),
              it("sign", x=1000, y=480, text="Q3: −$8.2BN ON PAPER", at=C("they cost"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=590, text="JUNE OFFER $355.20 → NOV 10 CLOSE $287.38", at=C("the new shares"), color="#FFE0B2", size=28),
              buddy(1700, 860, at=0.3, mood="worry", label="GOOG", color="#3DF5FF", hop=12)]},
    sources=["tenq", "px"])
board("p17_cash", "m2_draw", "Where twelve months of operating cash went", C("Here is the operating cash bar"), [
    {"d": "M 700 780 L 1560 780", "color": "ink", "width": 4, "start": C("Here is the operating cash bar"), "label": lbl("$BN · OUR CALC.", 1130, 830, 18, "ink")},
    bar(740, 150, 780, 380, "accent2", C("Here is the operating cash bar"), "OCF 180"),
    bar(940, 150, 780, 424, "risk", C("Here is the capex bar"), "CAPEX 160"),
    bar(1140, 150, 780, 736, "accent3", C("Here is what's left"), "FCF 20"),
    bar(1340, 150, 780, 645, "accent", C("And here is the new stock"), "NEW STOCK 62"),
], C("coming in from outside", 0.1), [1415, 620], sources=["tenq"])
kinetic("s18_t2", "m2_transition", [("At three and a half trillion…", 70, "At three and a half trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s19_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s20_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("The gap between"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (TTM, OUR CALC.)", note="P/E ≈ 26× WITHOUT THE PAPER GAINS",
                    base="TO BE CHOSEN: CAPEX IS BOOMING",
                    lenses=[("P/E (NET INCOME)", "14.9×", C("Price to earnings")), ("FCF YIELD", "0.6%", C("Free cash flow yield")), ("OCF YIELD", "5.1%", C("Operating cash"))]),
              stamp(400, 960, at=0.4, scale=0.6)]},
    sources=["rel", "px"])
stage("s21_proxy", "m3_proxy", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It's a proxy"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=200, text="A PROXY FOR A BUILDING SPREE", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=340, text="OCF $179.6BN", at=C("We take operating cash"), color="#BBDEFB", size=32),
              it("sign", x=1100, y=340, text="− DEPRECIATION ≈ $28.0BN", at=C("subtract depreciation"), color="#FFCDD2", size=32),
              it("letters", x=1000, y=500, text="= ≈ $151.6BN · YIELD ≈ 4.3%", at=C("That leaves"), size=50, color="gold"),
              it("sign", x=1300, y=640, text="ASSUMES CAPEX FALLS BACK TOWARD DEPRECIATION", at=C("It's a proxy"), color="#FFE0B2", size=24),
              buddy(1850, 880, at=0.4, mood="cool", label="PROXY", color="#FFE14D", hop=16)]},
    sources=["tenq", "px"])
stage("s22_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 4.5, C("With an eight percent"), "≈ 4.5% / YR"), ("AT 10%", 9.2, C("With ten percent"), "≈ 9.2% / YR"),
                    ["MARKET CAP $3.52TN (NOV 10)", "PROXY: OCF − DEPREC. $151.6BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED GROWTH, 10 YEARS", base="PROXY (CAPEX BOOM)", placardX=860, placardY=-200),
              it("sign", x=1500, y=880, text="ON TODAY'S FCF: ≈ 31-38% / YR", at=C("But run the same math"), color="#FFCDD2", size=30),
              stamp(1150, 980, at=0.6, scale=0.5),
              buddy(1750, 640, at=0.5, mood="happy", moods=[[C("the answer jumps"), "shock"]], label="GOOG", color="#7DFF8A", hop=22, scale=0.8)]},
    sources=["tenq", "px"])
stage("s23_mustearn", "m3_mustearn", {
    "zones": [Z("infolibrary", signs=["EVERY DOLLAR MUST WORK", "RETURN TO SENDER?", "CAPEX IN · CASH OUT", "QUIET: INDEXING"], query="WILL THE CAPEX PAY OFF?", cloudAt=0)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("every dollar of capex"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=520, text="WHAT THE CAPEX MUST EARN", at=0.2, size=58, color="gold"),
              it("sign", x=1000, y=640, text="IF CAPEX STAYS ≈ $160BN A YEAR…", at=C("keeps spending"), color="#BBDEFB", size=30),
              it("letters", x=1000, y=770, text="EACH $1 → +17¢ TO +29¢ OF YEARLY CASH", at=C("every dollar of capex"), size=44, color="gold"),
              it("sign", x=1000, y=890, text="WITHIN 10 YEARS · OUR ROUGH ILLUSTRATION", at=C("within a decade"), color="#FFE0B2", size=26)]},
    sources=["tenq", "px"])
board("p24_two", "m3_draw", "Two answers, one price (our illustration)", C("Here is the growth the price needs"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is the growth the price needs"), "label": lbl("% A YEAR · 10 YEARS · OUR CALC.", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 712, "accent3", C("Here is the growth the price needs"), "PROXY @8% 4.5"),
    bar(1010, 170, 780, 640, "accent2", C("Here it is at the higher rate"), "PROXY @10% 9.2"),
    bar(1240, 170, 780, 300, "risk", C("And here is what it needs"), "FCF 31-38"),
    {"d": arrow((1180, 600), (1235, 330), 0.1), "color": "accent", "width": 5, "kind": "arrow", "start": C("The difference"), "label": lbl("THE CAPEX", 1130, 470, 18, "accent")},
], C("the spending", 0.1), [1320, 400], sources=["tenq", "px"])
kinetic("s25_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s26_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s27_backlog", "m4_backlog", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("One caution"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="1 · THE CLOUD BACKLOG CONVERTS", at=0.2, size=52, color="gold"),
              it("counter", x=750, y=290, at=C("just over fifty-five percent"), prefix="≈ $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "over the next two years"}, 312]], text="EXPECTED IN 24 MONTHS (OUR CALC.)"),
              it("sign", x=1400, y=330, text="BACKLOG $567.7BN · 55%+ IN 2 YEARS", at=C("just over fifty-five percent"), color="#C8E6C9", size=28),
              it("sign", x=1300, y=480, text="COUNTING METHOD CHANGED IN 2026", at=C("One caution"), color="#FFCDD2", size=30),
              buddy(1750, 880, at=0.4, mood="happy", moods=[[C("One caution"), "worry"]], label="CLOUD", color="#7DFF8A", hop=18)]},
    sources=["tenq"])
stage("s28_payback", "m4_payback", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("For the price to work"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="2 · THE SPENDING PAYS BACK", at=0.2, size=54, color="gold"),
              it("sign", x=700, y=280, text="CAPEX = 89% OF OPERATING CASH", at=C("Capex is eating"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=280, text="'EXPECT TO SIGNIFICANTLY INCREASE'", at=C("expects to keep raising"), color="#FFE0B2", size=28),
              it("letters", x=1000, y=440, text="FREE CASH MUST CLIMB BACK · FOR YEARS", at=C("For the price to work"), size=44, color="gold")]},
    sources=["tenq", "rel"])
stage("s29_search", "m4_search", {
    "zones": [Z("infolibrary", signs=["SEARCH · STILL OPEN", "SHARE WITH RIVALS (COURT)", "AI ANSWERS · AISLE 1", "QUIET: INDEXING"], query="IS SEARCH CHANGING?")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("while a court order"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=520, text="3 · SEARCH HOLDS UP", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=660, text="≈ 53% OF REVENUE", at=C("of revenue"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=660, text="AI CHANGES HOW PEOPLE SEARCH", at=C("while A I changes"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=790, text="COURT ORDER: SHARE SOME SEARCH DATA WITH RIVALS", at=C("while a court order"), color="#FFCDD2", size=26),
              it("gavel", x=1850, y=760, hits=[C("forces Google")])]},
    sources=["rel", "tenq"])
stage("s30_funding", "m4_funding", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("To stop the dilution"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="4 · THE FUNDING GAP CLOSES", at=0.2, size=54, color="gold"),
              it("sign", x=700, y=280, text="2026: NEW SHARES + NEW DEBT", at=C("This year took"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=400, text="OPERATING CASH MUST CATCH UP WITH CAPEX", at=C("To stop the dilution"), color="#BBDEFB", size=26),
              it("letters", x=1100, y=560, text="BACK TO A SHRINKING SHARE COUNT?", at=C("shrinking its share count"), size=44, color="gold"),
              buddy(1800, 880, at=0.4, mood="worry", moods=[[C("shrinking its share count"), "happy"]], label="SHARES", color="#FF9F1C", hop=18)]},
    sources=["tenq"])
kinetic("s31_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s32_c5", "m5_card", "Risks and Upside", "What Alphabet itself warns about")
stage("s33_capexrisk", "m5_capex", {
    "zones": [Z("datacenter", darkAt=7.0)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("If demand falls short"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 1 · THE BUILD-OUT ITSELF", at=0.2, size=54, color="gold"),
              it("sign", x=1000, y=270, text="'MAY NOT RESULT IN AN ADEQUATE RETURN'", at=C("may not result"), color="#FFE0B2", size=26),
              it("sign", x=1000, y=390, text="COMMITMENTS $802.1BN · GUARANTEES · REPURCHASE PROMISES", at=C("of commitments"), color="#FFCDD2", size=24),
              it("sign", x=1000, y=510, text="DEMAND SHORT → IDLE CAPACITY", at=C("If demand falls short"), color="#FFCDD2", size=30),
              buddy(1800, 880, at=0.4, mood="worry", label="RACKS", color="#7B61FF", hop=10)]},
    sources=["tenq"])
stage("s34_legal", "m5_legal", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("In Europe"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 2 · THE COURTS", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=270, text="SEARCH JUDGMENT: DISTRIBUTION LIMITS", at=C("The search judgment"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=370, text="AD TECH: NO BREAKUP · OTHER REMEDIES", at=C("In ad tech"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=490, text="EU ANDROID FINE PAID: $5.2BN · SET ASIDE ≈ $13.8BN", at=C("In Europe"), color="#FFCDD2", size=26),
              it("gavel", x=1800, y=600, hits=[C("rejected a breakup"), C("set aside")])]},
    sources=["tenq"])
stage("s34b_fines", "m5_fines", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("A Swedish"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BILLS FROM EUROPE", at=0.2, size=60, color="gold"),
              it("sign", x=760, y=260, text="EU AD TECH: $3.5BN CHARGE", at=C("The European ad tech"), color="#FFCDD2", size=30),
              it("sign", x=1260, y=260, text="DMA: +$1.0BN (Q3)", at=C("digital markets"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=390, text="PRICERUNNER ≈ $2.1BN (APPEAL)", at=C("A Swedish"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=520, text="TEXAS AD TECH TRIAL: 'CANNOT ESTIMATE'", at=C("A Texas trial"), color="#F5F5F5", size=28),
              buddy(1700, 860, at=0.4, mood="worry", label="GOOG", color="#3DF5FF", hop=12)]},
    sources=["tenq"])
stage("s35_control", "m5_control", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And the filing now warns"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="RISK 3 · CONTROL AND DILUTION", at=0.2, size=54, color="gold"),
              it("sign", x=700, y=270, text="FOUNDERS' SHARES ≈ 53% OF VOTES", at=C("The founders' special shares"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=370, text="NEW SHARE SALES 'COULD ... DEPRESS OUR STOCK PRICE'", at=C("And the filing now warns"), color="#FFCDD2", size=24),
              it("sign", x=1000, y=490, text="PROFITS SWING WITH THE STAKES' VALUE", at=C("keep swinging"), color="#FFE0B2", size=28)]},
    sources=["tenq", "rel"])
stage("s36_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("Those are marks"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("BUILD-OUT · $802BN COMMITMENTS", 0.3), ("COURTS · FINES · REMEDIES", 0.9), ("CONTROL · DILUTION", 1.5)],
                    [("GEMINI APP: 1 BILLION USERS", C("the Gemini app")), ("TPU SYSTEMS: A NEW PRODUCT", C("T P U")), ("STAKES MARKED ≈ $203BN", C("its stakes"))],
                    title="RISKS VS UPSIDE (ALPHABET'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="MARKS, NOT CASH · UPSIDE NOT SIZED AS REVENUE", at=C("Those are marks"), color="#C8E6C9", size=28)]},
    sources=["rel", "tenq"])
kinetic("s37_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
board("p38_watch", "payoff", "3 numbers to watch (next report)", C("One, Google Cloud"), [
    {"d": rect(1320, 440, 250, 140), "color": "accent", "width": 6, "kind": "box", "start": C("One, Google Cloud"), "label": lbl("NEXT REPORT", 1445, 518, 22, "accent")},
    {"d": rect(700, 300, 440, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("One, Google Cloud"), "label": lbl("GOOGLE CLOUD", 920, 362, 20, "accent2")},
    {"d": "M 720 428 L 1120 428", "color": "ink", "width": 1, "start": C("One, Google Cloud", 0.3), "label": lbl("REVENUE + MARGIN (Q3: $30.7BN, 36%)", 920, 450, 14, "ink")},
    {"d": arrow((1150, 355), (1310, 462), 0.08), "color": "accent2", "width": 5, "kind": "arrow", "start": C("One, Google Cloud", 0.6)},
    {"d": rect(700, 470, 440, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("Two, capex"), "label": lbl("CAPEX AND FREE CASH", 920, 532, 20, "accent3")},
    {"d": "M 720 598 L 1120 598", "color": "ink", "width": 1, "start": C("Two, capex", 0.3), "label": lbl("VS Q3 FCF −$9.1BN · 2027 OUTLOOK", 920, 620, 14, "ink")},
    {"d": arrow((1150, 525), (1310, 505), 0.08), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Two, capex", 0.6)},
    {"d": rect(700, 640, 440, 110), "color": "risk", "width": 5, "kind": "box", "start": C("Three, Search"), "label": lbl("SEARCH + SHARE COUNT", 920, 702, 20, "risk")},
    {"d": "M 720 768 L 1120 768", "color": "ink", "width": 1, "start": C("Three, Search", 0.3), "label": lbl("SEARCH +12% · 12.29BN SHARES", 920, 790, 14, "ink")},
    {"d": arrow((1150, 695), (1310, 547), 0.08), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three, Search", 0.6)},
], C("Three, Search", 0.5), [1445, 510], sources=["rel", "tenq"])
stage("s39_edition", "payoff2", {
    "zones": [machine(SEGS, "THE ALPHABET MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [scorecard([("GOOGLE CLOUD", "REVENUE + MARGIN (Q3: $30.7BN, 36%)", 0.4),
                         ("CAPEX AND FREE CASH", "VS Q3 FCF −$9.1BN · 2027 OUTLOOK", 1.0),
                         ("SEARCH + SHARE COUNT", "SEARCH +12% · 12.29BN SHARES", 1.6)], x=960, y=230, at=0.2, scale=0.82),
              stamp(1560, 930, at=0.6, scale=0.7),
              it("sign", x=760, y=925, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=24)]},
    sources=["rel"])
add("s40_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_alphabet_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Alphabet (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
