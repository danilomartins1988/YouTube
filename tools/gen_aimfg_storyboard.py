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
KNOBS = lambda tar=10, busy=100, at=0.0: [{"label": "TARIFF", "v": tar, "at": at, "max": 30}, {"label": "ROBOTS BUSY", "v": busy, "at": at}]

# ====================================================================== ACT 1: the factory that changes everything (hook)
stage("s01_hook", "co_hook", {
    **W1("ohiobot", variant="us", hyp=True, hypAt=0, hypX=960, hypY=70, arms=5, armX=-200, armGap=520, scanX=1560, schedX=1250,
         hiAt=[[0, None], [C("Cameras check"), "vision"], [C("Software decides"), "sched"], [C("Now imagine"), None]]),
    "cam": cam((0, 700, 560, 1.15), (C("Inside, robot arms"), 900, 520, 1.0, 1.4), (C("Cameras check"), 1500, 480, 1.25, 1.0),
               (C("Software decides"), 1250, 300, 1.25, 1.0), (C("Now imagine"), 960, 520, 0.9, 1.4), (C("That factory is hypothetical"), 960, 500, 1.0, WHIP),
               (C("So could"), 960, 460, 0.85, 1.4)), "drift": 4,
    "items": [words("OHIO · SUNDAY AFTERNOON", 700, 200, 0.2, until=C("Inside, robot arms"), size=58),
              it("pricemeter", x=960, y=380, at=C("costs about the same"), until=C("That factory is hypothetical"), tilt=[[0, 0.6], [C("costs about the same", 0.4), 0.0]], scale=0.75,
                 left="OHIO", right="CHINA"),
              TORQ([[C("That factory is hypothetical"), 2300], [C("But almost every piece", 0.4), 1250]], C("That factory is hypothetical"),
                   faces=[[0, "happy"], [C("But almost every piece"), "smug"]]),
              sign("EVERY PIECE EXISTS SOMEWHERE · THE WHOLE THING, NOT YET", 960, 200, C("But almost every piece"), color="#FFF59D", size=28, until=C("So could")),
              words("COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?", 960, 190, C("So could"), size=46, color="#FFFFFF"),
              MEL([[C("would America actually win"), -200], [C("would America actually win", 1.0), 420]], C("would America actually win", -0.2), face="shock", pose="armsup")]},
    sfx=[{"kind": "hit", "cue": "That factory is hypothetical", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("aititle", lines=["CHEAPER THAN", "CHINA?"], sub="COULD AI MAKE AMERICAN FACTORIES CHEAPER THAN CHINA'S?",
         subs=[[2.2, "Tonight: “The Robot Who Wanted Legs” · Part 2 of the factory story"]]), "cam": STILL(), "drift": 0, "min_seconds": 5.4,
    "items": [TORQ(300, 2.4, y=1060, scale=0.8, legs=True, legsFallAt=4.4, faces=[[0, "happy"], [4.4, "shock"]]), MEL(1700, 2.6, scale=1.1, face="happy", pose="wave", y=1080)]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}, {"kind": "hit", "at": 4.5, "gain": 0.25}])
stage("s03_stakes", "a1_stakes", {
    **W1("ohiobot", variant="cn", arms=3, armX=200, armGap=700, scanX=2000, schedX=2400, carts=2, idle=[[0, 1.0], [C("But a robot"), 1.0], [C("If machines do more"), 0.0]]),
    "cam": cam((0, 900, 520, 0.95), (C("But a robot"), 1000, 520, 1.15, WHIP), (C("If machines do more"), 1100, 500, 0.95, 1.4), (C("And the stakes"), 1100, 480, 0.9, 1.2)), "drift": 4,
    "items": [words("RULE #1: GO WHERE WORK IS CHEAPEST", 960, 160, 0.3, until=C("But a robot"), size=52),
              KIP(500, 0.2, pose="point", face="smug", label="KIP · RELOCATION CONSULTANT", labelUntil=C("But a robot"), faces=[[0, "smug"], [C("starts to wobble"), "worry"]],
                  takes=[C("starts to wobble")]),
              TORQ([[C("But a robot"), -300], [C("But a robot", 1.2), 900]], C("But a robot", -0.3), faces=[[0, "happy"], [C("doesn't care"), "smug"]]),
              it("bubble", text="WAGES?\nNEVER HEARD OF 'EM.", x=1120, y=300, at=C("doesn't care about wages"), until=C("If machines do more", 0.6), tail=[960, 560], size=28),
              words("THE OLD RULE WOBBLES", 1100, 160, C("starts to wobble"), size=56, until=C("And the stakes")),
              sign("PRICES", 700, 180, C("Prices"), color="#FFE0B2", size=34), sign("SUPPLY CHAINS", 1100, 260, C("supply chains"), color="#C8E6C9", size=34),
              sign("WHO MAKES WHAT EVERYONE NEEDS", 1500, 180, C("which country"), color="#BBDEFB", size=34)]})
