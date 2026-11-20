"""Generates projects/before-you-buy-anthropic-2026-11/deliverables/documentary/storyboard.yaml
(series "Before You Buy", Anthropic (Nasdaq: ANT), November 2026 edition; spec docs/series/BEFORE_YOU_BUY.md).

A buyer's checklist, not a repeat of Ep 72. Protagonist MAYA (fictional would-be buyer, shared `toon` rig, holding a clipboard).
Series look (BYB kit: chipcity, editionstamp, chipbuddy "ANT", riskscale) + new items built for this film in
remotion/src/animation-engine/CartoonStage/bybant.tsx:
  checklist (MAYA'S CLIPBOARD, signature), classcards (the share-class family), floodgates (THE LOCK-UP DAM, signature),
  ipopath (Facebook 2012 and Arm 2023-24, first year vs the offer price), govtower (who is in charge).
Signature animations: the clipboard (s03, s36, s44), the share-class family (s06), the lock-up dam (s18, s20), the first-year
charts (s34, s35), the balance of bullish and bearish signals (s42-s43).
Presenter boards (4): p09 outstanding vs fully diluted, p14 price to sales vs Nvidia and Microsoft, p25 the first report card,
p30 the partner triangle.
NEUTRAL: no logos (ticker ANT), no real people drawn; every figure dated or labelled (FACT / OUR CALC / REPORTED); risks and
positives with equal weight; never buy/sell, no price target; "not investment advice" at the start and the end.
Short-safe layout: the Shorts crop the centre 1520 px (x 200-1720), so labels of c1_*, c3_* and c4_* scenes stay inside it.
QUARTERLY REFRESH: update EDITION, the closes and the multiples (sources.yaml), re-run.
Run: python tools/gen_byb_anthropic_storyboard.py   (checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from byb_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "before-you-buy-anthropic-2026-11"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
set_edition("DATA AS OF NOV 19, 2026 CLOSE", "FIRST TRADING DAY · 424B4 (NOV 18, 2026)")
AMBER, BLUE, GREEN, PINK, CREAM, LILAC = "#FFE0B2", "#BBDEFB", "#C8E6C9", "#FFCDD2", "#F5F5F5", "#E1BEE7"
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *k: [{"at": a[0], "x": a[1], "y": a[2], "zoom": a[3], **({"dur": a[4]} if len(a) > 4 else {})} for a in k]
QUESTIONS = ["WHAT DO I ACTUALLY OWN?", "WHAT AM I PAYING?", "WHEN CAN INSIDERS SELL?", "WHAT WILL THE FIRST REPORT SHOW?",
             "WHO DOES IT DEPEND ON?", "HOW WILD DO NEW STOCKS GET?", "WHO'S REALLY IN CHARGE?"]


def MAYA(x, at=0.0, **kw):
    """Maya, the fictional would-be buyer (shared toon rig)."""
    kw.setdefault("scale", 1.15)
    kw.setdefault("y", 1040)
    kw.setdefault("hold", "clipboard")
    return it("toon", x=x, at=at, who="shopper", v=8, skin=2, hair=4, hairStyle=2, color="#7357C9", glasses=True, scarf="#FFB547", **kw)


def ANT(x, y=860, **kw):
    kw.setdefault("label", "ANT")
    kw.setdefault("color", "#FFB547")
    return buddy(x, y, **kw)


def clip(rows_at, focus, ticks=None, **kw):
    rows = [{"text": q, "at": a, **({"tick": ticks[k]} if ticks and ticks[k] is not None else {})} for k, (q, a) in enumerate(zip(QUESTIONS, rows_at))]
    return it("checklist", rows=rows, focus=focus, title="BEFORE YOU BUY: ANT", **kw)


# ====================================================================== HOOK
stage("s01_open", "h_open", {
    "zones": [Z("livingroom")], "worldW": 2400,
    "cam": cam((0, 900, 560, 1.12), (C("On the screen"), 1000, 520, 1.0, 1.6), (C("And her thumb"), 760, 600, 1.15, 1.2)), "drift": 2,
    "items": [MAYA([[0, 420], [1.6, 560]], 0.0, hold="phone", pose="stand", face="happy", label="MAYA · WOULD-BE BUYER (FICTIONAL)", labelUntil=C("On the screen"),
                   faces=[[0, "happy"], [C("sold its first shares"), "shock"], [C("And her thumb"), "squint"]]),
              it("letters", x=1150, y=180, text="NEW TICKER: A · N · T", at=C("On the screen"), size=64, color="gold"),
              it("counter", x=1150, y=360, at=C("sold its first shares"), prefix="$", suffix="", decimals=2, steps=[[0, 0], [{"cue": "to the public at"}, 83.0]], text="IPO OFFER PRICE (424B4)"),
              it("sign", x=1150, y=560, text="NASDAQ · PRICED NOV 18 · FIRST TRADE NOV 19, 2026", at=C("to the public at"), color=BLUE, size=26),
              it("sign", x=1150, y=700, text="BUY?", at=C("And her thumb"), color=PINK, size=60),
              ANT(1750, 880, at=0.5, mood="happy", hop=24)]},
    sources=["ant_424b4", "ant_fwp"], sfx=[{"kind": "hit", "cue": "to the public at", "gain": 0.3}])
stage("s02_day", "h_day", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("slid back"), 1060, 540, 1.05, 1.6), (C("Maya has a rule"), 900, 560, 1.0, 1.2)), "drift": 2,
    "items": [it("stockelevator", x=1450, y=150, at=0.2, floors=["$111.50", "$97.17", "$83.00"], stops=[{"cue": "and closed at"}], scale=0.85),
              it("letters", x=650, y=160, text="DAY ONE: A ROLLER COASTER", at=0.2, size=50, color="gold", until=C("Everyone on her feed")),
              it("sign", x=650, y=320, text="CLOSE NOV 19, 2026: $97.17 · CNBC, THE NATIONAL", at=C("and closed at"), color=AMBER, size=24),
              it("sign", x=650, y=540, text="OPEN $111.50 · CLOSE $97.17 · OFFER $83.00", at=C("opened far above"), color=BLUE, size=24),
              it("sign", x=650, y=430, text="LATEST CLOSE WHEN THIS FILM WAS MADE", at=C("and closed at"), color=CREAM, size=22),
              it("letters", x=650, y=160, text="READ THE LABEL FIRST", at=C("Never buy something"), size=56, color="gold"),
              MAYA(520, 0.0, pose="stand", faces=[[0, "shock"], [C("slid back"), "worry"], [C("Maya has a rule"), "smug"]])]},
    sources=["cnbc_live", "national", "px"], sfx=[{"kind": "whoosh", "cue": "slid back", "gain": 0.25}])
stage("s03_list", "h_maya", {
    "zones": [Z("livingroom")], "worldW": 2400,
    "cam": cam((0, 960, 540, 1.0), (C("What do I actually own"), 1040, 520, 1.06, 2.0), (C("Let's go through them"), 960, 540, 1.0, 1.2)), "drift": 1,
    "items": [clip([C("What do I actually own"), C("What am I paying"), C("When can insiders sell"), C("What will the first report show"),
                    C("Who does this company depend on"), C("How wild do new stocks get"), C("who's really in charge")],
                   [[0, -1], [C("What do I actually own"), 0], [C("What am I paying"), 1], [C("When can insiders sell"), 2], [C("What will the first report show"), 3],
                    [C("Who does this company depend on"), 4], [C("How wild do new stocks get"), 5], [C("who's really in charge"), 6], [C("Let's go through them"), -1]],
                   x=1140, y=560, at=C("grabs a clipboard"), scale=0.95),
              MAYA([[0, 200], [1.4, 380]], 0.0, pose="stand", face="happy", faces=[[0, "happy"], [C("What am I paying"), "squint"], [C("Let's go through them"), "grin"]])]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "grabs a clipboard", "gain": 0.25}])
stage("s04_disc", "h_disclaimer", {
    "zones": [Z("chipcity", signs=["NOT INVESTMENT ADVICE", "FILINGS + NAMED PRESS", "OUR MATH · LABELLED", "DATED EDITION"])], "worldW": 2400,
    "cam": cam((0, 1000, 520, 1.05), (1.0, 1100, 520, 1.0, 2.0)), "drift": 3,
    "items": [it("letters", x=1000, y=150, text="NOT INVESTMENT ADVICE", at=0.2, size=64, color="gold"),
              it("sign", x=1000, y=290, text="NO BUY OR SELL CALL · NO PRICE TARGET", at=C("We won't tell you"), color=PINK, size=30),
              it("sign", x=1000, y=400, text="ANTHROPIC'S PROSPECTUS + FILINGS + NAMED PRESS + OUR MATH", at=C("Everything here comes from"), color=BLUE, size=26),
              it("sign", x=1000, y=510, text="DISCLOSURE: AI TOOLS INCL. CLAUDE ARE USED BY THIS CHANNEL", at=C("Our channel uses"), color=AMBER, size=26),
              it("sign", x=1000, y=620, text="ANTHROPIC DID NOT SPONSOR OR REVIEW THIS VIDEO", at=C("didn't sponsor or review"), color=CREAM, size=26),
              stamp(1560, 880, at=C("Everything here comes from"), scale=0.6),
              ANT(450, 880, at=0.3, mood="cool", hop=16), buddy(1600, 880, at=0.5, mood="happy", color="#5CC8FF", label="FILINGS", hop=20)]},
    sources=["ant_424b4"])

# ====================================================================== 1: what you actually own
card("s05_c1", "c1_card", "What You Actually Own", "Share classes, votes and how many shares exist")
stage("s06_classes", "c1_classes", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 540, 1.0), (C("Class A is"), 960, 540, 1.04, 2.0), (C("special classes"), 960, 520, 0.98, 1.6)), "drift": 1,
    "items": [it("classcards", x=960, y=600, at=0.1, scale=1.05, title="ONE COMPANY, A FAMILY OF SHARE CLASSES (424B4)", cw=262, gap=22, ch=440,
                 glow=[[0, -1], [C("Class A is"), 0], [C("Class N gets"), 1], [C("special classes"), -1]],
                 cards=[{"cls": "A", "who": "PUBLIC BUYERS\nNASDAQ: ANT", "money": "YES", "votes": "1 VOTE PER SHARE", "meter": 0.35, "color": "#E8A317", "at": C("Class A is")},
                        {"cls": "N", "who": "MOSTLY PARTNERS\n(STRATEGIC HOLDERS)", "money": "YES", "votes": "NO VOTE", "meter": 0.0, "color": "#2F6FDB", "at": C("Class N gets")},
                        {"cls": "F", "who": "FOUNDER LLC\n(CO-FOUNDERS)", "money": "NONE", "votes": "50.1% OF ALL VOTES", "meter": 0.5, "color": "#7357C9", "at": C("special classes")},
                        {"cls": "T", "who": "LONG-TERM\nBENEFIT TRUST", "money": "NONE", "votes": "ELECTS BOARD MAJORITY", "meter": 0.6, "color": "#2E9E6B", "at": C("special classes", 0.4)},
                        {"cls": "E", "who": "EMPLOYEES\n(NOT FOUNDERS)", "money": "NONE", "votes": "LIMITED MATTERS", "meter": 0.1, "color": "#E5483B", "at": C("special classes", 0.8)}])]},
    sources=["ant_424b4"], sfx=[{"kind": "whoosh", "cue": "special classes", "gain": 0.25}])
stage("s07_votes", "c1_votes", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 520, 1.0), (C("A single Class T share"), 1000, 500, 1.04, 1.6), (C("a Class A buyer"), 960, 540, 1.0, 1.2)), "drift": 1,
    "items": [it("letters", x=960, y=120, text="WHO HOLDS THE VOTES?", at=0.2, size=56, color="gold"),
              it("govtower", x=960, y=820, at=0.2, scale=0.82, seats=9, trust=5, trustAt=C("picks most of the board"),
                 founder=[[0, 0], [{"cue": "carries"}, 0], [{"cue": "of the votes"}, 0.501]], founderText="CLASS F: 50.1%",
                 ballotAt=C("a Class A buyer"), bx=680, labels={"trust": "MOST OF THE BOARD: PICKED BY THE TRUST (CLASS T)", "founder": "FOUNDER VOTE", "ballot": "CLASS A: 1 VOTE EACH"}),
              it("sign", x=960, y=260, text="BIG DECISIONS: ALREADY SPOKEN FOR", at=C("But the big decisions"), color=PINK, size=32)]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "of the votes", "gain": 0.3}])
stage("s08_float", "c1_float", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("But that block"), 960, 500, 1.04, 1.6), (C("most of them can't"), 960, 540, 1.0, 1.2)), "drift": 1,
    "items": [it("letters", x=960, y=110, text="HOW MANY SHARES REALLY EXIST?", at=0.2, size=52, color="gold"),
              it("shares", x=960, y=420, at=0.2, scale=0.95,
                 groups=[{"n": 7, "at": C("into public hands"), "color": "#FFD45C", "label": "FLOAT ≈ 7%", "step": 0.08},
                         {"n": 43, "at": C("early investors"), "color": "#5CC8FF", "label": "CLASS N 43%", "step": 0.02},
                         {"n": 50, "at": C("partners and employees"), "color": "#FFFFFF", "label": "OTHER A 50%", "step": 0.02}]),
              it("sign", x=960, y=870, text="0.98BN SOLD OF 13.22BN OUTSTANDING (OUR CALC, 424B4)", at=C("But that block"), color=AMBER, size=26),
              it("sign", x=960, y=975, text="MOST ARE LOCKED UP FOR NOW", at=C("most of them can't"), color=PINK, size=30),
              MAYA(1720, 0.0, pose="stand", faces=[[0, "happy"], [C("But that block"), "shock"]], scale=1.0)]},
    sources=["ant_424b4", "ant_fwp"])
board("p09_dilution", "c1_draw", "Outstanding vs fully diluted (424B4)", C("Outstanding shares are"), [
    {"d": "M 600 900 L 1640 900", "color": "ink", "width": 4, "start": C("Outstanding shares are"), "label": lbl("BILLIONS OF SHARES · 424B4 · OUR BUILD-UP", 1120, 950, 18, "ink")},
    bar(660, 260, 900, 470, "accent2", C("Outstanding shares are"), "OUTSTANDING 13.2"),
    bar(1120, 260, 900, 470, "accent2", C("Now add"), "SAME 13.2"),
    {"d": rect(1120, 400, 260, 70), "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.45, "kind": "bar", "start": C("employee stock options"), "label": lbl("+ OPTIONS 1.77", 1250, 445, 20, "ink")},
    {"d": rect(1120, 355, 260, 45), "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.45, "kind": "bar", "start": C("stock awards still vesting"), "label": lbl("+ RSUs 1.03", 1250, 385, 18, "ink")},
    {"d": rect(1120, 300, 260, 55), "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.35, "kind": "bar", "start": C("notes Amazon holds"), "label": lbl("+ AMAZON NOTES ETC.", 1250, 335, 18, "ink")},
    {"d": rect(1100, 270, 300, 640), "color": "ink", "width": 5, "kind": "box", "start": C("fully diluted count"), "label": lbl("FULLY DILUTED ≈ 17.6-18", 1250, 255, 24, "ink")},
    {"d": arrow((940, 560), (1090, 330), -0.2), "color": "accent", "width": 6, "kind": "arrow", "start": C("than today"), "label": lbl("≈ +1/3", 970, 420, 26, "accent")},
], C("ask which count", 0.1), [1250, 320], sources=["ant_424b4", "cnbc_price"])
stage("s10_dilute", "c1_dilute", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("Each time the share price"), 1000, 520, 1.05, 1.6), (C("A slightly smaller slice"), 960, 540, 1.0, 1.2)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="THE COUNT CAN KEEP GROWING", at=0.2, size=54, color="gold"),
              it("sign", x=960, y=240, text="AMAZON NOTES → CLASS N, EACH QUARTER, UP TO A CAP", at=C("Amazon's notes convert"), color=BLUE, size=26),
              it("sign", x=960, y=340, text="EMPLOYEE PLANS: AUTOMATIC ANNUAL TOP-UPS", at=C("Employee plans"), color=AMBER, size=26),
              it("sign", x=960, y=440, text="PUBLIC BENEFIT FUND: UP TO +2% OF SHARES EACH +50% PRICE MILESTONE", at=C("Each time the share price"), color=GREEN, size=22),
              it("sign", x=960, y=525, text="BOARD'S DISCRETION · 424B4", at=C("the board may hand"), color=CREAM, size=20),
              it("pie", x=640, y=800, r=150, at=C("Good for its mission"), title="TODAY", slices=[{"v": 10, "color": "#FFB547", "label": "YOU", "at": C("Good for its mission")}, {"v": 90, "color": "#5E6B85", "at": C("Good for its mission")}]),
              it("pie", x=1280, y=800, r=150, at=C("A slightly smaller slice"), title="MORE SHARES", total=115,
                 slices=[{"v": 10, "color": "#FFB547", "label": "YOU", "at": C("A slightly smaller slice")}, {"v": 90, "color": "#5E6B85", "at": C("A slightly smaller slice")}, {"v": 15, "color": "#FF5C7A", "label": "NEW", "at": C("A slightly smaller slice", 0.4)}]),
              it("sign", x=960, y=1010, text="ILLUSTRATION, NOT TO SCALE", at=C("A slightly smaller slice"), color=CREAM, size=18)]},
    sources=["ant_424b4"])
kinetic("s11_t1", "c1_transition", [("So that's what you own.", 66, "So that's what you own", None, False),
                                    ("Now, what are you paying?", 72, "what are you paying", "gold", False)])

# ====================================================================== 2: the price you pay
card("s12_c2", "c2_card", "The Price You Pay", "Price to sales, our calculation")
stage("s13_ps", "c2_ps", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 520, 1.05), (C("Take the latest close"), 960, 540, 1.0, 1.6), (C("By our math"), 960, 500, 1.06, 1.2)), "drift": 1,
    "items": [it("letters", x=960, y=110, text="P/E? NOT USEFUL YET", at=C("doesn't work"), size=54, color="gold", until=C("Investors use price to sales")),
              it("letters", x=960, y=110, text="PRICE ÷ SALES", at=C("Investors use price to sales"), size=60, color="gold"),
              it("sign", x=960, y=260, text="$97.17 (NOV 19 CLOSE) × 13.22BN SHARES ≈ $1.28T", at=C("multiply by the shares"), color=AMBER, size=28),
              it("sign", x=960, y=370, text="÷ REVENUE, LAST 12 MONTHS ≈ $35.3BN (424B4)", at=C("divide by the last year"), color=BLUE, size=28),
              it("counter", x=960, y=560, at=C("By our math"), prefix="≈ ", suffix="×", decimals=1, steps=[[0, 0], [{"cue": "sales"}, 36.4]], text="ANT PRICE / SALES (OUR CALC)", scale=1.25),
              it("sign", x=960, y=760, text="FULLY DILUTED: ≈ 50× · MARKET VALUE, NOT EV", at=C("By our math", 1.5), color=CREAM, size=24),
              stamp(1560, 930, at=C("By our math"), scale=0.6),
              ANT(320, 880, at=0.4, mood="cool", moods=[[C("By our math"), "shock"]], hop=18)]},
    sources=["ant_424b4", "px", "national"])
board("p14_ps", "c2_draw", "Price ÷ trailing sales (our calc, Nov 19, 2026 closes)", C("Here's Nvidia"), [
    {"d": "M 600 900 L 1640 900", "color": "ink", "width": 4, "start": C("Here's Nvidia"), "label": lbl("MARKET VALUE ÷ LAST 12 MONTHS' REVENUE · FILINGS · OUR CALC", 1120, 950, 18, "ink")},
    bar(680, 220, 900, 755, "accent2", C("Here's Nvidia"), "NVIDIA ≈ 9.7×"),
    bar(960, 220, 900, 740, "accent3", C("Here's Microsoft"), "MICROSOFT ≈ 10.7×"),
    bar(1260, 220, 900, 330, "accent", C("And here's A, N, T"), "ANT ≈ 36×"),
    {"d": arrow((1080, 700), (1250, 380), -0.15), "color": "risk", "width": 5, "kind": "arrow", "start": C("Same yardstick"), "label": lbl("≈ 3.5×", 1110, 520, 24, "risk")},
], C("Very different height", 0.1), [1370, 360], sources=["peers", "px", "ant_424b4"])
stage("s15_growth", "c2_growth", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("That's the bull case"), 900, 520, 1.04, 1.2), (C("The bear case"), 1040, 520, 1.04, 1.2)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="IS THAT CRAZY?", at=0.2, size=60, color="gold"),
              it("calendar", x=520, y=420, at=C("many times what it was"), pages=[[0, "$2.5BN", "JAN-SEP 2025"], [C("a year earlier"), "$33.2BN", "JAN-SEP 2026"]]),
              it("sign", x=1300, y=290, text="ON THE OCT 31 RUN RATE (≈$81BN): ≈ 16× (OUR CALC)", at=C("Measured against its latest"), color=BLUE, size=24),
              it("sign", x=1300, y=430, text="BULL: GROWTH CAN SHRINK THE MULTIPLE", at=C("That's the bull case"), color=GREEN, size=30),
              it("sign", x=1300, y=560, text="BEAR: FAST GROWTH RARELY LASTS FOREVER", at=C("The bear case"), color=PINK, size=30),
              it("sign", x=1300, y=680, text="RUN RATE = A SNAPSHOT, NOT REVENUE EARNED", at=C("stretched over a year"), color=CREAM, size=22),
              ANT(1750, 880, at=0.3, mood="happy", moods=[[C("The bear case"), "worry"]], hop=16)]},
    sources=["ant_424b4"])
stage("s16_value", "c2_value", {
    "zones": [Z("vault")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("So its enterprise value"), 1000, 520, 1.05, 1.6)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="ONE MORE LABEL TO CHECK", at=0.2, size=56, color="gold", until=C("So its enterprise value")),
              it("sign", x=640, y=260, text="CASH + SHORT-TERM INVESTMENTS ≈ $132BN (SEP 30)", at=C("a big pile of cash"), color=GREEN, size=24),
              it("sign", x=640, y=370, text="+ ≈ $105BN NET FROM THE OFFERING + PLACEMENT", at=C("the money from this offering"), color=GREEN, size=24),
              it("sign", x=640, y=480, text="DEBT ≈ $6.2BN", at=C("very little debt"), color=PINK, size=28),
              it("letters", x=960, y=110, text="MARKET VALUE ≠ ENTERPRISE VALUE", at=C("So its enterprise value"), size=50, color="gold"),
              it("sign", x=1350, y=620, text="OUR MULTIPLE USES MARKET VALUE", at=C("Our multiple uses"), color=AMBER, size=28),
              coins(300, 760, [1500, 820], at=C("a big pile of cash"), rate=5),
              MAYA(1720, 0.0, pose="stand", faces=[[0, "squint"], [C("Whatever headline"), "smug"]], scale=1.0)]},
    sources=["ant_424b4"])

# ====================================================================== 3: the lock-up calendar
card("s17_c3", "c3_card", "The Lock-Up Calendar", "When insiders can sell (424B4)")
stage("s18_waves", "c3_waves", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 520, 1.0), (C("It's a staircase"), 960, 540, 1.0, 1.0)), "drift": 1,
    "items": [it("floodgates", x=960, y=560, at=0.2, scale=0.92, w=1500, title="THE LOCK-UP STAIRCASE (UP TO, 424B4)", level=[[0, 1], [{"cue": "a bigger wave follows"}, 0.85]],
                 gates=[{"date": "NOV 19", "amt": "315M", "size": 0.2, "at": C("Some employee shares")},
                        {"date": "DEC 15", "amt": "303M", "size": 0.2, "at": C("More unlock in steps")},
                        {"date": "JAN 5", "amt": "303M", "size": 0.2, "at": C("More unlock in steps", 0.5)},
                        {"date": "JAN 19", "amt": "353M", "size": 0.25, "at": C("January and February")},
                        {"date": "FEB 2", "amt": "353M", "size": 0.25, "at": C("January and February", 0.6)},
                        {"date": "2026 RESULTS", "amt": "1.7BN", "size": 0.7, "at": C("a bigger wave follows")}],
                 note="SHARES THAT MAY BE SOLD, NOT SHARES THAT WILL BE SOLD"),
              it("letters", x=960, y=110, text="NOT ONE CLIFF: A STAIRCASE", at=C("It's a staircase"), size=52, color="gold")]},
    sources=["ant_424b4"], sfx=[{"kind": "whoosh", "cue": "a bigger wave follows", "gain": 0.3}])
stage("s19_gate", "c3_gate", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("at the very latest"), 960, 500, 1.08, 1.4)), "drift": 1,
    "items": [it("letters", x=960, y=110, text="THE BIG GATE", at=0.2, size=64, color="gold"),
              it("calendar", x=960, y=470, at=0.3, scale=1.2, color="#E5483B", pages=[[0, "?", "2027"], [C("at the very latest"), "MAY 17", "2027"]]),
              it("sign", x=960, y=760, text="OR EARLIER: 2 TRADING DAYS AFTER THE JAN-MAR RESULTS", at=C("right after the results"), color=AMBER, size=26),
              it("sign", x=960, y=860, text="DAY 180 AFTER THE PROSPECTUS (NOV 18, 2026) · 424B4", at=C("at the very latest"), color=CREAM, size=22),
              MAYA(330, 0.0, pose="stand", faces=[[0, "squint"], [C("at the very latest"), "shock"]], scale=1.0)]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "at the very latest", "gain": 0.35}])
stage("s20_size", "c3_size", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": STILL(), "drift": 1,
    "items": [it("floodgates", x=960, y=560, at=0.1, scale=0.92, w=1300, title="THE BIGGEST STEP (UP TO, 424B4)", level=[[0, 1], [{"cue": "the biggest single step"}, 0.6]],
                 gates=[{"date": "EARLIER STEPS", "amt": "SEE BEFORE", "size": 0.3, "at": 0.0},
                        {"date": "MAY 17, 2027*", "amt": "UP TO 3.0BN", "size": 1.0, "at": C("Behind that gate")},
                        {"date": "NOV 18, 2027*", "amt": "UP TO 1.9BN", "size": 0.65}],
                 note="* OR EARLIER, AFTER RESULTS · CLASS A + CLASS N"),
              it("letters", x=960, y=110, text="UP TO 3.0 BILLION SHARES", at=C("Behind that gate"), size=56, color="gold")]},
    sources=["ant_424b4"], sfx=[{"kind": "whoosh", "cue": "Behind that gate", "gain": 0.3}])
stage("s21_year", "c3_year", {
    "zones": [Z("depository")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("Up to a full year"), 1000, 520, 1.05, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="THE LONGEST WAIT", at=0.2, size=60, color="gold"),
              it("sign", x=960, y=260, text="CO-FOUNDERS + HOLDERS ABOVE 0.5% (FULLY DILUTED)", at=C("The co-founders"), color=BLUE, size=26),
              it("calendar", x=700, y=560, at=C("Up to a full year"), pages=[[0, "365", "DAYS"], [C("the following November"), "NOV 18", "2027"]]),
              it("sign", x=1300, y=500, text="OR EARLIER: 2 TRADING DAYS AFTER JUL-SEP 2027 RESULTS", at=C("results for next summer"), color=AMBER, size=22),
              it("sign", x=1300, y=620, text="UP TO 1.9BN SHARES · TIMED EARLY RELEASES APPLY", at=C("the following November"), color=CREAM, size=22)]},
    sources=["ant_424b4"])
stage("s22_meaning", "c3_meaning", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("so Maya writes"), 900, 540, 1.06, 1.2), (C("One more detail"), 1040, 520, 1.0, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="UNLOCKED ≠ SOLD", at=0.2, size=64, color="gold"),
              it("sign", x=1150, y=260, text="MORE SHARES THAT CAN BE SOLD = MORE POSSIBLE SELLERS", at=C("But more shares"), color=PINK, size=26),
              it("checklist", x=560, y=640, at=C("so Maya writes"), scale=0.55, title="DATES TO WATCH",
                 rows=[{"text": "DEC 15 · JAN 5 · JAN 19 · FEB 2", "at": C("so Maya writes")}, {"text": "AFTER THE 2026 RESULTS", "at": C("so Maya writes", 0.4)},
                       {"text": "MAY 17, 2027 OR EARLIER", "at": C("so Maya writes", 0.8)}, {"text": "NOV 18, 2027 OR EARLIER", "at": C("so Maya writes", 1.2)}]),
              it("sign", x=1250, y=470, text="PRIVATE PLACEMENT ($26BN AT $83): NOT LOCKED UP", at=C("One more detail"), color=BLUE, size=24),
              it("sign", x=1250, y=580, text="BUT RESTRICTED SECURITIES (RULE 144) · 424B4", at=C("their shares are restricted"), color=CREAM, size=24),
              MAYA(1650, 0.0, pose="stand", faces=[[0, "happy"], [C("so Maya writes"), "squint"]], scale=1.0)]},
    sources=["ant_424b4"])

# ====================================================================== 4: the first report card
card("s23_c4", "c4_card", "The First Report Card", "What to watch in the first results")
stage("s24_when", "c4_when", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("But it matters twice"), 1000, 520, 1.05, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="REPORT CARD #1 AS A PUBLIC COMPANY", at=0.2, size=48, color="gold"),
              it("calendar", x=620, y=470, at=C("will cover this full year"), pages=[[0, "2026", "FULL YEAR"], [C("should arrive early next year"), "EARLY", "2027"], [C("The date hasn't"), "TBA", "DATE"]]),
              it("sign", x=1250, y=330, text="1 · FIRST FRESH NUMBERS SINCE THE OFFERING", at=C("It's the first fresh look"), color=BLUE, size=26),
              it("sign", x=1250, y=450, text="2 · TRIGGERS A LOCK-UP STEP (UP TO 1.7BN)", at=C("the trigger"), color=PINK, size=26),
              MAYA(1250, 0.0, pose="stand", faces=[[0, "happy"], [C("But it matters twice"), "squint"]], scale=1.0)]},
    sources=["ant_424b4"])
board("p25_report", "c4_draw", "The first report card: four lines to read", C("First, revenue growth"), [
    {"d": rect(560, 300, 470, 120), "color": "accent3", "width": 5, "kind": "box", "start": C("First, revenue growth"), "label": lbl("1 · REVENUE GROWTH", 795, 372, 24, "accent3")},
    {"d": rect(560, 450, 470, 120), "color": "accent", "width": 5, "kind": "box", "start": C("Second, the compute bill"), "label": lbl("2 · COMPUTE COST PER $1", 795, 522, 24, "accent")},
    {"d": rect(560, 600, 470, 120), "color": "accent2", "width": 5, "kind": "box", "start": C("Third, operating cash flow"), "label": lbl("3 · OPERATING CASH FLOW", 795, 672, 24, "accent2")},
    {"d": rect(560, 750, 470, 120), "color": "risk", "width": 5, "kind": "box", "start": C("And fourth"), "label": lbl("4 · COMMITMENTS: HOW MUCH, WHEN", 795, 822, 20, "risk")},
    {"d": rect(1260, 470, 360, 220), "color": "ink", "width": 6, "kind": "box", "start": C("First, revenue growth", 0.6), "label": lbl("THE REPORT CARD", 1440, 590, 26, "ink")},
    {"d": arrow((1035, 360), (1255, 520), 0.1), "color": "accent3", "width": 5, "kind": "arrow", "start": C("Is the rocket")},
    {"d": arrow((1035, 510), (1255, 560), 0.05), "color": "accent", "width": 5, "kind": "arrow", "start": C("for each dollar of sales")},
    {"d": arrow((1035, 660), (1255, 620), -0.05), "color": "accent2", "width": 5, "kind": "arrow", "start": C("Is real cash")},
    {"d": arrow((1035, 810), (1255, 660), -0.1), "color": "risk", "width": 5, "kind": "arrow", "start": C("and when")},
], C("and when", 0.3), [1440, 580], sources=["ant_424b4"])
stage("s26_cost", "c4_cost", {
    "zones": [Z("datacenter")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("If that keeps falling"), 1000, 520, 1.04, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="THE ONE TO WATCH: THE COMPUTE BILL", at=0.2, size=50, color="gold"),
              it("counter", x=960, y=290, at=C("Last year"), prefix="$", suffix="", decimals=2, steps=[[0, 1.60], [{"cue": "So far this year"}, 1.60], [{"cue": "for every dollar"}, 0.57]],
                 text="COMPUTE COST PER $1 OF SALES (OUR CALC, 424B4)", scale=1.15),
              it("sign", x=640, y=480, text="2025: ≈ $1.60", at=C("Last year"), color=PINK, size=30),
              it("sign", x=1280, y=480, text="JAN-SEP 2026: ≈ $0.57", at=C("So far this year"), color=GREEN, size=30),
              it("sign", x=640, y=620, text="KEEPS FALLING → MARGINS OPEN UP", at=C("If that keeps falling"), color=GREEN, size=26),
              it("sign", x=1280, y=620, text="CLIMBS BACK → HARDER STORY", at=C("If it climbs back"), color=PINK, size=26),
              ANT(1750, 880, at=0.3, mood="worry", moods=[[C("So far this year"), "happy"], [C("If it climbs back"), "worry"]], hop=14)]},
    sources=["ant_424b4"])
stage("s27_cash", "c4_cash", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 520, 1.0), (C("On the other side"), 1000, 520, 1.04, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="THE PROMISES VS THE CASH", at=0.2, size=56, color="gold"),
              it("counter", x=620, y=290, at=C("has signed up to spend"), prefix="≈ $", suffix="BN", decimals=0, steps=[[0, 0], [{"cue": "on computing and data centers"}, 900.9]], text="COMMITMENTS TO 2045 (424B4)"),
              it("sign", x=620, y=470, text="≈ $70.7BN DUE IN THE 12 MONTHS AFTER SEP 30", at=C("much of it owed"), color=PINK, size=24),
              it("sign", x=1320, y=290, text="CASH + INVESTMENTS ≈ $132BN + IPO PROCEEDS", at=C("a large cash cushion"), color=GREEN, size=24),
              it("sign", x=1320, y=400, text="OPERATING CASH FLOW, JAN-SEP 2026: +$6.6BN", at=C("turned positive"), color=GREEN, size=24),
              it("sign", x=960, y=600, text="COMMITMENT ≠ DEBT ≠ EXPENSE · DEBT IS $6.2BN", at=C("The report will show"), color=CREAM, size=24),
              coins(300, 780, [1600, 820], at=C("turned positive"), rate=4)]},
    sources=["ant_424b4"])

# ====================================================================== 5: who it depends on
card("s28_c5", "c5_card", "Who It Depends On", "Partners, chips and customers")
stage("s29_partners", "c5_partners", {
    "zones": [Z("dccity")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("Partner, landlord"), 960, 500, 1.06, 1.2)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="AMAZON AND GOOGLE", at=C("Start with Amazon"), size=58, color="gold", until=C("Partner, landlord")),
              it("sign", x=560, y=270, text="SHAREHOLDERS: 14.6% · 13.4%", at=C("Both are big shareholders"), color=AMBER, size=26),
              it("sign", x=1360, y=270, text="THEY RENT IT COMPUTING", at=C("Both rent it"), color=BLUE, size=26),
              it("sign", x=560, y=390, text="THEY RESELL CLAUDE IN THEIR CLOUDS", at=C("Both sell Claude"), color=GREEN, size=24),
              it("sign", x=1360, y=390, text="THEY BUILD RIVAL AI MODELS", at=C("both build A I models"), color=PINK, size=26),
              it("letters", x=960, y=110, text="PARTNER · LANDLORD · SALESMAN · RIVAL", at=C("Partner, landlord"), size=44, color="gold"),
              it("isodc", x=960, y=760, at=0.3, n=6, step=0.25, cols=3, scale=0.6, glow=True),
              ANT(1750, 880, at=0.3, mood="cool", moods=[[C("both build A I models"), "worry"]], hop=14)]},
    sources=["ant_424b4", "amzn_10q"])
board("p30_loop", "c5_draw", "The partner triangle (424B4, Amazon 10-Q)", C("Amazon invests"), [
    {"d": rect(560, 300, 340, 150), "color": "accent2", "width": 6, "kind": "box", "start": C("Amazon invests"), "label": lbl("AMAZON (SHAREHOLDER)", 730, 382, 22, "accent2")},
    {"d": rect(1240, 300, 340, 150), "color": "accent", "width": 6, "kind": "box", "start": C("Amazon invests"), "label": lbl("ANT (ANTHROPIC)", 1410, 382, 24, "accent")},
    {"d": rect(900, 700, 340, 150), "color": "accent3", "width": 6, "kind": "box", "start": C("Amazon's cloud customers"), "label": lbl("CLOUD CUSTOMERS", 1070, 782, 22, "accent3")},
    {"d": arrow((905, 340), (1235, 340), -0.1), "color": "accent", "width": 6, "kind": "arrow", "start": C("Amazon invests", 0.4), "label": lbl("INVESTS", 1070, 300, 20, "ink")},
    {"d": arrow((1235, 420), (905, 420), -0.1), "color": "accent2", "width": 6, "kind": "arrow", "start": C("pays Amazon for computing"), "label": lbl("PAYS FOR COMPUTE", 1070, 470, 20, "ink")},
    {"d": arrow((1060, 695), (760, 455), 0.15), "color": "accent3", "width": 5, "kind": "arrow", "start": C("buy Claude"), "label": lbl("BUY CLAUDE", 820, 600, 20, "ink")},
    {"d": arrow((910, 455), (1300, 455), 0.25), "color": "accent3", "width": 4, "kind": "arrow", "start": C("keeps a cut"), "label": lbl("PAYS ANT, MINUS A CUT", 1260, 580, 18, "ink")},
    {"d": rect(1300, 860, 320, 70), "color": "muted", "width": 3, "kind": "box", "start": C("Google sits"), "label": lbl("GOOGLE: SIMILAR TRIANGLE", 1460, 902, 18, "ink")},
    {"d": rect(540, 910, 700, 70), "color": "risk", "width": 4, "kind": "box", "start": C("conflicts of"), "label": lbl("424B4: 'CONFLICTS OF INTEREST' RISK", 890, 952, 20, "risk")},
], C("access to computing", 0.1), [1070, 400], sources=["ant_424b4", "amzn_10q"])
stage("s31_chips", "c5_chips", {
    "zones": [Z("serverfarm")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("The flip side"), 1000, 520, 1.05, 1.2)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="FOUR CHIP FAMILIES", at=0.2, size=58, color="gold", until=C("The flip side")),
              it("sign", x=420, y=280, text="AWS TRAINIUM", at=C("chips from Amazon"), color=BLUE, size=28),
              it("sign", x=800, y=280, text="GOOGLE TPUs", at=C("Google, Nvidia"), color=BLUE, size=28),
              it("sign", x=1160, y=280, text="NVIDIA GPUs", at=C("Nvidia and A M D"), color=BLUE, size=28),
              it("sign", x=1520, y=280, text="AMD GPUs", at=C("Nvidia and A M D", 0.4), color=BLUE, size=28),
              it("sign", x=960, y=420, text="NO SINGLE CHOKE POINT", at=C("no single supplier"), color=GREEN, size=34),
              it("letters", x=960, y=110, text="THE FLIP SIDE", at=C("The flip side"), size=58, color="gold"),
              it("sign", x=960, y=540, text="SEVERAL SUPPLIERS ARE ALSO SHAREHOLDERS · HUGE COMMITMENTS", at=C("also shareholders"), color=PINK, size=26),
              it("hbm", x=960, y=800, at=0.4, scale=0.8)]},
    sources=["ant_424b4"])
stage("s32_customers", "c5_customers", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("But a big share"), 1000, 520, 1.04, 1.4)), "drift": 2,
    "items": [it("letters", x=960, y=110, text="AND THE CUSTOMERS?", at=0.2, size=58, color="gold"),
              it("pie", x=560, y=520, r=170, at=C("Last year"), title="2025",
                 slices=[{"v": 12, "color": "#FF5C7A", "label": "A 12%", "at": C("Last year")}, {"v": 12, "color": "#FFB547", "label": "B 12%", "at": C("Last year", 0.3)},
                         {"v": 76, "color": "#5CC8FF", "label": "ALL OTHERS", "at": C("Last year", 0.6)}]),
              it("pie", x=1060, y=520, r=170, at=C("So far this year"), title="JAN-SEP 2026",
                 slices=[{"v": 50, "color": "#7DFF8A", "label": "NO ONE\n≥ 10%", "at": C("So far this year")}, {"v": 50, "color": "#7DFF8A", "at": C("So far this year")}]),
              it("sign", x=820, y=820, text="A HEALTHIER SPREAD", at=C("a healthier spread"), color=GREEN, size=30),
              it("sign", x=1300, y=900, text="VIA CLOUD MARKETPLACES: 44% OF SALES", at=C("But a big share"), color=PINK, size=24),
              MAYA(1790, 0.0, pose="stand", faces=[[0, "squint"], [C("a healthier spread"), "happy"], [C("But a big share"), "worry"]], scale=1.0)]},
    sources=["ant_424b4"])

# ====================================================================== 6: new-IPO weather
FB = [[0.0, 38.23], [0.032, 29.6], [0.064, 27.4], [0.096, 33.05], [0.129, 31.47], [0.161, 28.09], [0.193, 23.71], [0.225, 20.72], [0.249, 19.87], [0.257, 20.01],
      [0.289, 19.09], [0.297, 17.73], [0.321, 20.93], [0.353, 20.79], [0.386, 21.95], [0.418, 19.48], [0.45, 21.94], [0.482, 19.21], [0.514, 24.32], [0.546, 27.46],
      [0.578, 26.81], [0.61, 26.05], [0.643, 30.59], [0.675, 30.73], [0.707, 29.73], [0.739, 27.91], [0.771, 27.39], [0.803, 27.96], [0.835, 25.86], [0.867, 25.42],
      [0.9, 27.4], [0.932, 26.11], [0.964, 27.57], [1.0, 26.25]]
ARM = [[0.0, 63.59], [0.031, 53.52], [0.062, 54.08], [0.094, 51.9], [0.102, 47.87], [0.125, 47.9], [0.156, 51.58], [0.188, 58.66], [0.219, 61.93], [0.25, 70.74],
       [0.281, 74.25], [0.312, 71.88], [0.344, 77.11], [0.375, 70.52], [0.391, 77.01], [0.395, 113.89], [0.406, 119.98], [0.438, 146.2], [0.469, 140.85], [0.5, 124.59],
       [0.531, 126.91], [0.562, 131.13], [0.594, 96.04], [0.625, 101.7], [0.656, 113.67], [0.688, 124.94], [0.719, 136.57], [0.75, 160.77], [0.781, 163.46],
       [0.812, 177.53], [0.844, 149.14], [0.875, 113.39], [0.906, 130.3], [0.938, 125.32], [0.969, 127.22], [1.0, 138.9]]
card("s33_c6", "c6_card", "New-IPO Weather", "How two tech IPOs moved in their first year")
stage("s34_fb", "c6_fb", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": cam((0, 960, 540, 1.0), (C("A year after"), 960, 540, 1.02, 1.4)), "drift": 1,
    "items": [it("ipopath", x=960, y=560, at=0.2, scale=0.95, title="FACEBOOK, YEAR ONE (MAY 2012 - MAY 2013) · DAILY CLOSES", points=FB, lo=10, hi=45, offer=38,
                 offerText="OFFER $38", color="#5CC8FF",
                 draw=[[0, 0], [{"cue": "Within a few months"}, 0.05], [{"cue": "the first lock-up ended"}, 0.3], [{"cue": "A year after"}, 0.55], [{"cue": "still below the"}, 1.0]],
                 marks=[{"x": 0.249, "text": "AUG 16: FIRST LOCK-UP ENDS", "at": C("the first lock-up ended"), "color": "#FFCDD2"},
                        {"x": 0.297, "text": "LOW CLOSE $17.73 (SEP 4)", "at": C("its shares had fallen"), "color": "#FFE0B2", "below": True},
                        {"x": 1.0, "text": "1 YEAR: $26.25", "at": C("still below the"), "color": "#BBDEFB"}],
                 foot="SOURCES: AP (LOCK-UP), YAHOO FINANCE DAILY CLOSES · PAST PATTERNS DON'T PREDICT ANT")]},
    sources=["fb_lock", "fb_px"], sfx=[{"kind": "whoosh", "cue": "its shares had fallen", "gain": 0.25}])
stage("s35_arm", "c6_arm", {
    "zones": [Z("newsroom")], "worldW": 2400,
    "cam": cam((0, 960, 540, 1.0), (C("in a single day"), 960, 520, 1.04, 1.2)), "drift": 1,
    "items": [it("ipopath", x=960, y=560, at=0.2, scale=0.95, title="ARM, YEAR ONE (SEP 2023 - SEP 2024) · DAILY CLOSES", points=ARM, lo=30, hi=190, offer=51,
                 offerText="OFFER $51", color="#7DFF8A",
                 draw=[[0, 0], [{"cue": "popped on day one"}, 0.02], [{"cue": "slipped below its offer"}, 0.12], [{"cue": "Months later"}, 0.39], [{"cue": "in a single day"}, 1.0]],
                 marks=[{"x": 0.0, "text": "DAY 1 CLOSE $63.59", "at": C("popped on day one"), "color": "#C8E6C9"},
                        {"x": 0.102, "text": "OCT 20: $47.87", "at": C("slipped below its offer"), "color": "#FFCDD2", "below": True},
                        {"x": 0.395, "text": "FEB 8, 2024: +48% IN A DAY", "at": C("the stock jumped"), "color": "#FFE0B2"}],
                 foot="SOURCES: BLOOMBERG (FEB 8, 2024), YAHOO FINANCE DAILY CLOSES · PAST PATTERNS DON'T PREDICT ANT")]},
    sources=["arm_ipo", "arm_px"], sfx=[{"kind": "hit", "cue": "the stock jumped", "gain": 0.3}])
stage("s36_lesson", "c6_lesson", {
    "zones": [Z("livingroom")], "worldW": 2400,
    "cam": cam((0, 960, 540, 1.0), (C("Those are exactly"), 1040, 520, 1.06, 1.2)), "drift": 1,
    "items": [clip([0] * 7, [[0, -1], [C("lock-up dates"), 2], [C("earnings reports"), 3]], ticks=[None, None, C("Those are exactly"), C("Those are exactly", 0.3), None, None, None],
                   x=1150, y=560, at=0.1, scale=0.9),
              it("letters", x=1150, y=70, text="IN BOTH CASES: BIG MOVES NEAR LOCK-UPS + REPORTS", at=C("In both of these cases"), size=36, color="gold"),
              MAYA(380, 0.0, pose="stand", faces=[[0, "squint"], [C("Those are exactly"), "grin"]])]},
    sources=["fb_lock", "arm_ipo"])

# ====================================================================== 7: who is in charge
card("s37_c7", "c7_card", "Who Is in Charge", "Public benefit corporation + trust")
stage("s38_pbc", "c7_pbc", {
    "zones": [Z("trustroom")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("By law"), 1000, 520, 1.04, 1.4)), "drift": 1,
    "items": [it("letters", x=960, y=110, text="A PUBLIC BENEFIT CORPORATION", at=C("public benefit corporation"), size=54, color="gold"),
              it("sign", x=480, y=300, text="SHAREHOLDERS' MONEY", at=C("shareholders' money"), color=AMBER, size=30),
              it("sign", x=960, y=300, text="PEOPLE AFFECTED", at=C("people affected"), color=BLUE, size=30),
              it("sign", x=1440, y=300, text="THE MISSION", at=C("a stated mission"), color=GREEN, size=30),
              it("sign", x=960, y=440, text="'RESPONSIBLE DEVELOPMENT ... OF ADVANCED AI FOR THE LONG-TERM BENEFIT OF HUMANITY' (424B4)", at=C("the responsible development"), color=CREAM, size=20),
              ANT(960, 880, at=0.3, mood="cool", hop=12)]},
    sources=["ant_424b4"])
stage("s39_trust", "c7_trust", {
    "zones": [Z("parliament")], "worldW": 2400,
    "cam": cam((0, 960, 520, 1.0), (C("controlled company"), 960, 520, 1.04, 1.2)), "drift": 1,
    "items": [it("letters", x=960, y=110, text="THE LONG-TERM BENEFIT TRUST", at=0.2, size=54, color="gold"),
              it("sign", x=960, y=250, text="5 TRUSTEES · NO FINANCIAL STAKE (424B4)", at=C("no financial stake"), color=GREEN, size=28),
              it("govtower", x=960, y=780, at=0.3, scale=0.8, seats=9, trust=5, trustAt=C("they elect most of the board"),
                 labels={"trust": "CLASS T ELECTS THE MAJORITY OF THE BOARD"}),
              it("sign", x=960, y=370, text="'CONTROLLED COMPANY': MAY OPT OUT OF SOME NASDAQ RULES", at=C("controlled company"), color=PINK, size=24)]},
    sources=["ant_424b4"])
stage("s40_meaning", "c7_meaning", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": cam((0, 960, 520, 1.0), (C("Either way"), 960, 500, 1.04, 1.2)), "drift": 1,
    "items": [scale([("TRUST MAY HAVE OTHER INTERESTS", C("may have interests")), ("IT MAY ACT IN WAYS YOU DISLIKE", C("could use its power"))],
                    [("SHIELDS LONG-TERM THINKING", C("Supporters say")), ("LESS SHORT-TERM PRESSURE", C("short-term pressure"))],
                    title="WHAT IT MEANS FOR A BUYER", leftLabel="424B4 RISK FACTOR", rightLabel="SUPPORTERS SAY", x=960, y=330, at=0.1, scale=0.95),
              it("sign", x=960, y=915, text="YOUR VOTE HAS LIMITS", at=C("your vote has limits"), color=CREAM, size=32)]},
    sources=["ant_424b4"])

# ====================================================================== 8: what would change the picture
card("s41_c8", "c8_card", "What Would Change the Picture", "Bullish and bearish signals, same weight")
BULL = [("REVENUE KEEPS GROWING FAST", "revenue that keeps growing"), ("COMPUTE COST PER $1 FALLS", "a compute bill that keeps"),
        ("CASH FLOW STAYS POSITIVE", "cash flow that stays"), ("LOCK-UPS PASS QUIETLY", "lock-up waves that pass")]
BEAR = [("GROWTH SLOWS SHARPLY", "growth that slows"), ("COMPUTE COST CLIMBS BACK", "a compute bill that climbs"),
        ("CASH LAGS COMMITMENTS", "cash that can't keep pace"), ("BIG HOLDERS EXIT AT GATES", "big holders heading")]
stage("s42_bull", "c8_bull", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": STILL(), "drift": 1,
    "items": [scale([], [(t_, C(c_)) for t_, c_ in BULL], title="BULLISH SIGNALS", leftLabel="BEARISH", rightLabel="BULLISH", x=960, y=330, at=0.1, scale=0.95),
              ANT(1750, 880, at=0.3, mood="happy", hop=20)]},
    sources=["ant_424b4"])
stage("s43_bear", "c8_bear", {
    "zones": [Z("studio", night=True)], "worldW": 1920, "night": True,
    "cam": STILL(), "drift": 1,
    "items": [scale([(t_, C(c_)) for t_, c_ in BEAR], [(t_, 0) for t_, _ in BULL], title="BULLISH VS BEARISH (SAME WEIGHT)", leftLabel="BEARISH", rightLabel="BULLISH", x=960, y=330, at=0.0, scale=0.95),
              ANT(170, 880, at=0.3, mood="worry", hop=12)]},
    sources=["ant_424b4"])
stage("s44_close", "c8_close", {
    "zones": [Z("livingroom")], "worldW": 2400,
    "cam": cam((0, 960, 540, 1.0), (C("this is not investment advice"), 1100, 520, 1.06, 1.2)), "drift": 1,
    "items": [clip([0] * 7, [[0, -1]], ticks=[C("what she would own"), C("what she would pay"), C("which dates to watch"), C("which dates to watch", 0.3),
                                              C("which dates to watch", 0.6), C("which dates to watch", 0.9), C("which dates to watch", 1.2)],
                   x=1150, y=560, at=0.1, scale=0.9, stamp={"text": "NOT INVESTMENT ADVICE", "at": C("this is not investment advice")}),
              it("sign", x=1150, y=1010, text="PRICES: NOV 19, 2026 CLOSE · SOURCES IN THE DESCRIPTION", at=C("first day's close"), color=CREAM, size=22),
              stamp(400, 330, at=C("first day's close"), scale=0.5),
              MAYA(380, 0.0, pose="stand", faces=[[0, "happy"], [C("we're not deciding"), "smug"], [C("which dates to watch"), "grin"]])]},
    sources=["ant_424b4", "px"])
add("s45_end", "teaser", "end_card", {"words": ["Next in the series:", "another giant, opened up the same way"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description · Not investment advice", "brand_cue": {"cue": "This is The Hidden Economics"}})


# ---------------------------------------------------------------- cue check
def cues(o):
    if isinstance(o, dict):
        if "cue" in o and isinstance(o["cue"], str) and set(o) <= {"cue", "offset"}:
            yield o["cue"]
        for v in o.values():
            yield from cues(v)
    elif isinstance(o, list):
        for v in o:
            yield from cues(v)


script = yaml.safe_load((ROOT / f"projects/{SLUG}/deliverables/documentary/script.yaml").read_text())
narr = {s["id"]: " ".join((s.get("narration") or "").split()).lower() for s in script["segments"]}
bad = [(s["segment"], c) for s in cartoon_kit.scenes for c in cues(s["params"]) if c.lower() not in narr.get(s["segment"], "")]
missing = [k for k in narr if k not in {s["segment"] for s in cartoon_kit.scenes}]
if bad or missing:
    raise SystemExit(f"cue check failed: {bad} missing segments: {missing}")
write(OUT, "# GENERATED by tools/gen_byb_anthropic_storyboard.py; edit the generator, not this file.\n"
           "# Before You Buy: Anthropic (Nov 2026 edition) storyboard; series kit tools/byb_kit.py; items CartoonStage/bybant.tsx.\n")
