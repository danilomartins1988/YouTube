"""Generates projects/could-ai-end-chinas-manufacturing-dominance/deliverables/documentary/storyboard.yaml
(Episode 62, arc Episode 2: Could AI Make American Factories Cheaper Than China's?).

OWNER DIRECTION: prime-time TV cartoon energy (retro-futurist sci-fi comedy at GENRE level only; everything original), human
characters, day scenes. Continuity with Ep 60 (arc Episode 1): the same fictional cast MEL, WEI and KIP, Mel's toaster as the
$100 product, the Ep 60 megafloor once as "the old formula". New, distinctive sets in CartoonStage/automation.tsx: ohiobot
(us / cn variants), billbox, toastlab, robotrace, chainweb, moneyriver, aititle, aibumper; items torq (running gag: the robot
who wants legs), humanoid (prototype on a test stand), pricemeter (illustrative, no numbers).
Signature animations: A the hypothetical Ohio plant (s01), B the cost box / pulling labor out (s15, p16), C the three-factory
lab with knobs that flip the winner (s19-s23, p24), D the robot race (s27) and the density twist (p29), E the supply web (s32),
F the money river and the value chain the presenter draws (p34, s35).
Presenter boards: p04 output vs jobs, p13 proven/growing/not yet, p16 pull labor out, p24 who wins when, p29 density, p34 chain.
Run: python tools/gen_aimfg_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/could-ai-end-chinas-manufacturing-dominance/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
TEAL, ORANGE, RED, GREEN, PURPLE, CY, NAVY = "#1F7A8C", "#FF9F1C", "#E5484D", "#2E9E5B", "#7E57C2", "#00A6C8", "#12203A"
ILL = "ILLUSTRATIVE MODEL · OUR ASSUMPTIONS"


def toon(x, at=0.0, **kw):
    return it("toon", x=x, at=at, **kw)


def MEL(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=2, skin=2, hair=0, hairStyle=3, color="#FF8A65", glasses=False, scarf="#FFD23F", **kw)


def WEI(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=1, skin=0, hair=1, hairStyle=4, color=TEAL, glasses=True, scarf="#FFFFFF", **kw)


def KIP(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.3)
    return toon(x, at, who="shopper", v=3, skin=4, hair=3, hairStyle=2, color="#5C6BC0", glasses=False, scarf=RED, **kw)


def TORQ(x, at=0.0, **kw):
    kw.setdefault("scale", 0.9)
    return it("torq", x=x, at=at, **kw)


def sign(text, x, y, at, **kw):
    return it("sign", text=text, x=x, y=y, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    return it("toonwords", text=text, x=x, y=y, at=at, **kw)


def bumper(id_, seg, num, act, title, caption, color, torq_face="happy"):
    stage(id_, seg, {**W1("aibumper", num=num, act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "sitcom",
                     "min_seconds": 4.0, "items": [TORQ([[0, -300], [0.9, 560]], 0.3, y=1010, scale=0.75, stampAt=1.0, face=torq_face, faces=[[0, torq_face], [1.05, "smug"]])]},
          sfx=[{"kind": "whoosh", "at": 0.05, "gain": 0.25}, {"kind": "hit", "at": 1.05, "gain": 0.3}])


# cost model blocks (ILLUSTRATIVE): label -> colour
MAT, LAB, MAC, ENG, UPK, DEF, SHP, TAR = "#1F7A8C", "#FF9F1C", "#7E57C2", "#F2C14E", "#26A69A", "#E57373", "#5C6BC0", "#E5484D"


def blocks(*rows):
    out = []
    for r in rows:
        b = {"label": r[0], "v": r[1], "color": r[2]}
        if len(r) > 3 and r[3] is not None:
            b["at"] = r[3]
        out.append(b)
    return out


F1 = lambda tar=9, at=None: blocks(("MATERIALS", 61, MAT, at), ("LABOR", 11, LAB, at), ("MACHINES", 5, MAC, at), ("ENERGY", 3, ENG, at), ("UPKEEP", 2, UPK, at),
                                   ("DEFECTS", 3, DEF, at), ("SHIPPING", 6, SHP, at), ("TARIFF", tar, TAR, at))
F2 = lambda mac=14, at=None: blocks(("MATERIALS", 64, MAT, at), ("LABOR", 13, LAB, at), ("MACHINES", mac, MAC, at), ("ENERGY", 3, ENG, at), ("UPKEEP", 4, UPK, at),
                                    ("DEFECTS", 2, DEF, at), ("SHIPPING", 2, SHP, at))
F3 = lambda tar=8, at=None: blocks(("MATERIALS", 59, MAT, at), ("LABOR", 3, LAB, at), ("MACHINES", 11, MAC, at), ("ENERGY", 3, ENG, at), ("UPKEEP", 3, UPK, at),
                                   ("DEFECTS", 2, DEF, at), ("SHIPPING", 6, SHP, at), ("TARIFF", tar, TAR, at))
COL1 = lambda b, at=0.0: {"name": "1 · CHINA, CONVENTIONAL", "sub": "TODAY'S WAY", "at": at, "color": RED, "blocks": b}
COL2 = lambda b, at=0.0: {"name": "2 · OHIO, AUTOMATED", "sub": "HYPOTHETICAL", "at": at, "color": CY, "blocks": b}
COL3 = lambda b, at=0.0: {"name": "3 · CHINA, AUTOMATED", "sub": "HYPOTHETICAL", "at": at, "color": GREEN, "blocks": b}
KNOBS = lambda tar=10, busy=100, at=0.0: [{"label": "TARIFF", "v": tar, "at": at, "max": 30, "show": [[0, "SOME"]]}, {"label": "ROBOTS BUSY", "v": busy, "at": at, "show": [[0, "ALWAYS"]]}]

# ====================================================================== ACT 1: the factory that changes everything (hook)
stage("s01_hook", "co_hook", {
    **W1("ohiobot", variant="us", hyp=True, hypAt=0, hypX=960, hypY=70, arms=5, armX=-200, armGap=520, scanX=1560, schedX=1250,
         hiAt=[[0, None], [C("Cameras checking"), "vision"], [C("Software deciding"), "sched"], [C("And a price"), None]]),
    "cam": cam((0, 700, 560, 1.15), (C("Robot arms working"), 900, 520, 1.0, 1.4), (C("Cameras checking"), 1500, 480, 1.25, 1.0),
               (C("Software deciding"), 1250, 300, 1.25, 1.0), (C("And a price"), 960, 520, 0.9, 1.4), (C("That factory doesn't exist"), 960, 500, 1.0, WHIP),
               (C("So could"), 960, 460, 0.85, 1.4)), "drift": 4,
    "items": [words("MEL'S DREAM: A TOASTER FACTORY IN OHIO", 760, 200, C("Picture her factory"), until=C("Robot arms working"), size=50),
              MEL([[0, 300], [C("So now she wants"), 600]], 0.1, label="MEL · FROM EPISODE 1", labelUntil=C("Picture her factory"), faces=[[0, "worry"], [C("So now she wants"), "smug"], [C("That factory doesn't exist"), "shock"]], hold="phone", until=C("So could")),
              it("bubble", text="FINE. I'LL MAKE\nMY OWN TOASTER.", x=750, y=330, at=C("So now she wants"), until=C("Picture her factory", 0.5), tail=[620, 560], size=30),
              it("pricemeter", x=960, y=380, at=C("And a price"), until=C("That factory doesn't exist"), tilt=[[0, 0.6], [C("matches China's", 0.2), 0.0]], scale=0.75,
                 left="OHIO", right="CHINA"),
              TORQ([[C("That factory doesn't exist"), 2300], [C("But almost every piece", 0.4), 1250]], C("That factory doesn't exist"),
                   faces=[[0, "happy"], [C("But almost every piece"), "smug"]]),
              sign("EVERY PIECE EXISTS SOMEWHERE · THE WHOLE THING, NOT YET", 960, 200, C("But almost every piece"), color="#FFF59D", size=28, until=C("So could")),
              words("COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?", 960, 190, C("So could"), size=46, color="#FFFFFF"),
              MEL([[C("would America actually win"), -200], [C("would America actually win", 1.0), 420]], C("would America actually win", -0.2), face="shock", pose="armsup")]},
    sfx=[{"kind": "hit", "cue": "That factory doesn't exist", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("aititle", lines=["CHEAPER THAN", "CHINA?"], sub="COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?",
         subs=[[2.2, "Tonight: “The Robot Who Wanted Legs” · Part 2 of the factory story"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.4,
    "items": [TORQ(300, 2.4, y=1060, scale=0.8, legs=True, legsFallAt=4.4, faces=[[0, "happy"], [4.4, "shock"]]), MEL(1700, 2.6, scale=1.1, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 4.5, "gain": 0.25}])
stage("s03_stakes", "a1_stakes", {
    **W1("ohiobot", variant="cn", arms=3, armX=200, armGap=700, scanX=2000, schedX=2400, carts=2, idle=[[0, 1.0], [C("But a robot"), 1.0], [C("If machines do more"), 0.0]]),
    "cam": cam((0, 900, 520, 0.95), (C("But a robot"), 1000, 520, 1.15, WHIP), (C("If machines do more"), 1100, 500, 0.95, 1.4), (C("And the stakes"), 1100, 480, 0.9, 1.2)), "drift": 4,
    "items": [words("THE OLD RULE: BUILD WHERE WORK IS CHEAPEST", 960, 160, 0.3, until=C("But a robot"), size=52),
              toon(450, 0.2, who="shopper", v=0, color="#455A64", scale=1.3, pose="clipboard", hold="clipboard", face="smug", label="MEL'S BANKER", labelUntil=C("But a robot"), faces=[[0, "smug"], [C("starts to wobble"), "worry"]], takes=[C("starts to wobble")]),
              MEL(1500, 0.2, face="happy", pose="point", faces=[[0, "worry"], [C("doesn't care about wages"), "grin"]]),
              TORQ([[C("But a robot"), -300], [C("But a robot", 1.2), 900]], C("But a robot", -0.3), faces=[[0, "happy"], [C("doesn't care"), "smug"]]),
              it("bubble", text="WAGES?\nNEVER HEARD OF 'EM.", x=1120, y=300, at=C("doesn't care about wages"), until=C("If machines do more", 0.6), tail=[960, 560], size=28),
              words("THE OLD RULE WOBBLES", 1100, 160, C("starts to wobble"), size=56, until=C("And the stakes")),
              sign("PRICES", 700, 180, C("Prices"), color="#FFE0B2", size=34), sign("JOBS", 1100, 260, C("jobs, and which"), color="#C8E6C9", size=34),
              sign("WHO MAKES WHAT EVERYONE NEEDS", 1500, 180, C("which country"), color="#BBDEFB", size=34)]})
add("p04_output", "a1_output", "engine_draw", {
    "title": "U.S. factories: output vs jobs since June 1979", "board": BOARD, "draw_start": C("And America has already"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("And America has already")},
        {"d": "M 700 820 L 700 667 L 840 667 L 840 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Today, American factories"), "label": lbl("OUTPUT, LATE '70s", 770, 650, 20, "accent2")},
        {"d": "M 860 820 L 860 500 L 1000 500 L 1000 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.75, "kind": "bar", "start": C("about twice as much"), "label": lbl("TODAY: ×2", 930, 482, 26, "accent2")},
        {"d": "M 1120 820 L 1120 508 L 1260 508 L 1260 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("with millions fewer"), "label": lbl("JOBS, LATE '70s", 1190, 490, 20, "risk")},
        {"d": "M 1280 820 L 1280 617 L 1420 617 L 1420 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.75, "kind": "bar", "start": C("with millions fewer", 0.8), "label": lbl("TODAY: ⅓ FEWER", 1350, 600, 24, "risk")},
        {"d": arrow((930, 440), (1340, 560), -0.2), "color": "accent", "width": 5, "kind": "arrow", "start": C("More stuff"), "label": lbl("MORE STUFF, FEWER PEOPLE", 1130, 420, 24, "accent")},
        {"d": dot(1050, 875), "color": "muted", "width": 1, "start": C("Automation is"), "label": lbl("FED G.17 OUTPUT INDEX · BLS JOBS · JUNE 1979 VS OCT 2026 · OUR CALCULATION", 1050, 875, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("More stuff", 0.2), "dur": 1.4, "target": [1350, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["fred_ipman", "fred_manemp"])

# ====================================================================== ACT 2: the old formula (brief: Episode 1 recap)
bumper("s05_b2", "a2_card", "2", "ACT TWO", "THE OLD FORMULA", "Previously, on The Hidden Economics...", ORANGE)
stage("s06_formula", "a2_formula", {
    **W1("megafloor", board="EPISODE 1: THE EVERYTHING FACTORY", boardX=1000),
    "cam": cam((0, 1000, 480, 1.05), (C("Wei's answer"), 1050, 520, 0.95, 1.4), (C("with suppliers"), 1200, 520, 1.0, 1.2)), "drift": 5,
    "items": [sign("EPISODE 1: “WHY THE WORLD STILL DEPENDS ON CHINESE FACTORIES”", 1000, 120, C("from our last episode"), color="#FFFFFF", size=28, until=C("Wei's answer")),
              words("ABOUT 1 IN 4 OF EVERYTHING MANUFACTURED", 1000, 120, C("China makes"), size=50, until=C("with suppliers")),
              sign("WORLD BANK DATA, 2025 · OUR CALCULATION", 1000, 220, C("of everything the world"), color="#FFF8E1", size=22, until=C("with suppliers")),
              sign("SUPPLIERS", 600, 140, C("suppliers down the street"), color="#C8E6C9", size=32), sign("PORTS", 980, 140, C("giant ports"), color="#BBDEFB", size=32),
              sign("POWER", 1340, 140, C("steady power"), color="#FFF59D", size=32), sign("ENGINEERS", 1700, 140, C("engineers who've"), color="#FFE0B2", size=32),
              WEI(1450, 0.3, pose="wave", face="happy", label="WEI · LINE ENGINEER (EPISODE 1)", labelUntil=C("Wei's answer"), poses=[[0, "wave"], [C("with suppliers"), "point"]]),
              MEL(300, 0.2, face="happy", pose="stand", hold="phone"),
              it("gizmo", x=600, y=760, at=0.4, scale=0.5, face="happy", parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]])]},
    sources=["wdi_mva"])
stage("s07_wage", "a2_wage", {
    **W1("megafloor", board="THE OLD FORMULA: PAY", boardX=-1400, hi=0),
    "cam": cam((0, 960, 540, 1.0), (C("five times"), 960, 500, 1.15, WHIP), (C("That gap"), 1000, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("≈ 5× THE PAY PER HOUR", 960, 170, C("five times"), size=70, color="#FFFFFF", until=C("That gap", 1.5)),
              sign("U.S. PRODUCTION WORKERS (BLS) VS LARGER CHINESE FIRMS (NBS), 2025 · ROUGH, OUR CALCULATION", 960, 300, C("five times", 0.4), color="#FFF8E1", size=20),
              it("gizmo", x=960, y=760, at=C("That gap"), scale=0.5, face="worry", parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]], stamp="MADE IN CHINA", stampAt=C("made in China", -0.2), stampY=60),
              MEL(450, 0.3, face="happy", pose="clipboard", hold="phone", faces=[[0, "happy"], [C("five times"), "shock"], [C("That gap"), "worry"]], takes=[C("five times", 0.2)]),
              WEI(1550, 0.3, face="happy", pose="stand", hold="clipboard")]},
    sources=["bls_ces", "nbs_wage", "fed_g5a"])
stage("s08_question", "a2_question", {
    **W1("megafloor", board="LABOR: CHINA'S OLDEST HEAD START", boardX=-1400, hi=None),
    "cam": cam((0, 900, 520, 1.0), (C("does China's oldest"), 1000, 500, 1.15, WHIP), (C("First, she needs"), 1300, 520, 0.95, 1.4)), "drift": 4,
    "items": [TORQ([[0, -300], [1.4, 800]], 0.0, faces=[[0, "happy"], [C("does China's oldest"), "smug"]]),
              it("homebox", x=[[0, 1000], [C("shrink the labor"), 1000], [C("does China's oldest"), 1000]], at=0.2, label="LABOR", face="worry", scale=1.0),
              words("ROBOTS SHRINK LABOR → HEAD START SHRINKS?", 960, 160, C("If robots shrink"), size=48, until=C("First, she needs")),
              words("WHAT CAN AI REALLY DO ON A FACTORY FLOOR?", 1300, 160, C("First, she needs"), size=48, color="#FFFFFF"),
              MEL(1600, 0.3, face="worry", pose="shrug", faces=[[0, "worry"], [C("First, she needs"), "smug"]])]})

# ====================================================================== ACT 3: when labor matters less
bumper("s09_b3", "a3_card", "3", "ACT THREE", "WHEN LABOR MATTERS LESS", "Results not typical. Robots shown are bolted down.", CY)
stage("s10_vision", "a3_vision", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1500, schedX=600, hi="vision"),
    "cam": cam((0, 1300, 520, 1.0), (C("Cameras running AI"), 1500, 470, 1.35, 1.4), (C("guide robot arms"), 1000, 500, 1.2, 1.2), (C("The International Federation"), 1200, 480, 0.95, 1.4)), "drift": 4,
    "items": [words("PROVEN #1: MACHINE VISION", 1300, 120, 0.3, until=C("The International Federation"), size=56),
              sign("✓ CHECKS EVERY PART", 1800, 260, C("faster than a human eye"), color="#C8E6C9", size=28),
              sign("✓ GUIDES THE GRIPPER", 900, 260, C("guide robot arms"), color="#BBDEFB", size=28),
              sign("“ESTABLISHED AND INDUSTRY-GRADE” · IFR WORLD ROBOTICS 2026", 1200, 140, C("calls machine vision"), color="#FFF59D", size=30),
              KIP(700, 0.2, face="smug", pose="point", label="KIP · MEL'S CONSULTANT", labelUntil=C("Cameras running AI")), MEL(1150, 0.3, face="happy", pose="stand", faces=[[0, "happy"], [C("guide robot arms"), "grin"]])]},
    sources=["ifr_wr26"])
stage("s11_maint", "a3_maint", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1700, schedX=1400, maintAt=C("Sensors listen"), maintX=600, schedAt=C("reshuffles the line"), carts=4,
         hiAt=[[0, "maint"], [C("Smart scheduling"), "sched"], [C("Self-driving carts"), "carts"], [C("The federation says"), None]]),
    "cam": cam((0, 600, 600, 1.3), (C("Smart scheduling"), 1400, 300, 1.2, 1.4), (C("Self-driving carts"), 1000, 760, 1.05, 1.4), (C("The federation says"), 1100, 520, 0.9, 1.4)), "drift": 4,
    "items": [words("PREDICTIVE MAINTENANCE", 600, 120, 0.3, until=C("Smart scheduling"), size=52),
              it("bubble", text="THAT MOTOR SOUNDS\nTIRED. FIX IT THURSDAY.", x=900, y=330, at=C("flags it"), until=C("Smart scheduling"), tail=[650, 700], size=26),
              words("SMART SCHEDULING", 1400, 600, C("Smart scheduling"), size=48, until=C("Self-driving carts")),
              words("SELF-DRIVING CARTS", 1000, 520, C("Self-driving carts"), size=48, until=C("The federation says")),
              sign("“INCREASINGLY USED IN INDUSTRY” · IFR 2026", 1100, 140, C("The federation says"), color="#FFF59D", size=30),
              MEL(1650, C("Smart scheduling"), face="happy", pose="point", hold="phone")]},
    sources=["ifr_wr26"])
stage("s12_twin", "a3_twin", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1700, schedX=-600, twinAt=C("a virtual copy"), twinX=900),
    "cam": cam((0, 900, 560, 1.0), (C("a virtual copy"), 900, 380, 0.9, 1.6), (C("Foxconn says"), 900, 420, 0.95, 1.2)), "drift": 4,
    "items": [words("DIGITAL TWINS", 960, 110, 0.3, until=C("a virtual copy"), size=60),
              sign("TEST THE LINE BEFORE YOU BUILD IT", 960, 120, C("where engineers test"), color="#C8E6C9", size=30, until=C("Foxconn says")),
              sign("FOXCONN: DIGITAL TWIN OF A NEW GUADALAJARA PLANT · ROBOTS TRAINED IN SIMULATION", 960, 120, C("Foxconn says"), color="#FFF59D", size=26,
                   sub="COMPANY STATEMENT · NVIDIA BLOG, JUN 2024 · A PLANNING TOOL, NOT A 'LIGHTS-OUT' FACTORY"),
              KIP(1700, 0.3, face="happy", pose="point", hold="phone", faces=[[0, "happy"], [C("a virtual copy"), "smug"]]), MEL(1200, 0.3, face="happy", faces=[[0, "happy"], [C("a virtual copy"), "shock"]], takes=[C("a virtual copy", 0.3)])]},
    sources=["nvidia_foxconn"])
add("p13_sort", "a3_draw", "engine_draw", {
    "title": "What AI can do on a factory floor (IFR, 2026)", "board": BOARD, "draw_start": C("Let me sort"), "speed": 1600, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(600, 400, 260, 380), "color": "accent3", "width": 6, "kind": "box", "start": C("Proven"), "label": lbl("PROVEN", 730, 440, 30, "accent3")},
        {"d": dot(730, 520), "color": "ink", "width": 1, "start": C("the robot arms"), "label": lbl("ROBOT ARMS", 730, 520, 22, "ink")},
        {"d": dot(730, 570), "color": "ink", "width": 1, "start": C("weld, paint and pick"), "label": lbl("WELD · PAINT · PICK", 730, 570, 18, "ink")},
        {"d": dot(730, 640), "color": "ink", "width": 1, "start": C("plus machine vision"), "label": lbl("MACHINE VISION", 730, 640, 22, "ink")},
        {"d": rect(900, 400, 260, 380), "color": "accent", "width": 6, "kind": "box", "start": C("Growing"), "label": lbl("GROWING", 1030, 440, 30, "accent")},
        {"d": dot(1030, 520), "color": "ink", "width": 1, "start": C("predictive maintenance,"), "label": lbl("PREDICTIVE", 1030, 520, 20, "ink")},
        {"d": dot(1030, 548), "color": "ink", "width": 1, "start": C("predictive maintenance,"), "label": lbl("MAINTENANCE", 1030, 548, 20, "ink")},
        {"d": dot(1030, 610), "color": "ink", "width": 1, "start": C("AI inspection"), "label": lbl("AI INSPECTION", 1030, 610, 20, "ink")},
        {"d": dot(1030, 670), "color": "ink", "width": 1, "start": C("smart scheduling"), "label": lbl("SCHEDULING", 1030, 670, 20, "ink")},
        {"d": rect(1200, 400, 260, 380), "color": "risk", "width": 6, "kind": "box", "start": C("Not yet"), "label": lbl("NOT YET", 1330, 440, 30, "risk")},
        {"d": dot(1330, 520), "color": "ink", "width": 1, "start": C("general-purpose robots"), "label": lbl("GENERAL-PURPOSE", 1330, 520, 20, "ink")},
        {"d": dot(1330, 548), "color": "ink", "width": 1, "start": C("general-purpose robots"), "label": lbl("ROBOTS", 1330, 548, 20, "ink")},
        {"d": dot(1330, 610), "color": "ink", "width": 1, "start": C("learn any job"), "label": lbl("LEARN BY WATCHING", 1330, 610, 18, "ink")},
        {"d": "M 1240 700 L 1420 760 M 1420 700 L 1240 760", "color": "risk", "width": 6, "start": C("isn't industry-grade")},
        {"d": dot(1030, 830), "color": "muted", "width": 1, "start": C("The federation says"), "label": lbl("SOURCE: IFR WORLD ROBOTICS 2026, TECHNOLOGY TRENDS", 1030, 830, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("isn't industry-grade", 0.1), "dur": 1.4, "target": [1330, 600]}],
    "scale": 0.86, "floor": 1040}, sources=["ifr_wr26"])
stage("s14_humanoid", "a3_humanoid", {
    **W1("ohiobot", variant="us", arms=3, armX=1400, armGap=420, scanX=2600, schedX=-800, carts=1),
    "cam": cam((0, 700, 540, 1.1), (C("The federation says"), 760, 520, 1.0, 1.2), (C("The robot that matters"), 1300, 520, 0.95, 1.4), (C("It's the arm"), 1600, 560, 1.2, WHIP)), "drift": 3,
    "items": [it("humanoid", x=560, at=0.1, dance=True, scale=0.8, wobbleAt=C("most are still prototypes"), fallAt=C("The robot that matters", -0.3)),
              words("VIRAL VIDEO ≠ FACTORY", 700, 110, 0.3, until=C("The federation says"), size=56),
              MEL(1700, 0.2, face="happy", pose="point", faces=[[0, "grin"], [C("most are still prototypes"), "worry"]]),
              sign("MOST HUMANOIDS: PROTOTYPES OR PILOTS (IFR 2026)", 760, 120, C("most are still prototypes"), color="#FFF59D", size=28, until=C("It's the arm")),
              sign("TODAY: INDUSTRIAL ROBOTS ARE THE BETTER DEAL (IFR)", 1300, 240, C("the better deal"), color="#C8E6C9", size=26),
              TORQ([[0, 1000], [C("The robot that matters"), 1000], [C("It's the arm"), 1200]], 0.2, legs=True, legsFallAt=C("isn't the one that dances"),
                   faces=[[0, "smug"], [C("isn't the one that dances"), "shock"], [C("It's the arm", 0.5), "happy"]]),
              words("THE ARM BOLTED TO THE FLOOR", 1600, 140, C("It's the arm"), size=54, color="#FFFFFF")]},
    sources=["ifr_wr26"], sfx=[{"kind": "hit", "cue": "isn't the one that dances", "gain": 0.3}])
stage("s15_bill", "a3_bill", {
    **W1("billbox", title="WHERE $1 OF U.S. FACTORY SALES WENT · 2021", slices=[[0.4, "MATERIALS & PARTS: THE BIGGEST BITE", 55, TEAL],
                                                                                 [C("go to wages"), "PAYROLL ≈ 13¢", 13, ORANGE],
                                                                                 [C("Materials and parts", -0.4), "EVERYTHING ELSE", 32, PURPLE]],
         note="CENSUS 2021 ANNUAL SURVEY OF MANUFACTURES · SHARES ARE OUR CALCULATION · PAYROLL = ALL EMPLOYEES, BEFORE BENEFITS", noteAt=C("In American factories")),
    "cam": cam((0, 960, 520, 1.05), (C("go to wages"), 960, 560, 1.15, 1.2), (C("Materials and parts"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [MEL(1500, 0.3, face="shock", pose="point", faces=[[0, "happy"], [C("go to wages"), "shock"]], takes=[C("go to wages", 0.5)]),
              it("bubble", text="THAT'S IT?!", x=1550, y=300, at=C("go to wages", 0.6), tail=[1500, 560], size=34),
              TORQ(380, 0.2, faces=[[0, "happy"], [C("go to wages"), "worry"]])]},
    sources=["census_asm21"])
add("p16_pull", "a3_pull", "engine_draw", {
    "title": "Pull labor out: what's left of $1 of factory sales", "board": BOARD, "draw_start": C("Watch what happens"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(800, 380, 240, 440), "color": "ink", "width": 5, "kind": "box", "start": C("Watch what happens")},
        {"d": "M 800 578 L 1040 578", "color": "ink", "width": 3, "start": C("Watch what happens", 0.4), "label": lbl("MATERIALS", 920, 710, 24, "accent2")},
        {"d": "M 800 520 L 1040 520", "color": "ink", "width": 3, "start": C("Watch what happens", 0.7), "label": lbl("PAYROLL 13¢", 920, 556, 22, "accent")},
        {"d": dot(920, 455), "color": "ink", "width": 1, "start": C("Watch what happens", 1.0), "label": lbl("EVERYTHING ELSE", 920, 455, 22, "ink")},
        {"d": "M 820 530 L 1020 570 M 1020 530 L 820 570", "color": "risk", "width": 7, "start": C("when I pull labor out")},
        {"d": arrow((1050, 550), (1260, 470), -0.2), "color": "risk", "width": 5, "kind": "arrow", "start": C("Even if every paycheck")},
        {"d": rect(1270, 420, 200, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Even if every paycheck", 0.4), "label": lbl("PAYCHECKS", 1370, 468, 22, "risk")},
        {"d": dot(1300, 640), "color": "ink", "width": 1, "start": C("the materials, the machines"), "label": lbl("STILL HERE: MATERIALS", 1300, 640, 20, "ink")},
        {"d": dot(1300, 676), "color": "ink", "width": 1, "start": C("the energy"), "label": lbl("MACHINES · ENERGY · BUILDING", 1300, 676, 20, "ink")},
        {"d": rect(1220, 720, 240, 60), "color": "accent2", "width": 5, "kind": "box", "start": C("send a bill of their own"), "label": lbl("ROBOTS + SOFTWARE: A NEW BILL", 1340, 758, 16, "accent2")},
        {"d": dot(920, 860), "color": "muted", "width": 1, "start": C("Automation shrinks"), "label": lbl("CENSUS 2021 SURVEY OF MANUFACTURES · OUR CALCULATION · SIZES SCHEMATIC", 920, 860, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("It doesn't make the factory free", 0.0), "dur": 1.4, "target": [920, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["census_asm21"])

# ====================================================================== ACT 4: the $100 experiment
bumper("s17_b4", "a4_card", "4", "ACT FOUR", "THE HUNDRED-DOLLAR EXPERIMENT", "No toasters were harmed. Several were modeled.", PURPLE)
stage("s18_setup", "a4_setup", {
    **W1("toastlab", cols=[], plain=True),
    "cam": cam((0, 960, 540, 1.0), (C("Her toaster costs"), 900, 600, 1.25, 1.2), (C("Our model is illustrative"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [it("gizmo", x=900, y=780, at=0.3, scale=0.7, face="happy", parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]],
                 stamp="$100 · MADE + SHIPPED TO A U.S. WAREHOUSE", stampAt=C("ship to an American"), stampY=60),
              words("MEL'S $100 TOASTER EXPERIMENT", 960, 140, 0.3, until=C("Our model is illustrative"), size=60),
              words("A SIMPLE MODEL · NOT ANY COMPANY'S COSTS", 960, 140, C("Our model is illustrative"), size=48, color="#FFFFFF"),
              MEL(1400, 0.4, face="happy", pose="point", faces=[[0, "happy"], [C("Her toaster costs"), "grin"]], hops=[C("Her toaster costs", 0.3)]),
              KIP(450, 0.5, face="smug", pose="clipboard", hold="clipboard"),
              sign("WHAT MATTERS: HOW THE NUMBERS MOVE", 960, 300, C("What matters"), color="#FFF59D", size=30)]})
stage("s19_f1", "a4_f1", {
    **W1("toastlab", plain=True, cols=[COL1(blocks(("MATERIALS", 61, MAT, C("suppliers next door")), ("LABOR", 11, LAB, C("Cheap labor")), ("MACHINES", 5, MAC, 0.4),
                                       ("ENERGY", 3, ENG, 0.6), ("UPKEEP", 2, UPK, 0.8), ("DEFECTS", 3, DEF, 1.0),
                                       ("SHIPPING", 6, SHP, C("an ocean to cross")), ("TARIFF", 9, TAR, C("and a tariff"))), at=0.2)],
         knobs=[{"label": "TARIFF", "v": 10, "at": C("and a tariff"), "max": 30, "show": [[0, "SOME"]]}]),
    "cam": cam((0, 700, 540, 1.1), (C("an ocean to cross"), 800, 480, 1.05, 1.2), (C("That's Mel's benchmark"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [MEL(1250, 0.3, face="happy", pose="point", label="MEL · RUNNING THE NUMBERS", labelUntil=C("an ocean to cross")),
              sign("BENCHMARK", 600, 300, C("That's Mel's benchmark"), color="#FFF59D", size=34),
              sign("TARIFF: OUR ASSUMPTION (REAL RATES VARY AND CHANGE)", 1300, 300, C("and a tariff"), color="#FFE0B2", size=24, until=C("That's Mel's benchmark"))]})
stage("s20_f2", "a4_f2", {
    **W1("toastlab", plain=True, cols=[COL1(F1()), COL2(blocks(("MATERIALS", [[0, 61], [C("many parts still come"), 64]], MAT, C("Next, Kip's dream")), ("LABOR", 13, LAB, C("but American pay")),
                                                 ("MACHINES", 14, MAC, C("add a big bill")), ("ENERGY", 3, ENG, C("add a big bill", 0.3)), ("UPKEEP", 4, UPK, C("add a big bill", 0.6)),
                                                 ("DEFECTS", 2, DEF, C("add a big bill", 0.9)), ("SHIPPING", 2, SHP, C("No ocean"))), at=C("Next, Kip's dream"))],
         knobs=KNOBS()),
    "cam": cam((0, 900, 540, 1.0), (C("Robots, software"), 1000, 500, 1.1, 1.2), (C("but many parts"), 900, 600, 1.1, 1.2), (C("The total"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [KIP(1450, 0.3, face="smug", pose="point", label="KIP · NOW SELLING OHIO", labelUntil=C("but American pay"), faces=[[0, "smug"], [C("but many parts"), "worry"]]),
              sign("MOST LABOR HOURS GONE · HIGHER PAY", 900, 260, C("Robots cut most"), color="#FFE0B2", size=24, until=C("Robots, software")),
              sign("PARTS STILL FROM ASIA", 900, 260, C("but many parts"), color="#FFCDD2", size=26), MEL(300, 0.3, face="happy", faces=[[0, "happy"], [C("The total"), "shock"]])]})
stage("s21_tie", "a4_tie", {
    **W1("toastlab", plain=True, cols=[COL1(F1()), COL2(F2())], knobs=KNOBS()),
    "cam": cam((0, 760, 500, 1.15), (C("Now watch"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("ALMOST A TIE", 760, 120, 0.2, size=70),
              MEL(1500, 0.2, face="shock", pose="armsup", hops=[0.6]), TORQ(300, 0.3, faces=[[0, "happy"], [C("Now watch"), "smug"]])]})
stage("s22_flip", "a4_flip", {
    **W1("toastlab", cols=[COL1(blocks(("MATERIALS", 61, MAT), ("LABOR", 11, LAB), ("MACHINES", 5, MAC), ("ENERGY", 3, ENG), ("UPKEEP", 2, UPK), ("DEFECTS", 3, DEF), ("SHIPPING", 6, SHP),
                                       ("TARIFF", [[0, 9], [C("Raise the tariff"), 9], [C("gets pricier"), 21], [C("Now let Ohio's"), 9]], TAR))),
                           COL2(blocks(("MATERIALS", 64, MAT), ("LABOR", 13, LAB), ("MACHINES", [[0, 14], [C("The cost of the machines"), 14], [C("doubles"), 28], [C("Tariffs, busy robots"), 14]], MAC),
                                       ("ENERGY", 3, ENG), ("UPKEEP", 4, UPK), ("DEFECTS", 2, DEF), ("SHIPPING", 2, SHP)))],
         judgeAt=0.3, plain=True, knobs=[{"label": "TARIFF", "v": [[0, 10], [C("Raise the tariff"), 10], [C("gets pricier"), 25], [C("Now let Ohio's"), 10]], "at": 0, "max": 30,
                                          "show": [[0, "SOME"], [C("gets pricier"), "HIGH"], [C("Now let Ohio's"), "SOME"]]},
                             {"label": "ROBOTS BUSY", "v": [[0, 100], [C("sit idle"), 100], [C("doubles"), 50], [C("Tariffs, busy robots"), 100]], "at": 0,
                              "show": [[0, "ALWAYS"], [C("sit idle"), "HALF THE TIME"], [C("Tariffs, busy robots"), "ALWAYS"]]}]),
    "cam": cam((0, 960, 520, 1.0), (C("Raise the tariff"), 1300, 520, 1.05, 1.0), (C("Ohio wins"), 800, 480, 1.1, WHIP), (C("sit idle"), 1300, 520, 1.05, 1.0),
               (C("China wins again"), 800, 480, 1.1, WHIP), (C("Those are the switches"), 960, 520, 0.95, 1.2)), "drift": 2,
    "items": [words("OHIO WINS", 760, 110, C("Ohio wins"), until=C("Now let Ohio's"), size=64, color="#FFFFFF"),
              words("CHINA WINS AGAIN", 760, 110, C("China wins again"), until=C("Tariffs, busy robots"), size=64, color="#FFFFFF"),
              words("THE SWITCHES: TARIFFS · BUSY ROBOTS · PARTS · ROBOT PRICES", 960, 110, C("Tariffs, busy robots"), size=40),
              MEL(1500, 0.2, face="happy", pose="stand", faces=[[0, "happy"], [C("Ohio wins"), "grin"], [C("China wins again"), "shock"]], hops=[C("Ohio wins", 0.2)], takes=[C("China wins again", 0.2)])]},
    sfx=[{"kind": "hit", "cue": "Ohio wins", "gain": 0.3}, {"kind": "hit", "cue": "China wins again", "gain": 0.3}])
stage("s23_f3", "a4_f3", {
    **W1("toastlab", plain=True, cols=[COL1(F1()), COL2(F2()),
                           COL3(blocks(("MATERIALS", 59, MAT, C("suppliers down the street")), ("LABOR", 3, LAB, C("Lower wages")), ("MACHINES", 11, MAC, C("Chinese-made robots")),
                                       ("ENERGY", 3, ENG, C("Chinese-made robots", 0.3)), ("UPKEEP", 3, UPK, C("Chinese-made robots", 0.6)), ("DEFECTS", 2, DEF, C("Chinese-made robots", 0.9)),
                                       ("SHIPPING", 6, SHP, C("that we assume")), ("TARIFF", 8, TAR, C("that we assume", 0.4))), at=C("The same robots"))],
         knobs=KNOBS(), judgeAt=C("five dollars under", 0.3)),
    "cam": cam((0, 700, 520, 1.0), (C("The same robots"), 1300, 520, 1.05, 1.2), (C("five dollars under"), 960, 520, 0.95, 1.2)), "drift": 3,
    "items": [TORQ([[0, 1900], [C("Then Wei calls back"), 1500]], 0.0, faces=[[0, "shock"], [C("The same robots"), "worry"]]),
              WEI(1600, C("Then Wei calls back"), face="happy", pose="point", hold="phone", label="WEI · CALLING FROM CHINA", labelUntil=C("Lower wages")),
              sign("CHINESE-MADE ROBOTS COST LESS: OUR ASSUMPTION", 1300, 230, C("that we assume"), color="#FFE0B2", size=24, until=C("five dollars under"))]},
    sfx=[{"kind": "hit", "cue": "five dollars under", "gain": 0.3}])
add("p24_who", "a4_result", "engine_draw", {
    "title": "Who wins when? (illustrative model)", "board": BOARD, "draw_start": C("In our base case"), "speed": 1700, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": dot(700, 500), "color": "ink", "width": 1, "start": C("In our base case"), "label": lbl("BASE CASE", 700, 500, 28, "ink", "start")},
        {"d": rect(1180, 465, 280, 54), "color": "accent3", "width": 5, "kind": "box", "start": C("Wei's automated factory wins"), "label": lbl("WEI (CHINA, ROBOTS)", 1320, 500, 22, "accent3")},
        {"d": dot(700, 600), "color": "ink", "width": 1, "start": C("Ohio only comes out ahead"), "label": lbl("HIGH TARIFF + BUSY ROBOTS", 700, 600, 28, "ink", "start")},
        {"d": rect(1180, 565, 280, 54), "color": "accent2", "width": 5, "kind": "box", "start": C("and its robots stay busy"), "label": lbl("OHIO", 1320, 600, 24, "accent2")},
        {"d": dot(700, 700), "color": "ink", "width": 1, "start": C("doesn't automatically favor"), "label": lbl("IDLE ROBOTS OR LOW TARIFF", 700, 700, 28, "ink", "start")},
        {"d": rect(1180, 665, 280, 54), "color": "risk", "width": 5, "kind": "box", "start": C("doesn't automatically favor", 0.6), "label": lbl("NOT OHIO", 1320, 700, 24, "risk")},
        {"d": "M 660 780 L 1480 780", "color": "accent", "width": 6, "start": C("It favors whoever"), "label": lbl("AUTOMATION FAVORS WHOEVER AUTOMATES BEST, AT SCALE", 1070, 830, 24, "accent")},
        {"d": dot(1070, 880), "color": "muted", "width": 1, "start": C("Which raises"), "label": lbl("ILLUSTRATIVE MODEL · OUR ASSUMPTIONS · FULL TABLE IN THE DESCRIPTION", 1070, 880, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Is China actually automating", 0.0), "dur": 1.4, "target": [1320, 500]}],
    "scale": 0.86, "floor": 1040})

# ====================================================================== ACT 5: the twist, China has robots too (midpoint)
bumper("s25_b5", "a5_card", "5", "ACT FIVE", "CHINA HAS ROBOTS TOO", "Plot twist. Bolted to the floor.", RED, torq_face="shock")
stage("s26_reveal", "a5_reveal", {
    **W1("ohiobot", variant="cn", arms=7, armX=-400, armGap=380, scanX=2300, schedX=1300, carts=4),
    "cam": cam((0, 960, 600, 1.4), (C("Last year"), 960, 520, 0.85, 2.0), (C("Compared with America"), 960, 520, 0.9, 1.2), (C("In a single year"), 960, 560, 1.15, WHIP)), "drift": 5,
    "items": [words("IT IS.", 960, 160, 0.1, until=C("Last year"), size=90, color="#FFFFFF"),
              words("MORE NEW ROBOTS THAN THE REST OF THE WORLD COMBINED", 960, 160, C("than the rest of the world"), size=46, until=C("Compared with America")),
              sign("IFR WORLD ROBOTICS 2026 · INSTALLATIONS IN 2025", 960, 270, C("than the rest of the world", 0.5), color="#FFF59D", size=24, until=C("Compared with America")),
              words("≈ 9 TO 1 VS AMERICA", 960, 170, C("Compared with America"), size=70, color="#FFFFFF"),
              sign("OUR CALCULATION FROM IFR DATA", 960, 290, C("robots for every"), color="#FFF8E1", size=22),
              WEI(600, 0.3, face="happy", pose="wave", label="WEI · HER LINE, NOW AUTOMATED", labelUntil=C("Compared with America")),
              MEL(1700, C("Compared with America"), face="shock", pose="armsup", hops=[C("In a single year")]),
              TORQ([[0, 2400], [C("than the rest of the world"), 1400]], C("than the rest of the world"), faces=[[0, "shock"], [C("In a single year"), "shock"]], hops=[C("In a single year")])]},
    sources=["ifr_wr26", "ifr_pr_global"], sfx=[{"kind": "hit", "cue": "In a single year", "gain": 0.35}])
stage("s27_race", "a5_chart", {
    **W1("robotrace", title="INDUSTRIAL ROBOTS INSTALLED IN 2025 · IFR WORLD ROBOTICS 2026", max=354, h=520, gap=420,
         rows=[{"name": "CHINA", "value": 354.2, "at": C("China's tower"), "display": "≈ 354,000", "color": RED},
               {"name": "U.S. (NOW #2)", "value": 38.4, "at": C("America, now"), "display": "≈ 38,000", "color": CY},
               {"name": "REST OF WORLD", "value": 210.7, "at": C("And worldwide"), "display": "≈ 211,000", "color": PURPLE}],
         foot="WORLD TOTAL A RECORD · REST OF WORLD = OUR CALCULATION"),
    "cam": cam((0, 960, 540, 1.0), (C("China's tower"), 700, 520, 1.15, 1.0), (C("America, now"), 960, 560, 1.05, 1.2), (C("And worldwide"), 960, 540, 0.95, 1.2)), "drift": 2,
    "items": [KIP(1750, 0.2, face="shock", pose="armsup", faces=[[0, "worry"], [C("China's tower"), "shock"], [C("America, now"), "happy"]], hops=[C("America, now")])]},
    sources=["ifr_wr26", "ifr_pr_global"])
stage("s28_brands", "a5_brands", {
    **W1("robotrace", title="CHINESE BRANDS' SHARE OF CHINA'S NEW ROBOT INSTALLATIONS (IFR)", max=60, h=520, gap=520,
         rows=[{"name": "A FEW YEARS AGO", "value": 30, "at": C("A few years ago"), "display": "≈ 30%", "color": "#90A4AE"},
               {"name": "LAST YEAR", "value": 55, "at": C("Now Chinese brands"), "display": "MORE THAN HALF", "color": RED}], hi=1),
    "cam": cam((0, 960, 540, 1.05), (C("A few years ago"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("SECOND SURPRISE: MADE IN CHINA, TOO", 960, 110, 0.2, until=C("A few years ago"), size=54),
              WEI(1650, 0.3, face="happy", pose="point", hold="clipboard"), TORQ(300, 0.3, face="worry", faces=[[0, "worry"], [C("Now Chinese brands"), "shock"]])]},
    sources=["ifr_pr_china", "ifr_wr26"])
add("p29_density", "a5_density", "engine_draw", {
    "title": "Robots per 10,000 factory employees, 2025 (IFR, Nov 2026)", "board": BOARD, "draw_start": C("Now the twist"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 660 820 L 1440 820", "color": "ink", "width": 5, "start": C("Per factory worker")},
        {"d": "M 960 820 L 960 723 L 1120 723 L 1120 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.6, "kind": "bar", "start": C("America has more robots"), "label": lbl("U.S. 323", 1040, 705, 22, "accent2")},
        {"d": "M 1200 820 L 1200 762 L 1360 762 L 1360 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.7, "kind": "bar", "start": C("Per factory worker", 0.6), "label": lbl("CHINA 193", 1280, 744, 22, "risk")},
        {"d": "M 720 820 L 720 500 L 880 500 L 880 820 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.6, "kind": "bar", "start": C("South Korea"), "label": lbl("S. KOREA 1,066", 800, 482, 22, "accent3")},
        {"d": dot(1280, 600), "color": "risk", "width": 1, "start": C("spread thin"), "label": lbl("SO MANY WORKERS → SPREAD THIN", 1200, 600, 22, "risk")},
        {"d": arrow((1280, 630), (1280, 730), 0.0), "color": "risk", "width": 5, "kind": "arrow", "start": C("spread thin", 0.5)},
        {"d": dot(1200, 550), "color": "accent", "width": 1, "start": C("That's room to grow"), "label": lbl("ROOM TO GROW", 1200, 550, 30, "accent")},
        {"d": dot(1050, 870), "color": "muted", "width": 1, "start": C("That's room to grow"), "label": lbl("CHINA ON A NATIONAL ECONOMIC CENSUS EMPLOYMENT BASE (IFR) · BARS TO SCALE", 1050, 870, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("spread thin", 0.2), "dur": 1.4, "target": [1280, 780]}, {"kind": "react", "at": C("That's room to grow", 0.2), "dur": 1.0}],
    "scale": 0.86, "floor": 1040}, sources=["ifr_density"])
stage("s30_why", "a5_why", {
    **W1("ohiobot", variant="cn", arms=6, armX=-200, armGap=420, scanX=2100, schedX=900, schedAt=C("five-year plan"), carts=3),
    "cam": cam((0, 1000, 560, 1.0), (C("The federation points"), 1100, 520, 0.95, 1.2), (C("Robots don't cancel"), 1400, 600, 1.05, 1.2), (C("Plugged into"), 2100, 640, 0.95, 1.4)), "drift": 4,
    "items": [words("HUGE ROOM LEFT TO AUTOMATE", 960, 120, 0.2, until=C("The federation points"), size=56),
              sign("LABOR SHORTAGE: AN AGING POPULATION (IFR)", 800, 120, C("labor shortage"), color="#FFE0B2", size=28, until=C("Robots don't cancel")),
              sign("NEW FIVE-YEAR PLAN: AI FOR PHYSICAL USES LIKE ROBOTS (IFR)", 1300, 230, C("five-year plan"), color="#C8E6C9", size=26, until=C("Robots don't cancel")),
              words("ROBOTS + SUPPLIERS DOWN THE STREET", 1700, 140, C("Plugged into"), size=50, color="#FFFFFF"),
              WEI(1200, 0.3, face="happy", pose="clipboard", hold="clipboard")]},
    sources=["ifr_pr_china"])

# ====================================================================== ACT 6: who captures the money?
bumper("s31_b6", "a6_card", "6", "ACT SIX", "WHO CAPTURES THE MONEY?", "Follow the toaster. Then follow the money.", GREEN)
SRCS = [{"label": "ROBOT ARMS", "from": "IMPORTED", "at": C("Robot arms"), "x": 230, "y": 260, "color": PURPLE},
        {"label": "PRECISION GEARS", "from": "IMPORTED", "at": C("precision"), "x": 1690, "y": 260, "color": ORANGE},
        {"label": "SENSORS", "from": "IMPORTED", "at": C("sensors"), "x": 230, "y": 700, "color": GREEN},
        {"label": "CHIPS", "from": "IMPORTED", "at": C("chips"), "x": 1690, "y": 700, "color": CY},
        {"label": "MAGNETS", "from": "RARE EARTHS", "at": C("rare-earth magnets"), "x": 960, "y": 210, "color": RED}]
stage("s32_supply", "a6_supply", {
    **W1("chainweb", srcs=SRCS, cutAt=C("from abroad", -0.4), cutIdx=4),
    "cam": cam((0, 960, 640, 1.3), (C("Robot arms"), 960, 540, 1.0, 1.4), (C("Build the factory"), 960, 520, 0.95, 1.2)), "drift": 3,
    "items": [words("THE SUPPLY-CHAIN PROBLEM", 960, 120, 0.2, until=C("Robot arms"), size=56),
              words("ITS BRAIN AND ITS MUSCLES: IMPORTED", 960, 1000, C("its brain"), size=46, color="#FFFFFF"),
              MEL(1250, 0.3, scale=0.9, y=800, face="worry", pose="shrug", faces=[[0, "happy"], [C("still depend"), "worry"], [C("from abroad"), "shock"]])]})
stage("s33_who", "a6_who", {
    **W1("chainweb", srcs=[{"label": "ROBOTS", "from": "JAPAN: #1 ROBOT MAKER (IFR)", "at": C("Japan builds"), "x": 230, "y": 260, "color": PURPLE},
                           {"label": "AUTOMATION", "from": "GERMANY · SWITZERLAND", "at": C("Germany and Switzerland"), "x": 1690, "y": 260, "color": ORANGE},
                           {"label": "AI + CHIP DESIGN", "from": "UNITED STATES", "at": C("America leads"), "x": 230, "y": 700, "color": CY},
                           {"label": "CHIPS", "from": "TAIWAN · SOUTH KOREA", "at": C("Taiwan"), "x": 1690, "y": 700, "color": GREEN},
                           {"label": "RARE EARTHS", "from": "CHINA: MOST REFINING (IEA)", "at": C("And China refines"), "x": 960, "y": 210, "color": RED}],
         plantName="OHIO PLANT", foot="WHO SUPPLIES THE AUTOMATED FACTORY"),
    "cam": cam((0, 700, 400, 1.2), (C("Germany and Switzerland"), 1300, 400, 1.2, 1.2), (C("America leads"), 700, 640, 1.2, 1.2), (C("Taiwan"), 1300, 640, 1.2, 1.2),
               (C("And China refines"), 960, 400, 1.15, 1.2), (C("behind those magnets"), 960, 540, 1.0, 1.2)), "drift": 2,
    "items": [sign("IFR (JUL 2025) · IEA (2025 DATA)", 960, 1010, C("behind those magnets"), color="#FFFFFF", size=22)]},
    sources=["ifr_japan", "iea_gcmo"])
add("p34_chain", "a6_draw", "engine_draw", {
    "title": "Where the money from Mel's toaster could go (illustrative)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1700, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(940, 370, 180, 70), "color": "accent", "width": 6, "kind": "box", "start": C("Let me draw"), "label": lbl("$100 SALE", 1030, 414, 26, "accent")},
        *[{"d": arrow((1030, 440), (x + 70, 590), 0.0), "color": "ink", "width": 4, "kind": "arrow", "start": C(cue, -0.2)} for x, cue in
          [(600, "Materials and parts"), (720, "The robot maker"), (840, "Chips and"), (960, "AI software"), (1080, "Energy"), (1200, "Logistics"), (1320, "factory owner")]],
        *[{"d": rect(x, 600, 140, 90), "color": c_, "width": 5, "kind": "box", "start": C(cue), "label": lbl(t_, x + 70, 652, 16, c_)} for x, cue, t_, c_ in
          [(600, "Materials and parts", "MATERIALS", "accent2"), (720, "The robot maker", "ROBOT MAKER", "ink"), (840, "Chips and", "CHIPS+SENSORS", "ink"),
           (960, "AI software", "AI SOFTWARE", "accent2"), (1080, "Energy", "ENERGY", "ink"), (1200, "Logistics", "LOGISTICS", "ink"), (1320, "factory owner", "OWNER", "accent3")]],
        {"d": dot(1030, 760), "color": "risk", "width": 1, "start": C("whatever is left"), "label": lbl("THE OWNER GETS WHAT'S LEFT", 1030, 760, 24, "risk")},
        {"d": dot(1030, 820), "color": "muted", "width": 1, "start": C("factory owner", 0.3), "label": lbl("ILLUSTRATIVE VALUE CHAIN · NO MEASURED SHARES", 1030, 820, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("factory owner", 0.2), "dur": 1.4, "target": [1390, 645]}],
    "scale": 0.86, "floor": 1040})
stage("s35_lesson", "a6_lesson", {
    **W1("moneyriver", buckets=[{"label": "MATERIALS & PARTS", "level": 0.9, "at": 0.2, "color": TEAL}, {"label": "ROBOT MAKER", "level": 0.45, "at": 0.4, "color": PURPLE},
                                {"label": "CHIPS & SENSORS", "level": 0.4, "at": 0.6, "color": "#5C6BC0"}, {"label": "AI SOFTWARE", "level": 0.35, "at": 0.8, "color": CY},
                                {"label": "ENERGY", "level": 0.25, "at": 1.0, "color": "#F2C14E"}, {"label": "LOGISTICS", "level": 0.25, "at": 1.2, "color": ORANGE},
                                {"label": "FACTORY OWNER", "level": [[0, 0.3], [C("may not capture"), 0.12]], "at": 1.4, "color": GREEN}], ownerAt=C("may not capture")),
    "cam": cam((0, 960, 420, 1.15), (C("The country that hosts"), 1500, 760, 1.2, 1.4), (C("In an automated world"), 960, 520, 0.95, 1.4)), "drift": 3,
    "items": [words("THE FACTORY ≠ THE MONEY", 760, 120, C("The country that hosts"), until=C("In an automated world"), size=56),
              words("ROBOTS · SOFTWARE · CHIPS", 760, 120, C("In an automated world"), size=56, color="#FFFFFF"),
              MEL(250, 0.3, face="happy", pose="point", hold="phone", faces=[[0, "happy"], [C("may not capture"), "shock"]])]})

# ====================================================================== ACT 7: the verdict
bumper("s36_b7", "a7_card", "7", "ACT SEVEN", "THE VERDICT", "No crystal balls were used in this verdict.", NAVY)
stage("s37_where", "a7_where", {
    **W1("ohiobot", variant="us", arms=5, armX=-100, armGap=480, scanX=1700, schedX=900, carts=3),
    "cam": cam((0, 960, 520, 0.95), (C("For some products"), 900, 520, 1.05, WHIP), (C("The likeliest"), 960, 500, 0.95, 1.2)), "drift": 4,
    "items": [it("pricemeter", x=960, y=360, at=0.2, until=C("The likeliest"), tilt=[[0, 0.5], [C("For some products"), -0.5]], scale=0.75, left="OHIO", right="CHINA"),
              words("FOR SOME PRODUCTS: YES", 960, 110, C("For some products"), size=64, color="#FFFFFF", until=C("The likeliest")),
              sign("HEAVY OR BULKY: COSTLY TO SHIP", 600, 140, C("heavy or bulky"), color="#BBDEFB", size=28),
              sign("MANY REPEATED PRECISION STEPS", 1300, 140, C("many repeated"), color="#C8E6C9", size=28),
              sign("CAN'T RISK RUNNING OUT: CHIPS · BATTERIES · MEDICAL SUPPLIES", 960, 270, C("can't risk"), color="#FFF59D", size=28, until=C("A toaster is light")),
              MEL(1500, 0.3, face="happy", pose="cheer", hops=[C("For some products", 0.2)], faces=[[0, "happy"], [C("A toaster is light"), "worry"]]),
              it("bubble", text="...AND MY TOASTER\nIS LIGHT. HMM.", x=1500, y=420, at=C("A toaster is light"), tail=[1500, 600], size=28)]})
stage("s38_jobs", "a7_jobs", {
    **W1("ohiobot", variant="us", arms=5, armX=-100, armGap=480, scanX=1700, schedX=900, techX=1400, carts=2),
    "cam": cam((0, 960, 540, 1.0), (C("Economists"), 960, 500, 0.95, 1.2), (C("The new jobs"), 1300, 600, 1.1, 1.4)), "drift": 3,
    "items": [words("THE FACTORY COMES BACK. THE OLD JOBS? NOT ALL.", 960, 120, 0.2, until=C("Economists"), size=46),
              sign("MORE ROBOTS → FEWER PEOPLE EMPLOYED, LOWER WAGES", 960, 120, C("the more robots arrived"), color="#FFF59D", size=30,
                   sub="U.S. LOCAL JOB MARKETS, 1990–2007 · ACEMOGLU & RESTREPO, JPE 2020"),
              sign("NEW JOBS: TECHNICIANS · PROGRAMMERS · MAINTENANCE CREWS", 1300, 320, C("The new jobs"), color="#C8E6C9", size=28),
              MEL(500, 0.3, face="worry", pose="shrug", hold="phone", faces=[[0, "worry"], [C("The new jobs"), "happy"]])]},
    sources=["ar_jpe"])
stage("s39_china", "a7_china", {
    **W1("ohiobot", variant="cn", arms=6, armX=-200, armGap=420, scanX=2100, schedX=900, carts=3, idle=[[0, 0], [C("Robots sitting idle"), 0], [C("Robots sitting idle", 1.0), 0.9], [C("missing parts"), 0]]),
    "cam": cam((0, 960, 540, 0.95), (C("What could stop"), 960, 520, 1.05, WHIP)), "drift": 4,
    "items": [words("CHINA KEEPS: SUPPLIERS · PORTS · SCALE · ROBOTS", 960, 110, 0.2, until=C("What could stop"), size=44),
              words("WHAT COULD STOP THE COMEBACK?", 960, 110, C("What could stop"), size=54, color="#FFFFFF"),
              sign("IDLE ROBOTS", 500, 230, C("Robots sitting idle"), color="#FFCDD2", size=30), sign("MISSING SUPPLIERS", 900, 230, C("missing parts"), color="#FFCDD2", size=30),
              sign("EXPENSIVE MONEY", 1300, 230, C("expensive money"), color="#FFCDD2", size=30), sign("SHIFTING TRADE RULES", 1650, 230, C("trade rules"), color="#FFCDD2", size=30),
              KIP(1600, 0.3, face="smug", pose="stand", faces=[[0, "smug"], [C("What could stop"), "worry"]], takes=[C("What could stop", 0.3)])]})
stage("s40_verdict", "a7_verdict", {
    "zones": [Z("ohiobot", x0=-1600, x1=1600, variant="cn", arms=3, armX=-300, armGap=500, scanX=1100, schedX=-900, carts=2),
              Z("ohiobot", x0=1600, x1=5000, variant="us", arms=3, armX=2300, armGap=500, scanX=3600, schedX=3100, carts=2)], "worldW": 3400,
    "cam": cam((0, 1600, 520, 0.7), (C("For decades"), 600, 520, 1.0, 1.6), (C("Now it's who"), 2700, 520, 1.0, 1.6),
               (C("America can win back"), 2700, 520, 1.1, 1.0), (C("And China can automate"), 600, 520, 1.1, 1.2), (C("Mel's choice won't"), 1600, 520, 0.7, 1.6)), "drift": 2,
    "items": [words("AI DOESN'T END IT. IT CHANGES THE TEST.", 1600, 120, 0.3, until=C("For decades"), size=50),
              words("OLD TEST: CHEAPEST WORKERS", 600, 140, C("For decades"), until=C("Now it's who"), size=50),
              words("NEW TEST: THE BEST SYSTEM", 2700, 140, C("Now it's who"), until=C("America can win back"), size=50, color="#FFFFFF"),
              sign("MACHINES · ENERGY · CAPITAL · SUPPLY CHAIN", 2700, 260, C("intelligent machines"), color="#FFF59D", size=28, until=C("America can win back")),
              sign("U.S.: COMPETITIVENESS BACK, PRODUCT BY PRODUCT · NOT THE SAME JOBS", 2700, 150, C("America can win back"), color="#BBDEFB", size=28, until=C("Mel's choice won't")),
              sign("CHINA: CAN AUTOMATE TOO", 600, 150, C("And China can automate"), color="#FFCDD2", size=32, until=C("Mel's choice won't")),
              words("NOT THE CHEAPEST LABOR. THE BEST SYSTEM.", 1600, 120, C("Mel's choice won't"), size=58, color="#FFFFFF"),
              WEI(500, 0.3, face="happy", pose="wave"), KIP(2600, 0.3, face="happy", pose="stand"), MEL(2900, 0.3, face="happy", pose="cheer", hops=[C("Mel's choice won't", 1.0)]),
              TORQ(1600, C("Mel's choice won't"), faces=[[0, "happy"]])]})
add("s41_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s42_button", "button", {
    **W1("ohiobot", variant="us", arms=3, armX=1400, armGap=420, scanX=2600, schedX=-800, carts=1),
    "cam": cam((0, 900, 560, 1.2), (3.2, 960, 560, 1.35, WHIP)), "drift": 0, "min_seconds": 5.6,
    "items": [it("gizmo", x=700, y=760, at=0.0, scale=0.55, face="happy", toastAt=1.2, parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]],
                 stamp="MADE IN OHIO* (*PARTS: EVERYWHERE)", stampAt=2.2, stampX=0, stampY=60),
              MEL(450, 0.0, face="grin", pose="cheer", hops=[1.4], scale=1.2),
              TORQ(1150, 0.0, legs=True, legsFallAt=3.2, faces=[[0, "smug"], [3.2, "shock"]], hops=[2.6]),
              it("bubble", text="LOOK! I'M A HUMANOID NOW!", x=1150, y=260, at=1.6, until=3.2, tail=[1150, 520], size=30),
              words("...STILL BOLTED TO THE FLOOR. ALMOST.", 960, 160, 3.6, size=52, color="#FFFFFF")]},
    sfx=[{"kind": "hit", "at": 3.2, "gain": 0.3}])

write(OUT, "# GENERATED by tools/gen_aimfg_storyboard.py; edit the generator, not this file.\n"
           "# Episode 62 storyboard (AI and manufacturing, arc Episode 2): bespoke worlds in CartoonStage/automation.tsx; tones from visual_direction.yaml.\n")