add("p04_output", "a1_output", "engine_draw", {
    "title": "U.S. factories: output vs jobs since June 1979", "board": BOARD, "draw_start": C("America has already"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("America has already")},
        {"d": "M 700 820 L 700 667 L 840 667 L 840 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("Since the summer"), "label": lbl("OUTPUT 1979 · 47.6", 770, 650, 20, "accent2")},
        {"d": "M 860 820 L 860 500 L 1000 500 L 1000 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.75, "kind": "bar", "start": C("roughly doubled"), "label": lbl("2026 · 99.7 (×2.1)", 930, 482, 20, "accent2")},
        {"d": "M 1120 820 L 1120 508 L 1260 508 L 1260 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.3, "kind": "bar", "start": C("factory jobs fell"), "label": lbl("JOBS 1979 · 19.6M", 1190, 490, 20, "risk")},
        {"d": "M 1280 820 L 1280 617 L 1420 617 L 1420 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.75, "kind": "bar", "start": C("to about twelve point seven"), "label": lbl("OCT 2026 · 12.7M", 1350, 600, 20, "risk")},
        {"d": arrow((930, 440), (1340, 560), -0.2), "color": "accent", "width": 5, "kind": "arrow", "start": C("More stuff"), "label": lbl("MORE STUFF, FEWER PEOPLE", 1130, 420, 24, "accent")},
        {"d": dot(1050, 875), "color": "muted", "width": 1, "start": C("by our calculation"), "label": lbl("OUTPUT: FED G.17 INDEX (2017=100) · JOBS: BLS · RATIOS OUR CALCULATION", 1050, 875, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("More stuff", 0.2), "dur": 1.4, "target": [1350, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["fred_ipman", "fred_manemp"])

# ====================================================================== ACT 2: the old formula (brief: Episode 1 recap)
bumper("s05_b2", "a2_card", "2", "ACT TWO", "THE OLD FORMULA", "Previously, on The Hidden Economics...", ORANGE)
stage("s06_formula", "a2_formula", {
    **W1("megafloor", board="EPISODE 1: THE EVERYTHING FACTORY", boardX=1000),
    "cam": cam((0, 1000, 480, 1.05), (C("Here's the short version"), 1050, 520, 0.95, 1.4), (C("It has suppliers"), 1200, 520, 1.0, 1.2)), "drift": 5,
    "items": [sign("LAST TIME: “WHY THE WORLD STILL DEPENDS ON CHINESE FACTORIES”", 1000, 120, C("In our last episode"), color="#FFFFFF", size=28, until=C("Here's the short version")),
              words("≈ 27% OF WORLD MANUFACTURING (2025)", 1000, 120, C("China makes"), size=50, until=C("It has suppliers")),
              sign("WORLD BANK WDI · OUR CALCULATION", 1000, 220, C("of the world's manufactured"), color="#FFF8E1", size=22, until=C("It has suppliers")),
              sign("SUPPLIERS", 600, 140, C("suppliers down the street"), color="#C8E6C9", size=32), sign("PORTS", 980, 140, C("giant ports"), color="#BBDEFB", size=32),
              sign("POWER", 1340, 140, C("steady power"), color="#FFF59D", size=32), sign("ENGINEERS", 1700, 140, C("engineers who have"), color="#FFE0B2", size=32),
              WEI(1450, 0.3, pose="wave", face="happy", label="WEI · LINE ENGINEER", labelUntil=C("Here's the short version"), poses=[[0, "wave"], [C("It has suppliers"), "point"]]),
              it("gizmo", x=600, y=760, at=0.4, scale=0.5, face="happy", parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]])]},
    sources=["wdi_mva"])
stage("s07_wage", "a2_wage", {
    **W1("megafloor", board="THE OLD FORMULA: PAY", boardX=-1400, hi=0),
    "cam": cam((0, 960, 540, 1.0), (C("A production"), 1000, 520, 1.05, 1.2), (C("By our rough math"), 960, 500, 1.15, WHIP)), "drift": 3,
    "items": [it("counter", x=600, y=170, at=C("an American factory"), prefix="$", suffix=" / HOUR", decimals=0, steps=[[0, 0], [C("an American factory"), 0], [C("earned about"), 29]],
                 text="U.S. PRODUCTION WORKER, 2025 (BLS)"),
              it("counter", x=1350, y=170, at=C("A production worker at"), prefix="$", suffix=" / YEAR", decimals=0, steps=[[0, 0], [C("A production worker at"), 0], [C("for the whole year"), 11200]],
                 text="CHINA, LARGER FIRMS, 2025 (NBS; FED RATE; OUR CONVERSION)"),
              words("PER HOUR: ROUGHLY 1/5 (ROUGH, OUR CALCULATION)", 960, 360, C("By our rough math"), size=44, color="#FFFFFF"),
              MEL(450, 0.3, face="happy", pose="clipboard", hold="phone", faces=[[0, "happy"], [C("By our rough math"), "shock"]], takes=[C("By our rough math")]),
              WEI(1550, 0.3, face="happy", pose="stand", hold="clipboard")]},
    sources=["bls_ces", "nbs_wage", "fed_g5a"])
stage("s08_question", "a2_question", {
    **W1("megafloor", board="LABOR: CHINA'S OLDEST HEAD START", boardX=-1400, hi=None),
    "cam": cam((0, 900, 520, 1.0), (C("does China's oldest"), 1000, 500, 1.15, WHIP), (C("To find out"), 1300, 520, 0.95, 1.4)), "drift": 4,
    "items": [TORQ([[0, -300], [1.4, 800]], 0.0, faces=[[0, "happy"], [C("does China's oldest"), "smug"]]),
              it("homebox", x=[[0, 1000], [C("shrink the labor"), 1000], [C("does China's oldest"), 1000]], at=0.2, label="LABOR", face="worry", scale=1.0),
              words("ROBOTS SHRINK LABOR → HEAD START SHRINKS?", 960, 160, C("So if robots"), size=48, until=C("To find out")),
              words("WHAT CAN AI REALLY DO ON A FACTORY FLOOR?", 1300, 160, C("To find out"), size=48, color="#FFFFFF")]})

# ====================================================================== ACT 3: when labor matters less
bumper("s09_b3", "a3_card", "3", "ACT THREE", "WHEN LABOR MATTERS LESS", "Results not typical. Robots shown are bolted down.", CY)
stage("s10_vision", "a3_vision", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1500, schedX=600, hi="vision"),
    "cam": cam((0, 1300, 520, 1.0), (C("Cameras running AI"), 1500, 470, 1.35, 1.4), (C("guide robot arms"), 1000, 500, 1.2, 1.2), (C("The International Federation"), 1200, 480, 0.95, 1.4)), "drift": 4,
    "items": [words("PROVEN #1: MACHINE VISION", 1300, 120, 0.3, until=C("The International Federation"), size=56),
              sign("✓ CHECKS EVERY PART", 1800, 260, C("faster than a human eye"), color="#C8E6C9", size=28),
              sign("✓ GUIDES THE GRIPPER", 900, 260, C("guide robot arms"), color="#BBDEFB", size=28),
              sign("“ESTABLISHED AND INDUSTRY-GRADE” · IFR WORLD ROBOTICS 2026", 1200, 140, C("calls machine vision"), color="#FFF59D", size=30)]},
    sources=["ifr_wr26"])
stage("s11_maint", "a3_maint", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1700, schedX=1400, maintAt=C("Sensors listen"), maintX=600, schedAt=C("reshuffles the line"), carts=4,
         hiAt=[[0, "maint"], [C("Then smart scheduling"), "sched"], [C("self-driving carts"), "carts"], [C("The federation says"), None]]),
    "cam": cam((0, 600, 600, 1.3), (C("Then smart scheduling"), 1400, 300, 1.2, 1.4), (C("self-driving carts"), 1000, 760, 1.05, 1.4), (C("The federation says"), 1100, 520, 0.9, 1.4)), "drift": 4,
    "items": [words("PREDICTIVE MAINTENANCE", 600, 120, 0.3, until=C("Then smart scheduling"), size=52),
              it("bubble", text="THAT MOTOR SOUNDS\nTIRED. FIX IT THURSDAY.", x=900, y=330, at=C("flags it"), until=C("Then smart scheduling"), tail=[650, 700], size=26),
              words("SMART SCHEDULING", 1400, 600, C("Then smart scheduling"), size=48, until=C("self-driving carts")),
              words("SELF-DRIVING CARTS", 1000, 520, C("self-driving carts"), size=48, until=C("The federation says")),
              sign("“INCREASINGLY USED IN INDUSTRY” · IFR 2026", 1100, 140, C("The federation says"), color="#FFF59D", size=30),
              WEI(1650, C("Then smart scheduling"), face="happy", pose="point", hold="clipboard", label="WEI · VISITING ENGINEER", labelUntil=C("self-driving carts"))]},
    sources=["ifr_wr26"])
stage("s12_twin", "a3_twin", {
    **W1("ohiobot", variant="us", arms=4, armX=100, armGap=480, scanX=1700, schedX=-600, twinAt=C("a full virtual copy"), twinX=900),
    "cam": cam((0, 900, 560, 1.0), (C("a full virtual copy"), 900, 380, 0.9, 1.6), (C("Foxconn says"), 900, 420, 0.95, 1.2)), "drift": 4,
    "items": [words("DIGITAL TWINS", 960, 110, 0.3, until=C("a full virtual copy"), size=60),
              sign("TEST THE LINE BEFORE YOU BUILD IT", 960, 120, C("where engineers test"), color="#C8E6C9", size=30, until=C("Foxconn says")),
              sign("FOXCONN: DIGITAL TWIN OF A NEW GUADALAJARA PLANT · ROBOTS TRAINED IN SIMULATION", 960, 120, C("Foxconn says"), color="#FFF59D", size=26,
                   sub="COMPANY STATEMENT · NVIDIA BLOG, JUN 2024 · A PLANNING TOOL, NOT A 'LIGHTS-OUT' FACTORY"),
              KIP(1700, 0.3, face="happy", pose="point", hold="phone", faces=[[0, "happy"], [C("a full virtual copy"), "shock"]], takes=[C("a full virtual copy", 0.3)])]},
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
              sign("MOST HUMANOIDS: PROTOTYPES OR PILOTS (IFR 2026)", 760, 120, C("most are still prototypes"), color="#FFF59D", size=28, until=C("It's the arm")),
              sign("TODAY: INDUSTRIAL ROBOTS ARE ECONOMICALLY SUPERIOR (IFR)", 1300, 240, C("economically superior"), color="#C8E6C9", size=26),
              TORQ([[0, 1000], [C("The robot that matters"), 1000], [C("It's the arm"), 1200]], 0.2, legs=True, legsFallAt=C("isn't the one that dances"),
                   faces=[[0, "smug"], [C("isn't the one that dances"), "shock"], [C("It's the arm", 0.5), "happy"]]),
              words("THE ARM BOLTED TO THE FLOOR", 1600, 140, C("It's the arm"), size=54, color="#FFFFFF")]},
    sources=["ifr_wr26"], sfx=[{"kind": "hit", "cue": "isn't the one that dances", "gain": 0.3}])
