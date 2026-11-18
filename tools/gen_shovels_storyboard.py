"""Generates projects/countries-that-win-the-ai-economy-without-building-ai/deliverables/documentary/storyboard.yaml
(Episode 68: The Countries That Could Win the AI Economy Without Building AI).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/shovels.tsx (svcreek, svstore, svmap, svfoundry, svpolder, svmemory, svlab, svdesert,
svmine, svledger, svtitle, svbumper; items nugget, shovel, svpass, svcoin). Story over statistics: one protagonist (HATTIE, a
gold-country hardware-store owner, fictional) and NUGGET (a talking AI chip with a passport, fictional). No real person is drawn;
companies are named in narration and shown only as generic buildings with plain plaques; no logos, no flags.
Signature animations: 1 the 1849 shovel store vs the creek (s01), 2 the passport-and-map journey (s05, map hops), 3 the AI dollar
rolling downhill through the shovel shops (p06 board), 4 the HBM pancake tower (s16), 5 the shovel-that-lasts split (p32 board).
Presenter boards: p06 the AI dollar's chain, p17 SK hynix from loss to record (bars), p32 which shovels last.
Every number carries a claim pill: FACT / FORECAST / PLAN / OUR CALC / COMPANY / FINDING / ANALYSIS / STORY / LIBRARY.
Run: python tools/gen_shovels_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "countries-that-win-the-ai-economy-without-building-ai"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
OX = 3400  # offset for a second zone
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE, COPPER = "#2F7DE1", "#E8A317", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#1E2233", "#F08A24", "#D9773A"
# treasure-map stamps (svmap canvas)
ST = {"home": {"x": 330, "y": 330, "label": "HOME", "sub": "HATTIE'S STORE", "c": GOLD},
      "tw": {"x": 1580, "y": 445, "label": "TAIWAN", "sub": "THE FOUNDRY", "c": BLUE},
      "nl": {"x": 960, "y": 215, "label": "NETHERLANDS", "sub": "THE MACHINE", "c": ORANGE},
      "kr": {"x": 1560, "y": 245, "label": "S. KOREA", "sub": "THE MEMORY", "c": PURPLE},
      "jp": {"x": 1765, "y": 335, "label": "JAPAN", "sub": "TOOLS + CHEMICALS", "c": RED},
      "gulf": {"x": 1200, "y": 470, "label": "THE GULF", "sub": "MONEY + SUN", "c": GOLD},
      "cl": {"x": 640, "y": 760, "label": "CHILE", "sub": "COPPER", "c": COPPER},
      "au": {"x": 1660, "y": 690, "label": "AUSTRALIA", "sub": "LITHIUM", "c": GREEN}}
ORDER = ["home", "tw", "nl", "kr", "jp", "gulf", "cl", "au"]


def stamps(upto, at0=0.0, gap=0.0):
    """stamps for map scenes: ORDER[:upto+1]; all shown at at0 (or staggered by gap)"""
    return [{**ST[k], "at": at0 + i * gap} for i, k in enumerate(ORDER[:upto + 1])]


def HAT(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=11, skin=1, hair=3, hairStyle=4, color=RED, glasses=True, scarf=GOLD, hat=GOLD, **kw)


def OLDIE(x=None, at=0.0, **kw):
    """the 1849 storekeeper (fictional)"""
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=11, skin=1, hair=3, hairStyle=4, color="#8D6E63", glasses=False, scarf="#FFF3D6", hat="#6D4C41", **kw)


def LOCAL(x=None, at=0.0, v=9, color=BLUE, **kw):
    kw.setdefault("scale", 1.1)
    return it("toon", x=x, at=at, who="shopper", v=v, skin=(v * 3) % 6, hair=(v * 5) % 7, hairStyle=v % 6, color=color, glasses=v % 2 == 0, hat=None, **kw)


def NUG(x, at=0.0, **kw):
    kw.setdefault("y", 860)
    kw.setdefault("scale", 0.7)
    kw.setdefault("passport", True)
    return it("nugget", x=x, at=at, **kw)


def words(text, x, y, at, **kw):
    kw.setdefault("size", 56)
    kw["size"] = min(kw["size"], int(1600 / (0.66 * max(1, len(text)))))
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
    stage(id_, seg, {**W1("svbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "trade",
                     "min_seconds": 4.2, "items": [NUG([[0, -200], [1.4, 300]], 0.9, y=1010, scale=0.55, face="grin", hops=[2.2], passport=True)]},
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


def maphop(frm, to, at, upto):
    """svmap params: stamps up to `upto`, balloon flies from stamp index frm to to at time `at`"""
    return {"stamps": stamps(upto), "route": [[0, frm], [at, frm], [at + 1.6, to]], "hi": [[at + 1.6, to]]}


# ====================================================================== CHAPTER 1: sell the shovels
stage("s01_hook", "co_hook", {
    **W2("svcreek", "svstore", {"rush": [[0, 0], [C("Crowds of dreamers"), 0], [C("Most of them find mud"), 1]], "glint": C("Most of them find mud", 1.0)},
         {"era": "1849", "coins": [[0, 0], [C("But down in town"), 0], [C("She sells the shovels"), 12]], "queue": [[0, 0], [C("But down in town"), 4]]}),
    "cam": cam((0, 900, 520, 1.0), (C("Crowds of dreamers"), 700, 540, 0.95, 1.4), (C("Most of them find mud"), 1150, 600, 1.2, 1.0),
               (C("But down in town"), OX + 600, 520, 0.95, WHIP), (C("She doesn't dig"), OX + 760, 560, 1.15, 1.2),
               (C("Today there's a new gold rush"), OX + 960, 520, 0.85, 1.6), (C("So which countries"), OX + 900, 520, 0.8, 1.4)), "drift": 3,
    "items": [words("CALIFORNIA, 1849", 900, 220, 0.2, size=64, until=C("Most of them find mud")),
              words("MOST FIND MUD", 1150, 220, C("Most of them find mud"), size=60, until=C("But down in town")),
              OLDIE(OX + 640, C("But down in town"), face="grin", pose="stand", faces=[[0, "grin"], [C("She sells the shovels"), "happy"]],
                    label="THE STOREKEEPER (FICTIONAL)", labelUntil=C("She doesn't dig")),
              bub("SHOVELS! GET YOUR SHOVELS!", OX + 640, 300, C("She doesn't dig"), until=C("Today there's a new gold rush"), tail=[OX + 640, 560], size=28),
              words("THE NEW GOLD RUSH: AI", OX + 960, 220, C("Today there's a new gold rush"), size=60, until=C("But some countries")),
              words("SOME COUNTRIES SELL THE SHOVELS", OX + 960, 220, C("But some countries"), size=52, until=C("So which countries")),
              words("WIN AI WITHOUT BUILDING AI?", OX + 960, 220, C("So which countries"), size=60),
              tag((0, "STORY · FICTIONAL STOREKEEPER"), (C("Today there's a new gold rush"), "ANALYSIS"))]},
    sfx=[{"kind": "whoosh", "cue": "But down in town", "gain": 0.3}, {"kind": "hit", "cue": "So which countries", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("svtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [NUG([[0, -200], [2.2, 280]], 1.6, y=1010, scale=0.6, face="grin", hops=[3.4])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])
stage("s03_brannan", "c1_brannan", {
    **W1("svstore", era="1849", coins=[[0, 4], [C("His stores sold the miners"), 4], [C("whatever price the rush"), 12]], queue=[[0, 2], [C("His stores sold the miners"), 7]],
         sign="GENERAL STORE"),
    "cam": cam((0, 700, 520, 0.9), (C("the pattern is real"), 900, 520, 1.0, 1.4), (C("He never mined"), 1150, 580, 1.15, 1.2), (C("His stores sold the miners"), 800, 560, 1.0, 1.4)), "drift": 3,
    "items": [words("TRUE STORY: SAM BRANNAN", 900, 220, C("the pattern is real"), size=56, until=C("He never mined")),
              words("'THE RICHEST MAN IN CALIFORNIA' · NEVER MINED", 1100, 220, C("He never mined"), size=42, until=C("His stores sold the miners")),
              words("HE SOLD WHAT THE MINERS NEEDED", 900, 220, C("His stores sold the miners"), size=50),
              it("svcoin", x=740, y=520, at=C("whatever price the rush"), n=10),
              tag((0, "STORY"), (C("the pattern is real"), "FACT · PBS AMERICAN EXPERIENCE"))]},
    sources=["pbs_brannan"], sfx=[{"kind": "hit", "cue": "He never mined", "gain": 0.3}])
stage("s04_hattie", "c1_hattie", {
    **W1("svstore", era="today", motto="IN A RUSH, SELL SHOVELS", pkg=C("a package lands"), coins=1),
    "cam": cam((0, 600, 500, 0.9), (C("Meet Hattie"), 560, 560, 1.1, 1.2), (C("the old rule"), 560, 420, 1.15, 1.2), (C("a package lands"), 820, 560, 1.15, 1.0),
               (C("And it talks"), 860, 600, 1.25, 1.0)), "drift": 3,
    "items": [HAT([[0, -200], [C("Meet Hattie"), -200], [C("Meet Hattie", 1.6), 420]], 0.0, face="happy", pose="stand", hold="coffee",
                  faces=[[0, "happy"], [C("a package lands"), "squint"], [C("And it talks"), "shock"]], takes=[C("And it talks", 0.2)],
                  label="HATTIE · STORE OWNER (FICTIONAL)", labelUntil=C("the old rule")),
              NUG([[0, 860], [C("And it talks"), 860]], C("Inside is a tiny"), y=720, scale=0.55, face="happy", faces=[[0, "happy"], [C("I'm Nugget"), "grin"]],
                  hops=[C("Hi, it says")], talk=[[C("Hi, it says"), C("I've been everywhere", 1.2)]], label="NUGGET · AI CHIP (FICTIONAL)", labelUntil=C("I'm Nugget", 1.4)),
              bub("HI! I'M NUGGET.", 900, 330, C("Hi, it says"), until=C("I've been everywhere"), tail=[870, 560], size=30),
              bub("I'VE BEEN EVERYWHERE.", 900, 330, C("I've been everywhere"), tail=[870, 560], size=30),
              tag((0, "STORY · FICTIONAL CAST"))]},
    sfx=[{"kind": "hit", "cue": "a package lands", "gain": 0.3}])
stage("s05_passport", "c1_passport", {
    **W2("svmap", "svstore", {"stamps": [{**ST[k], "at": C(cue)} for k, cue in
                                          [("home", "Nugget has a passport"), ("tw", "printed on an island"), ("nl", "a flat green country"), ("kr", "memory from across the sea"),
                                           ("jp", "Its tools and chemicals"), ("gulf", "its money"), ("cl", "its metal"), ("au", "from the mountains")]],
                                "route": [[0, 0], [C("Every stamp is a shovel shop"), 0], [C("Every stamp is a shovel shop", 3.0), 0]], "title": "NUGGET'S PASSPORT, MAPPED"},
         {"era": "today", "motto": "IN A RUSH, SELL SHOVELS"}),
    "cam": cam((0, 960, 540, 1.0), (C("Every stamp is a shovel shop"), 960, 540, 0.95, 1.2), (C("Hattie grabs her hat"), OX + 600, 540, 1.05, WHIP)), "drift": 1,
    "items": [it("svpass", x=960, y=560, at=0.2, until=C("printed on an island"), scale=0.9,
                 stamps=[{"label": "TW", "c": BLUE, "at": 0.8}, {"label": "NL", "c": ORANGE, "at": 1.4}, {"label": "KR", "c": PURPLE, "at": 2.0}, {"label": "JP", "c": RED, "at": 2.6}]),
              words("EVERY STAMP = A SHOVEL SHOP", 960, 980, C("Every stamp is a shovel shop"), size=48, until=C("Hattie grabs her hat")),
              HAT(OX + 420, C("Hattie grabs her hat"), face="grin", pose="cheer", hold="bag"),
              NUG(OX + 700, C("Hattie grabs her hat"), face="grin", hops=[C("Let's go meet", 0.3)]),
              bub("LET'S GO MEET THE SHOPKEEPERS!", OX + 520, 300, C("Let's go meet"), tail=[OX + 440, 560], size=28),
              tag((0, "STORY · SUPPLY CHAIN PER COMPANY REPORTS"))]})
board("p06_draw", "c1_draw", "Where an AI dollar goes", "Let me draw why", [
    S("M 560 1000 L 1780 1000", "ink", C("Let me draw why")),
    S(rect(820, 250, 520, 90), "accent2", C("At the top"), width=5, kind="box", label=lbl("CHATBOT: SELLS ANSWERS", 1080, 308, 30, "accent2")),
    S(arrow((1080, 345), (1080, 405), 0.0), "ink", C("rent a data"), kind="arrow"),
    S(rect(820, 410, 520, 80), "ink", C("rent a data"), width=5, kind="box", label=lbl("DATA CENTER", 1080, 462, 30, "ink")),
    S(arrow((1080, 495), (1080, 545), 0.0), "ink", C("The data center buys chips"), kind="arrow"),
    S(rect(820, 550, 520, 80), "accent2", C("The data center buys chips"), width=5, kind="box", label=lbl("CHIPS (THE FOUNDRY)", 1080, 602, 30, "accent2")),
    S(arrow((1080, 635), (1080, 685), 0.0), "ink", C("The chip factory buys"), kind="arrow"),
    S(rect(760, 690, 640, 80), "accent3", C("The chip factory buys"), width=5, kind="box", label=lbl("MACHINES · MEMORY · CHEMICALS", 1080, 742, 28, "accent3")),
    S(arrow((1080, 775), (1080, 825), 0.0), "ink", C("And all of it needs"), kind="arrow"),
    S(rect(760, 830, 640, 80), "accent", C("And all of it needs"), width=5, kind="box", label=lbl("POWER · MONEY · METAL", 1080, 882, 28, "accent")),
    S("M 700 300 Q 600 600 700 880", "accent", C("Every dollar spent"), width=7, kind="arrow", label=lbl("$ ROLLS DOWNHILL", 620, 600, 26, "accent")),
    S(rect(1420, 255, 360, 80), "risk", C("rivals"), width=5, kind="box", label=lbl("RIVALS EVERYWHERE", 1600, 306, 26, "risk")),
    S(rect(1440, 560, 340, 200), "accent3", C("Some shops near the bottom"), width=6, kind="box", label=lbl("ALMOST NO RIVALS", 1610, 670, 28, "accent3")),
    S(dot(1150, 960), "muted", C("Let me draw why"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NO FIGURES)", 1150, 960, 16, "muted")),
], [{"kind": "point", "at": C("At the top", 0.3), "dur": 1.4, "target": [1080, 300]}, {"kind": "point", "at": C("Every dollar spent", 0.4), "dur": 1.6, "target": [660, 600]},
    {"kind": "react", "at": C("Some shops near the bottom", 0.3)}])

# ====================================================================== CHAPTER 2: the island and the machine
bumper("s07_b2", "c2_card", "CHAPTER TWO", "The island and the machine", "Stamps one and two", BLUE)
stage("s08_taiwan", "c2_taiwan", {
    **W2("svmap", "svfoundry", maphop(0, 1, 0.2, 7), {"queue": [[0, 0], [C("Hattie watches the line"), 0], [C("all waiting at the same"), 6]], "wafers": 1, "plaque": "FOUNDRY (GENERIC)"}),
    "cam": cam((0, 960, 540, 1.0), (C("Nugget was born here"), OX + 1000, 500, 0.85, WHIP), (C("Its design came from America"), OX + 1500, 520, 1.0, 1.4),
               (C("Hattie watches the line"), OX + 200, 560, 1.0, 1.4), (C("Is this the only shop"), OX + 300, 580, 1.15, 1.2)), "drift": 3,
    "items": [words("DESIGNED IN AMERICA. BUILT HERE.", OX + 1300, 210, C("Its design came from America"), size=48, until=C("Hattie watches the line")),
              HAT(OX + 520, C("Nugget was born here"), face="wow" if False else "squint", pose="stand", faces=[[0, "squint"], [C("Is this the only shop"), "shock"]]),
              NUG(OX + 700, C("Nugget was born here"), face="happy", faces=[[0, "happy"], [C("Pretty much"), "grin"]], talk=[[C("Pretty much"), C("Pretty much", 1.0)]]),
              bub("IS THIS THE ONLY SHOP?", OX + 520, 300, C("Is this the only shop"), until=C("Pretty much"), tail=[OX + 520, 560], size=28),
              bub("PRETTY MUCH.", OX + 720, 380, C("Pretty much"), tail=[OX + 700, 640], size=30),
              tag((0, "STORY"), (C("Nugget was born here"), "FINDING · FOUNDRY LEADER (LIBRARY EP 07)"))]})
stage("s09_tsmc", "c2_tsmc", {
    **W1("svfoundry", queue=6, wafers=[[0, 1], [C("every new AI model"), 2.5]], glow=1, plaque="TSMC (GENERIC BUILDING)"),
    "cam": cam((0, 1100, 500, 0.85), (C("Last year"), 1500, 520, 1.05, 1.4), (C("every new AI model"), 1000, 520, 0.85, 1.6)), "drift": 3,
    "items": [words("2025 SALES ≈ $122 BILLION · A RECORD", 1150, 210, C("Last year"), size=50, until=C("every new AI model")),
              words("EVERY NEW AI MODEL NEEDS MORE", 1100, 210, C("every new AI model"), size=52),
              it("svcoin", x=1700, y=600, at=C("the most in its history"), n=12),
              HAT(420, 0.0, face="shock", pose="stand", faces=[[0, "happy"], [C("the most in its history"), "shock"]]),
              tag((0, "FACT · TSMC 2025 REVENUE"), (C("Last year"), "OUR CONVERSION · NT$3.81T AT FED 2025 AVG"))]},
    sources=["tsmc_dec25", "fed_g5a"], sfx=[{"kind": "hit", "cue": "Last year", "gain": 0.3}])
stage("s10_customer", "c2_customer", {
    **W1("svmap", stamps=[{"x": 380, "y": 330, "label": "USA", "sub": "CUSTOMER #1", "c": BLUE, "at": C("America became")},
                          {"x": 1450, "y": 330, "label": "CHINA + HK", "sub": "CUSTOMER #2", "c": PURPLE, "at": C("ahead of China")},
                          {**ST["tw"], "at": 0.2}], title="WHO BUYS FROM TAIWAN (2025)", hi=[[C("America became"), 0]]),
    "cam": cam((0, 960, 540, 1.0), (C("America became"), 700, 480, 1.1, 1.2), (C("Its biggest shipments"), 1400, 520, 1.1, 1.2)), "drift": 1,
    "items": [words("EXPORTS: A NEW RECORD", 960, 980, C("Taiwan's exports smashed"), size=50, until=C("for the first time")),
              words("USA = #1 CUSTOMER, FIRST TIME IN 26 YEARS", 960, 980, C("for the first time"), size=46, until=C("Its biggest shipments")),
              words("TOP SHIPMENTS: SERVERS + CHIPS", 960, 980, C("Its biggest shipments"), size=50),
              tag((0, "FACT · TAIWAN MINISTRY OF FINANCE, 2025"))]},
    sources=["mof_tw25"], sfx=[{"kind": "whoosh", "cue": "America became", "gain": 0.3}])
stage("s11_growth", "c2_growth", {
    **W1("svfoundry", queue=3, wafers=2, glow=[[0, 0.6], [C("faster this year"), 1]], plaque="THE ISLAND'S ECONOMY"),
    "cam": cam((0, 900, 520, 0.85), (C("faster this year"), 1150, 480, 1.0, 1.4), (C("Hattie stares"), 560, 580, 1.2, 1.2)), "drift": 2,
    "items": [words("2026 FORECAST: FASTEST GROWTH SINCE 1987", 1150, 210, C("faster this year"), size=46, until=C("Hattie stares")),
              HAT(520, 0.0, face="squint", pose="stand", hold="clipboard", faces=[[0, "squint"], [C("Hattie stares"), "shock"]], takes=[C("Hattie stares", 0.2)]),
              bub("ALL THAT, FROM SELLING SHOVELS?", 560, 290, C("All that"), tail=[540, 560], size=28),
              tag((0, "FORECAST · DGBAS (AUG 2026)"))]},
    sources=["dgbas_aug26"])
stage("s12_risk", "c2_risk", {
    **W1("svfoundry", queue=[[0, 8], [C("for every customer"), 8]], wafers=1, plaque="THE ONLY SHOP IN TOWN"),
    "cam": cam((0, 1100, 520, 0.85), (C("a little nerve-racking"), 300, 560, 1.1, 1.4), (C("We told that story"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("POWERFUL…", 1150, 210, 0.2, size=60, until=C("a little nerve-racking")),
              words("…AND A LITTLE NERVE-RACKING", 900, 210, C("a little nerve-racking"), size=54, until=C("We told that story")),
              words("LIBRARY: THE SMALL ISLAND THE WHOLE WORLD ECONOMY DEPENDS ON", 960, 210, C("We told that story"), size=34),
              NUG(560, 0.0, face="worry", y=880),
              tag((0, "ANALYSIS"), (C("We told that story"), "LIBRARY · EP 07"))]})
stage("s13_nl", "c2_nl", {
    **W2("svmap", "svpolder", maphop(1, 2, 0.2, 7), {"crate": [[0, 0], [C("by a machine that only one"), 0], [C("ASML"), 1]], "bus": True,
                                                       "planes": [[0, 0], [C("packed into cargo planes"), 0], [C("packed into cargo planes", 2.4), 2.6]], "plaque": "ASML (GENERIC BUILDING)"}),
    "cam": cam((0, 960, 540, 1.0), (C("A flat, green country"), OX + 800, 500, 0.85, WHIP), (C("by a machine that only one"), OX + 1150, 540, 1.05, 1.4),
               (C("about the size of a bus"), OX + 950, 540, 0.95, 1.2), (C("packed into cargo planes"), OX + 1700, 460, 0.9, 1.4)), "drift": 3,
    "items": [words("ONLY ONE COMPANY CAN BUILD IT", OX + 1150, 200, C("by a machine that only one"), size=52, until=C("about the size of a bus")),
              words("THE SIZE OF A BUS", OX + 950, 200, C("about the size of a bus"), size=60, until=C("packed into cargo planes")),
              words("SHIPPED IN PIECES BY AIR", OX + 1700, 200, C("packed into cargo planes"), size=54),
              HAT(OX + 300, C("A flat, green country"), face="happy", pose="stand", faces=[[0, "happy"], [C("by a machine that only one"), "shock"]]),
              NUG(OX + 500, C("A flat, green country"), face="grin"),
              tag((0, "STORY"), (C("by a machine that only one"), "FACT · ASML 20-F · REUTERS"))]},
    sources=["asml_ar25", "reuters_asml"], sfx=[{"kind": "whoosh", "cue": "A flat, green country", "gain": 0.3}])
stage("s14_asml", "c2_asml", {
    **W1("svpolder", crate=1, bus=False, planes=0, plaque="THE MACHINE"),
    "cam": cam((0, 1240, 520, 1.15), (C("And if you want"), 1000, 520, 0.9, 1.4), (C("Hattie whispers"), 900, 580, 1.15, 1.2)), "drift": 2,
    "items": [words("≈ $250 MILLION PER MACHINE", 1240, 200, 0.3, size=58, until=C("And if you want")),
              words("NO SECOND SHOP", 1000, 200, C("there is no"), size=64),
              HAT([[0, 2300], [C("And if you want"), 2300], [C("Hattie whispers"), 900]], 0.0, face="shock", pose="stand", faces=[[0, "shock"], [C("Now that's a shovel"), "grin"]]),
              it("shovel", x=760, y=860, at=C("Now that's a shovel"), scale=0.9, rot=-12, gold=True, chip=True),
              bub("NOW THAT'S A SHOVEL.", 900, 300, C("Hattie whispers"), tail=[900, 560], size=30),
              tag((0, "FACT · REUTERS (JAN 2026)"))]},
    sources=["reuters_asml"], sfx=[{"kind": "hit", "at": 0.3, "gain": 0.3}])
stage("s15_nlcatch", "c2_nlcatch", {
    **W2("svpolder", "svmap", {"crate": 1, "planes": [[0, 0], [C("Governments decide"), 0], [C("Governments decide", 2.0), 1.2]], "plaque": "EXPORT LICENCE REQUIRED"},
         {"stamps": [{"x": 1450, "y": 360, "label": "CHINA", "sub": "BIGGEST MARKET", "c": PURPLE, "at": C("biggest market")}, {**ST["nl"], "at": 0}], "title": "WHERE MAY THE MACHINE GO?"}),
    "cam": cam((0, 1240, 520, 0.95), (C("Governments decide"), 1700, 460, 0.9, 1.4), (C("biggest market"), OX + 1200, 420, 1.05, WHIP), (C("We took the machine apart"), OX + 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [words("GOVERNMENTS DECIDE WHERE IT GOES", 1300, 200, C("Governments decide"), size=50, until=C("biggest market")),
              words("CHINA: NO MOST-ADVANCED MACHINES", OX + 1200, 980, C("biggest market"), size=46, until=C("We took the machine apart")),
              words("LIBRARY: THE MACHINE EVERY ADVANCED CHIP DEPENDS ON", OX + 960, 980, C("We took the machine apart"), size=36),
              tag((0, "ANALYSIS"), (C("biggest market"), "FACT · ASML 20-F · DUTCH EXPORT LICENSING"), (C("We took the machine apart"), "LIBRARY · EP 08"))]},
    sources=["asml_ar25", "euv_licence"])

# ====================================================================== CHAPTER 3: the memory and the materials
bumper("s16_b3", "c3_card", "CHAPTER THREE", "The memory and the materials", "Stamps three and four", PURPLE)
stage("s17_korea", "c3_korea", {
    **W2("svmap", "svmemory", maphop(2, 3, 0.2, 7), {"layers": [[0, 0], [C("layer on"), 0], [C("like a tower of pancakes"), 8], [C("It's called HBM"), 10]], "t0": C("layer on"),
                                                       "syrup": C("I'm hungry"), "plaque": "SK HYNIX (GENERIC BUILDING)"}),
    "cam": cam((0, 960, 540, 1.0), (C("Nugget's brain is fast"), OX + 1100, 520, 0.95, WHIP), (C("like a tower of pancakes"), OX + 1300, 460, 1.05, 1.4),
               (C("Only a handful"), OX + 1100, 500, 0.9, 1.4), (C("I'm hungry"), OX + 900, 580, 1.15, 1.0)), "drift": 3,
    "items": [words("FAST BRAIN, FORGETFUL", OX + 1000, 200, C("Nugget's brain is fast"), size=54, until=C("like a tower of pancakes")),
              words("HBM: MEMORY STACKED LIKE PANCAKES", OX + 1200, 200, C("like a tower of pancakes"), size=48, until=C("Only a handful")),
              words("HBM LEADER: SK HYNIX", OX + 1100, 200, C("the leader is SK hynix"), size=56),
              NUG(OX + 700, C("Nugget's brain is fast"), face="worry", faces=[[0, "worry"], [C("I'm hungry"), "wow"]], talk=[[C("I'm hungry"), C("says Nugget")]]),
              HAT(OX + 450, C("Nugget's brain is fast"), face="happy", pose="stand", faces=[[0, "happy"], [C("You're a chip"), "squint"]]),
              bub("I'M HUNGRY.", OX + 720, 380, C("I'm hungry"), until=C("You're a chip"), tail=[OX + 700, 640], size=30),
              bub("YOU'RE A CHIP.", OX + 460, 300, C("You're a chip"), tail=[OX + 450, 560], size=30),
              tag((0, "STORY"), (C("the leader is SK hynix"), "FINDING · COUNTERPOINT HBM SHARE, Q3 2025"))]},
    sources=["skh_fy25", "cp_hbm"], sfx=[{"kind": "whoosh", "cue": "Nugget's brain is fast", "gain": 0.3}])
B0, SC = 800, 420 / 47.21
board("p18_draw", "c3_draw", "One shovel shop's rollercoaster (operating result)", "Let me draw what the AI rush did", [
    S(f"M 600 {B0} L 1700 {B0}", "ink", C("Let me draw what the AI rush did")),
    S(rect(680, B0, 200, round(7.73 * SC)), "risk", C("SK hynix was losing money"), width=4, fill="risk", fillOpacity=0.6, kind="bar", label=lbl("2023: A LOSS", 780, B0 + 110, 28, "risk")),
    S(rect(980, B0 - round(23.47 * SC), 200, round(23.47 * SC)), "accent2", C("The next year, a record"), width=4, fill="accent2", fillOpacity=0.55, kind="bar", label=lbl("2024: RECORD", 1080, B0 - round(23.47 * SC) - 20, 28, "accent2")),
    S(rect(1280, B0 - round(47.21 * SC), 200, round(47.21 * SC)), "accent3", C("The year after that"), width=4, fill="accent3", fillOpacity=0.6, kind="bar", label=lbl("2025 ≈ $33B", 1380, B0 - round(47.21 * SC) - 20, 30, "accent3")),
    S(f"M 640 {B0 - round(43.6 * SC)} L 1560 {B0 - round(43.6 * SC)}", "risk", C("it out-earned all of Samsung"), width=5, dash=True, label=lbl("ALL OF SAMSUNG, 2025", 860, B0 - round(43.6 * SC) - 16, 24, "risk")),
    S(arrow((900, 760), (1270, 420), -0.2), "accent", C("Then the rush arrived"), width=6, kind="arrow", label=lbl("AI RUSH", 1000, 560, 26, "accent")),
    S(dot(1150, 1000), "muted", C("Let me draw what the AI rush did"), width=1, label=lbl("BARS TO SCALE · SK HYNIX & SAMSUNG RESULTS · $ = OUR CONVERSION (FED 2025 AVG)", 1150, 1000, 15, "muted")),
], [{"kind": "point", "at": C("losing money", 0.3), "dur": 1.4, "target": [780, 850]}, {"kind": "point", "at": C("The year after that", 0.6), "dur": 1.6, "target": [1380, 420]},
    {"kind": "react", "at": C("out-earned all of Samsung", 0.2)}], enter_left=False, sources=["skh_fy25", "skh_fy24", "sec_fy25", "fed_g5a"])
stage("s19_exports", "c3_exports", {
    **W1("svmemory", layers=12, t0=-5, syrup=C("Hattie whistles"), plaque="KOREA'S CHIP EXPORTS"),
    "cam": cam((0, 1100, 500, 0.85), (C("set a new record"), 1300, 460, 1.05, 1.4), (C("Hattie whistles"), 800, 580, 1.15, 1.2)), "drift": 2,
    "items": [words("2025 CHIP EXPORTS ≈ $173 BILLION · A RECORD", 1150, 200, C("set a new record"), size=44, until=C("Hattie whistles")),
              it("svcoin", x=1300, y=520, at=C("set a new record"), n=12),
              HAT(600, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Hattie whistles"), "grin"]]),
              NUG(820, 0.0, face="wow", hops=[C("That's a lot of pancakes", 0.3)]),
              bub("THAT'S A LOT OF PANCAKES.", 640, 290, C("That's a lot of pancakes"), tail=[600, 560], size=28),
              tag((0, "FACT · KOREA MOTIE, 2025"))]},
    sources=["motie_25"], sfx=[{"kind": "hit", "cue": "set a new record", "gain": 0.3}])
stage("s20_japan", "c3_japan", {
    **W2("svmap", "svlab", maphop(3, 4, 0.2, 7), {"bottles": [[0, 0], [C("The ultra-pure chemicals"), 0], [C("Japanese companies make most"), 24]], "t0": C("The ultra-pure chemicals"),
                                                    "out": [[0, 0], [C("chip factories everywhere"), 1]], "plaque": "TOOLMAKER (GENERIC)"}),
    "cam": cam((0, 960, 540, 1.0), (C("No famous chatbot"), OX + 1000, 520, 0.9, WHIP), (C("The machines that coat"), OX + 1280, 480, 1.1, 1.2),
               (C("The ultra-pure chemicals"), OX + 450, 480, 1.05, 1.4), (C("chip factories everywhere"), OX + 1800, 540, 1.0, 1.4)), "drift": 3,
    "items": [words("COAT · ETCH · CLEAN", OX + 1280, 200, C("The machines that coat"), size=58, until=C("The ultra-pure chemicals")),
              words("ULTRA-PURE CHEMICALS + COATINGS", OX + 450, 200, C("The ultra-pure chemicals"), size=48, until=C("Japanese companies make most")),
              words("MOST CHIP COATINGS: MADE IN JAPAN", OX + 960, 200, C("Japanese companies make most"), size=50),
              HAT(OX + 900, C("No famous chatbot"), face="squint", pose="stand", hold="clipboard", faces=[[0, "squint"], [C("But look closer"), "happy"]]),
              NUG(OX + 1080, C("No famous chatbot"), face="happy"),
              tag((0, "STORY"), (C("The machines that coat"), "COMPANY · TOKYO ELECTRON FY2026"), (C("Japanese companies make most"), "FINDING · IHS MARKIT (2019 EST.)"))]},
    sources=["tel_fy26", "ihs_resist"], sfx=[{"kind": "whoosh", "cue": "No famous chatbot", "gain": 0.3}])
stage("s21_quiet", "c3_quiet", {
    **W1("svlab", bottles=24, t0=-5, out=1, plaque="QUIET. STEADY. HARD TO COPY."),
    "cam": cam((0, 1100, 520, 0.9), (C("They make the parts"), 1280, 480, 1.1, 1.4), (C("We opened that cabinet"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("THE PARTS NOBODY CAN SKIP", 1200, 200, C("They make the parts"), size=54, until=C("We opened that cabinet")),
              words("LIBRARY: THE CHEMICALS NOBODY TALKS ABOUT · WILL AI MAKE JAPAN RICH AGAIN?", 960, 200, C("We opened that cabinet"), size=30),
              HAT(500, 0.0, face="happy", pose="stand"), NUG(700, 0.0, face="grin", hops=[C("very hard to copy")]),
              tag((0, "ANALYSIS"), (C("We opened that cabinet"), "LIBRARY · EP 18 · EP 66"))]})

# ====================================================================== CHAPTER 4: money and metal
bumper("s22_b4", "c4_card", "CHAPTER FOUR", "Money and metal", "Stamps five, six and seven", ORANGE)
stage("s23_gulf", "c4_gulf", {
    **W2("svmap", "svdesert", maphop(4, 5, 0.2, 7), {"solar": [[0, 0], [C("and sunshine"), 1]], "vault": [[0, 0], [C("Hattie peeks inside"), 1]], "cash": [[0, 0], [C("pouring it into AI"), 1]],
                                                       "halls": [[0, 0], [C("pouring it into AI"), 3]], "t0": C("pouring it into AI"), "plaque": "INVESTMENT FUND (GENERIC)"}),
    "cam": cam((0, 960, 540, 1.0), (C("Here the shovel"), OX + 1100, 500, 0.85, WHIP), (C("pouring it into AI"), OX + 1200, 480, 0.9, 1.4), (C("Hattie peeks inside"), OX + 500, 560, 1.15, 1.2)), "drift": 3,
    "items": [words("THE SHOVEL: MONEY + SUNSHINE", OX + 1100, 200, C("Here the shovel"), size=52, until=C("Hattie peeks inside")),
              HAT(OX + 760, C("Here the shovel"), face="happy", pose="stand", faces=[[0, "happy"], [C("Hattie peeks inside"), "shock"]]),
              NUG(OX + 960, C("Here the shovel"), face="happy", faces=[[0, "happy"], [C("It's better"), "grin"]], talk=[[C("It's not gold"), C("It's patient", 0.8)]]),
              bub("IT'S NOT GOLD. IT'S BETTER.", OX + 980, 360, C("It's not gold"), until=C("It's patient"), tail=[OX + 960, 640], size=26),
              bub("IT'S PATIENT.", OX + 980, 360, C("It's patient"), tail=[OX + 960, 640], size=30),
              tag((0, "STORY"))]},
    sfx=[{"kind": "whoosh", "cue": "Here the shovel", "gain": 0.3}])
stage("s24_mgx", "c4_mgx", {
    **W2("svdesert", "svmap", {"solar": 1, "vault": 1, "cash": 1, "halls": 3, "t0": -5, "plaque": "MGX (GENERIC BUILDING)"},
         {"stamps": [{"x": 380, "y": 330, "label": "USA", "sub": "STARGATE (PLAN)", "c": PURPLE, "at": C("a plan announced")}, {**ST["gulf"], "at": 0}],
          "route": [[0, 0], [C("a plan announced"), 0], [C("on AI data centers"), 1]], "title": "GULF MONEY, AMERICAN DATA CENTERS"}),
    "cam": cam((0, 700, 520, 0.95), (C("one of the founding backers"), 2000, 460, 0.95, 1.4), (C("a plan announced"), OX + 900, 520, 0.95, WHIP)), "drift": 2,
    "items": [words("A FOUNDING BACKER OF STARGATE", 1200, 200, C("one of the founding backers"), size=50, until=C("a plan announced")),
              words("PLAN: UP TO $500 BILLION", OX + 960, 980, C("a plan announced"), size=56),
              tag((0, "FACT · OPENAI (JAN 2025)"), (C("a plan announced"), "PLAN · OPENAI ANNOUNCEMENT"))]},
    sources=["openai_stargate"], sfx=[{"kind": "hit", "cue": "a plan announced", "gain": 0.3}])
stage("s25_campus", "c4_campus", {
    **W1("svdesert", solar=[[0, 0.3], [C("powered by cheap sunshine"), 1]], vault=1, cash=[[0, 0.4], [C("own a piece of every"), 1]],
         halls=[[0, 1], [C("giant AI campuses"), 5]], t0=C("giant AI campuses"), plaque="AI CAMPUS (PLAN)"),
    "cam": cam((0, 1100, 500, 0.85), (C("giant AI campuses"), 1300, 480, 0.95, 1.4), (C("The bet is simple"), 700, 540, 1.05, 1.4), (C("We followed the power"), 960, 520, 0.85, 1.4)), "drift": 3,
    "items": [words("GIANT AI CAMPUSES IN THE DESERT", 1250, 200, C("giant AI campuses"), size=50, until=C("Saudi Arabia's")),
              words("A NEW AI COMPANY: HUMAIN (PIF)", 1150, 200, C("Saudi Arabia's"), size=48, until=C("The bet is simple")),
              words("CAN'T MAKE SHOVELS? OWN A PIECE OF EVERY SHOP", 960, 200, C("The bet is simple"), size=42, until=C("We followed the power")),
              words("LIBRARY: COULD CHEAP ELECTRICITY BECOME THE NEW OIL?", 960, 200, C("We followed the power"), size=36),
              HAT(400, C("The bet is simple"), face="grin", pose="point"),
              tag((0, "PLAN · STARGATE UAE · HUMAIN (PIF)"), (C("We followed the power"), "LIBRARY · EP 67"))]},
    sources=["g42_stargate_uae", "pif_humain"])
stage("s26_chile", "c4_chile", {
    **W2("svmap", "svmine", maphop(5, 6, 0.2, 7), {"variant": "andes", "trucks": [[0, 0.6], [C("Giant trucks haul"), 1.4]], "stock": [[0, 0], [C("Copper is the wire"), 0], [C("And Chile mines"), 10]],
                                                     "t0": C("Copper is the wire"), "plaque": "COPPER CATHODES"}),
    "cam": cam((0, 960, 540, 1.0), (C("the mountains of Chile"), OX + 900, 480, 0.85, WHIP), (C("Copper is the wire"), OX + 1650, 520, 1.05, 1.4), (C("And Chile mines"), OX + 1100, 500, 0.9, 1.4)), "drift": 3,
    "items": [words("COPPER: THE WIRE IN EVERYTHING AI", OX + 1300, 200, C("Copper is the wire"), size=50, until=C("And Chile mines")),
              words("CHILE ≈ 1 IN 4 TONS OF MINED COPPER", OX + 1100, 200, C("And Chile mines"), size=50),
              HAT(OX + 300, C("the mountains of Chile"), face="wow" if False else "happy", pose="stand", faces=[[0, "happy"], [C("And Chile mines"), "shock"]]),
              NUG(OX + 120, C("the mountains of Chile"), face="wow"),
              tag((0, "STORY"), (C("And Chile mines"), "OUR CALC · USGS MCS 2026 (2025 EST.)"))]},
    sources=["usgs_cu26"], sfx=[{"kind": "whoosh", "cue": "the mountains of Chile", "gain": 0.3}])
stage("s27_aus", "c4_aus", {
    **W2("svmap", "svmine", maphop(6, 7, 0.2, 7), {"variant": "outback", "trucks": 1, "stock": [[0, 0], [C("about a third"), 12]], "t0": C("about a third"), "plaque": "LITHIUM"}),
    "cam": cam((0, 960, 540, 1.0), (C("Australia digs up"), OX + 1200, 500, 0.9, WHIP), (C("the metal in the batteries"), OX + 1650, 480, 1.05, 1.4)), "drift": 3,
    "items": [words("AUSTRALIA ≈ 1/3 OF MINED LITHIUM", OX + 1200, 200, C("about a third"), size=50, until=C("the metal in the batteries")),
              words("LITHIUM: THE BATTERY METAL", OX + 1300, 200, C("the metal in the batteries"), size=54),
              NUG(OX + 400, C("Australia digs up"), face="happy", hops=[C("the metal in the batteries", 0.4)]),
              tag((0, "OUR CALC · USGS MCS 2026 (2025 EST.)"))]},
    sources=["usgs_li26"])
stage("s28_gap", "c4_gap", {
    **W1("svmine", variant="andes", trucks=[[0, 1.4], [C("could fall about a third short"), 0.5]], stock=[[0, 10], [C("could fall about a third short"), 4]], t0=-5,
         gauge=[[0, 0], [C("A shortage sounds like"), 0.9]], plaque="PLANNED MINES vs DEMAND"),
    "cam": cam((0, 900, 520, 0.85), (C("could fall about a third short"), 1500, 500, 1.0, 1.4), (C("A shortage sounds like"), 400, 480, 1.1, 1.4)), "drift": 2,
    "items": [words("FORECAST: PLANNED MINES ≈ 1/3 SHORT BY 2035", 1150, 200, C("could fall about a third short"), size=44, until=C("A shortage sounds like")),
              words("JACKPOT FOR CHILE?", 700, 200, C("A shortage sounds like"), size=62),
              HAT(700, C("A shortage sounds like"), face="grin", pose="cheer"),
              tag((0, "FORECAST · IEA CRITICAL MINERALS OUTLOOK 2025"))]},
    sources=["iea_gcmo25", "iea_gcmo26"], sfx=[{"kind": "hit", "cue": "Here's the twist", "gain": 0.3}])
stage("s29_price", "c4_price", {
    **W1("svmine", variant="andes", trucks=1, stock=6, t0=-5, gauge=[[0, 0.9], [C("When the rush runs hot"), 0.9], [C("When it"), -0.9], [C("So metal is"), -0.2]], plaque="ONE WORLD PRICE"),
    "cam": cam((0, 400, 480, 1.1), (C("When the rush runs hot"), 400, 480, 1.15, 1.0), (C("Nugget gulps"), 800, 580, 1.15, 1.4)), "drift": 2,
    "items": [words("ONE WORLD PRICE", 900, 200, C("Copper is sold"), size=60, until=C("When the rush runs hot")),
              words("HOT RUSH: EVERY MINE WINS", 900, 200, C("When the rush runs hot"), size=54, until=C("When it")),
              words("COOL RUSH: EVERYONE FALLS", 900, 200, C("When it"), size=54, until=C("So metal is")),
              NUG(800, 0.0, face="happy", faces=[[0, "happy"], [C("Nugget gulps"), "worry"]], talk=[[C("So metal is"), C("anyone can sell")]]),
              bub("SO METAL IS A SHOVEL ANYONE CAN SELL.", 820, 330, C("So metal is"), tail=[800, 640], size=26),
              tag((0, "ANALYSIS"))]})

# ====================================================================== CHAPTER 5: when the rush ends
bumper("s30_b5", "c5_card", "CHAPTER FIVE", "When the rush ends", "The catch", RED)
stage("s31_brannan", "c5_brannan", {
    **W1("svstore", era="1849", coins=[[0, 12], [C("his empire collapsed"), 12], [C("and he died poor"), 0]], queue=[[0, 2], [C("his empire collapsed"), 0]], sign="GENERAL STORE"),
    "cam": cam((0, 700, 520, 0.9), (C("his empire collapsed"), 800, 560, 1.1, 1.4), (C("The shovel seller"), 900, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("WHAT HAPPENED TO SAM BRANNAN?", 900, 200, 0.4, size=54, until=C("his empire collapsed")),
              words("HIS EMPIRE COLLAPSED. HE DIED POOR.", 900, 200, C("his empire collapsed"), size=50, until=C("The shovel seller")),
              words("UP WITH THE RUSH… AND DOWN WITH IT", 900, 200, C("The shovel seller"), size=50),
              tag((0, "FACT · PBS AMERICAN EXPERIENCE"))]},
    sources=["pbs_brannan"], sfx=[{"kind": "hit", "cue": "his empire collapsed", "gain": 0.3}])
stage("s32_crash", "c5_crash", {
    **W1("svmemory", layers=[[0, 12], [C("prices fell off a cliff"), 2]], t0=-5, plaque="MEMORY CRASH"),
    "cam": cam((0, 1150, 500, 0.95), (C("prices fell off a cliff"), 1300, 560, 1.1, 1.2), (C("We told that story"), 960, 520, 0.85, 1.4)), "drift": 2,
    "items": [words("IT HAPPENS WITH CHIPS TOO", 1100, 200, 0.3, size=54, until=C("That was a memory crash")),
              words("BUYERS PAUSE → PRICES CRASH", 1100, 200, C("That was a memory crash"), size=50, until=C("We told that story")),
              words("LIBRARY: THE THREE COMPANIES THAT DECIDE HOW MUCH YOUR MEMORY COSTS", 960, 200, C("We told that story"), size=30),
              NUG(700, 0.0, face="worry", faces=[[0, "happy"], [C("prices fell off a cliff"), "worry"]], takes=[C("prices fell off a cliff")]),
              tag((0, "ANALYSIS"), (C("We told that story"), "LIBRARY · EP 14"))]})
board("p33_draw", "c5_draw", "Which shovels last?", "Let me draw it", [
    S("M 1150 300 L 1150 900", "ink", C("Let me draw it")),
    S(rect(560, 300, 520, 90), "accent", C("the shovels anyone can sell"), width=6, kind="box", label=lbl("SHOVELS ANYONE CAN SELL", 820, 358, 28, "accent")),
    S(rect(580, 420, 480, 80), "accent", C("Metal, money, power"), width=4, kind="box", label=lbl("METAL · MONEY · POWER", 820, 472, 28, "ink")),
    S("M 600 640 Q 680 540 760 640 T 920 640 T 1060 640", "risk", C("Their price rises and falls"), width=7, label=lbl("PRICE RIDES THE RUSH", 820, 720, 26, "risk")),
    S(rect(1220, 300, 560, 90), "accent3", C("the shovels nobody else can make"), width=6, kind="box", label=lbl("SHOVELS NOBODY ELSE CAN MAKE", 1500, 358, 28, "accent3")),
    S(rect(1240, 420, 520, 80), "accent3", C("The foundry, the machine"), width=4, kind="box", label=lbl("FOUNDRY · MACHINE · TOP MEMORY", 1500, 472, 26, "ink")),
    S(arrow((1500, 510), (1500, 640), 0.0), "accent3", C("set their own price"), width=6, kind="arrow", label=lbl("SET THEIR OWN PRICE", 1500, 690, 26, "accent3")),
    S(rect(760, 790, 820, 100), "accent2", C("The safest shovel"), width=7, kind="box", label=lbl("SAFEST SHOVEL = NO SECOND SHOP", 1170, 856, 34, "accent2")),
    S(dot(1150, 960), "muted", C("Let me draw it"), width=1, label=lbl("ANALYSIS · OUR FRAMEWORK (NO FIGURES)", 1150, 960, 16, "muted")),
], [{"kind": "point", "at": C("Their price rises", 0.3), "dur": 1.4, "target": [820, 640]}, {"kind": "point", "at": C("set their own price", 0.3), "dur": 1.4, "target": [1500, 600]},
    {"kind": "react", "at": C("no second shop")}])
stage("s34_score", "c5_score", {
    **W1("svledger", rows=[{"label": "TAIWAN + NETHERLANDS: WINNING", "at": C("Taiwan and the Netherlands"), "mark": "yes"},
                           {"label": "SOUTH KOREA: WINNING BIG, ON A ROLLERCOASTER", "at": C("South Korea, winning big"), "mark": "ride"},
                           {"label": "JAPAN: STEADY, HARD TO REPLACE", "at": C("Japan, steady"), "mark": "yes"},
                           {"label": "THE GULF: BUYING A SEAT", "at": C("The Gulf, buying"), "mark": "maybe"},
                           {"label": "CHILE + AUSTRALIA: RICH IN GOOD YEARS", "at": C("Chile and Australia"), "mark": "ride"}]),
    "cam": cam((0, 960, 540, 1.0), (C("Taiwan and the Netherlands"), 960, 500, 1.06, 1.4), (C("Chile and Australia"), 960, 580, 1.06, 1.4)), "drift": 1,
    "items": [HAT(1700, 0.2, face="squint", pose="clipboard", y=1010, scale=0.95), tag((0, "VERDICT · OUR ANALYSIS"))]})
stage("s35_verdict", "c5_verdict", {
    **W2("svmap", "svstore", {"stamps": stamps(7), "route": [[0, 0], [1.0, 7]], "title": "THE SHOVEL SELLERS OF AI"}, {"era": "today", "motto": "IN A RUSH, SELL SHOVELS"}),
    "cam": cam((0, 960, 540, 1.0), (C("But the winners"), 960, 540, 0.95, 1.2), (C("They're the ones"), OX + 700, 520, 1.0, WHIP)), "drift": 1,
    "items": [words("YES. SOME ALREADY ARE.", 960, 980, C("Yes"), size=56, until=C("But the winners")),
              words("NOT WHO DIGS THE MOST…", 960, 980, C("But the winners"), size=54, until=C("They're the ones")),
              words("…WHO OWNS A SHOVEL NOBODY CAN COPY", OX + 900, 200, C("They're the ones"), size=50, until=C("and keep inventing")),
              words("AND INVENTS THE NEXT ONE", OX + 900, 200, C("and keep inventing"), size=56),
              it("shovel", x=OX + 600, y=860, at=C("They're the ones"), scale=1.0, rot=-8, gold=True, chip=True),
              tag((0, "VERDICT · OUR ANALYSIS"))]},
    sfx=[{"kind": "hit", "cue": "Yes", "gain": 0.3}])
stage("s36_hattie", "c5_hattie", {
    **W1("svstore", era="today", motto="WHATEVER THEY CAN'T GET ELSEWHERE", coins=4),
    "cam": cam((0, 560, 480, 1.05), (C("Nugget hops"), 800, 560, 1.15, 1.2), (C("Hattie smiles"), 560, 560, 1.2, 1.2)), "drift": 2,
    "items": [HAT(400, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("Hattie smiles"), "grin"]]),
              NUG([[0, 1200], [C("Nugget hops"), 1200], [C("Nugget hops", 1.2), 820]], 0.0, y=720, scale=0.55, face="happy", hops=[C("Nugget hops", 1.2)],
                  talk=[[C("So what do we sell"), C("Hattie smiles")]]),
              bub("SO WHAT DO WE SELL NOW?", 860, 340, C("So what do we sell"), until=C("Hattie smiles"), tail=[830, 560], size=28),
              bub("WHATEVER THEY CAN'T GET ANYWHERE ELSE.", 520, 290, C("Whatever they can't"), tail=[420, 560], size=26),
              tag((0, "STORY"))]})
add("s37_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s38_button", "button", {
    **W1("svstore", era="today", motto="NOW SELLING: THE NEXT SHOVEL"),
    "cam": cam((0, 700, 520, 1.05), (3.0, 800, 560, 1.2, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [HAT(420, 0.0, face="grin", pose="stand", hold="box", scale=1.15),
              bub("FIRST CUSTOMER?", 460, 300, 0.5, until=2.8, tail=[420, 560], size=30),
              NUG([[0, 2300], [2.0, 860]], 1.0, face="grin", hops=[3.2]),
              bub("I'LL TAKE THE GOLDEN ONE.", 900, 360, 2.9, tail=[860, 640], size=28)]},
    sfx=[{"kind": "hit", "at": 3.0, "gain": 0.3}])

TIGHT = {"svledger"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "FORECAST": "gold", "PLAN": "gold", "OUR": "gold", "ESTIMATE": "gold", "FINDING": "green", "COMPANY": "green"}
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

write(OUT, "# GENERATED by tools/gen_shovels_storyboard.py; edit the generator, not this file.\n"
           "# Episode 68 storyboard (The Countries That Could Win the AI Economy Without Building AI): bespoke worlds in CartoonStage/shovels.tsx.\n")

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
