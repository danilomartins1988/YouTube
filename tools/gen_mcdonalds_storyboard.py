"""Generates projects/the-hamburger-that-became-a-symbol-of-the-cold-wars-end/deliverables/documentary/storyboard.yaml
(Episode 26, McDonald's in Moscow 1990-2022).

Bespoke worlds (tones from visual_direction.yaml: bright -> strategy -> crisis -> reflective): a snowy winter square
(new `wintersquare` set) with a generic burger restaurant front (new `restaurant` item: its sign swaps to the new name in
2022), a pre-dawn queue in fur hats (new `queue` item), a negotiation office, potato fields (new `farm` set) and a food
plant with buns, patties and fries on the belts (new conveyor goods). A giant cartoon burger (new `burger` item) is the
through-line. Presenter: the joint venture (boxes + arrows), the supply chain (boxes + arrows), opening day (bars),
1990 vs 2022 (bars), the cost of leaving (boxes + arrows).
No McDonald's logo, arches, mascot, colours or trade dress; no likeness of real people (names in text only).
Run: python tools/gen_mcdonalds_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-hamburger-that-became-a-symbol-of-the-cold-wars-end/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
SQ = "PUSHKIN SQ."


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 2, "skin": (k % 4), **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def shop(x=1500, **kw):
    kw.setdefault("text", "HAMBURGERS")
    kw.setdefault("color", "#C62828")
    return it("restaurant", x=x, **kw)


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("wintersquare", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 700, "y": 560, "zoom": 1.2}, {"at": 2.5, "x": 1200, "y": 520, "zoom": 0.95, "dur": 3.5}], "drift": 4,
    "items": [shop(1700, at=0.1, scale=0.75, openAt=99), it("queue", x=200, at=0.3, n=26, gap=62, rows=2, move=6, scale=0.5),
              it("burger", x=1700, y=[[0, 160], [6, 140]], at=C("just to buy", 0.2), scale=0.45)],
    "callouts": [co("Thousands, in the snow, before dawn…", 960, 960, C("Why would"), "white", screen=True, size=40, until=C("just to buy", -0.3)),
                 co("…for a hamburger?", 960, 960, C("just to buy"), "gold", screen=True, size=46)]},
    sources=["cbc", "ap1990"])
stage("s02_stakes", "h_stakes", {
    "zones": [Z("wintersquare", night=True)], "worldW": 3600, "night": True,
    "cam": [{"at": 0, "x": 800, "y": 540, "zoom": 1.0}, {"at": C("By the end of the day"), "x": 1700, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("Thirty-two years later"), "x": 2500, "y": 520, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "JAN 31", "1990"], [{"cue": "Thirty-two years later"}, "2022", "32 YEARS ON"]], scale=0.8),
              it("queue", x=-300, at=0.3, n=18, gap=64, move=6, scale=0.5),
              shop(1700, at=0.2, scale=0.75, openAt=C("By the end of the day")),
              it("counter", x=1700, y=150, at=C("By the end of the day"), steps=[[0, 0], [{"cue": "customers had walked", "offset": 0.5}, 30000]], text="CUSTOMERS ON DAY ONE"),
              it("burger", x=2550, y=420, at=C("For a few years"), scale=0.7),
              it("letters", x=2550, y=150, text="END OF THE COLD WAR", at=C("a symbol of the Cold War"), size=54, color="gold")],
    "callouts": [co("31 Jan 1990: lining up from 4 a.m.", 960, 960, C("On January"), "white", screen=True, size=40, sub="CBC Archives", until=C("By the end of the day", -0.3)),
                 co("30,000 customers: an opening-day record", 960, 960, C("By the end of the day"), "gold", screen=True, size=38, sub="CBC · AP (1990)", until=C("For a few years", -0.3)),
                 co("…then a symbol of something else", 960, 960, C("Thirty-two years later"), "risk", screen=True, size=40)]},
    sources=["cbc", "ap1990"])

# ====================================================================== PART 1: fourteen years
card("s03_c1", "m1_card", "Fourteen Years", "1976-1990")
stage("s04_q1", "m1_question", {
    "zones": [Z("wintersquare")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("sign", x=960, y=380, at=0.3, text="STATE STORE", sub="private business not allowed", color="#FFE082", size=40),
              it("burger", x=1450, y=480, at=1.5, scale=0.4)],
    "callouts": [co("A burger chain… in the USSR?", 960, 150, C("How do you"), "gold", screen=True, size=44)]})
stage("s05_start", "m1_start", {
    "zones": [Z("office", -1600, 1500), Z("wintersquare", 1500, 5200)], "worldW": 3200,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("Beginning in"), "x": 1500, "y": 520, "zoom": 0.95, "dur": 2.6},
            {"at": C("In the Soviet Union, the state"), "x": 2400, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("person", x=700, pose="phone", at=0.3, scale=0.8, hair=1, skin=0, suit=False, tie=True),
              it("letters", x=1300, y=220, text="1976 → DOZENS OF TRIPS", at=C("Beginning in"), size=48, color="gold"),
              it("calendar", x=1300, y=420, at=C("Beginning in"), pages=[[0, "1976", "FIRST TRIP"], [{"cue": "to lobby the officials"}, "...", "STILL TRYING"]], scale=0.75),
              it("board", x=2400, y=380, at=C("In the Soviet Union, the state"), text="OWNED BY THE STATE", rows=[{"name": "SHOPS"}, {"name": "FARMS"}, {"name": "FACTORIES", "color": "gold"}])],
    "callouts": [co("From 1976: dozens of trips to Moscow", 960, 960, C("Beginning in"), "white", screen=True, size=38, sub="Ironside (UChicago BFI)", until=C("In the Soviet Union, the state", -0.3)),
                 co("No renting, no private selling", 960, 960, C("A foreign company"), "risk", screen=True, size=40)]},
    sources=["ironside"])
stage("s06_jv", "m1_jv", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("But there was a catch"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "1987", "PERESTROIKA"], [{"cue": "On April"}, "APR 29", "1987"]], scale=0.8),
              it("contract", x=1000, y=460, at=C("On April"), text="JOINT VENTURE", sub="McDonald's Canada + Moscow city", signAt=C("signed one", 0.5), scale=0.7),
              it("stack", x=1500, h=[[0, 40], [{"cue": "fifty-one percent", "offset": 0.5}, 330]], at=C("The city kept"), text="CITY 51%", color="#1565C0"),
              it("stack", x=1800, h=[[0, 40], [{"cue": "limited to forty-nine", "offset": 0.5}, 310]], at=C("The foreign partner"), text="McD 49%", color="#E89A00")],
    "callouts": [co("29 Apr 1987: a joint venture with Moscow", 960, 960, C("On April"), "white", screen=True, size=38, sub="Ironside (UChicago BFI)", until=C("But there was a catch", -0.3)),
                 co("City 51% · McDonald's 49%", 960, 960, C("But there was a catch"), "gold", screen=True, size=42)]},
    sources=["ironside"])
add("p07_jv", "m1_draw", "engine_draw", {
    "title": "The joint venture", "board": BOARD, "draw_start": C("On one side"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 360, 280, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("On one side"), "label": lbl("MOSCOW CITY 51%", 680, 428, 22, "accent2")},
        {"d": rect(1200, 360, 280, 120), "color": "accent", "width": 6, "kind": "box", "start": C("On the other"), "label": lbl("McD CANADA 49%", 1340, 428, 22, "accent")},
        {"d": rect(870, 640, 280, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Between them"), "label": lbl("1 RESTAURANT JV", 1010, 708, 22, "accent3")},
        {"d": arrow((700, 490), (900, 630), 0.1), "color": "ink", "width": 5, "start": C("The city brought"), "label": lbl("land · permits", 700, 590, 20, "ink")},
        {"d": arrow((1320, 490), (1120, 630), -0.1), "color": "ink", "width": 5, "start": C("McDonald's brought"), "label": lbl("money · recipes", 1330, 590, 20, "ink")},
    ],
    "actions": [{"kind": "point", "at": C("neither could do it alone", 0.2), "dur": 1.4, "target": [1010, 700]}],
    "scale": 0.86, "floor": 1040}, sources=["ironside"])
stage("s08_cost", "m1_cost", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("And a big part"), "x": 1400, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=220, at=0.3, prefix="$", suffix="M", steps=[[0, 0], [{"cue": "an investment of", "offset": 1}, 50]], text="INVESTED"),
              it("calendar", x=500, y=320, at=0.3, pages=[[0, "14", "YEARS"]], scale=0.8),
              it("coins", **{"from": [900, 400], "to": [1700, 500]}, at=C("And a big part"), rate=5)],
    "callouts": [co("14 years · $50 million", 960, 960, C("In the end"), "gold", screen=True, size=44, sub="CBC Archives")]},
    sources=["cbc"])
kinetic("s09_t1", "m1_transition", [("A problem nobody could negotiate away", 54, "a problem nobody", None, True), ("No reliable food supply", 60, "no reliable supply", "risk", False)])

# ====================================================================== PART 2: building a food chain
card("s10_c2", "m2_card", "Building a Food Chain", "1989-1990")
stage("s11_q2", "m2_question", {
    "zones": [Z("farm")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("burger", x=960, y=430, at=0.3, scale=0.6, bites=[[0, 0], [3, 1], [5, 2]])],
    "callouts": [co("No suppliers? Build your own", 960, 150, C("What do you do"), "gold", screen=True, size=44)]})
stage("s12_shortage", "m2_shortage", {
    "zones": [Z("carplant")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("So McDonald's decided"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("conveyor", x0=300, x1=1500, at=0.2, goods="bun", n=6, speed=110, stopAt=C("nobody could guarantee", 0.5), gapAt=C("nobody could guarantee"), gapText="NO SUPPLY"),
              it("letters", x=1000, y=200, text="SAME BUN · SAME BEEF · SAME POTATO", at=C("depends on the same bun"), size=40, color="gold"),
              it("sign", x=1900, y=400, at=C("So McDonald's decided"), text="BUILD IT OURSELVES", color="#C8E6C9", size=40)],
    "callouts": [co("Planned economy: no guaranteed supply", 960, 960, C("In the Soviet planned economy"), "risk", screen=True, size=38, until=C("So McDonald's decided", -0.3)),
                 co("So: build the whole supply chain", 960, 960, C("So McDonald's decided"), "white", screen=True, size=40)]},
    sources=["ironside"])
stage("s13_plant", "m2_plant", {
    "zones": [Z("carplant")], "worldW": 2800,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("According to CBC"), "x": 1400, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("The building opened"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=700, y=300, at=0.2, pages=[[0, "1989", "WORK BEGINS"], [{"cue": "The building opened"}, "1990", "OPEN"]], scale=0.75),
              it("letters", x=1000, y=200, text="≈ 100,000 SQ FT", at=C("It covered"), size=56, color="gold"),
              it("conveyor", x0=600, x1=2000, y=F - 260, at=C("it was built to turn out"), goods="bun", n=8, speed=160),
              it("conveyor", x0=600, x1=2000, at=C("ten thousand patties"), goods="patty", n=8, speed=140),
              it("counter", x=1750, y=200, at=C("it was built to turn out"), steps=[[0, 0], [{"cue": "it was built to turn out", "offset": 2}, 14000]], text="BUNS / HOUR")],
    "callouts": [co("A plant on Moscow's edge (1989-90)", 960, 960, C("In nineteen eighty-nine"), "white", screen=True, size=38, sub="Ironside (UChicago BFI)", until=C("According to CBC", -0.3)),
                 co("14,000 buns & 10,000 patties an hour", 960, 960, C("According to CBC"), "gold", screen=True, size=38, sub="CBC Archives")]},
    sources=["ironside", "cbc"])
stage("s14_potatoes", "m2_potatoes", {
    "zones": [Z("farm")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("and trained Soviet"), "x": 1600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("plane", x=[[0.3, -300], [4.0, 1100]], y=[[0.3, 250], [4.0, 300]], at=0.3, text="SEED POTATOES"),
              it("conveyor", x0=500, x1=1200, at=C("Russet Burbank"), goods="potato", n=5, speed=80),
              *crowd([1500, 1640, 1780], "cheer", at=C("and trained Soviet"), scale=0.7),
              it("sign", x=1650, y=300, at=C("collective farmers"), text="COLLECTIVE FARM", sub="bigger harvests", color="#FFE082", size=34)],
    "callouts": [co("Imported seed potatoes: Russet Burbank", 960, 960, C("Even the potatoes"), "white", screen=True, size=38, sub="Ironside (UChicago BFI)", until=C("and trained Soviet", -0.3)),
                 co("A burger chain teaching farming", 960, 960, C("A burger restaurant was teaching"), "gold", screen=True, size=40)]},
    sources=["ironside"])
add("p15_chain", "m2_draw", "engine_draw", {
    "title": "The supply chain", "board": BOARD, "draw_start": C("Here are the farms"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 480, 240, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("Here are the farms"), "label": lbl("FARMS + SEEDS", 660, 548, 22, "accent3")},
        {"d": rect(890, 480, 240, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("The crop goes into the plant"), "label": lbl("FOOD PLANT", 1010, 548, 24, "accent2")},
        {"d": rect(1240, 480, 240, 120), "color": "accent", "width": 6, "kind": "box", "start": C("the food goes to the restaurant"), "label": lbl("RESTAURANT", 1360, 548, 24, "accent")},
        {"d": arrow((785, 540), (885, 540), 0.0), "color": "ink", "width": 5, "start": C("The crop goes")},
        {"d": arrow((1135, 540), (1235, 540), 0.0), "color": "ink", "width": 5, "start": C("And from the plant")},
        {"d": "M 900 660 L 1120 660", "color": "risk", "width": 5, "start": C("which makes the buns"), "label": lbl("buns · patties · fries", 1010, 700, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("built from scratch", 0.2), "dur": 1.4, "target": [1010, 540]}],
    "scale": 0.86, "floor": 1040}, sources=["ironside", "cbc"])
kinetic("s16_t2", "m2_transition", [("The chain was ready", 60, "the chain was ready", None, False), ("Would anyone come?", 66, "whether anyone would come", "gold", False)])

# ====================================================================== PART 3: opening day
card("s17_c3", "m3_card", "Opening Day", "31 January 1990")
stage("s18_q3", "m3_question", {
    "zones": [Z("wintersquare", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("queue", x=200, at=0.3, n=20, gap=70, move=5, scale=0.55)],
    "callouts": [co("A taste of the West: how many will come?", 960, 150, C("How many people"), "gold", screen=True, size=40)]})
stage("s19_queue", "m3_queue", {
    "zones": [Z("wintersquare", night=True)], "worldW": 3200, "night": True,
    "cam": [{"at": 0, "x": 600, "y": 540, "zoom": 1.1}, {"at": C("By the time the doors opened"), "x": 1400, "y": 520, "zoom": 0.9, "dur": 3.0},
            {"at": C("Inside, the restaurant"), "x": 2300, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 4,
    "items": [it("clock", x=750, y=260, at=0.3, period=3.0, text="4 A.M."),
              it("queue", x=-200, at=0.4, n=40, gap=58, rows=2, move=7, scale=0.5),
              shop(2350, at=0.2, scale=0.8, openAt=C("By the time the doors opened", 1.0)),
              it("counter", x=2350, y=120, at=C("Inside, the restaurant"), steps=[[0, 0], [{"cue": "cash registers", "offset": 0}, 27]], text="CASH REGISTERS")],
    "callouts": [co("4 a.m., in the dark and the cold", 960, 960, C("On January"), "white", screen=True, size=40, sub="CBC Archives", until=C("By the time the doors opened", -0.3)),
                 co("Thousands in line", 960, 960, C("By the time the doors opened"), "gold", screen=True, size=42, sub="AP (1990)", until=C("Inside, the restaurant", -0.3)),
                 co("27 cash registers", 960, 960, C("Inside, the restaurant"), "white", screen=True, size=42, sub="AP (1990)")]},
    sources=["cbc", "ap1990"])
stage("s20_record", "m3_record", {
    "zones": [Z("wintersquare")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("They served"), "x": 1300, "y": 500, "zoom": 1.0, "dur": 2.2}], "drift": 3,
    "items": [shop(1300, at=0.2, scale=0.75),
              it("counter", x=1300, y=150, at=0.3, steps=[[0, 0], [{"cue": "meals that day", "offset": 0}, 10000], [{"cue": "They served", "offset": 2}, 30000]], text="MEALS SERVED"),
              it("burst", x=1300, y=150, at=C("No McDonald's anywhere")),
              *crowd([500, 620, 2000, 2120], "cheer", at=C("They served"), scale=0.65)],
    "callouts": [co("Expected: ~10,000 meals", 960, 960, C("The staff had expected"), "white", screen=True, size=40, sub="Ironside (UChicago BFI)", until=C("They served", -0.3)),
                 co("Served: 30,000. A world record", 960, 960, C("They served"), "gold", screen=True, size=42, sub="CBC Archives")]},
    sources=["ironside", "cbc"])
add("p21_day", "m3_draw", "engine_draw", {
    "title": "Opening day: plan vs reality", "board": BOARD, "draw_start": C("Here is the plan"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 860 L 1460 860", "color": "ink", "width": 4, "start": C("Here is the plan")},
        {"d": "M 760 860 L 760 760 L 940 760 L 940 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("ten thousand meals"), "label": lbl("PLAN 10,000", 850, 740, 24, "accent2")},
        {"d": "M 1120 860 L 1120 560 L 1300 560 L 1300 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("Thirty thousand."), "label": lbl("SERVED 30,000", 1210, 540, 26, "accent")},
        {"d": "M 960 640 Q 1030 560 1100 600", "color": "risk", "width": 5, "start": C("Three times the plan"), "label": lbl("× 3", 1000, 600, 34, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("Three times the plan", 0.2), "dur": 1.4, "target": [1210, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["ironside", "cbc"])
stage("s22_price", "m3_price", {
    "zones": [Z("wintersquare")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Still, the crowds"), "x": 1600, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("burger", x=700, y=430, at=0.2, scale=0.55, bites=[[0, 0], [4, 1]]),
              it("pricetag", x=1050, y=320, at=C("a meal cost about"), text="½ DAY'S PAY", scale=0.9),
              it("person", x=1300, pose="shrug", at=C("One man outside"), scale=0.75, hair=2, skin=3, hat="#795548"),
              it("queue", x=1500, at=C("Still, the crowds"), n=14, gap=64, move=6, scale=0.5)],
    "callouts": [co("A meal ≈ half a day's average wages", 960, 960, C("According to CBC"), "white", screen=True, size=38, sub="CBC Archives", until=C("Still, the crowds", -0.3)),
                 co("Not really about the food", 960, 960, C("For many people"), "gold", screen=True, size=42)]},
    sources=["cbc"])
stage("s23_quote", "m3_quote", {
    "zones": [Z("wintersquare", night=True)], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("I can touch"), "x": 1100, "y": 480, "zoom": 1.15, "dur": 2.6}], "drift": 1,
    "items": [shop(1500, at=0.2, scale=0.7),
              it("burger", x=900, y=420, at=C("I can touch"), scale=0.75),
              it("letters", x=1000, y=150, text="'BIG MAC IS PERESTROIKA'", at=C("I can taste it", 0.8), size=60, color="gold")],
    "callouts": [co("The first manager (as quoted by Ironside)", 960, 960, C("The restaurant's first manager"), "white", screen=True, size=36, until=C("I can touch", -0.3))]},
    sources=["ironside"])
stage("s24_leader", "m3_leader", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("A hamburger had become"), "x": 1400, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("paper", x=900, y=420, at=C("Mikhail Gorbachev"), text="'a breakthrough… new economic relations'", name="IRONSIDE", scale=0.65),
              it("burger", x=1600, y=440, at=C("A hamburger had become"), scale=0.55),
              it("letters", x=1600, y=170, text="FOREIGN POLICY", at=C("A hamburger had become", 0.5), size=60, color="gold")],
    "callouts": [co("Gorbachev: 'a breakthrough'", 960, 960, C("Mikhail Gorbachev"), "white", screen=True, size=40, sub="quoted by Ironside (UChicago BFI)", until=C("A hamburger had become", -0.3)),
                 co("A burger as foreign policy", 960, 960, C("A hamburger had become"), "gold", screen=True, size=42)]},
    sources=["ironside"])
kinetic("s25_t3", "m3_transition", [("Less than two years later…", 58, "Less than two years", None, True), ("the USSR was gone. The restaurant stayed.", 54, "the Soviet Union itself", "gold", False)])

# ====================================================================== PART 4: thirty years
card("s26_c4", "m4_card", "Thirty Years", "1990-2022")
stage("s27_q4", "m4_question", {
    "zones": [Z("wintersquare")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [shop(960, at=0.2, scale=0.7)],
    "callouts": [co("A symbol in a changing country", 960, 150, C("What happens"), "gold", screen=True, size=42)]})
stage("s28_control", "m4_control", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The company that had once"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "FEB", "1996"]], scale=0.8),
              it("stack", x=1000, h=[[0, 300], [{"cue": "raising its own stake", "offset": 1}, 120]], at=0.3, text="CITY", color="#1565C0"),
              it("stack", x=1300, h=[[0, 300], [{"cue": "raising its own stake", "offset": 1.5}, 480]], at=0.3, text="McD 49% → 80%", color="#E89A00"),
              it("sign", x=1900, y=380, at=C("The company that had once"), text="NOW RUNS THE BUSINESS", color="#FFE082", size=36)],
    "callouts": [co("1996: stake from 49% to 80%", 960, 960, C("In February"), "gold", screen=True, size=42, sub="Ironside (UChicago BFI)")]},
    sources=["ironside"])
stage("s29_growth", "m4_growth", {
    "zones": [Z("wintersquare")], "worldW": 3600,
    "cam": [{"at": 0, "x": 800, "y": 520, "zoom": 1.0}, {"at": C("They employed"), "x": 1700, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("Together with its restaurants"), "x": 2600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=800, y=150, at=0.3, steps=[[0, 1], [{"cue": "restaurants in Russia", "offset": 0.5}, 850]], suffix="+", text="RESTAURANTS IN RUSSIA"),
              *[shop(300 + k * 330, at=0.3 + 0.25 * k, scale=0.3) for k in range(5)],
              it("letters", x=900, y=330, text="≈ 84% COMPANY-OWNED", at=C("It owned about"), size=44, color="gold"),
              *crowd([1500 + 110 * k for k in range(6)], "walk", at=C("They employed"), scale=0.6),
              it("counter", x=1750, y=200, at=C("They employed"), steps=[[0, 0], [{"cue": "They employed", "offset": 1.5}, 62000]], text="EMPLOYEES"),
              it("counter", x=2600, y=200, at=C("Together with its restaurants"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "annual revenue", "offset": 0.5}, 2]], text="RUSSIA + UKRAINE REVENUE")],
    "callouts": [co("850+ restaurants · 62,000 staff", 960, 960, C("And it grew"), "white", screen=True, size=40, sub="McDonald's 10-Q · release", until=C("Together with its restaurants", -0.3)),
                 co("Russia + Ukraine: ~9% of revenue, ~$2bn", 960, 960, C("Together with its restaurants"), "gold", screen=True, size=36, sub="AP (Mar 2022)")]},
    sources=["q2_10q", "mcd_exit", "ap_mar22"])
add("p30_compare", "m4_draw", "engine_draw", {
    "title": "1990 vs 2022", "board": BOARD, "draw_start": C("In nineteen ninety, one restaurant"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 600 860 L 1460 860", "color": "ink", "width": 4, "start": C("In nineteen ninety, one restaurant")},
        {"d": "M 760 860 L 760 850 L 940 850 L 940 860", "color": "accent2", "width": 6, "fill": "accent2", "fillOpacity": 0.3, "kind": "bar", "start": C("one restaurant, forty-nine"), "label": lbl("1990: 1 · 49%", 850, 820, 24, "accent2")},
        {"d": "M 1120 860 L 1120 520 L 1300 520 L 1300 860", "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.4, "kind": "bar", "start": C("By twenty twenty-two"), "label": lbl("2022: 850+ · ~84%", 1210, 500, 24, "accent")},
        {"d": "M 1340 620 L 1440 620", "color": "risk", "width": 5, "start": C("so expensive"), "label": lbl("more to lose", 1390, 660, 22, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("so expensive", 0.2), "dur": 1.4, "target": [1210, 640]}],
    "scale": 0.86, "floor": 1040}, sources=["ironside", "q2_10q", "ap_mar22"])
kinetic("s31_t4", "m4_transition", [("February 2022", 60, "Then, in February", None, True), ("Russia invades Ukraine", 66, "Russia invaded Ukraine", "risk", False)])

# ====================================================================== PART 5: leaving
card("s32_c5", "m5_card", "Leaving", "2022")
stage("s33_q5", "m5_question", {
    "zones": [Z("wintersquare", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [shop(960, at=0.2, scale=0.7, openAt=99)],
    "callouts": [co("The price of walking away", 960, 150, C("What does it cost"), "gold", screen=True, size=42)]})
stage("s34_close", "m5_close", {
    "zones": [Z("wintersquare", night=True)], "worldW": 2800, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("Two months later"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Its chief executive"), "x": 1900, "y": 500, "zoom": 1.05, "dur": 2.4}], "drift": 2,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "MAR 8", "CLOSED"], [{"cue": "Two months later"}, "MAY 16", "EXIT"]], scale=0.8),
              shop(1400, at=0.2, scale=0.75, openAt=99, sub="TEMPORARILY CLOSED"),
              it("letters", x=1400, y=110, text="EXPECTED CHARGE $1.2-1.4BN", at=C("it expected to book"), size=46, color="risk"),
              it("paper", x=2100, y=420, at=C("Its chief executive"), text="'can no longer keep the Arches shining there'", name="CEO, 16 MAY 2022", scale=0.65)],
    "callouts": [co("8 Mar: closed · 16 May: leaving for good", 960, 960, C("On March"), "white", screen=True, size=38, sub="McDonald's", until=C("Its chief executive", -0.3)),
                 co("After 30+ years in Russia", 960, 960, C("Its chief executive"), "gold", screen=True, size=42)]},
    sources=["mcd_exit"])
stage("s35_sale", "m5_sale", {
    "zones": [Z("office")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("The deal kept"), "x": 1500, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("contract", x=900, y=460, at=0.3, text="SALE AGREEMENT", sub="whole Russian business", signAt=C("agreed to sell", 1.0), scale=0.7),
              it("sign", x=900, y=200, text="BUYER: A LICENSEE", sub="25 restaurants in Siberia", at=C("a local businessman"), color="#FFE082", size=34),
              *crowd([1400, 1520, 1640], "stand", at=C("The deal kept"), scale=0.65),
              it("pricetag", x=2100, y=320, at=C("The price was never"), text="$ ???", scale=0.9)],
    "callouts": [co("19 May: sold to licensee Alexander Govor", 960, 960, C("Three days later"), "white", screen=True, size=38, sub="McDonald's", until=C("The deal kept", -0.3)),
                 co("Staff kept 2+ years · price undisclosed", 960, 960, C("The deal kept"), "gold", screen=True, size=38)]},
    sources=["mcd_sale", "ap_jun22"])
add("p36_cost", "m5_draw", "engine_draw", {
    "title": "What leaving cost", "board": BOARD, "draw_start": C("Here is McDonald's"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 380, 260, 120), "color": "accent", "width": 6, "kind": "box", "start": C("Here is McDonald's"), "label": lbl("McDONALD'S", 670, 448, 24, "accent")},
        {"d": rect(1200, 380, 260, 120), "color": "accent2", "width": 6, "kind": "box", "start": C("here is the Russian business"), "label": lbl("850+ IN RUSSIA", 1330, 448, 22, "accent2")},
        {"d": rect(1200, 680, 260, 120), "color": "accent3", "width": 6, "kind": "box", "start": C("An arrow to the new owner"), "label": lbl("NEW OWNER", 1330, 748, 24, "accent3")},
        {"d": arrow((1330, 505), (1330, 670), 0.0), "color": "ink", "width": 5, "start": C("An arrow to the new owner"), "label": lbl("price: undisclosed", 1460, 600, 20, "ink")},
        {"d": arrow((1190, 440), (810, 440), 0.0), "color": "risk", "width": 6, "start": C("And an arrow back"), "label": lbl("−$1.3bn charge", 1000, 410, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("A charge of", 0.2), "dur": 1.4, "target": [1000, 440]}],
    "scale": 0.86, "floor": 1040}, sources=["q2_release", "mcd_sale"])
stage("s37_charge", "m5_charge", {
    "zones": [Z("office")], "worldW": 2400,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("over the first half"), "x": 1300, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=1000, y=220, at=0.3, prefix="−$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "in the second quarter", "offset": 0}, 1.2], [{"cue": "over the first half", "offset": 0.5}, 1.3]], text="PRE-TAX CHARGE"),
              it("docs", x=1500, y=560, at=C("In its results"), text="Q2 2022 RESULTS", scale=0.6, stamp="RUSSIA SALE", stampAt=C("related to the sale"))],
    "callouts": [co("Q2: $1.2bn · first half: $1.3bn (pre-tax)", 960, 960, C("In its results"), "risk", screen=True, size=38, sub="McDonald's Q2 2022 release · 10-Q")]},
    sources=["q2_release", "q2_10q"])
stage("s38_reopen", "m5_reopen", {
    "zones": [Z("wintersquare")], "worldW": 2600,
    "cam": [{"at": 0, "x": 1000, "y": 520, "zoom": 1.0}, {"at": C("Only the name had changed"), "x": 1300, "y": 480, "zoom": 1.1, "dur": 2.4}], "drift": 2,
    "items": [it("calendar", x=450, y=300, at=0.2, pages=[[0, "JUN 12", "2022"]], scale=0.75),
              shop(1300, at=0.2, scale=0.8, swapAt=C("Vkusno and tochka", -0.2), newText="VKUSNO & TOCHKA", newColor="#2E7D32", openAt=C("began to reopen")),
              *crowd([800, 920, 1800, 1920], "walk", at=C("Same address"), scale=0.6)],
    "callouts": [co("12 Jun 2022: same square, new owner", 960, 960, C("And then came"), "white", screen=True, size=38, sub="AP", until=C("Only the name had changed", -0.3)),
                 co("'Tasty, and that's it'", 960, 960, C("Vkusno and tochka"), "gold", screen=True, size=44)]},
    sources=["ap_jun22", "mcd_sale"])

# ====================================================================== PAYOFF
stage("s39_payoff", "payoff", {
    "zones": [Z("wintersquare", night=True)], "worldW": 2600, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("It took fourteen years"), "x": 1300, "y": 520, "zoom": 1.0, "dur": 2.6},
            {"at": C("What left was"), "x": 1500, "y": 500, "zoom": 1.1, "dur": 2.6}], "drift": 2,
    "items": [shop(1400, at=0.2, scale=0.75, text="HAMBURGERS", swapAt=C("one war to close it"), newText="VKUSNO & TOCHKA", newColor="#2E7D32"),
              it("burger", x=600, y=420, at=0.3, scale=0.5, until=C("What left was")),
              it("queue", x=-400, at=C("so are the customers"), n=12, gap=64, move=6, scale=0.5),
              it("letters", x=1400, y=110, text="14 YEARS TO OPEN · 1 WAR TO CLOSE", at=C("It took fourteen years"), size=44, color="gold")],
    "callouts": [co("A business is never only a business", 960, 960, C("That a business"), "white", screen=True, size=40, until=C("It took fourteen years", -0.3)),
                 co("Trade alone doesn't hold the world together", 960, 960, C("What left was"), "gold", screen=True, size=36)]},
    sources=["cbc", "mcd_exit", "ap_jun22"])
add("s40_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_mcdonalds_storyboard.py; edit the generator, not this file.\n"
           "# Episode 26 storyboard (McDonald's in Moscow 1990-2022): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
