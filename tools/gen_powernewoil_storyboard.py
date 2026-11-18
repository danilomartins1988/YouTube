"""Generates projects/could-cheap-electricity-become-the-new-oil/deliverables/documentary/storyboard.yaml
(Episode 67: Could Cheap Electricity Become the New Oil?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/powermap.tsx (pmoffice, pmmap, pmoil, pmsmelter, pmnorth, pmsun, pmtropic, pmqueue,
pmscore, pmtitle, pmbumper; items pmtag, cubby). Story over statistics: one protagonist (NIA, a site scout, fictional) and CUBBY
(the walking scale model of the campus she must find a home for). No real person is drawn; companies are named in narration and
shown only as generic buildings or plain plaques; no logos, no flags.
Signature animations: 1 oil ships, power doesn't (s06 + p07 board), 2 the smelter that eats a river (s09-s11), 3 the pin-by-pin
tour (s14-s22), 4 the line at the plug (s18, s25, s26), 5 one world market vs many local ones (p30 board).
Presenter boards: p07 why the factory goes to the energy, p24 the real price stack, p30 oil's one market vs power's many.
Every number carries a pmtag pill: FACT / FORECAST / PLAN / PROPOSED / OUR CALC / FINDING / ANALYSIS / STORY / LIBRARY.
Run: python tools/gen_powernewoil_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "could-cheap-electricity-become-the-new-oil"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#1E88E5", "#F5B700", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#16223A", "#F08A24"
OX = 3400  # offset for a second zone
# map pins (pmmap canvas)
PINS = [{"x": 1010, "y": 205, "label": "NORWAY", "c": BLUE}, {"x": 880, "y": 225, "label": "ICELAND", "c": TEAL},
        {"x": 560, "y": 290, "label": "QUEBEC", "c": GREEN}, {"x": 420, "y": 400, "label": "TEXAS", "c": ORANGE},
        {"x": 1180, "y": 440, "label": "THE GULF", "c": GOLD}, {"x": 690, "y": 600, "label": "BRAZIL", "c": GREEN}]


def NIA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=6, skin=3, hair=2, hairStyle=4, color=TEAL, glasses=False, scarf=GOLD, **kw)


def LOCAL(x=None, at=0.0, v=9, color=BLUE, **kw):
    kw.setdefault("scale", 1.1)
    return it("toon", x=x, at=at, who="shopper", v=v, skin=(v * 3) % 6, hair=(v * 5) % 7, hairStyle=v % 6, color=color, glasses=v % 2 == 0, **kw)


def CUB(x, at=0.0, **kw):
    kw.setdefault("y", 860)
    kw.setdefault("scale", 0.75)
    return it("cubby", x=x, at=at, **kw)


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
    stage(id_, seg, {**W1("pmbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.2, "items": [CUB([[0, 2300], [1.4, 1640]], 1.0, y=1010, scale=0.7, face="happy", hops=[2.2])]},
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


# ====================================================================== CHAPTER 1: follow the plug
stage("s01_hook", "co_hook", {
    **W2("pmoffice", "pmoil", {"screen": [[0, "NEW AI CAMPUS: FIND IT A HOME"], [C("Look for the plug"), "RULE 1: FOLLOW THE PLUG"]]},
         {"focus": "oil", "pump": 1.4, "ship": [[0, 0], [C("A century ago"), 0], [C("Now Nia is hunting"), 0.7]]}),
    "cam": cam((0, 700, 560, 1.15), (C("An AI company"), 1300, 500, 0.95, 1.4), (C("Her boss gives her"), 760, 560, 1.2, 1.0),
               (C("This place will drink"), 1100, 520, 0.9, 1.4), (C("A century ago"), OX + 700, 520, 0.95, WHIP),
               (C("Now Nia is hunting"), OX + 1200, 520, 0.85, 1.6), (C("So could"), OX + 960, 520, 0.8, 1.4)), "drift": 3,
    "items": [NIA([[0, -200], [1.6, 420]], 0.0, face="happy", pose="stand", hold="phone", faces=[[0, "happy"], [C("Her boss gives her"), "squint"], [C("Look for the plug"), "grin"]],
                  label="NIA · SITE SCOUT (FICTIONAL)", labelUntil=C("An AI company")),
              bub("FIND IT A HOME?", 480, 300, C("has to find it a home"), until=C("Her boss gives her"), tail=[440, 560], size=30),
              bub("DON'T LOOK FOR WORKERS. LOOK FOR THE PLUG.", 900, 260, C("Her boss gives her"), until=C("This place will drink"), tail=[600, 560], size=26),
              words("AS MUCH POWER AS A CITY. 24/7.", 1000, 220, C("This place will drink"), size=50, until=C("A century ago")),
              words("1900s: FOLLOW THE OIL", OX + 700, 230, C("A century ago"), size=56, until=C("Now Nia is hunting")),
              words("2020s: FOLLOW THE PLUG?", OX + 1300, 230, C("Now Nia is hunting"), size=56, until=C("So could")),
              words("THE NEW OIL?", OX + 960, 220, C("So could"), size=72),
              tag((0, "STORY · FICTIONAL CAST"), (C("A century ago"), "ANALYSIS"))]},
    sfx=[{"kind": "whoosh", "cue": "A century ago", "gain": 0.3}, {"kind": "hit", "cue": "So could", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("pmtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [CUB([[0, -200], [2.2, 300]], 1.6, y=1010, scale=0.7, face="happy", hops=[3.4])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_cubby", "c1_cubby", {
    **W1("pmoffice", screen=[[0, "CAMPUS MODEL: CUBBY"], [C("What it needs"), "NEEDS: POWER, 24/7, FOR YEARS"]]),
    "cam": cam((0, 760, 560, 1.1), (C("They call it Cubby"), 900, 600, 1.25, 1.0), (C("Once it's built"), 1100, 540, 0.95, 1.4), (C("What it needs"), 1250, 480, 1.0, 1.2)), "drift": 3,
    "items": [NIA(420, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("They call it Cubby"), "grin"]]),
              CUB([[0, 2000], [C("the team gave Nia"), 2000], [C("They call it Cubby"), 860]], 0.0, face="happy", faces=[[0, "happy"], [C("and into heat"), "wow"]],
                  hops=[C("They call it Cubby", 1.0)], label="CUBBY · CAMPUS MODEL (FICTIONAL)", labelUntil=C("Once it's built")),
              bub("HI! I'M A BUILDING.", 900, 330, C("They call it Cubby", 0.6), until=C("Cubby is a building"), tail=[880, 640], size=30),
              words("ELECTRICITY IN → ANSWERS + HEAT OUT", 960, 220, C("Cubby is a building"), size=46, until=C("Once it's built")),
              words("FEW PEOPLE. HUGE POWER.", 1100, 220, C("Once it's built"), size=58),
              tag((0, "STORY · FICTIONAL CAST"), (C("Cubby is a building"), "MECHANISM"))]})
stage("s04_list", "c1_list", {
    **W1("pmoffice", screen=[[0, "CHECKLIST FROM THE BOSS"]], shown=[[0, 0], [C("Cheap power"), 0], [C("Cheap power", 0.4), 1], [C("Lots of it"), 2], [C("Ready soon"), 3],
                                                              [C("Cool enough"), 4], [C("Close enough"), 5], [C("And a government"), 6]]),
    "cam": cam((0, 1200, 560, 0.95), (C("Cheap power"), 1340, 600, 1.15, 1.2), (C("Nia looks at the list"), 900, 560, 1.0, 1.2), (C("That's not a building site"), 700, 600, 1.2, 1.0)), "drift": 2,
    "items": [NIA(560, 0.0, face="squint", pose="stand", hold="phone", faces=[[0, "squint"], [C("Nia looks at the list"), "worry"], [C("That's a treasure map"), "grin"]]),
              CUB(860, 0.0, face="happy", faces=[[0, "happy"], [C("That's a treasure map"), "wow"]], hops=[C("That's a treasure map", 0.4)]),
              bub("THAT'S A TREASURE MAP.", 640, 300, C("That's a treasure map"), tail=[600, 560], size=32),
              tag((0, "STORY"))]})
stage("s05_demand", "c1_demand", {
    **W1("pmmap", pins=[{"x": 1660, "y": 300, "label": "JAPAN (TODAY)", "c": PURPLE, "at": 0.0}], hi=[[C("all of Japan"), 0]]),
    "cam": cam((0, 960, 540, 1.0), (C("all of Japan"), 1500, 470, 1.2, 1.2), (C("That's a whole new"), 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [CUB([[0, -300], [2.6, 360]], 0.0, y=1000, scale=0.6, face="happy"), CUB([[0, -500], [3.0, 520]], 0.4, y=1010, scale=0.5, face="happy"),
              CUB([[0, -700], [3.4, 670]], 0.8, y=1000, scale=0.55, face="happy"), CUB([[0, -900], [3.8, 810]], 1.2, y=1010, scale=0.45, face="wow"),
              CUB([[0, -1100], [4.2, 940]], 1.6, y=1000, scale=0.5, face="happy"),
              words("2030 FORECAST: DATA CENTERS ≈ ALL OF JAPAN", 960, 200, C("all of Japan"), size=46, until=C("That's a whole new")),
              words("A NEW INDUSTRIAL COUNTRY. WHERE DOES IT PLUG IN?", 960, 200, C("That's a whole new"), size=42),
              tag((0, "STORY"), (C("The International Energy Agency"), "FORECAST · IEA ENERGY AND AI"))]},
    sources=["iea_eai25"])
stage("s06_oil", "c1_oil", {
    **W1("pmoil", focus="oil", pump=1.2, ship=[[0, 0], [C("Refineries rose"), 0], [C("Nia wonders"), 0.8]], oilText="1900s: OIL BUILT BOOMTOWNS"),
    "cam": cam((0, 400, 540, 1.0), (C("which ports got busy"), 700, 560, 1.15, 1.4), (C("Refineries rose"), 900, 540, 0.9, 1.4), (C("Nia wonders"), 1300, 520, 0.85, 1.6)), "drift": 3,
    "items": [LOCAL(140, 0.0, v=3, color=ORANGE, face="grin", pose="stand"), LOCAL(260, 0.4, v=8, color=BLUE, face="happy", pose="stand"),
              words("OIL REDREW THE MAP", 700, 220, C("We've seen a map"), size=58, until=C("Nia wonders")),
              NIA([[0, 2300], [C("Nia wonders"), 2300], [C("Nia wonders", 1.6), 1500]], 0.0, face="squint", pose="stand"),
              bub("WILL POWER REDRAW IT?", 1500, 320, C("Nia wonders", 1.0), tail=[1480, 560], size=30),
              tag((0, "ANALYSIS · HISTORY"))]})
board("p07_draw", "c1_draw", "Why the factory goes to the energy", "Let me draw why", [
    S("M 560 860 L 1780 860", "ink", C("Let me draw why")),
    S("M 600 640 Q 720 600 840 640 Q 960 680 1080 640", "accent2", C("Here's oil"), label=lbl("OCEAN", 840, 700, 24, "accent2")),
    S(rect(600, 560, 110, 50), "ink", C("Pump it into a tanker"), width=5, fill="ink", fillOpacity=0.85, kind="bar", label=lbl("OIL TANKER", 655, 540, 24, "ink")),
    S(arrow((720, 560), (1060, 560), -0.25), "ink", C("it crosses an ocean"), kind="arrow", label=lbl("SHIPS ANYWHERE", 890, 470, 26, "ink")),
    S("M 1240 860 L 1240 520 M 1480 860 L 1480 520 M 1720 860 L 1720 520", "muted", C("Now here's electricity")),
    S("M 1240 530 Q 1360 580 1480 530 Q 1600 580 1720 530", "accent", C("giant power lines"), width=6, label=lbl("YEARS TO BUILD", 1480, 490, 26, "accent")),
    S(rect(1580, 590, 180, 60), "risk", C("you lose some along the way"), kind="box", label=lbl("LOSSES", 1670, 630, 26, "risk")),
    S(rect(1180, 300, 560, 110), "risk", C("Nobody ships a waterfall"), width=6, kind="box", label=lbl("NOBODY SHIPS A WATERFALL", 1460, 368, 32, "risk")),
    S(arrow((900, 400), (1200, 760), 0.2), "accent3", C("the factory goes to the energy"), width=6, kind="arrow", label=lbl("FACTORY → ENERGY", 860, 380, 30, "accent3")),
    S(dot(1150, 940), "muted", C("Let me draw why"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NO FIGURES)", 1150, 940, 16, "muted")),
], [{"kind": "point", "at": C("it crosses an ocean", 0.3), "dur": 1.4, "target": [890, 560]}, {"kind": "point", "at": C("you lose some", 0.4), "dur": 1.4, "target": [1670, 620]},
    {"kind": "react", "at": C("Nobody ships a waterfall", 0.3)}])

# ====================================================================== CHAPTER 2: the metal made of electricity
bumper("s08_b2", "c2_card", "CHAPTER TWO", "The metal made of electricity", "It happened before", BLUE)
stage("s09_smelt", "c2_smelt", {
    **W1("pmsmelter", flow=1, ingots=[[0, 0], [C("Making a single ton"), 2], [C("That's why"), 8]], plaque="ALUMINUM SMELTER (ILLUSTRATIVE)"),
    "cam": cam((0, 900, 540, 0.9), (C("Meet aluminum"), 1100, 560, 1.1, 1.4), (C("massive electric current"), 700, 520, 1.0, 1.4),
               (C("Making a single ton"), 1500, 560, 1.2, 1.4), (C("That's why"), 1000, 520, 0.85, 1.4)), "drift": 3,
    "items": [it("toonwords", text="⚡ + ORE → METAL", x=900, y=220, at=C("massive electric current"), size=56, until=C("Making a single ton")),
              words("1 TON ≈ MORE THAN A YEAR OF A US HOME'S POWER", 1250, 220, C("Making a single ton"), size=42, until=C("That's why")),
              words("ALUMINUM = SOLID ELECTRICITY", 1000, 220, C("That's why"), size=60),
              NIA(300, C("Meet aluminum"), face="wow" if False else "shock", pose="stand", hold="coffee", faces=[[0, "happy"], [C("Making a single ton"), "shock"]]),
              tag((0, "FACT · ALUMINUM SMELTING"), (C("Making a single ton"), "OUR CALC · IAI + EIA"))]},
    sources=["iai_int", "eia_res"], sfx=[{"kind": "hit", "cue": "Making a single ton", "gain": 0.3}])
stage("s10_iceland", "c2_iceland", {
    **W1("pmsmelter", flow=[[0, 0], [C("Iceland built"), 1]], ore=[[0, 0], [C("Electricity in"), 0], [C("ships to the world"), 1]], ingots=[[0, 0], [C("metal out"), 6]],
         out=[[0, 0], [C("ships to the world"), 0], [C("Iceland's national"), 0.6]], plaque="ICELAND'S FIRST SMELTER (ILLUSTRATIVE)"),
    "cam": cam((0, 500, 540, 0.9), (C("Iceland built"), 200, 520, 1.1, 1.4), (C("Electricity in"), 900, 540, 0.95, 1.4), (C("ships to the world"), 1800, 600, 1.0, 1.4),
               (C("Iceland's national"), 900, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("1960s: A DAM BUILT FOR A SMELTER", 400, 220, C("Iceland built"), size=52, until=C("Electricity in")),
              words("POWER IN. METAL OUT.", 1100, 220, C("Electricity in"), size=60, until=C("Iceland's national")),
              words("MOST POWER → HEAVY INDUSTRY", 900, 220, C("Iceland's national"), size=54),
              NIA([[0, -300], [2.0, 120]], 0.0, face="happy", pose="stand"),
              tag((0, "FACT · LANDSVIRKJUN (BÚRFELL, 1969)"), (C("Iceland's national"), "FACT · LANDSVIRKJUN ≈ 85% TO INDUSTRY"))]},
    sources=["lv_burfell", "lv_cust"])
stage("s11_quebec", "c2_quebec", {
    **W1("pmsmelter", flow=1, ore=[[0, 0], [C("The ore sails in"), 1]], ingots=[[0, 4], [C("The metal sails out"), 12]], out=[[0, 0], [C("The metal sails out"), 0], [C("In a way"), 0.8]],
         plaque="QUEBEC SMELTER (GENERIC)"),
    "cam": cam((0, 1100, 520, 0.85), (C("almost all"), 600, 540, 1.0, 1.4), (C("The ore sails in"), 1900, 600, 1.0, 1.2), (C("The metal sails out"), 1700, 560, 1.1, 1.2),
               (C("In a way"), 700, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("CANADA MINES NO BAUXITE…", 1000, 220, 0.3, size=54, until=C("Yet it's one")),
              words("…BUT 9 OF ITS 10 SMELTERS ARE IN QUEBEC", 1000, 220, C("Yet it's one"), size=46, until=C("The ore sails in")),
              words("ORE IN →", 1900, 220, C("The ore sails in"), size=60, until=C("The metal sails out")),
              words("→ METAL OUT", 1700, 220, C("The metal sails out"), size=60, until=C("In a way")),
              words("EXPORTING RIVERS, ONE INGOT AT A TIME", 800, 220, C("In a way"), size=48),
              tag((0, "FACT · NATURAL RESOURCES CANADA"))]},
    sources=["nrcan_al"])
stage("s12_twist", "c2_twist", {
    **W1("pmnorth", variant="fjord", halls=[[0, 0], [C("A data center is a smelter"), 0], [C("Electricity goes in"), 3]], air=[[0, 0], [C("Answers come out"), 1]], snow=True),
    "cam": cam((0, 700, 520, 0.9), (C("A data center is a smelter"), 1300, 540, 1.0, 1.4), (C("And answers"), 1500, 520, 1.15, 1.4), (C("So Nia starts"), 900, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("A SMELTER FOR THE DIGITAL AGE", 1200, 220, C("A data center is a smelter"), size=56, until=C("And answers")),
              words("ANSWERS SHIP AT LIGHT SPEED", 1400, 220, C("And answers"), size=56, until=C("So Nia starts")),
              NIA([[0, -300], [C("So Nia starts"), -300], [C("So Nia starts", 1.8), 650]], 0.0, face="grin", pose="stand", hold="bag"),
              CUB([[0, -500], [C("So Nia starts"), -500], [C("So Nia starts", 2.0), 860]], 0.0, face="happy", carry="suitcase"),
              tag((0, "ANALYSIS · ANALOGY"))]})

# ====================================================================== CHAPTER 3: pin by pin
bumper("s13_b3", "c3_card", "CHAPTER THREE", "Pin by pin", "Six places that sell cheap power", GREEN)
stage("s14_map", "c3_map", {
    **W1("pmmap", pins=[{**p, "at": 0.4 + 0.35 * k} for k, p in enumerate(PINS)], fly=[[1.0, 2], [C("books a lot of flights"), 0]], strings=True, title="NIA'S PIN BOARD"),
    "cam": cam((0, 960, 540, 1.0), (C("books a lot of flights"), 900, 500, 1.15, 1.6), (C("one very excited"), 960, 560, 0.95, 1.4)), "drift": 2,
    "items": [NIA(260, 0.0, face="happy", pose="stand", hold="bag", scale=1.0), CUB(1720, C("one very excited"), y=1000, scale=0.6, face="wow", hops=[C("one very excited", 0.6)]),
              words("6 PINS. 1 SUITCASE.", 960, 200, C("Six pins"), size=60),
              tag((0, "STORY"))]})
stage("s15_norway", "c3_norway", {
    **W2("pmmap", "pmnorth", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 2], [0.4, 0]], "hi": [[0.4, 0]]},
         {"variant": "fjord", "halls": [[0, 0], [C("In the port town"), 0], [C("picked for hydropower"), 3]], "air": [[0, 0], [C("cool air"), 1]], "snow": True,
          "tenant": [[0, ""], [C("announced as Stargate Norway"), "STARGATE NORWAY (ANNOUNCED 2025)"], [C("the tenant changed"), "BIG CUSTOMER: MICROSOFT (2026)"]], "plaque": "NARVIK, NORWAY"}),
    "cam": cam((0, 1000, 400, 1.15), (C("Nearly all"), OX + 500, 520, 0.95, WHIP), (C("In the port town"), OX + 1300, 520, 1.0, 1.4), (C("the tenant changed"), OX + 1500, 560, 1.2, 1.2),
               (C("Norway's oil fortune"), OX + 900, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("≈ 9 IN 10 KWH FROM FALLING WATER", OX + 600, 220, C("Nearly all"), size=48, until=C("In the port town")),
              words("THE CUSTOMER CHANGED. THE PLUG DIDN'T.", OX + 1300, 220, C("The plug stayed"), size=48, until=C("Norway's oil fortune")),
              words("SEE: WHY NORWAY IS SO RICH", OX + 900, 220, C("Norway's oil fortune"), size=52),
              NIA(OX + 700, C("Nearly all"), face="happy", pose="stand", hold="bag", faces=[[0, "happy"], [C("the tenant changed"), "shock"], [C("The plug stayed"), "grin"]]),
              CUB(OX + 900, C("Nearly all"), face="happy", faces=[[0, "happy"], [C("cool air"), "wow"]], hops=[C("cool air", 0.3)]),
              tag((0, "FACT · MINISTRY OF ENERGY (≈88% HYDRO)"), (C("In the port town"), "FACT · COMPANY ANNOUNCEMENTS 2025-26"), (C("Norway's oil fortune"), "LIBRARY · EP 04"))]},
    sources=["ef_no", "openai_no25", "nscale_no26"], sfx=[{"kind": "whoosh", "cue": "Nearly all", "gain": 0.3}])
stage("s16_iceland", "c3_iceland", {
    **W2("pmmap", "pmnorth", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 0], [0.3, 1]], "hi": [[0.3, 1]]},
         {"variant": "geo", "halls": 2, "air": [[0, 0], [C("cold air"), 1]], "level": [[0, 1], [C("When the reservoirs ran low"), 1], [C("had to sell less"), 0.25]], "snow": True, "plaque": "ICELAND"}),
    "cam": cam((0, 900, 420, 1.15), (C("Power from rivers"), OX + 700, 520, 0.95, WHIP), (C("cold air"), OX + 1400, 540, 1.1, 1.4), (C("But Nia hears"), OX + 600, 560, 1.0, 1.4),
               (C("Cheap doesn't mean"), OX + 960, 520, 0.85, 1.4)), "drift": 3,
    "items": [words("HOT GROUND, COLD AIR", OX + 900, 220, C("Power from rivers"), size=56, until=C("Data centers came")),
              words("CHEAP ≠ ENDLESS", OX + 960, 220, C("Cheap doesn't mean"), size=68),
              NIA(OX + 1000, C("Power from rivers"), face="happy", pose="stand", faces=[[0, "happy"], [C("But Nia hears"), "worry"]]),
              CUB(OX + 1200, C("Power from rivers"), face="happy", faces=[[0, "happy"], [C("When the reservoirs"), "worry"]]),
              LOCAL(OX + 300, C("But Nia hears"), v=12, color=GREEN, face="worry", pose="talk"),
              bub("LOW WATER, LESS POWER TO SELL.", OX + 400, 330, C("When the reservoirs"), until=C("Cheap doesn't mean"), tail=[OX + 320, 600], size=28),
              tag((0, "FACT · ICELAND ENERGY"), (C("When the reservoirs"), "FACT · LANDSVIRKJUN 2024 RESULTS"))]},
    sources=["lv_fs24"], sfx=[{"kind": "whoosh", "cue": "Power from rivers", "gain": 0.3}])
stage("s17_quebec", "c3_quebec", {
    **W2("pmmap", "pmnorth", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 1], [0.3, 2]], "hi": [[0.3, 2]]},
         {"variant": "river", "halls": [[0, 0], [C("Cubby is thrilled"), 2]], "plaque": "QUEBEC"}),
    "cam": cam((0, 700, 440, 1.15), (C("Nia checks the price"), OX + 800, 540, 1.0, WHIP), (C("less than a quarter"), OX + 1200, 520, 1.1, 1.4), (C("Cubby is thrilled"), OX + 900, 560, 1.15, 1.0)), "drift": 2,
    "min_seconds": 8.0,
    "items": [words("BIG FACTORY'S POWER BILL: MONTRÉAL 100 · BOSTON 445", OX + 1100, 220, C("less than a quarter"), size=40),
              NIA(OX + 700, C("Nia checks the price"), face="squint", pose="stand", hold="phone", faces=[[0, "squint"], [C("less than a quarter"), "shock"]]),
              CUB(OX + 950, C("Nia checks the price"), face="happy", faces=[[0, "happy"], [C("Cubby is thrilled"), "wow"]], hops=[C("Cubby is thrilled"), C("Cubby is thrilled", 0.7)]),
              tag((0, "FACT · HYDRO-QUÉBEC 2025 (EXCL. TAXES)"))]},
    sources=["hq_cmp25", "fed_g5a"], sfx=[{"kind": "hit", "cue": "less than a quarter", "gain": 0.3}])
stage("s18_quebec2", "c3_quebec2", {
    **W1("pmqueue", n=[[0, 2], [C("Big new users"), 6]], plaque="PERMISSION NEEDED: 5 MW+"),
    "cam": cam((0, 900, 520, 0.9), (C("Big new users"), 700, 540, 1.0, 1.4), (C("proposed a new rate"), 1100, 520, 1.05, 1.4), (C("The cheapest plug"), 960, 520, 0.85, 1.6)), "drift": 2,
    "items": [words("NO MORE SURPLUS POWER", 900, 220, C("Hydro-Québec now says"), size=56, until=C("Big new users")),
              words("PROPOSED DATA-CENTER RATE ≈ 2.5× TODAY'S", 1000, 220, C("proposed a new rate"), size=46, until=C("The cheapest plug")),
              words("ACTING LIKE AN OIL PRODUCER", 960, 220, C("The cheapest plug"), size=56),
              CUB(700, 0.0, face="worry", faces=[[0, "happy"], [C("Then the catch"), "worry"]]),
              NIA(1500, 0.0, face="worry", pose="stand", hold="phone", faces=[[0, "worry"], [C("The cheapest plug"), "squint"]]),
              tag((0, "FACT · HYDRO-QUÉBEC FILING 2026"), (C("proposed a new rate"), "PROPOSED · OUR CALC (NOT APPROVED)"))]},
    sources=["hq_rcd26", "blg_qc26", "lesoleil26"])
stage("s19_texas", "c3_texas", {
    **W2("pmmap", "pmsun", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 2], [0.3, 3]], "hi": [[0.3, 3]]},
         {"variant": "texas", "solar": [[0, 0.3], [C("huge wind and solar"), 1]], "gas": 1, "halls": [[0, 0], [C("In Abilene"), 0], [C("switched on"), 2]],
          "ghosts": [[0, 0], [C("Now everyone wants in"), 0], [C("requests that dwarf"), 14]], "plaque": "TEXAS"}),
    "cam": cam((0, 500, 460, 1.15), (C("Cheap natural gas"), OX + 700, 520, 0.95, WHIP), (C("In Abilene"), OX + 1100, 540, 1.05, 1.4), (C("Now everyone wants in"), OX + 1700, 500, 0.8, 1.6),
               (C("What all this means"), OX + 1100, 520, 0.85, 1.4)), "drift": 3,
    "items": [words("FAST TO PLUG IN", OX + 800, 220, C("a grid famous"), size=56, until=C("In Abilene")),
              words("2025: FIRST AI HALLS SWITCH ON", OX + 1100, 220, C("switched on"), size=50, until=C("Now everyone wants in")),
              words("REQUESTS > EVERYTHING TEXAS USES", OX + 1700, 200, C("requests that dwarf"), size=48, until=C("What all this means")),
              words("SEE: WHY AI COULD MAKE YOUR ELECTRICITY BILL EXPLODE", OX + 1100, 200, C("What all this means"), size=34),
              NIA(OX + 600, C("Cheap natural gas"), face="happy", pose="stand", hold="bag", faces=[[0, "happy"], [C("requests that dwarf"), "shock"]]),
              CUB(OX + 420, C("Cheap natural gas"), face="happy", faces=[[0, "happy"], [C("requests that dwarf"), "wow"]]),
              tag((0, "FACT · TEXAS GRID"), (C("In Abilene"), "FACT · CRUSOE (SEPT 2025)"), (C("Now everyone wants in"), "FINDING · ERCOT REQUESTS, NOT FORECASTS"), (C("What all this means"), "LIBRARY · EP 65"))]},
    sources=["crusoe_abilene", "ercot_ll26"], sfx=[{"kind": "whoosh", "cue": "Cheap natural gas", "gain": 0.3}])
stage("s20_gulf", "c3_gulf", {
    **W2("pmmap", "pmsun", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 3], [0.3, 4]], "hi": [[0.3, 4]]},
         {"variant": "gulf", "solar": [[0, 0], [C("Saudi Arabia signed"), 1]], "gas": [[0, 0], [C("cheap gas"), 1]], "halls": [[0, 0], [C("Abu Dhabi is building"), 0], [C("several big power plants"), 5]], "plaque": "THE GULF"}),
    "cam": cam((0, 1100, 460, 1.15), (C("Sunshine nearly every day"), OX + 700, 520, 0.95, WHIP), (C("Saudi Arabia signed"), OX + 300, 600, 1.1, 1.4), (C("Abu Dhabi is building"), OX + 1300, 520, 0.85, 1.6),
               (C("The countries that sold"), OX + 960, 520, 0.8, 1.4)), "drift": 3,
    "items": [words("SOLAR CONTRACT ≈ 1¢ PER KWH (DAYTIME)", OX + 500, 220, C("Saudi Arabia signed"), size=46, until=C("Abu Dhabi is building")),
              words("PLAN: AN AI CAMPUS UP TO 5 GW", OX + 1300, 220, C("Abu Dhabi is building"), size=48, until=C("The countries that sold")),
              words("FROM SELLING OIL TO SELLING COMPUTING", OX + 960, 200, C("The countries that sold"), size=44),
              NIA(OX + 900, C("Sunshine nearly every day"), face="happy", pose="stand", hold="bag"),
              CUB(OX + 1100, C("Sunshine nearly every day"), face="wow", hops=[C("among the cheapest ever")]),
              tag((0, "FACT · GULF"), (C("Saudi Arabia signed"), "FACT · SAUDI SOLAR AWARD (2021)"), (C("Abu Dhabi is building"), "PLAN · G42 / OPENAI"))]},
    sources=["acwa_shuaibah", "g42_uae"], sfx=[{"kind": "whoosh", "cue": "Sunshine nearly every day", "gain": 0.3}])
stage("s21_gulf2", "c3_gulf2", {
    **W1("pmsun", variant="gulf", solar=1, halls=5, night=[[0, 0], [C("The sun sets"), 0], [C("a data center never sleeps"), 1]], gas=[[0, 0.2], [C("lean on"), 1]],
         heat=[[0, 0], [C("cooling hot chips"), 1]]),
    "cam": cam((0, 1100, 520, 0.9), (C("The sun sets"), 1500, 470, 1.0, 1.6), (C("lean on"), 600, 520, 1.1, 1.2), (C("cooling hot chips"), 1200, 540, 1.05, 1.4), (C("Cheap sunshine"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("SUN SETS. SERVERS DON'T.", 1300, 220, C("The sun sets"), size=56, until=C("lean on")),
              words("NIGHT SHIFT: GAS", 700, 220, C("lean on"), size=56, until=C("cooling hot chips")),
              words("HEAD START, NOT A FREE RIDE", 960, 220, C("Cheap sunshine"), size=56),
              NIA(500, 0.0, face="worry", pose="stand", faces=[[0, "squint"], [C("cooling hot chips"), "worry"]]),
              CUB(760, 0.0, face="happy", faces=[[0, "happy"], [C("a data center never sleeps"), "sleep"], [C("cooling hot chips"), "worry"]]),
              tag((0, "ANALYSIS"))]})
stage("s22_brazil", "c3_brazil", {
    **W2("pmmap", "pmtropic", {"pins": [{**p, "at": 0} for p in PINS], "fly": [[0, 4], [0.3, 5]], "hi": [[0.3, 5]]},
         {"stack": [{"label": "MAKING THE POWER", "v": 0.25, "color": GREEN, "at": C("But Nia finds")}, {"label": "WIRES", "v": 0.2, "color": BLUE, "at": C("But Nia finds", 0.6)},
                    {"label": "TAXES + CHARGES", "v": 0.42, "color": RED, "at": C("Nearly half")}],
          "tax": [[0, ""], [C("Brazil has just passed"), "NEW DATA-CENTER TAX DEAL (2026)"]]}),
    "cam": cam((0, 700, 620, 1.15), (C("Its electricity is mostly"), OX + 400, 520, 0.95, WHIP), (C("But Nia finds"), OX + 1450, 500, 0.95, 1.4), (C("Nearly half"), OX + 1450, 470, 1.05, 1.2),
               (C("Brazil has just passed"), OX + 1100, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("MOSTLY RENEWABLE POWER", OX + 400, 220, C("Its electricity is mostly"), size=56, until=C("But Nia finds")),
              words("CHEAP TO MAKE. EXPENSIVE TO BUY.", OX + 1000, 200, C("The power is cheap"), size=48, until=C("Brazil has just passed")),
              NIA(OX + 900, C("Its electricity is mostly"), face="happy", pose="stand", hold="bag", faces=[[0, "happy"], [C("Nearly half"), "shock"]]),
              CUB(OX + 700, C("Its electricity is mostly"), face="happy", faces=[[0, "happy"], [C("Nearly half"), "worry"], [C("Brazil has just passed"), "happy"]]),
              tag((0, "FACT · EPE (88% RENEWABLE, 2024)"), (C("TikTok"), "FACT · TIKTOK (DEC 2025)"), (C("Nearly half"), "FACT · PWC / ACENDE BRASIL (2024)"), (C("Brazil has just passed"), "FACT · LAW 15,504/2026"))]},
    sources=["epe_ben25", "tiktok_ce", "acende24", "redata26"], sfx=[{"kind": "whoosh", "cue": "Its electricity is mostly", "gain": 0.3}, {"kind": "hit", "cue": "Nearly half", "gain": 0.3}])

# ====================================================================== CHAPTER 4: the catch
bumper("s23_b4", "c4_card", "CHAPTER FOUR", "The catch", "The price on the map is only the start", RED)
board("p24_draw", "c4_draw", "The real price of a plug", "Let me draw what Nia actually learned", [
    S("M 640 900 L 1420 900", "ink", C("Let me draw what Nia actually learned")),
    S(rect(760, 800, 420, 90), "accent3", C("The price on the map"), width=4, fill="accent3", fillOpacity=0.6, kind="bar", label=lbl("PRICE ON THE MAP", 970, 856, 28, "ink")),
    S(rect(760, 700, 420, 90), "accent2", C("the wires"), width=4, fill="accent2", fillOpacity=0.5, kind="bar", label=lbl("WIRES TO BRING IT IN", 970, 756, 28, "ink")),
    S(rect(760, 600, 420, 90), "risk", C("the taxes and charges"), width=4, fill="risk", fillOpacity=0.45, kind="bar", label=lbl("TAXES + CHARGES", 970, 656, 28, "ink")),
    S(rect(760, 500, 420, 90), "accent2", C("then the cooling"), width=4, fill="accent2", fillOpacity=0.3, kind="bar", label=lbl("COOLING", 970, 556, 28, "ink")),
    S(rect(760, 400, 420, 90), "accent", C("the distance"), width=4, fill="accent", fillOpacity=0.45, kind="bar", label=lbl("DISTANCE TO USERS", 970, 456, 28, "ink")),
    S(rect(640, 910, 660, 70), "risk", C("the wait"), width=7, kind="box", label=lbl("UNDER IT ALL: THE WAIT", 970, 956, 30, "risk")),
    S("M 1480 760 L 1600 640 L 1720 760 Z M 1600 640 L 1600 860", "ink", C("A cheap power plant"), width=5, label=lbl("CHEAP PLANT", 1600, 610, 24, "ink")),
    S("M 1500 880 L 1760 880", "risk", C("behind a full grid"), width=8, label=lbl("NO PIPELINE", 1630, 920, 26, "risk")),
    S(dot(1150, 1010), "muted", C("Let me draw what Nia actually learned"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE BLOCKS (NOT TO SCALE)", 1150, 1010, 16, "muted")),
], [{"kind": "point", "at": C("The price on the map", 0.4), "dur": 1.4, "target": [970, 840]}, {"kind": "point", "at": C("the wait", 0.4), "dur": 1.6, "target": [970, 945]},
    {"kind": "react", "at": C("like an oil field")}], enter_left=False)
stage("s25_queue", "c4_queue", {
    **W1("pmqueue", n=[[0, 3], [C("a data center can wait"), 9]], flip=[[0, 0], [C("as long as a decade"), 1.2]], years=True, plaque="GRID CONNECTION"),
    "cam": cam((0, 900, 520, 0.9), (C("a data center can wait"), 1200, 520, 0.85, 1.6), (C("as long as a decade"), 1450, 480, 1.05, 1.2), (C("Cubby can be ready"), 800, 560, 1.15, 1.4)), "drift": 2,
    "items": [words("WAIT FOR A GRID LINK: UP TO A DECADE", 1000, 200, C("as long as a decade"), size=46, until=C("Building the data center")),
              words("THE BUILDING IS FASTER THAN THE PLUG", 960, 200, C("Building the data center"), size=48),
              CUB(560, C("Cubby can be ready"), face="sleep", faces=[[0, "happy"], [C("Cubby can be ready", 1.0), "sleep"]], y=880, scale=0.7),
              tag((0, "FINDING · IEA (EUROPE)"))]},
    sources=["iea_eu_dc"])
stage("s26_ireland", "c4_ireland", {
    **W2("pmmap", "pmqueue", {"pins": [{"x": 935, "y": 265, "label": "IRELAND", "c": GREEN, "at": 0}], "hi": [[0.3, 0]]},
         {"n": 6, "bring": [[0, 0], [C("bring their"), 0], [C("own power"), 1]], "plaque": "DUBLIN GRID (GENERIC)"}),
    "cam": cam((0, 935, 380, 1.2), (C("Data centers there now use"), OX + 960, 520, 0.9, WHIP), (C("Around Dublin"), OX + 700, 540, 1.0, 1.4), (C("own power"), OX + 1100, 520, 1.1, 1.2)), "drift": 2,
    "items": [words("IRELAND 2024: DATA CENTERS 22% · CITY HOMES 18%", OX + 960, 200, C("more than a fifth"), size=42, until=C("Around Dublin")),
              words("NEWCOMERS: BRING YOUR OWN POWER", OX + 1000, 200, C("own power"), size=50),
              NIA(OX + 1600, C("Data centers there now use"), face="shock", pose="stand", faces=[[0, "shock"], [C("Around Dublin"), "worry"]]),
              tag((0, "FACT · CSO IRELAND (2024)"), (C("Around Dublin"), "FACT · CRU DECISION (DEC 2025)"))]},
    sources=["cso_ie24", "cru_ie25"], sfx=[{"kind": "hit", "cue": "more than a fifth", "gain": 0.3}])
stage("s27_heat", "c4_heat", {
    **W2("pmnorth", "pmmap", {"variant": "fjord", "halls": 4, "air": 1, "snow": True},
         {"pins": [{"x": 1000, "y": 200, "label": "TRAINING: FAR NORTH", "c": BLUE, "at": C("Training a giant")}, {"x": 520, "y": 380, "label": "ANSWERS: NEAR YOU", "c": ORANGE, "at": C("Answering your question")}]}),
    "cam": cam((0, 1300, 540, 1.0), (C("which is why the cold north"), 900, 520, 0.85, 1.4), (C("But distance matters"), OX + 960, 540, 1.0, WHIP), (C("So the far north"), OX + 760, 440, 1.15, 1.4)), "drift": 2,
    "items": [words("CHIPS RUN HOT", 1300, 220, 0.2, size=60, until=C("which is why the cold north")),
              words("COLD AIR = FREE COOLING", 900, 220, C("which is why the cold north"), size=56, until=C("But distance matters")),
              words("FAR FOR TRAINING. NEAR FOR ANSWERS.", OX + 960, 960, C("So the far north"), size=46),
              tag((0, "ANALYSIS"))]})
stage("s28_politics", "c4_politics", {
    **W1("pmmap", pins=[{"x": 1010, "y": 205, "label": "NORWAY", "c": BLUE, "at": C("Norway moved")}, {"x": 560, "y": 290, "label": "QUEBEC", "c": GREEN, "at": C("Quebec decides")},
                       {"x": 935, "y": 265, "label": "IRELAND", "c": GREEN, "at": C("Ireland makes")}, {"x": 420, "y": 400, "label": "TEXAS", "c": ORANGE, "at": C("Texas passed")}],
         hi=[[C("Norway moved"), 0], [C("Quebec decides"), 1], [C("Ireland makes"), 2], [C("Texas passed"), 3], [C("Cheap electricity, it turns out"), -1]]),
    "cam": cam((0, 960, 540, 0.95), (C("Norway moved"), 1000, 420, 1.15, 1.2), (C("Quebec decides"), 620, 440, 1.15, 1.2), (C("Ireland makes"), 930, 420, 1.15, 1.2), (C("Texas passed"), 480, 520, 1.15, 1.2),
               (C("Cheap electricity, it turns out"), 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [words("WHO GETS THE CHEAP POWER?", 960, 200, C("When power is cheap"), size=56, until=C("Norway moved")),
              words("GUARDED LIKE OIL", 960, 200, C("Cheap electricity, it turns out"), size=72),
              tag((0, "FACT · GOVERNMENT AND REGULATOR DECISIONS 2023-26"))]},
    sources=["no_crypto25", "blg_qc26", "cru_ie25", "tx_sb6"])

# ====================================================================== CHAPTER 5: is power the new oil?
bumper("s29_b5", "c5_card", "CHAPTER FIVE", "Is power the new oil?", "One big difference", PURPLE)
board("p30_draw", "c5_draw", "Oil's one world market vs power's many local ones", "Let me draw the big difference", [
    S(rect(560, 330, 120, 160), "ink", C("Oil made one world market"), width=5, fill="ink", fillOpacity=0.8, kind="bar", label=lbl("OIL", 620, 312, 28, "ink")),
    S("M 700 410 Q 900 300 1100 410 M 700 410 Q 900 520 1100 410 M 700 410 L 1100 410", "ink", C("wherever you buy it"), width=4, label=lbl("ONE WORLD PRICE (+ SHIPPING)", 900, 560, 26, "ink")),
    S(rect(1120, 370, 160, 80), "accent", C("whoever owned the wells"), kind="box", label=lbl("→ WELL OWNERS", 1200, 418, 24, "accent")),
    S(rect(600, 680, 200, 120) + " " + rect(880, 700, 200, 120) + " " + rect(1160, 680, 200, 120), "accent2", C("lots of little local markets"), width=5, kind="box",
      label=lbl("MANY LOCAL POWER MARKETS", 980, 660, 28, "accent2")),
    S("M 800 680 L 800 800 M 1080 700 L 1080 820 M 1360 680 L 1360 800", "risk", C("stuck behind its own wires"), width=8, label=lbl("WIRES = WALLS", 980, 860, 26, "risk")),
    S(rect(1420, 600, 400, 260), "accent3", C("It goes to whoever can deliver"), width=7, kind="box", label=lbl("PRIZE: FAST · BIG · ALWAYS ON", 1620, 740, 26, "accent3")),
    S(dot(1150, 960), "muted", C("Let me draw the big difference"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NO FIGURES)", 1150, 960, 16, "muted")),
], [{"kind": "point", "at": C("wherever you buy it", 0.3), "dur": 1.4, "target": [900, 410]}, {"kind": "point", "at": C("stuck behind", 0.4), "dur": 1.4, "target": [980, 760]},
    {"kind": "react", "at": C("and keep it on")}])
stage("s31_verdict", "c5_verdict", {
    **W1("pmoil", focus="both", pump=1, ship=[[0, 0], [C("Oil could be shipped"), 0], [C("Electricity has to be used"), 0.6]], wire=[[0, 0], [C("Electricity has to be used"), 1]],
         stopAt=C("close to where it's made"), stopText="USE IT NEAR THE DAM"),
    "cam": cam((0, 960, 520, 0.8), (C("In one way, yes"), 500, 520, 0.95, 1.4), (C("But in another way"), 1450, 520, 0.95, 1.4), (C("So the new oil"), 960, 520, 0.8, 1.6)), "drift": 2,
    "items": [words("YES: IT DECIDES WHERE INDUSTRY LANDS", 700, 220, C("In one way, yes"), size=46, until=C("But in another way")),
              words("NO: YOU CAN'T SHIP IT", 1400, 220, C("But in another way"), size=56, until=C("So the new oil")),
              words("NEW OIL = POWER YOU CAN PLUG INTO NOW", 960, 200, C("So the new oil"), size=50),
              tag((0, "VERDICT · OUR ANALYSIS"))]})
stage("s32_winners", "c5_winners", {
    **W1("pmscore", title="WHO'S WINNING THE PLUG RACE", rows=[{"label": "COLD HYDRO NORTH", "at": C("The cold hydro north"), "mark": "yes"},
                                                             {"label": "TEXAS + THE GULF", "at": C("Texas and the Gulf"), "mark": "yes"},
                                                             {"label": "QUEBEC (WITH PERMISSION)", "at": C("Quebec, if"), "mark": "maybe"},
                                                             {"label": "BRAZIL (IF THE BILL GETS LIGHTER)", "at": C("Brazil, if"), "mark": "maybe"},
                                                             {"label": "CHEAP POWER, FULL GRID", "at": C("And the losers"), "mark": "no"}]),
    "cam": cam((0, 960, 540, 1.0), (C("The cold hydro north"), 960, 500, 1.08, 1.4), (C("And the losers"), 960, 580, 1.08, 1.4)), "drift": 1,
    "items": [CUB(1660, 0.3, y=1010, scale=0.7, face="happy", faces=[[0, "happy"], [C("And the losers"), "worry"]]),
              tag((0, "VERDICT · OUR ANALYSIS"))]})
stage("s33_nia", "c5_nia", {
    **W1("pmnorth", variant="fjord", halls=4, air=1, snow=True, plaque="NIA'S REPORT: A PATTERN, NOT A PIN"),
    "cam": cam((0, 900, 520, 0.85), (C("The giant training halls"), 1300, 520, 1.0, 1.4), (C("Cubby finally gets"), 900, 560, 1.2, 1.2), (C("And Nia gets"), 700, 560, 1.1, 1.2)), "drift": 2,
    "items": [words("BUILD WIRES AS FAST AS DATA CENTERS", 1100, 230, C("And the winners"), size=46, until=C("Cubby finally gets")),
              NIA(600, 0.0, face="happy", pose="stand", hold="phone", faces=[[0, "happy"], [C("Cubby finally gets"), "grin"], [C("Find the plug"), "shock"]]),
              CUB(900, 0.0, face="happy", plugged=C("Cubby finally gets"), faces=[[0, "happy"], [C("Cubby finally gets"), "wow"]], hops=[C("Cubby finally gets", 0.5)]),
              bub("NEXT: ROBOT FACTORIES?!", 640, 320, C("Find the plug"), tail=[600, 560], size=32),
              tag((0, "STORY"))]},
    sfx=[{"kind": "hit", "cue": "Cubby finally gets", "gain": 0.3}])
add("s34_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s35_button", "button", {
    **W1("pmoffice", screen=[[0, "NEXT: ROBOT FACTORIES"]]),
    "cam": cam((0, 900, 600, 1.15), (3.0, 1100, 600, 1.25, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [NIA(600, 0.0, face="grin", pose="stand", hold="bag", scale=1.15),
              bub("PACK YOUR BAGS, CUBBY.", 620, 300, 0.5, until=2.8, tail=[600, 560], size=30),
              CUB([[0, 2300], [2.0, 1000]], 1.0, face="happy", carry="suitcase", hops=[3.2]),
              bub("I ONLY PACK CABLES.", 1060, 360, 2.9, tail=[1000, 640], size=30)]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

TIGHT = {"pmscore", "pmqueue"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "FORECAST": "gold", "PLAN": "gold", "PROPOSED": "gold", "OUR": "gold", "ESTIMATE": "gold", "FINDING": "green"}
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
        if _it.get("kind") in ("toonwords", "sign", "bubble") and isinstance(_it.get("y"), (int, float)) and _it["y"] < 200:
            _it["y"] = 200
        keep.append(_it)
    P["items"] = keep

write(OUT, "# GENERATED by tools/gen_powernewoil_storyboard.py; edit the generator, not this file.\n"
           "# Episode 67 storyboard (Could Cheap Electricity Become the New Oil?): bespoke worlds in CartoonStage/powermap.tsx.\n")

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
