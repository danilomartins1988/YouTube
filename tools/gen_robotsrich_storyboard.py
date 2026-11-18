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
    **W1("robotown", robots=[[0, 1], [C("They don't take a salary"), 3], [C("They never ask"), 6]], workers=[[0, 3], [C("They never ask"), 1]],
         flowAt=C("So when that warehouse"), flowTo="tower"),
    "cam": cam((0, 450, 560, 1.15), (C("They don't take a salary"), 450, 600, 1.3, 1.2), (C("So when that warehouse"), 700, 520, 0.95, 1.4),
               (C("In America"), 400, 520, 0.9, 1.2), (C("And most American stock"), 1000, 480, 1.0, 1.2), (C("So the real question"), 500, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("ROBOTS DO THE WORK", 450, 150, 0.1, until=C("They don't take a salary"), size=64),
              sign("NO SALARY", 250, 220, C("They don't take a salary"), color="#FFE0B2", size=34, until=C("So when that warehouse")),
              sign("NO VACATIONS", 520, 160, C("They don't take vacations"), color="#C8E6C9", size=34, until=C("So when that warehouse")),
              sign("NO RAISES", 780, 220, C("They never ask"), color="#BBDEFB", size=34, until=C("So when that warehouse")),
              words("WHO GETS THE MONEY?", 700, 150, C("So when that warehouse"), size=60, until=C("Here's a clue")),
              sign("WORKERS' SHARE OF BUSINESS OUTPUT: LOWEST ON RECORD", 400, 150, C("In America"), color="#FFCDD2", size=30, until=C("And most American stock")),
              sign("BLS LABOR SHARE INDEX · DATA SINCE 1947", 400, 220, C("Those records go back"), color="#FFFFFF", size=24, until=C("And most American stock")),
              sign("MOST U.S. STOCK: A SMALL GROUP (FED)", 1050, 150, C("And most American stock"), color="#FFF59D", size=30, until=C("So the real question")),
              words("WILL I KEEP MY JOB?", 500, 150, C("So the real question"), size=54, until=C("It may be")),
              words("DO I OWN ANY OF THE MACHINES?", 500, 150, C("It may be"), size=54, color="#FFFFFF"),
              DANA([[C("So the real question", -0.4), -700], [C("So the real question", 0.8), -200]], C("So the real question", -0.6), face="worry", pose="walk",
                   poses=[[C("So the real question", 0.8), "shrug"], [C("It may be"), "point"]], faces=[[0, "worry"], [C("It may be"), "shock"]]),
              tag((0, "THE SITUATION"), (C("In America"), "FACT"), (C("So the real question"), "QUESTION"))]},
    sources=["bls_ls", "fed_dfa"], sfx=[{"kind": "hit", "cue": "Here's a clue", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("rrtitle", lines=["WHO GETS RICH", "WHEN ROBOTS", "DO THE WORK?"], sub="FOLLOW THE MONEY WHEN MACHINES DO THE JOB"), "cam": STILL(), "drift": 0, "min_seconds": 5.8,
    "items": [DANA(300, 2.6, scale=1.0, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])

# ====================================================================== ACT 1: follow the $100
stage("s03_link", "a1_link", {
    **W1("robotown", robots=5, workers=2, whLabel="FACTORY"),
    "cam": cam((0, 450, 560, 1.0), (C("and in Could AI Bring Europe"), 600, 540, 1.05, 1.2), (C("Now let's follow"), 1000, 500, 1.0, WHIP)), "drift": 4,
    "items": [sign("EP 62 · COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?", 450, 150, 0.2, color="#BBDEFB", size=26, until=C("Now let's follow")),
              sign("EP 63 · COULD AI BRING EUROPE BACK TO POWER?", 600, 230, C("and in Could AI Bring Europe"), color="#C8E6C9", size=26, until=C("Now let's follow")),
              words("NOW: FOLLOW THE MONEY", 1000, 160, C("Now let's follow"), size=60, color="#FFFFFF"),
              BOLT([[0, -200], [C("Now let's follow"), 900]], 0.2, carry="coin", scale=1.1, y=1000),
              tag((0, "OUR SERIES"))]})
board("p04_split", "a1_draw", "$100 of U.S. income: who gets what?", C("Take a hundred dollars"), [
    {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("Take a hundred dollars")},
    {"d": "M 700 820 L 700 586 L 880 586 L 880 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.55, "kind": "bar", "start": C("Part goes to the people"), "label": lbl("PAY $58.40", 790, 710, 24, "ink")},
    {"d": "M 700 586 L 700 568 L 880 568 L 880 586 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.8, "kind": "bar", "start": C("Part goes to the owners"), "label": lbl("PROFITS $4.50", 1000, 580, 18, "ink")},
    {"d": "M 700 568 L 700 420 L 880 420 L 880 568 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("The rest covers"), "label": lbl("EVERYTHING ELSE", 790, 500, 18, "ink")},
    {"d": dot(790, 860), "color": "ink", "width": 1, "start": C("In nineteen seventy"), "label": lbl("1970", 790, 868, 30, "ink")},
    {"d": "M 1140 820 L 1140 616 L 1320 616 L 1320 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.55, "kind": "bar", "start": C("Last year"), "label": lbl("PAY $50.90", 1230, 725, 24, "ink")},
    {"d": "M 1140 616 L 1140 579 L 1320 579 L 1320 616 Z", "color": "accent", "width": 3, "fill": "accent", "fillOpacity": 0.8, "kind": "bar", "start": C("Meanwhile"), "label": lbl("$9.30", 1230, 605, 20, "ink")},
    {"d": "M 1140 579 L 1140 420 L 1320 420 L 1320 579 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.3, "kind": "bar", "start": C("Last year", 0.6), "label": lbl("EVERYTHING ELSE", 1230, 505, 18, "ink")},
    {"d": dot(1230, 860), "color": "ink", "width": 1, "start": C("Last year"), "label": lbl("2025", 1230, 868, 30, "ink")},
    {"d": arrow((900, 576), (1130, 596), -0.25), "color": "risk", "width": 5, "kind": "arrow", "start": C("roughly doubled"), "label": lbl("PROFITS ≈ ×2", 1015, 520, 24, "risk")},
    {"d": dot(1050, 905), "color": "muted", "width": 1, "start": C("Take a hundred dollars"), "label": lbl("SHARES OF U.S. GROSS DOMESTIC INCOME · PROFITS = DOMESTIC CORPORATE PROFITS AFTER TAX · SOURCE: BEA VIA FRED", 1050, 905, 15, "muted")},
], [{"kind": "point", "at": C("workers' pay took", 0.2), "dur": 1.4, "target": [790, 700]}, {"kind": "point", "at": C("roughly doubled", 0.2), "dur": 1.4, "target": [1230, 600]}],
    sources=["bea_gdi"])
stage("s05_splitter", "a1_scale", {
    **W1("splitter", pay=[[0, 58.4], [C("Seven and a half"), 58.4], [C("sounds small", 0.4), 50.9]], profit=[[0, 4.5], [C("Seven and a half"), 4.5], [C("sounds small", 0.4), 9.3]],
         other=[[0, 37.1], [C("Seven and a half"), 37.1], [C("sounds small", 0.4), 39.8]], year=[[0, "1970"], [C("sounds small"), "2025"]],
         hiAt=[[0, ""], [C("Seven and a half"), "pay"], [C("our rough math"), ""]],
         note="BEA (VIA FRED): SHARES OF GROSS DOMESTIC INCOME, 1970 vs 2025 · 'EVERYTHING ELSE' = DEPRECIATION, TAXES, INTEREST, RENT, SELF-EMPLOYED INCOME, ETC."),
    "cam": cam((0, 960, 520, 0.92), (C("On an economy"), 960, 470, 1.05, 1.2), (C("That's not money"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [counter(960, 640, C("our rough math"), 2.3, C("a year"), "OUR ROUGH MATH: 7.5 POINTS × $30.9T GDI (2025)", prefix="≈ $", suffix=" TRILLION A YEAR", decimals=1),
              sign("NOT STOLEN. THE SPLIT MOVED.", 960, 300, C("That's not money"), color="#FFF59D", size=34),
              BOLT(1650, 0.3, carry="coin", scale=0.9, y=900),
              tag((0, "FACT"), (C("our rough math"), "OUR MATH"))]},
    sources=["bea_gdi"])
board("p06_index", "a1_index", "Workers' share of U.S. business output (BLS index, 2017=100)", C("The Labor Department"), [
    {"d": "M 620 820 L 1500 820 M 620 820 L 620 420", "color": "ink", "width": 4, "start": C("The Labor Department")},
    {"d": dot(600, 470), "color": "muted", "width": 1, "start": C("The Labor Department"), "label": lbl("115", 600, 478, 18, "muted", "end")},
    {"d": dot(600, 770), "color": "muted", "width": 1, "start": C("The Labor Department"), "label": lbl("95", 600, 778, 18, "muted", "end")},
    {"d": "M 640 485 L 760 474 L 900 502 L 1080 505", "color": "accent2", "width": 7, "start": C("From nineteen forty-seven"), "label": lbl("A NARROW BAND, 1947-2000", 860, 450, 22, "accent2")},
    {"d": "M 1080 505 L 1260 683 L 1380 676 L 1470 761", "color": "risk", "width": 7, "start": C("Since then it has slid")},
    {"d": dot(1470, 761), "color": "risk", "width": 1, "start": C("in the latest data"), "label": lbl("93.7 · Q3 2026 · LOWEST SINCE 1947", 1330, 800, 20, "risk")},
    {"d": dot(760, 474), "color": "ink", "width": 1, "start": C("below its"), "label": lbl("PEAK 117.1 (1960)", 760, 440, 20, "ink")},
    {"d": arrow((800, 480), (1450, 750), 0.12), "color": "risk", "width": 4, "kind": "arrow", "start": C("twenty percent"), "label": lbl("≈ −20% (OUR CALC.)", 1180, 600, 24, "risk")},
    {"d": dot(1060, 870), "color": "muted", "width": 1, "start": C("The Labor Department"), "label": lbl("POINTS: 1947 Q1 116.0 · 1960 Q4 117.1 · 1980 112.1 · 2000 111.6 · 2010 99.5 · 2019 100.0 · 2026 Q3 93.7 (ANNUAL AVG. WHERE NO QUARTER) · BLS PRS85006173", 1060, 870, 13, "muted")},
    {"d": dot(1060, 900), "color": "muted", "width": 1, "start": C("The Labor Department"), "label": lbl("1947 · 1960 · 1980 · 2000 · 2010 · 2019 · 2026 (NOT TO SCALE IN TIME)", 1060, 900, 14, "muted")},
], [{"kind": "point", "at": C("Since then it has slid", 0.2), "dur": 1.4, "target": [1260, 683]}, {"kind": "point", "at": C("twenty percent", 0.2), "dur": 1.4, "target": [1470, 761]}],
    enter_left=False, sources=["bls_ls"])
stage("s07_why", "a1_why", {
    **W1("robotown", robots=[[0, 2], [C("When a machine does"), 2], [C("When a machine does", 1.0), 5]], workers=[[0, 3], [C("When a machine does"), 3], [C("When a machine does", 1.0), 1]],
         flowAt=C("the money that paid"), flowTo="tower"),
    "cam": cam((0, 500, 540, 0.9), (C("A robot is capital"), 450, 600, 1.2, 1.2), (C("the money that paid"), 700, 500, 0.92, 1.4)), "drift": 3,
    "items": [words("WHY?", 500, 140, 0.1, until=C("Global trade"), size=70),
              sign("SUSPECT 1: GLOBAL TRADE", 150, 150, C("Global trade"), color="#FFE0B2", size=28, until=C("But here's what robots add")),
              sign("SUSPECT 2: SUPERSTAR COMPANIES", 520, 220, C("a few superstar"), color="#E1D5FF", size=28, until=C("But here's what robots add")),
              sign("SUSPECT 3: AUTOMATION", 900, 150, C("and automation"), color="#BBDEFB", size=28, until=C("But here's what robots add")),
              words("A ROBOT IS CAPITAL", 450, 150, C("A robot is capital"), size=60, until=C("the money that paid")),
              sign("PAY → WHOEVER OWNS THE MACHINE", 700, 150, C("the money that paid"), color="#FFF59D", size=34),
              tag((0, "DEBATED CAUSES"), (C("But here's what robots add"), "MECHANISM"))]},
    sources=["autor_superstar", "ar_framework"])

# ====================================================================== ACT 2: who owns the machines?
bumper("s08_b2", "a2_card", "2", "WHO OWNS THE MACHINES?", "Hint: not the machines.", BLUE)
GROUPS = lambda at=(0, 0, 0, 0), v=(0.6, 11.4, 37.2, 50.9), disp=("$0.60", "$11.40", "$37.20", "$50.90"): [
    {"label": "BOTTOM 50", "n": 40, "v": v[0], "at": at[0], "color": GREY, "display": disp[0]},
    {"label": "NEXT 40", "n": 30, "v": v[1], "at": at[1], "color": TEAL, "display": disp[1]},
    {"label": "NEXT 9", "n": 9, "v": v[2], "at": at[2], "color": BLUE, "display": disp[2]},
    {"label": "TOP 1", "n": 1, "v": v[3], "at": at[3], "color": GOLD, "display": disp[3]}]
FOOT_EQ = "FED DISTRIBUTIONAL FINANCIAL ACCOUNTS, Q2 2026 · HOUSEHOLDS BY WEALTH · CORPORATE EQUITIES & MUTUAL FUND SHARES (EXCL. PENSIONS)"
stage("s09_own", "a2_own", {
    **W1("sharestreet", groups=GROUPS(at=(999, 999, 999, 999)), foot=FOOT_EQ),
    "cam": cam((0, 760, 520, 0.85), (C("Let's line up"), 300, 600, 1.1, 1.4), (C("and hand out"), 760, 480, 0.8, 1.6)), "drift": 3,
    "items": [words("WHO OWNS THE COMPANIES?", 760, 150, 0.2, until=C("Let's line up"), size=56),
              sign("100 HOUSEHOLDS · LEAST WEALTHY → MOST", 300, 160, C("Let's line up"), color="#FFFFFF", size=30, until=C("and hand out")),
              words("$100 OF STOCK TO SHARE OUT", 760, 130, C("and hand out"), size=54, color="#FFFFFF"),
              tag((0, "ILLUSTRATIVE SETUP"))]},
    sources=["fed_dfa"])
stage("s10_split", "a2_split", {
    **W1("sharestreet", groups=GROUPS(at=(C("The bottom fifty"), C("The next forty"), C("The next nine"), C("And the single richest"))), foot=FOOT_EQ),
    "cam": cam((0, 200, 640, 1.15), (C("The next forty"), 700, 560, 1.05, 1.2), (C("The next nine"), 1250, 480, 1.05, 1.2), (C("And the single richest"), 1700, 380, 1.0, 1.2),
               (C("Put together"), 900, 480, 0.78, 1.6)), "drift": 2,
    "items": [it("bubble", text="SIXTY CENTS. FOR ALL OF US.", x=200, y=330, at=C("Together."), until=C("The next forty"), tail=[200, 640], size=28),
              counter(900, 150, C("Put together"), 88.1, C("of these stocks"), "TOP 10% OF HOUSEHOLDS · FED DFA, Q2 2026", suffix="% OF THE STOCK", decimals=1),
              MILO(-150, 0.2, face="shock", pose="shrug", label="MILO · RETIRED BUS DRIVER", labelUntil=C("The next forty"), y=980),
              tag((0, "FACT"))]},
    sources=["fed_dfa"])
stage("s11_pension", "a2_pension", {
    **W1("sharestreet", groups=GROUPS(at=(C("Those are spread"), C("Those are spread", 0.5), C("The top ten percent"), C("The top ten percent", 0.4)), v=(4.8, 39.7, 44.1, 11.4),
                                      disp=("4.8%", "39.7%", "44.1%", "11.4%")),
         foot="FED DFA, Q2 2026 · DEFINED-CONTRIBUTION PENSION ENTITLEMENTS (401(k)-TYPE) · SHARES BY WEALTH GROUP"),
    "cam": cam((0, 760, 520, 0.8), (C("The top ten percent"), 1300, 460, 0.95, 1.2), (C("The bottom half"), 300, 600, 1.05, 1.2)), "drift": 2,
    "items": [words("401(k)-TYPE ACCOUNTS", 760, 140, 0.2, size=52, until=C("The top ten percent")),
              sign("TOP 10%: ≈55%", 1300, 140, C("The top ten percent"), color="#FFF59D", size=36, until=C("The bottom half")),
              sign("BOTTOM 50%: 4.8%", 300, 180, C("The bottom half"), color="#FFCDD2", size=36),
              tag((0, "FACT"))]},
    sources=["fed_dfa"])
stage("s12_flip", "a2_flip", {
    **W1("robotown", robots=5, workers=2, flowAt=C("If AI and robots move"), flowTo="tower", towerLabel="SHAREHOLDERS"),
    "cam": cam((0, 500, 540, 0.9), (C("For most of history"), 0, 600, 1.15, 1.2), (C("When machines do more"), 900, 500, 0.95, 1.4)), "drift": 3,
    "items": [words("PAYCHECKS → PROFITS → SHARES", 600, 150, C("If AI and robots move"), size=50, until=C("For most of history")),
              sign("THE OLD WAY UP: A BETTER JOB", 0, 170, C("For most of history"), color="#BBDEFB", size=32, until=C("When machines do more")),
              words("OWNING A PIECE MAY MATTER AS MUCH", 900, 150, C("When machines do more"), size=46, color="#FFFFFF"),
              DANA(-100, 0.2, face="worry", pose="clipboard", hold="clipboard", label="DANA · WAREHOUSE SHIFT LEAD", labelUntil=C("For most of history"),
                   faces=[[0, "worry"], [C("When machines do more"), "smug"]]),
              tag((0, "MECHANISM"), (C("When machines do more"), "A POSSIBILITY, NOT A FORECAST"))]})

# ====================================================================== ACT 3: the new factories
bumper("s13_b3", "a3_card", "3", "THE NEW FACTORIES", "The biggest machines ever built don't have arms.", PURPLE)
CAMPS = lambda ats: [{"name": "AMAZON", "v": 210.7, "display": "$210.7B", "at": ats[0]}, {"name": "ALPHABET", "v": 159.8, "display": "$159.8B", "at": ats[1]},
                     {"name": "MICROSOFT", "v": 135.9, "display": "$135.9B", "at": ats[2]}, {"name": "META", "v": 108.0, "display": "$108.0B", "at": ats[3]}]
FOOT_CAPEX = "CAPITAL SPENDING, 12 MONTHS TO SEP 30, 2026 · COMPANY FILINGS · AMAZON NET OF PROCEEDS · MICROSOFT CASH · META INCL. FINANCE LEASES · GENERIC BUILDINGS, NO LOGOS"
stage("s14_capex", "a3_capex", {
    **W1("dcfield", camps=CAMPS([C("Amazon spent"), C("Alphabet,"), C("Microsoft,"), C("Meta,")]), foot=FOOT_CAPEX),
    "cam": cam((0, 900, 520, 1.1), (C("Amazon spent"), 0, 480, 1.0, 1.2), (C("Alphabet,"), 500, 480, 1.0, 1.0), (C("Microsoft,"), 1000, 480, 1.0, 1.0),
               (C("Meta,"), 1300, 480, 1.0, 1.0), (C("Together"), 760, 470, 0.72, 1.4)), "drift": 2,
    "items": [words("DATA CENTERS", 900, 150, C("Data centers"), size=64, until=C("Amazon spent")),
              counter(760, 100, C("Together"), 614, C("in a single year"), "OUR SUM · DEFINITIONS DIFFER SLIGHTLY", prefix="≈ $", suffix="B IN ONE YEAR"),
              tag((0, "FACT"), (C("Together"), "OUR SUM"))]},
    sources=["byb_amzn", "byb_goog", "byb_msft", "byb_meta"])
stage("s15_nvidia", "a3_nvidia", {
    **W1("dcfield", camps=CAMPS([0, 0, 0, 0]), chipAt=0.3, chipX=1900, margin=[[0, 0], [C("and kept"), 0], [C("of every dollar"), 0.564]],
         marginText="≈ 56¢ OF EVERY $1 KEPT AS PROFIT", foot="NVIDIA, QUARTER ENDED OCT 25, 2026: REVENUE $115.8B · NET INCOME $65.3B · 56% IS OUR CALC. · GENERIC CHIP, NO LOGO"),
    "cam": cam((0, 900, 500, 0.75), (C("In its latest quarter"), 1850, 440, 1.0, 1.4)), "drift": 2,
    "items": [it("bubble", text="NVIDIA (THE CHIP SELLER)", x=1600, y=180, at=C("lands at the company"), until=C("In its latest quarter"), tail=[1850, 450], size=28),
              counter(1500, 140, C("In its latest quarter"), 115.8, C("in revenue"), "REVENUE, ONE QUARTER", prefix="$", suffix="B", decimals=1),
              counter(2200, 140, C("and kept"), 65.3, C("as profit"), "NET PROFIT, SAME QUARTER", prefix="$", suffix="B", decimals=1),
              BOLT([[0, 600], [C("lands at the company"), 1500]], 0.2, carry="coin", y=1000),
              tag((0, "FACT"), (C("That's about"), "OUR CALC."))]},
    sources=["byb_nvda"])
board("p16_loop", "a3_loop", "The AI money loop", C("A business pays"), [
    {"d": rect(600, 420, 240, 100), "color": "accent2", "width": 6, "kind": "box", "start": C("A business pays"), "label": lbl("BUSINESS", 720, 480, 28, "accent2")},
    {"d": arrow((845, 470), (1015, 470), -0.15), "color": "accent", "width": 6, "kind": "arrow", "start": C("That money goes"), "label": lbl("$ FOR AI", 930, 430, 22, "accent")},
    {"d": rect(1020, 420, 240, 100), "color": "accent3", "width": 6, "kind": "box", "start": C("That money goes"), "label": lbl("CLOUD", 1140, 480, 30, "accent3")},
    {"d": arrow((1140, 525), (1140, 630), 0.0), "color": "accent", "width": 6, "kind": "arrow", "start": C("buys chips")},
    {"d": rect(1020, 635, 240, 100), "color": "risk", "width": 6, "kind": "box", "start": C("buys chips"), "label": lbl("CHIPS + DATA CENTERS", 1140, 695, 20, "risk")},
    {"d": arrow((1015, 690), (845, 690), 0.0), "color": "accent", "width": 6, "kind": "arrow", "start": C("Profits flow")},
    {"d": rect(600, 635, 240, 100), "color": "accent", "width": 6, "kind": "box", "start": C("Profits flow"), "label": lbl("SHAREHOLDERS", 720, 695, 24, "accent")},
    {"d": arrow((720, 630), (720, 525), 0.0), "color": "muted", "width": 4, "kind": "arrow", "start": C("of both")},
    {"d": dot(1350, 560), "color": "muted", "width": 1, "start": C("A business pays"), "label": lbl("INSTEAD OF HIRING", 1400, 470, 22, "muted", "start")},
    {"d": dot(1060, 870), "color": "muted", "width": 1, "start": C("A business pays"), "label": lbl("A MECHANISM, NOT A MEASURED FLOW · NO FIGURES", 1060, 870, 16, "muted")},
], [{"kind": "point", "at": C("Profits flow", 0.2), "dur": 1.4, "target": [720, 690]}], enter_left=False)
stage("s17_missing", "a3_missing", {
    **W1("moneyloop", loopAt=0.0, outAt=C("The worker whose task"), doorAt=C("Unless that worker")),
    "cam": cam((0, 960, 500, 0.85), (C("The worker whose task"), 1350, 560, 1.0, 1.2), (C("Unless that worker"), 1150, 540, 0.9, 1.2)), "drift": 2,
    "items": [words("WHO'S MISSING?", 960, 120, 0.2, size=58, until=C("The worker whose task")),
              tag((0, "MECHANISM"))]})
stage("s18_risk", "a3_risk", {
    **W1("dcfield", camps=CAMPS([0, 0, 0, 0]), foot="AMAZON: FREE CASH FLOW, 12 MONTHS TO SEP 30, 2026 = 'AN OUTFLOW OF $42.4 BILLION' (COMPANY RELEASE)"),
    "cam": cam((0, 760, 500, 0.75), (C("Over those same"), 0, 500, 1.0, 1.2), (C("Owners get the upside"), 760, 500, 0.8, 1.4)), "drift": 2,
    "items": [words("A BET, NOT A GUARANTEE", 760, 120, 0.2, size=56, until=C("Over those same")),
              sign("AMAZON FREE CASH FLOW: −$42.4B (12 MONTHS)", 0, 140, C("Over those same"), color="#FFCDD2", size=32, until=C("Owners get the upside")),
              words("UPSIDE + RISK = OWNERSHIP", 760, 130, C("Owners get the upside"), size=52, color="#FFFFFF"),
              BOLT(200, 0.2, carry="none", moods=[[0, "happy"], [C("Over those same"), "sad"]], scale=1.1, y=1000),
              tag((0, "FACT"))]},
    sources=["byb_amzn"])

# ====================================================================== ACT 4: what the evidence says
bumper("s19_b4", "a4_card", "4", "WHAT THE EVIDENCE SAYS", "Measured findings on the left. Forecasts on the right.", TEAL)
CARD_BRYN = {"text": "SUPPORT AGENTS + AI: +14% ISSUES/HOUR", "sub": "+34% FOR NOVICES · 5,179 AGENTS · BRYNJOLFSSON, LI & RAYMOND (NBER)", "kind": "finding"}
CARD_DK = {"text": "DENMARK: NO MEASURABLE EFFECT ON PAY OR HOURS", "sub": "EFFECTS > 2% RULED OUT, 2 YEARS AFTER CHATGPT · HUMLUM & VESTERGAARD (NBER)", "kind": "finding"}
CARD_YOUNG = {"text": "AGES 22-25, AI-EXPOSED JOBS: −19% vs PEERS", "sub": "DESCRIPTIVE, NOT CAUSAL · ADP DATA TO JUNE 2026 · BRYNJOLFSSON, CHANDAR & CHEN", "kind": "finding"}
CARD_ACEM = {"text": "AI: ≤ +0.66% PRODUCTIVITY IN 10 YEARS", "sub": "AND A WIDER CAPITAL-LABOR INCOME GAP · ACEMOGLU (NBER, 2024) · A MODEL", "kind": "forecast"}
stage("s20_find", "a4_find", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": C("an AI assistant raised")}]),
    "cam": cam((0, 960, 480, 0.85), (C("First, findings"), 500, 420, 1.1, 1.2)), "drift": 2,
    "items": [words("MEASURED vs PREDICTED", 960, 110, 0.2, size=52, until=C("First, findings")),
              DANA(-60, 0.3, face="happy", pose="clipboard", hold="clipboard", y=1000, scale=1.0),
              tag((0, "SORTING THE EVIDENCE"), (C("First, findings"), "FINDING"))]},
    sources=["bryn"])
stage("s21_denmark", "a4_denmark", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": C("they found")}]),
    "cam": cam((0, 500, 470, 1.0), (C("they found"), 500, 520, 1.1, 1.2)), "drift": 2,
    "items": [BOLT(1500, 0.2, carry="box", scale=0.9, y=1000), tag((0, "FINDING"))]},
    sources=["humlum"])
stage("s22_young", "a4_young", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": 0}, {**CARD_YOUNG, "at": C("Young workers"), "kind": "descriptive"}]),
    "cam": cam((0, 500, 560, 1.05), (C("Experienced workers"), 500, 600, 1.1, 1.2), (C("The authors call"), 800, 520, 0.9, 1.2)), "drift": 2,
    "items": [sign("EARLY WARNING, NOT PROOF OF CAUSE", 1400, 300, C("The authors call"), color="#B2EBF2", size=32),
              MILO(1700, 0.2, face="worry", pose="stand", y=1000, scale=1.0),
              tag((0, "DESCRIPTIVE"))]},
    sources=["canaries"])
stage("s23_robots", "a4_robots", {
    **W1("robotown", robots=6, workers=[[0, 4], [C("cut the share"), 2]], whLabel="FACTORY · 1990-2007", homesLabel="LOCAL JOB MARKET"),
    "cam": cam((0, 450, 560, 1.0), (C("Between nineteen ninety"), 300, 560, 0.95, 1.2), (C("cut the share"), 0, 600, 1.1, 1.2)), "drift": 3,
    "items": [words("FACTORY ROBOTS: OLDER, CLEARER EVIDENCE", 450, 140, 0.2, size=44, until=C("Between nineteen ninety")),
              sign("+1 ROBOT PER 1,000 WORKERS (U.S., 1990-2007)", 300, 150, C("Between nineteen ninety"), color="#BBDEFB", size=30),
              sign("EMPLOYMENT RATE: −0.18 TO −0.34 POINTS", 0, 230, C("cut the share"), color="#FFCDD2", size=30),
              sign("WAGES: −0.25% TO −0.5%", 0, 300, C("and wages by"), color="#FFCDD2", size=30),
              sign("ACEMOGLU & RESTREPO (NBER / JPE)", 300, 380, C("cut the share"), color="#FFFFFF", size=22),
              tag((0, "FINDING"))]},
    sources=["ar_robots"])
stage("s24_forecast", "a4_forecast", {
    **W1("evidencelab", cards=[{**CARD_BRYN, "at": 0}, {**CARD_DK, "at": 0}, {**CARD_YOUNG, "at": 0, "kind": "descriptive"}, {**CARD_ACEM, "at": C("estimates AI")}]),
    "cam": cam((0, 960, 480, 0.85), (C("estimates AI"), 1420, 420, 1.1, 1.2), (C("Forecasts differ"), 960, 480, 0.85, 1.2)), "drift": 2,
    "items": [sign("A MODEL, NOT A MEASUREMENT", 1420, 560, C("That's a model"), color="#FFE0B2", size=32),
              words("FORECASTS DIFFER WIDELY", 960, 110, C("Forecasts differ"), size=50),
              tag((0, "FORECAST"))]},
    sources=["acemoglu"])

# ====================================================================== ACT 5: we've been here before
bumper("s25_b5", "a5_card", "5", "WE'VE BEEN HERE BEFORE", "Britain, the age of steam.", ORANGE)
stage("s26_britain", "a5_britain", {
    **W1("millyard", prog=[[0, 0.0], [C("Steam engines"), 0.05], [C("Workers' pay"), 0.5]], chartNote="ILLUSTRATIVE SHAPE OF ALLEN (2009): OUTPUT PER WORKER vs REAL WAGE, BRITAIN · NOT PLOTTED DATA"),
    "cam": cam((0, 960, 640, 1.1), (C("Steam engines"), 960, 520, 0.92, 1.4)), "drift": 3,
    "items": [words("BRITAIN, EARLY 1800s", 960, 130, 0.2, size=56, until=C("Steam engines")),
              sign("FACTORY OWNERS: RICH", 600, 620, C("Factory owners"), color="#FFF59D", size=30),
              sign("WORKERS' PAY: BARELY MOVED", 1350, 620, C("Workers' pay"), color="#FFCDD2", size=30),
              tag((0, "HISTORY"), (C("Steam engines"), "ILLUSTRATIVE SHAPE"))]},
    sources=["allen"])
board("p27_engels", "a5_draw", "Engels' pause (after Robert Allen, 2009)", C("Let me draw his story"), [
    {"d": "M 620 820 L 1500 820 M 620 820 L 620 420", "color": "ink", "width": 4, "start": C("Let me draw his story")},
    {"d": "M 640 790 Q 900 680 1100 560 T 1480 430", "color": "accent2", "width": 7, "start": C("output per worker kept climbing"), "label": lbl("OUTPUT PER WORKER", 1300, 440, 24, "accent2")},
    {"d": "M 640 795 L 1100 780", "color": "accent", "width": 7, "start": C("while real wages stagnated"), "label": lbl("REAL WAGE", 870, 760, 24, "accent")},
    {"d": "M 1100 780 Q 1300 650 1480 520", "color": "accent", "width": 7, "start": C("while real wages stagnated", 1.2)},
    {"d": rect(760, 560, 330, 210), "color": "risk", "width": 4, "kind": "box", "start": C("The profit rate doubled"), "label": lbl("PROFIT RATE ×2", 925, 610, 24, "risk")},
    {"d": dot(925, 650), "color": "risk", "width": 1, "start": C("and profits took"), "label": lbl("PROFIT SHARE ↑", 925, 655, 22, "risk")},
    {"d": dot(925, 520), "color": "ink", "width": 1, "start": C("Historians call it"), "label": lbl("“ENGELS' PAUSE”", 925, 520, 32, "ink")},
    {"d": dot(700, 860), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("1800", 700, 860, 20, "muted")},
    {"d": dot(1100, 860), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("≈1850", 1100, 860, 20, "muted")},
    {"d": dot(1060, 900), "color": "muted", "width": 1, "start": C("Let me draw his story"), "label": lbl("ILLUSTRATIVE SHAPE OF ALLEN'S FINDINGS · ENGELS, 'THE CONDITION OF THE WORKING CLASS IN ENGLAND' (1845)", 1060, 900, 15, "muted")},
], [{"kind": "point", "at": C("while real wages stagnated", 0.2), "dur": 1.4, "target": [870, 785]}, {"kind": "point", "at": C("The profit rate doubled", 0.2), "dur": 1.4, "target": [925, 610]}],
    sources=["allen"])
stage("s28_end", "a5_end", {
    **W1("millyard", prog=[[0, 0.55], [C("real wages began"), 0.6], [C("and the shares stabilized"), 1.0]], pauseAt=0.0, catchAt=C("real wages began")),
    "cam": cam((0, 960, 420, 1.0), (C("The pause ended"), 960, 520, 0.9, 1.2), (C("For the workers"), 700, 640, 1.15, 1.4)), "drift": 2,
    "items": [words("THE PAUSE ENDED...", 960, 640, C("The pause ended"), size=52, until=C("But it lasted")),
              words("...AFTER DECADES", 960, 640, C("But it lasted"), size=56, color="#FFFFFF"),
              tag((0, "HISTORY · ILLUSTRATIVE SHAPE"))]},
    sources=["allen"])

# ====================================================================== ACT 6: the case against the doom story
bumper("s29_b6", "a6_card", "6", "THE CASE AGAINST THE DOOM STORY", "Four reasons for hope, fairly stated.", GREEN)
stage("s30_newjobs", "a6_newjobs", {
    **W1("newjobs", old=[{"text": "SWITCHBOARD OPERATOR", "at": C("Machines take over"), "slot": 1}, {"text": "TYPIST POOL", "at": C("Machines take over", 0.3), "slot": 3},
                         {"text": "ELEVATOR OPERATOR", "at": C("Machines take over", 0.6), "slot": 5}],
         fresh=[{"text": "SOFTWARE DEVELOPER", "at": C("Economists led by"), "slot": 1, "up": 0}, {"text": "WIND TURBINE TECH", "at": C("found that most"), "slot": 3},
                {"text": "DATA ANALYST", "at": C("job specialties"), "slot": 5}, {"text": "AI TRAINER", "at": C("new kinds of work"), "slot": 2}]),
    "cam": cam((0, 900, 520, 0.8), (C("found that most"), 900, 500, 0.85, 1.2), (C("Machines take over"), 900, 520, 0.8, 1.2)), "drift": 3,
    "items": [words("1. NEW JOBS", 900, 120, 0.2, size=60, until=C("Economists led by")),
              sign("MOST JOBS TODAY: SPECIALTIES THAT DIDN'T EXIST IN 1940 (AUTOR ET AL.)", 900, 120, C("found that most"), color="#C8E6C9", size=28),
              sign("JOB TITLES: ILLUSTRATIVE EXAMPLES", 900, 190, C("Machines take over"), color="#FFFFFF", size=22),
              tag((0, "FINDING"))]},
    sources=["autor_newwork"])
stage("s31_wages", "a6_wages", {
    **W1("robotown", robots=5, workers=3, whLabel="WAREHOUSE · NEW TASKS"),
    "cam": cam((0, 450, 560, 1.05), (C("Even the economists"), 300, 540, 0.95, 1.4)), "drift": 3,
    "items": [words("2. PRODUCTIVITY CAN LIFT PAY", 450, 140, 0.2, size=50, until=C("Cheaper production")),
              sign("CHEAPER → PEOPLE BUY MORE", 300, 150, C("Cheaper production"), color="#BBDEFB", size=32, until=C("Even the economists")),
              sign("AI-SAVVY WORKERS → MORE VALUABLE", 650, 230, C("and workers who use"), color="#C8E6C9", size=30, until=C("Even the economists")),
              words("NEW TASKS: WORKERS' STRONGEST ALLY", 300, 150, C("Even the economists"), size=46, color="#FFFFFF"),
              DANA(-100, 0.3, face="happy", pose="clipboard", hold="clipboard", y=1000, label="DANA · NOW RUNS THE ROBOT FLEET", labelUntil=C("Even the economists")),
              tag((0, "MECHANISM"))]},
    sources=["ar_framework", "bryn"])
stage("s32_degree", "a6_degree", {
    "zones": [Z("triad", title="MEDIAN WEEKLY PAY, FULL-TIME, AGE 25+, Q3 2026 (BLS)", scale=0.32, gap=520,
                bars=[{"label": "BACHELOR'S OR MORE", "v": 1752, "color": BLUE, "display": "$1,752", "at": C("earned a typical")},
                      {"label": "HIGH SCHOOL ONLY", "v": 993, "color": GREY, "display": "$993", "at": C("versus")}],
                foot="BLS CURRENT POPULATION SURVEY VIA FRED (LEU0252918500Q, LEU0252917300Q) · NOT SEASONALLY ADJUSTED")], "worldW": 2400,
    "cam": cam((0, 960, 520, 0.95), (C("versus"), 960, 500, 1.0, 1.2)), "drift": 2,
    "items": [words("3. SKILLS STILL PAY", 960, 200, 0.2, size=56, until=C("This summer")),
              tag((0, "FACT"))]},
    sources=["bls_edu"])
stage("s33_policy", "a6_policy", {
    **W1("robotown", robots=4, workers=3, towerLabel="CITY HALL?", homesLabel="VOTERS"),
    "cam": cam((0, 450, 540, 0.9), (C("Others prefer training"), 600, 520, 0.95, 1.2), (C("This film takes no side"), 450, 540, 0.85, 1.2)), "drift": 3,
    "items": [words("4. POLICY CAN CHANGE THE SPLIT", 450, 130, 0.2, size=48, until=C("Some propose")),
              sign("SPREAD OWNERSHIP (EMPLOYEE STOCK, KIDS' ACCOUNTS, PUBLIC FUNDS)", 450, 140, C("Some propose"), color="#C8E6C9", size=24),
              sign("TRAINING", 150, 220, C("Others prefer training"), color="#BBDEFB", size=30),
              sign("TAX WORK vs CAPITAL DIFFERENTLY", 600, 220, C("or changing how"), color="#FFE0B2", size=28),
              sign("LET MARKETS ADJUST", 1000, 220, C("Others say markets"), color="#E1D5FF", size=30),
              words("EACH HAS TRADE-OFFS · NO SIDE TAKEN", 450, 320, C("Each has trade-offs"), size=40, color="#FFFFFF"),
              tag((0, "OPTIONS, NOT ENDORSEMENTS"))]})

# ====================================================================== ACT 7: what can you actually own?
bumper("s34_b7", "a7_card", "7", "WHAT CAN YOU ACTUALLY OWN?", "Education, not investment advice.", NAVY)
DOORS = lambda ats: [{"label": "401(k) / IRA", "sub": "RETIREMENT ACCOUNT", "at": ats[0], "color": BLUE},
                     {"label": "INDEX FUND", "sub": "SLICES OF MANY COMPANIES", "at": ats[1], "color": GREEN},
                     {"label": "EMPLOYEE STOCK", "sub": "ESOPs AND STOCK PLANS", "at": ats[2], "color": ORANGE}]
stage("s35_now", "a7_now", {
    **W1("doorways", doors=DOORS([999, 999, 999])),
    "cam": cam((0, 960, 480, 0.85), (C("Here's where Americans"), 960, 500, 0.9, 1.2)), "drift": 2,
    "items": [counter(960, 300, C("In the Federal Reserve's"), 56, C("owned some stock"), "FAMILIES OWNING ANY STOCK, 2025 (FED SCF)", suffix="%"),
              sign("BOTTOM HALF BY INCOME: 31%", 560, 420, C("bottom half by income"), color="#FFCDD2", size=32),
              sign("TOP 10% BY INCOME: 97%", 1360, 420, C("In the top tenth"), color="#C8E6C9", size=32),
              MILO(200, 0.2, face="happy", pose="wave", y=1000, scale=1.0),
              tag((0, "EDUCATION, NOT ADVICE"), (C("Here's where Americans"), "FACT"))]},
    sources=["scf25"])
board("p36_doors", "a7_doors", "Three common doors to owning (education, not advice)", C("Let me draw the doors"), [
    {"d": rect(600, 440, 220, 320), "color": "accent2", "width": 6, "kind": "box", "start": C("The most common one"), "label": lbl("401(k) / IRA", 710, 420, 26, "accent2")},
    {"d": dot(710, 600), "color": "ink", "width": 1, "start": C("Today,"), "label": lbl("54.9% OF FAMILIES", 710, 600, 22, "ink")},
    {"d": rect(900, 440, 220, 320), "color": "accent3", "width": 6, "kind": "box", "start": C("index funds"), "label": lbl("INDEX FUND", 1010, 420, 26, "accent3")},
    {"d": dot(1010, 600), "color": "ink", "width": 1, "start": C("small slices"), "label": lbl("MANY COMPANIES", 1010, 600, 20, "ink")},
    {"d": rect(1200, 440, 220, 320), "color": "accent", "width": 6, "kind": "box", "start": C("Some employers"), "label": lbl("EMPLOYEE STOCK", 1310, 420, 24, "accent")},
    {"d": dot(1310, 600), "color": "ink", "width": 1, "start": C("Employee stock ownership plans"), "label": lbl("ESOPs: 15.1M PEOPLE", 1310, 600, 20, "ink")},
    {"d": dot(1010, 830), "color": "muted", "width": 1, "start": C("Let me draw the doors"), "label": lbl("FED SCF 2025 · NCEO (2023 PLAN DATA) · NOTHING HERE IS A RECOMMENDATION TO BUY ANYTHING", 1010, 830, 16, "muted")},
], [{"kind": "point", "at": C("index funds", 0.2), "dur": 1.4, "target": [1010, 600]}, {"kind": "point", "at": C("Employee stock ownership plans", 0.2), "dur": 1.4, "target": [1310, 600]}],
    sources=["scf25", "nceo"])
stage("s37_risk", "a7_risk", {
    **W1("doorways", doors=DOORS([0, 0, 0]), riskAt=C("Stock prices can fall"),
         risks=[[0, ""], [C("Stock prices can fall"), "PRICES CAN FALL HARD"], [C("Fees eat returns"), "FEES EAT RETURNS"], [C("And betting your savings"), "ONE COMPANY = RISK ON RISK"]]),
    "cam": cam((0, 960, 520, 0.85), (C("Stock prices can fall"), 960, 380, 1.0, 1.2), (C("Owning a slice"), 960, 500, 0.85, 1.2)), "drift": 2,
    "items": [words("OWNING ISN'T FREE MONEY", 960, 160, 0.2, size=54, until=C("Stock prices can fall")),
              words("YOU SHARE THE BAD YEARS TOO", 960, 820, C("Owning a slice"), size=46, color="#FFFFFF"),
              tag((0, "EDUCATION, NOT ADVICE"))]})

# ====================================================================== ACT 8: who gets rich?
bumper("s38_b8", "a8_card", "8", "WHO GETS RICH?", "The answer, and the fine print.", GOLD)
stage("s39_verdict", "a8_verdict", {
    **W1("sharestreet", groups=GROUPS(at=(0.2, 0.4, 0.6, 0.8)), foot=FOOT_EQ),
    "cam": cam((0, 760, 520, 0.8), (C("mostly the people"), 1600, 420, 1.0, 1.4), (C("In America"), 1100, 480, 0.85, 1.4)), "drift": 2,
    "items": [words("WHO GETS RICH?", 760, 130, 0.2, size=60, until=C("mostly the people")),
              words("THE OWNERS", 1600, 110, C("mostly the people"), size=60, color="#FFFFFF", until=C("In America")),
              sign("TOP 10%: ALMOST $9 OF EVERY $10 OF STOCK", 1100, 130, C("In America"), color="#FFF59D", size=32),
              tag((0, "VERDICT"), (C("In America"), "FACT"))]},
    sources=["fed_dfa"])
stage("s40_but", "a8_but", {
    **W1("robotown", robots=5, workers=3, flowAt=0.2, flowTo="both"),
    "cam": cam((0, 450, 540, 0.9), (C("History says"), 200, 560, 1.05, 1.2), (C("More than half"), 450, 540, 0.85, 1.4)), "drift": 3,
    "items": [words("IT DOESN'T HAVE TO STAY NARROW", 450, 140, 0.2, size=48, until=C("History says")),
              sign("PAY CAN CATCH UP (AFTER A DELAY)", 150, 150, C("History says"), color="#C8E6C9", size=30, until=C("More than half")),
              sign("NEW JOBS APPEAR", 650, 230, C("New jobs"), color="#BBDEFB", size=30, until=C("More than half")),
              sign("56% OF FAMILIES OWN SOME STOCK (FED SCF 2025)", 450, 150, C("More than half"), color="#FFF59D", size=30),
              DANA(-150, 0.3, face="happy", pose="cheer", y=1000), MILO(80, 0.4, face="happy", pose="wave", y=1000),
              tag((0, "VERDICT"), (C("More than half"), "FACT"))]},
    sources=["allen", "autor_newwork", "scf25"])
stage("s41_close", "a8_close", {
    **W1("robotown", robots=6, workers=2, flowAt=0.5, flowTo="both"),
    "cam": cam((0, 300, 560, 1.15), (C("In the age of AI"), 500, 520, 0.95, 1.6), (C("What do you own"), 450, 520, 0.85, WHIP)), "drift": 2,
    "items": [words("WHAT DO YOU DO FOR A LIVING?", 300, 150, 0.3, size=50, until=C("In the age of AI")),
              words("...AND", 500, 150, C("In the age of AI"), size=56, until=C("What do you own")),
              words("WHAT DO YOU OWN?", 450, 160, C("What do you own"), size=72, color="#FFFFFF"),
              DANA(-100, 0.3, face="happy", pose="point", y=1000), BOLT(350, 0.5, carry="coin", y=1000)]})
add("s42_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s43_button", "button", {
    **W1("robotown", robots=3, workers=1),
    "cam": cam((0, 500, 560, 1.15), (3.0, 500, 560, 1.3, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [BOLT(650, 0.0, carry="none", scale=1.3, y=1000),
              it("bubble", text="SO... DO I GET A SHARE?", x=650, y=300, at=0.6, until=2.8, tail=[650, 700], size=30),
              DANA(300, 0.4, face="smug", pose="point", scale=1.1, y=1000),
              it("bubble", text="BUDDY, YOU ARE THE SHARE.", x=300, y=330, at=2.9, tail=[300, 600], size=30)]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_robotsrich_storyboard.py; edit the generator, not this file.\n"
           "# Episode 64 storyboard (Who Gets Rich When Robots Do the Work?): bespoke worlds in CartoonStage/robotsrich.tsx.\n")
