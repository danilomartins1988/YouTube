"""Generates projects/the-day-volkswagen-became-the-most-valuable-company/deliverables/documentary/storyboard.yaml (Episode 13).

Bespoke CartoonStage worlds for the 2008 Volkswagen short squeeze: the Frankfurt trading floor with a split-flap board
and a price counter that runs away, a car plant whose line stops when demand collapses, a hedge-fund trading room
(office set, night), a small sports-car maker next to a giant carmaker's tower, the state government building, a
newsroom printing Sunday's press release, a 10x10 grid of share certificates that shows who owns what (and the dashed
red certificates the short sellers owe), the index board that gets capped, and a courtroom. Four presenter boards:
short selling, the squeeze arithmetic, the index basket, the lesson. No logos, no real people drawn (names in text only).
Legal care: "Porsche denied", "acquitted", "neither false nor misleading".
Run: python tools/gen_volkswagen_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-day-volkswagen-became-the-most-valuable-company/deliverables/documentary/storyboard.yaml"

F = 860
VW = lambda x=960, **kw: it("tower", x=x, text="VOLKSWAGEN", color="#64B5F6", **kw)
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
GRN, RED, GOLD, BLUE, GREY = "#7BD389", "#FF8A80", "#FFC93C", "#64B5F6", "#CFD8DC"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def grid(x=960, y=420, at=0.2, porsche=None, lsax=None, free=None, owed=None, **kw):
    """The 100-share grid: Porsche (74, gold), Lower Saxony (20, green), free float (6, white); owed = dashed red column."""
    g = []
    if porsche is not None:
        g.append({"n": 74, "color": GOLD, "label": "PORSCHE ≈ 74", "at": porsche, "step": 0.015})
    if lsax is not None:
        g.append({"n": 20, "color": GRN, "label": "LOWER SAXONY 20", "at": lsax, "step": 0.03})
    if free is not None:
        g.append({"n": 6, "color": "#FFFFFF", "label": "FOR SALE < 6", "at": free, "step": 0.12})
    p = {"x": x, "y": y, "at": at, "groups": g, **kw}
    if owed is not None:
        p["owed"] = owed
    return it("shares", **p)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 470, "zoom": 1.2}, {"at": C("most valuable"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("chart", x=960, y=360, w=900, h=420, at=0.3, dur=4.5, text="VW SHARE PRICE · OCT 2008", pts=[0.12, 0.1, 0.11, 0.09, 0.12, 0.6, 0.97]),
              *crowd([330, 460, 1480, 1610], "worry", at=0.5, until=C("most valuable", 0.5)),
              *crowd([330, 460, 1480, 1610], "run", at=C("most valuable", 0.6)),
              it("burst", x=1350, y=170, at=C("most valuable", 0.4)),
              it("clock", x=1700, y=250, at=C("For about a day", -0.2), period=2.0, scale=0.6)],
    "callouts": [co("A carmaker in a crisis…", 960, 150, C("a carmaker"), "white", screen=True, size=44, until=C("most valuable", -0.3)),
                 co("…the most valuable company in the world?", 960, 150, C("most valuable"), "gold", screen=True, size=44, until=C("For about a day", -0.3)),
                 co("For about a day", 960, 960, C("For about a day"), "risk", screen=True, size=48)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 700, "y": 540, "zoom": 1.0}, {"at": C("For a brief moment"), "x": 1700, "y": 500, "zoom": 1.0, "dur": 2.6},
            {"at": C("How many shares"), "x": 1300, "y": 540, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "OCT", "2008"]], scale=0.8),
              it("counter", x=760, y=520, at=0.3, prefix="$", steps=[[0, 266], [{"cue": "jumped"}, 266], [{"cue": "jumped", "offset": 3.5}, 1250]], text="ONE VW SHARE"),
              it("board", x=1750, y=180, w=820, at=C("For a brief moment", -0.4), text="WORLD'S MOST VALUABLE",
                 rows=[{"name": "#1 EXXONMOBIL", "value": "$343bn"}],
                 swap={"at": C("more than ExxonMobil"), "out": 0, "in": {"name": "#1 VOLKSWAGEN", "value": "≈ $370bn", "color": "gold"}}),
              it("device", type="car", x=1750, y=F, at=C("Nothing about its cars"), scale=1.1),
              it("letters", x=1300, y=330, text="?", at=C("How many shares"), size=150, color="gold")],
    "callouts": [co("{{price.display}} → {{price.peak_display}} per share", 960, 960, C("jumped"), "gold", screen=True, size=44, sub="24 → 28 Oct 2008, converted at each day's Fed rate",
                    until=C("For a brief moment", -0.3)),
                 co("Briefly worth {{top.display}}", 960, 960, C("For a brief moment"), "gold", screen=True, size=44, sub="ExxonMobil: {{top.exxon_display}}",
                    until=C("Nothing about its cars", -0.3)),
                 co("The cars didn't change", 960, 960, C("Nothing about its cars"), "white", screen=True, until=C("How many shares", -0.3)),
                 co("How many shares were left?", 960, 960, C("How many shares"), "risk", screen=True, size=48)]},
    sources=["risk_options", "ib_squeeze", "fed_h10"], sfx=[{"kind": "hit", "cue": "more than ExxonMobil", "gain": 0.3}])

# ====================================================================== PART 1: the bet against Volkswagen
card("s03_c1", "m1_card", "The Bet Against Volkswagen", "Why so many sold shares they didn't own")
stage("s04_q1", "m1_question", {
    "zones": [Z("office", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 1.2}, {"at": C("would fall"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("desk", x=560, glow="green"), it("desk", x=1360, glow="cyan"),
              *crowd([490], "type", glasses=True, tie=True, scale=0.95), *crowd([1290], "phone", tie=True, scale=0.95),
              it("chart", x=960, y=300, w=640, h=320, at=C("would fall"), dur=3, text="BET: VW GOES DOWN", pts=[0.8, 0.7, 0.72, 0.55, 0.5, 0.35, 0.25], color="risk"),
              it("arrow", **{"from": [1500, 300], "to": [1650, 520]}, at=C("would fall", 0.6), color="risk", text="DOWN?")],
    "callouts": [co("Why bet against Volkswagen?", 960, 960, C("professional investors"), "gold", screen=True, size=46)]})
# ---- PRESENTER A: short selling
add("p05_short", "m1_draw", "engine_draw", {
    "title": "How to bet against a share", "board": BOARD, "draw_start": C("you borrow a share"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(520, 360, 240, 100), "color": "accent2", "width": 5, "start": C("you borrow a share"), "label": lbl("1 · BORROW", 640, 420, 28, "accent2")},
        {"d": arrow((770, 410), (850, 410)), "color": "ink", "width": 4, "start": C("you sell it")},
        {"d": rect(860, 360, 240, 100), "color": "accent", "width": 5, "start": C("you sell it", 0.3), "label": lbl("2 · SELL NOW", 980, 420, 28, "accent")},
        {"d": arrow((1110, 410), (1190, 410)), "color": "ink", "width": 4, "start": C("you buy a share back")},
        {"d": rect(1200, 360, 280, 100), "color": "accent3", "width": 5, "start": C("you buy a share back", 0.3), "label": lbl("3 · BUY BACK", 1340, 420, 28, "accent3")},
        {"d": arrow((1340, 470), (700, 470), 0.25), "color": "accent2", "width": 4, "start": C("return it")},
        {"d": "M 600 600 L 700 600 L 780 680 L 860 760", "color": "accent3", "width": 7, "start": C("If the price has fallen"), "label": lbl("price falls: profit", 760, 820, 26, "accent3")},
        {"d": "M 1100 760 L 1180 700 L 1260 640 L 1340 520 L 1400 330", "color": "risk", "width": 8, "start": C("rises instead"), "label": lbl("price rises: loss", 1230, 820, 26, "risk")},
        {"d": arrow((1400, 330), (1430, 250)), "color": "risk", "width": 8, "start": C("without any limit"), "label": lbl("NO LIMIT", 1560, 280, 34, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("the catch", 0.3), "dur": 1.4, "target": [1340, 520]}, {"kind": "react", "at": C("without any limit", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["ib_squeeze"])
stage("s06_why", "m1_why", {
    "zones": [Z("carplant", -1600, 2100, idle=0), Z("office", 2100, 6000)], "worldW": 3800,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Many hedge funds", -0.5), "x": 2850, "y": 540, "zoom": 1.0, "dur": 2.6},
            {"at": C("demand for new cars"), "x": 900, "y": 540, "zoom": 1.0, "dur": 2.4}, {"at": C("If you wanted"), "x": 2850, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("conveyor", x0=200, x1=1700, y=F - 40, at=0, n=6, speed=110, stopAt=C("collapsed"), goods="car"),
              it("sign", x=900, y=330, text="DEBT", sub="a carmaker carrying a lot of it", at=C("a lot of debt"), color="#FFCDD2", size=40, hang=True, swing=True),
              it("storm", x=[[0, 1700], [20, 600]], y=150, at=C("the financial crisis")),
              it("sign", x=900, y=520, text="DEMAND COLLAPSES", at=C("collapsed"), color="#FFCDD2", size=36),
              it("desk", x=2600, glow="green"), it("desk", x=3150, glow="cyan"),
              *crowd([2530, 3080], "type", at=0.2, tie=True),
              it("chart", x=2850, y=330, w=620, h=320, at=C("too expensive"), dur=2.5, text="VW: “TOO EXPENSIVE”", pts=[0.3, 0.45, 0.6, 0.75, 0.85]),
              *crowd([2850], "point", at=C("If you wanted", 0.3), glasses=True, tie=True)],
    "callouts": [co("A carmaker with a lot of debt", 960, 150, C("a lot of debt"), "risk", screen=True, until=C("Many hedge funds", -0.3)),
                 co("Hedge funds: the shares are too expensive", 960, 150, C("Many hedge funds"), "white", screen=True, until=C("demand for new cars", -0.3)),
                 co("Crisis: demand for new cars collapses", 960, 150, C("demand for new cars"), "risk", screen=True, until=C("If you wanted", -0.3)),
                 co("Looks like a perfect short", 960, 150, C("If you wanted"), "gold", screen=True, size=44)]},
    sources=["ib_squeeze"])
stage("s07_porsche", "m1_porsche", {
    "zones": [Z("district", -1600, 1900), Z("parliament", 1900, 6000, cx=2400)], "worldW": 3400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("By March"), "x": 1300, "y": 500, "zoom": 0.95, "dur": 2.4},
            {"at": C("The state of Lower Saxony", -0.4), "x": 2350, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("building", x=520, style="office", color="#FFE082", text="PORSCHE", scale=0.55, at=C("Porsche the sports car")),
              it("device", type="car", x=760, y=F, at=C("sports car maker"), scale=0.8, color="red"),
              VW(1400, scale=1.2, h=620),
              it("coins", **{"from": [520, 520], "to": [1400, 360]}, at=C("kept buying"), rate=4, arc=220),
              it("counter", x=1400, y=330, at=C("By March"), steps=[[{"cue": "By March"}, 0], [{"cue": "By March", "offset": 2.2}, 31]], suffix="%", text="PORSCHE'S STAKE"),
              it("letters", x=820, y=230, text="75%?", at=C("seventy-five percent"), size=90, color="gold", until=C("The state of Lower Saxony")),
              it("sign", x=2400, y=200, text="LOWER SAXONY", sub="state parliament", at=C("The state of Lower Saxony", -0.2), color="#C8E6C9", size=40),
              it("sign", x=2400, y=360, text="20% OF VOLKSWAGEN", at=C("owned"), color="#FFF59D", size=34),
              *crowd([2800], "shrug", at=C("simply weren't enough"), tie=True)],
    "callouts": [co("Porsche keeps buying", 960, 150, C("kept buying"), "gold", screen=True, until=C("By March", -0.3)),
                 co("March 2008: {{march.display}} of Volkswagen", 960, 960, C("By March"), "gold", screen=True, size=42, until=C("Porsche said", -0.3)),
                 co("Porsche: 75% is very unlikely", 960, 960, C("Porsche said"), "white", screen=True, until=C("The state of Lower Saxony", -0.3)),
                 co("Lower Saxony owns {{march.lsax_display}}", 960, 150, C("The state of Lower Saxony"), "white", screen=True, size=42, sub="Volkswagen's second largest shareholder")]},
    sources=["ib_squeeze"])
kinetic("s08_t1", "m1_transition", [("A weak carmaker · a crisis · plenty of shares", 48, "A weak carmaker", None, True), ("Or so everyone thought", 80, "Or so everyone", "risk", False)])

# ====================================================================== PART 2: the Sunday announcement
card("s09_c2", "m2_card", "The Sunday Announcement", "26 October 2008")
stage("s10_q2", "m2_question", {
    "zones": [Z("newsroom", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("press", x=1300, at=0.3, runAt=2.5, text="PRINTING"),
              it("magnifier", x=[[0, 300], [8, 900]], y=420, at=0.4, text="?", scale=0.9),
              *crowd([560], "read", at=0.3, glasses=True, tie=True)],
    "callouts": [co("What did they not know?", 960, 150, C("What did"), "gold", screen=True, size=46)]})
stage("s11_sunday", "m2_sunday", {
    "zones": [Z("newsroom", -1600, 1500), Z("office", 1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.05}, {"at": C("And on top of that", -0.5), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "SUN", "26 OCT 2008"]], scale=0.8),
              it("press", x=900, at=0.3, runAt=C("press release")),
              it("paper", x=900, y=420, at=C("press release", 0.8), text="PORSCHE", sub="holdings in Volkswagen", size=44, scale=0.8, until=C("And on top of that")),
              grid(2300, 400, at=C("It said"), porsche=C("ordinary shares"), owed=None, scale=0.75),
              it("letters", x=2900, y=230, text="74.1%", at=C("Together"), size=90, color="gold"),
              it("sign", x=2300, y=780, text="75% IN 2009", sub="Porsche's stated aim", at=C("Its aim"), color="#FFF59D", size=36)],
    "callouts": [co("Shares: {{stake.shares_display}}", 960, 150, C("ordinary shares"), "gold", screen=True, size=44, until=C("And on top of that", -0.3)),
                 co("+ cash-settled options: {{stake.options_display}}", 960, 150, C("And on top of that"), "gold", screen=True, size=42, sub="contracts linked to VW's share price", until=C("Together", -0.3)),
                 co("Together: {{stake.display}}", 960, 150, C("Together"), "gold", screen=True, size=48, sub="Porsche SE press release, 26 Oct 2008")]},
    sources=["porsche_oct26"], sfx=[{"kind": "hit", "cue": "Together", "gain": 0.3}])
stage("s12_options", "m2_options", {
    "zones": [Z("office", night=True)], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.05}, {"at": C("Now the market"), "x": 1350, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("docs", x=650, y=F, at=0.2, text="OPTIONS", stampAt=C("protect it"), stamp="HEDGE", color="orange"),
              it("calendar", x=330, y=300, at=C("Only a few weeks"), pages=[[0, "16 SEP", "≈ 35%"]], scale=0.75),
              it("magnifier", x=[[0, 1000], [{"cue": "Now the market"}, 1000], [{"cue": "Now the market", "offset": 4}, 1500]], y=480, at=C("Now the market"), scale=0.9),
              *crowd([1250, 1400, 1550, 1700], "worry", at=C("very different"), tie=True),
              it("letters", x=1500, y=300, text="!?", at=C("very different", 0.3), size=110, color="risk")],
    "callouts": [co("The surprise: the options", 960, 150, C("Those options"), "gold", screen=True, until=C("Only a few weeks", -0.3)),
                 co("September: ≈ 35% disclosed", 960, 150, C("Only a few weeks"), "white", screen=True, sub="Risk.net (35.14%, 16 Sep 2008)", until=C("Now the market", -0.3)),
                 co("Not what the short sellers believed", 960, 150, C("very different"), "risk", screen=True)]},
    sources=["porsche_oct26", "risk_options"])
# ---- PRESENTER B: the squeeze in 100 shares
add("p13_hundred", "m2_draw", "engine_draw", {
    "title": "The problem, in 100 shares", "board": BOARD, "draw_start": C("Porsche about"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 540 760 L 540 360 L 640 360 L 640 760", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.35, "kind": "bar", "start": C("Porsche about"), "label": lbl("PORSCHE ≈ 74", 590, 810, 24, "accent")},
        {"d": "M 720 760 L 720 650 L 820 650 L 820 760", "color": "accent3", "width": 5, "fill": "accent3", "fillOpacity": 0.35, "kind": "bar", "start": C("Lower Saxony twenty"), "label": lbl("STATE 20", 770, 810, 24, "accent3")},
        {"d": "M 900 760 L 900 727 L 1000 727 L 1000 760", "color": "ink", "width": 5, "fill": "ink", "fillOpacity": 0.15, "kind": "bar", "start": C("Less than six"), "label": lbl("FOR SALE < 6", 950, 810, 24, "ink")},
        {"d": "M 1180 760 L 1180 694 L 1280 694 L 1280 760", "color": "risk", "width": 6, "dash": "12 8", "kind": "bar", "start": C("Around twelve"), "label": lbl("OWED ≈ 12", 1230, 810, 24, "risk")},
        {"d": "M 1040 700 L 1140 700", "color": "risk", "width": 6, "start": C("Twelve shares owed"), "label": lbl("6  <  12", 1090, 650, 34, "risk")},
        {"d": dot(1450, 450), "color": "risk", "width": 1, "start": C("short squeeze"), "label": lbl("SHORT SQUEEZE", 1450, 460, 40, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Twelve shares owed", 0.3), "dur": 1.4, "target": [1090, 700]}, {"kind": "react", "at": C("short squeeze", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["porsche_oct26", "ib_squeeze"])
kinetic("s14_t2", "m2_transition", [("Monday morning", 72, "On Monday morning", None, False), ("everyone who owed shares went looking for the same few", 40, "everyone who owed", "risk", True)])

# ====================================================================== PART 3: the squeeze
card("s15_c3", "m3_card", "The Squeeze", "Everyone must buy. Almost no one can sell.")
stage("s16_q3", "m3_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.15}, {"at": 3.0, "x": 1060, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [grid(860, 420, at=0.1, porsche=0.2, lsax=0.9, free=1.6, owed={"n": 12, "at": 2.6, "label": "OWED ≈ 12", "shakeAt": 4.0}, scale=0.8)],
    "callouts": [co("Everyone must buy, almost no one can sell", 960, 960, C("What happens"), "risk", screen=True, size=40)]})
stage("s17_spike", "m3_spike", {
    "zones": [Z("exchange")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.0}, {"at": C("Short sellers were not buying"), "x": 1400, "y": 560, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "shake": [{"at": C("it touched"), "dur": 1.6, "amp": 10}],
    "items": [it("counter", x=700, y=300, at=0.3, prefix="$", steps=[[0, 266], [{"cue": "By Tuesday"}, 266], [{"cue": "it touched", "offset": 1.0}, 1250]], text="ONE VW SHARE"),
              it("calendar", x=1120, y=280, at=0.3, pages=[[0, "FRI", "24 OCT"], [C("By Tuesday"), "TUE", "28 OCT"]], scale=0.75),
              it("chart", x=1700, y=360, w=640, h=380, at=C("By Tuesday", -0.5), dur=3, text="VW", pts=[0.08, 0.1, 0.12, 0.3, 0.55, 0.96]),
              *crowd([620, 740, 860, 980, 1100, 1220], "run", at=C("Short sellers were not buying"), tie=True),
              it("coins", **{"from": [900, 600], "to": [1700, 400]}, at=C("they had to"), rate=6, until=C("even bigger", 1.5))],
    "callouts": [co("Friday: {{price.display}}", 960, 960, C("On Friday"), "white", screen=True, size=44, until=C("By Tuesday", -0.3)),
                 co("Tuesday 28 Oct: {{price.peak_display}}", 960, 960, C("By Tuesday"), "gold", screen=True, size=46, sub="converted at each day's Fed rate", until=C("Short sellers were not buying", -0.3)),
                 co("Not buying because they liked it: because they had to", 960, 960, C("Short sellers were not buying"), "risk", screen=True, until=C("Every purchase", -0.3)),
                 co("Every purchase pushes the price higher", 960, 960, C("Every purchase"), "risk", screen=True)]},
    sources=["risk_options", "porsche_oct29", "fed_h10"], sfx=[{"kind": "hit", "cue": "it touched", "gain": 0.35}])
stage("s18_top", "m3_top", {
    "zones": [Z("district")], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 1100, "y": 420, "zoom": 0.9}, {"at": C("A carmaker in the middle"), "x": 1100, "y": 380, "zoom": 0.82, "dur": 2.8}], "drift": 0,
    "items": [it("tower", x=1500, text="EXXONMOBIL", color="#B0BEC5", h=480, scale=1.0, at=C("ExxonMobil the giant", -0.4)),
              VW(800, scale=1.0, h=[[0, 260], [{"cue": "were worth"}, 260], [{"cue": "were worth", "offset": 3}, 540]]),
              it("board", x=1150, y=-60, w=880, at=C("A carmaker in the middle", -0.2), text="#1 ON 28 OCT 2008",
                 rows=[{"name": "#1 EXXONMOBIL", "value": "$343bn"}],
                 swap={"at": C("on paper"), "out": 0, "in": {"name": "#1 VOLKSWAGEN", "value": "≈ $370bn", "color": "gold"}}),
              it("burst", x=800, y=200, at=C("on paper", 0.8))],
    "callouts": [co("VW's voting shares: {{top.display}}", 960, 960, C("were worth"), "gold", screen=True, size=44, sub="converted at the Fed rate of 28 Oct 2008", until=C("ExxonMobil the giant", -0.3)),
                 co("ExxonMobil: {{top.exxon_display}}", 960, 960, C("ExxonMobil the giant"), "white", screen=True, size=44, until=C("A carmaker in the middle", -0.3)),
                 co("On paper: #1 on the planet", 960, 960, C("on paper"), "gold", screen=True, size=46, sub="very briefly (International Banker)")]},
    sources=["ib_squeeze", "fed_h10"], sfx=[{"kind": "hit", "cue": "on paper", "gain": 0.3}])
stage("s19_tears", "m3_tears", {
    "zones": [Z("office", -1600, 1700, night=True), Z("district", 1700, 6000)], "worldW": 3600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.05}, {"at": C("And Germany's financial regulator", -0.5), "x": 2500, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("desk", x=560, glow="red"), it("desk", x=1160, glow="red"),
              *crowd([490, 1090], "phone", at=0.2, tie=True), *crowd([800], "worry", at=C("in tears"), tie=True),
              it("letters", x=800, y=330, text="T_T", at=C("in tears", 0.2), size=80, color="blue", until=C("And Germany's financial regulator", 2)),
              it("building", x=2350, style="gov", color="#FFE082", text="REGULATOR", scale=0.75, at=C("BaFin", -0.4)),
              it("magnifier", x=[[0, 2600], [{"cue": "examining"}, 2600], [{"cue": "examining", "offset": 4}, 2950]], y=480, at=C("examining"), scale=0.8),
              it("sign", x=3000, y=360, text="PORSCHE: “WE DENY IT”", at=C("Porsche denied"), color="#FFF59D", size=34)],
    "callouts": [co("“Hedge fund managers literally in tears”", 960, 150, C("in tears"), "white", screen=True, sub="a London analyst, 29 Oct (International Banker)", until=C("And Germany's financial regulator", -0.3)),
                 co("BaFin examines the trading", 960, 150, C("And Germany's financial regulator"), "white", screen=True, sub="insider trading or manipulation? (an examination, not a finding)", until=C("Porsche denied", -0.3)),
                 co("Porsche denied all of it", 960, 150, C("Porsche denied"), "gold", screen=True, size=44)]},
    sources=["ib_squeeze", "risk_options", "porsche_oct29"])
kinetic("s20_t3", "m3_transition", [("A price like that could not last", 54, "A price like that", None, True), ("Who would let the air out?", 76, "who would let", "accent", False)])

# ====================================================================== PART 4: letting the air out
card("s21_c4", "m4_card", "Letting the Air Out", "Two moves, one week")
stage("s22_q4", "m4_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 460, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("chart", x=960, y=380, w=860, h=420, at=0.2, dur=3, text="VW", pts=[0.1, 0.12, 0.5, 0.95, 0.96, 0.95], color="risk"),
              it("letters", x=1500, y=260, text="?", at=C("How do you stop"), size=140, color="gold")],
    "callouts": [co("How do you stop a squeeze?", 960, 960, C("How do you stop"), "gold", screen=True, size=46)]})
stage("s23_porsche", "m4_porsche", {
    "zones": [Z("district")], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.05}, {"at": C("it would settle"), "x": 1350, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "WED", "29 OCT"]], scale=0.75),
              it("building", x=760, style="office", color="#FFE082", text="PORSCHE", scale=0.65),
              it("paper", x=760, y=330, at=C("short sellers were responsible"), text="“SHORT SELLERS ARE RESPONSIBLE”", sub="Porsche SE press release", size=34, scale=0.75, until=C("it would settle")),
              it("coins", **{"from": [760, 520], "to": [1900, 600]}, at=C("it would settle", 0.3), rate=5, shape="note", until=C("needed them", 1.5)),
              *crowd([1800, 1920, 2040], "cheer", at=C("within reach"), tie=True),
              it("sign", x=1350, y=360, text="UP TO 5% RELEASED", at=C("it would settle", 0.3), color="#C8E6C9", size=36, hang=True, swing=True),
              it("building", x=2450, style="gov", color="#FFE082", text="REGULATOR", scale=0.6, at=C("informed the regulator", -0.3))],
    "callouts": [co("Porsche: short sellers are responsible", 960, 150, C("short sellers were responsible"), "white", screen=True, until=C("it would settle", -0.3)),
                 co("Porsche settles options on {{settle.display}} of VW shares", 960, 150, C("it would settle"), "gold", screen=True, size=40, until=C("informed the regulator", -0.3)),
                 co("The regulator was told in advance", 960, 150, C("informed the regulator"), "white", screen=True, sub="according to Porsche")]},
    sources=["porsche_oct29", "ib_squeeze"])
stage("s24_index", "m4_index", {
    "zones": [Z("exchange")], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.1}, {"at": C("capped"), "x": 960, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("board", x=960, y=60, w=1100, at=0.3, text="DAX · WEIGHT IN THE INDEX",
                 rows=[{"name": "VOLKSWAGEN", "value": "27%", "color": "red"}, {"name": "29 OTHER COMPANIES", "value": "73%"}],
                 swap={"at": C("capped"), "out": 0, "in": {"name": "VOLKSWAGEN (CAPPED)", "value": "10%", "color": "gold"}}),
              *crowd([520, 1400], "point", at=C("Volkswagen alone"), tie=True),
              *crowd([960], "cheer", at=C("capped", 0.5), tie=True)],
    "callouts": [co("Deutsche Börse runs the DAX", 960, 960, C("Deutsche Börse"), "white", screen=True, until=C("Volkswagen alone", -0.3)),
                 co("VW alone: {{dax_cap.weight_display}} of the index", 960, 960, C("Volkswagen alone"), "risk", screen=True, size=44, sub="at Tuesday's close", until=C("capped", -0.3)),
                 co("Cap: {{dax_cap.display}}", 960, 960, C("capped"), "gold", screen=True, size=48, sub="brought forward to Monday 3 November")]},
    sources=["dbg_cap"], sfx=[{"kind": "hit", "cue": "capped", "gain": 0.3}])
# ---- PRESENTER C: the index basket
add("p25_basket", "m4_draw", "engine_draw", {
    "title": "Why the cap mattered", "board": BOARD, "draw_start": C("An index is like a basket"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": "M 560 420 L 1000 420 L 950 700 L 610 700 Z", "color": "border", "width": 6, "start": C("An index is like a basket"), "label": lbl("THE INDEX BASKET", 780, 760, 26, "muted")},
        {"d": "M 640 420 m -30 0 a 30 30 0 1 0 60 0 a 30 30 0 1 0 -60 0 M 730 420 m -30 0 a 30 30 0 1 0 60 0 a 30 30 0 1 0 -60 0 M 820 420 m -30 0 a 30 30 0 1 0 60 0 a 30 30 0 1 0 -60 0",
         "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "start": C("basket of companies")},
        {"d": rect(1100, 380, 300, 100), "color": "accent2", "width": 5, "start": C("Many funds simply copy"), "label": lbl("FUNDS COPY IT", 1250, 440, 26, "accent2")},
        {"d": "M 920 420 m -70 0 a 70 70 0 1 0 140 0 a 70 70 0 1 0 -140 0", "color": "risk", "width": 6, "fill": "risk", "fillOpacity": 0.3, "start": C("a giant slice"), "label": lbl("VW 27%", 920, 430, 26, "risk")},
        {"d": arrow((1250, 490), (1000, 560), 0.2), "color": "risk", "width": 5, "start": C("need more of it"), "label": lbl("buy more VW", 1180, 600, 24, "risk")},
        {"d": "M 1100 760 L 1400 760", "color": "accent", "width": 10, "start": C("Cap the slice"), "label": lbl("CAP: 10%", 1250, 730, 34, "accent")},
        {"d": dot(1250, 830), "color": "accent3", "width": 1, "start": C("pressure eases"), "label": lbl("pressure eases", 1250, 840, 26, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("a giant slice", 0.3), "dur": 1.4, "target": [920, 420]}, {"kind": "smile", "at": C("pressure eases"), "dur": 1.4}],
    "scale": 0.86, "floor": 1040}, sources=["dbg_cap"])
stage("s26_fall", "m4_fall", {
    "zones": [Z("exchange", -1600, 1700), Z("office", 1700, 6000, night=True)], "worldW": 3400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But for many short sellers"), "x": 2500, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 0,
    "items": [it("chart", x=900, y=380, w=760, h=420, at=0.2, dur=2, text="VW", pts=[0.1, 0.12, 0.5, 0.95], crashAt=C("closed at")),
              it("counter", x=900, y=760, at=C("closed at"), prefix="$", steps=[[{"cue": "closed at"}, 1250], [{"cue": "closed at", "offset": 2}, 660]], text="WEDNESDAY CLOSE",
                 until=C("Within four days", 3)),
              it("letters", x=1300, y=320, text="−58%", at=C("Within four days"), size=80, color="risk", until=C("A month later")),
              it("letters", x=1300, y=320, text="−70%", at=C("A month later"), size=80, color="risk"),
              it("desk", x=2300, glow="red"), *crowd([2230], "worry", at=0.3, tie=True),
              it("coins", **{"from": [2300, 600], "to": [3300, 200]}, at=C("lost"), rate=7),
              it("piggy", x=2800, at=C("already bought back"), crackAt=C("lost"), text="HEDGE FUND", scale=0.85)],
    "callouts": [co("Wednesday close: {{price.close_display}}", 960, 150, C("closed at"), "white", screen=True, size=42, sub="converted at the Fed rate of 29 Oct", until=C("Within four days", -0.3)),
                 co("{{fall.display}} in four days · {{fall.month_display}} in a month", 960, 150, C("Within four days"), "risk", screen=True, size=42, until=C("But for many short sellers", -0.3)),
                 co("Too late: they had bought back at the top", 960, 150, C("But for many short sellers"), "white", screen=True, until=C("lost", -0.3)),
                 co("Short sellers' losses: {{fall.loss_display}}", 960, 150, C("lost"), "risk", screen=True, size=44, sub="an estimate (International Banker)")]},
    sources=["risk_options", "ib_squeeze", "fed_h10"], sfx=[{"kind": "hit", "cue": "closed at", "gain": 0.3}])
kinetic("s27_t4", "m4_transition", [("Porsche seemed to be winning", 60, "Porsche seemed", None, True), ("The real ending was very different", 64, "The real ending", "accent", False)])

# ====================================================================== PART 5: the hunter and the hunted
card("s28_c5", "m5_card", "The Hunter and the Hunted", "Who really won?")
stage("s29_q5", "m5_question", {
    "zones": [Z("district")], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("building", x=520, style="office", color="#FFE082", text="PORSCHE", scale=0.6), VW(1350, scale=1.1, h=560),
              it("letters", x=940, y=300, text="?", at=C("who really won"), size=150, color="gold")],
    "callouts": [co("Who really won?", 960, 150, C("who really won"), "gold", screen=True, size=48)]})
stage("s30_gain", "m5_gain", {
    "zones": [Z("district")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 540, "zoom": 1.05}, {"at": C("A large part"), "x": 1200, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("building", x=640, style="office", color="#FFE082", text="PORSCHE", scale=0.7),
              it("stack", x=1250, at=C("a gain of"), h=[[{"cue": "a gain of"}, 40], [{"cue": "a gain of", "offset": 3}, 250]], text="OPTION GAINS", sub="business year 2007/08"),
              it("stack", x=1650, at=C("most of its profit"), h=[[{"cue": "most of its profit"}, 40], [{"cue": "most of its profit", "offset": 3}, 320]], text="ALL PROFIT"),
              it("device", type="car", x=2050, y=F, at=C("sports car maker"), scale=0.8),
              it("letters", x=1650, y=200, text="!", at=C("financial contracts"), size=110, color="gold")],
    "callouts": [co("Gain on VW options: {{options_gain.display}}", 960, 150, C("a gain of"), "gold", screen=True, size=44, sub="converted at the 2008 average rate", until=C("most of its profit", -0.3)),
                 co("Total profit: {{options_gain.profit_display}}", 960, 150, C("most of its profit"), "white", screen=True, size=44, until=C("A large part", -0.3)),
                 co("A large part from financial contracts", 960, 150, C("A large part"), "gold", screen=True)]},
    sources=["risk_options", "fed_h10"])
stage("s31_merger", "m5_merger", {
    "zones": [Z("carplant", -1600, 1100, idle=99), Z("district", 1100, 6000)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("the roles were reversed"), "x": 1400, "y": 500, "zoom": 0.95, "dur": 2.4},
            {"at": C("The hunter had become"), "x": 1500, "y": 540, "zoom": 1.08, "dur": 2.4}], "drift": 0,
    "items": [it("storm", x=[[0, 400], [14, 1400]], y=140, at=C("the crisis made that")),
              it("building", x=[[0, 700], [{"cue": "a brand inside"}, 700], [{"cue": "a brand inside", "offset": 3}, 1600]], style="office", color="#FFE082", text="PORSCHE", scale=0.6),
              VW(2000, scale=1.2, h=640),
              it("calendar", x=330, y=300, at=C("In August"), pages=[[0, "AUG", "2009"]], scale=0.75),
              it("docs", x=1150, y=F, at=C("agreed to merge"), text="MERGER PLAN", stampAt=C("first buy"), stamp="AGREED", color="green"),
              it("coins", **{"from": [2000, 400], "to": [700, 560]}, at=C("first buy", 0.4), rate=4, until=C("a brand inside")),
              it("sign", x=1600, y=360, text="10TH BRAND", sub="inside the Volkswagen group", at=C("a brand inside", 2.6), color="#BBDEFB", size=40),
              *crowd([2500], "point", at=C("The hunter had become"), tie=True)],
    "callouts": [co("Aug 2009: the two agree to merge", 960, 150, C("agreed to merge"), "white", screen=True, until=C("first buy", -0.3)),
                 co("VW buys {{merger.stake_display}} of Porsche for {{merger.display}}", 960, 150, C("first buy"), "gold", screen=True, size=40, sub="AFP's dollar figure", until=C("AFP called", -0.3)),
                 co("“The failure of a gamble”", 960, 150, C("AFP called"), "risk", screen=True, size=44, sub="AFP, 2009", until=C("The hunter had become", -0.3)),
                 co("The hunter became the hunted", 960, 960, C("The hunter had become"), "gold", screen=True, size=48)]},
    sources=["afp_merger"], sfx=[{"kind": "hit", "cue": "first buy", "gain": 0.3}])
stage("s32_court", "m5_court", {
    "zones": [Z("court", cx=960)], "worldW": 1920,
    "cam": [{"at": 0, "x": 960, "y": 480, "zoom": 1.15}, {"at": C("acquitted"), "x": 960, "y": 540, "zoom": 1.0, "dur": 2.4}], "drift": 0,
    "items": [it("gavel", x=960, y=F - 414, hits=[C("acquitted", 0.2), C("became final", 0.3)], scale=1.0),
              it("calendar", x=330, y=330, at=C("acquitted", -1.0), pages=[[0, "18 MAR", "2016"]], scale=0.8, color="navy"),
              it("sign", x=1330, y=330, text="CHARGE", sub="market manipulation (alleged)", at=C("charged"), color="#FFF59D", size=34, until=C("acquitted")),
              it("sign", x=1330, y=330, text="ACQUITTED", sub="on all charges", at=C("acquitted"), color="#C8E6C9", size=44),
              it("sign", x=960, y=200, text="VERDICT FINAL", sub="appeal withdrawn (July 2016)", at=C("became final"), color="#C8E6C9", size=36)],
    "callouts": [co("Prosecutors: alleged market manipulation", 960, 960, C("charged"), "white", screen=True, sub="former CEO Wendelin Wiedeking, former CFO Holger Härter", until=C("acquitted", -0.3)),
                 co("{{acquittal.display}}: acquitted on all charges", 960, 960, C("acquitted"), "gold", screen=True, size=42, until=C("neither false", -0.3)),
                 co("Statements: “neither false nor misleading”", 960, 960, C("neither false"), "white", screen=True, sub="Stuttgart Regional Court, as reported by Porsche SE")]},
    sources=["porsche_2016"], sfx=[{"kind": "hit", "cue": "acquitted", "gain": 0.3}])
# ---- PRESENTER D: the lesson
add("p33_lesson", "m5_draw", "engine_draw", {
    "title": "Three lessons of a squeeze", "board": BOARD, "draw_start": C("A short seller can lose"), "speed": 1500, "push": 0.003,
    "enter": {"from": 2200, "to": 1640, "at": C("Let me draw", -0.3), "dur": 1.3},
    "strokes": [
        {"d": rect(540, 340, 740, 110), "color": "risk", "width": 5, "start": C("A short seller can lose"), "label": lbl("1 · LOSSES HAVE NO CEILING", 910, 405, 28, "risk")},
        {"d": rect(540, 490, 740, 110), "color": "accent", "width": 5, "start": C("When too many people"), "label": lbl("2 · A CROWDED EXIT", 910, 555, 28, "accent")},
        {"d": rect(540, 640, 740, 110), "color": "accent2", "width": 5, "start": C("And when someone holds"), "label": lbl("3 · HIDDEN SCARCITY", 910, 705, 28, "accent2")},
        {"d": "M 1340 820 L 1340 780 L 1380 780 L 1380 820 M 1400 820 L 1400 690 L 1440 690 L 1440 820", "color": "risk", "width": 4, "fill": "risk", "fillOpacity": 0.3, "kind": "bar",
         "start": C("much smaller than everyone"), "label": lbl("for sale vs. owed", 1390, 870, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("crowded", 0.3), "dur": 1.3, "target": [910, 545]}, {"kind": "react", "at": C("much smaller than everyone", 0.4)}],
    "scale": 0.86, "floor": 1040}, sources=["risk_options", "ib_squeeze"])
# ====================================================================== PAYOFF
stage("s34_payoff", "payoff", {
    "zones": [Z("exchange")], "worldW": 2200,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("the scarcest thing"), "x": 1100, "y": 500, "zoom": 1.08, "dur": 2.4}], "drift": 0,
    "items": [it("device", type="car", x=500, y=F, at=C("Not by selling more cars"), scale=0.9),
              it("letters", x=500, y=380, text="✗", at=C("Not by inventing"), size=110, color="risk"),
              grid(1150, 400, at=C("its shares"), porsche=C("its shares", 0.2), lsax=C("its shares", 1.2), free=C("its shares", 1.8), owed={"n": 12, "at": C("scarcest thing", 0.5), "label": "OWED ≈ 12", "shakeAt": C("desperate buyer")}, scale=0.62),
              *crowd([1700, 1820, 1940], "run", at=C("the last desperate buyer"), tie=True),
              it("counter", x=1700, y=300, at=C("A price is not only"), prefix="$", steps=[[{"cue": "A price is not only"}, 266], [{"cue": "the last desperate buyer", "offset": 1}, 1250]], text="WHAT THE LAST BUYER PAYS")],
    "callouts": [co("Not more cars. Not a new invention.", 960, 150, C("Not by selling more cars"), "white", screen=True, until=C("the scarcest thing", -0.3)),
                 co("For a day, its shares were the scarcest thing in the market", 960, 150, C("the scarcest thing"), "gold", screen=True, size=40, until=C("A price is not only", -0.3)),
                 co("Sometimes a price is what the last desperate buyer has to pay", 960, 150, C("A price is not only"), "gold", screen=True, size=38)]},
    sources=["ib_squeeze"])
add("s35_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_volkswagen_storyboard.py; edit the generator, not this file.\n"
           "# Episode 13 storyboard: bespoke CartoonStage worlds. The channel intro is inserted automatically after the hook.\n")
