"""Generates projects/why-elon-musk-wants-his-own-chip-factory/deliverables/documentary/storyboard.yaml (Episode 16, C3).

Bespoke worlds for Terafab (tones from visual_direction.yaml: spectacle -> strategy -> tech -> strategy -> crisis ->
reflective): a long queue of customers at one chip printer, a launch night in Austin, the new `megafab` item (a factory
that builds section by section, with the dashed outline of today's largest building), the new `orbit` set and
`satellite` item for the data centers in space, a Texas county meeting, the IPO filing on an exchange floor, and a
yield-learning board. Presenter: the printing-press queue, why chipmaking punishes newcomers, build the queue vs wait in it.
No logos (company names in text only), no likeness of any real person (Musk is a name in text only), no smiling sun.
Run: python tools/gen_terafab_storyboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cartoon_kit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parents[1] / "projects/why-elon-musk-wants-his-own-chip-factory/deliverables/documentary/storyboard.yaml"
F = 860
Z = lambda s, x0=-1600, x1=4600, **kw: {"set": s, "x0": x0, "x1": x1, **kw}
TES, SPX, TSM, SAM, INT = "#E53935", "#37474F", "#C62828", "#1565C0", "#0071C5"


def crowd(xs, pose, at=0.0, until=None, scale=0.8, **kw):
    out = []
    for k, x in enumerate(xs):
        d = {"x": x, "pose": pose, "at": at, "scale": scale, "hair": k + 3, "skin": k + 2, **kw}
        if until is not None:
            d["until"] = until
        out.append(it("person", **d))
    return out


# ====================================================================== HOOK
stage("s01_hook", "h_question", {
    "zones": [Z("hills", label="none")], "worldW": 3000,
    "cam": [{"at": 0, "x": 700, "y": 520, "zoom": 1.2}, {"at": C("the largest building"), "x": 1500, "y": 560, "zoom": 0.62, "dur": 3.2}], "drift": 0,
    "items": [it("megafab", x=1500, at=0.2, w=2600, h=240, n=14, progress=[[0, 0.05], [{"cue": "the largest building"}, 0.15], [{"cue": "just to make chips"}, 1.0]], text="TERAFAB (PLANNED)"),
              it("letters", x=700, y=430, text="0 CHIPS MADE", at=C("never made a single chip"), size=70, color="risk", until=C("the largest building", 1.5))],
    "callouts": [co("Two companies that have never made a chip…", 960, 150, C("two companies"), "white", screen=True, size=40, until=C("the largest building", -0.3)),
                 co("…plan the largest building on Earth. For chips.", 960, 150, C("the largest building"), "gold", screen=True, size=42)]})
stage("s02_stakes", "h_stakes", {
    "zones": [Z("hills", label="none")], "worldW": 3000,
    "cam": [{"at": 0, "x": 1500, "y": 560, "zoom": 0.65}, {"at": C("And the man behind it"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.6}], "drift": 3,
    "items": [it("megafab", x=1500, at=0, w=2600, h=240, n=14, progress=1, glowAt=C("first phase alone"), text="TERAFAB"),
              it("counter", x=900, y=220, at=C("first phase alone"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "first phase alone", "offset": 2}, 16.8]], text="FIRST PHASE"),
              it("counter", x=2100, y=220, at=C("A county filing"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "A county filing", "offset": 2}, 119]], text="ALL PHASES (FILING: 'MAY')")],
    "callouts": [co("First phase: {{cost.display}} (Tesla & SpaceX)", 960, 960, C("first phase alone"), "gold", screen=True, size=40, until=C("A county filing", -0.3)),
                 co("All phases: up to {{cost.total_display}} (county filing)", 960, 960, C("A county filing"), "risk", screen=True, size=40, until=C("And the man behind it", -0.3)),
                 co("Elon Musk: 'We either build it, or we don't have the chips'", 960, 960, C("And the man behind it"), "white", screen=True, size=36, sub="launch event, March 2026 (Tom's Hardware)")]},
    sources=["tx_gov", "tc_119", "thw_launch"], sfx=[{"kind": "hit", "cue": "A county filing", "gain": 0.3}])

# ====================================================================== PART 1: the bottleneck
card("s03_c1", "m1_card", "The Bottleneck", "Why buying chips is not enough")
stage("s04_q1", "m1_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 2400, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 1500, "y": 520, "zoom": 1.2}, {"at": 3.0, "x": 1200, "y": 540, "zoom": 0.85, "dur": 3.4}], "drift": 4,
    "items": [it("litho", x=1900, at=0.2, fireAt=0.6, text="CHIP FACTORY", scale=0.6),
              *crowd([1450, 1300, 1150, 1000, 850, 700, 550], "stand", at=0.4, tie=True),
              it("sign", x=900, y=300, text="QUEUE", sub="the richest buyers in tech", at=1.4, color="#FFF59D", size=36)],
    "callouts": [co("Why can't they just buy the chips?", 960, 150, C("Why can't"), "gold", screen=True, size=44)]})
stage("s05_design", "m1_design", {
    "zones": [Z("carplant", -1600, 1500), Z("fab", 1500, 6000, label="yellow")], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("But Tesla does not make them"), "x": 2000, "y": 520, "zoom": 0.85, "dur": 2.4},
            {"at": C("Samsung signed a deal"), "x": 2600, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("hbm", x=760, y=420, at=0.3, scale=0.55, dur=2, text="TESLA DESIGN"),
              it("device", type="laptop", x=480, y=F, at=C("brains of its cars")),
              it("tower", x=1750, text="SAMSUNG", color=SAM, h=420, at=C("Samsung makes the current"), scale=0.8),
              it("tower", x=2150, text="TSMC", color=TSM, h=480, at=C("TSMC in Taiwan"), scale=0.8),
              it("contract", x=2700, y=420, at=C("Samsung signed a deal"), text="$16.5BN · TO 2033", sub="Taylor, Texas", scale=0.65),
              it("calendar", x=3050, y=300, at=C("running until"), pages=[[0, "2033", "END"]], scale=0.7)],
    "callouts": [co("Tesla designs its chips. Others make them.", 960, 960, C("But Tesla does not make them"), "white", screen=True, size=40, until=C("Samsung signed a deal", -0.3)),
                 co("Samsung deal: {{suppliers.display}} through 2033", 960, 960, C("Samsung signed a deal"), "gold", screen=True, size=40, sub="Tom's Hardware")]},
    sources=["thw_samsung"])
stage("s06_rate", "m1_rate", {
    "zones": [Z("district", night=True)], "worldW": 3000, "night": True,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("By his own estimate"), "x": 1600, "y": 520, "zoom": 0.9, "dur": 2.4},
            {"at": C("His target is"), "x": 2200, "y": 500, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("sign", x=800, y=300, text="AUSTIN · MARCH 2026", sub="launch event in an old power plant", at=0.3, color="#FFE0B2", size=34),
              *crowd([500, 640, 780, 920, 1060], "cheer", at=C("At the launch event")),
              it("chart", x=1600, y=420, w=520, h=300, at=C("much less than he"), dur=2.5, text="SUPPLY GROWTH vs WANTED", pts=[0.1, 0.15, 0.2, 0.25, 0.3], color="risk"),
              it("letters", x=1600, y=200, text="2%", at=C("By his own estimate"), size=140, color="gold"),
              it("letters", x=2250, y=280, text="1 TW / YEAR", at=C("His target is"), size=80, color="purple")],
    "callouts": [co("Suppliers grow 'much less than we'd like'", 960, 960, C("much less than he"), "white", screen=True, size=38, sub="Musk, March 2026 (Tom's Hardware)", until=C("By his own estimate", -0.3)),
                 co("Today's AI output: ≈ 2% of his eventual needs (his estimate)", 960, 960, C("By his own estimate"), "gold", screen=True, size=36, until=C("His target is", -0.3)),
                 co("Target: {{launch.tw_display}} of compute", 960, 960, C("His target is"), "white", screen=True, size=40, sub="a target")]},
    sources=["thw_launch"])
add("p07_queue", "m1_draw", "engine_draw", {
    "title": "A book with no printing press", "board": BOARD, "draw_start": C("A chip designer is like"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 360, 200, 150), "color": "accent2", "width": 5, "start": C("A chip designer is like"), "label": lbl("DESIGN", 660, 445, 28, "accent2")},
        {"d": rect(1240, 340, 240, 190), "color": "accent", "width": 6, "fill": "accent", "fillOpacity": 0.15, "kind": "box", "start": C("The printers are very few"), "label": lbl("PRINTER", 1360, 445, 30, "accent")},
        {"d": " ".join(rect(800 + k * 80, 600, 56, 56) for k in range(6)), "color": "ink", "width": 3, "start": C("every big customer"),
         "label": lbl("phones · AI · cars", 1020, 700, 24, "ink")},
        {"d": arrow((1290, 620), (1340, 540)), "color": "ink", "width": 4, "start": C("the printer decides")},
        {"d": "M 1250 600 L 1300 600", "color": "risk", "width": 8, "start": C("who goes first"), "label": lbl("WHO GOES FIRST?", 1380, 780, 28, "risk")},
        {"d": rect(560, 560, 200, 150), "color": "accent3", "width": 6, "start": C("buy his own printing press"), "label": lbl("OWN PRESS", 660, 645, 26, "accent3")},
        {"d": arrow((660, 520), (660, 552)), "color": "accent3", "width": 5, "start": C("buy his own printing press", 0.3)},
    ],
    "actions": [{"kind": "point", "at": C("who goes first", 0.2), "dur": 1.4, "target": [1360, 445]}],
    "scale": 0.86, "floor": 1040}, sources=["thw_launch"])
kinetic("s08_t1", "m1_transition", [("This is not a normal printing press", 54, "But this is not", None, True), ("It is meant to do everything at once", 54, "everything at once", "accent", True)])

# ====================================================================== PART 2: everything under one roof
card("s09_c2", "m2_card", "Everything Under One Roof", "What Terafab would do")
stage("s10_q2", "m2_question", {
    "zones": [Z("fab", label="red")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("wafer", x=960, y=420, r=210, at=0.2, spin=8, revealAt=1.0, fail=0.1),
              it("conveyor", x0=-200, x1=2100, y=F - 40, at=0, n=8, speed=110, goods="chip")],
    "callouts": [co("What would Terafab do differently?", 960, 150, C("What exactly"), "gold", screen=True, size=42)]})
stage("s11_roof", "m2_roof", {
    "zones": [Z("orbit", -1600, 1900), Z("fab", 1900, 6000, label="red")], "worldW": 3600,
    "cam": [{"at": 0, "x": 960, "y": 600, "zoom": 0.8}, {"at": C("Terafab is meant to do"), "x": 2700, "y": 520, "zoom": 0.9, "dur": 2.6}], "drift": 3,
    "items": [it("plane", x=[[0, 200], [{"cue": "packaged and tested", "offset": 3}, 1700]], y=[[0, 380], [{"cue": "packaged and tested", "offset": 3}, 300]], at=C("a chip travels the world"), text="WAFERS IN TRANSIT"),
              it("sign", x=300, y=560, text="DESIGN", at=C("It is designed"), color="#BBDEFB", size=30),
              it("sign", x=900, y=560, text="PRINT", at=C("printed in a factory"), color="#FFE0B2", size=30),
              it("sign", x=1500, y=560, text="PACKAGE + TEST", at=C("packaged and tested"), color="#C8E6C9", size=30),
              it("megafab", x=2700, at=C("Terafab is meant to do", -0.3), w=1500, h=230, n=5, progress=1, glowAt=C("Design, printing"), text="ONE ROOF"),
              *[it("letters", x=2160 + k * 270, y=420, text=w, at=C("Design, printing", 0.5 * k), size=34, color="gold") for k, w in enumerate(["DESIGN", "PRINT", "MEMORY", "PACKAGE", "TEST"])],
              it("arrow", **{"from": [2250, 250], "to": [3150, 250]}, at=C("make a chip, test it"), text="FAST LOOP", color="gold")],
    "callouts": [co("Today: a chip travels the world", 960, 960, C("a chip travels the world"), "white", screen=True, size=40, until=C("Terafab is meant to do", -0.3)),
                 co("Terafab: all of it under one roof", 960, 960, C("Terafab is meant to do"), "gold", screen=True, size=40, until=C("Musk says", -0.3)),
                 co("Make, test, fix, print again", 960, 960, C("Musk says"), "white", screen=True, size=40, sub="Musk at the launch (Tom's Hardware)")]},
    sources=["electrek_launch", "thw_launch"])
stage("s12_scale", "m2_scale", {
    "zones": [Z("fab", label="red")], "worldW": 3400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("For comparison"), "x": 1900, "y": 520, "zoom": 0.85, "dur": 2.6},
            {"at": C("So the full target"), "x": 1700, "y": 500, "zoom": 0.8, "dur": 2.4}], "drift": 3,
    "items": [it("counter", x=900, y=230, at=C("The plan starts at"), steps=[[0, 0], [{"cue": "The plan starts at", "offset": 1.5}, 100000], [{"cue": "the ambition is", "offset": 0.3}, 100000], [{"cue": "the ambition is", "offset": 2.3}, 1000000]], text="WAFERS / MONTH (TARGET)"),
              *[it("wafer", x=500 + k * 200, y=520, r=80, at=C("The plan starts at", 0.15 * k), spin=10, revealAt=C("the ambition is", 0.2 * k), fail=0.1) for k in range(5)],
              it("tower", x=2300, text="TSMC 2025", color=TSM, h=[[0, 40], [{"cue": "For comparison", "offset": 1.5}, 560]], at=C("For comparison"), scale=0.85),
              it("tower", x=2700, text="TERAFAB GOAL", color=TES, h=[[0, 40], [{"cue": "So the full target", "offset": 1.5}, 400]], at=C("So the full target"), scale=0.85),
              it("letters", x=2700, y=170, text="≈ 70%", at=C("So the full target", 1.2), size=90, color="gold"),
              it("sign", x=1500, y=300, text="TARGETS, NOT OUTPUT", at=C("These are targets"), color="#FFF59D", size=34)],
    "callouts": [co("Target: {{wafers.display}} → {{wafers.full_display}} wafers", 960, 960, C("The plan starts at"), "gold", screen=True, size=36, sub="Tesla, March 2026 (Electrek)", until=C("For comparison", -0.3)),
                 co("TSMC 2025: {{tsmc_cap.display}} (≈ 1.4M a month)", 960, 960, C("For comparison"), "white", screen=True, size=38, sub="TSMC", until=C("So the full target", -0.3)),
                 co("Full goal ≈ {{tsmc_cap.pct_display}} of TSMC, in one place", 960, 960, C("So the full target"), "risk", screen=True, size=38, sub="our calculation")]},
    sources=["electrek_launch", "tsmc_capacity"])
stage("s13_two", "m2_two", {
    "zones": [Z("carplant", -1600, 1500), Z("orbit", 1500, 6000)], "worldW": 3400,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("and powerful ones"), "x": 2300, "y": 460, "zoom": 0.95, "dur": 2.6},
            {"at": C("So the factory on Earth"), "x": 1700, "y": 520, "zoom": 0.75, "dur": 2.6}], "drift": 3,
    "items": [it("device", type="phone", x=560, y=F, at=C("Small, efficient ones")),
              it("racecar", x=[[0, 200], [20, 1200]], at=C("cars drive themselves"), scale=0.6, color="red"),
              it("satellite", x=2200, y=330, at=C("data centers in orbit"), scale=0.8, rays=True, text="AI SATELLITE (PLANNED)"),
              it("satellite", x=2800, y=220, at=C("data centers in orbit", 0.5), scale=0.5),
              it("letters", x=2500, y=620, text="≈ 5× SUN", at=C("the sun shines"), size=70, color="gold"),
              it("arrow", **{"from": [1300, 700], "to": [2000, 380]}, at=C("feed computers above it"), text="CHIPS TO ORBIT", color="gold")],
    "callouts": [co("Chips for cars and robots…", 960, 960, C("Small, efficient ones"), "white", screen=True, size=40, until=C("and powerful ones", -0.3)),
                 co("…and for data centers in orbit (planned)", 960, 960, C("and powerful ones"), "gold", screen=True, size=40, until=C("Musk wants most", -0.3)),
                 co("Musk: sunlight ≈ 5× stronger in space", 960, 960, C("Musk wants most"), "white", screen=True, size=38, sub="his argument (Electrek)")]},
    sources=["tc_168", "electrek_launch", "thw_launch"])
stage("s14_small", "m2_small", {
    "zones": [Z("carplant", -1600, 1700), Z("site", 1700, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("costing"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("He also said"), "x": 2300, "y": 520, "zoom": 1.0, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "APR", "2026"]], scale=0.8),
              it("crane", x=1100, text="RESEARCH FAB · GIGA TEXAS", at=C("research fab"), progress=[[0, 0.2], [20, 0.7]], scale=0.8),
              it("counter", x=1500, y=230, at=C("costing"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "costing", "offset": 1.5}, 3]], text="RESEARCH FAB (≈)"),
              it("wafer", x=1600, y=560, r=90, at=C("a few thousand wafers"), spin=8, revealAt=C("a few thousand wafers", 0.6), fail=0.3),
              it("sign", x=2300, y=330, text="INTEL 14A", sub="'not yet totally complete'", at=C("a manufacturing process from Intel"), color="#BBDEFB", size=40)],
    "callouts": [co("First: a {{research_fab.display}} research fab", 960, 960, C("research fab"), "white", screen=True, size=40, sub="Tesla Q1 2026 call", until=C("It is meant to try", -0.3)),
                 co("'A few thousand wafers a month… to try out ideas'", 960, 960, C("It is meant to try"), "gold", screen=True, size=36, until=C("He also said", -0.3)),
                 co("Intel's 14A process: 'not yet totally complete'", 960, 960, C("He also said"), "white", screen=True, size=38, sub="Musk, April 2026")]},
    sources=["tesla_q1"])
kinetic("s15_t2", "m2_transition", [("A test factory costs billions", 62, "A test factory", None, False), ("The real one costs a lot more", 62, "The real one", "risk", False)])

# ====================================================================== PART 3: the price tag
card("s16_c3", "m3_card", "The Price Tag", "What it really costs")
stage("s17_q3", "m3_question", {
    "zones": [Z("hills", label="none")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pricetag", x=960, y=320, at=0.3, pages=[[0, "$??"]], sub="one chip factory"),
              it("coins", **{"from": [-200, 300], "to": [960, 420]}, at=0.6, rate=5)],
    "callouts": [co("How much does it really cost?", 960, 150, C("How much"), "gold", screen=True, size=44)]})
stage("s18_money", "m3_money", {
    "zones": [Z("office", -1600, 1400), Z("hills", 1400, 3000), Z("fab", 3000, 7000, label="yellow")], "worldW": 4200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("In May"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("In August"), "x": 2200, "y": 520, "zoom": 1.0, "dur": 2.2}, {"at": C("For comparison"), "x": 3500, "y": 520, "zoom": 0.95, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=500, y=300, at=0.2, pages=[[0, "MAR", "$20-25BN"], [{"cue": "In May"}, "MAY", "$55BN → $119BN"], [{"cue": "In August"}, "AUG", "$16.8BN"]], scale=0.85),
              it("docs", x=1250, y=500, at=C("a filing on the website"), text="COUNTY FILING", scale=0.7),
              it("chart", x=1300, y=330, w=420, h=240, at=C("up to"), dur=2, text="ESTIMATE ($BN)", pts=[0.2, 0.25, 0.55, 0.95], color="risk"),
              it("sign", x=2200, y=320, text="GRIMES COUNTY", sub="outside Houston", at=C("chose that county"), color="#FFE0B2", size=40),
              it("counter", x=2200, y=560, at=C("announced the first phase"), prefix="$", suffix="bn", decimals=1, steps=[[0, 0], [{"cue": "announced the first phase", "offset": 1.5}, 16.8]], text="FIRST PHASE"),
              *[it("litho", x=3200 + k * 260, at=C("TSMC plans", 0.3 * k), fireAt=C("TSMC plans", 0.3 * k + 0.4), text="TSMC", scale=0.4, color=TSM) for k in range(4)],
              it("counter", x=3600, y=200, at=C("TSMC plans"), prefix="$", suffix="bn", steps=[[0, 0], [{"cue": "TSMC plans", "offset": 1.8}, 165]], text="TSMC'S TOTAL US PLAN")],
    "callouts": [co("May: {{cost.initial_display}} at first, up to {{cost.total_display}} (county filing)", 960, 960, C("In May"), "risk", screen=True, size=36, sub="TechCrunch", until=C("In August", -0.3)),
                 co("August: first phase {{cost.display}}", 960, 960, C("In August"), "gold", screen=True, size=40, sub="Office of the Texas Governor", until=C("For comparison", -0.3)),
                 co("TSMC's whole US plan: {{tsmc_us.display}}, several fabs", 960, 960, C("For comparison"), "white", screen=True, size=38, sub="TSMC")]},
    sources=["electrek_launch", "tc_119", "tx_gov", "tsmc_us"])
stage("s19_size", "m3_size", {
    "zones": [Z("hills", label="none")], "worldW": 3000,
    "cam": [{"at": 0, "x": 1500, "y": 560, "zoom": 0.62}, {"at": C("Musk called it"), "x": 1500, "y": 540, "zoom": 0.7, "dur": 2.4},
            {"at": C("The state of Texas"), "x": 1500, "y": 520, "zoom": 0.85, "dur": 2.4}], "drift": 2,
    "items": [it("megafab", x=1500, at=0.2, w=2600, h=240, n=14, progress=[[0, 0.0], [{"cue": "SpaceX plans", "offset": 3}, 1.0]],
                 compareAt=C("The largest building"), compareW=0.65, compareText="TODAY'S LARGEST: 65M SQ FT", text="100M+ SQ FT (PLANNED)", glowAt=C("Musk called it")),
              *crowd([700, 820, 940, 1060, 1180, 1300, 1420, 1540, 1660, 1780, 1900, 2020], "walk", at=C("create"), scale=0.55),
              it("letters", x=1500, y=170, text="3,000 JOBS", at=C("create"), size=70, color="gold")],
    "callouts": [co("Planned: {{size.display}} of factory floor", 960, 960, C("SpaceX plans"), "gold", screen=True, size=40, sub="SpaceX via Dezeen", until=C("The largest building", -0.3)),
                 co("Today's largest: a car plant in Russia, ≈ 65M sq ft", 960, 960, C("The largest building"), "risk", screen=True, size=38, until=C("The state of Texas", -0.3)),
                 co("Texas: 3,000 jobs and a {{cost.grant_display}} grant", 960, 960, C("The state of Texas"), "white", screen=True, size=40, sub="Office of the Texas Governor")]},
    sources=["dezeen", "tc_168", "tx_gov"])
stage("s20_water", "m3_water", {
    "zones": [Z("hills", label="none")], "worldW": 2600,
    "cam": [{"at": 0, "x": 900, "y": 560, "zoom": 0.9}, {"at": C("SpaceX says"), "x": 1400, "y": 560, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("megafab", x=1600, at=0, w=1500, h=220, n=8, progress=1, glowAt=0.5),
              it("sign", x=500, y=600, text="GIBBONS CREEK RESERVOIR", sub="instead of groundwater", at=C("SpaceX says"), color="#B3E5FC", size=30),
              it("coins", **{"from": [500, 700], "to": [1500, 640]}, at=C("SpaceX says", 0.5), rate=4),
              *crowd([2100, 2230, 2360], "walk", at=C("most of the jobs"), scale=0.6)],
    "callouts": [co("A factory this size needs a lot of water", 960, 150, C("A chip factory also needs water"), "white", screen=True, size=40, until=C("SpaceX says", -0.3)),
                 co("Reservoir water, not groundwater (SpaceX)", 960, 150, C("SpaceX says"), "gold", screen=True, size=40, sub="TechCrunch")]},
    sources=["tc_168"])
stage("s21_county", "m3_county", {
    "zones": [Z("court")], "worldW": 2400,
    "cam": [{"at": 0, "x": 900, "y": 520, "zoom": 1.0}, {"at": C("One commissioner"), "x": 1300, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("Hundreds of residents"), "x": 1500, "y": 540, "zoom": 0.85, "dur": 2.4}], "drift": 3,
    "items": [it("calendar", x=330, y=300, at=0.2, pages=[[0, "JUN", "2026"]], scale=0.8),
              it("board", x=900, y=380, at=C("voted four to one"), text="COUNTY VOTE", rows=[{"name": "YES", "value": "4", "color": "gold"}, {"name": "NO", "value": "1"}]),
              it("letters", x=1650, y=200, text="100% TAX BREAK", at=C("exemption"), size=60, color="risk"),
              it("sign", x=1700, y=400, text="3-4% OF THE COUNTY", sub="one commissioner's estimate", at=C("One commissioner"), color="#FFE0B2", size=30),
              *crowd([1300, 1420, 1540, 1660, 1780, 1900, 2020], "worry", at=C("Hundreds of residents"), tie=False, scale=0.7)],
    "callouts": [co("4-1 vote: {{tax.display}} property-tax exemption", 960, 960, C("voted four to one"), "gold", screen=True, size=40, sub="KBTX", until=C("Hundreds of residents", -0.3)),
                 co("Residents: tax breaks, transparency", 960, 960, C("Hundreds of residents"), "risk", screen=True, size=40, sub="TechCrunch")]},
    sources=["kbtx_tax", "tc_168"])
kinetic("s22_t3", "m3_transition", [("Big promises, big money", 62, "Big promises", None, False), ("The most revealing words were written by lawyers", 44, "the most revealing", "accent", True)])

# ====================================================================== PART 4: the fine print
card("s23_c4", "m4_card", "The Fine Print", "What the filing says")
stage("s24_q4", "m4_question", {
    "zones": [Z("office", night=True)], "worldW": 1920, "night": True, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.3}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("docs", x=960, y=520, at=0.3, text="THE FILING", scale=0.9),
              it("magnifier", x=[[0, 600], [7, 1300]], y=[[0, 420], [7, 560]], at=0.6, scale=0.9)],
    "callouts": [co("How solid is the plan, really?", 960, 150, C("How solid"), "gold", screen=True, size=44)]})
stage("s25_s1", "m4_s1", {
    "zones": [Z("exchange", -1600, 1500), Z("office", 1500, 6000, night=True)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("And the filing was careful"), "x": 2200, "y": 520, "zoom": 1.05, "dur": 2.4}], "drift": 3,
    "items": [it("ticker", y=110, at=0.3, items=["SPACEX FILES TO GO PUBLIC", "MAY 2026", "S-1 REGISTRATION STATEMENT"]),
              it("docs", x=2200, y=520, at=C("And the filing was careful", -0.3), text="S-1 · RISK FACTORS", scale=0.85),
              it("sign", x=1900, y=360, text="'VERY EARLY STAGES'", sub="SpaceX S-1", at=C("very early stages"), color="#FFF59D", size=34),
              it("sign", x=2800, y=330, text="ONLY A FRAMEWORK", sub="money, timing, IP: to be negotiated", at=C("general framework"), color="#FFCDD2", size=32),
              it("letters", x=2500, y=700, text="NOT OBLIGATED", at=C("neither Tesla nor Intel"), size=60, color="risk")],
    "callouts": [co("Selling shares means telling investors the risks", 960, 960, C("A company that sells shares"), "white", screen=True, size=38, until=C("very early stages", -0.3)),
                 co("Terafab: 'in the very early stages'", 960, 960, C("very early stages"), "gold", screen=True, size=40, sub="SpaceX S-1 (via Electrek)", until=C("neither Tesla nor Intel", -0.3)),
                 co("'Neither Tesla nor Intel are obligated to remain'", 960, 960, C("neither Tesla nor Intel"), "risk", screen=True, size=38)]},
    sources=["electrek_s1"])
stage("s26_tangle", "m4_tangle", {
    "zones": [Z("datacenter", -1600, 1500), Z("carplant", 1500, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 1600, "y": 520, "zoom": 0.8}, {"at": C("The AI company xAI"), "x": 900, "y": 520, "zoom": 0.95, "dur": 2.4},
            {"at": C("Terafab would tie"), "x": 1600, "y": 520, "zoom": 0.8, "dur": 2.4}], "drift": 3,
    "items": [it("tower", x=900, text="SPACEX + xAI", color=SPX, h=460, at=0.2, scale=0.8),
              it("tower", x=2300, text="TESLA", color=TES, h=420, at=0.4, scale=0.8),
              it("coins", **{"from": [900, 400], "to": [2300, 400]}, at=C("SpaceX bought"), rate=3, until=C("The AI company xAI")),
              it("coins", **{"from": [900, 300], "to": [2300, 300]}, at=C("The AI company xAI"), rate=7, until=C("Terafab would tie", 2)),
              it("counter", x=1600, y=180, at=C("SpaceX bought"), prefix="$", suffix="M", steps=[[0, 4], [{"cue": "SpaceX bought", "offset": 2}, 144]], text="SPACEX ← TESLA (2025)"),
              it("counter", x=1600, y=620, at=C("The AI company xAI"), prefix="$", suffix="M", steps=[[0, 0], [{"cue": "The AI company xAI", "offset": 2}, 506]], text="xAI ← TESLA (2025)"),
              it("arrow", **{"from": [1150, 440], "to": [2050, 440]}, at=C("Terafab would tie"), text="TERAFAB", color="gold")],
    "callouts": [co("2025: SpaceX bought $144M from Tesla (2024: $4M)", 960, 960, C("SpaceX bought"), "white", screen=True, size=36, sub="SpaceX S-1 (via Electrek)", until=C("The AI company xAI", -0.3)),
                 co("xAI: {{tangle.display}} from Tesla, mostly batteries", 960, 960, C("The AI company xAI"), "gold", screen=True, size=40, until=C("Terafab would tie", -0.3)),
                 co("Terafab would tie them tighter still", 960, 960, C("Terafab would tie"), "white", screen=True, size=40)]},
    sources=["electrek_s1"])
stage("s27_doubts", "m4_doubts", {
    "zones": [Z("newsroom", -1600, 1600), Z("orbit", 1600, 6000)], "worldW": 3200,
    "cam": [{"at": 0, "x": 760, "y": 520, "zoom": 1.0}, {"at": C("compared the event"), "x": 900, "y": 520, "zoom": 0.95, "dur": 2.2},
            {"at": C("And Musk said"), "x": 2300, "y": 460, "zoom": 0.95, "dur": 2.6}], "drift": 3,
    "items": [it("press", x=760, y=480, at=0.3, text="ELECTREK (OPINION)", scale=0.75),
              it("letters", x=1100, y=230, text="0 CHIPS MADE", at=C("no experience making chips"), size=60, color="risk"),
              it("calendar", x=1300, y=520, at=C("battery day"), pages=[[0, "2020", "BATTERY DAY"]], scale=0.7),
              it("satellite", x=2300, y=330, at=C("AI satellites in space"), scale=0.75, rays=True, text="80% OF THE COMPUTE?"),
              it("letters", x=2300, y=640, text="?", at=C("still has to prove"), size=140, color="gold")],
    "callouts": [co("Electrek: no experience making chips", 960, 960, C("Electrek pointed out"), "white", screen=True, size=40, sub="opinion", until=C("And Musk said", -0.3)),
                 co("Musk: {{doubts.display}}, an unproven idea", 960, 960, C("And Musk said"), "risk", screen=True, size=40)]},
    sources=["electrek_launch"])
add("p28_yield", "m4_draw", "engine_draw", {
    "title": "Why chipmaking punishes newcomers", "board": BOARD, "draw_start": C("A factory must be built"), "speed": 1400, "push": 0.003,
    "enter": {"from": 2200, "to": 1620, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": "M 560 820 L 1500 820 M 560 820 L 560 330", "color": "ink", "width": 4, "start": C("A factory must be built"), "label": lbl("time →", 1450, 860, 22, "ink")},
        {"d": rect(590, 700, 200, 110), "color": "risk", "width": 5, "fill": "risk", "fillOpacity": 0.2, "kind": "box", "start": C("before it earns"), "label": lbl("BUILD: $ OUT", 690, 760, 22, "risk")},
        {"d": "M 820 790 Q 950 780 1050 640 Q 1150 470 1450 400", "color": "accent3", "width": 7, "start": C("Then it must learn"), "label": lbl("GOOD CHIPS %", 1340, 370, 24, "accent3")},
        {"d": " ".join(f"M {x} {y} l 14 14 M {x + 14} {y} l -14 14" for x, y in [(860, 740), (900, 760), (940, 720), (980, 750)]), "color": "risk", "width": 4,
         "start": C("many broken chips"), "label": lbl("broken chips", 920, 700, 22, "risk")},
        {"d": "M 900 810 L 900 740 L 960 740 L 960 810 M 1040 810 L 1040 640 L 1100 640 L 1100 810 M 1180 810 L 1180 520 L 1240 520 L 1240 810 M 1320 810 L 1320 430 L 1380 430 L 1380 810",
         "color": "accent3", "width": 4, "fill": "accent3", "fillOpacity": 0.3, "kind": "bar", "start": C("Every month"), "label": lbl("good chips per wafer", 1140, 860, 20, "accent3")},
        {"d": "M 1100 600 L 1500 600", "color": "accent", "width": 4, "start": C("the money start to come back"), "label": lbl("money comes back", 1300, 585, 22, "accent")},
        {"d": arrow((1480, 470), (1480, 400)), "color": "accent2", "width": 5, "start": C("The companies at the top"), "label": lbl("LEADERS: DECADES UP HERE", 1250, 340, 22, "accent2")},
        {"d": dot(600, 800), "color": "risk", "width": 1, "start": C("A newcomer starts"), "label": lbl("NEWCOMER", 640, 870, 24, "risk")},
    ],
    "actions": [{"kind": "point", "at": C("A newcomer starts", 0.2), "dur": 1.4, "target": [600, 800]}],
    "scale": 0.86, "floor": 1040}, sources=["tesla_q1"])
kinetic("s29_t4", "m4_transition", [("So why take the risk?", 66, "So why take", None, False), ("Because of who controls the chips today", 48, "Because of who", "accent", True)])

# ====================================================================== PART 5: owning the factory
card("s30_c5", "m5_card", "Owning the Factory", "Build it or buy it")
stage("s31_q5", "m5_question", {
    "zones": [Z("fab", label="yellow")], "worldW": 1920, "min_seconds": 9.0,
    "cam": [{"at": 0, "x": 960, "y": 520, "zoom": 1.25}, {"at": 3.0, "x": 960, "y": 540, "zoom": 1.0, "dur": 3.0}], "drift": 3,
    "items": [it("pricetag", x=600, y=320, at=0.3, pages=[[0, "BUY"]], sub="a customer"),
              it("pricetag", x=1350, y=320, at=0.8, pages=[[0, "BUILD"]], sub="an owner")],
    "callouts": [co("When should you build what you could buy?", 960, 150, C("When does it make sense"), "gold", screen=True, size=40)]})
add("p32_why", "m5_why", "engine_draw", {
    "title": "Wait in the queue, or own it?", "board": BOARD, "draw_start": C("For years"), "speed": 1400, "push": 0.003,
    "enter": {"from": -260, "to": 430, "at": 0.2, "dur": 1.3},
    "strokes": [
        {"d": rect(560, 340, 220, 120), "color": "accent2", "width": 5, "start": C("Design the chip yourself"), "label": lbl("DESIGN", 670, 410, 26, "accent2")},
        {"d": arrow((790, 400), (930, 400)), "color": "ink", "width": 4, "start": C("let a specialist make it")},
        {"d": rect(940, 340, 240, 120), "color": "accent", "width": 5, "start": C("let a specialist make it", 0.3), "label": lbl("SPECIALIST FAB", 1060, 410, 24, "accent")},
        {"d": "M 1200 400 L 1300 400", "color": "accent3", "width": 6, "start": C("It saved billions"), "label": lbl("saves $ billions", 1320, 380, 22, "accent3", "start")},
        {"d": " ".join(rect(620 + k * 70, 560, 50, 50) for k in range(8)), "color": "risk", "width": 3, "start": C("fighting for"), "label": lbl("EVERY AI COMPANY IN LINE", 900, 650, 24, "risk")},
        {"d": rect(1240, 520, 220, 130), "color": "accent3", "width": 6, "fill": "accent3", "fillOpacity": 0.2, "kind": "box", "start": C("Owning the factory means"), "label": lbl("OWN THE LINE", 1350, 590, 26, "accent3")},
        {"d": "M 600 760 L 1460 760", "color": "accent", "width": 5, "start": C("That is the bet"), "label": lbl("not cheaper: no waiting", 1030, 810, 28, "accent")},
    ],
    "actions": [{"kind": "point", "at": C("Owning the factory means", 0.3), "dur": 1.4, "target": [1350, 590]}],
    "scale": 0.86, "floor": 1040}, sources=["thw_launch", "thw_samsung"])
stage("s33_still", "m5_still", {
    "zones": [Z("fab", label="yellow")], "worldW": 2800,
    "cam": [{"at": 0, "x": 1400, "y": 520, "zoom": 0.8}, {"at": C("Until it"), "x": 1100, "y": 540, "zoom": 1.0, "dur": 2.6}], "drift": 3,
    "items": [it("tower", x=1900, text="TSMC", color=TSM, h=480, at=C("TSMC, Samsung and Micron"), scale=0.7),
              it("tower", x=2200, text="SAMSUNG", color=SAM, h=420, at=C("TSMC, Samsung and Micron", 0.3), scale=0.7),
              it("tower", x=2500, text="MICRON", color="#7E57C2", h=380, at=C("TSMC, Samsung and Micron", 0.6), scale=0.7),
              it("calendar", x=600, y=300, at=C("He gave no date"), pages=[[0, "CHIPS?", "NO DATE"]], scale=0.8),
              *crowd([1700, 1560, 1420, 1280, 1140, 1000, 860], "stand", at=C("same line"), tie=True, scale=0.7),
              it("sign", x=1000, y=320, text="TESLA (IN LINE)", at=C("same line", 0.4), color="#FFCDD2", size=32)],
    "callouts": [co("Still buying from TSMC, Samsung and Micron", 960, 960, C("TSMC, Samsung and Micron"), "white", screen=True, size=40, sub="Musk, March 2026", until=C("He gave no date", -0.3)),
                 co("No date for Terafab's first chips", 960, 960, C("He gave no date"), "gold", screen=True, size=40)]},
    sources=["thw_launch"])

# ====================================================================== PAYOFF
stage("s34_payoff", "payoff", {
    "zones": [Z("hills", label="none")], "worldW": 3000,
    "cam": [{"at": 0, "x": 1500, "y": 560, "zoom": 0.65}, {"at": C("It is a place"), "x": 1100, "y": 540, "zoom": 0.9, "dur": 3},
            {"at": C("Whether it pays off"), "x": 1500, "y": 560, "zoom": 0.65, "dur": 3}], "drift": 2,
    "items": [it("megafab", x=1500, at=0.2, w=2600, h=240, n=14, progress=[[0, 0.1], [{"cue": "Terafab is a bet", "offset": 4}, 0.7]], text="TERAFAB"),
              *crowd([600, 740, 880, 1020, 1160], "stand", at=C("factory queue"), tie=True, scale=0.6),
              it("letters", x=1500, y=170, text="A PLACE IN THE QUEUE", at=C("It is a place"), size=56, color="gold"),
              it("letters", x=2400, y=330, text="?", at=C("still to be negotiated"), size=130, color="risk")],
    "callouts": [co("Not a good business for a newcomer…", 960, 150, C("Not because making chips"), "white", screen=True, size=40, until=C("It is a place", -0.3)),
                 co("…the scarcest thing is a place in the queue", 960, 150, C("It is a place"), "gold", screen=True, size=40, until=C("Whether it pays off", -0.3)),
                 co("The fine print: still to be negotiated", 960, 150, C("Whether it pays off"), "risk", screen=True, size=40)]},
    sources=["tc_119", "electrek_s1"])
add("s35_end", "teaser", "end_card", {"words": ["Next time:", "another hidden link of the world economy"], "brand": "The Hidden Economics",
    "teaser": "Every figure in this film is sourced in the description", "brand_cue": {"cue": "This is The Hidden Economics"}})
write(OUT, "# GENERATED by tools/gen_terafab_storyboard.py; edit the generator, not this file.\n"
           "# Episode 16 storyboard (chip series C3): bespoke CartoonStage worlds; tones from visual_direction.yaml.\n")
