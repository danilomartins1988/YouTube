"""Generates projects/before-you-buy-meta-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Meta, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit from
tools/byb_kit.py. Meta's own world: FEED CITY (new `feedcity` set: phone-shaped towers whose screens scroll generic feed
cards, ad cards slipping in, hearts / thumbs / chat bubbles floating up, an ad-auction ticker on the street). No real app
UI, logos or likenesses: shapes only; Mark Zuckerberg named in narration only, never drawn.
One visual language per part:
- Hook: feed city with a giant counter + edition stamp (cash below zero); data center + bank hall (capital raised).
- Part 1 (the machine): money machine (ads pipe dwarfs the rest); two engines in the money machine; feed city with ad
  cards (impressions x price); a box-and-arrow board.
- Part 2 (the cash): vault (OCF vs capex), court (Q3 charge), bank hall (buybacks stop, new capital), a bar board.
- Part 3 (what's priced in): priced-in calculator (three lenses; proxy gauge), data center (proxy), site (capex must earn),
  a bar board.
- Part 4 (what has to happen): feed city (ads), site (capex), exchange (margin), studio (Reality Labs).
- Part 5 (risks and upside): court, parliament, secret room (control), risk scale.
- Payoff: scorecard with the edition stamp; feed city sign-off.
Rules: no logos, generic shapes only, no real people drawn; numbers match sources.yaml; our calculations labelled;
NM accrual never described; forward-sale proceeds not yet received.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run. Note the Class C dividend
(Jan 19, 2027): the next edition sums Classes A + B + C.
Run: python tools/gen_byb_meta_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-meta-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q3 2026 (SEP 30, 2026)")
SEGS = [("ADVERTISING $235.6BN", 235.6, "#FF4FD8", None), ("OTHER (MESSAGING, SUBS) $3.8BN", 3.8, "#3DF5FF", None),
        ("REALITY LABS $2.2BN", 2.2, "#FFE14D", None)]
JOKES = ["ADS IN · CASH OUT", "SCROLL ZONE · NO BRAKES", "IMPRESSIONS: COUNTED", "LIKES NOT ACCEPTED AS PAYMENT"]
ADS = ["YOUR AD HERE · $", "SCROLL RESPONSIBLY", "NOW SHOWING: YOU", "LIKES REDEEMABLE NEVER"]

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("studio", night=True, x1=1080), Z("feedcity", ads=ADS, adAt=0.5, x0=1080)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=660, y=230, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "Meta is worth"}, 1.64]], text="META MARKET VALUE (OUR CALC.)", scale=1.15),
              it("sign", x=660, y=410, text="$641.39 × 2.56BN SHARES (A+B)", at=C("a share at the close"), color="#BBDEFB", size=28),
              it("letters", x=640, y=560, text="Q3 FREE CASH: −$2.1BN", at=C("for the first time"), size=50, color="gold"),
              stamp(700, 720, at=C("a share at the close"), scale=0.6),
              buddy(300, 860, at=0.5, mood="happy", moods=[[C("for the first time"), "shock"]], label="META", color="#FF4FD8", hop=30)]},
    sources=["px", "tenq", "rel"])
stage("s02_twist", "h_twist", {
    "zones": [Z("datacenter", x1=1500), Z("bankhall", x0=1500)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.05}, {"at": C("And instead of buying back"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.2}], "drift": 2,
    "items": [it("letters", x=800, y=130, text="ADS +26% · NOT SHRINKING", at=C("Ad revenue grew"), size=52, color="gold"),
              it("sign", x=800, y=300, text="≈ 45% OF SALES → DATA CENTERS", at=C("of everything it sells"), color="#FFE0B2", size=30),
              it("isodc", x=800, y=760, at=0.4, n=6, step=0.25, cols=3, scale=0.55, glow=True),
              it("counter", x=2200, y=200, at=C("And instead of buying back"), prefix="≈ $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "of new money"}, 56]], text="NEW CAPITAL LINED UP IN 2 WEEKS (OUR SUM)"),
              it("sign", x=2200, y=380, text="BUYBACKS IN 2026: $0", at=C("instead of buying back"), color="#FFCDD2", size=30),
              buddy(2600, 860, at=C("And instead of buying back"), mood="shock", label="META", color="#FF4FD8", hop=24)]},
    sources=["rel", "tenq", "cap8k"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=320, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=320, text="WHAT COULD BREAK IT?", at=C("what could"), color="#FFCDD2", size=34),
              buddy(1000, 860, at=0.4, mood="worry", label="META", color="#FF4FD8", hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: META", at=0.4, size=64, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="META'S", sources=["tenq"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Almost all of it is ads")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("came from advertising")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("Substantially all")),
                       (SEGS[2][0], SEGS[2][1], SEGS[2][2], C("Substantially all"))], "THE META MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("And those marketers"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "brought in"}, 241.6]], text="REVENUE, LAST 12 MONTHS (OUR CALC.)", scale=1.0),
              it("sign", x=650, y=860, text="ADS: 97.5% OF EVERYTHING", at=C("came from advertising"), color="#FFE0B2", size=30),
              it("sign", x=560, y=960, text="NO LONG-TERM AD CONTRACTS", at=C("And those marketers"), color="#FFCDD2", size=28)]},
    sources=["rel", "tenq"])
stage("s08_engines", "m1_engines", {
    "zones": [Z("feedcity", ads=ADS, x1=1700), Z("studio", night=True, x0=1700)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Reality Labs"), "x": 2400, "y": 520, "zoom": 1.0, "dur": 2.2}, {"at": C("One engine pays"), "x": 1600, "y": 520, "zoom": 0.85, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=800, y=120, text="FAMILY OF APPS · ≈ 52% MARGIN (2025)", at=C("The Family of Apps"), size=46, color="gold"),
              it("letters", x=2400, y=120, text="REALITY LABS · −$19.2BN (2025)", at=C("Reality Labs"), size=46, color="gold"),
              it("device", x=2250, y=860, type="phone", at=C("the headsets and glasses"), scale=1.1),
              buddy(2600, 860, at=C("Reality Labs"), mood="sad", label="RL", color="#FFE14D", hop=8),
              buddy(1100, 860, at=0.4, mood="happy", moods=[[C("One engine pays"), "cool"]], label="APPS", color="#FF4FD8", hop=26),
              coins(1150, 700, [2500, 760], at=C("One engine pays"), rate=5)]},
    sources=["rel"])
stage("s09_ads", "m1_ads", {
    "zones": [Z("feedcity", ads=["AD SLOTS · LIVE AUCTION", "MORE ADS · HIGHER PRICES", "TARGETING DEPT.", "MEASURED TWICE · SOLD ONCE"], adAt=0.3)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("More ads, at higher prices"), "x": 1150, "y": 500, "zoom": 1.0, "dur": 2.0}], "drift": 3,
    "items": [it("sign", x=650, y=200, text="IMPRESSIONS +10%", at=C("more ads"), color="#BBDEFB", size=34),
              it("sign", x=1350, y=200, text="PRICE PER AD +14%", at=C("more per ad"), color="#FFE0B2", size=34),
              it("counter", x=1000, y=360, at=0.2, prefix="", suffix="BN PEOPLE / DAY", decimals=2, steps=[[0, 0], [{"cue": "people use at least one"}, 3.64]], text="DAILY ACTIVE PEOPLE (Q3)"),
              it("letters", x=1000, y=540, text="MORE ADS × HIGHER PRICES", at=C("More ads, at higher prices"), size=50, color="gold")]},
    sources=["rel", "tenq"])
stage("s09b_geo", "m1_geo", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And the machine"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="WHERE THE AD MONEY COMES FROM", at=0.2, size=52, color="gold"),
              it("sign", x=720, y=250, text="U.S. & CANADA 39%", at=C("The United States"), color="#BBDEFB", size=30),
              it("sign", x=880, y=330, text="EUROPE 23%", at=C("Europe,"), color="#C8E6C9", size=30),
              it("sign", x=1200, y=250, text="ASIA-PACIFIC 27%", at=C("Asia Pacific"), color="#FFE0B2", size=30),
              it("sign", x=1320, y=330, text="REST OF WORLD 11%", at=C("The rest of the world"), color="#F5F5F5", size=30),
              it("sign", x=1000, y=480, text="HEADCOUNT 66,775 (−15%)", at=C("Meta's headcount"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=590, text="89% OF COSTS: THE APPS", at=C("Almost all the spending"), color="#FFF8E1", size=28),
              buddy(1700, 860, at=0.3, mood="happy", label="META", color="#FF4FD8", hop=14)]},
    sources=["tenq", "rel"])
board("p10_machine", "m1_draw", "The machine (segments, FY2025)", C("Here is the Family of Apps"), [
    {"d": rect(1080, 420, 360, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the Family of Apps"), "label": lbl("FAMILY OF APPS · +$102.5BN", 1260, 528, 20, "accent2")},
    {"d": rect(1080, 700, 360, 120), "color": "risk", "width": 6, "kind": "box", "start": C("Here is Reality Labs"), "label": lbl("REALITY LABS · −$19.2BN", 1260, 768, 20, "risk")},
    {"d": rect(640, 450, 260, 140), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is"), "label": lbl("ADS $196.2BN", 770, 528, 20, "accent3")},
    {"d": arrow((905, 520), (1075, 520)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("feeding the big engine"), "label": lbl("97%+", 990, 500, 18, "accent3")},
    {"d": arrow((1260, 625), (1260, 695), 0.0), "color": "accent", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("CASH", 1330, 665, 20, "accent")},
], C("running", 0.1), [1260, 660], sources=["rel"])
kinetic("s11_t1", "m1_transition", [("An ad machine that good…", 70, "An ad machine that good", None, False),
                                    ("…so where did the cash go?", 72, "So where did it go", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Where twelve months of cash went")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Free cash flow"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Operating cash flow"}, 133.1]], text="OPERATING CASH FLOW, 12 MONTHS"),
              it("sign", x=1350, y=280, text="NET INCOME $75.2BN (ONE-OFFS INSIDE)", at=C("Net income was"), color="#C8E6C9", size=26),
              it("sign", x=1350, y=400, text="CAPEX INCL. LEASES −$108.0BN", at=C("Then capex"), color="#FFCDD2", size=30),
              it("letters", x=1100, y=540, text="FREE CASH ≈ $25BN (META'S DEFINITION)", at=C("Free cash flow"), size=44, color="gold"),
              coins(400, 700, [1600, 760], at=0.4, rate=6, until=C("Then capex")),
              coins(1600, 700, [2200, 900], at=C("Then capex"), rate=7)]},
    sources=["tenq", "rel"])
stage("s14_quarter", "m2_quarter", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Without it"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE QUARTER WENT BELOW ZERO", at=0.2, size=54, color="gold"),
              it("sign", x=700, y=240, text="Q3 CHARGE: $9.89BN (STATE AGs SETTLEMENT)", at=C("charge for the settlement"), color="#FFE0B2", size=26),
              it("calendar", x=700, y=470, at=C("Including it"), pages=[[0, "Q3 REPORTED", "26.7%"], [C("Without it"), "Q3 EX-CHARGE", "≈ 42%"]]),
              it("sign", x=1450, y=380, text="FAMILY OF APPS MARGIN (OUR CALC.)", at=C("Including it"), color="#BBDEFB", size=28),
              it("gavel", x=1650, y=560, hits=[C("charge for the settlement")])]},
    sources=["rel", "tenq"])
stage("s15_capital", "m2_capital", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The share count is now"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("calendar", x=600, y=280, at=0.3, pages=[[0, "2025", "BUYBACKS $26.25BN"], [C("This"), "2026", "BUYBACKS $0"]]),
              it("sign", x=1350, y=200, text="$12.5BN CONVERTIBLE PREFERRED", at=C("of convertible preferred"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=320, text="≈ $28.7BN FORWARD SALE (NOT YET RECEIVED)", at=C("a forward sale"), color="#FFE0B2", size=26),
              it("sign", x=1350, y=440, text="$15.0BN OF BONDS", at=C("of bonds"), color="#FFE0B2", size=28),
              it("letters", x=1100, y=600, text="SHARE COUNT: RISING, NOT FALLING", at=C("The share count is now"), size=44, color="gold")]},
    sources=["cap8k", "tenq"])
stage("s15b_commit", "m2_commit", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("At the end of September"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE BILLS ARE ALREADY SIGNED", at=0.2, size=54, color="gold"),
              it("counter", x=800, y=270, at=C("Meta lists"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "non cancelable"}, 454.5]], text="COMMITMENTS (10-Q)"),
              it("sign", x=1280, y=230, text="DUE 2026: $45.9BN", at=C("due this year"), color="#FFE0B2", size=30),
              it("sign", x=1280, y=330, text="DUE 2027: $121.4BN", at=C("next year"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=500, text="CASH $82.4BN  ·  DEBT $84.0BN", at=C("At the end of September"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=610, text="SHARES +1% IN 9 MONTHS", at=C("the share count rose"), color="#F5F5F5", size=28),
              buddy(1700, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["tenq"])
board("p16_cash", "m2_draw", "Twelve months of cash (our calc.)", C("Here is the operating cash bar"), [
    {"d": "M 700 780 L 1560 780", "color": "ink", "width": 4, "start": C("Here is the operating cash bar"), "label": lbl("$BN · TTM · OUR CALC.", 1130, 830, 18, "ink")},
    bar(740, 150, 780, 380, "accent2", C("Here is the operating cash bar"), "OCF 133"),
    bar(940, 150, 780, 455, "risk", C("Here is the capex bar"), "CAPEX 108"),
    bar(1140, 150, 780, 704, "accent3", C("Here is what's left"), "FCF 25"),
    bar(1340, 150, 780, 612, "accent", C("And here is the new money"), "NEW CAPITAL ≈ 56"),
], C("more than"), [1415, 600], sources=["tenq", "cap8k"])
kinetic("s17_t2", "m2_transition", [("At one point six trillion…", 70, "At one point six trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s18_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s19_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("That gap is"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (TTM, OUR CALC.)", note="THE GAP = THE CAPEX",
                    base="TO BE CHOSEN: CAPEX IS BOOMING",
                    lenses=[("P/E (ONE-OFFS INSIDE)", "21.8×", C("Price to earnings")), ("FCF YIELD", "1.5%", C("Free cash flow")), ("OCF YIELD", "8.1%", C("Operating cash flow"))]),
              stamp(1500, 900, at=0.4, scale=0.7)]},
    sources=["tenq", "px"])
stage("s20_proxy", "m3_proxy", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It assumes capex"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="A PROXY FOR A BUILDING SPREE", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=260, text="OCF $133.1BN", at=C("We take operating cash"), color="#BBDEFB", size=32),
              it("sign", x=1100, y=260, text="− D&A ≈ $24.9BN", at=C("subtract depreciation"), color="#FFCDD2", size=32),
              it("letters", x=1000, y=420, text="= ≈ $108.2BN · YIELD ≈ 6.6%", at=C("That leaves"), size=50, color="gold"),
              it("sign", x=1300, y=560, text="ASSUMES CAPEX FALLS BACK TOWARD D&A", at=C("It assumes capex"), color="#FFE0B2", size=26),
              buddy(1750, 860, at=0.4, mood="cool", label="PROXY", color="#FFE14D", hop=16)]},
    sources=["tenq", "px"])
stage("s21_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 0.0, C("With an eight percent"), "≈ 0% / YR"), ("AT 10%", 3.4, C("With ten percent"), "≈ 3.4% / YR"),
                    ["MARKET CAP $1.64TN (NOV 10)", "PROXY: OCF − D&A $108.2BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED GROWTH, 10 YEARS", base="PROXY (CAPEX BOOM)", placardX=860, placardY=-200),
              it("sign", x=1500, y=880, text="ON TODAY'S FCF: ≈ 18-23% / YR", at=C("But on"), color="#FFCDD2", size=30),
              stamp(1150, 960, at=0.6, scale=0.55),
              buddy(1750, 640, at=0.5, mood="happy", moods=[[C("the answer jumps"), "shock"]], label="META", color="#FF4FD8", hop=22, scale=0.8)]},
    sources=["tenq", "px"])
stage("s22_mustearn", "m3_mustearn", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("every dollar"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 3,
    "items": [it("letters", x=1000, y=130, text="WHAT THE CAPEX MUST EARN", at=0.2, size=58, color="gold"),
              it("sign", x=1000, y=270, text="IF CAPEX STAYS ≈ $108BN A YEAR…", at=C("keeps spending"), color="#BBDEFB", size=30),
              it("letters", x=1000, y=420, text="EACH $1 → +9.5¢ TO +16¢ OF YEARLY CASH", at=C("every dollar"), size=46, color="gold"),
              it("sign", x=1000, y=540, text="LESS THAN MICROSOFT'S 18-32¢ · BUT META'S CAPEX IS STILL CLIMBING", at=C("Less than Microsoft"), color="#FFE0B2", size=24),
              coins(500, 860, [1500, 640], at=C("every dollar"), rate=5)]},
    sources=["tenq", "px"])
board("p23_two", "m3_draw", "Two answers, one price (our illustration)", C("Here is the growth the price needs"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is the growth the price needs"), "label": lbl("% A YEAR · 10 YEARS · OUR CALC.", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 768, "accent3", C("Here is the growth the price needs"), "PROXY @8% ≈ 0"),
    bar(1010, 170, 780, 720, "accent2", C("Here it is at the higher rate"), "PROXY @10% 3.4"),
    bar(1240, 170, 780, 337, "risk", C("And here is what it needs"), "FCF 18-23"),
    {"d": arrow((1180, 650), (1235, 360), 0.1), "color": "accent", "width": 5, "kind": "arrow", "start": C("The difference"), "label": lbl("THE CAPEX", 1130, 500, 18, "accent")},
], C("the capex", 0.1), [1320, 420], sources=["tenq", "px"])
kinetic("s24_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s25_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s26_ads", "m4_ads", {
    "zones": [Z("feedcity", ads=["MORE ADS · HIGHER PRICES", "GUIDE: $73-76BN", "AI INSIDE · ADS OUTSIDE", "SCROLL ZONE"], adAt=0.2)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("That's the engine"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="1 · ADS KEEP COMPOUNDING", at=0.2, size=54, color="gold"),
              it("sign", x=750, y=240, text="PRICE/AD +14% · IMPRESSIONS +10%", at=C("Price per ad"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=360, text="Q4 GUIDE: $73-76BN (CFO)", at=C("guided revenue"), color="#FFE0B2", size=30),
              buddy(1700, 860, at=0.4, mood="happy", label="ADS", color="#FF4FD8", hop=26)]},
    sources=["rel"])
stage("s27_capex", "m4_capex", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And it has"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="2 · CAPEX TURNS BACK INTO CASH", at=0.2, size=52, color="gold"),
              it("sign", x=700, y=240, text="2026 CAPEX GUIDE $135-145BN", at=C("Meta guides"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=240, text="IMPLIED Q4 ≈ $49-59BN (VS $34.9BN IN Q3)", at=C("that implies"), color="#FFCDD2", size=26),
              it("counter", x=1000, y=420, at=C("And it has"), prefix="$", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "of future commitments"}, 454]], text="FUTURE COMMITMENTS (10-Q)"),
              it("sign", x=1000, y=580, text="≈ $121BN DUE IN 2027", at=C("due next year"), color="#FFE0B2", size=30)]},
    sources=["rel", "tenq"])
stage("s28_margin", "m4_margin", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Depreciation from"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="3 · THE CORE MARGIN HOLDS", at=0.2, size=56, color="gold"),
              it("calendar", x=650, y=290, at=C("It was"), pages=[[0, "2025", "≈ 52%"], [C("last quarter"), "Q3 EX-CHARGE", "≈ 42%"]]),
              it("sign", x=1400, y=320, text="DEPRECIATION: $7.15BN VS $4.96BN A YEAR AGO", at=C("Depreciation from"), color="#FFCDD2", size=26),
              buddy(1700, 860, at=0.4, mood="worry", label="APPS", color="#FF4FD8", hop=12)]},
    sources=["rel", "tenq"])
stage("s29_rl", "m4_rl", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Every billion"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=960, y=120, text="4 · REALITY LABS LOSES LESS", at=0.2, size=56, color="gold"),
              it("calendar", x=600, y=330, at=C("The C F O expects"), pages=[[0, "2025", "−$19.2BN"], [C("this year"), "2026 GUIDE", "−$18-19BN"], [C("next year"), "2027 OUTLOOK", "≈ −$15BN"]]),
              it("sign", x=1300, y=380, text="EVERY $1BN SAVED → $1BN FOR AI", at=C("Every billion"), color="#C8E6C9", size=30),
              buddy(1500, 860, at=0.4, mood="sad", moods=[[C("Every billion"), "happy"]], label="RL", color="#FFE14D", hop=14)]},
    sources=["rel"])
kinetic("s30_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s31_c5", "m5_card", "Risks and Upside", "What Meta itself warns about")
stage("s32_courts", "m5_courts", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The settlement with"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 1 · THE COURTS", at=0.2, size=58, color="gold"),
              it("counter", x=750, y=250, at=C("A New Mexico court"), prefix="$", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "imposed a civil penalty"}, 25]], text="NEW MEXICO PENALTY (+15% INTEREST)"),
              it("sign", x=750, y=420, text="ACCRUED AMOUNT: NOT DISCLOSED · APPEAL", at=C("doesn't say how much"), color="#FFE0B2", size=26),
              it("sign", x=1400, y=300, text="AGs SETTLEMENT: UP TO ≈ $18.6BN", at=C("The settlement with"), color="#FFCDD2", size=28),
              it("sign", x=1400, y=440, text="LEGAL ACCRUALS ≈ $19.9BN", at=C("Legal accruals"), color="#FFCDD2", size=28),
              it("gavel", x=1750, y=600, hits=[C("imposed a civil penalty"), C("will appeal")])]},
    sources=["tenq"])
stage("s32b_youth", "m5_youth", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Lawyers for"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="NOT OVER YET", at=0.2, size=60, color="gold"),
              it("sign", x=740, y=250, text="$12.7BN OVER 10 YEARS", at=C("paid over ten years"), color="#FFE0B2", size=30),
              it("sign", x=1260, y=250, text="+$5.3BN IF RIVALS FOLLOW", at=C("only comes due"), color="#FFE0B2", size=28),
              it("sign", x=740, y=380, text="200,000+ ARBITRATION CLAIMANTS", at=C("Lawyers for"), color="#FFCDD2", size=28),
              it("sign", x=1260, y=380, text="NEXT TRIAL: FEB 2027", at=C("school district trial"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=510, text="DC: UP TO $1.7BN", at=C("District of Columbia"), color="#FFCDD2", size=30),
              it("sign", x=1000, y=630, text="'$1 TRILLION+' = PLAINTIFFS' CLAIM", at=C("Plaintiffs have claimed"), color="#F5F5F5", size=26),
              buddy(1700, 860, at=0.4, mood="worry", label="META", color="#FF4FD8", hop=12)]},
    sources=["tenq"])
stage("s33_europe", "m5_europe", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("and warns"), "x": 1200, "y": 500, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 2 · EUROPE (≈ 23% OF REVENUE)", at=0.2, size=50, color="gold"),
              it("sign", x=700, y=250, text="PAY-OR-CONSENT FINE: UNDER APPEAL", at=C("Meta is appealing"), color="#FFE0B2", size=28),
              it("sign", x=1300, y=370, text="MORE CHANGES COULD BE IMPOSED", at=C("and warns"), color="#FFCDD2", size=30)]},
    sources=["tenq"])
stage("s34_control", "m5_other", {
    "zones": [Z("secretroom")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It depends on"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 3 · THE SPENDING, AND CONTROL", at=0.2, size=50, color="gold"),
              it("sign", x=1000, y=240, text="'IF OUR INVESTMENTS ARE NOT SUCCESSFUL LONGER-TERM'", at=C("Meta's filing says"), color="#FFE0B2", size=24),
              it("sign", x=1000, y=360, text="SENTIMENT TOWARD DATA CENTERS IS SHIFTING", at=C("shifting public sentiment"), color="#FFCDD2", size=26),
              it("sign", x=1000, y=480, text="KEY PERSON · NEW NON-VOTING SHARES EXTEND CONTROL", at=C("It depends on"), color="#BBDEFB", size=24),
              it("emptychair", x=1600, y=860, at=C("It depends on"), scale=0.8)]},
    sources=["tenq"])
stage("s35_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("None of that"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("NM $25BN · AGs · LEGAL ACCRUALS", 0.3), ("EUROPE · AD-MODEL CHANGES", 0.9), ("CAPEX BET · KEY PERSON", 1.5)],
                    [("WHATSAPP PAID MESSAGING +59%", C("WhatsApp paid messaging")), ("MUSE: AGENTIC AI", C("Meta has launched Muse")), ("AI GLASSES", C("glasses are selling"))],
                    title="RISKS VS UPSIDE (META'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="UPSIDE IS UNSIZED: NO FORECAST GIVEN", at=C("None of that"), color="#C8E6C9", size=28)]},
    sources=["tenq"])
kinetic("s36_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
board("p37_watch", "payoff", "3 numbers to watch (next report)", C("One, fourth"), [
    {"d": rect(1320, 440, 250, 140), "color": "accent", "width": 6, "kind": "box", "start": C("One, fourth"), "label": lbl("NEXT REPORT", 1445, 518, 22, "accent")},
    {"d": "M 1360 640 L 1640 640", "color": "risk", "width": 2, "start": C("And one note"), "label": lbl("NEXT EDITION: SHARES ≈ 2× (CLASS C)", 1500, 670, 15, "risk")},
    {"d": rect(700, 300, 440, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("One, fourth"), "label": lbl("Q4 REVENUE", 920, 362, 20, "accent2")},
    {"d": "M 720 428 L 1120 428", "color": "ink", "width": 1, "start": C("One, fourth", 0.3), "label": lbl("VS THE $73-76BN GUIDE", 920, 450, 14, "ink")},
    {"d": arrow((1150, 355), (1310, 462), 0.08), "color": "accent2", "width": 5, "kind": "arrow", "start": C("One, fourth", 0.6)},
    {"d": rect(700, 470, 440, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("Two, capex"), "label": lbl("CAPEX + 2027 OUTLOOK", 920, 532, 20, "accent3")},
    {"d": "M 720 598 L 1120 598", "color": "ink", "width": 1, "start": C("Two, capex", 0.3), "label": lbl("FREE CASH BACK ABOVE ZERO? (Q3: −$2.1BN)", 920, 620, 14, "ink")},
    {"d": arrow((1150, 525), (1310, 505), 0.08), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Two, capex", 0.6)},
    {"d": rect(700, 640, 440, 110), "color": "risk", "width": 5, "kind": "box", "start": C("Three, legal"), "label": lbl("LEGAL ACCRUALS + CORE MARGIN", 920, 702, 20, "risk")},
    {"d": "M 720 768 L 1120 768", "color": "ink", "width": 1, "start": C("Three, legal", 0.3), "label": lbl("VS $19.9BN · VS ≈ 42% EX-CHARGE", 920, 790, 14, "ink")},
    {"d": arrow((1150, 695), (1310, 547), 0.08), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three, legal", 0.6)},
], C("Three, legal", 0.5), [1445, 510], sources=["rel", "tenq", "cap8k"])
stage("s38_edition", "payoff2", {
    "zones": [machine(SEGS, "THE META MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [scorecard([("Q4 REVENUE", "VS THE $73-76BN GUIDE", 0.4),
                         ("CAPEX + 2027 OUTLOOK", "FREE CASH BACK ABOVE ZERO? (Q3: −$2.1BN)", 1.0),
                         ("LEGAL ACCRUALS + CORE MARGIN", "VS $19.9BN · VS ≈ 42% EX-CHARGE", 1.6)], x=960, y=230, at=0.2, scale=0.82),
              stamp(1560, 930, at=0.6, scale=0.7),
              it("sign", x=760, y=925, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=24)]},
    sources=["rel"])
add("s39_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_meta_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Meta (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
