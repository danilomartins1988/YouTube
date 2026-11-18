"""Generates projects/why-canada-could-win-the-ai-boom/deliverables/documentary/storyboard.yaml
(Episode 70: Why Canada Could Be the Biggest Winner of the AI Boom).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/canada.tsx (caapt, cadesert, cachart, camap, cadam, castage, cacold, camine, calab, caborder,
careceipt, catitle, cabumper; item whirr). Story over statistics: one protagonist (MAYA, a young Montreal AI researcher weighing a California
offer) and one journey, with WHIRR (a walking data center fleeing the desert heat) and LUC (her dad, a Sudbury miner); all fictional. No real
person is drawn (Geoffrey Hinton and Yoshua Bengio are named in narration only); no logos, no flags, no maple leaves.
Signature animations: 1 the phone of crash headlines vs the offer card (s01), 2 the billboard chart's dip and rebound (s04, s05, s41),
3 AI's shopping list ticking on the map (s06, s40), 4 the dam, the permission gate and the price tag (s09-s12), 5 B.C.'s power talent show
(s13), 6 cold air in / heat piped to a campus (s16-s19), 7 mineral gems and the mine calendar counting years (s24-s26), 8 the bridge, the
tariff barrier and the data cable (s36, s37), 9 the printing scorecard receipt (s38).
Presenter boards: p07 AI's shopping list, p20 why the cold is worth money, p34 the talent pipeline with a leak.
Run: python tools/gen_canada_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "why-canada-could-win-the-ai-boom"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
OX = 3400  # offset for a second zone
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE = "#1E88E5", "#F5B700", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#16223A", "#F08A24"


def MAYA(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    return it("toon", x=x, at=at, who="shopper", v=3, skin=1, hair=1, hairStyle=4, color=PURPLE, glasses=True, scarf=TEAL, hat="", **kw)


def LUC(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.25)
    return it("toon", x=x, at=at, who="shopper", v=5, skin=1, hair=6, hairStyle=2, color=ORANGE, glasses=False, scarf="", hat=GOLD, **kw)


def LOCAL(x=None, at=0.0, v=9, color=BLUE, **kw):
    kw.setdefault("scale", 1.05)
    return it("toon", x=x, at=at, who="shopper", v=v, skin=(v * 3) % 5, hair=(v * 5) % 6, hairStyle=v % 6, color=color, glasses=v % 2 == 0, **kw)


def WH(x, at=0.0, **kw):
    kw.setdefault("scale", 0.85)
    return it("whirr", x=x, at=at, **kw)


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
    stage(id_, seg, {**W1("cabumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
                     "min_seconds": 4.2, "items": [WH([[0, 2300], [1.6, 1640]], 1.0, y=1060, scale=0.55, face="happy", hops=[2.4], scarf=0.0)]},
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


# ====================================================================== HOOK
APT = {"phone": [[0, 0], [C("this morning her phone"), 1]], "feed": [[0, ""], [C("Canada's economy is crashing"), "CANADA'S ECONOMY IS CRASHING"]],
       "offer": C("Then a message from California"), "offerText": "CALIFORNIA AI LAB"}
DES = {"temp": [[0, 0.6], [C("Whirr is overheating"), 0.95]], "meter": [[0, 0.5], [C("its power bill keeps climbing"), 0.95]], "fans": 3,
       "sign": [[0, "DESERT DATA CAMPUS"], [C("it needs a new home"), "FOR LEASE: MOVING NORTH?"]]}
stage("s01_hook", "co_hook", {
    **W2("caapt", "cadesert", APT, DES),
    "cam": cam((0, 900, 560, 1.0), (C("this morning her phone"), 1300, 540, 1.05, 1.2), (C("Canada's economy is crashing"), 1500, 520, 1.15, 0.8),
               (C("Pack your bags"), 1400, 540, 1.1, 1.0), (C("Meanwhile, far to the south"), OX + 960, 520, 0.9, WHIP),
               (C("This is Whirr"), OX + 1100, 560, 1.15, 1.2), (C("Maya is thinking of moving south"), 960, 560, 1.0, WHIP),
               (C("Whirr is thinking of moving north"), OX + 1000, 540, 1.0, WHIP), (C("So which is it"), OX + 960, 520, 0.85, 1.6)), "drift": 3,
    "items": [MAYA([[0, -200], [1.6, 760]], 0.0, face="happy", pose="walk", faces=[[0, "happy"], [C("this morning her phone"), "squint"], [C("Canada's economy is crashing"), "worry"],
                   [C("Then a message from California"), "shock"], [C("Pack your bags"), "grin"], [C("Maya is thinking of moving south"), "squint"]],
                   poses=[[1.6, "stand"], [C("Pack your bags"), "cheer"], [C("Maya is thinking of moving south"), "shrug"]], label="MAYA · AI RESEARCHER, MONTREAL (FICTIONAL)", labelUntil=C("this morning her phone")),
              WH(OX + 1100, C("Meanwhile, far to the south"), face="hot", sweat=[0, 999], fan=4, carry="suitcase", faces=[[0, "hot"], [C("One of them has read the map wrong"), "wow"]],
                 label="WHIRR · A DATA CENTER (FICTIONAL)", labelUntil=C("Its fans are screaming")),
              words("THE CRASH?", 1500, 210, C("Canada's economy is crashing"), size=64, until=C("Then a message from California")),
              words("ONE MOVES SOUTH. ONE MOVES NORTH.", OX + 960, 230, C("Whirr is thinking of moving north"), size=54, until=C("So which is it")),
              words("IS CANADA LOSING THE AI BOOM, OR WINNING IT?", OX + 960, 230, C("So which is it"), size=48),
              tag((0, "STORY · FICTIONAL CAST"))]},
    sfx=[{"kind": "whoosh", "cue": "Meanwhile, far to the south", "gain": 0.3}, {"kind": "hit", "cue": "So which is it", "gain": 0.3}])
stage("s02_title", "title_card", {
    **W1("catitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6,
    "items": [WH([[0, -200], [2.4, 560]], 1.4, y=1000, scale=0.6, face="happy", scarf=2.6, frost=2.8, hops=[3.6])]},
    sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])

# ====================================================================== CHAPTER 1: is Canada really crashing?
bumper("s03_b1", "c1_card", "CHAPTER ONE", "Is Canada really crashing?", "The headlines vs the map", RED)
stage("s04_crash", "c1_crash", {
    **W1("cachart", draw=[[0, 0.3], [C("the economy actually shrank"), 0.56]], closed=[[0, 0], [C("Maya's uncle sells car parts"), 0], [C("He stopped smiling"), 1]],
         focus=[[0, ""], [C("the economy actually shrank"), "dip"]], stamp=[[0, ""], [C("The headlines did the math"), "CRASH?"]]),
    "cam": cam((0, 960, 520, 0.95), (C("American tariffs hit"), 900, 480, 1.05, 1.2), (C("the economy actually shrank"), 800, 460, 1.15, 1.0),
               (C("Maya's uncle sells car parts"), 1600, 580, 1.15, 1.2), (C("The headlines did the math"), 960, 480, 1.0, WHIP)), "drift": 2,
    "items": [LOCAL(1500, 0.0, v=8, color=BLUE, face="happy", pose="stand", faces=[[0, "happy"], [C("He stopped smiling"), "worry"]], label="MAYA'S UNCLE (FICTIONAL)", labelUntil=C("He stopped smiling")),
              words("SPRING 2025: THE ECONOMY SHRANK", 960, 210, C("the economy actually shrank"), size=54, until=C("Maya's uncle sells car parts")),
              tag((0, "FACT · STATISTICS CANADA (Q2 2025)"), (C("The headlines did the math"), "STORY · ILLUSTRATIVE CHART"))]},
    sources=["statcan_gdp25"], sfx=[{"kind": "hit", "cue": "The headlines did the math", "gain": 0.35}])
stage("s05_rebound", "c1_rebound", {
    **W1("cachart", draw=[[0, 0.56], [C("This year the economy"), 1]], closed=1, focus=[[0, ""], [C("This year the economy"), "rebound"]]),
    "cam": cam((0, 960, 500, 1.0), (C("This year the economy"), 1200, 460, 1.1, 1.4), (C("That's a forecast"), 960, 520, 0.95, 1.2)), "drift": 2,
    "items": [MAYA(600, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("This year the economy"), "shock"], [C("not the picture on Maya's phone"), "grin"]]),
              words("2026: GROWING AGAIN", 1100, 210, C("This year the economy"), size=60, until=C("That's a forecast")),
              words("A FORECAST, NOT A PROMISE", 1100, 210, C("That's a forecast"), size=54),
              tag((0, "FACT · BANK OF CANADA (OCT 2026)"), (C("That's a forecast"), "FORECAST · BANK OF CANADA"))]},
    sources=["boc_os26"])
stage("s06_list", "c1_list", {
    **W1("camap", ticks=[[0, 0], [C("its shopping list"), 0], [C("looks a lot like a map of Canada"), 4]], route=[[0, 0], [C("The AI boom went shopping"), 1]],
         pins=[{"x": 700, "y": 520, "label": "MONTREAL", "at": C("looks a lot like a map of Canada")}, {"x": 560, "y": 560, "label": "TORONTO", "at": C("looks a lot like a map of Canada", 0.4)}]),
    "cam": cam((0, 960, 540, 0.9), (C("The AI boom went shopping"), 1500, 540, 1.1, 1.4), (C("looks a lot like a map of Canada"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [WH([[0, 400], [C("The AI boom went shopping", 2.0), 700]], 0.0, y=980, scale=0.45, face="wow", carry="suitcase"),
              tag((0, "ANALYSIS"))]})
board("p07_draw", "c1_draw", "What an AI factory needs", "Let me draw what an AI factory needs", [
    S(rect(520, 330, 280, 200), "accent", C("Start with a plug"), width=6, kind="box", label=lbl("A PLUG", 660, 310, 32, "accent")),
    S("M 600 470 L 640 400 L 620 400 L 670 340", "accent", C("all day and all night"), width=8, label=lbl("ALL DAY, ALL NIGHT", 660, 580, 22, "ink")),
    S(rect(840, 330, 280, 200), "accent2", C("Then a fridge"), width=6, kind="box", label=lbl("A FRIDGE", 980, 310, 32, "accent2")),
    S("M 940 500 q 20 -30 0 -60 q -20 -30 0 -60 M 1020 500 q 20 -30 0 -60 q -20 -30 0 -60", "risk", C("every chip turns power into heat"), width=6, label=lbl("HEAT OUT", 980, 580, 24, "risk")),
    S(rect(1160, 330, 280, 200), "muted", C("Then a mine"), width=6, kind="box", label=lbl("A MINE", 1300, 310, 32, "muted")),
    S("M 1220 500 L 1300 400 L 1380 500 Z", "muted", C("are made of metal"), width=5, fill="muted", fillOpacity=0.3, label=lbl("METALS", 1300, 580, 24, "ink")),
    S(rect(1480, 330, 280, 200), "accent3", C("And finally, a brain"), width=6, kind="box", label=lbl("A BRAIN", 1620, 310, 32, "accent3")),
    S("M 1560 440 Q 1580 380 1620 400 Q 1660 370 1680 430 Q 1690 480 1620 490 Q 1560 490 1560 440 Z", "accent3", C("people who know how to build"), width=5, label=lbl("PEOPLE", 1620, 580, 24, "ink")),
    S("M 540 700 Q 1140 760 1740 700", "ink", C("Most countries are strong in a couple"), width=5, label=lbl("MOST COUNTRIES: A COUPLE", 1140, 680, 30, "ink")),
    S(rect(820, 800, 640, 110), "risk", C("Very few have the whole list"), width=7, kind="box", label=lbl("THE WHOLE LIST: RARE", 1140, 870, 40, "risk")),
    S(dot(1150, 980), "muted", C("Let me draw what an AI factory needs"), width=1, label=lbl("ANALYSIS · ILLUSTRATIVE", 1150, 980, 16, "muted")),
], [{"kind": "point", "at": C("Start with a plug", 0.3), "dur": 1.2, "target": [660, 430]}, {"kind": "point", "at": C("Then a mine", 0.3), "dur": 1.2, "target": [1300, 430]},
    {"kind": "react", "at": C("Very few have the whole list", 0.3)}])

# ====================================================================== CHAPTER 2: the power
bumper("s08_b2", "c2_card", "CHAPTER TWO", "The power", "Falling water, and a twist", BLUE)
stage("s09_dam", "c2_dam", {
    **W1("cadam", variant="bc", spill=[[0, 0.4], [C("to dams the size of"), 1]], flow=1),
    "cam": cam((0, 1500, 540, 1.0), (C("They lead out of the mountains"), 960, 460, 0.85, 1.6), (C("Of all its electricity"), 860, 520, 1.05, 1.4),
               (C("Whirr has never seen anything"), 700, 600, 1.2, 1.0)), "drift": 3,
    "items": [WH([[0, 2300], [C("Of all its electricity"), 600]], 0.0, face="hot", carry="suitcase", sweat=[0, C("Of all its electricity")], faces=[[0, "hot"], [C("Whirr has never seen anything"), "wow"]]),
              words("≈ 6 IN 10 kWh FROM FALLING WATER", 960, 210, C("Of all its electricity"), size=56),
              tag((0, "STORY"), (C("Of all its electricity"), "FACT · CANADA ENERGY REGULATOR"))]},
    sources=["cer_can"], sfx=[{"kind": "whoosh", "cue": "They lead out of the mountains", "gain": 0.25}])
stage("s10_rank", "c2_rank", {
    **W1("cadam", variant="bc", spill=1, flow=1),
    "cam": cam((0, 900, 520, 0.95), (C("Whirr does a little dance"), 700, 580, 1.15, 1.2)), "drift": 2,
    "items": [WH(650, 0.0, face="wow", carry="suitcase", hops=[C("Whirr does a little dance", 0.2), C("Whirr does a little dance", 1.0), C("Whirr does a little dance", 1.8)],
                 faces=[[0, "wow"], [C("Whirr does a little dance"), "happy"]]),
              words("2023: WORLD'S NO. 3 HYDROPOWER MAKER", 960, 210, C("That makes Canada"), size=52, until=C("Whirr does a little dance")),
              words("CLEAN. STEADY. ALREADY BUILT.", 960, 210, C("Whirr does a little dance"), size=56),
              tag((0, "FACT · CANADA ENERGY REGULATOR"))]},
    sources=["cer_can"])
stage("s11_quebec", "c2_quebec", {
    **W1("cadam", variant="quebec", plaque="HYDRO-QUÉBEC", spill=0.6, flow=1, price=[[0, ""], [C("A big factory there pays"), "CHEAP POWER"]]),
    "cam": cam((0, 960, 540, 0.9), (C("A big factory there pays"), 700, 500, 1.05, 1.2), (C("We told that story"), 960, 520, 0.95, 1.2), (C("Whirr starts unpacking"), 1500, 600, 1.15, 1.0)), "drift": 2,
    "items": [WH([[0, 1700], [1.6, 1500]], 0.0, face="happy", faces=[[0, "happy"], [C("Whirr starts unpacking"), "calm"]], carry="suitcase", hops=[C("Whirr starts unpacking", 0.3)]),
              words("BIG FACTORY'S BILL: < 1/4 OF BOSTON'S", 960, 210, C("A big factory there pays"), size=50, until=C("We told that story")),
              words("SEE: COULD CHEAP ELECTRICITY BECOME THE NEW OIL?", 960, 210, C("We told that story"), size=38),
              tag((0, "FACT · HYDRO-QUÉBEC 2025 (INTERESTED PARTY)"), (C("We told that story"), "LIBRARY · EP 67"))]},
    sources=["hq_cmp25", "fed_g5a"])
stage("s12_twist", "c2_twist", {
    **W1("cadam", variant="quebec", plaque="HYDRO-QUÉBEC", spill=[[0, 0.6], [C("days of surplus power are over"), 0.05]], flow=0.6, gate=C("need the government's permission"), gateX=520,
         gateText="GOVERNMENT PERMISSION NEEDED", stamp=[[0, ""], [C("days of surplus power are over"), "SURPLUS: OVER"], [C("need the government's permission"), ""]],
         price=[[0, "CHEAP POWER"], [C("proposed for data centers"), "PROPOSED: 2.5×"]]),
    "cam": cam((0, 960, 520, 0.95), (C("days of surplus power are over"), 900, 400, 1.0, 1.0), (C("need the government's permission"), 700, 580, 1.05, 1.2),
               (C("proposed for data centers"), 520, 420, 1.1, 1.2), (C("Whirr stops unpacking"), 1400, 600, 1.15, 1.0)), "drift": 2,
    "items": [WH(1400, 0.0, face="calm", faces=[[0, "calm"], [C("days of surplus power are over"), "wow"], [C("Whirr stops unpacking"), "worry"]], carry="suitcase"),
              words("DATA-CENTER RATE: MORE THAN DOUBLE (PROPOSED)", 1100, 210, C("proposed for data centers"), size=44),
              tag((0, "FACT · HYDRO-QUÉBEC FILING"), (C("proposed for data centers"), "PROPOSED · OUR CALC (≈ 2.5×, NOT APPROVED)"))]},
    sources=["hq_rcd26", "blg_qc26", "hq_cmp25"], sfx=[{"kind": "hit", "cue": "days of surplus power are over", "gain": 0.35}])
stage("s13_bc", "c2_bc", {
    **W1("castage", n=[[0, 3], [C("have to compete"), 8]], left=[[0, 1], [C("for a limited slice"), 0.35]], lit=[[0, -1], [C("like a talent show"), 2], [C("judged on what they give back"), 5]]),
    "cam": cam((0, 960, 520, 0.9), (C("have to compete"), 900, 560, 1.0, 1.4), (C("for a limited slice"), 1500, 420, 1.15, 1.0), (C("like a talent show"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [WH(180, 0.0, scale=0.7, face="wow", carry="suitcase"),
              words("AI PROJECTS NOW COMPETE FOR POWER", 960, 230, C("have to compete"), size=52, until=C("like a talent show")),
              words("UP TO 400 MW · FIRST 2 YEARS", 960, 230, C("like a talent show"), size=56),
              tag((0, "FACT · B.C. GOVERNMENT (JAN 2026)"))]},
    sources=["bc_news26", "bc_iaf"], sfx=[{"kind": "hit", "cue": "like a talent show", "gain": 0.3}])
stage("s14_lesson", "c2_lesson", {
    **W1("cadam", variant="bc", spill=0.5, flow=[[0, 1], [C("already spoken for"), 0.25]]),
    "cam": cam((0, 960, 540, 0.9), (C("Canada has the power"), 900, 500, 1.0, 1.2), (C("The next power has to be built"), 1500, 500, 1.05, 1.4)), "drift": 2,
    "items": [WH(700, 0.0, face="calm", faces=[[0, "calm"], [C("already spoken for"), "worry"]]),
              words("THE CHEAP, EASY POWER: TAKEN", 960, 210, C("already spoken for"), size=56, until=C("The next power has to be built")),
              words("THE NEXT POWER HAS TO BE BUILT", 960, 210, C("The next power has to be built"), size=56),
              tag((0, "ANALYSIS"))]})

# ====================================================================== CHAPTER 3: the cold
bumper("s15_b3", "c3_card", "CHAPTER THREE", "The cold", "A natural fridge", TEAL)
stage("s16_cool", "c3_cool", {
    **W2("cacold", "cadesert", {"air": [[0, 0.3], [C("its fans slow down"), 1]]}, {"temp": 0.95, "meter": 0.95, "fans": 4, "sign": [[0, "AIR CONDITIONING: MAX"]]}),
    "cam": cam((0, 900, 560, 1.0), (C("its fans slow down"), 700, 580, 1.15, 1.2), (C("In the desert"), OX + 960, 520, 0.9, WHIP),
               (C("Up here"), 700, 540, 1.0, WHIP), (C("Whirr sighs"), 700, 600, 1.2, 1.0)), "drift": 3,
    "items": [WH([[0, -200], [C("Whirr steps outside"), -200], [C("Whirr steps outside", 1.6), 650]], 0.0, face="hot", fan=[[0, 4], [C("its fans slow down"), 4], [C("its fans slow down", 1.5), 0.6]],
                 faces=[[0, "hot"], [C("its fans slow down"), "wow"], [C("Whirr sighs"), "calm"]], frost=C("its fans slow down"), scarf=C("Whirr sighs")),
              WH(OX + 1100, 0.0, face="hot", sweat=[0, 999], fan=4),
              words("COLD AIR DOES THE WORK", 960, 210, C("Up here"), size=58),
              tag((0, "MECHANISM"))]},
    sfx=[{"kind": "whoosh", "cue": "In the desert", "gain": 0.25}, {"kind": "whoosh", "cue": "Up here", "gain": 0.25}])
stage("s17_claim", "c3_claim", {
    **W1("cacold", air=1),
    "cam": cam((0, 700, 540, 1.0), (C("That's its own claim"), 960, 520, 0.9, 1.4), (C("The cold is a giant"), 500, 560, 1.1, 1.2)), "drift": 2,
    "items": [WH(1200, 0.0, face="calm", scarf=0.0, frost=0.0, fan=0.6),
              words("FREE COOLING UP TO 80% OF THE YEAR", 960, 210, C("One Quebec operator says"), size=52, until=C("The cold is a giant")),
              words("A GIANT, NATURAL FRIDGE", 960, 210, C("The cold is a giant"), size=60),
              tag((0, "CLAIM · QSCALE (COMPANY, 2022)"), (C("That's its own claim"), "CLAIM · DEPENDS ON DESIGN"))]},
    sources=["qscale22"])
stage("s18_heat", "c3_heat", {
    **W1("cacold", air=1, pipe=[[0, 0], [C("pipe its leftover heat"), 1]], campus="UNIVERSITY CAMPUS"),
    "cam": cam((0, 900, 540, 0.95), (C("In Kamloops"), 1300, 520, 1.0, 1.4), (C("pipe its leftover heat"), 1350, 540, 1.05, 1.4), (C("The servers keep the students warm"), 1600, 580, 1.15, 1.0)), "drift": 2,
    "items": [WH(700, 0.0, face="calm", scarf=0.0, fan=0.8, faces=[[0, "calm"], [C("The servers keep the students warm"), "happy"]]),
              LOCAL(1580, C("The servers keep the students warm"), v=4, color=GOLD, face="grin", pose="cheer", scale=0.9),
              LOCAL(1780, C("The servers keep the students warm", 0.3), v=11, color=GREEN, face="happy", pose="wave", scale=0.9),
              words("LEFTOVER HEAT → CAMPUS", 1200, 210, C("pipe its leftover heat"), size=58),
              tag((0, "PLAN · BELL (KAMLOOPS, B.C.)"))]},
    sources=["bell_aif25"])
stage("s19_money", "c3_money", {
    **W1("cacold", air=1, pipe=1, campus="UNIVERSITY CAMPUS", build=[[0, 0], [C("Microsoft has announced plans"), 0.1], [C("a big bet on the north"), 1]]),
    "cam": cam((0, 1300, 520, 0.95), (C("Microsoft has announced plans"), 1450, 460, 1.0, 1.4), (C("That's a company plan"), 1300, 520, 0.9, 1.2)), "drift": 2,
    "items": [WH(600, 0.0, face="wow", scarf=0.0, fan=0.8),
              words("≈ US$13.6 BILLION PLANNED", 960, 210, C("Microsoft has announced plans"), size=60, until=C("That's a company plan")),
              words("A PLAN, NOT MONEY ALREADY SPENT", 960, 210, C("That's a company plan"), size=54),
              tag((0, "PLAN · MICROSOFT (C$19B, 2023-27; OUR CALC)"))]},
    sources=["msft_ca25", "fed_g5a"])
board("p20_draw", "c3_draw", "Why the cold is worth money", "Let me draw why the cold is worth money", [
    S(rect(560, 420, 220, 320), "ink", C("Here's a server"), width=6, kind="box", label=lbl("A SERVER", 670, 400, 32, "ink")),
    S(arrow((470, 580), (550, 580)), "accent", C("Power goes in"), width=6, kind="arrow", label=lbl("POWER IN", 500, 540, 24, "accent")),
    S("M 640 410 q 20 -30 0 -60 q -20 -30 0 -60 M 700 410 q 20 -30 0 -60 q -20 -30 0 -60", "risk", C("comes out as heat"), width=7, label=lbl("HEAT", 670, 270, 30, "risk")),
    S(rect(880, 380, 400, 170), "risk", C("you pay twice"), width=6, kind="box", label=lbl("HOT PLACE: PAY TWICE", 1080, 475, 32, "risk")),
    S(rect(880, 600, 400, 170), "accent2", C("In a cold place"), width=6, kind="box", label=lbl("COLD PLACE: AIR DOES IT", 1080, 695, 30, "accent2")),
    S(arrow((1290, 690), (1480, 690), -0.2), "accent2", C("carries much of the heat off"), width=6, kind="arrow", label=lbl("COLD AIR", 1390, 650, 24, "accent2")),
    S(rect(1500, 560, 260, 220), "accent3", C("a neighbor wants that heat"), width=6, kind="box", label=lbl("NEIGHBOR GETS HEAT", 1630, 680, 24, "accent3")),
    S("M 600 880 L 1700 880", "ink", C("Same chip, smaller bill"), width=6, label=lbl("SAME CHIP, SMALLER BILL", 1150, 860, 40, "ink")),
    S(dot(1150, 980), "muted", C("Let me draw why the cold is worth money"), width=1, label=lbl("MECHANISM · ILLUSTRATIVE (NOT TO SCALE)", 1150, 980, 16, "muted")),
], [{"kind": "point", "at": C("you pay twice", 0.3), "dur": 1.4, "target": [1080, 465]}, {"kind": "point", "at": C("a neighbor wants that heat", 0.3), "dur": 1.4, "target": [1630, 670]},
    {"kind": "react", "at": C("Same chip, smaller bill", 0.3)}])
stage("s21_whirr", "c3_whirr", {
    **W1("cacold", air=1, lot=C("It starts looking for a lot")),
    "cam": cam((0, 900, 560, 1.0), (C("Cold air, clean power"), 960, 520, 0.9, 1.4), (C("It starts looking for a lot"), 1400, 560, 1.1, 1.2)), "drift": 2,
    "items": [WH([[0, 700], [C("It starts looking for a lot"), 700], [C("It starts looking for a lot", 1.6), 1250]], 0.0, face="happy", scarf=0.0, frost=0.0, fan=0.6,
                 hops=[C("Whirr makes up its mind", 0.3)]),
              words("COLD AIR · CLEAN POWER · NEIGHBORS", 960, 210, C("Cold air, clean power"), size=52),
              tag((0, "STORY"))]})

# ====================================================================== CHAPTER 4: the metals
bumper("s22_b4", "c4_card", "CHAPTER FOUR", "The metals", "Rocks. Our rocks.", ORANGE)
stage("s23_dad", "c4_dad", {
    **W1("camine", gems=0),
    "cam": cam((0, 1000, 520, 0.9), (C("her dad, Luc"), 800, 580, 1.1, 1.2), (C("You know what's inside"), 760, 560, 1.15, 1.0), (C("Rocks. Our rocks"), 700, 560, 1.2, 0.8)), "drift": 2,
    "items": [MAYA([[0, -200], [1.8, 560]], 0.0, face="happy", pose="walk", poses=[[1.8, "stand"]], hold="bag", faces=[[0, "happy"], [C("Rocks. Our rocks"), "grin"]]),
              LUC(860, 0.0, face="happy", pose="wave", poses=[[1.0, "stand"], [C("Rocks. Our rocks"), "point"]], faces=[[0, "happy"], [C("He has heard"), "squint"], [C("Rocks. Our rocks"), "smug"]],
                  label="LUC · MAYA'S DAD, A MINER (FICTIONAL)", labelUntil=C("He has heard")),
              bub("YOU KNOW WHAT'S INSIDE THOSE AI COMPUTERS?", 860, 300, C("You know what's inside"), until=C("Rocks. Our rocks"), tail=[860, 560], size=26),
              bub("ROCKS. OUR ROCKS.", 860, 320, C("Rocks. Our rocks"), tail=[860, 560], size=34),
              tag((0, "STORY · FICTIONAL FAMILY"))]})
stage("s24_list", "c4_list", {
    **W1("camine", gems=[[0, 0], [C("Copper for the wires"), 1], [C("Nickel, lithium and graphite"), 4], [C("Uranium for the nuclear plants"), 5]]),
    "cam": cam((0, 700, 460, 1.0), (C("Uranium for the nuclear plants"), 960, 460, 0.95, 1.2), (C("an official list"), 960, 520, 0.9, 1.4)), "drift": 2,
    "items": [LUC(1500, 0.0, face="smug", pose="stand"),
              words("34 CRITICAL MINERALS ON CANADA'S LIST", 960, 210, C("an official list"), size=50),
              tag((0, "FACT · NATURAL RESOURCES CANADA (2024)"))]},
    sources=["nrcan_cml24"])
stage("s25_uranium", "c4_uranium", {
    **W1("camine", gems=5),
    "cam": cam((0, 960, 460, 0.95), (C("Luc grins"), 1400, 560, 1.15, 1.0)), "drift": 2,
    "items": [LUC(1400, 0.0, face="grin", pose="stand", poses=[[C("Luc grins"), "cheer"]]),
              words("WORLD'S NO. 2 URANIUM PRODUCER (2022)", 960, 210, C("In uranium, Canada is"), size=50),
              bub("ROCKS!", 1400, 330, C("Rocks, he says again"), tail=[1400, 560], size=40),
              tag((0, "FACT · CANADA ENERGY REGULATOR"))]},
    sources=["cer_can"])
stage("s26_slow", "c4_slow", {
    **W1("camine", gems=5, years=[[0, -1], [C("Around the world"), 1], [C("By then"), 16.5]]),
    "cam": cam((0, 960, 520, 0.95), (C("Around the world"), 1500, 420, 1.1, 1.2), (C("By then"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [MAYA(700, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("They're slow"), "squint"], [C("By then"), "shock"]]),
              words("16+ YEARS: DISCOVERY → FIRST ORE", 900, 210, C("Around the world"), size=54),
              tag((0, "FINDING · IEA (WORLD AVERAGE, 2010-19)"))]},
    sources=["iea_crit21"])
stage("s27_fix", "c4_fix", {
    **W1("camine", gems=5, stamp=[[0, ""], [C("Ottawa has set up"), "FASTER APPROVALS?"], [C("started producing less than a year later"), ""]]),
    "cam": cam((0, 960, 500, 0.95), (C("started producing less than a year later"), 1180, 520, 1.05, 1.4), (C("Whether that becomes normal"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [LUC(1500, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("Fast for a mine"), "happy"], [C("Whether that becomes normal"), "smug"]]),
              words("FAST, BUT IT WAS ALREADY MOSTLY BUILT", 960, 210, C("although it was already mostly built"), size=48, until=C("Whether that becomes normal")),
              words("THE TEST: WILL FAST BECOME NORMAL?", 960, 210, C("Whether that becomes normal"), size=50),
              tag((0, "FACT · MAJOR PROJECTS OFFICE (SASKATCHEWAN MINE)"))]},
    sources=["nrcan_mpo26"])

# ====================================================================== CHAPTER 5: the brains
bumper("s28_b5", "c5_card", "CHAPTER FIVE", "The brains", "Where deep learning grew up", PURPLE)
stage("s29_lab", "c5_lab", {
    **W1("calab", net=[[0, 0], [C("Some of the big ideas"), 1]]),
    "cam": cam((0, 700, 540, 0.95), (C("Some of the big ideas"), 1100, 400, 1.05, 1.4), (C("when most of the world had given up"), 960, 520, 0.9, 1.2)), "drift": 2,
    "items": [MAYA([[0, -200], [1.8, 520]], 0.0, face="happy", pose="walk", poses=[[1.8, "stand"]], hold="coffee"),
              words("BIG AI IDEAS GREW UP HERE", 960, 640, C("in Canadian universities"), size=52),
              tag((0, "STORY"))]})
stage("s30_hinton", "c5_hinton", {
    **W1("calab", net=1, screen=[[0, "NEURAL NETWORKS"], [C("a dead end"), "A DEAD END?"], [C("that work helped earn him"), "NOBEL PRIZE, PHYSICS"]]),
    "cam": cam((0, 700, 560, 1.05), (C("that work helped earn him"), 600, 600, 1.15, 1.2)), "drift": 2,
    "items": [MAYA(960, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("that work helped earn him"), "shock"]], poses=[[C("that work helped earn him"), "cheer"]]),
              words("2024 NOBEL PRIZE IN PHYSICS", 1200, 230, C("that work helped earn him"), size=56),
              tag((0, "FACT · NOBELPRIZE.ORG (U. OF TORONTO)"))]},
    sources=["nobel24", "vector"])
stage("s31_bengio", "c5_bengio", {
    **W1("camap", showList=False, pins=[{"x": 700, "y": 520, "label": "MONTREAL · MILA", "at": C("In Montreal, Yoshua Bengio"), "c": "#7357C9"},
                                        {"x": 560, "y": 560, "label": "TORONTO · VECTOR", "at": 0.4, "c": "#1E88E5"}]),
    "cam": cam((0, 900, 540, 0.95), (C("In Montreal, Yoshua Bengio"), 820, 520, 1.15, 1.4), (C("Maya's lab is just down"), 760, 560, 1.2, 1.2)), "drift": 2,
    "items": [words("'THE WORLD'S LARGEST ACADEMIC DEEP-LEARNING CENTER'", 960, 210, C("which describes itself"), size=42, until=C("Maya's lab is just down")),
              words("(ITS OWN DESCRIPTION)", 960, 290, C("which describes itself"), size=34, until=C("Maya's lab is just down")),
              MAYA(1500, C("Maya's lab is just down"), face="grin", pose="wave", scale=1.0),
              tag((0, "FACT · MILA (SELF-DESCRIPTION)"))]},
    sources=["mila"])
stage("s32_strategy", "c5_strategy", {
    **W1("calab", net=1, super=[[0, 0], [C("And now it's paying to build"), 0], [C("owned in Canada"), 1]]),
    "cam": cam((0, 960, 520, 0.95), (C("And now it's paying to build"), 1180, 460, 1.05, 1.4)), "drift": 2,
    "items": [MAYA(700, 0.0, face="happy", pose="stand", faces=[[0, "happy"], [C("owned in Canada"), "grin"]]),
              words("2017: WORLD'S FIRST NATIONAL AI STRATEGY", 960, 210, C("Canada was also"), size=48, until=C("And now it's paying to build")),
              words("A SUPERCOMPUTER OF ITS OWN", 960, 210, C("And now it's paying to build"), size=56),
              tag((0, "FACT · CIFAR"), (C("And now it's paying to build"), "PLAN · ISED (APR 2026)"))]},
    sources=["cifar", "ised_scip26"])
stage("s33_leak", "c5_leak", {
    **W2("calab", "caapt", {"net": 1}, {"phone": [[0, 0], [C("Maya's phone buzzes"), 1]], "feed": [[0, ""]], "offer": C("Maya's phone buzzes"), "offerText": "DECIDED YET?"}),
    "cam": cam((0, 900, 540, 0.95), (C("Follow Maya's classmates"), 1300, 560, 1.0, 1.4), (C("Promising Canadian startups"), 1700, 520, 1.0, 1.4),
               (C("Maya's phone buzzes"), OX + 1400, 540, 1.05, WHIP), (C("Not yet"), OX + 1000, 560, 1.1, 1.0)), "drift": 2,
    "items": [LOCAL([[0, 800], [C("But the stars get the biggest offers"), 800], [C("Promising Canadian startups"), 2500]], 0.0, v=6, color=GREEN, face="grin", pose="walk", hold="bag"),
              LOCAL([[0, 1000], [C("But the stars get the biggest offers", 0.5), 1000], [C("Promising Canadian startups", 0.8), 2600]], 0.0, v=10, color=ORANGE, face="happy", pose="walk", hold="bag"),
              LOCAL(1300, 0.0, v=2, color=BLUE, face="happy", pose="stand"),
              MAYA(500, 0.0, face="squint", pose="stand"),
              MAYA(OX + 800, C("Maya's phone buzzes"), face="squint", pose="stand", faces=[[0, "squint"], [C("Not yet"), "deadpan"]]),
              words("MOST GRADUATES STAY", 960, 210, C("Most science and tech graduates do stay"), size=58, until=C("But the stars get the biggest offers")),
              words("THE STARS GET THE BIGGEST OFFERS", 960, 210, C("But the stars get the biggest offers"), size=54, until=C("Maya's phone buzzes")),
              bub("NOT YET.", OX + 800, 330, C("Not yet"), tail=[OX + 800, 560], size=38),
              tag((0, "FACT · STATISTICS CANADA (STEM RETENTION, 2025)"), (C("But the stars get the biggest offers"), "ANALYSIS · WIDELY REPORTED"))]},
    sources=["statcan_stem25"])
board("p34_draw", "c5_draw", "Canada's talent pipeline", "Let me draw Canada's talent pipeline", [
    S(rect(520, 420, 220, 160), "accent2", C("Students go in here"), width=6, kind="box", label=lbl("UNIVERSITIES", 630, 400, 28, "accent2")),
    S("M 740 500 L 1100 500", "accent2", C("They come out as researchers"), width=30, label=lbl("RESEARCHERS", 920, 460, 26, "accent2")),
    S("M 1100 500 L 1460 500", "accent3", C("and then as founders"), width=30, label=lbl("FOUNDERS", 1280, 460, 26, "accent3")),
    S(arrow((1000, 520), (1120, 820), 0.2), "risk", C("There's a leak"), width=9, kind="arrow", label=lbl("THE LEAK: SOUTH", 1200, 860, 32, "risk")),
    S(rect(1280, 720, 460, 120), "risk", C("higher pay"), width=5, kind="box", label=lbl("PAY · COMPUTERS · FUNDING", 1510, 790, 26, "risk")),
    S(rect(520, 640, 640, 150), "accent3", C("It needs to give it reasons to stay"), width=7, kind="box", label=lbl("REASONS TO STAY: COMPUTERS + COMPANIES", 840, 725, 26, "accent3")),
    S(dot(1150, 980), "muted", C("Let me draw Canada's talent pipeline"), width=1, label=lbl("ANALYSIS · ILLUSTRATIVE", 1150, 980, 16, "muted")),
], [{"kind": "point", "at": C("There's a leak", 0.3), "dur": 1.4, "target": [1060, 650]}, {"kind": "react", "at": C("It needs to give it reasons to stay", 0.3)}], enter_left=False)

# ====================================================================== CHAPTER 6: the catch
bumper("s35_b6", "c6_card", "CHAPTER SIX", "The catch", "The best customer, the biggest risk", RED)
stage("s36_tariffs", "c6_tariffs", {
    **W1("caborder", share=0.75, tariff=C("When Washington adds tariffs")),
    "cam": cam((0, 960, 540, 0.9), (C("Of every dollar of goods"), 1100, 560, 1.0, 1.4), (C("When Washington adds tariffs"), 960, 520, 1.1, 0.8)), "drift": 2,
    "items": [words("≈ 3 IN 4 EXPORT DOLLARS GO TO THE U.S.", 960, 210, C("Of every dollar of goods"), size=50, until=C("When Washington adds tariffs")),
              words("CANADA FEELS IT FIRST", 960, 210, C("When Washington adds tariffs"), size=60),
              tag((0, "FACT · STATISTICS CANADA (2025: ≈72%; 2024: ≈76%)"))]},
    sources=["statcan_trade26"], sfx=[{"kind": "hit", "cue": "When Washington adds tariffs", "gain": 0.35}])
stage("s37_cables", "c6_cables", {
    **W1("caborder", share=0.75, tariff=0.0, cable=[[0, 0], [C("It travels through cables"), 1]]),
    "cam": cam((0, 960, 520, 0.95), (C("It travels through cables"), 960, 600, 0.95, 1.4), (C("but only if Canada builds"), 960, 540, 0.9, 1.2)), "drift": 2,
    "items": [WH(380, 0.0, scale=0.55, face="happy", scarf=0.0, hops=[C("It travels through cables", 0.6)]),
              words("A NEW KIND OF EXPORT?", 960, 210, C("That could be a new kind of export"), size=58, until=C("but only if Canada builds")),
              words("ONLY IF CANADA BUILDS IT", 960, 210, C("but only if Canada builds"), size=58),
              tag((0, "ANALYSIS"))]})
ROWS = [{"label": "POWER", "note": "PLENTY, BUT THE CHEAP PART IS TAKEN", "at": C("Power: plenty"), "mark": "catch"},
        {"label": "COLD", "note": "FREE", "at": C("Cold: free"), "mark": "yes"},
        {"label": "METALS", "note": "IN THE GROUND, SLOW TO DIG UP", "at": C("in the ground"), "mark": "catch"},
        {"label": "BRAINS", "note": "WORLD CLASS, TEMPTED SOUTH", "at": C("world class"), "mark": "catch"},
        {"label": "NEIGHBOR", "note": "CAN SLOW IT ALL WITH A TARIFF", "at": C("a giant neighbor"), "mark": "catch"}]
stage("s38_score", "c6_score", {
    **W1("careceipt", rows=ROWS, print=[[0, 0.15], [C("a giant neighbor", 1.0), 1]], title="THE SCORECARD"),
    "cam": cam((0, 960, 560, 0.95), (C("in the ground"), 960, 520, 0.9, 1.6), (C("a giant neighbor"), 960, 480, 0.88, 1.6)), "drift": 1,
    "items": [WH(1600, 0.0, scale=0.55, face="happy", scarf=0.0, faces=[[0, "happy"], [C("a giant neighbor"), "worry"]]),
              tag((0, "ANALYSIS · SUMMARY OF THE FILM'S SOURCES"))]})

# ====================================================================== CHAPTER 7: Maya's decision
bumper("s39_b7", "c7_card", "CHAPTER SEVEN", "Maya's decision", "So, could Canada win?", GOLD)
stage("s40_answer", "c7_answer", {
    **W1("camap", ticks=4, pins=[{"x": 700, "y": 520, "label": "MONTREAL", "at": 0.2}, {"x": 560, "y": 560, "label": "TORONTO", "at": 0.4},
                                 {"x": 610, "y": 470, "label": "SUDBURY", "at": 0.6}, {"x": 220, "y": 470, "label": "KAMLOOPS", "at": 0.8}]),
    "cam": cam((0, 960, 540, 0.9), (C("the whole shopping list"), 1500, 520, 1.05, 1.4), (C("having the list isn't the same as winning"), 960, 540, 0.9, 1.4)), "drift": 2,
    "items": [words("THE WHOLE LIST. NOW BUILD IT.", 900, 210, C("Canada wins only if it builds"), size=56),
              tag((0, "VERDICT · ANALYSIS"))]})
stage("s41_crash", "c7_crash", {
    **W1("cachart", draw=1, closed=[[0, 1]], focus=[[0, "dip"], [C("the AI boom is betting"), "rebound"]]),
    "cam": cam((0, 960, 520, 0.95), (C("It's real for some industries"), 1600, 580, 1.1, 1.2), (C("betting on a different Canada"), 960, 500, 0.95, 1.4)), "drift": 2,
    "items": [LOCAL(1500, 0.0, v=8, color=BLUE, face="worry", pose="stand"),
              words("THE AI BOOM BETS ON A DIFFERENT CANADA", 960, 210, C("betting on a different Canada"), size=48),
              tag((0, "VERDICT · ANALYSIS"))]})
stage("s42_maya", "c7_maya", {
    **W2("caapt", "cacold", {"phone": [[0, 1], [C("Maya types her answer"), 1]], "offer": 0.0, "offerText": "CALIFORNIA AI LAB", "feed": [[0, ""]]}, {"air": 1, "build": 1}),
    "cam": cam((0, 1200, 540, 1.0), (C("Then she looks out the window"), 900, 420, 1.05, 1.2), (C("a friendly data center waves"), OX + 1100, 560, 1.05, WHIP),
               (C("Maya types her answer"), 1300, 540, 1.05, WHIP), (C("For now, I'm staying"), 1100, 560, 1.0, 1.4)), "drift": 2,
    "items": [MAYA(860, 0.0, face="squint", pose="stand", faces=[[0, "squint"], [C("It's Whirr"), "shock"], [C("Maya types her answer"), "happy"], [C("For now, I'm staying"), "grin"]],
                   poses=[[C("For now, I'm staying"), "cheer"]]),
              WH(OX + 1000, 0.0, face="happy", scarf=0.0, frost=0.0, fan=0.6, wave=C("a friendly data center waves"), hops=[C("Your turn", 0.2)]),
              bub("I MOVED IN. YOUR TURN.", OX + 1000, 300, C("I moved in"), tail=[OX + 1000, 560], size=32),
              bub("ASK ME AGAIN NEXT YEAR. FOR NOW, I'M STAYING.", 960, 280, C("Maya types her answer"), tail=[880, 560], size=26),
              tag((0, "STORY · FICTIONAL"))]},
    sfx=[{"kind": "whoosh", "cue": "a friendly data center waves", "gain": 0.25}, {"kind": "hit", "cue": "For now, I'm staying", "gain": 0.3}])
stage("s43_teaser", "teaser", {
    **W1("camap", showList=False, route=1, pins=[{"x": 700, "y": 520, "label": "MONTREAL", "at": 0.2}]),
    "cam": cam((0, 900, 540, 0.95), (3.0, 960, 540, 0.85, 3.0)), "drift": 2,
    "items": [WH([[0, 2200], [3.0, 1500]], 0.0, scale=0.6, face="happy", scarf=0.0, hops=[3.4]),
              words("NEXT: ANOTHER HIDDEN LINK", 960, 210, C("Next time"), size=56)]})
stage("s44_button", "button", {
    **W1("cacold", air=1, build=1, campus="UNIVERSITY CAMPUS", pipe=1), "cam": cam((0, 960, 600, 1.05), (3.0, 1100, 600, 1.15, 2.0)), "drift": 0, "min_seconds": 5.0,
    "items": [WH(1000, 0.0, face="happy", scarf=0.0, frost=0.0, fan=0.6, wave=0.6),
              MAYA([[0, -200], [2.2, 700]], 0.6, face="grin", pose="walk", poses=[[2.2, "wave"]], scale=1.0),
              bub("SO... ABOUT THAT HEAT?", 1000, 300, 2.6, tail=[1000, 560], size=30)]},
    sfx=[{"kind": "hit", "at": 2.6, "gain": 0.3}])

TIGHT = {"careceipt"}
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.15))
            _k["y"] = max(480, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "PROJECTION": "gold", "SCENARIO": "gold", "OUR": "gold", "ESTIMATE": "gold", "FINDING": "green", "QUOTE": "green", "PLAN": "gold", "CLAIM": "gold", "PROPOSED": "gold", "FORECAST": "gold"}
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

write(OUT, "# GENERATED by tools/gen_canada_storyboard.py; edit the generator, not this file.\n"
           "# Episode 70 storyboard (Why Canada Could Be the Biggest Winner of the AI Boom): bespoke worlds in CartoonStage/canada.tsx.\n")

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
