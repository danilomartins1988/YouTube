"""Generates projects/before-you-buy-nvidia-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Nvidia, November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

Series look: very animated retro-futurist cartoon comedy (genre-level inspiration only, original designs). Series kit:
`moneymachine` set + `pricedin` / `riskscale` / `editionstamp` / `scorecard` items (tools/byb_kit.py helpers).
One visual language per part:
- Hook: chip city with a giant counter + edition stamp; the stock elevator of the two-week fall with the Huang caricature
  (respectful preset, label, only what the 8-K says); the disclaimer.
- Part 1 (the machine): the money machine (data center vs edge pipes); the data-center campus; a box-and-arrow board.
- Part 2 (the cash): the vault, the bank hall (buybacks), the office (receivables), the exchange (stakes), a bar board.
- Part 3 (what's priced in): the priced-in calculator (three lenses + gauge), the exchange, a bar board.
- Part 4 (what has to happen): data-center city, the studio, the site, the fab.
- Part 5 (risks and upside): the empty chair (no caricature next to the investigation line), the port, the risk scale.
- Payoff: the scorecard with the edition stamp.
Rules: no Nvidia logo, generic chips and racks only; numbers match sources.yaml; our calculations labelled.
QUARTERLY REFRESH: change EDITION and the numbers below to the new sources.yaml values, re-run.
Run: python tools/gen_byb_nvidia_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/before-you-buy-nvidia-2026-11/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 17, 2026 CLOSE", "LATEST REPORT: Q3 FY2027 (OCT 25, 2026)")
SEGS = [("HYPERSCALE $60.1BN", 60.1, "#3DF5FF", None), ("AI CLOUDS + ENTERPRISE $47.5BN", 47.5, "#7DFF8A", None),
        ("EDGE COMPUTING $8.2BN", 8.2, "#FF9F1C", None)]
JOKES = ["GPUS: HANDLE WITH OVEN MITTS", "WAITLIST STARTS HERE", "MEMORY NOT INCLUDED", "COOLING: VERY MUCH REQUIRED"]
HUANG = dict(who="huang")

# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("chipcity", signs=["ACCELERATOR AVE.", "RACKS DELIVERED DAILY", "NO LOITERING NEAR THE P/E", "QUARTER 3 · OPEN LATE"])], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 470, "zoom": 1.15}, {"at": 1.2, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=700, y=200, at=0.05, prefix="$", suffix="BN", decimals=1, steps=[[0.05, 0], [{"cue": "of revenue in three months"}, 115.8]], text="Q3 FY2027 REVENUE (+103%)", scale=1.1, until=C("just before that report")),
              it("counter", x=700, y=200, at=C("just before that report"), prefix="≈ $", suffix="TN", decimals=2, steps=[[0, 0], [{"cue": "was worth"}, 3.75]], text="NVIDIA MARKET VALUE (OUR CALC.)", scale=1.3),
              it("sign", x=700, y=400, text="$155.46 × 24.1BN SHARES", at=C("a share, times"), color="#BBDEFB", size=32),
              it("letters", x=1050, y=620, text="≈ 16.5× ITS PROFIT", at=C("By our math"), size=60, color="gold"),
              stamp(1480, 470, at=C("just before that report"), scale=0.75),
              it("hbm", x=1780, y=800, at=0.4, scale=0.9),
              buddy(480, 860, at=0.5, mood="happy", moods=[[C("By our math"), "shock"]], label="NVDA", hop=30)]},
    sources=["pr", "px"])
stage("s02_twist", "h_twist", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("In the middle"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=650, y=200, at=0.1, prefix="$", suffix="", decimals=2, steps=[[0.1, 200.13], [{"cue": "in two weeks"}, 155.46]], text="NVDA CLOSE · NOV 4 → NOV 17"),
              it("sign", x=650, y=390, text="≈ −22% IN TWO WEEKS (OUR CALC.)", at=C("in two weeks"), color="#FFCDD2", size=30),
              it("caricature", x=1450, y=880, at=C("In the middle"), scale=1.0, poses=[[0, "stand"]], label="JENSEN HUANG · CO-FOUNDER", **HUANG),
              it("sign", x=1450, y=250, text="NOV 11: RESIGNATION ACCEPTED (8-K)", at=C("the board accepted"), color="#FFE0B2", size=28),
              it("sign", x=1450, y=350, text="CEO SINCE 1993 (10-K)", at=C("at the top"), color="#BBDEFB", size=26)]},
    sources=["px", "ceo8k", "tenk"])
stage("s03_question", "h_question", {
    "zones": [Z("exchange", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 500, "zoom": 1.1}, {"at": 0.8, "x": 1050, "y": 520, "zoom": 1.0, "dur": 2.5}], "drift": 3,
    "items": [it("letters", x=1000, y=150, text="WHAT IS THE PRICE BETTING ON?", at=C("What is that price"), size=58, color="gold"),
              it("sign", x=650, y=320, text="WHAT HAS TO HAPPEN?", at=C("What has to happen"), color="#C8E6C9", size=34),
              it("sign", x=1350, y=320, text="WHAT COULD BREAK IT?", at=C("what could break"), color="#FFCDD2", size=34),
              buddy(1000, 860, at=0.4, mood="worry", label="NVDA", hop=12)]})
stage("s04_promise", "h_promise", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.05}], "drift": 0,
    "items": [it("sign", x=330, y=380, text="1 · THE MACHINE", at=C("open the machine"), color="#BBDEFB", size=30),
              it("sign", x=760, y=380, text="2 · THE CASH", at=C("follow the cash"), color="#FFE0B2", size=30),
              it("sign", x=1190, y=380, text="3 · PRICED IN", at=C("priced in"), color="#C8E6C9", size=30),
              it("sign", x=1610, y=380, text="4 · SCORECARD", at=C("three numbers"), color="#E1BEE7", size=30),
              it("letters", x=960, y=700, text="BEFORE YOU BUY: NVIDIA", at=0.4, size=64, color="gold")]})
disclaimer("s05_disc", "h_disclaimer", C("Everything here"), company="NVIDIA'S", sources=["pr"])

# ====================================================================== PART 1: the machine
card("s06_c1", "m1_card", "The Machine", "Where the money comes from")
stage("s07_machine", "m1_machine", {
    "zones": [machine([(SEGS[0][0], SEGS[0][1], SEGS[0][2], C("data centers brought in")), (SEGS[1][0], SEGS[1][1], SEGS[1][2], C("data centers brought in")),
                       (SEGS[2][0], SEGS[2][1], SEGS[2][2], C("The rest"))], "THE NVIDIA MACHINE", "SALES", JOKES)], "worldW": 2600,
    "cam": [{"at": 0, "x": 1100, "y": 520, "zoom": 0.88}, {"at": C("The rest"), "x": 1000, "y": 540, "zoom": 0.9, "dur": 2.0}], "drift": 2,
    "items": [it("sign", x=1100, y=150, text="10-Q NOT FILED YET · FIGURES FROM THE 8-K", at=0.3, until=C("data centers brought in"), color="#FFE0B2", size=28),
              it("counter", x=1500, y=830, at=C("data centers brought in"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "of everything"}, 107.6]], text="DATA CENTER, Q3 FY2027 (93%)", scale=1.0),
              it("sign", x=600, y=960, text="EDGE: PCS · WORKSTATIONS · CARS · ROBOTS", at=C("The rest"), color="#FFE0B2", size=28)]},
    sources=["pr", "cfo"])
stage("s08_split", "m1_split", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("The second pipe"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="TWO PIPES INSIDE DATA CENTER", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=240, text="HYPERSCALE $60.1BN · +71%", at=C("The giant cloud companies"), color="#BBDEFB", size=32),
              it("sign", x=1350, y=340, text="AI CLOUDS, INDUSTRY, ENTERPRISE $47.5BN · +195%", at=C("The second pipe"), color="#C8E6C9", size=28),
              it("isodc", x=1000, y=760, at=C("And the new Vera Rubin"), n=6, step=0.25, cols=3, scale=0.6, glow=True, label="RUBIN RACKS SHIPPING"),
              buddy(1750, 860, at=0.4, mood="happy", label="RUBIN", color="#76E04E", hop=24)]},
    sources=["pr", "cfo"])
stage("s09_profit", "m1_profit", {
    "zones": [machine([(l, v, c, None) for l, v, c, _ in SEGS], "THE NVIDIA MACHINE", "PROFIT", JOKES, boomAt=4.0)], "worldW": 2600,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.0}, {"at": C("So operating income"), "x": 1150, "y": 540, "zoom": 0.88, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=800, y=180, text="THE UNUSUAL PART", at=0.2, size=56, color="gold"),
              it("sign", x=650, y=960, text="GROSS MARGIN 74.8% · OPEX $9.2BN", at=C("Gross margin was"), color="#C8E6C9", size=30),
              it("sign", x=1350, y=960, text="OPERATING INCOME $77.5BN ≈ 67% (OUR CALC.)", at=C("So operating income"), color="#FFE0B2", size=28),
              it("sign", x=1350, y=860, text="NET INCOME $65.3BN · EPS $2.70", at=C("Net income was"), color="#BBDEFB", size=28),
              buddy(2200, 860, at=0.4, mood="cool", moods=[[C("So operating income"), "happy"]], label="NVDA", hop=24)]},
    sources=["pr"])
stage("s10_who", "m1_who", {
    "zones": [Z("port", x1=1500), Z("dccity", x0=1500)], "worldW": 3200,
    "cam": [{"at": 0, "x": 750, "y": 520, "zoom": 1.0}, {"at": C("And it's concentrated"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 1,
    "items": [it("letters", x=750, y=100, text="WHO PAYS? (BY CUSTOMER HQ)", at=0.2, size=50, color="gold"),
              it("sign", x=750, y=230, text="U.S. $72.9BN", at=C("the United States"), color="#BBDEFB", size=34),
              it("sign", x=750, y=330, text="TAIWAN $30.3BN", at=C("Taiwan"), color="#FFE0B2", size=34),
              it("sign", x=750, y=430, text="CHINA (INCL. HK) $11.1BN", at=C("and China"), color="#FFCDD2", size=30),
              it("sign", x=2200, y=200, text="3 DIRECT CUSTOMERS: 14% + 11% + 11%", at=C("Just three direct customers"), color="#FFE0B2", size=30),
              it("letters", x=2200, y=330, text="= 36% OF REVENUE", at=C("of revenue from three buyers"), size=50, color="gold"),
              it("sign", x=2200, y=450, text="NAMES NOT DISCLOSED", at=C("doesn't name them"), color="#F5F5F5", size=28),
              ship(kind="cargo", x=[[0, 300], [12, 1100]], y=760, scale=0.7)]},
    sources=["supp"])
board("p11_machine", "m1_draw", "The machine (Q3 FY2027, 8-K)", C("Here is the data center pipe"), [
    {"d": rect(640, 400, 300, 200), "color": "accent2", "width": 6, "kind": "box", "start": C("Here is the data center pipe"), "label": lbl("DATA CENTER 93%", 790, 508, 22, "accent2")},
    {"d": rect(640, 700, 300, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("Here is edge computing"), "label": lbl("EDGE 7%", 790, 752, 20, "accent3")},
    {"d": rect(1180, 520, 300, 200), "color": "accent", "width": 6, "kind": "box", "start": C("Both pour into"), "label": lbl("OPERATING PROFIT", 1330, 628, 22, "accent")},
    {"d": arrow((945, 500), (1175, 580)), "color": "accent2", "width": 8, "kind": "arrow", "start": C("Both pour into")},
    {"d": arrow((945, 745), (1175, 680)), "color": "accent3", "width": 4, "kind": "arrow", "start": C("Both pour into")},
    {"d": arrow((1330, 725), (1330, 860)), "color": "risk", "width": 3, "kind": "arrow", "start": C("look how little leaks"), "label": lbl("COSTS ≈ 33%", 1440, 820, 18, "risk")},
], C("About two thirds", 0.1), [1330, 620], sources=["pr", "cfo"])
kinetic("s12_t1", "m1_transition", [("A machine this profitable…", 66, "A machine this profitable", None, False),
                                    ("…so where does it go?", 72, "So where does it go", "gold", False)])

# ====================================================================== PART 2: the cash
card("s13_c2", "m2_card", "The Cash", "Where the cash goes")
stage("s14_cash", "m2_cash", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Over the last twelve months"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=800, y=150, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "operating cash flow was"}, 48.3]], text="OPERATING CASH FLOW, Q3"),
              it("sign", x=1350, y=260, text="FREE CASH FLOW $43.8BN (Q3)", at=C("Free cash flow was"), color="#C8E6C9", size=30),
              it("letters", x=1100, y=420, text="LAST 12 MONTHS ≈ $149BN (OUR CALC.)", at=C("Over the last twelve months"), size=46, color="gold"),
              it("sign", x=1100, y=550, text="CAPEX ONLY ≈ $10BN", at=C("And spending on buildings"), color="#FFE0B2", size=30),
              it("wafer", x=1750, y=780, r=150, at=C("Nvidia designs the chips"), n=7),
              coins(400, 700, [1600, 760], at=C("Free cash flow was"), rate=6)]},
    sources=["pr", "q4"])
stage("s15_returns", "m2_returns", {
    "zones": [Z("bankhall")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("The dividend is now"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [it("counter", x=800, y=140, at=0.2, prefix="$", suffix="BN", decimals=1, steps=[[0.2, 0], [{"cue": "Nvidia returned"}, 28.1]], text="RETURNED IN Q3 (8-K)"),
              it("sign", x=1400, y=230, text="BUYBACKS $22.1BN + DIVIDENDS $6.0BN", at=C("in buybacks"), color="#FFE0B2", size=28),
              it("letters", x=1100, y=370, text="≈ 2/3 OF THE QUARTER'S FREE CASH", at=C("of the quarter's free cash"), size=44, color="gold"),
              it("calendar", x=600, y=600, at=C("The dividend is now"), pages=[[0, "APR 2026", "1¢"], [C("up from one cent"), "DEC 2026", "25¢"]]),
              it("sign", x=1350, y=560, text="AUTHORIZATION LEFT: $227.3BN", at=C("And there's"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=670, text="≈ 6% OF MARKET VALUE (OUR CALC.)", at=C("of the company's market value"), color="#C8E6C9", size=28)]},
    sources=["pr", "cfo", "q4"])
stage("s16_quality", "m2_quality", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("And inventory jumped"), "x": 1100, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="A FOOTNOTE ON THE CASH", at=0.2, size=58, color="gold"),
              it("counter", x=750, y=270, at=C("Customers owe Nvidia"), prefix="$", suffix="BN", decimals=1, steps=[[0, 0], [{"cue": "It now takes"}, 81.0]], text="OWED BY CUSTOMERS (RECEIVABLES)"),
              it("calendar", x=1350, y=300, at=C("It now takes"), pages=[[0, "Q2", "60 DAYS"], [C("up from"), "Q3", "64 DAYS"]]),
              it("sign", x=1000, y=480, text="'EXTENDED PAYMENT TERMS' ON BIG DEALS", at=C("extended payment terms"), color="#FFE0B2", size=28),
              it("sign", x=1000, y=580, text="INVENTORY $31.6BN → $39.7BN", at=C("And inventory jumped"), color="#BBDEFB", size=30),
              buddy(1700, 860, at=0.3, mood="worry", label="CASH", color="#23995A", hop=12)]},
    sources=["cfo"])
stage("s17_stakes", "m2_stakes", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("That makes profit lumpy"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 2,
    "items": [it("counter", x=750, y=180, at=C("One more pile"), prefix="≈ $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "worth"}, 110]], text="STAKES IN OTHER COMPANIES"),
              it("sign", x=1350, y=260, text="MOSTLY PRIVATE AI LABS + FINANCIERS", at=C("mostly private"), color="#BBDEFB", size=28),
              it("letters", x=1100, y=420, text="LUMPY PROFIT", at=C("That makes profit lumpy"), size=56, color="gold"),
              it("sign", x=750, y=560, text="9-MONTH GAINS $25.5BN (PRE-TAX)", at=C("Over the first nine months"), color="#C8E6C9", size=28),
              it("sign", x=1450, y=560, text="Q3 WRITE-DOWN $1.8BN", at=C("Nvidia wrote down"), color="#FFCDD2", size=28),
              buddy(1750, 860, at=0.4, mood="cool", moods=[[C("Nvidia wrote down"), "worry"]], label="NVDA", hop=16)]},
    sources=["pr", "cfo", "supp"])
board("p18_cash", "m2_draw", "One quarter of cash (Q3 FY2027)", C("Here is the free cash flow bar"), [
    {"d": "M 700 760 L 1560 760", "color": "ink", "width": 4, "start": C("Here is the free cash flow bar"), "label": lbl("$BN · 8-K · OUR CALC.", 1130, 810, 18, "ink")},
    bar(740, 150, 760, 360, "accent2", C("Here is the free cash flow bar"), "FCF 43.8"),
    bar(940, 150, 760, 558, "accent", C("Here is the buyback bar"), "BUYBACKS 22.1"),
    bar(1140, 150, 760, 705, "accent3", C("Here are the dividends"), "DIVIDENDS 6.0"),
    bar(1340, 150, 760, 616, "risk", C("And this piece"), "KEPT ≈ 15.7"),
], C("straight back", 0.1), [1015, 560], sources=["pr"])
kinetic("s19_t2", "m2_transition", [("At almost four trillion dollars…", 66, "At almost four trillion", None, False),
                                    ("…what are you paying for?", 72, "what exactly are you paying for", "gold", False)])

# ====================================================================== PART 3: what's priced in
card("s20_c3", "m3_card", "What's Priced In", "Our math, assumptions on screen")
stage("s21_lenses", "m3_lenses", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.05}, {"at": C("Capital spending"), "x": 1000, "y": 540, "zoom": 1.0, "dur": 2.0}], "drift": 2,
    "items": [gauge(("8% RATE", 0, 99), ("10% RATE", 0, 99), [], x=960, y=650, at=0.2, scale=0.75, title="THREE LENSES (LAST 12 MONTHS, OUR CALC.)", note="NET CASH ≈ $21BN · ≈ 0.6% OF THE PRICE",
                    base="FREE CASH FLOW (CAPEX SMALL)",
                    lenses=[("P/E (≈18.7× EX GAINS)", "16.6×", C("Price to earnings")), ("FCF YIELD", "4.0%", C("Free cash flow yield")), ("OCF YIELD", "4.2%", C("Operating cash flow yield"))]),
              stamp(1500, 900, at=0.4, scale=0.7)]},
    sources=["pr", "q4", "px"])
stage("s22_gauge", "m3_gauge", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("With an eight percent"), "x": 960, "y": 540, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [gauge(("AT 8%", 5.6, C("With an eight percent"), "≈ 5.6% / YR"), ("AT 10%", 10.3, C("With ten percent"), "≈ 10.3% / YR"),
                    ["MARKET CAP $3.75TN (NOV 17)", "FCF LAST 12 MO. $148.6BN", "RATES 8% AND 10%", "10 YEARS, THEN 3%"], x=760, y=640, at=0.2, scale=0.85,
                    title="IMPLIED FCF GROWTH, 10 YEARS", placardX=860, placardY=-200),
              stamp(1200, 940, at=0.6, scale=0.6),
              buddy(1740, 860, at=0.5, mood="happy", moods=[[C("With ten percent"), "shock"]], label="NVDA", hop=22)]},
    sources=["pr", "q4", "px"])
stage("s23_zero", "m3_zero", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("is a bet on growth"), "x": 1150, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [it("letters", x=1000, y=110, text="IF CASH NEVER GREW…", at=0.2, size=60, color="gold"),
              it("sign", x=700, y=260, text="≈ $2.4TN AT 8%", at=C("at eight percent"), color="#BBDEFB", size=34),
              it("sign", x=1300, y=260, text="≈ $1.8TN AT 10%", at=C("at ten"), color="#BBDEFB", size=34),
              it("letters", x=1000, y=420, text="⅓ TO ½ OF THE PRICE = A BET ON GROWTH", at=C("is a bet on growth"), size=44, color="gold"),
              buddy(1000, 860, at=0.4, mood="shock", moods=[[C("is a bet on growth"), "cool"]], label="NVDA", hop=26)]},
    sources=["pr", "px"])
board("p24_gap", "m3_draw", "Flat cash vs the price (our illustration)", C("Here is what flat cash"), [
    {"d": "M 720 780 L 1520 780", "color": "ink", "width": 4, "start": C("Here is what flat cash"), "label": lbl("$TN · OUR CALC. · NOV 17, 2026", 1120, 830, 18, "ink")},
    bar(780, 170, 780, 600, "accent2", C("Here is what flat cash"), "FLAT @10% 1.8"),
    bar(1010, 170, 780, 533, "accent3", C("Here it is at eight"), "FLAT @8% 2.4"),
    bar(1240, 170, 780, 395, "accent", C("And here is the actual price"), "PRICE 3.75"),
    {"d": arrow((1190, 530), (1235, 410), 0.1), "color": "risk", "width": 5, "kind": "arrow", "start": C("That gap"), "label": lbl("THE GAP", 1150, 470, 18, "risk")},
], C("paying for in advance", 0.1), [1320, 460], sources=["pr", "px"])
stage("s25_history", "m3_history", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But the price only asks"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="THE STRANGE PART", at=0.2, size=58, color="gold"),
              it("calendar", x=600, y=320, at=C("Revenue just grew"), pages=[[0, "Q3 FY26", "$57.0BN"], [C("in a year"), "Q3 FY27", "$115.8BN"]]),
              it("sign", x=1300, y=250, text="Q4 OUTLOOK $130BN ± 3% (EXTRA WEEK)", at=C("Nvidia's own outlook"), color="#C8E6C9", size=28),
              it("letters", x=1300, y=400, text="PRICE ASKS ≈ 5.6–10.3% A YEAR", at=C("But the price only asks"), size=42, color="gold"),
              it("sign", x=1300, y=530, text="PRICED LIKE A PEAK?", at=C("It's treating this as a peak"), color="#FFCDD2", size=34),
              buddy(1600, 860, at=0.4, mood="worry", label="NVDA", hop=16)]},
    sources=["pr", "cfo"])
kinetic("s26_t3", "m3_transition", [("So what has to go right?", 78, "So what has to go right", "gold", False)])

# ====================================================================== PART 4: what has to happen
card("s27_c4", "m4_card", "What Has to Happen", "Four things that must go right")
stage("s28_demand", "m4_demand", {
    "zones": [Z("dccity")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("If even one"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="1 · THE BIG BUYERS KEEP BUILDING", at=0.2, size=52, color="gold"),
              it("sign", x=750, y=230, text="HYPERSCALE $60.1BN IN ONE QUARTER", at=C("The giant clouds alone"), color="#BBDEFB", size=30),
              it("sign", x=1350, y=340, text="3 BUYERS = 36% OF REVENUE", at=C("three direct customers"), color="#FFE0B2", size=30),
              it("isodc", x=1000, y=760, at=0.4, n=9, step=0.2, cols=3, scale=0.6, glow=True),
              it("letters", x=1300, y=480, text="ONE SLOWDOWN SHOWS UP FAST", at=C("If even one"), size=40, color="gold")]},
    sources=["cfo", "supp"])
stage("s29_margin", "m4_margin", {
    "zones": [Z("fab")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A new generation"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="2 · MARGINS HOLD THROUGH RUBIN", at=0.2, size=52, color="gold"),
              it("counter", x=750, y=250, at=0.4, prefix="", suffix="%", decimals=1, steps=[[0, 74.8], [{"cue": "next quarter"}, 71.5]], text="GROSS MARGIN: Q3 → Q4 OUTLOOK (MIDPOINT)"),
              it("sign", x=750, y=420, text="OUTLOOK 71–72% (NVIDIA)", at=C("Nvidia's own outlook calls"), color="#FFE0B2", size=30),
              it("hbm", x=1450, y=520, at=C("A new generation"), scale=0.8),
              it("sign", x=1450, y=780, text="DOES IT CLIMB BACK?", at=C("The question is"), color="#C8E6C9", size=32)]},
    sources=["pr", "cfo"])
stage("s30_paid", "m4_paid", {
    "zones": [Z("site")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Its guarantees could reach"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="3 · CUSTOMERS CAN PAY", at=0.2, size=56, color="gold"),
              it("sign", x=700, y=230, text="2 CUSTOMERS: 18% + 17% OF RECEIVABLES", at=C("Two direct customers"), color="#FFE0B2", size=28),
              it("sign", x=1300, y=330, text="NEOCLOUD DEALS ≤ $32BN · ONLY IF FINANCED", at=C("Its neocloud agreements"), color="#BBDEFB", size=26),
              it("counter", x=1000, y=480, at=C("Its guarantees could reach"), prefix="UP TO $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "of credit support"}, 118]], text="GUARANTEES (MAX. EXPOSURE)"),
              it("sign", x=1000, y=640, text="OHIO SITE FOR OPENAI LEASES: UP TO $105BN", at=C("of credit support"), color="#FFCDD2", size=26),
              it("sign", x=1000, y=730, text="PAID ON GUARANTEES SO FAR: $0", at=C("Nvidia says it hasn't paid"), color="#C8E6C9", size=28)]},
    sources=["cfo", "supp"])
stage("s31_supply", "m4_supply", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("All its commitments"), "x": 1200, "y": 520, "zoom": 1.05, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="4 · THE SUPPLY BET PAYS OFF", at=0.2, size=52, color="gold"),
              it("counter", x=750, y=250, at=0.3, prefix="$", suffix="BN", decimals=0, steps=[[0, 279], [{"cue": "a quarter earlier"}, 390]], text="SUPPLY COMMITMENTS (MOSTLY MEMORY)"),
              it("ramstick", x=1450, y=280, at=C("mostly memory"), scale=0.9),
              it("sign", x=1000, y=440, text="ALL COMMITMENTS $518BN", at=C("All its commitments"), color="#FFE0B2", size=32),
              it("sign", x=1000, y=540, text="≈ 1.4× REVENUE OF THE LAST 12 MONTHS (OUR CALC.)", at=C("By our math"), color="#BBDEFB", size=26),
              ship(kind="cargo", x=[[0, 200], [12, 1400]], y=780, scale=0.7),
              buddy(1750, 860, at=0.4, mood="happy", moods=[[C("Heavy if"), "worry"]], label="NVDA", hop=14)]},
    sources=["cfo"])
kinetic("s32_t4", "m4_transition", [("Now the other side", 76, "Now the other side", None, False),
                                    ("of the scale", 76, "of the scale", "gold", False)])

# ====================================================================== PART 5: risks and upside
card("s33_c5", "m5_card", "Risks and Upside", "What Nvidia itself discloses")
stage("s34_leadership", "m5_leadership", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And in its results"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 2,
    "items": [it("letters", x=1000, y=100, text="RISK 1 · LEADERSHIP", at=0.2, size=58, color="gold"),
              it("emptychair", x=500, y=880, at=0.3, scale=0.9, text="CEO SEARCH UNDER WAY"),
              it("sign", x=1250, y=230, text="INTERIM CEO + CFO: COLETTE KRESS", at=C("Colette Kress"), color="#BBDEFB", size=28),
              it("sign", x=1250, y=330, text="SEARCH: INTERNAL + EXTERNAL", at=C("the board is searching"), color="#C8E6C9", size=28),
              it("sign", x=1250, y=430, text="FIRST BOARD CHAIR: HARVEY JONES", at=C("Harvey Jones"), color="#FFE0B2", size=28),
              it("sign", x=1250, y=530, text="REASON: NOT GIVEN IN THE FILING", at=C("doesn't give a reason"), color="#F5F5F5", size=26),
              it("sign", x=1250, y=640, text="LISTED RISK: BOARD COMMITTEE INVESTIGATION (NO DETAILS)", at=C("an ongoing investigation"), color="#FFCDD2", size=22)]},
    sources=["ceo8k", "pr"])
stage("s35_china", "m5_china", {
    "zones": [Z("port")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("But its outlook"), "x": 1250, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="RISK 2 · CHINA", at=0.2, size=58, color="gold"),
              it("sign", x=700, y=250, text="Q3: $2.4BN OF HOPPER CHIPS SHIPPED", at=C("older Hopper"), color="#BBDEFB", size=30),
              it("sign", x=1300, y=360, text="Q4 OUTLOOK ASSUMES $0", at=C("But its outlook"), color="#FFCDD2", size=34),
              it("letters", x=1000, y=520, text="A SWING FACTOR, BOTH WAYS", at=C("So China is a swing factor"), size=44, color="gold"),
              ship(kind="cargo", x=[[0, 200], [10, 1300]], y=780, scale=0.7)]},
    sources=["cfo", "pr"])
stage("s36_bets", "m5_bets", {
    "zones": [Z("dccity", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.05}, {"at": C("In a slowdown"), "x": 1150, "y": 520, "zoom": 1.0, "dur": 1.8}], "drift": 3,
    "items": [it("letters", x=1000, y=100, text="RISK 3 · THE WEB OF BETS", at=0.2, size=56, color="gold"),
              it("sign", x=550, y=250, text="STAKES ≈ $110BN", at=C("Stakes of"), color="#BBDEFB", size=30),
              it("sign", x=1000, y=250, text="GUARANTEES ≤ $118BN", at=C("guarantees"), color="#FFE0B2", size=30),
              it("sign", x=1450, y=250, text="CUSTOMERS = PARTNERS", at=C("customers that are also partners"), color="#E1BEE7", size=30),
              it("letters", x=1000, y=430, text="LOOPS WORK BOTH WAYS", at=C("In a slowdown"), size=48, color="gold"),
              buddy(1000, 860, at=0.4, mood="cool", moods=[[C("In a slowdown"), "worry"]], label="NVDA", hop=14)]},
    sources=["pr", "cfo"])
stage("s37_scale", "m5_upside", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("None of that"), "x": 960, "y": 500, "zoom": 1.05, "dur": 2.0}], "drift": 2,
    "items": [scale([("LEADERSHIP · CEO SEARCH", 0.3), ("CHINA: $0 IN THE OUTLOOK", 0.9), ("STAKES · GUARANTEES · CREDIT", 1.5)],
                    [("VERA CPUS SOLD ALONE", C("Vera")), ("HUGGING FACE (PENDING)", C("Hugging")), ("EDGE +42% · REVENUE SHARE", C("Edge computing grew"))],
                    title="RISKS VS UPSIDE (NVIDIA'S OWN WORDS)", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="UPSIDE IS UNSIZED: NO NUMBERS GIVEN", at=C("None of that"), color="#C8E6C9", size=28)]},
    sources=["pr", "cfo"])
kinetic("s38_t5", "m5_transition", [("So, what should you watch?", 76, "what should you watch", "gold", False)])

# ====================================================================== PAYOFF
board("p39_watch", "payoff", "3 numbers to watch (next report)", C("One, revenue"), [
    {"d": rect(1320, 440, 250, 140), "color": "accent", "width": 6, "kind": "box", "start": C("One, revenue"), "label": lbl("NEXT REPORT", 1445, 518, 22, "accent")},
    {"d": rect(700, 300, 440, 110), "color": "accent2", "width": 5, "kind": "box", "start": C("One, revenue"), "label": lbl("Q4 REVENUE", 920, 362, 20, "accent2")},
    {"d": "M 720 428 L 1120 428", "color": "ink", "width": 1, "start": C("One, revenue", 0.3), "label": lbl("VS $130BN ± 3% (EXTRA WEEK)", 920, 450, 14, "ink")},
    {"d": arrow((1150, 355), (1310, 462), 0.08), "color": "accent2", "width": 5, "kind": "arrow", "start": C("One, revenue", 0.6)},
    {"d": rect(700, 470, 440, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("Two, gross margin"), "label": lbl("GROSS MARGIN", 920, 532, 20, "accent3")},
    {"d": "M 720 598 L 1120 598", "color": "ink", "width": 1, "start": C("Two, gross margin", 0.3), "label": lbl("VS 71–72% OUTLOOK", 920, 620, 14, "ink")},
    {"d": arrow((1150, 525), (1310, 505), 0.08), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Two, gross margin", 0.6)},
    {"d": rect(700, 640, 440, 110), "color": "risk", "width": 5, "kind": "box", "start": C("Three, the days"), "label": lbl("DAYS TO GET PAID", 920, 702, 20, "risk")},
    {"d": "M 720 768 L 1120 768", "color": "ink", "width": 1, "start": C("Three, the days", 0.3), "label": lbl("VS 64 DAYS IN Q3", 920, 790, 14, "ink")},
    {"d": arrow((1150, 695), (1310, 547), 0.08), "color": "risk", "width": 5, "kind": "arrow", "start": C("Three, the days", 0.6)},
], C("Three, the days", 0.5), [1445, 510], sources=["pr", "cfo"])
stage("s40_edition", "payoff2", {
    "zones": [machine([(l, v, c, None) for l, v, c, _ in SEGS], "THE NVIDIA MACHINE", "PROFIT", ["SEE YOU NEXT QUARTER", "NEW NUMBERS · SAME QUESTIONS", "EDITION: NOV 2026", "UPDATED EVERY QUARTER"])], "worldW": 2600,
    "cam": [{"at": 0, "x": 1300, "y": 520, "zoom": 1.0}, {"at": 2.0, "x": 1100, "y": 540, "zoom": 1.05, "dur": 3.0}], "drift": 2,
    "items": [scorecard([("Q4 REVENUE", "VS $130BN ± 3% (EXTRA WEEK)", 0.4),
                         ("GROSS MARGIN", "VS 71–72% OUTLOOK", 1.0),
                         ("DAYS TO GET PAID", "VS 64 DAYS IN Q3", 1.6)], x=960, y=230, at=0.2, scale=0.82),
              stamp(1560, 930, at=0.6, scale=0.7),
              it("sign", x=760, y=925, text="PRICED IN? · WHAT HAS TO HAPPEN? · WHAT COULD GO WRONG?", at=C("the same three questions"), color="#BBDEFB", size=24)]},
    sources=["pr"])
add("s41_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_byb_nvidia_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Nvidia (Nov 2026 edition) storyboard; series kit from tools/byb_kit.py.\n")
