"""Generates projects/the-three-companies-that-decide-memory-prices/deliverables/documentary/storyboard.yaml (Episode 14).

Bespoke worlds for the memory-price story (tones come from visual_direction.yaml: crisis -> strategy -> tech -> crisis ->
reflective): an electronics shop at night where one memory stick's price tag flips from $8.70 to $48 (the through-line),
the memory stick itself with its eight chips lifting off the board, a trading floor with the three makers' shares as a
100-certificate grid, an AI accelerator whose HBM stacks build layer by layer, a data centre that takes the coins the shop
used to get, a Shanghai listing board for CXMT with a tools barrier, a memory fab whose line stops in the 2023 bust, and
construction sites for the factories arriving in 2027. Presenter: oligopoly, wafer split, the memory cycle.
No logos (company names in text only), no smiling sun, no generic city.
Run: python tools/gen_memory_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/the-three-companies-that-decide-memory-prices/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
SAM, HYN, MIC, CXM, OTH = "#4FB3F6", "#FF8A65", "#B39DDB", "#FF4B3E", "#90A4AE"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 1, "skin": k, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


def makers(xs=(700, 1100, 1500), at=0.2, h=560, **kw):
    names = [("SAMSUNG", SAM), ("SK HYNIX", HYN), ("MICRON", MIC)]
    def later(a, d):
        return {**a, "offset": a.get("offset", 0) + d} if isinstance(a, dict) else a + d
    return [it("tower", x=x, text=n, color=c, h=h, at=later(at, k * 0.3), scale=0.95, **kw) for k, (x, (n, c)) in enumerate(zip(xs, names))]


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("shop", night=True, label="none")], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.35}, {"at": C("jumped"), "x": 960, "y": 520, "zoom": 1.05, "dur": 3.0}], "drift": 0,
    "items": [it("ramstick", x=960, y=520, at=0.3, scale=0.8, label="16 GB", hotAt=C("jumped")),
              it("pricetag", x=1500, y=300, at=0.6, pages=[[0, "$8.70"], [{"cue": "jumped"}, "$48", True]], sub="one memory chip"),
              it("letters", x=420, y=330, text="×5", at=C("five times"), size=130, color="risk")],
    "callouts": [co("One tiny part…", 960, 150, C("one tiny part"), "white", screen=True, size=42, until=C("jumped", -0.3)),
                 co("…more than 5× in one year", 960, 150, C("jumped"), "risk", screen=True, size=44)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("shop", -1600, 1500, night=True), Z("exchange", 1500, 6000)], "worldW": 3200, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 540, "zoom": 1.05}, {"at": C("three companies"), "x": 2300, "y": 520, "zoom": 0.95, "dur": 2.8}], "drift": 0,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "OCT", "2025"], [{"cue": "By September"}, "SEP", "2026"]], scale=0.8),
              it("counter", x=860, y=520, at=0.4, prefix="$", decimals=2, steps=[[0, 8.7], [{"cue": "By September"}, 8.7], [{"cue": "By September", "offset": 3}, 48]], text="ONE 16Gb DDR5 CHIP"),
              it("chart", x=860, y=780, w=520, h=220, at=C("By September", -0.2), dur=3, text="CONTRACT PRICE", pts=[0.05, 0.4, 0.52, 0.8, 0.88], color="risk"),
              *makers((1900, 2300, 2700), at=C("three companies", -0.4), h=520),
              it("letters", x=2300, y=180, text="?", at=C("one quiet choice"), size=130, color="gold")],
    "callouts": [co("Oct 2025: {{ddr5.display}} per chip", 960, 960, C("In October"), "white", screen=True, size=40, sub="contract price, TrendForce (via TeamGroup)", until=C("By September", -0.3)),
                 co("Sep 2026: {{ddr5.now_display}} ({{ddr5.pct_display}})", 960, 960, C("By September"), "risk", screen=True, size=44, until=C("three companies", -0.3)),
                 co("Three companies, one quiet choice", 960, 960, C("three companies"), "gold", screen=True, size=42)]},
    sources=["teamgroup_prices", "tf_2q26"], sfx=[{"kind": "hit", "cue": "By September", "gain": 0.3}])

# ====================================================================== PART 1: the shelf
card("s03_c1", "m1_card", "The Shelf", "What got so expensive")
stage("s04_q1", "m1_question", {
    "zones": [Z("shop", night=True, label="none")], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("ramstick", x=960, y=560, at=0.2, scale=0.75, label="16 GB"),
              it("magnifier", x=[[0, 500], [6, 1300]], y=[[0, 420], [6, 560]], at=0.4, scale=0.9),
              *crowd([300], "read", at=0.3, glasses=True)],
    "callouts": [co("What got so expensive?", 960, 150, C("what exactly"), "gold", screen=True, size=44)]})
stage("s05_what", "m1_what", {
    "zones": [Z("datacenter", -1600, 1300, darkAt=99), Z("shop", 1300, 6000, night=True, label="SPOT MARKET")], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("Most of it is sold"), "x": 1100, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("spot market"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 4,
    "items": [it("device", type="laptop", x=300, y=F, at=C("every computer")), it("device", type="phone", x=520, y=F, at=C("phone")),
              it("device", type="tv", x=760, y=F, at=C("game console")), it("device", type="server", x=1000, y=F, at=C("server")),
              it("letters", x=650, y=300, text="DRAM", at=C("called DRAM"), size=120, color="gold"),
              it("contract", x=1250, y=420, at=C("Most of it is sold"), text="SUPPLY CONTRACT", sub="price agreed every few months", scale=0.6),
              *crowd([2000, 2130, 2260], "phone", at=C("Anyone without"), tie=True),
              it("pricetag", x=2400, y=300, at=C("spot market"), pages=[[0, "$??"]], sub="today's price")],
    "callouts": [co("DRAM: the working memory of every device", 960, 150, C("called DRAM"), "white", screen=True, until=C("Most of it is sold", -0.3)),
                 co("Contracts: big buyers agree a price", 960, 150, C("Most of it is sold"), "gold", screen=True, until=C("Anyone without", -0.3)),
                 co("No contract? Spot price, whatever the day brings", 960, 150, C("Anyone without"), "risk", screen=True)]},
    sources=["teamgroup_prices"])
stage("s06_stick", "m1_stick", {
    "zones": [Z("shop", night=True, label="none")], "worldW": 1920, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.2}, {"at": C("In October"), "x": 960, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 2,
    "items": [it("ramstick", x=960, y=560, at=0.2, scale=0.95, label="16 GB", liftAt=C("eight of those chips"), hotAt=C("By September")),
              it("pricetag", x=1560, y=260, at=C("In October"), pages=[[0, "≈ $70"], [{"cue": "By September"}, "≈ $384", True]], sub="the 8 chips (our calc.)"),
              it("letters", x=380, y=280, text="×8", at=C("eight of those chips", 0.6), size=110, color="gold")],
    "callouts": [co("8 chips × 16 gigabits = 16 GB", 960, 150, C("eight of those chips"), "white", screen=True, until=C("In October", -0.3)),
                 co("Chips only: {{stick.display}} → {{stick.now_display}}", 960, 150, C("In October"), "risk", screen=True, size=42, sub="our calculation from TrendForce contract prices", until=C("only the chips", -0.3)),
                 co("…before the stick is built, shipped or shelved", 960, 960, C("only the chips"), "white", screen=True)]},
    sources=["teamgroup_prices"])
stage("s07_record", "m1_record", {
    "zones": [Z("office", -1600, 1500, night=True), Z("datacenter", 1500, 6000)], "worldW": 3200, "night": True,
    "shake": [{"at": C("largest quarterly"), "dur": 1.4, "amp": 10}],
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("Those without deals"), "x": 900, "y": 540, "zoom": 1.0, "dur": 2},
            {"at": C("Server memory"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "Q1", "2026"]], scale=0.8),
              it("chart", x=900, y=380, w=620, h=360, at=0.4, dur=3, text="PC MEMORY CONTRACT PRICE", pts=[0.1, 0.14, 0.2, 0.55, 0.95], color="risk"),
              it("stack", x=600, at=C("stockpiles shrink"), h=[[{"cue": "stockpiles shrink"}, 260], [{"cue": "stockpiles shrink", "offset": 3}, 40]], text="PC MAKERS' STOCK"),
              *crowd([1150, 1260], "worry", at=C("Those without deals"), tie=True),
              it("contract", x=2300, y=430, at=C("long-term deals"), text="LONG-TERM DEAL", sub="cloud companies lock in supply", scale=0.6)],
    "callouts": [co("PC memory: {{q1_record.display}} in one quarter (forecast)", 960, 150, C("expected contract prices"), "risk", screen=True, size=40, sub="'largest quarterly price surge on record', TrendForce", until=C("Server memory", -0.3)),
                 co("Server memory: ≈ +90%; cloud giants sign long-term deals", 960, 150, C("Server memory"), "gold", screen=True)]},
    sources=["tf_1q26"], sfx=[{"kind": "hit", "cue": "largest quarterly", "gain": 0.3}])
kinetic("s08_t1", "m1_transition", [("A price can only move like that", 50, "A price can only", None, True), ("if very few control the supply", 66, "very few people", "accent", False)])

# ====================================================================== PART 2: three companies
card("s09_c2", "m2_card", "Three Companies", "Who makes the world's memory")
stage("s10_q2", "m2_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("wafer", x=960, y=430, r=230, at=0.2, spin=8, revealAt=1.0, fail=0.05),
              it("conveyor", x0=-200, x1=2100, y=F - 40, at=0, n=8, speed=110, goods="chip")],
    "callouts": [co("Who makes the world's memory?", 960, 150, C("Who actually"), "gold", screen=True, size=44)]})
stage("s11_three", "m2_three", {
    "zones": [Z("exchange")], "worldW": 2600,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.0}, {"at": C("look at how the order"), "x": 1600, "y": 500, "zoom": 0.95, "dur": 2.6}], "drift": 0,
    "items": [it("shares", x=760, y=430, at=0.2, scale=0.82, groups=[
                  {"n": 39, "color": SAM, "label": "SAMSUNG", "at": C("Samsung took"), "step": 0.02},
                  {"n": 25, "color": HYN, "label": "SK HYNIX", "at": C("SK hynix"), "step": 0.02},
                  {"n": 23, "color": MIC, "label": "MICRON", "at": C("and Micron"), "step": 0.02},
                  {"n": 10, "color": CXM, "label": "OTHERS", "at": C("Together"), "step": 0.05}]),
              it("board", x=1800, y=80, w=760, at=C("look at how the order", -0.4), text="SHARE OF DRAM SALES",
                 rows=[{"name": "SAMSUNG", "value": "38.5% → 39.4%", "color": "gold"}, {"name": "SK HYNIX", "value": "28.8%"}, {"name": "MICRON", "value": "22.4% → 23.3%"}],
                 swap={"at": C("its share fell"), "out": 1, "in": {"name": "SK HYNIX", "value": "28.8% → 24.9%", "color": "red"}}),
              it("letters", x=760, y=150, text="≈ 88%", at=C("Together"), size=100, color="gold")],
    "callouts": [co("Q2 2026: {{big3.display}} of all DRAM sales go to three makers", 960, 960, C("Together"), "gold", screen=True, size=38, sub="TrendForce; our sum", until=C("The whole market", -0.3)),
                 co("The market: {{big3.total_display}} in one quarter", 960, 960, C("The whole market"), "white", screen=True, size=40, until=C("look at how the order", -0.3)),
                 co("AI memory kept SK hynix's prices from rising as fast", 960, 960, C("SK hynix sells"), "white", screen=True, sub="its share fell; Samsung pulled ahead")]},
    sources=["tf_2q26", "evertiq_2q26"])
add("p12_three", "m2_draw", "engine_draw", {
    "title": "Why three is a powerful number", "board": BOARD, "draw_start": C("A memory factory costs"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(540, 340, 300, 120), "color": "accent", "width": 5, "start": C("A memory factory costs"), "label": lbl("FACTORY: $ BILLIONS", 690, 405, 24, "accent")},
        {"d": rect(540, 490, 300, 120), "color": "accent", "width": 5, "start": C("takes years"), "label": lbl("YEARS TO BUILD", 690, 555, 26, "accent")},
        {"d": "M 880 470 L 980 470 M 950 440 L 980 470 L 950 500", "color": "risk", "width": 6, "start": C("nobody new"), "label": lbl("no new entrants", 930, 530, 22, "risk")},
        {"d": rect(1040, 330, 220, 90), "color": "accent2", "width": 5, "start": C("only three sellers"), "label": lbl("SELLER 1", 1150, 382, 24, "accent2")},
        {"d": rect(1040, 450, 220, 90), "color": "accent2", "width": 5, "start": C("only three sellers", 0.4), "label": lbl("SELLER 2", 1150, 502, 24, "accent2")},
        {"d": rect(1040, 570, 220, 90), "color": "accent2", "width": 5, "start": C("only three sellers", 0.8), "label": lbl("SELLER 3", 1150, 622, 24, "accent2")},
        {"d": "M 1300 380 L 1420 500 M 1300 500 L 1420 500 M 1300 620 L 1420 500", "color": "ink", "width": 4, "start": C("its own order book")},
        {"d": dot(1560, 500), "color": "accent3", "width": 1, "start": C("which customer pays"), "label": lbl("WHO PAYS MOST?", 1560, 510, 30, "accent3")},
        {"d": "M 1400 760 L 1400 700 L 1460 700 L 1460 760 M 1500 760 L 1500 640 L 1560 640 L 1560 760 M 1600 760 L 1600 560 L 1660 560 L 1660 760",
         "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("for the same silicon"), "label": lbl("bids for one wafer", 1530, 810, 22, "accent3")},
    ],
    "actions": [{"kind": "point", "at": C("which customer pays", 0.3), "dur": 1.4, "target": [1560, 500]}],
    "scale": 0.86, "floor": 1040}, sources=["tf_2q26"])
kinetic("s13_t2", "m2_transition", [("In 2026, the answer", 50, "In twenty twenty-six", None, True), ("was not you", 88, "was not you", "risk", False)])

# ====================================================================== PART 3: the customer who pays more
card("s14_c3", "m3_card", "The Customer Who Pays More", "AI, and the memory it eats")
stage("s15_q3", "m3_question", {
    "zones": [Z("datacenter")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 560, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("hbm", x=960, y=520, at=0.3, scale=0.8, dur=4, text="AI CHIP"),
              it("coins", **{"from": [-200, 300], "to": [960, 420]}, at=0.6, rate=5)],
    "callouts": [co("Who is outbidding us?", 960, 150, C("Who is outbidding"), "gold", screen=True, size=44)]})
stage("s16_hbm", "m3_hbm", {
    "zones": [Z("datacenter", -1600, 1600), Z("fab", 1600, 6000, label="yellow")], "worldW": 3200,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("making HBM takes"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("hbm", x=900, y=520, at=0.3, scale=0.85, dur=5, text="AI CHIP"),
              it("sign", x=900, y=220, text="HBM", sub="high bandwidth memory, stacked next to the processor", at=C("called HBM"), color="#BBDEFB", size=40),
              it("wafer", x=2050, y=420, r=170, at=C("making HBM takes", -0.3), spin=6),
              it("wafer", x=2450, y=420, r=170, at=C("making HBM takes"), spin=6),
              it("wafer", x=2850, y=420, r=170, at=C("making HBM takes", 0.3), spin=6),
              it("letters", x=2450, y=200, text="3×", at=C("the wafers"), size=130, color="gold"),
              it("sign", x=2450, y=740, text="$100BN HBM MARKET BY 2028", sub="Micron's forecast", at=C("Micron expects"), color="#FFF59D", size=30)],
    "callouts": [co("HBM: about {{hbm3x.display}} the wafers of DDR5", 960, 960, C("making HBM takes"), "gold", screen=True, size=40, sub="for the same amount of memory (Micron)", until=C("Micron expects", -0.3)),
                 co("Where the factories want to go", 960, 960, C("tells you where"), "white", screen=True)]},
    sources=["nextplatform_2024", "thw_micron_dec25"])
add("p17_wafer", "m3_draw", "engine_draw", {
    "title": "One wafer, two customers", "board": BOARD, "draw_start": C("Imagine one silicon wafer"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 760 520 m -170 0 a 170 170 0 1 0 340 0 a 170 170 0 1 0 -340 0", "color": "accent2", "width": 6, "start": C("Imagine one silicon wafer"), "label": lbl("ONE WAFER", 760, 740, 26, "accent2")},
        {"d": "M 640 420 L 880 420 M 610 480 L 910 480 M 600 540 L 920 540 M 610 600 L 910 600 M 700 360 L 700 680 M 760 350 L 760 690 M 820 360 L 820 680",
         "color": "accent2", "width": 2, "start": C("Cut it into ordinary memory")},
        {"d": "M 980 430 L 1100 380", "color": "ink", "width": 4, "start": C("you get a certain amount")},
        {"d": "M 1120 330 L 1120 290 L 1180 290 L 1180 330 Z M 1200 330 L 1200 290 L 1260 290 L 1260 330 Z M 1280 330 L 1280 290 L 1340 290 L 1340 330 Z",
         "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.35, "kind": "box", "start": C("you get a certain amount", 0.3), "label": lbl("3 UNITS · laptops, phones", 1230, 370, 22, "accent3")},
        {"d": "M 980 610 L 1100 660", "color": "ink", "width": 4, "start": C("Turn the same wafer")},
        {"d": "M 1120 700 L 1120 640 L 1180 640 L 1180 700 Z", "color": "accent", "width": 5, "fill": "accent", "fillOpacity": 0.4, "kind": "box",
         "start": C("about a third as much"), "label": lbl("1 UNIT · AI (pays more per bit)", 1290, 740, 22, "accent")},
        {"d": "M 1380 420 Q 1460 520 1380 640", "color": "risk", "width": 6, "start": C("Every wafer moved"), "label": lbl("less for your laptop", 1540, 540, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("about a third as much", 0.4), "dur": 1.4, "target": [1150, 670]}],
    "scale": 0.86, "floor": 1040}, sources=["nextplatform_2024"])
stage("s18_crucial", "m3_crucial", {
    "zones": [Z("shop", night=True, label="none")], "worldW": 2400, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.05}, {"at": C("even then"), "x": 1400, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "DEC", "2025"], [{"cue": "shipped until"}, "FEB", "2026"]], scale=0.8),
              it("sign", x=900, y=330, text="CRUCIAL", sub="Micron's consumer brand", at=C("Crucial consumer"), color="#E1BEE7", size=44),
              it("barrier", x=900, text="CLOSING", at=C("leaving its"), closeAt=C("shipped until")),
              it("coins", **{"from": [900, 520], "to": [2400, 300]}, at=C("larger, strategic customers"), rate=5),
              it("counter", x=1450, y=480, at=C("even then"), prefix="", suffix="", steps=[[{"cue": "even then"}, 100], [{"cue": "even then", "offset": 2.5}, 60]], text="% OF KEY CUSTOMERS' DEMAND MET",
                 until=C("wanted", 3))],
    "callouts": [co("Dec 2025: Micron leaves its Crucial consumer brand", 960, 150, C("Micron announced"), "risk", screen=True, size=38, sub="'to improve supply for larger, strategic customers'", until=C("even then", -0.3)),
                 co("Even so: only {{half_demand.display}} of key customers' demand", 960, 150, C("even then"), "gold", screen=True, size=40, sub="Micron, Dec 2025")]},
    sources=["register_crucial", "thw_micron_dec25"])
stage("s19_squeeze", "m3_squeeze", {
    "zones": [Z("shop", -1600, 1300, night=True, label="none"), Z("datacenter", 1300, 6000)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.05}, {"at": C("competing for silicon"), "x": 1400, "y": 520, "zoom": 0.85, "dur": 2.8},
            {"at": C("According to Nikkei"), "x": 1500, "y": 500, "zoom": 0.9, "dur": 2.4}], "drift": 0,
    "items": [it("device", type="phone", x=420, y=F, at=0.2), it("device", type="laptop", x=700, y=F, at=0.3),
              *crowd([960, 1080], "worry", at=C("curtailed"), tie=True),
              it("hbm", x=2100, y=520, at=0.3, scale=0.6, dur=2),
              it("coins", **{"from": [700, 560], "to": [2100, 420]}, at=C("competing for silicon"), rate=6),
              it("letters", x=1500, y=220, text="≈ 60%", at=C("According to Nikkei", 0.3), size=110, color="risk")],
    "callouts": [co("Consumer memory: supply 'significantly curtailed'", 960, 150, C("curtailed"), "risk", screen=True, size=38, sub="TrendForce, Sep 2026", until=C("competing for silicon", -0.3)),
                 co("Your phone vs the biggest data centers", 960, 150, C("competing for silicon"), "white", screen=True, until=C("According to Nikkei", -0.3)),
                 co("Makers can meet only {{nikkei.display}} of demand", 960, 150, C("According to Nikkei"), "gold", screen=True, sub="Nikkei Asia estimate (Apr 2026)")]},
    sources=["tf_2q26", "computerworld_nikkei"])
kinetic("s20_t3", "m3_transition", [("High prices attract a challenger", 54, "High prices", None, True), ("This time, one was waiting in China", 50, "one was waiting", "accent", True)])

# ====================================================================== PART 4: the challenger
card("s21_c4", "m4_card", "The Challenger", "A fourth seller")
stage("s22_q4", "m4_question", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 500, "zoom": 1.2}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("wafer", x=960, y=430, r=220, at=0.2, spin=-8, revealAt=1.2, fail=0.2),
              it("barrier", x=1500, text="HARD TO ENTER", at=0.5, closeAt=2.0)],
    "callouts": [co("Can a newcomer break in?", 960, 150, C("Can a newcomer"), "gold", screen=True, size=44)]})
stage("s23_cxmt", "m4_cxmt", {
    "zones": [Z("fab", -1600, 1300, label="red"), Z("exchange", 1300, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("In July"), "x": 2200, "y": 500, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("tower", x=700, text="CXMT", color=CXM, h=420, at=0.3, growAt=0.3),
              it("sign", x=700, y=300, text="#4 DRAM MAKER", sub="{{big3.cxmt_display}} of sales, Q2 2026", at=C("fourth largest"), color="#FFCDD2", size=34),
              it("board", x=2200, y=60, w=820, at=C("In July", -0.4), text="SHANGHAI · STAR MARKET",
                 rows=[{"name": "CXMT · LISTING DAY", "value": "$8.6bn raised"}], swap={"at": C("the shares jumped"), "out": 0, "in": {"name": "CXMT · DAY 1", "value": "+466%", "color": "gold"}}),
              it("chart", x=2200, y=560, w=600, h=320, at=C("In July"), dur=2, text="CXMT SHARES", pts=[0.1, 0.12, 0.85, 0.95]),
              it("burst", x=2200, y=350, at=C("the shares jumped", 0.4)),
              *crowd([2650, 2780], "cheer", at=C("Investors were betting"))],
    "callouts": [co("July 2026: raised {{cxmt.display}}", 960, 960, C("raised"), "gold", screen=True, size=42, sub="AP", until=C("the shares jumped", -0.3)),
                 co("Day one: {{cxmt.jump_display}}", 960, 960, C("the shares jumped"), "gold", screen=True, size=46, until=C("most valuable", -0.3)),
                 co("Mainland China's most valuable listed company (> $487bn on paper)", 960, 960, C("most valuable"), "white", screen=True, size=34)]},
    sources=["tf_2q26", "ap_cxmt"], sfx=[{"kind": "hit", "cue": "the shares jumped", "gain": 0.3}])
stage("s24_limits", "m4_limits", {
    "zones": [Z("fab", -1600, 1500, label="red"), Z("office", 1500, 6000)], "worldW": 3000,
    "cam": [{"at": 0, "x": 860, "y": 520, "zoom": 1.0}, {"at": C("Counterpoint forecasts"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("barrier", x=900, text="CHIPMAKING TOOLS: RESTRICTED", at=0.3, closeAt=C("is restricted")),
              it("sign", x=1250, y=330, text="US LAWMAKERS", sub="call to block US purchases of its chips", at=C("lawmakers"), color="#FFCDD2", size=32),
              it("shares", x=2250, y=420, at=C("Counterpoint forecasts", -0.2), scale=0.7, groups=[{"n": 11, "color": CXM, "label": "≈ 11% BY 2028 (FORECAST)", "at": C("Counterpoint forecasts"), "step": 0.1},
                  {"n": 4, "color": "#FFE0B2", "label": "NEEDS ≥ 15%", "at": C("at least fifteen"), "step": 0.15}]),
              it("letters", x=2250, y=140, text="11% < 15%", at=C("at least fifteen", 0.6), size=70, color="gold")],
    "callouts": [co("Tools restricted; US lawmakers push to block purchases", 960, 150, C("is restricted"), "risk", screen=True, size=36, until=C("Counterpoint forecasts", -0.3)),
                 co("A challenger, yes. A rescue, not yet.", 960, 960, C("A challenger, yes"), "white", screen=True, size=42)]},
    sources=["ap_cxmt"])
kinetic("s25_t4", "m4_transition", [("Is this the new normal?", 64, "So is this", None, False), ("Memory has always answered the hard way", 46, "very long history", "accent", True)])

# ====================================================================== PART 5: boom and bust
card("s26_c5", "m5_card", "Boom and Bust", "The memory cycle")
stage("s27_q5", "m5_question", {
    "zones": [Z("exchange")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 420, "zoom": 1.15}, {"at": 3.0, "x": 960, "y": 520, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("chart", x=960, y=380, w=980, h=440, at=0.2, dur=6, text="MEMORY PRICES (ILLUSTRATIVE CYCLE)", pts=[0.2, 0.6, 0.85, 0.3, 0.1, 0.25, 0.7, 0.95], color="gold")],
    "callouts": [co("What comes after a boom?", 960, 960, C("What happens"), "gold", screen=True, size=44)]})
stage("s28_2023", "m5_2023", {
    "zones": [Z("fab", -1600, 1600, label="yellow"), Z("office", 1600, 6000, night=True)], "worldW": 3200,
    "cam": [{"at": 0, "x": 2300, "y": 520, "zoom": 1.0}, {"at": C("Micron cut the wafers"), "x": 800, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "shake": [{"at": C("and it lost"), "dur": 1.4, "amp": 10}],
    "items": [it("calendar", x=1950, y=300, at=0.2, pages=[[0, "EARLY", "2023"]], scale=0.75),
              it("chart", x=2450, y=380, w=620, h=360, at=0.4, dur=1.6, text="MICRON QUARTERLY REVENUE", pts=[0.7, 0.85, 0.9], crashAt=C("Micron's revenue fell")),
              it("counter", x=2450, y=760, at=C("Micron's revenue fell"), prefix="$", suffix="bn", decimals=1, steps=[[{"cue": "Micron's revenue fell"}, 7.8], [{"cue": "Micron's revenue fell", "offset": 2.5}, 3.7]], text="ONE QUARTER, YEAR ON YEAR", until=C("For every dollar", 2)),
              it("piggy", x=2950, at=C("and it lost"), crackAt=C("and it lost", 0.6), text="LOSS $2.3BN", scale=0.85),
              it("conveyor", x0=-200, x1=1500, y=F - 40, at=0, n=7, speed=110, goods="chip", stopAt=C("Micron cut the wafers")),
              it("sign", x=700, y=330, text="WAFER STARTS −20%", at=C("Micron cut the wafers", 0.3), color="#FFCDD2", size=36),
              it("sign", x=1200, y=470, text="SAMSUNG CUTS TOO", sub="'meaningful' cut, 2023", at=C("Even Samsung"), color="#BBDEFB", size=30)],
    "callouts": [co("Q2 FY2023: revenue $7.8bn → $3.7bn, loss {{crash2023.display}}", 960, 150, C("Micron's revenue fell"), "risk", screen=True, size=36, until=C("Micron cut the wafers", -0.3)),
                 co("Production cuts across the industry", 960, 150, C("Micron cut the wafers"), "white", screen=True)]},
    sources=["thw_micron_2023", "thw_micron_cut", "fool_2023"], sfx=[{"kind": "hit", "cue": "and it lost", "gain": 0.3}])
add("p29_cycle", "m5_draw", "engine_draw", {
    "title": "The memory cycle", "board": BOARD, "draw_start": C("Prices rise"), "speed": 1500, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(1040, 300, 260, 80), "color": "accent3", "width": 5, "start": C("Prices rise"), "label": lbl("PRICES RISE", 1170, 350, 24, "accent3")},
        {"d": arrow((1310, 360), (1420, 470), -0.2), "color": "ink", "width": 4, "start": C("profits soar")},
        {"d": rect(1360, 480, 260, 80), "color": "accent", "width": 5, "start": C("Profits pay for"), "label": lbl("NEW FACTORIES", 1490, 530, 24, "accent")},
        {"d": arrow((1440, 570), (1300, 680), -0.2), "color": "ink", "width": 4, "start": C("they all arrive")},
        {"d": rect(1040, 670, 260, 80), "color": "risk", "width": 6, "start": C("Supply floods in"), "label": lbl("GLUT · PRICES CRASH", 1170, 720, 22, "risk")},
        {"d": arrow((1030, 690), (900, 580), -0.2), "color": "ink", "width": 4, "start": C("everyone cuts back")},
        {"d": rect(680, 480, 260, 80), "color": "muted", "width": 5, "start": C("everyone cuts back", 0.3), "label": lbl("CUTS", 810, 530, 26, "muted")},
        {"d": arrow((820, 470), (1030, 360), -0.2), "color": "ink", "width": 4, "start": C("shortages return")},
        {"d": dot(1170, 520), "color": "accent2", "width": 1, "start": C("the wheel turns"), "label": lbl("↻", 1170, 545, 80, "accent2")},
    ],
    "actions": [{"kind": "point", "at": C("Supply floods in", 0.3), "dur": 1.4, "target": [1170, 710]}],
    "scale": 0.86, "floor": 1040}, sources=["thw_micron_2023"])
stage("s30_next", "m5_next", {
    "zones": [Z("site", -1600, 1500), Z("fab", 1500, 6000, label="red")], "worldW": 3000,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("CXMT is expanding"), "x": 1900, "y": 520, "zoom": 1.0, "dur": 2.4},
            {"at": C("Forecasts reported"), "x": 1400, "y": 500, "zoom": 0.85, "dur": 2.6}], "drift": 3,
    "items": [it("crane", x=600, text="IDAHO FAB · MID-2027", at=0.3, progress=[[0, 0.3], [25, 0.9]], scale=0.85),
              it("crane", x=2000, text="CXMT EXPANSION", at=C("CXMT is expanding"), progress=[[0, 0.2], [25, 0.8]], scale=0.75),
              it("calendar", x=1400, y=260, at=C("Forecasts reported"), pages=[[0, "2027", "TIGHTEST?"], [{"cue": "around twenty twenty-eight"}, "2028", "BALANCE?"]], scale=0.8),
              it("sign", x=1400, y=560, text="FORECASTS, NOT FACTS", at=C("These are forecasts"), color="#FFF59D", size=36)],
    "callouts": [co("Micron's first Idaho fab: chips from mid-2027", 960, 150, C("Micron's first new plant"), "white", screen=True, until=C("CXMT is expanding", -0.3)),
                 co("Balance around 2028 (Nikkei); not before {{teamgroup_outlook.display}} (TeamGroup)", 960, 150, C("Forecasts reported"), "gold", screen=True, size=34, until=C("These are forecasts", -0.3)),
                 co("Tightest months: end-2026 to mid-2027 (TeamGroup)", 960, 960, C("tightest months"), "risk", screen=True, size=36)]},
    sources=["thw_micron_dec25", "computerworld_nikkei", "teamgroup_prices"])
# ====================================================================== PAYOFF
stage("s31_payoff", "payoff", {
    "zones": [Z("shop", night=True, label="none")], "worldW": 2200, "night": True,
    "cam": [{"at": 0, "x": 960, "y": 540, "zoom": 1.0}, {"at": C("In memory, the price"), "x": 1100, "y": 520, "zoom": 1.15, "dur": 3}], "drift": 2,
    "items": [it("ramstick", x=760, y=560, at=0.2, scale=0.6, label="16 GB"),
              it("pricetag", x=760, y=260, at=0.4, pages=[[0, "$48", True], [{"cue": "it may be you again"}, "?"]], sub="per chip"),
              it("device", type="server", x=1500, y=F, at=C("Today that customer"), scale=1.2),
              *crowd([1750, 1870, 1990, 2110], "stand", at=C("first in line"), tie=False),
              it("letters", x=1500, y=280, text="#1 IN LINE", at=C("Today that customer", 0.3), size=60, color="gold")],
    "callouts": [co("Who decides? Three companies", 960, 150, C("Three companies, each"), "white", screen=True, size=40, until=C("In memory, the price", -0.3)),
                 co("The price is about who is first in line", 960, 150, C("In memory, the price"), "gold", screen=True, size=42)]},
    sources=["tf_2q26"])
add("s32_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_memory_storyboard.py; edit the generator, not this file.\n"
           "# Episode 14 storyboard: bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
