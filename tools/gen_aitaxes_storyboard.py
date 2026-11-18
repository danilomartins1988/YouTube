"""Generates projects/if-ai-replaces-workers-who-pays-the-taxes/deliverables/documentary/storyboard.yaml
(Episode 69: If AI Replaces Workers, Who Pays the Taxes?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/aitaxes.tsx (txtown, txware, txpipes, txfair, txscale, txjars, txalaska, txmail, txclock,
txmeeting, txtitle, txbumper; items stub, rivet). Story over statistics: one protagonist (ROSA, mayor of fictional PINEWICK) with STUB
(the walking pay stub) and RIVET (the robot); all fictional. No real person is drawn (Bill Gates is quoted in narration only); no logos.
Signature animations: 1 the robot with no pockets (s03), 2 the money tank and its two taps (s07-s09, s14, s36), 3 the idea fair and the
Fair Scale (s16-s33, one good reason vs one catch per idea), 4 the Social Security reserve clock (s11, s12, s37), 5 checks to mailboxes.
Presenter boards: p10 the tank built for the big tap, p24 who carries the bill, p35 the whole puzzle on one page.
Run: python tools/gen_aitaxes_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "if-ai-replaces-workers-who-pays-the-taxes"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#1E88E5", "#F5B700", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#16223A", "#F08A24"
PINK = "#E86A92"
OX = 3400  # offset for a second zone


def ROSA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=7, skin=4, hair=1, hairStyle=3, color=RED, glasses=False, scarf=GOLD, **kw)


def LOCAL(x=None, at=0.0, v=9, color=BLUE, **kw):
    kw.setdefault("scale", 1.1)
    return it("toon", x=x, at=at, who="shopper", v=v, skin=(v * 3) % 6, hair=(v * 5) % 7, hairStyle=v % 6, color=color, glasses=v % 2 == 0, **kw)


def STUB(x, at=0.0, **kw):
    kw.setdefault("y", 860)
    kw.setdefault("scale", 0.9)
    return it("stub", x=x, at=at, **kw)


def RIV(x, at=0.0, **kw):
    kw.setdefault("y", 860)
    kw.setdefault("scale", 0.8)
    return it("rivet", x=x, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def bub(text, x, y, at, until=None, tail=None, size=30):
    d = {"text": text, "x": x, "y": y, "at": at, "size": size}
    if until is not None:
        d["until"] = until
    if tail:
        d["tail"] = tail
    return it("bubble", **d)


def tag(*keys, at=0.0):
    return it("pmtag", at=at, x=36, y=36, tags=[[k[0], k[1]] for k in keys])


def bumper(id_, seg, act, title, caption, color):
    stage(id_, seg, {**W1("txbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.2, "items": [STUB([[0, 2300], [1.4, 1640]], 1.0, y=1040, scale=0.7, face="happy", hops=[2.2])]},
          sfx=[{"kind": "whoosh", "at": 0.25, "gain": 0.25}, {"kind": "hit", "at": 1.0, "gain": 0.3}])


def board(id_, seg, title, start, strokes, actions, enter_left=True, sources=()):
    add(id_, seg, "engine_draw", {
        "title": title, "board": BOARD, "draw_start": C(start), "speed": 1500, "push": 0.003,
        "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3} if enter_left else {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
        "strokes": strokes, "actions": actions, "scale": 0.86, "floor": 1040}, sources=sources)


def S(d, color, start, label=None, width=5, **kw):
    s = {"d": d, "color": color, "width": width, "start": start, **kw}
    if label:
        s["label"] = label
    return s


# ====================================================================== CHAPTER 1: the robot with no paycheck
PARTY = {"robots": [[0, 1], [C("For the robots"), 4]], "lockers": [[0, 0], [C("Not for the workers"), 4]], "party": 0.0,
         "sign": [[0, "WELCOME, ROBOTS!"], [C("never pay income tax"), "PAYROLL: 0 ROBOTS"]]}
stage("s01_hook", "co_hook", {
    **W2("txtown", "txware", {"banner": [[0, "WELCOME TO PINEWICK"]]}, PARTY),
    "cam": cam((0, 900, 560, 1.0), (C("the warehouse on the hill"), 1600, 520, 1.15, 1.2), (C("This morning"), OX + 900, 520, 0.9, WHIP),
               (C("For the robots"), OX + 1200, 520, 1.0, 1.2), (C("never get a paycheck"), OX + 760, 560, 1.15, 1.2),
               (C("Rosa looks at"), OX + 600, 560, 1.2, 1.0), (C("If robots do the work"), OX + 960, 520, 0.85, 1.6)), "drift": 3,
    "items": [ROSA([[0, -200], [1.6, 700]], 0.0, face="happy", pose="wave", faces=[[0, "happy"]], label="ROSA · MAYOR OF PINEWICK (FICTIONAL)", labelUntil=C("This morning")),
              ROSA(OX + 520, C("This morning"), face="happy", pose="stand", faces=[[0, "happy"], [C("Not for the workers"), "squint"], [C("never get a paycheck"), "shock"], [C("Rosa looks at"), "worry"]]),
              RIV([[0, OX + 2300], [C("For the robots"), OX + 2300], [C("For the robots", 2.0), OX + 1100]], 0.0, face="happy", carry="box"),
              words("THE PARTY IS FOR THE ROBOTS", OX + 1100, 220, C("For the robots"), size=56, until=C("never get a paycheck")),
              words("NO PAYCHECK → NO INCOME TAX", OX + 900, 220, C("never get a paycheck"), size=56, until=C("If robots do the work")),
              words("IF ROBOTS DO THE WORK, WHO PAYS THE TAXES?", OX + 960, 210, C("If robots do the work"), size=50),
              tag((0, "STORY · FICTIONAL CAST"), (C("never pay income tax"), "MECHANISM"))]},
    sfx=[{"kind": "whoosh", "cue": "This morning", "gain": 0.3}, {"kind": "hit", "cue": "If robots do the work", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("txtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [STUB([[0, -200], [2.2, 260]], 1.6, y=1060, scale=0.6, face="happy", hops=[3.4])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_rivet", "c1_rivet", {
    **W1("txware", robots=3, lockers=4, sign=[[0, "NEW HIRE: RIVET"]]),
    "cam": cam((0, 1000, 540, 0.95), (C("Meet Rivet"), 1150, 520, 1.15, 1.2), (C("Rosa asks Rivet"), 900, 560, 1.05, 1.2), (C("Rivet checks"), 1150, 520, 1.2, 1.0),
               (C("I don't even have pockets"), 1150, 560, 1.25, 0.8)), "drift": 2,
    "items": [RIV([[0, 2300], [2.0, 1200]], 0.0, face="happy", faces=[[0, "happy"], [C("Rivet checks"), "wow"], [C("I don't have a paycheck"), "worry"]], carry="box",
                  label="RIVET · WAREHOUSE ROBOT (FICTIONAL)", labelUntil=C("Rosa asks Rivet"), pockets=C("I don't even have pockets")),
              ROSA(700, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Rosa asks Rivet"), "squint"], [C("I don't even have pockets"), "shock"]]),
              bub("WHERE DOES YOUR PAYCHECK GO?", 700, 300, C("Where does your paycheck go"), until=C("Rivet checks"), tail=[700, 560]),
              bub("I DON'T HAVE A PAYCHECK.", 1200, 260, C("I don't have a paycheck"), until=C("I don't even have pockets"), tail=[1180, 500]),
              bub("I DON'T EVEN HAVE POCKETS.", 1200, 260, C("I don't even have pockets"), tail=[1180, 500]),
              tag((0, "STORY"))]},
    sfx=[{"kind": "hit", "cue": "I don't even have pockets", "gain": 0.3}])
stage("s04_stub", "c1_stub", {
    **W1("txtown", banner=[[0, "PINEWICK"]], closed=[[0, 0], [C("before his job went"), 0.34]]),
    "cam": cam((0, 900, 560, 1.0), (C("This is Stub"), 1100, 600, 1.2, 1.2), (C("before his job went"), 1500, 540, 0.95, 1.4), (C("Every paycheck"), 1000, 580, 1.15, 1.2),
               (C("Follow me"), 960, 560, 0.95, 1.2)), "drift": 3,
    "items": [ROSA(700, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("This is Stub"), "wow"], [C("Every paycheck"), "happy"]]),
              STUB([[0, 2300], [C("Then Rosa meets"), 2300], [C("This is Stub"), 1000]], 0.0, face="happy", faces=[[0, "happy"], [C("before his job went"), "sad"], [C("Every paycheck"), "happy"]],
                   hops=[C("This is Stub", 0.8), C("Follow me", 0.3)], label="STUB · RAY'S LAST PAY STUB (FICTIONAL)", labelUntil=C("before his job went")),
              words("RAY'S LAST PAYCHECK", 1300, 220, C("the last one ever printed"), size=58, until=C("Every paycheck")),
              bub("EVERY PAYCHECK CARRIES A PIECE OF THE TOWN.", 1050, 300, C("Every paycheck"), until=C("Follow me"), tail=[1020, 580], size=26),
              bub("FOLLOW ME!", 1050, 320, C("Follow me"), tail=[1020, 580]),
              tag((0, "STORY · FICTIONAL CAST"))]})
stage("s05_whatif", "c1_whatif", {
    **W1("txtown", bus=True, banner=[[0, "A WHAT-IF, NOT A FORECAST"]]),
    "cam": cam((0, 960, 540, 0.9), (C("people are still working"), 700, 560, 1.05, 1.4), (C("Nobody knows"), 1400, 520, 1.0, 1.4), (C("But if it takes"), 960, 560, 1.15, 1.4)), "drift": 3,
    "items": [LOCAL(300, 0.0, v=3, color=ORANGE, face="happy", pose="walk"), LOCAL(520, 0.3, v=8, color=BLUE, face="happy", pose="stand", hold="coffee"),
              LOCAL(1500, 0.6, v=11, color=GREEN, face="happy", pose="stand"),
              words("STILL WORKING. STILL GETTING PAID.", 800, 220, C("people are still working"), size=52, until=C("Nobody knows")),
              words("HOW MANY JOBS WILL AI TAKE? NOBODY KNOWS.", 1100, 220, C("Nobody knows"), size=46, until=C("But if it takes")),
              ROSA(1000, C("But if it takes"), face="worry", pose="stand"), STUB(1200, C("But if it takes"), face="worry"),
              tag((0, "SCENARIO · NOT A FORECAST"))]})

# ====================================================================== CHAPTER 2: follow the paycheck
bumper("s06_b2", "c2_card", "CHAPTER TWO", "Follow the paycheck", "Where every payday goes", BLUE)
stage("s07_split", "c2_split", {
    **W1("txpipes", big=[[0, 0.6]], thin=0, level=[[0, 0.2], [C("A slice went to Washington"), 0.5], [C("another slice went"), 0.7]], bigLabel="RAY'S PAYCHECK"),
    "cam": cam((0, 700, 560, 1.0), (C("some of it was already gone"), 500, 560, 1.15, 1.2), (C("schools and roads"), 1450, 480, 1.05, 1.4),
               (C("A slice went to Washington"), 960, 500, 0.95, 1.2), (C("another slice went"), 1450, 620, 1.05, 1.4)), "drift": 2,
    "items": [STUB(520, 0.0, y=1000, scale=0.75, face="happy", torn=[[0, 0], [C("a slice went to the state"), 1], [C("A slice went to Washington"), 2], [C("another slice went"), 3]],
                   faces=[[0, "happy"], [C("some of it was already gone"), "wow"], [C("another slice went"), "worry"]]),
              ROSA(260, 0.0, y=1040, scale=0.9, face="squint", pose="stand"),
              words("SLICE 1: THE STATE (SCHOOLS, ROADS)", 1100, 220, C("a slice went to the state"), size=44, until=C("A slice went to Washington")),
              words("SLICE 2: WASHINGTON (INCOME TAX)", 1100, 220, C("A slice went to Washington"), size=46, until=C("another slice went")),
              words("SLICE 3: SOCIAL SECURITY", 1100, 220, C("another slice went"), size=50),
              tag((0, "MECHANISM · SIMPLIFIED"))]})
stage("s08_big", "c2_big", {
    **W1("txpipes", big=[[0, 0.7], [C("almost nine out of every ten"), 1.0]], thin=0.15, level=0.8),
    "cam": cam((0, 960, 540, 0.9), (C("almost nine out of every ten"), 600, 480, 1.1, 1.4), (C("through their income taxes"), 900, 520, 0.95, 1.4)), "drift": 2,
    "items": [STUB(1240, 0.0, y=1000, scale=0.7, face="happy", hops=[C("almost nine out of every ten", 0.5)]),
              words("≈ 9 OF EVERY 10 FEDERAL TAX DOLLARS COME FROM PEOPLE", 960, 210, C("almost nine out of every ten"), size=44),
              tag((0, "STORY"), (C("In America"), "OUR CALC · TREASURY FY2026"))]},
    sources=["mts_fy26", "cbo_mbr26"], sfx=[{"kind": "hit", "cue": "almost nine out of every ten", "gain": 0.3}])
stage("s09_corp", "c2_corp", {
    **W1("txpipes", big=1, thin=[[0, 0.15], [C("Corporate income tax"), 0.2]], level=0.8),
    "cam": cam((0, 960, 540, 0.9), (C("Corporate income tax"), 500, 640, 1.2, 1.2), (C("Rivet's company pays that"), 700, 620, 1.05, 1.2), (C("Rivet looks"), 760, 640, 1.2, 1.0)), "drift": 2,
    "items": [words("COMPANIES: ≈ 7¢ OF EVERY FEDERAL TAX $1", 700, 220, C("Corporate income tax"), size=46, until=C("Rivet itself pays nothing")),
              words("RIVET ITSELF: $0", 760, 220, C("Rivet itself pays nothing"), size=60),
              RIV([[0, -300], [C("Rivet's company pays that"), -300], [C("Rivet's company pays that", 1.6), 720]], 0.0, y=1040, scale=0.6, face="happy", faces=[[0, "happy"], [C("Rivet looks"), "worry"]]),
              tag((0, "OUR CALC · TREASURY FY2026"))]},
    sources=["mts_fy26"])
board("p10_draw", "c2_draw", "The tank built for the big tap", "Let me draw why", [
    S(rect(1000, 420, 360, 420), "ink", C("the government's money tank"), width=6, kind="box", label=lbl("THE MONEY TANK", 1180, 400, 30, "ink")),
    S(rect(1010, 560, 340, 270), "accent2", C("the government's money tank"), width=3, fill="accent2", fillOpacity=0.4, kind="bar"),
    S("M 560 500 L 990 500", "accent2", C("one big tap"), width=36, label=lbl("BIG TAP: PAYCHECKS", 760, 460, 28, "accent2")),
    S("M 600 760 L 990 760", "accent3", C("A thin tap"), width=8, label=lbl("THIN TAP: PROFITS", 790, 730, 26, "accent3")),
    S(rect(540, 440, 300, 120), "risk", C("The big tap shrinks"), width=6, kind="box", label=lbl("SHRINKS", 690, 600, 30, "risk")),
    S(arrow((620, 800), (860, 800), -0.2), "accent3", C("might grow"), width=5, kind="arrow", label=lbl("MIGHT GROW", 740, 860, 26, "accent3")),
    S("M 1400 470 Q 1600 470 1700 560", "ink", C("the whole tank was built"), width=5, label=lbl("BUILT FOR THE BIG ONE", 1560, 430, 28, "ink")),
    S(dot(1150, 960), "muted", C("Let me draw why"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NOT TO SCALE)", 1150, 960, 16, "muted")),
], [{"kind": "point", "at": C("one big tap", 0.3), "dur": 1.4, "target": [760, 500]}, {"kind": "point", "at": C("The big tap shrinks", 0.3), "dur": 1.4, "target": [690, 500]},
    {"kind": "react", "at": C("the whole tank was built", 0.3)}])
stage("s11_ss", "c2_ss", {
    **W1("txclock", inflow=[[0, 1], [C("No wages, no payroll tax"), 0.25], [C("already under strain"), 0.8]], level=[[0, 0.7], [C("run dry in 2034"), 0.08]],
         year=[[0, ""], [C("run dry in 2034"), "2034"]]),
    "cam": cam((0, 900, 540, 0.9), (C("the payroll tax"), 400, 520, 1.1, 1.2), (C("No wages, no payroll tax"), 500, 540, 1.2, 1.0), (C("Its trustees say"), 1400, 480, 1.05, 1.4)), "drift": 2,
    "items": [words("PAID BY A TAX ON WAGES", 600, 220, C("the payroll tax"), size=54, until=C("No wages, no payroll tax")),
              words("NO WAGES → NO PAYROLL TAX", 600, 220, C("No wages, no payroll tax"), size=54, until=C("Its trustees say")),
              words("RESERVE RUNS DRY: 2034", 1300, 220, C("run dry in 2034"), size=60),
              STUB(1000, 0.0, y=1000, scale=0.65, face="worry"),
              tag((0, "FACT · TREASURY (PAYROLL TAXES FUND IT)"), (C("Its trustees say"), "PROJECTION · TRUSTEES 2026"))]},
    sources=["ssa_tr26", "aaa_tr26", "mts_fy26"], sfx=[{"kind": "hit", "cue": "run dry in 2034", "gain": 0.3}])
stage("s12_ss2", "c2_ss2", {
    **W1("txclock", inflow=0.8, level=0.05, year=[[0, "2034"]]),
    "cam": cam((0, 1300, 540, 0.95), (C("only part of every check"), 1600, 560, 1.15, 1.2), (C("Stub does the math"), 1000, 600, 1.2, 1.2)), "drift": 2,
    "items": [words("THEN: ONLY PART OF EACH CHECK", 1300, 220, C("only part of every check"), size=54, until=C("Stub does the math")),
              STUB(1000, 0.0, y=1000, scale=0.7, face="worry", faces=[[0, "worry"], [C("he doesn't have many fingers"), "wow"]]),
              bub("UH... CARRY THE ONE?", 1000, 360, C("Stub does the math"), tail=[1000, 640]),
              tag((0, "PROJECTION · TRUSTEES 2026 (≈83%)"))]},
    sources=["ssa_tr26"])
stage("s13_world", "c2_world", {
    **W1("txjars", fill=[[0, 0], [C("about half"), 1]]),
    "cam": cam((0, 960, 540, 0.95), (C("about half"), 960, 560, 1.05, 1.4), (C("Everywhere you look"), 960, 540, 0.9, 1.4)), "drift": 1,
    "items": [words("≈ HALF: TAXES ON WORK AND PERSONAL INCOME", 960, 240, C("about half"), size=44, until=C("Everywhere you look")),
              words("THE SYSTEM LEANS ON THE PAYCHECK", 960, 240, C("Everywhere you look"), size=50),
              tag((0, "OUR CALC · OECD REVENUE STATISTICS 2025 (2023 DATA)"))]},
    sources=["oecd_rs25", "acctimes25"])
stage("s14_debt", "c2_debt", {
    **W1("txpipes", big=[[0, 1], [C("If the biggest tap"), 0.45]], thin=0.18, level=[[0, 0.5], [C("If the biggest tap"), 0.25]], tankLabel="SPENDS MORE THAN IT COLLECTS"),
    "cam": cam((0, 960, 540, 0.9), (C("a story we told"), 960, 520, 1.0, 1.4), (C("If the biggest tap"), 700, 520, 1.1, 1.2)), "drift": 2,
    "items": [words("SEE: WHO ACTUALLY OWNS AMERICA'S $40 TRILLION IN DEBT?", 960, 200, C("a story we told"), size=36, until=C("Rosa doesn't need")),
              ROSA(1300, C("Rosa doesn't need"), y=1040, scale=0.9, face="worry", pose="stand"),
              words("SMALLER TAP, DEEPER HOLE", 960, 200, C("If the biggest tap"), size=56),
              tag((0, "FACT · CBO (FY2026 DEFICIT)"), (C("a story we told"), "LIBRARY · EP 59"))]},
    sources=["cbo_mbr26"])

# ====================================================================== CHAPTER 3: the idea fair
bumper("s15_b3", "c3_card", "CHAPTER THREE", "The idea fair", "One good reason. One catch.", ORANGE)
stage("s16_fair", "c3_fair", {
    **W1("txfair", shown=[[0, 0], [C("a whole fair of them"), 0], [C("a whole fair of them", 2.0), 4]]),
    "cam": cam((0, 960, 560, 0.85), (C("a whole fair of them"), 960, 540, 0.9, 1.6), (C("Stub gives her one rule"), 900, 600, 1.15, 1.2)), "drift": 3,
    "items": [ROSA([[0, -200], [1.8, 560]], 0.0, face="wow", pose="stand", faces=[[0, "happy"], [C("a whole fair of them"), "wow"]]),
              STUB([[0, -400], [2.0, 780]], 0.0, face="happy", hops=[C("Stub gives her one rule", 0.4)]),
              bub("ONE GOOD REASON. ONE CATCH.", 820, 320, C("Stub gives her one rule"), tail=[800, 600]),
              tag((0, "STORY · PROPOSALS IN THE PUBLIC DEBATE"))]})
stage("s17_robot", "c3_robot", {
    **W1("txfair", lit=[[0, 0]]),
    "cam": cam((0, 700, 560, 1.0), (C("Tax the robots"), 420, 540, 1.2, 1.2), (C("The idea got famous"), 700, 520, 1.0, 1.4), (C("Rivet takes one step"), 900, 600, 1.15, 1.0)), "drift": 2,
    "items": [words("2017: BILL GATES: TAX A ROBOT 'AT A SIMILAR LEVEL' TO A WORKER", 900, 200, C("The idea got famous"), size=36),
              ROSA(700, 0.0, face="squint", pose="stand"),
              RIV([[0, 980], [C("Rivet takes one step"), 980], [C("Rivet takes one step", 0.6), 1180]], 0.0, face="happy", faces=[[0, "happy"], [C("Rivet takes one step"), "worry"]]),
              tag((0, "PROPOSAL"), (C("The idea got famous"), "QUOTE · QUARTZ INTERVIEW (FEB 2017)"))]},
    sources=["gates_qz17"])
stage("s18_korea", "c3_korea", {
    **W1("txware", robots=[[0, 2], [C("buy automation machines"), 3]], sign=[[0, "SOUTH KOREA, 2017"], [C("trimmed a tax break"), "TAX BREAK FOR ROBOTS: TRIMMED"]]),
    "cam": cam((0, 1000, 540, 0.9), (C("It didn't put a tax"), 1000, 520, 1.05, 1.4), (C("trimmed a tax break"), 1100, 480, 1.0, 1.2), (C("Headlines called it"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("NOT A TAX ON ROBOTS…", 960, 220, C("It didn't put a tax"), size=56, until=C("trimmed a tax break")),
              words("NICKNAME: 'THE FIRST ROBOT TAX'", 960, 220, C("Headlines called it"), size=54),
              RIV(1500, 0.0, face="wow", carry="box"),
              tag((0, "FACT · KOREA TAX REVISION PLAN (AUG 2017)"))]},
    sources=["korea17", "itif26"])


def scale(id_, seg, title, pro, con, catch_face="worry", extra=(), sources=()):
    stage(id_, seg, {
        **W1("txscale", title=title, pro=[[0, ""], [C("The good reason"), pro]], con=[[0, ""], [C("The catch"), con]],
             tilt=[[0, 0], [C("The good reason"), 0], [C("The good reason", 0.8), -0.7], [C("The catch"), -0.7], [C("The catch", 0.8), 0.6]]),
        "cam": cam((0, 960, 540, 0.95), (C("The good reason"), 760, 520, 1.05, 1.2), (C("The catch"), 1160, 520, 1.05, 1.2)), "drift": 1,
        "items": [STUB(200, 0.0, y=1040, scale=0.6, face="happy", faces=[[0, "happy"], [C("The catch"), catch_face]], hops=[C("The good reason", 0.3)]), *extra,
                  tag((0, "PROPOSAL · ONE REASON, ONE CATCH"))]}, sources=sources,
        sfx=[{"kind": "whoosh", "cue": "The good reason", "gain": 0.25}, {"kind": "hit", "cue": "The catch", "gain": 0.25}])


scale("s19_robot_scale", "c3_robot_scale", "BOOTH 1: TAX THE ROBOTS", "MONEY KEEPS COMING IN; WORKERS GET TIME", "WHAT COUNTS AS A ROBOT? FIRMS MAY BUY FEWER",
      extra=(RIV(1740, 0.0, y=1040, scale=0.6, face="happy", faces=[[0, "happy"], [C("What exactly counts"), "wow"], [C("Europe's lawmakers"), "happy"]]),
             words("2017: EUROPEAN PARLIAMENT SAYS NO", 960, 1000, C("Europe's lawmakers"), size=44)), sources=["gates_qz17", "itif26"])
stage("s20_profit", "c3_profit", {
    **W1("txfair", lit=[[0, 1]]),
    "cam": cam((0, 700, 560, 1.0), (C("Tax the owners"), 700, 540, 1.2, 1.2), (C("In Who Gets Rich"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("TAX PROFITS AND SHAREHOLDER GAINS A LITTLE MORE", 960, 200, C("If robots make companies"), size=42, until=C("In Who Gets Rich")),
              words("SEE: WHO GETS RICH WHEN ROBOTS DO THE WORK?", 960, 200, C("In Who Gets Rich"), size=42),
              ROSA(1000, 0.0, face="squint", pose="stand"),
              tag((0, "PROPOSAL"), (C("In Who Gets Rich"), "LIBRARY · EP 64"))]})
scale("s21_profit_scale", "c3_profit_scale", "BOOTH 2: TAX THE OWNERS", "IT FOLLOWS THE MONEY TO THE OWNERS", "PROFITS CAN MOVE TO LOW-TAX COUNTRIES", sources=["oecd_beps"])
stage("s22_shop", "c3_shop", {
    **W1("txfair", lit=[[0, 2]]),
    "cam": cam((0, 1140, 560, 1.0), (C("Tax the shopping"), 1140, 540, 1.2, 1.2), (C("Most rich countries"), 1000, 540, 0.95, 1.4), (C("America is the only one"), 1100, 560, 1.1, 1.2)), "drift": 2,
    "items": [words("ROBOTS DON'T EARN. SHOPPERS STILL BUY.", 960, 200, C("Robots don't earn"), size=48, until=C("Most rich countries")),
              words("MOST RICH COUNTRIES: A NATIONAL SALES TAX (VAT)", 960, 200, C("Most rich countries"), size=42, until=C("America is the only one")),
              words("USA: NO NATIONAL VAT", 960, 200, C("America is the only one"), size=60),
              ROSA(700, 0.0, face="happy", pose="stand", hold="bag", faces=[[0, "happy"], [C("America is the only one"), "wow"]]),
              tag((0, "PROPOSAL"), (C("Most rich countries"), "FACT · OECD"))]},
    sources=["oecd_vat", "acctimes25"])
scale("s23_shop_scale", "c3_shop_scale", "BOOTH 3: TAX THE SHOPPING", "HARD TO DODGE: EVERY BUYER PAYS", "IT BITES HARDER INTO TIGHT BUDGETS", sources=["cbo_vat"])
board("p24_draw", "c3_draw", "Who carries the bill?", "Let me draw what all three booths", [
    S(rect(1020, 330, 260, 110), "risk", C("the tax bill sits"), width=6, fill="risk", fillOpacity=0.35, kind="bar", label=lbl("THE BILL", 1150, 398, 34, "ink")),
    S("M 1150 460 L 1150 600 M 1100 520 L 1200 520 M 1150 600 L 1110 700 M 1150 600 L 1190 700", "ink", C("mostly on workers"), width=6, label=lbl("WORKERS (TODAY)", 1150, 750, 26, "ink")),
    S("M 620 600 L 620 760 M 570 650 L 670 650", "accent", C("A robot tax"), width=6, label=lbl("MACHINE BUYERS", 620, 800, 24, "accent")),
    S("M 880 640 L 880 790 M 830 690 L 930 690", "accent3", C("A profit tax"), width=6, label=lbl("OWNERS", 880, 830, 24, "accent3")),
    S("M 1460 640 L 1460 790 M 1410 690 L 1510 690", "accent2", C("A shopping tax"), width=6, label=lbl("SHOPPERS", 1460, 830, 24, "accent2")),
    S(arrow((1020, 400), (660, 560), 0.2), "accent", C("A robot tax"), width=4, kind="arrow"),
    S(arrow((1060, 440), (900, 600), 0.1), "accent3", C("A profit tax"), width=4, kind="arrow"),
    S(arrow((1280, 400), (1450, 600), -0.2), "accent2", C("A shopping tax"), width=4, kind="arrow"),
    S(rect(700, 880, 900, 80), "ink", C("Nobody makes the bill disappear"), width=5, kind="box", label=lbl("THE BILL NEVER DISAPPEARS. IT MOVES.", 1150, 932, 32, "ink")),
    S(dot(1150, 1010), "muted", C("Let me draw what all three booths"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NO FIGURES)", 1150, 1010, 16, "muted")),
], [{"kind": "point", "at": C("mostly on workers", 0.3), "dur": 1.4, "target": [1150, 560]}, {"kind": "point", "at": C("A shopping tax", 0.4), "dur": 1.2, "target": [1460, 700]},
    {"kind": "react", "at": C("whose shoulders")}], enter_left=False)

# ====================================================================== CHAPTER 4: send everyone a check?
bumper("s25_b4", "c4_card", "CHAPTER FOUR", "Send everyone a check?", "Dividends and basic income", GREEN)
stage("s26_dividend", "c4_dividend", {
    **W1("txfair", lit=[[0, 3]]),
    "cam": cam((0, 1580, 560, 1.0), (C("It isn't a new tax"), 1580, 540, 1.2, 1.2), (C("The idea is simple"), 1300, 540, 0.95, 1.4)), "drift": 2,
    "items": [words("NOT A TAX: A DIVIDEND", 1300, 200, C("It isn't a new tax"), size=60, until=C("The idea is simple")),
              words("A SLICE OF AI'S WEALTH FOR EVERY CITIZEN", 1200, 200, C("The idea is simple"), size=46),
              ROSA(1100, 0.0, face="wow", pose="stand"), STUB(1300, 0.0, face="wow", hops=[C("It's a dividend", 0.2)]),
              tag((0, "PROPOSAL"))]})
stage("s27_alaska", "c4_alaska", {
    **W1("txalaska", checks=[[0, 0], [C("Every year, Alaska sends"), 0], [C("Every year, Alaska sends", 1.6), 1]], swap=C("Could a country build")),
    "cam": cam((0, 960, 540, 0.9), (C("Every year, Alaska sends"), 1100, 520, 0.95, 1.4), (C("We told that story"), 960, 540, 0.9, 1.4), (C("Could a country build"), 520, 480, 1.15, 1.2)), "drift": 3,
    "items": [words("A YEARLY CHECK FROM AN OIL FUND", 1100, 200, C("Every year, Alaska sends"), size=52, until=C("We told that story")),
              words("SEE: ALASKA: THE STATE THAT PAYS YOU TO LIVE THERE", 1000, 200, C("We told that story"), size=38, until=C("Could a country build")),
              words("A FUND MADE OF ROBOTS?", 900, 200, C("Could a country build"), size=60),
              ROSA(300, C("Rosa wonders"), face="squint", pose="stand", faces=[[0, "squint"], [C("Could a country build"), "wow"]]),
              tag((0, "FACT · ALASKA PFD DIVISION"), (C("We told that story"), "LIBRARY · EP 48"))]},
    sources=["pfd_div"])
scale("s28_div_scale", "c4_div_scale", "BOOTH 4: AN AI DIVIDEND", "EVERYONE SHARES IN THE GAINS", "FIRST YOU MUST OWN OR TAX THE ROBOTS", sources=["pfd_div"])
stage("s29_ubi", "c4_ubi", {
    **W1("txmail", env=0, plaque="BASIC INCOME: CASH, NO STRINGS"),
    "cam": cam((0, 960, 540, 0.9), (C("has anyone actually tried"), 800, 560, 1.15, 1.2), (C("the results surprised"), 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [ROSA(800, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("the results surprised"), "wow"]]),
              bub("HAS ANYONE TRIED IT?", 800, 300, C("has anyone actually tried"), until=C("the results surprised"), tail=[800, 560]),
              words("YES. AND IT SURPRISED BOTH SIDES.", 960, 200, C("the results surprised"), size=50),
              tag((0, "PROPOSAL"))]})
stage("s30_stockton", "c4_stockton", {
    **W1("txmail", variant="valley", env=[[0, 0], [C("a small group of residents"), 0], [C("no strings attached"), 6]], cal=[[0, "STOCKTON, CA · 2019"]]),
    "cam": cam((0, 960, 540, 0.9), (C("a small group of residents"), 700, 540, 1.1, 1.6), (C("Plenty of critics"), 1100, 540, 1.0, 1.2), (C("Instead, after a year"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("$500 A MONTH. NO STRINGS.", 900, 220, C("a small group of residents"), size=60, until=C("Plenty of critics")),
              words("CRITICS: 'THEY'LL STOP WORKING'", 960, 220, C("Plenty of critics"), size=52, until=C("Instead, after a year")),
              words("YEAR 1: MORE IN FULL-TIME JOBS THAN THE COMPARISON GROUP", 960, 220, C("Instead, after a year"), size=38),
              LOCAL(1500, C("Instead, after a year"), v=5, color=TEAL, face="grin", pose="cheer"),
              tag((0, "FACT · SEED (2019-21)"), (C("Instead, after a year"), "FINDING · SEED YEAR 1 (PRELIMINARY)"))]},
    sources=["seed21"], sfx=[{"kind": "hit", "cue": "Instead, after a year", "gain": 0.25}])
stage("s31_or", "c4_or", {
    **W1("txmail", variant="city", env=[[0, 0], [C("a thousand dollars a month"), 6]], cal=[[0, "A 3-YEAR STUDY"]]),
    "cam": cam((0, 960, 540, 0.9), (C("a thousand dollars a month"), 700, 540, 1.1, 1.6), (C("compared them"), 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [words("BIGGER TEST: RANDOMIZED", 960, 220, C("carefully controlled"), size=56, until=C("a thousand dollars a month")),
              words("$1,000 A MONTH vs. ALMOST NOTHING", 960, 220, C("a thousand dollars a month"), size=52),
              tag((0, "FACT · OPENRESEARCH / NBER w32719"))]},
    sources=["or_nber"])
stage("s32_or2", "c4_or2", {
    **W1("txmail", variant="city", env=6),
    "cam": cam((0, 960, 540, 0.95), (C("people worked a little less"), 800, 560, 1.1, 1.2), (C("They spent more"), 1200, 540, 1.0, 1.4), (C("So, a cushion"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("WORKED ≈ 1-2 HOURS LESS A WEEK", 960, 220, C("people worked a little less"), size=54, until=C("They spent more")),
              words("MORE CHOICES. NO BETTER JOBS.", 960, 220, C("They spent more"), size=54, until=C("So, a cushion")),
              words("A CUSHION, NOT A CURE", 960, 220, C("So, a cushion"), size=66),
              LOCAL(700, 0.0, v=4, color=PURPLE, face="happy", pose="stand", hold="coffee"), LOCAL(1250, 0.3, v=10, color=ORANGE, face="squint", pose="stand"),
              tag((0, "FINDING · NBER w32719 (REV. 2025)"))]},
    sources=["or_nber"])
scale("s33_ubi_scale", "c4_ubi_scale", "BASIC INCOME FOR EVERYONE", "A FLOOR NOBODY FALLS THROUGH", "VERY EXPENSIVE: IT STILL NEEDS A TAX")

# ====================================================================== CHAPTER 5: so who pays?
bumper("s34_b5", "c5_card", "CHAPTER FIVE", "So who pays?", "The bill has to land somewhere", PURPLE)
board("p35_draw", "c5_draw", "The whole puzzle on one page", "Let me draw the whole puzzle", [
    S(rect(540, 340, 380, 560), "ink", C("the things we'll still need"), width=6, kind="box", label=lbl("WHAT WE STILL NEED", 730, 320, 28, "ink")),
    S(rect(570, 400, 320, 90), "accent", C("Schools"), width=4, fill="accent", fillOpacity=0.4, kind="bar", label=lbl("SCHOOLS", 730, 456, 28, "ink")),
    S(rect(570, 520, 320, 90), "muted", C("roads"), width=4, fill="muted", fillOpacity=0.3, kind="bar", label=lbl("ROADS", 730, 576, 28, "ink")),
    S(rect(570, 640, 320, 90), "accent3", C("checks for retirees"), width=4, fill="accent3", fillOpacity=0.4, kind="bar", label=lbl("RETIREES' CHECKS", 730, 696, 26, "ink")),
    S(rect(1380, 340, 380, 560), "ink", C("the places where AI's wealth"), width=6, kind="box", label=lbl("WHERE AI'S WEALTH PILES UP", 1570, 320, 26, "ink")),
    S(rect(1410, 400, 320, 90), "accent3", C("Profits"), width=4, fill="accent3", fillOpacity=0.3, kind="bar", label=lbl("PROFITS", 1570, 456, 28, "ink")),
    S(rect(1410, 520, 320, 90), "accent2", C("shopping"), width=4, fill="accent2", fillOpacity=0.3, kind="bar", label=lbl("SHOPPING", 1570, 576, 28, "ink")),
    S(rect(1410, 640, 320, 90), "accent", C("the robots themselves"), width=4, fill="accent", fillOpacity=0.3, kind="bar", label=lbl("THE ROBOTS", 1570, 696, 28, "ink")),
    S("M 1400 450 Q 1150 400 910 450 M 1400 570 Q 1150 520 910 570 M 1400 690 Q 1150 640 910 690", "accent2", C("a different pipe"), width=7, label=lbl("PIPES = PROPOSALS", 1150, 780, 28, "accent2")),
    S(rect(900, 830, 500, 70), "risk", C("who's standing under it"), width=6, kind="box", label=lbl("WHICH PIPE? WHO'S UNDER IT?", 1150, 878, 28, "risk")),
    S(dot(1150, 990), "muted", C("Let me draw the whole puzzle"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NO FIGURES)", 1150, 990, 16, "muted")),
], [{"kind": "point", "at": C("a different pipe", 0.3), "dur": 1.4, "target": [1150, 520]}, {"kind": "react", "at": C("who's standing under it")}])
stage("s36_verdict", "c5_verdict", {
    **W1("txpipes", big=[[0, 1], [C("If work shrinks"), 0.45]], thin=[[0, 0.18], [C("to profits"), 0.3]], level=0.6,
         extra=[{"label": "SHOPPING", "at": C("to shopping"), "c": PINK}, {"label": "ROBOT OWNERS", "at": C("to the owners of the robots"), "c": ORANGE},
                {"label": "A MIX?", "at": C("or to some mix"), "c": PURPLE}]),
    "cam": cam((0, 960, 540, 0.9), (C("nobody has decided yet"), 960, 520, 1.0, 1.2), (C("If work shrinks"), 700, 600, 1.0, 1.4), (C("And in the end"), 960, 540, 0.88, 1.6)), "drift": 2,
    "items": [words("NOBODY HAS DECIDED YET", 960, 200, C("nobody has decided yet"), size=60, until=C("If work shrinks")),
              words("THE BILL HAS TO MOVE", 960, 200, C("If work shrinks"), size=60, until=C("And in the end")),
              words("THE REAL CHOICE: WHO CARRIES THE BILL", 960, 200, C("And in the end"), size=50),
              tag((0, "VERDICT · OUR ANALYSIS (NO SIDE TAKEN)"))]})
stage("s37_clock", "c5_clock", {
    **W1("txclock", inflow=1, level=[[0, 0.5], [C("run dry in 2034"), 0.08]], year=[[0, "2034"]]),
    "cam": cam((0, 1300, 520, 0.95), (C("run dry in 2034"), 1500, 480, 1.1, 1.2), (C("So this debate"), 960, 540, 0.88, 1.6)), "drift": 2,
    "items": [words("TICK, TOCK: 2034", 1300, 220, C("run dry in 2034"), size=60, until=C("So this debate")),
              words("THE DEBATE MAY ARRIVE BEFORE THE ROBOTS DO", 960, 220, C("So this debate"), size=46),
              RIV(1000, C("long before robots"), y=1000, scale=0.6, face="wow"),
              tag((0, "PROJECTION · TRUSTEES 2026"))]},
    sources=["ssa_tr26"])
stage("s38_rosa", "c5_rosa", {
    **W1("txmeeting", list=["SCHOOLS, ROADS, RETIREES", "ROBOT TAX?", "TAX THE OWNERS?", "TAX THE SHOPPING?", "A ROBOT DIVIDEND?"],
         shown=[[0, 0], [C("Here's what we'll still need"), 1], [C("And here's who could pay"), 1], [C("And here's who could pay", 2.0), 5]], hands=C("Let's decide together", 0.5)),
    "cam": cam((0, 960, 560, 0.9), (C("Here's what we'll still need"), 1100, 520, 1.05, 1.2), (C("Rivet raises a hand"), 900, 560, 1.1, 1.2), (C("But you might get a bill"), 760, 560, 1.2, 1.0)), "drift": 2,
    "items": [ROSA(560, 0.0, y=600, face="happy", pose="talk", faces=[[0, "happy"], [C("Do I get a vote"), "squint"], [C("But you might get a bill"), "grin"]]),
              STUB(820, 0.0, y=600, scale=0.6, face="happy"),
              RIV(980, 0.0, y=860, scale=0.7, face="happy", hand=C("Rivet raises a hand"), faces=[[0, "happy"], [C("But you might get a bill"), "wow"]]),
              bub("DO I GET A VOTE?", 1000, 340, C("Do I get a vote"), until=C("Not yet, says Rosa"), tail=[980, 560]),
              bub("NOT YET. BUT YOU MIGHT GET A BILL.", 640, 260, C("Not yet, says Rosa"), tail=[600, 380], size=28),
              tag((0, "STORY"))]},
    sfx=[{"kind": "hit", "cue": "But you might get a bill", "gain": 0.3}])
add("s39_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s40_button", "button", {
    **W1("txtown", banner=[[0, "PINEWICK TOWN MEETING: TONIGHT"]]),
    "cam": cam((0, 960, 600, 1.1), (3.0, 1100, 600, 1.2, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [RIV(1000, 0.0, face="worry", pockets=0.8),
              bub("A BILL? I DON'T EVEN HAVE POCKETS.", 1000, 300, 0.5, until=3.4, tail=[1000, 480], size=28),
              STUB([[0, 2300], [2.4, 1300]], 1.4, face="happy", hops=[3.6]),
              bub("RELAX. YOU'D JUST NEED A PAYCHECK.", 1300, 360, 3.5, tail=[1300, 600], size=28)]},
    sfx=[{"kind": "hit", "at": 3.5, "gain": 0.3}])

TIGHT = {"txscale", "txjars", "txmeeting"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "PROJECTION": "gold", "SCENARIO": "gold", "OUR": "gold", "ESTIMATE": "gold", "FINDING": "green", "QUOTE": "green"}
for _sc in cartoon_kit.scenes:
    if _sc["type"] != "engine_cartoon":
        continue
    P = _sc["params"]
    for _k in P.get("cam", []):
        _k["zoom"] = min(_k["zoom"], 1.25)
        _k["y"] = max(380, min(620, _k["y"]))
    keep, calls = [], P.setdefault("callouts", [])
    for _it in P.get("items", []):
        if _it.get("kind") == "pmtag":
            tl = _it["tags"]
            for j, (t0, txt) in enumerate(tl):
                c = {"text": txt, "x": 40 + (len(txt) * 20 * 0.6 + 60) / 2, "y": 50, "at": t0, "size": 20, "screen": True, "color": TAGCOL.get(txt.split(" ")[0], "white")}
                if j + 1 < len(tl):
                    c["until"] = tl[j + 1][0]
                calls.append(c)
            continue
        if _it.get("kind") == "toonwords":
            _it["size"] = min(_it.get("size", 56), int(1250 / (0.75 * max(1, len(_it["text"])))))
        if _it.get("kind") in ("toonwords", "sign", "bubble") and isinstance(_it.get("y"), (int, float)) and _it["y"] < 200:
            _it["y"] = 200
        keep.append(_it)
    P["items"] = keep

write(OUT, "# GENERATED by tools/gen_aitaxes_storyboard.py; edit the generator, not this file.\n"
           "# Episode 69 storyboard (If AI Replaces Workers, Who Pays the Taxes?): bespoke worlds in CartoonStage/aitaxes.tsx.\n")

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
segs = {s.id for s in scr.segments}
missing = segs - {sc["segment"] for sc in cartoon_kit.scenes}
print("cue problems:", bad if bad else "none", "| segments without scenes:", sorted(missing) or "none")
