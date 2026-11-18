"""Generates projects/could-brazil-become-the-worlds-factory-for-robots/deliverables/documentary/storyboard.yaml
(Episode 71: Could Brazil Become the World's Factory for Robots?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/brazil.tsx (brhq, brfab, brdam, brmine, brfields, brcity, brcounter, brroad, brbank, brplant,
brgate, brtitle, brbumper; item costpack). Reused generic sets: txscale (aitaxes, the Fair Scale), svmine 'outback' (shovels, a lithium pit).
Story over statistics: one protagonist (GUS, fictional factory scout of fictional Boltwell Robotics) with BIA (fictional engineer from Minas
Gerais) and the COST BACKPACK (one brick per stop). No real person drawn; companies named in narration and on plain plaques only; no logos,
no flags. Signature animations: 1 the spinning globe that lands on Brazil (s04), 2 the treasure tour (s08-s15), 3 the backpack tour with a
brick per stop (s18-s22), 4 the backpack getting lighter (s25), 5 the quiet plant that wakes up (s27).
Presenter boards: p05 the robot's bill, p12 the treasure map, p23 what robots remove and what they don't.
Run: python tools/gen_brazilai_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "could-brazil-become-the-worlds-factory-for-robots"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#1E88E5", "#F5B700", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#16223A", "#F08A24"
OX = 3400


def GUS(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=3, skin=0, hair=2, hairStyle=2, color=BLUE, glasses=True, **kw)


def BIA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.15)
    return it("toon", x=x, at=at, who="shopper", v=6, skin=4, hair=0, hairStyle=4, color=TEAL, glasses=False, scarf=GOLD, **kw)


def BOSS(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.15)
    return it("toon", x=x, at=at, who="shopper", v=8, skin=2, hair=4, hairStyle=1, color=PURPLE, glasses=False, **kw)


def LOCAL(x=None, at=0.0, v=9, color=BLUE, **kw):
    kw.setdefault("scale", 1.05)
    return it("toon", x=x, at=at, who="shopper", v=v, skin=(v * 3) % 6, hair=(v * 5) % 7, hairStyle=v % 6, color=color, glasses=v % 2 == 0, **kw)


def PACK(x, at=0.0, **kw):
    kw.setdefault("y", 1000)
    kw.setdefault("scale", 0.75)
    return it("costpack", x=x, at=at, **kw)


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
    stage(id_, seg, {**W1("brbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.2, "items": []},
          sfx=[{"kind": "whoosh", "at": 0.25, "gain": 0.25}, {"kind": "hit", "at": 0.7, "gain": 0.35}])


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


THUD = lambda cue: {"kind": "hit", "cue": cue, "gain": 0.35}
B_TAX, B_PAPER, B_TRUCK, B_LOAN = "TAXES ON TAXES", "PAPERWORK", "TRUCKS", "PRICEY LOANS"

# ====================================================================== HOOK
stage("s01_hook", "co_hook", {
    **W2("brhq", "brfab", {"spin": 0.25, "screen": [[0, "NEW PLANT: ROBOTS BUILD ROBOTS"], [C("For decades"), "OLD RULE: GO WHERE WORKERS ARE CHEAP"]]},
         {"arms": [[0, 2], [C("barely needs workers"), 6]], "people": [[0, 4], [C("barely needs workers"), 1]], "sign": [[0, "BOLTWELL PLANT (FICTIONAL)"]]}),
    "cam": cam((0, 960, 540, 0.95), (C("Meet Gus"), 1000, 560, 1.1, 1.2), (C("Find the best spot"), 560, 560, 1.05, 1.2), (C("barely needs workers"), OX + 960, 520, 0.9, WHIP),
               (C("So the answer changes"), OX + 960, 540, 1.0, 1.2), (C("Could the robot in your future"), 560, 540, 1.05, WHIP)), "drift": 3,
    "items": [GUS([[0, -200], [1.8, 900]], 0.0, face="happy", pose="stand", label="GUS · FACTORY SCOUT (FICTIONAL)", labelUntil=C("Find the best spot"),
                  faces=[[0, "happy"], [C("Go where workers are cheap"), "squint"], [C("Could the robot in your future"), "wow"]]),
              words("ROBOTS THAT BUILD ROBOTS", OX + 960, 380, C("a place where robots build robots"), size=54, until=C("Meet Gus")),
              words("FEW WORKERS NEEDED", OX + 960, 380, C("barely needs workers"), size=60, until=C("And a country that never")),
              words("THE MAP CHANGES", OX + 960, 380, C("So the answer changes"), size=60, until=C("Could the robot in your future")),
              words("YOUR NEXT ROBOT: MADE IN BRAZIL?", 960, 240, C("Could the robot in your future"), size=56),
              tag((0, "STORY · FICTIONAL CAST"), (C("barely needs workers"), "MECHANISM · OUR ANALYSIS"))]},
    sfx=[{"kind": "whoosh", "cue": "barely needs workers", "gain": 0.3}, {"kind": "hit", "cue": "Could the robot in your future", "gain": 0.35}])
stage("s02_title", "title_card", {**W1("brtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6, "items": []},
      sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])

# ====================================================================== CHAPTER 1
bumper("s03_b1", "c1_card", "CHAPTER ONE", "Robots redraw the map", "Wages shrink. Everything else gets heavier.", BLUE)
stage("s04_boss", "c1_boss", {
    **W1("brhq", spin=[[0, 0.3], [C("His boss spins"), 1.4], [C("So, where"), 0.6]], land=C("The boss smiles"),
         screen=[[0, "THE SEARCH"], [C("Look for cheap, clean power"), "1. CHEAP, CLEAN POWER"], [C("Look for the metals"), "2. METALS"],
                 [C("lots of customers"), "3. CUSTOMERS"], [C("The boss smiles"), "WHERE?"]]),
    "cam": cam((0, 900, 560, 1.0), (C("His boss spins"), 640, 600, 1.15, 1.2), (C("So stop looking"), 1300, 480, 1.05, 1.2),
               (C("Gus nods"), 900, 560, 1.1, 1.0), (C("The boss smiles"), 640, 600, 1.2, 1.0)), "drift": 2,
    "items": [BOSS(860, 0.0, face="smug", pose="talk", label="THE BOSS (FICTIONAL)", labelUntil=C("These robots work"), faces=[[0, "smug"], [C("The boss smiles"), "grin"]]),
              GUS(1100, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("So, where"), "squint"], [C("That's your job"), "shock"]], takes=[C("That's your job", 0.2)]),
              bub("STOP LOOKING FOR CHEAP WORKERS.", 860, 300, C("So stop looking"), until=C("Look for cheap, clean power"), tail=[860, 520], size=28),
              bub("SO... WHERE?", 1100, 320, C("So, where"), until=C("The boss smiles"), tail=[1100, 520]),
              bub("THAT'S YOUR JOB.", 860, 300, C("That's your job"), tail=[860, 520]),
              tag((0, "STORY"))]},
    sfx=[{"kind": "whoosh", "cue": "His boss spins", "gain": 0.3}, {"kind": "hit", "cue": "That's your job", "gain": 0.3}])
board("p05_draw", "c1_draw", "The bill for making a robot", "Let me draw what changes", [
    S(rect(640, 300, 300, 600), "ink", C("Here's the bill"), width=6, kind="box", label=lbl("OLD FACTORY", 790, 280, 28, "ink")),
    S(rect(660, 320, 260, 330), "risk", C("the heaviest part was wages"), width=4, fill="risk", fillOpacity=0.35, kind="bar", label=lbl("WAGES", 790, 495, 34, "ink")),
    S(rect(660, 670, 260, 210), "muted", C("the heaviest part was wages"), width=4, fill="muted", fillOpacity=0.25, kind="bar", label=lbl("EVERYTHING ELSE", 790, 780, 24, "ink")),
    S(rect(1300, 300, 300, 600), "ink", C("In a factory full of robots"), width=6, kind="box", label=lbl("ROBOT FACTORY", 1450, 280, 28, "ink")),
    S(rect(1320, 790, 260, 90), "risk", C("that part shrinks"), width=4, fill="risk", fillOpacity=0.35, kind="bar", label=lbl("WAGES", 1450, 845, 26, "ink")),
    S(rect(1320, 320, 260, 110), "accent", C("The power that runs"), width=4, fill="accent", fillOpacity=0.4, kind="bar", label=lbl("POWER", 1450, 385, 28, "ink")),
    S(rect(1320, 440, 260, 110), "accent2", C("The metal they're made of"), width=4, fill="accent2", fillOpacity=0.35, kind="bar", label=lbl("METAL", 1450, 505, 28, "ink")),
    S(rect(1320, 560, 260, 100), "accent3", C("The cost of moving things"), width=4, fill="accent3", fillOpacity=0.35, kind="bar", label=lbl("MOVING THINGS", 1450, 620, 24, "ink")),
    S(rect(1320, 670, 260, 110), "ink", C("the cost of the money you borrow"), width=4, fill="ink", fillOpacity=0.15, kind="bar", label=lbl("BORROWED MONEY", 1450, 735, 24, "ink")),
    S(arrow((960, 600), (1280, 600), -0.15), "accent", C("So what's left"), width=6, kind="arrow"),
    S(rect(820, 930, 660, 60), "accent3", C("Whoever makes those cheapest"), width=5, kind="box", label=lbl("CHEAPEST POWER + METAL + MONEY WINS", 1150, 972, 28, "accent3")),
    S(dot(1150, 1020), "muted", C("Let me draw what changes"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NOT TO SCALE)", 1150, 1020, 16, "muted")),
], [{"kind": "point", "at": C("the heaviest part was wages", 0.3), "dur": 1.4, "target": [790, 480]}, {"kind": "point", "at": C("that part shrinks", 0.3), "dur": 1.2, "target": [1450, 830]},
    {"kind": "react", "at": C("Whoever makes those cheapest", 0.3)}])
stage("s06_bia", "c1_bia", {
    **W1("brhq", spin=0.1, land=0.0, screen=[[0, "INCOMING VIDEO CALL"], [C("It's Bia"), "BIA · MINAS GERAIS, BRAZIL"], [C("Come and see"), "COME AND SEE!"]]),
    "cam": cam((0, 1200, 480, 1.0), (C("It's Bia"), 1340, 420, 1.15, 1.2), (C("Gus grabs a little backpack"), 900, 600, 1.1, 1.2), (C("Pack light"), 1100, 540, 1.0, 1.0)), "drift": 2,
    "items": [BIA(1640, C("It's Bia"), y=760, scale=0.9, face="grin", pose="talk", label="BIA · ENGINEER, MINAS GERAIS (FICTIONAL)", labelUntil=C("Come and see"),
                  faces=[[0, "grin"], [C("Bia laughs"), "happy"]]),
              GUS(900, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("It's Bia"), "wow"], [C("Pack light"), "shock"]]),
              PACK(1050, C("Gus grabs a little backpack"), scale=0.55, label="THE COST BACKPACK", labelUntil=C("Pack light", 2.0)),
              bub("WE HAVE THE POWER, THE METALS AND THE PEOPLE.", 1500, 230, C("We have the power"), until=C("Gus grabs"), tail=[1600, 560], size=24),
              bub("PACK LIGHT. YOU'LL SEE WHY.", 1500, 240, C("Pack light"), tail=[1600, 560]),
              tag((0, "STORY · FICTIONAL CAST"))]},
    sfx=[{"kind": "hit", "cue": "Pack light", "gain": 0.25}])

# ====================================================================== CHAPTER 2
bumper("s07_b2", "c2_card", "CHAPTER TWO", "The treasure chest", "Power, metals, food and customers", GREEN)
stage("s08_power", "c2_power", {
    **W1("brdam", wind=[[0, 0], [C("with wind turbines"), 1]], flow=[[0, 0], [C("A robot factory could run"), 1]]),
    "cam": cam((0, 900, 520, 0.9), (C("with wind turbines"), 700, 460, 1.0, 1.4), (C("In Brazil"), 1200, 500, 1.05, 1.4), (C("A robot factory could run"), 1600, 520, 1.05, 1.2),
               (C("We told Brazil's power story"), 960, 540, 0.9, 1.4)), "drift": 3,
    "items": [GUS(1500, 0.0, y=1040, scale=1.0, face="wow", pose="stand"), BIA(1720, 0.0, y=1040, scale=1.0, face="happy", pose="talk"),
              words("ALMOST 9 OF EVERY 10 UNITS: RENEWABLE", 960, 220, C("In Brazil"), size=50, until=C("A robot factory could run")),
              words("CLEAN POWER, DAY AND NIGHT", 960, 220, C("A robot factory could run"), size=56, until=C("We told Brazil's power story")),
              words("SEE: COULD CHEAP ELECTRICITY BECOME THE NEW OIL?", 960, 220, C("We told Brazil's power story"), size=38),
              tag((0, "STORY"), (C("In Brazil"), "FACT · EPE 2025: 86.8%"), (C("We told Brazil's power story"), "LIBRARY · EP 67"))]},
    sources=["epe_ben26"], sfx=[{"kind": "whoosh", "cue": "A robot factory could run", "gain": 0.25}])
stage("s09_iron", "c2_iron", {
    **W1("brmine", train=[[0, 0.6], [C("Huge trains roll"), 1.4]], plaque="MINAS GERAIS"),
    "cam": cam((0, 960, 520, 0.9), (C("Huge trains roll"), 900, 600, 1.05, 1.4), (C("Brazil is the second"), 560, 520, 1.1, 1.2), (C("Gus pulls up"), 1200, 560, 1.15, 1.2)), "drift": 3,
    "items": [GUS(1250, 0.0, y=1040, scale=1.0, face="wow", pose="stand", hold="phone", faces=[[0, "wow"], [C("And robots are mostly steel"), "grin"]]),
              BIA(1450, 0.0, y=1040, scale=1.0, face="happy", pose="stand"),
              words("IRON ORE: WORLD #2 PRODUCER", 960, 220, C("Brazil is the second"), size=56, until=C("Gus pulls up")),
              bub("AND ROBOTS ARE MOSTLY STEEL.", 1250, 360, C("And robots are mostly steel"), tail=[1250, 640], size=28),
              tag((0, "STORY"), (C("Brazil is the second"), "FACT · USGS 2026"))]},
    sources=["usgs_fe26"], sfx=[{"kind": "whoosh", "cue": "Huge trains roll", "gain": 0.25}])
stage("s10_nb", "c2_niobium", {
    **W1("brmine", train=0.3, jar=C("a tiny jar"), plaque="ARAXÁ · NIOBIUM"),
    "cam": cam((0, 1100, 560, 1.0), (C("a tiny jar"), 1040, 600, 1.25, 1.2), (C("And Brazil mines"), 960, 540, 0.95, 1.4), (C("Gus nearly drops"), 1180, 580, 1.2, 0.8),
               (C("Bia grins"), 1000, 560, 1.1, 1.2)), "drift": 2,
    "items": [GUS(1250, 0.0, y=1040, scale=1.0, face="squint", pose="stand", faces=[[0, "squint"], [C("And Brazil mines"), "wow"], [C("Gus nearly drops"), "shock"]], takes=[C("Gus nearly drops", 0.2)]),
              BIA(820, 0.0, y=1040, scale=1.0, face="happy", pose="talk", faces=[[0, "happy"], [C("Bia grins"), "grin"]]),
              words("A PINCH MAKES STEEL STRONGER AND LIGHTER", 960, 220, C("A pinch of it"), size=46, until=C("And Brazil mines")),
              words("NIOBIUM: BRAZIL ≈ 9 OF EVERY 10 TONS", 960, 220, C("And Brazil mines"), size=52, until=C("Gus nearly drops")),
              bub("YOU HAVE ALMOST ALL OF IT?", 1250, 330, C("You have almost all of it"), until=C("Bia grins"), tail=[1250, 620]),
              bub("MOST OF IT: ONE MINE IN MY STATE.", 820, 330, C("Most of it comes from"), tail=[820, 620], size=28),
              tag((0, "STORY"), (C("And Brazil mines"), "FACT · USGS 2026: ≈93%"))]},
    sources=["usgs_nb26", "cbmm"], sfx=[{"kind": "hit", "cue": "Gus nearly drops", "gain": 0.3}])
stage("s11_magnets", "c2_magnets", {
    **W1("svmine", variant="outback", trucks=1, stock=[[0, 0], [C("lithium for batteries"), 10]], plaque="JEQUITINHONHA VALLEY · LITHIUM"),
    "cam": cam((0, 960, 520, 0.9), (C("Brazil has the second"), 900, 520, 1.0, 1.4), (C("And in the Jequitinhonha Valley"), 1100, 560, 1.1, 1.4)), "drift": 3,
    "items": [words("MOTORS NEED RARE-EARTH MAGNETS", 960, 220, C("Robots also need motors"), size=52, until=C("Brazil has the second")),
              words("RARE-EARTH RESERVES: WORLD #2", 960, 220, C("Brazil has the second"), size=56, until=C("though today it barely")),
              words("IN THE GROUND, BARELY MINED YET", 960, 220, C("though today it barely"), size=52, until=C("And in the Jequitinhonha Valley")),
              words("LITHIUM: ALREADY SHIPPING", 960, 220, C("And in the Jequitinhonha Valley"), size=56),
              GUS(1500, 0.0, y=1040, scale=0.95, face="wow", pose="stand"),
              tag((0, "FACT · USGS 2026"), (C("And in the Jequitinhonha Valley"), "FACT · USGS 2026 (LITHIUM)"))]},
    sources=["usgs_ree26", "usgs_li26"])
board("p12_draw", "c2_draw", "The treasure map", "Let me draw the treasure map", [
    S("M 900 330 Q 1020 300 1150 340 Q 1330 380 1420 480 Q 1460 560 1380 640 Q 1320 720 1250 800 Q 1180 900 1100 930 Q 1050 880 1060 800 Q 1000 700 940 640 Q 860 560 840 470 Q 840 380 900 330 Z",
      "accent3", C("Here's Brazil"), width=7, fill="accent3", fillOpacity=0.12, label=lbl("BRAZIL (STYLIZED)", 1140, 290, 28, "accent3")),
    S("M 920 420 Q 1000 440 1080 420 Q 1160 400 1230 430", "accent2", C("Rivers and wind"), width=8, label=lbl("POWER", 1080, 470, 24, "accent2")),
    S(dot(1250, 690), "risk", C("Iron in the hills"), width=14, label=lbl("IRON", 1330, 700, 26, "risk")),
    S(dot(1200, 740), "ink", C("Niobium"), width=14, label=lbl("NIOBIUM", 1110, 760, 24, "ink")),
    S(dot(1290, 610), "accent", C("Rare earths and lithium"), width=14, label=lbl("RARE EARTHS · LITHIUM", 1420, 580, 22, "accent")),
    S("M 980 560 L 1100 560 M 990 590 L 1110 590 M 1000 620 L 1120 620", "accent3", C("Farms"), width=6, label=lbl("FARMS", 1050, 660, 24, "accent3")),
    S(dot(1230, 800), "accent2", C("big cities"), width=16, label=lbl("CUSTOMERS", 1330, 830, 24, "accent2")),
    S(rect(640, 930, 1020, 64), "ink", C("On paper"), width=5, kind="box", label=lbl("ON PAPER: ALMOST THE WHOLE RECIPE FOR A ROBOT", 1150, 972, 28, "ink")),
    S(dot(1150, 1020), "muted", C("Let me draw the treasure map"), width=1, label=lbl("STYLIZED MAP · NOT TO SCALE · NO FIGURES", 1150, 1020, 16, "muted")),
], [{"kind": "point", "at": C("Iron in the hills", 0.2), "dur": 1.2, "target": [1250, 690]}, {"kind": "point", "at": C("big cities", 0.2), "dur": 1.2, "target": [1230, 800]},
    {"kind": "react", "at": C("On paper", 0.4)}], enter_left=False)
stage("s13_food", "c2_food", {
    **W1("brfields", harvest=[[0, 0], [C("Fields of soybeans"), 0.1], [C("She texts back"), 0.9]], plaque="SOYBEANS TO THE HORIZON"),
    "cam": cam((0, 960, 520, 0.9), (C("Brazil is the world's biggest"), 900, 500, 1.0, 1.4), (C("Gus takes a photo"), 760, 580, 1.15, 1.2), (C("She texts back"), 900, 520, 1.0, 1.0)), "drift": 3,
    "items": [GUS(760, 0.0, y=1040, scale=1.0, face="happy", pose="stand", hold="phone", faces=[[0, "happy"], [C("She texts back"), "grin"]]),
              words("WORLD'S BIGGEST SOYBEAN EXPORTER", 960, 220, C("Brazil is the world's biggest"), size=54, until=C("Gus takes a photo")),
              bub("!!!!!!!", 1100, 330, C("She texts back"), tail=[820, 600], size=44),
              tag((0, "FACT · USDA FAS"))]},
    sources=["usda_soy"])
stage("s14_people", "c2_people", {
    **W1("brfab", arms=2, people=[[0, 2], [C("Brazilian companies make"), 5]], sign=[[0, "BRAZIL BUILDS HARD THINGS"], [C("Brazilian companies make"), "JETS · ELECTRIC MOTORS"]]),
    "cam": cam((0, 960, 520, 0.92), (C("Brazilian companies make"), 960, 480, 1.0, 1.4), (C("Bia studied"), 760, 580, 1.15, 1.2), (C("We don't just dig"), 900, 560, 1.1, 1.0)), "drift": 2,
    "items": [BIA(760, 0.0, y=1040, scale=1.05, face="happy", pose="talk", faces=[[0, "happy"], [C("We don't just dig"), "grin"]]),
              GUS(1100, 0.0, y=1040, scale=1.05, face="squint", pose="stand", faces=[[0, "squint"], [C("We build things too"), "wow"]]),
              words("PASSENGER JETS. MOTORS FOR EVERY CONTINENT.", 960, 380, C("Brazilian companies make"), size=46, until=C("Bia studied")),
              bub("WE DON'T JUST DIG THINGS UP. WE BUILD THINGS TOO.", 760, 330, C("We don't just dig"), tail=[760, 620], size=26),
              tag((0, "DESCRIPTIVE"))]})
stage("s15_market", "c2_market", {
    **W1("brcity", crowd=[[0, 0.3], [C("More than two hundred million"), 1]], plaque="A BIG HOME MARKET"),
    "cam": cam((0, 960, 520, 0.9), (C("More than two hundred million"), 960, 500, 0.95, 1.4), (C("Gus counts"), 900, 600, 1.15, 1.2), (C("So why isn't everyone"), 960, 560, 1.05, 1.0),
               (C("Let me show you the backpack"), 1150, 600, 1.2, WHIP)), "drift": 3,
    "items": [GUS(900, 0.0, y=1040, scale=1.0, face="happy", pose="stand", faces=[[0, "happy"], [C("So why isn't everyone"), "squint"]]),
              BIA(1150, 0.0, y=1040, scale=1.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Bia sighs"), "worry"]]),
              words("MORE THAN 200 MILLION PEOPLE", 960, 220, C("More than two hundred million"), size=58, until=C("Gus counts")),
              words("POWER · METAL · MAGNETS · FOOD · CUSTOMERS", 960, 220, C("Power, metal, magnets"), size=42, until=C("So why isn't everyone")),
              bub("SO WHY ISN'T EVERYONE HERE?", 900, 330, C("So why isn't everyone"), until=C("Bia sighs"), tail=[900, 620]),
              bub("LET ME SHOW YOU THE BACKPACK.", 1150, 330, C("Let me show you the backpack"), tail=[1150, 620], size=28),
              tag((0, "FACT · IBGE 2025"))]},
    sources=["ibge_pop25"], sfx=[{"kind": "whoosh", "cue": "Let me show you the backpack", "gain": 0.3}])

# ====================================================================== CHAPTER 3
bumper("s16_b3", "c3_card", "CHAPTER THREE", "The backpack", "One brick at every stop", ORANGE)
stage("s17_twist", "c3_twist", {
    **W1("brplant", busy=[[0, 0.6], [C("losing ground"), 0.0]], sign=[[0, "FACTORIES"], [C("losing ground"), "FACTORIES: LOSING GROUND"]]),
    "cam": cam((0, 960, 520, 0.9), (C("Today they make only"), 960, 480, 1.0, 1.4), (C("Gus looks around"), 760, 580, 1.15, 1.2), (C("Making things here"), 1100, 560, 1.1, 1.0)), "drift": 2,
    "items": [GUS(760, 0.0, y=1040, scale=1.0, face="squint", pose="stand", faces=[[0, "squint"], [C("With all this treasure"), "shock"]]),
              BIA(1100, 0.0, y=1040, scale=1.0, face="worry", pose="stand"),
              words("FACTORIES ≈ 1/8 OF THE ECONOMY", 960, 220, C("Today they make only"), size=56, until=C("Economists have")),
              words("DEINDUSTRIALIZATION", 960, 220, C("Economists have"), size=64, until=C("Gus looks around")),
              bub("WITH ALL THIS TREASURE?", 760, 330, C("With all this treasure"), until=C("Bia nods"), tail=[760, 620]),
              bub("MAKING THINGS HERE COSTS EXTRA.", 1100, 330, C("Making things here"), tail=[1100, 620], size=28),
              tag((0, "OUR CALC · IBGE 2025: 11.8% OF GDP"))]},
    sources=["ibge_cnt"])
stage("s18_tax", "c3_tax", {
    **W1("brcounter", sign="THE TAX COUNTER", stack=[[0, 0.1], [C("picks up taxes"), 0.5]]),
    "cam": cam((0, 960, 540, 0.92), (C("As a part moves"), 1100, 500, 1.05, 1.4), (C("like a snowball"), 960, 540, 1.0, 1.0), (C("The first brick"), 760, 600, 1.15, 1.0)), "drift": 2,
    "items": [GUS(620, 0.0, y=1040, scale=1.0, face="happy", pose="stand", faces=[[0, "happy"], [C("like a snowball"), "squint"], [C("The first brick"), "shock"]]),
              PACK(820, 0.0, drops=[[C("Thunk"), B_TAX]]),
              words("THE BILL TO PRODUCE CARRIES EXTRA WEIGHT", 960, 220, C("the bill to produce"), size=46, until=C("As a part moves")),
              words("TAX ON TOP OF TAX", 960, 220, C("some taxes land on top"), size=62, until=C("Even the power bill")),
              words("SEE: THE NEW OIL EPISODE (EP 67)", 960, 220, C("Even the power bill"), size=44, until=C("Thunk")),
              tag((0, "MECHANISM · IN PLAIN TERMS"), (C("Even the power bill"), "LIBRARY · EP 67"))]},
    sources=["br_reform"], sfx=[THUD("Thunk")])
stage("s19_paper", "c3_paper", {
    **W1("brcounter", sign="THE PAPERWORK", stack=[[0, 0.5], [C("famous for being thick"), 1.0]], rush=[[0, 1], [C("spent more hours"), 6]]),
    "cam": cam((0, 960, 520, 0.9), (C("spent more hours"), 1000, 480, 1.05, 1.4), (C("Another brick"), 760, 600, 1.15, 1.0)), "drift": 2,
    "items": [GUS(620, 0.0, y=1040, scale=1.0, face="squint", pose="stand", faces=[[0, "squint"], [C("Another brick"), "worry"]]),
              PACK(820, 0.0, base=[B_TAX], drops=[[C("Thunk"), B_PAPER]]),
              words("MOST HOURS ON TAX FORMS ON EARTH", 960, 220, C("spent more hours"), size=52, until=C("Thunk")),
              tag((0, "FACT · WORLD BANK DOING BUSINESS 2020 (LAST EDITION)"))]},
    sources=["wb_db20"], sfx=[THUD("Thunk")])
stage("s20_truck", "c3_truck", {
    **W1("brroad", trucks=[[0, 2], [C("ride on trucks"), 10]], rail=[[0, 0], [C("trains and ships"), 1]]),
    "cam": cam((0, 960, 520, 0.9), (C("ride on trucks"), 900, 560, 1.0, 1.4), (C("trains and ships"), 960, 460, 0.95, 1.2), (C("Another brick"), 700, 600, 1.15, 1.0)), "drift": 3,
    "items": [GUS(560, 0.0, y=1040, scale=1.0, face="worry", pose="stand", faces=[[0, "worry"], [C("Gus starts to sweat"), "panic"]]),
              PACK(760, 0.0, base=[B_TAX, B_PAPER], drops=[[C("Thunk"), B_TRUCK]]),
              words("≈ 2 OF EVERY 3 TONS GO BY TRUCK", 960, 220, C("about two of every three"), size=54, until=C("Over distances")),
              words("FEWER TRAINS AND SHIPS", 960, 220, C("Over distances"), size=56, until=C("Thunk")),
              tag((0, "INDUSTRY STUDY · CNT 2026: 65.8%"))]},
    sources=["cnt_plan26", "wb_lpi23"], sfx=[THUD("Thunk")])
stage("s21_credit", "c3_credit", {
    **W1("brbank", rate=[[0, 0.3], [C("almost fourteen percent"), 0.92]], rateText=""),
    "cam": cam((0, 960, 520, 0.9), (C("almost fourteen percent"), 960, 460, 1.05, 1.2), (C("So every loan"), 960, 540, 0.95, 1.2), (C("Gus's knees wobble"), 700, 600, 1.15, 1.0)), "drift": 2,
    "items": [GUS(560, 0.0, y=1040, scale=1.0, face="worry", pose="stand", faces=[[0, "worry"], [C("Gus's knees wobble"), "panic"]], takes=[C("Gus's knees wobble", 0.1)]),
              PACK(760, 0.0, base=[B_TAX, B_PAPER, B_TRUCK], drops=[[C("Thunk"), B_LOAN]]),
              words("CENTRAL BANK RATE: ≈ 14%", 960, 220, C("almost fourteen percent"), size=60, until=C("So every loan")),
              words("EVERY LOAN COSTS MORE", 960, 220, C("So every loan"), size=60, until=C("Thunk")),
              tag((0, "FACT · BANCO CENTRAL: 13.75% (NOV 2026)"))]},
    sources=["bcb_selic"], sfx=[THUD("Thunk")])
stage("s22_total", "c3_total", {
    **W1("brcity", crowd=0.6, plaque="THE CUSTO BRASIL"),
    "cam": cam((0, 960, 540, 0.92), (C("put the extra cost"), 960, 480, 1.0, 1.4), (C("Gus sits down"), 960, 600, 1.15, 1.2)), "drift": 2,
    "items": [GUS(860, 0.0, y=1040, scale=1.0, face="panic", pose="stand", poses=[[0, "stand"], [C("Gus sits down"), "sit"]], faces=[[0, "panic"], [C("Or, it sits down on him"), "dizzy"]]),
              PACK([[0, 1060], [C("Gus sits down"), 1060], [C("Or, it sits down on him"), 900]], 0.0, scale=[[0, 0.75], [C("the backpack has a name"), 1.0]],
                   base=[B_TAX, B_PAPER, B_TRUCK, B_LOAN]),
              words("THE COST OF BRAZIL", 960, 220, C("the backpack has a name"), size=62, until=C("put the extra cost")),
              words("≈ $300 BILLION A YEAR", 960, 220, C("put the extra cost"), size=66, until=C("Gus sits down")),
              tag((0, "INDUSTRY ESTIMATE · MBC/MDIC (2023) · R$1.7 TN ≈ US$304 BN"))]},
    sources=["mbc_custo", "fed_g5a"], sfx=[{"kind": "hit", "cue": "Or, it sits down on him", "gain": 0.35}])
board("p23_draw", "c3_draw", "What robots remove, and what they don't", "Let me draw it", [
    S(rect(560, 300, 340, 620), "ink", C("Let me draw it"), width=6, kind="box", label=lbl("THE BACKPACK", 730, 280, 28, "ink")),
    S(rect(580, 320, 300, 100), "risk", C("Robots take the wage brick"), width=4, fill="risk", fillOpacity=0.3, kind="bar", label=lbl("WAGES", 730, 382, 28, "ink")),
    S(arrow((900, 360), (1200, 330), -0.2), "risk", C("out of the backpack"), width=6, kind="arrow", label=lbl("ROBOTS TAKE THIS OUT", 1250, 300, 26, "risk")),
    S(rect(580, 440, 300, 100), "muted", C("the tax brick"), width=4, fill="muted", fillOpacity=0.3, kind="bar", label=lbl("TAXES", 730, 502, 28, "ink")),
    S(rect(580, 560, 300, 100), "muted", C("the truck brick"), width=4, fill="muted", fillOpacity=0.3, kind="bar", label=lbl("TRUCKS", 730, 622, 28, "ink")),
    S(rect(580, 680, 300, 100), "muted", C("the loan brick"), width=4, fill="muted", fillOpacity=0.3, kind="bar", label=lbl("LOANS", 730, 742, 28, "ink")),
    S(rect(1150, 560, 500, 240), "accent2", C("mostly expensive machines"), width=5, kind="box", label=lbl("ROBOT FACTORY = MACHINES ON CREDIT", 1400, 690, 26, "accent2")),
    S(rect(580, 680, 300, 200), "risk", C("the loan brick gets heavier"), width=6, kind="box", label=lbl("LOANS GET HEAVIER", 730, 900, 26, "risk")),
    S(rect(1030, 860, 740, 60), "ink", C("Robots make Brazil's treasure"), width=5, kind="box", label=lbl("TREASURE WORTH MORE · BACKPACK HURTS MORE", 1400, 900, 24, "ink")),
    S(dot(1150, 1010), "muted", C("Let me draw it"), width=1, label=lbl("MECHANISM · OUR ANALYSIS · ILLUSTRATIVE", 1150, 1010, 16, "muted")),
], [{"kind": "point", "at": C("Robots take the wage brick", 0.3), "dur": 1.4, "target": [730, 370]}, {"kind": "point", "at": C("the loan brick gets heavier", 0.3), "dur": 1.4, "target": [730, 780]},
    {"kind": "react", "at": C("Robots make Brazil's treasure", 0.3)}])

# ====================================================================== CHAPTER 4
bumper("s24_b4", "c4_card", "CHAPTER FOUR", "Lightening the load", "A reform, a factory, a scale", TEAL)
stage("s25_reform", "c4_reform", {
    **W1("brcounter", sign="NEW: A SIMPLER SALES TAX", stack=[[0, 1.0], [C("A pile of old taxes"), 1.0], [C("built so that taxes stop"), 0.3]], rush=0.5),
    "cam": cam((0, 960, 540, 0.92), (C("A pile of old taxes"), 1000, 480, 1.05, 1.4), (C("Bia pulls the first brick"), 820, 600, 1.15, 1.2)), "drift": 2,
    "items": [GUS(620, 0.0, y=1040, scale=1.0, face="worry", pose="stand", faces=[[0, "worry"], [C("It's already a little lighter"), "happy"]]),
              PACK(820, 0.0, base=[B_TAX, B_PAPER, B_TRUCK, B_LOAN], pulls=[C("Bia pulls the first brick", 0.4)]),
              BIA(1080, 0.0, y=1040, scale=1.0, face="happy", pose="talk", faces=[[0, "happy"], [C("See?"), "grin"]]),
              words("BIGGEST SALES-TAX CHANGE IN DECADES", 960, 220, C("It recently passed"), size=50, until=C("A pile of old taxes")),
              words("NO MORE TAX ON TOP OF TAX", 960, 220, C("built so that taxes stop"), size=58, until=C("Bia pulls")),
              bub("SEE? ALREADY A LITTLE LIGHTER.", 1080, 330, C("See?"), tail=[1080, 620], size=28),
              tag((0, "FACT · EC 132/2023 · LC 214/2025"))]},
    sources=["br_reform"], sfx=[{"kind": "whoosh", "cue": "Bia pulls the first brick", "gain": 0.3}])
stage("s26_slow", "c4_slow", {
    **W1("brcounter", sign="TEST RUN: STARTED", stack=0.3, rush=[[0, 1], [C("Gus checks his calendar"), 8]]),
    "cam": cam((0, 960, 540, 0.92), (C("the old taxes don't fully"), 1100, 460, 1.05, 1.2), (C("Gus checks his calendar"), 760, 600, 1.15, 1.2)), "drift": 2,
    "items": [GUS(700, 0.0, y=1040, scale=1.0, face="squint", pose="stand", hold="phone", faces=[[0, "squint"], [C("That's a long time"), "deadpan"]]),
              PACK(900, 0.0, base=[B_PAPER, B_TRUCK, B_LOAN]),
              words("OLD TAXES FULLY GONE: 2033", 960, 220, C("the old taxes don't fully"), size=60, until=C("Gus checks")),
              bub("THAT'S A LONG TIME TO CARRY A BACKPACK.", 700, 330, C("That's a long time"), tail=[700, 620], size=26),
              tag((0, "FACT · LC 214/2025 TIMETABLE"))]},
    sources=["br_reform"])
stage("s27_ford", "c4_ford", {
    **W1("brplant", busy=[[0, 0.8], [C("The halls went quiet"), 0], [C("took over the site"), 0], [C("began building cars"), 1]],
         sign=[[0, "CAMAÇARI, BAHIA"], [C("The halls went quiet"), "CLOSED"], [C("took over the site"), "NEW OWNER: BYD"]]),
    "cam": cam((0, 960, 520, 0.9), (C("The halls went quiet"), 960, 540, 1.0, 1.4), (C("began building cars"), 1200, 560, 1.05, 1.2), (C("Brazil has also passed"), 960, 520, 0.92, 1.4)), "drift": 2,
    "items": [GUS(400, 0.0, y=1040, scale=0.95, face="happy", pose="stand", faces=[[0, "happy"], [C("The halls went quiet"), "worry"], [C("began building cars"), "wow"]]),
              words("FORD LEFT", 960, 220, C("Ford closed"), size=62, until=C("Then a Chinese carmaker")),
              words("A NEW OWNER · CARS AGAIN FROM 2025", 960, 220, C("began building cars"), size=50, until=C("Brazil has also passed")),
              words("PLUS: A TAX DEAL FOR CLEAN-POWER DATA CENTERS", 960, 220, C("Brazil has also passed"), size=40),
              tag((0, "FACT · COMPANY ANNOUNCEMENTS"), (C("Brazil has also passed"), "FACT · LAW 15,504/2026 · SEE EP 67"))]},
    sources=["byd_ba", "redata26"], sfx=[{"kind": "whoosh", "cue": "began building cars", "gain": 0.3}])
stage("s28_case", "c4_case", {
    **W1("txscale", title="BRAZIL ON THE SCALE", pro=[[0, ""], [C("The good reason"), "ROBOTS RAISE THE VALUE OF POWER AND METALS"]],
         con=[[0, ""], [C("The catch"), "THE BACKPACK: TAXES, TRUCKS, LOANS"]],
         tilt=[[0, 0], [C("The good reason"), 0], [C("The good reason", 0.8), -0.7], [C("The catch"), -0.7], [C("The catch", 0.8), 0.55]]),
    "cam": cam((0, 960, 540, 0.95), (C("The good reason"), 760, 520, 1.05, 1.2), (C("The catch"), 1160, 520, 1.05, 1.2), (C("the rivals carry"), 960, 540, 0.95, 1.2)), "drift": 1,
    "items": [PACK(1740, 0.0, y=1040, scale=0.5, base=[B_PAPER, B_TRUCK, B_LOAN]),
              BIA(220, 0.0, y=1040, scale=0.8, face="happy", pose="stand", faces=[[0, "happy"], [C("The catch"), "worry"]]),
              tag((0, "OUR ANALYSIS · ONE ARGUMENT FOR, THE OBSTACLES"))]},
    sfx=[{"kind": "whoosh", "cue": "The good reason", "gain": 0.25}, {"kind": "hit", "cue": "The catch", "gain": 0.25}])
stage("s29_rivals", "c4_rivals", {
    **W1("brhq", spin=1.2, screen=[[0, "OTHER BIDS"], [C("Mexico sits"), "MEXICO: NEXT DOOR"], [C("China already installs"), "CHINA: THE MOST ROBOTS"],
                                   [C("And America is paying"), "USA: BRING IT HOME"], [C("Gus's phone keeps"), "3 NEW OFFERS"]]),
    "cam": cam((0, 1200, 480, 1.0), (C("Mexico sits"), 1340, 420, 1.1, 1.2), (C("Gus's phone keeps"), 900, 600, 1.15, 1.2)), "drift": 2,
    "items": [GUS(900, 0.0, y=1040, scale=1.0, face="squint", pose="stand", hold="phone", faces=[[0, "squint"], [C("Gus's phone keeps"), "panic"]], takes=[C("Gus's phone keeps", 0.3), C("Gus's phone keeps", 1.2)]),
              bub("BZZT! BZZT!", 1060, 380, C("Gus's phone keeps"), tail=[960, 640]),
              tag((0, "DESCRIPTIVE"), (C("China already installs"), "FACT · IFR"))]},
    sources=["ifr_cn"])

# ====================================================================== CHAPTER 5
bumper("s30_b5", "c5_card", "CHAPTER FIVE", "So, could Brazil?", "The treasure is real. So is the backpack.", PURPLE)
stage("s31_verdict", "c5_verdict", {
    **W2("brdam", "brroad", {"wind": 1, "flow": 1}, {"trucks": [[0, 8], [C("If the reform really lightens"), 3]], "rail": [[0, 0], [C("roads, rails and loans"), 1]]}),
    "cam": cam((0, 960, 520, 0.9), (C("Brazil has ingredients"), 1200, 500, 1.0, 1.4), (C("But ingredients don't build"), OX + 960, 520, 0.92, WHIP),
               (C("If the reform really lightens"), OX + 900, 540, 1.0, 1.4), (C("If not"), OX + 1500, 480, 1.05, 1.4)), "drift": 2,
    "items": [words("IT COULD. BUT NOT WITH THIS BACKPACK.", 960, 220, C("The honest answer"), size=50, until=C("Brazil has ingredients")),
              words("RARE INGREDIENTS · ROBOTS MAKE THEM MATTER MORE", 960, 220, C("Brazil has ingredients"), size=40, until=C("But ingredients don't build")),
              words("INGREDIENTS DON'T BUILD FACTORIES. COSTS DO.", OX + 960, 220, C("But ingredients don't build"), size=44, until=C("If the reform really lightens")),
              words("LIGHTER BACKPACK → A BIG WINNER", OX + 960, 220, C("If the reform really lightens"), size=50, until=C("If not")),
              words("OR THE METALS SAIL AWAY", OX + 960, 220, C("If not"), size=56),
              tag((0, "VERDICT · OUR ANALYSIS (CONDITIONAL, NOT A FORECAST)"))]},
    sfx=[{"kind": "whoosh", "cue": "But ingredients don't build", "gain": 0.3}])
stage("s32_end", "c5_end", {
    **W1("brgate", plane=[[0, 0.1], [C("Bia waves goodbye"), 0.5]], board="REPORT: BRAZIL, ON THE SHORTLIST"),
    "cam": cam((0, 960, 560, 0.95), (C("Brazil, on the shortlist"), 1400, 420, 1.1, 1.2), (C("Bia waves goodbye"), 900, 600, 1.05, 1.2), (C("Gus takes both"), 760, 600, 1.2, 1.0)), "drift": 2,
    "items": [GUS(760, 0.0, y=1040, scale=1.0, face="happy", pose="stand", hold="clipboard", faces=[[0, "happy"], [C("Gus takes both"), "grin"]]),
              PACK(560, 0.0, y=1040, scale=0.6, base=[B_PAPER, B_TRUCK, B_LOAN]),
              BIA(1150, 0.0, y=1040, scale=1.0, face="happy", pose="talk", hold="coffee"),
              words("THE TREASURE IS REAL. SO IS THE BACKPACK.", 960, 220, C("The treasure is real"), size=46, until=C("Bia waves goodbye")),
              bub("LEAVE THE BACKPACK. TAKE THE COFFEE.", 1150, 330, C("Leave the backpack here"), until=C("Gus takes both"), tail=[1150, 620], size=26),
              tag((0, "STORY"))]})
add("s33_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s34_button", "button", {
    **W1("brgate", plane=0.9, board="NOW BOARDING"),
    "cam": cam((0, 960, 600, 1.1), (3.0, 1000, 600, 1.2, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [GUS([[0, 400], [2.4, 1000]], 0.0, y=1040, scale=1.0, face="happy", pose="stand", hold="coffee", faces=[[0, "happy"], [3.2, "shock"]]),
              PACK([[0, 600], [2.4, 1200]], 0.0, y=1040, scale=0.6, base=[B_TRUCK, B_LOAN], drops=[[3.2, "SOUVENIRS"]]),
              bub("WAIT. WHO PACKED SOUVENIRS?", 1000, 330, 3.6, tail=[1000, 620], size=28)]},
    sfx=[{"kind": "hit", "at": 3.2, "gain": 0.35}])

TIGHT = {"txscale", "brcounter", "brbank"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "PROJECTION": "gold", "OUR": "gold", "INDUSTRY": "gold", "ESTIMATE": "gold", "FINDING": "green", "VERDICT": "gold", "LIBRARY": "white"}
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

write(OUT, "# GENERATED by tools/gen_brazilai_storyboard.py; edit the generator, not this file.\n"
           "# Episode 71 storyboard (Could Brazil Become the World's Factory for Robots?): bespoke worlds in CartoonStage/brazil.tsx.\n")

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
