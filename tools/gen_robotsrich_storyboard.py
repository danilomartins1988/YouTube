"""Generates projects/who-gets-rich-when-robots-do-the-work/deliverables/documentary/storyboard.yaml
(Episode 64: Who Gets Rich When Robots Do the Work?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/robotsrich.tsx (robotown, splitter, sharestreet, dcfield, moneyloop, evidencelab, millyard,
newjobs, doorways, rrtitle, rrbumper; items rrtag, bolt). Cast (fictional): DANA (warehouse shift lead), MILO (retired bus driver),
BOLT (original helper robot). No real person drawn; no logos.
Signature animations: 1 follow $100 (p04 board + s05 splitter), 2 who owns the stocks (s09-s11 sharestreet), 3 the AI money loop
(s14-s15 dcfield + p16 board + s17 moneyloop), 4 findings vs forecasts (evidencelab), 5 Engels' pause (s27 millyard + p28 board),
6 the doors to ownership (s36 doorways + p37 board).
Presenter boards: p04 $100 split, p06 labor-share line, p16 money loop, p28 Engels' pause, p37 doors.
Every number is tagged on screen with the rrtag pill: FACT / FINDING / FORECAST / DESCRIPTIVE / OUR MATH / ILLUSTRATIVE / EDUCATION.
Run: python tools/gen_robotsrich_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/who-gets-rich-when-robots-do-the-work/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE, GREY = "#2A6FDB", "#F2B33D", "#D9483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#1B2333", "#E07A2F", "#8E9AAF"


def toon(x, at=0.0, **kw):
    return it("toon", x=x, at=at, **kw)


def DANA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return toon(x, at, who="shopper", v=2, skin=2, hair=1, hairStyle=1, color=TEAL, glasses=False, scarf=GOLD, **kw)


def MILO(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return toon(x, at, who="shopper", v=3, skin=3, hair=0, hairStyle=0, color=ORANGE, glasses=True, scarf=NAVY, old=True, **kw)


def BOLT(x, at=0.0, **kw):
    return it("bolt", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def tag(*keys, at=0.0):
    return it("rrtag", at=at, x=36, y=36, tags=[[k[0], k[1]] for k in keys])


def counter(x, y, at, to, cue_to, text, prefix="", suffix="", decimals=0, until=None):
    kw = {"until": until} if until is not None else {}
    return it("counter", x=x, y=y, at=at, prefix=prefix, suffix=suffix, decimals=decimals, steps=[[0, 0], [at, 0], [cue_to, to]], text=text, **kw)


def bumper(id_, seg, num, title, caption, color):
    stage(id_, seg, {**W1("rrbumper", num=num, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom", "min_seconds": 4.2},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 1.0, "gain": 0.3}])


def board(id_, seg, title, start, strokes, actions, enter_left=True, sources=()):
    add(id_, seg, "engine_draw", {
        "title": title, "board": BOARD, "draw_start": start, "speed": 1600, "push": 0.003,
        "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3} if enter_left else {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
        "strokes": strokes, "actions": actions, "scale": 0.86, "floor": 1040}, sources=sources)


TOWN = dict(robots=3, workers=3)

# ====================================================================== HOOK
stage("s01_hook", "co_hook", {
    **W1("robotown", robots=[[0, 0], [C("the robots arrived"), 2], [C("They don't take vacations"), 4], [C("They never ask"), 6]],
         workers=[[0, 4], [C("They never ask"), 1]], flowAt=C("And the warehouse is making"), flowTo="tower"),
    "cam": cam((0, 0, 600, 1.2), (C("the robots arrived"), 450, 600, 1.25, 1.2), (C("And the warehouse is making"), 700, 520, 0.95, 1.4),
               (C("So Dana has a question"), 0, 580, 1.15, 1.2), (C("Here's a clue"), 500, 520, 0.9, 1.2), (C("So the real question"), 300, 540, 0.85, 1.6)), "drift": 3,
    "items": [DANA(-80, 0.0, face="happy", pose="clipboard", hold="clipboard", label="DANA · WAREHOUSE SHIFT LEAD", labelUntil=C("the robots arrived"),
                   poses=[[C("So Dana has a question"), "shrug"], [C("It may be"), "point"]], faces=[[0, "happy"], [C("the robots arrived"), "shock"], [C("So Dana has a question"), "worry"], [C("It may be"), "smug"]]),
              sign("NO SALARY", 250, 220, C("They don't take a salary"), color="#FFE0B2", size=34, until=C("And the warehouse is making")),
              sign("NO VACATIONS", 520, 160, C("They don't take vacations"), color="#C8E6C9", size=34, until=C("And the warehouse is making")),
              sign("NO RAISES", 780, 220, C("They never ask"), color="#BBDEFB", size=34, until=C("And the warehouse is making")),
              it("bubble", text="IF THE ROBOTS DO THE WORK... WHO GETS THE MONEY?", x=200, y=280, at=C("If the robots do the work"), until=C("Here's a clue"), tail=[0, 560], size=26),
              words("WORKERS' SHARE: LOWEST ON RECORD", 500, 150, C("In America"), size=50, until=C("So the real question")),
              words("WILL I KEEP MY JOB?", 300, 150, C("So the real question"), size=54, until=C("It may be")),
              words("DO I OWN ANY OF THE MACHINES?", 300, 150, C("It may be"), size=54, color="#FFFFFF"),
              tag((0, "MEET DANA · FICTIONAL"), (C("In America"), "FACT · BLS"), (C("So the real question"), "QUESTION"))]},
    sources=["bls_ls"], sfx=[{"kind": "hit", "cue": "Here's a clue", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("rrtitle", lines=["WHO GETS RICH", "WHEN ROBOTS", "DO THE WORK?"], sub="FOLLOW THE MONEY WHEN MACHINES DO THE JOB"), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [DANA(300, 2.6, scale=1.0, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])

# ====================================================================== ACT 1: follow the $100
stage("s03_link", "a1_link", {
    **W1("robotown", robots=5, workers=2, whLabel="FACTORY"),
    "cam": cam((0, 450, 560, 1.0), (C("and in Could AI Bring Europe"), 600, 540, 1.05, 1.2), (C("Now let's follow"), 300, 520, 1.0, WHIP)), "drift": 4,
    "items": [sign("EP 62 · COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?", 450, 150, 0.2, color="#BBDEFB", size=26, until=C("Now let's follow")),
              sign("EP 63 · COULD AI BRING EUROPE BACK TO POWER?", 600, 230, C("and in Could AI Bring Europe"), color="#C8E6C9", size=26, until=C("Now let's follow")),
              words("NOW: FOLLOW THE MONEY", 300, 160, C("Now let's follow"), size=60, color="#FFFFFF"),
              BOLT([[0, -200], [C("Now let's follow"), 900]], 0.2, carry="coin", scale=1.1, y=1000),
              DANA(0, C("Now let's follow"), face="happy", pose="point", y=1000),
              tag((0, "OUR SERIES"))]})
board("p04_split", "a1_draw", "One $100 bill = everything America earns", C("Picture a hundred-dollar bill"), [
    {"d": rect(640, 420, 560, 240), "color": "accent3", "width": 6, "kind": "box", "start": C("Picture a hundred-dollar bill"), "label": lbl("$100", 920, 560, 90, "accent3")},
    {"d": "M 640 660 L 640 420 L 800 420 L 800 660 Z", "color": "accent2", "width": 4, "fill": "accent2", "fillOpacity": 0.45, "kind": "bar", "start": C("A slice goes to the people")},
    {"d": "M 800 660 L 800 420 L 860 420 L 860 660 Z", "color": "accent", "width": 4, "fill": "accent", "fillOpacity": 0.7, "kind": "bar", "start": C("A slice goes to the owners")},
    {"d": arrow((720, 665), (700, 780), 0.0), "color": "accent2", "width": 6, "kind": "arrow", "start": C("A slice goes to the people"), "label": lbl("PAY", 700, 820, 34, "accent2")},
    {"d": arrow((830, 665), (900, 780), 0.0), "color": "accent", "width": 6, "kind": "arrow", "start": C("A slice goes to the owners"), "label": lbl("PROFIT", 920, 820, 34, "accent")},
    {"d": arrow((1030, 665), (1150, 780), 0.0), "color": "muted", "width": 6, "kind": "arrow", "start": C("The rest covers"), "label": lbl("EVERYTHING ELSE", 1170, 820, 26, "muted")},
    {"d": dot(1060, 900), "color": "muted", "width": 1, "start": C("Picture a hundred-dollar bill"), "label": lbl("U.S. GROSS DOMESTIC INCOME AS $100 · SLICES NOT TO SCALE HERE · BEA", 1060, 900, 15, "muted")},
], [{"kind": "point", "at": C("A slice goes to the people", 0.2), "dur": 1.4, "target": [720, 600]}, {"kind": "point", "at": C("A slice goes to the owners", 0.2), "dur": 1.4, "target": [830, 600]}],
    sources=["bea_gdi"])
SPLIT = dict(note="BEA (VIA FRED): SHARES OF U.S. GROSS DOMESTIC INCOME, 1970 vs 2025 · 'EVERYTHING ELSE' = DEPRECIATION, TAXES, INTEREST, RENT, SELF-EMPLOYED INCOME", hideOther=True)
stage("s05_then", "a1_then", {
    **W1("splitter", pay=58.4, profit=4.5, other=37.1, year=[[0, "1970s"]], hiAt=[[0, ""], [C("workers got"), "pay"]], hideProfit=True, **SPLIT),
    "cam": cam((0, 960, 520, 0.92), (C("workers got"), 440, 560, 1.15, 1.2)), "drift": 2,
    "items": [toon(1700, 0.2, who="shopper", v=1, skin=2, hair=4, hairStyle=2, color=NAVY, glasses=False, scarf=GOLD, face="happy", pose="wave", y=1000, scale=0.9, label="DANA'S DAD, 1970s", labelUntil=C("workers got")),
              tag((0, "FACT · BEA, 1970"))]},
    sources=["bea_gdi"])
stage("s06_now", "a1_now", {
    **W1("splitter", pay=[[0, 58.4], [C("Today"), 58.4], [C("they get", 0.6), 50.9]], profit=[[0, 4.5], [C("And the owners' slice"), 4.5], [C("roughly doubled"), 9.3]],
         other=39.8, year=[[0, "1970s"], [C("Today"), "2025"]], hiAt=[[0, "pay"], [C("And the owners' slice"), "profit"]], hideProfit=True, **SPLIT),
    "cam": cam((0, 440, 560, 1.15), (C("And the owners' slice"), 960, 560, 1.15, 1.2)), "drift": 2,
    "items": [words("PROFITS: ROUGHLY DOUBLED", 960, 180, C("roughly doubled"), size=54, color="#FFFFFF"),
              DANA(1700, 0.2, face="shock", pose="shrug", y=1000, scale=0.9),
              tag((0, "FACT · BEA, 2025"))]},
    sources=["bea_gdi"])
stage("s07_scale", "a1_scale", {
    **W1("robotown", robots=6, workers=1, flowAt=C("But this bill stands"), flowTo="tower"),
    "cam": cam((0, 450, 560, 1.0), (C("By our rough math"), 600, 500, 0.85, 1.4), (C("Not stolen"), 450, 540, 0.95, 1.0)), "drift": 3,
    "items": [it("bubble", text="A FEW BUCKS? WHO CARES?", x=0, y=300, at=0.2, until=C("But this bill stands"), tail=[0, 560], size=28),
              DANA(0, 0.0, face="smug", pose="shrug", y=1000),
              counter(600, 160, C("By our rough math"), 2, C("a year"), "OUR ROUGH MATH: THE GAP × 2025 U.S. INCOME (BEA)", prefix="> $", suffix=" TRILLION A YEAR"),
              words("NOT STOLEN. THE SPLIT MOVED.", 450, 300, C("Not stolen"), size=46, color="#FFFFFF"),
              tag((0, "FACT"), (C("By our rough math"), "OUR MATH"))]},
    sources=["bea_gdi"])
board("p08_index", "a1_index", "Workers' share of U.S. business output (BLS)", C("The Labor Department"), [
    {"d": "M 620 820 L 1500 820 M 620 820 L 620 420", "color": "ink", "width": 4, "start": C("The Labor Department")},
    {"d": "M 640 485 L 760 474 L 900 502 L 1080 505", "color": "accent2", "width": 7, "start": C("For decades after the war"), "label": lbl("BARELY BUDGED", 860, 450, 24, "accent2")},
    {"d": "M 1080 505 L 1260 683 L 1380 676 L 1470 761", "color": "risk", "width": 7, "start": C("Then it started to slide")},
    {"d": dot(1470, 761), "color": "risk", "width": 1, "start": C("Today it's the lowest"), "label": lbl("2026: LOWEST ON RECORD", 1300, 800, 24, "risk")},
    {"d": dot(1060, 880), "color": "muted", "width": 1, "start": C("The Labor Department"), "label": lbl("BLS NONFARM BUSINESS LABOR SHARE, 1947-2026 · SHAPE TRACED FROM SELECTED POINTS (SEE FACT CHECK)", 1060, 880, 14, "muted")},
], [{"kind": "point", "at": C("Then it started to slide", 0.2), "dur": 1.4, "target": [1260, 683]}, {"kind": "point", "at": C("Today it's the lowest", 0.2), "dur": 1.4, "target": [1470, 761]}],
    enter_left=False, sources=["bls_ls"])
stage("s09_why", "a1_why", {
    **W1("robotown", robots=[[0, 2], [C("When a machine does"), 2], [C("When a machine does", 1.0), 5]], workers=[[0, 3], [C("When a machine does"), 3], [C("When a machine does", 1.0), 1]],
         flowAt=C("the money that paid"), flowTo="tower"),
    "cam": cam((0, 500, 540, 0.9), (C("A robot is capital"), 450, 600, 1.2, 1.2), (C("the money that paid"), 700, 500, 0.92, 1.4)), "drift": 3,
    "items": [words("WHY?", 500, 140, 0.1, until=C("Global trade"), size=70),
              sign("SUSPECT: GLOBAL TRADE", 150, 150, C("Global trade"), color="#FFE0B2", size=28, until=C("But here's what a robot adds")),
              sign("SUSPECT: SUPERSTAR COMPANIES", 520, 220, C("a few superstar"), color="#E1D5FF", size=28, until=C("But here's what a robot adds")),
              sign("SUSPECT: AUTOMATION", 900, 150, C("and automation"), color="#BBDEFB", size=28, until=C("But here's what a robot adds")),
              words("A ROBOT IS CAPITAL", 450, 150, C("A robot is capital"), size=60, until=C("the money that paid")),
              sign("PAY → WHOEVER OWNS THE MACHINE", 700, 150, C("the money that paid"), color="#FFF59D", size=34),
              BOLT(300, C("A robot is capital"), carry="box", scale=1.1, y=1000),
              tag((0, "DEBATED CAUSES"), (C("But here's what a robot adds"), "MECHANISM"))]},
    sources=["autor_superstar", "ar_framework"])

stage("s09b_dana", "a1_dana", {
    **W1("robotown", robots=[[0, 3], [C("The robots took"), 6]], workers=[[0, 3], [C("It just stopped hiring"), 1]], flowAt=C("It went somewhere"), flowTo="tower"),
    "cam": cam((0, 0, 600, 1.2), (C("The robots took"), 450, 560, 1.0, 1.2), (C("It went somewhere"), 800, 500, 0.9, 1.4)), "drift": 3,
    "items": [DANA(-60, 0.0, face="worry", pose="clipboard", hold="clipboard", y=1000, poses=[[C("It went somewhere"), "point"]]),
              it("bubble", text="NOBODY GOT FIRED. WE JUST STOPPED HIRING.", x=100, y=280, at=0.4, until=C("The robots took"), tail=[-60, 560], size=26),
              sign("NIGHT SHIFT: NOW ROBOTS", 450, 160, C("The robots took"), color="#BBDEFB", size=32, until=C("It went somewhere")),
              words("THE MONEY WENT SOMEWHERE", 800, 150, C("It went somewhere"), size=52, color="#FFFFFF"),
              tag((0, "DANA'S STORY · FICTIONAL"))]})
# ====================================================================== ACT 2: who owns the machines?
bumper("s10_b2", "a2_card", "2", "WHO OWNS THE MACHINES?", "Hint: not the machines.", BLUE)
GROUPS = lambda at=(0, 0, 0), disp=("< $1", "", "≈ $88"): [
    {"label": "BOTTOM HALF", "n": 40, "v": 0.6, "at": at[0], "color": GREY, "display": disp[0]},
    {"label": "NEXT 40%", "n": 30, "v": 11.4, "at": at[1], "color": TEAL, "display": disp[1]},
    {"label": "RICHEST 10%", "n": 10, "v": 88.1, "at": at[2], "color": GOLD, "display": disp[2]}]
FOOT_EQ = "FED DISTRIBUTIONAL FINANCIAL ACCOUNTS, Q2 2026 · HOUSEHOLDS BY WEALTH · STOCKS & STOCK FUNDS (EXCL. PENSIONS) · EXACT: 0.6 / 11.4 / 88.1 OF EVERY $100"
stage("s11_own", "a2_own", {
    **W1("sharestreet", groups=GROUPS(at=(999, 999, 999)), foot=FOOT_EQ),
    "cam": cam((0, 760, 520, 0.85), (C("So let's line up"), 300, 600, 1.1, 1.4), (C("and share out"), 760, 480, 0.8, 1.6)), "drift": 3,
    "items": [it("bubble", text="SO... WHO OWNS THE ROBOTS?", x=900, y=300, at=0.2, until=C("So let's line up"), tail=[1100, 700], size=30),
              DANA(1100, 0.0, face="worry", pose="shrug", y=1000, until=C("So let's line up")),
              sign("EVERY HOUSEHOLD · LEAST WEALTHY → MOST", 300, 160, C("So let's line up"), color="#FFFFFF", size=30, until=C("and share out")),
              words("$100 OF STOCK TO SHARE OUT", 760, 130, C("and share out"), size=54, color="#FFFFFF"),
              tag((0, "THE SETUP"))]},
    sources=["fed_dfa"])
stage("s12_split", "a2_split", {
    **W1("sharestreet", groups=GROUPS(at=(C("The whole bottom half"), 999, 999)), foot=FOOT_EQ),
    "cam": cam((0, 300, 640, 1.15), (C("all together"), 200, 620, 1.25, 1.2)), "drift": 2,
    "items": [it("bubble", text="LESS THAN A DOLLAR. FOR ALL OF US?!", x=250, y=330, at=C("gets less"), tail=[150, 700], size=28),
              MILO(-150, 0.2, face="shock", pose="shrug", y=1000), tag((0, "FACT · FED"))]},
    sources=["fed_dfa"])
stage("s13_top", "a2_top", {
    **W1("sharestreet", groups=GROUPS(at=(0, 0.2, C("And the richest tenth"))), foot=FOOT_EQ),
    "cam": cam((0, 700, 560, 0.9), (C("And the richest tenth"), 1250, 460, 1.0, 1.2), (C("Nearly the whole pile"), 800, 500, 0.8, 1.2)), "drift": 2,
    "items": [words("NEARLY THE WHOLE PILE", 800, 120, C("Nearly the whole pile"), size=58, color="#FFFFFF"), tag((0, "FACT · FED"))]},
    sources=["fed_dfa"])
stage("s14_pension", "a2_pension", {
    **W1("doorways", doors=[{"label": "MILO'S 401(k)", "sub": "SPREAD WIDER THAN STOCKS", "at": C("Accounts like his"), "color": BLUE}], bannerText="FED DFA, Q2 2026 · BOTTOM HALF HOLDS ≈5% OF 401(k)-TYPE ACCOUNTS"),
    "cam": cam((0, 500, 560, 1.1), (C("But even there"), 700, 520, 0.95, 1.2)), "drift": 2,
    "items": [MILO(800, 0.0, face="happy", pose="wave", y=1000, label="MILO · RETIRED BUS DRIVER", labelUntil=C("Accounts like his")),
              DANA(1100, 0.3, face="happy", pose="stand", y=1000),
              sign("POORER HOUSEHOLDS: ONLY A SLIVER", 900, 300, C("But even there"), color="#FFCDD2", size=34),
              tag((0, "FACT · FED"))]},
    sources=["fed_dfa"])
stage("s15_flip", "a2_flip", {
    **W1("robotown", robots=5, workers=2, flowAt=C("If robots move money"), flowTo="tower", towerLabel="SHAREHOLDERS"),
    "cam": cam((0, 500, 540, 0.9), (C("For generations"), 0, 600, 1.15, 1.2), (C("When machines do more"), 900, 500, 0.95, 1.4)), "drift": 3,
    "items": [words("PAYCHECKS → PROFITS → SHARES", 600, 150, C("If robots move money"), size=50, until=C("For generations")),
              sign("THE OLD WAY UP: A BETTER JOB", 0, 170, C("For generations"), color="#BBDEFB", size=32, until=C("When machines do more")),
              words("OWNING A PIECE MAY MATTER AS MUCH", 900, 150, C("When machines do more"), size=46, color="#FFFFFF"),
              DANA(-100, 0.2, face="worry", pose="clipboard", hold="clipboard", faces=[[0, "worry"], [C("When machines do more"), "smug"]], y=1000),
              tag((0, "MECHANISM"), (C("When machines do more"), "A POSSIBILITY, NOT A FORECAST"))]})

# ====================================================================== ACT 3: the new factories
bumper("s16_b3", "a3_card", "3", "THE NEW FACTORIES", "The biggest machines ever built don't have arms.", PURPLE)
CAMPS = lambda ats: [{"name": "AMAZON", "v": 210.7, "at": ats[0]}, {"name": "ALPHABET", "v": 159.8, "at": ats[1]},
                     {"name": "MICROSOFT", "v": 135.9, "at": ats[2]}, {"name": "META", "v": 108.0, "at": ats[3]}]
FOOT_CAPEX = "CAPITAL SPENDING, 12 MONTHS TO SEP 30, 2026 · COMPANY FILINGS · ≈ $614B BY OUR SUM · GENERIC BUILDINGS, NO LOGOS"
stage("s17_capex", "a3_capex", {
    **W1("dcfield", camps=CAMPS([C("Amazon"), C("Alphabet"), C("Microsoft"), C("and Meta")]), foot=FOOT_CAPEX),
    "cam": cam((0, 900, 520, 1.1), (C("Amazon"), 500, 480, 0.85, 1.4), (C("spent"), 760, 470, 0.72, 1.4)), "drift": 2,
    "items": [words("DATA CENTERS FOR AI", 900, 150, C("Data centers"), size=64, until=C("spent")),
              counter(760, 100, C("spent"), 600, C("on buildings"), "4 COMPANIES · ONE YEAR · OUR SUM", prefix="> $", suffix=" BILLION"),
              tag((0, "FACT"), (C("spent"), "OUR SUM"))]},
    sources=["byb_amzn", "byb_goog", "byb_msft", "byb_meta"])
stage("s18_nvidia", "a3_nvidia", {
    **W1("dcfield", camps=CAMPS([0, 0, 0, 0]), chipAt=0.3, chipX=1900, margin=[[0, 0], [C("Nvidia kept"), 0], [C("as profit"), 0.564]],
         marginText="MOST OF EVERY $1 OF SALES = PROFIT", foot="NVIDIA, QUARTER TO OCT 25, 2026: NET INCOME $65.3B ON REVENUE $115.8B ≈ 56% (OUR CALC.) · GENERIC CHIP, NO LOGO"),
    "cam": cam((0, 900, 500, 0.75), (C("In its latest quarter"), 1850, 440, 1.0, 1.4)), "drift": 2,
    "items": [it("bubble", text="THE CHIP SELLER", x=1600, y=180, at=C("lands at the company"), until=C("In its latest quarter"), tail=[1850, 450], size=30),
              BOLT([[0, 600], [C("lands at the company"), 1500]], 0.2, carry="coin", y=1000),
              tag((0, "FACT · COMPANY FILING"))]},
    sources=["byb_nvda"])
board("p19_loop", "a3_loop", "The AI money loop", C("A business pays"), [
    {"d": rect(600, 420, 240, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("A business pays"), "label": lbl("BUSINESS", 720, 480, 28, "accent2")},
    {"d": arrow((845, 470), (1015, 470), -0.15), "color": "accent", "width": 6, "kind": "arrow", "start": C("That money goes"), "label": lbl("$ FOR AI", 930, 430, 22, "accent")},
    {"d": rect(1020, 420, 240, 100), "color": "accent3", "width": 6, "kind": "box", "start": C("That money goes"), "label": lbl("CLOUD", 1140, 480, 30, "accent3")},
    {"d": arrow((1140, 525), (1140, 630), 0.0), "color": "accent", "width": 6, "kind": "arrow", "start": C("buys chips")},
    {"d": rect(1020, 635, 240, 100), "color": "risk", "width": 6, "kind": "box", "start": C("buys chips"), "label": lbl("CHIPS + DATA CENTERS", 1140, 695, 20, "risk")},
    {"d": arrow((1015, 690), (845, 690), 0.0), "color": "accent", "width": 6, "kind": "arrow", "start": C("Profits flow")},
    {"d": rect(600, 635, 240, 100), "color": "accent", "width": 6, "kind": "box", "start": C("Profits flow"), "label": lbl("SHAREHOLDERS", 720, 695, 24, "accent")},
    {"d": arrow((720, 630), (720, 525), 0.0), "color": "muted", "width": 4, "kind": "arrow", "start": C("of both")},
    {"d": dot(1060, 870), "color": "muted", "width": 1, "start": C("A business pays"), "label": lbl("A MECHANISM, NOT A MEASURED FLOW", 1060, 870, 16, "muted")},
], [{"kind": "point", "at": C("Profits flow", 0.2), "dur": 1.4, "target": [720, 690]}], enter_left=False)
stage("s20_missing", "a3_missing", {
    **W1("moneyloop", loopAt=0.0, outAt=C("The worker whose task"), doorAt=C("Unless that worker")),
    "cam": cam((0, 960, 500, 0.85), (C("The worker whose task"), 1350, 560, 1.0, 1.2), (C("Unless that worker"), 1150, 540, 0.9, 1.2)), "drift": 2,
    "items": [words("WHO'S MISSING?", 960, 120, 0.2, size=58, until=C("The worker whose task")),
              tag((0, "MECHANISM"))]})
stage("s20b_dana", "a3_dana", {
    **W1("moneyloop", loopAt=0.0, outAt=0.0, doorAt=C("Yet")),
    "cam": cam((0, 1350, 560, 1.0), (C("Every step of that chain"), 960, 500, 0.85, 1.4), (C("Yet"), 1150, 540, 0.95, WHIP)), "drift": 2,
    "items": [DANA(1750, 0.0, face="worry", pose="shrug", y=1000, faces=[[0, "worry"], [C("Yet"), "smug"]]),
              words("EVERY STEP HAS OWNERS", 960, 120, C("Every step of that chain"), size=54, until=C("Yet")),
              words("...YET", 1150, 120, C("Yet"), size=70, color="#FFFFFF"),
              tag((0, "DANA'S STORY · MECHANISM"))]})
stage("s21_risk", "a3_risk", {
    **W1("dcfield", camps=CAMPS([0, 0, 0, 0]), foot="AMAZON: FREE CASH FLOW, 12 MONTHS TO SEP 30, 2026 = 'AN OUTFLOW OF $42.4 BILLION' (COMPANY RELEASE)"),
    "cam": cam((0, 760, 500, 0.75), (C("Over the past year"), 0, 500, 1.0, 1.2), (C("Owners get the upside"), 760, 500, 0.8, 1.4)), "drift": 2,
    "items": [words("A BET, NOT A GUARANTEE", 760, 120, 0.2, size=56, until=C("Over the past year")),
              sign("AMAZON: MORE CASH OUT THAN IN (PAST YEAR)", 0, 140, C("Over the past year"), color="#FFCDD2", size=32, until=C("Owners get the upside")),
              words("UPSIDE + RISK = OWNERSHIP", 760, 130, C("Owners get the upside"), size=52, color="#FFFFFF"),
              BOLT(200, 0.2, carry="none", moods=[[0, "happy"], [C("Over the past year"), "sad"]], scale=1.1, y=1000),
              tag((0, "FACT"))]},
    sources=["byb_amzn"])

# ====================================================================== ACT 4: what the evidence says
bumper("s22_b4", "a4_card", "4", "WHAT THE EVIDENCE SAYS", "Measured findings on the left. Forecasts on the right.", TEAL)
CARD_BRYN = {"text": "AI ASSISTANT: MORE PROBLEMS SOLVED PER HOUR", "sub": "NEWEST AGENTS GAINED MOST · BRYNJOLFSSON, LI & RAYMOND (NBER)", "kind": "finding"}
CARD_DK = {"text": "DENMARK: NO MEASURABLE EFFECT ON PAY OR HOURS", "sub": "HUMLUM & VESTERGAARD (NBER) · PAYROLL RECORDS", "kind": "finding"}
CARD_YOUNG = {"text": "YOUNGEST WORKERS, AI-EXPOSED JOBS: ALMOST 1/5 FEWER", "sub": "DESCRIPTIVE, NOT CAUSAL · BRYNJOLFSSON, CHANDAR & CHEN (STANFORD)", "kind": "descriptive"}
CARD_ACEM = {"text": "AI: ONLY A SMALL PRODUCTIVITY LIFT IN 10 YEARS", "sub": "AND A WIDER CAPITAL-LABOR GAP · ACEMOGLU (NBER) · A MODEL", "kind": "forecast"}
stage("s23_find", "a4_find", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": C("they solved")}]),
    "cam": cam((0, 960, 480, 0.85), (C("First, a finding"), 500, 420, 1.1, 1.2)), "drift": 2,
    "items": [words("MEASURED vs PREDICTED", 960, 110, 0.2, size=52, until=C("First, a finding")),
              DANA(-60, 0.3, face="happy", pose="clipboard", hold="clipboard", y=1000, scale=1.0),
              tag((0, "SORTING THE EVIDENCE"), (C("First, a finding"), "FINDING"))]},
    sources=["bryn"])
stage("s24_denmark", "a4_denmark", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": C("they've found")}]),
    "cam": cam((0, 500, 470, 1.0), (C("they've found"), 500, 520, 1.1, 1.2)), "drift": 2,
    "items": [BOLT(1500, 0.2, carry="box", scale=0.9, y=1000), tag((0, "FINDING"))]},
    sources=["humlum"])
stage("s25_young", "a4_young", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": 0}, {**CARD_YOUNG, "at": C("Among the youngest")}]),
    "cam": cam((0, 500, 560, 1.05), (C("Experienced workers"), 500, 600, 1.1, 1.2), (C("The researchers call"), 800, 520, 0.9, 1.2)), "drift": 2,
    "items": [sign("EARLY WARNING, NOT PROOF", 1400, 300, C("The researchers call"), color="#B2EBF2", size=34),
              MILO(1700, 0.2, face="worry", pose="stand", y=1000, scale=1.0),
              tag((0, "DESCRIPTIVE"))]},
    sources=["canaries"])
stage("s26_robots", "a4_robots", {
    **W1("robotown", robots=6, workers=[[0, 4], [C("saw fewer jobs"), 2]], whLabel="FACTORY TOWN", homesLabel="LOCAL JOBS"),
    "cam": cam((0, 450, 560, 1.0), (C("Economists found"), 300, 560, 0.95, 1.2), (C("saw fewer jobs"), 0, 600, 1.1, 1.2)), "drift": 3,
    "items": [words("FACTORY ROBOTS: A LONGER RECORD", 450, 140, 0.2, size=48, until=C("Economists found")),
              sign("MORE ROBOTS → FEWER JOBS, SLIGHTLY LOWER PAY", 300, 150, C("saw fewer jobs"), color="#FFCDD2", size=30),
              sign("ACEMOGLU & RESTREPO · U.S. 1990-2007", 300, 230, C("saw fewer jobs"), color="#FFFFFF", size=22),
              tag((0, "FINDING"))]},
    sources=["ar_robots"])
stage("s27_forecast", "a4_forecast", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": 0}, {**CARD_YOUNG, "at": 0}, {**CARD_ACEM, "at": C("predicts AI")}]),
    "cam": cam((0, 960, 480, 0.85), (C("predicts AI"), 1420, 420, 1.1, 1.2), (C("Forecasts differ"), 960, 480, 0.85, 1.2)), "drift": 2,
    "items": [sign("A MODEL, NOT A MEASUREMENT", 1420, 560, C("That's a model"), color="#FFE0B2", size=32),
              words("FORECASTS DIFFER WIDELY", 960, 110, C("Forecasts differ"), size=50),
              tag((0, "FORECAST"))]},
    sources=["acemoglu"])

# ====================================================================== ACT 5: we've been here before
bumper("s28_b5", "a5_card", "5", "WE'VE BEEN HERE BEFORE", "Britain, the age of steam.", ORANGE)
stage("s29_britain", "a5_britain", {
    **W1("millyard", prog=[[0, 0.0], [C("Machines multiplied"), 0.05], [C("Workers' pay"), 0.5]], chartNote="ILLUSTRATIVE SHAPE OF ALLEN (2009): OUTPUT PER WORKER vs REAL WAGE, BRITAIN · NOT PLOTTED DATA"),
    "cam": cam((0, 960, 640, 1.1), (C("Machines multiplied"), 960, 520, 0.92, 1.4)), "drift": 3,
    "items": [words("BRITAIN, EARLY 1800s", 960, 130, 0.2, size=56, until=C("Machines multiplied")),
              sign("FACTORY OWNERS: RICH", 600, 620, C("Factory owners"), color="#FFF59D", size=30),
              sign("WORKERS' PAY: BARELY MOVED", 1350, 620, C("Workers' pay"), color="#FFCDD2", size=30),
              tag((0, "HISTORY"), (C("Machines multiplied"), "ILLUSTRATIVE SHAPE"))]},
    sources=["allen"])
board("p30_engels", "a5_draw", "Engels' pause (after Robert Allen, 2009)", C("Let me draw his story"), [
    {"d": "M 620 820 L 1500 820 M 620 820 L 620 420", "color": "ink", "width": 4, "start": C("Let me draw his story")},
    {"d": "M 640 790 Q 900 680 1100 560 T 1480 430", "color": "accent2", "width": 7, "start": C("Output per worker"), "label": lbl("OUTPUT PER WORKER", 1300, 440, 24, "accent2")},
    {"d": "M 640 795 L 1100 780", "color": "accent", "width": 7, "start": C("Real wages stayed flat"), "label": lbl("REAL WAGE", 870, 760, 24, "accent")},
    {"d": "M 1100 780 Q 1300 650 1480 520", "color": "accent", "width": 7, "start": C("Real wages stayed flat", 1.2)},
    {"d": rect(760, 560, 330, 210), "color": "risk", "width": 4, "kind": "box", "start": C("The profit rate doubled"), "label": lbl("PROFIT RATE ×2", 925, 610, 24, "risk")},
    {"d": dot(925, 650), "color": "risk", "width": 1, "start": C("The profit rate doubled", 0.6), "label": lbl("PROFIT SHARE ↑", 925, 655, 22, "risk")},
    {"d": dot(925, 520), "color": "ink", "width": 1, "start": C("Historians call it"), "label": lbl("“ENGELS' PAUSE”", 925, 520, 32, "ink")},
    {"d": dot(700, 860), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("1800", 700, 860, 20, "muted")},
    {"d": dot(1100, 860), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("≈1850", 1100, 860, 20, "muted")},
    {"d": dot(1060, 900), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("ILLUSTRATIVE SHAPE OF ALLEN'S FINDINGS · ENGELS, 'THE CONDITION OF THE WORKING CLASS IN ENGLAND' (1845)", 1060, 900, 15, "muted")},
], [{"kind": "point", "at": C("Real wages stayed flat", 0.2), "dur": 1.4, "target": [870, 785]}, {"kind": "point", "at": C("The profit rate doubled", 0.2), "dur": 1.4, "target": [925, 610]}],
    sources=["allen"])
stage("s31_end", "a5_end", {
    **W1("millyard", prog=[[0, 0.55], [C("wages finally began"), 0.6], [C("The pause ended"), 1.0]], pauseAt=0.0, catchAt=C("wages finally began")),
    "cam": cam((0, 960, 420, 1.0), (C("The pause ended"), 960, 520, 0.9, 1.2), (C("For the workers"), 700, 640, 1.15, 1.4)), "drift": 2,
    "items": [words("THE PAUSE ENDED...", 960, 640, C("The pause ended"), size=52, until=C("But it lasted")),
              words("...AFTER DECADES", 960, 640, C("But it lasted"), size=56, color="#FFFFFF"),
              tag((0, "HISTORY · ILLUSTRATIVE SHAPE"))]},
    sources=["allen"])

stage("s31b_today", "a5_today", {
    **W1("millyard", prog=1.0, pauseAt=0.0, catchAt=0.0),
    "cam": cam((0, 960, 420, 1.0), (C("What history does show"), 960, 560, 0.85, 1.4)), "drift": 2,
    "items": [words("A NEW ENGELS' PAUSE?", 960, 640, 0.2, size=56, until=C("Workers' share")),
              sign("TODAY: WORKERS' SHARE AT A RECORD LOW (BLS)", 960, 640, C("Workers' share"), color="#FFCDD2", size=30, until=C("What history does show")),
              sign("NEITHER THE PAUSE NOR THE CATCH-UP IS AUTOMATIC", 960, 640, C("What history does show"), color="#FFF59D", size=30),
              tag((0, "OPEN QUESTION"), (C("Workers' share"), "FACT · BLS"))]},
    sources=["bls_ls", "allen"])
# ====================================================================== ACT 6: the case against the doom story
bumper("s32_b6", "a6_card", "6", "THE CASE AGAINST THE DOOM STORY", "Four reasons for hope, fairly stated.", GREEN)
stage("s33_newjobs", "a6_newjobs", {
    **W1("newjobs", old=[{"text": "SWITCHBOARD OPERATOR", "at": C("Machines take over"), "slot": 1}, {"text": "TYPIST POOL", "at": C("Machines take over", 0.3), "slot": 3},
                         {"text": "ELEVATOR OPERATOR", "at": C("Machines take over", 0.6), "slot": 5}],
         fresh=[{"text": "SOFTWARE DEVELOPER", "at": C("A team led by"), "slot": 1, "up": 0}, {"text": "WIND TURBINE TECH", "at": C("found that most"), "slot": 3},
                {"text": "DATA ANALYST", "at": C("job specialties"), "slot": 5}, {"text": "AI TRAINER", "at": C("New kinds of work"), "slot": 2}]),
    "cam": cam((0, 900, 520, 0.8), (C("found that most"), 900, 500, 0.85, 1.2), (C("Machines take over"), 900, 520, 0.8, 1.2)), "drift": 3,
    "items": [words("1. NEW JOBS", 900, 120, 0.2, size=60, until=C("A team led by")),
              sign("MOST JOBS TODAY: SPECIALTIES THAT DIDN'T EXIST IN 1940 (AUTOR ET AL.)", 900, 120, C("found that most"), color="#C8E6C9", size=28),
              sign("JOB TITLES: ILLUSTRATIVE EXAMPLES", 900, 190, C("Machines take over"), color="#FFFFFF", size=22),
              tag((0, "FINDING"))]},
    sources=["autor_newwork"])
stage("s34_wages", "a6_wages", {
    **W1("robotown", robots=5, workers=3, whLabel="WAREHOUSE · NEW TASKS"),
    "cam": cam((0, 450, 560, 1.05), (C("Like Dana"), 300, 540, 0.95, 1.4)), "drift": 3,
    "items": [words("2. PRODUCTIVITY CAN LIFT PAY", 450, 140, 0.2, size=50, until=C("When things get cheaper")),
              sign("CHEAPER → PEOPLE BUY MORE", 300, 150, C("When things get cheaper"), color="#BBDEFB", size=32, until=C("Like Dana")),
              sign("AI-SAVVY WORKERS → MORE VALUABLE", 650, 230, C("And workers who use"), color="#C8E6C9", size=30, until=C("Like Dana")),
              words("LIKE DANA: NOW RUNS THE ROBOT FLEET", 300, 150, C("Like Dana"), size=46, color="#FFFFFF"),
              DANA(-100, 0.3, face="happy", pose="clipboard", hold="clipboard", y=1000, label="DANA · NOW RUNS THE ROBOT FLEET", labelUntil=C("Like Dana")),
              tag((0, "MECHANISM"))]},
    sources=["ar_framework", "bryn"])
stage("s35_degree", "a6_degree", {
    "zones": [Z("triad", title="MEDIAN WEEKLY PAY, FULL-TIME, AGE 25+, Q3 2026 (BLS)", scale=0.32, gap=520,
                bars=[{"label": "BACHELOR'S OR MORE", "v": 1752, "color": BLUE, "display": "$1,752", "at": C("typically earns")},
                      {"label": "HIGH SCHOOL ONLY", "v": 993, "color": GREY, "display": "$993", "at": C("than a high school")}],
                foot="BLS CURRENT POPULATION SURVEY VIA FRED (LEU0252918500Q, LEU0252917300Q) · NOT SEASONALLY ADJUSTED")], "worldW": 2400,
    "cam": cam((0, 960, 520, 0.95), (C("than a high school"), 960, 500, 1.0, 1.2)), "drift": 2,
    "items": [words("3. SKILLS STILL PAY", 960, 200, 0.2, size=56, until=C("A full-time worker")),
              tag((0, "FACT"))]},
    sources=["bls_edu"])
stage("s36_policy", "a6_policy", {
    **W1("robotown", robots=4, workers=3, towerLabel="CITY HALL?", homesLabel="VOTERS"),
    "cam": cam((0, 450, 540, 0.9), (C("Others prefer training"), 600, 520, 0.95, 1.2), (C("This film takes no side"), 450, 540, 0.85, 1.2)), "drift": 3,
    "items": [words("4. POLICY CAN CHANGE THE SPLIT", 450, 130, 0.2, size=48, until=C("Some want")),
              sign("SPREAD OWNERSHIP (EMPLOYEE STOCK, KIDS' ACCOUNTS, PUBLIC FUNDS)", 450, 140, C("Some want"), color="#C8E6C9", size=24),
              sign("TRAINING", 150, 220, C("Others prefer training"), color="#BBDEFB", size=30),
              sign("TAX WORK vs CAPITAL DIFFERENTLY", 600, 220, C("or changing how"), color="#FFE0B2", size=28),
              sign("LET MARKETS ADJUST", 1000, 220, C("Others say markets"), color="#E1D5FF", size=30),
              words("EACH HAS TRADE-OFFS · NO SIDE TAKEN", 450, 320, C("Each has trade-offs"), size=40, color="#FFFFFF"),
              tag((0, "OPTIONS, NOT ENDORSEMENTS"))]})

# ====================================================================== ACT 7: what can you actually own?
bumper("s37_b7", "a7_card", "7", "WHAT CAN YOU ACTUALLY OWN?", "Education, not investment advice.", NAVY)
DOORS = lambda ats: [{"label": "401(k) / IRA", "sub": "RETIREMENT ACCOUNT", "at": ats[0], "color": BLUE},
                     {"label": "INDEX FUND", "sub": "SLICES OF MANY COMPANIES", "at": ats[1], "color": GREEN},
                     {"label": "EMPLOYEE STOCK", "sub": "ESOPs AND STOCK PLANS", "at": ats[2], "color": ORANGE}]
stage("s38_now", "a7_now", {
    **W1("doorways", doors=DOORS([999, 999, 999])),
    "cam": cam((0, 960, 480, 0.85), (C("Most American families"), 960, 500, 0.9, 1.2)), "drift": 2,
    "items": [words("MOST FAMILIES OWN SOME STOCK", 960, 300, C("Most American families"), size=50, until=C("But among lower-income")),
              sign("LOWER-INCOME FAMILIES: FEWER THAN 1 IN 3", 960, 300, C("But among lower-income"), color="#FFCDD2", size=36),
              MILO(200, 0.2, face="happy", pose="wave", y=1000, scale=1.0),
              tag((0, "EDUCATION, NOT ADVICE"), (C("Most American families"), "FACT"))]},
    sources=["scf25"])
board("p39_doors", "a7_doors", "Three common doors to owning (education, not advice)", C("Let me draw the doors"), [
    {"d": rect(600, 440, 220, 320), "color": "accent2", "width": 6, "kind": "box", "start": C("The most common"), "label": lbl("401(k) / IRA", 710, 420, 26, "accent2")},
    {"d": dot(710, 600), "color": "ink", "width": 1, "start": C("The most common"), "label": lbl("MOST COMMON", 710, 600, 22, "ink")},
    {"d": rect(900, 440, 220, 320), "color": "accent3", "width": 6, "kind": "box", "start": C("index funds"), "label": lbl("INDEX FUND", 1010, 420, 26, "accent3")},
    {"d": dot(1010, 600), "color": "ink", "width": 1, "start": C("small slices"), "label": lbl("MANY COMPANIES", 1010, 600, 20, "ink")},
    {"d": rect(1200, 440, 220, 320), "color": "accent", "width": 6, "kind": "box", "start": C("Some employers"), "label": lbl("EMPLOYEE STOCK", 1310, 420, 24, "accent")},
    {"d": dot(1310, 600), "color": "ink", "width": 1, "start": C("Employee stock ownership plans"), "label": lbl("ESOPs: MILLIONS", 1310, 600, 22, "ink")},
    {"d": dot(1010, 830), "color": "muted", "width": 1, "start": C("Let me draw the doors"), "label": lbl("FED SCF 2025 · NCEO (2023 PLAN DATA) · NOTHING HERE IS A RECOMMENDATION TO BUY ANYTHING", 1010, 830, 16, "muted")},
], [{"kind": "point", "at": C("index funds", 0.2), "dur": 1.4, "target": [1010, 600]}, {"kind": "point", "at": C("Employee stock ownership plans", 0.2), "dur": 1.4, "target": [1310, 600]}],
    sources=["scf25", "nceo"])
stage("s40_risk", "a7_risk", {
    **W1("doorways", doors=DOORS([0, 0, 0]), riskAt=C("Stock prices can fall"),
         risks=[[0, ""], [C("Stock prices can fall"), "PRICES CAN FALL HARD"], [C("Fees eat returns"), "FEES EAT RETURNS"], [C("And betting your savings"), "ONE COMPANY = RISK ON RISK"]]),
    "cam": cam((0, 960, 520, 0.85), (C("Stock prices can fall"), 960, 380, 1.0, 1.2), (C("Owning a slice"), 960, 500, 0.85, 1.2)), "drift": 2,
    "items": [words("OWNING ISN'T FREE MONEY", 960, 160, 0.2, size=54, until=C("Stock prices can fall")),
              words("YOU SHARE THE BAD YEARS TOO", 960, 820, C("Owning a slice"), size=46, color="#FFFFFF"),
              tag((0, "EDUCATION, NOT ADVICE"))]})

stage("s40b_dana", "a7_dana", {
    **W1("doorways", doors=DOORS([C("Her employer offers"), 999, 999])),
    "cam": cam((0, 700, 560, 1.05), (C("But it's the moment"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [DANA(700, 0.0, face="happy", pose="clipboard", hold="clipboard", y=1000, faces=[[0, "worry"], [C("But it's the moment"), "happy"]]),
              sign("HER DECISION, NOT ADVICE", 960, 300, C("That's her decision"), color="#FFFFFF", size=32, until=C("But it's the moment")),
              words("BOTH SIDES OF THE LOOP", 960, 300, C("But it's the moment"), size=54, color="#FFFFFF"),
              tag((0, "DANA'S STORY · FICTIONAL"), (C("That's her decision"), "EDUCATION, NOT ADVICE"))]})
# ====================================================================== ACT 8: who gets rich?
bumper("s41_b8", "a8_card", "8", "WHO GETS RICH?", "The answer, and the fine print.", GOLD)
stage("s42_verdict", "a8_verdict", {
    **W1("sharestreet", groups=GROUPS(at=(0.2, 0.4, 0.6)), foot=FOOT_EQ),
    "cam": cam((0, 760, 520, 0.8), (C("mostly the people"), 1600, 420, 1.0, 1.4), (C("And in America"), 1100, 480, 0.85, 1.4)), "drift": 2,
    "items": [words("WHO GETS RICH?", 760, 130, 0.2, size=60, until=C("mostly the people")),
              words("THE OWNERS", 1600, 110, C("mostly the people"), size=60, color="#FFFFFF", until=C("And in America")),
              sign("RICHEST 10%: NEARLY THE WHOLE PILE", 1100, 130, C("And in America"), color="#FFF59D", size=32),
              tag((0, "VERDICT"), (C("And in America"), "FACT"))]},
    sources=["fed_dfa"])
stage("s43_but", "a8_but", {
    **W1("robotown", robots=5, workers=3, flowAt=0.2, flowTo="both"),
    "cam": cam((0, 450, 540, 0.9), (C("History says"), 200, 560, 1.05, 1.2), (C("More than half"), 450, 540, 0.85, 1.4)), "drift": 3,
    "items": [words("IT DOESN'T HAVE TO STAY NARROW", 450, 140, 0.2, size=48, until=C("History says")),
              sign("PAY CAN CATCH UP (AFTER A DELAY)", 150, 150, C("History says"), color="#C8E6C9", size=30, until=C("More than half")),
              sign("NEW JOBS APPEAR", 650, 230, C("New jobs"), color="#BBDEFB", size=30, until=C("More than half")),
              sign("MORE THAN HALF OF FAMILIES OWN SOME STOCK (FED SCF 2025)", 450, 150, C("More than half"), color="#FFF59D", size=30),
              DANA(-150, 0.3, face="happy", pose="cheer", y=1000), MILO(80, 0.4, face="happy", pose="wave", y=1000),
              tag((0, "VERDICT"), (C("More than half"), "FACT"))]},
    sources=["allen", "autor_newwork", "scf25"])
stage("s44_close", "a8_close", {
    **W1("robotown", robots=6, workers=2, flowAt=0.5, flowTo="both"),
    "cam": cam((0, 300, 560, 1.15), (C("Dana's question now"), 500, 520, 0.95, 1.6), (C("What do you own"), 450, 520, 0.85, WHIP)), "drift": 2,
    "items": [words("WHAT DO YOU DO FOR A LIVING?", 300, 150, 0.3, size=50, until=C("Dana's question now")),
              words("...AND A SECOND PART", 500, 150, C("Dana's question now"), size=52, until=C("What do you own")),
              words("WHAT DO YOU OWN?", 450, 160, C("What do you own"), size=72, color="#FFFFFF"),
              DANA(-100, 0.3, face="happy", pose="point", y=1000), BOLT(350, 0.5, carry="coin", y=1000)]})
add("s45_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s46_button", "button", {
    **W1("robotown", robots=3, workers=1),
    "cam": cam((0, 500, 560, 1.15), (3.0, 500, 560, 1.3, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [BOLT(650, 0.0, carry="none", scale=1.3, y=1000),
              it("bubble", text="SO... DO I GET A SHARE?", x=650, y=300, at=0.6, until=2.8, tail=[650, 700], size=30),
              DANA(300, 0.4, face="smug", pose="point", scale=1.1, y=1000),
              it("bubble", text="BUDDY, YOU ARE THE SHARE.", x=300, y=330, at=2.9, tail=[300, 600], size=30)]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_robotsrich_storyboard.py; edit the generator, not this file.\n"
           "# Episode 64 storyboard (Who Gets Rich When Robots Do the Work?): bespoke worlds in CartoonStage/robotsrich.tsx.\n")
