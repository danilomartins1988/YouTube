"""Generates projects/why-ai-could-make-your-electricity-bill-explode/deliverables/documentary/storyboard.yaml
(Episode 65: Why AI Could Make Your Electricity Bill Explode).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/powerbill.tsx (pbtown, bigbill, auction, gridbuild, hearing, plantdeal, gaugeroom,
pbtitle, pbbumper; items pbtag, billpaper, sparky). Story over statistics: one protagonist (MAYA, a Virginia homeowner, fictional) follows her $150 bill; DEV (a lineworker) is the second voice. Cast is fictional; no real
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
    **W1("pbtown", dc=[[0, 0.3], [C("Now look"), 0.3], [C("Giant windowless buildings"), 1.0]], zap=[[0, 0.0], [C("humming day and night"), 0.0], [C("This summer"), 1.0]],
         heat=[[0, 0.0], [C("humming day and night"), 1.0]], flagAt=0.4, campusText="DATA CENTER CAMPUS"),
    "cam": cam((0, 260, 640, 1.45), (C("this is her electric bill"), 300, 600, 1.6, 1.0), (C("Now look"), 900, 560, 1.0, 1.4), (C("Giant windowless buildings"), 1700, 470, 1.05, 1.4),
               (C("This summer"), 960, 520, 0.82, WHIP), (C("The grid's own watchdog"), 1400, 500, 1.0, 1.2), (C("So who really pays"), 400, 580, 1.2, 1.4)), "drift": 3,
    "items": [it("billpaper", x=[[0, 330], [C("this is her electric bill"), 360]], y=[[0, 650], [C("this is her electric bill"), 470]], at=C("this is her electric bill"), until=C("Now look"), scale=1.2, amount="$150"),
              words("$150 A MONTH", 330, 200, C("About"), size=60, until=C("Now look")),
              words("THE NEW NEIGHBORS", 1700, 150, C("Giant windowless buildings"), size=56, until=C("This summer")),
              it("bubble", text="WHAT ARE THOSE?", x=520, y=330, at=C("Now look", 0.4), until=C("This summer"), tail=[300, 520], size=30),
              words("TOP PRICE... AND STILL SHORT", 960, 160, C("bought its future electricity"), size=50, color="#FFFFFF", until=C("The grid's own watchdog")),
              it("bubble", text="THE DATA CENTERS ARE A BIG REASON.", x=1400, y=200, at=C("The grid's own watchdog"), until=C("So who really pays"), tail=[1600, 420], size=28),
              words("WHO PAYS FOR THE AI BOOM?", 500, 170, C("So who really pays"), size=56, color="#FFFFFF"),
              MAYA([[0, -300], [1.2, 120]], 0.0, face="happy", pose="stand", hold="card", faces=[[0, "happy"], [C("Now look"), "shock"], [C("or Maya"), "worry"]],
                   label="MAYA · HOMEOWNER, VIRGINIA", labelUntil=C("Now look"), takes=[C("Now look", 0.2)]),
              tag((0, "OUR CALC FROM VIRGINIA SCC FIGURES"), (C("This summer"), "FACT · PJM"), (C("The grid's own watchdog"), "ESTIMATE · MARKET MONITOR"))]},
    sources=["scc_dom", "pjm_bra2829", "imm_0728"], sfx=[{"kind": "hit", "cue": "This summer", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("pbtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [it("sparky", x=[[0, 2200], [2.6, 1650]], y=1060, at=2.2, scale=0.8, hops=[3.6], face="shock")]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_machines", "c1_machines", {
    **W1("pbtown", dc=[[0, 0.2], [C("Government researchers"), 0.2], [C("And their forecast"), 1.0]], cranes=True, zap=1.0, heat=[[0, 0.3], [C("and heat"), 1.0]], campusText="DATA CENTERS"),
    "cam": cam((0, 1750, 470, 1.15), (C("turns electricity into answers"), 1900, 420, 1.45, 1.4), (C("Government researchers"), 1500, 500, 0.95, 1.4),
               (C("And their forecast"), 1700, 480, 0.85, 1.6)), "drift": 3,
    "items": [words("ELECTRICITY IN → ANSWERS + HEAT OUT", 1850, 150, C("turns electricity into answers"), size=44, until=C("Government researchers")),
              words("≈ 17 MILLION HOMES' WORTH", 1500, 170, C("already using"), size=58, until=C("And their forecast")),
              words("FORECAST: ×2 TO ×3 BY 2028", 1700, 170, C("And their forecast"), size=58, color="#FFFFFF"),
              DEV(1050, 0.4, face="happy", pose="point", label="DEV · LINEWORKER", labelUntil=C("Government researchers"), faces=[[0, "happy"], [C("And their forecast"), "shock"]], takes=[C("or even triple")]),
              tag((0, "FACT · DOE / LBNL"), (C("already using"), "OUR CALC"), (C("And their forecast"), "FORECAST · DOE / LBNL"))]},
    sources=["doe_lbnl", "eia_srp"])
stage("s03b_maya", "c1_maya", {
    **W1("pbtown", dc=1.0, zap=[[0, 0.3], [C("pulls power"), 1.0]], heat=0.6, meter=2),
    "cam": cam((0, 200, 600, 1.35), (C("Her kids use it"), 300, 560, 1.2, 1.2), (C("But every one"), 1200, 500, 0.9, 1.6), (C("pulls power"), 500, 560, 1.15, 1.4),
               (C("Which raises"), 960, 520, 0.9, 1.4)), "drift": 3,
    "items": [it("bubble", text="HOMEWORK HELP!", x=420, y=300, at=C("Her kids use it"), until=C("She uses it"), tail=[260, 520], size=30),
              it("bubble", text="WHAT'S FOR DINNER?", x=420, y=300, at=C("She uses it"), until=C("But every one"), tail=[260, 520], size=30),
              words("SAME GRID", 700, 180, C("pulls power"), size=64, until=C("Which raises")),
              words("WHO PAYS FOR THE GROWING?", 960, 170, C("who pays for the growing"), size=54, color="#FFFFFF"),
              MAYA(220, 0.0, face="happy", pose="stand", hold="phone", faces=[[0, "happy"], [C("Which raises"), "worry"]]),
              tag((0, "OUR STORY · ILLUSTRATIVE HOUSEHOLD"))]})
add("p04_homes", "c1_draw", "engine_draw", {
    "title": "A new country of homes (our calculation)", "board": BOARD, "draw_start": C("Let me draw it"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 700 840 L 1500 840", "color": "ink", "width": 5, "start": C("Let me draw it")},
        {"d": rect(1180, 300, 260, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("Each little house"), "label": lbl("1 HOME · 1 YEAR", 1310, 362, 26, "accent2")},
        {"d": "M 780 840 L 780 660 L 940 660 L 940 840 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.6, "kind": "bar", "start": C("Stack them up"), "label": lbl("TODAY · ≈17M HOMES", 860, 642, 22, "accent2")},
        {"d": "M 1040 840 L 1040 430 L 1200 430 L 1200 840 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.6, "kind": "bar", "start": C("Now add the forecast"), "label": lbl("2028 FORECAST · UP TO ≈56M", 1120, 412, 22, "risk")},
        {"d": rect(1260, 560, 230, 110), "color": "accent3", "width": 5, "kind": "box", "start": C("That's our arithmetic"), "label": lbl("OUR CALC", 1375, 625, 28, "accent3")},
        {"d": arrow((1260, 700), (1200, 760), 0.2), "color": "ink", "width": 5, "kind": "arrow", "start": C("It's like a whole new country")},
        {"d": dot(1100, 890), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("DOE/LBNL: 176 TWh (2023) · 325-580 TWh (2028 FORECAST) ÷ EIA AVERAGE HOME USE · OUR CALCULATION", 1100, 890, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Stack them up", 0.4), "dur": 1.4, "target": [860, 700]}, {"kind": "point", "at": C("Now add the forecast", 0.6), "dur": 1.4, "target": [1120, 520]},
                {"kind": "react", "at": C("It's like a whole new country")}],
    "scale": 0.86, "floor": 1040}, sources=["doe_lbnl", "eia_srp"])
stage("s05_forecast", "c1_forecast", {
    "zones": [Z("gaugeroom", x0=-1600, x1=1500, gauge=False, dialX=600,
                dials=[{"label": "PJM PEAK-DEMAND GROWTH", "at": C("Grid operators"), "v": [[0, -0.8], [C("A few years ago"), -0.8], [C("Now it expects"), 0.9]], "l": "BARELY", "r": "×12"}]),
              Z("pbtown", x0=1500, x1=4600, dc=[[0, 0.4], [C("These"), 1.0]], cranes=True, zap=1.0, campusText="NEW LARGE LOADS")],
    "worldW": 2400,
    "cam": cam((0, 600, 540, 1.0), (C("Now it expects"), 700, 520, 1.1, 1.2), (C("These"), 3000, 480, 0.9, WHIP), (C("Remember that"), 3300, 520, 1.05, 1.4)), "drift": 3,
    "items": [words("PJM: THE GRID FOR 13 STATES + DC", 600, 300, 0.3, size=44, until=C("Now it expects")),
              words("×12 FASTER GROWTH", 600, 300, C("Now it expects"), size=64, until=C("These")),
              words("FORECASTS, NOT FACTS", 3200, 170, C("These"), size=54, color="#FFFFFF"),
              it("bubble", text="SOME WILL NEVER BE BUILT.", x=3100, y=380, at=C("some of these projects"), tail=[2900, 650], size=30),
              DEV(2850, C("These"), face="happy", pose="clipboard", hold="clipboard", faces=[[0, "happy"], [C("Remember that"), "worry"]]),
              tag((0, "FORECAST · PJM 2026 · OUR CALC ×12"))]},
    sources=["pjm_lf26"])

# ====================================================================== CHAPTER 2: follow the $150 bill
bumper("s06_b2", "c2_card", "CHAPTER TWO", "FOLLOW THE $150 BILL", "One household, four slices, one new neighbor.", TEAL)
add("p06_bill", "c2_bill", "engine_draw", {
    "title": "Follow Maya's $150 bill (illustrative split)", "board": BOARD, "draw_start": C("So let's follow"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 470, 220, 130), "color": "risk", "width": 7, "kind": "box", "start": C("So let's follow"), "label": lbl("$150 BILL", 670, 545, 32, "risk")},
        {"d": arrow((780, 520), (930, 330), -0.1), "color": "ink", "width": 5, "kind": "arrow", "start": C("The biggest slice")},
        {"d": rect(940, 280, 300, 90), "color": "accent2", "width": 6, "kind": "box", "start": C("The biggest slice"), "label": lbl("ENERGY", 1090, 338, 30, "accent2")},
        {"d": arrow((780, 540), (930, 450), -0.05), "color": "ink", "width": 5, "kind": "arrow", "start": C("Another pays for capacity")},
        {"d": rect(940, 410, 300, 90), "color": "accent", "width": 6, "kind": "box", "start": C("Another pays for capacity"), "label": lbl("CAPACITY", 1090, 468, 30, "accent")},
        {"d": arrow((780, 560), (930, 580), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("Another pays for transmission")},
        {"d": rect(940, 540, 300, 90), "color": "accent3", "width": 6, "kind": "box", "start": C("Another pays for transmission"), "label": lbl("TRANSMISSION", 1090, 598, 28, "accent3")},
        {"d": arrow((780, 580), (930, 710), 0.05), "color": "ink", "width": 5, "kind": "arrow", "start": C("The rest pays")},
        {"d": rect(940, 670, 300, 90), "color": "muted", "width": 6, "kind": "box", "start": C("The rest pays"), "label": lbl("WIRES + FEES", 1090, 726, 28, "muted")},
        {"d": rect(1420, 450, 230, 130), "color": "risk", "width": 7, "kind": "box", "start": C("And data centers can push"), "label": lbl("DATA CENTERS", 1535, 525, 28, "risk")},
        {"d": arrow((1420, 480), (1250, 330), 0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("And data centers can push", 0.4)},
        {"d": arrow((1420, 500), (1250, 455), 0.1), "color": "risk", "width": 6, "kind": "arrow", "start": C("And data centers can push", 0.7)},
        {"d": arrow((1420, 540), (1250, 585), -0.1), "color": "risk", "width": 6, "kind": "arrow", "start": C("every one of those", 0.0)},
        {"d": arrow((1420, 570), (1250, 715), -0.15), "color": "risk", "width": 6, "kind": "arrow", "start": C("every one of those", 0.3)},
        {"d": dot(1060, 880), "color": "muted", "width": 1, "start": C("So let's follow"), "label": lbl("$150 ≈ TYPICAL 1,000 kWh VIRGINIA BILL, OUR CALCULATION FROM THE SCC ORDER · SLICES ARE ILLUSTRATIVE", 1060, 880, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Another pays for capacity", 0.4), "dur": 1.4, "target": [1090, 455]},
                {"kind": "point", "at": C("And data centers can push", 0.2), "dur": 1.6, "target": [1535, 515]}, {"kind": "react", "at": C("every one of those", 0.6)}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom"])
SL = [{"label": "ENERGY", "v": 70, "color": BLUE, "at": 0.2}, {"label": "CAPACITY", "v": 18, "color": GOLD, "at": 0.5},
      {"label": "TRANSMISSION", "v": 22, "color": GREEN, "at": 0.8}, {"label": "WIRES + FEES", "v": 40, "color": "#8E9AAF", "at": 1.1}]
stage("s07_energy", "c2_energy", {
    **W1("bigbill", slices=SL, illus="ILLUSTRATIVE SPLIT · NOT A REAL BILL",
         push=[{"label": "ENERGY", "at": C("is up about"), "dv": 30, "text": "WHOLESALE +50%"}, {"label": "CAPACITY", "at": C("But the capacity slice"), "dv": 45, "text": "CAPACITY ×3"}],
         stamp=[[C("A brutal winter storm"), "STORM"]]),
    "cam": cam((0, 960, 540, 1.0), (C("So far this year"), 960, 520, 1.0, 1.4), (C("A brutal winter storm"), 960, 540, 1.0, 1.2), (C("But the capacity slice"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("WHOLESALE: +50%", 430, 250, C("is up about"), size=60, until=C("But the capacity slice")),
              words("CAPACITY: ×3", 430, 250, C("But the capacity slice"), size=72, color=RED),
              MAYA(1750, 0.3, face="worry", pose="stand", hold="coffee", faces=[[0, "worry"], [C("But the capacity slice"), "shock"]], takes=[C("roughly tripled")]),
              tag((0, "FACT · MARKET MONITOR, JAN-JUN 2026"))]},
    sources=["imm_0728", "steo_nov26"])
stage("s08_eleven", "c2_eleven", {
    **W1("bigbill", slices=[{**s, "at": 0} for s in SL], illus="OUR ILLUSTRATION · IF FULLY PASSED THROUGH",
         push=[{"label": "CAPACITY", "at": C("Put its estimate"), "dv": 30, "text": "≈ $11 / MONTH?"}],
         totals=[[0, "$150"], [C("that's"), "$150 + ≈$11?"]], stamp=[[C("But it isn't pennies"), "NOT PENNIES"]]),
    "cam": cam((0, 960, 540, 1.0), (C("Put its estimate"), 960, 520, 1.0, 1.2), (C("It usually isn't"), 960, 540, 1.0, 1.2)), "drift": 3,
    "items": [words("WITHOUT THE DATA CENTERS?", 430, 220, 0.3, size=44, until=C("Put its estimate")),
              words("≈ $11 A MONTH", 430, 250, C("that's"), size=70, color=RED, until=C("It usually isn't")),
              it("bubble", text="ELEVEN BUCKS?!", x=1650, y=300, at=C("that's", 1.0), until=C("It usually isn't"), tail=[1750, 600], size=34),
              sign("IF FULLY PASSED THROUGH · UTILITIES HEDGE", 430, 350, C("It usually isn't"), color="#E1D5FF", size=24),
              MAYA(1750, 0.2, face="worry", pose="stand", hold="card", faces=[[0, "worry"], [C("that's"), "shock"]], takes=[C("that's", 0.6)]),
              tag((0, "ESTIMATE · MARKET MONITOR"), (C("Put its estimate"), "OUR CALC · ILLUSTRATIVE"))]},
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
    **W1("auction", prices=[[0, "—"], [C("A few years"), "A BARGAIN"], [C("This July"), "$325"]], capAt=C("And that maximum"), capText="CAP",
         gavel=[C("This July", 0.6), C("to stop it", 0.3)], supply=0.55, demand=[[0, 0.4], [C("This July"), 0.4], [C("it cleared at"), 0.85]],
         board="CAPACITY PRICE · $ PER MEGAWATT-DAY · PJM"),
    "cam": cam((0, 960, 480, 1.1), (C("A few years"), 960, 300, 1.35, 1.2), (C("This July"), 960, 540, 0.95, 1.4), (C("And that maximum"), 960, 360, 1.2, 1.2)), "drift": 2,
    "items": [words("×11 IN A FEW YEARS", 960, 990, C("it cleared at"), size=56, color=RED, until=C("And that maximum")),
              sign("A CAP SET WITH THE GOVERNORS", 960, 990, C("And that maximum"), color="#FFCDD2", size=32),
              tag((0, "FACT · PJM"), (C("it cleared at"), "OUR CALC ×11"))]},
    sources=["pjm_bra2829", "pjm_bra2425"], sfx=[{"kind": "hit", "cue": "it cleared at", "gain": 0.35}])
stage("s11b_tickets", "c3_tickets", {
    **W1("auction", prices=[[0, "TICKETS"], [C("For years"), "CHEAP"], [C("Then a new group"), "SOLD OUT?"], [C("the price goes up"), "$$$"]], supply=0.55,
         demand=[[0, 0.3], [C("For years"), 0.3], [C("Then a new group"), 0.95]], gavel=[C("the price goes up", 0.2)], board="THE BOX OFFICE"),
    "cam": cam((0, 960, 540, 1.0), (C("The crowd is"), 960, 540, 1.06, 1.2), (C("Then a new group"), 960, 520, 1.0, 1.2), (C("When the venue"), 960, 540, 1.06, 1.2)), "drift": 2,
    "items": [words("SEATS = POWER PLANTS", 960, 990, C("The seats are"), size=48, until=C("The crowd is")),
              words("CROWD = EVERYONE ON THE HOTTEST DAY", 960, 990, C("The crowd is"), size=40, until=C("Then a new group")),
              words("DEEP POCKETS, BIG APPETITE", 960, 990, C("with very deep pockets"), size=46, color=PURPLE, until=C("When the venue")),
              words("PRICE UP FOR EVERYONE IN LINE", 960, 990, C("the price goes up"), size=46, color=RED),
              tag((0, "ANALOGY · MECHANISM"))]})
stage("s12_short", "c3_short", {
    **W1("auction", prices=[[0, "$325"]], capAt=0.0, capText="CAP", supply=0.55, demand=0.9,
         shortAt=C("came up short"), shortText="STILL SHORT", gavel=[C("And even at the cap", 0.1)]),
    "cam": cam((0, 960, 540, 0.95), (C("came up short"), 1060, 500, 1.06, 1.2), (C("It's the second"), 960, 520, 1.0, 1.2), (C("Demand is arriving"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("EVEN AT THE CAP...", 960, 990, 0.2, size=54, until=C("came up short")),
              words("A FIRST IN PJM HISTORY", 960, 990, C("It's the second"), size=52, until=C("Demand is arriving")),
              words("DEMAND > STEEL AND CONCRETE", 960, 990, C("Demand is arriving"), size=48),
              tag((0, "FACT · PJM"))]},
    sources=["pjm_bra2829"], sfx=[{"kind": "hit", "cue": "came up short", "gain": 0.3}])
stage("s13_monitor", "c3_monitor", {
    **W1("gridbuild", build=1.0, cost=[[0, ""], [C("The market monitor"), "ALMOST HALF"]], costTitle="CAPACITY BILL FROM DATA CENTERS (MONITOR ESTIMATE)",
         split=[{"who": "HOMES", "v": [[0, 0.0], [C("And that bill is shared"), 0.0], [C("Including Maya"), 0.6]]},
                {"who": "SHOPS", "v": [[0, 0.0], [C("And that bill is shared"), 0.0], [C("Including Maya"), 0.45]]},
                {"who": "FACTORIES", "v": [[0, 0.0], [C("And that bill is shared"), 0.0], [C("Including Maya"), 0.5]]},
                {"who": "DATA CENTERS", "v": [[0, 0.0], [C("And that bill is shared"), 0.0], [C("Including Maya"), 0.55]]}],
         hi=None),
    "cam": cam((0, 960, 540, 1.0), (C("data centers were behind"), 960, 520, 1.0, 1.2), (C("And that bill is shared"), 960, 540, 1.0, 1.4)), "drift": 3,
    "items": [words("SO HOW MUCH IS AI?", 1300, 380, 0.2, size=50, until=C("data centers were behind")),
              words("SHARED BY EVERYONE AT THE PEAK", 1300, 380, C("And that bill is shared"), size=42),
              MAYA(1000, C("Including Maya", -0.6), face="shock", pose="stand", scale=1.0),
              tag((0, "ESTIMATE · MARKET MONITOR"), (C("And that bill is shared"), "MECHANISM"))]},
    sources=["imm_0728"])
stage("s14_fix", "c3_fix", {
    **W1("auction", prices=[[0, "WHO PAYS?"]], capAt=0.0, capText="CAP", supply=0.55, demand=[[0, 0.9], [C("Take the data centers out"), 0.45]],
         gavel=[C("Who pays", 0.1)], board="THE OPEN QUESTION"),
    "cam": cam((0, 960, 600, 0.95), (C("Take the data centers out"), 1060, 520, 1.06, 1.2), (C("PJM is trying"), 960, 520, 1.0, 1.2), (C("Who pays"), 960, 500, 1.06, WHIP)), "drift": 2,
    "items": [sign("MONITOR: A SEPARATE AUCTION FOR DATA CENTERS", 960, 990, C("Take the data centers out"), color="#FFE0B2", size=28, until=C("PJM is trying")),
              sign("PJM: CONNECT, BUT CUT BACK WHEN THE GRID IS STRESSED", 960, 990, C("PJM is trying"), color="#BBDEFB", size=28, until=C("None of it")),
              words("UNSETTLED", 960, 960, C("None of it"), size=64),
              tag((0, "PROPOSALS · NOT RULES"))]},
    sources=["imm_0728", "pjm_bra2829"])

# ====================================================================== CHAPTER 4: who pays for the wires
bumper("s15_b4", "c4_card", "CHAPTER FOUR", "WHO PAYS FOR THE WIRES", "Billions in steel, split among us all.", GREEN)
stage("s16_capex", "c4_capex", {
    **W1("gridbuild", build=[[0, 0.0], [C("Now the wires"), 0.1], [C("And both point"), 1.0]],
         cost=[[0, ""], [C("have filed plans"), "$130 BILLION+"]], costTitle="DOMINION + AEP PLANS TO 2030 · OUR SUM OF 10-K FIGURES"),
    "cam": cam((0, 960, 560, 1.0), (C("have filed plans"), 960, 520, 0.95, 1.2), (C("New lines"), 960, 540, 1.0, 1.2), (C("And both point"), 960, 520, 0.95, 1.6)), "drift": 4,
    "items": [words("A BUILDING SPREE", 1400, 380, 0.3, size=56, until=C("New lines")),
              words("LINES · SUBSTATIONS · PLANTS", 1400, 380, C("New lines"), size=44, until=C("And both point")),
              words("REASON: GIANT NEW CUSTOMERS", 1400, 380, C("And both point"), size=44, color=PURPLE),
              DEV(1000, 0.3, face="happy", pose="point", faces=[[0, "happy"], [C("And both point"), "worry"]]),
              tag((0, "FACT · 10-K PLANS · OUR SUM"))]},
    sources=["dom_10k25", "aep_10k25"])
stage("s16b_dev", "c4_dev", {
    **W1("pbtown", dc=[[0, 0.5], [C("Lately"), 0.5], [C("each one planned"), 0.9]], cranes=True, zap=0.6, heat=0.4, campusText="FUTURE CUSTOMERS?"),
    "cam": cam((0, 820, 520, 1.3), (C("Lately"), 1000, 480, 1.1, 1.4), (C("each one planned"), 1800, 470, 0.95, 1.4), (C("And every tower"), 820, 520, 1.25, 1.4)), "drift": 3,
    "items": [DEV(700, 0.0, face="happy", pose="stand", hold="clipboard", label="DEV · LINEWORKER", labelUntil=C("Lately"), faces=[[0, "happy"], [C("may or may not"), "worry"]]),
              it("bubble", text="THE WORK NEVER STOPS.", x=820, y=280, at=C("Lately"), until=C("Steel towers"), tail=[700, 500], size=30),
              words("PLANNED YEARS AHEAD", 1800, 170, C("each one planned"), size=52, until=C("And every tower")),
              it("bubble", text="...WILL THEY SHOW UP?", x=1900, y=300, at=C("may or may not"), until=C("And every tower"), tail=[1800, 520], size=28),
              words("→ A LEDGER SOMEONE PAYS OFF", 820, 160, C("And every tower"), size=48, color="#FFFFFF"),
              tag((0, "OUR STORY · ILLUSTRATIVE CHARACTER"))]})
add("p17_rate", "c4_rate", "engine_draw", {
    "title": "How building more becomes your bill", "board": BOARD, "draw_start": C("Let me draw it"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(700, 300, 240, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("A regulated utility"), "label": lbl("BUILD", 820, 368, 34, "accent2")},
        {"d": arrow((940, 355), (1070, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("earns a set return")},
        {"d": rect(1080, 300, 300, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("earns a set return"), "label": lbl("SET RETURN", 1230, 368, 32, "accent3")},
        {"d": arrow((1230, 410), (820, 410), -0.35), "color": "risk", "width": 5, "kind": "arrow", "start": C("Build more")},
        {"d": arrow((1050, 470), (1050, 530), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("Then the cost is split")},
        {"d": rect(640, 550, 200, 90), "color": "accent2", "width": 5, "kind": "box", "start": C("Homes"), "label": lbl("HOMES", 740, 608, 26, "accent2")},
        {"d": rect(860, 550, 200, 90), "color": "accent3", "width": 5, "kind": "box", "start": C("shops"), "label": lbl("SHOPS", 960, 608, 26, "accent3")},
        {"d": rect(1080, 550, 210, 90), "color": "accent", "width": 5, "kind": "box", "start": C("factories"), "label": lbl("FACTORIES", 1185, 608, 24, "accent")},
        {"d": rect(1310, 550, 250, 90), "color": "risk", "width": 5, "kind": "box", "start": C("data centers."), "label": lbl("DATA CENTERS", 1435, 608, 24, "risk")},
        {"d": rect(800, 700, 560, 90), "color": "ink", "width": 5, "kind": "box", "start": C("And how it's split"), "label": lbl("THE SPLIT = A CHOICE", 1080, 758, 30, "ink")},
        {"d": dot(1080, 880), "color": "muted", "width": 1, "start": C("Let me draw it"), "label": lbl("MECHANISM · DOMINION'S AUTHORIZED ROE 9.8% (VIRGINIA SCC, NOV 2025) · SEE ALSO: WHY AMERICA'S ELECTRICITY BILLS ARE RISING", 1080, 880, 14, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Build more", 0.3), "dur": 1.4, "target": [1230, 355]}, {"kind": "point", "at": C("And how it's split", 0.3), "dur": 1.6, "target": [1080, 745]}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom"])
stage("s18_study", "c4_study", {
    **W1("gridbuild", build=1.0, cost=[[0, ""], [C("On the big transmission lines"), "≈ 1/7 THE RETURN"]], costTitle="DATA-CENTER CLASS vs OTHER BIG CUSTOMERS · TRANSMISSION",
         split=[{"who": "HOMES", "v": 0.6}, {"who": "SHOPS", "v": 0.5}, {"who": "FACTORIES", "v": [[0, 0.5], [C("On the big transmission lines"), 0.85]]},
                {"who": "DATA CENTERS", "v": [[0, 0.5], [C("On the big transmission lines"), 0.12]]}],
         hi=None),
    "cam": cam((0, 960, 540, 1.0), (C("On the big transmission lines"), 960, 520, 1.0, 1.2), (C("In plain English"), 960, 540, 1.0, 1.4), (C("The regulators say"), 960, 520, 1.0, 1.4)), "drift": 3,
    "items": [words("VIRGINIA'S OWN NUMBERS", 1300, 380, 0.3, size=50, until=C("On the big transmission lines")),
              words("BIGGEST USERS, SMALL SHARE", 1300, 380, C("In plain English"), size=46, until=C("The regulators say")),
              words("UNDER REVIEW", 1300, 380, C("The regulators say"), size=56, color=GREEN),
              tag((0, "FACT · VIRGINIA SCC ORDER"), (C("On the big transmission lines"), "FACT · OUR CALC ≈1/7"))]},
    sources=["scc_dom"])
stage("s19_bill", "c4_bill", {
    **W1("bigbill", slices=[{**s, "at": 0} for s in SL], illus="ILLUSTRATIVE SPLIT", totals=[[0, "$150"], [C("raised her base rates"), "+7.5%"]],
         push=[{"label": "WIRES + FEES", "at": C("raised her base rates"), "dv": 22, "text": "BASE RATES"}],
         stamp=[[C("On the monthly bill"), "YOUR BILL"]]),
    "cam": cam((0, 960, 540, 1.0), (C("raised her base rates"), 960, 520, 1.0, 1.2), (C("Not all of that"), 960, 540, 1.0, 1.4), (C("On the monthly bill"), 960, 520, 1.0, 1.0)), "drift": 3,
    "items": [words("+7.5% BASE RATES", 430, 250, C("raised her base rates"), size=58, color=RED, until=C("Not all of that")),
              sign("NOT ALL DATA CENTERS: STORMS, OLD EQUIPMENT...", 430, 250, C("Not all of that"), color="#E1D5FF", size=22),
              MAYA(1750, 0.3, face="worry", pose="shrug", faces=[[0, "worry"], [C("On the monthly bill"), "shock"]], takes=[C("On the monthly bill")]),
              tag((0, "FACT · VIRGINIA SCC ORDER"))]},
    sources=["scc_dom"])

# ====================================================================== CHAPTER 5: the fightback
bumper("s20_b5", "c5_card", "CHAPTER FIVE", "THE FIGHTBACK", "Minimum bills, long contracts, big checks.", ORANGE)
stage("s21_ohio", "c5_ohio", {
    **W1("hearing", bench="OHIO UTILITY COMMISSION", unroll=[[0, 0.0], [C("for years"), 0.0], [C("Walk away early"), 1.0]], years=12, ramp=4, yearsText="UP TO 12 YEARS",
         lockAt=C("must pay for at least"), lockText="85% MIN", lockX=1700),
    "cam": cam((0, 960, 460, 0.95), (C("must pay for at least"), 1060, 560, 1.06, 1.2), (C("for years"), 960, 580, 1.0, 1.2), (C("Walk away early"), 960, 540, 0.95, 1.2)), "drift": 2,
    "items": [words("PAUSED: NEW DATA CENTER DEALS", 960, 140, 0.4, size=44, until=C("a new rule")),
              words("USE IT OR NOT, PAY FOR IT", 960, 140, C("whether they use it"), size=48, until=C("Walk away early")),
              words("EXIT FEE", 960, 140, C("Walk away early"), size=64, color=RED),
              tag((0, "FACT · AEP OHIO TARIFF (PUCO, JUL 2025)"))]},
    sources=["aep_dct"])
stage("s21b_hearing", "c5_hearing", {
    **W1("hearing", bench="VIRGINIA STATE CORPORATION COMMISSION", lectern=True),
    "cam": cam((0, 960, 520, 1.06), (C("the parties in the room"), 960, 540, 0.95, 1.4), (C("Anyone can read"), 960, 520, 1.06, 1.2), (C("Most people never do"), 960, 540, 1.0, 1.2)), "drift": 2,
    "items": [words("THESE FIGHTS HAPPEN IN PUBLIC", 960, 140, 0.3, size=46, until=C("the parties in the room")),
              sign("BIG TECH LAWYERS", 560, 980, C("Amazon, Google"), color="#E1D5FF", size=30),
              sign("DATA CENTER INDUSTRY", 960, 980, C("the data center industry"), color="#FFE0B2", size=30),
              sign("CONSUMER ADVOCATES", 1360, 980, C("consumer advocates"), color="#C8E6C9", size=30),
              words("READ THE FILINGS", 960, 140, C("Anyone can read"), size=52, until=C("Most people never do")),
              words("...MOST PEOPLE NEVER DO", 960, 140, C("Most people never do"), size=50, color=RED),
              MAYA(1650, C("Most people never do"), face="shock", pose="stand", scale=1.0),
              tag((0, "FACT · SCC ORDER PARTIES"))]},
    sources=["scc_dom"])
stage("s22_gs5", "c5_gs5", {
    **W1("hearing", bench="VIRGINIA STATE CORPORATION COMMISSION", unroll=[[0, 0.0], [C("Long contracts"), 1.0]], years=14, ramp=4, yearsText="LONG CONTRACTS (FROM 2027)",
         lockAt=C("Minimum bills"), lockText="MIN BILL", lockX=1720),
    "cam": cam((0, 960, 540, 0.95), (C("Long contracts"), 960, 580, 1.0, 1.2), (C("Minimum bills"), 1060, 560, 1.06, 1.2), (C("Dominion says"), 960, 520, 0.95, 1.4)), "drift": 2,
    "items": [words("A RATE CLASS FOR THE GIANTS", 960, 140, 0.4, size=48, until=C("Dominion says")),
              words("NO SUBSIDIES BETWEEN CUSTOMERS", 960, 140, C("Dominion says"), size=44, color=GREEN),
              tag((0, "FACT · VIRGINIA SCC ORDER"))]},
    sources=["scc_dom", "dom_10k25"])
add("p23_strand", "c5_why", "engine_draw", {
    "title": "The line built for a data center that never comes", "board": BOARD, "draw_start": C("Picture a utility"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(700, 300, 260, 110), "color": "accent2", "width": 6, "kind": "box", "start": C("Picture a utility"), "label": lbl("NEW LINE BUILT", 830, 368, 26, "accent2")},
        {"d": arrow((960, 355), (1090, 355), 0.0), "color": "ink", "width": 5, "kind": "arrow", "start": C("for a data center")},
        {"d": rect(1100, 300, 300, 110), "color": "risk", "width": 6, "kind": "box", "start": C("that never shows up"), "label": lbl("NO-SHOW / SHUTS DOWN", 1250, 368, 24, "risk")},
        {"d": arrow((1180, 410), (960, 540), 0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("Without a contract")},
        {"d": rect(700, 550, 340, 110), "color": "risk", "width": 6, "kind": "box", "start": C("Without a contract"), "label": lbl("EVERYONE'S RATES", 870, 618, 28, "risk")},
        {"d": dot(870, 700), "color": "risk", "width": 1, "start": C("for decades"), "label": lbl("FOR DECADES", 870, 710, 24, "risk")},
        {"d": arrow((1320, 410), (1420, 540), -0.15), "color": "accent3", "width": 5, "kind": "arrow", "start": C("With a minimum bill")},
        {"d": rect(1240, 550, 340, 110), "color": "accent3", "width": 6, "kind": "box", "start": C("With a minimum bill"), "label": lbl("DATA CENTER PAYS", 1410, 618, 28, "accent3")},
        {"d": dot(1410, 700), "color": "accent3", "width": 1, "start": C("pays either way"), "label": lbl("EITHER WAY", 1410, 710, 24, "accent3")},
        {"d": rect(860, 770, 560, 80), "color": "accent", "width": 5, "kind": "box", "start": C("That one clause"), "label": lbl("ONE CLAUSE > ANY CHIP", 1140, 822, 30, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Without a contract", 0.3), "dur": 1.4, "target": [870, 605]}, {"kind": "point", "at": C("With a minimum bill", 0.3), "dur": 1.4, "target": [1410, 605]},
                {"kind": "react", "at": C("That one clause", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["scc_dom", "aep_dct"])
stage("s24_deals", "c5_deals", {
    **W1("plantdeal", steam=[[0, 0.0], [C("Microsoft is buying"), 0.0], [C("brought back to life"), 1.0]], plantText="NUCLEAR PLANT (GENERIC)", campusText="DATA CENTERS",
         tags=[[0, ""], [C("Microsoft is buying"), "MICROSOFT · A REACTOR RESTART"], [C("Meta signed"), "META · KEEPS A PLANT RUNNING"],
               [C("Amazon locked in"), "AMAZON · NUCLEAR, LONG-TERM"], [C("Some deals add"), "NEW POWER ≠ RESERVED POWER"]],
         tagX=[[0, 900], [C("Microsoft is buying"), 600], [C("Meta signed"), 900], [C("Amazon locked in"), 1300], [C("Some deals add"), 960]], shakeAt=C("signing their own"), shakeX=900),
    "cam": cam((0, 900, 560, 1.0), (C("Microsoft is buying"), 400, 520, 1.0, 1.4), (C("Meta signed"), 900, 520, 0.95, 1.2), (C("Amazon locked in"), 1300, 520, 1.0, 1.2),
               (C("Some deals add"), 960, 540, 0.85, 1.4)), "drift": 3,
    "items": [it("bubble", text="NO RATEPAYER SUPPORT, SAYS THE OWNER", x=900, y=330, at=C("without ratepayer support"), until=C("Amazon locked in"), tail=[700, 600], size=26),
              DEV(1900, C("Some deals add"), face="happy", pose="point", scale=1.0),
              tag((0, "DISCLOSED DEALS"))]},
    sources=["ceg_crane", "ceg_clinton", "talen_amzn"])
stage("s25_counter", "c5_counter", {
    **W1("plantdeal", steam=1.0, supply=[[0, 0.0], [C("But new supply"), 0.0], [C("a wave of new solar"), 1.0]], plantText="POWER PLANT", campusText="DATA CENTERS",
         tagX=[[0, 900], [C("More customers share"), 1300], [C("But new supply"), 2500], [C("And PJM itself"), 1300]],
         tags=[[0, "MORE DEMAND → LOWER PRICES (SO FAR)"], [C("It's not clear"), "...WILL THAT HOLD?"], [C("But new supply"), "A WAVE OF SOLAR + WIND"],
               [C("And PJM itself"), "PJM TRIMMED ITS NEAR-TERM FORECAST"]]),
    "cam": cam((0, 900, 540, 0.9), (C("More customers share"), 1300, 560, 1.05, 1.2), (C("But new supply"), 2500, 520, 0.95, 1.4), (C("And PJM itself"), 1300, 540, 0.9, 1.4)), "drift": 3,
    "items": [it("bubble", text="MORE USERS SHARE THE FIXED COST", x=1400, y=330, at=C("More customers share"), until=C("But new supply"), tail=[1450, 650], size=28),
              MAYA(600, 0.3, face="worry", pose="stand", faces=[[0, "worry"], [C("More customers share"), "happy"]]),
              tag((0, "FACT · LBNL / BRATTLE"), (C("But new supply"), "FORECAST · EIA"), (C("And PJM itself"), "FACT · PJM"))]},
    sources=["lbnl_prices", "steo_nov26", "pjm_lf26"])

# ====================================================================== CHAPTER 6: will your bill explode?
bumper("s26_b6", "c6_card", "CHAPTER SIX", "WILL YOUR BILL EXPLODE?", "The national number, and the hot spots.", RED)
stage("s27_trend", "c6_trend", {
    **W1("gaugeroom", lo=15, hi=20, dec=1, gaugeX=760, needle=[[0, 15], [C("Nationally"), 16.5], [C("is expected to climb"), 18.7]],
         marks=[{"v": 16.5, "label": "2024", "at": C("Nationally")}, {"v": 18.7, "label": "2027 FORECAST", "at": C("is expected to climb"), "color": PURPLE}]),
    "cam": cam((0, 960, 540, 0.95), (C("Nationally"), 900, 540, 1.06, 1.2), (C("Rising"), 960, 540, 0.95, 1.2)), "drift": 2,
    "items": [words("WILL IT EXPLODE?", 1380, 300, 0.2, size=56, until=C("is expected to climb")),
              words("≈ +13% IN 3 YEARS", 1380, 300, C("is expected to climb"), size=58, color=PURPLE, until=C("Rising")),
              words("RISING. NOT EXPLODING.", 1380, 300, C("Rising"), size=46),
              sign("U.S. HOME PRICE PER kWh · EIA FORECAST, NOV 2026", 1380, 420, 0.6, color="#FFFFFF", size=20),
              tag((0, "FORECAST · EIA"))]},
    sources=["steo_nov26"])
stage("s28_dials", "c6_dials", {
    **W1("gaugeroom", gauge=False, dialX=540,
         dials=[{"label": "MINIMUM-BILL CONTRACTS", "at": C("First, do the giants"), "v": [[0, 0], [C("Turn them all the right way"), 0.9], [C("Turn them the other way"), -0.9]], "l": "NONE", "r": "SIGNED"},
                {"label": "NEW SUPPLY SPEED", "at": C("Second, does new"), "v": [[0, 0], [C("Turn them all the right way"), 0.9], [C("Turn them the other way"), -0.9]], "l": "SLOW", "r": "FAST"},
                {"label": "HOW SHARED LINES ARE SPLIT", "at": C("Third, how do"), "v": [[0, 0], [C("Turn them all the right way"), 0.9], [C("Turn them the other way"), -0.9]], "l": "SPREAD", "r": "CAUSER PAYS"}]),
    "cam": cam((0, 960, 520, 1.06), (C("comes down to three dials"), 960, 540, 0.95, 1.2), (C("Turn them all the right way"), 960, 560, 0.9, 1.0), (C("Turn them the other way"), 960, 560, 0.95, 0.6)), "drift": 2,
    "items": [words("AVERAGES HIDE HOT SPOTS", 960, 260, 0.2, size=52, until=C("comes down to three dials")),
              words("THREE DIALS", 960, 300, C("comes down to three dials"), size=60, until=C("Turn them all the right way")),
              words("GROWTH CAN SPREAD COSTS THINNER", 960, 300, C("Turn them all the right way"), size=44, color=GREEN, until=C("Turn them the other way")),
              words("HOUSEHOLDS HELP PAY", 960, 300, C("Turn them the other way"), size=52, color=RED),
              it("sparky", x=[[0, 2300], [1.0, 1750]], y=1000, at=0.3, scale=0.8, face="happy", faces=[[0, "happy"], [C("Turn them the other way"), "shock"]], hops=[]),
              tag((0, "VERDICT · OUR FRAMEWORK"))]},
    sources=["scc_dom", "aep_dct", "pjm_bra2829", "lbnl_prices"])
stage("s28b_maya", "c6_maya", {
    **W1("pbtown", dc=1.0, zap=1.0, heat=0.5, meter=1),
    "cam": cam((0, 260, 600, 1.4), (C("It's the contract"), 1600, 480, 0.95, 1.6), (C("It's whether"), 900, 520, 0.9, 1.4), (C("And it's a formula"), 300, 600, 1.3, 1.4)), "drift": 2,
    "items": [it("billpaper", x=320, y=[[0, 520], [2.0, 480]], at=0.2, until=C("It's the contract"), scale=1.1, amount="$150"),
              words("NOT PRINTED ON THE BILL", 300, 180, 0.4, size=50, until=C("It's the contract")),
              words("THE CONTRACT DOWN THE ROAD", 1600, 160, C("It's the contract"), size=48, until=C("It's whether")),
              words("NEW PLANTS, ON TIME?", 900, 160, C("It's whether"), size=50, until=C("And it's a formula")),
              words("A FORMULA IN A RATE CASE", 300, 180, C("And it's a formula"), size=48, color="#FFFFFF"),
              MAYA(140, 0.0, face="happy", pose="clipboard", hold="card", faces=[[0, "worry"], [C("And it's a formula"), "happy"]]),
              tag((0, "VERDICT"))]})
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
