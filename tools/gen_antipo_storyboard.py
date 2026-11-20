"""Generates projects/anthropics-1-5-trillion-ipo/deliverables/documentary/storyboard.yaml
(Episode 72: Anthropic's $1.5 Trillion IPO: The AI Gold Rush or the Next Bubble?).

Prime-time TV-cartoon GENRE (original cast and sets, human characters, day scenes). Bespoke world:
remotion/src/animation-engine/CartoonStage/antipo.tsx (ajkitchen, ajmarket, ajlab, ajrocket, ajhall, ajscroll, ajloop, ajsupply, ajcase,
ajvault, ajroads, ajgold, ajtitle, ajbumper; item share). Story over statistics: one protagonist, JUNE (fictional nurse from Ohio) and her
ONE SHARE (a golden ticket with a face). Public figures only as respectful caricatures with name tags (Dario and Daniela Amodei, Andy Jassy,
Sundar Pichai), doing only what the narration documents. No logos: the company is shown by its ticker ANT and plain-text plaques.
NEUTRALITY: the bull case, the bear case and the circular-financing criticism get equal screen weight; every figure carries a claim pill.
Signature animations: 1 the first-day screen (s04), 2 the revenue rocket (s10), 3 the dollar machine (s14-s15), 4 the contract scroll (s16),
5 THE MONEY LOOP (s20-s23), 6 the round table of supplier-investors (s24), 7 THE FORK of bright, middle and dark roads (s34-s37).
Presenter boards: p05 three price tags, p11 five scoreboards, p17 four words, p33 what the price assumes.
Run: python tools/gen_antipo_storyboard.py   (it also checks that every cue phrase exists in its segment's narration)
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))
from cartoon_kit import *  # noqa: E402,F403
import cartoon_kit  # noqa: E402

SLUG = "anthropics-1-5-trillion-ipo"
OUT = ROOT / f"projects/{SLUG}/deliverables/documentary/storyboard.yaml"
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
W1 = lambda s, **kw: {"zones": [Z(s, **kw)], "worldW": 2400}
OX = 3400
W2 = lambda a, b, ka=None, kb=None: {"zones": [Z(a, x0=-1600, x1=3000, **(ka or {})), Z(b, x0=3000, x1=7200, ox=OX, **(kb or {}))], "worldW": 2400}
STILL = lambda: [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}]
cam = lambda *keys: [{"at": k[0], "x": k[1], "y": k[2], "zoom": k[3], **({"dur": k[4]} if len(k) > 4 else {})} for k in keys]
WHIP = 0.35
BLUE, GOLD, RED, GREEN, PURPLE, TEAL, NAVY, ORANGE, GREY = "#2F6FDB", "#E8A317", "#E5483B", "#2E9E6B", "#7357C9", "#1F8A8C", "#16223A", "#F08A24", "#5E6B85"


def JUNE(x=None, at=0.0, **kw):
    kw.setdefault("scale", 1.2)
    kw.setdefault("y", 1040)
    return it("toon", x=x, at=at, who="shopper", v=5, skin=3, hair=1, hairStyle=3, color="#3E8ED0", glasses=False, scarf="#E86A92", **kw)


def SHARE(x, y, at=0.0, **kw):
    return it("share", x=x, y=y, at=at, **kw)


def CARI(who, x, at=0.0, **kw):
    kw.setdefault("y", 1040)
    kw.setdefault("scale", 1.05)
    return it("caricature", who=who, x=x, at=at, **kw)


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
    stage(id_, seg, {**W1("ajbumper", act=act, title=title, caption=caption, color=color), "cam": STILL(), "drift": 0, "tone": "strategy",
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


DAYPRICE = lambda *k: [[a, b] for a, b in k]

# ====================================================================== HOOK
stage("s01_hook", "co_hook", {
    **W2("ajkitchen", "ajmarket",
         {"app": [[0, "MY PORTFOLIO"], [C("One share of the most"), "ORDER FILLED: 1 SHARE"]],
          "price": [[0, 0], [C("at the offer price"), 0], [C("at the offer price", 0.1), 83], [C("By lunchtime"), 83], [C("By lunchtime", 1.2), 111.5],
                    [C("By the closing bell"), 111.5], [C("By the closing bell", 1.2), 97.17]],
          "chart": [[0, 0], [C("By lunchtime"), 0.02], [C("By lunchtime", 1.2), 0.2], [C("By the closing bell"), 0.2], [C("By the closing bell", 1.4), 1]],
          "pill": [[C("By the closing bell", 1.5), "CLOSE NOV 19: +17%"]]},
         {"price": 97.17, "chart": 1, "crawl": [[0, "ANT · FIRST DAY OF TRADING · NOV 19, 2026"]], "crowd": 1}),
    "cam": cam((0, 960, 560, 0.95), (C("One share of the most"), 1180, 470, 1.18, 1.2), (C("But here's what puzzled her"), 760, 560, 1.05, 1.0),
               (C("It doesn't make chips"), 960, 540, 0.95, 1.0), (C("And its biggest partners"), OX + 960, 520, 0.9, WHIP), (C("So what exactly did June"), 760, 560, 1.1, WHIP)), "drift": 3,
    "items": [JUNE([[0, -200], [2.0, 560]], 0.0, pose="walk", face="happy", hold="phone", label="JUNE · NURSE, OHIO (FICTIONAL)", labelUntil=C("One share of the most"),
                   poses=[[0, "walk"], [2.0, "stand"]], faces=[[0, "happy"], [C("By lunchtime"), "wow"], [C("By the closing bell"), "squint"], [C("But here's what puzzled her"), "worry"],
                                                              [C("So what exactly did June"), "squint"]]),
              SHARE(860, 700, C("One share of the most"), mood=[[0, "happy"], [C("By lunchtime"), "wow"], [C("By the closing bell"), "calm"]], label="JUNE'S ONE SHARE",
                    labelUntil=C("By lunchtime")),
              words("BARELY OLD ENOUGH FOR KINDERGARTEN", 960, 230, C("barely old enough"), size=50, until=C("It doesn't make chips")),
              words("NO CHIP FACTORIES", 960, 230, C("It doesn't make chips"), size=60, until=C("It doesn't own a giant cloud")),
              words("NO GIANT CLOUD OF ITS OWN", 960, 230, C("It doesn't own a giant cloud"), size=56, until=C("And its biggest partners")),
              words("PARTNERS = SHAREHOLDERS = SUPPLIERS = RIVALS", OX + 960, 250, C("And its biggest partners"), size=44, until=C("So what exactly did June")),
              words("WHAT DID JUNE JUST BUY?", 960, 230, C("So what exactly did June"), size=62),
              tag((0, "STORY · JUNE IS FICTIONAL"), (C("at the offer price"), "FACT · OFFER $83 · 424B4"), (C("By lunchtime"), "FACT · OPEN $111.50 · CNBC"),
                  (C("By the closing bell"), "FACT · CLOSE $97.17 (NOV 19) · CNBC"), (C("barely old enough"), "FACT · FOUNDED JAN 2021 · 424B4"), (C("And its biggest partners"), "FACT · 424B4"))]},
    sources=["ant_424b4", "cnbc_live"], sfx=[{"kind": "hit", "cue": "By lunchtime", "gain": 0.3}, {"kind": "whoosh", "cue": "And its biggest partners", "gain": 0.3}])
stage("s02_title", "title_card", {**W1("ajtitle"), "cam": STILL(), "drift": 0, "min_seconds": 5.6, "items": []}, sfx=[{"kind": "hit", "at": 0.5, "gain": 0.35}])

# ====================================================================== CHAPTER 1
bumper("s03_b1", "c1_card", "CHAPTER ONE", "The trillion-dollar question", "One company, several price tags", BLUE)
stage("s04_day", "c1_day", {
    **W1("ajmarket", price=[[0, 83], [C("When trading opened"), 83], [C("buyers rushed in"), 111.5], [C("Then the excitement cooled"), 111.5],
                            [C("By the close"), 101], [C("By the close", 1.5), 97.17]],
         chart=[[0, 0], [C("When trading opened"), 0.05], [C("buyers rushed in", 1.0), 0.2], [C("Then the excitement cooled"), 0.25], [C("By the close", 1.5), 1]],
         ring=C("When trading opened"), crowd=[[0, 0.4], [C("buyers rushed in"), 1]],
         crawl=[[0, "PRICED LAST NIGHT AT $83"], [C("buyers rushed in"), "OPEN $111.50 · HIGH $115.10"], [C("By the close"), "CLOSE $97.17 · +17% ON THE DAY"]]),
    "cam": cam((0, 960, 520, 0.95), (C("When trading opened"), 1450, 520, 1.15, 1.0), (C("buyers rushed in"), 900, 420, 1.15, 1.2),
               (C("Then the excitement cooled"), 760, 460, 1.05, 1.4), (C("Still a gain for June"), 960, 560, 0.95, 1.0)), "drift": 2,
    "items": [SHARE(1700, 860, 0.0, mood=[[0, "calm"], [C("buyers rushed in"), "wow"], [C("Then the excitement cooled"), "worry"], [C("Still a gain for June"), "happy"]], scale=0.8),
              words("OPEN: $111.50", 960, 230, C("buyers rushed in"), size=64, until=C("Then the excitement cooled")),
              words("QUICK PROFITS TAKEN", 960, 230, C("Then the excitement cooled"), size=58, until=C("By the close")),
              words("CLOSE: $97.17 · STILL ABOVE $83", 960, 230, C("By the close"), size=54),
              tag((0, "FACT · 424B4, FWP"), (C("buyers rushed in"), "FACT · CNBC, FORBES"), (C("By the close"), "FACT · CLOSE NOV 19, 2026 (LATEST AVAILABLE ON NOV 20)"))]},
    sources=["cnbc_live", "forbes_live", "ant_fwp"], sfx=[{"kind": "hit", "cue": "When trading opened", "gain": 0.35}, {"kind": "whoosh", "cue": "By the close", "gain": 0.25}])
board("p05_three", "c1_three", "Several price tags, one company", "Let me draw why", [
    S(rect(560, 760, 260, 160), "accent2", C("Share price times the shares"), width=4, fill="accent2", fillOpacity=0.35, kind="bar", label=lbl("TODAY ≈ 13.2 BN", 690, 950, 24, "ink")),
    S(rect(900, 560, 260, 360), "accent", C("Add every share that could exist"), width=4, fill="accent", fillOpacity=0.4, kind="bar", label=lbl("+ OPTIONS, AWARDS, NOTES", 1050, 990, 20, "ink")),
    S(rect(900, 560, 260, 360), "ink", C("called fully diluted"), width=6, kind="box", label=lbl("FULLY DILUTED ≈ 18 BN", 1030, 540, 26, "ink")),
    S(arrow((1190, 700), (1420, 520), -0.15), "accent", C("At June's price"), width=6, kind="arrow"),
    S(rect(1380, 380, 400, 130), "accent3", C("Wall Street called it"), width=5, kind="box", label=lbl("× $83 ≈ $1.5 TRILLION", 1580, 460, 32, "accent3")),
    S(rect(1380, 560, 400, 150), "muted", C("Same company"), width=4, kind="box", label=lbl("AT $97.17: ≈$1.27T TODAY'S SHARES", 1580, 620, 20, "ink")),
    S(dot(1580, 680), "muted", C("Same company"), width=1, label=lbl("≈$1.75T FULLY DILUTED (THE NATIONAL)", 1580, 680, 20, "ink")),
    S(dot(1150, 1030), "muted", C("Let me draw why"), width=1, label=lbl("SHARE COUNTS: 424B4 · VALUES: CNBC, THE NATIONAL · ROUNDED", 1150, 1030, 16, "muted")),
], [{"kind": "point", "at": C("Share price times the shares", 0.3), "dur": 1.3, "target": [690, 820]}, {"kind": "point", "at": C("called fully diluted", 0.3), "dur": 1.3, "target": [1030, 600]},
    {"kind": "react", "at": C("Different counting", 0.1)}], sources=["ant_424b4", "cnbc_price", "national"])
stage("s06_raise", "c1_raise", {
    **W1("ajsupply", reveal=[[0, 0], [C("a group of chip and cloud giants"), 0], [C("agreed to buy even more stock"), 7]], flip=0, flow=0),
    "cam": cam((0, 960, 560, 1.15), (C("And almost all of that money"), 960, 520, 1.05, 1.2), (C("a group of chip and cloud giants"), 960, 540, 0.95, 1.4)), "drift": 2,
    "items": [words("$81.3 BILLION RAISED · A RECORD", 960, 230, 0.3, size=56, until=C("And almost all of that money")),
              words("97.6% NEW SHARES → THE COMPANY", 960, 230, C("And almost all of that money"), size=54, until=C("The co-founders each sold")),
              words("CO-FOUNDERS SOLD 2.4% OF THE SHARES", 960, 230, C("The co-founders each sold"), size=50, until=C("a group of chip and cloud giants")),
              words("+ $26 BILLION, SAME PRICE", 960, 230, C("a group of chip and cloud giants"), size=58, until=C("Remember that group")),
              words("REMEMBER THIS GROUP", 960, 230, C("Remember that group"), size=60),
              SHARE(1500, 900, 0.0, scale=0.6, mood="calm"),
              tag((0, "FACT · PRICING FWP"), (C("The co-founders each sold"), "FACT · 23.6M OF 980M SHARES · 424B4"), (C("a group of chip and cloud giants"), "FACT · PRIVATE PLACEMENT · 424B4"))]},
    sources=["ant_fwp", "ant_424b4", "national"], sfx=[{"kind": "hit", "cue": "agreed to buy even more stock", "gain": 0.3}])

# ====================================================================== CHAPTER 2
bumper("s07_b2", "c2_card", "CHAPTER TWO", "How it got so valuable", "A lab, a chatbot and a meter that never stops", GREEN)
stage("s08_origin", "c2_origin", {
    **W1("ajlab", plaque="ANTHROPIC · FOUNDED 2021", chat=[[0, ""], [C("an AI assistant called Claude"), "Hello! How can I help today?"]], chatAt=C("an AI assistant called Claude")),
    "cam": cam((0, 760, 560, 1.0), (C("Among them"), 900, 600, 1.1, 1.2), (C("They made Anthropic"), 560, 520, 1.1, 1.2), (C("Their product was"), 1300, 480, 1.15, 1.2)), "drift": 2,
    "items": [it("toon", x=[[0, -300], [2.0, 260]], at=0.0, who="shopper", v=11, skin=1, hair=2, hairStyle=1, color=GREY, scale=1.0, y=1040, pose="walk", face="happy",
                 poses=[[0, "walk"], [2.0, "stand"]], until=C("Among them")),
              it("toon", x=[[0, -500], [2.2, 120]], at=0.0, who="shopper", v=7, skin=4, hair=3, hairStyle=4, color=TEAL, scale=1.0, y=1040, pose="walk", face="happy",
                 poses=[[0, "walk"], [2.2, "stand"]], until=C("Among them")),
              CARI("dario", 760, C("Among them"), pose="talk", label="DARIO AMODEI · CEO", labelUntil=C("They made Anthropic"), poses=[[0, "talk"], [C("Their product was"), "point"]]),
              CARI("daniela", 1060, C("Among them", 0.3), pose="stand", label="DANIELA AMODEI · PRESIDENT", labelUntil=C("They made Anthropic"), flip=True),
              words("RESEARCHERS LEAVE OPENAI", 960, 230, C("A group of researchers"), size=56, until=C("Among them")),
              words("PUBLIC BENEFIT CORPORATION", 960, 230, C("They made Anthropic"), size=56, until=C("Their product was")),
              words("CLAUDE", 960, 230, C("an AI assistant called Claude"), size=80),
              tag((0, "FACT · 424B4: FOUNDED JAN 2021"), (C("Among them"), "FACT · OFFICERS PER 424B4"))]},
    sources=["ant_424b4"])
stage("s09_claude", "c2_claude", {
    **W1("ajlab", plaque="CLAUDE AT WORK", chat=[[0, "One chatbot among many..."], [C("Programmers used it"), "Fix this bug and add a test, please."],
                                                [C("It comes from usage"), "Billed by use: every task counts."]], chatAt=0),
    "cam": cam((0, 1340, 480, 1.25), (C("Programmers used it"), 1300, 460, 1.3, 1.2), (C("And most of the money"), 960, 540, 1.0, 1.2), (C("a little like an electricity bill"), 960, 560, 1.05, 1.0)), "drift": 2,
    "items": [words("CODE, AGENTS, COMPANY APPS", 960, 230, C("Programmers used it"), size=56, until=C("And most of the money")),
              words("USAGE ≈ 4 OF EVERY 5 DOLLARS", 960, 230, C("It comes from usage"), size=54, until=C("a little like an electricity bill")),
              words("PAY AS YOU GO, LIKE A POWER BILL", 960, 230, C("a little like an electricity bill"), size=52),
              SHARE(560, 820, C("And most of the money"), scale=0.7, mood="wow"),
              tag((0, "STORY"), (C("It comes from usage"), "FACT · USAGE 79%, SUBSCRIPTIONS 21% (JAN-SEP 2026) · 424B4"))]},
    sources=["ant_424b4"])
stage("s10_rocket", "c2_rocket", {
    **W1("ajrocket", lift=[[0, 0], [C("When Claude first went on sale"), 0.03], [C("So far this year"), 0.4], [C("That's the rocket"), 0.74], [C("That's the rocket", 4.0), 0.82]],
         marks=[["2023: $41 MILLION", 0.03], ["2024: $386 MILLION", 0.16], ["2025: $4.6 BILLION", 0.36], ["JAN-SEP 2026: $33.2 BILLION", 0.7]]),
    "cam": cam((0, 960, 560, 0.95), (C("When Claude first went on sale"), 880, 540, 1.05, 1.2), (C("So far this year"), 760, 520, 1.0, 1.4), (C("That's the rocket"), 960, 520, 0.95, 1.2)), "drift": 2,
    "items": [words("REVENUE, BY YEAR (NOT TO SCALE)", 1400, 260, C("When Claude first went on sale"), size=40, until=C("So far this year")),
              words("$33.2 BILLION IN 9 MONTHS", 1400, 260, C("So far this year"), size=48, until=C("That's the rocket")),
              words("THE PRICE IS STRAPPED TO THIS", 1400, 260, C("That's the rocket"), size=46),
              tag((0, "FACT · REVENUE 2023-2026 · 424B4"))]},
    sources=["ant_424b4"], sfx=[{"kind": "whoosh", "cue": "So far this year", "gain": 0.35}])
board("p11_score", "c2_score", "Five scoreboards", "Let me draw the others", [
    S(rect(540, 300, 360, 140), "accent3", C("Revenue is what customers paid"), width=5, kind="box", label=lbl("REVENUE: $33.2B (JAN-SEP)", 720, 380, 24, "ink")),
    S(rect(960, 300, 360, 140), "accent2", C("The run rate is"), width=5, kind="box", label=lbl("RUN RATE: ≈$81B (OCT)", 1140, 380, 24, "ink")),
    S(rect(1380, 300, 360, 140), "risk", C("Operating profit is"), width=5, kind="box", label=lbl("OPERATING: −$1.3B", 1560, 380, 24, "ink")),
    S(rect(740, 560, 420, 160), "risk", C("Net profit counts everything else"), width=5, fill="risk", fillOpacity=0.15, kind="box", label=lbl("NET: −$104B", 950, 640, 30, "risk")),
    S(rect(740, 730, 420, 60), "muted", C("mostly accounting on notes"), width=3, kind="box", label=lbl("$94.3B = NOTES' FAIR VALUE, NOT CASH", 950, 770, 18, "ink")),
    S(rect(1240, 560, 420, 160), "accent3", C("And cash flow"), width=5, fill="accent3", fillOpacity=0.2, kind="box", label=lbl("CASH IN: +$6.6B", 1450, 640, 30, "accent3")),
    S(arrow((1450, 740), (1450, 870), 0.0), "accent3", C("turned positive"), width=6, kind="arrow"),
    S(dot(1150, 1010), "muted", C("Let me draw the others"), width=1, label=lbl("JAN-SEP 2026 · RUN RATE AT OCT 31 · 424B4 · OPERATING CASH FLOW", 1150, 1010, 18, "muted")),
], [{"kind": "point", "at": C("Revenue is what customers paid", 0.3), "dur": 1.2, "target": [720, 370]}, {"kind": "point", "at": C("Net profit counts", 0.3), "dur": 1.4, "target": [950, 640]},
    {"kind": "react", "at": C("turned positive", 0.1)}], sources=["ant_424b4"])

# ====================================================================== CHAPTER 3
bumper("s12_b3", "c3_card", "CHAPTER THREE", "The cost of building intelligence", "Chips, power, buildings and promises", ORANGE)
stage("s13_hall", "c3_hall", {
    **W1("ajhall", cost=1.0, costText=[[0, ""]], coins=[[0, 0.3], [C("Running it costs money"), 1.5]]),
    "cam": cam((0, 300, 520, 1.2), (C("Every answer Claude writes"), 520, 520, 1.15, 1.6), (C("Training a new model"), 960, 520, 1.0, 1.2), (C("Running it costs money"), 960, 600, 1.1, 1.0)), "drift": 3,
    "items": [SHARE([[0, -100], [2.5, 400]], 860, 0.0, mood=[[0, "wow"]], scale=0.75, label="FOLLOW THE SHARE", labelUntil=2.5),
              words("CHIPS · POWER · COOLING · BUILDINGS", 960, 230, C("Every answer Claude writes"), size=46, until=C("Training a new model")),
              words("TRAINING: BUILD THE MODEL", 960, 230, C("Training a new model"), size=56, until=C("Running it costs money")),
              words("INFERENCE: EVERY QUESTION COSTS", 960, 230, C("Running it costs money"), size=52),
              tag((0, "MECHANISM · OUR EXPLANATION"))]},
    sources=["ant_424b4"])
stage("s14_dollar", "c3_dollar", {
    **W1("ajhall", cost=[[0, 1.0], [C("Last year"), 1.0], [C("on computing"), 1.6]], costText=[[0, ""], [C("on computing"), "2025: ≈ $1.60 PER $1 OF SALES"]], coins=1.2),
    "cam": cam((0, 960, 560, 1.0), (C("Last year"), 960, 600, 1.15, 1.2), (C("It was selling dollars"), 960, 560, 1.0, 1.0)), "drift": 2,
    "items": [words("SELLING $1 THAT COSTS $1.60", 960, 230, C("It was selling dollars"), size=56),
              tag((0, "OUR CALC · 2025: $7.3B COMPUTE ÷ $4.6B REVENUE · 424B4"))]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "on computing", "gain": 0.3}])
stage("s15_better", "c3_better", {
    **W1("ajhall", cost=[[0, 1.6], [C("the picture flipped"), 1.6], [C("computing cost"), 0.57]],
         costText=[[0, "2025: ≈ $1.60 PER $1 OF SALES"], [C("computing cost"), "JAN-SEP 2026: ≈ $0.57 PER $1"]], coins=1.5),
    "cam": cam((0, 960, 600, 1.15), (C("Bigger customers"), 960, 540, 0.95, 1.2)), "drift": 2,
    "items": [words("BIGGER CUSTOMERS · LEANER MODELS · BETTER CHIP DEALS", 960, 230, C("Bigger customers"), size=40, until=C("That's the chart the optimists")),
              words("THE OPTIMISTS' CHART", 960, 230, C("That's the chart the optimists"), size=60),
              tag((0, "OUR CALC · JAN-SEP 2026: $18.8B ÷ $33.2B · 424B4"))]},
    sources=["ant_424b4"], sfx=[{"kind": "whoosh", "cue": "the picture flipped", "gain": 0.3}])
stage("s16_scroll", "c3_commit", {
    **W1("ajscroll", unroll=[[0, 0.05], [C("To keep growing"), 0.08], [C("stretching over years"), 0.7], [C("some over decades"), 1.0]], stamp=C("But much of it is promised")),
    "cam": cam((0, 700, 560, 1.05), (C("To keep growing"), 900, 560, 1.0, 1.4), (C("some over decades"), 1100, 540, 0.95, 1.4), (C("But much of it is promised"), 1200, 480, 1.0, 0.8)), "drift": 2,
    "items": [words("THE SKEPTICS' CHART", 960, 230, 0.2, size=60, until=C("To keep growing")),
              words("≈ $900.9 BILLION OF COMPUTE PROMISES", 960, 230, C("To keep growing"), size=48, until=C("That's not money already spent")),
              words("NOT SPENT YET. PROMISED.", 960, 230, C("That's not money already spent"), size=58),
              tag((0, "FACT · COMMITMENTS AND LEASES, TO 2045 · 424B4"), (C("But much of it is promised"), "FACT · AMAZON, GOOGLE, MICROSOFT: 'REGARDLESS OF ACTUAL USAGE'"))]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "But much of it is promised", "gain": 0.35}])
board("p17_words", "c3_words", "Four words that get mixed up", "Let me separate some words", [
    S(rect(540, 300, 330, 150), "accent", C("A commitment is"), width=5, fill="accent", fillOpacity=0.3, kind="box", label=lbl("COMMITMENT ≈ $901B", 705, 385, 26, "ink")),
    S(rect(960, 300, 330, 150), "accent2", C("Spending is cash going out"), width=5, kind="box", label=lbl("SPENDING: CASH OUT", 1125, 385, 26, "ink")),
    S(arrow((880, 375), (950, 375), 0.0), "ink", C("Spending is cash going out"), width=5, kind="arrow"),
    S(rect(1380, 300, 330, 150), "risk", C("Debt is borrowed money"), width=5, kind="box", label=lbl("DEBT: $6.2B", 1545, 385, 28, "ink")),
    S(rect(960, 540, 330, 150), "muted", C("An expense hits profit"), width=5, kind="box", label=lbl("EXPENSE: HITS PROFIT", 1125, 625, 24, "ink")),
    S(arrow((1125, 460), (1125, 530), 0.0), "ink", C("An expense hits profit"), width=5, kind="arrow"),
    S(rect(560, 760, 160, 200), "accent3", C("its actual debt is small"), width=4, fill="accent3", fillOpacity=0.4, kind="bar", label=lbl("CASH ≈ $132B", 640, 990, 22, "ink")),
    S(rect(760, 935, 160, 25), "risk", C("its actual debt is small"), width=4, fill="risk", fillOpacity=0.5, kind="bar", label=lbl("DEBT $6.2B", 840, 990, 22, "ink")),
    S(rect(1200, 780, 520, 120), "risk", C("It's the promise"), width=6, kind="box", label=lbl("THE RISK = THE PROMISE", 1460, 855, 32, "risk")),
    S(dot(1150, 1030), "muted", C("Let me separate some words"), width=1, label=lbl("SEP 30, 2026, BEFORE IPO PROCEEDS · CASH INCL. SHORT-TERM INVESTMENTS · 424B4", 1150, 1030, 16, "muted")),
], [{"kind": "point", "at": C("A commitment is", 0.3), "dur": 1.2, "target": [705, 380]}, {"kind": "point", "at": C("its actual debt is small", 0.3), "dur": 1.4, "target": [700, 880]},
    {"kind": "react", "at": C("It's the promise", 0.1)}], enter_left=False, sources=["ant_424b4"])
stage("s18_question", "c3_question", {
    **W1("ajhall", cost=[[0, 0.57], [C("If demand keeps climbing"), 0.35], [C("If it stalls"), 1.4]],
         costText=[[0, "THE BET: EARN MORE THAN IT COSTS"], [C("If demand keeps climbing"), "DEMAND CLIMBS: PROMISES LOOK CHEAP"], [C("If it stalls"), "DEMAND STALLS: PROMISES LOOK HUGE"]], coins=[[0, 1], [C("If it stalls"), 0.2]]),
    "cam": cam((0, 960, 560, 1.0), (C("If demand keeps climbing"), 960, 600, 1.12, 1.0), (C("If it stalls"), 960, 600, 1.12, 0.6)), "drift": 2, "tone": "strategy",
    "items": [SHARE(1500, 760, 0.0, scale=0.7, mood=[[0, "calm"], [C("If demand keeps climbing"), "happy"], [C("If it stalls"), "worry"]]),
              tag((0, "ANALYSIS · ILLUSTRATIVE"))]},
    sources=["ant_424b4"])

# ====================================================================== CHAPTER 4
bumper("s19_b4", "c4_card", "CHAPTER FOUR", "Partners on every side", "Investors, suppliers, sellers and rivals", PURPLE)
stage("s20_amazon", "c4_amazon", {
    **W1("ajloop", invest=[[0, 0], [C("It has invested billions"), 0], [C("It has invested billions", 1.2), 1]], compute=[[0, 0], [C("Its cloud rents"), 0], [C("Its cloud rents", 1.0), 1]],
         pay=[[0, 0], [C("Anthropic has promised to spend"), 0], [C("Anthropic has promised to spend", 1.0), 1]], resell=[[0, 0], [C("Amazon also sells Claude"), 0], [C("Amazon also sells Claude", 1.4), 1]]),
    "cam": cam((0, 760, 560, 1.15), (C("It has invested billions"), 860, 520, 1.05, 1.2), (C("Anthropic has promised to spend"), 900, 560, 1.0, 1.2), (C("Amazon also sells Claude"), 700, 560, 1.0, 1.2),
               (C("and builds AI models"), 760, 560, 1.1, 1.0)), "drift": 2,
    "items": [CARI("jassy", 300, 0.3, y=1040, scale=0.95, pose="stand", label="ANDY JASSY · AMAZON CEO", labelUntil=C("It has invested billions", 2.5), until=C("Amazon also sells Claude")),
              words("AMAZON: INVESTOR", 960, 200, C("It has invested billions"), size=54, until=C("Its cloud rents")),
              words("AMAZON: LANDLORD FOR COMPUTE", 960, 200, C("Its cloud rents"), size=50, until=C("Anthropic has promised to spend")),
              words("≥ $110 BILLION PROMISED TO AMAZON, 2026-2036", 960, 200, C("Anthropic has promised to spend"), size=42, until=C("Amazon also sells Claude")),
              words("AMAZON: SELLER OF CLAUDE", 960, 200, C("Amazon also sells Claude"), size=52, until=C("and builds AI models")),
              words("AMAZON: RIVAL TOO", 960, 200, C("and builds AI models"), size=56),
              tag((0, "FACT · AMAZON 10-Q Q3 2026"), (C("Anthropic has promised to spend"), "FACT · ≥$110B, MAY 2026-APR 2036 · 424B4"), (C("and builds AI models"), "FACT · 424B4 RISK FACTORS"))]},
    sources=["amzn_10q", "ant_424b4"])
stage("s21_loop", "c4_loop", {
    **W1("ajloop", invest=[[0, 0], [C("Amazon sends cash to Anthropic"), 0], [C("Amazon sends cash to Anthropic", 1.0), 1]],
         compute=[[0, 0], [C("to pay for computing"), 0], [C("to pay for computing", 0.8), 1]],
         pay=[[0, 0], [C("Anthropic sends cash back"), 0], [C("Anthropic sends cash back", 1.0), 1]],
         resell=[[0, 0], [C("When Amazon sells Claude"), 0], [C("When Amazon sells Claude", 1.6), 1]],
         stake=[[0, 0], [C("And when Anthropic's value rises"), 0.05], [C("the stake on Amazon's books"), 0.9]],
         google=[[0, 0], [C("Google runs a similar loop"), 0], [C("Google runs a similar loop", 0.8), 1]], gloop=[[0, 0], [C("as investor, cloud supplier"), 0], [C("as investor, cloud supplier", 1.0), 1]],
         spin=[[0, 0], [C("the stake on Amazon's books"), 0], [C("the stake on Amazon's books", 0.8), 0.8]]),
    "cam": cam((0, 900, 540, 1.05), (C("Anthropic sends cash back"), 900, 600, 1.05, 1.0), (C("When Amazon sells Claude"), 600, 560, 1.0, 1.2),
               (C("And when Anthropic's value rises"), 760, 420, 1.05, 1.0), (C("Google runs a similar loop"), 1100, 540, 0.9, 1.2)), "drift": 2,
    "items": [CARI("pichai", 1840, C("Google runs a similar loop"), y=1040, scale=0.9, pose="stand", flip=True, label="SUNDAR PICHAI · ALPHABET CEO", labelUntil=C("as investor, cloud supplier", 2.5)),
              words("THE MONEY LOOP", 960, 180, 0.3, size=60, until=C("Amazon sends cash to Anthropic")),
              words("1 · INVESTMENT IN", 960, 180, C("Amazon sends cash to Anthropic"), size=56, until=C("Anthropic sends cash back")),
              words("2 · COMPUTE BILLS OUT = AMAZON SALES", 960, 180, C("Anthropic sends cash back"), size=46, until=C("When Amazon sells Claude")),
              words("3 · CLAUDE SOLD VIA THE CLOUD, MINUS A CUT", 960, 180, C("When Amazon sells Claude"), size=42, until=C("And when Anthropic's value rises")),
              words("4 · THE STAKE GROWS, ON PAPER", 960, 180, C("And when Anthropic's value rises"), size=50, until=C("Google runs a similar loop")),
              words("GOOGLE: A SIMILAR LOOP", 960, 180, C("Google runs a similar loop"), size=54),
              tag((0, "MECHANISM · FROM FILINGS (424B4, AMAZON 10-Q)"), (C("When Amazon sells Claude"), "FACT · CLOUD MARKETPLACES = 44% OF REVENUE (JAN-SEP 2026)"),
                  (C("And when Anthropic's value rises"), "FACT · AMAZON: +$62.8B GAINS IN 9M 2026 · 10-Q"), (C("Google runs a similar loop"), "FACT · GOOGLE ≥$121.3B HOSTING DEAL · 424B4"))]},
    sources=["amzn_10q", "ant_424b4"], sfx=[{"kind": "whoosh", "cue": "Watch the money move", "gain": 0.3}])
stage("s22_critics", "c4_critics", {
    **W1("ajcase", cards=[[C("Circular financing"), "CIRCULAR FINANCING?"], [C("demand can look stronger"), "DEMAND LOOKS BIGGER?"],
                          [C("everyone in the loop looks healthier"), "EVERYONE LOOKS HEALTHIER?"], [C("A rival has argued"), "REVENUE COUNTED IN FULL"],
                          [C("Some warn the risk"), "RISK ON SMALL INVESTORS?"], [C("And Anthropic's own filing warns"), "FILING: CONFLICTS OF INTEREST"]],
         strings=[[0, 0], [C("everyone in the loop looks healthier"), 0], [C("A rival has argued"), 1]], lens=[[0, 200], [C("A rival has argued"), 1300], [C("Some warn the risk"), 600], [C("And Anthropic's own filing warns"), 960]]),
    "cam": cam((0, 960, 520, 1.0), (C("A rival has argued"), 1300, 500, 1.15, 1.2), (C("Some warn the risk"), 760, 600, 1.1, 1.2), (C("And Anthropic's own filing warns"), 960, 560, 1.05, 1.2)), "drift": 2, "tone": "thriller",
    "items": [JUNE(500, C("like June"), face="worry", pose="stand", scale=1.0),
              tag((0, "CRITICISM · REUTERS (CIRCULAR RELATIONSHIP)"), (C("A rival has argued"), "REPORTED · OPENAI CRITICISM · AXIOS; GAAP ALLOWS BOTH"),
                  (C("Some warn the risk"), "OPINION · TECH POLICY PRESS"), (C("And Anthropic's own filing warns"), "FACT · 424B4 RISK FACTOR"))]},
    sources=["reuters_dep", "axios_rev", "tpp", "ant_424b4"], sfx=[{"kind": "hit", "cue": "Circular financing", "gain": 0.3}])
stage("s23_defense", "c4_defense", {
    **W1("ajloop", invest=1, compute=1, pay=1, resell=1, stake=0.6, google=1, gloop=1, spin=[[0, 0.8], [C("So the real question"), 0.8], [C("if the loop slowed down"), 0.2]],
         labels={"buy": "BUSINESSES PAY FOR CLAUDE"}),
    "cam": cam((0, 960, 540, 0.95), (C("most of Claude's paying customers"), 500, 600, 1.1, 1.2), (C("Suppliers lending to customers"), 960, 540, 0.95, 1.2), (C("So the real question"), 960, 520, 1.0, 1.0)), "drift": 2,
    "items": [words("THE CASH IS REAL", 960, 180, C("The cash is real"), size=58, until=C("most of Claude's paying customers")),
              words("MOSTLY ORDINARY BUSINESSES PAY", 960, 180, C("most of Claude's paying customers"), size=50, until=C("Counting cloud sales in full")),
              words("GROSS COUNTING: A STANDARD CHOICE", 960, 180, C("Counting cloud sales in full"), size=48, until=C("Suppliers lending to customers")),
              words("CARMAKERS LEND TO CAR BUYERS", 960, 180, C("Suppliers lending to customers"), size=50, until=C("And it's all disclosed")),
              words("ALL IN THE FILING", 960, 180, C("And it's all disclosed"), size=58, until=C("So the real question")),
              words("HOW MUCH GROWTH SURVIVES A SLOWER LOOP?", 960, 180, C("So the real question"), size=44),
              tag((0, "THE OTHER SIDE · ANALYSIS"), (C("most of Claude's paying customers"), "FACT · 11,900+ CUSTOMERS ≥$100K/YR; 56% OF REVENUE NOT VIA CLOUD MARKETPLACES · 424B4"),
                  (C("Counting cloud sales in full"), "FACT · 'PRINCIPAL ... GROSS BASIS' · 424B4"))]},
    sources=["ant_424b4", "axios_rev"])
stage("s24_twist", "c4_twist", {
    **W1("ajsupply", reveal=[[0, 0], [C("Google, Nvidia"), 0], [C("and the chipmaker TSMC"), 7]], flip=[[0, 0], [C("Most of them are"), 0], [C("part of the supply chain"), 7]],
         flow=[[0, 0], [C("The investors are often the suppliers"), 0], [C("The investors are often the suppliers", 1.0), 1]]),
    "cam": cam((0, 960, 560, 1.1), (C("Google, Nvidia"), 960, 520, 0.95, 1.2), (C("The investors are often the suppliers"), 960, 560, 1.0, 1.0)), "drift": 2,
    "items": [words("THE TWIST", 960, 200, 0.2, size=64, until=C("Google, Nvidia")),
              words("$26 BILLION AT $83 A SHARE", 960, 200, C("Google, Nvidia"), size=52, until=C("Most of them are")),
              words("INVESTORS = SUPPLIERS", 960, 200, C("The investors are often the suppliers"), size=62),
              tag((0, "FACT · PRIVATE PLACEMENT · 424B4"), (C("Most of them are"), "FACT · COMPUTE DEALS · 424B4; MICRON, TSMC INDIRECT"),
                  (C("part of what they put in"), "OUR ANALYSIS"))]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "The investors are often the suppliers", "gain": 0.35}])

# ====================================================================== CHAPTER 5
bumper("s25_b5", "c5_card", "CHAPTER FIVE", "Who got rich?", "Paper fortunes and locked doors", TEAL)
stage("s26_vc", "c5_vc", {
    **W1("ajcase", cards=[[C("Let's play detective"), "EARLY FUNDS"], [C("Let's play detective", 0.4), "AMAZON"], [C("Let's play detective", 0.8), "GOOGLE"],
                          [C("Let's play detective", 1.2), "FOUNDERS"], [C("Let's play detective", 1.6), "EMPLOYEES"], [C("Let's play detective", 2.0), "IPO BUYERS"]],
         strings=[[0, 0], [C("In Anthropic's first funding round"), 1]], lens=[[0, 100], [C("In Anthropic's first funding round"), 520]], paper=C("On paper")),
    "cam": cam((0, 960, 520, 1.0), (C("In Anthropic's first funding round"), 620, 420, 1.2, 1.2), (C("A small bet back then"), 960, 520, 1.0, 1.0)), "drift": 2,
    "items": [it("caricature", who="silhouette", x=1600, at=C("hypothetical early investor"), y=1040, scale=1.0, label="HYPOTHETICAL INVESTOR", labelUntil=C("On paper")),
              words("SERIES A ≈ $0.26 A SHARE", 960, 200, C("In Anthropic's first funding round"), size=56, until=C("A small bet back then")),
              words("≈ 378× AT THE FIRST CLOSE", 960, 200, C("A small bet back then"), size=58),
              tag((0, "HYPOTHETICAL INVESTOR · ILLUSTRATIVE"), (C("In Anthropic's first funding round"), "OUR CALC · SERIES A $2.57 ÷ ~10 SHARES · 424B4"),
                  (C("A small bet back then"), "OUR CALC · $97.17 ÷ ≈$0.26 · PAPER VALUE, BEFORE TAXES"))]},
    sources=["ant_424b4"])
stage("s27_giants", "c5_giants", {
    **W1("ajloop", invest=1, compute=0, pay=0, resell=0, stake=[[0, 0.1], [C("before the IPO it was already carrying"), 0.1], [C("many times what it paid"), 0.95]], google=0, gloop=0, spin=0),
    "cam": cam((0, 760, 520, 1.1), (C("before the IPO it was already carrying"), 600, 440, 1.2, 1.2), (C("But a paper gain"), 760, 520, 1.05, 1.0)), "drift": 2,
    "items": [words("AMAZON PUT IN ≈ $18 BILLION", 960, 180, C("Amazon bought its stake"), size=54, until=C("before the IPO it was already carrying")),
              words("CARRIED AT ≈ $239 BILLION (SEP 30)", 960, 180, C("before the IPO it was already carrying"), size=50, until=C("But a paper gain")),
              words("PAPER, UNTIL IT'S SOLD", 960, 180, C("But a paper gain"), size=58),
              tag((0, "FACT · AMAZON 10-Q Q3 2026"), (C("before the IPO it was already carrying"), "OUR CALC · PREFERRED $92.5B + NOTES $146.2B · 10-Q"),
                  (C("flowing into its reported profits"), "FACT · +$62.8B IN OTHER INCOME, 9M 2026 · 10-Q"))]},
    sources=["amzn_10q"])
stage("s28_staff", "c5_staff", {
    **W1("ajvault", days=180, crack=0, open=0, sign="EMPLOYEE STOCK"),
    "cam": cam((0, 700, 560, 1.05), (C("Reports say"), 960, 520, 1.0, 1.2)), "drift": 2,
    "items": [words("OPTIONS: BUY AT AN OLD, LOW PRICE", 960, 200, C("many paid partly in stock options"), size=48, until=C("Reports say")),
              words("400+ EMPLOYEES ≥ $100M EACH, ON PAPER", 960, 200, C("Reports say"), size=46),
              tag((0, "FACT · 1.77B OPTIONS, AVG EXERCISE $2.91 · 424B4"), (C("Reports say"), "REPORTED · CNBC, NOV 19, 2026"))]},
    sources=["ant_424b4", "cnbc_live"])
stage("s29_lock", "c5_lock", {
    **W1("ajvault", days=[[0, 180], [C("When the locks open"), 180], [C("When the locks open", 2.0), 0]], crack=[[0, 0], [C("When the locks open", 1.6), 0], [C("When the locks open", 2.4), 1]],
         open=[[0, 0], [C("When the locks open", 2.2), 0], [C("When the locks open", 3.4), 0.7]], sign=[[0, "LOCKUP: 180 DAYS"], [C("up to a year"), "BIG HOLDERS: UP TO 365 DAYS"]]),
    "cam": cam((0, 960, 520, 1.0), (C("A lockup keeps"), 1100, 520, 1.15, 1.2), (C("When the locks open"), 760, 560, 1.0, 1.2)), "drift": 2,
    "items": [words("ON PAPER ≠ IN THE BANK", 960, 180, 0.3, size=56, until=C("A lockup keeps")),
              words("A WAVE OF SELLERS?", 960, 180, C("When the locks open"), size=58),
              tag((0, "FACT · LOCK-UP TERMS · 424B4"), (C("When the locks open"), "FACT · ≈3.7B SHARES MAY UNLOCK EARLY; 10% OF EMPLOYEE SHARES FROM DAY 1 · 424B4"))]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "When the locks open", "gain": 0.3}])
stage("s30_june", "c5_june", {
    **W1("ajkitchen", app=[[0, "MY PORTFOLIO"]], price=97.17, chart=1, pill=[[0, "NO LOCKUP · SELL ANY TIME"]]),
    "cam": cam((0, 960, 560, 1.0), (C("The earliest backers paid"), 700, 560, 1.12, 1.2), (C("June paid full price"), 1100, 520, 1.1, 1.2), (C("Same share"), 960, 560, 1.0, 1.0)), "drift": 2,
    "items": [JUNE(560, 0.0, face="happy", pose="stand", hold="coffee", faces=[[0, "happy"], [C("June paid full price"), "squint"], [C("Very different bet"), "worry"]]),
              SHARE(860, 700, 0.0, mood=[[0, "happy"], [C("Very different bet"), "calm"]]),
              words("EARLY BACKERS: ≈ $0.26 A SHARE", 960, 230, C("The earliest backers paid"), size=50, until=C("June paid full price")),
              words("JUNE: $83 A SHARE", 960, 230, C("June paid full price"), size=60, until=C("Same share")),
              words("SAME SHARE. DIFFERENT BET.", 960, 230, C("Same share"), size=58),
              tag((0, "STORY · JUNE IS FICTIONAL"), (C("The earliest backers paid"), "OUR CALC · 424B4"))]},
    sources=["ant_424b4"])

# ====================================================================== CHAPTER 6
bumper("s31_b6", "c6_card", "CHAPTER SIX", "Is it worth the price?", "What a trillion-dollar price tag assumes", RED)
stage("s32_multiple", "c6_multiple", {
    **W1("ajmarket", price=97.17, chart=1, crowd=0.6, crawl=[[0, "FULLY DILUTED ≈ $1.75T · RUN RATE ≈ $81B"]]),
    "cam": cam((0, 960, 520, 0.95), (C("Compare the company's value"), 760, 420, 1.1, 1.2), (C("Not its profits"), 960, 520, 1.0, 1.0)), "drift": 2,
    "items": [words("VALUE ÷ SALES PACE ≈ 20×", 960, 210, C("The stock is priced at"), size=60, until=C("Not its profits")),
              words("SALES. NOT PROFITS.", 960, 210, C("Not its profits"), size=64),
              SHARE(1700, 860, 0.0, scale=0.75, mood=[[0, "calm"], [C("Not its profits"), "worry"]]),
              tag((0, "OUR CALC · ≈$1.75T ÷ ≈$81B ≈ 21.6× · EQUITY VALUE, NOT ENTERPRISE VALUE"))]},
    sources=["national", "ant_424b4"])
board("p33_need", "c6_need", "What the price assumes", "Let me draw what that price assumes", [
    S(rect(560, 360, 240, 560), "accent", C("Picture Anthropic years from now"), width=4, fill="accent", fillOpacity=0.4, kind="bar", label=lbl("VALUE ≈ $1.75T", 680, 340, 26, "ink")),
    S(arrow((900, 600), (1160, 600), -0.1), "ink", C("For today's price to look sensible"), width=6, kind="arrow", label=lbl("÷ 25 (A MATURE P/E)", 1030, 560, 20, "ink")),
    S(rect(1180, 700, 240, 220), "accent3", C("it would need profits"), width=4, fill="accent3", fillOpacity=0.4, kind="bar", label=lbl("≈ $70B PROFIT / YEAR", 1300, 680, 24, "ink")),
    S(rect(1500, 880, 240, 40), "risk", C("year after year"), width=4, fill="risk", fillOpacity=0.4, kind="bar", label=lbl("TODAY: OPERATING LOSS", 1620, 860, 22, "risk")),
    S(dot(1150, 1010), "muted", C("Let me draw what that price assumes"), width=1, label=lbl("HYPOTHETICAL · OUR CALCULATION · NOT A FORECAST", 1150, 1010, 20, "muted")),
], [{"kind": "point", "at": C("Picture Anthropic years from now", 0.3), "dur": 1.4, "target": [680, 600]}, {"kind": "react", "at": C("Not impossible", 0.1)}], sources=["national", "ant_424b4"])
ROADS = lambda **kw: W1("ajroads", **kw)
stage("s34_roads", "c6_roads", {
    **ROADS(focus=[[0, 0]], walk=0),
    "cam": cam((0, 960, 700, 1.25), (C("Several roads lead away"), 960, 540, 0.95, 1.6)), "drift": 2,
    "items": [words("THE FORK", 960, 200, 0.3, size=64, until=C("Several roads lead away")),
              words("NOBODY KNOWS THE ODDS", 960, 200, C("nobody knows the odds"), size=58),
              tag((0, "SCENARIOS · ILLUSTRATIVE · NO PROBABILITIES"))]})
stage("s35_bull", "c6_bull", {
    **ROADS(focus=[[0, 1]], walk=[[0, 0], [C("those huge contracts"), 0.6], [C("today's price could one day look cheap"), 1]]),
    "cam": cam((0, 900, 640, 1.05), (C("Anthropic keeps winning"), 700, 560, 1.1, 1.6), (C("On that road"), 520, 460, 1.15, 1.4)), "drift": 2,
    "items": [words("AI AS BASIC AS ELECTRICITY", 1300, 200, C("AI becomes as basic"), size=50, until=C("Anthropic keeps winning")),
              words("COSTS FALL · CONTRACTS = BARGAINS", 1300, 200, C("Anthropic keeps winning"), size=44, until=C("On that road")),
              words("TODAY'S PRICE: CHEAP?", 1300, 200, C("On that road"), size=56),
              tag((0, "BRIGHT ROAD · ILLUSTRATIVE SCENARIO"))]})
stage("s36_base", "c6_base", {
    **ROADS(focus=[[0, 2]], walk=[[0, 0], [C("because so much of the good news"), 0.9]]),
    "cam": cam((0, 960, 600, 1.05), (C("Anthropic becomes a big"), 960, 500, 1.15, 1.6)), "drift": 2,
    "items": [words("COMPETITION SQUEEZES PRICES", 960, 200, C("but competition squeezes"), size=50, until=C("Anthropic becomes a big")),
              words("BIG, HEALTHY, SLOW STOCK", 960, 200, C("Anthropic becomes a big"), size=52, until=C("because so much of the good news")),
              words("GOOD NEWS PAID FOR UP FRONT", 960, 200, C("because so much of the good news"), size=50),
              tag((0, "MIDDLE ROAD · ILLUSTRATIVE SCENARIO"))]})
stage("s37_bear", "c6_bear", {
    **ROADS(focus=[[0, 3]], focusAt3=0, walk=[[0, 0], [C("every new share it sells"), 1]]),
    "cam": cam((0, 1100, 600, 1.05), (C("Profits stay thin"), 1350, 500, 1.15, 1.6)), "drift": 2, "tone": "crisis",
    "items": [words("CHEAPER MODELS CATCH UP", 760, 200, C("cheaper models catch up"), size=50, until=C("the bills keep arriving")),
              words("THE BILLS KEEP ARRIVING", 760, 200, C("the bills keep arriving"), size=52, until=C("Profits stay thin")),
              words("MORE SHARES = SMALLER SLICE", 760, 200, C("every new share it sells"), size=50),
              tag((0, "DARK ROAD · ILLUSTRATIVE SCENARIO"), (C("every new share it sells"), "FACT · OPTIONS, NOTES, BENEFIT-FUND ISSUANCES CAN DILUTE · 424B4"))]},
    sources=["ant_424b4"], sfx=[{"kind": "hit", "cue": "Profits stay thin", "gain": 0.3}])

# ====================================================================== CHAPTER 7
bumper("s38_b7", "c7_card", "CHAPTER SEVEN", "The bigger question", "Who gets paid in a gold rush?", NAVY)
stage("s39_shovels", "c7_shovels", {
    **W1("ajgold", flow=[[0, 0], [C("the steadiest money"), 0], [C("the steadiest money", 1.0), 1]], twice=C("Some get paid twice")),
    "cam": cam((0, 760, 560, 1.0), (C("the shovel sellers are"), 1450, 520, 1.1, 1.4), (C("Some get paid twice"), 1450, 480, 1.2, 1.0)), "drift": 2,
    "items": [words("SELL THE SHOVELS", 960, 200, C("the steadiest money"), size=60, until=C("the shovel sellers are")),
              words("CHIPS · CLOUD · POWER", 960, 200, C("the shovel sellers are"), size=58, until=C("They get paid as long")),
              words("PAID WHILE THE BUILDING GOES ON", 960, 200, C("They get paid as long"), size=48),
              tag((0, "ANALYSIS · LIBRARY: THE COUNTRIES THAT COULD WIN THE AI ECONOMY WITHOUT BUILDING AI"))]})
stage("s40_answer", "c7_answer", {
    **W2("ajmarket", "ajscroll", {"price": 97.17, "chart": 1, "crowd": 0.7, "crawl": [[0, "WHAT DID WALL STREET BUY?"]]}, {"unroll": 1, "stamp": 0.2}),
    "cam": cam((0, 960, 520, 0.95), (C("Attached to a giant stack"), OX + 960, 540, 0.95, WHIP), (C("That doesn't make it a bubble"), 960, 540, 1.0, WHIP)), "drift": 2,
    "items": [words("REAL CUSTOMERS · REAL CASH", 960, 210, C("A share of one of the fastest-growing"), size=56, until=C("Attached to a giant stack")),
              words("+ A GIANT STACK OF PROMISES", OX + 960, 230, C("Attached to a giant stack"), size=54, until=C("That doesn't make it a bubble")),
              words("NOT A BUBBLE BY DEFINITION. NOT A SURE THING.", 960, 210, C("That doesn't make it a bubble"), size=42, until=C("It's a bet on how long")),
              words("A BET ON HOW LONG GROWTH LASTS", 960, 210, C("It's a bet on how long"), size=50),
              tag((0, "VERDICT · OUR ANALYSIS · NOT INVESTMENT ADVICE"))]})
stage("s41_close", "c7_close", {
    **W1("ajkitchen", app=[[0, "MY PORTFOLIO"]], price=97.17, chart=1, pill=[[0, "1 SHARE · ANT"]]),
    "cam": cam((0, 960, 560, 1.0), (C("June hasn't decided"), 760, 600, 1.15, 1.2), (C("The question isn't whether"), 960, 540, 1.0, 1.4)), "drift": 2,
    "items": [JUNE(560, 0.0, face="squint", pose="stand", hold="coffee", faces=[[0, "squint"], [C("June hasn't decided"), "smug"], [C("The question isn't whether"), "happy"]]),
              SHARE(860, 700, 0.0, mood=[[0, "calm"], [C("The question isn't whether"), "happy"]]),
              words("IMPORTANT ≠ PROFITABLE INVESTMENT", 960, 230, C("But importance and investment returns"), size=50, until=C("June hasn't decided")),
              words("HOW MUCH FUTURE IS ALREADY IN THE PRICE?", 960, 230, C("The question isn't whether"), size=44),
              tag((0, "VERDICT · NOT INVESTMENT ADVICE"), (C("June hasn't decided"), "STORY · JUNE IS FICTIONAL"))]})
add("s42_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description · Not investment advice", "brand_cue": {"cue": "This is The Hidden Economics"}})
stage("s43_button", "button", {
    **W1("ajkitchen", app=[[0, "MY PORTFOLIO"]], price=97.17, chart=1, pill=[[0, "MARKET CLOSED"]]),
    "cam": cam((0, 960, 600, 1.1), (3.0, 900, 600, 1.2, WHIP)), "drift": 0, "min_seconds": 6.0,
    "items": [JUNE([[0, 300], [2.2, 760]], 0.0, pose="walk", face="happy", poses=[[0, "walk"], [2.2, "stand"]], faces=[[0, "happy"], [3.2, "wink"]]),
              SHARE([[0, 1400], [2.6, 1040]], [[0, 700], [2.6, 560]], 0.0, mood=[[0, "calm"], [3.0, "wow"]]),
              bub("NIGHT SHIFT. YOU WATCH THE PRICE.", 760, 330, 3.2, tail=[760, 640], size=28)]},
    sfx=[{"kind": "hit", "at": 3.2, "gain": 0.3}])

# camera clamps + claim-pill conversion (same conventions as earlier generators)
TIGHT = {"ajcase", "ajvault", "ajsupply"}
HIGHWORDS = {"ajkitchen", "ajloop"}   # sets whose top half is busy: punchline words sit higher, camera stays wide
for _sc in cartoon_kit.scenes:
    _z = _sc["params"].get("zones") or []
    if _sc["type"] == "engine_cartoon" and len(_z) == 1 and _z[0]["set"] in TIGHT:
        for _k in _sc["params"].get("cam", []):
            _k["zoom"] = max(0.85, min(_k["zoom"], 1.2))
            _k["y"] = max(460, min(600, _k["y"]))
        _sc["params"]["drift"] = min(_sc["params"].get("drift", 3), 2)

TAGCOL = {"FACT": "green", "OUR": "gold", "REPORTED": "gold", "OPINION": "gold", "CRITICISM": "gold", "HYPOTHETICAL": "gold", "VERDICT": "gold", "ANALYSIS": "gold",
          "MECHANISM": "white", "STORY": "white", "SCENARIOS": "gold", "BRIGHT": "gold", "MIDDLE": "gold", "DARK": "gold", "THE": "white", "LIBRARY": "white"}
for _sc in cartoon_kit.scenes:
    if _sc["type"] != "engine_cartoon":
        continue
    P = _sc["params"]
    _sets = {z["set"] for z in P.get("zones") or []}
    for _k in P.get("cam", []):
        _k["zoom"] = min(_k["zoom"], 1.3)
        _k["y"] = max(380, min(700, _k["y"]))
        if "ajloop" in _sets:
            _k["zoom"] = min(_k["zoom"], 1.0)
            _k["y"] = max(540, _k["y"])
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
            _it["hud"] = True
            if _it["x"] > 1500:
                _it["x"] -= OX
        if _it.get("kind") in ("toonwords", "sign", "bubble") and isinstance(_it.get("y"), (int, float)) and _it["y"] < 180:
            _it["y"] = 180
        if _it.get("kind") == "toonwords" and _sets & HIGHWORDS:
            _it["y"] = 118
            _it["size"] = min(_it["size"], 50)
        if _it.get("kind") == "caricature" and "ajloop" in _sets:
            _it["y"] = 985
        keep.append(_it)
    P["items"] = keep

write(OUT, "# GENERATED by tools/gen_antipo_storyboard.py; edit the generator, not this file.\n"
           "# Episode 72 storyboard (Anthropic's $1.5 Trillion IPO): bespoke worlds in CartoonStage/antipo.tsx.\n")

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
