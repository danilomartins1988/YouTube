"""Generates projects/before-you-buy-microsoft-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Microsoft, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit from
tools/byb_kit.py. Microsoft's own world: the CLOUD PORT (new `cloudport` set: data-center towers on stilts, cloud-blimp
server pods docking, spinning fans), plus the data center, the money machine (two engines + Azure), the vault and the court.
One visual language per part:
- Hook: cloud port with a giant counter + edition stamp; the money machine; the disclaimer.
- Part 1 (the machine): money machine with the two recast engines; Azure in the cloud port; OpenAI as one big blimp; a
  box-and-arrow board.
- Part 2 (the cash): vault (OCF vs capex), data center building out, construction site (leases not yet started), bank
  hall (buybacks + dividends), a bar board.
- Part 3 (what's priced in): the priced-in calculator (three lenses; proxy base gauge), the cloud port (capex must earn),
  a bar board (proxy vs FCF answers).
- Part 4 (what has to happen): busy cloud port, office (backlog), site, exchange.
- Part 5 (risks and upside): data center going dark, port of partners, court, risk scale.
- Payoff: scorecard with the edition stamp.
Rules: no logos, generic shapes only, no real people drawn; numbers match sources.yaml; our calculations labelled.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_microsoft_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-microsoft-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 10, 2026 CLOSE", "LATEST REPORT: Q1 FY2027 (SEP 30, 2026)")
SEGS = [("AGENTS & INFRA $268.1BN", 268.1, "#3DF5FF", None), ("DEVICES & CONSUMER $63.7BN", 63.7, "#FF9F1C", None)]
JOKES = ["CAPACITY: PLEASE HOLD", "AZURE LANE · NO IDLING", "CAPEX ZONE · HARD HATS", "CLOUDS PARKED AT OWNER'S RISK"]
PORT = ["NOW DOCKING: MORE GPUS", "DEMAND > SUPPLY", "NO EMPTY RACKS", "CLOUD PARKING · 1 HR"]

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("cloudport", signs=PORT)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=700, y=210, at=0.05, prefix="≈ $", suffix="TN", decimals=2, steps=[[0.05, 0], [{"cue": "Microsoft is worth"}, 3.96]], text="MICROSOFT MARKET VALUE (OUR CALC.)", scale=1.3),
              it("sign", x=700, y=410, text="$533.16 × 7.43BN SHARES", at=C("a share at the close"), color="#BBDEFB", size=32),
              it("letters", x=1050, y=620, text="≈ 66× LAST 12 MONTHS' FREE CASH", at=C("by our math"), size=50, color="gold"),
              stamp(1480, 450, at=C("a share at the close"), scale=0.75),
              buddy(480, 860, at=0.5, mood="happy", moods=[[C("by our math"), "shock"]], label="MSFT", color="#3A86FF", hop=30)]},
    sources=["px", "tenq"])
stage("s02_twist", "h_twist", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("The cash is"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=180, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "on property and equipment"}, 135.9]], text="CAPEX, LAST 12 MONTHS (OUR CALC.)"),
              it("sign", x=1350, y=320, text="= 39% OF EVERYTHING IT SOLD", at=C("of everything it sold"), color="#FFE0B2", size=30),
              it("letters", x=1100, y=470, text="CONCRETE · CHIPS · COOLING", at=C("poured back"), size=50, color="gold"),
              it("isodc", x=1400, y=760, at=C("The cash is"), n=6, step=0.25, cols=3, scale=0.55, glow=True),
              buddy(450, 860, at=0.4, mood="worry", label="FCF", color="#7DFF8A", hop=14)]},
    sources=["tenq"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="WHAT IS THE PRICE BETTING ON?", at=0.3, size=58, color="gold"),
              it("sign", x=650, y=320, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=320, text="WHAT COULD BREAK IT?", at=C("what could"), color="#FFCDD2", size=34),
              buddy(1000, 860, at=0.4, mood="worry", label="MSFT", color="#3A86FF", hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: MICROSOFT", at=0.4, size=60, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="MICROSOFT'S", sources=["tenq"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Two engines, one cloud")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("Agents and Infra")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("Devices and Consumer"))],
                      "THE MICROSOFT MACHINE", "PROFIT", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("Devices and Consumer"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=1500, y=830, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "brought in"}, 331.8]], text="FY2026 REVENUE (RECAST 8-K)", scale=1.0),
              it("sign", x=560, y=960, text="+18% · TWO ENGINES NOW", at=C("two"), color="#C8E6C9", size=30),
              it("sign", x=650, y=860, text="AGENTS & INFRA: ≈ 51% MARGIN", at=C("operating"), color="#BBDEFB", size=30)]},
    sources=["rel"])
stage("s08_azure", "m1_azure", {
    "zones": [Z("cloudport", signs=PORT, busyAt=3.0)], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("Meanwhile"), "x": 1350, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=170, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "in the September quarter"}, 33.2]], text="AZURE, SEP QUARTER (+48%)"),
              it("sign", x=800, y=350, text="≈ 36% OF ALL REVENUE", at=C("of all of"), color="#BBDEFB", size=30),
              it("sign", x=1500, y=280, text="OFFICE CLOUD +17%", at=C("The Office cloud"), color="#C8E6C9", size=30),
              it("sign", x=1500, y=420, text="WINDOWS WITH NEW PCs −22%", at=C("Meanwhile"), color="#FFCDD2", size=30),
              it("device", x=1800, y=860, type="laptop", at=C("Meanwhile"), scale=1.0, redAt=C("fell")),
              buddy(450, 860, at=0.4, mood="happy", label="AZURE", color="#3DF5FF", hop=28)]},
    sources=["rel", "tenq"])
stage("s09_openai", "m1_openai", {
    "zones": [Z("cloudport", signs=["ONE VERY LARGE CUSTOMER", "PARTNER · OWNER · BUYER", "DOCK 1 RESERVED", "CAPACITY · PLEASE WAIT"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("So OpenAI is"), "x": 1150, "y": 500, "zoom": 1.08, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=750, y=170, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "of revenue from its arrangements"}, 10.0]], text="OPENAI REVENUE, ONE QUARTER (10-Q)"),
              it("sign", x=750, y=350, text="≈ 11% OF THE QUARTER", at=C("of the total"), color="#FFE0B2", size=32),
              it("sign", x=1450, y=300, text="STAKE ≈ 24% (AS CONVERTED)", at=C("on an as converted"), color="#BBDEFB", size=30),
              it("letters", x=1150, y=480, text="PARTNER · SHAREHOLDING · BUYER", at=C("So OpenAI is"), size=46, color="gold"),
              buddy(1700, 860, at=0.5, mood="shock", moods=[[C("all at once"), "cool"]], label="OPENAI", color="#7B61FF", hop=22, scale=1.25)]},
    sources=["tenq"])
stage("s09b_lines", "m1_lines", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("But the older businesses"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="DIFFERENT SPEEDS", at=0.2, size=60, color="gold"),
              it("sign", x=740, y=250, text="M365 CLOUD +17%", at=C("the cloud Office"), color="#C8E6C9", size=32),
              it("sign", x=1000, y=250, text="SEARCH & ADS +10%", at=C("Search and advertising"), color="#C8E6C9", size=32),
              it("sign", x=740, y=380, text="WINDOWS OEM −22%", at=C("Windows sales"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=380, text="XBOX −2%", at=C("Xbox slipped"), color="#FFCDD2", size=32),
              it("sign", x=1280, y=380, text="LICENSES −3%", at=C("classic software"), color="#FFCDD2", size=32),
              it("sign", x=1000, y=520, text="CLOUD ENGINE MARGIN ≈ 53%", at=C("So the cloud engine"), color="#BBDEFB", size=30),
              buddy(1700, 860, at=0.3, mood="happy", label="AZURE", hop=14)]},
    sources=["tenq"])
board("p10_machine", "m1_draw", "The machine (recast segments, Q1 FY27)", C("Here is Agents and Infra"), [
    {"d": rect(1080, 420, 360, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is Agents and Infra"), "label": lbl("AGENTS & INFRA · 52.8%", 1260, 528, 20, "accent2")},
    {"d": rect(1080, 700, 360, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Here is Devices and Consumer"), "label": lbl("DEVICES & CONSUMER", 1260, 768, 20, "accent")},
    {"d": rect(640, 450, 260, 140), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is Azure"), "label": lbl("AZURE $33.2BN", 770, 528, 20, "accent3")},
    {"d": arrow((905, 520), (1075, 520)), "color": "accent3", "width": 6, "kind": "arrow", "start": C("Here is Azure"), "label": lbl("+48%", 990, 500, 18, "accent3")},
    {"d": arrow((770, 760), (770, 600), 0.15), "color": "risk", "width": 8, "kind": "arrow", "start": C("this arrow"), "label": lbl("OPENAI ≈ 11%", 770, 800, 20, "risk")},
], C("through it", 0.1), [770, 680], sources=["tenq", "rel"])
kinetic("s11_t1", "m1_transition", [("An engine that big…", 70, "An engine that big", None, False),
                                    ("…why is free cash so small?", 70, "why is free cash flow so small", "gold", False)])

# ====================================================================== PART 2: the cash
card("s12_c2", "m2_card", "The Cash", "Where twelve months of cash went")
stage("s13_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("What was left"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Operating cash flow"}, 195.9]], text="OPERATING CASH FLOW, 12 MONTHS"),
              it("sign", x=1400, y=280, text="CAPEX −$135.9BN", at=C("But capex took"), color="#FFCDD2", size=32),
              it("letters", x=1100, y=430, text="FREE CASH ≈ $60BN (OUR CALC.)", at=C("What was left"), size=50, color="gold"),
              it("sign", x=1100, y=560, text="NET INCOME $142.6BN", at=C("Net income was"), color="#C8E6C9", size=28),
              coins(400, 700, [1600, 760], at=0.4, rate=6, until=C("But capex took")),
              coins(1600, 700, [2200, 900], at=C("But capex took"), rate=7)]},
    sources=["tenq"])
stage("s14_quarter", "m2_quarter", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Total capex"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("calendar", x=650, y=300, at=0.2, pages=[[0, "Q1 FY26", "FCF $25.7BN"], [C("A year earlier"), "Q1 FY27", "FCF $18.6BN"]]),
              it("sign", x=1350, y=220, text="FCF −27% (OUR CALC.)", at=C("down"), color="#FFCDD2", size=32),
              it("sign", x=1350, y=360, text="CAPEX $45.2BN INCL. LEASES · $39.4BN CASH", at=C("Total capex"), color="#FFE0B2", size=26),
              it("isodc", x=1400, y=780, at=C("Total capex"), n=9, step=0.18, cols=3, scale=0.6, glow=True)]},
    sources=["call"])
stage("s15_leases", "m2_leases", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Much of this"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("counter", x=800, y=160, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "of data center leases"}, 329.1]], text="DATA CENTER LEASES NOT YET STARTED (10-K)"),
              it("sign", x=1400, y=330, text="FINANCE LEASES ON THE BOOKS: $71.0BN", at=C("Finance lease liabilities"), color="#FFE0B2", size=28),
              it("letters", x=1100, y=480, text="NOT DEBT · STILL A PROMISE TO PAY", at=C("Much of this"), size=44, color="gold"),
              buddy(450, 860, at=0.4, mood="worry", label="MSFT", color="#3A86FF", hop=14)]},
    sources=["rel", "tenq"])
stage("s16_returns", "m2_returns", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The share count"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "came to"}, 48.0]], text="BUYBACKS + DIVIDENDS, 12 MONTHS"),
              it("sign", x=1400, y=280, text="$21.0BN BUYBACKS + $27.0BN DIVIDENDS", at=C("came to"), color="#FFE0B2", size=28),
              it("letters", x=1100, y=420, text="≈ 80% OF FREE CASH (OUR CALC.)", at=C("of free cash flow"), size=48, color="gold"),
              it("sign", x=1250, y=600, text="SHARE COUNT: ABOUT FLAT", at=C("The share count"), color="#C8E6C9", size=30)]},
    sources=["tenq"])
board("p17_cash", "m2_draw", "Where twelve months of operating cash went", C("Here is the operating cash bar"), [
    {"d": "M 700 780 L 1560 780", "color": "ink", "width": 4, "start": C("Here is the operating cash bar"), "label": lbl("$BN · TTM · OUR CALC.", 1130, 830, 18, "ink")},
    bar(740, 150, 780, 360, "accent2", C("Here is the operating cash bar"), "OCF 196"),
    bar(940, 150, 780, 489, "risk", C("Here is the capex bar"), "CAPEX 136"),
    bar(1140, 150, 780, 651, "accent3", C("Here is what's left"), "FCF 60"),
    bar(1340, 150, 780, 677, "accent", C("And here is what went back"), "RETURNED 48"),
], C("Almost nothing", 0.1), [1415, 640], sources=["tenq"])
kinetic("s18_t2", "m2_transition", [("At four trillion dollars…", 70, "At four trillion", None, False),
                                    ("…what are you paying for?", 72, "what are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s19_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s20_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Those last two"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (TTM, OUR CALC.)", note="THE GAP = THE DATA CENTER BILL",
                    base="TO BE CHOSEN: CAPEX IS BOOMING",
                    lenses=[("P/E (NET INCOME)", "27.8×", C("Price to earnings")), ("FCF YIELD", "1.5%", C("Free cash flow")), ("OCF YIELD", "4.9%", C("Operating cash flow"))]),
              stamp(1500, 900, at=0.4, scale=0.7)]},
    sources=["tenq", "px"])
stage("s21_proxy", "m3_proxy", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("It's a proxy"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="A PROXY FOR A BUILDING SPREE", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=260, text="OCF $195.9BN", at=C("We take operating cash"), color="#BBDEFB", size=32),
              it("sign", x=1050, y=260, text="− DEPRECIATION ≈ $38.3BN", at=C("subtract depreciation"), color="#FFCDD2", size=32),
              it("letters", x=1000, y=420, text="= ≈ $157.6BN · YIELD ≈ 4%", at=C("That leaves"), size=50, color="gold"),
              it("sign", x=1300, y=560, text="ASSUMES CAPEX FALLS BACK TOWARD DEPRECIATION", at=C("It's a proxy"), color="#FFE0B2", size=24),
              buddy(1750, 860, at=0.4, mood="cool", label="PROXY", color="#FFE14D", hop=16)]},
    sources=["tenq", "px"])
stage("s22_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 5.5, C("With an eight percent"), "≈ 5.5% / YR"), ("AT 10%", 10.2, C("With ten percent"), "≈ 10.2% / YR"),
                    ["MARKET CAP $3.96TN (NOV 10)", "PROXY: OCF − DEPREC. $157.6BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED GROWTH, 10 YEARS", base="PROXY (CAPEX BOOM)", placardX=860, placardY=-200),
              it("sign", x=1500, y=880, text="ON TODAY'S FCF: ≈ 18-23% / YR", at=C("But run the same math"), color="#FFCDD2", size=30),
              stamp(1150, 960, at=0.6, scale=0.55),
              buddy(1750, 640, at=0.5, mood="happy", moods=[[C("the answer jumps"), "shock"]], label="MSFT", color="#3A86FF", hop=22, scale=0.8)]},
    sources=["tenq", "px"])
stage("s23_mustearn", "m3_mustearn", {
    "zones": [Z("cloudport", signs=["EVERY DOLLAR MUST WORK", "RETURN TO SENDER?", "CAPEX IN · CASH OUT", "NO FREE CLOUDS"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("every dollar of capex"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=130, text="WHAT THE CAPEX MUST EARN", at=0.2, size=58, color="gold"),
              it("sign", x=1000, y=270, text="IF CAPEX STAYS ≈ $136BN A YEAR…", at=C("keeps spending"), color="#BBDEFB", size=30),
              it("letters", x=1000, y=420, text="EACH $1 → +18¢ TO +32¢ OF YEARLY CASH", at=C("every dollar of capex"), size=46, color="gold"),
              it("sign", x=1000, y=540, text="WITHIN 10 YEARS · OUR ROUGH ILLUSTRATION", at=C("within a decade"), color="#FFE0B2", size=26),
              coins(500, 860, [1500, 640], at=C("every dollar of capex"), rate=5)]},
    sources=["tenq", "px"])
board("p24_two", "m3_draw", "Two answers, one price (our illustration)", C("Here is the growth the price needs"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is the growth the price needs"), "label": lbl("% A YEAR · 10 YEARS · OUR CALC.", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 676, "accent3", C("Here is the growth the price needs"), "PROXY @8% 5.5"),
    bar(1010, 170, 780, 587, "accent2", C("Here it is at the higher rate"), "PROXY @10% 10.2"),
    bar(1240, 170, 780, 337, "risk", C("And here is what it needs"), "FCF 18-23"),
    {"d": arrow((1180, 600), (1235, 360), 0.1), "color": "accent", "width": 5, "kind": "arrow", "start": C("The difference"), "label": lbl("THE CAPEX", 1130, 470, 18, "accent")},
], C("the capex", 0.1), [1320, 420], sources=["tenq", "px"])
kinetic("s25_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s26_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s27_azure", "m4_azure", {
    "zones": [Z("cloudport", signs=PORT, busyAt=0.5)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("If the new capacity"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="1 · AZURE KEEPS GROWING NEAR 50%", at=0.2, size=50, color="gold"),
              it("sign", x=750, y=240, text="GUIDE: +49-50% (CONSTANT CURRENCY)", at=C("The C F O guided"), color="#BBDEFB", size=28),
              it("sign", x=1350, y=350, text="'DEMAND CONTINUES TO EXCEED AVAILABLE SUPPLY'", at=C("customer demand"), color="#FFE0B2", size=24),
              it("letters", x=1200, y=500, text="CAPACITY ON TIME → REVENUE", at=C("If the new capacity"), size=42, color="gold")]},
    sources=["call"])
stage("s28_backlog", "m4_backlog", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Bookings actually fell"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="2 · THE BACKLOG CONVERTS", at=0.2, size=56, color="gold"),
              it("counter", x=750, y=250, at=C("commercial backlog is"), prefix="$", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "up"}, 677]], text="COMMERCIAL BACKLOG (RPO), +73%"),
              it("sign", x=1400, y=300, text="≈ 30% IN 12 MONTHS ≈ $200BN", at=C("roughly thirty percent"), color="#C8E6C9", size=30),
              it("sign", x=1300, y=450, text="BOOKINGS −12% (BIG DEALS LAST YEAR)", at=C("Bookings actually fell"), color="#FFCDD2", size=28),
              buddy(1700, 860, at=0.4, mood="happy", moods=[[C("Bookings actually fell"), "worry"]], label="RPO", color="#7DFF8A", hop=18)]},
    sources=["call"])
stage("s29_capex", "m4_capex", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The price needs"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="3 · CAPEX PEAKS, FREE CASH RECOVERS", at=0.2, size=50, color="gold"),
              it("sign", x=700, y=240, text="THIS QUARTER: 'OVER $50 BILLION'", at=C("expects capex"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=240, text="CALENDAR 2026: ≈ $170BN", at=C("for the calendar year"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=380, text="'REMAIN FREE CASH FLOW POSITIVE IN FY27'", at=C("remain free cash flow positive"), color="#BBDEFB", size=28),
              it("letters", x=1000, y=520, text="THE PRICE NEEDS A LOT MORE THAN POSITIVE", at=C("The price needs"), size=40, color="gold")]},
    sources=["call"])
stage("s30_margin", "m4_margin", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Growth is not"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="4 · MARGINS HOLD", at=0.2, size=58, color="gold"),
              it("calendar", x=650, y=290, at=C("Microsoft Cloud gross margin"), pages=[[0, "FY2025", "69%"], [C("slipped to"), "Q1 FY27", "66%"], [C("the guide is"), "Q2 GUIDE", "≈ 65%"]]),
              it("sign", x=1400, y=300, text="REVENUE GUIDE $96-97.1BN (+18-19%)", at=C("Revenue for the quarter"), color="#C8E6C9", size=28),
              it("letters", x=1300, y=470, text="WATCH PROFIT PER DOLLAR", at=C("Growth is not"), size=44, color="gold")]},
    sources=["rel", "call"])
kinetic("s31_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s32_c5", "m5_card", "Risks and Upside", "What Microsoft itself warns about")
stage("s33_capexrisk", "m5_capex", {
    "zones": [Z("datacenter", darkAt=6.0)], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Overestimating demand"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 1 · THE BUILD-OUT ITSELF", at=0.2, size=54, color="gold"),
              it("sign", x=1000, y=240, text="'IN ADVANCE OF FULLY DEVELOPED REVENUE STREAMS'", at=C("in advance of fully developed"), color="#FFE0B2", size=24),
              it("sign", x=1000, y=370, text="IDLE CAPACITY → WRITE-DOWNS", at=C("Overestimating demand"), color="#FFCDD2", size=32),
              buddy(1700, 860, at=0.4, mood="worry", label="RACKS", color="#7B61FF", hop=10)]},
    sources=["tenq"])
stage("s34_partner", "m5_partner", {
    "zones": [Z("cloudport", signs=["ONE BIG CUSTOMER", "PRICE WAR AHEAD?", "DOCK 1 RESERVED", "MARGINS · HANDLE WITH CARE"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And if prices"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 2 · CONCENTRATION", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=250, text="PARTNERS = BIG AZURE CUSTOMERS", at=C("Partners like OpenAI"), color="#FFE0B2", size=30),
              it("sign", x=1350, y=370, text="AI PRICES ↓ → MARGINS ↓", at=C("And if prices"), color="#FFCDD2", size=32),
              it("pricetag", x=1650, y=560, at=C("And if prices"), text="AI COMPUTE", pages=[[C("because of competition"), "AI COMPUTE ↓", True]])]},
    sources=["tenq"])
stage("s34b_stake", "m5_stake", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("Last fiscal year"), "x": 1000, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE OPENAI TIE", at=0.2, size=60, color="gold"),
              it("sign", x=740, y=250, text="STAKE ≈ 24% (AS-CONVERTED)", at=C("Microsoft owns"), color="#BBDEFB", size=30),
              it("sign", x=1260, y=250, text="OPENAI OWES $7.2BN", at=C("OpenAI owes it"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=370, text="FUNDING: $12.0BN OF $13.0BN PAID IN", at=C("has committed"), color="#FFE0B2", size=30),
              it("sign", x=1000, y=490, text="FY2026: $24.1BN = 7.3% OF REVENUE", at=C("Last fiscal year"), color="#C8E6C9", size=30),
              it("sign", x=1000, y=610, text="'MAY RESULT IN EARLY TERMINATION OR RENEGOTIATION'", at=C("Microsoft's own filing"), color="#FFCDD2", size=26),
              buddy(1700, 860, at=0.4, mood="worry", label="MSFT", hop=12)]},
    sources=["tenq"])
stage("s35_other", "m5_other", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Regulators in Europe"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 3 · THE FINE PRINT", at=0.2, size=58, color="gold"),
              it("sign", x=750, y=250, text="IRS: +$28.9BN + PENALTIES (DISPUTED)", at=C("The I R S"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=370, text="REGULATORS: EU · UK · US · CHINA", at=C("Regulators in Europe"), color="#BBDEFB", size=28),
              it("sign", x=1000, y=490, text="TARIFFS → DEVICE + DATA CENTER COSTS", at=C("And tariffs"), color="#FFCDD2", size=28),
              it("gavel", x=1700, y=520, hits=[C("which Microsoft disputes"), C("are watching")])]},
    sources=["tenq"])
stage("s36_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("None of that"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("BUILD-OUT AHEAD OF REVENUE", 0.3), ("ONE BIG CUSTOMER · AI PRICES", 0.9), ("IRS · REGULATORS · TARIFFS", 1.5)],
                    [("FOUNDRY REVENUE: MORE THAN 3×", C("Foundry revenue")), ("COPILOT DAILY USERS > 5×", C("Copilot")), ("UNDERUSED CAPACITY, SOLD", C("underused"))],
                    title="RISKS VS UPSIDE (MICROSOFT'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="UPSIDE IS UNSIZED: NO DOLLAR FIGURES GIVEN", at=C("None of that"), color="#C8E6C9", size=28)]},
    sources=["call", "tenq"])
kinetic("s37_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
stage("s38_score", "payoff", {
    "zones": [Z("cloudport", signs=["SCOREBOARD", "NEXT REPORT: LATE JAN 2027?", "WATCH THE CAPEX", "BACKLOG CHECK"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}, {"at": C("If those hold up"), "x": 960, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [scorecard([("AZURE GROWTH", "VS +49-50% CC GUIDE (Q1: +48%)", C("One, Azure")),
                         ("CAPEX AND FREE CASH", "VS 'OVER $50BN' · FCF VS $18.6BN", C("Two, capex")),
                         ("BACKLOG $677BN", "BROADER THAN ONE CUSTOMER? (OPENAI ≈ 11%)", C("Three, the"))], x=960, y=220, at=0.2, scale=0.92),
              stamp(1500, 900, at=0.5, scale=0.7),
              buddy(300, 900, at=0.4, mood="happy", moods=[[C("If they crack"), "worry"]], label="MSFT", color="#3A86FF", hop=20)]},
    sources=["call", "tenq"])
stage("s39_edition", "payoff2", {
    "zones": [machine(SEGS, "THE MICROSOFT MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [stamp(800, 900, at=0.3, scale=0.9),
              it("sign", x=1100, y=200, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=26)]},
    sources=["rel"])
add("s40_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_microsoft_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Microsoft (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