stage("s15_bill", "a3_bill", {
    **W1("billbox", title="WHERE $1 OF U.S. FACTORY SALES WENT · 2021", slices=[[0.4, "MATERIALS & PARTS ≈ 55¢", 55, TEAL],
                                                                                 [C("Wages and salaries"), "PAYROLL ≈ 13¢", 13, ORANGE],
                                                                                 [C("That's our calculation", -0.2), "EVERYTHING ELSE ≈ 32¢", 32, PURPLE]],
         note="CENSUS 2021 ANNUAL SURVEY OF MANUFACTURES · SHARES ARE OUR CALCULATION · PAYROLL = ALL EMPLOYEES, BEFORE BENEFITS", noteAt=C("for American factories")),
    "cam": cam((0, 960, 520, 1.05), (C("Wages and salaries"), 960, 560, 1.15, 1.2), (C("That's our calculation"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [MEL(1500, 0.3, face="shock", pose="point", faces=[[0, "happy"], [C("came to"), "shock"]], takes=[C("came to", 0.5)]),
              it("bubble", text="ONLY 13 CENTS?!", x=1550, y=300, at=C("came to", 0.6), tail=[1500, 560], size=34),
              TORQ(380, 0.2, faces=[[0, "happy"], [C("Wages and salaries"), "worry"]])]},
    sources=["census_asm21"])
add("p16_pull", "a3_pull", "engine_draw", {
    "title": "Pull labor out: what's left of $1 of factory sales", "board": BOARD, "draw_start": C("Watch what happens"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(800, 380, 240, 440), "color": "ink", "width": 5, "kind": "box", "start": C("Watch what happens")},
        {"d": "M 800 578 L 1040 578", "color": "ink", "width": 3, "start": C("Watch what happens", 0.4), "label": lbl("MATERIALS 55¢", 920, 710, 24, "accent2")},
        {"d": "M 800 520 L 1040 520", "color": "ink", "width": 3, "start": C("Watch what happens", 0.7), "label": lbl("PAYROLL 13¢", 920, 556, 22, "accent")},
        {"d": dot(920, 455), "color": "ink", "width": 1, "start": C("Watch what happens", 1.0), "label": lbl("EVERYTHING ELSE 32¢", 920, 455, 22, "ink")},
        {"d": "M 820 530 L 1020 570 M 1020 530 L 820 570", "color": "risk", "width": 7, "start": C("when I pull labor out")},
        {"d": arrow((1050, 550), (1260, 470), -0.2), "color": "risk", "width": 5, "kind": "arrow", "start": C("Even if every paycheck")},
        {"d": rect(1270, 420, 200, 80), "color": "risk", "width": 5, "kind": "box", "start": C("Even if every paycheck", 0.4), "label": lbl("PAYCHECKS", 1370, 468, 22, "risk")},
        {"d": dot(1300, 640), "color": "ink", "width": 1, "start": C("the materials, the machines"), "label": lbl("STILL HERE: MATERIALS", 1300, 640, 20, "ink")},
        {"d": dot(1300, 676), "color": "ink", "width": 1, "start": C("the energy"), "label": lbl("MACHINES · ENERGY · BUILDING", 1300, 676, 20, "ink")},
        {"d": rect(1220, 720, 240, 60), "color": "accent2", "width": 5, "kind": "box", "start": C("have a bill of their own"), "label": lbl("ROBOTS + SOFTWARE: A NEW BILL", 1340, 758, 16, "accent2")},
        {"d": dot(920, 860), "color": "muted", "width": 1, "start": C("Automation shrinks"), "label": lbl("CENSUS ASM 2021 · OUR CALCULATION · NEW BILL SIZE NOT MEASURED", 920, 860, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("It doesn't make the factory free", 0.0), "dur": 1.4, "target": [920, 650]}],
    "scale": 0.86, "floor": 1040}, sources=["census_asm21"])

# ====================================================================== ACT 4: the $100 experiment
bumper("s17_b4", "a4_card", "4", "ACT FOUR", "THE HUNDRED-DOLLAR EXPERIMENT", "No toasters were harmed. Several were modeled.", PURPLE)
stage("s18_setup", "a4_setup", {
    **W1("toastlab", cols=[]),
    "cam": cam((0, 960, 540, 1.0), (C("Let's say a smart toaster"), 900, 600, 1.25, 1.2), (C("Our numbers are illustrative"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [it("gizmo", x=900, y=780, at=0.3, scale=0.7, face="happy", parts=[[0, p] for p in ["BODY", "SLOTS", "COIL", "LEVER", "KNOB", "PLUG", "FEET"]],
                 stamp="$100 · MADE + SHIPPED TO A U.S. WAREHOUSE", stampAt=C("ship to an American"), stampY=60),
              words("THE $100 TOASTER EXPERIMENT", 960, 140, 0.3, until=C("Our numbers are illustrative"), size=60),
              words("A SIMPLE MODEL · NOT ANY COMPANY'S COSTS", 960, 140, C("Our numbers are illustrative"), size=48, color="#FFFFFF"),
              MEL(1400, 0.4, face="happy", pose="point", faces=[[0, "happy"], [C("smart toaster"), "grin"]], hops=[C("smart toaster", 0.3)]),
              WEI(450, 0.5, face="happy", pose="clipboard", hold="clipboard"),
              sign("WHAT MATTERS: HOW THE NUMBERS MOVE", 960, 300, C("What matters"), color="#FFF59D", size=30)]})
stage("s19_f1", "a4_f1", {
    **W1("toastlab", cols=[COL1(blocks(("MATERIALS", 61, MAT, C("Materials and parts")), ("LABOR", 11, LAB, C("Labor, eleven")), ("MACHINES", 5, MAC, C("Machines, energy")),
                                       ("ENERGY", 3, ENG, C("Machines, energy", 0.3)), ("UPKEEP", 2, UPK, C("upkeep")), ("DEFECTS", 3, DEF, C("and defects")),
                                       ("SHIPPING", 6, SHP, C("Shipping across")), ("TARIFF", 9, TAR, C("nine"))), at=C("Factory one"))],
         knobs=[{"label": "TARIFF", "v": 10, "at": C("import tariff"), "max": 30}]),
    "cam": cam((0, 700, 540, 1.1), (C("Shipping across"), 800, 480, 1.05, 1.2), (C("Total, one hundred"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [WEI(1250, 0.3, face="happy", pose="point", label="WEI · CONVENTIONAL LINE", labelUntil=C("Labor, eleven")),
              sign("TARIFF: OUR ASSUMPTION (REAL RATES VARY AND CHANGE)", 1300, 300, C("which we set"), color="#FFE0B2", size=24)]})
stage("s20_f2", "a4_f2", {
    **W1("toastlab", cols=[COL1(F1()), COL2(blocks(("MATERIALS", [[0, 61], [C("so materials rise"), 64]], MAT, C("Factory two")), ("LABOR", 13, LAB, C("labor comes to")),
                                                 ("MACHINES", 14, MAC, C("machines jump")), ("ENERGY", 3, ENG, C("machines jump", 0.3)), ("UPKEEP", 4, UPK, C("upkeep to four")),
                                                 ("DEFECTS", 2, DEF, C("Defects fall")), ("SHIPPING", 2, SHP, C("No ocean"))), at=C("Factory two"))],
         knobs=KNOBS()),
    "cam": cam((0, 900, 540, 1.0), (C("Robots, software"), 1000, 500, 1.1, 1.2), (C("But many parts"), 900, 600, 1.1, 1.2), (C("Total, about one hundred and two"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [KIP(1450, 0.3, face="smug", pose="point", label="KIP · NOW SELLING OHIO", labelUntil=C("but American pay"), faces=[[0, "smug"], [C("But many parts"), "worry"]]),
              sign("¾ FEWER LABOR HOURS · HIGHER PAY", 900, 260, C("Robots cut labor hours"), color="#FFE0B2", size=24, until=C("Robots, software")),
              sign("PARTS STILL FROM ASIA", 900, 260, C("But many parts"), color="#FFCDD2", size=26)]})
stage("s21_tie", "a4_tie", {
    **W1("toastlab", cols=[COL1(F1()), COL2(F2())], knobs=KNOBS()),
    "cam": cam((0, 760, 500, 1.15), (C("Now watch"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("≈ $100 vs ≈ $102 · ALMOST A TIE", 760, 120, 0.2, size=54),
              MEL(1500, 0.2, face="shock", pose="armsup", hops=[0.6]), TORQ(300, 0.3, faces=[[0, "happy"], [C("Now watch"), "smug"]])]})
stage("s22_flip", "a4_flip", {
    **W1("toastlab", cols=[COL1(blocks(("MATERIALS", 61, MAT), ("LABOR", 11, LAB), ("MACHINES", 5, MAC), ("ENERGY", 3, ENG), ("UPKEEP", 2, UPK), ("DEFECTS", 3, DEF), ("SHIPPING", 6, SHP),
                                       ("TARIFF", [[0, 9], [C("Raise the tariff"), 9], [C("factory one jumps"), 21], [C("Now let the Ohio"), 9]], TAR))),
                           COL2(blocks(("MATERIALS", 64, MAT), ("LABOR", 13, LAB), ("MACHINES", [[0, 14], [C("The machine cost"), 14], [C("Ohio climbs"), 28], [C("Tariffs, utilization"), 14]], MAC),
                                       ("ENERGY", 3, ENG), ("UPKEEP", 4, UPK), ("DEFECTS", 2, DEF), ("SHIPPING", 2, SHP)))],
         judgeAt=0.3, knobs=[{"label": "TARIFF", "v": [[0, 10], [C("Raise the tariff"), 10], [C("factory one jumps"), 25], [C("Now let the Ohio"), 10]], "at": 0, "max": 30},
                             {"label": "ROBOTS BUSY", "v": [[0, 100], [C("sit idle"), 100], [C("Ohio climbs"), 50], [C("Tariffs, utilization"), 100]], "at": 0}]),
    "cam": cam((0, 960, 520, 1.0), (C("Raise the tariff"), 1300, 520, 1.05, 1.0), (C("Ohio wins"), 800, 480, 1.1, WHIP), (C("sit idle"), 1300, 520, 1.05, 1.0),
               (C("China wins again"), 800, 480, 1.1, WHIP), (C("Those are the switches"), 960, 520, 0.95, 1.2)), "drift": 2,
    "items": [words("OHIO WINS", 760, 110, C("Ohio wins"), until=C("Now let the Ohio"), size=64, color="#FFFFFF"),
              words("CHINA WINS AGAIN", 760, 110, C("China wins again"), until=C("Tariffs, utilization"), size=64, color="#FFFFFF"),
              words("THE SWITCHES: TARIFFS · UTILIZATION · PARTS · ROBOT PRICES", 960, 110, C("Tariffs, utilization"), size=40),
              KIP(1500, 0.2, face="happy", pose="stand", faces=[[0, "happy"], [C("Ohio wins"), "grin"], [C("China wins again"), "shock"]], hops=[C("Ohio wins", 0.2)], takes=[C("China wins again", 0.2)])]},
    sfx=[{"kind": "hit", "cue": "Ohio wins", "gain": 0.3}, {"kind": "hit", "cue": "China wins again", "gain": 0.3}])
stage("s23_f3", "a4_f3", {
    **W1("toastlab", cols=[COL1(F1()), COL2(F2()),
                           COL3(blocks(("MATERIALS", 59, MAT, C("Materials, fifty-nine")), ("LABOR", 3, LAB, C("Labor drops")), ("MACHINES", 11, MAC, C("Machines, eleven")),
                                       ("ENERGY", 3, ENG, C("Machines, eleven", 0.3)), ("UPKEEP", 3, UPK, C("Machines, eleven", 0.6)), ("DEFECTS", 2, DEF, C("Machines, eleven", 0.9)),
                                       ("SHIPPING", 6, SHP, C("Shipping and tariff")), ("TARIFF", 8, TAR, C("Shipping and tariff", 0.4))), at=C("Factory three"))],
         knobs=KNOBS(), judgeAt=C("Total, about ninety-five", 0.3)),
    "cam": cam((0, 700, 520, 1.0), (C("Factory three"), 1300, 520, 1.05, 1.2), (C("Total, about ninety-five"), 960, 520, 0.95, 1.2)), "drift": 3,
    "items": [TORQ([[0, 1900], [C("But we forgot someone"), 1500]], 0.0, faces=[[0, "shock"], [C("Factory three"), "worry"]]),
              WEI(1600, C("Factory three", 0.3), face="happy", pose="point", label="WEI · AUTOMATED LINE", labelUntil=C("Labor drops")),
              sign("CHINESE-MADE ROBOTS COST LESS: OUR ASSUMPTION", 1300, 230, C("that we assume"), color="#FFE0B2", size=24, until=C("Total, about ninety-five"))]},
    sfx=[{"kind": "hit", "cue": "Total, about ninety-five", "gain": 0.3}])
add("p24_who", "a4_result", "engine_draw", {
    "title": "Who wins when? (illustrative model, $ per toaster)", "board": BOARD, "draw_start": C("In our base case"), "speed": 1700, "push": 0.003,
    "enter": {"from": 2200, "to": 1720, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 440 L 1480 440", "color": "ink", "width": 4, "start": C("In our base case"), "label": lbl("SCENARIO        CHINA · OHIO · CHINA AUTO   WINNER", 1040, 420, 20, "muted")},
        {"d": dot(640, 500), "color": "ink", "width": 1, "start": C("In our base case"), "label": lbl("BASE (≈10% TARIFF)   100 · 102 · 95", 640, 500, 24, "ink", "start")},
        {"d": rect(1290, 470, 180, 44), "color": "accent3", "width": 4, "kind": "box", "start": C("the automated Chinese factory wins"), "label": lbl("CHINA AUTO", 1380, 500, 20, "accent3")},
        {"d": dot(640, 580), "color": "ink", "width": 1, "start": C("Ohio only comes out ahead"), "label": lbl("25% TARIFF, BUSY ROBOTS   112 · 102 · 107", 640, 580, 24, "ink", "start")},
        {"d": rect(1290, 550, 180, 44), "color": "accent2", "width": 4, "kind": "box", "start": C("tariffs are high"), "label": lbl("OHIO", 1380, 580, 20, "accent2")},
        {"d": dot(640, 660), "color": "ink", "width": 1, "start": C("and its robots stay busy"), "label": lbl("ROBOTS IDLE HALF THE TIME   OHIO → 116", 640, 660, 24, "ink", "start")},
        {"d": rect(1290, 630, 180, 44), "color": "risk", "width": 4, "kind": "box", "start": C("and its robots stay busy", 0.5), "label": lbl("NOT OHIO", 1380, 660, 20, "risk")},
        {"d": dot(640, 740), "color": "ink", "width": 1, "start": C("doesn't automatically favor"), "label": lbl("NO TARIFF   91 · 102 · 87", 640, 740, 24, "ink", "start")},
        {"d": rect(1290, 710, 180, 44), "color": "accent3", "width": 4, "kind": "box", "start": C("doesn't automatically favor", 0.5), "label": lbl("CHINA AUTO", 1380, 740, 20, "accent3")},
        {"d": "M 620 800 L 1480 800", "color": "accent", "width": 6, "start": C("It favors whoever"), "label": lbl("AUTOMATION FAVORS WHOEVER AUTOMATES BEST, AT SCALE", 1050, 840, 22, "accent")},
        {"d": dot(1050, 880), "color": "muted", "width": 1, "start": C("Which raises"), "label": lbl("ILLUSTRATIVE MODEL · OUR ASSUMPTIONS · NOT REAL COMPANY COSTS", 1050, 880, 16, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("Is China actually automating", 0.0), "dur": 1.4, "target": [1380, 500]}],
    "scale": 0.86, "floor": 1040})

# ====================================================================== ACT 5: the twist, China has robots too (midpoint)
bumper("s25_b5", "a5_card", "5", "ACT FIVE", "CHINA HAS ROBOTS TOO", "Plot twist. Bolted to the floor.", RED, torq_face="shock")
stage("s26_reveal", "a5_reveal", {
    **W1("ohiobot", variant="cn", arms=7, armX=-400, armGap=380, scanX=2300, schedX=1300, carts=4),
    "cam": cam((0, 960, 600, 1.4), (C("In twenty twenty-five"), 960, 520, 0.85, 2.0), (C("The United States installed"), 960, 520, 0.9, 1.2), (C("In a single year"), 960, 560, 1.15, WHIP)), "drift": 5,
    "items": [words("IT IS.", 960, 160, 0.1, until=C("In twenty twenty-five"), size=90, color="#FFFFFF"),
              it("counter", x=960, y=140, at=C("factories in China installed"), suffix=" ROBOTS", decimals=0, until=C("In a single year", -0.3),
                 steps=[[0, 0], [C("factories in China installed"), 0], [C("industrial robots"), 354226]], text="INSTALLED IN CHINA, 2025 (IFR WORLD ROBOTICS 2026)"),
              sign("59% OF THE WORLD'S NEW INDUSTRIAL ROBOTS", 960, 330, C("of every industrial robot"), color="#FFF59D", size=32, until=C("In a single year", -0.3)),
              sign("U.S.: 38,428", 1500, 430, C("The United States installed"), color="#BBDEFB", size=30, until=C("In a single year", -0.3)),
              words("≈ 9 TO 1 · IN ONE YEAR (OUR CALCULATION)", 960, 180, C("In a single year", -0.3), size=58, color="#FFFFFF"),
              WEI(600, 0.3, face="happy", pose="wave", label="WEI · HER LINE, NOW AUTOMATED", labelUntil=C("The United States installed")),
              TORQ([[0, 2400], [C("The United States installed"), 1500]], C("of every industrial robot"), faces=[[0, "shock"], [C("In a single year"), "shock"]], hops=[C("In a single year")])]},
    sources=["ifr_wr26", "ifr_pr_global"], sfx=[{"kind": "hit", "cue": "In a single year", "gain": 0.35}])
stage("s27_race", "a5_chart", {
    **W1("robotrace", title="INDUSTRIAL ROBOTS INSTALLED IN 2025 · UNITS · IFR WORLD ROBOTICS 2026", max=354, h=520, gap=300,
         rows=[{"name": "CHINA", "value": 354.2, "at": C("China, three hundred"), "display": "354,226", "color": RED},
               {"name": "U.S.", "value": 38.4, "at": C("The United States, about"), "display": "38,428 · NOW #2", "color": CY},
               {"name": "JAPAN", "value": 36.2, "at": C("Japan,"), "display": "36,219", "color": PURPLE},
               {"name": "S. KOREA", "value": 30, "at": C("South Korea"), "display": "≈ 30,000", "color": GREEN},
               {"name": "GERMANY", "value": 24, "at": C("Germany"), "display": "< 25,000", "color": ORANGE}],
         foot="WORLD 2025: 603,307 · A RECORD"),
    "cam": cam((0, 960, 540, 1.0), (C("China, three hundred"), 500, 520, 1.15, 1.0), (C("The United States, about"), 960, 560, 1.05, 1.2), (C("Worldwide"), 960, 540, 0.95, 1.2)), "drift": 2,
    "items": [KIP(1750, 0.2, face="shock", pose="armsup", faces=[[0, "worry"], [C("China, three hundred"), "shock"], [C("now the"), "happy"]], hops=[C("now the")])]},
    sources=["ifr_wr26", "ifr_pr_global"])
stage("s28_brands", "a5_brands", {
    **W1("robotrace", title="CHINESE BRANDS' SHARE OF CHINA'S NEW ROBOT INSTALLATIONS (IFR)", max=60, h=520, gap=520,
         rows=[{"name": "2019–2021", "value": 30, "at": C("A few years earlier"), "display": "≈ 30%", "color": "#90A4AE"},
               {"name": "2025", "value": 55, "at": C("Chinese brands supplied"), "display": "55%", "color": RED}], hi=1),
    "cam": cam((0, 960, 540, 1.05), (C("A few years earlier"), 960, 520, 1.0, 1.2)), "drift": 3,
    "items": [words("SECOND SURPRISE: MADE IN CHINA, TOO", 960, 110, 0.2, until=C("Chinese brands supplied"), size=54),
              WEI(1650, 0.3, face="happy", pose="point", hold="clipboard"), TORQ(300, 0.3, face="worry", faces=[[0, "worry"], [C("A few years earlier"), "shock"]])]},
    sources=["ifr_pr_china", "ifr_wr26"])
add("p29_density", "a5_density", "engine_draw", {
    "title": "Robots per 10,000 factory employees, 2025 (IFR, Nov 2026)", "board": BOARD, "draw_start": C("Now the twist"), "speed": 1600, "push": 0.003,
    "enter": {"from": -260, "to": 270, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 620 820 L 1480 820", "color": "ink", "width": 5, "start": C("The federation counts")},
        {"d": "M 680 820 L 680 500 L 820 500 L 820 820 Z", "color": "accent3", "width": 3, "fill": "accent3", "fillOpacity": 0.6, "kind": "bar", "start": C("South Korea"), "label": lbl("S. KOREA 1,066", 750, 482, 20, "accent3")},
        {"d": "M 880 820 L 880 723 L 1020 723 L 1020 820 Z", "color": "accent2", "width": 3, "fill": "accent2", "fillOpacity": 0.6, "kind": "bar", "start": C("The United States,"), "label": lbl("U.S. 323", 950, 705, 20, "accent2")},
        {"d": "M 1080 820 L 1080 762 L 1220 762 L 1220 820 Z", "color": "risk", "width": 3, "fill": "risk", "fillOpacity": 0.7, "kind": "bar", "start": C("one hundred and ninety-three"), "label": lbl("CHINA 193", 1150, 744, 20, "risk")},
        {"d": "M 1280 820 L 1280 774 L 1420 774 L 1420 820 Z", "color": "muted", "width": 3, "fill": "muted", "fillOpacity": 0.4, "kind": "bar", "start": C("because it has so many"), "label": lbl("WORLD 152", 1350, 756, 20, "muted")},
        {"d": dot(1150, 600), "color": "risk", "width": 1, "start": C("because it has so many"), "label": lbl("SO MANY WORKERS → LOW PER-WORKER COUNT", 1150, 600, 20, "risk")},
        {"d": arrow((1150, 640), (1150, 730), 0.0), "color": "risk", "width": 5, "kind": "arrow", "start": C("because it has so many", 0.5)},
        {"d": dot(1150, 560), "color": "accent", "width": 1, "start": C("its density rose"), "label": lbl("CHINA: +147% IN 2020–2025", 1150, 560, 24, "accent")},
        {"d": dot(1050, 870), "color": "muted", "width": 1, "start": C("its density rose"), "label": lbl("CHINA: NATIONAL ECONOMIC CENSUS EMPLOYMENT BASE (IFR) · BAR HEIGHTS TO SCALE", 1050, 870, 15, "muted")},
    ],
    "actions": [{"kind": "point", "at": C("one hundred and ninety-three", 0.3), "dur": 1.4, "target": [1150, 780]}, {"kind": "react", "at": C("its density rose", 0.4), "dur": 1.0}],
    "scale": 0.86, "floor": 1040}, sources=["ifr_density"])
stage("s30_why", "a5_why", {
    **W1("ohiobot", variant="cn", arms=6, armX=-200, armGap=420, scanX=2100, schedX=900, schedAt=C("five-year plan"), carts=3),
    "cam": cam((0, 1000, 560, 1.0), (C("The federation points"), 1100, 520, 0.95, 1.2), (C("Robots don't cancel"), 1400, 600, 1.05, 1.2), (C("Plugged into"), 2100, 640, 0.95, 1.4)), "drift": 4,
    "items": [words("HUGE ROOM LEFT TO AUTOMATE", 960, 120, 0.2, until=C("The federation points"), size=56),
              sign("LABOR SHORTAGE: AN AGING POPULATION (IFR)", 800, 120, C("labor shortage"), color="#FFE0B2", size=28, until=C("Robots don't cancel")),
              sign("15TH FIVE-YEAR PLAN (2026–30): AI → PHYSICAL USES (IFR)", 1300, 230, C("five-year plan"), color="#C8E6C9", size=26, until=C("Robots don't cancel")),
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
              KIP(1250, 0.3, scale=0.9, y=800, face="worry", pose="shrug", faces=[[0, "smug"], [C("still depend"), "worry"], [C("from abroad"), "shock"]])]})
stage("s33_who", "a6_who", {
    **W1("chainweb", srcs=[{"label": "ROBOTS", "from": "JAPAN: 38% OF OUTPUT (IFR)", "at": C("Japan makes"), "x": 230, "y": 260, "color": PURPLE},
                           {"label": "AUTOMATION", "from": "GERMANY · SWITZERLAND", "at": C("Germany and Switzerland"), "x": 1690, "y": 260, "color": ORANGE},
                           {"label": "AI + CHIP DESIGN", "from": "UNITED STATES", "at": C("America leads"), "x": 230, "y": 700, "color": CY},
                           {"label": "CHIPS", "from": "TAIWAN · SOUTH KOREA", "at": C("Taiwan"), "x": 1690, "y": 700, "color": GREEN},
                           {"label": "RARE EARTHS", "from": "CHINA: 85% OF REFINING", "at": C("And China does"), "x": 960, "y": 210, "color": RED}],
         plantName="OHIO PLANT", foot="WHO SUPPLIES THE AUTOMATED FACTORY"),
    "cam": cam((0, 700, 400, 1.2), (C("Germany and Switzerland"), 1300, 400, 1.2, 1.2), (C("America leads"), 700, 640, 1.2, 1.2), (C("Taiwan"), 1300, 640, 1.2, 1.2),
               (C("And China does"), 960, 400, 1.15, 1.2), (C("magnet rare earths"), 960, 540, 1.0, 1.2)), "drift": 2,
    "items": [sign("IFR (JUL 2025) · IEA (2025 DATA)", 960, 1010, C("magnet rare earths"), color="#FFFFFF", size=22)]},
    sources=["ifr_japan", "iea_gcmo"])
add("p34_chain", "a6_draw", "engine_draw", {
    "title": "Where the money from one robot-built toaster could go (illustrative)", "board": BOARD, "draw_start": C("Let me draw"), "speed": 1700, "push": 0.003,
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
              sign("CAN'T RISK RUNNING OUT: CHIPS · BATTERIES · MEDICAL SUPPLIES", 960, 270, C("can't risk"), color="#FFF59D", size=28),
              MEL(1500, 0.3, face="happy", pose="cheer", hops=[C("For some products", 0.2)])]})
stage("s38_jobs", "a7_jobs", {
    **W1("ohiobot", variant="us", arms=5, armX=-100, armGap=480, scanX=1700, schedX=900, techX=1400, carts=2),
    "cam": cam((0, 960, 540, 1.0), (C("Economists"), 960, 500, 0.95, 1.2), (C("The new jobs"), 1300, 600, 1.1, 1.4)), "drift": 3,
    "items": [words("THE FACTORY COMES BACK. THE OLD JOBS? NOT ALL.", 960, 120, 0.2, until=C("Economists"), size=46),
              sign("+1 ROBOT PER 1,000 WORKERS → EMPLOYMENT RATIO −0.2 PTS · WAGES −0.42%", 960, 120, C("each extra robot"), color="#FFF59D", size=26,
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
    "cam": cam((0, 1600, 520, 0.7), (C("For forty years"), 600, 520, 1.0, 1.6), (C("Now it's who"), 2700, 520, 1.0, 1.6),
               (C("America can win back"), 2700, 520, 1.1, 1.0), (C("And China can automate"), 600, 520, 1.1, 1.2), (C("The future of making"), 1600, 520, 0.7, 1.6)), "drift": 2,
    "items": [words("AI DOESN'T END IT. IT CHANGES THE TEST.", 1600, 120, 0.3, until=C("For forty years"), size=50),
              words("OLD TEST: CHEAPEST WORKERS", 600, 140, C("For forty years"), until=C("Now it's who"), size=50),
              words("NEW TEST: THE BEST SYSTEM", 2700, 140, C("Now it's who"), until=C("America can win back"), size=50, color="#FFFFFF"),
              sign("MACHINES · ENERGY · CAPITAL · SUPPLY CHAIN", 2700, 260, C("intelligent machines"), color="#FFF59D", size=28, until=C("America can win back")),
              sign("U.S.: COMPETITIVENESS BACK, PRODUCT BY PRODUCT · NOT THE SAME JOBS", 2700, 150, C("America can win back"), color="#BBDEFB", size=28, until=C("The future of making")),
              sign("CHINA: CAN AUTOMATE TOO", 600, 150, C("And China can automate"), color="#FFCDD2", size=32, until=C("The future of making")),
              words("NOT THE CHEAPEST LABOR. THE BEST SYSTEM.", 1600, 120, C("The future of making"), size=58, color="#FFFFFF"),
              WEI(500, 0.3, face="happy", pose="wave"), KIP(2600, 0.3, face="happy", pose="stand"), MEL(2900, 0.3, face="happy", pose="cheer", hops=[C("The future of making", 1.0)]),
              TORQ(1600, C("The future of making"), faces=[[0, "happy"]])]})
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
