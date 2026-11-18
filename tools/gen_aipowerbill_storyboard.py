"""Generates projects/why-ai-could-make-your-electricity-bill-explode/deliverables/documentary/storyboard.yaml
(Episode 65: Why AI Could Make Your Electricity Bill Explode).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/powerbill.tsx (pbtown, bigbill, auction, gridbuild, hearing, plantdeal, gaugeroom,
pbtitle, pbbumper; items pbtag, billpaper, sparky). Cast: MAYA (a homeowner) and DEV (a utility lineworker), both fictional; no real
person is drawn; companies are named in narration and shown only as generic buildings with plain plaques.
Signature animations: 1 follow the $150 bill (p06 board + s07 bigbill), 2 the auction at the cap (s11-s12 auction), 3 who pays for
the wires (p17 board + s16 gridbuild + s18 study buckets), 4 the minimum-bill lock vs stranded costs (s21 hearing + p23 board),
5 the three dials (s28 gaugeroom). Presenter boards: p04 homes math, p06 the bill, p17 rate base, p23 stranded line.
Every number carries a pbtag pill: FACT / FORECAST / ESTIMATE (Market Monitor) / OUR CALC / ILLUSTRATIVE / DISCLOSED.
Run: python tools/gen_aipowerbill_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "why-ai-could-make-your-electricity-bill-explode"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#1E88E5", "#F5B700", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#14213D", "#F08A24"


def toon(x, at=0.0, **kw):
    return it("toon", x=x, at=at, **kw)


def MAYA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=2, skin=3, hair=0, hairStyle=1, color=TEAL, glasses=False, scarf=GOLD, **kw)


def DEV(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=1, skin=4, hair=1, hairStyle=2, color=ORANGE, glasses=True, scarf=NAVY, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def tag(*keys, at=0.0):
    return it("pbtag", at=at, x=36, y=36, tags=[[k[0], k[1]] for k in keys])


def bumper(id_, seg, act, title, caption, color):
    stage(id_, seg, {**W1("pbbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.2, "items": [it("sparky", x=[[0, 2300], [1.2, 1700]], y=1000, at=0.9, scale=0.7, hops=[2.2], face="happy")]},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 0.9, "gain": 0.3}])


# ====================================================================== CHAPTER 1: the power-hungry boom
stage("s01_hook", "co_hook", {
    **W1("pbtown", dc=[[0, 0.35], [C("Now look at"), 0.35], [C("Every AI answer"), 1.0]], zap=[[0, 0.0], [C("Every AI answer"), 0.0], [C("and they never sleep"), 1.0]],
         heat=[[0, 0.0], [C("and they never sleep"), 1.0]], flagAt=0.4, campusText="DATA CENTER CAMPUS"),
    "cam": cam((0, 260, 640, 1.45), (C("Now look at"), 900, 560, 1.0, 1.4), (C("Every AI answer"), 1700, 470, 1.05, 1.4),
               (C("This summer"), 960, 520, 0.82, WHIP), (C("Its own watchdog"), 1400, 500, 1.0, 1.2), (C("So who really pays"), 700, 560, 1.05, 1.4)), "drift": 3,
    "items": [it("billpaper", x=[[0, 300], [0.8, 330], [3.0, 420]], y=[[0, 650], [0.8, 480]], at=0.3, until=C("Now look at"), scale=1.1, amount="≈$150"),
              sign("TYPICAL VIRGINIA HOME · ≈$150 A MONTH (OUR CALC FROM VIRGINIA SCC FIGURES)", 300, 200, 0.5, color="#FFF8E1", size=24, until=C("Now look at")),
              sign("DATA CENTERS = 28% OF VIRGINIA POWER'S SALES (2025, DOMINION 10-K)", 1000, 180, C("data centers already buy"), color="#E1D5FF", size=26, until=C("Every AI answer")),
              words("THEY NEVER SLEEP", 1700, 150, C("and they never sleep"), size=58, until=C("This summer")),
              sign("PJM 2028/29 AUCTION: PRICE AT THE CAP · STILL 6,831 MW SHORT", 960, 160, C("This summer"), color="#FFCDD2", size=30, until=C("Its own watchdog")),
              sign("MARKET MONITOR ESTIMATE: $6.3B OF $16.4B FROM DATA CENTER LOAD", 1400, 180, C("Its own watchdog"), color="#FFE0B2", size=28, until=C("So who really pays")),
              words("WHO PAYS FOR THE AI BOOM?", 700, 170, C("So who really pays"), size=60, color="#FFFFFF"),
              MAYA([[0, -300], [1.2, 120]], 0.0, face="happy", pose="stand", hold="card", faces=[[0, "happy"], [C("Its own watchdog"), "shock"], [C("The tech giants"), "worry"]],
                   label="MAYA · HOMEOWNER", labelUntil=C("Now look at")),
              tag((0, "FACT · OUR CALC"), (C("data centers already buy"), "FACT"), (C("Its own watchdog"), "ESTIMATE · MARKET MONITOR"))]},
    sources=["scc_dom", "dom_10k25", "pjm_bra2829", "imm_0728"], sfx=[{"kind": "hit", "cue": "This summer", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("pbtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [it("sparky", x=[[0, 2200], [2.6, 1650]], y=1060, at=2.2, scale=0.8, hops=[3.6], face="shock")]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_machines", "c1_machines", {
    **W1("pbtown", dc=[[0, 0.2], [C("measured it"), 0.2], [C("Their"), 1.0]], cranes=True, zap=1.0, heat=[[0, 0.3], [C("and heat"), 1.0]], campusText="DATA CENTERS"),
    "cam": cam((0, 1750, 470, 1.15), (C("chips turn electricity"), 1900, 420, 1.45, 1.4), (C("Researchers at"), 1500, 500, 0.95, 1.4),
               (C("Their"), 1700, 480, 0.85, 1.6), (C("That's a forecast"), 1500, 500, 1.0, 1.2)), "drift": 3,
    "items": [words("WAREHOUSES OF CHIPS", 1750, 160, 0.3, size=54, until=C("and heat")),
              words("ELECTRICITY → ANSWERS + HEAT", 1900, 150, C("and heat"), size=44, until=C("Researchers at")),
              it("counter", x=1500, y=230, at=C("American data"), suffix=" TWh", decimals=0, steps=[[0, 0], [C("American data"), 58], [C("by twenty twenty-three"), 176]],
                 text="U.S. DATA CENTER ELECTRICITY USE (DOE / LBNL)", until=C("Their")),
              sign("2014: 58 TWh → 2023: 176 TWh (4.4% OF U.S. POWER)", 1500, 360, C("by twenty twenty-three"), color="#C8E6C9", size=28, until=C("Their")),
              sign("2028 FORECAST: 325-580 TWh", 1700, 190, C("Their"), color="#E1D5FF", size=40),
              words("A WIDE FORECAST", 1700, 300, C("That's a forecast"), size=46, color="#FFFFFF"),
              DEV(1050, 0.4, face="happy", pose="point", label="DEV · LINEWORKER", labelUntil=C("Researchers at"), faces=[[0, "happy"], [C("Their"), "shock"]]),
              tag((0, "FACT"), (C("Their"), "FORECAST · DOE / LBNL"))]},
    sources=["doe_lbnl"])
add("p04_homes", "c1_draw", "engine_draw", {
    "title": "How many homes is that? (our calculation)", "board": BOARD, "draw_start": C("Let me make that"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 840 L 1500 840", "color": "ink", "width": 5, "start": C("Let me make that")},
        {"d": rect(640, 300, 260, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("An average American home"), "label": lbl("1 HOME ≈ 863 kWh/MONTH", 770, 365, 20, "accent2")},
        {"d": dot(770, 440), "color": "muted", "width": 1, "start": C("An average American home"), "label": lbl("EIA, 2024", 770, 445, 16, "muted")},
        {"d": "M 700 840 L 700 680 L 840 680 L 840 840 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.6, "kind": "bar", "start": C("Divide"), "label": lbl("2023 · ≈17M HOMES", 770, 662, 22, "accent2")},
        {"d": "M 920 840 L 920 600 L 1060 600 L 1060 840 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.5, "kind": "bar", "start": C("At the top"), "label": lbl("2028 LOW · ≈31M", 990, 582, 20, "accent")},
        {"d": "M 1140 840 L 1140 360 L 1280 360 L 1280 840 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.65, "kind": "bar", "start": C("At the top", 0.6), "label": lbl("2028 HIGH · ≈56M", 1210, 342, 22, "risk")},
        {"d": rect(1120, 250, 360, 70), "color": "risk", "width": 4, "kind": "box", "start": C("At the top", 1.2), "label": lbl("FORECAST RANGE", 1300, 295, 22, "risk")},
        {"d": rect(1320, 470, 230, 120), "color": "accent3", "width": 5, "kind": "box", "start": C("That's our arithmetic"), "label": lbl("OUR CALC", 1435, 540, 28, "accent3")},
        {"d": arrow((1320, 620), (1220, 700), 0.2), "color": "ink", "width": 5, "kind": "arrow", "start": C("It's like a new country")},
        {"d": dot(1060, 890), "color": "muted", "width": 1, "start": C("Let me make that"), "label": lbl("176 / 325 / 580 TWh (DOE/LBNL) ÷ 10,356 kWh PER HOME PER YEAR (EIA 2024) · OUR CALCULATION", 1060, 890, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Divide", 0.4), "dur": 1.4, "target": [770, 700]}, {"kind": "point", "at": C("At the top", 0.8), "dur": 1.4, "target": [1210, 420]},
                {"kind": "react", "at": C("It's like a new country")}],
    "scale": 0.86, "floor": 1040}, sources=["doe_lbnl", "eia_srp"])
stage("s05_forecast", "c1_forecast", {
    "zones": [Z("gaugeroom", x0=-1600, x1=1500, gauge=False, dialX=600,
                dials=[{"label": "PJM PEAK GROWTH / YEAR", "at": C("Grid operators"), "v": [[0, -0.8], [C("In twenty twenty-one"), -0.8], [C("Its newest forecast"), 0.9]], "l": "0.3% (2021)", "r": "3.6% (2026)"}]),
              Z("pbtown", x0=1500, x1=4600, dc=[[0, 0.4], [C("In Texas"), 1.0]], cranes=True, zap=1.0, campusText="NEW LARGE LOADS")],
    "worldW": 2400,
    "cam": cam((0, 600, 540, 1.0), (C("Its newest forecast"), 800, 520, 1.1, 1.2), (C("In Texas"), 3000, 480, 0.9, WHIP), (C("Some of these projects"), 3300, 520, 1.05, 1.4)), "drift": 3,
    "items": [words("PJM: 13 STATES + DC", 600, 330, 0.3, size=48, until=C("In Texas")),
              sign("SUMMER PEAK: 161 GW (2025) → ≈222 GW BY 2036", 800, 900, C("reaching"), color="#E1D5FF", size=30, until=C("In Texas")),
              sign("AEP TEXAS: LETTERS OF AGREEMENT FOR +36 GW BY 2030 (AEP 10-K)", 3000, 180, C("In Texas"), color="#FFE0B2", size=28),
              words("FORECASTS, NOT FACTS", 3300, 300, C("Again, these are forecasts"), size=50, color="#FFFFFF"),
              it("bubble", text="SOME WILL NEVER BE BUILT.", x=3100, y=420, at=C("Some of these projects"), tail=[2900, 650], size=30),
              DEV(2850, C("In Texas"), face="happy", pose="clipboard", hold="clipboard", faces=[[0, "happy"], [C("Some of these projects"), "worry"]]),
              tag((0, "FORECAST · PJM 2026"), (C("In Texas"), "FORECAST · AEP 10-K"))]},
    sources=["pjm_lf26", "aep_10k25"])

# ====================================================================== CHAPTER 2: follow the $150 bill
bumper("s06_b2", "c2_card", "CHAPTER TWO", "FOLLOW THE $150 BILL", "One household, four slices, one new neighbor.", TEAL)
add("p06_bill", "c2_bill", "engine_draw", {
    "title": "Follow one $150 bill (illustrative split)", "board": BOARD, "draw_start": C("So let's follow"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 470, 220, 130), "color": "risk", "width": 7, "kind": "box", "start": C("So let's follow"), "label": lbl("$150 BILL", 670, 545, 32, "risk")},
        {"d": dot(670, 630), "color": "muted", "width": 1, "start": C("for a thousand"), "label": lbl("1,000 kWh · TYPICAL VIRGINIA HOME", 670, 635, 16, "muted")},
        {"d": arrow((780, 520), (930, 330), -0.1), "color": "ink", "width": 5, "kind": "arrow", "start": C("Where does the money go")},
        {"d": rect(940, 280, 300, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("The biggest piece"), "label": lbl("ENERGY", 1090, 338, 30, "accent2")},
        {"d": arrow((780, 540), (930, 450), -0.05), "color": "ink", "width": 5, "kind": "arrow", "start": C("A slice pays for capacity")},
        {"d": rect(940, 410, 300, 90), "color": "accent", "width": 6, "kind": "box", "start": C("A slice pays for capacity"), "label": lbl("CAPACITY", 1090, 468, 30, "accent")},
        {"d": arrow((780, 560), (930, 580), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("Another slice")},
        {"d": rect(940, 540, 300, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("Another slice"), "label": lbl("TRANSMISSION", 1090, 598, 28, "accent3")},
        {"d": arrow((780, 580), (930, 710), 0.05), "color": "ink", "width": 5, "kind": "arrow", "start": C("The rest pays")},
        {"d": rect(940, 670, 300, 90), "color": "muted", "width": 6, "kind": "box", "start": C("The rest pays"), "label": lbl("DISTRIBUTION + FEES", 1090, 726, 24, "muted")},
        {"d": rect(1420, 450, 230, 130), "color": "risk", "width": 7, "kind": "box", "start": C("Data centers can push"), "label": lbl("DATA CENTERS", 1535, 525, 28, "risk")},
        {"d": arrow((1420, 480), (1250, 330), 0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("Data centers can push", 0.4)},
        {"d": arrow((1420, 500), (1250, 455), 0.1), "color": "risk", "width": 6, "kind": "arrow", "start": C("Data centers can push", 0.7)},
        {"d": arrow((1420, 540), (1250, 585), -0.1), "color": "risk", "width": 6, "kind": "arrow", "start": C("on every one", 0.0)},
        {"d": arrow((1420, 570), (1250, 715), -0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("on every one", 0.3)},
        {"d": dot(1060, 880), "color": "muted", "width": 1, "start": C("So let's follow"), "label": lbl("$150 ≈ $11.24 ÷ 7.5% (VIRGINIA SCC, NOV 2025) · OUR CALCULATION · SLICES SHOWN ARE ILLUSTRATIVE", 1060, 880, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("A slice pays for capacity", 0.4), "dur": 1.4, "target": [1090, 455]},
                {"kind": "point", "at": C("Data centers can push", 0.2), "dur": 1.6, "target": [1535, 515]}, {"kind": "react", "at": C("on every one", 0.6)}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom"])
SL = [{"label": "ENERGY", "v": 70, "color": BLUE, "at": 0.2}, {"label": "CAPACITY", "v": 18, "color": GOLD, "at": 0.5},
      {"label": "TRANSMISSION", "v": 22, "color": GREEN, "at": 0.8}, {"label": "DISTRIBUTION + FEES", "v": 40, "color": "#8E9AAF", "at": 1.1}]
stage("s07_energy", "c2_energy", {
    **W1("bigbill", billX=1230, slices=SL, illus="ILLUSTRATIVE SPLIT · NOT A REAL BILL", hi=[[0, None]],
         push=[{"label": "ENERGY", "at": C("up about"), "dv": 30, "text": "+50% WHOLESALE"}, {"label": "CAPACITY", "at": C("But the capacity piece"), "dv": 40, "text": "×3 CAPACITY"}],
         stamp=[[C("A brutal winter storm"), "STORM"]]),
    "cam": cam((0, 1100, 560, 0.95), (C("PJM's independent"), 1000, 520, 1.1, 1.4), (C("up about"), 1150, 520, 1.2, 1.2), (C("But the capacity piece"), 1100, 640, 1.35, 1.2)), "drift": 3,
    "items": [it("counter", x=430, y=250, at=C("the all-in wholesale cost"), prefix="$", decimals=2, steps=[[0, 0], [C("the all-in wholesale cost"), 76.16], [C("up about"), 114.50]],
                 text="PJM WHOLESALE $/MWh, JAN-JUN"),
              sign("2025: $76.16 → 2026: $114.50", 430, 400, C("up about"), color="#FFE0B2", size=26),
              sign("CAPACITY COSTS: +207%", 430, 500, C("But the capacity piece"), color="#FFCDD2", size=34),
              MAYA(1700, 0.3, face="worry", pose="stand", hold="coffee", faces=[[0, "worry"], [C("But the capacity piece"), "shock"]]),
              tag((0, "FACT · MARKET MONITOR"))]},
    sources=["imm_0728"])
stage("s08_eleven", "c2_eleven", {
    **W1("bigbill", billX=1230, slices=[{**s, "at": 0} for s in SL], illus="OUR ILLUSTRATION · IF FULLY PASSED THROUGH",
         push=[{"label": "CAPACITY", "at": C("Its estimate is"), "dv": 30, "text": "≈ $11 / MONTH?"}],
         totals=[[0, "$150"], [C("that's"), "$150 + ≈$11?"]], stamp=[[C("But the order of magnitude"), "NOT PENNIES"]]),
    "cam": cam((0, 1100, 600, 1.2), (C("Its estimate is"), 1000, 560, 1.05, 1.2), (C("Now, a thousand"), 1150, 300, 1.25, 1.4), (C("It isn't always"), 1100, 560, 1.0, 1.2)), "drift": 3,
    "items": [words("WITHOUT DATA CENTERS?", 430, 220, 0.3, size=48, until=C("Its estimate is")),
              sign("MONITOR: $11.11/MWh FROM DATA CENTERS", 430, 220, C("Its estimate is"), color="#FFE0B2", size=24),
              sign("1,000 kWh = 1 MWh", 430, 330, C("Now, a thousand"), color="#C8E6C9", size=40),
              sign("1 MWh × $11.11 ≈ $11 / MONTH", 430, 430, C("So if every cent"), color="#FFF59D", size=34),
              sign("PASS-THROUGH VARIES", 430, 530, C("It isn't always"), color="#E1D5FF", size=26),
              MAYA(1750, 0.2, face="shock", pose="stand", hold="card", faces=[[0, "shock"], [C("It isn't always"), "worry"]]),
              tag((0, "ESTIMATE · MARKET MONITOR"), (C("So if every cent"), "OUR CALC · ILLUSTRATIVE"))]},
    sources=["imm_0728"])
stage("s09_link", "c2_link", {
    **W1("pbtown", dc=1.0, zap=1.0, heat=0.6),
    "cam": cam((0, 300, 600, 1.2), (C("Here's what happened next"), 1500, 500, 0.95, 1.4)), "drift": 3,
    "items": [sign("WATCH: WHY AMERICA'S ELECTRICITY BILLS ARE RISING", 400, 200, 0.4, color="#FFFFFF", size=30, until=C("Here's what happened next")),
              words("WHAT HAPPENED NEXT...", 1500, 160, C("Here's what happened next"), size=56),
              MAYA(200, 0.2, face="happy", pose="point"), DEV(520, 0.4, face="happy", pose="wave"), tag((0, "LIBRARY"))]})

# ====================================================================== CHAPTER 3: the auction at the cap
bumper("s10_b3", "c3_card", "CHAPTER THREE", "THE AUCTION AT THE CAP", "Paying power plants to promise.", PURPLE)
stage("s11_auction", "c3_auction", {
    **W1("auction", prices=[[0, "—"], [C("For the delivery year"), "$28.92"], [C("it cleared at"), "$325"]], capAt=C("That's the maximum"), capText="CAP · $325",
         gavel=[C("it cleared at", 0.2), C("The total", 0.3)], supply=0.55, demand=[[0, 0.4], [C("This July"), 0.4], [C("it cleared at"), 0.85]],
         board="CAPACITY PRICE · $ PER MEGAWATT-DAY · PJM"),
    "cam": cam((0, 960, 480, 1.1), (C("For the delivery year"), 960, 300, 1.35, 1.2), (C("This July"), 960, 540, 0.95, 1.4), (C("That's the maximum"), 960, 360, 1.2, 1.2),
               (C("The total"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [sign("DELIVERY YEAR 2024/25", 960, 990, C("For the delivery year"), color="#FFF8E1", size=28, until=C("This July")),
              sign("DELIVERY YEAR 2028/29 (AUCTION: JULY 2026)", 960, 990, C("This July"), color="#E1D5FF", size=26, until=C("That's the maximum")),
              sign("CAP AGREED WITH THE GOVERNORS OF 13 STATES", 960, 990, C("That's the maximum"), color="#FFCDD2", size=26, until=C("The total")),
              sign("CLEARED SUPPLY × PRICE ≈ $16.4 BILLION", 960, 1040, C("The total"), color="#FFF59D", size=34),
              tag((0, "FACT · PJM"))]},
    sources=["pjm_bra2829", "pjm_bra2425"], sfx=[{"kind": "hit", "cue": "it cleared at", "gain": 0.35}])
stage("s12_short", "c3_short", {
    **W1("auction", prices=[[0, "$325"]], capAt=0.0, capText="CAP · $325", supply=[[0, 0.55], [C("Only"), 0.6]], demand=0.9,
         shortAt=C("short of what"), shortText="6,831 MW SHORT", gavel=[C("And even at the cap", 0.1)]),
    "cam": cam((0, 960, 540, 0.95), (C("short of what"), 1300, 480, 1.15, 1.2), (C("The last two auctions"), 960, 520, 1.0, 1.2), (C("Only"), 600, 640, 1.25, 1.2),
               (C("Demand is arriving"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("EVEN AT THE CAP...", 960, 990, 0.2, size=54, until=C("short of what")),
              sign("FIRST TIME IN PJM HISTORY: WHOLE GRID SHORT, TWO AUCTIONS IN A ROW", 960, 990, C("The last two auctions"), color="#FFCDD2", size=26, until=C("Only")),
              sign("NEW PLANTS + UPGRADES CLEARED: 525 MW", 960, 990, C("Only"), color="#FFE0B2", size=30, until=C("Demand is arriving")),
              words("DEMAND > STEEL AND CONCRETE", 960, 990, C("Demand is arriving"), size=48),
              tag((0, "FACT · PJM"))]},
    sources=["pjm_bra2829"], sfx=[{"kind": "hit", "cue": "short of what", "gain": 0.3}])
stage("s13_monitor", "c3_monitor", {
    **W1("gridbuild", build=1.0, cost=[[0, ""], [C("The market monitor"), "$6.3B OF $16.4B"], [C("Over the last four"), "$29.4B · 46%"], [C("In the forecasts"), "8 GW → 21.5 GW"]],
         costTitle="DATA CENTER SHARE (MARKET MONITOR ESTIMATE)",
         split=[{"who": "HOMES", "v": [[0, 0.0], [C("And capacity costs are shared"), 0.0], [C("Including you"), 0.6]]},
                {"who": "SHOPS", "v": [[0, 0.0], [C("And capacity costs are shared"), 0.0], [C("Including you"), 0.45]]},
                {"who": "FACTORIES", "v": [[0, 0.0], [C("And capacity costs are shared"), 0.0], [C("Including you"), 0.5]]},
                {"who": "DATA CENTERS", "v": [[0, 0.0], [C("And capacity costs are shared"), 0.0], [C("Including you"), 0.55]]}],
         hi=None),
    "cam": cam((0, 520, 400, 1.15), (C("Over the last four"), 520, 360, 1.25, 1.2), (C("In the forecasts"), 700, 420, 1.1, 1.2), (C("And capacity costs are shared"), 1640, 620, 1.05, 1.4)), "drift": 3,
    "items": [sign("2028/29: ≈38% OF THE AUCTION'S COST", 560, 310, C("about thirty-eight"), color="#FFE0B2", size=30, until=C("Over the last four")),
              sign("LAST FOUR AUCTIONS: ALMOST HALF", 560, 310, C("Almost half"), color="#FFCDD2", size=32, until=C("In the forecasts")),
              sign("DC LOAD IN PJM FORECAST: 7,927 → 21,470 MW", 560, 310, C("In the forecasts"), color="#E1D5FF", size=26, until=C("And capacity costs are shared")),
              words("SHARED BY EVERYONE AT THE PEAK", 1300, 380, C("And capacity costs are shared"), size=46),
              MAYA(1000, C("Including you", -0.6), face="shock", pose="stand", scale=1.0),
              tag((0, "ESTIMATE · MARKET MONITOR"), (C("And capacity costs are shared"), "MECHANISM"))]},
    sources=["imm_0728"])
stage("s14_fix", "c3_fix", {
    **W1("auction", prices=[[0, "WHO PAYS?"]], capAt=0.0, capText="CAP", supply=0.55, demand=[[0, 0.9], [C("Take data centers out"), 0.45]],
         gavel=[C("Who pays", 0.1)], board="THE OPEN QUESTION"),
    "cam": cam((0, 960, 600, 0.95), (C("Take data centers out"), 1300, 520, 1.1, 1.2), (C("PJM is trying"), 960, 520, 1.0, 1.2), (C("Who pays"), 960, 280, 1.3, WHIP)), "drift": 2,
    "items": [sign("MONITOR: A SEPARATE AUCTION FOR DATA CENTERS", 960, 990, C("Take data centers out"), color="#FFE0B2", size=28, until=C("PJM is trying")),
              sign("PJM: CONNECT, BUT CUT BACK WHEN THE GRID IS STRESSED", 960, 990, C("PJM is trying"), color="#BBDEFB", size=28, until=C("None of it")),
              words("UNSETTLED", 960, 940, C("None of it"), size=64),
              tag((0, "PROPOSALS · NOT RULES"))]},
    sources=["imm_0728", "pjm_bra2829"])

# ====================================================================== CHAPTER 4: who pays for the wires
bumper("s15_b4", "c4_card", "CHAPTER FOUR", "WHO PAYS FOR THE WIRES", "Billions in steel, split among us all.", GREEN)
stage("s16_capex", "c4_capex", {
    **W1("gridbuild", build=[[0, 0.0], [C("Utilities are planning"), 0.1], [C("Both point"), 1.0]],
         cost=[[0, ""], [C("Dominion Energy plans"), "DOMINION: $65.7B"], [C("AEP plans"), "AEP: ≈ $71.9B"]], costTitle="PLANNED SPENDING 2026-2030 (2025 10-Ks)"),
    "cam": cam((0, 300, 560, 1.1), (C("Dominion Energy plans"), 520, 420, 1.15, 1.2), (C("AEP plans"), 600, 480, 1.0, 1.2), (C("Both point"), 900, 540, 0.85, 1.6)), "drift": 4,
    "items": [words("A BUILDING SPREE", 300, 360, 0.3, size=56, until=C("Dominion Energy plans")),
              sign("AEP: $12.2B (2026) + $59.7B (2027-30) · OUR SUM", 600, 330, C("AEP plans"), color="#FFF8E1", size=24, until=C("Both point")),
              sign("REASON GIVEN: LARGE NEW LOADS, ABOVE ALL DATA CENTERS", 900, 300, C("Both point"), color="#E1D5FF", size=28),
              DEV(1000, 0.3, face="happy", pose="point", faces=[[0, "happy"], [C("Both point"), "worry"]]),
              tag((0, "FACT · 10-K PLANS"))]},
    sources=["dom_10k25", "aep_10k25"])
add("p17_rate", "c4_rate", "engine_draw", {
    "title": "How building more becomes your bill", "board": BOARD, "draw_start": C("Let me draw it"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 300, 240, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("A regulated utility"), "label": lbl("BUILD", 680, 368, 34, "accent2")},
        {"d": arrow((800, 355), (930, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("earns a return")},
        {"d": rect(940, 300, 260, 110), "color": "accent", "width": 6, "kind": "box", "start": C("earns a return"), "label": lbl("RATE BASE", 1070, 368, 32, "accent")},
        {"d": arrow((1200, 355), (1330, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("In Virginia")},
        {"d": rect(1340, 300, 220, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("In Virginia"), "label": lbl("ROE 9.8%", 1450, 368, 32, "accent3")},
        {"d": arrow((1450, 410), (690, 300), -0.35), "color": "risk", "width": 5, "kind": "arrow", "start": C("Build more")},
        {"d": arrow((1070, 410), (1070, 520), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("Then the cost is split")},
        {"d": rect(560, 540, 210, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Homes"), "label": lbl("HOMES", 665, 598, 26, "accent2")},
        {"d": rect(800, 540, 210, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("shops"), "label": lbl("SHOPS", 905, 598, 26, "accent3")},
        {"d": rect(1040, 540, 210, 90), "color": "accent", "width": 5, "kind": "box", "start": C("factories"), "label": lbl("FACTORIES", 1145, 598, 24, "accent")},
        {"d": rect(1280, 540, 260, 90), "color": "risk", "width": 5, "kind": "box", "start": C("data centers."), "label": lbl("DATA CENTERS", 1410, 598, 24, "risk")},
        {"d": rect(760, 690, 600, 90), "color": "ink", "width": 5, "kind": "box", "start": C("How it's split"), "label": lbl("THE SPLIT = A REGULATOR'S CHOICE", 1060, 748, 26, "ink")},
        {"d": dot(1060, 830), "color": "muted", "width": 1, "start": C("like each group's"), "label": lbl("e.g. EACH CLASS'S SHARE OF THE PEAK", 1060, 835, 20, "muted")},
        {"d": dot(1060, 890), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("MECHANISM · ROE: VIRGINIA SCC FINAL ORDER PUR-2025-00058 (NOV 2025) · SEE ALSO: WHY AMERICA'S ELECTRICITY BILLS ARE RISING", 1060, 890, 14, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Build more", 0.3), "dur": 1.4, "target": [1070, 355]}, {"kind": "point", "at": C("How it's split", 0.3), "dur": 1.6, "target": [1060, 735]}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom"])
stage("s18_study", "c4_study", {
    **W1("gridbuild", build=1.0, cost=[[0, ""], [C("On transmission"), "DATA-CENTER CLASS: 3.01%"], [C("Other large customers"), "OTHER BIG USERS: 22.41%"]],
         costTitle="RETURN EARNED ON TRANSMISSION (DOMINION COST STUDY, 2024)",
         split=[{"who": "HOMES", "v": 0.6}, {"who": "SHOPS", "v": 0.5}, {"who": "FACTORIES", "v": [[0, 0.5], [C("Other large customers"), 0.85]]},
                {"who": "DATA CENTERS", "v": [[0, 0.5], [C("On transmission"), 0.12]]}],
         hi=None),
    "cam": cam((0, 1640, 560, 1.0), (C("On transmission"), 520, 380, 1.15, 1.2), (C("In plain English"), 1640, 600, 1.05, 1.4), (C("The commission says"), 1200, 540, 0.9, 1.4)), "drift": 3,
    "items": [words("VIRGINIA'S OWN NUMBERS", 1300, 380, 0.3, size=50, until=C("On transmission")),
              words("BIGGEST USERS, SMALL SHARE OF THE BIG LINES", 1300, 380, C("In plain English"), size=40, until=C("The commission says")),
              sign("COMMISSION: TRANSMISSION SPLIT TO BE EXAMINED NEXT", 1200, 200, C("The commission says"), color="#C8E6C9", size=30),
              tag((0, "FACT · VIRGINIA SCC ORDER"))]},
    sources=["scc_dom"])
stage("s19_bill", "c4_bill", {
    **W1("bigbill", billX=1230, slices=[{**s, "at": 0} for s in SL], illus="ILLUSTRATIVE SPLIT", totals=[[0, "$150"], [C("A typical home pays"), "+$11.24"]],
         push=[{"label": "DISTRIBUTION + FEES", "at": C("A typical home pays"), "dv": 22, "text": "BASE RATES +7.5%"}],
         stamp=[[C("On the monthly bill"), "YOUR BILL"]]),
    "cam": cam((0, 1100, 560, 1.0), (C("A typical home pays"), 1300, 300, 1.25, 1.2), (C("Not all of it"), 1100, 560, 0.95, 1.4), (C("On the monthly bill"), 1200, 620, 1.2, 1.0)), "drift": 3,
    "items": [sign("TYPICAL HOME: +$11.24/MONTH (2026)", 430, 230, C("A typical home pays"), color="#FFE0B2", size=24),
              sign("NOT ALL DATA CENTERS", 430, 330, C("Not all of it"), color="#E1D5FF", size=24),
              MAYA(1750, 0.3, face="worry", pose="shrug", faces=[[0, "worry"], [C("On the monthly bill"), "shock"]]),
              tag((0, "FACT · VIRGINIA SCC ORDER"))]},
    sources=["scc_dom"])

# ====================================================================== CHAPTER 5: the fightback
bumper("s20_b5", "c5_card", "CHAPTER FIVE", "THE FIGHTBACK", "Minimum bills, long contracts, big checks.", ORANGE)
stage("s21_ohio", "c5_ohio", {
    **W1("hearing", bench="OHIO UTILITY COMMISSION", unroll=[[0, 0.0], [C("for up to"), 0.0], [C("Walk away early"), 1.0]], years=12, ramp=4, yearsText="UP TO 12 YEARS · RAMP ≤ 4",
         lockAt=C("must pay for at least"), lockText="85% MIN", lockX=1700),
    "cam": cam((0, 960, 460, 0.95), (C("must pay for at least"), 1500, 620, 1.1, 1.2), (C("for up to"), 1100, 760, 1.05, 1.2), (C("Walk away early"), 960, 560, 0.9, 1.2)), "drift": 2,
    "items": [sign("COLUMBUS AREA: NEW DATA CENTER AGREEMENTS PAUSED", 960, 140, 0.4, color="#FFE0B2", size=28, until=C("New data centers")),
              sign("25 MW+ DATA CENTERS PAY FOR ≥85% OF WHAT THEY RESERVE", 960, 140, C("New data centers"), color="#C8E6C9", size=28, until=C("Walk away early")),
              sign("EXIT FEE: 36 MONTHS OF MINIMUM CHARGES", 960, 140, C("Walk away early"), color="#FFCDD2", size=30),
              tag((0, "FACT · AEP OHIO TARIFF (PUCO, JUL 2025)"))]},
    sources=["aep_dct"])
stage("s22_gs5", "c5_gs5", {
    **W1("hearing", bench="VIRGINIA STATE CORPORATION COMMISSION", unroll=[[0, 0.0], [C("with"), 1.0]], years=14, ramp=4, yearsText="14-YEAR CONTRACTS (FROM 2027)",
         lockAt=C("They pay for at least"), lockText="85% / 60%", lockX=1720),
    "cam": cam((0, 960, 540, 0.95), (C("with"), 1100, 760, 1.05, 1.2), (C("They pay for at least"), 1600, 640, 1.15, 1.2), (C("Dominion says"), 960, 520, 0.9, 1.4)), "drift": 2,
    "items": [sign("NEW CLASS GS-5: 25 MW+, RUNNING ≥75% OF THE TIME", 960, 140, 0.4, color="#E1D5FF", size=28, until=C("They pay for at least")),
              sign("MINIMUMS: 85% DISTRIBUTION · 85% TRANSMISSION · 60% GENERATION", 960, 140, C("They pay for at least"), color="#C8E6C9", size=26, until=C("Dominion says")),
              sign("GOAL: NO CROSS-SUBSIDY · NO STRANDED COSTS", 960, 140, C("Dominion says"), color="#BBDEFB", size=30),
              tag((0, "FACT · VIRGINIA SCC ORDER"))]},
    sources=["scc_dom", "dom_10k25"])
add("p23_strand", "c5_why", "engine_draw", {
    "title": "The line built for a data center that never comes", "board": BOARD, "draw_start": C("Picture a utility"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 300, 260, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("Picture a utility"), "label": lbl("NEW LINE BUILT", 690, 368, 26, "accent2")},
        {"d": arrow((820, 355), (960, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("for a data center")},
        {"d": rect(970, 300, 300, 110), "color": "risk", "width": 6, "kind": "box", "start": C("that never shows up"), "label": lbl("NO-SHOW / SHUTS DOWN", 1120, 368, 24, "risk")},
        {"d": arrow((1060, 410), (820, 540), 0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("Without a contract")},
        {"d": rect(560, 540, 360, 110), "color": "risk", "width": 6, "kind": "box", "start": C("Without a contract"), "label": lbl("EVERYONE'S RATES", 740, 608, 28, "risk")},
        {"d": dot(740, 690), "color": "risk", "width": 1, "start": C("for decades"), "label": lbl("FOR DECADES", 740, 700, 24, "risk")},
        {"d": arrow((1180, 410), (1380, 540), -0.15), "color": "accent3", "width": 5, "kind": "arrow", "start": C("With a minimum bill")},
        {"d": rect(1220, 540, 360, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("With a minimum bill"), "label": lbl("DATA CENTER PAYS", 1400, 608, 28, "accent3")},
        {"d": dot(1400, 690), "color": "accent3", "width": 1, "start": C("pays either way"), "label": lbl("EITHER WAY", 1400, 700, 24, "accent3")},
        {"d": rect(760, 760, 620, 80), "color": "accent", "width": 5, "kind": "box", "start": C("That one clause"), "label": lbl("ONE CLAUSE > ANY CHIP", 1070, 812, 30, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Without a contract", 0.3), "dur": 1.4, "target": [740, 595]}, {"kind": "point", "at": C("With a minimum bill", 0.3), "dur": 1.4, "target": [1400, 595]},
                {"kind": "react", "at": C("That one clause", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom", "aep_dct"])
stage("s24_deals", "c5_deals", {
    **W1("plantdeal", steam=[[0, 0.0], [C("Microsoft agreed"), 0.0], [C("the former Three Mile Island"), 1.0]], plantText="NUCLEAR PLANT (GENERIC)", campusText="DATA CENTERS",
         tags=[[0, ""], [C("Microsoft agreed"), "MICROSOFT · 835 MW · 20 YEARS · REACTOR RESTART"], [C("Meta signed"), "META · 1,121 MW · 20 YEARS · FROM 2027"],
               [C("Amazon contracted"), "AMAZON · 1,920 MW · THROUGH 2042"], [C("Some deals add"), "NEW POWER ≠ RESERVED POWER"]],
         shakeAt=C("They're signing"), shakeX=900),
    "cam": cam((0, 900, 560, 1.0), (C("Microsoft agreed"), 300, 520, 1.0, 1.4), (C("Meta signed"), 900, 520, 0.95, 1.2), (C("Amazon contracted"), 1300, 520, 1.0, 1.2),
               (C("Some deals add"), 960, 540, 0.85, 1.4)), "drift": 3,
    "items": [sign("WITHOUT RATEPAYER SUPPORT (CONSTELLATION)", 900, 300, C("without ratepayer support"), color="#C8E6C9", size=28, until=C("Amazon contracted")),
              DEV(1900, C("Some deals add"), face="happy", pose="point", scale=1.0),
              tag((0, "DISCLOSED DEALS"))]},
    sources=["ceg_crane", "ceg_clinton", "talen_amzn"])
stage("s25_counter", "c5_counter", {
    **W1("plantdeal", steam=1.0, supply=[[0, 0.0], [C("And new supply"), 0.0], [C("of new solar"), 1.0]], plantText="POWER PLANT", campusText="DATA CENTERS", tagX=[[0, 900], [C("More customers share"), 1300], [C("And new supply"), 2500], [C("Even PJM trimmed"), 1300]],
         tags=[[0, "LOAD GROWTH HAS TENDED TO PUSH PRICES DOWN"], [C("though it's unclear"), "...BUT IT'S UNCLEAR IF THAT HOLDS"], [C("And new supply"), "+≈72 GW SOLAR · +20 GW WIND (2026-27, EIA)"],
               [C("Even PJM trimmed"), "PJM TRIMMED ITS NEAR-TERM FORECAST"]]),
    "cam": cam((0, 900, 540, 0.9), (C("More customers share"), 1300, 560, 1.05, 1.2), (C("And new supply"), 2500, 520, 0.95, 1.4), (C("Even PJM trimmed"), 1300, 540, 0.9, 1.4)), "drift": 3,
    "items": [it("bubble", text="MORE USERS SHARE THE FIXED COST", x=1400, y=330, at=C("More customers share"), until=C("And new supply"), tail=[1450, 650], size=28),
              sign("2027 PEAK FORECAST CUT BY 3,735 MW", 1300, 300, C("Even PJM trimmed"), color="#E1D5FF", size=30),
              MAYA(600, 0.3, face="happy", pose="stand", faces=[[0, "worry"], [C("More customers share"), "happy"]]),
              tag((0, "FACT · LBNL / BRATTLE"), (C("And new supply"), "FORECAST · EIA"))]},
    sources=["lbnl_prices", "steo_nov26", "pjm_lf26"])

# ====================================================================== CHAPTER 6: will your bill explode?
bumper("s26_b6", "c6_card", "CHAPTER SIX", "WILL YOUR BILL EXPLODE?", "The national number, and the hot spots.", RED)
stage("s27_trend", "c6_trend", {
    **W1("gaugeroom", lo=15, hi=20, dec=1, gaugeX=760, needle=[[0, 10], [C("The average home paid"), 16.5], [C("cents in twenty twenty-five"), 17.2], [C("The forecast is"), 18.2], [C("next"), 18.7]],
         marks=[{"v": 16.5, "label": "2024", "at": C("The average home paid")}, {"v": 17.2, "label": "2025", "at": C("cents in twenty twenty-five")},
                {"v": 18.2, "label": "2026 F", "at": C("The forecast is"), "color": PURPLE}, {"v": 18.7, "label": "2027 F", "at": C("next"), "color": PURPLE}]),
    "cam": cam((0, 960, 540, 0.95), (C("The average home paid"), 800, 540, 1.1, 1.2), (C("That's"), 1300, 520, 1.0, 1.2), (C("Rising, but"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [words("WILL IT EXPLODE?", 1500, 300, 0.2, size=56, until=C("That's")),
              sign("U.S. AVERAGE RESIDENTIAL PRICE · EIA STEO (NOV 2026)", 1500, 420, 0.6, color="#FFFFFF", size=24),
              sign("2024 → 2027: ≈ +13% (OUR CALC)", 1500, 520, C("That's"), color="#FFF59D", size=34),
              words("RISING, NOT EXPLODING (NATIONALLY)", 1450, 650, C("Rising, but"), size=40),
              tag((0, "FACT · EIA"), (C("The forecast is"), "FORECAST · EIA"))]},
    sources=["steo_nov26"])
stage("s28_dials", "c6_dials", {
    **W1("gaugeroom", gauge=False, dialX=540,
         dials=[{"label": "1 · MINIMUM-BILL CONTRACTS", "at": C("One, do big"), "v": [[0, 0], [C("Turn all three"), 0.9], [C("Turn them the other way"), -0.9]], "l": "NONE", "r": "SIGNED"},
                {"label": "2 · NEW SUPPLY SPEED", "at": C("Two, does new"), "v": [[0, 0], [C("Turn all three"), 0.9], [C("Turn them the other way"), -0.9]], "l": "SLOW", "r": "FAST"},
                {"label": "3 · HOW SHARED LINES ARE SPLIT", "at": C("Three, how do"), "v": [[0, 0], [C("Turn all three"), 0.9], [C("Turn them the other way"), -0.9]], "l": "SPREAD", "r": "CAUSER PAYS"}]),
    "cam": cam((0, 960, 400, 1.1), (C("comes down to three dials"), 960, 540, 0.95, 1.2), (C("Turn all three"), 960, 560, 0.9, 1.0), (C("Turn them the other way"), 960, 560, 0.95, 0.6)), "drift": 2,
    "items": [words("AVERAGES HIDE HOT SPOTS", 960, 260, 0.2, size=52, until=C("comes down to three dials")),
              sign("CAPACITY + WIRES: THE SLICES THAT CAN JUMP", 960, 360, C("Where data centers cluster"), color="#FFCDD2", size=30, until=C("comes down to three dials")),
              words("GROWTH CAN SPREAD COSTS THINNER", 960, 300, C("Turn all three"), size=44, color=GREEN, until=C("Turn them the other way")),
              words("HOUSEHOLDS HELP PAY", 960, 300, C("Turn them the other way"), size=52, color=RED),
              it("sparky", x=[[0, 2300], [1.0, 1750]], y=1000, at=0.3, scale=0.8, face="happy", faces=[[0, "happy"], [C("Turn them the other way"), "shock"]], hops=[]),
              tag((0, "VERDICT · OUR FRAMEWORK"))]},
    sources=["scc_dom", "aep_dct", "pjm_bra2829", "lbnl_prices"])
stage("s29_close", "c6_close", {
    **W1("pbtown", dc=1.0, zap=1.0, heat=0.5, meter=1),
    "cam": cam((0, 1700, 480, 1.0), (C("It's measured in"), 1500, 500, 0.9, 1.4), (C("But who pays it"), 400, 560, 1.15, 1.6), (C("And that may be"), 300, 600, 1.35, 1.6)), "drift": 2,
    "items": [words("THE AI POWER BILL IS REAL", 1700, 150, 0.3, size=54, until=C("But who pays it")),
              words("WHO PAYS = AUCTION RULES + RATE CASES", 600, 160, C("It's decided in"), size=44, color="#FFFFFF"),
              it("billpaper", x=[[C("And that may be"), 600], [C("And that may be", 2.0), 420]], y=[[C("And that may be"), 300], [C("And that may be", 2.0), 520]], at=C("And that may be"), scale=1.0, amount="$?"),
              MAYA(160, C("But who pays it"), face="happy", pose="clipboard", hold="card"),
              tag((0, "VERDICT"))]})
add("s30_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s31_button", "button", {
    **W1("pbtown", dc=1.0, zap=1.0, heat=0.4),
    "cam": cam((0, 300, 600, 1.2), (3.0, 300, 600, 1.35, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [DEV(160, 0.0, face="grin", pose="stand", scale=1.1),
              it("bubble", text="SO THE DATA CENTER PAYS FOR ITS OWN WIRES?", x=300, y=260, at=0.6, until=2.8, tail=[200, 520], size=28),
              MAYA(460, 0.4, face="happy", pose="point", scale=1.1),
              it("bubble", text="IF THE CONTRACT SAYS SO.", x=460, y=300, at=2.9, tail=[460, 560], size=30),
              it("sparky", x=700, y=1000, at=3.4, scale=0.6, hops=[3.6, 4.6], face="happy")]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

TIGHT = {"bigbill", "auction", "hearing", "gaugeroom", "gridbuild"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = min(_k["zoom"], 1.0 if _z[0]["set"] in ("bigbill", "gridbuild") else 1.06)
            _k["x"] = 960 if _z[0]["set"] in ("bigbill", "gridbuild") else max(860, min(1060, _k["x"]))
            _k["y"] = max(500, min(580, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 1)
        if _z[0]["set"] in ("bigbill", "gridbuild"):
            for _i, _k in enumerate(_sc["params"].get("cam", [])):
                _k["zoom"] = 0.95 + 0.05 * (_i % 2)
                _k["y"] = 540 - 20 * (_i % 2)

write(OUT, "# GENERATED by tools/gen_aipowerbill_storyboard.py; edit the generator, not this file.\n"
           "# Episode 65 storyboard (Why AI Could Make Your Electricity Bill Explode): bespoke worlds in CartoonStage/powerbill.tsx.\n")

# ---- cue check: every {cue: ...} must occur in its segment's rendered narration
from hiddeneco.config import ProjectPaths  # noqa: E402
from hiddeneco.research.dossier import build_dossier  # noqa: E402
from hiddeneco.script import load_script, render_text  # noqa: E402
import re  # noqa: E402

paths = ProjectPaths(SLUG, ROOT)
dos = build_dossier(paths)
scr = load_script(OUT.parent)
nar = {s.id: re.sub(r"[^\w% ]", "", render_text(s.narration, dos).lower()) for s in scr.segments}
bad = []


def walk(o, seg):
    if isinstance(o, dict):
        if "cue" in o and isinstance(o["cue"], str):
            c = re.sub(r"[^\w% ]", "", o["cue"].lower())
            if " ".join(c.split()) not in " ".join(nar.get(seg, "").split()):
                bad.append((seg, o["cue"]))
        for v in o.values():
            walk(v, seg)
    elif isinstance(o, list):
        for v in o:
            walk(v, seg)


for sc in cartoon_kit.scenes:
    walk(sc, sc["segment"])
print("cue problems:", bad if bad else "none")
